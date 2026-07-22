"""Workflow orchestrator.

Executes the autonomous B2B pipeline: lead ingestion → classification → proposal
generation, returning a structured JSON result suitable for logging or API
responses.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from agents.classifier import classify
from agents.proposal import generate_proposal
from providers.llm import LLMProvider

logger = logging.getLogger(__name__)


DEFAULT_LEAD = {
    "name": "Carolina Mendoza",
    "company": "LogiTech Andina",
    "need": "Automatizar el seguimiento de leads entrantes y reducir el tiempo de respuesta comercial.",
    "budget": "$4,000 - $6,000 USD",
    "timeline": "4-6 semanas",
    "source": "formulario web",
}


def run(
    lead: dict[str, Any] | None = None,
    provider: LLMProvider | None = None,
) -> dict[str, Any]:
    """Run the full autonomous workflow on a single lead.

    Args:
        lead: Lead dictionary. If None, a default synthetic lead is used.
        provider: Optional LLM provider.

    Returns:
        Structured workflow result with metadata, classification, and proposal.
    """
    lead = lead or DEFAULT_LEAD.copy()
    provider = provider or LLMProvider()

    started_at = datetime.now(timezone.utc).isoformat()
    logger.info("Starting workflow for lead: %s", lead.get("company"))

    qualification = classify(lead, provider)
    proposal = generate_proposal(lead, qualification, provider)

    result = {
        "workflow": "Autonomous Workflow Agent",
        "version": "0.1.0",
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "lead": lead,
        "classification": qualification,
        "proposal": proposal,
    }

    logger.info("Workflow completed for %s", lead.get("company"))
    return result
