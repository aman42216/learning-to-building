# Day-08 RAG Evaluation

| Configuration | Chunk Size | Top-K | Avg Distance | Relevant Questions | Q6 Policy |
|---|---:|---:|---:|---:|---|
| Config A | 500 | 3 | 0.3662 | 13/15 | Abstain |
| Config B | 1000 | 5 | 0.3695 | 13/15 | Abstain |

**Winner by average retrieval distance:** Config A

Lower average distance indicates closer semantic matches. This is a retrieval comparison, not a measurement of answer correctness.
Q6 abstention is enforced separately by the RAG application.