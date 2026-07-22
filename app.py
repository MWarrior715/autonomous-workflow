"""Optional FastAPI server for live demonstrations.

Endpoints:
    POST /run       Run the workflow with an optional lead JSON payload.
    GET  /health    Health check.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from workflow.runner import DEFAULT_LEAD, run

app = FastAPI(
    title="Autonomous Workflow Agent",
    version="0.1.0",
    description="Lead qualification and proposal generation powered by an autonomous AI workflow.",
)


class Lead(BaseModel):
    """Lead schema accepted by the workflow endpoint."""

    name: str = Field(..., description="Contact name")
    company: str = Field(..., description="Company name")
    need: str = Field(..., description="Business need or problem statement")
    budget: str = Field(..., description="Budget range")
    timeline: str = Field(default="", description="Expected timeline")
    source: str = Field(default="api", description="Lead source")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "Autonomous Workflow Agent"}


@app.post("/run")
def run_workflow(lead: Lead | None = None) -> dict[str, Any]:
    """Run the full autonomous workflow on the provided lead."""
    lead_dict = lead.model_dump() if lead else None
    return run(lead=lead_dict)


@app.get("/run")
def run_workflow_default() -> dict[str, Any]:
    """Run the workflow with the default synthetic lead."""
    return run(lead=DEFAULT_LEAD.copy())
