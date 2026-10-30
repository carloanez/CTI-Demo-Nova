"""Transparent, field-aware investigation helpers. Never executes telemetry commands."""
import hashlib
import importlib.metadata
import json
import re
from urllib.parse import urlsplit
import pandas as pd
from .paths import ROOT, DATA, output_dir

def versions():
    return {p: importlib.metadata.version(p) for p in ["msticpy", "nova-hunting", "pysigma", "pysigma-backend-sqlite", "openai"]}

def load_sources():
    return json.loads((DATA / "sources.json").read_text())

def normalize(value):
    value = str(value).strip().strip("`'\"").rstrip(".,;")
    value = re.sub(r"^hxxps://", "https://", value, flags=re.I)
    value = re.sub(r"^hxxp://", "http://", value, flags=re.I)
    return value.replace("[.]", ".").lower()

def extract_iocs(sources):
    from msticpy.transform.iocextract import IoCExtract
    extractor = IoCExtract()
    rows = []
    for source in sources:
        # DataFrame input produces a DataFrame with Observable, IoCType and SourceIndex.
        found = extractor.extract(data=pd.DataFrame({"text": [source["text"]]}), columns=["text"], ignore_tlds=True)
        if not isinstance(found, pd.DataFrame):
            raise TypeError("MSTICPy changed its extraction return shape; do not silently fallback")
        for _, row in found.iterrows():
            raw = str(row["Observable"])
            typ = {"dns":"domain", "md5_hash":"md5", "sha256_hash":"sha256", "sha1_hash":"sha1"}.get(row["IoCType"], row["IoCType"])
            if typ not in {"url", "domain", "ipv4", "ipv6", "md5", "sha1", "sha256"}: continue
            rows.append({"raw_observable": raw, "indicator": normalize(raw), "ioc_type": typ, "source_id": source["source_id"]})
    df = pd.DataFrame(rows, columns=["raw_observable", "indicator", "ioc_type", "source_id"]).drop_duplicates().reset_index(drop=True)
    df.attrs["engine"] = "MSTICPy IoCExtract (DataFrame API; no fallback)"
    return df

def enrich(iocs):
    ti = pd.DataFrame(json.loads((DATA / "ti.json").read_text())).rename(columns={"source_id":"enrichment_source_id"})
    return iocs.merge(ti, on="indicator", how="left").fillna({"verdict":"unknown", "confidence":"unassessed"})

def load_events():
    frames = [pd.read_csv(p) for p in sorted((DATA / "logs").glob("*.csv"))]
    df = pd.concat(frames, ignore_index=True).sort_values(["timestamp", "EventID"]).reset_index(drop=True)
    # Explicit numeric boolean enrichment, supported predictably by SQLite.
    df["ApprovedChange"] = 0
    for change in json.loads((DATA / "changes.json").read_text()):
        mask = (df.Computer.eq(change["Computer"]) & df.User.eq(change["User"]) & df.timestamp.between(change["start"], change["end"]))
        df.loc[mask, "ApprovedChange"] = 1
    return df

def correlate(iocs, events):
    hits = []
    for _, row in events.iterrows():
        seen = set()
        for _, ioc in iocs.iterrows():
            val, typ = ioc.indicator, ioc.ioc_type
            field = None
            if typ in {"ipv4", "ipv6"}:
                field = next((k for k in ["src_ip", "dst_ip", "answer"] if str(row.get(k, "")) == val), None)
            elif typ in {"url", "domain"}:
                url = str(row.get("url", ""))
                host = urlsplit(url).hostname or ""
                if typ == "url" and normalize(url) == val: field = "url"
                elif typ == "domain" and val in {host.lower(), str(row.get("query", "")).lower()}: field = "url_host" if host.lower() == val else "query"
            elif typ in {"md5", "sha1", "sha256"} and str(row.get(typ, "")).lower() == val:
                field = typ
            if field and (val, ioc.source_id) not in seen:
                seen.add((val, ioc.source_id))
                hits.append({"EventID": row.EventID, "timestamp": row.timestamp, "Computer": row.Computer, "indicator": val, "matched_field": field, "source_id": ioc.source_id})
    return pd.DataFrame(hits, columns=["EventID","timestamp","Computer","indicator","matched_field","source_id"])

def timeline(events, host=None):
    result = events if host is None else events[events.Computer.eq(host)]
    return result.sort_values(["timestamp", "EventID"])[["timestamp","EventID","EventType","Computer","User","CommandLine","url"]]

def attack_evidence(events):
    """Small analyst-reviewed evidence map, not automated attribution or complete ATT&CK coverage."""
    rows = []
    checks = [
        ("T1059.001", "PowerShell", "Image", r"powershell\.exe$", "Process invocation observed; malicious intent needs surrounding context.", "https://attack.mitre.org/techniques/T1059/001/"),
        ("T1560.001", "Archive via Utility", "CommandLine", r"^tar -czf", "Archive command observed; successful exfiltration is unconfirmed.", "https://attack.mitre.org/techniques/T1560/001/"),
    ]
    for tid, name, field, pattern, assessment, url in checks:
        selected = events[events[field].fillna("").str.contains(pattern, case=False, regex=True) & events.ApprovedChange.eq(0)]
        if len(selected): rows.append({"technique_id":tid,"technique":name,"event_ids":", ".join(selected.EventID),"assessment":assessment,"reference":url})
    return pd.DataFrame(rows)

def export_case(events, iocs, enriched, hits, mappings, detections, nova_results, draft):
    from .assistant import render
    out = output_dir()
    for name, frame in [("iocs",iocs),("enriched_iocs",enriched),("correlations",hits),("timeline",timeline(events)),("attack_evidence",mappings),("detection_metrics",detections["metrics"]),("nova_metrics",nova_results["metrics"]),("nova_case_results",nova_results["cases"])]:
        frame.to_csv(out / f"{name}.csv", index=False)
    (out / "sigma_queries.json").write_text(json.dumps(detections["queries"], indent=2))
    (out / "sigma_matches.json").write_text(json.dumps(detections["matches"], indent=2))
    (out / "ai_draft.json").write_text(json.dumps(draft, indent=2))
    brief = "# Obsidian analyst brief\n\nSynthetic exercise. Experimental detections require review.\n\n" + render(draft)
    brief += f"\n\n## Reproducibility\n\nEvents: {len(events)}. Unique correlated events: {hits.EventID.nunique()}.\n\n"
    brief += "ATT&CK mapping covers only the evidence-backed techniques in attack_evidence.csv. Log clearing is preserved as a behavior lead pending version-specific mapping review.\n\n"
    brief += "Detection results describe this authored fixture. They are not vendor performance benchmarks. No NovaHunting commercial pilot data is used.\n"
    (out / "analyst_brief.md").write_text(brief)
    (out / "run_provenance.json").write_text(json.dumps({"versions":versions(),"corpus_manifest_sha256":hashlib.sha256((DATA / "manifest.json").read_bytes()).hexdigest(),"ai_provenance":draft["provenance"]},indent=2))
    return str(out)
