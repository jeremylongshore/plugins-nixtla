# Sales Demo Builder - Status

**Plugin:** nixtla-sales-demo-builder
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Current Status: Planned

| Phase | Status | Notes |
|-------|--------|-------|
| Business Case | Complete | High priority - direct revenue impact |
| PRD | Complete | Requirements defined |
| Architecture | Complete | Design documented |
| User Journey | Complete | Workflows mapped |
| Technical Spec | Complete | APIs specified |
| Implementation | Not Started | Awaiting prioritization |
| Testing | Not Started | - |
| Documentation | Not Started | - |
| Deployment | Not Started | - |

---

## Timeline

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| PRD Complete | 2025-12-15 | Done |
| MVP Development | TBD | Not Started |
| Retail Template | TBD | Not Started |
| Energy Template | TBD | Not Started |
| Finance Template | TBD | Not Started |
| Production Release | TBD | Not Started |

---

## Estimated Effort

| Component | Effort |
|-----------|--------|
| Core template engine | 1 week |
| Dataset registry | 0.5 weeks |
| Retail vertical | 0.5 weeks |
| Energy vertical | 0.5 weeks |
| Finance vertical | 0.5 weeks |
| Comparison engine | 0.5 weeks |
| Export functionality | 0.5 weeks |
| **Total** | **3-4 weeks** |

Additional verticals: +1 week each

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| M5 Dataset | Available | Public, CC license |
| Energy Data | Available | Public utility data |
| Yahoo Finance | Available | Free API |
| Prophet | Available | Open source |
| statsforecast | Available | Nixtla open source |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Dataset availability | Low | Medium | Cache locally, multiple sources |
| Notebook execution fails | Medium | High | Pre-validate all templates |
| Slow generation | Low | Medium | Async processing, caching |

---

## Success Criteria

- [ ] Demo prep time: 4 hours → 15 minutes
- [ ] Sales cycle reduction: 20%
- [ ] Win rate increase: 10%
- [ ] Demo satisfaction: 9/10

---

## Related Documents

- [01-BUSINESS-CASE.md](./01-BUSINESS-CASE.md)
- [02-PRD.md](./02-PRD.md)
- [03-ARCHITECTURE.md](./03-ARCHITECTURE.md)
- [04-USER-JOURNEY.md](./04-USER-JOURNEY.md)
- [05-TECHNICAL-SPEC.md](./05-TECHNICAL-SPEC.md)
