# -*- coding: utf-8 -*-
"""Extrae preguntas de una página 'rendir' de examprazol (exámenes oficiales).

Uso:
  python tools/parse_examprazol.py <url> <salida.json> <exam_key> <fuente> <anio> [limite]
"""
import html
import io
import json
import re
import sys
import urllib.request


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        raw = r.read()
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:
            pass
    return raw.decode("utf-8", "ignore")


def clean(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def parse(html_text):
    text = re.sub(r"<!--.*?-->", "", html_text, flags=re.S)
    parts = re.split(r'<li id="p(\d+)"', text)
    out = []
    # parts[0] = antes; luego pares (num, bloque)
    for i in range(1, len(parts), 2):
        n = int(parts[i])
        block = parts[i + 1]
        m = re.search(
            r'<p class="font-anatomist-body[^"]*"><span class="font-semibold">\d+\.?</span>(.*?)</p>',
            block, re.S)
        if not m:
            continue
        stem = clean(m.group(1))
        opts = []
        for om in re.finditer(
                r'<button[^>]*><span class="font-semibold">([A-D])\.?</span>(.*?)</button>',
                block, re.S):
            letra = om.group(1)
            opts.append(letra + ". " + clean(om.group(2)))
        am = re.search(r"La correcta es\s+([A-D])", block)
        if not am:
            continue
        letra = am.group(1)
        texto = ""
        for o in opts:
            if o.startswith(letra + "."):
                texto = o[3:].strip()
        exp = ""
        em = re.search(r"La correcta es\s+[A-D]\.\s*(.*?)(?:</p>|</div>|$)", block, re.S)
        if em:
            exp = clean(em.group(1))
        if not exp or exp.startswith("Sin explicación"):
            exp = ""
        if len(opts) != 4:
            print("  [aviso] p%d tiene %d opciones" % (n, len(opts)))
            continue
        out.append({
            "n": n,
            "stem": stem,
            "opts": opts,
            "ans": {"letra": letra, "texto": texto},
            "meta": {"explicacion": exp},
        })
    return out


def main():
    url, salida, exam, fuente, anio = sys.argv[1:6]
    limite = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    qs = parse(fetch(url))
    qs.sort(key=lambda q: q["n"])
    if limite:
        qs = qs[:limite]
    payload = {
        "exam": exam,
        "meta": {
            "origen": "oficial",
            "fuente": fuente,
            "anio": int(anio),
            "verificado": "2026-11-24",
            "url": url,
        },
        "preguntas": qs,
    }
    with io.open(salida, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("Extraídas %d preguntas -> %s" % (len(qs), salida))


if __name__ == "__main__":
    main()
