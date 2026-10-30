from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1]
wheels=sorted((root/"wheelhouse").glob("*.whl"))
if not wheels: raise SystemExit("No wheels found")
(root/"wheelhouse/SHA256SUMS").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in wheels))
print("Hashed",len(wheels),"wheels")
