"""Authenticated, loopback-published instructor notebook service."""
import os
from jupyterlab.labapp import LabApp
token=os.environ.get("JUPYTER_TOKEN","")
if len(token)<24 or token.startswith("replace-"):
    raise SystemExit("Set JUPYTER_TOKEN to at least 24 random characters before starting Jupyter")
LabApp.launch_instance(argv=["--ip=0.0.0.0","--port=8888","--no-browser","--ServerApp.root_dir=/opt/cti-lab","--ServerApp.allow_remote_access=False",f"--IdentityProvider.token={token}"])
