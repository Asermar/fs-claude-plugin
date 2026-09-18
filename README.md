# Plugins de FacturaScripts para Claude Code y Codex

Este repositorio distribuye tres plugins independientes para trabajar con [FacturaScripts](https://facturascripts.com) desde Claude Code o Codex.

| Plugin | Para quién | Descripción |
|---|---|---|
| **fs-dev** | Desarrolladores | Skills portables, perfiles especializados, documentación técnica y automatizaciones |
| **fs-user** | Usuarios del ERP | Análisis de datos, informes y ayuda documentada sobre el uso del ERP |
| **fs-mcp** | Cualquier usuario | Servidor MCP con conexiones múltiples y módulos privados locales |

## Instalación en Claude Code

Añade el marketplace desde Claude Desktop/Cowork o desde Claude Code:

```text
/plugin add marketplace FacturaScripts/fs-claude-plugin
```

También puedes clonar el repositorio e instalarlo desde una ruta local:

```text
/plugin install /ruta/local/fs-claude-plugin
```

Activa después `fs-dev`, `fs-user` y/o `fs-mcp` desde el gestor de plugins. Tras actualizar una instalación local, usa `/reload-plugins` o abre una sesión nueva.

## Instalación local en Codex

Clona el repositorio y registra su marketplace local:

```bash
git clone https://github.com/FacturaScripts/fs-claude-plugin
codex plugin marketplace add /ruta/local/fs-claude-plugin
codex plugin add fs-dev@fs-claude-plugin
codex plugin add fs-user@fs-claude-plugin
codex plugin add fs-mcp@fs-claude-plugin
```

Después de instalar o actualizar, abre un hilo nuevo para que Codex cargue las skills y los servidores MCP actuales. Los hooks se revisan y autorizan desde `/hooks`; cuando cambia su definición, Codex solicita una nueva revisión.

Codex utiliza directamente las skills. Los archivos Markdown de `agents/` son agentes nativos de Claude Code; las skills de `fs-dev` cargan esos mismos archivos como perfiles de especialidad para mantener un único contenido compartido en ambos hosts.

La matriz de capacidades, diferencias de hooks y flujo de recarga está documentada en [COMPATIBILITY.md](COMPATIBILITY.md).

## Plugins incluidos

- [fs-dev — Desarrollo](fs-dev/README.md)
- [fs-user — Uso del ERP](fs-user/README.md)
- [fs-mcp — Servidor MCP](fs-mcp/README.md)

## Configuración compartida

Los tres plugins usan `~/.fs-claude.json`. El nombre se conserva por compatibilidad e incluye conexiones, opciones de automatización y `settings.localModulesPath`. Los módulos privados permanecen fuera de este repositorio y se cargan dinámicamente desde esa ruta.

## Requisitos

- Claude Code o Codex con soporte de plugins
- FacturaScripts con la API REST habilitada para `fs-mcp`
- Node.js 18 o superior para ejecutar el servidor MCP
- Python 3 para las automatizaciones de `fs-dev`

## Licencia

MIT — [FacturaScripts](https://facturascripts.com)
