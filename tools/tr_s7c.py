# -*- coding: utf-8 -*-
"""Türkiye 7. sınıf: Geometrik Nicelikler (19〜24)、İstatistiksel Araştırma Süreci (25)、Veriden Olasılığa (26〜27)。"""
import math
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, num, fr, M, NB
from tr_g7 import sn, dq, MINUS, gen, ondalik
import kr_pics56 as KP


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


# ============================================================ 19. küp yapıları ve görünümleri
def heights(w, d, mx=3):
    while True:
        h = {(x, y): ri(0, mx) for x in range(w) for y in range(d)}
        if sum(1 for v in h.values() if v) >= 3 and all(any(h[(x, y)] for y in range(d)) for x in range(w)) and all(any(h[(x, y)] for x in range(w)) for y in range(d)):
            return h


def cells_of(h):
    return [(x, y, z) for (x, y), v in h.items() for z in range(v)]


def iso(h):
    return KP.iso_cubes(cells_of(h), label="eş küplerden yapı").replace(">앞<", ">Ön<")


def view(h, kind):
    """(cells(c, r), w, h)"""
    w = max(x for x, _ in h) + 1
    d = max(y for _, y in h) + 1
    if kind == "on":       # önden: x sütunları, yükseklik = max_y
        H = max(h.values())
        col = [max(h[(x, y)] for y in range(d)) for x in range(w)]
        return ([(x, H - 1 - z) for x in range(w) for z in range(col[x])], w, H)
    if kind == "sag":      # sağdan: y sütunları (öndeki solda)
        H = max(h.values())
        col = [max(h[(x, y)] for x in range(w)) for y in range(d)]
        return ([(d - 1 - y, H - 1 - z) for y in range(d) for z in range(col[y])], d, H)
    return ([(x, y) for (x, y), v in h.items() if v], w, d)   # üstten


def key(v):
    return (tuple(sorted(v[0])), v[1], v[2])


def u19():
    def say():
        h = heights(ch([2, 3]), ch([2, 3]))
        n = sum(h.values())
        hidden = sum(1 for (x, y, z) in cells_of(h) if z == 0)
        return M("Şekildeki yapı kaç birim küpten oluşur? (Görünmeyen küpler, üstteki küpleri taşıyacak kadar vardır.)" + iso(h), num(n),
                 [num(n - 1), num(n + 1), num(len([1 for v in h.values() if v]))], "Her sütundaki küp sayılarını toplarız: <b>%d</b>." % n)

    def gor(kind, ad):
        def f():
            h = heights(ch([2, 3]), ch([2, 3]))
            good = view(h, kind)
            others = [view(h, k) for k in ("on", "sag", "ust") if k != kind]
            # yanlış: bir sütunu eksik / fazla
            cells, w, H = good
            alt = (cells[:-1], w, H) if len(cells) > 1 else None
            opts = [good] + [o for o in others if key(o) != key(good)] + ([alt] if alt else [])
            uniq = []
            for o in opts:
                if o and key(o) not in [key(u) for u in uniq]:
                    uniq.append(o)
            if len(uniq) < 4:
                return None
            uniq = uniq[:4]
            order = sh(range(4))
            pan = KP.views_panel([uniq[i] for i in order], labels="ABCD")
            j = order.index(0)
            return M("Yapının %s görünümü hangisidir?" % ad + iso(h) + pan, "ABCD"[j], [x for i, x in enumerate("ABCD") if i != j],
                     "%s bakınca her sütunda en yüksek küp sayısı görülür: <b>%s</b>." % (cap(ad.replace("görünümü", "")), "ABCD"[j]))
        return f

    def kac_en_az():
        top = ri(2, 7)
        n = ri(2, 4)
        return M("Bir yapının üstten görünümünde %d kare vardır. Önden görünümünde en yüksek sütun %d küp yüksekliğindedir. Bu yapı en az kaç küpten oluşur?" % (top, n), num(top + n - 1),
                 [num(top * n), num(top), num(top + n)], "Üstten görünen her konumda en az 1 küp, en yüksek sütun için %d − 1 küp daha: %d + %d = <b>%d</b>." % (n, top, n - 1, top + n - 1))

    sets = [("Küpleri sayma", [(say, 20)]),
            ("Önden görünüm", [(gor("on", "önden"), 20)]),
            ("Üstten görünüm", [(gor("ust", "üstten"), 20)]),
            ("Sağdan görünüm", [(gor("sag", "sağdan"), 20)]),
            ("Karışık", [(say, 7), (gor("on", "önden"), 7), (kac_en_az, 6)])]
    return unit("es-kuplerle-yapilar-ve-gorunumleri", "GN", "MAT.7.4.1", 19, "Eş Küplerle Oluşturulan Yapılar ve Görünümleri", "Yapılar ve Görünümler",
                "Eş küplerle oluşturulan yapılar ile görünümleri arasındaki ilişkiyi çözümler; yapıların farklı yönlerden görünümlerini çizer, görünümleri verilen yapıyı oluşturur.",
                "7. sınıf eş küplerle yapılar ve görünümleri çalışma kâğıdı: yapıdaki küpleri sayma, önden, üstten ve sağdan görünümler, görünümlerden en az küp sayısı. 100 soru ve cevap anahtarı.",
                "Her yönden en yüksek sütun görünür", "Öndeki küpler arkadakileri örter.", sets,
                ["Eş küplerle yapılan bir yapıya önden, sağdan ve üstten bakınca kareli kâğıda çizilebilen görünümler elde ederiz.",
                 "Önden görünümde her sütunda, o sıradaki en yüksek küp kulesi görülür; arkadaki daha kısa kuleler görünmez.",
                 "Üstten görünümde küp bulunan her konum bir kare olarak görülür; yükseklik görünmez."],
                [("Önde 2, arkada 3 küplük kule", ["Önden bakınca daha yüksek olan görünür"], "3 kare yüksekliğinde sütun"),
                 ("Üstten 4 kare, en yüksek sütun 3", ["4 konumda en az 1 küp", "+ 2 küp"], "En az 6 küp")],
                [["Görünmeyen küpleri saymamak", "Üstteki küplerin altında mutlaka küp vardır"],
                 ["Sağdan görünümü ters çizmek", "Sağdan bakarken öndeki sütun solda kalır"],
                 ["Üstten görünümde yüksekliği çizmeye çalışmak", "Üstten yalnızca konumlar görülür"]],
                [("Bir yapının tek görünümü onu belirler mi?", "Hayır. Farklı yapıların önden görünümü aynı olabilir; bu yüzden birkaç görünüm birlikte kullanılır."),
                 ("Görünümler neden kareli kâğıda çizilir?", "Her küpün yüzü bir kareye karşılık geldiği için ölçüler korunur."),
                 ("Mimarlar bunu kullanır mı?", "Evet. Binaların önden, yandan ve üstten görünümleri (planları) çizilir.")])


def cap(s):
    return G.cap(s.strip())


# ============================================================ 20. yüzey alanı
def u20():
    def boyut():
        a, b, c = ri(2, 15), ri(2, 12), ri(2, 10)
        S = 2 * (a * b + a * c + b * c)
        return M("Ayrıt uzunlukları %d cm, %d cm ve %d cm olan dikdörtgenler prizmasının yüzey alanı kaç cm²’dir?" % (a, b, c) + KP.box_svg(a, b, c),
                 num(S), [num(a * b * c), num(a * b + a * c + b * c), num(S + 2 * a * b)],
                 "Yüzey alanı = 2(ab + ac + bc) = 2(%d + %d + %d) = <b>%s cm²</b>." % (a * b, a * c, b * c, num(S)))

    def kup():
        a = ri(2, 30)
        return M("Bir ayrıtı %d cm olan küpün yüzey alanı kaç cm²’dir?" % a, num(6 * a * a), [num(a ** 3), num(4 * a * a), num(6 * a)],
                 "Küpün 6 eş kare yüzü vardır: 6 · %d · %d = <b>%s cm²</b>." % (a, a, num(6 * a * a)))

    def ac():
        a, b, c = ri(2, 9), ri(2, 9), ri(2, 9)
        if len({a, b, c}) < 3:
            return None
        k = ch(["en büyük", "en küçük"])
        fs = sorted([a * b, a * c, b * c])
        v = fs[-1] if k == "en büyük" else fs[0]
        return M("%d cm × %d cm × %d cm boyutlarındaki dikdörtgenler prizmasının açınımında %s yüzün alanı kaç cm²’dir?" % (a, b, c, k), num(v),
                 [num(x) for x in fs if x != v] + [num(v * 2)], "Yüzlerin alanları %s cm²; her biri 2 tane. %s: <b>%d cm²</b>." % (", ".join(map(str, fs)), cap(k), v))

    def kapsiz():
        a, b, c = ri(3, 12), ri(3, 12), ri(3, 10)
        S = a * b + 2 * (a * c + b * c)
        return M("Üstü açık, taban ayrıtları %d cm ve %d cm, yüksekliği %d cm olan dikdörtgenler prizması biçimindeki bir kutunun dış yüzeyi boyanacak. Boyanacak alan kaç cm²’dir?" % (a, b, c),
                 num(S), [num(S + a * b), num(a * b * c), num(2 * (a * c + b * c))], "Üst yüz yok: %d · %d + 2(%d · %d + %d · %d) = <b>%s cm²</b>." % (a, b, a, c, b, c, num(S)))

    def eksik():
        a, b, c = ri(2, 10), ri(2, 10), ri(2, 10)
        S = 2 * (a * b + a * c + b * c)
        return M("Yüzey alanı %s cm² olan dikdörtgenler prizmasının iki ayrıtı %d cm ve %d cm’dir. Üçüncü ayrıtı kaç cm’dir?" % (num(S), a, b), num(c),
                 [num(c + 1), num(c + 2) if c > 2 else num(c + 3), num(S // (a * b)) if S // (a * b) != c else num(c - 1)],
                 "2(%d + %d · c + %d · c) = %d → %d + %d · c = %d → c = <b>%d</b>." % (a * b, a, b, S, a * b, a + b, S // 2, c))

    sets = [("Yüzey alanı", [(boyut, 20)]),
            ("Küp", [(kup, 20)]),
            ("Açınımdaki yüzler", [(ac, 20)]),
            ("Üstü açık kutular", [(kapsiz, 20)]),
            ("Eksik ayrıt ve karışık", [(eksik, 8), (boyut, 6), (kapsiz, 6)])]
    return unit("dikdortgenler-prizmasinin-yuzey-alani", "GN", "MAT.7.4.2", 20, "Dikdörtgenler Prizmasının Yüzey Alanı", "Prizmanın Yüzey Alanı",
                "Dikdörtgenler prizmasının yüzey alanını yorumlar; farklı yüzey açınımlarını inceler, açınım ile yüzey alanı arasındaki ilişkiyi ifade eder ve yüzey alanını hesaplar.",
                "7. sınıf dikdörtgenler prizmasının yüzey alanı çalışma kâğıdı: ayrıtları verilen prizmanın ve küpün yüzey alanı, açınımdaki yüzler, üstü açık kutular, yüzey alanından ayrıt bulma. 100 soru ve cevap anahtarı.",
                "Yüzey alanı = yüzlerin alanları toplamı", "Prizma: 2(ab + ac + bc).  Küp: 6a².", sets,
                ["Dikdörtgenler prizmasının 6 yüzü vardır; karşılıklı yüzler eştir. Açınımı katlanınca prizma oluşur.",
                 "Yüzey alanı, bütün yüzlerin alanları toplamıdır: 2(ab + ac + bc). Küpte 6 eş kare vardır: 6a².",
                 "Üstü açık kutuda bir yüz eksiktir; o yüzün alanı toplamdan çıkarılır."],
                [("4 cm × 3 cm × 5 cm", ["2(12 + 20 + 15)"], "94 cm²"), ("Ayrıtı 7 cm olan küp", ["6 · 49"], "294 cm²")],
                [["Yüzey alanı yerine hacmi bulmak", "Yüzey alanı cm², hacim cm³ ile ölçülür"],
                 ["Her yüzden yalnızca birini saymak", "Karşılıklı eş yüzler: hepsi 2 tane"],
                 ["Üstü açık kutuda 6 yüzü de saymak", "Açık yüzü çıkar"]],
                [("Aynı yüzey alanına sahip farklı prizmalar olur mu?", "Evet. Farklı ayrıt uzunlukları aynı toplamı verebilir."),
                 ("Yüzey alanı günlük hayatta nerede kullanılır?", "Bir kutuyu kaplamak ya da bir odanın duvarlarını boyamak için gereken malzemeyi hesaplarken."),
                 ("Bir prizmanın kaç farklı açınımı vardır?", "Birden fazla. Küpün bile 11 farklı açınımı vardır.")])


# ============================================================ 21. hacim
def u21():
    def birim():
        a, b, c = ri(2, 6), ri(2, 5), ri(2, 5)
        cells = [(x, y, z) for x in range(a) for y in range(b) for z in range(c)]
        if len(cells) > 60:
            return None
        return M("Birim küplerle oluşturulmuş dikdörtgenler prizmasının hacmi kaç birim küptür?" + KP.iso_cubes(cells, label="birim küplerden prizma", front=False, A=18),
                 num(a * b * c), [num(a * b + c), num(2 * (a * b + a * c + b * c)), num(a * b * c + a)],
                 "Taban: %d · %d = %d küp, %d kat: %d · %d = <b>%d</b>." % (a, b, a * b, c, a * b, c, a * b * c))

    def formul():
        a, b, c = ri(2, 20), ri(2, 15), ri(2, 12)
        return M("Ayrıtları %d cm, %d cm ve %d cm olan dikdörtgenler prizmasının hacmi kaç cm³’tür?" % (a, b, c), num(a * b * c),
                 [num(2 * (a * b + a * c + b * c)), num(a + b + c), num(a * b * c + a * b)], "V = taban alanı × yükseklik = %d · %d · %d = <b>%s cm³</b>." % (a, b, c, num(a * b * c)))

    def eksik():
        a, b, c = ri(2, 12), ri(2, 12), ri(2, 12)
        V = a * b * c
        return M("Hacmi %s cm³ olan dikdörtgenler prizmasının taban ayrıtları %d cm ve %d cm’dir. Yüksekliği kaç cm’dir?" % (num(V), a, b), num(c),
                 [num(c + 1), num(V // a), num(c * 2)], "h = V ÷ (taban alanı) = %s ÷ %d = <b>%d cm</b>." % (num(V), a * b, c))

    def akvaryum():
        a, b, c = ri(4, 10) * 10, ri(3, 6) * 10, ri(3, 6) * 10
        k = ch([F(1, 2), F(3, 4), F(2, 3), F(4, 5)])
        V = a * b * c
        if (V * k).denominator != 1 or ((V * k) % 1000):
            return None
        L = int(V * k) // 1000
        return M("Boyutları %d cm × %d cm × %d cm olan akvaryumun %s kadarı su doludur. Akvaryumda kaç litre su vardır? (1 L = 1 dm³ = 1000 cm³)" % (a, b, c, fr(k.numerator, k.denominator)),
                 "%s L" % num(L), ["%s L" % num(V // 1000), "%s L" % num(L * 10), "%s L" % num(V // 1000 - L) if V // 1000 != 2 * L else "%s L" % num(L + 5)],
                 "Hacim %s cm³ = %s L; %s kadarı: <b>%s L</b>." % (num(V), num(V // 1000), fr(k.numerator, k.denominator), num(L)))

    def sigar():
        a, b, c = ri(2, 6) * 10, ri(2, 5) * 10, ri(2, 5) * 10
        k = ch([5, 10])
        n = (a // k) * (b // k) * (c // k)
        return M("Ayrıtları %d cm, %d cm ve %d cm olan dikdörtgenler prizması biçimindeki bir kutuya bir ayrıtı %d cm olan küpler boşluk kalmadan yerleştirilecek. Kaç küp gerekir?" % (a, b, c, k),
                 num(n), [num(a * b * c // k), num((a + b + c) // k), num(n * 2)], "Her ayrıt boyunca %d, %d ve %d küp: %d · %d · %d = <b>%d</b>." % (a // k, b // k, c // k, a // k, b // k, c // k, n))

    def ayni():
        V = ch([24, 36, 48, 60, 72])
        trip = sorted({tuple(sorted((a, b, V // (a * b)))) for a in range(1, V + 1) for b in range(1, V + 1) if V % (a * b) == 0})
        n = len(trip)
        return M("Ayrıt uzunlukları birer doğal sayı (cm) olan, hacmi %d cm³ olan kaç farklı dikdörtgenler prizması vardır? (Ayrıtların sırası önemsiz)" % V, num(n),
                 [num(n + 1), num(n - 1), num(n + 3)], "%s: toplam <b>%d</b>." % (", ".join("%d×%d×%d" % t for t in trip), n))

    sets = [("Birim küplerle hacim", [(birim, 20)]),
            ("Hacim bağıntısı", [(formul, 20)]),
            ("Eksik ayrıt", [(eksik, 20)]),
            ("Problemler", [(akvaryum, 10), (sigar, 10)]),
            ("Karışık", [(formul, 6), (eksik, 5), (sigar, 5), (ayni, 4)])]
    return unit("dikdortgenler-prizmasinin-hacmi", "GN", "MAT.7.4.3, MAT.7.4.4, MAT.7.4.6", 21, "Dikdörtgenler Prizmasının Hacmi", "Prizmanın Hacmi",
                "Dikdörtgenler prizmasının hacmini birim küplerle yorumlar, hacim bağıntısını (taban alanı × yükseklik) değerlendirir ve hacimle ilgili günlük hayat problemlerini çözer.",
                "7. sınıf dikdörtgenler prizmasının hacmi çalışma kâğıdı: birim küplerle hacim, V = a · b · c, eksik ayrıtı bulma, akvaryum ve kutu problemleri. 100 soru ve cevap anahtarı.",
                "Hacim = taban alanı × yükseklik", "V = a · b · c (birim: cm³, m³).", sets,
                ["Hacim, bir cismin kapladığı yerin ölçüsüdür. Birim küplerle doldurup küpleri sayarak ölçebiliriz.",
                 "Tabana sığan küp sayısı taban alanına eşittir; bunu kat sayısıyla (yükseklik) çarparız: V = a · b · c.",
                 "Aynı hacme sahip, ayrıtları farklı birçok prizma vardır: 2 × 3 × 4 ile 1 × 4 × 6’nın hacmi 24’tür."],
                [("6 cm × 4 cm × 5 cm", ["6 · 4 · 5"], "120 cm³"), ("Hacim 180 cm³, taban 6 cm × 5 cm", ["180 ÷ 30"], "Yükseklik 6 cm")],
                [["Hacmi yüzey alanıyla karıştırmak", "Hacim cm³, alan cm²"],
                 ["Görünmeyen küpleri saymamak", "Taban × kat sayısı ile hesapla"],
                 ["Litreye çevirirken 1000’e bölmeyi unutmak", "1 L = 1000 cm³"]],
                [("Hacim ile sığa aynı mı?", "Sığa, bir kabın alabileceği sıvı miktarıdır; içi boş bir kabın hacmine eşittir ve genellikle litreyle ölçülür."),
                 ("Küpün hacmi nasıl bulunur?", "Bir ayrıtı a ise V = a · a · a = a³."),
                 ("Ayrıtlar farklı birimlerdeyse?", "Önce hepsini aynı birime çevir, sonra çarp.")])


# ============================================================ 22. hacim ölçü birimleri
VUNITS = [("m³", 0), ("dm³", 1), ("cm³", 2), ("mm³", 3)]
LIQ = [("L", 0), ("dL", 1), ("cL", 2), ("mL", 3)]


def u22():
    def kup_birim():
        (u1, i), (u2, j) = sh(VUNITS)[:2]
        if abs(i - j) > (2 if i > j else 1) and ri(0, 1):
            return None
        v = ri(1, 90) * ch([1, 1, 10])
        if i < j:
            r = v * 1000 ** (j - i)
        else:
            r = F(v, 1000 ** (i - j))
        w = [v * 10 ** (j - i) if j > i else F(v, 10 ** (i - j)), r * 10, r / 10]
        return M("%s %s = ? %s" % (num(v), u1, u2), ondalik(r), [ondalik(x) for x in w],
                 "Hacim birimleri 1000’er 1000’er büyür ve küçülür (%s → %s: %d basamak). Sonuç <b>%s %s</b>." % (u1, u2, abs(j - i), ondalik(r), u2))

    def sivi():
        (u1, i), (u2, j) = sh(LIQ)[:2]
        v = ri(1, 90) * ch([1, 10])
        r = v * 10 ** (j - i) if j > i else F(v, 10 ** (i - j))
        w = [r * 10, r / 10, v * 1000 ** (j - i) if j > i else F(v, 1000 ** (i - j))]
        return M("%s %s = ? %s" % (num(v), u1, u2), ondalik(r), [ondalik(x) for x in w],
                 "Sıvı ölçü birimleri 10’ar 10’ar değişir. Sonuç <b>%s %s</b>." % (ondalik(r), u2))

    def bag():
        S = [("1 dm³", "1 L"), ("1 cm³", "1 mL"), ("1 m³", "1000 L"), ("1000 cm³", "1 L"), ("1 dm³", "1000 mL")]
        a, g = ch(S)
        v = ri(2, 40)
        if a == "1 dm³":
            q, ans, w = "%d dm³ kaç litredir?" % v, "%d L" % v, ["%s L" % num(v * 1000), "%s L" % dq(F(v, 1000)), "%d L" % (v * 10)]
        elif a == "1 cm³":
            q, ans, w = "%d cm³ kaç mililitredir?" % v, "%d mL" % v, ["%s mL" % num(v * 1000), "%s mL" % dq(F(v, 10)), "%d mL" % (v * 10)]
        elif a == "1 m³":
            q, ans, w = "%d m³ kaç litredir?" % v, "%s L" % num(v * 1000), ["%d L" % v, "%s L" % num(v * 100), "%s L" % num(v * 1000000)]
        elif a == "1000 cm³":
            q, ans, w = "%s cm³ kaç litredir?" % num(v * 1000), "%d L" % v, ["%s L" % num(v * 100), "%d L" % (v * 10), "%s L" % num(v * 1000)]
        else:
            q, ans, w = "%d dm³ kaç mililitredir?" % v, "%s mL" % num(v * 1000), ["%d mL" % v, "%s mL" % num(v * 100), "%s mL" % num(v * 10)]
        return M(q, ans, w, "1 dm³ = 1 L ve 1 cm³ = 1 mL’dir. Sonuç <b>%s</b>." % ans)

    def sirala():
        vals = [(ri(1, 9), "L"), (ri(1, 9) * 100, "mL"), (ri(1, 9), "dm³"), (ri(1, 9) * 1000, "cm³")]
        mls = [v * {"L": 1000, "mL": 1, "dm³": 1000, "cm³": 1}[u] for v, u in vals]
        if len(set(mls)) < 4:
            return None
        k = ch(["en büyük", "en küçük"])
        i = mls.index(max(mls) if k == "en büyük" else min(mls))
        show = ["%s %s" % (num(v), u) for v, u in vals]
        return G.withopts(M("Hangisi %stür?" % k, show[i], [x for j, x in enumerate(show) if j != i],
                            "Hepsini mL’ye çeviririz: %s. %s: <b>%s</b>." % (", ".join("%s = %s mL" % (s, num(m)) for s, m in zip(show, mls)), cap(k), show[i])), "%s miktarları veriliyor.")

    def problem():
        a, b, c = ri(2, 8) * 10, ri(2, 6) * 10, ri(2, 6) * 10
        V = a * b * c
        s = ch([250, 200, 500])
        if V % s:
            return None
        return M("Boyutları %d cm × %d cm × %d cm olan dolu bir su deposundaki su, %d mL’lik bardaklara dolduruluyor. Kaç bardak dolar?" % (a, b, c, s), num(V // s),
                 [num(V // 1000), num(V // s * 10), num(V // (s * 10))], "%s cm³ = %s mL; %s ÷ %d = <b>%s</b> bardak." % (num(V), num(V), num(V), s, num(V // s)))

    sets = [("Küp birimler", [(kup_birim, 20)]),
            ("Sıvı ölçü birimleri", [(sivi, 20)]),
            ("Hacim ve sıvı ilişkisi", [(bag, 20)]),
            ("Karşılaştırma", [(sirala, 20)]),
            ("Problemler", [(problem, 10), (bag, 5), (kup_birim, 5)])]
    return unit("hacim-olcme-birimleri", "GN", "MAT.7.4.5", 22, "Hacim Ölçme Birimleri: m³, dm³, cm³ ve Litre", "Hacim Ölçme Birimleri",
                "Hacim ölçme birimleri arasındaki ilişkileri değerlendirir; metreküp ve litreyi ölçme birimi olarak belirler, küp ve sıvı ölçü birimlerini (dm³, cm³, mm³; dL, cL, mL) ilişkilendirir.",
                "7. sınıf hacim ölçme birimleri çalışma kâğıdı: m³, dm³, cm³, mm³ dönüşümleri, L, dL, cL, mL dönüşümleri, 1 dm³ = 1 L ve 1 cm³ = 1 mL, karşılaştırma ve problemler. 100 soru ve cevap anahtarı.",
                "1 dm³ = 1 L,  1 cm³ = 1 mL", "Küp birimler 1000’er, sıvı birimleri 10’ar değişir.", sets,
                ["Hacmin temel birimi metreküptür (m³). Küp birimler arasında 1000’er kat vardır: 1 m³ = 1000 dm³, 1 dm³ = 1000 cm³, 1 cm³ = 1000 mm³.",
                 "Sıvı ölçü birimleri 10’ar 10’ar değişir: 1 L = 10 dL = 100 cL = 1000 mL.",
                 "İki sistem şöyle bağlanır: 1 dm³ = 1 L ve 1 cm³ = 1 mL. Bu yüzden 1 m³ = 1000 L’dir."],
                [("3,5 m³ kaç litre", ["1 m³ = 1000 L"], "3500 L"), ("2500 cm³ kaç litre", ["1000 cm³ = 1 L"], "2,5 L")],
                [["Küp birimleri 10’ar çevirmek", "1 m³ = 1000 dm³ (100 değil)"],
                 ["1 L’yi 1 cm³ sanmak", "1 L = 1 dm³ = 1000 cm³"],
                 ["Büyük birimden küçüğe geçerken bölmek", "Büyükten küçüğe: çarp"]],
                [("Neden küp birimler 1000’er değişir?", "1 dm = 10 cm olduğundan 1 dm³ = 10 × 10 × 10 = 1000 cm³’tür."),
                 ("Bir ilaç şişesi neden mL ile ölçülür?", "Küçük miktarları göstermek için mililitre daha uygundur; 1 mL = 1 cm³."),
                 ("Su faturasında hangi birim kullanılır?", "Metreküp (m³). 1 m³ su 1000 litredir.")])


# ============================================================ 23. dairenin alanı
def sector(r_lab, ang, label="daire dilimi"):
    cx, cy, R = 110, 105, 80
    a = math.radians(ang)
    x2, y2 = cx + R * math.cos(-a), cy + R * math.sin(-a)
    large = 1 if ang > 180 else 0
    s = ["<svg viewBox='0 0 220 210' role='img' aria-label='%s'>" % label,
         "<circle cx='%d' cy='%d' r='%d' fill='#f4faf6' stroke='#006633' stroke-width='2'/>" % (cx, cy, R),
         "<path d='M%d %d L%d %d A%d %d 0 %d 0 %.1f %.1f Z' fill='#a8d5ba' stroke='#006633' stroke-width='2.4'/>" % (cx, cy, cx + R, cy, R, R, large, x2, y2),
         "<text x='%d' y='%d' font-size='14' fill='#2f6fc4' text-anchor='middle'>%s</text>" % (cx + R / 2, cy + 18, r_lab),
         "<text x='%.1f' y='%.1f' font-size='14' font-weight='700' text-anchor='middle'>%d°</text>" % (cx + 30 * math.cos(-a / 2), cy + 30 * math.sin(-a / 2) + 5, ang),
         "<circle cx='%d' cy='%d' r='3' fill='#222'/>" % (cx, cy)]
    return "<div class='qfig'>" + G.lg("".join(s) + "</svg>") + "</div>"


def u23():
    def alan():
        r = ri(2, 20)
        p = ch([3, F(314, 100)])
        A = p * r * r
        pt = "3" if p == 3 else "3,14"
        return M("Yarıçapı %d cm olan dairenin alanı kaç cm²’dir? (π = %s alınız.)" % (r, pt), dq(A), [dq(2 * p * r), dq(p * 2 * r * 2 * r), dq(p * r)],
                 "A = π · r² = %s · %d² = %s · %d = <b>%s cm²</b>." % (pt, r, pt, r * r, dq(A)))

    def cap_():
        d = ri(2, 15) * 2
        A = 3 * (d // 2) ** 2
        return M("Çapı %d cm olan dairenin alanı kaç cm²’dir? (π = 3)" % d, num(A), [num(3 * d * d), num(3 * d), num(3 * d // 2)],
                 "r = %d ÷ 2 = %d; A = 3 · %d² = <b>%d cm²</b>." % (d, d // 2, d // 2, A))

    def ters():
        r = ri(2, 15)
        A = 3 * r * r
        return M("Alanı %s cm² olan dairenin yarıçapı kaç cm’dir? (π = 3)" % num(A), num(r), [num(r * r), num(2 * r), num(r + 1)],
                 "3 · r² = %d → r² = %d → r = <b>%d cm</b>." % (A, r * r, r))

    def dilim():
        r = ri(2, 12) * 2
        ang = ch([30, 45, 60, 90, 120, 150, 180, 240, 270])
        A = F(3 * r * r * ang, 360)
        if A.denominator != 1:
            return None
        return M("Şekildeki daire diliminin alanı kaç cm²’dir? (π = 3)" + sector("r = %d cm" % r, ang), num(A), [num(3 * r * r), num(A * 2), dq(F(2 * 3 * r * ang, 360))],
                 "Dilim alanı = π r² · (α ÷ 360) = 3 · %d · %d/360 = <b>%s cm²</b>." % (r * r, ang, num(A)))

    def aci():
        r = ri(2, 10) * 2
        ang = ch([30, 45, 60, 72, 90, 120, 135, 150, 180])
        A = F(3 * r * r * ang, 360)
        if A.denominator != 1:
            return None
        return M("Yarıçapı %d cm olan bir dairede alanı %s cm² olan daire diliminin merkez açısı kaç derecedir? (π = 3)" % (r, num(A)), "%d°" % ang,
                 ["%d°" % (ang * 2 if ang < 180 else ang // 2), "%d°" % (360 - ang), "%d°" % (ang + 30)], "α/360 = %s ÷ %d → α = <b>%d°</b>." % (num(A), 3 * r * r, ang))

    def pizza():
        r = ri(10, 20)
        n = ch([4, 6, 8, 12])
        A = F(3 * r * r, n)
        return M("Yarıçapı %d cm olan daire biçimindeki pizza %d eş dilime ayrıldı. Bir dilimin alanı kaç cm²’dir? (π = 3)" % (r, n), dq(A),
                 [num(3 * r * r), dq(F(3 * r * r, n * 2)), dq(F(6 * r, n))], "Pizzanın alanı 3 · %d = %d cm²; bunu %d eş parçaya böleriz: <b>%s cm²</b>." % (r * r, 3 * r * r, n, dq(A)))

    sets = [("Dairenin alanı", [(alan, 20)]),
            ("Çap ve yarıçap", [(cap_, 10), (ters, 10)]),
            ("Daire dilimi", [(dilim, 20)]),
            ("Merkez açı", [(aci, 20)]),
            ("Problemler", [(pizza, 12), (dilim, 8)])]
    return unit("dairenin-ve-daire-diliminin-alani", "GN", "MAT.7.4.7, MAT.7.4.8, MAT.7.4.10", 23, "Dairenin ve Daire Diliminin Alanı", "Dairenin Alanı",
                "Dikdörtgen ve paralelkenarın alanı ile çemberin uzunluğuna ilişkin deneyimlerini dairenin alan bağıntısına yansıtır; merkez açı ile daire diliminin alanı arasındaki ilişkiyi akıl yürüterek belirler.",
                "7. sınıf dairenin ve daire diliminin alanı çalışma kâğıdı: A = π r², çap ve yarıçaptan alan, alandan yarıçap, daire diliminin alanı, merkez açı, pizza problemleri. 100 soru ve cevap anahtarı.",
                "Dairenin alanı = π · r²", "Daire dilimi = π r² · (merkez açı ÷ 360°)", sets,
                ["Daireyi çok sayıda ince dilime ayırıp yan yana dizersek yaklaşık bir paralelkenar elde ederiz: tabanı πr (yarım çevre), yüksekliği r. Alan π · r · r = πr².",
                 "Daire diliminin alanı merkez açısıyla orantılıdır: merkez açı 90° ise dilim dairenin 90/360 = 1/4’üdür.",
                 "Hesaplarda soruda verilen π değerini (3 ya da 3,14) kullanırız."],
                [("r = 5 cm, π = 3", ["3 · 25"], "75 cm²"), ("r = 6 cm, merkez açı 120°", ["3 · 36 = 108", "108 · 120/360"], "36 cm²")],
                [["Çapı yarıçap gibi kullanmak", "Çap 10 ise r = 5"],
                 ["r² yerine 2r almak", "r² = r · r"],
                 ["Alanı çevreyle karıştırmak", "Çevre 2πr, alan πr²"]],
                [("π nedir?", "Bir çemberin uzunluğunun çapına oranıdır; yaklaşık 3,14’tür."),
                 ("Yarıçap iki katına çıkarsa alan ne olur?", "4 katına çıkar, çünkü r² iki kez çarpılır."),
                 ("Daire dilimi nerede görülür?", "Pasta dilimleri, saatin akrebinin taradığı alan, daire grafikleri.")])


# ============================================================ 24. eşkenar dörtgen ve yamuk
def u24():
    def eskenar():
        e, f = ri(2, 20) * 2, ri(2, 20)
        return M("Köşegen uzunlukları %d cm ve %d cm olan eşkenar dörtgenin alanı kaç cm²’dir?" % (e, f), num(e * f // 2), [num(e * f), num(e + f), num(2 * (e + f))],
                 "Alan = (e · f) ÷ 2 = %d · %d ÷ 2 = <b>%s cm²</b>." % (e, f, num(e * f // 2)))

    def yamuk():
        a, c = ri(3, 25), ri(3, 25)
        if a == c:
            return None
        h = ri(2, 15)
        if (a + c) * h % 2:
            h += 1
        A = (a + c) * h // 2
        return M("Paralel kenarları %d cm ve %d cm, yüksekliği %d cm olan yamuğun alanı kaç cm²’dir?" % (a, c, h) + yamuk_fig(a, c, h),
                 num(A), [num((a + c) * h), num(a * c * h // 2) if a * c * h % 2 == 0 else num(a * h), num(A + h)],
                 "Alan = (a + c) · h ÷ 2 = (%d + %d) · %d ÷ 2 = <b>%s cm²</b>." % (a, c, h, num(A)))

    def yamuk_h():
        a, c = ri(3, 20), ri(3, 20)
        if a == c:
            return None
        h = ri(2, 12) * 2
        A = (a + c) * h // 2
        return M("Alanı %s cm², paralel kenarları %d cm ve %d cm olan yamuğun yüksekliği kaç cm’dir?" % (num(A), a, c), num(h), [num(h // 2), num(2 * h), num(h + 1)],
                 "(%d + %d) · h ÷ 2 = %s → h = %s · 2 ÷ %d = <b>%d cm</b>." % (a, c, num(A), num(A), a + c, h))

    def esk_kosegen():
        e = ri(3, 15) * 2
        f = ri(3, 20)
        A = e * f // 2
        return M("Alanı %s cm² olan eşkenar dörtgenin bir köşegeni %d cm’dir. Diğer köşegeni kaç cm’dir?" % (num(A), e), num(f), [num(A // e), num(2 * A), num(f + 2)],
                 "e · f ÷ 2 = %s → f = 2 · %s ÷ %d = <b>%d cm</b>." % (num(A), num(A), e, f))

    def bahce():
        a, c, h = ri(5, 30) * 2, ri(5, 30) * 2, ri(4, 20)
        if a == c:
            return None
        p = ch([5, 8, 10, 12, 15])
        A = (a + c) * h // 2
        return M("Paralel kenarları %d m ve %d m, yüksekliği %d m olan yamuk biçimindeki bir bahçenin her metrekaresine %d TL’lik çim ekilecek. Toplam kaç TL ödenir?" % (a, c, h, p),
                 "%s TL" % num(A * p), ["%s TL" % num((a + c) * h * p), "%s TL" % num(A), "%s TL" % num((a + c + h) * p)], "Alan (%d + %d) · %d ÷ 2 = %s m²; %s · %d = <b>%s TL</b>." % (a, c, h, num(A), num(A), p, num(A * p)))

    sets = [("Eşkenar dörtgenin alanı", [(eskenar, 20)]),
            ("Yamuğun alanı", [(yamuk, 20)]),
            ("Eksik uzunluk", [(yamuk_h, 10), (esk_kosegen, 10)]),
            ("Problemler", [(bahce, 20)]),
            ("Karışık", [(eskenar, 7), (yamuk, 7), (esk_kosegen, 6)])]
    return unit("eskenar-dortgen-ve-yamugun-alani", "GN", "MAT.7.4.9, MAT.7.4.10", 24, "Eşkenar Dörtgen ve Yamuğun Alanı", "Eşkenar Dörtgen ve Yamuk",
                "Eşkenar dörtgen ve yamuğun alan bağıntılarına dair çıkarım yapar; şekilleri ayırıp tamamlayarak alanlarını belirler ve günlük hayat problemlerini çözer.",
                "7. sınıf eşkenar dörtgen ve yamuğun alanı çalışma kâğıdı: köşegenlerle eşkenar dörtgenin alanı, yamuğun alanı, alandan yükseklik ve köşegen bulma, bahçe problemleri. 100 soru ve cevap anahtarı.",
                "Yamuk: (a + c) · h ÷ 2", "Eşkenar dörtgen: köşegenlerin çarpımının yarısı.", sets,
                ["Eşkenar dörtgenin köşegenleri birbirine diktir. Şekli köşegenlerle bir dikdörtgenin içine yerleştirirsek dikdörtgenin yarısını kapladığını görürüz: A = e · f ÷ 2.",
                 "Yamuğun bir eşini ters çevirip yanına koyarsak tabanı (a + c), yüksekliği h olan bir paralelkenar elde ederiz. Yamuk bunun yarısıdır: A = (a + c) · h ÷ 2.",
                 "Alan verilip bir uzunluk sorulursa bağıntıyı yazar, bilinmeyeni yalnız bırakırız."],
                [("Köşegenler 10 cm ve 6 cm", ["10 · 6 ÷ 2"], "30 cm²"), ("Paralel kenarlar 8 ve 12 cm, h = 5 cm", ["(8 + 12) · 5 ÷ 2"], "50 cm²")],
                [["Yamukta 2’ye bölmeyi unutmak", "(a + c) · h ÷ 2"],
                 ["Yamukta yan kenarı yükseklik sanmak", "Yükseklik paralel kenarlara diktir"],
                 ["Eşkenar dörtgende kenarla köşegeni karıştırmak", "Alan köşegenlerle hesaplanır"]],
                [("Kare bir eşkenar dörtgen midir?", "Evet. Kenarları eşit olduğu için kare özel bir eşkenar dörtgendir."),
                 ("Paralelkenarın alanı ile yamuğunki nasıl ilişkili?", "İki eş yamuk birleşince paralelkenar olur; yamuk onun yarısıdır."),
                 ("Bu alanlar nerede kullanılır?", "Tarla, bahçe, çatı ve uçurtma gibi şekillerin alanını hesaplarken.")])


def yamuk_fig(a, c, h):
    sc = 200.0 / max(a, c, h * 1.6)
    A_, C_, H_ = a * sc, c * sc, h * sc
    off = (A_ - C_) / 2 if A_ > C_ else -(C_ - A_) / 2
    pts = [(0, H_), (A_, H_), (off + C_, 0), (off, 0)]
    return "<div class='qfig'>" + G.lg(G.poly(pts, side_labels=[num(a), "", num(c), ""], label="yamuk")) + "</div>"


# ============================================================ 25. veri analizi
def mad(xs):
    m = F(sum(xs), len(xs))
    return m, sum(abs(x - m) for x in xs) / len(xs)


def u25():
    def data(n=None):
        n = n or ch([5, 6, 8, 10])
        while True:
            xs = [ri(2, 30) for _ in range(n)]
            m = F(sum(xs), n)
            if m.denominator == 1 and mad(xs)[1].denominator <= 10 and is_dec(mad(xs)[1]):
                return xs

    def ort():
        xs = data()
        m = F(sum(xs), len(xs))
        return M("%s verilerinin aritmetik ortalaması kaçtır?" % ", ".join(map(str, xs)), num(m), [num(m + 1), num(sorted(xs)[len(xs) // 2]) if sorted(xs)[len(xs) // 2] != m else num(m - 1), num(sum(xs))],
                 "Toplam %d, veri sayısı %d: %d ÷ %d = <b>%s</b>." % (sum(xs), len(xs), sum(xs), len(xs), num(m)))

    def aciklik():
        xs = data()
        r = max(xs) - min(xs)
        return M("%s verilerinin açıklığı kaçtır?" % ", ".join(map(str, xs)), num(r), [num(max(xs) + min(xs)), num(r + 1), num(abs(xs[-1] - xs[0])) if abs(xs[-1] - xs[0]) != r else num(r - 1)],
                 "Açıklık = en büyük − en küçük = %d − %d = <b>%d</b>." % (max(xs), min(xs), r))

    def sapma():
        xs = data(ch([4, 5, 6]))
        m, d = mad(xs)
        return M("%s verilerinin ortalama mutlak sapması kaçtır?" % ", ".join(map(str, xs)), dq(d), [dq(d + 1), dq(m), dq(d * 2)],
                 "Ortalama %s. Uzaklıklar: %s. Ortalaması: <b>%s</b>." % (num(m), ", ".join(dq(abs(x - m)) for x in xs), dq(d)))

    def karsilas():
        n1, n2 = G.K.two()
        a, b = data(5), data(5)
        da, db = mad(a)[1], mad(b)[1]
        if da == db:
            return None
        g = n1 if da < db else n2
        return M("Son 5 haftada okunan sayfa sayılarının ortalama mutlak sapması %s için %s, %s için %s’dir. Okuma alışkanlığı daha düzenli (az değişken) olan kimdir?" % (n1, dq(da), n2, dq(db)),
                 g, [n2 if g == n1 else n1, "İkisi aynı", "Bilinemez"], "Ortalama mutlak sapma küçük olan dağılım daha az yayılır: <b>%s</b>." % g)

    def cizgi():
        ays = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
        vs = [ri(2, 30) for _ in ays]
        W, H = 380, 220
        s = ["<svg viewBox='0 0 %d %d' role='img' aria-label='çizgi grafiği'>" % (W, H), "<line x1='40' y1='180' x2='370' y2='180' stroke='#333'/><line x1='40' y1='180' x2='40' y2='10' stroke='#333'/>"]
        for v in range(0, 31, 5):
            y = 180 - v * 5.5
            s.append("<line x1='40' y1='%.0f' x2='370' y2='%.0f' stroke='#e3ded4'/><text x='34' y='%.0f' font-size='11' text-anchor='end'>%d</text>" % (y, y, y + 4, v))
        pts = []
        for i, (a, v) in enumerate(zip(ays, vs)):
            x = 70 + i * 56
            pts.append("%d,%.0f" % (x, 180 - v * 5.5))
            s.append("<text x='%d' y='198' font-size='12' text-anchor='middle'>%s</text><circle cx='%d' cy='%.0f' r='4' fill='#c0392b'/><text x='%d' y='%.0f' font-size='11' text-anchor='middle' fill='#c0392b'>%d</text>" % (x, a, x, 180 - v * 5.5, x, 180 - v * 5.5 - 8, v))
        s.append("<polyline points='%s' fill='none' stroke='#c0392b' stroke-width='2.4'/>" % " ".join(pts))
        fig = "<div class='qfig'>" + G.lg("".join(s) + "</svg>") + "</div>"
        diffs = [(vs[i + 1] - vs[i], i) for i in range(5)]
        k = ch(["artış", "azalış"])
        best = max(diffs) if k == "artış" else min(diffs)
        if (k == "artış" and best[0] <= 0) or (k == "azalış" and best[0] >= 0) or [d for d, _ in diffs].count(best[0]) > 1:
            return None
        i = best[1]
        g = "%s – %s" % (ays[i], ays[i + 1])
        w = ["%s – %s" % (ays[j], ays[j + 1]) for j in range(5) if j != i]
        return M("Grafik bir şehirde aylık yağışlı gün sayısını gösteriyor. En büyük %s hangi iki ay arasındadır?" % k + fig, g, sh(w),
                 "Ardışık aylar arasındaki farklara bakarız: en büyük %s %s ayları arasında (%s gün)." % (k, g, sn(best[0])) + " Cevap <b>%s</b>." % g)

    sets = [("Ortalama ve açıklık", [(ort, 10), (aciklik, 10)]),
            ("Ortalama mutlak sapma", [(sapma, 20)]),
            ("Dağılımları karşılaştırma", [(karsilas, 20)]),
            ("Çizgi grafiği", [(cizgi, 20)]),
            ("Karışık", [(sapma, 7), (ort, 7), (cizgi, 6)])]
    return unit("veri-analizi-ve-ortalama-mutlak-sapma", "IA", "MAT.7.6.1, MAT.7.6.2", 25, "Veri Analizi: Açıklık, Ortalama Mutlak Sapma ve Çizgi Grafiği", "Veri Analizi",
                "Kategorik veya nicel (sürekli) veriyle çalışır ve veriye dayalı karar verir; çizgi ve nokta grafiği, ortalama, açıklık ve ortalama mutlak sapma gibi araçları seçer, başkalarının istatistiksel yorumlarını tartışır.",
                "7. sınıf veri analizi çalışma kâğıdı: aritmetik ortalama, açıklık, ortalama mutlak sapma, iki dağılımı karşılaştırma, çizgi grafiğinde artış ve azalış. 100 soru ve cevap anahtarı.",
                "Ortalama mutlak sapma = yayılım", "Ortalamaya uzaklıkların ortalaması; küçükse tutarlı.", sets,
                ["Ortalama, verilerin merkezini; açıklık (en büyük − en küçük) ve ortalama mutlak sapma, verilerin ne kadar yayıldığını gösterir.",
                 "Ortalama mutlak sapma: önce ortalamayı bul, her verinin ortalamaya uzaklığını (mutlak değerle) yaz, bu uzaklıkların ortalamasını al.",
                 "Zamanla değişen veriler çizgi grafiğiyle gösterilir; noktaları birleştiren çizginin eğimi artış ve azalışı gösterir."],
                [("4, 6, 8, 10, 12", ["Ortalama 8", "Uzaklıklar 4, 2, 0, 2, 4", "12 ÷ 5"], "2,4"), ("Açıklık: 3, 9, 15, 7", ["15 − 3"], "12")],
                [["Uzaklıkları işaretiyle toplamak", "Mutlak değer alınır; uzaklık negatif olmaz"],
                 ["Açıklığı ilk ve son veriden bulmak", "En büyük ve en küçük veriyi kullan"],
                 ["Sapması büyük veriyi daha tutarlı sanmak", "Sapma küçükse veriler birbirine yakındır"]],
                [("Ortalama mutlak sapma neden kullanılır?", "İki grubun ortalaması aynı olsa bile hangisinin daha dağınık olduğunu gösterir."),
                 ("Çizgi grafiği hangi veriler için uygundur?", "Zamana göre değişen sürekli veriler (sıcaklık, boy, satış) için."),
                 ("Bir yorumun yanlı olduğunu nasıl anlarım?", "Örneklem küçükse ya da tek bir gruptan seçildiyse sonuç genele yayılamaz.")])


def is_dec(x):
    d = F(x).denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


# ============================================================ 26. olasılık ve tümleyen
BAGS = [("kırmızı", "mavi", "yeşil", "sarı")]


def u26():
    def torba():
        cs = ["kırmızı", "mavi", "yeşil", "sarı"][:ri(2, 4)]
        ns = [ri(1, 9) for _ in cs]
        T = sum(ns)
        i = ri(0, len(cs) - 1)
        p = F(ns[i], T)
        return M("Bir torbada %s top var. Torbadan rastgele çekilen bir topun %s olma olasılığı kaçtır?" % (", ".join("%d %s" % (n, c) for n, c in zip(ns, cs)), cs[i]),
                 sn(p), [sn(F(ns[i], T - ns[i])) if T > ns[i] else "1", sn(F(T - ns[i], T)), sn(F(1, len(cs)))],
                 "Olasılık = istenen çıktı sayısı ÷ tüm çıktı sayısı = %d/%d = <b>%s</b>." % (ns[i], T, sn(p)))

    def tumleyen():
        a, b = ri(1, 19), ri(21, 40)
        if a >= b:
            return None
        p = F(a, b)
        return M("Bir olayın olma olasılığı %s ise bu olayın olmama (tümleyen olayın) olasılığı kaçtır?" % sn(p), sn(1 - p), [sn(p), sn(F(b, a)), sn(F(b - a, 2 * b))],
                 "P(A) + P(A′) = 1 → P(A′) = 1 − %s = <b>%s</b>." % (sn(p), sn(1 - p)))

    def zar():
        S = [("çift sayı", [2, 4, 6]), ("tek sayı", [1, 3, 5]), ("asal sayı", [2, 3, 5]), ("3’ten büyük", [4, 5, 6]), ("4’ten küçük", [1, 2, 3]),
             ("5 ya da 6", [5, 6]), ("6’nın böleni", [1, 2, 3, 6]), ("3’ün katı", [3, 6]), ("1’den büyük", [2, 3, 4, 5, 6]), ("2", [2]),
             ("5’ten küçük", [1, 2, 3, 4]), ("2’den büyük", [3, 4, 5, 6]), ("1 ya da 2", [1, 2]), ("4", [4])]
        t, xs = ch(S)
        k = ch(["gelme", "gelmeme"])
        p = F(len(xs), 6) if k == "gelme" else F(6 - len(xs), 6)
        return M("Bir zar atılıyor. Üst yüze %s %s olasılığı kaçtır?" % (t, k), sn(p), [sn(1 - p), sn(F(len(xs), 5)), sn(F(1, 6)), sn(F(len(xs) + 1, 6)), sn(F(1, 3))],
                 "Örnek uzay {1, 2, 3, 4, 5, 6}. İstenen: %s → %s; olasılık <b>%s</b>." % (t, "{%s}" % ", ".join(map(str, xs)) if k == "gelme" else "tümleyeni, 6 − %d = %d çıktı" % (len(xs), 6 - len(xs)), sn(p)))

    def esit():
        S = [("Hilesiz bir madeni para atıldığında yazı ya da tura gelmesi", "Eşit olasılıklıdır"),
             ("Hilesiz bir zar atıldığında 1 ya da 6 gelmesi", "Eşit olasılıklıdır"),
             ("3 kırmızı ve 5 mavi top bulunan torbadan kırmızı ya da mavi top çekilmesi", "Eşit olasılıklı değildir"),
             ("Bir zar atıldığında çift sayı ya da tek sayı gelmesi", "Eşit olasılıklıdır"),
             ("Bir zar atıldığında 6 ya da 6’dan küçük bir sayı gelmesi", "Eşit olasılıklı değildir"),
             ("4 eş parçalı çarkta kırmızı ya da mavi gelmesi (2 parça kırmızı, 1 mavi, 1 sarı)", "Eşit olasılıklı değildir"),
             ("Alfabeden rastgele seçilen bir harfin sesli ya da sessiz olması", "Eşit olasılıklı değildir"),
             ("İçinde 4 sarı ve 4 yeşil kalem bulunan kutudan sarı ya da yeşil kalem çekilmesi", "Eşit olasılıklıdır")]
        t, g = ch(S)
        return M("%s durumu için hangisi doğrudur?" % t, g, ["Eşit olasılıklı değildir" if g.startswith("Eşit olasılıklıdır") else "Eşit olasılıklıdır", "Olasılık hesaplanamaz", "İkisi de kesin olaydır"],
                 "Çıktıların olasılıkları aynıysa olaylar eşit olasılıklıdır. Cevap: <b>%s</b>." % g)

    def kac():
        T = ch([12, 18, 20, 24, 30, 36, 40, 48, 60, 120])
        p = ch([F(1, 4), F(1, 5), F(1, 3), F(2, 5), F(3, 4), F(1, 6)])
        if (T * p).denominator != 1:
            return None
        n = int(T * p)
        return M("Bir kutuda %d kart var. Rastgele çekilen bir kartın mavi olma olasılığı %s ise kutuda kaç mavi kart vardır?" % (T, sn(p)), num(n),
                 [num(T - n), num(p.denominator), num(n + 1)], "%d · %s = <b>%d</b>." % (T, sn(p), n))

    sets = [("Torbadan top çekme", [(torba, 20)]),
            ("Zar", [(zar, 20)]),
            ("Tümleyen olay", [(tumleyen, 20)]),
            ("Eşit olasılık", [(esit, 8), (kac, 12)]),
            ("Karışık", [(torba, 9), (zar, 5), (kac, 6)])]
    return unit("teorik-olasilik-ve-tumleyen-olay", "VO", "MAT.7.7.1, MAT.7.7.2", 26, "Teorik Olasılık, Tümleyen Olay ve Eşit Olasılık", "Teorik Olasılık",
                "Bir olayın ve tümleyeninin olasılığına ilişkin tümevarımsal akıl yürütür; aynı deneye ait olayların eşit olasılıklı olup olmadığını değerlendirir.",
                "7. sınıf teorik olasılık çalışma kâğıdı: örnek uzay, torbadan top çekme ve zar atma olasılıkları, tümleyen olay (1 − P), eşit olasılıklı olaylar, olasılıktan sayıyı bulma. 100 soru ve cevap anahtarı.",
                "P = istenen ÷ tüm çıktılar", "Bir olay ile tümleyeninin olasılıkları toplamı 1’dir.", sets,
                ["Bir deneyin tüm olası çıktılarının kümesine örnek uzay denir. Zar için {1, 2, 3, 4, 5, 6}.",
                 "Çıktılar eşit şanslıysa bir olayın olasılığı = istenen çıktı sayısı ÷ tüm çıktı sayısıdır. Olasılık 0 ile 1 arasındadır.",
                 "Bir olayın gerçekleşmemesi tümleyen olaydır: P(A′) = 1 − P(A)."],
                [("3 kırmızı, 5 mavi top; kırmızı", ["3 ÷ 8"], "3/8"), ("P(A) = 2/7 ise P(A′)", ["1 − 2/7"], "5/7")],
                [["Payda olarak yalnızca diğer renkleri saymak", "Payda tüm topların sayısıdır"],
                 ["Tümleyeni 1’den çıkarmayı unutmak", "P(olmama) = 1 − P(olma)"],
                 ["Her rengin olasılığını eşit sanmak", "Sayıları farklıysa olasılıklar da farklıdır"]],
                [("Olasılık 1’den büyük olabilir mi?", "Hayır. Kesin olayın olasılığı 1, imkânsız olayınki 0’dır; diğerleri aradadır."),
                 ("Eşit olasılık ne demektir?", "Çıktıların her birinin gerçekleşme şansının aynı olmasıdır, hilesiz zar gibi."),
                 ("Teorik olasılık ile deneysel olasılık farkı nedir?", "Teorik olasılık hesapla bulunur; deneysel olasılık deney sonuçlarından elde edilir.")])


# ============================================================ 27. ayrık olaylar
def u27():
    EV = [("çift sayı gelmesi", {2, 4, 6}), ("tek sayı gelmesi", {1, 3, 5}), ("asal sayı gelmesi", {2, 3, 5}), ("3’ten büyük sayı gelmesi", {4, 5, 6}),
          ("4’ten küçük sayı gelmesi", {1, 2, 3}), ("6 gelmesi", {6}), ("1 gelmesi", {1}), ("3’ün katı gelmesi", {3, 6}), ("5’ten büyük sayı gelmesi", {6}),
          ("2’den küçük sayı gelmesi", {1}), ("4 gelmesi", {4})]

    def ayrik():
        (t1, s1), (t2, s2) = sh(EV)[:2]
        ok = not (s1 & s2)
        g = "Ayrık olaylardır" if ok else "Ayrık olaylar değildir"
        return M("Bir zar atılıyor. A: %s, B: %s. A ve B için hangisi doğrudur?" % (t1, t2), g, ["Ayrık olaylar değildir" if ok else "Ayrık olaylardır", "Tümleyen olaylardır", "İkisi de imkânsız olaydır"],
                 "A = {%s}, B = {%s}. %s" % (", ".join(map(str, sorted(s1))), ", ".join(map(str, sorted(s2))), "Ortak çıktı yok: <b>ayrık</b>." if ok else "Ortak çıktı var (%s): <b>ayrık değil</b>." % ", ".join(map(str, sorted(s1 & s2)))))

    def ortak():
        (t1, s1), (t2, s2) = sh(EV)[:2]
        c = s1 & s2
        if not c:
            return None
        g = "{%s}" % ", ".join(map(str, sorted(c)))
        w = ["{%s}" % ", ".join(map(str, sorted(s1 | s2))), "{%s}" % ", ".join(map(str, sorted(s1))), "{%s}" % ", ".join(map(str, sorted(s2))), "Ortak çıktı yoktur"]
        return M("Bir zar atılıyor. A: %s, B: %s. A ve B olaylarının ortak çıktıları hangisidir?" % (t1, t2), g, w,
                 "A = {%s}, B = {%s}; ikisinde de olan: <b>%s</b>." % (", ".join(map(str, sorted(s1))), ", ".join(map(str, sorted(s2))), g))

    def hangisi():
        (t1, s1) = ch(EV)
        dis = [(t, s) for t, s in EV if not (s & s1) and t != t1]
        nd = [(t, s) for t, s in EV if (s & s1) and t != t1]
        if not dis or len(nd) < 3:
            return None
        g = ch(dis)
        return G.withopts(M("Bir zar atılıyor. ‘%s’ olayı ile ayrık olan olay hangisidir?" % t1, g[0], [t for t, _ in sh(nd)[:3]],
                 "Ayrık olayların ortak çıktısı yoktur. {%s} ile {%s}: <b>%s</b>." % (", ".join(map(str, sorted(s1))), ", ".join(map(str, sorted(g[1]))), g[0])), "Olaylar: %s.")

    KART = [("1’den 20’ye kadar numaralı kartlar", range(1, 21)), ("1’den 15’e kadar numaralı kartlar", range(1, 16)), ("1’den 30’a kadar numaralı kartlar", range(1, 31))]
    PR = [("çift sayı", lambda n: n % 2 == 0), ("tek sayı", lambda n: n % 2 == 1), ("5’in katı", lambda n: n % 5 == 0), ("3’ün katı", lambda n: n % 3 == 0),
          ("10’dan büyük", lambda n: n > 10), ("asal sayı", lambda n: n > 1 and all(n % d for d in range(2, n))), ("4’ün katı", lambda n: n % 4 == 0)]

    def kart():
        (tk, rg) = ch(KART)
        (a, fa), (b, fb) = sh(PR)[:2]
        c = [n for n in rg if fa(n) and fb(n)]
        g = "Ayrık değildir (ortak çıktı: %s)" % ", ".join(map(str, c[:3])) + ("…" if len(c) > 3 else "") if c else "Ayrıktır"
        short = "Ayrık değildir" if c else "Ayrıktır"
        return M("%s karıştırılıp bir kart çekiliyor. ‘%s olması’ ile ‘%s olması’ olayları ayrık mıdır?" % (tk, a, b), short, ["Ayrıktır" if c else "Ayrık değildir", "Tümleyendir", "Kesin olaydır"],
                 g + ". Cevap: <b>%s</b>." % short)

    def tum_ayrik():
        S = [("Bir olay ile tümleyeni ayrık mıdır?", "Evet, her zaman", ["Hayır, hiçbir zaman", "Bazen", "Yalnızca zar için"]),
             ("Ayrık olayların ortak çıktı sayısı kaçtır?", "0", ["1", "2", "Hepsi"]),
             ("İki olay ayrık ise ikisi birlikte gerçekleşebilir mi?", "Hayır", ["Evet", "Bazen", "Yalnızca olasılıkları eşitse"]),
             ("Ayrık iki olaydan biri gerçekleşirse diğeri için ne söylenir?", "Gerçekleşmez", ["Kesin gerçekleşir", "Olasılığı artar", "Tümleyenidir"])]
        q, g, w = ch(S)
        return M(q, g, w, "Ayrık olayların ortak çıktısı yoktur; aynı anda gerçekleşemezler. Bir olay ile tümleyeni her zaman ayrıktır. Cevap: <b>%s</b>." % g)

    sets = [("Ayrık mı?", [(ayrik, 20)]),
            ("Ortak çıktılar", [(ortak, 20)]),
            ("Ayrık olanı bulma", [(hangisi, 20)]),
            ("Kart çekme", [(kart, 20)]),
            ("Karışık", [(tum_ayrik, 4), (ayrik, 6), (kart, 5), (ortak, 5)])]
    return unit("ayrik-ve-ayrik-olmayan-olaylar", "VO", "MAT.7.7.3", 27, "Ayrık ve Ayrık Olmayan Olaylar", "Ayrık Olaylar",
                "Olayları çıktıların ortak olup olmamasına göre ayrık olan ve ayrık olmayan olaylar olarak sınıflandırır ve etiketler.",
                "7. sınıf ayrık ve ayrık olmayan olaylar çalışma kâğıdı: zar ve kart deneylerinde iki olayın ortak çıktıları, ayrık olup olmama, ayrık olayı bulma, tümleyen olay ile ilişkisi. 100 soru ve cevap anahtarı.",
                "Ayrık: ortak çıktı yok", "Aynı anda gerçekleşemeyen olaylar ayrıktır.", sets,
                ["Bir olay, örnek uzayın bir alt kümesidir. Zar atıldığında ‘çift gelmesi’ = {2, 4, 6}.",
                 "İki olayın ortak çıktısı yoksa bu olaylar ayrıktır; aynı anda gerçekleşemezler: ‘1 gelmesi’ ve ‘çift gelmesi’.",
                 "Ortak çıktısı olan olaylar ayrık değildir: ‘çift gelmesi’ ve ‘asal gelmesi’ (ortak: 2)."],
                [("Çift gelmesi ve 3’ten büyük gelmesi", ["{2, 4, 6} ve {4, 5, 6}", "Ortak: 4, 6"], "Ayrık değil"), ("Tek gelmesi ve 6 gelmesi", ["{1, 3, 5} ve {6}"], "Ayrık")],
                [["Ayrık olayı tümleyen olayla karıştırmak", "Tümleyenler ayrıktır ama ayrık olaylar tümleyen olmak zorunda değildir"],
                 ["Ortak çıktıyı gözden kaçırmak", "2 hem çift hem asaldır"],
                 ["Çıktıları eksik yazmak", "Önce iki olayın kümesini tam yaz"]],
                [("Tümleyen olaylar ayrık mıdır?", "Evet. Bir olay ile gerçekleşmemesi aynı anda olamaz."),
                 ("Ayrık olaylar neden önemlidir?", "Ayrık olayların ‘ya biri ya diğeri’ olasılığı, olasılıkları toplanarak bulunur."),
                 ("Bir olay kendisiyle ayrık olabilir mi?", "Yalnızca imkânsız olay (boş küme) kendisiyle ayrıktır.")])


UNITS = [u19, u20, u21, u22, u23, u24, u25, u26, u27]
