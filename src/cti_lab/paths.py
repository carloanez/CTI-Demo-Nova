from pathlib import Path
import os

ROOT = Path(os.environ.get("CTI_LAB_ROOT", Path(__file__).resolve().parents[2])).resolve()
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"

def output_dir():
    OUTPUTS.mkdir(exist_ok=True)
    return OUTPUTS
