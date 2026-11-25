# -*- coding: utf-8 -*-
"""Indonesia / Matematika / Kelas 9 (SMP, Fase D)。python3 tools/id_smp.py 9 [番号…]"""
import math
from fractions import Fraction as Fr
import id_smp as S
from id_smp import (ri, ch, nz, sh, num, sn, par, pd, dz, fq, expr, lin, sup, pw, M, MN, MD, rp, NB, MINUS,
                    kosy, kurve, figure, poly_ang, tab, unit, fig, wrap, text, line, INK, BLUE, RED, FILL, GREEN)


def rt(n):
    """√n disederhanakan: (a, b) dengan a√b"""
    a, b = 1, n
    for f in range(int(math.isqrt(n)), 1, -1):
        if n % (f * f) == 0:
            a, b = f, n // (f * f)
            break
    return a, b


def surd(a, b):
    """a√b sebagai teks"""
    if b == 1:
        return sn(a)
    if a == 1:
        return "√%d" % b
    if a == -1:
        return "−√%d" % b
    return "%s√%d" % (sn(a), b)


# ============================================================ 1. bentuk akar
def u1():
    SQF = [2, 3, 5, 6, 7, 10, 11]

    def sederhana():
        a, b = ri(2, 9), ch(SQF)
        n = a * a * b
        return M("Bentuk sederhana dari √%d adalah …" % n, surd(a, b), [surd(b, a) if a not in SQF or True else None, surd(a * a, b), surd(a + 1, b), surd(1, n // 2) if n % 2 == 0 else surd(a - 1, b)],
                 "√%d = √(%d × %d) = %d√%d." % (n, a * a, b, a, b))

    def tambah():
        b = ch(SQF)
        p, q = ri(2, 6), ri(2, 6)
        k = ri(0, 2)
        if k == 0:
            a1, a2 = nz(-9, 9), nz(-9, 9)
            v = a1 + a2
            if v == 0:
                return None
            return M("Hasil dari %s %s %s adalah …" % (surd(a1, b), "+" if a2 > 0 else MINUS, surd(abs(a2), b)), surd(v, b), [surd(v, 2 * b), surd(a1 * a2, b), surd(a1 - a2, b) if a1 - a2 else surd(v + 1, b)],
                     "Akar sejenis dijumlahkan koefisiennya: %s + %s = %s, jadi %s." % (sn(a1), par(a2), sn(v), surd(v, b)))
        n1, n2 = p * p * b, q * q * b
        op = ch(["+", "−"])
        v = p + q if op == "+" else p - q
        if v == 0:
            return None
        return M("Hasil dari √%d %s √%d adalah …" % (n1, op, n2), surd(v, b), ["√%d" % (n1 + n2 if op == "+" else abs(n1 - n2)), surd(v, 2 * b), surd(p * q, b)],
                 "√%d = %s dan √%d = %s, jadi hasilnya %s." % (n1, surd(p, b), n2, surd(q, b), surd(v, b)))

    def kali():
        k = ri(0, 2)
        if k == 0:
            a, b = ch(SQF), ch(SQF)
            p, q = ri(1, 6), ri(1, 6)
            n = a * b
            c, d = rt(n)
            v = surd(p * q * c, d)
            return M("Hasil dari %s × %s adalah …" % (surd(p, a), surd(q, b)), v, [surd(p * q, a + b), surd(p + q, n), surd(p * q, n) if c != 1 else surd(p * q + 1, n)],
                     "Kalikan koefisien dan bilangan di dalam akar: %s." % (("%d√%d = %s" % (p * q, n, v)) if c != 1 else v))
        if k == 1:
            a, b = ch(SQF), ch(SQF)
            if a == b:
                return None
            q = ri(1, 4)
            p = q * ri(1, 6)
            v = surd(p // q, a)
            return M("Hasil dari %s : %s adalah …" % (surd(p, a * b), surd(q, b)), v, [surd(p // q, a * b), surd(p * q, a), surd(p // q, b)],
                     "Bagi koefisien (%d : %d = %d) dan bilangan di dalam akar (%d : %d = %d): %s." % (p, q, p // q, a * b, b, a, v))
        a = ch(SQF)
        p = ri(2, 9)
        v = p * p * a
        return MN("Hasil dari (%s)² adalah …" % surd(p, a), v, [p * a, p * p + a, 2 * p * a], "(%d√%d)² = %d² × %d = %s." % (p, a, p, a, num(v)))

    def rasional():
        b = ch(SQF)
        a = ri(1, 12)
        k = ri(0, 1)
        if k == 0:
            g = math.gcd(a, b)
            v = Fr(a, b)
            c = (S.fr("%s√%d" % ("" if v.numerator == 1 else str(v.numerator), b), v.denominator) if v.denominator != 1 else surd(v.numerator, b))
            return M("Bentuk rasional dari %s adalah …" % S.fr(a, "√%d" % b), c, [S.fr("%d√%d" % (a, b), b * b) if True else None, S.fr(a, b), S.fr("√%d" % b, a) if a != 1 else S.fr("√%d" % b, 2)],
                     "Kalikan dengan %s: %s × %s = %s." % (S.fr("√%d" % b, "√%d" % b), S.fr(a, "√%d" % b), S.fr("√%d" % b, "√%d" % b), c))
        c1 = ri(2, 6)
        if c1 * c1 == b:
            return None
        den = c1 * c1 - b
        if den == 0:
            return None
        num_ = a
        v = Fr(num_, den)
        top = "%s(%d − √%d)" % ("" if v == 1 else fq(v), c1, b) if v.denominator == 1 else None
        if top is None:
            return None
        return M("Bentuk rasional dari %s adalah …" % S.fr(a, "%d + √%d" % (c1, b)), top, ["%s(%d + √%d)" % ("" if v == 1 else fq(v), c1, b), "%s(%d − √%d)" % (fq(Fr(a, c1 * c1 + b)), c1, b), "%s(√%d − %d)" % ("" if v == 1 else fq(v), b, c1)],
                 "Kalikan dengan sekawannya (%d − √%d): penyebut menjadi %d − %d = %d." % (c1, b, c1 * c1, b, den)) if den > 0 else None

    def banding():
        a, b = ri(2, 9), ch(SQF)
        c, d = ri(2, 9), ch(SQF)
        x, y = a * a * b, c * c * d
        if x == y:
            return None
        A, B = surd(a, b), surd(c, d)
        k = ri(0, 1)
        if k == 0:
            cc = "%s &lt; %s" % (A, B) if x < y else "%s &gt; %s" % (A, B)
            return M("Mana yang benar untuk %s dan %s?" % (A, B), cc, ["%s &gt; %s" % (A, B) if x < y else "%s &lt; %s" % (A, B), "%s = %s" % (A, B), "Tidak dapat dibandingkan"],
                     "Masukkan koefisien ke dalam akar: %s = √%d dan %s = √%d. Jadi %s." % (A, x, B, y, cc))
        n = ri(10, 150)
        r = math.isqrt(n)
        if r * r == n:
            return None
        return M("Nilai √%d terletak di antara …" % n, "%d dan %d" % (r, r + 1), ["%d dan %d" % (r - 1, r), "%d dan %d" % (r + 1, r + 2), "%d dan %d" % (n // 2, n // 2 + 1) if n // 2 != r else "%d dan %d" % (r + 2, r + 3)],
                 "%d² = %d dan %d² = %d, jadi %d &lt; √%d &lt; %d." % (r, r * r, r + 1, (r + 1) ** 2, r, n, r + 1))

    def pecahan():
        k = ri(0, 1)
        if k == 0:
            b = ri(2, 5)
            e = ch([2, 3])
            n = b ** (2 * e) if e == 2 else b ** 3
            if e == 2:
                n = b ** 4
                return MN("Nilai dari %d%s adalah …" % (n, sup("1/4") if False else "<sup>1/4</sup>"), b, [n // 4 if n % 4 == 0 else b + 1, b * b, b + 2], "%d<sup>1/4</sup> = ⁴√%d = %d, karena %d⁴ = %d." % (n, n, b, b, n))
            return MN("Nilai dari %d<sup>1/3</sup> adalah …" % n, b, [n // 3 if n % 3 == 0 and n // 3 != b else b + 1, b * b, b + 2], "%d<sup>1/3</sup> = ∛%d = %d, karena %d³ = %d." % (n, n, b, b, n))
        b = ri(2, 5)
        m, nn = ch([(2, 3), (3, 2), (2, 2)]) if False else ch([(3, 2), (2, 3)])
        base = b ** nn
        v = b ** m
        return MN("Nilai dari %d<sup>%d/%d</sup> adalah …" % (base, m, nn), v, [base * m // nn if base * m % nn == 0 and base * m // nn != v else v + 1, b ** (m + 1) if b ** (m + 1) != v else v * 2, b * m], "%d<sup>%d/%d</sup> = (%s√%d)%s = %d%s = %d." % (base, m, nn, "" if nn == 2 else "∛"[0:0] + str(nn), base, sup(m), b, sup(m), v) if False else
                  "%d<sup>%d/%d</sup> = (akar pangkat %d dari %d)%s = %d%s = %d." % (base, m, nn, nn, base, sup(m), b, sup(m), v))

    sets = [("Menyederhanakan bentuk akar", [(sederhana, 20)]),
            ("Penjumlahan dan pengurangan", [(tambah, 20)]),
            ("Perkalian bentuk akar", [(kali, 20)]),
            ("Merasionalkan penyebut", [(rasional, 20)]),
            ("Membandingkan dan pangkat pecahan", [(banding, 12), (pecahan, 8)])]
    return unit("bentuk-akar", "B", 1, "Bentuk Akar: Menyederhanakan, Operasi, dan Merasionalkan", "Bentuk Akar",
                "Peserta didik menyederhanakan bentuk akar, melakukan operasi pada bentuk akar, merasionalkan penyebut, dan menghubungkan bentuk akar dengan pangkat pecahan.",
                "Latihan bentuk akar kelas 9 SMP: menyederhanakan akar, menjumlahkan dan mengurangkan akar sejenis, perkalian akar, merasionalkan penyebut, membandingkan akar, dan pangkat pecahan. 100 soal dengan kunci jawaban.",
                "√(a × b) = √a × √b", "Akar sejenis dapat dijumlahkan: 2√3 + 5√3 = 7√3.", sets,
                ["Sederhanakan akar dengan mencari faktor kuadrat terbesar: √50 = √(25 × 2) = 5√2.",
                 "Hanya akar sejenis (bilangan di dalam akar sama) yang dapat dijumlahkan atau dikurangkan. Perkalian: a√b × c√d = ac√(bd).",
                 "Untuk merasionalkan a/√b, kalikan dengan √b/√b. Untuk a/(c + √b), kalikan dengan sekawannya (c − √b)/(c − √b)."],
                [("Sederhanakan √72.", ["72 = 36 × 2"], "6√2"),
                 ("Rasionalkan 6/√3.", ["6/√3 × √3/√3 = 6√3/3"], "2√3")],
                [["√2 + √3 = √5", "√2 + √3 tidak dapat disederhanakan"],
                 ["√18 = 9√2", "√18 = √(9 × 2) = 3√2"],
                 ["(2√3)² = 12√3", "(2√3)² = 4 × 3 = 12"]],
                [("Kapan bentuk akar disebut paling sederhana?", "Jika bilangan di dalam akar tidak lagi mempunyai faktor bilangan kuadrat selain 1, dan tidak ada akar di penyebut."),
                 ("Mengapa penyebut perlu dirasionalkan?", "Agar bentuknya baku dan mudah dihitung atau dibandingkan."),
                 ("Apa hubungan akar dengan pangkat pecahan?", "√a = a<sup>1/2</sup>, ∛a = a<sup>1/3</sup>, dan a<sup>m/n</sup> adalah akar pangkat n dari aᵐ.")])


# ============================================================ 2. persamaan kuadrat
def u2():
    def faktor():
        a, b = nz(-9, 9), nz(-9, 9)
        if a == b or a + b == 0 and ri(0, 1):
            return None
        e = expr([(1, "x²"), (-(a + b), "x"), (a * b, "")])
        c = "x = %s atau x = %s" % (sn(min(a, b)), sn(max(a, b)))
        ws = ["x = %s atau x = %s" % (sn(min(-a, -b)), sn(max(-a, -b))), "x = %s atau x = %s" % (sn(min(a, -b)), sn(max(a, -b))), "x = %s atau x = %s" % (sn(min(-a, b)), sn(max(-a, b)))]
        return M("Penyelesaian dari %s = 0 adalah …" % e, c, ws, "%s = (x %s %d)(x %s %d) = 0, jadi x = %s atau x = %s." % (e, "−" if a > 0 else "+", abs(a), "−" if b > 0 else "+", abs(b), sn(a), sn(b)))

    def kuadrat():
        k = ri(0, 2)
        if k == 0:
            a = ri(1, 12)
            return M("Penyelesaian dari x² = %d adalah …" % (a * a), "x = %d atau x = −%d" % (a, a), ["x = %d saja" % a, "x = %d atau x = −%d" % (a * a // 2, a * a // 2) if a > 1 else "x = 0", "x = %d atau x = −%d" % (a + 1, a + 1)],
                     "x = ±√%d = ±%d." % (a * a, a))
        if k == 1:
            a = ri(1, 9)
            return M("Penyelesaian dari x² − %d = 0 adalah …" % (a * a), "x = %d atau x = −%d" % (a, a), ["x = %d saja" % (a * a), "x = %d atau x = −%d" % (a * a, a * a), "x = %d saja" % a],
                     "x² = %d, jadi x = ±%d." % (a * a, a))
        a = nz(-9, 9)
        c = expr([(1, "x²"), (-a, "x")])
        return M("Penyelesaian dari %s = 0 adalah …" % c, "x = 0 atau x = %s" % sn(a), ["x = %s saja" % sn(a), "x = 0 atau x = %s" % sn(-a), "x = 1 atau x = %s" % sn(a)],
                 "%s = x(x %s %d) = 0, jadi x = 0 atau x = %s." % (c, "−" if a > 0 else "+", abs(a), sn(a)))

    def akar():
        a, b = nz(-9, 9), nz(-9, 9)
        e = expr([(1, "x²"), (-(a + b), "x"), (a * b, "")])
        k = ri(0, 1)
        if k == 0:
            return MN("Jumlah akar-akar persamaan %s = 0 adalah …" % e, a + b, [-(a + b), a * b, a + b + 1], "x₁ + x₂ = −b/a = %s." % sn(a + b))
        return MN("Hasil kali akar-akar persamaan %s = 0 adalah …" % e, a * b, [-(a * b), a + b, a * b + 1], "x₁ × x₂ = c/a = %s." % sn(a * b))

    def rumus():
        while True:
            a, b, c = nz(-4, 4), nz(-9, 9), nz(-12, 12)
            D = b * b - 4 * a * c
            if D > 0:
                break
        r = math.isqrt(D)
        k = ri(0, 1)
        if k == 0:
            return MN("Nilai diskriminan persamaan %s = 0 adalah …" % expr([(a, "x²"), (b, "x"), (c, "")]), D, [b * b + 4 * a * c, -D, b - 4 * a * c], "D = b² − 4ac = %s² − 4 × %s × %s = %s." % (par(b), par(a), par(c), sn(D)))
        e = expr([(a, "x²"), (b, "x"), (c, "")])
        n = "dua akar real berbeda" if D > 0 else ("dua akar real kembar" if D == 0 else "tidak mempunyai akar real")
        a2, b2, c2 = ch([(1, 2, 1), (1, -6, 9), (4, 4, 1), (1, 4, 4), (9, -6, 1)])
        cc2 = ri(1, 9)
        F = [(e, D, n), (expr([(a2, "x²"), (b2, "x"), (c2, "")]), b2 * b2 - 4 * a2 * c2, "dua akar real kembar"),
             (expr([(1, "x²"), (ri(1, 3), "x"), (cc2 + 5, "")]), None, "tidak mempunyai akar real")]
        q, _, ans = ch(F)
        return M("Persamaan %s = 0 mempunyai …" % q, ans, [x for x in ["dua akar real berbeda", "dua akar real kembar", "tidak mempunyai akar real", "tiga akar real"] if x != ans],
                 "Hitung D = b² − 4ac: D &gt; 0 dua akar berbeda, D = 0 akar kembar, D &lt; 0 tidak ada akar real.")

    def abc():
        x1, x2 = nz(-6, 6), Fr(nz(-6, 6), ch([1, 2, 3]))
        a = x2.denominator
        b = -(a * x1 + x2.numerator)
        c = x1 * x2.numerator
        if x1 == x2:
            return None
        e = expr([(a, "x²"), (b, "x"), (c, "")])
        lo, hi = sorted([Fr(x1), x2])
        cc = "x = %s atau x = %s" % (fq(lo), fq(hi))
        return M("Dengan rumus kuadratik (rumus ABC), penyelesaian %s = 0 adalah …" % e, cc, ["x = %s atau x = %s" % (fq(-hi), fq(-lo)), "x = %s atau x = %s" % (fq(lo * a), fq(hi * a)) if a != 1 else "x = %s atau x = %s" % (fq(lo - 1), fq(hi + 1)), "x = %s atau x = %s" % (fq(lo), fq(-hi)) if lo != -hi else "x = %s saja" % fq(hi)],
                 "x = (−b ± √D) : 2a dengan D = %s. Hasilnya %s." % (sn(b * b - 4 * a * c), cc))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            l = ri(3, 15)
            d = ri(2, 8)
            p = l + d
            return MN("Panjang persegi panjang %d cm lebih dari lebarnya. Luasnya %d cm². Lebarnya …" % (d, p * l), l, [p, l + 1, p * l // d if p * l % d == 0 else l - 1], "x(x + %d) = %d → x² + %dx − %d = 0 → (x − %d)(x + %d) = 0 → x = %d cm." % (d, p * l, d, p * l, l, p, l), unit="cm")
        if k == 1:
            n = ri(3, 15)
            return MN("Hasil kali dua bilangan asli berurutan adalah %d. Bilangan yang lebih kecil …" % (n * (n + 1)), n, [n + 1, n - 1, n * (n + 1) // 2], "x(x + 1) = %d → x = %d." % (n * (n + 1), n))
        t = ri(1, 5)
        v = 5 * t
        h = v * t - 5 * t * t
        tt = 2 * t
        return MN("Bola dilempar ke atas. Tingginya h = %dt − 5t² meter setelah t detik. Bola kembali ke tanah setelah …" % (5 * tt), tt, [t, tt + 1, 5 * tt], "%dt − 5t² = 0 → 5t(%d − t) = 0 → t = 0 atau t = %d detik." % (5 * tt, tt, tt), unit="detik")

    sets = [("Memfaktorkan", [(faktor, 20)]),
            ("Persamaan x² = k dan x² + bx = 0", [(kuadrat, 20)]),
            ("Jumlah dan hasil kali akar", [(akar, 20)]),
            ("Diskriminan dan rumus kuadratik", [(rumus, 10), (abc, 10)]),
            ("Soal cerita", [(cerita, 14), (faktor, 6)])]
    return unit("persamaan-kuadrat", "A", 2, "Persamaan Kuadrat: Memfaktorkan dan Rumus Kuadratik", "Persamaan Kuadrat",
                "Peserta didik menyelesaikan persamaan kuadrat dengan memfaktorkan dan rumus kuadratik, menentukan jenis akar dengan diskriminan, dan menyelesaikan masalah kontekstual.",
                "Latihan persamaan kuadrat kelas 9 SMP: memfaktorkan, persamaan x² = k, jumlah dan hasil kali akar, diskriminan, rumus kuadratik (rumus ABC), dan soal cerita. 100 soal dengan kunci jawaban.",
                "Jika p × q = 0, maka p = 0 atau q = 0", "Faktorkan dulu, lalu setiap faktor sama dengan 0.", sets,
                ["Persamaan kuadrat berbentuk ax² + bx + c = 0 dengan a ≠ 0. Akar-akarnya adalah nilai x yang membuat persamaan benar.",
                 "Cara memfaktorkan: x² − 5x + 6 = (x − 2)(x − 3) = 0, jadi x = 2 atau x = 3. Jika tidak mudah difaktorkan, pakai rumus kuadratik x = (−b ± √(b² − 4ac)) : 2a.",
                 "Diskriminan D = b² − 4ac: jika D &gt; 0 ada dua akar real berbeda, D = 0 akar kembar, D &lt; 0 tidak ada akar real. Jumlah akar −b/a, hasil kali akar c/a."],
                [("x² − x − 12 = 0", ["(x − 4)(x + 3) = 0"], "x = 4 atau x = −3"),
                 ("x² = 49", ["x = ±7"], "x = 7 atau x = −7")],
                [["x² = 25 → x = 5 saja", "x = 5 atau x = −5"],
                 ["(x − 3)(x + 2) = 0 → x = −3 atau x = 2", "x − 3 = 0 → x = 3; x + 2 = 0 → x = −2"],
                 ["x² − 4x = 0 → x = 4 saja", "x(x − 4) = 0 → x = 0 atau x = 4"]],
                [("Berapa banyak akar persamaan kuadrat?", "Paling banyak dua akar real. Bisa juga satu akar kembar atau tidak ada akar real."),
                 ("Kapan memakai rumus kuadratik?", "Saat persamaan sulit difaktorkan. Rumus ini selalu dapat dipakai untuk semua persamaan kuadrat."),
                 ("Mengapa boleh membagi persamaan menjadi dua faktor?", "Karena jika hasil kali dua bilangan nol, salah satunya pasti nol.")])


# ============================================================ 3. fungsi kuadrat
def u3():
    def puncak():
        a = nz(-3, 3)
        p, q = ri(-4, 4), ri(-6, 6)
        b, c = -2 * a * p, a * p * p + q
        e = expr([(a, "x²"), (b, "x"), (c, "")])
        k = ri(0, 2)
        if k == 0:
            return M("Titik puncak grafik f(x) = %s adalah …" % e, "(%s, %s)" % (sn(p), sn(q)), ["(%s, %s)" % (sn(-p), sn(q)), "(%s, %s)" % (sn(q), sn(p)), "(%s, %s)" % (sn(p), sn(c)) if c != q else "(%s, %s)" % (sn(p), sn(-q))],
                     "x = −b/2a = %s. f(%s) = %s. Titik puncak (%s, %s)." % (sn(p), sn(p), sn(q), sn(p), sn(q)))
        if k == 1:
            return M("Persamaan sumbu simetri grafik f(x) = %s adalah …" % e, "x = %s" % sn(p), ["x = %s" % sn(-p) if p else "x = 1", "y = %s" % sn(q), "x = %s" % sn(b) if b != p else "x = %s" % sn(p + 2)],
                     "Sumbu simetri x = −b/2a = −(%s) : (2 × %s) = %s." % (sn(b), par(a), sn(p)))
        t = "maksimum" if a < 0 else "minimum"
        return M("Nilai %s fungsi f(x) = %s adalah …" % (t, e), sn(q), [sn(p), sn(c) if c != q else sn(q + 1), sn(-q) if q else "1"], "Grafik terbuka %s, nilai %s = f(%s) = %s." % ("ke bawah" if a < 0 else "ke atas", t, sn(p), sn(q)))

    def potong():
        r1, r2 = nz(-6, 6), nz(-6, 6)
        if r1 == r2:
            return None
        a = ch([1, 1, -1])
        b, c = -a * (r1 + r2), a * r1 * r2
        e = expr([(a, "x²"), (b, "x"), (c, "")])
        k = ri(0, 1)
        if k == 0:
            lo, hi = sorted([r1, r2])
            return M("Titik potong grafik f(x) = %s dengan sumbu x adalah …" % e, "(%s, 0) dan (%s, 0)" % (sn(lo), sn(hi)), ["(%s, 0) dan (%s, 0)" % (sn(-hi), sn(-lo)), "(0, %s) dan (0, %s)" % (sn(lo), sn(hi)), "(0, %s)" % sn(c)],
                     "f(x) = 0 → x = %s atau x = %s." % (sn(lo), sn(hi)))
        return M("Titik potong grafik f(x) = %s dengan sumbu y adalah …" % e, "(0, %s)" % sn(c), ["(%s, 0)" % sn(c), "(0, %s)" % sn(-c), "(0, %s)" % sn(b) if b != c else "(0, %s)" % sn(c + 1)], "x = 0 → f(0) = %s." % sn(c))

    def bentuk():
        a = nz(-4, 4)
        b, c = nz(-6, 6), nz(-9, 9)
        e = expr([(a, "x²"), (b, "x"), (c, "")])
        k = ri(0, 1)
        if k == 0:
            cc = "terbuka ke atas" if a > 0 else "terbuka ke bawah"
            return M("Grafik fungsi f(x) = %s …" % e, cc, ["terbuka ke bawah" if a > 0 else "terbuka ke atas", "berupa garis lurus", "tidak memotong sumbu y"], "Koefisien x² adalah %s, %s, jadi %s." % (sn(a), "positif" if a > 0 else "negatif", cc))
        x = nz(-4, 4)
        return MN("Diketahui f(x) = %s. Nilai f(%s) adalah …" % (e, sn(x)), a * x * x + b * x + c, [-a * x * x + b * x + c, a * x * x - b * x + c, a * 2 * x + b * x + c], "f(%s) = %s × %s + %s × %s + %s = %s." % (sn(x), sn(a), sn(x * x), par(b), par(x), par(c), sn(a * x * x + b * x + c)))

    def grafik():
        a = ch([1, -1])
        p, q = ri(-3, 3), ch([-4, -2, 0, 2, 4])
        f = lambda x: a * (x - p) ** 2 + q
        pic = kurve([(f, BLUE, "")], (-5, 5, 1), (-6, 6, 2), pts=[(p, q, "")], label="grafik fungsi kuadrat")
        b, c = -2 * a * p, a * p * p + q
        e = lambda aa, bb, cc: "f(x) = %s" % expr([(aa, "x²"), (bb, "x"), (cc, "")])
        k = ri(0, 1)
        if k == 0:
            return M("Titik puncak grafik fungsi kuadrat berikut adalah …" + pic, "(%s, %s)" % (sn(p), sn(q)), ["(%s, %s)" % (sn(q), sn(p)) if p != q else "(%s, %s)" % (sn(p), sn(q + 1)), "(%s, %s)" % (sn(-p), sn(q)) if p else "(1, %s)" % sn(q), "(%s, %s)" % (sn(p), sn(-q)) if q else "(%s, 1)" % sn(p)],
                     "Titik balik grafik ada di (%s, %s)." % (sn(p), sn(q)))
        return M("Grafik berikut adalah grafik fungsi …" + pic, e(a, b, c), [e(-a, -b, -c), e(a, -b, c) if b else e(a, 1, c), e(a, b, c + 2)], "Puncak (%s, %s) dan terbuka %s: f(x) = %s(x − %s)² + %s = %s." % (sn(p), sn(q), "ke atas" if a > 0 else "ke bawah", MINUS if a < 0 else "", par(p), par(q), e(a, b, c)[7:]))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            K = ri(5, 30) * 4
            s = K // 4
            return MN("Seutas kawat sepanjang %d cm dibentuk menjadi persegi panjang. Luas terbesar yang mungkin …" % K, s * s, [K * K // 16 + K // 4, s * s - s, K // 2 * 2], "p + l = %d. L = x(%d − x), maksimum saat x = %d: L = %d cm²." % (K // 2, K // 2, s, s * s), unit="cm²")
        if k == 1:
            v = ri(2, 6) * 10
            tp = Fr(v, 10)
            h = v * tp - 5 * tp * tp
            return MN("Tinggi bola h(t) = %dt − 5t² meter. Tinggi maksimum bola …" % v, h, [v * v // 10, h * 2, h + 5], "t = −b/2a = %s detik, h = %s m." % (sn(tp), sn(h)), unit="m")
        p = ri(2, 8) * 1000
        n = ri(50, 200)
        return MN("Keuntungan pedagang U(x) = −x² + %dx (ribu rupiah), dengan x banyak barang. Keuntungan maksimum dicapai saat x = …" % (2 * n), n, [2 * n, n * n, n // 2], "x = −b/2a = %d : 2 = %d." % (2 * n, n), unit="barang")

    sets = [("Titik puncak dan sumbu simetri", [(puncak, 20)]),
            ("Titik potong dengan sumbu", [(potong, 20)]),
            ("Arah grafik dan nilai fungsi", [(bentuk, 20)]),
            ("Membaca grafik", [(grafik, 20)]),
            ("Nilai maksimum dalam soal cerita", [(cerita, 14), (puncak, 6)])]
    return unit("fungsi-kuadrat", "A", 3, "Fungsi Kuadrat dan Grafiknya", "Fungsi Kuadrat",
                "Peserta didik menentukan sifat grafik fungsi kuadrat (arah, titik puncak, sumbu simetri, titik potong) dan menggunakannya untuk masalah nilai maksimum atau minimum.",
                "Latihan fungsi kuadrat kelas 9 SMP: titik puncak, sumbu simetri, titik potong dengan sumbu x dan y, arah grafik, membaca grafik parabola, dan nilai maksimum. 100 soal dengan kunci jawaban.",
                "Sumbu simetri x = −b/2a", "a &gt; 0 terbuka ke atas, a &lt; 0 terbuka ke bawah.", sets,
                ["Grafik f(x) = ax² + bx + c berbentuk parabola. Jika a &gt; 0 terbuka ke atas (punya nilai minimum), jika a &lt; 0 terbuka ke bawah (punya nilai maksimum).",
                 "Sumbu simetri x = −b/2a. Titik puncak (−b/2a, f(−b/2a)).",
                 "Titik potong sumbu y: (0, c). Titik potong sumbu x: selesaikan f(x) = 0."],
                [("Titik puncak f(x) = x² − 6x + 5?", ["x = 6 : 2 = 3", "f(3) = 9 − 18 + 5 = −4"], "(3, −4)"),
                 ("Titik potong f(x) = x² − 4 dengan sumbu x?", ["x² = 4"], "(−2, 0) dan (2, 0)")],
                [["Sumbu simetri x = b/2a", "x = −b/2a"],
                 ["Titik potong sumbu y adalah (c, 0)", "Titik potong sumbu y adalah (0, c)"],
                 ["a negatif berarti grafik di bawah sumbu x", "a negatif berarti parabola terbuka ke bawah"]],
                [("Apa itu titik puncak?", "Titik tertinggi (jika terbuka ke bawah) atau terendah (jika terbuka ke atas) pada parabola."),
                 ("Bagaimana menggambar grafik fungsi kuadrat?", "Tentukan arah, titik potong dengan sumbu, sumbu simetri, dan titik puncak, lalu hubungkan dengan kurva mulus."),
                 ("Di mana fungsi kuadrat dipakai?", "Untuk lintasan bola, luas terbesar, keuntungan maksimum, dan bentuk antena parabola.")])


# ============================================================ 4. kesebangunan
def u4():
    def skala():
        a, b = ri(2, 9), ri(2, 9)
        k = Fr(ch([2, 3, 4, Fr(3, 2), Fr(5, 2)]))
        A, B = a * k, b * k
        if A.denominator != 1 or B.denominator != 1:
            return None
        if ri(0, 1):
            return M("Persegi panjang P berukuran %d cm × %d cm sebangun dengan persegi panjang Q berukuran %d cm × %d cm. Faktor skala dari P ke Q adalah …" % (a, b, A, B), fq(k),
                     [fq(1 / k), fq(k + 1), fq(Fr(A - a))], "%d : %d = %s." % (A, a, fq(k)))
        return MN("Persegi panjang %d cm × %d cm sebangun dengan persegi panjang yang panjangnya %d cm. Lebar persegi panjang kedua …" % (a, b, A), B, [b + (A - a), b * a // A if b * a % A == 0 else B + 1, A - b if A - b > 0 and A - b != B else B + 2], "Faktor skala %s. %d × %s = %d cm." % (fq(k), b, fq(k), B), unit="cm")

    def segitiga():
        a, b, c = ch([(3, 4, 5), (5, 6, 8), (4, 6, 7), (6, 8, 9), (2, 3, 4), (5, 7, 9)])
        k = ch([2, 3, Fr(3, 2), Fr(5, 2), 4])
        A, B, C = a * k, b * k, c * k
        if any(x.denominator != 1 for x in (A, B, C)):
            return None
        w = ri(0, 2)
        s1, s2 = [a, b, c], [A, B, C]
        known = [i for i in range(3) if i != w]
        names = ["AB", "BC", "AC"]
        names2 = ["DE", "EF", "DF"]
        q = "Segitiga ABC sebangun dengan segitiga DEF. AB = %d cm, BC = %d cm, AC = %d cm, dan %s = %s cm. Panjang %s adalah …" % (a, b, c, names2[known[0]], num(int(s2[known[0]])), names2[w])
        return MN(q, s2[w], [s1[w] + (s2[known[0]] - s1[known[0]]), s2[w] + 1, s2[known[0]]], "Faktor skala %s : %d = %s. %s = %d × %s = %s cm." % (num(int(s2[known[0]])), s1[known[0]], fq(k), names2[w], s1[w], fq(k), sn(s2[w])), unit="cm")

    def bayangan():
        k = ri(0, 1)
        if k == 0:
            t, s = ri(15, 20) * 10, ri(1, 4) * 10
            T = ri(3, 12)
            S_ = Fr(T * s * 100, t)
            if S_.denominator != 1 or S_ > 3000:
                return None
            return MN("Anak setinggi %d cm memiliki bayangan %d cm. Pada saat yang sama, bayangan sebuah pohon %s cm. Tinggi pohon …" % (t, s, num(int(S_))), T * 100, [int(S_) * s // t if (int(S_) * s) % t == 0 else T * 100 + 50, T * 100 - 100, int(S_) + t - s], "%d/%d = x/%s → x = %s cm." % (t, s, num(int(S_)), num(T * 100)), unit="cm")
        a, b = ri(2, 8), ri(3, 10)
        d = ri(2, 8)
        if a == b:
            return None
        DE = Fr(b * (a + d), a)
        if DE.denominator != 1:
            return None
        pic = figure({"A": (0, 0), "B": (4, 0), "C": (2.2, 4.5), "D": (0.9, 2.0), "E": (3.1, 2.0)}, [("A", "B"), ("B", "C"), ("C", "A"), ("D", "E")],
                     label="segitiga ABC dengan garis DE sejajar AB")
        return MN("Pada segitiga ABC, DE sejajar AB dengan D pada AC dan E pada BC. CD = %d cm, DA = %d cm, dan DE = %d cm. Panjang AB adalah …" % (a, d, b) + pic, DE, [b + d, Fr(b * a, a + d) if Fr(b * a, a + d).denominator == 1 else DE + 1, b * d // a if (b * d) % a == 0 and b * d // a != DE else DE + 2],
                  "CD/CA = DE/AB → %d/%d = %d/AB → AB = %s cm." % (a, a + d, b, sn(DE)), unit="cm")

    def luas():
        k = ch([2, 3, 4, 5])
        L = ri(3, 20)
        q = ri(0, 1)
        if q == 0:
            return MN("Dua bangun sebangun dengan faktor skala %d. Luas bangun kecil %d cm². Luas bangun besar …" % (k, L), L * k * k, [L * k, L * k * k * k, L + k], "Luas berbanding k² = %d. %d × %d = %d cm²." % (k * k, L, k * k, L * k * k), unit="cm²")
        return M("Dua persegi sebangun. Panjang sisinya berbanding %d : %d. Perbandingan luasnya …" % (1, k), "1 : %d" % (k * k), ["1 : %d" % k, "1 : %d" % (2 * k), "1 : %d" % (k ** 3)], "Luas berbanding kuadrat sisi: 1² : %d² = 1 : %d." % (k, k * k))

    def peta():
        sk = ch([100, 200, 500, 1000, 2500, 50000, 100000, 250000])
        cm = ri(2, 15)
        real = cm * sk
        u, v = ("m", Fr(real, 100)) if real < 100000 else ("km", Fr(real, 100000))
        return M("Pada denah berskala 1 : %s, jarak dua tempat %d cm. Jarak sebenarnya …" % (num(sk), cm), "%s %s" % (dz(v), u), ["%s %s" % (dz(v * 10), u), "%s %s" % (dz(v / 10), u), "%s %s" % (num(real), u)],
                 "%d × %s = %s cm = %s %s." % (cm, num(sk), num(real), dz(v), u))

    sets = [("Faktor skala", [(skala, 20)]),
            ("Segitiga sebangun", [(segitiga, 20)]),
            ("Bayangan dan garis sejajar", [(bayangan, 20)]),
            ("Perbandingan luas", [(luas, 20)]),
            ("Skala peta dan campuran", [(peta, 12), (segitiga, 8)])]
    return unit("kesebangunan", "G", 4, "Kesebangunan Bangun Datar", "Kesebangunan",
                "Peserta didik menjelaskan syarat dua bangun sebangun dan menggunakannya untuk menentukan panjang sisi, skala, dan menyelesaikan masalah kontekstual.",
                "Latihan kesebangunan kelas 9 SMP: faktor skala, segitiga sebangun, bayangan benda, garis sejajar dalam segitiga, perbandingan luas, dan skala peta. 100 soal dengan kunci jawaban.",
                "Sisi seletak sebanding", "Sebangun: sudut seletak sama, sisi seletak sebanding.", sets,
                ["Dua bangun sebangun jika sudut-sudut yang seletak sama besar dan sisi-sisi yang seletak sebanding. Perbandingan itu disebut faktor skala.",
                 "Pada segitiga ABC dengan DE sejajar AB, segitiga CDE sebangun dengan segitiga CAB, jadi CD/CA = DE/AB.",
                 "Jika faktor skala k, panjang dikalikan k dan luas dikalikan k²."],
                [("ΔABC ~ ΔDEF, AB = 4, DE = 10, BC = 6. EF?", ["k = 10 : 4 = 5/2", "EF = 6 × 5/2"], "15"),
                 ("Tongkat 1,5 m berbayangan 2 m. Tiang berbayangan 8 m. Tinggi tiang?", ["1,5/2 = t/8"], "6 m")],
                [["DE/AB = CD/DA", "Bandingkan dengan sisi utuh: DE/AB = CD/CA"],
                 ["Luas dikali k", "Luas dikali k²"],
                 ["Sisi yang dibandingkan tidak seletak", "Pasangkan sisi di depan sudut yang sama besar"]],
                [("Apa beda sebangun dan kongruen?", "Kongruen berarti bentuk dan ukurannya sama. Sebangun berarti bentuknya sama, tetapi ukurannya bisa berbeda."),
                 ("Apakah semua persegi sebangun?", "Ya. Semua sudutnya 90° dan perbandingan sisinya selalu sama."),
                 ("Bagaimana mengetahui dua segitiga sebangun?", "Cukup dua pasang sudut sama besar, atau ketiga pasang sisi sebanding.")])


# ============================================================ 5. kekongruenan
def u5():
    def syarat():
        t1, t2 = ch([("ABC", "DEF"), ("PQR", "KLM"), ("ABC", "PQR"), ("KLM", "XYZ"), ("DEF", "STU"), ("RST", "UVW")])
        L = lambda t, i, j: t[i] + t[j]
        G = lambda t, i: "∠" + t[i]
        F = [("%s = %s, %s = %s, dan %s = %s" % (L(t1, 0, 1), L(t2, 0, 1), L(t1, 1, 2), L(t2, 1, 2), L(t1, 0, 2), L(t2, 0, 2)), "sisi, sisi, sisi (s-s-s)"),
             ("%s = %s, %s = %s, dan %s = %s" % (L(t1, 0, 1), L(t2, 0, 1), G(t1, 1), G(t2, 1), L(t1, 1, 2), L(t2, 1, 2)), "sisi, sudut, sisi (s-sd-s)"),
             ("%s = %s, %s = %s, dan %s = %s" % (G(t1, 0), G(t2, 0), L(t1, 0, 1), L(t2, 0, 1), G(t1, 1), G(t2, 1)), "sudut, sisi, sudut (sd-s-sd)"),
             ("%s = %s, %s = %s, dan %s = %s" % (L(t1, 1, 2), L(t2, 1, 2), G(t1, 2), G(t2, 2), L(t1, 0, 2), L(t2, 0, 2)), "sisi, sudut, sisi (s-sd-s)"),
             ("%s = %s, %s = %s, dan %s = %s" % (G(t1, 1), G(t2, 1), L(t1, 1, 2), L(t2, 1, 2), G(t1, 2), G(t2, 2)), "sudut, sisi, sudut (sd-s-sd)"),
             ("%s = %s, %s = %s, dan %s = %s" % (G(t1, 0), G(t2, 0), G(t1, 1), G(t2, 1), L(t1, 1, 2), L(t2, 1, 2)), "sudut, sudut, sisi (sd-sd-s)")]
        d, c = ch(F)
        return M("Segitiga %s dan %s dengan %s. Kedua segitiga kongruen berdasarkan syarat …" % (t1, t2, d), c,
                 [o for o in sh(["sisi, sisi, sisi (s-s-s)", "sisi, sudut, sisi (s-sd-s)", "sudut, sisi, sudut (sd-s-sd)", "sudut, sudut, sudut (sd-sd-sd)", "sudut, sudut, sisi (sd-sd-s)"]) if o != c],
                 "Unsur yang diketahui: %s, jadi syaratnya %s." % (d, c))

    def bukan():
        q = ch(["Manakah yang tidak menjamin dua segitiga kongruen?", "Syarat yang tidak cukup untuk membuktikan dua segitiga kongruen adalah …"])
        n = ri(1, 3)
        return M(q if n == 1 else q.replace("?", " (pilih satu)?") if n == 2 else q, "ketiga sudutnya sama besar (sd-sd-sd)", ["ketiga sisinya sama panjang (s-s-s)", "dua sisi dan sudut apitnya sama (s-sd-s)", "dua sudut dan sisi apitnya sama (sd-s-sd)"],
                 "Jika hanya ketiga sudutnya sama, segitiga bisa sebangun tetapi ukurannya berbeda.")

    def pasangan():
        a, b, c = ri(4, 15), ri(4, 15), ri(4, 15)
        if max(a, b, c) * 2 >= a + b + c or len({a, b, c}) < 3:
            return None
        A, B = ri(30, 80), ri(30, 80)
        C = 180 - A - B
        if C < 20:
            return None
        k = ri(0, 1)
        if k == 0:
            w = ch([("EF", "BC", b), ("DF", "AC", c), ("DE", "AB", a)])
            return MN("ΔABC ≅ ΔDEF dengan AB = %d cm, BC = %d cm, dan AC = %d cm. Panjang %s adalah …" % (a, b, c, w[0]), w[2], [x for x in [a, b, c] if x != w[2]] + [w[2] + 1], "%s seletak dengan %s, jadi %s = %d cm." % (w[0], w[1], w[0], w[2]), unit="cm")
        w = ch([("∠D", "∠A", A), ("∠E", "∠B", B), ("∠F", "∠C", C)])
        return MN("ΔABC ≅ ΔDEF dengan ∠A = %d° dan ∠B = %d°. Besar %s adalah …" % (A, B, w[0]), w[2], [x for x in [A, B, C] if x != w[2]] + [180 - w[2]], "%s seletak dengan %s%s, jadi %s = %d°." % (w[0], w[1], " (∠C = 180° − %d° − %d°)" % (A, B) if w[1] == "∠C" else "", w[0], w[2]), unit="°")

    def bangun():
        k = ch([0, 1, 3])
        if k == 0:
            p, l = ri(4, 15), ri(2, 10)
            return MN("Persegi panjang ABCD dibagi diagonal AC menjadi dua segitiga kongruen. Jika AB = %d cm dan BC = %d cm, luas segitiga ACD …" % (p, l), Fr(p * l, 2), [p * l, p + l, Fr(p * l, 4)], "ΔABC ≅ ΔCDA, jadi luasnya setengah persegi panjang: ½ × %d × %d = %s cm²." % (p, l, sn(Fr(p * l, 2))), unit="cm²")
        if k == 1:
            a = ri(40, 80)
            return MN("Pada jajargenjang ABCD, diagonal BD membagi jajargenjang menjadi ΔABD ≅ ΔCDB. Jika ∠A = %d°, besar ∠C adalah …" % a, a, [180 - a, 90 - a if a < 90 else a - 10, 360 - a], "Sudut yang seletak pada segitiga kongruen sama besar: ∠C = ∠A = %d°." % a, unit="°")
        if k == 2:
            s = ri(3, 14)
            return MN("Layang-layang ABCD dengan AB = AD = %d cm dibagi diagonal AC menjadi dua segitiga kongruen. Jika keliling layang-layang %d cm, panjang BC …" % (s, 2 * s + 2 * (s + ri(2, 6))), None, [], "") if False else None
        a = ri(30, 70)
        return MN("Segitiga sama kaki ABC dengan AC = BC dibagi garis tinggi CD menjadi ΔADC ≅ ΔBDC. Jika ∠ACD = %d°, besar ∠ACB adalah …" % a, 2 * a, [a, 180 - 2 * a, 90 - a], "∠BCD = ∠ACD = %d°, jadi ∠ACB = %d°." % (a, 2 * a), unit="°")

    def gambar():
        a, b = ri(3, 9), ri(4, 12)
        c = math.hypot(a, b)
        A = ri(30, 60)
        pic = figure({"A": (0, 0), "B": (4, 0), "C": (1.4, 2.8)}, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("A", "B", "%d cm" % a), ("A", "C", "%d cm" % b)], label="segitiga ABC") if False else ""
        k = ri(0, 1)
        if k == 0:
            return M("ΔPQR ≅ ΔKLM. Sisi yang seletak dengan QR adalah …", "LM", ["KL", "KM", "PR"], "Urutan huruf menunjukkan pasangan: P ↔ K, Q ↔ L, R ↔ M. Jadi QR ↔ LM.") if ri(0, 1) else \
                M("ΔPQR ≅ ΔKLM. Sudut yang sama besar dengan ∠R adalah …", "∠M", ["∠K", "∠L", "∠P"], "R seletak dengan M, jadi ∠R = ∠M.")
        pairs = [("ABC", "XYZ"), ("PQR", "STU"), ("KLM", "DEF"), ("ABC", "PQR"), ("DEF", "KLM"), ("RST", "UVW")]
        t1, t2 = ch(pairs)
        if ri(0, 1):
            i = ri(0, 2)
            return M("Δ%s ≅ Δ%s. Sudut yang sama besar dengan ∠%s adalah …" % (t1, t2, t1[i]), "∠" + t2[i], ["∠" + t2[j] for j in range(3) if j != i] + ["∠" + t1[(i + 1) % 3]],
                     "Pasangan titik: %s. Jadi ∠%s = ∠%s." % (", ".join("%s ↔ %s" % (t1[x], t2[x]) for x in range(3)), t1[i], t2[i]))
        i, j = sorted(sh(range(3))[:2])
        side = t1[i] + t1[j]
        c = t2[i] + t2[j]
        others = [t2[x] + t2[y] for x, y in [(0, 1), (1, 2), (0, 2)] if (x, y) != (i, j)] + [t1[3 - i - j] + t1[i]]
        return M("Δ%s ≅ Δ%s. Sisi yang seletak dengan %s adalah …" % (t1, t2, side), c, others, "Pasangan titik: %s. Jadi %s ↔ %s." % (", ".join("%s ↔ %s" % (t1[x], t2[x]) for x in range(3)), side, c))

    sets = [("Syarat dua segitiga kongruen", [(syarat, 14), (bukan, 3), (gambar, 3)]),
            ("Unsur yang seletak", [(gambar, 20)]),
            ("Panjang sisi dan besar sudut", [(pasangan, 20)]),
            ("Kekongruenan pada bangun datar", [(bangun, 20)]),
            ("Campuran", [(pasangan, 10), (syarat, 5), (bangun, 5)])]
    return unit("kekongruenan", "G", 5, "Kekongruenan Segitiga", "Kekongruenan",
                "Peserta didik menjelaskan syarat dua segitiga kongruen (s-s-s, s-sd-s, sd-s-sd, sd-sd-s) dan menggunakannya untuk menentukan panjang sisi dan besar sudut.",
                "Latihan kekongruenan kelas 9 SMP: syarat dua segitiga kongruen, sisi dan sudut yang seletak, menentukan panjang sisi dan besar sudut, serta kekongruenan pada bangun datar. 100 soal dengan kunci jawaban.",
                "Kongruen = bentuk dan ukuran sama", "Syarat: s-s-s, s-sd-s, sd-s-sd, atau sd-sd-s.", sets,
                ["Dua bangun kongruen jika bentuk dan ukurannya sama, sehingga dapat saling menutupi tepat. Sisi dan sudut yang seletak sama besar.",
                 "Dua segitiga kongruen jika memenuhi salah satu syarat: tiga sisi sama (s-s-s), dua sisi dan sudut apitnya (s-sd-s), dua sudut dan sisi apitnya (sd-s-sd), atau dua sudut dan satu sisi (sd-sd-s).",
                 "Pada penulisan ΔABC ≅ ΔDEF, urutan huruf menunjukkan pasangan: A ↔ D, B ↔ E, C ↔ F."],
                [("ΔABC ≅ ΔPQR. Sisi yang seletak dengan BC?", ["B ↔ Q, C ↔ R"], "QR"),
                 ("AB = PQ, ∠B = ∠Q, BC = QR. Syarat kongruen?", ["Dua sisi dan sudut apitnya"], "s-sd-s")],
                [["Tiga sudut sama berarti kongruen", "Tiga sudut sama hanya menjamin sebangun"],
                 ["Pasangan sisi ditebak dari gambar", "Pakai urutan huruf pada penulisan ≅"],
                 ["s-s-sd selalu kongruen", "Sudut harus diapit kedua sisi (s-sd-s)"]],
                [("Apa arti lambang ≅?", "Lambang ≅ berarti kongruen, yaitu sama bentuk dan sama ukuran."),
                 ("Mengapa sd-sd-sd bukan syarat kongruen?", "Dua segitiga dengan sudut yang sama bisa berbeda ukuran, misalnya segitiga kecil dan besar yang sebangun."),
                 ("Untuk apa kekongruenan dipakai?", "Untuk membuktikan dua sisi atau dua sudut sama besar, misalnya pada bangun simetris.")])


# ============================================================ 6. sudut pusat dan sudut keliling
def u6():
    def lingk(marks, label="lingkaran dengan sudut pusat dan sudut keliling"):
        cx, cy, r = 150, 120, 95
        P = lambda d: (cx + r * math.cos(math.radians(d)), cy - r * math.sin(math.radians(d)))
        a, b, c = -30, 210, 90
        A, B, C = P(a), P(b), P(c)
        s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2'/>" % (cx, cy, r, INK),
             line(A[0], A[1], cx, cy, BLUE, 2) + line(B[0], B[1], cx, cy, BLUE, 2), line(A[0], A[1], C[0], C[1], RED, 2) + line(B[0], B[1], C[0], C[1], RED, 2),
             "<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (cx, cy, INK), text(cx, cy - 10, "O", 14)]
        for nm, (x, y) in (("A", A), ("B", B), ("C", C)):
            s.append(text(x + (x - cx) / r * 16, y + (y - cy) / r * 16 + 5, nm, 15))
        s.append(text(cx, cy + 30, marks[0], 14, col=BLUE))
        s.append(text(C[0], C[1] + 36, marks[1], 14, col=RED))
        return wrap(300, 240, "".join(s), label)

    def hubungan():
        k = ri(0, 1)
        a = ri(15, 85)
        if k == 0:
            return MN("Sudut keliling ACB besarnya %d°. Besar sudut pusat AOB yang menghadap busur yang sama adalah …" % a + lingk(["?", "%d°" % a]), 2 * a, [a, 180 - a, 180 - 2 * a, 4 * a], "Sudut pusat = 2 × sudut keliling = 2 × %d° = %d°." % (a, 2 * a), unit="°")
        b = 2 * a
        return MN("Sudut pusat AOB besarnya %d°. Besar sudut keliling ACB yang menghadap busur yang sama adalah …" % b + lingk(["%d°" % b, "?"]), a, [b, 2 * b, 180 - b], "Sudut keliling = ½ × sudut pusat = ½ × %d° = %d°." % (b, a), unit="°")

    def aljabar():
        x = ri(5, 25)
        p, q = ri(1, 4), ri(-10, 20)
        c1 = lin(p, q)
        k = p * x + q
        if k <= 0 or 2 * k >= 180:
            return None
        r, s_ = ri(1, 4), 0
        s_ = 2 * k - r * x
        if s_ < -30 or s_ > 80 or r == 2 * p:
            return None
        return MN("Sudut keliling ACB = (%s)° dan sudut pusat AOB = (%s)° menghadap busur yang sama. Nilai x adalah …" % (c1, lin(r, s_)), x, [x + 2, x - 3, k],
                  "%s = 2(%s) → %s = %s → x = %d." % (lin(r, s_), c1, lin(r, s_), lin(2 * p, 2 * q), x))

    def setengah():
        a = ri(20, 70)
        k = ri(0, 1)
        if k == 0:
            return MN("AB adalah diameter lingkaran dan C titik pada lingkaran. Besar ∠ACB adalah …", 90, [180, 45, 60], "Sudut keliling yang menghadap diameter (setengah lingkaran) selalu 90°.", unit="°") if ri(0, 5) == 0 else \
                MN("AB diameter lingkaran dan C titik pada lingkaran. Jika ∠CAB = %d°, besar ∠CBA adalah …" % a, 90 - a, [180 - a, a, 90 + a], "∠ACB = 90° (menghadap diameter), jadi ∠CBA = 180° − 90° − %d° = %d°." % (a, 90 - a), unit="°")
        b = ri(20, 80)
        return MN("Dua sudut keliling ∠ACB dan ∠ADB menghadap busur AB yang sama. Jika ∠ACB = %d°, besar ∠ADB adalah …" % b, b, [2 * b, 180 - b, 90 - b if 90 - b != b else b + 10], "Sudut keliling yang menghadap busur yang sama besarnya sama: %d°." % b, unit="°")

    def segi4():
        a, b = ri(50, 130), ri(50, 130)
        k = ri(0, 1)
        w = ch([("∠C", "∠A", a), ("∠D", "∠B", b)])
        return MN("ABCD segi empat tali busur dengan ∠A = %d° dan ∠B = %d°. Besar %s adalah …" % (a, b, w[0]), 180 - w[2], [w[2], 360 - a - b, 90 - w[2] if w[2] < 90 else w[2] - 30], "Sudut yang berhadapan pada segi empat tali busur jumlahnya 180°: %s = 180° − %d° = %d°." % (w[0], w[2], 180 - w[2]), unit="°")

    def busur():
        r = ch([7, 14, 21, 28])
        a = ch([30, 45, 60, 90, 120])
        k = ri(0, 1)
        if k == 0:
            return MN("Sudut keliling yang menghadap busur AB besarnya %d°. Besar sudut pusat AOB adalah …" % (a // 2) if a % 2 == 0 else "", a, [a // 2, a * 2, 180 - a], "Sudut pusat = 2 × %d° = %d°." % (a // 2, a), unit="°") if a % 2 == 0 else None
        a1, a2 = ri(2, 8) * 10, 0
        a2 = ri(2, 8) * 10
        if a1 == a2:
            return None
        L1 = ri(2, 12) * 2
        L2 = Fr(L1 * a2, a1)
        if L2.denominator != 1:
            return None
        return MN("Pada sebuah lingkaran, sudut pusat %d° menghadap busur sepanjang %d cm. Panjang busur di depan sudut pusat %d° adalah …" % (a1, L1, a2), L2, [L1 + a2 - a1 if L1 + a2 - a1 > 0 else L2 + 2, Fr(L1 * a1, a2) if Fr(L1 * a1, a2) != L2 else L2 + 1, L2 * 2],
                  "Panjang busur sebanding dengan sudut pusat: %d/%d × %d = %s cm." % (a2, a1, L1, sn(L2)), unit="cm")

    sets = [("Sudut pusat dan sudut keliling", [(hubungan, 20)]),
            ("Sudut keliling menghadap busur yang sama dan diameter", [(setengah, 20)]),
            ("Segi empat tali busur", [(segi4, 20)]),
            ("Bentuk aljabar", [(aljabar, 20)]),
            ("Busur dan sudut pusat", [(busur, 14), (hubungan, 6)])]
    return unit("sudut-pusat-dan-sudut-keliling", "G", 6, "Sudut Pusat dan Sudut Keliling Lingkaran", "Sudut Pusat dan Sudut Keliling",
                "Peserta didik menjelaskan hubungan sudut pusat dan sudut keliling, sudut yang menghadap diameter, segi empat tali busur, dan hubungan sudut pusat dengan panjang busur.",
                "Latihan sudut pusat dan sudut keliling kelas 9 SMP: hubungan sudut pusat dan sudut keliling, sudut yang menghadap diameter, sudut keliling yang menghadap busur sama, segi empat tali busur, dan panjang busur. 100 soal dengan kunci jawaban.",
                "Sudut pusat = 2 × sudut keliling", "Sudut keliling yang menghadap diameter = 90°.", sets,
                ["Sudut pusat adalah sudut yang titik sudutnya di pusat lingkaran. Sudut keliling titik sudutnya pada lingkaran.",
                 "Jika menghadap busur yang sama, sudut pusat = 2 × sudut keliling. Semua sudut keliling yang menghadap busur yang sama besarnya sama, dan yang menghadap diameter besarnya 90°.",
                 "Pada segi empat tali busur, sudut yang berhadapan jumlahnya 180°. Panjang busur sebanding dengan besar sudut pusatnya."],
                [("Sudut keliling 35°. Sudut pusat yang menghadap busur sama?", ["2 × 35°"], "70°"),
                 ("Segi empat tali busur, ∠A = 105°. ∠C?", ["180° − 105°"], "75°")],
                [["Sudut keliling = 2 × sudut pusat", "Sudut pusat yang 2 kali sudut keliling"],
                 ["Sudut menghadap diameter = 180°", "Sudut keliling menghadap diameter = 90°"],
                 ["Sudut berhadapan segi empat tali busur sama besar", "Jumlahnya 180°"]],
                [("Apa itu segi empat tali busur?", "Segi empat yang keempat titik sudutnya terletak pada lingkaran."),
                 ("Mengapa sudut yang menghadap diameter 90°?", "Sudut pusatnya 180° (garis lurus), dan sudut keliling setengahnya, yaitu 90°."),
                 ("Apakah semua sudut keliling sama besar?", "Hanya jika menghadap busur yang sama.")])


# ============================================================ 7. tabung, kerucut, bola
def u7():
    def piv(r):
        return (Fr(22, 7), "22/7") if r % 7 == 0 else (Fr(314, 100), "3,14")

    def val(x):
        return dz(x) if S.endlich(x) else fq(x)

    R7 = [7, 14, 21, 3.5]
    RS = [7, 14, 21, 10, 5, 20, 3, 6, 30]

    def tabung():
        r = ch(RS)
        t = ri(2, 20) * (1 if r % 7 else 1)
        p, ps = piv(r)
        k = ri(0, 2)
        if k == 0:
            v = p * r * r * t
            return M("Volume tabung dengan jari-jari %d cm dan tinggi %d cm adalah … (π = %s)" % (r, t, ps), "%s cm³" % val(v), ["%s cm³" % val(2 * p * r * t), "%s cm³" % val(p * r * t), "%s cm³" % val(v / 3)], "V = πr²t = %s × %d² × %d = %s cm³." % (ps, r, t, val(v)))
        if k == 1:
            v = 2 * p * r * (r + t)
            return M("Luas permukaan tabung dengan jari-jari %d cm dan tinggi %d cm adalah … (π = %s)" % (r, t, ps), "%s cm²" % val(v), ["%s cm²" % val(2 * p * r * t), "%s cm²" % val(p * r * r * t), "%s cm²" % val(p * r * (r + t))], "LP = 2πr(r + t) = 2 × %s × %d × %d = %s cm²." % (ps, r, r + t, val(v)))
        v = 2 * p * r * t
        return M("Luas selimut tabung dengan jari-jari %d cm dan tinggi %d cm adalah … (π = %s)" % (r, t, ps), "%s cm²" % val(v), ["%s cm²" % val(2 * p * r * (r + t)), "%s cm²" % val(p * r * t), "%s cm²" % val(p * r * r * t)], "L selimut = 2πrt = %s cm²." % val(v))

    def kerucut():
        r, s, t = ch([(3, 5, 4), (6, 10, 8), (5, 13, 12), (7, 25, 24), (9, 15, 12), (8, 17, 15), (12, 20, 16), (21, 35, 28), (14, 50, 48), (15, 25, 20)])
        p, ps = piv(r)
        k = ri(0, 2)
        if k == 0:
            v = p * r * r * t / 3
            return M("Volume kerucut dengan jari-jari %d cm dan tinggi %d cm adalah … (π = %s)" % (r, t, ps), "%s cm³" % val(v), ["%s cm³" % val(p * r * r * t), "%s cm³" % val(p * r * r * s / 3), "%s cm³" % val(p * r * t / 3)], "V = ⅓πr²t = ⅓ × %s × %d² × %d = %s cm³." % (ps, r, t, val(v)))
        if k == 1:
            v = p * r * (r + s)
            return M("Luas permukaan kerucut dengan jari-jari %d cm dan garis pelukis %d cm adalah … (π = %s)" % (r, s, ps), "%s cm²" % val(v), ["%s cm²" % val(p * r * s), "%s cm²" % val(p * r * (r + t)), "%s cm²" % val(2 * p * r * (r + s))], "LP = πr(r + s) = %s × %d × %d = %s cm²." % (ps, r, r + s, val(v)))
        return MN("Kerucut dengan jari-jari %d cm dan tinggi %d cm. Panjang garis pelukisnya …" % (r, t), s, [r + t, s + 1, t - r if t > r else s + 2], "s = √(r² + t²) = √(%d + %d) = %d cm." % (r * r, t * t, s), unit="cm")

    def bola():
        r = ch([3, 6, 7, 9, 10, 12, 14, 15, 21, 30, 5, 20, 28, 35, 2, 4, 8, 42])
        p, ps = piv(r)
        k = ri(0, 1)
        if k == 0:
            v = Fr(4, 3) * p * r ** 3
            return M("Volume bola dengan jari-jari %d cm adalah … (π = %s)" % (r, ps), "%s cm³" % val(v), ["%s cm³" % val(4 * p * r * r), "%s cm³" % val(p * r ** 3), "%s cm³" % val(Fr(2, 3) * p * r ** 3)], "V = 4/3 πr³ = 4/3 × %s × %d³ = %s cm³." % (ps, r, val(v)))
        v = 4 * p * r * r
        return M("Luas permukaan bola dengan jari-jari %d cm adalah … (π = %s)" % (r, ps), "%s cm²" % val(v), ["%s cm²" % val(Fr(4, 3) * p * r ** 3), "%s cm²" % val(p * r * r), "%s cm²" % val(2 * p * r * r)], "L = 4πr² = 4 × %s × %d² = %s cm²." % (ps, r, val(v)))

    def banding():
        k = ri(0, 2)
        r = ri(2, 9)
        t = ri(2, 9) * 3
        if k == 0:
            return M("Tabung dan kerucut memiliki jari-jari %d cm dan tinggi %d cm. Perbandingan volume tabung dan kerucut …" % (r, t), "3 : 1", ["1 : 3", "2 : 1", "1 : 1"], "V kerucut = ⅓ V tabung, jadi 3 : 1.")
        if k == 1:
            f = ch([2, 3])
            return M("Jari-jari sebuah bola diperbesar %d kali. Volumenya menjadi … kali semula" % f, "%d" % f ** 3, ["%d" % f, "%d" % f ** 2, "%d" % (4 * f)], "V sebanding dengan r³: %d³ = %d." % (f, f ** 3))
        return M("Sebuah bola tepat masuk ke dalam tabung (jari-jari %d cm, tinggi %d cm). Perbandingan volume bola dan tabung …" % (r, 2 * r), "2 : 3", ["1 : 2", "3 : 4", "1 : 3"], "V bola = 4/3 πr³, V tabung = πr² × 2r = 2πr³. 4/3 : 2 = 2 : 3.")

    def cerita():
        k = ri(0, 2)
        if k == 0:
            r, t = ch([7, 14]), ri(2, 10) * 10
            v = Fr(22, 7) * r * r * t
            return M("Tangki air berbentuk tabung berjari-jari %d dm dan tinggi %d dm. Isi tangki jika penuh … (π = 22/7)" % (r, t), "%s liter" % num(int(v)), ["%s liter" % num(int(v) // 10), "%s liter" % num(int(2 * Fr(22, 7) * r * t)), "%s liter" % num(int(v) // 3)],
                     "V = 22/7 × %d² × %d = %s dm³ = %s liter." % (r, t, num(int(v)), num(int(v))))
        if k == 1:
            r = ch([7, 14, 21])
            v = Fr(2, 3) * Fr(22, 7) * r ** 3
            return M("Mangkuk berbentuk setengah bola berjari-jari %d cm. Volume mangkuk … (π = 22/7)" % r, "%s cm³" % val(v), ["%s cm³" % val(2 * v), "%s cm³" % val(v / 2), "%s cm³" % val(2 * Fr(22, 7) * r * r)], "½ × 4/3 × 22/7 × %d³ = %s cm³." % (r, val(v)))
        r, s, t = ch([(3, 5, 4), (6, 10, 8), (9, 15, 12)])
        return M("Topi ulang tahun berbentuk kerucut tanpa alas dengan jari-jari %d cm dan garis pelukis %d cm. Luas kertas yang diperlukan … (π = 3,14)" % (r, s), "%s cm²" % dz(Fr(314, 100) * r * s),
                 ["%s cm²" % dz(Fr(314, 100) * r * (r + s)), "%s cm²" % dz(Fr(314, 100) * r * t), "%s cm²" % dz(Fr(314, 100) * r * r * t / 3)], "Luas selimut = πrs = 3,14 × %d × %d = %s cm²." % (r, s, dz(Fr(314, 100) * r * s)))

    sets = [("Tabung", [(tabung, 20)]),
            ("Kerucut", [(kerucut, 20)]),
            ("Bola", [(bola, 20)]),
            ("Perbandingan volume", [(banding, 8), (tabung, 6), (bola, 6)]),
            ("Soal cerita", [(cerita, 14), (kerucut, 6)])]
    return unit("tabung-kerucut-dan-bola", "P", 7, "Tabung, Kerucut, dan Bola: Luas Permukaan dan Volume", "Tabung, Kerucut, dan Bola",
                "Peserta didik menghitung luas permukaan dan volume bangun ruang sisi lengkung (tabung, kerucut, bola) dan menyelesaikan masalah yang terkait.",
                "Latihan tabung, kerucut, dan bola kelas 9 SMP: volume, luas permukaan, luas selimut, garis pelukis kerucut, perbandingan volume, dan soal cerita dengan π = 22/7 dan 3,14. 100 soal dengan kunci jawaban.",
                "V kerucut = ⅓ × V tabung", "V tabung = πr²t, V kerucut = ⅓πr²t, V bola = 4/3 πr³.", sets,
                ["Tabung: V = πr²t, luas selimut 2πrt, luas permukaan 2πr(r + t).",
                 "Kerucut: V = ⅓πr²t, luas permukaan πr(r + s), dengan garis pelukis s = √(r² + t²).",
                 "Bola: V = 4/3 πr³ dan luas permukaan 4πr². Pakai π = 22/7 jika jari-jari kelipatan 7."],
                [("Tabung r = 7 cm, t = 10 cm. Volume?", ["22/7 × 49 × 10"], "1.540 cm³"),
                 ("Bola r = 21 cm. Luas permukaan?", ["4 × 22/7 × 441"], "5.544 cm²")],
                [["V kerucut = πr²t", "Jangan lupa dikali ⅓"],
                 ["Luas permukaan kerucut memakai tinggi t", "Pakai garis pelukis s"],
                 ["V bola = 4πr²", "4πr² adalah luas permukaan; volume 4/3 πr³"]],
                [("Apa itu garis pelukis kerucut?", "Ruas garis dari puncak kerucut ke tepi alasnya. Panjangnya s = √(r² + t²)."),
                 ("Mengapa volume kerucut sepertiga volume tabung?", "Tiga kerucut dengan alas dan tinggi sama dapat mengisi penuh satu tabung."),
                 ("Apa itu luas selimut?", "Luas sisi lengkung tanpa alas dan tutup.")])


# ============================================================ 8. dilatasi
def u8():
    def pt(x, y):
        return "(%s, %s)" % (sn(x), sn(y))

    def bayang():
        x, y = nz(-6, 6), nz(-6, 6)
        k = Fr(ch([2, 3, -2, Fr(1, 2), -1, 4, Fr(-1, 2)]))
        if (x * k).denominator != 1 or (y * k).denominator != 1:
            return None
        c = (x * k, y * k)
        return M("Bayangan titik A%s oleh dilatasi dengan pusat O(0, 0) dan faktor skala %s adalah …" % (pt(x, y), fq(k)), "A'%s" % pt(*c),
                 ["A'%s" % pt(x + k, y + k), "A'%s" % pt(-c[0], -c[1]), "A'%s" % pt(x * k, y), "A'%s" % pt(Fr(x) / k, Fr(y) / k)],
                 "(kx, ky) = (%s × %s, %s × %s) = %s." % (fq(k), par(x), fq(k), par(y), pt(*c)))

    def faktor():
        x, y = nz(-6, 6), nz(-6, 6)
        k = Fr(ch([2, 3, -2, -3, Fr(1, 2), 4]))
        if (x * k).denominator != 1 or (y * k).denominator != 1:
            return None
        return M("Titik P%s didilatasi dengan pusat O menjadi P'%s. Faktor skalanya …" % (pt(x, y), pt(x * k, y * k)), fq(k), [fq(1 / k), fq(-k), fq(k + 1)], "%s : %s = %s." % (sn(x * k), par(x), fq(k)))

    def ukuran():
        k = Fr(ch([2, 3, 4, Fr(1, 2), Fr(1, 3)]))
        L = ri(2, 12) * 9
        a = ri(2, 12) * 3
        q = ri(0, 2)
        if q == 0:
            return MN("Sebuah ruas garis sepanjang %d cm didilatasi dengan faktor skala %s. Panjang bayangannya …" % (a, fq(k)), a * k, [a + k, a * k * k, a / k], "%d × %s = %s cm." % (a, fq(k), sn(a * k)), unit="cm")
        if q == 1:
            return MN("Persegi dengan luas %d cm² didilatasi dengan faktor skala %s. Luas bayangannya …" % (L, fq(k)), L * k * k, [L * k, L * k * k * k, L + k * k], "Luas dikali k² = %s: %d × %s = %s cm²." % (fq(k * k), L, fq(k * k), sn(L * k * k)), unit="cm²")
        return M("Dilatasi dengan faktor skala %s menghasilkan bayangan yang …" % fq(k), "diperbesar" if k > 1 else "diperkecil", ["diperkecil" if k > 1 else "diperbesar", "sama besar", "berubah bentuk"],
                 "k &gt; 1 diperbesar, 0 &lt; k &lt; 1 diperkecil. Bentuknya tetap.")

    def pusat():
        a, b = nz(-4, 4), nz(-4, 4)
        x, y = nz(-6, 6), nz(-6, 6)
        k = ch([2, 3, -1, -2])
        c = (a + k * (x - a), b + k * (y - b))
        return M("Bayangan titik A%s oleh dilatasi dengan pusat P%s dan faktor skala %s adalah …" % (pt(x, y), pt(a, b), sn(k)), "A'%s" % pt(*c),
                 ["A'%s" % pt(k * x, k * y), "A'%s" % pt(k * (x - a), k * (y - b)), "A'%s" % pt(a + k * (x + a), b + k * (y + b))],
                 "(a + k(x − a), b + k(y − b)) = %s." % pt(*c))

    def gambar():
        m = ch([2, 3])
        x0, y0 = ri(0, 2), ri(0, 2)
        dx, dy = ch([1, 2]), ch([1, 2])
        fx, fy = ch([0, 1]), ch([0, 1])
        T = [(x0 + fx * dx, y0), (x0 + (1 - fx) * dx, y0), (x0 + fx * dx, y0 + dy)] if fy == 0 else [(x0, y0 + dy), (x0 + dx, y0 + dy), (x0 + fx * dx, y0)]
        if max(max(p) for p in T) * m > 9 or len(set(T)) < 3:
            return None
        Big = [(p[0] * m, p[1] * m) for p in T]
        up = ri(0, 1)
        k = Fr(m) if up else Fr(1, m)
        pts, img = (T, Big) if up else (Big, T)
        X = lambda v: 20 + float(v) * 26
        Y = lambda v: 262 - float(v) * 26
        s = []
        for i in range(0, 10):
            s.append(line(X(i), Y(0), X(i), Y(9), "#d5dfec", 1) + line(X(0), Y(i), X(9), Y(i), "#d5dfec", 1))
        s.append(line(X(0), Y(0), X(9), Y(0), INK, 2) + line(X(0), Y(0), X(0), Y(9), INK, 2) + text(X(0) - 8, Y(0) + 16, "O", 13))
        s.append("<polygon points='%s' fill='#c7d9f7' stroke='%s' stroke-width='2'/>" % (" ".join("%.0f,%.0f" % (X(a), Y(b)) for a, b in pts), BLUE))
        s.append("<polygon points='%s' fill='none' stroke='%s' stroke-width='2.4' stroke-dasharray='6 4'/>" % (" ".join("%.0f,%.0f" % (X(a), Y(b)) for a, b in img), RED))
        pic = wrap(280, 282, "".join(s), "segitiga dan bayangannya oleh dilatasi")
        return M("Segitiga biru didilatasi dengan pusat O menjadi segitiga merah (garis putus-putus). Faktor skalanya …" + pic, fq(k), [fq(1 / k), fq(k + 1) if up else fq(Fr(1, m + 1)), fq(-k)],
                 "Setiap koordinat titik sudut dikali %s." % fq(k))

    sets = [("Dilatasi dengan pusat O", [(bayang, 20)]),
            ("Menentukan faktor skala", [(faktor, 12), (gambar, 8)]),
            ("Ukuran bayangan", [(ukuran, 20)]),
            ("Dilatasi dengan pusat P(a, b)", [(pusat, 20)]),
            ("Campuran", [(bayang, 7), (gambar, 6), (ukuran, 7)])]
    return unit("dilatasi", "G", 8, "Dilatasi (Perbesaran dan Pengecilan)", "Dilatasi",
                "Peserta didik melakukan dilatasi pada bidang koordinat dengan pusat O dan pusat P(a, b), menentukan faktor skala, dan menghubungkan dilatasi dengan kesebangunan.",
                "Latihan dilatasi kelas 9 SMP: bayangan titik dengan pusat O dan pusat P(a, b), faktor skala positif dan negatif, panjang dan luas bayangan, serta membaca gambar dilatasi. 100 soal dengan kunci jawaban.",
                "Dilatasi [O, k]: (x, y) → (kx, ky)", "k &gt; 1 diperbesar, 0 &lt; k &lt; 1 diperkecil.", sets,
                ["Dilatasi dengan pusat O dan faktor skala k memetakan (x, y) ke (kx, ky). Bangun bayangan sebangun dengan bangun asal.",
                 "Jika k &gt; 1 bayangan diperbesar, jika 0 &lt; k &lt; 1 diperkecil, jika k negatif bayangan terletak di seberang pusat.",
                 "Dengan pusat P(a, b): (x, y) → (a + k(x − a), b + k(y − b)). Panjang dikali |k| dan luas dikali k²."],
                [("A(3, −2) didilatasi [O, 3].", ["(3 × 3, 3 × (−2))"], "A'(9, −6)"),
                 ("Persegi luas 8 cm² didilatasi k = 3. Luas bayangan?", ["8 × 3²"], "72 cm²")],
                [["(x, y) → (x + k, y + k)", "Dilatasi mengalikan: (kx, ky)"],
                 ["Luas bayangan = luas × k", "Luas bayangan = luas × k²"],
                 ["Faktor skala negatif berarti diperkecil", "Faktor negatif berarti bayangan terbalik di seberang pusat"]],
                [("Apa beda dilatasi dengan translasi, refleksi, dan rotasi?", "Dilatasi mengubah ukuran bangun, sedangkan ketiganya tidak."),
                 ("Apakah bayangan dilatasi sebangun dengan bangun asal?", "Ya. Bentuknya tetap, hanya ukurannya berubah dengan faktor skala k."),
                 ("Di mana dilatasi dipakai?", "Pada perbesaran foto, peta, proyektor, dan maket bangunan.")])


# ============================================================ 9. ukuran penyebaran
def u9():
    def data():
        n = ch([7, 11, 15])
        xs = [ri(40, 99) for _ in range(n)]
        return xs

    def kuart(xs):
        s = sorted(xs)
        n = len(s)
        return s[(n + 1) // 4 - 1], s[(n + 1) // 2 - 1], s[3 * (n + 1) // 4 - 1]

    def ds(xs):
        return "; ".join(num(x) for x in xs)

    def kuartil():
        xs = data()
        q1, q2, q3 = kuart(xs)
        if len({q1, q2, q3}) < 3:
            return None
        w = ri(0, 2)
        nm = ["kuartil bawah (Q₁)", "median (Q₂)", "kuartil atas (Q₃)"][w]
        v = [q1, q2, q3][w]
        return MN("Data: %s. Nilai %s adalah …" % (ds(xs), nm), v, [x for x in [q1, q2, q3] if x != v] + [xs[len(xs) // 4]], "Urutkan: %s. %s = %d." % (ds(sorted(xs)), nm.capitalize(), v))

    def iqr():
        xs = data()
        q1, q2, q3 = kuart(xs)
        k = ri(0, 1)
        if k == 0:
            return MN("Jangkauan antarkuartil dari data %s adalah …" % ds(xs), q3 - q1, [max(xs) - min(xs), q3 - q2, q2 - q1 if q2 - q1 != q3 - q2 else q3 - q1 + 1], "Q₁ = %d dan Q₃ = %d. Q₃ − Q₁ = %d." % (q1, q3, q3 - q1))
        return MN("Jangkauan dari data %s adalah …" % ds(xs), max(xs) - min(xs), [q3 - q1, max(xs), max(xs) - sorted(xs)[1]], "%d − %d = %d." % (max(xs), min(xs), max(xs) - min(xs)))

    def box():
        mn = ri(20, 40)
        q1 = mn + ri(3, 12)
        q2 = q1 + ri(3, 12)
        q3 = q2 + ri(3, 12)
        mx = q3 + ri(3, 12)
        X = lambda v: 30 + (v - 10) * 4.2
        s = [line(X(10), 80, X(100), 80, INK, 1.5)]
        for g in range(10, 101, 10):
            s.append(line(X(g), 76, X(g), 84, INK, 1.4) + text(X(g), 100, num(g), 12, weight=400))
        s.append(line(X(mn), 40, X(q1), 40, INK, 2) + line(X(q3), 40, X(mx), 40, INK, 2))
        s.append("<rect x='%.1f' y='22' width='%.1f' height='36' fill='#dfeafc' stroke='%s' stroke-width='2'/>" % (X(q1), X(q3) - X(q1), BLUE))
        s.append(line(X(q2), 22, X(q2), 58, RED, 2.6) + line(X(mn), 30, X(mn), 50, INK, 2) + line(X(mx), 30, X(mx), 50, INK, 2))
        for v in (mn, q1, q2, q3, mx):
            s.append(text(X(v), 16, num(v), 12, col=BLUE))
        pic = wrap(420, 110, "".join(s), "diagram kotak garis")
        k = ri(0, 3)
        if k == 0:
            return MN("Berdasarkan diagram kotak garis berikut, median data adalah …" + pic, q2, [q1, q3, (mn + mx) // 2 if (mn + mx) // 2 != q2 else q2 + 2], "Garis di dalam kotak menunjukkan median: %d." % q2)
        if k == 1:
            return MN("Berdasarkan diagram kotak garis berikut, jangkauan antarkuartil adalah …" + pic, q3 - q1, [mx - mn, q3 - q2, q2 - q1 if q2 - q1 != q3 - q2 else q3 - q1 + 2], "Q₃ − Q₁ = %d − %d = %d." % (q3, q1, q3 - q1))
        if k == 2:
            return MN("Berdasarkan diagram kotak garis berikut, kuartil bawah adalah …" + pic, q1, [mn, q2, q3], "Tepi kiri kotak adalah Q₁ = %d." % q1)
        return MN("Berdasarkan diagram kotak garis berikut, jangkauan data adalah …" + pic, mx - mn, [q3 - q1, mx, mx - q1], "Nilai terbesar − terkecil = %d − %d = %d." % (mx, mn, mx - mn))

    def pencilan():
        xs = data()
        q1, q2, q3 = kuart(xs)
        h = q3 - q1
        if h == 0:
            return None
        lo, hi = Fr(q1) - Fr(3, 2) * h, Fr(q3) + Fr(3, 2) * h
        k = ri(0, 1)
        if k == 0:
            return M("Q₁ = %d dan Q₃ = %d. Data dianggap pencilan jika kurang dari Q₁ − 1,5 × (Q₃ − Q₁) atau lebih dari Q₃ + 1,5 × (Q₃ − Q₁). Batas atasnya …" % (q1, q3), dz(hi), [dz(Fr(q3 + h)), dz(Fr(q3) + Fr(3, 2) * q3) if False else dz(hi + h), dz(lo)], "%d + 1,5 × %d = %s." % (q3, h, dz(hi)))
        out = int(hi) + ri(5, 20)
        ins = [q3, q2, int(hi) - 1 if int(hi) - 1 > q3 else q3 + 1]
        return MN("Q₁ = %d dan Q₃ = %d. Data dianggap pencilan jika lebih dari Q₃ + 1,5 × (Q₃ − Q₁). Manakah yang merupakan pencilan?" % (q1, q3), out, ins + [q1], "Batas atas %d + 1,5 × %d = %s. Hanya %d yang lebih besar." % (q3, h, dz(hi), out))

    def banding():
        a = data()
        b = [x + ri(-3, 3) for x in a]
        ra, rb = max(a) - min(a), max(b) - min(b)
        if ra == rb:
            return None
        F = ch([("Kelas A", "Kelas B")])
        return M("Nilai kelas A: %s. Nilai kelas B: %s. Data kelas mana yang jangkauannya lebih besar?" % (ds(a), ds(b)), "Kelas A" if ra > rb else "Kelas B", ["Kelas B" if ra > rb else "Kelas A", "Sama besar", "Tidak dapat ditentukan"],
                 "Jangkauan A = %d, jangkauan B = %d." % (ra, rb))

    sets = [("Kuartil", [(kuartil, 20)]),
            ("Jangkauan dan jangkauan antarkuartil", [(iqr, 20)]),
            ("Diagram kotak garis", [(box, 20)]),
            ("Pencilan", [(pencilan, 20)]),
            ("Membandingkan penyebaran data", [(banding, 10), (box, 5), (kuartil, 5)])]
    return unit("ukuran-penyebaran-data", "D", 9, "Ukuran Penyebaran Data: Kuartil dan Jangkauan", "Ukuran Penyebaran Data",
                "Peserta didik menentukan dan menafsirkan ukuran penyebaran data (jangkauan, kuartil, jangkauan antarkuartil), membaca diagram kotak garis, dan mengenali pencilan.",
                "Latihan ukuran penyebaran data kelas 9 SMP: kuartil bawah, median, kuartil atas, jangkauan, jangkauan antarkuartil, diagram kotak garis, pencilan, dan membandingkan penyebaran. 100 soal dengan kunci jawaban.",
                "Jangkauan antarkuartil = Q₃ − Q₁", "Q₁, Q₂, Q₃ membagi data terurut menjadi empat bagian.", sets,
                ["Urutkan data dulu. Median (Q₂) membagi data menjadi dua bagian. Q₁ adalah median bagian bawah, Q₃ median bagian atas.",
                 "Jangkauan = data terbesar − data terkecil. Jangkauan antarkuartil = Q₃ − Q₁ dan tidak terpengaruh data yang sangat besar atau kecil.",
                 "Diagram kotak garis menunjukkan lima nilai: terkecil, Q₁, Q₂, Q₃, dan terbesar. Pencilan adalah data di luar Q₁ − 1,5(Q₃ − Q₁) dan Q₃ + 1,5(Q₃ − Q₁)."],
                [("Data: 3; 5; 6; 8; 9; 11; 14. Q₁, Q₂, Q₃?", ["Q₂ = data ke-4", "Q₁ = data ke-2, Q₃ = data ke-6"], "5, 8, 11"),
                 ("Q₁ = 20, Q₃ = 32. Jangkauan antarkuartil?", ["32 − 20"], "12")],
                [["Kuartil dicari tanpa mengurutkan data", "Urutkan dulu"],
                 ["Jangkauan antarkuartil = Q₃ + Q₁", "Q₃ − Q₁"],
                 ["Garis tengah kotak dianggap rata-rata", "Garis tengah kotak adalah median"]],
                [("Mengapa perlu ukuran penyebaran?", "Dua kelompok data bisa punya rata-rata sama tetapi penyebarannya berbeda. Ukuran penyebaran menunjukkan seberapa beragam data itu."),
                 ("Apa itu pencilan?", "Data yang jauh lebih kecil atau lebih besar dari data lainnya, misalnya karena salah catat atau kejadian khusus."),
                 ("Apa kelebihan jangkauan antarkuartil?", "Tidak terpengaruh pencilan, karena hanya memakai 50% data di tengah.")])


# ============================================================ 10. peluang kejadian majemuk
def u10():
    def dadu2():
        F = [("jumlah mata dadu 7", lambda a, b: a + b == 7), ("jumlah mata dadu 10", lambda a, b: a + b == 10), ("jumlah mata dadu kurang dari 5", lambda a, b: a + b < 5),
             ("kedua mata dadu sama", lambda a, b: a == b), ("jumlah mata dadu 12", lambda a, b: a + b == 12), ("jumlah mata dadu lebih dari 9", lambda a, b: a + b > 9),
             ("hasil kali mata dadu 6", lambda a, b: a * b == 6), ("selisih mata dadu 2", lambda a, b: abs(a - b) == 2), ("jumlah mata dadu genap", lambda a, b: (a + b) % 2 == 0),
             ("jumlah mata dadu 5", lambda a, b: a + b == 5), ("jumlah mata dadu 9", lambda a, b: a + b == 9), ("mata dadu pertama lebih besar", lambda a, b: a > b),
             ("jumlah mata dadu 8", lambda a, b: a + b == 8), ("hasil kali mata dadu 12", lambda a, b: a * b == 12), ("selisih mata dadu 1", lambda a, b: abs(a - b) == 1),
             ("jumlah mata dadu 6", lambda a, b: a + b == 6), ("jumlah mata dadu 11", lambda a, b: a + b == 11), ("kedua mata dadu ganjil", lambda a, b: a % 2 and b % 2),
             ("hasil kali mata dadu genap", lambda a, b: a * b % 2 == 0), ("jumlah mata dadu prima", lambda a, b: a + b in (2, 3, 5, 7, 11)), ("salah satu mata dadu 6", lambda a, b: (a == 6) != (b == 6))]
        t, f = ch(F)
        n = sum(1 for a in range(1, 7) for b in range(1, 7) if f(a, b))
        v = Fr(n, 36)
        return M("Dua dadu dilempar bersama. Peluang %s adalah …" % t, fq(v), [fq(Fr(n, 12)) if Fr(n, 12) <= 1 and Fr(n, 12) != v else fq(Fr(n + 1, 36)), fq(Fr(36 - n, 36)), fq(Fr(n, 6)) if n < 6 else fq(Fr(n - 1, 36))],
                 "Ada 36 hasil. Yang memenuhi ada %d, jadi P = %d/36%s." % (n, n, " = " + fq(v) if v.numerator != n else ""))

    def koin():
        k = ri(0, 3)
        if k == 0:
            n = ri(2, 4)
            m = ri(0, n)
            c = math.comb(n, m)
            v = Fr(c, 2 ** n)
            sisi = ch(["gambar", "angka"])
            return M("%d koin dilempar bersama. Peluang muncul tepat %d %s adalah …" % (n, m, sisi), fq(v), [fq(Fr(1, 2 ** n)) if v != Fr(1, 2 ** n) else fq(Fr(1, 2)), fq(Fr(m, n)) if Fr(m, n) != v else fq(Fr(c + 1, 2 ** n)), fq(Fr(c, 2 * n))],
                     "Ada %d hasil, yang tepat %d %s ada %d. P = %s." % (2 ** n, m, sisi, c, fq(v)))
        if k == 1:
            F = [("gambar dan mata dadu genap", Fr(1, 4)), ("angka dan mata dadu 6", Fr(1, 12)), ("gambar dan mata dadu prima", Fr(1, 4)),
                 ("angka dan mata dadu lebih dari 4", Fr(1, 6)), ("gambar dan mata dadu kurang dari 3", Fr(1, 6)), ("angka dan mata dadu faktor dari 6", Fr(1, 3)),
                 ("gambar dan mata dadu 1", Fr(1, 12)), ("angka dan mata dadu ganjil", Fr(1, 4)), ("gambar dan mata dadu kelipatan 3", Fr(1, 6)),
                 ("angka dan mata dadu bukan 6", Fr(5, 12)), ("gambar dan mata dadu lebih dari 1", Fr(5, 12)), ("angka dan mata dadu kurang dari 5", Fr(1, 3))]
            t, v = ch(F)
            return M("Sebuah koin dan sebuah dadu dilempar bersama. Peluang muncul %s adalah …" % t, fq(v), [fq(v * 2), fq(v + Fr(1, 2)) if v + Fr(1, 2) < 1 else fq(Fr(1, 2)), fq(Fr(1, 12)) if v != Fr(1, 12) else fq(Fr(1, 6))],
                     "P = P(koin) × P(dadu) = %s." % fq(v))
        n = ri(2, 4)
        if ri(0, 1):
            v = Fr(n + 1, 2 ** n)
            return M("%d koin dilempar bersama. Peluang muncul paling banyak satu gambar adalah …" % n, fq(v), [fq(Fr(n, 2 ** n)), fq(Fr(1, 2 ** n)), fq(1 - v)],
                     "Tidak ada gambar (1 cara) atau tepat satu gambar (%d cara): %d/%d = %s." % (n, n + 1, 2 ** n, fq(v)))
        v = 1 - Fr(1, 2 ** n)
        return M("%d koin dilempar bersama. Peluang muncul paling sedikit satu gambar adalah …" % n, fq(v), [fq(Fr(1, 2 ** n)), fq(Fr(1, 2)), fq(Fr(n, 2 ** n))], "P = 1 − P(semua angka) = 1 − 1/%d = %s." % (2 ** n, fq(v)))

    def ambil():
        a, b = ri(2, 8), ri(2, 8)
        n = a + b
        k = ri(0, 2)
        ca, cb = ch([("merah", "biru"), ("hijau", "kuning"), ("putih", "hitam")])
        if k == 0:
            v = Fr(a, n) * Fr(a, n)
            return M("Kantong berisi %d bola %s dan %d bola %s. Diambil satu bola, dikembalikan, lalu diambil lagi. Peluang terambil dua bola %s …" % (a, ca, b, cb, ca), fq(v),
                     [fq(Fr(a, n) * Fr(a - 1, n - 1)), fq(Fr(2 * a, n)) if 2 * a <= n else fq(Fr(a, n)), fq(Fr(a, n) * Fr(b, n))], "Dikembalikan, jadi bebas: %d/%d × %d/%d = %s." % (a, n, a, n, fq(v)))
        if k == 1:
            v = Fr(a, n) * Fr(a - 1, n - 1)
            return M("Kantong berisi %d bola %s dan %d bola %s. Diambil dua bola satu per satu tanpa pengembalian. Peluang keduanya %s …" % (a, ca, b, cb, ca), fq(v),
                     [fq(Fr(a, n) * Fr(a, n)), fq(Fr(a, n) * Fr(a - 1, n)), fq(Fr(a - 1, n - 1))], "%d/%d × %d/%d = %s." % (a, n, a - 1, n - 1, fq(v)))
        v = Fr(a, n) * Fr(b, n - 1) + Fr(b, n) * Fr(a, n - 1)
        return M("Kantong berisi %d bola %s dan %d bola %s. Diambil dua bola satu per satu tanpa pengembalian. Peluang terambil warna berbeda …" % (a, ca, b, cb), fq(v),
                 [fq(Fr(a, n) * Fr(b, n - 1)), fq(Fr(a * b, n * n)), fq(1 - v)], "%s-%s atau %s-%s: %d/%d × %d/%d + %d/%d × %d/%d = %s." % (ca, cb, cb, ca, a, n, b, n - 1, b, n, a, n - 1, fq(v)))

    def bebas():
        p, q = ch([Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(4, 5), Fr(3, 5), Fr(7, 10), Fr(9, 10)]), ch([Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(4, 5), Fr(3, 5), Fr(1, 4)])
        k = ri(0, 2)
        a, b = ch([("Andi", "Budi"), ("Rina", "Sari"), ("Tono", "Dewi")])
        if k == 0:
            return M("Peluang %s lulus ujian %s dan peluang %s lulus %s. Peluang keduanya lulus …" % (a, fq(p), b, fq(q)), fq(p * q), [fq(p + q) if p + q <= 1 else fq((1 - p) * (1 - q)), fq((1 - p) * (1 - q)) if (1 - p) * (1 - q) != p * q else fq(p * (1 - q)), fq(p * (1 - q))],
                     "Kejadian saling bebas: %s × %s = %s." % (fq(p), fq(q), fq(p * q)))
        if k == 1:
            v = (1 - p) * (1 - q)
            return M("Peluang %s lulus ujian %s dan peluang %s lulus %s. Peluang keduanya tidak lulus …" % (a, fq(p), b, fq(q)), fq(v), [fq(p * q), fq(1 - p * q), fq(p * (1 - q))],
                     "(1 − %s) × (1 − %s) = %s." % (fq(p), fq(q), fq(v)))
        v = p * (1 - q) + (1 - p) * q
        return M("Peluang %s lulus ujian %s dan peluang %s lulus %s. Peluang tepat satu orang lulus …" % (a, fq(p), b, fq(q)), fq(v), [fq(p * (1 - q)), fq(p * q), fq(1 - v)],
                 "%s × %s + %s × %s = %s." % (fq(p), fq(1 - q), fq(1 - p), fq(q), fq(v)))

    def gabung():
        n = ri(10, 30)
        m = ch([3, 5])
        A = [x for x in range(1, n + 1) if x % 2 == 0]
        B = [x for x in range(1, n + 1) if x % m == 0]
        both = [x for x in A if x in B]
        k = ri(0, 1)
        if k == 0:
            u = len(A) + len(B) - len(both)
            v = Fr(u, n)
            return M("Kartu bernomor 1 sampai %d. Diambil satu kartu. Peluang terambil kartu genap atau kelipatan %d …" % (n, m), fq(v), [fq(Fr(len(A) + len(B), n)), fq(Fr(len(both), n)), fq(Fr(len(A), n))],
                     "Genap %d, kelipatan %d ada %d, keduanya %d. P = (%d + %d − %d)/%d = %s." % (len(A), m, len(B), len(both), len(A), len(B), len(both), n, fq(v)))
        v = Fr(len(both), n)
        return M("Kartu bernomor 1 sampai %d. Diambil satu kartu. Peluang terambil kartu genap dan kelipatan %d …" % (n, m), fq(v), [fq(Fr(len(A) + len(B) - len(both), n)), fq(Fr(len(A), n) * Fr(len(B), n)) if Fr(len(A), n) * Fr(len(B), n) != v else fq(Fr(len(both) + 1, n)), fq(Fr(len(B), n))],
                 "Yang genap dan kelipatan %d: %s. P = %d/%d%s." % (m, ", ".join(map(str, both)), len(both), n, " = " + fq(v) if v.numerator != len(both) else ""))

    sets = [("Dua dadu", [(dadu2, 15), (koin, 5)]),
            ("Koin dan dadu", [(koin, 20)]),
            ("Pengambilan dengan dan tanpa pengembalian", [(ambil, 20)]),
            ("Kejadian saling bebas", [(bebas, 20)]),
            ("Kejadian “atau” dan “dan”", [(gabung, 14), (ambil, 6)])]
    return unit("peluang-kejadian-majemuk", "D", 10, "Peluang Kejadian Majemuk", "Peluang Kejadian Majemuk",
                "Peserta didik menentukan peluang kejadian majemuk: dua dadu, koin dan dadu, pengambilan dengan dan tanpa pengembalian, kejadian saling bebas, serta gabungan dua kejadian.",
                "Latihan peluang kejadian majemuk kelas 9 SMP: dua dadu, beberapa koin, koin dan dadu, pengambilan bola dengan dan tanpa pengembalian, kejadian saling bebas, dan gabungan kejadian. 100 soal dengan kunci jawaban.",
                "Saling bebas: P(A dan B) = P(A) × P(B)", "Tanpa pengembalian: isi kantong berkurang.", sets,
                ["Untuk dua dadu, ada 6 × 6 = 36 hasil. Untuk n koin, ada 2ⁿ hasil. Hitung banyak hasil yang memenuhi, lalu bagi dengan banyak semua hasil.",
                 "Jika dua kejadian saling bebas, P(A dan B) = P(A) × P(B). Pada pengambilan tanpa pengembalian, peluang kedua dihitung dari isi kantong yang sudah berkurang.",
                 "P(A atau B) = P(A) + P(B) − P(A dan B). Peluang komplemen: P(bukan A) = 1 − P(A)."],
                [("Dua dadu. Peluang jumlah 7?", ["(1,6) (2,5) (3,4) (4,3) (5,2) (6,1)", "6/36"], "1/6"),
                 ("3 merah, 2 biru. Ambil 2 tanpa pengembalian, keduanya merah?", ["3/5 × 2/4"], "3/10")],
                [["Dua dadu dianggap 12 hasil", "Ada 6 × 6 = 36 hasil"],
                 ["Tanpa pengembalian dihitung 3/5 × 3/5", "Kedua kali 2/4 karena bola berkurang"],
                 ["P(A atau B) = P(A) + P(B) selalu", "Kurangi P(A dan B) jika ada irisan"]],
                [("Apa arti kejadian saling bebas?", "Hasil kejadian pertama tidak memengaruhi peluang kejadian kedua, misalnya melempar koin lalu dadu."),
                 ("Bagaimana memakai diagram pohon?", "Tulis setiap kemungkinan beserta peluangnya pada cabang, lalu kalikan peluang di sepanjang cabang."),
                 ("Apa beda dengan dan tanpa pengembalian?", "Dengan pengembalian, isi kantong tetap. Tanpa pengembalian, isi kantong berkurang sehingga peluang kedua berubah.")])


# ============================================================ 11. pola bilangan dan barisan
def u11():
    def suku_ar():
        a, b = nz(-10, 20), nz(-6, 9)
        n = ri(8, 40)
        xs = [a + i * b for i in range(4)]
        k = ri(0, 1)
        if k == 0:
            v = a + (n - 1) * b
            return MN("Suku ke-%d dari barisan %s, … adalah …" % (n, ", ".join(sn(x) for x in xs)), v, [a + n * b, n * b, v + b if v + b != a + n * b else v - 1], "Uₙ = a + (n − 1)b = %s + %d × %s = %s." % (sn(a), n - 1, par(b), sn(v)))
        c = "Uₙ = %s" % lin(b, a - b, "n")
        return M("Rumus suku ke-n dari barisan %s, … adalah …" % ", ".join(sn(x) for x in xs), c, ["Uₙ = %s" % lin(b, a, "n"), "Uₙ = %s" % lin(a, b, "n") if a != b else "Uₙ = %s" % lin(a + 1, b, "n"), "Uₙ = %s" % lin(b, a + b, "n")],
                 "a = %s, b = %s. Uₙ = %s + (n − 1)%s = %s." % (sn(a), sn(b), sn(a), par(b), lin(b, a - b, "n")))

    def jumlah():
        a, b = ri(1, 15), ri(1, 8)
        n = ri(5, 25)
        S_ = n * (2 * a + (n - 1) * b) // 2
        xs = [a + i * b for i in range(3)]
        return MN("Jumlah %d suku pertama barisan %s, … adalah …" % (n, ", ".join(num(x) for x in xs)), S_, [n * (a + (n - 1) * b), a + (n - 1) * b, n * (2 * a + n * b) // 2], "Sₙ = n/2 × (2a + (n − 1)b) = %d/2 × (%d + %d) = %s." % (n, 2 * a, (n - 1) * b, num(S_)))

    def geo():
        a, r = ri(1, 6), ch([2, 3, -2, 4])
        n = ri(4, 7)
        if abs(a * r ** (n - 1)) > 50000:
            return None
        xs = [a * r ** i for i in range(4)]
        v = a * r ** (n - 1)
        k = ri(0, 1)
        if k == 0:
            return MN("Suku ke-%d dari barisan %s, … adalah …" % (n, ", ".join(sn(x) for x in xs)), v, [a * r ** n, a * r * (n - 1), v // r if v % r == 0 else v + 1], "Uₙ = a × rⁿ⁻¹ = %d × %s%s = %s." % (a, par(r), sup(n - 1), sn(v)))
        return MN("Rasio barisan geometri %s, … adalah …" % ", ".join(sn(x) for x in xs), r, [xs[1] - xs[0], Fr(1, r), -r], "r = %s : %s = %s." % (sn(xs[1]), sn(xs[0]), sn(r)))

    def jenis():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(1, 9), ri(2, 7)
            xs = [a + i * b for i in range(5)]
            c = "aritmetika dengan beda %d" % b
        elif k == 1:
            a, r = ri(1, 5), ri(2, 4)
            xs = [a * r ** i for i in range(5)]
            c = "geometri dengan rasio %d" % r
        else:
            xs = [i * i for i in range(1, 6)] if ri(0, 1) else [i * (i + 1) // 2 for i in range(1, 6)]
            c = "bukan aritmetika dan bukan geometri"
        opts = ["aritmetika dengan beda %d" % (xs[1] - xs[0]), "geometri dengan rasio %s" % sn(Fr(xs[1], xs[0])), "bukan aritmetika dan bukan geometri", "aritmetika dengan beda %d" % (xs[2] - xs[1] + 1)]
        return M("Barisan %s, … termasuk barisan …" % ", ".join(num(x) for x in xs), c, [o for o in opts if o != c], "Periksa selisih dan perbandingan suku berurutan: %s." % c)

    def gambar():
        k = ri(0, 2)
        n = ri(5, 20)
        if k == 0:
            a, b = ch([(4, 3), (3, 2), (5, 4), (6, 5), (7, 6)])
            v = a + (n - 1) * b
            return MN("Pola batang korek api: pola ke-1 memakai %d batang, pola ke-2 memakai %d batang, pola ke-3 memakai %d batang. Banyak batang pada pola ke-%d …" % (a, a + b, a + 2 * b, n), v, [a * n, b * n, v + b], "Bertambah %d setiap pola: %d + (%d − 1) × %d = %d." % (b, a, n, b, v), unit="batang")
        if k == 1:
            return MN("Pola persegi: pola ke-1 terdiri dari 1 persegi kecil, pola ke-2 dari 4, pola ke-3 dari 9. Banyak persegi kecil pada pola ke-%d …" % n, n * n, [2 * n, n * n + 1, (n - 1) * (n - 1)], "Pola bilangan persegi: n² = %d." % (n * n), unit="persegi")
        return MN("Pola segitiga titik: 1, 3, 6, 10, … Banyak titik pada pola ke-%d …" % n, n * (n + 1) // 2, [n * n, n * (n - 1) // 2, n * (n + 1)], "Pola bilangan segitiga: n(n + 1)/2 = %d." % (n * (n + 1) // 2), unit="titik")

    def cerita():
        k = ri(0, 2)
        if k == 0:
            a, b, n = ri(5, 20) * 1000, ri(1, 5) * 1000, ri(6, 12)
            S_ = n * (2 * a + (n - 1) * b) // 2
            return M("Raka menabung %s pada bulan pertama. Setiap bulan tabungannya bertambah %s dari bulan sebelumnya. Jumlah tabungan selama %d bulan …" % (rp(a), rp(b), n), rp(S_),
                     [rp(a + (n - 1) * b), rp(n * a), rp(n * (a + (n - 1) * b))], "Sₙ = %d/2 × (2 × %s + %d × %s) = %s." % (n, num(a), n - 1, num(b), rp(S_)))
        if k == 1:
            a, b, n = ri(15, 30), ri(2, 4), ri(10, 25)
            return MN("Gedung pertunjukan: baris pertama %d kursi, setiap baris berikutnya %d kursi lebih banyak. Banyak kursi pada baris ke-%d …" % (a, b, n), a + (n - 1) * b, [a + n * b, n * b, a * n], "%d + (%d − 1) × %d = %d." % (a, n, b, a + (n - 1) * b), unit="kursi")
        a, r, n = ri(10, 50) * 10, 2, ri(3, 6)
        return MN("Banyak bakteri mula-mula %d dan menjadi dua kali lipat setiap jam. Banyak bakteri setelah %d jam …" % (a, n), a * 2 ** n, [a * 2 * n, a * 2 ** (n - 1), a + 2 ** n], "%d × 2%s = %s." % (a, sup(n), num(a * 2 ** n)), unit="bakteri")

    sets = [("Barisan aritmetika", [(suku_ar, 20)]),
            ("Deret aritmetika", [(jumlah, 20)]),
            ("Barisan geometri", [(geo, 14), (jenis, 6)]),
            ("Pola gambar", [(gambar, 20)]),
            ("Soal cerita", [(cerita, 14), (jenis, 6)])]
    return unit("pola-bilangan-dan-barisan", "A", 11, "Pola Bilangan, Barisan, dan Deret", "Pola Bilangan dan Barisan",
                "Peserta didik mengenali pola bilangan, menentukan suku ke-n barisan aritmetika dan geometri, menghitung jumlah deret aritmetika, dan menyelesaikan masalah kontekstual.",
                "Latihan pola bilangan dan barisan kelas 9 SMP: suku ke-n barisan aritmetika, rumus Uₙ, jumlah deret aritmetika, barisan geometri, pola gambar, dan soal cerita. 100 soal dengan kunci jawaban.",
                "Uₙ = a + (n − 1)b", "Barisan geometri: Uₙ = a × rⁿ⁻¹.", sets,
                ["Barisan aritmetika memiliki beda (b) tetap antara suku berurutan. Suku ke-n: Uₙ = a + (n − 1)b, dengan a suku pertama.",
                 "Jumlah n suku pertama deret aritmetika: Sₙ = n/2 × (2a + (n − 1)b) = n/2 × (a + Uₙ).",
                 "Barisan geometri memiliki rasio (r) tetap: setiap suku dikali r. Suku ke-n: Uₙ = a × rⁿ⁻¹."],
                [("Suku ke-20 dari 3, 7, 11, …?", ["a = 3, b = 4", "3 + 19 × 4"], "79"),
                 ("Suku ke-6 dari 2, 6, 18, …?", ["a = 2, r = 3", "2 × 3⁵"], "486")],
                [["Uₙ = a + nb", "Uₙ = a + (n − 1)b"],
                 ["Rasio dihitung dengan mengurangkan suku", "Rasio = suku : suku sebelumnya"],
                 ["Sₙ = n × Uₙ", "Sₙ = n/2 × (a + Uₙ)"]],
                [("Apa beda barisan dan deret?", "Barisan adalah urutan bilangan, misalnya 2, 5, 8. Deret adalah jumlah suku-sukunya, misalnya 2 + 5 + 8."),
                 ("Bagaimana mengenali barisan aritmetika?", "Selisih setiap dua suku berurutan selalu sama."),
                 ("Apa itu pola bilangan segitiga?", "1, 3, 6, 10, 15, …: banyak titik yang dapat disusun membentuk segitiga. Rumusnya n(n + 1)/2.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11]
