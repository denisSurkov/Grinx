from typing import Dict

from grinx.middlewares.base import BaseMiddleware


def register_middleware(cls: BaseMiddleware):
    MiddlewareRegistry.Middlewares[cls.__name__] = cls
    return cls


class MiddlewareRegistry:
    Middlewares: Dict[str, BaseMiddleware] = dict()

    def get_by_name(self, name: str) -> BaseMiddleware:
        return self.Middlewares[name]
