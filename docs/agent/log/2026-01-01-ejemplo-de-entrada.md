---
date: 2026-01-01
summary: Ejemplo de entrada de log — mostrá qué cambió, qué se verificó y qué quedó abierto. Borrá este archivo al empezar tu proyecto.
---

# 2026-01-01 — Ejemplo de entrada

Las entradas del log son **inmutables**: si algo cambió, entrada nueva. Por eso
nunca generan conflictos, aunque escriban varias ramas a la vez.

El `summary:` del frontmatter es lo que aparece en el índice generado, así que
tiene que decir algo: qué cambió y por qué importa, no "avances varios".

## Qué escribir

Una entrada le habla a alguien que no estuvo. Lo que rinde:

- **El defecto o la necesidad**, con el dato que lo demuestra.
- **La decisión y por qué**, incluidas las alternativas descartadas.
- **La verificación**: el comando y su salida real, no "anda bien".
- **Lo que quedó abierto**, con su criterio de salida.

## Qué no escribir

Lo que `git` ya sabe responder: la lista de archivos tocados, el diff, quién
commiteó. Eso se consulta; el log es para lo que no está en el código.
