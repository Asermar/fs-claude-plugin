# CLAUDE.md — `fs-claude-plugin` (fork público de Asermar)

Este repo es el **fork público** de `FacturaScripts/fs-claude-plugin`. Su papel es uno y sólo uno:
**ser la cabecera desde la que se abren los PR a upstream.**

La relación con las otras capas del MCP se documenta **por encima**, en `Tooling/fs-mcp/CLAUDE.md`;
aquí sólo lo que hace falta para trabajar dentro.

## Qué es, y qué NO va aquí

- **Sí**: parches que quieren llegar a upstream, cada uno con su rama y su PR.
- **No**: la capa **HTTP + OAuth**. Eso es del duplicado privado
  (`Asermar/fs-claude-plugin-private`) y son **permanentes** — nunca irán a upstream. Si un cambio
  no tiene sentido para el proyecto original, no empieza aquí.

## La topología no es la que parece: `main` es NUESTRA

- `main` = lo nuestro (lo que instala la flota). `original` = el espejo de upstream.
- El flujo va en **un solo sentido, `original` → `main`, para siempre**. **Esto no es OkoFlow**: si
  alguien cierra la integración en el espejo, ensucia el diff de todos los PR futuros.
- Se eligió así porque **el marketplace no admite rama** y Claude Code instala de la rama por
  defecto: con `main` siendo la nuestra, no hay ajuste que cambiar en cada equipo.
- **Las propuestas se cortan de `upstream/main`, nunca de `main`.** Con `main` llevando parches, lo
  intuitivo es lo equivocado: el PR saldría con cambios ajenos dentro.

## El inventario es la fuente: `.oko/divergencias.tsv`

**Lo que este fork lleva y upstream no se DECLARA ahí**, y ese fichero es la fuente — no los PR de
GitHub, no un directorio de parches, no la memoria de nadie. El propio fichero explica su porqué y
sus tres estados (`vigente`, `permanente`, `retirado`) en su cabecera; leerla antes de tocarlo.

Dos reglas que se olvidan:

- **Sólo se declara lo que no se puede deducir.** El estado del PR es observable y lo lee la
  máquina; copiarlo aquí sería un espejo que envejece.
- **La unidad es la divergencia, no el commit**: una puede ocupar varios, y por eso `commits` es una
  lista. Los merges y lo que sólo toca `.oko/` o la línea `version` están **exentos**.

Y una columna que no es de este repo pero vive aquí: **el SHA correspondiente en el duplicado
privado**. Existe porque un parche puede haberse *adaptado* al integrarlo allí, y entonces su
`patch-id` no coincide; declararlo evita que la comprobación lo dé por ausente. Sin esa columna, la
comprobación dice **«no consta si llegó»**, que no es lo mismo que «no llegó».

## Lo comprueba una máquina, no la buena voluntad

```bash
claude-dist plugins fork          # inventario × upstream × PR × el privado; sale 1 si hay hallazgos
```

Cruza el inventario con lo que hay de verdad: divergencias sin declarar, estado real de cada PR
(`gh pr view`) frente al declarado, y si lo declarado llegó al duplicado privado. Existe porque
antes había **dos listas y nadie las cruzaba**: cinco PR abiertos, un solo parche registrado, y la
herramienta informando «1 parche al día» — cierto y engañoso.

## El clon de trabajo

El del marketplace **no** sirve: lo gestiona Claude Code —lo actualiza y puede rehacerlo— y además
le falta el remoto `upstream`, sin el cual «¿se movió upstream?» siempre responde que no. Se trabaja
en un clon propio; `claude-dist plugins fork --clon <ruta>` acepta cuál.
