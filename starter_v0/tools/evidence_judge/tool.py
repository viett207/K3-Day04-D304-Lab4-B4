from __future__ import annotations

from typing import Any


def _non_negative_int(value: int, field_name: str) -> int:
    """Validate count-style inputs so scores cannot be distorted by negatives."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return value


def _clean_evidence(items: list[str] | None, field_name: str) -> list[str]:
    if items is None:
        return []
    if not isinstance(items, list) or any(not isinstance(item, str) for item in items):
        raise TypeError(f"{field_name} must be a list of strings")
    return [item.strip() for item in items if item.strip()]


def judge_evidence(
    topic: str = "",
    positive_evidence: list[str] | None = None,
    negative_evidence: list[str] | None = None,
    paper_count: int = 0,
    real_world_examples: int = 0,
    hype_signals: int = 0,
) -> dict[str, Any]:
    positive_evidence = _clean_evidence(positive_evidence, "positive_evidence")
    negative_evidence = _clean_evidence(negative_evidence, "negative_evidence")
    paper_count = _non_negative_int(paper_count, "paper_count")
    real_world_examples = _non_negative_int(real_world_examples, "real_world_examples")
    hype_signals = _non_negative_int(hype_signals, "hype_signals")

    # Independent dimensions make the verdict explainable: positive evidence
    # cannot itself increase the hype score, and each count has a clear weight.
    evidence_score = min(100, len(positive_evidence) * 10 + paper_count * 15)
    hype_score = min(100, hype_signals * 20)
    adoption_score = min(100, real_world_examples * 20)
    risk_score = min(100, len(negative_evidence) * 15)

    if evidence_score >= 70 and adoption_score >= 40 and risk_score < 40 and hype_score < 60:
        verdict = "Strong Opportunity"
    elif evidence_score >= 45 and risk_score < 60:
        verdict = "Promising but uncertain"
    elif hype_score >= 40 or risk_score >= 60:
        verdict = "Potential hype or material risk"
    else:
        verdict = "Mostly hype or too early"

    return {
        "tool": "evidence_judge",
        "topic": topic,
        "positive_evidence": positive_evidence,
        "negative_evidence": negative_evidence,
        "paper_count": paper_count,
        "real_world_examples": real_world_examples,
        "hype_signals": hype_signals,
        "scores": {
            "evidence_score": evidence_score,
            "hype_score": hype_score,
            "adoption_score": adoption_score,
            "risk_score": risk_score,
        },
        "scoring_method": {
            "evidence_score": "10 points per positive evidence item + 15 per paper",
            "hype_score": "20 points per hype signal",
            "adoption_score": "20 points per real-world example",
            "risk_score": "15 points per negative evidence item",
        },
        "verdict": verdict,
        "summary": (
            f"Topic: {topic}. Evidence {evidence_score}/100, hype {hype_score}/100, "
            f"adoption {adoption_score}/100, risk {risk_score}/100. Verdict: {verdict}."
        ),
    }
