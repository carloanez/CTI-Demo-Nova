"""Convert Sigma with the actual backend and execute against SQLite."""
import json
import sqlite3
from pathlib import Path
import pandas as pd
from sigma.collection import SigmaCollection
from sigma.backends.sqlite import sqliteBackend
from .paths import ROOT

def run_rule(rule_path, events):
    rules = SigmaCollection.from_yaml(Path(rule_path).read_text())
    queries = sqliteBackend().convert(rules)
    if len(queries) != 1: raise ValueError("Expected one query per exercise rule")
    with sqlite3.connect(":memory:") as db:
        events.to_sql("logs", db, index=False)
        matches = pd.read_sql_query(queries[0], db)
    return queries[0], sorted(matches.EventID.tolist())

def metrics(actual, expected, universe):
    a,e,u = set(actual),set(expected),set(universe)
    tp,fp,fn = len(a&e),len(a-e),len(e-a)
    tn = len(u - (a|e))
    return {"TP":tp,"FP":fp,"FN":fn,"TN":tn,"precision":tp/(tp+fp) if tp+fp else 0.0,"recall":tp/(tp+fn) if tp+fn else 0.0}

def evaluate_all(events):
    truth = json.loads((ROOT / "instructor/ground_truth.json").read_text())["expected"]
    matches,queries,rows = {},{},[]
    for path in sorted((ROOT / "rules/sigma").glob("*.yml")):
        name = path.stem
        query, found = run_rule(path, events)
        queries[name], matches[name] = query,found
        # Broad and tuned rules have the same analyst-intent positives.
        expected = truth["powershell_tuned"] if name == "powershell_broad" else truth[name]
        if name == "infrastructure":
            # Match correctness and scenario coverage are different questions.
            expected = [f"PX-A{i:02}" for i in range(1,11)]
        kind = "proxy" if name == "infrastructure" else "endpoint"
        rows.append({"rule":name,**metrics(found,expected,events[events.EventType.eq(kind)].EventID)})
    return {"queries":queries,"matches":matches,"metrics":pd.DataFrame(rows)}
