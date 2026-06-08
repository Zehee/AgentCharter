# TASK — sanitized example from the wolf-judge project

This is a real TASK file (names and details altered). It shows what an actual dispatched task looks like.

---

# TASK_042: Search Module Optimization

> **Filename**: `TASK_042_SEARCH-OPT_FLASH.md`
> **Location**: `inbox/`
> **Dispatcher**: Kimi (TPM)
> **Executor**: flash
> **Date**: 2026-06-03
> **Priority**: 🟡 P1
> **Review Level**: P1

---

## Goal

Improve search response time in the role configuration panel. The current fuzzy search blocks the UI thread when there are more than 20 roles in the list.

## Acceptance Criteria

- [x] Debounce search input by 300ms
- [x] Move fuzzy matching to a computed property (non-blocking)
- [x] Add a "no results" state when the search returns empty
- [x] Keep existing exact-match behavior for role names shorter than 3 characters
- [x] Submit `outbox/REPORT_042_20260603_FLASH.md`

## Notes

- Do NOT touch the backend search API — this is frontend optimization only.
- The `RoleFilter` component already has a search slot; reuse it.
