from redis.commands.search.query import Query
from redis.exceptions import BusyLoadingError
from type import AliShareInfo
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
import json
import importlib
from time import sleep

Search = importlib.import_module("redis-stubs.commands.search")


class SearchHanlder(BaseHTTPRequestHandler):
    offset: int = 0
    num: int = 200
    load_retry: int = 60
    load_wait: int = 2
    total: int = 0
    index: Search = AliShareInfo.db().ft(index_name=':type.AliShareInfo:index')
    search_text: str = ''

    def do_GET(self):
        self.search_text = unquote(self.path.split('?')[1])
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(self.retrieve())

    def retrieve(self):
        if self.search_text is not None:
            load_time = 0
            results = None
            while load_time < self.load_retry and results is None:
                try:
                    results = self.index.search(
                        Query(self.search_text).language('chinese').paging(
                            self.offset, self.num))
                except BusyLoadingError:
                    results = None
                    load_time = load_time + 1
                    sleep(self.load_wait)
            return json.dumps(
                [{'name': doc.name, 'size': doc.size, 'file_id': doc.file_id, 'share_id': doc.share_id}
                 for doc in results.docs]
            ).encode('utf-8')


def run(server_class=HTTPServer, handler_class=SearchHanlder):
    server_address = ('', int(os.getenv('PORT') or 8080))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
