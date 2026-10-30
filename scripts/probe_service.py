"""Finite localhost startup probe. No external requests, no persistent credentials."""
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request
root=Path(__file__).resolve().parents[1]
with socket.socket() as s:
    s.bind(("127.0.0.1",0));port=s.getsockname()[1]
env=os.environ.copy()
env.update(JUPYTER_PORT=str(port),JUPYTER_TOKEN="local-test-token-not-a-real-secret-123456789",AI_MODE="replay")
log=root/"instructor/service_probe.log"
with log.open("w") as stream:
    proc=subprocess.Popen([sys.executable,str(root/"scripts/serve_native.py")],env=env,stdout=stream,stderr=subprocess.STDOUT)
    try:
        for attempt in range(40):
            if proc.poll() is not None: raise RuntimeError("Jupyter exited; see service_probe.log")
            try:
                request=urllib.request.Request(f"http://127.0.0.1:{port}/api/status",headers={"Authorization":"token "+env["JUPYTER_TOKEN"]})
                with urllib.request.urlopen(request,timeout=2) as response:
                    if response.status==200: break
            except OSError: time.sleep(0.5)
        else: raise RuntimeError("Health probe timed out")
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/lab",timeout=3) as response:
            assert "/login" in response.url, response.url
        print("Local Jupyter authenticated /api/status=200; unauthenticated /lab redirects to login")
    finally:
        proc.terminate()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired: proc.kill();proc.wait()
# The probe token is public test material. Still avoid shipping runtime logs.
log.unlink()
