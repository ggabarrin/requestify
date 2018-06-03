
# requestify

Requestify parses a raw HTTP request and generates source code in different languages (templates) that makes the parsed request.

## Usage

First, clone the repo:

```sh
$ git clone https://github.com/ggabarrin/requestify.git
$ cd requestify
```

Then, install the dependencies:

```sh
$ pip install -r requirements.txt
```

Save the raw HTTP request you want to requestify in a file. Request should look similar to examples available on `requestify/examples` directory:

```sh
$ cat requestify/examples/get.txt
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

Select the language for the script you want to generate from the available templates:

* `python`: Python script using 'requests' module
* `php`: PHP script
* `nodejs`: Node.js script using 'request' module

Requestify!

```sh
python requestify/requestify.py -i <file> -l <language>
```

## Examples

### Parse GET request and generate python script

```sh
python requestify/requestify.py -i requestify/examples/get.txt -l python
```

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

```py
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
# print resp.status_code
# print resp.text
# print resp.headers
```

### Parse POST request and generate node.js script

```sh
python requestify/requestify.py -i requestify/examples/post.txt -l nodejs
```

Raw request:

```
POST /login HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 44
Cookie: yummy_cookie=choco; tasty_cookie=strawberry
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1

user=the_user&password=super_secure_password
```

Generated nodejs script:

```js
var request = require("request");

// headers
headers = {
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

// cookies
var jar = request.jar();
jar.add(request.cookie('yummy_cookie=choco'));
jar.add(request.cookie('tasty_cookie=strawberry'));

// data
var data = `user=the_user&password=super_secure_password`;

// prepare and send request
request({
  uri: 'https://localhost:443/login',
  method: 'POST',
  headers: headers,
  body: data,
  jar: jar,
}, function(error, response, body) {
  // console.log(response.status_code);
  // console.log(body);
  // console.log(response.headers)
});
```
