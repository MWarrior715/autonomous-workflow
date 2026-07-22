"""Lead qualification agent.

Produces a numeric score (1-100), a short justification, and a list of business
risks based on a synthetic B2B lead.
"""

from __future__ import annotations

import logging
from typing import Any

from providers.llm import LLMProvider

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a senior B2B lead qualification analyst.

Your task is to evaluate a sales lead and return a structured JSON object with the following fields exactly:
- "score": integer between 1 and 100 (100 = ideal lead)
- "justification": concise explanation in Spanish, 1-2 sentences
- "risks": array of strings with the main business risks you detect

Respond ONLY with the JSON object. Do not add markdown formatting or extra text."""


def _build_prompt(lead: dict[str, Any]) -> str:
    return (
        "Evalúa el siguiente lead B2B y devuélvelo como JSON.\n\n"
        f"{__import__('json').dumps(lead, ensure_ascii=False, indent=2)}\n\n"
        "Recuerda: score entre 1 y 100, justificación en español, riesgos como lista de strings."
    )


def classify(lead: dict[str, Any], provider: LLMProvider | None = None) -> dict[str, Any]:
    """Classify a lead.

    Args:
        lead: Lead dictionary with fields such as name, company, need, budget.
        provider: Optional LLM provider. If None, the default provider is used.

    Returns:
        A dictionary with normalized keys: score, justification, risks.
    """
    provider = provider or LLMProvider()
    prompt = _build_prompt(lead)

    logger.info("Classifying lead for %s @ %s", lead.get("name"), lead.get("company"))
    result = provider.complete(SYSTEM_PROMPT, prompt, json_mode=True)

    normalized = _normalize(result)
    logger.info("Lead classified with score %d", normalized["score"])
    return normalized


def _normalize(result: dict[str, Any]) -> dict[str, Any]:
    """Ensure the classifier output has the expected shape and types."""
    score = result.get("score")
    if not isinstance(score, int) or not (1 <= score <= 100):
        try:
            score = int(score)
        except (TypeError, ValueError):
            score = 50
    score = max(1, min(100, score))

    justification = result.get("justification") or "Sin justificación disponible."
    if not isinstance(justification, str):
        justification = str(justification)

    risks = result.get("risks") or []
    if isinstance(risks, str):
        risks = [risks]
    risks = [str(r) for r in risks]

    return {"score": score, "justification": justification, "risks": risks}
