# FM Computer LAN Discovery

FM AI mobile discovery uses DNS-SD service type `_fmcomputer._tcp.`.

The existing FM Computer API remains unchanged at `127.0.0.1:8080`.

## Files

- `advertise.py` — publishes the local DNS-SD service.
- `preflight.py` — checks API, Python, zeroconf and LAN address.
- `discovery-status.ps1` — Windows status check.
- `install-discovery.ps1` — Windows dependency setup.
- `start-discovery.ps1` — Windows launcher.
- `start-discovery.sh` — Linux/macOS launcher.
- `run-discovery.ps1` / `run-discovery.sh` — direct runners.
- `requirements.txt` — isolated discovery dependency.

## Safety

The discovery helper is LAN-only by design and does not replace the existing API.
It does not contain API keys and does not publish to YouTube.

Actual installation and execution must be performed on the FM Computer; repository changes alone do not install software on that machine.
