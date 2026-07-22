# Autonomous Workflow Agent

> **PoC 03 — AI Product Lab**  
> Automatización B2B con agentes inteligentes: un lead ingresa, se califica y se genera una propuesta por email lista para enviar.

## ¿Qué demuestra?

En una demo de 10 minutos este repositorio responde la pregunta clave de un CTO:

**"¿Puede esta persona automatizar procesos reales de negocio con IA?"**

El flujo es completamente autónomo:

1. **Ingesta** de un lead B2B (JSON).
2. **Clasificación inteligente**: score 1-100, justificación y riesgos detectados.
3. **Generación de propuesta**: email personalizado en español basado en el perfil del lead.
4. **Output estructurado**: JSON completo del flujo + email listo para usar.

## Stack

- **Python puro** — sin dependencias de plataformas visuales.
- **Motor de IA Local/Cloud** vía API OpenAI-compatible (configurable en `.env`).
- **Pydantic** para validación de esquemas.
- **FastAPI** opcional para demos en vivo.
- **pytest** para tests unitarios.

## Estructura

```text
autonomous-workflow/
├── agents/
│   ├── classifier.py      # Agente clasificador de leads
│   └── proposal.py        # Agente generador de propuestas/email
├── providers/
│   └── llm.py             # Cliente genérico del Motor de IA
├── workflow/
│   └── runner.py          # Orquestador del pipeline
├── tests/                 # Tests con pytest + mocks
├── data/
│   └── sample-lead.json   # Lead de ejemplo
├── cli.py                 # Interfaz principal
├── app.py                 # Servidor FastAPI opcional
├── config.py              # Configuración desde .env
├── requirements.txt
├── .env.example
└── README.md
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copia `.env.example` a `.env` y ajusta los valores de tu Motor de IA Local/Cloud:

```bash
cp .env.example .env
```

## Uso

### CLI — lead sintético por defecto

```bash
python cli.py
```

### CLI — lead personalizado desde archivo

```bash
python cli.py --lead data/sample-lead.json
```

### CLI — solo el email generado

```bash
python cli.py --email-only
```

### CLI — guardar resultado JSON

```bash
python cli.py --lead data/sample-lead.json --output outputs/result.json
```

### FastAPI (demo en vivo)

```bash
uvicorn app:app --reload
```

Endpoints:

- `GET  /health` — health check.
- `GET  /run` — ejecuta el flujo con el lead por defecto.
- `POST /run` — ejecuta el flujo con un lead JSON en el body.

## Salida de ejemplo

```json
{
  "workflow": "Autonomous Workflow Agent",
  "version": "0.1.0",
  "started_at": "2026-07-22T14:19:05.460863+00:00",
  "finished_at": "2026-07-22T14:19:24.998818+00:00",
  "lead": { ... },
  "classification": {
    "score": 75,
    "justification": "...",
    "risks": ["..."]
  },
  "proposal": {
    "subject": "Propuesta para ...",
    "body": "Estimado/a ..."
  }
}
```

## Tests

```bash
pytest -v
```

El test suite incluye mocks del proveedor LLM para no depender de un motor activo, y pruebas de los endpoints FastAPI.

## Documentación adicional

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — diseño técnico y flujo de datos.
- [`DECISIONS.md`](DECISIONS.md) — decisiones de diseño y trade-offs.
- [`ROADMAP.md`](ROADMAP.md) — evolución planeada.
- [`CHANGELOG.md`](CHANGELOG.md) — historial de cambios.
- [`LICENSE`](LICENSE) — licencia MIT.

## Autor

**Manuel Guerrero — AI Product Builder & Systems Integrator**

Este repositorio forma parte del AI Product Lab, un conjunto de pruebas de concepto diseñadas para demostrar capacidades reales de producto con IA.
