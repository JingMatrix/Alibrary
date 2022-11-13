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

    def do_SEARCH(self):
        type = self.headers.get('Content-Type')
        if type is not None and type == 'application/x-www-form-urlencoded':
            length = int(self.headers.get('Content-Length'))
            self.search_text = unquote(self.rfile.read(length), encoding='utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(self.retrieve())

    def do_RELAY(self):
        type = self.headers.get('Content-Type')
        if type is not None and type == 'application/json':
            length = int(self.headers.get('Content-Length'))
            param = json.loads(self.rfile.read(length))
            if 'file_id' in param:
                hash = ':type.AliShareInfo:' + param['file_id']
                if AliShareInfo.db().exists(hash):
                    self.send_response(200)
                    self.end_headers()
                    share_id = AliShareInfo.db().hget(hash, 'share_id')
                    self.wfile.write(Relay(file_id=param['file_id'], share_id=share_id).encode('utf-8'))

    def retrieve(self):
        if self.search_text is not None:
            reuslts = self.index.search(
                Query(self.search_text).language('chinese').paging(
                    self.offset, self.num))
            return json.dumps(
                {'total': reuslts.total,
                 'docs': [{'name': doc.name, 'size': doc.size, 'file_id': doc.file_id}
                          for doc in reuslts.docs]}
            ).encode('utf-8')


def run(server_class=HTTPServer, handler_class=SearchHanlder):
    server_address = ('', int(os.getenv('PORT') or 8080))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
