
# ShramikSathi – Prompt Comparison Evaluation

## 1. Objective

The objective of this evaluation is to compare two prompt
versions for ShramikSathi using 10 real user questions.

The evaluation checks answer quality, relevance, dataset
grounding, hallucination risk and handling of missing
information.

## 2. Prompt Versions

### Version 1 – Basic Prompt

- Accepts the user's question.
- Generates a general answer using the LLM.
- Does not provide retrieved FAQ context.
- May produce unsupported legal information.

### Version 2 – Dataset-Grounded Prompt

- Uses the user's question.
- Retrieves up to 3 relevant FAQ records using TF-IDF.
- Provides official FAQ context to the LLM.
- Instructs the model not to invent missing information.
- Encourages abstention when information is insufficient.

## 3. Evaluation Dataset

The evaluation used the 10 questions documented in:

`Day-05/docs/user_questions.md`

Both versions were tested on the same 10 questions.

Total LLM responses generated: 20.

- Version 1: 10 responses
- Version 2: 10 responses

Raw responses are stored in:

`Day-06/eval/evaluation_results.json`

## 4. Comparison Table

| No. | Evaluation Question | Version 1 Observation | Version 2 Observation |
|---|---|---|---|
| 1 | Minimum wage | General explanation | More structured and relevant |
| 2 | Gratuity | General explanation | More detailed statutory context |
| 3 | Four Labour Codes | Effective-date claim needs verification | Better structured answer |
| 4 | Wage components | Uses an older law reference | Uses Labour Code context |
| 5 | Leave encashment | Overconfident answer | More cautious explanation |
| 6 | Wedding leave in Maharashtra | Makes an unsupported specific claim | Correctly acknowledges missing information |
| 7 | Contract labour in core activities | Overconfident answer | Gives a potentially unsupported answer; needs review |
| 8 | Gratuity calculation | General calculation explanation | More closely follows FAQ context |
| 9 | Overtime and 50% wage rule | Confuses overtime premium with wage calculation rule | More relevant explanation |
| 10 | ESI coverage | General explanation | Uses more recent FAQ context |

## 5. Evaluation Criteria

The following criteria were used for qualitative comparison:

1. Relevance: Does the response address the user's question?
2. Grounding: Does it use the available official FAQ information?
3. Hallucination risk: Does it introduce unsupported legal claims?
4. Clarity: Is the response understandable to ordinary workers?
5. Abstention: Does it acknowledge missing information?

This is a qualitative evaluation, not a verified legal accuracy benchmark.

## 6. Key Findings

### Version 1

Strengths:
- Provides detailed explanations.
- Uses simple language.
- Can answer general questions.

Limitations:
- Can introduce unsupported legal claims.
- May rely on outdated or unrelated legal references.
- Does not consistently identify dataset limitations.

### Version 2

Strengths:
- Uses retrieved FAQ context.
- Produces more relevant answers for several questions.
- Correctly abstained on Question 6.
- Better aligns with the ShramikSathi dataset.

Limitations:
- Retrieval may return irrelevant or incomplete FAQ records.
- The model can still generate unsupported information.
- Question 7 demonstrates that dataset grounding alone does not guarantee correctness.

## 7. Overall Conclusion

Version 2 is the preferred prompt approach for ShramikSathi
because it incorporates retrieved official FAQ information
before generating answers.

However, the evaluation shows that prompt engineering
alone cannot guarantee legal accuracy.

Future improvements should include:

- Better retrieval relevance thresholds.
- Verification of retrieved FAQ sources.
- Stronger abstention rules.
- Human review of sensitive legal answers.
- Additional testing using real worker questions.

The goal is to make ShramikSathi a helpful and responsible
labour-rights information assistant.

## 8. Evaluation Status

- [x] 10 user questions selected
- [x] Version 1 responses generated
- [x] Version 2 responses generated
- [x] Responses saved in JSON
- [x] Qualitative comparison documented
- [x] Limitations identified
