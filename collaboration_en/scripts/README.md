# AgentCharter Scripts

**Python 3 optional tools — protocol layer is the foundation, scripts are enhancement.**
No Python? Directory structure, naming conventions, and ACTIONS.md flow tables work fine.
With Python? Scripts save memory and prevent mistakes.

---

## Entry Points

| Role | Command | Available Scripts |
|------|---------|------------------|
| **External Agent** | `python agent.py <NAME>` | new-report / new-review-report / new-decision / new-blocking / new-blocking-reply / validate-file |
| **TPM** | `python tpm.py TPM` | All commands + overview patrol + archive |

> External Agent's `new-decision` auto-creates a PROACTIVE_REPORT for TPM review.

## External Agent Commands

```
python agent.py KIMI               → identity + patrol (@KIMI only)
python agent.py KIMI new-report     → template schema + available ref numbers
python agent.py KIMI new-report '{"ref_nnn":"042"}' → create file
```

## TPM Commands

```
python tpm.py TPM                   → overview patrol + @TPM tasks
python tpm.py TPM daily-check       → full validation scan
python tpm.py TPM new-task '{"assignee":"KIMI","goal":"..."}' → create TASK
python tpm.py TPM new-revision '{"assignee":"KIMI","ref_nnn":"042"}' → create revision
python tpm.py TPM archive           → chain archive
```

## Three Calling Modes

Every `new-*.py` supports three modes:

```
no args         → output all {{variables}} from template
NAME only       → template + your pending tasks
NAME + JSON     → validate and create file
```

> 💡 **No need to memorize template fields**: run once with no args to see all required fields.

## Redline Reminder

Every command appends the project's redlines at the end of its output — always reminding what must never be broken.
