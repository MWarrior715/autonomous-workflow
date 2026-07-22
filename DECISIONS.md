# Decisiones de Diseño — Autonomous Workflow Agent

## 1. Python puro en lugar de plataformas visuales

**Decisión:** Implementar todo en Python modular en vez de usar una herramienta no-code/low-code.

**Razón:** Un CTO valora más la capacidad de extender, versionar y testear la lógica de negocio con código. Python también permite orquestar agentes y pruebas automatizadas.

**Trade-off:** Mayor curva inicial de código, pero mayor flexibilidad y profesionalismo técnico.

## 2. Motor de IA enchufable vía API OpenAI-compatible

**Decisión:** Usar el cliente oficial `openai` apuntando a un endpoint configurable (`OPENAI_BASE_URL`, `OPENAI_MODEL`, `OPENAI_API_KEY`).

**Razón:** Permite cambiar entre modelos locales, servicios cloud o endpoints auto-hospedados sin tocar la lógica de agentes.

**Trade-off:** Dependemos de que el endpoint respete el esquema de chat completions; casi todos los servidores locales/cloud lo hacen.

## 3. Fallback determinista en el proveedor LLM

**Decisión:** Si la llamada al Motor de IA falla, el proveedor devuelve un resultado genérico pero útil para que la demo no se rompa.

**Razón:** En entrevistas y demos el motor puede no estar disponible. Un fallback mantiene el flujo funcional y muestra la arquitectura.

**Trade-off:** El fallback no es personalizado real; está pensado para resiliencia, no para producción.

## 4. Agentes separados por responsabilidad

**Decisión:** Dividir el flujo en `classifier` y `proposal`, cada uno con su propio prompt y normalización.

**Razón:** Facilita testear, depurar y mejorar cada etapa por separado. También deja la puerta abierta a reemplazar un agente completo sin afectar al otro.

**Trade-off:** Dos llamadas al modelo en lugar de una, pero con mejor calidad y trazabilidad.

## 5. Salida JSON estructurada + email listo

**Decisión:** Cada agente devuelve un diccionario normalizado; el runner lo ensambla en un JSON completo. El email se expone como campo separado.

**Razón:** Permite integrar con otros sistemas (CRM, emailers, dashboards) y también mostrar el email de forma legible.

## 6. FastAPI opcional

**Decisión:** Incluir `app.py` con un servidor ligero, pero mantener `cli.py` como interfaz principal.

**Razón:** CLI es suficiente para MVP y tests. FastAPI añade valor para demos remotas o integraciones HTTP sin aumentar la complejidad crítica.

## 7. Tests con mocks

**Decisión:** Proveedor real se testea solo en su lógica de fallback/parsing; los agentes usan un `FakeProvider` en tests.

**Razón:** Los tests deben ser rápidos y deterministas, sin depender de un motor externo activo.
