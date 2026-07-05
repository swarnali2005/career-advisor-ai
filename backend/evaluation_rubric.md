\# Evaluation Rubric: Explainable, Affect-Aware Career Advisor vs. Baseline LLM



\## Dimension A: Groundedness (1-5 scale)

1 = Entirely generic, no verifiable facts, could apply to any career

2 = Mostly generic with occasional specific claims

3 = Mix of grounded and generic content

4 = Mostly grounded, minor generic filler

5 = Every claim traceable to a specific, real source fact



\## Dimension B: Affect-Appropriateness (1-5 scale)

1 = Response structure/tone identical regardless of user's emotional state

2 = Minor tonal gesture, but structure/depth unchanged

3 = Some adaptation in wording, but overall delivery similar across affect states

4 = Clear adaptation in structure and tone matching affect

5 = Response fully reshaped (length, structure, framing) to match affect state



\## Scoring: Baseline vs. System



| Test Message | Baseline Groundedness | System Groundedness | Baseline Affect-Fit | System Affect-Fit |

|---|---|---|---|---|

| "everything feels overwhelming..." (anxious) | 1 | 5 | 2 | 5 |

| "pretty confident... software engineering" (confident) | 1 | 5 | 2 | 5 |

| "can't decide between medicine and engineering" (undecided) | 2 | 5 | 2 | 5 |

| "don't understand what a data analyst does" (confused) | 1 | 5 | 2 | 5 |



\*\*Note:\*\* Baseline groundedness scored 1-2 throughout because claims (e.g., specific salary ranges) are unsourced and could be fabricated; System groundedness scored 5 throughout because every claim traces to a retrieved O\*NET document, verifiable in `career\_kb.jsonl`.

