---
id: EJEMPLO-pending-borrar-al-empezar
section: pending
title: EJEMPLO — así se ve un pendiente (borrá este archivo)
updated: '2026-01-01'
---

Un pendiente se escribe para alguien que no estuvo en la conversación. Dos
cosas lo hacen útil:

- **La evidencia adentro, no por referencia.** "Ver PR #42" sirve hoy y es
  basura en tres semanas. El número medido, el error exacto, el comando que lo
  reproduce: eso sobrevive.
- **Qué lo desbloquea.** Un pendiente sin criterio de salida no lo toma nadie.

Ejemplo real: *"El endpoint tarda 4,2 s en p95 (medido con `ab -n 200`).
Sospecha: N+1 en `list_orders`. Desbloquea: decidir si paginamos o cacheamos."*
