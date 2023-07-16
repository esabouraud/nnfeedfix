"""Fetch Nerf Now non-compliant Atom feed and make it palatable to feed readers"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib3


HOSTNAME = "0.0.0.0"
PORT = 18080


class MyServer(BaseHTTPRequestHandler):
    """Web server fetching feed and transforming it on each GET request"""

    def do_GET(self):
        """Perform HTTP GET on original feed and transform it"""
        status, headers, data = get_feed()
        self.send_response(status)
        #for header_name, header_value in headers.items():
        #    self.send_header(header_name, header_value)
        self.send_header("Content-Type", "text/xml; charset=utf-8")
        self.end_headers()
        self.wfile.write(data)


def serve():
    """Run web server"""

    web_server = HTTPServer((HOSTNAME, PORT), MyServer)
    print(f"Server started http://{HOSTNAME}:{PORT}")

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")


def sanitize_data(data):
    """Sanitize feed by removing email protection related xml tags,
    and rewriting relative urls to be absolute"""

    data_str = data.decode("utf-8")
    lines = [
        line.replace('src="/img/', 'src="http://www.nerfnow.com/img/')
        for line in data_str.split("\n")
        if not line.startswith("<email>") and not line.startswith("<script data-cfasync")]
    sanitized_data = "\n".join(lines)
    return sanitized_data.encode("utf-8")


def get_feed():
    """Get feed and sanitize it"""

    http = urllib3.PoolManager()
    resp = http.request("GET", "http://feeds.feedburner.com/nerfnow/full")
    # print(resp.data)
    print(resp.headers)
    if resp.status != 200:
        return resp.status, resp.headers, resp.data
    return resp.status, resp.headers, sanitize_data(resp.data)


def main():
    """Main function"""
    serve()
    #get_feed()


if __name__ == "__main__":
    main()
