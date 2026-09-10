---
name: api-designer
description: Diseña o modifica endpoints REST de FacturaScripts, tanto recursos CRUD como rutas personalizadas, autenticación, filtros, paginación e integraciones entre instancias.
---

# Diseño de API REST

Usa como instrucciones de especialidad el perfil [`../../agents/api-designer.md`](../../agents/api-designer.md) y léelo completo antes de actuar.

## Ejecución portable

- En Claude Code, delega al agente nativo `api-designer` cuando esté disponible.
- En Codex, aplica el perfil directamente. Si hay delegación genérica disponible y aporta valor, entrega al subagente una tarea acotada junto con el perfil y el contexto relevante.
- Si no puedes delegar, realiza tú mismo el trabajo siguiendo el perfil.
- Consulta `fs-dev:docs-expert` antes de afirmar detalles propios del framework y contrasta la implementación con el código local.

Incluye validación, autenticación, errores y pruebas proporcionales al cambio. No modifiques código ni configuración fuera de lo pedido por el usuario.
