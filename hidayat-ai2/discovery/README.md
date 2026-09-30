# FM Computer LAN Discovery

FM AI mobile discovery uses DNS-SD service type `_fmcomputer._tcp.`.

The FM Computer API must be reachable from the phone over the LAN on TCP port 8080. The server must bind to `0.0.0.0:8080` (not only `127.0.0.1:8080`).

## Required FM Computer configuration

If the FM Computer API is started by Flask, `backend/app.py` already uses `host="0.0.0.0"`. Start that API on port 8080, then run the discovery setup script on the same FM Computer. If Windows Firewall blocks it, allow inbound TCP/8080 on the private LAN profile.

## Files

- `advertise.py` — publishes the DNS-SD service only after LAN `/health` is reachable.
- `preflight.py` — checks local API, LAN reachability, Python, zeroconf and LAN address.
- `setup-and-start.ps1` / `setup-and-start.sh` — isolated setup, preflight and discovery startup.
- `start-discovery.ps1` / `start-discovery.sh` — direct launchers with preflight protection.
- `discovery-status.ps1` — Windows status check.
- `stop-discovery.ps1` / `stop-discovery.sh` — stops the local discovery process.

## Safety

LAN-only discovery; no API keys and no YouTube publishing. Repository changes do not install software on the FM Computer.
