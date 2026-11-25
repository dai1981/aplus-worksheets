# -*- coding: utf-8 -*-
"""Türkiye 3. sınıf: Sayılar ve Nicelikler (1)(2) — 1〜10 単元。tr_s3.py から使う。"""
import math
from tr_common import (num, tl, kurus, para, oku, saat_oku, hm, mcq, M, NB, Kids, wrap, text, line, table,
                       basamak_tablosu, bloklar, sayi_dogrusu, saat_svg, INK, GREEN, FILL, RED, BLUE)

R = None
K = None


def setup(rnd):
    global R, K
    R = rnd
    K = Kids(rnd)


def ri(a, b):
    return R.randint(a, b)


def ch(xs):
    return R.choice(list(xs))


def sh(xs):
    xs = list(xs)
    R.shuffle(xs)
    return xs


def named(f, n):
    f.__name__ = n
    return f


def unit(slug, dom, code, sort, title, short, std, meta, kb, ks, sets, think, ex, mist, faq):
    return dict(slug=slug, dom=dom, code=code, sort=sort, title=title, short=short, std=std, meta=meta, kb=kb, ks=ks,
                sets=sets, think=think, ex=ex, mist=mist, faq=faq)


def cap(s):
    """Türkçe büyük harf: i → İ, ı → I"""
    f = {"i": "İ", "ı": "I"}.get(s[0], s[0].upper())
    return f + s[1:]


def mi(w):
    """soru eki: '75 dakika mı', '1 saat mi', '2 litre mi'"""
    vs = [c for c in w.lower() if c in "aıoueiöü"]
    v = vs[-1] if vs else "e"
    return w + " " + {"a": "mı", "ı": "mı", "o": "mu", "u": "mu", "e": "mi", "i": "mi", "ö": "mü", "ü": "mü"}[v]


# ------------------------------------------------------------ dağıtma sayıları: üçer, dörder, altışar…
def dagit(n):
    w = oku(n)
    last = w.split()[-1]
    if last == "dört":
        return w[:-1] + "der"
    vow = [c for c in last if c in "aıoueiöü"]
    back = vow[-1] in "aıou"
    if last[-1] in "aıoueiöü":
        return w + ("şar" if back else "şer")
    return w + ("ar" if back else "er")


# kesir okunuşu: dörtte bir
_LOC = {2: "ikide", 3: "üçte", 4: "dörtte", 5: "beşte", 6: "altıda", 7: "yedide", 8: "sekizde", 9: "dokuzda", 10: "onda", 12: "on ikide"}


def kesir_oku(a, b):
    return "%s %s" % (_LOC[b], oku(a))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


# ------------------------------------------------------------ çizimler
def bar_frac(n, k, w=300, h=40, col="#7fb3d5"):
    s = []
    cw = w / float(n)
    for i in range(n):
        s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (6 + i * cw, cw, h, col if i < k else "#ffffff", INK))
    return wrap(w + 12, h + 12, "".join(s), "%d eş parçaya bölünmüş şerit, %d parça boyalı" % (n, k))


def pie(n, k, r=58, col="#f4a261"):
    cx = cy = r + 6
    s = []
    for i in range(n):
        a0 = -math.pi / 2 + 2 * math.pi * i / n
        a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
        if n == 1:
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, col if k else "#fff", INK))
        else:
            s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, cx + r * math.cos(a1), cy + r * math.sin(a1),
                        col if i < k else "#ffffff", INK))
    return wrap(2 * r + 12, 2 * r + 12, "".join(s), "%d eş parçaya bölünmüş daire, %d parça boyalı" % (n, k))


def rect_frac(n, k, col="#a8d5ba"):
    """kare, n eş parça (2: dikey, 4: 2×2)"""
    s = []
    a = 110
    if n == 4 and R.random() < 0.5:
        cells = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for i, (x, y) in enumerate(cells):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (6 + x * a / 2, 6 + y * a / 2, a / 2, a / 2, col if i < k else "#ffffff", INK))
    else:
        cw = a / float(n)
        for i in range(n):
            s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (6 + i * cw, cw, a, col if i < k else "#ffffff", INK))
    return wrap(a + 12, a + 12, "".join(s), "%d eş parçaya bölünmüş kare, %d parça boyalı" % (n, k))


def frac_pic(n, k):
    t = R.random()
    if t < 0.4:
        return pie(n, k)
    if t < 0.75 or n not in (2, 4):
        return bar_frac(n, k)
    return rect_frac(n, k)


def noktalar(n, per=2, col="#e07a5f"):
    """n nesne, ikişer ikişer eşlenmiş"""
    s = []
    cols = (n + per - 1) // per
    for i in range(n):
        x, y = 18 + (i // per) * 30, 18 + (i % per) * 26
        s.append("<circle cx='%d' cy='%d' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x, y, col, INK))
    return wrap(cols * 30 + 8, per * 26 + 10, "".join(s), "%d nesne ikişerli dizilmiş" % n)


# TL: madenî paralar ve kâğıt paralar
def coin(cx, cy, kr):
    r = {5: 13, 10: 14, 25: 15.5, 50: 17, 100: 19}[kr]
    fillc = "#e6c65a" if kr == 100 else "#d6d6d6" if kr in (25, 50) else "#d9a066"
    ring = ""
    if kr == 100:
        ring = "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#d6d6d6' stroke='%s'/>" % (cx, cy, r * 0.66, INK)
    lab = "1 TL" if kr == 100 else "%d kr" % kr
    return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>%s" % (cx, cy, r, fillc, INK, ring)
            + text(cx, cy + 4, lab.replace(" ", NB), 9))


NOTE_COL = {5: "#c9a6d8", 10: "#f0a3a3", 20: "#a5d6a7", 50: "#f6c47a", 100: "#9fc3e8", 200: "#e3b7d6"}


def note(x, y, t):
    return ("<rect x='%.1f' y='%.1f' width='74' height='38' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (x, y, NOTE_COL[t], INK) + text(x + 37, y + 25, "%d%sTL" % (t, NB), 15))


def para_svg(items):
    """items: kuruş cinsinden; 500 ve üstü kâğıt para"""
    s, x = [], 6
    notes = sorted([c for c in items if c >= 500], reverse=True)
    coins = sorted([c for c in items if c < 500], reverse=True)
    rows = []
    for c in notes:
        s.append(note(x, 6, c // 100))
        x += 82
    for c in coins:
        s.append(coin(x + 20, 25, c))
        x += 44
    return wrap(x + 4, 50, "".join(s), "paralar: toplam %s" % para(sum(items)).replace(NB, " "))


# ============================================================ 1. 1000'e kadar sayılar
def u1():
    def n3():
        return ri(101, 999)

    def okunus():
        n = n3()
        h, t, o = n // 100, n // 10 % 10, n % 10
        k = ri(0, 1)
        sw = [h * 100 + o * 10 + t, t * 100 + h * 10 + o, h * 1000 + t * 10 + o if t else h * 1000 + o]
        if t == 0:
            sw = [h * 100 + o * 10, h * 10 + o, h * 1000 + o]
        if k == 0:
            return mcq("Okunuşu <b>%s</b> olan sayı hangisidir?" % oku(n), num(n), [num(x) for x in sw] + [num(n + 10), num(n + 100)],
                       "%s → %d yüzlük, %d onluk, %d birlik: <b>%s</b>." % (cap(oku(n)), h, t, o, num(n)))
        return mcq("<b>%s</b> sayısının okunuşu hangisidir?" % num(n), cap(oku(n)), [cap(oku(x)) for x in sw if x < 1000] + [cap(oku(n + 1)), cap(oku(n + 10))],
                   "%s → %s." % (num(n), oku(n)))

    def blok():
        h, t, o = ri(1, 7), ri(0, 9), ri(0, 9)
        n = h * 100 + t * 10 + o
        return mcq("Modelde gösterilen sayı kaçtır?" + bloklar(h, t, o), num(n),
                   [num(h * 100 + o * 10 + t), num(h + t * 10 + o * 100), num(h * 100 + t + o * 10), num(n + 10), num(n - 1)],
                   "%d yüzlük = %d, %d onluk = %d, %d birlik = %d. Toplam <b>%s</b>." % (h, h * 100, t, t * 10, o, o, num(n)))

    def deger():
        n = n3()
        ds = str(n)
        i = ri(0, 2)
        d = int(ds[i])
        if d == 0 or ds.count(ds[i]) > 1:
            return None
        v = d * 10 ** (2 - i)
        names = ["yüzler", "onlar", "birler"]
        if R.random() < 0.5:
            return mcq("<b>%s</b> sayısında <b>%d</b> rakamının basamak değeri kaçtır?" % (num(n), d), num(v),
                       [num(d * 10 ** k) for k in range(3) if k != 2 - i] + [str(d)],
                       "%d rakamı %s basamağında. Basamak değeri <b>%s</b>." % (d, names[i], num(v)))
        return mcq("<b>%s</b> sayısında <b>%d</b> rakamı hangi basamaktadır?" % (num(n), d), names[i] + " basamağı",
                   [x + " basamağı" for x in names if x != names[i]] + ["binler basamağı"],
                   "%s sayısında soldan sağa yüzler, onlar, birler basamakları var. %d rakamı <b>%s basamağında</b>." % (num(n), d, names[i]))

    def cozumle():
        h, t, o = ri(1, 9), ri(0, 9), ri(0, 9)
        n = h * 100 + t * 10 + o
        k = ri(0, 2)
        if k == 0:
            q = "%s + %s + %s = ?" % (num(h * 100), num(t * 10), num(o)) if t and o else None
            if not q:
                return None
            return mcq(q, num(n), [num(h + t + o), num(h * 100 + o * 10 + t), num(h * 1000 + t * 10 + o)],
                       "Yüzler %d, onlar %d, birler %d: <b>%s</b>." % (h, t, o, num(n)))
        if k == 1:
            if t and o:
                return None
            return mcq("%d yüzlük, %d onluk ve %d birlik kaç eder?" % (h, t, o), num(n),
                       [num(h * 10 + t + o) if not t else num(h * 10 + t), num(h * 100 + o * 10 + t), num(int("%d%d" % (h, (t or o))))] + [num(n + 100)],
                       "Sıfır olan basamağa 0 yazılır: <b>%s</b>." % num(n))
        if not (t and o):
            return None
        return mcq("<b>%s</b> sayısının çözümlenmiş hâli hangisidir?" % num(n), "%s + %s + %s" % (num(h * 100), num(t * 10), num(o)),
                   ["%d + %d + %d" % (h, t, o), "%s + %s + %s" % (num(h * 100), num(o * 10), num(t)), "%s + %s + %s" % (num(h * 10), num(t * 100), num(o))],
                   "%s = %s + %s + %s." % (num(n), num(h * 100), num(t * 10), num(o)))

    def tablo():
        n = n3()
        return mcq("Basamak tablosunda gösterilen sayı kaçtır?" + basamak_tablosu(n), num(n),
                   [num(int(str(n)[::-1])), num(n + 100) if n < 900 else num(n - 100), num(n + 1)],
                   "Yüzler %s, onlar %s, birler %s: <b>%s</b>." % (str(n)[0], str(n)[1], str(n)[2], num(n)))

    sets = [("Sayıları okuma ve yazma", [(okunus, 20)]),
            ("Onluk ve yüzlük modeller", [(blok, 20)]),
            ("Basamak ve basamak değeri", [(deger, 20)]),
            ("Sayıları çözümleme", [(cozumle, 14), (tablo, 6)]),
            ("Karışık", [(okunus, 7), (deger, 7), (blok, 6)])]
    return unit("1000e-kadar-sayilar", "S", "MAT.3.1.1, MAT.3.1.2", 1, "1000'e Kadar Sayılar: Okuma, Yazma ve Basamak Değeri",
                "1000'e Kadar Sayılar",
                "Niceliklere karşılık gelen 1000'e kadar sayıların temsillerinden yararlanır; 1000'e kadar sayıları basamak ve basamak değerlerine göre çözümler.",
                "3. sınıf 1000'e kadar sayılar çalışma kâğıdı: üç basamaklı sayıları okuma ve yazma, onluk ve yüzlük modeller, basamak ve basamak değeri, sayıları çözümleme. 100 soru ve cevap anahtarı.",
                "Yüzler, onlar, birler", "Her rakamın değeri bulunduğu basamağa göre değişir.", sets,
                ["Üç basamaklı bir sayıda soldan sağa yüzler, onlar ve birler basamağı vardır.",
                 "Bir rakamın basamak değeri, rakamın bulunduğu basamağa göre bulunur: 472 sayısında 7 rakamının basamak değeri 70'tir.",
                 "Bir basamakta hiç onluk ya da birlik yoksa o basamağa 0 yazılır: 5 yüzlük ve 8 birlik 508 eder."],
                [("3 yüzlük, 6 onluk, 2 birlik", ["300 + 60 + 2"], "362"), ("Okunuşu: dört yüz beş", ["4 yüzlük, 0 onluk, 5 birlik"], "405")],
                [["Dört yüz beş: 45 yazmak", "Boş onlar basamağına 0 yazılır: 405"], ["472 sayısında 7 rakamının değeri: 7", "Onlar basamağında olduğu için 70"],
                 ["Dört yüz beş: 4005 yazmak", "Yüzler basamağı 3. basamaktır: 405"]],
                [("Basamak değeri ile sayı değeri arasındaki fark nedir?", "Sayı değeri rakamın kendisidir (7). Basamak değeri rakamın bulunduğu yere göre değişir (70 ya da 700)."),
                 ("En büyük üç basamaklı sayı kaçtır?", "999. Bir fazlası 1000'dir (bin)."),
                 ("Sıfır neden önemlidir?", "Sıfır boş basamağı gösterir. 508 ile 58 farklı sayılardır.")])


# ============================================================ 2. sıralama ve yuvarlama
def u2():
    def karsilastir():
        a = ri(100, 999)
        b = a + ch([1, 10, 100, -1, -10, -100, 9, 90, -9, -90])
        if not 100 <= b <= 999 or a == b:
            return None
        r = "&lt;" if a < b else "&gt;"
        good = "%s %s %s" % (num(a), r, num(b))
        bad = ["%s %s %s" % (num(a), o, num(b)) for o in ("&lt;", "&gt;", "=") if o != r]
        bad.append("%s %s %s" % (num(b), r, num(a)))
        return mcq("Hangisi doğrudur? (%s ve %s)" % (num(a), num(b)), good, bad,
                   "Önce yüzler basamağına, eşitse onlar basamağına bakılır. Doğrusu <b>%s</b>." % good)

    def sirala():
        base = ri(1, 8) * 100
        xs = sorted(set([base + ri(0, 99), base + ri(0, 99), base + ri(100, 199), base + ri(0, 9) * 10 + ri(0, 9), ri(100, 999)]))
        if len(xs) < 4:
            return None
        xs = sh(xs)[:4]
        up = R.random() < 0.5
        g = sorted(xs, reverse=not up)
        f = lambda ys: ", ".join(num(y) for y in ys)
        w = list(g)
        w[1], w[2] = w[2], w[1]
        return mcq("%s sayılarının %s sıralanışı hangisidir?" % (f(xs), "küçükten büyüğe" if up else "büyükten küçüğe"), f(g),
                   [f(g[::-1]), f(w), f(xs) if xs != g else f(w[::-1])], "Doğru sıralama: <b>%s</b>." % f(g))

    def once_sonra():
        n = ri(101, 998)
        k = ri(0, 2)
        if k == 0:
            return mcq("<b>%s</b> sayısından hemen sonra gelen sayı hangisidir?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 2)],
                       "Hemen sonra gelen sayı 1 fazlasıdır: <b>%s</b>." % num(n + 1))
        if k == 1:
            return mcq("<b>%s</b> sayısından hemen önce gelen sayı hangisidir?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 2)],
                       "Hemen önce gelen sayı 1 eksiğidir: <b>%s</b>." % num(n - 1))
        return mcq("%s ile %s arasındaki sayı hangisidir?" % (num(n - 1), num(n + 1)), num(n), [num(n - 1) if False else num(n + 2), num(n - 2), num(n + 10)],
                   "Sıralama %s, %s, %s." % (num(n - 1), num(n), num(n + 1)))

    def onluga():
        n = ri(101, 994)
        if n % 10 == 0:
            return None
        r = int(math.floor(n / 10.0 + 0.5)) * 10
        lo, hi = n // 10 * 10, n // 10 * 10 + 10
        return mcq("<b>%s</b> sayısı en yakın onluğa yuvarlanırsa kaç olur?" % num(n), num(r), [num(lo if r == hi else hi), num(int(math.floor(n / 100.0 + 0.5)) * 100), num(n // 10)],
                   "%s, %s ile %s arasında. Birler basamağı %d olduğu için %s. Cevap <b>%s</b>." % (num(n), num(lo), num(hi), n % 10,
                                                                                    "yukarı yuvarlanır" if n % 10 >= 5 else "aşağı yuvarlanır", num(r)))

    def yuzluge():
        n = ri(101, 949)
        if n % 100 == 0:
            return None
        r = int(math.floor(n / 100.0 + 0.5)) * 100
        lo, hi = n // 100 * 100, n // 100 * 100 + 100
        return mcq("<b>%s</b> sayısı en yakın yüzlüğe yuvarlanırsa kaç olur?" % num(n), num(r),
                   [num(lo if r == hi else hi), num(int(math.floor(n / 10.0 + 0.5)) * 10), num(n // 100)],
                   "Onlar basamağı %d. %s, bu yüzden <b>%s</b>." % (n // 10 % 10, "5 ve üstü yukarı yuvarlanır" if n // 10 % 10 >= 5 else "5'ten küçük olduğu için aşağı yuvarlanır", num(r)))

    def dogru():
        lo = ri(1, 8) * 100
        v = lo + ri(1, 9) * 10
        pic = sayi_dogrusu(lo, lo + 100, 10, [(v, "A")], labels=[lo, lo + 100], width=400)
        r = lo + 100 if v - lo >= 50 else lo
        k = ri(0, 1)
        if k == 0:
            return mcq("Sayı doğrusunda A noktası hangi sayıyı gösterir?" + pic, num(v), [num(v + 10), num(v - 10), num(lo + (v - lo) // 10)],
                       "Her çentik 10 artar: %s, … A = <b>%s</b>." % (num(lo), num(v)))
        if v - lo == 50:
            return None
        return mcq("A noktasının gösterdiği sayı en yakın yüzlüğe yuvarlanırsa kaç olur?" + pic, num(r), [num(lo + 100 if r == lo else lo), num(v), num(lo + 50)],
                   "A = %s. %s sayısına daha yakın: <b>%s</b>." % (num(v), num(r), num(r)))

    sets = [("Sayıları karşılaştırma", [(karsilastir, 20)]),
            ("Sıralama, önce ve sonra", [(sirala, 12), (once_sonra, 8)]),
            ("En yakın onluğa yuvarlama", [(onluga, 20)]),
            ("En yakın yüzlüğe yuvarlama", [(yuzluge, 14), (dogru, 6)]),
            ("Sayı doğrusu ve karışık", [(dogru, 10), (once_sonra, 5), (onluga, 5)])]
    return unit("sayilari-siralama-ve-yuvarlama", "S", "MAT.3.1.3", 2, "Sayıları Karşılaştırma, Sıralama ve Yuvarlama", "Sıralama ve Yuvarlama",
                "1000'e kadar sayıları öncelik ve sonralık ilişkisine göre sıralar; en yakın onluğa ve yüzlüğe göre ifade eder.",
                "3. sınıf sayıları karşılaştırma, sıralama ve yuvarlama çalışma kâğıdı: büyük-küçük işareti, küçükten büyüğe sıralama, hemen önce ve sonra gelen sayı, en yakın onluğa ve yüzlüğe yuvarlama. 100 soru ve cevap anahtarı.",
                "Önce en büyük basamağa bak", "Yuvarlarken bir sağdaki basamak 5 ve üstüyse yukarı.", sets,
                ["İki sayıyı karşılaştırırken önce yüzler basamağına bakılır. Eşitse onlar, sonra birler basamağı karşılaştırılır.",
                 "En yakın onluğa yuvarlarken birler basamağına bakılır: 0–4 ise aşağı, 5–9 ise yukarı yuvarlanır.",
                 "En yakın yüzlüğe yuvarlarken onlar basamağına bakılır: 347 → 300, 362 → 400."],
                [("458 ve 485", ["yüzler eşit (4)", "onlar: 5 &lt; 8"], "458 &lt; 485"), ("273 en yakın onluğa", ["birler 3 → aşağı"], "270")],
                [["Basamak sayısına bakmadan karşılaştırmak", "Önce yüzler basamağı karşılaştırılır"], ["347 en yakın yüzlüğe: 350", "Yüzlüğe yuvarlanınca 300 olur"],
                 ["265 en yakın onluğa: 260", "Birler 5 ise yukarı: 270"]],
                [("&lt; ve &gt; işaretleri nasıl okunur?", "&lt; küçüktür, &gt; büyüktür diye okunur. İşaretin açık tarafı büyük sayıya bakar."),
                 ("Yuvarlama ne işe yarar?", "Tahmin yaparken ve bir sayıyı kolay söylemek için kullanılır: 298 yaklaşık 300'dür."),
                 ("Tam ortadaki sayılar nasıl yuvarlanır?", "Birler basamağı 5 olan sayılar yukarı yuvarlanır: 45 → 50.")])


# ============================================================ 3. ritmik sayma
def u3():
    SAY = [(6, 60), (7, 70), (8, 80), (9, 90), (10, 1000), (100, 1000)]

    def ileri():
        d, mx = ch(SAY)
        s = ri(0, mx // d - 5) * d
        xs = [s + d * i for i in range(5)]
        j = ri(1, 4)
        show = ", ".join(num(x) if i != j else "…" for i, x in enumerate(xs))
        return mcq("%s ileri sayıyoruz. Noktalı yere hangi sayı gelir?<br>%s" % (cap(dagit(d)), show), num(xs[j]),
                   [num(xs[j] + 1), num(xs[j] - 1), num(xs[j] + d), num(xs[j] - d + 1)],
                   "Her adımda %d eklenir: <b>%s</b>." % (d, num(xs[j])))

    def geri():
        d, mx = ch(SAY)
        s = ri(4, mx // d) * d
        xs = [s - d * i for i in range(5)]
        if xs[-1] < 0:
            return None
        nx = xs[-1] - d
        if nx < 0:
            return None
        return mcq("%s geriye sayıyoruz: %s, … Sonraki sayı hangisidir?" % (cap(dagit(d)), ", ".join(num(x) for x in xs)), num(nx),
                   [num(xs[-1] + d), num(nx + 1), num(nx - d), num(nx - 1)], "Her adımda %d çıkarılır: <b>%s</b>." % (d, num(nx)))

    def hangisi():
        d, mx = ch(SAY[:4])
        good = [d * i for i in range(1, mx // d + 1)]
        bad = [x for x in range(d + 1, mx) if x % d]
        c = ch(bad)
        w = sh(good)[:3]
        return mcq("%s sayarken hangi sayıyı <b>söylemeyiz</b>? (%s)" % (cap(dagit(d)), ", ".join(num(x) for x in sorted(w + [c]))), num(c), [num(x) for x in w],
                   "%s sayarken %d sayısının katlarını söyleriz. %s, %d sayısının katı değil." % (cap(dagit(d)), d, num(c), d))

    def kac_adim():
        d, mx = ch(SAY[:4])
        n = ri(3, mx // d)
        return mcq("Sıfırdan başlayıp %s ileri sayıyoruz. %d. söylediğimiz sayı hangisidir?" % (dagit(d), n), num(n * d),
                   [num((n - 1) * d), num((n + 1) * d), num(n * d + 1), num(n + d)], "%d tane %d: %d × %d = <b>%s</b>." % (n, d, n, d, num(n * d)))

    def kural():
        d = ch([6, 7, 8, 9, 10, 100, 5, 4, 3])
        mx = 1000 if d >= 10 else d * 10
        s = ri(0, mx // d - 4) * d
        xs = [s + d * i for i in range(4)]
        good = "%s ileri sayılıyor" % dagit(d)
        others = [x for x in (6, 7, 8, 9, 10, 100, 5, 4, 3, 20, 50) if x != d]
        near = sorted(others, key=lambda x: abs(x - d))[:2]
        return mcq("%s … Bu sayılar nasıl sayılıyor?" % ", ".join(num(x) for x in xs), cap(good),
                   [cap("%s ileri sayılıyor" % dagit(x)) for x in near] + [cap("%s geri sayılıyor" % dagit(d))],
                   "Ardışık iki sayı arasındaki fark %d: <b>%s</b>." % (d, good))

    sets = [("Altışar, yedişer ileri sayma", [(ileri, 20)]),
            ("Geriye sayma", [(geri, 20)]),
            ("Hangi sayı söylenmez?", [(hangisi, 20)]),
            ("Sayma kuralını bulma", [(kural, 14), (kac_adim, 6)]),
            ("Karışık", [(kac_adim, 10), (ileri, 5), (geri, 5)])]
    return unit("ritmik-sayma", "S", "MAT.3.1.4", 3, "Ritmik Sayma: Altışar, Yedişer, Sekizer, Dokuzar, Onar ve Yüzer", "Ritmik Sayma",
                "İleriye ve geriye ritmik sayma yapar: 60 içinde altışar, 70 içinde yedişer, 80 içinde sekizer, 90 içinde dokuzar, 1000 içinde onar ve yüzer.",
                "3. sınıf ritmik sayma çalışma kâğıdı: altışar, yedişer, sekizer, dokuzar, onar ve yüzer ileri ve geri sayma, eksik sayıyı bulma, sayma kuralını bulma. 100 soru ve cevap anahtarı.",
                "Her adımda aynı sayıyı ekle", "Geriye sayarken aynı sayıyı çıkar.", sets,
                ["Ritmik saymada her adımda aynı sayı eklenir (ileri) ya da çıkarılır (geri).",
                 "Altışar sayarken söylenen sayılar 6'nın katlarıdır: 6, 12, 18, 24, 30, …",
                 "Çarpım tablosu ritmik saymadan gelir: yedişer sayınca 5. sayı 7 × 5 = 35."],
                [("Sekizer ileri: 16, 24, …", ["24 + 8"], "32"), ("Dokuzar geri: 81, 72, 63, …", ["63 − 9"], "54")],
                [["Geriye sayarken sayı eklemek", "Geriye sayarken çıkarılır"], ["Bir adımı atlamak", "Her adımda aynı sayıyı kontrol et"],
                 ["Yedişer: 7, 14, 22", "14 + 7 = 21"]],
                [("Ritmik sayma neden önemlidir?", "Çarpma ve bölmeyi hızlı yapmayı sağlar ve örüntüleri fark ettirir."),
                 ("Onar ve yüzer sayarken hangi basamak değişir?", "Onar sayarken onlar basamağı, yüzer sayarken yüzler basamağı bir artar."),
                 ("Sıfırdan başlamak gerekir mi?", "Hayır. Ritmik saymaya herhangi bir sayıdan başlanabilir, önemli olan her adımda aynı sayıyı eklemektir.")])


# ============================================================ 4. tek ve çift sayılar
def u4():
    def tur():
        n = ri(11, 999)
        g = "çift" if n % 2 == 0 else "tek"
        return mcq("<b>%s</b> sayısı tek mi çift mi?" % num(n), cap(g), ["Tek" if g == "çift" else "Çift", "Hem tek hem çift", "Ne tek ne çift"],
                   "Birler basamağı %d. %s, bu yüzden sayı <b>%s</b>." % (n % 10, "0, 2, 4, 6, 8 ise çift" if g == "çift" else "1, 3, 5, 7, 9 ise tek", g))

    def bul():
        want = ch(["tek", "çift"])
        xs = []
        while len(xs) < 3:
            x = ri(10, 999)
            if (x % 2 == 0) == (want == "tek") and x not in xs:
                xs.append(x)
        g = ri(10, 999)
        if (g % 2 == 0) != (want == "çift"):
            g += 1
        return mcq("Hangisi <b>%s</b> sayıdır? (%s)" % (want, ", ".join(num(x) for x in sorted(xs + [g]))), num(g), [num(x) for x in xs],
                   "Birler basamağına bakılır. %s sayısının birler basamağı %d: <b>%s</b>." % (num(g), g % 10, want))

    def resim():
        n = ri(5, 16)
        g = "çift" if n % 2 == 0 else "tek"
        return mcq("Nesneler ikişerli eşlenmiş. Nesne sayısı tek mi çift mi?" + noktalar(n), cap(g), ["Tek" if g == "çift" else "Çift", "Hiç eş yok", "Bilinemez"],
                   "%d nesne var. %s" % (n, "Hepsi eşlendi: <b>çift</b>." if g == "çift" else "Bir nesne eşsiz kaldı: <b>tek</b>."))

    def toplam():
        k = ri(0, 1)
        a, b = ri(1, 499), ri(1, 499)
        s = a + b
        g = "çift" if s % 2 == 0 else "tek"
        ta, tb = ("tek" if a % 2 else "çift"), ("tek" if b % 2 else "çift")
        if k == 0:
            return mcq("%s + %s toplamı tek mi çift mi? (İşlemi yapmadan bul.)" % (num(a), num(b)), cap(g), ["Tek" if g == "çift" else "Çift", "Toplam bulunmadan bilinemez", "Hem tek hem çift"],
                       "%s + %s = %s olduğu için toplam <b>%s</b>." % (ta, tb, g, g))
        p = ch([("tek", "tek", "çift"), ("çift", "çift", "çift"), ("tek", "çift", "tek"), ("çift", "tek", "tek")])
        return mcq("Bir %s sayı ile bir %s sayının toplamı nasıl bir sayıdır? (Örnek: %s + %s)" % (p[0], p[1], num(a | 1 if p[0] == "tek" else a & ~1 or 2), num(b | 1 if p[1] == "tek" else b & ~1 or 2)),
                   cap(p[2]) + " sayı", ["Tek sayı" if p[2] == "çift" else "Çift sayı", "Sıfır", "Bazen tek bazen çift"],
                   "%s + %s her zaman <b>%s</b> olur." % (p[0], p[1], p[2]))

    def ardisik():
        n = ri(20, 990)
        k = ri(0, 1)
        if k == 0:
            g = n + (2 if n % 2 == 0 else 1)
            return mcq("<b>%s</b> sayısından sonra gelen ilk çift sayı hangisidir?" % num(n), num(g), [num(n + 1) if n % 2 == 0 else num(n + 2), num(g + 2), num(n)],
                       "Çift sayılar ikişer artar. %s sayısından sonraki ilk çift sayı <b>%s</b>." % (num(n), num(g)))
        g = n + (2 if n % 2 else 1)
        return mcq("<b>%s</b> sayısından sonra gelen ilk tek sayı hangisidir?" % num(n), num(g), [num(n + 1) if n % 2 else num(n + 2), num(g + 2), num(n)],
                   "Tek sayılar ikişer artar. %s sayısından sonraki ilk tek sayı <b>%s</b>." % (num(n), num(g)))

    sets = [("Tek mi çift mi?", [(tur, 20)]),
            ("Eşleme ile tek ve çift", [(resim, 12), (tur, 8)]),
            ("Tek ve çift sayıyı bulma", [(bul, 20)]),
            ("Tek ve çift sayıların toplamı", [(toplam, 20)]),
            ("Karışık", [(ardisik, 12), (bul, 8)])]
    return unit("tek-ve-cift-sayilar", "S", "MAT.3.1.5, MAT.3.1.6", 4, "Tek ve Çift Sayılar ve Toplamları", "Tek ve Çift Sayılar",
                "Sayıları tek-çift olarak sınıflandırır; tek ve çift sayıların toplamlarının tek ya da çift olduğunu belirler.",
                "3. sınıf tek ve çift sayılar çalışma kâğıdı: 1000'e kadar sayılarda tek ve çift, eşleme modeli, tek ve çift sayıların toplamının tek mi çift mi olduğu. 100 soru ve cevap anahtarı.",
                "Birler basamağına bak", "0, 2, 4, 6, 8 çift; 1, 3, 5, 7, 9 tek.", sets,
                ["Bir sayının tek mi çift mi olduğunu birler basamağı gösterir.",
                 "Nesneler ikişer ikişer eşlenince hepsi eşlenirse sayı çifttir; bir tane eşsiz kalırsa tektir.",
                 "Tek + tek = çift, çift + çift = çift, tek + çift = tek."],
                [("438 tek mi çift mi?", ["birler basamağı 8"], "çift"), ("27 + 35 toplamı", ["tek + tek"], "çift")],
                [["Yüzler basamağına bakmak", "Yalnızca birler basamağına bakılır"], ["Tek + tek = tek sanmak", "İki eşsiz nesne birlikte eş olur: çift"],
                 ["0 sayısını tek sanmak", "0 çift sayıdır"]],
                [("0 çift sayı mıdır?", "Evet. 0'ın yanında eşsiz nesne kalmaz; 0 çift sayıdır."),
                 ("Büyük sayılarda da birler basamağına bakmak yeter mi?", "Evet. 1.000'den büyük sayılarda da yalnızca birler basamağına bakılır."),
                 ("Toplamı bulmadan tek mi çift mi olduğunu nasıl bilirim?", "Toplanan sayıların tek mi çift mi olduğuna bak: tek + tek ve çift + çift çift, tek + çift tek olur.")])


# ============================================================ 5. örüntüler
def kareler(counts, label="şekil örüntüsü"):
    """her adımda yan yana kareler sırası (counts: [3, 5, 7])"""
    s, x = [], 8
    q = 12
    hmax = 0
    for i, c in enumerate(counts):
        rows = (c + 4) // 5
        for t in range(c):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                     % (x + (t % 5) * q, 10 + (t // 5) * q, q, q, FILL, GREEN))
        hmax = max(hmax, rows)
        w = min(c, 5) * q
        s.append(text(x + w / 2.0, 10 + 5 * q + 18, "%d. adım" % (i + 1), 12, weight=600))
        x += w + 26
    return wrap(x, 10 + 5 * q + 26, "".join(s), label)


def u5():
    def sayi():
        d = ch([2, 3, 4, 5, 6, 10, 20, 25, 50, 100, 7, 8, 9])
        up = R.random() < 0.65
        s = ri(1, 60) * (1 if d < 20 else d // 5)
        xs = [s + d * i for i in range(5)] if up else [s + d * (4 - i) for i in range(5)]
        nx = xs[-1] + (d if up else -d)
        if nx < 0 or max(xs) > 999 or nx > 999:
            return None
        return mcq("Örüntüde sonraki sayı hangisidir? %s, …" % ", ".join(num(x) for x in xs), num(nx),
                   [num(xs[-1] + (-d if up else d)), num(nx + 1), num(nx + d if up else nx - d), num(nx - 1)],
                   "Kural: her adımda %s. Sonraki sayı <b>%s</b>." % ("%d eklenir" % d if up else "%d çıkarılır" % d, num(nx)))

    def kural():
        d = ch([2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 25, 50, 100])
        up = R.random() < 0.6
        s = ri(1, 50)
        xs = [s + d * i for i in range(4)] if up else [s + d * (3 - i) for i in range(4)]
        g = "%d eklenir" % d if up else "%d çıkarılır" % d
        return mcq("%s … Bu örüntünün kuralı nedir?" % ", ".join(num(x) for x in xs), "Her adımda " + g,
                   ["Her adımda %d %s" % (d, "çıkarılır" if up else "eklenir"), "Her adımda %d eklenir" % (d + 1), "Her adımda %d eklenir" % max(1, d - 1)],
                   "Ardışık iki sayının farkı %d. Sayılar %s: <b>%s</b>." % (d, "büyüyor" if up else "küçülüyor", g))

    def eksik():
        d = ch([3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 25])
        s = ri(1, 80)
        xs = [s + d * i for i in range(6)]
        j = ri(1, 4)
        return mcq("Örüntüde boş bırakılan sayı hangisidir? %s" % ", ".join(num(x) if i != j else "…" for i, x in enumerate(xs)), num(xs[j]),
                   [num(xs[j] + 1), num(xs[j] - 1), num(xs[j] + d)], "Her adımda %d eklenir: <b>%s</b>." % (d, num(xs[j])))

    def sekil():
        a, d = ri(1, 4), ri(1, 4)
        cs = [a + d * i for i in range(3)]
        n = ri(4, 6)
        v = a + d * (n - 1)
        if v > 25:
            return None
        return mcq("Şekil örüntüsünde her adımda kare sayısı aynı kuralla artıyor. %d. adımda kaç kare olur?" % n + kareler(cs), num(v),
                   [num(v + d), num(v - d), num(v + 1), num(a * n)], "Her adımda %d kare eklenir: %s, … %d. adımda <b>%d</b> kare." % (d, ", ".join(str(c) for c in cs), n, v))

    def sekil_kural():
        a, d = ri(1, 5), ri(2, 5)
        cs = [a + d * i for i in range(3)]
        g = "Her adımda %d kare eklenir" % d
        return mcq("Bu şekil örüntüsünün kuralı nedir?" + kareler(cs), g,
                   ["Her adımda %d kare eklenir" % x for x in (d + 1, d - 1 if d > 1 else d + 2, a)] if a != d else ["Her adımda %d kare eklenir" % x for x in (d + 1, d + 2, d - 1)],
                   "Kare sayıları %s: her adımda <b>%d</b> artıyor." % (", ".join(str(c) for c in cs), d))

    def dogru_mu():
        d = ch([3, 4, 5, 6, 7, 8, 9])
        s = ri(1, 30)
        xs = [s + d * i for i in range(5)]
        good = R.random() < 0.5
        if not good:
            j = ri(2, 4)
            xs[j] += ch([1, -1, 2])
        g = "Evet, her adımda %d eklenmiş" % d if good else "Hayır, kural bozulmuş"
        return mcq("%s sayılarının kuralı “her adımda %d ekle” midir?" % (", ".join(num(x) for x in xs), d), g,
                   ["Hayır, kural bozulmuş" if good else "Evet, her adımda %d eklenmiş" % d, "Evet, her adımda %d eklenmiş" % (d + 1), "Kural bulunamaz"],
                   "Ardışık farkları tek tek kontrol et: %s." % ", ".join(str(xs[i + 1] - xs[i]) for i in range(4)))

    sets = [("Sayı örüntüsünü devam ettirme", [(sayi, 20)]),
            ("Örüntünün kuralı", [(kural, 20)]),
            ("Eksik sayıyı bulma", [(eksik, 20)]),
            ("Şekil örüntüleri", [(sekil, 12), (sekil_kural, 8)]),
            ("Varsayımı sınama", [(dogru_mu, 12), (sekil, 8)])]
    return unit("oruntuler", "S", "MAT.3.1.7", 5, "Sayı ve Şekil Örüntüleri", "Örüntüler",
                "Sayı ve sayı temsiline dönüşen şekil örüntülerine dayalı çıkarım yapar: kuralı sözlü ifade eder ve örneklerle sınar.",
                "3. sınıf örüntüler çalışma kâğıdı: artan ve azalan sayı örüntüleri, örüntünün kuralı, eksik sayıyı bulma, şekil örüntüleri ve kuralı sınama. 100 soru ve cevap anahtarı.",
                "Ardışık iki terimin farkını bul", "Kuralı bütün terimlerde kontrol et.", sets,
                ["Örüntüde terimler belli bir kurala göre sıralanır. Kuralı bulmak için ardışık iki terimin farkına bakılır.",
                 "Kural bütün terimlerde aynı olmalıdır. Yalnızca ilk iki terime bakıp karar verme.",
                 "Şekil örüntülerinde her adımdaki şekil sayısını say ve sayı örüntüsüne dönüştür."],
                [("5, 9, 13, 17, …", ["fark 4"], "21"), ("Kareler: 2, 5, 8", ["her adımda 3 kare"], "4. adımda 11 kare")],
                [["Yalnızca son iki sayıya bakmak", "Bütün ardışık farkları kontrol et"], ["Azalan örüntüde ekleme yapmak", "Sayılar küçülüyorsa çıkarılır"],
                 ["Adım numarasını kare sayısı sanmak", "Her adımdaki kareleri tek tek say"]],
                [("Örüntü nedir?", "Belli bir kurala göre devam eden sayı ya da şekil dizisidir."),
                 ("Bir örüntünün kuralı nasıl sınanır?", "Kuralı ilk terime uygulayıp bütün terimleri yeniden elde etmeye çalış. Hepsi tutarsa kural doğrudur."),
                 ("Günlük hayatta örüntü var mı?", "Evet: takvimdeki haftalar, kaldırım taşları, kilim desenleri ve ritmik sayma birer örüntüdür.")])


# ============================================================ 6. kesirler
def u6():
    def okuma():
        n = ch([2, 3, 4, 5, 6, 8])
        k = ri(1, n - 1)
        if k > 1 and n in (2,):
            return None
        g = fr(k, n)
        return mcq("Şekildeki boyalı kısım bütünün kaçta kaçıdır?" + frac_pic(n, k), g,
                   [fr(n - k, n) if n - k != k else fr(k, n + 1), fr(k, n - k) if n - k != k and n - k > 0 else fr(k + 1, n), fr(n, k) if k > 1 else fr(k, n + 2), fr(1, n) if k != 1 else fr(1, n - 1)],
                   "Bütün %d eş parçaya bölünmüş, %d parça boyalı: <b>%s</b> (%s)." % (n, k, g, kesir_oku(k, n)))

    def yarim_ceyrek():
        F = [("yarım", fr(1, 2), 2), ("çeyrek", fr(1, 4), 4), ("bütün", fr(2, 2), 2), ("bütün", fr(4, 4), 4)]
        k = ri(0, 3)
        if k == 0:
            n, w = ch([(2, "yarım"), (4, "çeyrek")])
            return mcq("Bir bütün kaç tane %s içerir?" % w, str(n), [str(x) for x in (1, 3, 8, 2, 4) if x != n][:3],
                       "Bir bütün %d eş parçadan oluşur: %d tane %s." % (n, n, w))
        if k == 1:
            w, g, n = ch(F[:2])
            return mcq("“%s” kesir olarak nasıl gösterilir?" % cap(w), g, [fr(1, 3), fr(2, 4) if n == 4 else fr(1, 4), fr(n, 1), fr(1, 2) if n == 4 else fr(2, 1)],
                       "%s: bütün %d eş parçaya bölünür, 1 parça alınır: <b>%s</b>." % (cap(w), n, g))
        if k == 2:
            n = ch([2, 4])
            kk = ri(1, n)
            w = {(2, 1): "yarım", (2, 2): "bütün", (4, 1): "çeyrek", (4, 2): "yarım", (4, 3): "üç çeyrek", (4, 4): "bütün"}[(n, kk)]
            return mcq("Boyalı kısım hangisidir?" + frac_pic(n, kk), cap(w), [cap(x) for x in ("yarım", "çeyrek", "bütün", "üç çeyrek") if x != w],
                       "%d eş parçadan %d tanesi boyalı: <b>%s</b>." % (n, kk, w))
        item = ch(["ekmek", "pizza", "karpuz", "pasta", "elma", "kâğıt", "simit", "lahmacun"])
        n, w = ch([(2, "yarısını"), (4, "çeyreğini")])
        return mcq("Bir %s %d eş parçaya bölünüyor. Bir parça bütünün kaçta kaçıdır?" % (item, n), fr(1, n),
                   [fr(n, 1), fr(1, n + 1), fr(2, n) if n == 4 else fr(1, 4)], "%d eş parçadan biri: <b>%s</b> (%s)." % (n, fr(1, n), kesir_oku(1, n)))

    def birim():
        n = ch([2, 3, 4, 5, 6, 7, 8, 9, 10])
        k = ri(0, 2)
        if k == 0:
            return mcq("Paydası %d olan birim kesir hangisidir?" % n, fr(1, n), [fr(n, 1), fr(n - 1, n) if n > 2 else fr(2, 3), fr(1, n + 1)],
                       "Birim kesrin payı 1'dir: <b>%s</b>." % fr(1, n))
        if k == 1:
            return mcq("Bir bütün %d eş parçaya bölünürse her parça kaç olur?" % n, fr(1, n), [fr(n, 1), fr(1, n - 1), fr(2, n) if n > 2 else fr(1, 3)],
                       "Her parça bütünün <b>%s</b> kadarıdır." % fr(1, n))
        return mcq("%s kesrinden kaç tane bir bütünü oluşturur?" % fr(1, n), str(n), [str(n - 1), str(n + 1), "1"],
                   "%d tane %s bir bütündür." % (n, fr(1, n)))

    def pay_payda():
        n = ch([3, 4, 5, 6, 7, 8, 9, 10])
        a = ri(1, n - 1)
        k = ri(0, 3)
        if k == 0:
            return mcq("%s kesrinin paydası kaçtır?" % fr(a, n), str(n), [str(a), str(n - a), str(n + a)] if a != n - a else [str(a), str(n + a), "1"],
                       "Kesir çizgisinin altındaki sayı paydadır: <b>%d</b>." % n)
        if k == 1:
            return mcq("%s kesrinin payı kaçtır?" % fr(a, n), str(a), [str(n), str(n - a), str(n + a)] if a != n - a else [str(n), str(n + a), "1"],
                       "Kesir çizgisinin üstündeki sayı paydır: <b>%d</b>." % a)
        if k == 2:
            return mcq("%s kesrinde payda neyi gösterir?" % fr(a, n), "Bütünün kaç eş parçaya bölündüğünü",
                       ["Kaç parça alındığını", "Kaç parça kaldığını", "Parçaların ne kadar büyük olduğunu"],
                       "Payda (%d) bütünün kaç eş parçaya bölündüğünü, pay (%d) kaç parça alındığını gösterir." % (n, a))
        return mcq("%s kesri nasıl okunur?" % fr(a, n), cap(kesir_oku(a, n)), [cap(kesir_oku(n - a, n)) if n - a != a else cap(kesir_oku(a, n + 1 if n < 10 else n - 1)),
                                                                             "%s bölü %s" % (cap(oku(n)), oku(a)), cap(oku(a)) + " " + oku(n)],
                   "Önce payda sonra pay okunur: <b>%s</b>." % kesir_oku(a, n))

    def kalan():
        n = ch([3, 4, 5, 6, 8, 10])
        a = ri(1, n - 1)
        item = ch(["pizza", "pasta", "çikolata", "kek", "börek"])
        name = K.next()
        return mcq("%s, %d eş parçaya bölünmüş bir %s parçasından %d tanesini yedi. Yenmeyen kısım bütünün kaçta kaçıdır?" % (name, n, item, a), fr(n - a, n),
                   [fr(a, n) if a != n - a else fr(a, n + 1), fr(n - a, a) if n - a != a else fr(1, n), fr(1, n) if n - a != 1 else fr(2, n)],
                   "%d parçadan %d tanesi yendi, %d parça kaldı: <b>%s</b>." % (n, a, n - a, fr(n - a, n)))

    sets = [("Bütün, yarım ve çeyrek", [(yarim_ceyrek, 20)]),
            ("Boyalı kısmı kesirle gösterme", [(okuma, 20)]),
            ("Birim kesirler", [(birim, 20)]),
            ("Pay ve payda", [(pay_payda, 20)]),
            ("Problemler", [(kalan, 12), (okuma, 8)])]
    return unit("kesirler", "S", "MAT.3.1.9, MAT.3.1.10, MAT.3.1.11", 6, "Kesirler: Bütün, Yarım, Çeyrek, Birim Kesir, Pay ve Payda", "Kesirler",
                "Bütün, yarım ve çeyreğin kesirle gösterimi için modellerden yararlanır; bir bütünü eş parçalar oluşturacak şekilde birim kesir olarak çözümler; bir kesrin payı ile paydası arasındaki ilişkiyi çözümler.",
                "3. sınıf kesirler çalışma kâğıdı: bütün, yarım ve çeyrek, boyalı kısmı kesirle gösterme, birim kesirler, pay ve payda, kesirlerin okunuşu ve problemler. 100 soru ve cevap anahtarı.",
                "Payda: kaç eş parça? Pay: kaç parça?", "Bütün mutlaka eş parçalara bölünmelidir.", sets,
                ["Bir bütün eş parçalara bölünür. Bir eş parça, payı 1 olan birim kesirle gösterilir: 1/4 (dörtte bir).",
                 "Kesrin altındaki sayı payda, üstündeki sayı paydır. Payda bütünün kaç eş parçaya bölündüğünü, pay kaç parça alındığını gösterir.",
                 "İki yarım ya da dört çeyrek bir bütündür."],
                [("4 eş parçadan 3'ü boyalı", ["payda 4, pay 3"], "3/4 (dörtte üç)"), ("Paydası 5 olan birim kesir", ["pay 1"], "1/5")],
                [["Pay ve paydayı yer değiştirmek", "Payda bütündeki parça sayısıdır (altta)"], ["Eş olmayan parçaları kesir saymak", "Parçalar eş olmalıdır"],
                 ["3/4 kesrini “üçte dört” okumak", "Önce payda okunur: dörtte üç"]],
                [("Birim kesir nedir?", "Payı 1 olan kesirdir: 1/2, 1/3, 1/4 gibi. Bütünün bir eş parçasını gösterir."),
                 ("Yarım ve çeyrek arasındaki ilişki nedir?", "Bir yarım iki çeyrektir; iki yarım ya da dört çeyrek bir bütündür."),
                 ("Kesirler günlük hayatta nerede kullanılır?", "Ekmek, pizza ya da pastayı paylaşırken ve “yarım saat”, “çeyrek kala” gibi zaman ifadelerinde.")])


# ============================================================ 7. saat
MIN5 = list(range(0, 60, 5))


def u7():
    def oku_analog():
        h, m = ri(1, 12), ch(MIN5)
        g = hm(h, m)
        w = [hm(m // 5 if m else 12, h * 5 % 60), hm(h % 12 + 1, m), hm(h - 1 if h > 1 else 12, m) if m >= 30 else hm(h, (m + 5) % 60)]
        return mcq("Saat kaçı gösteriyor?" + saat_svg(h, m), g, w + [hm(h, (60 - m) % 60)],
                   "Kısa (akrep) %d, uzun (yelkovan) %d dakikayı gösteriyor: <b>%s</b>." % (h, m, g))

    def soz():
        h, m = ri(1, 12), ch([0, 15, 30, 45, 5, 10, 20, 25, 35, 40, 50, 55])
        g = hm(h, m)
        w = [hm(h % 12 + 1, m), hm(h - 1 if h > 1 else 12, m), hm(h, (60 - m) % 60) if m not in (0, 30) else hm(h, (m + 15) % 60)]
        if m > 30:
            w[0] = hm(h % 12 + 1, 60 - m)
        return mcq("“%s” hangi saati gösterir?" % cap(saat_oku(h, m)), g, w, "%s: <b>%s</b>." % (cap(saat_oku(h, m)), g))

    def soz_ters():
        h, m = ri(1, 12), ch([15, 30, 45, 10, 20, 40, 50])
        g = cap(saat_oku(h, m))
        alts = [cap(saat_oku(h % 12 + 1, m)), cap(saat_oku(h, (60 - m) % 60)) if m != 30 else cap(saat_oku(h, 15)), cap(saat_oku(h - 1 if h > 1 else 12, m))]
        return mcq("Saat %s nasıl okunur?" % hm(h, m), g, alts, "%s → <b>%s</b>." % (hm(h, m), saat_oku(h, m)))

    def dijital():
        h, m = ri(1, 11), ch(MIN5)
        k = ri(0, 1)
        if k == 0:
            g = hm(h + 12, m)
            return mcq("Öğleden sonra %s dijital saatte nasıl görünür?" % saat_oku(h, m), g, [hm(h, m), hm(h + 10, m), hm(h + 11, m)],
                       "Öğleden sonra saate 12 eklenir: %d + 12 = %d. Cevap <b>%s</b>." % (h, h + 12, g))
        g = cap(saat_oku(h, m))
        return mcq("Dijital saat %s gösteriyor. Bu saat nasıl okunur?" % hm(h + 12, m), g,
                   [cap(saat_oku((h + 2) % 12 or 12, m)), cap(saat_oku(h % 12 + 1, m)), cap(saat_oku(h, (m + 30) % 60))],
                   "%d − 12 = %d. %s, <b>%s</b>." % (h + 12, h, hm(h + 12, m), saat_oku(h, m)))

    def zaman():
        k = ri(0, 1)
        h, m = ri(7, 17), ch(MIN5)
        d = ch([10, 15, 20, 25, 30, 35, 40, 45, 50])
        t = h * 60 + m + d
        e, f = divmod(t, 60)
        act = ch(["Ders", "Film", "Maç", "Piknik", "Oyun", "Kitap okuma saati", "Resim dersi", "Yüzme dersi"])
        if k == 0:
            return mcq("%s saat %s olunca başlıyor ve %d dakika sürüyor. Saat kaçta biter?" % (act, hm(h, m), d), hm(e, f),
                       [hm(e, (f + 5) % 60), hm(h, (m + d) % 60) if m + d >= 60 else hm(e + 1, f), hm(e, (f - 10) % 60)],
                       "%s + %d dakika = <b>%s</b>." % (hm(h, m), d, hm(e, f)))
        return mcq("%s saat %s olunca başladı, saat %s olunca bitti. Kaç dakika sürdü?" % (act, hm(h, m), hm(e, f)), "%d dakika" % d,
                   ["%d dakika" % x for x in (d + 10, d - 5, d + 40) if x > 0] + ["%d dakika" % (d + 5)],
                   "%s ile %s arası <b>%d dakika</b>." % (hm(h, m), hm(e, f), d))

    sets = [("Analog saati okuma", [(oku_analog, 20)]),
            ("Çeyrek geçe, çeyrek kala, buçuk", [(soz, 20)]),
            ("Saatin okunuşu", [(soz_ters, 20)]),
            ("Dijital saat: sabah ve öğleden sonra", [(dijital, 20)]),
            ("Ne zaman biter, ne kadar sürer?", [(zaman, 14), (oku_analog, 6)])]
    return unit("saat-okuma", "S", "MAT.3.1.12", 7, "Analog ve Dijital Saatte Zamanı Okuma", "Saat Okuma",
                "Analog ve dijital saatlerde zamanı okur ve yazar.",
                "3. sınıf saat okuma çalışma kâğıdı: analog saatte akrep ve yelkovan, buçuk, çeyrek geçiyor ve çeyrek var, dijital saat, öğleden sonra saatleri ve geçen süre. 100 soru ve cevap anahtarı.",
                "Akrep saati, yelkovan dakikayı gösterir", "Yelkovan bir tam tur atınca 60 dakika geçer.", sets,
                ["Akrep (kısa kol) saati, yelkovan (uzun kol) dakikayı gösterir. Yelkovan bir sayıdan diğerine 5 dakikada gider.",
                 "Yelkovan 3 üzerindeyse çeyrek geçiyor, 6 üzerindeyse buçuk, 9 üzerindeyse çeyrek var denir.",
                 "Dijital saatte öğleden sonraki saatler 12 eklenerek yazılır: öğleden sonra 3 → 15.00."],
                [("Akrep 4 ile 5 arasında, yelkovan 3 üzerinde", ["15 dakika geçmiş"], "04.15 (saat dördü çeyrek geçiyor)"),
                 ("Öğleden sonra saat beş buçuk", ["5 + 12 = 17"], "17.30")],
                [["Akrep ile yelkovanı karıştırmak", "Kısa kol saati, uzun kol dakikayı gösterir"], ["Yelkovan 4 üzerinde: 4 dakika", "Her sayı 5 dakikadır: 20 dakika"],
                 ["Çeyrek var: saati yanlış söylemek", "Saat beşe çeyrek var = 04.45"]],
                [("Akrep neden iki sayının arasında olabilir?", "Akrep saat ilerledikçe yavaşça bir sonraki sayıya doğru gider. Buçukta iki sayının tam ortasındadır."),
                 ("Dijital saatte 00.00 ne demektir?", "Gece yarısı, yani saat 12'dir. Yeni gün başlar."),
                 ("“Saat üçü on geçiyor” nasıl yazılır?", "03.10 olarak yazılır. Öğleden sonraysa 15.10.")])


# ============================================================ 8. zaman ölçü birimleri
SURE = [("Dişlerini fırçalamak", "2 dakika", ["2 saniye", "2 saat", "2 gün"]),
        ("Bir öğün yemek yemek", "20 dakika", ["20 saniye", "20 saat", "20 gün"]),
        ("Bir kez göz kırpmak", "1 saniye", ["1 dakika", "1 saat", "1 hafta"]),
        ("Gece uyumak", "9 saat", ["9 dakika", "9 saniye", "9 gün"]),
        ("Bir ders saati", "40 dakika", ["40 saniye", "40 saat", "4 gün"]),
        ("Bir çekirdeğin filizlenmesi", "1 hafta", ["1 dakika", "1 saniye", "1 yıl"]),
        ("Yaz tatili", "3 ay", ["3 gün", "3 saat", "3 yıl"]),
        ("Ellerini yıkamak", "30 saniye", ["30 saat", "30 gün", "30 ay"]),
        ("Ayakkabı bağcığını bağlamak", "10 saniye", ["10 saat", "10 gün", "10 hafta"]),
        ("Bir futbol maçı", "90 dakika", ["90 saniye", "90 gün", "90 saat"]),
        ("İlkokulu bitirmek", "4 yıl", ["4 gün", "4 hafta", "4 saat"]),
        ("Bir bardak su içmek", "10 saniye", ["10 saat", "10 gün", "10 ay"]),
        ("Bir masal kitabı okumak", "1 saat", ["1 saniye", "1 yıl", "1 ay"]),
        ("Okul yılı (eğitim öğretim yılı)", "9 ay", ["9 gün", "9 saat", "9 hafta"]),
        ("Bir şarkı dinlemek", "3 dakika", ["3 saniye", "3 saat", "3 gün"]),
        ("Ankara’dan İstanbul’a otobüsle gitmek", "6 saat", ["6 dakika", "6 saniye", "6 ay"]),
        ("Bir civcivin yumurtadan çıkması", "3 hafta", ["3 dakika", "3 saniye", "3 yıl"]),
        ("Bir topu yakalamak", "1 saniye", ["1 saat", "1 gün", "1 ay"])]


def u8():
    def birim():
        F = [("1 saat kaç dakikadır?", "60 dakika", ["100 dakika", "30 dakika", "24 dakika"]), ("1 dakika kaç saniyedir?", "60 saniye", ["100 saniye", "10 saniye", "30 saniye"]),
             ("1 gün kaç saattir?", "24 saat", ["12 saat", "60 saat", "7 saat"]), ("1 hafta kaç gündür?", "7 gün", ["5 gün", "10 gün", "30 gün"]),
             ("1 yıl kaç aydır?", "12 ay", ["10 ay", "52 ay", "365 ay"]), ("1 ay yaklaşık kaç gündür?", "30 gün", ["7 gün", "12 gün", "365 gün"]),
             ("1 yıl kaç gündür?", "365 gün (artık yılda 366)", ["100 gün", "12 gün", "52 gün"]), ("1 yıl yaklaşık kaç haftadır?", "52 hafta", ["12 hafta", "30 hafta", "100 hafta"]),
             ("Yarım saat kaç dakikadır?", "30 dakika", ["50 dakika", "15 dakika", "60 dakika"]), ("Çeyrek saat kaç dakikadır?", "15 dakika", ["25 dakika", "4 dakika", "30 dakika"])]
        q, g, w = ch(F)
        return mcq(q, g, w, "<b>%s</b>." % g)

    def donustur():
        k = ri(0, 5)
        n = ri(2, 9)
        if k == 0:
            return mcq("%d saat kaç dakikadır?" % n, "%d dakika" % (n * 60), ["%d dakika" % (n * 100), "%d dakika" % (n + 60), "%d dakika" % (n * 30)],
                       "1 saat = 60 dakika. %d × 60 = <b>%d dakika</b>." % (n, n * 60))
        if k == 1:
            return mcq("%d dakika kaç saniyedir?" % n, "%d saniye" % (n * 60), ["%d saniye" % (n * 100), "%d saniye" % (n * 10), "%d saniye" % (n + 60)],
                       "1 dakika = 60 saniye. %d × 60 = <b>%d saniye</b>." % (n, n * 60))
        if k == 2:
            return mcq("%d hafta kaç gündür?" % n, "%d gün" % (n * 7), ["%d gün" % (n * 5), "%d gün" % (n + 7), "%d gün" % (n * 10)],
                       "1 hafta = 7 gün. %d × 7 = <b>%d gün</b>." % (n, n * 7))
        if k == 3:
            n = ri(2, 5)
            return mcq("%d gün kaç saattir?" % n, "%d saat" % (n * 24), ["%d saat" % (n * 12), "%d saat" % (n * 60), "%d saat" % (n + 24)],
                       "1 gün = 24 saat. %d × 24 = <b>%d saat</b>." % (n, n * 24))
        if k == 4:
            d = ri(1, 10) * 7
            return mcq("%d gün kaç haftadır?" % d, "%d hafta" % (d // 7), ["%d hafta" % (d // 7 + 1), "%d hafta" % (d // 5), "%d hafta" % (d - 7) if d > 7 else "7 hafta"],
                       "7 gün = 1 hafta. %d ÷ 7 = <b>%d hafta</b>." % (d, d // 7))
        n = ri(2, 3)
        return mcq("%d yıl kaç aydır?" % n, "%d ay" % (n * 12), ["%d ay" % (n * 10), "%d ay" % (n + 12), "%d ay" % (n * 30)],
                   "1 yıl = 12 ay. %d × 12 = <b>%d ay</b>." % (n, n * 12))

    def karisik():
        k = ri(0, 2)
        if k == 0:
            h, m = ri(1, 3), ch([10, 15, 20, 30, 40, 45, 50])
            return mcq("%d saat %d dakika kaç dakikadır?" % (h, m), "%d dakika" % (h * 60 + m), ["%d dakika" % (h * 100 + m), "%d dakika" % (h + m), "%d dakika" % (h * 60 + m + 10)],
                       "%d × 60 + %d = <b>%d dakika</b>." % (h, m, h * 60 + m))
        if k == 1:
            t = ri(61, 200)
            if t % 60 == 0:
                return None
            return mcq("%d dakika kaç saat kaç dakikadır?" % t, "%d saat %d dakika" % divmod(t, 60),
                       ["%d saat %d dakika" % (t // 100, t % 100), "%d saat %d dakika" % (t // 60 + 1, t % 60), "%d saat %d dakika" % (t // 60, t % 60 + 10)],
                       "60 dakika = 1 saat. %d = %d × 60 + %d: <b>%d saat %d dakika</b>." % ((t,) + divmod(t, 60) + divmod(t, 60)))
        d = ri(8, 30)
        if d % 7 == 0:
            return None
        return mcq("%d gün kaç hafta kaç gündür?" % d, "%d hafta %d gün" % divmod(d, 7),
                   ["%d hafta %d gün" % (d // 10, d % 10), "%d hafta %d gün" % (d // 7 + 1, d % 7), "%d hafta %d gün" % (d // 7, d % 7 + 1)],
                   "7 gün = 1 hafta: <b>%d hafta %d gün</b>." % divmod(d, 7))

    def tahmin():
        a, g, w = ch(SURE)
        return mcq("%s yaklaşık ne kadar sürer?" % a, g, w, "%s yaklaşık <b>%s</b> sürer." % (a, g))

    def karsilastir():
        P = [("75 dakika", "1 saat", "75 dakika"), ("100 saniye", "1 dakika", "100 saniye"), ("2 hafta", "10 gün", "2 hafta"),
             ("1 yıl", "10 ay", "1 yıl"), ("50 dakika", "1 saat", "1 saat"), ("30 saat", "1 gün", "30 saat"), ("20 gün", "3 hafta", "3 hafta"),
             ("90 saniye", "2 dakika", "2 dakika"), ("15 ay", "1 yıl", "15 ay"), ("45 dakika", "yarım saat", "45 dakika"), ("1 gün", "20 saat", "1 gün"),
             ("40 saniye", "yarım dakika", "40 saniye"), ("8 gün", "1 hafta", "8 gün"), ("70 dakika", "1 saat 15 dakika", "1 saat 15 dakika")]
        a, b, g = ch(P)
        x, y = sorted([a, b])
        return mcq("Hangisi daha uzun bir süredir: %s, %s?" % (mi(x), mi(y)), cap(g), [cap(a if g == b else b), "İkisi eşit", "Karşılaştırılamaz"],
                   "Aynı birime çevir ve karşılaştır: <b>%s</b> daha uzun." % g)

    sets = [("Zaman ölçü birimleri", [(birim, 10), (donustur, 10)]),
            ("Birimleri dönüştürme", [(donustur, 20)]),
            ("Saat ve dakika, hafta ve gün", [(karisik, 20)]),
            ("Süreyi tahmin etme", [(tahmin, 18), (karsilastir, 2)]),
            ("Süreleri karşılaştırma", [(karsilastir, 12), (donustur, 8)])]
    return unit("zaman-olcu-birimleri", "S", "MAT.3.1.13, MAT.3.1.14", 8, "Zaman Ölçü Birimleri ve Süre Tahmini", "Zaman Ölçü Birimleri",
                "Zaman ölçü birimlerini (yıl, ay, hafta, gün, saat, dakika, saniye) ve aralarındaki ilişkileri çözümler; olayların oluş sürelerini tahmin ederek yargıda bulunur.",
                "3. sınıf zaman ölçme çalışma kâğıdı: yıl, ay, hafta, gün, saat, dakika ve saniye arasındaki ilişkiler, birim dönüştürme, olayların süresini tahmin etme ve süreleri karşılaştırma. 100 soru ve cevap anahtarı.",
                "1 saat = 60 dakika, 1 dakika = 60 saniye", "1 gün = 24 saat, 1 hafta = 7 gün, 1 yıl = 12 ay.", sets,
                ["Zaman birimleri: saniye, dakika, saat, gün, hafta, ay, yıl. 1 dakika 60 saniye, 1 saat 60 dakikadır.",
                 "Büyük birimden küçük birime çevirirken çarparız: 3 saat = 3 × 60 = 180 dakika.",
                 "Süre tahmininde olayı daha önce yaşadığın bir olayla karşılaştır: diş fırçalamak dakikalar, uyku saatler sürer."],
                [("2 saat 15 dakika = ? dakika", ["2 × 60 = 120", "120 + 15"], "135 dakika"), ("23 gün", ["3 hafta = 21 gün", "2 gün kalır"], "3 hafta 2 gün")],
                [["1 saat = 100 dakika sanmak", "1 saat = 60 dakika"], ["Haftayı 5 gün saymak", "Bir hafta 7 gündür"],
                 ["Birimi yazmadan cevap vermek", "Sürenin yanına birimi yaz: 20 dakika"]],
                [("Bir yılda kaç gün vardır?", "365 gün. Dört yılda bir şubat 29 gün çeker ve yıl 366 gün olur."),
                 ("Saniyeyi nasıl hissedebilirim?", "“Bir-elma, iki-elma” diye saymak yaklaşık birer saniye sürer."),
                 ("Neden süre tahmini yaparız?", "Günü planlamak, okula zamanında yetişmek ve ödevlere yeterli zaman ayırmak için.")])


# ============================================================ 9. uzunluk ve kütle
UZ = [("Bir kalemin uzunluğu", 15, "cm"), ("Sınıf kapısının yüksekliği", 2, "m"), ("Bir silginin uzunluğu", 4, "cm"),
      ("İki şehir arasındaki uzaklık", 120, "km"), ("Bir karıncanın boyu", 5, "mm"), ("Okul bahçesinin uzunluğu", 60, "m"),
      ("Bir defterin eni", 20, "cm"), ("Bir otobüsün uzunluğu", 12, "m"), ("Bir düğmenin çapı", 12, "mm"), ("Bir maraton koşusu", 42, "km"),
      ("Bir tırnağın eni", 10, "mm"), ("Bir yatağın uzunluğu", 2, "m"), ("Bir köprünün uzunluğu", 1, "km"), ("Bir kitabın kalınlığı", 2, "cm")]
KU = [("Bir elma", 150, "g"), ("Bir öğrenci", 30, "kg"), ("Bir fil", 5, "ton"), ("Bir kalem", 10, "g"), ("Bir çuval un", 25, "kg"),
      ("Bir kamyon", 10, "ton"), ("Bir paket tuz", 750, "g"), ("Bir karpuz", 6, "kg"), ("Bir mektup", 20, "g"), ("Bir balina", 100, "ton"),
      ("Bir çanta", 4, "kg"), ("Bir silgi", 15, "g"), ("Bir köpek", 20, "kg"), ("Bir otomobil", 1, "ton")]


def u9():
    def uz_birim():
        a, v, b = ch(UZ)
        return mcq("%s yaklaşık %d … olur. Noktalı yere hangi birim gelir?" % (a, v), b, [x for x in ("mm", "cm", "m", "km") if x != b],
                   "%s yaklaşık <b>%d %s</b>." % (a, v, b))

    def ku_birim():
        a, v, b = ch(KU)
        return mcq("%s yaklaşık %d … gelir. Noktalı yere hangi birim gelir?" % (a, v), b, [x for x in ("g", "kg", "ton", "cm") if x != b],
                   "%s yaklaşık <b>%d %s</b> gelir." % (a, v, b))

    def m_cm():
        k = ri(0, 3)
        if k == 0:
            m = ri(2, 9)
            return mcq("%d m kaç santimetredir?" % m, "%d cm" % (m * 100), ["%d cm" % (m * 10), "%d cm" % (m * 1000), "%d cm" % (m + 100)],
                       "1 m = 100 cm. %d × 100 = <b>%d cm</b>." % (m, m * 100))
        if k == 1:
            m, c = ri(1, 8), ri(5, 95)
            return mcq("%d m %d cm kaç santimetredir?" % (m, c), "%d cm" % (m * 100 + c), ["%d cm" % (m * 10 + c), "%d cm" % (m + c), "%d cm" % (m * 1000 + c)],
                       "%d m = %d cm. %d + %d = <b>%d cm</b>." % (m, m * 100, m * 100, c, m * 100 + c))
        if k == 2:
            t = ri(101, 899)
            if t % 100 == 0:
                return None
            return mcq("%d cm kaç metre kaç santimetredir?" % t, "%d m %d cm" % divmod(t, 100),
                       ["%d m %d cm" % (t // 10, t % 10), "%d m %d cm" % (t // 100 + 1, t % 100), "%d m %d cm" % (t % 100, t // 100) if t % 100 != t // 100 else "%d m" % t],
                       "100 cm = 1 m: <b>%d m %d cm</b>." % divmod(t, 100))
        c = ri(2, 9)
        return mcq("%d cm kaç milimetredir?" % c, "%d mm" % (c * 10), ["%d mm" % (c * 100), "%d mm" % (c + 10), "%d mm" % c],
                   "1 cm = 10 mm. %d × 10 = <b>%d mm</b>." % (c, c * 10))

    def kg_g():
        k = ri(0, 2)
        if k == 0:
            kg = ri(2, 9)
            return mcq("%d kg kaç gramdır?" % kg, "%s g" % num(kg * 1000), ["%d g" % (kg * 100), "%d g" % (kg * 10), "%s g" % num(kg * 1000 + 100)],
                       "1 kg = 1.000 g. %d × 1.000 = <b>%s g</b>." % (kg, num(kg * 1000)))
        if k == 1:
            kg, g = ri(1, 5), ch([100, 200, 250, 300, 400, 500, 600, 750, 800])
            t = kg * 1000 + g
            return mcq("%d kg %d g kaç gramdır?" % (kg, g), "%s g" % num(t), ["%d g" % (kg * 100 + g), "%d g" % (kg + g), "%s g" % num(kg * 1000 + g // 10)],
                       "%d kg = %s g. %s + %d = <b>%s g</b>." % (kg, num(kg * 1000), num(kg * 1000), g, num(t)))
        F = [("yarım kilogram", "500 g"), ("1 kilogramın yarısı", "500 g"), ("1 kilogramın çeyreği", "250 g"), ("çeyrek kilogram", "250 g"), ("bir buçuk kilogram", "1.500 g")]
        a, g = ch(F)
        return mcq("%s kaç gramdır?" % cap(a), g, [x for x in ("500 g", "250 g", "1.500 g", "50 g", "150 g") if x != g],
                   "1 kg = 1.000 g olduğu için %s <b>%s</b>." % (a, g))

    def problem():
        k = ri(0, 2)
        name = K.next()
        if k == 0:
            a, b = ri(1, 3) * 100 + ri(1, 9) * 10, ri(1, 99)
            return mcq("%s, %d cm uzunluğundaki bir kurdeleden %d cm kesti. Kurdelenin kalanı kaç cm?" % (name, a, b), "%d cm" % (a - b),
                       ["%d cm" % (a + b), "%d cm" % (a - b + 10), "%d cm" % (a - b - 10)], "%d − %d = <b>%d cm</b>." % (a, b, a - b))
        if k == 1:
            a, b = ch([250, 500, 750, 300, 400, 600]), ch([200, 250, 350, 450, 500])
            if a + b > 1000:
                return None
            r = 1000 - a - b
            return mcq("%s, 1 kg una ihtiyaç duyuyor. Elinde %d g ve %d g un var. Kaç gram daha una ihtiyacı var?" % (name, a, b), "%d g" % r,
                       ["%d g" % (a + b), "%d g" % (r + 100), "%d g" % (100 - (a + b) // 10) if r != 100 - (a + b) // 10 and 100 - (a + b) // 10 > 0 else "%d g" % (r + 50)],
                       "1 kg = 1.000 g. %d + %d = %d. 1.000 − %d = <b>%d g</b>." % (a, b, a + b, a + b, r))
        m1, m2 = ri(1, 4), ri(10, 90)
        c = ri(20, 90)
        t = m1 * 100 + m2 + c
        return mcq("Bir ip %d m %d cm, diğer ip %d cm. İki ipin toplam uzunluğu kaç santimetredir?" % (m1, m2, c), "%d cm" % t,
                   ["%d cm" % (m1 + m2 + c), "%d cm" % (m1 * 10 + m2 + c), "%d cm" % (t + 100)], "%d m %d cm = %d cm. %d + %d = <b>%d cm</b>." % (m1, m2, m1 * 100 + m2, m1 * 100 + m2, c, t))

    sets = [("Uzunluk birimini seçme", [(uz_birim, 14), (m_cm, 6)]),
            ("Metre, santimetre ve milimetre", [(m_cm, 20)]),
            ("Kütle birimini seçme", [(ku_birim, 14), (kg_g, 6)]),
            ("Kilogram ve gram", [(kg_g, 20)]),
            ("Problemler", [(problem, 14), (m_cm, 6)])]
    return unit("uzunluk-ve-kutle-olcme", "S", "MAT.3.1.15", 9, "Uzunluk ve Kütle Ölçme: mm, cm, m, km, g, kg, ton", "Uzunluk ve Kütle",
                "Uzunluk ve kütle birimleri arasındaki ilişkileri kullanarak birimleri kendi içinde çözümler: milimetre, santimetre, metre, kilometre; gram, kilogram, ton. Kilometre ve tonun dönüşümüne yer verilmez.",
                "3. sınıf uzunluk ve kütle ölçme çalışma kâğıdı: milimetre, santimetre, metre ve kilometre, gram, kilogram ve ton, uygun birimi seçme, metre-santimetre ve kilogram-gram dönüşümleri, problemler. 100 soru ve cevap anahtarı.",
                "1 m = 100 cm, 1 kg = 1.000 g", "1 cm = 10 mm. Uzun yollar km, çok ağır yükler ton.", sets,
                ["Uzunluk birimleri: milimetre (mm), santimetre (cm), metre (m), kilometre (km). 1 cm = 10 mm, 1 m = 100 cm.",
                 "Kütle birimleri: gram (g), kilogram (kg), ton. 1 kg = 1.000 g. Çok ağır şeyler (fil, kamyon) ton ile ölçülür.",
                 "Uygun birimi seçerken ölçülen şeyin büyüklüğünü düşün: kalem cm, sınıf m, iki şehir arası km ile ölçülür."],
                [("3 m 40 cm = ? cm", ["3 m = 300 cm", "300 + 40"], "340 cm"), ("2 kg 500 g = ? g", ["2 kg = 2.000 g", "2.000 + 500"], "2.500 g")],
                [["1 m = 10 cm sanmak", "1 m = 100 cm"], ["1 kg = 100 g sanmak", "1 kg = 1.000 g"],
                 ["Farklı birimleri doğrudan toplamak", "Önce aynı birime çevir"]],
                [("Kilometre ne kadar uzundur?", "1 km = 1.000 m. Yaklaşık 15 dakikalık bir yürüyüş mesafesidir."),
                 ("Ton ile kilogram arasındaki ilişki nedir?", "1 ton = 1.000 kg. 3. sınıfta tonu yalnızca tanıyoruz, dönüşüm yapmıyoruz."),
                 ("Kütle ile ağırlık aynı mıdır?", "Günlük dilde aynı anlamda kullanılır. Matematik derslerinde terazide ölçtüğümüz büyüklüğe kütle denir.")])


# ============================================================ 10. paralarımız
def u10():
    COINS = [5, 10, 25, 50, 100]
    NOTES = [500, 1000, 2000, 5000, 10000, 20000]

    def say():
        k = ri(0, 1)
        if k == 0:
            items = [ch(COINS) for _ in range(ri(3, 5))]
        else:
            items = [ch(NOTES) for _ in range(ri(2, 4))]
        t = sum(items)
        if k == 0 and t % 100 == 0 and R.random() < 0.3:
            return None
        g = para(t)
        alts = [para(t + ch([5, 10, 25, 50]) if k == 0 else t + 500), para(t - items[0]), para(t * 10) if k == 0 else para(t + 1000)]
        return mcq("Resimdeki paraların toplamı ne kadardır?" + para_svg(items), g, alts + [para(t + 100)],
                   "%s = <b>%s</b>." % (" + ".join(para(c) for c in sorted(items, reverse=True)), g))

    def tl_kr():
        k = ri(0, 3)
        if k == 0:
            t, c = ri(1, 9), ch([5, 10, 25, 50, 75, 20, 40, 60, 80, 90])
            return mcq("%s kaç kuruştur?" % para(t * 100 + c), kurus(t * 100 + c), [kurus(t * 10 + c), kurus(t + c), kurus(t * 1000 + c)],
                       "1 TL = 100 kuruş. %d TL = %d kuruş. %d + %d = <b>%s</b>." % (t, t * 100, t * 100, c, kurus(t * 100 + c)))
        if k == 1:
            v = ri(101, 999)
            if v % 100 == 0:
                return None
            return mcq("%s kaç lira kaç kuruştur?" % kurus(v), para(v), [para(v // 10 * 100 + v % 10) if v // 10 < 100 else para(v + 100), para(v + 100), para((v % 100) * 100 + v // 100)],
                       "100 kuruş = 1 TL: <b>%s</b>." % para(v))
        if k == 2:
            c, n = ch([(25, 4), (50, 2), (10, 10), (5, 20), (25, 8), (50, 6), (10, 20), (25, 12), (50, 10)])
            return mcq("%d tane %d kuruş kaç lira eder?" % (n, c), tl(c * n // 100), [tl(c * n // 10), tl(n), tl(c * n // 100 + 1)],
                       "%d × %d = %d kuruş = <b>%s</b>." % (n, c, c * n, tl(c * n // 100)))
        a, b = ch([(10, 5), (20, 10), (20, 5), (50, 10), (50, 5), (100, 50), (100, 20), (100, 10), (200, 100), (200, 50), (200, 20), (50, 20)])
        if a % b:
            return None
        return mcq("Bir %s kaç tane %s eder?" % (tl(a), tl(b)), str(a // b), [str(a // b + 1), str(a // b * 2), str(a - b)] if a - b != a // b else [str(a // b + 1), str(a // b * 2), str(a // b - 1)],
                   "%d ÷ %d = <b>%d</b>." % (a, b, a // b))

    def bozdur():
        t = ch([20, 50, 100, 200])
        opts = {20: [(10, 10), (5, 5, 10), (10, 5, 5)], 50: [(20, 20, 10), (10, 10, 10, 20), (20, 10, 10, 10)], 100: [(50, 20, 20, 10), (50, 50), (20, 20, 20, 20, 20)],
                200: [(100, 50, 50), (100, 100), (50, 50, 50, 50)]}
        good = ch(opts[t])
        bad = []
        for o in sh(sum(opts.values(), [])):
            if sum(o) != t and o not in bad:
                bad.append(o)
        f = lambda xs: " + ".join(tl(x) for x in xs)
        return mcq("Bir %s yerine hangi paralar verilebilir?" % tl(t), f(good), [f(b) for b in bad[:6]],
                   "%s = <b>%s</b>." % (f(good), tl(t)))

    def alisveris():
        k = ri(0, 2)
        name = K.next()
        item = ch(["kitap", "kalem kutusu", "top", "boya seti", "oyuncak araba", "defter", "suluk", "çanta", "yapboz", "kumbara"])
        if k == 0:
            p = ri(3, 18) * 5 + ch([0, 0, 2, 3])
            pay = min(x for x in (20, 50, 100, 200) if x > p)
            return mcq("%s, fiyatı %s olan bir %s aldı. Kasaya %s verdi. Ne kadar para üstü alır?" % (name, tl(p), item, tl(pay)), tl(pay - p),
                       [tl(pay - p + 10), tl(p), tl(pay - p - 1) if pay - p > 1 else tl(pay - p + 1)], "%d − %d = <b>%s</b>." % (pay, p, tl(pay - p)))
        if k == 1:
            a, b = ri(150, 950) // 25 * 25, ri(100, 650) // 25 * 25
            if a % 100 == 0 or b % 100 == 0:
                return None
            return mcq("Bir simit %s, bir ayran %s. İkisinin toplam fiyatı ne kadardır?" % (para(a), para(b)), para(a + b),
                       [para(a + b + 100), para(a + b - 25), para(abs(a - b)) if a != b else para(a + b + 50)],
                       "%s + %s = <b>%s</b>." % (para(a), para(b), para(a + b)))
        p, n = ri(2, 15), ri(2, 6)
        return mcq("Tanesi %s olan defterden %d tane alan %s kaç lira öder?" % (tl(p), n, name), tl(p * n), [tl(p + n), tl(p * n + p), tl(p * (n - 1))],
                   "%d × %d = <b>%s</b>." % (n, p, tl(p * n)))

    sets = [("Paraları sayma", [(say, 20)]),
            ("Lira ve kuruş", [(tl_kr, 20)]),
            ("Para bozdurma ve dönüştürme", [(bozdur, 4), (tl_kr, 16)]),
            ("Alışveriş", [(alisveris, 20)]),
            ("Karışık", [(say, 8), (alisveris, 6), (tl_kr, 6)])]
    return unit("paralarimiz", "S", "MAT.3.1.16", 10, "Paralarımız: Lira ve Kuruş", "Paralarımız",
                "Madenî ve kâğıt paraları değerlerine göre ilişkilendirerek yorumlar; paraları dönüştürür ve paranın değerini anlamını değiştirmeden yeniden ifade eder.",
                "3. sınıf paralarımız çalışma kâğıdı: madenî paralar ve kâğıt paralar, lira ve kuruş dönüşümü, para bozdurma, alışveriş ve para üstü problemleri. 100 soru ve cevap anahtarı.",
                "1 TL = 100 kuruş", "Madenî paralar: 5, 10, 25, 50 kuruş ve 1 TL.", sets,
                ["Paramızın birimi Türk lirasıdır (TL). 1 TL = 100 kuruş.",
                 "Madenî paralar: 5, 10, 25 ve 50 kuruş ile 1 TL. Kâğıt paralar: 5, 10, 20, 50, 100 ve 200 TL.",
                 "Paraları sayarken büyük değerliden başlamak kolaylık sağlar. Para üstü, verilen paradan fiyat çıkarılarak bulunur."],
                [("2 TL 25 kuruş = ? kuruş", ["2 TL = 200 kuruş", "200 + 25"], "225 kuruş"), ("50 TL verdi, 32 TL ödedi", ["50 − 32"], "18 TL para üstü")],
                [["1 TL = 10 kuruş sanmak", "1 TL = 100 kuruş"], ["Para sayısını toplamı sanmak", "Paraların değerlerini topla"],
                 ["Para üstünü bulurken toplamak", "Verilen paradan fiyatı çıkar"]],
                [("Kuruş nedir?", "Liranın yüzde biridir. 100 kuruş bir lira eder."),
                 ("Hangi kâğıt paralar vardır?", "5, 10, 20, 50, 100 ve 200 TL'lik kâğıt paralar vardır."),
                 ("Paraları neden bozdururuz?", "Küçük alışverişlerde para üstü verebilmek ve tam ödeme yapabilmek için.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
