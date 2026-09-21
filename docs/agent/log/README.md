# Historial de sesiones

Una entrada por sesión o PR: `YYYY-MM-DD-<slug>.md`, con `summary:` en el
frontmatter. **Inmutables**: si algo cambió, entrada nueva — nunca se edita una
vieja. Eso es lo que hace que varias ramas puedan escribir acá sin chocar.

`INDEX.md` se **genera** (`python scripts/render_state.py`) y no se versiona.
