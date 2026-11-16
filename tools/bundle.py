#!/usr/bin/env python3
"""Unpack / repack the __bundler/template island of index.html.

  python3 tools/bundle.py unpack   # index.html -> build/template.html
  python3 tools/bundle.py pack     # build/template.html -> index.html
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "build" / "template.html"
PAT = re.compile(r'(<script type="__bundler/template"[^>]*>)(.*?)(</script>)', re.S)

def main():
    doc = SRC.read_text(encoding="utf-8")
    m = PAT.search(doc)
    if not m:
        sys.exit("template island not found")
    if sys.argv[1:] == ["unpack"]:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(json.loads(m.group(2)), encoding="utf-8")
        print("wrote", OUT)
    elif sys.argv[1:] == ["pack"]:
        payload = json.dumps(OUT.read_text(encoding="utf-8"), ensure_ascii=False)
        payload = payload.replace("</", "<\\/")
        SRC.write_text(doc[:m.start(2)] + payload + doc[m.end(2):], encoding="utf-8")
        print("packed", len(payload), "bytes")
    else:
        sys.exit(__doc__)
main()
