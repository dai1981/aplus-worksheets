# -*- coding: utf-8 -*-
"""Türkiye 4. sınıf: Nesnelerin Geometrisi, Olayların Olasılığı ve Veriye Dayalı Araştırma — 19〜25 単元（tr_run.py 4）。"""
from tr_common import low
import math
import random as _r
import tr_g as G
from tr_g import unit, cap, num, oku, mcq, M, wrap, text, line, poly, grid_shape, dot_plot, freq_table, sutun_grafigi, cetele, NB, INK, GREEN, FILL, RED, BLUE
import id_k5b as IDB
from tr_common import hm, saat_svg
import gen_au_maths_y5_angles as AU

AU.random = _r


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def row4(svgs, caps=("A", "B", "C", "D")):
    return "<div class='qfig'>" + "".join("<span style='display:inline-block;margin:4px 10px;text-align:center;vertical-align:top'><b>%s</b><br>%s</span>"
                                          % (c, s.replace("<div class='qfig'>", "").replace("</div>", "")) for c, s in zip(caps, svgs)) + "</div>"


# ============================================================ 19. açınımlar
def net_letters(cells, letters, sz=30):
    s = []
    for i, (x, y) in enumerate(cells):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (6 + x * sz, 6 + y * sz, sz, sz, FILL, GREEN))
        if letters:
            s.append(text(6 + x * sz + sz / 2.0, 6 + y * sz + sz / 2.0 + 6, letters[i], 16))
    W = (max(c[0] for c in cells) + 1) * sz + 12
    H = (max(c[1] for c in cells) + 1) * sz + 12
    return G.wrap(W, H, "".join(s), "küpün açınımı")


def prism_net(kind):
    """kare prizma, dikdörtgenler prizması, üçgen prizma, kare piramit, silindir, koni açınımları (kabaca)"""
    s = []
    if kind in ("kare prizma", "dikdörtgenler prizması"):
        a, b, h = (30, 30, 50) if kind == "kare prizma" else (44, 26, 34)
        xs = [6, 6 + a, 6 + a + b, 6 + 2 * a + b]
        ws = [a, b, a, b]
        for x, w in zip(xs, ws):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, 6 + b, w, h, FILL, GREEN))
        s.append("<rect x='%d' y='6' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (6 + a, b, b, FILL, GREEN))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (6 + a, 6 + b + h, b, b, FILL, GREEN))
        W, H = 12 + 2 * (a + b), 12 + 2 * b + h
    elif kind == "üçgen prizma":
        a, h = 40, 60
        for i in range(3):
            s.append("<rect x='%d' y='40' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (6 + i * a, a, h, FILL, GREEN))
        x0 = 6 + a
        s.append("<polygon points='%d,40 %d,40 %d,%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x0, x0 + a, x0 + a / 2, 40 - 34, FILL, GREEN))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x0, 40 + h, x0 + a, 40 + h, x0 + a / 2, 40 + h + 34, FILL, GREEN))
        W, H = 12 + 3 * a, 40 + h + 40
    elif kind in ("kare piramit", "üçgen piramit"):
        a = 46
        cx, cy = 80, 80
        if kind == "kare piramit":
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx - a / 2, cy - a / 2, a, a, FILL, GREEN))
            for (x1, y1, x2, y2, tx, ty) in [(-1, -1, 1, -1, 0, -2), (1, -1, 1, 1, 2, 0), (1, 1, -1, 1, 0, 2), (-1, 1, -1, -1, -2, 0)]:
                s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.6'/>"
                         % (cx + x1 * a / 2, cy + y1 * a / 2, cx + x2 * a / 2, cy + y2 * a / 2, cx + tx * a * 0.85, cy + ty * a * 0.85, FILL, GREEN))
            W = H = 160
        else:
            P = [(cx, cy - 30), (cx - 26, cy + 15), (cx + 26, cy + 15)]
            s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.6'/>" % (" ".join("%.1f,%.1f" % p for p in P), FILL, GREEN))
            for i in range(3):
                p, q = P[i], P[(i + 1) % 3]
                mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                ox, oy = mx - cx, my - (cy + 0)
                d = math.hypot(ox, oy)
                t = (mx + ox / d * 45, my + oy / d * 45)
                s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.6'/>" % (p[0], p[1], q[0], q[1], t[0], t[1], FILL, GREEN))
            W = H = 160
    elif kind == "silindir":
        s.append("<rect x='6' y='40' width='130' height='60' fill='%s' stroke='%s' stroke-width='1.6'/>" % (FILL, GREEN))
        s.append("<circle cx='71' cy='21' r='19' fill='%s' stroke='%s' stroke-width='1.6'/>" % (FILL, GREEN))
        s.append("<circle cx='71' cy='119' r='19' fill='%s' stroke='%s' stroke-width='1.6'/>" % (FILL, GREEN))
        W, H = 142, 144
    else:  # koni
        s.append("<path d='M70 10 L20 90 A60 60 0 0 0 120 90 Z' fill='%s' stroke='%s' stroke-width='1.6'/>" % (FILL, GREEN))
        s.append("<circle cx='70' cy='122' r='22' fill='%s' stroke='%s' stroke-width='1.6'/>" % (FILL, GREEN))
        W, H = 140, 150
    return G.wrap(W, H, "".join(s), "bir geometrik cismin açınımı")


NET_FACES = {"küp": "6 kare", "kare prizma": "2 kare ve 4 dikdörtgen", "dikdörtgenler prizması": "6 dikdörtgen", "üçgen prizma": "2 üçgen ve 3 dikdörtgen",
             "kare piramit": "1 kare ve 4 üçgen", "üçgen piramit": "4 üçgen", "silindir": "2 daire ve 1 dikdörtgen", "koni": "1 daire ve 1 daire dilimi"}


def u19():
    IDB.build_nets()

    def kup_mu():
        good = ch(IDB.NETS_OK)
        bads = sh(IDB.NETS_BAD)[:3]
        figs = [good] + bads
        figs = sh(figs)
        k = figs.index(good)
        return mcq("Hangisi bir küpün açınımıdır?" + row4([net_letters(f, None, 20) for f in figs]), "ABCD"[k], [x for i, x in enumerate("ABCD") if i != k],
                   "Katlandığında altı yüz üst üste binmeden kapanan tek açınım <b>%s</b>." % "ABCD"[k])

    def karsi():
        cells = ch(IDB.NETS_OK)
        cells = list(cells)
        nm = IDB.fold(cells)
        letters = sh(list("ABCDEF"))
        i = ri(0, 5)
        n = nm[cells[i]]
        j = [t for t in range(6) if nm[cells[t]] == tuple(-x for x in n)][0]
        return mcq("Açınım katlanarak küp yapılıyor. %s yüzünün karşısına hangi yüz gelir?%s" % (letters[i], net_letters(cells, letters)), letters[j],
                   [letters[t] for t in range(6) if t not in (i, j)], "Karşılıklı yüzler katlanınca birbirine değmez; aralarında bir kare vardır. %s yüzünün karşısı <b>%s</b>." % (letters[i], letters[j]))

    def hangi_cisim():
        kind = ch(list(NET_FACES))
        if kind == "küp":
            kind = "kare prizma"
        return mcq("Açınımı verilen geometrik cisim hangisidir?" + prism_net(kind), cap(kind),
                   [cap(x) for x in sh([k for k in NET_FACES if k != kind and k != "küp"])], "Açınımda %s var: <b>%s</b>." % (NET_FACES[kind], kind))

    def yuzler():
        kind = ch(list(NET_FACES))
        k = ri(0, 1)
        if k == 0:
            return mcq("%s cisminin açınımı hangi şekillerden oluşur?" % cap(kind), NET_FACES[kind], [v for x, v in NET_FACES.items() if x != kind],
                       "%s: <b>%s</b>." % (cap(kind), NET_FACES[kind]))
        return mcq("Açınımı %s olan cisim hangisidir?" % NET_FACES[kind], cap(kind), [cap(x) for x in NET_FACES if x != kind], "<b>%s</b>." % cap(kind))

    def kup_yuz():
        cells = ch(IDB.NETS_OK)
        k = ri(0, 2)
        if k == 0:
            return mcq("Bir küpün açınımında kaç kare vardır?" + net_letters(list(cells), None, 22), "6", ["4", "5", "8"], "Küpün 6 yüzü var, açınımında <b>6</b> kare olur.")
        if k == 1:
            n = ri(2, 6)
            return mcq("Bir kenarı %d cm olan küpün açınımında bir karenin bir kenarı kaç santimetredir?" % n, "%d cm" % n, ["%d cm" % (n * 6), "%d cm" % (n * 4), "%d cm" % (n + 6)],
                       "Küpün bütün ayrıtları eşittir; açınımdaki kareler de aynı büyüklüktedir: <b>%d cm</b>." % n)
        cells2 = list(cells)
        idx = ri(0, 5)
        miss = cells2[:idx] + cells2[idx + 1:]
        return mcq("Bir küpün açınımından bir kare koparılmış. Küp yapmak için kaç kare daha gerekir?" + net_letters(miss, None, 22), "1", ["2", "0", "6"],
                   "Açınımda 5 kare var. Küpün 6 yüzü olduğu için <b>1</b> kare gerekir.")

    def ozellik():
        GEN = {"küp": "küpün", "kare prizma": "kare prizmanın", "dikdörtgenler prizması": "dikdörtgenler prizmasının", "üçgen prizma": "üçgen prizmanın",
               "kare piramit": "kare piramidin", "üçgen piramit": "üçgen piramidin", "beşgen prizma": "beşgen prizmanın", "altıgen prizma": "altıgen prizmanın"}
        V = {"küp": (6, 8, 12), "kare prizma": (6, 8, 12), "dikdörtgenler prizması": (6, 8, 12), "üçgen prizma": (5, 6, 9), "kare piramit": (5, 5, 8),
             "üçgen piramit": (4, 4, 6), "beşgen prizma": (7, 10, 15), "altıgen prizma": (8, 12, 18)}
        kind = ch(list(GEN))
        j = ri(0, 2)
        w = ["yüzü", "köşesi", "ayrıtı"][j]
        v = V[kind][j]
        return mcq("Bir %s kaç %s vardır?" % (GEN[kind], w), str(v), [str(x) for x in V[kind] if x != v] + [str(v + 1), str(v - 1)],
                   "%s: %d yüz, %d köşe, %d ayrıt. Cevap <b>%d</b>." % (cap(kind), V[kind][0], V[kind][1], V[kind][2], v))

    def kup_alan():
        n = ri(2, 6)
        return mcq("Bir küpün her yüzü %d × %d birim kareden oluşuyor. Küpün açınımı toplam kaç birim karedir?" % (n, n), str(6 * n * n),
                   [str(4 * n * n), str(n * n), str(6 * n), str(5 * n * n)], "Bir yüz %d birim kare, 6 yüz: 6 × %d = <b>%d</b>." % (n * n, n * n, 6 * n * n))

    sets = [("Küpün açınımı", [(kup_mu, 20)]),
            ("Karşılıklı yüzler", [(karsi, 20)]),
            ("Açınımdan cisme", [(hangi_cisim, 7), (yuzler, 13)]),
            ("Yüz, köşe ve ayrıt", [(ozellik, 20)]),
            ("Küp ve açınımı", [(kup_yuz, 8), (kup_alan, 4), (karsi, 4), (kup_mu, 4)])]
    return unit("geometrik-cisimlerin-acinimlari", "G", "MAT.4.3.1", 19, "Geometrik Cisimlerin Açınımları", "Cisimlerin Açınımları",
                "Geometrik cisimlerin açınımlarını inceleyerek yüzler arasındaki ilişkileri ortaya koyar ve açınımdan cismi oluşturur.",
                "4. sınıf geometrik cisimlerin açınımları çalışma kâğıdı: küpün açınımları, karşılıklı yüzler, prizma, piramit, silindir ve koninin açınımı. 100 soru ve cevap anahtarı.",
                "Açınım, cismin yüzlerinin düz hâlidir", "Küpün açınımında 6 eş kare vardır.", sets,
                ["Bir cismi yüzlerinden kesip düzlemde açtığımızda açınımını elde ederiz. Açınımdaki şekiller cismin yüzleridir.",
                 "Küpün 11 farklı açınımı vardır; hepsinde 6 eş kare bulunur. 2 × 3 gibi kare blokları ya da bir sırada 5 kare küp açınımı olmaz.",
                 "Prizmanın açınımında 2 taban ve yan yüzler, piramidin açınımında 1 taban ve üçgen yan yüzler bulunur."],
                [("Üçgen prizmanın açınımı", ["Tabanlar: 2 üçgen", "Yan yüzler: 3 dikdörtgen"], "2 üçgen ve 3 dikdörtgen"),
                 ("Küp açınımında karşılıklı yüzler", ["Bir sırada yan yana olmayan, arada bir kare bulunan yüzler"], "katlanınca karşı karşıya gelir")],
                [["Her 6 kareli şekli küp açınımı sanmak", "Katlandığında yüzler üst üste binmemeli"], ["Yan yana kareleri karşılıklı sanmak", "Yan yana kareler katlanınca komşu olur"],
                 ["Silindirin yan yüzünü daire sanmak", "Silindirin yan yüzü açılınca dikdörtgen olur"]],
                [("Küpün kaç farklı açınımı vardır?", "11 farklı açınımı vardır."),
                 ("Açınımı nasıl kontrol ederim?", "Kâğıda çizip kesip katlayarak; ya da bir kareyi taban seçip diğerlerini zihninde katlayarak."),
                 ("Piramit ile prizmanın açınımı nasıl ayırt edilir?", "Prizmada iki taban ve dikdörtgen yan yüzler, piramitte bir taban ve üçgen yan yüzler vardır.")])


# ============================================================ 20. üçgen, kare, dikdörtgen
def tri_by_sides(a, b, c, unit_="cm"):
    """kenar uzunlukları a (taban), b (sol), c (sağ) olan üçgeni ölçekli çiz"""
    sc = 150.0 / max(a, b, c)
    A_, B_, C_ = a * sc, b * sc, c * sc
    x = (B_ ** 2 - C_ ** 2 + A_ ** 2) / (2 * A_)
    y = math.sqrt(max(B_ ** 2 - x ** 2, 1))
    pts = [(0, 0), (A_, 0), (x, -y)]
    return poly(pts, [str(a), str(c), str(b)], unit_=unit_, label="kenar uzunlukları verilen üçgen")


def tri_kind(a, b, c):
    s = sorted([a, b, c])
    if s[0] == s[2]:
        return "Eşkenar üçgen"
    if s[0] == s[1] or s[1] == s[2]:
        return "İkizkenar üçgen"
    return "Çeşitkenar üçgen"


def rand_tri(kind):
    while True:
        if kind == "Eşkenar üçgen":
            a = ri(3, 12)
            t = (a, a, a)
        elif kind == "İkizkenar üçgen":
            a, b = ri(3, 12), ri(3, 12)
            if a == b or b >= 2 * a or a >= 2 * b + 6:
                continue
            t = sh([a, a, b])
        else:
            t = sh(sorted(set(ri(3, 14) for _ in range(5)))[:3])
            if len(t) < 3:
                continue
        s = sorted(t)
        if s[0] + s[1] > s[2] + 1:
            return t


def u20():
    def ucgen_turu():
        kind = ch(["Eşkenar üçgen", "İkizkenar üçgen", "Çeşitkenar üçgen"])
        a, b, c = rand_tri(kind)
        return mcq("Kenar uzunlukları verilen üçgen hangi üçgendir?" + tri_by_sides(a, b, c), kind, ["Eşkenar üçgen", "İkizkenar üçgen", "Çeşitkenar üçgen", "Dik üçgen"],
                   {"Eşkenar üçgen": "Üç kenarı da eşit: <b>eşkenar üçgen</b>.", "İkizkenar üçgen": "İki kenarı eşit: <b>ikizkenar üçgen</b>.",
                    "Çeşitkenar üçgen": "Üç kenarı da farklı: <b>çeşitkenar üçgen</b>."}[kind])

    def ucgen_sozel():
        kind = ch(["Eşkenar üçgen", "İkizkenar üçgen", "Çeşitkenar üçgen"])
        a, b, c = rand_tri(kind)
        return mcq("Kenar uzunlukları %d cm, %d cm ve %d cm olan üçgen hangi üçgendir?" % (a, b, c), kind, ["Eşkenar üçgen", "İkizkenar üçgen", "Çeşitkenar üçgen", "Kare"],
                   "Eşit kenarları sayarız: <b>%s</b>." % low(kind))

    def kose_kenar():
        S = [("üçgenin", 3), ("karenin", 4), ("dikdörtgenin", 4), ("beşgenin", 5), ("altıgenin", 6)]
        sh_, n = ch(S)
        w = ch(["köşesi", "kenarı"])
        return mcq("Bir %s kaç %s vardır?" % (sh_, w), str(n), [str(x) for x in (n - 1, n + 1, n + 2, 2 * n) if x != n],
                   "Çokgenlerde köşe sayısı kenar sayısına eşittir: <b>%d</b>." % n)

    def kare_dikd():
        S = [("Her kare bir dikdörtgendir.", "Doğru"), ("Her dikdörtgen bir karedir.", "Yanlış"), ("Karenin bütün kenarları eşittir.", "Doğru"),
             ("Dikdörtgenin karşılıklı kenarları eşittir.", "Doğru"), ("Dikdörtgenin bütün kenarları her zaman eşittir.", "Yanlış"),
             ("Karenin dört köşesi de dik açıdır.", "Doğru"), ("Eşkenar üçgenin iki kenarı farklı uzunluktadır.", "Yanlış"),
             ("İkizkenar üçgenin en az iki kenarı eşittir.", "Doğru"), ("Çeşitkenar üçgenin iki kenarı eşittir.", "Yanlış"),
             ("Dikdörtgenin dört köşesi de dik açıdır.", "Doğru"), ("Üçgenin dört köşesi vardır.", "Yanlış"), ("Her eşkenar üçgen bir ikizkenar üçgendir.", "Doğru")]
        st, g = ch(S)
        return mcq("“%s” ifadesi doğru mu, yanlış mı?" % st, g, ["Yanlış" if g == "Doğru" else "Doğru", "Bazen doğru", "Bilinemez"],
                   "<b>%s</b>. Karenin dört kenarı eşit ve dört köşesi dik açıdır; bu yüzden kare özel bir dikdörtgendir." % g if "kare" in low(st) or "dikdörtgen" in low(st)
                   else "<b>%s</b>. Eşkenar üçgende üç, ikizkenar üçgende en az iki kenar eşittir; çeşitkenar üçgende hiçbir kenar eşit değildir." % g)

    def eksik_kenar():
        k = ri(0, 1)
        if k == 0:
            a, b = ri(3, 15), ri(3, 15)
            if a == b:
                return None
            pic = poly([(0, 0), (a * 12, 0), (a * 12, -b * 12), (0, -b * 12)], [str(a), None, None, str(b)], label="dikdörtgen", rights=(0, 1, 2, 3))
            return mcq("Dikdörtgenin üst kenarı kaç santimetredir?" + pic, "%d cm" % a, ["%d cm" % b, "%d cm" % (a + b), "%d cm" % (2 * a)],
                       "Dikdörtgenin karşılıklı kenarları eşittir: <b>%d cm</b>." % a)
        a = ri(3, 14)
        b = ri(3, 14)
        if a == b:
            return None
        kind = "İkizkenar"
        return mcq("Bir ikizkenar üçgenin eşit kenarlarından biri %d cm, farklı kenarı %d cm. Üçgenin kenar uzunlukları hangileridir?" % (a, b),
                   "%d cm, %d cm, %d cm" % (a, a, b), ["%d cm, %d cm, %d cm" % (a, b, b), "%d cm, %d cm, %d cm" % (a, a, a), "%d cm, %d cm, %d cm" % (b, b, b)],
                   "İkizkenar üçgende iki kenar eşittir: <b>%d cm, %d cm, %d cm</b>." % (a, a, b))

    sets = [("Kenarlarına göre üçgenler", [(ucgen_turu, 20)]),
            ("Kenar uzunluklarından üçgen türü", [(ucgen_sozel, 20)]),
            ("Köşe ve kenar", [(kose_kenar, 8), (eksik_kenar, 12)]),
            ("Kare ve dikdörtgen ilişkisi", [(kare_dikd, 10), (eksik_kenar, 10)]),
            ("Karışık sorular", [(ucgen_turu, 9), (ucgen_sozel, 9), (kare_dikd, 2)])]
    return unit("ucgen-kare-ve-dikdortgen", "G", "MAT.4.3.2", 20, "Üçgen, Kare ve Dikdörtgen: Köşe, Kenar ve Üçgen Çeşitleri", "Üçgen, Kare ve Dikdörtgen",
                "Üçgen, kare ve dikdörtgenin köşe ve kenarlarını belirler; üçgenleri kenar uzunluklarına göre sınıflandırır, kare ile dikdörtgen arasındaki ilişkiyi açıklar.",
                "4. sınıf üçgen, kare ve dikdörtgen çalışma kâğıdı: eşkenar, ikizkenar ve çeşitkenar üçgen, köşe ve kenar sayısı, kare ile dikdörtgen arasındaki ilişki. 100 soru ve cevap anahtarı.",
                "Üçgenler kenarlarına göre üçe ayrılır", "Her kare bir dikdörtgendir, tersi doğru değildir.", sets,
                ["Eşkenar üçgenin üç kenarı eşittir. İkizkenar üçgenin iki kenarı eşittir. Çeşitkenar üçgenin üç kenarı da farklıdır.",
                 "Dikdörtgenin karşılıklı kenarları eşittir ve dört köşesi dik açıdır. Karenin ise dört kenarı da eşittir.",
                 "Kare, bütün kenarları eşit olan bir dikdörtgendir. Bu yüzden her kare bir dikdörtgendir ama her dikdörtgen kare değildir."],
                [("Kenarları 5 cm, 5 cm, 8 cm olan üçgen", ["İki kenar eşit"], "ikizkenar üçgen"), ("Kenarları 4, 6, 7 cm olan üçgen", ["Hiçbir kenar eşit değil"], "çeşitkenar üçgen")],
                [["Kareyi dikdörtgen saymamak", "Kare özel bir dikdörtgendir"], ["İkizkenar üçgende üç kenarın eşit olması gerektiğini sanmak", "İki kenarın eşit olması yeter"],
                 ["Üçgeni çizimdeki görüntüsüne göre sınıflamak", "Kenar uzunluklarına bak"]],
                [("Eşkenar üçgen ikizkenar üçgen midir?", "Evet. En az iki kenarı eşit olduğu için her eşkenar üçgen aynı zamanda ikizkenardır."),
                 ("Dikdörtgen ile karenin ortak özellikleri nelerdir?", "İkisinin de 4 kenarı, 4 köşesi ve 4 dik açısı vardır; karşılıklı kenarları eşittir."),
                 ("Köşe ve kenar sayısı neden eşittir?", "Çokgenlerde her kenar iki köşeyi birleştirir ve şekil kapalıdır; bu yüzden sayılar eşittir.")])


# ============================================================ 21. çevre ve alan
def u21():
    def ucgen_cevre():
        kind = ch(["Eşkenar üçgen", "İkizkenar üçgen", "Çeşitkenar üçgen"])
        a, b, c = rand_tri(kind)
        g = a + b + c
        return mcq("Üçgenin çevre uzunluğu kaç santimetredir?" + tri_by_sides(a, b, c), "%d cm" % g, ["%d cm" % x for x in (a + b, g + max(a, b, c), a * b, g - 1)],
                   "Bütün kenarlar toplanır: %d + %d + %d = <b>%d cm</b>." % (a, b, c, g))

    def dikd_cevre():
        a, b = ri(3, 18), ri(2, 12)
        if a == b:
            return None
        pic = poly([(0, 0), (a * 10, 0), (a * 10, -b * 10), (0, -b * 10)], [str(a), str(b), None, None], label="dikdörtgen", rights=(0, 1, 2, 3))
        g = 2 * (a + b)
        return mcq("Dikdörtgenin çevre uzunluğu kaç santimetredir?" + pic, "%d cm" % g, ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm" % (2 * a + b)],
                   "Karşılıklı kenarlar eşit: %d + %d + %d + %d = <b>%d cm</b>." % (a, b, a, b, g))

    def kare_cevre():
        a = ri(2, 25)
        k = ri(0, 1)
        if k == 0:
            return mcq("Bir kenarı %d cm olan karenin çevre uzunluğu kaç santimetredir?" % a, "%d cm" % (4 * a), ["%d cm" % x for x in (2 * a, a * a, 3 * a, a + 4)],
                       "Karenin 4 kenarı eşit: 4 × %d = <b>%d cm</b>." % (a, 4 * a))
        return mcq("Çevre uzunluğu %d cm olan karenin bir kenarı kaç santimetredir?" % (4 * a), "%d cm" % a, ["%d cm" % x for x in (2 * a, 4 * a, a + 2, 4 * a - 4)],
                   "%d ÷ 4 = <b>%d cm</b>." % (4 * a, a))

    def eksik():
        a, b = ri(3, 20), ri(2, 15)
        if a == b:
            return None
        g = 2 * (a + b)
        return mcq("Çevre uzunluğu %d cm olan bir dikdörtgenin uzun kenarı %d cm ise kısa kenarı kaç santimetredir?" % (g, max(a, b)), "%d cm" % min(a, b),
                   ["%d cm" % x for x in (g - max(a, b), g // 2, (g - max(a, b)) // 2 + 1, min(a, b) * 2)],
                   "Bir uzun ve bir kısa kenar çevrenin yarısıdır: %d ÷ 2 = %d. %d − %d = <b>%d cm</b>." % (g, g // 2, g // 2, max(a, b), min(a, b)))

    def alan_say():
        w, h = ri(2, 6), ri(2, 5)
        cells = [(x, y) for x in range(w) for y in range(h)]
        extra = ri(0, 3)
        for _ in range(extra):
            cells.append((w, ri(0, h - 1)))
        cells = sorted(set(cells))
        n = len(cells)
        return mcq("Şeklin alanı kaç birim karedir?" + grid_shape(cells), "%d birim kare" % n, ["%d birim kare" % x for x in (n + 2, n - 1, 2 * (w + h), n + w)],
                   "Boyalı kareleri sayarız: <b>%d birim kare</b>." % n)

    def alan_yarim():
        w, h = ri(2, 5), ri(2, 4)
        cells = [(x, y) for x in range(w) for y in range(h)]
        tri = [(w, y, ch([1, 2])) for y in range(h)]
        t = len(tri)
        if t % 2:
            tri = tri[:-1]
            t -= 1
        n = len(cells) + t // 2
        return mcq("Şeklin alanı kaç birim karedir? (İki yarım kare bir birim kare eder.)" + grid_shape(cells, tri=tri), "%d birim kare" % n,
                   ["%d birim kare" % x for x in (len(cells) + t, len(cells), n + 1, n - 1)], "%d tam kare ve %d yarım kare: %d + %d = <b>%d birim kare</b>." % (len(cells), t, len(cells), t // 2, n))

    def karsilastir():
        a = [(x, y) for x in range(ri(2, 5)) for y in range(ri(2, 4))]
        b = [(x, y) for x in range(ri(2, 5)) for y in range(ri(2, 4))]
        if len(a) == len(b):
            return None
        pic = row4([grid_shape(a, label="A şekli"), grid_shape(b, col="#f4c28b", label="B şekli")], ("A", "B"))
        g = "A" if len(a) > len(b) else "B"
        d = abs(len(a) - len(b))
        return mcq("Hangi şeklin alanı daha büyüktür ve kaç birim kare fazladır?" + pic, "%s, %d birim kare" % (g, d),
                   ["%s, %d birim kare" % ("B" if g == "A" else "A", d), "%s, %d birim kare" % (g, d + 1), "%s, %d birim kare" % (g, max(len(a), len(b)))],
                   "A: %d, B: %d birim kare. Fark <b>%d</b>." % (len(a), len(b), d))

    sets = [("Üçgenin çevresi", [(ucgen_cevre, 20)]),
            ("Kare ve dikdörtgenin çevresi", [(dikd_cevre, 10), (kare_cevre, 10)]),
            ("Eksik kenarı bulma", [(eksik, 20)]),
            ("Birim karelerle alan", [(alan_say, 12), (alan_yarim, 8)]),
            ("Alanları karşılaştırma", [(karsilastir, 12), (alan_yarim, 8)])]
    return unit("cevre-ve-alan", "G", "MAT.4.3.3, MAT.4.3.4", 21, "Çevre Uzunluğu ve Birim Karelerle Alan", "Çevre ve Alan",
                "Üçgen, kare ve dikdörtgenin çevre uzunluklarını ölçer; şekillerin alanlarını standart olmayan birimlerle tahmin eder ve ölçer.",
                "4. sınıf çevre ve alan çalışma kâğıdı: üçgen, kare ve dikdörtgenin çevre uzunluğu, eksik kenar, birim karelerle alan ölçme ve alanları karşılaştırma. 100 soru ve cevap anahtarı.",
                "Çevre: kenarlar toplamı", "Alan: şeklin içini kaplayan birim kare sayısı.", sets,
                ["Bir şeklin çevre uzunluğu bütün kenar uzunluklarının toplamıdır. Karenin çevresi 4 × kenar, dikdörtgenin çevresi 2 × (uzun kenar + kısa kenar).",
                 "Alan, bir yüzeyin ne kadar yer kapladığıdır. Yüzeyi kaplayan birim kareleri sayarak ölçeriz. İki yarım kare bir birim kare eder.",
                 "Çevre uzunluk birimiyle (cm, m), alan ise birim kare ile ifade edilir."],
                [("Kenarları 7 cm ve 4 cm olan dikdörtgenin çevresi", ["7 + 4 + 7 + 4"], "22 cm"), ("6 tam ve 2 yarım kareden oluşan şeklin alanı", ["6 + 1"], "7 birim kare")],
                [["Dikdörtgende yalnızca iki kenarı toplamak", "Dört kenarın hepsini topla"], ["Çevre ile alanı karıştırmak", "Çevre kenarlar boyunca, alan şeklin içindedir"],
                 ["Yarım kareleri tam saymak", "İki yarım kare bir tam kare eder"]],
                [("Çevre uzunluğunu hangi araçlarla ölçeriz?", "Cetvel, şerit metre ve mezura ile kenarları ölçüp toplarız."),
                 ("Standart olmayan birimle alan ölçmek ne demektir?", "Defter, kart, kare kâğıt gibi aynı büyüklükteki parçalarla bir yüzeyi kaplayıp saymaktır."),
                 ("Aynı çevreli iki şeklin alanı farklı olabilir mi?", "Evet. Bu konuyu 5. sınıfta daha ayrıntılı inceleyeceksin.")])


# ============================================================ 22. açılar
def ang_pic(d, rot=None):
    rot = ri(0, 60) if rot is None else rot
    s = AU.angle_fig(d, rot, label="işaretli açı")
    return "<div class='qfig'>" + G.lg(s) + "</div>"


KIND = lambda d: "Dar açı" if d < 90 else ("Dik açı" if d == 90 else "Geniş açı")


def u22():
    def tur():
        d = ch([ri(20, 80), 90, ri(100, 165)])
        g = KIND(d)
        return mcq("Şekildeki açı hangi açıdır?" + ang_pic(d), g, ["Dar açı", "Dik açı", "Geniş açı", "Doğru açı"],
                   {"Dar açı": "Dik açıdan küçük: <b>dar açı</b>.", "Dik açı": "Köşedeki kare işareti dik açıyı gösterir: <b>dik açı</b>.",
                    "Geniş açı": "Dik açıdan büyük: <b>geniş açı</b>."}[g])

    def saat():
        h = ri(1, 12)
        m = ch([0, 0, 30])
        hd = (h % 12) * 30 + m / 2.0
        md = m * 6
        d = abs(hd - md)
        d = min(d, 360 - d)
        if d in (0, 180) or abs(d - 90) < 1e-9 and False:
            return None
        g = KIND(d) if d != 90 else "Dik açı"
        if abs(d - 90) < 0.6:
            g = "Dik açı"
        elif d < 90:
            g = "Dar açı"
        else:
            g = "Geniş açı"
        return mcq("Saat %s olduğunda akrep ile yelkovan arasındaki küçük açı hangi açıdır?%s" % (hm(h, m), saat_svg(h, m, 140)),
                   g, ["Dar açı", "Dik açı", "Geniş açı", "Açı oluşmaz"], "Kollar arasındaki açıyı dik açıyla (kare köşesiyle) karşılaştırırız: <b>%s</b>." % low(g))

    def donus():
        S = [("çeyrek dönüş", "Dik açı"), ("yarım dönüş", "Doğru açı (iki dik açı)"), ("tam dönüş", "Tam açı (dört dik açı)"), ("çeyrek dönüşten az", "Dar açı"),
             ("çeyrek dönüşten fazla, yarım dönüşten az", "Geniş açı")]
        t, g = ch(S)
        who = ch(["Bir kapı", "Saatin yelkovanı", "Bir dönme dolap", "Bir musluk", "Bir robot"])
        return mcq("%s %s yapıyor. Oluşan açı hangisidir?" % (who, t), g, [x for _, x in S if x != g], "%s → <b>%s</b>." % (cap(t), low(g)))

    def hangisi():
        kinds = ["Dar açı", "Dik açı", "Geniş açı"]
        want = ch(kinds)
        ds = {"Dar açı": ri(25, 75), "Dik açı": 90, "Geniş açı": ri(105, 160)}
        others = [k for k in kinds if k != want]
        opts = [ds[want], ds[others[0]], ds[others[1]], {"Dar açı": ri(25, 75), "Dik açı": ri(100, 160), "Geniş açı": ri(20, 70)}[want] if want != "Dik açı" else ri(110, 160)]
        if want == "Dik açı":
            opts[3] = ri(20, 70)
        if len([o for o in opts if KIND(o) == want]) != 1:
            return None
        order = sh(range(4))
        svgs = [AU.angle_fig(opts[i], ri(0, 40), label="açı") for i in order]
        k = order.index(0)
        return mcq("Hangisi %s gösterir?" % {"Dar açı": "bir dar açıyı", "Dik açı": "bir dik açıyı", "Geniş açı": "bir geniş açıyı"}[want] + row4(svgs), "ABCD"[k],
                   [x for i, x in enumerate("ABCD") if i != k], "Dik açıyla karşılaştırırız: <b>%s</b>." % "ABCD"[k])

    def sekilde():
        S = [("Bir karede", "4", "dik açı"), ("Bir dikdörtgende", "4", "dik açı"), ("Bir eşkenar üçgende", "3", "dar açı"),
             ("Bir dik üçgende", "1", "dik açı"), ("Bir dik üçgende", "2", "dar açı")]
        a, g, k = ch(S)
        return mcq("%s kaç tane %s vardır?" % (a, k), g, [x for x in ("0", "1", "2", "3", "4") if x != g], "%s <b>%s</b> %s vardır." % (a, g, k))

    sets = [("Açı çeşitleri", [(tur, 20)]),
            ("Hangisi?", [(hangisi, 20)]),
            ("Saatte açılar", [(saat, 18), (tur, 2)]),
            ("Dönüş ve açı", [(donus, 16), (sekilde, 4)]),
            ("Karışık sorular", [(tur, 10), (hangisi, 8), (saat, 2)])]
    return unit("acilar", "G", "MAT.4.3.5, MAT.4.3.6, MAT.4.3.7", 22, "Açılar: Dar, Dik ve Geniş Açı", "Açılar",
                "Açıyı günlük hayattan örneklerle dönüş miktarı olarak yorumlar; standart açı ölçme araçlarına duyulan ihtiyacı değerlendirir; açıları dik açıyı referans alarak dar ve geniş açı olarak sınıflandırır.",
                "4. sınıf açılar çalışma kâğıdı: dar, dik ve geniş açı, şekillerdeki açılar, saatte akrep ile yelkovan arasındaki açı, dönüş ve açı. 100 soru ve cevap anahtarı.",
                "Dik açıdan küçük dar, büyük geniş açı", "Çeyrek dönüş bir dik açıdır; dik açıyla karşılaştır.", sets,
                ["Açı, ortak bir noktadan çıkan iki ışının oluşturduğu şekildir; bir kolun ne kadar döndüğünü gösterir.",
                 "Dik açı çeyrek dönüştür; kâğıdın köşesi bir dik açıdır. Dik açıdan küçük açılar dar açı, dik açıdan büyük açılar geniş açıdır.",
                 "Açıları karşılaştırırken kolların uzunluğuna değil, kollar arasındaki açıklığa bakarız."],
                [("Saat 3.00", ["Akrep 3, yelkovan 12", "Çeyrek dönüş"], "dik açı"), ("Saat 5.00", ["Kollar arası çeyrek dönüşten fazla"], "geniş açı")],
                [["Kolları uzun olan açıyı büyük sanmak", "Açının büyüklüğü kollar arasındaki açıklıktır"], ["Döndürülmüş dik açıyı tanımamak", "Kare köşe işareti dik açıyı gösterir"],
                 ["Geniş açıyı dik açıyla karıştırmak", "Kâğıdın köşesini yerleştirip karşılaştır"]],
                [("Açıyı neden standart araçla ölçeriz?", "El karışı ya da kâğıt köşesi gibi birimler herkeste farklıdır. Açıölçer herkese aynı sonucu verir."),
                 ("Günlük hayatta dik açı nerede vardır?", "Kitabın, masanın, kapının ve pencerenin köşelerinde."),
                 ("Yarım dönüş hangi açıyı oluşturur?", "İki dik açı kadar, yani doğru açıyı oluşturur.")])


# ============================================================ 23. simetri
GRID_N = 8
CELL = 20


def sym_grid(cells, axis, pts=None, n=GRID_N, col="#a8d5ba"):
    """axis: ('v', k) → x = k çizgisi; ('h', k) → y = k çizgisi"""
    W = H = n * CELL + 12
    s = []
    for i in range(n + 1):
        s.append(line(6 + i * CELL, 6, 6 + i * CELL, 6 + n * CELL, "#d5dde3", 1) + line(6, 6 + i * CELL, 6 + n * CELL, 6 + i * CELL, "#d5dde3", 1))
    for x, y in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>" % (6 + x * CELL, 6 + y * CELL, CELL, CELL, col, GREEN))
    if axis[0] == "v":
        s.append(line(6 + axis[1] * CELL, 2, 6 + axis[1] * CELL, H - 2, RED, 2.4, " stroke-dasharray='6 4'"))
    else:
        s.append(line(2, 6 + axis[1] * CELL, W - 2, 6 + axis[1] * CELL, RED, 2.4, " stroke-dasharray='6 4'"))
    for (x, y, lab) in (pts or []):
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (6 + x * CELL, 6 + y * CELL, INK) + text(6 + x * CELL + 9, 6 + y * CELL - 6, lab, 13))
    return G.wrap(W, H, "".join(s), "kareli kâğıtta şekil ve simetri doğrusu")


def reflect(cells, axis):
    k = axis[1]
    if axis[0] == "v":
        return sorted((2 * k - 1 - x, y) for x, y in cells)
    return sorted((x, 2 * k - 1 - y) for x, y in cells)


def blob(axis):
    k = axis[1]
    cells = set()
    for _ in range(40):
        if len(cells) >= ri(4, 6):
            break
        if not cells:
            c = (k - 1, ri(2, 5)) if axis[0] == "v" else (ri(2, 5), k - 1)
        else:
            b = ch(sorted(cells))
            d = ch([(1, 0), (-1, 0), (0, 1), (0, -1)])
            c = (b[0] + d[0], b[1] + d[1])
        x, y = c
        if axis[0] == "v" and not (k - 3 <= x <= k - 1 and 0 <= y < GRID_N):
            continue
        if axis[0] == "h" and not (k - 3 <= y <= k - 1 and 0 <= x < GRID_N):
            continue
        cells.add(c)
    return sorted(cells)


def u23():
    def yansima():
        axis = (ch(["v", "h"]), 4)
        h = blob(axis)
        good = sorted(h + reflect(h, axis))
        k = axis[1]
        if axis[0] == "v":
            tr = sorted(h + [(x + 3, y) for x, y in h])
        else:
            tr = sorted(h + [(x, y + 3) for x, y in h])
        other = ("h", 4) if axis[0] == "v" else ("v", 4)
        wr = sorted(h + [c for c in reflect(h, axis)][:-1] + [(reflect(h, axis)[-1][0] + (1 if axis[0] == "h" else 0), reflect(h, axis)[-1][1] + (1 if axis[0] == "v" else 0))])
        rot = sorted(h + [(2 * k - 1 - x, 2 * k - 1 - y) if axis[0] == "v" else (2 * k - 1 - x, 2 * k - 1 - y) for x, y in h])
        opts = [good, tr, wr, rot]
        if len({tuple(o) for o in opts}) < 4 or any(not all(0 <= x < GRID_N and 0 <= y < GRID_N for x, y in o) for o in opts):
            return None
        order = sh(range(4))
        svgs = [sym_grid(opts[i], axis) for i in order]
        q = "Kırmızı doğru simetri doğrusudur. Şeklin simetriği doğru çizilmiş olan hangisidir?" + row4(svgs)
        j = order.index(0)
        return mcq(q, "ABCD"[j], [x for i, x in enumerate("ABCD") if i != j], "Her kare, simetri doğrusuna eşit uzaklıkta karşı tarafa çizilir: <b>%s</b>." % "ABCD"[j])

    def nokta():
        axis = (ch(["v", "h"]), ri(3, 5))
        k = axis[1]
        if axis[0] == "v":
            x, y = ri(max(0, k - 3), k - 1), ri(1, 7)
            img = (2 * k - x, y)
            cands = [img, (img[0] + 1, y), (img[0] - 1 if img[0] - 1 > k else img[0] + 2, y), (img[0], y + 1 if y < 7 else y - 1)]
        else:
            x, y = ri(1, 7), ri(max(0, k - 3), k - 1)
            img = (x, 2 * k - y)
            cands = [img, (x, img[1] + 1), (x, img[1] - 1 if img[1] - 1 > k else img[1] + 2), (x + 1 if x < 7 else x - 1, img[1])]
        if any(not (0 <= a <= 8 and 0 <= b <= 8) for a, b in cands) or len(set(cands)) < 4:
            return None
        labs = sh(["A", "B", "C", "D"])
        pts = [(x, y, "P")] + [(a, b, labs[i]) for i, (a, b) in enumerate(cands)]
        return mcq("P noktasının kırmızı doğruya göre simetriği hangi noktadır?" + sym_grid([], axis, pts).replace("kareli kâğıtta şekil", "kareli kâğıtta noktalar"),
                   labs[0], labs[1:], "P noktası doğruya %d birim uzaklıkta. Simetriği karşı tarafta yine %d birim uzaklıkta: <b>%s</b>." % (abs((x if axis[0] == "v" else y) - k), abs((x if axis[0] == "v" else y) - k), labs[0]))

    def kac_kare():
        axis = (ch(["v", "h"]), 4)
        h = blob(axis)
        n = len(h)
        return mcq("Şeklin simetrisi çizilip tamamlanırsa tüm şekil kaç kareden oluşur?" + sym_grid(h, axis), str(2 * n), [str(n), str(2 * n + 1), str(2 * n - 2)],
                   "Simetrik şekilde her karenin bir eşi vardır: %d × 2 = <b>%d</b>." % (n, 2 * n))

    def dogru_mu():
        S = [("dikdörtgen", "köşegen", False), ("dikdörtgen", "kısa kenarların ortalarını birleştiren doğru", True), ("kare", "köşegen", True),
             ("ikizkenar üçgen", "tepe noktasından tabanın ortasına inen doğru", True), ("çeşitkenar üçgen", "bir köşeden karşı kenarın ortasına çizilen doğru", False),
             ("daire", "merkezden geçen her doğru", True), ("eşkenar üçgen", "bir köşeden karşı kenarın ortasına inen doğru", True),
             ("kare", "iki karşılıklı kenarın ortalarını birleştiren doğru", True), ("dikdörtgen", "uzun kenarların ortalarını birleştiren doğru", True),
             ("düzgün altıgen", "karşılıklı iki köşeyi birleştiren doğru", True), ("dikdörtgen", "bir köşeden karşı kenarın ortasına çizilen doğru", False),
             ("kare", "bir köşeden karşı kenarın ortasına çizilen doğru", False), ("eşkenar üçgen", "bir kenara paralel çizilen doğru", False)]
        a, b, ok = ch(S)
        g = "Evet" if ok else "Hayır"
        return mcq("Bir %s için %s bir simetri doğrusu mudur?" % (a, b), g, ["Hayır" if ok else "Evet", "Bazen", "Bilinemez"],
                   "Şekil bu doğrudan katlandığında iki parça tam üst üste %s: <b>%s</b>." % ("gelir" if ok else "gelmez", low(g)))

    def ayna():
        S = [("Bir öğrenci aynanın karşısında sağ elini kaldırıyor. Aynadaki görüntüsü hangi elini kaldırmış gibi görünür?", "Sol elini", ["Sağ elini", "İki elini", "Hiçbirini"]),
             ("Aynaya 3 adım uzaklıkta duran bir çocuğun görüntüsü aynanın arkasında kaç adım uzakta görünür?", "3 adım", ["6 adım", "1 adım", "0 adım"]),
             ("Ayna simetrisinde şekil ile görüntüsünün büyüklüğü nasıldır?", "Aynıdır", ["Görüntü daha büyüktür", "Görüntü daha küçüktür", "Değişir"]),
             ("Ayna, şekil ile görüntüsü arasında hangi görevi görür?", "Simetri doğrusu", ["Kenar", "Köşe", "Alan"]),
             ("Bir kelebeğin kanatları gövdesine göre nasıldır?", "Simetriktir", ["Simetrik değildir", "Farklı büyüklüktedir", "Üst üste gelmez"]),
             ("Aynaya 5 cm uzaklıktaki bir noktanın görüntüsü noktadan kaç cm uzaktadır?", "10 cm", ["5 cm", "15 cm", "0 cm"])]
        q, g, w = ch(S)
        return mcq(q, g, w, "Ayna simetrisinde görüntü aynaya, cisimle aynı uzaklıkta ve aynı büyüklükte oluşur; sağ ve sol yer değiştirir: <b>%s</b>." % low(g))

    sets = [("Simetriğini çizme", [(yansima, 20)]),
            ("Noktanın simetriği", [(nokta, 20)]),
            ("Simetri doğrusu", [(dogru_mu, 10), (kac_kare, 10)]),
            ("Simetrik şekli tamamlama", [(kac_kare, 10), (yansima, 10)]),
            ("Ayna simetrisi", [(ayna, 6), (nokta, 11), (dogru_mu, 3)])]
    return unit("simetri", "G", "MAT.4.3.8, MAT.4.3.9", 23, "Doğruya Göre Simetri ve Ayna Simetrisi", "Simetri",
                "Geometrik şekil ve modellerden yararlanarak doğruya göre simetriyi yorumlar; bir şeklin doğruya göre simetriğini oluşturur.",
                "4. sınıf simetri çalışma kâğıdı: ayna simetrisi, kareli kâğıtta simetriğini çizme, noktanın simetriği, şekillerin simetri doğruları. 100 soru ve cevap anahtarı.",
                "Simetrik nokta doğruya eşit uzaklıktadır", "Şekil katlanınca iki yarısı üst üste gelir.", sets,
                ["Bir şekli bir doğru boyunca katladığımızda iki parça tam üst üste geliyorsa bu doğru simetri doğrusudur.",
                 "Ayna, simetri doğrusu gibi davranır: görüntü aynaya cisimle aynı uzaklıktadır ve aynı büyüklüktedir; sağ ve sol yer değiştirir.",
                 "Kareli kâğıtta simetriğini çizerken her köşenin doğruya kaç kare uzakta olduğunu sayarız ve karşı tarafa aynı uzaklıkta işaretleriz."],
                [("Doğrunun 2 kare solundaki nokta", ["Doğrunun 2 kare sağına"], "simetriği"), ("Dikdörtgenin köşegeni", ["Katlayınca parçalar üst üste gelmez"], "simetri doğrusu değildir")],
                [["Şekli kaydırmak (öteleme)", "Simetrik çizimde şekil ters döner, doğruya eşit uzaklıkta olur"], ["Dikdörtgenin köşegenini simetri doğrusu sanmak", "Köşegen boyunca katlanınca parçalar çakışmaz"],
                 ["Uzaklıkları yanlış saymak", "Kareleri simetri doğrusundan başlayarak say"]],
                [("Simetri doğrusu her şekilde var mıdır?", "Hayır. Çeşitkenar üçgen ya da F harfi gibi şekillerin simetri doğrusu yoktur."),
                 ("Bir şeklin birden çok simetri doğrusu olabilir mi?", "Evet. Karenin 4, dikdörtgenin 2, eşkenar üçgenin 3 simetri doğrusu vardır."),
                 ("Simetriyi günlük hayatta nerede görürüz?", "Kelebek kanatlarında, yapraklarda, binalarda, halı ve çini desenlerinde.")])


# ============================================================ 24. olasılık
COL = [("kırmızı", "#e15759"), ("mavi", "#4e79a7"), ("yeşil", "#59a14f"), ("sarı", "#f2c94c")]


def torba(cnt):
    s = ["<path d='M30 40 Q20 150 110 160 Q200 150 190 40 Z' fill='#f3ead8' stroke='%s' stroke-width='2'/>" % INK]
    pts = [(55 + (i % 6) * 22, 62 + (i // 6) * 22) for i in range(24)]
    items = [c for c, n in cnt for _ in range(n)]
    order = sh(range(len(items)))
    for i, k in enumerate(order):
        x, y = pts[i]
        s.append("<circle cx='%d' cy='%d' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x, y, dict(COL)[items[k]], INK))
    return G.wrap(220, 170, "".join(s), "torbadaki toplar: " + ", ".join("%d %s" % (n, c) for c, n in cnt))


def u24():
    def torba_q():
        cs = sh(COL)[:ri(1, 3)]
        cnt = [(c, ri(1, 6)) for c, _ in cs]
        names = [c for c, _ in cnt]
        k = ri(0, 2)
        if k == 0:
            c = ch([x for x, _ in COL if x not in names])
            g = "İmkânsız"
            q = "Torbadan bakmadan bir top çekiliyor. Çekilen topun %s olması nasıl bir olaydır?" % c
            e = "Torbada %s top yok: <b>imkânsız</b>." % c
        elif k == 1 and len(cnt) == 1:
            c = names[0]
            g = "Kesin"
            q = "Torbadan bakmadan bir top çekiliyor. Çekilen topun %s olması nasıl bir olaydır?" % c
            e = "Torbadaki bütün toplar %s: <b>kesin</b>." % c
        else:
            if len(cnt) == 1:
                return None
            c = ch(names)
            g = "Olabilir"
            q = "Torbadan bakmadan bir top çekiliyor. Çekilen topun %s olması nasıl bir olaydır?" % c
            e = "Torbada %s top da başka renkte top da var: <b>olabilir</b>." % c
        return mcq(q + torba(cnt), g, ["İmkânsız", "Olabilir", "Kesin", "Daha önce olmuş"], e)

    def gunluk():
        S = [("Yarın güneşin doğması", "Kesin"), ("Bir zar atıldığında 7 gelmesi", "İmkânsız"), ("Bir zar atıldığında 4 gelmesi", "Olabilir"),
             ("Bir yazı tura atıldığında yazı gelmesi", "Olabilir"), ("Bir haftanın 8 gün olması", "İmkânsız"), ("Pazartesiden sonra salı gelmesi", "Kesin"),
             ("Yarın yağmur yağması", "Olabilir"), ("Bir kedinin uçarak okula gelmesi", "İmkânsız"), ("Suyun 0 derecede donması", "Kesin"),
             ("Ocak ayından sonra şubat gelmesi", "Kesin"), ("Bir zar atıldığında çift sayı gelmesi", "Olabilir"), ("Bir yılın 13 ay olması", "İmkânsız"),
             ("Okulda yeni bir arkadaş edinmek", "Olabilir"), ("Bir çantadaki 5 kırmızı kalemden birini çekince kırmızı gelmesi", "Kesin"),
             ("Bir zar atıldığında 0 gelmesi", "İmkânsız"), ("Bugün sınıfta birinin doğum günü olması", "Olabilir"),
             ("Bir zar atıldığında 6’dan küçük ya da 6’ya eşit bir sayı gelmesi", "Kesin"), ("Bir zar atıldığında 3 gelmesi", "Olabilir"),
             ("Yazı tura atıldığında hem yazı hem tura gelmesi", "İmkânsız"), ("Bir ağacın bir günde gökdelen kadar uzaması", "İmkânsız"),
             ("Yarın okulda müzik dersi olması", "Olabilir"), ("Bir saatin 60 dakika olması", "Kesin"), ("Bir üçgenin 4 kenarı olması", "İmkânsız"),
             ("Bir dakikanın 60 saniye olması", "Kesin"), ("Bir arkadaşının seninle aynı ayda doğmuş olması", "Olabilir"),
             ("Bir balığın ağaca tırmanması", "İmkânsız"), ("Bir kutudaki yeşil ve mavi kalemlerden birini çekince yeşil gelmesi", "Olabilir"),
             ("Bir yılın 12 ay olması", "Kesin")]
        t, g = ch(S)
        return mcq("“%s” nasıl bir olaydır?" % t, g, ["İmkânsız", "Olabilir", "Kesin", "Her gün olur"],
                   {"Kesin": "Mutlaka olur: <b>kesin</b>.", "İmkânsız": "Hiçbir zaman olmaz: <b>imkânsız</b>.", "Olabilir": "Olabilir de olmayabilir de: <b>olabilir</b>."}[g])

    def hangisi():
        k = ch(["İmkânsız", "Kesin", "Olabilir"])
        I = ["Zar atınca 8 gelmesi", "Bir günün 30 saat olması", "Ayın kare olması", "Bir kalemin kendi kendine yazı yazması"]
        Ke = ["Kışın ardından ilkbaharın gelmesi", "Cumadan sonra cumartesi gelmesi", "Bir saatin 60 dakika olması", "Bir üçgenin 3 köşesi olması"]
        O = ["Zar atınca 2 gelmesi", "Bugün kar yağması", "Yazı tura atınca tura gelmesi", "Bir maçta takımımızın kazanması"]
        pool = {"İmkânsız": I, "Kesin": Ke, "Olabilir": O}
        g = ch(pool[k])
        others = [y for y in pool if y != k]
        w = [ch(pool[others[0]]), ch(pool[others[1]]), ch(pool[others[ri(0, 1)]])]
        if len(set(w)) < 3:
            return None
        cards = sh([g] + w)
        nm = G.K.next()
        return mcq("%s dört karta şu olayları yazdı: %s. Hangisi <b>%s</b> bir olaydır?" % (nm, "; ".join(cards), low(k)), g, w,
                   "<b>%s</b>: %s." % (g, low(k)))

    def degistir():
        a = ri(2, 6)
        c1, c2 = sh([c for c, _ in COL])[:2]
        q = "Bir torbada yalnızca %d %s top var. Çekilen topun %s olmasını “olabilir” yapmak için ne yapılmalıdır?" % (a, c1, c2)
        g = "Torbaya %s top eklemek" % c2
        return mcq(q, g, ["Torbaya %s top eklemek" % c1, "Torbadan bir %s top çıkarmak" % c1, "Hiçbir şey yapmamak"],
                   "Şu an %s top çekmek imkânsız. Torbaya %s top eklersek <b>olabilir</b> olur." % (c2, c2))

    def daha_cok():
        a, b = ri(1, 4), ri(5, 9)
        c1, c2 = sh([c for c, _ in COL])[:2]
        cnt = [(c1, a), (c2, b)]
        return mcq("Torbadan bakmadan bir top çekiliyor. Hangi renkte top gelme olasılığı daha fazladır?" + torba(cnt), cap(c2), [cap(c1), "İkisi eşit", "Bilinemez"],
                   "%s top daha çok (%d &gt; %d): <b>%s</b>." % (cap(c2), b, a, c2))

    sets = [("Torbadan top çekme", [(torba_q, 20)]),
            ("Günlük hayatta olaylar", [(gunluk, 20)]),
            ("Hangisi?", [(hangisi, 20)]),
            ("Olayı değiştirme", [(degistir, 10), (daha_cok, 10)]),
            ("Karışık sorular", [(torba_q, 8), (gunluk, 6), (daha_cok, 6)])]
    return unit("imkansiz-olabilir-kesin", "OV", "MAT.4.4.1", 24, "Olasılık: İmkânsız, Olabilir ve Kesin Olaylar", "İmkânsız, Olabilir, Kesin",
                "Günlük hayattaki bir olayın gerçekleşme durumunun imkânsız, olabilir veya kesin olduğunu belirler.",
                "4. sınıf olasılık çalışma kâğıdı: imkânsız, olabilir ve kesin olaylar, torbadan top çekme, zar ve yazı tura, günlük hayattan olaylar. 100 soru ve cevap anahtarı.",
                "İmkânsız, olabilir, kesin", "Kesin mutlaka olur, imkânsız hiç olmaz.", sets,
                ["Bir olay hiçbir zaman gerçekleşemiyorsa imkânsız, mutlaka gerçekleşiyorsa kesin, gerçekleşebilir de gerçekleşmeyebilir de ise olabilir.",
                 "Torbadan top çekerken torbadaki renklere bakarız: torbada olmayan renk imkânsız, tek renk varsa o renk kesin.",
                 "Bir rengin topu daha çoksa o rengin gelme olasılığı daha fazladır."],
                [("Zar atınca 7 gelmesi", ["Zarda 1’den 6’ya kadar sayılar var"], "imkânsız"), ("Yalnızca mavi toplar olan torbadan mavi top çekmek", ["Bütün toplar mavi"], "kesin")],
                [["Olabilir ile kesini karıştırmak", "Kesin olay her zaman olur; olabilir olay bazen olur"], ["Az olan rengi imkânsız sanmak", "Torbada bir tane bile varsa olabilir"],
                 ["Daha önce olmamış her olayı imkânsız sanmak", "İmkânsız olay hiçbir zaman olamaz"]],
                [("Olasılık nedir?", "Bir olayın gerçekleşme şansıdır. 4. sınıfta olayları imkânsız, olabilir ve kesin diye sınıflandırırız."),
                 ("Yarın yağmur yağması neden “olabilir”dir?", "Yağabilir de yağmayabilir de; kesin olarak bilemeyiz."),
                 ("Bir olayın olasılığını nasıl değiştirebilirim?", "Torbaya top ekleyip çıkararak ya da kuralları değiştirerek.")])


# ============================================================ 25. veri
KONU = [("En sevilen meyve", ["Elma", "Muz", "Çilek", "Kiraz", "Portakal"]), ("En sevilen spor", ["Futbol", "Voleybol", "Basketbol", "Yüzme", "Tenis"]),
        ("Okula geliş şekli", ["Yürüyerek", "Servisle", "Otobüsle", "Arabayla", "Bisikletle"]), ("En sevilen renk", ["Mavi", "Kırmızı", "Yeşil", "Mor", "Sarı"]),
        ("Evcil hayvan", ["Kedi", "Köpek", "Kuş", "Balık", "Tavşan"]), ("En sevilen ders", ["Matematik", "Türkçe", "Fen", "Müzik", "Beden eğitimi"])]


def u25():
    def veri(mx=12, n=None):
        t, cats = ch(KONU)
        n = n or ri(3, 5)
        cats = sh(cats)[:n]
        vals = [ri(2, mx) for _ in cats]
        if len(set(vals)) < len(vals):
            return None
        return t, cats, vals

    def soru(t, cats, vals, pic, intro):
        k = ri(0, 4)
        i = ri(0, len(cats) - 1)
        if k == 0:
            g = cats[vals.index(max(vals))]
            return mcq(intro + pic + "En çok tercih edilen hangisidir?", g, [c for c in cats if c != g] + ["Hepsi eşit"], "En büyük sıklık %d: <b>%s</b>." % (max(vals), g))
        if k == 1:
            g = cats[vals.index(min(vals))]
            return mcq(intro + pic + "En az tercih edilen hangisidir?", g, [c for c in cats if c != g] + ["Hepsi eşit"], "En küçük sıklık %d: <b>%s</b>." % (min(vals), g))
        if k == 2:
            s = sum(vals)
            return mcq(intro + pic + "Araştırmaya toplam kaç öğrenci katılmıştır?", str(s), [str(s + 2), str(s - 1), str(max(vals) * len(vals))], "Bütün sıklıklar toplanır: <b>%d</b>." % s)
        if k == 3:
            a, b = vals.index(max(vals)), vals.index(min(vals))
            d = vals[a] - vals[b]
            return mcq(intro + pic + "%s seçen öğrenci sayısı %s seçenlerden kaç fazladır?" % (cats[a], cats[b]), str(d), [str(d + 1), str(vals[a] + vals[b]), str(d - 1) if d > 1 else str(d + 2)],
                       "%d − %d = <b>%d</b>." % (vals[a], vals[b], d))
        return mcq(intro + pic + "%s seçen kaç öğrenci vardır?" % cats[i], str(vals[i]), [str(vals[i] + 1), str(vals[i] - 1), str(vals[(i + 1) % len(vals)])],
                   "%s seçen <b>%d</b> öğrenci var." % (cats[i], vals[i]))

    def tablo():
        d = veri(15)
        if not d:
            return None
        t, cats, vals = d
        return soru(t, cats, vals, freq_table(t, cats, vals), "“%s” araştırmasının sıklık tablosu:" % t)

    def grafik():
        d = veri(12)
        if not d:
            return None
        t, cats, vals = d
        return soru(t, cats, vals, sutun_grafigi(list(zip(cats, vals)), "öğrenci"), "“%s” araştırmasının sütun grafiği:" % t)

    def cetele_q():
        d = veri(14, 3)
        if not d:
            return None
        t, cats, vals = d
        tab = ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>%s</th><th>Çetele</th></tr></thead><tbody>%s</tbody></table>"
               % (t, "".join("<tr><td>%s</td><td>%s</td></tr>" % (c, cetele(v).replace("<div class='qfig'>", "").replace("</div>", "")) for c, v in zip(cats, vals))))
        return soru(t, cats, vals, tab, "“%s” araştırmasının çetele tablosu:" % t)

    def iki_grup():
        t, cats = ch(KONU)
        cats = sh(cats)[:3]
        a = [ri(2, 9) for _ in cats]
        b = [ri(2, 9) for _ in cats]
        tab = ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>%s</th><th>4-A</th><th>4-B</th></tr></thead><tbody>%s</tbody></table>"
               % (t, "".join("<tr><td>%s</td><td style='text-align:center'>%d</td><td style='text-align:center'>%d</td></tr>" % (c, x, y) for c, x, y in zip(cats, a, b))))
        k = ri(0, 2)
        if k == 0:
            tot = [x + y for x, y in zip(a, b)]
            if tot.count(max(tot)) > 1:
                return None
            g = cats[tot.index(max(tot))]
            return mcq("İki sınıfta yapılan “%s” araştırmasının sonuçları:%sİki sınıf birlikte düşünüldüğünde en çok tercih edilen hangisidir?" % (t, tab), g, [c for c in cats if c != g] + ["Bilinemez"],
                       "Toplamlar: %s. En büyük: <b>%s</b>." % (", ".join("%s %d" % (c, x) for c, x in zip(cats, tot)), g))
        if k == 1:
            sa, sb = sum(a), sum(b)
            if sa == sb:
                return None
            g = "4-A" if sa > sb else "4-B"
            return mcq("İki sınıfta yapılan “%s” araştırmasının sonuçları:%sHangi sınıftan daha çok öğrenci araştırmaya katılmıştır?" % (t, tab), g, ["4-B" if g == "4-A" else "4-A", "Eşit sayıda", "Bilinemez"],
                       "4-A: %d, 4-B: %d öğrenci: <b>%s</b>." % (sa, sb, g))
        i = ri(0, 2)
        d = abs(a[i] - b[i])
        if d == 0:
            return None
        return mcq("İki sınıfta yapılan “%s” araştırmasının sonuçları:%s%s seçenlerin sayısı iki sınıf arasında kaç farklıdır?" % (t, tab, cats[i]), str(d), [str(a[i] + b[i]), str(d + 1), str(max(a[i], b[i]))],
                   "%d ile %d arasındaki fark <b>%d</b>." % (a[i], b[i], d))

    def nokta_q():
        t, cats = ch(KONU)
        n = ri(8, 14)
        data = [ri(1, 6) for _ in range(n)]
        lo, hi = 1, 6
        k = ri(0, 2)
        pic = dot_plot(lo, hi, data, "nokta grafiği")
        title = "Bir sınıftaki öğrencilerin kardeş sayıları (1–6) nokta grafiğinde gösterilmiştir."
        if k == 0:
            v = ri(1, 6)
            return mcq(title + pic + "%d kardeşi olan kaç öğrenci vardır?" % v, str(data.count(v)), [str(data.count(v) + 1), str(v), str(n - data.count(v))],
                       "%d sayısının üstündeki noktaları sayarız: <b>%d</b>." % (v, data.count(v)))
        if k == 1:
            return mcq(title + pic + "Grafikte kaç öğrencinin verisi vardır?", str(n), [str(n + 1), str(n - 1), "6"], "Bütün noktaları sayarız: <b>%d</b>." % n)
        cnt = {v: data.count(v) for v in range(1, 7)}
        m = max(cnt.values())
        if list(cnt.values()).count(m) > 1:
            return None
        g = [v for v in cnt if cnt[v] == m][0]
        return mcq(title + pic + "Öğrencilerin çoğunun kaç kardeşi vardır?", str(g), [str(x) for x in range(1, 7) if x != g], "En yüksek nokta sütunu %d: <b>%d</b>." % (g, g))

    sets = [("Sıklık tablosu", [(tablo, 20)]),
            ("Çetele tablosu", [(cetele_q, 20)]),
            ("Sütun grafiği", [(grafik, 20)]),
            ("Nokta grafiği", [(nokta_q, 20)]),
            ("İki grubu karşılaştırma", [(iki_grup, 20)])]
    return unit("veri-toplama-ve-grafikler", "OV", "MAT.4.4.2", 25, "Veri Toplama, Tablo ve Grafikler", "Veri ve Grafikler",
                "En fazla iki gruba ait kategorik veya sayıya dayalı veriyle çalışır; veriyi çetele, sıklık tablosu, sütun ve nokta grafiğiyle gösterir ve veriye dayalı karar verir.",
                "4. sınıf veri toplama ve grafikler çalışma kâğıdı: çetele ve sıklık tablosu, sütun grafiği, nokta grafiği, iki grubun verilerini karşılaştırma. 100 soru ve cevap anahtarı.",
                "Veriyi tabloya, sonra grafiğe dök", "Grafikte en yüksek sütun en çok tercihi gösterir.", sets,
                ["Bir araştırmada önce soru belirlenir, sonra veri toplanır. Veriyi çetele ve sıklık tablosuyla düzenleriz.",
                 "Sütun grafiğinde her sütunun yüksekliği o seçeneğin sıklığını gösterir. Nokta grafiğinde her nokta bir veriyi gösterir.",
                 "İki grubu karşılaştırırken aynı seçeneğin değerlerine bakar, toplamları ve farkları buluruz."],
                [("Elma 8, Muz 5, Çilek 11", ["En çok: Çilek", "Toplam 8 + 5 + 11"], "24 öğrenci"), ("Çetelede ||||  ||||  ||", ["5 + 5 + 2"], "12")],
                [["Çetelede beşlik demeti 4 saymak", "Çaprazlı demet 5’tir"], ["Grafiğin ölçeğini okumamak", "Eksendeki sayılara bakarak oku"],
                 ["Farkı bulurken toplamak", "Ne kadar fazla sorusu çıkarma ister"]],
                [("Çetele neden kullanılır?", "Veri toplarken her yanıtı bir çizgiyle hızlıca kaydetmek için. Beşinci çizgi diğer dördünün üstüne çapraz çizilir."),
                 ("Hangi grafik ne zaman kullanılır?", "Kategorileri karşılaştırmak için sütun grafiği, sayısal veriyi göstermek için nokta grafiği kullanışlıdır."),
                 ("Veriye dayalı karar ne demektir?", "Topladığımız verilere bakarak seçim yapmaktır; ör. sınıf gezisini en çok tercih edilen yere düzenlemek.")])


UNITS = [u19, u20, u21, u22, u23, u24, u25]
