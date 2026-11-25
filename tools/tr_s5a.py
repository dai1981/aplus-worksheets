# -*- coding: utf-8 -*-
"""Türkiye 5. sınıf (Maarif Modeli, Ortaokul Matematik 2026): Geometrik Şekiller, Sayılar ve Nicelikler (1), Geometrik Nicelikler — 1〜10 単元。"""
import math
import random as _r
import tr_g as G
from tr_g import unit, cap, num, oku, mcq, M, wrap, text, line, poly, grid_shape, circle_fig, NB, INK, GREEN, FILL, RED, BLUE
from tr_common import low
import gen_au_maths_y5_angles as AU
from gen_au_maths_y5_angles import Pic, pol

AU.random = _r
O = (0.0, 0.0)


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def fig(svg, lab="geometrik şekil"):
    svg = svg.replace("aria-label='protractor measuring an angle'", "aria-label='açıölçer'").replace("aria-label='marked angle'", "aria-label='%s'" % lab)
    return "<div class='qfig'>" + G.lg(svg) + "</div>"


def row4(svgs, caps=("A", "B", "C", "D")):
    return "<div class='qfig'>" + "".join("<span style='display:inline-block;margin:4px 10px;text-align:center;vertical-align:top'><b>%s</b><br>%s</span>"
                                          % (c, s.replace("<div class='qfig'>", "").replace("</div>", "")) for c, s in zip(caps, svgs)) + "</div>"


# ------------------------------------------------------------ çizimler: doğru, ışın, doğru parçası
def arrow(x, y, d):
    return "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>" % (x, y, x - 10 * d, y - 6, x - 10 * d, y + 6, GREEN)


def linefig(kind, a="A", b="B", tilt=0):
    """kind: 'dp' doğru parçası, 'isin' ışın (A başlangıç), 'dogru' doğru"""
    W, H = 260, 70
    x1, x2, y = 50, 210, 40
    s = []
    lx1 = x1 if kind in ("dp", "isin") else 14
    lx2 = x2 if kind == "dp" else 246
    s.append(line(lx1, y, lx2, y, GREEN, 3))
    if kind in ("isin", "dogru"):
        s.append(arrow(lx2, y, 1))
    if kind == "dogru":
        s.append(arrow(lx1, y, -1))
    for x, t in ((x1, a), (x2, b)):
        s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (x, y, INK) + text(x, y - 12, t, 15))
    return G.wrap(W, H, "".join(s), {"dp": "doğru parçası", "isin": "ışın", "dogru": "doğru"}[kind] + " " + a + b)


def kesisen(d, texts, L=80, label="kesişen iki doğru"):
    """O’da kesişen iki doğru: biri 0–180°, öbürü d–(d+180)°. texts: {0..3: metin} bölge 0 = (0, d), 1 = (d, 180), 2 = (180, 180 + d), 3 = (180 + d, 360)"""
    P = Pic()
    for a_ in (0, 180, d, d + 180):
        P.line(O, pol(O, L, a_))
    P.dot(O)
    edges = [(0, d), (d, 180), (180, 180 + d), (180 + d, 360)]
    for k, t in texts.items():
        a, b = edges[k]
        P.mark(O, pol(O, L, a), pol(O, L, b), b - a, t, ccw=True, r=22)
    return fig(P.svg(label), label)


def rays(dirs, texts, L=85, base=False, label="açılar"):
    """O’dan çıkan ışınlar. dirs artan açılar; texts {(i, j): metin} i. ve j. ışın arasındaki açı. base: 0 ve 180 doğrusu"""
    P = Pic()
    for d in dirs:
        P.line(O, pol(O, L, d))
    P.dot(O)
    for (i, j), t in texts.items():
        v = dirs[j] - dirs[i]
        if v == 90 and t is None:
            P.mark(O, pol(O, L, dirs[i]), pol(O, L, dirs[j]), 90, kind="right", ccw=True)
        else:
            P.mark(O, pol(O, L, dirs[i]), pol(O, L, dirs[j]), v, t, ccw=True, r=20 if v > 35 else 30)
    return fig(P.svg(label), label)


# ============================================================ 1. temel geometrik kavramlar
def u1():
    def ad():
        kind = ch(["dp", "isin", "dogru"])
        a, b = sh(list("ABCDEKLMNPRST"))[:2]
        g = {"dp": "Doğru parçası", "isin": "Işın", "dogru": "Doğru"}[kind]
        return mcq("Şekildeki geometrik çizim hangisidir?" + linefig(kind, a, b), g, ["Doğru parçası", "Işın", "Doğru", "Nokta"],
                   {"dp": "İki ucu da noktayla sınırlı: <b>doğru parçası</b>.", "isin": "Bir ucu noktayla sınırlı, diğer ucu sonsuza uzanıyor: <b>ışın</b>.",
                    "dogru": "İki yönde de sonsuza uzanıyor: <b>doğru</b>."}[kind])

    def gosterim():
        kind = ch(["dp", "isin", "dogru", "uz"])
        a, b = sh(list("ABCDEKLMNPRST"))[:2]
        g = {"dp": "[%s%s]" % (a, b), "isin": "[%s%s" % (a, b), "dogru": "%s%s doğrusu" % (a, b), "uz": "|%s%s|" % (a, b)}[kind]
        alts = ["[%s%s]" % (a, b), "[%s%s" % (a, b), "%s%s doğrusu" % (a, b), "|%s%s|" % (a, b)]
        q = {"dp": "%s ve %s noktaları arasındaki doğru parçası nasıl gösterilir?" % (a, b), "isin": "Başlangıç noktası %s olan ve %s noktasından geçen ışın nasıl gösterilir?" % (a, b),
             "dogru": "%s ve %s noktalarından geçen doğru nasıl gösterilir?" % (a, b), "uz": "%s%s doğru parçasının uzunluğu nasıl gösterilir?" % (a, b)}[kind]
        return mcq(q, g, alts, "Doğru parçası [AB], ışın [AB, doğru parçasının uzunluğu |AB| ile gösterilir. Cevap <b>%s</b>." % g)

    def sayi():
        k = ri(0, 3)
        if k == 0:
            n = ri(3, 7)
            pts = "".join(sh(list("ABCDEFGH"))[:n])
            g = n * (n - 1) // 2
            return mcq("Bir doğru üzerinde %d nokta var (%s). Bu noktalarla kaç farklı doğru parçası çizilebilir?" % (n, ", ".join(pts)), str(g), [str(n), str(n - 1), str(n * (n - 1))],
                       "Her nokta çifti bir doğru parçası verir: %s = <b>%d</b>." % (" + ".join(str(i) for i in range(n - 1, 0, -1)), g))
        if k == 1:
            return mcq("Bir noktadan kaç farklı doğru geçebilir?", "Sonsuz sayıda", ["1", "2", "Hiç"], "Bir noktadan her yönde bir doğru çizilebilir: <b>sonsuz sayıda</b>.")
        if k == 2:
            return mcq("İki farklı noktadan kaç farklı doğru geçer?", "1", ["2", "Sonsuz sayıda", "Hiç"], "İki noktadan yalnızca <b>bir</b> doğru geçer.")
        n = ri(2, 5)
        return mcq("Bir doğru üzerinde %d nokta işaretlendi. Doğru kaç parçaya (ışın ve doğru parçası) ayrılır?" % n, str(n + 1), [str(n), str(n - 1), str(2 * n)],
                   "%d nokta doğruyu %d doğru parçası ve 2 ışın olmak üzere <b>%d</b> parçaya ayırır." % (n, n - 1, n + 1))

    def iliski():
        S = [("Birbirini dik kesen iki doğru", "AB ⊥ CD"), ("Hiç kesişmeyen ve aynı düzlemdeki iki doğru", "AB // CD"), ("Doğru parçasının uzunluğu", "|AB|"),
             ("Başlangıç noktası A olan ışın", "[AB"), ("Uç noktaları A ve B olan doğru parçası", "[AB]")]
        t, g = ch(S)
        return mcq("“%s” sembollerle nasıl gösterilir?" % t, g, [x for _, x in S if x != g], "⊥ diklik, // paralellik sembolüdür. Cevap <b>%s</b>." % g)

    def uzunluk():
        a, b = ri(2, 9), ri(2, 9)
        k = ri(0, 1)
        if k == 0:
            return mcq("A, B ve C noktaları bu sırayla bir doğru üzerindedir. |AB| = %d cm ve |BC| = %d cm ise |AC| kaç cm’dir?" % (a, b), "%d cm" % (a + b),
                       ["%d cm" % abs(a - b) if a != b else "%d cm" % (a + b + 1), "%d cm" % (a * b), "%d cm" % (a + b + 2)], "|AC| = |AB| + |BC| = %d + %d = <b>%d cm</b>." % (a, b, a + b))
        c = a + b
        return mcq("A, B ve C noktaları bu sırayla bir doğru üzerindedir. |AC| = %d cm ve |AB| = %d cm ise |BC| kaç cm’dir?" % (c, a), "%d cm" % b,
                   ["%d cm" % (c + a), "%d cm" % a if a != b else "%d cm" % (b + 1), "%d cm" % (b + 2)], "|BC| = |AC| − |AB| = %d − %d = <b>%d cm</b>." % (c, a, b))

    sets = [("Doğru, ışın, doğru parçası", [(ad, 20)]),
            ("Gösterimler", [(gosterim, 20)]),
            ("Nokta ve doğru sayıları", [(sayi, 20)]),
            ("Diklik ve paralellik sembolleri", [(iliski, 5), (uzunluk, 15)]),
            ("Karışık sorular", [(ad, 6), (gosterim, 6), (uzunluk, 8)])]
    return unit("temel-geometrik-kavramlar", "GS", "MAT.5.3.1, MAT.5.3.2", 1, "Nokta, Doğru, Işın ve Doğru Parçası", "Temel Geometrik Kavramlar",
                "Temel geometrik çizimler için uygun araç ve teknolojiyi kullanır; nokta, doğru, ışın, doğru parçası, dik ve paralel doğrular gibi temel çizimlerin özelliklerine ilişkin çıkarımlarda bulunur.",
                "5. sınıf temel geometrik kavramlar çalışma kâğıdı: nokta, doğru, ışın, doğru parçası, gösterimleri ([AB], [AB, |AB|), dik ve paralel sembolleri, uzunluk. 100 soru ve cevap anahtarı.",
                "Doğru iki yönde, ışın tek yönde uzanır", "Doğru parçasının iki ucu da bellidir.", sets,
                ["Doğru iki yönde sonsuza uzanır. Işın bir başlangıç noktasından bir yönde sonsuza uzanır. Doğru parçasının iki uç noktası vardır, uzunluğu ölçülebilir.",
                 "Gösterimler: doğru parçası [AB], ışın [AB (başlangıç A), uzunluk |AB|. Diklik ⊥, paralellik // sembolüyle gösterilir.",
                 "İki noktadan yalnızca bir doğru geçer; bir noktadan sonsuz sayıda doğru geçer."],
                [("A, B, C sırayla doğru üzerinde; |AB| = 4 cm, |BC| = 6 cm", ["|AC| = 4 + 6"], "10 cm"), ("4 noktayla çizilen doğru parçası sayısı", ["3 + 2 + 1"], "6")],
                [["Işının uzunluğunu ölçmek", "Işın sonsuzdur; yalnızca doğru parçasının uzunluğu ölçülür"], ["[AB ile [BA aynı sanmak", "Işının başlangıç noktası farklıdır"],
                 ["Doğru parçalarını sayarken bazı çiftleri atlamak", "Her noktayı kendisinden sonrakilerle eşleştir"]],
                [("Doğru ile doğru parçası arasındaki fark nedir?", "Doğru sonsuzdur ve ölçülemez; doğru parçasının iki ucu vardır ve uzunluğu ölçülür."),
                 ("Paralel doğrular kesişir mi?", "Hayır. Aynı düzlemde olup hiç kesişmeyen doğrulara paralel doğrular denir."),
                 ("Dik doğrular nasıl çizilir?", "Gönye ya da açıölçerle aralarında 90° olacak şekilde çizilir.")])


# ============================================================ 2. açı ölçme
def u2():
    def oku():
        d = ri(2, 17) * 10 + ch([0, 0, 5])
        if d in (90,) or d >= 180:
            return None
        pic = fig(AU.protractor_svg([0, d]), "açıölçer")
        return mcq("Açıölçerle ölçülen açı kaç derecedir?" + pic, "%d°" % d, ["%d°" % x for x in (180 - d, d + 10, d - 5, d + 5)],
                   "Açının bir kolu iç ölçekte 0’dan başlıyor. Aynı ölçekten okuruz: <b>%d°</b>." % d)

    def oku2():
        a = ri(1, 8) * 10
        d = ri(3, 10) * 10
        if a + d > 180 or d == 90:
            return None
        pic = fig(AU.protractor_svg([a, a + d]), "açıölçer")
        return mcq("Açıölçerde kolları gösterilen açı kaç derecedir?" + pic, "%d°" % d, ["%d°" % x for x in (a + d, 180 - a - d, d + 10, abs(180 - d))],
                   "Kollar %d° ve %d° çizgilerinde: %d − %d = <b>%d°</b>." % (a, a + d, a + d, a, d))

    def tur():
        d = ch([ri(10, 85), 90, ri(95, 175), 180, 360])
        g = "Dar açı" if d < 90 else "Dik açı" if d == 90 else "Geniş açı" if d < 180 else "Doğru açı" if d == 180 else "Tam açı"
        return mcq("Ölçüsü %d° olan açı hangi açıdır?" % d, g, ["Dar açı", "Dik açı", "Geniş açı", "Doğru açı", "Tam açı"],
                   "Dar açı 0° ile 90° arası, dik açı 90°, geniş açı 90° ile 180° arası, doğru açı 180°, tam açı 360°: <b>%s</b>." % low(g))

    def tahmin():
        d = ch([ri(2, 8) * 10 + 5, ri(10, 17) * 10 + 5])
        pic = fig(AU.angle_fig(d, ri(0, 30), label="açı"), "açı")
        cands = [d, d + 40 if d < 120 else d - 70, 180 - d if abs(180 - 2 * d) > 30 else d + 70, d - 40 if d > 50 else d + 90]
        return mcq("Şekildeki açının ölçüsü yaklaşık kaç derecedir?" + pic, "%d°" % d, ["%d°" % x for x in cands[1:] if 0 < x < 180],
                   "Önce dik açıyla karşılaştırırız: %s. Yaklaşık <b>%d°</b>." % ("90°’den küçük" if d < 90 else "90°’den büyük", d))

    def saat():
        h = ri(1, 11)
        m = 0
        d = min(h * 30, 360 - h * 30)
        return mcq("Saat %d.00 olduğunda akrep ile yelkovan arasındaki küçük açı kaç derecedir?" % h, "%d°" % d, ["%d°" % x for x in (d + 30, d - 30 if d > 30 else d + 60, 360 - d, h * 10)],
                   "Saat kadranında iki sayı arası 30°. Kollar arasında %d aralık var: %d × 30 = <b>%d°</b>." % (d // 30, d // 30, d))

    sets = [("Açıölçerle okuma", [(oku, 20)]),
            ("Kolları 0’da olmayan açılar", [(oku2, 20)]),
            ("Ölçüsüne göre açı türleri", [(tur, 10), (saat, 10)]),
            ("Açıyı tahmin etme", [(tahmin, 20)]),
            ("Karışık sorular", [(oku, 8), (oku2, 8), (tur, 4)])]
    return unit("aci-olcme", "GS", "MAT.5.3.3", 2, "Açıölçerle Açı Ölçme", "Açı Ölçme",
                "Açıları ölçmek için uygun araç ve teknolojiyi kullanır.",
                "5. sınıf açı ölçme çalışma kâğıdı: açıölçerde iç ve dış ölçeği okuma, kolları 0’da olmayan açılar, dar, dik, geniş, doğru ve tam açı, açı tahmini. 100 soru ve cevap anahtarı.",
                "Bir kolun gösterdiği 0’dan say", "Önce dar mı geniş mi diye tahmin et, sonra ölç.", sets,
                ["Açıölçerin merkezi açının köşesine, 0 çizgisi bir kola yerleştirilir. Diğer kolun geçtiği sayı, 0’ın bulunduğu ölçekten okunur.",
                 "Kollardan hiçbiri 0’da değilse iki okumanın farkını alırız: 120° − 40° = 80°.",
                 "Ölçmeden önce tahmin etmek hatayı önler: dar açı 90°’den küçük, geniş açı 90°’den büyüktür."],
                [("Kollar 0° ve 65°’de", ["İç ölçekten 65"], "65°"), ("Kollar 30° ve 110°’de", ["110 − 30"], "80°")],
                [["Yanlış ölçekten okumak (65° yerine 115°)", "0’ın bulunduğu ölçeği kullan; önce dar mı geniş mi diye bak"], ["Merkezi köşeye koymamak", "Açıölçerin merkezi tam köşede olmalı"],
                 ["Kolların uzunluğuna bakmak", "Açı kollar arasındaki açıklıktır"]],
                [("Açıölçerde neden iki ölçek var?", "Açının kolu sağda ya da solda olabilir. Hangi kol 0’daysa o ölçek kullanılır."),
                 ("Doğru açı ve tam açı nedir?", "Doğru açı 180°’dir (yarım dönüş); tam açı 360°’dir (tam dönüş)."),
                 ("Açının birimi nedir?", "Derecedir ve ° sembolüyle gösterilir.")])


# ============================================================ 3. doğruların oluşturduğu açılar
def u3():
    def ters():
        d = ri(25, 155)
        if d == 90:
            return None
        k = ri(0, 1)
        if k == 0:
            pic = kesisen(d, {0: "%d°" % d, 2: "x"})
            return mcq("Kesişen iki doğruda x kaç derecedir?" + pic, "%d°" % d, ["%d°" % x for x in (180 - d, 90 - d if d < 90 else d - 90, 360 - d)],
                       "Ters açılar eşittir: <b>x = %d°</b>." % d)
        pic = kesisen(d, {0: "%d°" % d, 1: "x"})
        return mcq("Kesişen iki doğruda x kaç derecedir?" + pic, "%d°" % (180 - d), ["%d°" % x for x in (d, 360 - d, abs(90 - d) if d != 90 else 45)],
                   "Komşu bütünler açılar: x = 180° − %d° = <b>%d°</b>." % (d, 180 - d))

    def tumler():
        a = ri(15, 75)
        k = ri(0, 1)
        if k == 0:
            pic = rays([0, a, 90], {(0, 1): "%d°" % a, (1, 2): "x", (0, 2): None})
            return mcq("Şekilde dik açı iki açıya ayrılmıştır. x kaç derecedir?" + pic, "%d°" % (90 - a), ["%d°" % x for x in (180 - a, a, 90 + a)],
                       "Tümler açıların toplamı 90°: x = 90° − %d° = <b>%d°</b>." % (a, 90 - a))
        return mcq("%d° ölçülü açının tümleri kaç derecedir?" % a, "%d°" % (90 - a), ["%d°" % x for x in (180 - a, a, 90 + a)],
                   "Tümler açıların toplamı 90°: 90 − %d = <b>%d°</b>." % (a, 90 - a))

    def butunler():
        a = ri(20, 160)
        if a == 90:
            return None
        k = ri(0, 1)
        if k == 0:
            pic = rays([0, a, 180], {(0, 1): "%d°" % a, (1, 2): "x"})
            return mcq("Şekilde doğru açı iki açıya ayrılmıştır. x kaç derecedir?" + pic, "%d°" % (180 - a), ["%d°" % x for x in (90 - a if a < 90 else a - 90, a, 360 - a)],
                       "Bütünler açıların toplamı 180°: x = 180° − %d° = <b>%d°</b>." % (a, 180 - a))
        return mcq("%d° ölçülü açının bütünleri kaç derecedir?" % a, "%d°" % (180 - a), ["%d°" % x for x in (abs(90 - a), a, 360 - a)],
                   "Bütünler açıların toplamı 180°: 180 − %d = <b>%d°</b>." % (a, 180 - a))

    def uc():
        a, b = ri(25, 70), ri(25, 70)
        if a + b >= 160:
            return None
        pic = rays([0, a, a + b, 180], {(0, 1): "%d°" % a, (1, 2): "x", (2, 3): "%d°" % (180 - a - b)})
        return mcq("Şekilde bir doğru açı üç açıya ayrılmıştır. x kaç derecedir?" + pic, "%d°" % b, ["%d°" % x for x in (180 - a, 180 - (180 - a - b), 90 - a if a < 90 else b + 10, b + 10)],
                   "Üç açının toplamı 180°: x = 180° − %d° − %d° = <b>%d°</b>." % (a, 180 - a - b, b))

    def paralel():
        th = ri(35, 145)
        if th == 90:
            return None
        k = ri(0, 2)
        names = [("yöndeş", 1, 5), ("iç ters", 3, 5), ("dış ters", 1, 7)]
        nm, i, j = names[k]
        val = {1: th, 2: 180 - th, 3: th, 4: 180 - th, 5: th, 6: 180 - th, 7: th, 8: 180 - th}
        pic = G.parallel_fig(th, {i: "%d°" % val[i], j: "x"})
        return mcq("d<sub>1</sub> // d<sub>2</sub> ise x kaç derecedir?" + pic, "%d°" % val[j], ["%d°" % x for x in (180 - val[j], 90, val[j] + 10)],
                   "x ile %d° %s açılardır; paralel doğrularda %s açılar eşittir: <b>x = %d°</b>." % (val[i], nm, nm, val[j]))

    def ad():
        S = [("Toplamı 90° olan iki açıya ne denir?", "Tümler açılar"), ("Toplamı 180° olan iki açıya ne denir?", "Bütünler açılar"),
             ("Kesişen iki doğrunun oluşturduğu karşılıklı açılara ne denir?", "Ters açılar"), ("Köşeleri ve birer kolları ortak olan açılara ne denir?", "Komşu açılar")]
        q, g = ch(S)
        return mcq(q, g, [x for _, x in S if x != g], "<b>%s</b>." % g)

    sets = [("Kesişen doğrularda açılar", [(ters, 20)]),
            ("Tümler açılar", [(tumler, 20)]),
            ("Bütünler açılar", [(butunler, 20)]),
            ("Doğru açıda açılar", [(uc, 16), (ad, 4)]),
            ("Paralel doğrular ve kesen", [(paralel, 20)])]
    return unit("dogrularin-olusturdugu-acilar", "GS", "MAT.5.3.4", 3, "İki veya Üç Doğrunun Oluşturduğu Açılar", "Doğruların Oluşturduğu Açılar",
                "Düzlemde iki veya üç doğrunun oluşturduğu açılara ilişkin akıl yürütür; açıları türlerine ve aralarındaki ilişkilere göre listeler.",
                "5. sınıf açılar çalışma kâğıdı: komşu açılar, tümler ve bütünler açılar, ters açılar, doğru açının parçaları, paralel doğrularda yöndeş, iç ters ve dış ters açılar. 100 soru ve cevap anahtarı.",
                "Ters açılar eşittir", "Tümler 90°, bütünler 180° eder.", sets,
                ["İki doğru kesiştiğinde karşılıklı açılar (ters açılar) eşittir. Yan yana iki açı ise bütünlerdir, toplamları 180°’dir.",
                 "Toplamı 90° olan açılara tümler, toplamı 180° olan açılara bütünler açılar denir.",
                 "İki paralel doğruyu bir kesen kestiğinde yöndeş açılar, iç ters açılar ve dış ters açılar eşittir."],
                [("Kesişen doğrularda bir açı 65°", ["Komşusu 180 − 65 = 115", "Tersi 65"], "65°, 115°, 65°, 115°"), ("40°’lik açının tümleri", ["90 − 40"], "50°")],
                [["Tümler ile bütünleri karıştırmak", "Tümler 90°, bütünler 180°"], ["Komşu açıları eşit sanmak", "Kesişen doğrularda komşu açılar bütünlerdir; eşit olanlar ters açılardır"],
                 ["Paralel olmayan doğrularda yöndeş açıları eşit saymak", "Yöndeş açılar yalnızca doğrular paralelse eşittir"]],
                [("Ters açılar neden eşittir?", "İkisi de aynı açıyla bütünlerdir; 180°’den aynı sayı çıkınca sonuç aynı olur."),
                 ("Yöndeş açı nedir?", "Paralel doğruları kesen doğrunun aynı tarafında ve paralel doğruların aynı tarafında bulunan açılardır."),
                 ("Bir açının tümleri her zaman var mıdır?", "Hayır. Yalnızca 90°’den küçük açıların tümleri vardır.")])


# ============================================================ 4. çokgenler
ADLAR = {3: "üçgen", 4: "dörtgen", 5: "beşgen", 6: "altıgen", 7: "yedigen", 8: "sekizgen"}


def regular(n, r=60, rot=None, label="çokgen"):
    rot = -90 if rot is None else rot
    pts = [(r * math.cos(math.radians(rot + 360 * i / n)), r * math.sin(math.radians(rot + 360 * i / n))) for i in range(n)]
    return pts


def u4():
    def ad():
        n = ri(3, 8)
        irr = G.R.random() < 0.5
        pts = regular(n)
        if irr:
            pts = [(x * G.R.uniform(0.75, 1.15), y * G.R.uniform(0.75, 1.15)) for x, y in pts]
        pic = poly(pts, label="çokgen")
        return mcq("Şekildeki çokgenin adı nedir?" + pic, cap(ADLAR[n]), [cap(ADLAR[x]) for x in ADLAR if x != n],
                   "Kenarları sayarız: %d kenar → <b>%s</b>." % (n, ADLAR[n]))

    def elemanlar():
        n = ri(3, 8)
        w = ch(["kenarı", "köşesi", "iç açısı"])
        return mcq("Bir %s kaç %s vardır?" % ({3: "üçgenin", 4: "dörtgenin", 5: "beşgenin", 6: "altıgenin", 7: "yedigenin", 8: "sekizgenin"}[n], w), str(n),
                   [str(x) for x in (n - 1, n + 1, 2 * n, n + 2)], "Çokgenlerde kenar, köşe ve iç açı sayıları eşittir: <b>%d</b>." % n)

    def duzgun():
        n = ri(3, 8)
        a = ri(2, 15)
        k = ri(0, 1)
        if k == 0:
            pic = poly(regular(n), [str(a)] + [None] * (n - 1), ticks=[(i, 1) for i in range(n)], label="düzgün çokgen")
            return mcq("Şekildeki düzgün %s çevre uzunluğu kaç santimetredir?" % {3: "üçgenin", 4: "dörtgenin (karenin)", 5: "beşgenin", 6: "altıgenin", 7: "yedigenin", 8: "sekizgenin"}[n] + pic,
                       "%d cm" % (n * a), ["%d cm" % x for x in (a, (n - 1) * a, (n + 1) * a, n + a)], "Düzgün çokgende bütün kenarlar eşit: %d × %d = <b>%d cm</b>." % (n, a, n * a))
        return mcq("Çevre uzunluğu %d cm olan düzgün %s bir kenarı kaç santimetredir?" % (n * a, {3: "üçgenin", 4: "dörtgenin", 5: "beşgenin", 6: "altıgenin", 7: "yedigenin", 8: "sekizgenin"}[n]),
                   "%d cm" % a, ["%d cm" % x for x in (n * a - n, a + 1, a * 2, a + n)], "%d ÷ %d = <b>%d cm</b>." % (n * a, n, a))

    def duzgun_mu():
        S = [("Bütün kenarları ve bütün açıları eşit olan çokgen", "Düzgün çokgen"), ("Kare", "Düzgün dörtgen"), ("Eşkenar üçgen", "Düzgün üçgen"),
             ("Kenarları eşit ama açıları eşit olmayan dörtgen", "Eşkenar dörtgen"), ("Açıları eşit ama kenarları eşit olmayan dörtgen", "Dikdörtgen")]
        t, g = ch(S)
        return mcq("“%s” aşağıdakilerden hangisidir?" % t, g, [x for _, x in S if x != g], "Düzgün çokgende hem kenarlar hem açılar eşittir: <b>%s</b>." % g)

    def kosegen():
        n = ri(4, 8)
        g = n * (n - 3) // 2
        return mcq("Bir %s bir köşesinden kaç köşegen çizilebilir?" % {4: "dörtgenin", 5: "beşgenin", 6: "altıgenin", 7: "yedigenin", 8: "sekizgenin"}[n], str(n - 3),
                   [str(x) for x in (n - 2, n - 1, n, g if g != n - 3 else n + 1)], "Kendisine ve iki komşusuna köşegen çizilmez: %d − 3 = <b>%d</b>." % (n, n - 3))

    def cokgen_mu():
        S = [("Üç kenarlı kapalı şekil", "Evet"), ("Bir daire", "Hayır"), ("Kenarları kesişmeyen ve kapalı olan, doğru parçalarından oluşan şekil", "Evet"),
             ("Açık bir zikzak çizgi", "Hayır"), ("Bir yarım daire", "Hayır"), ("Bir kare", "Evet"), ("İki doğru parçası", "Hayır"), ("Bir yıldız şekli (kenarları doğru parçası, kapalı)", "Evet")]
        t, g = ch(S)
        return mcq("“%s” bir çokgen midir?" % t, g, ["Hayır" if g == "Evet" else "Evet", "Bazen", "Bilinemez"],
                   "Çokgen, doğru parçalarından oluşan kapalı şekildir; eğri kenarlar ya da açık şekiller çokgen değildir: <b>%s</b>." % low(g))

    sets = [("Çokgenlerin adları", [(ad, 20)]),
            ("Kenar, köşe ve açı", [(elemanlar, 18), (kosegen, 2)]),
            ("Düzgün çokgenler", [(duzgun, 20)]),
            ("Köşegenler ve çokgen tanımı", [(kosegen, 3), (cokgen_mu, 7), (duzgun_mu, 5), (ad, 5)]),
            ("Karışık sorular", [(duzgun, 10), (ad, 10)])]
    return unit("cokgenler", "GS", "MAT.5.3.5, MAT.5.3.6", 4, "Çokgenler: Kenar, Köşe, Açı ve Düzgün Çokgenler", "Çokgenler",
                "Çokgenleri, ardışık olarak kesişen doğruların oluşturduğu kapalı şekiller olarak yorumlar; çokgenlerin kenar ve açı özelliklerine ilişkin çıkarımlarda bulunur.",
                "5. sınıf çokgenler çalışma kâğıdı: üçgen, dörtgen, beşgen, altıgen, kenar, köşe ve iç açı sayısı, düzgün çokgenler ve çevreleri, köşegen. 100 soru ve cevap anahtarı.",
                "Çokgen: doğru parçalarından kapalı şekil", "Düzgün çokgende kenarlar ve açılar eşittir.", sets,
                ["En az üç doğrunun art arda kesişmesiyle ve sonuncunun ilkiyle birleşmesiyle oluşan kapalı şekle çokgen denir.",
                 "Bir çokgende kenar, köşe ve iç açı sayıları eşittir. Kenar sayısına göre ad verilir: üçgen, dörtgen, beşgen, altıgen…",
                 "Bütün kenarları ve bütün iç açıları eşit olan çokgene düzgün çokgen denir. Kare ve eşkenar üçgen düzgün çokgendir."],
                [("Düzgün altıgenin bir kenarı 5 cm", ["6 × 5"], "30 cm"), ("Beşgenin bir köşesinden çizilen köşegen", ["5 − 3"], "2")],
                [["Daireyi çokgen sanmak", "Daire eğri çizgiden oluşur, çokgen değildir"], ["Kenarları eşit her şekli düzgün sanmak", "Açılar da eşit olmalı: eşkenar dörtgen düzgün değildir"],
                 ["Köşegen ile kenarı karıştırmak", "Köşegen komşu olmayan iki köşeyi birleştirir"]],
                [("Düzgün çokgen örnekleri nelerdir?", "Eşkenar üçgen, kare, düzgün beşgen ve düzgün altıgen (bal peteği)."),
                 ("Çokgen hangi geometrik kavramlardan oluşur?", "Doğru parçalarından (kenarlar), noktalardan (köşeler) ve açılardan."),
                 ("En az kaç kenarlı çokgen olur?", "En az 3 kenar gerekir; en küçük çokgen üçgendir.")])


# ============================================================ 5. üçgenler ve çember
def u5():
    def toplam():
        a, b = ri(25, 100), ri(25, 100)
        c = 180 - a - b
        if c < 15:
            return None
        pts = AU.tri_pts(a, b, 160)
        pic = fig(AU.shape_svg(pts, {0: "%d°" % a, 1: "%d°" % b, 2: "x"}, "üçgen", rights=tuple(i for i, v in enumerate((a, b, c)) if v == 90 and False)), "üçgen")
        if 90 in (a, b, c):
            return None
        return mcq("Üçgende x kaç derecedir?" + pic, "%d°" % c, ["%d°" % x for x in (180 - a, 180 - b, c + 10, 360 - a - b)],
                   "Üçgenin iç açıları toplamı 180°: x = 180° − %d° − %d° = <b>%d°</b>." % (a, b, c))

    def aci_tur():
        a, b = ri(20, 110), ri(20, 110)
        c = 180 - a - b
        if c < 10:
            return None
        mx = max(a, b, c)
        g = "Dar açılı üçgen" if mx < 90 else "Dik açılı üçgen" if mx == 90 else "Geniş açılı üçgen"
        return mcq("İç açıları %d°, %d° ve %d° olan üçgen hangi üçgendir?" % (a, b, c), g, ["Dar açılı üçgen", "Dik açılı üçgen", "Geniş açılı üçgen", "Eşkenar üçgen"],
                   "En büyük açı %d°: <b>%s</b>." % (mx, low(g)))

    def kenar_tur():
        kind = ch(["Eşkenar üçgen", "İkizkenar üçgen", "Çeşitkenar üçgen"])
        import tr_s4c as C4
        a, b, c = C4.rand_tri(kind)
        return mcq("Kenar uzunlukları %d cm, %d cm ve %d cm olan üçgen kenarlarına göre hangi üçgendir?" % (a, b, c), kind,
                   ["Eşkenar üçgen", "İkizkenar üçgen", "Çeşitkenar üçgen", "Dik açılı üçgen"], "Eşit kenarları sayarız: <b>%s</b>." % low(kind))

    def eskenar():
        k = ri(0, 2)
        if k == 0:
            return mcq("Eşkenar üçgenin bir iç açısı kaç derecedir?", "60°", ["90°", "45°", "180°"], "Üç açı eşit: 180 ÷ 3 = <b>60°</b>.")
        if k == 1:
            a = ri(20, 80)
            return mcq("Bir ikizkenar üçgenin tepe açısı %d° ise taban açılarından biri kaç derecedir?" % (180 - 2 * a), "%d°" % a, ["%d°" % x for x in (180 - a, 2 * a, a + 10)],
                       "Taban açıları eşit: (180 − %d) ÷ 2 = <b>%d°</b>." % (180 - 2 * a, a))
        a = ri(25, 75)
        return mcq("Bir ikizkenar üçgenin taban açılarından biri %d° ise tepe açısı kaç derecedir?" % a, "%d°" % (180 - 2 * a), ["%d°" % x for x in (180 - a, a, 90 - a)],
                   "180 − %d − %d = <b>%d°</b>." % (a, a, 180 - 2 * a))

    def cember():
        k = ri(0, 3)
        r = ri(2, 15)
        if k == 0:
            pic = circle_fig("%d cm" % r, "r", label="yarıçapı gösterilen çember")
            return mcq("Çemberin çapı kaç santimetredir?" + pic, "%d cm" % (2 * r), ["%d cm" % x for x in (r, r + 2, 4 * r)], "Çap = 2 × yarıçap = 2 × %d = <b>%d cm</b>." % (r, 2 * r))
        if k == 1:
            pic = circle_fig("%d cm" % (2 * r), "d", label="çapı gösterilen çember")
            return mcq("Çemberin yarıçapı kaç santimetredir?" + pic, "%d cm" % r, ["%d cm" % x for x in (2 * r, 4 * r, r + 1)], "Yarıçap = çap ÷ 2 = %d ÷ 2 = <b>%d cm</b>." % (2 * r, r))
        if k == 2:
            S = [("Çemberin merkezini çember üzerindeki bir noktaya birleştiren doğru parçası", "Yarıçap"),
                 ("Merkezden geçen ve uçları çember üzerinde olan doğru parçası", "Çap"), ("Çemberin bütün noktalarına eşit uzaklıktaki nokta", "Merkez"),
                 ("Çember ve iç bölgesinin birleşimi", "Daire")]
            t, g = ch(S)
            return mcq("“%s” neyin tanımıdır?" % t, g, [x for _, x in S if x != g], "<b>%s</b>." % g)
        n1 = G.K.next()
        return mcq("%s pergelinin uçları arasını %d cm açarak bir çember çizdi. Çemberin çapı kaç santimetredir?" % (n1, r), "%d cm" % (2 * r), ["%d cm" % x for x in (r, r + 2, 3 * r)],
                   "Pergelin açıklığı yarıçaptır. Çap = 2 × %d = <b>%d cm</b>." % (r, 2 * r))

    def pergel():
        a = ri(3, 9)
        b = ri(3, 9)
        if a == b:
            g = "Eşkenar üçgen"
            q = "Merkezleri A ve B olan, yarıçapları |AB| = %d cm olan iki çember çiziliyor. Kesişim noktası C ile ABC üçgeni oluşturuluyor. Bu üçgen hangisidir?" % a
            e = "|AC| = |BC| = |AB| = %d cm: <b>eşkenar üçgen</b>." % a
        else:
            g = "İkizkenar üçgen"
            q = "A ve B arası %d cm. Merkezi A ve B olan, yarıçapı %d cm olan iki çember çiziliyor. Kesişim noktası C ile ABC üçgeni oluşturuluyor. Bu üçgen hangisidir?" % (a, b)
            e = "|AC| = |BC| = %d cm, |AB| = %d cm: iki kenar eşit, <b>ikizkenar üçgen</b>." % (b, a)
            if b * 2 <= a:
                return None
        return mcq(q, g, ["Eşkenar üçgen", "İkizkenar üçgen", "Çeşitkenar üçgen", "Dik açılı üçgen"], e)

    sets = [("İç açılar toplamı", [(toplam, 20)]),
            ("Açılarına göre üçgenler", [(aci_tur, 20)]),
            ("Kenarlarına göre üçgenler", [(kenar_tur, 12), (pergel, 8)]),
            ("Eşkenar ve ikizkenar üçgende açılar", [(eskenar, 20)]),
            ("Çember: merkez, yarıçap, çap", [(cember, 20)])]
    return unit("ucgenler-ve-cember", "GS", "MAT.5.3.7", 5, "Üçgenler ve Çember: Açılar, Kenarlar, Yarıçap ve Çap", "Üçgenler ve Çember",
                "İki çemberin merkezleri ve kesişim noktasıyla oluşturulan üçgenlerin kenar özelliklerine ilişkin çıkarım yapar; üçgenleri kenar ve açılarına göre sınıflandırır.",
                "5. sınıf üçgenler ve çember çalışma kâğıdı: üçgenin iç açıları toplamı 180°, dar, dik ve geniş açılı üçgen, eşkenar, ikizkenar ve çeşitkenar üçgen, çemberin merkezi, yarıçapı ve çapı. 100 soru ve cevap anahtarı.",
                "Üçgenin iç açıları toplamı 180°", "Çap, yarıçapın iki katıdır.", sets,
                ["Bir üçgenin üç iç açısının toplamı 180°’dir. Bilinmeyen açıyı bulmak için diğer ikisini 180°’den çıkarırız.",
                 "Açılarına göre: bütün açıları dar → dar açılı, bir açısı 90° → dik açılı, bir açısı 90°’den büyük → geniş açılı üçgen.",
                 "Çemberin merkezi bütün noktalarına eşit uzaklıktadır. Bu uzaklık yarıçaptır; çap yarıçapın iki katıdır. Pergelle aynı yarıçaplı çemberler çizerek eşkenar ve ikizkenar üçgen oluşturabiliriz."],
                [("Açıları 50° ve 70° olan üçgenin üçüncü açısı", ["180 − 50 − 70"], "60°"), ("Yarıçapı 6 cm olan çemberin çapı", ["2 × 6"], "12 cm")],
                [["Üçgenin açılarını 360°’ye tamamlamak", "Üçgenin iç açıları toplamı 180°’dir"], ["Çap ile yarıçapı karıştırmak", "Çap merkezden geçer ve yarıçapın 2 katıdır"],
                 ["Çember ile daireyi aynı sanmak", "Çember yalnızca çizgidir; daire çember ve iç bölgesidir"]],
                [("Bir üçgenin iki dik açısı olabilir mi?", "Hayır. İki açı 90° olursa toplam zaten 180° olur ve üçüncü açıya yer kalmaz."),
                 ("Pergelle eşkenar üçgen nasıl çizilir?", "AB doğru parçasını çiz. A ve B merkezli, yarıçapı |AB| olan iki çember çiz. Kesişim noktası C ile ABC eşkenar üçgendir."),
                 ("Eşkenar üçgenin açıları neden 60°’dir?", "Üç açı eşit ve toplamları 180° olduğu için her biri 180 ÷ 3 = 60°’dir.")])


# ============================================================ 6. büyük sayılar
OKU_BIG = None


def oku_big(n):
    n = int(n)
    if n == 0:
        return "sıfır"
    parts = []
    for v, ad in ((10 ** 9, "milyar"), (10 ** 6, "milyon"), (1000, "bin")):
        q, n = divmod(n, v)
        if q:
            parts.append("bin" if (q == 1 and ad == "bin") else oku(q) + " " + ad)
    if n:
        parts.append(oku(n))
    return " ".join(parts)


def big(lo=10 ** 6, hi=10 ** 10 - 1, zeros=True):
    n = ri(lo, hi)
    ds = list(str(n))
    for i in range(1, len(ds)):
        if zeros and G.R.random() < 0.4:
            ds[i] = "0"
    return int("".join(ds))


def u6():
    def okunus():
        n = big()
        s = str(n)
        alts = set()
        for _ in range(12):
            j = ri(1, len(s) - 1)
            t = list(s)
            t[j] = str((int(t[j]) + ri(1, 9)) % 10)
            alts.add(int("".join(t)))
        return mcq("%s sayısının okunuşu hangisidir?" % num(n), oku_big(n), [oku_big(x) for x in alts if x != n], "Bölük bölük okunur: <b>%s</b>." % oku_big(n))

    def yazilis():
        n = big()
        s = str(n)
        w = []
        for _ in range(10):
            j = ri(1, len(s) - 1)
            t = s[:j] + s[j + 1:] + "0" if G.R.random() < 0.5 else s[:j] + "0" + s[j:-1]
            if t[0] != "0":
                w.append(num(int(t)))
        return mcq("“%s” sayısı rakamlarla nasıl yazılır?" % oku_big(n), num(n), w, "Her bölük üç basamaktır; boş basamaklara 0 yazılır: <b>%s</b>." % num(n))

    def bolukler():
        n = big(10 ** 7, 10 ** 10 - 1, False)
        names = [("birler", 1), ("binler", 1000), ("milyonlar", 10 ** 6), ("milyarlar", 10 ** 9)]
        avail = [x for x in names if n >= x[1]]
        ad, v = ch(avail)
        g = n // v % 1000
        return mcq("%s sayısının %s bölüğündeki sayı kaçtır?" % (num(n), ad), str(g), [str(n // x[1] % 1000) for x in avail if x[0] != ad] + [str(g // 10 + 1)],
                   "Sağdan üçerli ayırırız: birler, binler, milyonlar, milyarlar. %s bölüğü <b>%d</b>." % (cap(ad), g))

    def bas_deg():
        n = big(10 ** 7, 10 ** 10 - 1, False)
        s = str(n)
        j = ri(0, len(s) - 2)
        d = int(s[j])
        if d == 0 or s.count(s[j]) > 1:
            return None
        v = d * 10 ** (len(s) - 1 - j)
        return mcq("%s sayısında %d rakamının basamak değeri kaçtır?" % (num(n), d), num(v), [num(v // 10), num(v * 10), num(v // 1000), str(d)],
                   "%d rakamı sağdan %d. basamakta: <b>%s</b>." % (d, len(s) - j, num(v)))

    def yuvarla():
        n = big(10 ** 6, 10 ** 9 - 1, False)
        b, ad = ch([(1000, "bine"), (10 ** 6, "milyona"), (10 ** 5, "yüz bine")])
        if n < b:
            return None
        g = (n + b // 2) // b * b
        return mcq("%s sayısı en yakın %s yuvarlanırsa hangi sayı olur?" % (num(n), ad), num(g), [num(n // b * b + b if g == n // b * b else n // b * b), num(g * 10), num((n + b * 5) // (b * 10) * b * 10)],
                   "Yuvarlanacak basamağın sağındaki rakama bakarız; 5 ve fazlasıysa yukarı yuvarlanır: <b>%s</b>." % num(g))

    def kac_basamak():
        k = ri(0, 2)
        if k == 0:
            d = ri(7, 10)
            return mcq("%d basamaklı en küçük sayı kaçtır?" % d, num(10 ** (d - 1)), [num(10 ** (d - 2)), num(10 ** d - 1), num(10 ** (d - 1) + 1)],
                       "1 ve ardından %d tane 0: <b>%s</b>." % (d - 1, num(10 ** (d - 1))))
        if k == 1:
            d = ri(7, 10)
            return mcq("%d basamaklı en büyük sayı kaçtır?" % d, num(10 ** d - 1), [num(10 ** (d - 1) - 1), num(10 ** d), num(10 ** (d - 1))], "%d tane 9: <b>%s</b>." % (d, num(10 ** d - 1)))
        n = big()
        return mcq("%s sayısı kaç basamaklıdır?" % num(n), str(len(str(n))), [str(len(str(n)) + x) for x in (1, -1, 2)], "Rakamları sayarız: <b>%d</b>." % len(str(n)))

    def hayat():
        S = [("Türkiye’nin nüfusu yaklaşık", 85000000, 86999999), ("Bir şehrin yıllık su tüketimi", 100000000, 900000000), ("Bir yılda bir havalimanını kullanan yolcu sayısı", 10000000, 80000000),
             ("Dünya ile Güneş arasındaki uzaklık yaklaşık (km)", 149000000, 150999999), ("Bir ülkenin yıllık buğday üretimi (kg)", 1000000000, 9999999999)]
        t, lo, hi = ch(S)
        n = ri(lo, hi) // 1000 * 1000
        return mcq("%s %s. Bu sayının okunuşu hangisidir?" % (t, num(n)), oku_big(n), [oku_big(n + 10 ** 6), oku_big(n // 10), oku_big(n + 10 ** 5)],
                   "<b>%s</b>." % oku_big(n))

    sets = [("Büyük sayıları okuma", [(okunus, 20)]),
            ("Büyük sayıları yazma", [(yazilis, 20)]),
            ("Bölükler ve basamak değeri", [(bolukler, 10), (bas_deg, 10)]),
            ("Basamak sayısı ve yuvarlama", [(kac_basamak, 10), (yuvarla, 10)]),
            ("Günlük hayatta büyük sayılar", [(hayat, 12), (okunus, 4), (yazilis, 4)])]
    return unit("buyuk-sayilar", "S", "MAT.5.1.1", 6, "Büyük Sayılar: Milyonlar ve Milyarlar", "Büyük Sayılar",
                "Altı veya daha fazla basamaklı doğal sayıları okur ve yazar; büyük doğal sayılara genellemeler yapar.",
                "5. sınıf büyük sayılar çalışma kâğıdı: milyonlar ve milyarlar bölüğü, büyük sayıları okuma ve yazma, basamak değeri, en yakın bine ve milyona yuvarlama. 100 soru ve cevap anahtarı.",
                "Her bölük üç basamaktır", "Birler, binler, milyonlar, milyarlar bölüğü.", sets,
                ["Büyük sayıları sağdan başlayarak üçerli bölüklere ayırırız: birler, binler, milyonlar, milyarlar.",
                 "Okurken soldan başlar, her bölüğü okuyup bölüğün adını söyleriz: 3.050.200.000 → üç milyar elli milyon iki yüz bin.",
                 "Rakamla yazarken her bölüğün üç basamak olduğunu unutmayız; boş basamaklara 0 yazarız."],
                [("2.040.300.005", ["iki milyar", "kırk milyon", "üç yüz bin", "beş"], "iki milyar kırk milyon üç yüz bin beş"),
                 ("“yedi milyon altı bin on”", ["7 / 006 / 010"], "7.006.010")],
                [["“yedi milyon altı bin on” → 7.6.10", "Her bölük üç basamak: 7.006.010"], ["Bölükleri soldan ayırmak", "Bölükler sağdan üçerli ayrılır"],
                 ["Milyonu 100.000 sanmak", "1 milyon = 1.000.000 (bin tane bin)"]],
                [("1 milyar kaç milyondur?", "1.000 milyondur: 1.000.000.000."),
                 ("Büyük sayıları nerede görürüz?", "Nüfus, uzaklık, bütçe ve üretim miktarları gibi konularda."),
                 ("Bölüklere neden nokta koyarız?", "Sayıyı kolay okumak için; her nokta bir bölüğü ayırır.")])


# ============================================================ 7. doğal sayılarla problemler
def u7():
    def alisveris():
        nm = G.K.next()
        a, b = ri(120, 950), ri(2, 9)
        c, d = ri(35, 280), ri(2, 12)
        p = ri(30, 60) * 100
        tot = a * b + c * d
        if tot >= p:
            return None
        return mcq("%s tanesi %d TL olan %d ayakkabı ve tanesi %d TL olan %d tişört aldı. %s TL verdi. Kaç lira para üstü aldı?" % (nm, a, b, c, d, num(p)), "%s TL" % num(p - tot),
                   ["%s TL" % num(x) for x in (tot, p - a * b, p - tot + 100, p - a - c)], "%d × %d + %d × %d = %s TL. %s − %s = <b>%s TL</b>." % (a, b, c, d, num(tot), num(p), num(tot), num(p - tot)))

    def taksit():
        p = ri(12, 96) * 100
        n = ch([3, 4, 6, 8, 12])
        if p % n:
            return None
        pe = ri(0, 1)
        if pe:
            pes = ri(1, 9) * 100
            if (p - pes) % n or pes >= p:
                return None
            g = (p - pes) // n
            return mcq("Fiyatı %s TL olan bir bilgisayarın %s TL’si peşin, kalanı %d eşit taksitle ödenecek. Bir taksit kaç liradır?" % (num(p), num(pes), n), "%s TL" % num(g),
                       ["%s TL" % num(x) for x in (p // n, g + pes // n, (p + pes) // n if (p + pes) % n == 0 else g + 10)], "(%s − %s) ÷ %d = <b>%s TL</b>." % (num(p), num(pes), n, num(g)))
        return mcq("Fiyatı %s TL olan bir buzdolabı %d eşit taksitle ödenecek. Bir taksit kaç liradır?" % (num(p), n), "%s TL" % num(p // n), ["%s TL" % num(x) for x in (p // n + 100, p - n, p // (n + 1) if p % (n + 1) == 0 else p // n - 50)],
                   "%s ÷ %d = <b>%s TL</b>." % (num(p), n, num(p // n)))

    def uretim():
        a, b, c = ri(120, 980), ri(12, 30), ri(2, 12)
        g = a * b * c
        return mcq("Bir fabrika günde %d oyuncak üretiyor. Ayda %d gün çalışırsa %d ayda kaç oyuncak üretir?" % (a, b, c), num(g), [num(a * b), num(a * c), num(g + a * b)],
                   "%d × %d × %d = <b>%s</b>." % (a, b, c, num(g)))

    def paylas():
        n = ri(3, 12)
        each = ri(150, 4500)
        extra = ri(0, n - 1)
        tot = n * each + extra
        k = ri(0, 1)
        if k == 0 or extra == 0:
            tot = n * each
            return mcq("%s TL %d kişiye eşit paylaştırılıyor. Her kişi kaç lira alır?" % (num(tot), n), "%s TL" % num(each), ["%s TL" % num(x) for x in (each + 1, tot - n, each * 10)],
                       "%s ÷ %d = <b>%s TL</b>." % (num(tot), n, num(each)))
        return mcq("%s kitap %d rafa eşit dizilecek. Her rafa kaç kitap konur ve kaç kitap artar?" % (num(tot), n), "%s kitap, %d artar" % (num(each), extra),
                   ["%s kitap, %d artar" % (num(each + 1), extra), "%s kitap, %d artar" % (num(each), extra + 1 if extra + 1 < n else extra - 1), "%s kitap, %d artar" % (num(each - 1), extra + n)],
                   "%s ÷ %d = %s, kalan %d: <b>%s kitap, %d artar</b>." % (num(tot), n, num(each), extra, num(each), extra))

    def tahmin():
        a, b = ri(1100, 9800), ri(21, 98)
        ra, rb = (a + 500) // 1000 * 1000, (b + 5) // 10 * 10
        return mcq("%s × %d işleminin sonucu yaklaşık kaçtır?" % (num(a), b), num(ra * rb), [num(ra * rb * 10), num(ra * rb // 10), num(ra + rb)],
                   "%s ≈ %s, %d ≈ %d. %s × %d = <b>%s</b>." % (num(a), num(ra), b, rb, num(ra), rb, num(ra * rb)))

    def cok_adim():
        a = ri(25, 60)
        b = ri(3, 8)
        c = ri(4, 10)
        d = ri(100, 400)
        g = a * b * c - d
        if g <= 0:
            return None
        return mcq("Bir okulda %d sınıf var. Her sınıfa %d kutu, her kutuda %d kalem dağıtıldı. Sonra %d kalem kayboldu. Kaç kalem kaldı?" % (b, c, a, d), num(g),
                   [num(a * b * c), num(a * b * c + d), num(a * b + c - d) if a * b + c > d else num(g + 100)], "%d × %d × %d = %s, %s − %d = <b>%s</b>." % (b, c, a, num(a * b * c), num(a * b * c), d, num(g)))

    sets = [("Alışveriş problemleri", [(alisveris, 20)]),
            ("Taksit ve paylaştırma", [(taksit, 10), (paylas, 10)]),
            ("Üretim ve çok adımlı problemler", [(uretim, 10), (cok_adim, 10)]),
            ("Tahmin", [(tahmin, 20)]),
            ("Karışık problemler", [(alisveris, 5), (taksit, 5), (paylas, 5), (cok_adim, 5)])]
    return unit("dogal-sayilarla-problemler", "S", "MAT.5.1.2", 7, "Doğal Sayılarla İşlemler ve Problemler", "Doğal Sayılarla Problemler",
                "Doğal sayılar ve işlemler içeren gerçek yaşam problemlerini çözer.",
                "5. sınıf doğal sayılarla problemler çalışma kâğıdı: alışveriş ve para üstü, taksit, paylaştırma, üretim, çok adımlı problemler ve tahmin. 100 soru ve cevap anahtarı.",
                "Verileni ve isteneni ayır, adım adım çöz", "Sonucu tahminle kontrol et.", sets,
                ["Problemi okuyunca önce verilenleri ve isteneni yaz. Hangi işlemlerin hangi sırayla yapılacağına karar ver.",
                 "Çok adımlı problemlerde her adımın sonucunu ayrı yaz; sonra son işlemi yap.",
                 "Sonucu yuvarlayarak tahmin et. Bulduğun sonuç tahmine yakın değilse işlemi kontrol et."],
                [("Tanesi 450 TL olan 2 ayakkabı ve 120 TL’lik 3 tişört; 2.000 TL verildi", ["2 × 450 + 3 × 120 = 1.260", "2.000 − 1.260"], "740 TL"),
                 ("3.600 TL 6 eşit taksit", ["3.600 ÷ 6"], "600 TL")],
                [["Ara sonucu cevap sanmak", "Sorunun ne istediğini tekrar oku"], ["Kalanı yok saymak", "Problemde kalanın anlamını düşün"],
                 ["Birimi yazmamak", "Cevabı TL, kitap gibi birimiyle yaz"]],
                [("Problemi çözdükten sonra ne yapmalıyım?", "Sonucu tahminle karşılaştır ve problemde yerine koyarak kontrol et."),
                 ("Taksit nedir?", "Bir borcun eşit parçalara bölünerek belirli aralıklarla ödenmesidir."),
                 ("Bir problemi farklı yollarla çözebilir miyim?", "Evet. Önemli olan her adımın doğru ve açık olmasıdır.")])


# ============================================================ 8. dikdörtgenin çevresi
def u8():
    def kenarlar():
        P = ri(5, 15) * 2
        h = P // 2
        a = ri(1, h - 1)
        b = h - a
        return mcq("Çevre uzunluğu %d cm olan bir dikdörtgenin kısa kenarı %d cm ise uzun kenarı kaç santimetredir?" % (P, min(a, b)), "%d cm" % max(a, b),
                   ["%d cm" % x for x in (P - min(a, b), h, max(a, b) + 1, P // 4)], "Bir uzun + bir kısa kenar = %d ÷ 2 = %d. %d − %d = <b>%d cm</b>." % (P, h, h, min(a, b), max(a, b))) if a != b else None

    def kac_farkli():
        h = ri(4, 12)
        P = 2 * h
        g = h // 2
        return mcq("Kenar uzunlukları doğal sayı (cm) olan ve çevresi %d cm olan kaç farklı dikdörtgen çizilebilir? (Kare de dikdörtgendir; 3 × 5 ile 5 × 3 aynıdır.)" % P, str(g),
                   [str(x) for x in (g + 1, h, h - 1, g - 1) if x > 0], "Uzun + kısa = %d. Kısa kenar %s cm olabilir: <b>%d</b> dikdörtgen." % (h, ", ".join(str(i) for i in range(1, g + 1)), g))

    def hangisi():
        h = ri(5, 13)
        P = 2 * h
        a = ri(1, h - 1)
        g = "%d cm ve %d cm" % (a, h - a)
        w = ["%d cm ve %d cm" % (a, h - a + 1), "%d cm ve %d cm" % (a + 2, h - a + 1), "%d cm ve %d cm" % (a, P - a)]
        return mcq("%s çevresi %d cm olan bir dikdörtgen çizdi. Dikdörtgenin kenar uzunlukları hangisi olabilir?" % (G.K.next(), P), g, w, "Kenarların toplamı %d ÷ 2 = %d olmalı: %d + %d = %d. Cevap <b>%s</b>." % (P, h, a, h - a, h, g))

    def kare():
        a = ri(2, 25)
        k = ri(0, 1)
        if k == 0:
            return mcq("Çevresi %d cm olan karenin bir kenarı kaç santimetredir?" % (4 * a), "%d cm" % a, ["%d cm" % x for x in (2 * a, 4 * a, a + 4)], "%d ÷ 4 = <b>%d cm</b>." % (4 * a, a))
        b = ri(1, 3)
        return mcq("Bir kenarı %d cm olan kare ile aynı çevreye sahip ve kısa kenarı %d cm olan dikdörtgenin uzun kenarı kaç santimetredir?" % (a + b, a), "%d cm" % (a + 2 * b),
                   ["%d cm" % x for x in (a + b, a + b + 1, 2 * (a + b) - a)], "Çevre 4 × %d = %d. Uzun kenar %d ÷ 2 − %d = <b>%d cm</b>." % (a + b, 4 * (a + b), 4 * (a + b), a, a + 2 * b))

    def cizim():
        a, b = ri(2, 8), ri(2, 6)
        if a == b:
            return None
        cells = [(x, y) for x in range(a) for y in range(b)]
        P = 2 * (a + b)
        return mcq("Birim karelerin bir kenarı 1 cm’dir. Şeklin çevre uzunluğu kaç santimetredir?" + grid_shape(cells), "%d cm" % P, ["%d cm" % x for x in (a * b, a + b, P + 2, P - 2)],
                   "%d + %d + %d + %d = <b>%d cm</b>." % (a, b, a, b, P))

    def problem():
        a, b = ri(8, 40), ri(5, 30)
        if a == b:
            return None
        p = ri(3, 9)
        P = 2 * (a + b)
        k = ri(0, 1)
        if k == 0:
            return mcq("Kenarları %d m ve %d m olan dikdörtgen bir bahçenin etrafı tel ile çevrilecek. Kaç metre tel gerekir?" % (a, b), "%d m" % P, ["%d m" % x for x in (a + b, a * b, P + a)],
                       "Çevre: 2 × (%d + %d) = <b>%d m</b>." % (a, b, P))
        return mcq("Kenarları %d m ve %d m olan dikdörtgen bir bahçenin etrafı %d sıra tel ile çevrilecek. Kaç metre tel gerekir?" % (a, b, p), "%d m" % (P * p), ["%d m" % x for x in (P, (a + b) * p, P * p + p)],
                   "Çevre %d m. %d × %d = <b>%d m</b>." % (P, P, p, P * p))

    sets = [("Kenar uzunluklarını bulma", [(kenarlar, 20)]),
            ("Aynı çevreli dikdörtgenler", [(kac_farkli, 6), (hangisi, 14)]),
            ("Kare ve dikdörtgen", [(kare, 20)]),
            ("Kareli kâğıtta çevre", [(cizim, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("dikdortgenin-cevresi", "GN", "MAT.5.4.1", 8, "Çevresi Verilen Dikdörtgenin Kenar Uzunlukları", "Dikdörtgenin Çevresi",
                "Çevre uzunluğu verilen dikdörtgenin kenar uzunluklarını yorumlar; aynı çevre uzunluğuna sahip farklı dikdörtgenler oluşturur.",
                "5. sınıf dikdörtgenin çevresi çalışma kâğıdı: çevresi verilen dikdörtgenin kenarları, aynı çevreli farklı dikdörtgenler, kare ve dikdörtgen, kareli kâğıtta çevre ve problemler. 100 soru ve cevap anahtarı.",
                "Uzun kenar + kısa kenar = çevre ÷ 2", "Aynı çevreli birçok farklı dikdörtgen olabilir.", sets,
                ["Dikdörtgenin çevresi = 2 × (uzun kenar + kısa kenar). Bu yüzden bir uzun ve bir kısa kenarın toplamı çevrenin yarısıdır.",
                 "Çevre verildiğinde önce yarısını buluruz, sonra bu toplamı veren kenar çiftlerini yazarız: çevre 16 cm → 1 + 7, 2 + 6, 3 + 5, 4 + 4.",
                 "Kare de bir dikdörtgendir; çevresi 4 × kenardır."],
                [("Çevre 20 cm, kısa kenar 3 cm", ["20 ÷ 2 = 10", "10 − 3"], "7 cm"), ("Çevresi 12 cm olan dikdörtgenler", ["Toplam 6: 1–5, 2–4, 3–3"], "3 dikdörtgen")],
                [["Çevreden kısa kenarı doğrudan çıkarmak", "Önce çevreyi ikiye böl"], ["3 × 5 ile 5 × 3’ü farklı saymak", "Döndürülmüş dikdörtgen aynı dikdörtgendir"],
                 ["Kareyi dikdörtgen saymamak", "Kare özel bir dikdörtgendir"]],
                [("Çevre uzunluğu hangi birimle ölçülür?", "Uzunluk birimleriyle: mm, cm, m, km."),
                 ("Aynı çevreli dikdörtgenlerin alanları aynı mıdır?", "Hayır. Kenarlar birbirine yaklaştıkça alan büyür; en büyük alan kareye aittir."),
                 ("Günlük hayatta çevreyi nerede kullanırız?", "Bahçe çiti, çerçeve, kurdele ve süpürgelik gibi kenar boyunca ölçülen işlerde.")])


# ============================================================ 9. dikdörtgenin alanı
def u9():
    def say():
        a, b = ri(2, 6), ri(2, 6)
        cells = [(x, y) for x in range(a) for y in range(b)]
        return mcq("Şeklin alanı kaç birim karedir?" + grid_shape(cells), "%d birim kare" % (a * b), ["%d birim kare" % x for x in (2 * (a + b), a + b, a * b + a, a * b - 1)],
                   "%d sırada %d kare: %d × %d = <b>%d birim kare</b>." % (b, a, a, b, a * b))

    def formul():
        a, b = ri(2, 9), ri(2, 6)
        if a * b > 36 or a == b:
            return None
        u, uad = ch([("cm", "santimetrekare"), ("m", "metrekare")])
        pic = poly([(0, 0), (a * 22, 0), (a * 22, -b * 22), (0, -b * 22)], [str(a), str(b), None, None], unit_=u, label="dikdörtgen", rights=(0, 1, 2, 3))
        return mcq("Dikdörtgenin alanı kaç %s?" % ({"cm": "santimetrekaredir", "m": "metrekaredir"}[u]) + pic, "%d %s²" % (a * b, u), ["%d %s²" % (x, u) for x in (2 * (a + b), a + b, a * b + b)] + ["%d %s" % (a * b, u)],
                   "Alan = iki komşu kenarın çarpımı = %d × %d = <b>%d %s²</b>." % (a, b, a * b, u))

    def kare():
        a = ri(2, 6)
        return mcq("Bir kenarı %d m olan kare şeklindeki odanın alanı kaç metrekaredir?" % a, "%d m²" % (a * a), ["%d m²" % x for x in (4 * a, 2 * a, a * a + a)] + ["%d m" % (a * a)],
                   "%d × %d = <b>%d m²</b>." % (a, a, a * a))

    def eksik():
        a, b = ri(2, 9), ri(2, 6)
        if a * b > 36 or a == b:
            return None
        return mcq("Alanı %d cm² olan dikdörtgenin bir kenarı %d cm ise diğer kenarı kaç santimetredir?" % (a * b, a), "%d cm" % b, ["%d cm" % x for x in (a * b - a, a, b + 1, a * b // 2)],
                   "%d ÷ %d = <b>%d cm</b>." % (a * b, a, b))

    def birim():
        S = [("Bir defter sayfasının alanı", "cm²"), ("Bir sınıfın tabanının alanı", "m²"), ("Bir futbol sahasının alanı", "m²"), ("Bir posta pulunun alanı", "cm²"),
             ("Bir kitap kapağının alanı", "cm²"), ("Bir evin bahçesinin alanı", "m²"), ("Bir masa örtüsünün alanı", "m²"), ("Bir silginin bir yüzünün alanı", "cm²")]
        t, g = ch(S)
        return mcq("%s hangi birimle ölçülmeye daha uygundur?" % t, g, ["cm²" if g == "m²" else "m²", "cm", "m"],
                   "Küçük yüzeyler için cm², büyük yüzeyler için m² kullanılır: <b>%s</b>." % g)

    def kareler():
        a = ri(2, 6)
        b = ri(2, 6)
        n = a * b
        if n > 36:
            return None
        return mcq("Bir kenarı 1 cm olan %d tane kare yan yana ve üst üste dizilerek %d sıralı bir dikdörtgen oluşturuldu. Her sırada kaç kare vardır?" % (n, b), str(a),
                   [str(x) for x in (n - b, b, a + 1, n // 2)], "%d ÷ %d = <b>%d</b>." % (n, b, a))

    sets = [("Birim karelerle alan", [(say, 20)]),
            ("Alan formülü", [(formul, 20)]),
            ("Kare ve alan birimleri", [(kare, 5), (birim, 8), (kareler, 7)]),
            ("Eksik kenarı bulma", [(eksik, 20)]),
            ("Karışık sorular", [(formul, 10), (eksik, 6), (kareler, 4)])]
    return unit("dikdortgenin-alani", "GN", "MAT.5.4.2", 9, "Dikdörtgenin Alanı: Birim Kareler ve Alan Formülü", "Dikdörtgenin Alanı",
                "Dikdörtgenin alanını birim karelerle değerlendirir; birim kare sayısı ile iki komşu kenar uzunluğu arasındaki ilişkiden alan bağıntısına ulaşır.",
                "5. sınıf dikdörtgenin alanı çalışma kâğıdı: birim karelerle alan, alan = uzun kenar × kısa kenar, karenin alanı, cm² ve m², eksik kenarı bulma. 100 soru ve cevap anahtarı.",
                "Alan = iki komşu kenarın çarpımı", "Alan birim kare (cm², m²) ile ölçülür.", sets,
                ["Bir dikdörtgeni birim karelerle kaplarsak her sırada uzun kenar kadar, toplamda kısa kenar kadar sıra olur. Bu yüzden alan = uzun kenar × kısa kenar.",
                 "Kenarı 1 cm olan karenin alanı 1 cm², kenarı 1 m olan karenin alanı 1 m²’dir.",
                 "Alanı ve bir kenarı verilen dikdörtgenin diğer kenarını bölmeyle buluruz."],
                [("Kenarları 6 cm ve 4 cm olan dikdörtgen", ["6 × 4"], "24 cm²"), ("Alanı 30 cm², bir kenarı 5 cm", ["30 ÷ 5"], "6 cm")],
                [["Alanı cm ile yazmak", "Alan birimi cm² ya da m²’dir"], ["Alan yerine çevreyi hesaplamak", "Alan için kenarlar çarpılır, çevre için toplanır"],
                 ["Birim kareleri eksik saymak", "Sıra sayısı × her sıradaki kare sayısı"]],
                [("cm² nasıl okunur?", "“Santimetrekare” diye okunur."),
                 ("Karenin alanı nasıl bulunur?", "Kare bir dikdörtgendir: kenar × kenar."),
                 ("Alan ile çevre arasındaki fark nedir?", "Çevre kenarların toplam uzunluğu, alan ise şeklin kapladığı yüzeydir.")])


# ============================================================ 10. çevre ve alan problemleri
def u10():
    def ayni_alan():
        n = ch([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 48])
        pairs = [(a, n // a) for a in range(1, n + 1) if n % a == 0 and a <= n // a]
        a, b = ch(pairs)
        g = 2 * (a + b)
        return mcq("Alanı %d cm² olan, kenarları doğal sayı olan dikdörtgenlerden kısa kenarı %d cm olanın çevresi kaç santimetredir?" % (n, a), "%d cm" % g,
                   ["%d cm" % (2 * (x + n // x)) for x, _ in pairs if x != a] + ["%d cm" % n, "%d cm" % (a + b)], "Kenarlar %d cm ve %d cm. Çevre 2 × (%d + %d) = <b>%d cm</b>." % (a, b, a, b, g))

    def ayni_cevre():
        h = ri(5, 15)
        a = ri(1, h // 2)
        b = h - a
        g = a * b
        return mcq("Çevresi %d cm olan ve kısa kenarı %d cm olan dikdörtgenin alanı kaç santimetrekaredir?" % (2 * h, a), "%d cm²" % g, ["%d cm²" % x for x in (2 * h, h, (a + 1) * (b - 1) if b - 1 > a else g + h, a + b + 1)],
                   "Uzun kenar %d − %d = %d. Alan %d × %d = <b>%d cm²</b>." % (h, a, b, a, b, g))

    def en_buyuk():
        h = ri(4, 12)
        P = 2 * h
        a = h // 2
        g = a * (h - a)
        return mcq("Çevresi %d cm olan ve kenarları doğal sayı olan dikdörtgenlerden alanı en büyük olanın alanı kaç santimetrekaredir?" % P, "%d cm²" % g,
                   ["%d cm²" % x for x in ((a - 1) * (h - a + 1), h - 1, P, 1 * (h - 1)) if x != g], "Kenarlar birbirine en yakın olduğunda alan en büyüktür: %d × %d = <b>%d cm²</b>." % (a, h - a, g))

    def karsilastir():
        a, b = ri(2, 6), ri(2, 6)
        c, d = ri(2, 6), ri(2, 6)
        if a * b == c * d or 2 * (a + b) != 2 * (c + d):
            return None
        g = "Çevreleri eşit, alanları farklı"
        return mcq("Birinci dikdörtgenin kenarları %d cm ve %d cm, ikincisinin kenarları %d cm ve %d cm. Hangisi doğrudur?" % (a, b, c, d), g,
                   ["Alanları eşit, çevreleri farklı", "Hem alanları hem çevreleri eşit", "Hem alanları hem çevreleri farklı"],
                   "Çevreler: %d cm ve %d cm. Alanlar: %d cm² ve %d cm². <b>%s</b>." % (2 * (a + b), 2 * (c + d), a * b, c * d, g))

    def karsilastir2():
        n = ch([12, 16, 18, 24, 36])
        pairs = [(x, n // x) for x in range(1, n + 1) if n % x == 0 and x < n // x]
        if len(pairs) < 2:
            return None
        (a, b), (c, d) = sh(pairs)[:2]
        g = "Alanları eşit, çevreleri farklı"
        return mcq("Birinci dikdörtgenin kenarları %d cm ve %d cm, ikincisinin kenarları %d cm ve %d cm. Hangisi doğrudur?" % (a, b, c, d), g,
                   ["Çevreleri eşit, alanları farklı", "Hem alanları hem çevreleri eşit", "Hem alanları hem çevreleri farklı"],
                   "Alanlar: %d cm² ve %d cm². Çevreler: %d cm ve %d cm. <b>%s</b>." % (a * b, c * d, 2 * (a + b), 2 * (c + d), g))

    def problem():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(3, 9), ri(2, 4)
            p = ri(2, 9) * 50
            return mcq("Kenarları %d m ve %d m olan dikdörtgen şeklindeki bir odaya halı döşenecek. Halının metrekaresi %d TL ise kaç lira ödenir?" % (a, b, p), "%s TL" % num(a * b * p),
                       ["%s TL" % num(x) for x in (2 * (a + b) * p, a * b, (a + b) * p)], "Alan %d × %d = %d m². %d × %d = <b>%s TL</b>." % (a, b, a * b, a * b, p, num(a * b * p)))
        if k == 1:
            a = ri(2, 6)
            s = a * a
            return mcq("Alanı %d m² olan kare şeklindeki bir bahçenin çevresine çit yapılacak. Kaç metre çit gerekir?" % s, "%d m" % (4 * a), ["%d m" % x for x in (s, 2 * a, 4 * s)],
                       "Kenar %d m (%d × %d = %d). Çevre 4 × %d = <b>%d m</b>." % (a, a, a, s, a, 4 * a))
        a, b = ri(2, 6), ri(2, 6)
        t = 1
        return mcq("Bir kenarı 1 m olan kare fayanslarla %d m × %d m boyutlarındaki bir zemin kaplanacak. Kaç fayans gerekir?" % (a, b), str(a * b), [str(x) for x in (2 * (a + b), a + b, a * b + a)],
                   "Alan %d × %d = %d m². Her fayans 1 m²: <b>%d fayans</b>." % (a, b, a * b, a * b))

    sets = [("Alanı verilen dikdörtgenin çevresi", [(ayni_alan, 20)]),
            ("Çevresi verilen dikdörtgenin alanı", [(ayni_cevre, 14), (en_buyuk, 6)]),
            ("Çevre ve alan karşılaştırma", [(karsilastir, 10), (karsilastir2, 10)]),
            ("Problemler", [(problem, 20)]),
            ("Karışık sorular", [(ayni_alan, 7), (ayni_cevre, 7), (problem, 6)])]
    return unit("cevre-ve-alan-iliskisi", "GN", "MAT.5.4.3, MAT.5.4.4", 10, "Dikdörtgende Çevre ve Alan İlişkisi ve Problemler", "Çevre ve Alan İlişkisi",
                "Kenar uzunlukları doğal sayı olan dikdörtgenlerde alanı verilenin çevresini, çevresi verilenin alanını yorumlar; dikdörtgenin çevre ve alanıyla ilgili problemleri çözer.",
                "5. sınıf çevre ve alan ilişkisi çalışma kâğıdı: aynı alanlı farklı çevreli ve aynı çevreli farklı alanlı dikdörtgenler, en büyük alan, halı, çit ve fayans problemleri. 100 soru ve cevap anahtarı.",
                "Eşit çevre ≠ eşit alan", "Aynı alanlı dikdörtgenlerin çevreleri farklı olabilir.", sets,
                ["Aynı çevreye sahip dikdörtgenlerin alanları farklı olabilir: çevre 12 cm → 1 × 5 (5 cm²), 2 × 4 (8 cm²), 3 × 3 (9 cm²).",
                 "Aynı alana sahip dikdörtgenlerin çevreleri farklı olabilir: alan 12 cm² → 1 × 12 (çevre 26 cm), 2 × 6 (16 cm), 3 × 4 (14 cm).",
                 "Problemde ne istendiğine bakarız: kenar boyunca (çit, kurdele) → çevre; yüzey kaplama (halı, boya, fayans) → alan."],
                [("Alan 18 cm², kısa kenar 3 cm", ["Uzun kenar 18 ÷ 3 = 6", "Çevre 2 × (3 + 6)"], "18 cm"), ("4 m × 3 m oda, m²’si 200 TL halı", ["Alan 12 m²", "12 × 200"], "2.400 TL")],
                [["Çevreleri eşitse alanları da eşit sanmak", "Kenarları hesaplayıp alanları ayrı ayrı bul"], ["Çit için alan hesaplamak", "Çit kenar boyuncadır: çevre"],
                 ["Halı için çevre hesaplamak", "Halı yüzeyi kaplar: alan"]],
                [("Aynı çevrede en büyük alan hangi dikdörtgendedir?", "Kenarları birbirine en yakın olanda; kenarlar eşitse (kare) alan en büyüktür."),
                 ("Aynı alanda en küçük çevre hangisindedir?", "Yine kenarları birbirine en yakın olan dikdörtgende."),
                 ("Alan problemlerinde birimlere nasıl dikkat ederim?", "Kenarlar m ise alan m², cm ise cm² olur. Farklı birimleri önce aynı birime çevir.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
