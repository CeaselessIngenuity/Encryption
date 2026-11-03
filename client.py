"""
client.py - terminal chat client.

Flow:  you type -> encrypt -> send to server -> server relays ->
       other clients receive -> decrypt -> display
"""
import socket
import threading

from cipher import make_cipher, to_wire, from_wire

PORT = 5000


def receive_loop(sock: socket.socket, cipher) -> None:
    """Runs in a background thread so incoming messages appear while you type."""
    reader = sock.makefile("r", encoding="utf-8")
    try:
        for line in reader:
            line = line.strip()
            if not line:
                continue
            try:
                print(f"\r{from_wire(cipher, line)}\n> ", end="", flush=True)
            except Exception:
                print("\r[could not decrypt a message - wrong key?]\n> ", end="", flush=True)
    except OSError:
        pass
    print("\nDisconnected from server.")


def main() -> None:
    host = input("Server address (blank for this computer): ").strip() or "127.0.0.1"
    name = input("Your name: ").strip() or "anonymous"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, PORT))
    except OSError as e:
        print(f"Could not connect to {host}:{PORT} ({e})")
        return

    cipher = make_cipher()
    threading.Thread(target=receive_loop, args=(sock, cipher), daemon=True).start()

    print("Connected! Type a message and press Enter. Type 'quit' to leave.")
    try:
        while True:
            text = input("> ")
            if text.strip().lower() == "quit":
                break
            if text.strip():
                wire = to_wire(cipher, f"{name}: {text}")
                sock.sendall((wire + "\n").encode("utf-8"))
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        sock.close()


if __name__ == "__main__":
    main()
