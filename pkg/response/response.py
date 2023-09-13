import abc
import json
from typing import Dict, Tuple

status_codes = {
    200: "200 OK",
    201: "201 Created",

    301: "301 Moved Permanently",
    307: "307 Temporary Redirect",
    308: "308 Permanent Redirect",

    400: "400 Bad Request",
    401: "401 Unauthorized",
    402: "402 Payment Required",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    406: "406 Not Acceptable",
    408: "408 Request Timeout",
    411: "411 Length Required",
    412: "412 Precondition Failed",
    413: "413 Payload Too Large",
    424: "424 Failed Dependency",
    429: "429 Too Many Requests",

    500: "500 Internal Server Error",
    501: "501 Not Implemented",
    502: "502 Bad Gateway",
    503: "503 Service Unavailable",
    504: "504 Gateway Timeout",
}


class BaseResponse:
    @abc.abstractmethod
    def serialize(self) -> Tuple[bytes, str]:
        raise NotImplemented


class JsonResponse(BaseResponse):

    def __init__(self, response_json: Dict, code: int):
        self._response = response_json
        self._code = code

    def serialize(self) -> Tuple[bytes, str]:
        return json.dumps(self._response).encode("utf-8"), status_codes[self._code]
