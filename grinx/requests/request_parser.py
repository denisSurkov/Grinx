import re
from asyncio import StreamReader

from grinx.exceptions.bad_request import BadGrinxRequest
from grinx.requests.base import BaseRequest


ALLOWED_METHOD = frozenset((
        'OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'
))

# http://jmrware.com/articles/2009/uri_regexp/URI_regex.html
RE_PYTHON_RFC3986_ABSOLUTE_URI = re.compile(r""" ^
    # free-spacing mode regex for URI component:  absolute-URI
    [A-Za-z][A-Za-z0-9+\-.]* :                                      # scheme ":"
    (?: //                                                          # hier-part
      (?: (?:[A-Za-z0-9\-._~!$&'()*+,;=:]|%[0-9A-Fa-f]{2})* @)?
      (?:
        \[
        (?:
          (?:
            (?:                                                    (?:[0-9A-Fa-f]{1,4}:){6}
            |                                                   :: (?:[0-9A-Fa-f]{1,4}:){5}
            | (?:                            [0-9A-Fa-f]{1,4})? :: (?:[0-9A-Fa-f]{1,4}:){4}
            | (?: (?:[0-9A-Fa-f]{1,4}:){0,1} [0-9A-Fa-f]{1,4})? :: (?:[0-9A-Fa-f]{1,4}:){3}
            | (?: (?:[0-9A-Fa-f]{1,4}:){0,2} [0-9A-Fa-f]{1,4})? :: (?:[0-9A-Fa-f]{1,4}:){2}
            | (?: (?:[0-9A-Fa-f]{1,4}:){0,3} [0-9A-Fa-f]{1,4})? ::    [0-9A-Fa-f]{1,4}:
            | (?: (?:[0-9A-Fa-f]{1,4}:){0,4} [0-9A-Fa-f]{1,4})? ::
            ) (?:
                [0-9A-Fa-f]{1,4} : [0-9A-Fa-f]{1,4}
              | (?: (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?) \.){3}
                    (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
              )
          |   (?: (?:[0-9A-Fa-f]{1,4}:){0,5} [0-9A-Fa-f]{1,4})? ::    [0-9A-Fa-f]{1,4}
          |   (?: (?:[0-9A-Fa-f]{1,4}:){0,6} [0-9A-Fa-f]{1,4})? ::
          )
        | [Vv][0-9A-Fa-f]+\.[A-Za-z0-9\-._~!$&'()*+,;=:]+
        )
        \]
      | (?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}
           (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
      | (?:[A-Za-z0-9\-._~!$&'()*+,;=]|%[0-9A-Fa-f]{2})*
      )
      (?: : [0-9]* )?
      (?:/ (?:[A-Za-z0-9\-._~!$&'()*+,;=:@]|%[0-9A-Fa-f]{2})* )*
    | /
      (?:    (?:[A-Za-z0-9\-._~!$&'()*+,;=:@]|%[0-9A-Fa-f]{2})+
        (?:/ (?:[A-Za-z0-9\-._~!$&'()*+,;=:@]|%[0-9A-Fa-f]{2})* )*
      )?
    |        (?:[A-Za-z0-9\-._~!$&'()*+,;=:@]|%[0-9A-Fa-f]{2})+
        (?:/ (?:[A-Za-z0-9\-._~!$&'()*+,;=:@]|%[0-9A-Fa-f]{2})* )*
    |
    )
    (?:\? (?:[A-Za-z0-9\-._~!$&'()*+,;=:@/?]|%[0-9A-Fa-f]{2})* )?   # [ "?" query ]
    $ """, re.VERBOSE)


class RequestParser:
    def __init__(self, reader: StreamReader):
        self.reader = reader

    async def __call__(self) -> BaseRequest:
        return await self.parse_request()

    async def parse_request(self):
        return await self.read_header()

    async def read_header(self):
        first_line = await self.reader.readline()
        splited_first_line = first_line.decode('utf8').strip().split(' ')

        # only three values in first line are allowed
        # so if there are more or less values in first line
        # than server cannot proceed this request
        if len(splited_first_line) - 3 != 0:
            raise BadGrinxRequest()

        # https://datatracker.ietf.org/doc/html/rfc2616#section-5.1
        method, request_uri, version = splited_first_line

        self.validate_method(method)
        self.validate_request_uri(request_uri)
        self.validate_version(version)

        incoming_request = BaseRequest.from_header(method, request_uri, version)
        return incoming_request

    def validate_method(self, method: str):
        if method not in ALLOWED_METHOD:
            raise BadGrinxRequest(f'{method} is not allowed')

    def validate_request_uri(self, request_uri: str):
        pass

    def validate_version(self, version: str):
        if version != 'HTTP/1.1':
            raise BadGrinxRequest(f'{version} is not supported')
