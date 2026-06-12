# Claim Evidence Matrix

Every major manuscript claim must map to verified evidence before it appears in the Chinese or English draft.

| claim_id | manuscript_section | claim_text | evidence_type | evidence_path | result_id_or_citation | status | notes |
|---|---|---|---|---|---|---|---|
| C001 | Introduction |  | literature |  |  | pending |  |
| C002 | Results |  | metric/table/figure/log |  |  | pending |  |
| C003 | Discussion |  | failure_case/limitation |  |  | pending |  |

Allowed `evidence_type` values include `metric`, `table`, `figure`, `log`, `config`, `checkpoint`, `dataset_report`, `preprocess_report`, `hardware_report`, `citation`, and `limitation`.

Use `status = verified` only when the claim text exactly matches the evidence. Use `status = revise` when the evidence supports a weaker claim. Use `status = blocked` when evidence is missing.
