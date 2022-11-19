from psycopg2 import connect
from prompt_toolkit import PromptSession, print_formatted_text as print, HTML
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.validation import Validator, ValidationError, DummyValidator
from prompt_toolkit.key_binding import KeyBindings
from download import Download
from humanize import naturalsize
import re


class SearchPrompt:
    offset: int = 0
    num: int = 20
    db = connect("port=5433 dbname=alibrary").cursor()
    total: int = 0
    limit: int = 300
    skip: bool = False
    session = PromptSession()
    search_text: str = ''
    docs = []
    bindings = KeyBindings()

    def __init__(self, search_text: str = None):

        @self.bindings.add('c-n')
        def _(event):
            " Show the next page when `c-n` is pressed. "
            self.skip = True
            self.retrieve()

        @self.bindings.add('c-p')
        def _(event):
            " Show the previous page when `c-p` is pressed. "
            self.skip = True
            self.offset = max(self.offset - 2 * self.num, 0)
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
                self.skip = False
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
        print('')
        if self.search_text is not None and not self.skip:
            self.offset = 0
            self.db.execute("SELECT id,name,size FROM record WHERE tsv @@ to_tsquery('jiebacfg', %s) LIMIT %s;", (self.search_text, self.limit))
            self.docs = self.db.fetchall()
            self.total = len(self.docs)
        HTML('We have in total <b>' + str(len(self.docs)) + '</b> results')
        start_idx = self.offset
        for idx in range(start_idx, min(self.total, self.num + start_idx)):
            print(FormattedText([('#E9CD4C', str(self.offset + 1).ljust(6)),
                                 ('#2EA9DF', self.docs[self.offset][1]),
                                 ('#707C74', '  ' + naturalsize(int(self.docs[self.offset][2]) * 1024, binary=True))]))
            self.offset += 1

    def download_prompt(self):
        if self.total > 0:
            idx: str = self.session.prompt('Please choose files to download: ',
                                           key_bindings=self.bindings,
                                           validator=NumberValidator(self.total),
                                           validate_while_typing=False,
                                           enable_history_search=True)
            if idx is not None:
                for id in parseRange(idx):
                    doc = self.docs[id - 1]
                    Download(share_index=doc[0], file_name=doc[1])
        else:
            self.search_text = None


class NumberValidator(Validator):
    up_limit: int = 0
    down_limit: int = 0

    def __init__(self, up_limit: int, down_limit: int = 0):
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
