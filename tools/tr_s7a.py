# -*- coding: utf-8 -*-
"""Türkiye 7. sınıf (Maarif Modeli, Ortaokul Matematik 2026): Sayılar ve Nicelikler (1)(2) — 1〜9 単元。"""
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, num, fr, M, NB
from tr_g7 import sn, par, dq, dpar, is_fin, ondalik, MINUS, gen


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


def rq(dens=(2, 3, 4, 5, 6, 8, 10), lo=-3, hi=3):
    """sıfırdan farklı, tam sayı olmayan rasyonel sayı"""
    while True:
        d = ch(dens)
        n = ri(lo * d, hi * d)
        x = F(n, d)
        if x and x.denominator > 1:
            return x


def numline(lo, hi, parts, mark, label="sayı doğrusu"):
    """lo..hi tam sayılar, her aralık parts eşit parça, mark (Fraction) noktası A"""
    W, H, L, Rr = 460, 70, 24, 24
    n = (hi - lo) * parts
    step = (W - L - Rr) / n
    s = "<svg viewBox='0 0 %d %d' role='img' aria-label='%s'>" % (W, H, label)
    s += "<line x1='%d' y1='30' x2='%d' y2='30' stroke='#333' stroke-width='2'/>" % (L - 10, W - Rr + 10)
    for i in range(n + 1):
        x = L + i * step
        big = i % parts == 0
        s += "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='#333' stroke-width='%s'/>" % (x, 30 - (8 if big else 5), x, 30 + (8 if big else 5), "2" if big else "1")
        if big:
            v = lo + i // parts
            s += "<text x='%.1f' y='56' font-size='14' text-anchor='middle' fill='#222'>%s</text>" % (x, (MINUS if v < 0 else "") + str(abs(v)))
    xm = L + float((F(mark) - lo) * parts) * step
    s += "<circle cx='%.1f' cy='30' r='6' fill='#c0392b'/><text x='%.1f' y='16' font-size='15' font-weight='700' text-anchor='middle' fill='#c0392b'>A</text>" % (xm, xm)
    return "<div class='qfig'>" + G.lg(s + "</svg>") + "</div>"


# ============================================================ 1. tam sayılar ve rasyonel sayılar
def u1():
    def mutlak():
        a = nz(-60, 60)
        k = ch(["|%s|" % sn(a), "|%s| + |%s|" % (sn(a), sn(-a // 2 or 1))])
        if "+" in k:
            b = -a // 2 or 1
            v = abs(a) + abs(b)
            return M("%s işleminin sonucu kaçtır?" % k, sn(v), [sn(a + b), sn(-v), sn(abs(a) - abs(b))],
                     "Mutlak değer, sayının sıfıra olan uzaklığıdır; hep pozitif ya da sıfırdır. |%s| = %s, |%s| = %s, toplam <b>%s</b>." % (sn(a), sn(abs(a)), sn(b), sn(abs(b)), sn(v)))
        return M("%s kaçtır?" % k, sn(abs(a)), [sn(-abs(a)), sn(abs(a) + 1), "0"],
                 "Mutlak değer, sayının sıfıra olan uzaklığıdır: <b>%s</b>." % sn(abs(a)))

    def zit():
        a = rq() if ri(0, 1) else F(nz(-40, 40))
        return M("%s sayısının toplama işlemine göre tersi (zıt işaretlisi) hangisidir?" % sn(a), sn(-a), [sn(a), sn(1 / a), sn(-1 / a)],
                 "Toplamları 0 olan sayılar birbirinin zıttıdır: %s + %s = 0. Cevap <b>%s</b>." % (sn(a), par(-a), sn(-a)))

    def dogru():
        lo = ri(-4, 1)
        parts = ch([2, 3, 4, 5])
        k = ri(1, 3 * parts - 1)
        if k % parts == 0:
            return None
        m = lo + F(k, parts)
        w = [sn(lo + F(k + 1, parts)), sn(-m), sn(lo + F(k, parts + 1) if parts < 5 else lo + F(k - 1, parts)), sn(m + 1)]
        return M("Sayı doğrusunda A noktasının gösterdiği rasyonel sayı hangisidir?" + numline(lo, lo + 3, parts, m), sn(m), w,
                 "Her birim %d eşit parçaya bölünmüş; her parça %s. A, %s noktasından %d parça sağda: <b>%s</b>." % (parts, fr(1, parts), sn(lo), k, sn(m)))

    SETS = [("doğal sayı", lambda x: x.denominator == 1 and x >= 0), ("tam sayı", lambda x: x.denominator == 1),
            ("negatif tam sayı", lambda x: x.denominator == 1 and x < 0), ("tam sayı olmayan rasyonel sayı", lambda x: x.denominator > 1)]

    def sinif():
        nm, f = ch(SETS)
        pool = [F(nz(-30, 30)) for _ in range(3)] + [rq() for _ in range(3)] + [F(ri(0, 30))]
        good = [x for x in pool if f(x)]
        bad = [x for x in pool if not f(x)]
        if not good or len(set(bad)) < 3:
            return None
        g = ch(good)
        return G.withopts(M("Hangisi bir <b>%sdır</b>?" % nm, sn(g), [sn(x) for x in sh(bad)],
                 "Doğal sayılar 0, 1, 2… ; tam sayılar negatifleri de kapsar; rasyonel sayılar a/b (b ≠ 0) biçimindeki sayılardır. Cevap <b>%s</b>." % sn(g)), "%s sayıları veriliyor.")

    CTX = [("Bir dalgıç deniz seviyesinin %d m altında.", "m", -1), ("Hava sıcaklığı sıfırın %d derece altında.", "°C", -1),
           ("Bir asansör zemin katın %d kat altında.", "kat", -1), ("Bir uçak deniz seviyesinin %d m üstünde.", "m", 1),
           ("Hesapta %d TL borç var.", "TL", -1), ("Bir oyunda %d puan kazanıldı.", "puan", 1)]

    def baglam():
        t, u, s = ch(CTX)
        a = ri(2, 40) * (100 if u == "m" and s > 0 else 1)
        v = s * a
        return M("%s Bu durum hangi tam sayı ile gösterilir?" % (t % a), sn(v), [sn(-v), sn(v + s), "0"],
                 "Seviyenin altı, borç ve kayıp negatif; üstü ve kazanç pozitif sayıyla gösterilir: <b>%s</b>." % sn(v))

    sets = [("Mutlak değer ve zıt sayı", [(mutlak, 10), (zit, 10)]),
            ("Sayı doğrusunda rasyonel sayılar", [(dogru, 20)]),
            ("Sayı kümeleri", [(sinif, 20)]),
            ("Günlük hayatta tam sayılar", [(baglam, 12), (zit, 8)]),
            ("Karışık", [(dogru, 7), (mutlak, 7), (sinif, 6)])]
    return unit("tam-sayilar-ve-rasyonel-sayilar", "S", "MAT.7.1.1", 1, "Tam Sayılar ve Rasyonel Sayılar", "Rasyonel Sayılar",
                "Gerçek yaşam ya da matematiksel durumlarda doğal sayılar, tam sayılar ve rasyonel sayıları yorumlar; tam sayılardan rasyonel sayılara geçer, sayı doğrusunda mutlak değerle açıklar.",
                "7. sınıf tam sayılar ve rasyonel sayılar çalışma kâğıdı: mutlak değer, zıt sayı, sayı doğrusunda rasyonel sayılar, sayı kümeleri ve günlük hayattan örnekler. 100 soru ve cevap anahtarı.",
                "a/b (b ≠ 0) bir rasyonel sayıdır", "Her tam sayı da bir rasyonel sayıdır: −3 = −3/1.", sets,
                ["Tam sayılar: …, −2, −1, 0, 1, 2, … Negatifler sıfırın solunda, pozitifler sağındadır.",
                 "Rasyonel sayı, a ve b tam sayı ve b ≠ 0 olmak üzere a/b biçiminde yazılabilen sayıdır. Her rasyonel sayı sayı doğrusunda bir noktadır.",
                 "Mutlak değer, sayının sıfıra olan uzaklığıdır: |−5| = 5, |5| = 5."],
                [("−2 ile −1 arasının 4 eşit parçaya bölündüğü sayı doğrusunda −2’den 3 parça sağdaki nokta", ["Her parça 1/4", "−2 + 3/4 = −5/4"], "−5/4"),
                 ("|−8| + |3|", ["|−8| = 8, |3| = 3"], "11")],
                [["Mutlak değeri negatif yazmak", "|−7| = 7; uzaklık negatif olamaz"],
                 ["−1/2’yi −1’in solunda göstermek", "−1/2, −1 ile 0 arasındadır"],
                 ["Tam sayıları rasyonel saymamak", "−4 = −4/1 de bir rasyonel sayıdır"]],
                [("0 rasyonel sayı mıdır?", "Evet. 0 = 0/1 biçiminde yazılır."),
                 ("Her rasyonel sayı tam sayı mıdır?", "Hayır. 1/2 rasyonel sayıdır ama tam sayı değildir."),
                 ("Zıt sayı ile ters sayı aynı mı?", "Hayır. 3’ün zıttı −3’tür (toplamları 0); tersi 1/3’tür (çarpımları 1).")])


# ============================================================ 2. ondalık gösterim
def u2():
    DENS = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 20, 25]

    def cevir():
        b = ch(DENS)
        a = ri(1, 3 * b)
        x = F(a, b) * ch([1, 1, -1])
        if x.denominator == 1:
            return None
        o = ondalik(x)
        w = [ondalik(x + F(1, 10)), ondalik(-x), ondalik(1 / x),
             dq(x.numerator + F(x.denominator, 10) if abs(x.numerator) < 10 else x + 1, 2)]
        return M("%s rasyonel sayısının ondalık gösterimi hangisidir?" % sn(x), o, w,
                 "Payı paydaya böleriz: %s ÷ %s = <b>%s</b>%s" % (num(abs(x.numerator)), num(x.denominator), o,
                                                                    "" if is_fin(x) else " (devirli; çizgili rakamlar sonsuza kadar tekrar eder)."))

    def tur():
        b = ch(DENS)
        a = ri(1, b * 2)
        x = F(a, b)
        if x.denominator == 1:
            return None
        ok = "Sonlu ondalık" if is_fin(x) else "Devirli ondalık"
        return M("%s sayısının ondalık gösterimi nasıldır? (Bölme işlemini yaparak düşün.)" % sn(x), ok,
                 ["Devirli ondalık" if ok.startswith("S") else "Sonlu ondalık", "Tam sayı", "Ondalık gösterimi yoktur"],
                 "%s = %s. %s" % (sn(x), ondalik(x), "Bölme biter: <b>sonlu</b>." if is_fin(x) else "Kalanlar tekrar eder: <b>devirli</b>."))

    def geri():
        b = ch([2, 4, 5, 8, 10, 20, 25, 50, 100])
        a = ri(1, 3 * b)
        x = F(a, b) * ch([1, -1])
        if x.denominator == 1:
            return None
        k = len(dq(x).split(",")[1])
        return M("%s ondalık gösterimi hangi rasyonel sayıya eşittir? (En sade biçim)" % dq(x), sn(x),
                 [sn(x * 10), sn(F(x.numerator, x.denominator + 1)), sn(-x), sn(x + F(1, x.denominator))],
                 "%s = %s%s/%s; sadeleştirince <b>%s</b>." % (dq(x), MINUS if x < 0 else "", num(int(abs(x) * 10 ** k)), num(10 ** k), sn(x)))

    def hangisi():
        want = ch(["devirli", "sonlu"])
        fins = [F(a, b) for b in (2, 4, 5, 8, 20, 25) for a in range(1, 9) if F(a, b).denominator > 1]
        devs = [F(a, b) for b in (3, 6, 7, 9, 11, 12, 15) for a in range(1, 9) if not is_fin(F(a, b))]
        g = ch(devs if want == "devirli" else fins)
        bad = sh(fins if want == "devirli" else devs)[:3]
        return G.withopts(M("Hangi kesrin ondalık gösterimi <b>%s</b>?" % {"devirli": "devirlidir", "sonlu": "sonludur"}[want], sn(g), [sn(x) for x in bad],
                            "Sadeleşmiş kesrin paydasında yalnızca 2 ve 5 çarpanı varsa ondalık gösterim sonludur; başka asal çarpan varsa devirlidir. %s = %s." % (sn(g), ondalik(g))), "%s sayıları veriliyor.")

    sets = [("Kesirden ondalığa", [(cevir, 20)]),
            ("Sonlu mu, devirli mi?", [(tur, 20)]),
            ("Ondalıktan kesre", [(geri, 20)]),
            ("Payda ve ondalık gösterim", [(hangisi, 12), (tur, 8)]),
            ("Karışık", [(cevir, 7), (geri, 7), (hangisi, 6)])]
    return unit("rasyonel-sayilarin-ondalik-gosterimi", "S", "MAT.7.1.2", 2, "Rasyonel Sayıların Ondalık Gösterimi: Sonlu ve Devirli", "Ondalık Gösterim",
                "Gerçek yaşam durumlarında rasyonel sayıları ondalık gösterimle ifade eder; her rasyonel sayının sonlu ya da devirli bir ondalık gösterimi olduğunu değerlendirir.",
                "7. sınıf rasyonel sayıların ondalık gösterimi çalışma kâğıdı: kesri bölme ile ondalığa çevirme, sonlu ve devirli ondalık gösterim, ondalıktan kesre geçme. 100 soru ve cevap anahtarı.",
                "a/b = a ÷ b", "Bölme biterse sonlu, kalanlar tekrar ederse devirli.", sets,
                ["Bir rasyonel sayının ondalık gösterimini bulmak için payı paydaya böleriz: 3/8 = 3 ÷ 8 = 0,375.",
                 "Bölmede kalanlar tekrar etmeye başlarsa rakamlar da tekrar eder: 1/3 = 0,333… Bu gösterime devirli denir ve tekrar eden kısmın üstüne çizgi çekilir.",
                 "Sadeleşmiş kesrin paydasında yalnızca 2 ve 5 çarpanları varsa gösterim sonludur."],
                [("5/6", ["5 ÷ 6 = 0,8333…", "3 tekrar ediyor"], "0,8<span class='ov'>3</span>"), ("−0,45", ["−45/100", "5’e böl: −9/20"], "−9/20")],
                [["Çizgiyi tüm ondalık kısmın üstüne çekmek", "Yalnızca tekrar eden rakamların üstüne çizilir: 0,8<span class='ov'>3</span>"],
                 ["0,25’i 25/10 yazmak", "İki basamak → payda 100: 25/100 = 1/4"],
                 ["Sadeleştirmeden paydaya bakmak", "6/15 = 2/5; payda 5 olduğu için sonludur"]],
                [("Her rasyonel sayının ondalık gösterimi var mı?", "Evet; ya sonlu ya da devirlidir."),
                 ("0,<span class='ov'>9</span> neye eşittir?", "1’e eşittir. 1/3 = 0,<span class='ov'>3</span> ise 3/3 = 0,<span class='ov'>9</span> = 1."),
                 ("Hesap makinesi devirli sayıyı nasıl gösterir?", "Ekrana sığdığı kadar basamak yazar ve son basamağı yuvarlar.")])


# ============================================================ 3. karşılaştırma ve sıralama
def u3():
    def iki():
        a, b = rq(), rq()
        if a == b:
            return None
        s = "&lt;" if a < b else "&gt;"
        return M("%s ☐ %s &nbsp; Kutuya hangi sembol gelir?" % (sn(a), sn(b)), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "≤"],
                 "%s = %s, %s = %s. Sayı doğrusunda sağdaki büyüktür: <b>%s %s %s</b>." % (sn(a), ondalik(a), sn(b), ondalik(b), sn(a), s, sn(b)))

    def sirala():
        xs = set()
        while len(xs) < 4:
            xs.add(rq(lo=-2, hi=2) if ri(0, 2) else F(nz(-3, 3)))
        xs = list(xs)
        up = sorted(xs)
        dirx = ch(["küçükten büyüğe", "büyükten küçüğe"])
        good = up if dirx.startswith("k") else up[::-1]
        def show(L):
            return " , ".join(sn(x) for x in L)
        w = [show(good[::-1]), show(sorted(xs, key=abs)), show(sh(xs))]
        return M("%s sayılarını %s sıralayınız." % (" ; ".join(sn(x) for x in sh(xs)), dirx), show(good), w,
                 "Ondalıklarına bakalım: %s. %s: <b>%s</b>." % (", ".join("%s = %s" % (sn(x), ondalik(x)) for x in up), cap(dirx), show(good)))

    def en():
        xs = set()
        while len(xs) < 4:
            xs.add(rq(lo=-3, hi=3))
        xs = list(xs)
        k = ch(["en büyük", "en küçük"])
        g = max(xs) if k == "en büyük" else min(xs)
        return G.withopts(M("Hangisi %stür?" % k, sn(g), [sn(x) for x in xs if x != g],
                 "Negatif sayılardan mutlak değeri büyük olan daha küçüktür. %s: <b>%s</b>." % (cap(k), sn(g))), "%s sayıları veriliyor.")

    def arasi():
        a = rq(lo=-3, hi=2)
        b = a + F(ch([1, 2]), ch([2, 3, 4]))
        g = (a + b) / 2
        w = [a - F(1, 4), b + F(1, 4), a - 1, b + 1]
        return M("%s ile %s arasında olan sayı hangisidir?" % (sn(a), sn(b)), sn(g), [sn(x) for x in w],
                 "%s = %s ve %s = %s. Aradaki sayı: <b>%s</b> = %s." % (sn(a), ondalik(a), sn(b), ondalik(b), sn(g), ondalik(g)))

    def sicak():
        cs = sh(["Erzurum", "Kars", "Ardahan", "Sivas", "Van", "Ağrı"])[:4]
        vs = []
        while len(set(vs)) < 4:
            vs = [F(ri(-120, 20), 10) for _ in cs]
        k = ch(["en soğuk", "en sıcak"])
        i = vs.index(min(vs) if k == "en soğuk" else max(vs))
        return M("Bir sabah ölçülen sıcaklıklar: %s. Hangi il %s?" % (", ".join("%s %s °C" % (c, dq(v)) for c, v in zip(cs, vs)), {"en soğuk": "en soğuktu", "en sıcak": "en sıcaktı"}[k]), cs[i],
                 [c for j, c in enumerate(cs) if j != i], "Sıcaklıkları sıralarız; %s: <b>%s</b> (%s °C)." % (k, cs[i], dq(vs[i])))

    sets = [("İki sayıyı karşılaştırma", [(iki, 20)]),
            ("En büyük, en küçük", [(en, 20)]),
            ("Sıralama", [(sirala, 20)]),
            ("Arada hangisi var?", [(arasi, 20)]),
            ("Günlük hayat", [(sicak, 10), (iki, 5), (sirala, 5)])]
    return unit("rasyonel-sayilari-karsilastirma-ve-siralama", "S", "MAT.7.1.3", 3, "Rasyonel Sayıları Karşılaştırma ve Sıralama", "Karşılaştırma ve Sıralama",
                "Rasyonel sayılarda karşılaştırma ve sıralamayı yorumlar; sayı doğrusundan yararlanarak sembolle ifade eder ve kendi cümleleriyle açıklar.",
                "7. sınıf rasyonel sayıları karşılaştırma ve sıralama çalışma kâğıdı: &lt; ve &gt; sembolleri, en büyük ve en küçük, sıralama, iki sayı arasındaki sayı, sıcaklıklar. 100 soru ve cevap anahtarı.",
                "Sayı doğrusunda sağdaki büyüktür", "Negatiflerde mutlak değeri büyük olan küçüktür: −3/4 < −1/2.", sets,
                ["Sayı doğrusunda sağdaki sayı soldakinden büyüktür. Her pozitif sayı her negatif sayıdan büyüktür.",
                 "Kesirleri karşılaştırmak için paydaları eşitleriz ya da ondalık gösterime çeviririz.",
                 "İki negatif sayıdan mutlak değeri büyük olan daha küçüktür: −5 < −2."],
                [("−3/4 ile −2/3", ["−9/12 ile −8/12", "−9 < −8"], "−3/4 &lt; −2/3"), ("−1,2 ; 1/2 ; −3/2 ; 0", ["−1,5 < −1,2 < 0 < 0,5"], "−3/2, −1,2, 0, 1/2")],
                [["−5’i −2’den büyük sanmak", "−5, sayı doğrusunda −2’nin solundadır"],
                 ["Paydası büyük kesri her zaman büyük sanmak", "1/3 > 1/4; pay ve paydaya birlikte bak"],
                 ["Negatif kesirde payları doğrudan karşılaştırmak", "−3/4 ile −2/3: önce paydaları eşitle"]],
                [("0 pozitif midir?", "Hayır. 0 ne pozitif ne negatiftir; negatiflerden büyük, pozitiflerden küçüktür."),
                 ("İki rasyonel sayı arasında kaç rasyonel sayı vardır?", "Sonsuz tane. Örneğin iki sayının ortalaması her zaman aradadır."),
                 ("Ondalık ve kesir karışıksa ne yapmalı?", "Hepsini aynı gösterime (genellikle ondalık) çevirip karşılaştır.")])


def cap(s):
    return G.cap(s)


# ============================================================ 4. toplama ve çıkarma
def u4():
    def tam():
        a, b = nz(-50, 50), nz(-50, 50)
        op = ch(["+", MINUS])
        v = a + b if op == "+" else a - b
        return M("%s %s %s işleminin sonucu kaçtır?" % (sn(a), op, par(b)), sn(v), [sn(-v), sn(a - b if op == "+" else a + b), sn(abs(a) + abs(b)) if abs(a) + abs(b) != abs(v) else sn(v + 10)],
                 "%s<b>%s</b>" % ("Çıkarma, zıttıyla toplamadır: %s + %s = " % (sn(a), par(-b)) if op != "+" else "%s + %s = " % (sn(a), par(b)), sn(v)))

    def kesir():
        a, b = rq((2, 3, 4, 6), -2, 2), rq((2, 3, 4, 6), -2, 2)
        op = ch(["+", MINUS])
        v = a + b if op == "+" else a - b
        w = [sn(-v), sn(a - b if op == "+" else a + b), sn(F(a.numerator + (b.numerator if op == "+" else -b.numerator), a.denominator + b.denominator)) if a.denominator + b.denominator else None, sn(v + 1)]
        return M("%s %s %s = ?" % (sn(a), op, par(b)), sn(v), w,
                 "Paydaları eşitleriz (%s ile %s → payda %d). Sonuç <b>%s</b>." % (sn(a), sn(b), (a.denominator * b.denominator) // __import__("math").gcd(a.denominator, b.denominator), sn(v)))

    def ondal():
        a, b = F(nz(-99, 99), 10), F(nz(-99, 99), 100) * ch([1, 10])
        op = ch(["+", MINUS])
        v = a + b if op == "+" else a - b
        return M("%s %s %s = ?" % (dq(a), op, dpar(b)), dq(v), [dq(-v), dq(a - b if op == "+" else a + b), dq(v + F(1, 10))],
                 "Virgülleri alt alta getirip işaret kurallarıyla hesaplarız: <b>%s</b>." % dq(v))

    def uc():
        xs = [nz(-20, 20) for _ in range(3)]
        ops = [ch(["+", MINUS]) for _ in range(2)]
        v = xs[0]
        for o, x in zip(ops, xs[1:]):
            v = v + x if o == "+" else v - x
        e = "%s %s %s %s %s" % (sn(xs[0]), ops[0], par(xs[1]), ops[1], par(xs[2]))
        return M("%s = ?" % e, sn(v), [sn(-v), sn(v + 2), sn(v - 2)], "Soldan sağa: <b>%s</b>." % sn(v))

    def eksik():
        a, v = nz(-30, 30), nz(-30, 30)
        x = v - a
        return M("%s + ☐ = %s &nbsp; Kutuya hangi sayı gelir?" % (sn(a), sn(v)), sn(x), [sn(-x), sn(v + a), sn(x + 1)],
                 "☐ = %s %s %s = <b>%s</b>." % (sn(v), MINUS, par(a), sn(x)))

    sets = [("Tam sayılarla", [(tam, 20)]),
            ("Kesirlerle", [(kesir, 20)]),
            ("Ondalık gösterimlerle", [(ondal, 20)]),
            ("Üç sayı", [(uc, 20)]),
            ("Eksik sayı ve karışık", [(eksik, 8), (kesir, 6), (ondal, 6)])]
    return unit("rasyonel-sayilarla-toplama-ve-cikarma", "S", "MAT.7.1.4", 4, "Rasyonel Sayılarla Toplama ve Çıkarma", "Toplama ve Çıkarma",
                "Rasyonel sayılarla toplama ve çıkarma işlemlerini içeren problemleri çözer; işlemleri sayı doğrusu gibi temsillerle açıklar.",
                "7. sınıf rasyonel sayılarla toplama ve çıkarma çalışma kâğıdı: tam sayılar, işaretli kesirler ve ondalık gösterimlerle toplama-çıkarma, üç sayılı işlemler, eksik sayı. 100 soru ve cevap anahtarı.",
                "Çıkarmak = zıttını eklemek", "a − (−b) = a + b", sets,
                ["Aynı işaretli sayıları toplarken mutlak değerleri toplar, ortak işareti yazarız: (−3) + (−5) = −8.",
                 "Zıt işaretli sayıları toplarken mutlak değerleri çıkarır, mutlak değeri büyük olanın işaretini yazarız: (−7) + 4 = −3.",
                 "Çıkarma işlemi, çıkanın zıttını eklemektir: 2 − (−6) = 2 + 6 = 8. Kesirlerde önce paydalar eşitlenir."],
                [("−3/4 + 1/6", ["−9/12 + 2/12"], "−7/12"), ("−2,5 − (−4,1)", ["−2,5 + 4,1"], "1,6")],
                [["2 − (−6) = −4 demek", "Eksi eksi artı olur: 2 + 6 = 8"],
                 ["(−7) + 4 sonucuna + işaret koymak", "Mutlak değeri büyük olan −7: sonuç −3"],
                 ["Kesirlerde paydaları da toplamak", "1/2 + 1/3 = 3/6 + 2/6 = 5/6"]],
                [("Sayı doğrusunda toplama nasıl gösterilir?", "Pozitif sayı eklerken sağa, negatif sayı eklerken sola gideriz."),
                 ("Toplamada sıra önemli mi?", "Hayır, toplama değişmelidir. Çıkarmada ise sıra önemlidir."),
                 ("Ondalıklı sayılarda nelere dikkat etmeli?", "Virgüller alt alta gelmeli; işaret kuralı tam sayılardaki gibidir.")])


# ============================================================ 5. çarpma ve bölme
def u5():
    def isaret():
        a, b = nz(-15, 15), nz(-15, 15)
        op = ch(["×", "÷"])
        if op == "÷":
            a = a * b
        v = a * b if op == "×" else F(a, b)
        return M("%s %s %s = ?" % (sn(a), op, par(b)), sn(v), [sn(-v), sn(a + b), sn(abs(v) + 1)],
                 "Aynı işaretlilerin çarpımı/bölümü pozitif, zıt işaretlilerinki negatiftir: <b>%s</b>." % sn(v))

    def kesir():
        a, b = rq((2, 3, 4, 5, 6), -2, 2), rq((2, 3, 4, 5, 6), -2, 2)
        op = ch(["×", "÷"])
        v = a * b if op == "×" else a / b
        w = [sn(-v), sn(a / b if op == "×" else a * b), sn(F(a.numerator * b.numerator, a.denominator + b.denominator)), sn(v * 2)]
        return M("%s %s %s = ?" % (sn(a), op, par(b)), sn(v), w,
                 ("Pay ile pay, payda ile payda çarpılır" if op == "×" else "Bölmede ikinci kesir ters çevrilip çarpılır") + ": <b>%s</b>." % sn(v))

    def ondal():
        a = F(nz(-50, 50), 10)
        b = F(nz(-9, 9), ch([1, 10]))
        op = ch(["×", "÷"])
        if op == "÷":
            a = a * b
        v = a * b if op == "×" else a / b
        return M("%s %s %s = ?" % (dq(a), op, dpar(b)), dq(v), [dq(-v), dq(v * 10), dq(v / 10)],
                 "Önce işareti belirleriz, sonra virgülü hesaba katarak işlemi yaparız: <b>%s</b>." % dq(v))

    def ters():
        a = rq((2, 3, 4, 5, 7), -3, 3) if ri(0, 1) else F(nz(-9, 9))
        if a == 1 or a == -1:
            return None
        return M("%s sayısının çarpma işlemine göre tersi hangisidir?" % sn(a), sn(1 / a), [sn(-a), sn(-1 / a), sn(a)],
                 "Çarpımları 1 olan sayılar birbirinin çarpmaya göre tersidir: %s × %s = 1. Cevap <b>%s</b>." % (sn(a), par(1 / a), sn(1 / a)))

    def kuvvet():
        a = nz(-5, 5)
        if abs(a) == 1:
            return None
        n = ri(2, 4)
        v = a ** n
        e = "(%s)<sup>%d</sup>" % (sn(a), n) if a < 0 else "%s<sup>%d</sup>" % (sn(a), n)
        alt = "%s%s<sup>%d</sup>" % (MINUS, num(abs(a)), n)
        if ri(0, 1) and a < 0:
            return M("%s = ?" % alt, sn(-(abs(a) ** n)), [sn(abs(a) ** n), sn(-abs(a) * n), sn(abs(a) * n)],
                     "Üs yalnızca %d’e aittir, eksi dışarıda kalır: %s = %s%d = <b>%s</b>." % (abs(a), alt, MINUS, abs(a) ** n, sn(-(abs(a) ** n))))
        return M("%s = ?" % e, sn(v), [sn(-v), sn(a * n), sn(abs(a) * n)],
                 "Negatif sayının çift kuvveti pozitif, tek kuvveti negatiftir: <b>%s</b>." % sn(v))

    sets = [("İşaret kuralı", [(isaret, 20)]),
            ("Kesirlerle", [(kesir, 20)]),
            ("Ondalık gösterimlerle", [(ondal, 20)]),
            ("Ters sayı ve kuvvet", [(ters, 10), (kuvvet, 10)]),
            ("Karışık", [(isaret, 7), (kesir, 7), (kuvvet, 6)])]
    return unit("rasyonel-sayilarla-carpma-ve-bolme", "S", "MAT.7.1.4", 5, "Rasyonel Sayılarla Çarpma ve Bölme", "Çarpma ve Bölme",
                "Rasyonel sayılarla çarpma ve bölme işlemlerini içeren problemleri çözer; işaret kurallarını ve çarpmaya göre tersi kullanır.",
                "7. sınıf rasyonel sayılarla çarpma ve bölme çalışma kâğıdı: işaret kuralı, işaretli kesir ve ondalıklarla çarpma-bölme, çarpmaya göre ters, negatif sayıların kuvvetleri. 100 soru ve cevap anahtarı.",
                "Aynı işaret +, zıt işaret −", "(−) × (−) = (+), (−) × (+) = (−). Bölmede de aynıdır.", sets,
                ["Çarpma ve bölmede önce işareti belirleriz: aynı işaretli iki sayının sonucu pozitif, zıt işaretlilerin sonucu negatiftir.",
                 "Kesirlerde pay ile pay, payda ile payda çarpılır. Bölmede ikinci kesir ters çevrilip çarpılır: a/b ÷ c/d = a/b × d/c.",
                 "Negatif bir sayının çift kuvveti pozitif, tek kuvveti negatiftir: (−2)³ = −8, (−2)⁴ = 16."],
                [("(−3/4) × 2/9", ["İşaret: −", "6/36 = 1/6"], "−1/6"), ("−2,4 ÷ (−0,6)", ["İşaret: +", "24 ÷ 6 = 4"], "4")],
                [["(−3) × (−4) = −12 demek", "Aynı işaret: pozitif, 12"],
                 ["−2⁴ ile (−2)⁴’ü aynı sanmak", "−2⁴ = −16, (−2)⁴ = 16"],
                 ["Bölmede ilk kesri ters çevirmek", "İkinci kesir (bölen) ters çevrilir"]],
                [("0’ın çarpmaya göre tersi var mı?", "Hayır. Hiçbir sayıyla çarpımı 1 olmaz."),
                 ("Bir sayıyı −1 ile çarpınca ne olur?", "Sayının zıttı elde edilir: 5 × (−1) = −5."),
                 ("Birden fazla negatif çarpan varsa?", "Negatiflerin sayısı çiftse sonuç pozitif, tekse negatiftir.")])


# ============================================================ 6. problemler
def u6():
    def sicaklik():
        a = ri(-12, 15)
        d = nz(-18, 18)
        v = a + d
        yon = "yükseldi" if d > 0 else "düştü"
        return M("Sabah sıcaklık %s °C idi. Öğlene kadar %d °C %s. Öğlen sıcaklık kaç °C oldu?" % (sn(a), abs(d), yon), sn(v),
                 [sn(a - d), sn(-v), sn(abs(a) + abs(d))], "%s %s %d = <b>%s</b> °C." % (sn(a), "+" if d > 0 else MINUS, abs(d), sn(v)))

    def fark():
        a, b = ri(-25, 10), ri(-30, 5)
        if a == b:
            return None
        hi, lo = max(a, b), min(a, b)
        return M("Bir günde %s en yüksek sıcaklık %s °C, en düşük sıcaklık %s °C ölçüldü. Sıcaklık farkı kaç derecedir?" % (ch(["Ankara’da", "Kars’ta", "Erzurum’da", "Sivas’ta", "Van’da", "Ardahan’da"]), sn(hi), sn(lo)),
                 num(hi - lo), [num(abs(hi + lo)), num(hi - lo + 2), num(abs(hi) - abs(lo)) if abs(hi) - abs(lo) > 0 else num(hi - lo - 1)],
                 "Fark = en yüksek − en düşük = %s %s %s = <b>%d</b> °C." % (sn(hi), MINUS, par(lo), hi - lo))

    def asansor():
        a = ri(-3, 12)
        u, d = ri(2, 9), ri(2, 12)
        v = a + u - d
        def kat(x):
            return "zemin kattan" if x == 0 else ("%d. kattan" % x if x > 0 else "%d. bodrum kattan" % -x)
        return M("Bir asansör %s %d kat yukarı, sonra %d kat aşağı gitti. Zemin kat 0, bodrum katlar negatif sayılarla gösteriliyor. Asansör hangi kattadır? (Sayı olarak)" % (kat(a), u, d),
                 sn(v), [sn(a - u + d), sn(v + 1), sn(-v)], "%s + %d %s %d = <b>%s</b>." % (sn(a), u, MINUS, d, sn(v)))

    def hesap():
        b = ri(-500, 1500)
        x, y = ri(100, 900), ri(100, 1500)
        v = b + x - y
        def tl_(n):
            return ("%s TL" % sn(n))
        return M("%s banka hesabında %s var (negatif değer borç demektir). Hesaba %s yatırdı, sonra %s ödedi. Hesapta kaç TL var?" % (gen(G.K.next()), tl_(b), tl_(x), tl_(y)),
                 tl_(v), [tl_(b - x + y), tl_(-v), tl_(v + 100)], "%s + %s %s %s = <b>%s</b>." % (sn(b), num(x), MINUS, num(y), tl_(v)))

    def kesir_prob():
        T = ch([24, 36, 48, 60, 72, 120])
        a, b = ch([(1, 3), (1, 4), (2, 3), (3, 4), (1, 6), (5, 6), (3, 8)])
        if (T * a) % b:
            return None
        c, d = ch([(1, 2), (1, 3), (1, 4)])
        k = T * a // b
        rest = T - k
        if (rest * c) % d:
            return None
        s = rest * c // d
        v = rest - s
        nm = G.K.next()
        return M("%s %d sayfalık kitabın %s kısmını birinci gün, kalan sayfaların %s kısmını ikinci gün okudu. Okumadığı kaç sayfa kaldı?" % (nm, T, fr(a, b), fr(c, d)),
                 num(v), [num(rest), num(s), num(T - k - T * c // d)], "1. gün %d × %s = %d; kalan %d. 2. gün %d × %s = %d. Geriye <b>%d</b> sayfa." % (T, fr(a, b), k, rest, rest, fr(c, d), s, v))

    def dalgic():
        a = ri(5, 40)
        b = ri(2, 6)
        t = ri(3, 8)
        v = -a - b * t
        return M("Bir dalgıç deniz seviyesinin %d m altında. Her dakika %d m daha aşağı iniyor. %d dakika sonra konumu hangi tam sayıyla gösterilir? (Deniz seviyesi 0)" % (a, b, t),
                 sn(v), [sn(-v), sn(-a + b * t), sn(-a - b - t)], "%s + %d × %s = <b>%s</b> m." % (sn(-a), t, par(-b), sn(v)))

    sets = [("Sıcaklık", [(sicaklik, 12), (fark, 8)]),
            ("Katlar ve konum", [(asansor, 12), (dalgic, 8)]),
            ("Para ve borç", [(hesap, 20)]),
            ("Kesirli problemler", [(kesir_prob, 20)]),
            ("Karışık problemler", [(fark, 5), (dalgic, 5), (hesap, 5), (kesir_prob, 5)])]
    return unit("rasyonel-sayi-problemleri", "S", "MAT.7.1.4", 6, "Rasyonel Sayılarla Problem Çözme", "Rasyonel Sayı Problemleri",
                "Rasyonel sayılarla dört işlem içeren gerçek yaşam problemlerini çözer; problemi sayı doğrusu gibi temsillere dönüştürür, strateji geliştirir ve çözümü kontrol eder.",
                "7. sınıf rasyonel sayı problemleri çalışma kâğıdı: sıcaklık değişimi ve farkı, asansör ve dalgıç, banka hesabı ve borç, kesirli kalan problemleri. 100 soru ve cevap anahtarı.",
                "Önce işareti anlamlandır", "Artış, yukarı, gelir: +   Azalış, aşağı, borç: −", sets,
                ["Problemdeki her niceliği işaretli bir sayıyla gösteririz: sıcaklık düşüşü, aşağı inme, borç negatif; artış, yükselme, gelir pozitiftir.",
                 "İki değer arasındaki fark = büyük − küçük. −5 ile 8 arasındaki fark 8 − (−5) = 13’tür.",
                 "Kesir problemlerinde ‘kalanın’ sözcüğüne dikkat: önce kalanı bulur, sonra onun kesrini alırız."],
                [("−7 °C’den 12 °C yükselen sıcaklık", ["−7 + 12"], "5 °C"), ("120 sayfanın 1/4’ü, sonra kalanın 1/3’ü okundu", ["30 okundu, kalan 90", "90’ın 1/3’ü 30", "90 − 30"], "60 sayfa")],
                [["Sıcaklık farkını −5 + 8 = 3 bulmak", "Fark = 8 − (−5) = 13"],
                 ["‘Kalanın’ yerine bütünün kesrini almak", "Önce kalanı bul"],
                 ["Bodrum katları pozitif yazmak", "Zeminin altı negatiftir"]],
                [("Sıcaklık farkı negatif olabilir mi?", "Fark, büyükten küçük çıkarılarak bulunduğu için pozitiftir."),
                 ("Problemi çözdükten sonra ne yapmalı?", "Sonucun durumla uyumlu olup olmadığını kontrol et: örneğin dalgıç yükselmediyse konum daha negatif olmalı."),
                 ("Sayı doğrusu ne işe yarar?", "Artış ve azalışları sağa-sola hareket olarak görmeyi sağlar.")])


# ============================================================ 7. oran
def u7():
    def sade():
        k = ri(2, 12)
        a, b = ri(1, 9), ri(1, 9)
        if a == b or __import__("math").gcd(a, b) != 1:
            return None
        A, B = a * k, b * k
        return M("%d : %d oranının en sade biçimi hangisidir?" % (A, B), "%d : %d" % (a, b), ["%d : %d" % (b, a), "%d : %d" % (A - B if A > B else B - A, b), "%d : %d" % (a + 1, b + 1)],
                 "İki terimi de %d ile böleriz: <b>%d : %d</b>." % (k, a, b))

    UNITS = [("km", "saat", "km/sa", "Bir araç %d saatte %d km yol gidiyor."), ("TL", "kg", "TL/kg", "%d kg peynir %d TL."),
             ("litre", "dakika", "L/dk", "Bir musluk %d dakikada %d litre su akıtıyor."), ("sayfa", "gün", "sayfa/gün", "%d günde %d sayfa okunuyor.")]

    def birim():
        u1, u2, lab, t = ch(UNITS)
        b = ri(2, 9)
        r = ri(3, 60) * (5 if u1 == "TL" else 1)
        a = b * r
        txt = t % (b, a)
        return M("%s Birim oran kaçtır?" % txt, "%d %s" % (r, lab), ["%d %s" % (a, lab), "%d %s" % (r + b, lab), "%s %s" % (sn(F(b, a)), lab)],
                 "Birim oran, 1 birime düşen miktardır: %d ÷ %d = <b>%d %s</b>." % (a, b, r, lab))

    def esdeger():
        a, b = ri(1, 9), ri(2, 9)
        if a == b:
            return None
        k = ri(2, 9)
        g = "%d : %d" % (a * k, b * k)
        w = ["%d : %d" % (a * k, b * k + 1), "%d : %d" % (a + k, b + k), "%d : %d" % (b * k, a * k)]
        return G.withopts(M("Hangisi %d : %d oranına denktir?" % (a, b), g, w, "Oranın iki terimi aynı sayıyla çarpılırsa denk oran elde edilir: %d : %d = <b>%s</b>." % (a, b, g)), "%s oranları veriliyor.")

    def birimli():
        q = ch([("Bir sınıfta %d kız, %d erkek öğrenci var. Kız öğrencilerin erkek öğrencilere oranı nedir?", False),
                ("Bir koşucu %d dakikada %d m koştu. Koşulan yolun süreye oranı nedir?", True)])
        a, b = ri(8, 20), ri(8, 20)
        if q[1]:
            a, b = ri(3, 9), ri(5, 20) * 100
            ans = "%d m/dk" % (b // a) if b % a == 0 else None
            if ans is None:
                return None
            return M(q[0] % (a, b), ans, ["%d" % (b // a), "%d dk/m" % (b // a), "%d m/dk" % (b - a)],
                     "Farklı birimli çokluklar oranlanınca oran birimli olur: %d m ÷ %d dk = <b>%s</b>." % (b, a, ans))
        if a == b:
            return None
        g = __import__("math").gcd(a, b)
        ans = "%d : %d" % (a // g, b // g)
        return M(q[0] % (a, b), ans, ["%d : %d" % (b // g, a // g), "%d : %d" % (a // g, (a + b) // g), "%d kişi" % (a - b if a > b else b - a)],
                 "Aynı birimli çokluklar oranlanınca birimsiz bir oran elde edilir: kızlar : erkekler = %d : %d = <b>%s</b>." % (a, b, ans))

    def karsilastir():
        n1, n2 = G.K.two()
        a1, b1 = ri(2, 9), ri(2, 9)
        a2, b2 = ri(2, 9), ri(2, 9)
        if F(a1, b1) == F(a2, b2):
            return None
        f = "su"
        ans = n1 if F(a1, b1) > F(a2, b2) else n2
        return M("%s %d bardak meyve suyunu %d bardak suyla, %s %d bardak meyve suyunu %d bardak suyla karıştırdı. Hangisinin karışımı daha yoğun meyve tadındadır?" % (n1, a1, b1, n2, a2, b2),
                 ans, [n2 if ans == n1 else n1, "İkisi aynı", "Bilinemez"],
                 "Çarpımsal karşılaştırma: %s için %d/%d, %s için %d/%d. Meyve suyunun suya oranı büyük olan: <b>%s</b>." % (n1, a1, b1, n2, a2, b2, ans))

    sets = [("Oranı sadeleştirme", [(sade, 20)]),
            ("Birim oran", [(birim, 20)]),
            ("Denk oranlar", [(esdeger, 20)]),
            ("Birimli ve birimsiz oran", [(birimli, 20)]),
            ("Hangisi daha yoğun?", [(karsilastir, 12), (birim, 8)])]
    return unit("oran", "S", "MAT.7.1.5", 7, "Oran: Birimli, Birimsiz, Denk ve Birim Oran", "Oran",
                "Gerçek yaşam durumlarında oran ilişkilerine dair akıl yürütür; iki çokluğu çarpımsal olarak karşılaştırır, birimli ve birimsiz oranları, denk ve birim oranları açıklar.",
                "7. sınıf oran çalışma kâğıdı: oranı sadeleştirme, birim oran (km/sa, TL/kg), denk oranlar, birimli ve birimsiz oranlar, hangi karışım daha yoğun. 100 soru ve cevap anahtarı.",
                "Oran: çarpımsal karşılaştırma", "Birim oran: 1 birime düşen miktar.", sets,
                ["Oran, iki çokluğun çarpımsal karşılaştırmasıdır ve a : b ya da a/b biçiminde yazılır. ‘Kaç fazla?’ toplamsal, ‘kaç katı?’ çarpımsal karşılaştırmadır.",
                 "Aynı birimdeki çokluklar oranlanırsa birimsiz, farklı birimdekiler oranlanırsa birimli oran (km/sa, TL/kg) elde edilir.",
                 "Oranın iki terimi aynı sayıyla çarpılır ya da bölünürse denk oran elde edilir. Birim oran, 1 birime karşılık gelen miktardır."],
                [("36 : 48", ["12’ye böl"], "3 : 4"), ("5 saatte 350 km", ["350 ÷ 5"], "70 km/sa")],
                [["Oranın terimlerinin yerini değiştirmek", "‘Kızların erkeklere oranı’: önce kızlar"],
                 ["Toplamsal karşılaştırma yapmak", "2’ye 3 ile 5’e 6 karışımında farklar aynı ama oranlar farklıdır"],
                 ["Birimli oranda birimi yazmamak", "70 değil 70 km/sa"]],
                [("Oran ile kesir aynı mı?", "Oran kesir biçiminde yazılabilir ama iki çokluğun karşılaştırmasını anlatır; parça-bütün olmak zorunda değildir."),
                 ("Birim oran neden işe yarar?", "Farklı paketlerin fiyatlarını ya da hızları kolayca karşılaştırmayı sağlar."),
                 ("Oranın terimleri ondalıklı olabilir mi?", "Evet. 1,5 : 2 = 3 : 4 gibi sadeleştirilebilir.")])


# ============================================================ 8. orantı
def u8():
    def mi_orantili():
        k = ri(2, 9)
        xs = sorted(sh(range(1, 13))[:4])
        good = ri(0, 1)
        ys = [k * x for x in xs]
        if not good:
            i = ri(1, 3)
            ys[i] += ch([1, 2, -1])
        rows = "<table class='sn-table'><tr><th>Ürün sayısı</th>%s</tr><tr><th>Fiyat (TL)</th>%s</tr></table>" % ("".join("<td>%d</td>" % x for x in xs), "".join("<td>%d</td>" % y for y in ys))
        ok = "Evet, orantılıdır" if good else "Hayır, orantılı değildir"
        return M("Tablodaki çokluklar orantılı mıdır?<div class='qfig'>%s</div>" % rows, ok,
                 ["Hayır, orantılı değildir" if good else "Evet, orantılıdır", "Yalnızca ilk iki sütun orantılıdır", "Tabloya bakarak karar verilemez"],
                 ("Her sütunda fiyat ÷ ürün sayısı = %d (sabit): <b>orantılıdır</b>." % k) if good else "Fiyat ÷ ürün sayısı her sütunda aynı değil: <b>orantılı değildir</b>.")

    def eksik():
        a, b = ri(1, 12), ri(2, 12)
        k = ri(2, 9)
        c = a * k
        x = b * k
        return M("%d/%d = %d/x orantısında x kaçtır?" % (a, b, c), num(x), [num(b + c - a), num(c * b // a + 1) if a else None, num(x + k), num(a * c)],
                 "İçler dışlar çarpımı: %d · x = %d · %d → x = <b>%d</b>." % (a, b, c, x))

    def sabit():
        k = ri(2, 12)
        xs = sorted(sh(range(1, 11))[:3])
        nm = ch(["Gidilen yol (km)", "Ödenen para (TL)", "Kullanılan un (g)"])
        nm2 = {"Gidilen yol (km)": "Süre (saat)", "Ödenen para (TL)": "Alınan defter", "Kullanılan un (g)": "Kek sayısı"}[nm]
        rows = "<table class='sn-table'><tr><th>%s</th>%s</tr><tr><th>%s</th>%s</tr></table>" % (nm2, "".join("<td>%d</td>" % x for x in xs), nm, "".join("<td>%d</td>" % (k * x * (10 if "un" in nm else 1)) for x in xs))
        kk = k * (10 if "un" in nm else 1)
        return M("Tablodaki orantının orantı sabiti (%s ÷ %s) kaçtır?<div class='qfig'>%s</div>" % (nm.split(" (")[0].lower(), nm2.split(" (")[0].lower(), rows), num(kk),
                 [num(kk + 1), num(kk * 2), sn(F(1, kk))], "Her sütunda bölüm aynıdır: <b>%d</b>." % kk)

    def iki_oran():
        a, b = ri(2, 9), ri(2, 9)
        if a == b:
            return None
        c, d = a * ri(2, 5), b * ri(2, 5)
        good = F(a, b) == F(c, d)
        if not good and ri(0, 1):
            k = ri(2, 5)
            c, d = a * k, b * k
            good = True
        ok = "Evet" if good else "Hayır"
        return M("%d : %d ile %d : %d oranları bir orantı oluşturur mu?" % (a, b, c, d), ok, ["Hayır" if good else "Evet", "Yalnızca terimler eşitse", "Paydaya bağlı"],
                 "İçler çarpımı %d × %d = %d, dışlar çarpımı %d × %d = %d. %s" % (b, c, b * c, a, d, a * d, "Eşit: <b>orantı oluşturur</b>." if good else "Eşit değil: <b>orantı oluşturmaz</b>."))

    def grafik():
        k = ri(2, 6)
        good = ri(0, 1)
        b = 0 if good else ri(1, 4)
        W, H = 260, 200
        s = "<svg viewBox='0 0 %d %d' role='img' aria-label='doğru grafiği'>" % (W, H)
        s += "<line x1='30' y1='170' x2='250' y2='170' stroke='#333'/><line x1='30' y1='170' x2='30' y2='10' stroke='#333'/>"
        for i in range(1, 6):
            s += "<text x='%d' y='186' font-size='12' text-anchor='middle'>%d</text>" % (30 + i * 40, i)
        top = k * 5 + b
        sc = 150 / top
        for v in range(0, top + 1, max(1, top // 5)):
            s += "<text x='24' y='%d' font-size='11' text-anchor='end'>%d</text>" % (170 - v * sc + 4, v)
        s += "<line x1='30' y1='%.1f' x2='230' y2='%.1f' stroke='#c0392b' stroke-width='3'/></svg>" % (170 - b * sc, 170 - (k * 5 + b) * sc)
        ok = "Evet, doğru orantılıdır" if good else "Hayır, doğru orantılı değildir"
        return M("Grafikteki iki çokluk doğru orantılı mıdır?<div class='qfig'>%s</div>" % G.lg(s), ok,
                 ["Hayır, doğru orantılı değildir" if good else "Evet, doğru orantılıdır", "Ters orantılıdır", "Grafikten anlaşılmaz"],
                 "Doğru orantılı çoklukların grafiği başlangıç noktasından (0, 0) geçen bir doğrudur. %s" % ("Bu doğru (0, 0)’dan geçiyor: <b>doğru orantılı</b>." if good else "Bu doğru (0, 0)’dan geçmiyor: <b>doğru orantılı değil</b>."))

    sets = [("Tablo orantılı mı?", [(mi_orantili, 20)]),
            ("Orantı sabiti", [(sabit, 20)]),
            ("Orantı oluşur mu?", [(iki_oran, 20)]),
            ("Eksik terim", [(eksik, 20)]),
            ("Grafik ve karışık", [(grafik, 8), (eksik, 6), (mi_orantili, 6)])]
    return unit("oranti", "S", "MAT.7.1.6", 8, "Orantı: Orantılı Durumlar ve Orantı Sabiti", "Orantı",
                "Gerçek yaşamdaki iki durumun orantılı olup olmadığını inceler; orantılı çoklukları tablo ve grafikle temsil eder, orantı kavramını kendi cümleleriyle açıklar.",
                "7. sınıf orantı çalışma kâğıdı: tablodaki çoklukların orantılı olup olmadığı, orantı sabiti, iki oranın orantı oluşturması, içler dışlar çarpımı, doğru orantı grafiği. 100 soru ve cevap anahtarı.",
                "a/b = c/d ise a · d = b · c", "Orantılı çoklukların bölümü sabittir (orantı sabiti).", sets,
                ["İki oranın eşitliğine orantı denir: 2/3 = 4/6. Orantıda içler çarpımı dışlar çarpımına eşittir: 3 × 4 = 2 × 6.",
                 "Bir tablodaki çoklukların bölümü her sütunda aynıysa çokluklar doğru orantılıdır; bu sabit bölüme orantı sabiti denir.",
                 "Doğru orantılı iki çokluğun grafiği, başlangıç noktasından geçen bir doğrudur."],
                [("3/5 = 12/x", ["3 · x = 5 · 12", "x = 60 ÷ 3"], "20"), ("2 kalem 14 TL, 5 kalem 35 TL", ["14 ÷ 2 = 7, 35 ÷ 5 = 7"], "Orantılı, sabit 7")],
                [["Bölüm yerine farkı kontrol etmek", "Orantıda farklar değil bölümler sabittir"],
                 ["İçler dışlar çarpımını çapraz olmayan sayılarla yapmak", "a/b = c/d → a · d = b · c"],
                 ["(0, 0)’dan geçmeyen doğruyu doğru orantı sanmak", "Sabit ücret eklenince orantı bozulur"]],
                [("Her doğru grafiği doğru orantı mı gösterir?", "Hayır. Yalnızca (0, 0)’dan geçen doğrular doğru orantıyı gösterir."),
                 ("Orantı sabiti kesir olabilir mi?", "Evet. Örneğin 2 kaşık şekere 3 bardak su: sabit 3/2."),
                 ("Taksi ücreti doğru orantılı mıdır?", "Açılış ücreti varsa değildir; 0 km’de bile ücret ödenir.")])


# ============================================================ 9. doğru orantı problemleri
def u9():
    def fiyat():
        a, b = ri(2, 9), ri(2, 15)
        p = ri(3, 40) * 5
        item = ch(["defter", "kalem", "simit", "ekmek", "kitap", "top"])
        if a == b:
            return None
        return M("%d %s %d TL ise %d %s kaç TL’dir?" % (a, item, a * p, b, item), "%s TL" % num(b * p),
                 ["%s TL" % num(a * p + (b - a)), "%s TL" % num(p), "%s TL" % num(b * p + p)],
                 "Birim fiyat %d ÷ %d = %d TL; %d × %d = <b>%s TL</b>." % (a * p, a, p, b, p, num(b * p)))

    def tarif():
        k = ch([2, 3, 4, 6])
        n2 = k * ch([2, 3])
        un = k * ch([25, 50, 75, 100, 125])
        return M("%d kişilik bir kek için %d g un gerekiyor. Aynı tarifle %d kişilik kek için kaç gram un gerekir?" % (k, un, n2), "%s g" % num(un * n2 // k),
                 ["%s g" % num(un + n2 - k), "%s g" % num(un * n2), "%s g" % num(un // k)], "1 kişilik %s g; %d kişilik %d × %s = <b>%s g</b>." % (num(un // k), n2, n2, num(un // k), num(un * n2 // k)))

    def harita():
        sc = ch([100000, 200000, 500000, 1000000, 2000000])
        cm = ri(2, 15)
        km = cm * sc // 100000
        return M("Ölçeği 1 : %s olan bir haritada iki şehir arası %d cm’dir. Gerçek uzaklık kaç km’dir?" % (num(sc), cm), "%s km" % num(km),
                 ["%s km" % num(km * 10), "%s km" % num(km // 10) if km >= 10 else "%s km" % num(km + 5), "%s km" % num(cm * sc // 1000)],
                 "%d cm × %s = %s cm = <b>%s km</b> (1 km = 100.000 cm)." % (cm, num(sc), num(cm * sc), num(km)))

    def hiz():
        v = ri(40, 110)
        t1, t2 = ri(2, 4), ri(5, 9)
        return M("Sabit hızla giden bir otobüs %d saatte %d km yol alıyor. %d saatte kaç km yol alır?" % (t1, v * t1, t2), "%s km" % num(v * t2),
                 ["%s km" % num(v * t1 + t2), "%s km" % num(v * (t2 - t1)), "%s km" % num(v * t2 + v)], "Saatte %d km; %d × %d = <b>%s km</b>." % (v, t2, v, num(v * t2)))

    def tablo_doldur():
        k = ri(3, 15)
        xs = [ri(2, 6), ri(7, 12)]
        rows = "<table class='sn-table'><tr><th>Litre benzin</th><td>%d</td><td>%d</td></tr><tr><th>Gidilen yol (km)</th><td>%d</td><td>?</td></tr></table>" % (xs[0], xs[1], k * xs[0])
        return M("Bir araç harcadığı benzinle doğru orantılı yol gidiyor. Tabloda ? yerine hangi sayı gelir?<div class='qfig'>%s</div>" % rows, num(k * xs[1]),
                 [num(k * xs[0] + xs[1] - xs[0]), num(k * xs[1] + k), num(k)], "1 litrede %d km; %d × %d = <b>%d</b>." % (k, xs[1], k, k * xs[1]))

    def paylas():
        a, b = ri(1, 5), ri(1, 5)
        if a == b:
            return None
        T = (a + b) * ri(5, 40)
        n1, n2 = G.K.two()
        p = T * a // (a + b)
        return M("%s ile %s %s TL’yi %d : %d oranında paylaştı. %s kaç TL aldı?" % (n1, n2, num(T), a, b, n1), "%s TL" % num(p),
                 ["%s TL" % num(T - p), "%s TL" % num(T // 2), "%s TL" % num(T // (a + b))], "Toplam %d pay; 1 pay %s TL. %s: %d × %s = <b>%s TL</b>." % (a + b, num(T // (a + b)), n1, a, num(T // (a + b)), num(p)))

    sets = [("Fiyat ve miktar", [(fiyat, 20)]),
            ("Tarif ve tablo", [(tarif, 10), (tablo_doldur, 10)]),
            ("Hız ve harita", [(hiz, 10), (harita, 10)]),
            ("Oranında paylaştırma", [(paylas, 20)]),
            ("Karışık problemler", [(fiyat, 5), (harita, 5), (paylas, 5), (tablo_doldur, 5)])]
    return unit("dogru-oranti-problemleri", "S", "MAT.7.1.7", 9, "Doğru Orantı Problemleri", "Doğru Orantı Problemleri",
                "Gerçek yaşamda doğru orantı içeren problemleri çözer; doğru orantılı çoklukları tablo ve grafikle temsil eder, farklı stratejilerle çözümü doğrular.",
                "7. sınıf doğru orantı problemleri çalışma kâğıdı: birim fiyat, tarif, hız ve yol, harita ölçeği, tabloyu tamamlama, verilen oranda paylaştırma. 100 soru ve cevap anahtarı.",
                "Önce 1 birimi bul", "Birim değeri bulup istenen miktarla çarp.", sets,
                ["Doğru orantıda bir çokluk kaç katına çıkarsa diğeri de aynı katına çıkar.",
                 "En güvenli yol birim değerdir: 3 defter 45 TL ise 1 defter 15 TL; 8 defter 8 × 15 = 120 TL.",
                 "Oranında paylaştırmada toplam pay sayısını bulur, bir payın değerini hesaplarız."],
                [("4 kg elma 100 TL ise 7 kg", ["1 kg 25 TL", "7 × 25"], "175 TL"), ("600 TL 2 : 3 oranında", ["5 pay, 1 pay 120", "2 × 120 ve 3 × 120"], "240 TL ve 360 TL")],
                [["Farkla hesaplamak", "4 kg 100 TL ise 7 kg 103 TL değildir"],
                 ["Harita ölçeğinde birim çevirmeyi unutmak", "1 km = 100.000 cm"],
                 ["Oranında paylaştırmada toplamı ikiye bölmek", "Pay sayısına göre böl"]],
                [("Doğru orantı problemini nasıl tanırım?", "Bir çokluk artarken diğeri de aynı oranda artıyorsa doğru orantıdır."),
                 ("Birim değer yerine içler dışlar kullanılabilir mi?", "Evet. 4/100 = 7/x gibi bir orantı kurup çözebilirsin."),
                 ("Sonucu nasıl kontrol ederim?", "Bulduğun değerle bölümü yeniden hesapla; orantı sabiti aynı çıkmalı.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9]
