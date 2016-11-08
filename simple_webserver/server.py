# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class base_case(object):
    """Parent for case handlers."""

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        raise NotImplementedError

    def act(self, handler):
        raise NotImplementedError


class case_no_file(base_case):
    """File or directory does not exist."""

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise BaseException("'{0}' not found".format(handler.path))


class case_existing_file(base_case):
    """File exists."""

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)


class case_always_fail(base_case):
    """Base case if nothing else worked."""

    def test(self, handler):
        return True

    def act(self, handler):
        raise BaseException("Unknown object '{0}'".format(handler.path))


class case_directory_index_file(base_case):
    """Serve index.html page for a directory."""

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))


class case_directory_no_index_file(base_case):
    """Serve listing for a directory without an index.html page."""

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        handler.list_dir(handler.full_path)


class RequstHandler(BaseHTTPRequestHandler):
    Page = """"\
<html>
<body>
<table>
<tr>  <td>Header</td>         <td>Value</td>          </tr>
<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
<tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
<tr>  <td>Command</td>        <td>{command}</td>      </tr>
<tr>  <td>Path</td>           <td>{path}</td>         </tr>
</table>
</body>
</html>
"""
    Error_Page = """"\
<html>
<body>
<h1>Error accessing {path} </h1>
<h1>Error message {msg}</h1>
</body>
</html>
"""
    Listing_Page = '''\
            <html>
            <body>
            <ul>
            {0}
            </ul>
            </body>
            </html>
            '''
    Cases = [case_no_file(),
             case_existing_file(),
             case_directory_index_file(),
             case_directory_no_index_file(),
             case_always_fail()]

    # path = '/1.docx'
    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            print(self.path)

            for case in self.Cases:
                handler = case
                if handler.test(self):
                    handler.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Conetent-Length', str(len(content)))
        self.end_headers()
        if not isinstance(content, bytes):
            content = bytes(content, encoding='utf-8')
        self.wfile.write(content)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

    def list_dir(self, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ["<li><a href='localhost:8080/template/{}'>{}</a></li>".format(e, e)
                       for e in entries if not e.startswith('.')]
            page = self.Listing_Page.format('\n'.join(bullets))
            self.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(self.path, msg)
            self.handle_error(msg)


if __name__ == '__main__':
    server_address = ('', 8080)
    server = HTTPServer(server_address, RequstHandler)
    server.serve_forever()
