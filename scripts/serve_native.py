import os
from pathlib import Path
from dotenv import load_dotenv
from jupyterlab.labapp import LabApp
root=Path(__file__).resolve().parents[1]
load_dotenv(root/".env")
token=os.getenv("JUPYTER_TOKEN","")
if len(token)<24 or token.startswith("replace-"): raise SystemExit("Set a random JUPYTER_TOKEN of at least 24 characters in .env")
LabApp.launch_instance(argv=["--ip=127.0.0.1","--port="+os.getenv("JUPYTER_PORT","8888"),"--no-browser","--ServerApp.root_dir="+str(root),f"--IdentityProvider.token={token}"])
