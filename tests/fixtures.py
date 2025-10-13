import socket
import pytest
import threading


def _find_free_port() -> int:
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

@pytest.fixture
def raw_example_server() -> int:
    host = '127.0.0.1'
    port = _find_free_port()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    connections = []

    def server_loop():
        while True:
            try:
                client, _ = server_socket.accept()
                connections.append(client)  # Keep connection open
            except socket.timeout:
                continue
            except OSError:
                break

    thread = threading.Thread(target=server_loop, daemon=True)
    thread.start()

    yield port

    # Cleanup
    for conn in connections:
        conn.close()
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    thread.join()
