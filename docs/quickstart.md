# QuickStart

First, start by importing Httpx:

```pycon
>>> from iutils.OkHttps import Httpx
```

Now, let’s try to get a webpage.

```pycon
>>> r = Httpx.sendApi(url='https://httpbin.org/get', method='get')
>>> r
<Response [200 OK]>
```

Similarly, to make an HTTP POST request:

```pycon
>>> r = Httpx.sendApi(url='https://httpbin.org/post', method='post', data={'key': 'value'})
```

The PUT, DELETE, HEAD, and OPTIONS requests all follow the same style:

```pycon
>>> r = Httpx.sendApi(url='https://httpbin.org/put', method='post', data={'key': 'value'})
>>> r = Httpx.sendApi(url='https://httpbin.org/delete', method='delete')
>>> r = Httpx.sendApi(url='https://httpbin.org/get', method='head')
>>> r = Httpx.sendApi(url='https://httpbin.org/get', method='options')
```

## Passing Parameters in URLs

To include URL query parameters in the request, use the `params` keyword:

```pycon
>>> params = {'key1': 'value1', 'key2': 'value2'}
>>> r = Httpx.sendApi(url='https://httpbin.org/get', method='get', params={'key': 'value'})
```

To see how the values get encoding into the URL string, we can inspect the
resulting URL that was used to make the request:

```pycon
>>> r.url
URL('https://httpbin.org/get?key2=value2&key1=value1')
```

You can also pass a list of items as a value:

```pycon
>>> params = {'key1': 'value1', 'key2': ['value2', 'value3']}
>>> r = Httpx.sendApi(url='https://httpbin.org/get', method='get', params={'key': 'value'})
>>> r.url
URL('https://httpbin.org/get?key1=value1&key2=value2&key2=value3')
```

## Response Content

HTTPX will automatically handle decoding the response content into Unicode text.

```pycon
>>> r = Httpx.sendApi(url='https://httpbin.org/get', method='get', params={'key': 'value'})
>>> r.text 原生
>>> Httpx.getText(r) 二次封装调用
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

You can inspect what encoding will be used to decode the response.

```pycon
>>> r.encoding 原生
>>> Httpx.getEncoding(r) 二次封装调用
'UTF-8'
```

In some cases the response may not contain an explicit encoding, in which case HTTPX
will attempt to automatically determine an encoding to use.

```pycon
>>> r.encoding
None
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

If you need to override the standard behaviour and explicitly set the encoding to
use, then you can do that too.

```pycon
>>> r.encoding = 'ISO-8859-1'
```

## Binary Response Content

The response content can also be accessed as bytes, for non-text responses:

```pycon
>>> r.content
>>> Httpx.getContent(r) 二次封装调用
b'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

Any `gzip` and `deflate` HTTP response encodings will automatically
be decoded for you. If `brotlipy` is installed, then the `brotli` response
encoding will also be supported.

For example, to create an image from binary data returned by a request, you can use the following code:

```pycon
>>> from PIL import Image
>>> from io import BytesIO
>>> i = Image.open(BytesIO(r.content))
```

## JSON Response Content

Often Web API responses will be encoded as JSON.

```pycon
>>> r.json()
[{u'repository': {u'open_issues': 0, u'url': 'https://github.com/...' ...  }}]
```

## Custom Headers

To include additional headers in the outgoing request, use the `headers` keyword argument:

```pycon
>>> url = 'https://httpbin.org/headers'
>>> headers = {'user-agent': 'my-app/0.0.1'}
>>> r = Httpx.sendApi(url=url, headers=headers , method="get")
>>> r.headers
```

## Sending Form Encoded Data

Some types of HTTP requests, such as `POST` and `PUT` requests, can include data
in the request body. One common way of including that is as form-encoded data,
which is used for HTML forms.

```pycon
>>> data = {'key1': 'value1', 'key2': 'value2'}
### 原生
>>> r = requests.post("https://httpbin.org/post", data=data)
### sendApi
>>> r = Httpx.sendApi(url="https://httpbin.org/post", method="post", data=data)
>>> print(r.text)
{
  ...
  "form": {
    "key2": "value2",
    "key1": "value1"
  },
  ...
}

```

Form encoded data can also include multiple values from a given key.

```pycon
>>> data = {'key1': ['value1', 'value2']}
>>> r = requests.post("https://httpbin.org/post", data=data)
>>> print(r.text)
{
  ...
  "form": {
    "key1": [
      "value1",
      "value2"
    ]
  },
  ...
}
```

## Sending Multipart File Uploads

You can also upload files, using HTTP multipart encoding:

```pycon
>>> files = {'upload-file': open('report.xls', 'rb')}
>>> r = requests.post("https://httpbin.org/post", files=files)
>>> print(r.text)
{
  ...
  "files": {
    "upload-file": "<... binary content ...>"
  },
  ...
}
```

You can also explicitly set the filename and content type, by using a tuple
of items for the file value:

```pycon
>>> files = {'upload-file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel')}
>>> r = requests.post("https://httpbin.org/post", files=files)
>>> print(r.text)
{
  ...
  "files": {
    "upload-file": "<... binary content ...>"
  },
  ...
}
```

If you need to include non-file data fields in the multipart form, use the `data=...` parameter:

```pycon
>>> data = {'message': 'Hello, world!'}
>>> files = {'file': open('report.xls', 'rb')}
>>> r = requests.post("https://httpbin.org/post", data=data, files=files)
>>> print(r.text)
{
  ...
  "files": {
    "file": "<... binary content ...>"
  },
  "form": {
    "message": "Hello, world!",
  },
  ...
}
```

## Sending JSON Encoded Data

Form encoded data is okay if all you need is a simple key-value data structure.
For more complicated data structures you'll often want to use JSON encoding instead.

```pycon
>>> data = {'integer': 123, 'boolean': True, 'list': ['a', 'b', 'c']}
### 原生
>>> r = requests.post("https://httpbin.org/post", json=data)
### sendApi
>>> r = Httpx.sendApi(url="https://httpbin.org/post", method="post", json=data)
>>> print(r.text)
{
  ...
  "json": {
    "boolean": true,
    "integer": 123,
    "list": [
      "a",
      "b",
      "c"
    ]
  },
  ...
}
```

## Response Status Codes

We can inspect the HTTP status code of the response:

```pycon
>>> r = Httpx.sendApi(url="https://httpbin.org/get", method="get")
>>> r.status_code
200
```

## Cookies

Any cookies that are set on the response can be easily accessed:

```pycon
>>> r = Httpx.sendApi('https://httpbin.org/cookies/set?chocolate=chip', method='get')
>>> r.cookies['chocolate']
'chip'
```

## Timeouts

OkHttps defaults to including reasonable timeouts for all network operations,
meaning that if a connection is not properly established then it should always
raise an error rather than hanging indefinitely.

The default timeout for network inactivity is five seconds. You can modify the
value to be more or less strict:

```pycon
>>> Httpx.sendApi(url='https://httpbin.org/get', method='get', timeout=0.01)
```

You can also disable the timeout behavior completely...

```pycon
>>> Httpx.sendApi(url='https://httpbin.org/get', method='get') # 不传默认为None
>>> Httpx.sendApi(url='https://httpbin.org/get', method='get', timeout=None)
```

## Authentication

OkHttps supports Basic and Digest HTTP authentication.

To provide Basic authentication credentials, pass a 2-tuple of
plaintext `str` or `bytes` objects as the `auth` argument to the request
functions:

```pycon
>>> auth=("my_user", "password123")
>>> Httpx.sendApi(url='https://httpbin.org/get', method='get', auth=auth)
```

## ReportTag

Of course you can label a single use case as a test report

```pycon
>>> setTag({'feature': '一级标签', 'severity': 'blocker'})
>>> setTag([{'feature': '一级标签', 'severity': 'blocker'},
             {'severity': 'critical（覆盖掉原有的blocker）',
             'description': '这是用例描述', 
             'story': '二级标签'}])
```

## Assert

You can use native Assert

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
 
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    assert x == y  #如果这个断言失败，则后续都不会执行
    assert True
    assert False
```

You can also use pytest-assume

```
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_pytest_assume(x, y):
    pytest.assume(x == y) #即使这个断言失败，后续仍旧执行
    pytest.assume(True)
    pytest.assume(False)
```


|断言类型| 1，1 | 1，0 | 0，1 | 结论 |
| :----:| :----: | :----: |:----:| :----: |
| assert | 断言3失败 | 断言1失败 |断言2和断言3不执行|断言1失败，断言2和断言3不执行|assert遇到断言失败则停下|
| pytest.assume | 断言3失败 | 断言1失败 |断言2和断言3继续执行|断言1失败，断言2和断言3继续执行|pytest.assume无论断言结果，全部执行|

Pytest-assume is used with the context manager with

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
from pytest import assume
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    #使用上下文管理器的好处是不用显示去try和finally捕获异常，建议使用这种写法，简洁有效。
    with assume: assert x == y
    with assume: assert True
    with assume: assert False
```

The main thing to note is that if the context manager contains multiple assertions, only the first one will be executed, as in

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
from pytest import assume
    
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    #使用上下文管理器的好处是不用显示去try和finally捕获异常，建议使用这种写法，简洁有效。
    with assume: 
        #只有第一个断言会被执行！
        assert x == y
        assert True
        assert False  
```

