# -*- coding: utf-8 -*-
"""
新しい辞書バッチ（jdict/batches/BATCH/）の検査。
  python3 tools/jdict_check.py BATCH [BATCH ...]     エラーがあれば終了コード 1
  python3 tools/jdict_check.py --all                  jdict/batches の全部
"""
import glob, json, os, re, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BASE_LANGS = ['en', 'vi', 'zh', 'ko']
TR_LANGS = ['id', 'es', 'pt', 'fr', 'de', 'ru', 'th', 'ar']
RUBY = re.compile(r'([㐀-鿿豈-﫿々〆ヶケ0-9０-９]+)\[([^\]]+)\]')
KANJI = re.compile(r'[㐀-鿿豈-﫿々〆]')
SCRIPT = {'cyr': re.compile(r'[Ѐ-ӿ]'), 'hangul': re.compile(r'[가-힯]'),
          'thai': re.compile(r'[฀-๿]'), 'arabic': re.compile(r'[؀-ۿ]')}
OWN = {'ru': 'cyr', 'ko': 'hangul', 'th': 'thai', 'ar': 'arabic'}


def check(name):
    errs = []
    d = os.path.join(REPO, "jdict", "batches", name)
    todo_p = os.path.join(REPO, "jdict", "todo", name + ".json")
    try:
        base = json.load(open(os.path.join(d, "base.json"), encoding="utf-8"))
    except Exception as e:
        return ["base.json: %s" % e]
    todo = json.load(open(todo_p, encoding="utf-8")) if os.path.exists(todo_p) else None
    if todo is not None and len(base) != len(todo):
        errs.append("base.json has %d words, todo has %d (say in the reply which were skipped and why)" % (len(base), len(todo)))
    tr = {}
    for L in TR_LANGS:
        try:
            tr[L] = json.load(open(os.path.join(d, L + ".json"), encoding="utf-8"))
        except Exception as e:
            errs.append("%s.json: %s" % (L, e))
    seen = set()

    def text(where, t, L):
        if not isinstance(t, str) or not t.strip():
            errs.append("%s: empty" % where); return
        for sc, rx in SCRIPT.items():
            if rx.search(t) and OWN.get(L) != sc:
                errs.append("%s: has %s letters" % (where, sc))

    def furi(where, ja):
        if not isinstance(ja, str) or not ja.strip():
            errs.append("%s: empty Japanese" % where); return
        rest = RUBY.sub('', ja)
        if KANJI.search(rest):
            errs.append("%s: kanji without [reading]: %s" % (where, ja))

    for i, b in enumerate(base):
        key = "%s|%s" % (b.get('w'), b.get('k'))
        at = "%s #%d %s" % (name, i + 1, key)
        if key in seen:
            errs.append("%s: duplicate" % at)
        seen.add(key)
        for f in ('w', 'k', 'r', 'cat', 'pos', 'sen', 'ex', 'ph', 'note', 'kj', 'syn', 'ant'):
            if f not in b:
                errs.append("%s: missing %s" % (at, f))
        if errs and errs[-1].startswith(at + ": missing"):
            continue
        if not (1 <= len(b['sen']) <= 3): errs.append("%s: sen must have 1-3 items" % at)
        if len(b['ex']) != 2: errs.append("%s: ex must have 2 items" % at)
        if not (2 <= len(b['ph']) <= 3): errs.append("%s: ph must have 2-3 items" % at)
        if KANJI.search(b['w']) and not b['kj']: errs.append("%s: kj is empty" % at)
        for j, x in enumerate(b['sen']):
            for L in BASE_LANGS: text("%s sen%d.%s" % (at, j, L), x.get(L), L)
        for j, x in enumerate(b['ex']):
            furi("%s ex%d" % (at, j), x.get('ja'))
            if not x.get('r'): errs.append("%s ex%d: no romaji" % (at, j))
            for L in BASE_LANGS: text("%s ex%d.%s" % (at, j, L), x.get(L), L)
        for j, x in enumerate(b['ph']):
            furi("%s ph%d" % (at, j), x.get('ja'))
            for L in BASE_LANGS: text("%s ph%d.%s" % (at, j, L), x.get(L), L)
        for L in BASE_LANGS: text("%s note.%s" % (at, L), b['note'].get(L), L)
        for L in TR_LANGS:
            if L not in tr: continue
            t = tr[L].get(key)
            if not t:
                errs.append("%s: missing in %s.json" % (at, L)); continue
            for part in ('sen', 'ex', 'ph'):
                if len(t.get(part, [])) != len(b[part]):
                    errs.append("%s %s.%s: %d items, base has %d" % (at, L, part, len(t.get(part, [])), len(b[part])))
                for j, s in enumerate(t.get(part, [])):
                    text("%s %s.%s%d" % (at, L, part, j), s, L)
            text("%s %s.note" % (at, L), t.get('note'), L)
    for L in tr:
        extra = set(tr[L]) - seen
        if extra: errs.append("%s.json: keys not in base.json: %s" % (L, ", ".join(sorted(extra))[:200]))
    return errs


def main():
    names = sys.argv[1:]
    if names == ['--all']:
        names = sorted(os.path.basename(x) for x in glob.glob(os.path.join(REPO, "jdict", "batches", "*")))
    bad = 0
    for n in names:
        e = check(n)
        print("%s: %s" % (n, "OK" if not e else "%d error(s)" % len(e)))
        for x in e[:60]:
            print("  " + x)
        bad += len(e)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
