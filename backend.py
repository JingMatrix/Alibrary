from redis.commands.search.query import Query
from type import AliShareInfo
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
import json
import importlib
from relay import Relay

Search = importlib.import_module("redis-stubs.commands.search")


class SearchHanlder(BaseHTTPRequestHandler):
    offset: int = 0
    num: int = 200
    total: int = 0
    index: Search = AliShareInfo.db().ft(index_name=':type.AliShareInfo:index')
    search_text: str = ''

    def do_GET(self):
        print(self.path)
        self.search_text = unquote(self.path.split('?')[1])
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(self.retrieve())

    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        file_id = self.rfile.read(length).decode('utf-8')
        hash = ':type.AliShareInfo:' + file_id
        if AliShareInfo.db().exists(hash):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            share_id = AliShareInfo.db().hget(hash, 'share_id')
            self.wfile.write(Relay(file_id=file_id, share_id=share_id).encode('utf-8'))

    def retrieve(self):
        if self.search_text is not None:
            reuslts = self.index.search(
                Query(self.search_text).language('chinese').paging(
                    self.offset, self.num))
            return json.dumps(
                [{'name': doc.name, 'size': doc.size, 'file_id': doc.file_id}
                 for doc in reuslts.docs]
            ).encode('utf-8')


def run(server_class=HTTPServer, handler_class=SearchHanlder):
    server_address = ('', int(os.getenv('PORT') or 8080))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
