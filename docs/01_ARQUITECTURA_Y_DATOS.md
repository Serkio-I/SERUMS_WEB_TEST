# 01 — Arquitectura y modelo de datos

> App estática, sin framework, sin build. Todo corre en el navegador. Sin backend ni login.

## 1. Archivos del proyecto

| Archivo | Rol | Se toca al… |
|---|---|---|
| `index.html` | **App completa**: HTML + CSS + JS + datos embebidos (`EXAMES`). | Cambiar UI, lógica, modos. |
| `serums_banco_data.js` | **Fuente única de datos** (`const EXAMES = {...}`). | Importar preguntas (vía `registro.py`). |
| `banco_registro.json` | Registro anti-solape (huellas SHA-1). | Automático con `registro.py`. |
| `tools/registro.py` | `build` / `stats` / `check` / `import`. | Importar/validar preguntas. |
| `tools/sync_index.py` | Re-embebe datos en `index.html` + regenera pestañas/etiquetas. | **Siempre después de importar.** |
| `tools/parse_examprazol.py` | Extrae exámenes oficiales desde examprazol (`/rendir`). | Traer exámenes oficiales. |
| `normas/` | PDFs oficiales + fichas coteadas. | Generar preguntas. |
| `docs/` | Esta documentación. | Documentar cambios. |
| `PLAN_MANANA.md` | Plan operativo del siguiente paso. | — |
| `subir_serums_banco.ps1` | Publica a GitHub Pages. | Deploy. |
| `.gitignore` | Excluye backups, PDFs pesados, artefactos. | — |

## 2. Tecnologías

- **HTML/CSS/JS vanilla** (ES5/ES6 básico). Sin React, sin bundler, sin npm.
- Datos como objeto JS `const EXAMES`.
- Persistencia: `localStorage` (solo marcas del Modo Simulacro).
- Sin dependencias de red en runtime, salvo el enlace externo a ChatGPT.

## 3. Flujo de datos (importante)

```
serums_banco_data.js  ──(sync_index.py)──▶  index.html (EXAMES embebido + EXAM_LABELS + chips)
        ▲                                            │
        │                                            ▼
   registro.py import                        window.load → render()
        │
tools/parse_examprazol.py (extrae oficiales)
```

- `serums_banco_data.js` es la **verdad** para datos.
- `index.html` **duplica** los datos embebidos para ser autocontenido (funciona con doble clic y en GitHub Pages solo con `index.html`).
- **Regla de oro:** después de cualquier `registro.py import`, correr `python tools/sync_index.py` para que la app refleje los datos.

## 4. Modelo de datos — `EXAMES`

```js
const EXAMES = {
  "2025-I": [
    {
      "n": 1,
      "stem": "Enunciado de la pregunta…",
      "opts": ["A. Opción 1", "B. Opción 2", "C. Opción 3", "D. Opción 4"],
      "ans": { "letra": "A", "texto": "Opción 1" },
      "meta": {
        "origen": "oficial",            // "oficial" | "generada"
        "fuente": "MINSA - SERUMS 2025-I",
        "anio": 2025,
        "verificado": "2026-11-24",
        "area": "Salud pública y epidemiología", // opcional
        "tema": "…",                    // opcional
        "ref": "NTS …",                 // opcional (norma/tabla)
        "explicacion": "…"              // opcional (89/100 de 2024-II-I la traen)
      }
    }
  ],
  "2024-II-I": [ … ]
};
```

### Reglas del formato
- `opts` **siempre** 4 opciones, cada una con prefijo `"X. "` (letra + punto + espacio).
- `ans.letra` ∈ {A,B,C,D} y debe existir una opción que empiece con `"<letra>."`.
- `ans.texto` = texto de la opción correcta **sin** el prefijo.
- `n` = número de pregunta (1..N), único dentro del examen.

### Claves de examen (`examKey`)
- Formato oficial: `AAAA` + `-` + `I|II` (+ `-I|II` si hay dos cuadernillos). Ej.: `2024-II-I`, `2025-I`, `2026-II`.
- Generadas: `GEN-AAAA` (ej. `GEN-2026`).
- El orden de pestañas lo define `ORDER` en `tools/sync_index.py`:
  `["2024-II-I","2025-I","2025-II","2026-I","2026-II"]`.
- Etiquetas en `EXAM_LABELS` (lo regenera `sync_index.py` desde `LABELS`).

## 5. Modelo de datos — registro anti-solape (`banco_registro.json`)

```json
{
  "version": 1,
  "fingerprint_algo": "sha1(norm(stem))",
  "updated": "2026-11-24",
  "counts": { "total": 500, "oficial": 500 },
  "items": {
    "<sha1>": {
      "id": "2024-II-I-001",
      "origin": "oficial",
      "source": "MINSA - SERUMS 2024-II Medicina I",
      "exam": "2024-II-I",
      "n": 1,
      "area": null, "tema": null, "ref": null,
      "status": "verificada",
      "added": "2026-11-24",
      "preview": "¿Cómo se denomina al caso nuevo…"
    }
  }
}
```

- `norm(s)` = minúsculas, sin tildes, solo `[a-z0-9]`, espacios colapsados.
- `fp(stem)` = `sha1(norm(stem))`.
- `import` salta preguntas cuya huella ya existe (evita solape entre exámenes).

## 6. Estado en el navegador — `localStorage`

- Clave: **`serums_marks`**.
- Formato: `{ "examKey:n": { "picked": "B" } }`. Ej.: `{ "2025-I:12": {"picked":"B"} }`.
- Uso: solo **Modo Simulacro** (recordar qué marcó el usuario por pregunta/examen).
- `getMarks()` / `saveMarks(m)` / `markKey(exam,n)` / `applyMark(card,q)` / `desmarcarBank()`.
- El Modo Flash usará estado **en memoria por sesión** (no persiste entre recargas), salvo decisión contraria (ver RN-13).

## 7. Funciones del script actual (`index.html`)

| Función | Qué hace |
|---|---|
| `deepUrl(q, picked)` | Construye URL `https://chatgpt.com/?q=…` con contexto + pregunta + clave. **Bug a corregir (RN-11):** no incluye el texto de la opción marcada. |
| `getMarks()` / `saveMarks()` | Leer/escribir marcas en `localStorage`. |
| `markKey(exam,n)` | Clave `"exam:n"`. |
| `applyMark(card,q)` | Re-aplica la marca guardada al renderizar (incluye estado visual + resultado + link IA). |
| `render()` | Pinta las tarjetas del examen activo (chip) o "todas". |
| `desmarcarBank()` | Borra marcas del examen activo (o todas) y re-renderiza. |

**Eventos actuales:**
- `#examFilter` click → cambia chip activo → `render()`; si es `.reset-btn` → `desmarcarBank()`.
- `#bankContent` click → delegación: si clic en `.opt` de una `.q-card`, marca/desmarca y evalúa.
- `window.load` → `render()`.

**Clases CSS clave:** `.chip`, `.chip.active`, `.reset-btn`, `.q-card`, `.q-head`, `.q-num`, `.q-exam-tag`, `.q-text`, `.opts`, `.opt`, `.letra`, `.opt.selected`, `.opt.correct`, `.ans`, `.result`, `.result.ok`, `.result.bad`, `.deep-btn`, `.hidden`, `.ia-btn`.

## 8. HTML relevante

- `<header>`: título, subtítulo, `#sourceInfo` (conteo).
- `#examFilter`: botones `.chip` por examen + `.chip.reset-btn` ("Desmarcar").
- `<main id="bankContent">`: aquí se inyectan las tarjetas.
- `<footer>`: fuente/verificación.
- Un único `<script>` al final con todo el JS y `EXAMES` embebido.

## 9. Agregar preguntas (flujo)

```powershell
cd C:\Users\sambrosio_hnc\MOCKUP
# 1) extraer (oficial)  → genera tools/_prueba_X.json con exam "TMP"
python tools/parse_examprazol.py "<url /rendir>" "tools/_prueba_X.json" "TMP" "<fuente>" <anio>
# 2) generar tools/_import_X.json con exam = "AAAA-II-I" y meta
# 3) importar
python tools/registro.py import tools/_import_X.json
# 4) sincronizar app
python tools/sync_index.py
# 5) validar
python tools/registro.py check
```

## 10. Invariantes (no romper)

1. `EXAMES` debe seguir siendo un objeto global accesible en `index.html`.
2. `opts` = 4 opciones con prefijo `"X. "`; `ans.letra` presente en `opts`.
3. Tras importar, **siempre** `sync_index.py`.
4. No agregar dependencias externas que rompan el "doble clic" (la app debe abrir sin servidor).
5. Mantener compatibilidad con `localStorage` existente (`serums_marks`).
6. La app debe seguir siendo usable en móvil (ancho ~360–480 px).
