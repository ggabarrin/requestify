# requestify

Requestify parses a raw HTTP request and generates source code in different languages (templates) that makes the parsed request.

Available templates:
* `python`: Python script using 'requests' module
* `php`: PHP script
* `nodejs`: Node.js script using 'request' module

## Examples

### Parse GET request and generate python script

`python requestify/requestify.py -i requestify/examples/get.txt -l python`

Raw request:

```
GET / HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
```

Generated python script:

```
import requests

# Headers
headers = {
    'accept-language': 'en-US,en;q=0.5',
    'accept-encoding': 'gzip, deflate',
    'host': 'localhost:8080',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'dnt': '1',
    'connection': 'keep-alive',
    'upgrade-insecure-requests': '1',
}

# Data
data = r""""""

# Cookies
cookies = {
}

# Prepare and send request
req = requests.Request(
    method="GET",
    url="http://localhost:8080/",
    headers=headers,
    data=data,
    cookies=cookies,
)
prepared_req = req.prepare()
session = requests.Session()
resp = session.send(prepared_req)
```
