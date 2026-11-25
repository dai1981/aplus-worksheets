# -*- coding: utf-8 -*-
"""
Türkiye 1.〜2. sınıf の問題関数（k_pics の絵にトルコ語の aria-label）。tr_s1a・tr_s2a から使う。
とても短い文。数字のすぐ後ろに接尾辞を付けない（「7 sayısından」のように語を挟む）。
"""
import math
import re
import k_pics as P
from f_common import pattern_svg, glasses_svg
import tr_g as G
import tr_s3a as A
from tr_common import num, M, NB, oku, fig, svg_wrap, text, INK, saat_oku, saat_svg, cetele, sutun_grafigi, basamak_tablosu
from tr_g7 import gen

RED = "#e07a5f"
BLUE = "#3b82c4"

BENDA = {"apple": "elma", "star": "yıldız", "ball": "top", "button": "düğme", "fish": "balık", "flower": "çiçek",
         "duck": "ördek", "cup": "bardak", "bug": "uğur böceği"}
KINDS = list(BENDA)
SHAPE = {"circle": "daire", "triangle": "üçgen", "square": "kare", "rectangle": "dikdörtgen", "hexagon": "altıgen"}
RENK = {"red": "kırmızı", "blue": "mavi", "yellow": "sarı", "green": "yeşil"}
SIDES = {"circle": 0, "triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6}


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def rnd():
    return G.R.random()


def nm():
    return G.K.next()


def cap(s):
    return A.cap(s)


def named(f, n):
    f.__name__ = n
    return f


def b(kind):
    return BENDA[kind]


def pic(svg, label, lg=False):
    svg = re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label.replace("'", "’"), svg, count=1)
    if lg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return svg if svg.startswith("<div") else fig(svg)


def near(n, lo=0, hi=100, ds=(1, -1, 2, -2, 10, -10)):
    return [str(n + d) for d in ds if lo <= n + d <= hi and d != 0]


def mq(q, g, ws, e):
    return M(q, g, ws, e)


# ------------------------------------------------------------ 絵
def sira(n, kind):
    return pic(P.row_svg(n, kind, 10 if n > 5 else 5), "%d %s yan yana" % (n, b(kind)))


def dagin(n, kind, cols=None, rows=None):
    return pic(P.scatter_svg(n, kind, ri(1, 99999), cols, rows), "%d %s" % (n, b(kind)))


def cerceve(n):
    return pic(P.tenframe_svg(n), "%d noktalı onluk çerçeve" % n) if n <= 10 else pic(P.tenframe_svg(n, 2), "%d noktalı iki onluk çerçeve" % n)


def zar(vals):
    return pic(P.dice_svg(vals), "zar: " + ", ".join(map(str, vals)))


def iki(a, ka, c, kb, sign):
    return pic(P.two_groups_svg(a, ka, c, kb, sign), "%d %s %s %d %s" % (a, b(ka), "ve" if sign == "+" else sign, c, b(kb)))


def cizik(n, kind, k):
    return pic(P.crossed_row_svg(n, kind, k, 5), "%d %s, %d tanesinin üstü çizili" % (n, b(kind), k))


def kutu(n, kind):
    return pic(P.box_svg(n, kind), "%d %s ve kapalı bir kutu" % (n, b(kind)))


def atla(start, hops, lo, hi):
    return pic(P.hop_line_svg(start, hops, lo, hi), "atlamalı sayı doğrusu")


def bag(w, x, y):
    return pic(P.bond_svg(w, x, y), "parça-bütün şeması")


def onluk(t, o):
    return pic(P.rods_svg(t, o), "%d onluk ve %d birlik" % (t, o))


def kule(hs):
    return pic(P.towers_svg(hs), "küp kuleleri")


def terazi(left, right, tilt):
    return pic(P.balance_svg(left, right, tilt), "eşit kollu terazi")


def gruplar(g, k, kind):
    return pic(P.groups_svg([(k, kind)] * g), "%d grup, her grupta %d %s" % (g, k, b(kind)))


def dizi(r, c, kind):
    return pic(P.array_svg(r, c, kind), "%d sıra, her sırada %d %s" % (r, c, b(kind)))


COLS = {"yellow": "#f4d03f", "red": "#e74c3c", "blue": "#3498db", "green": "#27ae60"}


def prizma_svg(color="#f4d03f"):
    s = ("<rect x='20' y='50' width='120' height='60' fill='%s' stroke='%s' stroke-width='2'/>"
         "<polygon points='20,50 50,24 170,24 140,50' fill='%s' fill-opacity='0.6' stroke='%s' stroke-width='2'/>"
         "<polygon points='140,50 170,24 170,84 140,110' fill='%s' stroke='%s' stroke-width='2'/>"
         "<polygon points='140,50 170,24 170,84 140,110' fill='#000' fill-opacity='0.15'/>" % (color, INK, color, INK, color, INK))
    return svg_wrap(190, 126, s, "dikdörtgenler prizması")


def cisim_svg(kind, color="yellow", r=40):
    if kind == "prism":
        return prizma_svg(COLS[color]).replace("viewBox='0 0 190 126'", "viewBox='0 0 190 126' style='width:%dpx'" % (r * 4.5), 1)
    return P.one_solid_svg(kind, color, r)


CISIM = {"sphere": "küre", "cube": "küp", "cylinder": "silindir", "cone": "koni", "prism": "dikdörtgenler prizması"}


# ============================================================ sayılar
def m_say(lo, hi):
    def f():
        n, kind = ri(lo, hi), ch(KINDS)
        k = ri(0, 2) if n <= 10 else ch([0, 1, 2]) if n <= 16 else ch([0, 2])
        p = sira(n, kind) if k == 0 else dagin(n, kind) if k == 1 else cerceve(n) if n <= 20 else sira(n, kind)
        what = "nokta" if (k == 2 and n <= 20) else b(kind)
        return mq("Kaç %s var?%s" % (what, p), num(n), near(n, 0, 100, (1, -1, 2, -2)), "Birer birer sayarız. <b>%d</b> %s var." % (n, what))
    return named(f, "say")


def m_okunus(lo, hi):
    def f():
        n = ri(lo, hi)
        ws = [x for x in (int(str(n)[::-1]) if n > 10 and n % 10 else n + 2, n + 1, n - 1, n + 10, n - 10, n + 2) if 0 <= x <= 100 and x != n]
        if rnd() < 0.5:
            return mq("“%s” sayısı rakamla nasıl yazılır?" % oku(n), num(n), [num(x) for x in ws], "%s: <b>%d</b>." % (cap(oku(n)), n))
        return mq("<b>%d</b> sayısı nasıl okunur?" % n, cap(oku(n)), [cap(oku(x)) for x in ws], "%d: <b>%s</b>." % (n, oku(n)))
    return named(f, "okunus")


def m_once_sonra(lo, hi, steps=(1,)):
    def f():
        n, d = ri(lo, hi), ch(steps)
        k = ri(0, 2)
        if k == 0:
            if n + d > hi:
                return None
            q = "%d sayısından hemen sonra gelen sayı hangisidir?" % n if d == 1 else "%d sayısının %d fazlası kaçtır?" % (n, d)
            return mq(q, num(n + d), [num(n - d)] + near(n + d, 0, 120, (1, -1, 10 if d == 1 else 1)), "%d + %d = <b>%d</b>." % (n, d, n + d))
        if k == 1:
            if n - d < max(lo, 0):
                return None
            q = "%d sayısından hemen önce gelen sayı hangisidir?" % n if d == 1 else "%d sayısının %d eksiği kaçtır?" % (n, d)
            return mq(q, num(n - d), [num(n + d)] + near(n - d, 0, 120, (1, -1, 2)), "%d − %d = <b>%d</b>." % (n, d, n - d))
        if n - 1 < lo or n + 1 > hi or d != 1:
            return None
        return mq("%d ile %d arasındaki sayı hangisidir?" % (n - 1, n + 1), num(n), [num(n - 1), num(n + 1), num(n + 2), num(n - 2)],
                  "Sıra: %d, <b>%d</b>, %d." % (n - 1, n, n + 1))
    return named(f, "once_sonra")


def m_eksik(lo, hi, steps=(1,), down=None):
    def f():
        d = ch(steps)
        s = ri(lo, hi - 4 * d)
        if d > 1 and rnd() < 0.7:
            s = s // d * d
        if s < lo:
            return None
        xs = [s + d * i for i in range(5)]
        dn = (rnd() < 0.3) if down is None else down
        if dn:
            xs = xs[::-1]
        j = ri(1, 4)
        show = ", ".join(str(x) if i != j else "…" for i, x in enumerate(xs))
        return mq("Boş bırakılan yere hangi sayı gelir?<br>%s" % show, num(xs[j]), near(xs[j], 0, 120, (1, -1, d + 1, -d - 1, 2 * d)),
                  "Sayılar %s %s %s. Boşluğa <b>%d</b> gelir." % (A.dagit(d), A.dagit(d), "azalıyor" if dn else "artıyor", xs[j]))
    return named(f, "eksik")


def m_cok_az(hi):
    def f():
        a, c = ri(2, hi), ri(2, hi)
        k1, k2 = sh(KINDS)[:2]
        if a == c and rnd() < 0.6:
            return None
        q = ch(["daha çok", "daha az"])
        if a == c:
            g = "Eşit sayıda"
        elif q == "daha çok":
            g = cap(b(k1)) if a > c else cap(b(k2))
        else:
            g = cap(b(k1)) if a < c else cap(b(k2))
        return mq("Hangisinden %s var?%s%s" % (q, sira(a, k1), sira(c, k2)), g, [x for x in (cap(b(k1)), cap(b(k2)), "Eşit sayıda", "Bilinemez") if x != g],
                  "%d %s, %d %s var. Cevap: <b>%s</b>." % (a, b(k1), c, b(k2), g))
    return named(f, "cok_az")


def m_karsilastir(lo, hi):
    def f():
        a, c = ri(lo, hi), ri(lo, hi)
        if a == c and rnd() < 0.7:
            return None
        g = "&lt;" if a < c else "&gt;" if a > c else "="
        return mq("%d ○ %d<br>Daireye hangi işaret gelir?" % (a, c), g, [x for x in ("&lt;", "&gt;", "=", "+") if x != g],
                  "%d, %d sayısından %s: <b>%d %s %d</b>." % (a, c, "küçüktür" if a < c else "büyüktür" if a > c else "eşittir", a, g, c) if a != c else "İki sayı eşittir: <b>%d = %d</b>." % (a, c))
    return named(f, "karsilastir")


def m_en(lo, hi):
    def f():
        xs = sorted(set(ri(lo, hi) for _ in range(6)))
        if len(xs) < 4:
            return None
        xs = sh(xs)[:4]
        big = rnd() < 0.5
        c = max(xs) if big else min(xs)
        return mq("%s sayılarından en %s hangisidir?" % (", ".join(map(str, xs)), "büyüğü" if big else "küçüğü"), num(c), [num(x) for x in xs if x != c],
                  "En %s sayı <b>%d</b>." % ("büyük" if big else "küçük", c))
    return named(f, "en")


def m_sirala(lo, hi):
    def f():
        xs = sorted(set(ri(lo, hi) for _ in range(6)))
        if len(xs) < 4:
            return None
        xs = sh(xs)[:4]
        up = rnd() < 0.5
        g = sorted(xs, reverse=not up)
        w3 = list(g)
        w3[1], w3[2] = w3[2], w3[1]
        fm = lambda ys: ", ".join(map(str, ys))
        return mq("%s sayılarını %s sıralayınız." % (fm(xs), "küçükten büyüğe" if up else "büyükten küçüğe"), fm(g),
                  [fm(g[::-1]), fm(w3), fm(xs) if xs != g else fm(w3[::-1])], "Sıralama: <b>%s</b>." % fm(g))
    return named(f, "sirala")


ORD = ["birinci", "ikinci", "üçüncü", "dördüncü", "beşinci", "altıncı", "yedinci", "sekizinci", "dokuzuncu", "onuncu"]


def m_sira_sayisi():
    def f():
        ks = sh(KINDS)[:5]
        p = pic(P.kinds_row_svg(ks), "sıra: " + ", ".join(b(x) for x in ks))
        k = ri(0, 2)
        side = ch(["soldan", "sağdan"])
        if k == 0:
            pos = ri(1, 5)
            j = pos - 1 if side == "soldan" else 5 - pos
            return mq("%s %d. sıradaki nesne hangisidir?%s" % (cap(side), pos, p), cap(b(ks[j])), [cap(b(x)) for x in ks if x != ks[j]],
                      "%s sayarız: %d. sırada <b>%s</b> var." % (cap(side), pos, b(ks[j])))
        if k == 1:
            j = ri(0, 4)
            pos = j + 1 if side == "soldan" else 5 - j
            return mq("%s %s kaçıncı sıradadır?%s" % (cap(b(ks[j])), side, p), "%d." % pos, ["%d." % x for x in range(1, 6) if x != pos],
                      "%s sayarız: %s <b>%d.</b> sırada." % (cap(side), b(ks[j]), pos))
        j = ri(0, 4)
        pos = j + 1
        return mq("Soldan %s sıradaki nesne hangisidir?%s" % (ORD[pos - 1], p), cap(b(ks[j])), [cap(b(x)) for x in ks if x != ks[j]],
                  "Soldan %s: <b>%s</b>." % (ORD[pos - 1], b(ks[j])))
    return named(f, "sira_sayisi")


def m_yaris():
    def f():
        n = ri(6, 10)
        x = nm()
        p = ri(2, n - 1)
        k = ri(0, 2)
        if k == 0:
            return mq("Bir koşuda %d çocuk yarıştı. %s %d. oldu. %s önünde kaç çocuk var?" % (n, x, p, cap(gen(x))) if False else
                      "Bir koşuda %d çocuk var. %s yarışı %s bitirdi. %s önünde kaç çocuk vardı?" % (n, x, ORD[p - 1] + " olarak", gen(x)),
                      num(p - 1), [num(p), num(p + 1), num(n - p)] if n - p not in (p - 1, p, p + 1) else [num(p), num(p + 1), num(p + 2)],
                      "%s olan çocuğun önünde <b>%d</b> çocuk vardır." % (cap(ORD[p - 1]), p - 1))
        if k == 1:
            return mq("Bir sırada %d çocuk var. %s baştan %s. %s arkasında kaç çocuk var?" % (n, x, ORD[p - 1], gen(x)), num(n - p),
                      [num(n - p + 1), num(p - 1) if p - 1 != n - p else num(n - p + 2), num(p)],
                      "%d çocuktan baştaki %d çocuk çıkarılır: %d − %d = <b>%d</b>." % (n, p, n, p, n - p))
        return mq("Bir sırada %d çocuk var. %s baştan %s, sondan kaçıncıdır?" % (n, x, ORD[p - 1]), "%d." % (n - p + 1),
                  ["%d." % v for v in (n - p, n - p + 2, p) if v != n - p + 1 and v > 0] + ["%d." % n],
                  "Sondan sayarız: %d − %d + 1 = <b>%d.</b>" % (n, p, n - p + 1))
    return named(f, "yaris")


def m_ritmik(mx, steps, down=False, lo=0):
    def f():
        d = ch(steps)
        if down:
            s = ri(lo + 5 * d, mx)
            if d > 1:
                s = s // d * d
            xs = [s - d * i for i in range(5)]
            if xs[-1] - d < lo:
                return None
            nx = xs[-1] - d
        else:
            s = ri(lo, mx - 5 * d)
            if d > 1 and rnd() < 0.8:
                s = s // d * d
            xs = [s + d * i for i in range(5)]
            nx = xs[-1] + d
            if nx > mx:
                return None
        return mq("%s %s %s sayıyoruz: %s, … Sıradaki sayı hangisidir?" % (cap(A.dagit(d)), A.dagit(d), "geriye" if down else "ileriye", ", ".join(map(str, xs))),
                  num(nx), near(nx, 0, 120, (1, -1, d + 1, -d - 1)) + [num(xs[-1])],
                  "Her adımda %d %s. Sıradaki sayı <b>%d</b>." % (d, "azalıyor" if down else "artıyor", nx))
    return named(f, "ritmik_geri" if down else "ritmik")


def m_atlama_kac(mx, steps):
    def f():
        d = ch(steps)
        n = ri(2, min(10, mx // d))
        return mq("Sıfırdan başlayıp %s %s sayan Ela %d sayısına kadar kaç sayı söyler? (Sıfırı saymayın.)" % (A.dagit(d), A.dagit(d), n * d), num(n),
                  [num(n + 1), num(n * d), num(n - 1)], "%s: %s → <b>%d</b> sayı." % (A.dagit(d), ", ".join(str(d * i) for i in range(1, n + 1)), n))
    return named(f, "atlama_kac")


def m_tahmin(mx, step):
    def f():
        g = ri(1, mx // step) * step
        n = g + ch([-2, -1, 0, 1, 2]) if step >= 5 else g
        if n < 3 or n > mx:
            return None
        kind = ch(["dot", "star", "button", "ball", "flower"])
        cols = 6 if mx <= 20 else 10
        rows = math.ceil(max(n, 20) / float(cols)) + 1
        p = pic(P.scatter_svg(n, kind, ri(1, 99999), cols, rows), "bir grup nesne", lg=mx > 20)
        ws = ["Yaklaşık %d" % (g + d) for d in (step, -step, 2 * step, -2 * step) if 0 < g + d <= mx + step]
        return mq("Resimde yaklaşık kaç nesne var? Saymadan tahmin ediniz.%s" % p, "Yaklaşık %d" % g, ws,
                  "Tam %d nesne var; en yakın tahmin <b>yaklaşık %d</b>." % (n, g))
    return named(f, "tahmin")


def m_tahmin_kiyas(mx):
    def f():
        ref = ch([5, 10]) if mx <= 20 else ch([10, 20])
        n = ri(ref + 2, mx)
        kind = ch(["dot", "star", "button"])
        cols = 6 if mx <= 20 else 10
        rows = math.ceil(max(n, 20) / float(cols)) + 1
        p = pic(P.scatter_svg(n, kind, ri(1, 99999), cols, rows), "bir grup nesne", lg=mx > 20)
        g = "%d sayısından çok" % ref
        return mq("Bir avuçta %d nesne olduğunu biliyoruz. Resimdeki nesneler için hangisi doğrudur?%s" % (ref, p), g,
                  ["%d sayısından az" % ref, "Tam %d" % ref, "Hiç yok"],
                  "Resimde %d nesne var: <b>%s</b>." % (n, g))
    return named(f, "tahmin_kiyas")


# ============================================================ örüntüler
POLA_SH = ["circle", "triangle", "square"]


def m_oruntu():
    def f():
        k = ri(0, 1)
        unit_len = ch([2, 2, 3, 3, 4])
        if k == 0:
            base = [("shape", s, c) for s, c in zip(sh(POLA_SH)[:3], sh(list(RENK))[:3])]
            name_ = lambda it: "%s %s" % (RENK[it[2]], SHAPE[it[1]])
        else:
            base = [("obj", x) for x in sh(KINDS)[:3]]
            name_ = lambda it: b(it[1])
        tpl = ch({2: ["AB"], 3: ["ABC", "AAB", "ABB"], 4: ["AABB", "ABAC"]}[unit_len])
        seq = [base["ABC".index(c)] for c in tpl] * 3
        L = ri(len(tpl) + 2, min(len(seq) - 1, 8))
        shown, nxt = seq[:L], seq[L]
        cands = sorted({name_(x) for x in base})
        return mq("Örüntüde boş kutuya ne gelir?%s" % pic(pattern_svg(shown, 1), "tekrarlayan örüntü"), cap(name_(nxt)),
                  [cap(c) for c in cands if c != name_(nxt)] + ["Hiçbiri"],
                  "Örüntü birimi: %s. Sıradaki <b>%s</b>." % (", ".join(name_(x) for x in seq[:len(tpl)]), name_(nxt)))
    return named(f, "oruntu")


def m_sekil_say_oruntu():
    def f():
        a, d = ri(1, 5), ri(1, 4)
        st = ri(4, 5)
        xs = [a + d * i for i in range(st)]
        if xs[-1] > 20:
            return None
        svg = A.kareler(xs[:3])
        svg = svg if svg.startswith("<div") else fig(svg)
        v = xs[st - 1]
        return mq("Şekil örüntüsünde her adımda kare sayısı aynı miktarda artıyor. %d. adımda kaç kare olur?%s" % (st, svg), num(v),
                  [num(v + d), num(xs[2] + 1) if xs[2] + 1 != v else num(v + 2 * d), num(v + 1), num(v - 1)],
                  "Kareler %s, %s, %s: her adımda %d artar. %s. adım: <b>%d</b>." % (xs[0], xs[1], xs[2], d, st, v))
    return named(f, "sekil_say_oruntu")


# ============================================================ toplama ve çıkarma
def m_topla_resim(mx):
    def f():
        a, c = ri(1, min(10, mx - 1)), ri(1, min(10, mx - 1))
        if a + c > mx:
            return None
        k1, k2 = sh(KINDS)[:2]
        return mq("Hepsi kaç tane eder?%s" % iki(a, k1, c, k2, "+"), num(a + c), near(a + c, 1, 30, (1, -1, 2)) + [num(abs(a - c)) if a != c else None],
                  "%d + %d = <b>%d</b>." % (a, c, a + c))
    return named(f, "topla_resim")


def m_islem(op, lo, hi, carry=None):
    """op '+' / '-'。carry: None=どちらでも、True=eldeli/bozarak、False=eldesiz"""
    def f():
        if op == "+":
            a, c = ri(lo, hi), ri(1, hi)
            s = a + c
            if s > hi or s < lo:
                return None
            el = (a % 10 + c % 10) >= 10
            if carry is not None and el != carry:
                return None
            ws = [s + 1, s - 1, s + 10, s - 10, abs(a - c)]
            return mq("%d + %d = ?" % (a, c), num(s), [num(w) for w in ws if 0 <= w <= 200 and w != s], "%d + %d = <b>%d</b>." % (a, c, s))
        a = ri(lo, hi)
        c = ri(1, a - 1) if a > 1 else 1
        if c >= a:
            return None
        bz = (a % 10) < (c % 10)
        if carry is not None and bz != carry:
            return None
        v = a - c
        ws = [v + 1, v - 1, v + 10, v - 10, a + c, abs((a % 10) - (c % 10)) + (a // 10 - c // 10) * 10]
        return mq("%d − %d = ?" % (a, c), num(v), [num(w) for w in ws if 0 <= w <= 200 and w != v], "%d − %d = <b>%d</b>." % (a, c, v))
    return named(f, "islem")


def m_cizik(mx):
    def f():
        n, kind = ri(3, min(mx, 15)), ch(KINDS)
        k = ri(1, n - 1)
        return mq("%d %s vardı. Üstü çizili olanlar gitti. Kaç %s kaldı?%s" % (n, b(kind), b(kind), cizik(n, kind, k)), num(n - k),
                  near(n - k, 0, 30, (1, -1, 2)) + [num(n + k), num(k)], "%d − %d = <b>%d</b>." % (n, k, n - k))
    return named(f, "cizik")


def m_atla(op, mx):
    def f():
        hi = 10 if mx <= 10 else 20
        s, h = ri(0, hi), ri(1, 5)
        if op == "+":
            if s + h > hi:
                return None
            lo_ = 0 if (hi == 10 or s + h <= 10) else 10
            if lo_ == 10 and s < 10:
                return None
            return mq("%d sayısından başla, sağa doğru %d adım atla. Hangi sayıya varırsın?%s" % (s, h, atla(s, h, lo_, lo_ + 10)), num(s + h),
                      near(s + h, 0, 20, (1, -1, 2)) + [num(s - h) if s >= h else None], "%d + %d = <b>%d</b>." % (s, h, s + h))
        if s - h < 0:
            return None
        lo_ = 0 if s <= 10 else 10
        if lo_ == 10 and s - h < 10:
            return None
        return mq("%d sayısından başla, sola doğru %d adım atla. Hangi sayıya varırsın?%s" % (s, h, atla(s, -h, lo_, lo_ + 10)), num(s - h),
                  near(s - h, 0, 20, (1, -1, 2)) + [num(s + h)], "%d − %d = <b>%d</b>." % (s, h, s - h))
    return named(f, "atla")


def m_kutu(mx):
    def f():
        t, kind = ri(4, min(mx, 20)), ch(KINDS)
        n = ri(1, min(t - 1, 10))
        return mq("Toplam %d %s var. Dışarıda olanları görüyorsun, gerisi kutunun içinde. Kutuda kaç %s var?%s" % (t, b(kind), b(kind), kutu(n, kind)), num(t - n),
                  near(t - n, 0, 30, (1, -1, 2)) + [num(t + n), num(n)], "%d − %d = <b>%d</b>." % (t, n, t - n))
    return named(f, "kutu")


def m_parca_butun(mx):
    def f():
        w = ri(3, mx)
        a = ri(1, w - 1)
        k = ri(0, 2)
        x = [str(w), str(a), str(w - a)]
        g = x[k]
        x[k] = "?"
        return mq("Soru işaretinin yerine hangi sayı gelir?%s" % bag(*x), g, near(int(g), 0, 120, (1, -1, 2)) + [str(w + a)],
                  "%d + %d = %d. Cevap: <b>%s</b>." % (a, w - a, w, g))
    return named(f, "parca_butun")


def m_bos(mx, lo=1):
    def f():
        a, c = ri(lo, mx), ri(1, mx)
        if a + c > mx:
            return None
        s = a + c
        k = ri(0, 3)
        q = ["%d + … = %d" % (a, s), "… + %d = %d" % (c, s), "%d − … = %d" % (s, a), "… − %d = %d" % (c, a)][k]
        g = [c, a, c, s][k]
        return mq("Noktalı yere hangi sayı gelir?<br>%s" % q, num(g), near(g, 0, 200, (1, -1, 2, 10)) + [num(s + (a if k != 1 else c))],
                  "%d + %d = %d. Cevap: <b>%d</b>." % (a, c, s, g))
    return named(f, "bos")


def m_iliski(mx):
    def f():
        a, c = ri(1, mx - 1), ri(1, mx - 1)
        if a + c > mx or a == c:
            return None
        s = a + c
        k = ri(0, 1)
        if k == 0:
            g = "%d − %d = %d" % (s, a, c)
            return mq("%d + %d = %d ise hangi çıkarma işlemi doğrudur?" % (a, c, s), g,
                      ["%d − %d = %d" % (a, c, s), "%d − %d = %d" % (s, a, s), "%d − %d = %d" % (c, a, s)],
                      "Toplamdan bir toplanan çıkarılınca diğer toplanan bulunur: <b>%s</b>." % g)
        g = "%d + %d = %d" % (c, a, s)
        return mq("%d − %d = %d ise hangi toplama işlemi doğrudur?" % (s, a, c), g,
                  ["%d + %d = %d" % (s, a, c), "%d + %d = %d" % (s, c, a), "%d + %d = %d" % (a, s, c)],
                  "Fark ile çıkan toplanınca eksilen bulunur: <b>%s</b>." % g)
    return named(f, "iliski")


def m_tahmin_islem(lo, hi):
    def f():
        a, c = ri(lo, hi), ri(lo, hi)
        op = ch("+-")
        if op == "-" and c >= a:
            a, c = c, a
        if a == c:
            return None
        v = a + c if op == "+" else a - c
        ra, rc = int(math.floor(a / 10.0 + 0.5)) * 10, int(math.floor(c / 10.0 + 0.5)) * 10
        rv = ra + rc if op == "+" else ra - rc
        if rv <= 0:
            return None
        return mq("%d %s %d işleminin sonucu yaklaşık kaçtır? (Sayıları en yakın onluğa yuvarlayınız.)" % (a, "+" if op == "+" else "−", c), "Yaklaşık %d" % rv,
                  ["Yaklaşık %d" % x for x in (rv + 10, rv - 10, rv + 20) if x > 0] + ["Yaklaşık %d" % (rv + 30)],
                  "%d → %d, %d → %d. %d %s %d = <b>%d</b>. (Tam sonuç %d.)" % (a, ra, c, rc, ra, "+" if op == "+" else "−", rc, rv, v))
    return named(f, "tahmin_islem")


TOP_C = [(lambda x, a, c: "%s %d bilye aldı. Sonra %d bilye daha aldı. Şimdi kaç bilyesi var?" % (x, a, c), "bilye"),
         (lambda x, a, c: "Havuzda %d balık vardı. %d balık daha geldi. Havuzda kaç balık oldu?" % (a, c), "balık"),
         (lambda x, a, c: "%s %d portakal ve %d mandalina topladı. Kaç meyve topladı?" % (x, a, c), "meyve"),
         (lambda x, a, c: "Dalda %d kuş vardı. %d kuş daha kondu. Dalda kaç kuş oldu?" % (a, c), "kuş"),
         (lambda x, a, c: "%s okula %d kırmızı ve %d mavi kalem getirdi. Kaç kalem getirdi?" % (x, a, c), "kalem"),
         (lambda x, a, c: "Bahçede %d çocuk top oynuyor, %d çocuk ip atlıyor. Bahçede kaç çocuk var?" % (a, c), "çocuk")]
CIK_C = [(lambda x, a, c: "%s %d şekeri vardı. %d şekerini yedi. Kaç şekeri kaldı?" % (gen(x), a, c), "şeker"),
         (lambda x, a, c: "%d balon vardı. %d balon patladı. Kaç balon kaldı?" % (a, c), "balon"),
         (lambda x, a, c: "Ağaçta %d elma vardı. Annem %d elma topladı. Ağaçta kaç elma kaldı?" % (a, c), "elma"),
         (lambda x, a, c: "Otobüste %d yolcu vardı. %d yolcu indi. Otobüste kaç yolcu kaldı?" % (a, c), "yolcu"),
         (lambda x, a, c: "%s %d çıkartması vardı. %d çıkartmasını kardeşine verdi. Kaç çıkartması kaldı?" % (gen(x), a, c), "çıkartma")]
FARK_C = [(lambda x, y, a, c: "%s %d kitap okudu. %s %d kitap okudu. Aralarında kaç kitap fark var?" % (x, a, y, c), "kitap"),
          (lambda x, y, a, c: "Kümeste %d tavuk ve %d ördek var. Tavuklar ördeklerden kaç fazla?" % (a, c), "tane")]


def m_problem(mx, kinds="+-="):
    def f():
        k = ch(kinds)
        x = nm()
        if k == "+":
            t, un = ch(TOP_C)
            a, c = ri(1, mx - 1), ri(1, mx - 1)
            if a + c > mx:
                return None
            q = t(x, a, c)
            v, e = a + c, "Birleştirme var, toplarız: %d + %d = <b>%d</b>." % (a, c, a + c)
            ws = [abs(a - c), v + 1, v - 1, v + 10]
        elif k == "-":
            t, un = ch(CIK_C)
            a = ri(3, mx)
            c = ri(1, a - 1)
            q = t(x, a, c)
            v, e = a - c, "Eksilme var, çıkarırız: %d − %d = <b>%d</b>." % (a, c, a - c)
            ws = [a + c, v + 1, v - 1, v + 10]
        else:
            t, un = ch(FARK_C)
            a, c = ri(5, mx), ri(1, mx)
            if c >= a:
                return None
            y = nm()
            if y == x:
                return None
            q = t(x, y, a, c)
            v, e = a - c, "Fark için çıkarırız: %d − %d = <b>%d</b>." % (a, c, a - c)
            ws = [a + c, v + 1, v - 1, v + 10]
        return mq(q, "%d %s" % (v, un), ["%d %s" % (w, un) for w in ws if w >= 0 and w != v], e)
    return named(f, "problem")


def m_esit(mx):
    def f():
        a, c = ri(1, mx - 1), ri(1, mx - 1)
        s = a + c
        if s > mx:
            return None
        d = ri(1, s - 1)
        if d in (a, c):
            return None
        k = ri(0, 2)
        if k == 0:
            g = s - d
            return mq("%d + %d = %d + …<br>Noktalı yere hangi sayı gelir?" % (a, c, d), num(g), [num(s), num(s + d), num(g + 1)],
                      "Eşittir işaretinin iki yanı aynı değeri gösterir: %d + %d = %d, %d + %d = %d. Cevap: <b>%d</b>." % (a, c, s, d, g, s, g))
        if k == 1:
            good = "%d + %d" % (d, s - d)
            return mq("Hangisi %d + %d ile aynı değerdedir?" % (a, c), good, ["%d + %d" % (d, s - d + 1), "%d − %d" % (s, d), "%d + %d" % (d + 1, s - d + 1)],
                      "İkisi de %d eder: <b>%s</b>." % (s, good))
        t = ch([True, False])
        dd = s - d if t else s - d + ch([1, -1, 2])
        if dd < 0:
            return None
        g = "Doğru" if t else "Yanlış"
        return mq("%d + %d = %d + %d eşitliği doğru mu, yanlış mı?" % (a, c, d, dd), g, ["Yanlış" if t else "Doğru", "Bilinemez", "Yalnızca ters yazılırsa doğru"],
                  "Sol taraf %d, sağ taraf %d: <b>%s</b>." % (s, d + dd, g.lower()))
    return named(f, "esit")


def m_terazi_sayi(mx):
    def f():
        a, c = ri(1, 9), ri(1, 9)
        s = a + c
        if s > mx:
            return None
        d = ri(1, s - 1)
        return mq("Terazi dengede. Sol kefede %d ve %d, sağ kefede %d ve bir kutu var. Kutuda kaç olmalı?" % (a, c, d), num(s - d),
                  [num(s), num(s - d + 1), num(s + d)], "%d + %d = %d. %d + %d = %d. Cevap: <b>%d</b>." % (a, c, s, d, s - d, s, s - d))
    return named(f, "terazi_sayi")


# ============================================================ şekiller, cisimler, konum
def m_sekil_ad(kinds=("circle", "triangle", "square", "rectangle")):
    def f():
        k, col = ch(kinds), ch(list(RENK))
        rot = ch([0, 0, 20, -20]) if k != "circle" else 0
        return mq("Bu şeklin adı nedir?%s" % pic(P.one_shape_svg(k, col, 40, rot), "%s bir şekil" % RENK[col]), cap(SHAPE[k]),
                  [cap(SHAPE[x]) for x in SHAPE if x != k], "Bu şekil bir <b>%s</b>." % SHAPE[k])
    return named(f, "sekil_ad")


def m_sekil_bul(kinds=("circle", "triangle", "square", "rectangle")):
    def f():
        ks = sh(kinds)[:4]
        items = [(k, ch(list(RENK))) for k in ks]
        t = ch(ks)
        L = "ABCD"[ks.index(t)]
        return mq("Hangisi %s?%s" % (SHAPE[t], pic(P.lettered_shapes_svg(items), "A, B, C ve D şekilleri")), L, [c for c in "ABCD" if c != L],
                  "%s şekli <b>%s</b>." % (L, SHAPE[t]))
    return named(f, "sekil_bul")


def m_kenar(kinds=("triangle", "square", "rectangle", "hexagon")):
    def f():
        k, col = ch(kinds), ch(list(RENK))
        what = ch(["kenarı", "köşesi"])
        n = SIDES[k]
        return mq("Bu şeklin kaç %s vardır?%s" % (what, pic(P.one_shape_svg(k, col, 40, ch([0, 15, -15])), SHAPE[k])), num(n),
                  [num(x) for x in (n + 1, n - 1, n + 2, 0) if x != n], "%s: %d kenar, %d köşe. Cevap: <b>%d</b>." % (cap(SHAPE[k]), n, n, n))
    return named(f, "kenar")


def m_sekil_say():
    def f():
        t = ch(["circle", "triangle", "square"])
        n = ri(1, 5)
        others = [k for k in ("circle", "triangle", "square", "rectangle") if k != t]
        items = [(t, ch(list(RENK))) for _ in range(n)] + [(ch(others), ch(list(RENK))) for _ in range(ri(3, 7))]
        if len(items) > 15:
            return None
        G.R.shuffle(items)
        return mq("Resimde kaç %s var?%s" % (SHAPE[t], pic(P.shapes_mix_svg(items, ri(1, 9999)), "karışık şekiller")), num(n),
                  [num(x) for x in (n + 1, n - 1, n + 2, len(items)) if x != n and x >= 0], "<b>%d</b> %s var." % (n, SHAPE[t]))
    return named(f, "sekil_say")


GERCEK_SEKIL = [("duvar saati", "daire"), ("bisiklet tekerleği", "daire"), ("madenî para", "daire"), ("tabak", "daire"),
                ("yazı tahtası", "dikdörtgen"), ("kapı", "dikdörtgen"), ("defter", "dikdörtgen"), ("Türk bayrağı", "dikdörtgen"),
                ("yer karosu", "kare"), ("mendil", "kare"), ("satranç tahtası", "kare"),
                ("üçgen sandviç", "üçgen"), ("uyarı levhası", "üçgen"), ("çatı (önden)", "üçgen")]


def m_sekil_gercek():
    def f():
        o, g = ch(GERCEK_SEKIL)
        return mq("%s hangi şekle benzer?" % cap(o), cap(g), [cap(x) for x in ("daire", "üçgen", "kare", "dikdörtgen") if x != g],
                  "%s <b>%s</b> şeklindedir." % (cap(o), g))
    return named(f, "sekil_gercek")


GERCEK_CISIM = [("futbol topu", "küre"), ("misket", "küre"), ("portakal", "küre"), ("zar", "küp"), ("küp şeker", "küp"),
                ("konserve kutusu", "silindir"), ("bardak", "silindir"), ("davul", "silindir"), ("doğum günü şapkası", "koni"), ("dondurma külahı", "koni"),
                ("trafik konisi", "koni"), ("ayakkabı kutusu", "dikdörtgenler prizması"), ("dolap", "dikdörtgenler prizması"), ("tuğla", "dikdörtgenler prizması"),
                ("kibrit kutusu", "dikdörtgenler prizması")]


def m_cisim_ad():
    def f():
        k = ch(list(CISIM))
        return mq("Bu geometrik cismin adı nedir?%s" % pic(cisim_svg(k, ch(list(COLS)), ri(34, 44)), "geometrik cisim"), cap(CISIM[k]),
                  [cap(CISIM[x]) for x in CISIM if x != k], "Bu cisim <b>%s</b>." % CISIM[k])
    return named(f, "cisim_ad")


def m_cisim_gercek():
    def f():
        o, g = ch(GERCEK_CISIM)
        if rnd() < 0.5:
            others = sh([x for x, y in GERCEK_CISIM if y != g])[:3]
            return mq("Hangisi %s şeklindedir? (%s)" % (g, ", ".join(sorted([o] + others))), cap(o), [cap(x) for x in others], "%s <b>%s</b> şeklindedir." % (cap(o), g))
        return mq("%s hangi geometrik cisme benzer?" % cap(o), cap(g), [cap(x) for x in CISIM.values() if x != g], "%s <b>%s</b> şeklindedir." % (cap(o), g))
    return named(f, "cisim_gercek")


def m_yuvarlanir():
    def f():
        if rnd() < 0.5:
            g = ch(["küre", "silindir", "koni"])
            o, _ = ch([x for x in GERCEK_CISIM if x[1] == g])
            bad = sh([x for x, y in GERCEK_CISIM if y in ("küp", "dikdörtgenler prizması")])[:3]
            return mq("Hangisi yuvarlanabilir? (%s)" % ", ".join(sorted([o] + bad)), cap(o), [cap(x) for x in bad],
                      "%s %s şeklindedir; eğri yüzeyi olduğu için yuvarlanır. Cevap: <b>%s</b>." % (cap(o), g, o))
        g = ch(["küp", "dikdörtgenler prizması"])
        o, _ = ch([x for x in GERCEK_CISIM if x[1] == g])
        bad = sh([x for x, y in GERCEK_CISIM if y in ("küre", "silindir", "koni")])[:3]
        return mq("Hangisi yuvarlanamaz? (%s)" % ", ".join(sorted([o] + bad)), cap(o), [cap(x) for x in bad],
                  "%s %s şeklindedir; bütün yüzleri düz olduğu için yuvarlanmaz. Cevap: <b>%s</b>." % (cap(o), g, o))
    return named(f, "yuvarlanir")


def m_masa():
    def f():
        kind = ch(KINDS)
        r = ch(["above", "below", "beside", "beside-left"])
        T = {"above": "masanın üstünde", "below": "masanın altında", "beside": "masanın sağında", "beside-left": "masanın solunda"}
        g = T[r]
        return mq("%s nerede?%s" % (cap(b(kind)), pic(P.table_scene_svg(kind, r), "masa ve %s" % b(kind))), cap(g), [cap(x) for x in T.values() if x != g],
                  "%s <b>%s</b>." % (cap(b(kind)), g))
    return named(f, "masa")


def m_kutu_konum():
    def f():
        kind = ch(KINDS)
        r = ch(["front", "behind", "beside", "above"])
        T = {"front": "kutunun önünde", "behind": "kutunun arkasında", "beside": "kutunun yanında", "above": "kutunun üstünde"}
        g = T[r]
        return mq("%s nerede?%s" % (cap(b(kind)), pic(P.box_scene_svg(kind, r), "kutu ve %s" % b(kind))), cap(g), [cap(x) for x in T.values() if x != g],
                  "%s <b>%s</b>." % (cap(b(kind)), g))
    return named(f, "kutu_konum")


def m_raf():
    def f():
        ks = sh(KINDS)[:4]
        i = ri(0, 3)
        k = ri(0, 2)
        p = pic(P.shelf_svg(ks), "raflarda " + ", ".join(b(x) for x in ks))
        if k == 0:
            pos = ["en üst", "üstten ikinci", "üstten üçüncü", "en alt"][i]
            return mq("%s rafta ne var?%s" % (cap(pos), p), cap(b(ks[i])), [cap(b(x)) for x in ks if x != ks[i]], "%s rafta <b>%s</b> var." % (cap(pos), b(ks[i])))
        if i == 0:
            return None
        if k == 1:
            return mq("%s rafının hemen üstündeki rafta ne var?%s" % (cap(b(ks[i])), p), cap(b(ks[i - 1])), [cap(b(x)) for x in ks if x != ks[i - 1]],
                      "Hemen üstte <b>%s</b> var." % b(ks[i - 1]))
        return mq("%s rafının hemen altındaki rafta ne var?%s" % (cap(b(ks[i - 1])), p), cap(b(ks[i])), [cap(b(x)) for x in ks if x != ks[i]],
                  "Hemen altta <b>%s</b> var." % b(ks[i]))
    return named(f, "raf")


def m_sag_sol():
    def f():
        ks = sh(KINDS)[:5]
        i = ri(0, 4)
        p = pic(P.kinds_row_svg(ks), "sıra: " + ", ".join(b(x) for x in ks))
        if ri(0, 1) == 0 and i < 4:
            return mq("%s nesnesinin hemen sağında ne var?%s" % (cap(b(ks[i])), p), cap(b(ks[i + 1])), [cap(b(x)) for x in ks if x != ks[i + 1]],
                      "Hemen sağda <b>%s</b> var." % b(ks[i + 1]))
        if i > 0:
            return mq("%s nesnesinin hemen solunda ne var?%s" % (cap(b(ks[i])), p), cap(b(ks[i - 1])), [cap(b(x)) for x in ks if x != ks[i - 1]],
                      "Hemen solda <b>%s</b> var." % b(ks[i - 1]))
        return None
    return named(f, "sag_sol")


def izgara(start, targets, n=6, cell=40):
    """start: (c, r) yıldız; targets: [(c, r, harf)]. r=0 alt sıra."""
    W = H = n * cell + 20
    s = []
    for i in range(n + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c9d3df' stroke-width='1.5'/>" % (10 + i * cell, 10, 10 + i * cell, 10 + n * cell))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c9d3df' stroke-width='1.5'/>" % (10, 10 + i * cell, 10 + n * cell, 10 + i * cell))
    X = lambda c: 10 + c * cell + cell / 2.0
    Y = lambda r: 10 + (n - 1 - r) * cell + cell / 2.0
    s.append(P.obj("star", X(start[0]), Y(start[1]), 14))
    for c, r, L in targets:
        s.append("<circle cx='%.1f' cy='%.1f' r='14' fill='#fff' stroke='%s' stroke-width='2'/>" % (X(c), Y(r), BLUE) + text(X(c), Y(r) + 6, L, 16))
    return pic(svg_wrap(W, H, "".join(s), "kareli zemin, yıldız ve harfler"), "kareli zemin, yıldız ve harfler")


def m_yonerge(n=6):
    def f():
        sc, sr = ri(0, n - 1), ri(0, n - 1)
        dx, dy = ri(-3, 3), ri(-3, 3)
        if dx == 0 and dy == 0:
            return None
        tc, tr = sc + dx, sr + dy
        if not (0 <= tc < n and 0 <= tr < n):
            return None
        cands = {(tc, tr)}
        for ddx, ddy in [(-dx, dy), (dx, -dy), (dy, dx), (dx + 1, dy), (dx, dy - 1), (-dx, -dy)]:
            p = (sc + ddx, sr + ddy)
            if 0 <= p[0] < n and 0 <= p[1] < n and p != (sc, sr):
                cands.add(p)
            if len(cands) == 4:
                break
        if len(cands) < 4:
            return None
        cl = sh(sorted(cands))
        Ls = "ABCD"
        tg = [(c, r, Ls[i]) for i, (c, r) in enumerate(cl)]
        g = Ls[cl.index((tc, tr))]
        parts = []
        if dx:
            parts.append("%d kare %s" % (abs(dx), "sağa" if dx > 0 else "sola"))
        if dy:
            parts.append("%d kare %s" % (abs(dy), "yukarı" if dy > 0 else "aşağı"))
        return mq("Yıldızdan başla: %s git. Hangi harfe ulaşırsın?%s" % (", sonra ".join(parts), izgara((sc, sr), tg, n)), g, [x for x in Ls if x != g],
                  "Önce %s. Ulaşılan harf <b>%s</b>." % (", sonra ".join(parts), g))
    return named(f, "yonerge")


def m_yon_bul(n=6):
    def f():
        sc, sr = ri(0, n - 1), ri(0, n - 1)
        dx, dy = ri(-3, 3), ri(-3, 3)
        if dx == 0 or dy == 0:
            return None
        tc, tr = sc + dx, sr + dy
        if not (0 <= tc < n and 0 <= tr < n):
            return None
        g = "%d kare %s, %d kare %s" % (abs(dx), "sağa" if dx > 0 else "sola", abs(dy), "yukarı" if dy > 0 else "aşağı")
        ws = ["%d kare %s, %d kare %s" % (abs(dx), "sola" if dx > 0 else "sağa", abs(dy), "yukarı" if dy > 0 else "aşağı"),
              "%d kare %s, %d kare %s" % (abs(dx), "sağa" if dx > 0 else "sola", abs(dy), "aşağı" if dy > 0 else "yukarı"),
              "%d kare %s, %d kare %s" % (abs(dy), "sağa" if dx > 0 else "sola", abs(dx), "yukarı" if dy > 0 else "aşağı")]
        return mq("Yıldızdan A harfine nasıl gidilir?%s" % izgara((sc, sr), [(tc, tr, "A")], n), g, ws, "Yatayda %d, dikeyde %d kare: <b>%s</b>." % (abs(dx), abs(dy), g))
    return named(f, "yon_bul")


def es_svg(ref, items, size=26):
    """ref: (kind, color, scale)；items: [(kind, color, scale, rot)] → A〜D（同じ縮尺）"""
    s = [P.shape(ref[0], 200, 46, size * ref[2], ref[1]), text(200, 100, "Verilen şekil", 13)]
    s.append("<line x1='10' y1='112' x2='390' y2='112' stroke='#c9d3df' stroke-width='1.5'/>")
    for i, (k, col, sc, rot) in enumerate(items):
        cx = 50 + i * 100
        s.append(P.shape_rot(k, cx, 166, size * sc, col, rot) if rot else P.shape(k, cx, 166, size * sc, col))
        s.append(text(cx, 228, "ABCD"[i], 16))
    return svg_wrap(400, 240, "".join(s), "verilen şekil ve A, B, C, D şekilleri")


def m_es():
    def f():
        k = ch(["triangle", "square", "rectangle", "hexagon"])
        col = ch(list(RENK))
        sc = ch([0.9, 1.0, 1.1])
        others = [x for x in ("triangle", "square", "rectangle", "hexagon", "circle") if x != k]
        o1, o2 = sh(others)[:2]
        good = (k, ch(list(RENK)), sc, ch([0, 30, 90, 180]))
        bad = [(k, ch(list(RENK)), sc * ch([0.55, 1.5]), 0), (o1, col, sc, 0), (o2, col, sc, 0)]
        items = sh([good] + bad)
        g = "ABCD"[items.index(good)]
        return mq("Verilen şekille eş olan (aynı biçim ve büyüklükte) şekil hangisidir? Rengi ve duruşu önemli değildir.%s" % pic(es_svg((k, col, sc), items), "verilen şekil ve A, B, C, D"),
                  g, [x for x in "ABCD" if x != g], "Eş şekillerin biçimi ve büyüklüğü aynıdır; döndürülmüş ya da farklı renkte olabilir. Cevap: <b>%s</b>." % g)
    return named(f, "es")


# ============================================================ ölçme
def m_uzun():
    def f():
        ls = sh(range(3, 10))[:ri(3, 4)]
        lng = rnd() < 0.5
        c = max(ls) if lng else min(ls)
        i = ls.index(c)
        return mq("Hangi kalem en %s?%s" % ("uzun" if lng else "kısa", pic(P.pencils_svg(ls), "A'dan %s'ye kalemler" % "ABCD"[len(ls) - 1])),
                  "%s kalemi" % "ABCD"[i], ["%s kalemi" % "ABCD"[j] for j in range(len(ls)) if j != i] + ["Hepsi eşit"],
                  "Kalemlerin sol uçları aynı hizada. <b>%s kalemi</b> en %s." % ("ABCD"[i], "uzun" if lng else "kısa"))
    return named(f, "uzun")


def m_kule():
    def f():
        hs = sh(range(2, 10))[:ri(3, 4)]
        k = ri(0, 2)
        p = kule(hs)
        if k == 2:
            i = ri(0, len(hs) - 1)
            return mq("%s kulesi kaç küp yüksekliğindedir?%s" % ("ABCD"[i], p), "%d küp" % hs[i], ["%d küp" % x for x in (hs[i] + 1, hs[i] - 1, hs[i] + 2)],
                      "Küpleri sayarız: <b>%d küp</b>." % hs[i])
        tall = k == 0
        c = max(hs) if tall else min(hs)
        i = hs.index(c)
        return mq("Hangi kule en %s?%s" % ("yüksek" if tall else "alçak", p), "%s kulesi" % "ABCD"[i], ["%s kulesi" % "ABCD"[j] for j in range(len(hs)) if j != i] + ["Hepsi eşit"],
                  "%s kulesinde %d küp var: <b>en %s</b>." % ("ABCD"[i], c, "yüksek" if tall else "alçak"))
    return named(f, "kule")


AGIR = ["apple", "ball", "cup", "fish", "duck", "flower"]


def m_agir():
    def f():
        k1, k2 = sh(AGIR)[:2]
        tilt = ch(["left", "right"])
        heavy = k1 if tilt == "left" else k2
        light = k2 if tilt == "left" else k1
        q = ch(["ağır", "hafif"])
        g = heavy if q == "ağır" else light
        return mq("Teraziye bakınız. Hangisi daha %s?%s" % (q, terazi((k1, 1), (k2, 1), tilt)), cap(b(g)),
                  [cap(b(light if g == heavy else heavy)), "İkisi eşit", "Bilinemez"],
                  "Ağır olan kefe aşağı iner. Daha %s olan <b>%s</b>." % (q, b(g)))
    return named(f, "agir")


def m_denge():
    def f():
        k = ch(AGIR)
        n = ri(2, 6)
        return mq("Terazi dengede. Bir %s kaç küp ağırlığındadır?%s" % (b(k), terazi((k, 1), ("cube", n), "equal")), "%d küp" % n,
                  ["%d küp" % x for x in (n + 1, n - 1, 1, n + 2) if x != n and x > 0], "Terazi dengede, yani 1 %s = <b>%d küp</b>." % (b(k), n))
    return named(f, "denge")


OLCU_TB = [("sıranın boyu", "karış"), ("sınıfın uzunluğu", "adım"), ("kalemin boyu", "ataş"), ("kitabın eni", "parmak")]


def m_standart_olmayan():
    def f():
        x, y = G.K.two()
        what, un = ch(OLCU_TB)
        a, c = ri(5, 15), ri(5, 15)
        if a == c:
            return None
        if rnd() < 0.5:
            return mq("%s %s ölçtü ve %d %s buldu. %s aynı şeyi ölçtü ve %d %s buldu. Sonuçlar neden farklı?" % (x, what.replace("boyu", "boyunu").replace("uzunluğu", "uzunluğunu").replace("eni", "enini"), a, un, y, c, un),
                      "%s uzunlukları farklıdır" % cap(un) if un != "ataş" else "Kullandıkları ataşlar farklıdır",
                      ["Ölçülen şey değişti", "Biri ters saydı", "Standart olmayan birimler hep aynıdır"],
                      "Herkesin %s uzunluğu farklıdır; bu yüzden sonuçlar farklı çıkabilir." % un)
        return None
    return named(f, "standart_olmayan")


def m_kac_birim():
    def f():
        n = ri(3, 9)
        un = ch(["ataş", "küp", "silgi"])
        L = "%s kaç %s uzunluğundadır?" % (ch(["Kalem", "Kurdele", "Fırça", "Şerit"]), un)
        s = []
        u = 36
        for i in range(n):
            s.append("<rect x='%d' y='52' width='%d' height='16' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>" % (10 + i * u, u - 2, "#f2c94c" if un == "küp" else "#cfd8dc" if un == "ataş" else "#f4a3b4", INK))
        s.append("<rect x='10' y='20' width='%d' height='18' rx='6' fill='#7fb3d5' stroke='%s' stroke-width='1.5'/>" % (n * u - 2, INK))
        p = pic(svg_wrap(n * u + 20, 80, "".join(s), "nesne ve altında birimler"), "nesne ve altında %d birim" % n)
        return mq(L + p, "%d %s" % (n, un), ["%d %s" % (x, un) for x in (n + 1, n - 1, n + 2)], "Birimleri sayarız: <b>%d %s</b>." % (n, un))
    return named(f, "kac_birim")


def m_kap():
    def f():
        k = ri(0, 1)
        if k == 0:
            hs = sh([50, 70, 90, 110])[:4]
            items = [(40, h, 1.0) for h in hs]
            big = rnd() < 0.5
            c = max(hs) if big else min(hs)
            g = "ABCD"[hs.index(c)]
            return mq("Kaplar aynı genişlikte ve tamamen dolu. Hangisinde en %s su var?%s" % ("çok" if big else "az", pic(glasses_svg(items), "A, B, C, D kapları")),
                      g, [x for x in "ABCD" if x != g], "Aynı genişlikteki kaplarda su yüksekliği büyük olanda daha çok su vardır. Cevap: <b>%s</b>." % g)
        n = ri(2, 8)
        kap = ch(["sürahi", "kova", "tencere", "şişe"])
        bar = ch(["bardak", "fincan", "kepçe"])
        x = nm()
        return mq("%s, bir %s suyu %d %s ile doldurdu. %s kaç %s su alır?" % (x, kap, n, bar, cap(kap), bar), "%d %s" % (n, bar),
                  ["%d %s" % (v, bar) for v in (n + 1, n - 1, n + 2, 2 * n) if v != n and v > 0], "%d %s ile dolduğu için <b>%d %s</b>." % (n, bar, n, bar))
    return named(f, "kap")


# ============================================================ veri
KAT = [("en sevilen meyve", ["Elma", "Portakal", "Muz", "Çilek"]), ("en sevilen renk", ["Kırmızı", "Mavi", "Sarı", "Yeşil"]),
       ("evcil hayvan", ["Kedi", "Balık", "Kuş", "Tavşan"]), ("sınıftaki oyuncak", ["Top", "Bebek", "Araba", "Blok"])]


def nesne_grafigi(cats, vals, kind="dot"):
    rows = "".join("<tr><td>%s</td><td style='text-align:left'>%s</td></tr>" % (c, re.sub(r"aria-label='[^']*'", "aria-label='%d simge'" % v, P.row_svg(v, kind, 10)).replace("<svg ", "<svg style='height:30px;width:auto' ", 1) if v else "")
                   for c, v in zip(cats, vals))
    return "<table class='sn-table' style='width:auto'><tbody>%s</tbody></table>" % rows


def cetele_tablosu(cats, vals):
    rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (c, cetele(v).replace("<svg ", "<svg style='height:26px;width:auto' ", 1)) for c, v in zip(cats, vals))
    return "<table class='sn-table' style='width:auto'><thead><tr><th>Seçenek</th><th>Çetele</th></tr></thead><tbody>%s</tbody></table>" % rows


def m_cetele(mx):
    def f():
        n = ri(2, mx)
        k = ri(0, 2)
        if k == 1 and n >= 5:
            return mq("Bu çetelede kaç tane beşli grup var?%s" % cetele(n), num(n // 5), [num(x) for x in (n // 5 + 1, n, n % 5, n // 5 + 2) if x != n // 5],
                      "Her grup 5 çizgidir. <b>%d</b> grup var." % (n // 5))
        if k == 2 and n < mx:
            return mq("Bu çeteleye 1 çizgi daha eklenirse hangi sayı gösterilir?%s" % cetele(n), num(n + 1), near(n + 1, 1, 30, (1, -1, 5)),
                      "%d + 1 = <b>%d</b>." % (n, n + 1))
        return mq("Bu çetele hangi sayıyı gösterir?%s" % cetele(n), num(n), near(n, 1, 30, (1, -1, 5, -5)),
                  "Her grup 5. %d grup ve %d çizgi: <b>%d</b>." % (n // 5, n % 5, n))
    return named(f, "cetele")


def m_veri(mx, how="nesne", kq="all", ncat=(3, 4)):
    def f():
        t, cats = ch(KAT)
        k = ch(ncat)
        cats = cats[:k]
        vals = [ri(1, mx) for _ in cats]
        if len(set(vals)) < k:
            return None
        if how == "nesne":
            disp = nesne_grafigi(cats, vals)
            intro = "Nesne grafiği: %s (her simge 1 öğrenci)." % t
        elif how == "cetele":
            disp = cetele_tablosu(cats, vals)
            intro = "Çetele tablosu: %s." % t
        else:
            disp = sutun_grafigi(list(zip(cats, vals)), "öğrenci sayısı")
            intro = "Sütun grafiği: %s." % t
        q = ri(0, 3) if kq == "all" else ch(kq)
        if q == 0:
            i = ri(0, k - 1)
            return mq("%s%s%s seçeneğini kaç öğrenci seçti?" % (intro, disp, cats[i]), num(vals[i]), near(vals[i], 0, 40, (1, -1, 2)) + [num(sum(vals))],
                      "%s: <b>%d</b>." % (cats[i], vals[i]))
        if q == 1:
            big = rnd() < 0.5
            c = max(vals) if big else min(vals)
            i = vals.index(c)
            return mq("%s%sEn %s seçilen hangisidir?" % (intro, disp, "çok" if big else "az"), cats[i], [x for x in cats if x != cats[i]] + ["Hepsi eşit"],
                      "%s: %d. Cevap: <b>%s</b>." % (cats[i], c, cats[i]))
        i, j = sh(range(k))[:2]
        if q == 2:
            if vals[i] == vals[j]:
                return None
            if vals[i] < vals[j]:
                i, j = j, i
            a, c = vals[i], vals[j]
            return mq("%s%s%s seçen öğrenci sayısı, %s seçenlerden kaç fazladır?" % (intro, disp, cats[i], cats[j]), num(a - c), near(a - c, 0, 40, (1, -1)) + [num(a + c)],
                      "%d − %d = <b>%d</b>." % (a, c, a - c))
        s = vals[i] + vals[j]
        return mq("%s%s%s ya da %s seçen toplam kaç öğrenci var?" % (intro, disp, cats[i], cats[j]), num(s), near(s, 0, 80, (1, -1, 2)) + [num(abs(vals[i] - vals[j]))],
                  "%d + %d = <b>%d</b>." % (vals[i], vals[j], s))
    return named(f, "veri_" + how)


def m_karar(mx):
    def f():
        t, cats = ch(KAT)
        cats = cats[:4]
        vals = [ri(1, mx) for _ in cats]
        if len(set(vals)) < 4:
            return None
        i = vals.index(max(vals))
        Q = {"en sevilen meyve": "Sınıf gezisine hangi meyveyi götürmek en uygun olur?", "en sevilen renk": "Sınıf panosu hangi renkte olursa en çok öğrenci sevinir?",
             "evcil hayvan": "Hangi hayvanı besleyen öğrenci sayısı en fazladır?", "sınıftaki oyuncak": "Teneffüste en çok hangi oyuncağa ihtiyaç olur?"}
        return mq("Nesne grafiği: %s (her simge 1 öğrenci).%s%s" % (t, nesne_grafigi(cats, vals), Q[t]), cats[i], [x for x in cats if x != cats[i]],
                  "En çok seçilen <b>%s</b> (%d öğrenci); veriye dayalı karar budur." % (cats[i], vals[i]))
    return named(f, "karar")


# ============================================================ 2. sınıf
def m_onluk_birlik(kinds=(0, 1, 2, 3, 4)):
    def f():
        n = ri(11, 99)
        t, o = divmod(n, 10)
        if o == 0 or t == o:
            return None
        k = ch(kinds)
        if k == 0:
            return mq("%d sayısında %d rakamının basamak değeri kaçtır?" % (n, t), num(t * 10), [num(t), num(o), num(o * 10), num(n)],
                      "%d onlar basamağında: <b>%d</b>." % (t, t * 10))
        if k == 1:
            return mq("%d sayısının çözümlenmesi hangisidir?" % n, "%d + %d" % (t * 10, o), ["%d + %d" % (t, o), "%d + %d" % (o * 10, t), "%d + %d" % (t * 10, o * 10)],
                      "%d onluk %d birlik: <b>%d + %d</b>." % (t, o, t * 10, o))
        if k == 2:
            return mq("%d onluk %d birlik hangi sayıdır?" % (t, o), num(n), [num(o * 10 + t), num(t + o), num(n + 10) if n < 90 else num(n - 10)], "%d + %d = <b>%d</b>." % (t * 10, o, n))
        if k == 3:
            return mq("Bloklar hangi sayıyı gösteriyor?%s" % onluk(t, o), num(n), [num(o * 10 + t), num(n + 1), num(t + o), num(n - 10)],
                      "%d onluk ve %d birlik: <b>%d</b>." % (t, o, n))
        return mq("Basamak tablosundaki sayı hangisidir?" + basamak_tablosu(n, 2), num(n), [num(o * 10 + t), num(t + o), num(n + 10) if n < 90 else num(n - 10)],
                  "Onlar %d, birler %d: <b>%d</b>." % (t, o, n))
    return named(f, "onluk_birlik")


def m_tek_cift():
    def f():
        n = ri(2, 99)
        k = ri(0, 2)
        if k == 0:
            g = "Çift" if n % 2 == 0 else "Tek"
            return mq("%d sayısı tek mi, çift mi?" % n, g, ["Tek" if g == "Çift" else "Çift", "İkisi de", "Hiçbiri"],
                      "Birler basamağı %d: <b>%s</b>." % (n % 10, g.lower()))
        xs = sh(list(range(n, n + 8)))[:4]
        ev = [x for x in xs if x % 2 == (0 if k == 1 else 1)]
        if len(ev) != 1:
            return None
        return mq("Hangisi %s sayıdır?" % ("çift" if k == 1 else "tek"), num(ev[0]), [num(x) for x in xs if x != ev[0]],
                  "%s sayıların birler basamağı %s olur. Cevap: <b>%d</b>." % ("Çift" if k == 1 else "Tek", "0, 2, 4, 6 ya da 8" if k == 1 else "1, 3, 5, 7 ya da 9", ev[0]))
    return named(f, "tek_cift")


def m_carpma_resim(mx_f=5):
    def f():
        g, k = ri(2, mx_f), ri(1, 10)
        if g * k > 50:
            return None
        kind = ch(KINDS)
        if rnd() < 0.5 and k <= 5:
            p = gruplar(g, k, kind)
            q = "%d grupta %d’şer %s var. Hepsi kaç tane eder?" if False else "Her grupta %d %s olan %d grup var. Toplam kaç %s var?" % (k, b(kind), g, b(kind))
        else:
            if k > 10:
                return None
            p = dizi(g, k, kind)
            q = "Her sırada %d %s olan %d sıra var. Toplam kaç %s var?" % (k, b(kind), g, b(kind))
        v = g * k
        return mq(q + p, num(v), [num(g + k), num(v + k), num(v - g) if v - g != g + k else num(v + 1)],
                  "%s = %d × %d = <b>%d</b>." % (" + ".join([str(k)] * g), g, k, v))
    return named(f, "carpma_resim")


def m_tekrarli(mx_f=5):
    def f():
        g, k = ri(2, mx_f), ri(1, 10)
        v = g * k
        if rnd() < 0.5:
            return mq("%s toplama işlemi hangi çarpma işlemiyle gösterilir?" % " + ".join([str(k)] * g), "%d × %d" % (g, k),
                      ["%d × %d" % (k, k), "%d + %d" % (g, k), "%d × %d" % (g, g)] if k != g else ["%d × %d" % (g, g + 1), "%d + %d" % (g, k), "%d × %d" % (g + 1, k)],
                      "%d tane %d toplanıyor: <b>%d × %d</b>." % (g, k, g, k))
        return mq("%d × %d işlemi hangi toplama işlemine eşittir?" % (g, k), " + ".join([str(k)] * g),
                  [" + ".join([str(g)] * (k if k <= 6 else 2)) if k != g else " + ".join([str(k)] * (g + 1)), "%d + %d" % (g, k), " + ".join([str(k)] * (g + 1))],
                  "%d × %d: %d tane %d: <b>%s</b>." % (g, k, g, k, " + ".join([str(k)] * g)))
    return named(f, "tekrarli")


def m_carpim(fs=(1, 2, 3, 4, 5)):
    def f():
        a, c = ch(fs), ri(1, 10)
        if rnd() < 0.5:
            a, c = c, a
        v = a * c
        return mq("%d × %d = ?" % (a, c), num(v), [num(a + c), num(v + min(a, c)), num(v - min(a, c)) if v - min(a, c) > 0 else num(v + 1), num(v + 1)],
                  "%d × %d = <b>%d</b>." % (a, c, v))
    return named(f, "carpim")


def m_carpma_problem(mx_f=5):
    def f():
        g, k = ri(2, mx_f), ri(2, 10)
        x = nm()
        T = [("%s her gün %d sayfa kitap okuyor. %d günde kaç sayfa okur?", "sayfa", (x, k, g)),
             ("Bir tabakta %d kurabiye var. %d tabakta kaç kurabiye olur?", "kurabiye", (k, g)),
             ("Bir kutuda %d boya kalemi var. %s %d kutu aldı. Kaç boya kalemi oldu?", "kalem", (k, x, g)),
             ("Bir arabanın 4 tekerleği var. %d arabada kaç tekerlek olur?", "tekerlek", (k,)),
             ("Bir sırada %d öğrenci oturuyor. %d sırada kaç öğrenci oturur?", "öğrenci", (k, g))]
        t, un, args = ch(T)
        if un == "tekerlek":
            g, k = 4, ri(2, 10)
            args = (k,)
        else:
            g = args[-1]
        v = g * k
        return mq(t % args, "%d %s" % (v, un), ["%d %s" % (w, un) for w in (g + k, v + k, v - g if v - g != g + k else v + 1)],
                  "%d × %d = <b>%d</b>." % (g, k, v))
    return named(f, "carpma_problem")


def m_bolme_resim():
    def f():
        d = ri(2, 5)
        q = ri(1, 20 // d)
        n = d * q
        kind = ch(KINDS)
        if q > 5:
            return None
        k = ri(0, 1)
        p = gruplar(d, q, kind)
        if k == 0:
            return mq("%d %s, %d çocuğa eşit paylaştırılıyor. Her çocuk kaç %s alır?%s" % (n, b(kind), d, b(kind), p), num(q),
                      [num(q + 1), num(n - d), num(d) if d != q else num(q + 2)], "%d ÷ %d = <b>%d</b>." % (n, d, q))
        return mq("%d %s, %d’erli değil, her grupta %d olacak şekilde gruplanıyor. Kaç grup olur?%s" % (n, b(kind), 0, q, p) if False else
                  "%d %s, her grupta %d tane olacak şekilde gruplanıyor. Kaç grup olur?%s" % (n, b(kind), q, p), num(d),
                  [num(d + 1), num(n - q), num(q) if q != d else num(d + 2)], "%d ÷ %d = <b>%d</b>." % (n, q, d))
    return named(f, "bolme_resim")


def m_tekrarli_cikarma():
    def f():
        d = ri(2, 5)
        q = ri(2, 20 // d)
        n = d * q
        steps = [n - d * i for i in range(q + 1)]
        return mq("%d sayısından art arda %d çıkararak sıfıra ulaşıyoruz: %s. Kaç kez çıkardık?" % (n, d, " → ".join(map(str, steps))), num(q),
                  [num(q + 1), num(d) if d != q else num(q - 1), num(n)], "%d kez çıkardık: %d ÷ %d = <b>%d</b>." % (q, n, d, q))
    return named(f, "tekrarli_cikarma")


def m_bolum():
    def f():
        d = ri(2, 5)
        q = ri(1, 20 // d)
        n = d * q
        return mq("%d ÷ %d = ?" % (n, d), num(q), [num(q + 1), num(n - d), num(q - 1) if q > 1 else num(q + 2), num(d * 2)],
                  "%d × %d = %d, bu yüzden %d ÷ %d = <b>%d</b>." % (d, q, n, n, d, q))
    return named(f, "bolum")


def m_bolme_iliski():
    def f():
        d = ri(2, 5)
        q = ri(1, 20 // d)
        n = d * q
        if rnd() < 0.5:
            return mq("%d × %d = %d ise %d ÷ %d kaçtır?" % (d, q, n, n, d), num(q), [num(n), num(d) if d != q else num(q + 1), num(q + 2)],
                      "Bölme çarpmanın tersidir: <b>%d</b>." % q)
        return mq("%d ÷ %d = %d işlemini hangi çarpma işlemi doğrular?" % (n, d, q), "%d × %d = %d" % (d, q, n),
                  ["%d × %d = %d" % (n, d, q), "%d + %d = %d" % (d, q, n), "%d × %d = %d" % (q, q, n)] if q != d else ["%d × %d = %d" % (n, d, q), "%d + %d = %d" % (d, q, n), "%d × %d = %d" % (n, q, d)],
                  "Bölüm ile bölen çarpılınca bölünen bulunur: <b>%d × %d = %d</b>." % (d, q, n))
    return named(f, "bolme_iliski")


def m_bolme_problem():
    def f():
        d = ri(2, 5)
        q = ri(2, 20 // d)
        n = d * q
        x = nm()
        T = [("%s, %d cevizi %d arkadaşına eşit paylaştırdı. Her arkadaşı kaç ceviz aldı?", "ceviz", (x, n, d), q),
             ("%d öğrenci %d kişilik gruplara ayrıldı. Kaç grup oldu?", "grup", (n, d), q),
             ("%d kalem %d kutuya eşit konuldu. Her kutuda kaç kalem var?", "kalem", (n, d), q),
             ("%d yumurta, %d’li kolilere değil; her tabakta %d yumurta olacak şekilde konuldu. Kaç tabak gerekir?", "tabak", (n, 0, d), q)]
        t, un, args, v = ch(T[:3])
        return mq(t % args, "%d %s" % (v, un), ["%d %s" % (w, un) for w in (v + 1, n - d, d if d != v else v + 2)], "%d ÷ %d = <b>%d</b>." % (n, d, v))
    return named(f, "bolme_problem")


def m_esit_dort(mx=50):
    def f():
        k = ri(0, 3)
        if k == 0:
            a, c = ri(2, 5), ri(2, 10)
            d = ch([x for x in (1, 2, 5, 10) if (a * c) % x == 0 and x not in (a, c)] or [1])
            return mq("%d × %d = %d × …<br>Noktalı yere hangi sayı gelir?" % (a, c, d), num(a * c // d), [num(a * c), num(a + c - d), num(a * c // d + 1)],
                      "%d × %d = %d. %d × %d = %d. Cevap: <b>%d</b>." % (a, c, a * c, d, a * c // d, a * c, a * c // d))
        if k == 1:
            a, c = ri(2, 5), ri(2, 9)
            return mq("%d × %d = … + … + … (kaç tane %d toplanır?)" % (a, c, c) if False else "%d × %d işleminin sonucu hangisine eşittir?" % (a, c),
                      "%d + %d" % (a * c - c, c), ["%d + %d" % (a + c, c), "%d + %d" % (a * c, c), "%d − %d" % (a * c, c)],
                      "%d × %d = %d ve %d + %d = %d: <b>%d + %d</b>." % (a, c, a * c, a * c - c, c, a * c, a * c - c, c))
        if k == 2:
            a, c = ri(10, 60), ri(10, 39)
            if a + c > mx + 40:
                return None
            d = ri(1, 9)
            return mq("%d + %d = %d + …<br>Noktalı yere hangi sayı gelir?" % (a, c, a + d), num(c - d), [num(c + d), num(a + c), num(c - d + 1)],
                      "%d sayısını %d artırdık, öbür sayıyı %d azaltırız: <b>%d</b>." % (a, d, d, c - d))
        d = ri(2, 5)
        q = ri(2, 20 // d)
        return mq("%d ÷ %d = … − %d<br>Noktalı yere hangi sayı gelir?" % (d * q, d, ri(1, 3)) if False else "%d ÷ %d = %d − …<br>Noktalı yere hangi sayı gelir?" % (d * q, d, q + 3),
                  num(3), [num(q), num(q + 3), num(2)], "%d ÷ %d = %d. %d − 3 = %d. Cevap: <b>3</b>." % (d * q, d, q, q + 3, q))
    return named(f, "esit_dort")


def m_yarim(kinds=(0, 1, 2)):
    def f():
        k = ch(kinds)
        if k == 0:
            n, s = ch([(2, 1), (4, 1), (4, 2), (1, 1), (4, 3)])
            col = ch(["#f4a261", "#7fb3d5", "#a8d5ba", "#f2c94c"])
            p = A.pie(n, s, ch([50, 60, 70]), col) if rnd() < 0.5 else A.bar_frac(n, s, ch([240, 300, 360]), 40, col)
            name_ = {(2, 1): "yarım", (4, 1): "çeyrek", (4, 2): "yarım", (1, 1): "bütün", (4, 3): "üç çeyrek"}[(n, s)]
            ex = "Bütün %d eş parçaya bölünmüş, %d parça boyalı: <b>%s</b>." % (n, s, name_) if n > 1 else "Hepsi boyalı: <b>bütün</b>."
            return mq("Boyalı kısım bütünün ne kadarıdır?%s" % (p if p.startswith("<div") else fig(p)), cap(name_),
                      [cap(o) for o in ("yarım", "çeyrek", "bütün", "üç çeyrek") if o != name_], ex)
        if k == 1:
            kk = ch([2, 4])
            g_ = ri(1, 5)
            n = kk * g_
            kind = ch(KINDS)
            w = "yarısını" if kk == 2 else "çeyreğini"
            x = nm()
            return mq("%s, %d %s aldı. Bunların %s kardeşine verdi. Kardeşine kaç %s verdi?%s" % (x, n, b(kind), w, b(kind), gruplar(kk, g_, kind)),
                      num(g_), near(g_, 1, 20, (1, -1)) + [num(n - g_), num(n)], "%d tane %d eş gruba ayrılır: her grupta <b>%d</b>." % (n, kk, g_))
        BANK = [("Bir ekmek 2 eş parçaya bölündü. Bir parçaya ne denir?", "Yarım", ["Çeyrek", "Bütün", "Üç çeyrek"]),
                ("Bir pizza 4 eş parçaya bölündü. Bir dilime ne denir?", "Çeyrek", ["Yarım", "Bütün", "Üç çeyrek"]),
                ("2 çeyrek kaç yarım eder?", "1 yarım", ["2 yarım", "1 bütün", "4 yarım"]),
                ("4 çeyrek ne eder?", "1 bütün", ["1 yarım", "2 bütün", "1 çeyrek"]),
                ("2 yarım ne eder?", "1 bütün", ["1 çeyrek", "2 bütün", "4 çeyrek"]),
                ("Aynı pastanın yarımı mı büyüktür, çeyreği mi?", "Yarımı", ["Çeyreği", "Eşittir", "Karşılaştırılamaz"]),
                ("Bir kâğıt ortadan iki eş parçaya katlandı. Her parça ne kadardır?", "Yarım", ["Çeyrek", "Bütün", "Üç çeyrek"]),
                ("Bir kâğıt iki kez katlanıp 4 eş parçaya ayrıldı. Her parça ne kadardır?", "Çeyrek", ["Yarım", "Bütün", "Üç çeyrek"]),
                ("Bir bütün elmada kaç çeyrek vardır?", "4 çeyrek", ["2 çeyrek", "1 çeyrek", "3 çeyrek"]),
                ("Bir bütün portakalda kaç yarım vardır?", "2 yarım", ["4 yarım", "1 yarım", "3 yarım"]),
                ("Yarım saat kaç çeyrek saattir?", "2 çeyrek saat", ["4 çeyrek saat", "1 çeyrek saat", "3 çeyrek saat"]),
                ("Bir saat kaç çeyrek saattir?", "4 çeyrek saat", ["2 çeyrek saat", "3 çeyrek saat", "1 çeyrek saat"])]
        q, g, w = ch(BANK)
        return mq(q, g, w, "Cevap: <b>%s</b>." % g)
    return named(f, "yarim")


def m_para_tanı(notes=(1, 5, 10, 20, 50, 100, 200)):
    def f():
        v = ch(notes)
        items = [v * 100]
        p = pic(A.para_svg(items), "bir para")
        return mq("Resimdeki para kaç liradır?%s" % p, "%d TL" % v, ["%d TL" % x for x in notes if x != v][:6], "Bu para <b>%d TL</b>." % v)
    return named(f, "para_tani")


def m_para_say(notes=(1, 5, 10, 20, 50), mx=100, k_=(2, 4)):
    def f():
        items = [ch(notes) for _ in range(ri(*k_))]
        t = sum(items)
        if t > mx:
            return None
        p = pic(A.para_svg([x * 100 for x in items]), "paralar")
        return mq("Resimdeki paralar toplam kaç liradır?%s" % p, "%d TL" % t, ["%d TL" % x for x in (t + 5, t - items[0], t + 10, t + 1) if x > 0],
                  "%s = <b>%d TL</b>." % (" + ".join("%d" % x for x in sorted(items, reverse=True)), t))
    return named(f, "para_say")


def m_para_karsilastir(notes=(1, 5, 10, 20, 50, 100, 200)):
    def f():
        a, c = sh(notes)[:2]
        big = rnd() < 0.5
        g = "%d TL" % (max(a, c) if big else min(a, c))
        return mq("%d TL ile %d TL’den hangisi daha %s değerlidir?" % (a, c, "çok" if big else "az") if False else
                  "Hangisi daha %sdeğerlidir: %d TL mi, %d TL mi?" % ("" if big else "az ", a, c), g, ["%d TL" % (min(a, c) if big else max(a, c)), "İkisi eşit", "Bilinemez"],
                  "Cevap: <b>%s</b>." % g)
    return named(f, "para_karsilastir")


def m_para_eksik(mx=20):
    def f():
        x = nm()
        a = ri(1, mx - 2)
        p = ri(a + 1, mx)
        item = ch(["oyuncak", "kitap", "top", "boya kalemi", "yapboz", "defter"])
        return mq("%s cebinde %d TL var. Fiyatı %d TL olan bir %s almak istiyor. Kaç TL daha gerekir?" % (gen(x).replace("’in", "’in").rsplit("’", 1)[0] + "’in" if False else x + ":", a, p, item) if False else
                  "%s, fiyatı %d TL olan bir %s almak istiyor. Cebinde %d TL var. Kaç TL daha gerekir?" % (x, p, item, a), "%d TL" % (p - a),
                  ["%d TL" % v for v in (p + a, p - a + 1, p - a - 1 if p - a > 1 else p - a + 2, a)], "%d − %d = <b>%d TL</b>." % (p, a, p - a))
    return named(f, "para_eksik")


def m_para_bozdur(pairs=None):
    def f():
        P_ = pairs or [(10, 5), (20, 10), (20, 5), (50, 10), (50, 5), (100, 50), (100, 20), (100, 10), (200, 100), (200, 50), (10, 1), (5, 1), (50, 25)]
        a, c = ch([p for p in P_ if p[0] % p[1] == 0])
        n = a // c
        if rnd() < 0.5:
            k = ri(2, 9)
            if k * c > 200 or (c >= 20 and k > 4):
                return None
            return mq("%d tane %d TL kaç TL eder?" % (k, c), "%d TL" % (k * c), ["%d TL" % x for x in (k + c, k * c + c, k * c - c if k * c - c > 0 else k * c + 2 * c)],
                      "%s = <b>%d TL</b>." % (" + ".join([str(c)] * k), k * c))
        return mq("Bir %d TL kaç tane %d TL eder?" % (a, c), num(n), [num(n + 1), num(n * 2), num(n - 1) if n > 2 else num(n + 3)],
                  "%s = %d. Cevap: <b>%d</b>." % (" + ".join([str(c)] * n) if n <= 10 else "%d × %d" % (n, c), a, n))
    return named(f, "para_bozdur")


def m_para_alisveris(mx=100):
    def f():
        x = nm()
        item = ch(["kitap", "top", "boya seti", "oyuncak araba", "defter", "matara", "yapboz", "kumbara", "silgi", "kalem"])
        p = ri(2, mx - 5)
        pay = min([v for v in (5, 10, 20, 50, 100, 200) if v > p] or [None])
        if pay is None or pay > mx:
            return None
        return mq("%s, %d TL’lik bir %s aldı. %d TL verdi. Kaç TL para üstü alır?" % (x, p, item, pay) if False else
                  "%s bir %s aldı. Fiyatı %d TL. Kasaya %d TL verdi. Kaç TL para üstü alır?" % (x, item, p, pay), "%d TL" % (pay - p),
                  ["%d TL" % v for v in (pay - p + 1, p, pay - p + 10, pay + p) if v != pay - p and v >= 0], "%d − %d = <b>%d TL</b>." % (pay, p, pay - p))
    return named(f, "para_alisveris")


AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]


def m_takvim():
    def f():
        k = ri(0, 5)
        if k == 0:
            i = ri(0, 6)
            d = ch([1, 2, 3])
            g = GUNLER[(i + d) % 7]
            return mq("Bugün %s. %d gün sonra hangi gün olur?" % (GUNLER[i].lower(), d), g, [x for x in GUNLER if x != g][:6],
                      "%s → %s. Cevap: <b>%s</b>." % (GUNLER[i], " → ".join(GUNLER[(i + j) % 7] for j in range(1, d + 1)), g))
        if k == 1:
            i = ri(0, 6)
            g = GUNLER[(i - 1) % 7]
            return mq("Bugün %s. Dün hangi gündü?" % GUNLER[i].lower(), g, [x for x in GUNLER if x != g], "%s gününden önce <b>%s</b> gelir." % (GUNLER[i], g))
        if k == 2:
            i = ri(0, 11)
            g = AYLAR[(i + 1) % 12]
            return mq("%s ayından sonra hangi ay gelir?" % AYLAR[i], g, [x for x in AYLAR if x != g], "Aylar sırasıyla: %s → <b>%s</b>." % (AYLAR[i], g))
        if k == 3:
            S = [("Bir hafta kaç gündür?", "7 gün", ["5 gün", "10 gün", "12 gün"]), ("Bir yıl kaç aydır?", "12 ay", ["7 ay", "10 ay", "52 ay"]),
                 ("Bir gün kaç saattir?", "24 saat", ["12 saat", "60 saat", "7 saat"]), ("Bir saat kaç dakikadır?", "60 dakika", ["100 dakika", "30 dakika", "24 dakika"]),
                 ("Yarım saat kaç dakikadır?", "30 dakika", ["15 dakika", "50 dakika", "60 dakika"]), ("Çeyrek saat kaç dakikadır?", "15 dakika", ["25 dakika", "30 dakika", "4 dakika"]),
                 ("Bir dakika kaç saniyedir?", "60 saniye", ["100 saniye", "30 saniye", "10 saniye"]), ("Bir yılın ilk ayı hangisidir?", "Ocak", ["Aralık", "Eylül", "Mart"]),
                 ("Bir yılın son ayı hangisidir?", "Aralık", ["Ocak", "Kasım", "Haziran"]), ("Haftanın hafta sonu günleri hangileridir?", "Cumartesi ve Pazar", ["Cuma ve Cumartesi", "Pazartesi ve Salı", "Pazar ve Pazartesi"])]
            q, g, w = ch(S)
            return mq(q, g, w, "Cevap: <b>%s</b>." % g)
        if k == 4:
            w = ri(2, 4)
            return mq("%d hafta kaç gündür?" % w, "%d gün" % (7 * w), ["%d gün" % x for x in (7 * w + 1, 7 + w, 5 * w)], "%d × 7 = <b>%d gün</b>." % (w, 7 * w))
        i = ri(0, 11)
        d = ri(2, 4)
        g = AYLAR[(i + d) % 12]
        return mq("%s ayından %d ay sonra hangi ay gelir?" % (AYLAR[i], d), g, [x for x in AYLAR if x != g], "%s. Cevap: <b>%s</b>." % (" → ".join(AYLAR[(i + j) % 12] for j in range(d + 1)), g))
    return named(f, "takvim")


def m_saat(mins=(0, 30), digital=True):
    def f():
        h, m = ri(1, 12), ch(mins)
        k = ri(0, 2) if digital else ri(0, 1)
        p = pic(saat_svg(h, m, 150), "analog saat")
        if k == 0:
            g = cap(saat_oku(h, m)).rstrip(".")
            alts = [cap(saat_oku(h % 12 + 1, m)).rstrip("."), cap(saat_oku(h, (m + 30) % 60)).rstrip("."), cap(saat_oku((h + 10) % 12 + 1, m)).rstrip("."),
                    cap(saat_oku(m // 5 if m // 5 else 12, h * 5 % 60)).rstrip(".")]
            return mq("Saat kaçı gösteriyor?%s" % p, g, alts, "Akrep ve yelkovanın yerine bakarız: <b>%s</b>." % g.lower())
        if k == 1:
            hh = h if rnd() < 0.5 else h + 12
            g = "%02d.%02d" % (hh % 24 if hh != 24 else 12, m)
            g = "%02d.%02d" % (h, m)
            return mq("Saatin gösterdiği zaman (öğleden önce) dijital olarak nasıl yazılır?%s" % p, g,
                      ["%02d.%02d" % (h % 12 + 1, m), "%02d.%02d" % (h, (m + 30) % 60), "%02d.%02d" % (m // 5 if m // 5 else 12, h * 5 % 60)],
                      "Saat %d, dakika %d: <b>%s</b>." % (h, m, g))
        g = "%02d.%02d" % (h, m)
        return mq("“%s” dijital saatte nasıl görünür?" % cap(saat_oku(h, m)).rstrip("."), g,
                  ["%02d.%02d" % (h % 12 + 1, m), "%02d.%02d" % (h, (m + 30) % 60), "%02d.%02d" % ((h - 2) % 12 + 1, m)], "<b>%s</b>." % g)
    return named(f, "saat")


def m_uzunluk_tahmin():
    def f():
        S = [("Bir kurşun kalemin boyu", "Yaklaşık 15 cm", ["Yaklaşık 15 m", "Yaklaşık 1 cm", "Yaklaşık 150 m"]),
             ("Sınıf kapısının yüksekliği", "Yaklaşık 2 m", ["Yaklaşık 2 cm", "Yaklaşık 20 m", "Yaklaşık 200 m"]),
             ("Bir silginin boyu", "Yaklaşık 4 cm", ["Yaklaşık 4 m", "Yaklaşık 40 m", "Yaklaşık 400 cm"]),
             ("Bir okul sırasının boyu", "Yaklaşık 1 m", ["Yaklaşık 1 cm", "Yaklaşık 10 m", "Yaklaşık 100 m"]),
             ("Bir öğrencinin boyu", "Yaklaşık 120 cm", ["Yaklaşık 12 cm", "Yaklaşık 120 m", "Yaklaşık 12 m"]),
             ("Bir defterin eni", "Yaklaşık 20 cm", ["Yaklaşık 20 m", "Yaklaşık 2 cm", "Yaklaşık 200 m"]),
             ("Okul bahçesinin uzunluğu", "Yaklaşık 50 m", ["Yaklaşık 50 cm", "Yaklaşık 5 cm", "Yaklaşık 5 kg"]),
             ("Bir elmanın kütlesi", "Yaklaşık 200 g", ["Yaklaşık 200 kg", "Yaklaşık 2 kg", "Yaklaşık 20 kg"]),
             ("Bir çocuğun kütlesi", "Yaklaşık 25 kg", ["Yaklaşık 25 g", "Yaklaşık 250 kg", "Yaklaşık 2 g"]),
             ("Bir torba unun kütlesi", "Yaklaşık 5 kg", ["Yaklaşık 5 g", "Yaklaşık 500 kg", "Yaklaşık 50 g"]),
             ("Bir silginin kütlesi", "Yaklaşık 20 g", ["Yaklaşık 20 kg", "Yaklaşık 2 kg", "Yaklaşık 200 kg"]),
             ("Bir karpuzun kütlesi", "Yaklaşık 4 kg", ["Yaklaşık 4 g", "Yaklaşık 40 kg", "Yaklaşık 400 kg"]),
             ("Bir okul çantasının kütlesi", "Yaklaşık 3 kg", ["Yaklaşık 3 g", "Yaklaşık 300 kg", "Yaklaşık 30 g"]),
             ("Bir otomobilin uzunluğu", "Yaklaşık 4 m", ["Yaklaşık 4 cm", "Yaklaşık 40 m", "Yaklaşık 400 m"])]
        t, g, w = ch(S)
        return mq("%s hangisine en yakındır?" % t, g, w, "Gerçek nesneyi düşünürüz: <b>%s</b>." % g.lower())
    return named(f, "uzunluk_tahmin")


def cetvel(n, start=0):
    W = (n + start + 1) * 24 + 40
    s = ["<rect x='14' y='50' width='%d' height='30' fill='#fdf3c4' stroke='%s' stroke-width='1.5'/>" % ((n + start + 1) * 24 + 12, INK)]
    for i in range(n + start + 2):
        x = 20 + i * 24
        s.append("<line x1='%d' y1='50' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (x, x, 64 if True else 60, INK))
        s.append(text(x, 77, str(i), 10))
    s.append("<rect x='%d' y='26' width='%d' height='16' rx='7' fill='#7fb3d5' stroke='%s' stroke-width='1.5'/>" % (20 + start * 24, n * 24, INK))
    return pic(svg_wrap(W, 88, "".join(s), "cetvel ve nesne"), "cetvel üzerinde bir nesne")


def m_cetvel():
    def f():
        n = ri(2, 12)
        st = 0 if rnd() < 0.6 else ri(1, 3)
        return mq("Nesnenin boyu kaç santimetredir?%s" % cetvel(n, st), "%d cm" % n, ["%d cm" % x for x in (n + st, n + 1, n - 1, n + 2) if x != n and x > 0],
                  "%s<b>%d cm</b>." % ("Başlangıç %d, bitiş %d: %d − %d = " % (st, st + n, st + n, st) if st else "Sıfırdan başlıyor: ", n))
    return named(f, "cetvel")


def m_birim_sec():
    def f():
        S = [("bir kalemin boyunu", "santimetre (cm)"), ("sınıfın uzunluğunu", "metre (m)"), ("bir parmağın enini", "santimetre (cm)"),
             ("koridorun uzunluğunu", "metre (m)"), ("bir karpuzun ağırlığını", "kilogram (kg)"), ("bir kitabın boyunu", "santimetre (cm)"),
             ("bir çuval patatesin kütlesini", "kilogram (kg)"), ("bir ağacın yüksekliğini", "metre (m)"), ("bir yaprağın boyunu", "santimetre (cm)"),
             ("kendi kütleni", "kilogram (kg)")]
        t, g = ch(S)
        return mq("%s ölçmek için hangi birim daha uygundur?" % cap(t), cap(g), [cap(x) for x in ("santimetre (cm)", "metre (m)", "kilogram (kg)", "litre (L)") if x != g],
                  "Kısa uzunluklar cm, uzun uzunluklar m, kütle kg ile ölçülür. Cevap: <b>%s</b>." % g)
    return named(f, "birim_sec")


