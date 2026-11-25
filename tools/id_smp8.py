# -*- coding: utf-8 -*-
"""Indonesia / Matematika / Kelas 8 (SMP, Fase D)。python3 tools/id_smp.py 8 [番号…]"""
import math
from fractions import Fraction as Fr
import id_smp as S
from id_smp import (ri, ch, nz, sh, num, sn, par, pd, dz, fq, expr, lin, sup, pw, M, MN, MD, rp, NB, MINUS,
                    numline, kosy, figure, poly_ang, tab, unit, fig, wrap, text, line, INK, BLUE, RED, FILL, GREEN)


def sci(m, e):
    """3,2 × 10⁵"""
    return "%s × 10%s" % (dz(m), sup(e))


# ============================================================ 1. bilangan berpangkat
def u1():
    def hitung():
        k = ri(0, 3)
        if k == 0:
            b, e = nz(-6, 6), ri(2, 4)
            if abs(b) == 1 or abs(b) ** e > 2000:
                return None
            v = b ** e
            return MN("Nilai dari %s adalah …" % pw(b, e), v, [b * e, -v, b ** (e - 1) if e > 2 else b * 3, (b ** e) * b if abs(b ** (e + 1)) < 5000 else v + 1],
                      "%s = %s = %s." % (pw(b, e), " × ".join([par(b)] * e), sn(v)))
        if k == 1:
            b = ri(2, 9)
            e = 2 if b > 4 else ch([2, 4])
            v = b ** e
            neg = ri(0, 1)
            q = ("−%d%s" % (b, sup(e))) if neg else ("(−%d)%s" % (b, sup(e)))
            c = sn(-v) if neg else sn(v)
            return M("Nilai dari %s adalah …" % q, c, [sn(v) if neg else sn(-v), sn(-b * e) if neg else sn(b * e), sn(b * e) if neg else sn(-b * e)],
                     "%s berarti %s = %s." % (q, ("−(%s)" % " × ".join([str(b)] * e)) if neg else " × ".join(["(−%d)" % b] * e), c))
        if k == 2:
            a = ri(2, 9)
            e = ri(-3, 0)
            if e == 0:
                return M("Nilai dari %d⁰ adalah …" % a if ri(0, 1) else "Nilai dari (%s)⁰ adalah …" % sn(-a), "1", ["0", str(a), sn(-1)], "Setiap bilangan (bukan 0) berpangkat 0 hasilnya 1.")
            v = Fr(1, a ** (-e))
            return M("Nilai dari %d%s adalah …" % (a, sup(e)), fq(v), [sn(-(a ** (-e))), sn(a * e), fq(Fr(1, a * (-e))) if a * (-e) != a ** (-e) else fq(Fr(-1, a ** (-e)))],
                     "a%s = 1/a%s, jadi %d%s = 1/%d%s = %s." % (sup(e), sup(-e), a, sup(e), a, sup(-e), fq(v)))
        a, b = Fr(ri(1, 5), ri(2, 5)), ri(2, 3)
        if a.denominator == 1:
            return None
        v = a ** b
        return M("Nilai dari %s adalah …" % pw(a, b), fq(v), [fq(Fr(a.numerator ** b, a.denominator)), fq(a * b), fq(Fr(a.numerator, a.denominator ** b))],
                 "Pangkatkan pembilang dan penyebut: %s." % fq(v))

    def sifat():
        a = ch([2, 3, 5, 7, "a", "x", "p"])
        m, n = ri(2, 9), ri(2, 7)
        k = ri(0, 2)
        A = str(a)
        if k == 0:
            return M("Bentuk sederhana dari %s%s × %s%s adalah …" % (A, sup(m), A, sup(n)), "%s%s" % (A, sup(m + n)), ["%s%s" % (A, sup(m * n)), "%s%s" % (A + A if isinstance(a, str) else str(a * a), sup(m + n)), "%s%s" % (A, sup(m + n + 1))],
                     "aᵐ × aⁿ = aᵐ⁺ⁿ: pangkatnya dijumlahkan, %d + %d = %d." % (m, n, m + n))
        if k == 1:
            if m == n:
                return None
            m, n = max(m, n) + ri(1, 4), min(m, n)
            return M("Bentuk sederhana dari %s%s : %s%s adalah …" % (A, sup(m), A, sup(n)), "%s%s" % (A, sup(m - n)), ["%s%s" % (A, sup(m + n)), "%s%s" % (A, sup(m // n)) if m % n == 0 and m // n != m - n else "%s%s" % (A, sup(m * n)), "1%s" % sup(m - n)],
                     "Pangkatnya dikurangkan: %d − %d = %d." % (m, n, m - n))
        return M("Bentuk sederhana dari (%s%s)%s adalah …" % (A, sup(m), sup(n)), "%s%s" % (A, sup(m * n)), ["%s%s" % (A, sup(m + n)), "%s%s" % (A, sup(m ** n)) if m ** n < 1000 else "%s%s" % (A, sup(m * n + 1)), "%s%s" % (A, sup(m * n + m))],
                 "(aᵐ)ⁿ = aᵐⁿ: pangkatnya dikalikan, %d × %d = %d." % (m, n, m * n))

    def aljabar():
        k = ri(0, 2)
        a, b = nz(-6, 6), ri(2, 6)
        m, n = ri(1, 6), ri(1, 6)
        v = ch(["x", "y", "a", "p"])
        if k == 0:
            c = "%s%s%s" % (sn(a * b) if abs(a * b) != 1 else ("" if a * b > 0 else MINUS), v, sup(m + n))
            return M("Hasil dari %s%s%s × %d%s%s adalah …" % (sn(a), v, sup(m) if m > 1 else "", b, v, sup(n) if n > 1 else ""), c,
                     ["%s%s%s" % (sn(a + b), v, sup(m + n)), "%s%s%s" % (sn(a * b), v, sup(m * n)), "%s%s%s" % (sn(-a * b), v, sup(m + n))],
                     "Kalikan koefisien (%s × %d = %s) dan jumlahkan pangkat (%d + %d = %d)." % (sn(a), b, sn(a * b), m, n, m + n))
        if k == 1:
            e = ri(2, 4)
            c = "%s%s%s" % (sn(b ** e), v, sup(m * e))
            return M("Hasil dari (%d%s%s)%s adalah …" % (b, v, sup(m) if m > 1 else "", sup(e)), c, ["%d%s%s" % (b, v, sup(m * e)), "%s%s%s" % (sn(b * e), v, sup(m * e)), "%s%s%s" % (sn(b ** e), v, sup(m + e))],
                     "Setiap faktor dipangkatkan %d: %d%s = %s dan pangkat %s menjadi %d." % (e, b, sup(e), sn(b ** e), v, m * e))
        p = ri(4, 9)
        q = ri(1, p - 1)
        cf = b * ri(2, 5)
        c = "%s%s%s" % (sn(Fr(cf * a, b)) if abs(cf * a // b) != 1 else ("" if cf * a > 0 else MINUS), v, sup(p - q) if p - q > 1 else "")
        return M("Hasil dari %s%s%s : %d%s%s adalah …" % (sn(cf * a), v, sup(p), b, v, sup(q) if q > 1 else ""), c,
                 ["%s%s%s" % (sn(cf * a // b), v, sup(p + q)), "%s%s%s" % (sn(cf * a - b), v, sup(p - q) if p - q > 1 else ""), "%s%s%s" % (sn(-cf * a // b), v, sup(p - q) if p - q > 1 else "")],
                 "Bagi koefisien (%s : %d = %s) dan kurangkan pangkat (%d − %d = %d)." % (sn(cf * a), b, sn(cf * a // b), p, q, p - q))

    def campur():
        b = ch([2, 3, 5])
        m, n, p = ri(2, 6), ri(2, 6), ri(1, 5)
        e = m + n - p
        if e < 0 or b ** e > 100000:
            return None
        v = b ** e
        return MN("Nilai dari (%d%s × %d%s) : %d%s adalah …" % (b, sup(m), b, sup(n), b, sup(p)), v, [b ** (m * n - p) if m * n - p < 12 and b ** (m * n - p) != v else v * b, b ** (e - 1), v * b * b],
                  "= %d%s : %d%s = %d%s = %s." % (b, sup(m + n), b, sup(p), b, sup(e), num(v)))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            a, n = ch([2, 3]), ri(3, 8)
            j = ri(1, 4) * 10
            v = a ** n
            t = "membelah diri menjadi %d setiap %d menit" % (a, j)
            return MN("Satu bakteri %s. Berapa banyak bakteri setelah %d menit?" % (t, n * j), v, [a * n, a ** (n - 1), a ** (n + 1)], "Terjadi %d kali pembelahan: %d%s = %s bakteri." % (n, a, sup(n), num(v)), unit="bakteri")
        if k == 1:
            s = ri(2, 6) * ch([1, 10])
            return MN("Volume kubus dengan rusuk %d cm adalah …" % s, s ** 3, [3 * s, s * s, 6 * s * s], "V = %d³ = %s cm³." % (s, num(s ** 3)), unit="cm³")
        n = ri(2, 5)
        return MN("Sebuah kertas dilipat menjadi dua sebanyak %d kali. Berapa lapisan kertas yang terbentuk?" % n, 2 ** n, [2 * n, 2 ** (n - 1), n * n if n * n != 2 ** n else n + 2], "Setiap lipatan menggandakan lapisan: 2%s = %d lapisan." % (sup(n), 2 ** n), unit="lapisan")

    sets = [("Menghitung bilangan berpangkat", [(hitung, 20)]),
            ("Sifat-sifat perpangkatan", [(sifat, 20)]),
            ("Pangkat nol, negatif, dan campuran", [(hitung, 8), (campur, 12)]),
            ("Perpangkatan bentuk aljabar", [(aljabar, 20)]),
            ("Soal cerita dan campuran", [(cerita, 12), (sifat, 8)])]
    return unit("bilangan-berpangkat", "B", 1, "Bilangan Berpangkat dan Sifat-Sifatnya", "Bilangan Berpangkat",
                "Peserta didik memahami bilangan berpangkat bulat, menggunakan sifat-sifat perpangkatan, dan menyederhanakan bentuk perpangkatan.",
                "Latihan bilangan berpangkat kelas 8 SMP: menghitung pangkat, bilangan negatif berpangkat, sifat perkalian, pembagian, dan pangkat dari pangkat, pangkat nol dan negatif, serta bentuk aljabar. 100 soal dengan kunci jawaban.",
                "aᵐ × aⁿ = aᵐ⁺ⁿ", "Bagi: pangkat dikurangkan. Pangkat dari pangkat: dikalikan.", sets,
                ["aⁿ berarti a dikalikan dengan dirinya sendiri sebanyak n kali. Contoh 2⁵ = 2 × 2 × 2 × 2 × 2 = 32.",
                 "Sifat perpangkatan: aᵐ × aⁿ = aᵐ⁺ⁿ, aᵐ : aⁿ = aᵐ⁻ⁿ, (aᵐ)ⁿ = aᵐⁿ, a⁰ = 1, dan a⁻ⁿ = 1/aⁿ.",
                 "Perhatikan tanda: (−3)² = 9 karena basisnya −3, tetapi −3² = −9 karena yang dipangkatkan hanya 3."],
                [("3⁴ × 3² : 3³ = …", ["= 3⁶ : 3³ = 3³"], "27"),
                 ("(2x³)² = …", ["2² = 4, (x³)² = x⁶"], "4x⁶")],
                [["2³ = 6", "2³ = 2 × 2 × 2 = 8"],
                 ["a³ × a⁴ = a¹²", "Pangkatnya dijumlahkan: a⁷"],
                 ["5⁰ = 0", "Bilangan bukan nol berpangkat 0 hasilnya 1"]],
                [("Mengapa a⁰ = 1?", "Karena aⁿ : aⁿ = aⁿ⁻ⁿ = a⁰, dan bilangan dibagi dirinya sendiri hasilnya 1."),
                 ("Apa arti pangkat negatif?", "a⁻ⁿ adalah kebalikan dari aⁿ, yaitu 1/aⁿ. Contoh 2⁻³ = 1/8."),
                 ("Apakah (−2)⁴ sama dengan −2⁴?", "Tidak. (−2)⁴ = 16, sedangkan −2⁴ = −16.")])


# ============================================================ 2. notasi ilmiah
def u2():
    def besar():
        m = Fr(ri(10, 99), 10) if ri(0, 1) else Fr(ri(100, 999), 100)
        e = ri(3, 11)
        n = int(m * 10 ** e)
        k = ri(0, 1)
        if k == 0:
            return M("Notasi ilmiah dari %s adalah …" % num(n), sci(m, e), [sci(m, e - 1), sci(m * 10, e - 1), sci(m, e + 1)],
                     "Geser koma ke kiri sampai tersisa satu angka (1 sampai 9) di depan koma: %d kali. Jadi %s." % (e, sci(m, e)))
        return MN("Bentuk biasa dari %s adalah …" % sci(m, e), n, [n // 10, n * 10, int(m * 10 ** (e - 1)) * 100 if False else n + 10 ** (e - 1)],
                  "Geser koma %d tempat ke kanan: %s." % (e, num(n)))

    def kecil():
        m = Fr(ri(10, 99), 10) if ri(0, 1) else Fr(ri(11, 9), 1) if False else Fr(ri(10, 99), 10)
        e = ri(2, 7)
        v = m / 10 ** e
        k = ri(0, 1)
        if k == 0:
            return M("Notasi ilmiah dari %s adalah …" % dz(v), sci(m, -e), [sci(m, e), sci(m, -e + 1), sci(m, -e - 1)],
                     "Geser koma ke kanan %d tempat, jadi pangkatnya negatif: %s." % (e, sci(m, -e)))
        return MD("Bentuk desimal dari %s adalah …" % sci(m, -e), v, [v * 10, v / 10, m * 10 ** e if e < 4 else v * 100], "Geser koma %d tempat ke kiri: %s." % (e, dz(v)))

    def benar():
        m = Fr(ri(11, 99), 10)
        e = ri(-6, 9)
        if e in (0, 1):
            return None
        v = m * Fr(10) ** e
        c = sci(m, e)
        ws = ["%s × 10%s" % (dz(m * 10), sup(e - 1)), "%s × 10%s" % (dz(m / 10), sup(e + 1)), "%s × 10%s" % (dz(m * 100), sup(e - 2))]
        return M("Bilangan %s sama dengan semua bentuk berikut. Manakah yang merupakan notasi ilmiah?" % (num(int(v)) if v.denominator == 1 else dz(v)), c, ws,
                 "Pada notasi ilmiah a × 10ⁿ, nilai a harus 1 ≤ a &lt; 10. Hanya %s yang memenuhi." % c)

    def operasi():
        a, b = Fr(ri(11, 49), 10), Fr(ri(11, 29), 10)
        m, n = ri(2, 8), ri(-6, 8)
        k = ri(0, 1)
        if k == 0:
            p = a * b
            e = m + n
            if p >= 10:
                p, e = p / 10, e + 1
            if not S.endlich(p) or len(dz(p)) > 6:
                return None
            return M("Hasil dari (%s) × (%s) adalah …" % (sci(a, m), sci(b, n)), sci(p, e), [sci(a * b, m * n) if a * b < 10 else sci(a * b / 10, m * n), sci(p, e - 1), sci(p, e + 1)],
                     "Kalikan bilangan depan (%s × %s = %s) dan jumlahkan pangkat 10, lalu tulis dalam notasi ilmiah: %s." % (dz(a), dz(b), dz(a * b), sci(p, e)))
        q = a * b
        e = m + n
        if q >= 10:
            q, e = q / 10, e + 1
        return M("Hasil dari (%s) : (%s) adalah …" % (sci(q, e), sci(b, n)), sci(a, m), [sci(a, e + n), sci(a, m + 1), sci(a, m - 1)],
                 "Bagi bilangan depan dan kurangkan pangkat 10: %s." % sci(a, m)) if S.endlich(q) and len(dz(q)) <= 6 else None

    def konteks():
        F = [("Jarak Bumi ke Matahari sekitar 150.000.000 km.", Fr(15, 10), 8, "km"), ("Kecepatan cahaya sekitar 300.000.000 m/detik.", Fr(3), 8, "m/detik"),
             ("Jumlah penduduk Indonesia sekitar 280.000.000 jiwa.", Fr(28, 10), 8, "jiwa"), ("Diameter sel darah merah sekitar 0,000008 m.", Fr(8), -6, "m"),
             ("Ukuran sebuah virus sekitar 0,0000001 m.", Fr(1), -7, "m"), ("Massa sebutir debu sekitar 0,00000075 kg.", Fr(75, 10), -7, "kg"),
             ("Luas daratan Indonesia sekitar 1.900.000 km².", Fr(19, 10), 6, "km²"), ("Tebal selembar kertas sekitar 0,0001 m.", Fr(1), -4, "m"),
             ("Jarak Bumi ke Bulan sekitar 384.000 km.", Fr(384, 100), 5, "km"), ("Panjang Sungai Kapuas sekitar 1.143.000 m.", Fr(1143, 1000), 6, "m"),
             ("Massa Bumi sekitar 5.970.000.000.000.000.000.000.000 kg.", Fr(597, 100), 24, "kg"), ("Ukuran atom hidrogen sekitar 0,0000000001 m.", Fr(1), -10, "m")]
        d, m, e, u = ch(F)
        return M("%s Dalam notasi ilmiah ditulis …" % d, "%s %s" % (sci(m, e), u), ["%s %s" % (sci(m, -e), u), "%s %s" % (sci(m, e + 1), u), "%s %s" % (sci(m * 10, e), u)],
                 "Hitung berapa kali koma digeser: %s %s." % (sci(m, e), u))

    def banding():
        a, b = Fr(ri(11, 99), 10), Fr(ri(11, 99), 10)
        m, n = ri(-8, 9), ri(-8, 9)
        if (a, m) == (b, n):
            return None
        x, y = a * Fr(10) ** m, b * Fr(10) ** n
        if x == y:
            return None
        A, B = sci(a, m), sci(b, n)
        c = "%s &lt; %s" % (A, B) if x < y else "%s &gt; %s" % (A, B)
        return M("Mana yang benar untuk %s dan %s?" % (A, B), c, ["%s &gt; %s" % (A, B) if x < y else "%s &lt; %s" % (A, B), "%s = %s" % (A, B), "Tidak dapat dibandingkan"],
                 "Bandingkan pangkat 10 dulu%s. Jadi %s." % (", lalu bilangan depannya" if m == n else "", c))

    sets = [("Bilangan besar", [(besar, 20)]),
            ("Bilangan kecil", [(kecil, 20)]),
            ("Notasi ilmiah yang benar dan membandingkan", [(benar, 10), (banding, 10)]),
            ("Operasi notasi ilmiah", [(operasi, 20)]),
            ("Notasi ilmiah dalam kehidupan", [(konteks, 12), (banding, 8)])]
    return unit("notasi-ilmiah", "B", 2, "Notasi Ilmiah (Bentuk Baku)", "Notasi Ilmiah",
                "Peserta didik menuliskan bilangan sangat besar dan sangat kecil dalam notasi ilmiah, membandingkannya, dan melakukan operasi perkalian dan pembagian.",
                "Latihan notasi ilmiah kelas 8 SMP: menulis bilangan besar dan bilangan kecil dalam bentuk baku a × 10ⁿ, mengubah ke bentuk biasa, membandingkan, mengalikan, dan membagi. 100 soal dengan kunci jawaban.",
                "a × 10ⁿ dengan 1 ≤ a &lt; 10", "Bilangan kecil memakai pangkat negatif: 0,003 = 3 × 10⁻³.", sets,
                ["Notasi ilmiah (bentuk baku) ditulis a × 10ⁿ, dengan 1 ≤ a &lt; 10 dan n bilangan bulat.",
                 "Untuk bilangan besar, geser koma ke kiri; banyak geseran menjadi pangkat positif. Untuk bilangan kecil, geser koma ke kanan; pangkatnya negatif.",
                 "Untuk mengalikan, kalikan bilangan depan dan jumlahkan pangkat 10. Untuk membagi, bagi bilangan depan dan kurangkan pangkat 10."],
                [("Tulis 45.000.000 dalam notasi ilmiah.", ["Koma digeser 7 tempat ke kiri"], "4,5 × 10⁷"),
                 ("(2 × 10³) × (4 × 10⁵) = …", ["2 × 4 = 8", "10³ × 10⁵ = 10⁸"], "8 × 10⁸")],
                [["45.000 = 45 × 10³", "Bilangan depan harus kurang dari 10: 4,5 × 10⁴"],
                 ["0,0006 = 6 × 10⁴", "Bilangan kecil berpangkat negatif: 6 × 10⁻⁴"],
                 ["(3 × 10⁴) × (5 × 10²) = 15 × 10⁶", "15 × 10⁶ = 1,5 × 10⁷"]],
                [("Mengapa memakai notasi ilmiah?", "Agar bilangan yang sangat besar atau sangat kecil mudah ditulis, dibaca, dan dibandingkan."),
                 ("Bagaimana membandingkan dua notasi ilmiah?", "Bandingkan pangkat 10-nya dulu. Jika pangkatnya sama, bandingkan bilangan depannya."),
                 ("Apa arti 10⁻³?", "10⁻³ = 1/1.000 = 0,001.")])


# ============================================================ 3. pythagoras
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (12, 16, 20), (9, 40, 41), (20, 21, 29), (12, 35, 37), (15, 20, 25), (10, 24, 26), (18, 24, 30), (15, 36, 39)]


def rt_pic(a, b, la, lb, lc):
    sc = 150.0 / max(a, b)
    return figure({"A": (0, 0), "B": (a, 0), "C": (0, b)}, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("A", "B", la), ("A", "C", lb), ("B", "C", lc)], right=[("A", "B", "C")],
                  label="segitiga siku-siku")


def u3():
    def miring():
        a, b, c = ch(TRIP)
        if ri(0, 1):
            a, b = b, a
        return MN("Panjang sisi miring segitiga siku-siku berikut adalah …" + rt_pic(a, b, "%d cm" % a, "%d cm" % b, "?"), c, [a + b, c + 1, b - a if b > a else a - b + c, max(a, b) + 1 if max(a, b) + 1 != c else c + 2],
                  "c² = %d² + %d² = %s + %s = %s, jadi c = %d cm." % (a, b, num(a * a), num(b * b), num(c * c), c), unit="cm")

    def siku():
        a, b, c = ch(TRIP)
        if ri(0, 1):
            a, b = b, a
        return MN("Panjang sisi yang ditanyakan pada segitiga siku-siku berikut adalah …" + rt_pic(a, b, "?", "%d cm" % b, "%d cm" % c), a, [c - b, b + 1 if b + 1 != a else b + 2, c + b if c + b < 100 else a + 1, a + 2],
                  "a² = %d² − %d² = %s − %s = %s, jadi a = %d cm." % (c, b, num(c * c), num(b * b), num(a * a), a), unit="cm")

    def tripel():
        a, b, c = ch(TRIP)
        k = ri(0, 2)
        if k == 0:
            d = c + ch([-1, 1, 2])
            sets_ = [(a, b, c)] + [(a, b, d), (a + 1, b, c), (a, b + 2, c + 1)]
            return M("Manakah yang merupakan tripel Pythagoras?", "%d, %d, %d" % (a, b, c), ["%d, %d, %d" % t for t in sets_[1:]],
                     "%d² + %d² = %d = %d². Bilangan lain tidak memenuhi." % (a, b, a * a + b * b, c))
        x, y, z = sorted([ri(4, 15), ri(4, 15), ri(4, 15)])
        if x + y <= z:
            return None
        s = x * x + y * y
        t = "siku-siku" if s == z * z else ("lancip" if s > z * z else "tumpul")
        return M("Segitiga dengan sisi %d cm, %d cm, dan %d cm termasuk segitiga …" % (x, y, z), t, [w for w in ["siku-siku", "lancip", "tumpul", "sama sisi"] if w != t],
                 "%d² + %d² = %d dan %d² = %d. %s." % (x, y, s, z, z * z, "Sama, jadi siku-siku" if t == "siku-siku" else ("Lebih besar, jadi lancip" if t == "lancip" else "Lebih kecil, jadi tumpul")))

    def akar():
        a, b = ri(1, 9), ri(1, 9)
        s = a * a + b * b
        r = math.isqrt(s)
        if r * r == s:
            return None
        k = ri(0, 1)
        return M("Sisi siku-siku segitiga %d cm dan %d cm. Panjang sisi miringnya …" % (a, b), "√%d cm" % s, ["%d cm" % (a + b), "√%d cm" % abs(a * a - b * b) if a != b else "√%d cm" % (s + 1), "%d cm" % s],
                 "c = √(%d² + %d²) = √%d cm." % (a, b, s))

    def cerita():
        a, b, c = ch(TRIP)
        k = ri(0, 3)
        if k == 0:
            return MN("Sebuah tangga sepanjang %d m bersandar pada tembok. Kaki tangga berjarak %d m dari tembok. Tinggi ujung atas tangga dari lantai …" % (c, a), b,
                      [c - a, c + a, b + 1], "t = √(%d² − %d²) = √%d = %d m." % (c, a, b * b, b), unit="m")
        if k == 1:
            return MN("Andi berjalan %d m ke timur lalu %d m ke utara. Jarak Andi dari titik awal …" % (a, b), c, [a + b, c + 2, abs(b - a) if b != a else c - 1], "√(%d² + %d²) = √%d = %d m." % (a, b, c * c, c), unit="m")
        if k == 2:
            return MN("Layar televisi berbentuk persegi panjang dengan ukuran %d inci × %d inci. Panjang diagonal layarnya …" % (a * 2 if c * 2 < 100 else a, b * 2 if c * 2 < 100 else b), c * 2 if c * 2 < 100 else c,
                      [(a + b) * 2 if c * 2 < 100 else a + b, (c + 1) * 2, (c - 1) * 2], "d = √(p² + l²) = %d inci." % (c * 2 if c * 2 < 100 else c), unit="inci")
        return MN("Sebuah tiang setinggi %d m diikat tali dari puncaknya ke tanah. Tali itu sepanjang %d m dan lurus. Jarak ujung tali di tanah ke kaki tiang …" % (b, c), a,
                  [c - b, c + b, a + 2], "√(%d² − %d²) = √%d = %d m." % (c, b, a * a, a), unit="m")

    def jarak():
        x1, y1 = ri(-5, 5), ri(-5, 5)
        a, b, c = ch(TRIP[:5])
        sx, sy = ch([1, -1]), ch([1, -1])
        x2, y2 = x1 + sx * a, y1 + sy * b
        return MN("Jarak titik A(%s, %s) dan B(%s, %s) adalah …" % (sn(x1), sn(y1), sn(x2), sn(y2)), c, [a + b, c + 1, abs(x2 - x1 - (y2 - y1)) if abs(x2 - x1 - (y2 - y1)) != c else c + 3],
                  "Selisih x = %d, selisih y = %d. AB = √(%d² + %d²) = %d." % (a, b, a, b, c), unit="satuan")

    sets = [("Mencari sisi miring", [(miring, 20)]),
            ("Mencari sisi siku-siku", [(siku, 20)]),
            ("Tripel Pythagoras dan jenis segitiga", [(tripel, 20)]),
            ("Hasil dalam bentuk akar dan jarak dua titik", [(akar, 10), (jarak, 10)]),
            ("Soal cerita", [(cerita, 20)])]
    return unit("teorema-pythagoras", "G", 3, "Teorema Pythagoras", "Teorema Pythagoras",
                "Peserta didik menjelaskan dan menggunakan teorema Pythagoras untuk menentukan panjang sisi segitiga siku-siku, jenis segitiga, dan jarak dua titik.",
                "Latihan teorema Pythagoras kelas 8 SMP: mencari sisi miring dan sisi siku-siku, tripel Pythagoras, jenis segitiga lancip, siku-siku, tumpul, jarak dua titik, dan soal cerita. 100 soal dengan kunci jawaban.",
                "c² = a² + b²", "c adalah sisi miring (sisi terpanjang).", sets,
                ["Pada segitiga siku-siku, kuadrat sisi miring sama dengan jumlah kuadrat kedua sisi siku-sikunya: c² = a² + b².",
                 "Untuk mencari sisi siku-siku, kurangkan: a² = c² − b². Tiga bilangan bulat yang memenuhi a² + b² = c² disebut tripel Pythagoras, misalnya 3, 4, 5.",
                 "Untuk segitiga dengan sisi terpanjang c: jika a² + b² = c² siku-siku, jika a² + b² &gt; c² lancip, jika a² + b² &lt; c² tumpul."],
                [("Sisi siku-siku 6 cm dan 8 cm. Sisi miring?", ["c² = 36 + 64 = 100"], "10 cm"),
                 ("Sisi miring 13 cm, satu sisi 5 cm. Sisi lain?", ["a² = 169 − 25 = 144"], "12 cm")],
                [["c = a + b", "c² = a² + b², lalu ambil akarnya"],
                 ["Mencari sisi siku-siku dengan menjumlahkan kuadrat", "Kurangkan: a² = c² − b²"],
                 ["Sisi miring dianggap sisi mana saja", "Sisi miring selalu sisi terpanjang"]],
                [("Apakah teorema Pythagoras berlaku untuk semua segitiga?", "Tidak, hanya untuk segitiga siku-siku. Untuk segitiga lain, teorema ini dipakai untuk menentukan jenisnya."),
                 ("Apa itu tripel Pythagoras?", "Tiga bilangan asli a, b, c yang memenuhi a² + b² = c², misalnya 3, 4, 5 atau 5, 12, 13."),
                 ("Bagaimana mencari jarak dua titik pada bidang koordinat?", "Hitung selisih x dan selisih y, lalu gunakan teorema Pythagoras.")])


# ============================================================ 4. relasi dan fungsi
def u4():
    def apakah():
        A = sh([1, 2, 3, 4])
        B = ["a", "b", "c", "d"]
        good = [(x, ch(B)) for x in A]
        bad1 = good[:-1] + [(good[0][0], ch([b for b in B if b != good[0][1]]))]
        bad2 = good[:-1]
        k = ri(0, 1)
        f = lambda l: "{" + ", ".join("(%d, %s)" % p for p in l) + "}"
        if k == 0:
            return M("A = {1, 2, 3, 4} dan B = {a, b, c, d}. Manakah himpunan pasangan berurutan yang merupakan fungsi dari A ke B?", f(good),
                     [f(bad1), f(bad2), f(bad1[:-1] + [(bad1[-1][0], "a"), (good[1][0], "d" if good[1][1] != "d" else "c")])],
                     "Fungsi: setiap anggota A berpasangan dengan tepat satu anggota B. Hanya %s yang memenuhi." % f(good))
        return M("Relasi dari A = {1, 2, 3, 4} ke B = {a, b, c, d} berikut: %s. Relasi ini …" % f(bad1),
                 "bukan fungsi, karena %d berpasangan dengan dua anggota B" % good[0][0],
                 ["fungsi, karena semua anggota B mempunyai pasangan", "fungsi, karena setiap anggota A mempunyai pasangan", "bukan fungsi, karena ada anggota B yang tidak berpasangan"],
                 "Anggota %d mempunyai dua pasangan, jadi bukan fungsi." % good[0][0])

    def daerah():
        xs = sorted(sh(range(1, 8))[:4])
        a, b = nz(-3, 4), nz(-5, 6)
        ys = [a * x + b for x in xs]
        f = lambda l: "{" + ", ".join(sn(v) for v in l) + "}"
        k = ri(0, 1)
        q = "Fungsi f(x) = %s dengan domain %s." % (lin(a, b), f(xs))
        if k == 0:
            return M(q + " Daerah hasilnya adalah …", f(ys), [f(xs), f([a * x - b for x in xs]), f([a + x + b for x in xs])], "Hitung f(x) untuk setiap x: %s." % ", ".join("f(%d) = %s" % (x, sn(y)) for x, y in zip(xs, ys)))
        pairs = "{" + ", ".join("(%d, %s)" % (x, sn(y)) for x, y in zip(xs, ys)) + "}"
        return M("Fungsi dinyatakan dengan pasangan berurutan %s. Domain fungsi itu adalah …" % pairs, f(xs), [f(ys), f(xs + ys[:1]) if ys[0] not in xs else f(xs[:-1]), f(sorted(set(xs + ys)))],
                 "Domain adalah himpunan semua nilai pertama (x): %s." % f(xs))

    def nilai():
        a, b = nz(-6, 6), nz(-12, 12)
        x = nz(-6, 6)
        k = ri(0, 2)
        if k == 0:
            return MN("Diketahui f(x) = %s. Nilai f(%s) adalah …" % (lin(a, b), sn(x)), a * x + b, [a * x - b, a * (-x) + b, a + x + b], "f(%s) = %s %s %d = %s." % (sn(x), ("%s × %s" % (sn(a), par(x))) if a not in (1, -1) else ("%s%s" % ("" if a == 1 else MINUS, par(x))), "+" if b > 0 else "−", abs(b), sn(a * x + b)))
        if k == 1:
            y = a * x + b
            return MN("Diketahui f(x) = %s dan f(p) = %s. Nilai p adalah …" % (lin(a, b), sn(y)), x, [-x, y, Fr(y + b, a) if Fr(y + b, a).denominator == 1 else x + 1], "%s = %s → %s = %s → p = %s." % (lin(a, b, "p"), sn(y), expr([(a, "p")]), sn(y - b), sn(x)))
        c = nz(-4, 4)
        v = a * x * x + c if False else a * x + b
        return MN("Diketahui f(x) = %s. Nilai f(%s) − f(%s) adalah …" % (lin(a, b), sn(x + 2), sn(x)), 2 * a, [2 * a + b, a, 2 * a + 2 * b], "f(%s) − f(%s) = %s − %s = %s." % (sn(x + 2), sn(x), sn(a * (x + 2) + b), par(a * x + b), sn(2 * a)))

    def rumus():
        a, b = nz(-5, 6), nz(-10, 10)
        x1, x2 = sorted(sh(range(-4, 6))[:2])
        y1, y2 = a * x1 + b, a * x2 + b
        k = ri(0, 1)
        if k == 0:
            return M("Fungsi f(x) = ax + b dengan f(%s) = %s dan f(%s) = %s. Rumus fungsinya …" % (sn(x1), sn(y1), sn(x2), sn(y2)), "f(x) = %s" % lin(a, b),
                     ["f(x) = %s" % lin(b, a), "f(x) = %s" % lin(a, -b), "f(x) = %s" % lin(-a, b)], "a = (%s − %s) : (%s − %s) = %s, lalu b = %s." % (sn(y2), par(y1), sn(x2), par(x1), sn(a), sn(b)))
        xs = [0, 1, 2, 3]
        rows = [["x"] + [sn(x) for x in xs], ["f(x)"] + [sn(a * x + b) for x in xs]]
        t = "<table class='sn-table'><tbody>%s</tbody></table>" % "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
        return M("Tabel fungsi berikut sesuai dengan rumus …" + t, "f(x) = %s" % lin(a, b), ["f(x) = %s" % lin(b, a) if b != a else "f(x) = %s" % lin(a + 1, b - 1), "f(x) = %s" % lin(1, b + a) if a != 1 else "f(x) = %s" % lin(2, b - 1), "f(x) = %s" % lin(a, -b)],
                 "Setiap x bertambah 1, f(x) bertambah %s, jadi a = %s. f(0) = %s, jadi b = %s." % (sn(a), sn(a), sn(b), sn(b)))

    def banyak():
        n, m = ri(2, 5), ri(2, 4)
        k = ri(0, 1)
        if k == 0:
            return MN("A = {%s} dan B = {%s}. Banyak fungsi yang mungkin dari A ke B adalah …" % (", ".join("abcde"[:n]), ", ".join(str(i) for i in range(1, m + 1))), m ** n,
                      [n ** m if n ** m != m ** n else m * n + 1, m * n, m ** n + 1], "Setiap anggota A punya %d pilihan pasangan: %d%s = %d." % (m, m, sup(n), m ** n))
        n = ri(2, 6)
        f = math.factorial(n)
        return MN("Banyak korespondensi satu-satu antara dua himpunan yang masing-masing mempunyai %d anggota adalah …" % n, f, [n * n, 2 ** n if 2 ** n != f else f + 1, n], "%d! = %d." % (n, f))

    sets = [("Relasi dan fungsi", [(apakah, 20)]),
            ("Domain dan daerah hasil", [(daerah, 20)]),
            ("Nilai fungsi", [(nilai, 20)]),
            ("Menentukan rumus fungsi", [(rumus, 20)]),
            ("Banyak fungsi dan campuran", [(banyak, 8), (nilai, 6), (rumus, 6)])]
    return unit("relasi-dan-fungsi", "A", 4, "Relasi dan Fungsi", "Relasi dan Fungsi",
                "Peserta didik memahami relasi dan fungsi (domain, kodomain, daerah hasil), menyajikannya dalam berbagai bentuk, dan menentukan nilai serta rumus fungsi linear.",
                "Latihan relasi dan fungsi kelas 8 SMP: membedakan relasi dan fungsi, domain, kodomain, daerah hasil, nilai fungsi, menentukan rumus fungsi linear, dan korespondensi satu-satu. 100 soal dengan kunci jawaban.",
                "Setiap x punya tepat satu pasangan", "f(x) = ax + b: ganti x dengan bilangannya.", sets,
                ["Relasi adalah aturan yang memasangkan anggota himpunan A dengan anggota himpunan B. Fungsi adalah relasi khusus: setiap anggota A berpasangan dengan tepat satu anggota B.",
                 "Domain adalah himpunan asal (A), kodomain adalah himpunan kawan (B), dan daerah hasil adalah himpunan semua pasangan yang benar-benar dipakai.",
                 "Pada fungsi f(x) = ax + b, nilai f(3) didapat dengan mengganti x dengan 3. Dari dua nilai fungsi, a = perubahan f(x) : perubahan x."],
                [("f(x) = 3x − 5. Nilai f(−2)?", ["3 × (−2) − 5"], "−11"),
                 ("f(1) = 4 dan f(3) = 10. Rumus f?", ["a = (10 − 4) : (3 − 1) = 3", "b = 4 − 3 = 1"], "f(x) = 3x + 1")],
                [["Relasi dengan anggota B yang tidak berpasangan dianggap bukan fungsi", "Yang penting setiap anggota A tepat satu pasangan"],
                 ["Daerah hasil disamakan dengan kodomain", "Daerah hasil hanya pasangan yang dipakai"],
                 ["f(−2) untuk f(x) = 3x − 5 dihitung 3 − 2 − 5", "f(−2) = 3 × (−2) − 5 = −11"]],
                [("Apa beda relasi dan fungsi?", "Setiap fungsi adalah relasi, tetapi tidak setiap relasi adalah fungsi. Pada fungsi, setiap anggota domain punya tepat satu pasangan."),
                 ("Apa itu korespondensi satu-satu?", "Fungsi yang setiap anggota A berpasangan dengan tepat satu anggota B, dan sebaliknya. Banyak anggota A dan B harus sama."),
                 ("Bagaimana fungsi dapat disajikan?", "Dengan diagram panah, himpunan pasangan berurutan, tabel, rumus, atau grafik.")])


# ============================================================ 5. persamaan garis lurus
def u5():
    def grad2():
        while True:
            x1, y1, x2, y2 = ri(-6, 6), ri(-6, 6), ri(-6, 6), ri(-6, 6)
            if x1 != x2:
                break
        m = Fr(y2 - y1, x2 - x1)
        return M("Gradien garis yang melalui titik (%s, %s) dan (%s, %s) adalah …" % (sn(x1), sn(y1), sn(x2), sn(y2)), fq(m),
                 [fq(1 / m) if m else "1", fq(-m) if m else fq(Fr(1, 2)), fq(Fr(y2 + y1, x2 - x1)) if Fr(y2 + y1, x2 - x1) != m else fq(m + 1), fq(m + 1)],
                 "m = (y₂ − y₁) : (x₂ − x₁) = (%s − %s) : (%s − %s) = %s." % (sn(y2), par(y1), sn(x2), par(x1), fq(m)))

    def grad_pers():
        k = ri(0, 1)
        if k == 0:
            m, c = Fr(nz(-6, 6), ch([1, 1, 2, 3])), nz(-9, 9)
            return M("Gradien garis y = %s adalah …" % expr([(m, "x"), (c, "")]), fq(m), [sn(c), fq(-m), fq(1 / m)], "Pada y = mx + c, gradiennya m = %s." % fq(m))
        a, b, c = nz(-6, 6), nz(-6, 6), nz(-12, 12)
        m = Fr(-a, b)
        return M("Gradien garis %s = %s adalah …" % (expr([(a, "x"), (b, "y")]), sn(c)), fq(m), [fq(-m), fq(Fr(b, a)) if Fr(b, a) != m else fq(m + 1), fq(Fr(c, b)) if Fr(c, b) != m else fq(m - 1), fq(Fr(-b, a))],
                 "Ubah ke y = mx + c: y = %s, jadi m = −a/b = %s." % (expr([(m, "x"), (Fr(c, b), "")]), fq(m)))

    def pers():
        m, x1, y1 = nz(-5, 5), ri(-5, 5), ri(-6, 6)
        c = y1 - m * x1
        k = ri(0, 1)
        if k == 0:
            return M("Persamaan garis yang melalui titik (%s, %s) dengan gradien %s adalah …" % (sn(x1), sn(y1), sn(m)), "y = %s" % lin(m, c),
                     ["y = %s" % lin(m, y1 + m * x1) if y1 + m * x1 != c else "y = %s" % lin(m, c + 1), "y = %s" % lin(-m, c), "y = %s" % lin(m, -c) if c else "y = %s" % lin(m, 2)],
                     "y − %s = %s(x − %s) → y = %s." % (par(y1), sn(m), par(x1), lin(m, c)))
        x2 = x1 + ch([1, 2, 3])
        y2 = y1 + m * (x2 - x1)
        return M("Persamaan garis yang melalui titik (%s, %s) dan (%s, %s) adalah …" % (sn(x1), sn(y1), sn(x2), sn(y2)), "y = %s" % lin(m, c),
                 ["y = %s" % lin(-m, c), "y = %s" % lin(m, c + m), "y = %s" % lin(Fr(1, m), c) if m not in (1, -1) else "y = %s" % lin(m, -c if c else 3)],
                 "m = %s, lalu y = %s." % (sn(m), lin(m, c)))

    def sejajar():
        m = Fr(nz(-5, 5), ch([1, 1, 2]))
        c = nz(-8, 8)
        k = ri(0, 1)
        if k == 0:
            return M("Gradien garis yang sejajar dengan y = %s adalah …" % expr([(m, "x"), (c, "")]), fq(m), [fq(-m), fq(-1 / m), fq(1 / m) if 1 / m != m else sn(c)], "Garis sejajar mempunyai gradien yang sama: %s." % fq(m))
        return M("Gradien garis yang tegak lurus dengan y = %s adalah …" % expr([(m, "x"), (c, "")]), fq(-1 / m), [fq(m), fq(-m) if -m != -1 / m else fq(m * 2), fq(1 / m)],
                 "Garis tegak lurus: m₁ × m₂ = −1, jadi m₂ = −1 : %s = %s." % (par(m) if m.denominator == 1 else fq(m), fq(-1 / m)))

    def potong():
        a, b = nz(-5, 5), nz(-5, 5)
        g = math.gcd(a, b)
        c = a * b * ri(1, 3) * ch([1, -1])
        k = ri(0, 1)
        e = "%s = %s" % (expr([(a, "x"), (b, "y")]), sn(c))
        if k == 0:
            return M("Titik potong garis %s dengan sumbu x adalah …" % e, "(%s, 0)" % sn(Fr(c, a)), ["(0, %s)" % sn(Fr(c, a)), "(%s, 0)" % sn(Fr(c, b)) if Fr(c, b) != Fr(c, a) else "(%s, 0)" % sn(-Fr(c, a)), "(0, %s)" % sn(Fr(c, b))],
                     "Sumbu x berarti y = 0: %s = %s, x = %s." % (expr([(a, "x")]), sn(c), sn(Fr(c, a))))
        return M("Titik potong garis %s dengan sumbu y adalah …" % e, "(0, %s)" % sn(Fr(c, b)), ["(%s, 0)" % sn(Fr(c, b)), "(0, %s)" % sn(Fr(c, a)) if Fr(c, a) != Fr(c, b) else "(0, %s)" % sn(-Fr(c, b)), "(%s, 0)" % sn(Fr(c, a))],
                 "Sumbu y berarti x = 0: %s = %s, y = %s." % (expr([(b, "y")]), sn(c), sn(Fr(c, b))))

    def grafik():
        m = Fr(nz(-3, 3), ch([1, 1, 2]))
        c = ri(-3, 3)
        if abs(m * 4 + c) > 5 and abs(-m * 4 + c) > 5 and False:
            return None
        pic = kosy(lines=[(m, c, BLUE, "")], lo=-5, hi=5, label="grafik garis lurus")
        e = lambda mm, cc: "y = %s" % expr([(mm, "x"), (cc, "")])
        return M("Persamaan garis pada grafik berikut adalah …" + pic, e(m, c), [e(-m, c), e(m, -c) if c else e(m, 1), e(1 / m, c) if 1 / m != m else e(m, c + 2)],
                 "Garis memotong sumbu y di %s, dan setiap ke kanan %d satuan naik %s satuan, jadi m = %s." % (sn(c), m.denominator, sn(m.numerator), fq(m)))

    sets = [("Gradien dari dua titik", [(grad2, 20)]),
            ("Gradien dari persamaan", [(grad_pers, 14), (sejajar, 6)]),
            ("Menentukan persamaan garis", [(pers, 20)]),
            ("Garis sejajar, tegak lurus, dan titik potong", [(sejajar, 10), (potong, 10)]),
            ("Membaca grafik", [(grafik, 20)])]
    return unit("persamaan-garis-lurus", "A", 5, "Persamaan Garis Lurus dan Gradien", "Persamaan Garis Lurus",
                "Peserta didik menentukan gradien, persamaan garis lurus, titik potong dengan sumbu, serta hubungan garis sejajar dan tegak lurus, dan membaca grafiknya.",
                "Latihan persamaan garis lurus kelas 8 SMP: gradien dari dua titik dan dari persamaan, persamaan garis melalui titik, garis sejajar dan tegak lurus, titik potong sumbu, dan membaca grafik. 100 soal dengan kunci jawaban.",
                "m = (y₂ − y₁) : (x₂ − x₁)", "y = mx + c: m gradien, c titik potong sumbu y.", sets,
                ["Gradien (kemiringan) garis m = perubahan y : perubahan x = (y₂ − y₁) : (x₂ − x₁). Garis naik ke kanan bergradien positif, turun ke kanan negatif.",
                 "Pada y = mx + c, m adalah gradien dan garis memotong sumbu y di (0, c). Pada ax + by = c, gradiennya −a/b.",
                 "Persamaan garis melalui (x₁, y₁) bergradien m: y − y₁ = m(x − x₁). Garis sejajar gradiennya sama; garis tegak lurus m₁ × m₂ = −1."],
                [("Gradien garis melalui (1, 2) dan (4, 11)?", ["(11 − 2) : (4 − 1) = 9 : 3"], "3"),
                 ("Garis melalui (2, −1) dengan gradien 3?", ["y + 1 = 3(x − 2)"], "y = 3x − 7")],
                [["m = (x₂ − x₁) : (y₂ − y₁)", "y di atas, x di bawah: m = (y₂ − y₁) : (x₂ − x₁)"],
                 ["Gradien 2x + 3y = 6 adalah 2", "Ubah ke y = −2/3 x + 2, gradiennya −2/3"],
                 ["Gradien tegak lurus dari 2 adalah −2", "m₂ = −1/2 (kebalikan dan berlawanan tanda)"]],
                [("Apa arti gradien 0?", "Garisnya mendatar (sejajar sumbu x), misalnya y = 3."),
                 ("Bagaimana mengetahui dua garis tegak lurus?", "Kalikan gradiennya. Jika hasilnya −1, kedua garis tegak lurus."),
                 ("Bagaimana menggambar garis y = 2x − 1?", "Cari dua titik, misalnya x = 0 → y = −1 dan x = 2 → y = 3, lalu hubungkan keduanya.")])


# ============================================================ 6. SPLDV
def u6():
    def solve():
        x, y = nz(-8, 8), nz(-8, 8)
        a1, b1, a2, b2 = nz(-5, 5), nz(-5, 5), nz(-5, 5), nz(-5, 5)
        if a1 * b2 == a2 * b1:
            return None
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        k = ri(0, 1)
        sy = "<span class='sys'>%s = %s<br>%s = %s</span>" % (expr([(a1, "x"), (b1, "y")]), sn(c1), expr([(a2, "x"), (b2, "y")]), sn(c2))
        if k == 0:
            return M("Penyelesaian sistem persamaan %s adalah …" % sy, "x = %s, y = %s" % (sn(x), sn(y)), ["x = %s, y = %s" % (sn(y), sn(x)) if x != y else "x = %s, y = %s" % (sn(-x), sn(y)), "x = %s, y = %s" % (sn(-x), sn(-y)), "x = %s, y = %s" % (sn(x), sn(-y))],
                     "Eliminasi salah satu variabel, lalu substitusi. Hasilnya x = %s dan y = %s." % (sn(x), sn(y)))
        w = ch(["x", "y"])
        return MN("Diketahui sistem persamaan %s. Nilai %s adalah …" % (sy, w), x if w == "x" else y, [y if w == "x" else x, -(x if w == "x" else y), (x if w == "x" else y) + 1, (x if w == "x" else y) - 2],
                  "Penyelesaiannya x = %s dan y = %s." % (sn(x), sn(y)))

    def subst():
        x, y = nz(-7, 7), nz(-7, 7)
        m, c = nz(-4, 4), 0
        c = y - m * x
        a, b = nz(-4, 4), nz(-4, 4)
        d = a * x + b * y
        sy = "<span class='sys'>y = %s<br>%s = %s</span>" % (lin(m, c), expr([(a, "x"), (b, "y")]), sn(d))
        if a + b * m == 0:
            return None
        w = ch(["x", "y", "x + y", "x − y"])
        v = {"x": x, "y": y, "x + y": x + y, "x − y": x - y}[w]
        return MN("Dari sistem %s, nilai %s adalah …" % (sy, w), v, [v + 1, -v, {"x": y, "y": x, "x + y": x - y, "x − y": x + y}[w], v - 2],
                  "Substitusi y = %s ke persamaan kedua: x = %s, y = %s. Jadi %s = %s." % (lin(m, c), sn(x), sn(y), w, sn(v)))

    def cek():
        x, y = nz(-6, 6), nz(-6, 6)
        a1, b1, a2, b2 = nz(-4, 4), nz(-4, 4), nz(-4, 4), nz(-4, 4)
        if a1 * b2 == a2 * b1:
            return None
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        sy = "<span class='sys'>%s = %s<br>%s = %s</span>" % (expr([(a1, "x"), (b1, "y")]), sn(c1), expr([(a2, "x"), (b2, "y")]), sn(c2))
        return M("Pasangan (x, y) manakah yang merupakan penyelesaian %s?" % sy, "(%s, %s)" % (sn(x), sn(y)), ["(%s, %s)" % (sn(y), sn(x)), "(%s, %s)" % (sn(x + 1), sn(y)), "(%s, %s)" % (sn(x), sn(y - 1)), "(%s, %s)" % (sn(-x), sn(y))],
                 "Substitusikan (%s, %s) ke kedua persamaan; keduanya benar." % (sn(x), sn(y)))

    def cerita():
        k = ri(0, 4)
        if k == 0:
            x, y = ri(2, 9) * 1000, ri(1, 6) * 500
            a, b, c, d = ri(1, 4), ri(1, 5), ri(1, 4), ri(1, 5)
            if a * d == b * c:
                return None
            return M("Harga %d buku dan %d pensil %s. Harga %d buku dan %d pensil %s. Harga 1 buku dan 1 pensil …" % (a, b, rp(a * x + b * y), c, d, rp(c * x + d * y)), rp(x + y),
                     [rp(x), rp(y), rp(x + 2 * y)], "Selesaikan: buku = %s, pensil = %s. Jumlahnya %s." % (rp(x), rp(y), rp(x + y)))
        if k == 1:
            x, y = ri(10, 40), ri(5, 30)
            if x == y:
                return None
            return MN("Jumlah dua bilangan %d dan selisihnya %d. Bilangan yang lebih besar adalah …" % (x + y, abs(x - y)), max(x, y), [min(x, y), x + y, abs(x - y)], "a + b = %d, a − b = %d → 2a = %d → a = %d." % (x + y, abs(x - y), 2 * max(x, y), max(x, y)))
        if k == 2:
            p, l = ri(8, 20), ri(3, 12)
            if p <= l:
                return None
            return MN("Keliling persegi panjang %d cm. Panjangnya %d cm lebih dari lebarnya. Luasnya …" % (2 * (p + l), p - l), p * l, [2 * (p + l), p + l, (p + 1) * (l - 1)], "p + l = %d dan p − l = %d → p = %d, l = %d. Luas %d cm²." % (p + l, p - l, p, l, p * l), unit="cm²")
        if k == 3:
            m, n = ri(10, 25), ri(10, 25)
            tot = m + n
            kaki = 2 * m + 4 * n
            return MN("Di kandang ada ayam dan kambing sebanyak %d ekor. Jumlah kakinya %d. Banyak kambing …" % (tot, kaki), n, [m, tot // 2 if tot % 2 == 0 and tot // 2 != n else n + 1, kaki // 4], "a + k = %d, 2a + 4k = %d → 2k = %d → k = %d ekor." % (tot, kaki, kaki - 2 * tot, n), unit="ekor")
        a, b = ri(20, 45), ri(3, 15)
        return MN("Umur ayah sekarang %d tahun lebih tua dari umur anaknya. Jumlah umur mereka %d tahun. Umur anak sekarang …" % (a, 2 * b + a), b, [a + b, (2 * b + a) // 2, b + 1], "x + (x + %d) = %d → x = %d tahun." % (a, 2 * b + a, b), unit="tahun")

    sets = [("Menyelesaikan SPLDV", [(solve, 20)]),
            ("Metode substitusi", [(subst, 20)]),
            ("Memeriksa penyelesaian", [(cek, 14), (solve, 6)]),
            ("Soal cerita", [(cerita, 20)]),
            ("Campuran", [(solve, 7), (subst, 7), (cerita, 6)])]
    return unit("sistem-persamaan-linear-dua-variabel", "A", 6, "Sistem Persamaan Linear Dua Variabel (SPLDV)", "SPLDV",
                "Peserta didik menyelesaikan sistem persamaan linear dua variabel dengan metode substitusi, eliminasi, atau grafik, serta menggunakannya untuk menyelesaikan masalah.",
                "Latihan sistem persamaan linear dua variabel (SPLDV) kelas 8 SMP: metode eliminasi dan substitusi, memeriksa penyelesaian, dan soal cerita harga barang, umur, keliling, dan kaki hewan. 100 soal dengan kunci jawaban.",
                "Hilangkan satu variabel dulu", "Eliminasi atau substitusi, lalu cari variabel kedua.", sets,
                ["SPLDV terdiri dari dua persamaan linear dengan dua variabel (misalnya x dan y). Penyelesaiannya adalah pasangan (x, y) yang memenuhi kedua persamaan.",
                 "Metode eliminasi: samakan koefisien salah satu variabel, lalu jumlahkan atau kurangkan kedua persamaan. Metode substitusi: nyatakan satu variabel dari satu persamaan, lalu masukkan ke persamaan lain.",
                 "Pada grafik, penyelesaian SPLDV adalah titik potong kedua garis."],
                [("x + y = 10 dan x − y = 4", ["Jumlahkan: 2x = 14, x = 7", "y = 10 − 7"], "x = 7, y = 3"),
                 ("y = 2x dan x + y = 9", ["x + 2x = 9, x = 3"], "x = 3, y = 6")],
                [["Hanya mencari x lalu berhenti", "Substitusikan x untuk mencari y juga"],
                 ["Mengurangkan persamaan dengan tanda salah", "Kurangkan setiap suku, termasuk tandanya"],
                 ["Tidak memeriksa jawaban", "Masukkan (x, y) ke kedua persamaan"]],
                [("Kapan memakai eliminasi dan kapan substitusi?", "Substitusi mudah jika salah satu persamaan sudah berbentuk y = … atau x = …. Eliminasi mudah jika koefisiennya mudah disamakan."),
                 ("Apakah SPLDV selalu punya satu penyelesaian?", "Tidak. Jika kedua garis sejajar, tidak ada penyelesaian. Jika kedua garis berimpit, penyelesaiannya tak terhingga."),
                 ("Bagaimana membuat model SPLDV dari soal cerita?", "Misalkan dua hal yang belum diketahui dengan x dan y, lalu tulis dua persamaan dari dua keterangan di soal.")])


# ============================================================ 7. faktorisasi
def u7():
    def kali():
        a, b = nz(-9, 9), nz(-9, 9)
        k = ri(0, 2)
        if k == 0:
            q = "(x %s %d)(x %s %d)" % ("+" if a > 0 else MINUS, abs(a), "+" if b > 0 else MINUS, abs(b))
            c = expr([(1, "x²"), (a + b, "x"), (a * b, "")])
            return M("Hasil dari %s adalah …" % q, c, [expr([(1, "x²"), (a * b, "x"), (a + b, "")]), expr([(1, "x²"), (a * b, "")]), expr([(1, "x²"), (a + b, "x"), (-a * b, "")])],
                     "x × x + x × %s + %s × x + %s × %s = %s." % (par(b), par(a), par(a), par(b), c))
        if k == 1:
            a = ri(2, 9)
            c = "x² − %d" % (a * a)
            return M("Hasil dari (x + %d)(x − %d) adalah …" % (a, a), c, ["x² + %d" % (a * a), "x² − %dx − %d" % (2 * a, a * a), "x² − %d" % (2 * a)], "(a + b)(a − b) = a² − b² = x² − %d." % (a * a))
        a = nz(-8, 8)
        c = expr([(1, "x²"), (2 * a, "x"), (a * a, "")])
        return M("Hasil dari (x %s %d)² adalah …" % ("+" if a > 0 else MINUS, abs(a)), c, [expr([(1, "x²"), (a * a, "")]), expr([(1, "x²"), (a, "x"), (a * a, "")]), expr([(1, "x²"), (2 * a, "x"), (-a * a, "")])],
                 "(a + b)² = a² + 2ab + b² = %s." % c)

    def faktor_sama():
        a = ri(2, 9)
        p, q = nz(-9, 9), nz(-9, 9)
        if math.gcd(p, q) != 1:
            return None
        v = ch(["x", "y", "a"])
        k = ri(0, 1)
        if k == 0:
            e = expr([(a * p, v), (a * q, "")])
            c = "%d(%s)" % (a, lin(p, q, v))
            return M("Bentuk faktor dari %s adalah …" % e, c, ["%d(%s)" % (a, lin(p, a * q, v)), "%s(%s)" % (v, lin(a * p, a * q, "")) if False else "%d(%s)" % (a * p, lin(1, q, v)), "%d(%s)" % (a, lin(p, -q, v))],
                     "FPB dari %d dan %d adalah %d, jadi %s." % (abs(a * p), abs(a * q), a, c))
        e = expr([(a * p, v + "²"), (a * q, v)])
        c = "%d%s(%s)" % (a, v, lin(p, q, v))
        return M("Bentuk faktor dari %s adalah …" % e, c, ["%d(%s)" % (a, expr([(p, v + "²"), (q, v)])), "%s(%s)" % (v, lin(a * p, q, v)), "%d%s(%s)" % (a, v, lin(p, -q, v))],
                 "Faktor persekutuan %d%s, jadi %s." % (a, v, c))

    def trinomial():
        a, b = nz(-9, 9), nz(-9, 9)
        if a + b == 0:
            return None
        e = expr([(1, "x²"), (a + b, "x"), (a * b, "")])
        f = lambda p, q: "(x %s %d)(x %s %d)" % ("+" if p > 0 else MINUS, abs(p), "+" if q > 0 else MINUS, abs(q))
        p, q = sorted([a, b], reverse=True)
        c = f(p, q)
        ws = [f(-p, -q), f(p, -q) if p != -q else f(p + 1, q - 1), f(-p, q) if -p != q else f(p - 1, q + 1)]
        if a * b in (0,):
            return None
        return M("Bentuk faktor dari %s adalah …" % e, c, ws, "Cari dua bilangan yang hasil kalinya %s dan jumlahnya %s: %s dan %s." % (sn(a * b), sn(a + b), sn(p), sn(q)))

    def selisih():
        a = ri(1, 9)
        b = ri(1, 4)
        v = ch(["x", "y", "p"])
        k = ri(0, 1)
        if k == 0:
            e = "%s² − %d" % (v, a * a)
            c = "(%s + %d)(%s − %d)" % (v, a, v, a)
            return M("Bentuk faktor dari %s adalah …" % e, c, ["(%s − %d)²" % (v, a), "(%s + %d)²" % (v, a), "(%s − %d)(%s − %d)" % (v, a, v, a * a)] if a > 1 else ["(%s − 1)²" % v, "(%s + 1)²" % v, "%s(%s − 1)" % (v, v)],
                     "a² − b² = (a + b)(a − b), dengan b = %d." % a)
        e = "%d%s² − %d" % (b * b, v, a * a)
        if b == 1 or math.gcd(a, b) != 1:
            return None
        c = "(%d%s + %d)(%d%s − %d)" % (b, v, a, b, v, a)
        return M("Bentuk faktor dari %s adalah …" % e, c, ["(%d%s − %d)²" % (b, v, a), "(%d%s + %d)(%d%s − %d)" % (b * b, v, a, b * b, v, a), "(%d%s + %d)(%s − %d)" % (b, v, a * a, v, 1)],
                 "%d%s² = (%d%s)² dan %d = %d², jadi %s." % (b * b, v, b, v, a * a, a, c))

    def ax2():
        a = ch([2, 3, 5])
        p, q = nz(-6, 6), nz(-6, 6)
        # (a x + p)(x + q) = a x² + (aq + p) x + pq
        if math.gcd(a, p) != 1:
            return None
        e = expr([(a, "x²"), (a * q + p, "x"), (p * q, "")])
        f = lambda r, s: "(%dx %s %d)(x %s %d)" % (a, "+" if r > 0 else MINUS, abs(r), "+" if s > 0 else MINUS, abs(s))
        c = f(p, q)
        if a * q + p == 0:
            return None
        return M("Bentuk faktor dari %s adalah …" % e, c, [f(q, p) if q != p else f(-p, q), f(-p, -q), f(p, -q)], "Periksa dengan mengalikan: %s = %s." % (c, e))

    sets = [("Perkalian bentuk aljabar", [(kali, 20)]),
            ("Faktor persekutuan", [(faktor_sama, 20)]),
            ("Faktorisasi x² + bx + c", [(trinomial, 20)]),
            ("Selisih dua kuadrat", [(selisih, 20)]),
            ("Faktorisasi ax² + bx + c dan campuran", [(ax2, 10), (trinomial, 5), (selisih, 5)])]
    return unit("faktorisasi-bentuk-aljabar", "A", 7, "Perkalian dan Faktorisasi Bentuk Aljabar", "Faktorisasi Bentuk Aljabar",
                "Peserta didik melakukan perkalian bentuk aljabar dan memfaktorkan bentuk aljabar: faktor persekutuan, trinomial, dan selisih dua kuadrat.",
                "Latihan faktorisasi bentuk aljabar kelas 8 SMP: perkalian suku dua, kuadrat suku dua, faktor persekutuan, memfaktorkan x² + bx + c dan ax² + bx + c, serta selisih dua kuadrat. 100 soal dengan kunci jawaban.",
                "x² + bx + c = (x + p)(x + q)", "p × q = c dan p + q = b.", sets,
                ["Perkalian suku dua: (x + a)(x + b) = x² + (a + b)x + ab. Kuadrat: (x + a)² = x² + 2ax + a². Selisih: (x + a)(x − a) = x² − a².",
                 "Memfaktorkan adalah kebalikan dari mengalikan. Mulailah dengan mencari faktor persekutuan, misalnya 6x + 9 = 3(2x + 3).",
                 "Untuk x² + bx + c, cari dua bilangan p dan q dengan p × q = c dan p + q = b. Untuk a² − b², gunakan (a + b)(a − b)."],
                [("Faktorkan x² + 7x + 12.", ["3 × 4 = 12 dan 3 + 4 = 7"], "(x + 3)(x + 4)"),
                 ("Faktorkan 4x² − 25.", ["(2x)² − 5²"], "(2x + 5)(2x − 5)")],
                [["(x + 3)² = x² + 9", "(x + 3)² = x² + 6x + 9"],
                 ["x² − 5x + 6 = (x + 2)(x + 3)", "Hasil kali 6 dan jumlah −5: (x − 2)(x − 3)"],
                 ["x² + 9 = (x + 3)(x − 3)", "x² + 9 tidak dapat difaktorkan; yang dapat adalah x² − 9"]],
                [("Bagaimana memeriksa hasil faktorisasi?", "Kalikan kembali faktor-faktornya. Jika hasilnya sama dengan bentuk awal, faktorisasinya benar."),
                 ("Apa itu selisih dua kuadrat?", "Bentuk a² − b², yang faktornya (a + b)(a − b)."),
                 ("Mengapa faktorisasi berguna?", "Untuk menyederhanakan pecahan bentuk aljabar dan menyelesaikan persamaan kuadrat.")])


# ============================================================ 8. lingkaran
def u8():
    def pi_of(r):
        return (Fr(22, 7), "22/7") if r % 7 == 0 else (Fr(314, 100), "3,14")

    def val(x):
        return dz(x) if S.endlich(x) else fq(x)

    def unsur():
        F = [("garis yang menghubungkan titik pusat dengan titik pada lingkaran", "jari-jari"), ("tali busur yang melalui titik pusat", "diameter"),
             ("garis yang menghubungkan dua titik pada lingkaran", "tali busur"), ("bagian lengkung lingkaran di antara dua titik", "busur"),
             ("daerah yang dibatasi dua jari-jari dan sebuah busur", "juring"), ("daerah yang dibatasi tali busur dan busurnya", "tembereng"),
             ("jarak terpendek dari titik pusat ke tali busur", "apotema")]
        d, c = ch(F)
        return M("Pada lingkaran, %s disebut …" % d, c, [x for x in sh([f[1] for f in F]) if x != c], "Itulah pengertian %s." % c)

    def keliling():
        r = ch([7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 10, 20, 5, 30, 15, 25, 40, 50, 8, 12])
        p, ps = pi_of(r)
        k = ri(0, 2)
        if k == 0:
            v = 2 * p * r
            return M("Keliling lingkaran dengan jari-jari %d cm adalah … (π = %s)" % (r, ps), "%s cm" % val(v), ["%s cm" % val(p * r), "%s cm" % val(p * r * r), "%s cm" % val(4 * p * r)], "K = 2πr = 2 × %s × %d = %s cm." % (ps, r, val(v)))
        if k == 1:
            d = 2 * r
            v = p * d
            return M("Keliling lingkaran dengan diameter %d cm adalah … (π = %s)" % (d, ps), "%s cm" % val(v), ["%s cm" % val(2 * p * d), "%s cm" % val(p * r * r), "%s cm" % val(p * r)], "K = πd = %s × %d = %s cm." % (ps, d, val(v)))
        v = 2 * p * r
        return MN("Keliling sebuah lingkaran %s cm. Jari-jarinya … (π = %s)" % (val(v), ps), r, [2 * r, r + 7 if r % 7 == 0 else r + 5, r // 2 if r % 2 == 0 else r * 3], "r = K : (2π) = %s : (2 × %s) = %d cm." % (val(v), ps, r), unit="cm")

    def luas():
        r = ch([7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 10, 20, 5, 30, 15, 25, 40, 50, 8, 12])
        p, ps = pi_of(r)
        k = ri(0, 1)
        if k == 0:
            v = p * r * r
            return M("Luas lingkaran dengan jari-jari %d cm adalah … (π = %s)" % (r, ps), "%s cm²" % val(v), ["%s cm²" % val(2 * p * r), "%s cm²" % val(p * 4 * r * r), "%s cm²" % val(p * r)], "L = πr² = %s × %d × %d = %s cm²." % (ps, r, r, val(v)))
        d = 2 * r
        v = p * r * r
        return M("Luas lingkaran dengan diameter %d cm adalah … (π = %s)" % (d, ps), "%s cm²" % val(v), ["%s cm²" % val(p * d * d), "%s cm²" % val(p * d), "%s cm²" % val(2 * p * r * r)], "r = %d cm, L = %s × %d² = %s cm²." % (r, ps, r, val(v)))

    def busur():
        r = ch([7, 14, 21, 28, 35, 42])
        a = ch([30, 45, 60, 72, 90, 120, 135, 150, 180, 210, 240, 270])
        p = Fr(22, 7)
        k = ri(0, 1)
        if (Fr(a, 360) * p * r * r).denominator not in (1, 2) or (Fr(a, 360) * 2 * p * r).denominator not in (1, 2):
            return None
        if k == 0:
            v = Fr(a, 360) * 2 * p * r
            return M("Panjang busur dengan sudut pusat %d° pada lingkaran berjari-jari %d cm adalah … (π = 22/7)" % (a, r), "%s cm" % val(v),
                     ["%s cm" % val(Fr(a, 360) * p * r * r), "%s cm" % val(2 * p * r), "%s cm" % val(Fr(a, 180) * 2 * p * r)], "%d/360 × 2 × 22/7 × %d = %s cm." % (a, r, val(v)))
        v = Fr(a, 360) * p * r * r
        return M("Luas juring dengan sudut pusat %d° pada lingkaran berjari-jari %d cm adalah … (π = 22/7)" % (a, r), "%s cm²" % val(v),
                 ["%s cm²" % val(Fr(a, 360) * 2 * p * r), "%s cm²" % val(p * r * r), "%s cm²" % val(Fr(a, 180) * p * r * r)], "%d/360 × 22/7 × %d² = %s cm²." % (a, r, val(v)))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            r = ch([21, 28, 35, 42, 49])
            n = ri(5, 50) * 10
            v = 2 * Fr(22, 7) * r * n
            return MD("Roda sepeda berjari-jari %d cm berputar %d kali. Jarak yang ditempuh … (π = 22/7)" % (r, n), v / 100, [Fr(22, 7) * r * n / 100, 2 * Fr(22, 7) * r / 100 * 10, v / 1000], "Satu putaran = 2 × 22/7 × %d = %d cm. %d × %d = %s cm = %s m." % (r, 2 * 22 * r // 7, n, 2 * 22 * r // 7, num(int(v)), dz(v / 100)), unit="m") if (v / 100).denominator == 1 else None
        if k == 1:
            d = ch([14, 28, 42, 56])
            h = ri(2, 9) * 5000
            v = Fr(22, 7) * d
            return M("Taman berbentuk lingkaran berdiameter %d m akan dipagari. Biaya pagar %s per meter. Biaya seluruhnya … (π = 22/7)" % (d, rp(h)), rp(int(v * h)), [rp(int(v * h / 2)), rp(int(Fr(22, 7) * (d // 2) ** 2 * h)), rp(int(v * h * 2))],
                     "Keliling = 22/7 × %d = %s m. Biaya %s × %s = %s." % (d, dz(v), dz(v), rp(h), rp(int(v * h))))
        r = ch([10, 20, 5, 15])
        s = 2 * r
        v = s * s - Fr(314, 100) * r * r
        return MD("Sebuah lingkaran berjari-jari %d cm berada tepat di dalam persegi bersisi %d cm. Luas daerah persegi di luar lingkaran … (π = 3,14)" % (r, s), v, [Fr(314, 100) * r * r, s * s, s * s - Fr(314, 100) * r * 2],
                  "%d² − 3,14 × %d² = %s − %s = %s cm²." % (s, r, num(s * s), dz(Fr(314, 100) * r * r), dz(v)), unit="cm²")

    sets = [("Unsur-unsur dan keliling lingkaran", [(unsur, 7), (keliling, 13)]),
            ("Keliling lingkaran", [(keliling, 20)]),
            ("Luas lingkaran", [(luas, 20)]),
            ("Panjang busur dan luas juring", [(busur, 20)]),
            ("Soal cerita", [(cerita, 14), (luas, 6)])]
    return unit("lingkaran", "G", 8, "Lingkaran: Keliling, Luas, Busur, dan Juring", "Lingkaran",
                "Peserta didik menjelaskan unsur-unsur lingkaran dan menghitung keliling, luas, panjang busur, dan luas juring lingkaran.",
                "Latihan lingkaran kelas 8 SMP: unsur-unsur lingkaran, keliling dan luas lingkaran, panjang busur, luas juring, dan soal cerita dengan π = 22/7 dan 3,14. 100 soal dengan kunci jawaban.",
                "K = 2πr dan L = πr²", "Busur dan juring: kalikan dengan sudut pusat/360°.", sets,
                ["Jari-jari (r) adalah jarak titik pusat ke lingkaran. Diameter d = 2r. Tali busur, busur, juring, tembereng, dan apotema juga unsur lingkaran.",
                 "Keliling K = 2πr = πd dan luas L = πr². Pakai π = 22/7 jika jari-jari kelipatan 7, selain itu π = 3,14.",
                 "Panjang busur = sudut pusat/360° × keliling. Luas juring = sudut pusat/360° × luas lingkaran."],
                [("Keliling lingkaran r = 14 cm (π = 22/7)?", ["2 × 22/7 × 14"], "88 cm"),
                 ("Luas juring 90°, r = 7 cm?", ["90/360 × 22/7 × 49"], "38,5 cm²")],
                [["L = 2πr", "L = πr²; 2πr adalah keliling"],
                 ["Memakai diameter sebagai r", "Bagi diameter dengan 2 dulu"],
                 ["Busur 60° = 60 × keliling", "Busur = 60/360 × keliling"]],
                [("Apa itu π?", "π adalah perbandingan keliling lingkaran dengan diameternya, kira-kira 3,14 atau 22/7."),
                 ("Apa beda juring dan tembereng?", "Juring dibatasi dua jari-jari dan busur. Tembereng dibatasi tali busur dan busur."),
                 ("Kapan memakai π = 22/7?", "Saat jari-jari atau diameter kelipatan 7, karena hasilnya menjadi bilangan bulat atau mudah dihitung.")])


# ============================================================ 9. prisma dan limas
def u9():
    def unsur():
        n = ri(3, 8)
        names = {3: "segitiga", 4: "segi empat", 5: "segi lima", 6: "segi enam", 7: "segi tujuh", 8: "segi delapan"}
        kind = ch(["prisma", "limas"])
        what = ch(["sisi", "rusuk", "titik sudut"])
        v = {"prisma": {"sisi": n + 2, "rusuk": 3 * n, "titik sudut": 2 * n}, "limas": {"sisi": n + 1, "rusuk": 2 * n, "titik sudut": n + 1}}[kind][what]
        alls = [n + 2, 3 * n, 2 * n, n + 1, n]
        return MN("Banyak %s pada %s %s adalah …" % (what, kind, names[n]), v, [x for x in sh(alls) if x != v], "%s alas segi-%d: sisi %d, rusuk %d, titik sudut %d." % (kind.capitalize(), n, n + 2 if kind == "prisma" else n + 1, 3 * n if kind == "prisma" else 2 * n, 2 * n if kind == "prisma" else n + 1))

    def v_prisma():
        a, t = ri(3, 12) * 2, ri(3, 12)
        T = ri(5, 20)
        k = ri(0, 1)
        if k == 0:
            v = a * t // 2 * T
            return MN("Prisma segitiga memiliki alas segitiga dengan alas %d cm dan tinggi %d cm. Tinggi prisma %d cm. Volumenya …" % (a, t, T), v, [a * t * T, a * t // 2 + T, v // 3 if v % 3 == 0 else v + T], "V = luas alas × tinggi = (½ × %d × %d) × %d = %s cm³." % (a, t, T, num(v)), unit="cm³")
        L = ri(10, 80)
        return MN("Luas alas sebuah prisma %d cm² dan tingginya %d cm. Volumenya …" % (L, T), L * T, [L * T // 3 if L * T % 3 == 0 else L + T, 2 * L + T, L * T * 2], "V = %d × %d = %s cm³." % (L, T, num(L * T)), unit="cm³")

    def v_limas():
        s = ri(3, 15)
        t = ri(2, 10) * 3
        k = ri(0, 1)
        if k == 0:
            v = s * s * t // 3
            return MN("Limas persegi dengan sisi alas %d cm dan tinggi %d cm. Volumenya …" % (s, t), v, [s * s * t, s * s * t // 2 if s * s * t % 2 == 0 else v + s, s * t // 3 * 4], "V = ⅓ × luas alas × tinggi = ⅓ × %d × %d = %s cm³." % (s * s, t, num(v)), unit="cm³")
        p, l = ri(4, 15), ri(3, 12)
        v = p * l * t // 3
        return MN("Limas dengan alas persegi panjang %d cm × %d cm dan tinggi %d cm. Volumenya …" % (p, l, t), v, [p * l * t, p * l + t, v * 2], "V = ⅓ × %d × %d × %d = %s cm³." % (p, l, t, num(v)), unit="cm³")

    def lp():
        k = ri(0, 2)
        if k == 0:
            a, b, c = ch([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15)])
            T = ri(5, 20)
            v = a * b + (a + b + c) * T
            return MN("Prisma alasnya segitiga siku-siku dengan sisi %d cm, %d cm, dan %d cm. Tinggi prisma %d cm. Luas permukaannya …" % (a, b, c, T), v,
                      [a * b // 2 * T, (a + b + c) * T, a * b // 2 + (a + b + c) * T], "LP = 2 × luas alas + keliling alas × tinggi = 2 × %d + %d × %d = %s cm²." % (a * b // 2, a + b + c, T, num(v)), unit="cm²")
        if k == 1:
            s, h = ch([(6, 4), (8, 3), (10, 12), (12, 8), (16, 6), (6, 4), (24, 5)])
            ts = int(math.hypot(s / 2, h))
            if ts * ts != (s // 2) ** 2 + h * h:
                return None
            v = s * s + 4 * (s * ts // 2)
            return MN("Limas persegi dengan sisi alas %d cm dan tinggi limas %d cm. Luas permukaannya …" % (s, h), v,
                      [s * s + 4 * (s * h // 2), 4 * (s * ts // 2), s * s * h // 3], "Tinggi sisi tegak = √(%d² + %d²) = %d cm. LP = %d + 4 × ½ × %d × %d = %s cm²." % (s // 2, h, ts, s * s, s, ts, num(v)), unit="cm²")
        s, ts = ri(4, 16), ri(5, 15)
        v = s * s + 2 * s * ts
        return MN("Limas persegi dengan sisi alas %d cm dan tinggi sisi tegak %d cm. Luas permukaannya …" % (s, ts), v, [s * s + s * ts, 2 * s * ts, s * s + 4 * s * ts], "LP = %d² + 4 × ½ × %d × %d = %s cm²." % (s, s, ts, num(v)), unit="cm²")

    def cerita():
        k = ri(0, 2)
        if k == 0:
            s, t = ri(3, 8) * 10, ri(3, 9) * 10
            v = s * s * t // 3
            return M("Atap rumah berbentuk limas persegi dengan sisi alas %d dm dan tinggi %d dm. Volume ruang di dalam atap …" % (s, t), "%s liter" % num(v),
                     ["%s liter" % num(s * s * t), "%s liter" % num(v // 10), "%s liter" % num(v * 10)], "⅓ × %d² × %d = %s dm³ = %s liter." % (s, t, num(v), num(v)))
        if k == 1:
            a, t, T = ri(2, 6) * 10, ri(2, 5) * 10, ri(3, 10) * 10
            v = a * t // 2 * T
            return M("Cokelat batangan berbentuk prisma segitiga: alas segitiga %d mm, tinggi segitiga %d mm, dan panjang %d mm. Volumenya …" % (a, t, T), "%s mm³" % num(v), ["%s mm³" % num(a * t * T), "%s mm³" % num(v // 3), "%s mm³" % num(v + a * t)],
                     "½ × %d × %d × %d = %s mm³." % (a, t, T, num(v)))
        s = ri(2, 6)
        t = ri(2, 6) * 3
        return M("Sebuah prisma dan sebuah limas memiliki alas dan tinggi yang sama. Jika volume prisma %d cm³, volume limas …" % (s * s * t), "%s cm³" % num(s * s * t // 3), ["%s cm³" % num(s * s * t), "%s cm³" % num(s * s * t * 3), "%s cm³" % num(s * s * t // 2 if s * s * t % 2 == 0 else s * s * t - 1)],
                 "Volume limas = ⅓ volume prisma: %s cm³." % num(s * s * t // 3))

    sets = [("Unsur prisma dan limas", [(unsur, 20)]),
            ("Volume prisma", [(v_prisma, 20)]),
            ("Volume limas", [(v_limas, 20)]),
            ("Luas permukaan", [(lp, 20)]),
            ("Soal cerita", [(cerita, 12), (v_limas, 4), (v_prisma, 4)])]
    return unit("prisma-dan-limas", "P", 9, "Prisma dan Limas: Luas Permukaan dan Volume", "Prisma dan Limas",
                "Peserta didik menjelaskan unsur-unsur prisma dan limas serta menghitung luas permukaan dan volumenya untuk menyelesaikan masalah.",
                "Latihan prisma dan limas kelas 8 SMP: banyak sisi, rusuk, dan titik sudut, volume prisma segitiga, volume limas, luas permukaan prisma dan limas, dan soal cerita. 100 soal dengan kunci jawaban.",
                "V limas = ⅓ × luas alas × tinggi", "V prisma = luas alas × tinggi.", sets,
                ["Prisma segi-n mempunyai n + 2 sisi, 3n rusuk, dan 2n titik sudut. Limas segi-n mempunyai n + 1 sisi, 2n rusuk, dan n + 1 titik sudut.",
                 "Volume prisma = luas alas × tinggi. Volume limas = ⅓ × luas alas × tinggi.",
                 "Luas permukaan prisma = 2 × luas alas + keliling alas × tinggi. Luas permukaan limas = luas alas + jumlah luas sisi tegak."],
                [("Limas persegi: sisi alas 6 cm, tinggi 10 cm. Volume?", ["⅓ × 36 × 10"], "120 cm³"),
                 ("Prisma segitiga: alas 4 cm, tinggi segitiga 3 cm, tinggi prisma 10 cm. Volume?", ["½ × 4 × 3 = 6", "6 × 10"], "60 cm³")],
                [["Volume limas = luas alas × tinggi", "Jangan lupa dikali ⅓"],
                 ["Tinggi limas dipakai untuk luas sisi tegak", "Pakai tinggi sisi tegak (apotema), bukan tinggi limas"],
                 ["Prisma segitiga punya 6 sisi", "Prisma segitiga punya 5 sisi: 2 alas dan 3 sisi tegak"]],
                [("Mengapa volume limas sepertiga volume prisma?", "Tiga limas dengan alas dan tinggi yang sama dapat mengisi penuh satu prisma."),
                 ("Apa itu tinggi sisi tegak?", "Tinggi segitiga sisi tegak limas, diukur dari alas segitiga ke puncak limas. Bisa dicari dengan teorema Pythagoras."),
                 ("Apakah kubus termasuk prisma?", "Ya. Kubus dan balok adalah prisma dengan alas persegi atau persegi panjang.")])


# ============================================================ 10. transformasi
def u10():
    def pt(x, y):
        return "(%s, %s)" % (sn(x), sn(y))

    def translasi():
        x, y, a, b = nz(-6, 6), nz(-6, 6), nz(-5, 5), nz(-5, 5)
        k = ri(0, 1)
        if k == 0:
            return M("Titik A%s ditranslasi oleh (%s, %s). Bayangannya …" % (pt(x, y), sn(a), sn(b)), "A'%s" % pt(x + a, y + b), ["A'%s" % pt(x - a, y - b), "A'%s" % pt(x + b, y + a), "A'%s" % pt(a, b)],
                     "(x + a, y + b) = (%s + %s, %s + %s) = %s." % (sn(x), par(a), sn(y), par(b), pt(x + a, y + b)))
        return M("Titik P%s ditranslasi menjadi P'%s. Translasinya …" % (pt(x, y), pt(x + a, y + b)), "(%s, %s)" % (sn(a), sn(b)), ["(%s, %s)" % (sn(-a), sn(-b)), "(%s, %s)" % (sn(b), sn(a)), "(%s, %s)" % (sn(x + a), sn(y + b))],
                 "a = %s − %s = %s dan b = %s − %s = %s." % (sn(x + a), par(x), sn(a), sn(y + b), par(y), sn(b)))

    R = {"sumbu x": lambda x, y: (x, -y), "sumbu y": lambda x, y: (-x, y), "titik asal O": lambda x, y: (-x, -y), "garis y = x": lambda x, y: (y, x), "garis y = −x": lambda x, y: (-y, -x)}

    def refleksi():
        x, y = nz(-7, 7), nz(-7, 7)
        if abs(x) == abs(y):
            return None
        m = ch(list(R))
        c = R[m](x, y)
        ws = [R[o](x, y) for o in R if o != m and R[o](x, y) != c]
        return M("Bayangan titik A%s oleh refleksi terhadap %s adalah …" % (pt(x, y), m), "A'%s" % pt(*c), ["A'%s" % pt(*w) for w in ws], "Refleksi terhadap %s: %s → %s." % (m, pt(x, y), pt(*c)))

    ROT = {"90° berlawanan arah jarum jam": lambda x, y: (-y, x), "90° searah jarum jam": lambda x, y: (y, -x), "180°": lambda x, y: (-x, -y)}

    def rotasi():
        x, y = nz(-7, 7), nz(-7, 7)
        if abs(x) == abs(y):
            return None
        m = ch(list(ROT))
        c = ROT[m](x, y)
        ws = [ROT[o](x, y) for o in ROT if o != m] + [(-x, y), (y, x)]
        return M("Bayangan titik B%s oleh rotasi %s dengan pusat O(0, 0) adalah …" % (pt(x, y), m), "B'%s" % pt(*c), ["B'%s" % pt(*w) for w in ws if w != c], "Rotasi %s: %s → %s." % (m, pt(x, y), pt(*c)))

    def gambar():
        pts = [(ri(1, 3), ri(1, 3))]
        pts.append((pts[0][0] + ri(1, 2), pts[0][1]))
        pts.append((pts[0][0], pts[0][1] + ri(1, 2)))
        k = ri(0, 2)
        if k == 0:
            f = lambda p: (-p[0], p[1])
            nm = "refleksi terhadap sumbu y"
        elif k == 1:
            f = lambda p: (p[0], -p[1])
            nm = "refleksi terhadap sumbu x"
        else:
            f = lambda p: (-p[0], -p[1])
            nm = "rotasi 180° dengan pusat O"
        img = [f(p) for p in pts]
        import id_smp as SS
        X = lambda x: 20 + (x + 5) * 24
        Y = lambda y: 20 + (5 - y) * 24
        s = []
        for i in range(-5, 6):
            s.append(line(X(i), Y(-5), X(i), Y(5), "#d5dfec", 1) + line(X(-5), Y(i), X(5), Y(i), "#d5dfec", 1))
        s.append(line(X(-5), Y(0), X(5), Y(0), INK, 2) + line(X(0), Y(-5), X(0), Y(5), INK, 2))
        s.append("<polygon points='%s' fill='#c7d9f7' stroke='%s' stroke-width='2'/>" % (" ".join("%d,%d" % (X(a), Y(b)) for a, b in pts), BLUE))
        s.append("<polygon points='%s' fill='#fbd3d3' stroke='%s' stroke-width='2'/>" % (" ".join("%d,%d" % (X(a), Y(b)) for a, b in img), RED))
        s.append(text(X(sum(p[0] for p in pts) / 3.0), Y(sum(p[1] for p in pts) / 3.0) + 5, "A", 13) + text(X(sum(p[0] for p in img) / 3.0), Y(sum(p[1] for p in img) / 3.0) + 5, "B", 13))
        pic = wrap(280, 280, "".join(s), "dua segitiga pada bidang koordinat")
        others = [o for o in ["refleksi terhadap sumbu y", "refleksi terhadap sumbu x", "rotasi 180° dengan pusat O", "translasi (2, 0)"] if o != nm]
        return M("Segitiga B adalah bayangan segitiga A oleh …" + pic, nm, others, "Bandingkan letak titik-titik sudutnya: %s." % nm) if True else None

    def sifat():
        F = [("translasi", "ukuran dan bentuknya tetap"), ("refleksi", "ukuran dan bentuknya tetap"), ("rotasi", "ukuran dan bentuknya tetap"),
             ("dilatasi dengan faktor skala 2", "bentuknya tetap tetapi ukurannya menjadi 2 kali")]
        t, c = ch(F)
        return M("Bangun yang ditransformasi dengan %s, …" % t, c, [o for o in ["ukuran dan bentuknya tetap", "bentuknya tetap tetapi ukurannya menjadi 2 kali", "bentuknya berubah", "ukurannya menjadi setengah"] if o != c],
                 "Translasi, refleksi, dan rotasi tidak mengubah ukuran; dilatasi mengubah ukuran tetapi tidak mengubah bentuk.")

    def dua():
        x, y, a, b = nz(-5, 5), nz(-5, 5), nz(-4, 4), nz(-4, 4)
        x1, y1 = x + a, y + b
        c = (x1, -y1)
        return M("Titik A%s ditranslasi oleh (%s, %s), lalu direfleksi terhadap sumbu x. Bayangan akhirnya …" % (pt(x, y), sn(a), sn(b)), "A''%s" % pt(*c),
                 ["A''%s" % pt(x1, y1), "A''%s" % pt(-x1, y1), "A''%s" % pt(x + a, -y + b)], "Translasi: %s. Refleksi sumbu x: %s." % (pt(x1, y1), pt(*c)))

    sets = [("Translasi", [(translasi, 20)]),
            ("Refleksi", [(refleksi, 20)]),
            ("Rotasi", [(rotasi, 20)]),
            ("Mengenali transformasi", [(gambar, 14), (sifat, 4), (dua, 2)]),
            ("Campuran", [(translasi, 5), (refleksi, 5), (rotasi, 5), (dua, 5)])]
    return unit("transformasi-geometri", "G", 10, "Transformasi Geometri: Translasi, Refleksi, dan Rotasi", "Transformasi Geometri",
                "Peserta didik melakukan dan menjelaskan transformasi tunggal (translasi, refleksi, rotasi) pada bidang koordinat Kartesius.",
                "Latihan transformasi geometri kelas 8 SMP: translasi, refleksi terhadap sumbu x, sumbu y, garis y = x, titik asal, rotasi 90° dan 180°, serta mengenali transformasi pada gambar. 100 soal dengan kunci jawaban.",
                "Refleksi sumbu x: (x, y) → (x, −y)", "Rotasi 90° berlawanan arah jarum jam: (x, y) → (−y, x).", sets,
                ["Translasi (a, b) menggeser setiap titik: (x, y) → (x + a, y + b).",
                 "Refleksi: terhadap sumbu x (x, y) → (x, −y), sumbu y (x, y) → (−x, y), titik asal (x, y) → (−x, −y), garis y = x (x, y) → (y, x).",
                 "Rotasi dengan pusat O: 90° berlawanan arah jarum jam (x, y) → (−y, x), 90° searah jarum jam (x, y) → (y, −x), 180° (x, y) → (−x, −y)."],
                [("A(3, −2) ditranslasi (−4, 5).", ["(3 − 4, −2 + 5)"], "A'(−1, 3)"),
                 ("B(2, 5) direfleksi terhadap sumbu y.", ["x berubah tanda"], "B'(−2, 5)")],
                [["Refleksi sumbu x mengubah tanda x", "Refleksi sumbu x mengubah tanda y"],
                 ["Rotasi 90°: (x, y) → (y, x)", "Rotasi 90° berlawanan arah jarum jam: (−y, x)"],
                 ["Translasi (2, 3) dari (1, 1) adalah (2, 3)", "Tambahkan: (1 + 2, 1 + 3) = (3, 4)"]],
                [("Apa itu transformasi isometri?", "Transformasi yang tidak mengubah ukuran dan bentuk bangun, yaitu translasi, refleksi, dan rotasi."),
                 ("Arah rotasi positif itu ke mana?", "Rotasi positif berlawanan arah jarum jam, rotasi negatif searah jarum jam."),
                 ("Bagaimana mengecek refleksi pada gambar?", "Jarak setiap titik ke cermin sama dengan jarak bayangannya ke cermin.")])


# ============================================================ 11. statistika
def u11():
    def data(n=None, lo=50, hi=95):
        n = n or ri(5, 9)
        return [ri(lo, hi) for _ in range(n)]

    def ds(xs):
        return "; ".join(num(x) for x in xs)

    def mean():
        while True:
            xs = data(ri(5, 8), 3, 30)
            if sum(xs) % len(xs) == 0:
                break
        v = sum(xs) // len(xs)
        return MN("Rata-rata (mean) dari data %s adalah …" % ds(xs), v, [sorted(xs)[len(xs) // 2], sum(xs) // (len(xs) - 1) if sum(xs) % (len(xs) - 1) == 0 else v + 1, max(xs) - min(xs)],
                  "Jumlah %d dibagi banyak data %d: %d." % (sum(xs), len(xs), v))

    def median():
        xs = data(ri(5, 10), 1, 40)
        s = sorted(xs)
        n = len(s)
        v = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
        ws = [Fr(xs[n // 2]) if n % 2 else Fr(xs[n // 2 - 1] + xs[n // 2], 2), Fr(sum(xs), n), Fr(s[n // 2 + 1]) if n % 2 else Fr(s[n // 2])]
        return MD("Median dari data %s adalah …" % ds(xs), v, ws + [v + 1], "Urutkan: %s. %s." % (ds(s), "Data tengah ke-%d adalah %s" % (n // 2 + 1, dz(v)) if n % 2 else "Rata-rata data ke-%d dan ke-%d: %s" % (n // 2, n // 2 + 1, dz(v))))

    def modus():
        base = sh(range(1, 15))[:5]
        m = base[0]
        xs = sh(base + [m, m] + [base[1]])
        return MN("Modus dari data %s adalah …" % ds(xs), m, [base[1], max(xs), sorted(xs)[len(xs) // 2] if sorted(xs)[len(xs) // 2] != m else min(xs)], "%d muncul paling sering (3 kali)." % m)

    def jangkauan():
        xs = data(ri(6, 10), 5, 60)
        v = max(xs) - min(xs)
        return MN("Jangkauan dari data %s adalah …" % ds(xs), v, [max(xs), max(xs) - sorted(xs)[1], sorted(xs)[-2] - min(xs), v + 1], "Jangkauan = terbesar − terkecil = %d − %d = %d." % (max(xs), min(xs), v))

    def tabel():
        vals = sorted(sh(range(5, 11))[:4])
        fs = [ri(1, 8) for _ in vals]
        n = sum(fs)
        tot = sum(v * f for v, f in zip(vals, fs))
        t = "<table class='sn-table'><tbody><tr><td>Nilai</td>%s</tr><tr><td>Frekuensi</td>%s</tr></tbody></table>" % ("".join("<td>%d</td>" % v for v in vals), "".join("<td>%d</td>" % f for f in fs))
        k = ri(0, 2)
        if k == 0:
            m = Fr(tot, n)
            if not S.endlich(m) or len(dz(m)) > 5:
                return None
            return MD("Rata-rata nilai pada tabel berikut adalah …" + t, m, [Fr(sum(vals), len(vals)), Fr(tot, len(vals)), m + 1], "Σ(nilai × frekuensi) = %d, Σf = %d. Rata-rata = %d : %d = %s." % (tot, n, tot, n, dz(m)))
        if k == 1:
            if fs.count(max(fs)) > 1:
                return None
            v = vals[fs.index(max(fs))]
            return MN("Modus data pada tabel berikut adalah …" + t, v, [max(fs), vals[-1], vals[0] if vals[0] != v else vals[1]], "Frekuensi terbesar %d dimiliki nilai %d." % (max(fs), v))
        s = sorted([v for v, f in zip(vals, fs) for _ in range(f)])
        md = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
        return MD("Median data pada tabel berikut adalah …" + t, md, [Fr(vals[1] + vals[2], 2), md + 1, Fr(tot, n) if Fr(tot, n) != md and S.endlich(Fr(tot, n)) else md - 1], "Ada %d data. Median adalah data ke-%s: %s." % (n, num(n // 2 + 1) if n % 2 else "%d dan ke-%d" % (n // 2, n // 2 + 1), dz(md)))

    def ubah():
        k = ri(0, 2)
        n = ri(5, 12)
        m = ri(60, 85)
        if k == 0:
            x = ri(50, 98)
            v = Fr(n * m + x, n + 1)
            if not S.endlich(v) or len(dz(v)) > 5:
                return None
            return MD("Rata-rata nilai %d siswa adalah %d. Seorang siswa baru dengan nilai %d bergabung. Rata-rata sekarang …" % (n, m, x), v, [Fr(m + x, 2), Fr(n * m + x, n), v + 1], "(%d × %d + %d) : %d = %s." % (n, m, x, n + 1, dz(v)))
        if k == 1:
            x = ri(50, 98)
            tot = n * m
            m2 = Fr(tot + x, n + 1)
            if m2.denominator != 1:
                return None
            return MN("Rata-rata %d data adalah %d. Setelah ditambah satu data, rata-ratanya menjadi %s. Data yang ditambahkan …" % (n, m, sn(m2)), x, [int(m2), x + n, (n + 1) * int(m2) - tot + 1], "(%d + 1) × %s − %d × %d = %d." % (n, sn(m2), n, m, x))
        a = [ri(60, 95) for _ in range(4)]
        t = ri(70, 85)
        x = 5 * t - sum(a)
        if not 40 <= x <= 100:
            return None
        return MN("Nilai empat ulangan Sari: %s. Agar rata-rata lima ulangan %d, nilai ulangan kelima harus …" % (ds(a), t), x, [t, x + 5, 4 * t - sum(a) if 4 * t - sum(a) > 0 else x - 4], "5 × %d − %d = %d." % (t, sum(a), x))

    sets = [("Rata-rata (mean)", [(mean, 20)]),
            ("Median", [(median, 20)]),
            ("Modus dan jangkauan", [(modus, 10), (jangkauan, 10)]),
            ("Data dalam tabel frekuensi", [(tabel, 20)]),
            ("Perubahan rata-rata", [(ubah, 20)])]
    return unit("statistika", "D", 11, "Statistika: Mean, Median, Modus, dan Jangkauan", "Statistika",
                "Peserta didik menentukan dan menafsirkan ukuran pemusatan (mean, median, modus) dan ukuran penyebaran (jangkauan) dari data tunggal dan tabel frekuensi.",
                "Latihan statistika kelas 8 SMP: rata-rata (mean), median, modus, jangkauan, data dalam tabel frekuensi, rata-rata gabungan, dan mencari data yang hilang. 100 soal dengan kunci jawaban.",
                "Median: urutkan dulu, ambil tengahnya", "Mean = jumlah data : banyak data.", sets,
                ["Rata-rata (mean) = jumlah semua data : banyak data. Modus adalah data yang paling sering muncul.",
                 "Median adalah nilai tengah setelah data diurutkan. Jika banyak data genap, median = rata-rata dua data tengah.",
                 "Jangkauan = data terbesar − data terkecil. Pada tabel frekuensi, jumlah data = Σ(nilai × frekuensi)."],
                [("Data: 7; 3; 9; 5; 6. Median?", ["Urutkan: 3; 5; 6; 7; 9"], "6"),
                 ("Rata-rata 4 data adalah 8. Data kelima 13. Rata-rata baru?", ["(32 + 13) : 5"], "9")],
                [["Median diambil tanpa mengurutkan data", "Urutkan dulu dari terkecil"],
                 ["Modus dijawab frekuensinya", "Modus adalah nilainya, bukan frekuensinya"],
                 ["Rata-rata tabel = jumlah nilai : banyak nilai", "Kalikan setiap nilai dengan frekuensinya"]],
                [("Kapan median lebih tepat daripada mean?", "Saat ada data yang sangat besar atau sangat kecil (pencilan), median lebih menggambarkan data pada umumnya."),
                 ("Bisakah data tidak punya modus?", "Bisa, jika semua data muncul sama banyak."),
                 ("Apa kegunaan jangkauan?", "Jangkauan menunjukkan seberapa jauh data menyebar dari yang terkecil sampai yang terbesar.")])


# ============================================================ 12. peluang empirik dan teoretik
def u12():
    def relatif():
        n = ch([20, 25, 40, 50, 60, 80, 100, 120, 200])
        while True:
            a = ri(n // 6, n * 2 // 3)
            if Fr(a, n).denominator <= 25:
                break
        it = ch([("sebuah koin dilempar", "muncul gambar"), ("sebuah dadu dilempar", "muncul mata dadu 6"), ("paku payung dijatuhkan", "jatuh dengan ujung ke atas"),
                 ("tutup botol dilempar", "jatuh terbuka"), ("sebuah dadu dilempar", "muncul mata dadu genap")])
        v = Fr(a, n)
        return M("Dalam percobaan, %s sebanyak %d kali. Hasilnya, %s sebanyak %d kali. Frekuensi relatif kejadian itu …" % (it[0], n, it[1], a), fq(v), [fq(Fr(n - a, n)), fq(Fr(a, n - a)) if n != 2 * a else fq(Fr(1, 3)), fq(Fr(1, 2)) if v != Fr(1, 2) else fq(Fr(1, 3))],
                 "Frekuensi relatif = banyak kejadian : banyak percobaan = %s." % (("%d/%d = %s" % (a, n, fq(v))) if v.numerator != a else fq(v)))

    def bandingkan():
        n = ch([60, 120, 180, 300, 600])
        kind = ch([("mata dadu 3", Fr(1, 6)), ("mata dadu genap", Fr(1, 2)), ("mata dadu lebih dari 4", Fr(1, 3)), ("bilangan prima", Fr(1, 2))])
        t = kind[1] * n
        obs = int(t) + ri(-8, 8)
        if obs == t:
            return None
        k = ri(0, 1)
        if k == 0:
            return M("Dadu dilempar %d kali dan %s muncul %d kali. Peluang teoretik muncul %s adalah …" % (n, kind[0], obs, kind[0]), fq(kind[1]), [fq(Fr(obs, n)), fq(1 - kind[1]), fq(Fr(obs, n - obs))],
                     "Peluang teoretik tidak bergantung pada hasil percobaan: %s." % fq(kind[1]))
        return M("Dadu dilempar %d kali dan %s muncul %d kali. Selisih frekuensi muncul dengan frekuensi harapannya …" % (n, kind[0], obs), "%d kali" % abs(obs - int(t)),
                 ["%d kali" % obs, "%d kali" % int(t), "%d kali" % (abs(obs - int(t)) + 10)], "Frekuensi harapan = %s × %d = %d. Selisih |%d − %d| = %d kali." % (fq(kind[1]), n, int(t), obs, int(t), abs(obs - int(t))))

    def perkiraan():
        n0 = ch([20, 25, 40, 50, 100])
        a = ri(1, n0 // 2)
        N = n0 * ri(2, 20)
        k = ri(0, 1)
        it = ch([("lampu", "rusak"), ("telur", "retak"), ("baut", "cacat"), ("mangga", "busuk")])
        if k == 0:
            return MN("Dari %d %s yang diperiksa, %d %s. Dari %s %s, perkiraan banyak yang %s …" % (n0, it[0], a, it[1], num(N), it[0], it[1]), N * a // n0, [a * N // 100 if a * N % 100 == 0 and a * N // 100 != N * a // n0 else N * a // n0 + a, N - N * a // n0, a * n0],
                      "%d/%d × %s = %s." % (a, n0, num(N), num(N * a // n0)), unit=it[0])
        p = ch([Fr(1, 4), Fr(1, 5), Fr(2, 5), Fr(3, 10), Fr(3, 4)])
        N = p.denominator * ri(2, 8)
        return MN("Peluang seorang pemain mencetak gol dari tendangan penalti adalah %s. Jika ia menendang %d kali, perkiraan banyak gol …" % (fq(p), N), p * N, [(1 - p) * N, N // 2 if N % 2 == 0 and p != Fr(1, 2) else p * N + 1, p * N + p.denominator], "%s × %d = %d gol." % (fq(p), N, p * N), unit="gol")

    def tabel():
        n = 6
        tot = ch([60, 120, 90, 150])
        fs = [ri(tot // 10, tot // 4) for _ in range(5)]
        last = tot - sum(fs)
        if last < 1:
            return None
        fs.append(last)
        i = ri(0, 5)
        t = "<table class='sn-table'><tbody><tr><td>Mata dadu</td>%s</tr><tr><td>Frekuensi</td>%s</tr></tbody></table>" % ("".join("<td>%d</td>" % (j + 1) for j in range(6)), "".join("<td>%d</td>" % f for f in fs))
        k = ri(0, 1)
        if k == 0:
            v = Fr(fs[i], tot)
            return M("Hasil pelemparan dadu %d kali tercatat pada tabel. Frekuensi relatif muncul mata dadu %d adalah …" % (tot, i + 1) + t, fq(v), [fq(Fr(1, 6)) if v != Fr(1, 6) else fq(Fr(1, 5)), fq(Fr(fs[i], tot - fs[i])), fq(Fr(tot - fs[i], tot))],
                     "%s." % (("%d/%d = %s" % (fs[i], tot, fq(v))) if v.numerator != fs[i] else fq(v)))
        e = fs[1] + fs[3] + fs[5]
        v = Fr(e, tot)
        return M("Hasil pelemparan dadu %d kali tercatat pada tabel. Frekuensi relatif muncul mata dadu genap adalah …" % tot + t, fq(v), [fq(Fr(1, 2)) if v != Fr(1, 2) else fq(Fr(2, 5)), fq(Fr(tot - e, tot)), fq(Fr(e, tot - e))],
                 "Genap: %d + %d + %d = %d. P = %s." % (fs[1], fs[3], fs[5], e, ("%d/%d = %s" % (e, tot, fq(v))) if v.numerator != e else fq(v)))

    def konsep():
        F = [("Makin banyak percobaan dilakukan, frekuensi relatif …", "makin mendekati peluang teoretik", ["makin jauh dari peluang teoretik", "selalu sama dengan 0", "selalu lebih dari 1"]),
             ("Nilai frekuensi relatif selalu …", "di antara 0 dan 1", ["lebih dari 1", "kurang dari 0", "sama dengan 1/2"]),
             ("Peluang empirik diperoleh dari …", "hasil percobaan", ["rumus n(A)/n(S) saja", "menebak", "banyak anggota ruang sampel saja"]),
             ("Peluang teoretik diperoleh dari …", "perbandingan banyak hasil yang diharapkan dengan banyak semua hasil yang mungkin", ["hasil percobaan", "banyak percobaan", "frekuensi harapan"]),
             ("Jika peluang suatu kejadian 0,2, peluang kejadian itu tidak terjadi adalah …", "0,8", ["0,2", "1,2", "0"]),
             ("Jika frekuensi relatif suatu kejadian 3/10 dari 50 percobaan, kejadian itu muncul …", "15 kali", ["3 kali", "30 kali", "10 kali"]),
             ("Koin dilempar 10 kali dan muncul gambar 7 kali. Pernyataan yang benar adalah …", "koin itu belum tentu tidak seimbang, karena percobaannya sedikit", ["peluang teoretik gambar adalah 7/10", "koin pasti tidak seimbang", "peluang angka adalah 7/10"])]
        q, c, ws = ch(F)
        return M(q, c, ws, "%s." % c[0].upper() + c[1:] if False else "Jawabannya: %s." % c)

    sets = [("Frekuensi relatif", [(relatif, 20)]),
            ("Tabel hasil percobaan", [(tabel, 20)]),
            ("Peluang empirik dan teoretik", [(bandingkan, 14), (konsep, 6)]),
            ("Memperkirakan dengan peluang", [(perkiraan, 20)]),
            ("Campuran", [(relatif, 7), (tabel, 7), (bandingkan, 6)])]
    return unit("peluang-empirik-dan-teoretik", "D", 12, "Peluang Empirik dan Peluang Teoretik", "Peluang Empirik dan Teoretik",
                "Peserta didik menjelaskan dan menggunakan frekuensi relatif (peluang empirik) dari percobaan, membandingkannya dengan peluang teoretik, dan membuat perkiraan.",
                "Latihan peluang empirik dan teoretik kelas 8 SMP: frekuensi relatif, tabel hasil percobaan dadu, membandingkan peluang empirik dan teoretik, frekuensi harapan, dan perkiraan. 100 soal dengan kunci jawaban.",
                "Frekuensi relatif = kejadian : percobaan", "Makin banyak percobaan, makin dekat ke peluang teoretik.", sets,
                ["Peluang empirik (frekuensi relatif) dihitung dari percobaan: banyak kejadian muncul : banyak percobaan.",
                 "Peluang teoretik dihitung dari ruang sampel: n(A) : n(S). Pada dadu seimbang, peluang setiap mata dadu 1/6.",
                 "Jika percobaan diulang sangat banyak, frekuensi relatif mendekati peluang teoretik. Peluang juga dipakai untuk memperkirakan: banyak kejadian ≈ peluang × banyak percobaan."],
                [("Koin dilempar 50 kali, gambar 28 kali. Frekuensi relatif gambar?", ["28/50"], "14/25"),
                 ("Dari 40 lampu, 2 rusak. Dari 1.000 lampu, perkiraan yang rusak?", ["2/40 × 1.000"], "50 lampu")],
                [["Frekuensi relatif dihitung kejadian : kejadian lain", "Bagi dengan banyak seluruh percobaan"],
                 ["Peluang teoretik diubah oleh hasil percobaan", "Peluang teoretik tetap, yang berubah frekuensi relatif"],
                 ["Frekuensi relatif bisa lebih dari 1", "Frekuensi relatif selalu antara 0 dan 1"]],
                [("Apa beda peluang empirik dan teoretik?", "Peluang empirik diperoleh dari percobaan nyata. Peluang teoretik dihitung dari semua hasil yang mungkin."),
                 ("Mengapa hasil percobaan tidak selalu sama dengan peluang teoretik?", "Karena hasil acak bervariasi. Perbedaan itu makin kecil jika percobaannya makin banyak."),
                 ("Untuk apa peluang empirik dipakai?", "Untuk kejadian yang peluang teoretiknya sulit dihitung, misalnya peluang paku payung jatuh dengan ujung ke atas.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12]
