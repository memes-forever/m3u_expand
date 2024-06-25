from http.server import HTTPServer, SimpleHTTPRequestHandler
from lib import expand_playlist, shaffle, shaffle_by_priority

url_main = 'http://localhost:8090/playlistall/all.m3u'


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/expand_playlist':
            new_list = expand_playlist(url_main)

            self.send_response(200)
            self.send_header('Content-type', 'audio/x-mpegurl; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(new_list).encode('utf-8'))

        elif self.path == '/shaffle':
            new_list = expand_playlist(url_main)
            new_random_list = shaffle(new_list)

            self.send_response(200)
            self.send_header('Content-type', 'audio/x-mpegurl; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(new_random_list).encode('utf-8'))

        elif '/shaffle?search=' in self.path:
            search = self.path.replace('/shaffle?search=', '').replace('%7C', '|')
            new_list = expand_playlist(url_main, search=search)
            new_random_list = shaffle(new_list)

            self.send_response(200)
            self.send_header('Content-type', 'audio/x-mpegurl; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(new_random_list).encode('utf-8'))

        elif '/shaffle_by_priority' in self.path:
            new_list = expand_playlist(url_main)
            new_random_list = shaffle_by_priority(new_list)

            self.send_response(200)
            self.send_header('Content-type', 'audio/x-mpegurl; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(new_random_list).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()


def run_server():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Serving HTTP on localhost port " + str(server_address) + "/) ...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
