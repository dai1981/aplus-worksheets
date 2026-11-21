# -*- coding: utf-8 -*-
"""
Deutschland (Grundschule, KMK-Bildungsstandards Mathematik Primarbereich) の単元生成の共通部品。
・文はドイツ語。子ども向けに短い文、du で話しかける
・数: 4 けたまではそのまま（1000）、5 けた以上は 10 000（ノーブレークスペース）。小数はコンマ（2,50 €）
・記号: 3 · 4（mal）、12 : 3（geteilt）、17 : 5 = 3 Rest 2
・お金: 3,50 €、45 ct
・HTML の属性はシングルクォート、バックスラッシュなし（check.py と同じルール）
・答えも誤答もすべてコードで計算する
"""
import math, re
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)

UPDATED = "2026-11-21"
STD_URL = ("https://www.kmk.org/fileadmin/Dateien/veroeffentlichungen_beschluesse/2022/"
           "2022_06_23-Bista-Primarbereich-Mathe.pdf")
STD_URL_SEK = ("https://www.kmk.org/fileadmin/Dateien/veroeffentlichungen_beschluesse/2022/"
               "2022_06_23-Bista-ESA-MSA-Mathe.pdf")
SEK = {"klasse-%d" % n for n in range(5, 11)}
# Leitideen der Bildungsstandards (Fassung 2022)
DOMAIN = {
    "F": "Funktionaler Zusammenhang",
    "Z": "Zahl und Operation",
    "R": "Raum und Form",
    "M": "Muster, Strukturen und funktionaler Zusammenhang",
    "G": "Größen und Messen",
    "D": "Daten und Zufall",
}
GIRLS = ["Emma", "Mia", "Hannah", "Sophia", "Lena", "Marie", "Anna", "Lina", "Clara", "Ida", "Paula", "Aylin", "Frieda", "Leni"]
BOYS = ["Ben", "Paul", "Leon", "Finn", "Elias", "Felix", "Jonas", "Emil", "Max", "Anton", "Theo", "Moritz", "Yusuf", "Luca"]
NB = " "
MAL = "·"
GETEILT = ":"


# ------------------------------------------------------------ numbers
def num(n):
    """1000、10 000、250 000（5 けた以上はノーブレークスペースで区切る）"""
    n = int(n)
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return ("−" if n < 0 else "") + s


def dez(v, places=None):
    """Dezimalzahl mit Komma: 2,5 / 1,25（places を指定すると桁をそろえる）"""
    if places is None:
        s = ("%.3f" % v).rstrip("0").rstrip(".")
    else:
        s = ("%." + str(places) + "f") % v
    ip, _, fp = s.partition(".")
    return num(int(ip)) + ("," + fp if fp else "")


def eur(cents, ct=False):
    """Geld: 350 → 3,50 €、300 → 3 €、45 → 45 ct（ct=True のとき 1 € 未満を ct で）"""
    cents = int(cents)
    if ct and cents < 100:
        return "%d%sct" % (cents, NB)
    e, c = divmod(cents, 100)
    if c == 0:
        return "%s%s€" % (num(e), NB)
    return "%s,%02d%s€" % (num(e), c, NB)


def unit(v, u):
    return "%s%s%s" % (num(v) if isinstance(v, int) else v, NB, u)


# ------------------------------------------------------------ names
class Kids:
    """Namen mit Geschlecht: next() → (Name, 'sie'|'er')"""

    def __init__(self, rnd):
        self.pool = [(n, "sie") for n in GIRLS] + [(n, "er") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def two(self):
        a = self.next()
        b = self.next()
        while b[0] == a[0]:
            b = self.next()
        return a, b


def Er(p):
    return p[1].capitalize()


# ------------------------------------------------------------ questions
def mcq(q, correct, cands, e, neg=False):
    """4 択：正解＋重複しない誤答 3 つ（文字列で比べる）。並びは balance() で決める。
    足りないときは答えの数を ±1、±2 … した近い数で補う。"""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or (not neg and (c.startswith("-") or c.startswith("−"))):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3 and "<" not in correct:
        m = re.match(r"^(.*?)(\d(?:\d|\u00a0(?=\d))*(?:,\d+)?)([^\d]*)$", correct)
        if m:
            raw = m.group(2).replace(NB, "")
            places = len(raw.split(",")[1]) if "," in raw else 0
            v = int(raw.replace(",", ""))
            for d in (1, -1, 2, -2, 3, 10, -10):
                nv = v + d
                if nv <= 0:
                    continue
                body = num(nv) if places == 0 else "%s,%s" % (num(nv // 10 ** places), str(nv % 10 ** places).rjust(places, "0"))
                c = "%s%s%s" % (m.group(1), body, m.group(3))
                if c not in seen:
                    seen.add(c)
                    pick.append(c)
                if len(pick) == 3:
                    break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def pick_unique(rnd, maker, n, seen=None, tries=6000):
    """maker() を呼んで、問題文が重ならない n 問を集める（seen を渡すと単元全体で重ならない）"""
    out = []
    seen = set() if seen is None else seen
    for _ in range(tries):
        try:
            it = maker()
        except (ValueError, IndexError, ZeroDivisionError):
            continue
        if it is None:
            continue
        k = re.sub(r"\s+", " ", it["q"])
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
        if len(out) == n:
            return out
    raise AssertionError("could not make %d unique questions (%d)" % (n, len(out)))


def mix(rnd, seen, parts):
    """parts: [(maker, n)] を集めて混ぜる（同じセットの中で種類が交互に出る）"""
    out = []
    for mk, n in parts:
        out += pick_unique(rnd, mk, n, seen)
    rnd.shuffle(out)
    return out


# ------------------------------------------------------------ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ("<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead>"
            "<tbody>%s</tbody></table></div>" % (h, b))


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Beispiel</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Lösung: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html：So geht's → Beispiele → Typische Fehler（kurze Sätze）"""
    h = "<h2>So geht's</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(examples)
    h += "<h2>Typische Fehler</h2>" + table(["Typischer Fehler", "So ist es richtig"], mist)
    return h


def plain_text(t):
    t = re.sub(r"<span class='fr'><span class='fn'>(.*?)</span><span class='fd'>([^<]*)</span></span>", r"\1/\2", t)
    assert not re.search(r"<[a-zA-Z/]", t), t
    return t


def make_unit(rnd, slug, dom, std_text, title, seo_title, short_title, meta_desc,
              key_big, key_sub, body_html, faq, sets, sort, grade="klasse-3"):
    """sets: [(Rundenname, [items x20])] を balance して書き出す"""
    sets = [{"title": t, "items": items} for t, items in sets]
    assert len(sets) == 5, slug
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
        for it in s["items"]:
            k = re.sub(r"\s+", " ", it["q"])
            assert k not in allq, ("duplicate question", slug, k)
            allq.add(k)
    balance(sets, rnd)
    title, seo_title, short_title, meta_desc, key_big, key_sub = map(plain_text, (title, seo_title, short_title, meta_desc, key_big, key_sub))
    write_unit("de", "mathe", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": DOMAIN[dom], "standard_code": "Leitidee " + DOMAIN[dom], "standard_url": STD_URL_SEK if grade in SEK else STD_URL,
        "standard_text": std_text, "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": faq, "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


# ------------------------------------------------------------ pictures
def wrap(w, h, body, label, lg=False):
    s = svg_wrap(int(w), int(h), body, label)
    if lg:
        s = s.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(s)


def zahlenstrahl(lo, hi, step, marks=(), labels=None, label="Zahlenstrahl", every=None, width=460):
    """Zahlenstrahl von lo bis hi mit Strichen alle step. marks: [(Wert, Buchstabe)] als Pfeile.
    labels: Werte, die unter dem Strich stehen (Standard: lo, hi und alle every)"""
    n = (hi - lo) // step
    u = width / float(n)
    lv = labels if labels is not None else [lo, hi]
    x0, y = max(24, 5 + 4.4 * max(len(num(v)) for v in lv)), 58
    X = lambda v: x0 + (v - lo) / float(step) * u
    s = [line(x0 - 8, y, x0 + n * u + 12, y, INK, 2),
         "<path d='M%.1f %.1f l-9 -6 v12 Z' fill='%s'/>" % (x0 + n * u + 20, y, INK)]
    big = every or (step * 10 if n >= 20 else step * 5 if n >= 10 else step)
    for i in range(n + 1):
        v = lo + i * step
        long = (v - lo) % big == 0
        s.append(line(X(v), y - (10 if long else 6), X(v), y + (10 if long else 6), INK, 2 if long else 1.3))
    for v in (labels if labels is not None else [lo + i * big for i in range((hi - lo) // big + 1)]):
        s.append(text(X(v), y + 30, num(v), 14, weight=600))
    for v, ch in marks:
        s.append("<path d='M%.1f %.1f l-7 -12 h14 Z' fill='%s'/>" % (X(v), y - 12, RED))
        s.append(text(X(v), y - 28, ch, 16, col=RED))
    return wrap(x0 * 2 + n * u + 4, y + 42, "".join(s), label, lg=True)


def stellenwerttafel(h, z, e, t=None):
    """Stellenwerttafel als HTML-Tabelle (T H Z E)"""
    head = (["T"] if t is not None else []) + ["H", "Z", "E"]
    row = ([str(t)] if t is not None else []) + [str(h), str(z), str(e)]
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead>"
            "<tbody><tr>%s</tr></tbody></table>" % ("".join("<th>%s</th>" % c for c in head),
                                                   "".join("<td style='text-align:center;min-width:34px'>%s</td>" % c for c in row)))


def dienes(h, z, e, label=None):
    """Hunderterplatten, Zehnerstangen und Einerwürfel"""
    s, x = [], 8
    for _ in range(h):
        s.append("<rect x='%d' y='8' width='50' height='50' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, FILL, GREEN))
        for k in range(1, 10):
            s.append(line(x + k * 5, 8, x + k * 5, 58, GREEN, 0.5))
            s.append(line(x, 8 + k * 5, x + 50, 8 + k * 5, GREEN, 0.5))
        x += 58
    for _ in range(z):
        s.append("<rect x='%d' y='8' width='6' height='50' fill='#f2c94c' stroke='%s' stroke-width='1.2'/>" % (x, INK))
        for k in range(1, 10):
            s.append(line(x, 8 + k * 5, x + 6, 8 + k * 5, INK, 0.5))
        x += 10
    if z:
        x += 6
    for i in range(e):
        s.append("<rect x='%d' y='%d' width='6' height='6' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (x + (i % 5) * 8, 44 - (i // 5) * 8 + 8, BLUE, INK))
    if e:
        x += 42
    return wrap(max(x + 4, 60), 66, "".join(s), label or "%d Hunderter, %d Zehner, %d Einer" % (h, z, e))


def saeulen(data, unit_label="", label="Säulendiagramm", step=None):
    """Säulendiagramm: data = [(Name, Wert)]"""
    mx = max(v for _, v in data)
    step = step or (1 if mx <= 10 else 2 if mx <= 20 else 5 if mx <= 50 else 10)
    top = int(math.ceil(mx / float(step)) * step)
    H, bw, gap, x0, y0 = 160, 42, 26, 44, 20
    W = x0 + len(data) * (bw + gap) + 10
    Y = lambda v: y0 + H - v / float(top) * H
    s = []
    for v in range(0, top + 1, step):
        s.append(line(x0, Y(v), W - 6, Y(v), "#cccccc", 1))
        s.append(text(x0 - 8, Y(v) + 5, num(v), 12, anchor="end", weight=400))
    s.append(line(x0, y0, x0, y0 + H, INK, 2))
    s.append(line(x0, y0 + H, W - 6, y0 + H, INK, 2))
    for i, (n, v) in enumerate(data):
        x = x0 + gap / 2 + i * (bw + gap)
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%.1f' fill='%s' stroke='%s' stroke-width='1.2'/>"
                 % (x, Y(v), bw, y0 + H - Y(v), FILL, GREEN))
        s.append(text(x + bw / 2, y0 + H + 18, n, 12, weight=600))
    if unit_label:
        s.append(text(8, y0 - 6, unit_label, 12, anchor="start", weight=600))
    return wrap(W, y0 + H + 28, "".join(s), label, lg=True)


def strichliste(n):
    """Strichliste: Fünferbündel"""
    s, x = [], 6
    for b in range(n // 5):
        for k in range(4):
            s.append(line(x + k * 7, 4, x + k * 7, 30, INK, 2.2))
        s.append(line(x - 3, 26, x + 24, 8, INK, 2.2))
        x += 38
    for k in range(n % 5):
        s.append(line(x + k * 7, 4, x + k * 7, 30, INK, 2.2))
    x += (n % 5) * 7
    return svg_wrap(max(x + 6, 20), 34, "".join(s), "Strichliste mit %d Strichen" % n)


def coin(cx, cy, cents):
    """Euromünze (vereinfachte Zeichnung) mit Aufschrift"""
    r = {1: 12, 2: 13, 5: 15, 10: 14, 20: 16, 50: 17, 100: 17, 200: 19}[cents]
    gold = cents in (10, 20, 50)
    copper = cents in (1, 2, 5)
    fillc = "#e0b84c" if gold else "#c9733c" if copper else "#d6d6d6"
    ring = ""
    if cents == 100:
        ring = "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#d6d6d6' stroke='%s'/>" % (cx, cy, r * 0.68, INK)
        fillc = "#e0b84c"
    if cents == 200:
        ring = "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#e0b84c' stroke='%s'/>" % (cx, cy, r * 0.68, INK)
        fillc = "#d6d6d6"
    lab = "%d €" % (cents // 100) if cents >= 100 else "%d ct" % cents
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>%s" % (cx, cy, r, fillc, INK, ring)
            + text(cx, cy + 4, lab.replace(" ", NB), 9 if cents < 100 else 10))


def note(x, y, euro):
    col = {5: "#b9b9b9", 10: "#e8a0a0", 20: "#9fc3e8", 50: "#f0c27a", 100: "#9fd39f", 200: "#f3e08a"}[euro]
    return ("<rect x='%.1f' y='%.1f' width='70' height='38' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (x, y, col, INK) + text(x + 35, y + 25, "%d%s€" % (euro, NB), 15))


def geld_svg(items):
    """items: Liste von Cent-Beträgen; ab 500 Scheine, sonst Münzen"""
    s, x = [], 6
    notes = [c for c in items if c >= 500]
    coins = [c for c in items if c < 500]
    for c in sorted(notes, reverse=True):
        s.append(note(x, 6, c // 100))
        x += 78
    for c in sorted(coins, reverse=True):
        r = 20
        s.append(coin(x + r, 25, c))
        x += 2 * r + 4
    total = sum(items)
    return wrap(x + 4, 50, "".join(s), "Geld: zusammen %s" % eur(total).replace(NB, " "))


def solid_svg(kind, r=34, color="#cfe6d6"):
    """Körper: wuerfel, quader, kugel, zylinder, kegel, pyramide"""
    from k_pics import solid
    W = int(r * 2.9 + 16)
    cx = cy = W / 2.0
    if kind in ("kugel", "wuerfel", "zylinder", "kegel"):
        body = solid({"kugel": "sphere", "wuerfel": "cube", "zylinder": "cylinder", "kegel": "cone"}[kind], cx, cy, r, color)
    elif kind == "quader":
        a, b, d = r * 1.9, r * 1.0, r * 0.55
        x0, y0 = cx - a / 2 - d / 2, cy - b / 2 + d / 2
        body = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#ffffff' fill-opacity='0.5' stroke='%s' stroke-width='2'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' fill-opacity='0.75' stroke='%s' stroke-width='2'/>"
                % (x0, y0, a, b, color, INK, x0, y0, x0 + d, y0 - d, x0 + a + d, y0 - d, x0 + a, y0, INK,
                   x0 + a, y0, x0 + a + d, y0 - d, x0 + a + d, y0 + b - d, x0 + a, y0 + b, color, INK))
    elif kind == "pyramide":
        h = r * 1.8
        ax, ay = cx, cy - h / 2
        p1, p2, p3, p4 = (cx - r * 1.1, cy + h / 2), (cx + r * 0.6, cy + h / 2), (cx + r * 1.2, cy + h / 2 - r * 0.45), (cx - r * 0.5, cy + h / 2 - r * 0.45)
        body = ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' fill-opacity='0.7' stroke='%s' stroke-width='2'/>"
                "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.3' stroke-dasharray='4 3'/>"
                % (ax, ay, p1[0], p1[1], p2[0], p2[1], color, INK,
                   ax, ay, p2[0], p2[1], p3[0], p3[1], color, INK,
                   p1[0], p1[1], p4[0], p4[1], p3[0], p3[1], ax, ay, p4[0], p4[1], INK))
    else:
        raise ValueError(kind)
    names = {"kugel": "Kugel", "wuerfel": "Würfel", "quader": "Quader", "zylinder": "Zylinder", "kegel": "Kegel", "pyramide": "Pyramide"}
    return wrap(W, W, body, "ein Körper")


def clock(h, m, size=170):
    from tw_common import clock as _clock
    return _clock(h, m, size, label="Uhr")


def schriftlich(rows, op="+", carries=None, label="schriftliche Rechnung", result=None):
    """Schriftliche Rechnung auf Karopapier: rows untereinander, rechtsbündig. carries: Ziffern über der Linie (Übertrag),
    als dict {Stelle von rechts: Ziffer}. result: Ergebnis (Text) oder None (leer lassen)"""
    c = 26
    width = max(len(r) for r in rows + ([result] if result else [])) + 2
    nrow = len(rows) + 2
    W, H = width * c + 8, nrow * c + 10
    s = []
    for i in range(width + 1):
        s.append(line(4 + i * c, 4, 4 + i * c, 4 + nrow * c, "#bcd6e6", 1))
    for j in range(nrow + 1):
        s.append(line(4, 4 + j * c, 4 + width * c, 4 + j * c, "#bcd6e6", 1))
    R0 = 4 + width * c

    def put(t, j, col=INK, fs=18):
        for k, ch in enumerate(reversed(t)):
            s.append(text(R0 - c * k - c / 2, 4 + j * c + c * 0.72, ch, fs, col=col))
    for j, r in enumerate(rows):
        put(r, j)
    s.append(text(R0 - c * (len(max(rows, key=len)) + 1) + c / 2 - c * 0.0, 4 + (len(rows) - 1) * c + c * 0.72, op, 18, col=GREEN))
    ly = 4 + len(rows) * c + c * 0.42
    if carries:
        for k, d in carries.items():
            s.append(text(R0 - c * k - c / 2, ly - 3, str(d), 11, col=RED))
    s.append(line(4 + c * 0.5, ly + 1, R0 - 2, ly + 1, INK, 2.4))
    if result:
        put(result, len(rows) + 1 - 0.35, col=BLUE)
    return wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ Zahlwörter und große Stellenwerttafel (Klasse 4)
_ONES = ["", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun"]
_TEENS = ["zehn", "elf", "zwölf", "dreizehn", "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"]
_TENS = ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig", "siebzig", "achtzig", "neunzig"]


def _w99(n):
    if n < 10:
        return _ONES[n]
    if n < 20:
        return _TEENS[n - 10]
    t, o = divmod(n, 10)
    return (("ein" if o == 1 else _ONES[o]) + "und" + _TENS[t]) if o else _TENS[t]


def _w999(n, end=True):
    h, r = divmod(n, 100)
    s = (("ein" if h == 1 else _ONES[h]) + "hundert") if h else ""
    if r == 1 and not end:
        return s + "ein"
    return s + _w99(r)


def wort(n):
    """Zahlwort bis eine Million: 345206 → dreihundertfünfundvierzigtausendzweihundertsechs"""
    if n == 1000000:
        return "eine Million"
    if n == 0:
        return "null"
    t, r = divmod(n, 1000)
    s = (_w999(t, end=False) + "tausend") if t else ""
    return s + (_w999(r) if r else "")


STELLEN = ["HT", "ZT", "T", "H", "Z", "E"]


def stellentafel(n, cols=6):
    """Stellenwerttafel HT ZT T H Z E (rechts die letzten cols Stellen)"""
    head = STELLEN[6 - cols:]
    ds = str(n).rjust(cols, " ")
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head),
               "".join("<td style='text-align:center;min-width:30px'>%s</td>" % (d if d != " " else "") for d in ds)))
