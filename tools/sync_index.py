#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sincroniza index.html con serums_banco_data.js (fuente única de datos).

Hace, de forma idempotente:
  1. Re-embebe EXAMES (todos los exámenes del data.js) dentro de index.html.
  2. Regenera EXAM_LABELS (etiqueta + subtítulo por examen).
  3. Regenera los botones .chip del filtro de exámenes.
  4. Actualiza los textos de cabecera/pie con el conteo total.

Uso:
    python tools/sync_index.py

Después de cualquier `registro.py import`, correr esto y la app queda al día.
"""
import io
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(BASE, "serums_banco_data.js")
INDEX = os.path.join(BASE, "index.html")

# Etiquetas de presentación (label, subtítulo). El orden manda en las pestañas.
LABELS = {
    "2024-II-I": ("SERUMS 2024-II (Med. I)", "Medicina Humana · Examen 2024-II · Medicina I"),
    "2025-I":    ("SERUMS 2025-I", "Medicina Humana · Evaluación 06/04/2025"),
    "2025-II":   ("SERUMS 2025-II", "Medicina Humana · Evaluación 24/08/2025"),
    "2026-I":    ("SERUMS 2026-I", "Medicina Humana · Evaluación 19/04/2026"),
    "2026-II":   ("SERUMS 2026-II", "Medicina Humana · Evaluación 09/08/2026"),
}
ORDER = ["2024-II-I", "2025-I", "2025-II", "2026-I", "2026-II"]


def load_data():
    with io.open(DATA_JS, encoding="utf-8") as f:
        t = f.read()
    b, e = t.find("{"), t.rfind("}")
    return json.loads(t[b:e + 1])


def main():
    data = load_data()
    total = sum(len(v) for v in data.values())
    exams = [k for k in ORDER if k in data]
    exams += [k for k in data if k not in exams]
    # reordenar cronológicamente para que "Todas" respete el orden de las pestañas
    data = {k: data[k] for k in exams}

    with io.open(INDEX, encoding="utf-8") as f:
        t = f.read()

    # 1) EXAMES embebido
    i0 = t.index("const EXAMES = ")
    i1 = t.index("const EXAM_LABELS")
    compact = json.dumps(data, ensure_ascii=False)
    t = t[:i0] + "const EXAMES = " + compact + ";\n\n    " + t[i1:]

    # 2) EXAM_LABELS
    j0 = t.index("const EXAM_LABELS")
    j1 = t.index("const IA_CONTEXT")
    lines = ["const EXAM_LABELS = {"]
    for idx, k in enumerate(exams):
        lab, sub = LABELS.get(k, (k, "Medicina Humana"))
        lines.append('  "%s": {' % k)
        lines.append('    "label": "%s",' % lab)
        lines.append('    "sub": "%s"' % sub)
        lines.append("  }" + ("," if idx < len(exams) - 1 else ""))
    lines.append("};\n\n    ")
    t = t[:j0] + "\n".join(lines) + t[j1:]

    # 3) chips del filtro
    c0 = t.index('data-exam="todas">Todas</button>') + len('data-exam="todas">Todas</button>')
    c1 = t.index('<button class="chip reset-btn"')
    chips = [""]
    for k in exams:
        lab = LABELS.get(k, (k, ""))[0]
        chips.append('      <button class="chip" data-exam="%s">%s</button>' % (k, lab))
    chips.append("      ")
    t = t[:c0] + "\n".join(chips) + t[c1:]

    # 4) textos con el conteo
    t = re.sub(r"Evaluaciones 20\d\d[^\s·]*?20\d\d", "Evaluaciones 2024–2026", t)
    t = re.sub(r"Banco SERUMS Medicina Humana 20\d\d[–-]20\d\d",
               "Banco SERUMS Medicina Humana 2024–2026", t)
    t = re.sub(r"Banco completo · \d+ preguntas · Verificación [\d-]+",
               "Banco completo · %d preguntas · Verificación 2026-11-24" % total, t)
    t = re.sub(r">\d+ preguntas del banco · Fuente: MINSA",
               ">%d preguntas del banco · Fuente: MINSA" % total, t)

    with io.open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)

    print("index.html sincronizado:")
    for k in exams:
        print("  %-12s %3d" % (k, len(data[k])))
    print("  TOTAL        %3d" % total)


if __name__ == "__main__":
    main()
