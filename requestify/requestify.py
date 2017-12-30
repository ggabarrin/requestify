from urlparse import urlparse
from jinja2 import Environment, PackageLoader


PYTHON_REQUESTS_TEMPLATE = "python_requests.txt"
PHP_TEMPLATE = "php.txt"


def parse_http_request(raw_request):
    """
    Parse raw HTTP request

    :param raw_request: raw HTTP request
    :returns: dictionary with data from parsed HTTP request
    """
    try:
        message_separator = raw_request.index("\n\n")
        message_header = raw_request[:message_separator]
        message_body = raw_request[message_separator+2:]
    except ValueError:
        message_header = raw_request
        message_body = None

    try:
        message_header_lines = message_header.split("\n")
        request_line = message_header_lines[0]

        # Parse headers
        headers = {}
        for request_header in message_header_lines[1:]:
            if not len(request_header.strip()):
                break

            header_parts = request_header.split(": ")
            if len(header_parts):
                header_name = header_parts[0]
                header_value = header_parts[1]
                headers[header_name] = header_value

        # Parse cookies
        raw_cookies = headers.pop("Cookie", None)
        cookies = {}
        if raw_cookies:
            for raw_cookie in raw_cookies.split(";"):
                cookie_parts = request_header.split("=")
                cookie_name = cookie_parts[0].strip()
                cookie_value = cookie_parts[1:].strip()
                cookies[cookie_name] = cookie_value

        # Parse method, URI and version
        request_line_parts = request_line.split(" ")
        method = request_line_parts[0]
        uri = request_line_parts[1]
        if uri.index("/") == 0:  # Relative URI
            print "Relative URI detected. Please enter scheme, hostname and port to generate URL"
            host_header = headers.get("Host", None)
            port = None
            if host_header:
                if ":" not in host_header:
                    hostname = host_header
                else:
                    hostname = host_header.split(":")[0]
                    port = int(host_header.split(":")[1])

            scheme = raw_input("Scheme (http/https): ")
            if hostname:
                hostname_input = raw_input("Hostname '{}' detected in 'Host' header. Use this hostname? [Y/n] ".format(hostname))
                if hostname_input == "n" or hostname_input == "no":
                    hostname = None

            if not hostname:
                hostname = raw_input("Enter hostname (e.g. www.wikipedia.org): ")

            if port:
                port_input = raw_input("Port '{}' detected in 'Host' header. Use this port? [Y/n] ".format(port))
                if port_input == "n" or port_input == "no":
                    port = None

            if not port:
                port = int(raw_input("Enter port (e.g. 80, 443, ..): "))

        else:  # Absolute URI
            parsed_url = urlparse(uri)
            scheme = parsed_url.scheme
            hostname = parsed_url.hostname
            port = parsed_url.port
            if not port:
                if scheme == "http":
                    port = 80
                elif scheme == "https":
                    port = 443
            uri = parsed_url.path
            if parsed_url.query:
                uri += "?{}".format(parsed_url.query)

        http_version = request_line_parts[2]

        # Message body
        data = message_body
    except:
        print "Error while parsing raw HTTP request."
        return None

    return {
        "method": method,
        "scheme": scheme,
        "host": hostname,
        "port": port,
        "uri": uri,
        "headers": headers,
        "data": data,
        "cookies": cookies,
    }


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
        headers=request["headers"],
        data=request["data"],
        cookies=request["cookies"],
        method=request["method"],
        scheme=request["scheme"],
        host=request["host"],
        port=request["port"],
        uri=request["uri"],
    )


def main():
    raw_http_request = r"""GET / HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1"""

    parsed_request = parse_http_request(raw_http_request)
    if parsed_request:
        generated_code = generate_request_code(parsed_request, PYTHON_REQUESTS_TEMPLATE)
        print generated_code


if __name__ == '__main__':
    main()
