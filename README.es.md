# Template: trabajo multi-dev + multi-IA

**Español** · [English](README.md)

Esqueleto para arrancar un repo donde van a trabajar **varias personas y varios
agentes de IA** (Codex, Claude Code, Cursor, Gemini) sin pisarse.

No es un framework ni trae dependencias. Son cuatro archivos de convención y un
script de ~250 líneas de stdlib.

## El problema que resuelve

Cuando el estado del proyecto vive en un markdown que todos editan, cada rama
choca contra cada rama. No es falta de disciplina: es geometría — todos escriben
en el mismo lugar del mismo archivo.

Acá el estado vive en **muchos archivos chicos, uno por ítem**, y la vista
agregada (`docs/agent/STATE.md`) se **genera** y no se versiona. Dos agentes que
trabajan cosas distintas tocan archivos distintos, y git mergea solo.

## Cómo se usa en un proyecto nuevo

**1. Copiá el esqueleto** a tu repo (sin `.git`):

```bash
git clone <url-de-este-template> /tmp/tpl
rm -rf /tmp/tpl/.git
cp -r /tmp/tpl/. mi-proyecto/
```

**2. Pedile a tu agente que lo adapte.** Este prompt alcanza:

> Este repo trae el template de trabajo multi-agente. Leé `AGENTS.md` y
> `docs/agent/`. Adaptalos a este proyecto: completá `docs/agent/state/status.yaml`,
> reemplazá los comandos de `AGENTS.md` por los reales de este stack, borrá los
> fragments de ejemplo (`EJEMPLO-*`) y la entrada de log de ejemplo, y creá los
> fragments de `pending/` que correspondan a lo que falta hacer. Después corré
> `python scripts/render_state.py` y confirmá que sale 0.

**3. Verificá** que el ciclo cierra:

```bash
python scripts/render_state.py   # debe salir 0
cat docs/agent/STATE.md
```

Listo. A partir de ahí ningún agente necesita que le pases nada: su herramienta
lee el contrato sola al abrir el repo.

## Por qué funciona con cualquier herramienta

`AGENTS.md` es el **único** contenido. El resto son punteros de una línea:

| Archivo | Lo lee |
| --- | --- |
| `AGENTS.md` | Codex y varios agentes |
| `CLAUDE.md` | Claude Code |
| `.cursor/rules` | Cursor |
| `GEMINI.md` | Gemini CLI |

Un dev que usa otra herramienta **no configura nada**: clona el repo y su
agente ya está bajo el mismo contrato. Si mañana aparece una herramienta nueva,
se agrega un puntero más — nunca una segunda copia de las reglas.

## Qué hay adentro

```
AGENTS.md                     contrato para agentes (el único contenido real)
CLAUDE.md / GEMINI.md
.cursor/rules                 punteros de una línea
.gitattributes                LF: devs Windows + CI Linux
.gitignore                    las vistas generadas NO se versionan

docs/agent/
  state/                      ESTADO VIVO — un archivo por ítem
    status.yaml               invariantes del proyecto
    active/                   en curso (y las reservas de archivos)
    pending/                  cola, cada ítem con su criterio de salida
    blocked/                  espera a una persona o a infraestructura
    conventions/              decisiones vigentes
  log/                        HISTORIA INMUTABLE — YYYY-MM-DD-slug.md
  STATE.md                    GENERADO — gitignoreado, nadie lo edita

scripts/render_state.py       el generador (stdlib, sin instalar nada)
.github/workflows/            el check que hace que la convención se cumpla
```

## Las tres decisiones que no conviene cambiar

**1. La vista se genera y no se versiona.** Si la agregás al repo, vuelven los
conflictos que todo esto existe para evitar. El CI lo verifica.

**2. El generador falla cerrado.** Ante cualquier error borra las salidas y sale
1. El contrato dice: *si no sale 0, no leas `STATE.md`*. Una vista a medias leída
como verdad es el modo de falla más caro, porque parece dato bueno.

**3. Los datos volátiles no se escriben.** SHAs, PRs y ramas se consultan al
generar. Un puntero escrito a mano envejece en horas y alguien decide con él.

## Cerrar un ítem es borrar su archivo

No se tacha, no se marca "LISTO" dejando el texto abajo. Se borra el fragmento y
se escribe una entrada en `log/`. Hay que decirlo explícito porque el reflejo de
todo agente es *agregar*: si no lo prohibís, en dos meses tenés 58 ítems
"activos" de los cuales 36 cerraron hace semanas.

## Para el equipo

Pegá esto en el README de tu proyecto:

```markdown
## Trabajo con agentes de IA
El contrato vive en AGENTS.md (tu herramienta lo lee sola).
Antes de trabajar:  python scripts/render_state.py  → leé docs/agent/STATE.md
Al cerrar: entrada en docs/agent/log/ + actualizá docs/agent/state/.
Todo entra por PR. Nadie edita STATE.md: se genera.
```

## Qué agregar después

El esqueleto cubre el estado compartido. Cuando el proyecto crezca:

- **Specs con aprobación humana** antes de implementar. Con varios agentes en
  paralelo es lo que más rinde: sin propuesta aprobada, dos agentes resuelven el
  mismo problema en dos direcciones incompatibles.
- **Revisión del propio diff** antes de pedir revisión humana.
- **Checks para cada convención que importe.** Sin verificación, una convención
  es una sugerencia.

## Licencia

MIT — usalo, copialo y adaptalo libremente, en proyectos propios o de tu empresa.

## Contribuir

Si lo usaste y algo no encajó en tu stack, un issue con el caso concreto vale
más que una sugerencia general: este esqueleto salió de modos de falla reales,
y así es como sigue creciendo.
