# Documentación — Banco SERUMS / ENCAPS Medicina Humana

> **Proyecto:** app web móvil de práctica de preguntas para el examen SERUMS/ENCAPS (Medicina Humana, Perú).
> **Ubicación:** `C:\Users\sambrosio_hnc\MOCKUP`
> **Versión documentada:** v0.2 (500 preguntas, modo Simulacro) — 2026-11-24.
> **Próxima versión:** v0.3 (Modo Flash + arreglos) — ver `03_ESPEC_MODOS.md` y `05_TAREAS_Y_CHANGELOG.md`.

Este paquete de documentación existe para poder **continuar el proyecto en otra IA o en otra sesión** sin perder reglas, decisiones ni contexto.

## Cómo leer esta documentación

| Nº | Archivo | Contenido |
|---|---|---|
| 00 | `00_INDICE.md` | Este archivo. Mapa general y cómo correr la app. |
| 01 | `01_ARQUITECTURA_Y_DATOS.md` | Archivos, tecnologías, flujo de datos, esquema de preguntas, `localStorage`, herramientas. |
| 02 | `02_REGLAS_NEGOCIO.md` | Reglas de negocio numeradas (RN-xx): modos, tiempo, puntaje, fuentes, persistencia. |
| 03 | `03_ESPEC_MODOS.md` | Especificación funcional detallada de **Modo Simulacro** y **Modo Flash**, con criterios de aceptación. |
| 04 | `04_GUIA_TRASPASO.md` | Guía para retomar en otra IA: invariantes, qué tocar / qué no, checklist de pruebas. |
| 05 | `05_TAREAS_Y_CHANGELOG.md` | Lista de tareas ordenadas (T-xx) + historial de versiones. |

## Resumen en 10 líneas

- App estática (HTML/CSS/JS puro, sin framework ni build).
- **500 preguntas** oficiales (MINSA) con clave: 2024-II-I, 2025-I, 2025-II, 2026-I, 2026-II.
- Datos en `serums_banco_data.js` (fuente única) y **embebidos** en `index.html` (app autocontenida).
- **Modo Simulacro** (actual): filtra por examen, marca → corrige al instante + botón IA; marcas persisten.
- **Modo Flash** (a implementar): el alumno elige N preguntas y (opcional) exámenes; miniexamen con **conteo regresivo**; feedback solo correcto/incorrecto; al final repaso completo + botón IA + guardar resultado como imagen.
- Regla temporal: **72 s por pregunta** (1:12, confirmado) → total = N × 72 s.
- Sin login, sin backend. Solo el enlace a ChatGPT sale a internet.
- Anti-duplicado por huella SHA-1 del enunciado normalizado.
- Herramientas: `tools/registro.py`, `tools/sync_index.py`, `tools/parse_examprazol.py`.

## Cómo correr la app localmente

```powershell
cd C:\Users\sambrosio_hnc\MOCKUP
python -m http.server 8765 --bind 127.0.0.1
# abrir http://127.0.0.1:8765/index.html
```
> El navegador embebido bloquea `file://`; por eso se sirve por HTTP. Doble clic en `index.html` también funciona en un navegador común.

## Cómo sumar preguntas

Ver `01_ARQUITECTURA_Y_DATOS.md` §"Agregar preguntas" y `PLAN_MANANA.md` en la raíz (flujo `entregar → registro.py import → sync_index.py`).

## Estado actual (implementado vs planificado)

| Capacidad | Estado |
|---|---|
| Banco 500 preguntas / 6 pestañas | ✅ Implementado |
| Marcar → corregir al instante (Modo Simulacro) | ✅ Implementado |
| Botón "Adentrarse con IA" | ✅ Implementado (deep-link corregido, RN-13) |
| Persistencia de marcas (`localStorage`) | ✅ Implementado |
| "Desmarcar" | ✅ Implementado |
| Modo Flash (N preguntas + timer) | 🟡 En progreso (T-02, T-03, T-04, T-05, T-06, T-07 hechos en 2026-11-24) |
| Resultados separados correctas/incorrectas | 🟡 Planificado |
| Guardar resultado como imagen | 🟡 Planificado |
| Arreglo del texto a la IA (opción marcada) | ✅ Hecho (T-01, RN-13) |
