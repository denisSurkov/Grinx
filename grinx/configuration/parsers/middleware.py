from typing import Any, Dict, List, Tuple

from grinx.configuration.exceptions import Misconfiguration
from grinx.middlewares.basic_auth import BasicAuthMiddleware


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

        if not isinstance(u, dict):
            raise Misconfiguration('Misconfigurated BasicAuthMiddleware')

        parsed_users.append((username, password))

    return BasicAuthMiddleware(parsed_users)


MIDDLEWARE_PARSERS = {
    'BasicAuthMiddleware': parse_basic_auth,
}
