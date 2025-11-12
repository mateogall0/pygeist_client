from types import NoneType
import json


class ServerMessage:
    @property
    def body(self) -> str | dict | NoneType:
        return self._body

    @body.setter
    def body(self, body: str | dict | NoneType) -> None:
        try:
            self._body = json.loads(body)
        except (json.JSONDecodeError, TypeError) as e:
            self._body = body
            if len(body) == 0:
                self._body = None

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, raw_headers: str) -> None:
        headers = {}
        if not raw_headers:
            return

        lines = raw_headers.splitlines()
        for line in lines:
            if not line.strip():
                continue
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
            else:
                headers[line.strip()] = None
        self._headers = headers

    # def __str__(self) -> str:
    #     return f'Response:\n  status: {self.status}\n  body: {self.body}'

    # __repr__ = __str__
