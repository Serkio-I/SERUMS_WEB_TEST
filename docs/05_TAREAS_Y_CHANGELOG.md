# 05 — Tareas (una por una) y Changelog

> Ejecutar **en orden**. Cada tarea tiene criterio de aceptación. Marcar `[x]` al terminar y anotar en el Changelog.
> Objetivo: cubrirnos del límite de uso haciendo tandas chicas y verificables.

## Definición de "hecho" (para toda tarea)
1. Código en `index.html` sin romper el Modo Simulacro.
2. `node --check` del JS extraído pasa.
3. Probado en navegador real (Playwright o manual).
4. Documentación/CHANGELOG actualizados.

---

## Cola de tareas

### T-01 · Arreglar deep-link IA (RN-13) — prioridad alta, chico — **✅ HECHO 2026-11-24**
**Qué:** en `deepUrl(q, picked)`, cuando la opción marcada es incorrecta, incluir **su texto**, no solo la letra: "Yo marqué la opción B: <texto>. Pero la correcta es A: <texto>."
**Aceptación:**
- [x] Respuesta incorrecta → mensaje con letra **y texto** de la marcada + letra y texto de la correcta.
- [x] Respuesta correcta / sin marcar → mensaje sin "yo marqué".
- [x] Sin errores de encoding en el enlace.

### T-02 · Selector de modo + esqueleto Flash — **✅ HECHO 2026-11-24**
**Qué:** agregar conmutador `Simulacro | Flash` arriba. Simulacro = lo actual. Flash = pantalla vacía con título.
**Aceptación:**
- [x] Cambiar de modo no rompe Simulacro (500 tarjetas intactas).
- [x] Estado activo visible.
- [x] Móvil OK.

### T-03 · Flash — Configuración (N + exámenes + tiempo estimado)
**Qué:** pantalla de config: N (10/20/25/50/custom), multiselección de exámenes (opcional, default todos), tiempo estimado `N×72s`, botón Iniciar. Sortear N preguntas del pool.
**Aceptación:**
- [ ] N validado (1..500).
- [ ] Filtro vacío = todos.
- [ ] Tiempo estimado correcto.
- [ ] Iniciar genera N preguntas aleatorias sin repetir.

### T-04 · Flash — Motor del examen (1 pregunta + feedback + siguiente)
**Qué:** mostrar 1 pregunta; marcar → solo correcto/incorrecto; "Siguiente"; progreso `i/N`; re-marcar antes de siguiente; guardar estado.
**Aceptación:**
- [ ] Una pregunta por pantalla.
- [ ] Solo correcto/incorrecto durante el examen (sin clave, sin IA).
- [ ] "Siguiente" avanza y no se duplica con doble clic.
- [ ] Última → resultados.

### T-05 · Flash — Temporizador
**Qué:** conteo regresivo `mm:ss` sticky; total `N×72s`; al 0 termina; colores de aviso.
**Aceptación:**
- [ ] Decrece correctamente.
- [ ] Al 0 termina y va a resultados.
- [ ] No respondidas = incorrectas.
- [ ] Cambio de color en umbrales.

### T-06 · Flash — Pantalla de resultados
**Qué:** puntaje X/N y %; listas separadas de correctas e incorrectas (con "sin responder"); cada pregunta con tu respuesta, la correcta y botón IA.
**Aceptación:**
- [ ] Correctas e incorrectas separadas.
- [ ] Muestra tu respuesta vs correcta.
- [ ] Botón IA con texto de la opción marcada (RN-13).
- [ ] "Hacer otro Flash" reinicia config.

### T-07 · Flash — Guardar resultado como imagen (RN-15)
**Qué:** botón flotante superior; Canvas → PNG descargable con puntaje, exámenes, N, fecha.
**Aceptación:**
- [ ] Descarga PNG válido.
- [ ] Contiene puntaje + exámenes + N.
- [ ] Funciona en móvil sin librerías.

### T-08 · Casos borde y pulido
**Qué:** validaciones (N=0, N>pool, doble clic, timer a 0 con pendientes), estilos móviles, textos.
**Aceptación:**
- [ ] Tabla de casos borde de `03_ESPEC_MODOS.md` §3 cumplida.

### T-09 · Documentación + pruebas finales
**Qué:** actualizar docs y CHANGELOG; correr checklist de `04_GUIA_TRASPASO.md` §6.
**Aceptación:**
- [ ] Checklist completo en verde.
- [ ] Docs actualizados.

### T-10 · (Opcional) Deploy y PWA
**Qué:** publicar en GitHub Pages; evaluar manifest/service worker para uso offline.
**Aceptación:**
- [ ] URL pública funcionando en el celular.

---

## Changelog

### v0.2 — 2026-11-24
- **+100 preguntas** oficiales: SERUMS 2024-II · Medicina I (con clave, 89 con explicación).
- Banco total: **500** (2024-II-I, 2025-I, 2025-II, 2026-I, 2026-II).
- Nueva herramienta `tools/sync_index.py` (re-embebe datos y regenera pestañas).
- `tools/parse_examprazol.py` corregido y probado.
- Registro anti-solape: 500 huellas, 0 duplicados.
- App validada: 500 tarjetas, 6 pestañas, persistencia, Desmarcar.
- Documentación completa creada (`docs/`).
- `subir_serums_banco.ps1` corregido (esperaba archivos inexistentes).

### v0.1 — 2026-11-20
- App base con 400 preguntas (2025-I, 2025-II, 2026-I, 2026-II).
- Flujo marcar → corregir al instante → botón IA.
- Persistencia de marcas (`localStorage`) y "Desmarcar".
- Validación con Playwright.

### v0.3 — (en curso)
- ✅ **T-01:** fix del deep-link IA — ahora incluye el texto de la opción marcada (RN-13). Verificado en navegador.
- ✅ **T-02:** selector de modo `Simulacro | Flash` + esqueleto del Modo Flash. Simulacro intacto (500 tarjetas). Verificado en navegador.
- ⏳ Pendiente: Modo Flash completo (T-03…T-08).
