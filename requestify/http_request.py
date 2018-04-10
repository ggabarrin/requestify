from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, raw_http_request):
        self.rfile = StringIO(raw_http_request)
        self.raw_requestline = self.rfile.readline()
        self.parse_request()

        self.headers = dict(self.headers)
        # Data
        try:
            self.data = raw_http_request[raw_http_request.index("\n\n")+2:].rstrip()
        except ValueError:
            self.data = None

        # Cookies
        self.cookies = {}
        raw_cookies = self.headers.get("cookie")
        if raw_cookies:
            for raw_cookie in raw_cookies.split(";"):
                cookie_parts = raw_cookie.split("=")
                cookie_name = cookie_parts[0].strip()
                cookie_value = "".join(cookie_parts[1:]).strip()
                self.cookies[cookie_name] = cookie_value

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message
