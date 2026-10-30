"""Execute the notebook and save a separate instructor copy (never overwrites source)."""
from pathlib import Path
import os
import nbformat
from nbclient import NotebookClient
root=Path(__file__).resolve().parents[1]
os.environ["AI_MODE"]="replay"
nb=nbformat.read(root/"notebooks/01_Threat_Intelligence_to_Detection.ipynb",as_version=4)
NotebookClient(nb,timeout=180,kernel_name="python3",resources={"metadata":{"path":str(root)}}).execute()
target=root/"instructor/executed_demo.ipynb"
nbformat.write(nb,target)
print("Executed notebook saved to",target)
