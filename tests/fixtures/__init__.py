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

RES_VERSION = "ZEIT/RES"



@pytest.fixture
def math_example_server() -> int:
    host = "127.0.0.1"
    port = _find_free_port()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    stop_event = threading.Event()

    def handle_client(client_sock):
        try:
            client_sock.settimeout(0.5)
            data = client_sock.recv(1024)
            if not data:
                return

            lines = data.decode().split("\r\n")
            method, path, req_id = lines[0].split()
            headers = {}
            i = 1
            while i < len(lines) and lines[i]:
                if ":" in lines[i]:
                    key, value = lines[i].split(":", 1)
                    headers[key.strip()] = value.strip()
                i += 1

            body = "\r\n".join(lines[i+1:]).strip()
            op_type = headers.get("Operation-Type")

            try:
                num = float(body)
            except Exception:
                response = f"{RES_VERSION} 400 {req_id}\r\nContent-Length: 0\r\n\r\n"
            else:
                if op_type == "sum":
                    result = num + num
                elif op_type == "sub":
                    result = num - num
                elif op_type == "mul":
                    result = num * num
                elif op_type == "div":
                    if num == 0:
                        response = f"{RES_VERSION} 400 {req_id}\r\nContent-Length: 0\r\n\r\n"
                        client_sock.sendall(response.encode())
                        return
                    result = num / num
                else:
                    response = f"{RES_VERSION} 400 {req_id}\r\nContent-Length: 0\r\n\r\n"
                    client_sock.sendall(response.encode())
                    return

                body_bytes = str(result).encode()
                response = (
                    f"{RES_VERSION} 200 {req_id}\r\n"
                    f"Content-Length: {len(body_bytes)}\r\n"
                    "Content-Type: text/plain\r\n"
                    "\r\n"
                    f"{result}"
                )
            client_sock.sendall(response.encode())
        finally:
            # Only close the socket when the thread is done
            try:
                client_sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            client_sock.close()

    def server_loop():
        while not stop_event.is_set():
            try:
                client, _ = server_socket.accept()
                threading.Thread(target=handle_client, args=(client,), daemon=True).start()
            except socket.timeout:
                continue
            except OSError:
                break

    thread = threading.Thread(target=server_loop, daemon=True)
    thread.start()

    yield port

    # Only stop the server, don't touch client sockets
    stop_event.set()
    try:
        server_socket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    server_socket.close()
    thread.join()
