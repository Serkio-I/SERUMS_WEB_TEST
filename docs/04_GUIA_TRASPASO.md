# 04 — Guía de traspaso (continuar en otra IA)

> Pega este archivo (y los demás de `docs/`) en la otra IA para retomar sin perder contexto.

## 1. Qué es el proyecto

App web móvil, estática (HTML/CSS/JS puro), para practicar preguntas del **SERUMS/ENCAPS de Medicina Humana (Perú)**. Corre en el navegador, sin backend ni login. Banco actual: **500 preguntas oficiales** (MINSA) con clave.

## 2. Dónde está todo

```
C:\Users\sambrosio_hnc\MOCKUP\
├─ index.html                 ← la app (HTML+CSS+JS+datos embebidos)
├─ serums_banco_data.js       ← datos (fuente única)
├─ banco_registro.json        ← anti-duplicado
├─ tools\
│  ├─ registro.py             ← import/stats/check/build
│  ├─ sync_index.py           ← re-embebe datos en index.html
│  └─ parse_examprazol.py     ← extrae oficiales
├─ normas\                    ← PDFs + fichas coteadas
├─ docs\                      ← esta documentación
├─ PLAN_MANANA.md             ← plan operativo
└─ subir_serums_banco.ps1     ← deploy a GitHub Pages
```

## 3. Comandos

```powershell
cd C:\Users\sambrosio_hnc\MOCKUP
python tools/sync_index.py           # tras importar datos
python tools/registro.py stats       # conteos
python tools/registro.py check       # duplicados
python -m http.server 8765 --bind 127.0.0.1   # probar en navegador
node --check <archivo.js>            # validar sintaxis JS extraída
```

## 4. Invariantes (NO romper)

1. `EXAMES` global con el formato de `01_ARQUITECTURA_Y_DATOS.md` §4.
2. `opts` = 4 con prefijo `"X. "`; `ans.letra` presente.
3. Tras `registro.py import` → **siempre** `sync_index.py`.
4. La app debe abrir con **doble clic** (sin servidor) y en GitHub Pages.
5. No romper `localStorage['serums_marks']` (marcas del Modo Simulacro).
6. Mobile-first (~360–480 px). Sin dependencias CDN.
7. Textos en español, tuteo neutro peruano (sin voseo).

## 5. Qué hacer y qué NO

**Sí:**
- Documentar cada función nueva en `docs/` y anotar en `05_TAREAS_Y_CHANGELOG.md`.
- Probar en navegador real (Playwright) antes de dar por cerrada una tarea.
- Mantener el modo Simulacro funcionando mientras se agrega Flash.

**No:**
- No reescribir todo `index.html` de golpe (riesgo de romper). Cambios incrementales.
- No meter frameworks ni build.
- No persistir datos personales.
- No cambiar 72 s/pregunta sin confirmar (RN-08).

## 6. Checklist de pruebas (Playwright / navegador)

1. Abrir la app → 500 tarjetas en "Todas".
2. Chip de cada examen → 100 tarjetas con la etiqueta correcta.
3. Simulacro: marcar opción → aparece ¡Correcto!/Incorrecto + respuesta + botón IA.
4. Recargar → la marca persiste.
5. "Desmarcar" en un examen → borra solo ese examen; en "Todas" → borra todo.
6. Abrir el enlace IA de una respuesta **incorrecta** → el texto debe decir "Yo marqué la opción B: <texto>. Pero la correcta es A: <texto>."
7. Flash: elegir N y exámenes → Iniciar → 1 pregunta por pantalla con timer.
8. Dejar correr el timer hasta 0 → termina y va a resultados.
9. Resultados: correctas e incorrectas separadas; cada una con IA.
10. "Guardar resultado" → descarga PNG con puntaje, exámenes y N.

## 7. Funciones clave actuales (para editar con cuidado)

```js
function deepUrl(q, picked) {
  let msg = IA_CONTEXT + ". La pregunta es: " + q.stem + ". ";
  if (picked && picked !== q.ans.letra) {
    msg += "Yo marqué esta respuesta: " + picked + ". Pero la respuesta correcta es: " + q.ans.letra + ". " + q.ans.texto + ".";
  } else {
    msg += "La respuesta correcta es: " + q.ans.letra + ". " + q.ans.texto + ".";
  }
  return "https://chatgpt.com/?q=" + encodeURIComponent(msg);
}
```
**Fix RN-13:** incluir el texto de la opción marcada:
```js
function optionText(q, letra) {
  const o = q.opts.find(function (x) { return x.charAt(0) === letra; });
  return o ? o.slice(2).trim() : "";
}
// dentro del if:
msg += "Yo marqué la opción " + picked + ": " + optionText(q, picked) +
       ". Pero la respuesta correcta es " + q.ans.letra + ": " + q.ans.texto + ".";
```

## 8. Prompt listo para pegar en otra IA

```
Estoy continuando una app web estática para practicar preguntas SERUMS/ENCAPS
Medicina Humana (Perú). Está en C:\Users\sambrosio_hnc\MOCKUP.
Lee PRIMERO: docs/00_INDICE.md, docs/01_ARQUITECTURA_Y_DATOS.md,
docs/02_REGLAS_NEGOCIO.md, docs/03_ESPEC_MODOS.md, docs/04_GUIA_TRASPASO.md,
docs/05_TAREAS_Y_CHANGELOG.md y PLAN_MANANA.md.
La app es HTML/CSS/JS puro, sin backend. Datos en serums_banco_data.js y
embebidos en index.html; tras cualquier import se corre tools/sync_index.py.
Debemos implementar el Modo Flash y corregir el deep-link IA (RN-13) tarea por
tarea, sin romper el Modo Simulacro. Valida con Playwright y actualiza el
CHANGELOG. No inventes reglas: están en docs/02_REGLAS_NEGOCIO.md.
```

## 9. Contacto de datos / credenciales

- No hay credenciales ni API keys en el proyecto.
- Deploy: `subir_serums_banco.ps1` requiere un **PAT clásico** con scope `repo` (lo aporta el usuario).
