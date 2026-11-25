# -*- coding: utf-8 -*-
"""Türkiye 8. sınıf: Geometrik Şekiller (13〜17)、Geometrik Nicelikler (18〜19)、Dönüşüm (20〜21)、İstatistik (22)、Olasılık (23)。"""
import math
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, num, fr, M, NB
from tr_g7 import sn, par, dq, ondalik, MINUS, gen
from id_smp import kosy as _kosy, figure as _figure


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def nz(a, b):
    while True:
        x = ri(a, b)
        if x:
            return x


def kosy(lines=(), pts=(), lo=-6, hi=6, label="koordinat düzlemi"):
    return _kosy(lines=lines, pts=pts, lo=lo, hi=hi, label=label)


def figure(pts, segs, sides=(), right=(), label="geometrik şekil", ticks=()):
    return _figure(pts, segs, sides=sides, right=right, label=label, ticks=ticks)


def tri_by_sides(a, b, c):
    """kenarları a = |BC|, b = |AC|, c = |AB| olan üçgenin köşeleri (B orijinde)"""
    x = (c * c + a * a - b * b) / (2.0 * a)
    y = math.sqrt(max(c * c - x * x, 0.01))
    return {"B": (0, 0), "C": (a, 0), "A": (x, y)}


# ============================================================ 13. açı-kenar ilişkisi
def u13():
    def buyuk_aci():
        while True:
            a, b, c = ri(3, 15), ri(3, 15), ri(3, 15)
            if a + b > c and a + c > b and b + c > a and len({a, b, c}) == 3:
                break
        sides = {"BC": a, "AC": b, "AB": c}
        opp = {"BC": "A", "AC": "B", "AB": "C"}
        k = ch(["en büyük", "en küçük"])
        e = max(sides, key=sides.get) if k == "en büyük" else min(sides, key=sides.get)
        g = "%s açısı" % opp[e]
        return M("ABC üçgeninde |BC| = %d cm, |AC| = %d cm, |AB| = %d cm’dir. Hangi açının ölçüsü %stür?" % (a, b, c, k), g, ["%s açısı" % v for v in "ABC" if v != opp[e]] + ["Hepsi eşittir"],
                 "Üçgende %s kenarın karşısında %s açı bulunur. %s kenar [%s] → <b>%s</b>." % (k, k, cap(k), e, g))

    def buyuk_kenar():
        while True:
            A_, B_ = ri(20, 120), ri(20, 120)
            C_ = 180 - A_ - B_
            if C_ > 5 and len({A_, B_, C_}) == 3:
                break
        ang = {"A": A_, "B": B_, "C": C_}
        opp = {"A": "[BC]", "B": "[AC]", "C": "[AB]"}
        k = ch(["en uzun", "en kısa"])
        v = max(ang, key=ang.get) if k == "en uzun" else min(ang, key=ang.get)
        return M("ABC üçgeninde m(A) = %d°, m(B) = %d°’dir. Hangi kenar %s?" % (A_, B_, {"en uzun": "en uzundur", "en kısa": "en kısadır"}[k]), opp[v], [x for x in ("[AB]", "[AC]", "[BC]") if x != opp[v]] + ["Kenarlar eşittir"],
                 "m(C) = 180 − %d − %d = %d°. %s açının karşısındaki kenar %s: <b>%s</b>." % (A_, B_, C_, "En büyük" if k == "en uzun" else "En küçük", {"en uzun": "en uzundur", "en kısa": "en kısadır"}[k], opp[v]))

    def sirala():
        while True:
            A_, B_ = ri(25, 110), ri(25, 110)
            C_ = 180 - A_ - B_
            if C_ > 10 and len({A_, B_, C_}) == 3:
                break
        ang = {"a": A_, "b": B_, "c": C_}
        g = " &lt; ".join(sorted(ang, key=ang.get))
        w = [" &lt; ".join(p) for p in (("a", "b", "c"), ("c", "b", "a"), ("b", "a", "c"), ("a", "c", "b"), ("c", "a", "b"), ("b", "c", "a")) if " &lt; ".join(p) != g][:3]
        return M("ABC üçgeninde m(A) = %d°, m(B) = %d°’dir. a = |BC|, b = |AC|, c = |AB| olmak üzere kenarların sıralaması hangisidir?" % (A_, B_), g, w,
                 "m(C) = %d°. Açılar küçükten büyüğe sıralanınca karşılarındaki kenarlar da aynı sırada olur: <b>%s</b>." % (C_, g))

    def ikizkenar():
        t = ri(20, 80) * 2
        b = (180 - t) // 2
        return M("İkizkenar bir üçgende tepe açısı %d°’dir. Taban açılarından biri kaç derecedir?" % t, "%d°" % b, ["%d°" % t, "%d°" % (180 - t), "%d°" % (90 - b if 90 - b != b else b + 10)],
                 "Eşit kenarların karşısındaki açılar eşittir: (180 − %d) ÷ 2 = <b>%d°</b>." % (t, b))

    def dogru_mu():
        S = [("Bir üçgende en uzun kenarın karşısındaki açı en büyük açıdır.", "Doğru"), ("Eşkenar üçgenin bütün açıları 60°’dir.", "Doğru"),
             ("Bir üçgende eşit kenarların karşısındaki açılar farklıdır.", "Yanlış"), ("Dik üçgende en uzun kenar hipotenüstür.", "Doğru"),
             ("Geniş açılı bir üçgende en uzun kenar geniş açının karşısındadır.", "Doğru"), ("Bir üçgende en küçük açının karşısında en uzun kenar bulunur.", "Yanlış")]
        t, g = ch(S)
        return M("“%s” ifadesi doğru mu, yanlış mı?" % t, g, ["Yanlış" if g == "Doğru" else "Doğru", "Bazen doğru", "Bilinemez"],
                 "Üçgende büyük açının karşısında büyük kenar, eşit açıların karşısında eşit kenarlar bulunur. Cevap: <b>%s</b>." % g)

    sets = [("Kenarlardan açılara", [(buyuk_aci, 20)]),
            ("Açılardan kenarlara", [(buyuk_kenar, 20)]),
            ("Sıralama", [(sirala, 20)]),
            ("İkizkenar üçgen", [(ikizkenar, 16), (dogru_mu, 4)]),
            ("Karışık", [(buyuk_aci, 7), (buyuk_kenar, 7), (sirala, 6)])]
    return unit("ucgende-aci-kenar-iliskisi", "GS", "MAT.8.3.1", 13, "Üçgende Açı-Kenar İlişkisi", "Açı-Kenar İlişkisi",
                "Araç ve teknoloji yardımıyla üçgenin kenarları ile açıları arasındaki ilişkiyi yorumlar; kenar uzunluklarına göre açıları, açı ölçülerine göre kenarları sıralar.",
                "8. sınıf üçgende açı-kenar ilişkisi çalışma kâğıdı: en uzun kenarın karşısındaki en büyük açı, açılardan kenar sıralaması, ikizkenar üçgende taban açıları. 100 soru ve cevap anahtarı.",
                "Büyük açı karşısında büyük kenar", "Eşit kenarların karşısındaki açılar da eşittir.", sets,
                ["Bir üçgende en uzun kenarın karşısında en büyük açı, en kısa kenarın karşısında en küçük açı bulunur.",
                 "Açıları sıralayınca karşılarındaki kenarlar da aynı sırayla sıralanır: m(A) &lt; m(B) &lt; m(C) ise a &lt; b &lt; c.",
                 "İkizkenar üçgende eşit kenarların karşısındaki taban açıları eşittir."],
                [("m(A) = 70°, m(B) = 45°", ["m(C) = 65°", "45 &lt; 65 &lt; 70"], "b &lt; c &lt; a"), ("Tepe açısı 40° olan ikizkenar üçgen", ["(180 − 40) ÷ 2"], "70°")],
                [["Açının yanındaki kenarı karşısındaki sanmak", "A açısının karşısı [BC]’dir"],
                 ["Üçüncü açıyı hesaplamadan sıralamak", "Önce 180’den çıkar"],
                 ["Taban açısını tepe açısıyla karıştırmak", "Tepe açısı eşit kenarların arasındadır"]],
                [("Bu ilişki her üçgende geçerli mi?", "Evet, dar, dik ve geniş açılı bütün üçgenlerde geçerlidir."),
                 ("Dik üçgende en uzun kenar neden hipotenüstür?", "Çünkü en büyük açı 90°’dir ve hipotenüs onun karşısındadır."),
                 ("Açıölçer olmadan kenar sıralanabilir mi?", "Evet, açı ölçüleri biliniyorsa karşılarındaki kenarlar aynı sırayla sıralanır.")])


def cap(s):
    return G.cap(s)


# ============================================================ 14. üçgen eşitsizliği
def u14():
    def olusur_mu():
        a, b = ri(2, 15), ri(2, 15)
        c = ch([a + b, abs(a - b), ri(abs(a - b) + 1, a + b - 1), a + b + ri(1, 4)])
        if c <= 0:
            return None
        ok = abs(a - b) < c < a + b
        g = "Oluşturur" if ok else "Oluşturmaz"
        return M("Uzunlukları %d cm, %d cm ve %d cm olan doğru parçalarıyla bir üçgen oluşturulabilir mi?" % (a, b, c), g, ["Oluşturmaz" if ok else "Oluşturur", "Yalnızca dik üçgen oluşur", "Yalnızca eşkenar üçgen oluşur"],
                 "Üçgen için her kenar diğer ikisinin farkından büyük, toplamından küçük olmalı: |%d − %d| = %d, %d + %d = %d. %s" % (a, b, abs(a - b), a, b, a + b, "<b>Oluşturur</b>." if ok else "%d bu aralıkta değil: <b>oluşturmaz</b>." % c))

    def aralik():
        a, b = ri(2, 20), ri(2, 20)
        if a == b:
            return None
        lo, hi = abs(a - b), a + b
        g = "%d &lt; x &lt; %d" % (lo, hi)
        return M("Bir üçgenin iki kenarı %d cm ve %d cm’dir. Üçüncü kenar x için hangisi doğrudur?" % (a, b), g, ["%d ≤ x ≤ %d" % (lo, hi), "%d &lt; x &lt; %d" % (0, hi), "%d &lt; x &lt; %d" % (lo, max(a, b))],
                 "|%d − %d| &lt; x &lt; %d + %d → <b>%s</b>." % (a, b, a, b, g))

    def kac():
        a, b = ri(2, 15), ri(2, 15)
        lo, hi = abs(a - b), a + b
        n = hi - lo - 1
        return M("Bir üçgenin iki kenarı %d cm ve %d cm’dir. Üçüncü kenarın uzunluğu tam sayı ise kaç farklı değer alabilir?" % (a, b), num(n), [num(n + 2), num(n + 1), num(hi - lo + 1) if hi - lo + 1 != n + 2 else num(n - 1)],
                 "%d &lt; x &lt; %d; tam sayılar %d, %d, …, %d: <b>%d</b> değer." % (lo, hi, lo + 1, lo + 2, hi - 1, n))

    def en():
        a, b = ri(3, 18), ri(3, 18)
        lo, hi = abs(a - b), a + b
        k = ch(["en büyük", "en küçük"])
        v = hi - 1 if k == "en büyük" else lo + 1
        return M("Bir üçgenin iki kenarı %d cm ve %d cm’dir. Üçüncü kenarın tam sayı olarak alabileceği %s değer kaçtır?" % (a, b, k), num(v), [num(hi) if k == "en büyük" else num(lo), num(v + 2) if k == "en büyük" else num(max(v - 2, 0) if v - 2 != lo else v + 3), num(max(a, b))] if num(max(a, b)) != num(v) else [num(hi) if k == "en büyük" else num(lo), num(v + 2), num(v - 3)],
                 "%d &lt; x &lt; %d olduğundan %s tam sayı <b>%d</b>." % (lo, hi, k, v))

    def hangisi():
        a, b = ri(3, 15), ri(3, 15)
        lo, hi = abs(a - b), a + b
        good = ri(lo + 1, hi - 1)
        bad = sh([lo, hi, hi + 1, hi + 2, lo - 1 if lo > 1 else hi + 3])[:3]
        return G.withopts(M("Kenarları %d cm ve %d cm olan bir üçgenin üçüncü kenarı hangisi olabilir?" % (a, b), "%d cm" % good, ["%d cm" % x for x in bad],
                            "%d &lt; x &lt; %d: <b>%d cm</b>." % (lo, hi, good)), "%s uzunlukları veriliyor.")

    sets = [("Üçgen oluşur mu?", [(olusur_mu, 20)]),
            ("Üçüncü kenarın aralığı", [(aralik, 20)]),
            ("Kaç farklı değer?", [(kac, 20)]),
            ("En büyük ve en küçük", [(en, 12), (hangisi, 8)]),
            ("Karışık", [(olusur_mu, 7), (kac, 7), (hangisi, 6)])]
    return unit("ucgen-esitsizligi", "GS", "MAT.8.3.2", 14, "Üçgen Eşitsizliği", "Üçgen Eşitsizliği",
                "Üçgenin kenar uzunlukları arasındaki ilişkiye dair çıkarım yapar; üçgen oluşturabilen doğru parçalarının uzunluklarını inceler ve kenarlar arasındaki ilişkiye dair önerme sunar.",
                "8. sınıf üçgen eşitsizliği çalışma kâğıdı: verilen uzunluklarla üçgen oluşup oluşmayacağı, üçüncü kenarın aralığı, tam sayı değerlerin sayısı, en büyük ve en küçük değer. 100 soru ve cevap anahtarı.",
                "|a − b| < c < a + b", "Her kenar diğer ikisinin farkından büyük, toplamından küçük.", sets,
                ["Bir üçgende herhangi iki kenarın uzunlukları toplamı üçüncü kenardan büyüktür.",
                 "Herhangi iki kenarın uzunlukları farkı üçüncü kenardan küçüktür. Kısaca: |a − b| &lt; c &lt; a + b.",
                 "Toplam üçüncü kenara eşitse doğru parçaları üst üste düşer; üçgen oluşmaz."],
                [("5, 8 ve 14 cm", ["5 + 8 = 13 &lt; 14"], "Üçgen oluşmaz"), ("Kenarlar 7 ve 4, üçüncü kenar tam sayı", ["3 &lt; x &lt; 11", "4, 5, …, 10"], "7 değer")],
                [["Eşitlik durumunu kabul etmek", "3, 4, 7: 3 + 4 = 7, üçgen oluşmaz"],
                 ["Yalnızca toplamı kontrol etmek", "Fark koşulu da gerekir"],
                 ["Uç değerleri saymak", "Aralık açıktır: uçlar dâhil değil"]],
                [("Üçgen eşitsizliği neden doğrudur?", "İki nokta arasındaki en kısa yol doğru parçasıdır; üçüncü köşeden dolaşmak her zaman daha uzundur."),
                 ("Üç kenarı da kontrol etmek gerekir mi?", "En uzun kenarın diğer ikisinin toplamından küçük olduğunu kontrol etmek yeterlidir."),
                 ("Günlük hayatta nerede karşımıza çıkar?", "İki şehir arasındaki doğrudan yolun, üçüncü bir şehirden geçen yoldan kısa olmasında.")])


# ============================================================ 15. eşlik
def u15():
    def kural():
        S = [("İki kenar uzunluğu ve bu kenarlar arasındaki açının ölçüsü eşit", "Kenar-Açı-Kenar (KAK)"),
             ("Üç kenar uzunluğu eşit", "Kenar-Kenar-Kenar (KKK)"),
             ("İki açısının ölçüsü ve bu açılar arasındaki kenarın uzunluğu eşit", "Açı-Kenar-Açı (AKA)")]
        t, g = ch(S)
        w = [x for _, x in S if x != g] + ["Açı-Açı-Açı (AAA)"]
        return M("İki üçgenin %s ise üçgenler hangi eşlik koşuluna göre eştir?" % t.lower() if False else "İki üçgende %s ise üçgenler hangi eşlik koşuluna göre eştir?" % t.lower(), g, w,
                 "Eş üçgen oluşturmak için %s yeterlidir: <b>%s</b>." % (t.lower(), g))

    def aaa():
        S = [("Üç açısının ölçüsü eşit olan iki üçgen her zaman eştir.", "Yanlış"), ("Üç kenarı eşit olan iki üçgen eştir.", "Doğru"),
             ("İki kenarı ve aralarındaki açısı eşit olan iki üçgen eştir.", "Doğru"), ("Eş üçgenlerin karşılıklı açıları eşittir.", "Doğru"),
             ("Eş üçgenlerin alanları farklı olabilir.", "Yanlış"), ("Bir kenarı eşit olan iki üçgen eştir.", "Yanlış")]
        t, g = ch(S)
        return M("“%s” ifadesi doğru mu, yanlış mı?" % t, g, ["Yanlış" if g == "Doğru" else "Doğru", "Bazen doğru", "Bilinemez"],
                 "Eş üçgenlerin bütün karşılıklı kenarları ve açıları eşittir; AAA eşlik için yeterli değildir (benzerlik verir). Cevap: <b>%s</b>." % g)

    def eleman():
        a, b, c = ri(3, 15), ri(3, 15), ri(3, 15)
        if not (a + b > c and a + c > b and b + c > a):
            return None
        A_ = ri(30, 100)
        B_ = ri(20, 150 - A_)
        C_ = 180 - A_ - B_
        k = ch(["kenar", "açı"])
        if k == "kenar":
            return M("ABC ≅ DEF olduğu biliniyor. |AB| = %d cm, |BC| = %d cm, |AC| = %d cm ise |EF| kaç cm’dir?" % (c, a, b), "%d cm" % a, ["%d cm" % c, "%d cm" % b, "%d cm" % (a + 1)],
                     "Eşlikte köşeler sırasıyla eşleşir: A↔D, B↔E, C↔F. [EF], [BC]’ye karşılık gelir: <b>%d cm</b>." % a)
        return M("ABC ≅ DEF olduğu biliniyor. m(A) = %d°, m(B) = %d° ise m(F) kaç derecedir?" % (A_, B_), "%d°" % C_, ["%d°" % A_, "%d°" % B_, "%d°" % (C_ + 10)],
                 "F, C’ye karşılık gelir: m(C) = 180 − %d − %d = <b>%d°</b>." % (A_, B_, C_))

    def bulmaca():
        x = ri(2, 12)
        a, b = ri(2, 5), ri(1, 15)
        m = a * x + b
        k = ri(1, a - 1) if a > 1 else 0
        c = m - k * x
        return M("ABC ≅ DEF üçgenlerinde |AB| = (%s) cm ve |DE| = (%s) cm ise x kaçtır?" % ("%dx + %d" % (a, b), ("%dx + %d" % (k, c)) if k > 1 else ("x + %d" % c if k == 1 else "%d" % c)), num(x),
                 [num(x + 1), num(m), num(x * 2)], "Eş üçgenlerin karşılık gelen kenarları eşittir: %dx + %d = %s → x = <b>%d</b>." % (a, b, ("%dx + %d" % (k, c)) if k > 1 else ("x + %d" % c if k == 1 else "%d" % c), x))

    def yeterli():
        S = [("|AB| = |DE|, |BC| = |EF|, m(B) = m(E)", "Evet, KAK"), ("|AB| = |DE|, |BC| = |EF|, |AC| = |DF|", "Evet, KKK"),
             ("m(A) = m(D), |AB| = |DE|, m(B) = m(E)", "Evet, AKA"), ("m(A) = m(D), m(B) = m(E), m(C) = m(F)", "Hayır, yalnızca açılar eşit"),
             ("|AB| = |DE|, |BC| = |EF|", "Hayır, iki kenar yetmez")]
        t, g = ch(S)
        w = [x for _, x in S if x != g][:3]
        return M("ABC ve DEF üçgenlerinde %s olduğu biliniyor. Üçgenlerin eş olduğu söylenebilir mi?" % t, g, w, "Eşlik için KKK, KAK ya da AKA koşullarından biri gerekir. Cevap: <b>%s</b>." % g)

    sets = [("Eşlik koşulları", [(kural, 3), (yeterli, 5), (eleman, 12)]),
            ("Karşılık gelen elemanlar", [(eleman, 20)]),
            ("Eş kenarlarla denklem", [(bulmaca, 20)]),
            ("Eşlik bilgisi ve denklemler", [(aaa, 6), (bulmaca, 14)]),
            ("Karışık", [(eleman, 10), (bulmaca, 10)])]
    return unit("eslik", "GS", "MAT.8.3.3", 15, "Üçgenlerde Eşlik", "Eşlik",
                "Bir üçgene eş üçgen oluşturmak için yeterli elemanlar hakkında çıkarım yapar; KKK, KAK ve AKA eşlik koşullarına dair önerme sunar ve karşılık gelen elemanları belirler.",
                "8. sınıf üçgenlerde eşlik çalışma kâğıdı: KKK, KAK ve AKA eşlik koşulları, eş üçgenlerde karşılık gelen kenar ve açılar, eş kenarlarla denklem kurma. 100 soru ve cevap anahtarı.",
                "Eş üçgen: bütün kenar ve açılar eşit", "Yeterli koşullar: KKK, KAK, AKA.", sets,
                ["Bütün karşılıklı kenarları ve açıları eşit olan üçgenlere eş üçgenler denir ve ABC ≅ DEF biçiminde yazılır. Köşeler sırasıyla eşleşir: A↔D, B↔E, C↔F.",
                 "Eşlik için üç koşuldan biri yeterlidir: üç kenar (KKK), iki kenar ve aradaki açı (KAK), iki açı ve aradaki kenar (AKA).",
                 "Üç açının eşit olması (AAA) eşlik için yeterli değildir; üçgenler farklı büyüklükte olabilir."],
                [("ABC ≅ DEF, |BC| = 9 cm", ["B↔E, C↔F"], "|EF| = 9 cm"), ("|AB| = |DE|, m(B) = m(E), |BC| = |EF|", ["Aradaki açı eşit"], "KAK ile eş")],
                [["Köşeleri sırasız eşleştirmek", "ABC ≅ DEF’te A↔D, B↔E, C↔F"],
                 ["Açının kenarların arasında olmadığı durumu KAK sanmak", "Açı iki kenarın arasında olmalı"],
                 ["AAA ile eşlik var sanmak", "AAA benzerlik verir, eşlik vermez"]],
                [("Eşlik ile benzerlik farkı nedir?", "Eş üçgenler aynı biçim ve aynı büyüklüktedir; benzer üçgenler aynı biçimde ama farklı büyüklükte olabilir."),
                 ("Eşlik nerede kullanılır?", "Köprü ve çatı makaslarında, aynı parçaların üretiminde."),
                 ("≅ işareti ne demek?", "‘Eştir’ demektir.")])


# ============================================================ 16. benzerlik
def u16():
    def oran():
        a, b, c = ri(2, 9), ri(2, 9), ri(2, 9)
        k = F(ri(2, 5), ch([1, 1, 2]))
        if k == 1:
            return None
        A, B = a * k, b * k
        if A.denominator > 1 or B.denominator > 1:
            return None
        return M("ABC ∼ DEF üçgenlerinde |AB| = %d cm, |BC| = %d cm ve |DE| = %s cm’dir. |EF| kaç cm’dir?" % (a, b, sn(A)), "%s cm" % sn(B), ["%s cm" % sn(b + A - a), "%s cm" % sn(F(b) / k), "%s cm" % sn(A)],
                 "Benzerlik oranı %s ÷ %d = %s; |EF| = %d · %s = <b>%s cm</b>." % (sn(A), a, sn(k), b, sn(k), sn(B)))

    def benzer_mi():
        a, b, c = ri(2, 9), ri(2, 9), ri(2, 9)
        if not (a + b > c and a + c > b and b + c > a):
            return None
        k = ri(2, 4)
        good = ri(0, 1)
        d, e, f = a * k, b * k, c * k + (0 if good else ch([1, -1]))
        g = "Evet, benzerdir" if good else "Hayır, benzer değildir"
        return M("Kenarları %d, %d, %d cm olan üçgen ile kenarları %d, %d, %d cm olan üçgen benzer midir?" % (a, b, c, d, e, f), g, ["Hayır, benzer değildir" if good else "Evet, benzerdir", "Eştir", "Bilinemez"],
                 "Karşılıklı kenarların oranları: %d/%d, %d/%d, %d/%d. %s" % (d, a, e, b, f, c, "Hepsi %d: <b>benzerdir</b>." % k if good else "Oranlar eşit değil: <b>benzer değildir</b>."))

    def aci():
        A_, B_ = ri(30, 90), ri(20, 70)
        C_ = 180 - A_ - B_
        return M("ABC ∼ DEF ve m(A) = %d°, m(E) = %d° ise m(F) kaç derecedir?" % (A_, B_), "%d°" % C_, ["%d°" % A_, "%d°" % B_, "%d°" % (180 - A_)],
                 "Benzer üçgenlerin karşılık gelen açıları eşittir: m(D) = %d°, m(E) = %d°, m(F) = 180 − %d − %d = <b>%d°</b>." % (A_, B_, A_, B_, C_))

    def golge():
        h = ri(12, 40) * 10
        s = ri(5, 30) * 10
        p = ri(150, 190)
        ps = F(p * s, h)
        if ps.denominator != 1:
            return None
        nm = G.K.next()
        return M("Boyu %d cm olan bir ağacın gölgesi %d cm iken boyu %d cm olan %s’in gölgesi aynı anda kaç cm’dir?" % (h, s, p, nm) if False else
                 "Aynı anda, boyu %d cm olan bir direğin gölgesi %d cm, boyu %d cm olan bir öğrencinin gölgesi kaç cm’dir?" % (h, s, p), "%s cm" % sn(ps),
                 ["%s cm" % num(p - (h - s)) if p - (h - s) > 0 else "%s cm" % num(p), "%s cm" % sn(F(h * p, s)) if (h * p) % s == 0 else "%s cm" % num(s), "%s cm" % num(int(ps) + 10)],
                 "Güneş ışınları aynı açıyla geldiği için üçgenler benzerdir: %d/%d = %d/x → x = <b>%s cm</b>." % (h, s, p, sn(ps)))

    def oran_bul():
        a = ri(3, 12)
        k = ri(2, 5)
        return M("Benzer iki üçgenin karşılık gelen kenarları %d cm ve %d cm’dir. Benzerlik oranı kaçtır? (Küçükten büyüğe)" % (a, a * k), "1/%d" % k if False else sn(F(1, k)),
                 [sn(F(k)), sn(F(a, a * k + 1)), sn(F(1, k + 1))], "%d ÷ %d = <b>%s</b>." % (a, a * k, sn(F(1, k))))

    sets = [("Benzer üçgenlerde kenar", [(oran, 20)]),
            ("Benzer mi?", [(benzer_mi, 20)]),
            ("Karşılık gelen açılar", [(aci, 12), (oran_bul, 8)]),
            ("Gölge problemleri", [(golge, 20)]),
            ("Karışık", [(oran, 7), (benzer_mi, 7), (golge, 6)])]
    return unit("benzerlik", "GS", "MAT.8.3.4", 16, "Üçgenlerde Benzerlik", "Benzerlik",
                "Bir üçgene benzer üçgen oluşturmak için yeterli elemanlar hakkında çıkarım yapar; benzer üçgenlerde karşılık gelen kenarların oranını (benzerlik oranı) ve açıların eşitliğini kullanır.",
                "8. sınıf üçgenlerde benzerlik çalışma kâğıdı: benzerlik oranı, benzer üçgenlerde eksik kenar, kenar oranlarına göre benzerlik, karşılık gelen açılar, gölge problemleri. 100 soru ve cevap anahtarı.",
                "Benzer: açılar eşit, kenarlar orantılı", "Karşılık gelen kenarların oranı benzerlik oranıdır.", sets,
                ["Karşılık gelen açıları eşit ve karşılık gelen kenarları orantılı olan üçgenler benzerdir: ABC ∼ DEF.",
                 "Karşılık gelen kenarların oranına benzerlik oranı denir: |DE|/|AB| = |EF|/|BC| = |DF|/|AC| = k.",
                 "İki açısı eşit olan üçgenler benzerdir. Aynı anda oluşan gölgeler benzer üçgenler oluşturur."],
                [("ABC ∼ DEF, |AB| = 4, |DE| = 10, |BC| = 6", ["k = 10/4 = 5/2", "|EF| = 6 · 5/2"], "15 cm"),
                 ("3 m’lik direk 2 m gölge, 1,5 m’lik çocuk", ["3/2 = 1,5/x"], "1 m")],
                [["Kenarları sırasız eşleştirmek", "Köşe sırasına göre: A↔D, B↔E"],
                 ["Benzerlikte kenar farklarını eşit sanmak", "Oranlar eşit olmalı, farklar değil"],
                 ["Benzerliği eşlik sanmak", "k = 1 ise eş olur"]],
                [("Eş üçgenler benzer midir?", "Evet, benzerlik oranı 1 olan benzer üçgenlerdir."),
                 ("Benzerlik nerede kullanılır?", "Harita, maket, fotoğraf büyütme ve yüksekliği ulaşılamayan nesneleri ölçmede."),
                 ("∼ işareti ne demek?", "‘Benzerdir’ demektir.")])


# ============================================================ 17. Pisagor
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]


def u17():
    def hip():
        a, b, c = ch(TRIP)
        k = ri(1, 6)
        a, b, c = a * k, b * k, c * k
        pts = {"A": (0, b), "B": (0, 0), "C": (a, 0)}
        fig = figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("B", "C", "%d cm" % a), ("A", "B", "%d cm" % b), ("A", "C", "x")], right=[("B", "A", "C")], label="dik üçgen")
        return M("Şekildeki dik üçgende x kaç cm’dir?" + fig, "%d cm" % c, ["%d cm" % (a + b), "%d cm" % (c + 1), "%d cm" % (b + 1 if b + 1 != c else b + 2)],
                 "x² = %d² + %d² = %d + %d = %d → x = <b>%d cm</b>." % (a, b, a * a, b * b, c * c, c))

    def dik_kenar():
        a, b, c = ch(TRIP)
        k = ri(1, 6)
        a, b, c = a * k, b * k, c * k
        return M("Hipotenüsü %d cm, bir dik kenarı %d cm olan dik üçgenin diğer dik kenarı kaç cm’dir?" % (c, a), "%d cm" % b, ["%d cm" % (c - a), "%d cm" % (c + a), "%d cm" % (b + k)],
                 "b² = %d² − %d² = %d − %d = %d → b = <b>%d cm</b>." % (c, a, c * c, a * a, b * b, b))

    def dik_mi():
        a, b, c = ch(TRIP)
        k = ri(1, 3)
        good = ri(0, 1)
        x, y, z = a * k, b * k, c * k + (0 if good else ch([1, -1]))
        sq = x * x + y * y
        g = "Dik üçgendir" if sq == z * z else ("Geniş açılı üçgendir" if z * z > sq else "Dar açılı üçgendir")
        return M("Kenarları %d cm, %d cm ve %d cm olan üçgen nasıl bir üçgendir?" % (x, y, z), g, [v for v in ("Dik üçgendir", "Geniş açılı üçgendir", "Dar açılı üçgendir", "Üçgen oluşmaz") if v != g],
                 "%d² + %d² = %d, %d² = %d. %s" % (x, y, sq, z, z * z, "Eşit: <b>dik üçgen</b>." if sq == z * z else ("En uzun kenarın karesi büyük: <b>geniş açılı</b>." if z * z > sq else "En uzun kenarın karesi küçük: <b>dar açılı</b>.")))

    def merdiven():
        a, b, c = ch(TRIP[:5])
        k = ch([1, 2, 3])
        a, b, c = a * k, b * k, c * k
        if ri(0, 1):
            return M("Uzunluğu %d m olan bir merdiven duvara dayanmıştır. Merdivenin üst ucu yerden %d m yüksektedir. Alt ucu duvardan kaç m uzaktadır?" % (c, b), "%d m" % a,
                     ["%d m" % (c - b), "%d m" % (c + b), "%d m" % (a + 1)], "√(%d² − %d²) = √%d = <b>%d m</b>." % (c, b, a * a, a))
        return M("Uzunluğu %d m olan bir merdiven duvara dayanmıştır. Merdivenin alt ucu duvardan %d m uzaktadır. Merdivenin üst ucu yerden kaç m yüksektedir?" % (c, a), "%d m" % b,
                 ["%d m" % (c - a), "%d m" % (c + a), "%d m" % (b + 1)], "Duvar, yer ve merdiven dik üçgen oluşturur: √(%d² − %d²) = √%d = <b>%d m</b>." % (c, a, b * b, b))

    def kosegen():
        a, b, c = ch(TRIP)
        k = ri(1, 3)
        a, b, c = a * k, b * k, c * k
        return M("Kenarları %d cm ve %d cm olan dikdörtgenin köşegeni kaç cm’dir?" % (a, b), "%d cm" % c, ["%d cm" % (a + b), "%d cm" % (2 * (a + b)), "%d cm" % (c + 2)],
                 "Köşegen dikdörtgeni iki dik üçgene ayırır: √(%d + %d) = <b>%d cm</b>." % (a * a, b * b, c))

    def yaklasik():
        a, b = ri(1, 9), ri(1, 9)
        s = a * a + b * b
        r = math.isqrt(s)
        if r * r == s:
            return None
        return M("Dik kenarları %d cm ve %d cm olan dik üçgenin hipotenüsü hangi iki ardışık tam sayı arasındadır?" % (a, b), "%d ile %d" % (r, r + 1),
                 ["%d ile %d" % (r - 1, r), "%d ile %d" % (r + 1, r + 2), "%d ile %d" % (a + b - 1, a + b) if a + b - 1 != r else "%d ile %d" % (a + b + 1, a + b + 2)],
                 "Hipotenüs √%d; %d² = %d &lt; %d &lt; %d = %d²: <b>%d ile %d</b>." % (s, r, r * r, s, (r + 1) ** 2, r + 1, r, r + 1))

    sets = [("Hipotenüs", [(hip, 20)]),
            ("Dik kenar", [(dik_kenar, 20)]),
            ("Dik üçgen mi?", [(dik_mi, 20)]),
            ("Merdiven ve köşegen", [(merdiven, 10), (kosegen, 10)]),
            ("Karışık", [(yaklasik, 8), (hip, 6), (dik_kenar, 6)])]
    return unit("pisagor-bagintisi", "GS", "MAT.8.3.5, MAT.8.3.6", 17, "Pisagor Bağıntısı", "Pisagor Bağıntısı",
                "a² + b² = c² eşitliğini sağlayan üçgenleri inceler; Pisagor bağıntısını açı-kenar ilişkisi ve üçgen eşitsizliğiyle ilişkilendirir ve bu ilişkileri içeren problemleri çözer.",
                "8. sınıf Pisagor bağıntısı çalışma kâğıdı: hipotenüsü ve dik kenarı bulma, üçgenin dik, dar ya da geniş açılı olduğunu belirleme, merdiven ve köşegen problemleri, yaklaşık hipotenüs. 100 soru ve cevap anahtarı.",
                "a² + b² = c²", "c hipotenüs (dik açının karşısındaki en uzun kenar).", sets,
                ["Dik üçgende dik kenarların kareleri toplamı hipotenüsün karesine eşittir: a² + b² = c². Buna Pisagor bağıntısı denir.",
                 "Hipotenüs dik açının karşısındaki en uzun kenardır. Bir dik kenarı bulmak için b² = c² − a² yazarız.",
                 "Kenarları verilen bir üçgende en uzun kenarın karesi diğer ikisinin kareleri toplamına eşitse dik, büyükse geniş açılı, küçükse dar açılı üçgendir."],
                [("Dik kenarlar 6 ve 8 cm", ["36 + 64 = 100"], "Hipotenüs 10 cm"), ("Kenarlar 5, 6, 8", ["25 + 36 = 61 &lt; 64"], "Geniş açılı üçgen")],
                [["Kareleri almadan toplamak", "6 + 8 = 14 değil; √(36 + 64) = 10"],
                 ["Dik kenarı bulurken toplamak", "Dik kenar için çıkar: c² − a²"],
                 ["Hipotenüsü yanlış kenar seçmek", "Dik açının karşısındaki kenar hipotenüstür"]],
                [("Pisagor üçlüsü nedir?", "a² + b² = c² eşitliğini sağlayan doğal sayı üçlüleridir: 3-4-5, 5-12-13, 8-15-17."),
                 ("Pisagor bağıntısı her üçgende geçerli mi?", "Hayır, yalnızca dik üçgenlerde geçerlidir."),
                 ("Nerede kullanılır?", "Ekran boyutları (köşegen), inşaatta dik açı kontrolü ve iki nokta arasındaki uzaklıkta.")])


# ============================================================ 18. açınımlar
def u18():
    SOL = [("dik üçgen prizma", "2 üçgen ve 3 dikdörtgen"), ("dikdörtgenler prizması", "6 dikdörtgen"), ("küp", "6 kare"),
           ("kare dik piramit", "1 kare ve 4 ikizkenar üçgen"), ("dikdörtgen dik piramit", "1 dikdörtgen ve 4 ikizkenar üçgen"),
           ("dik dairesel silindir", "2 daire ve 1 dikdörtgen"), ("dik dairesel koni", "1 daire ve 1 daire dilimi"), ("altıgen dik prizma", "2 altıgen ve 6 dikdörtgen"),
           ("beşgen dik prizma", "2 beşgen ve 5 dikdörtgen")]

    def acinim():
        t, g = ch(SOL)
        w = [x for _, x in SOL if x != g]
        return M("Bir %s’nın yüzey açınımı hangi şekillerden oluşur?" % t if t.endswith("a") else "%s açınımında hangi şekiller vardır?" % cap(t), g, sh(w)[:3], "%s: <b>%s</b>." % (cap(t), g))

    def ters():
        t, g = ch(SOL)
        w = [x for x, _ in SOL if x != t]
        return M("Yüzey açınımı %s olan cisim hangisidir?" % g, cap(t), [cap(x) for x in sh(w)[:3]], "%s → <b>%s</b>." % (g, cap(t)))

    def sayi():
        n = ri(3, 10)
        k = ch(["prizma", "piramit"])
        nm = {3: "üçgen", 4: "dörtgen", 5: "beşgen", 6: "altıgen", 7: "yedigen", 8: "sekizgen", 9: "dokuzgen", 10: "ongen"}[n]
        q = ch(["yüz", "köşe", "ayrıt"])
        v = {("prizma", "yüz"): n + 2, ("prizma", "köşe"): 2 * n, ("prizma", "ayrıt"): 3 * n, ("piramit", "yüz"): n + 1, ("piramit", "köşe"): n + 1, ("piramit", "ayrıt"): 2 * n}[(k, q)]
        return M("Tabanı %s olan bir dik %s kaç %s sahiptir?" % (nm, k, {"yüz": "yüze", "köşe": "köşeye", "ayrıt": "ayrıta"}[q]), num(v), [num(v + 1), num(v - 1), num(v + n)],
                 "%s: taban kenar sayısı n = %d. %s sayısı <b>%d</b>." % (cap(k), n, cap(q), v))

    def silindir():
        r = ri(1, 15)
        k = ch(["genişlik", "taban"])
        if k == "genişlik":
            return M("Yarıçapı %d cm olan silindirin açınımındaki dikdörtgenin uzun kenarı kaç cm’dir? (π = 3)" % r, "%d cm" % (6 * r), ["%d cm" % (3 * r), "%d cm" % (3 * r * r), "%d cm" % (2 * r)],
                     "Dikdörtgenin bu kenarı taban çemberinin uzunluğuna eşittir: 2πr = 2 · 3 · %d = <b>%d cm</b>." % (r, 6 * r))
        return M("Yanal yüzey açınımındaki dikdörtgenin bir kenarı %d cm olan silindirin taban yarıçapı kaç cm’dir? (π = 3, bu kenar taban çevresine eşittir)" % (6 * r), "%d cm" % r,
                 ["%d cm" % (2 * r), "%d cm" % (3 * r), "%d cm" % (6 * r)], "2 · 3 · r = %d → r = <b>%d cm</b>." % (6 * r, r))

    def alan():
        k = ch(["küp", "prizma", "piramit"])
        if k == "küp":
            a = ri(2, 15)
            return M("Ayrıtı %d cm olan küpün açınımı 6 kareden oluşur. Açınımın alanı kaç cm²’dir?" % a, num(6 * a * a), [num(4 * a * a), num(a ** 3), num(6 * a)],
                     "6 · %d² = 6 · %d = <b>%s cm²</b>." % (a, a * a, num(6 * a * a)))
        if k == "prizma":
            a, b, c = ri(2, 10), ri(2, 10), ri(2, 10)
            if len({a, b, c}) < 3:
                return None
            S = 2 * (a * b + a * c + b * c)
            return M("Ayrıtları %d cm, %d cm ve %d cm olan dikdörtgenler prizmasının açınımının alanı kaç cm²’dir?" % (a, b, c), num(S), [num(S // 2), num(a * b * c), num(S + 2 * a * b)],
                     "2 · (%d · %d + %d · %d + %d · %d) = <b>%s cm²</b>." % (a, b, a, c, b, c, num(S)))
        a, h = ri(2, 12), ri(3, 15)
        S = a * a + 2 * a * h
        return M("Kare dik piramidin açınımında karenin kenarı %d cm, her üçgenin yüksekliği %d cm’dir. Açınımın alanı kaç cm²’dir?" % (a, h), num(S), [num(a * a + 4 * a * h), num(2 * a * h), num(a * a + a * h)],
                 "Kare: %d. Dört üçgen: 4 · (%d · %d ÷ 2) = %d. Toplam <b>%s cm²</b>." % (a * a, a, h, 2 * a * h, num(S)))

    sets = [("Açınımdaki şekiller", [(acinim, 9), (sayi, 11)]),
            ("Açınımdan cisme", [(ters, 9), (sayi, 11)]),
            ("Yüz, köşe ve ayrıt", [(sayi, 20)]),
            ("Silindir açınımı", [(silindir, 20)]),
            ("Açınımın alanı", [(alan, 20)])]
    return unit("cisimlerin-yuzey-acinimlari", "GN", "MAT.8.4.1", 18, "Prizma, Piramit, Silindir ve Koninin Yüzey Açınımları", "Yüzey Açınımları",
                "Dik prizma, dikdörtgen dik piramit, dik dairesel silindir ve dik dairesel koninin yüzey açınımlarını çözümler; açınımlardaki şekilleri ve aralarındaki ilişkileri belirler.",
                "8. sınıf cisimlerin yüzey açınımları çalışma kâğıdı: prizma, piramit, silindir ve koni açınımındaki şekiller, açınımdan cismi bulma, yüz, köşe ve ayrıt sayıları, silindir açınımındaki dikdörtgen. 100 soru ve cevap anahtarı.",
                "Açınım: cismin yüzeyini düz kâğıda açmak", "Silindir: 2 daire ve 1 dikdörtgen.", sets,
                ["Bir cismin yüzeyi kesilip düz bir zemine açılınca yüzey açınımı elde edilir. Açınım katlanınca cisim yeniden oluşur.",
                 "Dik prizmada iki eş taban ve tabanın kenar sayısı kadar dikdörtgen yan yüz vardır. Piramitte bir taban ve üçgen yan yüzler vardır.",
                 "Silindirin açınımı iki daire ve bir dikdörtgendir; dikdörtgenin bir kenarı taban çevresine (2πr), diğeri yüksekliğe eşittir. Koninin açınımı bir daire ve bir daire dilimidir."],
                [("Altıgen dik prizma", ["2 altıgen taban", "6 dikdörtgen yan yüz"], "8 yüz"), ("r = 5 cm silindir (π = 3)", ["2 · 3 · 5"], "Dikdörtgenin bir kenarı 30 cm")],
                [["Piramidin yan yüzlerini dikdörtgen sanmak", "Piramidin yan yüzleri üçgendir"],
                 ["Silindir açınımındaki dikdörtgenin kenarını çap sanmak", "Kenar taban çevresidir: 2πr"],
                 ["Prizmada taban sayısını 1 almak", "Prizmanın 2 eş tabanı vardır"]],
                [("Koninin yanal yüzü neden daire dilimidir?", "Tepe noktası etrafında açılınca kenarı tepe ile tabanı birleştiren ana doğru olan bir dilim oluşur."),
                 ("Bir cismin kaç açınımı olur?", "Birden fazla olabilir; küpün 11 farklı açınımı vardır."),
                 ("Açınım ne işe yarar?", "Kutu ve ambalaj tasarımında, yüzey alanını hesaplamada.")])


# ============================================================ 19. silindir
def u19():
    def yanal():
        r, h = ri(1, 12), ri(2, 20)
        return M("Yarıçapı %d cm, yüksekliği %d cm olan silindirin yanal alanı kaç cm²’dir? (π = 3)" % (r, h), num(6 * r * h), [num(3 * r * h), num(6 * r * h + 6 * r * r), num(3 * r * r * h)],
                 "Yanal alan = 2πr · h = 2 · 3 · %d · %d = <b>%s cm²</b>." % (r, h, num(6 * r * h)))

    def yuzey():
        r, h = ri(1, 10), ri(2, 20)
        S = 6 * r * h + 6 * r * r
        return M("Yarıçapı %d cm, yüksekliği %d cm olan silindirin yüzey alanı kaç cm²’dir? (π = 3)" % (r, h), num(S), [num(6 * r * h), num(6 * r * h + 3 * r * r), num(3 * r * r * h)],
                 "Yüzey alanı = 2πr² + 2πrh = %d + %d = <b>%s cm²</b>." % (6 * r * r, 6 * r * h, num(S)))

    def hacim():
        r, h = ri(1, 12), ri(2, 20)
        p = ch([3, F(314, 100)])
        V = p * r * r * h
        pt = "3" if p == 3 else "3,14"
        return M("Yarıçapı %d cm, yüksekliği %d cm olan silindirin hacmi kaç cm³’tür? (π = %s)" % (r, h, pt), dq(V), [dq(2 * p * r * h), dq(p * r * h), dq(p * 4 * r * r * h)],
                 "V = πr² · h = %s · %d · %d = <b>%s cm³</b>." % (pt, r * r, h, dq(V)))

    def ters():
        r, h = ri(1, 10), ri(2, 20)
        V = 3 * r * r * h
        return M("Hacmi %s cm³, taban yarıçapı %d cm olan silindirin yüksekliği kaç cm’dir? (π = 3)" % (num(V), r), "%d cm" % h, ["%d cm" % (h * r), "%d cm" % (V // (6 * r)) if V // (6 * r) != h else "%d cm" % (h + 2), "%d cm" % (h + 1)],
                 "%s = 3 · %d · h → h = <b>%d cm</b>." % (num(V), r * r, h))

    def problem():
        r, h = ri(2, 5) * 10, ri(3, 10) * 10
        V = 3 * r * r * h
        if V % 1000:
            return None
        return M("Taban yarıçapı %d cm, yüksekliği %d cm olan silindir biçimindeki bir su deposu kaç litre su alır? (π = 3, 1 L = 1.000 cm³)" % (r, h), "%s L" % num(V // 1000),
                 ["%s L" % num(V // 100), "%s L" % num(V // 10000) if V >= 10000 else "%s L" % num(V // 1000 + 3), "%s L" % num(6 * r * h // 1000) if 6 * r * h >= 1000 else "%s L" % num(V // 1000 * 2)],
                 "V = 3 · %d · %d = %s cm³ = <b>%s L</b>." % (r * r, h, num(V), num(V // 1000)))

    sets = [("Yanal alan", [(yanal, 20)]),
            ("Yüzey alanı", [(yuzey, 20)]),
            ("Hacim", [(hacim, 20)]),
            ("Yükseklik ve problemler", [(ters, 10), (problem, 10)]),
            ("Karışık", [(yuzey, 7), (hacim, 7), (ters, 6)])]
    return unit("silindirin-yuzey-alani-ve-hacmi", "GN", "MAT.8.4.2, MAT.8.4.3", 19, "Dik Dairesel Silindirin Yüzey Alanı ve Hacmi", "Silindir",
                "Dik dairesel silindirin yüzey açınımı deneyimini yüzey alanına yansıtır; dairenin alan bağıntısından hareketle silindirin hacmine dair analojik akıl yürütür.",
                "8. sınıf silindirin yüzey alanı ve hacmi çalışma kâğıdı: yanal alan, yüzey alanı, hacim (V = πr²h), hacimden yükseklik bulma, su deposu problemleri. 100 soru ve cevap anahtarı.",
                "V = πr² · h", "Yüzey alanı = 2πr² + 2πrh (iki taban + yanal yüz).", sets,
                ["Silindirin açınımı iki daire ve bir dikdörtgendir. Dikdörtgenin kenarları 2πr ve h olduğundan yanal alan 2πrh’dir.",
                 "Yüzey alanı = iki tabanın alanı + yanal alan = 2πr² + 2πrh.",
                 "Silindir, üst üste konmuş çok ince dairelerden oluşur gibi düşünülebilir: hacim = taban alanı × yükseklik = πr²h."],
                [("r = 4 cm, h = 10 cm, π = 3", ["Yanal 2 · 3 · 4 · 10 = 240", "Tabanlar 2 · 3 · 16 = 96"], "Yüzey alanı 336 cm²"), ("r = 5 cm, h = 8 cm", ["3 · 25 · 8"], "600 cm³")],
                [["Yüzey alanında bir tabanı unutmak", "İki taban vardır: 2πr²"],
                 ["Hacimde çapı kullanmak", "r yarıçaptır; çap 10 ise r = 5"],
                 ["Yanal alanda πr² kullanmak", "Yanal alan 2πrh"]],
                [("Silindir hacmi prizmaya benzer mi?", "Evet, ikisinde de hacim taban alanı × yüksekliktir."),
                 ("Konserve kutusunun etiketi neyi gösterir?", "Yanal yüzeyi; açıldığında bir dikdörtgen olur."),
                 ("π için hangi değer kullanılır?", "Soruda ne verilirse: genellikle 3 ya da 3,14.")])


# ============================================================ 20. öteleme
def u20():
    def nokta():
        x, y = nz(-5, 5), nz(-5, 5)
        dx, dy = nz(-5, 5), ri(-5, 5)
        g = "(%s, %s)" % (sn(x + dx), sn(y + dy))
        yon = "%d birim %s" % (abs(dx), "sağa" if dx > 0 else "sola") + ("" if dy == 0 else " ve %d birim %s" % (abs(dy), "yukarı" if dy > 0 else "aşağı"))
        return M("A(%s, %s) noktası %s ötelenirse görüntüsü A′ hangi noktadır?" % (sn(x), sn(y), yon), g,
                 ["(%s, %s)" % (sn(x - dx), sn(y + dy)), "(%s, %s)" % (sn(x + dy), sn(y + dx)), "(%s, %s)" % (sn(x + dx), sn(y - dy)) if dy else "(%s, %s)" % (sn(x), sn(y + dx))],
                 "Sağa/sola öteleme x’i, yukarı/aşağı öteleme y’yi değiştirir: <b>%s</b>." % g)

    def ozellik():
        S = [("Öteleme dönüşümünde şekil ile görüntüsü için hangisi doğrudur?", "Eştir; yönü de değişmez", ["Görüntü daha büyüktür", "Şeklin yönü ters döner", "Yalnızca alanları eşittir"]),
             ("Ötelemede şeklin her noktası için hangisi doğrudur?", "Aynı yönde, aynı miktarda kayar", ["Farklı miktarlarda kayar", "Bir noktanın etrafında döner", "Bir doğruya göre yansır"]),
             ("Ötelemede bir kenar ile görüntüsü nasıldır?", "Eşit uzunlukta ve paraleldir", ["Diktir", "Görüntü iki katıdır", "Kesişir"])]
        q, g, w = ch(S)
        return M(q, g, w, "Ötelemede şekil kaydırılır; boyut, biçim ve yön korunur. Cevap: <b>%s</b>." % g)

    def kural():
        x, y = nz(-5, 5), nz(-5, 5)
        dx, dy = nz(-6, 6), nz(-6, 6)
        g = "%d birim %s, %d birim %s" % (abs(dx), "sağa" if dx > 0 else "sola", abs(dy), "yukarı" if dy > 0 else "aşağı")
        w = ["%d birim %s, %d birim %s" % (abs(dx), "sola" if dx > 0 else "sağa", abs(dy), "yukarı" if dy > 0 else "aşağı"),
             "%d birim %s, %d birim %s" % (abs(dy), "sağa" if dy > 0 else "sola", abs(dx), "yukarı" if dx > 0 else "aşağı"),
             "%d birim %s, %d birim %s" % (abs(dx), "sağa" if dx > 0 else "sola", abs(dy), "aşağı" if dy > 0 else "yukarı")]
        return M("A(%s, %s) noktası ötelenerek A′(%s, %s) noktasına taşınmıştır. Öteleme nasıl yapılmıştır?" % (sn(x), sn(y), sn(x + dx), sn(y + dy)), g, w,
                 "x %s’ten %s’e (%s), y %s’ten %s’e (%s): <b>%s</b>." % (sn(x), sn(x + dx), sn(dx), sn(y), sn(y + dy), sn(dy), g) if False else
                 "x’teki değişim %s, y’deki değişim %s: <b>%s</b>." % (sn(dx), sn(dy), g))

    def sekil():
        pts = [(ri(-5, -1), ri(-5, -1)), (ri(-5, -1), ri(-5, -1)), (ri(-5, -1), ri(-5, -1))]
        if len(set(pts)) < 3:
            return None
        dx, dy = ri(2, 6), ri(2, 6)
        vs = ["A", "B", "C"]
        i = ri(0, 2)
        p = pts[i]
        g = "(%s, %s)" % (sn(p[0] + dx), sn(p[1] + dy))
        return M("ABC üçgeninin köşeleri A(%s, %s), B(%s, %s), C(%s, %s)’dir. Üçgen %d birim sağa ve %d birim yukarı ötelenirse %s′ hangi noktadır?" % (sn(pts[0][0]), sn(pts[0][1]), sn(pts[1][0]), sn(pts[1][1]), sn(pts[2][0]), sn(pts[2][1]), dx, dy, vs[i]),
                 g, ["(%s, %s)" % (sn(p[0] + dy), sn(p[1] + dx)) if dx != dy else "(%s, %s)" % (sn(p[0] + dx), sn(p[1])), "(%s, %s)" % (sn(p[0] - dx), sn(p[1] + dy)), "(%s, %s)" % (sn(p[0] + dx), sn(p[1] - dy))],
                 "%s(%s, %s) → (%s + %d, %s + %d) = <b>%s</b>." % (vs[i], sn(p[0]), sn(p[1]), sn(p[0]), dx, sn(p[1]), dy, g))

    sets = [("Noktayı öteleme", [(nokta, 20)]),
            ("Ötelemeyi bulma", [(kural, 20)]),
            ("Üçgeni öteleme", [(sekil, 20)]),
            ("Ötelemenin özellikleri", [(ozellik, 3), (nokta, 17)]),
            ("Karışık", [(kural, 10), (sekil, 10)])]
    return unit("oteleme-donusumu", "D", "MAT.8.5.1", 20, "Öteleme Dönüşümü", "Öteleme",
                "Matematiksel araç ve teknoloji yardımıyla öteleme dönüşümünü çözümler; şekillerin öteleme altındaki görüntülerinin kenar ve açı özelliklerini ve şekil ile görüntüsü arasındaki ilişkileri belirler.",
                "8. sınıf öteleme dönüşümü çalışma kâğıdı: bir noktayı ve üçgeni öteleme, verilen görüntüden ötelemeyi bulma, ötelemenin özellikleri. 100 soru ve cevap anahtarı.",
                "Öteleme: kaydırma", "Sağa/sola x değişir, yukarı/aşağı y değişir; şekil eş kalır.", sets,
                ["Öteleme, bir şeklin her noktasının aynı yönde ve aynı miktarda kaydırılmasıdır.",
                 "Ötelemede şekil ile görüntüsü eştir; kenarlar görüntüleriyle paralel ve eşit uzunluktadır, şeklin yönü değişmez.",
                 "Koordinat düzleminde a birim sağa ve b birim yukarı öteleme: (x, y) → (x + a, y + b). Sola ve aşağı için çıkarırız."],
                [("A(−2, 3), 5 birim sağa, 4 birim aşağı", ["x: −2 + 5", "y: 3 − 4"], "A′(3, −1)"), ("A(1, 1) → A′(−3, 6)", ["x: −4", "y: +5"], "4 birim sola, 5 birim yukarı")],
                [["Sağa ötelemede y’yi değiştirmek", "Sağa/sola: yalnızca x değişir"],
                 ["Aşağı ötelemede eklemek", "Aşağı: y’den çıkar"],
                 ["Ötelemeyi yansımayla karıştırmak", "Ötelemede şeklin yönü ters dönmez"]],
                [("Öteleme ile yansıma farkı nedir?", "Ötelemede şekil kayar ve yönü aynı kalır; yansımada şekil ayna görüntüsüne döner."),
                 ("Günlük hayatta öteleme?", "Asansörün hareketi, yürüyen merdiven, satranç taşını düz kaydırmak."),
                 ("Ötelemede açılar değişir mi?", "Hayır, açılar ve uzunluklar aynı kalır.")])


# ============================================================ 21. koordinatlarda yansıma ve öteleme
def u21():
    def yansima():
        x, y = nz(-6, 6), nz(-6, 6)
        k = ch(["x", "y"])
        g = "(%s, %s)" % (sn(x), sn(-y)) if k == "x" else "(%s, %s)" % (sn(-x), sn(y))
        w = ["(%s, %s)" % (sn(-x), sn(y)) if k == "x" else "(%s, %s)" % (sn(x), sn(-y)), "(%s, %s)" % (sn(-x), sn(-y)), "(%s, %s)" % (sn(y), sn(x))]
        return M("A(%s, %s) noktasının %s eksenine göre yansıması hangi noktadır?" % (sn(x), sn(y), k), g, w,
                 "%s eksenine göre yansımada %s aynı kalır, %s işaret değiştirir: <b>%s</b>." % (k, "x" if k == "x" else "y", "y" if k == "x" else "x", g))

    def grafik():
        x, y = nz(-5, 5), nz(-5, 5)
        k = ch(["x", "y"])
        img = (x, -y) if k == "x" else (-x, y)
        cands = [img, (-x, -y), (x, -y) if k == "y" else (-x, y), (y, x)]
        if len(set(cands)) < 4 or (x, y) in cands:
            return None
        labs = sh(["B", "C", "D", "E"])
        pts = [(x, y, "A")] + [(c[0], c[1], labs[i]) for i, c in enumerate(cands)]
        return M("A noktasının %s eksenine göre yansıması hangi noktadır?" % k + kosy(pts=pts), labs[0], labs[1:],
                 "A(%s, %s); %s eksenine göre görüntüsü (%s, %s): <b>%s</b>." % (sn(x), sn(y), k, sn(img[0]), sn(img[1]), labs[0]))

    def ard():
        x, y = nz(-5, 5), nz(-5, 5)
        dx, dy = nz(-4, 4), nz(-4, 4)
        k = ch(["x", "y"])
        p = (x + dx, y + dy)
        img = (p[0], -p[1]) if k == "x" else (-p[0], p[1])
        g = "(%s, %s)" % (sn(img[0]), sn(img[1]))
        yon = "%d birim %s ve %d birim %s" % (abs(dx), "sağa" if dx > 0 else "sola", abs(dy), "yukarı" if dy > 0 else "aşağı")
        return M("A(%s, %s) noktası önce %s ötelenip sonra %s eksenine göre yansıtılıyor. Son görüntü hangi noktadır?" % (sn(x), sn(y), yon, k), g,
                 ["(%s, %s)" % (sn(p[0]), sn(p[1])), "(%s, %s)" % (sn(-img[0]), sn(-img[1])), "(%s, %s)" % (sn((x, -y)[0] + dx if k == "x" else -x + dx), sn((-y + dy) if k == "x" else y + dy))],
                 "Öteleme: (%s, %s). %s eksenine göre yansıma: <b>%s</b>." % (sn(p[0]), sn(p[1]), k, g))

    def hangi():
        x, y = nz(-6, 6), nz(-6, 6)
        k = ch(["x eksenine göre yansıma", "y eksenine göre yansıma", "öteleme"])
        if k.startswith("x"):
            q = (x, -y)
        elif k.startswith("y"):
            q = (-x, y)
        else:
            q = (x + nz(-4, 4), y + nz(-4, 4))
            if q in ((x, -y), (-x, y)):
                return None
        if q == (x, y) or (k != "öteleme" and ((x, -y) == (-x, y))):
            return None
        cz = lambda v: v if v[0] in "xy" else cap(v)
        return M("A(%s, %s) noktası A′(%s, %s) noktasına taşınmıştır. Bu hangi dönüşümle olabilir?" % (sn(x), sn(y), sn(q[0]), sn(q[1])), cz(k),
                 [cz(v) for v in ("x eksenine göre yansıma", "y eksenine göre yansıma", "öteleme", "dönme") if v != k][:3],
                 "x eksenine göre yansımada y, y eksenine göre yansımada x işaret değiştirir; ötelemede ikisi de bir miktar değişir. Cevap: <b>%s</b>." % cz(k))

    sets = [("Eksenlere göre yansıma", [(yansima, 20)]),
            ("Grafikte yansıma", [(grafik, 20)]),
            ("Art arda dönüşüm", [(ard, 20)]),
            ("Hangi dönüşüm?", [(hangi, 20)]),
            ("Karışık", [(yansima, 7), (ard, 7), (hangi, 6)])]
    return unit("koordinat-duzleminde-oteleme-ve-yansima", "D", "MAT.8.5.2, MAT.8.5.3", 21, "Koordinat Düzleminde Öteleme ve Yansıma", "Öteleme ve Yansıma",
                "Dik koordinat sisteminde noktaların apsis ve ordinatlarının öteleme ve eksenlere göre yansıma dönüşümündeki değişimi hakkında çıkarım yapar ve bu dönüşümleri içeren problemleri çözer.",
                "8. sınıf koordinat düzleminde öteleme ve yansıma çalışma kâğıdı: x ve y eksenine göre yansıma, grafikte yansıma, art arda öteleme ve yansıma, dönüşümün türünü bulma. 100 soru ve cevap anahtarı.",
                "x eksenine göre: (x, y) → (x, −y)", "y eksenine göre: (x, y) → (−x, y).", sets,
                ["x eksenine göre yansımada apsis aynı kalır, ordinat işaret değiştirir: (3, 2) → (3, −2).",
                 "y eksenine göre yansımada ordinat aynı kalır, apsis işaret değiştirir: (3, 2) → (−3, 2).",
                 "Art arda dönüşümlerde sıraya dikkat ederiz: önce birinci dönüşümün görüntüsünü bulur, sonra ona ikinci dönüşümü uygularız."],
                [("A(−4, 5), x eksenine göre", ["y işaret değiştirir"], "(−4, −5)"), ("A(1, 2): 3 birim sağa, sonra y eksenine göre", ["(4, 2)", "(−4, 2)"], "(−4, 2)")],
                [["x eksenine göre yansımada x’i değiştirmek", "x ekseni yatay; y değişir"],
                 ["Art arda dönüşümde sırayı karıştırmak", "Önce öteleme, sonra yansıma"],
                 ["Yansımada ikisinin de işaretini değiştirmek", "O, başlangıç noktasına göre yansımadır"]],
                [("Başlangıç noktasına göre yansıma nedir?", "Hem x hem y işaret değiştirir: (x, y) → (−x, −y)."),
                 ("Dönüşümlerin sırası önemli mi?", "Evet, öteleme ve yansımanın sırası değişince sonuç genellikle değişir."),
                 ("Bu dönüşümler nerede kullanılır?", "Bilgisayar oyunlarında ve grafik tasarımda nesneleri taşımak ve aynalamak için.")])


# ============================================================ 22. veri
def u22():
    def grafik_sec():
        S = [("Bir sınıftaki öğrencilerin en sevdiği spor dallarının yüzdelerini göstermek", "Daire grafiği"), ("Bir şehrin bir yıl boyunca aylık ortalama sıcaklığındaki değişimi göstermek", "Çizgi grafiği"),
             ("Farklı illerdeki kütüphane sayılarını karşılaştırmak", "Sütun grafiği"), ("Bir sınıftaki öğrencilerin boy uzunluklarının dağılımını sıklıkla göstermek", "Histogram"),
             ("Bir ailenin aylık bütçesinin harcama kalemlerine dağılımını göstermek", "Daire grafiği"), ("Bir bebeğin aylara göre kilosundaki artışı göstermek", "Çizgi grafiği"),
             ("Beş ürünün haftalık satış adetlerini karşılaştırmak", "Sütun grafiği"), ("Koşucuların bitirme sürelerinin aralıklara göre dağılımını göstermek", "Histogram")]
        t, g = ch(S)
        return M("Amaç: %s. Hangi grafik türü en uygundur?" % t, g, [x for x in ("Daire grafiği", "Çizgi grafiği", "Sütun grafiği", "Histogram") if x != g],
                 "Parça-bütün için daire, zamana göre değişim için çizgi, kategorileri karşılaştırma için sütun, sürekli verinin dağılımı için histogram. Cevap: <b>%s</b>." % g)

    def ozet():
        n = ch([5, 7, 9])
        xs = sorted(ri(1, 40) for _ in range(n))
        k = ch(["ortanca (medyan)", "açıklık", "tepe değer (mod)"])
        kq = {"ortanca (medyan)": "ortancası (medyanı)", "açıklık": "açıklığı", "tepe değer (mod)": "tepe değeri (modu)"}[k]
        if k.startswith("tepe"):
            v = ch(xs)
            xs = sorted(xs[:-1] + [v])
            from collections import Counter
            c = Counter(xs).most_common()
            if len(c) > 1 and c[0][1] == c[1][1]:
                return None
            val = c[0][0]
        elif k.startswith("ortanca"):
            val = xs[n // 2]
        else:
            val = xs[-1] - xs[0]
        shown = sh(xs)
        others = {xs[n // 2], xs[-1] - xs[0], F(sum(xs), n)}
        w = [sn(o) if not isinstance(o, F) or o.denominator == 1 else dq(o, 1) for o in others if o != val] + [num(val + 1)]
        return M("%s verilerinin %s kaçtır?" % (", ".join(map(str, shown)), kq), num(val), w,
                 "Veriler sıralanır: %s. %s: <b>%d</b>." % (", ".join(map(str, xs)), cap(k), val))

    def yanli():
        S = [("Okulun en sevilen yemeğini belirlemek için yalnızca basketbol takımındaki öğrencilere soru sormak", "Yanlıdır; örneklem bütün okulu temsil etmiyor"),
             ("Bir ilçedeki ailelerin kitap okuma alışkanlığını belirlemek için kütüphane girişinde anket yapmak", "Yanlıdır; kütüphaneye gelenler daha çok kitap okuyor olabilir"),
             ("Sınıftaki öğrencilerin uyku sürelerini belirlemek için her öğrenciye sormak", "Yanlı değildir; evrenin tamamı soruldu"),
             ("Bir okuldaki öğrencilerin servis kullanımını belirlemek için her sınıftan rastgele 5 öğrenci seçmek", "Yanlı değildir; örneklem rastgele ve her sınıftan"),
             ("Bir filmin beğenilip beğenilmediğini yalnızca filmin hayran sayfasındaki yorumlarla değerlendirmek", "Yanlıdır; yalnızca filmi sevenlerin görüşü alınıyor")]
        t, r = ch(S)
        g, why = r.split("; ")
        w = [x for x in ("Yanlıdır", "Yanlı değildir") if x != g] + ["Veri toplamaya gerek yoktur", "Bilinemez"]
        return M("“%s” Bu veri toplama yöntemi yanlı mıdır?" % t, g, w, "Örneklem evreni temsil etmeli. Burada %s: <b>%s</b>." % (why, g))

    def kiyas():
        n1, n2 = ch([("A sınıfı", "B sınıfı"), ("Kız öğrenciler", "Erkek öğrenciler"), ("Sabah grubu", "Öğle grubu")])
        m1, m2 = ri(50, 80), ri(50, 80)
        r1, r2 = ri(10, 40), ri(10, 40)
        if m1 == m2 or r1 == r2:
            return None
        k = ch(["ortalama başarısı daha yüksek", "puanları daha tutarlı (az yayılmış)"])
        g = (n1 if m1 > m2 else n2) if k.startswith("ortalama") else (n1 if r1 < r2 else n2)
        return M("%s: ortalama %d, açıklık %d. %s: ortalama %d, açıklık %d. Hangisinin %s?" % (n1, m1, r1, n2, m2, r2, k), g, [n2 if g == n1 else n1, "İkisi aynı", "Bilinemez"],
                 "Ortalama merkezi, açıklık yayılımı gösterir. %s: <b>%s</b>." % ("Ortalaması büyük olan" if k.startswith("ortalama") else "Açıklığı küçük olan", g))

    sets = [("Uygun grafik", [(grafik_sec, 8), (ozet, 12)]),
            ("Merkez ve yayılım", [(ozet, 20)]),
            ("Grupları karşılaştırma", [(kiyas, 20)]),
            ("Yanlı örneklem", [(yanli, 5), (kiyas, 15)]),
            ("Karışık", [(ozet, 10), (kiyas, 10)])]
    return unit("veri-analizi-ve-yorumlama", "IA", "MAT.8.6.1, MAT.8.6.2", 22, "Veri Analizi: Uygun Grafik, Özetleme ve Yanlılık", "Veri Analizi",
                "Kategorik veya nicel (kesikli-sürekli) veriyle çalışır ve veriye dayalı karar verir; görselleştirme ve özetleme araçlarını gerekçeyle seçer, başkalarının istatistiksel sonuçlarındaki hata ve yanlılıkları tartışır.",
                "8. sınıf veri analizi çalışma kâğıdı: amaca uygun grafik seçimi, ortanca, tepe değer ve açıklık, iki grubu ortalama ve açıklıkla karşılaştırma, yanlı örneklem. 100 soru ve cevap anahtarı.",
                "Amaca göre grafik, veriye göre özet", "Ortalama merkezi, açıklık yayılımı gösterir.", sets,
                ["Veri türüne ve amaca göre grafik seçeriz: daire (parça-bütün), sütun (karşılaştırma), çizgi (zamana göre değişim), histogram (sürekli veri dağılımı).",
                 "Merkezi eğilim ölçüleri (ortalama, ortanca, tepe değer) verinin nerede toplandığını; açıklık verinin ne kadar yayıldığını gösterir.",
                 "Örneklem evreni temsil etmezse sonuç yanlı olur. Örneklem rastgele ve farklı gruplardan seçilmelidir."],
                [("3, 7, 7, 9, 14", ["Ortanca: 7", "Tepe değer: 7", "Açıklık: 11"], "7, 7 ve 11"), ("Okulun görüşü için yalnızca bir kulübe sormak", ["Kulüp okulu temsil etmez"], "Yanlı")],
                [["Ortancayı sıralamadan bulmak", "Önce küçükten büyüğe sırala"],
                 ["Zamana göre değişim için daire grafiği seçmek", "Çizgi grafiği kullanılır"],
                 ["Küçük ve seçilmiş bir grubu genele yaymak", "Örneklem temsil edici olmalı"]],
                [("Evren ve örneklem nedir?", "Evren, hakkında bilgi istenen grubun tamamıdır; örneklem bu gruptan seçilen kısımdır."),
                 ("Ortalama mı ortanca mı kullanmalı?", "Uç değerler varsa ortanca daha iyi bir merkez ölçüsüdür."),
                 ("Bir haberdeki istatistiğe nasıl yaklaşmalı?", "Verinin nereden, kaç kişiden ve nasıl toplandığını sorgula.")])


# ============================================================ 23. olasılık yaklaşımları
def u23():
    def tur():
        S = [("Yarın yağmur yağacağını düşünüyorum, çünkü bulutlar kararıyor.", "Öznel olasılık"),
             ("Bir zar 600 kez atıldı ve 95 kez 6 geldi; 6 gelme olasılığı 95/600’dür.", "Deneysel olasılık"),
             ("Hilesiz bir zarda 6 gelme olasılığı 1/6’dır.", "Teorik olasılık"),
             ("Takımımızın maçı kazanma ihtimali bence yüksek.", "Öznel olasılık"),
             ("Bir torbada 3 kırmızı, 5 mavi top var; kırmızı çekme olasılığı 3/8’dir.", "Teorik olasılık"),
             ("Bir okulda 200 öğrenciden 46’sı gözlük takıyor; rastgele seçilen öğrencinin gözlüklü olma olasılığı 46/200’dür.", "Deneysel olasılık"),
             ("Bir para 50 kez atıldı, 28 kez yazı geldi.", "Deneysel olasılık"), ("Bu sınavdan iyi not alacağımı hissediyorum.", "Öznel olasılık"),
             ("Hilesiz bir parada tura gelme olasılığı 1/2’dir.", "Teorik olasılık")]
        t, g = ch(S)
        return M("“%s” Bu ifade hangi olasılık yaklaşımına örnektir?" % t, g, [x for x in ("Öznel olasılık", "Deneysel olasılık", "Teorik olasılık", "Kesin olay") if x != g],
                 "Öznel: kişisel görüş; deneysel: deney ve gözlem sonuçları; teorik: eşit olasılıklı çıktılarla hesap. Cevap: <b>%s</b>." % g)

    def deneysel():
        n = ch([20, 40, 50, 60, 80, 100, 200])
        k = ri(1, n - 1)
        p = F(k, n)
        ob = ch(["kırmızı", "sarı", "mavi"])
        return M("Bir çark %d kez çevrildi ve %d kez %s renkte durdu. Çarkın %s renkte durmasının deneysel olasılığı kaçtır?" % (n, k, ob, ob), sn(p), [sn(F(n - k, n)), sn(F(k, n - k)) if n != 2 * k else sn(F(1, 3)), sn(F(1, 3)) if p != F(1, 3) else sn(F(1, 4))],
                 "Deneysel olasılık = olayın gözlenme sayısı ÷ deney sayısı = %d/%d = <b>%s</b>." % (k, n, sn(p)))

    def yaklasma():
        S = [("Bir zar 10 kez atıldığında 6 gelme oranı 3/10, 10 000 kez atıldığında 1 668/10 000 bulundu. Hangisi doğrudur?", "Deney sayısı arttıkça deneysel olasılık teorik olasılığa (1/6) yaklaşır"),
             ("Bir para 20 kez atılınca 14 yazı geldi. Bu sonuca göre hangisi doğrudur?", "Deney sayısı az olduğu için sonuç 1/2’den uzak çıkabilir"),
             ("Bir deneyi çok sayıda tekrarlamak neden önemlidir?", "Deneysel olasılık teorik olasılığa yaklaşır ve daha güvenilir olur")]
        q, g = ch(S)
        w = ["Deney sayısı arttıkça deneysel olasılık 0’a yaklaşır", "Deneysel ve teorik olasılık her zaman eşittir", "Deney sayısının sonuca etkisi yoktur"]
        return M(q, g, w, "Bir deney çok kez tekrarlandıkça deneysel olasılık teorik olasılığa yaklaşır. Cevap: <b>%s</b>." % g)

    def tahmin():
        p = ch([F(1, 2), F(1, 4), F(1, 5), F(1, 6), F(2, 5), F(3, 10), F(1, 10)])
        n = ch([60, 100, 120, 200, 300, 600])
        if (n * p).denominator != 1:
            return None
        v = int(n * p)
        return M("Bir olayın teorik olasılığı %s olarak hesaplanmıştır. Deney %d kez tekrarlanırsa olayın yaklaşık kaç kez gerçekleşmesi beklenir?" % (sn(p), n), num(v), [num(n - v), num(v * 2), num(p.denominator)],
                 "%d · %s = <b>%d</b> (deneysel sonuç bunun çevresinde olur)." % (n, sn(p), v))

    def karar():
        n1 = G.K.next()
        a, b = ri(10, 40), ri(41, 100)
        x, y = ri(2, a - 1), ri(5, b - 1)
        return M("%s bir zarın hileli olup olmadığını anlamak istiyor. Birinci denemede zarı %d kez attı ve %d kez 6 geldi; ikinci denemede %d kez attı ve %d kez 6 geldi. Hangi deneme daha güvenilir sonuç verir?" % (n1, a, x, b, y),
                 "İkinci deneme (deney sayısı daha fazla)", ["Birinci deneme (deney sayısı daha az)", "İkisi aynı güvenilirliktedir", "Hiçbiri; yalnızca öznel olasılık kullanılır"],
                 "Çok sayıda tekrar, teorik olasılığa daha yakın ve güvenilir sonuç verir: <b>ikinci deneme</b>.")

    sets = [("Olasılık yaklaşımları", [(tur, 9), (deneysel, 11)]),
            ("Deneysel olasılık", [(deneysel, 20)]),
            ("Beklenen sonuç", [(tahmin, 20)]),
            ("Deney sayısı ve güvenilirlik", [(yaklasma, 3), (karar, 17)]),
            ("Karışık", [(deneysel, 7), (tahmin, 7), (karar, 6)])]
    return unit("olasilik-yaklasimlari", "VO", "MAT.8.7.1", 23, "Öznel, Deneysel ve Teorik Olasılık", "Olasılık Yaklaşımları",
                "Gerçek yaşamdaki bir olayın olasılığı için öznel, deneysel ve teorik yaklaşımlardan uygun olanı seçerek karar verir; deney sayısı arttıkça deneysel olasılığın teorik olasılığa yaklaştığını değerlendirir.",
                "8. sınıf olasılık yaklaşımları çalışma kâğıdı: öznel, deneysel ve teorik olasılık örnekleri, deneysel olasılığı hesaplama, beklenen sonuç sayısı, deney sayısının güvenilirliğe etkisi. 100 soru ve cevap anahtarı.",
                "Çok deney → teorik olasılığa yaklaşır", "Öznel: tahmin, deneysel: gözlem, teorik: hesap.", sets,
                ["Öznel olasılık kişisel deneyim ve görüşe dayanır. Deneysel olasılık, bir deneyin sonuçlarından hesaplanır: olayın gözlenme sayısı ÷ deney sayısı.",
                 "Teorik olasılık, çıktılar eşit olasılıklıysa istenen çıktı sayısının tüm çıktı sayısına bölünmesiyle bulunur.",
                 "Deney sayısı arttıkça deneysel olasılık teorik olasılığa yaklaşır; bu yüzden çok tekrarlı deneyler daha güvenilirdir. Benzetim (simülasyon), deneyi bilgisayarla çok kez tekrarlamaktır."],
                [("Çark 50 kez çevrildi, 12 kez mavi", ["12 ÷ 50"], "12/50 = 6/25"), ("Olasılık 1/4, 200 deney", ["200 · 1/4"], "Yaklaşık 50 kez")],
                [["Deneysel olasılığı teorik olasılıkla aynı sanmak", "Az deneyde farklı çıkabilir"],
                 ["Öznel görüşü kesin bilgi sanmak", "Öznel olasılık kişiden kişiye değişir"],
                 ["Beklenen sayının kesin gerçekleşeceğini düşünmek", "Yaklaşık değerdir"]],
                [("Hangi yaklaşımı ne zaman kullanmalı?", "Çıktılar eşit olasılıklıysa teorik; bilinmiyorsa deney; veri yoksa öznel yaklaşım kullanılır."),
                 ("Benzetim (simülasyon) nedir?", "Bir deneyi bilgisayar ya da rastgele sayılarla çok kez taklit ederek sonuç toplamaktır."),
                 ("Hava durumu tahmini hangi yaklaşımdır?", "Geçmiş verilere ve modellere dayanır; deneysel olasılığa yakındır.")])


UNITS = [u13, u14, u15, u16, u17, u18, u19, u20, u21, u22, u23]
