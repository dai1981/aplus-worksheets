# -*- coding: utf-8 -*-
"""Türkiye 9. sınıf (Maarif Modeli, Ortaöğretim Matematik 2026 DÖP)。MAT.9.1〜MAT.9.7。
自前の問題（lise の水準）と、7.〜8. sınıf の問題関数（from_unit）を混ぜる。負の数は「−」。"""
import math
from fractions import Fraction as F
import importlib
import tr_g as G
from tr_g import unit, num, M, NB
from tr_g7 import sn, par, dq, lin, MINUS, gen
from id_smp import kosy as _kosy, kurve as _kurve, figure as _figure

MODS = ["tr_s6b", "tr_s7a", "tr_s7b", "tr_s7c", "tr_s8a", "tr_s8b"]


def setup(rnd):
    for m in MODS:
        importlib.import_module(m).setup(rnd)


def reuse(mod, ufn, name):
    d = getattr(importlib.import_module(mod), ufn)()
    for _, parts in d["sets"]:
        for m, _n in parts:
            if m.__name__ == name:
                return m
    raise KeyError(name)


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


def named(f, n):
    f.__name__ = n
    return f


def kosy(lines=(), pts=(), lo=-6, hi=6, label="koordinat düzlemi"):
    return _kosy(lines=lines, pts=pts, lo=lo, hi=hi, label=label)


def kurve(fs, xr, yr, pts=(), label="grafik"):
    return _kurve(fs, xr, yr, pts=pts, label=label)


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def pw(a, n):
    a = F(a)
    base = sn(a) if (a >= 0 and a.denominator == 1) else "(" + (sn(a) if a.denominator == 1 else "%s/%d" % (sn(a.numerator), a.denominator)) + ")"
    return base + str(n).replace("-", "−").translate(SUP).replace("−", "⁻")


def rt(n):
    """√n sadeleştir → (dış, iç)"""
    o, i = 1, n
    for k in range(int(math.isqrt(n)), 1, -1):
        if n % (k * k) == 0:
            return k, n // (k * k)
    return o, i


def rts(a, n):
    """a√n gösterimi"""
    if n == 1:
        return sn(a)
    if a == 1:
        return "√%d" % n
    if a == -1:
        return MINUS + "√%d" % n
    return "%s√%d" % (sn(a), n)


# ============================================================ 1. üslü ifadeler
def u1():
    us_kural = reuse("tr_s8a", "u2", "carp")
    us_bol = reuse("tr_s8a", "u2", "bol")

    def rasyonel_us():
        b = ch([2, 3, 4, 5, 8, 9, 16, 25, 27, 32, 64, 81, 100, 125])
        roots = [(k, round(b ** (1.0 / k))) for k in (2, 3, 4, 5, 6) if round(b ** (1.0 / k)) ** k == b]
        if not roots:
            return None
        k, r = ch(roots)
        m = ch([1, 2, 3])
        v = r ** m
        s = ch([1, -1])
        val = F(v) if s == 1 else F(1, v)
        e = "%s%d/%d" % ("−" if s < 0 else "", m, k)
        return M("%d<sup>%s</sup> ifadesinin değeri kaçtır?" % (b, e), sn(val), [sn(F(b * m, k)) if (b * m) % k == 0 else sn(v + 1), sn(F(1, val)) if val != 1 else "0", sn(val * r) if r > 1 else sn(val + 2)],
                 "a<sup>m/n</sup> = (ⁿ√a)<sup>m</sup>: %s√%d = %d, %d<sup>%d</sup> = %d%s. Cevap: <b>%s</b>." % ("" if k == 2 else str(k).translate(SUP), b, r, r, m, v, "; negatif üs ters çevirir" if s < 0 else "", sn(val)))

    def sadelestir():
        a = ch([2, 3, 5])
        m, n, p = ri(2, 7), ri(2, 6), ri(1, 4)
        top = m + n
        res = top - p
        kq = ch([0, 1])
        if kq == 0:
            g = pw(a, res)
            return M("%s · %s ÷ %s işleminin sonucu hangisidir?" % (pw(a, m), pw(a, n), pw(a, p)), g, [pw(a, m * n - p), pw(a, top + p), pw(a * a, res)],
                     "Tabanlar aynı: üsler toplanır, bölmede çıkarılır. %d + %d − %d = %d → <b>%s</b>." % (m, n, p, res, g))
        b = ch([x for x in (2, 3, 5) if x != a])
        k = ri(2, 4)
        g = "%s · %s" % (pw(a, m * k), pw(b, n * k))
        return M("(%s · %s)%s ifadesi hangisine eşittir?" % (pw(a, m), pw(b, n), str(k).translate(SUP)), g,
                 ["%s · %s" % (pw(a, m + k), pw(b, n + k)), "%s · %s" % (pw(a, m * k), pw(b, n)), "%s" % pw(a * b, m * n * k)],
                 "Çarpımın kuvveti: her çarpanın üssü %d ile çarpılır → <b>%s</b>." % (k, g))

    def denklem():
        a = ch([2, 3, 5])
        p = ri(1, 4)
        q = ri(1, 3)
        x = ri(-3, 5)
        rhs = p * x + q
        val = F(a) ** rhs
        if abs(rhs) > 8 or rhs == 0 or max(val.numerator, val.denominator) > 1000:
            return None
        lhs = "%d<sup>%s</sup>" % (a, lin(p, "x", q))
        right = sn(val) if val.denominator == 1 else "1/%d" % val.denominator
        return M("%s = %s denkleminde x kaçtır?" % (lhs, right), sn(x), [sn(x + 1), sn(-x) if x else "1", sn(rhs)],
                 "%s = %d<sup>%s</sup> → %s = %s → x = <b>%s</b>." % (right, a, sn(rhs), lin(p, "x", q), sn(rhs), sn(x)))

    sets = [("Üslü ifadelerle işlemler", [(us_kural, 10), (us_bol, 10)]),
            ("Sadeleştirme", [(sadelestir, 20)]),
            ("Rasyonel üsler", [(rasyonel_us, 20)]),
            ("Üslü denklemler", [(denklem, 20)]),
            ("Karışık", [(sadelestir, 7), (rasyonel_us, 7), (denklem, 6)])]
    return unit("uslu-ifadeler", "SY", "MAT.9.1.1", 1, "Üslü İfadeler: Rasyonel Üsler ve Üslü Denklemler", "Üslü İfadeler",
                "Gerçek sayıların üslü gösterimleriyle yapılan işlemlere dair muhakeme yapar; üs kurallarını, rasyonel üsleri ve basit üslü denklemleri kullanır.",
                "9. sınıf üslü ifadeler çalışma kâğıdı: üs kuralları, çarpımın ve bölümün kuvveti, negatif ve rasyonel üsler, tabanları eşitleyerek üslü denklem çözme. 100 soru ve cevap anahtarı.",
                "aᵐ · aⁿ = aᵐ⁺ⁿ", "a^(m/n) = (n. kök a)^m; negatif üs ters çevirir.", sets,
                ["Tabanları aynı üslü ifadelerin çarpımında üsler toplanır, bölümünde çıkarılır: aᵐ · aⁿ = aᵐ⁺ⁿ, aᵐ ÷ aⁿ = aᵐ⁻ⁿ.",
                 "Negatif üs ters çevirir: a⁻ⁿ = 1/aⁿ. Rasyonel üs kök demektir: a<sup>m/n</sup> = (ⁿ√a)<sup>m</sup>.",
                 "Üslü denklemde tabanları eşitler, sonra üsleri eşitleriz: 2<sup>x + 1</sup> = 32 = 2⁵ → x + 1 = 5."],
                [("8<sup>2/3</sup>", ["³√8 = 2", "2² = 4"], "4"), ("3<sup>2x − 1</sup> = 27", ["27 = 3³", "2x − 1 = 3"], "x = 2")],
                [["aᵐ · aⁿ için üsleri çarpmak", "Üsler toplanır"], ["Negatif üssü negatif sayı sanmak", "2⁻³ = 1/8, −8 değil"],
                 ["Rasyonel üste pay ile paydayı karıştırmak", "Payda kökün derecesi"]],
                [("a⁰ neden 1’dir?", "aⁿ ÷ aⁿ = a⁰ ve aynı zamanda 1’dir (a ≠ 0)."),
                 ("Negatif tabanın kesirli üssü tanımlı mı?", "Çift dereceli kök negatif sayıda gerçek sayı vermez; bu durumlar dikkatle ele alınır."),
                 ("Üslü denklemde tabanlar eşitlenemezse?", "Bu yıl tabanları eşitlenebilen denklemler çözülür; diğerleri logaritma ile çözülür.")])


# ============================================================ 2. köklü ifadeler
def u2():
    def sadelestir():
        a = ri(2, 9)
        b = ch([2, 3, 5, 6, 7])
        n = a * a * b
        return M("√%d ifadesinin en sade hâli hangisidir?" % n, rts(a, b), [rts(b, a) if b != a and a not in (4, 9) else "√%d" % (a * b), rts(a * a, b), rts(a + 1, b)],
                 "%d = %d · %d → √%d = <b>%s</b>." % (n, a * a, b, n, rts(a, b)))

    def topla():
        b = ch([2, 3, 5, 6, 7])
        p, q = ri(1, 5), ri(1, 5)
        x, y = p * p * b, q * q * b
        if x == y:
            return None
        op = ch("+-")
        r = p + q if op == "+" else p - q
        return M("√%d %s √%d işleminin sonucu hangisidir?" % (x, "+" if op == "+" else "−", y), rts(r, b) if r else "0",
                 ["√%d" % (x + y if op == "+" else abs(x - y)), rts(r + 1, b), rts(p * q, b)],
                 "√%d = %s, √%d = %s → <b>%s</b>." % (x, rts(p, b), y, rts(q, b), rts(r, b) if r else "0"))

    def carp():
        a, b = ri(2, 6), ri(2, 6)
        m, n = ch([2, 3, 5, 6]), ch([2, 3, 5, 6])
        prod = m * n
        o, i = rt(prod)
        coef = a * b * o
        g = rts(coef, i) if i > 1 else sn(coef)
        return M("%s · %s işleminin sonucu hangisidir?" % (rts(a, m), rts(b, n)), g, [rts(a * b, m + n), rts(a + b, prod), rts(a * b, prod) if (o > 1) else sn(coef + 1)],
                 "%d · %d = %d, √%d · √%d = √%d = %s → <b>%s</b>." % (a, b, a * b, m, n, prod, rts(o, i) if i > 1 else str(o), g))

    def payda():
        a = ri(1, 9)
        b = ch([2, 3, 5, 6, 7])
        k = ri(1, 4)
        num_ = a * b * k
        g = rts(F(num_, b), b) if True else ""
        v = F(num_, b)
        return M("%d/√%d ifadesinin paydası rasyonel yapılınca hangisi elde edilir?" % (num_, b), rts(v, b),
                 [rts(num_, b), "%d" % (num_ // b) if num_ % b == 0 else rts(F(num_, b * b), b), rts(v * 2, b)],
                 "Pay ve payda √%d ile çarpılır: %d√%d/%d = <b>%s</b>." % (b, num_, b, b, rts(v, b)))

    def arasinda():
        n = ri(2, 150)
        r = math.isqrt(n)
        if r * r == n:
            return None
        k = ch([1, 2])
        if k == 1:
            return M("√%d hangi iki ardışık tam sayı arasındadır?" % n, "%d ile %d" % (r, r + 1), ["%d ile %d" % (r - 1, r), "%d ile %d" % (r + 1, r + 2), "%d ile %d" % (n // 2, n // 2 + 1)],
                     "%d² = %d &lt; %d &lt; %d = %d² → <b>%d ile %d</b>." % (r, r * r, n, (r + 1) ** 2, r + 1, r, r + 1))
        a, b = ri(2, 6), ch([2, 3, 5, 7])
        c = a * a * b
        rr = math.isqrt(c)
        return M("%s sayısı hangi iki ardışık tam sayı arasındadır?" % rts(a, b), "%d ile %d" % (rr, rr + 1), ["%d ile %d" % (rr - 1, rr), "%d ile %d" % (rr + 1, rr + 2), "%d ile %d" % (a * b - 1, a * b) if a * b - 1 != rr else "%d ile %d" % (a, a + 1)],
                 "%s = √%d; %d² = %d &lt; %d &lt; %d → <b>%d ile %d</b>." % (rts(a, b), c, rr, rr * rr, c, (rr + 1) ** 2, rr, rr + 1))

    sets = [("Sadeleştirme", [(sadelestir, 20)]),
            ("Toplama ve çıkarma", [(topla, 20)]),
            ("Çarpma", [(carp, 20)]),
            ("Paydayı rasyonel yapma", [(payda, 20)]),
            ("Köklü sayıların yeri", [(arasinda, 20)])]
    return unit("koklu-ifadeler", "SY", "MAT.9.1.1", 2, "Köklü İfadeler: Sadeleştirme ve İşlemler", "Köklü İfadeler",
                "Gerçek sayıların köklü gösterimleriyle yapılan işlemlere dair muhakeme yapar; köklü ifadeleri sadeleştirir, toplar, çarpar ve paydayı rasyonel yapar.",
                "9. sınıf köklü ifadeler çalışma kâğıdı: kökün dışına çıkarma, benzer köklüleri toplama ve çıkarma, köklü ifadelerle çarpma, paydayı rasyonel yapma, köklü sayıyı iki tam sayı arasında gösterme. 100 soru ve cevap anahtarı.",
                "√(a² · b) = a√b", "Yalnızca kök içleri aynı olanlar toplanır.", sets,
                ["Kök içindeki sayının tam kare çarpanı kökün dışına çıkar: √72 = √(36 · 2) = 6√2.",
                 "Kök içleri aynı olan ifadeler toplanır ya da çıkarılır: 3√2 + 5√2 = 8√2. √a · √b = √(ab).",
                 "Paydada kök varsa pay ve payda aynı kökle çarpılır: 6/√3 = 6√3/3 = 2√3."],
                [("√50 + √8", ["5√2 + 2√2"], "7√2"), ("10/√5", ["10√5/5"], "2√5")],
                [["√9 + √16 = √25 sanmak", "3 + 4 = 7; kökler toplanmaz"], ["Sadeleştirmede kare olmayan çarpanı dışarı çıkarmak", "Yalnızca tam kare çarpan çıkar"],
                 ["Paydayı rasyonel yaparken yalnızca paydayı çarpmak", "Pay da aynı sayıyla çarpılır"]],
                [("Kök neden sadeleştirilir?", "İşlemleri kolaylaştırmak ve benzer kökleri görmek için."),
                 ("√a · √a neye eşittir?", "a’ya eşittir (a ≥ 0)."),
                 ("Paydayı rasyonel yapmak zorunlu mu?", "Matematikte sade yazım kuralıdır; sonuçları karşılaştırmayı kolaylaştırır.")])


# ============================================================ 3. aralıklar ve küme işlemleri
def iv(a, b, la, rb):
    return "%s%s, %s%s" % ("[" if la else "(", "−∞" if a is None else sn(a), "∞" if b is None else sn(b), "]" if rb else ")")


def u3():
    def gosterim():
        a, b = ri(-6, 4), ri(-3, 8)
        if a >= b:
            return None
        la, rb = ch([True, False]), ch([True, False])
        s = "%s %s x %s %s" % (sn(a), "≤" if la else "&lt;", "≤" if rb else "&lt;", sn(b))
        g = iv(a, b, la, rb)
        return M("{x ∈ ℝ | %s} kümesinin aralık gösterimi hangisidir?" % s, g, [iv(a, b, not la, rb), iv(a, b, la, not rb), iv(a, b, not la, not rb)],
                 "≤ kapalı uç [ ], &lt; açık uç ( ) ile gösterilir: <b>%s</b>." % g)

    def kesisim():
        a, b = ri(-6, 2), ri(-2, 6)
        c, d = ri(-4, 4), ri(0, 9)
        if not (a < b and c < d) or max(a, c) >= min(b, d):
            return None
        op = ch(["∩", "∪"])
        if op == "∩":
            lo, hi = max(a, c), min(b, d)
            left_closed = (lo == a) and not (lo == c)
            right_closed = (hi == d) and not (hi == b)
            g = iv(lo, hi, left_closed, right_closed)
            w = [iv(min(a, c), max(b, d), a <= c, d >= b), iv(lo, hi, not left_closed, right_closed), iv(lo, hi, left_closed, not right_closed)]
        else:
            lo, hi = min(a, c), max(b, d)
            left_closed = lo == a
            right_closed = hi == d
            g = iv(lo, hi, left_closed, right_closed)
            ll, hh = max(a, c), min(b, d)
            w = [iv(ll, hh, ll == a and ll != c, hh == d and hh != b), iv(lo, hi, not left_closed, right_closed), iv(lo, hi, left_closed, not right_closed)]
        return M("A = [%s, %s) ve B = (%s, %s] ise A %s B hangisidir?" % (sn(a), sn(b), sn(c), sn(d), op), g, w,
                 "Sayı doğrusunda iki aralığı çizeriz; %s için %s alırız: <b>%s</b>." % (op, "ortak kısmı" if op == "∩" else "ikisinin birleşimini", g))

    def tam_say():
        a, b = ri(-7, 3), ri(-2, 9)
        if a >= b:
            return None
        la, rb = ch([True, False]), ch([True, False])
        cnt = (b - a + 1) - (0 if la else 1) - (0 if rb else 1)
        return M("%s aralığında kaç tam sayı vardır?" % iv(a, b, la, rb), num(cnt), [num(cnt + 1), num(cnt - 1) if cnt > 1 else num(cnt + 2), num(b - a)] if b - a not in (cnt, cnt + 1, cnt - 1) else [num(cnt + 1), num(cnt + 2), num(cnt - 1) if cnt > 1 else num(cnt + 3)],
                 "%s ile %s arasındaki tam sayılar sayılır; açık uç dâhil edilmez: <b>%d</b>." % (sn(a), sn(b), cnt))

    def mutlak():
        c, r = ri(-4, 5), ri(1, 6)
        k = ch(["≤", "&lt;"])
        g = iv(c - r, c + r, k == "≤", k == "≤")
        inner = "x" if c == 0 else ("x − %d" % c if c > 0 else "x + %d" % (-c))
        return M("|%s| %s %d koşulunu sağlayan x değerleri hangi aralıktadır?" % (inner, k, r), g, [iv(c - r, c + r, k != "≤", k != "≤"), iv(-r, r, k == "≤", k == "≤") if c else iv(c - r - 1, c + r + 1, k == "≤", k == "≤"), iv(c, c + r, k == "≤", k == "≤")],
                 "x’in %s sayısına uzaklığı en fazla %d (%s): %s − %d ile %s + %d arası → <b>%s</b>." % (sn(c), r, "eşit olabilir" if k == "≤" else "eşit değil", sn(c), r, sn(c), r, g))

    sets = [("Aralık gösterimi", [(gosterim, 20)]),
            ("Kesişim ve birleşim", [(kesisim, 20)]),
            ("Aralıktaki tam sayılar", [(tam_say, 20)]),
            ("Mutlak değer ve aralık", [(mutlak, 20)]),
            ("Karışık", [(gosterim, 6), (kesisim, 7), (mutlak, 7)])]
    return unit("gercek-sayi-araliklari", "SY", "MAT.9.1.2", 3, "Gerçek Sayı Aralıkları ve Küme İşlemleri", "Sayı Aralıkları",
                "Gerçek sayı aralıklarının gösteriminde ve aralıklarla ilgili işlemlerde küme sembol ve işlemlerinden yararlanır; aralıkların kesişimini ve birleşimini bulur.",
                "9. sınıf gerçek sayı aralıkları çalışma kâğıdı: açık, kapalı ve yarı açık aralık gösterimi, aralıkların kesişimi ve birleşimi, aralıktaki tam sayılar, mutlak değerle aralık. 100 soru ve cevap anahtarı.",
                "[ ] dâhil, ( ) dâhil değil", "Kesişim ortak kısım, birleşim hepsi.", sets,
                ["a ≤ x ≤ b kapalı aralık [a, b], a &lt; x &lt; b açık aralık (a, b) ile gösterilir. Sonsuz uçlar her zaman açıktır.",
                 "A ∩ B iki aralığın ortak kısmı, A ∪ B ikisinin birleşimidir. Sayı doğrusunda çizmek kolaylık sağlar.",
                 "|x − c| ≤ r, x’in c sayısına uzaklığının r’den fazla olmadığını söyler: [c − r, c + r]."],
                [("[−2, 5) ∩ (1, 7]", ["Ortak kısım 1 ile 5 arası"], "(1, 5)"), ("|x − 3| &lt; 2", ["3 − 2 ile 3 + 2"], "(1, 5)")],
                [["Açık ucu dâhil etmek", "( ) uçtaki sayıyı içermez"], ["Kesişim ile birleşimi karıştırmak", "∩ ortak, ∪ birleşim"],
                 ["Sonsuzu kapalı yazmak", "∞ her zaman açık uçtur"]],
                [("Aralık ile küme farkı nedir?", "Aralık, iki sayı arasındaki bütün gerçek sayılardan oluşan bir kümedir."),
                 ("Boş kesişim nasıl yazılır?", "∅ ile gösterilir."),
                 ("Mutlak değer neden aralıkla ilgilidir?", "|x − c|, x ile c arasındaki uzaklıktır.")])


# ============================================================ 4. sayı kümeleri
NUMS = [("−5", "ℤ"), ("7", "ℕ"), ("0", "ℕ"), ("3/4", "ℚ"), ("−2,5", "ℚ"), ("0,333…", "ℚ"), ("√2", "ℝ"), ("π", "ℝ"), ("√16", "ℕ"), ("−√9", "ℤ"), ("√5", "ℝ"), ("1,4142…(devirsiz)", "ℝ"), ("−12", "ℤ"), ("22/7", "ℚ"), ("√0,25", "ℚ")]
SMALL = {"ℕ": "doğal sayılar (ℕ)", "ℤ": "tam sayılar (ℤ)", "ℚ": "rasyonel sayılar (ℚ)", "ℝ": "irrasyonel sayılar (ℝ − ℚ)"}


def u4():
    def en_kucuk():
        x, k = ch(NUMS)
        g = SMALL[k]
        return M("%s sayısının ait olduğu en küçük sayı kümesi hangisidir?" % x, cap(g), [cap(v) for v in SMALL.values() if v != g],
                 "ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ. %s → <b>%s</b>." % (x, g))

    def kapali():
        S = [("ℕ", "çıkarma", "Kapalı değildir", "3 − 5 = −2 ∉ ℕ"), ("ℕ", "toplama", "Kapalıdır", "İki doğal sayının toplamı doğal sayıdır"),
             ("ℤ", "çarpma", "Kapalıdır", "İki tam sayının çarpımı tam sayıdır"), ("ℤ", "bölme", "Kapalı değildir", "1 ÷ 2 = 1/2 ∉ ℤ"),
             ("ℚ", "toplama", "Kapalıdır", "İki rasyonelin toplamı rasyoneldir"), ("ℚ − {0}", "bölme", "Kapalıdır", "Sıfırdan farklı iki rasyonelin bölümü rasyoneldir"),
             ("ℝ − ℚ (irrasyoneller)", "çarpma", "Kapalı değildir", "√2 · √2 = 2 rasyoneldir"), ("ℝ − ℚ (irrasyoneller)", "toplama", "Kapalı değildir", "√2 + (−√2) = 0 rasyoneldir"),
             ("ℤ", "çıkarma", "Kapalıdır", "İki tam sayının farkı tam sayıdır"), ("ℕ", "çarpma", "Kapalıdır", "İki doğal sayının çarpımı doğal sayıdır")]
        s, op, g, why = ch(S)
        return M("%s kümesi %s işlemine göre kapalı mıdır?" % (s, op), g, ["Kapalıdır" if g != "Kapalıdır" else "Kapalı değildir", "Yalnızca pozitifler için kapalıdır", "Bilinemez"],
                 "%s. Cevap: <b>%s</b>." % (why, g))

    def dogru():
        S = [("Her tam sayı bir rasyonel sayıdır.", "Doğru"), ("Her rasyonel sayı bir tam sayıdır.", "Yanlış"), ("İki irrasyonel sayının toplamı her zaman irrasyoneldir.", "Yanlış"),
             ("Bir rasyonel ile bir irrasyonelin toplamı irrasyoneldir.", "Doğru"), ("Devirli ondalık sayılar rasyoneldir.", "Doğru"), ("π bir rasyonel sayıdır.", "Yanlış"),
             ("0 bir doğal sayıdır.", "Doğru"), ("Her gerçek sayı ya rasyonel ya irrasyoneldir.", "Doğru"), ("√9 irrasyoneldir.", "Yanlış"),
             ("Sıfırdan farklı bir rasyonel ile bir irrasyonelin çarpımı irrasyoneldir.", "Doğru")]
        t, g = ch(S)
        return M("“%s” ifadesi doğru mu, yanlış mı?" % t, g, ["Yanlış" if g == "Doğru" else "Doğru", "Bazen doğru", "Bilinemez"], "Cevap: <b>%s</b>." % g)

    def devirli():
        a, b = ri(1, 9), ri(0, 9)
        k = ch([1, 2])
        if k == 1:
            v = F(a, 9)
            return M("0,%s… (%d tekrar ediyor) sayısının rasyonel gösterimi hangisidir?" % (str(a) * 3, a), sn(v), [sn(F(a, 10)), sn(F(a, 99)), sn(F(a + 1, 9))],
                     "x = 0,%s… → 10x − x = %d → x = %d/9 = <b>%s</b>." % (str(a) * 3, a, a, sn(v)))
        n = 10 * a + b
        if a == b:
            return None
        v = F(n, 99)
        return M("0,%02d%02d… (%02d tekrar ediyor) sayısının rasyonel gösterimi hangisidir?" % (n, n, n), sn(v), [sn(F(n, 100)), sn(F(n, 90)), sn(F(n, 9))],
                 "x = 0,%02d%02d… → 100x − x = %d → x = %d/99 = <b>%s</b>." % (n, n, n, n, sn(v)))

    def islem():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(2, 12), ri(2, 12)
            p = a * b
            r = math.isqrt(p)
            g = "Rasyonel" if r * r == p else "İrrasyonel"
            return M("√%d · √%d sayısı rasyonel mi, irrasyonel mi?" % (a, b), g, ["İrrasyonel" if g == "Rasyonel" else "Rasyonel", "Tam sayı değildir, rasyonel de değildir", "Tanımsızdır"],
                     "√%d · √%d = √%d%s. Cevap: <b>%s</b>." % (a, b, p, " = %d" % r if r * r == p else "", g.lower()))
        if k == 1:
            a = ri(2, 30)
            r = math.isqrt(a)
            q = ri(1, 9)
            g = "Rasyonel" if r * r == a else "İrrasyonel"
            return M("%d + √%d sayısı rasyonel mi, irrasyonel mi?" % (q, a), g, ["İrrasyonel" if g == "Rasyonel" else "Rasyonel", "Doğal sayı değildir, gerçek sayı da değildir", "Tanımsızdır"],
                     "√%d %s; rasyonel ile %s toplamı %s. Cevap: <b>%s</b>." % (a, "= %d rasyoneldir" % r if r * r == a else "irrasyoneldir", "rasyonelin" if r * r == a else "irrasyonelin", g.lower(), g.lower()))
        a, b = ri(2, 20), ri(2, 20)
        ra, rb = math.isqrt(a), math.isqrt(b)
        if a == b:
            return None
        v = F(a, b)
        sq = math.isqrt(v.numerator) ** 2 == v.numerator and math.isqrt(v.denominator) ** 2 == v.denominator
        g = "Rasyonel" if sq else "İrrasyonel"
        return M("√%d ÷ √%d sayısı rasyonel mi, irrasyonel mi?" % (a, b), g, ["İrrasyonel" if g == "Rasyonel" else "Rasyonel", "Tam sayıdır ama rasyonel değildir", "Tanımsızdır"],
                 "√%d ÷ √%d = √(%s). Cevap: <b>%s</b>." % (a, b, sn(v), g.lower()))

    sets = [("En küçük sayı kümesi", [(en_kucuk, 15), (dogru, 5)]),
            ("İşlemlere göre kapalılık", [(kapali, 10), (dogru, 5), (islem, 5)]),
            ("Devirli ondalıklar", [(devirli, 20)]),
            ("Rasyonel mi, irrasyonel mi?", [(islem, 20)]),
            ("Karışık", [(devirli, 10), (islem, 10)])]
    return unit("sayi-kumeleri", "SY", "MAT.9.1.3", 4, "Sayı Kümeleri: Doğal, Tam, Rasyonel ve Gerçek Sayılar", "Sayı Kümeleri",
                "Farklı sayı kümelerinin (ℕ, ℤ, ℚ, ℝ) özellikleri hakkında muhakeme yapar; sayıların ait olduğu kümeleri, işlemlere göre kapalılığı ve devirli ondalıkların rasyonel gösterimini inceler.",
                "9. sınıf sayı kümeleri çalışma kâğıdı: ℕ, ℤ, ℚ ve ℝ, bir sayının ait olduğu en küçük küme, işlemlere göre kapalılık, devirli ondalığı kesre çevirme, rasyonel mi irrasyonel mi. 100 soru ve cevap anahtarı.",
                "ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ", "Devirli ondalıklar rasyonel, π ve √2 irrasyoneldir.", sets,
                ["ℕ doğal sayılar, ℤ tam sayılar, ℚ rasyonel sayılar (a/b, b ≠ 0), ℝ gerçek sayılardır. ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ.",
                 "Bir kümedeki iki sayıya işlem uygulandığında sonuç yine kümedeyse küme o işleme göre kapalıdır.",
                 "Devirli ondalıklar rasyoneldir: 0,777… = 7/9, 0,1212… = 12/99. Devirsiz ve sonsuz ondalıklar irrasyoneldir."],
                [("0,555…", ["10x − x = 5"], "5/9"), ("ℕ çıkarmaya göre", ["2 − 5 = −3 ∉ ℕ"], "Kapalı değil")],
                [["√16’yı irrasyonel sanmak", "√16 = 4"], ["3,14’ü π’ye eşit sanmak", "3,14 yaklaşık değerdir"],
                 ["İki irrasyonelin toplamını her zaman irrasyonel sanmak", "√2 + (−√2) = 0"]],
                [("Neden sayı kümelerini genişletiriz?", "Çıkarma için ℤ, bölme için ℚ, kök için ℝ gibi; işlemleri her zaman yapabilmek için."),
                 ("Sıfır hangi kümelerdedir?", "ℕ, ℤ, ℚ ve ℝ kümelerindedir."),
                 ("Her kesir rasyonel midir?", "Payı ve paydası tam sayı olan (payda ≠ 0) kesirler rasyoneldir.")])


def cap(s):
    return G.cap(s)


UNITS = [u1, u2, u3, u4]
