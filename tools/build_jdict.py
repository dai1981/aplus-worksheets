# -*- coding: utf-8 -*-
"""
日本語辞書（/japanese/{L}/word/）を PHP + DB 方式にするためのデータを作る。
  python3 tools/build_jdict.py [JDICT_DIR]
入力: JDICT_DIR（既定 /home/claude/build/jdict）の make_jdict.py と data/ tr/（語のデータと各言語の訳）
出力:
  jdict/words/NNN.json            1ファイル 200語。DB の jd_word に入る（1語1行）
  site/japanese/_dict/inc/ju.json 画面の文言（12言語）
  site/japanese/{L}/word/index.html, row-*.html, index.json   辞書トップ・五十音の一覧・検索候補（静的のまま）
  site/japanese/sitemap-{L}.xml   単語ページのサイトマップ（言語ごと。/aplus/sitemap.php のインデックスに載せる）
  jdict/lastmod.json              語ごとの中身のハッシュと、最後に中身が変わった日（サイトマップの lastmod）
単語ページの HTML はここでは作らない（サーバーの PHP が DB から作る）。
"""
import datetime, hashlib, json, os, random, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
JD = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/build/jdict"
LANGS = ['en', 'vi', 'zh', 'tw', 'ko', 'id', 'es', 'pt', 'fr', 'de', 'ru', 'th', 'ar']
PER_FILE = 200

# make_jdict.py のデータ読み込み・ファイル名づけ・一覧ページを、そのまま使う（ページ生成の最後の部分は実行しない）
src = open(os.path.join(JD, "make_jdict.py"), encoding="utf-8").read()
src = src.split("\nonly = sys.argv")[0]
g = {"__file__": os.path.join(JD, "make_jdict.py"), "__name__": "jdict"}
exec(compile(src, "make_jdict.py", "exec"), g)
g["LANGS"][:] = LANGS
g["ROOT"] = os.path.join(REPO, "site")                  # 一覧ページの出力先
WORDS, slug, JU, BATCH, WIDX = g["WORDS"], g["slug"], g["JU"], g["BATCH"], g["WIDX"]


def pin_slugs():
    """公開済みの語の URL（slug）は変えない。新しい語だけ、空いている名前を make_jdict と同じ規則で付ける。
    これで、作成途中で公開しても、あとから足した語が既存の URL を押しのけることはない。"""
    import glob, re
    pinned = {}
    for f in glob.glob(os.path.join(REPO, "jdict", "words", "*.json")):
        for r in json.load(open(f, encoding="utf-8")):
            pinned[(r['w'], r['k'])] = r['s']
    S = g["SLUGS"]
    old = dict(S)
    used = {'index'} | {'row-' + r[0] for r in g["ROWS"]}
    new = {}
    for k, v in old.items():
        if k in pinned:
            new[k] = pinned[k]; used.add(pinned[k])
    sl = g["sl"]
    for w in sorted(WORDS, key=lambda x: (g["batch_order"](x['_b']), WIDX[id(x)])):
        k = (w['w'], w['kana'])
        if k in new:
            continue
        s0 = sl(w['romaji']) or 'w'; s = s0
        if s in used:
            gg = re.split(r'[,;/]', re.sub(r'\(.*?\)', '', w['senses'][0]['en']))[0]
            gg = re.sub(r'^(to|a|an|the) ', '', gg.strip().lower())
            gg = sl(' '.join(gg.split()[:2]))
            if not gg or gg == s0 or gg.startswith(s0 + '-'):
                gg = {'name': 'name', 'place': 'place', 'works': 'anime', 'anime': 'anime', 'slang': 'slang', 'culture': 'japan',
                      'grammar': 'grammar', 'brand': 'brand'}.get(w.get('cat'), 'w')
            s = f"{s0}-{gg}"
        n = 2
        while s in used:
            s = f'{s0}-{n}'; n += 1
        used.add(s); new[k] = s
    S.clear(); S.update(new)
    print("slugs: pinned", sum(1 for k in new if k in pinned), "new", sum(1 for k in new if k not in pinned))


pin_slugs()

Q_EX = {'en': 'What does this sentence mean?', 'vi': 'Câu này có nghĩa là gì?', 'zh': '这句话是什么意思？', 'tw': '這句話是什麼意思？',
        'ko': '이 문장은 무슨 뜻일까요?', 'id': 'Apa arti kalimat ini?', 'es': '¿Qué significa esta oración?', 'pt': 'O que significa esta frase?',
        'fr': 'Que signifie cette phrase ?', 'de': 'Was bedeutet dieser Satz?', 'ru': 'Что означает это предложение?', 'th': 'ประโยคนี้หมายความว่าอะไร', 'ar': 'ما معنى هذه الجملة؟'}
PREV = {'en': 'Previous', 'vi': 'Từ trước', 'zh': '上一个', 'tw': '上一個', 'ko': '이전 단어', 'id': 'Sebelumnya', 'es': 'Anterior', 'pt': 'Anterior',
        'fr': 'Précédent', 'de': 'Vorheriges', 'ru': 'Предыдущее', 'th': 'ก่อนหน้า', 'ar': 'السابق'}
NEXT = {'en': 'Next', 'vi': 'Từ tiếp theo', 'zh': '下一个', 'tw': '下一個', 'ko': '다음 단어', 'id': 'Berikutnya', 'es': 'Siguiente', 'pt': 'Próxima',
        'fr': 'Suivant', 'de': 'Nächstes', 'ru': 'Следующее', 'th': 'ถัดไป', 'ar': 'التالي'}


def quiz_data(w, L):
    """The same two questions as the old static pages (same random choices), plus a new third question
    about the meaning of the first example sentence. Choices are stored as word slugs (or kana for the
    reading question), so the page shows each word's meaning in the reader's language."""
    rnd = random.Random(w['w'] + w['kana'])
    others = [x for x in BATCH[w['_b']] if x is not w]
    if len(others) < 6:
        others = [x for x in WORDS[max(0, WIDX[id(w)] - 30):WIDX[id(w)] + 30] if x is not w]
    out = {}
    pool = [x for x in others if x['senses'][0][L] != w['senses'][0][L]]
    opts = [w] + rnd.sample(pool, 3)
    order = list(range(4)); rnd.shuffle(order)
    out['m'] = [[slug(opts[order[i]]) for i in range(4)], 'ABCD'[order.index(0)]]
    if w['w'] != w['kana']:
        pool = sorted({x['kana'] for x in others if x['kana'] != w['kana']})
        opts = [w['kana']] + rnd.sample(pool, 3)
        order = list(range(4)); rnd.shuffle(order)
        out['r'] = [[opts[order[i]] for i in range(4)], 'ABCD'[order.index(0)]]
    # 新しい3問目：例文の意味（他の語の1つ目の例文の訳から3つ）
    r3 = random.Random('ex|' + w['w'] + w['kana'])
    seen, pool = {w['ex'][0][L]}, []
    for x in others:
        if x['ex'] and x['ex'][0][L] not in seen:
            seen.add(x['ex'][0][L]); pool.append(x)
    if len(pool) >= 3:
        opts = [w] + r3.sample(pool, 3)
        order = list(range(4)); r3.shuffle(order)
        out['x'] = [[slug(opts[order[i]]) for i in range(4)], 'ABCD'[order.index(0)]]
    return out


def quiz_all(w):
    """Quiz for every language. Stored once under '*' plus only the languages whose choices differ."""
    qs = {L: quiz_data(w, L) for L in LANGS}
    out = {'*': qs['en']}
    for L in LANGS:
        if qs[L] != qs['en']:
            out[L] = qs[L]
    return out


def record(w, i):
    s = slug(w)
    def pick(d, keys):
        return {k: d[k] for k in keys if k in d}
    rel = lambda lst: [[x, slug(g["WMAP"][x]) if x in g["WMAP"] else None] for x in (lst or [])]
    near = [WORDS[j] for j in range(max(0, i - 3), min(len(WORDS), i + 4)) if WORDS[j] is not w][:6]
    return {
        "s": s, "w": w['w'], "k": w['kana'], "r": w['romaji'], "jlpt": w['jlpt'], "cat": w.get('cat') or '', "pos": w['pos'],
        "forms": w.get('forms') or '', "row": g["row_of"](w['kana']),
        "sen": [pick(x, ['en'] + LANGS) for x in w['senses']],
        "ex": [dict(pick(x, LANGS), ja=x['ja'], r=x['romaji']) for x in w['ex']],
        "ph": [dict(pick(x, LANGS), ja=x['ja']) for x in w['ph']],
        "note": pick(w['note'], LANGS),
        "kj": [[k['k'], k.get('on') or '', k.get('kun') or ''] for k in w.get('kanji', [])],
        "syn": rel(w.get('syn')), "ant": rel(w.get('ant')),
        "near": [slug(x) for x in near],
        "prev": slug(WORDS[i - 1]) if i > 0 else None, "next": slug(WORDS[i + 1]) if i + 1 < len(WORDS) else None,
        "quiz": quiz_all(w),
    }


def main():
    out_dir = os.path.join(REPO, "jdict", "words")
    os.makedirs(out_dir, exist_ok=True)
    recs = [record(w, i) for i, w in enumerate(WORDS)]
    assert len({r['s'] for r in recs}) == len(recs)
    for k in range(0, len(recs), PER_FILE):
        path = os.path.join(out_dir, "%03d.json" % (k // PER_FILE + 1))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(recs[k:k + PER_FILE], f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
    print("words:", len(recs), "files:", (len(recs) + PER_FILE - 1) // PER_FILE)

    # lastmod: 中身が変わった語だけ今日の日付にする
    lm_path = os.path.join(REPO, "jdict", "lastmod.json")
    old = json.load(open(lm_path)) if os.path.exists(lm_path) else {}
    today = datetime.date.today().isoformat()
    lm = {}
    for r in recs:
        h = hashlib.md5(json.dumps(r, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        lm[r['s']] = [h, old[r['s']][1] if r['s'] in old and old[r['s']][0] == h else today]
    json.dump(lm, open(lm_path, "w"), separators=(",", ":"), sort_keys=True)
    for L in LANGS:
        rows = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for r in sorted(recs, key=lambda x: x['s']):
            rows.append("  <url><loc>https://www.apu2.com/japanese/%s/word/%s.html</loc><lastmod>%s</lastmod></url>" % (L, r['s'], lm[r['s']][1]))
        rows.append("</urlset>")
        open(os.path.join(REPO, "site", "japanese", "sitemap-%s.xml" % L), "w").write("\n".join(rows) + "\n")
    print("sitemaps:", len(LANGS))

    ui = {}
    for L in LANGS:
        t = dict(JU[L]); t['q_ex'] = Q_EX[L]; t['prev'] = PREV[L]; t['next'] = NEXT[L]
        ui[L] = t
    meta = {"langs": LANGS, "hl": {k: g["HL"][k] for k in LANGS}, "og": {k: g["OG"][k] for k in LANGS}, "name": {k: g["NAME"][k] for k in LANGS},
            "hub": sorted(g["HUB"]), "jlearn": sorted(g["JLEARN"]), "priv": sorted(g["PRIV"]), "cat_en": JU['en']['cat'], "v": g["V"]}
    inc = os.path.join(REPO, "site", "japanese", "_dict", "inc")
    os.makedirs(inc, exist_ok=True)
    json.dump({"ui": ui, "meta": meta}, open(os.path.join(inc, "ju.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    for L in LANGS:                                     # 辞書トップ・五十音の一覧・検索候補
        g["index_pages"](L)
    print("index pages:", len(LANGS), "languages")


if __name__ == "__main__":
    main()
