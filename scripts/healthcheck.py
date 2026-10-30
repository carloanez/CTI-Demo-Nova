import os
import urllib.request
port=os.getenv("JUPYTER_PORT","8888")
request=urllib.request.Request(f"http://127.0.0.1:{port}/api/status",headers={"Authorization":"token "+os.environ["JUPYTER_TOKEN"]})
with urllib.request.urlopen(request,timeout=3) as response:
    if response.status!=200: raise SystemExit(1)
