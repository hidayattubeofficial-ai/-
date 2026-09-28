# FM Computer LAN Discovery

FM AI mobile discovery uses DNS-SD service type `_fmcomputer._tcp.`.

The existing FM Computer API remains unchanged at `127.0.0.1:8080`.
This discovery helper is isolated from the existing website/backend.

## Behavior

- Advertises the FM Computer API port on the local LAN.
- Does not publish YouTube content.
- Does not expose API keys.
- Does not replace the existing local API.
- Intended for the same trusted LAN as the FM AI APK.

## Runtime dependency

The Python helper uses the `zeroconf` package. Install it only in the FM AI local environment:

```text
pip install zeroconf
```

Run:

```text
python advertise.py
```

Stop the process to remove the advertisement.

This file is a source/configuration component only; it does not claim that software has been installed on FM Computer.
