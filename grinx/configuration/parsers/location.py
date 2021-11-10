from typing import Any, Dict

from grinx.configuration.exceptions import Misconfiguration
from grinx.locations.file_location import RootFileLocation, AliasFileLocation
from grinx.locations.proxy_pass_location import ProxyPassLocation


def parse_root_location(location_payload: Dict[str, Any]) -> RootFileLocation:
    """
    :param location_payload: {
        "Type": "RootFileLocation",
        "Path": "",
        "Root": ""
    }
    """
    path = location_payload.get('Path')
    root = location_payload.get('Root')

    if not (path and root):
        raise Misconfiguration('Misconfigured RootFileLocation')

    return RootFileLocation(path_starts_with=path, root=root)


def parse_alias_location(location_payload: Dict[str, Any]) -> AliasFileLocation:
    """
    :param location_payload: {
        "Type": "AliasFileLocation",
        "Path": "",
        "Alias": ""
    }
    """
    path = location_payload.get('Path')
    alias = location_payload.get('Alias')

    if not (path and alias):
        raise Misconfiguration('Misconfigured AliasFileLocation')

    return AliasFileLocation(path_starts_with=path, alias=alias)


def parse_proxy_location(location_payload: Dict[str, Any]) -> ProxyPassLocation:
    """
    :param location_payload: {
       "Type": "ProxyPassLocation",
       "Path": "",
       "PassTo": ""
    }
    """
    path = location_payload.get('Path')
    pass_to_server = location_payload.get('PassTo')

    if not (path and pass_to_server):
        raise Misconfiguration('Misconfigured ProxyPassLocation')

    return ProxyPassLocation(path_starts_with=path, pass_to_address=pass_to_server)


LOCATION_PARSERS = {
    'RootFileLocation': parse_root_location,
    'AliasFileLocation': parse_alias_location,
    'ProxyPassLocation': parse_proxy_location,
}

