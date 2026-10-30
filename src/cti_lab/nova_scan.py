"""Actual Nova SDK integration with a separately visible application policy."""
from functools import lru_cache
import json
import pandas as pd
from nova.sdk import Nova
from .paths import ROOT, DATA
from .detection import metrics

@lru_cache(maxsize=1)
def engine():
    return Nova(rules_path=ROOT / "rules/nova", policy={"CTI":{"action":"flag"}}, auto_redact=False)

def scan(text, context="external_report"):
    result = engine().scan(text, skip_llm=True, parallel=False)
    raw_match = bool(result.matches)
    action = "review_quotation" if raw_match and context == "security_quotation" else "withhold_chunk" if raw_match else "allow"
    return {"raw_match":raw_match,"matched_rules":[m.rule_name for m in result.matches],"policy_action":action,"warnings":result.warnings}

def evaluate_cases():
    cases = json.loads((DATA / "nova_cases.json").read_text())
    labels = json.loads((ROOT / "instructor/nova_labels.json").read_text())
    rows = [{**c, **scan(c["text"],c["context"]), **labels[c["case_id"]]} for c in cases]
    df = pd.DataFrame(rows)
    scores = []
    for split in ["development", "heldout"]:
        part = df[df.split.eq(split)]
        for stage,col in [("raw_pattern","raw_match"),("application_policy","policy_action")]:
            actual = part.loc[part[col].eq("withhold_chunk") if stage == "application_policy" else part[col], "case_id"]
            expected = part.loc[part.expected_attack,"case_id"]
            scores.append({"split":split,"stage":stage,**metrics(actual,expected,part.case_id)})
    return {"cases":df,"metrics":pd.DataFrame(scores)}
