# Banco SERUMS Medicina Humana — Estado del proyecto

Ubicación: `C:\Users\sambrosio_hnc\MOCKUP`

> Plan de mañana (paso a paso): ver **`PLAN_MANANA.md`**.
> Ficha de anemia coteada: **`normas/FICHA_ANEMIA_213-2024.md`**.

## Estado actual (2026-11-24)

- **500 preguntas** integradas y verificadas en `index.html`.
  - 2024-II · Medicina I: 100 (NUEVO — oficial, clave MINSA)
  - 2025-I: 100 · 2025-II: 100 · 2026-I: 100 · 2026-II: 100
- **6 pestañas** en la app: Todas + 5 exámenes (orden cronológico).
- Registro anti-solape: `banco_registro.json` (500 huellas, 0 duplicados).
- Última verificación: `node --check` OK · Playwright: 500 tarjetas, pestaña 2024-II-I = 100, marcar→evaluar→IA OK, persistencia `localStorage` OK, "Desmarcar" OK.

## Arquitectura

| Archivo | Rol |
|---|---|
| `serums_banco_data.js` | Fuente única de datos (`EXAMES`). |
| `index.html` | App móvil (datos embebidos, autocontenida). |
| `tools/registro.py` | `build`/`stats`/`check`/`import`. Dedupe por `sha1(norm(stem))`. |
| `tools/sync_index.py` | Re-embebe datos y regenera pestañas/etiquetas en `index.html`. **Correr tras cada import.** |
| `tools/parse_examprazol.py` | Extrae exámenes oficiales de examprazol (`/rendir`). |
| `banco_registro.json` | Huellas SHA-1 de todo lo barrido. |
| `normas/` | PDFs oficiales + fichas coteadas. |
| `PLAN_MANANA.md` | Siguiente paso detallado. |

## Flujo para sumar un examen oficial

```powershell
cd C:\Users\sambrosio_hnc\MOCKUP
python tools/parse_examprazol.py "<url /rendir>" "tools/_prueba_X.json" "<EXAM_KEY>" "<fuente>" <anio>
# revisar 100 / opts=4 / letra válida; generar _import_X.json con exam=EXAM_KEY
python tools/registro.py import tools/_import_X.json
python tools/sync_index.py
python tools/registro.py check
```

## Qué se hizo el 2026-11-24

1. Parser de examprazol corregido (regex de número/letra con punto). 100/100 preguntas de 2024-II-I, 4 opciones, 89 con explicación.
2. Confirmado que 2025-I tipo A y B son el mismo examen (100/100 coinciden) → no aportan.
3. Importado **2024-II · Medicina I completo (100)** como examen oficial. Banco 400 → 500.
4. Creado `tools/sync_index.py` (sincronización reproducible app↔datos). Elimina el desfase manual.
5. Descargadas las normas para generar: NTS 246-2026 (inmunizaciones, **escaneada**, requiere OCR) y NTS 213-2024 (anemia, con texto). Ficha de anemia extraída y coteada.
6. App validada en navegador real (Playwright) con las 500 preguntas.

## Historia breve

- Banco nació del PDF oficial (229) → completado a 400 parseando 2025-II y 2026-II.
- 2026-11-24: +100 (2024-II-I) → 500.

## Documentación (2026-11-24)

- `docs/00_INDICE.md` … `docs/05_TAREAS_Y_CHANGELOG.md`: arquitectura, modelo de datos, **reglas de negocio (RN-xx)**, especificación de **Modo Simulacro y Modo Flash**, guía de traspaso a otra IA y cola de tareas (T-xx).
- **T-01** (fix deep-link IA: incluir texto de la opción marcada) ✅ hecho y verificado en navegador.

## Pendientes

1. Implementar **Modo Flash** (T-02…T-08) según `docs/03_ESPEC_MODOS.md`.
2. Importar 2024-II · Medicina II (100 oficiales) → 600.
3. Generar 25 desde anemia (ficha lista). Inmunizaciones: OCR pendiente.
4. Deploy: activar GitHub Pages.
