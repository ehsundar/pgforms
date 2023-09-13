import re
from typing import Type, Dict, Tuple

from pkg.views.base import BaseView


class Router:
    def __init__(self, not_found_view: BaseView):
        self._routes: Dict[re.Pattern, BaseView] = {}
        self._not_found_view = not_found_view

    def register(self, url_pattern: re.Pattern, view: BaseView):
        self._routes[url_pattern] = view

    def route(self, url: str) -> Tuple[BaseView, Dict[str, str]]:
        for r, v in self._routes.items():
            m = r.match(url)
            if m:
                return v, m.groupdict()
        return self._not_found_view, {}
