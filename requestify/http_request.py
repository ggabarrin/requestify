from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from urlparse import urlparse


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, raw_http_request):
        self.rfile = StringIO(raw_http_request)
        self.raw_requestline = self.rfile.readline()
        self.parse_request()

        self.headers = dict(self.headers)
        # Data
        try:
            self.data = raw_http_request[raw_http_request.index("\n\n")+2:]
        except ValueError:
            self.data = None

        # Cookies
        self.cookies = {}
        raw_cookies = self.headers.pop("cookie", None)
        if raw_cookies:
            for raw_cookie in raw_cookies.split(";"):
                cookie_parts = request_header.split("=")
                cookie_name = cookie_parts[0].strip()
                cookie_value = cookie_parts[1:].strip()
                self.cookies[cookie_name] = cookie_value

        # Path
        if self.path.index("/") == 0:  # Relative URI
            print "[*] Relative URI detected. Please enter scheme, hostname and port to generate URL"
            host_header = self.headers.get("host", None)
            self.port = None
            if host_header:
                if ":" not in host_header:
                    self.host = host_header
                else:
                    self.host = host_header.split(":")[0]
                    self.port = int(host_header.split(":")[1])

            self.scheme = raw_input("[+] Scheme (http/https): ")
            if self.host:
                hostname_input = raw_input("[+] Hostname '{}' detected in 'Host' header. Use this hostname? [Y/n] ".format(self.host))
                if hostname_input == "n" or hostname_input == "no":
                    self.host = None

            if not self.host:
                self.host = raw_input("[+] Enter hostname (e.g. www.wikipedia.org): ")

            if self.port:
                port_input = raw_input("[+] Port '{}' detected in 'Host' header. Use this port? [Y/n] ".format(self.port))
                if port_input == "n" or port_input == "no":
                    self.port = None

            if not self.port:
                self.port = int(raw_input("[+] Enter port (e.g. 80, 443, ..): "))

        else:  # Absolute URI
            parsed_url = urlparse(self.path)
            self.scheme = parsed_url.scheme
            self.host = parsed_url.hostname
            self.port = parsed_url.port
            if not self.port:
                if self.scheme == "http":
                    self.port = 80
                elif self.scheme == "https":
                    self.port = 443
            self.path = parsed_url.path
            if parsed_url.query:
                self.path += "?{}".format(parsed_url.query)

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message
