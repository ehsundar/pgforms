from http.server import HTTPServer

from internal.views.index import IndexView
from pkg.templates.templates import Templates


def main():
    t = Templates("templates/")

    server = HTTPServer(("", 8000), IndexView(t).as_http_request_handler())
    server.serve_forever()


if __name__ == '__main__':
    main()
