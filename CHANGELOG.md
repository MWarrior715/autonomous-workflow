# Changelog — Autonomous Workflow Agent

## [0.1.0] - 2026-07-22

### Added

- MVP completo del flujo autónomo B2B: lead → clasificación → propuesta por email.
- `providers/llm.py`: proveedor OpenAI-compatible con fallback determinista.
- `agents/classifier.py`: agente de calificación de leads (score 1-100, justificación, riesgos).
- `agents/proposal.py`: agente generador de emails de propuesta personalizados.
- `workflow/runner.py`: orquestador central del pipeline.
- `cli.py`: interfaz de línea de comandos principal.
- `app.py`: servidor FastAPI opcional para demostraciones HTTP.
- `config.py`: configuración cargada desde `.env`.
- Tests con `pytest` y proveedor simulado.
- Documentación inicial: README, ARCHITECTURE, DECISIONS, ROADMAP, LICENSE.
- Lead de ejemplo en `data/sample-lead.json`.
