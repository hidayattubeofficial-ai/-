# Hidayat Video Command Library — Cross-Library Uniqueness Audit

## Audit date
2026-10-01

## Scope
Exact command-name cross-check across:
- v1 verified example batches
- v2 locked example batches
- v3 canonical-expansion candidate JSON

## Results

| Layer | Command count |
|---|---:|
| v1 unique | 98 |
| v2 unique | 75 |
| v3 canonical-expansion candidate | 49 |

### Cross-layer duplicates

- v1 ↔ v2: **1 exact duplicate** — `/goldenhour`
- v1 ↔ v3: **0**
- v2 ↔ v3: **0**
- v3 internal duplicates: **0**

## Important source-of-truth discrepancy

The locked v2 index states **173 unique commands** (98 v1 + 75 v2). The exact command-name audit shows that `/goldenhour` exists in both v1 Weather, Lighting & Effects and v2 Time & Atmosphere.

Therefore, the union of the currently verified v1 and v2 command names is **172 unique commands**, not 173.

This audit does **not** rewrite or silently invalidate the existing v2 lock. The historical v2 lock remains recorded as-is until the source-of-truth decision is explicitly resolved.

## v3 impact

The 49 v3 canonical-expansion candidates have no exact command-name overlap with the verified v1/v2 batch headings.

If the v1/v2 discrepancy is resolved by treating `/goldenhour` as one canonical command, the combined v1+v2+v3 name union is currently **221 unique commands** (98 + 75 + 49 - 1 duplicate).

## Lock status

**FULL LIBRARY LOCK: BLOCKED**

Reason: the existing v2 locked total (173) conflicts with the exact cross-library command-name audit (172 unique across v1+v2).

Required before a final full-library machine-readable lock:
1. Decide the canonical ownership of `/goldenhour`.
2. Record whether v2 remains a 75-command addition count or becomes 74 unique additions.
3. Re-run full duplicate, schema, placeholder, duration, and safety validation.
4. Only then publish the final aggregate count.

## Integrity rule

No command was renamed, deleted, or silently reclassified by this audit. The audit records the discrepancy so the final registry can be locked deliberately rather than hiding a duplicate.
