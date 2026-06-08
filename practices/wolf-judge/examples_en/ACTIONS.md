# Collaboration Link Table

Defines who communicates with whom through which channel in the collaboration network. New members are moved here by the TPM from `REGISTER.md` after onboarding.

---

| Action | From → To | Channel |
|------|----------------|------|
| Assign Task | Kimi → flash | inbox/TASK |
| Assign Task | Kimi → Peter | Internal Channel + inbox/TASK (record) |
| Submit Report | flash → Kimi | outbox/REPORT |
| Submit Report | Peter → Kimi | Internal Channel (code diff) + outbox/REPORT |
| Blocking Notice | flash → Peter | outbox/BLOCKING |
| Blocking Notice | Peter → flash | outbox/BLOCKING |
| Active Design Assignment | User → Designer | Direct delivery (not through inbox) |
| Submit Proactive Report | Designer → Kimi | outbox/PROACTIVE_REPORT |
| Blocking Notice | Designer → flash | outbox/BLOCKING |
| Blocking Notice | flash → Designer | outbox/BLOCKING |
| Blocking Notice | Designer → Kimi | outbox/BLOCKING (design baseline change approval) |
| **Review Code** | **Jim → flash** | **REPORT → REVIEW_REPORT (P1/P2/P3, Jim closes loop directly)** |
| **Review Code** | **Jim → Peter** | **REPORT → REVIEW_REPORT (P1/P2/P3, Jim closes loop directly)** |
| **Review Conclusion** | **Jim → flash** | **reviews/REVIEW_REPORT (direct to code author)** |
| **Review Conclusion** | **Jim → Peter** | **reviews/REVIEW_REPORT (direct to code author)** |
| **Quality Confirmation** | **Jim → Kimi** | **Internal Channel "ACCEPT notification" (P1/P2/P3)** |
| **Wake for Review** | **Kimi → Jim** | **Internal Channel lightweight notice (REPORT number only)** |
| **P0 Auto-pass** | **—** | **Kimi directly commits; no Jim involvement** |
| Assign Task | Kimi → buddy | inbox/TASK_TEST |
| Submit Report | buddy → Kimi | outbox/TEST_REPORT |
| Submit Proactive Report | buddy → Kimi | outbox/PROACTIVE_REPORT |
| Blocking Notice | buddy → Kimi | outbox/BLOCKING |
