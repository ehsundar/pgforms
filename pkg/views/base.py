from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from typing import Type
from urllib.parse import parse_qsl, urlparse

from pkg.response.response import BaseResponse


class BaseView:
    def as_http_request_handler(parent_self) -> Type[BaseHTTPRequestHandler]:

        class WebRequestHandler(BaseHTTPRequestHandler):
            @cached_property
            def url(self):
                return urlparse(self.path)

            @cached_property
            def query_data(self):
                return dict(parse_qsl(self.url.query))

            @cached_property
            def post_data(self):
                content_length = int(self.headers.get("Content-Length", 0))
                return self.rfile.read(content_length)

            @cached_property
            def form_data(self):
                return dict(parse_qsl(self.post_data.decode("utf-8")))

            @cached_property
            def cookies(self):
                return SimpleCookie(self.headers.get("Cookie"))

            def do_GET(self):
                parent_self.handle_get(self)

            def do_POST(self):
                parent_self.handle_post(self)

        return WebRequestHandler

    def handle_get(self, handler: BaseHTTPRequestHandler):
        raise NotImplemented

    def handle_post(self, handler: BaseHTTPRequestHandler):
        raise NotImplemented

    def do_get(self, request) -> BaseResponse:
        raise NotImplemented
