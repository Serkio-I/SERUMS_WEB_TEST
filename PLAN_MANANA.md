# Plan de trabajo — mañana (continuación del banco SERUMS)

Actualizado: **2026-11-24**. Ubicación: `C:\Users\sambrosio_hnc\MOCKUP`.

> ## ⏸️ MARCADO PARA MAÑANA (2026-11-24)
> - **Hoy cerró:** T-01 (fix deep-link IA) ✅ · T-02 (selector Simulacro/Flash) ✅.
> - **Siguiente:** **T-03** — Modo Flash: configuración (N + exámenes + tiempo estimado). 72 s/pregunta confirmado.
> - **Otros pendientes (fuera de app):** importar 2024-II-II (100 oficiales) → 600; generar 25 desde anemia; inmunizaciones OCR.
> - **Subido:** ✅ commit + push de todo el avance del día (selector de modo, fix IA, docs, banco 500).

## Estado al cerrar hoy

- **500 preguntas** integradas y verificadas en la app (`index.html`).
  - 2024-II · Medicina I: **100** (NUEVO, oficial, clave MINSA) ✅
  - 2025-I: 100 · 2025-II: 100 · 2026-I: 100 · 2026-II: 100
- App probada en navegador: 500 tarjetas, 6 pestañas (Todas + 5 exámenes), marcar→evaluar→IA, persistencia en `localStorage`, "Desmarcar" OK.
- Verificaciones: `node --check` OK, 0 duplicados (`registro.py check`), 0 solape con los 4 exámenes previos.

## Cómo está armado (no romper)

| Archivo | Rol |
|---|---|
| `serums_banco_data.js` | **Fuente única de datos** (`EXAMES`, 500 preguntas). |
| `index.html` | App. Tiene los datos **embebidos** (autocontenida). |
| `tools/registro.py` | `build` / `stats` / `check` / `import` + registro anti-solape. |
| `tools/sync_index.py` | Re-embebe datos en `index.html` y regenera pestañas/etiquetas. **Correr SIEMPRE después de importar.** |
| `tools/parse_examprazol.py` | Extrae preguntas de páginas `/rendir` de examprazol (oficiales, con clave). |
| `banco_registro.json` | Registro de huellas SHA-1 (500). |
| `normas/` | PDFs oficiales (NTS 246-2026 inmunizaciones, NTS 213-2024 anemia) + fichas coteadas. |

### Flujo estándar para sumar un examen oficial
```powershell
cd C:\Users\sambrosio_hnc\MOCKUP
# 1) extraer (ejemplo: 2024-II Medicina II)
python tools/parse_examprazol.py "https://examprazol.com/examenes-pasados/serums-2024-ii-medicina-ii/rendir" "tools/_prueba_2024II-II.json" "2024-II-II" "MINSA - SERUMS 2024-II Medicina II" 2024
# 2) revisar que traiga 100, opts=4, letra válida (mismo chequeo que ya usamos)
# 3) importar
python tools/registro.py import tools/_import_2024II-II.json
# 4) sincronizar la app
python tools/sync_index.py
# 5) verificar
python tools/registro.py check
```
> Al importar, el archivo debe tener `"exam": "2024-II-II"` y `"meta": {"origen":"oficial","fuente":"...","anio":2024,"verificado":"<fecha>"}`. El `_prueba_*.json` sale con `exam:"TMP"`; cambiar a la clave real (o generar `_import_*.json` con un mini script, como se hizo hoy).

## Mañana — Paso 1: cerrar los oficiales 2024+ (100)

- **2024-II · Medicina II** → 100 preguntas oficiales, mismo parser. Deja el banco en **600**.
- Con esto se agota lo oficial SERUMS ≥ 2024 (piso fijado por el usuario). Lo anterior a 2024 NO se usa (cambió el examen).

## Mañana — Paso 2: generación coteada (meta 25)

**Áreas de trabajo (taxonomía para filtros):**
1. Salud pública y epidemiología
2. Gestión y administración en salud
3. Investigación y bioestadística
4. Ética y bioética
5. Clínica y cuidados integrales

**Fuentes ya listas:**
- **Anemia:** `normas/FICHA_ANEMIA_213-2024.md` — datos exactos (prevención 2 mg/kg/día vs tratamiento 3 mg/kg/día, cortes de Hb, gestante). **Lista para generar YA.**
- **Inmunizaciones:** `normas/NTS-246-2026-parte-1.pdf` (97 págs) y `parte-2.pdf` (43 págs). ⚠️ **Son escaneadas: no tienen capa de texto.** Para generar hay que aplicar **OCR** (tesseract no está instalado). Opciones:
  - Instalar: `winget install UB-Mannheim.TesseractOCR` y luego `pytesseract` sobre las páginas del esquema (anexo, casi al final).
  - O usar OCR en la nube / leer las imágenes del esquema.
  - Mientras no haya OCR, **generar solo de anemia** y dejar inmunizaciones para cuando esté el OCR.

**Plantilla de pregunta generada** (archivo `tools/_gen_*.json`):
```json
{
  "exam": "GEN-2026",
  "meta": {"origen": "generada", "fuente": "NTS 213-2024 (R.M. 251-2024/MINSA)", "anio": 2026, "verificado": "2026-11-25"},
  "preguntas": [
    {
      "n": 1,
      "stem": "Niño de 8 meses, a término, buen peso, Hb 11.0 g/dL. ¿Qué suplementación preventiva de hierro corresponde?",
      "opts": ["A. 2 mg/kg/día", "B. 3 mg/kg/día", "C. 6 mg/kg/día", "D. 1 mg/kg/día"],
      "ans": {"letra": "A", "texto": "2 mg/kg/día"},
      "meta": {"area": "Clínica y cuidados integrales", "tema": "Anemia - suplementación preventiva", "ref": "NTS 213-2024, Tabla N° 6"}
    }
  ]
}
```
Importar y sincronizar:
```powershell
python tools/registro.py import tools/_gen_anemia.json
python tools/sync_index.py
```

**Regla de cotejo (no negociable):** cada pregunta generada lleva `ref` a la tabla/sección exacta de la norma, y su clave se contrasta con la ficha. Si un dato no está en la norma, no se genera.

## Cola pendiente (después)

1. 2024-II-II (100 oficiales) — Paso 1 de mañana.
2. Generación desde anemia (25) — Paso 2.
3. Inmunizaciones (OCR NTS 246) → más generadas.
4. Simulacros públicos de academias: Usamedic (100 resueltas, pide correo → no 100% abierto), SeruMaster (10 gratis, 3 opciones). Bajo rendimiento; evaluar después de los oficiales.
5. ENAM 2026-I / 2026-II Extraordinario (ASPEFAM) — exámenes completos, pero **son ENAM**, no SERUMS. Decidir si se suman como sección aparte.

## URLs clave
- Exámenes oficiales (gratis, sin cuenta): https://examprazol.com/examenes-pasados
- 2024-II Med II (rendir): https://examprazol.com/examenes-pasados/serums-2024-ii-medicina-ii/rendir
- NTS 246-2026 (R.M. 561-2026): https://www.gob.pe/institucion/minsa/normas-legales/8265031-561-2026-minsa
- NTS 213-2024 anemia (R.M. 251-2024): https://www.gob.pe/institucion/minsa/normas-legales/5440166-251-2024-minsa
