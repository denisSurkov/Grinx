from typing import Any, Dict, List, Tuple

from grinx.configuration.exceptions import Misconfiguration
from grinx.middlewares.basic_auth import BasicAuthMiddleware
from grinx.middlewares.path_rewrite import PathRewriteMiddleware, PathRewriteInstruction


def parse_basic_auth(middleware_payload: Dict[str, Any]) -> BasicAuthMiddleware:
    """
    :param middleware_payload: {
       "Type": "BasicAuthMiddleware",
       "Users": [
            {
                "User": "",
                "Password": ""
            }
       ]
    }
    """
    users = middleware_payload.get('Users')

    if not users:
        raise Misconfiguration('Misconfigurated BasicAuthMiddleware')

    parsed_users: List[Tuple[str, str]] = []
    for u in users:
        if not isinstance(u, dict):
            raise Misconfiguration('Misconfigurated BasicAuthMiddleware')

        username = u.get('User')
        password = u.get('Password')

        if not (username or password):
            raise Misconfiguration('Misconfigurated BasicAuthMiddleware')

        parsed_users.append((username, password))

    return BasicAuthMiddleware(parsed_users)


def parse_path_rewrite(middleware_payload: Dict[str, Any]) -> PathRewriteMiddleware:
    """
    :param middleware_payload: {
      "Type": "PathRewriteMiddleware",
      "Rules": [
        {
          "From": "/foo/",
          "To": "/bar/",
        }
      ]
    }
    """
    rules = middleware_payload.get('Rules')

    if not rules:
        raise Misconfiguration('Misconfigurated PathRewriteMiddleware')

    parsed_rules: List[Tuple[str, str]] = []
    for r in rules:
        if not isinstance(r, dict):
            raise Misconfiguration('Misconfigurated PathRewriteMiddleware')

        from_path = r.get('From')
        to_path = r.get('To')

        if not (from_path or to_path):
            raise Misconfiguration('Misconfigurated PathRewriteMiddleware')

        parsed_rules.append(PathRewriteInstruction(from_path, to_path))

    return PathRewriteMiddleware(parsed_rules)


MIDDLEWARE_PARSERS = {
    'BasicAuthMiddleware': parse_basic_auth,
    'PathRewriteMiddleware': parse_path_rewrite,
}
