# -*- coding: utf-8 -*-
"""
台灣（國小數學・108課綱）の単元生成の共通部品。
・文は繁體中文（台灣用語：公分、毫米、公升、毫升、公斤、公克、元）
・4けたまではカンマなし、5けた以上は 10,000 のようにカンマ
・HTML の属性はシングルクォート、バックスラッシュなし（check.py と同じルール）
・答えも誤答もすべてコードで計算する
"""
import os
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)

UPDATED = "2026-11-16"
STD_URL = ("https://www.naer.edu.tw/upload/1/16/doc/815/"
           "十二年國民基本教育課程綱要國民中小學暨普通型高級中等學校-數學領域.pdf")
GIRLS = ["小美", "小芳", "怡君", "佳穎", "雅婷", "心怡", "詩涵", "欣妤", "宜蓁", "品妍"]
BOYS = ["小明", "小華", "志明", "家豪", "俊宏", "冠宇", "宇翔", "柏翰", "承恩", "子軒"]
DOMAIN = {"N": "數與量", "S": "空間與形狀", "R": "關係", "D": "資料與不確定性", "A": "代數", "G": "坐標幾何"}


def num(n):
    """4けたまで 3468、5けた以上 12,500"""
    n = int(n)
    return str(n) if abs(n) < 10000 else "{:,}".format(n)


def dnum(v, places=1):
    """小數：0.3、2.5（不要な 0 は付けない）"""
    s = ("%." + str(places) + "f") % v
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s


class Names:
    def __init__(self, rnd):
        self.pool = GIRLS + BOYS
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        n = self.pool[self.i % len(self.pool)]
        self.i += 1
        return n


def mcq(q, correct, cands, e):
    """4 択：正解＋重複しない誤答 3 つ（文字列で比べる）。並びは balance() で決める。"""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or c.startswith("-") or c.startswith("−"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        # 足りないときは、答えの数字を ±1、±2、×10 した近い数で補う（単位などの文字はそのまま）
        import re as _re
        m = _re.match(r"^(.*?)(\d[\d,]*(?:\.\d+)?)([^\d]*)$", correct)
        if m and "<" not in correct:
            from decimal import Decimal as _D
            v = _D(m.group(2).replace(",", ""))
            places = len(m.group(2).split(".")[1]) if "." in m.group(2) else 0
            step = _D(1).scaleb(-places)
            for d in (1, -1, 2, -2, 3):
                nv = v + step * d
                if nv <= 0:
                    continue
                c = "%s%s%s" % (m.group(1), num(int(nv)) if places == 0 else format(nv, "f"), m.group(3))
                if c not in seen:
                    seen.add(c)
                    pick.append(c)
                if len(pick) == 3:
                    break
    if len(pick) < 3 and "class='fn'" in correct:
        # 分數の答え：分子を ±1、±2 した分數で補う（分母はそのまま）
        import re as _re
        m = _re.search(r"<span class='fn'>(\d+)</span>", correct)
        v = int(m.group(1))
        for d in (1, -1, 2, -2, 3):
            if v + d <= 0:
                continue
            c = correct[:m.start(1)] + str(v + d) + correct[m.end(1):]
            if c not in seen:
                seen.add(c)
                pick.append(c)
            if len(pick) == 3:
                break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ("<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead>"
            "<tbody>%s</tbody></table></div>" % (h, b))


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>例題</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>答：%s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def mistakes(rows):
    """よくある間違い：[(まちがい, 正しくは)]"""
    return "<h2>常見錯誤</h2>" + table(["常見錯誤", "正確的想法"], rows)


def lesson(think, examples, mist, extra=""):
    """body_html：怎麼想 → 例題 → 常見錯誤（短い文で）"""
    h = "<h2>怎麼想</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(examples)
    h += mistakes(mist)
    return h


def make_unit(rnd, grade, slug, code, std_text, title, seo_title, short_title, meta_desc,
              key_big, key_sub, body_html, faq, sets, sort):
    """sets: [(セット名, [items x20])] を balance して書き出す"""
    sets = [{"title": t, "items": items} for t, items in sets]
    for s in sets:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
    balance(sets, rnd)
    write_unit("tw", "math", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": DOMAIN[code[0]], "standard_code": code, "standard_url": STD_URL,
        "standard_text": std_text, "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": faq, "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def uniq(items):
    """同じ問題が 2 回出ないかを確かめる（生成側の安全確認）"""
    seen = set()
    for it in items:
        k = it["q"]
        assert k not in seen, ("duplicate question", k)
        seen.add(k)
    return items


def pick_unique(rnd, maker, n, seen=None, tries=4000):
    """maker() を呼んで、問題文が重ならない n 問を集める（seen を渡すと単元全体で重ならない）"""
    out = []
    seen = set() if seen is None else seen
    for _ in range(tries):
        it = maker()
        if it is None or it["q"] in seen:
            continue
        seen.add(it["q"])
        out.append(it)
        if len(out) == n:
            return out
    raise AssertionError("could not make %d unique questions" % n)


def clock(h, m, size=180, label=None):
    """時鐘（短針は (h + m/60) × 30 度の位置）。時刻の問題・角の問題で使う"""
    import math
    cx = cy = size / 2.0
    Rr = cx - 6
    k = Rr / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, Rr, GREEN, max(5 * k, 1.5))]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = Rr - (13 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (Rr - 3 * k) * math.cos(a), cy + (Rr - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), INK, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), INK, max(2.6 * k, 1.2)))
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + Rr * 0.5 * math.cos(ah), cy + Rr * 0.5 * math.sin(ah), INK, max(8 * k, 2.5)))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + Rr * 0.86 * math.cos(am), cy + Rr * 0.86 * math.sin(am), RED, max(4.5 * k, 1.8)))
    fs = 19 * k
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, INK, 3.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        rn = Rr - 29 * k
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, max(6 * k, 2), INK))
    return fig(svg_wrap(int(size), int(size), "".join(s), label or "時鐘 %d時%d分" % (h, m)))


def mx(w, n, d):
    """帶分數：2 又 3/4（整數と分數を並べる）"""
    return "%d%s" % (w, fr(n, d)) if w else fr(n, d)


DIG = "零一二三四五六七八九"


def zh4(n):
    """0〜9999 の國字（先頭の「一十」は「十」）"""
    if n == 0:
        return "零"
    s = str(n)
    out, zero = "", False
    L = len(s)
    for i, ch in enumerate(s):
        d = int(ch)
        p = L - 1 - i
        if d == 0:
            zero = True
            continue
        if zero and out:
            out += "零"
        zero = False
        if p == 1 and d == 1 and out == "":
            out += "十"
        else:
            out += DIG[d] + ("" if p == 0 else ["", "十", "百", "千"][p])
    return out


def zh(n):
    """一億まで：32050400 → 三千二百零五萬零四百"""
    if n == 100000000:
        return "一億"
    w, r = divmod(n, 10000)
    if not w:
        return zh4(r)
    s = zh4(w) + "萬"
    if r:
        if r < 1000:
            s += "零"
        s += zh4(r) if not (r >= 10 and r < 20) else "一" + zh4(r)
    return s


def wan(n):
    """萬を使った書き方：32050400 → 3205萬400"""
    w, r = divmod(n, 10000)
    if not w:
        return str(r)
    return "%d萬%s" % (w, r if r else "")


def ff(v, mixed=True):
    """Fraction を最簡分數で：7/4 → 1又3/4（mixed=False なら 7/4）、整数はそのまま"""
    from fractions import Fraction as _F
    v = _F(v)
    if v.denominator == 1:
        return num(v.numerator)
    w, r = divmod(v.numerator, v.denominator)
    if mixed and w:
        return mx(w, r, v.denominator)
    return fr(v.numerator, v.denominator)
