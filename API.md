# Autonomous Workflow — API

> Referencia de la interfaz de línea de comandos (CLI) y del servidor REST (FastAPI) del PoC **Autonomous Workflow Agent**.
> El pipeline califica un lead B2B y genera una propuesta por email de forma autónoma.

---

## CLI

Interfaz principal: `cli.py`. Ejecuta el flujo completo (clasificación + propuesta) sobre un lead y devuelve JSON estructurado o solo el email.

### Argumentos y flags

| Argumento / flag     | Tipo    | Descripción                                                                                              | Por defecto                  |
| -------------------- | ------- | -------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `--lead <path>`      | `Path`  | Ruta a un archivo JSON con el lead. Si se omite, se usa un lead sintético embebido (`DEFAULT_LEAD`).     | Lead sintético interno       |
| `--output <path>`    | `Path`  | Ruta donde escribir el resultado JSON completo del workflow. El directorio padre se crea si no existe.  | No guardar (solo stdout)     |
| `--email-only`       | flag    | Imprime únicamente el email generado (`Subject:` + body) en lugar del JSON completo.                     | `false`                      |

### Esquema del lead (JSON)

```json
{
  "name": "Andrés Ríos",
  "company": "Constructora Horizonte",
  "need": "Sistema de clasificación automática de oportunidades comerciales para su equipo de ventas.",
  "budget": "$3,000 - $5,000 USD",
  "timeline": "6 semanas",
  "source": "LinkedIn"
}
```

### Ejemplo — calificación de lead con salida JSON completa

```bash
python cli.py --lead data/sample-lead.json --output outputs/result.json
```

Salida (stdout, JSON):

```json
{
  "workflow": "Autonomous Workflow Agent",
  "version": "0.1.0",
  "started_at": "2026-07-22T14:19:05.460863+00:00",
  "finished_at": "2026-07-22T14:19:24.998818+00:00",
  "lead": {
    "name": "Andrés Ríos",
    "company": "Constructora Horizonte",
    "need": "Sistema de clasificación automática de oportunidades comerciales para su equipo de ventas.",
    "budget": "$3,000 - $5,000 USD",
    "timeline": "6 semanas",
    "source": "LinkedIn"
  },
  "classification": {
    "score": 75,
    "justification": "Lead con presupuesto adecuado y necesidad clara, pero con un timeline ajustado que requiere validación temprana.",
    "risks": ["Timeline de 6 semanas puede comprimir el delivery", "Dependencia de un único stakeholder comercial"]
  },
  "proposal": {
    "subject": "Propuesta para Constructora Horizonte",
    "body": "Estimado/a Andrés ..."
  }
}
```

### Ejemplo — solo el email generado

```bash
python cli.py --lead data/sample-lead.json --email-only
```

Salida (stdout, texto plano):

```text
Subject: Propuesta para Constructora Horizonte

Estimado/a Andrés ...
```

---

## REST (FastAPI)

Servidor opcional para demos en vivo, definido en `app.py`.

### Levantar el servidor

```bash
uvicorn app:app --reload
```

Por defecto el servidor escucha en `http://127.0.0.1:8000`. La documentación interactiva está disponible en `/docs` (Swagger UI) y `/redoc`.

### Endpoints

| Método | Ruta      | Descripción                                              | Body                                        |
| ------ | --------- | -------------------------------------------------------- | ------------------------------------------- |
| `GET`  | `/health` | Health check del servicio.                               | —                                           |
| `GET`  | `/run`    | Ejecuta el workflow con el lead sintético por defecto.   | —                                           |
| `POST` | `/run`    | Ejecuta el workflow con un lead JSON provisto en el body. | `Lead` (JSON, opcional) — ver esquema abajo |

### Esquema `Lead` (body de `POST /run`)

Modelo Pydantic aceptado por el endpoint:

| Campo     | Tipo   | Requerido | Descripción                          | Por defecto |
| --------- | ------ | --------- | ------------------------------------ | ----------- |
| `name`    | string | sí        | Nombre del contacto.                 | —           |
| `company` | string | sí        | Nombre de la empresa.                | —           |
| `need`    | string | sí        | Necesidad o problema de negocio.     | —           |
| `budget`  | string | sí        | Rango de presupuesto.                | —           |
| `timeline`| string | no        | Timeline esperado.                   | `""`        |
| `source`  | string | no        | Origen del lead.                     | `"api"`     |

Si se envía el body vacío, el endpoint ejecuta el workflow con el lead sintético por defecto (mismo comportamiento que `GET /run`).

### `GET /health`

```bash
curl http://127.0.0.1:8000/health
```

Respuesta:

```json
{
  "status": "ok",
  "service": "Autonomous Workflow Agent"
}
```

### `GET /run`

```bash
curl http://127.0.0.1:8000/run
```

Respuesta (representativa):

```json
{
  "workflow": "Autonomous Workflow Agent",
  "version": "0.1.0",
  "started_at": "2026-07-22T14:19:05.460863+00:00",
  "finished_at": "2026-07-22T14:19:24.998818+00:00",
  "lead": {
    "name": "Carolina Mendoza",
    "company": "LogiTech Andina",
    "need": "Automatizar el seguimiento de leads entrantes y reducir el tiempo de respuesta comercial.",
    "budget": "$4,000 - $6,000 USD",
    "timeline": "4-6 semanas",
    "source": "formulario web"
  },
  "classification": {
    "score": 78,
    "justification": "Lead con necesidad alineada a la propuesta y presupuesto dentro de rango; el timeline es viable.",
    "risks": ["Dependencia de adopción por parte del equipo comercial"]
  },
  "proposal": {
    "subject": "Propuesta para LogiTech Andina",
    "body": "Estimado/a Carolina ..."
  }
}
```

### `POST /run`

```bash
curl -X POST http://127.0.0.1:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Andrés Ríos",
    "company": "Constructora Horizonte",
    "need": "Sistema de clasificación automática de oportunidades comerciales para su equipo de ventas.",
    "budget": "$3,000 - $5,000 USD",
    "timeline": "6 semanas",
    "source": "LinkedIn"
  }'
```

Respuesta (representativa, mismo esquema que `GET /run`):

```json
{
  "workflow": "Autonomous Workflow Agent",
  "version": "0.1.0",
  "started_at": "2026-07-22T14:20:01.112233+00:00",
  "finished_at": "2026-07-22T14:20:18.998818+00:00",
  "lead": {
    "name": "Andrés Ríos",
    "company": "Constructora Horizonte",
    "need": "Sistema de clasificación automática de oportunidades comerciales para su equipo de ventas.",
    "budget": "$3,000 - $5,000 USD",
    "timeline": "6 semanas",
    "source": "LinkedIn"
  },
  "classification": {
    "score": 75,
    "justification": "Lead con presupuesto adecuado y necesidad clara, pero con un timeline ajustado que requiere validación temprana.",
    "risks": ["Timeline de 6 semanas puede comprimir el delivery"]
  },
  "proposal": {
    "subject": "Propuesta para Constructora Horizonte",
    "body": "Estimado/a Andrés ..."
  }
}
```

---

## Flujo de agentes

El orquestador `workflow/runner.py` ejecuta el pipeline autónomo sobre un único lead:

1. **Ingesta del lead** — el lead (dict JSON) se carga desde archivo, desde el body de la petición REST, o se usa el lead sintético por defecto.
2. **Agente clasificador** (`agents/classifier.py`) — cualifica el lead devolviendo un `score` entero (1–100), una `justification` en español y una lista de `risks`. La salida se normaliza para garantizar tipos y rangos.
3. **Agente generador de propuesta** (`agents/proposal.py`) — recibe el lead y el resultado de la clasificación, y genera un email personalizado en español con `subject` y `body`. La salida se normaliza para garantizar campos no vacíos.
4. **Resultado estructurado** — el runner ensambla un JSON con metadatos (`workflow`, `version`, `started_at`, `finished_at`), el `lead`, la `classification` y la `proposal`, devuelto tanto por la CLI como por los endpoints REST.

Ambos agentes consumen un cliente genérico del Motor de IA Local/Cloud vía API OpenAI-compatible (`providers/llm.py`), configurable mediante variables de entorno en `.env`.