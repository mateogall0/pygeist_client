from types import NoneType
import json
from pygeist_client.abstract.server_message import ServerMessage


class Response(ServerMessage):
    def __init__(self,
                 rid: int,
                 headers: str,
                 body: str,
                 status_msg: str,
                 ) -> None:
        self.rid: int = rid
        self.headers = headers
        self.body = body
        self.status_msg: str = status_msg
        self.status = status_msg

    @property
    def status(self) -> int | None:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        try:
            self._status = int(status)
        except ValueError:
            self._status = 500
            return
        if self._status < 100 or self._status > 599:
            self._status = None
