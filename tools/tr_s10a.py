# -*- coding: utf-8 -*-
"""Türkiye 10. sınıf (2026 DÖP)：MAT.10.1 Geometrik Şekiller、MAT.10.2 İki kategorik değişken、MAT.10.3 Sayılar、MAT.10.4 fonksiyonlar（一部）。"""
import math
from fractions import Fraction as F
import tr_s9a
from tr_lise import *  # noqa: F401,F403
from tr_lise import dq, G, M, num, sn, par, lin, MINUS, ri, ch, sh, nz, named, kosy, kurve, figure, frs, TRIG, TRIP, U, W3, rts, rt, iv, poly, peval


def setup(rnd):
    tr_s9a.setup(rnd)


def sqs(n):
    o, i = rt(n)
    return rts(o, i) if i > 1 else str(o)


ORAN = {"sin": "sinüs", "cos": "kosinüs", "tan": "tanjant", "cot": "kotanjant"}


def dik(a, b, labs=("A", "B", "C"), sides=()):
    """B dik açı; |BC| = a yatay, |AB| = b dikey"""
    A, B, C = labs
    pts = {A: (0, b), B: (0, 0), C: (a, 0)}
    return figure(pts, [(A, B), (B, C), (C, A)], sides=sides, right=[(B, A, C)], label="dik üçgen")


# ============================================================ 1. dik üçgende trigonometrik oranlar
def u1():
    def oran():
        a, b, c = ch(TRIP)
        k = ri(1, 3)
        a, b, c = a * k, b * k, c * k
        f = ch(["sin", "cos", "tan", "cot"])
        # C açısı: karşı = |AB| = b, komşu = |BC| = a
        v = {"sin": F(b, c), "cos": F(a, c), "tan": F(b, a), "cot": F(a, b)}[f]
        ws = [sn(F(a, c)), sn(F(b, c)), sn(F(b, a)), sn(F(a, b)), sn(F(c, a))]
        fig = dik(a, b, sides=[("B", "C", "%d" % a), ("A", "B", "%d" % b), ("A", "C", "%d" % c)])
        return M("Şekildeki dik üçgende %s C kaçtır?%s" % (f, fig), sn(v), W3(ws, sn(v)),
                 "%s C = %s: <b>%s</b>." % (f, {"sin": "karşı dik kenar ÷ hipotenüs", "cos": "komşu dik kenar ÷ hipotenüs", "tan": "karşı ÷ komşu", "cot": "komşu ÷ karşı"}[f], sn(v)))

    def ozel():
        f = ch(["sin", "cos", "tan", "cot"])
        a = ch([30, 45, 60])
        g = TRIG[(f, a)]
        ws = [TRIG[(f2, a2)] for f2 in ("sin", "cos", "tan") for a2 in (30, 45, 60)]
        return M("%s %d° kaçtır?" % (f, a), g, W3(sh(ws), g), "Özel açılar tablosundan: %s %d° = <b>%s</b>." % (f, a, g))

    def ifade():
        a, b = ch([30, 45, 60]), ch([30, 45, 60])
        f1, f2 = ch([("sin", "cos"), ("tan", "cot"), ("sin", "sin"), ("cos", "cos")])
        from tr_lise import TVAL
        v = TVAL[(f1, a)] ** 2 + TVAL[(f2, b)] ** 2
        fv = F(round(v * 4), 4)
        if abs(float(fv) - v) > 1e-9:
            return None
        return M("%s²%d° + %s²%d° ifadesinin değeri kaçtır?" % (f1, a, f2, b), sn(fv), [sn(fv + F(1, 2)), sn(fv - F(1, 4)) if fv > F(1, 4) else sn(fv + 1), sn(fv * 2), "1" if fv != 1 else "2"],
                 "%s²%d° = %s, %s²%d° = %s. Toplam <b>%s</b>." % (f1, a, sn(F(round(TVAL[(f1, a)] ** 2 * 4), 4)), f2, b, sn(F(round(TVAL[(f2, b)] ** 2 * 4), 4)), sn(fv)))

    def kenar():
        a = ch([30, 45, 60])
        h = ri(2, 12) * 2
        k = ch(["karşı", "komşu"])
        if a == 45:
            g = "%d" % h if k == "karşı" else "%d" % h
            g = rts(h // 2, 2) if True else g
            q = "Hipotenüsü %s olan ikizkenar dik üçgende dik kenar kaçtır?" % rts(h // 2 * 2 // 2, 2) if False else "Bir dik üçgende hipotenüs %d cm ve bir dar açı 45°’dir. Dik kenarlardan biri kaç cm’dir?" % h
            return M(q, "%s cm" % rts(h // 2, 2), ["%d cm" % (h // 2), "%s cm" % rts(h, 2), "%d cm" % h], "sin 45° = √2/2 → %d · √2/2 = <b>%s cm</b>." % (h, rts(h // 2, 2)))
        opp = (a == 30) == (k == "karşı")
        g = "%d cm" % (h // 2) if opp else "%s cm" % rts(h // 2, 3)
        return M("Bir dik üçgende hipotenüs %d cm ve bir dar açının ölçüsü %d° olsun. Bu açının %s dik kenarı kaç cm’dir?" % (h, a, k), g,
                 W3(["%d cm" % (h // 2), "%s cm" % rts(h // 2, 3), "%s cm" % rts(h, 3), "%d cm" % h], g),
                 "30° karşısındaki kenar hipotenüsün yarısı, 60° karşısındaki kenar yarısının √3 katıdır: <b>%s</b>." % g)

    def tan_problem():
        a = ch([30, 45, 60])
        d = ri(2, 20) * 3
        h = {30: rts(d // 3, 3), 45: "%d" % d, 60: rts(d, 3)}[a]
        return M("Bir ağaçtan %d m uzaktaki noktadan ağacın tepesine bakış açısı %d° olarak ölçülüyor. Ağacın boyu kaç m’dir? (Göz yüksekliğini önemsemeyin.)" % (d, a), "%s m" % h,
                 W3(["%s m" % x for x in (rts(d // 3, 3), "%d" % d, rts(d, 3), "%d" % (d // 2))], "%s m" % h), "tan %d° = boy ÷ %d → boy = %d · tan %d° = <b>%s m</b>." % (a, d, d, a, h))

    sets = [("Oranlar", [(oran, 20)]), ("Özel açılar", [(ozel, 12), (oran, 8)]), ("Kenar bulma", [(kenar, 20)]),
            ("İfadelerin değeri", [(ifade, 20)]), ("Problemler", [(tan_problem, 20)])]
    return U(10, "dik-ucgende-trigonometrik-oranlar", "GS", "MAT.10.1.1", 1, "Dik Üçgende Trigonometrik Oranlar", "Trigonometrik Oranlar",
             "Dik üçgende trigonometrik oranlara (sinüs, kosinüs, tanjant, kotanjant) ilişkin çıkarım yapar; 30°, 45° ve 60° özel açılarının oranlarını kullanır.",
             "sinüs, kosinüs, tanjant ve kotanjant oranları, 30°, 45° ve 60° özel açıları, kenar bulma, yükseklik problemleri",
             "sin = karşı ÷ hipotenüs", "cos = komşu ÷ hipotenüs, tan = karşı ÷ komşu.", sets,
             ["Dik üçgende bir dar açının sinüsü karşı dik kenarın hipotenüse, kosinüsü komşu dik kenarın hipotenüse oranıdır.",
              "Tanjant karşı dik kenarın komşu dik kenara, kotanjant komşu dik kenarın karşı dik kenara oranıdır.",
              "Özel açılar: sin 30° = 1/2, sin 45° = √2/2, sin 60° = √3/2; cos değerleri ters sıradadır."],
             [("Kenarlar 3, 4, 5; 3 karşı kenar", ["sin = 3/5", "cos = 4/5"], "tan = 3/4"), ("Hipotenüs 10, açı 30°", ["Karşı kenar 10 ÷ 2"], "5")],
             [["Karşı ile komşu kenarı karıştırmak", "Açının karşısındaki kenar karşı kenardır"], ["sin 30° ile sin 60°’ı karıştırmak", "sin 30° = 1/2"],
              ["Hipotenüsü dik kenar sanmak", "Hipotenüs dik açının karşısındadır"]],
             [("Trigonometrik oranlar açının büyüklüğüne mi bağlıdır?", "Evet; üçgen büyüse de aynı açı için oranlar değişmez (benzerlik)."),
              ("cot ile tan ilişkisi nedir?", "cot x = 1 ÷ tan x."), ("Nerede kullanılır?", "Yükseklik, eğim ve uzaklık ölçümünde.")])


# ============================================================ 2. özdeşlikler
def u2():
    def tamamla():
        a, b, c = ch(TRIP)
        f = ch(["sin", "cos"])
        g = ch(["cos", "tan", "cot"]) if f == "sin" else ch(["sin", "tan", "cot"])
        sv, cv = F(a, c), F(b, c)
        given = sv if f == "sin" else cv
        val = {"sin": sv, "cos": cv, "tan": sv / cv, "cot": cv / sv}[g]
        return M("x dar açı ve %s x = %s ise %s x kaçtır?" % (f, sn(given), g), sn(val), W3([sn(sv), sn(cv), sn(sv / cv), sn(cv / sv), sn(1 - given)], sn(val)),
                 "sin²x + cos²x = 1 ile diğer oran bulunur: sin x = %s, cos x = %s → %s x = <b>%s</b>." % (sn(sv), sn(cv), g, sn(val)))

    def ozdeslik():
        S = [("sin²x + cos²x", "1"), ("tan x · cot x", "1"), ("sin x ÷ cos x", "tan x"), ("cos x ÷ sin x", "cot x"), ("1 − sin²x", "cos²x"),
             ("1 − cos²x", "sin²x"), ("sin(90° − x)", "cos x"), ("cos(90° − x)", "sin x"), ("tan(90° − x)", "cot x"), ("(sin x + cos x)² − 2 sin x cos x", "1"),
             ("sin²x ÷ (1 − cos²x)", "1"), ("tan x · cos x", "sin x")]
        q, g = ch(S)
        return M("x dar açı olmak üzere %s ifadesi neye eşittir?" % q, g, W3(sh(["1", "0", "tan x", "cot x", "sin x", "cos x", "sin²x", "cos²x"]), g)[:3],
                 "Temel özdeşlikler: sin²x + cos²x = 1, tan x = sin x ÷ cos x, sin(90° − x) = cos x. Cevap: <b>%s</b>." % g)

    def tumler():
        a = ri(5, 85)
        f = ch(["sin", "cos", "tan", "cot"])
        g = {"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan"}[f]
        return M("%s %d° hangisine eşittir?" % (f, a), "%s %d°" % (g, 90 - a), ["%s %d°" % (f, 90 - a), "%s %d°" % (g, a), "%s %d°" % (g, 180 - a)],
                 "Tümler açıların oranları: %s x = %s(90° − x). Cevap: <b>%s %d°</b>." % (f, g, g, 90 - a))

    def deger():
        a = ri(10, 80)
        k = ch([0, 1])
        if k == 0:
            g = "1"
            return M("sin²%d° + sin²%d° ifadesinin değeri kaçtır?" % (a, 90 - a), g, ["2", "0", "sin 90°" if False else "1/2"], "sin %d° = cos %d° → sin² + cos² = <b>1</b>." % (90 - a, a))
        return M("tan %d° · tan %d° ifadesinin değeri kaçtır?" % (a, 90 - a), "1", ["0", "2", "tan 90°"], "tan %d° = cot %d° ve tan · cot = <b>1</b>." % (90 - a, a))

    sets = [("Bir orandan diğerleri", [(tamamla, 20)]), ("Temel özdeşlikler", [(ozdeslik, 12), (deger, 8)]), ("Tümler açılar", [(tumler, 20)]),
            ("Değer hesaplama", [(deger, 12), (tamamla, 8)]), ("Karışık", [(tumler, 10), (deger, 10)])]
    return U(10, "trigonometrik-ozdeslikler", "GS", "MAT.10.1.1", 2, "Trigonometrik Özdeşlikler", "Trigonometrik Özdeşlikler",
             "Dik üçgende trigonometrik oranlar arasındaki özdeşliklere (sin²x + cos²x = 1, tan x · cot x = 1, tümler açıların oranları) ilişkin çıkarım yapar.",
             "sin²x + cos²x = 1, tan x · cot x = 1, bir orandan diğerlerini bulma, tümler açıların oranları",
             "sin²x + cos²x = 1", "tan x = sin x ÷ cos x; sin(90° − x) = cos x.", sets,
             ["Pisagor bağıntısından sin²x + cos²x = 1 elde edilir.",
              "tan x = sin x ÷ cos x ve cot x = cos x ÷ sin x olduğundan tan x · cot x = 1’dir.",
              "Tümler açılarda bir açının sinüsü diğerinin kosinüsüne, tanjantı diğerinin kotanjantına eşittir."],
             [("sin x = 3/5", ["cos x = 4/5"], "tan x = 3/4"), ("sin 20° ÷ cos 70°", ["cos 70° = sin 20°"], "1")],
             [["sin²x’i sin(x²) sanmak", "sin²x = (sin x)²"], ["cos x’i 1 − sin x sanmak", "cos²x = 1 − sin²x"], ["Tümler yerine bütünler açı almak", "Tümler: toplam 90°"]],
             [("Özdeşlik ile denklem farkı nedir?", "Özdeşlik her x için doğrudur; denklem belirli değerlerde sağlanır."),
              ("Neden dar açı?", "Bu yıl oranlar dik üçgende, yani dar açılar için tanımlanır."), ("Özdeşlikler ne işe yarar?", "İfadeleri sadeleştirmeye ve bilinmeyen oranları bulmaya.")])


# ============================================================ 3. yardımcı elemanlar
def u3():
    def agirlik():
        m = ri(2, 15) * 3
        k = ch([0, 1, 2])
        if k == 0:
            return M("Bir üçgende |AD| kenarortayının uzunluğu %d cm’dir. G ağırlık merkezi ise |AG| kaç cm’dir?" % m, "%d cm" % (2 * m // 3), W3(["%d cm" % (m // 3), "%d cm" % (m // 2) if m % 2 == 0 else "%d cm" % (m - 1), "%d cm" % m], "%d cm" % (2 * m // 3)),
                     "Ağırlık merkezi kenarortayı köşeden itibaren 2 : 1 böler: <b>%d cm</b>." % (2 * m // 3))
        if k == 1:
            return M("Bir üçgende G ağırlık merkezi ve |GD| = %d cm’dir ([AD] kenarortay). |AD| kaç cm’dir?" % (m // 3), "%d cm" % m, W3(["%d cm" % (2 * m // 3), "%d cm" % (m // 3 * 2 + 1), "%d cm" % (m // 3 * 4)], "%d cm" % m),
                     "|AG| = 2|GD| = %d, |AD| = %d + %d = <b>%d cm</b>." % (2 * m // 3, 2 * m // 3, m // 3, m))
        return M("Bir üçgende G ağırlık merkezi ve |AG| = %d cm’dir ([AD] kenarortay). |GD| kaç cm’dir?" % (2 * m // 3), "%d cm" % (m // 3), W3(["%d cm" % m, "%d cm" % (2 * m // 3), "%d cm" % (m // 3 + 2)], "%d cm" % (m // 3)),
                 "|GD| = |AG| ÷ 2 = <b>%d cm</b>." % (m // 3))

    def aciortay():
        b, c = ri(3, 15), ri(3, 15)
        if b == c:
            return None
        a = ri(abs(b - c) + 1, b + c - 1)
        x = F(a * c, b + c)
        if x.denominator != 1:
            return None
        return M("ABC üçgeninde [AD] iç açıortay, |AB| = %d, |AC| = %d, |BC| = %d olsun. |BD| kaçtır?" % (c, b, a) if False else "ABC üçgeninde [AD] iç açıortaydır. |AB| = %d cm, |AC| = %d cm, |BC| = %d cm ise |BD| kaç cm’dir?" % (c, b, a),
                 "%s cm" % sn(x), W3(["%s cm" % sn(F(a * b, b + c)), "%s cm" % sn(F(a, 2)), "%s cm" % sn(x + 1)], "%s cm" % sn(x)),
                 "İç açıortay teoremi: |BD| ÷ |DC| = |AB| ÷ |AC| = %d ÷ %d → |BD| = %d · %d ÷ %d = <b>%s cm</b>." % (c, b, a, c, b + c, sn(x)))

    def kenarortay_dik():
        a, b, c = ch(TRIP)
        k = ri(1, 9)
        c = c * k
        if c % 2:
            return None
        return M("Bir dik üçgende hipotenüs %d cm’dir. Hipotenüse ait kenarortay kaç cm’dir?" % c, "%d cm" % (c // 2), W3(["%d cm" % c, "%d cm" % (c // 3) if c % 3 == 0 else "%d cm" % (c // 2 + 1), "%d cm" % (c * 2)], "%d cm" % (c // 2)),
                 "Dik üçgende hipotenüse ait kenarortay hipotenüsün yarısıdır: <b>%d cm</b>." % (c // 2))

    def tani():
        S = [("Kenarortayların kesim noktası", "Ağırlık merkezi"), ("İç açıortayların kesim noktası", "İç teğet çemberin merkezi"),
             ("Kenar orta dikmelerinin kesim noktası", "Çevrel çemberin merkezi"), ("Yüksekliklerin kesim noktası", "Diklik merkezi")]
        t, g = ch(S)
        return M("%s neyi verir?" % t, g, [x for _, x in S if x != g], "Cevap: <b>%s</b>." % g)

    def yukseklik():
        a, b, c = ch(TRIP)
        k = ri(1, 6)
        a, b, c = a * k, b * k, c * k
        h = F(a * b, c)
        return M("Dik kenarları %d cm ve %d cm olan dik üçgende hipotenüse ait yükseklik kaç cm’dir?" % (a, b), "%s cm" % (sn(h) if h.denominator == 1 else dq(h, 1) if (h * 10).denominator == 1 else sn(h)),
                 W3(["%s cm" % sn(F(a + b, 2)), "%s cm" % sn(F(c, 2)), "%s cm" % sn(F(a * b, 2))], None), "Alan iki yoldan: %d · %d ÷ 2 = %d · h ÷ 2 → h = %d · %d ÷ %d = <b>%s cm</b>." % (a, b, c, a, b, c, sn(h) if h.denominator == 1 else dq(h, 1) if (h * 10).denominator == 1 else sn(h)))

    sets = [("Ağırlık merkezi", [(agirlik, 20)]), ("İç açıortay teoremi", [(aciortay, 20)]), ("Dik üçgende kenarortay", [(kenarortay_dik, 10), (tani, 4), (agirlik, 6)]),
            ("Hipotenüse ait yükseklik", [(yukseklik, 20)]), ("Karışık", [(aciortay, 10), (yukseklik, 10)])]
    return U(10, "ucgende-yardimci-elemanlar", "GS", "MAT.10.1.2", 3, "Üçgende Yardımcı Elemanlar: Kenarortay, Açıortay, Yükseklik", "Yardımcı Elemanlar",
             "Üçgenin yardımcı elemanlarının (kenarortay, açıortay, yükseklik, kenar orta dikme) özellikleri ile ilgili çıkarım yapar.",
             "ağırlık merkezi ve 2 : 1 oranı, iç açıortay teoremi, dik üçgende hipotenüse ait kenarortay, hipotenüse ait yükseklik, özel noktalar",
             "Ağırlık merkezi kenarortayı 2 : 1 böler", "İç açıortay karşı kenarı komşu kenarlar oranında böler.", sets,
             ["Kenarortaylar ağırlık merkezinde kesişir; ağırlık merkezi her kenarortayı köşeden itibaren 2 : 1 oranında böler.",
              "İç açıortay karşı kenarı, açıyı oluşturan kenarların oranında böler: |BD| ÷ |DC| = |AB| ÷ |AC|.",
              "Dik üçgende hipotenüse ait kenarortay hipotenüsün yarısıdır. Yüksekliği alanı iki yoldan yazarak buluruz."],
             [("|AD| = 12, G ağırlık merkezi", ["|AG| = 8, |GD| = 4"], "8 cm"), ("|AB| = 6, |AC| = 9, |BC| = 10", ["|BD| = 10 · 6 ÷ 15"], "4 cm")],
             [["Ağırlık merkezini kenarortayın ortası sanmak", "Oran 2 : 1"], ["Açıortay teoreminde kenarları ters eşlemek", "|BD|, |AB| ile orantılıdır"],
              ["Yüksekliği kenarortayla karıştırmak", "Yükseklik karşı kenara diktir"]],
             [("Ağırlık merkezi neden önemlidir?", "Üçgen biçimli bir levha bu noktadan tek parmakla dengede tutulabilir."),
              ("Çevrel çemberin merkezi nerededir?", "Kenar orta dikmelerin kesiştiği noktadadır."), ("Açıortay üzerindeki noktaların özelliği?", "Açının kollarına eşit uzaklıktadır.")])


# ============================================================ 4. üçgenin alanı
def u4():
    def taban():
        a, h = ri(3, 20), ri(2, 20)
        S = F(a * h, 2)
        return M("Taban uzunluğu %d cm ve bu tabana ait yüksekliği %d cm olan üçgenin alanı kaç cm²’dir?" % (a, h), sn(S), W3([sn(a * h), sn(a + h), sn(S + a)], sn(S)), "A = a · h ÷ 2 = %d · %d ÷ 2 = <b>%s</b>." % (a, h, sn(S)))

    def sinus():
        b, c = ri(2, 14), ri(2, 14)
        a = ch([30, 150, 90])
        S = F(b * c, 4) if a != 90 else F(b * c, 2)
        return M("İki kenarı %d cm ve %d cm, bu kenarlar arasındaki açı %d° olan üçgenin alanı kaç cm²’dir?" % (b, c, a), sn(S), W3([sn(b * c), sn(F(b * c, 2)), sn(F(b * c, 8))], sn(S)),
                 "A = ½ · %d · %d · sin %d° = ½ · %d · %s = <b>%s</b>." % (b, c, a, b * c, {30: "½", 150: "½", 90: "1"}[a], sn(S)))

    def degisim():
        k1, k2 = ch([2, 3, F(1, 2)]), ch([2, 3, F(1, 2), 1])
        A = ri(4, 30) * 4
        newA = A * k1 * k2
        if newA.denominator != 1 if isinstance(newA, F) else False:
            return None
        newA = F(newA)
        if newA.denominator != 1:
            return None
        t1 = {2: "2 katına çıkarılıyor", 3: "3 katına çıkarılıyor", F(1, 2): "yarıya indiriliyor"}[k1]
        t2 = {2: "2 katına çıkarılıyor", 3: "3 katına çıkarılıyor", F(1, 2): "yarıya indiriliyor", 1: "değiştirilmiyor"}[k2]
        return M("Alanı %d cm² olan bir üçgenin tabanı %s, bu tabana ait yüksekliği %s. Yeni alan kaç cm²’dir?" % (A, t1, t2), sn(newA), W3([sn(A * F(k1)), sn(A * F(k2)), sn(A * (F(k1) + F(k2))), sn(A)], sn(newA)),
                 "Alan taban ile yüksekliğin çarpımıyla orantılıdır: %d · %s · %s = <b>%s</b>." % (A, sn(F(k1)), sn(F(k2)), sn(newA)))

    def koordinat():
        x1, y1, x2, y2, x3, y3 = [ri(-5, 5) for _ in range(6)]
        S2 = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if S2 == 0:
            return None
        S = F(S2, 2)
        pts = [(x1, y1, "A"), (x2, y2, "B"), (x3, y3, "C")]
        return M("Köşeleri A(%s, %s), B(%s, %s), C(%s, %s) olan üçgenin alanı kaç birimkaredir?" % (sn(x1), sn(y1), sn(x2), sn(y2), sn(x3), sn(y3)), sn(S), W3([sn(S2), sn(S + 1), sn(S * 2 + 1)], sn(S)),
                 "Üçgeni bir dikdörtgenin içine yerleştirip dışta kalan dik üçgenleri çıkarırız ya da ½|x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)| = <b>%s</b>." % sn(S))

    def oran():
        a, b = ri(2, 9), ri(2, 9)
        if math.gcd(a, b) != 1:
            return None
        A = ri(2, 10) * (a + b)
        x = F(A * a, a + b)
        return M("ABC üçgeninde D noktası [BC] üzerindedir ve |BD| : |DC| = %d : %d olsun. A(ABC) = %d cm² ise A(ABD) kaç cm²’dir?" % (a, b, A), sn(x), W3([sn(F(A * b, a + b)), sn(F(A, 2)), sn(x + a)], sn(x)),
                 "Yükseklikleri ortak olan üçgenlerin alanları tabanlarıyla orantılıdır: %d · %d ÷ %d = <b>%s</b>." % (A, a, a + b, sn(x)))

    sets = [("Taban ve yükseklik", [(taban, 20)]), ("İki kenar ve aradaki açı", [(sinus, 20)]), ("Alanın değişimi", [(degisim, 20)]),
            ("Ortak yükseklik", [(oran, 20)]), ("Koordinatlarda alan", [(koordinat, 20)])]
    return U(10, "ucgenin-alani", "GS", "MAT.10.1.3", 4, "Üçgenin Alanı ve Alanın Değişimi", "Üçgenin Alanı",
             "Üçgenin bir kenarı ve o kenara ait yüksekliğinin değişimine bağlı olarak alanının değişimine ilişkin çıkarım yapar; alanı farklı yollarla hesaplar.",
             "taban ve yükseklikle alan, iki kenar ve aradaki açıyla alan, taban ve yükseklik değişince alanın değişimi, ortak yükseklikli üçgenler, koordinatlarda alan",
             "A = taban × yükseklik ÷ 2", "A = ½ · b · c · sin A.", sets,
             ["Üçgenin alanı bir kenar ile o kenara ait yüksekliğin çarpımının yarısıdır.",
              "İki kenar ve aradaki açı biliniyorsa A = ½ · b · c · sin A kullanılır.",
              "Taban k katına, yükseklik m katına çıkarsa alan k · m katına çıkar. Yükseklikleri ortak üçgenlerin alanları tabanlarıyla orantılıdır."],
             [("Taban 8, yükseklik 5", ["8 · 5 ÷ 2"], "20"), ("Kenarlar 6 ve 10, açı 30°", ["½ · 6 · 10 · ½"], "15")],
             [["Yarıya bölmeyi unutmak", "Alan = a · h ÷ 2"], ["Yüksekliği başka kenara ait almak", "Yükseklik tabana dik olmalı"], ["Alanı taban kadar değiştirmek", "Hem taban hem yükseklik etkiler"]],
             [("Geniş açılı üçgende yükseklik nerede?", "Tabanın uzantısı üzerine düşebilir."), ("sin 150° neden ½?", "sin(180° − x) = sin x olduğundan."),
              ("Alan birimi nedir?", "Uzunluk birimi cm ise alan birimi cm²’dir.")])


# ============================================================ 5. sinüs ve kosinüs teoremleri
def u5():
    def kosinus():
        b, c = ri(2, 10), ri(2, 10)
        A = ch([60, 120, 90])
        a2 = b * b + c * c - {60: b * c, 120: -b * c, 90: 0}[A]
        o, i = rt(a2)
        g = rts(o, i) if i > 1 else str(o)
        return M("ABC üçgeninde |AB| = %d, |AC| = %d ve m(A) = %d° olsun. |BC| kaçtır?" % (c, b, A), g, W3([str(b + c), sqs(b * b + c * c), sqs(a2 + b * c), sqs(a2 + 2 * b * c), str(abs(b - c) + 1)], g),
                 "a² = b² + c² − 2bc · cos A = %d + %d − 2 · %d · %d · %s = %d → a = <b>%s</b>." % (b * b, c * c, b, c, {60: "½", 120: "(−½)", 90: "0"}[A], a2, g))

    def sinus():
        A, B = ch([(30, 90), (30, 60), (45, 90), (90, 30), (60, 90), (30, 45), (45, 30)])
        from tr_lise import TVAL
        a = ri(2, 12) * 2
        sA = {30: F(1, 2), 90: F(1), 60: None, 45: None}[A]
        if A == 30 and B in (90, 60, 45):
            if B == 90:
                g = str(2 * a)
            elif B == 60:
                g = rts(a, 3)
            else:
                g = rts(a, 2)
        elif A == 45 and B == 90:
            g = rts(a, 2)
        elif A == 45 and B == 30:
            g = rts(a, 2) if False else (rts(a // 2, 2) if a % 2 == 0 else None)
        elif A == 90 and B == 30:
            g = str(a // 2)
        elif A == 60 and B == 90:
            g = rts(F(2 * a, 3) if False else a * 2, 3) if False else None
            if (2 * a) % 3:
                return None
            g = rts(2 * a // 3, 3)
        else:
            return None
        if g is None:
            return None
        return M("ABC üçgeninde m(A) = %d°, m(B) = %d° ve |BC| = a = %d olsun. |AC| = b kaçtır?" % (A, B, a), g, W3([str(a), str(2 * a), rts(a, 3), rts(a, 2), str(a // 2)], g),
                 "Sinüs teoremi: a ÷ sin A = b ÷ sin B → b = a · sin %d° ÷ sin %d° = <b>%s</b>." % (B, A, g))

    def cevrel():
        A = ch([30, 90, 150])
        a = ri(2, 15)
        R = F(a, 2) / {30: F(1, 2), 90: F(1), 150: F(1, 2)}[A]
        return M("Bir üçgende m(A) = %d° ve |BC| = %d ise çevrel çemberin yarıçapı kaçtır?" % (A, a), sn(R), W3([sn(R * 2), sn(F(a, 2)), sn(R + 1)], sn(R)),
                 "a ÷ sin A = 2R → 2R = %d ÷ %s → R = <b>%s</b>." % (a, {30: "½", 90: "1", 150: "½"}[A], sn(R)))

    def aci_bul():
        a, b, c = ch([(7, 5, 8), (7, 3, 8), (13, 7, 15), (19, 5, 21), (7, 8, 3), (13, 8, 15), (31, 11, 35), (3, 5, 7), (7, 5, 3), (13, 7, 8)])
        k = ri(1, 3)
        a, b, c = a * k, b * k, c * k
        cosA = F(b * b + c * c - a * a, 2 * b * c)
        ang = {F(1, 2): 60, F(-1, 2): 120, F(0): 90}.get(cosA)
        if ang is None:
            return None
        return M("Kenar uzunlukları a = %d, b = %d, c = %d olan üçgende A açısı kaç derecedir?" % (a, b, c), "%d°" % ang, W3(["%d°" % x for x in (30, 45, 60, 90, 120, 150)], "%d°" % ang)[:3],
                 "cos A = (b² + c² − a²) ÷ 2bc = %s → m(A) = <b>%d°</b>." % (sn(cosA), ang))

    sets = [("Kosinüs teoremi", [(kosinus, 20)]), ("Sinüs teoremi", [(sinus, 20)]), ("Çevrel çember", [(cevrel, 20)]),
            ("Açı bulma", [(aci_bul, 10), (kosinus, 10)]), ("Karışık", [(sinus, 7), (cevrel, 7), (kosinus, 6)])]
    return U(10, "sinus-ve-kosinus-teoremleri", "GS", "MAT.10.1.4", 5, "Sinüs ve Kosinüs Teoremleri", "Sinüs ve Kosinüs Teoremleri",
             "Sinüs ve kosinüs teoremlerini doğrular veya ispatlar; herhangi bir üçgende kenar ve açı bulmak için kullanır.",
             "kosinüs teoremiyle kenar ve açı bulma, sinüs teoremiyle kenar bulma, çevrel çemberin yarıçapı",
             "a² = b² + c² − 2bc · cos A", "a ÷ sin A = b ÷ sin B = 2R.", sets,
             ["Kosinüs teoremi: a² = b² + c² − 2bc · cos A. A = 90° ise Pisagor teoremine dönüşür.",
              "Sinüs teoremi: a ÷ sin A = b ÷ sin B = c ÷ sin C = 2R (R çevrel çemberin yarıçapı).",
              "İki kenar ve aradaki açı verilince kosinüs, iki açı ve bir kenar verilince sinüs teoremi kullanılır."],
             [("b = 3, c = 5, A = 120°", ["9 + 25 + 15 = 49"], "a = 7"), ("A = 30°, a = 6", ["2R = 6 ÷ ½ = 12"], "R = 6")],
             [["cos 120°’yi pozitif almak", "cos 120° = −½"], ["Sinüs teoreminde kenarı karşı açısıyla eşlememek", "a, A açısının karşısındadır"],
              ["2R yerine R yazmak", "a ÷ sin A = 2R"]],
             [("Kosinüs teoremi Pisagor’la nasıl ilişkili?", "A = 90° iken cos A = 0 olur ve a² = b² + c² kalır."), ("Hangi teoremi seçerim?", "Verilenlere göre: iki kenar + aradaki açı → kosinüs."),
              ("Nerede kullanılır?", "Haritacılık, denizcilik ve mühendislikte uzaklık hesaplamada.")])


# ============================================================ 6. iki kategorik değişken
def u6():
    CAT = [("Kız", "Erkek", "Spor yapıyor", "Spor yapmıyor"), ("9. sınıf", "10. sınıf", "Kitap okuyor", "Kitap okumuyor"),
           ("Sabah grubu", "Öğle grubu", "Sınavı geçti", "Sınavı geçemedi"), ("A okulu", "B okulu", "Servisle geliyor", "Yürüyerek geliyor")]

    def tablo():
        r1, r2, c1, c2 = ch(CAT)
        a, b, c, d = [ri(5, 60) for _ in range(4)]
        t = "<table class='sn-table' style='width:auto'><thead><tr><th></th><th>%s</th><th>%s</th></tr></thead><tbody><tr><td>%s</td><td>%d</td><td>%d</td></tr><tr><td>%s</td><td>%d</td><td>%d</td></tr></tbody></table>" % (c1, c2, r1, a, b, r2, c, d)
        k = ri(0, 3)
        if k == 0:
            v = F(a, a + b)
            return M("İki yönlü tablo:%s%s arasında “%s” olanların oranı kaçtır?" % (t, r1, c1.lower()), sn(v), W3([sn(F(a, a + c)), sn(F(a, a + b + c + d)), sn(F(b, a + b))], sn(v)),
                     "%s satırının toplamı %d; oran %d ÷ %d = <b>%s</b>." % (r1, a + b, a, a + b, sn(v)))
        if k == 1:
            v = F(a, a + c)
            return M("İki yönlü tablo:%s“%s” olanlar arasında %s oranı kaçtır?" % (t, c1, r1), sn(v), W3([sn(F(a, a + b)), sn(F(a, a + b + c + d)), sn(F(c, a + c))], sn(v)),
                     "%s sütununun toplamı %d; oran %d ÷ %d = <b>%s</b>." % (c1, a + c, a, a + c, sn(v)))
        if k == 2:
            n = a + b + c + d
            v = F(c + d, n)
            return M("İki yönlü tablo:%sTüm grupta %s oranı kaçtır?" % (t, r2), sn(v), W3([sn(F(c, n)), sn(F(a + b, n)), sn(F(c + d, a + b))], sn(v)), "(%d + %d) ÷ %d = <b>%s</b>." % (c, d, n, sn(v)))
        p1, p2 = F(a, a + b), F(c, c + d)
        if p1 == p2:
            return None
        g = r1 if p1 > p2 else r2
        return M("İki yönlü tablo:%sHangi grupta “%s” olanların oranı daha yüksektir?" % (t, c1.lower()), g, [r2 if g == r1 else r1, "İki grupta eşit", "Bilinemez"],
                 "Sayılar değil oranlar karşılaştırılır: %s %s, %s %s → <b>%s</b>." % (r1, sn(p1), r2, sn(p2), g))

    def iliski():
        r1, r2, c1, c2 = ch(CAT)
        a, b = ri(10, 40), ri(10, 40)
        k = ri(1, 4)
        same = ri(0, 1)
        c, d = (a * k, b * k) if same else (a * k + ri(10, 30), b * k)
        p1, p2 = F(a, a + b), F(c, c + d)
        g = "İlişki yoktur; oranlar eşittir" if p1 == p2 else "İlişki vardır; oranlar farklıdır"
        t = "<table class='sn-table' style='width:auto'><thead><tr><th></th><th>%s</th><th>%s</th></tr></thead><tbody><tr><td>%s</td><td>%d</td><td>%d</td></tr><tr><td>%s</td><td>%d</td><td>%d</td></tr></tbody></table>" % (c1, c2, r1, a, b, r2, c, d)
        return M("Tabloya göre iki değişken arasında ilişki var mıdır?%s" % t, g, [("İlişki vardır; oranlar farklıdır" if p1 == p2 else "İlişki yoktur; oranlar eşittir"), "Sayılar farklı olduğu için kesin ilişki vardır", "Tablodan karar verilemez"],
                 "%s: %s, %s: %s. Cevap: <b>%s</b>." % (r1, sn(p1), r2, sn(p2), g))

    def yorum():
        S = [("Bir haberde “Kafeteryada yemek yiyen öğrencilerin 60’ı başarılı” deniyor; toplam sayı verilmemiş.", "Oran verilmediği için yorum eksiktir"),
             ("Bir araştırmada yalnızca bir sınıfın verisiyle bütün okul hakkında sonuç çıkarılmış.", "Örneklem okulu temsil etmeyebilir"),
             ("İki grubun sayıları farklıyken yalnızca sıklıklar karşılaştırılmış.", "Oranlar karşılaştırılmalıydı"),
             ("İki değişken arasında ilişki bulunca biri diğerinin nedeni denmiş.", "İlişki neden-sonuç anlamına gelmez")]
        t, g = ch(S)
        return M("“%s” Bu yorumdaki sorun nedir?" % t, g, [x for _, x in S if x != g], "Cevap: <b>%s</b>." % g)

    sets = [("Tablo okuma", [(tablo, 20)]), ("Oranlarla karşılaştırma", [(tablo, 20)]), ("İlişki var mı?", [(iliski, 20)]),
            ("Yorumları değerlendirme", [(yorum, 4), (iliski, 16)]), ("Karışık", [(tablo, 10), (iliski, 10)])]
    return U(10, "iki-kategorik-degiskenli-veri", "IA", "MAT.10.2.1, MAT.10.2.2", 6, "İki Kategorik Değişkenli Veri ve İki Yönlü Tablolar", "İki Kategorik Değişken",
             "İki kategorik değişkenli veri ile çalışır; iki yönlü tablolarda oranları karşılaştırarak değişkenler arasındaki ilişkililiğe dayalı karar verir ve başkalarının yorumlarını tartışır.",
             "iki yönlü tablo okuma, satır ve sütun oranları, gruplar arası karşılaştırma, ilişkililik, istatistiksel yorumları değerlendirme",
             "Sayıları değil oranları karşılaştır", "Oranlar eşitse değişkenler arasında ilişki yoktur.", sets,
             ["İki kategorik değişken iki yönlü tabloyla gösterilir; satır ve sütun toplamları önemlidir.",
              "Gruplar farklı büyüklükteyse sıklıklar değil oranlar karşılaştırılır.",
              "Gruplarda oranlar farklıysa değişkenler arasında ilişki vardır; ilişki neden-sonuç demek değildir."],
             [("Kız 30/50, erkek 20/50 spor yapıyor", ["0,6 ile 0,4"], "Kızlarda oran yüksek"), ("Oranlar 1/3 ve 1/3", ["Eşit"], "İlişki yok")],
             [["Sıklıkları karşılaştırmak", "Oranları karşılaştır"], ["Yanlış toplama bölmek", "Satır mı sütun mu, soruya bak"], ["İlişkiyi neden sanmak", "İlişki ≠ neden"]],
             [("İki yönlü tablo nedir?", "İki kategorik değişkenin birlikte sıklıklarını gösteren tablodur."), ("Koşullu oran nedir?", "Bir grubun içindeki oranıdır."),
              ("Bu konu neye hazırlar?", "Koşullu olasılık ve Bayes teoremine.")])


# ============================================================ 7–9. sayılar
def u7():
    def carpan():
        ps = sh([2, 3, 5, 7])[:ri(2, 3)]
        es = [ri(1, 3) for _ in ps]
        n = 1
        for p, e in zip(ps, es):
            n *= p ** e
        if n > 5000:
            return None
        fs = " · ".join("%d%s" % (p, "" if e == 1 else str(e).translate(str.maketrans("23", "²³"))) for p, e in sorted(zip(ps, es)))
        k = ri(0, 2)
        if k == 0:
            w = [" · ".join("%d%s" % (p, "" if e == 1 else str(e + 1).translate(str.maketrans("234", "²³⁴"))) for p, e in sorted(zip(ps, es)))]
            return M("%s sayısının asal çarpanlarına ayrılmış hâli hangisidir?" % num(n), fs, W3(w + [" · ".join(str(p) for p in sorted(ps)), "%d · %d" % (sorted(ps)[0], n // sorted(ps)[0])], fs),
                     "%s = <b>%s</b>." % (num(n), fs))
        d = 1
        for e in es:
            d *= e + 1
        if k == 1:
            return M("%s sayısının kaç tane pozitif böleni vardır?" % num(n), num(d), W3([num(d - 1), num(d + 2), num(sum(es)), num(d * 2)], num(d)),
                     "%s = %s → (%s) = <b>%d</b>." % (num(n), fs, ") · (".join("%d + 1" % e for e in es), d))
        s = 1
        for p, e in zip(ps, es):
            s *= (p ** (e + 1) - 1) // (p - 1)
        return M("%s sayısının pozitif bölenlerinin toplamı kaçtır?" % num(n), num(s), W3([num(s - n), num(s + 1), num(n + 1)], num(s)),
                 "Her asal çarpan için 1 + p + … + pᵉ çarpılır: <b>%s</b>." % num(s))

    def kare():
        p, q = sh([2, 3, 5, 7])[:2]
        a, b = ri(1, 4), ri(1, 4)
        n = p ** a * q ** b
        if n > 3000 or (a % 2 == 0 and b % 2 == 0):
            return None
        k = (p if a % 2 else 1) * (q if b % 2 else 1)
        return M("%s · x bir tam kare sayı olduğuna göre x’in alabileceği en küçük pozitif tam sayı kaçtır?" % num(n), num(k), W3([num(n), num(k * 4), num(p * q) if p * q != k else num(k * 2), "1"], num(k)),
                 "Asal çarpanların üsleri çift olmalı: %s → x = <b>%d</b>." % (num(n), k))

    sets = [("Asal çarpanlar", [(carpan, 20)]), ("Bölen sayısı", [(carpan, 20)]), ("Bölenlerin toplamı", [(carpan, 20)]),
            ("Tam kare yapma", [(kare, 20)]), ("Karışık", [(carpan, 10), (kare, 10)])]
    return U(10, "asal-carpanlar-ve-bolenler", "SY", "MAT.10.3.1", 7, "Asal Çarpanlar ve Bölenler", "Asal Çarpanlar ve Bölenler",
             "Bir doğal sayı ile asal çarpanları ve bölenleri arasındaki ilişkilere dair çıkarım yapar; pozitif bölen sayısını ve bölenlerin toplamını bulur.",
             "asal çarpanlara ayırma, pozitif bölen sayısı, bölenlerin toplamı, bir sayıyı tam kare yapma",
             "Her doğal sayı asalların çarpımıdır", "n = pᵃ · qᵇ → bölen sayısı (a + 1)(b + 1).", sets,
             ["1’den büyük her doğal sayı asal sayıların çarpımı biçiminde tek türlü yazılır.",
              "n = pᵃ · qᵇ · rᶜ ise pozitif bölen sayısı (a + 1)(b + 1)(c + 1)’dir.",
              "Bir sayının tam kare olması için asal çarpanlarının bütün üsleri çift olmalıdır."],
             [("72", ["2³ · 3²", "(3 + 1)(2 + 1)"], "12 bölen"), ("12 · x tam kare", ["2² · 3", "3 eksik"], "x = 3")],
             [["Üslere 1 eklemeyi unutmak", "(a + 1)(b + 1)"], ["1’i asal saymak", "1 asal değildir"], ["Asal olmayan çarpanla bırakmak", "Bütün çarpanlar asal olmalı"]],
             [("Neden tek türlü yazılır?", "Aritmetiğin temel teoremi bunu garanti eder."), ("Tam bölen sayısı nasıl kontrol edilir?", "Bölenleri çiftler hâlinde yazabilirsin."),
              ("Asal sayılar sonsuz mudur?", "Evet, Öklid bunu ispatlamıştır.")])


def u8():
    def ebob():
        g = ri(2, 15)
        a, b = ri(2, 9), ri(2, 9)
        if math.gcd(a, b) != 1 or a == b:
            return None
        x, y = g * a, g * b
        k = ch(["EBOB", "EKOK"])
        v = g if k == "EBOB" else g * a * b
        return M("%d ve %d sayılarının %s’u kaçtır?" % (x, y, k) if k == "EBOB" else "%d ve %d sayılarının %s’u kaçtır?" % (x, y, k), num(v), W3([num(g * a * b), num(g), num(x * y), num(g * a)], num(v)),
                 "EBOB(%d, %d) = %d, EKOK = %d · %d ÷ %d = %d. Cevap: <b>%s</b>." % (x, y, g, x, y, g, g * a * b, num(v)))

    def problem():
        k = ri(0, 2)
        g = ri(2, 12)
        a, b = ri(2, 8), ri(2, 8)
        if math.gcd(a, b) != 1 or a == b:
            return None
        if k == 0:
            return M("Boyutları %d cm ve %d cm olan dikdörtgen biçimindeki bir kâğıt, hiç artmayacak biçimde eş ve en büyük karelere bölünüyor. Bir karenin kenarı kaç cm’dir?" % (g * a, g * b), "%d cm" % g,
                     W3(["%d cm" % (g * a * b), "%d cm" % (g * a), "%d cm" % (g // 2 if g > 2 else g + 1)], "%d cm" % g), "EBOB(%d, %d) = <b>%d</b>." % (g * a, g * b, g))
        if k == 1:
            return M("İki otobüs aynı duraktan %d dakikada bir ve %d dakikada bir kalkıyor. Birlikte kalktıktan en az kaç dakika sonra yine birlikte kalkarlar?" % (g * a, g * b), "%d dakika" % (g * a * b),
                     W3(["%d dakika" % g, "%d dakika" % (g * a * g * b), "%d dakika" % (g * a + g * b)], "%d dakika" % (g * a * b)), "EKOK(%d, %d) = <b>%d</b>." % (g * a, g * b, g * a * b))
        return M("%d elma ve %d armut, her pakette aynı sayıda elma ve aynı sayıda armut olacak biçimde en çok kaç pakete ayrılabilir?" % (g * a, g * b), num(g), W3([num(g * a * b), num(a + b), num(g * a)], num(g)),
                 "EBOB(%d, %d) = <b>%d</b> paket." % (g * a, g * b, g))

    def iliski():
        g = ri(2, 12)
        a, b = ri(2, 9), ri(2, 9)
        if math.gcd(a, b) != 1 or a == b:
            return None
        x, y = g * a, g * b
        return M("İki sayının EBOB’u %d, EKOK’u %d ve sayılardan biri %d ise diğer sayı kaçtır?" % (g, g * a * b, x), num(y), W3([num(g * a * b), num(y + g), num(x * y), num(a * b)], num(y)),
                 "a · b = EBOB · EKOK → %d · b = %d · %d → b = <b>%d</b>." % (x, g, g * a * b, y))

    sets = [("EBOB ve EKOK", [(ebob, 20)]), ("EBOB · EKOK = a · b", [(iliski, 20)]), ("EBOB problemleri", [(problem, 20)]),
            ("EKOK problemleri", [(problem, 20)]), ("Karışık", [(ebob, 10), (iliski, 10)])]
    return U(10, "ebob-ve-ekok", "SY", "MAT.10.3.2", 8, "En Büyük Ortak Bölen ve En Küçük Ortak Kat", "EBOB ve EKOK",
             "Birden çok doğal sayının ortak bölenleriyle bunların en büyüğü ve ortak katlarıyla bunların en küçüğü arasındaki ilişkileri inceler ve problemlerde kullanır.",
             "EBOB ve EKOK bulma, EBOB · EKOK = a · b ilişkisi, kare kesme ve paketleme problemleri, birlikte tekrar eden olaylar",
             "EBOB · EKOK = a · b", "Bölme ve kesme → EBOB, birlikte tekrar → EKOK.", sets,
             ["EBOB, sayıların ortak bölenlerinin en büyüğüdür; EKOK, ortak katlarının en küçüğüdür.",
              "İki sayı için EBOB · EKOK = a · b’dir.",
              "Eş parçalara bölme ve paketleme problemleri EBOB, aynı anda tekrar eden olay problemleri EKOK ile çözülür."],
             [("12 ve 18", ["EBOB 6", "EKOK 36"], "6 ve 36"), ("12 dk ve 18 dk", ["EKOK"], "36 dk sonra")],
             [["EBOB ile EKOK’u karıştırmak", "Bölmede EBOB, birleşmede EKOK"], ["Aralarında asal sayılarda EBOB’u sayılardan biri almak", "EBOB 1’dir"], ["Çarpımı EKOK sanmak", "EKOK = çarpım ÷ EBOB"]],
             [("Aralarında asal ne demek?", "EBOB’u 1 olan sayılar."), ("Üç sayının EBOB’u nasıl bulunur?", "Önce ikisinin, sonra sonucun üçüncüyle EBOB’u alınır."),
              ("Asal çarpanlarla nasıl bulunur?", "EBOB’da ortak asallar en küçük üsle, EKOK’ta bütün asallar en büyük üsle alınır.")])


def u9():
    def kalan():
        d = ch([3, 4, 5, 6, 7, 8, 9])
        a, b = ri(10, 99), ri(10, 99)
        op = ch(["+", "·"])
        r = (a + b) % d if op == "+" else (a * b) % d
        return M("%d %s %d ifadesinin %d ile bölümünden kalan kaçtır?" % (a, "+" if op == "+" else "·", b, d), num(r), W3([num((r + 1) % d), num((a % d) + (b % d)) if op == "+" else num((a % d) * (b % d)), num((r + 2) % d)], num(r)),
                 "Kalanlarla işlem yaparız: %d → %d, %d → %d. Sonuç: <b>%d</b>." % (a, a % d, b, b % d, r))

    def us():
        b, d = ch([(2, 3), (2, 5), (3, 4), (3, 5), (2, 7), (3, 7), (7, 5)])
        n = ri(5, 60)
        r = pow(b, n, d)
        cyc = []
        x = 1
        for _ in range(d):
            x = x * b % d
            if x in cyc:
                break
            cyc.append(x)
        return M("%d<sup>%d</sup> sayısının %d ile bölümünden kalan kaçtır?" % (b, n, d), num(r), W3([num(x2) for x2 in range(d)], num(r))[:3],
                 "Kalanlar %s biçiminde tekrar eder (devir %d). %d sayısının %d ile bölümünden kalana bakılır: <b>%d</b>." % (", ".join(map(str, cyc)), len(cyc), n, len(cyc), r))

    def kural():
        d = ch([3, 4, 5, 6, 9, 11])
        n = ri(1000, 99999)
        r = n % d
        return M("%s sayısının %d ile bölümünden kalan kaçtır?" % (num(n), d), num(r), W3([num((r + 1) % d), num((r + 2) % d), num(sum(map(int, str(n))) % d) if d not in (3, 9) else num((r + 3) % d)], num(r)),
                 "%d ile bölünebilme kuralından kalan: <b>%d</b>." % (d, r))

    def rakam():
        d = ch([3, 9])
        base = [ri(1, 9), ri(0, 9), ri(0, 9)]
        s = sum(base)
        a_ = [x for x in range(10) if (s + x) % d == 0]
        g = ", ".join(map(str, a_))
        return M("%d%d%dA dört basamaklı sayısı %d ile tam bölünebiliyorsa A rakamı hangileri olabilir?" % (base[0], base[1], base[2], d), g,
                 W3([", ".join(str((x + 1) % 10) for x in a_), ", ".join(str((x + 2) % 10) for x in a_), str(a_[0])], g),
                 "Rakamlar toplamı %d + A, %s katı olmalı: <b>%s</b>." % (s, {3: "3’ün", 9: "9’un"}[d], g))

    sets = [("Kalanlarla işlem", [(kalan, 20)]), ("Bölünebilme kuralları", [(kural, 20)]), ("Eksik rakam", [(rakam, 20)]),
            ("Üslü sayıların kalanı", [(us, 20)]), ("Karışık", [(kalan, 10), (us, 10)])]
    return U(10, "bolunebilme-ve-kalan", "SY", "MAT.10.3.3", 9, "Bölünebilme ve Kalan", "Bölünebilme ve Kalan",
             "Bir doğal sayının belirli doğal sayılara bölümünden kalanlarına dair muhakeme yapar; bölünebilme kurallarını ve kalanlarla işlemleri kullanır.",
             "toplam ve çarpımın kalanı, 3, 4, 5, 6, 9 ve 11 ile bölünebilme, eksik rakam bulma, üslü sayıların kalan devri",
             "Kalanlarla işlem yap", "Toplamın kalanı kalanların toplamının kalanıdır.", sets,
             ["Toplamın ve çarpımın bir sayıya bölümünden kalan, terimlerin kalanlarıyla işlem yapılarak bulunur.",
              "3 ve 9 için rakamlar toplamına, 4 için son iki basamağa, 5 için birler basamağına, 11 için rakamların sırayla toplanıp çıkarılmasına bakılır.",
              "Üslü sayıların kalanları belli bir devirle tekrar eder."],
             [("47 · 38 ÷ 5", ["2 · 3 = 6", "6 ÷ 5 kalan 1"], "1"), ("2²⁰ ÷ 3", ["Kalanlar 2, 1, 2, 1…", "20 çift"], "1")],
             [["Kalan toplamını bölmeyi unutmak", "Kalan bölenden küçük olmalı"], ["4 kuralında son basamağa bakmak", "Son iki basamak"], ["Devri yanlış saymak", "Kalanları sırayla yaz"]],
             [("Kalan neden bölenden küçüktür?", "Daha büyük olsaydı bir kez daha bölünebilirdi."), ("11 kuralı nasıl?", "Rakamlar sağdan +, −, + diye toplanır."),
              ("Devir neden oluşur?", "Kalanlar sonlu sayıda olduğundan bir süre sonra tekrar eder.")])


# ============================================================ 10. fonksiyon olma şartları
def u10():
    def mi():
        k = ri(0, 2)
        if k == 0:
            xs = sh(list(range(1, 6)))[:4]
            ys = [ri(1, 9) for _ in xs]
            pairs = list(zip(xs, ys))
            bad = ri(0, 1)
            if bad:
                pairs.append((xs[0], (ys[0] % 9) + 1))
            sh_ = sh(pairs)
            g = "Fonksiyon değildir" if bad else "Fonksiyondur"
            return M("{%s} bağıntısı bir fonksiyon mudur?" % ", ".join("(%d, %d)" % p for p in sh_), g, ["Fonksiyondur" if bad else "Fonksiyon değildir", "Yalnızca x pozitifse fonksiyondur", "Bilinemez"],
                     "Her x’e tek bir y karşılık gelmeli. %s" % ("x = %d iki farklı değere gidiyor: <b>fonksiyon değildir</b>." % xs[0] if bad else "Her x tek değere gidiyor: <b>fonksiyondur</b>."))
        S = [("y² = x", "Değildir"), ("y = x²", "Fonksiyondur"), ("x² + y² = 4", "Değildir"), ("y = |x|", "Fonksiyondur"), ("x = 3", "Değildir"), ("y = 3", "Fonksiyondur"),
             ("y = √x (x ≥ 0)", "Fonksiyondur"), ("|y| = x", "Değildir"), ("y = 1/x (x ≠ 0)", "Fonksiyondur"), ("y = 2x − 1", "Fonksiyondur")]
        t, g = ch(S)
        return M("ℝ’de tanımlı “%s” bağıntısı y’yi x’in fonksiyonu olarak verir mi?" % t, "Fonksiyondur" if g == "Fonksiyondur" else "Fonksiyon değildir",
                 ["Fonksiyon değildir" if g == "Fonksiyondur" else "Fonksiyondur", "Yalnızca x pozitifse fonksiyondur", "Bilinemez"],
                 "Düşey doğru testi: her düşey doğru grafiği en çok bir noktada kesmeli. Cevap: <b>%s</b>." % ("fonksiyondur" if g == "Fonksiyondur" else "fonksiyon değildir"))

    def tanim():
        k = ri(0, 2)
        a = ri(-6, 6)
        if k == 0:
            g = "x ≥ %s" % sn(a)
            return M("f(x) = √(%s) fonksiyonunun en geniş tanım kümesi hangisidir?" % lin(1, "x", -a), "[%s, ∞)" % sn(a), ["(%s, ∞)" % sn(a), "[%s, ∞)" % sn(-a) if a else "(−∞, 0]", "ℝ"],
                     "Kök içi negatif olamaz: x − (%s) ≥ 0 → <b>[%s, ∞)</b>." % (sn(a), sn(a)))
        if k == 1:
            return M("f(x) = 1 ÷ (%s) fonksiyonunun en geniş tanım kümesi hangisidir?" % lin(1, "x", -a), "ℝ − {%s}" % sn(a), ["ℝ − {%s}" % sn(-a) if a else "ℝ − {1}", "ℝ", "[%s, ∞)" % sn(a)],
                     "Payda sıfır olamaz: x ≠ %s → <b>ℝ − {%s}</b>." % (sn(a), sn(a)))
        if k == 2 and ri(0, 1):
            a = ri(1, 9)
            return M("f(x) = 1 ÷ (x² − %d) fonksiyonunun en geniş tanım kümesi hangisidir?" % (a * a), "ℝ − {%s, %d}" % (sn(-a), a), ["ℝ − {%d}" % a, "ℝ − {%d}" % (a * a), "ℝ"],
                     "x² − %d = 0 → x = ±%d: <b>ℝ − {%s, %d}</b>." % (a * a, a, sn(-a), a))
        b = ri(1, 9)
        if ri(0, 1):
            return M("f(x) = √(%d − x) fonksiyonunun en geniş tanım kümesi hangisidir?" % b, "(−∞, %d]" % b, ["[%d, ∞)" % b, "(−∞, %d)" % b, "ℝ − {%d}" % b],
                     "%d − x ≥ 0 → x ≤ %d: <b>(−∞, %d]</b>." % (b, b, b))
        return M("f(x) = %s fonksiyonunun görüntü kümesi hangisidir?" % ("x² + %d" % b), "[%d, ∞)" % b, ["ℝ", "(%d, ∞)" % b, "[0, ∞)"], "x² ≥ 0 olduğundan x² + %d ≥ %d: <b>[%d, ∞)</b>." % (b, b, b))

    def ozellik():
        S = [("f(x) = 2x + 1", "Bire birdir"), ("f(x) = x²", "Bire bir değildir"), ("f(x) = |x|", "Bire bir değildir"), ("f(x) = x³", "Bire birdir"),
             ("f(x) = −x + 4", "Bire birdir"), ("f(x) = 5", "Bire bir değildir"), ("f(x) = x² + 1", "Bire bir değildir"), ("f(x) = 3x", "Bire birdir")]
        t, g = ch(S)
        return M("ℝ’den ℝ’ye tanımlı %s fonksiyonu bire bir midir?" % t, g, ["Bire bir değildir" if g == "Bire birdir" else "Bire birdir", "Yalnızca x &gt; 0 için bire birdir", "Bilinemez"],
                 "Yatay doğru testi: her yatay doğru grafiği en çok bir noktada kesmeli. Cevap: <b>%s</b>." % g.lower())

    def artan():
        a, b = nz(-4, 4), ri(-5, 5)
        k = ch(["artan", "azalan"])
        g = "Artandır" if a > 0 else "Azalandır"
        return M("f(x) = %s fonksiyonu ℝ’de artan mı, azalan mı?" % lin(a, "x", b), g, ["Azalandır" if a > 0 else "Artandır", "Sabittir", "Önce artan sonra azalandır"],
                 "x büyüdükçe f(x) %s: <b>%s</b>." % ("büyür" if a > 0 else "küçülür", g.lower()))

    sets = [("Fonksiyon mu?", [(mi, 20)]), ("Tanım ve görüntü kümesi", [(tanim, 20)]), ("Bire bir fonksiyonlar", [(ozellik, 8), (artan, 12)]),
            ("Artan ve azalan", [(artan, 8), (tanim, 12)]), ("Karışık", [(mi, 10), (tanim, 10)])]
    return U(10, "fonksiyon-olma-sartlari", "N", "MAT.10.4.1", 10, "Gerçek Sayılarda Fonksiyon Olma Şartları", "Fonksiyon Olma Şartları",
             "Gerçek sayılarda fonksiyon olma şartları ile fonksiyonların tanım ve görüntü kümesi, bire birlik, artanlık ve azalanlık gibi nitel özelliklerini matematiksel temsillerle değerlendirir.",
             "bir bağıntının fonksiyon olup olmadığı, düşey doğru testi, en geniş tanım kümesi, görüntü kümesi, bire bir fonksiyon, artan ve azalan fonksiyon",
             "Her x’e tek bir y", "Düşey doğru testi: fonksiyon mu?", sets,
             ["Tanım kümesindeki her elemana görüntü kümesinde yalnızca bir eleman karşılık geliyorsa bağıntı fonksiyondur.",
              "Kök içi negatif olamaz, payda sıfır olamaz; en geniş tanım kümesi buna göre bulunur.",
              "Farklı x değerleri farklı y değerlerine gidiyorsa fonksiyon bire birdir."],
             [("y² = x", ["x = 4 için y = 2 ve y = −2"], "Fonksiyon değil"), ("√(x − 3)", ["x − 3 ≥ 0"], "[3, ∞)")],
             [["Bire birliği fonksiyon olmakla karıştırmak", "Fonksiyon: her x’e tek y"], ["Paydayı sıfır yapan değeri dâhil etmek", "O değer çıkarılır"],
              ["x² fonksiyonunu bire bir sanmak", "f(2) = f(−2)"]],
             [("Düşey doğru testi nedir?", "Grafiği bir düşey doğru iki noktada kesiyorsa fonksiyon değildir."), ("Görüntü kümesi nedir?", "Fonksiyonun aldığı bütün değerlerdir."),
              ("Tanım kümesi neden önemlidir?", "Fonksiyonun hangi değerlerde anlamlı olduğunu gösterir.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
