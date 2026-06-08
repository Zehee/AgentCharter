> ✅ Read BY BUDDY @ 2026-06-04

# NOTICE_005: Review Flow v3 Change Notice

**From**: Kimi (TPM)
**Date**: 2026-06-04
**Audience**: ALL (flash / Peter / Jim / buddy / Designer)
**Effective**: Immediately

---

## Change Summary

Review flow upgraded from v2 (Kimi fully involved) to v3 (Jim closes loop directly + TASK tiering). Goals: reduce Kimi's context consumption, accelerate review cycles, maintain quality.

**Core changes**:
1. **REVIEW_TASK / REVISION abolished** — Kimi no longer creates review tasks and revision tasks
2. **Jim closes the loop directly** — Jim reviews REPORT → writes REVIEW_REPORT → executor reads → fixes → loop until ACCEPT
3. **TASK tiering** — differentiated by change complexity: P0/P1/P2/P3/Hotfix, Kimi engages at different depths
4. **[Review Summary] flow** — summary accumulates across rounds; executor carries historical information

---

## TASK Tiering Standards

| Level | Criteria | Your Action |
|------|----------|----------|
| **P0** | Single file, pure UI/copy/style/formatting | Submit REPORT → Kimi **directly commits**, no review |
| **P1** | 2-3 files, component-level logic | Submit REPORT → Jim reviews → if fixes needed, enable [Review Summary] in REPORT_R1 |
| **P2** | Cross-module, data flow, new IPC | Submit REPORT → Jim reviews → Kimi reads summary + key opinions → commit |
| **P3** | Architecture/model/security/core flow | Submit REPORT → Jim reviews → Kimi deep verification → commit |
| **Hotfix** | Production emergency | Fast track; may skip Jim as appropriate |

**P0 whitelist**: CSS/styles, copy, icon replacement, layout tweaks, formatting

---

## What You Need to Do

### All Executors (flash / Peter)

1. **After submitting REPORT, proactively scan reviews/**
   - Look for `REVIEW_REPORT_*_{your name}.md` in `docs/collaboration/reviews/`
   - If found, read immediately and fix per the feedback

2. **For multi-round fixes, enable [Review Summary] in REPORT**
   - REPORT template has a pre-commented [Review Summary] section
   - For R1/R2, uncomment it and copy the previous REVIEW_REPORT's [Summary] text verbatim

3. **P0 task REPORTs can be minimal**
   - File list + one-line description + build result is enough

### Jim (CodeReviewer)

1. **No longer read inbox/ REVIEW_TASK**. Instead:
   - Kimi wakes you via internal channel with REPORT number only
   - Read the REPORT from outbox/ autonomously
   - After review, **write REVIEW_REPORT directly to reviews/** (not back to Kimi via internal channel)

2. **[Review Summary] section is mandatory**
   - First round: write only `### R0`
   - R1/R2: copy all historical text from executor's REPORT_RN [Review Summary], append this round at bottom

3. **Notify Kimi after completion**
   ```
   REPORT_XXX review complete
   - Score: X/10
   - 🔴: N | 🟡: N | 💡: N
   - Status: ✅ ACCEPT / 🔄 Fix needed
   - REVIEW_REPORT path: reviews/REVIEW_REPORT_XXX_YYYYMMDD_JIM.md
   ```

---

## Why This Change

| Problem | Solution |
|------|----------|
| Kimi reads every REPORT, context explodes | Tiering: P0 not read, P1 only 5-10 lines of summary |
| Jim and code authors have "no contact" | Jim writes REVIEW_REPORT directly to reviews/; code author reads directly |
| Jim's context unstable across rounds, history lost | Executor carries summary; Jim always reads only the current REPORT |
| REVIEW_TASK/REVISION redundant | Abolished; Jim closes the loop instead |

---

**Questions? Contact Kimi via outbox/BLOCKING or internal channel.**
