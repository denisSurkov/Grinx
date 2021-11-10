from typing import List, Dict, Any, Optional
import json

from grinx.configuration.exceptions import Misconfiguration
from grinx.configuration.parsers.location import LOCATION_PARSERS
from grinx.configuration.parsers.middleware import MIDDLEWARE_PARSERS
from grinx.servers.base import BaseServer
from grinx.locations.base import BaseLocation
from grinx.middlewares.base import BaseMiddleware


class ConfigParser:
    SERVERS = 'Servers'
    LOCATIONS = 'Locations'
    MIDDLEWARES = 'Middlewares'
    SERVER_HOST = 'Host'
    TYPE_KEYWORD = 'Type'

    def __init__(self, path_to_config_file: str):
        self.path_to_config_file = path_to_config_file
        self.host: Optional[str] = None
        self.port: Optional[str] = None

    def configure_servers(self) -> List[BaseServer]:
        configurations = self.load_config_file()

        self.host = configurations.get('Host', 'localhost')
        self.port = configurations.get('Port', '8000')

        servers = configurations.get(self.SERVERS)
        if not servers:
            raise Misconfiguration('No servers')

        return list(map(self.configure_server, servers))

    def load_config_file(self) -> Dict[str, Any]:
        with open(self.path_to_config_file, 'r') as f:
            return json.load(f)

    def configure_server(self, server_config: Dict[str, Any]) -> BaseServer:
        location_configs = server_config.get(self.LOCATIONS)
        if not location_configs:
            raise Misconfiguration('No locations for server')
        locations = list(map(self.configure_location, location_configs))

        middleware_configs = server_config.get(self.MIDDLEWARES)
        if middleware_configs is None:
            raise Misconfiguration('No middleware for server')
        middlewares = list(map(self.configure_middleware, middleware_configs))

        host = server_config.get(self.SERVER_HOST)
        if not host:
            raise Misconfiguration('No host for server')

        return BaseServer(host, locations, middlewares)

    def configure_location(self, location_config: Dict[str, Any]) -> BaseLocation:
        location_type = location_config.get(self.TYPE_KEYWORD)

        if not location_type:
            raise Misconfiguration('No location type')

        parser = LOCATION_PARSERS.get(location_type)

        if not parser:
            raise Misconfiguration(f'No parser for type {location_type}')

        return parser(location_config)

    def configure_middleware(self, middleware_config: Dict[str, Any]) -> BaseMiddleware:
        middleware_type = middleware_config.get(self.TYPE_KEYWORD)

        if not middleware_type:
            raise Misconfiguration('No middleware type')

        parser = MIDDLEWARE_PARSERS.get(middleware_type)

        if not parser:
            raise Misconfiguration(f'No parser for type {middleware_type}')

        return parser(middleware_config)
