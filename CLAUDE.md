@AGENTS.md

---

# Este repo es el fork público de Asermar

Este repo es el **fork público** de `FacturaScripts/fs-ai-plugin` (antes `fs-claude-plugin`; el nombre viejo redirige). Su papel es uno y sólo uno:
**ser la cabecera desde la que se abren los PR a upstream.**

La relación con las otras capas del MCP se documenta **por encima**, en `Tooling/fs-mcp/CLAUDE.md`;
aquí sólo lo que hace falta para trabajar dentro.

## Qué es, y qué NO va aquí

- **Sí**: parches que quieren llegar a upstream, cada uno con su rama y su PR.
- **No**: la capa **HTTP + OAuth**. Eso es del duplicado privado
  (`Asermar/fs-claude-plugin-private`) y son **permanentes** — nunca irán a upstream. Si un cambio
  no tiene sentido para el proyecto original, no empieza aquí.

## La norma: seguir lo publicado

Dicha por Alexis el 7-oct-2026.

- **Este fork sigue a upstream.** Cada versión que upstream publica se integra aquí y en el
  duplicado privado **sin necesidad de preguntar**.
- **Lo que upstream no tiene se le ofrece por PR.**
- **Aquí solo divergen dos cosas**, y las dos constan en `.oko/divergencias.tsv`:
  - nuestros PR **sin aprobar**, de forma temporal (`vigente`);
  - los **rechazados**, de forma fija mientras a nuestro juicio sigan teniendo motivo (`permanente`).

  Lo que upstream acepta pasa a `retirado`. Aparte queda lo propio del fork: `.oko/`, este
  `CLAUDE.md` y la línea `version` de cada `plugin.json`.
- **Lo que la norma NO cubre: desplegar el servidor MCP con un pin nuevo.** Es producción de un
  cliente y se autoriza en cada despliegue.

Cómo se integra cada versión, en este orden:

1. `git fetch upstream` y avance rápido de `original` a `upstream/main`
   (`git push origin upstream/main:refs/heads/original`). Es solo un avance: `original` no lleva
   nada propio, así que si no fuera un fast-forward, algo va mal.
2. Merge `--no-ff` de `original` en `main`, por una rama `feature/*`. El conflicto habitual es la
   línea `version` de algún `plugin.json`: se queda la nuestra y se sube si el contenido de ese
   plugin cambia, como dice la cabecera de `.oko/base.tsv`, que además recoge la base nueva.
3. Comprobar que `git diff upstream/main main` solo toca lo que la norma permite, y pasar
   `claude-dist plugins fork --clon <la rama>`.
4. Llevar ese `main` al duplicado privado, a la rama de su pin, borrando `.oko/`, y mover el pin en
   `develop` de `Asermar/fs-remote-mcp`. Ahí se para: lo siguiente ya es desplegar.

## Cómo se escribe cada PR a upstream

El modelo es el PR que el core oficial aceptó a la primera y cuyo autor agradeció por lo bien
documentado (NeoRazorX/facturascripts#2051, 16-oct-2026). Lo que funcionó allí vale aquí:

- **Rama desde `upstream/main`, un único cambio coherente, y un PR que no dependa de otro abierto.**
  Si dos arreglos tocan el mismo fichero de tests, se reparten para que cada PR funda solo (así se
  separó el #18 del #17). Un fallo hermano en el mismo sitio va en el mismo PR; otro problema, en otro.
- **La reproducción con el propio repo, sin datos de nadie.** El fallo puede salir de un plugin o una
  instalación nuestra, pero el PR lo cuenta con un caso que el revisor puede ejecutar en su máquina.
  Ni clientes, ni plugins propios, ni rutas nuestras: se comprueba con un grep antes de abrir.
- **Tests en `fs-dev/tests/` que fallan sin el cambio, y el PR lo dice así.** Uno por cada rama del
  arreglo, y cada uno probado con su mutación: se quita esa parte del arreglo y cae sólo su test.
- **Las pruebas, con lo NO ejecutado marcado.** La lista de «Validación mínima» de arriba, diciendo
  qué se ejecutó y qué no.
- **Las decisiones discutibles, explicadas antes de que las pregunten**, y una línea para quien
  dependa del comportamiento que cambia.
- **Antes de abrirlo:** supervisor de codificación, revisión de seguridad del lenguaje, y
  `git merge-tree` contra el `upstream/main` del día.
- **Al fusionarse**, upstream puede retocarlo: se compara lo fusionado con lo nuestro antes de pasar
  la fila a `retirado`.

La versión larga, con el caso entero, está en el árbol de conocimiento de la casa:
`arbol/FS/Core/un-pr-al-core-oficial.md`.

## Cada PR propio entra en `main` en cuanto se abre

**Abrir un PR a upstream y llevar su rama a `main` son UN solo paso, no dos.** La flota instala
`main`, así que un PR que sólo existe en GitHub no lo usa nadie mientras upstream lo estudia, que
puede ser semanas. Y no es una opción: es lo que significa `vigente`.

En cuanto el PR está abierto, por una rama `feature/integra-*`:

1. Merge `--no-ff` de la rama del PR en `main`. La rama sale de `upstream/main` y `main` ya contiene
   esa base, así que lo esperable es que funda limpio.
2. Su fila en `.oko/divergencias.tsv` con estado `vigente`, y `pendiente` en la columna del privado
   hasta que se lleve allí.
3. Subir la línea `version` del `plugin.json` de cada plugin cuyo contenido cambie, y recogerla en
   `.oko/base.tsv`: sin la subida, los equipos no ven actualización.
4. Los tests del plugin y `claude-dist plugins fork --clon <la rama>`, y después merge en `main`.

Y después, **siempre, al privado**, con el paso 4 de arriba: rama del pin, borrando `.oko/`, y el pin
movido en `develop` de `fs-remote-mcp`. No es una decisión aparte. Lo que sí se autoriza cada vez es
desplegar ese pin.

**Qué contiene cada capa** (Alexis, 15-oct-2026):

- **el fork** = upstream + nuestros PR pendientes + los rechazados que sigan siendo válidos;
- **el privado** = el fork entero + lo nuestro privado: HTTP, OAuth y las listas de tools.

> Por qué está escrito (15-oct-2026): el PR #16 pasó una semana abierto **sin estar en `main`**,
> mientras el #17, abierto después, sí entró. El plan del #16 sólo preveía llevarlo al privado y
> esta sección no existía: el procedimiento de arriba cubre las versiones de upstream y no decía
> nada de los PR propios.

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
  lista. La cobertura se mide **por fichero**: cada fichero que difiere de la base del último merge
  con upstream necesita declarados todos los commits que lo traen, incluido el merge cuya resolución
  difiere de la automática. Sólo están **exentos** `.oko/`, este `CLAUDE.md` y la línea `version` de
  un `plugin.json` (también el merge cuya resolución de ese fichero sólo toca esa línea).

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

## Frontera

**Destino:** que la documentación empaquetada del plugin sea alcanzable en los dos hosts **desde el
código de upstream**, sin que este fork tenga que volver a llevar un parche de rutas.

**El hallazgo que la abre** (medido el 18-sep-2026, al integrar `1a25075`): las skills que upstream
reescribió declaran que `../../references/docs/` «se resuelve respecto a este `SKILL.md`», y la
documentación de Claude Code dice lo contrario — *«Claude Code runs each command in the session
shell's current working directory (…) Use `${CLAUDE_SKILL_DIR}` or `${CLAUDE_PROJECT_DIR}` in paths
that must resolve the same way every time»*, y su tabla de sustituciones lista `${CLAUDE_PLUGIN_ROOT}`
como disponible dentro del cuerpo de un `SKILL.md`
([skills.md](https://code.claude.com/docs/en/skills.md)). En una sesión abierta en el proyecto del
usuario esa ruta apunta **dos niveles por encima de su proyecto**: es el mismo defecto que
`docs-ruta-plugin-root` arreglaba, reaparecido en la capa que reescribieron.

### Pendiente de decidir

- ¿Sustituye **Codex** `${CLAUDE_PLUGIN_ROOT}` en el cuerpo de un `SKILL.md`? — decide si hay arreglo
  posible o hay que buscar otra vía. **NO VERIFICADO**: no hay Codex en esta casa. Upstream afirma
  que «ambos hosts lo proporcionan por compatibilidad», pero lo dice de los **hooks**. Lo pregunta
  Alexis al mantenedor.
- ¿Entra en `.oko/divergencias.tsv`, y con qué estado, cuando exista el PR a upstream? — hoy no
  procede: sus tres estados describen divergencias que **llevamos**, y de esto no llevamos nada.

### Fuera de alcance

- **Parchear las skills aquí** para que usen `${CLAUDE_PLUGIN_ROOT}` — revertiría en silencio una
  decisión que upstream tomó a propósito por Codex («Resuelve los recursos relativos respecto al
  directorio de la skill», su `CLAUDE.md`). Si hay arreglo, sale por PR a upstream, no por divergencia.
