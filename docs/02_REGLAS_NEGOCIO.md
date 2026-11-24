# 02 — Reglas de negocio (RN)

> Cada regla tiene un ID para citarla en el código, en los tests y en otras IAs.
> Estado: ✅ vigente · 🟡 a implementar · ⚠️ a confirmar.

## A. Alcance y fuentes

**RN-01 · Carrera y examen.** La app es para **Medicina Humana** (SERUMS/ENCAPS, Perú). No mezclar otras carreras en el mismo banco.

**RN-02 · Vigencia de fuentes.** Solo preguntas de exámenes **≥ 2024** (antes cambió el examen). Oficiales = con clave MINSA. Generadas = desde normas MINSA vigentes, marcadas `meta.origen = "generada"`.

**RN-03 · Anti-duplicado.** Toda pregunta se indexa por `sha1(norm(stem))`. Si la huella ya existe, **no se agrega** (evita solape entre exámenes y entre oficiales/generadas).

**RN-04 · Integridad.** Cada pregunta: 4 opciones con prefijo `"X. "`, `ans.letra` válida, `ans.texto` correcto. Se valida con `registro.py check`.

## B. Modos de uso

**RN-05 · Dos modos.** La app tiene dos modos de estudio:
- **Modo Simulacro** = comportamiento actual: recorrer el banco (filtrable por examen), marcar y corregir al instante.
- **Modo Flash** = miniexamen: el alumno elige cuántas preguntas quiere y (opcional) de qué exámenes; se responde una por una contra reloj.

**RN-06 · Selección en Modo Flash.** El alumno define:
1. **Cantidad N** de preguntas (obligatorio). Sugeridos: 10 / 20 / 25 / 50 / personalizado.
2. **Exámenes** (opcional, multiselección). Si no elige ninguno → se usan **todos**.
Las N preguntas se sortean (aleatorio) del pool resultante. Si N > pool disponible → usar el máximo disponible y avisar.

**RN-07 · Orden y flujo Flash.** Una pregunta por pantalla. El alumno marca una opción → se evalúa → botón **"Siguiente"** → siguiente pregunta. Al responder la última → resultados.

## C. Tiempo

**RN-08 · Tiempo por pregunta = 72 s (1:12).** ✅ **Confirmado por el usuario el 2026-11-24.**
- **Tiempo total = N × 72 s.**
- **Conteo regresivo** visible (mm:ss) y fijo/sticky en pantalla.
- Al llegar a **00:00** → el examen **termina de inmediato** y pasa a resultados.
- Las preguntas **sin responder** al agotarse el tiempo se cuentan como **incorrectas**.
- El tiempo corre desde que se inicia el examen, no por pregunta.

**RN-09 · Cálculo del puntaje.** `puntaje = correctas / N`. Mostrar como `X/N` y `%`. Sin responder = incorrecta. No hay puntaje negativo.

## D. Feedback

**RN-10 · Feedback en Modo Simulacro.** Al marcar: se muestra **¡Correcto!/Incorrecto**, se revela la respuesta correcta y aparece el botón **"Adentrarse con IA"**. Marca reversible (se puede desmarcar). Persiste en `localStorage`.

**RN-11 · Feedback en Modo Flash.** Durante el examen: al marcar se muestra **solo correcto/incorrecto** (sin revelar la respuesta correcta, sin IA) y se habilita **"Siguiente"**. *No se muestra la clave ni la explicación hasta el final.*

**RN-12 · Resultados Flash.** Al terminar (por tiempo o por completar):
- Mensaje de cierre + puntaje (X/N, %).
- **Todas las preguntas**, separadas en **Correctas** e **Incorrectas**.
- Cada pregunta mostrada con: enunciado, opciones, **tu respuesta**, **respuesta correcta** y botón **"Adentrarse con IA"** (versión completa, como Simulacro).
- Las no respondidas aparecen en "Incorrectas" como "Sin responder".

## E. Enlace a IA

**RN-13 · Texto del deep-link a IA.** El mensaje a ChatGPT debe incluir:
- Contexto ("Me estoy preparando para mi examen de ENCAPS en Perú").
- El enunciado.
- Si el alumno marcó una opción incorrecta: **"Yo marqué la opción B: <texto de B>. Pero la respuesta correcta es A: <texto de A>."**
- Si marcó la correcta o no marcó: "La respuesta correcta es A: <texto de A>."
> ✅ **Corregido 2026-11-24:** `deepUrl()` ahora incluye el texto de la opción marcada (helper `optText`).

**RN-14 · URL de IA.** `https://chatgpt.com/?q=<mensaje>` (URL-encoded), abierto en pestaña nueva.

## F. Guardar resultado (Flash)

**RN-15 · Imagen del resultado.** Botón **flotante superior** "Guardar resultado" en la pantalla de resultados. Genera y **descarga una imagen (PNG)** con:
- Puntaje (X/N y %).
- Exámenes incluidos (o "Todos").
- Cantidad de preguntas.
- Fecha/hora (opcional, recomendado).
> Solo eso: no se guarda historial ni datos personales. La imagen se genera en el navegador (Canvas → `toDataURL('image/png')` → descarga).

## G. Persistencia y plataforma

**RN-16 · Persistencia Simulacro.** Marcas en `localStorage` (`serums_marks`); sobreviven recarga/cierre. "Desmarcar" borra solo el examen activo (o todas si está en "Todas").

**RN-17 · Persistencia Flash.** Estado **efímero**: al recargar se pierde el examen en curso. (Sin historial por ahora.)

**RN-18 · Sin login / sin backend.** Todo local. Único tráfico externo: el enlace a ChatGPT.

**RN-19 · Móvil y rápido.** Diseño mobile-first (~360–480 px), carga instantánea, sin dependencias externas que rompan el uso con doble clic.

**RN-20 · Idioma y tono.** Español, tuteo neutro peruano. Sin voseo en textos de la app.

## Resumen de cambios a implementar (para trazabilidad)

| ID | Cambio | Prioridad |
|---|---|---|
| RN-11 | Arreglar texto del deep-link (incluir opción marcada) | Alta (T-01) |
| RN-05/06/07 | Modo Flash (selección + flujo) | Alta (T-02…T-05) |
| RN-08/09 | Timer + puntaje | Alta (T-03) |
| RN-12 | Pantalla de resultados separada | Alta (T-06) |
| RN-15 | Guardar resultado como imagen | Media (T-07) |
