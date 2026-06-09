# Contributing to AgentCharter

Thank you for your interest!

## Project Structure

```
collaboration/          # Framework core — Agent-side specs and templates
├── README.md           # Agent collaboration spec (12 chapters)
├── CHARTER.md          # Charter template (TPM fills, then moves to project root)
├── TPM.md              # TPM code of conduct
├── PROJECT.md          # Project config template
├── REGISTER.md         # Registration form
├── ACTIONS.md          # Collaboration link table template
├── templates/          # 15 file templates
├── context/            # Sub-Agent context memory
├── inbox/ outbox/ reviews/ logs/ todos/ archive/

practices/              # Community practice cases
├── wolf-judge/         # 5-person team, full-stack practice
```

## How to Contribute

### Reporting Issues

- Open a GitHub Issue describing the problem
- Bugs: specify which file, which rule, expected behavior
- Framework rule improvements: explain the rationale and impact scope

### Submitting Improvements

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/xxx`
3. Commit your changes: `git commit -m 'description'`
4. Push: `git push origin feature/xxx`
5. Open a Pull Request

### Framework File Modification Principles

AgentCharter's core is rule consistency and simplicity:

- **Minimal changes**: change only what's necessary; leave unrelated content alone
- **Agent perspective**: files under `collaboration/` target AI Agents — avoid human marketing language
- **Generality**: do not introduce assumptions about specific tech stacks or Agent platforms
- **Placeholders**: use `[placeholder]` instead of specific names (e.g., `[your tech stack]`)
- **Template baseline**: `templates/` is a read-only reference; modifying it breaks file format for all downstream instances

### Practice Case Contributions

Submit a `practices/<name>/` directory with a README.md (refer to wolf-judge format). Focus on role setup, collaboration relationships, and custom rules.

## Discussion

For changes requiring community consensus (e.g., new file types, role definition adjustments), open an Issue for discussion first.
