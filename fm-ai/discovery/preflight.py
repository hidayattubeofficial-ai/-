"""Local preflight checks for FM Computer discovery."""

import importlib.util
import socket
import urllib.request

PORT = 8080
API_URL = f"http://127.0.0.1:{PORT}/health"


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
    lan_ok = []
    for address in addresses:
        try:
            with urllib.request.urlopen(f"http://{address}:{PORT}/health", timeout=3) as response:
                if 200 <= response.status < 300:
                    lan_ok.append(address)
        except Exception:
            pass

    print("LAN API (/health):", ", ".join(lan_ok) if lan_ok else "NOT REACHABLE")
    print("Required bind: 0.0.0.0:8080")
    print("Service:", "_fmcomputer._tcp.")
    print("YouTube auto-publish: OFF")
    print("FM Home approval: REQUIRED")
    if not lan_ok:
        print("Preflight FAILED: bind FM Computer API to 0.0.0.0:8080 and allow LAN TCP/8080.")
        return 1
    if not importlib.util.find_spec("zeroconf"):
        print("Preflight FAILED: install zeroconf.")
        return 1
    print("Preflight PASSED: LAN API is reachable and ready for DNS-SD.")


if __name__ == "__main__":
    main()
