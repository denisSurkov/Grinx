from typing import Dict

from grinx.locations.base import BaseLocation


def register_location(cls: BaseLocation):
    LocationRegistry.Locations[cls.__name__] = cls
    return cls


class LocationRegistry:
    Locations: Dict[str, BaseLocation] = dict()

    def get_by_name(self, name: str) -> BaseLocation:
        return self.Locations[name]
