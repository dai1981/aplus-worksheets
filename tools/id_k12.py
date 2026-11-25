# -*- coding: utf-8 -*-
"""
Indonesia / Matematika / Kelas 1・Kelas 2 (Fase A, Kurikulum Merdeka CP 2025)。
Kelas 1: 20 まで（数えるのは 20 まで）、Kelas 2: 100 まで（計算は 20 まで、CP Fase A のとおり）。とても短い文、ほぼ全問に絵。
python3 tools/id_k12.py 1 [番号…]   /   python3 tools/id_k12.py 2 [番号…]
seed は 40100 + sort（Kelas 1）、40200 + sort（Kelas 2）。
絵は k_pics（aria-label をインドネシア語に）。図形の合成・平面図形は Kelas 4 の問題関数（id_k4c）も使う。
"""
import math
import random
import re
import sys
import k_pics as P
from f_common import pattern_svg
import id_k4a as A
from id_k4a import ri, ch, pool, terbilang, cap, rel, stmt, pie, bar_frac
from id_common import (num, mcq, mix, lesson, example, table, make_unit, fig, svg_wrap, text, nilai_tempat,
                       INK, GREEN, FILL, RED)

BENDA = {"apple": "apel", "star": "bintang", "ball": "bola", "button": "kancing", "fish": "ikan", "flower": "bunga",
         "duck": "bebek", "cup": "cangkir", "bug": "kepik"}
KINDS = list(BENDA)
SHAPE = {"circle": "lingkaran", "triangle": "segitiga", "square": "persegi", "rectangle": "persegi panjang", "hexagon": "segi enam"}
WARNA = {"red": "merah", "blue": "biru", "yellow": "kuning", "green": "hijau"}
SIDES = {"circle": 0, "triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6}
NAMA = ["Asep", "Azizah", "Slamet", "Helen", "Putu", "Karel", "Andi", "Candra", "Tono", "Tini", "Wiwin", "Ali",
        "Nazilla", "Tiara", "Dayu", "Made", "Siti", "Beni", "Lina", "Rudi", "Dewi", "Agus", "Rina", "Yosef"]


def R():
    return A.R


def nm():
    return ch(NAMA)


def pic(svg, label, lg=False):
    svg = re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label.replace("'", "’"), svg, count=1)
    if lg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(svg)


def b(kind):
    return BENDA[kind]


def kata(n):
    return terbilang(n)


def near(n, lo=1, hi=100, ds=(1, -1, 2, -2, 10, -10)):
    return [str(n + d) for d in ds if lo <= n + d <= hi and d != 0]


def maker_of(d, name, i=0):
    out = []
    for _, parts in d["sets"]:
        for m, _n in parts:
            if m.__name__ == name and m not in out:
                out.append(m)
    return out[i]


def named(f, n):
    f.__name__ = n
    return f


# ------------------------------------------------------------ 絵
def baris(n, kind):
    return pic(P.row_svg(n, kind, 10 if n > 5 else 5), "%d %s berjajar" % (n, b(kind)))


def acak(n, kind):
    return pic(P.scatter_svg(n, kind, ri(1, 99999)), "%d %s" % (n, b(kind)))


def bingkai(n):
    return pic(P.tenframe_svg(n), "bingkai sepuluh berisi %d titik" % n)


def dadu(vals):
    return pic(P.dice_svg(vals), "dadu: " + ", ".join(map(str, vals)))


def dua(a, ka, bb, kb, sign):
    return pic(P.two_groups_svg(a, ka, bb, kb, sign), "%d %s %s %d %s" % (a, b(ka), "dan" if sign == "+" else sign, bb, b(kb)))


def coret(n, kind, k):
    return pic(P.crossed_row_svg(n, kind, k, 5), "%d %s, %d dicoret" % (n, b(kind), k))


def kotak(n, kind):
    return pic(P.box_svg(n, kind), "%d %s dan sebuah kotak tertutup" % (n, b(kind)))


def lompat(start, hops, lo, hi):
    return pic(P.hop_line_svg(start, hops, lo, hi), "garis bilangan dengan lompatan")


def ikatan(w, x, y):
    return pic(P.bond_svg(w, x, y), "pasangan bilangan")


def batang(t, o):
    return pic(P.rods_svg(t, o), "%d batang puluhan dan %d kubus satuan" % (t, o))


def menara(hs, labels=None):
    return pic(P.towers_svg(hs, labels), "menara kubus")


def timbangan(left, right, tilt):
    return pic(P.balance_svg(left, right, tilt), "timbangan")


def kelompok(g, k, kind):
    return pic(P.groups_svg([(k, kind)] * g), "%d kelompok, setiap kelompok %d %s" % (g, k, b(kind)))


def turus_svg(n, raw=False):
    s, x = [], 10
    full, rest = divmod(n, 5)
    for g in range(full + (1 if rest else 0)):
        k = 4 if g < full else rest
        for i in range(k):
            s.append("<line x1='%d' y1='8' x2='%d' y2='46' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (x + i * 9, x + i * 9, INK))
        if g < full:
            s.append("<line x1='%d' y1='40' x2='%d' y2='14' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (x - 5, x + 32, RED))
        x += 52
    sv = svg_wrap(x, 54, "".join(s), "turus")
    return sv if raw else fig(sv)


def balok_svg(color="#f4d03f"):
    s = ("<rect x='20' y='50' width='120' height='60' fill='%s' stroke='%s' stroke-width='2'/>"
         "<polygon points='20,50 50,24 170,24 140,50' fill='%s' fill-opacity='0.6' stroke='%s' stroke-width='2'/>"
         "<polygon points='140,50 170,24 170,84 140,110' fill='%s' stroke='%s' stroke-width='2'/>"
         "<polygon points='140,50 170,24 170,84 140,110' fill='#000' fill-opacity='0.15'/>" % (color, INK, color, INK, color, INK))
    return svg_wrap(190, 126, s, "balok")


COLS = {"yellow": "#f4d03f", "red": "#e74c3c", "blue": "#3498db", "green": "#27ae60"}


def solid_svg(kind, color="yellow", r=40):
    if kind == "balok":
        return balok_svg(COLS[color]).replace("viewBox='0 0 190 126'", "viewBox='0 0 190 126' style='width:%dpx'" % (r * 4.5), 1)
    return P.one_solid_svg(kind, color, r)


RUANG = {"sphere": "bola", "cube": "kubus", "cylinder": "tabung", "cone": "kerucut", "balok": "balok"}


# ============================================================ 共通の問題関数
def m_hitung(lo, hi):
    def f():
        n, kind = ri(lo, hi), ch(KINDS)
        k = ri(0, 2) if n <= 10 else ch([0, 3])
        p = baris(n, kind) if k == 0 else acak(n, kind) if k == 1 else bingkai(n) if n <= 10 else pic(P.tenframe_svg(n, 2), "dua bingkai sepuluh berisi %d titik" % n)
        what = "titik" if k >= 2 else b(kind)
        return mcq("Ada berapa %s?%s" % (what, p), str(n), near(n, 1, 100, (1, -1, 2, -2)), "Hitung satu per satu. Ada %d %s." % (n, what))
    return named(f, "hitung")


def m_kata(lo, hi):
    def f():
        n = ri(lo, hi)
        ws = [x for x in (int(str(n)[::-1]) if n > 10 and n % 10 else n + 2, n + 1, n - 1, n + 10, n - 10, n + 2, n - 2) if 0 <= x <= 100 and x != n]
        if R().random() < 0.5:
            return mcq("Lambang bilangan <i>%s</i> adalah …" % kata(n), str(n), [str(x) for x in ws], "%s ditulis %d." % (cap(kata(n)), n))
        return mcq("Bilangan <b>%d</b> dibaca …" % n, cap(kata(n)), [cap(kata(x)) for x in ws], "%d dibaca %s." % (n, kata(n)))
    return named(f, "kata")


def m_sesudah(lo, hi, steps=(1,)):
    def f():
        n, d = ri(lo, hi), ch(steps)
        k = ri(0, 2)
        if k == 0:
            if n + d > hi:
                return None
            return mcq("Bilangan sesudah %d adalah …" % n if d == 1 else "Bilangan yang %d lebih dari %d adalah …" % (d, n),
                       str(n + d), [str(n - d)] + near(n + d, 0, 120, (1, -1, 10 if d == 1 else 1)), "%d + %d = %d." % (n, d, n + d))
        if k == 1:
            if n - d < max(lo, 0):
                return None
            return mcq("Bilangan sebelum %d adalah …" % n if d == 1 else "Bilangan yang %d kurang dari %d adalah …" % (d, n),
                       str(n - d), [str(n + d)] + near(n - d, 0, 120, (1, -1, 2)), "%d − %d = %d." % (n, d, n - d))
        if n - 1 < lo or n + 1 > hi or d != 1:
            return None
        return mcq("Bilangan di antara %d dan %d adalah …" % (n - 1, n + 1), str(n), [str(n - 1), str(n + 1), str(n + 2), str(n - 2)],
                   "Urutannya %d, %d, %d." % (n - 1, n, n + 1))
    return named(f, "sesudah")


def m_urut(lo, hi, steps=(1,)):
    def f():
        d = ch(steps)
        s = ri(lo // d, (hi - 4 * d) // d) * d if lo % d == 0 else ri(lo, hi - 4 * d)
        if s < lo:
            return None
        xs = [s + d * i for i in range(5)]
        j = ri(1, 4)
        show = ", ".join(str(x) if i != j else "…" for i, x in enumerate(xs))
        return mcq("Bilangan yang hilang: %s" % show, str(xs[j]), near(xs[j], 0, 120, (1, -1, d + 1, -d - 1, 2 * d)),
                   "Setiap bilangan %s %d. Jadi %d." % ("bertambah", d, xs[j]))
    return named(f, "urut")


def m_banding_gambar(hi):
    def f():
        a, c = ri(2, hi), ri(2, hi)
        k1, k2 = pool(KINDS)[:2]
        if a == c and R().random() < 0.6:
            return None
        g = "%s lebih banyak" % cap(b(k1)) if a > c else "%s lebih banyak" % cap(b(k2)) if c > a else "Sama banyak"
        opts = ["%s lebih banyak" % cap(b(k1)), "%s lebih banyak" % cap(b(k2)), "Sama banyak", "Tidak bisa dihitung"]
        return mcq("Mana yang lebih banyak?%s%s" % (baris(a, k1), baris(c, k2)), g, [o for o in opts if o != g],
                   "Ada %d %s dan %d %s." % (a, b(k1), c, b(k2)))
    return named(f, "banding_gambar")


def m_banding(lo, hi):
    def f():
        a, c = ri(lo, hi), ri(lo, hi)
        if a == c:
            return None
        return stmt(str(a), str(c), a, c, "%d %s %d." % (a, rel(a, c), c))
    return named(f, "banding")


def m_ekstrem(lo, hi):
    def f():
        xs = sorted(set(ri(lo, hi) for _ in range(6)))
        if len(xs) < 4:
            return None
        xs = pool(xs)[:4]
        big = R().random() < 0.5
        c = max(xs) if big else min(xs)
        return mcq("Bilangan %s dari %s adalah …" % ("terbesar" if big else "terkecil", ", ".join(map(str, xs))), str(c), [str(x) for x in xs if x != c],
                   "Yang %s adalah %d." % ("terbesar" if big else "terkecil", c))
    return named(f, "ekstrem")


def m_urutkan(lo, hi):
    def f():
        xs = sorted(set(ri(lo, hi) for _ in range(6)))
        if len(xs) < 4:
            return None
        xs = pool(xs)[:4]
        up = R().random() < 0.5
        g = sorted(xs, reverse=not up)
        w3 = list(g)
        w3[1], w3[2] = w3[2], w3[1]
        fm = lambda ys: ", ".join(map(str, ys))
        return mcq("Urutkan dari yang %s: %s" % ("terkecil" if up else "terbesar", fm(xs)), fm(g), [fm(g[::-1]), fm(w3), fm(xs) if xs != g else fm(w3[::-1])],
                   "Urutannya %s." % fm(g))
    return named(f, "urutkan")


def m_tambah_gambar(mx):
    def f():
        a, c = ri(1, mx - 1), ri(1, mx - 1)
        if a + c > mx or a > 10 or c > 10:
            return None
        k1, k2 = pool(KINDS)[:2]
        return mcq("Berapa jumlah semuanya?%s" % dua(a, k1, c, k2, "+"), str(a + c), near(a + c, 1, 30, (1, -1, 2)) + [str(abs(a - c)) if a != c else None],
                   "%d + %d = %d." % (a, c, a + c))
    return named(f, "tambah_gambar")


def m_fakta(op, mx, cross=None):
    def f():
        a, c = ri(1, mx), ri(1, mx)
        if op == "+":
            if a + c > mx or (cross is not None and (a < 10 and c < 10 and a + c > 10) != cross):
                return None
            v, q = a + c, "%d + %d = …" % (a, c)
            ws = [v + 1, v - 1, v + 2, abs(a - c), v + 10]
        else:
            if c >= a or a > mx or (cross is not None and (10 < a < 20 and c < 10 and a % 10 < c) != cross):
                return None
            v, q = a - c, "%d − %d = …" % (a, c)
            ws = [v + 1, v - 1, a + c, v + 2]
        return mcq(q, str(v), [str(w) for w in ws if 0 <= w <= 40 and w != v] + ["0" if v else "1"], "%s = %d." % (q.replace(" = …", ""), v))
    return named(f, "fakta")


def m_coret(mx):
    def f():
        n, kind = ri(3, mx), ch(KINDS)
        k = ri(1, n - 1)
        if n > 10 and R().random() < 0.5:
            return None
        return mcq("Ada %d %s. Sebanyak %d dicoret. Berapa yang tersisa?%s" % (n, b(kind), k, coret(n, kind, k)), str(n - k),
                   near(n - k, 0, 30, (1, -1, 2)) + [str(n + k), str(k)], "%d − %d = %d." % (n, k, n - k))
    return named(f, "coret")


def m_lompat(op, mx):
    def f():
        hi = 10 if mx <= 10 else 20
        s, h = ri(0, hi), ri(1, 5)
        if op == "+":
            if s + h > hi:
                return None
            return mcq("Mulai dari %d, lompat %d kali ke kanan. Sampai di bilangan …%s" % (s, h, lompat(s, h, 0 if hi == 10 else 10, hi) if (hi == 10 or s >= 10) else lompat(s, h, 0, 10) if s + h <= 10 else ""),
                       str(s + h), near(s + h, 0, 20, (1, -1, 2)) + [str(s - h) if s >= h else None], "%d + %d = %d." % (s, h, s + h))
        if s - h < 0:
            return None
        return mcq("Mulai dari %d, lompat %d kali ke kiri. Sampai di bilangan …%s" % (s, h, lompat(s, -h, 0 if hi == 10 else 10, hi) if (hi == 10 or s - h >= 10) else lompat(s, -h, 0, 10) if s <= 10 else ""),
                   str(s - h), near(s - h, 0, 20, (1, -1, 2)) + [str(s + h)], "%d − %d = %d." % (s, h, s - h))
    return named(f, "lompat")


def m_kotak(mx):
    def f():
        t, kind = ri(4, mx), ch(KINDS)
        n = ri(1, min(t - 1, 10))
        return mcq("Semuanya ada %d %s. Sebagian ada di dalam kotak. Berapa %s di dalam kotak?%s" % (t, b(kind), b(kind), kotak(n, kind)), str(t - n),
                   near(t - n, 0, 30, (1, -1, 2)) + [str(t + n), str(n)], "%d − %d = %d." % (t, n, t - n))
    return named(f, "kotak")


def m_ikatan(mx):
    def f():
        w = ri(3, mx)
        a = ri(0, w)
        k = ri(0, 2)
        x = [str(w), str(a), str(w - a)]
        g = x[k]
        x[k] = "?"
        e = "%d + %d = %d." % (a, w - a, w)
        return mcq("Bilangan apa yang tepat untuk tanda ?%s" % ikatan(*x), g, near(int(g), 0, 30, (1, -1, 2)) + [str(w + a)], e)
    return named(f, "ikatan")


def m_kosong(mx):
    def f():
        a, c = ri(1, mx), ri(1, mx)
        if a + c > mx:
            return None
        s = a + c
        k = ri(0, 3)
        q = ["%d + … = %d" % (a, s), "… + %d = %d" % (c, s), "%d − … = %d" % (s, a), "… − %d = %d" % (c, a)][k]
        g = [c, a, c, s][k]
        return mcq("Bilangan yang tepat untuk … adalah …<br>%s" % q, str(g), near(g, 0, 40, (1, -1, 2)) + [str(s + (a if k != 1 else c))],
                   "%d + %d = %d." % (a, c, s))
    return named(f, "kosong")


ADD_C = [("%s punya %d kelereng. Ia mendapat %d kelereng lagi. Berapa kelereng %s sekarang?", "kelereng"),
         ("Di kolam ada %d ikan. Lalu datang %d ikan lagi. Berapa ikan di kolam sekarang?", "ikan"),
         ("%s memetik %d jeruk dan %d jambu. Berapa buah yang dipetik %s?", "buah"),
         ("Di dahan ada %d burung. Kemudian hinggap %d burung lagi. Berapa burung sekarang?", "burung"),
         ("%s membawa %d pensil merah dan %d pensil biru. Berapa pensil %s semuanya?", "pensil"),
         ("Ada %d anak bermain bola dan %d anak bermain lompat tali. Berapa anak semuanya?", "anak")]
SUB_C = [("%s punya %d permen. Ia memakan %d permen. Berapa permen %s yang tersisa?", "permen"),
         ("Ada %d balon. Sebanyak %d balon meletus. Berapa balon yang tersisa?", "balon"),
         ("Di pohon ada %d mangga. Ibu memetik %d mangga. Berapa mangga yang masih di pohon?", "mangga"),
         ("Di bus ada %d penumpang. Sebanyak %d penumpang turun. Berapa penumpang yang masih di bus?", "penumpang"),
         ("%s punya %d stiker. Ia memberikan %d stiker kepada adiknya. Berapa stiker %s sekarang?", "stiker")]
DIF_C = [("%s punya %d buku. %s punya %d buku. Berapa selisih buku mereka?", "buku"),
         ("Ada %d ayam dan %d bebek. Berapa lebih banyak ayam daripada bebek?", "ekor")]


def m_cerita(mx, kinds="+-="):
    def f():
        k = ch(kinds)
        x = nm()
        if k == "+":
            t, un = ch(ADD_C)
            a, c = ri(1, mx - 1), ri(1, mx - 1)
            if a + c > mx:
                return None
            q = t % ((x, a, c, x) if t.count("%s") == 2 else (a, c))
            v, e = a + c, "Digabung, jadi dijumlah: %d + %d = %d." % (a, c, a + c)
            ws = [abs(a - c), v + 1, v - 1]
        elif k == "-":
            t, un = ch(SUB_C)
            a = ri(3, mx)
            c = ri(1, a - 1)
            q = t % ((x, a, c, x) if t.count("%s") == 2 else (a, c))
            v, e = a - c, "Diambil, jadi dikurangi: %d − %d = %d." % (a, c, a - c)
            ws = [a + c, v + 1, v - 1]
        else:
            t, un = ch(DIF_C)
            a, c = ri(5, mx), ri(1, mx)
            if c >= a:
                return None
            y = ch([n for n in NAMA if n != x])
            q = t % ((x, a, y, c) if t.count("%s") == 2 else (a, c))
            v, e = a - c, "Selisih = %d − %d = %d." % (a, c, a - c)
            ws = [a + c, v + 1, v - 1]
        return mcq(q, "%d %s" % (v, un), ["%d %s" % (w, un) for w in ws if w >= 0 and w != v] + ["%d %s" % (v + 2, un)], e)
    return named(f, "cerita")


# ------------------------------------------------------------ 図形・位置・測定・データ
def m_nama_datar(kinds=("circle", "triangle", "square", "rectangle")):
    def f():
        k, col = ch(kinds), ch(list(WARNA))
        rot = ch([0, 0, 20, -20, 45]) if k not in ("circle",) else 0
        if k == "square" and rot == 45:
            rot = 0
        return mcq("Nama bangun ini adalah …%s" % pic(P.one_shape_svg(k, col, 40, rot), "sebuah bangun datar %s" % WARNA[col]), SHAPE[k],
                   [SHAPE[x] for x in SHAPE if x != k], "Bangun ini %s." % SHAPE[k])
    return named(f, "nama_datar")


def m_cari_datar(kinds=("circle", "triangle", "square", "rectangle")):
    def f():
        ks = pool(kinds)[:4] if len(kinds) >= 4 else None
        items = [(k, ch(list(WARNA))) for k in ks]
        t = ch(ks)
        return mcq("Manakah yang berbentuk %s?%s" % (SHAPE[t], pic(P.lettered_shapes_svg(items), "bangun A sampai D")), "ABCD"[ks.index(t)],
                   [c for c in "ABCD" if c != "ABCD"[ks.index(t)]], "Gambar %s adalah %s." % ("ABCD"[ks.index(t)], SHAPE[t]))
    return named(f, "cari_datar")


def m_sisi(kinds=("triangle", "square", "rectangle", "hexagon")):
    def f():
        k, col = ch(kinds), ch(list(WARNA))
        what = ch(["sisi", "titik sudut"])
        n = SIDES[k]
        return mcq("Berapa banyak %s pada bangun ini?%s" % (what, pic(P.one_shape_svg(k, col, 40, ch([0, 15, -15])), SHAPE[k])), str(n),
                   [str(x) for x in (n + 1, n - 1, n + 2, 0) if x != n], "%s punya %d sisi dan %d titik sudut." % (cap(SHAPE[k]), n, n))
    return named(f, "sisi")


def m_hitung_datar():
    def f():
        t = ch(["circle", "triangle", "square"])
        n = ri(1, 5)
        others = [k for k in ("circle", "triangle", "square", "rectangle") if k != t]
        items = [(t, ch(list(WARNA))) for _ in range(n)] + [(ch(others), ch(list(WARNA))) for _ in range(ri(3, 7))]
        if len(items) > 15:
            return None
        R().shuffle(items)
        return mcq("Ada berapa %s pada gambar?%s" % (SHAPE[t], pic(P.shapes_mix_svg(items, ri(1, 9999)), "berbagai bangun datar")), str(n),
                   [str(x) for x in (n + 1, n - 1, n + 2, len(items)) if x != n and x >= 0], "Ada %d %s." % (n, SHAPE[t]))
    return named(f, "hitung_datar")


BENTUK_NYATA = [("jam dinding", "lingkaran"), ("roda sepeda", "lingkaran"), ("uang logam", "lingkaran"), ("piring", "lingkaran"),
                ("papan tulis", "persegi panjang"), ("pintu", "persegi panjang"), ("buku tulis", "persegi panjang"), ("bendera Indonesia", "persegi panjang"),
                ("ubin lantai", "persegi"), ("sapu tangan", "persegi"), ("papan catur", "persegi"),
                ("potongan roti lapis", "segitiga"), ("rambu jalan peringatan", "segitiga"), ("atap rumah (dari depan)", "segitiga")]


def m_datar_nyata():
    def f():
        o, g = ch(BENTUK_NYATA)
        return mcq("Bentuk %s mirip bangun …" % o, g, [x for x in ("lingkaran", "segitiga", "persegi", "persegi panjang") if x != g],
                   "%s berbentuk %s." % (cap(o), g))
    return named(f, "datar_nyata")


RUANG_NYATA = [("bola sepak", "bola"), ("kelereng", "bola"), ("jeruk", "bola"), ("dadu", "kubus"), ("kotak kado berbentuk kubus", "kubus"),
               ("kaleng susu", "tabung"), ("gelas", "tabung"), ("drum", "tabung"), ("topi ulang tahun", "kerucut"), ("cone es krim", "kerucut"),
               ("tumpeng", "kerucut"), ("kotak sepatu", "balok"), ("lemari", "balok"), ("batu bata", "balok"), ("kotak pensil", "balok")]


def m_ruang():
    def f():
        k = ch(list(RUANG))
        return mcq("Nama bangun ruang ini adalah …%s" % pic(solid_svg(k, ch(list(COLS)), ri(34, 44)), "bangun ruang"), RUANG[k], [RUANG[x] for x in RUANG if x != k],
                   "Bangun ini %s." % RUANG[k])
    return named(f, "ruang")


def m_ruang_nyata():
    def f():
        o, g = ch(RUANG_NYATA)
        if R().random() < 0.5:
            others = pool([x for x, y in RUANG_NYATA if y != g])[:3]
            return mcq("Benda yang berbentuk %s adalah …  (%s)" % (g, ", ".join(sorted([o] + others))), o, others, "%s berbentuk %s." % (cap(o), g))
        return mcq("Bentuk %s seperti bangun ruang …" % o, g, [x for x in RUANG.values() if x != g], "%s berbentuk %s." % (cap(o), g))
    return named(f, "ruang_nyata")


def m_gelinding():
    def f():
        k = R().random()
        if k < 0.5:
            g = ch(["bola", "tabung", "kerucut"])
            o, _ = ch([x for x in RUANG_NYATA if x[1] == g])
            bad = pool([x for x, y in RUANG_NYATA if y in ("kubus", "balok")])[:3]
            return mcq("Manakah yang dapat menggelinding? (%s)" % ", ".join(sorted([o] + bad)), o, bad, "%s berbentuk %s, punya sisi lengkung, jadi dapat menggelinding." % (cap(o), g))
        g = ch(["kubus", "balok"])
        o, _ = ch([x for x in RUANG_NYATA if x[1] == g])
        bad = pool([x for x, y in RUANG_NYATA if y in ("bola", "tabung", "kerucut")])[:3]
        return mcq("Manakah yang tidak dapat menggelinding? (%s)" % ", ".join(sorted([o] + bad)), o, bad, "%s berbentuk %s, semua sisinya datar, jadi tidak menggelinding." % (cap(o), g))
    return named(f, "gelinding")


def m_meja():
    def f():
        kind = ch(KINDS)
        rel_ = ch(["above", "below", "beside", "beside-left"])
        g = {"above": "di atas meja", "below": "di bawah meja", "beside": "di samping kanan meja", "beside-left": "di samping kiri meja"}[rel_]
        return mcq("Di mana letak %s?%s" % (b(kind), pic(P.table_scene_svg(kind, rel_), "meja dan %s" % b(kind))), g,
                   [x for x in ("di atas meja", "di bawah meja", "di samping kanan meja", "di samping kiri meja") if x != g], "%s ada %s." % (cap(b(kind)), g))
    return named(f, "meja")


def m_kardus():
    def f():
        kind = ch(KINDS)
        rel_ = ch(["front", "behind", "beside", "above"])
        g = {"front": "di depan kardus", "behind": "di belakang kardus", "beside": "di samping kardus", "above": "di atas kardus"}[rel_]
        return mcq("Di mana letak %s?%s" % (b(kind), pic(P.box_scene_svg(kind, rel_), "kardus dan %s" % b(kind))), g,
                   [x for x in ("di depan kardus", "di belakang kardus", "di samping kardus", "di atas kardus") if x != g], "%s ada %s." % (cap(b(kind)), g))
    return named(f, "kardus")


def m_rak():
    def f():
        ks = pool(KINDS)[:4]
        i = ri(0, 3)
        k = ri(0, 2)
        p = pic(P.shelf_svg(ks), "rak dengan %s" % ", ".join(b(x) for x in ks))
        if k == 0:
            pos = ["paling atas", "kedua dari atas", "ketiga dari atas", "paling bawah"][i]
            return mcq("Benda apa yang ada di rak %s?%s" % (pos, p), b(ks[i]), [b(x) for x in ks if x != ks[i]], "Rak %s berisi %s." % (pos, b(ks[i])))
        if i == 0:
            return None
        if k == 1:
            return mcq("Benda apa yang ada tepat di atas %s?%s" % (b(ks[i]), p), b(ks[i - 1]), [b(x) for x in ks if x != ks[i - 1]], "Tepat di atas %s ada %s." % (b(ks[i]), b(ks[i - 1])))
        return mcq("Benda apa yang ada tepat di bawah %s?%s" % (b(ks[i - 1]), p), b(ks[i]), [b(x) for x in ks if x != ks[i]], "Tepat di bawah %s ada %s." % (b(ks[i - 1]), b(ks[i])))
    return named(f, "rak")


def m_kanan_kiri():
    def f():
        ks = pool(KINDS)[:5]
        i = ri(0, 4)
        p = pic(P.kinds_row_svg(ks), "deretan " + ", ".join(b(x) for x in ks))
        k = ri(0, 2)
        if k == 0:
            pos = ri(1, 5)
            side = ch(["kiri", "kanan"])
            j = pos - 1 if side == "kiri" else 5 - pos
            return mcq("Benda ke-%d dari %s adalah …%s" % (pos, side, p), b(ks[j]), [b(x) for x in ks if x != ks[j]],
                       "Hitung dari %s: benda ke-%d adalah %s." % (side, pos, b(ks[j])))
        if k == 1 and i < 4:
            return mcq("Benda apa yang ada tepat di sebelah kanan %s?%s" % (b(ks[i]), p), b(ks[i + 1]), [b(x) for x in ks if x != ks[i + 1]],
                       "Di sebelah kanan %s ada %s." % (b(ks[i]), b(ks[i + 1])))
        if k == 2 and i > 0:
            return mcq("Benda apa yang ada tepat di sebelah kiri %s?%s" % (b(ks[i]), p), b(ks[i - 1]), [b(x) for x in ks if x != ks[i - 1]],
                       "Di sebelah kiri %s ada %s." % (b(ks[i]), b(ks[i - 1])))
        return None
    return named(f, "kanan_kiri")


def m_panjang():
    def f():
        ls = pool(range(3, 10))[:ri(3, 4)]
        long_ = R().random() < 0.5
        c = max(ls) if long_ else min(ls)
        i = ls.index(c)
        return mcq("Pensil mana yang paling %s?%s" % ("panjang" if long_ else "pendek", pic(P.pencils_svg(ls), "pensil A sampai %s" % "ABCD"[len(ls) - 1])),
                   "Pensil " + "ABCD"[i], ["Pensil " + "ABCD"[j] for j in range(len(ls)) if j != i] + ["Semua sama panjang"],
                   "Ujung kiri pensil sejajar. Pensil %s ujungnya paling %s." % ("ABCD"[i], "jauh" if long_ else "dekat"))
    return named(f, "panjang")


def m_tinggi():
    def f():
        hs = pool(range(2, 10))[:ri(3, 4)]
        k = ri(0, 2)
        p = menara(hs)
        if k == 2:
            i = ri(0, len(hs) - 1)
            return mcq("Menara %s tingginya berapa kubus?%s" % ("ABCD"[i], p), "%d kubus" % hs[i], ["%d kubus" % x for x in (hs[i] + 1, hs[i] - 1, hs[i] + 2)],
                       "Hitung kubusnya: %d." % hs[i])
        tall = k == 0
        c = max(hs) if tall else min(hs)
        i = hs.index(c)
        return mcq("Menara mana yang paling %s?%s" % ("tinggi" if tall else "rendah", p), "Menara " + "ABCD"[i], ["Menara " + "ABCD"[j] for j in range(len(hs)) if j != i] + ["Sama tinggi"],
                   "Menara %s punya %d kubus, paling %s." % ("ABCD"[i], c, "banyak" if tall else "sedikit"))
    return named(f, "tinggi")


BERAT = ["apple", "ball", "cup", "fish", "duck", "flower"]


def m_berat():
    def f():
        k1, k2 = pool(BERAT)[:2]
        tilt = ch(["left", "right"])
        heavy = k1 if tilt == "left" else k2
        light = k2 if tilt == "left" else k1
        q = ch(["berat", "ringan"])
        g = heavy if q == "berat" else light
        return mcq("Perhatikan timbangan. Mana yang lebih %s?%s" % (q, timbangan((k1, 1), (k2, 1), tilt)), cap(b(g)),
                   [cap(b(light if g == heavy else heavy)), "Sama berat", "Tidak bisa diketahui"],
                   "Sisi yang lebih berat turun ke bawah. %s lebih berat." % cap(b(heavy)))
    return named(f, "berat")


def m_seimbang():
    def f():
        k = ch(BERAT)
        n = ri(2, 6)
        return mcq("Timbangan seimbang. Satu %s sama beratnya dengan berapa kubus?%s" % (b(k), timbangan((k, 1), ("cube", n), "equal")), "%d kubus" % n,
                   ["%d kubus" % x for x in (n + 1, n - 1, 1, n + 2) if x != n and x > 0], "Timbangan seimbang, jadi 1 %s seberat %d kubus." % (b(k), n))
    return named(f, "seimbang")


SATUAN_TB = [("panjang meja", "jengkal"), ("panjang kelas", "langkah"), ("panjang pensil", "klip kertas"), ("lebar buku", "jari")]


def m_ukur_nb():
    def f():
        x, y = pool(NAMA)[:2]
        what, un = ch(SATUAN_TB)
        a, c = ri(5, 15), ri(5, 15)
        if a == c:
            return None
        if R().random() < 0.5:
            return mcq("%s mengukur %s dan mendapat %d %s. %s mendapat %d %s. Kenapa hasilnya berbeda?" % (x, what, a, un, y, c, un),
                       "Ukuran %s mereka berbeda" % un, ["Mejanya berubah", "Salah satu menghitung terbalik", "Satuan tidak baku selalu sama"],
                       "Setiap orang punya %s yang berbeda ukurannya, jadi hasilnya bisa berbeda." % un)
        big = max(a, c)
        g = x if a == big else y
        return mcq("%s mengukur dengan %d %s, %s dengan %d %s pada benda yang berbeda (%s sama besar). Benda siapa yang lebih panjang?" % (x, a, un, y, c, un, un),
                   "Benda %s" % g, ["Benda %s" % (y if g == x else x), "Sama panjang", "Tidak bisa dibandingkan"], "%d %s lebih banyak, jadi lebih panjang." % (big, un))
    return named(f, "ukur_nb")


POLA_SH = ["circle", "triangle", "square"]


def m_pola():
    def f():
        k = ri(0, 1)
        unit_len = ch([2, 2, 3, 3, 4])
        if k == 0:
            base = [("shape", s, c) for s, c in zip(pool(POLA_SH)[:3], pool(list(WARNA))[:3])]
            name_ = lambda it: "%s %s" % (SHAPE[it[1]], WARNA[it[2]])
        else:
            base = [("obj", x) for x in pool(KINDS)[:3]]
            name_ = lambda it: b(it[1])
        tpl = ch({2: ["AB"], 3: ["ABC", "AAB", "ABB"], 4: ["AABB", "ABAC"]}[unit_len])
        seq = [base["ABC".index(ch_)] for ch_ in tpl] * 3
        L = ri(len(tpl) + 2, min(len(seq) - 1, 8))
        shown, nxt = seq[:L], seq[L]
        cands = list({name_(x) for x in base})
        return mcq("Gambar apa yang tepat untuk tanda ?%s" % pic(pattern_svg(shown, 1), "pola berulang"), name_(nxt), [c for c in cands if c != name_(nxt)] + ["tidak ada"],
                   "Polanya berulang: %s. Berikutnya %s." % (", ".join(name_(x) for x in seq[:len(tpl)]), name_(nxt)))
    return named(f, "pola")


def m_pola_bil(mx, steps=(1, 2), up_=None):
    def f():
        d = ch(steps)
        up = (R().random() < 0.6) if up_ is None else up_
        s = ri(0, mx - 5 * d)
        xs = [s + d * i for i in range(5)]
        if not up:
            xs = xs[::-1]
        nx = xs[-1] + (d if up else -d)
        if nx < 0 or nx > mx:
            return None
        return mcq("Bilangan berikutnya: %s, …" % ", ".join(map(str, xs)), str(nx), near(nx, 0, 120, (1, -1, d + 1, -d - 1)) + [str(xs[-1])],
                   "Setiap langkah %s %d." % ("ditambah" if up else "dikurangi", d))
    return named(f, "pola_bil")


KAT = [("buah kesukaan siswa", ["Apel", "Jeruk", "Pisang", "Mangga"]), ("warna kesukaan siswa", ["Merah", "Biru", "Kuning", "Hijau"]),
       ("hewan peliharaan siswa", ["Kucing", "Ikan", "Burung", "Kelinci"]), ("mainan di kelas", ["Bola", "Boneka", "Mobil", "Balok"])]


def pikto(cats, vals, kind):
    rows = "".join("<tr><td>%s</td><td style='text-align:left'>%s</td></tr>" % (c, re.sub(r"aria-label='[^']*'", "aria-label='%d gambar'" % v, P.row_svg(v, kind, 10)).replace("<svg ", "<svg style='height:30px;width:auto' ", 1) if v else "")
                   for c, v in zip(cats, vals))
    return "<table class='sn-table' style='width:auto'><tbody>%s</tbody></table>" % rows


def tabel_turus(cats, vals):
    rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (c, turus_svg(v, True).replace("<svg ", "<svg style='height:26px;width:auto' ", 1)) for c, v in zip(cats, vals))
    return "<table class='sn-table' style='width:auto'><thead><tr><th>Pilihan</th><th>Turus</th></tr></thead><tbody>%s</tbody></table>" % rows


def m_turus(mx):
    def f():
        n = ri(2, mx)
        k = ri(0, 2)
        if k == 1 and n >= 5:
            return mcq("Ada berapa ikatan lima pada turus ini?%s" % turus_svg(n), str(n // 5), [str(x) for x in (n // 5 + 1, n, n % 5, n // 5 + 2) if x != n // 5],
                       "Setiap ikatan = 5 garis. Ada %d ikatan." % (n // 5))
        if k == 2 and n < mx:
            return mcq("Turus ini ditambah 1 garis lagi. Bilangannya menjadi …%s" % turus_svg(n), str(n + 1), near(n + 1, 1, 30, (1, -1, 5)),
                       "%d + 1 = %d." % (n, n + 1))
        return mcq("Turus ini menunjukkan bilangan …%s" % turus_svg(n), str(n), near(n, 1, 30, (1, -1, 5, -5)),
                   "Satu ikatan = 5. %d ikatan dan %d garis = %d." % (n // 5, n % 5, n))
    return named(f, "turus")


def m_data(mx, how="pikto", kind_q="all"):
    def f():
        t, cats = ch(KAT)
        k = ri(3, 4)
        cats = cats[:k]
        vals = [ri(1, mx) for _ in cats]
        if len(set(vals)) < k:
            return None
        kind = "dot"
        disp = pikto(cats, vals, kind) if how == "pikto" else tabel_turus(cats, vals)
        intro = ("Piktogram %s (1 gambar = 1 siswa)." % t if how == "pikto" else "Tabel turus %s." % t)
        q = ri(0, 3) if kind_q == "all" else ch(kind_q)
        if q == 0:
            i = ri(0, k - 1)
            return mcq("%s%sBerapa yang memilih %s?" % (intro, disp, cats[i]), str(vals[i]), near(vals[i], 0, 40, (1, -1, 2)) + [str(sum(vals))], "%s: %d." % (cats[i], vals[i]))
        if q == 1:
            big = R().random() < 0.5
            c = max(vals) if big else min(vals)
            i = vals.index(c)
            return mcq("%s%sPilihan mana yang paling %s?" % (intro, disp, "banyak" if big else "sedikit"), cats[i], [x for x in cats if x != cats[i]] + ["Semua sama banyak"], "%s: %d." % (cats[i], c))
        i, j = pool(range(k))[:2]
        if q == 2:
            if vals[i] == vals[j]:
                return None
            a, c = max(vals[i], vals[j]), min(vals[i], vals[j])
            return mcq("%s%sBerapa selisih %s dan %s?" % (intro, disp, cats[i], cats[j]), str(a - c), near(a - c, 0, 40, (1, -1)) + [str(a + c)], "%d − %d = %d." % (a, c, a - c))
        s = vals[i] + vals[j]
        return mcq("%s%sBerapa jumlah %s dan %s?" % (intro, disp, cats[i], cats[j]), str(s), near(s, 0, 60, (1, -1, 2)) + [str(abs(vals[i] - vals[j]))],
                   "%d + %d = %d." % (vals[i], vals[j], s))
    return named(f, "data_" + how)


# ------------------------------------------------------------ Kelas 2 だけの問題関数
def m_batang(lo, hi):
    def f():
        n = ri(lo, hi)
        t, o = divmod(n, 10)
        return mcq("Bilangan yang ditunjukkan gambar adalah …%s" % batang(t, o), str(n), [str(o * 10 + t) if o else str(n + 1), str(n + 10) if n + 10 <= 100 else str(n - 10), str(t + o), str(n - 1)],
                   "%d puluhan dan %d satuan = %d." % (t, o, n))
    return named(f, "batang")


def m_puluhan(kinds=(0, 1, 2, 3)):
    def f():
        n = ri(11, 99)
        t, o = divmod(n, 10)
        if o == 0 or t == o:
            return None
        k = ch(kinds)
        if k == 0:
            return mcq("Pada bilangan %d, angka %d bernilai …" % (n, t), str(t * 10), [str(t), str(o), str(o * 10), str(n)], "Angka %d di tempat puluhan, nilainya %d." % (t, t * 10))
        if k == 1:
            return mcq("Bentuk panjang %d adalah …" % n, "%d + %d" % (t * 10, o), ["%d + %d" % (t, o), "%d + %d" % (o * 10, t), "%d + %d" % (t * 10, o * 10)],
                       "%d = %d puluhan + %d satuan = %d + %d." % (n, t, o, t * 10, o))
        if k == 2:
            return mcq("%d puluhan + %d satuan = …" % (t, o), str(n), [str(o * 10 + t), str(t + o), str(t * 10 + o * 10) if t + o < 10 else str(n + 1)], "%d + %d = %d." % (t * 10, o, n))
        return mcq("Bilangan pada tabel nilai tempat ini adalah …" + nilai_tempat(n, 2), str(n), [str(o * 10 + t), str(t + o), str(n + 10) if n < 90 else str(n - 10)],
                   "Puluhan %d, satuan %d: %d." % (t, o, n))
    return named(f, "puluhan")


def m_genap():
    def f():
        n = ri(2, 99)
        k = ri(0, 2)
        if k == 0:
            g = "genap" if n % 2 == 0 else "ganjil"
            return mcq("Bilangan %d termasuk bilangan …" % n, g, ["ganjil" if g == "genap" else "genap", "puluhan", "nol"],
                       "Angka satuannya %d, jadi %s." % (n % 10, g))
        xs = pool([x for x in range(n, n + 8)])[:4]
        ev = [x for x in xs if x % 2 == (0 if k == 1 else 1)]
        if len(ev) != 1:
            return None
        return mcq("Manakah bilangan %s?" % ("genap" if k == 1 else "ganjil"), str(ev[0]), [str(x) for x in xs if x != ev[0]],
                   "Bilangan %s berakhiran %s." % ("genap" if k == 1 else "ganjil", "0, 2, 4, 6, 8" if k == 1 else "1, 3, 5, 7, 9"))
    return named(f, "genap")


def m_kesamaan(mx):
    def f():
        a, c = ri(1, mx - 1), ri(1, mx - 1)
        s = a + c
        if s > mx:
            return None
        d = ri(1, mx - 1)
        if d >= s or d in (a, c):
            return None
        k = ri(0, 2)
        if k == 0:
            g = s - d
            return mcq("%d + %d = %d + …" % (a, c, d), str(g), [str(s), str(s + d), str(g + 1)], "%d + %d = %d, dan %d + %d = %d." % (a, c, s, d, g, s))
        if k == 1:
            good = "%d + %d" % (d, s - d)
            return mcq("Manakah yang sama dengan %d + %d?" % (a, c), good, ["%d + %d" % (d, s - d + 1), "%d − %d" % (s, d), "%d + %d" % (d + 1, s - d + 1)],
                       "Keduanya bernilai %d." % s)
        t = ch([True, False])
        dd = s - d if t else s - d + ch([1, -1, 2])
        if dd < 0:
            return None
        g = "benar" if t else "salah"
        return mcq("Benar atau salah? %d + %d = %d + %d" % (a, c, d, dd), cap(g), ["Benar" if g == "salah" else "Salah", "Hanya benar jika dibalik", "Tidak bisa diketahui"],
                   "Kiri: %d. Kanan: %d. Jadi %s." % (s, d + dd, g))
    return named(f, "kesamaan")


def m_timb_bil(mx):
    def f():
        a, c = ri(1, 9), ri(1, 9)
        s = a + c
        d = ri(1, s - 1)
        return mcq("Timbangan seimbang jika kedua sisi sama. Kiri: %d + %d. Kanan: %d + … Bilangan yang tepat adalah …" % (a, c, d), str(s - d),
                   [str(s), str(s - d + 1), str(s + d)], "%d + %d = %d, jadi %d + %d = %d." % (a, c, s, d, s - d, s))
    return named(f, "timb_bil")


def m_pecahan_gambar():
    def f():
        n, k = ch([(2, 1), (4, 1), (4, 2), (4, 3), (1, 1)])
        col = ch(["#f4a261", "#7fb3d5", "#a8d5ba", "#f2c94c"])
        p = pie(max(n, 1), k, ch([50, 60, 70]), col) if R().random() < 0.5 else bar_frac(n, k, ch([240, 300, 360]), 40, col)
        name_ = {(2, 1): "setengah", (4, 1): "seperempat", (4, 2): "setengah", (4, 3): "tiga perempat", (1, 1): "utuh"}[(n, k)]
        opts = ["setengah", "seperempat", "utuh", "tiga perempat"]
        return mcq("Bagian yang diarsir adalah …%s" % p, name_, [o for o in opts if o != name_],
                   "Dibagi %d sama besar, %d bagian diarsir: %s." % (n, k, name_) if n > 1 else "Semua bagian diarsir: utuh.")
    return named(f, "pecahan_gambar")


def m_pecahan_benda(ks=(2, 4)):
    def f():
        k = ch(ks)
        g = ri(1, 5)
        n = k * g
        kind = ch(KINDS)
        w = "setengah" if k == 2 else "seperempat"
        x = nm()
        return mcq("%s punya %d %s. %s dari %s itu diberikan kepada adiknya. Berapa %s yang diberikan?%s" % (x, n, b(kind), cap(w), b(kind), b(kind), kelompok(k, g, kind)),
                   str(g), near(g, 1, 20, (1, -1)) + [str(n - g), str(n)], "%d dibagi %d sama banyak = %d." % (n, k, g))
    return named(f, "pecahan_benda")


def m_pecahan_kata():
    def f():
        BANK = [("Sebuah roti dibagi 2 sama besar. Satu bagian disebut …", "setengah", ["seperempat", "utuh", "sepertiga"]),
                ("Sebuah pizza dibagi 4 sama besar. Satu potong disebut …", "seperempat", ["setengah", "utuh", "sepertiga"]),
                ("Dua bagian seperempat sama dengan …", "setengah", ["seperempat", "utuh", "tiga perempat"]),
                ("Empat bagian seperempat sama dengan …", "utuh", ["setengah", "seperempat", "dua"]),
                ("Dua bagian setengah sama dengan …", "utuh", ["seperempat", "setengah", "empat"]),
                ("Mana yang lebih besar: setengah kue atau seperempat kue yang sama?", "setengah kue", ["seperempat kue", "sama besar", "tidak bisa dibandingkan"]),
                ("Kertas dilipat dua sama besar. Setiap bagian adalah …", "setengah", ["seperempat", "utuh", "dua"]),
                ("Kertas dilipat dua kali menjadi 4 bagian sama besar. Setiap bagian adalah …", "seperempat", ["setengah", "utuh", "empat"]),
                ("Semangka dibagi 4 sama besar. Andi makan 1 bagian. Andi makan … semangka.", "seperempat", ["setengah", "utuh", "empat"]),
                ("Apel dipotong 2 sama besar. Tini dan Beni masing-masing mendapat …", "setengah", ["seperempat", "utuh", "dua"])]
        q, g, w = ch(BANK)
        return mcq(q, g, w, "Jawabannya %s." % g)
    return named(f, "pecahan_kata")


# ============================================================ Kelas 1
def K1():
    U = []
    U.append(dict(slug="bilangan-sampai-10", dom="B", title="Bilangan sampai 10", short="Bilangan sampai 10",
                  std="Peserta didik menunjukkan pemahaman dan memiliki intuisi bilangan (number sense) pada bilangan cacah sampai 10: membilang, membaca, dan menulis bilangan.",
                  meta="Latihan bilangan sampai 10 untuk kelas 1 SD: menghitung benda, bingkai sepuluh, dadu, membaca dan menulis bilangan, sebelum dan sesudah. 100 soal dengan kunci jawaban.",
                  kb="Hitung satu per satu", ks="Bilangan terakhir yang disebut = banyaknya benda.",
                  sets=[("Menghitung benda", [(m_hitung(1, 10), 20)]), ("Membaca dan menulis bilangan", [(m_kata(0, 10), 20)]),
                        ("Dadu dan bingkai sepuluh", [(named(lambda: (lambda v: mcq("Berapa banyak titik pada dadu?" + dadu(v), str(sum(v)), near(sum(v), 1, 12, (1, -1, 2)), "Hitung titiknya: %d." % sum(v)))([ri(1, 6)] + ([ri(1, 4)] if R().random() < 0.4 else [])), "dadu"), 10), (m_hitung(1, 10), 10)]),
                        ("Sebelum dan sesudah", [(m_sesudah(0, 10), 20)]), ("Bilangan yang hilang", [(m_urut(0, 10), 14), (m_banding_gambar(10), 6)])],
                  think=["Hitung benda satu per satu. Tunjuk setiap benda satu kali.", "Bilangan terakhir yang kita sebut adalah banyaknya benda.", "Sesudah berarti tambah 1. Sebelum berarti kurang 1."],
                  ex=[("Ada berapa apel? (7 apel)", ["satu, dua, tiga, empat, lima, enam, tujuh"], "7"), ("Bilangan sesudah 5?", ["5 + 1"], "6")],
                  mist=[["Ada benda yang dihitung dua kali", "Tandai benda yang sudah dihitung"], ["Sesudah 8 dijawab 7", "Sesudah berarti tambah 1: 9"], ["Angka 6 dan 9 tertukar", "Perhatikan bulatan 6 di bawah, 9 di atas"]],
                  faq=[["Bagaimana cara menghitung benda yang berserakan?", "Hitung dari kiri ke kanan atau dari atas ke bawah, dan tandai benda yang sudah dihitung."], ["Apa itu bingkai sepuluh?", "Kotak berisi 10 tempat (2 baris, masing-masing 5). Membantu melihat banyak benda dengan cepat."], ["Bilangan berapa sesudah 9?", "Sesudah 9 adalah 10 (sepuluh)."]]))
    U.append(dict(slug="penjumlahan-sampai-10", dom="B", title="Penjumlahan sampai 10", short="Penjumlahan sampai 10",
                  std="Peserta didik melakukan operasi penjumlahan menggunakan benda-benda konkret yang banyaknya sampai 10.",
                  meta="Latihan penjumlahan sampai 10 untuk kelas 1 SD: menggabungkan gambar, lompat di garis bilangan, pasangan bilangan, dan soal cerita. 100 soal dengan kunci jawaban.",
                  kb="Tambah = menggabungkan", ks="3 + 4 = 7: gabungkan 3 dan 4 benda.",
                  sets=[("Menggabungkan gambar", [(m_tambah_gambar(10), 20)]), ("Lompat di garis bilangan", [(m_lompat("+", 10), 20)]),
                        ("Fakta penjumlahan", [(m_fakta("+", 10), 20)]), ("Pasangan bilangan", [(m_ikatan(10), 14), (m_kosong(10), 6)]),
                        ("Soal cerita", [(m_cerita(10, "+"), 20)])],
                  think=["Penjumlahan berarti menggabungkan dua kelompok benda.", "Mulai dari bilangan yang lebih besar, lalu hitung maju.", "Tanda + dibaca <i>tambah</i>, tanda = dibaca <i>sama dengan</i>."],
                  ex=[("4 + 3 = …", ["Mulai dari 4, hitung maju 3: 5, 6, 7"], "7"), ("2 + 6 = …", ["Mulai dari 6: 7, 8"], "8")],
                  mist=[["Menghitung ulang dari 1", "Mulai dari bilangan yang lebih besar"], ["4 + 3 dijawab 1", "Tambah berarti bertambah banyak: 7"], ["Lompatan pertama ikut dihitung dari angka awal", "Lompat dulu, baru hitung: 4 → 5, 6, 7"]],
                  faq=[["Apa arti penjumlahan?", "Penjumlahan adalah menggabungkan benda. 2 apel dan 3 apel digabung menjadi 5 apel."], ["Apakah 3 + 5 sama dengan 5 + 3?", "Ya, hasilnya sama, yaitu 8."], ["Apa itu pasangan bilangan?", "Dua bilangan yang jika dijumlahkan menjadi bilangan tertentu, misalnya 4 dan 6 adalah pasangan 10."]]))
    U.append(dict(slug="pengurangan-sampai-10", dom="B", title="Pengurangan sampai 10", short="Pengurangan sampai 10",
                  std="Peserta didik melakukan operasi pengurangan menggunakan benda-benda konkret yang banyaknya sampai 10.",
                  meta="Latihan pengurangan sampai 10 untuk kelas 1 SD: mencoret gambar, lompat mundur, benda di dalam kotak, dan soal cerita. 100 soal dengan kunci jawaban.",
                  kb="Kurang = mengambil", ks="7 − 3 = 4: ambil 3 dari 7.",
                  sets=[("Mencoret gambar", [(m_coret(10), 20)]), ("Lompat mundur", [(m_lompat("-", 10), 20)]), ("Fakta pengurangan", [(m_fakta("-", 10), 20)]),
                        ("Benda di dalam kotak", [(m_kotak(10), 14), (m_kosong(10), 6)]), ("Soal cerita", [(m_cerita(10, "-="), 20)])],
                  think=["Pengurangan berarti mengambil sebagian benda. Yang tersisa adalah hasilnya.", "Pada garis bilangan, pengurangan berarti lompat ke kiri.", "Tanda − dibaca <i>kurang</i>."],
                  ex=[("8 − 3 = …", ["Mulai dari 8, mundur 3: 7, 6, 5"], "5"), ("Ada 6 balon, 2 meletus. Sisa?", ["6 − 2"], "4 balon")],
                  mist=[["8 − 3 dijawab 11", "Kurang berarti berkurang: 5"], ["Mundur dimulai dengan menyebut 8", "Mundur dulu: 7, 6, 5"], ["Selisih dicari dengan menjumlah", "Selisih = besar − kecil"]],
                  faq=[["Apa arti pengurangan?", "Mengambil sebagian benda. Dari 7 kue dimakan 2, sisanya 7 − 2 = 5."], ["Bagaimana memeriksa hasil pengurangan?", "Jumlahkan hasilnya dengan bilangan pengurang. 5 + 2 = 7, jadi benar."], ["Apa itu selisih?", "Selisih adalah beda banyak dua kelompok benda."]]))
    U.append(dict(slug="bilangan-11-sampai-20", dom="B", title="Bilangan 11 sampai 20", short="Bilangan 11 sampai 20",
                  std="Peserta didik membaca, menulis, menentukan nilai tempat, melakukan komposisi dan dekomposisi bilangan cacah sampai 20.",
                  meta="Latihan bilangan 11 sampai 20 untuk kelas 1 SD: menghitung dengan dua bingkai sepuluh, sepuluh dan satuan, membaca belasan, garis bilangan. 100 soal dengan kunci jawaban.",
                  kb="Belasan = 10 dan satuan", ks="14 = 10 + 4, dibaca empat belas.",
                  sets=[("Menghitung sampai 20", [(m_hitung(11, 20), 20)]), ("Membaca belasan", [(m_kata(11, 20), 20)]),
                        ("Sepuluh dan satuan", [(m_batang(11, 20), 8), (named(lambda: (lambda o: mcq("10 + %d = …" % o, str(10 + o), [str(o), str(10 + o + 1), str(o * 10) if o > 1 else "100", str(10 + o - 1)], "10 dan %d satuan = %d." % (o, 10 + o)) if R().random() < 0.5 else mcq("%d = 10 + …" % (10 + o), str(o), [str(o + 1), str(10 + o), str(o - 1) if o > 1 else "10", "1"], "%d = 10 + %d." % (10 + o, o)))(ri(1, 9)), "sepuluh"), 12)]),
                        ("Sebelum dan sesudah", [(m_sesudah(10, 20), 20)]), ("Bilangan yang hilang", [(m_urut(10, 20), 20)])],
                  think=["Bilangan 11 sampai 19 terdiri dari 1 puluhan (10) dan beberapa satuan.", "11 dibaca <i>sebelas</i>. 12 sampai 19 dibaca dengan kata <i>belas</i>: 15 = lima belas.", "20 = 2 puluhan, dibaca <i>dua puluh</i>."],
                  ex=[("10 dan 6 = …", ["1 puluhan dan 6 satuan"], "16"), ("Bacalah 13.", ["3 + belas"], "tiga belas")],
                  mist=[["16 ditulis 61", "Puluhan ditulis dulu: 16"], ["11 dibaca satu belas", "11 dibaca sebelas"], ["Bilangan sesudah 19 ditulis 110", "Sesudah 19 adalah 20"]],
                  faq=[["Bagaimana membaca bilangan belasan?", "Sebut angka satuannya lalu tambahkan kata belas. 17 = tujuh belas. Khusus 11 dibaca sebelas."], ["Apa itu puluhan?", "Kelompok berisi 10 satuan."], ["Berapa puluhan dalam 20?", "20 = 2 puluhan."]]))
    U.append(dict(slug="membandingkan-dan-mengurutkan-bilangan", dom="B", title="Membandingkan dan Mengurutkan Bilangan sampai 20", short="Membandingkan Bilangan",
                  std="Peserta didik membandingkan dan mengurutkan bilangan cacah sampai 20.",
                  meta="Latihan membandingkan bilangan sampai 20 untuk kelas 1 SD: lebih banyak dan lebih sedikit, tanda <, > dan =, terbesar dan terkecil, mengurutkan. 100 soal dengan kunci jawaban.",
                  kb="Lebih banyak atau lebih sedikit?", ks="Bilangan di kanan garis bilangan lebih besar.",
                  sets=[("Lebih banyak", [(m_banding_gambar(10), 20)]), ("Menara kubus", [(m_tinggi(), 20)]), ("Tanda &lt;, &gt;, dan =", [(m_banding(0, 20), 20)]),
                        ("Terbesar dan terkecil", [(m_ekstrem(0, 20), 20)]), ("Mengurutkan", [(m_urutkan(0, 20), 20)])],
                  think=["Untuk membandingkan, pasangkan benda satu per satu. Yang tersisa lebih banyak.", "Pada garis bilangan, bilangan di sebelah kanan lebih besar.", "Tanda &lt; artinya kurang dari, &gt; artinya lebih dari."],
                  ex=[("Bandingkan 12 dan 9.", ["12 ada di kanan 9"], "12 &gt; 9"), ("Urutkan: 15, 8, 11", ["terkecil 8"], "8, 11, 15")],
                  mist=[["Gambar besar dianggap lebih banyak", "Hitung banyaknya, bukan besar gambarnya"], ["Arah tanda terbalik", "Mulut tanda terbuka ke bilangan yang lebih besar"], ["9 &gt; 12 karena 9 besar", "12 punya puluhan, jadi lebih besar"]],
                  faq=[["Bagaimana membandingkan dua kelompok benda?", "Hitung kedua kelompok, atau pasangkan benda satu per satu."], ["Apa arti tanda < dan >?", "< artinya kurang dari, > artinya lebih dari."], ["Bagaimana mengurutkan bilangan?", "Cari bilangan terkecil dulu, lalu yang berikutnya, sampai yang terbesar."]]))
    U.append(dict(slug="penjumlahan-dan-pengurangan-sampai-20", dom="B", title="Penjumlahan dan Pengurangan sampai 20", short="Penjumlahan dan Pengurangan sampai 20",
                  std="Peserta didik melakukan operasi penjumlahan dan pengurangan menggunakan benda-benda konkret yang banyaknya sampai 20.",
                  meta="Latihan penjumlahan dan pengurangan sampai 20 untuk kelas 1 SD: lewat sepuluh, garis bilangan, bilangan yang hilang. 100 soal dengan kunci jawaban.",
                  kb="Buat 10 dulu", ks="8 + 5 = 8 + 2 + 3 = 13.",
                  sets=[("Penjumlahan tanpa lewat 10", [(m_fakta("+", 20, False), 20)]), ("Penjumlahan lewat 10", [(m_fakta("+", 20, True), 20)]),
                        ("Pengurangan tanpa lewat 10", [(m_fakta("-", 20, False), 20)]), ("Pengurangan lewat 10", [(m_fakta("-", 20, True), 20)]),
                        ("Bilangan yang hilang", [(m_kosong(20), 14), (m_lompat("+", 20), 3), (m_lompat("-", 20), 3)])],
                  think=["Untuk 8 + 5, lengkapi dulu sampai 10: 8 + 2 = 10, lalu tambah sisanya 3 = 13.", "Untuk 13 − 5, kurangi dulu sampai 10: 13 − 3 = 10, lalu kurangi sisanya 2 = 8.", "Penjumlahan dan pengurangan saling berhubungan: 8 + 5 = 13, jadi 13 − 5 = 8."],
                  ex=[("9 + 4 = …", ["9 + 1 = 10", "10 + 3 = 13"], "13"), ("15 − 7 = …", ["15 − 5 = 10", "10 − 2 = 8"], "8")],
                  mist=[["9 + 4 = 12 (lupa sisa)", "Pecah 4 menjadi 1 dan 3: 10 + 3 = 13"], ["15 − 7 = 12 (7 − 5 = 2)", "Ambil 5 dulu lalu 2: 8"], ["Hanya menjumlah satuan", "Ingat puluhan: 10 + 3 = 13"]],
                  faq=[["Apa itu strategi membuat 10?", "Pecah salah satu bilangan agar yang lain menjadi 10, karena menambah ke 10 lebih mudah."], ["Bagaimana menghitung 14 − 6?", "14 − 4 = 10, lalu 10 − 2 = 8."], ["Apa hubungan penjumlahan dan pengurangan?", "Jika 7 + 6 = 13, maka 13 − 6 = 7 dan 13 − 7 = 6."]]))
    U.append(dict(slug="soal-cerita", dom="B", title="Soal Cerita Penjumlahan dan Pengurangan", short="Soal Cerita",
                  std="Peserta didik menyelesaikan masalah berkaitan dengan penjumlahan dan pengurangan bilangan cacah sampai 20.",
                  meta="Latihan soal cerita untuk kelas 1 SD: menggabungkan, mengambil, dan membandingkan benda sampai 20, dengan gambar. 100 soal dengan kunci jawaban.",
                  kb="Digabung tambah, diambil kurang", ks="Baca ceritanya, lalu pilih + atau −.",
                  sets=[("Cerita menggabungkan", [(m_cerita(10, "+"), 20)]), ("Cerita mengambil", [(m_cerita(10, "-"), 20)]), ("Cerita sampai 20", [(m_cerita(20, "+-"), 20)]),
                        ("Cerita membandingkan", [(m_cerita(20, "="), 20)]), ("Campuran", [(m_cerita(20, "+-="), 10), (m_kotak(20), 10)])],
                  think=["Baca cerita dengan teliti. Apakah benda digabung, diambil, atau dibandingkan?", "Digabung atau datang lagi: tambah. Dimakan, diberikan, pergi: kurang.", "Berapa lebih banyak atau selisih: kurangkan bilangan besar dengan bilangan kecil."],
                  ex=[("Ada 6 burung, datang 5 lagi. Berapa burung?", ["datang lagi = tambah", "6 + 5"], "11 burung"), ("Ada 12 permen, dimakan 4. Sisa?", ["dimakan = kurang", "12 − 4"], "8 permen")],
                  mist=[["Semua soal dijumlahkan", "Kata dimakan, pergi, diberikan berarti kurang"], ["Jawaban tanpa satuan benda", "Tulis bendanya: 8 permen"], ["Selisih dijawab dengan menjumlah", "Selisih = besar − kecil"]],
                  faq=[["Bagaimana tahu harus menambah atau mengurang?", "Jika benda bertambah atau digabung, tambah. Jika berkurang atau diambil, kurang."], ["Apa itu selisih?", "Beda banyak dua kelompok benda."], ["Bagaimana memeriksa jawaban?", "Masukkan jawabanmu kembali ke cerita dan lihat apakah masuk akal."]]))
    U.append(dict(slug="bangun-datar", dom="G", title="Mengenal Bangun Datar", short="Bangun Datar",
                  std="Peserta didik dapat mengenal berbagai bangun datar (segitiga, segiempat, segibanyak, lingkaran).",
                  meta="Latihan bangun datar untuk kelas 1 SD: lingkaran, segitiga, persegi, persegi panjang, sisi dan titik sudut, bentuk benda di sekitar. 100 soal dengan kunci jawaban.",
                  kb="Lingkaran, segitiga, persegi", ks="Hitung sisinya: segitiga punya 3 sisi.",
                  sets=[("Nama bangun datar", [(m_nama_datar(), 20)]), ("Mencari bangun", [(m_cari_datar(), 20)]), ("Sisi dan titik sudut", [(m_sisi(("triangle", "square", "rectangle")), 20)]),
                        ("Menghitung bangun", [(m_hitung_datar(), 20)]), ("Bangun di sekitar kita", [(m_datar_nyata(), 14), (m_nama_datar(), 6)])],
                  think=["Lingkaran bulat dan tidak punya sudut.", "Segitiga punya 3 sisi dan 3 titik sudut.", "Persegi punya 4 sisi sama panjang. Persegi panjang punya 4 sisi, dua panjang dan dua pendek."],
                  ex=[("Berapa sisi segitiga?", ["hitung garis lurus di tepinya"], "3"), ("Bentuk jam dinding?", ["bulat"], "lingkaran")],
                  mist=[["Segitiga yang miring dianggap bukan segitiga", "Diputar pun tetap segitiga"], ["Persegi panjang disebut persegi", "Persegi: 4 sisi sama panjang"], ["Lingkaran dikira punya sudut", "Lingkaran tidak punya sudut"]],
                  faq=[["Apa beda persegi dan persegi panjang?", "Persegi punya 4 sisi sama panjang. Persegi panjang punya 2 sisi panjang dan 2 sisi pendek."], ["Apakah bangun yang diputar berubah nama?", "Tidak. Segitiga yang diputar tetap segitiga."], ["Benda apa yang berbentuk lingkaran?", "Jam dinding, roda, piring, dan uang logam."]]))
    U.append(dict(slug="bangun-ruang", dom="G", title="Mengenal Bangun Ruang", short="Bangun Ruang",
                  std="Peserta didik dapat mengenal berbagai bangun ruang (balok, kubus, kerucut, dan bola).",
                  meta="Latihan bangun ruang untuk kelas 1 SD: bola, kubus, balok, tabung, kerucut, benda di sekitar, dan bangun yang dapat menggelinding. 100 soal dengan kunci jawaban.",
                  kb="Bola, kubus, balok, kerucut", ks="Yang punya sisi lengkung dapat menggelinding.",
                  sets=[("Nama bangun ruang", [(m_ruang(), 20)]), ("Benda di sekitar kita", [(m_ruang_nyata(), 20)]), ("Menggelinding atau tidak", [(m_gelinding(), 6), (m_ruang(), 7), (m_ruang_nyata(), 7)]),
                        ("Bangun datar dan bangun ruang", [(m_nama_datar(), 10), (m_ruang(), 10)]), ("Campuran", [(m_ruang_nyata(), 12), (m_cari_datar(), 8)])],
                  think=["Bangun ruang adalah bangun yang punya isi, bisa dipegang dari segala arah.", "Bola bulat seperti kelereng. Kubus seperti dadu. Balok seperti kotak sepatu. Tabung seperti kaleng. Kerucut seperti topi ulang tahun.", "Bangun dengan sisi lengkung (bola, tabung, kerucut) dapat menggelinding."],
                  ex=[("Bentuk dadu?", ["semua sisinya persegi sama besar"], "kubus"), ("Bentuk kaleng susu?", ["atas dan bawah lingkaran"], "tabung")],
                  mist=[["Kubus dan balok tertukar", "Kubus: semua sisi sama. Balok: ada sisi yang lebih panjang"], ["Bola disebut lingkaran", "Lingkaran bangun datar, bola bangun ruang"], ["Kerucut disebut segitiga", "Kerucut bangun ruang seperti topi"]],
                  faq=[["Apa beda bangun datar dan bangun ruang?", "Bangun datar rata seperti gambar di kertas. Bangun ruang punya isi, seperti bola dan kotak."], ["Bangun ruang apa yang dapat menggelinding?", "Bola, tabung, dan kerucut, karena punya sisi lengkung."], ["Benda apa yang berbentuk balok?", "Kotak sepatu, lemari, dan batu bata."]]))
    U.append(dict(slug="membandingkan-panjang-dan-berat", dom="P", title="Membandingkan Panjang dan Berat", short="Panjang dan Berat",
                  std="Peserta didik dapat membandingkan panjang dan berat benda secara langsung, dan membandingkan durasi waktu.",
                  meta="Latihan membandingkan panjang dan berat untuk kelas 1 SD: lebih panjang, lebih pendek, lebih tinggi, lebih berat, lebih ringan, dan timbangan. 100 soal dengan kunci jawaban.",
                  kb="Panjang, pendek, berat, ringan", ks="Sisi timbangan yang turun lebih berat.",
                  sets=[("Lebih panjang atau pendek", [(m_panjang(), 20)]), ("Lebih tinggi atau rendah", [(m_tinggi(), 20)]), ("Lebih berat atau ringan", [(m_berat(), 20)]),
                        ("Timbangan seimbang", [(m_seimbang(), 20)]), ("Campuran", [(m_panjang(), 7), (m_tinggi(), 7), (m_berat(), 6)])],
                  think=["Untuk membandingkan panjang, sejajarkan ujung benda. Yang ujungnya lebih jauh lebih panjang.", "Pada timbangan, sisi yang lebih berat turun ke bawah.", "Jika timbangan seimbang (datar), kedua sisi sama berat."],
                  ex=[("Pensil A 5 kubus, pensil B 7 kubus. Mana yang lebih panjang?", ["7 lebih dari 5"], "pensil B"), ("Timbangan turun di sisi apel. Mana lebih berat?", ["sisi yang turun lebih berat"], "apel")],
                  mist=[["Ujung benda tidak disejajarkan", "Sejajarkan ujung kiri dulu"], ["Sisi timbangan yang naik dianggap lebih berat", "Yang turun lebih berat"], ["Benda besar selalu lebih berat", "Lihat timbangannya, jangan hanya ukurannya"]],
                  faq=[["Bagaimana membandingkan panjang dua benda?", "Letakkan berdampingan dengan ujung yang sejajar, lalu lihat ujung yang lain."], ["Bagaimana tahu benda mana yang lebih berat?", "Letakkan di timbangan. Sisi yang turun lebih berat."], ["Apa arti timbangan seimbang?", "Kedua sisi sama berat, sehingga timbangan datar."]]))
    U.append(dict(slug="pola-gambar-dan-bilangan", dom="A", title="Pola Gambar dan Pola Bilangan", short="Pola",
                  std="Peserta didik dapat mengenali, meniru, dan melanjutkan pola bukan bilangan (misalnya gambar, warna, dan suara).",
                  meta="Latihan pola untuk kelas 1 SD: pola gambar berulang, pola warna dan bentuk, pola bilangan sederhana. 100 soal dengan kunci jawaban.",
                  kb="Cari bagian yang berulang", ks="Merah, biru, merah, biru, … berikutnya merah.",
                  sets=[("Pola dua gambar", [(m_pola(), 20)]), ("Pola bentuk dan warna", [(m_pola(), 20)]), ("Pola bilangan naik", [(m_pola_bil(20, (1, 2), True), 20)]),
                        ("Pola bilangan turun", [(m_pola_bil(20, (1, 2), False), 20)]), ("Campuran", [(m_pola(), 10), (m_urut(0, 20, (1, 2)), 10)])],
                  think=["Pola adalah susunan yang berulang dengan aturan yang sama.", "Cari bagian yang berulang, lalu ulangi lagi.", "Pada pola bilangan, lihat berapa yang ditambah atau dikurangi setiap langkah."],
                  ex=[("bola, bintang, bola, bintang, …", ["bagian berulang: bola, bintang"], "bola"), ("2, 4, 6, 8, …", ["ditambah 2"], "10")],
                  mist=[["Hanya melihat gambar terakhir", "Lihat bagian yang berulang dari awal"], ["Pola AAB diteruskan ABAB", "Ulangi persis: A, A, B, A, A, B"], ["Pola turun dijawab bertambah", "Perhatikan bilangan makin kecil"]],
                  faq=[["Apa itu pola?", "Susunan benda, warna, bentuk, atau bilangan yang berulang dengan aturan tertentu."], ["Di mana kita melihat pola?", "Pada motif batik, ubin lantai, dan susunan manik-manik."], ["Bagaimana melanjutkan pola bilangan?", "Cari selisih dua bilangan berurutan, lalu tambahkan atau kurangkan selisih itu."]]))
    U.append(dict(slug="posisi-benda", dom="G", title="Posisi Benda", short="Posisi Benda",
                  std="Peserta didik dapat menentukan posisi benda terhadap benda lain (kanan, kiri, depan, belakang, atas, bawah).",
                  meta="Latihan posisi benda untuk kelas 1 SD: di atas, di bawah, di samping, di depan, di belakang, kanan dan kiri, urutan ke berapa. 100 soal dengan kunci jawaban.",
                  kb="Atas, bawah, depan, belakang", ks="Kanan dan kiri dilihat dari kita.",
                  sets=[("Atas, bawah, samping", [(m_meja(), 20)]), ("Depan dan belakang", [(m_kardus(), 20)]), ("Rak buku", [(m_rak(), 20)]),
                        ("Kanan dan kiri", [(m_kanan_kiri(), 20)]), ("Campuran", [(m_meja(), 6), (m_kardus(), 7), (m_kanan_kiri(), 7)])],
                  think=["Posisi benda dilihat dari benda lain: di atas meja, di bawah meja, di samping kardus.", "Benda yang sebagian tertutup ada di belakang.", "Kanan dan kiri dilihat dari arah kita melihat gambar."],
                  ex=[("Bola ada di bawah meja. Di mana bola?", ["bola lebih rendah dari meja"], "di bawah meja"), ("Deretan: apel, ikan, bunga. Sebelah kanan ikan?", ["lihat ke kanan ikan"], "bunga")],
                  mist=[["Kanan dan kiri tertukar", "Tangan yang dipakai menulis biasanya tangan kanan"], ["Benda di belakang dianggap di depan", "Benda di belakang sebagian tertutup"], ["Urutan dihitung dari arah yang salah", "Baca soal: dari kiri atau dari kanan"]],
                  faq=[["Bagaimana menentukan kanan dan kiri pada gambar?", "Lihat dari posisi kita yang melihat gambar."], ["Apa arti di belakang?", "Benda berada di sisi yang jauh dan sebagian tertutup oleh benda lain."], ["Apa arti benda ke-3 dari kiri?", "Hitung dari ujung kiri: satu, dua, tiga."]]))
    U.append(dict(slug="turus-dan-piktogram", dom="D", title="Data dengan Turus dan Piktogram", short="Turus dan Piktogram",
                  std="Peserta didik dapat mengurutkan, menyortir, mengelompokkan, membandingkan, dan menyajikan data dari banyak benda dengan menggunakan turus dan piktogram paling banyak 4 kategori.",
                  meta="Latihan data untuk kelas 1 SD: membaca turus, tabel turus, piktogram, paling banyak dan paling sedikit, selisih. 100 soal dengan kunci jawaban.",
                  kb="Satu ikatan turus = 5", ks="Pada piktogram, hitung gambarnya.",
                  sets=[("Membaca turus", [(m_turus(15), 20)]), ("Tabel turus", [(m_data(10, "turus"), 20)]), ("Piktogram", [(m_data(8, "pikto", (0, 1)), 20)]),
                        ("Membandingkan data", [(m_data(8, "pikto", (1, 2)), 20)]), ("Campuran", [(m_data(10, "turus", (2, 3)), 10), (m_data(8, "pikto", (3,)), 10)])],
                  think=["Turus adalah garis untuk mencatat. Setiap garis = 1. Garis kelima dibuat miring dan mengikat 4 garis, jadi satu ikatan = 5.", "Piktogram memakai gambar. Pada latihan ini, 1 gambar = 1.", "Untuk membandingkan data, cari yang paling banyak, paling sedikit, atau hitung selisihnya."],
                  ex=[("Satu ikatan dan 2 garis turus = …", ["5 + 2"], "7"), ("Jeruk 6 gambar, apel 4 gambar. Selisih?", ["6 − 4"], "2")],
                  mist=[["Ikatan turus dihitung 4", "Ikatan = 4 garis + 1 garis miring = 5"], ["Gambar yang besar dihitung lebih", "Setiap gambar bernilai sama"], ["Paling sedikit dijawab yang paling banyak", "Baca soal dengan teliti"]],
                  faq=[["Apa itu turus?", "Garis-garis untuk mencatat data. Setiap lima garis diikat menjadi satu kelompok."], ["Apa itu piktogram?", "Penyajian data dengan gambar. Setiap gambar mewakili sejumlah benda."], ["Kenapa turus diikat lima-lima?", "Agar lebih mudah dan cepat dihitung."]]))
    return U


# ============================================================ Kelas 2
def K2():
    import id_k4c as C
    import id_k4
    d15 = id_k4.UNITS[14]()
    d16 = id_k4.UNITS[15]()
    nama_segi, hitung_sisi = maker_of(d15, "nama_segi"), maker_of(d15, "hitung")
    urai, susun, cara, berapa = (maker_of(d16, x) for x in ("urai", "susun", "cara", "berapa"))

    def small(mk, mx=20):
        def g():
            it = mk()
            if it is None:
                return None
            t = re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
            if any(int(x) > mx for x in re.findall(r"\d+", t)):
                return None
            return it
        return named(g, mk.__name__)
    berapa = small(berapa)
    U = []
    U.append(dict(slug="bilangan-sampai-100", dom="B", title="Bilangan sampai 100", short="Bilangan sampai 100",
                  std="Peserta didik menunjukkan pemahaman dan memiliki intuisi bilangan (number sense) pada bilangan cacah sampai 100: membaca, menulis, dan membilang.",
                  meta="Latihan bilangan sampai 100 untuk kelas 2 SD: membaca dan menulis bilangan, batang puluhan, sebelum dan sesudah, 10 lebih dan 10 kurang. 100 soal dengan kunci jawaban.",
                  kb="Puluhan dulu, lalu satuan", ks="47 dibaca empat puluh tujuh.",
                  sets=[("Membaca bilangan", [(m_kata(21, 99), 20)]), ("Batang puluhan", [(m_batang(21, 99), 20)]), ("Sebelum dan sesudah", [(m_sesudah(20, 99), 20)]),
                        ("10 lebih dan 10 kurang", [(m_sesudah(20, 90, (10,)), 20)]), ("Bilangan yang hilang", [(m_urut(20, 100), 20)])],
                  think=["Bilangan dua angka terdiri dari puluhan dan satuan. 47 = 4 puluhan dan 7 satuan.", "Baca puluhan dulu: 40 = empat puluh, lalu satuan: tujuh. Jadi empat puluh tujuh.", "10 lebih berarti angka puluhan bertambah 1: 10 lebih dari 47 adalah 57."],
                  ex=[("Bacalah 62.", ["6 puluhan → enam puluh", "2 satuan → dua"], "enam puluh dua"), ("10 lebih dari 38?", ["puluhan 3 menjadi 4"], "48")],
                  mist=[["47 ditulis 407", "4 puluhan dan 7 satuan: 47"], ["Sesudah 59 ditulis 510", "Sesudah 59 adalah 60"], ["10 lebih dari 38 dijawab 39", "Tambah 10, bukan 1: 48"]],
                  faq=[["Bagaimana membaca 35?", "Tiga puluh lima: 3 puluhan dibaca tiga puluh, 5 satuan dibaca lima."], ["Apa bilangan sesudah 99?", "Sesudah 99 adalah 100 (seratus)."], ["Apa arti 10 lebih dari?", "Tambahkan 10. Angka puluhan bertambah 1, angka satuan tetap."]]))
    U.append(dict(slug="puluhan-dan-satuan", dom="B", title="Nilai Tempat Puluhan dan Satuan", short="Puluhan dan Satuan",
                  std="Peserta didik dapat menentukan nilai tempat, melakukan komposisi (menyusun) dan dekomposisi (mengurai) bilangan cacah sampai 100.",
                  meta="Latihan nilai tempat untuk kelas 2 SD: puluhan dan satuan, nilai angka, bentuk panjang, tabel nilai tempat, menyusun dan mengurai bilangan. 100 soal dengan kunci jawaban.",
                  kb="58 = 50 + 8", ks="Angka di kiri adalah puluhan.",
                  sets=[("Batang dan kubus", [(m_batang(11, 99), 20)]), ("Nilai angka", [(m_puluhan((0,)), 20)]), ("Bentuk panjang", [(m_puluhan((1, 2)), 20)]),
                        ("Tabel nilai tempat", [(m_puluhan((3,)), 20)]), ("Campuran", [(m_batang(11, 99), 10), (m_puluhan(), 10)])],
                  think=["Pada bilangan dua angka, angka kiri adalah puluhan dan angka kanan adalah satuan.", "Nilai angka puluhan = angka × 10. Pada 58, angka 5 bernilai 50.", "Bentuk panjang menuliskan nilai setiap angka: 58 = 50 + 8."],
                  ex=[("Nilai angka 7 pada 73?", ["7 di tempat puluhan"], "70"), ("6 puluhan + 4 satuan = …", ["60 + 4"], "64")],
                  mist=[["Nilai angka 7 pada 73 adalah 7", "7 di puluhan, nilainya 70"], ["Bentuk panjang 64 ditulis 6 + 4", "64 = 60 + 4"], ["Puluhan dan satuan tertukar", "Puluhan ditulis di kiri"]],
                  faq=[["Apa itu nilai tempat?", "Nilai angka menurut posisinya. Angka 3 di puluhan bernilai 30, di satuan bernilai 3."], ["Berapa satuan dalam 1 puluhan?", "1 puluhan = 10 satuan."], ["Apa itu bentuk panjang?", "Penjumlahan nilai setiap angka, misalnya 82 = 80 + 2."]]))
    U.append(dict(slug="membandingkan-dan-mengurutkan-bilangan", dom="B", title="Membandingkan dan Mengurutkan Bilangan sampai 100", short="Membandingkan dan Mengurutkan Bilangan",
                  std="Peserta didik dapat membandingkan dan mengurutkan bilangan cacah sampai 100.",
                  meta="Latihan membandingkan bilangan sampai 100 untuk kelas 2 SD: tanda <, > dan =, terbesar dan terkecil, mengurutkan bilangan. 100 soal dengan kunci jawaban.",
                  kb="Bandingkan puluhan dulu", ks="Jika puluhan sama, bandingkan satuan.",
                  sets=[("Tanda &lt;, &gt;, dan =", [(m_banding(10, 99), 20)]), ("Puluhan sama", [(named(lambda: (lambda t, a, c: stmt(str(t * 10 + a), str(t * 10 + c), a, c, "Puluhan sama, bandingkan satuan: %d %s %d." % (a, rel(a, c), c)) if a != c else None)(ri(1, 9), ri(0, 9), ri(0, 9)), "banding2"), 20)]),
                        ("Terbesar dan terkecil", [(m_ekstrem(10, 99), 20)]), ("Mengurutkan", [(m_urutkan(10, 99), 20)]), ("Campuran", [(m_banding(10, 99), 7), (m_ekstrem(10, 99), 7), (m_urutkan(10, 99), 6)])],
                  think=["Untuk membandingkan bilangan dua angka, bandingkan angka puluhan dulu.", "Jika puluhannya sama, bandingkan angka satuan.", "Tanda &lt; artinya kurang dari, &gt; artinya lebih dari."],
                  ex=[("Bandingkan 64 dan 46.", ["puluhan: 6 &gt; 4"], "64 &gt; 46"), ("Bandingkan 38 dan 35.", ["puluhan sama, satuan 8 &gt; 5"], "38 &gt; 35")],
                  mist=[["46 &gt; 64 karena 6 &gt; 4 di satuan", "Bandingkan puluhan dulu"], ["Arah tanda terbalik", "Mulut tanda terbuka ke bilangan yang lebih besar"], ["Urutan tertukar", "Baca: dari terkecil atau terbesar"]],
                  faq=[["Bagaimana membandingkan 52 dan 25?", "Puluhan 5 lebih besar dari 2, jadi 52 > 25."], ["Bagaimana jika puluhannya sama?", "Bandingkan satuannya. 73 > 71 karena 3 > 1."], ["Apa arti urutan naik?", "Dari bilangan terkecil ke terbesar."]]))
    U.append(dict(slug="lompat-hitung-dan-bilangan-genap-ganjil", dom="A", title="Lompat Hitung, Bilangan Genap dan Ganjil", short="Lompat Hitung, Genap, dan Ganjil",
                  std="Peserta didik dapat mengenali, meniru, dan melanjutkan pola bilangan, termasuk membilang loncat 2, 5, dan 10.",
                  meta="Latihan lompat hitung untuk kelas 2 SD: membilang loncat 2, 5, dan 10, pola bilangan, bilangan genap dan ganjil. 100 soal dengan kunci jawaban.",
                  kb="Lompat 2, 5, dan 10", ks="Bilangan genap berakhiran 0, 2, 4, 6, 8.",
                  sets=[("Lompat 2", [(m_urut(0, 100, (2,)), 20)]), ("Lompat 5", [(m_urut(0, 100, (5,)), 20)]), ("Lompat 10", [(m_urut(0, 100, (10,)), 10), (m_pola_bil(100, (10,)), 10)]),
                        ("Pola bilangan", [(m_pola_bil(100, (2, 5, 10)), 20)]), ("Genap dan ganjil", [(m_genap(), 20)])],
                  think=["Lompat 2: 2, 4, 6, 8, … Lompat 5: 5, 10, 15, 20, … Lompat 10: 10, 20, 30, …", "Bilangan genap dapat dibagi menjadi pasangan tanpa sisa. Angka satuannya 0, 2, 4, 6, atau 8.", "Bilangan ganjil selalu sisa satu jika dipasangkan. Angka satuannya 1, 3, 5, 7, atau 9."],
                  ex=[("35, 40, 45, …", ["lompat 5"], "50"), ("Apakah 27 genap?", ["angka satuan 7"], "ganjil")],
                  mist=[["Lompat 5 ditulis 5, 10, 14", "Setiap lompatan tambah 5: 15"], ["30 dianggap ganjil karena ada 3", "Lihat angka satuan: 0, jadi genap"], ["Lompat 10 hanya menambah satuan", "Lompat 10: angka puluhan bertambah 1"]],
                  faq=[["Apa itu lompat hitung?", "Membilang dengan melewati beberapa bilangan, misalnya 2, 4, 6, 8."], ["Bagaimana tahu bilangan genap?", "Lihat angka satuannya. Jika 0, 2, 4, 6, atau 8, bilangan itu genap."], ["Apakah 0 genap?", "Ya, 0 termasuk bilangan genap."]]))
    U.append(dict(slug="penjumlahan-dan-pengurangan-sampai-20", dom="B", title="Penjumlahan dan Pengurangan sampai 20", short="Penjumlahan dan Pengurangan sampai 20",
                  std="Peserta didik dapat melakukan operasi penjumlahan dan pengurangan menggunakan benda-benda konkret yang banyaknya sampai 20.",
                  meta="Latihan penjumlahan dan pengurangan sampai 20 untuk kelas 2 SD: fakta dasar, lewat sepuluh, pasangan bilangan, bilangan yang hilang. 100 soal dengan kunci jawaban.",
                  kb="Buat 10 dulu", ks="7 + 6 = 7 + 3 + 3 = 13.",
                  sets=[("Penjumlahan lewat 10", [(m_fakta("+", 20, True), 20)]), ("Pengurangan lewat 10", [(m_fakta("-", 20, True), 20)]),
                        ("Pasangan bilangan", [(m_ikatan(20), 20)]), ("Bilangan yang hilang", [(m_kosong(20), 20)]), ("Campuran", [(m_fakta("+", 20), 10), (m_fakta("-", 20), 10)])],
                  think=["Ingat pasangan 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5.", "Untuk 7 + 6, buat 10 dulu: 7 + 3 = 10, sisa 3, jadi 13.", "Untuk 13 − 6, kurangi sampai 10 dulu: 13 − 3 = 10, lalu 10 − 3 = 7."],
                  ex=[("8 + 7 = …", ["8 + 2 = 10", "10 + 5"], "15"), ("16 − 9 = …", ["16 − 6 = 10", "10 − 3"], "7")],
                  mist=[["8 + 7 = 14", "8 + 2 + 5 = 15"], ["16 − 9 = 13", "16 − 6 − 3 = 7"], ["Bilangan yang hilang dijawab dengan menjumlah", "8 + … = 15, jadi … = 15 − 8 = 7"]],
                  faq=[["Kenapa perlu hafal pasangan 10?", "Pasangan 10 membantu menjumlah dan mengurang lewat sepuluh dengan cepat."], ["Bagaimana mencari bilangan yang hilang?", "Gunakan kebalikannya. Untuk 6 + … = 14, hitung 14 − 6 = 8."], ["Apa itu keluarga bilangan?", "Tiga bilangan yang saling berhubungan, misalnya 6 + 8 = 14, 8 + 6 = 14, 14 − 6 = 8, 14 − 8 = 6."]]))
    U.append(dict(slug="kesamaan-dan-tanda-sama-dengan", dom="A", title="Kesamaan dan Tanda Sama Dengan", short="Kesamaan",
                  std="Peserta didik dapat menunjukkan pemahaman makna simbol matematika “=” dalam suatu kalimat matematika yang terkait dengan penjumlahan dan pengurangan bilangan cacah sampai 20.",
                  meta="Latihan kesamaan untuk kelas 2 SD: arti tanda sama dengan, kalimat matematika yang setara, benar atau salah, timbangan seimbang. 100 soal dengan kunci jawaban.",
                  kb="= berarti sama nilainya", ks="6 + 4 = 7 + 3, keduanya 10.",
                  sets=[("Melengkapi kesamaan", [(m_kesamaan(20), 20)]), ("Timbangan seimbang", [(m_timb_bil(20), 20)]), ("Benar atau salah", [(m_kesamaan(20), 20)]),
                        ("Bilangan yang hilang", [(m_kosong(20), 20)]), ("Campuran", [(m_kesamaan(20), 10), (m_timb_bil(20), 10)])],
                  think=["Tanda = berarti nilai di sebelah kiri sama dengan nilai di sebelah kanan.", "Tanda = bukan hanya untuk menulis hasil. 5 + 3 = 4 + 4 juga benar.", "Seperti timbangan seimbang: kedua sisi harus sama berat."],
                  ex=[("6 + 4 = 7 + …", ["6 + 4 = 10", "7 + 3 = 10"], "3"), ("Benar atau salah: 9 + 2 = 6 + 5", ["kiri 11, kanan 11"], "benar")],
                  mist=[["6 + 4 = 7 + … dijawab 10", "Kanan juga harus 10: 7 + 3"], ["Tanda = dianggap “hasilnya”", "= artinya kedua sisi sama nilainya"], ["Hanya menghitung sisi kiri", "Hitung kedua sisi lalu bandingkan"]],
                  faq=[["Apa arti tanda sama dengan?", "Nilai di kedua sisi tanda = sama besar."], ["Apakah 3 + 5 = 8 + 0 benar?", "Benar, kedua sisi bernilai 8."], ["Bagaimana melengkapi 5 + 7 = 4 + …?", "Kiri bernilai 12. Bilangan yang ditambah 4 menjadi 12 adalah 8."]]))
    U.append(dict(slug="soal-cerita", dom="B", title="Soal Cerita Penjumlahan dan Pengurangan", short="Soal Cerita",
                  std="Peserta didik dapat menyelesaikan masalah berkaitan dengan penjumlahan dan pengurangan bilangan cacah sampai 20.",
                  meta="Latihan soal cerita untuk kelas 2 SD: menggabungkan, mengambil, membandingkan, dan benda tersembunyi sampai 20. 100 soal dengan kunci jawaban.",
                  kb="Digabung tambah, diambil kurang", ks="Selisih = bilangan besar − bilangan kecil.",
                  sets=[("Cerita menggabungkan", [(m_cerita(20, "+"), 20)]), ("Cerita mengambil", [(m_cerita(20, "-"), 20)]), ("Cerita membandingkan", [(m_cerita(20, "="), 20)]),
                        ("Benda tersembunyi", [(m_kotak(20), 20)]), ("Campuran", [(m_cerita(20, "+-="), 20)])],
                  think=["Baca cerita, lalu tentukan: digabung (tambah), diambil (kurang), atau dibandingkan (selisih).", "Tulis kalimat matematikanya dulu, baru hitung.", "Tulis jawaban dengan nama bendanya."],
                  ex=[("Ada 9 ayam dan 6 bebek. Berapa lebih banyak ayam?", ["9 − 6"], "3 ekor"), ("Siti punya 8 stiker, dapat 7 lagi.", ["8 + 7"], "15 stiker")],
                  mist=[["Lebih banyak berapa dijawab dengan menjumlah", "Lebih banyak berapa = selisih: kurang"], ["Jawaban tanpa nama benda", "Tulis: 15 stiker"], ["Tidak membaca soal sampai akhir", "Baca pertanyaannya dengan teliti"]],
                  faq=[["Bagaimana mengerjakan soal cerita?", "Baca cerita, cari bilangannya, tentukan tambah atau kurang, hitung, lalu periksa."], ["Kata apa yang berarti mengurang?", "Dimakan, diberikan, pergi, meletus, terjual, tersisa."], ["Apa arti berapa lebih banyak?", "Mencari selisih: bilangan besar dikurangi bilangan kecil."]]))
    U.append(dict(slug="setengah-dan-seperempat", dom="B", title="Pecahan Setengah dan Seperempat", short="Setengah dan Seperempat",
                  std="Peserta didik dapat menunjukkan pemahaman pecahan sebagai bagian dari keseluruhan melalui konteks membagi sebuah benda atau kumpulan benda sama banyak (setengah dan seperempat).",
                  meta="Latihan pecahan setengah dan seperempat untuk kelas 2 SD: bagian yang diarsir, membagi benda sama besar, setengah dan seperempat dari kumpulan benda. 100 soal dengan kunci jawaban.",
                  kb="Setengah = 1 dari 2 bagian sama", ks="Seperempat = 1 dari 4 bagian sama.",
                  sets=[("Bagian yang diarsir", [(m_pecahan_gambar(), 20)]), ("Membagi benda", [(m_pecahan_kata(), 10), (m_pecahan_gambar(), 10)]),
                        ("Setengah dari kumpulan", [(m_pecahan_benda((2,)), 20)]), ("Seperempat dari kumpulan", [(m_pecahan_benda((4,)), 20)]),
                        ("Campuran", [(m_pecahan_gambar(), 10), (m_pecahan_benda(), 10)])],
                  think=["Setengah berarti satu benda dibagi menjadi 2 bagian yang sama besar, lalu diambil 1 bagian.", "Seperempat berarti dibagi menjadi 4 bagian yang sama besar, lalu diambil 1 bagian.", "Setengah dari 8 apel = 8 dibagi 2 sama banyak = 4 apel."],
                  ex=[("Setengah dari 10 kelereng?", ["bagi 2 kelompok sama banyak"], "5 kelereng"), ("Seperempat dari 12 kue?", ["bagi 4 kelompok sama banyak"], "3 kue")],
                  mist=[["Bagian tidak sama besar disebut setengah", "Setengah harus sama besar"], ["Seperempat lebih besar dari setengah", "Makin banyak potongan, makin kecil: setengah lebih besar"], ["Setengah dari 8 dijawab 2", "8 dibagi 2 = 4"]],
                  faq=[["Apa itu setengah?", "Satu dari dua bagian yang sama besar."], ["Apa itu seperempat?", "Satu dari empat bagian yang sama besar."], ["Berapa seperempat yang sama dengan setengah?", "Dua seperempat sama dengan setengah."]]))
    U.append(dict(slug="mengukur-dengan-satuan-tidak-baku", dom="P", title="Mengukur Panjang dan Berat dengan Satuan Tidak Baku", short="Satuan Tidak Baku",
                  std="Peserta didik dapat mengukur dan mengestimasi panjang dan berat benda menggunakan satuan tidak baku.",
                  meta="Latihan mengukur dengan satuan tidak baku untuk kelas 2 SD: mengukur dengan kubus, jengkal, dan langkah, membandingkan panjang dan berat dengan timbangan. 100 soal dengan kunci jawaban.",
                  kb="Hitung berapa kali satuannya", ks="Satuan tidak baku: jengkal, langkah, kubus.",
                  sets=[("Mengukur dengan kubus", [(m_tinggi(), 20)]), ("Membandingkan panjang", [(m_panjang(), 20)]), ("Mengukur berat dengan kubus", [(m_seimbang(), 20)]),
                        ("Lebih berat atau ringan", [(m_berat(), 20)]), ("Jengkal dan langkah", [(m_ukur_nb(), 20)])],
                  think=["Satuan tidak baku adalah benda yang dipakai untuk mengukur, misalnya kubus, klip kertas, jengkal, atau langkah.", "Hitung berapa kali satuan itu dipakai sampai ujung benda.", "Hasil bisa berbeda jika ukuran satuannya berbeda, misalnya jengkal tangan ayah dan jengkal tangan adik."],
                  ex=[("Menara A terdiri dari 6 kubus. Tingginya?", ["hitung kubus"], "6 kubus"), ("1 apel seimbang dengan 4 kubus.", ["timbangan datar"], "1 apel seberat 4 kubus")],
                  mist=[["Satuan dipasang dengan celah", "Pasang satuan rapat tanpa celah"], ["Jengkal ayah dan adik dianggap sama", "Ukuran jengkal tiap orang berbeda"], ["Timbangan miring dianggap seimbang", "Seimbang berarti datar"]],
                  faq=[["Apa itu satuan tidak baku?", "Ukuran dari benda sehari-hari seperti jengkal, langkah, atau kubus yang ukurannya bisa berbeda-beda."], ["Kenapa hasil mengukur bisa berbeda?", "Karena ukuran satuannya tidak sama, misalnya langkah orang dewasa lebih panjang dari langkah anak."], ["Bagaimana mengukur berat tanpa angka?", "Bandingkan dengan timbangan, atau hitung berapa kubus yang seimbang dengan benda itu."]]))
    U.append(dict(slug="bangun-datar-dan-bangun-ruang", dom="G", title="Bangun Datar dan Bangun Ruang", short="Bangun Datar dan Bangun Ruang",
                  std="Peserta didik dapat mengenal berbagai bangun datar (segitiga, segiempat, segibanyak, lingkaran) dan bangun ruang (balok, kubus, kerucut, dan bola).",
                  meta="Latihan bangun datar dan bangun ruang untuk kelas 2 SD: segitiga, segi empat, segi banyak, lingkaran, sisi dan titik sudut, balok, kubus, kerucut, bola, tabung. 100 soal dengan kunci jawaban.",
                  kb="Hitung sisi dan titik sudut", ks="Segi enam punya 6 sisi dan 6 titik sudut.",
                  sets=[("Nama bangun datar", [(nama_segi, 14), (m_nama_datar(tuple(SHAPE)), 6)]), ("Sisi dan titik sudut", [(hitung_sisi, 14), (m_sisi(), 6)]),
                        ("Nama bangun ruang", [(m_ruang(), 20)]), ("Benda di sekitar kita", [(m_ruang_nyata(), 12), (m_datar_nyata(), 8)]), ("Campuran", [(m_gelinding(), 6), (m_hitung_datar(), 14)])],
                  think=["Bangun datar diberi nama menurut banyak sisinya: segitiga (3), segi empat (4), segi lima (5), segi enam (6).", "Lingkaran tidak punya sisi lurus dan titik sudut.", "Bangun ruang: bola, kubus, balok, tabung, kerucut. Bangun dengan sisi lengkung dapat menggelinding."],
                  ex=[("Bangun dengan 5 sisi?", ["5 sisi"], "segi lima"), ("Bentuk tumpeng?", ["seperti topi ulang tahun"], "kerucut")],
                  mist=[["Titik sudut dihitung dua kali", "Beri tanda setiap titik yang sudah dihitung"], ["Kubus disebut persegi", "Persegi bangun datar, kubus bangun ruang"], ["Bangun miring dianggap berbeda", "Nama bangun tidak berubah jika diputar"]],
                  faq=[["Bagaimana menamai bangun datar?", "Hitung sisinya. Bangun dengan 6 sisi disebut segi enam."], ["Apa beda kubus dan balok?", "Semua sisi kubus persegi yang sama besar. Balok punya sisi persegi panjang."], ["Bangun ruang apa yang dapat menggelinding?", "Bola, tabung, dan kerucut."]]))
    U.append(dict(slug="menyusun-dan-mengurai-bangun-datar", dom="G", title="Menyusun dan Mengurai Bangun Datar", short="Menyusun dan Mengurai Bangun Datar",
                  std="Peserta didik dapat menyusun (komposisi) dan mengurai (dekomposisi) suatu bangun datar (segitiga, segiempat, dan segibanyak).",
                  meta="Latihan menyusun dan mengurai bangun datar untuk kelas 2 SD: memecah bangun menjadi bagian, menyusun kepingan, menghitung kepingan. 100 soal dengan kunci jawaban.",
                  kb="Bangun bisa dipecah dan disusun", ks="2 segitiga dapat menjadi 1 persegi.",
                  sets=[("Mengurai bangun", [(urai, 20)]), ("Menyusun bangun", [(susun, 14), (cara, 6)]), ("Berapa kepingan?", [(berapa, 12), (m_hitung_datar(), 8)]),
                        ("Campuran", [(urai, 10), (susun, 10)]), ("Bangun di sekitar kita", [(m_datar_nyata(), 10), (m_hitung_datar(), 10)])],
                  think=["Bangun datar dapat dipecah (diurai) menjadi bangun yang lebih kecil, misalnya persegi menjadi 2 segitiga.", "Beberapa bangun kecil dapat disusun menjadi bangun yang lebih besar.", "Perhatikan garis putus-putus: itu tempat bangun dipotong."],
                  ex=[("Persegi dipotong pada diagonalnya.", ["menjadi 2 bagian"], "2 segitiga"), ("2 persegi berdampingan.", ["menjadi bangun panjang"], "persegi panjang")],
                  mist=[["Garis potong dihitung sebagai keping", "Hitung bagiannya, bukan garisnya"], ["Kepingan yang diputar dianggap berbeda", "Diputar tetap bangun yang sama"], ["Lupa kepingan kecil di pojok", "Hitung semua bagian"]],
                  faq=[["Apa itu mengurai bangun datar?", "Memecah bangun menjadi beberapa bangun yang lebih kecil."], ["Apa itu menyusun bangun datar?", "Menggabungkan beberapa bangun kecil menjadi bangun yang lebih besar."], ["Bangun apa yang terbentuk dari 2 segitiga?", "Bisa persegi, persegi panjang, atau segitiga yang lebih besar, tergantung cara menyusunnya."]]))
    U.append(dict(slug="pola", dom="A", title="Pola Gambar dan Pola Bilangan", short="Pola",
                  std="Peserta didik dapat mengenali, meniru, dan melanjutkan pola bukan bilangan dan pola bilangan sederhana.",
                  meta="Latihan pola untuk kelas 2 SD: pola gambar berulang, pola bentuk dan warna, pola bilangan naik dan turun sampai 100. 100 soal dengan kunci jawaban.",
                  kb="Cari bagian yang berulang", ks="Pada pola bilangan, cari berapa yang ditambah.",
                  sets=[("Pola gambar", [(m_pola(), 20)]), ("Pola bentuk dan warna", [(m_pola(), 20)]), ("Pola bilangan naik dan turun", [(m_pola_bil(100, (2, 3, 5, 10)), 20)]),
                        ("Bilangan yang hilang", [(m_urut(0, 100, (2, 3, 5, 10)), 20)]), ("Campuran", [(m_pola(), 10), (m_pola_bil(100, (2, 5, 10)), 10)])],
                  think=["Pola gambar punya bagian yang berulang. Cari bagian itu, lalu ulangi.", "Pola bilangan bertambah atau berkurang dengan aturan yang sama.", "Periksa aturannya pada semua bilangan, bukan hanya dua bilangan pertama."],
                  ex=[("segitiga, lingkaran, lingkaran, segitiga, lingkaran, lingkaran, …", ["bagian berulang: segitiga, lingkaran, lingkaran"], "segitiga"), ("15, 18, 21, …", ["ditambah 3"], "24")],
                  mist=[["Pola ABB diteruskan AB", "Ulangi bagian lengkapnya: A, B, B"], ["Hanya melihat dua bilangan terakhir", "Periksa aturan pada semua bilangan"], ["Pola turun diteruskan naik", "Lihat apakah bilangan makin besar atau makin kecil"]],
                  faq=[["Apa itu pola berulang?", "Susunan yang bagian-bagiannya terus diulang, misalnya merah, biru, merah, biru."], ["Bagaimana mencari aturan pola bilangan?", "Kurangkan dua bilangan berurutan untuk melihat berapa yang ditambah atau dikurangi."], ["Apakah pola ada di sekitar kita?", "Ada, misalnya motif kain, ubin lantai, dan nomor rumah."]]))
    U.append(dict(slug="turus-dan-piktogram", dom="D", title="Mengumpulkan dan Menyajikan Data", short="Turus dan Piktogram",
                  std="Peserta didik dapat mengurutkan, menyortir, mengelompokkan, membandingkan, dan menyajikan data dari banyak benda dengan menggunakan turus dan piktogram paling banyak 4 kategori.",
                  meta="Latihan data untuk kelas 2 SD: turus sampai 20, tabel turus, piktogram, paling banyak, selisih, dan jumlah data. 100 soal dengan kunci jawaban.",
                  kb="Turus diikat lima-lima", ks="Bandingkan data: paling banyak, selisih, jumlah.",
                  sets=[("Membaca turus", [(m_turus(20), 20)]), ("Tabel turus", [(m_data(15, "turus"), 20)]), ("Piktogram", [(m_data(10, "pikto"), 20)]),
                        ("Selisih dan jumlah", [(m_data(10, "pikto", (2, 3)), 20)]), ("Campuran", [(m_data(15, "turus", (1, 2, 3)), 20)])],
                  think=["Data dikumpulkan dengan turus: setiap data satu garis, setiap lima garis diikat.", "Data dapat disajikan dengan piktogram: setiap gambar mewakili 1 benda.", "Dari data, kita bisa mencari yang paling banyak, paling sedikit, selisih, dan jumlahnya."],
                  ex=[("Tiga ikatan turus = …", ["5 + 5 + 5"], "15"), ("Kucing 9, ikan 5. Selisih?", ["9 − 5"], "4")],
                  mist=[["Ikatan turus dihitung 4", "Satu ikatan = 5"], ["Jumlah dan selisih tertukar", "Jumlah: tambah. Selisih: kurang"], ["Menjawab dengan nama yang salah baris", "Lihat baris yang sesuai dengan namanya"]],
                  faq=[["Bagaimana mencatat data dengan turus?", "Buat satu garis untuk setiap data. Garis kelima dibuat miring mengikat empat garis sebelumnya."], ["Apa gunanya piktogram?", "Agar data mudah dibaca dan dibandingkan dengan melihat gambarnya."], ["Berapa kategori data di kelas 2?", "Paling banyak 4 kategori, misalnya 4 jenis buah kesukaan."]]))
    return U


# ------------------------------------------------------------
def build(lv, i):
    rnd = random.Random(40000 + 100 * lv + i)
    A.setup(rnd)
    U = (K1 if lv == 1 else K2)()
    d = U[i - 1]
    body = lesson(d["think"], [example(q, s, a) for q, s, a in d["ex"]], d["mist"])
    faq = [{"q": q, "a": a} for q, a in d["faq"]]
    seen = set()
    sets = [(t, mix(rnd, seen, parts)) for t, parts in d["sets"]]
    make_unit(rnd, d["slug"], d["dom"], d["std"] + " (Capaian Pembelajaran Fase A)", d["title"], d["short"], d["meta"], d["kb"], d["ks"],
              body, faq, sets, i, grade="kelas-%d" % lv, fase="Fase A")
    return d["slug"]


if __name__ == "__main__":
    lv = int(sys.argv[1])
    want = sys.argv[2:]
    n = 13
    for i in range(1, n + 1):
        if want and str(i) not in want:
            continue
        print(i, build(lv, i), flush=True)
