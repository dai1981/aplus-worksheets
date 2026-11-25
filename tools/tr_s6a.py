# -*- coding: utf-8 -*-
"""Türkiye 6. sınıf (Maarif Modeli, Ortaokul Matematik 2026): Sayılar ve Nicelikler (1)(2) — 1〜10 単元。"""
from fractions import Fraction as F
from math import gcd
import tr_g as G
from tr_g import unit, cap, fr, ff, mf, num, dec, oku, mcq, M, wrap, text, line, NB, INK, GREEN, FILL, RED, BLUE
from tr_common import low


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def dz(x, k=None):
    return dec(float(x), k)


def bolenler(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def asal(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def carpanlar(n):
    out = []
    d = 2
    while n > 1:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    return out


def ust(fs):
    """[2, 2, 3] → 2<sup>2</sup> × 3"""
    out = []
    for p in sorted(set(fs)):
        k = fs.count(p)
        out.append("%d<sup>%d</sup>" % (p, k) if k > 1 else str(p))
    return " × ".join(out)


# ============================================================ 1. çarpanlar ve katlar
def u1():
    def bolen_sayisi():
        n = ch([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 64, 72, 80, 84, 90, 96, 100])
        b = bolenler(n)
        return mcq("%d sayısının kaç tane çarpanı (böleni) vardır?" % n, str(len(b)), [str(len(b) + x) for x in (1, -1, 2, -2) if len(b) + x > 0],
                   "%d sayısının çarpanları: %s. Toplam <b>%d</b>." % (n, ", ".join(map(str, b)), len(b)))

    def bolen_mu():
        n = ri(12, 120)
        b = bolenler(n)
        g = ch(b[1:-1]) if len(b) > 2 else None
        if g is None:
            return None
        w = [x for x in range(2, n) if n % x and x <= n // 2]
        w = sh(w)[:3]
        return G.withopts(mcq("Hangisi %d sayısının bir çarpanıdır?" % n, str(g), [str(x) for x in w], "%d ÷ %d = %d, kalan 0: <b>%d</b> bir çarpandır." % (n, g, n // g, g)), "%s sayıları veriliyor.")

    def kat():
        n = ri(3, 15)
        k = ri(2, 12)
        w = [n * k + x for x in (1, 2, -1, n // 2 + 1) if (n * k + x) % n]
        return G.withopts(mcq("Hangisi %d sayısının bir katıdır?" % n, str(n * k), [str(x) for x in w], "%d × %d = %d: <b>%d</b> bir kattır." % (n, k, n * k, n * k)), "%s sayıları veriliyor.")

    def katlar_arasi():
        n = ri(3, 12)
        lo = ri(10, 60)
        hi = lo + ri(20, 40)
        c = len([x for x in range(lo, hi + 1) if x % n == 0])
        return mcq("%d ile %d arasında (ikisi de dâhil) %d sayısının kaç katı vardır?" % (lo, hi, n), str(c), [str(c + 1), str(c - 1) if c > 1 else str(c + 2), str((hi - lo) // n + 2)],
                   "Katlar: %s. Toplam <b>%d</b>." % (", ".join(str(x) for x in range(lo, hi + 1) if x % n == 0), c))

    def dikdortgen():
        n = ch([12, 18, 20, 24, 30, 36, 40, 48])
        pairs = [(a, n // a) for a in bolenler(n) if a <= n // a]
        return mcq("%d birim kare kullanılarak kenar uzunlukları doğal sayı olan kaç farklı dikdörtgen oluşturulabilir? (2 × 3 ile 3 × 2 aynıdır.)" % n, str(len(pairs)),
                   [str(len(pairs) + 1), str(len(bolenler(n))), str(len(pairs) - 1)], "Çarpan çiftleri: %s. Toplam <b>%d</b>." % (", ".join("%d × %d" % p for p in pairs), len(pairs)))

    def problem():
        n = ch([24, 30, 36, 40, 48, 60, 72])
        b = [x for x in bolenler(n) if 1 < x < n]
        g = len(b)
        return mcq("%d öğrenci, her grupta eşit sayıda öğrenci olacak ve en az 2 grup ile her grupta en az 2 öğrenci olacak şekilde kaç farklı biçimde gruplara ayrılabilir?" % n, str(g),
                   [str(g + 2), str(len(bolenler(n))), str(g - 1)], "%d sayısının 1 ve %d dışındaki çarpanları: %s. Toplam <b>%d</b>." % (n, n, ", ".join(map(str, b)), g))

    sets = [("Çarpan sayısı", [(bolen_sayisi, 20)]),
            ("Çarpan mı?", [(bolen_mu, 20)]),
            ("Kat mı?", [(kat, 12), (katlar_arasi, 8)]),
            ("Çarpan çiftleri ve dikdörtgenler", [(dikdortgen, 8), (katlar_arasi, 12)]),
            ("Problemler", [(problem, 7), (bolen_mu, 7), (kat, 6)])]
    return unit("carpanlar-ve-katlar", "S", "MAT.6.1.1", 1, "Çarpanlar ve Katlar", "Çarpanlar ve Katlar",
                "Doğal sayıların çarpanları ve katlarına ilişkin akıl yürütür; çarpan ve katlarla ilgili genellemeler yapar ve modellerle test eder.",
                "6. sınıf çarpanlar ve katlar çalışma kâğıdı: bir sayının çarpanlarını (bölenlerini) bulma, çarpan sayısı, katlar, çarpan çiftleri ve dikdörtgen modeli, gruplama problemleri. 100 soru ve cevap anahtarı.",
                "Çarpan: sayıyı kalansız böler", "Kat: sayının bir doğal sayıyla çarpımı.", sets,
                ["Bir sayıyı kalansız bölen doğal sayılara o sayının çarpanları (bölenleri) denir. 12’nin çarpanları: 1, 2, 3, 4, 6, 12.",
                 "Bir sayının doğal sayılarla çarpımına o sayının katları denir. 5’in katları: 0, 5, 10, 15…",
                 "Çarpanları çiftler hâlinde buluruz: 12 = 1 × 12 = 2 × 6 = 3 × 4. Her çift, alanı 12 birim kare olan bir dikdörtgen verir."],
                [("18 sayısının çarpanları", ["1 × 18, 2 × 9, 3 × 6"], "1, 2, 3, 6, 9, 18"), ("20 ile 40 arasında 7’nin katları", ["21, 28, 35"], "3 tane")],
                [["1’i ve sayının kendisini çarpan saymamak", "Her sayı 1’e ve kendisine bölünür"], ["Çarpan ile katı karıştırmak", "Çarpanlar sayıdan büyük olamaz; katlar sayıdan küçük olamaz (0 hariç)"],
                 ["Çarpan çiftlerini eksik bulmak", "1’den başlayıp sırayla dene"]],
                [("Her sayının çarpanı 1 midir?", "Evet. 1 her doğal sayıyı böler."),
                 ("Bir sayının katları sonlu mudur?", "Hayır, katlar sonsuza kadar devam eder; çarpanlar ise sınırlıdır."),
                 ("Çarpanlar günlük hayatta nerede kullanılır?", "Eşit gruplar oluşturmada, paylaştırmada ve dikdörtgen düzenlerde.")])


# ============================================================ 2. bölünebilme kuralları
KURAL = {2: "Birler basamağı çift (0, 2, 4, 6, 8) olan sayılar 2 ile bölünür.", 3: "Rakamları toplamı 3’ün katı olan sayılar 3 ile bölünür.",
         4: "Son iki basamağı 4’ün katı (veya 00) olan sayılar 4 ile bölünür.", 5: "Birler basamağı 0 veya 5 olan sayılar 5 ile bölünür.",
         6: "Hem 2 hem 3 ile bölünen sayılar 6 ile bölünür.", 9: "Rakamları toplamı 9’un katı olan sayılar 9 ile bölünür.", 10: "Birler basamağı 0 olan sayılar 10 ile bölünür."}


def u2():
    def hangisi():
        d = ch(list(KURAL))
        g = ri(100, 9999) // d * d
        if g < 100:
            return None
        w = [x for x in (g + 1, g + 2, g - 1, g + d // 2 + 1, g + 3) if x % d]
        return G.withopts(mcq("Hangi sayı %d ile kalansız bölünür?" % d, num(g), [num(x) for x in w], "%s <b>%s</b>." % (KURAL[d], num(g))), "%s sayıları veriliyor.")

    def hangi_bolen():
        n = ri(100, 9999)
        ds = [d for d in (2, 3, 4, 5, 6, 9, 10) if n % d == 0]
        nds = [d for d in (2, 3, 4, 5, 6, 9, 10) if n % d]
        if not ds or len(nds) < 3:
            return None
        g = ch(ds)
        return mcq("%s sayısı aşağıdakilerden hangisine kalansız bölünür?" % num(n), str(g), [str(x) for x in sh(nds)[:3]], KURAL[g] + " <b>%d</b>." % g)

    def rakam():
        d = ch([3, 9, 4, 6, 5, 2])
        n = ri(100, 999)
        s = str(n)
        j = ri(1, len(s) - 1)
        ops = [int(s[:j] + str(x) + s[j + 1:]) for x in range(10)]
        good = [x for x in range(10) if ops[x] % d == 0]
        if len(good) != 1 and d != 5:
            return None
        if not good:
            return None
        g = good[0] if d != 5 else ch(good)
        masked = s[:j] + "□" + s[j + 1:]
        bad = [x for x in range(10) if ops[x] % d][:6]
        return mcq("%s sayısı %d ile kalansız bölünebiliyorsa □ yerine hangi rakam gelebilir?" % (masked, d), str(g), [str(x) for x in sh(bad)[:3]],
                   "%s □ = %d olunca sayı %s olur. <b>%d</b>." % (KURAL[d], g, num(ops[g]), g))

    def kalan():
        d = ch([2, 3, 5, 9, 10])
        n = ri(1000, 99999)
        r = n % d
        return mcq("%s sayısının %d ile bölümünden kalan kaçtır?" % (num(n), d), str(r), [str(x) for x in range(d) if x != r][:4] if d > 2 else ["1" if r == 0 else "0", "2", "3"],
                   ("Rakamları toplamı %d; %d ile bölümünden kalan <b>%d</b>." % (sum(map(int, str(n))), d, r)) if d in (3, 9) else
                   ("Birler basamağına bakarız: <b>%d</b>." % r))

    def kural():
        d = ch(list(KURAL))
        return mcq("%d ile bölünebilme kuralı hangisidir?" % d, KURAL[d], [KURAL[x] for x in KURAL if x != d], "<b>%s</b>" % KURAL[d])

    def problem():
        n = ri(100, 500)
        d = ch([3, 4, 5, 6, 9])
        r = n % d
        return mcq("%d ceviz %d kişiye eşit paylaştırılmak isteniyor. Hiç ceviz artmaması için en az kaç ceviz daha gerekir?" % (n, d), str((d - r) % d),
                   [str(r), str(d), str((d - r) % d + 1)], "%d ÷ %d → kalan %d. %d ceviz eklenirse kalan 0 olur: <b>%d</b>." % (n, d, r, (d - r) % d, (d - r) % d))

    sets = [("Hangisi bölünür?", [(hangisi, 20)]),
            ("Bölenleri bulma", [(hangi_bolen, 20)]),
            ("Eksik rakam", [(rakam, 20)]),
            ("Kalanı bulma", [(kalan, 20)]),
            ("Kurallar ve problemler", [(kural, 7), (problem, 13)])]
    return unit("bolunebilme-kurallari", "S", "MAT.6.1.2", 2, "2, 3, 4, 5, 6, 9 ve 10 ile Bölünebilme", "Bölünebilme Kuralları",
                "2, 3, 4, 5, 6, 9 ve 10 ile bölünebilme kurallarına ilişkin akıl yürütür; kuralları basamak değerleri ve katlarla genelleyip test eder.",
                "6. sınıf bölünebilme kuralları çalışma kâğıdı: 2, 3, 4, 5, 6, 9 ve 10 ile bölünebilme, eksik rakamı bulma, kalanı bulma ve paylaştırma problemleri. 100 soru ve cevap anahtarı.",
                "Rakam toplamı 3’e bölünüyorsa sayı da", "2, 5, 10 için son basamağa; 3, 9 için rakam toplamına bak.", sets,
                ["2, 5 ve 10 ile bölünebilmede birler basamağına bakarız. 4 ile bölünebilmede son iki basamağa bakarız.",
                 "3 ve 9 ile bölünebilmede rakamların toplamına bakarız: toplam 3’ün (9’un) katıysa sayı da öyledir.",
                 "6 ile bölünen sayılar hem 2 hem 3 ile bölünür."],
                [("2.376 sayısı 9 ile bölünür mü?", ["2 + 3 + 7 + 6 = 18", "18, 9’un katı"], "Evet"), ("5.134 sayısı 4 ile bölünür mü?", ["Son iki basamak 34", "34, 4’ün katı değil"], "Hayır")],
                [["4 ile bölünmede yalnızca son basamağa bakmak", "Son iki basamağa bak"], ["6 ile bölünmede yalnızca çift olmaya bakmak", "3 ile de bölünmeli"],
                 ["9 ile bölünen her sayıyı 3’e bölünmez sanmak", "9’a bölünen her sayı 3’e de bölünür"]],
                [("Bölünebilme kuralları ne işe yarar?", "Bölme yapmadan bir sayının bölünüp bölünmediğini hızlıca anlamamızı sağlar."),
                 ("3 ile bölünen her sayı 9 ile bölünür mü?", "Hayır. 12 sayısı 3 ile bölünür ama 9 ile bölünmez."),
                 ("Kalanı nasıl bulurum?", "3 ve 9 için rakamlar toplamının kalanı, 2, 5 ve 10 için birler basamağının kalanı aynıdır.")])


# ============================================================ 3. asal sayılar ve asal çarpanlar
def u3():
    def asal_mi():
        ps = [p for p in range(2, 100) if asal(p)]
        cs = [c for c in range(4, 100) if not asal(c)]
        k = ri(0, 1)
        if k == 0:
            g = ch(ps)
            w = sh([c for c in cs if abs(c - g) < 20])[:3]
            return G.withopts(mcq("Hangisi asal sayıdır?", str(g), [str(x) for x in w], "%d yalnızca 1’e ve kendisine bölünür: <b>%d</b> asaldır." % (g, g)), "%s sayıları veriliyor.")
        g = ch(cs)
        w = sh([p for p in ps if abs(p - g) < 25])[:3]
        return G.withopts(mcq("Hangisi asal sayı <b>değildir</b>?", str(g), [str(x) for x in w], "%d sayısının 1 ve kendisinden başka çarpanı var (%d = %s): <b>%d</b>." % (g, g, " × ".join(map(str, carpanlar(g))), g)), "%s sayıları veriliyor.")

    def kac_asal():
        lo = ri(1, 60)
        hi = lo + ri(10, 25)
        ps = [p for p in range(lo, hi + 1) if asal(p)]
        return mcq("%d ile %d arasında (ikisi de dâhil) kaç asal sayı vardır?" % (lo, hi), str(len(ps)), [str(len(ps) + x) for x in (1, -1, 2) if len(ps) + x >= 0] + ["%d" % (len(ps) + 3)],
                   "Asal sayılar: %s. Toplam <b>%d</b>." % (", ".join(map(str, ps)) or "yok", len(ps)))

    def asal_carpan():
        n = ri(12, 300)
        fs = carpanlar(n)
        if len(fs) < 2 or len(set(fs)) < 2:
            return None
        g = ", ".join(map(str, sorted(set(fs))))
        alts = [", ".join(map(str, sorted(set(fs) | {x}))) for x in (2, 3, 5, 7) if x not in fs][:2] + [", ".join(map(str, sorted(set(fs))[:-1])), ", ".join(str(x) for x in bolenler(n)[1:4])]
        return mcq("%d sayısının asal çarpanları hangileridir?" % n, g, alts, "%d = %s. Asal çarpanlar: <b>%s</b>." % (n, " × ".join(map(str, fs)), g))

    def carpanlarina():
        n = ri(12, 500)
        fs = carpanlar(n)
        if len(fs) < 3:
            return None
        g = ust(fs)
        bad1 = ust(fs[:-1] + [fs[-1] + 2 if asal(fs[-1] + 2) else fs[-1] + 4])
        bad2 = ust(fs[1:]) if len(fs) > 3 else ust(fs + [2])
        bad3 = " × ".join(map(str, bolenler(n)[1:3]))
        return mcq("%d sayısının asal çarpanlarının çarpımı biçiminde yazılışı hangisidir?" % n, g, [bad1, bad2, bad3], "Asal sayılara bölerek ilerleriz: %d = <b>%s</b>." % (n, g))

    def tersi():
        fs = sorted([ch([2, 2, 3, 3, 5, 7, 11]) for _ in range(ri(3, 4))])
        n = 1
        for f in fs:
            n *= f
        if n > 2000:
            return None
        return mcq("Asal çarpanlarının çarpımı %s olan sayı kaçtır?" % ust(fs), num(n), [num(n * 2), num(n // fs[0] if n // fs[0] != n else n + 1), num(sum(fs)), num(n + fs[-1])],
                   "%s = <b>%s</b>." % (" × ".join(map(str, fs)), num(n)))

    def ozellik():
        S = [("En küçük asal sayı hangisidir?", "2", ["1", "3", "0"]), ("Çift olan tek asal sayı hangisidir?", "2", ["4", "0", "6"]),
             ("1 sayısı asal mıdır?", "Hayır, 1 asal değildir", ["Evet, 1 asaldır", "Bazen asaldır", "1 bileşik sayıdır"]),
             ("Bir asal sayının kaç tane çarpanı vardır?", "2", ["1", "3", "Sonsuz"]), ("İki basamaklı en küçük asal sayı hangisidir?", "11", ["10", "13", "12"]),
             ("İki basamaklı en büyük asal sayı hangisidir?", "97", ["99", "91", "93"])]
        q, g, w = ch(S)
        return mcq(q, g, w, "Asal sayılar yalnızca 1’e ve kendisine bölünür; 1 asal değildir, 2 en küçük ve tek çift asal sayıdır: <b>%s</b>." % g)

    sets = [("Asal mı, bileşik mi?", [(asal_mi, 20)]),
            ("Aralıktaki asal sayılar", [(kac_asal, 14), (ozellik, 6)]),
            ("Asal çarpanlar", [(asal_carpan, 20)]),
            ("Asal çarpanlarına ayırma", [(carpanlarina, 20)]),
            ("Asal çarpanlardan sayıya", [(tersi, 20)])]
    return unit("asal-sayilar-ve-asal-carpanlar", "S", "MAT.6.1.3", 3, "Asal Sayılar ve Asal Çarpanlar", "Asal Sayılar",
                "Bir sayının asal olup olmadığını ve asal çarpanlarını belirler; asal sayıların özelliklerini ve çarpanlarla ilişkisini açıklar.",
                "6. sınıf asal sayılar çalışma kâğıdı: asal ve bileşik sayılar, aralıktaki asal sayılar, asal çarpanlar, sayıyı asal çarpanlarına ayırma ve üslü yazma. 100 soru ve cevap anahtarı.",
                "Asal: yalnız 1’e ve kendisine bölünür", "1 asal değildir; 2 tek çift asal sayıdır.", sets,
                ["Yalnızca 1’e ve kendisine bölünen, 1’den büyük doğal sayılara asal sayı denir: 2, 3, 5, 7, 11, 13…",
                 "Bir sayıyı asal çarpanlarına ayırmak için en küçük asal sayıdan başlayarak böleriz: 60 = 2 × 2 × 3 × 5 = 2<sup>2</sup> × 3 × 5.",
                 "Bir sayının asal çarpanları, onu bölen asal sayılardır. 60’ın asal çarpanları 2, 3 ve 5’tir."],
                [("84 sayısını asal çarpanlarına ayır", ["84 ÷ 2 = 42", "42 ÷ 2 = 21", "21 ÷ 3 = 7"], "2<sup>2</sup> × 3 × 7"), ("51 asal mı?", ["51 = 3 × 17"], "Hayır")],
                [["1’i asal saymak", "Asal sayının tam iki çarpanı vardır; 1’in tek çarpanı var"], ["Bütün tek sayıları asal sanmak", "9, 15, 21 tek ama asal değil"],
                 ["Asal çarpanları yazarken tekrar edenleri unutmak", "60 = 2 × 2 × 3 × 5"]],
                [("Asal sayılar sonsuz mudur?", "Evet. Ne kadar ilerlersek ilerleyelim yeni asal sayılar vardır."),
                 ("Bir sayının asal olup olmadığını nasıl anlarım?", "Kareköküne kadar olan asal sayılara bölmeyi denersin; hiçbirine bölünmüyorsa asaldır."),
                 ("Bileşik sayı nedir?", "1’den büyük olup asal olmayan sayılardır; ikiden fazla çarpanları vardır.")])


# ============================================================ 4. ortak bölenler ve ortak katlar
def u4():
    def ortak_bolen():
        a, b = sh([12, 16, 18, 20, 24, 30, 32, 36, 40, 42, 48, 54, 60])[:2]
        c = sorted(set(bolenler(a)) & set(bolenler(b)))
        k = ri(0, 1)
        if k == 0:
            return mcq("%d ve %d sayılarının ortak bölenleri hangileridir?" % (a, b), ", ".join(map(str, c)),
                       [", ".join(map(str, c[:-1])) if len(c) > 1 else "2", ", ".join(map(str, sorted(set(c) | {a // c[-1] * 1 if a // c[-1] not in c else 7}))), ", ".join(map(str, bolenler(a)[:len(c) + 1]))],
                       "%d: %s; %d: %s. Ortak olanlar: <b>%s</b>." % (a, ", ".join(map(str, bolenler(a))), b, ", ".join(map(str, bolenler(b))), ", ".join(map(str, c))))
        return mcq("%d ve %d sayılarının en büyük ortak böleni kaçtır?" % (a, b), str(c[-1]), [str(x) for x in (c[-2] if len(c) > 1 else 1, a * b // c[-1], c[-1] * 2, min(a, b))],
                   "Ortak bölenler %s. En büyüğü <b>%d</b>." % (", ".join(map(str, c)), c[-1]))

    def ortak_kat():
        a, b = sh([2, 3, 4, 5, 6, 8, 9, 10, 12, 15])[:2]
        l = a * b // gcd(a, b)
        k = ri(0, 1)
        if k == 0:
            return mcq("%d ve %d sayılarının en küçük ortak katı kaçtır? (0 hariç)" % (a, b), str(l), [str(x) for x in (a * b if a * b != l else l * 2, l + min(a, b), max(a, b), l // 2 if l // 2 % a and l // 2 > 0 else l + a)],
                       "%d: %s…; %d: %s… İlk ortak kat <b>%d</b>." % (a, ", ".join(str(a * i) for i in range(1, l // a + 1)), b, ", ".join(str(b * i) for i in range(1, l // b + 1)), l))
        n = ri(2, 4)
        return mcq("%d ve %d sayılarının 100’den küçük ortak katlarından kaç tanesi vardır? (0 hariç)" % (a, b), str(99 // l), [str(99 // l + 1), str(99 // l - 1) if 99 // l > 1 else "4", str(99 // a)],
                   "Ortak katlar %d’in katlarıdır: %s. Toplam <b>%d</b>." % (l, ", ".join(str(l * i) for i in range(1, 99 // l + 1)), 99 // l) if l < 10 else
                   "Ortak katlar %d sayısının katlarıdır: %s. Toplam <b>%d</b>." % (l, ", ".join(str(l * i) for i in range(1, 99 // l + 1)), 99 // l))

    def aralarinda_asal():
        k = ri(0, 1)
        pairs = [(a, b) for a in range(2, 30) for b in range(a + 1, 31)]
        cop = [(a, b) for a, b in pairs if gcd(a, b) == 1]
        ncop = [(a, b) for a, b in pairs if gcd(a, b) > 1]
        if k == 0:
            g = ch(cop)
            w = sh(ncop)[:3]
            return G.withopts(mcq("Hangi sayı çifti aralarında asaldır?", "(%d, %d)" % g, ["(%d, %d)" % x for x in w], "%d ve %d sayılarının 1’den başka ortak böleni yoktur: <b>aralarında asal</b>." % g), "Sayı çiftleri: %s.")
        g = ch(ncop)
        w = sh(cop)[:3]
        cb = gcd(*g)
        return G.withopts(mcq("Hangi sayı çifti aralarında asal <b>değildir</b>?", "(%d, %d)" % g, ["(%d, %d)" % x for x in w], "%d ve %d sayılarının ortak böleni %d: aralarında asal değil." % (g[0], g[1], cb)), "Sayı çiftleri: %s.")

    def problem_bolen():
        g = ri(2, 9)
        a, b = g * ri(2, 9), g * ri(2, 9)
        if gcd(a, b) != g or a == b:
            return None
        return mcq("%d kırmızı ve %d mavi bilye, her pakette aynı renkten eşit sayıda bilye olacak ve hiç bilye artmayacak şekilde paketlenecek. Bir pakette en çok kaç bilye olabilir?" % (a, b),
                   str(g), [str(x) for x in (a * b // g, min(a, b), g * 2, 1)], "%d ve %d sayılarının en büyük ortak böleni <b>%d</b>." % (a, b, g))

    def problem_kat():
        a, b = sh([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])[:2]
        l = a * b // gcd(a, b)
        if l > 120:
            return None
        return mcq("Bir otobüs %d dakikada bir, diğeri %d dakikada bir duraktan kalkıyor. İkisi birlikte kalktıktan en az kaç dakika sonra yine birlikte kalkarlar?" % (a, b), "%d dakika" % l,
                   ["%d dakika" % x for x in (a + b, a * b if a * b != l else l * 2, max(a, b), l // 2 if l // 2 > max(a, b) else l + 10)],
                   "%d ve %d sayılarının en küçük ortak katı <b>%d</b>." % (a, b, l))

    sets = [("Ortak bölenler", [(ortak_bolen, 20)]),
            ("Ortak katlar", [(ortak_kat, 20)]),
            ("Aralarında asal sayılar", [(aralarinda_asal, 20)]),
            ("Paketleme problemleri", [(problem_bolen, 20)]),
            ("Birlikte olma problemleri", [(problem_kat, 20)])]
    return unit("ortak-bolenler-ve-ortak-katlar", "S", "MAT.6.1.4", 4, "Ortak Bölenler, Ortak Katlar ve Aralarında Asal Sayılar", "Ortak Bölenler ve Katlar",
                "İki doğal sayının ortak katlarını ve ortak bölenlerini inceler; bunları şema, tablo veya sayı doğrusuyla gösterir ve kendi ifadeleriyle açıklar.",
                "6. sınıf ortak bölenler ve ortak katlar çalışma kâğıdı: iki sayının ortak bölenleri ve en büyüğü, ortak katları ve en küçüğü, aralarında asal sayılar, paketleme ve birlikte olma problemleri. 100 soru ve cevap anahtarı.",
                "İki listede ortak olanları bul", "Ortak bölen tek olarak 1 ise sayılar aralarında asaldır.", sets,
                ["İki sayının bölenlerini ayrı ayrı yazar, ikisinde de bulunanları seçeriz: bunlar ortak bölenlerdir.",
                 "İki sayının katlarını yazarak ikisinde de bulunanları buluruz: bunlar ortak katlardır. İlk ortak kat iki olayın yeniden birlikte olacağı zamanı verir.",
                 "1’den başka ortak böleni olmayan iki sayıya aralarında asal sayılar denir: 8 ve 15 gibi."],
                [("12 ve 18 sayılarının ortak bölenleri", ["12: 1, 2, 3, 4, 6, 12", "18: 1, 2, 3, 6, 9, 18"], "1, 2, 3, 6"), ("4 ve 6 sayılarının ilk ortak katı", ["4: 4, 8, 12", "6: 6, 12"], "12")],
                [["Ortak katı bulmak için sayıları çarpmak", "4 × 6 = 24 bir ortak kattır ama en küçüğü 12’dir"], ["Aralarında asal sayıların asal olması gerektiğini sanmak", "8 ve 15 asal değil ama aralarında asaldır"],
                 ["Paketleme sorusunda ortak kat kullanmak", "Bölme ve paylaştırma → ortak bölen; birlikte olma → ortak kat"]],
                [("Ortak bölen ve ortak kat ne zaman kullanılır?", "Eşit paylaştırmada ortak bölen, tekrar eden olayların birlikte olmasında ortak kat kullanılır."),
                 ("İki asal sayı her zaman aralarında asal mıdır?", "Farklı iki asal sayı her zaman aralarında asaldır."),
                 ("1 ile her sayı aralarında asal mıdır?", "Evet, çünkü tek ortak bölenleri 1’dir.")])


# ============================================================ 5. ondalık gösterim ve basamak değeri
def u5():
    def bas_degeri():
        v = ri(10001, 999999) / 1000.0
        s = "%.3f" % v
        ip, fp = s.split(".")
        j = ri(0, 2)
        d = fp[j]
        if d == "0" or (ip + fp).count(d) > 1:
            return None
        val = int(d) * 10 ** (-(j + 1))
        g = dec(val)
        return mcq("%s sayısında %s rakamının basamak değeri kaçtır?" % (dec(v, 3), d), g, [dec(val * 10), dec(val / 10), d],
                   "%s rakamı %s basamağında: <b>%s</b>." % (d, ["onda birler", "yüzde birler", "binde birler"][j], g))

    def cozum():
        a, b, c, d = ri(1, 99), ri(1, 9), ri(0, 9), ri(1, 9)
        v = a + b / 10.0 + c / 100.0 + d / 1000.0
        g = "%d + %s + %s + %s" % (a, fr(b, 10), fr(c, 100), fr(d, 1000)) if c else "%d + %s + %s" % (a, fr(b, 10), fr(d, 1000))
        w = ["%d + %s + %s + %s" % (a, fr(b, 100), fr(c, 1000), fr(d, 10)) if c else "%d + %s + %s" % (a, fr(b, 100), fr(d, 10)),
             "%d + %s" % (a, fr(b * 100 + c * 10 + d, 100)), "%d + %s + %s + %s" % (a, fr(d, 10), fr(c, 100), fr(b, 1000)) if c else "%d + %s + %s" % (a, fr(d, 10), fr(b, 1000))]
        return mcq("%s sayısının çözümlenmiş hâli hangisidir?" % dec(v, 3), g, w, "Her rakam basamağının kesriyle yazılır: <b>%s</b>." % g)

    def kesirden():
        a = ri(1, 9999)
        den = ch([10, 100, 1000])
        if a % 10 == 0:
            return None
        v = a / float(den)
        return mcq("%s kesrinin ondalık gösterimi hangisidir?" % fr(a, den), dec(v), [dec(v * 10), dec(v / 10), "%d,%d" % (a, den)], "Paydadaki sıfır sayısı kadar basamak: <b>%s</b>." % dec(v))

    def karsilastir():
        a = ri(100, 9999) / 1000.0
        b = round(a + ch([0.1, -0.01, 0.001, 0.09, -0.2]), 3)
        if b <= 0:
            return None
        s = "&gt;" if a > b else "&lt;"
        return mcq("%s ○ %s karşılaştırmasında ○ yerine hangi sembol gelir?" % (dec(a), dec(b)), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "+"],
                   "Önce tam kısımlar, sonra onda birler, yüzde birler ve binde birler karşılaştırılır: <b>%s</b>." % s)

    def yuvarla():
        n = ri(1001, 99999)
        k = ri(0, 1)
        if k == 0:
            g = (n + 50) // 100
            gs = F(g, 10)
            alts = [F(g + 1, 10), F(g - 1, 10), F((n + 500) // 1000, 1), F((n + 5) // 10, 100)]
            return mcq("%s sayısını onda birler basamağına yuvarlayınız." % dec(n / 1000.0, 3), dz(gs), [dz(x) for x in alts if x != gs],
                       "Yüzde birler basamağına bakarız; 5 ve üstüyse yukarı yuvarlanır: <b>%s</b>." % dz(gs))
        g = (n + 5) // 10
        gs = F(g, 100)
        alts = [F(g + 1, 100), F(g - 1, 100), F((n + 50) // 100, 10), F(n, 1000)]
        return mcq("%s sayısını yüzde birler basamağına yuvarlayınız." % dec(n / 1000.0, 3), dz(gs), [dz(x) for x in alts if x != gs],
                   "Binde birler basamağına bakarız: <b>%s</b>." % dz(gs))

    sets = [("Basamak değeri", [(bas_degeri, 20)]),
            ("Çözümleme", [(cozum, 20)]),
            ("Kesirden ondalık gösterime", [(kesirden, 20)]),
            ("Karşılaştırma", [(karsilastir, 20)]),
            ("Yuvarlama", [(yuvarla, 20)])]
    return unit("ondalik-gosterimde-basamak-degeri", "S", "MAT.6.1.5", 5, "Ondalık Gösterimde Basamak Değeri ve Çözümleme", "Ondalık Gösterim",
                "Ondalık gösterimlerdeki basamak değerlerini inceler; ondalık gösterimleri paydası 10, 100, 1000 olan kesirlerin toplamı olarak yazar.",
                "6. sınıf ondalık gösterim çalışma kâğıdı: onda birler, yüzde birler ve binde birler basamak değeri, çözümleme, kesirden ondalık gösterime, karşılaştırma ve yuvarlama. 100 soru ve cevap anahtarı.",
                "Virgülden sonra: onda, yüzde, binde", "Her basamak bir öncekinin onda biridir.", sets,
                ["Virgülden sonraki basamaklar onda birler (1/10), yüzde birler (1/100) ve binde birler (1/1000) basamaklarıdır.",
                 "Ondalık gösterimi çözümleyebiliriz: 3,407 = 3 + 4/10 + 0/100 + 7/1000.",
                 "Karşılaştırırken önce tam kısma, sonra soldan sağa ondalık basamaklara bakarız."],
                [("5,286 sayısında 8’in basamak değeri", ["8 yüzde birler basamağında", "8/100"], "0,08"), ("2,749 onda birlere yuvarla", ["Yüzde birler 4: aşağı"], "2,7")],
                [["0,5 &lt; 0,45 (45 &gt; 5)", "Basamakları eşitle: 0,50 &gt; 0,45"], ["Basamak değerini rakamın kendisi sanmak", "0,08’deki 8’in değeri 8/100’dür"],
                 ["Yuvarlarken yanlış basamağa bakmak", "Yuvarlanacak basamağın bir sağındaki rakama bak"]],
                [("Virgülden sonra kaç basamak olabilir?", "İstediğimiz kadar; 6. sınıfta en çok binde birler basamağını kullanırız."),
                 ("2,50 ile 2,5 farklı mıdır?", "Hayır, sondaki sıfırlar değeri değiştirmez."),
                 ("Ondalık gösterimler nerede kullanılır?", "Para, uzunluk, kütle ve sınav puanları gibi ölçümlerde.")])


# ============================================================ 6. kesir ve bölme ilişkisi
def ondalik_str(a, b):
    """a/b → '0,25' ya da devirli '0,<ov>3</ov>'"""
    q, r = divmod(a, b)
    digits = []
    seen = {}
    while r and r not in seen:
        seen[r] = len(digits)
        r *= 10
        digits.append(str(r // b))
        r %= b
    if not r:
        return num(q) + ("," + "".join(digits) if digits else ""), False
    i = seen[r]
    return num(q) + "," + "".join(digits[:i]) + "<span class='ov'>%s</span>" % "".join(digits[i:]), True


def u6():
    def bolme():
        a, b = ri(1, 30), ch([2, 4, 5, 8, 10, 20, 25])
        if a % b == 0:
            return None
        g, _ = ondalik_str(a, b)
        return mcq("%s kesrinin ondalık gösterimi hangisidir? (Payı paydaya böl.)" % fr(a, b), g, [ondalik_str(a, b * 10)[0], ondalik_str(b, a)[0] if a else "0", "%d,%d" % (a, b)],
                   "%d ÷ %d = <b>%s</b>." % (a, b, g))

    def devirli():
        b = ch([3, 6, 7, 9, 11, 12, 15])
        a = ri(1, 2 * b)
        if a % b == 0:
            return None
        g, rep = ondalik_str(a, b)
        if not rep:
            return None
        plain = g.replace("<span class='ov'>", "").replace("</span>", "")
        w = [plain, ondalik_str(a, b * 10)[0], ondalik_str(a + 1, b)[0] if (a + 1) % b else plain + "0"]
        return mcq("%s kesrinin ondalık gösterimi hangisidir?" % fr(a, b), g, w, "%d ÷ %d bölmesinde kalanlar tekrar eder; tekrar eden kısım çizgiyle gösterilir: <b>%s</b>." % (a, b, g))

    def sonlu_mu():
        b = ch([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 20, 25])
        a = ri(1, b - 1)
        from math import gcd
        bb = b // gcd(a, b)
        ok = all(p in (2, 5) for p in carpanlar(bb)) if bb > 1 else True
        g = "Sonlu" if ok else "Devirli"
        return mcq("%s kesrinin ondalık gösterimi sonlu mu, devirli mi?" % fr(a, b), g, ["Devirli" if ok else "Sonlu", "Hem sonlu hem devirli", "Ondalık gösterimi yoktur"],
                   "%s = %s: <b>%s</b>." % (fr(a, b), ondalik_str(a, b)[0], low(g)))

    def kesir_bolme():
        a, b = ri(2, 30), ri(2, 12)
        if a % b == 0:
            return None
        return mcq("%d ÷ %d işlemi hangi kesirle gösterilir?" % (a, b), fr(a, b), [fr(b, a), fr(a, b * 10), fr(a - b, b) if a > b else fr(a + b, b)],
                   "Bölünen pay, bölen payda olur: <b>%s</b>." % fr(a, b))

    def paylasim():
        a = ri(2, 9)
        b = ri(2, 12)
        if a % b == 0:
            return None
        g = ff(F(a, b), mixed=True)
        what = ch(["pizza", "pasta", "karpuz", "ekmek"])
        return mcq("%d %s %d kişiye eşit paylaştırılıyor. Her kişiye ne kadar düşer?" % (a, what, b), g, [fr(b, a), ff(F(a, b + 1), True), ff(F(a + 1, b), True)],
                   "%d ÷ %d = %s = <b>%s</b>." % (a, b, fr(a, b), g))

    def oruntu():
        b = ch([3, 9, 11])
        a = ri(1, b - 1)
        s, _ = ondalik_str(a, b)
        plain = s.replace("<span class='ov'>", "").replace("</span>", "")
        rep = s.split("<span class='ov'>")[1].split("</span>")[0]
        n = ri(5, 20)
        digits = (rep * 30)[:n]
        g = digits[-1]
        return mcq("%s kesrinin ondalık gösteriminde virgülden sonraki %d. basamakta hangi rakam vardır?" % (fr(a, b), n), g, [d for d in "0123456789" if d != g][:6],
                   "%s = %s. Tekrar eden kısım “%s”. %d. basamak <b>%s</b>." % (fr(a, b), s, rep, n, g))

    sets = [("Bölerek ondalık gösterim", [(bolme, 20)]),
            ("Devirli ondalık gösterim", [(devirli, 20)]),
            ("Sonlu mu, devirli mi?", [(sonlu_mu, 20)]),
            ("Kesir bir bölmedir", [(kesir_bolme, 10), (paylasim, 10)]),
            ("Örüntüyü kullanma", [(oruntu, 20)])]
    return unit("kesir-ve-bolme-iliskisi", "S", "MAT.6.1.6", 6, "Kesir ile Bölme İlişkisi: Sonlu ve Devirli Ondalık Gösterim", "Kesir ve Bölme",
                "Kesir ile bölme arasındaki ilişkiye yönelik tümevarımsal akıl yürütür; kesirlerin ondalık gösterimlerinde sonlu ve devirli örüntüleri belirler.",
                "6. sınıf kesir ve bölme ilişkisi çalışma kâğıdı: payı paydaya bölerek ondalık gösterim, sonlu ve devirli ondalık gösterim, devreden kısım, kesir olarak bölme ve paylaşım. 100 soru ve cevap anahtarı.",
                "Kesir bir bölmedir: 3/4 = 3 ÷ 4", "Kalan tekrar ederse ondalık gösterim devirli olur.", sets,
                ["Bir kesir payın paydaya bölümüdür: 3/4 = 3 ÷ 4 = 0,75.",
                 "Bölmede kalan 0 olursa ondalık gösterim sonludur. Kalanlar tekrar ederse rakamlar da tekrar eder; buna devirli ondalık gösterim denir: 1/3 = 0,333… = 0,<span class='ov'>3</span>.",
                 "Sadeleşmiş kesrin paydası yalnızca 2 ve 5 çarpanlarından oluşuyorsa ondalık gösterim sonludur."],
                [("5/8", ["5 ÷ 8 = 0,625"], "0,625"), ("2/3", ["2 ÷ 3 = 0,666…"], "0,<span class='ov'>6</span>")],
                [["1/3 = 0,3 yazmak", "1/3 = 0,333…; tekrar eden kısım çizgiyle gösterilir"], ["Paydayı paya bölmek", "Pay paydaya bölünür: 3/4 = 3 ÷ 4"],
                 ["Devreden kısmın tamamını değil bir kısmını çizmek", "1/11 = 0,<span class='ov'>09</span>"]],
                [("Her kesrin ondalık gösterimi var mıdır?", "Evet. Ya sonlu ya da devirlidir."),
                 ("Devirli ondalık gösterim nasıl yazılır?", "Tekrar eden rakamların üzerine çizgi çekilir: 0,<span class='ov'>3</span>, 0,1<span class='ov'>6</span>."),
                 ("Paydası 2 ve 5 dışında çarpanı olan her kesir devirli midir?", "Önce sadeleştir. Sadeleşmiş paydada 2 ve 5 dışında asal çarpan varsa devirlidir.")])


# ============================================================ 7. kesirlerle işlemler
def u7():
    def topla():
        a, b = ri(2, 9), ri(2, 9)
        if a == b:
            return None
        x, y = F(ri(1, a - 1), a), F(ri(1, b - 1), b)
        k = ri(0, 1)
        if k == 0:
            g = x + y
            L = x.denominator * y.denominator // gcd(x.denominator, y.denominator)
            return mcq("%s + %s işleminin sonucu kaçtır?" % (ff(x), ff(y)), ff(g, True), [fr(x.numerator + y.numerator, x.denominator + y.denominator), ff(g + F(1, L), True), ff(x * y)],
                       "Paydalar eşitlenir: %s + %s = <b>%s</b>." % (fr(x.numerator * L // x.denominator, L), fr(y.numerator * L // y.denominator, L), ff(g, True)))
        if x < y:
            x, y = y, x
        g = x - y
        return mcq("%s − %s işleminin sonucu kaçtır?" % (ff(x), ff(y)), ff(g), [fr(abs(x.numerator - y.numerator), abs(x.denominator - y.denominator) or 1), ff(x + y, True), ff(g + F(1, a * b))],
                   "Paydalar eşitlenir ve paylar çıkarılır: <b>%s</b>." % ff(g))

    def carp():
        a, b = F(ri(1, 8), ri(2, 9)), F(ri(1, 8), ri(2, 9))
        if a >= 1 or b >= 1:
            return None
        g = a * b
        return mcq("%s × %s işleminin sonucu kaçtır?" % (ff(a), ff(b)), ff(g), [fr(a.numerator * b.denominator, a.denominator * b.numerator), ff(a + b, True), fr(a.numerator * b.numerator, a.denominator + b.denominator)],
                   "Paylar çarpılır, paydalar çarpılır: <b>%s</b>." % ff(g))

    def bol():
        a, b = F(ri(1, 8), ri(2, 9)), F(ri(1, 8), ri(2, 9))
        if a >= 1 or b >= 1 or a == b:
            return None
        g = a / b
        return mcq("%s ÷ %s işleminin sonucu kaçtır?" % (ff(a), ff(b)), ff(g, True), [ff(a * b), ff(b / a, True), fr(a.numerator * b.numerator, a.denominator * b.denominator + 1)],
                   "Birinci kesir, ikincinin ters çevrilmişiyle çarpılır: %s × %s = <b>%s</b>." % (ff(a), fr(b.denominator, b.numerator), ff(g, True)))

    def dogal():
        n = ri(2, 12)
        b = ch([2, 3, 4, 5, 6, 8])
        a = ri(1, b - 1)
        k = ri(0, 1)
        if k == 0:
            g = F(a, b) * n
            return mcq("%d × %s işleminin sonucu kaçtır?" % (n, fr(a, b)), ff(g, True), [fr(a * n, b * n), ff(F(a, b * n)), ff(g + 1, True)], "%d × %d = %d: %s = <b>%s</b>." % (n, a, a * n, fr(a * n, b), ff(g, True)))
        g = F(a, b) / n
        return mcq("%s ÷ %d işleminin sonucu kaçtır?" % (fr(a, b), n), ff(g), [ff(F(a * n, b), True), fr(a, b + n), ff(F(a, b) * n, True) if F(a, b) * n != F(a * n, b) else fr(a + n, b)],
                   "%s × %s = <b>%s</b>." % (fr(a, b), fr(1, n), ff(g)))

    def problem():
        nm = G.K.next()
        k = ri(0, 2)
        if k == 0:
            T = ri(2, 9) * 12
            a = F(ri(1, 3), 4)
            b = F(ri(1, 2), 3)
            if a + b >= 1:
                return None
            g = T - T * a - T * b
            return mcq("%s %d sayfalık kitabının %s kadarını birinci gün, %s kadarını ikinci gün okudu. Okuyacağı kaç sayfa kaldı?" % (nm, T, ff(a), ff(b)), str(g),
                       [str(T * a + T * b), str(T - T * a), str(g + 4)], "%d × %s = %d, %d × %s = %d. %d − %d − %d = <b>%d</b>." % (T, ff(a), T * a, T, ff(b), T * b, T, T * a, T * b, g))
        if k == 1:
            L = F(ri(3, 12), 2)
            p = F(1, ch([2, 4]))
            n = L / p
            if n.denominator != 1:
                return None
            return mcq("%s m uzunluğundaki bir kurdele %s m uzunluğunda parçalara ayrılıyor. Kaç parça elde edilir?" % (ff(L, True), ff(p)), str(n), [str(L * p) if (L * p).denominator == 1 else ff(L * p, True), str(n + 1), str(n // 2 or 1)],
                       "%s ÷ %s = <b>%d</b>." % (ff(L, True), ff(p), n))
        a = F(ri(1, 4), 5)
        b = F(ri(1, 3), 4)
        g = a * b
        return mcq("Bir bahçenin %s kadarına sebze ekildi. Sebze ekilen kısmın %s kadarına domates ekildi. Domates bahçenin ne kadarıdır?" % (ff(a), ff(b)), ff(g),
                   [ff(a + b, True), ff(a - b) if a > b else ff(b - a), fr(a.numerator * b.numerator, a.denominator + b.denominator)], "%s × %s = <b>%s</b>." % (ff(a), ff(b), ff(g)))

    sets = [("Toplama ve çıkarma", [(topla, 20)]),
            ("Çarpma", [(carp, 20)]),
            ("Bölme", [(bol, 20)]),
            ("Doğal sayıyla çarpma ve bölme", [(dogal, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("kesirlerle-islemler", "S", "MAT.6.1.7", 7, "Kesirlerle Toplama, Çıkarma, Çarpma ve Bölme", "Kesirlerle İşlemler",
                "Kesir, ondalık gösterim ve yüzdelerle dört işlem gerektiren problemleri çözer.",
                "6. sınıf kesirlerle işlemler çalışma kâğıdı: paydaları farklı kesirlerle toplama ve çıkarma, kesirlerle çarpma ve bölme, doğal sayıyla çarpma ve bölme, problemler. 100 soru ve cevap anahtarı.",
                "Toplamada paydaları eşitle", "Bölmede ikinci kesri ters çevirip çarp.", sets,
                ["Paydaları farklı kesirleri toplarken ve çıkarırken önce paydaları eşitleriz: 1/2 + 1/3 = 3/6 + 2/6 = 5/6.",
                 "Çarparken paylar ve paydalar ayrı ayrı çarpılır: 2/3 × 3/5 = 6/15 = 2/5.",
                 "Bölerken birinci kesir, ikinci kesrin ters çevrilmişiyle çarpılır: 3/4 ÷ 1/2 = 3/4 × 2/1 = 3/2."],
                [("2/3 + 1/4", ["8/12 + 3/12"], "11/12"), ("4/5 ÷ 2/3", ["4/5 × 3/2 = 12/10"], "6/5 = 1 1/5")],
                [["1/2 + 1/3 = 2/5", "Paydalar eşitlenir: 3/6 + 2/6 = 5/6"], ["Bölmede ilk kesri ters çevirmek", "İkinci kesir ters çevrilir"],
                 ["Doğal sayıyla çarparken paydayı da çarpmak", "3 × 2/5 = 6/5; payda değişmez"]],
                [("Kesirle çarpınca sonuç neden küçülebilir?", "1’den küçük bir kesirle çarpmak, sayının bir parçasını almak demektir."),
                 ("Sonucu sadeleştirmeli miyim?", "Evet, en sade hâlde yazmak daha kolay okunur."),
                 ("Bir kesrin tersi nedir?", "Pay ile paydanın yer değiştirmiş hâlidir: 3/4’ün tersi 4/3.")])


# ============================================================ 8. ondalık gösterimlerle işlemler
def u8():
    def topla():
        a, b = ri(100, 9999) / 100.0, ri(10, 999) / 100.0
        k = ri(0, 1)
        if k == 0:
            g = round(a + b, 2)
            return mcq("%s + %s işleminin sonucu kaçtır?" % (dec(a), dec(b)), dec(g), [dec(round(a + b * 10, 2)), dec(round(g + 0.1, 2)), dec(round(g - 1, 2))],
                       "Virgüller alt alta gelecek şekilde toplanır: <b>%s</b>." % dec(g))
        if a < b:
            a, b = b, a
        g = round(a - b, 2)
        return mcq("%s − %s işleminin sonucu kaçtır?" % (dec(a), dec(b)), dec(g), [dec(round(a - b / 10, 2)), dec(round(g + 0.1, 2)), dec(round(g + 1, 2))],
                   "Virgüller alt alta gelecek şekilde çıkarılır: <b>%s</b>." % dec(g))

    def carp():
        a, b = ri(11, 999) / 10.0, ri(2, 99)
        k = ri(0, 1)
        if k == 0:
            g = round(a * b, 2)
            return mcq("%s × %d işleminin sonucu kaçtır?" % (dec(a), b), dec(g), [dec(round(g * 10, 2)), dec(round(g / 10, 3)), dec(round(g + a, 2))],
                       "Virgül yokmuş gibi çarpılır, sonra virgülden sonra 1 basamak ayrılır: <b>%s</b>." % dec(g))
        a2 = ri(11, 99) / 10.0
        b2 = ri(11, 99) / 10.0
        g = round(a2 * b2, 2)
        return mcq("%s × %s işleminin sonucu kaçtır?" % (dec(a2), dec(b2)), dec(g), [dec(round(g * 10, 2)), dec(round(g / 10, 3)), dec(round(a2 + b2, 2))],
                   "Virgülden sonra toplam 2 basamak ayrılır: <b>%s</b>." % dec(g))

    def bol():
        b = ri(2, 9)
        q = ri(11, 999) / 100.0
        a = round(q * b, 2)
        g = q
        return mcq("%s ÷ %d işleminin sonucu kaçtır?" % (dec(a), b), dec(g), [dec(round(g * 10, 2)), dec(round(g / 10, 3)), dec(round(g + 0.1, 2))],
                   "Sağlama: %s × %d = %s. Sonuç <b>%s</b>." % (dec(g), b, dec(a), dec(g)))

    def on_kat():
        v = ri(11, 9999) / 100.0
        p = ch([10, 100, 1000])
        k = ri(0, 1)
        if k == 0:
            g = round(v * p, 3)
            return mcq("%s × %s işleminin sonucu kaçtır?" % (dec(v), num(p)), dec(g), [dec(round(v * p / 10, 3)), dec(round(v * p * 10, 3)), dec(round(v / p, 5))],
                       "Virgül %d basamak sağa kayar: <b>%s</b>." % (len(str(p)) - 1, dec(g)))
        g = round(v / p, 5)
        return mcq("%s ÷ %s işleminin sonucu kaçtır?" % (dec(v), num(p)), dec(g), [dec(round(v / p * 10, 5)), dec(round(v / p / 10, 6)), dec(round(v * p, 3))],
                   "Virgül %d basamak sola kayar: <b>%s</b>." % (len(str(p)) - 1, dec(g)))

    def problem():
        nm = G.K.next()
        k = ri(0, 2)
        if k == 0:
            p = ri(150, 990) / 10.0
            n = ri(2, 9)
            m = ri(10, 50) * 10
            tot = round(p * n, 2)
            if tot >= m:
                return None
            return mcq("%s tanesi %s TL olan %d kitap aldı ve kasaya %d TL verdi. Kaç TL para üstü aldı?" % (nm, dec(p, 2), n, m), "%s TL" % dec(round(m - tot, 2), 2),
                       ["%s TL" % dec(x, 2) for x in (tot, round(m - p, 2), round(m - tot + 1, 2))], "%s × %d = %s TL. %d − %s = <b>%s TL</b>." % (dec(p, 2), n, dec(tot, 2), m, dec(tot, 2), dec(round(m - tot, 2), 2)))
        if k == 1:
            L = ri(20, 99) / 10.0
            n = ri(2, 6)
            g = round(L / n, 3)
            if len(dec(g)) > 5:
                return None
            return mcq("%s m uzunluğundaki bir ip %d eş parçaya bölünüyor. Bir parça kaç metredir?" % (dec(L), n), "%s m" % dec(g), ["%s m" % dec(x) for x in (round(L * n, 2), round(g * 10, 2), round(L - n, 2))],
                       "%s ÷ %d = <b>%s m</b>." % (dec(L), n, dec(g)))
        a, b, c = ri(10, 99) / 10.0, ri(10, 99) / 10.0, ri(10, 99) / 10.0
        g = round(a + b + c, 1)
        return mcq("Bir koşucu üç günde sırayla %s km, %s km ve %s km koştu. Toplam kaç km koştu?" % (dec(a), dec(b), dec(c)), "%s km" % dec(g), ["%s km" % dec(x) for x in (round(g + 1, 1), round(g - 0.1, 1), round(a + b, 1))],
                   "%s + %s + %s = <b>%s km</b>." % (dec(a), dec(b), dec(c), dec(g)))

    sets = [("Toplama ve çıkarma", [(topla, 20)]),
            ("Çarpma", [(carp, 20)]),
            ("Bölme", [(bol, 20)]),
            ("10, 100, 1000 ile çarpma ve bölme", [(on_kat, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("ondalik-gosterimlerle-islemler", "S", "MAT.6.1.7", 8, "Ondalık Gösterimlerle Dört İşlem", "Ondalık Gösterimlerle İşlemler",
                "Kesir, ondalık gösterim ve yüzdelerle dört işlem gerektiren problemleri çözer.",
                "6. sınıf ondalık gösterimlerle işlemler çalışma kâğıdı: ondalık gösterimlerle toplama, çıkarma, çarpma ve bölme, 10, 100 ve 1000 ile çarpma ve bölme, para ve uzunluk problemleri. 100 soru ve cevap anahtarı.",
                "Toplamada virgüller alt alta", "Çarpmada virgülden sonraki basamaklar toplanır.", sets,
                ["Toplama ve çıkarmada virgüller alt alta gelecek şekilde yazılır; boş basamaklara 0 yazılabilir.",
                 "Çarpmada virgül yokmuş gibi çarpılır; sonuçta çarpanların virgülden sonraki basamak sayılarının toplamı kadar basamak ayrılır.",
                 "10, 100, 1000 ile çarparken virgül sağa, bölerken sola kayar."],
                [("3,45 + 12,6", ["3,45 + 12,60"], "16,05"), ("2,4 × 1,5", ["24 × 15 = 360", "2 basamak ayır"], "3,6")],
                [["3,45 + 12,6 = 4,71 (sağdan hizalamak)", "Virgülleri hizala: 16,05"], ["2,4 × 1,5 = 36", "İki basamak ayır: 3,60"],
                 ["÷ 10 yapınca virgülü sağa kaydırmak", "Bölmede virgül sola kayar"]],
                [("Ondalık bölmede kalan olursa ne yaparız?", "Bölünenin sonuna 0 ekleyerek bölmeye devam ederiz."),
                 ("Para hesaplarında kaç basamak kullanırız?", "Kuruş için virgülden sonra 2 basamak kullanırız: 12,50 TL."),
                 ("Sonucu nasıl kontrol ederim?", "Yuvarlayarak tahmin et: 2,4 × 1,5 ≈ 2 × 2 = 4; 3,6 makul.")])


# ============================================================ 9. yüzde problemleri
def u9():
    def yuzdesi():
        p = ch([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80])
        n = ri(2, 40) * 20
        g = n * p // 100
        return mcq("%s sayısının %%%d kadarı kaçtır?" % (num(n), p), num(g), [num(n * p // 10) if p != 10 else num(n), num(n - g), num(g + p)], "%s × %d ÷ 100 = <b>%s</b>." % (num(n), p, num(g)))

    def indirim():
        p = ch([10, 15, 20, 25, 30, 40, 50])
        n = ri(4, 60) * 20
        d = n * p // 100
        return mcq("Fiyatı %s TL olan bir ayakkabıya %%%d indirim yapılıyor. Ayakkabının indirimli fiyatı kaç TL olur?" % (num(n), p), "%s TL" % num(n - d),
                   ["%s TL" % num(x) for x in (d, n + d, n - p)], "İndirim %s × %d ÷ 100 = %s TL. %s − %s = <b>%s TL</b>." % (num(n), p, num(d), num(n), num(d), num(n - d)))

    def zam():
        p = ch([5, 10, 20, 25, 50])
        n = ri(4, 50) * 20
        d = n * p // 100
        return mcq("Fiyatı %s TL olan bir ürüne %%%d zam yapılıyor. Ürünün yeni fiyatı kaç TL olur?" % (num(n), p), "%s TL" % num(n + d),
                   ["%s TL" % num(x) for x in (d, n - d, n + p)], "Zam %s TL. %s + %s = <b>%s TL</b>." % (num(d), num(n), num(d), num(n + d)))

    def kac_yuzde():
        n = ch([20, 25, 40, 50, 80, 200])
        a = ri(1, n - 1)
        if (a * 100) % n:
            return None
        g = a * 100 // n
        return mcq("Bir sınıftaki %d öğrenciden %d tanesi kızdır. Kız öğrenciler sınıfın yüzde kaçıdır?" % (n, a), "%%%d" % g, ["%%%d" % x for x in (a, 100 - g, g + 10 if g < 90 else g - 10)],
                   "%s = %s = <b>%%%d</b>." % (fr(a, n), fr(g, 100), g))

    def butun():
        p = ch([10, 20, 25, 40, 50])
        g = ri(2, 30) * 20
        part = g * p // 100
        return mcq("Bir sayının %%%d kadarı %s ise sayının tamamı kaçtır?" % (p, num(part)), num(g), [num(part * p), num(part + p), num(part * 100 // (100 - p)) if (part * 100) % (100 - p) == 0 else num(g + part)],
                   "%%%d → %s ise %%1 → %s ÷ %d, %%100 → %s × 100 ÷ %d = <b>%s</b>." % (p, num(part), num(part), p, num(part), p, num(g)))

    sets = [("Bir sayının yüzdesi", [(yuzdesi, 20)]),
            ("İndirim", [(indirim, 20)]),
            ("Zam", [(zam, 20)]),
            ("Yüzde kaçı?", [(kac_yuzde, 20)]),
            ("Yüzdesi verilen bütün", [(butun, 20)])]
    return unit("yuzde-problemleri", "S", "MAT.6.1.7", 9, "Yüzde Problemleri: İndirim, Zam ve Yüzdesi Verilen Bütün", "Yüzde Problemleri",
                "Kesir, ondalık gösterim ve yüzdelerle dört işlem gerektiren problemleri çözer.",
                "6. sınıf yüzde problemleri çalışma kâğıdı: bir sayının yüzdesini bulma, indirim ve zam, bir çokluğun yüzde kaçı olduğunu bulma, yüzdesi verilen bütünü bulma. 100 soru ve cevap anahtarı.",
                "%20’si: × 20 ÷ 100", "İndirimli fiyat = fiyat − indirim.", sets,
                ["Bir sayının yüzdesini bulmak için sayıyı yüzde değeriyle çarpıp 100’e böleriz: 300’ün %20’si = 300 × 20 ÷ 100 = 60.",
                 "İndirimde indirim miktarı fiyattan çıkarılır; zamda zam miktarı fiyata eklenir.",
                 "Yüzdesi verilen bütünü bulmak için önce %1’ini, sonra %100’ünü buluruz."],
                [("480 TL’ye %25 indirim", ["480 × 25 ÷ 100 = 120", "480 − 120"], "360 TL"), ("%40’ı 60 olan sayı", ["%1 = 60 ÷ 40 = 1,5", "%100 = 150"], "150")],
                [["İndirim miktarını indirimli fiyat sanmak", "İndirimli fiyat = fiyat − indirim"], ["%20 ile 20’yi karıştırmak", "%20 = 20/100"],
                 ["Yüzdesi verilen bütünü bulurken çarpmak", "Önce yüzde değerine böl, sonra 100 ile çarp"]],
                [("Yüzdeyi zihinden nasıl hesaplarım?", "%10 için 10’a böl; %5 için onun yarısını al; %25 için 4’e böl; %50 için 2’ye böl."),
                 ("%100’den fazla yüzde olur mu?", "Evet. Bir fiyat iki katına çıkarsa %100 artmıştır."),
                 ("İndirim ve zam günlük hayatta nerede görülür?", "Mağaza kampanyalarında, fiyat artışlarında ve faturalarda.")])


# ============================================================ 10. uzunluk ölçme
UZ = [("km", 1000), ("hm", 100), ("dam", 10), ("m", 1), ("dm", F(1, 10)), ("cm", F(1, 100)), ("mm", F(1, 1000))]


def u10():
    def cevir():
        i, j = sh(range(7))[:2]
        a, va = UZ[i]
        b, vb = UZ[j]
        if abs(i - j) > 3:
            return None
        n = ri(2, 95)
        g = F(n) * F(va) / F(vb)
        if g.denominator != 1 and len(dz(g)) > 7:
            return None
        gs = num(g) if g.denominator == 1 else dz(g)
        k = 10 ** abs(i - j)
        w = [g * 10, g / 10, g * k * k if g * k * k < 10 ** 7 else g * 100]
        return mcq("%d %s kaç %s eder?" % (n, a, b), "%s %s" % (gs, b), ["%s %s" % (num(x) if F(x).denominator == 1 else dz(x), b) for x in w if F(x) != g],
                   "%s ile %s arasında %d basamak var; her basamak 10 kat: <b>%s %s</b>." % (a, b, abs(i - j), gs, b))

    def bilesik():
        n, c = ri(1, 9), ri(1, 99)
        g = n * 100 + c
        return mcq("%d m %d cm kaç santimetredir?" % (n, c), "%s cm" % num(g), ["%s cm" % num(x) for x in (n * 10 + c, n + c, int(str(n) + str(c)) if int(str(n) + str(c)) != g else g + 100, g + 100)],
                   "%d m = %d cm. %d + %d = <b>%d cm</b>." % (n, n * 100, n * 100, c, g))

    def ondalik():
        v = ri(101, 9999) / 100.0
        k = ri(0, 1)
        if k == 0:
            return mcq("%s m kaç santimetredir?" % dec(v), "%s cm" % num(int(round(v * 100))), ["%s cm" % x for x in (dec(v * 10), num(int(round(v * 1000))), dec(v / 100))],
                       "1 m = 100 cm. %s × 100 = <b>%s cm</b>." % (dec(v), num(int(round(v * 100)))))
        n = ri(101, 99999)
        return mcq("%s m kaç kilometredir?" % num(n), "%s km" % dec(n / 1000.0), ["%s km" % dec(x) for x in (n / 100.0, n / 10000.0, n * 1000.0 if n < 100 else n / 10.0)],
                   "1 km = 1.000 m. %s ÷ 1.000 = <b>%s km</b>." % (num(n), dec(n / 1000.0)))

    def sirala():
        vals = [(ri(1, 9), "m"), (ri(10, 99), "dm"), (ri(100, 999), "cm"), (ri(1000, 9999), "mm")]
        mm = {"m": 1000, "dm": 100, "cm": 10, "mm": 1}
        ms = [v * mm[u] for v, u in vals]
        if len(set(ms)) < 4:
            return None
        k = ri(0, 1)
        i = ms.index(max(ms)) if k == 0 else ms.index(min(ms))
        opts = ["%s %s" % (num(v), u) for v, u in vals]
        return mcq("%s uzunluklarından en %s hangisidir?" % (", ".join(opts), "uzunu" if k == 0 else "kısası"), opts[i], [o for j, o in enumerate(opts) if j != i],
                   "Hepsini milimetreye çeviririz: %s. En %s <b>%s</b>." % (", ".join("%s mm" % num(x) for x in ms), "uzun" if k == 0 else "kısa", opts[i]))

    def problem():
        a, b = ri(2, 9), ri(100, 900)
        k = ri(0, 1)
        if k == 0:
            g = a * 1000 - b
            return mcq("%d km’lik bir yolun %d metresi yüründü. Kaç metre yol kaldı?" % (a, b), "%s m" % num(g), ["%s m" % num(x) for x in (a * 100 - b if a * 100 > b else g + 100, a * 1000 + b, g - 100)],
                       "%d km = %s m. %s − %d = <b>%s m</b>." % (a, num(a * 1000), num(a * 1000), b, num(g)))
        n = ri(3, 12)
        c = ri(15, 95)
        g = n * c
        return mcq("Her biri %d cm olan %d tahta uç uca ekleniyor. Toplam uzunluk kaç metredir?" % (c, n), "%s m" % dec(g / 100.0), ["%s m" % dec(x) for x in (g / 10.0, g / 1000.0, g * 1.0)],
                   "%d × %d = %d cm = <b>%s m</b>." % (n, c, g, dec(g / 100.0)))

    sets = [("Birimleri dönüştürme", [(cevir, 20)]),
            ("İki birimle verilen uzunluklar", [(bilesik, 20)]),
            ("Ondalık gösterimle uzunluk", [(ondalik, 20)]),
            ("Uzunlukları karşılaştırma", [(sirala, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("uzunluk-olcme", "S", "MAT.6.1.8", 10, "Uzunluk Ölçme Birimleri: km, hm, dam, m, dm, cm, mm", "Uzunluk Ölçme",
                "Metreyi referans alarak standart uzunluk ölçme birimleriyle ölçüm yapar ve birimleri karşılaştırır.",
                "6. sınıf uzunluk ölçme çalışma kâğıdı: km, hm, dam, m, dm, cm ve mm arasında dönüştürme, iki birimle verilen uzunluklar, ondalık gösterimle uzunluk, karşılaştırma ve problemler. 100 soru ve cevap anahtarı.",
                "Her birim bir sonrakinin 10 katı", "Büyükten küçüğe çarp, küçükten büyüğe böl.", sets,
                ["Uzunluk birimleri metreden büyükten küçüğe: km, hm, dam, m, dm, cm, mm. Her birim bir sağındakinin 10 katıdır.",
                 "Büyük birimi küçük birime çevirirken 10, 100, 1000 ile çarparız; küçük birimi büyük birime çevirirken böleriz.",
                 "Karşılaştırmadan önce bütün uzunlukları aynı birime çeviririz."],
                [("3,25 m kaç cm?", ["3,25 × 100"], "325 cm"), ("4.500 m kaç km?", ["4.500 ÷ 1.000"], "4,5 km")],
                [["1 m = 10 cm", "1 m = 10 dm = 100 cm"], ["Büyük birime çevirirken çarpmak", "Küçükten büyüğe bölünür"],
                 ["Farklı birimleri doğrudan karşılaştırmak", "Önce aynı birime çevir"]],
                [("dam ve hm nerede kullanılır?", "Günlük hayatta seyrek kullanılır; birimler arasındaki 10’ar katlık ilişkiyi görmemizi sağlar."),
                 ("Uzunluk ölçerken hangi birimi seçmeliyim?", "Ölçülen nesneye uygun birimi: kalem için cm, oda için m, şehirler arası için km."),
                 ("1 km kaç mm’dir?", "1 km = 1.000 m = 1.000.000 mm.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
