# -*- coding: utf-8 -*-
"""Indonesia / Matematika / Kelas 11 (SMA, Fase F)。python3 tools/id_smp.py 11 [番号…]"""
import math
from fractions import Fraction as Fr
import id_smp as S
from id_smp import (ri, ch, nz, sh, num, sn, par, pd, dz, fq, expr, lin, sup, pw, M, MN, MD, rp, NB, MINUS, mat,
                    kosy, kurve, figure, tab, unit, fig, wrap, text, line, INK, BLUE, RED, FILL, GREEN)
from id_sma10 import surd, sub, SIN, COS, TAN, neg


def quad(a, b, c, v="x"):
    return expr([(a, v + "²"), (b, v), (c, "")])


# ============================================================ 1. komposisi dan invers
def u1():
    def komposisi():
        a, b, c, d = nz(-5, 5), nz(-8, 8), nz(-4, 4), nz(-8, 8)
        k = ri(0, 2)
        f, g = lin(a, b), lin(c, d)
        if k == 0:
            r = lin(a * c, a * d + b)
            return M("Diketahui f(x) = %s dan g(x) = %s. Fungsi (f ∘ g)(x) adalah …" % (f, g), r, [lin(a * c, c * b + d), lin(a * c, b + d), lin(a + c, b + d)],
                     "(f ∘ g)(x) = f(g(x)) = %s(%s) %s %d = %s." % (sn(a) if a not in (1, -1) else ("" if a == 1 else MINUS), g, "+" if b > 0 else "−", abs(b), r))
        if k == 1:
            r = lin(a * c, c * b + d)
            return M("Diketahui f(x) = %s dan g(x) = %s. Fungsi (g ∘ f)(x) adalah …" % (f, g), r, [lin(a * c, a * d + b), lin(a * c, b + d), lin(a * c, -(c * b + d))],
                     "(g ∘ f)(x) = g(f(x)) = %s(%s) %s %d = %s." % (sn(c) if c not in (1, -1) else ("" if c == 1 else MINUS), f, "+" if d > 0 else "−", abs(d), r))
        p = ri(1, 3)
        q = nz(-5, 5)
        x = nz(-3, 3)
        g2 = quad(1, 0, q)
        val = a * (x * x + q) + b
        return MN("Diketahui f(x) = %s dan g(x) = %s. Nilai (f ∘ g)(%s) adalah …" % (f, g2, sn(x)), val, [(a * x + b) ** 2 + q, a * x + b + x * x + q, val + a],
                  "g(%s) = %s, lalu f(%s) = %s." % (sn(x), sn(x * x + q), sn(x * x + q), sn(val)))

    def invers():
        k = ri(0, 2)
        if k == 0:
            a, b = nz(-6, 6), nz(-9, 9)
            if abs(a) == 1:
                return None
            r = "%s" % S.fr(lin(1, -b), sn(a)) if a > 0 else S.fr(lin(-1, b), sn(-a))
            return M("Invers dari f(x) = %s adalah f⁻¹(x) = …" % lin(a, b), r, [S.fr(lin(1, b), sn(abs(a))), lin(Fr(1, a), -b), S.fr(sn(a), lin(1, -b))],
                     "y = %s → x = (y %s %d)/%s, jadi f⁻¹(x) = %s." % (lin(a, b), "−" if b > 0 else "+", abs(b), sn(a), r))
        if k == 1:
            a, b, c, d = nz(-5, 5), nz(-6, 6), nz(-3, 3), nz(-5, 5)
            if a * d - b * c == 0 or c == 0:
                return None
            f = S.fr(lin(a, b), lin(c, d))
            r = S.fr(lin(-d, b), lin(c, -a))
            return M("Invers dari f(x) = %s, x ≠ %s, adalah f⁻¹(x) = …" % (f, fq(Fr(-d, c))), r, [S.fr(lin(d, -b), lin(c, -a)), S.fr(lin(-d, b), lin(c, a)), S.fr(lin(c, d), lin(a, b))],
                     "Untuk f(x) = (ax + b)/(cx + d), f⁻¹(x) = (−dx + b)/(cx − a). Hasilnya %s." % r)
        a, b = nz(-6, 6), nz(-9, 9)
        y = nz(-10, 10)
        x = Fr(y - b, a)
        return M("Diketahui f(x) = %s. Nilai f⁻¹(%s) adalah …" % (lin(a, b), sn(y)), fq(x), [sn(a * y + b), fq(Fr(y + b, a)) if Fr(y + b, a) != x else fq(x + 1), fq(-x) if x else "1"],
                 "f⁻¹(%s) = x dengan f(x) = %s: %s = %s, x = %s." % (sn(y), sn(y), lin(a, b), sn(y), fq(x)))

    def cari_g():
        a, b, c, d = nz(-4, 4), nz(-8, 8), nz(-4, 4), nz(-8, 8)
        if abs(a) == 1:
            return None
        k = ri(0, 1)
        if k == 0:
            # f(x) = ax + b, (f∘g)(x) = a(cx + d) + b → cari g
            fg = lin(a * c, a * d + b)
            return M("Diketahui f(x) = %s dan (f ∘ g)(x) = %s. Fungsi g(x) adalah …" % (lin(a, b), fg), lin(c, d), [lin(a * c, d), lin(c, a * d), lin(c, d + b)],
                     "%s × g(x) %s %d = %s, jadi g(x) = %s." % (sn(a), "+" if b > 0 else "−", abs(b), fg, lin(c, d)))
        gf = lin(c * a, c * b + d)
        return M("Diketahui f(x) = %s dan (g ∘ f)(x) = %s. Fungsi g(x) adalah …" % (lin(a, b), gf), lin(c, d), [lin(c * a, d), lin(c, c * b + d), lin(a, d)],
                 "Misalkan g(x) = px + q: p(%s) + q = %s, sehingga p = %s dan q = %s." % (lin(a, b), gf, sn(c), sn(d)))

    def domain():
        k = ri(0, 2)
        if k == 0:
            c, d = nz(-4, 4), nz(-9, 9)
            x0 = Fr(-d, c)
            return M("Daerah asal fungsi f(x) = %s adalah …" % S.fr("%d" % ri(1, 9), lin(c, d)), "{x | x ≠ %s, x ∈ R}" % fq(x0), ["{x | x ≠ %s, x ∈ R}" % fq(-x0) if x0 else "{x | x ≠ 1, x ∈ R}", "{x | x &gt; %s, x ∈ R}" % fq(x0), "{x | x ∈ R}"],
                     "Penyebut tidak boleh 0: %s ≠ 0, x ≠ %s." % (lin(c, d), fq(x0)))
        if k == 1:
            a = nz(-9, 9)
            return M("Daerah asal fungsi f(x) = √(%s) adalah …" % lin(1, -a), "{x | x ≥ %s, x ∈ R}" % sn(a), ["{x | x ≤ %s, x ∈ R}" % sn(a), "{x | x &gt; %s, x ∈ R}" % sn(a), "{x | x ≥ %s, x ∈ R}" % sn(-a)],
                     "Bilangan di dalam akar tidak boleh negatif: %s ≥ 0, x ≥ %s." % (lin(1, -a), sn(a)))
        a, b = nz(-5, 5), nz(-9, 9)
        x = ri(-3, 3)
        return MN("Diketahui f(x) = %s dan g(x) = x². Nilai (g ∘ f)(%s) adalah …" % (lin(a, b), sn(x)), (a * x + b) ** 2, [a * x * x + b, (a * x + b) * 2, (a * x) ** 2 + b], "f(%s) = %s, lalu g(%s) = %s." % (sn(x), sn(a * x + b), sn(a * x + b), sn((a * x + b) ** 2)))

    def cerita():
        k = ri(0, 1)
        if k == 0:
            a, b = ri(2, 6), ri(1, 5) * 1000
            c, d = ri(2, 4), ri(10, 40)
            x = ri(5, 20)
            return M("Sebuah pabrik mengolah bahan x ton menjadi kertas g(x) = %dx + %d ton, lalu kertas itu dijual dengan pendapatan f(y) = %dy + %s ribu rupiah. Pendapatan jika bahan %d ton …" % (c, d, a, num(b), x),
                     "%s ribu rupiah" % num(a * (c * x + d) + b), ["%s ribu rupiah" % num(a * x + b), "%s ribu rupiah" % num(c * (a * x + b) + d), "%s ribu rupiah" % num(c * x + d)],
                     "g(%d) = %d, lalu f(%d) = %s." % (x, c * x + d, c * x + d, num(a * (c * x + d) + b)))
        a, b = Fr(9, 5), 32
        C = ri(-4, 8) * 5
        F = a * C + b
        if F.denominator != 1:
            return None
        return MN("Suhu Fahrenheit F = %s C + 32. Fungsi inversnya mengubah F ke C. Jika F = %s, maka C = …" % (fq(a), sn(F)), C, [int(F - 32), int(a * F + 32) if (a * F + 32).denominator == 1 else C + 5, C + 10],
                  "C = (F − 32) × 5/9 = (%s − 32) × 5/9 = %s." % (sn(F), sn(C)), unit="°C")

    sets = [("Fungsi komposisi", [(komposisi, 20)]),
            ("Fungsi invers", [(invers, 20)]),
            ("Mencari fungsi dari komposisi", [(cari_g, 20)]),
            ("Daerah asal dan nilai komposisi", [(domain, 20)]),
            ("Komposisi dalam kehidupan", [(cerita, 10), (komposisi, 5), (invers, 5)])]
    return unit("komposisi-fungsi-dan-fungsi-invers", "A", 1, "Komposisi Fungsi dan Fungsi Invers", "Komposisi Fungsi dan Fungsi Invers",
                "Peserta didik menentukan fungsi komposisi dan fungsi invers, daerah asal fungsi, dan menggunakannya untuk memodelkan masalah.",
                "Latihan komposisi fungsi dan fungsi invers kelas 11 SMA: (f ∘ g)(x), (g ∘ f)(x), nilai komposisi, mencari fungsi dari komposisi, invers fungsi linear dan pecahan, daerah asal, dan soal cerita. 100 soal dengan kunci jawaban.",
                "(f ∘ g)(x) = f(g(x))", "Kerjakan fungsi yang di kanan dulu.", sets,
                ["Komposisi (f ∘ g)(x) = f(g(x)): masukkan g(x) ke dalam f. Umumnya (f ∘ g)(x) ≠ (g ∘ f)(x).",
                 "Invers f⁻¹ membalik kerja f. Caranya: tulis y = f(x), nyatakan x dalam y, lalu tukar x dan y. Untuk f(x) = (ax + b)/(cx + d), f⁻¹(x) = (−dx + b)/(cx − a).",
                 "Daerah asal: penyebut tidak boleh 0 dan bilangan di dalam akar tidak boleh negatif."],
                [("f(x) = 2x + 1, g(x) = x − 3. (f ∘ g)(x)?", ["2(x − 3) + 1"], "2x − 5"),
                 ("f(x) = 3x − 6. f⁻¹(x)?", ["y = 3x − 6 → x = (y + 6)/3"], "f⁻¹(x) = (x + 6)/3")],
                [["(f ∘ g)(x) dihitung g(f(x))", "(f ∘ g)(x) = f(g(x)): g dulu"],
                 ["f⁻¹(x) = 1/f(x)", "f⁻¹ adalah invers fungsi, bukan kebalikan bilangan"],
                 ["Lupa syarat penyebut ≠ 0", "Tuliskan x ≠ … pada daerah asal"]],
                [("Apakah komposisi fungsi bersifat komutatif?", "Umumnya tidak: (f ∘ g)(x) biasanya berbeda dengan (g ∘ f)(x)."),
                 ("Kapan suatu fungsi mempunyai invers?", "Jika fungsinya korespondensi satu-satu (setiap nilai y berasal dari tepat satu x)."),
                 ("Apa hubungan grafik f dan f⁻¹?", "Grafik f⁻¹ adalah pencerminan grafik f terhadap garis y = x.")])


# ============================================================ 2. persamaan lingkaran
def u2():
    def pt(a, b):
        return "(%s, %s)" % (sn(a), sn(b))

    def eq(a, b, r2):
        sa = "x²" if a == 0 else "(%s)²" % lin(1, -a)
        sb = "y²" if b == 0 else "(%s)²" % lin(1, -b, "y")
        return "%s + %s = %s" % (sa, sb, sn(r2))

    def gen(a, b, r2):
        return "x² + y² %s = 0" % expr([(-2 * a, "x"), (-2 * b, "y"), (a * a + b * b - r2, "")]).replace("x", "x", 1) if False else expr([(1, "x²"), (1, "y²"), (-2 * a, "x"), (-2 * b, "y"), (a * a + b * b - r2, "")]) + " = 0"

    def bentuk():
        a, b, r = ri(-6, 6), ri(-6, 6), ri(1, 9)
        k = ri(0, 1)
        if k == 0:
            return M("Persamaan lingkaran dengan pusat %s dan jari-jari %d adalah …" % (pt(a, b), r), eq(a, b, r * r), [eq(-a, -b, r * r) if (a, b) != (0, 0) else eq(a, b, r), eq(a, b, r), eq(b, a, r * r) if a != b else eq(a, b, 2 * r * r)],
                     "(x − a)² + (y − b)² = r², dengan a = %s, b = %s, r² = %d." % (sn(a), sn(b), r * r))
        x1, y1 = a + ch([3, -3, 4, -4, 0, 5]), b + ch([4, -4, 3, -3, 5, 0])
        r2 = (x1 - a) ** 2 + (y1 - b) ** 2
        return M("Persamaan lingkaran dengan pusat %s dan melalui titik %s adalah …" % (pt(a, b), pt(x1, y1)), eq(a, b, r2), [eq(a, b, int(math.isqrt(r2))), eq(-a, -b, r2) if (a, b) != (0, 0) else eq(a, b, r2 + 1), eq(x1, y1, r2)],
                 "r² = (%s − %s)² + (%s − %s)² = %d." % (sn(x1), par(a), sn(y1), par(b), r2))

    def pusat():
        a, b, r = nz(-6, 6), nz(-6, 6), ri(1, 9)
        g = gen(a, b, r * r)
        k = ri(0, 1)
        if k == 0:
            return M("Pusat lingkaran %s adalah …" % g, pt(a, b), [pt(-a, -b), pt(2 * a, 2 * b), pt(b, a) if a != b else pt(a, -b)], "Pusat (−A/2, −B/2) = %s." % pt(a, b))
        return MN("Jari-jari lingkaran %s adalah …" % g, r, [r * r, r + 1, abs(a * a + b * b + r * r - a * a - b * b) if False else a * a + b * b], "r = √(a² + b² − C) = √(%d + %d − (%s)) = %d." % (a * a, b * b, sn(a * a + b * b - r * r), r))

    def posisi():
        a, b, r = ri(-4, 4), ri(-4, 4), ri(3, 8)
        x, y = a + ri(-r - 2, r + 2), b + ri(-r - 2, r + 2)
        d2 = (x - a) ** 2 + (y - b) ** 2
        t = "di dalam lingkaran" if d2 < r * r else ("pada lingkaran" if d2 == r * r else "di luar lingkaran")
        return M("Kedudukan titik %s terhadap lingkaran %s adalah …" % (pt(x, y), eq(a, b, r * r)), t, [o for o in ["di dalam lingkaran", "pada lingkaran", "di luar lingkaran", "di pusat lingkaran"] if o != t],
                 "Substitusi: %s + %s = %d, dibandingkan dengan r² = %d." % ("(%s)²" % sn(x - a), "(%s)²" % sn(y - b), d2, r * r))

    def singgung():
        T = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (4, 3, 5), (12, 5, 13), (0, 5, 5), (7, 0, 7), (2, 1, 0)]
        x1, y1, r = ch(T[:8])
        x1, y1 = x1 * ch([1, -1]), y1 * ch([1, -1])
        k = ri(0, 1)
        if k == 0:
            c = "%s = %d" % (expr([(x1, "x"), (y1, "y")]), r * r)
            return M("Persamaan garis singgung lingkaran x² + y² = %d di titik %s adalah …" % (r * r, pt(x1, y1)), c,
                     ["%s = %d" % (expr([(y1, "x"), (x1, "y")]), r * r) if x1 != y1 else "%s = %d" % (expr([(x1, "x"), (-y1, "y")]), r * r), "%s = %d" % (expr([(x1, "x"), (y1, "y")]), r), "%s = %d" % (expr([(-x1, "x"), (-y1, "y")]), r * r)],
                     "Garis singgung di (x₁, y₁) pada x² + y² = r²: x₁x + y₁y = r², yaitu %s." % c)
        d = ri(3, 13)
        rr = ri(2, 9)
        if d <= rr:
            return None
        L = d * d - rr * rr
        rt_ = math.isqrt(L)
        c = sn(rt_) if rt_ * rt_ == L else surd(1, L)
        return M("Titik P berjarak %d cm dari pusat lingkaran berjari-jari %d cm. Panjang garis singgung dari P ke lingkaran adalah … cm" % (d, rr), c, [sn(d - rr), surd(1, d * d + rr * rr) if math.isqrt(d * d + rr * rr) ** 2 != d * d + rr * rr else sn(math.isqrt(d * d + rr * rr)), sn(d + rr)],
                 "Garis singgung tegak lurus jari-jari: √(%d² − %d²) = %s cm." % (d, rr, c))

    sets = [("Menentukan persamaan lingkaran", [(bentuk, 20)]),
            ("Pusat dan jari-jari", [(pusat, 20)]),
            ("Kedudukan titik", [(posisi, 20)]),
            ("Garis singgung lingkaran", [(singgung, 20)]),
            ("Campuran", [(bentuk, 7), (pusat, 7), (singgung, 6)])]
    return unit("persamaan-lingkaran", "G", 2, "Persamaan Lingkaran dan Garis Singgung", "Persamaan Lingkaran",
                "Peserta didik menentukan persamaan lingkaran, pusat dan jari-jarinya, kedudukan titik terhadap lingkaran, dan persamaan serta panjang garis singgung lingkaran.",
                "Latihan persamaan lingkaran kelas 11 SMA: persamaan lingkaran dengan pusat dan jari-jari, bentuk umum x² + y² + Ax + By + C = 0, pusat dan jari-jari, kedudukan titik, dan garis singgung. 100 soal dengan kunci jawaban.",
                "(x − a)² + (y − b)² = r²", "Pusat (a, b), jari-jari r.", sets,
                ["Lingkaran dengan pusat (a, b) dan jari-jari r: (x − a)² + (y − b)² = r². Jika pusatnya O, persamaannya x² + y² = r².",
                 "Bentuk umum x² + y² + Ax + By + C = 0 mempunyai pusat (−A/2, −B/2) dan jari-jari √(A²/4 + B²/4 − C).",
                 "Garis singgung di titik (x₁, y₁) pada x² + y² = r²: x₁x + y₁y = r². Panjang garis singgung dari titik berjarak d dari pusat: √(d² − r²)."],
                [("Pusat (2, −3), jari-jari 4.", ["(x − 2)² + (y + 3)² = 16"], "(x − 2)² + (y + 3)² = 16"),
                 ("x² + y² − 6x + 8y − 11 = 0. Pusat dan jari-jari?", ["Pusat (3, −4)", "r = √(9 + 16 + 11)"], "(3, −4), r = 6")],
                [["Pusat x² + y² − 6x + 8y = 0 adalah (−3, 4)", "Pusat (−A/2, −B/2) = (3, −4)"],
                 ["(x − 2)² + (y + 3)² = 16 berjari-jari 16", "Jari-jari √16 = 4"],
                 ["Garis singgung di (3, 4): 3x + 4y = 5", "Ruas kanan r² = 25"]],
                [("Bagaimana mengecek titik di dalam atau di luar lingkaran?", "Substitusikan titik ke ruas kiri persamaan. Lebih kecil dari r² di dalam, sama dengan r² pada lingkaran, lebih besar di luar."),
                 ("Mengapa garis singgung tegak lurus jari-jari?", "Karena garis singgung hanya menyentuh lingkaran di satu titik, dan jarak terpendek dari pusat ke garis itu adalah jari-jari."),
                 ("Apa itu bentuk umum persamaan lingkaran?", "Bentuk x² + y² + Ax + By + C = 0 yang didapat dengan menjabarkan (x − a)² + (y − b)² = r².")])


# ============================================================ 3. korelasi dan regresi
def u3():
    def jenis():
        F = [("Makin lama belajar, makin tinggi nilai ujian.", "korelasi positif"), ("Makin tinggi suatu tempat, makin rendah suhunya.", "korelasi negatif"),
             ("Ukuran sepatu dan nilai ulangan matematika siswa.", "tidak ada korelasi"), ("Makin banyak kendaraan, makin tinggi polusi udara.", "korelasi positif"),
             ("Makin cepat kendaraan, makin singkat waktu tempuhnya.", "korelasi negatif"), ("Tinggi badan dan berat badan siswa.", "korelasi positif"),
             ("Harga barang naik, banyak barang yang terjual turun.", "korelasi negatif"), ("Nomor rumah dan banyak anggota keluarga.", "tidak ada korelasi"),
             ("Banyak jam bermain gim dan waktu tidur siswa.", "korelasi negatif"), ("Luas lahan sawah dan hasil panen padi.", "korelasi positif")]
        d, c = ch(F)
        return M("Hubungan berikut termasuk … <br>“%s”" % d, c, [o for o in ["korelasi positif", "korelasi negatif", "tidak ada korelasi", "korelasi sempurna"] if o != c],
                 "Positif: keduanya naik bersama. Negatif: satu naik, yang lain turun. Tidak ada: tidak terlihat pola.")

    def pencar():
        k = ri(0, 2)
        m = [1, -1, 0][k]
        pts = []
        for i in range(10):
            x = ri(1, 9)
            y = 5 + m * (x - 5) * 0.8 + R_noise() if m else ri(1, 9)
            pts.append((x, max(1, min(9, round(y)))))
        mx_ = sum(p[0] for p in pts) / 10.0
        my_ = sum(p[1] for p in pts) / 10.0
        sxy = sum((p[0] - mx_) * (p[1] - my_) for p in pts)
        sxx = sum((p[0] - mx_) ** 2 for p in pts)
        syy = sum((p[1] - my_) ** 2 for p in pts)
        if not sxx or not syy:
            return None
        rr = sxy / math.sqrt(sxx * syy)
        if (m == 1 and rr < 0.7) or (m == -1 and rr > -0.7) or (m == 0 and abs(rr) > 0.15):
            return None
        X = lambda v: 30 + v * 26
        Y = lambda v: 260 - v * 24
        s = [line(30, 260, 290, 260, INK, 2) + line(30, 260, 30, 20, INK, 2) + text(290, 278, "x", 14, italic=True) + text(18, 24, "y", 14, italic=True)]
        for x, y in pts:
            s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (X(x), Y(y), BLUE))
        pic = wrap(300, 285, "".join(s), "diagram pencar")
        c = ["korelasi positif", "korelasi negatif", "tidak ada korelasi"][k]
        return M("Diagram pencar berikut menunjukkan …" + pic, c, [o for o in ["korelasi positif", "korelasi negatif", "tidak ada korelasi", "korelasi sempurna"] if o != c],
                 "Lihat arah sebaran titik: naik ke kanan positif, turun ke kanan negatif, tidak berpola berarti tidak ada korelasi.")

    def r_nilai():
        F = [("0,92", "korelasi positif kuat"), ("−0,88", "korelasi negatif kuat"), ("0,15", "korelasi positif sangat lemah"), ("−0,10", "korelasi negatif sangat lemah"),
             ("0,55", "korelasi positif sedang"), ("−0,60", "korelasi negatif sedang"), ("1", "korelasi positif sempurna"), ("−1", "korelasi negatif sempurna"),
             ("0,97", "korelasi positif kuat"), ("−0,95", "korelasi negatif kuat"), ("0,45", "korelasi positif sedang"), ("−0,42", "korelasi negatif sedang")]
        r, c = ch(F)
        return M("Koefisien korelasi dua variabel adalah r = %s. Artinya …" % r, c, sh([o for o in ["korelasi positif kuat", "korelasi negatif kuat", "korelasi positif sedang", "korelasi negatif sedang", "korelasi positif sangat lemah", "korelasi negatif sangat lemah", "korelasi positif sempurna", "korelasi negatif sempurna"] if o != c]),
                 "Tanda r menunjukkan arah, |r| menunjukkan kekuatan: dekat 1 kuat, sekitar 0,5 sedang, dekat 0 lemah.")

    def prediksi():
        a, b = Fr(ri(5, 60)), Fr(ri(5, 40), 10)
        x = ri(3, 20)
        it = ch([("lama belajar (jam)", "nilai ujian", ""), ("luas rumah (m²)", "harga sewa (ratus ribu rupiah)", ""), ("suhu udara (°C)", "penjualan es (bungkus)", ""), ("banyak iklan", "penjualan (unit)", "")])
        k = ri(0, 1)
        if k == 0:
            v = a + b * x
            return MD("Persamaan regresi dengan x = %s dan y = %s adalah ŷ = %s + %sx. Perkiraan y untuk x = %d adalah …" % (it[0], it[1], dz(a), dz(b), x), v, [a * x + b, b * x, v + b],
                      "ŷ = %s + %s × %d = %s." % (dz(a), dz(b), x, dz(v)))
        return M("Persamaan regresi ŷ = %s + %sx, dengan x = %s dan y = %s. Arti koefisien %s adalah …" % (dz(a), dz(b), it[0], it[1], dz(b)),
                 "setiap x bertambah 1, y diperkirakan bertambah %s" % dz(b), ["setiap y bertambah 1, x bertambah %s" % dz(b), "nilai y jika x = 0", "setiap x bertambah 1, y bertambah %s" % dz(a)],
                 "Koefisien x (kemiringan) menyatakan perubahan rata-rata y untuk setiap kenaikan 1 satuan x.")

    def hitung():
        b = Fr(ri(2, 9), ch([1, 2]))
        a = ri(-5, 20)
        xs = sorted(sh(range(1, 13))[:5])
        ys = [a + b * x for x in xs]
        if any(Fr(y).denominator != 1 for y in ys):
            return None
        mx, my = Fr(sum(xs), 5), Fr(sum(ys), 5)
        k = ri(0, 1)
        t = "<table class='sn-table'><tbody><tr><td>x</td>%s</tr><tr><td>y</td>%s</tr></tbody></table>" % ("".join("<td>%d</td>" % x for x in xs), "".join("<td>%s</td>" % sn(y) for y in ys))
        if k == 0:
            return MD("Rata-rata x̄ dan ȳ dari data berikut adalah titik yang dilalui garis regresi. Nilai ȳ adalah …" + t, my, [mx, my + 1, Fr(sum(ys), 4)], "ȳ = %s : 5 = %s." % (sn(sum(ys)), dz(my)))
        return MD("Garis regresi data berikut mempunyai kemiringan b = %s dan melalui (x̄, ȳ). Konstanta a pada ŷ = a + bx adalah …" % dz(b) + t, my - b * mx, [my, mx - b * my, my + b * mx],
                  "x̄ = %s, ȳ = %s. a = ȳ − b x̄ = %s − %s × %s = %s." % (dz(mx), dz(my), dz(my), dz(b), dz(mx), dz(my - b * mx)))

    sets = [("Jenis korelasi", [(jenis, 10), (r_nilai, 10)]),
            ("Diagram pencar", [(pencar, 20)]),
            ("Koefisien korelasi", [(r_nilai, 2), (pencar, 8), (jenis, 0), (hitung, 10)]),
            ("Prediksi dengan regresi", [(prediksi, 20)]),
            ("Menentukan garis regresi", [(hitung, 10), (prediksi, 10)])]
    sets[2] = ("Rata-rata dan konstanta regresi", [(hitung, 20)])
    sets[4] = ("Regresi dan prediksi", [(prediksi, 12), (pencar, 8)])
    return unit("korelasi-dan-regresi-linear", "D", 3, "Diagram Pencar, Korelasi, dan Regresi Linear", "Korelasi dan Regresi",
                "Peserta didik menyajikan data bivariat dalam diagram pencar, menafsirkan korelasi, dan menggunakan garis regresi linear untuk membuat prediksi.",
                "Latihan korelasi dan regresi kelas 11 SMA: diagram pencar, korelasi positif, negatif, dan tidak ada korelasi, koefisien korelasi r, persamaan regresi linear, dan prediksi. 100 soal dengan kunci jawaban.",
                "ŷ = a + bx untuk memperkirakan y", "r dekat 1 atau −1: korelasi kuat.", sets,
                ["Diagram pencar menunjukkan hubungan dua variabel. Titik yang naik ke kanan menunjukkan korelasi positif, turun ke kanan korelasi negatif.",
                 "Koefisien korelasi r bernilai −1 sampai 1. Tandanya menunjukkan arah, nilai mutlaknya menunjukkan kekuatan hubungan.",
                 "Garis regresi ŷ = a + bx melalui (x̄, ȳ). Kemiringan b adalah perubahan y untuk setiap kenaikan 1 satuan x; a = ȳ − b x̄."],
                [("ŷ = 40 + 5x, x = 6?", ["40 + 30"], "70"),
                 ("b = 2, x̄ = 4, ȳ = 15. a?", ["15 − 2 × 4"], "7")],
                [["Korelasi berarti sebab-akibat", "Korelasi hanya menunjukkan hubungan, belum tentu sebab-akibat"],
                 ["r = −0,9 dianggap lemah karena negatif", "|r| = 0,9 berarti kuat; tandanya hanya arah"],
                 ["Memakai regresi untuk x yang jauh di luar data", "Prediksi paling dapat dipercaya di dalam rentang data"]],
                [("Apa itu data bivariat?", "Data yang terdiri dari pasangan dua variabel untuk setiap objek, misalnya lama belajar dan nilai ujian."),
                 ("Apakah korelasi kuat berarti sebab-akibat?", "Tidak selalu. Dua variabel bisa sama-sama dipengaruhi variabel lain."),
                 ("Untuk apa garis regresi?", "Untuk memperkirakan nilai satu variabel dari variabel lain berdasarkan pola data.")])


def R_noise():
    return S.R.uniform(-1.2, 1.2)


# ============================================================ 4. peluang bersyarat
def u4():
    def tabel():
        a, b, c, d = ri(3, 20), ri(3, 20), ri(3, 20), ri(3, 20)
        r1, r2 = ch([("Laki-laki", "Perempuan"), ("Kelas XI-1", "Kelas XI-2")])
        c1, c2 = ch([("Suka voli", "Suka basket"), ("Naik bus", "Naik motor"), ("Pramuka", "PMR")])
        t = "<table class='sn-table'><thead><tr><th></th><th>%s</th><th>%s</th></tr></thead><tbody><tr><td>%s</td><td>%d</td><td>%d</td></tr><tr><td>%s</td><td>%d</td><td>%d</td></tr></tbody></table>" % (c1, c2, r1, a, b, r2, c, d)
        k = ri(0, 2)
        if k == 0:
            v = Fr(a, a + b)
            return M("Dari tabel berikut dipilih satu siswa acak. Jika yang terpilih %s, peluang ia %s adalah …" % (r1.lower() if r1[0] == "L" else "dari " + r1, c1.lower()) + t, fq(v),
                     [fq(Fr(a, a + b + c + d)), fq(Fr(a, a + c)) if Fr(a, a + c) != v else fq(Fr(b, a + b)), fq(Fr(a + b, a + b + c + d))], "P(%s | %s) = %d/(%d + %d) = %s." % (c1.lower(), r1, a, a, b, fq(v)))
        if k == 1:
            v = Fr(c, a + c)
            return M("Dari tabel berikut dipilih satu siswa acak. Jika yang terpilih %s, peluang ia %s adalah …" % (c1.lower(), r2.lower() if r2[0] == "P" else "dari " + r2) + t, fq(v),
                     [fq(Fr(c, c + d)) if Fr(c, c + d) != v else fq(Fr(a, a + c)), fq(Fr(c, a + b + c + d)), fq(Fr(a, a + c)) if Fr(a, a + c) != v else fq(Fr(d, a + b + c + d))], "P(%s | %s) = %d/(%d + %d) = %s." % (r2, c1.lower(), c, a, c, fq(v)))
        n = a + b + c + d
        v = Fr(a, n)
        return M("Dari tabel berikut dipilih satu siswa acak. Peluang terpilih siswa %s dan %s adalah …" % (r1.lower() if r1[0] == "L" else "dari " + r1, c1.lower()) + t, fq(v),
                 [fq(x) for x in (Fr(a, a + b), Fr(a, a + c), Fr(a + b, n), Fr(a + c, n), Fr(b, n))], "%d dari %d siswa: %s." % (a, n, fq(v)))

    def tanpa():
        m, p = ri(2, 8), ri(2, 8)
        n = m + p
        k = ri(0, 1)
        if k == 0:
            v = Fr(m - 1, n - 1)
            return M("Kantong berisi %d bola merah dan %d bola putih. Diambil dua bola satu per satu tanpa pengembalian. Jika bola pertama merah, peluang bola kedua merah …" % (m, p), fq(v), [fq(Fr(m, n)), fq(Fr(m - 1, n)), fq(Fr(m, n) * Fr(m - 1, n - 1))],
                     "Setelah satu merah diambil, sisa %d merah dari %d bola: %s." % (m - 1, n - 1, fq(v)))
        v = Fr(m, n) * Fr(p, n - 1)
        return M("Kantong berisi %d bola merah dan %d bola putih. Diambil dua bola satu per satu tanpa pengembalian. Peluang pertama merah dan kedua putih …" % (m, p), fq(v), [fq(Fr(m, n) * Fr(p, n)), fq(Fr(p, n - 1)), fq(Fr(m * p, n * n - 1))],
                 "P = %d/%d × %d/%d = %s." % (m, n, p, n - 1, fq(v)))

    def rumus():
        pa = Fr(ri(2, 8), 10)
        pab = pa * Fr(ri(1, 4), 5)
        k = ri(0, 1)
        if k == 0:
            v = pab / pa
            return MD("Diketahui P(A) = %s dan P(A ∩ B) = %s. Nilai P(B | A) adalah …" % (dz(pa), dz(pab)), v, [pab * pa, pa / pab if pab else 1, pa - pab], "P(B | A) = P(A ∩ B)/P(A) = %s/%s = %s." % (dz(pab), dz(pa), dz(v)))
        pba = Fr(ri(1, 9), 10)
        v = pa * pba
        return MD("Diketahui P(A) = %s dan P(B | A) = %s. Nilai P(A ∩ B) adalah …" % (dz(pa), dz(pba)), v, [pa + pba if pa + pba <= 1 else pa, pba / pa if (pba / pa) <= 1 else pba, v * 2 if v * 2 <= 1 else v / 2], "P(A ∩ B) = P(A) × P(B | A) = %s × %s = %s." % (dz(pa), dz(pba), dz(v)))

    def dadu():
        F = [("jumlah mata dadu 8", "mata dadu pertama 3", 1, 6), ("kedua mata dadu genap", "jumlah mata dadu genap", 9, 18), ("jumlah mata dadu 10", "salah satu mata dadu 5", 1, 11),
             ("jumlah mata dadu lebih dari 9", "mata dadu pertama 6", 3, 6), ("kedua mata dadu sama", "jumlah mata dadu 8", 1, 5), ("mata dadu pertama 4", "jumlah mata dadu 7", 1, 6),
             ("jumlah mata dadu 7", "mata dadu pertama ganjil", 3, 18), ("kedua mata dadu ganjil", "jumlah mata dadu genap", 9, 18), ("salah satu mata dadu 6", "jumlah mata dadu 10", 2, 3)]
        a, b, n, d = ch(F)
        v = Fr(n, d)
        return M("Dua dadu dilempar. Diketahui %s. Peluang %s adalah …" % (b, a), fq(v), [fq(x) for x in (Fr(n, 36), Fr(d, 36), Fr(n, d + 1), Fr(n + 1, d), Fr(d - n, d), Fr(n, 6))],
                 "Ruang sampel baru: %d hasil dengan %s. Yang juga %s ada %d. P = %s." % (d, b, a, n, fq(v)))

    def bayes():
        p1, p2 = ch([(Fr(6, 10), Fr(4, 10)), (Fr(7, 10), Fr(3, 10)), (Fr(1, 2), Fr(1, 2)), (Fr(3, 5), Fr(2, 5))])
        r1, r2 = Fr(ri(1, 5), 100), Fr(ri(1, 8), 100)
        k = ri(0, 1)
        tot = p1 * r1 + p2 * r2
        if k == 0:
            return MD("Mesin A membuat %s%% dan mesin B %s%% produk. Persentase produk cacat mesin A %s%% dan mesin B %s%%. Peluang sebuah produk acak cacat …" % (dz(p1 * 100), dz(p2 * 100), dz(r1 * 100), dz(r2 * 100)), tot,
                      [r1 + r2, (r1 + r2) / 2 if (r1 + r2) / 2 != tot else tot * 2, p1 * r1], "P = %s × %s + %s × %s = %s." % (dz(p1), dz(r1), dz(p2), dz(r2), dz(tot)))
        v = p1 * r1 / tot
        if not S.endlich(v) or len(dz(v)) > 6:
            return M("Mesin A membuat %s%% dan mesin B %s%% produk, dengan persentase cacat %s%% dan %s%%. Jika sebuah produk cacat, peluang produk itu dari mesin A …" % (dz(p1 * 100), dz(p2 * 100), dz(r1 * 100), dz(r2 * 100)), fq(v),
                     [fq(p1 * r1), fq(r1 / (r1 + r2)) if r1 / (r1 + r2) != v else fq(p1), fq(1 - v)], "P(A | cacat) = (%s × %s)/%s = %s." % (dz(p1), dz(r1), dz(tot), fq(v)))
        return MD("Mesin A membuat %s%% dan mesin B %s%% produk, dengan persentase cacat %s%% dan %s%%. Jika sebuah produk cacat, peluang produk itu dari mesin A …" % (dz(p1 * 100), dz(p2 * 100), dz(r1 * 100), dz(r2 * 100)), v,
                  [p1 * r1, r1 / (r1 + r2) if r1 / (r1 + r2) != v else p1, 1 - v], "P(A | cacat) = (%s × %s)/%s = %s." % (dz(p1), dz(r1), dz(tot), dz(v)))

    sets = [("Peluang bersyarat dari tabel", [(tabel, 20)]),
            ("Pengambilan tanpa pengembalian", [(tanpa, 20)]),
            ("Rumus peluang bersyarat", [(rumus, 20)]),
            ("Peluang bersyarat pada dadu dan tabel", [(dadu, 9), (tabel, 11)]),
            ("Peluang total dan teorema Bayes", [(bayes, 20)])]
    return unit("peluang-bersyarat", "D", 4, "Peluang Bersyarat dan Teorema Bayes", "Peluang Bersyarat",
                "Peserta didik menentukan peluang bersyarat dari tabel kontingensi, pengambilan tanpa pengembalian, dan kejadian berurutan, serta menggunakan aturan peluang total dan teorema Bayes.",
                "Latihan peluang bersyarat kelas 11 SMA: peluang bersyarat dari tabel kontingensi, pengambilan tanpa pengembalian, rumus P(B | A), dadu, peluang total, dan teorema Bayes. 100 soal dengan kunci jawaban.",
                "P(B | A) = P(A ∩ B) : P(A)", "Ruang sampel menyempit menjadi kejadian A.", sets,
                ["Peluang bersyarat P(B | A) adalah peluang B terjadi jika diketahui A sudah terjadi: P(B | A) = P(A ∩ B)/P(A).",
                 "Pada tabel kontingensi, peluang bersyarat dihitung dari baris atau kolom yang diketahui saja.",
                 "Peluang total: P(B) = P(A₁)P(B | A₁) + P(A₂)P(B | A₂). Teorema Bayes: P(A₁ | B) = P(A₁)P(B | A₁)/P(B)."],
                [("P(A) = 0,5, P(A ∩ B) = 0,2. P(B | A)?", ["0,2 : 0,5"], "0,4"),
                 ("5 merah, 3 putih, tanpa pengembalian. Merah lalu merah?", ["5/8 × 4/7"], "5/14")],
                [["P(B | A) = P(A ∩ B)", "Bagi dengan P(A)"],
                 ["Tanpa pengembalian dihitung seperti dikembalikan", "Peluang kedua memakai isi kantong yang berkurang"],
                 ["Dari tabel, dibagi dengan jumlah seluruh siswa", "Bagi dengan jumlah pada baris atau kolom yang diketahui"]],
                [("Apa beda P(A ∩ B) dan P(B | A)?", "P(A ∩ B) adalah peluang keduanya terjadi dari seluruh ruang sampel. P(B | A) adalah peluang B jika A sudah pasti terjadi."),
                 ("Kapan P(B | A) = P(B)?", "Jika A dan B saling bebas."),
                 ("Untuk apa teorema Bayes?", "Untuk membalik arah peluang, misalnya dari peluang cacat jika dari mesin A menjadi peluang dari mesin A jika produknya cacat.")])


# ============================================================ 5. polinomial
def u5():
    def peval(cs, x):
        v = 0
        for c in cs:
            v = v * x + c
        return v

    def pstr(cs):
        n = len(cs) - 1
        return expr([(c, ("x" + (sup(n - i) if n - i > 1 else "")) if n - i > 0 else "") for i, c in enumerate(cs)])

    def nilai():
        cs = [nz(-4, 4)] + [ri(-6, 6) for _ in range(ri(2, 3))]
        x = nz(-3, 3)
        k = ri(0, 2)
        v = peval(cs, x)
        if k == 0:
            return MN("Nilai P(x) = %s untuk x = %s adalah …" % (pstr(cs), sn(x)), v, [peval(cs, -x), v + cs[-1], peval(cs[::-1], x) if peval(cs[::-1], x) != v else v + 2], "Substitusi x = %s: P(%s) = %s." % (sn(x), sn(x), sn(v)))
        if k == 1:
            return MN("Derajat polinomial %s adalah …" % pstr(cs), len(cs) - 1, [len(cs), len(cs) - 2, cs[0]] if cs[0] not in (len(cs), len(cs) - 2, len(cs) - 1) else [len(cs), len(cs) - 2, len(cs) + 1], "Pangkat tertinggi x adalah %d." % (len(cs) - 1))
        return MN("Sisa pembagian P(x) = %s oleh (%s) adalah …" % (pstr(cs), lin(1, -x)), v, [peval(cs, -x), v + 1, cs[-1]], "Teorema sisa: sisanya P(%s) = %s." % (sn(x), sn(v)))

    def horner():
        q = [nz(-3, 3), ri(-5, 5), ri(-6, 6)]
        a = nz(-3, 3)
        r = ri(-8, 8)
        # P = (x − a) q + r
        cs = [q[0], q[1] - a * q[0], q[2] - a * q[1], r - a * q[2]]
        k = ri(0, 1)
        if k == 0:
            return M("Hasil bagi P(x) = %s oleh (%s) adalah …" % (pstr(cs), lin(1, -a)), pstr(q), [pstr([q[0], q[1] + 2 * a * q[0], q[2]]), pstr([q[0], -q[1], q[2]]) if q[1] else pstr([q[0], 1, q[2]]), pstr([q[0], q[1], q[2] + r])],
                     "Dengan cara Horner (bagan) memakai %s, hasil baginya %s dan sisanya %s." % (sn(a), pstr(q), sn(r)))
        return MN("Sisa pembagian P(x) = %s oleh (%s) adalah …" % (pstr(cs), lin(1, -a)), r, [peval(cs, -a), r + q[-1], cs[-1]], "Sisa = P(%s) = %s." % (sn(a), sn(r)))

    def faktor():
        r1, r2, r3 = sh([x for x in range(-5, 6) if x])[:3]
        cs = [1, -(r1 + r2 + r3), r1 * r2 + r1 * r3 + r2 * r3, -r1 * r2 * r3]
        k = ri(0, 2)
        if k == 0:
            lo = sorted([r1, r2, r3])
            return M("Akar-akar persamaan %s = 0 adalah …" % pstr(cs), ", ".join(sn(x) for x in lo), [", ".join(sn(-x) for x in sorted([r1, r2, r3], reverse=True)), ", ".join(sn(x) for x in [lo[0], lo[1], -lo[2]]), ", ".join(sn(x) for x in [-lo[0], lo[1], lo[2]])],
                     "Coba faktor dari %s; ternyata P(%s) = P(%s) = P(%s) = 0." % (sn(cs[-1]), sn(r1), sn(r2), sn(r3)))
        if k == 1:
            v = r1 + r2 + r3
            return MN("Jumlah akar-akar persamaan %s = 0 adalah …" % pstr(cs), v, [-v if v else 1, r1 * r2 * r3, cs[2]], "x₁ + x₂ + x₃ = −b/a = %s." % sn(v))
        a = nz(-4, 4)
        c0 = ri(-6, 6)
        # P(x) = x³ + c1 x² + c0 x + k habis dibagi (x − a) → P(a) = 0
        c1 = ri(-4, 4)
        kk = -(a ** 3 + c1 * a * a + c0 * a)
        return MN("Polinomial %s + k habis dibagi (%s). Nilai k adalah …" % (pstr([1, c1, c0, 0]).rstrip(), lin(1, -a)), kk, [-kk if kk else 1, a ** 3 + c1 * a * a + c0 * a + 1, kk + a], "P(%s) = 0: %s + k = 0, jadi k = %s." % (sn(a), sn(-kk), sn(kk)))

    def operasi():
        p = [nz(-4, 4), ri(-5, 5), ri(-6, 6)]
        q = [nz(-3, 3), ri(-5, 5)]
        k = ri(0, 1)
        if k == 0:
            s_ = [p[0], p[1] + q[0], p[2] + q[1]]
            return M("Jika P(x) = %s dan Q(x) = %s, maka P(x) − Q(x) = …" % (pstr(p), pstr(q)), pstr([p[0], p[1] - q[0], p[2] - q[1]]), [pstr(s_), pstr([p[0] - q[0], p[1] - q[1], p[2]]), pstr([p[0], p[1] - q[0], p[2] + q[1]])],
                     "Kurangkan suku sejenis: %s." % pstr([p[0], p[1] - q[0], p[2] - q[1]]))
        r = [p[0] * q[0], p[0] * q[1] + p[1] * q[0], p[1] * q[1] + p[2] * q[0], p[2] * q[1]]
        return M("Hasil kali (%s)(%s) adalah …" % (pstr(p), pstr(q)), pstr(r), [pstr([p[0] * q[0], p[1] * q[0], p[2] * q[0], p[2] * q[1]]), pstr([p[0] * q[0], p[0] * q[1] + p[1] * q[0], p[2] * q[1]]), pstr([r[0], r[1], r[2], -r[3]]) if r[3] else pstr([r[0], r[1], r[2] + 1, 0])],
                 "Kalikan setiap suku: %s." % pstr(r))

    sets = [("Nilai dan derajat polinomial", [(nilai, 20)]),
            ("Penjumlahan dan perkalian polinomial", [(operasi, 20)]),
            ("Pembagian cara Horner", [(horner, 20)]),
            ("Teorema sisa", [(nilai, 8), (horner, 12)]),
            ("Teorema faktor dan akar", [(faktor, 20)])]
    sets[3] = ("Teorema sisa dan faktor", [(faktor, 20)])
    sets[4] = ("Campuran", [(nilai, 7), (horner, 7), (operasi, 6)])
    return unit("polinomial", "A", 5, "Polinomial: Operasi, Pembagian, Teorema Sisa, dan Teorema Faktor", "Polinomial",
                "Peserta didik melakukan operasi pada polinomial, membagi polinomial dengan cara Horner, serta menggunakan teorema sisa dan teorema faktor untuk menentukan akar-akar polinomial.",
                "Latihan polinomial kelas 11 SMA: derajat dan nilai polinomial, penjumlahan dan perkalian, pembagian cara Horner (bagan), teorema sisa, teorema faktor, dan akar-akar persamaan suku banyak. 100 soal dengan kunci jawaban.",
                "Sisa P(x) : (x − a) adalah P(a)", "(x − a) faktor P(x) jika P(a) = 0.", sets,
                ["Polinomial (suku banyak) berderajat n mempunyai pangkat tertinggi xⁿ. Nilainya dihitung dengan substitusi atau cara Horner.",
                 "Pembagian P(x) oleh (x − a) menghasilkan P(x) = (x − a)H(x) + S. Teorema sisa: S = P(a).",
                 "Teorema faktor: (x − a) adalah faktor P(x) jika dan hanya jika P(a) = 0. Akar bulat persamaan suku banyak adalah faktor dari konstantanya."],
                [("Sisa x³ − 2x² + 4 dibagi (x − 2)?", ["P(2) = 8 − 8 + 4"], "4"),
                 ("x³ − 6x² + 11x − 6 = 0", ["P(1) = 0, P(2) = 0, P(3) = 0"], "1, 2, 3")],
                [["Sisa dibagi (x + 2) adalah P(2)", "x + 2 = x − (−2), jadi sisanya P(−2)"],
                 ["Melewatkan koefisien 0 pada cara Horner", "Tulis 0 untuk pangkat yang tidak ada"],
                 ["Jumlah akar = b/a", "Jumlah akar x³ + bx² + … adalah −b/a"]],
                [("Apa itu cara Horner?", "Cara cepat membagi polinomial dengan (x − a) memakai bagan koefisien: turunkan, kalikan dengan a, lalu jumlahkan."),
                 ("Bagaimana mencari akar polinomial berderajat tiga?", "Coba faktor-faktor konstanta. Jika satu akar ditemukan, bagi polinomial itu lalu selesaikan sisa persamaan kuadratnya."),
                 ("Apa hubungan sisa dan faktor?", "Jika sisa pembagian oleh (x − a) adalah 0, maka (x − a) adalah faktor.")])


# ============================================================ 6. matriks
def u6():
    def M2():
        return [[nz(-6, 6), nz(-6, 6)], [nz(-6, 6), nz(-6, 6)]]

    def ordo():
        r, c = ri(1, 3), ri(1, 3)
        A = [[nz(-9, 9) for _ in range(c)] for _ in range(r)]
        k = ri(0, 1)
        if k == 0 or r == c:
            return M("Ordo matriks A = %s adalah …" % mat(A), "%d × %d" % (r, c), ["%d × %d" % (c, r) if r != c else "%d × %d" % (r, c + 1), "%d × %d" % (r * c, 1), "%d × %d" % (r + 1, c)] if r != c else ["%d × %d" % (r, c + 1), "%d × %d" % (r + 1, c), "%d × %d" % (r * c, 1)],
                     "Ordo = banyak baris × banyak kolom = %d × %d." % (r, c))
        if min(r, c) < 2:
            return None
        T = [list(x) for x in zip(*A)]
        return M("Transpose matriks A = %s adalah …" % mat(A), mat(T), [mat([row[::-1] for row in A]), mat([[-x for x in row] for row in A]), mat(A[::-1])], "Baris menjadi kolom: Aᵀ = %s." % mat(T))

    def jumlah():
        A, B = M2(), M2()
        p, q = ch([1, 2, 3, -1]), ch([1, -1, 2, -2])
        Cm = [[p * A[i][j] + q * B[i][j] for j in range(2)] for i in range(2)]
        lab = expr([(p, "A"), (q, "B")])
        return M("Diketahui A = %s dan B = %s. Matriks %s adalah …" % (mat(A), mat(B), lab), mat(Cm),
                 [mat([[p * A[i][j] - q * B[i][j] for j in range(2)] for i in range(2)]), mat([[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]) if (p, q) != (1, 1) else mat([[A[i][j] * B[i][j] for j in range(2)] for i in range(2)]), mat([[Cm[j][i] for j in range(2)] for i in range(2)]) if Cm[0][1] != Cm[1][0] else mat([[Cm[i][j] + 1 for j in range(2)] for i in range(2)])],
                 "Operasikan elemen yang seletak: %s." % mat(Cm))

    def kali():
        A, B = M2(), M2()
        P = [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        wrong1 = [[A[i][j] * B[i][j] for j in range(2)] for i in range(2)]
        BA = [[sum(B[i][k] * A[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        return M("Diketahui A = %s dan B = %s. Hasil AB adalah …" % (mat(A), mat(B)), mat(P), [mat(wrong1), mat(BA) if BA != P else mat([[P[i][j] + 1 for j in range(2)] for i in range(2)]), mat([[P[i][j] if (i, j) != (0, 0) else -P[0][0] for j in range(2)] for i in range(2)]) if P[0][0] else mat([[P[i][j] + 2 for j in range(2)] for i in range(2)])],
                 "Baris × kolom: elemen baris 1 kolom 1 = %s × %s + %s × %s = %s, dan seterusnya." % (sn(A[0][0]), par(B[0][0]), par(A[0][1]), par(B[1][0]), sn(P[0][0])))

    def det():
        k = ri(0, 1)
        if k == 0:
            A = M2()
            d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
            return MN("Determinan matriks A = %s adalah …" % mat(A), d, [A[0][0] * A[1][1] + A[0][1] * A[1][0], A[0][1] * A[1][0] - A[0][0] * A[1][1] if d else 1, A[0][0] * A[0][1] - A[1][0] * A[1][1]],
                      "det A = ad − bc = %s × %s − %s × %s = %s." % (sn(A[0][0]), par(A[1][1]), par(A[0][1]), par(A[1][0]), sn(d)))
        A = [[ri(-3, 4) for _ in range(3)] for _ in range(3)]
        a = A
        d = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
        pos = a[0][0] * a[1][1] * a[2][2] + a[0][1] * a[1][2] * a[2][0] + a[0][2] * a[1][0] * a[2][1]
        return MN("Determinan matriks %s adalah …" % mat(A), d, [pos, -d if d else 1, d + 2], "Aturan Sarrus: jumlah hasil kali diagonal ke kanan dikurangi jumlah hasil kali diagonal ke kiri = %s." % sn(d))

    def invers():
        while True:
            A = M2()
            d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
            if d in (1, -1, 2, -2):
                break
        inv = [[Fr(A[1][1], d), Fr(-A[0][1], d)], [Fr(-A[1][0], d), Fr(A[0][0], d)]]
        f = lambda m: mat([[fq(x) for x in row] for row in m])
        return M("Invers matriks A = %s adalah …" % mat(A), f(inv), [f([[Fr(A[1][1], -d), Fr(-A[0][1], -d)], [Fr(-A[1][0], -d), Fr(A[0][0], -d)]]), f([[Fr(A[0][0], d), Fr(A[0][1], d)], [Fr(A[1][0], d), Fr(A[1][1], d)]]), f([[Fr(A[1][1]), Fr(-A[0][1])], [Fr(-A[1][0]), Fr(A[0][0])]]) if abs(d) != 1 else f([[Fr(-A[1][1]), Fr(A[0][1])], [Fr(A[1][0]), Fr(A[0][0])]])],
                 "A⁻¹ = (1/det A) × (tukar a dan d, ubah tanda b dan c), dengan det A = %s." % sn(d))

    def persamaan():
        while True:
            A = M2()
            d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
            if d:
                break
        x, y = nz(-6, 6), nz(-6, 6)
        b = [A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y]
        return M("Jika %s %s = %s, nilai x dan y adalah …" % (mat(A), mat([["x"], ["y"]]), mat([[b[0]], [b[1]]])), "x = %s, y = %s" % (sn(x), sn(y)),
                 ["x = %s, y = %s" % (sn(y), sn(x)) if x != y else "x = %s, y = %s" % (sn(-x), sn(y)), "x = %s, y = %s" % (sn(-x), sn(-y)), "x = %s, y = %s" % (sn(x + 1), sn(y))],
                 "Kalikan: %s = %s dan %s = %s, lalu selesaikan." % (expr([(A[0][0], "x"), (A[0][1], "y")]), sn(b[0]), expr([(A[1][0], "x"), (A[1][1], "y")]), sn(b[1])))

    sets = [("Ordo dan transpose", [(ordo, 20)]),
            ("Penjumlahan dan perkalian skalar", [(jumlah, 20)]),
            ("Perkalian matriks", [(kali, 20)]),
            ("Determinan", [(det, 20)]),
            ("Invers dan persamaan matriks", [(invers, 10), (persamaan, 10)])]
    return unit("matriks", "A", 6, "Matriks: Operasi, Determinan, dan Invers", "Matriks",
                "Peserta didik melakukan operasi pada matriks (penjumlahan, perkalian skalar, perkalian matriks), menentukan determinan dan invers, serta menyelesaikan persamaan matriks.",
                "Latihan matriks kelas 11 SMA: ordo dan transpose, penjumlahan dan perkalian skalar, perkalian matriks 2 × 2, determinan 2 × 2 dan 3 × 3 (Sarrus), invers matriks, dan persamaan matriks. 100 soal dengan kunci jawaban.",
                "det (a b; c d) = ad − bc", "Perkalian matriks: baris kali kolom.", sets,
                ["Matriks berordo m × n mempunyai m baris dan n kolom. Transpose Aᵀ menukar baris menjadi kolom.",
                 "Penjumlahan dilakukan elemen demi elemen. Perkalian AB: elemen baris i kolom j = jumlah hasil kali baris i dari A dengan kolom j dari B. Umumnya AB ≠ BA.",
                 "Untuk A = (a b; c d): det A = ad − bc dan A⁻¹ = 1/(ad − bc) × (d −b; −c a). Persamaan AX = B diselesaikan dengan X = A⁻¹B."],
                [("det (3 2; 1 4)?", ["3 × 4 − 2 × 1"], "10"),
                 ("(1 2; 3 4)(2 0; 1 1)?", ["Baris 1: 1 × 2 + 2 × 1 = 4, 1 × 0 + 2 × 1 = 2"], "(4 2; 10 4)")],
                [["Perkalian matriks dilakukan per elemen", "Pakai baris kali kolom"],
                 ["det = ad + bc", "det = ad − bc"],
                 ["Invers: tukar b dan c", "Tukar a dan d, ubah tanda b dan c, lalu bagi dengan det"]],
                [("Kapan dua matriks dapat dikalikan?", "Jika banyak kolom matriks pertama sama dengan banyak baris matriks kedua."),
                 ("Kapan matriks tidak mempunyai invers?", "Jika determinannya 0 (matriks singular)."),
                 ("Di mana matriks dipakai?", "Untuk menyelesaikan sistem persamaan, transformasi geometri, grafika komputer, dan pengolahan data.")])


# ============================================================ 7. fungsi trigonometri
def u7():
    def radian():
        d = ch([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360])
        r = Fr(d, 180)
        pi = lambda f: ("π" if f == 1 else ("%sπ" % sn(f) if f.denominator == 1 else "%sπ" % fq(f)))
        k = ri(0, 1)
        if k == 0:
            return M("Sudut %d° dalam radian adalah …" % d, pi(r), [pi(Fr(d, 360)), pi(r * 2), pi(1 / r) if r != 1 else pi(Fr(1, 2))], "%d° × π/180° = %s rad." % (d, pi(r)))
        return M("Sudut %s rad dalam derajat adalah …" % pi(r), "%d°" % d, ["%d°" % (d // 2) if d % 2 == 0 else "%d°" % (d + 30), "%d°" % (d * 2), "%d°" % (360 - d) if d != 180 else "90°"], "%s × 180°/π = %d°." % (pi(r), d))

    def ciri():
        a = ri(1, 5) * ch([1, -1])
        b = ch([1, 2, 3, 4, Fr(1, 2)])
        c = ri(-3, 3)
        f = ch(["sin", "cos"])
        e = "y = %s%s(%sx)" % (sn(a) + " " if abs(a) != 1 else ("" if a == 1 else MINUS), f, sn(b) if b != 1 else "") + ("" if c == 0 else " %s %d" % ("+" if c > 0 else "−", abs(c)))
        k = ri(0, 2)
        if k == 0:
            per = Fr(360) / b
            return M("Periode fungsi %s adalah …" % e, "%s°" % sn(per), ["%s°" % sn(Fr(360) * b) if Fr(360) * b != per else "180°", "%s°" % sn(per / 2), "%d°" % abs(a) if False else "%s°" % sn(per * 2)], "Periode y = a %s(bx) adalah 360°/b = 360°/%s = %s°." % (f, fq(b), sn(per)))
        if k == 1:
            return MN("Amplitudo fungsi %s adalah …" % e, abs(a), [a * 2 if a * 2 != abs(a) else abs(a) + 1, abs(a) + abs(c) if c else abs(a) + 2, b if Fr(b).denominator == 1 and b != abs(a) else abs(a) * 3], "Amplitudo = |a| = %d." % abs(a))
        return M("Nilai maksimum dan minimum fungsi %s adalah …" % e, "%s dan %s" % (sn(abs(a) + c), sn(-abs(a) + c)), ["%s dan %s" % (sn(abs(a)), sn(-abs(a))) if c else "%s dan %s" % (sn(abs(a) + 1), sn(-abs(a) - 1)), "%s dan %s" % (sn(abs(a) - c), sn(-abs(a) - c)) if c else "1 dan −1", "%s dan %s" % (sn(abs(a) + c), sn(c))],
                 "Maksimum = |a| + c = %s, minimum = −|a| + c = %s." % (sn(abs(a) + c), sn(-abs(a) + c)))

    def nilai():
        a = ri(1, 4) * ch([1, -1])
        f = ch(["sin", "cos"])
        x = ch([0, 30, 45, 60, 90, 120, 150, 180, 210, 270, 300])
        import math as m_
        val = round(m_.sin(m_.radians(x)) if f == "sin" else m_.cos(m_.radians(x)), 6)
        table = {0.0: "0", 0.5: "½", 1.0: "1", -0.5: "−½", -1.0: "−1", round(m_.sqrt(2) / 2, 6): "½√2", round(m_.sqrt(3) / 2, 6): "½√3", round(-m_.sqrt(3) / 2, 6): "−½√3", round(-m_.sqrt(2) / 2, 6): "−½√2"}
        base = table.get(val)
        if base is None:
            return None
        def scale(sv):
            if sv == "0":
                return "0"
            neg_ = sv.startswith(MINUS)
            sv = sv.lstrip(MINUS)
            sign = (-1 if neg_ else 1) * (1 if a > 0 else -1)
            k = abs(a)
            if sv == "1":
                r = sn(k)
            elif sv == "½":
                r = fq(Fr(k, 2))
            else:
                rad = sv[1:]
                r = (fq(Fr(k, 2)) if k % 2 else ("" if k == 2 else sn(k // 2))) + rad
            return (MINUS if sign < 0 else "") + r
        c = scale(base)
        ws = [scale(neg(base)) if base != "0" else scale("1"), scale(table.get(round(m_.cos(m_.radians(x)) if f == "sin" else m_.sin(m_.radians(x)), 6), "1")), sn(a)]
        return M("Nilai f(x) = %s%s x untuk x = %d° adalah …" % (sn(a) + " " if abs(a) != 1 else ("" if a == 1 else MINUS), f, x), c, ws, "f(%d°) = %s × %s %d° = %s." % (x, sn(a), f, x, c))

    def grafik():
        a = ri(1, 3)
        b = ch([1, 2])
        f = ch(["sin", "cos"])
        import math as m_
        F = (lambda x: a * m_.sin(m_.radians(b * x))) if f == "sin" else (lambda x: a * m_.cos(m_.radians(b * x)))
        pic = kurve([(F, BLUE, "")], (0, 360, 90), (-3, 3, 1), label="grafik fungsi trigonometri")
        e = lambda aa, bb, ff: "y = %s%s %s" % ("" if aa == 1 else sn(aa) + " ", ff, ("x" if bb == 1 else "%dx" % bb))
        c = e(a, b, f)
        other = "cos" if f == "sin" else "sin"
        return M("Grafik berikut adalah grafik fungsi … (x dalam derajat)" + pic, c, [e(a, b, other), e(a, 3 - b, f), e(a + 1 if a < 3 else a - 1, b, f)],
                 "Nilai maksimum %d menunjukkan amplitudo %d. Periode %d° menunjukkan b = %d. Grafik %s." % (a, a, 360 // b, b, "mulai dari 0 (sinus)" if f == "sin" else "mulai dari puncak (kosinus)"))

    def persamaan():
        F = [("sin x = ½", "{30°, 150°}"), ("cos x = ½", "{60°, 300°}"), ("tan x = 1", "{45°, 225°}"), ("sin x = −½", "{210°, 330°}"), ("cos x = −½", "{120°, 240°}"),
             ("sin x = ½√3", "{60°, 120°}"), ("cos x = ½√2", "{45°, 315°}"), ("tan x = √3", "{60°, 240°}"), ("sin x = 1", "{90°}"), ("cos x = 0", "{90°, 270°}"),
             ("2 sin x = 1", "{30°, 150°}"), ("2 cos x − √3 = 0", "{30°, 330°}"), ("tan x = −1", "{135°, 315°}"), ("sin x = −1", "{270°}"), ("cos x = −1", "{180°}")]
        q, c = ch(F)
        alls = [x[1] for x in F]
        return M("Himpunan penyelesaian %s untuk 0° ≤ x &lt; 360° adalah …" % q, c, [w for w in sh(alls) if w != c][:3], "Cari sudut dasar di kuadran I, lalu tentukan kuadran yang tandanya sesuai: %s." % c)

    sets = [("Derajat dan radian", [(radian, 20)]),
            ("Periode, amplitudo, maksimum, dan minimum", [(ciri, 20)]),
            ("Nilai fungsi trigonometri", [(nilai, 20)]),
            ("Grafik fungsi trigonometri", [(grafik, 12), (ciri, 8)]),
            ("Persamaan trigonometri sederhana", [(persamaan, 15), (radian, 5)])]
    return unit("fungsi-trigonometri", "A", 7, "Fungsi Trigonometri dan Grafiknya", "Fungsi Trigonometri",
                "Peserta didik mengubah ukuran sudut derajat dan radian, menganalisis grafik fungsi sinus dan kosinus (periode, amplitudo, nilai maksimum dan minimum), dan menyelesaikan persamaan trigonometri sederhana.",
                "Latihan fungsi trigonometri kelas 11 SMA: derajat dan radian, periode dan amplitudo, nilai maksimum dan minimum, nilai fungsi sinus dan kosinus, membaca grafik, dan persamaan trigonometri. 100 soal dengan kunci jawaban.",
                "y = a sin bx: amplitudo |a|", "Periode 360°/b. Ingat: 180° = π radian.", sets,
                ["180° = π radian, jadi 1° = π/180 rad. Contoh 60° = π/3 rad.",
                 "Untuk y = a sin(bx) + c dan y = a cos(bx) + c: amplitudo |a|, periode 360°/b, nilai maksimum |a| + c, dan nilai minimum −|a| + c.",
                 "Persamaan sin x = sin α mempunyai penyelesaian x = α dan x = 180° − α; cos x = cos α mempunyai x = α dan x = 360° − α (dalam 0° sampai 360°)."],
                [("y = 3 sin 2x + 1. Periode, maksimum, minimum?", ["360°/2", "3 + 1, −3 + 1"], "180°, 4, −2"),
                 ("cos x = ½, 0° ≤ x &lt; 360°", ["x = 60° dan 360° − 60°"], "{60°, 300°}")],
                [["Periode y = sin 2x adalah 720°", "Periode = 360°/2 = 180°"],
                 ["Amplitudo y = −2 cos x adalah −2", "Amplitudo selalu positif: |−2| = 2"],
                 ["sin x = ½ hanya x = 30°", "Juga x = 150° (kuadran II)"]],
                [("Mengapa grafik sinus berulang?", "Karena sudut yang berbeda 360° menunjuk ke titik yang sama pada lingkaran satuan."),
                 ("Apa beda grafik sinus dan kosinus?", "Bentuknya sama, tetapi grafik kosinus bergeser 90°: sinus mulai dari 0, kosinus mulai dari puncak."),
                 ("Di mana fungsi trigonometri dipakai?", "Untuk gelombang bunyi, arus listrik bolak-balik, pasang surut air laut, dan gerak putar.")])


# ============================================================ 8. bilangan kompleks
def u8():
    def cx(a, b):
        if b == 0:
            return sn(a)
        bi = ("" if abs(b) == 1 else sn(abs(b))) + "i"
        if a == 0:
            return (MINUS if b < 0 else "") + bi
        return "%s %s %s" % (sn(a), "+" if b > 0 else "−", bi)

    def dasar():
        k = ri(0, 2)
        if k == 0:
            n = ri(2, 30)
            v = ["1", "i", "−1", "−i"][n % 4]
            return M("Nilai i%s adalah …" % sup(n), v, [w for w in ["1", "i", "−1", "−i"] if w != v], "i² = −1, i⁴ = 1. %d = 4 × %d + %d, jadi i%s = i%s = %s." % (n, n // 4, n % 4, sup(n), sup(n % 4), v))
        if k == 1:
            a, b = nz(-9, 9), nz(-9, 9)
            w = ch(["bagian real", "bagian imajiner"])
            v = a if w == "bagian real" else b
            return MN("%s dari z = %s adalah …" % (w.capitalize(), cx(a, b)), v, [b if w == "bagian real" else a, -v, abs(a) + abs(b)], "z = a + bi: bagian real a = %s, bagian imajiner b = %s." % (sn(a), sn(b)))
        n = ri(2, 12)
        return M("Nilai √(−%d) adalah …" % (n * n), "%di" % n, ["−%d" % n, "%d" % n, "%di" % (n * n)], "√(−%d) = √%d × √(−1) = %di." % (n * n, n * n, n))

    def operasi():
        a, b, c, d = nz(-7, 7), nz(-7, 7), nz(-7, 7), nz(-7, 7)
        k = ri(0, 2)
        if k == 0:
            return M("Hasil (%s) + (%s) adalah …" % (cx(a, b), cx(c, d)), cx(a + c, b + d), [cx(a + c, b - d), cx(a - c, b + d), cx(a + b, c + d)], "Jumlahkan bagian real dan bagian imajiner masing-masing: %s." % cx(a + c, b + d))
        if k == 1:
            return M("Hasil (%s) − (%s) adalah …" % (cx(a, b), cx(c, d)), cx(a - c, b - d), [cx(a + c, b + d), cx(a - c, b + d), cx(c - a, d - b)], "%s." % cx(a - c, b - d))
        re, im = a * c - b * d, a * d + b * c
        return M("Hasil (%s)(%s) adalah …" % (cx(a, b), cx(c, d)), cx(re, im), [cx(a * c + b * d, im), cx(a * c, b * d), cx(re, -im) if im else cx(re + 1, im)], "(a + bi)(c + di) = (ac − bd) + (ad + bc)i = %s." % cx(re, im))

    def sekawan():
        a, b = nz(-8, 8), nz(-8, 8)
        k = ri(0, 2)
        if k == 0:
            return M("Sekawan (konjugat) dari z = %s adalah …" % cx(a, b), cx(a, -b), [cx(-a, b), cx(-a, -b), cx(b, a)], "Sekawan a + bi adalah a − bi: %s." % cx(a, -b))
        if k == 1:
            T = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (0, 7, 7), (9, 12, 15)]
            p, q, r = ch(T)
            p, q = p * ch([1, -1]), q * ch([1, -1])
            return MN("Modulus |z| dari z = %s adalah …" % cx(p, q), r, [abs(p) + abs(q), r * r, r + 1], "|z| = √(a² + b²) = √(%d + %d) = %d." % (p * p, q * q, r))
        return MN("Hasil z × z̄ untuk z = %s adalah …" % cx(a, b), a * a + b * b, [a * a - b * b, 2 * a, (a + b) ** 2], "(a + bi)(a − bi) = a² + b² = %d." % (a * a + b * b))

    def bagi():
        c, d = nz(-4, 4), nz(-4, 4)
        x, y = nz(-5, 5), ri(-5, 5)
        # (x + yi)(c + di) = numerator
        re, im = x * c - y * d, x * d + y * c
        return M("Hasil (%s) : (%s) adalah …" % (cx(re, im), cx(c, d)), cx(x, y), [cx(-x, y) if x else cx(1, y), cx(x, -y) if y else cx(x, 1), cx(y, x) if (y, x) != (x, y) else cx(x + 1, y)],
                 "Kalikan pembilang dan penyebut dengan sekawan penyebut (%s), lalu bagi dengan %d. Hasilnya %s." % (cx(c, -d), c * c + d * d, cx(x, y)))

    def akar():
        p = ri(-6, 6)
        q = ri(1, 8)
        # x² − 2p x + (p² + q²) = 0 → x = p ± qi
        e = expr([(1, "x²"), (-2 * p, "x"), (p * p + q * q, "")])
        return M("Akar-akar persamaan %s = 0 adalah …" % e, "%s dan %s" % (cx(p, q), cx(p, -q)), ["%s dan %s" % (cx(-p, q), cx(-p, -q)) if p else "%s dan %s" % (cx(1, q), cx(1, -q)), "%s dan %s" % (sn(p + q), sn(p - q)), "%s dan %s" % (cx(q, p), cx(q, -p)) if q != p else "%s dan %s" % (cx(p, 2 * q), cx(p, -2 * q))],
                 "D = %s &lt; 0. x = (%s ± √(%s))/2 = %s ± %si." % (sn(4 * p * p - 4 * (p * p + q * q)), sn(2 * p), sn(-4 * q * q), sn(p), "" if q == 1 else sn(q)))

    sets = [("Satuan imajiner dan bentuk a + bi", [(dasar, 20)]),
            ("Penjumlahan, pengurangan, dan perkalian", [(operasi, 20)]),
            ("Sekawan dan modulus", [(sekawan, 20)]),
            ("Pembagian bilangan kompleks", [(bagi, 20)]),
            ("Akar persamaan kuadrat", [(akar, 14), (operasi, 6)])]
    return unit("bilangan-kompleks", "B", 8, "Bilangan Kompleks", "Bilangan Kompleks",
                "Peserta didik memahami bilangan kompleks, melakukan operasi pada bilangan kompleks, menentukan sekawan dan modulus, serta menyelesaikan persamaan kuadrat dengan diskriminan negatif.",
                "Latihan bilangan kompleks kelas 11 SMA: satuan imajiner i dan pangkatnya, bagian real dan imajiner, penjumlahan, perkalian, pembagian, sekawan, modulus, dan akar kompleks persamaan kuadrat. 100 soal dengan kunci jawaban.",
                "i² = −1", "z = a + bi: a bagian real, b bagian imajiner.", sets,
                ["Satuan imajiner i memenuhi i² = −1. Pangkat i berulang setiap 4: i, −1, −i, 1.",
                 "Bilangan kompleks z = a + bi. Penjumlahan per bagian; perkalian (a + bi)(c + di) = (ac − bd) + (ad + bc)i.",
                 "Sekawan z̄ = a − bi, modulus |z| = √(a² + b²), dan z × z̄ = a² + b². Untuk membagi, kalikan dengan sekawan penyebut."],
                [("(2 + 3i)(1 − i)?", ["2 − 2i + 3i − 3i² = 2 + i + 3"], "5 + i"),
                 ("x² + 4x + 13 = 0", ["D = −36", "x = (−4 ± 6i)/2"], "−2 + 3i dan −2 − 3i")],
                [["i² = 1", "i² = −1"],
                 ["(a + bi)(c + di) = ac + bdi", "Kalikan semua suku dan pakai i² = −1"],
                 ["|3 − 4i| = 3 − 4", "|3 − 4i| = √(9 + 16) = 5"]],
                [("Mengapa diperlukan bilangan kompleks?", "Agar setiap persamaan kuadrat mempunyai penyelesaian, termasuk yang diskriminannya negatif."),
                 ("Apa itu bidang kompleks?", "Bidang dengan sumbu mendatar untuk bagian real dan sumbu tegak untuk bagian imajiner; z = a + bi digambar sebagai titik (a, b)."),
                 ("Di mana bilangan kompleks dipakai?", "Dalam teknik listrik (arus bolak-balik), pengolahan sinyal, dan fisika gelombang.")])


# ============================================================ 9. ragam dan simpangan baku
def u9():
    def data(n=None):
        while True:
            n = n or ch([4, 5, 6, 8])
            m = ri(5, 20)
            devs = [ri(-5, 5) for _ in range(n - 1)]
            devs.append(-sum(devs))
            if abs(devs[-1]) <= 8 and any(devs):
                return [m + d for d in devs], m, devs

    def ds(xs):
        return "; ".join(num(x) for x in xs)

    def ragam():
        xs, m, devs = data()
        n = len(xs)
        v = Fr(sum(d * d for d in devs), n)
        if not S.endlich(v) or ("," in dz(v) and len(dz(v).split(",")[1]) > 2):
            return None
        return MD("Ragam (varians) dari data %s adalah …" % ds(xs), v, [Fr(sum(d * d for d in devs), n - 1) if S.endlich(Fr(sum(d * d for d in devs), n - 1)) else v + 1, Fr(sum(abs(d) for d in devs), n), v * 2],
                  "x̄ = %d. s² = Σ(x − x̄)²/n = %d/%d = %s." % (m, sum(d * d for d in devs), n, dz(v)))

    def baku():
        while True:
            xs, m, devs = data()
            n = len(xs)
            v = Fr(sum(d * d for d in devs), n)
            if v.denominator == 1 and math.isqrt(int(v)) ** 2 == int(v):
                break
        s = math.isqrt(int(v))
        return MN("Simpangan baku dari data %s adalah …" % ds(xs), s, [int(v), Fr(sum(abs(d) for d in devs), n) if Fr(sum(abs(d) for d in devs), n) != s else s + 1, s + 1], "s² = %d/%d = %d, jadi s = √%d = %d." % (sum(d * d for d in devs), n, int(v), int(v), s))

    def sr():
        xs, m, devs = data()
        n = len(xs)
        v = Fr(sum(abs(d) for d in devs), n)
        if not S.endlich(v) or ("," in dz(v) and len(dz(v).split(",")[1]) > 2):
            return None
        return MD("Simpangan rata-rata dari data %s adalah …" % ds(xs), v, [Fr(sum(d * d for d in devs), n) if S.endlich(Fr(sum(d * d for d in devs), n)) else v + 1, Fr(sum(abs(d) for d in devs), n - 1) if S.endlich(Fr(sum(abs(d) for d in devs), n - 1)) else v + 2, 0],
                  "x̄ = %d. SR = Σ|x − x̄|/n = %d/%d = %s." % (m, sum(abs(d) for d in devs), n, dz(v)))

    def sifat():
        k = ri(0, 2)
        s = ri(2, 9)
        c = ri(2, 10)
        if k == 0:
            return MN("Simpangan baku suatu data adalah %d. Jika setiap data ditambah %d, simpangan bakunya menjadi …" % (s, c), s, [s + c, s * c, s - 1], "Menambah bilangan yang sama tidak mengubah penyebaran data, jadi tetap %d." % s)
        if k == 1:
            k_ = ri(2, 4)
            return MN("Simpangan baku suatu data adalah %d. Jika setiap data dikali %d, simpangan bakunya menjadi …" % (s, k_), s * k_, [s, s * k_ * k_, s + k_], "Dikali %d, simpangan baku juga dikali %d: %d." % (k_, k_, s * k_))
        k_ = ri(2, 4)
        return MN("Ragam suatu data adalah %d. Jika setiap data dikali %d, ragamnya menjadi …" % (s, k_), s * k_ * k_, [s * k_, s, s + k_], "Ragam dikali k²: %d × %d = %d." % (s, k_ * k_, s * k_ * k_))

    def banding():
        a, ma, da = data(5)
        b = [ma + d * 2 for d in da]
        va, vb = Fr(sum(d * d for d in da), 5), Fr(sum(4 * d * d for d in da), 5)
        return M("Data A: %s. Data B: %s. Pernyataan yang benar …" % (ds(a), ds(b)), "rata-ratanya sama, tetapi data B lebih menyebar",
                 ["rata-ratanya sama dan penyebarannya sama", "data A lebih menyebar", "rata-rata data B lebih besar"], "Keduanya berpusat di %d, tetapi simpangan data B dua kali simpangan data A." % ma)

    sets = [("Simpangan rata-rata", [(sr, 20)]),
            ("Ragam", [(ragam, 20)]),
            ("Simpangan baku", [(baku, 20)]),
            ("Sifat ragam dan simpangan baku", [(sifat, 20)]),
            ("Membandingkan penyebaran data", [(banding, 10), (ragam, 5), (baku, 5)])]
    return unit("ragam-dan-simpangan-baku", "D", 9, "Ukuran Penyebaran: Simpangan Rata-Rata, Ragam, dan Simpangan Baku", "Ragam dan Simpangan Baku",
                "Peserta didik menentukan dan menafsirkan ukuran penyebaran data (simpangan rata-rata, ragam, simpangan baku) serta pengaruh perubahan data terhadap ukuran penyebaran.",
                "Latihan ragam dan simpangan baku kelas 11 SMA: simpangan rata-rata, ragam (varians), simpangan baku, pengaruh penambahan dan perkalian data, dan membandingkan penyebaran dua data. 100 soal dengan kunci jawaban.",
                "s² = Σ(x − x̄)²/n", "Simpangan baku s = √ragam.", sets,
                ["Ukuran penyebaran menunjukkan seberapa jauh data menyebar dari rata-ratanya.",
                 "Simpangan rata-rata SR = Σ|x − x̄|/n. Ragam s² = Σ(x − x̄)²/n. Simpangan baku s = √s².",
                 "Jika setiap data ditambah c, ragam dan simpangan baku tetap. Jika setiap data dikali k, simpangan baku dikali |k| dan ragam dikali k²."],
                [("Data 4; 6; 8; 10; 12. Ragam?", ["x̄ = 8", "(16 + 4 + 0 + 4 + 16)/5"], "8"),
                 ("Simpangan baku 3, setiap data dikali 2?", ["3 × 2"], "6")],
                [["Ragam dihitung tanpa mengkuadratkan selisih", "Kuadratkan setiap selisih dari rata-rata"],
                 ["Data ditambah 5, simpangan baku bertambah 5", "Simpangan baku tetap"],
                 ["Simpangan baku = ragam", "Simpangan baku = √ragam"]],
                [("Apa arti simpangan baku kecil?", "Data mengumpul dekat rata-rata, jadi data itu seragam."),
                 ("Mengapa selisih dikuadratkan?", "Agar selisih negatif dan positif tidak saling meniadakan, dan simpangan besar lebih berpengaruh."),
                 ("Kapan memakai pembagi n − 1?", "Untuk sampel dalam statistika lanjut. Pada latihan ini data dianggap populasi, jadi pembaginya n.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9]
