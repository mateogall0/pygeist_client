from pygeist_client import _adapter


class PygeistClient:
    def __init__(self,
                 unresolved_payload_capacity: int = 2,
                 resolved_payload_capacity: int = 2) -> None:
        self.c = _adapter._create_client(unresolved_payload_capacity,
                                         resolved_payload_capacity)

    def connect(self,
                url: str,
                port: int) -> None:
        _adapter._connect_client(self.c, url, port)

    def disconnect(self) -> None:
        _adapter._disconnect_client(self.c)

    def __del__(self) -> None:
        _adapter._destroy_client(self.c)
