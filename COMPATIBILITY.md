# Compatibilidad entre Claude Code y Codex

El repositorio mantiene una única implementación para ambos hosts. Separar un `fs-codex-plugin` duplicaría skills, documentación, versiones y mantenimiento sin aportar una capacidad que no pueda resolverse desde este marketplace compartido.

| Componente | Claude Code | Codex | Implementación compartida |
|---|---|---|---|
| Skills | Nativas | Nativas | `*/skills/*/SKILL.md` |
| Agentes especializados | Agentes Markdown nativos | Perfiles leídos por las skills; delegación genérica opcional | `*/agents/*.md` |
| Inicio de sesión | `SessionStart` | `SessionStart` | `*/hooks/hooks.json` |
| Cambio de directorio | `CwdChanged` | No disponible; requiere hilo nuevo | Hook conservado para Claude Code |
| Ediciones automáticas | `Write` y `Edit` | `apply_patch` | `fs-dev/scripts/post-edit.py` |
| Servidor MCP | Raíz mediante `CLAUDE_PLUGIN_ROOT` | Raíz mediante el directorio de trabajo del plugin | Lanzador portable definido en `fs-mcp/.claude-plugin/plugin.json` |
| Módulos privados | `settings.localModulesPath` | `settings.localModulesPath` | `~/.fs-claude.json` |

## Automatización de ediciones

El hook `PostToolUse` normaliza los formatos de entrada de ambos hosts. Procesa todos los archivos de un parche en orden estable y ejecuta primero la actualización de copyright y después la ordenación de la clase PHP. De este modo no hay dos hooks escribiendo simultáneamente el mismo archivo.

En Codex, los hooks instalados deben revisarse desde `/hooks`. Cualquier cambio en `hooks.json` invalida la confianza anterior. El modificador de clase solo actúa sobre archivos PHP con namespace `FacturaScripts\\`.

## Referencias y perfiles

Las referencias viven fuera de `agents/` para que ningún host las interprete como agentes:

- `fs-dev/references/docs/`: documentación técnica.
- `fs-user/references/docs/`: documentación para usuarios.
- `fs-user/references/projects/`: catálogo de extensiones.

Los agentes de Claude Code precargan la skill `docs-expert`. En Codex, cada skill especializada lee el mismo perfil Markdown y puede aplicarlo en el hilo principal o proporcionárselo a un subagente genérico.

## Recarga durante desarrollo local

- Claude Code: ejecuta `/reload-plugins` o reinicia la sesión.
- Codex: reinstala el plugin desde el marketplace local cuando cambie su versión y abre un hilo nuevo.
- Codex hooks: revisa y autoriza de nuevo la definición desde `/hooks`.
- MCP: abre una sesión nueva o reinicia el host para reiniciar el proceso del servidor.

El nombre `~/.fs-claude.json` se conserva por retrocompatibilidad, aunque el archivo se comparte entre Claude Code y Codex.

El lanzador MCP usa `CLAUDE_PLUGIN_ROOT` cuando Claude Code la exporta y, en su ausencia, el directorio de trabajo que Codex resuelve respecto a la raíz instalada del plugin. Esto evita rutas absolutas y permite distribuir el mismo manifiesto en ambos hosts.
