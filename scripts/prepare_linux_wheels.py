"""Build a Linux amd64 / CPython 3.12 wheelhouse from the universal lock."""
from pathlib import Path
import argparse
import hashlib
import subprocess
import sys
from packaging.markers import default_environment
from packaging.requirements import Requirement

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(); parser.add_argument("--download",action="store_true")
args=parser.parse_args()
env=default_environment()
env.update(os_name="posix",sys_platform="linux",platform_system="Linux",platform_machine="x86_64",python_version="3.12",python_full_version="3.12.12",implementation_name="cpython",platform_python_implementation="CPython")
pins=[]
for line in (root/"requirements.lock").read_text().splitlines():
    line=line.strip()
    if not line or line.startswith("#"): continue
    req=Requirement(line)
    if req.marker is None or req.marker.evaluate(env): pins.append(f"{req.name}{req.specifier}")
target=root/"requirements-linux-amd64.lock"
target.write_text("# Generated from requirements.lock for Linux amd64 CPython 3.12\n"+"\n".join(pins)+"\n")
print("Linux pins:",len(pins))
if args.download:
    dest=root/"wheelhouse"; dest.mkdir(exist_ok=True)
    cmd=[sys.executable,"-m","pip","download","--no-deps","--only-binary=:all:","--python-version","312","--implementation","cp","--abi","cp312","--platform","manylinux2014_x86_64"]
    # Debian bookworm uses glibc 2.36; do not select newer-only wheels.
    for glibc in range(17,37): cmd += ["--platform",f"manylinux_2_{glibc}_x86_64"]
    cmd += ["--dest",str(dest),"-r",str(target)]
    subprocess.run(cmd,check=True)
    sums="".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in sorted(dest.glob("*.whl")))
    (dest/"SHA256SUMS").write_text(sums)
