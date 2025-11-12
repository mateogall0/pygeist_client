from pygeist_client.abstract.server_message import ServerMessage


class Unrequested(ServerMessage):
    def __init__(self,
                 headers: str,
                 body: str,
                 raw_payload: str,
                 ) -> None:
        self.raw_payload = raw_payload
        self.headers = headers
        self.body = body
