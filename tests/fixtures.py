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
    server_socket.bind((host, port))
    server_socket.listen()
    server_socket.settimeout(0.5)

    connections = []
    stop_event = threading.Event()

    def handle_client(client_sock):
        client_sock.settimeout(0.5)
        data = b""
        try:
            while True:
                try:
                    chunk = client_sock.recv(1024)
                    if not chunk:
                        return
                    data += chunk
                except socket.timeout:
                    break

            if not data:
                return

            lines = data.decode().split("\r\n")
            method, path, id = lines[0].split()
            headers = {}
            i = 1
            while lines[i]:
                key, value = lines[i].split(":", 1)
                headers[key.strip()] = value.strip()
                i += 1
            body = "\r\n".join(lines[i + 1:]).strip()

            op_type = headers.get("Operation-Type")
            try:
                num = float(body)
            except Exception:
                response = f"{RES_VERSION} 400 {id}\r\nContent-Length: 0\r\n\r\n"
            else:
                if op_type == "sum":
                    result = num + num
                elif op_type == "sub":
                    result = num - num
                elif op_type == "mul":
                    result = num * num
                elif op_type == "div":
                    if num == 0:
                        response = f"{RES_VERSION} 400 {id}\r\nContent-Length: 0\r\n\r\n"
                        client_sock.sendall(response.encode())
                        return
                    result = num / num
                else:
                    response = f"{RES_VERSION} 400 {id}\r\nContent-Length: 0\r\n\r\n"
                    client_sock.sendall(response.encode())
                    return

                body_bytes = str(result).encode()
                response = (
                    f"{RES_VERSION} 200 {id}\r\n"
                    f"Content-Length: {len(body_bytes)}\r\n"
                    "Content-Type: text/plain\r\n"
                    "\r\n"
                    f"{result}"
                )
            client_sock.sendall(response.encode())
        except Exception:
            pass

    def server_loop():
        while not stop_event.is_set():
            try:
                client, _ = server_socket.accept()
                client.settimeout(0.5)
                connections.append(client)
                threading.Thread(target=handle_client, args=(client,), daemon=True).start()
            except socket.timeout:
                continue
            except OSError:
                break

    thread = threading.Thread(target=server_loop, daemon=True)
    thread.start()

    yield port

    stop_event.set()
    for conn in connections:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        conn.close()
    try:
        server_socket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    server_socket.close()
    thread.join(timeout=1)




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
            buffer = b""
            while not stop_event.is_set():
                chunk = client_sock.recv(1024)
                if not chunk:
                    break
                buffer += chunk

                while b"\r\n\r\n" in buffer:
                    # Split one full message
                    header_part, remainder = buffer.split(b"\r\n\r\n", 1)
                    buffer = remainder  # keep rest for next loop
                    lines = header_part.decode().split("\r\n")
                    if not lines:
                        continue

                    try:
                        method, path, req_id = lines[0].split()
                    except ValueError:
                        continue

                    headers = {}
                    i = 1
                    while i < len(lines) and lines[i]:
                        if ":" in lines[i]:
                            key, value = lines[i].split(":", 1)
                            headers[key.strip()] = value.strip()
                        i += 1

                    # The body for this message comes from remainder, not the previous buffer
                    body = remainder.decode().strip()
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
                                continue
                            result = num / num
                        else:
                            response = f"{RES_VERSION} 400 {req_id}\r\nContent-Length: 0\r\n\r\n"
                            client_sock.sendall(response.encode())
                            continue

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
            client_sock.close()



    def server_loop():
        while not stop_event.is_set():
            try:
                client, _ = server_socket.accept()
                threading.Thread(target=handle_client, args=(client,), daemon=True).start()
            except OSError:
                break

    thread = threading.Thread(target=server_loop, daemon=True)
    thread.start()

    yield port

    stop_event.set()
    try:
        server_socket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    server_socket.close()
    thread.join()
