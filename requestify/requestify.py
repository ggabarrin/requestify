import sys
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
    # Read and parse raw HTTP request
    file_path = sys.argv[1]
    raw_http_request = "".join(open(file_path, "r").readlines())
    print raw_http_request
    request = HTTPRequest(raw_http_request)
    if request:
        # Generate source code that makes request
        generated_code = generate_request_code(request, PYTHON_REQUESTS_TEMPLATE)
        print generated_code


if __name__ == '__main__':
    main()
