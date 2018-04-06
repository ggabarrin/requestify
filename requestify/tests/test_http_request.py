import unittest

from requestify.http_request import HTTPRequest


class HTTPRequestTest(unittest.TestCase):

    def setUp(self):
        raw_http_request = "".join(open("requestify/examples/post.txt", "r").readlines())
        self.http_request = HTTPRequest(raw_http_request)

    def test_headers(self):
        assert self.http_request.headers == {
            'content-length': '44',
            'accept-language': 'en-US,en;q=0.5',
            'accept-encoding': 'gzip, deflate',
            'host': 'localhost',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'dnt': '1',
            'connection': 'keep-alive',
            'cookie': 'yummy_cookie=choco; tasty_cookie=strawberry',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
        }

    def test_data(self):
        assert self.http_request.data == "user=the_user&password=super_secure_password"

    def test_cookies(self):
        assert self.http_request.cookies == {
            'yummy_cookie': 'choco',
            'tasty_cookie': 'strawberry',
        }

    def test_method(self):
        assert self.http_request.command == "POST"

    def test_path(self):
        assert self.http_request.path == "/login"
