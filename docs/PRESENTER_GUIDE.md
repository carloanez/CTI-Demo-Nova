# Presenter guide

60 minutes, including 28 minutes of notebook demonstration.

Read README.md and docs/CLAUDE_DEPLOYMENT.md for setup. Keep instructor/executed_demo.ipynb available as a visibly labeled replay backup. No local model is used.

HI Cyber Con revision: 22 slides with a conference-themed cover, introduction and QR-code closing. The conference website advertises 45-minute sessions. Confirm the assigned slot before presenting; this deck preserves Carlo's requested 60-minute plan.


## Slide 1: From Threat Intelligence to Detection

00:00–00:30. Open with the audience question: How do you turn a report into an investigation you can run and a detection you can test? Explain that this is a synthetic case with real analysis libraries. The investigation runs locally. Live AI uses the OpenAI API, while offline mode uses an explicitly authored fixture. Promise visible evidence and executable tests. Keep the introduction short and move into the outcome. The cover illustration is original AI-generated conceptual art, inspired by the conference palette rather than an official event asset.


References:
- https://hicybercon.hiddeninvestigations.net/conference
- assets/ARTWORK_AND_SOURCES.md

## Slide 2: Who am I?

00:30–01:30. Introduce yourself in a minute. Connect your cybersecurity experience, training and research to the practical notebook workflow. Cause-Finder provides consulting, change management and AI adoption services. IgniteCyber Academy is the public training brand under Cause-Finder. The portrait and experience/language facts come from the supplied DEFCON introduction. The three logos were supplied by Carlo for inclusion. Do not infer an employment, ownership or formal endorsement relationship from a logo. Close by explaining that this session combines evidence-led investigation, executable detection tests and careful use of AI.


References:
- User-supplied DEFCON introduction slide and original portrait
- User-supplied TCM Security, IgniteCyber Academy and Cause-Finder logos
- User-provided business and training context

## Slide 3: The analyst handoff

01:30–03:00. Describe the artifacts attendees can reproduce. Ask which is hardest in their environment: retrieving evidence, mapping behavior, or testing a rule. Show that each artifact supports a decision. A timeline helps decide what happened; mapping organizes observed behavior; tests expose coverage; the brief communicates uncertainty. Explain that the package includes a ready-to-run notebook and instructor notes.



## Slide 4: The investigation workflow

03:00–05:00. Walk the audience through this table. Reports propose leads. Enterprise events can corroborate some leads but leave other claims unproven. The notebook creates traceable outputs at each stage. AI is a bounded writing and interpretation assistant. It does not get shell access, browse the internet, or deploy detection rules. Introduce the distinction between an observation and an inference, which will recur throughout the demo.



## Slide 5: Project Obsidian

05:00–08:00. Introduce WKSTN-1042, SRV-BUILD-02, and svc_build. Cinder Jackal is a fictional internal cluster name. No real threat actor attribution is implied. Explain that the incident includes conventional enterprise leads and a second threat against the analyst's AI workflow. Do not reveal the poisoned text yet. State that all command strings are data and the notebook never executes them.


References:
- data/reports/R01.md
- data/reports/R07.md

## Slide 6: The expanded corpus

08:00–11:00. Explain the deterministic seed and corpus hash manifest. The enterprise events contain normal background traffic, approved maintenance, and authored adversarial events. The reports preserve an intelligence gap about exfiltration and AI-assisted tooling. The Nova set includes ordinary analysis text, instruction attacks, and security quotations. Ground truth sits in instructor files and is excluded from retrieval. Counts describe an authored teaching fixture, not a sample of production threat prevalence.


References:
- data/manifest.json

## Slide 7: Evidence provenance

11:00–13:00. Show how the case brief links to a numbered passage and then an event. Preserve raw indicators and create a normalized copy for matching. Several indicators can match one event, so distinguish match count from unique event count. ApprovedChange is an enrichment derived from an independent change inventory using host, identity, and time. It is not a native Windows field or an instructor verdict. Explain how change data can be incomplete in a real organization.


References:
- src/cti_lab/investigation.py
- data/reports/R08.md

## Slide 8: Local architecture

13:00–16:00. Explain that offline computation and hosted generation have different requirements. No local inference model is installed. The base Docker profile uses an internal network and replay mode. An explicit live override adds outbound access and mounts an API secret. The notebook, corpus, rules and tests remain local in either mode. A live API error is visible and never silently becomes a replay. The prebuilt container image or Python wheelhouse must be staged before entering a disconnected environment.


References:
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://github.com/Nova-Hunting/nova-framework
- compose.yml
- compose.openai.yml

## Slide 9: ATT&CK mapping follows evidence

16:00–19:00. Explain why a word such as credentials does not establish Unsecured Credentials. A valid-account login does not by itself prove misuse. Walk through the two explicit mappings implemented in the notebook. The log-clear command remains a behavioral lead because an invocation does not establish success, and technique numbering must match the ATT&CK version used. The package links primary technique pages and deliberately avoids an unreviewed complete heat map. Review current definitions before externally reusing mappings.


References:
- https://attack.mitre.org/techniques/T1059/001/
- https://attack.mitre.org/techniques/T1560/001/
- https://attack.mitre.org/resources/versions/

## Slide 10: A testable detection hypothesis

19:00–22:00. State the hypothesis precisely: process creation containing PowerShell, NoProfile, WindowStyle Hidden, and Invoke-WebRequest deserves investigation when no matching approved change exists. It does not cover every PowerShell download or every adversarial technique. Contrast the known-domain baseline with the behavioral rule. Explain that a rule can be syntactically valid and still have poor coverage. Transition to the notebook, and tell the audience that slides 11 through 17 are demo checkpoints.


References:
- rules/sigma/powershell_tuned.yml
- https://github.com/SigmaHQ/pySigma-backend-sqlite

## Slide 11: Demo 1: report intake

22:00–25:00. In the notebook, run setup and sections 1 through 3. Show the printed dependency versions. Open R01 and point out the defanged URL and empty-content SHA256. Run the real MSTICPy DataFrame API and show its engine attribute. Explain why source provenance stays attached to every extraction. Inspect enrichment unknowns instead of assigning an invented malicious verdict. If the live notebook fails, open instructor/executed_demo.ipynb and clearly state that it is the pre-executed replay copy.


References:
- https://msticpy.readthedocs.io/en/latest/api/msticpy.transform.iocextract.html
- notebooks/01_Threat_Intelligence_to_Detection.ipynb

## Slide 12: Demo 2: telemetry pivots

25:00–30:00. Run notebook sections 4 and 5. Inspect a proxy event, its corresponding DNS activity and endpoint command. Point out that the field-aware matcher cannot confuse 203.0.113.4 with 203.0.113.42 or evil.invalid with not-evil.invalid. Sort by timestamp and stable event ID. Explain that examples are authored and timestamps do not establish causation by themselves. Read the ATT&CK table, retain the caveats, and ask the audience which extra evidence would establish archive exfiltration.


References:
- src/cti_lab/investigation.py

## Slide 13: Demo 3: executable Sigma tests

30:00–35:00. Run notebook sections 6 and 7. Show the YAML, its generated SQL, and the matching event IDs. The known-domain rule finds five proxy events and misses five rotated-domain events. The broad PowerShell rule finds seven adversarial endpoint events and two approved maintenance events. The tuned rule retains the seven and suppresses the two by a constrained change join. Do not describe this as production precision or a comparison of vendors. A change record can be missing or wrong. Show the mutation test in tests/test_lab.py if asked whether the evaluator really uses the YAML.


References:
- outputs/detection_metrics.csv
- https://github.com/SigmaHQ/pySigma-backend-sqlite

## Slide 14: Demo 4: an untrusted report passage

35:00–39:00. Open R06 before scanning. Read the quoted instruction as evidence and explain the trust boundary. It arrived in a report, not from the human analyst. Show the second transfer-request specimen and its reserved collector.invalid destination. The notebook never follows the request. Explain that retrieval grounding does not make retrieved content trustworthy. Whether a specific model obeys this injection can vary. The demo does not force or fake successful exploitation; it measures scanning and policy behavior.


References:
- data/reports/R06.md

## Slide 15: Demo 5: Nova rules and policy

39:00–42:00. Run notebook section 8. Open rules/nova/override.nov and explain keywords and condition. The real Nova SDK runs keyword-only rules with LLM evaluation disabled, so this scan remains offline. Nova returns matches; our application separately decides to withhold a chunk. The original report stays unchanged. A known security quotation can go to review_quotation under the exercise policy, but that context is trusted application metadata and must not be supplied by an attacker as an allowlist. A scan hit is not proof of compromise.


References:
- https://github.com/Nova-Hunting/nova-framework/blob/main/nova/sdk/README.md
- rules/nova/override.nov
- src/cti_lab/nova_scan.py

## Slide 16: Demo 6: the held-out gap

42:00–45:00. Run notebook section 9. Compare raw-pattern metrics with application-policy metrics. The development set contains 30 attacks, 20 ordinary samples and 20 quotations. The held-out set contains a separate paraphrase family with 10 attacks, 20 ordinary samples and 20 quotations. All ten held-out attacks are missed by this deliberately narrow rule set. Explain template-family isolation and why retuning on the held-out cases turns them into development data. Proposed next work is a fresh evaluation set plus expanded or semantic rules, not a claim that enabling an LLM guarantees coverage.


References:
- outputs/nova_metrics.csv
- scripts/build_corpus.py

## Slide 17: Demo 7: a cited analyst draft

45:00–50:00. Run notebook sections 10 and 11. For live mode, confirm the live Compose profile or shell configuration before the session. The API receives only the bounded selected synthetic passages. It has no tools. Show store=False, maximum output tokens, the source IDs and exact-quote validation. Interpretations still require review even when quotes validate. If the key, model access, rate limit or internet fails, stop and explicitly select replay. The supplied fixture is instructor-authored and never presented as a captured API result. Export the brief and show run_provenance.json.


References:
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://developers.openai.com/api/docs/guides/migrate-to-responses
- src/cti_lab/assistant.py

## Slide 18: What the detections observe

50:00–52:00. Return to slides. Explain why these are complementary layers. A clean scan cannot establish that an agent is safe, and a process match cannot establish attribution. AI summary output must be checked against sources and events. Emphasize what the audience actually ran: real extraction, rule conversion, SQL execution, real Nova scanning, and an optional hosted drafting request. Separate mechanics, authored data labels, and operational conclusions.



## Slide 19: The wider Nova ecosystem

52:00–54:00. Keep this slide brief. The lab uses open-source Nova and original training rules. PromptIntel can seed a future licensed, curated intelligence workstream. The optional local MCP fixture supports a Proximity exploration outside the main 60-minute flow. Tracer is a Claude Code integration, not a general Jupyter tracer. Its tool-output detection occurs after content is read. Commercial NovaHunting is not bundled or required. Commercial services require separately agreed access and are outside this open-source lab. These teaching results describe only the authored fixtures.


References:
- https://promptintel.novahunting.ai/
- https://github.com/Nova-Hunting/nova-proximity
- https://github.com/Nova-Hunting/nova-tracer
- https://securitybreak.io/novahunting

## Slide 20: A reproducible handoff

54:00–55:00. Show the README, PRESENTER_GUIDE.md and CLAUDE_DEPLOYMENT.md. Mention that the Proxmox handoff uses an Ubuntu guest, not package installation on the hypervisor. The supplied Linux amd64 wheelhouse supports disconnected dependency installation once Python and the OS exist. A container image should be built and exported before a fully disconnected rehearsal. Explain the native path as an alternative. Ask attendees to identify one evidence gap and one false positive in their own future adaptation.


References:
- README.md
- docs/CLAUDE_DEPLOYMENT.md

## Slide 21: Questions

55:00–59:30. Invite questions about evidence, deployment, rule semantics, or AI use. If asked about production accuracy, explain that the metrics describe only the authored corpus. If asked to enable autonomous response, explain that this lab is read-only analysis and does not grant execution permissions to the AI. If time remains, compare the source and analyst-output provenance or show the deliberate held-out paraphrase. Close with the practical outcome: a runnable investigation and a detection you can test.



## Slide 22: Keep learning. Stay connected.

59:30–60:00. Leave this slide visible as you close. Point attendees to the first QR code for the public GitHub repository. Its README links to the notebooks, slides and latest release containing the full offline demo bundle and checksums. The remaining codes open TCM Security, IgniteCyber Academy and Carlo's LinkedIn profile. All four codes use direct HTTPS links without tracking or a shortening service. The images work offline for scanning, while opening the websites requires internet. QR payloads were decoded and checked from the rendered closing slide.


References:
- https://github.com/carloanez/CTI-Demo-Nova
- https://tcm-sec.com/
- https://certifications.tcm-sec.com/privacy-policy/
- https://ignitecyber.academy/
- https://www.linkedin.com/in/carloanez