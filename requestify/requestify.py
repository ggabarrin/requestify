from jinja2 import Environment, PackageLoader

from http_request import HTTPRequest


PYTHON_REQUESTS_TEMPLATE = "python_requests.txt"
PHP_TEMPLATE = "php.txt"


def generate_request_code(request, selected_template):
    """
    Generate python code that makes HTTP request

    :param request: dictionary with request data
    :returns: string containing generated python code
    """
    env = Environment(
        loader=PackageLoader('requestify', 'templates'),
    )
    template = env.get_template(selected_template)
    return template.render(
        headers=request.headers,
        data=request.data,
        cookies=request.cookies,
        method=request.command,
        scheme=request.scheme,
        host=request.host,
        port=request.port,
        uri=request.path,
    )


def main():
    raw_http_request = (
        "GET / HTTP/1.1\r\n"
        "Host: localhost:8080\r\n"
        "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0\r\n"
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        "Accept-Language: en-US,en;q=0.5\r\n"
        "Accept-Encoding: gzip, deflate\r\n"
        "DNT: 1\r\n"
        "Connection: keep-alive\r\n"
        "Upgrade-Insecure-Requests: 1\r\n"
    )
    request = HTTPRequest(raw_http_request)
    if request:
        generated_code = generate_request_code(request, PYTHON_REQUESTS_TEMPLATE)
        print generated_code


if __name__ == '__main__':
    main()
