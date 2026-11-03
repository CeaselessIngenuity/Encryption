"""
server.py - relays messages between clients.

The server NEVER decrypts anything. It only sees ciphertext, which is exactly
what an eavesdropper on the network would see. Its printout is your
"man in the middle" demo window.
"""
import socket
import threading

HOST = "0.0.0.0"  # listen on all network interfaces (needed for other devices)
PORT = 5000

clients = []                # all connected sockets
clients_lock = threading.Lock()


def broadcast(line: str, sender: socket.socket) -> None:
    """Send a line to everyone except the person who wrote it."""
    with clients_lock:
        for client in list(clients):
            if client is not sender:
                try:
                    client.sendall((line + "\n").encode("utf-8"))
                except OSError:
                    pass  # that client is gone; its own thread will clean up


def handle_client(conn: socket.socket, addr) -> None:
    print(f"[+] {addr[0]}:{addr[1]} connected")
    reader = conn.makefile("r", encoding="utf-8")
    try:
        for line in reader:
            line = line.strip()
            if line:
                print(f"[{addr[0]}] on the wire: {line}")
                broadcast(line, conn)
    except OSError:
        pass
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"[-] {addr[0]}:{addr[1]} disconnected")


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on port {PORT}. Press Ctrl+C to stop.")

    try:
        while True:
            conn, addr = server.accept()
            with clients_lock:
                clients.append(conn)
            # one thread per client so they can all talk at once
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
