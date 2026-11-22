# -*- coding: utf-8 -*-
"""
France collège (6e : programme 2025 du cycle 3 ; 5e・4e・3e : programme 2026 du cycle 4) の生成スクリプト共通部品。fr_common の上に:
・負の数は「−」（U+2212）。sg(n) → −3、par(n) → (−3)（負のときだけかっこ）
・小数はコンマ：d(x) は Fraction / int / float を「2,5」に（割り切れないときは ValueError）
・fq(x) は Fraction を HTML の分数に（整数ならそのまま、負なら −）
・expr([(係数, "x"), (定数, "")]) → 3x − 5（係数 1 は省略）
・M(q, a, w, e)：mcq(neg=True)。誤答に正解と同じ値が入らないよう呼ぶ側で計算する
・relabel(svg, label)：DE の図の aria-label をフランス語に
・unit(grade, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort)：seo_title・standard_text の末尾を自動
・grade は "6e" "5e" "4e" "3e"。dom は 6e なら N/G/E/D/P、5e〜3e なら N/A/F/E/D（fr_common.DOMAIN_C3 / DOMAIN_C4）
"""
import re
from fractions import Fraction as Fr
from fr_common import (mcq, num, dec, eur, hm, dur, fp, Kids, Il, mix, table, example, lesson, make_unit,  # noqa: F401
                       wrap, text, line, INK, FILL, GREEN, RED, BLUE, NB, FOIS, DIV, fr, droite, barres, solide_svg)

MINUS = "−"


def d(x):
    """nombre décimal (Fraction, int ou float) avec virgule ; ValueError s’il n’est pas décimal"""
    x = Fr(x).limit_denominator(10 ** 6) if isinstance(x, float) else Fr(x)
    k = 0
    t = x.denominator
    for p in (2, 5):
        while t % p == 0:
            t //= p
    if t != 1:
        raise ValueError("pas décimal")
    while (x * 10 ** k).denominator != 1:
        k += 1
    n = int(abs(x) * 10 ** k)
    ip, fpart = divmod(n, 10 ** k)
    s = num(ip) + ("," + str(fpart).rjust(k, "0") if k else "")
    return (MINUS if x < 0 else "") + s


def sg(x):
    return d(x)


def par(x):
    return "(%s)" % d(x) if Fr(x) < 0 else d(x)


def fq(x, mixed=False):
    """Fraction → HTML (entier si possible)"""
    x = Fr(x)
    if x.denominator == 1:
        return d(x)
    s = MINUS if x < 0 else ""
    a = abs(x)
    return s + fr(a.numerator, a.denominator)


def coef(k, var, first):
    k = Fr(k)
    a = abs(k)
    body = ("" if (a == 1 and var) else (fq(a) if a.denominator != 1 else d(a))) + var
    if first:
        return (MINUS if k < 0 else "") + body
    return " %s %s" % (MINUS if k < 0 else "+", body)


def expr(terms):
    out = ""
    for k, v in terms:
        if Fr(k) == 0:
            continue
        out += coef(k, v, out == "")
    return out or "0"


def val(t):
    """valeur numérique d’une réponse (« −3,50 » → Fraction), ou None"""
    t = re.sub(r"<span class='fn'>([^<]*)</span><span class='fd'>([^<]*)</span>", r"\1/\2", str(t))
    t = re.sub(r"<[^>]+>", "", t).replace(NB, "").replace(" ", "").replace(MINUS, "-")
    m = re.match(r"^(-?)(\d+(?:,\d+)?)(?:/(\d+))?([a-zA-Z€%²³°]*)$", t)
    if not m:
        return None
    v = Fr(m.group(2).replace(",", "."))
    if m.group(3):
        v /= int(m.group(3))
    return (-v if m.group(1) else v, m.group(4))


def M(q, a, w, e):
    """mcq (négatifs permis) ; on enlève les distracteurs qui ont la même valeur que la réponse (2,9 et 2,90)"""
    va = val(a)
    if va is not None:
        w = [x for x in w if x is None or val(x) != va]
    return mcq(q, a, w, e, neg=True)


def relabel(svg, label):
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)


def pl(n, s, p=None):
    return "%s %s" % (d(n), s if abs(n) <= 1 else (p or s + "s"))


def que(n):
    return ("qu’" if n[0] in "AEIOUÉaeiouéH" else "que ") + n


def de_n(n):
    return ("d’" if n[0] in "AEIOUÉaeiouéH" else "de ") + n


def unit(grade, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort):
    seo = "%s %s : fiches et exercices avec corrigé" % (short, grade)
    tail = " (résumé du programme 2025 du cycle 3)" if grade == "6e" else " (résumé du programme 2026 du cycle 4)"
    make_unit(R, slug, dom, std + tail, title, seo, short, meta, key_big, key_sub, body, faq, sets, sort, grade=grade)


def L(think, ex, mist):
    """lesson : think = [phrases], ex = [(énoncé, [étapes], réponse)], mist = [[erreur, correction]]"""
    return lesson(think, [example(a, b, c) for a, b, c in ex], mist)


def dk(x, k):
    """décimal avec exactement k chiffres après la virgule (72,90)"""
    x = Fr(x)
    n = int(round(abs(x) * 10 ** k))
    ip, fpart = divmod(n, 10 ** k)
    return (MINUS if x < 0 else "") + num(ip) + ("," + str(fpart).rjust(k, "0") if k else "")


def euro(x):
    """35 € ; 12,50 €"""
    x = Fr(x)
    return (d(x) if x.denominator == 1 else dk(x, 2)) + NB + "€"


def em(x):
    """montant sans le symbole : 35 ; 12,50"""
    x = Fr(x)
    return d(x) if x.denominator == 1 else dk(x, 2)


def figure(pts, segs, sides=(), right=(), W=340, H=230, label="figure géométrique", ticks=(), dashed=()):
    """pts : {nom: (x, y)} (repère mathématique) ; segs : [(A, B)] ; sides : [(A, B, texte)] ;
    right : [(sommet, A, B)] marque d’angle droit ; ticks : [(A, B, n)] codage de longueurs égales ; dashed : [(A, B)]"""
    import math
    xs = [p[0] for p in pts.values()]
    ys = [p[1] for p in pts.values()]
    m, mxm = 34, 64
    sc = min((W - 2 * mxm) / float(max(xs) - min(xs) or 1), (H - 2 * m) / float(max(ys) - min(ys) or 1))
    ox = (W - (max(xs) - min(xs)) * sc) / 2.0
    oy = (H - (max(ys) - min(ys)) * sc) / 2.0
    P = {k: (ox + (x - min(xs)) * sc, H - oy - (y - min(ys)) * sc) for k, (x, y) in pts.items()}
    cx = sum(p[0] for p in P.values()) / len(P)
    cy = sum(p[1] for p in P.values()) / len(P)
    s = []
    for a, b in segs:
        s.append(line(P[a][0], P[a][1], P[b][0], P[b][1], INK, 2))
    for a, b in dashed:
        s.append(line(P[a][0], P[a][1], P[b][0], P[b][1], BLUE, 1.6, " stroke-dasharray='5 4'"))
    for v, a, b in right:
        (vx, vy), (ax, ay), (bx, by) = P[v], P[a], P[b]
        da = math.hypot(ax - vx, ay - vy)
        db = math.hypot(bx - vx, by - vy)
        ux, uy = (ax - vx) / da * 11, (ay - vy) / da * 11
        wx, wy = (bx - vx) / db * 11, (by - vy) / db * 11
        s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.6'/>" % (vx + ux, vy + uy, vx + ux + wx, vy + uy + wy, vx + wx, vy + wy, INK))
    for a, b, n in ticks:
        mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
        dx, dy = P[b][0] - P[a][0], P[b][1] - P[a][1]
        L_ = math.hypot(dx, dy)
        nx, ny = -dy / L_ * 6, dx / L_ * 6
        tx, ty = dx / L_ * 4, dy / L_ * 4
        for i in range(n):
            o = (i - (n - 1) / 2.0)
            s.append(line(mx + o * tx - nx, my + o * ty - ny, mx + o * tx + nx, my + o * ty + ny, RED, 1.8))
    for a, b, t in sides:
        mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
        dx, dy = P[b][0] - P[a][0], P[b][1] - P[a][1]
        L_ = math.hypot(dx, dy)
        nx, ny = -dy / L_, dx / L_
        if (mx + nx - cx) ** 2 + (my + ny - cy) ** 2 < (mx - cx) ** 2 + (my - cy) ** 2:
            nx, ny = -nx, -ny
        anc = "middle" if abs(nx) < 0.6 else ("start" if nx > 0 else "end")
        s.append(text(mx + nx * (16 if anc == "middle" else 8), my + ny * 16 + 5, t, 14, anchor=anc, col=BLUE))
    for k, (x, y) in P.items():
        dx, dy = x - cx, y - cy
        L_ = math.hypot(dx, dy) or 1
        s.append(text(x + dx / L_ * 15, y + dy / L_ * 15 + 5, k, 15))
    return wrap(W, H, "".join(s), label, lg=True)
