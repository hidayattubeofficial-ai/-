"""Advertise the existing FM Computer API on the local LAN via DNS-SD.

This helper does not replace or modify the existing API server.
"""

import os
import socket
import signal
import sys
import time
import urllib.error
import urllib.request

from zeroconf import ServiceInfo, Zeroconf


SERVICE_TYPE = "_fmcomputer._tcp.local."
SERVICE_NAME = "FM Computer._fmcomputer._tcp.local."
DEFAULT_PORT = 8080


def get_lan_addresses():
    addresses = []
    try:
        for item in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            address = item[4][0]
            if address.startswith("127."):
                continue
            if address not in addresses:
                addresses.append(address)
    except OSError:
        pass
    return addresses


def lan_health(address, port):
    try:
        with urllib.request.urlopen(f"http://{address}:{port}/health", timeout=2) as response:
            return 200 <= response.status < 300
    except (OSError, urllib.error.URLError):
        return False


def main():
    port = int(os.getenv("FM_COMPUTER_PORT", str(DEFAULT_PORT)))
    addresses = get_lan_addresses()
    reachable = [address for address in addresses if lan_health(address, port)]

    if not reachable:
        print("FM Computer LAN API is not reachable on any LAN IPv4 address.")
        print("Required: bind the FM Computer API to 0.0.0.0:8080 and allow LAN TCP/8080.")
        return 1

    zeroconf = Zeroconf()
    info = ServiceInfo(
        SERVICE_TYPE,
        SERVICE_NAME,
        addresses=[socket.inet_aton(address) for address in reachable],
        port=port,
        properties={
            b"name": b"FM Computer",
            b"api": b"/health",
            b"scope": b"local-lan",
        },
    )

    zeroconf.register_service(info)
    print(f"FM Computer discovery active: {SERVICE_NAME} port={port}")
    print("Advertised LAN addresses:", ", ".join(reachable))

    stopping = False

    def stop(_signum, _frame):
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    try:
        while not stopping:
            time.sleep(1)
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()
        print("FM Computer discovery stopped.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
