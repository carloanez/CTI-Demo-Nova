"""Verify offline wheel hashes, target tags, pins, and base dependency closure."""
from pathlib import Path
import hashlib
import zipfile
from email.parser import Parser
from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.tags import cpython_tags, compatible_tags
from packaging.utils import canonicalize_name, parse_wheel_filename

root=Path(__file__).resolve().parents[1]
folder=root/"wheelhouse"
platforms=[f"manylinux_2_{n}_x86_64" for n in range(36,4,-1)]+["manylinux2014_x86_64","manylinux2010_x86_64","manylinux1_x86_64"]
allowed=set(cpython_tags((3,12),["cp312"],platforms))|set(compatible_tags((3,12),"cp312",platforms))
env=default_environment();env.update(os_name="posix",sys_platform="linux",platform_system="Linux",platform_machine="x86_64",python_version="3.12",python_full_version="3.12.12",implementation_name="cpython",platform_python_implementation="CPython",extra="")
packages={}
for line in (folder/"SHA256SUMS").read_text().splitlines():
    digest,name=line.split("  ",1)
    wheel=folder/name
    assert hashlib.sha256(wheel.read_bytes()).hexdigest()==digest, name
    parsed,version,_,tags=parse_wheel_filename(name)
    assert tags & allowed, f"No Linux amd64 CPython 3.12 / glibc <= 2.36 tag: {name}"
    with zipfile.ZipFile(wheel) as z:
        metadata=Parser().parsestr(z.read(next(n for n in z.namelist() if n.endswith('.dist-info/METADATA'))).decode())
    packages[canonicalize_name(parsed)]=(version,metadata)
for line in (root/"requirements-linux-amd64.lock").read_text().splitlines():
    if not line or line.startswith('#'): continue
    req=Requirement(line);name=canonicalize_name(req.name)
    assert name in packages and packages[name][0] in req.specifier, f"Missing or wrong pin: {line}"
for name,(version,metadata) in packages.items():
    for item in metadata.get_all('Requires-Dist',[]):
        req=Requirement(item)
        if req.marker and not req.marker.evaluate(env): continue
        dep=canonicalize_name(req.name)
        assert dep in packages, f"Missing dependency of {name}: {req}"
        assert packages[dep][0] in req.specifier, f"Incompatible dependency of {name}: {req}"
print(f"Verified {len(packages)} Linux amd64 CPython 3.12 wheels: hashes, pins, tags and dependency closure")
