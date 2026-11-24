# 03 — Especificación funcional: Modo Simulacro y Modo Flash

> Referencias a reglas: RN-xx (ver `02_REGLAS_NEGOCIO.md`).
> Estado: Simulacro = ✅ actual. Flash = 🟡 a construir.

---

## 0. Navegación global (nuevo)

Un selector de modo arriba, debajo del título:

```
[ Simulacro ]  [ Flash ]
```

- **Simulacro** → muestra lo que hoy existe (chips por examen + banco de tarjetas).
- **Flash** → muestra la pantalla de configuración del miniexamen.
- El modo activo se recuerda en memoria (no hace falta persistir).
- En móvil: dos botones tipo pastilla, grandes y táctiles (`min-height: 44px`).

---

## 1. MODO SIMULACRO (comportamiento actual, se conserva)

**Objetivo:** recorrer el banco y estudiar con corrección inmediata.

### UI
- Fila de `.chip`: `Todas`, un chip por examen, botón `Desmarcar`.
- Lista de tarjetas (`.q-card`) con: número, etiqueta de examen, enunciado, 4 opciones, caja de respuesta, caja de resultado, botón IA.

### Flujo
1. El usuario elige un chip (examen) o "Todas".
2. Se renderizan las preguntas de ese filtro.
3. Al tocar una opción:
   - Se marca (`.selected`).
   - Se evalúa: **¡Correcto!** o **Incorrecto** + se revela la respuesta correcta.
   - Aparece el botón **"Adentrarse con esta pregunta con la IA"**.
   - Se guarda la marca en `localStorage`.
4. Tocar la misma opción otra vez → desmarca y oculta resultado/IA.
5. "Desmarcar" → borra marcas del examen activo (o todas).

### Criterios de aceptación (Simulacro)
- [ ] 500 preguntas visibles en "Todas"; cada examen muestra sus 100.
- [ ] Marcar corrige al instante y revela la correcta.
- [ ] El botón IA se muestra tras evaluar y su enlace incluye el texto de la opción marcada (RN-13).
- [ ] Las marcas persisten tras recargar.
- [ ] "Desmarcar" respeta el alcance (examen vs todas).

---

## 2. MODO FLASH (nuevo)

**Objetivo:** práctica rápida tipo "mini-simulacro" contra reloj, ideal para ratos libres.

### 2.1 Pantalla A — Configuración

Elementos:
- Título: "Modo Flash".
- **Cantidad de preguntas (N):** botones rápidos `10 · 20 · 25 · 50` + campo numérico "Otra cantidad".
  - Validación: entero entre 1 y total disponible (500). Si N > pool → avisar y usar el máximo.
- **Exámenes (opcional, multiselección):** chips con check para cada examen + "Todos" (por defecto "Todos").
  - Si el usuario no elige ninguno → equivale a "Todos".
- **Tiempo estimado:** se calcula y muestra en vivo: `N × 72 s` en formato `mm:ss` (o `h:mm:ss`). Ej.: 20 → `24:00`.
- **Botón "Iniciar"** (grande, ancho completo).
- Texto de ayuda: "Se eligen al azar del banco. Al agotarse el tiempo, el examen termina."

### Criterios de aceptación (Config)
- [ ] N acepta rápidos y personalizado; se valida rango.
- [ ] Filtro de exámenes opcional; vacío = todos.
- [ ] El tiempo estimado se actualiza al cambiar N.
- [ ] "Iniciar" arranca el examen con N preguntas sorteadas del pool.

### 2.2 Pantalla B — Examen

Layout (móvil):
```
┌───────────────────────────────┐
│  Pregunta 3 / 20      ⏱ 18:42 │  ← sticky (progreso + timer)
│  [Progreso ▓▓▓░░░░░░░░]        │
├───────────────────────────────┤
│  SERUMS 2025-I                 │  ← etiqueta examen
│  Enunciado de la pregunta…     │
│  A. Opción 1                   │
│  B. Opción 2                   │
│  C. Opción 3                   │
│  D. Opción 4                   │
│                                │
│  [ ¡Correcto! / Incorrecto ]   │  ← feedback breve
│                                │
│           [ Siguiente → ]      │  ← habilitado tras marcar
└───────────────────────────────┘
```

Reglas de comportamiento:
- Se muestra **una sola pregunta** a la vez.
- El alumno puede cambiar su respuesta **antes** de pulsar "Siguiente" (re-marcar). Al pulsar "Siguiente" se fija la respuesta.
- Al marcar se muestra **solo** correcto/incorrecto (sin revelar la correcta, sin IA) — RN-11.
- "Siguiente" guarda `{pregunta, marcada, correcta?}` en el estado de la sesión y avanza.
- Barra de progreso y contador `Pregunta i / N`.
- **Timer** en `mm:ss`, actualizado cada segundo; color normal → ámbar (< 25% del tiempo) → rojo (< 10% o < 60 s).
- Al llegar a **00:00** → termina automáticamente (RN-08).
- Al responder la última y pulsar "Siguiente" → termina.

### Criterios de aceptación (Examen)
- [ ] Se muestra 1 pregunta por pantalla con progreso y timer.
- [ ] Marcar muestra solo correcto/incorrecto y habilita "Siguiente".
- [ ] No aparece IA ni la respuesta correcta durante el examen.
- [ ] El timer decrece y al llegar a 0 termina el examen.
- [ ] Re-marcar antes de "Siguiente" actualiza la selección.
- [ ] Las no respondidas quedan como incorrectas.

### 2.3 Pantalla C — Resultados

Elementos:
- **Encabezado:** "Examen terminado" + resumen: `Correctas X de N (P%)` + tiempo usado.
- **Botón flotante superior "Guardar resultado"** (ver 2.4).
- **Sección Correctas (X):** lista de preguntas acertadas.
- **Sección Incorrectas (Y):** lista de preguntas falladas + las no respondidas ("Sin responder").
- Cada ítem muestra:
  - Enunciado.
  - Opciones con marca de **tu respuesta** y de la **correcta** (verde).
  - Botón **"Adentrarse con IA"** (RN-13) — aquí sí, versión completa.
- Botones de cierre: **"Hacer otro Flash"** (vuelve a Configuración) y **"Volver a Simulacro"**.

### Criterios de aceptación (Resultados)
- [ ] Se muestran todas las preguntas, separadas en correctas e incorrectas.
- [ ] Cada pregunta indica tu respuesta y la correcta.
- [ ] Cada pregunta tiene botón IA con el texto de la opción marcada.
- [ ] "Hacer otro Flash" reinicia la configuración.

### 2.4 Guardar resultado como imagen (RN-15)

- Botón **flotante superior** visible en Resultados.
- Al pulsar: genera un **PNG** con un diseño tipo "tarjeta de puntaje":
  - Título: "Banco SERUMS — Resultado Flash".
  - **Puntaje:** `X/N (P%)`.
  - **Exámenes:** lista o "Todos".
  - **Cantidad de preguntas:** N.
  - **Fecha/hora** de finalización.
  - (Opcional) marca/logo textual.
- Implementación: `Canvas` 1080×1350 (o similar) → `canvas.toDataURL('image/png')` → `<a download>`.
- Nombre de archivo: `serums-flash-YYYYMMDD-HHMM.png`.
- Sin datos personales.

### Criterios de aceptación (Imagen)
- [ ] El botón descarga un PNG válido.
- [ ] La imagen contiene puntaje, exámenes y cantidad.
- [ ] Funciona en móvil (sin librerías externas).

---

## 3. Casos borde

| Caso | Comportamiento |
|---|---|
| N = 0 o vacío | Bloquear "Iniciar"; pedir cantidad ≥ 1. |
| N > disponibles | Usar máximo disponible; avisar "Solo hay M disponibles". |
| Filtro de exámenes deja 0 preguntas | No puede pasar (siempre hay 500); si pasara, avisar. |
| El usuario cierra/recarga en Flash | Se pierde la sesión (RN-17). |
| Timer en 0 con preguntas pendientes | Se cierran como incorrectas (sin responder). |
| Marca una opción y no pulsa "Siguiente" | Cuenta como respondida al cerrar por tiempo si ya marcó; si no marcó, "Sin responder". |
| Doble clic en "Siguiente" | Ignorar el segundo (avanzar una sola vez). |

## 4. Notas de implementación (para el que programe)

- Mantener **todo en `index.html`** (o, si se prefiere, mover el JS a `app.js` y referenciarlo; decidir antes de empezar).
- **No** romper `localStorage` existente (`serums_marks`).
- El estado de Flash vive en un objeto en memoria: `flashState = { n, exams:[], items:[], idx, remaining, finished }`.
- Cada `item` = `{ exam, q, picked, correct, answered }`.
- Reutilizar `deepUrl(q, picked)` para el botón IA (con el fix RN-13).
- Sortear con `Math.random()` sin reemplazo (Fisher–Yates sobre el pool).
- El timer: `setInterval` de 1000 ms; guardar `startedAt` y calcular `remaining` por diferencia de reloj (más robusto que decrementar).
- Evitar dependencias CDN (rompen el uso con doble clic / offline).
