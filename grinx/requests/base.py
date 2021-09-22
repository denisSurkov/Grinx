from typing import Optional, Dict, Callable
import re


# http://jmrware.com/articles/2009/uri_regexp/URI_regex.html#uri-42
RELATIVE_PATH_REXGEXP = re.compile(r""" ^
    # RFC-3986 URI component:  relative-ref
    (?P<path> //                                                          # relative-part
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
    |        (?:[A-Za-z0-9\-._~!$&'()*+,;=@] |%[0-9A-Fa-f]{2})+
        (?:/ (?:[A-Za-z0-9\-._~!$&'()*+,;=:@]|%[0-9A-Fa-f]{2})* )*
    |
    )
    (?P<query>\? (?:[A-Za-z0-9\-._~!$&'()*+,;=:@/?]|%[0-9A-Fa-f]{2})* )?   # [ "?" query ]
    (?P<fragment>\# (?:[A-Za-z0-9\-._~!$&'()*+,;=:@/?]|%[0-9A-Fa-f]{2})* )?   # [ "#" fragment ]
    $ """, re.VERBOSE)


class RequestPath:
    def __init__(self, path: str, query: Optional[str] = None, fragment: Optional[str] = None):
        self.path = path
        self.query = query
        self.fragment = fragment

    @staticmethod
    def from_relative_path(relative_path: str, raise_if_not_correct: bool = True) -> 'RequestPath':
        match = RELATIVE_PATH_REXGEXP.match(relative_path)

        if not match and raise_if_not_correct:
            raise Exception()

        path, query, fragment = match.groups()
        return RequestPath(path, query, fragment)


class BaseRequest:
    def __init__(self, method: str,
                 request_path: RequestPath,
                 callback_to_read_all_headers: Callable[[], Dict[str, str]],
                 callback_to_read_body: Callable[[], bytes],
                 protocol: str = 'HTTP/1.1',):
        self.protocol: str = protocol
        self.method: str = method
        self.request_path = request_path

        self.callback_to_read_all_headers = callback_to_read_all_headers
        self._headers: Optional[Dict[str, str]] = None

        self.callback_to_read_body = callback_to_read_body
        self._body: Optional[bytes] = None

    @staticmethod
    def from_header(method: str, request_path: RequestPath, protocol: str) -> 'BaseRequest':
        return BaseRequest(method, request_path, protocol, None, None)

    @property
    def path(self) -> str:
        return self.request_path.path

    @property
    def query(self) -> Optional[str]:
        return self.request_path.query

    @property
    def path_fragment(self) -> Optional[str]:
        return self.request_path.fragment

    @property
    def body(self) -> bytes:
        if self._body:
            return self._body

        # we have to read headers before body
        _ = self.headers

        self._body = self.callback_to_read_body()
        return self._body

    @property
    def headers(self) -> Dict[str, str]:
        if self._headers:
            return self._headers

        self._headers = self.callback_to_read_all_headers()
        return self._headers


__all__ = (
    'RequestPath',
    'BaseRequest',
)
