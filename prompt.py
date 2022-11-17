from redis_om import redis
from redis import Redis
from redis.commands.search.query import Query
from redis.commands.search.document import Document
from prompt_toolkit import PromptSession, print_formatted_text as print, HTML
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.validation import Validator, ValidationError, DummyValidator
from prompt_toolkit.key_binding import KeyBindings
from download import Download
from humanize import naturalsize
import importlib
import re

Search = importlib.import_module("redis-stubs.commands.search")


class SearchPrompt:
    offset: int = 0
    num: int = 20
    db: Redis = None
    total: int = 0
    index: Search = None
    session = PromptSession()
    docs: [Document] = []
    search_text: str = ''
    bindings = KeyBindings()

    def __init__(self, db: redis.Redis, search_text: str = None):

        self.db = db

        @self.bindings.add('c-n')
        def _(event):
            " Show the next page when `c-n` is pressed. "
            self.offset = min(self.offset + self.num, self.total - 1)
            self.retrieve()

        @self.bindings.add('c-p')
        def _(event):
            " Show the previous page when `c-p` is pressed. "
            self.offset = max(self.offset - self.num, 0)
            self.retrieve()

        @self.bindings.add('c-s')
        def _(event):
            " Invoke new searches when `c-s` is pressed. "
            self.search_text = None
            self.offset = 0
            event.app.exit()

        @self.bindings.add('c-d')
        def _(event):
            " Exit when `c-d` is pressed. "
            event.app.exit()
            self.session = None

        print(
            HTML(
                'Gald to see you here! We offer the following keyboard shortcuts:'
            ))
        print(HTML('<u>Ctrl-N</u>: Next Page \t<u>Ctrl-P</u>: Previous Page'))
        print(HTML('<u>Ctrl-S</u>: New Search\t<u>Ctrl-D</u>: Exit'))
        self.search_text = search_text

        while True:
            if self.search_text is None:
                self.search_prompt()
            else:
                self.retrieve()
                self.download_prompt()
            print('')
            if self.session is None:
                break

        print(
            HTML(
                "Goodbye! You can always invoke new searches using <i>python3 aliyun_share SEARCHTEXT</i>."
            ))

    def search_prompt(self):
        self.search_text = self.session.prompt(
            'Please enter a string to invoke search: ',
            key_bindings=self.bindings,
            validator=DummyValidator(),
            enable_history_search=True)

    def retrieve(self):
        if self.search_text is not None:
            self.total = 0
            self.docs = []
            for index in self.db.execute_command('ft._list'):
                self.index = self.db.ft(index_name=index)
                results = self.index.search(
                    Query(self.search_text).language('chinese').paging(
                        self.offset, self.num))
                self.docs += results.docs
                self.total += results.total
                print(
                    HTML('We have in total <b>' + str(self.total) +
                         '</b> results'))
        for idx, doc in enumerate(self.docs):
            print(FormattedText([('#E9CD4C', str(idx + self.offset + 1).ljust(6)),
                                 ('#2EA9DF', doc.n),
                                 ('#707C74', '  ' + naturalsize(int(doc.s) * 1024, binary=True))]))

    def download_prompt(self):
        if self.total > 0:
            idx: str = self.session.prompt('Please choose files to download: ',
                                           key_bindings=self.bindings,
                                           validator=NumberValidator(
                                               self.offset + 1,
                                               min(self.offset + self.num, self.total)),
                                           validate_while_typing=False,
                                           enable_history_search=True)
            if idx is not None:
                for id in parseRange(idx):
                    doc = self.docs[id - self.offset - 1]
                    Download(share_index=doc.id, file_name=doc.n)
        else:
            self.search_text = None


class NumberValidator(Validator):
    up_limit: int = 0
    down_limit: int = 0

    def __init__(self, down_limit: int, up_limit: int):
        self.up_limit = up_limit
        self.down_limit = down_limit

    def validate(self, document):
        text = document.text

        if re.match("^[-0-9 ,<]*$", text) is None:
            raise ValidationError(
                message='This input contains non-numeric characters.')
        else:
            try:
                ids = parseRange(text)
            except ValueError:
                raise ValidationError(
                    message='Bad range syntax.')

        for id in ids:
            if id > self.up_limit or id < self.down_limit:
                raise ValidationError(
                    message=str(id) + " is not between " +
                    str(self.down_limit) + ' and ' + str(self.up_limit) + '.')


def parseRange(rng: str):
    ids = set()
    for x in rng.split(','):
        x = x.strip()
        if x.isdigit():
            ids.add(int(x))
            continue
        if x[0] == '<':
            for n in range(1, int(x[1:]) + 1):
                ids.add(n)
            continue
        if '-' in x:
            xr = [n.strip() for n in x.split('-')]
            for n in range(int(xr[0]), int(xr[len(xr) - 1]) + 1):
                ids.add(n)
        else:
            raise ValueError('Unknown range type: ', x)
    return ids
