import re
from typing import Dict

def context_match_score(answer: str, context: str) -> float:
    answer_tokens = set(answer.lower().split())
    context_tokens = set(context.lower().split())
    if not answer_tokens:
        return 0.0
    return len(answer_tokens & context_tokens) / len(answer_tokens)
STOPWORDS = {
    "the", "is", "a", "an", "and", "or", "to", "of",
    "in", "on", "for", "with", "as", "by", "that",
    "this", "it", "are", "was", "were", "be"
}

def normalize(text: str):
    return re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())

def hallucination_detected(answer: str, context: str) -> bool:
    answer_tokens = [
        t for t in normalize(answer)
        if t not in STOPWORDS
    ]

    context_tokens = set(normalize(context))

    if not answer_tokens:
        return False

    unsupported = [
        t for t in answer_tokens
        if t not in context_tokens
    ]

    return len(unsupported) / len(answer_tokens) > 0.4

def faithfulness_score(answer: str, context: str) -> Dict:
    match = context_match_score(answer, context)
    hallucinated = hallucination_detected(answer, context)

    confidence = round(match * (0.5 if hallucinated else 1.0), 2)

    return {
        "context_match": round(match, 2),
        "hallucination": hallucinated,
        "confidence": confidence
    }
