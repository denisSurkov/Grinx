from collections import namedtuple
from typing import Optional, List, Tuple
import re

from grinx.middlewares.base import BaseMiddleware
from grinx.requests import BaseRequest, RequestPath
from grinx.responses import BaseResponse

PathRewriteInstruction = namedtuple('PathRewriteInstruction', ['from_path', 'to_path'])


class PathRewriteMiddleware(BaseMiddleware):
    def __init__(self, raw_instructions: List[PathRewriteInstruction], _regexp_rules=None):
        if _regexp_rules:
            self.rewrite_rules = _regexp_rules
        else:
            self.rewrite_rules = self.make_regexp_rules(raw_instructions)

    @staticmethod
    def make_regexp_rules(raw_instructions:  List[PathRewriteInstruction]) -> List[Tuple[re.Pattern, str]]:
        rules = []
        for instruction in raw_instructions:
            from_rule = re.compile(instruction.from_path)
            to_rule = instruction.to_path
            rules.append((from_rule, to_rule))
        return rules

    def new(self) -> 'BaseMiddleware':
        return PathRewriteMiddleware([], self.rewrite_rules)

    async def process_before(self, request: BaseRequest) -> BaseRequest:
        result_path = request.full_path

        for from_, to_ in self.rewrite_rules:
            from_match = from_.match(request.full_path)

            if not from_match:
                continue

            matched_groups = from_match.groups()
            result_path = to_

            if '$' in to_:
                for i, match_group in enumerate(matched_groups):
                    result_path = result_path.replace('$1', match_group)
                break

        request.request_path = RequestPath.from_relative_path(result_path, raise_if_not_correct=True)
        return request

    async def process_after(self, request: BaseRequest, response: Optional[BaseResponse], any_exception: Optional[BaseException] = None) -> BaseResponse:
        return response
