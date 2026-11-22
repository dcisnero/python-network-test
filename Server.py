"""Local TCP server for the network programming assignment."""

import socket
from datetime import datetime

HOST = "127.0.0.1"  # Only accept connections from this computer.
PORT = 50555


def log(message):
    """Print a message with a timestamp for screenshot evidence."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def main():
    """Listen for clients and respond to their messages."""
    try:
        # The with statement closes the socket when the server exits.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)
            log(f"Server listening on {HOST}:{PORT}")
            log("Press Control+C to stop the server.")

            while True:
                connection, address = server.accept()

                with connection:
                    log(f"Client connected: {address}")

                    try:
                        # Newlines separate messages in the TCP stream.
                        with connection.makefile(
                            "r", encoding="utf-8"
                        ) as reader:
                            for line in reader:
                                message = line.rstrip("\n")
                                log(f"Received from client: {message}")

                                if message.lower() == "quit":
                                    connection.sendall(
                                        b"Goodbye! Disconnecting.\n"
                                    )
                                    log("Client requested a clean disconnect.")
                                    break

                                response = f"Server received: {message}\n"
                                connection.sendall(response.encode("utf-8"))
                                log("Response sent to client.")

                    except (OSError, UnicodeError) as error:
                        log(f"Client communication error: {error}")

                log("Client disconnected. Waiting for another connection.")

    except KeyboardInterrupt:
        log("Server stopped by user. Connections closed.")
    except OSError as error:
        log(f"Server error: {error}")


if __name__ == "__main__":
    main()