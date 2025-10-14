class Response:
    def __init__(self,
                 rid: int,
                 headers: str,
                 body: str,
                 status_msg: str,
                 ) -> None:
        self.rid: int = rid
        self.headers: str = headers
        self.body: str = body
        self.status_msg: str = status_msg
        self.status = int(status_msg)
