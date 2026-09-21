# AGENTS.md — contrato para agentes de IA en este repo

Este archivo es el contrato **único** para cualquier agente (Codex, Claude Code,
Cursor, Gemini u otro). `CLAUDE.md`, `.cursor/rules` y `GEMINI.md` sólo apuntan
acá — no dupliques contenido en ellos.

> Adaptá este archivo a tu proyecto. Lo que está entre `<...>` hay que
> reemplazarlo. Lo que no aplique, borralo: un contrato con reglas muertas
> enseña que las reglas son decorativas.

## Al iniciar una sesión

```bash
python scripts/render_state.py
```

- **Sale 0** → leé `docs/agent/STATE.md`. Ese es el estado del proyecto.
- **Sale distinto de 0** → **no leas `STATE.md`**: está borrado o viejo. Arreglá
  los fragments que el error nombra, o avisá. Nunca trabajes sobre un estado
  que no se pudo generar.

`STATE.md` y `log/INDEX.md` son **generados y no se versionan**. No los edites:
tu cambio se pierde en el próximo render y no lo ve nadie.

## Reglas duras

Numeradas para poder citarlas en una revisión ("esto viola la regla 4").

1. **Todo entra por PR.** Ningún agente commitea directo a la rama principal,
   tampoco documentación. Sin excepciones por "es un cambio chico".
2. **Nada de trabajo sin registrar.** Antes de tocar código, creá un fragmento
   en `docs/agent/state/active/` que diga qué vas a hacer y **qué archivos vas a
   tocar**. Antes de empezar, leé los demás fragments de `active/` para no
   pisar a otra persona o agente.
3. **Cerrar un ítem = borrar su archivo** de `state/`, más una entrada nueva en
   `docs/agent/log/`. No se tacha ni se marca "CERRADO" dejando el texto.
4. **Verificá antes de afirmar.** Antes de decir "listo", "arreglado" o "pasa",
   corré el comando que lo demuestra y mirá la salida real. Si no lo corriste,
   no lo digas.
5. **Tests con cada cambio de comportamiento.** El test se escribe primero y se
   ve fallar; un test que nunca falló no prueba nada.
6. **No amplíes el alcance.** No "mejores" código adyacente, no agregues
   dependencias sin justificarlas, no refactorices lo que no se rompió.
7. **No saltees los hooks** (`--no-verify`) ni fuerces push. Si un hook falla,
   arreglá la causa.
8. **Los datos volátiles no se escriben.** SHAs, números de PR, listas de ramas:
   se consultan con `git` / `gh` en el momento. Si lo escribís en un `.md`,
   envejece y alguien decide con un dato falso.
9. **Nada de datos de prueba en producción sin limpiar.** Si tenés que crearlos,
   los borrás al terminar y verificás que quedaron borrados.
10. **Ante la duda, preguntá.** Una pregunta cuesta minutos; una suposición
    incorrecta descubierta después del merge, días.

## Al cerrar una sesión o un PR

En el **mismo PR** del cambio, nunca en un commit aparte:

1. Entrada nueva en `docs/agent/log/YYYY-MM-DD-<slug>.md`, con `summary:` en el
   frontmatter (una oración: qué cambió y por qué importa).
2. Actualizá `docs/agent/state/`: **borrá** el fragmento del ítem que cerraste,
   creá los de lo que quedó pendiente. Un pendiente sin criterio de salida no lo
   toma nadie: decí qué lo desbloquea.
3. Volvé a correr `python scripts/render_state.py` y confirmá que sale 0.

**No dejes nada "para después del merge".** Todo paso diferido deja de hacerse:
o viaja en este PR, o no existe. Si de verdad no puede hacerse ahora, va como
fragmento en `pending/` con su criterio de salida — nunca como un comentario en
el PR.

## Comandos

<!-- Reemplazá por los de tu stack. Deben ser los que corre CI, uno por línea. -->

```bash
<comando de setup>          # instalar dependencias
<comando de tests>          # suite
<comando de lint>
<comando de tipos>
<comando de build>
```

## Flujo de un cambio

```
necesidad → spec/propuesta → [GATE 1: una persona aprueba]
          → implementación (tests primero)
          → revisión del propio diff
          → PR → [GATE 2: una persona revisa] → merge
          → [GATE 3: una persona autoriza el deploy]
```

Los gates los cruza una persona, nunca un agente. El **Gate 1 es el que más
rinde con varios agentes en paralelo**: sin una propuesta aprobada, dos agentes
resuelven el mismo problema en dos direcciones incompatibles.

Antes de pedir el Gate 2, revisá tu propio diff con ojo crítico y listá los
hallazgos en el PR bajo `## Revisión previa`. Verificá cada hallazgo
**ejecutándolo**, no leyéndolo.

## Trabajo en paralelo

- Un agente, una rama, un worktree. **Un worktree es de alguien**: no lo borres
  sin confirmar que su rama está pusheada.
- Si un subagente tuyo tocó archivos compartidos, **verificá el diff vos mismo**
  (`git diff --stat`). Un reporte de "quedó limpio" no es evidencia.
- Si la rama principal avanzó, integrala (`git fetch && git merge origin/<main>`).
  Eso actualiza tu rama; **no** te autoriza a pushear ni a mergear.

## Idioma

- Código, comentarios, commits, PRs: **inglés**.
- Documentación de `docs/agent/` y conversación: **español**.

## Estilo de commits

Conventional Commits con scope: `feat(api): add rate limiting`.
Tipos: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `ci`, `perf`.
