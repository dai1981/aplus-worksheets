# -*- coding: utf-8 -*-
"""Türkiye 12. sınıf (2026 DÖP)：MAT.12.3 geometrik cisimler、MAT.12.4 değişimin matematiği（limit, süreklilik, türev）、MAT.12.5 hazır veriler。"""
import math
from fractions import Fraction as F
from tr_lise import M, num, sn, par, lin, dq, MINUS, ri, ch, sh, nz, frs, U, W3, rts, rt, poly, peval
from tr_s12a import pis, pmul, fct


def setup(rnd):
    pass


def deriv(cs):
    n = len(cs) - 1
    return [c * (n - i) for i, c in enumerate(cs[:-1])] or [0]


def fx(cs):
    return poly(cs)


# ============================================================ 10. prizma ve silindir
def u10():
    def kare_prizma():
        a, b, c = ri(2, 15), ri(2, 15), ri(2, 15)
        k = ri(0, 1)
        if k == 0:
            v = a * b * c
            return M("Boyutları %d cm, %d cm ve %d cm olan dikdörtgenler prizmasının hacmi kaç cm³’tür?" % (a, b, c), num(v), W3([num(2 * (a * b + b * c + a * c)), num(a * b + c), num(v // 2) if v % 2 == 0 else num(v + a), num(4 * (a + b + c))], num(v)),
                     "V = a · b · c = <b>%s</b>." % num(v))
        A = 2 * (a * b + b * c + a * c)
        return M("Boyutları %d cm, %d cm ve %d cm olan dikdörtgenler prizmasının yüzey alanı kaç cm²’dir?" % (a, b, c), num(A), W3([num(a * b * c), num(a * b + b * c + a * c), num(4 * (a + b + c)), num(A + a * b)], num(A)),
                 "Alan = 2(ab + bc + ac) = <b>%s</b>." % num(A))

    def ucgen_prizma():
        a, b, c = ch([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
        h = ri(2, 20)
        k = ri(0, 1)
        if k == 0:
            v = a * b // 2 * h
            return M("Tabanı dik kenarları %d cm ve %d cm olan dik üçgen, yüksekliği %d cm olan üçgen dik prizmanın hacmi kaç cm³’tür?" % (a, b, h), num(v), W3([num(a * b * h), num(v + h), num((a + b + c) * h), num(a * b // 2 + h)], num(v)),
                     "V = taban alanı × h = %d · %d = <b>%s</b>." % (a * b // 2, h, num(v)))
        A = a * b + (a + b + c) * h
        return M("Tabanı dik kenarları %d cm ve %d cm olan dik üçgen, yüksekliği %d cm olan üçgen dik prizmanın yüzey alanı kaç cm²’dir?" % (a, b, h), num(A), W3([num(a * b // 2 * h), num((a + b + c) * h), num(A - a * b // 2), num(A + c * h)], num(A)),
                 "2 taban + yanal alan = %d + %d · %d = <b>%s</b>." % (a * b, a + b + c, h, num(A)))

    def silindir():
        r, h = ri(1, 12), ri(1, 20)
        k = ri(0, 2)
        if k == 0:
            return M("Taban yarıçapı %d cm ve yüksekliği %d cm olan dik dairesel silindirin hacmi kaç cm³’tür?" % (r, h), pis(r * r * h), W3([pis(2 * r * h), pis(r * h), pis(2 * r * r * h), pis(r * r + h)], pis(r * r * h)),
                     "V = πr²h = <b>%s</b>." % pis(r * r * h))
        if k == 1:
            return M("Taban yarıçapı %d cm ve yüksekliği %d cm olan silindirin yanal alanı kaç cm²’dir?" % (r, h), pis(2 * r * h), W3([pis(r * h), pis(r * r * h), pis(2 * r * h + 2 * r * r), pis(2 * r * (r + h) + r)], pis(2 * r * h)),
                     "Yanal alan 2πrh = <b>%s</b>." % pis(2 * r * h))
        return M("Taban yarıçapı %d cm ve yüksekliği %d cm olan silindirin bütün yüzey alanı kaç cm²’dir?" % (r, h), pis(2 * r * (r + h)), W3([pis(2 * r * h), pis(r * r * h), pis(r * (r + h)), pis(2 * r * r + r * h)], pis(2 * r * (r + h))),
                 "2πr² + 2πrh = <b>%s</b>." % pis(2 * r * (r + h)))

    def kup():
        a = ri(2, 15)
        k = ri(0, 2)
        if k == 0:
            return M("Bir ayrıtı %d cm olan küpün hacmi kaç cm³’tür?" % a, num(a ** 3), W3([num(6 * a * a), num(a * a), num(3 * a), num(a ** 3 + a)], num(a ** 3)), "a³ = <b>%s</b>." % num(a ** 3))
        if k == 1:
            return M("Bir ayrıtı %d cm olan küpün cisim köşegeni kaç cm’dir?" % a, "%s cm" % rts(a, 3), W3(["%s cm" % rts(a, 2), "%d cm" % (3 * a), "%s cm" % rts(2 * a, 3), "%d cm" % a], "%s cm" % rts(a, 3)),
                     "Cisim köşegeni a√3 = <b>%s cm</b>." % rts(a, 3))
        return M("Yüzey alanı %s cm² olan küpün hacmi kaç cm³’tür?" % num(6 * a * a), num(a ** 3), W3([num(a * a), num(6 * a * a // 6 * 6), num((a + 1) ** 3), num(a ** 3 // a * 3)], num(a ** 3)),
                 "6a² = %s → a = %d → a³ = <b>%s</b>." % (num(6 * a * a), a, num(a ** 3)))

    sets = [("Dikdörtgenler prizması", [(kare_prizma, 20)]), ("Küp", [(kup, 20)]), ("Üçgen prizma", [(ucgen_prizma, 20)]),
            ("Silindir", [(silindir, 20)]), ("Karışık", [(kare_prizma, 7), (silindir, 7), (kup, 6)])]
    return U(12, "prizma-ve-silindir", "GC", "MAT.12.3.1", 10, "Dik Prizma ve Dik Dairesel Silindir", "Prizma ve Silindir",
             "Dik prizma ve dik dairesel silindirin elemanlarını, açınımlarını, yüzey alanlarını ve hacimlerini inceler.",
             "dikdörtgenler prizmasının hacmi ve yüzey alanı, küp ve cisim köşegeni, üçgen prizma, silindirin hacmi, yanal ve bütün yüzey alanı",
             "V = taban alanı × yükseklik", "Silindir: V = πr²h, yanal alan 2πrh.", sets,
             ["Dik prizmaların ve silindirin hacmi taban alanı ile yüksekliğin çarpımıdır.",
              "Yüzey alanı iki taban alanı ile yanal alanın toplamıdır; prizmada yanal alan taban çevresi × yüksekliktir.",
              "Silindirin açınımında yanal yüzey, kenarları 2πr ve h olan bir dikdörtgendir."],
             [("3 × 4 × 5 prizma", ["60", "2(12 + 20 + 15) = 94"], "V = 60, A = 94"), ("r = 3, h = 5", ["π · 9 · 5"], "45π")],
             [["Hacimde yüzey alanı formülünü kullanmak", "Hacim üç boyutun çarpımı"], ["Silindirde çapı yarıçap almak", "r = çap ÷ 2"], ["Bütün yüzey alanında tabanları unutmak", "2πr² ekle"]],
             [("Küp bir prizma mıdır?", "Evet; bütün yüzleri kare olan dikdörtgenler prizmasıdır."), ("Cavalieri ilkesi nedir?", "Aynı yükseklikteki kesit alanları eşit olan cisimlerin hacimleri eşittir."),
              ("Silindir hangi prizmaya benzer?", "Tabanı çok kenarlı bir çokgene yaklaşan prizmanın limitidir.")])


# ============================================================ 11. piramit, koni, küre
def u11():
    def piramit():
        a, h = ri(2, 15) * 3, ri(2, 20)
        v = a * a * h // 3
        return M("Tabanı bir kenarı %d cm olan kare ve yüksekliği %d cm olan kare piramidin hacmi kaç cm³’tür?" % (a, h), num(v), W3([num(a * a * h), num(a * a * h // 2) if (a * a * h) % 2 == 0 else num(v * 2), num(v + a), num(4 * a * h)], num(v)),
                 "V = taban alanı × h ÷ 3 = %d · %d ÷ 3 = <b>%s</b>." % (a * a, h, num(v)))

    def piramit_alan():
        a, b, c = ch([(3, 4, 5), (5, 12, 13), (8, 15, 17), (4, 3, 5), (12, 5, 13), (15, 8, 17), (7, 24, 25), (24, 7, 25)])
        m = ri(1, 4)
        a, b, c = a * m, b * m, c * m
        # yükseklik b, taban yarı kenarı a → yan yüz yüksekliği c; taban kenarı 2a
        s = 2 * a
        A = s * s + 4 * (s * c // 2)
        return M("Yüksekliği %d cm, tabanı bir kenarı %d cm olan kare olan düzgün piramidin bütün yüzey alanı kaç cm²’dir?" % (b, s), num(A), W3([num(4 * s * c // 2), num(s * s + 4 * s * b // 2), num(s * s * b // 3), num(A + s * s)], num(A)),
                 "Yan yüz yüksekliği √(%d² + %d²) = %d; alan %d + 4 · %d · %d ÷ 2 = <b>%s</b>." % (b, a, c, s * s, s, c, num(A)))

    def koni():
        a, b, c = ch([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25)])
        r, h, l = (a, b, c) if ri(0, 1) else (b, a, c)
        k = ri(0, 2)
        if k == 0:
            v = F(r * r * h, 3)
            return M("Taban yarıçapı %d cm ve yüksekliği %d cm olan dik dairesel koninin hacmi kaç cm³’tür?" % (r, h), pis(v), W3([pis(r * r * h), pis(F(r * h, 3)), pis(F(r * r * l, 3)), pis(v * 2)], pis(v)),
                     "V = πr²h ÷ 3 = <b>%s</b>." % pis(v))
        if k == 1:
            return M("Taban yarıçapı %d cm ve yüksekliği %d cm olan dik koninin ana doğrusu kaç cm’dir?" % (r, h), "%d cm" % l, W3(["%d cm" % (r + h), "%d cm" % (l + 1), "%d cm" % abs(h - r) if h != r else "1 cm", "%d cm" % (2 * l)], "%d cm" % l),
                     "Ana doğru √(r² + h²) = <b>%d cm</b>." % l)
        return M("Taban yarıçapı %d cm ve ana doğrusu %d cm olan koninin yanal alanı kaç cm²’dir?" % (r, l), pis(r * l), W3([pis(r * h), pis(r * r + r * l), pis(2 * r * l), pis(F(r * l, 2)) if (r * l) % 2 == 0 else pis(r * l + r)], pis(r * l)),
                 "Yanal alan πrl = <b>%s</b>." % pis(r * l))

    def kure():
        r = ri(1, 15)
        k = ri(0, 1)
        if k == 0:
            v = F(4 * r ** 3, 3)
            return M("Yarıçapı %d cm olan kürenin hacmi kaç cm³’tür?" % r, pis(v), W3([pis(4 * r * r), pis(r ** 3), pis(F(4 * r * r, 3)), pis(v * 2)], pis(v)), "V = 4πr³ ÷ 3 = <b>%s</b>." % pis(v))
        return M("Yarıçapı %d cm olan kürenin yüzey alanı kaç cm²’dir?" % r, pis(4 * r * r), W3([pis(2 * r * r), pis(r * r), pis(F(4 * r ** 3, 3)), pis(8 * r)], pis(4 * r * r)), "A = 4πr² = <b>%s</b>." % pis(4 * r * r))

    def karsilastir():
        r = ri(1, 12)
        k = ri(0, 1)
        if k == 0:
            return M("Taban yarıçapı ve yüksekliği eşit olan bir silindir ile bir koninin hacimleri oranı (silindir : koni) kaçtır?", "3 : 1", ["1 : 3", "2 : 1", "1 : 1"], "Koni, aynı taban ve yükseklikteki silindirin üçte biridir: <b>3 : 1</b>.") if r == 1 else None
        return M("Yarıçapı %d cm olan küre, taban yarıçapı %d cm ve yüksekliği %d cm olan silindirin içine tam sığıyor. Silindirin hacminin kürenin hacmine oranı kaçtır?" % (r, r, 2 * r), frs(3, 2), [frs(2, 3), "2", frs(4, 3)],
                 "Silindir 2πr³, küre 4πr³ ÷ 3; oran <b>3/2</b> (Arşimet)." )

    sets = [("Piramidin hacmi", [(piramit, 20)]), ("Piramidin yüzey alanı", [(piramit_alan, 20)]), ("Koni", [(koni, 20)]),
            ("Küre", [(kure, 20)]), ("Karışık", [(koni, 7), (kure, 7), (karsilastir, 6)])]
    return U(12, "piramit-koni-ve-kure", "GC", "MAT.12.3.2", 11, "Dik Piramit, Dik Dairesel Koni ve Küre", "Piramit, Koni ve Küre",
             "Dik piramit, dik dairesel koni ve kürenin elemanlarını, yüzey alanlarını ve hacimlerini inceler.",
             "kare piramidin hacmi ve yüzey alanı, koninin hacmi, ana doğrusu ve yanal alanı, kürenin hacmi ve yüzey alanı, cisimlerin karşılaştırılması",
             "Piramit ve koni: V = taban × h ÷ 3", "Küre: V = 4πr³ ÷ 3, A = 4πr².", sets,
             ["Piramit ve koninin hacmi, aynı taban ve yükseklikteki prizma ya da silindirin üçte biridir.",
              "Koninin ana doğrusu l = √(r² + h²), yanal alanı πrl’dir.",
              "Kürenin hacmi 4πr³ ÷ 3, yüzey alanı 4πr²’dir."],
             [("Kare piramit, a = 6, h = 5", ["36 · 5 ÷ 3"], "60"), ("Koni, r = 3, h = 4", ["l = 5", "9π · 4 ÷ 3"], "12π")],
             [["Hacimde 3’e bölmeyi unutmak", "Piramit ve koni ÷ 3"], ["Yükseklik ile ana doğruyu karıştırmak", "l eğik kenardır"], ["Kürede r² ile r³’ü karıştırmak", "Hacim r³, alan r²"]],
             [("Neden üçte bir?", "Bir küp, tepeleri küpün merkezinde olan 6 eş piramide ayrılabilir."), ("Arşimet neyi buldu?", "Küre ile onu saran silindirin hacim oranının 2 : 3 olduğunu."),
              ("Dünya yaklaşık bir küre midir?", "Evet; yüzey alanı ve hacmi küre formülleriyle tahmin edilir.")])


# ============================================================ 12. cisim problemleri
def u12():
    def su():
        a, b = ri(2, 10) * 5, ri(2, 10) * 5
        h = ri(2, 20)
        x = ri(1, 8)
        v = a * b * x
        return M("Taban boyutları %d cm ve %d cm olan dikdörtgenler prizması biçimindeki akvaryuma bir taş atılınca su seviyesi %d cm yükseliyor. Taşın hacmi kaç cm³’tür?" % (a, b, x), num(v), W3([num(a * b), num((a + b) * x), num(v * 2), num(v // x * (x + 1))], num(v)),
                 "Taşın hacmi yükselen suyun hacmidir: %d · %d · %d = <b>%s</b>." % (a, b, x, num(v)))

    def eritme():
        a = ri(1, 4)
        n = ch([8, 27, 64, 125])
        A = a * round(n ** (1 / 3))
        return M("Ayrıtı %d cm olan bir küp eritilerek ayrıtı %d cm olan küçük küpler yapılıyor. Kaç küçük küp elde edilir?" % (A, a), num(n), W3([num(round(n ** (1 / 3))), num(round(n ** (1 / 3)) ** 2), num(n * 2), num(6 * round(n ** (1 / 3)))], num(n)),
                 "Hacimler oranı (%d ÷ %d)³ = <b>%d</b>." % (A, a, n))

    def benzer():
        k = ri(2, 5)
        t = ch(["hacmi", "yüzey alanı"])
        v = k ** 3 if t == "hacmi" else k * k
        return M("Bütün boyutları %d katına çıkarılan bir cismin %s kaç katına çıkar?" % (k, t), num(v), W3([num(k), num(k * k) if t == "hacmi" else num(k ** 3), num(2 * k), num(v + k)], num(v)),
                 "Uzunluklar k katına çıkınca alanlar k², hacimler k³ katına çıkar: <b>%d</b>." % v)

    def doldur():
        r, h = ri(1, 6), ri(2, 12)
        H = h * ri(2, 6)
        n = H // h * 3
        return M("Taban yarıçapı %d cm ve yüksekliği %d cm olan koni biçimindeki bir kapla, aynı taban yarıçaplı ve yüksekliği %d cm olan silindir biçimindeki bir kap kaç kez doldurularak tamamen dolar?" % (r, h, H), num(n),
                 W3([num(H // h), num(n // 3 * 2), num(n + 3), num(3)], num(n)), "Silindir πr² · %d, koni πr² · %d ÷ 3; oran %d · 3 ÷ %d = <b>%d</b>." % (H, h, H, h, n))

    def boya():
        a = ri(2, 12)
        k = ri(0, 1)
        if k == 0:
            n = a ** 3
            return M("Ayrıtı %d cm olan küp, ayrıtı 1 cm olan birim küplere bölünüyor. Kaç birim küp elde edilir?" % a, num(n), W3([num(a * a), num(6 * a * a), num(3 * a), num(n - a)], num(n)), "%d³ = <b>%s</b>." % (a, num(n)))
        if a < 3:
            return None
        v = (a - 2) ** 3
        return M("Bütün yüzleri boyanmış, ayrıtı %d cm olan küp birim küplere bölünüyor. Hiçbir yüzü boyalı olmayan kaç birim küp vardır?" % a, num(v), W3([num((a - 1) ** 3), num(a ** 3 - 6 * a * a), num((a - 2) ** 2), num(6 * (a - 2) ** 2)], num(v)) if a ** 3 - 6 * a * a != v else None,
                 "İçteki küp (%d − 2)³ = <b>%s</b>." % (a, num(v)))

    sets = [("Su seviyesi", [(su, 20)]), ("Eritme ve birim küpler", [(eritme, 4), (boya, 8), (doldur, 8)]), ("Benzer cisimler", [(benzer, 8), (su, 12)]),
            ("Kap doldurma", [(doldur, 20)]), ("Karışık", [(su, 5), (doldur, 10), (boya, 5)])]
    return U(12, "cisim-problemleri", "GC", "MAT.12.3.3", 12, "Geometrik Cisimlerle İlgili Problemler", "Cisim Problemleri",
             "Geometrik cisimlerin yüzey alanları ve hacimleriyle ilgili gerçek yaşam problemlerini çözer.",
             "taş atılınca yükselen su, eritip yeniden şekillendirme, birim küpler ve boyalı yüzler, benzer cisimlerde alan ve hacim, kap doldurma",
             "Eritmede hacim korunur", "Uzunluk k katı → alan k², hacim k³ katı.", sets,
             ["Bir cisim suya batırılınca yükselen suyun hacmi cismin hacmine eşittir.",
              "Eritip yeniden şekillendirmede toplam hacim değişmez.",
              "Bütün uzunlukları k katına çıkan cismin yüzey alanı k², hacmi k³ katına çıkar."],
             [("Taban 20 × 30, su 2 cm yükseldi", ["20 · 30 · 2"], "1.200 cm³"), ("Ayrıt 2 katı", ["2³"], "Hacim 8 katı")],
             [["Hacim oranını uzunluk oranı sanmak", "Hacim k³"], ["Su seviyesinde toplam yüksekliği kullanmak", "Yalnızca artış"], ["Boyalı küplerde köşeleri iki kez saymak", "İçteki küpü hesapla"]],
             [("Arşimet ilkesi nedir?", "Suya batan cisim kendi hacmi kadar suyu yerinden eder."), ("Neden hacim k³ katı?", "Üç boyutun her biri k katına çıkar."),
              ("Bu problemler nerede çıkar?", "Ambalaj, inşaat ve mühendislik tasarımlarında.")])


# ============================================================ 13. limit
def u13():
    def polinom():
        cs = [nz(-3, 3), ri(-6, 6), ri(-9, 9)]
        a = ri(-4, 4)
        v = peval(cs, a)
        return M("lim<sub>x→%s</sub> (%s) kaçtır?" % (sn(a), poly(cs)), sn(v), W3([sn(peval(cs, -a)), sn(v + 1), sn(cs[-1]), "Limit yoktur"], sn(v)),
                 "Polinomlarda limit, değer yerine yazılarak bulunur: <b>%s</b>." % sn(v))

    def parcali():
        a = ri(-4, 4)
        m1, n1 = nz(-4, 4), ri(-6, 6)
        m2, n2 = nz(-4, 4), ri(-6, 6)
        L = m1 * a + n1
        R_ = m2 * a + n2
        k = ch(["sol", "sağ", "iki"])
        f = "f(x) = %s (x &lt; %s), f(x) = %s (x ≥ %s)" % (lin(m1, "x", n1), sn(a), lin(m2, "x", n2), sn(a))
        if k == "sol":
            return M("%s ise x %s’e soldan yaklaşırken f(x)’in limiti kaçtır?" % (f, sn(a)) if False else "%s olmak üzere lim<sub>x→%s⁻</sub> f(x) kaçtır?" % (f, sn(a)), sn(L), W3([sn(R_), sn(L + 1), sn(L + R_), "Limit yoktur"], sn(L)),
                     "Soldan yaklaşırken x &lt; %s kuralı kullanılır: <b>%s</b>." % (sn(a), sn(L)))
        if k == "sağ":
            return M("%s olmak üzere lim<sub>x→%s⁺</sub> f(x) kaçtır?" % (f, sn(a)), sn(R_), W3([sn(L), sn(R_ + 1), sn(L + R_), "Limit yoktur"], sn(R_)),
                     "Sağdan yaklaşırken x ≥ %s kuralı kullanılır: <b>%s</b>." % (sn(a), sn(R_)))
        g = sn(L) if L == R_ else "Limit yoktur"
        return M("%s olmak üzere lim<sub>x→%s</sub> f(x) kaçtır?" % (f, sn(a)), g, W3([sn(L), sn(R_), sn(L + R_), "Limit yoktur", sn(L + 1)], g),
                 "Sol limit %s, sağ limit %s: %s" % (sn(L), sn(R_), "eşit olduğundan limit <b>%s</b>." % sn(L) if L == R_ else "farklı olduğundan <b>limit yoktur</b>."))

    def tablo():
        a = ri(-3, 5)
        L = ri(-9, 9)
        xs = [a - F(1, 10), a - F(1, 100), a + F(1, 100), a + F(1, 10)]
        m = nz(-3, 3)
        ys = [L + m * (x - a) for x in xs]
        t = "<table class='sn-table' style='width:auto'><tbody><tr><td>x</td>%s</tr><tr><td>f(x)</td>%s</tr></tbody></table>" % ("".join("<td>%s</td>" % dq(x) for x in xs), "".join("<td>%s</td>" % dq(y) for y in ys))
        return M("Tabloya göre lim<sub>x→%s</sub> f(x) değeri kaçtır?%s" % (sn(a), t), sn(L), W3([sn(L + m), sn(L - m), sn(a), sn(L + 1)], sn(L)),
                 "x, %s’e iki yandan yaklaştıkça f(x) %s’e yaklaşıyor: <b>%s</b>." % (sn(a), sn(L), sn(L)) if False else "x iki yandan yaklaştıkça f(x) değerleri aynı sayıya yaklaşıyor: <b>%s</b>." % sn(L))

    def sonsuz():
        a, b = nz(-6, 6), ri(-9, 9)
        c, d = nz(-6, 6), ri(-9, 9)
        k = ri(0, 1)
        if k == 0:
            v = F(a, c)
            return M("lim<sub>x→∞</sub> (%s) ÷ (%s) kaçtır?" % (lin(a, "x", b), lin(c, "x", d)), sn(v), W3([sn(F(c, a)), sn(F(b, d)) if d else "0", "∞", sn(v + 1)], sn(v)),
                     "Dereceler eşit; başkatsayıların oranı: <b>%s</b>." % sn(v))
        return M("lim<sub>x→∞</sub> (%s) ÷ (%s) kaçtır?" % (lin(a, "x", b), poly([c, 0, d])), "0", W3([sn(F(a, c)), "∞", sn(F(b, d)) if d else "1", "1"], "0"),
                 "Paydanın derecesi daha büyük olduğundan limit <b>0</b>.")

    sets = [("Polinomlarda limit", [(polinom, 20)]), ("Tablodan limit", [(tablo, 20)]), ("Soldan ve sağdan limit", [(parcali, 20)]),
            ("Limitin varlığı", [(parcali, 20)]), ("Sonsuzda limit", [(sonsuz, 20)])]
    return U(12, "limit", "DM", "MAT.12.4.1, MAT.12.4.2", 13, "Limit: Soldan, Sağdan ve Sonsuzda Limit", "Limit",
             "Bir fonksiyonun bir noktadaki limitini tablo, grafik ve cebirsel yollarla inceler; soldan ve sağdan limit ile limitin varlığını yorumlar.",
             "polinomlarda limit, tablodan limit, parçalı fonksiyonlarda soldan ve sağdan limit, limitin varlığı, sonsuzda limit",
             "Limit = sol limit = sağ limit", "Polinomda limit, değer yerine yazılarak bulunur.", sets,
             ["x bir a değerine yaklaşırken f(x) bir L sayısına yaklaşıyorsa limit L’dir; x’in a’ya eşit olması gerekmez.",
              "Bir noktada limit olması için soldan ve sağdan limitlerin var ve eşit olması gerekir.",
              "x → ∞ iken rasyonel fonksiyonlarda dereceler eşitse limit başkatsayıların oranıdır; paydanın derecesi büyükse limit 0’dır."],
             [("lim x→2 (x² + 1)", ["4 + 1"], "5"), ("Sol limit 3, sağ limit 5", ["Farklı"], "Limit yok")],
             [["Limiti fonksiyonun değeriyle karıştırmak", "Limit yaklaşılan değerdir"], ["Parçalı fonksiyonda yanlış kuralı kullanmak", "Sol için sol kural"], ["Sonsuzda sabit terimlere bakmak", "Başkatsayılar önemli"]],
             [("Limit neden gerekli?", "Türev ve integral limit kavramına dayanır."), ("Fonksiyon tanımsızken limit olur mu?", "Evet; limit yalnızca yaklaşılan değere bakar."),
              ("Sonsuzda limit ne anlatır?", "Grafiğin uzun vadede hangi değere yaklaştığını.")])


# ============================================================ 14. belirsizlik ve süreklilik
def u14():
    def sifir_sifir():
        a = nz(-6, 6)
        b = ri(-6, 6)
        k = ri(0, 1)
        if k == 0:
            # (x² − a²) ÷ (x − a)
            v = 2 * a
            return M("lim<sub>x→%s</sub> (x² − %d) ÷ (%s) kaçtır?" % (sn(a), a * a, lin(1, "x", -a)), sn(v), W3([sn(a), "0", "Tanımsız", sn(a * a)], sn(v)),
                     "0/0 belirsizliği; x² − %d = (x − %s)(x + %s) sadeleşir: %s + %s = <b>%s</b>." % (a * a, par(a), par(a), sn(a), par(a), sn(v)))
        # (x − a)(x − b) ÷ (x − a)
        cs = pmul([1, -a], [1, -b])
        v = a - b
        return M("lim<sub>x→%s</sub> (%s) ÷ (%s) kaçtır?" % (sn(a), poly(cs), lin(1, "x", -a)), sn(v), W3([sn(a + b), "0", sn(-v) if v else "1", sn(b)], sn(v)),
                 "Pay %s%s biçiminde çarpanlarına ayrılır, sadeleşir: %s − %s = <b>%s</b>." % (fct(a), fct(b), sn(a), par(b), sn(v)))

    def surekli_k():
        a = ri(-4, 4)
        m1, n1 = nz(-4, 4), ri(-6, 6)
        m2 = nz(-4, 4)
        L = m1 * a + n1
        k = L - m2 * a
        f = "f(x) = %s (x &lt; %s), f(x) = %s (x ≥ %s)" % (lin(m1, "x", n1), sn(a), lin(m2, "x", 0) + " + k", sn(a))
        return M("%s fonksiyonu x = %s’de sürekli ise k kaçtır?" % (f, sn(a)) if False else "%s fonksiyonu her yerde sürekli ise k kaçtır?" % f, sn(k), W3([sn(-k) if k else "1", sn(L), sn(k + m2), sn(L + m2 * a)], sn(k)),
                 "Sol limit %s, sağ limit %s + k olmalı: k = <b>%s</b>." % (sn(L), sn(m2 * a), sn(k)))

    def nokta():
        a = ri(-5, 5)
        k = ri(0, 2)
        if k == 0:
            g = "x = %s" % sn(a)
            return M("f(x) = 1 ÷ (%s) fonksiyonu hangi noktada sürekli değildir?" % lin(1, "x", -a), g, W3(["x = %s" % sn(-a) if a else "x = 1", "x = 0" if a else "x = 2", "Her yerde süreklidir", "x = %s" % sn(a + 1)], g),
                     "Payda sıfır olduğunda fonksiyon tanımsızdır: <b>%s</b>." % g)
        if k == 1:
            return M("f(x) = %s fonksiyonu hangi noktalarda süreklidir?" % poly([nz(-3, 3), ri(-5, 5), ri(-5, 5)]), "Bütün gerçek sayılarda", ["Yalnızca x &gt; 0 için", "x = 0 dışında", "Hiçbir noktada"],
                     "Polinomlar her yerde süreklidir: <b>bütün gerçek sayılarda</b>.")
        b = nz(1, 6)
        g = "x = %s ve x = %d" % (sn(-b), b)
        return M("f(x) = (x + 1) ÷ (x² − %d) fonksiyonu hangi noktalarda sürekli değildir?" % (b * b), g, W3(["x = %d" % b, "x = %d" % (b * b), "x = −1", "Her yerde süreklidir"], g), "x² − %d = 0 → <b>%s</b>." % (b * b, g))

    def sart():
        a = ri(-5, 5)
        L, v = ri(-9, 9), ri(-9, 9)
        g = "Sürekli" if L == v else "Sürekli değil"
        return M("lim<sub>x→%s</sub> f(x) = %s ve f(%s) = %s ise f, x = %s noktasında sürekli midir?" % (sn(a), sn(L), sn(a), sn(v), sn(a)), g, ["Sürekli değil" if g == "Sürekli" else "Sürekli", "Karar verilemez", "Limit yoktur"],
                 "Süreklilik için limit fonksiyonun değerine eşit olmalı: %s %s %s → <b>%s</b>." % (sn(L), "=" if L == v else "≠", sn(v), g.lower()))

    sets = [("0/0 belirsizliği", [(sifir_sifir, 20)]), ("Süreklilik şartı", [(sart, 20)]), ("Süreksiz noktalar", [(nokta, 10), (sifir_sifir, 10)]),
            ("Parçalı fonksiyonda süreklilik", [(surekli_k, 20)]), ("Karışık", [(sifir_sifir, 7), (surekli_k, 7), (sart, 6)])]
    return U(12, "belirsizlik-ve-sureklilik", "DM", "MAT.12.4.3, MAT.12.4.4", 14, "0/0 Belirsizliği ve Süreklilik", "Belirsizlik ve Süreklilik",
             "0/0 belirsizliği içeren limitleri çarpanlara ayırarak hesaplar; bir fonksiyonun bir noktada sürekliliğini inceler.",
             "0/0 belirsizliği, süreklilik şartı, süreksiz noktalar, parçalı fonksiyonu sürekli yapan değer",
             "0/0 ise çarpanlara ayır ve sadeleştir", "Sürekli: limit = fonksiyonun değeri.", sets,
             ["Yerine yazınca 0/0 çıkıyorsa pay ve payda çarpanlarına ayrılır, ortak çarpan sadeleştirilir.",
              "f, x = a’da süreklidir ⇔ f(a) tanımlı, limit var ve lim f(x) = f(a).",
              "Polinomlar her yerde süreklidir; rasyonel fonksiyonlar paydayı sıfır yapan noktalarda sürekli değildir."],
             [("lim x→3 (x² − 9) ÷ (x − 3)", ["(x + 3)"], "6"), ("Sol 4, sağ 2 + k", ["k = 2"], "Sürekli")],
             [["0/0’ı 0 ya da tanımsız sanmak", "Belirsizliktir, sadeleştir"], ["Limit varsa sürekli sanmak", "f(a) ile de eşit olmalı"], ["Parçalı fonksiyonda tek tarafa bakmak", "İki taraf da"]],
             [("Süreklilik görsel olarak ne demek?", "Grafiği kalemi kaldırmadan çizebilmektir."), ("Neden 0/0 belirsiz?", "Sonuç farklı fonksiyonlarda farklı değerler olabilir."),
              ("Ara değer teoremi nedir?", "Sürekli bir fonksiyon iki değer arasındaki bütün değerleri alır.")])


# ============================================================ 15. türevin tanımı
def u15():
    def ortalama():
        cs = [nz(-3, 3), ri(-6, 6), ri(-9, 9)]
        a = ri(-4, 3)
        b = a + ri(1, 4)
        v = F(peval(cs, b) - peval(cs, a), b - a)
        return M("f(x) = %s fonksiyonunun [%s, %s] aralığındaki ortalama değişim hızı kaçtır?" % (poly(cs), sn(a), sn(b)), sn(v), W3([sn(peval(cs, b) - peval(cs, a)), sn(v + 1), sn(F(peval(cs, b) + peval(cs, a), b - a)), sn(-v) if v else "1"], sn(v)),
                 "(f(%s) − f(%s)) ÷ (%s − %s) = (%s − %s) ÷ %d = <b>%s</b>." % (sn(b), sn(a), sn(b), par(a), sn(peval(cs, b)), par(peval(cs, a)), b - a, sn(v)))

    def tanim():
        a = nz(-3, 3)
        b = ri(-6, 6)
        x0 = ri(-4, 4)
        v = 2 * a * x0 + b
        return M("f(x) = %s için lim<sub>h→0</sub> (f(%s + h) − f(%s)) ÷ h kaçtır?" % (poly([a, b, ri(-9, 9)]), sn(x0), sn(x0)), sn(v), W3([sn(a * x0 * x0 + b * x0), sn(2 * a + b), sn(v + b), "0"], sn(v)),
                 "Bu limit f′(%s) değeridir: f′(x) = %s → <b>%s</b>." % (sn(x0), lin(2 * a, "x", b), sn(v)))

    def turevsiz():
        a = ri(-6, 6)
        k = ri(0, 1)
        if k == 0:
            g = "x = %s" % sn(a)
            return M("f(x) = |%s| fonksiyonu hangi noktada türevlenemez?" % lin(1, "x", -a), g, W3(["x = %s" % sn(-a) if a else "x = 1", "x = 0" if a else "x = 2", "Her yerde türevlenebilir", "x = %s" % sn(a + 1)], g),
                     "Grafikte köşe (sivri nokta) vardır; soldan türev −1, sağdan türev 1: <b>%s</b>." % g)
        m1, m2 = nz(-4, 4), nz(-4, 4)
        n1 = ri(-5, 5)
        n2 = m1 * a + n1 - m2 * a
        same = m1 == m2
        f = "f(x) = %s (x &lt; %s), f(x) = %s (x ≥ %s)" % (lin(m1, "x", n1), sn(a), lin(m2, "x", n2), sn(a))
        g = "Türevlenebilir" if same else "Türevlenemez (sürekli ama köşe var)"
        return M("%s fonksiyonu x = %s noktasında türevlenebilir mi?" % (f, sn(a)), g, W3(["Türevlenebilir", "Türevlenemez (sürekli ama köşe var)", "Türevlenemez (sürekli değil)", "Karar verilemez"], g),
                 "Fonksiyon x = %s’de sürekli; soldan türev %s, sağdan türev %s → <b>%s</b>." % (sn(a), sn(m1), sn(m2), g.lower()) if False else "Fonksiyon bu noktada sürekli; soldan türev %s, sağdan türev %s → <b>%s</b>." % (sn(m1), sn(m2), g.lower()))

    def hiz():
        a, b = ri(1, 5), ri(0, 20)
        t = ri(1, 10)
        v = 2 * a * t + b
        return M("Bir cismin t saniyede aldığı yol s(t) = %s metredir. t = %d saniyedeki anlık hızı kaç m/s’dir?" % (poly([a, b, 0], "t"), t), num(v), W3([num(a * t * t + b * t), num(2 * a + b), num(a * t + b), num(v + a)], num(v)),
                 "Anlık hız s′(t) = %s; s′(%d) = <b>%d m/s</b>." % (lin(2 * a, "t", b), t, v))

    sets = [("Ortalama değişim hızı", [(ortalama, 20)]), ("Türevin tanımı", [(tanim, 20)]), ("Anlık hız", [(hiz, 20)]),
            ("Türevlenemeyen noktalar", [(turevsiz, 20)]), ("Karışık", [(ortalama, 10), (tanim, 10)])]
    return U(12, "turevin-tanimi", "DM", "MAT.12.4.5, MAT.12.4.6", 15, "Türevin Tanımı ve Anlık Değişim Hızı", "Türevin Tanımı",
             "Ortalama ve anlık değişim hızı yardımıyla türevi tanımlar; bir fonksiyonun türevlenemediği noktaları belirler.",
             "ortalama değişim hızı, türevin limit tanımı, anlık hız, mutlak değer ve parçalı fonksiyonlarda türevlenemeyen noktalar",
             "f′(a) = lim (f(a + h) − f(a)) ÷ h", "Köşe ve süreksizlik noktalarında türev yoktur.", sets,
             ["[a, b] aralığında ortalama değişim hızı (f(b) − f(a)) ÷ (b − a)’dır; kesen doğrunun eğimidir.",
              "h → 0 iken ortalama değişim hızının limiti anlık değişim hızıdır: f′(a) = lim (f(a + h) − f(a)) ÷ h.",
              "Fonksiyonun sürekli olmadığı ya da grafiğinde köşe olduğu noktalarda türev yoktur."],
             [("f(x) = x², [1, 3]", ["(9 − 1) ÷ 2"], "4"), ("s(t) = t², t = 3", ["s′(t) = 2t"], "6 m/s")],
             [["Ortalama hızı anlık hızla karıştırmak", "Anlık hız limittir"], ["Sürekli olan her fonksiyonu türevlenebilir sanmak", "|x| sürekli ama 0’da türevsiz"], ["Bölmeyi unutmak", "Fark ÷ aralık"]],
             [("Türev neyi ölçer?", "Bir niceliğin anlık değişim hızını."), ("Hız ile türev ilişkisi?", "Konumun türevi hız, hızın türevi ivmedir."),
              ("Türev kim tarafından geliştirildi?", "Newton ve Leibniz tarafından 17. yüzyılda.")])


# ============================================================ 16. türev kuralları
def u16():
    def kuvvet():
        n = ri(2, 7)
        a = nz(-6, 6)
        cs = [a] + [0] * n
        d = deriv(cs)
        g = "f′(x) = " + poly(d)
        return M("f(x) = %s ise f′(x) hangisidir?" % poly(cs), g, W3(["f′(x) = " + poly([a * n] + [0] * n), "f′(x) = " + poly([a] + [0] * (n - 1)), "f′(x) = " + poly([a * (n - 1)] + [0] * (n - 1)), "f′(x) = " + poly([a * n] + [0] * (n - 2))], g),
                 "(xⁿ)′ = nxⁿ⁻¹: <b>%s</b>." % poly(d))

    def polinom():
        cs = [nz(-4, 4), ri(-6, 6), ri(-9, 9), ri(-9, 9)]
        d = deriv(cs)
        g = "f′(x) = " + poly(d)
        w = ["f′(x) = " + poly([d[0], d[1], d[2] + cs[3]]) if cs[3] else "f′(x) = " + poly([d[0], d[1], d[2] + 1]), "f′(x) = " + poly([cs[0] * 3, cs[1] * 2, cs[2], 0]), "f′(x) = " + poly([cs[0], cs[1], cs[2]]), "f′(x) = " + poly([d[0], -d[1], d[2]]) if d[1] else "f′(x) = " + poly([d[0], 1, d[2]])]
        return M("f(x) = %s ise f′(x) hangisidir?" % poly(cs), g, W3(w, g), "Terim terim türev alınır; sabitin türevi 0: <b>%s</b>." % poly(d))

    def deger():
        cs = [nz(-3, 3), ri(-5, 5), ri(-9, 9), ri(-9, 9)]
        x = ri(-3, 3)
        v = peval(deriv(cs), x)
        return M("f(x) = %s ise f′(%s) kaçtır?" % (poly(cs), sn(x)), sn(v), W3([sn(peval(cs, x)), sn(v + 1), sn(peval(deriv(cs), -x)), sn(deriv(cs)[-1])], sn(v)),
                 "f′(x) = %s → f′(%s) = <b>%s</b>." % (poly(deriv(cs)), sn(x), sn(v)))

    def carpim():
        a, b, c, d = nz(-4, 4), ri(-6, 6), nz(-4, 4), ri(-6, 6)
        x = ri(-3, 3)
        v = a * (c * x + d) + c * (a * x + b)
        return M("f(x) = (%s)(%s) ise f′(%s) kaçtır?" % (lin(a, "x", b), lin(c, "x", d), sn(x)), sn(v), W3([sn(a * c), sn((a * x + b) * (c * x + d)), sn(a * (c * x + d)), sn(v + 1)], sn(v)),
                 "Çarpım kuralı: (uv)′ = u′v + uv′ = %s · %s + %s · %s = <b>%s</b>." % (sn(a), par(c * x + d), par(a * x + b), sn(c), sn(v)))

    def zincir():
        a, b = nz(-4, 4), ri(-6, 6)
        n = ri(2, 5)
        x = ri(-2, 2)
        u = a * x + b
        v = n * u ** (n - 1) * a
        return M("f(x) = (%s)<sup>%d</sup> ise f′(%s) kaçtır?" % (lin(a, "x", b), n, sn(x)), sn(v), W3([sn(n * u ** (n - 1)), sn(u ** n), sn(n * u ** (n - 1) * a + 1), sn(n * a)], sn(v)),
                 "Zincir kuralı: %d(%s)<sup>%d</sup> · %s → x = %s için %d · %s<sup>%d</sup> · %s = <b>%s</b>." % (n, lin(a, "x", b), n - 1, sn(a), sn(x), n, par(u), n - 1, par(a), sn(v)))

    def bolum():
        a, b, c, d = nz(-4, 4), ri(-6, 6), nz(-3, 3), ri(-6, 6)
        x = ri(-3, 3)
        if c * x + d == 0 or a * d == b * c:
            return None
        v = F(a * d - b * c, (c * x + d) ** 2)
        return M("f(x) = (%s) ÷ (%s) ise f′(%s) kaçtır?" % (lin(a, "x", b), lin(c, "x", d), sn(x)), sn(v), W3([sn(F(a, c)), sn(F(b * c - a * d, (c * x + d) ** 2)), sn(F(a * d - b * c, c * x + d)), sn(v + 1)], sn(v)),
                 "Bölüm kuralı: (ad − bc) ÷ (cx + d)² = %s ÷ %s = <b>%s</b>." % (sn(a * d - b * c), sn((c * x + d) ** 2), sn(v)))

    sets = [("Kuvvet kuralı", [(kuvvet, 20)]), ("Polinomların türevi", [(polinom, 20)]), ("Türevin değeri", [(deger, 20)]),
            ("Çarpım ve bölüm kuralı", [(carpim, 10), (bolum, 10)]), ("Zincir kuralı", [(zincir, 20)])]
    return U(12, "turev-kurallari", "DM", "MAT.12.4.7", 16, "Türev Alma Kuralları", "Türev Kuralları",
             "Türev alma kurallarını (kuvvet, toplam, sabitle çarpım, çarpım, bölüm, zincir kuralı) kullanarak fonksiyonların türevini bulur.",
             "kuvvet kuralı, polinomların türevi, türevin bir noktadaki değeri, çarpım ve bölüm kuralı, zincir kuralı",
             "(xⁿ)′ = n · xⁿ⁻¹", "(uv)′ = u′v + uv′; sabitin türevi 0.", sets,
             ["(xⁿ)′ = nxⁿ⁻¹; sabitin türevi 0’dır; toplamın türevi türevlerin toplamıdır.",
              "Çarpım kuralı (uv)′ = u′v + uv′, bölüm kuralı (u ÷ v)′ = (u′v − uv′) ÷ v².",
              "Zincir kuralı: (f(g(x)))′ = f′(g(x)) · g′(x); örneğin ((ax + b)ⁿ)′ = n(ax + b)ⁿ⁻¹ · a."],
             [("f(x) = 3x⁴", ["4 · 3x³"], "12x³"), ("(2x + 1)³", ["3(2x + 1)² · 2"], "6(2x + 1)²")],
             [["Üssü azaltmayı unutmak", "n − 1"], ["Çarpımın türevini türevlerin çarpımı sanmak", "u′v + uv′"], ["Zincirde iç türevi unutmak", "· g′(x)"]],
             [("Türevin türevi nedir?", "İkinci türevdir; ivmeyi ve eğriliği gösterir."), ("eˣ’in türevi?", "Kendisidir."),
              ("Kurallar nereden gelir?", "Hepsi türevin limit tanımından ispatlanır.")])


# ============================================================ 17. türevin geometrik yorumu
def u17():
    def egim():
        cs = [nz(-3, 3), ri(-6, 6), ri(-9, 9)]
        x = ri(-4, 4)
        m = peval(deriv(cs), x)
        return M("f(x) = %s eğrisine x = %s apsisli noktasında çizilen teğetin eğimi kaçtır?" % (poly(cs), sn(x)), sn(m), W3([sn(peval(cs, x)), sn(m + 1), sn(-m) if m else "1", sn(cs[0] * 2)], sn(m)),
                 "Teğetin eğimi f′(%s) = <b>%s</b>." % (sn(x), sn(m)))

    def denklem():
        cs = [nz(-3, 3), ri(-6, 6), ri(-9, 9)]
        x = ri(-3, 3)
        m = peval(deriv(cs), x)
        y = peval(cs, x)
        c = y - m * x
        g = "y = %s" % lin(m, "x", c)
        return M("f(x) = %s eğrisine x = %s apsisli noktasında çizilen teğetin denklemi hangisidir?" % (poly(cs), sn(x)), g,
                 W3(["y = %s" % lin(m, "x", y), "y = %s" % lin(y, "x", c) if y else "y = %s" % lin(m, "x", c + 1), "y = %s" % lin(m, "x", -c) if c else "y = %s" % lin(m, "x", 2), "y = %s" % lin(-m, "x", c) if m else "y = %s" % lin(1, "x", c)], g),
                 "Nokta (%s, %s), eğim %s: y − %s = %s(x − %s) → <b>%s</b>." % (sn(x), sn(y), sn(m), par(y), sn(m), par(x), g))

    def yatay():
        a = nz(-3, 3)
        r = ri(-5, 5)
        k = ri(-9, 9)
        cs = [a, -2 * a * r, a * r * r + k]
        g = "(%s, %s)" % (sn(r), sn(k))
        return M("f(x) = %s eğrisinin teğetinin yatay olduğu nokta hangisidir?" % poly(cs), g, W3(["(%s, %s)" % (sn(-r), sn(k)), "(%s, %s)" % (sn(r), sn(a * r * r)), "(%s, %s)" % (sn(k), sn(r)), "(0, %s)" % sn(cs[2])], g),
                 "Yatay teğette f′(x) = 0: %s = 0 → x = %s, f(%s) = %s → <b>%s</b>." % (lin(2 * a, "x", -2 * a * r), sn(r), sn(r), sn(k), g))

    def paralel():
        a = nz(-3, 3)
        b = ri(-6, 6)
        m = ri(-9, 9)
        x = F(m - b, 2 * a)
        if x.denominator != 1:
            return None
        return M("f(x) = %s eğrisinin hangi apsisli noktasındaki teğeti y = %s doğrusuna paraleldir?" % (poly([a, b, ri(-5, 5)]), lin(m, "x", ri(-5, 5))), "x = %s" % sn(x),
                 W3(["x = %s" % sn(-x) if x else "x = 1", "x = %s" % sn(F(m, 2 * a)) if F(m, 2 * a) != x else "x = %s" % sn(x + 2), "x = %s" % sn(x + 1), "x = %s" % sn(m)], "x = %s" % sn(x)),
                 "Paralel doğruların eğimleri eşit: %s = %s → x = <b>%s</b>." % (lin(2 * a, "x", b), sn(m), sn(x)))

    def normal():
        cs = [nz(-3, 3), ri(-6, 6), ri(-9, 9)]
        x = ri(-3, 3)
        m = peval(deriv(cs), x)
        if m == 0:
            return None
        n_ = F(-1, m)
        return M("f(x) = %s eğrisine x = %s apsisli noktasında çizilen teğete dik olan doğrunun (normalin) eğimi kaçtır?" % (poly(cs), sn(x)), sn(n_), W3([sn(m), sn(-m), sn(F(1, m)), sn(n_ + 1)], sn(n_)),
                 "Teğetin eğimi %s; dik doğrunun eğimi −1 ÷ %s = <b>%s</b>." % (sn(m), par(m), sn(n_)))

    sets = [("Teğetin eğimi", [(egim, 20)]), ("Teğet denklemi", [(denklem, 20)]), ("Yatay teğet", [(yatay, 20)]),
            ("Paralel teğet", [(paralel, 20)]), ("Normal doğrusu", [(normal, 20)])]
    return U(12, "turevin-geometrik-yorumu", "DM", "MAT.12.4.8", 17, "Türevin Geometrik Yorumu: Teğet Doğrusu", "Türevin Geometrik Yorumu",
             "Bir fonksiyonun bir noktadaki türevini, o noktadaki teğetin eğimi olarak yorumlar; teğet ve normal doğrusunun denklemini bulur.",
             "teğetin eğimi, teğet denklemi, yatay teğet, verilen doğruya paralel teğet, normal doğrusunun eğimi",
             "f′(a) = teğetin eğimi", "Teğet: y − f(a) = f′(a)(x − a).", sets,
             ["f′(a), eğrinin (a, f(a)) noktasındaki teğetinin eğimidir.",
              "Teğet denklemi y − f(a) = f′(a)(x − a)’dır. f′(a) = 0 ise teğet yataydır.",
              "Normal doğrusu teğete diktir; eğimi −1 ÷ f′(a)’dır."],
             [("f(x) = x², x = 3", ["f′(3) = 6", "f(3) = 9"], "y = 6x − 9"), ("f(x) = x² − 4x", ["2x − 4 = 0"], "Yatay teğet (2, −4)")],
             [["Eğim yerine fonksiyonun değerini almak", "Eğim f′(a)"], ["Teğet denkleminde noktayı yanlış almak", "(a, f(a))"], ["Normal eğiminde işareti unutmak", "−1 ÷ m"]],
             [("Teğet eğriyi keser mi?", "Değme noktasının dışında başka bir yerde kesebilir."), ("Yatay teğet ne anlatır?", "Genellikle tepe ya da çukur noktası."),
              ("Bu fikir nerede kullanılır?", "Yaklaşık hesaplamada ve hareketin yönünü bulmada.")])


# ============================================================ 18. türevin uygulamaları
def u18():
    def aralik():
        a = nz(-3, 3)
        r = ri(-5, 5)
        cs = [a, -2 * a * r, ri(-9, 9)]
        k = ch(["artan", "azalan"])
        if (a > 0) == (k == "artan"):
            g = "(%s, ∞)" % sn(r)
        else:
            g = "(−∞, %s)" % sn(r)
        return M("f(x) = %s fonksiyonu hangi aralıkta %sdır?" % (poly(cs), k), g, W3(["(%s, ∞)" % sn(r), "(−∞, %s)" % sn(r), "(%s, ∞)" % sn(-r) if r else "(1, ∞)", "(−∞, %s)" % sn(-r) if r else "(−∞, 1)"], g),
                 "f′(x) = %s; f′(x) %s 0 olan aralık: <b>%s</b>." % (lin(2 * a, "x", -2 * a * r), "&gt;" if k == "artan" else "&lt;", g))

    def ekstrem():
        p, q = sorted(sh(list(range(-4, 5)))[:2])
        # f′(x) = 3(x − p)(x − q) → f = x³ − 3(p+q)/2 x² + 3pq x + c
        if (p + q) % 2:
            return None
        cs = [1, F(-3 * (p + q), 2), 3 * p * q, ri(-9, 9)]
        k = ch(["yerel en büyük", "yerel en küçük"])
        x = p if k == "yerel en büyük" else q
        return M("f(x) = %s fonksiyonunun %s değeri hangi x değerinde alınır?" % (poly(cs), k), "x = %s" % sn(x), W3(["x = %s" % sn(q if x == p else p), "x = %s" % sn(-x) if x else "x = 1", "x = %s" % sn(F(p + q, 2)), "x = 0" if x else "x = 2"], "x = %s" % sn(x)),
                 "f′(x) = 3%s%s; işaret +, −, + olduğundan x = %s’de yerel en büyük, x = %s’de yerel en küçük: <b>x = %s</b>." % (fct(p), fct(q), sn(p), sn(q), sn(x)) if False else
                 "f′(x) = 3%s%s; işaret sırayla +, −, +. Küçük kökte yerel en büyük, büyük kökte yerel en küçük: <b>x = %s</b>." % (fct(p), fct(q), sn(x)))

    def optim():
        k = ri(0, 2)
        if k == 0:
            P = ri(4, 40) * 4
            x = P // 4
            return M("Çevresi %d m olan dikdörtgenlerden alanı en büyük olanın alanı kaç m²’dir?" % P, num(x * x), W3([num(x * x - 1), num(P * P // 8), num(P), num(x * x * 2)], num(x * x)),
                     "A(x) = x(%d − x); A′(x) = %d − 2x = 0 → x = %d → <b>%s m²</b>." % (P // 2, P // 2, x, num(x * x)))
        if k == 1:
            s = ri(4, 30) * 2
            return M("Toplamları %d olan iki pozitif sayının çarpımı en çok kaçtır?" % s, num((s // 2) ** 2), W3([num((s // 2) ** 2 - 1), num(s * s // 2), num(s), num((s // 2 + 1) * (s // 2 - 1) - 1)], num((s // 2) ** 2)),
                     "P(x) = x(%d − x); P′(x) = 0 → x = %d → <b>%s</b>." % (s, s // 2, num((s // 2) ** 2)))
        a = ri(2, 12) * 6
        # kare karton a; köşelerden x kesilip kutu: V = x(a − 2x)²; max x = a/6
        x = a // 6
        v = x * (a - 2 * x) ** 2
        return M("Bir kenarı %d cm olan kare kartonun köşelerinden eş kareler kesilip üstü açık kutu yapılıyor. Hacmin en büyük olması için kesilen karenin kenarı kaç cm olmalıdır?" % a, "%d cm" % x,
                 W3(["%d cm" % (a // 4), "%d cm" % (a // 3), "%d cm" % (x + 1), "%d cm" % (a // 2)], "%d cm" % x), "V(x) = x(%d − 2x)²; V′(x) = 0 → x = %d ÷ 6 = <b>%d cm</b>." % (a, a, x))

    def hiz_ivme():
        a, b, c = ri(1, 3), ri(-6, 6), ri(-9, 9)
        t = ri(1, 6)
        k = ri(0, 1)
        cs = [a, b, c, 0]
        if k == 0:
            v = peval(deriv(cs), t)
            return M("Bir cismin konumu s(t) = %s metredir. t = %d saniyedeki hızı kaç m/s’dir?" % (poly(cs, "t"), t), sn(v), W3([sn(peval(cs, t)), sn(peval(deriv(deriv(cs)), t)), sn(v + 1), sn(v - c)], sn(v)),
                     "v(t) = s′(t) = %s → v(%d) = <b>%s</b>." % (poly(deriv(cs), "t"), t, sn(v)))
        v = peval(deriv(deriv(cs)), t)
        return M("Bir cismin konumu s(t) = %s metredir. t = %d saniyedeki ivmesi kaç m/s²’dir?" % (poly(cs, "t"), t), sn(v), W3([sn(peval(deriv(cs), t)), sn(peval(cs, t)), sn(v + 2), sn(6 * a)], sn(v)),
                 "a(t) = s″(t) = %s → a(%d) = <b>%s</b>." % (poly(deriv(deriv(cs)), "t"), t, sn(v)))

    def mutlak():
        a = nz(-3, 3)
        r = ri(-3, 3)
        k_ = ri(-9, 9)
        cs = [a, -2 * a * r, a * r * r + k_]
        lo, hi = r - ri(1, 3), r + ri(1, 4)
        vals = [peval(cs, lo), peval(cs, hi), k_]
        t = ch(["en büyük", "en küçük"])
        v = max(vals) if t == "en büyük" else min(vals)
        return M("f(x) = %s fonksiyonunun [%s, %s] aralığındaki %s değeri kaçtır?" % (poly(cs), sn(lo), sn(hi), t), sn(v), W3([sn(x) for x in vals] + [sn(v + 1)], sn(v)),
                 "Uç noktalar ve f′(x) = 0 noktası (x = %s) karşılaştırılır: f(%s) = %s, f(%s) = %s, f(%s) = %s → <b>%s</b>." % (sn(r), sn(lo), sn(vals[0]), sn(hi), sn(vals[1]), sn(r), sn(k_), sn(v)))

    sets = [("Artan ve azalan aralıklar", [(aralik, 20)]), ("Yerel ekstremum", [(ekstrem, 20)]), ("Kapalı aralıkta en büyük ve en küçük", [(mutlak, 20)]),
            ("Hız ve ivme", [(hiz_ivme, 20)]), ("Optimizasyon", [(optim, 20)])]
    return U(12, "turevin-uygulamalari", "DM", "MAT.12.4.9", 18, "Türevin Uygulamaları: Artanlık, Ekstremum ve Optimizasyon", "Türevin Uygulamaları",
             "Türevi kullanarak fonksiyonların artan ve azalan olduğu aralıkları, ekstremum noktalarını bulur; optimizasyon ve hareket problemlerini çözer.",
             "artan ve azalan aralıklar, yerel en büyük ve en küçük, kapalı aralıkta mutlak ekstremum, hız ve ivme, optimizasyon problemleri",
             "f′ > 0 artan, f′ < 0 azalan", "Ekstremum noktalarında f′(x) = 0.", sets,
             ["f′(x) &gt; 0 olan aralıkta fonksiyon artan, f′(x) &lt; 0 olan aralıkta azalandır.",
              "f′ işaret değiştirdiği noktada yerel ekstremum vardır: + → − ise yerel en büyük, − → + ise yerel en küçük.",
              "Kapalı aralıkta en büyük ve en küçük değer, uç noktalar ile f′(x) = 0 noktaları karşılaştırılarak bulunur. Konumun türevi hız, hızın türevi ivmedir."],
             [("f(x) = x² − 6x", ["f′ = 2x − 6"], "(3, ∞)’da artan"), ("Çevre 40, en büyük alan", ["x = 10"], "100 m²")],
             [["f′ = 0 olan her noktayı ekstremum sanmak", "İşaret değişmeli"], ["Kapalı aralıkta uç noktaları unutmak", "Uçlar da kontrol edilir"], ["Hız ile ivmeyi karıştırmak", "İvme ikinci türev"]],
             [("Optimizasyon nedir?", "En iyi (en büyük ya da en küçük) değeri bulmaktır."), ("Neden uç noktalar?", "En büyük değer aralığın ucunda da olabilir."),
              ("Nerede kullanılır?", "Maliyet azaltma, kâr artırma ve mühendislik tasarımında.")])


# ============================================================ 19. hazır veriler
def u19():
    def degisim():
        a = ri(20, 200) * 1000
        p = nz(-40, 60)
        b = a + a * p // 100
        if (a * p) % 100:
            return None
        g = "%%%s %s" % (num(abs(p)), "artış" if p > 0 else "azalış")
        return M("Bir ilçenin 2023’teki nüfusu %s, 2024’teki nüfusu %s olarak açıklanmıştır. Nüfustaki yüzde değişim nedir?" % (num(a), num(b)), g,
                 W3(["%%%s %s" % (num(abs(p)), "azalış" if p > 0 else "artış"), "%%%s %s" % (num(abs(b - a) * 100 // b) if (abs(b - a) * 100) % b == 0 else num(abs(p) + 5), "artış" if p > 0 else "azalış"), "%%%s %s" % (num(abs(p) * 2), "artış" if p > 0 else "azalış"), "%%%s %s" % (num(abs(b - a)), "artış" if p > 0 else "azalış") if abs(b - a) < 1000 else "%%%s %s" % (num(abs(p) + 10), "artış" if p > 0 else "azalış")], g),
                 "(%s − %s) ÷ %s · 100 = <b>%s</b>." % (num(b), num(a), num(a), g))

    def tablo():
        yrs = [2020, 2021, 2022, 2023, 2024]
        vals = [ri(30, 90) for _ in yrs]
        k = ri(0, 2)
        t = "<table class='sn-table' style='width:auto'><thead><tr><th>Yıl</th>%s</tr></thead><tbody><tr><td>Üretim (bin ton)</td>%s</tr></tbody></table>" % ("".join("<th>%d</th>" % y for y in yrs), "".join("<td>%d</td>" % v for v in vals))
        if k == 0:
            i = max(range(1, 5), key=lambda j: vals[j] - vals[j - 1])
            if sorted([vals[j] - vals[j - 1] for j in range(1, 5)])[-1] == sorted([vals[j] - vals[j - 1] for j in range(1, 5)])[-2]:
                return None
            g = "%d → %d" % (yrs[i - 1], yrs[i])
            return M("Bir ürünün yıllara göre üretimi tabloda verilmiştir.%sEn büyük artış hangi iki yıl arasında olmuştur?" % t, g, W3(["%d → %d" % (yrs[j - 1], yrs[j]) for j in range(1, 5)], g),
                     "Ardışık farklar: %s → <b>%s</b>." % (", ".join(sn(vals[j] - vals[j - 1]) for j in range(1, 5)), g))
        if k == 1:
            m = F(sum(vals), 5)
            return M("Bir ürünün yıllara göre üretimi tabloda verilmiştir.%sYıllık ortalama üretim kaç bin tondur?" % t, dq(m), W3([dq(m + 1), dq(F(sum(vals), 4)), dq(sorted(vals)[2]) if sorted(vals)[2] != m else dq(m - 2), dq(F(max(vals) + min(vals), 2))], dq(m)),
                     "Toplam %d ÷ 5 = <b>%s</b>." % (sum(vals), dq(m)))
        d = vals[4] - vals[0]
        g = "%s bin ton %s" % (num(abs(d)), "artmıştır" if d > 0 else "azalmıştır") if d else "Değişmemiştir"
        return M("Bir ürünün yıllara göre üretimi tabloda verilmiştir.%s2020’den 2024’e üretim nasıl değişmiştir?" % t, g,
                 W3(["%s bin ton %s" % (num(abs(d)), "azalmıştır" if d > 0 else "artmıştır") if d else "1 bin ton artmıştır", "%s bin ton %s" % (num(abs(d) + 5), "artmıştır" if d > 0 else "azalmıştır"), "Değişmemiştir", "%s bin ton artmıştır" % num(vals[4])], g),
                 "%d − %d = %s → <b>%s</b>." % (vals[4], vals[0], sn(d), g))

    def yorum():
        S = [("Bir haberde yalnızca iki yılın verisine bakılarak “artış sürekli devam edecek” deniyor.", "İki veriyle eğilim hakkında genelleme yapılamaz"),
             ("Bir grafikte dikey eksen 0’dan değil 95’ten başlıyor ve küçük fark çok büyük görünüyor.", "Eksen ölçeği farkı abartıyor"),
             ("Farklı büyüklükteki iki şehrin trafik kazası sayıları doğrudan karşılaştırılıyor.", "Nüfusa göre oranlar karşılaştırılmalı"),
             ("Bir ankette yalnızca bir web sitesinin ziyaretçilerine soru sorulmuş ve sonuç tüm ülkeye genellenmiş.", "Örneklem ülkeyi temsil etmiyor"),
             ("Bir firmanın satışlarının ortalaması verilmiş ama çok büyük tek bir satış ortalamayı yükseltmiş.", "Uç değer ortalamayı etkiliyor; medyan da verilmeli")]
        t, g = ch(S)
        return M("“%s” Bu durumdaki sorun nedir?" % t, g, W3(sh([x for _, x in S]), g), "Cevap: <b>%s</b>." % g)

    def oran():
        a = ri(100, 900) * 1000
        b = ri(1, 9) * 100
        per = F(b * 100000, a)
        if (per * 10).denominator != 1:
            return None
        return M("Nüfusu %s olan bir ilde bir yılda %s yeni iş yeri açılmıştır. 100.000 kişi başına kaç yeni iş yeri düşer?" % (num(a), num(b)), dq(per), W3([dq(per * 10), dq(per / 10), dq(F(b, a // 1000)), dq(per + 1)], dq(per)),
                 "%s ÷ %s · 100.000 = <b>%s</b>." % (num(b), num(a), dq(per)))

    sets = [("Yüzde değişim", [(degisim, 20)]), ("Tablo yorumlama", [(tablo, 20)]), ("Oranla karşılaştırma", [(oran, 20)]),
            ("Yorumları değerlendirme", [(yorum, 5), (tablo, 15)]), ("Karışık", [(degisim, 10), (oran, 10)])]
    return U(12, "hazir-veriler-uzerinde-calisma", "HV", "MAT.12.5.1", 19, "Hazır Veriler Üzerinde Çalışma", "Hazır Veriler",
             "Resmî kurumların yayımladığı hazır veriler üzerinde çalışır; yüzde değişim, ortalama ve oranlarla yorum yapar ve veriyle ilgili iddiaları değerlendirir.",
             "yüzde değişim, tablolardan eğilim ve ortalama, kişi başına oranlar, yanıltıcı grafikler ve yorumları değerlendirme",
             "Sayıları değil oranları karşılaştır", "Yüzde değişim = fark ÷ eski değer × 100.", sets,
             ["Yüzde değişim, iki değer arasındaki farkın eski değere oranının 100 ile çarpımıdır.",
              "Büyüklükleri farklı gruplar karşılaştırılırken kişi başına ya da 100.000 kişi başına oranlar kullanılır.",
              "Bir veriyi yorumlarken kaynağa, örnekleme, eksen ölçeğine ve uç değerlere dikkat edilir."],
             [("2.000 → 2.300", ["300 ÷ 2.000"], "%15 artış"), ("500.000 kişi, 250 olay", ["250 ÷ 5"], "100.000 kişide 50")],
             [["Yüzdeyi yeni değere bölerek bulmak", "Eski değere böl"], ["Farklı büyüklükteki grupları sayıyla karşılaştırmak", "Oranla karşılaştır"], ["Kesik eksenli grafiği olduğu gibi okumak", "Eksenin başlangıcına bak"]],
             [("Hazır veri nereden bulunur?", "TÜİK gibi resmî istatistik kurumlarının yayınlarından."), ("Neden oran?", "Büyük şehirde sayılar doğal olarak büyüktür."),
              ("Grafik yanıltabilir mi?", "Evet; eksen ölçeği ve seçilen aralık algıyı değiştirebilir.")])


UNITS = [u10, u11, u12, u13, u14, u15, u16, u17, u18, u19]
