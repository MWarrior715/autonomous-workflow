"""Proposal generation agent.

Produces a personalized sales email (subject + body) based on a qualified lead
and the classifier output.
"""

from __future__ import annotations

import logging
from typing import Any

from providers.llm import LLMProvider

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a senior B2B sales copywriter.

Your task is to write a short, personalized sales email in Spanish for a prospective client. Return a JSON object with exactly these fields:
- "subject": concise email subject line in Spanish
- "body": full email body in Spanish, 3-5 paragraphs, professional tone, with a clear call to action

Respond ONLY with the JSON object. Do not add markdown formatting or extra text."""


def _build_prompt(lead: dict[str, Any], qualification: dict[str, Any]) -> str:
    return (
        "Escribe un email de propuesta personalizado para el siguiente lead.\n\n"
        "Lead:\n"
        f"{__import__('json').dumps(lead, ensure_ascii=False, indent=2)}\n\n"
        "Clasificación del lead:\n"
        f"{__import__('json').dumps(qualification, ensure_ascii=False, indent=2)}\n\n"
        "Devuelve un JSON con 'subject' y 'body'. El tono debe ser profesional, cercano y con una llamada a la acción clara."
    )


def generate_proposal(
    lead: dict[str, Any],
    qualification: dict[str, Any],
    provider: LLMProvider | None = None,
) -> dict[str, str]:
    """Generate a personalized proposal email.

    Args:
        lead: Lead dictionary.
        qualification: Output from the classifier agent.
        provider: Optional LLM provider.

    Returns:
        A dictionary with normalized keys: subject, body.
    """
    provider = provider or LLMProvider()
    prompt = _build_prompt(lead, qualification)

    logger.info("Generating proposal for %s @ %s", lead.get("name"), lead.get("company"))
    result = provider.complete(SYSTEM_PROMPT, prompt, json_mode=True)

    normalized = _normalize(result)
    logger.info("Proposal generated with subject: %s", normalized["subject"])
    return normalized


def _normalize(result: dict[str, Any]) -> dict[str, str]:
    subject = result.get("subject") or "Propuesta personalizada"
    body = result.get("body") or "Estimado/a cliente,\n\nGracias por contactarnos. Quedamos atentos a coordinar una reunión.\n\nSaludos cordiales."
    if not isinstance(subject, str):
        subject = str(subject)
    if not isinstance(body, str):
        body = str(body)
    return {"subject": subject.strip(), "body": body.strip()}
