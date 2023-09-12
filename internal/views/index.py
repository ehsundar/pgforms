from http.server import BaseHTTPRequestHandler

from pkg.views.base import BaseView
from pkg.templates.templates import Templates


class IndexView(BaseView):

    def __init__(self, templates: Templates):
        self._templates = templates

    def handle_get(self, handler: BaseHTTPRequestHandler):
        resp = self._templates.render("index", {})

        handler.send_response(200)
        handler.send_header("Content-Type", "text/html")
        handler.end_headers()
        handler.wfile.write(resp.encode("utf-8"))
