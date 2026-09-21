---
id: EJEMPLO-active-borrar-al-empezar
section: active
title: EJEMPLO — así se ve un ítem en curso (borrá este archivo)
updated: '2026-01-01'
---

Un fragmento por ítem. El `id` coincide con el nombre del archivo y la
`section` con la carpeta: el generador falla si no.

**Reserva —** esta es la parte que evita que dos agentes se pisen:

> Trabajando en el parser de facturas. No tocar `src/billing/parser.py`
> ni `tests/test_parser.py` mientras esta línea esté viva.

Cuando el ítem cierra, **este archivo se borra** y se escribe una entrada en
`docs/agent/log/`. No se tacha ni se marca "LISTO".
