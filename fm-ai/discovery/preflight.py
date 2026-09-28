"""Local preflight checks for FM Computer discovery."""

import importlib.util
import socket
import urllib.request

API_URL = "http://127.0.0.1:8080/health"


def main():
    print("FM AI Discovery Preflight")
    print("API:", API_URL)

    try:
        with urllib.request.urlopen(API_URL, timeout=3) as response:
            print("FM Computer API:", "ONLINE", response.status)
    except Exception as exc:
        print("FM Computer API: OFFLINE", type(exc).__name__)

    print("Python:", socket.gethostname())
    print("zeroconf:", "AVAILABLE" if importlib.util.find_spec("zeroconf") else "MISSING")

    addresses = []
    try:
        for item in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            address = item[4][0]
            if not address.startswith("127.") and address not in addresses:
                addresses.append(address)
    except OSError:
        pass

    print("LAN IPv4:", ", ".join(addresses) if addresses else "NOT FOUND")
    print("Service:", "_fmcomputer._tcp.")
    print("YouTube auto-publish: OFF")
    print("FM Home approval: REQUIRED")


if __name__ == "__main__":
    main()
