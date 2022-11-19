#! /bin/python3
from psycopg2 import connect
from psycopg2.errors import SyntaxError
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
import json


class SearchHanlder(BaseHTTPRequestHandler):
    offset: int = 0
    limit: int = 500
    total: int = 0
    db = connect("dbname=alibrary").cursor()
    search_text: str = ''
    sql: str = "SELECT id,name,size FROM record WHERE tsv @@ to_tsquery('jiebacfg', %s) LIMIT %s;"
    docs = []
    result = '{"erorr": "Invalid query format"}'.encode()

    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'
        path = self.path.split('?')
        if len(path) == 2:
            self.search_text = unquote(self.path.split('?')[1]).strip()
            self.result = self.retrieve()
        else:
            self.send_response(400)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(self.result)

    def retrieve(self):
        if self.search_text is not None:
            self.docs = []
            if ' ' in self.search_text and '&' not in self.search_text and '|' not in self.search_text and '<->' not in self.search_text and '!' not in self.search_text:
                self.search_text = ' & '.join(self.search_text.split())
            try:
                self.db.execute(self.sql, (self.search_text, self.limit))
            except SyntaxError as e:
                self.send_response(400)
                return json.dumps({"error": str(e).strip()}).encode()

            self.docs = self.db.fetchall()
        self.send_response(200)
        return json.dumps([{
            'name': doc[1],
            'size': int(doc[2]) * 1024,
            'file_id': doc[0].split(':')[1],
            'share_id': doc[0].split(':')[0]
        } for doc in self.docs]).encode('utf-8')


def run(server_class=HTTPServer, handler_class=SearchHanlder):
    server_address = ('', int(os.getenv('PORT') or 8080))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
