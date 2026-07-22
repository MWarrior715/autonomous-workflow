# Roadmap — Autonomous Workflow Agent

## v0.1.0 — MVP actual ✅

- [x] Ingesta de lead JSON (por defecto y desde archivo).
- [x] Agente clasificador con score, justificación y riesgos.
- [x] Agente generador de propuestas por email.
- [x] Runner que orquesta el flujo y produce JSON completo.
- [x] CLI principal con flags `--lead`, `--output`, `--email-only`.
- [x] FastAPI opcional con endpoints `/health` y `/run`.
- [x] Proveedor LLM enchufable + fallback determinista.
- [x] Tests unitarios con `pytest`.
- [x] Documentación: README, ARCHITECTURE, DECISIONS, ROADMAP, CHANGELOG, LICENSE.

## v0.2.0 — Resiliencia y trazabilidad

- [ ] Logging estructurado a archivo (`outputs/logs/`).
- [ ] Métricas de flujo: tiempo por agente, tokens estimados, éxitos/errores.
- [ ] Validación de esquema del lead con Pydantic.
- [ ] Manejo de errores por agente con retry configurable.

## v0.3.0 — Integraciones B2B

- [ ] Conector de entrada: webhook genérico para recibir leads.
- [ ] Conector de salida: envío de email vía SMTP o API de email service.
- [ ] Persistencia en SQLite/Postgres con historial por lead.
- [ ] Exportación a CSV/JSONL para análisis comercial.

## v0.4.0 — Multi-agente avanzado

- [ ] Agente de seguimiento (follow-up) con recordatorios.
- [ ] Agente de scheduling para agendar reuniones.
- [ ] Agente de reporting con resumen diario/semanal.
- [ ] Dashboard web simple para visualizar leads y propuestas.

## v1.0.0 — Producto demo cerrado

- [ ] Pipeline CI/CD con tests y lint.
- [ ] Contenedor Docker para despliegue en 1 comando.
- [ ] Demo pública desplegada.
- [ ] Video Loom de demostración de 10 minutos.
