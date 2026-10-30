"""Create a reproducible archive without runtime credentials or private build artifacts."""
from pathlib import Path
import argparse
import hashlib
import tarfile
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--target',type=Path,default=root/"dist")
parser.add_argument('--name',default="CTI_Demo_Nova_v1.0.0_offline.tar.gz")
args=parser.parse_args()
target=args.target
target.mkdir(parents=True,exist_ok=True)
archive=target/args.name
excluded={".git","dist",".venv",".env","secrets","__pycache__",".pytest_cache",".ipynb_checkpoints",".DS_Store","deployment","backups","recordings"}
with tarfile.open(archive,"w:gz") as t:
    for p in sorted(root.rglob("*")):
        rel=p.relative_to(root)
        if not p.is_file() or any(part in excluded or part.endswith('.egg-info') for part in rel.parts) or p.suffix==".pyc": continue
        if p.name.startswith("live_"): continue
        t.add(p,arcname=str(Path("cti-notebook-workflow")/rel),recursive=False)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(target/"SHA256SUMS").write_text(f"{digest}  {archive.name}\n")
print(archive,archive.stat().st_size)
