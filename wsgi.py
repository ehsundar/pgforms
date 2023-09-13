import re
from pprint import pprint
from wsgiref.simple_server import make_server
from wsgiref.types import WSGIEnvironment, StartResponse

from internal.views.tables import TableListView
from pkg.router.router import Router


def app_factory():
    storage = {}

    r = Router(None)
    r.register(re.compile(r"/tables/(?P<table_name>\w+)/(?P<row_id>\d+)/"), TableListView(storage))

    def application(environ: WSGIEnvironment, start_response: StartResponse):
        pprint(environ)
        url = environ.get("PATH_INFO")
        view, params = r.route(url)
        response = view.do_get(params)

        response_bytes, code = response.serialize()

        start_response(code, [])

        return [response_bytes]

    return application


app = app_factory()

if __name__ == "__main__":
    server = make_server('localhost', 8000, app=app)
    server.serve_forever()
