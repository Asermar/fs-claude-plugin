---
name: testing-expert
description: Revisa, crea o ejecuta tests de FacturaScripts con PHPUnit y herramientas como PHPStan o CS-Check; úsala también para analizar cobertura y fallos de pruebas.
---

# Testing y calidad

Usa como instrucciones de especialidad el perfil [`../../agents/testing-expert.md`](../../agents/testing-expert.md) y léelo completo antes de actuar.

## Ejecución portable

- En Claude Code, delega al agente nativo `testing-expert` cuando esté disponible.
- En Codex, aplica el perfil directamente o pásalo a un subagente genérico para una revisión acotada cuando resulte útil.
- Si no puedes delegar, realiza tú mismo el trabajo siguiendo el perfil.
- Consulta `fs-dev:docs-expert`, los tests existentes y la configuración real del proyecto antes de ejecutar herramientas.

Prueba comportamiento observable y casos límite; informa por separado fallos preexistentes y regresiones del cambio.
