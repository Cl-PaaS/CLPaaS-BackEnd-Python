from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from web import validate_phishing

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed_path.query)

        url_param = query.get('url', [None])[0]

        if url_param is None:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Bad Request')

        isPhishing = validate_phishing(url_param)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response_message = f'URL: {url_param}, isPhishing: {isPhishing}'
        self.wfile.write(response_message.encode())
            

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
