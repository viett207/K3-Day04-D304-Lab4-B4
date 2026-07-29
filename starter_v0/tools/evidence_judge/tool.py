from __future__ import annotations

from typing import Any


def judge_evidence(
    topic: str = "",
    positive_evidence: list[str] | None = None,
    negative_evidence: list[str] | None = None,
    paper_count: int = 0,
    real_world_examples: int = 0,
    hype_signals: int = 0,
) -> dict[str, Any]:
    positive_evidence = positive_evidence or []
    negative_evidence = negative_evidence or []

    positive_score = min(100, len(positive_evidence) * 12 + paper_count * 10 + real_world_examples * 8)
    negative_score = min(100, len(negative_evidence) * 14 + hype_signals * 10)
    evidence_score = min(100, positive_score)
    hype_score = min(100, max(0, hype_signals * 10 + len(positive_evidence) * 2 - paper_count * 6))
    adoption_score = min(100, real_world_examples * 15 + len(positive_evidence) * 6)
    risk_score = min(100, negative_score)

    if evidence_score >= 75 and risk_score < 40:
        verdict = "Strong Opportunity"
    elif evidence_score >= 50 and risk_score < 60:
        verdict = "Promising but uncertain"
    elif evidence_score >= 40:
        verdict = "Potential hype with real signals"
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
        "verdict": verdict,
        "summary": (
            f"Topic: {topic}. Evidence {evidence_score}/100, hype {hype_score}/100, "
            f"adoption {adoption_score}/100, risk {risk_score}/100. Verdict: {verdict}."
        ),
    }
