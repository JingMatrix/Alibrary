from redis_om import redis
from redis.commands.search.query import Query
from redis.commands.search.document import Document
from prompt_toolkit import PromptSession, print_formatted_text as print, HTML
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.key_binding import KeyBindings
from download import Download
import importlib
Search = importlib.import_module("redis-stubs.commands.search")


class SearchPrompt:
    offset: int = 0
    num: int = 5
    total: int = 0
    index: Search = None
    session = PromptSession()
    docs: [Document] = []
    search_text: str = ''
    bindings = KeyBindings()

    def __init__(self, db: redis.Redis, search_text: str = None):

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
            " Invoke new searches when `c-d` is pressed. "
            self.search_prompt()

        @self.bindings.add('c-d')
        def _(event):
            " Exit when `c-d` is pressed. "
            event.app.exit()

        print(HTML('Gald to see you here! We offer the following keyboard shortcuts:'))
        print(HTML('<u>Ctrl-N</u>: Next Page \t<u>Ctrl-P</u>: Previous Page'))
        print(HTML('<u>Ctrl-S</u>: New Search\t<u>Ctrl-D</u>: Exit'))
        print('')
        self.search_text = search_text
        self.index = db.ft(index_name=':type.AliShareInfo:index')
        if self.search_text is None:
            self.search_prompt()
            self.download_prompt()
        else:
            self.retrieve()
            self.download_prompt()

    def search_prompt(self):
        self.search_text = self.session.prompt('Please enter a string to invoke search: ',
                                               key_bindings=self.bindings)
        self.retrieve()

    def retrieve(self):
        results = self.index.search(Query(self.search_text).
                                    language('chinese').
                                    paging(self.offset, self.num))
        self.docs = results.docs
        self.total = results.total
        print(HTML('We have in total <b>' + str(self.total) + '</b> results'))
        for idx, doc in enumerate(self.docs):
            print(idx + self.offset + 1, doc.name)

    def download_prompt(self):
        idx: int = self.session.prompt('Please choose a file to download: ',
                                       key_bindings=self.bindings,
                                       validator=NumberValidator(self.offset + 1, self.offset + self.num),
                                       validate_while_typing=False)
        if idx is not None:
            Download(self.docs[int(idx) - self.offset - 1])
        print(HTML("Goodbye! You can always invoke new searches using <i>python3 aliyun_share SEARCHTEXT</i>."))


class NumberValidator(Validator):
    up_limit: int = 0
    down_limit: int = 0

    def __init__(self, down_limit: int, up_limit: int):
        self.up_limit = up_limit
        self.down_limit = down_limit

    def validate(self, document):
        text = document.text

        if not text.isdigit():
            raise ValidationError(message='This input contains non-numeric characters')
        elif int(text) > self.up_limit or int(text) < self.down_limit:
            raise ValidationError(message='The input index should be between ' +
                                  str(self.down_limit) + ' and ' +
                                  str(self.up_limit) + '.')
