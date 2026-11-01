# -*- coding: utf-8 -*-
"""
Build an "add units" SQL file that touches only ws_unit (REPLACE INTO, safe to re-run).
  python tools/build_add.py OUT.sql us/math/grade-3/fractions us/math/grade-3/telling-time ...
Each argument is a content path without .json.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_sql import row, jdump

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def unit_row(u):
    return row("ws_unit", {
        "country": u["country"], "subject": u["subject"], "grade": u["grade"], "slug": u["slug"],
        "title": u["title"], "seo_title": u.get("seo_title", ""), "short_title": u.get("short_title", ""),
        "domain": u.get("domain", ""), "standard_code": u.get("standard_code", ""),
        "standard_url": u.get("standard_url", ""), "standard_text": u.get("standard_text", ""),
        "meta_desc": u.get("meta_desc", ""), "key_big": u.get("key_big", ""), "key_sub": u.get("key_sub", ""),
        "body_html": u.get("body_html", ""), "faq_json": jdump(u.get("faq", [])), "sets_json": jdump(u["sets"]),
        "pdf_url": u.get("pdf_url", ""), "sort": u.get("sort", 0), "updated": u.get("updated"),
    })


def main():
    out_path, items = sys.argv[1], sys.argv[2:]
    lines = ["-- Aplus worksheets: add / update units (changes only the ws_unit table)", "SET NAMES utf8mb4;"]
    for it in items:
        with open(os.path.join(ROOT, "content", it + ".json"), encoding="utf-8") as f:
            u = json.load(f)
        for s in u["sets"]:
            for q in s["items"]:
                assert len(q["c"]) == 4 and 0 <= q["a"] < 4
        lines.append(unit_row(u))
        print("  +", it, "(sort %s)" % u.get("sort"))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", out_path, os.path.getsize(out_path) // 1024, "KB")


if __name__ == "__main__":
    main()
