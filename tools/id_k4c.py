# -*- coding: utf-8 -*-
"""Indonesia Kelas 4 (Fase B): geometri dan data（15〜17）。"""
import math
import id_k4a as A
from id_k4a import ri, ch, pool
from id_common import (num, mcq, lesson, example, table, wrap, diagram_batang, text, line, INK, GREEN, FILL, RED, BLUE)
from de_common import strichliste


def R():
    return A.R


def K():
    return A.K


def poly_svg(pts, label, col="#cfe6d6", pad=12, dashed=(), lg=False):
    xs = [p[0] for p in pts] + [q[0] for d in dashed for q in d]
    ys = [p[1] for p in pts] + [q[1] for d in dashed for q in d]
    x0, y0 = min(xs), min(ys)
    s = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2' stroke-linejoin='round'/>" % (
        " ".join("%.1f,%.1f" % (x - x0 + pad, y - y0 + pad) for x, y in pts), col, INK)
    for (a, b) in dashed:
        s += line(a[0] - x0 + pad, a[1] - y0 + pad, b[0] - x0 + pad, b[1] - y0 + pad, INK, 1.6, " stroke-dasharray='5 4'")
    return wrap(max(xs) - x0 + 2 * pad, max(ys) - y0 + 2 * pad, s, label, lg=lg)


def regular(n, r, rot=None, jitter=0.0):
    rot = -math.pi / 2 if rot is None else rot
    pts = []
    for i in range(n):
        a = rot + 2 * math.pi * i / n + (R().uniform(-jitter, jitter) if jitter else 0)
        rr = r * (R().uniform(0.75, 1.0) if jitter else 1)
        pts.append((r + 10 + rr * math.cos(a), r + 10 + rr * math.sin(a)))
    return pts


# ------------------------------------------------------------ bangun datar
def shape(kind):
    """(nama, titik)"""
    s = ri(14, 22)
    if kind == "persegi":
        a = s * 5
        return [(0, 0), (a, 0), (a, a), (0, a)]
    if kind == "persegi panjang":
        a, b = s * 7, s * ri(3, 4)
        return [(0, 0), (a, 0), (a, b), (0, b)] if R().random() < 0.6 else [(0, 0), (b, 0), (b, a), (0, a)]
    if kind == "jajargenjang":
        a, b, o = s * 6, s * 3, s * ri(2, 3)
        return [(o, 0), (a + o, 0), (a, b), (0, b)]
    if kind == "trapesium":
        a, b, o1, o2 = s * 7, s * 3, s * ri(1, 2), s * ri(1, 3)
        return [(o1, 0), (a - o2, 0), (a, b), (0, b)]
    if kind == "belah ketupat":
        a, b = s * ri(3, 4), s * ri(2, 3)
        return [(a, 0), (2 * a, b), (a, 2 * b), (0, b)]
    if kind == "layang-layang":
        a, b, c = s * 3, s * 2, s * 5
        return [(a, 0), (2 * a, b), (a, c), (0, b)]
    if kind == "segitiga":
        t = ri(0, 2)
        if t == 0:
            return regular(3, s * 3.2)
        if t == 1:
            return [(0, 0), (0, s * 5), (s * 6, s * 5)]
        return [(s * ri(1, 4), 0), (s * 7, s * 5), (0, s * 5)]
    n = {"segi lima": 5, "segi enam": 6, "segi delapan": 8}[kind]
    return regular(n, s * 3.3, jitter=0.18 if R().random() < 0.4 else 0)


SIDES = {"segitiga": 3, "persegi": 4, "persegi panjang": 4, "jajargenjang": 4, "trapesium": 4, "belah ketupat": 4, "layang-layang": 4,
         "segi lima": 5, "segi enam": 6, "segi delapan": 8}
QUAD = ["persegi", "persegi panjang", "jajargenjang", "trapesium", "belah ketupat", "layang-layang"]
CIRI = {
    "persegi": "4 sisi sama panjang dan 4 sudut siku-siku",
    "persegi panjang": "2 pasang sisi berhadapan sama panjang dan 4 sudut siku-siku",
    "jajargenjang": "2 pasang sisi berhadapan sejajar dan sama panjang, tetapi tidak ada sudut siku-siku",
    "trapesium": "tepat 1 pasang sisi yang sejajar",
    "belah ketupat": "4 sisi sama panjang, tetapi sudutnya tidak siku-siku",
    "layang-layang": "2 pasang sisi yang berdekatan sama panjang",
}


def u15():
    def nama_segi():
        k = ch(["segitiga", "segi lima", "segi enam", "segi delapan", "segitiga", "segi lima", "segi enam"])
        pts = shape(k)
        k4 = "segi empat"
        names = ["segitiga", k4, "segi lima", "segi enam", "segi delapan"]
        return mcq("Nama bangun datar ini adalah …" + poly_svg(pts, "bangun datar"), k, [x for x in names if x != k],
                   "Bangun ini punya %d sisi, jadi namanya %s." % (SIDES[k], k))

    def nama_empat():
        k = ch(QUAD)
        pts = shape(k)
        return mcq("Nama segi empat ini adalah …" + poly_svg(pts, "segi empat"), k, [x for x in pool(QUAD) if x != k],
                   "Ciri %s: %s." % (k, CIRI[k]))

    def hitung():
        k = ch(list(SIDES))
        pts = shape(k)
        what = ch(["sisi", "titik sudut"])
        n = SIDES[k]
        return mcq("Berapa banyak %s pada bangun ini?" % what + poly_svg(pts, "bangun datar"), str(n), [str(n + 1), str(n - 1), str(n + 2)],
                   "Hitung satu per satu: ada %d %s. Banyak sisi dan titik sudut selalu sama." % (n, what))

    def ciri():
        k = ch(QUAD)
        return mcq("Bangun segi empat yang memiliki %s adalah …" % CIRI[k], k, [x for x in pool(QUAD) if x != k],
                   "Itu adalah ciri %s." % k)

    def dari_sisi():
        n = ch([3, 4, 5, 6, 8])
        nm = {3: "segitiga", 4: "segi empat", 5: "segi lima", 6: "segi enam", 8: "segi delapan"}
        who = A.K.next()
        what = ch(["sisi", "titik sudut"])
        return mcq("%s menggambar bangun datar yang memiliki %d %s. Bangun yang digambar %s adalah …" % (who, n, what, who), nm[n],
                   [v for kk, v in nm.items() if kk != n], "Bangun dengan %d %s disebut %s." % (n, what, nm[n]))

    TRUE = {
        "persegi": ["Semua sisinya sama panjang", "Keempat sudutnya siku-siku"],
        "persegi panjang": ["Sisi yang berhadapan sama panjang", "Keempat sudutnya siku-siku"],
        "segitiga": ["Memiliki 3 sisi dan 3 titik sudut"],
        "segi enam": ["Memiliki 6 sisi dan 6 titik sudut"],
        "trapesium": ["Memiliki tepat sepasang sisi yang sejajar"],
        "belah ketupat": ["Semua sisinya sama panjang"],
        "jajargenjang": ["Sisi yang berhadapan sejajar"],
    }
    FALSE = {
        "persegi": ["Hanya dua sisinya yang sama panjang", "Memiliki 5 titik sudut", "Tidak memiliki sudut siku-siku"],
        "persegi panjang": ["Semua sisinya selalu sama panjang", "Memiliki 3 sudut siku-siku", "Tidak ada sisi yang sejajar"],
        "segitiga": ["Memiliki 4 titik sudut", "Semua segitiga punya sudut siku-siku", "Memiliki 2 sisi"],
        "segi enam": ["Memiliki 5 sisi", "Memiliki 8 titik sudut", "Semua sudutnya siku-siku"],
        "trapesium": ["Semua sisinya sama panjang", "Memiliki 2 pasang sisi sejajar", "Memiliki 5 sisi"],
        "belah ketupat": ["Semua sudutnya siku-siku", "Memiliki 3 sisi", "Tidak ada sisi yang sejajar"],
        "jajargenjang": ["Semua sudutnya siku-siku", "Memiliki 6 titik sudut", "Tidak ada sisi yang sama panjang"],
    }

    def benar():
        k = ch(list(TRUE))
        return mcq("Pernyataan yang benar tentang %s adalah …" % k + poly_svg(shape(k), k), ch(TRUE[k]), FALSE[k],
                   "%s: %s." % (k.capitalize(), "; ".join(TRUE[k]).lower()))

    def siku():
        k = ch(["persegi", "persegi panjang", "segitiga siku-siku", "trapesium siku-siku", "jajargenjang", "belah ketupat"])
        s = ri(16, 22)
        pts = {"persegi": [(0, 0), (5 * s, 0), (5 * s, 5 * s), (0, 5 * s)],
               "persegi panjang": [(0, 0), (8 * s, 0), (8 * s, 4 * s), (0, 4 * s)],
               "segitiga siku-siku": [(0, 0), (0, 5 * s), (7 * s, 5 * s)],
               "trapesium siku-siku": [(0, 0), (4 * s, 0), (7 * s, 4 * s), (0, 4 * s)],
               "jajargenjang": [(2 * s, 0), (8 * s, 0), (6 * s, 4 * s), (0, 4 * s)],
               "belah ketupat": [(3 * s, 0), (6 * s, 2 * s), (3 * s, 4 * s), (0, 2 * s)]}[k]
        n = {"persegi": 4, "persegi panjang": 4, "segitiga siku-siku": 1, "trapesium siku-siku": 2, "jajargenjang": 0, "belah ketupat": 0}[k]
        return mcq("Berapa banyak sudut siku-siku pada bangun ini?" + poly_svg(pts, k), str(n), [str(x) for x in (0, 1, 2, 3, 4) if x != n],
                   "Sudut siku-siku seperti pojok buku. Bangun ini (%s) punya %d sudut siku-siku." % (k, n))

    sets = [("Nama bangun datar", [(nama_segi, 12), (dari_sisi, 8)]),
            ("Sisi dan titik sudut", [(hitung, 20)]),
            ("Jenis segi empat", [(nama_empat, 14), (ciri, 6)]),
            ("Ciri-ciri bangun datar", [(benar, 12), (siku, 8)]),
            ("Campuran", [(siku, 6), (dari_sisi, 4), (nama_empat, 6), (hitung, 4)])]
    body = lesson(
        ["Bangun datar dinamai menurut banyak sisinya: segitiga (3), segi empat (4), segi lima (5), segi enam (6), segi delapan (8).",
         "Banyak sisi selalu sama dengan banyak titik sudut.",
         "Segi empat ada beberapa jenis. Lihat panjang sisinya, sisi yang sejajar, dan sudut siku-sikunya."],
        [example("Bangun dengan 4 sisi sama panjang dan 4 sudut siku-siku.", ["4 sisi → segi empat", "Semua sisi sama dan siku-siku"], "persegi"),
         example("Bangun dengan tepat sepasang sisi sejajar.", ["4 sisi, hanya 1 pasang sejajar"], "trapesium")],
        [["Persegi dan belah ketupat dianggap sama", "Persegi punya sudut siku-siku, belah ketupat tidak"],
         ["Segi lima yang tidak beraturan tidak disebut segi lima", "Segi lima adalah semua bangun dengan 5 sisi"],
         ["Sisi miring tidak dihitung", "Hitung semua sisi, tegak, mendatar, atau miring"]],
        table(["Nama", "Sisi", "Titik sudut"], [["segitiga", "3", "3"], ["segi empat", "4", "4"], ["segi lima", "5", "5"], ["segi enam", "6", "6"], ["segi delapan", "8", "8"]]))
    faq = [{"q": "Apa saja jenis segi empat?", "a": "Persegi, persegi panjang, jajargenjang, trapesium, belah ketupat, dan layang-layang. Semuanya punya 4 sisi dan 4 titik sudut."},
           {"q": "Apa bedanya persegi dan persegi panjang?", "a": "Keduanya punya 4 sudut siku-siku. Pada persegi semua sisi sama panjang, pada persegi panjang hanya sisi yang berhadapan yang sama panjang."},
           {"q": "Apa itu segi banyak?", "a": "Segi banyak adalah bangun datar yang dibatasi oleh garis lurus, misalnya segi lima, segi enam, dan segi delapan."}]
    return dict(slug="bangun-datar", dom="G", sort=15,
                std_text="Peserta didik dapat mendeskripsikan ciri berbagai bentuk bangun datar (segi empat, segitiga, segi banyak).",
                title="Ciri-Ciri Bangun Datar", short_title="Bangun Datar",
                meta_desc="Latihan mengenal segitiga, segi empat, segi lima, segi enam, dan segi delapan, menghitung sisi dan titik sudut, jenis segi empat, dan sudut siku-siku. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Banyak sisi = banyak titik sudut", key_sub="Nama bangun datar menurut banyak sisinya.",
                body=body, faq=faq, sets=sets)


# ------------------------------------------------------------ menyusun dan mengurai
H3 = math.sqrt(3) / 2


def blocks(kind, s):
    """kepingan pola (pattern blocks) dengan sisi s"""
    if kind == "segitiga":
        return [(0, s * H3), (s, s * H3), (s / 2, 0)], []
    if kind == "belah ketupat":
        return [(0, s * H3), (s, s * H3), (1.5 * s, 0), (0.5 * s, 0)], []
    if kind == "trapesium":
        return [(0, s * H3), (2 * s, s * H3), (1.5 * s, 0), (0.5 * s, 0)], []
    if kind == "segi enam":
        return [(s * math.cos(math.pi / 3 * i) + s, s * math.sin(math.pi / 3 * i) + s * H3) for i in range(6)], []
    if kind == "segitiga besar":
        return [(0, 2 * s * H3), (2 * s, 2 * s * H3), (s, 0)], []
    if kind == "segitiga besar 3":
        return [(0, 3 * s * H3), (3 * s, 3 * s * H3), (1.5 * s, 0)], []
    raise ValueError(kind)


COLS = {"segitiga": "#7ec46d", "belah ketupat": "#6aa7e0", "trapesium": "#e86a5f", "segi enam": "#f2c94c",
        "segitiga besar": "#c3e6b5", "segitiga besar 3": "#c3e6b5"}
TRI = {"segitiga": 1, "belah ketupat": 2, "trapesium": 3, "segi enam": 6, "segitiga besar": 4, "segitiga besar 3": 9}
LBL = {"segitiga besar": "segitiga besar", "segitiga besar 3": "segitiga besar"}


def piece(kind, s=30):
    pts, _ = blocks(kind, s)
    return poly_svg(pts, kind, COLS[kind])


def split_fig(kind, w, h):
    """bangun dengan garis putus-putus: (titik, garis, jawaban, salah)"""
    if kind == 0:
        return [(0, 0), (w, 0), (w, h), (0, h)], [((0, 0), (w, h))], "2 segitiga siku-siku", ["2 persegi panjang", "3 segitiga", "1 segitiga dan 1 persegi"]
    if kind == 1:
        return [(0, 0), (w, 0), (w, h), (0, h)], [((w / 2, 0), (w / 2, h))], "2 persegi panjang", ["2 segitiga siku-siku", "4 persegi", "1 persegi panjang dan 1 segitiga"]
    if kind == 2:
        return [(0, 0), (w, 0), (w, w), (0, w)], [((0, 0), (w, w)), ((w, 0), (0, w))], "4 segitiga", ["2 segitiga", "4 persegi", "3 segitiga"]
    if kind == 3:
        return [(0, 0), (w, 0), (w, w), (0, w)], [((w / 2, 0), (w / 2, w)), ((0, w / 2), (w, w / 2))], "4 persegi kecil", ["4 segitiga", "2 persegi panjang", "3 persegi kecil"]
    if kind == 4:
        o = h * 0.8
        return [(o, 0), (w, 0), (w, h), (0, h)], [((o, 0), (o, h))], "1 segitiga siku-siku dan 1 persegi panjang", ["2 segitiga siku-siku", "2 persegi panjang", "1 segitiga dan 1 jajargenjang"]
    if kind == 5:
        o = h * 0.8
        return [(o, 0), (w - o, 0), (w, h), (0, h)], [((o, 0), (o, h)), ((w - o, 0), (w - o, h))], "2 segitiga siku-siku dan 1 persegi panjang", ["3 segitiga", "1 segitiga dan 2 persegi panjang", "2 persegi panjang dan 1 persegi"]
    if kind == 6:
        o = h * 0.8
        return [(o, 0), (w + o, 0), (w, h), (0, h)], [((o, 0), (w, h))], "2 segitiga", ["2 persegi panjang", "2 jajargenjang", "1 segitiga dan 1 persegi"]
    if kind == 7:
        r = w / 2
        pts = [(r + r * math.cos(math.pi / 3 * i), r * H3 + r * math.sin(math.pi / 3 * i)) for i in range(6)]
        c = (r, r * H3)
        return pts, [(c, p) for p in pts], "6 segitiga", ["3 segitiga", "6 belah ketupat", "2 trapesium"]
    if kind == 8:
        r = w / 2
        pts = [(r + r * math.cos(math.pi / 3 * i), r * H3 + r * math.sin(math.pi / 3 * i)) for i in range(6)]
        return pts, [(pts[0], pts[3])], "2 trapesium", ["2 segitiga", "3 belah ketupat", "2 persegi panjang"]
    if kind == 9:
        r = w / 2
        pts = [(r + r * math.cos(math.pi / 3 * i), r * H3 + r * math.sin(math.pi / 3 * i)) for i in range(6)]
        c = (r, r * H3)
        return pts, [(c, pts[0]), (c, pts[2]), (c, pts[4])], "3 belah ketupat", ["6 segitiga", "2 trapesium", "3 segitiga"]
    if kind == 10:
        return [(0, 0), (w, 0), (w, h), (0, h)], [((w / 3, 0), (w / 3, h)), ((2 * w / 3, 0), (2 * w / 3, h))], "3 persegi panjang", ["2 persegi panjang", "3 segitiga", "4 persegi panjang"]
    if kind == 11:
        return [(0, h), (w, h), (w / 2, 0)], [((w / 2, 0), (w / 2, h))], "2 segitiga siku-siku", ["2 persegi panjang", "3 segitiga", "1 segitiga dan 1 trapesium"]
    raise ValueError(kind)


def u16():
    def urai():
        kind = ri(0, 11)
        w = ri(7, 11) * 20 if kind not in (7, 8, 9) else ri(6, 8) * 20
        h = ri(4, 6) * 20
        pts, dashed, good, bad = split_fig(kind, w, h)
        return mcq("Bangun ini dipotong sepanjang garis putus-putus. Bangun-bangun yang terbentuk adalah …" + poly_svg(pts, "bangun dengan garis potong", dashed=dashed),
                   good, bad, "Lihat setiap bagian di antara garis putus-putus: %s." % good)

    def berapa():
        a, b = ch([("segitiga", "belah ketupat"), ("segitiga", "trapesium"), ("segitiga", "segi enam"), ("belah ketupat", "segi enam"),
                   ("trapesium", "segi enam"), ("segitiga", "segitiga besar"), ("segitiga", "segitiga besar 3")])
        k = ri(1, 4)
        n = TRI[b] // TRI[a] * k
        bn = LBL.get(b, b)
        what = ("1 %s" % bn) if k == 1 else ("%d %s" % (k, bn))
        return mcq("Berapa kepingan %s yang diperlukan untuk menyusun %s?%s%s" % (a, what, piece(a), piece(b, 30)), str(n),
                   [str(n + k), str(n - k) if n - k > 0 else str(n + 2 * k), str(TRI[b] * k + 1), str(n * 2)],
                   "1 %s tersusun dari %d %s. Untuk %d: %d × %d = %d." % (bn, TRI[b] // TRI[a], a, k, k, TRI[b] // TRI[a], n))

    COMB = [(["segitiga", "segitiga"], "belah ketupat", ["persegi", "trapesium", "segi enam"]),
            (["segitiga", "belah ketupat"], "trapesium", ["segi enam", "persegi", "segitiga besar"]),
            (["trapesium", "trapesium"], "segi enam", ["persegi panjang", "belah ketupat", "segi delapan"]),
            (["belah ketupat", "belah ketupat", "belah ketupat"], "segi enam", ["trapesium", "segi lima", "persegi"]),
            (["segitiga", "segitiga", "segitiga", "segitiga"], "segitiga besar", ["persegi", "segi enam", "trapesium"]),
            (["trapesium", "segitiga"], "segitiga besar", ["segi enam", "persegi", "belah ketupat"])]

    def susun():
        parts, res, bad = ch(COMB)
        s = ri(26, 34)
        pics = "".join(piece(p, s) for p in parts)
        return mcq("Kepingan-kepingan ini disusun tanpa celah dan tanpa tumpang tindih. Bangun yang dapat terbentuk adalah …" + pics, res, bad,
                   "%s menjadi %s." % (" dan ".join(sorted(set(parts))), res))

    def kotak():
        w, h = ri(2, 6), ri(2, 4)
        s = 24
        pts = [(0, 0), (w * s, 0), (w * s, h * s), (0, h * s)]
        dashed = [((i * s, 0), (i * s, h * s)) for i in range(1, w)] + [((0, j * s), (w * s, j * s)) for j in range(1, h)]
        half = R().random() < 0.5
        if half:
            dashed += [((i * s, j * s), ((i + 1) * s, (j + 1) * s)) for i in range(w) for j in range(h)]
            n = 2 * w * h
            return mcq("Persegi panjang ini disusun dari segitiga-segitiga kecil yang sama besar. Berapa banyak segitiga kecil itu?" + poly_svg(pts, "persegi panjang", dashed=dashed),
                       str(n), [str(w * h), str(n + 2), str(2 * (w + h))], "Ada %d persegi kecil, dan setiap persegi berisi 2 segitiga: %d × 2 = %d." % (w * h, w * h, n))
        n = w * h
        return mcq("Persegi panjang ini disusun dari persegi-persegi kecil. Berapa banyak persegi kecil itu?" + poly_svg(pts, "persegi panjang", dashed=dashed),
                   str(n), [str(w + h), str(2 * (w + h)), str(n + w)], "%d baris × %d persegi = %d." % (h, w, n))

    def cerita():
        a, b = ch([("segitiga", "segi enam"), ("belah ketupat", "segi enam"), ("trapesium", "segi enam"), ("segitiga", "trapesium"), ("segitiga", "belah ketupat")])
        per = TRI[b] // TRI[a]
        k = ri(2, 6)
        extra = ri(0, per - 1)
        have = per * k + extra
        who = K().next()
        return mcq("%s punya %d kepingan %s. Setiap %s disusun dari %d %s. Paling banyak berapa %s yang dapat disusun %s?" % (who, have, a, b, per, a, b, who),
                   str(k), [str(k + 1), str(have - per), str(per)] if have - per != k else [str(k + 1), str(k - 1), str(per + k)],
                   "%d : %d = %d%s." % (have, per, k, (" sisa %d" % extra) if extra else ""))

    def cara():
        n = ri(2, 5)
        b = ch(["segi enam", "trapesium"])
        if b == "segi enam":
            good = ch(["6 segitiga", "3 belah ketupat", "2 trapesium", "1 trapesium dan 3 segitiga", "1 trapesium, 1 belah ketupat, dan 1 segitiga", "2 belah ketupat dan 2 segitiga"])
            bad = ["5 segitiga", "4 belah ketupat", "3 trapesium", "2 belah ketupat dan 1 segitiga", "1 trapesium dan 2 segitiga"]
        else:
            good = ch(["3 segitiga", "1 belah ketupat dan 1 segitiga"])
            bad = ["2 segitiga", "2 belah ketupat", "4 segitiga", "1 belah ketupat dan 2 segitiga"]
        R().shuffle(bad)
        return mcq("Kepingan mana yang dapat menyusun satu %s? (1 belah ketupat = 2 segitiga, 1 trapesium = 3 segitiga, 1 segi enam = 6 segitiga)" % b + piece(b, 26 + n),
                   good, bad, "Hitung dalam segitiga: semuanya harus %d segitiga." % TRI[b])

    sets = [("Mengurai bangun datar", [(urai, 20)]),
            ("Menyusun bangun datar", [(susun, 13), (cara, 7)]),
            ("Berapa kepingan?", [(berapa, 20)]),
            ("Menghitung bagian", [(kotak, 14), (urai, 6)]),
            ("Soal cerita", [(cerita, 14), (berapa, 6)])]
    body = lesson(
        ["Menyusun (komposisi) berarti menggabungkan beberapa bangun datar menjadi bangun baru tanpa celah dan tanpa tumpang tindih.",
         "Mengurai (dekomposisi) berarti memotong satu bangun menjadi beberapa bangun yang lebih kecil.",
         "Satu bangun sering dapat disusun dengan lebih dari satu cara. Segi enam dapat disusun dari 6 segitiga, 3 belah ketupat, atau 2 trapesium."],
        [example("Persegi panjang dipotong dari pojok ke pojok.", ["Garis potong membagi dua bagian yang sama"], "2 segitiga siku-siku"),
         example("Berapa segitiga untuk 2 segi enam?", ["1 segi enam = 6 segitiga", "2 × 6"], "12 segitiga")],
        [["Kepingan boleh tumpang tindih", "Kepingan harus pas, tanpa celah dan tanpa tumpang tindih"],
         ["Mengira hanya ada satu cara", "Coba susunan lain dengan kepingan berbeda"],
         ["Lupa mengalikan saat bangunnya lebih dari satu", "Hitung untuk satu bangun, lalu kalikan"]])
    faq = [{"q": "Apa itu komposisi dan dekomposisi bangun datar?", "a": "Komposisi adalah menyusun beberapa bangun menjadi satu bangun baru. Dekomposisi adalah mengurai satu bangun menjadi beberapa bangun yang lebih kecil."},
           {"q": "Bangun apa saja yang dapat dibuat dari dua segitiga?", "a": "Dua segitiga sama besar dapat disusun menjadi persegi panjang, persegi, jajargenjang, belah ketupat, atau segitiga yang lebih besar, tergantung bentuk segitiganya."},
           {"q": "Mengapa segi enam bisa disusun dengan banyak cara?", "a": "Karena segi enam setara dengan 6 segitiga. Setiap gabungan kepingan yang jumlahnya 6 segitiga, misalnya 2 trapesium atau 3 belah ketupat, dapat menyusunnya."}]
    return dict(slug="menyusun-dan-mengurai-bangun-datar", dom="G", sort=16,
                std_text="Peserta didik dapat menyusun (komposisi) dan mengurai (dekomposisi) berbagai bangun datar dengan lebih dari satu cara jika memungkinkan.",
                title="Menyusun dan Mengurai Bangun Datar", short_title="Menyusun dan Mengurai Bangun Datar",
                meta_desc="Latihan memotong bangun datar menjadi bangun yang lebih kecil, menyusun kepingan segitiga, belah ketupat, trapesium, dan segi enam, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Tanpa celah, tanpa tumpang tindih", key_sub="Satu bangun bisa disusun dengan beberapa cara.",
                body=body, faq=faq, sets=sets)


# ------------------------------------------------------------ data
TOPIK = [("buah kesukaan", ["Mangga", "Pisang", "Jeruk", "Rambutan", "Salak", "Pepaya"], "siswa"),
         ("cara siswa pergi ke sekolah", ["Jalan kaki", "Sepeda", "Motor", "Angkot", "Mobil"], "siswa"),
         ("olahraga kesukaan", ["Sepak bola", "Bulu tangkis", "Voli", "Renang", "Lari"], "siswa"),
         ("warna kesukaan", ["Merah", "Biru", "Hijau", "Kuning", "Ungu"], "siswa"),
         ("buku yang dipinjam di perpustakaan", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"], "buku"),
         ("hewan peliharaan siswa", ["Kucing", "Ikan", "Burung", "Kelinci", "Ayam"], "ekor"),
         ("kue yang terjual di kantin", ["Lemper", "Risoles", "Onde-onde", "Kue lapis", "Pastel"], "buah"),
         ("tanaman di kebun sekolah", ["Cabai", "Tomat", "Terong", "Bayam", "Kangkung"], "pot")]


def dataset(lo=1, hi=10, n=None):
    t, cats, unit = ch(TOPIK)
    n = n or ri(4, min(5, len(cats)))
    cs = cats[:n] if t.startswith("buku") else R().sample(cats, n)
    vals = R().sample(range(lo, hi + 1), n)
    return t, list(zip(cs, vals)), unit


def pikto(data, unit):
    s = []
    lw = 108
    y = 10
    for name, v in data:
        s.append(text(6, y + 17, name, 13, anchor="start", weight=600))
        for i in range(v):
            cx = lw + 12 + i * 26
            s.append("<circle cx='%d' cy='%d' r='10' fill='#f2c94c' stroke='%s' stroke-width='1.3'/>"
                     "<circle cx='%d' cy='%d' r='1.6' fill='%s'/><circle cx='%d' cy='%d' r='1.6' fill='%s'/>"
                     "<path d='M%d %d q4 4 8 0' fill='none' stroke='%s' stroke-width='1.3'/>"
                     % (cx, y + 12, INK, cx - 3.5, y + 10, INK, cx + 3.5, y + 10, INK, cx - 4, y + 15, INK))
        s.append(line(lw, y - 4, lw, y + 28, "#bbb", 1))
        y += 32
    mx = max(v for _, v in data)
    W = lw + 24 + mx * 26
    s.append("<circle cx='18' cy='%d' r='10' fill='#f2c94c' stroke='%s' stroke-width='1.3'/>" % (y + 14, INK))
    s.append(text(34, y + 19, "= 1 %s" % unit, 13, anchor="start", weight=600))
    return wrap(max(W, 200), y + 32, "".join(s), "piktogram", lg=True)


def data_q(t, data, unit, pic, kind=None):
    kind = kind if kind is not None else ri(0, 4)
    names = [d[0] for d in data]
    vals = dict(data)
    if kind == 0:
        nm, v = ch(data)
        return mcq("Data %s.%s Berapa banyak %s untuk <b>%s</b>?" % (t, pic, unit, nm), str(v), [str(x) for x in sorted(set(vals.values()) - {v})] + [str(v + 1)],
                   "Baca data untuk %s: %d %s." % (nm, v, unit))
    if kind == 1:
        big = R().random() < 0.5
        nm = max(data, key=lambda d: d[1])[0] if big else min(data, key=lambda d: d[1])[0]
        return mcq("Data %s.%s Manakah yang paling %s?" % (t, pic, "banyak" if big else "sedikit"), nm, [x for x in names if x != nm],
                   "%s punya nilai %s, yaitu %d." % (nm, "terbesar" if big else "terkecil", vals[nm]))
    if kind == 2:
        (a, va), (b, vb) = R().sample(data, 2)
        if va == vb:
            return None
        if va < vb:
            (a, va), (b, vb) = (b, vb), (a, va)
        d = va - vb
        return mcq("Data %s.%s Berapa selisih data %s dan %s?" % (t, pic, a, b), str(d), [str(va + vb), str(d + 1), str(va)],
                   "%d − %d = %d." % (va, vb, d))
    if kind == 3:
        tot = sum(vals.values())
        return mcq("Data %s.%s Berapa jumlah semuanya?" % (t, pic), "%d %s" % (tot, unit), ["%d %s" % (x, unit) for x in (tot + 1, tot - 1, tot + 2, len(data))],
                   "%s = %d." % (" + ".join(str(v) for v in vals.values()), tot))
    (a, va), (b, vb) = R().sample(data, 2)
    s = va + vb
    return mcq("Data %s.%s Berapa jumlah %s untuk %s dan %s?" % (t, pic, unit, a, b), str(s), [str(abs(va - vb)), str(s + 1), str(s - 1)],
               "%d + %d = %d." % (va, vb, s))


def u17():
    def piktogram(kind=None):
        def mk():
            t, data, unit = dataset(1, 9)
            return data_q(t, data, unit, pikto(data, unit), kind)
        return mk

    def batang(kind=None):
        def mk():
            t, data, unit = dataset(1, 12)
            pic = diagram_batang(data, "Banyak " + unit, "diagram batang", 1)
            return data_q(t, data, unit, pic, kind)
        return mk

    def turus():
        n = ri(3, 19)
        return mcq("Bilangan yang ditunjukkan turus ini adalah …" + "<div class='qfig'>%s</div>" % strichliste(n),
                   str(n), [str(n + 1), str(n - 1), str(n // 5 + n % 5)] if n // 5 + n % 5 not in (n + 1, n - 1, n) else [str(n + 1), str(n - 1), str(n + 5)],
                   ("Satu ikat turus = 5. %d ikat dan %d turus: %d." % (n // 5, n % 5, n)) if n >= 5 else "Ada %d garis turus." % n)

    def tabel():
        t, data, unit = dataset(2, 20)
        rows = "".join("<tr><td>%s</td><td>%d</td></tr>" % d for d in data)
        tb = "<table class='sn-table' style='width:auto'><thead><tr><th>%s</th><th>Banyak %s</th></tr></thead><tbody>%s</tbody></table>" % (
            "Hari" if t.startswith("buku") else "Pilihan", unit, rows)
        return data_q(t, data, unit, tb)

    def tinggi():
        t, data, unit = dataset(1, 12)
        pic = diagram_batang(data, "Banyak " + unit, "diagram batang", 1)
        (a, va), (b, vb) = R().sample(data, 2)
        if va <= vb:
            return None
        return mcq("Data %s.%s Data %s lebih banyak berapa %s daripada data %s?" % (t, pic, a, unit, b), str(va - vb), [str(va + vb), str(va), str(va - vb + 1)],
                   "Batang %s = %d, batang %s = %d. %d − %d = %d." % (a, va, b, vb, va, vb, va - vb))

    sets = [("Membaca tabel dan turus", [(turus, 10), (tabel, 10)]),
            ("Piktogram", [(piktogram(0), 6), (piktogram(1), 5), (piktogram(2), 5), (piktogram(3), 4)]),
            ("Diagram batang", [(batang(0), 7), (batang(1), 7), (batang(4), 6)]),
            ("Membandingkan data", [(tinggi, 10), (batang(2), 5), (piktogram(4), 5)]),
            ("Campuran", [(piktogram(), 7), (batang(), 7), (tabel, 6)])]
    body = lesson(
        ["Data dapat disajikan dalam tabel, turus, piktogram, atau diagram batang.",
         "Pada piktogram, lihat keterangannya. Di sini satu gambar mewakili 1.",
         "Pada diagram batang, baca angka pada sumbu tegak di ujung atas batang. Batang paling tinggi menunjukkan data terbanyak."],
        [example("Batang Mangga sampai angka 7 dan batang Jeruk sampai angka 4.", ["Selisih = 7 − 4"], "3 siswa"),
         example("Turus: 2 ikat dan 3 garis.", ["1 ikat = 5", "5 + 5 + 3"], "13")],
        [["Membaca diagram batang dari panjang batang di gambar dengan penggaris", "Baca angka pada sumbu tegak"],
         ["Lupa keterangan piktogram", "Periksa dulu satu gambar mewakili berapa"],
         ["Selisih dihitung dengan menjumlah", "Selisih = nilai besar − nilai kecil"]])
    faq = [{"q": "Apa itu piktogram?", "a": "Piktogram adalah penyajian data dengan gambar. Setiap gambar mewakili sejumlah benda sesuai keterangan, misalnya satu gambar mewakili 1 siswa."},
           {"q": "Bagaimana membaca diagram batang?", "a": "Lihat ujung atas batang, lalu tarik garis ke sumbu tegak dan baca angkanya. Di kelas 4 skalanya satu satuan, jadi setiap garis bantu bernilai 1."},
           {"q": "Apa itu turus?", "a": "Turus adalah garis-garis untuk mencatat data. Setiap garis bernilai 1, dan setiap 5 garis diikat dengan garis miring."}]
    return dict(slug="piktogram-dan-diagram-batang", dom="D", sort=17,
                std_text="Peserta didik dapat mengurutkan, membandingkan, menyajikan, menganalisis, dan menginterpretasi data dalam bentuk tabel, diagram gambar, piktogram, dan diagram batang (skala satu satuan).",
                title="Tabel, Piktogram, dan Diagram Batang", short_title="Piktogram dan Diagram Batang",
                meta_desc="Latihan membaca tabel, turus, piktogram, dan diagram batang skala satu satuan, menentukan data terbanyak, selisih, dan jumlah. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Baca keterangan dan sumbunya", key_sub="Batang tertinggi = data terbanyak.",
                body=body, faq=faq, sets=sets)
