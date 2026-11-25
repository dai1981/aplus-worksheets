# -*- coding: utf-8 -*-
"""
Indonesia / Matematika / Kelas 6 (Fase C, Kurikulum Merdeka CP 2025)。18 単元。
Kelas 5 の内容をまとめ、使う・組み合わせる学年（数は 1.000.000 まで、四則は 100.000 まで）。
python3 tools/id_k6.py [番号…]
seed は 40600 + sort。Kelas 5 の問題関数（id_k5a・id_k5b）も新しい seed で使う。
"""
import math
import random
import sys
from fractions import Fraction as Fr
import id_k4a as A
from id_k4a import ri, ch, pool, cap, rel, stmt
from id_k5a import f, fx
from id_k5b import shape_svg, lg
from id_common import (num, rp, u, NB, mcq, mix, lesson, example, table, make_unit, wrap, text, line, fig, svg_wrap,
                       INK, GREEN, FILL, RED, BLUE)

G = "kelas-6"


def R():
    return A.R


def K():
    return A.K


def maker(d, name, i=0):
    out = []
    for _, parts in d["sets"]:
        for m, _n in parts:
            if m.__name__ == name and m not in out:
                out.append(m)
    return out[i]


def d2(h):
    """百分の一単位の整数 → 0,25 / 1,5 / 3"""
    h = int(h)
    w, r = divmod(abs(h), 100)
    s = num(w)
    if r:
        s += "," + ("%02d" % r).rstrip("0")
    return ("−" if h < 0 else "") + s


def pct(x):
    return "%s%%" % (num(x) if float(x).is_integer() else str(x).replace(".", ","))


# ============================================================ 1. operasi hitung campuran
def u1():
    def urutan():
        k = ri(0, 3)
        if k == 0:
            a, b, c = ri(10, 90), ri(2, 9), ri(2, 9)
            v, w = a + b * c, (a + b) * c
            q = "%d + %d × %d" % (a, b, c)
        elif k == 1:
            a, b, c = ri(50, 150), ri(2, 9), ri(2, 9)
            v, w = a - b * c, (a - b) * c
            q = "%d − %d × %d" % (a, b, c)
        elif k == 2:
            c, d = ri(2, 9), ri(2, 9)
            b = c * d
            a = ri(10, 90)
            v, w = a + d, Fr(a + b, c)
            q = "%d + %d : %d" % (a, b, c)
        else:
            c, d = ri(2, 9), ri(2, 9)
            b = c * d
            a = ri(d + 10, 120)
            v, w = a - d, Fr(a - b, c)
            q = "%d − %d : %d" % (a, b, c)
        if v <= 0:
            return None
        ws = [str(w) if Fr(w).denominator == 1 and w > 0 else None, str(v + 10), str(v - 1), str(v + 1)]
        return mcq("%s = …" % q, str(v), ws, "Perkalian dan pembagian dikerjakan lebih dulu, baru penjumlahan dan pengurangan. %s = %d." % (q, v))

    def kurung():
        k = ri(0, 2)
        a, b, c = ri(5, 40), ri(2, 30), ri(2, 9)
        if k == 0:
            q, v, w = "(%d + %d) × %d" % (a, b, c), (a + b) * c, a + b * c
        elif k == 1:
            if a <= b:
                a, b = b + ri(2, 20), a
            q, v, w = "(%d − %d) × %d" % (a, b, c), (a - b) * c, a - b * c
        else:
            q, v, w = "%d × (%d + %d)" % (c, a, b), c * (a + b), c * a + b
        return mcq("%s = …" % q, num(v), [num(w) if w > 0 else None, num(v + c), num(v - c), num(v + 10)],
                   "Kerjakan yang di dalam kurung lebih dulu. %s = %s." % (q, num(v)))

    def besar():
        a, b = ri(11, 99), ri(101, 999)
        c, d = ri(2, 9), ri(1001, 9999)
        k = ri(0, 1)
        if k == 0:
            v = a * b + d
            if v > 100000:
                return None
            q = "%s × %s + %s" % (num(a), num(b), num(d))
            ws = [a * (b + d), v + 100, v - 1000, v + 10]
        else:
            v = d - c * b
            if v <= 0:
                return None
            q = "%s − %d × %s" % (num(d), c, num(b))
            ws = [(d - c) * b, v + 100, v - 10, v + 1000]
        return mcq("%s = …" % q, num(v), [num(x) for x in ws if 0 < x <= 1000000], "Kalikan dulu, lalu jumlahkan atau kurangkan: %s." % num(v))

    def pilih():
        a, b, c = ri(20, 90), ri(2, 9), ri(2, 9)
        op = ch([("+", "×"), ("−", "×"), ("+", ":"), ("−", ":")])
        if op[1] == ":":
            b = b * c
        q = "%d %s %d %s %d" % (a, op[0], b, op[1], c)
        first = "%d %s %d" % (b, op[1], c)
        other = "%d %s %d" % (a, op[0], b)
        if R().random() < 0.5:
            q2 = "(%d %s %d) %s %d" % (a, op[0], b, op[1], c)
            return mcq("Pada %s, yang dikerjakan lebih dulu adalah …" % q2, other, [first, "%d %s %d" % (a, op[1], c), "dari kanan ke kiri"],
                       "Bagian dalam kurung dikerjakan lebih dulu: %s." % other)
        return mcq("Pada %s, yang dikerjakan lebih dulu adalah …" % q, first, [other, "%d %s %d" % (a, op[1], c), "dari kiri ke kanan"],
                   "%s dikerjakan sebelum %s, jadi %s dulu." % ("Perkalian" if op[1] == "×" else "Pembagian", "penjumlahan" if op[0] == "+" else "pengurangan", first))

    ITEM = [("buku tulis", 4500), ("pensil", 3000), ("spidol", 7500), ("roti", 6000), ("susu kotak", 5500), ("penggaris", 4000), ("map", 2500), ("bolpoin", 3500)]

    def cerita():
        k = ri(0, 2)
        x = K().next()
        if k == 0:
            (a, pa), (b, pb) = pool(ITEM)[:2]
            m, n = ri(2, 6), ri(2, 5)
            tot = m * pa + n * pb
            pay = ch([50000, 100000])
            if tot >= pay:
                return None
            return mcq("%s membeli %d %s seharga %s per buah dan %d %s seharga %s per buah. Ia membayar %s. Berapa kembaliannya?"
                       % (x, m, a, rp(pa), n, b, rp(pb), rp(pay)), rp(pay - tot),
                       [rp(pay - (m + n) * pa), rp(tot), rp(pay - tot + 1000), rp(pay - pa - pb)],
                       "%s − (%d × %s + %d × %s) = %s − %s = %s." % (rp(pay), m, rp(pa), n, rp(pb), rp(pay), rp(tot), rp(pay - tot)))
        if k == 1:
            box, isi, ambil = ri(12, 48), ri(12, 30), ri(20, 150)
            tot = box * isi - ambil
            return mcq("Ada %d kardus, setiap kardus berisi %d botol air. Sebanyak %d botol dibagikan. Berapa botol yang tersisa?" % (box, isi, ambil),
                       u(tot, "botol"), [u(box * (isi - ambil) if isi > ambil else box * isi + ambil, "botol"), u(box * isi, "botol"), u(tot + 10, "botol")],
                       "%d × %d − %d = %s − %d = %s." % (box, isi, ambil, num(box * isi), ambil, num(tot)))
        per = ri(4, 12)
        tot = per * ri(6, 45)
        kel = tot // per
        return mcq("Sebanyak %s kue dikemas dalam kotak, setiap kotak %d kue. Setiap kotak dijual %s. Berapa uang yang didapat jika semua kotak terjual?"
                   % (num(tot), per, rp(per * 1500)), rp(kel * per * 1500),
                   [rp(tot * 1500 // 10), rp(kel * 1500), rp(kel * per * 1500 + per * 1500)],
                   "Banyak kotak = %s : %d = %d. Uang = %d × %s = %s." % (num(tot), per, kel, kel, rp(per * 1500), rp(kel * per * 1500)))

    sets = [("Kali dan bagi lebih dulu", [(urutan, 20)]),
            ("Tanda kurung", [(kurung, 20)]),
            ("Mana yang lebih dulu?", [(pilih, 10), (urutan, 5), (kurung, 5)]),
            ("Bilangan besar", [(besar, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Dalam operasi hitung campuran ada aturan urutan: kerjakan yang di dalam kurung dulu.",
         "Setelah itu, perkalian dan pembagian dikerjakan lebih dulu dari penjumlahan dan pengurangan.",
         "Jika tingkatannya sama (misalnya + dan −), kerjakan dari kiri ke kanan."],
        [example("25 + 4 × 6 = …", ["4 × 6 = 24 dulu", "25 + 24"], "49"),
         example("(25 + 4) × 6 = …", ["Kurung dulu: 25 + 4 = 29", "29 × 6"], "174")],
        [["25 + 4 × 6 dihitung dari kiri: 29 × 6 = 174", "Kalikan dulu: 25 + 24 = 49"],
         ["Tanda kurung diabaikan", "Bagian dalam kurung selalu dikerjakan pertama"],
         ["60 − 20 + 10 dihitung 60 − 30", "Dari kiri ke kanan: 40 + 10 = 50"]])
    faq = [{"q": "Apa urutan operasi hitung campuran?", "a": "Kurung dulu, lalu perkalian dan pembagian dari kiri ke kanan, lalu penjumlahan dan pengurangan dari kiri ke kanan."},
           {"q": "Mana yang dikerjakan dulu, perkalian atau pembagian?", "a": "Perkalian dan pembagian setingkat. Kerjakan yang lebih dulu muncul dari kiri."},
           {"q": "Kenapa urutan ini penting?", "a": "Agar semua orang mendapat hasil yang sama. Tanpa aturan, 2 + 3 × 4 bisa dihitung 20 atau 14; yang benar adalah 14."}]
    return dict(slug="operasi-hitung-campuran", dom="B", sort=1,
                std_text="Peserta didik melakukan operasi penjumlahan, pengurangan, perkalian, dan pembagian bilangan cacah sampai 100.000 dan menyelesaikan masalah yang melibatkan operasi hitung campuran.",
                title="Operasi Hitung Campuran", short_title="Operasi Hitung Campuran",
                meta_desc="Latihan operasi hitung campuran untuk kelas 6 SD: urutan perkalian dan pembagian, tanda kurung, bilangan besar, dan soal cerita dua langkah. 100 soal dengan kunci jawaban.",
                key_big="Kurung, lalu × dan :, lalu + dan −", key_sub="Operasi yang setingkat dikerjakan dari kiri.",
                body=body, faq=faq, sets=sets)


# ============================================================ 2. pembulatan dan taksiran
def u2(d1, d2_):
    bulat, taksir = maker(d1, "bulat"), maker(d2_, "taksir")

    def r10(x, p):
        return int(math.floor(x / float(p) + 0.5)) * p

    def kali():
        a, b = ri(11, 99), ri(11, 99)
        if a % 10 == 5 or b % 10 == 5:
            return None
        ra, rb = r10(a, 10), r10(b, 10)
        g = ra * rb
        return mcq("Taksiran terbaik untuk %d × %d adalah …" % (a, b), num(g), [num(g + ra * 10), num(g - rb * 10), num(a * b), num(g * 10)],
                   "%d ≈ %d dan %d ≈ %d, jadi %d × %d = %s." % (a, ra, b, rb, ra, rb, num(g)))

    def bagi():
        d = ri(3, 9)
        q = ri(11, 90)
        n = d * q * 10 + ri(1, d * 10 - 1)
        cn = d * q * 10
        if n % (d * 10) == 0:
            return None
        return mcq("Taksiran %s : %d dengan bilangan yang mudah dibagi adalah …" % (num(n), d), num(q * 10),
                   [num(q), num(q * 100), num(q * 10 + 10), num(q * 10 - 10)],
                   "%s dekat dengan %s, dan %s : %d = %s." % (num(n), num(cn), num(cn), d, num(q * 10)))

    ITEM = [("tas", 87500), ("sepatu", 124900), ("jaket", 152000), ("kipas angin", 189500), ("buku gambar", 18900), ("helm", 96000), ("payung", 41500), ("termos", 63200)]

    def uang():
        (a, pa), (b, pb) = pool(ITEM)[:2]
        ra, rb = r10(pa, 1000), r10(pb, 1000)
        g = ra + rb
        return mcq("Harga %s %s dan %s %s. Dibulatkan ke ribuan terdekat, kira-kira berapa harga keduanya?" % (a, rp(pa), b, rp(pb)), rp(g),
                   [rp(g + 1000), rp(g - 1000), rp(r10(pa, 10000) + r10(pb, 10000)) if r10(pa, 10000) + r10(pb, 10000) != g else rp(g + 2000), rp(pa + pb)],
                   "%s ≈ %s dan %s ≈ %s. Jumlahnya %s." % (rp(pa), rp(ra), rp(pb), rp(rb), rp(g)))

    def cukup():
        (a, pa), (b, pb), (c, pc) = pool(ITEM)[:3]
        tot = pa + pb + pc
        have = r10(tot, 10000) + ch([-20000, -10000, 10000, 20000])
        if have <= 0 or abs(have - tot) < 6000:
            return None
        ok = have > tot
        return mcq("%s membawa %s. Ia ingin membeli %s (%s), %s (%s), dan %s (%s). Dengan menaksir, apakah uangnya cukup?"
                   % (K().next(), rp(have), a, rp(pa), b, rp(pb), c, rp(pc)), "Cukup" if ok else "Tidak cukup",
                   ["Tidak cukup" if ok else "Cukup", "Uangnya pas", "Tidak bisa ditaksir"],
                   "Taksiran harga: %s + %s + %s = %s, %s %s." % (rp(r10(pa, 1000)), rp(r10(pb, 1000)), rp(r10(pc, 1000)),
                                                                 rp(r10(pa, 1000) + r10(pb, 1000) + r10(pc, 1000)), "lebih kecil dari" if ok else "lebih besar dari", rp(have)))

    sets = [("Pembulatan", [(bulat, 20)]),
            ("Menaksir penjumlahan dan pengurangan", [(taksir, 20)]),
            ("Menaksir perkalian", [(kali, 20)]),
            ("Menaksir pembagian", [(bagi, 20)]),
            ("Menaksir uang belanja", [(uang, 12), (cukup, 8)])]
    body = lesson(
        ["Membulatkan berarti mengganti bilangan dengan bilangan yang mudah, misalnya ke puluhan, ratusan, atau ribuan terdekat.",
         "Lihat angka di sebelah kanan tempat pembulatan. Jika 5 atau lebih, bulatkan ke atas. Jika kurang dari 5, bulatkan ke bawah.",
         "Menaksir berarti menghitung dengan bilangan bulatan untuk mendapat hasil kira-kira dengan cepat."],
        [example("Taksir 48 × 31.", ["48 ≈ 50, 31 ≈ 30", "50 × 30"], "1.500"),
         example("Taksir 2.785 : 7.", ["2.785 dekat 2.800, dan 28 mudah dibagi 7", "2.800 : 7"], "400")],
        [["Membulatkan 46 ke puluhan menjadi 40", "Angka satuan 6 ≥ 5, jadi 50"],
         ["Taksiran dianggap hasil tepat", "Taksiran hanya kira-kira; tanda ≈ artinya hampir sama"],
         ["Membulatkan pembilang yang dibagi menjadi bilangan yang sulit dibagi", "Pilih bilangan yang mudah dibagi: 2.785 : 7 ≈ 2.800 : 7"]])
    faq = [{"q": "Apa bedanya pembulatan dan taksiran?", "a": "Pembulatan mengubah satu bilangan menjadi bilangan yang mudah. Taksiran adalah hasil hitung kira-kira dengan bilangan bulatan itu."},
           {"q": "Kapan kita perlu menaksir?", "a": "Saat berbelanja, merencanakan uang, atau memeriksa apakah hasil hitungan masuk akal."},
           {"q": "Bagaimana membulatkan ke ribuan terdekat?", "a": "Lihat angka ratusan. Jika 5 atau lebih, ribuannya ditambah 1; jika kurang dari 5, ribuannya tetap. Contoh: 48.672 ≈ 49.000."}]
    return dict(slug="pembulatan-dan-taksiran", dom="B", sort=2,
                std_text="Peserta didik melakukan estimasi atau taksiran hasil operasi hitung bilangan cacah sampai 100.000 dan menggunakannya dalam masalah sehari-hari.",
                title="Pembulatan dan Taksiran", short_title="Pembulatan dan Taksiran",
                meta_desc="Latihan pembulatan dan taksiran untuk kelas 6 SD: membulatkan bilangan, menaksir penjumlahan, pengurangan, perkalian, pembagian, dan uang belanja. 100 soal dengan kunci jawaban.",
                key_big="Angka 5 atau lebih: bulatkan ke atas", key_sub="Taksiran = hitung cepat dengan bilangan bulatan.",
                body=body, faq=faq, sets=sets)


# ============================================================ 3. KPK dan FPB dalam soal cerita
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


def u3(d5):
    kpk, fpb, ck, cf = (maker(d5, x) for x in ("kpk", "fpb", "cerita_kpk", "cerita_fpb"))

    def hari():
        a, b = ri(2, 8), ri(3, 10)
        if a == b:
            return None
        L = a * b // math.gcd(a, b)
        if L > 40 or L % 7 == 0:
            return None
        x, y = K().two()
        s = ri(0, 6)
        h = HARI[(s + L) % 7]
        return mcq("%s berenang setiap %d hari sekali dan %s setiap %d hari sekali. Mereka berenang bersama pada hari %s. Pada hari apa mereka berenang bersama lagi?"
                   % (x, a, y, b, HARI[s]), h, [HARI[(s + a * b) % 7], HARI[(s + L + 1) % 7], HARI[(s + a + b) % 7], HARI[(s + L - 1) % 7], HARI[(s + L + 2) % 7], HARI[s], HARI[(s + L + 3) % 7]],
                   "KPK dari %d dan %d adalah %d. %d hari setelah %s adalah hari %s." % (a, b, L, L, HARI[s], h))

    def lampu():
        a, b = ch([(10, 15), (12, 18), (15, 20), (20, 30), (6, 8), (8, 12), (12, 16), (10, 25), (9, 12), (15, 25), (6, 10), (20, 25)])
        L = a * b // math.gcd(a, b)
        h, m = ri(6, 9), ch([0, 15, 30])
        t = h * 60 + m + L
        fmt = lambda t: "%02d.%02d" % (t // 60, t % 60)
        what = ch([("Lampu merah", "lampu kuning", "menyala"), ("Bus A", "bus B", "berangkat dari terminal"), ("Bel kelas", "bel kantor", "berbunyi")])
        return mcq("%s %s setiap %d menit dan %s setiap %d menit. Keduanya %s bersama pukul %s. Pukul berapa keduanya %s bersama lagi?"
                   % (what[0], what[2], a, what[1], b, what[2], fmt(h * 60 + m), what[2]), fmt(t),
                   [fmt(h * 60 + m + a * b), fmt(h * 60 + m + a + b), fmt(t + 10)],
                   "KPK dari %d dan %d adalah %d menit. %s + %d menit = %s." % (a, b, L, fmt(h * 60 + m), L, fmt(t)))

    THING = [("buku tulis", "pensil"), ("jeruk", "apel"), ("permen cokelat", "permen susu"), ("kue lapis", "kue lumpur"), ("bolpoin", "penghapus")]

    def paket():
        g = ri(3, 12)
        p, q = ri(2, 9), ri(2, 9)
        if math.gcd(p, q) != 1 or p == q:
            return None
        a, b = g * p, g * q
        s1, s2 = ch(THING)
        if R().random() < 0.5:
            return mcq("Ada %d %s dan %d %s. Semua dibagikan sama banyak ke dalam paket, tanpa sisa. Paling banyak berapa paket yang bisa dibuat?" % (a, s1, b, s2),
                       u(g, "paket"), [u(a * b // g, "paket"), u(p, "paket"), u(g * 2, "paket"), u(a + b, "paket")],
                       "FPB dari %d dan %d adalah %d, jadi %d paket." % (a, b, g, g))
        return mcq("Ada %d %s dan %d %s yang dibagikan ke paket sebanyak-banyaknya, sama banyak dan tanpa sisa. Berapa %s dalam setiap paket?" % (a, s1, b, s2, s1),
                   str(p), [str(q), str(g), str(p + 1), str(a // 2)],
                   "FPB dari %d dan %d adalah %d paket. Setiap paket berisi %d : %d = %d %s." % (a, b, g, a, g, p, s1))

    sets = [("KPK", [(kpk, 14), (ck, 6)]),
            ("FPB", [(fpb, 14), (cf, 6)]),
            ("Bertemu lagi pada hari apa?", [(hari, 20)]),
            ("Bertemu lagi pukul berapa?", [(lampu, 20)]),
            ("Membagi ke dalam paket", [(paket, 20)])]
    body = lesson(
        ["KPK (kelipatan persekutuan terkecil) dipakai untuk masalah <i>bersamaan lagi</i>: kapan dua kegiatan berulang terjadi bersama lagi.",
         "FPB (faktor persekutuan terbesar) dipakai untuk masalah <i>membagi sama banyak sebanyak-banyaknya</i> tanpa sisa.",
         "Tanyakan dulu: apakah yang dicari waktu bertemu lagi (KPK) atau banyak kelompok terbesar (FPB)?"],
        [example("Rina les setiap 4 hari, Dewi setiap 6 hari. Mereka les bersama hari Senin. Kapan bersama lagi?", ["KPK 4 dan 6 = 12", "12 hari setelah Senin: 12 = 7 + 5, jadi Senin + 5 hari"], "Sabtu"),
         example("Ada 24 apel dan 36 jeruk dibagi ke paket sebanyak-banyaknya. Berapa paket?", ["FPB 24 dan 36 = 12"], "12 paket")],
        [["Menjumlahkan kedua bilangan (4 + 6 = 10 hari)", "Cari KPK: 12 hari"],
         ["Memakai KPK untuk membagi ke paket", "Membagi sama banyak memakai FPB"],
         ["Menghitung hari dimulai dari hari yang sama sebagai hari ke-1", "Hitung 12 hari setelah Senin"]])
    faq = [{"q": "Kapan memakai KPK dalam soal cerita?", "a": "Saat mencari kapan dua atau lebih kejadian yang berulang akan terjadi bersamaan lagi, misalnya jadwal piket, lampu berkedip, atau bus berangkat."},
           {"q": "Kapan memakai FPB dalam soal cerita?", "a": "Saat membagi beberapa jenis benda ke dalam kelompok atau paket sebanyak-banyaknya dengan isi yang sama dan tanpa sisa."},
           {"q": "Bagaimana mencari hari setelah sekian hari?", "a": "Seminggu ada 7 hari. Bagi banyak hari dengan 7, lalu majukan hari sebanyak sisanya."}]
    return dict(slug="kpk-dan-fpb-dalam-soal-cerita", dom="B", sort=3,
                std_text="Peserta didik menentukan KPK dan FPB serta menggunakannya untuk menyelesaikan masalah sehari-hari.",
                title="KPK dan FPB dalam Soal Cerita", short_title="KPK dan FPB dalam Soal Cerita",
                meta_desc="Latihan KPK dan FPB untuk kelas 6 SD: mencari KPK dan FPB, jadwal bertemu lagi pada hari dan jam yang sama, dan membagi benda ke paket. 100 soal dengan kunci jawaban.",
                key_big="Bersama lagi: KPK. Dibagi: FPB", key_sub="KPK untuk jadwal, FPB untuk paket terbanyak.",
                body=body, faq=faq, sets=sets)


# ============================================================ 4. pecahan, desimal, dan persen
VALS = [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 5), Fr(2, 5), Fr(3, 5), Fr(4, 5), Fr(1, 10), Fr(3, 10), Fr(7, 10), Fr(9, 10),
        Fr(1, 20), Fr(3, 20), Fr(7, 20), Fr(1, 25), Fr(6, 25), Fr(1, 50), Fr(9, 50), Fr(11, 20), Fr(17, 20), Fr(12, 25), Fr(3, 50)]


def rep(v, kind):
    if kind == "p":
        return f(v.numerator, v.denominator)
    if kind == "d":
        return d2(v * 100)
    return pct(int(v * 100))


def u4(d9):
    ubah = maker(d9, "ubah")

    def ke_persen():
        v = ch(VALS)
        k = ri(0, 2)
        if k == 0:
            return mcq("%s = …%%" % rep(v, "p"), str(int(v * 100)), [str(v.numerator * 10), str(v.denominator), str(int(v * 100) + 10), str(v.numerator)],
                       "%s = %s, jadi %s." % (rep(v, "p"), f(int(v * 100), 100), rep(v, "%")))
        if k == 1:
            return mcq("%s = …" % rep(v, "%"), rep(v, "d"), [d2(v * 10) if v * 10 != int(v * 10) or True else None, num(int(v * 100)), d2(v * 100 + 10)],
                       "%s = %s = %s." % (rep(v, "%"), f(int(v * 100), 100), rep(v, "d")))
        return mcq("Pecahan biasa paling sederhana dari %s adalah …" % rep(v, "d"), rep(v, "p"),
                   [f(int(v * 100), 10) if int(v * 100) % 10 == 0 else f(int(v * 100), 1000), f(v.denominator, v.numerator) if v.numerator > 1 else f(1, v.denominator + 1), f(v.numerator + 1, v.denominator)],
                   "%s = %s = %s." % (rep(v, "d"), f(int(v * 100), 100), rep(v, "p")))

    def banding():
        a, b = pool(VALS)[:2]
        ka, kb = ch(["p", "d", "%"]), ch(["p", "d", "%"])
        if ka == kb or a == b:
            return None
        sa, sb = rep(a, ka), rep(b, kb)
        return stmt(sa, sb, a, b, "Ubah ke bentuk yang sama: %s = %s dan %s = %s, jadi %s %s %s." % (sa, rep(a, "%"), sb, rep(b, "%"), sa, rel(a, b), sb))

    def urut():
        vs = pool(VALS)[:3]
        if len(set(vs)) < 3:
            return None
        kinds = pool(["p", "d", "%"])
        sh = [rep(v, k) for v, k in zip(vs, kinds)]
        up = R().random() < 0.5
        order = sorted(range(3), key=lambda i: vs[i], reverse=not up)
        g = ", ".join(sh[i] for i in order)
        w1 = ", ".join(sh[i] for i in order[::-1])
        w2 = ", ".join(sh)
        w3 = ", ".join(sh[i] for i in [order[1], order[0], order[2]])
        return mcq("Urutan %s dari yang %s adalah …" % (", ".join(sh), "terkecil" if up else "terbesar"), g, [w1, w2, w3, ", ".join(sh[i] for i in [order[0], order[2], order[1]])],
                   "Dalam persen: %s. Urutannya %s." % (", ".join(rep(v, "%") for v in vs), g))

    def terbesar():
        vs = pool(VALS)[:4]
        kinds = [ch(["p", "d", "%"]) for _ in vs]
        big = R().random() < 0.5
        c = max(vs) if big else min(vs)
        sh = [rep(v, k) for v, k in zip(vs, kinds)]
        return mcq("Bilangan %s dari %s adalah …" % ("terbesar" if big else "terkecil", ", ".join(sh)), sh[vs.index(c)], [s for s, v in zip(sh, vs) if v != c],
                   "Dalam persen: %s." % ", ".join(rep(v, "%") for v in vs))

    sets = [("Mengubah ke persen dan desimal", [(ke_persen, 14), (ubah, 6)]),
            ("Pecahan, desimal, dan persen", [(ubah, 14), (ke_persen, 6)]),
            ("Membandingkan", [(banding, 20)]),
            ("Terbesar dan terkecil", [(terbesar, 20)]),
            ("Mengurutkan", [(urut, 20)])]
    body = lesson(
        ["Pecahan, desimal, dan persen bisa menunjukkan nilai yang sama. " + f(1, 4) + " = 0,25 = 25%.",
         "Persen berarti per seratus. Ubah pecahan menjadi penyebut 100 untuk mendapatkan persennya.",
         "Untuk membandingkan, ubah semua ke bentuk yang sama, misalnya semua ke persen atau semua ke desimal."],
        [example("Ubah " + f(3, 5) + " ke persen.", [f(3, 5) + " = " + f(60, 100)], "60%"),
         example("Mana yang lebih besar: 0,7 atau " + f(3, 4) + "?", ["0,7 = 70%", f(3, 4) + " = 75%"], f(3, 4))],
        [["0,7 = 7%", "0,7 = 0,70 = 70%"],
         [f(1, 5) + " = 15%", f(1, 5) + " = " + f(20, 100) + " = 20%"],
         ["Membandingkan angka saja: 0,35 &gt; " + f(1, 2) + " karena 35 &gt; 2", "Ubah dulu: 0,35 = 35% dan " + f(1, 2) + " = 50%"]])
    faq = [{"q": "Bagaimana mengubah pecahan menjadi persen?", "a": "Ubah penyebutnya menjadi 100, lalu pembilangnya adalah persennya. Contoh: 3/4 = 75/100 = 75%."},
           {"q": "Bagaimana mengubah persen menjadi desimal?", "a": "Bagi dengan 100, atau geser koma dua tempat ke kiri. Contoh: 45% = 0,45."},
           {"q": "Bagaimana membandingkan pecahan dan desimal?", "a": "Ubah keduanya ke bentuk yang sama, misalnya ke persen, lalu bandingkan."}]
    return dict(slug="pecahan-desimal-dan-persen", dom="B", sort=4,
                std_text="Peserta didik membandingkan dan mengurutkan berbagai pecahan, termasuk pecahan desimal dan persen, serta mengubah bentuk satu ke bentuk yang lain.",
                title="Membandingkan Pecahan, Desimal, dan Persen", short_title="Pecahan, Desimal, dan Persen",
                meta_desc="Latihan pecahan, desimal, dan persen untuk kelas 6 SD: mengubah bentuk, membandingkan, mencari terbesar dan terkecil, dan mengurutkan. 100 soal dengan kunci jawaban.",
                key_big="1/4 = 0,25 = 25%", key_sub="Ubah ke bentuk yang sama sebelum membandingkan.",
                body=body, faq=faq, sets=sets)


# ============================================================ 5. operasi hitung pecahan
def u5(d7, d8):
    beda, campur7 = maker(d7, "beda"), maker(d7, "campur")
    kali, bagi, campur8 = maker(d8, "kali"), maker(d8, "bagi"), maker(d8, "campur")

    def campuran():
        a, b = ri(2, 6), ri(2, 6)
        if a == b:
            return None
        n = ri(2, 6)
        x = Fr(1, a) + Fr(1, b)
        v = x * n
        q = "(%s + %s) × %d" % (f(1, a), f(1, b), n)
        return mcq("%s = …" % q, fx(v), [fx(Fr(1, a) + Fr(n, b)), fx(Fr(2 * n, a + b)), fx(v + 1), fx(x)],
                   "Kurung dulu: %s + %s = %s. Lalu %s × %d = %s." % (f(1, a), f(1, b), fx(x), fx(x), n, fx(v)))

    sets = [("Penjumlahan dan pengurangan", [(beda, 20)]),
            ("Pecahan campuran", [(campur7, 20)]),
            ("Perkalian pecahan dengan bilangan asli", [(kali, 12), (campur8, 8)]),
            ("Pembagian pecahan dengan bilangan asli", [(bagi, 20)]),
            ("Operasi campuran", [(campuran, 14), (beda, 3), (bagi, 3)])]
    body = lesson(
        ["Untuk menjumlah atau mengurang pecahan berpenyebut berbeda, samakan penyebutnya dengan KPK.",
         "Pecahan × bilangan asli: kalikan pembilangnya. " + f(2, 5) + " × 3 = " + f(6, 5) + " = 1" + f(1, 5) + ".",
         "Pecahan : bilangan asli: kalikan penyebutnya. " + f(3, 4) + " : 2 = " + f(3, 8) + ".",
         "Pada operasi campuran, kerjakan kurung dulu, lalu × dan :, lalu + dan −. Sederhanakan hasilnya."],
        [example(f(2, 3) + " + " + f(1, 4) + " = …", ["KPK 3 dan 4 = 12", f(8, 12) + " + " + f(3, 12)], f(11, 12)),
         example("1" + f(1, 2) + " × 3 = …", ["1" + f(1, 2) + " = " + f(3, 2), f(3, 2) + " × 3 = " + f(9, 2)], "4" + f(1, 2))],
        [[f(1, 2) + " + " + f(1, 3) + " = " + f(2, 5), "Samakan penyebut: " + f(3, 6) + " + " + f(2, 6) + " = " + f(5, 6)],
         [f(2, 5) + " × 3 = " + f(6, 15), "Penyebut tetap: " + f(6, 5)],
         [f(3, 4) + " : 2 = " + f(3, 2), "Penyebut dikali 2: " + f(3, 8)]])
    faq = [{"q": "Bagaimana menjumlahkan pecahan berpenyebut berbeda?", "a": "Samakan penyebutnya dengan KPK kedua penyebut, ubah pembilangnya, lalu jumlahkan pembilang."},
           {"q": "Bagaimana mengalikan pecahan campuran dengan bilangan asli?", "a": "Ubah pecahan campuran menjadi pecahan biasa, kalikan pembilangnya dengan bilangan asli, lalu sederhanakan."},
           {"q": "Mengapa pecahan dibagi bilangan asli menjadi lebih kecil?", "a": "Karena bagian itu dibagi lagi menjadi beberapa bagian. Setengah kue dibagi 2 menjadi seperempat kue."}]
    return dict(slug="operasi-hitung-pecahan", dom="B", sort=5,
                std_text="Peserta didik melakukan operasi penjumlahan dan pengurangan pecahan, serta perkalian dan pembagian pecahan dengan bilangan asli.",
                title="Operasi Hitung Pecahan", short_title="Operasi Hitung Pecahan",
                meta_desc="Latihan operasi hitung pecahan untuk kelas 6 SD: penjumlahan dan pengurangan, pecahan campuran, perkalian dan pembagian pecahan dengan bilangan asli, operasi campuran. 100 soal dengan kunci jawaban.",
                key_big="Samakan penyebut, lalu hitung", key_sub="× asli: kali pembilang. : asli: kali penyebut.",
                body=body, faq=faq, sets=sets)


# ============================================================ 6. operasi hitung desimal
def u6():
    def tambah():
        p = ch([1, 2])
        a, b = ri(11, 999), ri(11, 999)
        if p == 1:
            a, b = a * 10, b * 10
        s = a + b
        w1 = s + (9 if p == 2 else 90)
        return mcq("%s + %s = …" % (d2(a), d2(b)), d2(s), [d2(s + 10), d2(s - 100) if s > 100 else d2(s + 100), d2(s + 100), d2(w1)],
                   "Luruskan koma: %s + %s = %s." % (d2(a), d2(b), d2(s)))

    def beda():
        a, b = ri(100, 999) * 10 if R().random() < 0.5 else ri(1000, 9999), ri(11, 99)
        if b >= a:
            return None
        k = R().random() < 0.5
        if k:
            b *= 10
        s = a - b
        if s <= 0:
            return None
        return mcq("%s − %s = …" % (d2(a), d2(b)), d2(s), [d2(s + 10), d2(s - 10) if s > 10 else d2(s + 100), d2(s + 100), d2(s - 1) if s > 1 else d2(s + 1)],
                   "Luruskan koma dan tambahkan 0 jika perlu: %s − %s = %s." % (d2(a), d2(b), d2(s)))

    def kali():
        a = ri(2, 95)
        n = ri(2, 9)
        if a % 10 == 0:
            return None
        v = a * n
        return mcq("%s × %d = …" % (d2(a), n), d2(v), [d2(v * 10), str(a * n), d2(v + n), d2(v + 100)],
                   "%d × %d = %d, lalu beri koma dua angka dari kanan: %s." % (a, n, v, d2(v)))

    def kali1():
        a = ri(2, 99)
        n = ri(2, 9)
        if a % 10 == 0:
            return None
        v = a * n * 10
        return mcq("%s × %d = …" % (d2(a * 10), n), d2(v), [d2(v * 10), d2(v // 10), d2(v + 10 * n)],
                   "%d × %d = %d, lalu beri koma satu angka dari kanan: %s." % (a, n, a * n, d2(v)))

    def sepuluh():
        a = ri(101, 9999)
        if a % 10 == 0:
            return None
        k = ch([10, 100])
        if R().random() < 0.5:
            return mcq("%s × %d = …" % (d2(a), k), d2(a * k), [d2(a * k * 10), d2(a * k // 10), d2(a)],
                       "Dikali %d, koma bergeser %d tempat ke kanan: %s." % (k, 1 if k == 10 else 2, d2(a * k)))
        return mcq("%s : %d = …" % (d2(a * k), k), d2(a), [d2(a * 10) if k == 100 else d2(a * 100), d2(a * k * 10), d2(a * k)],
                   "Dibagi %d, koma bergeser %d tempat ke kiri: %s." % (k, 1 if k == 10 else 2, d2(a)))

    CER = [("Panjang pita Lina %s m dan pita Siti %s m. Berapa panjang pita mereka jika disambung?", "m", "+"),
           ("Berat beras di karung %s kg. Ibu menambahkan %s kg. Berapa kg beras sekarang?", "kg", "+"),
           ("Tinggi pohon mangga %s m dan tinggi pohon jambu %s m. Berapa selisih tingginya?", "m", "−"),
           ("Botol berisi %s liter air. Sebanyak %s liter diminum. Berapa liter air yang tersisa?", "liter", "−"),
           ("Jarak rumah ke sekolah %s km dan dari sekolah ke pasar %s km. Berapa km jarak rumah ke pasar lewat sekolah?", "km", "+")]

    def cerita():
        t, un, op = ch(CER)
        a, b = ri(105, 995), ri(25, 480)
        if a % 5 or b % 5:
            return None
        if op == "−":
            if b >= a:
                return None
            v = a - b
        else:
            v = a + b
        if op == "+" and R().random() < 0.3:
            k = ri(2, 5)
            return mcq("Satu kantong berisi %s kg gula. Berapa kg gula dalam %d kantong?" % (d2(a), k), u(d2(a * k), "kg"),
                       [u(d2(a * k * 10), "kg"), u(d2(a + k * 100), "kg"), u(d2(a * k + 100), "kg")], "%s × %d = %s kg." % (d2(a), k, d2(a * k)))
        return mcq(t % (d2(a), d2(b)), u(d2(v), un), [u(d2(a - b if op == "+" and a > b else a + b), un), u(d2(v + 10), un), u(d2(v + 100), un)],
                   "%s %s %s = %s %s." % (d2(a), op, d2(b), d2(v), un))

    sets = [("Penjumlahan desimal", [(tambah, 20)]),
            ("Pengurangan desimal", [(beda, 20)]),
            ("Desimal × bilangan asli", [(kali1, 10), (kali, 10)]),
            ("Dikali dan dibagi 10 dan 100", [(sepuluh, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Saat menjumlah atau mengurang desimal, tulis bersusun dengan <b>koma lurus</b> di bawah koma.",
         "Jika banyak angka di belakang koma berbeda, tambahkan 0: 4,5 = 4,50.",
         "Desimal × bilangan asli: kalikan seperti bilangan biasa, lalu beri koma sebanyak angka di belakang koma semula.",
         "Dikali 10 atau 100, koma bergeser ke kanan 1 atau 2 tempat. Dibagi 10 atau 100, koma bergeser ke kiri."],
        [example("3,75 + 2,5 = …", ["3,75 + 2,50", "luruskan koma"], "6,25"),
         example("1,25 × 4 = …", ["125 × 4 = 500", "dua angka di belakang koma: 5,00"], "5")],
        [["3,75 + 2,5 = 4,00 (2,5 ditulis di bawah 75)", "Koma lurus: 3,75 + 2,50 = 6,25"],
         ["0,3 × 4 = 0,12", "3 × 4 = 12, satu angka di belakang koma: 1,2"],
         ["2,5 × 10 = 2,50", "Koma bergeser ke kanan: 25"]])
    faq = [{"q": "Bagaimana menjumlahkan bilangan desimal?", "a": "Tulis bersusun dengan koma sejajar, tambahkan 0 jika perlu, lalu jumlahkan seperti biasa dan beri koma di tempat yang sama."},
           {"q": "Bagaimana mengalikan desimal dengan bilangan asli?", "a": "Abaikan koma dan kalikan, lalu beri koma sebanyak angka di belakang koma pada bilangan desimal."},
           {"q": "Apa yang terjadi jika desimal dikali 100?", "a": "Koma bergeser dua tempat ke kanan. Contoh: 0,45 × 100 = 45."}]
    return dict(slug="operasi-hitung-desimal", dom="B", sort=6,
                std_text="Peserta didik melakukan operasi hitung bilangan desimal dan menggunakannya untuk menyelesaikan masalah pengukuran sehari-hari.",
                title="Operasi Hitung Bilangan Desimal", short_title="Operasi Hitung Desimal",
                meta_desc="Latihan operasi hitung desimal untuk kelas 6 SD: penjumlahan dan pengurangan desimal, desimal dikali bilangan asli, dikali dan dibagi 10 dan 100, soal cerita pengukuran. 100 soal dengan kunci jawaban.",
                key_big="Koma lurus di bawah koma", key_sub="Tambahkan 0 agar banyak angka di belakang koma sama.",
                body=body, faq=faq, sets=sets)


# ============================================================ 7. persen
def u7():
    PS = [10, 20, 25, 50, 75, 5, 30, 40, 60, 15]

    def dari():
        p = ch(PS)
        n = ri(2, 40) * ch([20, 40, 100])
        v = Fr(p * n, 100)
        if v.denominator != 1:
            return None
        v = int(v)
        return mcq("%d%% dari %s = …" % (p, num(n)), num(v), [num(n - v), num(v * 10), num(v + p), num(p * n // 10) if p * n // 10 != v else num(v * 2)],
                   "%d%% dari %s = %s × %s = %s." % (p, num(n), f(p, 100), num(n), num(v)))

    def bagian():
        n = ch([20, 25, 40, 50, 80, 100, 200])
        p = ch(PS)
        k = n * p // 100
        if k * 100 != n * p or k == 0:
            return None
        return mcq("%s dari %s sama dengan …%%" % (num(k), num(n)), str(p), [str(k), str(100 - p), str(p + 5)],
                   "%s = %s = %d%%." % (f(k, n), f(p, 100), p))

    ITEM = ["tas", "sepatu", "baju", "jam tangan", "boneka", "sepeda", "kipas angin", "raket"]

    def diskon():
        p = ch([10, 20, 25, 30, 40, 50])
        price = ri(4, 40) * 10000
        d = price * p // 100
        x = ch(ITEM)
        if R().random() < 0.5:
            return mcq("Harga %s %s. Toko memberi diskon %d%%. Berapa harga yang harus dibayar?" % (x, rp(price), p), rp(price - d),
                       [rp(d), rp(price - p * 1000), rp(price + d), rp(price - d - 1000)],
                       "Diskon = %d%% × %s = %s. Bayar = %s − %s = %s." % (p, rp(price), rp(d), rp(price), rp(d), rp(price - d)))
        return mcq("Harga %s %s dan mendapat diskon %d%%. Berapa besar potongan harganya?" % (x, rp(price), p), rp(d),
                   [rp(price - d), rp(p * 1000), rp(d * 2)],
                   "%d%% × %s = %s." % (p, rp(price), rp(d)))

    CER = ["Di kelas ada %d siswa. Sebanyak %d%% siswa suka sepak bola. Berapa siswa yang suka sepak bola?",
           "Sebuah sekolah punya %d siswa. Sebanyak %d%% siswa naik sepeda ke sekolah. Berapa siswa yang naik sepeda?",
           "Pak Tono menanam %d bibit cabai. Sebanyak %d%% bibit tumbuh. Berapa bibit yang tumbuh?",
           "Ada %d soal ujian. Rina menjawab benar %d%% soal. Berapa soal yang dijawab benar?"]

    def cerita():
        n = ch([20, 25, 40, 50, 60, 80, 120, 200, 240, 300, 400])
        p = ch(PS)
        v = n * p // 100
        if v * 100 != n * p:
            return None
        t = ch(CER)
        if R().random() < 0.4:
            return mcq((t % (n, p)).replace("Berapa siswa yang suka sepak bola?", "Berapa siswa yang tidak suka sepak bola?").replace("Berapa siswa yang naik sepeda?", "Berapa siswa yang tidak naik sepeda?").replace("Berapa bibit yang tumbuh?", "Berapa bibit yang tidak tumbuh?").replace("Berapa soal yang dijawab benar?", "Berapa soal yang dijawab salah?"),
                       num(n - v), [num(v), num(n - p), num(n - v + 10)],
                       "%d%% dari %d = %d. Sisanya %d − %d = %d." % (p, n, v, n, v, n - v))
        return mcq(t % (n, p), num(v), [num(n - v), num(p), num(v + 10), num(n // p) if n // p != v else num(v * 2)],
                   "%d%% dari %d = %s × %d = %d." % (p, n, f(p, 100), n, v))

    def bunga():
        m = ri(2, 20) * 50000
        p = ch([2, 4, 5, 6, 10])
        b = m * p // 100
        return mcq("Rudi menabung %s di bank. Setelah satu tahun ia mendapat bunga %d%%. Berapa besar bunganya?" % (rp(m), p), rp(b),
                   [rp(m + b), rp(b * 10), rp(p * 1000)], "%d%% × %s = %s." % (p, rp(m), rp(b)))

    sets = [("Persen dari suatu bilangan", [(dari, 20)]),
            ("Bagian sebagai persen", [(bagian, 20)]),
            ("Diskon", [(diskon, 20)]),
            ("Soal cerita", [(cerita, 20)]),
            ("Campuran", [(bunga, 6), (dari, 5), (diskon, 5), (cerita, 4)])]
    body = lesson(
        ["Persen artinya per seratus. 25% = " + f(25, 100) + " = " + f(1, 4) + ".",
         "Untuk mencari persen dari suatu bilangan, ubah persen menjadi pecahan, lalu kalikan. 10% berarti dibagi 10.",
         "Diskon adalah potongan harga. Harga bayar = harga awal − diskon."],
        [example("25% dari 80 = …", ["25% = " + f(1, 4), "80 : 4"], "20"),
         example("Harga tas Rp150.000, diskon 20%. Harga bayar?", ["Diskon = 20% × Rp150.000 = Rp30.000", "Rp150.000 − Rp30.000"], "Rp120.000")],
        [["Diskon dianggap harga bayar", "Harga bayar = harga awal − diskon"],
         ["20% dari 50 = 20 × 50 = 1.000", "20% dari 50 = " + f(20, 100) + " × 50 = 10"],
         ["12 dari 40 dianggap 12%", "12 dari 40 = " + f(12, 40) + " = " + f(30, 100) + " = 30%"]])
    faq = [{"q": "Bagaimana cara cepat menghitung 10%?", "a": "Bagi bilangan dengan 10. Contoh: 10% dari Rp45.000 adalah Rp4.500."},
           {"q": "Apa itu diskon?", "a": "Diskon adalah potongan harga dalam persen. Diskon 20% untuk barang Rp50.000 berarti harganya turun Rp10.000."},
           {"q": "Bagaimana mengubah bagian menjadi persen?", "a": "Tulis bagian sebagai pecahan, lalu ubah penyebutnya menjadi 100. Contoh: 9 dari 20 = 45/100 = 45%."}]
    return dict(slug="persen", dom="B", sort=7,
                std_text="Peserta didik menggunakan persen dalam menyelesaikan masalah sehari-hari, misalnya bagian dari suatu jumlah dan potongan harga.",
                title="Persen dalam Kehidupan Sehari-hari", short_title="Persen",
                meta_desc="Latihan persen untuk kelas 6 SD: persen dari suatu bilangan, bagian sebagai persen, diskon, bunga tabungan, dan soal cerita. 100 soal dengan kunci jawaban.",
                key_big="Persen = per seratus", key_sub="Harga bayar = harga awal − diskon.",
                body=body, faq=faq, sets=sets)


# ============================================================ 8. soal cerita pecahan
def u8(d7, d8):
    c7, c8, dari = maker(d7, "cerita"), maker(d8, "cerita"), maker(d8, "dari")

    def kelas():
        k = ch([2, 3, 4, 5, 6])
        a = ri(1, k - 1)
        if math.gcd(a, k) != 1:
            return None
        n = k * ri(5, 9)
        v = n * a // k
        g1, g2 = ch([("laki-laki", "perempuan"), ("suka voli", "suka bulu tangkis"), ("naik sepeda", "jalan kaki"), ("memakai topi", "tidak memakai topi")])
        return mcq("Di aula ada %d anak. Sebanyak %s dari mereka %s, sisanya %s. Berapa anak yang %s?" % (n, f(a, k), g1, g2, g2), str(n - v),
                   [str(v), str(n - a), str(n // k), str(n - v + 1)],
                   "%s dari %d = %d. Yang %s = %d − %d = %d." % (f(a, k), n, v, g2, n, v, n - v))

    def sisa():
        k = ch([4, 5, 8, 10])
        w = ri(2, 5)
        a = ri(1, k - 1)
        tot = Fr(w)
        used = Fr(a, k)
        s = tot - used
        what = ch([("gula", "kg"), ("tepung", "kg"), ("minyak", "liter"), ("susu", "liter")])
        return mcq("Ibu punya %d %s %s. Sebanyak %s %s dipakai untuk membuat kue. Berapa %s %s yang tersisa?" % (w, what[1], what[0], f(a, k), what[1], what[1], what[0]),
                   fx(s) + " " + what[1], [fx(Fr(w - a, k)) + " " + what[1] if w > a else fx(s + 1) + " " + what[1], fx(s - 1) + " " + what[1] if s > 1 else fx(s + Fr(1, k)) + " " + what[1], fx(used) + " " + what[1]],
                   "%d − %s = %s %s." % (w, f(a, k), fx(s), what[1]))

    def dua():
        n = ri(2, 6) * 24
        a = ch([2, 3, 4])
        b = ch([2, 3, 4])
        x = K().next()
        first = n // a
        rest = n - first
        second = rest // b
        if rest % b:
            return None
        return mcq("%s punya %d kelereng. %s bagian diberikan kepada adiknya, lalu %s dari sisanya diberikan kepada temannya. Berapa kelereng %s sekarang?"
                   % (x, n, f(1, a), f(1, b), x), str(rest - second),
                   [str(n - n // a - n // b), str(rest), str(second), str(rest - second + 2)],
                   "Adik: %d : %d = %d, sisa %d. Teman: %d : %d = %d. Sekarang %d − %d = %d." % (n, a, first, rest, rest, b, second, rest, second, rest - second))

    sets = [("Pecahan dari suatu jumlah", [(dari, 14), (kelas, 6)]),
            ("Bagian yang lain", [(kelas, 14), (dari, 6)]),
            ("Penjumlahan dan pengurangan", [(c7, 12), (sisa, 8)]),
            ("Perkalian dan pembagian", [(c8, 20)]),
            ("Soal dua langkah", [(dua, 14), (sisa, 6)])]
    body = lesson(
        ["Bacalah soal dan tentukan dulu: bagian dari suatu jumlah (dikali), digabung (dijumlah), sisa (dikurang), atau dibagi rata (dibagi).",
         "Pecahan dari suatu jumlah: bagi dengan penyebut, lalu kali pembilang. " + f(3, 4) + " dari 20 = 20 : 4 × 3 = 15.",
         "Jika soal memakai kata <i>sisanya</i>, hitung dulu bagian pertama, lalu kurangkan."],
        [example(f(2, 5) + " dari 35 siswa suka menggambar. Berapa yang tidak suka?", ["35 : 5 × 2 = 14", "35 − 14"], "21 siswa"),
         example("Ada 3 kg tepung, dipakai " + f(3, 4) + " kg. Sisanya?", ["3 = 2" + f(4, 4), "2" + f(4, 4) + " − " + f(3, 4)], "2" + f(1, 4) + " kg")],
        [["Menjawab bagian yang ditanya pertama saja", "Baca lagi: yang ditanya bagian yang lain atau sisanya"],
         [f(1, 3) + " dari sisa dihitung dari jumlah awal", "Hitung dari sisa, bukan dari jumlah awal"],
         ["3 − " + f(3, 4) + " = " + f(0, 4), "Ubah 3 menjadi 2" + f(4, 4) + " lalu kurangkan"]])
    faq = [{"q": "Bagaimana menghitung pecahan dari suatu jumlah?", "a": "Bagi jumlah itu dengan penyebut, lalu kalikan dengan pembilang. Contoh: 2/3 dari 24 = 24 : 3 × 2 = 16."},
           {"q": "Apa arti 'dari sisanya'?", "a": "Bagian kedua dihitung dari yang tersisa setelah bagian pertama diambil, bukan dari jumlah awal."},
           {"q": "Bagaimana memeriksa jawaban soal cerita?", "a": "Masukkan jawaban ke cerita. Jumlah semua bagian harus sama dengan jumlah awal."}]
    return dict(slug="soal-cerita-pecahan", dom="B", sort=8,
                std_text="Peserta didik menyelesaikan masalah sehari-hari yang melibatkan operasi hitung pecahan.",
                title="Soal Cerita Pecahan", short_title="Soal Cerita Pecahan",
                meta_desc="Latihan soal cerita pecahan untuk kelas 6 SD: pecahan dari suatu jumlah, bagian yang lain, sisa, perkalian dan pembagian pecahan, soal dua langkah. 100 soal dengan kunci jawaban.",
                key_big="3/4 dari 20 = 20 : 4 × 3", key_sub="Kata 'sisanya': hitung dari yang tersisa.",
                body=body, faq=faq, sets=sets)


# ============================================================ 9. perbandingan dan skala
def u9(d13):
    sederhana, bagian, tabel = (maker(d13, x) for x in ("sederhana", "bagian", "tabel"))

    def skala_cm():
        km = ch([1, 2, 5, 10, 20, 25, 50])
        cm = ri(2, 15)
        x, y = ch([("Kota A", "Kota B"), ("Desa Suka", "Desa Maju"), ("Rumah Putu", "pantai"), ("Sekolah", "museum"), ("Pelabuhan", "bandara")])
        return mcq("Pada peta, 1 cm mewakili %d km. Jarak %s ke %s pada peta %d cm. Berapa jarak sebenarnya?" % (km, x, y, cm), u(cm * km, "km"),
                   [u(cm + km, "km"), u(cm * km * 10, "km"), u(cm * km + km, "km")], "%d × %d km = %d km." % (cm, km, cm * km))

    def skala():
        s = ch([100, 200, 500, 1000, 50000, 100000, 200000, 500000, 1000000])
        cm = ri(2, 12)
        real = cm * s
        if s <= 1000:
            ans = real / 100.0
            unit = "m"
        else:
            ans = real / 100000.0
            unit = "km"
        txt = (num(int(ans)) if ans == int(ans) else str(ans).replace(".", ",")) + " " + unit
        bad = [(num(int(ans * 10)) if ans * 10 == int(ans * 10) else str(ans * 10).replace(".", ",")) + " " + unit,
               (num(int(ans / 10)) if ans / 10 == int(ans / 10) else str(ans / 10).replace(".", ",")) + " " + unit,
               num(real) + " " + unit]
        return mcq("Skala sebuah %s 1 : %s. Jarak pada %s %d cm. Berapa jarak sebenarnya?" % ("denah" if s <= 1000 else "peta", num(s), "denah" if s <= 1000 else "peta", cm), txt, bad,
                   "%d cm × %s = %s cm = %s." % (cm, num(s), num(real), txt))

    def peta_cm():
        km = ch([2, 5, 10, 20, 25])
        d = km * ri(2, 12)
        return mcq("Pada peta, 1 cm mewakili %d km. Jarak sebenarnya dua kota %d km. Berapa cm jarak pada peta?" % (km, d), u(d // km, "cm"),
                   [u(d * km, "cm"), u(d - km, "cm"), u(d // km + 1, "cm")], "%d : %d = %d cm." % (d, km, d // km))

    def denah():
        s = ch([100, 200, 500])
        p, l = ri(2, 9), ri(2, 9)
        if p == l:
            return None
        P, L = p * s // 100, l * s // 100
        return mcq("Denah kamar berskala 1 : %d. Ukuran kamar pada denah %d cm × %d cm. Berapa ukuran sebenarnya?" % (s, p, l), "%d m × %d m" % (P, L),
                   ["%d cm × %d cm" % (p * s, l), "%d m × %d m" % (p * s // 10, l * s // 10), "%d m × %d m" % (P + 1, L + 1)],
                   "%d cm × %d = %d cm = %d m, dan %d cm × %d = %d cm = %d m." % (p, s, p * s, P, l, s, l * s, L))

    sets = [("Perbandingan sederhana", [(sederhana, 20)]),
            ("Mencari bagian dari perbandingan", [(bagian, 14), (tabel, 6)]),
            ("1 cm mewakili …", [(skala_cm, 14), (peta_cm, 6)]),
            ("Skala peta dan denah", [(skala, 14), (denah, 6)]),
            ("Campuran", [(tabel, 6), (peta_cm, 7), (denah, 7)])]
    body = lesson(
        ["Perbandingan atau rasio membandingkan dua banyak benda, misalnya 2 : 3. Perbandingan bisa disederhanakan dengan membagi keduanya dengan FPB.",
         "Skala adalah perbandingan jarak pada peta dengan jarak sebenarnya. Skala 1 : 100.000 berarti 1 cm pada peta = 100.000 cm sebenarnya = 1 km.",
         "Jarak sebenarnya = jarak pada peta × skala. Jarak pada peta = jarak sebenarnya : skala."],
        [example("Skala 1 : 500.000. Jarak pada peta 4 cm. Jarak sebenarnya?", ["4 × 500.000 = 2.000.000 cm", "2.000.000 cm = 20 km"], "20 km"),
         example("Perbandingan kelereng Asep dan Beni 2 : 3. Jumlahnya 25. Kelereng Beni?", ["2 + 3 = 5 bagian", "25 : 5 = 5, Beni 3 × 5"], "15")],
        [["Lupa mengubah cm ke km", "100.000 cm = 1 km"],
         ["Skala 1 : 200 dianggap 1 cm = 200 m", "1 cm = 200 cm = 2 m"],
         ["Perbandingan 2 : 3 dari 25 dihitung 25 : 2", "Jumlahkan bagiannya dulu: 2 + 3 = 5"]])
    faq = [{"q": "Apa arti skala 1 : 100.000?", "a": "Setiap 1 cm pada peta mewakili 100.000 cm atau 1 km jarak sebenarnya."},
           {"q": "Bagaimana mengubah cm ke km?", "a": "1 km = 100.000 cm. Bagi dengan 100.000, atau hapus lima angka nol."},
           {"q": "Apa itu denah?", "a": "Denah adalah gambar tampak atas sebuah ruangan, rumah, atau tempat dengan skala tertentu."}]
    return dict(slug="perbandingan-dan-skala", dom="A", sort=9,
                std_text="Peserta didik menggunakan rasio atau perbandingan untuk membandingkan dua besaran, termasuk skala pada peta dan denah.",
                title="Perbandingan dan Skala", short_title="Perbandingan dan Skala",
                meta_desc="Latihan perbandingan dan skala untuk kelas 6 SD: menyederhanakan perbandingan, mencari bagian, skala peta dan denah, jarak sebenarnya dan jarak pada peta. 100 soal dengan kunci jawaban.",
                key_big="Jarak sebenarnya = peta × skala", key_sub="1 : 100.000 berarti 1 cm = 1 km.",
                body=body, faq=faq, sets=sets)


# ============================================================ 10. pola bilangan
def dots(kind, n):
    s = []
    if kind == "segitiga":
        for r in range(n):
            for c in range(r + 1):
                s.append((c * 14 - r * 7, r * 13))
    elif kind == "persegi":
        for r in range(n):
            for c in range(n):
                s.append((c * 14, r * 14))
    else:
        for r in range(n):
            for c in range(n + 1):
                s.append((c * 14, r * 14))
    return s


def dots_svg(kind, k=4):
    parts, x = [], 10
    H = 0
    for n in range(1, k + 1):
        pts = dots(kind, n)
        mnx = min(p[0] for p in pts)
        mxx = max(p[0] for p in pts)
        for (a, b) in pts:
            parts.append("<circle cx='%d' cy='%d' r='5' fill='#e07a5f' stroke='%s'/>" % (x + a - mnx + 6, 30 + b, INK))
        H = max(H, max(p[1] for p in pts) + 50)
        parts.append(text(x + (mxx - mnx) / 2 + 6, 16, "ke-%d" % n, 12, weight=700))
        x += mxx - mnx + 44
    return wrap(x, H, "".join(parts), "pola titik %s" % kind)


def u10(d12):
    aturan, tengah, cerita = maker(d12, "aturan"), maker(d12, "tengah"), maker(d12, "cerita")
    MKS = [m for m in (maker(d12, "mk", 0), maker(d12, "mk", 1))]

    def konfig():
        kind = ch(["segitiga", "persegi", "persegi panjang"])
        n = ri(5, 13)
        if kind == "segitiga":
            v, rule = n * (n + 1) // 2, "1, 3, 6, 10, … (bertambah 2, 3, 4, …)"
            ws = [n * n, v + n, v - n + 1]
        elif kind == "persegi":
            v, rule = n * n, "1, 4, 9, 16, … (n × n)"
            ws = [n * (n + 1) // 2, 4 * n, v + 2 * n + 1]
        else:
            v, rule = n * (n + 1), "2, 6, 12, 20, … (n × (n + 1))"
            ws = [n * n, (n + 1) * (n + 2), 2 * n + 1]
        return mcq("Perhatikan pola titik berikut. Berapa banyak titik pada pola ke-%d?%s" % (n, dots_svg(kind)), str(v), [str(w) for w in ws],
                   "Polanya %s. Pola ke-%d = %d." % (rule, n, v))

    def suku():
        a, d = ri(1, 20), ri(2, 9)
        n = ri(10, 30)
        xs = [a + d * i for i in range(4)]
        v = a + d * (n - 1)
        return mcq("Pola: %s, … Berapa bilangan ke-%d?" % (", ".join(map(str, xs)), n), num(v), [num(a + d * n), num(d * n), num(v - d * 2), num(a * n)],
                   "Bertambah %d. Bilangan ke-%d = %d + (%d − 1) × %d = %s." % (d, n, a, n, d, num(v)))

    def ganjil():
        n = ri(5, 15)
        k = R().random() < 0.5
        if k:
            return mcq("Jumlah %d bilangan ganjil pertama (1 + 3 + 5 + …) adalah …" % n, str(n * n), [str(n * (n + 1)), str(2 * n - 1), str(n * n + n - 1)],
                       "Jumlah n bilangan ganjil pertama = n × n = %d × %d = %d." % (n, n, n * n))
        return mcq("Bilangan ganjil ke-%d adalah …" % n, str(2 * n - 1), [str(2 * n + 1), str(2 * n), str(n + 1)],
                   "Bilangan ganjil ke-n = 2 × n − 1 = %d." % (2 * n - 1))

    def dua():
        a, p, q = ri(10, 40), ri(3, 9), ri(1, 4)
        if p == q:
            return None
        xs = [a]
        for i in range(6):
            xs.append(xs[-1] + (p if i % 2 == 0 else -q))
        v = xs[-1] + p
        return mcq("Pola: %s, … Bilangan berikutnya adalah …" % ", ".join(map(str, xs)), str(v), [str(xs[-1] - q), str(v + p), str(xs[-1] + p - q)],
                   "Aturannya bergantian +%d, −%d. Berikutnya %d + %d = %d." % (p, q, xs[-1], p, v))

    sets = [("Pola dikali dan dibagi", [(MKS[0], 10), (MKS[1], 10)]),
            ("Aturan dan bilangan yang hilang", [(aturan, 10), (tengah, 10)]),
            ("Bilangan ke-n", [(suku, 14), (ganjil, 6)]),
            ("Pola titik", [(konfig, 20)]),
            ("Pola dua aturan dan soal cerita", [(dua, 10), (cerita, 10)])]
    body = lesson(
        ["Pola bilangan bisa bertambah atau berkurang tetap, dikali atau dibagi, atau mengikuti dua aturan bergantian.",
         "Untuk mencari bilangan jauh di depan, misalnya ke-25, gunakan aturan: bilangan pertama + (n − 1) × selisih.",
         "Pola titik punya nama: bilangan segitiga (1, 3, 6, 10, …), bilangan persegi (1, 4, 9, 16, …), dan bilangan persegi panjang (2, 6, 12, 20, …)."],
        [example("4, 7, 10, 13, … Bilangan ke-20?", ["Selisih 3", "4 + 19 × 3 = 4 + 57"], "61"),
         example("Bilangan persegi ke-8?", ["8 × 8"], "64")],
        [["Bilangan ke-20 dihitung 20 × 3", "Mulai dari bilangan pertama: 4 + 19 × 3"],
         ["Pola 1, 3, 6, 10 dianggap selalu +2", "Selisihnya bertambah: +2, +3, +4"],
         ["Hanya memakai satu aturan pada pola bergantian", "Periksa selisih semua pasangan"]])
    faq = [{"q": "Bagaimana mencari bilangan ke-n pada pola?", "a": "Jika selisihnya tetap, bilangan ke-n = bilangan pertama + (n − 1) × selisih."},
           {"q": "Apa itu bilangan persegi?", "a": "Bilangan yang titiknya bisa disusun menjadi persegi: 1, 4, 9, 16, 25, … yaitu n × n."},
           {"q": "Apa itu bilangan segitiga?", "a": "Bilangan yang titiknya bisa disusun menjadi segitiga: 1, 3, 6, 10, 15, … Selisihnya bertambah 1 setiap langkah."}]
    return dict(slug="pola-bilangan-dan-pola-titik", dom="A", sort=10,
                std_text="Peserta didik mengidentifikasi, meniru, dan mengembangkan pola bilangan yang melibatkan operasi hitung, serta menentukan bilangan ke-n dari suatu pola.",
                title="Pola Bilangan dan Pola Titik", short_title="Pola Bilangan dan Pola Titik",
                meta_desc="Latihan pola bilangan untuk kelas 6 SD: pola dikali dan dibagi, aturan pola, bilangan ke-n, bilangan segitiga dan persegi, pola dua aturan. 100 soal dengan kunci jawaban.",
                key_big="Ke-n = pertama + (n − 1) × selisih", key_sub="Bilangan persegi: 1, 4, 9, 16, …",
                body=body, faq=faq, sets=sets)


# ============================================================ 11. persamaan sederhana
BX = "<span style='display:inline-block;width:1.4em;border:2px solid #333;border-radius:3px'>&nbsp;</span>"


def u11(d11):
    kali, bagi, campur, model, selesai = (maker(d11, x) for x in ("kali", "bagi", "campur", "model", "selesai"))

    def dua():
        a, x = ri(2, 9), ri(2, 15)
        b = ri(1, 30)
        k = ri(0, 2)
        if k == 0:
            c = a * x + b
            q = "%d × %s + %d = %d" % (a, BX, b, c)
            ws = [(c + b) // a if (c + b) % a == 0 else c - b, c - b, x + 1]
            e = "%d × %s = %d − %d = %d, jadi %s = %d : %d = %d." % (a, BX, c, b, c - b, BX, c - b, a, x)
        elif k == 1:
            c = a * x - b
            if c <= 0:
                return None
            q = "%d × %s − %d = %d" % (a, BX, b, c)
            ws = [(c - b) // a if c > b and (c - b) % a == 0 else c + b, c + b, x - 1]
            e = "%d × %s = %d + %d = %d, jadi %s = %d : %d = %d." % (a, BX, c, b, c + b, BX, c + b, a, x)
        else:
            y = x * a
            c = x + b
            q = "%s : %d + %d = %d" % (BX, a, b, c)
            ws = [(c - b) // a if (c - b) % a == 0 else c * a, c * a, x]
            x = y
            e = "%s : %d = %d − %d = %d, jadi %s = %d × %d = %d." % (BX, a, c, b, c - b, BX, c - b, a, y)
        return mcq("Bilangan yang tepat untuk kotak: %s" % q, str(x), [str(w) for w in ws if w > 0] + [str(x + 1), str(x - 1)], e)

    BENDA = [("kotak pensil", "pensil"), ("kantong", "kelereng"), ("keranjang", "jeruk"), ("bungkus", "permen")]

    def timbang():
        wadah, isi = ch(BENDA)
        a, x, b = ri(2, 6), ri(3, 12), ri(1, 9)
        tot = a * x + b
        return mcq("Ada %d %s berisi sama banyak %s dan %d %s lepas. Jumlah semuanya %d %s. Kalimat matematika dan jawabannya yang tepat adalah …"
                   % (a, wadah, isi, b, isi, tot, isi),
                   "%d × %s + %d = %d, %s = %d" % (a, BX, b, tot, BX, x),
                   ["%d + %s + %d = %d, %s = %d" % (a, BX, b, tot, BX, tot - a - b), "%d × %s = %d, %s = %d" % (a, BX, tot, BX, tot // a) if tot % a == 0 else "%d × %s − %d = %d, %s = %d" % (a, BX, b, tot, BX, (tot + b) // a),
                    "%d × %s + %d = %d, %s = %d" % (a, BX, b, tot, BX, x + 1)],
                   "%d × %s = %d − %d = %d, jadi %s = %d." % (a, BX, tot, b, tot - b, BX, x))

    sets = [("Kotak pada perkalian dan pembagian", [(kali, 10), (bagi, 10)]),
            ("Kedua ruas sama", [(campur, 20)]),
            ("Persamaan dua langkah", [(dua, 20)]),
            ("Membuat kalimat matematika", [(model, 12), (timbang, 8)]),
            ("Soal cerita", [(selesai, 12), (timbang, 8)])]
    body = lesson(
        ["Kalimat matematika dengan tanda = adalah persamaan. Kotak □ adalah bilangan yang belum diketahui.",
         "Untuk mencari □, gunakan operasi kebalikan: + dengan −, × dengan :.",
         "Pada persamaan dua langkah seperti 3 × □ + 5 = 26, kerjakan mundur: kurangi 5 dulu, lalu bagi 3."],
        [example("3 × □ + 5 = 26", ["3 × □ = 26 − 5 = 21", "□ = 21 : 3"], "7"),
         example("□ : 4 − 2 = 6", ["□ : 4 = 6 + 2 = 8", "□ = 8 × 4"], "32")],
        [["3 × □ + 5 = 26, langsung 26 : 3", "Kurangi 5 dulu: 21 : 3 = 7"],
         ["□ : 4 = 8 dijawab 2", "Kebalikan dari : adalah ×: 8 × 4 = 32"],
         ["Tidak memeriksa jawaban", "Masukkan jawaban: 3 × 7 + 5 = 26 ✓"]])
    faq = [{"q": "Apa itu persamaan?", "a": "Persamaan adalah kalimat matematika yang memakai tanda sama dengan, dan ada bilangan yang belum diketahui."},
           {"q": "Bagaimana menyelesaikan persamaan dua langkah?", "a": "Kerjakan mundur dengan operasi kebalikan. Hilangkan penjumlahan atau pengurangan dulu, lalu perkalian atau pembagian."},
           {"q": "Bagaimana memeriksa jawaban?", "a": "Ganti kotak dengan jawabanmu dan hitung. Jika kedua ruas sama, jawabannya benar."}]
    return dict(slug="persamaan-sederhana", dom="A", sort=11,
                std_text="Peserta didik menemukan nilai yang belum diketahui dalam kalimat matematika yang berkaitan dengan operasi hitung bilangan cacah sampai 100.",
                title="Persamaan Sederhana", short_title="Persamaan Sederhana",
                meta_desc="Latihan persamaan sederhana untuk kelas 6 SD: kotak pada perkalian dan pembagian, kedua ruas sama, persamaan dua langkah, membuat kalimat matematika dari cerita. 100 soal dengan kunci jawaban.",
                key_big="Kerjakan mundur dengan kebalikan", key_sub="3 × □ + 5 = 26 → □ = (26 − 5) : 3 = 7.",
                body=body, faq=faq, sets=sets)


# ============================================================ 12. luas bangun datar dan gabungan
def u12(d14):
    gabung, segitiga, jajar, cerita = (maker(d14, x) for x in ("gabung", "segitiga", "jajar", "cerita"))

    def trapesium():
        a, b, t = ri(3, 10), ri(5, 16), ri(2, 9)
        if b <= a or (a + b) % 2 and t % 2:
            return None
        L = (a + b) * t // 2
        off = (b - a) // 2
        sc = 1.0 if b <= 10 else 0.7
        svg = shape_svg([(0, t), (b, t), (off + a, 0), (off, 0)],
                        [(off + a / 2.0, -0.6, "%d cm" % a), (b / 2.0, t + 0.9, "%d cm" % b), (off + 1.4, t / 2.0, "%d cm" % t)],
                        dashed=[((off, 0), (off, t))], right=[(off, t, 1, -1)], sc=sc, label="trapesium")
        return mcq("Berapa luas trapesium ini?" + svg, "%d cm²" % L, ["%d cm²" % ((a + b) * t), "%d cm²" % (a * b * t // 2 if a * b * t % 2 == 0 else a + b + t), "%d cm²" % (a + b + 2 * t)],
                   "L = (a + b) × t : 2 = (%d + %d) × %d : 2 = %d cm²." % (a, b, t, L))

    def layang():
        d1, d2_ = ri(4, 16), ri(4, 16)
        if d1 * d2_ % 2:
            return None
        nm = ch(["layang-layang", "belah ketupat"])
        L = d1 * d2_ // 2
        return mcq("Diagonal sebuah %s %d cm dan %d cm. Berapa luasnya?" % (nm, d1, d2_), "%d cm²" % L, ["%d cm²" % (d1 * d2_), "%d cm²" % (d1 + d2_), "%d cm²" % (2 * (d1 + d2_))],
                   "L = d₁ × d₂ : 2 = %d × %d : 2 = %d cm²." % (d1, d2_, L))

    sets = [("Segitiga dan jajargenjang", [(segitiga, 10), (jajar, 10)]),
            ("Trapesium", [(trapesium, 20)]),
            ("Layang-layang dan belah ketupat", [(layang, 20)]),
            ("Bangun gabungan", [(gabung, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Luas segitiga = alas × tinggi : 2. Luas jajargenjang = alas × tinggi.",
         "Luas trapesium = (jumlah sisi sejajar) × tinggi : 2. Luas layang-layang dan belah ketupat = diagonal × diagonal : 2.",
         "Bangun gabungan dipecah menjadi bangun yang sudah dikenal, lalu luasnya dijumlahkan (atau dikurangkan jika ada bagian yang dibuang)."],
        [example("Trapesium dengan sisi sejajar 6 cm dan 10 cm, tinggi 4 cm.", ["(6 + 10) × 4 : 2 = 16 × 4 : 2"], "32 cm²"),
         example("Layang-layang dengan diagonal 8 cm dan 12 cm.", ["8 × 12 : 2"], "48 cm²")],
        [["Lupa dibagi 2 pada segitiga dan trapesium", "Luas segitiga = alas × tinggi : 2"],
         ["Memakai sisi miring sebagai tinggi", "Tinggi tegak lurus dengan alas"],
         ["Satuan luas ditulis cm", "Satuan luas adalah cm² atau m²"]])
    faq = [{"q": "Apa rumus luas trapesium?", "a": "Luas trapesium = (sisi sejajar pertama + sisi sejajar kedua) × tinggi : 2."},
           {"q": "Apa rumus luas layang-layang?", "a": "Luas layang-layang = diagonal pertama × diagonal kedua : 2. Rumus ini juga berlaku untuk belah ketupat."},
           {"q": "Bagaimana menghitung luas bangun gabungan?", "a": "Pecah bangun menjadi beberapa bangun sederhana, hitung luas masing-masing, lalu jumlahkan."}]
    return dict(slug="luas-bangun-datar-dan-gabungan", dom="P", sort=12,
                std_text="Peserta didik menentukan luas berbagai bentuk bangun datar (segitiga, segi empat, segi banyak) serta gabungannya.",
                title="Luas Bangun Datar dan Bangun Gabungan", short_title="Luas Bangun Datar dan Gabungan",
                meta_desc="Latihan luas bangun datar untuk kelas 6 SD: segitiga, jajargenjang, trapesium, layang-layang, belah ketupat, bangun gabungan, dan soal cerita. 100 soal dengan kunci jawaban.",
                key_big="Trapesium: (a + b) × t : 2", key_sub="Bangun gabungan: pecah, hitung, lalu jumlahkan.",
                body=body, faq=faq, sets=sets)


# ============================================================ 13. sudut dan segitiga
def tri_svg(A_, B_, angles_shown):
    """sudut A dan B di alas, C di atas"""
    import math as M
    base = 220.0
    a, b = M.radians(A_), M.radians(B_)
    # titik C: perpotongan
    t = base * M.sin(b) / M.sin(a + b)
    cx, cy = t * M.cos(a), t * M.sin(a)
    if cy > 170:
        sc = 170 / cy
    else:
        sc = 1.0
    P = [(30, 190), (30 + base * sc, 190), (30 + cx * sc, 190 - cy * sc)]
    xs = [p[0] for p in P]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (" ".join("%.1f,%.1f" % p for p in P), FILL, GREEN)]
    lab = [(P[0][0] + 26, P[0][1] - 8), (P[1][0] - 30, P[1][1] - 8), (P[2][0], P[2][1] + 30)]
    for (x, y), t_ in zip(lab, angles_shown):
        s.append(text(x, y, t_, 13, weight=700))
    W = max(xs) + 40
    return fig(lg(svg_wrap(int(max(W, 290)), 210, "".join(s), "segitiga")))


def u13(d15):
    jenis, pelurus, potong = maker(d15, "jenis"), maker(d15, "pelurus"), maker(d15, "potong")

    def ketiga():
        a, b = ri(25, 100), ri(25, 100)
        c = 180 - a - b
        if c < 20:
            return None
        k = ri(0, 2)
        shown = [("%d°" % a, "%d°" % b, "?"), ("?", "%d°" % b, "%d°" % c), ("%d°" % a, "?", "%d°" % c)][k]
        v = [c, a, b][k]
        known = [x for x in (a, b, c) if x != v] if [a, b, c].count(v) == 1 else None
        if known is None or len(known) != 2:
            return None
        return mcq("Berapa besar sudut yang ditandai ? pada segitiga ini?" + tri_svg(a, b, shown), "%d°" % v,
                   ["%d°" % (360 - sum(known)), "%d°" % (90 - known[0]) if known[0] < 90 else "%d°" % (v + 10), "%d°" % (sum(known)), "%d°" % (v + 10)],
                   "Jumlah sudut segitiga 180°. 180° − %d° − %d° = %d°." % (known[0], known[1], v))

    def jenis_sudut():
        a, b = ri(20, 110), ri(20, 110)
        c = 180 - a - b
        if c < 10:
            return None
        mx = max(a, b, c)
        g = "segitiga siku-siku" if mx == 90 else "segitiga tumpul" if mx > 90 else "segitiga lancip"
        return mcq("Sebuah segitiga punya sudut %d°, %d°, dan %d°. Segitiga itu adalah …" % (a, b, c), g,
                   [x for x in ["segitiga lancip", "segitiga siku-siku", "segitiga tumpul", "segitiga sama sisi"] if x != g],
                   "Sudut terbesarnya %d°, %s, jadi %s." % (mx, "tepat 90°" if mx == 90 else "lebih dari 90°" if mx > 90 else "kurang dari 90°", g))

    def sisi():
        k = ri(0, 2)
        if k == 0:
            a = ri(3, 15)
            s = (a, a, a)
            g = "segitiga sama sisi"
        elif k == 1:
            a, b = ri(4, 15), ri(3, 15)
            if a == b or 2 * a <= b:
                return None
            s = (a, a, b)
            g = "segitiga sama kaki"
        else:
            a, b, c = sorted([ri(3, 15), ri(3, 15), ri(3, 15)])
            if len({a, b, c}) < 3 or a + b <= c:
                return None
            s = (a, b, c)
            g = "segitiga sembarang"
        s = pool(s)
        return mcq("Panjang sisi sebuah segitiga %d cm, %d cm, dan %d cm. Segitiga itu adalah …" % tuple(s), g,
                   [x for x in ["segitiga sama sisi", "segitiga sama kaki", "segitiga sembarang", "segitiga siku-siku"] if x != g],
                   "%s." % {"segitiga sama sisi": "Ketiga sisinya sama panjang", "segitiga sama kaki": "Dua sisinya sama panjang", "segitiga sembarang": "Ketiga sisinya berbeda"}[g])

    def sama_kaki():
        a = ri(20, 80) * 2 // 2
        if R().random() < 0.5:
            top = 180 - 2 * a
            if top <= 0:
                return None
            return mcq("Pada segitiga sama kaki, kedua sudut alasnya masing-masing %d°. Berapa besar sudut puncaknya?" % a, "%d°" % top,
                       ["%d°" % (180 - a), "%d°" % (90 - a) if a < 90 else "%d°" % (top + 10), "%d°" % (360 - 2 * a)], "180° − %d° − %d° = %d°." % (a, a, top))
        top = ri(10, 80) * 2
        base = (180 - top) // 2
        return mcq("Sudut puncak segitiga sama kaki %d°. Berapa besar setiap sudut alasnya?" % top, "%d°" % base,
                   ["%d°" % (180 - top), "%d°" % top, "%d°" % (base + 10)], "(180° − %d°) : 2 = %d°." % (top, base))

    sets = [("Jenis sudut", [(jenis, 20)]),
            ("Sudut berpelurus dan bertolak belakang", [(pelurus, 10), (potong, 10)]),
            ("Jumlah sudut segitiga", [(ketiga, 20)]),
            ("Jenis segitiga", [(jenis_sudut, 10), (sisi, 10)]),
            ("Segitiga sama kaki", [(sama_kaki, 12), (ketiga, 8)])]
    body = lesson(
        ["Jumlah ketiga sudut dalam segitiga selalu 180°. Jika dua sudut diketahui, sudut ketiga = 180° − sudut pertama − sudut kedua.",
         "Menurut sudutnya: segitiga lancip (semua sudut &lt; 90°), siku-siku (ada sudut 90°), dan tumpul (ada sudut &gt; 90°).",
         "Menurut sisinya: segitiga sama sisi (3 sisi sama), sama kaki (2 sisi sama), dan sembarang (semua berbeda). Pada segitiga sama kaki, kedua sudut alasnya sama besar."],
        [example("Dua sudut segitiga 65° dan 45°. Sudut ketiga?", ["180° − 65° − 45°"], "70°"),
         example("Sudut puncak segitiga sama kaki 40°. Sudut alasnya?", ["(180° − 40°) : 2"], "70°")],
        [["Jumlah sudut segitiga dianggap 360°", "Segitiga 180°, segi empat 360°"],
         ["Segitiga dengan sudut 100° disebut lancip", "Ada sudut lebih dari 90°, jadi tumpul"],
         ["Sudut alas sama kaki dihitung 180° − 40°", "Sisa 140° dibagi dua sudut: 70°"]])
    faq = [{"q": "Berapa jumlah sudut dalam segitiga?", "a": "Jumlah ketiga sudut dalam segitiga selalu 180°."},
           {"q": "Apa itu segitiga tumpul?", "a": "Segitiga yang salah satu sudutnya lebih besar dari 90°."},
           {"q": "Apa ciri segitiga sama kaki?", "a": "Dua sisinya sama panjang, dan dua sudut di depan sisi itu (sudut alas) sama besar."}]
    return dict(slug="sudut-dan-segitiga", dom="G", sort=13,
                std_text="Peserta didik mengukur besar sudut dan membandingkan karakteristik antarbangun datar, termasuk jenis-jenis segitiga.",
                title="Sudut dan Jenis Segitiga", short_title="Sudut dan Segitiga",
                meta_desc="Latihan sudut dan segitiga untuk kelas 6 SD: jenis sudut, sudut berpelurus, jumlah sudut segitiga 180°, segitiga lancip, siku-siku, tumpul, sama sisi, sama kaki. 100 soal dengan kunci jawaban.",
                key_big="Jumlah sudut segitiga = 180°", key_sub="Lancip, siku-siku, tumpul; sama sisi, sama kaki, sembarang.",
                body=body, faq=faq, sets=sets)


# ============================================================ 14. bangun ruang
def u14(d17):
    jaring, berhadapan, tampak, hitung = (maker(d17, x) for x in ("jaring", "berhadapan", "tampak", "hitung"))

    def volume():
        p, l, t = ri(2, 15), ri(2, 10), ri(2, 10)
        if len({p, l, t}) < 2:
            return None
        V = p * l * t
        if R().random() < 0.5:
            return mcq("Sebuah balok panjangnya %d cm, lebarnya %d cm, dan tingginya %d cm. Berapa volumenya?" % (p, l, t), "%s cm³" % num(V),
                       ["%d cm³" % (p + l + t), "%s cm³" % num(2 * (p * l + p * t + l * t)), "%s cm³" % num(p * l)],
                       "V = p × l × t = %d × %d × %d = %s cm³." % (p, l, t, num(V)))
        return mcq("Volume balok %s cm³. Panjangnya %d cm dan lebarnya %d cm. Berapa tingginya?" % (num(V), p, l), "%d cm" % t,
                   ["%d cm" % (V // p), "%d cm" % (V - p * l) if V - p * l < 1000 else "%d cm" % (t + 2), "%d cm" % (t + 1)],
                   "t = %s : (%d × %d) = %s : %d = %d cm." % (num(V), p, l, num(V), p * l, t))

    def kubus():
        s = ri(2, 12)
        if R().random() < 0.5:
            return mcq("Rusuk sebuah kubus %d cm. Berapa volumenya?" % s, "%s cm³" % num(s ** 3), ["%d cm³" % (s * s), "%d cm³" % (3 * s), "%s cm³" % num(6 * s * s)],
                       "V = s × s × s = %d × %d × %d = %s cm³." % (s, s, s, num(s ** 3)))
        return mcq("Volume sebuah kubus %s cm³. Berapa panjang rusuknya?" % num(s ** 3), "%d cm" % s, ["%d cm" % (s ** 3 // 3) if s ** 3 // 3 != s else "%d cm" % (s + 2), "%d cm" % (s * s), "%d cm" % (s + 1)],
                   "%d × %d × %d = %s, jadi rusuknya %d cm." % (s, s, s, num(s ** 3), s))

    def unsur():
        B = [("kubus", 6, 12, 8), ("balok", 6, 12, 8), ("prisma segitiga", 5, 9, 6), ("limas segi empat", 5, 8, 5), ("limas segitiga", 4, 6, 4), ("prisma segi enam", 8, 18, 12)]
        nm, sisi, rusuk, titik = ch(B)
        k = ch([("sisi", sisi), ("rusuk", rusuk), ("titik sudut", titik)])
        others = [x for x in {sisi, rusuk, titik, sisi + 1, rusuk - 1, titik + 2} if x != k[1]]
        return mcq("Berapa banyak %s pada %s?" % (k[0], nm), str(k[1]), [str(x) for x in pool(others)],
                   "%s punya %d sisi, %d rusuk, dan %d titik sudut." % (cap(nm), sisi, rusuk, titik))

    sets = [("Unsur bangun ruang", [(unsur, 14), (hitung, 6)]),
            ("Jaring-jaring kubus", [(jaring, 12), (berhadapan, 8)]),
            ("Tampak depan, samping, dan atas", [(tampak, 20)]),
            ("Volume balok", [(volume, 20)]),
            ("Volume kubus", [(kubus, 14), (hitung, 6)])]
    body = lesson(
        ["Bangun ruang punya sisi (bidang), rusuk (garis pertemuan dua sisi), dan titik sudut.",
         "Jaring-jaring adalah bangun ruang yang dibuka menjadi bangun datar. Kubus punya 11 jaring-jaring yang berbeda.",
         "Volume balok = panjang × lebar × tinggi. Volume kubus = rusuk × rusuk × rusuk. Satuannya cm³ atau m³."],
        [example("Balok 8 cm × 5 cm × 3 cm. Volumenya?", ["8 × 5 × 3"], "120 cm³"),
         example("Volume kubus 64 cm³. Rusuknya?", ["4 × 4 × 4 = 64"], "4 cm")],
        [["Volume dihitung p + l + t", "Volume = p × l × t"],
         ["Satuan volume ditulis cm²", "Volume memakai cm³"],
         ["Rusuk kubus dari volume 27 cm³ dianggap 9 cm", "3 × 3 × 3 = 27, jadi 3 cm"]])
    faq = [{"q": "Apa rumus volume balok?", "a": "Volume balok = panjang × lebar × tinggi."},
           {"q": "Berapa banyak rusuk kubus?", "a": "Kubus punya 12 rusuk yang sama panjang, 6 sisi berbentuk persegi, dan 8 titik sudut."},
           {"q": "Apa itu tampak depan?", "a": "Tampak depan adalah bentuk yang terlihat jika bangun dilihat lurus dari depan."}]
    return dict(slug="bangun-ruang-dan-volume", dom="G", sort=14,
                std_text="Peserta didik mengkonstruksi dan mengurai beberapa bangun ruang dan gabungannya, mengenali visualisasi spasial (tampak depan, atas, dan samping), serta menentukan volume.",
                title="Bangun Ruang, Jaring-jaring, dan Volume", short_title="Bangun Ruang dan Volume",
                meta_desc="Latihan bangun ruang untuk kelas 6 SD: sisi, rusuk, dan titik sudut, jaring-jaring kubus, tampak depan dan samping, volume balok dan kubus. 100 soal dengan kunci jawaban.",
                key_big="Volume balok = p × l × t", key_sub="Volume kubus = s × s × s.",
                body=body, faq=faq, sets=sets)


# ============================================================ 15. lokasi dan arah mata angin
ARAH = ["utara", "timur laut", "timur", "tenggara", "selatan", "barat daya", "barat", "barat laut"]
TEMPAT = ["Sekolah", "Pasar", "Masjid", "Taman", "Bank", "Stasiun", "Puskesmas", "Museum", "Kantor Pos", "Pura"]


def kompas(center, around):
    """around: {index arah: nama}"""
    cx, cy, r = 230, 165, 120
    s = ["<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (cx, cy, RED), text(cx, cy + 24, center, 13, weight=700)]
    for i, nm in around.items():
        ang = math.radians(90 - i * 45)
        x, y = cx + r * math.cos(ang), cy - r * 0.9 * math.sin(ang)
        s.append(line(cx, cy, x, y, col="#999", w=1.2, extra=" stroke-dasharray='4 4'"))
        s.append("<rect x='%.1f' y='%.1f' width='96' height='26' rx='5' fill='#fff' stroke='%s'/>" % (x - 48, y - 13, INK))
        s.append(text(x, y + 5, nm, 12, weight=700))
    s.append("<path d='M420 50 L428 70 L420 64 L412 70 Z' fill='%s'/>" % INK)
    s.append(text(420, 42, "U", 13, weight=700))
    return fig(svg_wrap(460, 330, "".join(s), "arah mata angin dari " + center))


def u15(d18):
    lokasi, gerak, jarak, dekat = (maker(d18, x) for x in ("lokasi", "gerak", "jarak", "dekat"))

    def arah():
        tp = pool(TEMPAT)
        c = tp[0]
        idx = pool(range(8))[:4]
        around = {i: tp[j + 1] for j, i in enumerate(idx)}
        i = ch(idx)
        if R().random() < 0.5:
            return mcq("Perhatikan denah. %s berada di sebelah … %s.%s" % (around[i], c, kompas(c, around)), ARAH[i], [ARAH[(i + 4) % 8], ARAH[(i + 2) % 8], ARAH[(i + 1) % 8], ARAH[(i + 7) % 8]],
                    "Utara ada di atas. %s ada di arah %s dari %s." % (around[i], ARAH[i], c))
        return mcq("Perhatikan denah. Bangunan yang berada di sebelah %s %s adalah …%s" % (ARAH[i], c, kompas(c, around)), around[i],
                   [around[j] for j in idx if j != i], "Arah %s dari %s adalah %s." % (ARAH[i], c, around[i]))

    def balik():
        i = ri(0, 7)
        a, b = pool(TEMPAT)[:2]
        return mcq("%s berada di sebelah %s %s. Maka %s berada di sebelah … %s." % (a, ARAH[i], b, b, a), ARAH[(i + 4) % 8],
                   [ARAH[i], ARAH[(i + 2) % 8], ARAH[(i + 6) % 8]], "Arah kebalikan dari %s adalah %s." % (ARAH[i], ARAH[(i + 4) % 8]))

    def putar():
        i = ri(0, 7)
        k = ch([1, 2, 4, 6])
        cw = R().random() < 0.5
        j = (i + k if cw else i - k) % 8
        deg = k * 45
        return mcq("Beni menghadap ke %s. Ia berputar %d° searah jarum jam. Sekarang Beni menghadap ke …" % (ARAH[i], deg) if cw else
                   "Beni menghadap ke %s. Ia berputar %d° berlawanan arah jarum jam. Sekarang Beni menghadap ke …" % (ARAH[i], deg), ARAH[j],
                   [ARAH[(i - k if cw else i + k) % 8], ARAH[i], ARAH[(j + 1) % 8], ARAH[(j + 7) % 8]],
                   "Satu langkah arah mata angin = 45°. %d° = %d langkah %s: %s." % (deg, k, "searah jarum jam" if cw else "berlawanan arah jarum jam", ARAH[j]))

    sets = [("Arah mata angin", [(arah, 20)]),
            ("Arah kebalikan dan berputar", [(balik, 10), (putar, 10)]),
            ("Letak pada peta berpetak", [(lokasi, 20)]),
            ("Bergerak pada peta", [(gerak, 14), (putar, 6)]),
            ("Jarak dan tempat terdekat", [(jarak, 10), (dekat, 10)])]
    body = lesson(
        ["Ada delapan arah mata angin: utara, timur laut, timur, tenggara, selatan, barat daya, barat, dan barat laut. Pada peta, utara biasanya di atas.",
         "Arah kebalikan adalah arah yang berseberangan: utara ↔ selatan, timur laut ↔ barat daya, timur ↔ barat, tenggara ↔ barat laut.",
         "Pada peta berpetak, letak ditulis dengan huruf kolom dan angka baris, misalnya C4."],
        [example("Pasar di sebelah timur laut sekolah. Sekolah di sebelah … pasar?", ["Kebalikan timur laut"], "barat daya"),
         example("Menghadap utara, berputar 90° searah jarum jam.", ["90° = 2 langkah: timur laut, timur"], "timur")],
        [["Timur dan barat tertukar", "Jika utara di atas, timur di kanan dan barat di kiri"],
         ["Kebalikan timur laut ditulis barat laut", "Kebalikan timur laut adalah barat daya"],
         ["Setiap langkah arah dihitung 90°", "Delapan arah: setiap langkah 45°"]])
    faq = [{"q": "Apa saja delapan arah mata angin?", "a": "Utara, timur laut, timur, tenggara, selatan, barat daya, barat, dan barat laut."},
           {"q": "Bagaimana tahu arah utara pada peta?", "a": "Lihat tanda panah atau mata angin pada peta. Jika tidak ada, biasanya utara di bagian atas."},
           {"q": "Berapa derajat dari utara ke timur?", "a": "Seperempat putaran, yaitu 90°. Dari utara ke timur laut 45°."}]
    return dict(slug="lokasi-dan-arah-mata-angin", dom="G", sort=15,
                std_text="Peserta didik menentukan lokasi pada peta yang menggunakan sistem berpetak dan arah mata angin.",
                title="Lokasi dan Arah Mata Angin", short_title="Lokasi dan Arah Mata Angin",
                meta_desc="Latihan lokasi dan arah untuk kelas 6 SD: delapan arah mata angin, arah kebalikan, berputar, letak dan gerak pada peta berpetak, jarak dan tempat terdekat. 100 soal dengan kunci jawaban.",
                key_big="Utara di atas, timur di kanan", key_sub="Delapan arah, setiap langkah 45°.",
                body=body, faq=faq, sets=sets)


# ============================================================ 16. waktu dan jadwal
def u16(d16):
    ubah, lama, akhir, awal, jadwal = (maker(d16, x) for x in ("ubah", "lama", "akhir", "awal", "jadwal"))
    BULAN = [("Januari", 31), ("Februari", 28), ("Maret", 31), ("April", 30), ("Mei", 31), ("Juni", 30), ("Juli", 31), ("Agustus", 31),
             ("September", 30), ("Oktober", 31), ("November", 30), ("Desember", 31)]

    def panjang():
        k = ri(0, 5)
        n = ri(2, 9)
        if k == 0:
            return mcq("%d minggu = … hari" % n, str(7 * n), [str(n * 10), str(n * 5), str(7 * n + 7)], "1 minggu = 7 hari, jadi %d × 7 = %d hari." % (n, 7 * n))
        if k == 1:
            return mcq("%d tahun = … bulan" % n, str(12 * n), [str(10 * n), str(52 * n), str(12 * n + 12)], "1 tahun = 12 bulan, jadi %d × 12 = %d bulan." % (n, 12 * n))
        if k == 2:
            d = 7 * n + ri(1, 6)
            return mcq("%d hari = … minggu … hari" % d, "%d minggu %d hari" % (d // 7, d % 7), ["%d minggu %d hari" % (d // 10, d % 10), "%d minggu %d hari" % (d // 7 - 1, d % 7 + 7), "%d minggu %d hari" % (d % 7, d // 7)],
                       "%d : 7 = %d sisa %d." % (d, d // 7, d % 7))
        if k == 3:
            return mcq("%d windu = … tahun" % n, str(8 * n), [str(10 * n), str(12 * n), str(5 * n)], "1 windu = 8 tahun, jadi %d windu = %d tahun." % (n, 8 * n))
        if k == 4:
            return mcq("%d dasawarsa = … tahun" % n, str(10 * n), [str(8 * n), str(100 * n), str(12 * n)], "1 dasawarsa = 10 tahun, jadi %d dasawarsa = %d tahun." % (n, 10 * n))
        m = ri(13, 47)
        return mcq("%d bulan = … tahun … bulan" % m, "%d tahun %d bulan" % (m // 12, m % 12), ["%d tahun %d bulan" % (m // 10, m % 10), "%d tahun %d bulan" % (m % 12, m // 12), "%d tahun %d bulan" % (m // 12 + 1, m % 12)],
                   "%d : 12 = %d sisa %d." % (m, m // 12, m % 12)) if m % 12 else None

    def tanggal():
        bi = ri(0, 11)
        nm, days = BULAN[bi]
        d = ri(1, days)
        n = ri(5, 25)
        t = d + n
        if t > days:
            t -= days
            nm2 = BULAN[(bi + 1) % 12][0]
        else:
            nm2 = nm
        x = K().next()
        return mcq("%s berangkat berlibur tanggal %d %s dan pulang %d hari kemudian. Tanggal berapa ia pulang?" % (x, d, nm, n), "%d %s" % (t, nm2),
                   ["%d %s" % (t + 1 if t < 28 else t - 1, nm2), "%d %s" % ((d + n - 30) if d + n > 30 else d + n + 1, nm2 if d + n > 30 else nm), "%d %s" % (t - 1 if t > 1 else t + 2, nm2)],
                   "%d %s + %d hari = %d %s (%s ada %d hari)." % (d, nm, n, t, nm2, nm, days))

    sets = [("Satuan waktu", [(ubah, 10), (panjang, 10)]),
            ("Lama kegiatan", [(lama, 20)]),
            ("Waktu mulai dan selesai", [(akhir, 10), (awal, 10)]),
            ("Jadwal perjalanan", [(jadwal, 20)]),
            ("Kalender", [(tanggal, 14), (panjang, 6)])]
    body = lesson(
        ["Satuan waktu: 1 jam = 60 menit, 1 hari = 24 jam, 1 minggu = 7 hari, 1 tahun = 12 bulan, 1 windu = 8 tahun, 1 dasawarsa = 10 tahun, 1 abad = 100 tahun.",
         "Lama kegiatan = waktu selesai − waktu mulai. Hitung jam dan menit secara terpisah, atau lompat ke jam bulat dulu.",
         "Pada kalender, perhatikan banyak hari dalam bulan itu (28, 30, atau 31 hari)."],
        [example("Bus berangkat 07.45 dan tiba 10.20. Lama perjalanan?", ["07.45 → 08.00 = 15 menit", "08.00 → 10.20 = 2 jam 20 menit"], "2 jam 35 menit"),
         example("Tanggal 25 Juni ditambah 10 hari?", ["Juni ada 30 hari: 25 + 10 = 35", "35 − 30 = 5"], "5 Juli")],
        [["1 jam dianggap 100 menit", "1 jam = 60 menit"],
         ["Semua bulan dianggap 30 hari", "Januari 31 hari, Februari 28 (atau 29) hari, April 30 hari"],
         ["Lama dari 07.45 ke 10.20 dihitung 10.20 − 07.45 = 2.75", "Hitung menit: 2 jam 35 menit"]])
    faq = [{"q": "Berapa hari dalam satu tahun?", "a": "Tahun biasa 365 hari, tahun kabisat 366 hari karena Februari punya 29 hari."},
           {"q": "Bagaimana menghitung lama perjalanan?", "a": "Hitung dari waktu berangkat ke jam bulat berikutnya, lalu sampai waktu tiba. Jumlahkan jam dan menitnya."},
           {"q": "Berapa tahun satu windu?", "a": "Satu windu = 8 tahun. Satu dasawarsa = 10 tahun, dan satu abad = 100 tahun."}]
    return dict(slug="waktu-jadwal-dan-kalender", dom="P", sort=16,
                std_text="Peserta didik menghitung durasi waktu dan menyelesaikan masalah yang berkaitan dengan jadwal dan kalender.",
                title="Waktu, Jadwal, dan Kalender", short_title="Waktu, Jadwal, dan Kalender",
                meta_desc="Latihan waktu untuk kelas 6 SD: satuan waktu (minggu, bulan, tahun, windu), lama kegiatan, waktu mulai dan selesai, jadwal perjalanan, dan kalender. 100 soal dengan kunci jawaban.",
                key_big="Lama = selesai − mulai", key_sub="1 jam = 60 menit, 1 minggu = 7 hari.",
                body=body, faq=faq, sets=sets)


# ============================================================ 17. modus dan penyajian data
def u17(d19):
    tabel, batang, pikto, frek = (maker(d19, x) for x in ("tabel", "batang", "pikto", "frek"))
    TOPIK = [("nilai ulangan matematika", ""), ("banyak buku yang dibaca dalam sebulan", " buku"), ("ukuran sepatu", ""), ("banyak saudara", " orang"),
             ("tinggi tanaman kacang (cm)", " cm"), ("lama tidur (jam)", " jam")]

    def modus():
        t, un = ch(TOPIK)
        base = ri(3, 9) if "nilai" not in t and "sepatu" not in t and "tinggi" not in t else ri(60, 90) if "nilai" in t else ri(30, 38) if "sepatu" in t else ri(10, 20)
        vals = [base + ri(0, 5) for _ in range(ri(9, 13))]
        m = ch(vals)
        vals += [m, m]
        cnt = {v: vals.count(v) for v in vals}
        top = max(cnt.values())
        mods = [v for v in cnt if cnt[v] == top]
        if len(mods) != 1:
            return None
        md = mods[0]
        R().shuffle(vals)
        others = sorted(set(vals) - {md}, key=lambda v: -cnt[v])
        return mcq("Data %s: %s. Modus data itu adalah …" % (t, "; ".join(map(str, vals))), str(md), [str(x) for x in others[:2]] + [str(max(vals)), str(len(vals))],
                   "%d muncul paling sering (%d kali), jadi modusnya %d." % (md, top, md))

    def modus_tabel():
        t, un = ch(TOPIK[:4])
        xs = sorted(set(ri(1, 10) + (60 if "nilai" in t else 30 if "sepatu" in t else 0) for _ in range(6)))[:5]
        if len(xs) < 4:
            return None
        fs = [ri(1, 12) for _ in xs]
        mx = max(fs)
        if fs.count(mx) > 1:
            return None
        md = xs[fs.index(mx)]
        rows = "".join("<tr><td>%d</td><td>%d</td></tr>" % (a, b) for a, b in zip(xs, fs))
        tb = "<table class='sn-table' style='width:auto'><thead><tr><th>%s</th><th>Frekuensi</th></tr></thead><tbody>%s</tbody></table>" % (cap(t), rows)
        return mcq("Tabel frekuensi %s:%sModus data itu adalah …" % (t, tb), str(md), [str(mx), str(xs[-1]) if xs[-1] != md else str(xs[0]), str(sum(fs))] + [str(x) for x in xs if x != md],
                   "Frekuensi terbesar %d, yaitu pada %d. Modusnya %d." % (mx, md, md))

    def jangkauan():
        t, un = ch(TOPIK)
        vals = [ri(20, 99) for _ in range(ri(6, 9))]
        if len(set(vals)) < len(vals):
            return None
        k = ri(0, 2)
        if k == 0:
            v = max(vals) - min(vals)
            return mcq("Data hasil lompat jauh (cm): %s. Berapa selisih data terbesar dan terkecil?" % "; ".join(map(str, vals)), str(v),
                       [str(max(vals)), str(min(vals)), str(max(vals) + min(vals)), str(v + 10)], "%d − %d = %d." % (max(vals), min(vals), v))
        if k == 1:
            v = sorted(vals)
            return mcq("Data berat badan siswa (kg): %s. Data jika diurutkan dari terkecil adalah …" % "; ".join(map(str, vals)), "; ".join(map(str, v)),
                       ["; ".join(map(str, v[::-1])), "; ".join(map(str, vals)), "; ".join(map(str, v[:2][::-1] + v[2:]))], "Urutkan dari yang terkecil: %s." % "; ".join(map(str, v)))
        lim = ri(40, 80)
        v = sum(1 for x in vals if x >= lim)
        return mcq("Data nilai tes membaca: %s. Siswa lulus jika nilainya %d atau lebih. Berapa siswa yang lulus?" % ("; ".join(map(str, vals)), lim), str(v),
                   [str(len(vals) - v), str(v + 1), str(v - 1) if v > 0 else str(v + 2), str(len(vals))], "Nilai ≥ %d: %d siswa." % (lim, v))

    sets = [("Modus dari data", [(modus, 20)]),
            ("Modus dari tabel", [(modus_tabel, 14), (frek, 6)]),
            ("Mengurutkan dan menganalisis data", [(jangkauan, 20)]),
            ("Tabel dan diagram batang", [(tabel, 10), (batang, 10)]),
            ("Piktogram dan campuran", [(pikto, 10), (modus, 5), (batang, 5)])]
    body = lesson(
        ["Data dikumpulkan lalu diurutkan dan disajikan dalam tabel frekuensi, piktogram, atau diagram batang agar mudah dibaca.",
         "Modus adalah nilai yang paling sering muncul dalam data. Pada tabel frekuensi, modus adalah data dengan frekuensi terbesar.",
         "Untuk menganalisis data, bandingkan nilai terbesar dan terkecil, hitung selisihnya, atau hitung berapa data yang memenuhi syarat tertentu."],
        [example("Data: 7; 8; 6; 8; 9; 8; 7. Modusnya?", ["8 muncul 3 kali, paling sering"], "8"),
         example("Frekuensi ukuran sepatu 33: 4, 34: 9, 35: 6. Modusnya?", ["Frekuensi terbesar 9"], "34")],
        [["Modus dari tabel dijawab frekuensinya (9)", "Modus adalah datanya (ukuran 34)"],
         ["Modus dianggap nilai terbesar", "Modus = yang paling sering muncul"],
         ["Selisih terbesar dan terkecil dihitung dari data pertama dan terakhir", "Cari dulu nilai terbesar dan terkecil"]])
    faq = [{"q": "Apa itu modus?", "a": "Modus adalah nilai yang paling sering muncul dalam sekumpulan data."},
           {"q": "Bisakah data punya lebih dari satu modus?", "a": "Bisa. Jika dua nilai sama-sama paling sering muncul, data itu punya dua modus."},
           {"q": "Bagaimana mencari modus dari tabel frekuensi?", "a": "Cari frekuensi terbesar, lalu lihat data di baris yang sama. Itulah modusnya."}]
    return dict(slug="modus-dan-penyajian-data", dom="D", sort=17,
                std_text="Peserta didik mengurutkan, membandingkan, menyajikan, menganalisis, dan menginterpretasi data dalam bentuk tabel, piktogram, dan diagram batang, serta menentukan modus.",
                title="Modus dan Penyajian Data", short_title="Modus dan Penyajian Data",
                meta_desc="Latihan data untuk kelas 6 SD: modus dari data dan tabel frekuensi, mengurutkan dan menganalisis data, tabel, diagram batang, dan piktogram. 100 soal dengan kunci jawaban.",
                key_big="Modus = yang paling sering muncul", key_sub="Pada tabel frekuensi: cari frekuensi terbesar.",
                body=body, faq=faq, sets=sets)


# ============================================================ 18. peluang
def u18(d20):
    kel, banding, pasti, putar, dua = (maker(d20, x) for x in ("kel", "banding", "pasti", "putar", "dua_kantong"))

    def dadu():
        k = ri(0, 3)
        if k == 0:
            n = ri(1, 6)
            return mcq("Sebuah dadu dilempar sekali. Kejadian muncul mata dadu %d adalah …" % n, "mungkin", ["pasti", "mustahil", "selalu terjadi"],
                       "Mata dadu 1 sampai 6, jadi %d mungkin muncul, tetapi tidak pasti." % n)
        if k == 1:
            n = ri(7, 12)
            return mcq("Sebuah dadu dilempar sekali. Kejadian muncul mata dadu %d adalah …" % n, "mustahil", ["mungkin", "pasti", "sering terjadi"],
                       "Dadu hanya punya mata 1 sampai 6, jadi %d mustahil muncul." % n)
        if k == 2:
            n = ri(7, 10)
            return mcq("Sebuah dadu dilempar sekali. Kejadian muncul mata dadu kurang dari %d adalah …" % n, "pasti", ["mungkin", "mustahil", "jarang terjadi"],
                       "Semua mata dadu (1 sampai 6) kurang dari %d, jadi pasti terjadi." % n)
        a, b = ch([("genap", "lebih dari 4"), ("ganjil", "6"), ("kurang dari 5", "genap"), ("lebih dari 1", "kurang dari 3"), ("bukan 6", "1 atau 2")])
        cnt = {"genap": 3, "ganjil": 3, "lebih dari 4": 2, "6": 1, "kurang dari 5": 4, "lebih dari 1": 5, "kurang dari 3": 2, "bukan 6": 5, "1 atau 2": 2}
        g = "mata dadu " + a if cnt[a] > cnt[b] else "mata dadu " + b
        if cnt[a] == cnt[b]:
            return None
        return mcq("Sebuah dadu dilempar. Mana yang lebih mungkin terjadi?", g, ["mata dadu " + b if g.endswith(a) else "mata dadu " + a, "Sama mungkinnya", "Tidak bisa ditentukan"],
                   "Mata dadu %s ada %d kemungkinan, mata dadu %s ada %d kemungkinan." % (a, cnt[a], b, cnt[b]))

    sets = [("Pasti, mungkin, mustahil", [(pasti, 12), (dadu, 8)]),
            ("Paling mungkin", [(kel, 20)]),
            ("Lebih mungkin atau kurang mungkin", [(banding, 14), (dadu, 6)]),
            ("Roda putar", [(putar, 20)]),
            ("Membandingkan dua kantong", [(dua, 20)])]
    body = lesson(
        ["Peluang menyatakan seberapa mungkin suatu kejadian terjadi: mustahil, kurang mungkin, sama mungkinnya, lebih mungkin, atau pasti.",
         "Kejadian yang punya lebih banyak kemungkinan hasil lebih mungkin terjadi. Pada kantong, warna yang paling banyak paling mungkin terambil.",
         "Pada dadu biasa ada 6 hasil: 1, 2, 3, 4, 5, 6. Mata dadu 7 mustahil, mata dadu kurang dari 7 pasti."],
        [example("Kantong berisi 5 merah dan 2 biru. Mana yang lebih mungkin terambil?", ["merah lebih banyak"], "merah"),
         example("Dadu dilempar. Muncul mata genap atau mata 6?", ["genap: 2, 4, 6 (3 kemungkinan)", "6: 1 kemungkinan"], "mata genap lebih mungkin")],
        [["Kejadian yang mungkin dianggap pasti", "Pasti berarti selalu terjadi; mungkin berarti bisa terjadi atau tidak"],
         ["Membandingkan banyak benda, bukan perbandingannya, pada dua kantong yang isinya berbeda", "Bandingkan bagian dari seluruh isi kantong"],
         ["Bagian roda yang besar dianggap sama dengan yang kecil", "Bagian yang lebih luas lebih mungkin ditunjuk"]])
    faq = [{"q": "Apa arti kejadian mustahil?", "a": "Kejadian yang tidak mungkin terjadi, misalnya muncul mata dadu 8 pada dadu biasa."},
           {"q": "Bagaimana menentukan kejadian yang lebih mungkin?", "a": "Hitung banyak hasil yang membuat kejadian itu terjadi. Yang hasilnya lebih banyak, lebih mungkin terjadi."},
           {"q": "Apakah peluang sama dengan menebak?", "a": "Tidak. Peluang tidak bisa memastikan hasil, tetapi membantu kita memperkirakan hasil mana yang lebih sering muncul."}]
    return dict(slug="peluang", dom="D", sort=18,
                std_text="Peserta didik menjelaskan kemungkinan suatu kejadian dengan kata-kata (pasti, mungkin, mustahil) dan membandingkan kemungkinan dua kejadian.",
                title="Peluang Suatu Kejadian", short_title="Peluang",
                meta_desc="Latihan peluang untuk kelas 6 SD: pasti, mungkin, mustahil, kejadian yang paling mungkin, dadu, roda putar, dan membandingkan dua kantong. 100 soal dengan kunci jawaban.",
                key_big="Lebih banyak hasil = lebih mungkin", key_sub="Pasti, mungkin, atau mustahil?",
                body=body, faq=faq, sets=sets)


# ------------------------------------------------------------
NEED5 = {2: (1, 2), 3: (5,), 4: (9,), 5: (7, 8), 8: (7, 8), 9: (13,), 10: (12,), 11: (11,), 12: (14,), 13: (15,), 14: (17,), 15: (18,), 16: (16,), 17: (19,), 18: (20,)}
UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18]


def build(i):
    import id_k5
    rnd = random.Random(40600 + i)
    A.setup(rnd)
    ds = [id_k5.UNITS[k - 1]() for k in NEED5.get(i, ())]
    d = UNITS[i - 1](*ds)
    seen = set()
    sets = [(t, mix(rnd, seen, parts)) for t, parts in d["sets"]]
    make_unit(rnd, d["slug"], d["dom"], d["std_text"], d["title"], d["short_title"], d["meta_desc"],
              d["key_big"], d["key_sub"], d["body"], d["faq"], sets, d["sort"], grade=G, fase="Fase C")
    return d["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    for i in range(1, len(UNITS) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(i), flush=True)
