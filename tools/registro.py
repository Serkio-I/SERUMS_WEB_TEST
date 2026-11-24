#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Registro anti-solape del Banco SERUMS / ENCAPS.

Uso:
    python tools/registro.py build
    python tools/registro.py stats
    python tools/registro.py check
    python tools/registro.py import ruta/al/archivo_nuevas.json

- `build`   : (re)construye banco_registro.json a partir de serums_banco_data.js
- `stats`   : muestra conteos por origen / examen
- `check`   : detecta duplicados (misma huella) dentro del banco
- `import`  : agrega preguntas nuevas al banco y al registro, saltando duplicados

Formato del JSON de importación:
{
  "exam": "SIM-2026",
  "meta": {"origen": "simulacro", "fuente": "...", "anio": 2026,
           "verificado": "2026-11-24"},
  "preguntas": [
    {"n": 1, "stem": "...",
     "opts": ["A. ...", "B. ...", "C. ...", "D. ..."],
     "ans": {"letra": "B", "texto": "..."},
     "meta": {"area": "...", "tema": "...", "ref": "..."}}
  ]
}

La huella (fingerprint) se calcula sobre el enunciado normalizado
(minúsculas, sin tildes, sin signos, espacios colapsados) con SHA-1.
"""
import argparse
import hashlib
import io
import json
import os
import re
import sys
import unicodedata
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(BASE, "serums_banco_data.js")
REGISTRO = os.path.join(BASE, "banco_registro.json")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def fp(stem):
    return hashlib.sha1(norm(stem).encode("utf-8")).hexdigest()


def load_data():
    with io.open(DATA_JS, encoding="utf-8") as f:
        t = f.read()
    b, e = t.find("{"), t.rfind("}")
    return json.loads(t[b:e + 1])


def save_data(data):
    body = json.dumps(data, ensure_ascii=False, indent=2)
    with io.open(DATA_JS, "w", encoding="utf-8", newline="\n") as f:
        f.write("// Banco SERUMS Medicina Humana - preguntas y claves\n")
        f.write("const EXAMES = " + body + ";\n")


def load_registro():
    if not os.path.exists(REGISTRO):
        return {"version": 1, "fingerprint_algo": "sha1(norm(stem))",
                "items": {}}
    with io.open(REGISTRO, encoding="utf-8") as f:
        return json.load(f)


def save_registro(reg):
    reg["updated"] = date.today().isoformat()
    items = reg["items"]
    counts = {"total": len(items)}
    for it in items.values():
        counts[it.get("origin", "?")] = counts.get(it.get("origin", "?"), 0) + 1
    reg["counts"] = counts
    with io.open(REGISTRO, "w", encoding="utf-8", newline="\n") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


def cmd_build(_args):
    data = load_data()
    reg = {"version": 1, "fingerprint_algo": "sha1(norm(stem))",
           "items": {}}
    dup = 0
    for exam, qs in data.items():
        for q in qs:
            h = fp(q["stem"])
            if h in reg["items"]:
                dup += 1
                print("  [dup] %s n=%s" % (exam, q.get("n")))
                continue
            meta = q.get("meta", {})
            reg["items"][h] = {
                "id": "%s-%03d" % (exam, q.get("n", 0)),
                "origin": meta.get("origen", "oficial"),
                "source": meta.get("fuente", "MINSA - SERUMS " + exam),
                "exam": exam,
                "n": q.get("n"),
                "area": meta.get("area"),
                "tema": meta.get("tema"),
                "ref": meta.get("ref"),
                "status": meta.get("status", "verificada"),
                "added": meta.get("added", "2026-11-20"),
                "preview": q["stem"][:110],
            }
    save_registro(reg)
    print("Registro reconstruido: %d preguntas, %d duplicados saltados."
          % (len(reg["items"]), dup))


def cmd_stats(_args):
    reg = load_registro()
    items = reg["items"].values()
    print("Total registrado: %d" % len(reg["items"]))
    by = {}
    for it in items:
        by.setdefault(it.get("origin", "?"), {}).setdefault(
            it.get("exam", "?"), 0)
        by[it["origin"]][it["exam"]] += 1
    for origin in sorted(by):
        print("\n[%s]" % origin)
        for exam in sorted(by[origin]):
            print("  %-12s %3d" % (exam, by[origin][exam]))


def cmd_check(_args):
    data = load_data()
    seen = {}
    dups = 0
    for exam, qs in data.items():
        for q in qs:
            h = fp(q["stem"])
            if h in seen:
                dups += 1
                print("DUPLICADO: %s n=%s == %s n=%s"
                      % (exam, q.get("n"), seen[h][0], seen[h][1]))
            else:
                seen[h] = (exam, q.get("n"))
    print("Revisadas %d preguntas, %d duplicados." % (sum(len(v) for v in data.values()), dups))


def cmd_import(args):
    with io.open(args.archivo, encoding="utf-8") as f:
        payload = json.load(f)

    exam = payload["exam"]
    base_meta = payload.get("meta", {})
    nuevas = payload.get("preguntas", [])
    if not nuevas:
        print("No hay preguntas en el archivo.")
        return 1

    data = load_data()
    reg = load_registro()
    existentes = set(reg["items"].keys())
    # también huellas de lo que ya está en data.js (por si el registro quedó viejo)
    for qs in data.values():
        for q in qs:
            existentes.add(fp(q["stem"]))

    destino = data.setdefault(exam, [])
    usados = {q.get("n") for q in destino}
    siguiente_n = max(usados) + 1 if usados else 1

    agregadas, saltadas = 0, 0
    for q in nuevas:
        h = fp(q["stem"])
        if h in existentes:
            saltadas += 1
            print("  [skip dup] %s" % q["stem"][:70])
            continue
        n = q.get("n")
        if not n or n in usados:
            n = siguiente_n
            siguiente_n += 1
        q["n"] = n
        usados.add(n)
        q.setdefault("meta", {})
        for k, v in base_meta.items():
            q["meta"].setdefault(k, v)
        q["meta"].setdefault("status", "verificada")
        q["meta"].setdefault("added", date.today().isoformat())
        destino.append(q)
        existentes.add(h)
        reg["items"][h] = {
            "id": "%s-%03d" % (exam, n),
            "origin": q["meta"].get("origen", "?"),
            "source": q["meta"].get("fuente", "?"),
            "exam": exam,
            "n": n,
            "area": q["meta"].get("area"),
            "tema": q["meta"].get("tema"),
            "ref": q["meta"].get("ref"),
            "status": q["meta"].get("status", "verificada"),
            "added": q["meta"].get("added"),
            "preview": q["stem"][:110],
        }
        agregadas += 1

    save_data(data)
    save_registro(reg)
    print("\nImportadas: %d | Saltadas por duplicado: %d | Total examen %s: %d"
          % (agregadas, saltadas, exam, len(destino)))
    print("Total banco: %d" % sum(len(v) for v in data.values()))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Registro anti-solape del banco SERUMS")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    p = sub.add_parser("import")
    p.add_argument("archivo")
    p.set_defaults(fn=cmd_import)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
