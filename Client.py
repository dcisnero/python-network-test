"""Local TCP client for the network programming assignment."""

import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 50555


def log(message):
    """Print a message with a timestamp for screenshot evidence."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def main():
    """Connect to the server and exchange messages."""
    try:
        # Allow up to five seconds to establish the connection.
        with socket.create_connection((HOST, PORT), timeout=5) as client:
            log(f"Connected to server at {HOST}:{PORT}")
            log("Type a message, or type quit to disconnect.")

            # Read complete newline-separated responses.
            with client.makefile("r", encoding="utf-8") as reader:
                while True:
                    message = input("Your message: ")
                    client.sendall((message + "\n").encode("utf-8"))

                    response = reader.readline()
                    if not response:
                        log("Server closed the connection.")
                        break

                    log(f"Server response: {response.rstrip()}")

                    if message.lower() == "quit":
                        break

    except ConnectionRefusedError:
        log("Connection refused. Make sure the server is running.")
    except socket.timeout:
        log("Connection timed out. The server did not respond in time.")
    except (OSError, UnicodeError) as error:
        log(f"Connection error: {error}")
    except (KeyboardInterrupt, EOFError):
        log("Client stopped by user.")
    finally:
        log("Client finished. Connection closed.")


if __name__ == "__main__":
    main()