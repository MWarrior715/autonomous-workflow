# Arquitectura — Autonomous Workflow Agent

## Visión general

Sistema de automatización B2B compuesto por dos agentes especializados orquestados por un runner central. Cada agente consume un único proveedor de Motor de IA enchufable, lo que permite cambiar de backend (local, cloud, auto-hospedado) sin modificar la lógica de negocio.

```text
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Input     │────▶│  Classifier  │────▶│  Proposal   │────▶│   Output    │
│  Lead JSON  │     │   Agent      │     │   Agent     │     │ JSON + Email│
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
                            │                     │
                            └──────────┬──────────┘
                                       ▼
                            ┌──────────────────────┐
                            │   LLM Provider       │
                            │ OpenAI-compatible    │
                            │ Motor de IA Local/Cloud│
                            └──────────────────────┘
```

## Componentes

### 1. `config.py`

Carga variables de entorno desde `.env`. Expone `settings` como objeto plano para evitar dependencias circulares.

### 2. `providers/llm.py`

Wrapper sobre `openai.ChatCompletion`:

- Recibe system/user prompts.
- Solicita salida JSON cuando `json_mode=True`.
- Parsea la respuesta y tolera texto libre con extracción best-effort de JSON.
- **Fallback determinista**: si el motor no está disponible, devuelve un resultado coherente para seguir haciendo demos.

### 3. `agents/classifier.py`

Responsabilidades:

- Evaluar fit comercial del lead.
- Asignar score 1-100.
- Justificar el score en español.
- Listar riesgos detectados.

Prompt estructurado con salida JSON forzada.

### 4. `agents/proposal.py`

Responsabilidades:

- Leer el lead y su clasificación.
- Generar `subject` y `body` de un email de propuesta profesional en español.
- Incluir CTA y referencias concretas al presupuesto/timeline del lead.

### 5. `workflow/runner.py`

Orquestador:

- Recibe lead opcional.
- Ejecuta classifier → proposal secuencialmente.
- Inyecta timestamps estructurados.
- Devuelve un único objeto JSON con toda la trazabilidad del flujo.

### 6. `cli.py`

Interfaz principal. Soporta:

- Lead por defecto.
- `--lead <archivo.json>`.
- `--output <archivo.json>`.
- `--email-only`.

### 7. `app.py`

FastAPI opcional para demos HTTP.

## Flujo de datos

1. Usuario invoca `cli.py` o endpoint `/run`.
2. `runner.run()` recibe el lead.
3. `classify()` envía lead al Motor de IA y normaliza la respuesta.
4. `generate_proposal()` envía lead + clasificación al Motor de IA y normaliza.
5. `runner` ensambla resultado final con metadatos.
6. CLI imprime o guarda el JSON; email puede mostrarse por separado.

## Seguridad y configuración

- La URL, key y modelo del Motor de IA viven en `.env` (gitignored).
- `.env.example` sirve como plantilla genérica sin credenciales reales.
- Nunca se versiona configuración privada.

## Escalabilidad futura

- Agregar cola de leads (Redis / RabbitMQ).
- Persistir resultados en base de datos.
- Historial de interacciones por lead.
- Nuevos agentes: scheduling, follow-up, CRM sync.
