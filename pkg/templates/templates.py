import os.path
from typing import Any, Dict

from jinja2 import Template


class Templates:
    def __init__(self, templates_directory: str):
        self._templates_directory: str = templates_directory

    def render(self, ident: str, data: Dict) -> str:
        cwd = os.path.curdir
        abs_path = os.path.join(cwd, self._templates_directory, ident)

        abs_path += ".html"

        with open(abs_path, 'r') as f:
            t = Template(f.read())
            return t.render(data)
