# -*- coding: utf-8 -*-
"""Türkiye 11. sınıf (2026 DÖP)：MAT.11.1 iki nicel değişken、MAT.11.2 dörtgenler ve çokgenler、MAT.11.3.1 trigonometrik fonksiyonlar。"""
import math
from fractions import Fraction as F
from tr_lise import M, num, sn, par, lin, dq, MINUS, ri, ch, sh, nz, kurve, figure, frs, TRIG, TRIP, U, W3, rts, rt, cap


def setup(rnd):
    pass


def sqs(n):
    o, i = rt(n)
    return rts(o, i) if i > 1 else str(o)


def pis(fr):
    """π’nin katı → '3π/4' (HTML kesir)"""
    fr = F(fr)
    if fr == 0:
        return "0"
    s = MINUS if fr < 0 else ""
    a = abs(fr)
    top = ("" if a.numerator == 1 else str(a.numerator)) + "π"
    return s + (top if a.denominator == 1 else frs(top, a.denominator))


def tbl(xs, ys, xn="x", yn="y"):
    return "<table class='sn-table' style='width:auto'><tbody><tr><td>%s</td>%s</tr><tr><td>%s</td>%s</tr></tbody></table>" % (
        xn, "".join("<td>%s</td>" % num(x) for x in xs), yn, "".join("<td>%s</td>" % num(y) for y in ys))


# ============================================================ 1. iki nicel değişken
def u1():
    CTX = [("haftalık çalışma süresi (saat)", "sınav puanı"), ("hava sıcaklığı (°C)", "satılan dondurma sayısı"), ("arabanın yaşı (yıl)", "arabanın değeri (bin TL)"),
           ("günlük ekran süresi (saat)", "uyku süresi (saat)"), ("ağacın yaşı (yıl)", "ağacın boyu (m)"), ("evin büyüklüğü (m²)", "aylık kira (bin TL)")]

    def yon():
        k = ri(0, 2)
        n = 6
        xs = sorted(sh(list(range(1, 11)))[:n])
        if k == 0:
            ys = [x + ri(0, 2) for x in xs]
            g = "Pozitif yönlü ilişki"
        elif k == 1:
            ys = [12 - x + ri(0, 2) for x in xs]
            g = "Negatif yönlü ilişki"
        else:
            ys = sh([3, 9, 4, 8, 5, 7, 6, 2])[:n]
            r = corr(xs, ys)
            if abs(r) > 0.3:
                return None
            g = "Belirgin bir ilişki yok"
        p = kurve([], (0, 11, 1), (0, 13, 1), pts=[(x, y, "") for x, y in zip(xs, ys)], label="serpme diyagramı")
        return M("Serpme diyagramındaki iki değişken arasında nasıl bir ilişki vardır?%s" % p, g, W3(["Pozitif yönlü ilişki", "Negatif yönlü ilişki", "Belirgin bir ilişki yok", "Önce artan sonra azalan ilişki"], g),
                 "Noktalar %s: <b>%s</b>." % ({0: "sağa doğru yükseliyor", 1: "sağa doğru alçalıyor", 2: "dağınık, bir yön göstermiyor"}[k], g.lower()))

    def r_yorum():
        r = F(ri(-99, 99), 100)
        if abs(r) < F(5, 100):
            return None
        a = abs(r)
        guc = "güçlü" if a >= F(7, 10) else "orta" if a >= F(4, 10) else "zayıf"
        yon_ = "pozitif" if r > 0 else "negatif"
        g = "%s %s ilişki" % (cap(guc), yon_)
        w = ["%s %s ilişki" % (cap(x), y) for x in ("güçlü", "orta", "zayıf") for y in ("pozitif", "negatif")]
        return M("İki değişken arasındaki korelasyon katsayısı r = %s olarak bulunmuştur. Bu ilişki nasıl yorumlanır? (|r| ≥ 0,7 güçlü, 0,4 ≤ |r| &lt; 0,7 orta, |r| &lt; 0,4 zayıf)" % dq(r, 2), g,
                 W3(sh(w), g), "|r| = %s ve işaret %s: <b>%s</b>." % (dq(a, 2), "artı" if r > 0 else "eksi", g.lower()))

    def tahmin():
        xn, yn = ch(CTX)
        a, b = F(ri(10, 90)), F(ri(-40, 40), 10)
        if b == 0:
            return None
        x = ri(2, 12)
        y = a + b * x
        if y <= 0:
            return None
        return M("“%s” (x) ile “%s” (y) için regresyon doğrusu ŷ = %s + %sx olarak bulunmuştur. x = %d için tahmin edilen y değeri kaçtır?" % (xn, yn, dq(a), dq(b) if b > 0 else "(" + dq(b) + ")", x),
                 dq(y), W3([dq(a + b), dq(y + b), dq(b * x), dq(a * x + b)], dq(y)), "ŷ = %s + %s · %d = <b>%s</b>." % (dq(a), par(dq(b)) if b < 0 else dq(b), x, dq(y)))

    def egim():
        xn, yn = ch(CTX)
        a, b = F(ri(10, 90)), F(ri(-40, 40), 10)
        if b == 0:
            return None
        g = "%s birim %s" % (dq(abs(b)), "artar" if b > 0 else "azalır")
        return M("“%s” (x) ile “%s” (y) için regresyon doğrusu ŷ = %s %s %sx’tir. x 1 birim artınca y ortalama olarak nasıl değişir?" % (xn, yn, dq(a), "+" if b > 0 else "−", dq(abs(b))) if False else
                 "“%s” (x) ile “%s” (y) için regresyon doğrusu ŷ = %s %s %sx olarak bulunmuştur. x 1 birim artınca y ortalama olarak nasıl değişir?" % (xn, yn, dq(a), "+" if b > 0 else "−", dq(abs(b))),
                 g, W3(["%s birim %s" % (dq(abs(b)), "azalır" if b > 0 else "artar"), "%s birim artar" % dq(a), "%s birim azalır" % dq(a + abs(b)), "Değişmez"], g),
                 "Doğrunun eğimi %s: x 1 artınca y <b>%s</b>." % (dq(b), g))

    def ortalama():
        a, b = ri(-10, 30), nz(-6, 6)
        xbar = ri(2, 15)
        ybar = a + b * xbar
        return M("Bir veri setinde x̄ = %d’dir ve regresyon doğrusu ŷ = %s’dir. Doğru (x̄, ȳ) noktasından geçtiğine göre ȳ kaçtır?" % (xbar, lin(b, "x", a)) if False else
                 "Bir veri setinde x değerlerinin ortalaması x̄ = %d ve regresyon doğrusu ŷ = %s olarak bulunmuştur. Doğru (x̄, ȳ) noktasından geçtiğine göre ȳ kaçtır?" % (xbar, lin(b, "x", a)),
                 sn(ybar), W3([sn(ybar + b), sn(a), sn(b * xbar), sn(ybar - a + 1)], sn(ybar)), "ȳ = %s = <b>%s</b>." % (lin(b, "·" + " %d" % xbar, a).replace("x", ""), sn(ybar)) if False else "ȳ = %s · %d %s %s = <b>%s</b>." % (sn(b), xbar, "+" if a >= 0 else "−", sn(abs(a)), sn(ybar)))

    def neden():
        S = [("Dondurma satışları arttıkça boğulma olayları da artıyor.", "Her ikisini de sıcak hava etkiliyor; neden-sonuç yoktur"),
             ("Ayakkabı numarası büyük olan öğrencilerin okuma hızı daha yüksek.", "İkisi de yaşla artıyor; neden-sonuç yoktur"),
             ("Bir şehirde itfaiyeci sayısı arttıkça yangın hasarı da artıyor.", "Büyük yangınlara çok itfaiyeci gidiyor; neden-sonuç tersine yorumlanmış"),
             ("Kahve içen kişilerin uykusu daha az.", "İlişki neden-sonuç için tek başına yeterli değildir")]
        t, g = ch(S)
        return M("“%s” Bu korelasyonla ilgili en doğru yorum hangisidir?" % t, g, W3([x for _, x in S] + ["Biri diğerinin kesin nedenidir"], g),
                 "Korelasyon, neden-sonuç ilişkisi olduğunu göstermez. Cevap: <b>%s</b>." % g)

    sets = [("Serpme diyagramı", [(yon, 20)]), ("Korelasyon katsayısı", [(r_yorum, 16), (neden, 4)]), ("Regresyon doğrusuyla tahmin", [(tahmin, 20)]),
            ("Eğimin anlamı", [(egim, 20)]), ("Ortalama noktası", [(ortalama, 20)])]
    return U(11, "iki-nicel-degiskenli-veri", "IA", "MAT.11.1.1, MAT.11.1.2", 1, "İki Nicel Değişkenli Veri: Korelasyon ve Regresyon", "Korelasyon ve Regresyon",
             "İki nicel değişkenli veri ile çalışarak serpme diyagramı oluşturur, korelasyonu yorumlar, regresyon doğrusuyla tahmin yapar ve başkalarının yorumlarını değerlendirir.",
             "serpme diyagramı, korelasyonun yönü ve gücü, korelasyon katsayısı, regresyon doğrusuyla tahmin, eğimin anlamı, korelasyon ve neden-sonuç",
             "Korelasyon neden-sonuç değildir", "ŷ = a + bx; b, x 1 artınca y’nin ortalama değişimidir.", sets,
             ["Serpme diyagramında noktalar sağa doğru yükseliyorsa pozitif, alçalıyorsa negatif yönlü ilişki vardır.",
              "Korelasyon katsayısı r, −1 ile 1 arasındadır; |r| 1’e yaklaştıkça doğrusal ilişki güçlenir.",
              "Regresyon doğrusu ŷ = a + bx ile tahmin yapılır; doğru (x̄, ȳ) noktasından geçer. İlişki olması neden-sonuç olduğunu göstermez."],
             [("ŷ = 40 + 5x, x = 6", ["40 + 30"], "70"), ("r = −0,85", ["|r| ≥ 0,7", "eksi"], "Güçlü negatif ilişki")],
             [["Negatif korelasyonu zayıf sanmak", "İşaret yönü, büyüklük gücü gösterir"], ["Eğimi sabit terimle karıştırmak", "Eğim x’in katsayısıdır"], ["İlişkiyi neden sanmak", "Üçüncü bir değişken olabilir"]],
             [("r = 0 ne demek?", "Doğrusal bir ilişki yoktur; başka türlü bir ilişki olabilir."), ("Veri aralığının dışında tahmin güvenilir mi?", "Hayır; ilişki o bölgede değişebilir."),
              ("Regresyon doğrusu nasıl bulunur?", "Noktalara en yakın geçen doğru en küçük kareler yöntemiyle bulunur.")])


def corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return sxy / (sx * sy) if sx and sy else 0


# ============================================================ 2. dörtgenlerin özellikleri
def u2():
    def aci():
        a, b, c = ri(50, 140), ri(50, 140), ri(50, 140)
        d = 360 - a - b - c
        if not 20 <= d <= 170:
            return None
        return M("ABCD dörtgeninde m(A) = %d°, m(B) = %d° ve m(C) = %d° ise m(D) kaç derecedir?" % (a, b, c), "%d°" % d, W3(["%d°" % (180 - d) if d != 90 else "100°", "%d°" % (d + 10), "%d°" % (540 - a - b - c) if 540 - a - b - c < 300 else "%d°" % (d - 10), "%d°" % abs(180 - a - b + c)], "%d°" % d),
                 "Dörtgenin iç açıları toplamı 360°: 360 − %d − %d − %d = <b>%d°</b>." % (a, b, c, d))

    def oran():
        rs = ch([(1, 2, 3, 4), (2, 3, 4, 3), (1, 1, 2, 2), (3, 4, 5, 6), (2, 2, 3, 5), (1, 2, 2, 3), (4, 5, 6, 3), (5, 6, 7, 6), (2, 3, 3, 4), (1, 3, 4, 4)])
        k = F(360, sum(rs))
        if k.denominator != 1:
            return None
        i = ri(0, 3)
        n = ["A", "B", "C", "D"][i]
        v = rs[i] * k
        return M("ABCD dörtgeninin açıları %s oranındadır (A : B : C : D). m(%s) kaç derecedir?" % (" : ".join(map(str, rs)), n), "%d°" % v, W3(["%d°" % (rs[(i + 1) % 4] * k), "%d°" % (rs[i] * 180 // sum(rs)), "%d°" % k, "%d°" % (v + 10)], "%d°" % v),
                 "Bir pay = 360 ÷ %d = %d°; m(%s) = %d · %d = <b>%d°</b>." % (sum(rs), k, n, rs[i], k, v))

    def dis():
        a, b, c = ri(60, 130), ri(60, 130), ri(60, 130)
        d = 360 - a - b - c
        if not 30 <= d <= 170:
            return None
        return M("Bir dörtgenin üç dış açısı %d°, %d° ve %d°’dir. Dördüncü dış açı kaç derecedir?" % (a, b, c) if False else "Bir dörtgenin üç dış açısının ölçüleri %d°, %d° ve %d° ise dördüncü dış açı kaç derecedir?" % (a, b, c),
                 "%d°" % d, W3(["%d°" % (180 - d), "%d°" % (d + 20), "%d°" % (d - 20) if d > 40 else "%d°" % (d + 30)], "%d°" % d), "Dış açılar toplamı 360°: <b>%d°</b>." % d)

    def kosegen():
        S = [("Köşegenleri birbirini ortalayan en genel dörtgen", "Paralelkenar"), ("Köşegenleri eşit uzunlukta olan paralelkenar", "Dikdörtgen"),
             ("Köşegenleri dik kesişen paralelkenar", "Eşkenar dörtgen"), ("Köşegenleri eşit ve dik kesişen paralelkenar", "Kare"),
             ("Yalnızca bir çift karşılıklı kenarı paralel olan dörtgen", "Yamuk"), ("İki çift komşu kenarı eşit olan ve paralelkenar olmayan dörtgen", "Deltoid")]
        t, g = ch(S)
        return M("%s hangisidir?" % t, g, W3(sh([x for _, x in S]), g), "Cevap: <b>%s</b>." % g)

    def ickenar():
        a = ri(3, 30)
        b = ri(3, 30)
        c = ri(3, 30)
        lo, hi = 1, a + b + c - 1
        if a + b + c > 60:
            return None
        return M("Bir dörtgenin üç kenarı %d cm, %d cm ve %d cm’dir. Dördüncü kenar en çok kaç cm olabilir? (Kenar uzunlukları tam sayıdır.)" % (a, b, c) if False else
                 "Bir dörtgenin üç kenarının uzunlukları %d cm, %d cm ve %d cm olsun. Dördüncü kenar tam sayı ise en çok kaç cm olabilir?" % (a, b, c),
                 "%d cm" % hi, W3(["%d cm" % (hi + 1), "%d cm" % (a + b), "%d cm" % (hi - 1), "%d cm" % max(a, b, c)], "%d cm" % hi),
                 "Bir kenar diğer üç kenarın toplamından küçük olmalı: %d + %d + %d = %d → en çok <b>%d cm</b>." % (a, b, c, a + b + c, hi))

    sets = [("İç açılar", [(aci, 20)]), ("Açıların oranı", [(oran, 10), (aci, 10)]), ("Dış açılar", [(dis, 20)]),
            ("Köşegen özellikleri", [(kosegen, 6), (ickenar, 14)]), ("Karışık", [(aci, 7), (dis, 7), (ickenar, 6)])]
    return U(11, "dortgenlerin-ozellikleri", "GS", "MAT.11.2.1", 2, "Dörtgenlerin Özellikleri: Açılar, Kenarlar ve Köşegenler", "Dörtgenlerin Özellikleri",
             "Dörtgenlerin açı, kenar ve köşegen özelliklerine ilişkin çıkarım yapar.",
             "iç açılar toplamı, açıların oranı, dış açılar toplamı, köşegen özelliklerine göre dörtgenler, kenar uzunluğu sınırları",
             "İç açılar toplamı 360°", "Dış açılar toplamı da 360°’dir.", sets,
             ["Bir köşegen dörtgeni iki üçgene ayırır; bu yüzden iç açılar toplamı 2 · 180° = 360°’dir.",
              "Dışbükey dörtgende her köşedeki dış açı 180° − iç açıdır ve dış açılar toplamı 360°’dir.",
              "Bir dörtgende herhangi bir kenar, diğer üç kenarın toplamından küçüktür."],
             [("A = 80°, B = 95°, C = 110°", ["360 − 285"], "75°"), ("Oran 1 : 2 : 3 : 4", ["360 ÷ 10 = 36"], "36°, 72°, 108°, 144°")],
             [["Toplamı 180° almak", "Dörtgende 360°"], ["Dış açıyı iç açıyla karıştırmak", "Dış açı = 180° − iç açı"], ["Oranda paya bölmeyi unutmak", "Önce bir payı bul"]],
             [("İçbükey dörtgende toplam değişir mi?", "Hayır, iç açılar toplamı yine 360°’dir."), ("Köşegen sayısı kaçtır?", "Her dörtgende 2 köşegen vardır."),
              ("Dörtgenler nasıl sınıflanır?", "Paralel kenarlarına, kenar ve açı eşitliklerine ve köşegen özelliklerine göre.")])


# ============================================================ 3. özel dörtgenler
def u3():
    def paralelkenar():
        a = ri(35, 145)
        if a == 90:
            return None
        k = ri(0, 1)
        if k == 0:
            return M("Bir paralelkenarın bir açısının ölçüsü %d° ise bu açıya komşu açının ölçüsü kaç derecedir?" % a, "%d°" % (180 - a), W3(["%d°" % a, "%d°" % (360 - a), "%d°" % (90 - a) if a < 90 else "%d°" % (a - 90)], "%d°" % (180 - a)),
                     "Paralelkenarda komşu açılar bütünlerdir: 180 − %d = <b>%d°</b>." % (a, 180 - a))
        x = ri(5, 30)
        p, q = ri(2, 5), ri(1, 40)
        A1 = p * x + q
        if not 20 < A1 < 160:
            return None
        return M("ABCD paralelkenarında m(A) = (%s)° ve m(C) = %d° ise x kaçtır?" % (lin(p, "x", q), A1), sn(x), W3([sn(F(180 - A1 - q, p)) if (180 - A1 - q) > 0 and (180 - A1 - q) % p == 0 else sn(x + 1), sn(x - 1), sn(x + 2)], sn(x)),
                 "Paralelkenarda karşılıklı açılar eşittir: %s = %d → x = <b>%d</b>." % (lin(p, "x", q), A1, x))

    def eskenar():
        a, b, c = ch(TRIP[:4])
        k = ri(1, 4)
        d1, d2 = 2 * a * k, 2 * b * k
        kk = ri(0, 1)
        if kk == 0:
            return M("Köşegenlerinin uzunlukları %d cm ve %d cm olan eşkenar dörtgenin alanı kaç cm²’dir?" % (d1, d2), num(d1 * d2 // 2), W3([num(d1 * d2), num(d1 * d2 // 4), num(d1 + d2), num(2 * (d1 + d2))], num(d1 * d2 // 2)),
                     "A = d₁ · d₂ ÷ 2 = %d · %d ÷ 2 = <b>%s</b>." % (d1, d2, num(d1 * d2 // 2)))
        return M("Köşegenlerinin uzunlukları %d cm ve %d cm olan eşkenar dörtgenin bir kenarı kaç cm’dir?" % (d1, d2), "%d cm" % (c * k), W3(["%d cm" % ((d1 + d2) // 2), "%d cm" % (c * k * 2), "%d cm" % (a * k + b * k), "%d cm" % (c * k + 1)], "%d cm" % (c * k)),
                 "Köşegenler birbirini dik ortalar: kenar = √(%d² + %d²) = <b>%d cm</b>." % (a * k, b * k, c * k))

    def dikdortgen():
        a, b, c = ch(TRIP)
        k = ri(1, 4)
        a, b, c = a * k, b * k, c * k
        return M("Kenarları %d cm ve %d cm olan dikdörtgenin köşegeni kaç cm’dir?" % (a, b), "%d cm" % c, W3(["%d cm" % (a + b), "%d cm" % (c + k), "%d cm" % (c * 2), "%d cm" % abs(b - a)], "%d cm" % c),
                 "Pisagor: √(%d + %d) = <b>%d cm</b>." % (a * a, b * b, c))

    def kare():
        a = ri(2, 20)
        k = ri(0, 1)
        if k == 0:
            return M("Bir kenarı %d cm olan karenin köşegeni kaç cm’dir?" % a, "%s cm" % rts(a, 2), W3(["%d cm" % (2 * a), "%s cm" % rts(a, 3), "%s cm" % rts(2 * a, 2), "%d cm" % a], "%s cm" % rts(a, 2)),
                     "Köşegen = kenar · √2 = <b>%s cm</b>." % rts(a, 2))
        d = 2 * a
        return M("Köşegeni %d cm olan karenin alanı kaç cm²’dir?" % d, num(d * d // 2), W3([num(d * d), num(d * d // 4), num(a * a), num(2 * d)], num(d * d // 2)),
                 "Kare bir eşkenar dörtgendir: A = d · d ÷ 2 = <b>%s</b>." % num(d * d // 2))

    def yamuk():
        a, c = ri(4, 30), ri(4, 30)
        if a == c or (a + c) % 2:
            return None
        h = ri(2, 15)
        k = ri(0, 1)
        if k == 0:
            v = (a + c) * h // 2
            return M("Tabanları %d cm ve %d cm, yüksekliği %d cm olan yamuğun alanı kaç cm²’dir?" % (a, c, h), num(v), W3([num((a + c) * h), num(a * c * h // 2) if a * c * h % 2 == 0 else num(v + h), num(v + h), num((a + c + h))], num(v)),
                     "A = (a + c) ÷ 2 · h = %d · %d = <b>%s</b>." % ((a + c) // 2, h, num(v)))
        return M("Tabanları %d cm ve %d cm olan yamuğun orta tabanı kaç cm’dir?" % (a, c), "%d cm" % ((a + c) // 2), W3(["%d cm" % (a + c), "%d cm" % (abs(a - c) // 2 or 1), "%d cm" % ((a + c) // 2 + 1)], "%d cm" % ((a + c) // 2)),
                 "Orta taban tabanların ortalamasıdır: <b>%d cm</b>." % ((a + c) // 2))

    def sinif():
        S = [("Her kare bir dikdörtgendir.", "Doğru"), ("Her dikdörtgen bir karedir.", "Yanlış"), ("Her kare bir eşkenar dörtgendir.", "Doğru"),
             ("Her eşkenar dörtgen bir paralelkenardır.", "Doğru"), ("Her paralelkenar bir dikdörtgendir.", "Yanlış"), ("Her yamuk bir paralelkenardır.", "Yanlış"),
             ("Dikdörtgenin köşegenleri eşittir.", "Doğru"), ("Eşkenar dörtgenin köşegenleri eşittir.", "Yanlış"), ("Paralelkenarın köşegenleri birbirini ortalar.", "Doğru"),
             ("Deltoidin köşegenleri dik kesişir.", "Doğru"), ("Her eşkenar dörtgen bir karedir.", "Yanlış"), ("İkizkenar yamukta taban açıları eşittir.", "Doğru")]
        t, g = ch(S)
        return M("“%s” ifadesi doğru mu, yanlış mı?" % t, g, ["Yanlış" if g == "Doğru" else "Doğru", "Yalnızca bazı durumlarda doğru", "Karar verilemez"],
                 "Özel dörtgenler arasındaki ilişkilere göre: <b>%s</b>." % g.lower())

    sets = [("Paralelkenar", [(paralelkenar, 20)]), ("Dikdörtgen ve kare", [(dikdortgen, 10), (kare, 10)]), ("Eşkenar dörtgen", [(eskenar, 20)]),
            ("Yamuk", [(yamuk, 20)]), ("Dörtgenler arası ilişkiler", [(sinif, 10), (kare, 10)])]
    return U(11, "ozel-dortgenler", "GS", "MAT.11.2.2", 3, "Özel Dörtgenler: Paralelkenar, Eşkenar Dörtgen, Dikdörtgen, Kare, Yamuk", "Özel Dörtgenler",
             "Özel dörtgenlerin özellikleri ve bu dörtgenler arasındaki ilişkileri inceler; kenar, açı, köşegen ve alan hesaplar.",
             "paralelkenarda açılar, dikdörtgen ve kare köşegeni, eşkenar dörtgenin alanı ve kenarı, yamuğun alanı ve orta tabanı, özel dörtgenler arası ilişkiler",
             "Kare hem dikdörtgen hem eşkenar dörtgen", "Eşkenar dörtgende A = d₁ · d₂ ÷ 2.", sets,
             ["Paralelkenarda karşılıklı kenarlar ve açılar eşittir, komşu açılar bütünlerdir, köşegenler birbirini ortalar.",
              "Dikdörtgenin köşegenleri eşittir; eşkenar dörtgenin köşegenleri dik kesişir ve alan d₁ · d₂ ÷ 2’dir. Kare her iki özelliği taşır.",
              "Yamuğun alanı (a + c) ÷ 2 · h’dir; orta taban (a + c) ÷ 2’dir."],
             [("Köşegenler 6 ve 8", ["Yarıları 3 ve 4"], "Kenar 5, alan 24"), ("Tabanlar 6 ve 10, h = 4", ["8 · 4"], "32")],
             [["Eşkenar dörtgenin köşegenlerini eşit sanmak", "Yalnızca karede eşittir"], ["Yamuk alanında ikiye bölmeyi unutmak", "Ortalama taban × h"],
              ["Komşu açıları eşit sanmak", "Komşu açılar toplamı 180°"]],
             [("Kare neden eşkenar dörtgendir?", "Bütün kenarları eşit olduğu için."), ("Deltoid nedir?", "İki çift komşu kenarı eşit olan dörtgendir."),
              ("Dikdörtgenin köşegenleri neden eşit?", "Eş dik üçgenlerin hipotenüsleri oldukları için.")])


# ============================================================ 4. çokgenler
def u4():
    def ic():
        n = ri(5, 40)
        v = (n - 2) * 180
        return M("%d kenarlı bir çokgenin iç açılarının ölçüleri toplamı kaç derecedir?" % n, "%s°" % num(v), W3(["%s°" % num(n * 180), "%s°" % num((n - 1) * 180), "%s°" % num((n - 3) * 180), "360°"], "%s°" % num(v)),
                 "(n − 2) · 180° = %d · 180° = <b>%s°</b>." % (n - 2, num(v)))

    def duzgun():
        n = ch([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
        k = ri(0, 1)
        if k == 0:
            v = F((n - 2) * 180, n)
            return M("Düzgün %d kenarlı bir çokgenin bir iç açısı kaç derecedir?" % n, "%s°" % dq(v), W3(["%s°" % dq(F(360, n)), "%s°" % dq(180 - v + 10), "%s°" % dq(F((n - 1) * 180, n)), "%s°" % dq(v + 5)], "%s°" % dq(v)),
                     "(%d − 2) · 180 ÷ %d = <b>%s°</b>." % (n, n, dq(v)))
        return M("Bir dış açısının ölçüsü %s° olan düzgün çokgen kaç kenarlıdır?" % dq(F(360, n)), num(n), W3([num(n + 2), num(n - 1), num(2 * n), num(n + 1)], num(n)),
                 "Dış açılar toplamı 360°: 360 ÷ %s = <b>%d</b>." % (dq(F(360, n)), n))

    def kosegen():
        n = ri(4, 25)
        v = n * (n - 3) // 2
        k = ri(0, 1)
        if k == 0:
            return M("%d kenarlı bir çokgenin kaç köşegeni vardır?" % n, num(v), W3([num(n * (n - 3)), num(n - 3), num(n * (n - 1) // 2), num(v + n)], num(v)), "n(n − 3) ÷ 2 = %d · %d ÷ 2 = <b>%d</b>." % (n, n - 3, v))
        return M("Bir köşesinden %d köşegen çizilebilen çokgen kaç kenarlıdır?" % (n - 3), num(n), W3([num(n - 3), num(n - 1), num(n + 3), num(n - 2)], num(n)), "Bir köşeden n − 3 köşegen çıkar: n = %d + 3 = <b>%d</b>." % (n - 3, n))

    def bukey():
        S = [("Bütün iç açıları 180°’den küçük olan çokgen", "Dışbükey çokgen"), ("En az bir iç açısı 180°’den büyük olan çokgen", "İçbükey çokgen"),
             ("Bütün köşegenleri çokgenin içinde kalan çokgen", "Dışbükey çokgen"), ("En az bir köşegeni çokgenin dışına taşan çokgen", "İçbükey çokgen"),
             ("Kenarları ve açıları eşit olan dışbükey çokgen", "Düzgün çokgen")]
        t, g = ch(S)
        return M("%s nasıl adlandırılır?" % t, g, W3(["Dışbükey çokgen", "İçbükey çokgen", "Düzgün çokgen", "Yıldız çokgen"], g), "Cevap: <b>%s</b>." % g)

    def eksik():
        n = ri(5, 8)
        T = (n - 2) * 180
        angs = [ri(95, 160) for _ in range(n - 1)]
        x = T - sum(angs)
        if not 60 <= x <= 175:
            return None
        return M("%d kenarlı dışbükey bir çokgenin açılarından %d tanesinin ölçüleri %s° ise kalan açı kaç derecedir?" % (n, n - 1, "°, ".join(map(str, angs))), "%d°" % x,
                 W3(["%d°" % (x + 180) if x + 180 < 360 else "%d°" % (x - 30), "%d°" % (x - 10), "%d°" % (x + 20), "%d°" % (180 - x)], "%d°" % x), "Toplam (%d − 2) · 180 = %s°; %s − %s = <b>%d°</b>." % (n, num(T), num(T), num(sum(angs)), x))

    sets = [("İç açılar toplamı", [(ic, 20)]), ("Düzgün çokgenler", [(duzgun, 20)]), ("Köşegen sayısı", [(kosegen, 20)]),
            ("Eksik açı", [(eksik, 20)]), ("Dışbükey ve içbükey", [(bukey, 5), (ic, 8), (kosegen, 7)])]
    return U(11, "cokgenler", "GS", "MAT.11.2.3, MAT.11.2.4", 4, "Çokgenler: İç ve Dış Açılar, Köşegenler", "Çokgenler",
             "İçbükey ve dışbükey çokgenleri ayırt eder; dışbükey çokgenlerin iç ve dış açıları ile köşegen sayısına ilişkin özellikleri kullanır.",
             "iç açılar toplamı, düzgün çokgenin iç ve dış açısı, köşegen sayısı, eksik açı, dışbükey ve içbükey çokgen",
             "İç açılar toplamı (n − 2) · 180°", "Dış açılar toplamı her zaman 360°.", sets,
             ["n kenarlı dışbükey çokgen bir köşeden çizilen köşegenlerle n − 2 üçgene ayrılır; iç açılar toplamı (n − 2) · 180°’dir.",
              "Dış açılar toplamı 360°’dir; düzgün çokgende bir dış açı 360° ÷ n’dir.",
              "Köşegen sayısı n(n − 3) ÷ 2’dir. Bütün iç açıları 180°’den küçük çokgen dışbükey, en az biri büyükse içbükeydir."],
             [("Altıgen", ["(6 − 2) · 180"], "720°"), ("Dış açı 24°", ["360 ÷ 24"], "15 kenar")],
             [["n · 180 almak", "(n − 2) · 180"], ["Köşegen sayısında 2’ye bölmeyi unutmak", "Her köşegen iki kez sayılır"], ["Dış açıyı iç açıyla karıştırmak", "İç + dış = 180°"]],
             [("Üçgenin köşegeni var mı?", "Hayır; n(n − 3) ÷ 2 = 0."), ("Düzgün çokgen ne demek?", "Bütün kenarları ve açıları eşit."),
              ("Arı peteği neden altıgen?", "Düzgün altıgenler boşluk bırakmadan kaplar ve az malzemeyle çok alan sağlar.")])


# ============================================================ 5. çokgen problemleri
def u5():
    def altigen():
        a = ri(2, 16)
        k = ri(0, 1)
        if k == 0:
            g = rts(F(3 * a * a, 2), 3) if (3 * a * a) % 2 == 0 else frs(rts(3 * a * a, 3), 2)
            return M("Bir kenarı %d cm olan düzgün altıgenin alanı kaç cm²’dir?" % a, g, W3([rts(F(a * a, 4), 3) if (a * a) % 4 == 0 else frs(rts(a * a, 3), 4), rts(6 * a * a, 3), rts(3 * a * a, 3), frs(rts(3 * a * a, 2), 2)], g),
                     "Düzgün altıgen 6 eşkenar üçgendir: 6 · %d²√3 ÷ 4 = <b>%s</b>." % (a, g))
        return M("Bir kenarı %d cm olan düzgün altıgenin en uzun köşegeni kaç cm’dir?" % a, "%d cm" % (2 * a), W3(["%s cm" % rts(a, 3), "%d cm" % a, "%d cm" % (3 * a), "%s cm" % rts(a, 2)], "%d cm" % (2 * a)),
                 "En uzun köşegen iki kenar uzunluğundadır: <b>%d cm</b>." % (2 * a))

    def eskenar():
        a = ri(1, 30) * 2
        g = rts(a * a // 4, 3)
        return M("Bir kenarı %d cm olan eşkenar üçgenin alanı kaç cm²’dir?" % a, g, W3([rts(a * a // 2, 3), rts(a * a, 3), num(a * a // 2), rts(a * a // 4, 2)], g), "A = a²√3 ÷ 4 = %d · √3 ÷ 4 = <b>%s</b>." % (a * a, g))

    def ickenar():
        n = ch([3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90])
        v = F((n - 2) * 180, n)
        if v.denominator != 1:
            return None
        return M("Bir iç açısı %d° olan düzgün çokgenin kaç köşegeni vardır?" % v, num(n * (n - 3) // 2), W3([num(n), num(n * (n - 3)), num(n - 3), num(n * (n - 3) // 2 + n)], num(n * (n - 3) // 2)),
                 "Dış açı 180 − %d = %d°, n = 360 ÷ %d = %d; köşegen %d · %d ÷ 2 = <b>%s</b>." % (v, 180 - v, 180 - v, n, n, n - 3, num(n * (n - 3) // 2))) if n > 3 else None

    def kaplama():
        S = [("Düzgün altıgen", "Kaplar"), ("Kare", "Kaplar"), ("Eşkenar üçgen", "Kaplar"), ("Düzgün beşgen", "Kaplamaz"), ("Düzgün sekizgen", "Kaplamaz"), ("Düzgün ongen", "Kaplamaz"),
             ("Düzgün onikigen", "Kaplamaz"), ("Düzgün dokuzgen", "Kaplamaz")]
        t, g = ch(S)
        return M("Yalnızca eş “%s” biçimindeki karolarla bir düzlem boşluk ve üst üste binme olmadan kaplanabilir mi?" % low_(t), g if g == "Kaplar" else "Kaplamaz",
                 ["Kaplamaz" if g == "Kaplar" else "Kaplar", "Yalnızca kenar uzunluğu 1 ise kaplar", "Karar verilemez"],
                 "Bir köşede birleşen iç açılar toplamı 360° olmalı; iç açı 360°’yi tam bölmelidir: <b>%s</b>." % g.lower())

    def cevre():
        n = ri(5, 12)
        a = ri(2, 15)
        k = ri(0, 1)
        if k == 0:
            return M("Bir kenarı %d cm olan düzgün %d kenarlı çokgenin çevresi kaç cm’dir?" % (a, n), "%d cm" % (n * a), W3(["%d cm" % ((n - 1) * a), "%d cm" % (n + a), "%d cm" % ((n + 1) * a)], "%d cm" % (n * a)), "%d · %d = <b>%d cm</b>." % (n, a, n * a))
        T = (n - 2) * 180
        return M("İç açıları toplamı %s° olan düzgün çokgenin bir kenarı %d cm ise çevresi kaç cm’dir?" % (num(T), a), "%d cm" % (n * a), W3(["%d cm" % ((n - 2) * a), "%d cm" % ((n + 2) * a), "%d cm" % ((n - 1) * a)], "%d cm" % (n * a)),
                 "(n − 2) · 180 = %s → n = %d; çevre %d · %d = <b>%d cm</b>." % (num(T), n, n, a, n * a))

    sets = [("Eşkenar üçgenin alanı", [(eskenar, 20)]), ("Düzgün altıgen", [(altigen, 20)]), ("İç açı, kenar ve köşegen", [(ickenar, 10), (cevre, 10)]),
            ("Düzlemi kaplama ve çevre", [(kaplama, 6), (cevre, 14)]), ("Karışık", [(altigen, 8), (eskenar, 6), (cevre, 6)])]
    return U(11, "cokgen-problemleri", "GS", "MAT.11.2.5", 5, "Çokgenlerle İlgili Problemler", "Çokgen Problemleri",
             "Çokgenlerin özelliklerini kullanarak alan, çevre, açı ve köşegen problemleri çözer; düzgün çokgenlerle düzlemi kaplamayı inceler.",
             "eşkenar üçgenin alanı, düzgün altıgenin alanı ve köşegeni, iç açıdan kenar ve köşegen sayısı, düzgün çokgenin çevresi, düzlemi kaplama",
             "Düzgün altıgen 6 eşkenar üçgendir", "Eşkenar üçgenin alanı a²√3 ÷ 4.", sets,
             ["Kenarı a olan eşkenar üçgenin alanı a²√3 ÷ 4’tür.",
              "Düzgün altıgen merkezden köşelere çizilen doğru parçalarıyla 6 eş eşkenar üçgene ayrılır; alanı 6 · a²√3 ÷ 4’tür.",
              "Düzlemi tek tür düzgün çokgenle kaplamak için iç açı 360°’yi tam bölmelidir; bu yalnızca eşkenar üçgen, kare ve düzgün altıgende olur."],
             [("Eşkenar üçgen, a = 6", ["36√3 ÷ 4"], "9√3"), ("Düzgün altıgen, a = 2", ["6 · √3"], "6√3")],
             [["Eşkenar üçgen alanında √3’ü unutmak", "a²√3 ÷ 4"], ["Altıgeni 4 üçgene ayırmak", "Merkezden 6 üçgen"], ["Her düzgün çokgenin düzlemi kapladığını sanmak", "Yalnızca 3, 4 ve 6 kenarlılar"]],
             [("Neden beşgen kaplamaz?", "İç açısı 108° ve 360 ÷ 108 tam sayı değildir."), ("Farklı çokgenlerle kaplanabilir mi?", "Evet, örneğin sekizgen ve kare birlikte kaplar."),
              ("Nerede görülür?", "Yer karolarında, arı peteğinde ve mozaiklerde.")])


def low_(s):
    from tr_common import low
    return low(s)


# ============================================================ 6. trigonometrik fonksiyonlar (birim çember)
QUAD_ANG = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]


def tval(f, d):
    """sin/cos/tan of degree d (special) → Fraction-like (sign, base angle) string"""
    r = math.radians(d)
    v = {"sin": math.sin(r), "cos": math.cos(r), "tan": math.tan(r) if d % 180 != 90 else None}[f]
    if v is None:
        return "Tanımsız"
    base = {0: 0, 30: 30, 45: 45, 60: 60, 90: 90}
    ref = d % 180
    ref = ref if ref <= 90 else 180 - ref
    if f == "tan":
        s = {0: "0", 30: TRIG[("tan", 30)], 45: "1", 60: "√3"}[ref]
    else:
        s = TRIG[("sin", ref)] if f == "sin" else TRIG[("cos", ref)]
    if abs(v) < 1e-9:
        return "0"
    return (MINUS if v < 0 else "") + s


def u6():
    def radyan():
        d = ch([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 20, 36, 40, 72, 100, 108])
        k = ri(0, 1)
        r = F(d, 180)
        if k == 0:
            return M("%d° kaç radyandır?" % d, pis(r), W3([pis(F(d, 360)), pis(F(180, d)) if F(180, d).denominator < 20 else pis(r * 2), pis(r * 2), pis(r + F(1, 6))], pis(r)), "%d° · π ÷ 180 = <b>%s</b> radyan." % (d, pis(r)))
        return M("%s radyan kaç derecedir?" % pis(r), "%d°" % d, W3(["%d°" % (2 * d) if 2 * d <= 720 else "%d°" % (d // 2), "%d°" % (d + 30), "%d°" % (d // 2) if d % 2 == 0 else "%d°" % (d + 60), "%d°" % abs(180 - d) if d != 180 and d != 90 else "%d°" % (d + 90)], "%d°" % d),
                 "π radyan = 180° olduğundan %s · 180° ÷ π = <b>%d°</b>." % (pis(r), d))

    def deger():
        d = ch([x for x in QUAD_ANG if x not in (0, 90, 180, 270)])
        f = ch(["sin", "cos", "tan"])
        g = tval(f, d)
        ref = d % 180 if d % 180 <= 90 else 180 - d % 180
        w = [tval(f, ref), (g[1:] if g.startswith(MINUS) else MINUS + g), tval({"sin": "cos", "cos": "sin", "tan": "sin"}[f], d), tval(f, (d + 90) % 360), tval(f, (d + 180) % 360), "1", MINUS + "1", frs(1, 2)]
        return M("%s %d° kaçtır?" % (f, d), g, W3(w, g), "%d° %d. bölgededir; %s işareti %s, referans açı %d°: <b>%s</b>." % (d, d // 90 + 1, f, "negatif" if g.startswith(MINUS) else "pozitif", ref, g))

    def bolge():
        d = ri(1, 359)
        if d % 90 == 0:
            return None
        q = d // 90 + 1
        f = ch(["sin", "cos", "tan"])
        v = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[f](math.radians(d))
        g = "Pozitif" if v > 0 else "Negatif"
        return M("%s %d° pozitif mi, negatif mi?" % (f, d), g, ["Negatif" if g == "Pozitif" else "Pozitif", "Sıfır", "Tanımsız"],
                 "%d° %d. bölgededir; bu bölgede %s <b>%s</b>." % (d, q, f, g.lower()))

    def esas():
        b = ri(1, 359)
        k = ri(1, 5)
        neg = ri(0, 1)
        d = b + 360 * k if not neg else b - 360 * k
        return M("%s° açısının esas ölçüsü kaç derecedir?" % sn(d), "%d°" % b, W3(["%d°" % (360 - b), "%d°" % ((b + 180) % 360), "%d°" % abs(d % 180), "%d°" % ((b + 90) % 360)], "%d°" % b),
                 "360°’nin katları eklenip çıkarılır: %s %s %d · 360 = <b>%d°</b>." % (sn(d), "−" if d > 0 else "+", k, b))

    def nokta():
        d = ch([x for x in QUAD_ANG if x % 90])
        g = "(%s, %s)" % (tval("cos", d), tval("sin", d))
        w = ["(%s, %s)" % (tval("sin", d), tval("cos", d)), "(%s, %s)" % (tval("cos", (d + 180) % 360), tval("sin", d)), "(%s, %s)" % (tval("cos", d), tval("sin", (d + 180) % 360)), "(%s, %s)" % (tval("cos", (360 - d) % 360), tval("sin", (d + 180) % 360))]
        return M("Birim çember üzerinde, pozitif x ekseniyle %d° açı yapan noktanın koordinatları nedir?" % d, g, W3(w, g), "Nokta (cos %d°, sin %d°) = <b>%s</b>." % (d, d, g))

    sets = [("Derece ve radyan", [(radyan, 20)]), ("Esas ölçü", [(esas, 20)]), ("Bölgelere göre işaret", [(bolge, 20)]),
            ("Özel açıların değerleri", [(deger, 20)]), ("Birim çember", [(nokta, 10), (bolge, 10)])]
    return U(11, "trigonometrik-fonksiyonlar", "N", "MAT.11.3.1", 6, "Birim Çember ve Trigonometrik Fonksiyonlar", "Trigonometrik Fonksiyonlar",
             "Birim çemberi kullanarak trigonometrik fonksiyonları tanımlar; derece ve radyan dönüşümü yapar, açıların esas ölçüsünü ve bölgelere göre işaretleri belirler.",
             "derece ve radyan, esas ölçü, bölgelere göre işaretler, özel açıların sinüs, kosinüs ve tanjant değerleri, birim çember üzerindeki noktalar",
             "Birim çemberde nokta (cos x, sin x)", "π radyan = 180°.", sets,
             ["Birim çember merkezi orijin, yarıçapı 1 olan çemberdir; x açısına karşılık gelen nokta (cos x, sin x)’tir.",
              "π radyan = 180°’dir. Bir açıya 360°’nin katları eklenip çıkarılınca esas ölçü (0° ile 360° arası) bulunur.",
              "I. bölgede hepsi, II. bölgede sinüs, III. bölgede tanjant, IV. bölgede kosinüs pozitiftir."],
             [("150°", ["II. bölge", "Referans 30°"], "sin 150° = 1/2"), ("750°", ["750 − 720"], "Esas ölçü 30°")],
             [["İşareti bölgeye göre belirlememek", "Önce bölgeyi bul"], ["Radyanda π’yi unutmak", "Derece · π ÷ 180"], ["sin ile cos’u ters yazmak", "Nokta (cos, sin)"]],
             [("Radyan nedir?", "Yarıçap uzunluğundaki yayı gören merkez açıdır."), ("tan 90° neden tanımsız?", "cos 90° = 0 olduğundan bölme yapılamaz."),
              ("Trigonometrik fonksiyonlar neden periyodiktir?", "Çember üzerinde 360° dönünce aynı noktaya gelinir.")])


# ============================================================ 7. trigonometrik fonksiyonların grafikleri
def u7():
    def fstr(a, f, b, c, d):
        inner = lin(b, "x", 0) if c == 0 else "(%s)" % lin(b, "x", c)
        s = ("" if a == 1 else MINUS if a == -1 else sn(a)) + "%s %s" % (f, inner) if inner.startswith("(") else ("" if a == 1 else MINUS if a == -1 else sn(a)) + "%s %s" % (f, inner)
        s = s.replace("%s (" % f, "%s(" % f) if False else s
        if d:
            s += (" + %s" % sn(d)) if d > 0 else (" − %s" % sn(-d))
        return s

    def periyot():
        a, b, d = nz(-5, 5), ri(1, 8), ri(-6, 6)
        f = ch(["sin", "cos", "tan"])
        T = F(2, b) if f != "tan" else F(1, b)
        g = pis(T)
        return M("f(x) = %s fonksiyonunun esas periyodu kaçtır?" % fstr(a, f, b, 0, d), g, W3([pis(T * 2), pis(T / 2), pis(F(2 * b)), pis(F(b, 2)) if b != 2 else pis(4)], g),
                 "%s için periyot %s ÷ |b| = %s ÷ %d = <b>%s</b>." % (f, "π" if f == "tan" else "2π", "π" if f == "tan" else "2π", b, g))

    def maxmin():
        a, b, d = nz(-6, 6), ri(1, 5), ri(-8, 8)
        f = ch(["sin", "cos"])
        k = ch(["en büyük", "en küçük"])
        v = abs(a) + d if k == "en büyük" else -abs(a) + d
        return M("f(x) = %s fonksiyonunun %s değeri kaçtır?" % (fstr(a, f, b, 0, d), k), sn(v), W3([sn(a + d) if a + d != v else sn(-a + d), sn(abs(a)), sn(d), sn(-v) if v else "1", sn(v + b)], sn(v)),
                 "%s değeri −1 ile 1 arasında olduğundan f(x), %s ile %s arasındadır: <b>%s</b>." % (f, sn(d - abs(a)), sn(d + abs(a)), sn(v)))

    def goruntu():
        a, b, d = nz(-6, 6), ri(1, 5), ri(-8, 8)
        f = ch(["sin", "cos"])
        g = "[%s, %s]" % (sn(d - abs(a)), sn(d + abs(a)))
        return M("f(x) = %s fonksiyonunun görüntü kümesi hangisidir?" % fstr(a, f, b, 0, d), g, W3(["[%s, %s]" % (sn(-abs(a)), sn(abs(a))), "[%s, %s]" % (sn(d - 1), sn(d + 1)), "[%s, %s]" % (sn(d - abs(a) * b), sn(d + abs(a) * b)), "(%s, %s)" % (sn(d - abs(a)), sn(d + abs(a)))], g),
                 "−1 ≤ %s ≤ 1 olduğundan <b>%s</b>." % (f, g))

    def deger():
        a, d = nz(-4, 4), ri(-5, 5)
        f = ch(["sin", "cos"])
        x = ch([30, 60, 90, 150, 180, 210, 270, 330, 0, 120, 240, 300])
        val = math.sin(math.radians(x)) if f == "sin" else math.cos(math.radians(x))
        fv = F(round(val * 2), 2)
        if abs(float(fv) - val) > 1e-9:
            return None
        v = a * fv + d
        return M("f(x) = %s için f(%s) kaçtır?" % (fstr(a, f, 1, 0, d), pis(F(x, 180))), sn(v), W3([sn(a * (-fv) + d), sn(a + d), sn(d), sn(a * fv), sn(v + 1)], sn(v)),
                 "%s(%s) = %s → %s · %s %s %s = <b>%s</b>." % (f, pis(F(x, 180)), sn(fv), sn(a), par(fv) if fv < 0 else sn(fv), "+" if d >= 0 else "−", sn(abs(d)), sn(v)))

    def grafik():
        a, d = ch([1, 2, 3, -1, -2]), ri(-2, 2)
        b = 1
        f = ch(["sin", "cos"])
        if abs(a) + abs(d) > 4:
            return None
        fn = (lambda x: a * math.sin(x) + d) if f == "sin" else (lambda x: a * math.cos(x) + d)
        p = kurve([(fn, "#c0392b", "")], (0, 7, 1), (-5, 5, 1), label="trigonometrik fonksiyon grafiği")
        g = "y = " + fstr(a, f, b, 0, d)
        o = "cos" if f == "sin" else "sin"
        w = ["y = " + fstr(-a, f, b, 0, d), "y = " + fstr(a, o, b, 0, d), "y = " + fstr(a, f, b, 0, -d) if d else "y = " + fstr(a, f, b, 0, 1), "y = " + fstr(a + (1 if a > 0 else -1), f, b, 0, d)]
        return M("Grafiği verilen fonksiyon hangisidir? (x ekseni radyan; 0 ≤ x ≤ 7)%s" % p, g, W3(w, g),
                 "Grafik x = 0’da %s değerini alıyor; en büyük %s, en küçük %s: <b>%s</b>." % (sn(d if f == "sin" else a + d), sn(abs(a) + d), sn(d - abs(a)), g))

    sets = [("Değer bulma", [(deger, 20)]), ("En büyük ve en küçük değer", [(maxmin, 20)]), ("Görüntü kümesi", [(goruntu, 20)]),
            ("Periyot", [(periyot, 20)]), ("Grafikten fonksiyon", [(grafik, 20)])]
    return U(11, "trigonometrik-fonksiyonlarin-grafikleri", "N", "MAT.11.3.1", 7, "Trigonometrik Fonksiyonların Grafikleri", "Trigonometrik Grafikler",
             "g(x) = k · f(mx ± r) ± s biçimindeki trigonometrik fonksiyonların grafiklerini çizer; periyot, en büyük ve en küçük değer ile görüntü kümesini yorumlar.",
             "trigonometrik fonksiyonun değeri, en büyük ve en küçük değer, görüntü kümesi, esas periyot, grafikten fonksiyonu bulma",
             "a·sin(bx) + d: periyot 2π ÷ |b|", "Değerler d − |a| ile d + |a| arasındadır.", sets,
             ["sin x ve cos x, −1 ile 1 arasında değer alır; periyotları 2π’dir. tan x’in periyodu π’dir.",
              "f(x) = a · sin(bx) + d için görüntü kümesi [d − |a|, d + |a|], esas periyot 2π ÷ |b|’dir.",
              "a grafiği dikey yönde uzatır, d yukarı-aşağı öteler, b grafiği yatay yönde sıkıştırır."],
             [("3 sin 2x + 1", ["−3 ≤ 3 sin 2x ≤ 3"], "[−2, 4], periyot π"), ("2 cos x, x = π", ["cos π = −1"], "−2")],
             [["Periyotta 2π ÷ b yerine 2π · b almak", "b büyüdükçe periyot küçülür"], ["a negatifken en büyük değeri d + a sanmak", "|a| kullanılır"],
              ["tan için 2π almak", "tan’ın periyodu π"]],
             [("Periyot ne demek?", "Grafiğin kendini tekrar ettiği en küçük aralıktır."), ("Gerçek hayatta?", "Ses dalgaları, gelgitler ve alternatif akım sinüs biçimindedir."),
              ("Genlik nedir?", "|a| değeridir; tepe ile orta çizgi arasındaki uzaklıktır.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7]
