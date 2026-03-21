# Confidence Formula

## Formula

```
confidence = (positive - warnings×0.3 - blockers×0.5) / max_signals
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `positive` | int | Number of positive signals |
| `warnings` | int | Number of warning signals |
| `blockers` | int | Number of blocker signals |
| `max_signals` | int | Total signals (positive + warnings + blockers) |

## Thresholds

| Range | Status | Action |
|-------|--------|--------|
| > 0.7 | 🟢 HIGH | Continue |
| 0.4-0.7 | 🟡 MODERATE | Continue but monitor warnings |
| < 0.4 | 🔴 LOW | Pause, resolve blockers |
| blockers >= 2 | 🛑 STOP | Stop, ask human |

## Positive Signals

| Signal | Meaning |
|--------|---------|
| `code_created` | Created code |
| `test_created` | Created tests |
| `test_passed` | Tests passed |
| `refactoring_done` | Refactored successfully |
| `bug_fixed` | Fixed a bug |
| `spec_aligned` | Code matches SPEC |
| `deps_added` | Added dependencies |
| `docs_updated` | Updated documentation |

## Warning Signals

| Signal | Meaning |
|--------|---------|
| `assumption_made` | Used unverified assumption |
| `edge_case_found` | Found edge case |
| `complexity_increased` | Code complexity increased |
| `deps_added` | Added new dependency |
| `confidence_dropped` | Confidence dropped |

## Blocker Signals

| Signal | Meaning |
|--------|---------|
| `spec_unaligned` | Code diverged from SPEC |
| `unknown_blocking` | Unknown issue blocking |
| `decision_blocking` | Need decision to continue |
| `spec_unclear` | SPEC unclear |
| `env_blocking` | Environment issue |
