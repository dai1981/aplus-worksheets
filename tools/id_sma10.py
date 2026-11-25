# -*- coding: utf-8 -*-
"""Indonesia / Matematika / Kelas 10 (SMA, Fase E)。python3 tools/id_smp.py 10 [番号…]"""
import math
from fractions import Fraction as Fr
import id_smp as S
from id_smp import (ri, ch, nz, sh, num, sn, par, pd, dz, fq, expr, lin, sup, pw, M, MN, MD, rp, NB, MINUS,
                    kosy, kurve, figure, tab, unit, fig, wrap, text, line, INK, BLUE, RED, FILL, GREEN)


def LOG(b, x):
    return "<sup>%s</sup>log%s%s" % (b, NB, x)


def P(e):
    return "<sup>%s</sup>" % e


# nilai trigonometri sudut istimewa (teks)
SIN = {0: "0", 30: "½", 45: "½√2", 60: "½√3", 90: "1"}
COS = {0: "1", 30: "½√3", 45: "½√2", 60: "½", 90: "0"}
TAN = {0: "0", 30: "⅓√3", 45: "1", 60: "√3"}


def neg(s):
    return s if s == "0" else (s[1:] if s.startswith(MINUS) else MINUS + s)


def surd(a, b):
    """a√b disederhanakan"""
    k = 1
    for f in range(int(math.isqrt(b)), 1, -1):
        if b % (f * f) == 0:
            k, b = f, b // (f * f)
            break
    a = a * k
    if b == 1:
        return sn(a)
    return ("" if a == 1 else (MINUS if a == -1 else sn(a))) + "√%d" % b


# ============================================================ 1. eksponen
def u1():
    def sifat():
        b = ch([2, 3, 5])
        m, n, p = nz(-5, 7), nz(-5, 7), nz(-4, 6)
        e = m + n - p
        if abs(e) > 4 or e == 0 or b ** abs(e) > 700:
            return None
        v = Fr(b) ** e
        q = "(%d%s × %d%s) : %d%s" % (b, sup(m), b, sup(n), b, sup(p))
        return M("Nilai dari %s adalah …" % q, fq(v), [fq(Fr(b) ** (m * n - p)) if abs(m * n - p) <= 4 else fq(v * b), fq(Fr(b) ** (-e)), fq(Fr(b) ** (m + n + p)) if abs(m + n + p) <= 4 else fq(v / b), sn(b * e)],
                 "Pangkat dijumlahkan saat dikali dan dikurangkan saat dibagi: %s + %s − %s = %s. %d%s = %s." % (sn(m), par(n), par(p), sn(e), b, sup(e), fq(v)))

    def pecahan():
        b = ch([2, 3, 4, 5, 6, 7, 10])
        n = ch([2, 3, 4, 5]) if b == 2 else (ch([2, 3, 4]) if b == 3 else ch([2, 3]))
        m = ch([1, 2, 3, -1, -2, -3])
        base = b ** n
        if base > 1000 or abs(m) > n + 1 or math.gcd(abs(m), n) != 1:
            return None
        v = Fr(b) ** m
        return M("Nilai dari %d%s adalah …" % (base, P("%s/%d" % (sn(m), n))), fq(v), [fq(Fr(base * m, n)) if (base * m) % n == 0 and Fr(base * m, n) != v else fq(v * b), fq(1 / v), fq(Fr(b) ** (m + 1)) if Fr(b) ** (m + 1) != 1 / v else sn(b * n)],
                 "%d = %d%s, jadi %d%s = %d%s = %s." % (base, b, sup(n), base, P("%s/%d" % (sn(m), n)), b, sup(m), fq(v)))

    def aljabar():
        a, b = ri(2, 7), ri(2, 7)
        c, d = ri(1, 4), ri(1, 4)
        k = ri(0, 1)
        if k == 0:
            n = ri(2, 3)
            co = 2 ** n if n else 1
            q = "(2a%s b%s)%s" % (sup(c), sup(-d), sup(n))
            num_ = "%da%s" % (co, sup(c * n))
            den = "b%s" % sup(d * n)
            ans = S.fr(num_, den)
            return M("Bentuk sederhana dari %s dengan pangkat positif adalah …" % q, ans, [S.fr("%da%s" % (2 * n, sup(c * n)), den), "%sb%s" % (num_, sup(d * n)), S.fr("%da%s" % (co, sup(c + n)), "b%s" % sup(d + n))],
                     "Setiap faktor dipangkatkan %d, lalu b%s = 1/b%s: %s." % (n, sup(-d * n), sup(d * n), ans))
        if a == c:
            return None
        e1, e2 = a - c, -(d + b)
        X = lambda v, e: v if e == 1 else v + sup(e)
        q = S.fr("%s %s" % (X("x", a), X("y", -d)), "%s %s" % (X("x", c), X("y", b)))
        top = X("x", e1) if e1 > 0 else "1"
        bot = "y%s" % sup(-e2) + ("" if e1 > 0 else " x%s" % sup(-e1) if e1 != -1 else " x")
        ans = S.fr(top, bot)
        return M("Bentuk sederhana dari %s adalah …" % q, ans, [S.fr(top, "y%s" % sup(b - d)) if b != d else S.fr(top, "y"), "%s %s" % (X("x", e1), X("y", -e2)), S.fr(X("x", a + c), X("y", -e2))],
                 "Kurangkan pangkat untuk basis yang sama: x%s dan y%s, lalu tulis dengan pangkat positif: %s." % (sup(e1), sup(e2), ans))

    def persamaan():
        k = ri(0, 3)
        if k == 0:
            b = ch([2, 3, 5])
            n = ri(2, 5 if b == 2 else 4)
            c = ri(-2, 3)
            x = n - c
            return MN("Penyelesaian dari %d%s = %s adalah x = …" % (b, P(lin(1, c)), num(b ** n)), x, [n, n + c, x + 1], "%s = %d%s, jadi x %s %d = %d dan x = %s." % (num(b ** n), b, sup(n), "+" if c >= 0 else "−", abs(c), n, sn(x)))
        if k == 1:
            base, p, q = ch([(4, 2, 1), (8, 3, 1), (9, 2, 1), (27, 3, 1), (16, 4, 1), (25, 2, 1)])
            b = {4: 2, 8: 2, 9: 3, 27: 3, 16: 2, 25: 5}[base]
            x = ri(-3, 6)
            c = ri(1, 3)
            # base^(x) = b^(?)
            rhs = p * x
            rhs_c = c
            q2 = "%d%s = %d%s" % (base, P("x"), b, P(lin(1, rhs - x) if rhs - x else "x")) if False else None
            a1, a2 = ri(1, 3), ri(-4, 4)
            # base^(a1 x + a2) = b^(m x + n) → p(a1x+a2) = m x + n
            m = ri(1, 6)
            if m == p * a1:
                return None
            n = p * (a1 * x + a2) - m * x
            return MN("Penyelesaian dari %d%s = %d%s adalah x = …" % (base, P(lin(a1, a2)), b, P(lin(m, n))), x, [-x, x + 1, Fr(n - a2, a1 - m) if a1 != m and Fr(n - a2, a1 - m).denominator == 1 and Fr(n - a2, a1 - m) != x else x - 2],
                      "%d = %d%s, jadi %d(%s) = %s → x = %s." % (base, b, sup(p), p, lin(a1, a2), lin(m, n), sn(x)))
        if k == 2:
            n = ri(1, 5)
            b = ch([2, 3])
            return MN("Penyelesaian dari (1/%d)%s = %s adalah x = …" % (b, P("x"), num(b ** n)), -n, [n, Fr(1, n), -n - 1], "(1/%d)%s = %d%s, jadi −x = %d dan x = %s." % (b, sup("x"), b, P("−x"), n, sn(-n)))
        b = ch([2, 3, 5])
        x = ri(0, 4)
        v = b ** x
        return MN("Diketahui f(x) = %d%s. Nilai f(%d) + f(0) adalah …" % (b, P("x"), x), v + 1, [v, b * x + 1, v + b], "f(%d) = %s dan f(0) = 1. Jumlahnya %s." % (x, num(v), num(v + 1)))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            n0, t, h = ri(2, 9) * 100, ch([15, 20, 30]), ri(2, 4)
            k_ = 60 * h // t
            return MN("Sebuah koloni bakteri berjumlah %d dan menjadi dua kali lipat setiap %d menit. Banyak bakteri setelah %d jam …" % (n0, t, h), n0 * 2 ** k_,
                      [n0 * 2 * k_, n0 * 2 ** (k_ - 1), n0 * 2 ** h], "%d jam = %d kali %d menit. %d × 2%s = %s." % (h, k_, t, n0, sup(k_), num(n0 * 2 ** k_)), unit="bakteri")
        if k == 1:
            m0, w, n = ch([80, 160, 320, 640, 400, 200]), ch([2, 3, 4, 5, 6]), ri(2, 4)
            v = Fr(m0, 2 ** n)
            return MD("Zat radioaktif bermassa %d gram memiliki waktu paruh %d jam. Massa yang tersisa setelah %d jam …" % (m0, w, w * n), v, [Fr(m0, 2 * n), Fr(m0, 2 ** (n - 1)), m0 - Fr(m0, 2 ** n)],
                      "Ada %d kali waktu paruh: %d × (½)%s = %s gram." % (n, m0, sup(n), dz(v)), unit="gram")
        p0, r, n = ri(2, 9) * 1000, ch([2, 3]), ri(2, 4)
        return MN("Banyak pengguna sebuah aplikasi %s orang dan menjadi %d kali lipat setiap bulan. Banyak pengguna setelah %d bulan …" % (num(p0), r, n), p0 * r ** n,
                  [p0 * r * n, p0 * r ** (n - 1), p0 * r ** (n + 1)], "%s × %d%s = %s orang." % (num(p0), r, sup(n), num(p0 * r ** n)), unit="orang")

    sets = [("Sifat-sifat bilangan berpangkat", [(sifat, 20)]),
            ("Pangkat pecahan", [(pecahan, 20)]),
            ("Bentuk aljabar berpangkat", [(aljabar, 20)]),
            ("Persamaan eksponen", [(persamaan, 20)]),
            ("Pertumbuhan dan peluruhan", [(cerita, 14), (persamaan, 6)])]
    return unit("eksponen", "B", 1, "Eksponen: Sifat, Pangkat Pecahan, dan Persamaan Eksponen", "Eksponen",
                "Peserta didik menggeneralisasi sifat-sifat operasi bilangan berpangkat (eksponen), menyelesaikan persamaan eksponen sederhana, dan memodelkan pertumbuhan serta peluruhan eksponensial.",
                "Latihan eksponen kelas 10 SMA: sifat-sifat bilangan berpangkat, pangkat nol, negatif, dan pecahan, bentuk aljabar berpangkat, persamaan eksponen, serta pertumbuhan dan peluruhan. 100 soal dengan kunci jawaban.",
                "aᵐ × aⁿ = aᵐ⁺ⁿ dan a^(m/n) = ⁿ√aᵐ", "a⁻ⁿ = 1/aⁿ dan a⁰ = 1 (a ≠ 0).", sets,
                ["Sifat eksponen: aᵐ × aⁿ = aᵐ⁺ⁿ, aᵐ : aⁿ = aᵐ⁻ⁿ, (aᵐ)ⁿ = aᵐⁿ, (ab)ⁿ = aⁿbⁿ, a⁰ = 1, dan a⁻ⁿ = 1/aⁿ.",
                 "Pangkat pecahan: a<sup>m/n</sup> adalah akar pangkat n dari aᵐ. Contoh 8<sup>2/3</sup> = (∛8)² = 4.",
                 "Persamaan eksponen: samakan basisnya dulu, lalu samakan pangkatnya. Jika aᶠ⁽ˣ⁾ = aᵍ⁽ˣ⁾, maka f(x) = g(x)."],
                [("Selesaikan 4<sup>x + 1</sup> = 32.", ["2<sup>2x + 2</sup> = 2⁵", "2x + 2 = 5"], "x = 3/2"),
                 ("Nilai 27<sup>−2/3</sup>?", ["27 = 3³", "3⁻² = 1/9"], "1/9")],
                [["2³ × 2⁴ = 4⁷", "Basis tetap 2: 2⁷"],
                 ["5⁻² = −25", "5⁻² = 1/5² = 1/25"],
                 ["4<sup>x</sup> = 8 → x = 2", "Samakan basis: 2<sup>2x</sup> = 2³, x = 3/2"]],
                [("Mengapa a⁰ = 1?", "Karena aⁿ : aⁿ = aⁿ⁻ⁿ = a⁰, dan bilangan yang dibagi dirinya sendiri hasilnya 1."),
                 ("Bagaimana menyelesaikan persamaan eksponen yang basisnya berbeda?", "Ubah kedua basis menjadi pangkat dari bilangan yang sama, misalnya 4 = 2² dan 8 = 2³."),
                 ("Di mana eksponen dipakai?", "Pada pertumbuhan bakteri, bunga majemuk, peluruhan zat radioaktif, dan penyebaran informasi.")])


# ============================================================ 2. logaritma
def u2():
    def definisi():
        b = ch([2, 3, 4, 5, 10])
        n = ri(-2, 4) if b != 10 else ri(-3, 5)
        x = Fr(b) ** n
        k = ri(0, 1)
        xs = fq(x) if x.denominator != 1 else num(int(x))
        if k == 0:
            return MN("Nilai dari %s adalah …" % LOG(b, xs) if b != 10 else "Nilai dari log%s%s adalah …" % (NB, dz(x) if S.endlich(x) else xs), n,
                      [x / b if (x / b).denominator == 1 and x / b != n else n + 1, -n if n else 1, b * n if b * n != n else n - 1],
                      "%d%s = %s, jadi %s = %s." % (b, sup(n), xs, LOG(b, xs) if b != 10 else "log " + xs, sn(n)))
        n = ri(2, 5)
        return M("Bentuk logaritma dari %d%s = %s adalah …" % (b, sup(n), num(b ** n)), LOG(b, num(b ** n)) + " = %d" % n,
                 [LOG(n, num(b ** n)) + " = %d" % b, LOG(b, n) + " = %s" % num(b ** n), LOG(num(b ** n), b) + " = %d" % n],
                 "aⁿ = c ditulis <sup>a</sup>log c = n.")

    def sifat():
        b = ch([2, 3, 5, 6])
        k = ri(0, 3)
        if k == 0:
            p, q = ri(1, 4), ri(1, 4)
            x, y = b ** p, b ** q
            m = ri(1, 4)
            if y == 1:
                return None
            return MN("Nilai dari %s + %s adalah …" % (LOG(b, num(x * m)), LOG(b, Fr(y, m) if Fr(y, m).denominator == 1 else fq(Fr(y, m)))), p + q,
                      [p * q, p + q + 1, (x * m + y) // b if False else p + q - 1], "%s + %s = %s = %d." % (LOG(b, num(x * m)), LOG(b, fq(Fr(y, m))), LOG(b, num(x * y)), p + q)) if Fr(y, m).denominator == 1 else None
        if k == 1:
            p = ri(1, 3)
            m = ri(2, 9)
            if m % b == 0:
                return None
            return MN("Nilai dari %s − %s adalah …" % (LOG(b, num(m * b ** p)), LOG(b, m)), p, [p + 1, m * b ** p - m, b ** p], "%s = %s = %d." % (LOG(b, "%s/%d" % (num(m * b ** p), m)), LOG(b, num(b ** p)), p))
        if k == 2:
            p = ri(2, 4)
            c = ri(2, 3)
            return MN("Nilai dari %s adalah …" % LOG(b, "%s" % pw(b ** p, c) if b ** p < 30 else num(b ** p) + sup(c)), p * c, [p + c, p, b ** p * c if b ** p * c < 200 else p * c + 1], "%s = %d × %s = %d × %d = %d." % (LOG(b, "a" + sup("n")) if False else "<sup>a</sup>log b" + sup("n"), c, LOG(b, num(b ** p)), c, p, p * c) if False else
                      "<sup>a</sup>log bⁿ = n × <sup>a</sup>log b: %d × %d = %d." % (c, p, p * c))
        a, c = ch([(2, 3), (3, 5), (2, 5), (5, 7), (3, 7)])
        n = ri(2, 4)
        return MN("Nilai dari %s × %s adalah …" % (LOG(a, c), LOG(c, num(a ** n))), n, [n + 1, a * c, a ** n], "Rantai logaritma: <sup>a</sup>log b × <sup>b</sup>log c = <sup>a</sup>log c, jadi %s = %d." % (LOG(a, num(a ** n)), n))

    def diketahui():
        k = ri(0, 7)
        F = [("6", "p + q", ["pq", "p − q", "6p"]), ("12", "2p + q", ["p² + q", "2pq", "p + 2q"]), ("1,5", "q − p", ["p − q", "q : p", "p + q"]),
             ("5", "1 − p", ["p − 1", "5p", "1 + p"]), ("18", "p + 2q", ["2p + q", "p + q²", "2pq"]), ("8", "3p", ["p³", "8p", "p + 3"]),
             ("15", "1 − p + q", ["p + q + 1", "q − p", "1 + p − q"]), ("36", "2p + 2q", ["p² + q²", "4pq", "p + q"])]
        x, c, ws = F[k]
        return M("Diketahui log 2 = p dan log 3 = q. Nilai log %s adalah …" % x, c, ws, "Tulis %s sebagai hasil kali atau pembagian dari 2, 3, dan 10, lalu pakai sifat logaritma: log %s = %s." % (x, x, c))

    def persamaan():
        k = ri(0, 2)
        if k == 0:
            b, n = ch([2, 3, 5]), ri(1, 4)
            c = nz(-6, 6)
            x = b ** n - c
            if x <= 0:
                return None
            return MN("Penyelesaian dari %s = %d adalah x = …" % (LOG(b, "(%s)" % lin(1, c)), n), x, [b ** n + c, b * n - c, n - c], "x %s %d = %d%s = %d, jadi x = %d." % ("+" if c > 0 else "−", abs(c), b, sup(n), b ** n, x))
        if k == 1:
            a, n = ch([2, 4, 5, 20, 25]), ri(2, 3)
            x = Fr(10 ** n, a)
            if x.denominator != 1:
                return None
            return MN("Penyelesaian dari log x + log %d = %d adalah x = …" % (a, n), x, [10 ** n - a, Fr(10 ** n, a) * 10, n * 10 // a if n * 10 % a == 0 and n * 10 // a != x else x + 1], "log %dx = %d → %dx = %s → x = %s." % (a, n, a, num(10 ** n), num(int(x))))
        b = ch([2, 3])
        n = ri(2, 4)
        x = b ** n
        return MN("Penyelesaian dari %s + %s = %d adalah x = …" % (LOG(b, "x"), LOG(b, b), n + 1), x, [b * n, n + 1, b ** (n + 1)], "%s = %d, jadi x = %d%s = %d." % (LOG(b, "x"), n, b, sup(n), x))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            n = ri(2, 12)
            return MN("pH larutan dihitung dengan pH = −log[H⁺]. Jika [H⁺] = 10%s mol/L, pH larutan itu …" % sup(-n), n, [-n, 10 - n if 10 - n != n else n + 1, n + 1], "pH = −log 10%s = −(%s) = %d." % (sup(-n), sn(-n), n))
        if k == 1:
            m1, d = ri(4, 7), ri(1, 2)
            return MN("Pada skala Richter, kenaikan 1 skala berarti amplitudo gempa 10 kali lebih besar. Gempa %d SR dibandingkan gempa %d SR, amplitudonya … kali" % (m1 + d, m1), 10 ** d, [10 * d, d, 10 ** (d + 1)], "Selisih %d skala: 10%s = %s kali." % (d, sup(d), num(10 ** d)), unit="")
        db, k_ = ch([(10, 1), (20, 2), (30, 3), (40, 4)])
        return MN("Taraf intensitas bunyi TI = 10 log(I/I₀) desibel. Jika intensitas bunyi I = 10%s × I₀, TI = …" % sup(k_), db, [k_, 10 ** k_, db + 10], "TI = 10 × log 10%s = 10 × %d = %d dB." % (sup(k_), k_, db), unit="dB")

    sets = [("Definisi logaritma", [(definisi, 20)]),
            ("Sifat-sifat logaritma", [(sifat, 20)]),
            ("Logaritma dengan nilai yang diketahui", [(diketahui, 8), (sifat, 12)]),
            ("Persamaan logaritma", [(persamaan, 20)]),
            ("Logaritma dalam kehidupan", [(cerita, 12), (definisi, 8)])]
    return unit("logaritma", "B", 2, "Logaritma: Definisi, Sifat, dan Persamaan Logaritma", "Logaritma",
                "Peserta didik memahami logaritma sebagai invers dari eksponen, menggunakan sifat-sifat logaritma, dan menyelesaikan masalah yang terkait.",
                "Latihan logaritma kelas 10 SMA: definisi logaritma, mengubah bentuk eksponen ke logaritma, sifat-sifat logaritma, log 2 = p dan log 3 = q, persamaan logaritma, pH, dan desibel. 100 soal dengan kunci jawaban.",
                "ᵃlog c = n artinya aⁿ = c", "Logaritma adalah kebalikan dari eksponen.", sets,
                ["<sup>a</sup>log c = n artinya aⁿ = c, dengan a &gt; 0, a ≠ 1, dan c &gt; 0. Jika basisnya tidak ditulis, basisnya 10.",
                 "Sifat: <sup>a</sup>log bc = <sup>a</sup>log b + <sup>a</sup>log c, <sup>a</sup>log (b/c) = <sup>a</sup>log b − <sup>a</sup>log c, <sup>a</sup>log bⁿ = n × <sup>a</sup>log b, dan <sup>a</sup>log b × <sup>b</sup>log c = <sup>a</sup>log c.",
                 "Persamaan logaritma: ubah ke bentuk eksponen, lalu periksa syarat bilangan di dalam log harus positif."],
                [("<sup>2</sup>log 32 = …", ["2⁵ = 32"], "5"),
                 ("<sup>3</sup>log 18 − <sup>3</sup>log 2 = …", ["<sup>3</sup>log 9"], "2")],
                [["<sup>2</sup>log 8 = 4 (8 : 2)", "2³ = 8, jadi <sup>2</sup>log 8 = 3"],
                 ["log 2 + log 5 = log 7", "log 2 + log 5 = log 10 = 1"],
                 ["Lupa syarat bilangan di dalam log positif", "Periksa: hasil x harus membuat bilangan di dalam log positif"]],
                [("Apa hubungan logaritma dan eksponen?", "Logaritma adalah kebalikan dari eksponen: 2³ = 8 sama dengan <sup>2</sup>log 8 = 3."),
                 ("Mengapa log 1 = 0 untuk semua basis?", "Karena setiap bilangan (bukan 0) berpangkat 0 hasilnya 1."),
                 ("Untuk apa logaritma dipakai?", "Untuk skala yang sangat lebar, misalnya pH, skala Richter, dan desibel, serta untuk menghitung lama waktu pada pertumbuhan.")])


# ============================================================ 3. barisan dan deret
def u3():
    def aritmetika():
        a, b = nz(-10, 20), nz(-6, 9)
        p, q = sorted(sh(range(2, 10))[:2])
        n = ri(12, 40)
        up, uq = a + (p - 1) * b, a + (q - 1) * b
        k = ri(0, 1)
        if k == 0:
            v = a + (n - 1) * b
            return MN("Diketahui suku ke-%d barisan aritmetika adalah %s dan suku ke-%d adalah %s. Suku ke-%d adalah …" % (p, sn(up), q, sn(uq), n), v,
                      [a + n * b, v + b if v + b != a + n * b else v - 1, up + (n - 1) * b if up + (n - 1) * b != v else v + 2], "b = (%s − %s) : %d = %s, a = %s. U%s = %s + %d × %s = %s." % (sn(uq), par(up), q - p, sn(b), sn(a), sub(n), sn(a), n - 1, par(b), sn(v)))
        return MN("Diketahui U%s = %s dan U%s = %s pada barisan aritmetika. Beda barisan itu …" % (sub(p), sn(up), sub(q), sn(uq)), b, [Fr(uq - up, q - p + 1) if Fr(uq - up, q - p + 1).denominator == 1 and Fr(uq - up, q - p + 1) != b else b + 1, uq - up, -b], "b = (%s − %s) : (%d − %d) = %s." % (sn(uq), par(up), q, p, sn(b)))

    def deret_ar():
        a, b = ri(1, 20), ri(1, 9)
        n = ri(8, 30)
        S_ = n * (2 * a + (n - 1) * b) // 2
        k = ri(0, 1)
        if k == 0:
            return MN("Jumlah %d suku pertama deret %s adalah …" % (n, " + ".join(num(a + i * b) for i in range(3)) + " + …"), S_, [n * (a + (n - 1) * b), n * (2 * a + n * b) // 2, S_ - a], "Sₙ = n/2 (2a + (n − 1)b) = %d/2 × (%d + %d) = %s." % (n, 2 * a, (n - 1) * b, num(S_)))
        lo, step = ri(1, 9), ch([2, 3, 4, 5, 6, 7])
        hi = lo + step * ri(10, 30)
        cnt = (hi - lo) // step + 1
        S2 = cnt * (lo + hi) // 2
        return MN("Jumlah semua bilangan antara %d dan %d yang dibagi %d bersisa %d adalah …" % (lo - 1 if lo > 1 else 0, hi + 1, step, lo % step), S2,
                  [cnt * hi, (cnt - 1) * (lo + hi) // 2, S2 + hi], "Bilangannya %d, %d, …, %d (ada %d suku). S = %d/2 × (%d + %d) = %s." % (lo, lo + step, hi, cnt, cnt, lo, hi, num(S2))) if lo < step else None

    def geometri():
        a, r = nz(-5, 6), ch([2, 3, -2, Fr(1, 2), -3])
        n = ri(4, 7)
        v = a * Fr(r) ** (n - 1)
        if abs(v) > 30000 or v == 0:
            return None
        xs = [a * Fr(r) ** i for i in range(3)]
        k = ri(0, 1)
        if k == 0:
            return M("Suku ke-%d barisan %s, … adalah …" % (n, ", ".join(fq(x) for x in xs)), fq(v), [fq(a * Fr(r) ** n), fq(a * Fr(r) * (n - 1)), fq(-v)], "Uₙ = a × rⁿ⁻¹ = %s × %s%s = %s." % (sn(a), par(r) if Fr(r).denominator == 1 else "(%s)" % fq(r), sup(n - 1), fq(v)))
        p = ri(2, 4)
        up, uq = a * Fr(r) ** (p - 1), a * Fr(r) ** (p + 1)
        if Fr(r) < 0:
            return None
        return M("Pada barisan geometri dengan suku positif, U%s = %s dan U%s = %s. Rasionya …" % (sub(p), fq(up), sub(p + 2), fq(uq)), fq(r), [fq(Fr(r) ** 2), fq(uq - up), fq(1 / Fr(r))], "r² = %s : %s = %s, jadi r = %s." % (fq(uq), fq(up), fq(Fr(r) ** 2), fq(r)))

    def deret_geo():
        k = ri(0, 1)
        if k == 0:
            a, r, n = ri(1, 6), ch([2, 3]), ri(3, 7)
            S_ = a * (r ** n - 1) // (r - 1)
            return MN("Jumlah %d suku pertama deret geometri %s adalah …" % (n, " + ".join(num(a * r ** i) for i in range(3)) + " + …"), S_, [a * r ** n, a * r ** (n - 1), S_ - a], "Sₙ = a(rⁿ − 1)/(r − 1) = %d(%d%s − 1)/%d = %s." % (a, r, sup(n), r - 1, num(S_)))
        a, r = ri(2, 30), ch([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(2, 3), Fr(-1, 2), Fr(3, 4)])
        v = a / (1 - r)
        return M("Jumlah deret geometri tak hingga %s adalah …" % (" + ".join(fq(a * r ** i) if a * r ** i >= 0 else "(%s)" % fq(a * r ** i) for i in range(3)) + " + …"), fq(v),
                 [fq(a / (1 + r)), fq(a * (1 - r)), fq(v * 2)], "S∞ = a/(1 − r) = %d/(1 − %s) = %s." % (a, "(%s)" % fq(r) if r < 0 else fq(r), fq(v)))

    def cerita():
        k = ri(0, 3)
        if k == 0:
            h, r = ch([(8, Fr(1, 2)), (9, Fr(2, 3)), (12, Fr(3, 4)), (10, Fr(1, 2)), (6, Fr(2, 3)), (16, Fr(3, 4))])
            v = h + 2 * h * r / (1 - r)
            return MN("Bola dijatuhkan dari ketinggian %d m dan memantul setinggi %s dari tinggi sebelumnya, terus-menerus. Panjang lintasan bola sampai berhenti …" % (h, fq(r)), v,
                      [h / (1 - r), 2 * h / (1 - r), h * r / (1 - r)], "Turun: %d/(1 − %s), naik: %s/(1 − %s). Total = %s m." % (h, fq(r), fq(h * r), fq(r), sn(v)), unit="m")
        if k == 1:
            a, b, n = ri(10, 30), ri(2, 5), ri(10, 20)
            return MN("Pada gedung pertunjukan, baris pertama ada %d kursi dan setiap baris berikutnya bertambah %d kursi. Jika ada %d baris, banyak kursi seluruhnya …" % (a, b, n), n * (2 * a + (n - 1) * b) // 2,
                      [a + (n - 1) * b, n * a, n * (2 * a + n * b) // 2], "Sₙ = %d/2 × (%d + %d) = %s." % (n, 2 * a, (n - 1) * b, num(n * (2 * a + (n - 1) * b) // 2)), unit="kursi")
        if k == 2:
            a, b, n = ri(5, 20) * 10000, ri(1, 5) * 10000, ri(6, 12)
            S_ = n * (2 * a + (n - 1) * b) // 2
            return M("Gaji pertama seorang karyawan magang %s, dan setiap bulan naik %s. Jumlah gaji selama %d bulan …" % (rp(a), rp(b), n), rp(S_), [rp(a + (n - 1) * b), rp(n * a), rp(n * (a + n * b))], "Sₙ = %d/2 × (2 × %s + %d × %s) = %s." % (n, num(a), n - 1, num(b), rp(S_)))
        a, r, n = ri(2, 6), 2, ri(5, 8)
        return MN("Sebuah pesan berantai dikirim ke %d orang pada hari pertama. Setiap hari, banyak penerima baru dua kali hari sebelumnya. Jumlah penerima selama %d hari …" % (a, n), a * (2 ** n - 1),
                  [a * 2 ** (n - 1), a * 2 ** n, a * 2 * n], "Sₙ = %d(2%s − 1) = %s." % (a, sup(n), num(a * (2 ** n - 1))), unit="orang")

    sets = [("Barisan aritmetika", [(aritmetika, 20)]),
            ("Deret aritmetika", [(deret_ar, 20)]),
            ("Barisan geometri", [(geometri, 20)]),
            ("Deret geometri dan deret tak hingga", [(deret_geo, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    return unit("barisan-dan-deret", "A", 3, "Barisan dan Deret Aritmetika dan Geometri", "Barisan dan Deret",
                "Peserta didik menggunakan barisan dan deret aritmetika dan geometri, termasuk deret geometri tak hingga, untuk menyelesaikan masalah kontekstual.",
                "Latihan barisan dan deret kelas 10 SMA: suku ke-n barisan aritmetika dan geometri, beda dan rasio, jumlah n suku, deret geometri tak hingga, bola memantul, dan soal cerita. 100 soal dengan kunci jawaban.",
                "Aritmetika: tambah b. Geometri: kali r", "S∞ = a/(1 − r) untuk −1 &lt; r &lt; 1.", sets,
                ["Barisan aritmetika: Uₙ = a + (n − 1)b, deret: Sₙ = n/2 (2a + (n − 1)b) = n/2 (a + Uₙ).",
                 "Barisan geometri: Uₙ = a rⁿ⁻¹, deret: Sₙ = a(rⁿ − 1)/(r − 1) untuk r ≠ 1.",
                 "Deret geometri tak hingga dengan −1 &lt; r &lt; 1 mempunyai jumlah S∞ = a/(1 − r)."],
                [("U₃ = 11 dan U₇ = 27. U₂₀?", ["4b = 16, b = 4, a = 3", "U₂₀ = 3 + 19 × 4"], "79"),
                 ("8 + 4 + 2 + … = ?", ["a = 8, r = ½", "8/(1 − ½)"], "16")],
                [["Uₙ = a + nb", "Uₙ = a + (n − 1)b"],
                 ["Rasio = selisih dua suku", "Rasio = suku : suku sebelumnya"],
                 ["Bola memantul hanya dihitung lintasan turun", "Hitung lintasan turun dan naik"]],
                [("Apa beda barisan dan deret?", "Barisan adalah urutan bilangan. Deret adalah jumlah suku-suku barisan."),
                 ("Kapan deret geometri tak hingga mempunyai jumlah?", "Jika rasionya di antara −1 dan 1, sehingga suku-sukunya makin mendekati 0."),
                 ("Bagaimana mencari beda jika diketahui dua suku?", "Selisih kedua suku dibagi selisih nomor sukunya.")])


def sub(n):
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(c)] for c in str(n))


# ============================================================ 4. bunga majemuk, pertumbuhan, peluruhan
def u4():
    def majemuk():
        m = ri(1, 20) * 1000000
        i = ch([5, 10, 20])
        n = ri(2, 3)
        v = Fr(m) * Fr(100 + i, 100) ** n
        if v.denominator != 1:
            return None
        k = ri(0, 1)
        if k == 0:
            return M("Modal %s disimpan dengan bunga majemuk %d%% per tahun. Nilai akhir setelah %d tahun …" % (rp(m), i, n), rp(int(v)), [rp(m + m * i * n // 100), rp(int(v) - m), rp(int(Fr(m) * Fr(100 + i, 100) ** (n - 1)))],
                     "Mₙ = M(1 + i)ⁿ = %s × %s%s = %s." % (rp(m), dz(Fr(100 + i, 100)), sup(n), rp(int(v))))
        return M("Modal %s dengan bunga majemuk %d%% per tahun. Besar bunga selama %d tahun …" % (rp(m), i, n), rp(int(v) - m), [rp(m * i * n // 100), rp(int(v)), rp(m * i // 100)], "Nilai akhir %s, bunga = %s − %s = %s." % (rp(int(v)), rp(int(v)), rp(m), rp(int(v) - m)))

    def banding():
        m = ri(2, 20) * 1000000
        i = ch([10, 20])
        n = 2
        maj = Fr(m) * Fr(100 + i, 100) ** n
        tun = m + m * i * n // 100
        return M("Modal %s disimpan %d tahun dengan bunga %d%% per tahun. Selisih nilai akhir bunga majemuk dan bunga tunggal …" % (rp(m), n, i), rp(int(maj) - tun), [rp(int(maj) - m), rp(tun - m), rp(m * i // 100)],
                 "Majemuk %s, tunggal %s. Selisih %s." % (rp(int(maj)), rp(tun), rp(int(maj) - tun)))

    def tumbuh():
        p0 = ri(1, 50) * 1000
        r = ch([10, 20, 50])
        n = ri(2, 3)
        v = Fr(p0) * Fr(100 + r, 100) ** n
        if v.denominator != 1:
            return None
        it = ch([("Penduduk sebuah kota", "jiwa", "tahun"), ("Banyak pelanggan sebuah toko daring", "orang", "bulan"), ("Populasi ikan di kolam", "ekor", "bulan")])
        return MN("%s %s %s dan bertambah %d%% setiap %s. Setelah %d %s menjadi …" % (it[0], num(p0), it[1], r, it[2], n, it[2]), v, [p0 + p0 * r * n // 100, p0 * Fr(100 + r, 100) ** (n - 1), v + p0], "P = %s × %s%s = %s." % (num(p0), dz(Fr(100 + r, 100)), sup(n), num(int(v))), unit=it[1])

    def susut():
        h = ri(5, 40) * 1000000
        r = ch([10, 20, 25, 30])
        n = 2
        v = Fr(h) * Fr(100 - r, 100) ** n
        if v.denominator != 1:
            return None
        it = ch(["motor", "mobil", "laptop", "mesin jahit"])
        return M("Harga sebuah %s %s dan nilainya menyusut %d%% setiap tahun dari nilai tahun sebelumnya. Nilainya setelah %d tahun …" % (it, rp(h), r, n), rp(int(v)), [rp(h - h * r * n // 100), rp(int(Fr(h) * Fr(100 - r, 100))), rp(h - int(v))],
                 "%s × %s² = %s." % (rp(h), dz(Fr(100 - r, 100)), rp(int(v))))

    def paruh():
        m0 = ch([100, 200, 400, 800, 1600, 640])
        n = ri(2, 5)
        t = ch([6, 8, 12, 24])
        v = Fr(m0, 2 ** n)
        k = ri(0, 1)
        if k == 0:
            return MD("Obat %d mg dalam darah berkurang setengahnya setiap %d jam. Banyak obat setelah %d jam …" % (m0, t, n * t), v, [Fr(m0, 2 * n), Fr(m0, 2 ** (n + 1)), m0 - v], "%d jam = %d kali waktu paruh: %d × (½)%s = %s mg." % (n * t, n, m0, sup(n), dz(v)), unit="mg")
        return MN("Zat %d gram meluruh menjadi %s gram dalam %d hari. Waktu paruhnya …" % (m0, dz(v), n * t), t, [n * t, t * 2, Fr(n * t, n + 1) if Fr(n * t, n + 1).denominator == 1 else t + 2], "%d → %s gram berarti %d kali setengah. Waktu paruh = %d : %d = %d hari." % (m0, dz(v), n, n * t, n, t), unit="hari")

    sets = [("Bunga majemuk", [(majemuk, 20)]),
            ("Bunga tunggal dan bunga majemuk", [(banding, 8), (majemuk, 12)]),
            ("Pertumbuhan", [(tumbuh, 20)]),
            ("Penyusutan nilai", [(susut, 20)]),
            ("Peluruhan dan waktu paruh", [(paruh, 20)])]
    return unit("bunga-majemuk-pertumbuhan-dan-peluruhan", "A", 4, "Bunga Majemuk, Pertumbuhan, dan Peluruhan", "Bunga Majemuk, Pertumbuhan, dan Peluruhan",
                "Peserta didik menggunakan fungsi eksponensial dan barisan geometri untuk menyelesaikan masalah bunga majemuk, pertumbuhan, penyusutan, dan peluruhan (literasi finansial).",
                "Latihan bunga majemuk, pertumbuhan, dan peluruhan kelas 10 SMA: nilai akhir modal, bunga tunggal dan majemuk, pertumbuhan penduduk, penyusutan harga barang, dan waktu paruh. 100 soal dengan kunci jawaban.",
                "Mₙ = M(1 + i)ⁿ", "Pertumbuhan dikali (1 + r), penyusutan dikali (1 − r).", sets,
                ["Bunga majemuk: bunga ikut berbunga. Nilai akhir Mₙ = M(1 + i)ⁿ, dengan i persen bunga per periode dan n banyak periode.",
                 "Pertumbuhan r% per periode: P = P₀(1 + r)ⁿ. Penyusutan r% per periode: P = P₀(1 − r)ⁿ.",
                 "Peluruhan dengan waktu paruh T: setelah n kali waktu paruh, sisa zat = M₀ × (½)ⁿ."],
                [("Rp2.000.000 dengan bunga majemuk 10% per tahun, 2 tahun?", ["2.000.000 × 1,1²"], "Rp2.420.000"),
                 ("Motor Rp20.000.000 menyusut 20% per tahun, 2 tahun?", ["20.000.000 × 0,8²"], "Rp12.800.000")],
                [["Bunga majemuk dihitung seperti bunga tunggal", "Bunga tahun kedua dihitung dari modal + bunga tahun pertama"],
                 ["Penyusutan 20% dua tahun = 40%", "Dikali 0,8 dua kali: 0,64 (berkurang 36%)"],
                 ["Waktu paruh dianggap habis dalam 2 kali waktu paruh", "Setiap waktu paruh, sisa menjadi setengahnya"]],
                [("Apa beda bunga tunggal dan bunga majemuk?", "Bunga tunggal selalu dihitung dari modal awal. Bunga majemuk dihitung dari modal ditambah bunga sebelumnya."),
                 ("Apa itu waktu paruh?", "Waktu yang diperlukan agar banyak zat tinggal setengahnya."),
                 ("Mengapa bunga majemuk lebih menguntungkan bagi penabung?", "Karena bunga juga mendapat bunga, sehingga nilai tabungan tumbuh makin cepat.")])


# ============================================================ 5. vektor
def u5():
    def v(x, y):
        return "(%s, %s)" % (sn(x), sn(y))

    def komponen():
        x1, y1, x2, y2 = nz(-6, 6), nz(-6, 6), nz(-6, 6), nz(-6, 6)
        if (x1, y1) == (x2, y2):
            return None
        k = ri(0, 1)
        if k == 0:
            return M("Diketahui A%s dan B%s. Vektor <span class='vec'>AB</span> adalah …" % (v(x1, y1), v(x2, y2)), v(x2 - x1, y2 - y1),
                     [v(x1 - x2, y1 - y2), v(x1 + x2, y1 + y2), v(x2 - x1, y1 - y2)], "<span class='vec'>AB</span> = B − A = %s." % v(x2 - x1, y2 - y1))
        return M("Titik tengah ruas garis AB dengan A%s dan B%s adalah …" % (v(x1, y1), v(x2, y2)), "(%s, %s)" % (fq(Fr(x1 + x2, 2)), fq(Fr(y1 + y2, 2))),
                 ["(%s, %s)" % (fq(Fr(x2 - x1, 2)), fq(Fr(y2 - y1, 2))), v(x1 + x2, y1 + y2), "(%s, %s)" % (fq(Fr(x1 + x2, 2)), fq(Fr(y1 - y2, 2)))],
                 "Titik tengah = ((x₁ + x₂)/2, (y₁ + y₂)/2) = (%s, %s)." % (fq(Fr(x1 + x2, 2)), fq(Fr(y1 + y2, 2))))

    def operasi():
        a, b, c, d = nz(-6, 6), nz(-6, 6), nz(-6, 6), nz(-6, 6)
        p, q = ch([1, 2, 3, -1, -2]), ch([1, 2, 3, -1, -2, -3])
        if p == 1 and q == 1:
            return None
        res = (p * a + q * c, p * b + q * d)
        lab = expr([(p, "<b>u</b>"), (q, "<b>v</b>")])
        return M("Diketahui <b>u</b> = %s dan <b>v</b> = %s. Vektor %s adalah …" % (v(a, b), v(c, d), lab), v(*res),
                 [v(p * a - q * c, p * b - q * d), v(p * a + c, p * b + d), v(res[0], -res[1]) if res[1] else v(res[0] + 1, res[1])],
                 "%s = (%s, %s) = %s." % (lab, "%s × %s + %s × %s" % (sn(p), par(a), par(q), par(c)), "%s × %s + %s × %s" % (sn(p), par(b), par(q), par(d)), v(*res)))

    def panjang():
        a, b, c = ch([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (7, 24, 25)])
        sx, sy = ch([1, -1]), ch([1, -1])
        x, y = sx * a, sy * b
        if ri(0, 1):
            x, y = y, x
        k = ri(0, 1)
        if k == 0:
            return MN("Panjang vektor <b>u</b> = %s adalah …" % v(x, y), c, [a + b, c * c, abs(x - y) if abs(x - y) != c else c + 1], "|<b>u</b>| = √(%s² + %s²) = √%d = %d." % (par(x), par(y), c * c, c))
        p, q = ri(1, 5), ri(1, 5)
        s = p * p + q * q
        r = math.isqrt(s)
        if r * r == s:
            return None
        return M("Panjang vektor <b>u</b> = %s adalah …" % v(p * ch([1, -1]), q * ch([1, -1])), "√%d" % s, ["%d" % (p + q), "√%d" % abs(p * p - q * q) if p != q else "√%d" % (s + 1), "%d" % s], "|<b>u</b>| = √(%d + %d) = √%d." % (p * p, q * q, s))

    def titik():
        a, b, c, d = nz(-6, 6), nz(-6, 6), nz(-6, 6), nz(-6, 6)
        k = ri(0, 1)
        if k == 0:
            val = a * c + b * d
            return MN("Diketahui <b>u</b> = %s dan <b>v</b> = %s. Hasil <b>u</b> · <b>v</b> adalah …" % (v(a, b), v(c, d)), val, [a * d + b * c, (a + c) * (b + d), -val if val else 1], "<b>u</b> · <b>v</b> = %s × %s + %s × %s = %s." % (sn(a), par(c), sn(b), par(d), sn(val)))
        # u = (a, b), v = (k, d), cari k agar tegak lurus
        k_ = Fr(-b * d, a)
        if k_.denominator != 1:
            return None
        return MN("Vektor <b>u</b> = %s dan <b>v</b> = (k, %s) saling tegak lurus. Nilai k adalah …" % (v(a, b), sn(d)), k_, [-k_ if k_ else 1, Fr(b * d, a) * 2 if b * d else 2, k_ + 1], "Tegak lurus berarti <b>u</b> · <b>v</b> = 0: %s k + %s × %s = 0, jadi k = %s." % (sn(a), par(b), par(d), sn(k_)))

    def sudut():
        F = [((1, 0), (0, 1), 90), ((1, 1), (1, 0), 45), ((1, 0), (-1, 0), 180), ((3, 4), (-4, 3), 90), ((2, 2), (0, 3), 45), ((1, 1), (-1, 1), 90),
             ((2, 0), (1, 1), 45), ((0, 2), (0, 5), 0), ((1, 0), (-1, 1), 135), ((3, 0), (0, -2), 90), ((4, 4), (-2, 0), 135), ((5, 0), (-3, 0), 180)]
        u_, w_, ang = ch(F)
        return M("Besar sudut antara vektor <b>u</b> = %s dan <b>v</b> = %s adalah …" % (v(*u_), v(*w_)), "%d°" % ang, ["%d°" % x for x in [0, 30, 45, 60, 90, 120, 135, 180] if x != ang][:6] and sh(["%d°" % x for x in [0, 45, 60, 90, 135, 180] if x != ang]),
                 "cos θ = (<b>u</b> · <b>v</b>) / (|<b>u</b>| |<b>v</b>|) memberikan θ = %d°." % ang)

    def cerita():
        a, b = ch([(3, 4), (6, 8), (5, 12), (9, 12), (8, 6), (12, 5)])
        k = ri(0, 1)
        if k == 0:
            c = int(math.hypot(a, b))
            return MN("Sebuah perahu bergerak %d km ke timur, lalu %d km ke utara. Besar perpindahannya …" % (a, b), c, [a + b, abs(a - b), c + 1], "Perpindahan = √(%d² + %d²) = %d km." % (a, b, c), unit="km")
        p, q, r, s = ri(1, 6), ri(1, 6), ri(1, 6), ri(1, 6)
        return M("Gaya <b>F₁</b> = (%d, %d) N dan <b>F₂</b> = (%d, %s) N bekerja pada sebuah benda. Resultan gayanya …" % (p, q, r, sn(-s)), "(%d, %s) N" % (p + r, sn(q - s)), ["(%s, %d) N" % (sn(p - r), q + s), "(%d, %d) N" % (p + r, q + s), "(%d, %s) N" % (p * r, sn(-q * s))],
                 "Jumlahkan komponen yang bersesuaian: (%d + %d, %d + %s) = (%d, %s)." % (p, r, q, par(-s), p + r, sn(q - s)))

    sets = [("Vektor dari dua titik", [(komponen, 20)]),
            ("Penjumlahan dan perkalian skalar", [(operasi, 20)]),
            ("Panjang vektor", [(panjang, 20)]),
            ("Perkalian titik dan sudut", [(titik, 12), (sudut, 8)]),
            ("Vektor dalam kehidupan", [(cerita, 20)])]
    return unit("vektor", "G", 5, "Vektor dan Operasinya", "Vektor",
                "Peserta didik menyatakan vektor pada bidang koordinat, melakukan operasi vektor (penjumlahan, pengurangan, perkalian skalar), dan menggunakannya untuk menyelesaikan masalah.",
                "Latihan vektor kelas 10 SMA: vektor dari dua titik, titik tengah, penjumlahan, pengurangan, perkalian skalar, panjang vektor, perkalian titik, vektor tegak lurus, dan perpindahan. 100 soal dengan kunci jawaban.",
                "AB = B − A", "|u| = √(x² + y²), u · v = x₁x₂ + y₁y₂.", sets,
                ["Vektor mempunyai besar dan arah. Vektor dari A ke B adalah <span class='vec'>AB</span> = B − A, yaitu selisih koordinat ujung dan pangkal.",
                 "Penjumlahan dan perkalian skalar dilakukan per komponen: (a, b) + (c, d) = (a + c, b + d) dan k(a, b) = (ka, kb).",
                 "Panjang vektor |(x, y)| = √(x² + y²). Perkalian titik (a, b) · (c, d) = ac + bd; dua vektor tegak lurus jika hasilnya 0."],
                [("A(1, 2), B(4, −2). <span class='vec'>AB</span> dan panjangnya?", ["(4 − 1, −2 − 2) = (3, −4)", "√(9 + 16)"], "(3, −4), panjang 5"),
                 ("u = (2, −1), v = (3, 4). 2u − v?", ["(4, −2) − (3, 4)"], "(1, −6)")],
                [["<span class='vec'>AB</span> = A − B", "<span class='vec'>AB</span> = B − A (ujung dikurangi pangkal)"],
                 ["|(3, −4)| = 3 + (−4) = −1", "|(3, −4)| = √(9 + 16) = 5"],
                 ["u · v hasilnya vektor", "Hasil perkalian titik adalah bilangan"]],
                [("Apa beda vektor dan skalar?", "Skalar hanya mempunyai besar (misalnya massa). Vektor mempunyai besar dan arah (misalnya gaya atau perpindahan)."),
                 ("Kapan dua vektor tegak lurus?", "Jika hasil perkalian titiknya 0."),
                 ("Di mana vektor dipakai?", "Dalam fisika (gaya, kecepatan), navigasi kapal dan pesawat, serta grafika komputer.")])


# ============================================================ 6. perbandingan trigonometri
TR = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


def u6():
    def segitiga():
        a, b, c = ch(TR)
        if ri(0, 1):
            a, b = b, a
        f = ch(["sin", "cos", "tan"])
        val = {"sin": Fr(a, c), "cos": Fr(b, c), "tan": Fr(a, b)}
        pic = figure({"A": (0, 0), "B": (b, 0), "C": (b, a)}, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("A", "B", str(b)), ("B", "C", str(a)), ("A", "C", str(c))], right=[("B", "A", "C")], label="segitiga siku-siku ABC")
        return M("Pada segitiga siku-siku berikut, nilai %s A adalah …" % f + pic, fq(val[f]), [fq(x) for k, x in val.items() if k != f] + [fq(1 / val[f])],
                 "sin A = depan/miring, cos A = samping/miring, tan A = depan/samping. %s A = %s." % (f, fq(val[f])))

    def dari_satu():
        a, b, c = ch(TR)
        g, f = ch([("sin", "cos"), ("sin", "tan"), ("cos", "sin"), ("cos", "tan"), ("tan", "sin"), ("tan", "cos")])
        val = {"sin": Fr(a, c), "cos": Fr(b, c), "tan": Fr(a, b)}
        return M("Sudut A lancip dan %s A = %s. Nilai %s A adalah …" % (g, fq(val[g]), f), fq(val[f]), [fq(x) for k, x in val.items() if k != f and x != val[f]] + [fq(1 / val[f])],
                 "Gambar segitiga siku-siku dengan sisi %d, %d, %d (teorema Pythagoras). %s A = %s." % (a, b, c, f, fq(val[f])))

    def istimewa():
        E = [("sin 30° + cos 60°", "1"), ("sin 60° × cos 30°", "¾"), ("tan 45° + sin 90°", "2"), ("2 sin 45° cos 45°", "1"), ("sin² 60° + cos² 60°", "1"),
             ("tan 60° × tan 30°", "1"), ("cos 0° − sin 30°", "½"), ("sin 45° × cos 45°", "½"), ("2 cos 60° + tan 45°", "2"), ("sin 30° × tan 60°", "½√3"),
             ("cos² 45° + sin² 30°", "¾"), ("4 sin 30° cos 60°", "1"), ("tan 30° × cos 30°", "½"), ("sin 90° − cos² 30°", "¼"), ("3 tan² 30°", "1"),
             ("cos 30° + sin 60°", "√3"), ("tan² 60° − 1", "2"), ("sin 60° : cos 60°", "√3")]
        q, c = ch(E)
        return M("Nilai dari %s adalah …" % q, c, sh([x for x in ["0", "½", "1", "2", "¾", "¼", "√3", "½√3", "½√2", "√2"] if x != c]), "Gunakan nilai sudut istimewa: sin 30° = ½, cos 30° = ½√3, sin 45° = cos 45° = ½√2, tan 60° = √3. Hasilnya %s." % c)

    def berelasi():
        q = ri(1, 3)
        base = ch([30, 45, 60])
        ang = [180 - base, 180 + base, 360 - base][q - 1]
        f = ch(["sin", "cos", "tan"])
        sign = {1: {"sin": 1, "cos": -1, "tan": -1}, 2: {"sin": -1, "cos": -1, "tan": 1}, 3: {"sin": -1, "cos": 1, "tan": -1}}[q][f]
        tbl = {"sin": SIN, "cos": COS, "tan": TAN}[f]
        val = tbl[base]
        c = val if sign > 0 else neg(val)
        ws = [neg(c), {"sin": COS, "cos": SIN, "tan": TAN}[f][base] if f != "tan" else ("⅓√3" if base == 60 else ("√3" if base == 30 else "0")), neg({"sin": COS, "cos": SIN, "tan": TAN}[f][base]) if f != "tan" else MINUS + "√3"]
        return M("Nilai %s %d° adalah …" % (f, ang), c, ws, "%d° = %s di kuadran %s. Di kuadran itu %s bernilai %s, jadi %s %d° = %s." % (ang, ["180° − %d°" % base, "180° + %d°" % base, "360° − %d°" % base][q - 1], ["II", "III", "IV"][q - 1], f, "positif" if sign > 0 else "negatif", f, ang, c))

    def sisi():
        ang = ch([30, 45, 60])
        k = ri(0, 2)
        h = ri(2, 12) * 2
        if k == 0:
            # sisi miring h, cari sisi depan
            v = {30: sn(h // 2), 45: surd(h // 2, 2), 60: surd(h // 2, 3)}[ang]
            w = {30: [surd(h // 2, 3), surd(h // 2, 2), sn(h)], 45: [sn(h // 2), surd(h, 2), surd(h // 2, 3)], 60: [sn(h // 2), surd(h // 2, 2), surd(h, 3)]}[ang]
            return M("Pada segitiga siku-siku, sisi miring %d cm dan salah satu sudut lancipnya %d°. Panjang sisi di depan sudut itu … cm" % (h, ang), v, w, "Sisi depan = sisi miring × sin %d° = %d × %s = %s cm." % (ang, h, SIN[ang], v))
        if k == 1:
            v = {30: surd(h // 2, 3), 45: surd(h // 2, 2), 60: sn(h // 2)}[ang]
            w = [surd(h // 2, 3) if ang != 30 else sn(h // 2), surd(h, 2) if ang != 45 else sn(h // 2), surd(h // 2, 2) if ang != 45 else surd(h // 2, 3)]
            return M("Pada segitiga siku-siku, sisi miring %d cm dan salah satu sudut lancipnya %d°. Panjang sisi di samping sudut itu … cm" % (h, ang), v, w, "Sisi samping = sisi miring × cos %d° = %d × %s = %s cm." % (ang, h, COS[ang], v))
        s = h // 2
        v = {30: S.fr(surd(s, 3), 3) if s % 3 else surd(s // 3, 3), 45: sn(s), 60: surd(s, 3)}[ang]
        return M("Pada segitiga siku-siku, sisi di samping sudut %d° panjangnya %d cm. Panjang sisi di depan sudut itu … cm" % (ang, s), v, sh([x for x in [surd(s, 3), sn(s), surd(s, 2), sn(2 * s)] if x != v]), "Sisi depan = sisi samping × tan %d° = %d × %s." % (ang, s, TAN[ang]))

    sets = [("Perbandingan pada segitiga siku-siku", [(segitiga, 20)]),
            ("Mencari perbandingan lain", [(dari_satu, 20)]),
            ("Sudut istimewa", [(istimewa, 18), (segitiga, 2)]),
            ("Sudut berelasi di kuadran II, III, IV", [(berelasi, 16), (segitiga, 4)]),
            ("Menghitung panjang sisi", [(sisi, 20)])]
    return unit("perbandingan-trigonometri", "G", 6, "Perbandingan Trigonometri dan Sudut Istimewa", "Perbandingan Trigonometri",
                "Peserta didik menjelaskan rasio trigonometri (sinus, kosinus, tangen) pada segitiga siku-siku, nilai sudut istimewa, dan sudut berelasi untuk menyelesaikan masalah.",
                "Latihan perbandingan trigonometri kelas 10 SMA: sin, cos, dan tan pada segitiga siku-siku, mencari perbandingan lain, nilai sudut istimewa 30°, 45°, 60°, sudut berelasi di semua kuadran, dan panjang sisi. 100 soal dengan kunci jawaban.",
                "sin = depan/miring, cos = samping/miring", "tan = depan/samping. Ingat tanda di setiap kuadran.", sets,
                ["Pada segitiga siku-siku dengan sudut lancip A: sin A = sisi depan/sisi miring, cos A = sisi samping/sisi miring, tan A = sisi depan/sisi samping.",
                 "Sudut istimewa: sin 30° = ½, sin 45° = ½√2, sin 60° = ½√3; cos 30° = ½√3, cos 45° = ½√2, cos 60° = ½; tan 30° = ⅓√3, tan 45° = 1, tan 60° = √3.",
                 "Di kuadran I semua positif, kuadran II hanya sin positif, kuadran III hanya tan positif, kuadran IV hanya cos positif. Contoh sin 150° = sin 30° = ½."],
                [("sin A = 3/5. cos A dan tan A?", ["Sisi samping = √(25 − 9) = 4"], "cos A = 4/5, tan A = 3/4"),
                 ("cos 120° = …", ["120° = 180° − 60° (kuadran II)", "cos negatif"], "−½")],
                [["sin A = samping/miring", "sin A = depan/miring"],
                 ["cos 120° = cos 60° = ½", "Di kuadran II cos negatif: −½"],
                 ["tan 30° = √3", "tan 30° = ⅓√3; tan 60° = √3"]],
                [("Apa arti sinus suatu sudut?", "Perbandingan sisi di depan sudut dengan sisi miring pada segitiga siku-siku."),
                 ("Bagaimana mengingat tanda di setiap kuadran?", "Kuadran I semua positif, II sinus, III tangen, IV kosinus."),
                 ("Mengapa sin² A + cos² A = 1?", "Karena (depan/miring)² + (samping/miring)² = (depan² + samping²)/miring² = 1 menurut teorema Pythagoras.")])


# ============================================================ 7. aplikasi trigonometri
def u7():
    COS60 = [(a, b, int(math.isqrt(a * a + b * b - a * b))) for a in range(2, 41) for b in range(a + 1, 41) if math.isqrt(a * a + b * b - a * b) ** 2 == a * a + b * b - a * b]
    COS120 = [(a, b, int(math.isqrt(a * a + b * b + a * b))) for a in range(2, 41) for b in range(a + 1, 41) if math.isqrt(a * a + b * b + a * b) ** 2 == a * a + b * b + a * b]
    COS60 += [(b, a, c) for a, b, c in COS60]
    COS120 += [(b, a, c) for a, b, c in COS120]

    def elevasi():
        ang = ch([30, 45, 60])
        d = ri(2, 15) * 10
        h = {30: S.fr(surd(d, 3), 3) if d % 3 else surd(d // 3, 3), 45: sn(d), 60: surd(d, 3)}[ang]
        k = ri(0, 1)
        if k == 0:
            return M("Dari titik yang berjarak %d m dari kaki sebuah menara, puncak menara terlihat dengan sudut elevasi %d°. Tinggi menara … m" % (d, ang), h,
                     sh([x for x in [surd(d, 3), sn(d), surd(d, 2), sn(d // 2), S.fr(surd(d, 3), 3) if d % 3 else surd(d // 3, 3)] if x != h]), "Tinggi = %d × tan %d° = %s m." % (d, ang, h))
        return M("Dari puncak mercusuar setinggi %d m, sebuah kapal terlihat dengan sudut depresi %d°. Jarak kapal ke kaki mercusuar … m" % (d, ang),
                 {30: surd(d, 3), 45: sn(d), 60: S.fr(surd(d, 3), 3) if d % 3 else surd(d // 3, 3)}[ang],
                 sh([x for x in [surd(d, 3), sn(d), surd(d, 2), S.fr(surd(d, 3), 3) if d % 3 else surd(d // 3, 3), sn(2 * d)] if x != {30: surd(d, 3), 45: sn(d), 60: S.fr(surd(d, 3), 3) if d % 3 else surd(d // 3, 3)}[ang]]),
                 "Jarak = tinggi : tan %d°." % ang)

    def sinus():
        A, B = ch([(30, 45), (45, 30), (30, 60), (60, 30), (45, 60), (60, 45), (30, 90), (90, 30), (45, 90), (30, 120), (120, 30), (45, 135)])
        sv = {30: (1, 1), 45: (1, 2), 60: (1, 3), 90: (2, 1), 120: (1, 3), 135: (1, 2)}  # sin = k/2 * √m
        a = ri(2, 10) * 2
        # b = a sinB / sinA
        ka, ma = sv[A]
        kb, mb = sv[B]
        # sinA = ka/2 √ma , sinB = kb/2 √mb ; b = a kb √mb /(ka √ma) = a kb √(mb ma)/(ka ma)
        num_ = Fr(a * kb, ka * ma)
        root = mb * ma
        kk = 1
        for f in range(int(math.isqrt(root)), 1, -1):
            if root % (f * f) == 0:
                kk, root = f, root // (f * f)
                break
        coef = num_ * kk
        if coef.denominator != 1:
            return None
        c = surd(int(coef), root)
        return M("Pada segitiga ABC, ∠A = %d°, ∠B = %d°, dan BC = %d cm. Panjang AC adalah … cm" % (A, B, a), c,
                 sh([x for x in [surd(a, 2), surd(a, 3), sn(a * 2), sn(a // 2), surd(a // 2, 6), surd(a // 2, 2), surd(a // 2, 3)] if x != c]),
                 "Aturan sinus: AC/sin B = BC/sin A, jadi AC = %d × sin %d° : sin %d° = %s cm." % (a, B, A, c))

    def kosinus():
        k = ri(0, 1)
        a, b, c = ch(COS60 if k == 0 else COS120)
        C = 60 if k == 0 else 120
        return MN("Pada segitiga ABC, CA = %d cm, CB = %d cm, dan ∠C = %d°. Panjang AB adalah …" % (a, b, C), c, [a + b - 1 if a + b - 1 != c else c + 2, int(math.isqrt(a * a + b * b)) if math.isqrt(a * a + b * b) != c else c - 1, abs(b - a) + 1],
                  "AB² = %d² + %d² − 2 × %d × %d × cos %d° = %d, jadi AB = %d cm." % (a, b, a, b, C, c * c, c), unit="cm")

    def luas():
        a, b = ri(3, 16), ri(3, 16)
        C = ch([30, 150, 90, 60, 45, 120, 135])
        k_ = {30: (Fr(1, 2), 1), 150: (Fr(1, 2), 1), 90: (1, 1), 60: (Fr(1, 2), 3), 120: (Fr(1, 2), 3), 45: (Fr(1, 2), 2), 135: (Fr(1, 2), 2)}[C]
        coef = Fr(a * b, 2) * k_[0]
        if coef.denominator != 1:
            return None
        c = surd(int(coef), k_[1])
        ws = [surd(int(coef) * 2, k_[1]) if True else "", sn(a * b), surd(int(coef), 3 if k_[1] != 3 else 2)]
        return M("Luas segitiga dengan dua sisi %d cm dan %d cm serta sudut apit %d° adalah … cm²" % (a, b, C), c, ws, "L = ½ × %d × %d × sin %d° = %s cm²." % (a, b, C, c))

    def kapal():
        k = ri(0, 1)
        a, b, c = ch(COS60 if k == 0 else COS120)
        C = 60 if k == 0 else 120
        return MN("Dua kapal berangkat dari pelabuhan yang sama. Kapal A berlayar %d km dan kapal B %d km, dengan sudut antara arah keduanya %d°. Jarak kedua kapal …" % (a, b, C), c,
                  [a + b, int(math.isqrt(a * a + b * b)) if math.isqrt(a * a + b * b) != c else c + 1, abs(a - b) if abs(a - b) != c else c - 1], "Aturan kosinus: d² = %d² + %d² − 2 × %d × %d × cos %d° = %d, d = %d km." % (a, b, a, b, C, c * c, c), unit="km")

    sets = [("Sudut elevasi dan depresi", [(elevasi, 20)]),
            ("Aturan sinus", [(sinus, 20)]),
            ("Aturan kosinus", [(kosinus, 20)]),
            ("Luas segitiga", [(luas, 20)]),
            ("Soal cerita", [(kapal, 12), (elevasi, 8)])]
    return unit("aturan-sinus-kosinus-dan-luas-segitiga", "G", 7, "Aturan Sinus, Aturan Kosinus, dan Luas Segitiga", "Aturan Sinus dan Kosinus",
                "Peserta didik menggunakan perbandingan trigonometri, aturan sinus, dan aturan kosinus untuk menyelesaikan masalah segitiga, termasuk sudut elevasi, sudut depresi, dan luas segitiga.",
                "Latihan aplikasi trigonometri kelas 10 SMA: sudut elevasi dan depresi, aturan sinus, aturan kosinus, luas segitiga dengan rumus ½ab sin C, dan jarak dua kapal. 100 soal dengan kunci jawaban.",
                "a/sin A = b/sin B = c/sin C", "c² = a² + b² − 2ab cos C; L = ½ab sin C.", sets,
                ["Sudut elevasi diukur ke atas dari garis mendatar, sudut depresi diukur ke bawah. Gunakan tan = depan/samping untuk mencari tinggi atau jarak.",
                 "Aturan sinus: a/sin A = b/sin B = c/sin C. Dipakai jika diketahui dua sudut dan satu sisi.",
                 "Aturan kosinus: c² = a² + b² − 2ab cos C, dipakai jika diketahui dua sisi dan sudut apitnya. Luas segitiga = ½ab sin C."],
                [("Jarak 30 m, sudut elevasi 60°. Tinggi?", ["30 × tan 60° = 30√3"], "30√3 m"),
                 ("a = 5, b = 8, C = 60°. c?", ["c² = 25 + 64 − 40 = 49"], "7")],
                [["Aturan kosinus tanpa tanda minus", "c² = a² + b² − 2ab cos C"],
                 ["cos 120° dianggap ½", "cos 120° = −½, sehingga −2ab cos C menjadi +ab"],
                 ["Luas segitiga = ab sin C", "Luas = ½ab sin C"]],
                [("Kapan memakai aturan sinus dan kapan aturan kosinus?", "Aturan sinus untuk pasangan sisi dan sudut di depannya. Aturan kosinus untuk dua sisi dengan sudut apit, atau tiga sisi."),
                 ("Apa beda sudut elevasi dan sudut depresi?", "Sudut elevasi dilihat ke atas, sudut depresi dilihat ke bawah, keduanya dari garis mendatar."),
                 ("Apakah aturan kosinus berlaku untuk segitiga siku-siku?", "Ya. Jika C = 90°, cos C = 0 sehingga menjadi teorema Pythagoras.")])


# ============================================================ 8. SPLTV
def u8():
    def sys3():
        while True:
            x, y, z = nz(-5, 6), nz(-5, 6), nz(-5, 6)
            rows = [[nz(-3, 3), nz(-3, 3), nz(-3, 3)] for _ in range(3)]
            a = rows
            det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
            if det:
                break
        rhs = [r[0] * x + r[1] * y + r[2] * z for r in rows]
        sy = "<span class='sys'>%s</span>" % "<br>".join("%s = %s" % (expr([(r[0], "x"), (r[1], "y"), (r[2], "z")]), sn(c)) for r, c in zip(rows, rhs))
        return sy, x, y, z

    def solve():
        sy, x, y, z = sys3()
        w = ch(["x", "y", "z", "x + y + z", "xyz"])
        v = {"x": x, "y": y, "z": z, "x + y + z": x + y + z, "xyz": x * y * z}[w]
        return MN("Diketahui sistem persamaan %s. Nilai %s adalah …" % (sy, w), v, [v + 1, -v if v else 2, {"x": y, "y": z, "z": x, "x + y + z": x * y * z, "xyz": x + y + z}[w], v - 2],
                  "Eliminasi satu variabel dari dua pasang persamaan, selesaikan SPLDV-nya, lalu substitusi. Hasilnya x = %s, y = %s, z = %s." % (sn(x), sn(y), sn(z)))

    def cek():
        sy, x, y, z = sys3()
        t = lambda a, b, c: "(%s, %s, %s)" % (sn(a), sn(b), sn(c))
        return M("Himpunan penyelesaian sistem %s adalah …" % sy, "{%s}" % t(x, y, z), ["{%s}" % t(y, x, z) if x != y else "{%s}" % t(x, y, -z), "{%s}" % t(x, z, y) if y != z else "{%s}" % t(-x, y, z), "{%s}" % t(-x, -y, -z), "{%s}" % t(x + 1, y, z)],
                 "Substitusikan setiap pilihan; hanya %s yang memenuhi ketiga persamaan." % t(x, y, z))

    def mudah():
        x, y, z = ri(1, 9), ri(1, 9), ri(1, 9)
        k = ri(0, 1)
        if k == 0:
            sy = "<span class='sys'>x + y + z = %d<br>y + z = %d<br>z = %d</span>" % (x + y + z, y + z, z)
            return MN("Nilai x dari sistem %s adalah …" % sy, x, [y, x + y + z - z, z], "Dari bawah ke atas: z = %d, y = %d − %d = %d, x = %d − %d = %d." % (z, y + z, z, y, x + y + z, y + z, x))
        sy = "<span class='sys'>x + y = %d<br>y + z = %d<br>x + z = %d</span>" % (x + y, y + z, x + z)
        return MN("Nilai x + y + z dari sistem %s adalah …" % sy, x + y + z, [2 * (x + y + z), x + y + y + z, x + y + z + 1], "Jumlahkan ketiga persamaan: 2(x + y + z) = %d, jadi x + y + z = %d." % (2 * (x + y + z), x + y + z))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            a, b, c = ri(2, 9) * 1000, ri(1, 6) * 1000, ri(3, 12) * 500
            it = ch([("buku", "pensil", "penggaris"), ("apel", "jeruk", "mangga"), ("kopi", "teh", "roti")])
            return M("Harga 1 %s, 2 %s, dan 1 %s adalah %s. Harga 2 %s dan 1 %s adalah %s. Harga 1 %s dan 1 %s adalah %s. Harga 1 %s …" % (
                it[0], it[1], it[2], rp(a + 2 * b + c), it[0], it[1], rp(2 * a + b), it[1], it[2], rp(b + c), it[0]),
                rp(a), [rp(b), rp(c), rp(a + b)], "Misalkan harga %s = x, %s = y, %s = z, lalu selesaikan SPLTV: x = %s, y = %s, z = %s." % (it[0], it[1], it[2], rp(a), rp(b), rp(c)))
        if k == 1:
            x, y, z = ri(2, 9), ri(2, 9), ri(2, 9)
            return MN("Jumlah tiga bilangan %d. Bilangan pertama ditambah bilangan kedua sama dengan %d, dan bilangan kedua ditambah bilangan ketiga sama dengan %d. Bilangan pertama adalah …" % (x + y + z, x + y, y + z), x,
                      [y, z, x + y + z - (x + y)], "z = %d − %d = %d, y = %d − %d = %d, x = %d − %d = %d." % (x + y + z, x + y, z, y + z, z, y, x + y, y, x))
        a, b, c = ri(1, 9), ri(2, 9), ri(-9, 9)
        xs = [1, 2, 3]
        ys = [a * x * x + b * x + c for x in xs]
        return M("Grafik y = ax² + bx + c melalui titik (1, %s), (2, %s), dan (3, %s). Nilai a + b + c adalah …" % tuple(sn(v) for v in ys), sn(a + b + c), [sn(a + b + c + 1), sn(ys[1]), sn(a * b * c) if a * b * c != a + b + c else sn(a + b)],
                 "Titik (1, %s) memberikan langsung a + b + c = %s." % (sn(ys[0]), sn(ys[0])))

    sets = [("SPLTV yang mudah", [(mudah, 20)]),
            ("Menyelesaikan SPLTV", [(solve, 20)]),
            ("Himpunan penyelesaian", [(cek, 20)]),
            ("Soal cerita", [(cerita, 20)]),
            ("Campuran", [(solve, 10), (cek, 5), (cerita, 5)])]
    return unit("sistem-persamaan-linear-tiga-variabel", "A", 8, "Sistem Persamaan Linear Tiga Variabel (SPLTV)", "SPLTV",
                "Peserta didik menyelesaikan sistem persamaan linear tiga variabel dan menggunakannya untuk memodelkan dan menyelesaikan masalah kontekstual.",
                "Latihan sistem persamaan linear tiga variabel (SPLTV) kelas 10 SMA: metode eliminasi dan substitusi, himpunan penyelesaian, sistem bentuk khusus, dan soal cerita harga barang. 100 soal dengan kunci jawaban.",
                "Tiga persamaan → SPLDV → satu variabel", "Eliminasi satu variabel dari dua pasang persamaan.", sets,
                ["SPLTV terdiri dari tiga persamaan linear dengan tiga variabel, misalnya x, y, dan z. Penyelesaiannya (x, y, z) memenuhi ketiga persamaan.",
                 "Langkah: eliminasi satu variabel (misalnya z) dari persamaan I dan II, lalu dari II dan III, sehingga didapat SPLDV. Selesaikan SPLDV, lalu substitusi untuk mencari z.",
                 "Jika sistemnya berbentuk x + y, y + z, x + z, jumlahkan ketiganya lebih dulu."],
                [("x + y + z = 6, y + z = 5, z = 3", ["y = 2, x = 1"], "(1, 2, 3)"),
                 ("x + y = 5, y + z = 7, x + z = 6", ["2(x + y + z) = 18", "x + y + z = 9"], "x = 2, y = 3, z = 4")],
                [["Mengeliminasi variabel yang berbeda pada dua pasangan", "Eliminasi variabel yang sama dari kedua pasangan"],
                 ["Berhenti setelah mendapat dua variabel", "Substitusi lagi untuk mencari variabel ketiga"],
                 ["Tidak memeriksa jawaban", "Masukkan (x, y, z) ke ketiga persamaan"]],
                [("Apakah SPLTV selalu punya satu penyelesaian?", "Tidak selalu. Bisa tidak punya penyelesaian atau punya tak hingga banyak penyelesaian."),
                 ("Metode apa yang paling mudah?", "Biasanya gabungan eliminasi dan substitusi. Pilih variabel yang koefisiennya paling mudah disamakan."),
                 ("Di mana SPLTV dipakai?", "Untuk menghitung harga beberapa barang, mencampur bahan, dan menentukan persamaan parabola dari tiga titik.")])


# ============================================================ 9. SPtLDV dan program linear
def u9():
    def titik():
        a, b, c = ri(1, 5), ri(1, 5), ri(6, 20)
        d, e, f = ri(1, 5), ri(1, 5), ri(6, 20)
        sy = "<span class='sys'>%s ≤ %d<br>%s ≤ %d<br>x ≥ 0, y ≥ 0</span>" % (expr([(a, "x"), (b, "y")]), c, expr([(d, "x"), (e, "y")]), f)
        ok = lambda x, y: a * x + b * y <= c and d * x + e * y <= f and x >= 0 and y >= 0
        pts = [(x, y) for x in range(0, 9) for y in range(0, 9)]
        good = [p for p in pts if ok(*p) and p != (0, 0)]
        bad = [p for p in pts if not ok(*p)] + [(-1, 1), (1, -1)]
        if not good or len(bad) < 3:
            return None
        g = ch(good)
        bs = sh(bad)[:3]
        f_ = lambda p: "(%s, %s)" % (sn(p[0]), sn(p[1]))
        return M("Titik yang memenuhi sistem pertidaksamaan %s adalah …" % sy, f_(g), [f_(p) for p in bs], "Substitusikan %s: %d ≤ %d dan %d ≤ %d, dan keduanya tidak negatif." % (f_(g), a * g[0] + b * g[1], c, d * g[0] + e * g[1], f))

    def garis():
        p, q = ri(2, 8), ri(2, 8)
        s = ch(["≤", "≥"])
        g = math.gcd(p, q)
        pic = kosy(lines=[(Fr(-q, p), q, BLUE, "")], pts=[(p, 0, ""), (0, q, "")], lo=-1, hi=9, label="garis pada bidang koordinat")
        c = "%s %s %d" % (expr([(q // g, "x"), (p // g, "y")]), "≤" if s == "≤" else "≥", p * q // g)
        side = "memuat titik O(0, 0)" if s == "≤" else "tidak memuat titik O(0, 0)"
        return M("Garis pada gambar melalui (%d, 0) dan (0, %d). Pertidaksamaan untuk daerah yang %s adalah …" % (p, q, side) + pic, c,
                 ["%s %s %d" % (expr([(q // g, "x"), (p // g, "y")]), "≥" if s == "≤" else "≤", p * q // g), "%s %s %d" % (expr([(p // g, "x"), (q // g, "y")]), s, p * q // g) if p != q else "%s %s %d" % (expr([(q // g, "x"), (p // g, "y")]), s, p + q), "%s %s %d" % (expr([(q, "x"), (p, "y")]), s, p + q)],
                 "Persamaan garis: x/%d + y/%d = 1, yaitu %s. Uji titik O: 0 %s %d, jadi tandanya %s." % (p, q, "%s = %d" % (expr([(q // g, "x"), (p // g, "y")]), p * q // g), "≤" if s == "≤" else "≥", p * q // g, s))

    def region():
        while True:
            a, b, c = ri(1, 4), ri(1, 4), 0
            d, e = ri(1, 4), ri(1, 4)
            if a * e == b * d:
                continue
            x0, y0 = ri(1, 6), ri(1, 6)
            c, f = a * x0 + b * y0, d * x0 + e * y0
            xa, ya = Fr(c, a), Fr(c, b)
            xb, yb = Fr(f, d), Fr(f, e)
            verts = [(0, 0)]
            verts.append((min(xa, xb), 0))
            verts.append((0, min(ya, yb)))
            verts.append((x0, y0))
            if all(Fr(v[0]).denominator == 1 and Fr(v[1]).denominator == 1 for v in verts) and (xa < xb) != (ya < yb):
                break
        return a, b, c, d, e, f, verts

    def pojok():
        a, b, c, d, e, f, verts = region()
        sy = "<span class='sys'>%s ≤ %d<br>%s ≤ %d<br>x ≥ 0, y ≥ 0</span>" % (expr([(a, "x"), (b, "y")]), c, expr([(d, "x"), (e, "y")]), f)
        x0, y0 = verts[3]
        return M("Titik potong kedua garis batas pada sistem %s adalah …" % sy, "(%d, %d)" % (x0, y0), ["(%d, %d)" % (y0, x0) if x0 != y0 else "(%d, %d)" % (x0 + 1, y0), "(%d, 0)" % c, "(0, %d)" % f, "(%d, %d)" % (x0 + 1, y0 - 1)],
                 "Selesaikan %s = %d dan %s = %d: x = %d, y = %d." % (expr([(a, "x"), (b, "y")]), c, expr([(d, "x"), (e, "y")]), f, x0, y0))

    def optimum():
        a, b, c, d, e, f, verts = region()
        p, q = ri(1, 9), ri(1, 9)
        vals = {v: p * v[0] + q * v[1] for v in verts}
        mx = max(vals.values())
        if list(vals.values()).count(mx) > 1:
            return None
        sy = "<span class='sys'>%s ≤ %d<br>%s ≤ %d<br>x ≥ 0, y ≥ 0</span>" % (expr([(a, "x"), (b, "y")]), c, expr([(d, "x"), (e, "y")]), f)
        return MN("Nilai maksimum f(x, y) = %s pada daerah penyelesaian %s adalah …" % (expr([(p, "x"), (q, "y")]), sy), mx, sorted(set(vals.values()) - {mx}) + [mx + p],
                  "Uji titik pojok %s. Nilai terbesar %d." % (", ".join("(%s, %s) → %d" % (sn(v[0]), sn(v[1]), vals[v]) for v in verts), mx))

    def model():
        k = ri(0, 2)
        if k == 0:
            m, t, s = ri(2, 5), ri(1, 4), ri(20, 60)
            n = ri(10, 30)
            return M("Tempat parkir hanya muat %d kendaraan. Luas tempat parkir %d m², mobil memerlukan %d m² dan motor %d m². Jika x banyak mobil dan y banyak motor, model matematikanya …" % (n, s * 5, s // 2 * 2 if False else 10, 2),
                     "x + y ≤ %d; 10x + 2y ≤ %d; x ≥ 0; y ≥ 0" % (n, s * 5), ["x + y ≥ %d; 10x + 2y ≥ %d; x ≥ 0; y ≥ 0" % (n, s * 5), "x + y ≤ %d; 2x + 10y ≤ %d; x ≥ 0; y ≥ 0" % (n, s * 5), "10x + y ≤ %d; x + 2y ≤ %d; x ≥ 0; y ≥ 0" % (n, s * 5)],
                     "Batas banyak kendaraan dan batas luas, keduanya memakai ≤.")
        if k == 1:
            a1, b1, a2, b2 = ri(1, 4), ri(1, 4), ri(1, 4), ri(1, 4)
            T, G = ri(10, 40), ri(10, 40)
            return M("Roti A memerlukan %d ons tepung dan %d ons gula, roti B memerlukan %d ons tepung dan %d ons gula. Tersedia %d ons tepung dan %d ons gula. Jika x roti A dan y roti B, model matematikanya …" % (a1, b1, a2, b2, T, G),
                     "%s ≤ %d; %s ≤ %d; x ≥ 0; y ≥ 0" % (expr([(a1, "x"), (a2, "y")]), T, expr([(b1, "x"), (b2, "y")]), G),
                     ["%s ≤ %d; %s ≤ %d; x ≥ 0; y ≥ 0" % (expr([(a1, "x"), (b1, "y")]), T, expr([(a2, "x"), (b2, "y")]), G), "%s ≥ %d; %s ≥ %d; x ≥ 0; y ≥ 0" % (expr([(a1, "x"), (a2, "y")]), T, expr([(b1, "x"), (b2, "y")]), G),
                      "%s ≤ %d; %s ≤ %d; x ≥ 0; y ≥ 0" % (expr([(a1, "x"), (a2, "y")]), G, expr([(b1, "x"), (b2, "y")]), T)],
                     "Setiap bahan memberi satu pertidaksamaan: kebutuhan tepung ≤ %d dan kebutuhan gula ≤ %d." % (T, G))
        a, b, c, d, e, f, verts = region()
        p, q = ri(2, 9) * 1000, ri(2, 9) * 1000
        vals = {v: p * v[0] + q * v[1] for v in verts}
        mx = max(vals.values())
        if list(vals.values()).count(mx) > 1:
            return None
        return M("Seorang pedagang membuat x kue A dan y kue B dengan syarat %s ≤ %d, %s ≤ %d, x ≥ 0, y ≥ 0. Keuntungan kue A %s dan kue B %s per buah. Keuntungan maksimum …" % (expr([(a, "x"), (b, "y")]), c, expr([(d, "x"), (e, "y")]), f, rp(p), rp(q)),
                 rp(mx), [rp(v) for v in sorted(set(vals.values()) - {mx})] + [rp(mx + p)], "Uji titik pojok; keuntungan terbesar %s." % rp(mx))

    sets = [("Titik pada daerah penyelesaian", [(titik, 20)]),
            ("Pertidaksamaan dari grafik", [(garis, 20)]),
            ("Titik pojok", [(pojok, 20)]),
            ("Nilai optimum", [(optimum, 20)]),
            ("Model matematika dan program linear", [(model, 20)])]
    return unit("sistem-pertidaksamaan-linear-dua-variabel", "A", 9, "Sistem Pertidaksamaan Linear Dua Variabel dan Program Linear", "SPtLDV dan Program Linear",
                "Peserta didik menyelesaikan sistem pertidaksamaan linear dua variabel secara grafik dan menggunakannya untuk memodelkan masalah optimasi (program linear).",
                "Latihan sistem pertidaksamaan linear dua variabel kelas 10 SMA: titik pada daerah penyelesaian, pertidaksamaan dari grafik, titik pojok, nilai maksimum, dan model matematika program linear. 100 soal dengan kunci jawaban.",
                "Nilai optimum ada di titik pojok", "Uji titik O(0, 0) untuk menentukan daerah.", sets,
                ["Daerah penyelesaian pertidaksamaan ax + by ≤ c adalah salah satu sisi garis ax + by = c. Uji titik O(0, 0): jika memenuhi, daerahnya yang memuat O.",
                 "Daerah penyelesaian sistem adalah irisan semua daerah. Titik pojok didapat dari perpotongan garis-garis batas.",
                 "Program linear: nilai maksimum atau minimum fungsi tujuan f(x, y) = px + qy selalu terjadi di salah satu titik pojok."],
                [("x + y ≤ 6, 2x + y ≤ 8, x, y ≥ 0. Titik pojok?", ["(0, 0), (4, 0), (0, 6)", "Potong: x = 2, y = 4"], "(0, 0), (4, 0), (2, 4), (0, 6)"),
                 ("f = 3x + 2y di titik pojok di atas, maksimum?", ["0, 12, 14, 12"], "14 di (2, 4)")],
                [["Titik pojok hanya titik potong dengan sumbu", "Titik potong kedua garis juga titik pojok"],
                 ["Tanda ≥ dan ≤ tertukar saat membuat model", "Batas persediaan memakai ≤, syarat paling sedikit memakai ≥"],
                 ["Nilai maksimum dicari di sembarang titik", "Hitung nilai di semua titik pojok, lalu bandingkan"]],
                [("Mengapa nilai optimum ada di titik pojok?", "Karena fungsi tujuan linear, nilainya terus naik atau turun searah, sehingga ekstremnya berada di ujung daerah."),
                 ("Apa itu fungsi tujuan?", "Fungsi yang ingin dimaksimumkan atau diminimumkan, misalnya keuntungan atau biaya."),
                 ("Mengapa ada syarat x ≥ 0 dan y ≥ 0?", "Karena banyak barang tidak mungkin negatif.")])


# ============================================================ 10. persamaan dan fungsi kuadrat
def u10():
    def susun():
        p, q = nz(-7, 7), nz(-7, 7)
        c = "x² %s = 0" % expr([(-(p + q), "x"), (p * q, "")]).replace("x", "x", 1) if False else expr([(1, "x²"), (-(p + q), "x"), (p * q, "")]) + " = 0"
        return M("Persamaan kuadrat yang akar-akarnya %s dan %s adalah …" % (sn(p), sn(q)), c,
                 [expr([(1, "x²"), (p + q, "x"), (p * q, "")]) + " = 0", expr([(1, "x²"), (-(p + q), "x"), (-p * q, "")]) + " = 0", expr([(1, "x²"), (-(p * q), "x"), (p + q, "")]) + " = 0"],
                 "x² − (x₁ + x₂)x + x₁x₂ = 0: jumlah akar %s, hasil kali %s." % (sn(p + q), sn(p * q)))

    def akar():
        p, q = nz(-6, 6), nz(-6, 6)
        a = ch([1, 1, 2])
        b, c = -a * (p + q), a * p * q
        e = expr([(a, "x²"), (b, "x"), (c, "")]) + " = 0"
        k = ri(0, 2)
        if k == 0:
            v = p * p + q * q
            return MN("Jika x₁ dan x₂ akar-akar persamaan %s, nilai x₁² + x₂² adalah …" % e, v, [(p + q) ** 2, (p + q) ** 2 + 2 * p * q, v + 1], "x₁² + x₂² = (x₁ + x₂)² − 2x₁x₂ = %s² − 2 × %s = %s." % (par(p + q), par(p * q), sn(v)))
        if k == 1:
            if p * q == 0:
                return None
            v = Fr(p + q, p * q)
            return M("Jika x₁ dan x₂ akar-akar persamaan %s, nilai 1/x₁ + 1/x₂ adalah …" % e, fq(v), [fq(Fr(p * q, p + q)) if p + q else "0", fq(-v) if v else "1", fq(Fr(1, p + q)) if p + q else fq(v + 1)],
                     "1/x₁ + 1/x₂ = (x₁ + x₂)/(x₁x₂) = %s/%s = %s." % (sn(p + q), par(p * q), fq(v)))
        r = p + 2
        s = q + 2
        return M("Akar-akar %s adalah x₁ dan x₂. Persamaan kuadrat baru yang akar-akarnya x₁ + 2 dan x₂ + 2 adalah …" % e, expr([(1, "x²"), (-(r + s), "x"), (r * s, "")]) + " = 0",
                 [expr([(1, "x²"), (-(p + q + 2), "x"), (p * q + 2, "")]) + " = 0", expr([(1, "x²"), (r + s, "x"), (r * s, "")]) + " = 0", expr([(1, "x²"), (-(r + s), "x"), (p * q, "")]) + " = 0"],
                 "Jumlah akar baru %s, hasil kali (x₁ + 2)(x₂ + 2) = %s." % (sn(r + s), sn(r * s)))

    def diskriminan():
        k = ri(0, 2)
        if k == 0:
            c = ri(1, 9) ** 2 * ch([1, 4]) if False else ri(1, 9) ** 2
            m = 2 * math.isqrt(c)
            return M("Nilai m agar persamaan x² + mx + %d = 0 mempunyai dua akar kembar adalah …" % c, "m = %d atau m = −%d" % (m, m), ["m = %d saja" % m, "m = %d atau m = −%d" % (c, c), "m = %d atau m = −%d" % (m // 2, m // 2)],
                     "Akar kembar jika D = 0: m² − 4 × %d = 0, m² = %d, m = ±%d." % (c, m * m, m))
        if k == 1:
            a, b = ri(1, 3), ri(2, 10)
            lim = Fr(b * b, 4 * a)
            return M("Persamaan %s + p = 0 mempunyai dua akar real berbeda jika …" % expr([(a, "x²"), (b, "x")]), "p &lt; %s" % fq(lim), ["p &gt; %s" % fq(lim), "p = %s" % fq(lim), "p &lt; %s" % fq(-lim)],
                     "D &gt; 0: %d − %dp &gt; 0, jadi p &lt; %s." % (b * b, 4 * a, fq(lim)))
        a = ch([1, 2, -1, -2])
        b = nz(-4, 4)
        c = ri(1, 9) * (1 if a > 0 else -1) + (b * b // (4 * a) if False else 0)
        D = b * b - 4 * a * c
        t = "definit positif" if a > 0 and D < 0 else ("definit negatif" if a < 0 and D < 0 else "tidak definit")
        return M("Fungsi f(x) = %s termasuk …" % expr([(a, "x²"), (b, "x"), (c, "")]), t, [x for x in ["definit positif", "definit negatif", "tidak definit", "fungsi linear"] if x != t],
                 "a = %s dan D = %s. Definit positif jika a &gt; 0 dan D &lt; 0; definit negatif jika a &lt; 0 dan D &lt; 0." % (sn(a), sn(D)))

    def fungsi():
        p, q = ri(-4, 4), ri(-8, 8)
        a = nz(-3, 3)
        x1 = p + ch([1, 2, -1, -2])
        y1 = a * (x1 - p) ** 2 + q
        b, c = -2 * a * p, a * p * p + q
        F = lambda aa, bb, cc: "f(x) = %s" % expr([(aa, "x²"), (bb, "x"), (cc, "")])
        return M("Fungsi kuadrat dengan titik puncak (%s, %s) dan melalui titik (%s, %s) adalah …" % (sn(p), sn(q), sn(x1), sn(y1)), F(a, b, c),
                 [F(-a, -b, -c + 2 * q) if F(-a, -b, -c + 2 * q) != F(a, b, c) else F(a, -b, c), F(a, 2 * a * p, a * p * p + q) if p else F(a, b, c + 1), F(a, b, c + 2 * q) if q else F(a, b, c - 1)],
                 "f(x) = a(x − %s)² + %s. Substitusi (%s, %s): a = %s. Hasilnya %s." % (par(p), par(q), sn(x1), sn(y1), sn(a), F(a, b, c)))

    def potong():
        a = ch([1, -1])
        b, c = nz(-6, 6), nz(-6, 6)
        m, n = nz(-4, 4), nz(-6, 6)
        D = (b - m) ** 2 - 4 * a * (c - n)
        t = "memotong di dua titik" if D > 0 else ("menyinggung parabola" if D == 0 else "tidak memotong parabola")
        return M("Garis y = %s dan parabola y = %s …" % (lin(m, n), expr([(a, "x²"), (b, "x"), (c, "")])), t, [x for x in ["memotong di dua titik", "menyinggung parabola", "tidak memotong parabola", "sejajar sumbu y"] if x != t],
                 "Samakan: %s = 0, D = %s. D &gt; 0 memotong, D = 0 menyinggung, D &lt; 0 tidak memotong." % (expr([(a, "x²"), (b - m, "x"), (c - n, "")]), sn(D)))

    sets = [("Menyusun persamaan kuadrat", [(susun, 20)]),
            ("Jumlah dan hasil kali akar", [(akar, 20)]),
            ("Diskriminan", [(diskriminan, 20)]),
            ("Menentukan fungsi kuadrat", [(fungsi, 20)]),
            ("Garis dan parabola", [(potong, 14), (diskriminan, 6)])]
    return unit("persamaan-dan-fungsi-kuadrat", "A", 10, "Persamaan dan Fungsi Kuadrat", "Persamaan dan Fungsi Kuadrat",
                "Peserta didik menganalisis persamaan dan fungsi kuadrat: jumlah dan hasil kali akar, diskriminan, menyusun persamaan kuadrat, menentukan fungsi kuadrat, serta kedudukan garis dan parabola.",
                "Latihan persamaan dan fungsi kuadrat kelas 10 SMA: menyusun persamaan kuadrat dari akar-akarnya, jumlah dan hasil kali akar, diskriminan, definit, menentukan fungsi kuadrat, serta garis dan parabola. 100 soal dengan kunci jawaban.",
                "x₁ + x₂ = −b/a dan x₁x₂ = c/a", "D = b² − 4ac menentukan jenis akar.", sets,
                ["Untuk ax² + bx + c = 0: x₁ + x₂ = −b/a dan x₁x₂ = c/a. Persamaan kuadrat dengan akar x₁ dan x₂: x² − (x₁ + x₂)x + x₁x₂ = 0.",
                 "Diskriminan D = b² − 4ac: D &gt; 0 dua akar real berbeda, D = 0 akar kembar, D &lt; 0 tidak ada akar real.",
                 "Fungsi kuadrat dengan puncak (p, q): f(x) = a(x − p)² + q. Kedudukan garis dan parabola ditentukan oleh D dari persamaan gabungannya."],
                [("Akar −2 dan 5. Persamaannya?", ["Jumlah 3, hasil kali −10"], "x² − 3x − 10 = 0"),
                 ("x² − 4x + 1 = 0. x₁² + x₂²?", ["(x₁ + x₂)² − 2x₁x₂ = 16 − 2"], "14")],
                [["x₁ + x₂ = b/a", "x₁ + x₂ = −b/a"],
                 ["x₁² + x₂² = (x₁ + x₂)²", "Kurangi 2x₁x₂"],
                 ["Akar kembar jika D &gt; 0", "Akar kembar jika D = 0"]],
                [("Apa itu fungsi definit positif?", "Fungsi kuadrat yang nilainya selalu positif untuk semua x, yaitu jika a &gt; 0 dan D &lt; 0."),
                 ("Bagaimana menentukan fungsi kuadrat dari titik puncak?", "Pakai f(x) = a(x − p)² + q, lalu cari a dari satu titik lain yang dilalui."),
                 ("Apa arti garis menyinggung parabola?", "Garis dan parabola bertemu di tepat satu titik, yaitu D = 0.")])


# ============================================================ 11. statistika data berkelompok
def u11():
    def tabel():
        lo = ch([10, 20, 30, 40, 50, 140, 150])
        p = ch([5, 10])
        k = ri(5, 6)
        fs = [ri(2, 12) for _ in range(k)]
        return lo, p, fs

    def html(lo, p, fs):
        rows = "".join("<tr><td>%d − %d</td><td>%d</td></tr>" % (lo + i * p, lo + (i + 1) * p - 1, f) for i, f in enumerate(fs))
        return "<table class='sn-table'><thead><tr><th>Nilai</th><th>Frekuensi</th></tr></thead><tbody>%s</tbody></table>" % rows

    def unsur():
        lo, p, fs = tabel()
        i = ri(0, len(fs) - 1)
        k = ri(0, 3)
        t = html(lo, p, fs)
        a, b = lo + i * p, lo + (i + 1) * p - 1
        if k == 0:
            return M("Tepi bawah kelas %d − %d pada tabel berikut adalah …" % (a, b) + t, dz(Fr(2 * a - 1, 2)), [str(a), dz(Fr(2 * b + 1, 2)), dz(Fr(a + b, 2))], "Tepi bawah = batas bawah − 0,5 = %s." % dz(Fr(2 * a - 1, 2)))
        if k == 1:
            return M("Titik tengah kelas %d − %d pada tabel berikut adalah …" % (a, b) + t, dz(Fr(a + b, 2)), [dz(Fr(2 * a - 1, 2)), str(b), str(a + p)], "Titik tengah = (%d + %d) : 2 = %s." % (a, b, dz(Fr(a + b, 2))))
        if k == 2:
            return MN("Panjang kelas (interval) pada tabel berikut adalah …" + t, p, [p - 1, p + 1, len(fs)], "Panjang kelas = %s − %s = %d." % (dz(Fr(2 * a + 2 * p - 1, 2)), dz(Fr(2 * a - 1, 2)), p))
        fk = sum(fs[:i + 1])
        return MN("Frekuensi kumulatif kurang dari %s pada tabel berikut adalah …" % dz(Fr(2 * b + 1, 2)) + t, fk, [fs[i], fk - fs[i] if fk - fs[i] else fk + 1, sum(fs) - fk if sum(fs) - fk != fk else fk + 2], "Jumlahkan frekuensi sampai kelas %d − %d: %d." % (a, b, fk))

    def mean():
        lo, p, fs = tabel()
        mids = [Fr(2 * (lo + i * p) + p - 1, 2) for i in range(len(fs))]
        n = sum(fs)
        m = sum(f * x for f, x in zip(fs, mids)) / n
        if not S.endlich(m) or len(dz(m).split(",")[-1]) > 2 and "," in dz(m):
            return None
        return MD("Rata-rata data pada tabel berikut adalah …" + html(lo, p, fs), m, [sum(mids) / len(mids), m + p, m - Fr(1, 2)], "x̄ = Σfᵢxᵢ / Σf = %s / %d = %s, dengan xᵢ titik tengah kelas." % (dz(sum(f * x for f, x in zip(fs, mids))), n, dz(m)))

    def median():
        lo, p, fs = tabel()
        n = sum(fs)
        half = Fr(n, 2)
        cum = 0
        for i, f in enumerate(fs):
            if cum + f >= half:
                break
            cum += f
        L = Fr(2 * (lo + i * p) - 1, 2)
        v = L + (half - cum) / f * p
        if not S.endlich(v) or ("," in dz(v) and len(dz(v).split(",")[1]) > 2):
            return None
        return MD("Median data pada tabel berikut adalah …" + html(lo, p, fs), v, [L + p / 2, L + (half - cum) / n * p if L + (half - cum) / n * p != v and S.endlich(L + (half - cum) / n * p) else v + 1, v + p],
                  "Kelas median ke-%d (data ke-%s). Me = L + ((n/2 − F)/f) × p = %s + ((%s − %d)/%d) × %d = %s." % (i + 1, dz(half), dz(L), dz(half), cum, f, p, dz(v)))

    def modus():
        lo, p, fs = tabel()
        i = fs.index(max(fs))
        if fs.count(max(fs)) > 1 or i == 0 or i == len(fs) - 1:
            return None
        d1, d2 = fs[i] - fs[i - 1], fs[i] - fs[i + 1]
        L = Fr(2 * (lo + i * p) - 1, 2)
        v = L + Fr(d1, d1 + d2) * p
        if not S.endlich(v) or ("," in dz(v) and len(dz(v).split(",")[1]) > 2):
            return None
        return MD("Modus data pada tabel berikut adalah …" + html(lo, p, fs), v, [L + Fr(d2, d1 + d2) * p if d1 != d2 else v + 1, Fr(2 * (lo + i * p) + p - 1, 2) if Fr(2 * (lo + i * p) + p - 1, 2) != v else v + 2, v + p],
                  "Kelas modus %d − %d. Mo = L + (d₁/(d₁ + d₂)) × p = %s + (%d/%d) × %d = %s." % (lo + i * p, lo + (i + 1) * p - 1, dz(L), d1, d1 + d2, p, dz(v)))

    def kuartil():
        lo, p, fs = tabel()
        n = sum(fs)
        if n % 4:
            return None
        w = ch([1, 3])
        pos = Fr(w * n, 4)
        cum = 0
        for i, f in enumerate(fs):
            if cum + f >= pos:
                break
            cum += f
        L = Fr(2 * (lo + i * p) - 1, 2)
        v = L + (pos - cum) / f * p
        if not S.endlich(v) or ("," in dz(v) and len(dz(v).split(",")[1]) > 2):
            return None
        return MD("Kuartil %s (Q%s) data pada tabel berikut adalah …" % ("bawah" if w == 1 else "atas", sub(w)) + html(lo, p, fs), v, [L + p / 2, v + p, v - Fr(p, 2)],
                  "Letak Q%s = data ke-%s. Q%s = %s + ((%s − %d)/%d) × %d = %s." % (sub(w), dz(pos), sub(w), dz(L), dz(pos), cum, f, p, dz(v)))

    sets = [("Unsur tabel distribusi frekuensi", [(unsur, 20)]),
            ("Rata-rata data berkelompok", [(mean, 20)]),
            ("Median data berkelompok", [(median, 20)]),
            ("Modus data berkelompok", [(modus, 20)]),
            ("Kuartil data berkelompok", [(kuartil, 20)])]
    return unit("statistika-data-berkelompok", "D", 11, "Statistika: Ukuran Pemusatan dan Letak Data Berkelompok", "Statistika Data Berkelompok",
                "Peserta didik menyajikan data dalam tabel distribusi frekuensi dan menentukan ukuran pemusatan (rata-rata, median, modus) serta ukuran letak (kuartil) data berkelompok.",
                "Latihan statistika data berkelompok kelas 10 SMA: tepi kelas, titik tengah, panjang kelas, frekuensi kumulatif, rata-rata, median, modus, dan kuartil dari tabel distribusi frekuensi. 100 soal dengan kunci jawaban.",
                "Me = L + ((n/2 − F)/f) × p", "L: tepi bawah, F: frekuensi kumulatif sebelum kelas.", sets,
                ["Pada tabel distribusi frekuensi, tepi bawah = batas bawah − 0,5, titik tengah = (batas bawah + batas atas)/2, dan panjang kelas p = selisih dua tepi bawah berurutan.",
                 "Rata-rata: x̄ = Σfᵢxᵢ/Σf dengan xᵢ titik tengah kelas.",
                 "Median dan kuartil: cari kelasnya dengan frekuensi kumulatif, lalu Qᵢ = L + ((i·n/4 − F)/f) × p. Modus: Mo = L + (d₁/(d₁ + d₂)) × p."],
                [("Kelas median 60 − 69, n = 40, F = 15, f = 10.", ["L = 59,5, n/2 = 20", "59,5 + (5/10) × 10"], "64,5"),
                 ("Kelas modus 70 − 79, d₁ = 4, d₂ = 6.", ["69,5 + (4/10) × 10"], "73,5")],
                [["L memakai batas bawah (60)", "L memakai tepi bawah (59,5)"],
                 ["F adalah frekuensi kelas median", "F adalah frekuensi kumulatif sebelum kelas median"],
                 ["Rata-rata memakai batas bawah kelas", "Rata-rata memakai titik tengah kelas"]],
                [("Mengapa memakai tepi kelas, bukan batas kelas?", "Karena data kontinu: kelas 60 − 69 sebenarnya mencakup 59,5 sampai 69,5."),
                 ("Apa itu frekuensi kumulatif?", "Jumlah frekuensi dari kelas pertama sampai kelas tertentu."),
                 ("Apakah hasil dari data berkelompok tepat?", "Hasilnya perkiraan, karena data asli di dalam setiap kelas tidak diketahui.")])


# ============================================================ 12. peluang
def u12():
    def kartu():
        F = [("kartu As atau kartu King", 8), ("kartu hati atau kartu wajik", 26), ("kartu merah atau kartu As", 28), ("kartu hati atau kartu As", 16),
             ("kartu King atau kartu Queen atau kartu Jack", 12), ("kartu sekop atau kartu bergambar (J, Q, K)", 22), ("kartu bernomor 10 atau kartu hitam", 28), ("kartu As merah", 2),
             ("kartu bergambar (J, Q, K)", 12), ("kartu keriting bernomor genap (2 sampai 10)", 5), ("kartu hati bergambar (J, Q, K)", 3), ("bukan kartu As", 48),
             ("kartu bernomor 7", 4), ("kartu merah", 26), ("kartu sekop", 13), ("kartu King hitam", 2), ("kartu wajik atau kartu Queen", 16), ("kartu bernomor prima (2, 3, 5, 7)", 16)]
        t, n = ch(F)
        v = Fr(n, 52)
        return M("Satu kartu diambil acak dari seperangkat kartu bridge (52 kartu). Peluang terambil %s adalah …" % t, fq(v), [fq(Fr(n + 1, 52)), fq(Fr(n, 13)) if n <= 13 else fq(1 - v), fq(Fr(n, 26)) if n <= 26 and Fr(n, 26) != v else fq(Fr(n - 1, 52))],
                 "Ada %d kartu yang memenuhi dari 52 kartu. P = %d/52 = %s." % (n, n, fq(v)))

    def lepas():
        F = [("jumlah mata dadu 5 atau 9", 4 + 4), ("jumlah mata dadu 7 atau 11", 6 + 2), ("jumlah mata dadu 3 atau 10", 2 + 3), ("jumlah mata dadu 2 atau 12", 2), ("jumlah mata dadu kurang dari 4 atau lebih dari 10", 3 + 3),
             ("jumlah mata dadu 6 atau 8", 5 + 5), ("kedua mata dadu sama atau jumlahnya 7", 6 + 6), ("jumlah mata dadu 4 atau 6", 3 + 5), ("jumlah mata dadu 8 atau 10", 5 + 3), ("jumlah mata dadu 9 atau 11", 4 + 2)]
        t, n = ch(F)
        v = Fr(n, 36)
        return M("Dua dadu dilempar bersama. Peluang muncul %s adalah …" % t, fq(v), [fq(Fr(n, 12)), fq(Fr(n + 1, 36)), fq(1 - v)], "Kedua kejadian saling lepas: P(A ∪ B) = P(A) + P(B) = %d/36 = %s." % (n, fq(v)))

    def gabung():
        n = ri(10, 40)
        a, b = ch([(2, 3), (2, 5), (3, 5), (3, 4), (4, 6), (2, 7)])
        A = n // a
        B = n // b
        AB = n // (a * b // math.gcd(a, b))
        v = Fr(A + B - AB, n)
        return M("Dari kartu bernomor 1 sampai %d diambil satu kartu. Peluang terambil kelipatan %d atau kelipatan %d adalah …" % (n, a, b), fq(v), [fq(Fr(A + B, n)), fq(Fr(AB, n)), fq(Fr(A * B, n * n))],
                 "P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = (%d + %d − %d)/%d = %s." % (A, B, AB, n, fq(v)))

    def bebas():
        k = ri(0, 2)
        if k == 0:
            a, b = ch([("muncul angka", Fr(1, 2)), ("muncul gambar", Fr(1, 2))]), ch([("mata dadu genap", Fr(1, 2)), ("mata dadu prima", Fr(1, 2)), ("mata dadu 6", Fr(1, 6)), ("mata dadu kurang dari 3", Fr(1, 3)), ("mata dadu kelipatan 3", Fr(1, 3))])
            v = a[1] * b[1]
            return M("Sebuah koin dan sebuah dadu dilempar bersama. Peluang koin %s dan %s adalah …" % (a[0], b[0]), fq(v), [fq(a[1] + b[1]) if a[1] + b[1] < 1 else fq(Fr(2, 3)), fq(b[1]), fq(v * 2)], "Saling bebas: P(A ∩ B) = P(A) × P(B) = %s × %s = %s." % (fq(a[1]), fq(b[1]), fq(v)))
        if k == 1:
            m, b = ri(2, 8), ri(2, 8)
            n = m + b
            v = Fr(m, n) * Fr(b, n)
            return M("Kotak A berisi %d bola merah dan %d bola putih; kotak B juga berisi %d bola merah dan %d bola putih. Dari setiap kotak diambil satu bola. Peluang terambil merah dari A dan putih dari B …" % (m, b, m, b), fq(v),
                     [fq(Fr(m, n) * Fr(b, n - 1)), fq(Fr(m + b, 2 * n)), fq(Fr(m, n) * Fr(m, n))], "%d/%d × %d/%d = %s." % (m, n, b, n, fq(v)))
        p, q = ch([Fr(3, 4), Fr(2, 3), Fr(4, 5), Fr(9, 10), Fr(3, 5)]), ch([Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(4, 5), Fr(5, 6)])
        v = 1 - (1 - p) * (1 - q)
        return M("Peluang Andi menembak tepat sasaran %s dan peluang Budi %s. Jika keduanya menembak sekali, peluang sasaran terkena paling sedikit sekali …" % (fq(p), fq(q)), fq(v), [fq(p * q), fq((1 - p) * (1 - q)), fq(p + q - 1) if p + q - 1 > 0 else fq(Fr(1, 2))],
                 "P = 1 − P(keduanya meleset) = 1 − %s × %s = %s." % (fq(1 - p), fq(1 - q), fq(v)))

    def harapan():
        k = ri(0, 2)
        if k == 0:
            n = ch([72, 108, 144, 180, 360])
            F = [("jumlah mata dadu 7", 6), ("jumlah mata dadu 10", 3), ("mata dadu kembar", 6), ("jumlah mata dadu kurang dari 5", 6), ("jumlah mata dadu 11", 2)]
            t, c = ch(F)
            return MN("Dua dadu dilempar %d kali. Frekuensi harapan muncul %s adalah …" % (n, t), n * c // 36, [n * c // 6 if n * c // 6 != n * c // 36 else n // 2, n // 6, n * c // 18], "P = %d/36. Fh = %d/36 × %d = %d kali." % (c, c, n, n * c // 36), unit="kali")
        if k == 1:
            n = ch([40, 80, 120, 160])
            return MN("Tiga koin dilempar %d kali. Frekuensi harapan muncul tepat dua gambar …" % n, n * 3 // 8, [n // 8, n // 2, n * 2 // 3 if n % 3 == 0 else n // 4], "P(tepat dua gambar) = 3/8. Fh = 3/8 × %d = %d kali." % (n, n * 3 // 8), unit="kali")
        p = ch([Fr(1, 20), Fr(1, 25), Fr(2, 25), Fr(3, 100), Fr(1, 50)])
        N = p.denominator * ri(10, 60)
        return MN("Peluang seorang bayi terkena demam setelah imunisasi adalah %s. Dari %s bayi yang diimunisasi, perkiraan yang demam …" % (dz(p), num(N)), p * N, [N - p * N, p * N * 10, p * N + 10], "%s × %s = %s bayi." % (dz(p), num(N), num(int(p * N))), unit="bayi")

    sets = [("Peluang pada kartu bridge", [(kartu, 14), (gabung, 6)]),
            ("Kejadian saling lepas", [(lepas, 10), (gabung, 10)]),
            ("Kejadian tidak saling lepas", [(gabung, 20)]),
            ("Kejadian saling bebas", [(bebas, 20)]),
            ("Frekuensi harapan", [(harapan, 20)])]
    return unit("peluang-kejadian-saling-lepas-dan-saling-bebas", "D", 12, "Peluang Kejadian Majemuk: Saling Lepas dan Saling Bebas", "Peluang Saling Lepas dan Saling Bebas",
                "Peserta didik menentukan peluang kejadian majemuk (saling lepas, tidak saling lepas, saling bebas) dan frekuensi harapan untuk menyelesaikan masalah.",
                "Latihan peluang kelas 10 SMA: peluang pada kartu bridge, kejadian saling lepas, kejadian tidak saling lepas (P(A ∪ B)), kejadian saling bebas (P(A ∩ B)), dan frekuensi harapan. 100 soal dengan kunci jawaban.",
                "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)", "Saling bebas: P(A ∩ B) = P(A) × P(B).", sets,
                ["Dua kejadian saling lepas jika tidak dapat terjadi bersamaan: P(A ∪ B) = P(A) + P(B).",
                 "Jika tidak saling lepas, kurangi irisannya: P(A ∪ B) = P(A) + P(B) − P(A ∩ B).",
                 "Dua kejadian saling bebas jika yang satu tidak memengaruhi yang lain: P(A ∩ B) = P(A) × P(B). Frekuensi harapan = P(A) × banyak percobaan."],
                [("Kartu bridge: As atau hati?", ["4/52 + 13/52 − 1/52"], "16/52 = 4/13"),
                 ("Koin dan dadu: gambar dan mata 6?", ["½ × 1/6"], "1/12")],
                [["P(As atau hati) = 4/52 + 13/52", "As hati dihitung dua kali, kurangi 1/52"],
                 ["Saling bebas dihitung dengan menjumlahkan", "Kejadian saling bebas dikalikan"],
                 ["Saling lepas dan saling bebas dianggap sama", "Saling lepas: tidak bisa bersamaan. Saling bebas: tidak saling memengaruhi"]],
                [("Ada berapa kartu dalam kartu bridge?", "52 kartu: 4 jenis (hati, wajik, keriting, sekop), masing-masing 13 kartu (As, 2–10, J, Q, K)."),
                 ("Apa beda saling lepas dan saling bebas?", "Saling lepas berarti tidak ada irisan. Saling bebas berarti terjadinya satu kejadian tidak mengubah peluang kejadian lain."),
                 ("Apa itu peluang komplemen?", "P(bukan A) = 1 − P(A). Cara ini memudahkan soal “paling sedikit satu”.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12]
