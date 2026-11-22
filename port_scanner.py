"""Simple TCP port scanner. Scan only authorized targets."""

import errno
import socket
import time
from datetime import datetime


def log(message):
    """Print a message with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def parse_ports(text):
    """Accept comma-separated ports or one inclusive range."""
    if "-" in text:
        start, end = map(int, text.split("-"))
        if not 1 <= start <= end <= 65535:
            raise ValueError("Range must be within 1–65535, start <= end.")
        return list(range(start, end + 1))

    ports = sorted(set(int(port.strip()) for port in text.split(",")))
    if not all(1 <= port <= 65535 for port in ports):
        raise ValueError("Port numbers must be between 1 and 65535.")
    return ports


def main():
    """Read inputs, scan ports, and report results."""
    try:
        host = input("Target host: ").strip()
        ports = parse_ports(input("Ports (21,22,80,443 or 5000-5010): "))

        if not host:
            raise ValueError("Target host cannot be empty.")

        address = socket.gethostbyname(host)
        log(f"Scanning {host} ({address}), {len(ports)} ports")
        started = time.perf_counter()
        open_count = 0

        for port in ports:
            # A context manager closes each socket automatically.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1.0)
                result = sock.connect_ex((address, port))

            if result == 0:
                status = "OPEN"
                open_count += 1
            elif result == errno.ECONNREFUSED:
                status = "CLOSED"
            elif result in (errno.ETIMEDOUT, errno.EAGAIN):
                status = "TIMED OUT (filtered or unreachable)"
            elif result in (errno.EHOSTUNREACH, errno.ENETUNREACH):
                log(f"Host/network unreachable at port {port}. Stopping.")
                break
            else:
                status = f"CONNECTION ERROR ({result})"

            log(f"Port {port}: {status}")

        elapsed = time.perf_counter() - started
        log(f"Scan finished. Open ports: {open_count}. Time: {elapsed:.2f}s")

    except ValueError as error:
        log(f"Invalid input: {error}")
    except socket.gaierror:
        log("Host lookup failed. Check the hostname or address.")
    except OSError as error:
        log(f"Network error: {error}")
    except (KeyboardInterrupt, EOFError):
        log("Scanner stopped by user.")


if __name__ == "__main__":
    main()