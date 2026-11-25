# -*- coding: utf-8 -*-
"""Indonesia / Matematika / Kelas 12 (SMA, Fase F)。python3 tools/id_smp.py 12 [番号…]"""
import math
from fractions import Fraction as Fr
import id_smp as S
from id_smp import (ri, ch, nz, sh, num, sn, par, dz, fq, expr, lin, sup, M, MN, MD, MINUS, NB,
                    kosy, kurve, tab, unit, wrap, text, line, INK, BLUE, RED, FILL, GREEN)
from id_sma10 import surd


def X(e, v="x"):
    return "" if e == 0 else (v if e == 1 else v + sup(e))


def up(n):
    return "" if n == 1 else sup(n)


def P(cs, v="x"):
    """{pangkat: koefisien} → string"""
    ks = sorted((k for k in cs if cs[k] != 0), reverse=True)
    if not ks:
        return "0"
    return expr([(cs[k], X(k, v)) for k in ks])


def rnd_poly(deg, lo=-6, hi=6):
    cs = {deg: nz(-4, 4)}
    for k in range(deg - 1, -1, -1):
        cs[k] = ri(lo, hi)
    return cs


def deriv(cs):
    return {k - 1: c * k for k, c in cs.items() if k > 0}


def ev(cs, x):
    return sum(Fr(c) * Fr(x) ** k for k, c in cs.items())


def integ(cs):
    return {k + 1: Fr(c, k + 1) for k, c in cs.items()}


def fact(n):
    return math.factorial(n)


def nPr(n, r):
    return fact(n) // fact(n - r)


def nCr(n, r):
    return math.comb(n, r)


# ============================================================ 1. kaidah pencacahan
def u1():
    def kali():
        F = [("baju", "celana", "sepatu"), ("jenis nasi", "lauk", "minuman"), ("rute dari Bandung ke Jakarta", "rute dari Jakarta ke Semarang", None),
             ("warna cat", "jenis kuas", None), ("pilihan topi", "pilihan kaus", "pilihan tas")]
        it = ch(F)
        ns = [ri(2, 6) for _ in it if _]
        names = [x for x in it if x]
        v = 1
        for n in ns:
            v *= n
        q = "Tersedia " + ", ".join("%d %s" % (n, w) for n, w in zip(ns, names)) + ". Banyak pasangan berbeda yang dapat dipilih (satu dari masing-masing) adalah …"
        return MN(q, v, [sum(ns), v * 2, v - 1 if v > 2 else v + 3], "Aturan perkalian: %s = %d." % (" × ".join(str(n) for n in ns), v))

    def angka():
        ds = sorted(sh(range(0, 10))[:ri(4, 7)])
        n = len(ds)
        L = ri(2, 3)
        zero = 0 in ds
        k = ri(0, 2)
        digs = ", ".join(str(d) for d in ds)
        if k == 0:
            v = (n - 1) * nPr(n - 1, L - 1) if zero else nPr(n, L)
            return MN("Dari angka %s akan dibuat bilangan %d angka berbeda. Banyak bilangan yang dapat dibuat adalah …" % (digs, L), v, [nPr(n, L) if zero else nPr(n, L) // 2 or 1, n ** L, v + n], "%s" % ("Angka pertama tidak boleh 0: %d pilihan, lalu %s." % (n - 1, " × ".join(str(n - 1 - i) for i in range(L - 1))) if zero else "Pilihan tiap tempat: %s = %d." % (" × ".join(str(n - i) for i in range(L)), v)))
        if k == 1:
            v = (n - 1) * n ** (L - 1) if zero else n ** L
            return MN("Dari angka %s akan dibuat bilangan %d angka dan angka boleh berulang. Banyak bilangan yang dapat dibuat adalah …" % (digs, L), v, [nPr(n, L), n ** L if zero else n ** (L - 1), n * L], "Setiap tempat boleh memakai angka yang sama%s: %d." % (", kecuali angka pertama tidak boleh 0" if zero else "", v))
        if zero:
            return None
        odd = [d for d in ds if d % 2]
        if not odd:
            return None
        v = len(odd) * nPr(n - 1, L - 1)
        return MN("Dari angka %s akan dibuat bilangan ganjil %d angka berbeda. Banyak bilangan yang dapat dibuat adalah …" % (digs, L), v, [nPr(n, L), len(odd) * n ** (L - 1), v // 2 or v + 1], "Satuan harus ganjil: %d pilihan, lalu tempat lain %s. Hasilnya %d." % (len(odd), " × ".join(str(n - 1 - i) for i in range(L - 1)), v))

    def faktorial():
        k = ri(0, 2)
        if k == 0:
            n = ri(3, 10)
            return MN("Nilai %d! adalah …" % n, fact(n), [n * (n - 1), fact(n - 1), fact(n) // 2], "%d! = %s = %s." % (n, " × ".join(str(i) for i in range(n, 0, -1)), num(fact(n))))
        if k == 1:
            n = ri(6, 15)
            r = ri(2, 3)
            v = fact(n) // fact(n - r)
            return MN("Nilai %d! : %d! adalah …" % (n, n - r), v, [fact(r) if fact(r) != v else v + 1, n - (n - r), v // fact(r) if v // fact(r) != v else v * 2], "%d!/%d! = %s = %s." % (n, n - r, " × ".join(str(n - i) for i in range(r)), num(v)))
        n = ri(5, 16)
        v = fact(n) // (fact(2) * fact(n - 2))
        return MN("Nilai %d! : (2! × %d!) adalah …" % (n, n - 2), v, [v * 2, n * (n - 1) * (n - 2), n], "%d × %d : 2 = %d." % (n, n - 1, v))

    def jalan():
        a, b, c = ri(2, 5), ri(2, 5), ri(2, 4)
        k = ri(0, 1)
        if k == 0:
            v = a * b
            return MN("Dari kota A ke kota B ada %d jalan dan dari B ke C ada %d jalan. Banyak cara pergi dari A ke C melalui B adalah …" % (a, b), v, [a + b, v * 2, v - 1], "%d × %d = %d." % (a, b, v))
        v = a * b * b * a
        return MN("Dari kota A ke B ada %d jalan dan dari B ke C ada %d jalan. Banyak cara pergi A → C lalu pulang C → A melalui B adalah …" % (a, b), v, [a * b, 2 * a * b, a * b * (a - 1) * (b - 1) if a * b * (a - 1) * (b - 1) != v else v + 1], "Pergi %d × %d, pulang %d × %d: %d." % (a, b, b, a, v))

    sets = [("Aturan perkalian", [(kali, 12), (jalan, 8)]),
            ("Notasi faktorial", [(faktorial, 20)]),
            ("Menyusun bilangan dengan angka berbeda", [(angka, 20)]),
            ("Rute dan pilihan", [(jalan, 10), (kali, 10)]),
            ("Campuran", [(angka, 10), (faktorial, 5), (kali, 5)])]
    return unit("kaidah-pencacahan", "D", 1, "Kaidah Pencacahan: Aturan Perkalian dan Faktorial", "Kaidah Pencacahan",
                "Peserta didik menggunakan aturan penjumlahan, aturan perkalian, dan notasi faktorial untuk menentukan banyak kemungkinan suatu kejadian.",
                "Latihan kaidah pencacahan kelas 12 SMA: aturan perkalian (filling slots), menyusun bilangan dari angka-angka, rute perjalanan, dan notasi faktorial. 100 soal dengan kunci jawaban.",
                "Tahap berurutan: pilihan dikalikan", "n! = n × (n − 1) × … × 1", sets,
                ["Jika tahap pertama dapat dilakukan dengan a cara dan tahap kedua dengan b cara, keseluruhannya dapat dilakukan dengan a × b cara (aturan perkalian).",
                 "Saat menyusun bilangan, isi dulu tempat yang mempunyai syarat (angka pertama bukan 0, angka terakhir ganjil), lalu tempat lainnya.",
                 "Faktorial n! = n × (n − 1) × … × 2 × 1, dengan 0! = 1. Pembagian faktorial dapat disederhanakan: 7!/5! = 7 × 6."],
                [("3 baju, 4 celana. Banyak pasangan?", ["3 × 4"], "12"),
                 ("Angka 1, 2, 3, 4, 5. Bilangan 3 angka berbeda?", ["5 × 4 × 3"], "60")],
                [["Menjumlahkan pilihan tiap tahap", "Tahap berurutan dikalikan"],
                 ["Angka 0 boleh di depan", "Bilangan tidak diawali 0"],
                 ["7!/5! = 2!", "7!/5! = 7 × 6 = 42"]],
                [("Kapan memakai aturan penjumlahan?", "Jika hanya satu dari beberapa pilihan yang dilakukan, misalnya naik bus atau kereta. Banyak caranya dijumlahkan."),
                 ("Mengapa 0! = 1?", "Agar rumus n! = n × (n − 1)! tetap berlaku untuk n = 1, dan ada tepat satu cara menyusun nol benda."),
                 ("Apa itu filling slots?", "Cara menghitung dengan membuat kotak untuk setiap tempat, menulis banyak pilihannya, lalu mengalikan.")])


# ============================================================ 2. permutasi dan kombinasi
def u2():
    def notasi():
        n = ri(4, 10)
        r = ri(2, min(4, n - 1))
        k = ri(0, 1)
        if k == 0:
            v = nPr(n, r)
            return MN("Nilai P(%d, %d) adalah …" % (n, r), v, [nCr(n, r), n ** r if n ** r != v else v + 1, n * r], "P(n, r) = n!/(n − r)! = %s = %s." % (" × ".join(str(n - i) for i in range(r)), num(v)))
        v = nCr(n, r)
        return MN("Nilai C(%d, %d) adalah …" % (n, r), v, [nPr(n, r), v * 2, n * r if n * r != v else v + 1], "C(n, r) = n!/(r!(n − r)!) = %s/%d = %s." % (num(nPr(n, r)), fact(r), num(v)))

    def perm():
        F = [("ketua, sekretaris, dan bendahara", 3), ("juara 1, 2, dan 3", 3), ("ketua dan wakil ketua", 2), ("ketua, wakil, sekretaris, dan bendahara", 4)]
        w, r = ch(F)
        n = ri(r + 2, 12)
        v = nPr(n, r)
        return MN("Dari %d siswa akan dipilih %s. Banyak susunan yang mungkin adalah …" % (n, w), v, [nCr(n, r), n * r, fact(n) // fact(r) if fact(n) // fact(r) != v else v + 1], "Urutan (jabatan) diperhatikan: P(%d, %d) = %s." % (n, r, num(v)))

    def komb():
        F = [("perwakilan", "siswa"), ("anggota tim", "pemain"), ("buah", "jenis buah"), ("soal yang dikerjakan", "soal")]
        w, u = ch(F)
        n = ri(5, 12)
        r = ri(2, min(5, n - 2))
        k = ri(0, 1)
        if k == 0:
            v = nCr(n, r)
            return MN("Dari %d %s akan dipilih %d %s. Banyak cara memilih adalah …" % (n, u, r, w), v, [nPr(n, r), n * r, nCr(n, r - 1) if nCr(n, r - 1) != v else v + 1], "Urutan tidak diperhatikan: C(%d, %d) = %s." % (n, r, num(v)))
        n = ri(5, 12)
        v = nCr(n, 2)
        return MN("Dalam sebuah pertemuan, %d orang saling berjabat tangan tepat sekali. Banyak jabat tangan adalah …" % n, v, [n * (n - 1), n * 2, nCr(n, 3)], "C(%d, 2) = %d × %d : 2 = %d." % (n, n, n - 1, v))

    def khusus():
        k = ri(0, 2)
        if k == 0:
            W = [("MATEMATIKA", None), ("KATAK", None), ("BANANA", None), ("SAMASAMA", None), ("ANAKANAK", None), ("KAKAK", None), ("APAPUN", None), ("BOBOK", None), ("PAPAYA", None), ("JAJAN", None)]
            w = ch(W)[0]
            from collections import Counter
            cnt = Counter(w)
            v = fact(len(w))
            for c in cnt.values():
                v //= fact(c)
            return MN("Banyak susunan huruf berbeda dari kata %s adalah …" % w, v, [fact(len(w)), v * 2, nPr(len(w), len(cnt)) if nPr(len(w), len(cnt)) != v else v + 1],
                      "Ada huruf yang sama: %d!/(%s) = %s." % (len(w), " × ".join("%d!" % c for c in cnt.values() if c > 1), num(v)))
        if k == 1:
            n = ri(4, 9)
            v = fact(n - 1)
            return MN("%d orang duduk mengelilingi meja bundar. Banyak susunan duduk yang berbeda adalah …" % n, v, [fact(n), n * (n - 1), fact(n - 2)], "Permutasi siklis: (%d − 1)! = %d! = %s." % (n, n - 1, num(v)))
        a, b = ri(4, 8), ri(3, 7)
        ra, rb = ri(1, 3), ri(1, 3)
        v = nCr(a, ra) * nCr(b, rb)
        return MN("Dari %d siswa laki-laki dan %d siswa perempuan akan dipilih %d laki-laki dan %d perempuan. Banyak cara memilih adalah …" % (a, b, ra, rb), v, [nCr(a + b, ra + rb), nCr(a, ra) + nCr(b, rb), nPr(a, ra) * nPr(b, rb) if nPr(a, ra) * nPr(b, rb) != v else v + 1],
                  "C(%d, %d) × C(%d, %d) = %d × %d = %s." % (a, ra, b, rb, nCr(a, ra), nCr(b, rb), num(v)))

    def peluang():
        a, b = ri(3, 7), ri(3, 7)
        r = 2
        tot = nCr(a + b, r)
        k = ri(0, 1)
        if k == 0:
            v = Fr(nCr(a, 2), tot)
            return M("Kantong berisi %d bola merah dan %d bola biru. Diambil 2 bola sekaligus. Peluang keduanya merah adalah …" % (a, b), fq(v), [fq(x) for x in (Fr(a, a + b) ** 2, Fr(a, a + b), Fr(nCr(b, 2), tot), Fr(a * b, tot))],
                     "C(%d, 2)/C(%d, 2) = %d/%d = %s." % (a, a + b, nCr(a, 2), tot, fq(v)))
        v = Fr(a * b, tot)
        return M("Kantong berisi %d bola merah dan %d bola biru. Diambil 2 bola sekaligus. Peluang terambil 1 merah dan 1 biru adalah …" % (a, b), fq(v), [fq(x) for x in (Fr(a * b, (a + b) ** 2), Fr(1, 2), Fr(nCr(a, 2), tot), Fr(a + b, tot))],
                 "C(%d, 1) × C(%d, 1)/C(%d, 2) = %d/%d = %s." % (a, b, a + b, a * b, tot, fq(v)))

    sets = [("Notasi permutasi dan kombinasi", [(notasi, 20)]),
            ("Permutasi: urutan diperhatikan", [(perm, 20)]),
            ("Kombinasi: urutan tidak diperhatikan", [(komb, 20)]),
            ("Permutasi unsur sama, siklis, dan kombinasi bertingkat", [(khusus, 20)]),
            ("Peluang dengan kombinasi", [(peluang, 14), (perm, 3), (komb, 3)])]
    return unit("permutasi-dan-kombinasi", "D", 2, "Permutasi dan Kombinasi", "Permutasi dan Kombinasi",
                "Peserta didik membedakan permutasi dan kombinasi, menghitung permutasi unsur yang sama dan permutasi siklis, serta menggunakan kombinasi untuk menentukan peluang.",
                "Latihan permutasi dan kombinasi kelas 12 SMA: notasi P(n, r) dan C(n, r), memilih pengurus, memilih tim, jabat tangan, permutasi huruf yang sama, permutasi siklis, dan peluang dengan kombinasi. 100 soal dengan kunci jawaban.",
                "Urutan penting: permutasi", "Urutan tidak penting: kombinasi. C(n, r) = P(n, r) : r!", sets,
                ["Permutasi P(n, r) = n!/(n − r)! menghitung susunan r unsur dari n unsur dengan memperhatikan urutan, misalnya ketua dan wakil.",
                 "Kombinasi C(n, r) = n!/(r!(n − r)!) menghitung pilihan r unsur tanpa memperhatikan urutan, misalnya memilih anggota tim.",
                 "Permutasi n unsur dengan unsur yang sama: n!/(k₁! k₂! …). Permutasi siklis n unsur: (n − 1)!."],
                [("Dari 8 siswa dipilih ketua dan wakil.", ["P(8, 2) = 8 × 7"], "56"),
                 ("Dari 8 siswa dipilih 2 perwakilan.", ["C(8, 2) = 56 : 2"], "28")],
                [["Memilih tim memakai permutasi", "Anggota tim tanpa jabatan: kombinasi"],
                 ["Meja bundar dihitung n!", "Permutasi siklis (n − 1)!"],
                 ["Huruf yang sama dihitung berbeda", "Bagi dengan faktorial banyak huruf yang sama"]],
                [("Bagaimana membedakan permutasi dan kombinasi?", "Tukar urutan dua unsur. Jika hasilnya dianggap berbeda (misalnya ketua dan wakil bertukar), itu permutasi. Jika sama, itu kombinasi."),
                 ("Mengapa C(n, r) = C(n, n − r)?", "Memilih r unsur sama saja dengan memilih n − r unsur yang tidak diambil."),
                 ("Apa hubungan kombinasi dan segitiga Pascal?", "Bilangan pada baris ke-n segitiga Pascal adalah C(n, 0), C(n, 1), …, C(n, n).")])


# ============================================================ 3. limit
def u3():
    def subst():
        cs = rnd_poly(ri(1, 2))
        a = ri(-4, 4)
        v = ev(cs, a)
        return MN("Nilai lim<sub>x→%s</sub> (%s) adalah …" % (sn(a), P(cs)), v, [ev(cs, -a) if ev(cs, -a) != v else v + 2, ev(cs, a + 1), cs.get(0, 0) if cs.get(0, 0) != v else v - 1], "Substitusi langsung x = %s: %s." % (sn(a), sn(v)))

    def faktor():
        a = nz(-6, 6)
        b = nz(-8, 8)
        if b == -a:
            return None
        # (x − a)(x + b)/(x − a)
        num_ = expr([(1, "x²"), (b - a, "x"), (-a * b, "")])
        v = a + b
        return MN("Nilai lim<sub>x→%s</sub> (%s)/(%s) adalah …" % (sn(a), num_, lin(1, -a)), v, [b if b != v else v + 1, 0, -a * b if -a * b != v else v - 1], "Faktorkan: (%s)(%s)/(%s) = %s. Substitusi x = %s: %s." % (lin(1, -a), lin(1, b), lin(1, -a), lin(1, b), sn(a), sn(v)))

    def faktor2():
        a = ri(1, 7)
        k = ri(0, 2)
        if k == 2:
            return MN("Nilai lim<sub>x→%d</sub> (x³ − %d)/(x − %d) adalah …" % (a, a ** 3, a), 3 * a * a, [a * a, 3 * a, 0], "x³ − %d = (x − %d)(x² + %dx + %d), jadi limitnya %d + %d + %d = %d." % (a ** 3, a, a, a * a, a * a, a * a, a * a, 3 * a * a))
        if k == 0:
            v = 2 * a
            return MN("Nilai lim<sub>x→%d</sub> (x² − %d)/(x − %d) adalah …" % (a, a * a, a), v, [a, 0, a * a], "(x − %d)(x + %d)/(x − %d) = x + %d → %d." % (a, a, a, a, v))
        c = nz(-5, 5)
        v = Fr(1, 2 * a) if True else 0
        # (√x − a)/(x − a²) = 1/(√x + a)
        return M("Nilai lim<sub>x→%d</sub> (√x − %d)/(x − %d) adalah …" % (a * a, a, a * a), fq(Fr(1, 2 * a)), [fq(Fr(1, a)), "0", fq(Fr(2 * a))], "Kalikan sekawan (√x + %d): hasilnya 1/(√x + %d) → 1/%d." % (a, a, 2 * a))

    def takhingga():
        a, b = nz(-6, 6), nz(1, 6)
        p, q = ri(-9, 9), ri(-9, 9)
        k = ri(0, 2)
        if k == 0:
            v = Fr(a, b)
            return M("Nilai lim<sub>x→∞</sub> (%s)/(%s) adalah …" % (expr([(a, "x²"), (p, "x"), (q, "")]), expr([(b, "x²"), (ri(-9, 9), "x"), (nz(-9, 9), "")])), fq(v), [fq(Fr(b, a)), "0", "∞", fq(Fr(p, b)) if Fr(p, b) != v else "1"],
                     "Pangkat tertinggi pembilang dan penyebut sama (2): limitnya %s/%s = %s." % (sn(a), sn(b), fq(v)))
        if k == 1:
            return M("Nilai lim<sub>x→∞</sub> (%s)/(%s) adalah …" % (expr([(a, "x"), (p, "")]), expr([(b, "x²"), (q, "x"), (nz(-9, 9), "")])), "0", [fq(Fr(a, b)), "∞", fq(Fr(b, a))],
                     "Pangkat tertinggi penyebut lebih besar: limitnya 0.")
        sgn = "∞" if a * b > 0 else MINUS + "∞"
        return M("Nilai lim<sub>x→∞</sub> (%s)/(%s) adalah …" % (expr([(a, "x³"), (p, "x"), (q, "")]), expr([(b, "x²"), (ri(-9, 9), "x"), (nz(-9, 9), "")])), sgn, [fq(Fr(a, b)), "0", MINUS + "∞" if sgn == "∞" else "∞"],
                 "Pangkat tertinggi pembilang lebih besar: limitnya %s." % sgn)

    def sifat():
        f, g = nz(-6, 6), nz(-6, 6)
        k = ri(0, 2)
        if k == 0:
            v = f + g
            return MN("Jika lim f(x) = %s dan lim g(x) = %s untuk x → 2, maka lim [f(x) + g(x)] = …" % (sn(f), sn(g)), v, [f * g, f - g if f - g != v else v + 1, v * 2], "Limit jumlah = jumlah limit: %s." % sn(v))
        if k == 1:
            c = ri(2, 5)
            v = c * f - g
            return MN("Jika lim f(x) = %s dan lim g(x) = %s untuk x → 1, maka lim [%df(x) − g(x)] = …" % (sn(f), sn(g), c), v, [c * f + g, c * (f - g) if c * (f - g) != v else v + 1, f - g if f - g != v else v - 1], "%d × %s − %s = %s." % (c, par(f), par(g), sn(v)))
        v = f * f
        return MN("Jika lim<sub>x→3</sub> f(x) = %s, maka lim<sub>x→3</sub> [f(x)]² = …" % sn(f), v, [2 * f, f, -v], "Limit pangkat = pangkat limit: %s² = %s." % (par(f), sn(v)))

    sets = [("Substitusi langsung", [(subst, 20)]),
            ("Bentuk 0/0: pemfaktoran", [(faktor, 20)]),
            ("Bentuk 0/0: selisih kuadrat dan akar sekawan", [(faktor2, 12), (sifat, 8)]),
            ("Limit di tak hingga", [(takhingga, 20)]),
            ("Sifat-sifat limit dan campuran", [(sifat, 8), (faktor, 6), (takhingga, 6)])]
    return unit("limit-fungsi-aljabar", "A", 3, "Limit Fungsi Aljabar", "Limit Fungsi",
                "Peserta didik menentukan limit fungsi aljabar dengan substitusi, pemfaktoran, dan perkalian sekawan, menentukan limit di tak hingga, dan menggunakan sifat-sifat limit.",
                "Latihan limit fungsi aljabar kelas 12 SMA: substitusi langsung, bentuk tak tentu 0/0 dengan pemfaktoran dan akar sekawan, limit di tak hingga, dan sifat-sifat limit. 100 soal dengan kunci jawaban.",
                "Hasil 0/0: faktorkan lalu sederhanakan", "Limit di ∞: bandingkan pangkat tertinggi.", sets,
                ["lim<sub>x→a</sub> f(x) adalah nilai yang didekati f(x) ketika x mendekati a. Coba substitusi langsung lebih dulu.",
                 "Jika substitusi menghasilkan 0/0, faktorkan pembilang dan penyebut lalu coret faktor yang sama, atau kalikan dengan bentuk sekawan jika ada akar.",
                 "Untuk limit di tak hingga, bandingkan pangkat tertinggi: sama berarti hasil bagi koefisiennya, penyebut lebih tinggi berarti 0, pembilang lebih tinggi berarti ±∞."],
                [("lim<sub>x→3</sub> (x² − 9)/(x − 3)", ["(x − 3)(x + 3)/(x − 3) = x + 3"], "6"),
                 ("lim<sub>x→∞</sub> (4x² + 1)/(2x² − x)", ["Pangkat sama: 4/2"], "2")],
                [["0/0 dianggap 0", "0/0 bentuk tak tentu: sederhanakan dulu"],
                 ["Limit di ∞ selalu 0", "Bandingkan pangkat tertinggi pembilang dan penyebut"],
                 ["Mencoret x, bukan faktor", "Yang dicoret harus faktor yang sama, misalnya (x − 3)"]],
                [("Apakah limit sama dengan nilai fungsi?", "Tidak selalu. Fungsi bisa tidak terdefinisi di x = a tetapi limitnya ada, seperti (x² − 9)/(x − 3) di x = 3."),
                 ("Apa itu bentuk tak tentu?", "Bentuk seperti 0/0 atau ∞/∞ yang belum menunjukkan nilai; perlu disederhanakan dulu."),
                 ("Untuk apa limit dipelajari?", "Limit adalah dasar turunan dan integral, misalnya untuk menghitung kecepatan sesaat.")])


# ============================================================ 4. turunan
def u4():
    def pangkat():
        k = ri(0, 2)
        if k == 0:
            cs = rnd_poly(ri(2, 4))
            d = deriv(cs)
            wrong = {k_: c for k_, c in cs.items() if k_ > 0}
            return M("Turunan pertama f(x) = %s adalah f′(x) = …" % P(cs), P(d), [P({k_ - 1: c for k_, c in cs.items() if k_ > 0}), P({k_: c * k_ for k_, c in cs.items() if k_ > 0}), P({k_ - 1: c * k_ for k_, c in cs.items()} if 0 not in cs or cs[0] == 0 else {**{k_ - 1: c * k_ for k_, c in cs.items() if k_ > 0}, 0: d.get(0, 0) + cs[0]})],
                     "Turunan axⁿ adalah naxⁿ⁻¹, turunan konstanta 0: %s." % P(d))
        if k == 1:
            a, n = nz(-6, 6), ri(-3, -1)
            return M("Turunan f(x) = %s adalah …" % (expr([(a, "x" + sup(n))])), expr([(a * n, "x" + sup(n - 1))]), [expr([(a * n, "x" + sup(n + 1))]), expr([(a, "x" + sup(n - 1))]), expr([(-a * n, "x" + sup(n - 1))])],
                     "f′(x) = %s × %s x%s = %s." % (sn(a), par(n), sup(n - 1), expr([(a * n, "x" + sup(n - 1))])))
        a = nz(-5, 5) * 2
        return M("Turunan f(x) = %s√x adalah …" % ("" if a == 1 else sn(a)), "%s/√x" % sn(Fr(a, 2)) if Fr(a, 2).denominator == 1 else "", ["%s√x" % sn(Fr(a, 2)), "%s/√x" % sn(a), "%sx√x" % sn(Fr(a * 3, 2)) if Fr(a * 3, 2).denominator == 1 else "%sx" % sn(a)],
                 "√x = x<sup>1/2</sup>, turunannya ½x<sup>−1/2</sup>. Jadi f′(x) = %s/√x." % sn(Fr(a, 2)))

    def nilai():
        cs = rnd_poly(ri(2, 3))
        a = nz(-3, 3)
        d = deriv(cs)
        v = ev(d, a)
        return MN("Jika f(x) = %s, nilai f′(%s) adalah …" % (P(cs), sn(a)), v, [ev(cs, a), ev(d, -a) if ev(d, -a) != v else v + 1, v + cs.get(0, 0) if cs.get(0, 0) else v - 2], "f′(x) = %s, f′(%s) = %s." % (P(d), sn(a), sn(v)))

    def aturan():
        k = ri(0, 1)
        a, b, c, d = nz(-4, 4), nz(-6, 6), nz(-4, 4), nz(-6, 6)
        if k == 0:
            # (ax + b)(cx + d) → 2acx + ad + bc
            r = lin(2 * a * c, a * d + b * c)
            return M("Turunan f(x) = (%s)(%s) adalah …" % (lin(a, b), lin(c, d)), r, [sn(a * c), lin(a * c, a * d + b * c), lin(2 * a * c, a * d - b * c) if a * d - b * c != a * d + b * c else lin(a * c, b * d)],
                     "Aturan perkalian u′v + uv′: %s(%s) + (%s) × %s = %s." % (sn(a), lin(c, d), lin(a, b), par(c), r))
        n = ri(2, 5)
        r = "%s(%s)%s" % (sn(n * a), lin(a, b), up(n - 1))
        return M("Turunan f(x) = (%s)%s adalah …" % (lin(a, b), sup(n)), r, ["%s(%s)%s" % (sn(n), lin(a, b), up(n - 1)), "%s(%s)%s" % (sn(n * a), lin(a, b), sup(n)), "%s(%s)%s" % (sn(n), lin(a, b), sup(n)), "%s(%s)%s" % (sn(-n * a), lin(a, b), up(n - 1))],
                 "Aturan rantai: %d(%s)%s × %s = %s." % (n, lin(a, b), up(n - 1), par(a), r))

    def singgung():
        cs = rnd_poly(2, -5, 5)
        a = ri(-3, 3)
        m = ev(deriv(cs), a)
        y0 = ev(cs, a)
        c = y0 - m * a
        r = "y = %s" % lin(m, c) if m else "y = %s" % sn(c)
        return M("Persamaan garis singgung kurva y = %s di titik berabsis x = %s adalah …" % (P(cs), sn(a)), r, ["y = %s" % lin(m, y0) if m else "y = %s" % sn(y0 + 1), "y = %s" % lin(-m if m else 1, c), "y = %s" % lin(m if m else 2, c + 1)],
                 "y(%s) = %s, gradien m = f′(%s) = %s. y − %s = %s(x − %s) → %s." % (sn(a), sn(y0), sn(a), sn(m), par(y0), sn(m), par(a), r))

    sets = [("Turunan fungsi pangkat", [(pangkat, 20)]),
            ("Nilai turunan", [(nilai, 20)]),
            ("Aturan perkalian dan aturan rantai", [(aturan, 20)]),
            ("Gradien dan garis singgung", [(singgung, 20)]),
            ("Campuran", [(pangkat, 7), (aturan, 7), (singgung, 6)])]
    return unit("turunan-fungsi-aljabar", "A", 4, "Turunan Fungsi Aljabar", "Turunan Fungsi",
                "Peserta didik menentukan turunan fungsi aljabar dengan aturan pangkat, perkalian, dan rantai, serta menggunakan turunan untuk menentukan gradien dan persamaan garis singgung.",
                "Latihan turunan fungsi aljabar kelas 12 SMA: turunan axⁿ, pangkat negatif dan akar, nilai f′(a), aturan perkalian, aturan rantai, dan persamaan garis singgung kurva. 100 soal dengan kunci jawaban.",
                "Turunan axⁿ adalah naxⁿ⁻¹", "f′(a) adalah gradien garis singgung di x = a.", sets,
                ["Turunan f′(x) = lim<sub>h→0</sub> (f(x + h) − f(x))/h. Untuk f(x) = axⁿ, f′(x) = naxⁿ⁻¹; turunan konstanta adalah 0.",
                 "Aturan perkalian: (uv)′ = u′v + uv′. Aturan rantai: turunan (ax + b)ⁿ adalah n(ax + b)ⁿ⁻¹ × a.",
                 "Gradien garis singgung kurva di x = a adalah m = f′(a). Persamaannya y − f(a) = m(x − a)."],
                [("f(x) = 3x⁴ − 2x² + 5", ["12x³ − 4x"], "f′(x) = 12x³ − 4x"),
                 ("y = x² − 3x, x = 2", ["y = −2, m = 2 × 2 − 3 = 1"], "y = x − 4")],
                [["Turunan 5 adalah 5", "Turunan konstanta adalah 0"],
                 ["Turunan x⁻² adalah −2x⁻¹", "Pangkat dikurangi 1: −2x⁻³"],
                 ["Aturan rantai tanpa dikali a", "Kalikan dengan turunan bagian dalam"]],
                [("Apa arti turunan?", "Laju perubahan sesaat fungsi, atau gradien garis singgung grafiknya."),
                 ("Apakah turunan hasil kali sama dengan hasil kali turunan?", "Tidak. Pakai aturan (uv)′ = u′v + uv′."),
                 ("Bagaimana menurunkan √x?", "Tulis sebagai x<sup>1/2</sup>, lalu pakai aturan pangkat: ½x<sup>−1/2</sup> = 1/(2√x).")])


# ============================================================ 5. aplikasi turunan
def u5():
    def cubic():
        while True:
            p, q = sorted([ri(-4, 4), ri(-4, 4)])
            if p != q:
                break
        a = ch([1, -1]) * ch([1, 2])
        # f′ = 3a(x − p)(x − q) → f = a x³ − 3a(p+q)/2 x² + 3a pq x + d
        b = Fr(-3 * a * (p + q), 2)
        if b.denominator != 1:
            return None
        c = 3 * a * p * q
        d = ri(-5, 5)
        cs = {3: a, 2: int(b), 1: c, 0: d}
        return cs, p, q

    def stasioner():
        r = cubic()
        if not r:
            return None
        cs, p, q = r
        k = ri(0, 1)
        if k == 0:
            return M("Fungsi f(x) = %s mempunyai titik stasioner di x = …" % P(cs), "%s dan %s" % (sn(p), sn(q)), ["%s dan %s" % (sn(-q), sn(-p)), "%s dan %s" % (sn(p), sn(-q)) if q else "%s dan 1" % sn(p), "%s dan %s" % (sn(p + q), sn(p * q)) if (p + q, p * q) not in ((p, q), (q, p)) else "%s dan %s" % (sn(p - 1), sn(q + 1))],
                     "f′(x) = %s = 0, jadi x = %s atau x = %s." % (P(deriv(cs)), sn(p), sn(q)))
        mx = p if cs[3] > 0 else q
        mn = q if cs[3] > 0 else p
        w = ch(["maksimum", "minimum"])
        x0 = mx if w == "maksimum" else mn
        v = ev(cs, x0)
        o = mn if w == "maksimum" else mx
        return MN("Nilai %s lokal fungsi f(x) = %s adalah …" % (w, P(cs)), v, [ev(cs, o), sn(x0) and Fr(x0), ev(cs, 0) if ev(cs, 0) not in (v, ev(cs, o)) else v + 1], "f′(x) = 0 di x = %s dan x = %s. Nilai %s lokal di x = %s: f(%s) = %s." % (sn(p), sn(q), w, sn(x0), sn(x0), sn(v)))

    def naik():
        r = cubic()
        if not r:
            return None
        cs, p, q = r
        up = cs[3] > 0
        w = ch(["naik", "turun"])
        if (w == "naik") == up:
            c = "x &lt; %s atau x &gt; %s" % (sn(p), sn(q))
            o = "%s &lt; x &lt; %s" % (sn(p), sn(q))
        else:
            o = "x &lt; %s atau x &gt; %s" % (sn(p), sn(q))
            c = "%s &lt; x &lt; %s" % (sn(p), sn(q))
        return M("Fungsi f(x) = %s %s pada interval …" % (P(cs), w), c, [o, "x &gt; %s" % sn(q), "x &lt; %s" % sn(p), "%s &lt; x &lt; %s" % (sn(-q), sn(-p))],
                 "f′(x) = %s. f %s jika f′(x) %s 0, yaitu %s." % (P(deriv(cs)), w, "&gt;" if w == "naik" else "&lt;", c))

    def optim():
        k = ri(0, 3)
        if k == 0:
            L = ri(5, 30) * 4
            s = L // 4
            return MN("Keliling sebuah persegi panjang %d m. Luas maksimumnya adalah … m²" % L, s * s, [s * (s + 1) if False else (L // 2) ** 2 // 2, L * L // 4, s * s // 2 if s % 2 == 0 else s * s + s], "L = x(%d − x), L′ = %d − 2x = 0 → x = %d. Luas maksimum %d × %d = %s m²." % (L // 2, L // 2, s, s, s, num(s * s)))
        if k == 1:
            v0 = ri(2, 10) * 5
            g = 5
            t = Fr(v0, 2 * g)
            h = v0 * t - g * t * t
            if t.denominator != 1:
                return None
            return MN("Tinggi bola setelah t detik adalah h(t) = %dt − 5t² meter. Tinggi maksimum bola adalah … m" % v0, h, [v0 * t, h * 2, int(t)], "h′(t) = %d − 10t = 0 → t = %s. h(%s) = %s m." % (v0, sn(t), sn(t), sn(h)))
        if k == 2:
            n = ri(4, 20) * 2
            x = n // 2
            return MN("Jumlah dua bilangan positif adalah %d. Hasil kali maksimum kedua bilangan itu adalah …" % n, x * x, [n * n // 2, x * x - 1, n], "P = x(%d − x), P′ = %d − 2x = 0 → x = %d. P = %d × %d = %s." % (n, n, x, x, x, num(x * x)))
        a = ri(2, 6)
        b = ri(20, 80) * 2 * a
        x = Fr(b, 2 * a)
        if x.denominator != 1:
            return None
        p = b * x - a * x * x
        return MN("Keuntungan menjual x barang adalah K(x) = %sx − %sx² ribu rupiah. Banyak barang agar keuntungan maksimum adalah …" % (num(b), sn(a)), x, [x * 2, Fr(b, a), x + 1], "K′(x) = %s − %dx = 0 → x = %s." % (num(b), 2 * a, num(int(x))))

    def gerak():
        a, b, c = ri(1, 3), ri(-6, 6), ri(-9, 9)
        t = ri(1, 5)
        k = ri(0, 1)
        s = {3: a, 2: b, 1: c}
        v = deriv(s)
        if k == 0:
            val = ev(v, t)
            return MN("Posisi benda s(t) = %s meter. Kecepatan benda saat t = %d detik adalah … m/s" % (P(s, "t"), t), val, [ev(s, t), ev(deriv(v), t), val + c], "v(t) = s′(t) = %s, v(%d) = %s m/s." % (P(v, "t"), t, sn(val)))
        acc = deriv(v)
        val = ev(acc, t)
        return MN("Posisi benda s(t) = %s meter. Percepatan benda saat t = %d detik adalah … m/s²" % (P(s, "t"), t), val, [ev(v, t) if ev(v, t) != val else val + 1, ev(s, t) if ev(s, t) != val else val - 2, 6 * a], "a(t) = s″(t) = %s, a(%d) = %s m/s²." % (P(acc, "t"), t, sn(val)))

    sets = [("Titik stasioner dan nilai ekstrem", [(stasioner, 20)]),
            ("Interval fungsi naik dan turun", [(naik, 20)]),
            ("Masalah optimasi", [(optim, 20)]),
            ("Kecepatan dan percepatan", [(gerak, 20)]),
            ("Campuran", [(stasioner, 6), (naik, 6), (optim, 8)])]
    return unit("aplikasi-turunan", "A", 5, "Aplikasi Turunan: Fungsi Naik, Titik Stasioner, dan Optimasi", "Aplikasi Turunan",
                "Peserta didik menggunakan turunan untuk menentukan interval fungsi naik dan turun, titik stasioner, nilai maksimum dan minimum, serta menyelesaikan masalah optimasi dan gerak.",
                "Latihan aplikasi turunan kelas 12 SMA: titik stasioner, nilai maksimum dan minimum lokal, interval fungsi naik dan turun, masalah optimasi (luas, keuntungan, tinggi maksimum), kecepatan dan percepatan. 100 soal dengan kunci jawaban.",
                "Titik stasioner: f′(x) = 0", "f′ positif: naik. f′ negatif: turun.", sets,
                ["Fungsi naik jika f′(x) &gt; 0 dan turun jika f′(x) &lt; 0. Titik stasioner terjadi saat f′(x) = 0.",
                 "Pada titik stasioner, jika f′ berubah dari positif ke negatif, titik itu maksimum; dari negatif ke positif, minimum.",
                 "Masalah optimasi: nyatakan besaran yang dicari sebagai fungsi satu variabel, turunkan, samakan dengan 0, lalu hitung nilainya. Kecepatan v = s′(t), percepatan a = v′(t)."],
                [("f(x) = x³ − 3x² − 9x + 2", ["f′(x) = 3x² − 6x − 9 = 3(x + 1)(x − 3)"], "Stasioner di x = −1 (maksimum) dan x = 3 (minimum)"),
                 ("Keliling 40 m, luas maksimum?", ["L = x(20 − x), L′ = 20 − 2x = 0, x = 10"], "100 m²")],
                [["Nilai maksimum ditulis sebagai nilai x", "Nilai maksimum adalah f(x), bukan x"],
                 ["f′(x) = 0 pasti maksimum", "Periksa perubahan tanda f′ untuk tahu maksimum atau minimum"],
                 ["Kecepatan = posisi", "Kecepatan adalah turunan posisi"]],
                [("Apa beda maksimum lokal dan maksimum mutlak?", "Maksimum lokal adalah nilai terbesar di sekitar suatu titik. Maksimum mutlak adalah nilai terbesar pada seluruh interval yang ditinjau."),
                 ("Bagaimana memakai turunan kedua?", "Jika f″(a) &lt; 0 di titik stasioner, titik itu maksimum; jika f″(a) &gt; 0, minimum."),
                 ("Di mana optimasi dipakai?", "Untuk mencari biaya terkecil, keuntungan terbesar, atau ukuran kemasan yang paling hemat bahan.")])


# ============================================================ 6. integral tak tentu
def u6():
    def ps(cs):
        return P(cs) + " + C"

    def poly():
        return pangkat(0)

    def pangkat(k=None):
        k = ri(0, 2) if k is None else k
        if k == 0:
            deg = ri(1, 3)
            cs = {deg: (deg + 1) * nz(-3, 3)}
            for j in range(deg - 1, -1, -1):
                cs[j] = (j + 1) * ri(-4, 4)
            I = integ(cs)
            return M("Hasil ∫(%s) dx adalah …" % P(cs), ps(I), [ps(deriv(cs)), ps({k_ + 1: c for k_, c in cs.items()}), ps({k_ + 1: Fr(c, k_ + 2) for k_, c in cs.items()})],
                     "∫axⁿ dx = a/(n + 1) xⁿ⁺¹ + C: %s." % ps(I))
        if k == 1:
            a, n = nz(-6, 6), ri(-4, -2)
            I = {n + 1: Fr(a, n + 1)}
            return M("Hasil ∫%s dx adalah …" % expr([(a, "x" + sup(n))]), expr([(Fr(a, n + 1), "x" + sup(n + 1))]) + " + C",
                     [expr([(Fr(a, n - 1), "x" + sup(n - 1))]) + " + C", expr([(a * n, "x" + sup(n - 1))]) + " + C", expr([(a, "x" + sup(n + 1))]) + " + C"],
                     "∫%s dx = %s/%s x%s + C." % (expr([(a, "x" + sup(n))]), sn(a), par(n + 1), sup(n + 1)))
        a = ri(1, 6) * 3
        return M("Hasil ∫%s√x dx adalah …" % ("" if a == 1 else sn(a)), "%sx√x + C" % sn(Fr(2 * a, 3)), ["%s√x + C" % sn(Fr(2 * a, 3)), "%sx√x + C" % sn(Fr(3 * a, 2)), "%sx + C" % sn(a)],
                 "√x = x<sup>1/2</sup>: ∫x<sup>1/2</sup> dx = ⅔x<sup>3/2</sup>. Jadi %sx√x + C." % sn(Fr(2 * a, 3)))

    def fungsi():
        cs = {2: 3 * nz(-2, 2), 1: 2 * ri(-4, 4), 0: ri(-6, 6)}
        x0 = ri(-2, 2)
        y0 = ri(-10, 10)
        I = integ(cs)
        C = y0 - ev(I, x0)
        F = dict(I)
        F[0] = C
        return M("Diketahui f′(x) = %s dan f(%s) = %s. Fungsi f(x) adalah …" % (P(cs), sn(x0), sn(y0)), P(F), [P({**I, 0: y0}) if C != y0 else P({**I, 0: C + 1}), P({**I, 0: -C}) if C else P({**I, 0: 2}), P({**deriv(cs), 0: C}) if 0 in deriv(cs) else P({**I, 0: C + 2})],
                 "f(x) = %s + C. f(%s) = %s → C = %s." % (P(I), sn(x0), sn(y0), sn(C)))

    def subst():
        a, b = nz(-4, 4), nz(-6, 6)
        n = ri(2, 5)
        r = "%s(%s)%s + C" % (fq(Fr(1, a * (n + 1))) + " " if abs(a * (n + 1)) != 1 else ("" if a * (n + 1) == 1 else MINUS), lin(a, b), sup(n + 1))
        return M("Hasil ∫(%s)%s dx adalah …" % (lin(a, b), sup(n)), r,
                 ["%s(%s)%s + C" % (fq(Fr(1, n + 1)), lin(a, b), sup(n + 1)), "%s(%s)%s + C" % (sn(n * a), lin(a, b), up(n - 1)), "%s(%s)%s + C" % (fq(Fr(1, a * n)) if abs(a * n) != 1 else "", lin(a, b), sup(n + 1))],
                 "Misalkan u = %s, du = %s dx: ∫u%s du/%s = %s." % (lin(a, b), sn(a), sup(n), par(a), r))

    def kurva():
        a = nz(-3, 3) * 2
        b = ri(-5, 5)
        x0, y0 = ri(-2, 3), ri(-8, 8)
        I = {2: Fr(a, 2), 1: b}
        C = y0 - ev(I, x0)
        F = {**I, 0: C}
        return M("Gradien garis singgung suatu kurva adalah dy/dx = %s. Jika kurva melalui titik (%s, %s), persamaan kurvanya adalah y = …" % (lin(a, b), sn(x0), sn(y0)), P(F), [P({**I, 0: y0}) if C != y0 else P({**I, 0: C + 1}), P({2: a, 1: b, 0: C}), P({**I, 0: -C}) if C else P({**I, 0: 3})],
                 "y = %s + C. Substitusi (%s, %s): C = %s." % (P(I), sn(x0), sn(y0), sn(C)))

    sets = [("Integral fungsi pangkat", [(pangkat, 20)]),
            ("Integral polinomial", [(poly, 20)]),
            ("Menentukan fungsi dari turunannya", [(fungsi, 20)]),
            ("Integral substitusi", [(subst, 20)]),
            ("Persamaan kurva dari gradien", [(kurva, 14), (subst, 6)])]
    return unit("integral-tak-tentu", "A", 6, "Integral Tak Tentu", "Integral Tak Tentu",
                "Peserta didik memahami integral sebagai antiturunan, menentukan integral tak tentu fungsi aljabar dengan aturan pangkat dan substitusi, serta menentukan fungsi dari turunannya.",
                "Latihan integral tak tentu kelas 12 SMA: integral axⁿ, pangkat negatif dan akar, integral polinomial, menentukan konstanta C, integral substitusi (ax + b)ⁿ, dan persamaan kurva dari gradien. 100 soal dengan kunci jawaban.",
                "∫axⁿ dx = a/(n + 1) xⁿ⁺¹ + C", "Integral adalah kebalikan turunan.", sets,
                ["Integral tak tentu adalah antiturunan: jika F′(x) = f(x), maka ∫f(x) dx = F(x) + C. Konstanta C muncul karena turunan konstanta adalah 0.",
                 "Aturan pangkat: ∫axⁿ dx = a/(n + 1) xⁿ⁺¹ + C untuk n ≠ −1. Integral jumlah adalah jumlah integral.",
                 "Untuk ∫(ax + b)ⁿ dx, misalkan u = ax + b: hasilnya (ax + b)ⁿ⁺¹/(a(n + 1)) + C. Nilai C ditentukan dari satu titik yang diketahui."],
                [("∫(6x² − 4x + 3) dx", ["2x³ − 2x² + 3x"], "2x³ − 2x² + 3x + C"),
                 ("f′(x) = 2x, f(1) = 5", ["f(x) = x² + C, 1 + C = 5"], "f(x) = x² + 4")],
                [["Lupa + C", "Integral tak tentu selalu ditambah C"],
                 ["Pangkat ditambah 1 tetapi tidak dibagi", "Bagi dengan pangkat yang baru"],
                 ["∫(2x + 1)³ dx = (2x + 1)⁴/4 + C", "Bagi juga dengan 2: (2x + 1)⁴/8 + C"]],
                [("Mengapa ada + C?", "Banyak fungsi mempunyai turunan yang sama, misalnya x² dan x² + 5. C mewakili semua kemungkinan itu."),
                 ("Bagaimana mengecek hasil integral?", "Turunkan hasilnya. Jika kembali ke fungsi semula, integralnya benar."),
                 ("Mengapa n ≠ −1?", "Karena pembaginya n + 1 menjadi 0. Integral x⁻¹ dipelajari dengan logaritma natural.")])


# ============================================================ 7. integral tentu
def u7():
    def tentu():
        cs = {2: 3 * nz(-2, 2), 1: 2 * ri(-3, 3), 0: ri(-5, 5)}
        a = ri(-2, 1)
        b = a + ri(1, 3)
        I = integ(cs)
        v = ev(I, b) - ev(I, a)
        return MN("Nilai ∫<sub>%s</sub><sup>%s</sup> (%s) dx adalah …" % (sn(a), sn(b), P(cs)), v, [ev(I, b) + ev(I, a), ev(cs, b) - ev(cs, a), ev(I, b)] if ev(I, b) != v else [ev(I, b) + ev(I, a) + 1, ev(cs, b) - ev(cs, a), -v if v else 1],
                  "[%s]<sub>%s</sub><sup>%s</sup> = %s − %s = %s." % (P(I), sn(a), sn(b), par(ev(I, b)), par(ev(I, a)), sn(v)))

    def sifat():
        p, q = nz(-9, 9), nz(-9, 9)
        k = ri(0, 2)
        if k == 0:
            return MN("Jika ∫<sub>1</sub><sup>4</sup> f(x) dx = %s dan ∫<sub>4</sub><sup>7</sup> f(x) dx = %s, maka ∫<sub>1</sub><sup>7</sup> f(x) dx = …" % (sn(p), sn(q)), p + q, [p - q, q - p if q - p != p - q else p * q, p * q], "Interval berurutan dapat digabung: %s + %s = %s." % (sn(p), par(q), sn(p + q)))
        if k == 1:
            return MN("Jika ∫<sub>2</sub><sup>5</sup> f(x) dx = %s, maka ∫<sub>5</sub><sup>2</sup> f(x) dx = …" % sn(p), -p, [p, 0, 2 * p], "Menukar batas mengubah tanda: %s." % sn(-p))
        c = ri(2, 5)
        return MN("Jika ∫<sub>0</sub><sup>3</sup> f(x) dx = %s, maka ∫<sub>0</sub><sup>3</sup> (%df(x) + 2) dx = …" % (sn(p), c), c * p + 6, [c * p + 2, c * (p + 2), c * p], "%d × %s + ∫<sub>0</sub><sup>3</sup> 2 dx = %s + 6 = %s." % (c, par(p), sn(c * p), sn(c * p + 6)))

    def luas():
        k = ri(0, 1)
        if k == 0:
            p, q = sorted(sh(range(-4, 6))[:2])
            # y = −(x − p)(x − q) di atas sumbu x antara p dan q
            cs = {2: -1, 1: p + q, 0: -p * q}
            L = Fr((q - p) ** 3, 6)
            X = lambda x: -(x - p) * (x - q)
            lo_, hi_ = min(-2, int(X(q + 1)) - 1), int(Fr((q - p) ** 2, 4)) + 2
            st_ = 1 if hi_ - lo_ <= 8 else 2
            lo_ -= lo_ % st_
            hi_ += (-hi_) % st_
            pic = kurve([(X, BLUE, "")], (p - 1, q + 1, 1), (lo_, hi_, st_), label="kurva dan sumbu x")
            return M("Luas daerah yang dibatasi kurva y = %s dan sumbu x adalah … satuan luas" % P(cs) + pic, fq(L) if L.denominator > 1 else sn(L), [fq(x) for x in (Fr((q - p) ** 2, 2), Fr((q - p) ** 3, 3), -L, L + 1, Fr((q - p) ** 3, 2)) if x != L],
                     "Kurva memotong sumbu x di x = %s dan x = %s. L = ∫<sub>%s</sub><sup>%s</sup> (%s) dx = %s." % (sn(p), sn(q), sn(p), sn(q), P(cs), fq(L)))
        a = ri(1, 4)
        b = a + ri(1, 3)
        c = ri(0, 3)
        cs = {2: 1, 0: c}
        I = integ(cs)
        L = ev(I, b) - ev(I, a)
        return M("Luas daerah di bawah kurva y = %s, di atas sumbu x, antara x = %d dan x = %d adalah … satuan luas" % (P(cs), a, b), fq(L), [fq(x) for x in (Fr(b * b - a * a + 0), Fr(b ** 3 - a ** 3), (b - a) * (b * b + c), L + 1) if x != L],
                 "L = [%s]<sub>%d</sub><sup>%d</sup> = %s." % (P(I), a, b, fq(L)))

    def dua_kurva():
        p, q = sorted(sh(range(-3, 5))[:2])
        # y1 = x + p+q ... gunakan y = x² dan garis y = (p+q)x − pq
        L = Fr((q - p) ** 3, 6)
        g = lin(p + q, -p * q) if p + q else sn(-p * q)
        return M("Luas daerah yang dibatasi kurva y = x² dan garis y = %s adalah … satuan luas" % g, fq(L), [fq(x) for x in (Fr((q - p) ** 3, 3), Fr((q - p) ** 2, 2), L * 2, L + 1) if x != L],
                 "Titik potong: x² = %s → x = %s dan x = %s. L = ∫<sub>%s</sub><sup>%s</sup> (%s − x²) dx = %s." % (g, sn(p), sn(q), sn(p), sn(q), g, fq(L)))

    sets = [("Menghitung integral tentu", [(tentu, 20)]),
            ("Sifat-sifat integral tentu", [(sifat, 20)]),
            ("Luas daerah di bawah kurva", [(luas, 20)]),
            ("Luas daerah antara dua kurva", [(dua_kurva, 20)]),
            ("Campuran", [(tentu, 8), (luas, 6), (sifat, 6)])]
    return unit("integral-tentu-dan-luas-daerah", "A", 7, "Integral Tentu dan Luas Daerah", "Integral Tentu",
                "Peserta didik menghitung integral tentu dengan teorema dasar kalkulus, menggunakan sifat-sifat integral tentu, dan menentukan luas daerah di bawah kurva dan di antara dua kurva.",
                "Latihan integral tentu kelas 12 SMA: menghitung integral tentu, sifat-sifat integral tentu (menggabung interval, menukar batas), luas daerah di bawah kurva, dan luas daerah antara kurva dan garis. 100 soal dengan kunci jawaban.",
                "∫ₐᵇ f(x) dx = F(b) − F(a)", "Luas = ∫ (kurva atas − kurva bawah) dx", sets,
                ["Teorema dasar kalkulus: jika F′(x) = f(x), maka ∫<sub>a</sub><sup>b</sup> f(x) dx = F(b) − F(a). Konstanta C tidak perlu ditulis.",
                 "Sifat: ∫<sub>a</sub><sup>b</sup> + ∫<sub>b</sub><sup>c</sup> = ∫<sub>a</sub><sup>c</sup>, dan menukar batas mengubah tanda.",
                 "Luas daerah antara dua kurva dari x = a sampai x = b adalah ∫(y atas − y bawah) dx. Batasnya sering adalah titik potong kedua kurva."],
                [("∫<sub>1</sub><sup>3</sup> 2x dx", ["[x²] dari 1 sampai 3 = 9 − 1"], "8"),
                 ("y = x² dan y = 2x", ["Titik potong x = 0 dan x = 2", "∫(2x − x²) dx = 4 − 8/3"], "4/3")],
                [["F(a) − F(b)", "Batas atas dulu: F(b) − F(a)"],
                 ["Luas di bawah sumbu x bernilai negatif", "Luas selalu positif; ambil nilai mutlaknya"],
                 ["Menghitung y bawah − y atas", "Kurangkan dari kurva yang di atas"]],
                [("Apa beda integral tentu dan tak tentu?", "Integral tak tentu menghasilkan fungsi + C, sedangkan integral tentu menghasilkan bilangan."),
                 ("Apakah integral tentu selalu sama dengan luas?", "Hanya jika kurvanya di atas sumbu x. Bagian di bawah sumbu x memberi nilai negatif."),
                 ("Di mana integral tentu dipakai?", "Untuk menghitung luas, volume benda putar, jarak dari kecepatan, dan banyak besaran fisika.")])


# ============================================================ 8. transformasi dan komposisi
def u8():
    def pt(a, b):
        return "(%s, %s)" % (sn(a), sn(b))

    T = {"pencerminan terhadap sumbu x": lambda x, y: (x, -y), "pencerminan terhadap sumbu y": lambda x, y: (-x, y),
         "pencerminan terhadap garis y = x": lambda x, y: (y, x), "pencerminan terhadap garis y = −x": lambda x, y: (-y, -x),
         "pencerminan terhadap titik asal O": lambda x, y: (-x, -y), "rotasi 90° berlawanan arah jarum jam dengan pusat O": lambda x, y: (-y, x),
         "rotasi 90° searah jarum jam dengan pusat O": lambda x, y: (y, -x), "rotasi 180° dengan pusat O": lambda x, y: (-x, -y)}
    names = list(T)

    def tunggal():
        x, y = nz(-8, 8), nz(-8, 8)
        if abs(x) == abs(y):
            return None
        n = ch(names)
        r = T[n](x, y)
        return M("Bayangan titik %s oleh %s adalah …" % (pt(x, y), n), pt(*r), [pt(*T[m](x, y)) for m in sh(names) if T[m](x, y) != r] + [pt(x, y)], "Aturan %s: %s → %s." % (n, pt(x, y), pt(*r)))

    def komposisi():
        x, y = nz(-7, 7), nz(-7, 7)
        if abs(x) == abs(y):
            return None
        a, b = nz(-5, 5), nz(-5, 5)
        n = ch(names)
        k = ri(0, 1)
        if k == 0:
            r = T[n](x + a, y + b)
            alt = T[n](x, y)
            return M("Titik %s ditranslasi oleh (%s, %s), lalu dilanjutkan %s. Bayangan akhirnya adalah …" % (pt(x, y), sn(a), sn(b), n), pt(*r), [pt(alt[0] + a, alt[1] + b), pt(x + a, y + b), pt(*T[n](x - a, y - b))],
                     "Translasi: %s. Lalu %s: %s." % (pt(x + a, y + b), n, pt(*r)))
        m = ch([v for v in names if v != n])
        r = T[m](*T[n](x, y))
        w = T[n](*T[m](x, y))
        return M("Titik %s dikenai %s, dilanjutkan %s. Bayangan akhirnya adalah …" % (pt(x, y), n, m), pt(*r), [pt(*w), pt(*T[n](x, y)), pt(*T[m](x, y)), pt(-r[0], -r[1]), pt(r[1], r[0])],
                 "Pertama %s, lalu %s: %s." % (pt(*T[n](x, y)), pt(*r), pt(*r)))

    def dilatasi():
        x, y = nz(-6, 6), nz(-6, 6)
        k = ch([2, 3, -2, Fr(1, 2), -1, 4])
        a, b = ri(-3, 3), ri(-3, 3)
        if (a, b) == (0, 0):
            r = (k * x, k * y)
            return M("Bayangan titik %s oleh dilatasi dengan pusat O dan faktor skala %s adalah …" % (pt(x, y), sn(k)), pt(*r), [pt(x + k, y + k), pt(-r[0], -r[1]), pt(x * k, y)], "(kx, ky) = %s." % pt(*r))
        r = (a + k * (x - a), b + k * (y - b))
        return M("Bayangan titik %s oleh dilatasi dengan pusat %s dan faktor skala %s adalah …" % (pt(x, y), pt(a, b), sn(k)), pt(*r), [pt(k * x, k * y), pt(k * (x - a), k * (y - b)), pt(a + k * x, b + k * y)],
                 "(a + k(x − a), b + k(y − b)) = %s." % pt(*r))

    def garis():
        a, b, c = nz(-5, 5), nz(-5, 5), ri(-9, 9)
        n = ch(names[:5] + ["translasi"])
        if n == "translasi":
            p, q = nz(-4, 4), nz(-4, 4)
            # a(x − p) + b(y − q) + c = 0
            c2 = c - a * p - b * q
            r = expr([(a, "x"), (b, "y"), (c2, "")]) + " = 0"
            return M("Bayangan garis %s = 0 oleh translasi (%s, %s) adalah …" % (expr([(a, "x"), (b, "y"), (c, "")]), sn(p), sn(q)), r,
                     [expr([(a, "x"), (b, "y"), (c + a * p + b * q, "")]) + " = 0", expr([(a, "x"), (b, "y"), (c - p - q, "")]) + " = 0", expr([(b, "x"), (a, "y"), (c2, "")]) + " = 0"],
                     "Ganti x dengan x − %s dan y dengan y − %s: %s." % (par(p), par(q), r))
        if abs(a) == abs(b):
            return None
        inv = {"pencerminan terhadap sumbu x": (a, -b), "pencerminan terhadap sumbu y": (-a, b), "pencerminan terhadap garis y = x": (b, a),
               "pencerminan terhadap garis y = −x": (-b, -a), "pencerminan terhadap titik asal O": (-a, -b)}[n]
        r = expr([(inv[0], "x"), (inv[1], "y"), (c, "")]) + " = 0"
        alts = [expr([(u, "x"), (v, "y"), (c, "")]) + " = 0" for u, v in [(a, -b), (-a, b), (b, a), (-b, -a), (-a, -b), (a, b)] if (u, v) != inv]
        return M("Bayangan garis %s = 0 oleh %s adalah …" % (expr([(a, "x"), (b, "y"), (c, "")]), n), r, sh(alts), "Substitusikan aturan %s ke persamaan garis: %s." % (n, r))

    sets = [("Pencerminan dan rotasi", [(tunggal, 20)]),
            ("Dilatasi", [(dilatasi, 20)]),
            ("Komposisi transformasi", [(komposisi, 20)]),
            ("Bayangan garis", [(garis, 20)]),
            ("Campuran", [(komposisi, 8), (tunggal, 6), (dilatasi, 6)])]
    return unit("transformasi-geometri-dan-komposisinya", "G", 8, "Transformasi Geometri dan Komposisinya", "Komposisi Transformasi",
                "Peserta didik menentukan bayangan titik dan garis oleh translasi, refleksi, rotasi, dan dilatasi, serta oleh komposisi dua transformasi.",
                "Latihan transformasi geometri kelas 12 SMA: pencerminan terhadap sumbu dan garis, rotasi 90° dan 180°, dilatasi dengan pusat O dan pusat lain, komposisi transformasi, dan bayangan garis. 100 soal dengan kunci jawaban.",
                "Komposisi: kerjakan berurutan", "Rotasi 90° berlawanan: (x, y) → (−y, x)", sets,
                ["Pencerminan: sumbu x (x, −y), sumbu y (−x, y), garis y = x (y, x), garis y = −x (−y, −x). Rotasi 90° berlawanan arah jarum jam: (−y, x); 180°: (−x, −y).",
                 "Dilatasi pusat (a, b) dan faktor k: (x, y) → (a + k(x − a), b + k(y − b)).",
                 "Komposisi transformasi dikerjakan berurutan: hasil transformasi pertama menjadi titik awal transformasi kedua. Urutannya biasanya tidak boleh ditukar."],
                [("(3, −2) dicerminkan terhadap y = x, lalu dirotasi 180°.", ["(−2, 3)", "(2, −3)"], "(2, −3)"),
                 ("(4, 1) didilatasi pusat (1, 1), k = 3.", ["(1 + 3 × 3, 1 + 3 × 0)"], "(10, 1)")],
                [["Rotasi 90° berlawanan: (y, −x)", "Berlawanan arah jarum jam: (−y, x)"],
                 ["Dilatasi pusat (a, b) dihitung seperti pusat O", "Kurangi pusat dulu, kalikan k, lalu tambahkan pusat"],
                 ["Urutan komposisi ditukar", "Kerjakan sesuai urutan yang disebut"]],
                [("Apakah komposisi transformasi bersifat komutatif?", "Umumnya tidak. Pencerminan terhadap sumbu x lalu y = x biasanya berbeda dengan sebaliknya."),
                 ("Bagaimana memakai matriks untuk transformasi?", "Setiap refleksi, rotasi, dan dilatasi dengan pusat O dapat ditulis sebagai matriks 2 × 2. Komposisinya adalah hasil kali matriks."),
                 ("Transformasi mana yang mengubah ukuran?", "Hanya dilatasi (dengan k ≠ ±1). Translasi, refleksi, dan rotasi mempertahankan ukuran dan bentuk.")])


# ============================================================ 9. dimensi tiga
def u9():
    def kubus_svg():
        s = []
        A = (40, 190); B = (190, 190); C = (250, 140); D = (100, 140)
        E = (40, 40); F = (190, 40); G = (250, -10); H = (100, -10)
        off = 30
        P_ = {k: (v[0], v[1] + off) for k, v in dict(A=A, B=B, C=C, D=D, E=E, F=F, G=G, H=H).items()}
        solid = ["AB", "BC", "AE", "BF", "CG", "EF", "FG", "GH", "HE"]
        dashed = ["AD", "DC", "DH"]
        for e in solid:
            a, b = P_[e[0]], P_[e[1]]
            s.append(line(a[0], a[1], b[0], b[1], INK, 2))
        for e in dashed:
            a, b = P_[e[0]], P_[e[1]]
            s.append(line(a[0], a[1], b[0], b[1], INK, 1.5, " stroke-dasharray='6 4'"))
        lab = dict(A=(-14, 14), B=(8, 16), C=(14, 6), D=(-14, -4), E=(-14, -4), F=(-4, -8), G=(12, -4), H=(-6, -8))
        for k, (dx, dy) in lab.items():
            s.append(text(P_[k][0] + dx, P_[k][1] + dy, k, 15, italic=True))
        return wrap(280, 240, "".join(s), "kubus ABCD.EFGH")

    def jarak():
        a = ri(2, 15)
        k = ri(0, 4)
        pic = kubus_svg()
        if k == 0:
            return M("Panjang rusuk kubus ABCD.EFGH adalah %d cm. Jarak titik A ke titik C adalah … cm" % a + pic, surd(a, 2), [surd(a, 3), sn(2 * a), sn(a)], "AC diagonal sisi: %d√2 cm." % a)
        if k == 1:
            return M("Panjang rusuk kubus ABCD.EFGH adalah %d cm. Jarak titik A ke titik G adalah … cm" % a + pic, surd(a, 3), [surd(a, 2), sn(3 * a), surd(1, 3 * a) if a > 1 else "3"], "AG diagonal ruang: %d√3 cm." % a)
        if k == 2:
            return MN("Panjang rusuk kubus ABCD.EFGH adalah %d cm. Jarak titik A ke garis BF adalah … cm" % a + pic, a, [a * 2, Fr(a, 2), 0], "AB tegak lurus BF, jadi jaraknya AB = %d cm." % a)
        if k == 3:
            return M("Panjang rusuk kubus ABCD.EFGH adalah %d cm. Jarak titik E ke bidang ABCD adalah … cm" % a + pic, sn(a), [surd(a, 2), surd(a, 3), sn(Fr(a, 2)) if a % 2 == 0 else sn(2 * a)], "EA tegak lurus bidang ABCD: %d cm." % a)
        b = a * 2
        return M("Panjang rusuk kubus ABCD.EFGH adalah %d cm. Jarak titik A ke titik tengah rusuk GH adalah … cm" % b + pic, sn(3 * a), [surd(a, 5), surd(b, 3), sn(2 * b)],
                 "Misal M tengah GH. AM² = AD² + DH² + HM² = %d + %d + %d = %d, AM = %d cm." % (b * b, b * b, a * a, 9 * a * a, 3 * a))

    def balok():
        T = [(2, 3, 6, 7), (1, 2, 2, 3), (2, 6, 9, 11), (3, 4, 12, 13), (4, 4, 7, 9), (2, 10, 11, 15), (6, 6, 7, 11), (1, 4, 8, 9), (8, 9, 12, 17), (2, 5, 14, 15)]
        p, l, t, d = ch(T)
        p, l, t = sh([p, l, t])
        k = ri(0, 1)
        if k == 0:
            return MN("Balok ABCD.EFGH berukuran %d cm × %d cm × %d cm. Panjang diagonal ruangnya adalah … cm" % (p, l, t), d, [p + l + t, d * d, d + 1], "d = √(%d² + %d² + %d²) = √%d = %d cm." % (p, l, t, d * d, d))
        s2 = p * p + l * l
        r = math.isqrt(s2)
        c = sn(r) if r * r == s2 else surd(1, s2)
        return M("Balok ABCD.EFGH dengan AB = %d cm, BC = %d cm, dan AE = %d cm. Panjang diagonal sisi AC adalah … cm" % (p, l, t), c, [sn(p + l), sn(d), surd(1, p * p + t * t) if math.isqrt(p * p + t * t) ** 2 != p * p + t * t else sn(math.isqrt(p * p + t * t) + 1)], "AC = √(%d² + %d²) = %s cm." % (p, l, c))

    def sudut():
        F = [("antara garis AG dan bidang ABCD", "tan θ = ½√2", "AG diproyeksikan ke AC. tan θ = CG/AC = a/(a√2) = ½√2."),
             ("antara garis AF dan bidang ABCD", "45°", "AF diproyeksikan ke AB. Segitiga ABF siku-siku sama kaki, jadi 45°."),
             ("antara garis AH dan garis BG", "0°", "AH sejajar BG, jadi sudutnya 0°."),
             ("antara garis AC dan garis EG", "0°", "AC sejajar EG, jadi sudutnya 0°."),
             ("antara garis AC dan garis BD", "90°", "Diagonal sisi persegi saling tegak lurus."),
             ("antara garis AF dan garis AC", "60°", "Segitiga AFC sama sisi (semua diagonal sisi), jadi 60°."),
             ("antara bidang ABCD dan bidang ABGH", "45°", "Sudutnya sama dengan sudut antara BC dan BG, yaitu 45°."),
             ("antara garis AE dan bidang ABCD", "90°", "AE tegak lurus bidang ABCD."),
             ("antara garis AB dan garis HG", "0°", "AB sejajar HG."),
             ("antara garis AF dan garis EG", "60°", "AF sejajar DG, dan segitiga DGE sama sisi, jadi 60°.")]
        w, c, e = ch(F)
        return M("Pada kubus ABCD.EFGH, besar sudut %s adalah …" % w + kubus_svg(), c, [o for o in ["0°", "30°", "45°", "60°", "90°", "tan θ = ½√2", "tan θ = √2"] if o != c][:3] if c not in ("0°", "90°") else [o for o in ["45°", "60°", "30°", "90°", "0°"] if o != c][:3], e)

    def kedudukan():
        F = [("garis AB dan garis CD", "sejajar"), ("garis AB dan garis BC", "berpotongan"), ("garis AB dan garis CG", "bersilangan"), ("garis AE dan garis CG", "sejajar"),
             ("garis EF dan garis BC", "bersilangan"), ("garis AC dan garis BD", "berpotongan"), ("garis AH dan garis BG", "sejajar"), ("garis EH dan garis BF", "bersilangan"),
             ("garis DH dan garis FG", "bersilangan"), ("garis AF dan garis BE", "berpotongan"), ("garis EG dan garis BD", "bersilangan"), ("garis AD dan garis FG", "sejajar")]
        w, c = ch(F)
        return M("Pada kubus ABCD.EFGH, kedudukan %s adalah …" % w + kubus_svg(), c, [o for o in ["sejajar", "berpotongan", "bersilangan", "berimpit"] if o != c],
                 "Sejajar: sebidang dan tidak bertemu. Berpotongan: bertemu di satu titik. Bersilangan: tidak sebidang dan tidak bertemu.")

    sets = [("Kedudukan titik, garis, dan bidang", [(kedudukan, 12), (jarak, 8)]),
            ("Jarak pada kubus", [(jarak, 20)]),
            ("Diagonal balok", [(balok, 20)]),
            ("Sudut dalam ruang", [(sudut, 10), (jarak, 10)]),
            ("Campuran", [(balok, 8), (jarak, 12)])]
    return unit("dimensi-tiga", "G", 9, "Dimensi Tiga: Kedudukan, Jarak, dan Sudut dalam Ruang", "Dimensi Tiga",
                "Peserta didik menentukan kedudukan titik, garis, dan bidang dalam ruang, serta menghitung jarak dan sudut pada kubus dan balok.",
                "Latihan dimensi tiga kelas 12 SMA: kedudukan garis (sejajar, berpotongan, bersilangan), jarak titik ke titik, ke garis, dan ke bidang pada kubus, diagonal sisi dan diagonal ruang balok, dan sudut antara garis dan bidang. 100 soal dengan kunci jawaban.",
                "Diagonal ruang kubus = a√3", "Diagonal sisi kubus = a√2.", sets,
                ["Dua garis dalam ruang dapat sejajar, berpotongan, atau bersilangan (tidak sebidang dan tidak bertemu).",
                 "Jarak titik ke garis atau ke bidang adalah panjang ruas garis tegak lurus. Pada kubus berusuk a: diagonal sisi a√2 dan diagonal ruang a√3.",
                 "Diagonal ruang balok p × l × t adalah √(p² + l² + t²). Sudut antara garis dan bidang adalah sudut antara garis itu dan proyeksinya pada bidang."],
                [("Kubus rusuk 6 cm. Jarak A ke G?", ["AG = 6√3"], "6√3 cm"),
                 ("Balok 3 × 4 × 12. Diagonal ruang?", ["√(9 + 16 + 144) = √169"], "13 cm")],
                [["Garis yang tidak bertemu pasti sejajar", "Jika tidak sebidang, garis itu bersilangan"],
                 ["Diagonal ruang kubus a√2", "Diagonal sisi a√2, diagonal ruang a√3"],
                 ["Jarak diukur miring", "Jarak selalu diukur tegak lurus"]],
                [("Apa beda sejajar dan bersilangan?", "Keduanya tidak bertemu, tetapi garis sejajar terletak pada satu bidang, sedangkan garis bersilangan tidak."),
                 ("Bagaimana mencari jarak titik ke bidang?", "Tarik garis dari titik itu tegak lurus ke bidang; panjang garis itu adalah jaraknya."),
                 ("Mengapa diagonal ruang kubus a√3?", "Diagonal sisi a√2 dan rusuk a membentuk segitiga siku-siku: √(2a² + a²) = a√3.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9]
