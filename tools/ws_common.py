# -*- coding: utf-8 -*-
"""
Shared helpers for unit generators (US Grade 7 and later).
Same rules as the older generators: HTML attributes in single quotes, no backslashes,
negative numbers with the real minus sign (U+2212), exact arithmetic with Fraction.
"""
import json, os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
GREEN = "#006633"
FILL = "#cfe6d6"
GRAY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#1f5fa8"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace", "Chloe", "Hana"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen", "Ethan", "Ravi"]
X = "<i>x</i>"


# ------------------------------------------------------------ numbers
def comma(n):
    return "{:,}".format(int(n))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def terminates(v):
    d = F(v).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def dec(v):
    """Exact decimal text with commas, no sign: 2.85, 1,250.5"""
    v = abs(F(v))
    assert terminates(v), v
    n, d = v.numerator, v.denominator
    k = 0
    while (10 ** k) % d:
        k += 1
    s = str(n * (10 ** k) // d).rjust(k + 1, "0")
    ip, fp = (s[:-k], s[-k:]) if k else (s, "")
    return comma(int(ip)) + ("." + fp if fp else "")


def frac(v):
    """Simplest form, no sign; mixed number above 1."""
    v = abs(F(v))
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return comma(w)
    if w == 0:
        return fr(r, v.denominator)
    return "%s %s" % (comma(w), fr(r, v.denominator))


def num(v, style="d"):
    """Signed number. style 'd' decimal (or whole), 'f' fraction. None if it cannot be shown."""
    v = F(v)
    if style == "d" and not terminates(v):
        return None
    body = dec(v) if style == "d" else frac(v)
    return (MINUS if v < 0 else "") + body


def par(v, style="d"):
    """Negative numbers in parentheses after an operation sign: 4 + (−7)."""
    s = num(v, style)
    return "(%s)" % s if F(v) < 0 else s


def plain(s):
    assert "<" not in s, s
    return s


# ------------------------------------------------------------ questions
def mcq(q, correct, cands, e):
    """correct / cands: (html, key). Candidates with a key already used are skipped."""
    seen = {correct[1]}
    pick = []
    for c in cands:
        if c is None or c[0] is None or c[1] is None:
            continue
        if c[1] in seen:
            continue
        seen.add(c[1])
        pick.append(c[0])
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct[0]] + pick, "a": 0, "e": e}


def nums(vs, style="d", unit=""):
    out = []
    for v in vs:
        if v is None:
            out.append(None)
            continue
        s = num(v, style)
        out.append(None if s is None else (s + unit, F(v)))
    return out


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [c[it["a"]]] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def B(s):
    return "<b>%s</b>" % s


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ figures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def figure(svg, caption):
    return "<figure class='sn-fig'>%s<figcaption>%s</figcaption></figure>" % (svg, caption)


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, italic=False, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, weight, col, anchor, " font-style='italic'" if italic else "", t))


def line(x1, y1, x2, y2, col=INK, w=2, extra=""):
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'%s/>" % (x1, y1, x2, y2, col, w, extra)


def arrow_head(x, y, direction, col):
    """Small triangle pointing left (-1) or right (+1) with its tip at (x, y)."""
    d = direction
    return "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>" % (x, y, x - 9 * d, y - 6, x - 9 * d, y + 6, col)


def number_line(lo, hi, jumps=(), dots=(), label="number line", step=1, labels_every=1, width=None):
    """Integer number line from lo to hi. jumps: [(start, end, colour)] drawn as arcs above the line.
    dots: [(value, colour)]."""
    n = hi - lo
    unit = (width or 440) / float(n)
    x0, y = 18, 70 + 22 * max(0, len(jumps) - 1)
    W = int(x0 * 2 + n * unit)
    X = lambda v: x0 + (v - lo) * unit
    s = [line(x0 - 10, y, x0 + n * unit + 10, y, INK, 2),
         arrow_head(x0 - 12, y, -1, INK), arrow_head(x0 + n * unit + 12, y, 1, INK)]
    for v in range(lo, hi + 1, step):
        s.append(line(X(v), y - 7, X(v), y + 7, INK, 2))
        if (v - lo) % labels_every == 0 or v == 0:
            s.append(text(X(v), y + 26, num(v), 14, weight=700 if v == 0 else 400))
    for k, (a, b, col) in enumerate(jumps):
        h = 26 + 20 * k
        xa, xb = X(a), X(b)
        mid = (xa + xb) / 2
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xa, y - 4, mid, y - 4 - h * 2, xb, y - 4, col))
        s.append(arrow_head(xb, y - 6, 1 if b > a else -1, col))
        d = b - a
        s.append(text(mid, y - 6 - h - 4, ("+" if d > 0 else MINUS) + str(abs(d)), 14, col=col))
    for v, col in dots:
        s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (X(v), y, col))
    return svg_wrap(W + 6, y + 36, "".join(s), label)


def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Example</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Answer: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


# ------------------------------------------------------------ output
def write_unit(country, subject, grade, unit):
    out = os.path.join(HERE, "..", "content", country, subject, grade)
    os.makedirs(out, exist_ok=True)
    unit = dict(unit)
    unit.update(country=country, subject=subject, grade=grade)
    for s in unit["sets"]:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(it["c"]) == 4 and len({c for c in it["c"]}) == 4, it
    blob = json.dumps(unit, ensure_ascii=False, indent=1)
    assert "\\" not in blob.replace('\\"', ""), "backslash in output"
    path = os.path.join(out, unit["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(blob + "\n")
    print("wrote", os.path.relpath(path, os.path.join(HERE, "..")),
          sum(len(s["items"]) for s in unit["sets"]), "questions")
