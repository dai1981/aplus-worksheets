# -*- coding: utf-8 -*-
"""Türkiye 4. sınıf: Sayılar ve Nicelikler (1)(2) — 1〜11 単元（tr_run.py 4）。"""
from fractions import Fraction as F
from tr_common import low
import tr_g as G
from tr_g import (unit, cap, dagit, kesir_oku, fr, ff, mf, num, oku, mcq, M, NB, wrap, text, line, basamak_tablosu, sayi_dogrusu,
                  INK, GREEN, FILL, RED, BLUE)
import tr_s3a as A


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def n6(lo=1000, hi=999999, zeros=False):
    n = ri(lo, hi)
    if zeros:
        ds = list(str(n))
        for i in range(1, len(ds)):
            if G.R.random() < 0.35:
                ds[i] = "0"
        n = int("".join(ds))
    return n


def swap_digits(n):
    s = list(str(n))
    i = ri(0, len(s) - 2)
    s[i], s[i + 1] = s[i + 1], s[i]
    if s[0] == "0":
        return None
    v = int("".join(s))
    return None if v == n else v


BAS = ["birler", "onlar", "yüzler", "binler", "on binler", "yüz binler"]


# ============================================================ 1. altı basamaklı sayılar
def u1():
    def okunus():
        n = n6(10000, 999999, True)
        w = [oku(x) for x in (swap_digits(n), n + 10000 * ch([1, -1]) if n > 20000 else n + 10000, n // 10 if n % 10 == 0 else n * 10 % 1000000) if x]
        return mcq("%s sayısının okunuşu hangisidir?" % num(n), oku(n), w + [oku(n + 100), oku(n + 1), oku(n + 1000)], "%s → <b>%s</b>." % (num(n), oku(n)))

    def yazilis():
        n = n6(10000, 999999, True)
        b, r = divmod(n, 1000)
        w = [num(b * 100 + r) if r < 100 else None, num(b * 10000 + r) if b < 100 else num(swap_digits(n) or n + 1), num(swap_digits(n) or n + 10)]
        w.append(num(int(str(b) + str(r))) if r else num(b * 1000 + 1))
        return mcq("“%s” sayısı rakamlarla nasıl yazılır?" % oku(n), num(n), w,
                   "Önce binler bölüğü (%s bin), sonra birler bölüğü yazılır. Birler bölüğü 3 basamaktır: <b>%s</b>." % (oku(b), num(n)))

    def basamak_sayisi():
        n = n6(ch([1000, 10000, 100000]), 999999, True)
        k = len(str(n))
        return mcq("%s sayısı kaç basamaklıdır?" % num(n), "%d basamaklı" % k, ["%d basamaklı" % x for x in (k - 1, k + 1, k - 2, k + 2) if x > 2],
                   "Rakamları sayarız: %s sayısında %d rakam var. Cevap <b>%d basamaklı</b>." % (num(n), k, k))

    def cozumleme():
        n = n6(100000, 999999, True)
        ds = str(n)
        parts = [int(d) * 10 ** (5 - i) for i, d in enumerate(ds) if d != "0"]
        q = " + ".join(num(p) for p in parts)
        return mcq("%s toplamı hangi sayıya eşittir?" % q, num(n), [num(swap_digits(n) or n + 1), num(n // 10), num(n + 90000 if n < 900000 else n - 90000)],
                   "Basamak değerleri toplanır: <b>%s</b>." % num(n))

    def en_buyuk():
        ds = sh(sorted(set(ri(1, 9) for _ in range(12))))[:6]
        if len(ds) < 6:
            return None
        k = ri(0, 1)
        s = sorted(ds, reverse=(k == 0))
        g = int("".join(map(str, s)))
        w = [int("".join(map(str, sorted(ds, reverse=(k == 1))))), int("".join(map(str, s[:4] + s[4:][::-1]))), int("".join(map(str, s[1:2] + s[:1] + s[2:])))]
        return mcq("%s rakamlarını birer kez kullanarak yazılabilecek altı basamaklı en %s sayı hangisidir?" % (", ".join(map(str, sorted(ds))), "büyük" if k == 0 else "küçük"),
                   num(g), [num(x) for x in w],
                   "En %s sayı için rakamlar %s sıralanır: <b>%s</b>." % ("büyük" if k == 0 else "küçük", "büyükten küçüğe" if k == 0 else "küçükten büyüğe", num(g)))

    def hayat():
        yer, lo, hi = ch([("Bir futbol stadyumunda", 20000, 80000), ("Bir ilçede", 100000, 600000), ("Bir kütüphanede", 10000, 90000),
                          ("Bir fabrikada bir yılda", 100000, 900000), ("Bir maratonda", 10000, 40000), ("Bir şehir parkında", 100000, 500000)])
        n = n6(lo, hi, True)
        what = {"Bir futbol stadyumunda": "seyirci var", "Bir ilçede": "kişi yaşıyor", "Bir kütüphanede": "kitap var",
                "Bir fabrikada bir yılda": "oyuncak üretildi", "Bir maratonda": "koşucu yarıştı", "Bir şehir parkında": "ağaç var"}[yer]
        return mcq("%s %s %s. Bu sayı nasıl okunur?" % (yer, num(n), what), oku(n), [oku(x) for x in (swap_digits(n), n + 1000, n - 100, n + 10000, n - 10, n + 100000 if n < 900000 else n - 100000) if x and x > 0],
                   "%s → <b>%s</b>." % (num(n), oku(n)))

    sets = [("Sayıların okunuşu", [(okunus, 20)]),
            ("Rakamlarla yazma", [(yazilis, 20)]),
            ("Basamak sayısı ve çözümleme", [(basamak_sayisi, 8), (cozumleme, 12)]),
            ("En büyük ve en küçük sayı", [(en_buyuk, 20)]),
            ("Günlük hayattan sayılar", [(hayat, 12), (okunus, 4), (yazilis, 4)])]
    return unit("alti-basamakli-sayilar", "S", "MAT.4.1.1", 1, "Altı Basamaklı Sayılar: Okuma ve Yazma", "Altı Basamaklı Sayılar",
                "Altı basamağa kadar olan çoklukları sayılarla ifade eder; sayıları okur ve yazar.",
                "4. sınıf altı basamaklı sayılar çalışma kâğıdı: sayıları okuma ve rakamlarla yazma, basamak sayısı, çözümleme, en büyük ve en küçük sayı. 100 soru ve cevap anahtarı.",
                "Sayılar bölük bölük okunur", "Önce binler bölüğü, sonra birler bölüğü okunur.", sets,
                ["Büyük sayıları sağdan başlayarak üçerli bölüklere ayırırız: birler bölüğü ve binler bölüğü. Bölükler arasına nokta koyarız: 305.040.",
                 "Okurken önce binler bölüğünü okur, sonuna “bin” ekleriz; sonra birler bölüğünü okuruz.",
                 "Okunuşu rakamla yazarken birler bölüğü her zaman 3 basamaktır. Boş basamaklara 0 yazarız."],
                [("305.040 sayısını oku.", ["Binler bölüğü 305: üç yüz beş bin", "Birler bölüğü 040: kırk"], "üç yüz beş bin kırk"),
                 ("“yüz yirmi bin altı” sayısını rakamla yaz.", ["Binler bölüğü 120", "Birler bölüğü 006"], "120.006")],
                [["“yüz yirmi bin altı” → 1206", "Birler bölüğü 3 basamak: 120.006"], ["450.300 → “dört yüz elli üç yüz”", "Önce “bin” eklenir: dört yüz elli bin üç yüz"],
                 ["Rakam sayısını yanlış saymak", "Noktalar rakam değildir; yalnızca rakamlar sayılır"]],
                [("Altı basamaklı en büyük sayı hangisidir?", "999.999 (dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz)."),
                 ("Altı basamaklı en küçük sayı hangisidir?", "100.000 (yüz bin)."),
                 ("Sayılara neden nokta koyarız?", "Bölükleri ayırmak ve sayıyı kolay okumak için. Nokta, binler bölüğü ile birler bölüğünü ayırır.")])


# ============================================================ 2. basamak ve bölük
def u2():
    def bas_degeri():
        n = n6(100000, 999999)
        ds = str(n)
        i = ri(0, 5)
        d = int(ds[i])
        if d == 0:
            return None
        v = d * 10 ** (5 - i)
        idx = [j for j in range(6) if ds[j] == ds[i]]
        if len(idx) > 1:
            return None
        return mcq("%s sayısındaki %d rakamının basamak değeri kaçtır?" % (num(n), d), num(v),
                   [num(d * 10 ** k) for k in range(6) if k != 5 - i] + [str(d)],
                   "%d rakamı %s basamağındadır. Basamak değeri <b>%s</b>." % (d, BAS[5 - i], num(v)))

    def hangi_basamak():
        n = n6(100000, 999999)
        ds = str(n)
        if len(set(ds)) < 6:
            return None
        i = ri(0, 5)
        return mcq("%s sayısının %s basamağındaki rakam hangisidir?" % (num(n), BAS[5 - i]), ds[i], [ds[j] for j in range(6) if j != i],
                   "Sağdan sayarız: birler, onlar, yüzler, binler, on binler, yüz binler. %s basamağında <b>%s</b> var." % (cap(BAS[5 - i]), ds[i]))

    def boluk():
        n = n6(100000, 999999)
        b, r = divmod(n, 1000)
        k = ri(0, 1)
        if k == 0:
            return mcq("%s sayısının binler bölüğündeki sayı hangisidir?" % num(n), str(b), [str(r), str(b // 10), str(int(str(n)[1:4]))],
                       "Sağdan üç basamak birler bölüğü (%03d), sonraki üç basamak binler bölüğüdür: <b>%d</b>." % (r, b))
        return mcq("%s sayısının birler bölüğündeki sayı hangisidir?" % num(n), "%03d" % r, [str(b), "%03d" % (n // 100 % 1000), "%03d" % (n // 10 % 1000)],
                   "Birler bölüğü sağdaki üç basamaktır: <b>%03d</b>." % r)

    def cozum():
        n = n6(100000, 999999, True)
        ds = str(n)
        parts = ["%s × %s" % (d, num(10 ** (5 - i))) for i, d in enumerate(ds) if d != "0"]
        g = " + ".join(parts)
        alt = " + ".join(("%s × %s" % (d, num(10 ** (4 - i))) if i < 5 else "%s × 1" % d) for i, d in enumerate(ds) if d != "0")
        bad = list(ds)
        j = ri(0, 4)
        bad[j], bad[j + 1] = bad[j + 1], bad[j]
        alt2 = " + ".join("%s × %s" % (d, num(10 ** (5 - i))) for i, d in enumerate(bad) if d != "0")
        nz = [i for i, d in enumerate(ds) if d != "0"]
        alt3 = " + ".join("%s × %s" % (ds[i], num(10 ** (5 - i))) for i in nz[:-1])
        return M("%s sayısının çözümlenmiş hâli hangisidir?" % num(n), g, [alt, alt2, alt3 if len(nz) > 1 else None, g.replace(" + ", " + ", 1)[:-1] + "0"],
                 "Her rakam basamak değeriyle yazılır: <b>%s</b>." % g)

    def tablo():
        n = n6(100000, 999999, True)
        return mcq("Basamak tablosunda gösterilen sayı hangisidir?" + basamak_tablosu_6(n), num(n), [num(swap_digits(n) or n + 1), num(int(str(n)[::-1].rstrip("0") or "1")), num(n // 10)],
                   "Tablodaki rakamlar soldan sağa yazılır: <b>%s</b>." % num(n))

    def sayi_vs_deger():
        n = n6(100000, 999999)
        ds = str(n)
        i = ri(0, 4)
        d = int(ds[i])
        if d == 0 or ds.count(ds[i]) > 1:
            return None
        v = d * 10 ** (5 - i)
        return mcq("%s sayısında %d rakamının basamak değeri ile sayı değerinin farkı kaçtır?" % (num(n), d), num(v - d), [num(v), num(v + d), num(v - 10 * d)],
                   "Basamak değeri %s, sayı değeri %d. Fark %s − %d = <b>%s</b>." % (num(v), d, num(v), d, num(v - d)))

    sets = [("Basamak değeri", [(bas_degeri, 20)]),
            ("Hangi basamakta?", [(hangi_basamak, 20)]),
            ("Birler bölüğü ve binler bölüğü", [(boluk, 20)]),
            ("Çözümleme ve basamak tablosu", [(cozum, 10), (tablo, 10)]),
            ("Basamak değeri ve sayı değeri", [(sayi_vs_deger, 12), (bas_degeri, 8)])]
    return unit("basamak-ve-boluk", "S", "MAT.4.1.2", 2, "Basamak, Basamak Değeri ve Bölük", "Basamak ve Bölük",
                "Altı basamağa kadar olan sayıları basamak ve bölüklerine ayırır; rakam, basamak, bölük, basamak değeri ve sayı değeri arasındaki ilişkiyi açıklar.",
                "4. sınıf basamak ve bölük çalışma kâğıdı: basamak adları, basamak değeri, sayı değeri, birler ve binler bölüğü, çözümleme. 100 soru ve cevap anahtarı.",
                "Rakamın değeri basamağına bağlıdır", "Aynı rakam farklı basamakta farklı değer alır.", sets,
                ["Sağdan sola basamaklar: birler, onlar, yüzler, binler, on binler, yüz binler.",
                 "İlk üç basamak birler bölüğü, sonraki üç basamak binler bölüğüdür.",
                 "Basamak değeri = rakam × basamağın değeri. Sayı değeri ise rakamın kendisidir."],
                [("472.315 sayısında 7 rakamının basamak değeri", ["7 on binler basamağında", "7 × 10.000"], "70.000"),
                 ("472.315 sayısının binler bölüğü", ["Sağdan üç basamak: 315", "Sonraki üç basamak: 472"], "472")],
                [["Basamakları soldan saymak", "Basamaklar sağdan sayılır: birler, onlar, yüzler…"], ["Basamak değeri ile sayı değerini karıştırmak", "472.315 sayısında 7’nin sayı değeri 7, basamak değeri 70.000"],
                 ["Bölüğü tek rakam sanmak", "Her bölük üç basamaktır"]],
                [("Bölük nedir?", "Sayının sağdan başlayarak üçerli ayrılan kısımlarıdır. 4. sınıfta birler ve binler bölüğünü kullanırız."),
                 ("0 rakamının basamak değeri kaçtır?", "Hangi basamakta olursa olsun 0’ın basamak değeri 0’dır."),
                 ("Çözümleme ne demektir?", "Sayıyı basamak değerlerinin toplamı olarak yazmaktır: 304.020 = 300.000 + 4.000 + 20.")])


def basamak_tablosu_6(n):
    head = ["Yüz binler", "On binler", "Binler", "Yüzler", "Onlar", "Birler"]
    ds = str(n).rjust(6, "0")
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th colspan='3'>Binler bölüğü</th><th colspan='3'>Birler bölüğü</th></tr>"
            "<tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>" % ("".join("<th>%s</th>" % c for c in head),
                                                                  "".join("<td style='text-align:center;min-width:44px'>%s</td>" % c for c in ds)))


# ============================================================ 3. sıralama ve yuvarlama
def yuvarla(n, b):
    return (n + b // 2) // b * b


def u3():
    def karsilastir():
        a = n6(10000, 999999)
        k = ri(0, 2)
        b = swap_digits(a) if k == 0 else (a + ch([1, 10, 100, 1000]) * ch([1, -1]) if k == 1 else n6(10000, 999999))
        if not b or a == b:
            return None
        s = "&lt;" if a < b else "&gt;"
        return mcq("%s ○ %s karşılaştırmasında ○ yerine hangi sembol gelir?" % (num(a), num(b)), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "+"],
                   "Basamak sayıları %s. Soldan başlayarak ilk farklı rakamlar karşılaştırılır: %s <b>%s</b> %s." % ("eşit" if len(str(a)) == len(str(b)) else "farklı", num(a), s, num(b)))

    def sirala():
        base = n6(100000, 899999)
        xs = sorted(set([base, swap_digits(base) or base + 9, base + ch([1000, 10000]), base - ch([100, 10])]))
        if len(xs) < 4:
            return None
        k = ri(0, 1)
        g = xs if k == 0 else xs[::-1]
        sh_ = sh(xs)
        w = [", ".join(num(x) for x in p) for p in (g[::-1], [g[1], g[0]] + g[2:], g[:2] + [g[3], g[2]])]
        return M("%s sayılarının %s sıralanışı hangisidir?" % (", ".join(num(x) for x in sh_), "küçükten büyüğe" if k == 0 else "büyükten küçüğe"),
                 ", ".join(num(x) for x in g), w, "Basamaklar soldan karşılaştırılır: <b>%s</b>." % ", ".join(num(x) for x in g))

    def yuvar():
        b = ch([10, 100, 1000])
        n = ri(1001, 9999)
        if n % b == 0 or (b == 10 and n % 100 == 0):
            return None
        g = yuvarla(n, b)
        ad = {10: "onluğa", 100: "yüzlüğe", 1000: "binliğe"}[b]
        w = [n // b * b, n // b * b + b, yuvarla(n, 10 if b != 10 else 100), yuvarla(n, 1000 if b != 1000 else 100)]
        return mcq("%s sayısı en yakın %s yuvarlanırsa hangi sayı olur?" % (num(n), ad), num(g), [num(x) for x in w],
                   "%s ile %s arasında, %s sayısına daha yakın (yarısı ve üstü yukarı yuvarlanır): <b>%s</b>." % (num(n // b * b), num(n // b * b + b), num(g), num(g)))

    def hangisi_yuvar():
        b = ch([100, 1000])
        t = ri(2, 9) * b if b == 1000 else ri(11, 99) * b
        ad = {100: "yüzlüğe", 1000: "binliğe"}[b]
        g = t + ri(-b // 2, b // 2 - 1)
        w = [t + b // 2 + ri(0, b // 4), t - b // 2 - ri(1, b // 4), t + b + ri(-b // 4, b // 4)]
        return mcq("En yakın %s yuvarlandığında %s olan sayı hangisidir?" % (ad, num(t)), num(g), [num(x) for x in w],
                   "%s ile %s arasındaki sayılar %s sayısına yuvarlanır. <b>%s</b> bu aralıkta." % (num(t - b // 2), num(t + b // 2 - 1), num(t), num(g)))

    def dogru():
        b = ch([100, 1000])
        lo = ri(1, 8) * b * (10 if b == 100 else 1)
        lo = lo if lo < 9000 else 3000
        k = ri(1, 9)
        v = lo + k * b // 10
        pic = sayi_dogrusu(lo, lo + b, b // 10, marks=[(v, "A")], labels=[lo, lo + b])
        g = yuvarla(v, b)
        return mcq("A noktasının gösterdiği sayı en yakın %s yuvarlanırsa kaç olur?%s" % ({100: "yüzlüğe", 1000: "binliğe"}[b], pic), num(g),
                   [num(lo), num(lo + b), num(v), num(yuvarla(v, b // 10))],
                   "A noktası %s. %s sayısına daha yakın: <b>%s</b>." % (num(v), num(g), num(g)))

    def grupla():
        n = n6(100000, 999999)
        b = ch([10, 100, 1000])
        g = n // b
        ad = {10: "onluk", 100: "yüzlük", 1000: "binlik"}[b]
        return mcq("%s sayısında kaç tane %s vardır?" % (num(n), ad), num(g), [num(n // (b * 10)), num(n // max(1, b // 10)), num(n // b + 1)],
                   "%s sayısının sağdaki %d basamağı atılır: <b>%s</b> tane %s." % (num(n), len(str(b)) - 1, num(g), ad))

    sets = [("Sayıları karşılaştırma", [(karsilastir, 20)]),
            ("Sıralama", [(sirala, 20)]),
            ("En yakın onluğa, yüzlüğe, binliğe", [(yuvar, 20)]),
            ("Hangi sayı yuvarlanır?", [(hangisi_yuvar, 10), (dogru, 10)]),
            ("Onluk, yüzlük, binlik gruplar", [(grupla, 14), (yuvar, 6)])]
    return unit("siralama-ve-yuvarlama", "S", "MAT.4.1.3", 3, "Sayıları Sıralama, Gruplama ve Yuvarlama", "Sıralama ve Yuvarlama",
                "Altı basamağa kadar olan sayılarda önce gelme ve sonra gelme ilişkilerini sembol kullanarak belirler; sayıları onluk, yüzlük ve binlik olarak gruplar; dört basamağa kadar olan sayıları en yakın onluğa, yüzlüğe veya binliğe yuvarlar.",
                "4. sınıf sayıları sıralama ve yuvarlama çalışma kâğıdı: büyük, küçük sembolleri, sıralama, onluk, yüzlük ve binlik gruplar, en yakın onluğa, yüzlüğe ve binliğe yuvarlama. 100 soru ve cevap anahtarı.",
                "Yarısı ve üstü yukarı yuvarlanır", "Karşılaştırırken soldan ilk farklı rakama bak.", sets,
                ["İki sayıyı karşılaştırırken önce basamak sayısına bakarız. Basamak sayısı eşitse soldan başlayarak ilk farklı rakamları karşılaştırırız.",
                 "Yuvarlarken sayının hangi iki onluk, yüzlük ya da binlik arasında olduğunu buluruz. Daha yakın olana yuvarlarız; tam ortadaysa yukarı yuvarlarız.",
                 "Bir sayıda kaç yüzlük olduğunu bulmak için sağdaki iki basamağı atarız: 4.567 sayısında 45 yüzlük var."],
                [("3.650 sayısını en yakın yüzlüğe yuvarla.", ["3.600 ile 3.700 arasında", "Onlar basamağı 5: yukarı"], "3.700"),
                 ("7.249 sayısını en yakın binliğe yuvarla.", ["7.000 ile 8.000 arasında", "Yüzler basamağı 2: aşağı"], "7.000")],
                [["3.650 → 3.600", "Onlar basamağı 5 ise yukarı yuvarlanır: 3.700"], ["Basamak sayısı farklı sayılarda ilk rakama bakmak", "Önce basamak sayısına bak: 98.000 &lt; 100.000"],
                 ["&lt; ve &gt; sembollerini karıştırmak", "Sembolün açık ağzı büyük sayıya bakar"]],
                [("Yuvarlama ne işe yarar?", "Sonucu tahmin etmek ve büyük sayıları kolay söylemek için. “Yaklaşık 4.000 kişi” demek gibi."),
                 ("5 ile biten bir sayı en yakın onluğa nasıl yuvarlanır?", "Tam ortada olduğu için yukarı yuvarlanır: 2.345 → 2.350."),
                 ("Büyük ve küçük sembolleri nasıl hatırlanır?", "Sembolün geniş tarafı büyük sayıya, sivri ucu küçük sayıya bakar.")])


# ============================================================ 4. ritmik sayma
def u4():
    def ileri():
        d = ch([10, 100, 1000])
        k = ri(0, 1)
        a = ri(1, 9000 - 6 * d) if d < 1000 else ri(0, 3) * 1000 + ch([0, 500, 250, 100])
        a = a // 10 * 10 if d >= 10 and G.R.random() < 0.5 else a
        xs = [a + i * d for i in range(6)]
        if k:
            xs = xs[::-1]
        j = ri(1, 5)
        show = ", ".join("…" if i == j else num(x) for i, x in enumerate(xs))
        g = xs[j]
        return mcq("%s %s sayıyoruz. Noktalı yere hangi sayı gelir?<br>%s" % (cap(dagit(d)), "ileri" if not k else "geri", show), num(g),
                   [num(g + d), num(g - d), num(g + d // 10 if d > 10 else g + 1)], "Her adımda %s %s: <b>%s</b>." % (num(d), "eklenir" if not k else "çıkarılır", num(g)))

    def kac_adim():
        d = ch([10, 100, 1000])
        a = ri(1, 40) * d
        n = ri(3, 9)
        b = a + n * d
        if b > 10000:
            return None
        return mcq("%s sayısından başlayıp %s ileri sayarak %s sayısına kaç adımda ulaşırız?" % (num(a), dagit(d), num(b)), str(n), [str(n + 1), str(n - 1), str(n * 10)],
                   "%s − %s = %s. %s ÷ %s = <b>%d</b> adım." % (num(b), num(a), num(n * d), num(n * d), num(d), n))

    def sonraki():
        d = ch([10, 100, 1000])
        a = ri(1, 9999 - 5 * d)
        k = ri(1, 5)
        dirn = ri(0, 1)
        if dirn and a - k * d < 0:
            return None
        g = a + k * d if not dirn else a - k * d
        return mcq("%s sayısından başlayarak %s %s sayan Ece %d. sayışta hangi sayıyı söyler?" % (num(a), dagit(d), "ileri" if not dirn else "geri", k), num(g),
                   [num(g + d), num(g - d), num(a + k) if not dirn else num(a - k)],
                   "%d kez %s %s: <b>%s</b>." % (k, num(d), "eklenir" if not dirn else "çıkarılır", num(g)))

    def kural():
        d = ch([10, 100, 1000, 20, 50, 200, 500])
        a = ri(1, 50) * 10
        dirn = ri(0, 1)
        xs = [a + i * d for i in range(5)]
        if dirn:
            xs = xs[::-1]
        g = "%s %s sayılmış" % (cap(dagit(d)), "ileri" if not dirn else "geri")
        alts = ["%s %s sayılmış" % (cap(dagit(x)), "ileri" if not dirn else "geri") for x in (d * 10, max(1, d // 10), d * 2) if x != d] + ["%s %s sayılmış" % (cap(dagit(d)), "geri" if not dirn else "ileri")]
        return mcq("%s dizisinde nasıl sayılmıştır?" % ", ".join(num(x) for x in xs), g, alts, "Ardışık iki sayının farkı %s: <b>%s</b>." % (num(d), low(g)))

    def hedef():
        a = ri(1, 80) * 100
        t = a + ri(2, 9) * 1000 + ri(2, 9) * 100
        if t > 10000:
            return None
        bn = (t - a) // 1000
        yz = (t - a - bn * 1000) // 100
        return mcq("Mert %s sayısından başlıyor. Önce biner, sonra yüzer ileri sayarak %s sayısına ulaşıyor. Biner kaç kez saymıştır? (En az adımla)" % (num(a), num(t)),
                   str(bn), [str(yz), str(bn + 1), str(bn + yz)], "%s − %s = %s. Bunda %d bin ve %d yüz var. Biner <b>%d</b> kez sayar." % (num(t), num(a), num(t - a), bn, yz, bn))

    sets = [("Onar, yüzer, biner ileri sayma", [(ileri, 20)]),
            ("Kaç adımda?", [(kac_adim, 20)]),
            ("Sayışta hangi sayı?", [(sonraki, 20)]),
            ("Sayma kuralını bulma", [(kural, 20)]),
            ("Hedef sayıya ulaşma", [(hedef, 10), (ileri, 5), (sonraki, 5)])]
    return unit("ritmik-sayma", "S", "MAT.4.1.4", 4, "Ritmik Sayma: Onar, Yüzer, Biner İleri ve Geri", "Ritmik Sayma",
                "10.000’e kadar onar, yüzer veya biner ileri ve geri sayarak hedef sayıya ulaşır.",
                "4. sınıf ritmik sayma çalışma kâğıdı: 10.000’e kadar onar, yüzer ve biner ileri ve geri sayma, eksik sayıyı bulma, sayma kuralı ve hedef sayıya ulaşma. 100 soru ve cevap anahtarı.",
                "Her adımda aynı sayı eklenir", "Geri sayarken her adımda aynı sayı çıkarılır.", sets,
                ["Onar sayarken onlar basamağı, yüzer sayarken yüzler basamağı, biner sayarken binler basamağı birer artar.",
                 "Geri sayarken aynı basamak birer azalır. 9’dan sonraki artışta bir üst basamak da değişir: 2.950, 3.050.",
                 "Hedef sayıya kaç adımda ulaşacağımızı bulmak için farkı sayma sayısına böleriz."],
                [("2.950 sayısından yüzer ileri say.", ["2.950 + 100 = 3.050", "3.050 + 100 = 3.150"], "2.950, 3.050, 3.150"),
                 ("4.300 sayısından biner geri 3 adım", ["4.300 − 3.000"], "1.300")],
                [["2.950 + 100 = 2.1050", "Yüzler 9’dan 10’a çıkınca binler artar: 3.050"], ["Onar sayarken birler basamağını değiştirmek", "Onar sayarken birler basamağı aynı kalır"],
                 ["Adım sayısını farkla karıştırmak", "Fark ÷ sayma sayısı = adım sayısı"]],
                [("Ritmik sayma neden önemlidir?", "Toplama, çıkarma ve çarpmayı hızlandırır; büyük sayılarda yön bulmayı kolaylaştırır."),
                 ("Biner sayarken hangi basamak değişir?", "Binler basamağı; 10.000’e gelince on binler basamağı da değişir."),
                 ("Geri sayarken 0’ın altına inilir mi?", "4. sınıfta 0’ın altına inmeyiz; sayma 0’da biter.")])


# ============================================================ 5. örüntüler
def sq_pattern(counts, c=12):
    """her adım: üst üste dizilmiş kareler (sütunlar)"""
    s = []
    x = 24
    H = 0
    for k, n in enumerate(counts):
        cols = (n + 3) // 4
        for i in range(n):
            cx, cy = x + (i // 4) * c, 8 + (i % 4) * c
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#a8d5ba' stroke='%s' stroke-width='1.2'/>" % (cx, cy, c, c, GREEN))
        s.append(text(x + cols * c / 2.0, 8 + 4 * c + 18, "%d. adım" % (k + 1), 12))
        x += max(cols * c, 30) + 34
        H = 8 + 4 * c + 26
    return wrap(x, H, "".join(s), "şekil örüntüsü")


def u5():
    def artan():
        d = ri(3, 99) if G.R.random() < 0.6 else ch([125, 250, 150, 300, 1000])
        a = ri(1, 500)
        k = ri(0, 1)
        xs = [a + i * d for i in range(6)]
        if k:
            xs = xs[::-1]
        j = ch([4, 5])
        show = ", ".join(num(x) if i < j else "…" for i, x in enumerate(xs[:j + 1]))
        g = xs[j]
        return mcq("%s örüntüsünde sıradaki sayı kaçtır?" % show, num(g), [num(g + d), num(g - d), num(g + (1 if k == 0 else -1) * (d + 1))],
                   "Örüntü her adımda %s %s: <b>%s</b>." % (num(d), "artıyor" if not k else "azalıyor", num(g)))

    def kural():
        d = ri(3, 60)
        a = ri(2, 99)
        k = ri(0, 1)
        xs = [a + i * d for i in range(5)]
        if k:
            xs = xs[::-1]
        g = "Her adımda %d %s" % (d, "artıyor" if not k else "azalıyor")
        return mcq("%s örüntüsünün kuralı nedir?" % ", ".join(num(x) for x in xs), g,
                   ["Her adımda %d %s" % (d, "azalıyor" if not k else "artıyor"), "Her adımda %d %s" % (d + 1, "artıyor" if not k else "azalıyor"),
                    "Her adımda %d %s" % (d * 2, "artıyor" if not k else "azalıyor")],
                   "Ardışık iki sayının farkı %d: <b>%s</b>." % (d, low(g)))

    def adim():
        d = ri(2, 12)
        a = ri(1, 20)
        n = ri(8, 25)
        g = a + (n - 1) * d
        xs = [a + i * d for i in range(4)]
        return mcq("%s, … örüntüsünün %d. adımındaki sayı kaçtır?" % (", ".join(num(x) for x in xs), n), num(g), [num(a + n * d), num(n * d), num(g - 1)],
                   "1. adım %d, sonra her adımda %d artıyor. %d. adım: %d + %d × %d = <b>%s</b>." % (a, d, n, a, n - 1, d, num(g)))

    def sekil():
        a, d = ri(1, 5), ri(1, 4)
        counts = [a + i * d for i in range(3)]
        n = ri(4, 7)
        g = a + (n - 1) * d
        return mcq("Şekil örüntüsünde her adımda kare sayısı aynı kuralla artıyor. %d. adımda kaç kare olur?%s" % (n, sq_pattern(counts)), str(g),
                   [str(g + d), str(g - d), str(n * d)], "Kareler %d, %d, %d… Her adımda %d artıyor. %d. adım: <b>%d</b>." % (counts[0], counts[1], counts[2], d, n, g))

    def artan_azalan():
        a = ri(5, 40)
        p, q = ri(3, 9), ri(1, 2)
        xs = [a]
        for i in range(6):
            xs.append(xs[-1] + (p if i % 2 == 0 else -q))
        j = 6
        show = ", ".join(num(x) for x in xs[:j]) + ", …"
        g = xs[j]
        return mcq("%s örüntüsünde sayılar bir artıp bir azalıyor. Sıradaki sayı kaçtır?" % show, num(g), [num(xs[j - 1] + p), num(xs[j - 2]), num(g - 1), num(g + q + p)],
                   "Kural: %d artır, %d azalt. Son adımda %d artırıldı; şimdi %d azaltılır: <b>%s</b>." % (p, q, p, q, num(g)))

    def hata():
        d = ri(4, 25)
        a = ri(10, 200)
        xs = [a + i * d for i in range(6)]
        j = ri(1, 5)
        bad = xs[j] + ch([1, -1, 2, 10])
        ys = xs[:j] + [bad] + xs[j + 1:]
        return mcq("%s örüntüsünde bir sayı yanlış yazılmış. Yanlış sayı hangisidir?" % ", ".join(num(x) for x in ys), num(bad),
                   [num(y) for y in ys if y != bad], "Kural: her adımda %d artıyor. %s yerine %s olmalıydı: <b>%s</b> yanlış." % (d, num(bad), num(xs[j]), num(bad)))

    sets = [("Sıradaki sayı", [(artan, 20)]),
            ("Örüntünün kuralı", [(kural, 20)]),
            ("İstenen adımdaki sayı", [(adim, 20)]),
            ("Şekil örüntüleri", [(sekil, 20)]),
            ("Artıp azalan örüntüler ve hata bulma", [(artan_azalan, 10), (hata, 10)])]
    return unit("oruntuler", "S", "MAT.4.1.5", 5, "Artan ve Azalan Sayı ve Şekil Örüntüleri", "Örüntüler",
                "Artan ve azalan sayı ve şekil örüntülerindeki değişimi genelleyerek kuralını sözlü olarak ifade eder.",
                "4. sınıf örüntüler çalışma kâğıdı: artan ve azalan sayı örüntüleri, kural bulma, istenen adımdaki sayı, şekil örüntüleri, artıp azalan örüntüler. 100 soru ve cevap anahtarı.",
                "Ardışık iki terimin farkı kuralı verir", "Kuralı bulunca istediğin adımı hesaplarsın.", sets,
                ["Bir örüntüde ardışık iki terim arasındaki fark hep aynıysa örüntü sabit miktarda artar ya da azalır.",
                 "Kuralı bulmak için birkaç terimin farkına bakarız. Kural bütün terimler için doğru olmalıdır.",
                 "Uzak bir adımı bulmak için: 1. terim + (adım − 1) × artış miktarı."],
                [("5, 9, 13, 17 örüntüsünün 10. adımı", ["Kural: 4 artıyor", "5 + 9 × 4 = 41"], "41"),
                 ("80, 72, 64, 56, … sıradaki sayı", ["Kural: 8 azalıyor", "56 − 8"], "48")],
                [["10. adım için 10 × 4 eklemek", "1. adımdan 10. adıma 9 adım vardır: 5 + 9 × 4"], ["Yalnızca ilk iki terime bakmak", "Kuralı birkaç terimle kontrol et"],
                 ["Azalan örüntüde eklemek", "Terimler küçülüyorsa çıkarılır"]],
                [("Örüntü nedir?", "Belli bir kurala göre devam eden sayı ya da şekil dizisidir."),
                 ("Bir örüntü hem artıp hem azalabilir mi?", "Evet. “3 artır, 1 azalt” gibi kurallarla terimler bir artar bir azalır."),
                 ("Şekil örüntüsünde kural nasıl bulunur?", "Her adımdaki şekil sayısını sayıp ardışık adımların farkına bakarız.")])


# ============================================================ 6. kesir çeşitleri
def pies(n, b, k):
    """n tane b parçalı daire, toplam k parça boyalı"""
    out = []
    for i in range(n):
        out.append(A.pie(b, max(0, min(b, k - i * b)), r=36))
    return "<div class='qfig'>" + "".join(o.replace("<div class='qfig'>", "<span style='display:inline-block;margin:2px 6px'>").replace("</div>", "</span>") for o in out) + "</div>"


def u6():
    def tur():
        b = ri(2, 10)
        k = ri(0, 2)
        if k == 0:
            a = ri(1, b - 1)
            x, g = fr(a, b), "Basit kesir"
        elif k == 1:
            a = ri(b, 3 * b)
            x, g = fr(a, b), "Bileşik kesir"
        else:
            w, a = ri(1, 4), ri(1, b - 1)
            x, g = mf(w, a, b), "Tam sayılı kesir"
        return mcq("%s hangi kesir türüdür?" % x, g, ["Basit kesir", "Bileşik kesir", "Tam sayılı kesir", "Birim kesir"],
                   {0: "Pay paydadan küçük: <b>basit kesir</b>.", 1: "Pay paydaya eşit ya da paydadan büyük: <b>bileşik kesir</b>.",
                    2: "Bir tam sayı ve bir basit kesirden oluşuyor: <b>tam sayılı kesir</b>."}[k])

    def model():
        b = ch([2, 3, 4, 6, 8])
        w = ri(1, 2)
        a = ri(1, b - 1)
        k = w * b + a
        pic = pies(w + 1, b, k)
        t = ri(0, 1)
        if t == 0:
            return mcq("Boyalı kısmı tam sayılı kesir olarak yazınız.%s" % pic, mf(w, a, b), [mf(w + 1, a, b), mf(w, b - a, b), fr(a, b), fr(k, b * (w + 1))],
                       "%d bütün tamamen, sonuncunun %d parçadan %d tanesi boyalı: <b>%s</b>." % (w, b, a, mf(w, a, b)))
        return mcq("Boyalı kısmı bileşik kesir olarak yazınız.%s" % pic, fr(k, b), [fr(b, k), fr(k, b * (w + 1)), fr(a, b), fr(k + 1, b)],
                   "Her bütün %d parça. Boyalı parça sayısı %d: <b>%s</b>." % (b, k, fr(k, b)))

    def b2t():
        b = ri(2, 9)
        w, a = ri(1, 5), ri(1, b - 1)
        k = w * b + a
        return mcq("%s bileşik kesrinin tam sayılı kesir olarak yazılışı hangisidir?" % fr(k, b), mf(w, a, b), [mf(a, w, b) if w < b else mf(w + 1, a, b), mf(w - 1, a + b, b) if w > 1 else mf(w, a + 1, b), mf(w, b - a, b)],
                   "%d ÷ %d = %d, kalan %d. Cevap <b>%s</b>." % (k, b, w, a, mf(w, a, b)))

    def t2b():
        b = ri(2, 9)
        w, a = ri(1, 5), ri(1, b - 1)
        k = w * b + a
        return mcq("%s tam sayılı kesrinin bileşik kesir olarak yazılışı hangisidir?" % mf(w, a, b), fr(k, b), [fr(w * a + b, b), fr(w + a, b), fr(k, w * b), fr(k - 1, b)],
                   "Tam kısım × payda + pay: %d × %d + %d = %d. Cevap <b>%s</b>." % (w, b, a, k, fr(k, b)))

    def hayat():
        b = ch([2, 4])
        w = ri(1, 4)
        a = ri(1, b - 1)
        nm = G.K.next()
        what = ch(["pizza", "ekmek", "pasta", "karpuz"])
        q = "%s %d bütün ve %s %s yedi. Yediği miktarı tam sayılı kesir olarak nasıl yazarız?" % (nm, w, "bir yarım" if b == 2 else ("%s çeyrek" % oku(a)), what)
        return mcq(q, mf(w, a, b), [mf(w, b, a) if a > 1 else mf(w + 1, a, b), fr(w + a, b), mf(a, w, b) if w < b else mf(w, a, b + 1)],
                   "%d bütün ve %s → <b>%s</b>." % (w, fr(a, b), mf(w, a, b)))

    def bir_butun():
        b = ri(2, 12)
        k = ri(0, 1)
        if k == 0:
            return mcq("Hangi kesir bir bütüne eşittir?", fr(b, b), [fr(1, b), fr(b - 1, b), fr(b + 1, b)] if b > 2 else [fr(1, 2), fr(3, 2), fr(4, 2)],
                       "Pay ile payda eşitse kesir bir bütündür: <b>%s</b>." % fr(b, b))
        w = ri(2, 4)
        return mcq("%d bütün kaç tane %s eder?" % (w, fr(1, b)), str(w * b), [str(w + b), str(b), str(w * b + 1)],
                   "Her bütünde %d tane %s var: %d × %d = <b>%d</b>." % (b, fr(1, b), w, b, w * b))

    sets = [("Basit, bileşik ve tam sayılı kesir", [(tur, 20)]),
            ("Modeli kesirle yazma", [(model, 20)]),
            ("Bileşik kesri tam sayılı kesre çevirme", [(b2t, 20)]),
            ("Tam sayılı kesri bileşik kesre çevirme", [(t2b, 20)]),
            ("Günlük hayatta kesirler", [(hayat, 8), (bir_butun, 12)])]
    return unit("kesir-cesitleri", "S", "MAT.4.1.6", 6, "Basit, Bileşik ve Tam Sayılı Kesirler", "Kesir Çeşitleri",
                "Basit, bileşik ve tam sayılı kesirlerin gösterimlerini tanır, günlük hayattaki durumlara uygun gösterimleri belirler ve kullanır.",
                "4. sınıf kesir çeşitleri çalışma kâğıdı: basit, bileşik ve tam sayılı kesirler, modellerle gösterme, bileşik kesri tam sayılı kesre ve tam sayılı kesri bileşik kesre çevirme. 100 soru ve cevap anahtarı.",
                "Pay paydadan büyükse bileşik kesir", "Bileşik kesir bir tam ve bir basit kesir olarak yazılabilir.", sets,
                ["Basit kesirde pay paydadan küçüktür (3/4). Bileşik kesirde pay paydaya eşit ya da büyüktür (7/4).",
                 "Tam sayılı kesir bir tam sayı ile bir basit kesirden oluşur: 1 3/4 (bir tam dörtte üç).",
                 "Bileşik kesri çevirmek için payı paydaya böleriz: bölüm tam kısım, kalan yeni pay olur. Tersini yaparken tam kısım × payda + pay."],
                [("11/4 kesrini tam sayılı kesre çevir.", ["11 ÷ 4 = 2, kalan 3"], "2 3/4"),
                 ("3 1/2 kesrini bileşik kesre çevir.", ["3 × 2 + 1 = 7"], "7/2")],
                [["3 1/2 → 4/2", "Tam kısım paydayla çarpılır: 3 × 2 + 1 = 7, cevap 7/2"], ["4/4 kesrini basit kesir sanmak", "Pay paydaya eşitse bileşik kesirdir; 1 bütüne eşittir"],
                 ["Kalanı tam kısma yazmak", "11 ÷ 4: bölüm 2 tam kısım, kalan 3 pay olur"]],
                [("Bileşik kesir her zaman 1’den büyük müdür?", "Bir bütüne eşit ya da büyüktür. 5/5 bileşik kesirdir ve 1’e eşittir."),
                 ("Tam sayılı kesir nasıl okunur?", "2 3/4 “iki tam dörtte üç” diye okunur."),
                 ("Günlük hayatta tam sayılı kesir nerede kullanılır?", "“1 buçuk ekmek”, “2 buçuk saat” gibi ifadeler tam sayılı kesirdir: 1 1/2, 2 1/2.")])


# ============================================================ 7. denk kesirler
def u7():
    def model():
        b = ch([2, 3, 4, 5])
        a = ri(1, b - 1)
        m = ch([2, 3])
        pic = "<div class='qfig'><span style='display:inline-block;margin:2px 6px'>%s</span><span style='display:inline-block;margin:2px 6px'>%s</span></div>" % (
            A.bar_frac(b, a, w=240).replace("<div class='qfig'>", "").replace("</div>", ""), A.bar_frac(b * m, a * m, w=240).replace("<div class='qfig'>", "").replace("</div>", ""))
        return mcq("Aynı büyüklükteki iki şeritte boyalı kısımlar eşittir. Üstteki şerit %s ise alttaki hangi kesirdir?%s" % (fr(a, b), pic), fr(a * m, b * m),
                   [fr(a, b * m), fr(a * m, b), fr(a + m, b + m), fr(a * m + 1, b * m)], "Parçalar %d kat çoğaldı, boyalı parçalar da %d kat: <b>%s</b>." % (m, m, fr(a * m, b * m)))

    def eksik_pay():
        b = ri(2, 6)
        a = ri(1, b - 1)
        m = ri(2, 5)
        return mcq("%s = <span class='fr'><span class='fn'>?</span><span class='fd'>%d</span></span> eşitliğinde ? yerine hangi sayı gelir?" % (fr(a, b), b * m), str(a * m),
                   [str(a + b * m - b), str(a * m + 1), str(b * m - a), str(a + m)], "Payda %d ile çarpıldı (%d × %d = %d), pay da %d ile çarpılır: <b>%d</b>." % (m, b, m, b * m, m, a * m))

    def eksik_payda():
        b = ri(2, 6)
        a = ri(1, b - 1)
        m = ri(2, 5)
        return mcq("%s = <span class='fr'><span class='fn'>%d</span><span class='fd'>?</span></span> eşitliğinde ? yerine hangi sayı gelir?" % (fr(a, b), a * m), str(b * m),
                   [str(b + a * m - a), str(b * m + 1), str(b * a), str(b + m)], "Pay %d ile çarpıldı, payda da %d ile çarpılır: %d × %d = <b>%d</b>." % (m, m, b, m, b * m))

    def hangisi():
        b = ri(2, 6)
        a = ri(1, b - 1)
        m = ri(2, 4)
        w = [fr(a + m, b + m), fr(a * m, b * m + 1), fr(a * m, b + m), fr(a + 1, b * m)]
        return mcq("Hangisi %s kesrine denktir?" % fr(a, b), fr(a * m, b * m), w, "Pay ve payda aynı sayıyla (%d) çarpılır: <b>%s</b>." % (m, fr(a * m, b * m)))

    def denk_degil():
        b = ri(2, 5)
        a = ri(1, b - 1)
        ms = sh([2, 3, 4, 5])[:3]
        goods = [fr(a * m, b * m) for m in ms]
        bad = fr(a * ms[0] + 1, b * ms[0])
        return mcq("Hangisi %s kesrine denk <b>değildir</b>?" % fr(a, b), bad, goods, "Diğerlerinde pay ve payda aynı sayıyla çarpılmış. <b>%s</b> denk değil." % bad)

    def hayat():
        nm1, nm2 = G.K.two()
        b = ch([2, 3, 4])
        a = ri(1, b - 1)
        m = ch([2, 3])
        what, acc = ch([("pizza", "pizzasını"), ("pasta", "pastasını"), ("çikolata", "çikolatasını"), ("börek", "böreğini"), ("kek", "kekini")])
        return mcq("Aynı büyüklükte iki %s var. %s kendi %s %d eş parçaya bölüp %d parçasını, %s de %d eş parçaya bölüp birkaç parçasını yedi. İkisi eşit miktar yediyse %s kaç parça yemiştir?" % (
            what, nm1, acc, b, a, nm2, b * m, nm2),
            str(a * m), [str(a), str(a + m), str(a * m + 1)], "%s = %s. %s <b>%d</b> parça yedi." % (fr(a, b), fr(a * m, b * m), nm2, a * m))

    sets = [("Modellerle denk kesirler", [(model, 20)]),
            ("Eksik payı bulma", [(eksik_pay, 20)]),
            ("Eksik paydayı bulma", [(eksik_payda, 20)]),
            ("Hangisi denk?", [(hangisi, 10), (denk_degil, 10)]),
            ("Günlük hayatta denk kesirler", [(hayat, 10), (hangisi, 5), (eksik_pay, 5)])]
    return unit("denk-kesirler", "S", "MAT.4.1.7", 7, "Denk Kesirler", "Denk Kesirler",
                "Denk kesirlerin gösterimlerini tanır, günlük hayattaki durumlara uygun gösterimleri belirler ve kullanır.",
                "4. sınıf denk kesirler çalışma kâğıdı: modellerle denk kesirler, eksik pay ve paydayı bulma, denk kesirleri seçme ve problemler. 100 soru ve cevap anahtarı.",
                "Pay ve payda aynı sayıyla çarpılır", "Denk kesirler aynı büyüklüğü farklı yazar.", sets,
                ["Denk kesirler bir bütünün aynı büyüklükteki kısmını gösterir: 1/2 = 2/4 = 3/6.",
                 "Bir kesrin pay ve paydasını aynı sayıyla çarparsak denk bir kesir elde ederiz.",
                 "Eksik sayıyı bulurken önce pay ya da paydanın kaç katına çıktığına bakarız."],
                [("2/3 = ?/12", ["3 × 4 = 12", "2 × 4 = 8"], "8"), ("1/4 kesrine denk bir kesir", ["Pay ve payda 3 ile çarpılır"], "3/12")],
                [["1/2 = 2/3 (paya ve paydaya 1 eklemek)", "Toplamak değil çarpmak gerekir: 1/2 = 2/4"], ["Yalnızca paydayı çarpmak", "Pay ve payda aynı sayıyla çarpılır"],
                 ["Daha çok parça daha büyük kesir sanmak", "4/8 ile 1/2 aynı büyüklüktedir"]],
                [("Denk kesirler neden eşittir?", "Bütün daha küçük eş parçalara bölünür; parça sayısı artar ama boyalı alan aynı kalır."),
                 ("Bir kesrin kaç denk kesri vardır?", "Sonsuz tane: pay ve paydayı 2, 3, 4… ile çarparak yenilerini yazabiliriz."),
                 ("Denk kesirleri model olmadan nasıl kontrol ederim?", "Birinin pay ve paydası diğerininkinin aynı katı mı, ona bakarsın.")])


# ============================================================ 8. kesirleri karşılaştırma
def u8():
    def birim():
        a, b = sh(range(2, 13))[:2]
        k = ri(0, 1)
        g = fr(1, min(a, b)) if k == 0 else fr(1, max(a, b))
        return mcq("%s ve %s kesirlerinden hangisi daha %s?" % (fr(1, a), fr(1, b), "büyüktür" if k == 0 else "küçüktür"), g,
                   [fr(1, max(a, b)) if k == 0 else fr(1, min(a, b)), "İkisi eşittir", fr(1, a + b)],
                   "Birim kesirlerde payda büyüdükçe parça küçülür. Daha %s olan <b>%s</b>." % ("büyük" if k == 0 else "küçük", g))

    def sembol():
        k = ri(0, 1)
        if k == 0:
            a, b = sh(range(2, 13))[:2]
            x, y = fr(1, a), fr(1, b)
            s = "&gt;" if a < b else "&lt;"
            e = "Payları 1 olan kesirlerde paydası küçük olan büyüktür."
        else:
            d = ri(3, 12)
            a, b = sh(range(1, d))[:2] if d > 2 else (1, 2)
            x, y = fr(a, d), fr(b, d)
            s = "&gt;" if a > b else "&lt;"
            e = "Paydalar eşit; payı büyük olan büyüktür."
        return mcq("%s ○ %s karşılaştırmasında ○ yerine hangi sembol gelir?" % (x, y), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "+"], e + " Cevap <b>%s</b>." % s)

    def payda_esit():
        d = ri(5, 12)
        xs = sh(range(1, d))[:4]
        k = ri(0, 1)
        g = max(xs) if k == 0 else min(xs)
        return mcq("%s kesirlerinden en %s hangisidir?" % (", ".join(fr(x, d) for x in xs), "büyüğü" if k == 0 else "küçüğü"), fr(g, d), [fr(x, d) for x in xs if x != g],
                   "Paydalar eşit. Payı en %s olan: <b>%s</b>." % ("büyük" if k == 0 else "küçük", fr(g, d)))

    def sirala():
        k = ri(0, 1)
        if k == 0:
            ds = sorted(sh(range(2, 11))[:4])
            g = [fr(1, x) for x in ds[::-1]]
            sh_ = sh(ds)
            q = "%s birim kesirlerinin küçükten büyüğe sıralanışı hangisidir?" % ", ".join(fr(1, x) for x in sh_)
            w = [[fr(1, x) for x in ds], [fr(1, x) for x in ds[::-1][:2][::-1] + ds[::-1][2:]], [fr(1, x) for x in sh_]]
        else:
            d = ri(6, 12)
            xs = sorted(sh(range(1, d))[:4])
            g = [fr(x, d) for x in xs]
            sh_ = sh(xs)
            q = "%s kesirlerinin küçükten büyüğe sıralanışı hangisidir?" % ", ".join(fr(x, d) for x in sh_)
            w = [[fr(x, d) for x in xs[::-1]], [fr(x, d) for x in xs[1:2] + xs[:1] + xs[2:]], [fr(x, d) for x in sh_]]
        return M(q, " &lt; ".join(g), [" &lt; ".join(x) for x in w], "Doğru sıralama: <b>%s</b>." % " &lt; ".join(g))

    def model():
        a, b = sh([2, 3, 4, 6, 8])[:2]
        pic = "<div class='qfig'>%s%s</div>" % (A.bar_frac(a, 1, w=240).replace("<div class='qfig'>", "<div>"), A.bar_frac(b, 1, w=240).replace("<div class='qfig'>", "<div>"))
        g = fr(1, min(a, b))
        return mcq("Aynı uzunluktaki şeritlerden üstteki %d, alttaki %d eş parçaya bölünmüş. Bir parçası daha uzun olan hangisidir?%s" % (a, b, pic), g,
                   [fr(1, max(a, b)), "İkisi eşittir", fr(1, a * b)], "Daha az parçaya bölünen şeridin parçaları daha uzundur: <b>%s</b>." % g)

    def problem():
        n1, n2 = G.K.two()
        k = ri(0, 1)
        if k == 0:
            a, b = sh(range(2, 9))[:2]
            q = "%s bir pizzanın %s kadarını, %s aynı büyüklükteki pizzanın %s kadarını yedi. Kim daha çok yedi?" % (n1, fr(1, a), n2, fr(1, b))
            g = n1 if a < b else n2
            e = "%s &gt; %s. Paydası küçük olan birim kesir büyüktür: <b>%s</b>." % (fr(1, min(a, b)), fr(1, max(a, b)), g)
        else:
            d = ri(5, 12)
            a, b = sh(range(1, d))[:2]
            q = "%s bir kitabın %s kadarını, %s aynı kitabın %s kadarını okudu. Kim daha çok okudu?" % (n1, fr(a, d), n2, fr(b, d))
            g = n1 if a > b else n2
            e = "Paydalar eşit, payı büyük olan büyük: <b>%s</b>." % g
        other = n2 if g == n1 else n1
        return mcq(q, g, [other, "İkisi eşit okudu" if k else "İkisi eşit yedi", "Bilinemez"], e)

    sets = [("Birim kesirleri karşılaştırma", [(birim, 20)]),
            ("Büyük, küçük ve eşit sembolleri", [(sembol, 20)]),
            ("Paydaları eşit kesirler", [(payda_esit, 20)]),
            ("Kesirleri sıralama", [(sirala, 14), (model, 6)]),
            ("Problemler", [(problem, 16), (model, 4)])]
    return unit("kesirleri-karsilastirma", "S", "MAT.4.1.8, MAT.4.1.9", 8, "Birim Kesirleri ve Paydaları Eşit Kesirleri Karşılaştırma", "Kesirleri Karşılaştırma",
                "Birim kesirler arasındaki ve paydaları eşit kesirler arasındaki büyüklük-küçüklük ilişkisini çözümler.",
                "4. sınıf kesirleri karşılaştırma çalışma kâğıdı: birim kesirleri karşılaştırma, paydaları eşit kesirler, büyük ve küçük sembolleri, sıralama ve problemler. 100 soru ve cevap anahtarı.",
                "Birim kesirde payda küçükse kesir büyük", "Paydalar eşitse payı büyük olan büyüktür.", sets,
                ["Birim kesirlerin payı 1’dir. Bütünü ne kadar çok parçaya bölersek bir parça o kadar küçük olur: 1/2 &gt; 1/3 &gt; 1/4.",
                 "Paydaları eşit kesirlerde parçalar aynı büyüklüktedir. Daha çok parça alan, yani payı büyük olan kesir büyüktür: 5/8 &gt; 3/8.",
                 "Sıralarken önce kesirlerin birim kesir mi, paydaları eşit mi olduğuna bakarız."],
                [("1/5 ile 1/8 karşılaştır.", ["Paylar 1", "Paydası küçük olan büyük"], "1/5 &gt; 1/8"),
                 ("7/10 ile 3/10 karşılaştır.", ["Paydalar eşit", "Payı büyük olan büyük"], "7/10 &gt; 3/10")],
                [["1/8 &gt; 1/5 (8 büyük olduğu için)", "Payda büyüdükçe birim kesir küçülür"], ["3/10 &gt; 7/10 sanmak", "Paydalar eşitse paylar karşılaştırılır"],
                 ["Farklı bütünlerin parçalarını karşılaştırmak", "Bütünler aynı büyüklükte olmalı"]],
                [("Paydası büyük kesir neden küçük?", "Bütün daha çok parçaya bölündüğü için her parça küçülür."),
                 ("Paydaları farklı kesirler nasıl karşılaştırılır?", "4. sınıfta birim kesirleri ve paydası eşit kesirleri karşılaştırırız. Diğerleri için denk kesirler kullanılır."),
                 ("Kesirleri karşılaştırırken nelere dikkat ederim?", "Bütünlerin aynı büyüklükte olmasına ve parçaların eş olmasına.")])


# ============================================================ 9. bir çokluğun kesri
def u9():
    def basit():
        b = ri(2, 10)
        a = ri(1, b - 1)
        n = b * ri(2, 12)
        g = n // b * a
        return mcq("%s sayısının %s kadarı kaçtır?" % (num(n), fr(a, b)), num(g), [num(n // b), num(n - g), num(n * a), num(g + n // b)],
                   "%s ÷ %d = %s (bir parça), %s × %d = <b>%s</b>." % (num(n), b, num(n // b), num(n // b), a, num(g)))

    def birim():
        b = ri(2, 10)
        n = b * ri(2, 15)
        return mcq("%d bilyenin %s kadarı kaç bilyedir?" % (n, fr(1, b)), str(n // b), [str(n - n // b), str(n * b), str(n // b + b), str(b)],
                   "%d eş parçaya böleriz: %d ÷ %d = <b>%d</b>." % (b, n, b, n // b))

    def butun_birim():
        b = ri(2, 10)
        p = ri(2, 15)
        return mcq("Bir sayının %s kadarı %d ise sayının tamamı kaçtır?" % (fr(1, b), p), str(p * b), [str(p + b), str(p // b) if p % b == 0 else str(p * b + b), str(p * (b - 1)), str(p * b - 1)],
                   "1 parça %d, %d parça %d × %d = <b>%d</b>." % (p, b, p, b, p * b))

    def butun():
        b = ri(3, 9)
        a = ri(2, b - 1)
        u = ri(2, 12)
        p = a * u
        return mcq("Bir sayının %s kadarı %d ise sayının tamamı kaçtır?" % (fr(a, b), p), str(u * b), [str(p * b), str(u * a), str(p + b), str(u * (b - a))],
                   "%d parça %d ise 1 parça %d ÷ %d = %d. %d parça %d × %d = <b>%d</b>." % (a, p, p, a, u, b, u, b, u * b))

    def problem():
        nm = G.K.next()
        b = ch([2, 3, 4, 5, 6, 8, 10])
        a = ri(1, b - 1)
        u = ri(2, 20)
        n = u * b
        k = ri(0, 2)
        if k == 0:
            what, it = ch([("lira harçlığının", "lira"), ("sayfalık kitabının", "sayfa"), ("cevizin", "ceviz"), ("misketinin", "misket")])
            q = "%s %d %s %s kadarını kullandı. Kaç %s kullandı?" % (nm, n, what, fr(a, b), it)
            g = u * a
            e = "%d ÷ %d = %d, %d × %d = <b>%d</b> %s." % (n, b, u, u, a, g, it)
        elif k == 1:
            q = "%s %d sayfalık kitabının %s kadarını okudu. Okuması gereken kaç sayfa kaldı?" % (nm, n, fr(a, b))
            g = n - u * a
            e = "Okunan %d ÷ %d × %d = %d. Kalan %d − %d = <b>%d</b> sayfa." % (n, b, a, u * a, n, u * a, g)
        else:
            q = "Bir sınıftaki öğrencilerin %s kadarı kız ve kız öğrenci sayısı %d. Sınıfta kaç öğrenci vardır?" % (fr(a, b), u * a)
            g = n
            e = "%d parça %d ise 1 parça %d. Tamamı %d × %d = <b>%d</b>." % (a, u * a, u, u, b, n)
        return mcq(q, str(g), [str(x) for x in (u, n - g if n - g != g else n + u, g + u, n * a // max(1, b - a), g * 2) if x > 0], e)

    def model():
        b = ch([2, 3, 4, 5, 6])
        a = ri(1, b - 1)
        u = ri(2, 4)
        n = b * u
        pic = G.grid_shape([(i % (b * 2) if False else i % b, i // b) for i in range(n)], c=22, label="%d kare, %d sırada" % (n, u)).replace(">", ">", 1)
        return mcq("Şekildeki %d karenin %s kadarı kaç karedir?%s" % (n, fr(a, b), pic), str(u * a), [str(u), str(n - u * a) if n - u * a != u * a else str(n), str(a * b), str(u * a + 1)],
                   "%d ÷ %d = %d, %d × %d = <b>%d</b>." % (n, b, u, u, a, u * a))

    sets = [("Bir çokluğun birim kesri", [(birim, 20)]),
            ("Bir çokluğun basit kesri", [(basit, 14), (model, 6)]),
            ("Birim kesri verilen bütünü bulma", [(butun_birim, 20)]),
            ("Basit kesri verilen bütünü bulma", [(butun, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("bir-coklugun-kesri", "S", "MAT.4.1.10", 9, "Bir Çokluğun Basit Kesri ve Kesri Verilen Bütün", "Bir Çokluğun Kesri",
                "Bir çokluğun belirtilen basit kesir kadarını ve basit kesir kadarı verilen bir çokluğun tamamını bulur.",
                "4. sınıf bir çokluğun kesri çalışma kâğıdı: bir çokluğun birim ve basit kesri, kesri verilen bütünü bulma ve problemler. 100 soru ve cevap anahtarı.",
                "Önce paydaya böl, sonra payla çarp", "Bütünü bulurken önce bir parçayı bul.", sets,
                ["Bir çokluğun 3/4 kadarını bulmak için önce çokluğu 4 eş parçaya böleriz, sonra 3 parçayı alırız.",
                 "Bir çokluğun 2/5 kadarı verilmişse önce 1 parçayı buluruz (2’ye böleriz), sonra 5 parçayı buluruz (5 ile çarparız)."],
                [("24 sayısının 3/4 kadarı", ["24 ÷ 4 = 6", "6 × 3 = 18"], "18"), ("Bir sayının 2/5 kadarı 12", ["12 ÷ 2 = 6", "6 × 5 = 30"], "30")],
                [["24 sayısının 3/4 kadarı için 24 ÷ 3", "Önce paydaya böl: 24 ÷ 4 = 6, sonra 6 × 3"], ["Verilen kısmı bütün sanmak", "Kesri verilen sayı bir parçanın kaç katıdır, ona bak"],
                 ["Kalan kısmı sorarken alınan kısmı yazmak", "Kalan = bütün − alınan"]],
                [("Bir çokluğun kesri günlük hayatta nerede kullanılır?", "Harçlığın yarısını biriktirmek, kitabın 1/4 kadarını okumak gibi durumlarda."),
                 ("Bir çokluğun 4/4 kadarı nedir?", "Çokluğun tamamıdır, çünkü 4/4 bir bütündür."),
                 ("Kesri verilen bütün nasıl bulunur?", "Verilen sayıyı paya bölüp bir parçayı buluruz; sonra paydayla çarparız.")])


# ============================================================ 10. kesirlerle toplama ve çıkarma
def u10():
    def topla():
        d = ri(3, 12)
        a = ri(1, d - 2)
        b = ri(1, d - a)
        return mcq("%s + %s işleminin sonucu kaçtır?" % (fr(a, d), fr(b, d)), fr(a + b, d), [fr(a + b, d + d), fr(a * b, d), fr(a + b + 1, d), fr(a + b, d - 1)],
                   "Paydalar eşit; paylar toplanır, payda aynı kalır: <b>%s</b>." % fr(a + b, d))

    def cikar():
        d = ri(3, 12)
        a = ri(2, d)
        b = ri(1, a - 1)
        return mcq("%s − %s işleminin sonucu kaçtır?" % (fr(a, d), fr(b, d)), fr(a - b, d), [fr(a - b, 0 + d * 2) if a - b else fr(1, d), fr(a + b, d), fr(a - b + 1, d), fr(a - b, d - 1)],
                   "Paydalar eşit; paylar çıkarılır, payda aynı kalır: <b>%s</b>." % fr(a - b, d))

    def butunden():
        d = ri(3, 12)
        a = ri(1, d - 1)
        return mcq("1 − %s işleminin sonucu kaçtır?" % fr(a, d), fr(d - a, d), [fr(a, d), fr(1 - 0, d) if d - a != 1 else fr(2, d), fr(d - a, d + 1), fr(d - a + 1, d)],
                   "1 bütün = %s. %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(a, d), fr(d - a, d)))

    def eksik():
        d = ri(4, 12)
        c = ri(3, d)
        a = ri(1, c - 1)
        return mcq("%s + ? = %s ise ? yerine hangi kesir gelir?" % (fr(a, d), fr(c, d)), fr(c - a, d), [fr(c + a, d), fr(c - a, d * 2), fr(a, d), fr(c - a + 1, d)],
                   "? = %s − %s = <b>%s</b>." % (fr(c, d), fr(a, d), fr(c - a, d)))

    def problem():
        nm = G.K.next()
        d = ch([4, 5, 6, 8, 10, 12])
        k = ri(0, 2)
        if k == 0:
            a = ri(1, d - 2)
            b = ri(1, d - a - 1)
            q = "%s bir pastanın önce %s, sonra %s kadarını yedi. Pastanın ne kadarını yedi?" % (nm, fr(a, d), fr(b, d))
            g = fr(a + b, d)
            e = "%s + %s = <b>%s</b>." % (fr(a, d), fr(b, d), g)
            w = [fr(a + b, d * 2), fr(d - a - b, d), fr(a + b + 1, d)]
        elif k == 1:
            a = ri(1, d - 1)
            q = "%s bir duvarın %s kadarını boyadı. Duvarın ne kadarı boyanmadı?" % (nm, fr(a, d))
            g = fr(d - a, d)
            e = "Bütün %s. %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(a, d), g)
            w = [fr(a, d), fr(d - a, d + 1), fr(d - a + 1, d)]
        else:
            a = ri(2, d - 1)
            b = ri(1, a - 1)
            q = "Bir şişedeki suyun %s kadarı dolu. %s bunun %s kadarını içti. Şişenin ne kadarı dolu kaldı?" % (fr(a, d), nm, fr(b, d))
            g = fr(a - b, d)
            e = "%s − %s = <b>%s</b>." % (fr(a, d), fr(b, d), g)
            w = [fr(a + b, d), fr(a - b, d * 2) if a - b != 0 else fr(1, d), fr(d - a + b, d) if d - a + b != a - b else fr(a - b + 1, d)]
        return mcq(q, g, w + [fr(1, d)], e)

    def model():
        d = ch([4, 5, 6, 8])
        a = ri(1, d - 2)
        b = ri(1, d - a - 1) if d - a - 1 >= 1 else 1
        s = A.bar_frac(d, a, w=260).replace("<div class='qfig'>", "<div>") + A.bar_frac(d, b, w=260, col="#f4a261").replace("<div class='qfig'>", "<div>")
        return mcq("Şeritlerde boyalı kısımların toplamı hangi kesirdir?<div class='qfig'>%s</div>" % s, fr(a + b, d), [fr(a + b, d * 2), fr(a * b, d), fr(abs(a - b), d) if a != b else fr(d, d)],
                   "%s + %s = <b>%s</b>." % (fr(a, d), fr(b, d), fr(a + b, d)))

    sets = [("Paydaları eşit kesirlerle toplama", [(topla, 14), (model, 6)]),
            ("Paydaları eşit kesirlerle çıkarma", [(cikar, 20)]),
            ("Bütünden çıkarma", [(butunden, 20)]),
            ("Eksik kesri bulma", [(eksik, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("kesirlerle-toplama-ve-cikarma", "S", "MAT.4.1.11, MAT.4.1.12", 10, "Paydaları Eşit Kesirlerle Toplama ve Çıkarma", "Kesirlerle Toplama ve Çıkarma",
                "Paydaları eşit kesirlerle toplama ve çıkarma işlemlerini yapılandırır; bu işlemleri gerektiren günlük hayat problemlerini çözer.",
                "4. sınıf kesirlerle toplama ve çıkarma çalışma kâğıdı: paydaları eşit kesirlerle toplama ve çıkarma, bütünden çıkarma, eksik kesir ve problemler. 100 soru ve cevap anahtarı.",
                "Paylar toplanır, payda aynı kalır", "Parçalar aynı büyüklükte olduğu için payda değişmez.", sets,
                ["Paydaları eşit kesirlerde parçalar aynı büyüklüktedir. Toplarken parça sayılarını, yani payları toplarız; payda değişmez.",
                 "Çıkarırken de payları çıkarırız. 1 bütünü, paydası aynı olan bir kesir olarak yazarız: 1 = 8/8.",
                 "Problemlerde “toplam”, “birlikte” toplama; “kalan”, “fark” çıkarma işaretidir."],
                [("3/8 + 4/8", ["3 + 4 = 7", "Payda 8"], "7/8"), ("1 − 2/5", ["1 = 5/5", "5 − 2 = 3"], "3/5")],
                [["3/8 + 4/8 = 7/16", "Paydalar toplanmaz: 7/8"], ["1 − 2/5 = 1/5", "Önce 1 = 5/5 yazılır: 3/5"], ["Payları çarpmak", "Toplamada paylar toplanır"]],
                [("Neden paydaları toplamayız?", "Payda parçaların büyüklüğünü gösterir. Aynı büyüklükteki parçaları topladığımızda parça büyüklüğü değişmez."),
                 ("Toplam 1’den büyük olabilir mi?", "Evet: 5/6 + 4/6 = 9/6. Bu bileşik kesir 1 3/6 olarak da yazılabilir."),
                 ("Paydaları farklı kesirler toplanır mı?", "Önce denk kesirlerle paydalar eşitlenir. 4. sınıfta paydası eşit kesirlerle çalışırız.")])


# ============================================================ 11. uzunluk ve kütle dönüşümleri
def u11():
    UZ = [("km", "m", 1000), ("m", "cm", 100), ("cm", "mm", 10), ("m", "mm", 1000)]
    KU = [("kg", "g", 1000), ("ton", "kg", 1000)]

    def cevir():
        big, small, f = ch(UZ + KU)
        n = ri(2, 15)
        k = ri(0, 1)
        if k == 0:
            return mcq("%d %s kaç %s eder?" % (n, big, small), "%s %s" % (num(n * f), small), ["%s %s" % (num(n * f // 10), small), "%s %s" % (num(n * f * 10), small), "%s %s" % (num(n + f), small)],
                       "1 %s = %s %s. %d × %s = <b>%s %s</b>." % (big, num(f), small, n, num(f), num(n * f), small))
        return mcq("%s %s kaç %s eder?" % (num(n * f), small, big), "%d %s" % (n, big), ["%d %s" % (n * 10, big), "%s %s" % (num(n * f // 10), big), "%d %s" % (n + 1, big)],
                   "%s ÷ %s = <b>%d %s</b>." % (num(n * f), num(f), n, big))

    def bilesik():
        big, small, f = ch(UZ[:3] + KU)
        a = ri(1, 9)
        b = ri(1, f - 1) if f <= 100 else ri(1, 99) * 10
        return mcq("%d %s %s %s kaç %s eder?" % (a, big, num(b), small, small), "%s %s" % (num(a * f + b), small),
                   ["%s %s" % (num(a + b), small), "%s %s" % (num(a * f), small), "%s %s" % (num(int(str(a) + str(b))), small) if int(str(a) + str(b)) != a * f + b else "%s %s" % (num(a * f + b * 10), small)],
                   "%d %s = %s %s. %s + %s = <b>%s %s</b>." % (a, big, num(a * f), small, num(a * f), num(b), num(a * f + b), small))

    def ayir():
        big, small, f = ch(UZ[:3] + KU)
        a = ri(1, 9)
        b = ri(1, f - 1) if f <= 100 else ri(1, 99) * 10
        n = a * f + b
        return mcq("%s %s kaç %s kaç %s eder?" % (num(n), small, big, small), "%d %s %s %s" % (a, big, num(b), small),
                   ["%d %s %s %s" % (a + 1, big, num(b), small), "%s %s %d %s" % (num(b), big, a, small), "%d %s %s %s" % (a, big, num(b * 10 if b * 10 < f else b + 1), small)],
                   "%s ÷ %s = %d, kalan %s: <b>%d %s %s %s</b>." % (num(n), num(f), a, num(b), a, big, num(b), small))

    def karsilastir():
        big, small, f = ch(UZ[:3] + KU)
        a = ri(2, 9)
        b = a * f + ch([-1, 1]) * ri(1, f // 2) if f > 10 else a * f + ch([-1, 1])
        x, y = "%d %s" % (a, big), "%s %s" % (num(b), small)
        s = "&gt;" if a * f > b else "&lt;"
        return mcq("%s ○ %s karşılaştırmasında ○ yerine hangi sembol gelir?" % (x, y), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "+"],
                   "%d %s = %s %s. %s %s %s: <b>%s</b>." % (a, big, num(a * f), small, num(a * f), s, num(b), s))

    def problem():
        nm = G.K.next()
        k = ri(0, 3)
        if k == 0:
            a = ri(1, 4)
            b = ri(2, 9) * 100
            g = a * 1000 - b
            return mcq("%s %d km yürüyecek. %s metre yürüdü. Kaç metre yolu kaldı?" % (nm, a, num(b)), "%s m" % num(g), ["%s m" % num(a * 1000 + b), "%s m" % num(b), "%s m" % num(a * 100 - b if a * 100 > b else a * 1000 - b + 100)],
                       "%d km = %s m. %s − %s = <b>%s m</b>." % (a, num(a * 1000), num(a * 1000), num(b), num(g)))
        if k == 1:
            a = ri(2, 5)
            b = ri(1, 9) * 100
            n = ri(2, 5)
            g = a * 1000 - n * b
            if g <= 0:
                return None
            return mcq("%d kg unun %d paketinden her birine %s g un kondu. Geriye kaç gram un kaldı?" % (a, n, num(b)) if False else "Bir pastanede %d kg un var. Pastacı kekler için %d kez %s g un kullandı. Geriye kaç gram un kaldı?" % (a, n, num(b)),
                       "%s g" % num(g), ["%s g" % num(a * 1000 - b), "%s g" % num(n * b), "%s g" % num(g + 100)],
                       "%d kg = %s g. Kullanılan %d × %s = %s g. Kalan <b>%s g</b>." % (a, num(a * 1000), n, num(b), num(n * b), num(g)))
        if k == 2:
            a = ri(2, 9)
            n = ri(2, 6)
            g = a * 100 * n
            return mcq("Bir kumaştan %d m %s cm uzunluğunda... " % (a, 0) if False else "Bir kurdele %d m. %d eş parçaya bölünüyor. Her parça kaç santimetredir?" % (a * n, n),
                       "%d cm" % (a * 100), ["%d cm" % a, "%d cm" % (a * 10), "%d cm" % (a * 100 * n)],
                       "%d m = %s cm. %s ÷ %d = <b>%d cm</b>." % (a * n, num(a * n * 100), num(a * n * 100), n, a * 100))
        a = ri(2, 8)
        b = ri(2, 9)
        return mcq("Bir kamyonda %d ton, bir başka kamyonda %s kg yük var. İki kamyondaki yük toplam kaç kilogramdır?" % (a, num(b * 500)), "%s kg" % num(a * 1000 + b * 500),
                   ["%s kg" % num(a + b * 500), "%s kg" % num(a * 100 + b * 500), "%s kg" % num(a * 1000 - b * 500 if a * 1000 > b * 500 else a * 1000 + b * 50)],
                   "%d ton = %s kg. %s + %s = <b>%s kg</b>." % (a, num(a * 1000), num(a * 1000), num(b * 500), num(a * 1000 + b * 500)))

    sets = [("Birimleri dönüştürme", [(cevir, 20)]),
            ("Tek birimle ifade etme", [(bilesik, 20)]),
            ("İki birimle ifade etme", [(ayir, 20)]),
            ("Karşılaştırma", [(karsilastir, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("uzunluk-ve-kutle-donusumleri", "S", "MAT.4.1.13", 11, "Uzunluk ve Kütle Ölçü Birimlerini Dönüştürme", "Uzunluk ve Kütle Dönüşümleri",
                "Uzunluk ve kütle ölçme birimlerinin kendi içindeki dönüşümlerini yorumlar.",
                "4. sınıf uzunluk ve kütle dönüşümleri çalışma kâğıdı: km, m, cm, mm, ton, kg, g arasında dönüştürme, iki birimle ifade etme, karşılaştırma ve problemler. 100 soru ve cevap anahtarı.",
                "Büyük birimden küçüğe: çarp", "Küçük birimden büyüğe: böl.", sets,
                ["1 km = 1.000 m, 1 m = 100 cm, 1 cm = 10 mm. 1 ton = 1.000 kg, 1 kg = 1.000 g.",
                 "Büyük birimi küçük birime çevirirken çarparız (3 km = 3.000 m). Küçük birimi büyük birime çevirirken böleriz (4.000 g = 4 kg).",
                 "Karşılaştırmadan ya da işlem yapmadan önce ölçüleri aynı birime çeviririz."],
                [("2 m 35 cm kaç cm?", ["2 m = 200 cm", "200 + 35"], "235 cm"), ("3.250 g kaç kg kaç g?", ["3.250 ÷ 1.000 = 3, kalan 250"], "3 kg 250 g")],
                [["2 m 35 cm = 2.035 cm", "1 m = 100 cm: 200 + 35 = 235 cm"], ["4.000 g = 40 kg", "1 kg = 1.000 g: 4.000 ÷ 1.000 = 4 kg"],
                 ["Farklı birimleri doğrudan karşılaştırmak", "Önce aynı birime çevir"]],
                [("Milimetre nerede kullanılır?", "Silgi, bilye, böcek gibi çok küçük uzunlukları ölçerken."),
                 ("Ton nerede kullanılır?", "Kamyon yükü, fil, gemi gibi çok ağır kütleleri ölçerken."),
                 ("km ile m arasındaki ilişki nedir?", "1 km 1.000 metredir. Şehirler arası uzaklıklar km ile ölçülür.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11]
