from pkg.response.response import JsonResponse
from pkg.views.base import BaseView


class TableListView(BaseView):
    def __init__(self, storage):
        self._storage = storage

    def do_get(self, request):
        print(request)
        return JsonResponse({"hello": "world"}, 200)
