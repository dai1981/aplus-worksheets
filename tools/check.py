# -*- coding: utf-8 -*-
"""
content/ の JSON を公開前にチェックする（GitHub Actions でも毎回実行）。
エラーが1つでもあればアップロードもDB更新も止まる。

  python tools/check.py
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "..", "content")
KEY = re.compile(r"^[a-z0-9-]{1,80}$")
NEED = ["country", "subject", "grade", "slug", "title", "short_title", "domain",
        "meta_desc", "key_big", "body_html", "sets"]
# 過去に実際に出た文法ミス
BAD = [(re.compile(r"\b1 (minutes|hours|pencils|marks|apples|books|days|cups)\b"), "singular after 1"),
       (re.compile(r"\.\.(?!\.)"), "double period"),
       (re.compile(r"\b\d{1,2}:6\d\b"), "time like 9:60")]


def text(s):
    return re.sub(r"<[^>]+>", " ", s or "")


def main():
    errs, warns = [], []
    cat = json.load(open(os.path.join(CONTENT, "catalog.json"), encoding="utf-8"))
    grades = {(g["country"], g["subject"], g["slug"]) for g in cat["grades"]}
    seen = {}
    for p in sorted(glob.glob(os.path.join(CONTENT, "**", "*.json"), recursive=True)):
        if os.path.basename(p) == "catalog.json":
            continue
        rel = os.path.relpath(p, CONTENT)
        try:
            u = json.load(open(p, encoding="utf-8"))
        except ValueError as e:
            errs.append("%s: JSON error %s" % (rel, e)); continue
        for k in NEED:
            if not u.get(k):
                errs.append("%s: missing %s" % (rel, k))
        for k in ("country", "subject", "grade", "slug"):
            if not KEY.match(str(u.get(k, ""))):
                errs.append("%s: bad %s" % (rel, k))
        if (u.get("country"), u.get("subject"), u.get("grade")) not in grades:
            errs.append("%s: grade not in catalog.json" % rel)
        want = "/".join([u.get("country", ""), u.get("subject", ""), u.get("grade", ""), u.get("slug", "")]) + ".json"
        if rel.replace(os.sep, "/") != want:
            errs.append("%s: file path must be %s" % (rel, want))
        key = want
        if key in seen:
            errs.append("%s: duplicate of %s" % (rel, seen[key]))
        seen[key] = rel
        sets = u.get("sets") or []
        if len(sets) != 5:
            errs.append("%s: needs 5 sets (has %d)" % (rel, len(sets)))
        allq = []
        for si, s in enumerate(sets):
            items = s.get("items") or []
            if len(items) != 20:
                errs.append("%s set %d: needs 20 questions (has %d)" % (rel, si + 1, len(items)))
            for qi, it in enumerate(items):
                where = "%s set %d q%d" % (rel, si + 1, qi + 1)
                c = it.get("c") or []
                if len(c) != 4:
                    errs.append(where + ": needs 4 choices")
                elif len({text(x).strip() for x in c}) != 4:
                    errs.append(where + ": duplicate choices")
                if not isinstance(it.get("a"), int) or not 0 <= it["a"] < 4:
                    errs.append(where + ": bad answer index")
                if not it.get("q"):
                    errs.append(where + ": empty question")
                if "\\" in json.dumps(it, ensure_ascii=False).replace("\\\"", ""):
                    errs.append(where + ": backslash (use single quotes in HTML)")
                allq.append(text(it.get("q")) + " | " + " | ".join(text(x) for x in c))
                for rx, name in BAD:
                    if name and rx.search(allq[-1]):
                        warns.append("%s: %s" % (where, name))
        qs = [json.dumps([it.get("q"), it.get("c")]) for s in sets for it in (s.get("items") or [])]
        dup = len(qs) - len(set(qs))
        if dup:
            warns.append("%s: %d repeated question(s)" % (rel, dup))
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    print("checked %d unit(s): %d error(s), %d warning(s)" % (len(seen), len(errs), len(warns)))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
