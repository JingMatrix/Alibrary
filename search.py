#! /bin/python3
from psycopg2 import connect
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
import json


class SearchHanlder(BaseHTTPRequestHandler):
    offset: int = 0
    limit: int = 500
    total: int = 0
    db = connect("port=5433 dbname=alibrary").cursor()
    search_text: str = ''
    docs = []

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        path = self.path.split('?')
        if len(path) == 2:
            self.search_text = unquote(self.path.split('?')[1])
            self.wfile.write(self.retrieve())
        else:
            self.wfile.write('{"erorr": "Invalid query format"}'.encode())

    def retrieve(self):
        if self.search_text is not None:
            self.docs = []
            self.db.execute("SELECT id,name,size FROM record WHERE tsv @@ to_tsquery('jiebacfg', %s) LIMIT %s;", (self.search_text, self.limit))
            self.docs = self.db.fetchall()
        return json.dumps(
            [{'name': doc[1], 'size': int(doc[2]) * 1024, 'file_id': doc[0].split(':')[0], 'share_id': doc[0].split(':')[1]}
             for doc in self.docs]
        ).encode('utf-8')


def run(server_class=HTTPServer, handler_class=SearchHanlder):
    server_address = ('', int(os.getenv('PORT') or 8080))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
