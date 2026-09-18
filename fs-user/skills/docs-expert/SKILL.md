---
name: docs-expert
description: "Consulta la documentación incluida para explicar cómo usar FacturaScripts: operaciones, menús, clientes, ventas, compras, inventario, contabilidad y flujos de documentos. Si el core no cubre la necesidad, busca extensiones relevantes en el catálogo incluido."
---

# Documentación de usuario de FacturaScripts

Responde a partir de la documentación de usuario incluida en [`../../references/docs/`](../../references/docs/). Si la funcionalidad no forma parte del core, consulta el catálogo de plugins en [`../../references/projects/`](../../references/projects/). Ambas rutas se resuelven respecto a este `SKILL.md`.

## Flujo

1. Busca términos de la pregunta en `../../references/docs/` mediante `rg` o la herramienta disponible.
2. Lee completos los documentos relevantes y explica los pasos con los nombres de menús y campos que aparezcan en ellos.
3. Si el core no cubre la funcionalidad, busca en `../../references/projects/` y menciona como máximo tres extensiones realmente pertinentes.
4. Cita los archivos consultados mediante enlaces o rutas precisas.
5. Si no hay documentación ni extensión aplicable, dilo sin inventar el procedimiento.

No muestres un plugin como parte del core ni atribuyas capacidades que su ficha no documente.

## Compatibilidad de agentes

En Claude Code esta skill puede estar precargada en el agente `docs-expert`. En Codex aplica estas instrucciones directamente; no depende de que exista el agente Markdown de Claude.
