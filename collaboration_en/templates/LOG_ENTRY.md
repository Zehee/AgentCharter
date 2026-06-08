<!--
  File Type: Operation Log
  Scope: `logs/{identifier}-log.md`
  Rule: Each log file is written exclusively by the corresponding role. Others read-only.
-->

# Operation Log Specification

## Format

### 1. Date Sections

Each date begins with `## YYYY-MM-DD`, followed by the header and log entries.

### 2. Unified Header

```markdown
| Time | Operation | Target | Notes |
|------|------|------|------|
```

- **Time**: `HH:MM` or `HH:MM:SS`, UTC+8
- **Operation**: use standard terms from the table below
- **Target**: file path, task number, module name, etc.; use `-` if not applicable
- **Notes**: specific description, may include build results, scores, status, etc.

### 3. Operation Types

| Operation | Use Case |
|------|----------|
| `Create` | New file, new task, new report |
| `Edit` | Modify file, modify code |
| `Delete` | Delete file |
| `Move` | Move / rename file |
| `Read` | Read file for review or context |
| `Verify` | Build verification, test run, code check |
| `Review` | Review output, code review |
| `Dispatch` | Dispatch task |
| `Inspect` | Self-check, investigation, code-review |
| `Standby` | Enter standby |
| `Install` | Install dependencies, environment setup |
| `Start` / `Stop` | Start / stop background process |
| `Other` | Custom; describe in Notes field |

### 4. Separators

Use `---` between different date sections.

---

## Example

```markdown
## 2026-05-31

| Time | Operation | Target | Notes |
|------|------|------|------|
| 16:10 | Review | TASK_057 Backend | 8.5/10 ✅ ACCEPTED |
| 16:45 | Verify | `src/mod.rs` | R1 revision passed, 82 pass |

---

## 2026-06-01

| Time | Operation | Target | Notes |
|------|------|------|------|
| 09:00 | Create | TASK_061 | M5 MVP release plan → inbox/ |
```
