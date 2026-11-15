# -*- coding: utf-8 -*-
"""
日本語辞書（/japanese/{L}/word/）のデータを作る。元データはこのリポジトリの中だけ（外のフォルダに頼らない）。

  python3 tools/build_jdict.py            公開済みの語 + 完成した新しいバッチ をまとめて書き出す
  python3 tools/build_jdict.py --check    書き出さずに、完成したバッチの数と語数だけ表示

入力:
  jdict/words/NNN.json                   公開済みの全語（13言語）。これが正本
  jdict/batches/BATCH/base.json          新しいバッチ（ja・en・vi・zh・ko）。作り方は jdict/BRIEF.md
  jdict/batches/BATCH/{id,es,pt,fr,de,ru,th,ar}.json   同じバッチの8言語の訳
    → 9ファイルがそろったバッチだけ取り込む。tw は zh から OpenCC（s2twp）で作る
出力:
  jdict/words/NNN.json（200語ずつ・五十音順）、jdict/lastmod.json
  site/japanese/{L}/word/index.json・index.html・row-*.html（語の一覧。既存のページの中身だけ差し替える）
  site/japanese/sitemap-{L}.xml、site/japanese/_dict/inc/ju.json の検索データの版（meta.v）

決まり:
  ・公開済みの語の URL（slug）と並び順は変えない。新しい語は五十音の位置に差し込む
  ・同じ見出し語＋読みがすでにあれば新しい方は取り込まない
  ・lastmod はその語自身の中身が変わったときだけ今日になる（近くの語・前後・クイズは比べない）
"""
import bisect, datetime, glob, hashlib, html, json, os, random, re, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
WDIR = os.path.join(REPO, "jdict", "words")
BDIR = os.path.join(REPO, "jdict", "batches")
SITE = os.path.join(REPO, "site", "japanese")
LANGS = ['en', 'vi', 'zh', 'tw', 'ko', 'id', 'es', 'pt', 'fr', 'de', 'ru', 'th', 'ar']
TR_LANGS = ['id', 'es', 'pt', 'fr', 'de', 'ru', 'th', 'ar']
BASE_LANGS = ['en', 'vi', 'zh', 'ko']
PER_FILE = 200
ROWS = [('a', 'あいうえおぁぃぅぇぉゔっ'), ('ka', 'かきくけこがぎぐげごゕゖ'), ('sa', 'さしすせそざじずぜぞ'),
        ('ta', 'たちつてとだぢづでど'), ('na', 'なにぬねの'), ('ha', 'はひふへほばびぶべぼぱぴぷぺぽ'),
        ('ma', 'まみむめも'), ('ya', 'やゆよゃゅょ'), ('ra', 'らりるれろ'), ('wa', 'わをんゎゐゑ')]
CAT_KEYS = ['anime', 'works', 'slang', 'place', 'name', 'culture', 'onoma', 'phrase', 'proverb', 'business',
            'everyday', 'grammar', 'brand']


def hira(s):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)


def row_of(k):
    c = hira(k)[:1]
    for r, cs in ROWS:
        if c in cs:
            return r
    return 'a'


def sl(r):
    return re.sub(r'[^a-z0-9]+', '-', r.lower()).strip('-')


def own_hash(r):
    own = {k: v for k, v in r.items() if k not in ('near', 'prev', 'next', 'quiz')}
    return hashlib.md5(json.dumps(own, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- 読み込み
def load_words():
    out = []
    for f in sorted(glob.glob(os.path.join(WDIR, "*.json"))):
        out.extend(json.load(open(f, encoding="utf-8")))
    return out


def complete_batches():
    """9ファイルがそろったバッチ名（名前順）"""
    out = []
    for d in sorted(glob.glob(os.path.join(BDIR, "*"))):
        if os.path.isfile(os.path.join(d, "base.json")) and all(os.path.isfile(os.path.join(d, L + ".json")) for L in TR_LANGS):
            out.append(os.path.basename(d))
    return out


def load_batch(name, to_tw):
    d = os.path.join(BDIR, name)
    base = json.load(open(os.path.join(d, "base.json"), encoding="utf-8"))
    tr = {L: json.load(open(os.path.join(d, L + ".json"), encoding="utf-8")) for L in TR_LANGS}
    recs = []
    for b in base:
        key = b['w'] + '|' + b['k']
        t = {L: tr[L].get(key) for L in TR_LANGS}
        miss = [L for L in TR_LANGS if not t[L]]
        if miss:
            raise SystemExit("%s: %s has no translation in %s" % (name, key, ",".join(miss)))
        def merge(items, part, with_r=False):
            res = []
            for i, x in enumerate(items):
                y = {L: x[L] for L in BASE_LANGS}
                y['tw'] = to_tw(x['zh'])
                for L in TR_LANGS:
                    y[L] = t[L][part][i]
                res.append(y)
            return res
        sen = merge(b['sen'], 'sen')
        ex = merge(b['ex'], 'ex')
        for i, x in enumerate(b['ex']):
            ex[i]['ja'] = x['ja']; ex[i]['r'] = x['r']
        ph = merge(b['ph'], 'ph')
        for i, x in enumerate(b['ph']):
            ph[i]['ja'] = x['ja']
        note = {L: b['note'][L] for L in BASE_LANGS}
        note['tw'] = to_tw(b['note']['zh'])
        for L in TR_LANGS:
            note[L] = t[L]['note']
        recs.append({
            "s": None, "w": b['w'], "k": b['k'], "r": b['r'], "jlpt": b.get('jlpt', ''), "cat": b.get('cat', ''),
            "pos": b['pos'], "forms": b.get('forms', ''), "row": row_of(b['k']),
            "sen": [{L: x[L] for L in LANGS} for x in sen],
            "ex": [dict({L: x[L] for L in LANGS}, ja=x['ja'], r=x['r']) for x in ex],
            "ph": [dict({L: x[L] for L in LANGS}, ja=x['ja']) for x in ph],
            "note": {L: note[L] for L in LANGS},
            "kj": [list(k) for k in b.get('kj', [])],
            "syn": [[x, None] for x in b.get('syn', [])], "ant": [[x, None] for x in b.get('ant', [])],
            "near": [], "prev": None, "next": None, "quiz": None, "_new": True,
        })
    return recs


# ---------------------------------------------------------------- 新しい語の slug・クイズ
def new_slug(r, used):
    s0 = sl(r['r']) or 'w'
    s = s0
    if s in used:
        gg = re.split(r'[,;/]', re.sub(r'\(.*?\)', '', r['sen'][0]['en']))[0]
        gg = re.sub(r'^(to|a|an|the) ', '', gg.strip().lower())
        gg = sl(' '.join(gg.split()[:2]))
        if not gg or gg == s0 or gg.startswith(s0 + '-'):
            gg = {'name': 'name', 'place': 'place', 'works': 'anime', 'anime': 'anime', 'slang': 'slang',
                  'culture': 'japan', 'grammar': 'grammar', 'brand': 'brand'}.get(r.get('cat'), 'w')
        s = "%s-%s" % (s0, gg)
    n = 2
    while s in used:
        s = "%s-%d" % (s0, n); n += 1
    used.add(s)
    return s


def quiz_for(w, others, L):
    """意味（m）・読み（r）・例文の意味（x）の3問。選択肢は近くの語から（固定の乱数で毎回同じ）"""
    rnd = random.Random(w['w'] + w['k'])
    out = {}
    pool = [x for x in others if x['sen'][0][L] != w['sen'][0][L]]
    opts = [w] + rnd.sample(pool, 3)
    order = list(range(4)); rnd.shuffle(order)
    out['m'] = [[opts[order[i]]['s'] for i in range(4)], 'ABCD'[order.index(0)]]
    if w['w'] != w['k']:
        kp = sorted({x['k'] for x in others if x['k'] != w['k']})
        opts = [w['k']] + rnd.sample(kp, 3)
        order = list(range(4)); rnd.shuffle(order)
        out['r'] = [[opts[order[i]] for i in range(4)], 'ABCD'[order.index(0)]]
    r3 = random.Random('ex|' + w['w'] + w['k'])
    seen, pool = {w['ex'][0][L]}, []
    for x in others:
        if x['ex'] and x['ex'][0][L] not in seen:
            seen.add(x['ex'][0][L]); pool.append(x)
    if len(pool) >= 3:
        opts = [w] + r3.sample(pool, 3)
        order = list(range(4)); r3.shuffle(order)
        out['x'] = [[opts[order[i]]['s'] for i in range(4)], 'ABCD'[order.index(0)]]
    return out


# ---------------------------------------------------------------- 一覧ページ（既存ページの中身だけ差し替え）
def grp(r):
    return r['jlpt'] or r['cat']


def mean(r, L):
    return '; '.join(x[L] for x in r['sen'][:2])


def esc(t):
    return html.escape(t)


def li(L, r):
    k = '<small lang="ja">%s</small>' % esc(r['k']) if r['k'] != r['w'] else ''
    return ('<li data-lv="%s"><a href="/japanese/%s/word/%s.html"><b lang="ja">%s%s</b><span>%s</span></a></li>'
            % (grp(r), L, r['s'], esc(r['w']), k, esc(mean(r, L))))


def write_lists(words, ver, cat_label):
    for L in LANGS:
        d = os.path.join(SITE, L, "word")
        idx = [[r['w'], r['s'], mean(r, L), r['k'], r['r']] for r in words]
        with open(os.path.join(d, "index.json"), "w", encoding="utf-8") as f:
            json.dump(idx, f, ensure_ascii=False, separators=(",", ":"))
        by_row = {}
        for r in words:
            by_row.setdefault(r['row'], []).append(r)
        for rw, _ in ROWS:
            p = os.path.join(d, "row-%s.html" % rw)
            if not os.path.exists(p):
                continue
            s = open(p, encoding="utf-8").read()
            items = by_row.get(rw, [])
            s = re.sub(r'(<div class="info-card"><ul class="wl">).*?(</ul>)', lambda m: m.group(1) + ''.join(li(L, r) for r in items) + m.group(2), s, count=1, flags=re.S)
            s = re.sub(r'(<div class="dict-hero"><h1>.*?</h1><p>)(\d+)', lambda m: m.group(1) + str(len(items)), s, count=1, flags=re.S)
            s = re.sub(r'data-v="\d+[a-z]?"', 'data-v="%s"' % ver, s)
            open(p, "w", encoding="utf-8").write(s)
        p = os.path.join(d, "index.html")
        s = open(p, encoding="utf-8").read()
        for rw, _ in ROWS:
            s = re.sub(r'(<a href="/japanese/%s/word/row-%s\.html"><b lang="ja">.</b><span>)(\d+)' % (L, rw),
                       lambda m: m.group(1) + str(len(by_row.get(rw, []))), s)
        cnt = {}
        for r in words:
            cnt[grp(r)] = cnt.get(grp(r), 0) + 1
        def jc(m):
            lab = html.unescape(m.group(1))
            g = lab[5:] if lab.startswith('JLPT N') else cat_label.get(L, {}).get(lab)
            return m.group(0) if g is None else '<span class="jcount">%s: %d</span>' % (m.group(1), cnt.get(g, 0))
        s = re.sub(r'<span class="jcount">(.*?): \d+</span>', jc, s)
        s = re.sub(r'data-v="\d+[a-z]?"', 'data-v="%s"' % ver, s)
        open(p, "w", encoding="utf-8").write(s)


# ---------------------------------------------------------------- 本体
def main():
    check = '--check' in sys.argv
    words = load_words()
    have = {(r['w'], r['k']) for r in words}
    names = complete_batches()
    new = []
    if names:
        import opencc
        cc = opencc.OpenCC('s2twp')
        for n in names:
            for r in load_batch(n, cc.convert):
                if (r['w'], r['k']) in have:
                    continue
                have.add((r['w'], r['k'])); new.append(r)
    print("published:", len(words), " complete batches:", len(names), " new words:", len(new))
    if check:
        return

    # 新しい語を五十音の位置に差し込む（公開済みの語どうしの並びは変えない）
    keys = [hira(r['k']) for r in words]
    for r in sorted(new, key=lambda x: (hira(x['k']), x['w'])):
        i = bisect.bisect_right(keys, hira(r['k']))
        words.insert(i, r); keys.insert(i, hira(r['k']))
    used = {r['s'] for r in words if r['s']} | {'index'} | {'row-' + x for x, _ in ROWS}
    for r in words:
        if not r['s']:
            r['s'] = new_slug(r, used)
    wmap = {}
    for r in words:
        wmap.setdefault(r['w'], r['s'])
    for i, r in enumerate(words):
        r['near'] = [words[j]['s'] for j in range(max(0, i - 3), min(len(words), i + 4)) if j != i][:6]
        r['prev'] = words[i - 1]['s'] if i > 0 else None
        r['next'] = words[i + 1]['s'] if i + 1 < len(words) else None
        for k in ('syn', 'ant'):
            r[k] = [[x[0], x[1] or wmap.get(x[0])] for x in r[k]]
    for i, r in enumerate(words):
        if r.pop('_new', False):
            others = [x for x in words[max(0, i - 30):i + 31] if x is not r]
            qs = {L: quiz_for(r, others, L) for L in LANGS}
            r['quiz'] = {'*': qs['en']}
            for L in LANGS:
                if qs[L] != qs['en']:
                    r['quiz'][L] = qs[L]
    assert len({r['s'] for r in words}) == len(words)

    for f in glob.glob(os.path.join(WDIR, "*.json")):
        os.remove(f)
    for k in range(0, len(words), PER_FILE):
        with open(os.path.join(WDIR, "%03d.json" % (k // PER_FILE + 1)), "w", encoding="utf-8") as f:
            json.dump(words[k:k + PER_FILE], f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")

    lm_path = os.path.join(REPO, "jdict", "lastmod.json")
    old = json.load(open(lm_path))
    today = datetime.date.today().isoformat()
    lm = {'__v': 2}
    for r in words:
        h = own_hash(r)
        o = old.get(r['s'])
        lm[r['s']] = [h, o[1] if o and o[0] == h else today]
    json.dump(lm, open(lm_path, "w"), separators=(",", ":"), sort_keys=True)
    for L in LANGS:
        rows = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for s in sorted(r['s'] for r in words):
            rows.append("  <url><loc>https://www.apu2.com/japanese/%s/word/%s.html</loc><lastmod>%s</lastmod></url>" % (L, s, lm[s][1]))
        rows.append("</urlset>")
        open(os.path.join(SITE, "sitemap-%s.xml" % L), "w").write("\n".join(rows) + "\n")

    ju_path = os.path.join(SITE, "_dict", "inc", "ju.json")
    ju = json.load(open(ju_path, encoding="utf-8"))
    ver = datetime.date.today().strftime("%Y%m%d") + "a"
    if new:
        ju['meta']['v'] = ver
        json.dump(ju, open(ju_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    else:
        ver = ju['meta']['v']
    cat_label = {L: {html.unescape(v): k for k, v in ju['ui'][L]['cat'].items()} for L in LANGS}
    write_lists(words, ver, cat_label)
    print("words:", len(words), " files:", (len(words) + PER_FILE - 1) // PER_FILE, " new:", len(new))


if __name__ == "__main__":
    main()
