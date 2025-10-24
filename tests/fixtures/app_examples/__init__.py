import socket
import time
from pygeist.testclient import multiprocessing


def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def server_start(app) -> multiprocessing.Process:
    server_process = multiprocessing.Process(target=app.run)
    server_process.start()

    for _ in range(500):
        try:
            with socket.create_connection(("127.0.0.1", app.port), timeout=0.1):
                break
        except OSError:
            time.sleep(0.001)
    else:
        raise RuntimeError("server did not start in time")
    return server_process

def server_stop(server_process):
    server_process.terminate()
    server_process.join()
