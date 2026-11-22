# -*- coding: utf-8 -*-
"""
France (école élémentaire, programmes de mathématiques 2024 du cycle 2 / cycle 3) の単元生成の共通部品。
・文はフランス語。子ども向けに短い文、tu で話しかける。: ; ? ! の前はノーブレークスペース（フランスの組版）
・数: 1 000 以上は空白区切り（ノーブレークスペース）。小数はコンマ（2,50 €）
・記号: 3 × 4、12 ÷ 3、時刻は 8 h 15、時間の長さは 1 h 25 min
・お金: 3,50 €、45 c
・HTML の属性はシングルクォート、バックスラッシュなし（check.py と同じルール）
・答えも誤答もすべてコードで計算する
"""
import math, re
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)

UPDATED = "2026-11-22"
STD_URL = "https://www.education.gouv.fr/bo/2024/Hebdo41/MENE2415135A"
DOMAIN = {
    "N": "Nombres, calcul et résolution de problèmes",
    "G": "Grandeurs et mesures",
    "E": "Espace et géométrie",
    "D": "Organisation et gestion des données",
}
STD_URL_C3 = "https://www.education.gouv.fr/bo/2025/Hebdo16/MENE2504620A"
DOMAIN_C3 = dict(DOMAIN, D="Organisation et gestion de données et probabilités", P="Proportionnalité")
STD_URL_C4 = "https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A"
DOMAIN_C4 = {"N": "Nombres et calculs", "A": "Calcul littéral et algébrique", "F": "Proportionnalité et fonctions",
             "E": "Espace et géométrie", "D": "Données et probabilités"}
GIRLS = ["Emma", "Léa", "Chloé", "Inès", "Jade", "Louise", "Manon", "Camille", "Zoé", "Lina", "Alice", "Rose", "Ambre", "Nour"]
BOYS = ["Lucas", "Hugo", "Nathan", "Louis", "Gabriel", "Arthur", "Jules", "Adam", "Léo", "Tom", "Raphaël", "Sacha", "Noah", "Malo"]
NB = " "
FOIS = "×"
DIV = "÷"


# ------------------------------------------------------------ numbers
def num(n):
    """1 000, 10 000（1 000 以上はノーブレークスペースで区切る）"""
    n = int(n)
    s = str(abs(n))
    if len(s) >= 4:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return ("−" if n < 0 else "") + s


def dec(v, places=None):
    """nombre décimal avec virgule : 2,5 / 1,25"""
    if places is None:
        s = ("%.3f" % v).rstrip("0").rstrip(".")
    else:
        s = ("%." + str(places) + "f") % v
    ip, _, fp = s.partition(".")
    return num(int(ip)) + ("," + fp if fp else "")


def eur(cents, c=False):
    """argent : 350 → 3,50 €, 300 → 3 €, 45 → 45 c（c=True のとき 1 € 未満を c で）"""
    cents = int(cents)
    if c and cents < 100:
        return "%d%sc" % (cents, NB)
    e, r = divmod(cents, 100)
    if r == 0:
        return "%s%s€" % (num(e), NB)
    return "%s,%02d%s€" % (num(e), r, NB)


def unit(v, u):
    return "%s%s%s" % (num(v) if isinstance(v, int) else v, NB, u)


def hm(h, m):
    """8 h 15, 14 h, 9 h 05"""
    return "%d%sh%s" % (h, NB, (NB + "%02d" % m) if m else "")


def dur(mins):
    """durée : 1 h 25 min, 45 min, 2 h"""
    h, m = divmod(int(mins), 60)
    if h and m:
        return "%d%sh%s%d%smin" % (h, NB, NB, m, NB)
    if h:
        return "%d%sh" % (h, NB)
    return "%d%smin" % (m, NB)


def fp(t):
    """espaces insécables avant : ; ? !（フランス語の句読点）"""
    return re.sub(r" ([:;?!])", NB + r"\1", t)


# ------------------------------------------------------------ names
class Kids:
    """prénoms avec genre : next() → (prénom, 'elle'|'il')"""

    def __init__(self, rnd):
        self.pool = [(n, "elle") for n in GIRLS] + [(n, "il") for n in BOYS]
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


def Il(p):
    return p[1].capitalize()


# ------------------------------------------------------------ questions
def mcq(q, correct, cands, e, neg=False):
    """4 択：正解＋重複しない誤答 3 つ。足りないときは答えの数を ±1、±2 … した近い数で補う。"""
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
        m = re.match(r"^(.*?)(\d(?:\d| (?=\d))*(?:,\d+)?)([^\d]*)$", correct)
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
    return {"q": fp(q), "c": [correct] + pick, "a": 0, "e": fp(e)}


def pick_unique(rnd, maker, n, seen=None, tries=6000):
    out = []
    seen = set() if seen is None else seen
    for _ in range(tries):
        try:
            it = maker()
        except (ValueError, IndexError, ZeroDivisionError, AssertionError):
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
    raise AssertionError("could not make %d unique questions (%d) %s" % (n, len(out), getattr(maker, "__name__", "")))


def mix(rnd, seen, parts):
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
    return fp("<div class='sn-ex'><span class='sn-ex-t'>Exemple</span><p class='sn-ex-q'>%s</p>%s"
              "<p class='sn-ex-a'>Réponse : %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html : Comment faire → Exemples → Erreurs fréquentes（phrases courtes）"""
    h = "<h2>Comment faire</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(examples)
    h += "<h2>Erreurs fréquentes</h2>" + table(["Erreur fréquente", "Ce qu'il faut faire"], mist)
    return fp(h)


def plain_text(t):
    t = re.sub(r"<span class='fr'><span class='fn'>(.*?)</span><span class='fd'>([^<]*)</span></span>", r"\1/\2", t)
    assert not re.search(r"<[a-zA-Z/]", t), t
    return t


def make_unit(rnd, slug, dom, std_text, title, seo_title, short_title, meta_desc,
              key_big, key_sub, body_html, faq, sets, sort, grade="ce2"):
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
    title, seo_title, short_title, meta_desc, key_big, key_sub = [fp(plain_text(x)) for x in (title, seo_title, short_title, meta_desc, key_big, key_sub)]
    c3 = grade in ("cm1", "cm2", "6e")
    c4 = grade in ("5e", "4e", "3e")
    dname = (DOMAIN_C4 if c4 else DOMAIN_C3 if c3 else DOMAIN)[dom]
    glab = grade if grade[0].isdigit() else grade.upper()
    write_unit("fr", "maths", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": dname, "standard_code": "%s · %s" % (glab, dname), "standard_url": STD_URL_C4 if c4 else STD_URL_C3 if c3 else STD_URL,
        "standard_text": fp(std_text), "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": [{"q": fp(q), "a": fp(a)} for q, a in faq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


# ------------------------------------------------------------ pictures
def wrap(w, h, body, label, lg=False):
    s = svg_wrap(int(w), int(h), body, label)
    if lg:
        s = s.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(s)


def droite(lo, hi, step, marks=(), labels=None, label="droite graduée", every=None, width=460):
    """droite graduée de lo à hi, un trait tous les step. marks : [(valeur, lettre)] avec une flèche"""
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
        lg_ = (v - lo) % big == 0
        s.append(line(X(v), y - (10 if lg_ else 6), X(v), y + (10 if lg_ else 6), INK, 2 if lg_ else 1.3))
    for v in (labels if labels is not None else [lo + i * big for i in range((hi - lo) // big + 1)]):
        s.append(text(X(v), y + 30, num(v), 14, weight=600))
    for v, ch in marks:
        s.append("<path d='M%.1f %.1f l-7 -12 h14 Z' fill='%s'/>" % (X(v), y - 12, RED))
        s.append(text(X(v), y - 28, ch, 16, col=RED))
    return wrap(x0 * 2 + n * u + 4, y + 42, "".join(s), label, lg=True)


def numeration(n, cols=4):
    """tableau de numération : m c d u"""
    head = ["m", "c", "d", "u"][4 - cols:]
    ds = str(n).rjust(cols, " ")
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head),
               "".join("<td style='text-align:center;min-width:30px'>%s</td>" % (d if d != " " else "") for d in ds)))


def blocs(m, c, d, u, label=None):
    """cubes milliers, plaques de cent, barres de dix et petits cubes"""
    s, x = [], 8
    for _ in range(m):
        s.append("<rect x='%d' y='8' width='50' height='50' fill='#f6d0a8' stroke='%s' stroke-width='2'/>" % (x, INK))
        s.append("<polygon points='%d,8 %d,0 %d,0 %d,8' fill='#f9e0c6' stroke='%s' stroke-width='1.2'/>" % (x, x + 8, x + 58, x + 50, INK))
        s.append("<polygon points='%d,8 %d,0 %d,50 %d,58' fill='#e9b98a' stroke='%s' stroke-width='1.2'/>" % (x + 50, x + 58, x + 58, x + 50, INK))
        s.append(text(x + 25, 40, "1" + NB + "000", 11))
        x += 66
    for _ in range(c):
        s.append("<rect x='%d' y='8' width='50' height='50' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, FILL, GREEN))
        for k in range(1, 10):
            s.append(line(x + k * 5, 8, x + k * 5, 58, GREEN, 0.5))
            s.append(line(x, 8 + k * 5, x + 50, 8 + k * 5, GREEN, 0.5))
        x += 58
    for _ in range(d):
        s.append("<rect x='%d' y='8' width='6' height='50' fill='#f2c94c' stroke='%s' stroke-width='1.2'/>" % (x, INK))
        for k in range(1, 10):
            s.append(line(x, 8 + k * 5, x + 6, 8 + k * 5, INK, 0.5))
        x += 10
    if d:
        x += 6
    for i in range(u):
        s.append("<rect x='%d' y='%d' width='6' height='6' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (x + (i % 5) * 8, 44 - (i // 5) * 8 + 8, BLUE, INK))
    if u:
        x += 42
    return wrap(max(x + 4, 60), 66, "".join(s), label or "%d milliers, %d centaines, %d dizaines, %d unités" % (m, c, d, u))


def barres(data, unit_label="", label="diagramme en barres", step=None):
    """diagramme en barres : data = [(nom, valeur)]"""
    mx = max(v for _, v in data)
    step = step or (1 if mx <= 10 else 2 if mx <= 20 else 5 if mx <= 50 else 10 if mx <= 100 else 20)
    top = int(math.ceil(mx / float(step)) * step)
    H, bw, gap, x0, y0 = 160, 46, 26, 44, 20
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


def coin(cx, cy, cents):
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
    lab = "%d €" % (cents // 100) if cents >= 100 else "%d c" % cents
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>%s" % (cx, cy, r, fillc, INK, ring)
            + text(cx, cy + 4, lab.replace(" ", NB), 9 if cents < 100 else 10))


def note(x, y, euro):
    col = {5: "#b9b9b9", 10: "#e8a0a0", 20: "#9fc3e8", 50: "#f0c27a", 100: "#9fd39f", 200: "#f3e08a"}[euro]
    return ("<rect x='%.1f' y='%.1f' width='70' height='38' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (x, y, col, INK) + text(x + 35, y + 25, "%d%s€" % (euro, NB), 15))


def argent_svg(items):
    """items : montants en centimes ; à partir de 500, des billets"""
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
    return wrap(x + 4, 50, "".join(s), "pièces et billets : en tout %s" % eur(sum(items)).replace(NB, " "))


def solide_svg(kind, r=34, color="#cfe6d6"):
    """cube, pave, boule, cylindre, cone, pyramide"""
    import de_common
    k = {"cube": "wuerfel", "pave": "quader", "boule": "kugel", "cylindre": "zylinder", "cone": "kegel", "pyramide": "pyramide"}[kind]
    return de_common.solid_svg(k, r, color).replace("aria-label='ein Körper'", "aria-label='un solide'")


def horloge(h, m, size=170):
    from tw_common import clock as _clock
    return _clock(h, m, size, label="horloge")


def posee(rows, op="+", carries=None, label="opération posée", result=None):
    import de_common
    return de_common.schriftlich(rows, op, carries, label, result)


# ------------------------------------------------------------ nombres en lettres (jusqu'à 9 999)
_U = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize"]
_D = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def _w99(n):
    if n <= 16:
        return _U[n]
    if n < 20:
        return "dix-" + _U[n - 10]
    d, u = divmod(n, 10)
    if d in (7, 9):
        base = "soixante" if d == 7 else "quatre-vingt"
        rest = 10 + u
        if d == 7 and u == 1:
            return "soixante et onze"
        return base + "-" + _w99(rest)
    if d == 8:
        return "quatre-vingts" if u == 0 else "quatre-vingt-" + _U[u]
    if u == 0:
        return _D[d]
    if u == 1:
        return _D[d] + " et un"
    return _D[d] + "-" + _U[u]


def _w999(n, final=True):
    c, r = divmod(n, 100)
    parts = []
    if c:
        if c == 1:
            parts.append("cent")
        else:
            parts.append(_U[c] + (" cents" if r == 0 and final else " cent"))
    if r:
        w = _w99(r)
        if not final and w == "quatre-vingts":
            w = "quatre-vingt"
        parts.append(w)
    return " ".join(parts)


def lettres(n):
    """nombre en lettres (orthographe traditionnelle) : 3 482 → trois mille quatre cent quatre-vingt-deux"""
    if n == 0:
        return "zéro"
    m, r = divmod(n, 1000)
    s = []
    if m:
        s.append("mille" if m == 1 else _w999(m, final=False) + " mille")
    if r:
        s.append(_w999(r))
    return " ".join(s)


# ------------------------------------------------------------ fractions
def frac_label(n, d):
    return "%d/%d" % (n, d)


def bande(d, k, w=300, label=None):
    """bande partagée en d parts égales, k parts coloriées（k > d なら 2 本）"""
    bars = (k + d - 1) // d if k > d else 1
    h, s = 40, []
    for b in range(bars):
        y = 6 + b * (h + 10)
        for i in range(d):
            on = b * d + i < k
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (6 + i * w / float(d), y, w / float(d), h, FILL if on else "#ffffff", INK))
    return wrap(w + 12, 12 + bars * (h + 10) - 10, "".join(s), label or "bande : %d parts sur %d coloriées" % (k, d))


def disque(d, k, r=60, label=None):
    """disque partagé en d parts égales, k coloriées"""
    cx = cy = r + 6
    s = []
    for i in range(d):
        a0, a1 = 2 * math.pi * i / d - math.pi / 2, 2 * math.pi * (i + 1) / d - math.pi / 2
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        big = 1 if a1 - a0 > math.pi else 0
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (cx, cy, x0, y0, r, r, big, x1, y1, FILL if i < k else "#ffffff", INK))
    return wrap(2 * r + 12, 2 * r + 12, "".join(s), label or "disque : %d parts sur %d coloriées" % (k, d))


def droite_frac(d, units=2, marks=(), width=420):
    """droite graduée de 0 à units, chaque unité partagée en d ; marks = [(numérateur, lettre)]"""
    n = d * units
    u = width / float(n)
    x0, y = 24, 58
    X = lambda k: x0 + k * u
    s = [line(x0 - 8, y, x0 + n * u + 12, y, INK, 2),
         "<path d='M%.1f %.1f l-9 -6 v12 Z' fill='%s'/>" % (x0 + n * u + 20, y, INK)]
    for k in range(n + 1):
        big = k % d == 0
        s.append(line(X(k), y - (11 if big else 7), X(k), y + (11 if big else 7), INK, 2 if big else 1.3))
        if big:
            s.append(text(X(k), y + 32, str(k // d), 15, weight=700))
    for k, ch in marks:
        s.append("<path d='M%.1f %.1f l-7 -12 h14 Z' fill='%s'/>" % (X(k), y - 12, RED))
        s.append(text(X(k), y - 28, ch, 16, col=RED))
    return wrap(x0 * 2 + n * u + 4, y + 42, "".join(s), "droite graduée de 0 à %d, chaque unité partagée en %d" % (units, d), lg=True)
