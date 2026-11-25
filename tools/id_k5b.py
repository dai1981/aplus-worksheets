# -*- coding: utf-8 -*-
"""Indonesia Kelas 5 (Fase C): Aljabar, Pengukuran, Geometri, Data（11〜20）。"""
import math
from fractions import Fraction as F
import id_k4a as A
from id_k4a import ri, ch, pool, stmt, rel, cap
from id_k5a import f, fx, fw, d1
from id_common import (num, rp, u, NB, mcq, lesson, example, table, wrap, fr, diagram_batang, text, line, svg_wrap, fig,
                       INK, GREEN, FILL, RED, BLUE)

BOX = "<span style='display:inline-block;width:1.4em;border:2px solid #333;border-radius:3px'>&nbsp;</span>"


def K():
    return A.K


def R():
    return A.R


def lg(svg):
    return svg.replace("<svg ", "<svg data-pf='lg' ", 1)


# ============================================================ 11. kalimat matematika
def u11():
    def kali():
        a, b = ri(3, 25), ri(4, 40)
        p = a * b
        if p > 1000:
            return None
        if R().random() < 0.5:
            q = "%s × %d = %s" % (BOX, a, num(p))
        else:
            q = "%d × %s = %s" % (a, BOX, num(p))
        return mcq("Bilangan yang tepat untuk kotak adalah …<br>" + q, str(b), [str(p - a), str(b + 1), num(p * a) if p * a < 100000 else str(b * 2)],
                   "%s : %d = %d. Periksa: %d × %d = %s." % (num(p), a, b, a, b, num(p)))

    def bagi():
        b, c = ri(3, 25), ri(4, 40)
        a = b * c
        if a > 1000:
            return None
        k = ri(0, 1)
        if k == 0:
            return mcq("Bilangan yang tepat untuk kotak adalah …<br>%s : %s = %d" % (num(a), BOX, c), str(b), [num(a * c) if a * c < 100000 else str(b + 2), str(a - c), str(b + 1)],
                       "%s : %d = %d. Periksa: %s : %d = %d." % (num(a), c, b, num(a), b, c))
        return mcq("Bilangan yang tepat untuk kotak adalah …<br>%s : %d = %d" % (BOX, b, c), num(a), [str(c - b) if c > b else str(c + b), str(b + c), num(a + b)],
                   "%d × %d = %s. Periksa: %s : %d = %d." % (c, b, num(a), num(a), b, c))

    def campur():
        a, b = ri(100, 600), ri(10, 300)
        c = ri(10, a + b - 10)
        d = a + b - c
        return mcq("Bilangan yang tepat untuk kotak adalah …<br>%s + %s = %s + %s" % (num(a), num(b), BOX, num(c)), num(d), [num(a + b), num(a + b + c), num(d + 10)],
                   "%s + %s = %s, lalu %s − %s = %s." % (num(a), num(b), num(a + b), num(a + b), num(c), num(d)))

    def sifat():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(12, 99), ri(12, 99)
            return mcq("Bilangan yang tepat untuk kotak adalah …<br>%d × %d = %d × %s" % (a, b, b, BOX), str(a), [str(b), num(a * b), str(a + b)],
                       "Sifat pertukaran (komutatif): urutan perkalian boleh ditukar.")
        if k == 1:
            a, b, c = ri(2, 25), ri(2, 9), ri(2, 9)
            return mcq("Bilangan yang tepat untuk kotak adalah …<br>(%d × %d) × %d = %d × (%s × %d)" % (a, b, c, a, BOX, c), str(b), [str(c), str(a), str(b * c)],
                       "Sifat pengelompokan (asosiatif): (%d × %d) × %d = %d × (%d × %d)." % (a, b, c, a, b, c))
        a = ri(3, 9)
        t, o = ri(2, 9) * 10, ri(1, 9)
        return mcq("Bilangan yang tepat untuk kotak adalah …<br>%d × %d = %d × %d + %d × %s" % (a, t + o, a, t, a, BOX), str(o), [str(t), str(t + o), str(a * o)],
                   "Sifat distributif: %d × (%d + %d) = %d × %d + %d × %d." % (a, t, o, a, t, a, o))

    SC = [("Setiap kotak berisi %s kue. Ada beberapa kotak, dan jumlah kuenya %s.", "×", "kotak"),
          ("Sebanyak %s buku disusun sama banyak di beberapa rak. Setiap rak berisi %s buku.", ":", "rak"),
          ("Harga satu pensil Rp%s. %s membeli beberapa pensil dan membayar Rp%s.", "×$", "pensil"),
          ("Sebanyak %s siswa dibagi dalam beberapa kelompok. Setiap kelompok %s siswa.", ":", "kelompok")]

    def model():
        t, op, un = ch(SC)
        a, n = ri(4, 25), ri(3, 30)
        p = a * n
        if p > 1000:
            return None
        if op == "×":
            q = t % (a, num(p))
            g = "%d × %s = %s" % (a, BOX, num(p))
            bad = ["%d + %s = %s" % (a, BOX, num(p)), "%s : %d = %s" % (num(p), a, BOX) if False else "%s − %d = %s" % (num(p), a, BOX), "%d × %s = %s" % (a, num(p), BOX)]
        elif op == "×$":
            a = a * 500
            p = a * n
            q = t % (num(a), K().next(), num(p))
            g = "%s × %s = %s" % (num(a), BOX, num(p))
            bad = ["%s + %s = %s" % (num(a), BOX, num(p)), "%s × %s = %s" % (num(a), num(p), BOX), "%s : %s = %s" % (num(a), num(p), BOX)]
        else:
            q = t % (num(p), a)
            g = "%s : %s = %d" % (num(p), BOX, a)
            bad = ["%s × %s = %d" % (num(p), BOX, a), "%s − %s = %d" % (num(p), BOX, a), "%s : %d = %d" % (BOX, a, p)]
        return mcq(q + " Kalimat matematika untuk mencari banyak %s adalah …" % un, g, bad, "Kotak adalah banyak %s." % un)

    def selesai():
        a, n = ri(6, 25), ri(4, 30)
        p = a * n
        if p > 1000:
            return None
        who = K().next()
        k = ri(0, 2)
        if k == 0:
            return mcq("%s membagikan %s permen kepada beberapa teman. Setiap teman mendapat %d permen. Berapa banyak teman %s?" % (who, num(p), a, who),
                       "%d orang" % n, ["%d orang" % x for x in (n + 1, p - a, a)], "%s : %d = %d." % (num(p), a, n))
        if k == 1:
            return mcq("Sebuah bilangan dikalikan %d, hasilnya %s. Berapa bilangan itu?" % (a, num(p)), str(n), [str(p - a), str(n + 1), num(p * a) if p * a < 100000 else str(n * 2)],
                       "%s × %d = %s, jadi %s = %s : %d = %d." % (BOX, a, num(p), BOX, num(p), a, n))
        return mcq("Sebuah bilangan dibagi %d, hasilnya %d. Berapa bilangan itu?" % (a, n), num(p), [str(n - a) if n > a else str(a + n), str(a + n), num(p + a)],
                   "%s : %d = %d, jadi %s = %d × %d = %s." % (BOX, a, n, BOX, n, a, num(p)))

    sets = [("Kotak pada perkalian", [(kali, 20)]),
            ("Kotak pada pembagian", [(bagi, 20)]),
            ("Kedua ruas sama", [(campur, 12), (sifat, 8)]),
            ("Sifat-sifat operasi", [(sifat, 12), (kali, 4), (bagi, 4)]),
            ("Soal cerita", [(model, 10), (selesai, 10)])]
    body = lesson(
        ["Kalimat matematika memakai tanda = yang berarti kedua ruas sama nilainya.",
         "Cari bilangan di kotak dengan operasi kebalikannya: perkalian ↔ pembagian, penjumlahan ↔ pengurangan.",
         "Sifat operasi membantu: pertukaran (a × b = b × a), pengelompokan ((a × b) × c = a × (b × c)), dan distributif (a × (b + c) = a × b + a × c)."],
        [example("%s × 15 = 360" % BOX, ["360 : 15 = 24", "Periksa: 24 × 15 = 360"], "24"),
         example("%s : 8 = 45" % BOX, ["45 × 8 = 360"], "360")],
        [["%s : 8 = 45, kotak diisi 45 : 8" % BOX, "Bilangan yang dibagi = hasil × pembagi = 360"],
         ["%s × 15 = 360, kotak diisi 360 − 15" % BOX, "Gunakan pembagian: 360 : 15 = 24"],
         ["Tidak memeriksa jawaban", "Masukkan jawaban ke kotak dan hitung ulang"]])
    faq = [{"q": "Bagaimana mencari bilangan yang belum diketahui pada perkalian?", "a": "Bagi hasil kali dengan bilangan yang diketahui. Contoh: □ × 12 = 156, maka □ = 156 : 12 = 13."},
           {"q": "Bagaimana jika kotak ada di depan tanda bagi?", "a": "Kalikan hasil bagi dengan pembagi. Contoh: □ : 7 = 45, maka □ = 45 × 7 = 315."},
           {"q": "Apa itu sifat distributif?", "a": "Perkalian dapat dibagi ke penjumlahan: 6 × 47 = 6 × 40 + 6 × 7 = 240 + 42 = 282."}]
    return dict(slug="kalimat-matematika", dom="A", sort=11,
                std_text="Murid menemukan nilai yang belum diketahui dalam kalimat matematika yang melibatkan penjumlahan, pengurangan, perkalian, dan pembagian pada bilangan cacah sampai 1000 dengan menggunakan sifat-sifat bilangan dan operasinya.",
                title="Kalimat Matematika dan Sifat Operasi", short_title="Kalimat Matematika",
                meta_desc="Latihan mencari bilangan yang belum diketahui pada perkalian dan pembagian sampai 1.000, sifat komutatif, asosiatif, dan distributif, serta soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="□ × 15 = 360 → □ = 24", key_sub="Gunakan operasi kebalikannya, lalu periksa.", body=body, faq=faq, sets=sets)


# ============================================================ 12. pola bilangan
def u12():
    def seq_up():
        a = ri(1, 12)
        k = ch([2, 3, 4, 5, 10])
        s = [a * k ** i for i in range(6)]
        if s[5] > 100000:
            return None
        return s, k, True

    def seq_down():
        k = ch([2, 3, 4, 5, 10])
        last = ri(1, 9)
        s = [last * k ** (5 - i) for i in range(6)]
        if s[0] > 100000:
            return None
        return s, k, False

    def lanjut(up):
        def mk():
            r = seq_up() if up else seq_down()
            if not r:
                return None
            s, k, _ = r
            n = s[5]
            prev = s[4]
            return mcq("Bilangan berikutnya pada pola %s, … adalah …" % ", ".join(num(x) for x in s[:5]), num(n),
                       [num(prev + (s[4] - s[3])) if up else num(prev - (s[3] - s[4])) if prev - (s[3] - s[4]) > 0 else num(n + 1), num(n * k) if up else num(n + k), num(n + 1) if not up else num(n - k)],
                       "Setiap langkah %s %d: %s %s %d = %s." % ("dikali" if up else "dibagi", k, num(prev), "×" if up else ":", k, num(n)))
        return mk

    def tengah():
        r = seq_up() if R().random() < 0.5 else seq_down()
        if not r:
            return None
        s, k, up = r
        s = s[:5]
        i = ri(1, 3)
        show = [num(x) if j != i else BOX for j, x in enumerate(s)]
        return mcq("Bilangan yang tepat untuk kotak pada pola ini adalah …<br>%s" % ", ".join(show), num(s[i]),
                   [num(s[i] + 1), num((s[i - 1] + s[i + 1]) // 2) if (s[i - 1] + s[i + 1]) // 2 != s[i] else num(s[i] + k), num(s[i] * k)],
                   "Aturannya %s %d." % ("dikali" if up else "dibagi", k))

    def aturan():
        r = seq_up() if R().random() < 0.5 else seq_down()
        if not r:
            return None
        s, k, up = r
        s = s[:4]
        g = ("dikali %d" if up else "dibagi %d") % k
        d = abs(s[1] - s[0])
        bad = [("ditambah %s" if up else "dikurangi %s") % num(d), ("dibagi %d" if up else "dikali %d") % k, ("dikali %d" if up else "dibagi %d") % (k + 1)]
        return mcq("Aturan pola %s adalah …" % ", ".join(num(x) for x in s), g, bad,
                   "%s %s %d = %s, %s %s %d = %s. Selisihnya tidak tetap, tetapi hasil baginya tetap." % (num(s[0]), "×" if up else ":", k, num(s[1]), num(s[1]), "×" if up else ":", k, num(s[2])))

    def campur():
        a = ri(1, 6)
        k = ch([2, 3])
        c = ch([1, 2, -1])
        s = [a]
        for _ in range(4):
            s.append(s[-1] * k + c)
        if min(s) <= 0 or s[-1] > 2000:
            return None
        rule = "dikali %d lalu %s %d" % (k, "ditambah" if c > 0 else "dikurangi", abs(c))
        n = s[4]
        return mcq("Pola %s, … memakai aturan <i>%s</i>. Bilangan berikutnya adalah …" % (", ".join(num(x) for x in s[:4]), rule), num(n),
                   [num(s[3] * k), num(s[3] + (s[3] - s[2])), num(n + k)], "%s × %d %s %d = %s." % (num(s[3]), k, "+" if c > 0 else "−", abs(c), num(n)))

    def cerita():
        k = ri(0, 3)
        if k == 0:
            a = ch([5, 10, 20, 25, 50, 100])
            h = ri(3, 7)
            v = a * 2 ** h
            if v > 100000:
                return None
            return mcq("Banyak bakteri menjadi 2 kali lipat setiap jam. Mula-mula ada %d bakteri. Berapa banyak bakteri setelah %d jam?" % (a, h), num(v),
                       [num(a * 2 * h), num(v // 2), num(v * 2)], "%d × 2 × 2 × … (%d kali) = %s." % (a, h, num(v)))
        if k == 1:
            h = ri(3, 6)
            v = 2 ** h
            return mcq("Selembar kertas dilipat menjadi dua sama besar sebanyak %d kali, lalu dibuka. Menjadi berapa bagian kertas itu?" % h, "%d bagian" % v,
                       ["%d bagian" % x for x in (2 * h, v // 2, v + 2)], "Setiap lipatan membuat bagiannya 2 kali lipat: 2 × 2 × … = %d." % v)
        if k == 2:
            a = ch([64, 128, 256, 512, 1024]) * ch([1, 5, 10])
            h = ri(2, 5)
            v = a // 2 ** h
            if v * 2 ** h != a:
                return None
            return mcq("Air di sebuah bak tinggal setengahnya setiap hari. Hari ini ada %s liter. Berapa liter air setelah %d hari?" % (num(a), h), "%s liter" % num(v),
                       ["%s liter" % num(x) for x in (a - 2 * h, v * 2, v // 2 if v > 1 else v + 1)], "%s : 2 : 2 … (%d kali) = %s." % (num(a), h, num(v)))
        a = ri(2, 5)
        k = 3
        h = ri(3, 6)
        v = a * k ** h
        if v > 100000:
            return None
        return mcq("Sebuah pesan berantai: setiap orang mengirim ke 3 orang baru. Pada putaran pertama ada %d orang mengirim. Pada putaran berikutnya banyak pengirim 3 kali lipat. Berapa pengirim pada putaran ke-%d?" % (a, h + 1),
                   num(v), [num(a * 3 * h), num(v // 3), num(v * 3)], "%d × 3 sebanyak %d kali = %s." % (a, h, num(v)))

    sets = [("Pola dikali", [(lanjut(True), 20)]),
            ("Pola dibagi", [(lanjut(False), 20)]),
            ("Menemukan aturan pola", [(aturan, 14), (tengah, 6)]),
            ("Bilangan yang hilang", [(tengah, 12), (campur, 8)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Pada pola perkalian, setiap bilangan didapat dengan mengalikan bilangan sebelumnya dengan bilangan yang sama: 3, 6, 12, 24, … (dikali 2).",
         "Pada pola pembagian, setiap bilangan dibagi dengan bilangan yang sama: 2.000, 400, 80, 16, … (dibagi 5).",
         "Jika selisihnya tidak tetap, coba cari hasil baginya: 12 : 6 = 2, 24 : 12 = 2."],
        [example("Lanjutkan: 5, 15, 45, 135, …", ["15 : 5 = 3, 45 : 15 = 3", "135 × 3"], "405"),
         example("Lanjutkan: 640, 320, 160, 80, …", ["Setiap langkah dibagi 2"], "40")],
        [["5, 15, 45, … dianggap ditambah 10", "15 − 5 = 10, tetapi 45 − 15 = 30. Aturannya dikali 3"],
         ["Pola turun dianggap dikurangi", "Periksa hasil bagi: 640 : 320 = 2"],
         ["Melipat kertas 4 kali = 8 bagian", "2 × 2 × 2 × 2 = 16 bagian"]])
    faq = [{"q": "Bagaimana mengetahui pola perkalian?", "a": "Bagi setiap bilangan dengan bilangan sebelumnya. Jika hasilnya selalu sama, itulah pengalinya."},
           {"q": "Apa bedanya pola penjumlahan dan pola perkalian?", "a": "Pola penjumlahan bertambah dengan selisih tetap (4, 7, 10, 13). Pola perkalian bertambah makin cepat (2, 6, 18, 54)."},
           {"q": "Di mana pola perkalian terlihat dalam kehidupan?", "a": "Contohnya pertumbuhan bakteri, pesan berantai, dan kertas yang dilipat berkali-kali."}]
    return dict(slug="pola-bilangan", dom="A", sort=12,
                std_text="Murid dapat mengidentifikasi, meniru, dan mengembangkan pola bilangan membesar dan mengecil yang melibatkan perkalian dan pembagian.",
                title="Pola Bilangan dengan Perkalian dan Pembagian", short_title="Pola Bilangan",
                meta_desc="Latihan pola bilangan membesar dan mengecil dengan perkalian dan pembagian, menemukan aturan pola, bilangan yang hilang, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="3, 6, 12, 24 (dikali 2)", key_sub="Jika selisihnya berubah, coba cari hasil baginya.", body=body, faq=faq, sets=sets)


# ============================================================ 13. rasio dan proporsi
def u13():
    def sederhana():
        a, b = R().sample(range(1, 10), 2)
        k = ri(2, 9)
        x, y = a * k, b * k
        g = math.gcd(a, b)
        a, b = a // g, b // g
        if (a, b) == (1, 1):
            return None
        X, Y = ch([("kelereng merah", "kelereng biru"), ("siswa laki-laki", "siswa perempuan"), ("ayam", "bebek"), ("buku tulis", "buku gambar")])
        return mcq("Ada %d %s dan %d %s. Perbandingan %s dan %s dalam bentuk paling sederhana adalah …" % (x, X, y, Y, X, Y),
                   "%d : %d" % (a, b), ["%d : %d" % (b, a), "%d : %d" % (x, y) if (x, y) != (a, b) else "%d : %d" % (a + 1, b), "%d : %d" % (a, a + b)],
                   "%d : %d, bagi keduanya dengan %d: %d : %d." % (x, y, x // a, a, b))

    def bagian():
        a, b = R().sample(range(1, 8), 2)
        if math.gcd(a, b) != 1:
            return None
        k = ri(2, 12)
        X, Y = ch([("laki-laki", "perempuan"), ("merah", "putih"), ("mangga", "jeruk"), ("kambing", "sapi")])
        if R().random() < 0.5:
            return mcq("Perbandingan %s dan %s adalah %d : %d. Jika banyak %s %d, berapa banyak %s?" % (X, Y, a, b, X, a * k, Y), str(b * k),
                       [str(a * k + b), str(b * k + a), str(a * b * k) if a * b * k != b * k else str(b * k + 1)], "%d : %d = %d, jadi %s = %d × %d = %d." % (a * k, a, k, Y, b, k, b * k))
        t = (a + b) * k
        return mcq("Jumlah %s dan %s adalah %d. Perbandingannya %d : %d. Berapa banyak %s?" % (X, Y, t, a, b, X), str(a * k),
                   [str(b * k), str(t // a) if t % a == 0 and t // a != a * k else str(a * k + 1), str(t - a)], "Ada %d + %d = %d bagian. Satu bagian = %d : %d = %d. %s = %d × %d = %d." % (a, b, a + b, t, a + b, k, X, a, k, a * k))

    def satuan():
        k = ri(0, 2)
        if k == 0:
            n, p = ri(2, 8), ch([2500, 3000, 3500, 4000, 5000, 6000])
            m = ri(2, 12)
            if m == n:
                return None
            it = ch(["buku tulis", "pensil warna", "bolpoin", "spidol"])
            return mcq("Harga %d %s adalah %s. Berapa harga %d %s?" % (n, it, rp(n * p), m, it), rp(m * p), [rp(n * p + m * p), rp(m * p + p), rp(n * p * m)],
                       "Harga 1 %s = %s. Harga %d %s = %s." % (it, rp(p), m, it, rp(m * p)))
        if k == 1:
            l, km = ri(2, 6), ch([12, 14, 15, 16, 18, 20])
            m = ri(2, 10)
            return mcq("Sebuah motor menempuh %d km dengan %d liter bensin. Berapa km jarak yang ditempuh dengan %d liter bensin?" % (l * km, l, m), "%d km" % (m * km),
                       ["%d km" % x for x in (l * km + m, m * km + km, l * km * m)], "1 liter → %d : %d = %d km. %d liter → %d km." % (l * km, l, km, m, m * km))
        t, d = ri(2, 6), ch([45, 50, 60, 70, 80])
        m = ri(2, 8)
        return mcq("Sebuah bus menempuh %d km dalam %d jam dengan kecepatan tetap. Berapa km yang ditempuh dalam %d jam?" % (t * d, t, m), "%d km" % (m * d),
                   ["%d km" % x for x in (t * d + m, m * d + d, m * d - d)], "1 jam → %d km. %d jam → %d km." % (d, m, m * d))

    def resep():
        a = ri(2, 6)
        g = ch([100, 150, 200, 250, 300])
        m = ch([x for x in (2, 3, 4, 6, 8, 9, 10, 12) if x != a])
        if (g * m) % a:
            return None
        bahan = ch(["tepung", "gula", "mentega", "susu bubuk"])
        return mcq("Untuk membuat %d kue diperlukan %d gram %s. Berapa gram %s untuk %d kue?" % (a, g, bahan, bahan, m), "%s gram" % num(g * m // a),
                   ["%s gram" % num(x) for x in (g * m, g + m - a if g + m - a > 0 else g + m, g * m // a + g)], "%d gram untuk %d kue, jadi untuk %d kue = %d × %d : %d = %s gram." % (g, a, m, g, m, a, num(g * m // a)))

    def tabel():
        a = ri(2, 6)
        b = a * ri(2, 6)
        xs = [a, 2 * a, 3 * a, 5 * a]
        ys = [b, 2 * b, 3 * b, 5 * b]
        i = ri(1, 3)
        rows = "".join("<td>%s</td>" % (num(y) if j != i else "?") for j, y in enumerate(ys))
        t = ("<table class='sn-table' style='width:auto'><tbody><tr><th>Banyak kotak</th>%s</tr><tr><th>Banyak kue</th>%s</tr></tbody></table>"
             % ("".join("<td>%d</td>" % x for x in xs), rows))
        return mcq("Tabel menunjukkan banyak kue dalam kotak. Berapa nilai yang ditandai ?" + t, num(ys[i]), [num(ys[i] + b), num(ys[i] - 1), num(xs[i] + b)],
                   "Setiap kotak berisi %d : %d = %s kue. %d × %s = %s." % (b, a, fx(F(b, a)), xs[i], fx(F(b, a)), num(ys[i])))

    sets = [("Perbandingan sederhana", [(sederhana, 20)]),
            ("Mencari bagian dari perbandingan", [(bagian, 20)]),
            ("Rasio satuan", [(satuan, 20)]),
            ("Tabel perbandingan", [(tabel, 12), (bagian, 8)]),
            ("Soal cerita", [(resep, 10), (satuan, 10)])]
    body = lesson(
        ["Perbandingan (rasio) a : b membandingkan dua banyak benda. Sederhanakan dengan membagi keduanya dengan FPB.",
         "Rasio satuan adalah nilai untuk 1, misalnya harga 1 barang atau jarak dengan 1 liter bensin. Cari nilai untuk 1 dulu, lalu kalikan.",
         "Jika jumlah dan perbandingan diketahui, hitung banyak bagian: satu bagian = jumlah : banyak bagian."],
        [example("Harga 4 buku Rp18.000. Berapa harga 7 buku?", ["1 buku = Rp18.000 : 4 = Rp4.500", "7 × Rp4.500"], "Rp31.500"),
         example("Perbandingan laki-laki dan perempuan 2 : 3, jumlah 30 siswa. Berapa laki-laki?", ["2 + 3 = 5 bagian", "1 bagian = 30 : 5 = 6", "2 × 6"], "12 siswa")],
        [["Perbandingan 12 : 18 ditulis 6 : 9", "Bagi dengan FPB (6): 2 : 3"],
         ["Jumlah 30 dibagi 2 (angka pertama perbandingan)", "Bagi dengan jumlah bagian (2 + 3 = 5)"],
         ["Urutan perbandingan ditukar", "Ikuti urutan yang ditanyakan: merah : biru"]])
    faq = [{"q": "Apa itu perbandingan atau rasio?", "a": "Cara membandingkan dua banyak benda dengan pembagian, ditulis a : b. Contoh: 6 kelereng merah dan 9 biru, perbandingannya 6 : 9 = 2 : 3."},
           {"q": "Apa itu rasio satuan?", "a": "Nilai untuk satu satuan, misalnya harga per buah atau km per liter. Dengan rasio satuan kita bisa menghitung untuk banyak berapa pun."},
           {"q": "Bagaimana menyelesaikan soal proporsi?", "a": "Cari nilai untuk satu, lalu kalikan dengan banyak yang ditanyakan. Atau lihat berapa kali lipat banyaknya berubah."}]
    return dict(slug="rasio-dan-proporsi", dom="A", sort=13,
                std_text="Murid bernalar secara proporsional untuk menyelesaikan masalah sehari-hari dengan rasio satuan, dan menggunakan operasi perkalian dan pembagian dalam menyelesaikan masalah sehari-hari yang terkait dengan proporsi.",
                title="Rasio, Perbandingan, dan Proporsi", short_title="Rasio dan Proporsi",
                meta_desc="Latihan perbandingan sederhana, mencari bagian dari perbandingan, rasio satuan, tabel perbandingan, dan soal cerita proporsi. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Cari nilai untuk 1 dulu", key_sub="Lalu kalikan dengan banyak yang ditanyakan.", body=body, faq=faq, sets=sets)


# ============================================================ 14. keliling dan luas
def shape_svg(pts, labels, dashed=(), right=(), sc=1.0, label="bangun datar"):
    """pts: titik (satuan cm); labels: [(x, y, teks)]; right: titik sudut siku-siku (x, y, dx, dy)"""
    S = 22.0 * sc
    xs = [p[0] for p in pts] + [l[0] for l in labels]
    ys = [p[1] for p in pts] + [l[1] for l in labels]
    x0, y0 = min(xs) * S - 40, min(ys) * S - 26
    P = lambda x, y: (x * S - x0, y * S - y0)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2' stroke-linejoin='round'/>" % (" ".join("%.1f,%.1f" % P(*p) for p in pts), FILL, GREEN)]
    for a, b in dashed:
        s.append(line(*(P(*a) + P(*b)), col=INK, w=1.6, extra=" stroke-dasharray='5 4'"))
    for (x, y, dx, dy) in right:
        X, Y = P(x, y)
        s.append("<path d='M%.1f %.1f h%.1f v%.1f h%.1f' fill='none' stroke='%s' stroke-width='1.5'/>" % (X + dx * 10, Y, 0, dy * 10, -dx * 10, INK))
    for (x, y, t) in labels:
        X, Y = P(x, y)
        s.append(text(X, Y + 5, t, 14, weight=700))
    W = max(xs) * S - x0 + 44
    H = max(ys) * S - y0 + 24
    return fig(lg(svg_wrap(int(W), int(H), "".join(s), label)))


TRIS = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 6, 10), (12, 5, 13), (4, 3, 5), (12, 9, 15)]


def u14():
    def persegi_panjang():
        p, l = ri(3, 15), ri(2, 9)
        if p == l:
            return None
        k = R().random() < 0.5
        sc = 1.0 if p <= 10 else 0.7
        pic = shape_svg([(0, 0), (p, 0), (p, l), (0, l)], [(p / 2.0, -0.6, "%d cm" % p), (p + 1.1, l / 2.0, "%d cm" % l)], sc=sc, label="persegi panjang")
        if k:
            return mcq("Berapa keliling persegi panjang ini?" + pic, "%d cm" % (2 * (p + l)), ["%d cm" % x for x in (p + l, p * l, 2 * p + l)],
                       "Keliling = 2 × (%d + %d) = %d cm." % (p, l, 2 * (p + l)))
        return mcq("Berapa luas persegi panjang ini?" + pic, "%d cm²" % (p * l), ["%d cm²" % x for x in (2 * (p + l), p + l, p * l + p)],
                   "Luas = panjang × lebar = %d × %d = %d cm²." % (p, l, p * l))

    def persegi():
        s = ri(3, 15)
        k = ri(0, 2)
        pic = shape_svg([(0, 0), (s, 0), (s, s), (0, s)], [(s / 2.0, -0.6, "%d cm" % s)], sc=1.0 if s <= 10 else 0.7, label="persegi")
        if k == 0:
            return mcq("Berapa keliling persegi ini?" + pic, "%d cm" % (4 * s), ["%d cm" % x for x in (s * s, 2 * s, 4 * s + 4)] if s != 4 else ["16 cm²", "8 cm", "20 cm"],
                       "Keliling persegi = 4 × sisi = 4 × %d = %d cm." % (s, 4 * s))
        if k == 1:
            return mcq("Berapa luas persegi ini?" + pic, "%d cm²" % (s * s), ["%d cm²" % x for x in (4 * s, 2 * s, s * s + s)] if s != 4 else ["8 cm²", "20 cm²", "12 cm²"],
                       "Luas persegi = sisi × sisi = %d × %d = %d cm²." % (s, s, s * s))
        return mcq("Keliling sebuah persegi %d cm. Berapa panjang sisinya?" % (4 * s), "%d cm" % s, ["%d cm" % x for x in (2 * s, s + 4, s - 1)],
                   "Sisi = keliling : 4 = %d : 4 = %d cm." % (4 * s, s))

    def segitiga():
        a, t, h = ch(TRIS)
        k = R().random() < 0.5
        pic = shape_svg([(0, t), (a, t), (0, 0)], [(a / 2.0, t + 0.8, "%d cm" % a), (-1.1, t / 2.0, "%d cm" % t), (a / 2.0 + 1.2, t / 2.0 - 0.4, "%d cm" % h)],
                        right=[(0, t, 1, -1)], sc=0.9 if max(a, t) <= 9 else 0.6, label="segitiga siku-siku")
        if k:
            return mcq("Berapa luas segitiga ini?" + pic, "%d cm²" % (a * t // 2), ["%d cm²" % x for x in (a * t, a + t + h, a * h // 2)],
                       "Luas = alas × tinggi : 2 = %d × %d : 2 = %d cm²." % (a, t, a * t // 2))
        return mcq("Berapa keliling segitiga ini?" + pic, "%d cm" % (a + t + h), ["%d cm" % x for x in (a * t // 2, a + t, 2 * (a + t))],
                   "Keliling = jumlah semua sisi = %d + %d + %d = %d cm." % (a, t, h, a + t + h))

    def segitiga_umum():
        a = ri(3, 8) * 2 if R().random() < 0.5 else ri(4, 14)
        t = ri(3, 9)
        if a * t % 2:
            return None
        o = ri(1, a - 1)
        pic = shape_svg([(0, t), (a, t), (o, 0)], [(a / 2.0, t + 0.8, "alas %d cm" % a), (o + 1.6, t / 2.0, "%d cm" % t)], dashed=[((o, 0), (o, t))],
                        right=[(o, t, 1, -1)], sc=0.9 if a <= 12 else 0.6, label="segitiga dengan tinggi")
        return mcq("Berapa luas segitiga ini?" + pic, "%d cm²" % (a * t // 2), ["%d cm²" % x for x in (a * t, a + t, a * t // 2 + t)],
                   "Luas segitiga = alas × tinggi : 2 = %d × %d : 2 = %d cm²." % (a, t, a * t // 2))

    def jajar():
        o, t, s = ch([(3, 4, 5), (4, 3, 5), (6, 8, 10), (5, 12, 13)])
        a = ri(max(6, o + 2), 14)
        k = R().random() < 0.5
        pic = shape_svg([(o, 0), (a + o, 0), (a, t), (0, t)], [(a / 2.0, t + 0.8, "%d cm" % a), (o + 1.4, t / 2.0, "%d cm" % t), (o / 2.0 - 1.4, t / 2.0 - 0.6, "%d cm" % s)],
                        dashed=[((o, 0), (o, t))], right=[(o, t, 1, -1)], sc=0.8 if a + o <= 14 else 0.55, label="jajargenjang")
        if k:
            return mcq("Berapa luas jajargenjang ini?" + pic, "%d cm²" % (a * t), ["%d cm²" % x for x in (a * s, a * t // 2, 2 * (a + s))],
                       "Luas = alas × tinggi = %d × %d = %d cm² (bukan sisi miring)." % (a, t, a * t))
        return mcq("Berapa keliling jajargenjang ini?" + pic, "%d cm" % (2 * (a + s)), ["%d cm" % x for x in (2 * (a + t), a * t, a + s)],
                   "Keliling = 2 × (%d + %d) = %d cm." % (a, s, 2 * (a + s)))

    def gabung():
        W, H = ri(6, 12), ri(5, 9)
        w, h = ri(2, W - 3), ri(2, H - 2)
        k = R().random() < 0.5
        pts = [(0, 0), (W - w, 0), (W - w, h), (W, h), (W, H), (0, H)]
        labs = [(W / 2.0, H + 0.8, "%d cm" % W), (-1.1, H / 2.0, "%d cm" % H), ((W - w) / 2.0, -0.6, "%d cm" % (W - w)), (W + 1.1, (h + H) / 2.0, "%d cm" % (H - h)),
                (W - w - 1.0, h / 2.0, "%d cm" % h), (W - w / 2.0, h - 0.6, "%d cm" % w)]
        pic = shape_svg(pts, labs, sc=0.8 if W <= 10 else 0.6, label="bangun gabungan")
        if k:
            A_ = W * H - w * h
            return mcq("Berapa luas bangun gabungan ini?" + pic, "%d cm²" % A_, ["%d cm²" % x for x in (W * H, 2 * (W + H), W * H + w * h)],
                       "Luas persegi panjang besar − bagian yang terpotong = %d × %d − %d × %d = %d cm²." % (W, H, w, h, A_))
        return mcq("Berapa keliling bangun gabungan ini?" + pic, "%d cm" % (2 * (W + H)), ["%d cm" % x for x in (2 * (W + H) - w - h, W * H - w * h, 2 * (W + H) + 2 * w)],
                   "Jumlahkan semua sisi: %d cm (sama dengan keliling persegi panjang %d × %d)." % (2 * (W + H), W, H))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            p, l = ri(10, 40), ri(5, 25)
            return mcq("Sebuah kebun berbentuk persegi panjang %d m × %d m akan dipagari di sekelilingnya. Berapa meter pagar yang diperlukan?" % (p, l), "%d m" % (2 * (p + l)),
                       ["%d m" % x for x in (p * l, p + l, 2 * p + l)], "Keliling = 2 × (%d + %d) = %d m." % (p, l, 2 * (p + l)))
        if k == 1:
            p, l = ri(3, 8), ri(2, 6)
            harga = ch([50000, 75000, 80000, 100000])
            return mcq("Lantai kamar berukuran %d m × %d m akan dipasang karpet seharga %s per m². Berapa biayanya?" % (p, l, rp(harga)), rp(p * l * harga),
                       [rp(2 * (p + l) * harga), rp((p + l) * harga), rp(p * l * harga + harga)], "Luas = %d m². %d × %s = %s." % (p * l, p * l, rp(harga), rp(p * l * harga)))
        s = ri(4, 20)
        return mcq("Sebuah taman berbentuk persegi dengan keliling %d m. Berapa luas taman itu?" % (4 * s), "%d m²" % (s * s),
                   ["%d m²" % x for x in (4 * s, (4 * s) ** 2 // 4, 2 * s)], "Sisi = %d : 4 = %d m. Luas = %d × %d = %d m²." % (4 * s, s, s, s, s * s))

    sets = [("Persegi dan persegi panjang", [(persegi, 10), (persegi_panjang, 10)]),
            ("Segitiga", [(segitiga, 10), (segitiga_umum, 10)]),
            ("Jajargenjang", [(jajar, 14), (segitiga_umum, 6)]),
            ("Bangun gabungan", [(gabung, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Keliling adalah panjang semua sisi yang mengelilingi bangun (satuan cm, m). Luas adalah besar daerah di dalamnya (satuan cm², m²).",
         "Rumus luas: persegi panjang = p × l, persegi = s × s, segitiga = alas × tinggi : 2, jajargenjang = alas × tinggi.",
         "Untuk bangun gabungan, pecah menjadi bangun yang dikenal, atau kurangkan bagian yang terpotong."],
        [example("Segitiga dengan alas 10 cm dan tinggi 6 cm.", ["Luas = 10 × 6 : 2"], "30 cm²"),
         example("Persegi panjang 9 cm × 7 cm dipotong persegi panjang 3 cm × 2 cm di pojok.", ["63 − 6"], "57 cm²")],
        [["Luas segitiga = alas × tinggi (lupa dibagi 2)", "Luas segitiga = alas × tinggi : 2"],
         ["Luas jajargenjang memakai sisi miring", "Pakai tinggi yang tegak lurus dengan alas"],
         ["Keliling ditulis dalam cm²", "Keliling dalam cm, luas dalam cm²"]])
    faq = [{"q": "Apa bedanya keliling dan luas?", "a": "Keliling adalah panjang garis di sekeliling bangun, satuannya cm atau m. Luas adalah besar daerah di dalam bangun, satuannya cm² atau m²."},
           {"q": "Mengapa luas segitiga dibagi 2?", "a": "Karena segitiga adalah setengah dari persegi panjang (atau jajargenjang) dengan alas dan tinggi yang sama."},
           {"q": "Bagaimana menghitung luas bangun gabungan?", "a": "Pecah bangun menjadi beberapa persegi panjang atau segitiga, hitung luas masing-masing, lalu jumlahkan. Atau hitung bangun besar lalu kurangi bagian yang terpotong."}]
    return dict(slug="keliling-dan-luas-bangun-datar", dom="P", sort=14,
                std_text="Murid menentukan keliling dan luas berbagai bentuk bangun datar (segitiga, segiempat, dan segi banyak) serta gabungannya.",
                title="Keliling dan Luas Bangun Datar", short_title="Keliling dan Luas Bangun Datar",
                meta_desc="Latihan keliling dan luas persegi, persegi panjang, segitiga, jajargenjang, bangun gabungan, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Luas segitiga = alas × tinggi : 2", key_sub="Keliling dalam cm, luas dalam cm².", body=body, faq=faq, sets=sets)


# ============================================================ 15. sudut
def u15():
    import gen_au_maths_y5_angles as AU
    import random as _r
    AU.random = _r

    def q_fig(svg, lab):
        svg = svg.replace("aria-label='protractor measuring an angle'", "aria-label='busur derajat'").replace("aria-label='marked angle'", "aria-label='%s'" % lab)
        return "<div class='qfig'>" + lg(svg) + "</div>"

    def busur():
        d = ri(2, 17) * 10 + ch([0, 0, 5])
        if d in (90,) or d >= 180:
            return None
        pic = q_fig(AU.protractor_svg([0, d]), "busur derajat")
        return mcq("Berapa besar sudut yang diukur dengan busur derajat ini?" + pic, "%d°" % d, ["%d°" % x for x in (180 - d, d + 10, d - 5)],
                   "Salah satu kaki sudut ada di angka 0 skala dalam. Baca skala yang sama: %d°." % d)

    def jenis():
        d = ch([ri(15, 85), 90, ri(95, 175), 180, ri(190, 340)])
        nm = "lancip" if d < 90 else "siku-siku" if d == 90 else "tumpul" if d < 180 else "lurus" if d == 180 else "refleks"
        if R().random() < 0.5 or d == 180:
            return mcq("Sudut yang besarnya %d° termasuk sudut …" % d, nm, [x for x in ["lancip", "siku-siku", "tumpul", "lurus", "refleks"] if x != nm],
                       "Lancip &lt; 90°, siku-siku = 90°, tumpul antara 90° dan 180°, lurus = 180°, refleks &gt; 180°.")
        pic = q_fig(AU.angle_fig(d, ri(0, 40)), "sudut")
        return mcq("Sudut yang ditandai pada gambar termasuk sudut …" + pic, nm, [x for x in ["lancip", "siku-siku", "tumpul", "refleks"] if x != nm],
                   "Sudut ini besarnya %d°, jadi termasuk sudut %s." % (d, nm))

    def potong():
        d = ri(25, 155)
        if d == 90:
            return None
        cx, cy, L = 150, 105, 95

        def P(deg, r):
            return cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg))
        s = [line(*(P(180, L) + P(0, L)), col=INK, w=2.4), line(*(P(d + 180, L) + P(d, L)), col=INK, w=2.4)]
        names = ["p", "q", "r", "s"]
        mids = [d / 2.0, d + (180 - d) / 2.0, 180 + d / 2.0, 180 + d + (180 - d) / 2.0]
        vals = [d, 180 - d, d, 180 - d]
        gi = ri(0, 3)
        for i, m in enumerate(mids):
            X, Y = P(m, 36)
            s.append(text(X, Y + 5, ("%d°" % vals[i]) if i == gi else names[i], 15, col=RED if i == gi else INK))
        pic = fig(lg(svg_wrap(300, 210, "".join(s), "dua garis berpotongan")))
        ti = ch([i for i in range(4) if i != gi])
        good = vals[ti]
        rule = "bertolak belakang (sama besar)" if (ti - gi) % 2 == 0 else "berpelurus (jumlahnya 180°)"
        return mcq("Dua garis lurus berpotongan. Berapa besar sudut %s?" % names[ti] + pic, "%d°" % good,
                   ["%d°" % x for x in (180 - good, 360 - good, 90 - good if good < 90 else good - 90)],
                   "Sudut %s dan sudut %d° saling %s. Jadi sudut %s = %d°." % (names[ti], vals[gi], rule, names[ti], good))

    def pelurus():
        d = ri(15, 165)
        if R().random() < 0.5:
            return mcq("Dua sudut saling berpelurus (jumlahnya 180°). Jika satu sudut %d°, berapa besar sudut yang lain?" % d, "%d°" % (180 - d),
                       ["%d°" % x for x in (d, 360 - d, abs(90 - d) if d != 90 else 45)], "180° − %d° = %d°." % (d, 180 - d))
        d = ri(10, 80)
        return mcq("Dua sudut membentuk sudut siku-siku (jumlahnya 90°). Jika satu sudut %d°, berapa besar sudut yang lain?" % d, "%d°" % (90 - d),
                   ["%d°" % x for x in (180 - d, d, 90 + d)], "90° − %d° = %d°." % (d, 90 - d))

    def jam():
        from tw_common import clock
        h = ri(1, 11)
        a = 30 * h if h <= 6 else 360 - 30 * h
        pic = "<div class='qfig'>" + clock(h, 0, 160, label="jam %d" % h) + "</div>"
        return mcq("Berapa besar sudut terkecil antara jarum jam dan jarum menit pada pukul %02d.00?" % h + pic, "%d°" % a,
                   ["%d°" % x for x in (360 - a if a != 180 else 90, h * 10, a + 30 if a < 180 else a - 60)],
                   "Setiap angka pada jam berjarak 30°. Ada %d jarak: %d × 30° = %d°." % (min(h, 12 - h), min(h, 12 - h), a))

    sets = [("Mengukur sudut dengan busur", [(busur, 20)]),
            ("Jenis-jenis sudut", [(jenis, 20)]),
            ("Sudut berpelurus dan berpenyiku", [(pelurus, 20)]),
            ("Sudut pada dua garis berpotongan", [(potong, 20)]),
            ("Sudut pada jam", [(jam, 11), (potong, 9)])]
    body = lesson(
        ["Sudut diukur dengan busur derajat dalam satuan derajat (°). Letakkan titik tengah busur di titik sudut dan salah satu kaki sudut di garis 0°.",
         "Baca skala yang dimulai dari 0 pada kaki itu. Busur punya dua skala, jangan tertukar.",
         "Dua garis berpotongan membentuk empat sudut. Sudut bertolak belakang sama besar. Sudut yang bersebelahan berpelurus (jumlahnya 180°)."],
        [example("Satu sudut pada dua garis berpotongan besarnya 65°. Berapa sudut di sebelahnya?", ["Berpelurus: 180° − 65°"], "115°"),
         example("Sudut pada pukul 04.00.", ["4 jarak × 30°"], "120°")],
        [["Membaca skala yang salah (membaca 130° untuk sudut 50°)", "Mulai dari skala yang angka 0-nya ada di kaki sudut"],
         ["Sudut bertolak belakang dianggap berpelurus", "Bertolak belakang = sama besar; bersebelahan = 180°"],
         ["Sudut 90° disebut tumpul", "90° adalah sudut siku-siku; tumpul antara 90° dan 180°"]])
    faq = [{"q": "Bagaimana cara mengukur sudut dengan busur derajat?", "a": "Letakkan titik pusat busur tepat di titik sudut, impitkan garis 0° dengan salah satu kaki sudut, lalu baca angka pada kaki sudut yang lain dengan skala yang dimulai dari 0."},
           {"q": "Apa itu sudut bertolak belakang?", "a": "Sudut yang berhadapan ketika dua garis berpotongan. Besarnya selalu sama."},
           {"q": "Apa saja jenis sudut?", "a": "Lancip (kurang dari 90°), siku-siku (90°), tumpul (antara 90° dan 180°), lurus (180°), dan refleks (lebih dari 180°)."}]
    return dict(slug="mengukur-sudut", dom="P", sort=15,
                std_text="Murid mengukur besar sudut pada bangun datar atau yang dibentuk dari dua garis berpotongan.",
                title="Mengukur Sudut", short_title="Mengukur Sudut",
                meta_desc="Latihan mengukur sudut dengan busur derajat, jenis-jenis sudut, sudut berpelurus, sudut pada dua garis berpotongan, dan sudut pada jam. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Bertolak belakang = sama besar", key_sub="Bersebelahan pada garis lurus = 180°.", body=body, faq=faq, sets=sets)


# ============================================================ 16. durasi waktu
def hm(t):
    t %= 1440
    return "%02d.%02d" % divmod(t, 60)


def dur(m):
    h, mm = divmod(m, 60)
    if h and mm:
        return "%d jam %d menit" % (h, mm)
    return ("%d jam" % h) if h else ("%d menit" % mm)


def u16():
    def ubah():
        k = ri(0, 3)
        if k == 0:
            h, m = ri(1, 5), ri(5, 55)
            return mcq("%d jam %d menit = … menit" % (h, m), str(h * 60 + m), [str(h * 100 + m), str(h + m), str(h * 60 + m + 60)],
                       "1 jam = 60 menit. %d × 60 + %d = %d menit." % (h, m, h * 60 + m))
        if k == 1:
            t = ri(70, 400)
            if t % 60 == 0:
                return None
            return mcq("%d menit = … jam … menit" % t, dur(t), [dur(t // 100 * 60 + t % 100) if t % 100 < 60 and t // 100 * 60 + t % 100 != t else dur(t + 60), dur(t - 60), dur(t + 10)],
                       "%d : 60 = %d sisa %d." % (t, t // 60, t % 60))
        if k == 2:
            m, s = ri(1, 9), ri(5, 55)
            return mcq("%d menit %d detik = … detik" % (m, s), str(m * 60 + s), [str(m * 100 + s), str(m + s), str(m * 60)],
                       "1 menit = 60 detik. %d × 60 + %d = %d detik." % (m, s, m * 60 + s))
        d, h = ri(1, 4), ri(1, 23)
        return mcq("%d hari %d jam = … jam" % (d, h), str(d * 24 + h), [str(d * 12 + h), str(d * 60 + h), str(d + h)],
                   "1 hari = 24 jam. %d × 24 + %d = %d jam." % (d, h, d * 24 + h))

    def lama():
        a = ri(6 * 60, 15 * 60) // 5 * 5
        m = ri(25, 300) // 5 * 5
        b = a + m
        wrong_borrow = (b // 60 - a // 60) * 100 + (b % 60 - a % 60)
        w1 = dur(abs(b // 60 - a // 60) * 60 + abs(b % 60 - a % 60))
        return mcq("Sebuah kegiatan dimulai pukul %s dan selesai pukul %s. Berapa lama kegiatan itu?" % (hm(a), hm(b)), dur(m),
                   [w1 if w1 != dur(m) else dur(m + 60), dur(m + 40) if m % 60 + 40 < 60 else dur(m - 40), dur(m - 60) if m > 60 else dur(m + 30)],
                   "Dari %s ke %s: %s." % (hm(a), hm(b), dur(m)))

    def akhir():
        a = ri(6 * 60, 16 * 60) // 5 * 5
        m = ri(35, 280) // 5 * 5
        b = a + m
        naive = (a // 60 + m // 60) * 60 + (a % 60 + m % 60) % 100
        return mcq("%s berangkat pukul %s. Perjalanannya %s. Pukul berapa ia tiba?" % (K().next(), hm(a), dur(m)), "pukul %s" % hm(b),
                   ["pukul %s" % hm(x) for x in (b - 60, b + 40 if (a % 60 + m % 60) < 60 else b - 40, b + 60)],
                   "%s + %s = %s." % (hm(a), dur(m), hm(b)))

    def awal():
        b = ri(9 * 60, 20 * 60) // 5 * 5
        m = ri(35, 240) // 5 * 5
        a = b - m
        return mcq("Film selesai pukul %s. Lama film %s. Pukul berapa film dimulai?" % (hm(b), dur(m)), "pukul %s" % hm(a),
                   ["pukul %s" % hm(x) for x in (b + m, a + 60, a - 40 if a % 60 >= 40 else a + 40)],
                   "%s − %s = %s." % (hm(b), dur(m), hm(a)))

    def jadwal():
        st = ["Stasiun Bogor", "Stasiun Depok", "Stasiun Manggarai", "Stasiun Jakarta Kota"]
        t0 = ri(5 * 60, 9 * 60) // 5 * 5
        gaps = [ri(3, 6) * 5 for _ in range(3)]
        ts = [t0]
        for g in gaps:
            ts.append(ts[-1] + g)
        rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (s, hm(t)) for s, t in zip(st, ts))
        tb = "<table class='sn-table' style='width:auto'><thead><tr><th>Stasiun</th><th>Pukul</th></tr></thead><tbody>%s</tbody></table>" % rows
        i, j = sorted(R().sample(range(4), 2))
        m = ts[j] - ts[i]
        return mcq("Jadwal kereta ditunjukkan pada tabel. Berapa lama perjalanan dari %s ke %s?%s" % (st[i], st[j], tb), dur(m),
                   [dur(m + 5), dur(m - 5) if m > 5 else dur(m + 10), dur(ts[j] % 100 - ts[i] % 100) if ts[j] % 100 - ts[i] % 100 > 0 and ts[j] % 100 - ts[i] % 100 != m else dur(m + 15)],
                   "%s − %s = %s." % (hm(ts[j]), hm(ts[i]), dur(m)))

    def jam_gambar():
        from tw_common import clock
        h1, m1 = ri(1, 10), ch([0, 15, 30, 45, 10, 20, 40, 50])
        m = ri(20, 180) // 5 * 5
        t2 = h1 * 60 + m1 + m
        h2, m2 = divmod(t2, 60)
        if h2 > 12:
            return None
        pics = "<div class='qfig'>" + clock(h1, m1, 140, label="jam mulai") + clock(h2 % 12, m2, 140, label="jam selesai") + "</div>"
        return mcq("Jam pertama menunjukkan waktu mulai belajar dan jam kedua waktu selesai (pada pagi atau siang yang sama). Berapa lama belajarnya?" + pics, dur(m),
                   [dur(m + 60), dur(m - 15) if m > 15 else dur(m + 15), dur(m + 30)], "Dari pukul %02d.%02d sampai pukul %02d.%02d: %s." % (h1, m1, h2, m2, dur(m)))

    sets = [("Satuan waktu", [(ubah, 20)]),
            ("Lama kegiatan", [(lama, 14), (jam_gambar, 6)]),
            ("Waktu selesai", [(akhir, 20)]),
            ("Waktu mulai", [(awal, 20)]),
            ("Jadwal perjalanan", [(jadwal, 14), (jam_gambar, 6)])]
    body = lesson(
        ["1 jam = 60 menit, 1 menit = 60 detik, 1 hari = 24 jam. Waktu ditulis pukul 07.30 atau 19.30.",
         "Untuk menghitung lama, hitung dari waktu mulai ke jam bulat berikutnya, lalu sampai waktu selesai.",
         "Ingat: satu jam berisi 60 menit, bukan 100 menit."],
        [example("Dari pukul 08.45 sampai 11.20.", ["08.45 → 09.00 = 15 menit", "09.00 → 11.00 = 2 jam", "11.00 → 11.20 = 20 menit"], "2 jam 35 menit"),
         example("Berangkat 13.50, perjalanan 1 jam 25 menit.", ["13.50 + 1 jam = 14.50", "14.50 + 25 menit = 15.15"], "pukul 15.15")],
        [["11.20 − 08.45 dihitung 2 jam 75 menit", "Jam berisi 60 menit: 2 jam 35 menit"],
         ["13.50 + 25 menit = 13.75", "50 + 25 = 75 menit = 1 jam 15 menit, jadi 14.15"],
         ["2 jam 15 menit = 215 menit", "2 × 60 + 15 = 135 menit"]])
    faq = [{"q": "Bagaimana menghitung lama waktu?", "a": "Hitung dari waktu mulai ke jam bulat terdekat, lalu tambahkan jam penuh, lalu menit sisanya. Contoh: 08.45 sampai 11.20 = 15 menit + 2 jam + 20 menit = 2 jam 35 menit."},
           {"q": "Mengapa tidak boleh mengurangkan waktu seperti bilangan biasa?", "a": "Karena 1 jam = 60 menit, bukan 100 menit. Jika mengurangkan seperti biasa, hasilnya bisa salah."},
           {"q": "Bagaimana menulis waktu sore dan malam?", "a": "Gunakan sistem 24 jam: pukul 3 sore ditulis 15.00 dan pukul 7 malam ditulis 19.00."}]
    return dict(slug="durasi-waktu", dom="P", sort=16,
                std_text="Murid menghitung durasi waktu.",
                title="Menghitung Durasi Waktu", short_title="Durasi Waktu",
                meta_desc="Latihan satuan waktu jam, menit, detik, menghitung lama kegiatan, waktu mulai dan selesai, serta membaca jadwal perjalanan. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="1 jam = 60 menit", key_sub="Hitung sampai jam bulat, lalu lanjutkan.", body=body, faq=faq, sets=sets)


# ============================================================ 17. kubus dan balok
FACE_DIR = {"R": lambda f, a, b: (a, tuple(-x for x in f), b), "L": lambda f, a, b: (tuple(-x for x in a), f, b),
            "D": lambda f, a, b: (b, a, tuple(-x for x in f)), "U": lambda f, a, b: (tuple(-x for x in b), a, f)}


def fold(cells):
    """jaring-jaring: cells (c, r). Kembalikan dict sel → normal, atau None jika tidak membentuk kubus"""
    cells = set(cells)
    start = min(cells)
    st = {start: ((0, 0, -1), (1, 0, 0), (0, 1, 0))}
    todo = [start]
    while todo:
        c = todo.pop()
        f_, a_, b_ = st[c]
        for d, (dc, dr) in (("R", (1, 0)), ("L", (-1, 0)), ("D", (0, 1)), ("U", (0, -1))):
            n = (c[0] + dc, c[1] + dr)
            if n in cells and n not in st:
                st[n] = FACE_DIR[d](f_, a_, b_)
                todo.append(n)
    if len(st) != 6:
        return None
    normals = [v[0] for v in st.values()]
    return {c: v[0] for c, v in st.items()} if len(set(normals)) == 6 else None


def rand_hexomino():
    cells = {(0, 0)}
    while len(cells) < 6:
        c = ch(sorted(cells))
        d = ch([(1, 0), (-1, 0), (0, 1), (0, -1)])
        cells.add((c[0] + d[0], c[1] + d[1]))
    mx, my = min(c[0] for c in cells), min(c[1] for c in cells)
    return tuple(sorted((x - mx, y - my) for x, y in cells))


def net_svg(cells, letters=None, sz=26, label="jaring-jaring"):
    s = []
    for i, (x, y) in enumerate(cells):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (6 + x * sz, 6 + y * sz, sz, sz, FILL, GREEN))
        if letters:
            s.append(text(6 + x * sz + sz / 2.0, 6 + y * sz + sz / 2.0 + 5, letters[i], 14))
    W = (max(c[0] for c in cells) + 1) * sz + 12
    H = (max(c[1] for c in cells) + 1) * sz + 12
    return svg_wrap(W, H, "".join(s), label)


def row4(svgs, caps=("A", "B", "C", "D")):
    return "<div class='qfig'>" + "".join("<span style='display:inline-block;margin:4px 10px;text-align:center'><b>%s</b><br>%s</span>" % (c, s) for c, s in zip(caps, svgs)) + "</div>"


def canon(cells):
    """bentuk yang sama jika diputar/dicerminkan"""
    best = None
    pts = list(cells)
    for k in range(8):
        q = []
        for x, y in pts:
            for _ in range(k % 4):
                x, y = y, -x
            if k >= 4:
                x = -x
            q.append((x, y))
        mx, my = min(a for a, _ in q), min(b for _, b in q)
        t = tuple(sorted((a - mx, b - my) for a, b in q))
        best = t if best is None or t < best else best
    return best


NETS_OK, NETS_BAD = [], []


def build_nets():
    if NETS_OK:
        return
    import random as _r
    rr = _r.Random(5405)
    seen = set()
    for _ in range(20000):
        cells = {(0, 0)}
        while len(cells) < 6:
            c = rr.choice(sorted(cells))
            d = rr.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            cells.add((c[0] + d[0], c[1] + d[1]))
        cn = canon(cells)
        if cn in seen:
            continue
        seen.add(cn)
        (NETS_OK if fold(cn) else NETS_BAD).append(cn)
    NETS_OK.sort()
    NETS_BAD.sort()
    assert len(NETS_OK) == 11, len(NETS_OK)


def orient(cells):
    q = list(cells)
    for _ in range(ri(0, 3)):
        q = [(y, -x) for x, y in q]
    if R().random() < 0.5:
        q = [(-x, y) for x, y in q]
    mx, my = min(a for a, _ in q), min(b for _, b in q)
    return tuple(sorted((a - mx, b - my) for a, b in q))


def u17():
    build_nets()
    from id_k4b import kubus

    def unsur():
        b = ch(["kubus", "balok"])
        k = ch(["sisi", "rusuk", "titik sudut"])
        n = {"sisi": 6, "rusuk": 12, "titik sudut": 8}[k]
        pic = kubus(2, 2, 2, s=16) if b == "kubus" else kubus(3, 1, 2, s=16)
        return mcq("Berapa banyak %s pada sebuah %s?" % (k, b) + pic, str(n), [str(x) for x in (6, 8, 12, 4) if x != n],
                   "%s memiliki 6 sisi, 12 rusuk, dan 8 titik sudut." % b.capitalize())

    STMT = [("kubus", "Semua sisinya berbentuk persegi yang sama besar", ["Sisinya berbentuk segitiga", "Memiliki 8 sisi", "Rusuknya tidak ada yang sama panjang"]),
            ("balok", "Sisi yang berhadapan sama besar", ["Semua sisinya selalu persegi", "Memiliki 6 titik sudut", "Memiliki 10 rusuk"]),
            ("kubus", "Semua rusuknya sama panjang", ["Memiliki 6 rusuk", "Sisinya berbentuk persegi panjang yang berbeda", "Memiliki 4 titik sudut"]),
            ("balok", "Sisinya berbentuk persegi panjang (bisa juga ada yang persegi)", ["Semua rusuknya harus sama panjang", "Memiliki 5 sisi", "Memiliki 9 titik sudut"])]

    def ciri():
        b, g, bad = ch(STMT)
        pic = kubus(2, 2, 2, s=ri(13, 18)) if b == "kubus" else kubus(ri(2, 4), 1, ri(1, 3), s=ri(13, 18))
        return mcq("Pernyataan yang benar tentang %s adalah …" % b + pic, g, bad, "%s: %s." % (b.capitalize(), g.lower()))

    def hitung():
        W, D = ri(2, 4), ri(2, 3)
        h = {}
        for x in range(W):
            for y in range(D):
                up = min([h.get((x - 1, y), 4), h.get((x, y - 1), 4)])
                h[(x, y)] = ri(1 if x + y else 2, max(1, min(up, 3)))
        cells = [(x, y, z) for (x, y), hh in h.items() for z in range(hh)]
        n = len(cells)
        from kr_pics56 import iso_cubes
        pic = iso_cubes(cells, label="susunan kubus satuan", front=False)
        vis = sum(1 for (x, y), hh in h.items())
        return mcq("Berapa banyak kubus satuan pada susunan ini? (Tidak ada kubus yang melayang.)" + pic, "%d kubus" % n,
                   ["%d kubus" % x for x in (n + 1, n - 1, vis, n + 2) if x != n], "Hitung per tumpukan: %s = %d." % (" + ".join(str(h[k]) for k in sorted(h)), n))

    def jaring():
        good = orient(ch(NETS_OK))
        bads = [orient(c) for c in R().sample(NETS_BAD, 3)]
        opts = [good] + bads
        R().shuffle(opts)
        i = opts.index(good)
        pic = row4([net_svg(c, sz=20, label="rangkaian persegi %s" % "ABCD"[j]) for j, c in enumerate(opts)])
        return mcq("Manakah yang merupakan jaring-jaring kubus?" + pic, "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]],
                   "Jika dilipat, jaring-jaring %s menutup keenam sisi kubus tanpa bertumpuk. Yang lain ada sisi yang bertumpuk." % "ABCD"[i])

    def berhadapan():
        cells = orient(ch(NETS_OK))
        nr = fold(cells)
        letters = "ABCDEF"
        lab = {c: letters[i] for i, c in enumerate(cells)}
        c0 = ch(cells)
        opp = [c for c in cells if nr[c] == tuple(-x for x in nr[c0])][0]
        pic = "<div class='qfig'>" + lg(net_svg(cells, [lab[c] for c in cells], sz=34, label="jaring-jaring kubus berhuruf")) + "</div>"
        return mcq("Jaring-jaring ini dilipat menjadi kubus. Sisi yang berhadapan dengan sisi %s adalah …" % lab[c0] + pic, lab[opp],
                   [lab[c] for c in cells if c not in (c0, opp)], "Sisi yang berhadapan tidak bersentuhan. Pada jaring-jaring ini, %s berhadapan dengan %s." % (lab[c0], lab[opp]))

    def tampak():
        from kr_pics56 import iso_cubes
        W, D = ri(2, 3), ri(2, 3)
        h = {}
        for x in range(W):
            for y in range(D):
                up = min([h.get((x - 1, y), 3), h.get((x, y - 1), 3)])
                h[(x, y)] = ri(1, up)
        if len(set(h.values())) < 2:
            return None
        cells = [(x, y, z) for (x, y), hh in h.items() for z in range(hh)]
        pic = iso_cubes(cells, label="bangun dari kubus satuan").replace(">앞<", ">depan<")
        front = [max(h[(x, y)] for y in range(D)) for x in range(W)]      # dilihat dari depan (y besar)
        side = [max(h[(x, y)] for x in range(W)) for y in range(D)]       # dilihat dari kanan
        side = side[::-1]
        top = [(x, y) for x in range(W) for y in range(D)]
        which = ch(["depan", "samping kanan"])
        want = front if which == "depan" else side
        def colsvg(cols):
            s = []
            H = max(cols)
            for i, c in enumerate(cols):
                for z in range(c):
                    s.append("<rect x='%d' y='%d' width='20' height='20' fill='%s' stroke='%s' stroke-width='1.4'/>" % (6 + i * 20, 6 + (H - 1 - z) * 20, FILL, GREEN))
            return svg_wrap(len(cols) * 20 + 12, H * 20 + 12, "".join(s), "tampak")
        cands = [want, want[::-1], side if which == "depan" else front, [max(want)] * len(want), [c + 1 if i == 0 else c for i, c in enumerate(want)]]
        opts = []
        for c in cands:
            if c not in opts:
                opts.append(c)
        if len(opts) < 4:
            return None
        opts = opts[:4]
        good = opts[0]
        R().shuffle(opts)
        i = opts.index(good)
        return mcq("Gambar tampak %s dari bangun ini adalah …" % which + pic + row4([colsvg(c) for c in opts]), "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]],
                   "Dari %s, kita melihat tumpukan tertinggi di setiap kolom: %s." % (which, ", ".join(map(str, want))))

    def volume():
        a, b, c = ri(2, 5), ri(2, 4), ri(2, 4)
        return mcq("Sebuah balok disusun dari kubus satuan, panjang %d, lebar %d, dan tinggi %d kubus. Berapa banyak kubus satuan yang diperlukan?" % (a, b, c),
                   "%d kubus" % (a * b * c), ["%d kubus" % x for x in (a * b + c, a + b + c, 2 * (a * b + b * c + a * c))],
                   "%d × %d × %d = %d kubus." % (a, b, c, a * b * c))

    sets = [("Unsur kubus dan balok", [(unsur, 6), (ciri, 8), (volume, 6)]),
            ("Menyusun kubus satuan", [(hitung, 20)]),
            ("Jaring-jaring kubus", [(jaring, 20)]),
            ("Sisi yang berhadapan", [(berhadapan, 20)]),
            ("Tampak depan dan samping", [(tampak, 20)])]
    body = lesson(
        ["Kubus dan balok sama-sama punya 6 sisi, 12 rusuk, dan 8 titik sudut. Semua sisi kubus berbentuk persegi yang sama besar.",
         "Jaring-jaring kubus adalah 6 persegi yang jika dilipat menjadi kubus tanpa bertumpuk. Ada 11 bentuk jaring-jaring kubus.",
         "Tampak depan menunjukkan tumpukan tertinggi pada setiap kolom jika bangun dilihat dari depan."],
        [example("Balok 4 × 3 × 2 kubus satuan.", ["Satu lapis: 4 × 3 = 12", "2 lapis: 12 × 2"], "24 kubus"),
         example("Pada jaring-jaring bentuk salib, sisi tengah atas berhadapan dengan sisi …", ["Sisi yang berhadapan tidak bersebelahan"], "sisi paling bawah")],
        [["Menganggap 6 persegi apa saja bisa menjadi kubus", "Coba lipat: tidak boleh ada sisi yang bertumpuk"],
         ["Hanya menghitung kubus yang terlihat", "Hitung tumpukan di setiap kolom"],
         ["Sisi berhadapan dipilih yang bersebelahan", "Sisi berhadapan tidak pernah bersentuhan"]])
    faq = [{"q": "Ada berapa jaring-jaring kubus?", "a": "Ada 11 bentuk jaring-jaring kubus yang berbeda (tidak dihitung yang hanya diputar atau dibalik)."},
           {"q": "Apa bedanya kubus dan balok?", "a": "Semua rusuk kubus sama panjang dan semua sisinya persegi. Pada balok, sisinya persegi panjang dan rusuknya bisa berbeda panjang."},
           {"q": "Bagaimana menggambar tampak depan?", "a": "Lihat bangun dari depan. Pada setiap kolom, gambar persegi sebanyak tumpukan yang paling tinggi."}]
    return dict(slug="kubus-dan-balok", dom="G", sort=17,
                std_text="Murid mengkonstruksi dan mengurai bangun ruang (kubus, balok, dan gabungannya), mengenali visualisasi spasial (bagian depan, atas, dan samping), dan membandingkan karakteristik antarbangun ruang.",
                title="Kubus dan Balok: Jaring-Jaring dan Tampak", short_title="Kubus dan Balok",
                meta_desc="Latihan unsur kubus dan balok, menghitung kubus satuan, jaring-jaring kubus, sisi yang berhadapan, serta tampak depan dan samping. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="6 sisi, 12 rusuk, 8 titik sudut", key_sub="Ada 11 jaring-jaring kubus.", body=body, faq=faq, sets=sets)


# ============================================================ 18. peta berpetak
PLACES = ["Sekolah", "Pasar", "Masjid", "Taman", "Bank", "Stasiun", "Puskesmas", "Museum", "Kantor Pos", "Gereja", "Pura", "Kolam", "Bioskop", "Toko Buku"]
COLS = "ABCDEF"


def peta(places, n=6, c=76):
    s = []
    x0, y0 = 30, 8
    for i in range(n + 1):
        s.append(line(x0 + i * c, y0, x0 + i * c, y0 + n * c, "#9bb8c9", 1.2))
        s.append(line(x0, y0 + i * c, x0 + n * c, y0 + i * c, "#9bb8c9", 1.2))
    for i in range(n):
        s.append(text(x0 + i * c + c / 2.0, y0 + n * c + 20, COLS[i], 15))
        s.append(text(x0 - 14, y0 + (n - 1 - i) * c + c / 2.0 + 5, str(i + 1), 15))
    for nm, (col, row) in places.items():
        X, Y = x0 + col * c, y0 + (n - row) * c
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='5' fill='#fbe7c8' stroke='%s' stroke-width='1.2'/>" % (X + 3, Y + 10, c - 6, c - 20, INK))
        ws = nm.split(" ")
        for k, w in enumerate(ws):
            s.append(text(X + c / 2.0, Y + c / 2.0 + 5 + (k - (len(ws) - 1) / 2.0) * 14, w, 12, weight=700))
    return fig(lg(svg_wrap(x0 + n * c + 10, y0 + n * c + 30, "".join(s), "peta berpetak")))


def u18():
    def layout():
        nms = R().sample(PLACES, 6)
        cells = R().sample([(x, y) for x in range(6) for y in range(1, 7)], 6)
        return dict(zip(nms, cells))

    def nm(cell):
        return "%s%d" % (COLS[cell[0]], cell[1])

    def lokasi():
        P = layout()
        p = ch(sorted(P))
        c = P[p]
        cand = [(c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1), (c[1] - 1, c[0] + 1)]
        wr = [nm(x) for x in cand if 0 <= x[0] < 6 and 1 <= x[1] <= 6 and x != c]
        return mcq("Pada peta berpetak ini, %s berada di petak …" % p + peta(P), nm(c), wr,
                   "Baca huruf di bawah (kolom) lalu angka di samping (baris): %s." % nm(c))

    def apa():
        P = layout()
        p = ch(sorted(P))
        return mcq("Bangunan yang berada di petak %s adalah …" % nm(P[p]) + peta(P), p, [x for x in sorted(P) if x != p],
                   "Kolom %s, baris %d: %s." % (COLS[P[p][0]], P[p][1], p))

    def gerak():
        P = layout()
        a = ch(sorted(P))
        ca = P[a]
        dx, dy = ri(-3, 3), ri(-3, 3)
        tx, ty = ca[0] + dx, ca[1] + dy
        if (dx, dy) == (0, 0) or not (0 <= tx < 6 and 1 <= ty <= 6):
            return None
        parts = []
        if dx:
            parts.append("%d petak ke %s" % (abs(dx), "kanan" if dx > 0 else "kiri"))
        if dy:
            parts.append("%d petak ke %s" % (abs(dy), "atas" if dy > 0 else "bawah"))
        g = nm((tx, ty))
        wr = [nm((ca[0] - dx, ca[1] + dy)) if 0 <= ca[0] - dx < 6 and 1 <= ca[1] + dy <= 6 else None, nm((ca[0] + dx, ca[1] - dy)) if 0 <= ca[0] + dx < 6 and 1 <= ca[1] - dy <= 6 else None,
              nm((ca[0] + dy, ca[1] + dx)) if 0 <= ca[0] + dy < 6 and 1 <= ca[1] + dx <= 6 else None, nm((tx, ty % 6 + 1)), nm(((tx + 1) % 6, ty))]
        return mcq("%s berjalan dari %s %s. Di petak mana ia sekarang?" % (K().next(), a, " lalu ".join(parts)) + peta(P), g, [w for w in wr if w and w != g],
                   "Mulai dari %s, lalu %s: %s." % (nm(ca), " dan ".join(parts), g))

    def jarak():
        P = layout()
        a, b = R().sample(sorted(P), 2)
        ca, cb = P[a], P[b]
        dx, dy = cb[0] - ca[0], cb[1] - ca[1]
        if dx == 0 or dy == 0:
            return None
        g = "%d petak ke %s dan %d petak ke %s" % (abs(dx), "kanan" if dx > 0 else "kiri", abs(dy), "atas" if dy > 0 else "bawah")
        bad = ["%d petak ke %s dan %d petak ke %s" % (abs(dx), "kiri" if dx > 0 else "kanan", abs(dy), "atas" if dy > 0 else "bawah"),
               "%d petak ke %s dan %d petak ke %s" % (abs(dy), "kanan" if dx > 0 else "kiri", abs(dx), "atas" if dy > 0 else "bawah"),
               "%d petak ke %s dan %d petak ke %s" % (abs(dx), "kanan" if dx > 0 else "kiri", abs(dy), "bawah" if dy > 0 else "atas")]
        return mcq("Bagaimana cara berjalan dari %s ke %s mengikuti garis petak?" % (a, b) + peta(P), g, bad,
                   "%s di %s dan %s di %s." % (a, nm(ca), b, nm(cb)))

    def dekat():
        P = layout()
        a = ch(sorted(P))
        ca = P[a]
        dd = {p: abs(c[0] - ca[0]) + abs(c[1] - ca[1]) for p, c in P.items() if p != a}
        best = min(dd.values())
        win = [p for p, v in dd.items() if v == best]
        if len(win) != 1:
            return None
        return mcq("Bangunan mana yang paling dekat dengan %s jika berjalan mengikuti garis petak?" % a + peta(P), win[0], [p for p in sorted(dd) if p != win[0]],
                   "Hitung banyak petak ke kanan/kiri ditambah ke atas/bawah. %s hanya %d petak dari %s." % (win[0], best, a))

    sets = [("Menentukan letak", [(lokasi, 20)]),
            ("Membaca petak", [(apa, 20)]),
            ("Bergerak pada peta", [(gerak, 20)]),
            ("Arah dan jarak", [(jarak, 20)]),
            ("Yang paling dekat", [(dekat, 14), (gerak, 6)])]
    body = lesson(
        ["Peta berpetak memakai huruf untuk kolom (mendatar) dan angka untuk baris (tegak). Letak ditulis huruf dulu lalu angka, misalnya C4.",
         "Untuk menentukan letak, lihat huruf di bawah kolom, lalu angka di samping baris.",
         "Saat bergerak, hitung petak ke kanan atau kiri, lalu ke atas atau bawah."],
        [example("Sekolah di B2. Berjalan 3 petak ke kanan dan 2 petak ke atas.", ["B → C, D, E", "2 → 3, 4"], "E4"),
         example("Pasar di D5 dan Bank di A2.", ["D ke A = 3 petak ke kiri", "5 ke 2 = 3 petak ke bawah"], "3 ke kiri, 3 ke bawah")],
        [["Menulis angka dulu (4C)", "Tulis huruf kolom dulu, lalu angka baris: C4"],
         ["Menghitung petak awal sebagai langkah pertama", "Langkah pertama adalah petak sesudahnya"],
         ["Tertukar arah kiri dan kanan", "Huruf makin ke kanan: A, B, C, …"]])
    faq = [{"q": "Apa itu peta berpetak?", "a": "Peta yang dibagi menjadi petak-petak sama besar. Setiap petak punya nama dari huruf kolom dan angka baris, misalnya B3."},
           {"q": "Mengapa huruf ditulis lebih dulu?", "a": "Supaya semua orang membaca letak dengan cara yang sama: lihat kolom dulu (huruf), lalu baris (angka)."},
           {"q": "Bagaimana mengukur jarak pada peta berpetak?", "a": "Hitung banyak petak yang dilewati ke kanan atau kiri, lalu ke atas atau bawah, lalu jumlahkan."}]
    return dict(slug="peta-berpetak", dom="G", sort=18,
                std_text="Murid menentukan lokasi pada peta yang menggunakan sistem berpetak.",
                title="Menentukan Lokasi pada Peta Berpetak", short_title="Peta Berpetak",
                meta_desc="Latihan menentukan letak bangunan pada peta berpetak, membaca nama petak, bergerak ke kanan, kiri, atas, dan bawah, serta menentukan yang paling dekat. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Huruf kolom, lalu angka baris", key_sub="Contoh: C4 = kolom C, baris 4.", body=body, faq=faq, sets=sets)


# ============================================================ 19. pengolahan data
def pikto_k(data, unit, k):
    s, y, lw = [], 10, 110
    for name, v in data:
        s.append(text(6, y + 17, name, 13, anchor="start", weight=600))
        for i in range(v // k):
            cx = lw + 14 + i * 26
            s.append("<rect x='%d' y='%d' width='18' height='20' rx='3' fill='#7fb3d5' stroke='%s' stroke-width='1.2'/>" % (cx - 9, y + 2, INK))
        s.append(line(lw, y - 4, lw, y + 28, "#bbb", 1))
        y += 32
    mx = max(v for _, v in data) // k
    s.append("<rect x='9' y='%d' width='18' height='20' rx='3' fill='#7fb3d5' stroke='%s' stroke-width='1.2'/>" % (y + 4, INK))
    s.append(text(34, y + 19, "= %d %s" % (k, unit), 13, anchor="start", weight=600))
    return wrap(max(lw + 24 + mx * 26, 220), y + 34, "".join(s), "piktogram", lg=True)


def u19():
    def frek():
        vals = ch([(list(range(5, 11)), "nilai ulangan", "Nilai"), (list(range(31, 37)), "ukuran sepatu", "Ukuran"), (list(range(130, 136)), "tinggi badan (cm)", "Tinggi")])
        xs, what, head = vals
        data = [ch(xs[1:-1]) if R().random() < 0.5 else ch(xs) for _ in range(ri(16, 24))]
        v = ch(sorted(set(data)))
        n = data.count(v)
        lst = ", ".join(str(x) for x in data)
        return mcq("Data %s %d siswa: %s. Berapa banyak siswa dengan %s %d?" % (what, len(data), lst, head.lower(), v), "%d siswa" % n,
                   ["%d siswa" % x for x in (n + 1, n - 1 if n > 1 else n + 2, len(data) - n, n + 2)], "Hitung angka %d pada data (pakai turus): ada %d." % (v, n))

    def tabel():
        xs = list(range(ri(5, 6), 11))
        fr_ = [ri(1, 9) for _ in xs]
        rows = "".join("<tr><td>%d</td><td>%d</td></tr>" % (x, f_) for x, f_ in zip(xs, fr_))
        tb = "<table class='sn-table' style='width:auto'><thead><tr><th>Nilai</th><th>Frekuensi</th></tr></thead><tbody>%s</tbody></table>" % rows
        k = ri(0, 3)
        tot = sum(fr_)
        if k == 0:
            return mcq("Tabel frekuensi nilai ulangan matematika.%s Berapa banyak siswa seluruhnya?" % tb, "%d siswa" % tot, ["%d siswa" % x for x in (tot + 1, len(xs), sum(xs))],
                       "Jumlahkan frekuensinya: %s = %d." % (" + ".join(map(str, fr_)), tot))
        if k == 1:
            m = max(fr_)
            if fr_.count(m) > 1:
                return None
            v = xs[fr_.index(m)]
            return mcq("Tabel frekuensi nilai ulangan matematika.%s Nilai berapa yang paling banyak diperoleh siswa?" % tb, str(v), [str(x) for x in xs if x != v],
                       "Frekuensi terbesar %d ada pada nilai %d." % (m, v))
        if k == 2:
            t = ri(7, 9)
            n = sum(f_ for x, f_ in zip(xs, fr_) if x >= t)
            return mcq("Tabel frekuensi nilai ulangan matematika.%s Berapa siswa yang mendapat nilai %d atau lebih?" % (tb, t), "%d siswa" % n,
                       ["%d siswa" % x for x in (n - fr_[xs.index(t)], tot - n, n + 1) if x >= 0], "Jumlahkan frekuensi nilai %d sampai 10: %d." % (t, n))
        t = ri(6, 8)
        n = sum(f_ for x, f_ in zip(xs, fr_) if x < t)
        if n == 0:
            return None
        return mcq("Tabel frekuensi nilai ulangan matematika.%s Siswa dengan nilai kurang dari %d harus ikut remedial. Berapa siswa yang ikut remedial?" % (tb, t), "%d siswa" % n,
                   ["%d siswa" % x for x in (n + fr_[xs.index(t)], tot - n, n + 1)], "Jumlahkan frekuensi nilai di bawah %d: %d." % (t, n))

    def batang():
        weeks = ["Minggu 1", "Minggu 2", "Minggu 3", "Minggu 4", "Minggu 5"]
        st = ri(2, 6)
        vals = [st]
        for _ in range(4):
            vals.append(vals[-1] + ri(1, 5))
        data = list(zip([w.replace("Minggu ", "M") for w in weeks], vals))
        pic = diagram_batang(data, "Tinggi (cm)", "diagram batang tinggi tanaman", 2 if max(vals) > 20 else 1)
        k = ri(0, 2)
        if k == 0:
            i = ri(1, 4)
            g = vals[i] - vals[i - 1]
            return mcq("Diagram batang menunjukkan tinggi tanaman kacang setiap minggu (M1 = minggu 1).%s Berapa cm tanaman bertambah tinggi dari minggu %d ke minggu %d?" % (pic, i, i + 1),
                       "%d cm" % g, ["%d cm" % x for x in (vals[i], vals[i] + vals[i - 1], g + 1)], "%d − %d = %d cm." % (vals[i], vals[i - 1], g))
        if k == 1:
            g = vals[4] - vals[0]
            return mcq("Diagram batang menunjukkan tinggi tanaman kacang setiap minggu (M1 = minggu 1).%s Berapa cm pertambahan tinggi dari minggu 1 sampai minggu 5?" % pic,
                       "%d cm" % g, ["%d cm" % x for x in (vals[4], sum(vals), g + 2)], "%d − %d = %d cm." % (vals[4], vals[0], g))
        incs = [vals[i] - vals[i - 1] for i in range(1, 5)]
        m = max(incs)
        if incs.count(m) > 1:
            return None
        i = incs.index(m) + 1
        opts = ["minggu %d ke minggu %d" % (j, j + 1) for j in range(1, 5)]
        return mcq("Diagram batang menunjukkan tinggi tanaman kacang setiap minggu (M1 = minggu 1).%s Kapan pertambahan tinggi paling besar?" % pic, opts[i - 1], [o for o in opts if o != opts[i - 1]],
                   "Pertambahannya %s cm. Yang terbesar %d cm, dari minggu %d ke minggu %d." % (", ".join(map(str, incs)), m, i, i + 1))

    def pikto():
        k = ch([2, 5, 10])
        cats = R().sample(["Kelas 5A", "Kelas 5B", "Kelas 5C", "Kelas 5D", "Kelas 6A"], 4)
        vals = [k * ri(1, 8) for _ in cats]
        data = list(zip(cats, vals))
        pic = pikto_k(data, "buku", k)
        q = ri(0, 2)
        if q == 0:
            c, v = ch(data)
            return mcq("Piktogram banyak buku yang dikumpulkan setiap kelas.%s Berapa buku yang dikumpulkan %s?" % (pic, c), "%d buku" % v,
                       ["%d buku" % x for x in (v // k, v + k, v - k if v > k else v + 2 * k)], "Ada %d gambar, setiap gambar = %d buku: %d × %d = %d." % (v // k, k, v // k, k, v))
        if q == 1:
            t = sum(vals)
            return mcq("Piktogram banyak buku yang dikumpulkan setiap kelas.%s Berapa jumlah semua buku?" % pic, "%d buku" % t,
                       ["%d buku" % x for x in (t // k, t + k, t - k)], "Ada %d gambar × %d = %d buku." % (t // k, k, t))
        (a, va), (b, vb) = R().sample(data, 2)
        if va == vb:
            return None
        return mcq("Piktogram banyak buku yang dikumpulkan setiap kelas.%s Berapa selisih buku %s dan %s?" % (pic, a, b), "%d buku" % abs(va - vb),
                   ["%d buku" % x for x in (abs(va - vb) // k, va + vb, abs(va - vb) + k)], "%d − %d = %d buku." % (max(va, vb), min(va, vb), abs(va - vb)))

    sets = [("Mengolah data menjadi frekuensi", [(frek, 20)]),
            ("Tabel frekuensi", [(tabel, 20)]),
            ("Diagram batang data pengukuran", [(batang, 20)]),
            ("Piktogram dengan skala", [(pikto, 20)]),
            ("Campuran", [(tabel, 7), (batang, 7), (pikto, 6)])]
    body = lesson(
        ["Data dapat diringkas dalam tabel frekuensi. Frekuensi adalah banyaknya suatu data muncul.",
         "Pada piktogram, perhatikan keterangan: satu gambar bisa mewakili 2, 5, atau 10 benda.",
         "Pada diagram batang data pengukuran, bandingkan tinggi batang untuk melihat perubahan."],
        [example("Data: 7, 8, 8, 6, 7, 8, 9. Berapa frekuensi nilai 8?", ["Hitung angka 8: ada 3"], "3"),
         example("Piktogram: 4 gambar, satu gambar = 5 buku.", ["4 × 5"], "20 buku")],
        [["Lupa keterangan piktogram (4 gambar = 4 buku)", "Kalikan dengan nilai satu gambar: 4 × 5 = 20"],
         ["Frekuensi dianggap sama dengan nilainya", "Frekuensi adalah berapa kali nilai itu muncul"],
         ["Membaca diagram batang tanpa melihat skala", "Perhatikan angka pada sumbu tegak"]])
    faq = [{"q": "Apa itu tabel frekuensi?", "a": "Tabel yang menunjukkan setiap nilai data dan berapa kali nilai itu muncul (frekuensi). Tabel ini membuat data mudah dibaca."},
           {"q": "Bagaimana membuat tabel frekuensi?", "a": "Tulis semua nilai yang mungkin, buat turus setiap kali nilai muncul, lalu hitung turusnya."},
           {"q": "Apa itu data hasil pengukuran?", "a": "Data yang didapat dari mengukur, misalnya tinggi badan, berat, atau tinggi tanaman setiap minggu."}]
    return dict(slug="tabel-frekuensi-dan-diagram", dom="D", sort=19,
                std_text="Murid mengurutkan, membandingkan, menyajikan, dan menganalisis data banyak benda dan data hasil pengukuran dalam bentuk gambar, piktogram, diagram batang, dan tabel frekuensi untuk mendapatkan informasi.",
                title="Tabel Frekuensi, Piktogram, dan Diagram Batang", short_title="Tabel Frekuensi dan Diagram",
                meta_desc="Latihan mengolah data menjadi tabel frekuensi, membaca tabel frekuensi, diagram batang data pengukuran, dan piktogram dengan skala. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Frekuensi = berapa kali muncul", key_sub="Periksa keterangan dan skala gambar.", body=body, faq=faq, sets=sets)


# ============================================================ 20. peluang
COL = [("merah", "#e15759"), ("biru", "#4e79a7"), ("hijau", "#59a14f"), ("kuning", "#edc948")]


def kantong(cnt):
    s = ["<path d='M30 40 Q20 150 110 160 Q200 150 190 40 Z' fill='#f3ead8' stroke='%s' stroke-width='2'/>" % INK,
         "<rect x='60' y='22' width='100' height='20' rx='6' fill='#e6d5b8' stroke='%s' stroke-width='1.5'/>" % INK]
    pts = [(55 + (i % 6) * 22, 62 + (i // 6) * 22) for i in range(24)]
    items = [c for c, n in cnt for _ in range(n)]
    order = list(range(len(items)))
    A.R.shuffle(order)
    for i, k in enumerate(order):
        col = dict(COL)[items[k]]
        x, y = pts[i]
        s.append("<circle cx='%d' cy='%d' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x, y, col, INK))
    return fig(svg_wrap(220, 170, "".join(s), "kantong berisi kelereng: " + ", ".join("%d %s" % (n, c) for c, n in cnt)))


def spinner(parts):
    r, cx, cy = 70, 80, 80
    s = []
    tot = len(parts)
    for i, c in enumerate(parts):
        a0 = -math.pi / 2 + 2 * math.pi * i / tot
        a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / tot
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, cx + r * math.cos(a1), cy + r * math.sin(a1), dict(COL)[c], INK))
    s.append("<path d='M%d %d L%d %d' stroke='%s' stroke-width='3'/><circle cx='%d' cy='%d' r='5' fill='%s'/>" % (cx, cy, cx + 30, cy - 40, INK, cx, cy, INK))
    return fig(svg_wrap(160, 160, "".join(s), "roda putar dengan %d bagian sama besar" % tot))


def u20():
    def kel():
        cs = R().sample([c for c, _ in COL], ri(2, 4))
        ns = R().sample(range(1, 9), len(cs))
        cnt = list(zip(cs, ns))
        big = R().random() < 0.5
        k = max(cnt, key=lambda t: t[1]) if big else min(cnt, key=lambda t: t[1])
        return mcq("Sebuah kelereng diambil dari kantong ini tanpa melihat. Warna apa yang %s terambil?" % ("paling mungkin" if big else "paling kecil kemungkinannya") + kantong(cnt),
                   k[0], [c for c in [x for x, _ in COL] if c != k[0]][:3],
                   "Kelereng %s paling %s (%d butir)." % (k[0], "banyak" if big else "sedikit", k[1]))

    def banding():
        cs = R().sample([c for c, _ in COL], 2)
        a, b = R().sample(range(1, 10), 2)
        cnt = [(cs[0], a), (cs[1], b)]
        g = "Mengambil %s lebih mungkin" % (cs[0] if a > b else cs[1])
        return mcq("Kantong berisi %d kelereng %s dan %d kelereng %s. Pernyataan yang benar adalah …" % (a, cs[0], b, cs[1]) + kantong(cnt), g,
                   ["Mengambil %s lebih mungkin" % (cs[1] if a > b else cs[0]), "Keduanya sama mungkin", "Pasti terambil %s" % cs[0]],
                   "Warna yang lebih banyak lebih mungkin terambil: %d dan %d." % (a, b))

    def pasti():
        k = ri(0, 3)
        c1, c2 = R().sample([c for c, _ in COL], 2)
        n = ri(3, 10)
        if k == 0:
            return mcq("Kantong berisi %d kelereng %s saja. Mengambil kelereng %s adalah kejadian yang …" % (n, c1, c1) + kantong([(c1, n)]), "pasti",
                       ["mustahil", "mungkin", "kurang mungkin"], "Semua kelereng berwarna %s, jadi pasti terambil %s." % (c1, c1))
        if k == 1:
            return mcq("Kantong berisi %d kelereng %s saja. Mengambil kelereng %s adalah kejadian yang …" % (n, c1, c2) + kantong([(c1, n)]), "mustahil",
                       ["pasti", "mungkin", "lebih mungkin"], "Tidak ada kelereng %s, jadi mustahil terambil." % c2)
        if k == 2:
            d = ri(1, 6)
            ev = ch([("angka lebih dari 6", "mustahil"), ("angka kurang dari 7", "pasti"), ("angka %d" % d, "mungkin"), ("angka genap", "mungkin")])
            return mcq("Sebuah dadu bermata 1 sampai 6 dilempar. Muncul %s adalah kejadian yang …" % ev[0], ev[1],
                       [x for x in ["pasti", "mustahil", "mungkin", "lebih mungkin daripada tidak muncul"] if x != ev[1]],
                       "Mata dadu 1, 2, 3, 4, 5, 6. Jadi muncul %s %s." % (ev[0], ev[1]))
        m = ri(1, n - 1)
        return mcq("Kantong berisi %d kelereng %s dan %d kelereng %s. Mengambil kelereng %s adalah kejadian yang …" % (m, c1, n - m, c2, c1) + kantong([(c1, m), (c2, n - m)]), "mungkin",
                   ["pasti", "mustahil", "tidak bisa terjadi"], "Ada kelereng %s di dalam kantong, tetapi juga ada warna lain. Jadi mungkin terambil." % c1)

    def putar():
        n = ch([4, 6, 8])
        cs = R().sample([c for c, _ in COL], 3)
        parts = []
        cnts = R().sample(range(1, n - 1), 1)[0]
        rest = n - cnts
        a2 = ri(1, rest - 1) if rest > 1 else 0
        parts = [cs[0]] * cnts + [cs[1]] * a2 + [cs[2]] * (rest - a2)
        if rest - a2 <= 0:
            return None
        R().shuffle(parts)
        counts = {c: parts.count(c) for c in set(parts)}
        big = R().random() < 0.5
        m = max(counts.values()) if big else min(counts.values())
        win = [c for c, v in counts.items() if v == m]
        if len(win) != 1:
            return None
        return mcq("Roda ini diputar. Warna apa yang %s ditunjuk jarum?" % ("paling mungkin" if big else "paling kecil kemungkinannya") + spinner(parts), win[0],
                   [c for c in [x for x, _ in COL] if c != win[0]], "Bagian %s paling %s (%d dari %d bagian)." % (win[0], "banyak" if big else "sedikit", m, n))

    def dua_kantong():
        c = ch([x for x, _ in COL])
        o = ch([x for x, _ in COL if x != c])
        a, b = ri(1, 5), ri(1, 5)
        x_, y_ = ri(1, 5), ri(1, 5)
        pa, pb = F(a, a + b), F(x_, x_ + y_)
        if pa == pb:
            return None
        g = "Kantong A" if pa > pb else "Kantong B"
        return mcq("Kantong A berisi %d kelereng %s dan %d kelereng %s. Kantong B berisi %d kelereng %s dan %d kelereng %s. Dari kantong mana lebih mungkin terambil kelereng %s?" % (a, c, b, o, x_, c, y_, o, c),
                   g, ["Kantong B" if g == "Kantong A" else "Kantong A", "Sama saja", "Tidak dapat ditentukan"],
                   "Bandingkan bagian %s: kantong A %d dari %d, kantong B %d dari %d." % (c, a, a + b, x_, x_ + y_))

    sets = [("Paling mungkin dan paling kecil kemungkinannya", [(kel, 20)]),
            ("Lebih mungkin atau kurang mungkin", [(banding, 20)]),
            ("Pasti, mungkin, mustahil", [(pasti, 20)]),
            ("Roda putar", [(putar, 20)]),
            ("Membandingkan dua kantong", [(dua_kantong, 20)])]
    body = lesson(
        ["Kemungkinan menunjukkan seberapa mudah suatu kejadian terjadi: mustahil, kurang mungkin, mungkin, lebih mungkin, atau pasti.",
         "Pada kantong kelereng, warna yang paling banyak paling mungkin terambil.",
         "Untuk membandingkan dua kantong, lihat bagiannya dari seluruh isi kantong, bukan banyaknya saja."],
        [example("Kantong berisi 5 merah dan 2 biru. Warna yang lebih mungkin terambil?", ["5 &gt; 2"], "merah"),
         example("Dadu 1–6. Muncul angka 7?", ["Tidak ada angka 7"], "mustahil")],
        [["Warna yang sedikit dianggap mustahil", "Selama ada, kejadian itu mungkin"],
         ["Membandingkan dua kantong dari banyaknya saja", "Lihat bagiannya dari seluruh isi kantong"],
         ["Roda dengan bagian lebih besar diabaikan", "Bagian yang lebih banyak lebih mungkin ditunjuk"]])
    faq = [{"q": "Apa itu percobaan acak?", "a": "Percobaan yang hasilnya tidak bisa ditentukan sebelumnya, misalnya melempar dadu, memutar roda, atau mengambil kelereng tanpa melihat."},
           {"q": "Kapan suatu kejadian disebut pasti?", "a": "Jika kejadian itu selalu terjadi. Contoh: mengambil kelereng merah dari kantong yang hanya berisi kelereng merah."},
           {"q": "Kapan suatu kejadian disebut mustahil?", "a": "Jika kejadian itu tidak mungkin terjadi. Contoh: muncul angka 7 pada dadu bermata 1 sampai 6."}]
    return dict(slug="peluang", dom="D", sort=20,
                std_text="Murid menentukan kejadian dengan kemungkinan yang lebih besar atau lebih kecil dalam suatu percobaan acak.",
                title="Peluang: Kejadian Lebih Mungkin dan Kurang Mungkin", short_title="Peluang",
                meta_desc="Latihan menentukan kejadian yang paling mungkin, membandingkan kemungkinan, kejadian pasti, mungkin, dan mustahil, roda putar, dan dua kantong kelereng. 100 soal dengan kunci jawaban untuk kelas 5 SD.",
                key_big="Yang paling banyak paling mungkin", key_sub="Bandingkan bagiannya dari seluruh isi.", body=body, faq=faq, sets=sets)
