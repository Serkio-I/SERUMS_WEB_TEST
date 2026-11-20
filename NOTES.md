# Banco SERUMS Medicina Humana 2025-2026 — Estado del proyecto

Ubicación: `C:\Users\sambrosio_hnc\MOCKUP`

## Estado final de la app (serums_banco.html + serums_banco_data.js)

- **400 preguntas únicas** (Tipo A): 2025-I: 100, 2025-II: 100, 2026-I: 100, 2026-II: 100.
- Flujo: marcar opción → evaluación instantánea (¡Correcto!/Incorrecto, slide-in NDP) → respuesta correcta oculta hasta evaluar → botón deep → ChatGPT (contexto + pregunta + respuesta; si fallaste, muestra la que marcaste).
- Botón **"Desmarcar"**: pestaña de un examen → borra solo las marcas de ese examen; "Todas" → borra todas las marcas. Marcas persisten en `localStorage` (key `serums_marks`) — sobreviven a recargar/cerrar el navegador.
- "Desmarcar" solo quita marcas, **no borra las preguntas** del banco.
- Validación realizada: `node --check` ✅, Playwright (navegador): 400 cards renderizadas, flujo marcar→evaluar→deep ✅, Desmarcar verificado (examen solo / Todas) ✅, persistencia de marcas verificada (recarga mantiene la marca) ✅.

## Archivos finales

- `serums_banco.html` — app principal (banco, flujo, persistencia).
- `serums_banco_data.js` — datos (`EXAMES`, 400 preguntas).
- `serums-study.html` — página de IA Profesora (opcional, no es el banco).
- `Banco_SERUMS_Medicina_2025-2026.pdf` — PDF oficial (referencia, MINSA).
- `fuentes_oficiales/` — PDFs de claves oficiales (referencia).
- `README.md` — descripción corta del proyecto.
- `NOTES.md` — este archivo (estado para próximos tajos).
- `subir_serums_banco.ps1` — script automatizado para subir a GitHub.
- `.gitignore` — ignora `.playwright-mcp/` (archivos de prueba de Playwright).

## Datos verificados (2026-11-20)

- 400 preguntas parseadas del PDF oficial de MINSA (gob.pe): preguntas + opciones + clave de respuesta por examen.
- Errores de transcripción corregidos; encoding UTF-8 del PDF verificado.
- Cada examen: 100 preguntas (ns 1-100, sin duplicados), 4 opciones cada una, clave de respuesta presente.

## Cómo subir a GitHub (pendiente)

- Necesito un **PAT clásico** (Classic PAT) con scope `repo`: https://github.com/settings/tokens
- Ejecutar: `.\subir_serums_banco.ps1 -Token "<el token>"` (el script descubre tu usuario de GitHub desde el token)
- Luego activar **GitHub Pages**: Settings → Pages → Branch: `main` → Save → URL: `https://<usuario>.github.io/serums-banco/`
- Probar desde el celular.

## Script automatizado: subir_serums_banco.ps1

- Crea el repo vía API (`private = $false`, i.e. **público**).
- Inicializa git (`init -b main`), commitea los archivos, pone el remote `origin` y hace `git push`.
- Validado sintácticamente: sin token imprime el mensaje "Necesitás un token..." y sale 1.

## Credenciales actuales

- git: user.name "Serkio Italo", user.email "ambrosio.italo@pucp.edu.pe". No hay token de GitHub configurado.
- `gh` CLI no está instalado; se usa el CLI de git.

## Historia breve

- El banco quedó en 229 preguntas tras la carga inicial del PDF; luego se completó a 400 parseando las preguntas faltantes (2025-II y 2026-II) desde el PDF oficial (Python/pdfplumber).
- Reset/Desmarcar está implementado; marcas en localStorage implementadas y verificadas.

## Próximos pasos

1. Dar el token (Classic PAT, scope `repo`) → ejecutar `subir_serums_banco.ps1` → pusheo a GitHub.
2. Activar GitHub Pages (Settings → Pages → main).
3. Probar desde el celular: `https://<usuario>.github.io/serums-banco/serums_banco.html`.
