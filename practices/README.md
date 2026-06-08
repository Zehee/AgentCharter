# Practice Cases

> AgentCharter is a framework, not a set of rigid rules. Different teams and projects evolve different collaboration patterns.
> These cases show how to configure and use AgentCharter in real projects.

---

## Case Index

| Case | Team | Tech Stack | Scale | Key Features |
|------|------|--------|------|----------|
| [wolf-judge](./wolf-judge/README_en.md) | 5 | Tauri + Rust + Vue 3 | 120+ tasks | P0-P3 tiered review, Sub-Agent context memory — [examples](./wolf-judge/examples_en/) |

---

## How to Use

1. Read cases close to your project's scale and tech stack
2. Focus on `PROJECT.md` (team config) and `ACTIONS.md` (collaboration relationships)
3. Reference their task dispatch strategy, review process, archive rules
4. Adapt to your project's actual requirements

---

## Contributing Practice Cases

If you have successful AgentCharter practice experience, contributions are welcome. Submit a PR with:

```
practices/<your-practice-name>/
├── README.md           # Case overview (required)
├── CHARTER.md          # Cooperation charter (required)
├── PROJECT.md          # Team config (required)
├── ACTIONS.md          # Collaboration links (required)
└── extra/              # Additional reference material (optional)
```

> Before contributing, sanitize sensitive data (keys, internal URLs, personal info).
