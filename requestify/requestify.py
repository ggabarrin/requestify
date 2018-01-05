import optparse
import sys
from jinja2 import Environment, PackageLoader

from http_request import HTTPRequest


LANGUAGES = {
    "python-requests": {
        "description": "Python script using 'requests' module",
        "template_file": "python_requests.txt",
    },
    "php": {
        "description": "PHP script",
        "template_file": "php.txt",
    },
}


def generate_request_code(request, selected_template):
    """
    Generate script that makes HTTP request

    :param request: request object containing request information
    :returns: string containing generated script
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
    parser.add_option('-l', '--language', dest='lang', type='string', help='specify programming language of the output script', default="python-requests")
    (options, args) = parser.parse_args()

    # Input file
    if not options.input_file:
        print parser.usage
        exit(0)

    # Configure output script template
    lang = LANGUAGES.get(options.lang, None)
    if not lang:
        # Show list of availabe languages
        print "Invalid language option. Please select one of the available languages."
        for language, data in LANGUAGES.iteritems():
            print "[+] {}: {}".format(language, data["description"])

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
