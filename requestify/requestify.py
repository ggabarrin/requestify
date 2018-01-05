import optparse
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
    # Menu
    parser = optparse.OptionParser('usage %prog -i <input_file>')
    parser.add_option('-i', '--input', dest='input_file', type='string', help='specify input file containing raw HTTP request')
    (options, args) = parser.parse_args()

    # Input file
    if not options.input_file:
        print parser.usage
        exit(0)

    # Read and parse raw HTTP request
    try:
        raw_http_request = "".join(open(options.input_file, "r").readlines())
    except:
        print "Error while reading file."
        exit(0)

    print raw_http_request
    request = HTTPRequest(raw_http_request)
    if request:
        # Generate source code that makes request
        generated_code = generate_request_code(request, PYTHON_REQUESTS_TEMPLATE)
        print generated_code


if __name__ == '__main__':
    main()
