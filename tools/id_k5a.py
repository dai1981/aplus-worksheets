# -*- coding: utf-8 -*-
"""Indonesia Kelas 5 (Fase C): Bilangan（1〜10）。id_k5.py から使う。"""
import math
from fractions import Fraction as F
import id_k4a as A
from id_k4a import ri, ch, pool, stmt, rel, cap, pie, bar_frac
from id_common import (num, rp, u, NB, mcq, lesson, example, table, wrap, fr, nilai_tempat, bersusun,
                       text, line, INK, GREEN, FILL, RED, BLUE)

G = "kelas-5"


def K():
    return A.K


def R():
    return A.R


def terbilang(n):
    n = int(n)
    if n == 1000000:
        return "satu juta"
    return A.terbilang(n)


def f(a, b):
    return fr(a, b)


def fx(x):
    """Fraction → HTML（帯分数は 2⅓ の形、整数はそのまま）"""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    w, r = divmod(x.numerator, x.denominator)
    if w == 0:
        return f(r, x.denominator)
    return "%d%s" % (w, f(r, x.denominator))


def fw(x):
    """誤答用：正の Fraction だけ"""
    x = F(x)
    return fx(x) if x > 0 else None


def digits_op(a, b, op):
    """桁ごとの計算（繰り上がり・繰り下がりを忘れた答え）"""
    s, m = 0, 1
    while a or b:
        x, y = a % 10, b % 10
        s += ((x + y) % 10 if op == "+" else abs(x - y)) * m
        a //= 10
        b //= 10
        m *= 10
    return s


PL6 = ["satuan", "puluhan", "ratusan", "ribuan", "puluh ribuan", "ratus ribuan"]


def n6(zero=False):
    d = [ri(1, 9)] + [ri(0, 9) for _ in range(5)]
    if zero:
        for _ in range(ri(1, 2)):
            d[ri(1, 5)] = 0
    return int("".join(map(str, d)))


def wrong6(n):
    s = str(n)
    out = []
    for i in range(len(s) - 1):
        t = list(s)
        t[i], t[i + 1] = t[i + 1], t[i]
        t = "".join(t)
        if t[0] != "0" and int(t) != n:
            out.append(int(t))
    for d in (100000, 10000, 1000):
        out.append(n + d if n + d < 1000000 else n - d)
    return out


# ============================================================ 1. bilangan cacah sampai 1.000.000
def u1():
    def baca():
        n = n6(R().random() < 0.5)
        return mcq("Bilangan <b>%s</b> dibaca …" % num(n), cap(terbilang(n)), [cap(terbilang(w)) for w in wrong6(n)],
                   "%s = %s ribu + %s, dibaca %s." % (num(n), terbilang(n // 1000), num(n % 1000), terbilang(n)))

    def tulis():
        n = n6(R().random() < 0.6)
        return mcq("Lambang bilangan dari <i>%s</i> adalah …" % terbilang(n), num(n), [num(w) for w in wrong6(n)],
                   "%s ditulis %s." % (cap(terbilang(n)), num(n)))

    def nilai():
        n = n6()
        s = str(n)
        i = ri(0, 5)
        d = int(s[i])
        if d == 0 or s.count(s[i]) > 1:
            return None
        p = 5 - i
        return mcq("Pada bilangan %s, angka %d bernilai …" % (num(n), d), num(d * 10 ** p),
                   [num(d * 10 ** q) for q in (p - 1, p + 1, p - 2, p + 2) if 0 <= q <= 5],
                   "Angka %d ada di tempat %s, jadi nilainya %s." % (d, PL6[p], num(d * 10 ** p)))

    def tempat():
        n = n6()
        s = str(n)
        i = ri(0, 5)
        if s.count(s[i]) > 1:
            return None
        p = 5 - i
        return mcq("Pada bilangan %s, angka %s menempati tempat …" % (num(n), s[i]), PL6[p],
                   [x for x in pool(PL6) if x != PL6[p]],
                   "Dari kanan: satuan, puluhan, ratusan, ribuan, puluh ribuan, ratus ribuan. Angka %s ada di tempat %s." % (s[i], PL6[p]))

    def panjang():
        n = n6(R().random() < 0.4)
        s = str(n)
        p = [int(d) * 10 ** (5 - i) for i, d in enumerate(s) if d != "0"]
        j = lambda ps: " + ".join(num(x) for x in ps)
        w1 = [x // 10 if i == 1 else x for i, x in enumerate(p)]
        w2 = [x * 10 if i == len(p) - 1 and x < 100000 else x for i, x in enumerate(p)]
        return mcq("Bentuk panjang dari %s adalah …" % num(n), j(p), [j(w1), j(w2), j(p[:-1]) if len(p) > 2 else j(p + [1])],
                   "Tulis nilai setiap angka: %s." % j(p))

    def banding():
        a = n6()
        s = list(str(a))
        i = ri(1, 5)
        s[i] = str((int(s[i]) + ri(1, 8)) % 10)
        b = int("".join(s))
        if R().random() < 0.25:
            b = ri(10000, 99999)
        if a == b:
            return None
        return stmt(num(a), num(b), a, b, "Bandingkan dari angka paling kiri sampai ada yang berbeda. %s %s %s." % (num(a), rel(a, b), num(b)))

    def urut():
        base = ri(1, 9) * 100000 + ri(0, 9) * 10000
        xs = set()
        while len(xs) < 4:
            xs.add(base + ri(0, 9) * 1000 + ri(0, 999))
        xs = sorted(xs)
        up = R().random() < 0.5
        g = sorted(xs, reverse=not up)
        w1 = sorted(xs, reverse=up)
        w2 = list(g)
        w2[1], w2[2] = w2[2], w2[1]
        w3 = list(g)
        w3[0], w3[3] = w3[3], w3[0]
        j = lambda ys: ", ".join(num(y) for y in ys)
        return mcq("Urutan %s dari yang %s adalah …" % (j(pool(xs)), "terkecil" if up else "terbesar"), j(g), [j(w1), j(w2), j(w3)],
                   "Bandingkan ribuan, lalu ratusan, puluhan, satuan. Urutannya %s." % j(g))

    def bulat():
        n = n6()
        p = ch([1000, 10000, 100000])
        nm = {1000: "ribuan", 10000: "puluh ribuan", 100000: "ratus ribuan"}[p]
        r = int(math.floor(n / float(p) + 0.5)) * p
        lo = n // p * p
        hi = lo + p
        wr = [hi if r == lo else lo, r + p if r + p <= 1000000 else r - 2 * p, int(math.floor(n / (p / 10.0) + 0.5)) * p // 10]
        d = (n // (p // 10)) % 10
        return mcq("Hasil pembulatan %s ke %s terdekat adalah …" % (num(n), nm), num(r), [num(x) for x in wr if x != r],
                   "Lihat angka di kanan tempat %s, yaitu %d. %s, jadi hasilnya %s." % (nm, d, "5 atau lebih dibulatkan ke atas" if d >= 5 else "Kurang dari 5 dibulatkan ke bawah", num(r)))

    CT = ["Jumlah penduduk sebuah kota adalah %s jiwa.", "Pada pertandingan final, stadion dikunjungi %s penonton.",
          "Sebuah pabrik roti membuat %s bungkus roti dalam sebulan.", "Panjang jalan tol itu %s meter.",
          "Harga sebuah sepeda motor bekas adalah Rp%s.", "Perpustakaan daerah memiliki %s buku."]

    def cerita():
        n = n6(R().random() < 0.5)
        t = ch(CT) % num(n)
        if R().random() < 0.5:
            return mcq(t + " Bilangan itu dibaca …", cap(terbilang(n)), [cap(terbilang(w)) for w in wrong6(n)], "%s dibaca %s." % (num(n), terbilang(n)))
        p = ch([1000, 10000])
        r = int(math.floor(n / float(p) + 0.5)) * p
        lo = n // p * p
        return mcq(t + " Jika dibulatkan ke %s terdekat, bilangan itu menjadi …" % ("ribuan" if p == 1000 else "puluh ribuan"), num(r),
                   [num(lo + p if r == lo else lo), num(r + p), num(n // 100 * 100)], "Pembulatan %s ke %s terdekat = %s." % (num(n), "ribuan" if p == 1000 else "puluh ribuan", num(r)))

    sets = [("Membaca dan menulis bilangan", [(baca, 10), (tulis, 10)]),
            ("Nilai tempat", [(nilai, 10), (tempat, 6), (panjang, 4)]),
            ("Membandingkan dan mengurutkan", [(banding, 12), (urut, 8)]),
            ("Pembulatan", [(bulat, 20)]),
            ("Soal cerita", [(cerita, 14), (panjang, 6)])]
    body = lesson(
        ["Bilangan sampai 1.000.000 punya tempat ratus ribuan, puluh ribuan, ribuan, ratusan, puluhan, dan satuan.",
         "Baca dalam kelompok tiga angka. 452.307 dibaca <i>empat ratus lima puluh dua ribu tiga ratus tujuh</i>.",
         "Untuk membulatkan, lihat satu angka di kanan tempat yang diminta. 5 atau lebih dibulatkan ke atas, kurang dari 5 ke bawah."],
        [example("Bulatkan 357.482 ke ribuan terdekat.", ["Tempat ribuan: 7", "Angka di kanannya 4 (kurang dari 5)"], "357.000"),
         example("Tulis <i>enam ratus empat ribu lima puluh</i>.", ["604 ribu → 604", "lima puluh → 050"], "604.050")],
        [["604.050 ditulis 6.450 atau 64.050", "Setiap kelompok setelah titik harus 3 angka: 604.050"],
         ["Pembulatan 357.482 ke ribuan menjadi 358.000", "Lihat angka ratusan (4), jadi 357.000"],
         ["Membandingkan dari angka paling kanan", "Mulai dari tempat terbesar di kiri"]],
        table(["Ratus ribuan", "Puluh ribuan", "Ribuan", "Ratusan", "Puluhan", "Satuan"], [["4", "5", "2", "3", "0", "7"]]))
    faq = [{"q": "Bagaimana membaca bilangan enam angka?", "a": "Pisahkan tiga angka dari kanan. Baca kelompok kiri dengan kata ribu, lalu baca kelompok kanan. Contoh: 452.307 = empat ratus lima puluh dua ribu tiga ratus tujuh."},
           {"q": "Bagaimana cara membulatkan ke ribuan terdekat?", "a": "Lihat angka ratusan. Jika 5 atau lebih, angka ribuan ditambah 1. Jika kurang dari 5, angka ribuan tetap. Semua angka di kanannya menjadi 0."},
           {"q": "Berapa banyak nol pada satu juta?", "a": "Satu juta ditulis 1.000.000, ada enam angka nol."}]
    return dict(slug="bilangan-cacah-sampai-1000000", dom="B", sort=1,
                std_text="Murid menunjukkan pemahaman dan intuisi bilangan (number sense) pada bilangan cacah sampai 1.000.000.",
                title="Bilangan Cacah sampai 1.000.000", short_title="Bilangan Cacah sampai 1.000.000",
                meta_desc="Latihan membaca dan menulis bilangan sampai 1.000.000, nilai tempat, membandingkan, mengurutkan, dan pembulatan untuk kelas 5 SD. 100 soal dengan kunci jawaban dan lembar kerja siap cetak.",
                key_big="Baca per tiga angka", key_sub="452.307 = 452 ribu + 307.", body=body, faq=faq, sets=sets)


# ============================================================ 2. penjumlahan dan pengurangan sampai 100.000
def u2():
    def tambah(pic=False):
        def mk():
            a, b = ri(10000, 70000), ri(1000, 29999)
            if a + b > 100000:
                return None
            s = a + b
            w = [digits_op(a, b, "+"), s + 1000, s - 10, s + 100]
            q = ("%s + %s = …" % (num(a), num(b))) if not pic else "Hasil penjumlahan bersusun ini adalah …" + bersusun([str(a), str(b)], "+")
            return mcq(q, num(s), [num(x) for x in w if x != s and x > 0],
                       "Mulai dari satuan. Jika 10 atau lebih, simpan 1 ke tempat berikutnya. %s + %s = %s." % (num(a), num(b), num(s)))
        return mk

    def kurang(pic=False):
        def mk():
            a, b = ri(20000, 99999), ri(1000, 19999)
            d = a - b
            w = [digits_op(a, b, "-"), d + 1000, d + 10, d - 100]
            q = ("%s − %s = …" % (num(a), num(b))) if not pic else "Hasil pengurangan bersusun ini adalah …" + bersusun([str(a), str(b)], "−")
            return mcq(q, num(d), [num(x) for x in w if x != d and x > 0],
                       "Jika angka atas lebih kecil, pinjam 1 dari tempat di kirinya. %s − %s = %s." % (num(a), num(b), num(d)))
        return mk

    def campur():
        a, b, c = ri(10000, 50000), ri(1000, 30000), ri(1000, 20000)
        if a + b > 100000 or a + b - c <= 0:
            return None
        r = a + b - c
        return mcq("%s + %s − %s = …" % (num(a), num(b), num(c)), num(r), [num(a - b + c) if a - b + c > 0 else num(r + 1000), num(a + b + c), num(r - 1000)],
                   "Kerjakan dari kiri: %s + %s = %s, lalu %s − %s = %s." % (num(a), num(b), num(a + b), num(a + b), num(c), num(r)))

    def taksir():
        a, b = ri(11, 69) * 1000 + ri(1, 999), ri(5, 29) * 1000 + ri(1, 999)
        op = ch(["+", "−"])
        ra, rb = int(a / 1000.0 + 0.5) * 1000, int(b / 1000.0 + 0.5) * 1000
        g = ra + rb if op == "+" else ra - rb
        return mcq("Taksiran hasil %s %s %s dengan membulatkan ke ribuan terdekat adalah …" % (num(a), op, num(b)), num(g),
                   [num(g + 1000), num(g - 1000), num(a // 1000 * 1000 + b // 1000 * 1000 if op == "+" else a // 1000 * 1000 - b // 1000 * 1000)],
                   "%s ≈ %s dan %s ≈ %s. %s %s %s = %s." % (num(a), num(ra), num(b), num(rb), num(ra), op, num(rb), num(g)))

    ADD = [("Pada hari Sabtu ada %s pengunjung Taman Mini dan pada hari Minggu %s pengunjung. Berapa jumlah pengunjung kedua hari itu?", "orang"),
           ("Koperasi sekolah menjual %s buku tulis pada semester pertama dan %s buku tulis pada semester kedua. Berapa jumlah buku yang terjual?", "buku"),
           ("Sebuah kebun menghasilkan %s kg jeruk tahun lalu dan %s kg jeruk tahun ini. Berapa jumlah panen kedua tahun?", "kg")]
    SUB = [("Sebuah stadion memiliki %s kursi. Sebanyak %s kursi sudah terisi. Berapa kursi yang masih kosong?", "kursi"),
           ("Pabrik membuat %s botol minum. Sebanyak %s botol sudah dikirim. Berapa botol yang belum dikirim?", "botol"),
           ("Jarak kota A ke kota B %s meter. Pak Andi sudah menempuh %s meter. Berapa meter lagi jarak yang harus ditempuh?", "meter")]

    def cerita():
        if R().random() < 0.5:
            t, un = ch(ADD)
            a, b = ri(10000, 60000), ri(5000, 39000)
            if a + b > 100000:
                return None
            return mcq(t % (num(a), num(b)), u(a + b, un), [u(digits_op(a, b, "+"), un) if digits_op(a, b, "+") != a + b else u(a + b + 100, un), u(a - b if a > b else b - a, un), u(a + b - 1000, un)],
                       "Digabung, jadi dijumlah: %s + %s = %s." % (num(a), num(b), num(a + b)))
        t, un = ch(SUB)
        a, b = ri(30000, 99999), ri(5000, 29999)
        d = a - b
        return mcq(t % (num(a), num(b)), u(d, un), [u(a + b, un) if a + b <= 130000 else u(d + 1000, un), u(digits_op(a, b, "-"), un) if digits_op(a, b, "-") != d else u(d - 100, un), u(d + 10, un)],
                   "Sisa dicari dengan pengurangan: %s − %s = %s." % (num(a), num(b), num(d)))

    sets = [("Penjumlahan", [(tambah(), 12), (tambah(True), 8)]),
            ("Pengurangan", [(kurang(), 12), (kurang(True), 8)]),
            ("Penjumlahan dan pengurangan berurutan", [(campur, 20)]),
            ("Menaksir hasil", [(taksir, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Tulis bilangan bersusun dengan tempat yang lurus: satuan di bawah satuan, ribuan di bawah ribuan.",
         "Mulai dari satuan. Saat menjumlah, simpan 1 jika hasilnya 10 atau lebih. Saat mengurang, pinjam 1 dari tempat di kiri.",
         "Untuk memeriksa, taksir dulu hasilnya dengan membulatkan ke ribuan terdekat."],
        [example("45.678 + 28.546 = …", ["8 + 6 = 14, tulis 4 simpan 1", "7 + 4 + 1 = 12, tulis 2 simpan 1", "6 + 5 + 1 = 12, tulis 2 simpan 1", "5 + 8 + 1 = 14, tulis 4 simpan 1", "4 + 2 + 1 = 7"], "74.224"),
         example("Taksir 38.912 − 12.305.", ["38.912 ≈ 39.000", "12.305 ≈ 12.000"], "sekitar 27.000")],
        [["Lupa menambahkan angka yang disimpan", "Tulis angka simpanan kecil di atas dan jumlahkan"],
         ["Mengurangi angka kecil dari angka besar di setiap tempat", "Pinjam 1 dari kiri jika angka atas lebih kecil"],
         ["Angka tidak lurus menurut tempatnya", "Ratakan dari kanan (satuan)"]])
    faq = [{"q": "Bagaimana menjumlahkan bilangan lima angka?", "a": "Susun ke bawah dengan satuan lurus, lalu jumlahkan dari kanan ke kiri. Jika hasil satu tempat 10 atau lebih, tulis satuannya dan simpan 1."},
           {"q": "Bagaimana memeriksa hasil pengurangan?", "a": "Jumlahkan hasil dengan bilangan pengurang. Hasilnya harus sama dengan bilangan yang dikurangi."},
           {"q": "Apa gunanya menaksir?", "a": "Taksiran membantu mengetahui apakah jawaban masuk akal. Jika hasil hitunganmu jauh dari taksiran, periksa lagi."}]
    return dict(slug="penjumlahan-dan-pengurangan", dom="B", sort=2,
                std_text="Murid melakukan operasi penjumlahan dan pengurangan bilangan cacah sampai 100.000.",
                title="Penjumlahan dan Pengurangan sampai 100.000", short_title="Penjumlahan dan Pengurangan",
                meta_desc="Latihan penjumlahan dan pengurangan bersusun sampai 100.000, operasi berurutan, menaksir hasil, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Lurus menurut tempatnya", key_sub="Mulai dari satuan, simpan atau pinjam 1.", body=body, faq=faq, sets=sets)


# ============================================================ 3. perkalian
def u3():
    def dua_dua():
        a, b = ri(12, 99), ri(12, 99)
        if a % 10 == 0 or b % 10 == 0:
            return None
        p = a * b
        noshift = a * (b // 10) + a * (b % 10)
        return mcq("%d × %d = …" % (a, b), num(p), [num(noshift), num(p + a), num(p - b), num(p + 100)],
                   "%d × %d = %s dan %d × %d = %s. %s + %s = %s." % (a, b % 10, num(a * (b % 10)), a, b // 10 * 10, num(a * (b // 10) * 10),
                                                                   num(a * (b % 10)), num(a * (b // 10) * 10), num(p)))

    def tiga_dua(pic=False):
        def mk():
            a, b = ri(102, 999), ri(12, 99)
            if b % 10 == 0 or a * b > 100000:
                return None
            p = a * b
            noshift = a * (b // 10) + a * (b % 10)
            q = ("%s × %d = …" % (num(a), b)) if not pic else "Hasil perkalian bersusun ini adalah …" + bersusun([str(a), str(b)], "×")
            return mcq(q, num(p), [num(noshift), num(p + a), num(p - 10 * a), num(p + 1000)],
                       "Kalikan dengan satuan lalu dengan puluhan (geser satu tempat): %s + %s = %s." % (num(a * (b % 10)), num(a * (b // 10) * 10), num(p)))
        return mk

    def puluhan():
        a = ri(2, 999)
        k = ch([10, 100, 1000])
        if a * k > 1000000:
            return None
        p = a * k
        z = len(str(k)) - 1
        return mcq("%s × %s = …" % (num(a), num(k)), num(p), [num(p // 10), num(p * 10) if p * 10 <= 10000000 else num(p + k), num(a + k)],
                   "Mengalikan dengan %s berarti menambah %d angka nol: %s." % (num(k), z, num(p)))

    def sifat():
        a = ch([25, 50, 125, 20, 15, 99, 101, 48, 52])
        b = ri(4, 40)
        p = a * b
        if a in (99, 101):
            near = 100
            g = "%d × %d %s %d × %d" % (near, b, "−" if a == 99 else "+", 1, b)
            return mcq("Cara mudah menghitung %d × %d adalah …" % (a, b), g,
                       ["%d × %d + %d" % (near, b, 1), "%d × %d %s %d" % (near, b, "+" if a == 99 else "−", b), "%d + %d" % (a, b)],
                       "%d = %d %s 1, jadi %d × %d = %s %s %d = %s." % (a, near, "−" if a == 99 else "+", a, b, num(near * b), "−" if a == 99 else "+", b, num(p)))
        t, o = b // 10 * 10, b % 10
        if t == 0 or o == 0:
            return None
        g = "%d × %d + %d × %d" % (a, t, a, o)
        return mcq("%d × %d sama dengan …" % (a, b), g, ["%d × %d + %d" % (a, t, o), "%d + %d × %d" % (a, t, o), "%d × %d × %d" % (a, t, o)],
                   "Sifat distributif: %d × (%d + %d) = %d × %d + %d × %d = %s." % (a, t, o, a, t, a, o, num(p)))

    CT = [("Sebuah truk mengangkut %d karung beras. Setiap karung beratnya %d kg. Berapa kg berat semua beras?", "kg"),
          ("Sebuah gedung pertunjukan punya %d baris kursi. Setiap baris ada %d kursi. Berapa banyak kursi seluruhnya?", "kursi"),
          ("Pabrik membuat %d kotak permen setiap hari. Berapa kotak yang dibuat dalam %d hari?", "kotak"),
          ("Ada %d kardus buku. Setiap kardus berisi %d buku. Berapa banyak buku seluruhnya?", "buku"),
          ("Satu lembar karton berisi %d stiker. Berapa banyak stiker pada %d lembar karton?", "stiker")]

    def cerita():
        t, un = ch(CT)
        a, b = ri(24, 480), ri(12, 75)
        if a * b > 100000:
            return None
        p = a * b
        return mcq(t % (a, b), u(p, un), [u(a + b, un), u(a * (b // 10) + a * (b % 10), un), u(p + a, un)], "%d × %d = %s." % (a, b, num(p)))

    sets = [("Dua angka × dua angka", [(dua_dua, 20)]),
            ("Tiga angka × dua angka", [(tiga_dua(), 14), (tiga_dua(True), 6)]),
            ("Dikali 10, 100, dan 1.000", [(puluhan, 20)]),
            ("Sifat perkalian", [(sifat, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Kalikan dulu dengan angka satuan, lalu dengan angka puluhan. Hasil dengan puluhan ditulis bergeser satu tempat ke kiri (ada nol di belakang).",
         "Jumlahkan kedua hasil itu.",
         "Mengalikan dengan 10, 100, atau 1.000 cukup menambah 1, 2, atau 3 angka nol."],
        [example("234 × 26 = …", ["234 × 6 = 1.404", "234 × 20 = 4.680", "1.404 + 4.680"], "6.084"),
         example("25 × 36 = …", ["25 × 30 + 25 × 6", "750 + 150"], "900")],
        [["Hasil kali puluhan tidak digeser (234 × 2 = 468 lalu 1.404 + 468)", "234 × 20 = 4.680, tulis nol di satuan"],
         ["Lupa menambahkan simpanan", "Tulis angka simpanan kecil di atas"],
         ["35 × 100 = 350", "35 × 100 = 3.500 (dua angka nol)"]])
    faq = [{"q": "Bagaimana cara perkalian bersusun dua angka?", "a": "Kalikan bilangan atas dengan satuan, lalu dengan puluhan (hasilnya bergeser satu tempat). Jumlahkan kedua hasil."},
           {"q": "Apa itu sifat distributif?", "a": "Perkalian dapat dipecah: a × (b + c) = a × b + a × c. Contoh: 25 × 36 = 25 × 30 + 25 × 6."},
           {"q": "Bagaimana memeriksa hasil perkalian?", "a": "Taksir dengan membulatkan. 234 × 26 kira-kira 200 × 30 = 6.000, jadi 6.084 masuk akal."}]
    return dict(slug="perkalian", dom="B", sort=3,
                std_text="Murid melakukan operasi perkalian bilangan cacah sampai 100.000.",
                title="Perkalian Bersusun", short_title="Perkalian",
                meta_desc="Latihan perkalian dua angka dan tiga angka dengan dua angka, perkalian dengan 10, 100, dan 1.000, sifat perkalian, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Satuan dulu, lalu puluhan", key_sub="Hasil kali puluhan digeser satu tempat.", body=body, faq=faq, sets=sets)


# ============================================================ 4. pembagian
def u4():
    def satu():
        b = ri(2, 9)
        q = ri(102, 9999 // b)
        n = q * b
        zq = int(str(q).replace("0", "")) if "0" in str(q) else q + 10
        return mcq("%s : %d = …" % (num(n), b), num(q), [num(zq), num(q + 1), num(q - 10) if q > 10 else num(q + 2), num(q * 10)],
                   "Bagi mulai dari angka paling kiri. Periksa: %s × %d = %s." % (num(q), b, num(n)))

    def dua():
        b = ri(11, 49)
        q = ri(12, 99999 // b if b * 12 < 100000 else 12)
        n = q * b
        if n > 100000 or q > 999:
            return None
        return mcq("%s : %d = …" % (num(n), b), num(q), [num(q + 1), num(q - 1), num(q * 10) if q < 100 else num(q + 10), num(q // 10) if q >= 100 else num(q + 2)],
                   "Periksa dengan perkalian: %s × %d = %s." % (num(q), b, num(n)))

    def sisa():
        b = ri(3, 25)
        q = ri(12, 400)
        r = ri(1, b - 1)
        n = q * b + r
        return mcq("%s : %d = %d sisa …" % (num(n), b, q), str(r), [str(r + 1), str(b - r) if b - r != r else str(r + 2), str(b + r)],
                   "%d × %d = %s, dan %s − %s = %d." % (q, b, num(q * b), num(n), num(q * b), r))

    def nol():
        k = ch([10, 100, 1000])
        q = ri(2, 900)
        n = q * k
        if n > 100000:
            return None
        return mcq("%s : %s = …" % (num(n), num(k)), num(q), [num(q * 10), num(q // 10) if q >= 10 else num(q + 1), num(n - k)],
                   "Membagi dengan %s berarti menghapus %d angka nol: %s." % (num(k), len(str(k)) - 1, num(q)))

    def hubung():
        a, b = ri(12, 99), ri(12, 99)
        p = a * b
        return mcq("Jika %d × %d = %s, maka %s : %d = …" % (a, b, num(p), num(p), a), str(b), [str(a), num(p - a), str(b + 1)],
                   "Pembagian adalah kebalikan perkalian: %s : %d = %d." % (num(p), a, b))

    CT = ["Sebanyak %s buku dibagikan sama banyak ke %d sekolah. Berapa buku yang diterima setiap sekolah?",
          "Ada %s kg beras dimasukkan ke karung. Setiap karung berisi %d kg. Berapa karung yang diperlukan?",
          "Sebanyak %s siswa ikut upacara dan berbaris dalam %d barisan sama panjang. Berapa siswa di setiap barisan?",
          "Pak Karel memanen %s butir telur dan memasukkannya ke kotak berisi %d butir. Berapa kotak yang terisi penuh?"]

    def cerita():
        t = ch(CT)
        b = ri(6, 30)
        q = ri(15, 400)
        n = q * b
        if n > 100000:
            return None
        if "terisi penuh" in t and R().random() < 0.5:
            r = ri(1, b - 1)
            n += r
            return mcq(t % (num(n), b), str(q), [str(q + 1), str(r), num(n - b)], "%s : %d = %d sisa %d. Kotak yang penuh ada %d." % (num(n), b, q, r, q))
        return mcq(t % (num(n), b), num(q), [num(q + 1), num(n - b), num(q * 10)], "%s : %d = %s." % (num(n), b, num(q)))

    sets = [("Dibagi bilangan satu angka", [(satu, 20)]),
            ("Dibagi bilangan dua angka", [(dua, 14), (hubung, 6)]),
            ("Pembagian bersisa", [(sisa, 20)]),
            ("Dibagi 10, 100, dan 1.000", [(nol, 12), (hubung, 8)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Pembagian bersusun (porogapit) dimulai dari angka paling kiri. Bagi, kalikan, kurangkan, lalu turunkan angka berikutnya.",
         "Jika angka yang diturunkan lebih kecil dari pembagi, tulis 0 di hasil bagi.",
         "Periksa jawaban: hasil bagi × pembagi + sisa = bilangan yang dibagi."],
        [example("4.230 : 6 = …", ["42 : 6 = 7", "3 : 6 = 0 (tulis 0)", "30 : 6 = 5"], "705"),
         example("1.250 : 25 = …", ["125 : 25 = 5", "0 : 25 = 0"], "50")],
        [["4.230 : 6 = 75 (lupa angka 0)", "Jika tidak bisa dibagi, tulis 0: 705"],
         ["Sisa lebih besar dari pembagi", "Sisa harus lebih kecil dari pembagi"],
         ["Tidak memeriksa jawaban", "Hasil bagi × pembagi + sisa harus kembali ke bilangan awal"]])
    faq = [{"q": "Apa itu porogapit?", "a": "Porogapit adalah cara pembagian bersusun ke bawah. Kita membagi angka demi angka dari kiri, lalu menurunkan angka berikutnya."},
           {"q": "Kapan hasil bagi memiliki angka 0 di tengah?", "a": "Jika setelah menurunkan angka, bilangannya lebih kecil dari pembagi. Tulis 0 di hasil bagi lalu turunkan angka berikutnya."},
           {"q": "Bagaimana memeriksa pembagian bersisa?", "a": "Kalikan hasil bagi dengan pembagi lalu tambahkan sisa. Contoh: 47 : 5 = 9 sisa 2, periksa 9 × 5 + 2 = 47."}]
    return dict(slug="pembagian", dom="B", sort=4,
                std_text="Murid melakukan operasi pembagian bilangan cacah sampai 100.000.",
                title="Pembagian Bersusun (Porogapit)", short_title="Pembagian",
                meta_desc="Latihan pembagian dengan bilangan satu dan dua angka, pembagian bersisa, dibagi 10, 100, dan 1.000, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Bagi, kali, kurang, turunkan", key_sub="Periksa: hasil bagi × pembagi + sisa.", body=body, faq=faq, sets=sets)


# ============================================================ 5. KPK dan FPB
def pf(n):
    out, d = [], 2
    while n > 1:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    return out


def pf_txt(n):
    ps = pf(n)
    parts = []
    for p in sorted(set(ps)):
        k = ps.count(p)
        parts.append("%d<sup>%d</sup>" % (p, k) if k > 1 else str(p))
    return " × ".join(parts)


def u5():
    def faktorisasi():
        n = ch([x for x in range(12, 201) if len(pf(x)) >= 3])
        g = pf_txt(n)
        ps = pf(n)
        w1 = " × ".join(map(str, sorted(set(ps))))
        w2 = pf_txt(n * 2)
        w3 = pf_txt(n // ps[0] * (ps[0] + 1)) if (ps[0] + 1) in (3, 5, 7) and n // ps[0] * (ps[0] + 1) != n else pf_txt(n * 3)
        return mcq("Faktorisasi prima dari %d adalah …" % n, g, [w1, w2, w3], "%d = %s = %s." % (n, " × ".join(map(str, ps)), g))

    def prima():
        g = ch([p for p in range(11, 98) if len(pf(p)) == 1])
        bad = R().sample([x for x in range(11, 99) if len(pf(x)) > 1 and x % 2 == 1], 3)
        xs = sorted([g] + bad)
        return mcq("Di antara bilangan %s, manakah yang merupakan bilangan prima?" % ", ".join(map(str, xs)), str(g), [str(b) for b in bad],
                   "%d hanya punya dua faktor, yaitu 1 dan %d." % (g, g))

    def pasangan():
        a, b = R().sample(range(4, 61), 2)
        if math.gcd(a, b) in (1, a, b):
            return None
        return a, b

    def kpk():
        p = pasangan()
        if not p:
            return None
        a, b = p
        l = a * b // math.gcd(a, b)
        return mcq("KPK dari %d dan %d adalah …" % (a, b), num(l), [num(a * b) if a * b != l else num(l * 2), str(math.gcd(a, b)), num(l + max(a, b))],
                   "Kelipatan persekutuan terkecil dari %d dan %d adalah %d." % (a, b, l))

    def fpb():
        p = pasangan()
        if not p:
            return None
        a, b = p
        g = math.gcd(a, b)
        l = a * b // g
        fs = [d for d in range(2, min(a, b) + 1) if a % d == 0 and b % d == 0 and d != g]
        return mcq("FPB dari %d dan %d adalah …" % (a, b), str(g), [num(l), str(fs[0]) if fs else str(g + 1), str(min(a, b)) if min(a, b) != g else str(g * 2)],
                   "Faktor persekutuan terbesar dari %d dan %d adalah %d." % (a, b, g))

    def dari_pf():
        a, b = pasangan() or (12, 18)
        g, l = math.gcd(a, b), a * b // math.gcd(a, b)
        which = R().random() < 0.5
        return mcq("%d = %s dan %d = %s. %s dari %d dan %d adalah …" % (a, pf_txt(a), b, pf_txt(b), "KPK" if which else "FPB", a, b),
                   num(l if which else g), [num(g if which else l), num(a * b) if a * b not in (g, l) else num(l + 1), str(max(a, b))],
                   ("KPK: ambil semua faktor prima dengan pangkat terbesar = %d." % l) if which else ("FPB: ambil faktor prima yang sama dengan pangkat terkecil = %d." % g))

    def cerita_kpk():
        a, b = R().sample([2, 3, 4, 5, 6, 8, 9, 10, 12, 15], 2)
        l = a * b // math.gcd(a, b)
        if l in (a, b) or l > 60:
            return None
        x, y = K().two()
        what = ch(["berenang", "ke perpustakaan", "bermain bulu tangkis", "les menari", "menjenguk nenek"])
        return mcq("%s %s setiap %d hari sekali, dan %s setiap %d hari sekali. Hari ini mereka %s bersama. Berapa hari lagi mereka akan %s bersama lagi?" % (x, what, a, y, b, what, what),
                   "%d hari" % l, ["%d hari" % (a * b) if a * b != l else "%d hari" % (l * 2), "%d hari" % (a + b), "%d hari" % math.gcd(a, b) if math.gcd(a, b) > 1 else "%d hari" % (l - 1)],
                   "Cari KPK dari %d dan %d, yaitu %d." % (a, b, l))

    def cerita_fpb():
        g = ri(3, 12)
        a, b = g * ri(2, 9), g * ri(2, 9)
        if a == b or math.gcd(a, b) != g:
            return None
        A_, B_ = ch([("buku tulis", "pensil"), ("jeruk", "apel"), ("kue lapis", "kue lumpur"), ("kelereng merah", "kelereng biru")])
        return mcq("Bu Tini punya %d %s dan %d %s. Semua akan dibagikan ke beberapa bingkisan dengan isi yang sama banyak. Paling banyak berapa bingkisan yang dapat dibuat?" % (a, A_, b, B_),
                   "%d bingkisan" % g, ["%d bingkisan" % (a * b // g), "%d bingkisan" % (a + b), "%d bingkisan" % min(a // g, b // g) if min(a // g, b // g) != g else "%d bingkisan" % (g + 1)],
                   "Cari FPB dari %d dan %d, yaitu %d. Setiap bingkisan berisi %d %s dan %d %s." % (a, b, g, a // g, A_, b // g, B_))

    sets = [("Bilangan prima dan faktorisasi", [(prima, 6), (faktorisasi, 14)]),
            ("KPK", [(kpk, 20)]),
            ("FPB", [(fpb, 20)]),
            ("KPK dan FPB dengan faktorisasi prima", [(dari_pf, 20)]),
            ("Soal cerita", [(cerita_kpk, 10), (cerita_fpb, 10)])]
    body = lesson(
        ["Bilangan prima hanya punya dua faktor: 1 dan bilangan itu sendiri (2, 3, 5, 7, 11, …).",
         "Faktorisasi prima menulis bilangan sebagai perkalian bilangan prima: 24 = 2<sup>3</sup> × 3.",
         "KPK: ambil semua faktor prima dengan pangkat terbesar. FPB: ambil faktor prima yang sama dengan pangkat terkecil."],
        [example("KPK dan FPB dari 12 dan 18.", ["12 = 2<sup>2</sup> × 3, 18 = 2 × 3<sup>2</sup>", "KPK = 2<sup>2</sup> × 3<sup>2</sup> = 36", "FPB = 2 × 3 = 6"], "KPK 36, FPB 6"),
         example("Lampu A berkedip setiap 4 detik, lampu B setiap 6 detik. Kapan berkedip bersama lagi?", ["KPK dari 4 dan 6"], "12 detik lagi")],
        [["Tertukar KPK dan FPB", "KPK ≥ bilangan terbesar, FPB ≤ bilangan terkecil"],
         ["KPK dihitung dengan mengalikan kedua bilangan", "4 × 6 = 24, padahal KPK 4 dan 6 adalah 12"],
         ["1 dianggap bilangan prima", "1 bukan bilangan prima (faktornya hanya satu)"]])
    faq = [{"q": "Kapan memakai KPK dalam soal cerita?", "a": "Saat mencari kapan dua kejadian yang berulang terjadi bersamaan lagi, misalnya jadwal atau lampu yang berkedip."},
           {"q": "Kapan memakai FPB dalam soal cerita?", "a": "Saat membagi beberapa jenis benda ke kelompok sebanyak mungkin dengan isi yang sama, misalnya bingkisan atau barisan."},
           {"q": "Bagaimana mencari faktorisasi prima?", "a": "Bagi terus dengan bilangan prima terkecil (2, 3, 5, …) sampai hasilnya 1. Contoh: 60 = 2 × 2 × 3 × 5 = 2² × 3 × 5."}]
    return dict(slug="kpk-dan-fpb", dom="B", sort=5,
                std_text="Murid dapat menyelesaikan masalah yang berkaitan dengan KPK dan FPB.",
                title="KPK dan FPB", short_title="KPK dan FPB",
                meta_desc="Latihan bilangan prima, faktorisasi prima, KPK, FPB, dan soal cerita KPK dan FPB untuk kelas 5 SD. 100 soal dengan kunci jawaban dan lembar kerja siap cetak.",
                key_big="KPK: pangkat terbesar, FPB: terkecil", key_sub="Mulai dengan faktorisasi prima.", body=body, faq=faq, sets=sets)


# ============================================================ 6. pecahan campuran
def u6():
    def ke_campur():
        b = ri(2, 12)
        w = ri(1, 9)
        a = ri(1, b - 1)
        if math.gcd(a, b) != 1:
            return None
        n = w * b + a
        return mcq("Pecahan %s jika diubah ke pecahan campuran adalah …" % f(n, b), fx(F(n, b)),
                   ["%d%s" % (a, f(w, b)) if w < b else None, "%d%s" % (w + 1, f(a, b)), "%d%s" % (w, f(b - a, b)) if b - a != a else "%d%s" % (w, f(a, b + 1)), "%d%s" % (w - 1 if w > 1 else w + 2, f(a, b))],
                   "%d : %d = %d sisa %d, jadi %s = %s." % (n, b, w, a, f(n, b), fx(F(n, b))))

    def ke_biasa():
        b = ri(2, 12)
        w = ri(1, 9)
        a = ri(1, b - 1)
        n = w * b + a
        return mcq("Pecahan %s jika diubah ke pecahan biasa adalah …" % fx(F(n, b)), f(n, b),
                   [f(w + a, b), f(w * a + b, b), f(w * b, a) if w * b != n else f(n + 1, b), f(n - 1, b)],
                   "%d × %d + %d = %d, jadi %s = %s." % (w, b, a, n, fx(F(n, b)), f(n, b)))

    def gambar():
        b = ch([2, 3, 4, 6, 8])
        w = ri(1, 3)
        a = ri(1, b - 1)
        pics = "".join(pie(b, b, r=34) for _ in range(w)) + pie(b, a, r=34)
        pics = pics.replace("</div><div class='qfig'>", "")
        return mcq("Bagian yang diarsir pada gambar adalah …" + pics, fx(F(w * b + a, b)),
                   ["%d%s" % (w + 1, f(a, b)), f(a, b), "%d%s" % (w, f(b - a, b)) if b - a != a else "%d%s" % (w, f(a, b * 2)), f(w * b + a, b * (w + 1))],
                   "Ada %d lingkaran penuh dan %s lingkaran: %s." % (w, f(a, b), fx(F(w * b + a, b))))

    def banding():
        a, b = R().sample(range(2, 13), 2)
        p, q = ri(1, a - 1), ri(1, b - 1)
        x, y = F(p, a), F(q, b)
        if x == y:
            return None
        l = a * b // math.gcd(a, b)
        return stmt(f(p, a), f(q, b), x, y, "Samakan penyebut menjadi %d: %s dan %s." % (l, f(p * l // a, l), f(q * l // b, l)))

    def banding_campur():
        w = ri(1, 5)
        a, b = R().sample(range(2, 10), 2)
        p, q = ri(1, a - 1), ri(1, b - 1)
        x, y = w + F(p, a), F(w * b + q, b)
        if x == y:
            return None
        return stmt(fx(x), f(w * b + q, b), x, y, "Ubah ke bentuk yang sama: %s = %s." % (f(w * b + q, b), fx(y)))

    def urut():
        d = ch([6, 8, 10, 12])
        ds = [x for x in (2, 3, 4, 5, 6, 8, 10, 12) if d % x == 0]
        xs = set()
        while len(xs) < 4:
            b = ch(ds)
            xs.add(F(ri(1, 2 * b - 1), b))
        xs = sorted(xs)
        if len(set(xs)) < 4:
            return None
        up = R().random() < 0.5
        g = sorted(xs, reverse=not up)
        j = lambda ys: ", ".join(fx(y) for y in ys)
        w2 = list(g)
        w2[0], w2[1] = w2[1], w2[0]
        w3 = sorted(xs, key=lambda z: (z.denominator, z.numerator), reverse=not up)
        return mcq("Urutan pecahan %s dari yang %s adalah …" % (j(pool(xs)), "terkecil" if up else "terbesar"), j(g),
                   [j(sorted(xs, reverse=up)), j(w2), j(w3), j(list(reversed(w2)))], "Samakan penyebut menjadi %d, lalu bandingkan pembilangnya." % d)

    def cerita():
        x, y = K().two()
        a, b = R().sample([2, 3, 4, 5, 6, 8], 2)
        p, q = ri(1, a - 1), ri(1, b - 1)
        X, Y = F(1, 1) + F(p, a), F(1, 1) + F(q, b)
        if X == Y:
            return None
        what = ch(["liter jus", "kg tepung", "meter pita", "jam belajar"])
        win = x if X > Y else y
        return mcq("%s memakai %s %s, sedangkan %s memakai %s %s. Siapa yang memakai lebih banyak?" % (x, fx(X), what, y, fx(Y), what),
                   win, [y if win == x else x, "Sama banyak", "Tidak dapat ditentukan"],
                   "Bagian utuhnya sama (1). Bandingkan %s dan %s." % (fx(X - 1), fx(Y - 1)))

    sets = [("Pecahan biasa ke campuran", [(ke_campur, 14), (gambar, 6)]),
            ("Pecahan campuran ke biasa", [(ke_biasa, 14), (gambar, 6)]),
            ("Membandingkan pecahan", [(banding, 20)]),
            ("Pecahan campuran dan urutan", [(banding_campur, 10), (urut, 10)]),
            ("Soal cerita", [(cerita, 14), (urut, 6)])]
    body = lesson(
        ["Pecahan campuran terdiri dari bilangan utuh dan pecahan, misalnya 2" + f(1, 3) + ".",
         "Pecahan biasa ke campuran: bagi pembilang dengan penyebut. Hasil bagi = bilangan utuh, sisa = pembilang baru.",
         "Untuk membandingkan pecahan dengan penyebut berbeda, samakan dulu penyebutnya."],
        [example("Ubah %s ke pecahan campuran." % f(17, 5), ["17 : 5 = 3 sisa 2"], "3" + f(2, 5)),
         example("Bandingkan %s dan %s." % (f(3, 4), f(5, 6)), ["Penyebut 12: %s dan %s" % (f(9, 12), f(10, 12))], "%s &lt; %s" % (f(3, 4), f(5, 6)))],
        [["2%s = %s (2 + 1 = 3)" % (f(1, 3), f(3, 3)), "2 × 3 + 1 = 7, jadi %s" % f(7, 3)],
         ["Membandingkan penyebut saja", "Samakan penyebut, lalu bandingkan pembilang"],
         ["%s diubah menjadi 2%s" % (f(17, 5), f(7, 5)), "Sisa harus lebih kecil dari penyebut: 3%s" % f(2, 5)]])
    faq = [{"q": "Apa itu pecahan campuran?", "a": "Pecahan yang terdiri dari bilangan bulat dan pecahan biasa, misalnya 1 3/4. Nilainya lebih dari 1."},
           {"q": "Bagaimana mengubah pecahan campuran ke pecahan biasa?", "a": "Kalikan bilangan bulat dengan penyebut, tambahkan pembilang, lalu tulis di atas penyebut yang sama. 2 3/5 = (2 × 5 + 3)/5 = 13/5."},
           {"q": "Bagaimana membandingkan pecahan berpenyebut berbeda?", "a": "Samakan penyebutnya dengan KPK kedua penyebut, lalu bandingkan pembilangnya."}]
    return dict(slug="pecahan-campuran", dom="B", sort=6,
                std_text="Murid dapat membandingkan dan mengurutkan berbagai pecahan termasuk pecahan campuran, serta mengubah pecahan menjadi berbagai bentuk pecahan lain.",
                title="Pecahan Campuran dan Membandingkan Pecahan", short_title="Pecahan Campuran",
                meta_desc="Latihan mengubah pecahan biasa ke pecahan campuran dan sebaliknya, membandingkan dan mengurutkan pecahan berpenyebut berbeda, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="17/5 = 3 2/5", key_sub="Samakan penyebut sebelum membandingkan.", body=body, faq=faq, sets=sets)


# ============================================================ 7. penjumlahan dan pengurangan pecahan
def u7():
    DN = [2, 3, 4, 5, 6, 8, 9, 10, 12]

    def sama():
        b = ri(4, 12)
        a, c = ri(1, b - 1), ri(1, b - 1)
        add = R().random() < 0.5
        if not add and a <= c:
            a, c = c, a
        if a == c:
            return None
        r = F(a, b) + F(c, b) if add else F(a, b) - F(c, b)
        op = "+" if add else "−"
        return mcq("%s %s %s = …" % (f(a, b), op, f(c, b)), fx(r),
                   [fw(F(a + c if add else a - c, 2 * b)), fw(r + F(1, b)), fw(r - F(1, b)), f(a + c if add else a - c, b) if fx(r) != f(a + c if add else a - c, b) else fw(r * 2)],
                   "Penyebut sama, jadi %s pembilangnya: %s%s." % ("jumlahkan" if add else "kurangkan", f(a + c if add else a - c, b), "" if fx(r) == f(a + c if add else a - c, b) else " = " + fx(r)))

    def beda():
        b, d = R().sample(DN, 2)
        a, c = ri(1, b - 1), ri(1, d - 1)
        add = R().random() < 0.5
        x, y = F(a, b), F(c, d)
        if not add and x <= y:
            x, y, a, b, c, d = y, x, c, d, a, b
        r = x + y if add else x - y
        if r == 0:
            return None
        l = b * d // math.gcd(b, d)
        op = "+" if add else "−"
        naive = F(a + c, b + d) if add else (F(a - c, abs(b - d)) if a > c and b != d else None)
        return mcq("%s %s %s = …" % (f(a, b), op, f(c, d)), fx(r), [fw(naive) if naive else None, fw(r + F(1, l)), fw(r - F(1, l)), fw(r * 2), fw(F(r.numerator + 1, r.denominator))],
                   "Samakan penyebut menjadi %d: %s %s %s = %s." % (l, f(a * l // b, l), op, f(c * l // d, l), fx(r)))

    def campur():
        w1, w2 = ri(1, 5), ri(1, 4)
        b, d = R().sample([2, 3, 4, 5, 6, 8], 2)
        a, c = ri(1, b - 1), ri(1, d - 1)
        x, y = w1 + F(a, b), w2 + F(c, d)
        add = R().random() < 0.5
        if not add and x <= y:
            x, y = y, x
        r = x + y if add else x - y
        op = "+" if add else "−"
        whole = (int(x) + int(y)) if add else (int(x) - int(y))
        frac = (x - int(x)) + (y - int(y)) if add else (x - int(x)) - (y - int(y))
        return mcq("%s %s %s = …" % (fx(x), op, fx(y)), fx(r), [fw(r + 1), fw(r - 1) if r > 1 else fw(r + 2), fw(whole + abs(frac)) if fw(whole + abs(frac)) != fx(r) else fw(r + F(1, 2)), fw(r + F(1, b * d))],
                   "Hitung bilangan utuh dan pecahannya, atau ubah ke pecahan biasa dulu. Hasilnya %s." % fx(r))

    CT = [("Ibu membeli %s kg gula pasir dan %s kg gula merah. Berapa kg gula yang dibeli Ibu?", "+", "kg"),
          ("Panjang pita %s m. Sepanjang %s m dipakai untuk hiasan. Berapa m sisa pita?", "−", "m"),
          ("Kakak minum %s liter air pagi hari dan %s liter siang hari. Berapa liter air yang diminum Kakak?", "+", "liter"),
          ("Sebuah kebun ditanami jagung %s bagian dan cabai %s bagian. Berapa bagian kebun yang ditanami?", "+", "bagian"),
          ("Persediaan minyak %s liter. Sebanyak %s liter dipakai untuk menggoreng. Berapa liter sisa minyak?", "−", "liter")]

    def cerita():
        t, op, un = ch(CT)
        b, d = R().sample([2, 3, 4, 5, 6, 8, 10], 2)
        if un == "bagian":
            a, c = ri(1, b - 1), ri(1, d - 1)
            x, y = F(a, b), F(c, d)
            if x + y >= 1:
                return None
        else:
            x, y = ri(1, 3) + F(ri(1, b - 1), b), F(ri(1, d - 1), d) + ri(0, 2)
        if op == "−" and x <= y:
            x, y = y, x
        r = x + y if op == "+" else x - y
        return mcq(t % (fx(x), fx(y)), "%s %s" % (fx(r), un), ["%s %s" % (s, un) for s in [fw(x - y if op == "+" else x + y), fw(r + F(1, 2)), fw(r + 1), fw(r - F(1, 4))] if s],
                   "%s %s %s = %s." % (fx(x), op, fx(y), fx(r)))

    sets = [("Penyebut sama", [(sama, 20)]),
            ("Penyebut berbeda", [(beda, 20)]),
            ("Penyebut berbeda lagi", [(beda, 20)]),
            ("Pecahan campuran", [(campur, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Jika penyebutnya sama, jumlahkan atau kurangkan pembilangnya saja. Penyebutnya tetap.",
         "Jika penyebutnya berbeda, samakan dulu penyebutnya dengan KPK.",
         "Untuk pecahan campuran, hitung bilangan utuh dan pecahannya, atau ubah ke pecahan biasa. Tulis hasil dalam bentuk paling sederhana."],
        [example("%s + %s = …" % (f(2, 3), f(1, 4)), ["KPK 3 dan 4 = 12", "%s + %s = %s" % (f(8, 12), f(3, 12), f(11, 12))], f(11, 12)),
         example("3%s − 1%s = …" % (f(1, 2), f(3, 4)), ["%s − %s" % (f(7, 2), f(7, 4)), "%s − %s = %s" % (f(14, 4), f(7, 4), f(7, 4))], "1" + f(3, 4))],
        [["%s + %s = %s" % (f(1, 2), f(1, 3), f(2, 5)), "Samakan penyebut: %s + %s = %s" % (f(3, 6), f(2, 6), f(5, 6))],
         ["Penyebut ikut dijumlahkan", "Penyebut tetap, hanya pembilang yang dijumlah"],
         ["Hasil tidak disederhanakan", "Bagi pembilang dan penyebut dengan FPB-nya"]])
    faq = [{"q": "Mengapa penyebut harus disamakan?", "a": "Karena kita hanya bisa menjumlahkan bagian-bagian yang sama besar. Sepertiga dan seperempat harus diubah menjadi perdua belas dulu."},
           {"q": "Bagaimana mengurangkan pecahan campuran jika pecahannya kurang?", "a": "Ubah kedua pecahan campuran ke pecahan biasa, lalu kurangkan. Atau pinjam 1 dari bilangan utuh."},
           {"q": "Apakah hasil harus disederhanakan?", "a": "Ya. Tulis hasil dalam bentuk paling sederhana, dan ubah ke pecahan campuran jika lebih dari 1."}]
    return dict(slug="penjumlahan-dan-pengurangan-pecahan", dom="B", sort=7,
                std_text="Murid dapat melakukan operasi penjumlahan dan pengurangan pecahan, termasuk pecahan berpenyebut berbeda dan pecahan campuran.",
                title="Penjumlahan dan Pengurangan Pecahan", short_title="Penjumlahan dan Pengurangan Pecahan",
                meta_desc="Latihan penjumlahan dan pengurangan pecahan berpenyebut sama dan berbeda, pecahan campuran, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Samakan penyebutnya dulu", key_sub="Penyebut tetap, pembilang dijumlah atau dikurang.", body=body, faq=faq, sets=sets)


# ============================================================ 8. perkalian dan pembagian pecahan dengan bilangan asli
def u8():
    def kali():
        b = ri(2, 12)
        a = ri(1, b - 1)
        n = ri(2, 9)
        r = F(a, b) * n
        if R().random() < 0.5:
            q = "%s × %d = …" % (f(a, b), n)
        else:
            q = "%d × %s = …" % (n, f(a, b))
        return mcq(q, fx(r), [fw(F(a * n, b * n)), fw(F(a, b * n)), fw(F(a + n, b)), fw(r + 1)],
                   "Kalikan pembilang dengan %d: %s = %s." % (n, f(a * n, b), fx(r)))

    def dari():
        b = ch([2, 3, 4, 5, 6, 8, 10])
        a = ri(1, b - 1)
        n = b * ri(2, 12)
        r = n * a // b
        what = ch(["siswa", "kelereng", "buku", "telur", "rupiah"])
        if what == "rupiah":
            n *= 1000
            r = n * a // b
            return mcq("%s dari Rp%s adalah …" % (f(a, b), num(n)), "Rp" + num(r), ["Rp" + num(n // b), "Rp" + num(n - r) if n - r != r else "Rp" + num(r + 1000), "Rp" + num(n * a)],
                       "Rp%s : %d × %d = Rp%s." % (num(n), b, a, num(r)))
        return mcq("%s dari %d %s adalah …" % (f(a, b), n, what), "%d %s" % (r, what), ["%d %s" % (x, what) for x in (n // b, n - r, n * a, r + a) if x != r],
                   "%d : %d = %d, lalu × %d = %d." % (n, b, n // b, a, r))

    def bagi():
        b = ri(2, 10)
        a = ri(1, b - 1)
        n = ri(2, 6)
        r = F(a, b) / n
        return mcq("%s : %d = …" % (f(a, b), n), fx(r), [fw(F(a * n, b)), fw(F(a, b + n)), fw(F(a, n)), fw(r * 2)],
                   "Membagi dengan %d sama dengan mengalikan dengan %s: %s × %s = %s." % (n, f(1, n), f(a, b), f(1, n), fx(r)))

    def bagi_asli():
        n = ri(2, 9)
        b = ri(2, 6)
        r = n * b
        return mcq("%d : %s = …" % (n, f(1, b)), str(r), [fw(F(n, b)), str(n + b), str(r + n)],
                   "Berapa banyak %s dalam %d? Setiap 1 ada %d bagian, jadi %d × %d = %d." % (f(1, b), n, b, n, b, r))

    def campur():
        w = ri(1, 4)
        b = ri(2, 6)
        a = ri(1, b - 1)
        n = ri(2, 5)
        x = w + F(a, b)
        r = x * n
        return mcq("%s × %d = …" % (fx(x), n), fx(r), [fw(w * n + F(a, b)), fw(w + F(a * n, b)) if fw(w + F(a * n, b)) != fx(r) else fw(r + 1), fw(r - 1), fw(r + F(1, b))],
                   "Ubah ke pecahan biasa: %s × %d = %s = %s." % (f(w * b + a, b), n, f((w * b + a) * n, b), fx(r)))

    CT = [("Setiap anak minum %s liter susu sehari. Berapa liter susu untuk %d anak?", "kali", "liter"),
          ("Sebuah resep memerlukan %s kg tepung. Ibu membuat %d kali resep itu. Berapa kg tepung yang diperlukan?", "kali", "kg"),
          ("Sebanyak %s liter jus dibagi sama banyak ke %d gelas. Berapa liter jus di setiap gelas?", "bagi", "liter"),
          ("Seutas tali panjangnya %s m dipotong menjadi %d bagian sama panjang. Berapa m panjang setiap bagian?", "bagi", "m")]

    def cerita():
        t, op, un = ch(CT)
        b = ch([2, 3, 4, 5, 8])
        a = ri(1, b - 1)
        n = ri(2, 6)
        x = F(a, b) if op == "bagi" or R().random() < 0.6 else 1 + F(a, b)
        r = x * n if op == "kali" else x / n
        return mcq(t % (fx(x), n), "%s %s" % (fx(r), un), ["%s %s" % (s, un) for s in (fw(x / n if op == "kali" else x * n), fw(x + n), fw(r + F(1, b))) if s],
                   "%s %s %d = %s." % (fx(x), "×" if op == "kali" else ":", n, fx(r)))

    sets = [("Pecahan × bilangan asli", [(kali, 20)]),
            ("Pecahan dari suatu bilangan", [(dari, 20)]),
            ("Pecahan : bilangan asli", [(bagi, 14), (bagi_asli, 6)]),
            ("Pecahan campuran × bilangan asli", [(campur, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Pecahan × bilangan asli: kalikan pembilangnya saja. %s × 3 = %s." % (f(2, 5), f(6, 5)),
         "Pecahan dari suatu bilangan: bagi dengan penyebut, lalu kalikan dengan pembilang. %s dari 20 = 20 : 4 × 3 = 15." % f(3, 4),
         "Pecahan : bilangan asli: kalikan penyebutnya. %s : 3 = %s." % (f(2, 5), f(2, 15))],
        [example("%s × 4 = …" % f(5, 6), ["%s" % f(20, 6), "Sederhanakan"], "3" + f(1, 3)),
         example("%s : 2 = …" % f(3, 4), ["%s × %s" % (f(3, 4), f(1, 2))], f(3, 8))],
        [["%s × 3 = %s (penyebut ikut dikali)" % (f(2, 5), f(6, 15)), "Hanya pembilang dikali: %s" % f(6, 5)],
         ["%s : 3 = %s (pembilang dibagi)" % (f(2, 5), f(2, 5)), "Penyebut dikali 3: %s" % f(2, 15)],
         ["%s dari 20 = 20 : 3" % f(3, 4), "20 : 4 = 5, lalu 5 × 3 = 15"]])
    faq = [{"q": "Bagaimana mengalikan pecahan dengan bilangan asli?", "a": "Kalikan pembilangnya dengan bilangan itu, penyebutnya tetap. Lalu sederhanakan."},
           {"q": "Apa arti 3/4 dari 20?", "a": "Artinya 20 dibagi menjadi 4 bagian sama besar, lalu diambil 3 bagian: 20 : 4 × 3 = 15."},
           {"q": "Bagaimana membagi pecahan dengan bilangan asli?", "a": "Kalikan penyebutnya dengan bilangan itu. 2/3 : 4 = 2/12 = 1/6."}]
    return dict(slug="perkalian-dan-pembagian-pecahan", dom="B", sort=8,
                std_text="Murid dapat melakukan operasi perkalian dan pembagian pecahan dengan bilangan asli.",
                title="Perkalian dan Pembagian Pecahan dengan Bilangan Asli", short_title="Perkalian dan Pembagian Pecahan",
                meta_desc="Latihan perkalian pecahan dengan bilangan asli, pecahan dari suatu bilangan, pembagian pecahan dengan bilangan asli, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Kali: pembilang. Bagi: penyebut", key_sub="3/4 dari 20 = 20 : 4 × 3 = 15.", body=body, faq=faq, sets=sets)


# ============================================================ 9. desimal
def d1(t):
    """t persepuluh → '2,5'"""
    return "%d,%d" % divmod(t, 10)


def ften(t):
    """t persepuluh sebagai pecahan berpenyebut 10 (tidak disederhanakan)"""
    w, r = divmod(t, 10)
    return ("%d" % w if w else "") + f(r, 10)


def u9():
    def baca():
        t = ri(1, 99)
        if t % 10 == 0:
            return None
        return mcq("%s dalam bentuk desimal adalah …" % ften(t), d1(t), ["%d,%d" % (t % 10, t // 10) if t // 10 else "0,0%d" % t, "%d,%d" % (t, 0) if t < 10 else "%d,%d" % (t // 10 + 1, t % 10), "0,%d" % t if t >= 10 else "%d,1" % t],
                   "%s = %s." % (ften(t), d1(t)))

    def ke_pecahan():
        t = ri(1, 99)
        if t % 10 == 0:
            return None
        return mcq("%s dalam bentuk pecahan persepuluhan adalah …" % d1(t), ften(t), [fw(F(t, 100)), fw(F(t % 10, t // 10)) if t // 10 else fw(F(10, t)), fw(F(t // 10 + t % 10, 10)) if t >= 10 else fw(F(t, 1)), fw(F(t + 1, 10))],
                   "Satu angka di belakang koma = persepuluhan: %s = %s." % (d1(t), ften(t)))

    def garis():
        lo = ri(0, 8)
        k = ri(1, 9)
        if k == 5:
            return None
        v = lo * 10 + k
        svg = garis_dec(lo, k)
        return mcq("Bilangan desimal yang ditunjuk huruf A adalah …" + svg, d1(v), [d1(lo * 10 + 10 - k), d1(v + 1), "%d,%d" % (lo, k + 1) if k < 9 else d1(v - 2)],
                   "Jarak %d ke %d dibagi 10. A ada %d garis dari %d: %s." % (lo, lo + 1, k, lo, d1(v)))

    def banding():
        a, b = R().sample(range(1, 100), 2)
        sa, sb = d1(a), d1(b)
        return stmt(sa, sb, a, b, "Bandingkan bilangan utuhnya dulu, lalu angka persepuluhan. %s %s %s." % (sa, rel(a, b), sb))

    def urut():
        xs = R().sample(range(1, 100), 4)
        up = R().random() < 0.5
        g = sorted(xs, reverse=not up)
        j = lambda ys: "; ".join(d1(y) for y in ys)
        w2 = sorted(xs, key=lambda z: (z % 10, z), reverse=not up)
        w3 = list(g)
        w3[1], w3[2] = w3[2], w3[1]
        return mcq("Urutan %s dari yang %s adalah …" % (j(pool(xs)), "terkecil" if up else "terbesar"), j(g), [j(sorted(xs, reverse=up)), j(w2), j(w3)],
                   "Urutannya %s." % j(g))

    PAIRS = [(1, 2, 5), (1, 5, 2), (2, 5, 4), (3, 5, 6), (4, 5, 8), (3, 2, 15), (5, 2, 25), (6, 5, 12), (7, 2, 35), (9, 5, 18), (1, 1, 10)]

    def ubah():
        a, b, t = ch(PAIRS[:-1])
        kind = ri(0, 2)
        if kind == 0:
            return mcq("%s dalam bentuk desimal adalah …" % fx(F(a, b)), d1(t), ["%d,%d" % (a, b), d1(t + 1), "0,%d" % (a * 10 + b) if a < 10 else d1(t * 10)],
                       "Ubah penyebutnya menjadi 10: %s = %s = %s." % (fx(F(a, b)), f(t, 10), d1(t)))
        p = t * 10
        if kind == 1:
            return mcq("%s = …%%" % d1(t), "%d%%" % p, ["%d%%" % t, "%d%%" % (p + 10), "%d%%" % (p // 10 if p >= 100 else p + 5)],
                       "%s = %s = %d%%." % (d1(t), f(p, 100), p))
        return mcq("%d%% dalam bentuk desimal adalah …" % p, d1(t), ["%d,%d" % (p // 10, p % 10) if p >= 10 else "0,0%d" % p, "0,%02d" % (p // 10) if p < 100 else d1(t + 10), d1(t + 1)],
                   "%d%% = %s = %s." % (p, f(p, 100), d1(t)))

    CT = ["Berat badan %s %s kg dan berat badan %s %s kg. Siapa yang lebih berat?",
          "Lompatan jauh %s mencapai %s m dan lompatan %s %s m. Siapa yang melompat lebih jauh?",
          "%s berlari %s km dan %s berlari %s km. Siapa yang berlari lebih jauh?"]

    def cerita():
        x, y = K().two()
        t = ch(CT)
        if "Berat" in t:
            a, b = ri(250, 450), ri(250, 450)
        elif "Lompatan" in t:
            a, b = ri(18, 45), ri(18, 45)
        else:
            a, b = ri(10, 60), ri(10, 60)
        if a == b:
            return None
        win = x if a > b else y
        return mcq(t % (x, d1(a), y, d1(b)), win, [y if win == x else x, "Sama", "Tidak dapat ditentukan"],
                   "%s %s %s." % (d1(a), rel(a, b), d1(b)))

    sets = [("Pecahan persepuluhan dan desimal", [(baca, 10), (ke_pecahan, 10)]),
            ("Desimal pada garis bilangan", [(garis, 20)]),
            ("Membandingkan desimal", [(banding, 14), (urut, 6)]),
            ("Pecahan, desimal, dan persen", [(ubah, 20)]),
            ("Soal cerita", [(cerita, 14), (urut, 6)])]
    body = lesson(
        ["Desimal dengan satu angka di belakang koma menunjukkan persepuluhan: 2,7 = 2 + %s = %s." % (f(7, 10), f(27, 10)),
         "Untuk membandingkan, lihat bilangan utuhnya dulu. Jika sama, bandingkan angka di belakang koma.",
         "Pecahan dapat diubah ke desimal dengan membuat penyebutnya 10: %s = %s = 0,6. Lalu 0,6 = %s = 60%%." % (f(3, 5), f(6, 10), f(60, 100))],
        [example("Bandingkan 3,8 dan 4,1.", ["Bilangan utuh: 3 &lt; 4"], "3,8 &lt; 4,1"),
         example("Ubah %s ke desimal." % f(7, 2), ["%s = %s" % (f(7, 2), f(35, 10))], "3,5")],
        [["3,8 &gt; 4,1 karena 8 &gt; 1", "Bandingkan bilangan utuh dulu: 3 &lt; 4"],
         ["%s = 0,07" % f(7, 10), "%s = 0,7 (persepuluhan, satu angka di belakang koma)" % f(7, 10)],
         ["0,5 = 5%", "0,5 = %s = 50%%" % f(50, 100)]])
    faq = [{"q": "Bagaimana membandingkan bilangan desimal?", "a": "Bandingkan bilangan di depan koma lebih dulu. Jika sama, bandingkan angka persepuluhan di belakang koma."},
           {"q": "Bagaimana mengubah pecahan menjadi desimal?", "a": "Ubah pecahan menjadi pecahan berpenyebut 10 (atau 100). Contoh: 4/5 = 8/10 = 0,8."},
           {"q": "Mengapa desimal di Indonesia memakai koma?", "a": "Dalam bahasa Indonesia, koma dipakai untuk desimal (2,5) dan titik untuk pemisah ribuan (2.500)."}]
    return dict(slug="desimal", dom="B", sort=9,
                std_text="Murid dapat membandingkan dan mengurutkan bilangan desimal (satu angka di belakang koma) serta mengubah pecahan menjadi desimal dan persen.",
                title="Bilangan Desimal: Membandingkan dan Mengubah Bentuk", short_title="Desimal",
                meta_desc="Latihan pecahan persepuluhan dan desimal, desimal pada garis bilangan, membandingkan dan mengurutkan desimal, serta mengubah pecahan, desimal, dan persen. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="3/5 = 6/10 = 0,6 = 60%", key_sub="Bandingkan bilangan utuh dulu, lalu persepuluhan.", body=body, faq=faq, sets=sets)


def garis_dec(lo, k):
    """garis bilangan lo sampai lo + 1 dengan 10 bagian, panah A di lo + k/10"""
    W, x0, y = 440, 30, 58
    s = [line(x0 - 8, y, x0 + W + 12, y, INK, 2), "<path d='M%d %d l-9 -6 v12 Z' fill='%s'/>" % (x0 + W + 20, y, INK)]
    for i in range(11):
        X = x0 + i * W / 10.0
        long = i in (0, 10, 5)
        s.append(line(X, y - (10 if long else 6), X, y + (10 if long else 6), INK, 2 if long else 1.3))
    s.append(text(x0, y + 30, str(lo), 15))
    s.append(text(x0 + W, y + 30, str(lo + 1), 15))
    X = x0 + k * W / 10.0
    s.append("<path d='M%.1f %d l-7 -12 h14 Z' fill='%s'/>" % (X, y - 12, RED))
    s.append(text(X, y - 28, "A", 16, col=RED))
    return wrap(W + 60, y + 42, "".join(s), "garis bilangan dari %d sampai %d" % (lo, lo + 1), lg=True)


# ============================================================ 10. soal cerita uang
ITEMS5 = [("tas sekolah", 85000), ("sepatu", 120000), ("kaus olahraga", 45000), ("buku cerita", 38000), ("payung", 35000), ("kotak pensil", 27500),
          ("bola sepak", 95000), ("jam dinding", 62500), ("botol minum", 24500), ("topi", 32000), ("raket", 150000), ("kamus", 56000)]


def u10():
    def total():
        (a, pa), (b, pb), (c, pc) = R().sample(ITEMS5, 3)
        who = K().next()
        t = pa + pb + pc
        if t > 300000:
            return None
        return mcq("%s membeli %s seharga %s, %s seharga %s, dan %s seharga %s. Berapa total harganya?" % (who, a, rp(pa), b, rp(pb), c, rp(pc)),
                   rp(t), [rp(t + 1000), rp(t - 500), rp(pa + pb)], "%s + %s + %s = %s." % (rp(pa), rp(pb), rp(pc), rp(t)))

    def kembali():
        it, p = ch(ITEMS5)
        k = ri(1, 3)
        cost = p * k
        pay = ch([x for x in (50000, 100000, 200000, 300000) if x > cost] or [cost + 50000])
        who = K().next()
        return mcq("%s membeli %d %s seharga %s per buah dan membayar dengan %s. Berapa uang kembaliannya?" % (who, k, it, rp(p), rp(pay)),
                   rp(pay - cost), [rp(pay - p) if k > 1 else rp(pay - cost + 5000), rp(pay - cost - 1000), rp(cost)],
                   "Harga %d %s = %s. Kembalian = %s − %s = %s." % (k, it, rp(cost), rp(pay), rp(cost), rp(pay - cost)))

    def lembar():
        n = ch([2000, 5000, 10000, 20000, 50000])
        k = ri(2, 20)
        tot = n * k
        if tot > 500000:
            return None
        return mcq("Uang %s ditukar dengan uang pecahan %s. Berapa lembar uang yang didapat?" % (rp(tot), rp(n)), "%d lembar" % k,
                   ["%d lembar" % x for x in (k + 1, k * 10 if k < 10 else k - 2, tot // 1000)], "%s : %s = %d." % (rp(tot), rp(n), k))

    def satuan():
        it = ch(["pensil", "buku tulis", "spidol", "penghapus", "kelereng"])
        p = ch([1500, 2500, 3000, 3500, 4000, 4500, 6000])
        a, b = ri(2, 12), ri(2, 12)
        if a == b:
            return None
        return mcq("Harga %d %s adalah %s. Berapa harga %d %s?" % (a, it, rp(p * a), b, it), rp(p * b), [rp(p * a + p * b), rp(p * (b + 1)), rp(p * abs(b - a)) if a != b else rp(p)],
                   "Harga 1 %s = %s : %d = %s. Harga %d %s = %d × %s = %s." % (it, rp(p * a), a, rp(p), b, it, b, rp(p), rp(p * b)))

    def tabung():
        who = K().next()
        per = ch([2000, 2500, 5000, 7500, 10000])
        target = ch([x for x in (50000, 75000, 100000, 150000, 200000) if x % per == 0 and x // per <= 40])
        have = per * ri(1, target // per - 2)
        n = (target - have) // per
        it = ch(["sepatu baru", "sepeda bekas", "tas", "kamus", "raket"])
        return mcq("%s ingin membeli %s seharga %s. Ia sudah punya %s dan menabung %s setiap minggu. Berapa minggu lagi uangnya cukup?" % (who, it, rp(target), rp(have), rp(per)),
                   "%d minggu" % n, ["%d minggu" % x for x in (target // per, n + 1, n - 1 if n > 1 else n + 2)],
                   "Kurangnya %s − %s = %s. %s : %s = %d minggu." % (rp(target), rp(have), rp(target - have), rp(target - have), rp(per), n))

    def banding():
        it = ch(["minyak goreng", "beras", "gula", "sabun cuci", "susu"])
        a, b = ch([(1, 2), (2, 5), (1, 3), (2, 3), (3, 5)])
        pa = ch([12000, 15000, 18000, 20000, 24000])
        pb_unit = pa // a + ch([-1000, -500, 500, 1000])
        pb = pb_unit * b
        ua, ub = F(pa, a), F(pb, b)
        g = "Kemasan %d" % b if ub < ua else "Kemasan %d" % a
        un = "kg" if it in ("beras", "gula") else "liter"
        return mcq("%s %d %s harganya %s, dan %d %s harganya %s. Kemasan mana yang lebih murah per %s?" % (it.capitalize(), a, un, rp(pa), b, un, rp(pb), un),
                   ("Kemasan %d %s" % (b, un)) if ub < ua else ("Kemasan %d %s" % (a, un)),
                   [("Kemasan %d %s" % (a, un)) if ub < ua else ("Kemasan %d %s" % (b, un)), "Harganya sama", "Tidak dapat dibandingkan"],
                   "Harga per %s: %s : %d = %s dan %s : %d = %s." % (un, rp(pa), a, rp(int(ua)), rp(pb), b, rp(int(ub))))

    sets = [("Total belanja", [(total, 20)]),
            ("Uang kembalian", [(kembali, 20)]),
            ("Menukar uang dan harga satuan", [(lembar, 10), (satuan, 10)]),
            ("Menabung", [(tabung, 20)]),
            ("Membandingkan harga", [(banding, 10), (satuan, 5), (kembali, 5)])]
    body = lesson(
        ["Baca soal dengan teliti: apa yang diketahui dan apa yang ditanyakan.",
         "Total belanja = jumlah semua harga. Kembalian = uang yang dibayar − total belanja.",
         "Untuk membandingkan harga, hitung harga satuan (harga untuk 1 buah, 1 kg, atau 1 liter)."],
        [example("Harga 4 spidol Rp14.000. Berapa harga 6 spidol?", ["1 spidol = Rp14.000 : 4 = Rp3.500", "6 × Rp3.500"], "Rp21.000"),
         example("Uang Rp150.000 ditukar uang Rp5.000.", ["Rp150.000 : Rp5.000"], "30 lembar")],
        [["Kembalian dihitung dengan menambah", "Kembalian = uang dibayar − harga"],
         ["Kemasan besar selalu lebih murah", "Hitung harga per satuan dulu"],
         ["Lupa mengurangi uang yang sudah ada", "Hitung kekurangannya, baru dibagi tabungan per minggu"]])
    faq = [{"q": "Apa itu harga satuan?", "a": "Harga untuk satu barang atau satu satuan, misalnya per kg atau per liter. Harga satuan = harga total : banyak barang."},
           {"q": "Bagaimana menghitung kembalian?", "a": "Kurangkan total belanja dari uang yang dibayarkan."},
           {"q": "Bagaimana menghitung lama menabung?", "a": "Hitung kekurangan uang, lalu bagi dengan uang yang ditabung setiap minggu."}]
    return dict(slug="soal-cerita-uang", dom="B", sort=10,
                std_text="Murid dapat menyelesaikan masalah yang berkaitan dengan uang.",
                title="Soal Cerita Uang", short_title="Soal Cerita Uang",
                meta_desc="Latihan soal cerita uang rupiah: total belanja, kembalian, menukar uang, harga satuan, menabung, dan membandingkan harga. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Hitung harga satuan", key_sub="Kembalian = uang dibayar − total belanja.", body=body, faq=faq, sets=sets)
