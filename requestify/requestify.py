import errno
import optparse
import os
import sys
from jinja2 import Environment, PackageLoader
from urlparse import urlparse

from http_request import HTTPRequest


LANGUAGES = {
    'python': {
        'description': 'Python script using \'requests\' module',
        'template_file': 'python.j2',
    },
    'nodejs': {
        'description': 'Node.js script using \'request\' module',
        'template_file': 'nodejs.j2',
    },
    'php': {
        'description': 'PHP script',
        'template_file': 'php.j2',
    },
}
SEPARATOR = '#' * 40


def generate_request_code(request, selected_template):
    '''
    Generate script that makes HTTP request

    :param request: request object containing request information
    :returns: string containing generated script
    '''
    env = Environment(
        loader=PackageLoader('requestify', 'templates'),
    )
    template = env.get_template(selected_template)

    # Retrieve scheme, host and port
    if request.path.index('/') == 0:  # Relative URI
        print '[*] Relative URI detected. Please enter scheme, hostname and port to generate URL'
        host = None
        port = None
        host_header_value = request.headers.get('host', None)
        if host_header_value:
            if ':' not in host_header_value:
                host = host_header_value
            else:
                host = host_header_value.split(':')[0]
                port = int(host_header_value.split(':')[1])

        scheme = raw_input('[+] Scheme (http/https): ')
        if host:
            hostname_input = raw_input(
                '[+] Hostname \'{}\' detected in \'Host\' header. Use this hostname? [Y/n] '.format(host))
            if hostname_input == 'n' or hostname_input == 'no':
                host = None

        if not host:
            host = raw_input('[+] Enter hostname (e.g. www.wikipedia.org): ')

        if port:
            port_input = raw_input(
                '[+] Port \'{}\' detected in \'Host\' header. Use this port? [Y/n] '.format(port))
            if port_input == 'n' or port_input == 'no':
                port = None

        if not port:
            port = int(raw_input('[+] Enter port (e.g. 80, 443, ..): '))

    else:  # Absolute URI
        parsed_url = urlparse(request.path)
        scheme = parsed_url.scheme
        host = parsed_url.hostname
        port = parsed_url.port
        if not port:
            if scheme == 'http':
                port = 80
            elif scheme == 'https':
                port = 443
        request.path = parsed_url.path
        if parsed_url.query:
            request.path += '?{}'.format(parsed_url.query)

    return template.render(
        headers=request.headers,
        data=request.data,
        cookies=request.cookies,
        method=request.command,
        uri=request.path,
        scheme=scheme,
        host=host,
        port=port,
    )


def main():
    # Menu
    parser = optparse.OptionParser('usage %prog -i <input_file>')
    parser.add_option('-i', '--input', dest='input_file', type='string',
                      help='specify input file containing raw HTTP request')
    parser.add_option('-o', '--output', dest='output_file',
                      type='string', help='specify output file')
    parser.add_option('-l', '--language', dest='lang', type='string',
                      help='specify programming language of the output script', default='python-requests')
    (options, args) = parser.parse_args()

    # Input file
    if not options.input_file:
        print parser.usage
        exit(0)

    print '[*] Input file: {}'.format(options.input_file)

    # Output file
    output_file = None
    if options.output_file is not None:
        if os.path.dirname(options.output_file):
            if not os.path.exists(os.path.dirname(options.output_file)):
                try:
                    os.makedirs(os.path.dirname(options.output_file))
                except OSError as e:  # Guard against race condition
                    if e.errno != errno.EEXIST:
                        raise

        print '[*] Output file: {}'.format(options.input_file)
        output_file = open(options.output_file, 'w')

    # Configure output script template
    lang = LANGUAGES.get(options.lang, None)
    if not lang:
        # Show list of availabe languages
        print '[*] Invalid language option. Please select one of the available languages.'
        for language, data in LANGUAGES.iteritems():
            print '[+] {}: {}'.format(language, data['description'])

        exit(0)
    print '[*] Output script language: {}'.format(options.lang)

    # Read and parse raw HTTP request
    try:
        raw_http_request = ''.join(open(options.input_file, 'r').readlines())
    except:
        print '[*] Error while reading raw HTTP request file.'
        exit(0)

    print '\n{0} BEGIN RAW HTTP REQUEST {0} \n'.format(SEPARATOR)
    print raw_http_request
    print '\n{0} END RAW HTTP REQUEST {0} \n'.format(SEPARATOR)
    request = HTTPRequest(raw_http_request)
    if request:
        # Generate source code that makes request
        generated_code = generate_request_code(request, lang['template_file'])
        print '\n{0} BEGIN GENERATED SCRIPT {0}\n'.format(SEPARATOR)
        print generated_code
        print '\n{0} END GENERATED SCRIPT {0}\n'.format(SEPARATOR)

        if output_file:
            output_file.write(generated_code)
            output_file.close()


if __name__ == '__main__':
    main()
