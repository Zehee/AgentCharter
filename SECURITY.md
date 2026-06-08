# Security Policy

## Reporting a Vulnerability

AgentCharter is a framework project with no runtime code. If you discover a security risk in its rule design or templates (e.g., privilege escalation vectors, data leak scenarios), please:

- **Do not open a public Issue**
- Contact the project maintainer (via GitHub private message if no email is published)
- We will acknowledge within 48 hours and begin remediation

## Supported Versions

| Version | Support Status |
|------|----------|
| v3.x (current) | ✅ Actively supported |

## Security Considerations

AgentCharter's risk surface is primarily in:

- **Git isolation rules**: ensuring non-TPM Agents cannot execute git commands
- **Permission table accuracy**: incorrect read/write directions in `ACTIONS.md` could allow Agents to accidentally modify others' files
- **Context injection safety**: `context/` memory files containing sensitive credentials must be sanitized by the TPM before injection

These risks are mitigated by the user project's TPM through `CHARTER.md`. The framework provides only the rule templates.
