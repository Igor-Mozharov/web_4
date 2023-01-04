import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from urllib.parse import unquote_plus, parse_qs
from socket_server import  run_client
import  socket

template_path = 'templates/'

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def send_html_file(self, filename, status_code=200):
        self.send_response(status_code,)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(os.path.join(template_path, filename), 'rb') as file:
            self.wfile.write(file.read())

    def send_static(self, filepath, status_code=200):
        self.send_response(status_code)
        mt = mimetypes.guess_type(filepath)
        if mt:
            self.send_header('Content-type', mt)
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(filepath, 'rb') as file:
            self.wfile.write(file.read())

    def do_GET(self):
        print(f'{self.path}')
        if self.path == '/':
            self.send_html_file('index.html')
        elif self.path == '/message':
            self.send_html_file('message.html')
        else:
            if os.path.exists(os.path.join('static', self.path[1:])):
                self.send_static(os.path.join('static', self.path[1:]))
            else:
                self.send_html_file('error.html')

    def do_POST(self):
        inputs = self.rfile.readline(int(self.headers['Content-Length']))
        # print(f'{data=}')
        query_data = unquote_plus(inputs.decode())
        print(f'{parse_qs(query_data)}=')
        data = parse_qs(query_data)
        res = run_client('127.0.0.1', 5000, data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


def run():
    http = HTTPServer(('127.0.0.1', 3000), CustomHTTPRequestHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
