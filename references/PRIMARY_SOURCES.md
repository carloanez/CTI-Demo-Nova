# Primary sources and provenance

Reviewed 2026-10-29. This package adapts the user's DEFCON34 CTI deck and demo concept. The new case material, telemetry, rules and replay fixture were authored for this lesson. Public project descriptions are context, not independent efficacy validation.

| Source | Use |
|---|---|
| https://msticpy.readthedocs.io/en/latest/api/msticpy.transform.iocextract.html | Correct string versus DataFrame extraction shape |
| https://github.com/Nova-Hunting/nova-framework | Nova matching architecture and package |
| https://github.com/Nova-Hunting/nova-framework/blob/main/nova/sdk/README.md | Scan and policy concepts |
| https://github.com/Nova-Hunting/nova-rules | Official rule ecosystem, not redistributed in this bundle |
| https://github.com/SigmaHQ/pySigma-backend-sqlite | Executable local rule conversion |
| https://sigmahq.io/docs/basics/rules.html | Sigma structure and semantics |
| https://attack.mitre.org/techniques/T1059/001/ | PowerShell mapping |
| https://attack.mitre.org/techniques/T1560/001/ | Archive via Utility mapping |
| https://attack.mitre.org/resources/versions/ | ATT&CK release/version awareness |
| https://developers.openai.com/api/docs/guides/structured-outputs | Responses Structured Outputs |
| https://developers.openai.com/api/docs/guides/migrate-to-responses | Responses API storage control |
| https://github.com/Nova-Hunting/nova-proximity | Optional MCP/skills scanner context |
| https://github.com/Nova-Hunting/nova-tracer | Optional Claude Code tracing and passive detection limits |
| https://promptintel.novahunting.ai/ | Intelligence ecosystem context |
| https://securitybreak.io/novahunting | Commercial runtime monitoring context |
| https://docs.docker.com/engine/install/ubuntu/ | Docker guest installation |
| https://pve.proxmox.com/pve-docs/qm.1.html | Proxmox VM reference; verify commands against the target's installed help |

The bundle includes a small curated ATT&CK reference set rather than the full catalog. Live reference pages may change; consult version history and review mappings before reusing externally. Runtime packages are pinned separately. Third-party wheels include their upstream dist-info metadata/license files; no third-party endorsement is implied.
