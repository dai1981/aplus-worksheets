# -*- coding: utf-8 -*-
"""Indonesia / Matematika / Kelas 7 (SMP, Fase D)。python3 tools/id_smp.py 7 [番号…]"""
from fractions import Fraction as Fr
import id_smp as S
from id_smp import (ri, ch, nz, sh, num, sn, par, pd, dz, fq, expr, lin, M, MN, MD, rp, pct, NB, MINUS,
                    numline, kosy, figure, poly_ang, sejajar, pie, bars, tab, unit, fig, wrap, text, line, INK, BLUE, RED, FILL, GREEN)

T = "Kelas 7"


def lt(a, b):
    return "%s &lt; %s" % (a, b)


def gt(a, b):
    return "%s &gt; %s" % (a, b)


# ============================================================ 1. bilangan bulat
def u1():
    def garis():
        lo = ri(-10, -4)
        hi = lo + 10
        v = ri(lo + 1, hi - 1)
        if v == 0:
            return None
        k = ri(0, 1)
        if k == 0:
            return MN("Bilangan bulat yang ditunjukkan oleh titik A adalah …" + numline(lo, hi, [(v, "A")], every=2),
                      v, [-v, v + 1, v - 1, v + 2], "Hitung ruas dari 0. Titik A berada %d ruas di %s 0, jadi A = %s." % (abs(v), "kiri" if v < 0 else "kanan", sn(v)))
        w = ri(lo + 1, hi - 1)
        if w == v or w == 0 or (w > 0) == (v > 0):
            return None
        return MN("Pada garis bilangan, A = %s dan B = %s. Berapa jarak A ke B?" % (sn(v), sn(w)) + numline(lo, hi, [(v, "A"), (w, "B")], every=2),
                  abs(v - w), [abs(v) + abs(w) if abs(v) + abs(w) != abs(v - w) else abs(v - w) + 2, abs(abs(v) - abs(w)), abs(v - w) + 1, abs(v - w) - 1],
                  "Hitung ruas dari A ke B: %s − %s = %d satuan." % (sn(max(v, w)), par(min(v, w)), abs(v - w)), unit="satuan")

    def lawan():
        v = nz(-60, 60)
        k = ri(0, 2)
        if k == 0:
            return MN("Lawan dari %s adalah …" % sn(v), -v, [v, abs(v) + 1, -v - 1 if v > 0 else -v + 1, 0],
                      "Lawan suatu bilangan berjarak sama dari 0 tetapi di sisi lain. Lawan dari %s adalah %s." % (sn(v), sn(-v)))
        if k == 1:
            n = abs(v)
            a, b = ch([("naik %d meter" % n, "turun %d meter" % n), ("untung Rp%s" % num(n * 1000), "rugi Rp%s" % num(n * 1000)),
                       ("%d meter di atas permukaan laut" % n, "%d meter di bawah permukaan laut" % n), ("maju %d langkah" % n, "mundur %d langkah" % n),
                       ("suhu %d°C di atas nol" % n, "suhu %d°C di bawah nol" % n)])
            m = n * 1000 if "Rp" in a else n
            return MN("Jika \u201c%s\u201d ditulis %s, maka \u201c%s\u201d ditulis …" % (a, num(m), b), -m, [m, -m + 1, 0, -2 * m],
                      "Arah yang berlawanan diberi tanda negatif: %s." % sn(-m))
        v = ri(2, 40)
        return MN("Bilangan bulat yang berjarak %d dari 0 dan terletak di kiri 0 adalah …" % v, -v, [v, -v + 1, -v - 1, 0],
                  "Di kiri 0 berarti negatif, jadi %s." % sn(-v))

    def banding():
        a, b = nz(-30, 30), nz(-30, 30)
        if a == b:
            return None
        if ri(0, 2) and (a > 0 or b > 0):
            a, b = -abs(a), -abs(b)
            if a == b:
                return None
        q = "Mana yang benar untuk bilangan %s dan %s?" % (sn(a), sn(b))
        if a < b:
            c = lt(sn(a), sn(b))
            ws = [gt(sn(a), sn(b)), lt(sn(b), sn(a)), "%s = %s" % (sn(a), sn(b))]
        else:
            c = gt(sn(a), sn(b))
            ws = [lt(sn(a), sn(b)), gt(sn(b), sn(a)), "%s = %s" % (sn(a), sn(b))]
        return M(q, c, ws, "Pada garis bilangan, bilangan di sebelah kanan lebih besar. %s." % (c if a > b else c))

    def urut():
        xs = sorted(set(nz(-25, 25) for _ in range(5)))
        if len(xs) < 4:
            return None
        xs = xs[:4]
        r = sh(xs)
        up = ri(0, 1)
        f = lambda l: "; ".join(sn(x) for x in l)
        c = f(xs if up else xs[::-1])
        byabs = sorted(xs, key=lambda x: (abs(x), x))
        ws = [f(xs[::-1] if up else xs), f(byabs if up else byabs[::-1]), f(sorted(xs, key=lambda x: (x < 0, abs(x))))]
        return M("Urutkan dari yang %s: %s" % ("terkecil ke terbesar" if up else "terbesar ke terkecil", f(r)), c, ws,
                 "Bilangan negatif yang angkanya besar justru lebih kecil. Urutannya: %s." % c)

    def ekstrem():
        xs = sorted(set(nz(-40, 40) for _ in range(5)))
        if len(xs) < 4:
            return None
        xs = sh(xs[:4])
        big = ri(0, 1)
        v = max(xs) if big else min(xs)
        ws = [x for x in xs if x != v] + [max(xs, key=abs)]
        return MN("Bilangan %s dari %s adalah …" % ("terbesar" if big else "terkecil", "; ".join(sn(x) for x in xs)), v, ws,
                  "Bilangan paling %s pada garis bilangan adalah %s." % ("kanan" if big else "kiri", sn(v)))

    def antara():
        a = ri(-12, 2)
        b = ri(a + 3, a + 12)
        n = b - a - 1
        k = ri(0, 1)
        if k == 0:
            return MN("Ada berapa bilangan bulat di antara %s dan %s?" % (sn(a), sn(b)), n, [n + 1, n + 2, b - a + 1 if b - a + 1 != n + 2 else n - 1],
                      "Bilangan bulat di antara %s dan %s adalah %s sampai %s: ada %d bilangan." % (sn(a), sn(b), sn(a + 1), sn(b - 1), n))
        neg = [x for x in range(a + 1, b) if x < 0]
        if not neg:
            return None
        return MN("Ada berapa bilangan bulat negatif yang lebih besar dari %s?" % sn(a), len(neg) if b > 0 else -a - 1, [-a, -a + 1, -a - 2 if -a - 2 >= 0 else -a + 2],
                  "Bilangan negatif yang lebih besar dari %s: %s sampai −1, ada %d bilangan." % (sn(a), sn(a + 1), -a - 1))

    def cerita():
        k = ri(0, 5)
        if k == 0:
            t, d = ri(-12, -1), ri(3, 15)
            return MN("Suhu pagi di puncak gunung %s°C. Siang hari suhu naik %d°C. Suhu siang hari adalah …" % (sn(t), d), t + d,
                      [t - d, -(t + d) if t + d else 1, abs(t) + d], "%s + %d = %s." % (sn(t), d, sn(t + d)), unit="°C")
        if k == 1:
            t, d = ri(-5, 8), ri(6, 15)
            return MN("Suhu sebuah ruang pendingin %s°C, lalu turun %d°C. Suhunya sekarang …" % (sn(t), d), t - d,
                      [t + d, d - t, -(t + d)], "%s − %d = %s." % (sn(t), d, sn(t - d)), unit="°C")
        if k == 2:
            a, b = ri(-15, -1), ri(10, 35)
            c1, c2 = ch([("Moskow", "Jakarta"), ("Tokyo", "Surabaya"), ("Seoul", "Medan"), ("Beijing", "Makassar")])
            return MN("Suhu di %s %s°C dan di %s %d°C. Berapa selisih suhu kedua kota?" % (c1, sn(a), c2, b), b - a,
                      [b + a, b - a + 1, abs(a + b) + 1 if abs(a + b) + 1 != b - a else b - a - 2], "Selisih = %d − %s = %d°C." % (b, par(a), b - a), unit="°C")
        if k == 3:
            h, d = ri(2, 9) * 100, ri(1, 6) * 10
            return MN("Seekor burung terbang %d m di atas permukaan laut. Seekor ikan berenang %d m di bawah permukaan laut tepat di bawahnya. Berapa jarak keduanya?" % (h, d),
                      h + d, [h - d, d - h, h + d + 10], "%d − (−%d) = %d m." % (h, d, h + d), unit="m")
        if k == 4:
            f0, up = ri(-3, -1), ri(4, 12)
            return MN("Lift berada di lantai %s (ruang bawah tanah). Lift naik %d lantai. Sekarang lift di lantai …" % (sn(f0), up), f0 + up,
                      [f0 - up, up - f0, f0 + up + 1], "%s + %d = %s." % (sn(f0), up, sn(f0 + up)))
        b, s = ri(8, 20), ri(2, 7)
        w = ri(b // 2 + 1, b) if False else None
        benar, salah = ri(10, 20), ri(3, 10)
        v = 4 * benar - 1 * salah
        return MN("Dalam kuis, jawaban benar diberi skor 4 dan jawaban salah diberi skor −1. Rani menjawab %d benar dan %d salah. Skornya …" % (benar, salah),
                  v, [4 * benar + salah, benar - salah, 4 * (benar - salah)], "4 × %d + (−1) × %d = %d − %d = %d." % (benar, salah, 4 * benar, salah, v))

    sets = [("Garis bilangan dan lawan", [(garis, 12), (lawan, 8)]),
            ("Membandingkan bilangan bulat", [(banding, 20)]),
            ("Mengurutkan bilangan bulat", [(urut, 12), (ekstrem, 8)]),
            ("Bilangan di antara dan jarak", [(antara, 10), (garis, 10)]),
            ("Bilangan bulat dalam kehidupan", [(cerita, 20)])]
    return unit("bilangan-bulat", "B", 1, "Bilangan Bulat: Garis Bilangan, Membandingkan, dan Mengurutkan", "Bilangan Bulat",
                "Peserta didik membaca, menulis, dan membandingkan bilangan bulat, serta menggunakannya untuk menyelesaikan masalah kontekstual.",
                "Latihan bilangan bulat kelas 7 SMP: garis bilangan, lawan bilangan, membandingkan dan mengurutkan bilangan bulat positif dan negatif, suhu, dan kedalaman. 100 soal dengan kunci jawaban.",
                "Makin ke kanan, makin besar", "−8 &lt; −3, karena −8 lebih jauh di kiri 0.", sets,
                ["Bilangan bulat terdiri dari bilangan bulat negatif (…, −3, −2, −1), nol, dan bilangan bulat positif (1, 2, 3, …).",
                 "Pada garis bilangan, bilangan di sebelah kanan selalu lebih besar. Jadi semua bilangan negatif lebih kecil dari 0.",
                 "Bilangan negatif dipakai untuk suhu di bawah nol, kedalaman di bawah permukaan laut, lantai ruang bawah tanah, atau utang."],
                [("Bandingkan −7 dan −2.", ["−7 lebih jauh di kiri 0 daripada −2"], "−7 &lt; −2"),
                 ("Urutkan dari terkecil: 3; −5; 0; −1.", ["Bilangan negatif dulu, yang paling jauh dari 0 paling kecil"], "−5; −1; 0; 3")],
                [["−8 &gt; −3 karena 8 &gt; 3", "−8 &lt; −3, karena −8 ada di kiri −3"],
                 ["Jarak −4 ke 3 dihitung 3 − 4 = −1", "Jarak = 3 − (−4) = 7 satuan"],
                 ["Lawan dari −6 adalah −6", "Lawan dari −6 adalah 6"]],
                [("Apakah 0 termasuk bilangan bulat?", "Ya. Nol adalah bilangan bulat yang bukan positif dan bukan negatif."),
                 ("Mengapa −10 lebih kecil dari −2?", "Karena −10 terletak lebih jauh di sebelah kiri 0 pada garis bilangan. Suhu −10°C juga lebih dingin dari −2°C."),
                 ("Bagaimana menghitung jarak dua bilangan pada garis bilangan?", "Kurangkan bilangan yang lebih kecil dari bilangan yang lebih besar, misalnya jarak −3 ke 5 adalah 5 − (−3) = 8.")])


# ============================================================ 2. operasi bilangan bulat
def u2():
    def tambah():
        a, b = nz(-30, 30), nz(-30, 30)
        if a > 0 and b > 0:
            return None
        v = a + b
        return MN("%s + %s = …" % (sn(a), par(b)), v, [-v, abs(a) + abs(b), a - b, -(abs(a) + abs(b))],
                  "Tanda sama: jumlahkan dan pakai tandanya. Tanda beda: kurangkan dan pakai tanda bilangan yang angkanya lebih besar. Hasilnya %s." % sn(v))

    def kurang():
        a, b = nz(-30, 30), nz(-30, 30)
        v = a - b
        return MN("%s − %s = …" % (sn(a), par(b)), v, [a + b, -v, b - a + 1 if b - a + 1 != v else v + 2, -(a + b)],
                  "Mengurangi sama dengan menambah lawannya: %s + %s = %s." % (sn(a), par(-b), sn(v)))

    def kali():
        a, b = nz(-15, 15), nz(-12, 12)
        if a > 0 and b > 0:
            a = -a
        v = a * b
        return MN("%s × %s = …" % (sn(a), par(b)), v, [-v, a + b, abs(v) + abs(a) if v > 0 else v - a],
                  "Tanda sama hasilnya positif, tanda beda hasilnya negatif. %s × %s = %s." % (sn(a), par(b), sn(v)))

    def bagi():
        b, v = nz(-12, 12), nz(-15, 15)
        a = b * v
        if a > 0 and b > 0:
            return None
        return MN("%s : %s = …" % (sn(a), par(b)), v, [-v, a - b if abs(a - b) < 200 else v + 1, v + 1 if v + 1 else 2],
                  "%s × %s = %s, jadi %s : %s = %s." % (par(b), par(v), sn(a), sn(a), par(b), sn(v)))

    def campur():
        k = ri(0, 3)
        a, b, c = nz(-12, 12), nz(-9, 9), nz(-9, 9)
        if k == 0:
            v = a + b * c
            q = "%s + %s × %s" % (sn(a), par(b), par(c))
            w = (a + b) * c
        elif k == 1:
            v = a - b * c
            q = "%s − %s × %s" % (sn(a), par(b), par(c))
            w = (a - b) * c
        elif k == 2:
            v = (a + b) * c
            q = "(%s + %s) × %s" % (sn(a), par(b), par(c))
            w = a + b * c
        else:
            c = ch([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
            d = nz(-8, 8)
            b = c * d
            v = a - b // c
            q = "%s − %s : %s" % (sn(a), par(b), par(c))
            w = Fr(a - b, c)
            w = int(w) if w.denominator == 1 else v + 3
        return MN("%s = …" % q, v, [w, -v, v + 2, v - 2], "Kerjakan yang di dalam kurung dulu, lalu × dan :, terakhir + dan −. Hasilnya %s." % sn(v))

    def sifat():
        k = ri(0, 2)
        a, b, c = nz(-20, 20), nz(-20, 20), nz(-9, 9)
        if k == 0:
            return M("Sifat apa yang ditunjukkan oleh %s + %s = %s + %s?" % (sn(a), par(b), sn(b), par(a)), "komutatif (pertukaran)",
                     ["asosiatif (pengelompokan)", "distributif (penyebaran)", "identitas"], "Urutan bilangan ditukar dan hasilnya tetap: sifat komutatif.")
        if k == 1:
            return M("Sifat apa yang ditunjukkan oleh %s × (%s + %s) = %s × %s + %s × %s?" % (par(c), sn(a), par(b), par(c), par(a), par(c), par(b)),
                     "distributif (penyebaran)", ["komutatif (pertukaran)", "asosiatif (pengelompokan)", "tertutup"], "Perkalian disebarkan ke setiap suku penjumlahan: sifat distributif.")
        return M("Sifat apa yang ditunjukkan oleh (%s + %s) + %d = %s + (%s + %d)?" % (sn(a), par(b), abs(c), sn(a), par(b), abs(c)), "asosiatif (pengelompokan)",
                 ["komutatif (pertukaran)", "distributif (penyebaran)", "invers"], "Pengelompokan diubah dan hasilnya tetap: sifat asosiatif.")

    def cerita():
        k = ri(0, 5)
        if k == 0:
            s0, a, b = ri(2, 9) * 10000, ri(3, 12) * 10000, ri(1, 5) * 10000
            v = s0 - a + b
            return MN("Saldo tabungan Dimas %s. Ia mengambil %s, lalu menabung %s. Saldonya sekarang …" % (rp(s0), rp(a), rp(b)),
                      v, [s0 + a - b, s0 - a - b, s0 + a + b], "%s − %s + %s = %s." % (num(s0), num(a), num(b), sn(v)), unit="rupiah") if v >= 0 else None
        if k == 1:
            t, n, d = ri(-4, 6), ri(2, 6), ri(2, 4)
            v = t - n * d
            return MN("Suhu %s°C. Setiap jam suhu turun %d°C. Berapa suhu setelah %d jam?" % (sn(t), d, n), v, [t + n * d, t - d, -(t + n * d)],
                      "%s − %d × %d = %s." % (sn(t), n, d, sn(v)), unit="°C")
        if k == 2:
            b, s, k_ = ri(15, 30), ri(3, 10), ri(2, 6)
            v = 4 * b - 2 * s
            return MN("Pada tes, jawaban benar skor 4, salah skor −2, tidak dijawab skor 0. Ani menjawab %d benar, %d salah, dan %d tidak dijawab. Skornya …" % (b, s, k_),
                      v, [4 * b + 2 * s, 4 * b - 2 * s - k_, 4 * (b - s)], "4 × %d + (−2) × %d + 0 = %d − %d = %d." % (b, s, 4 * b, 2 * s, v))
        if k == 3:
            d, n = ri(2, 8) * 5, ri(3, 8)
            d0 = d * n + ri(1, 12) * 5
            v = -d0 + d * n
            return MN("Seorang penyelam berada di kedalaman %s m. Ia naik %d m setiap menit selama %d menit. Posisinya sekarang …" % (sn(-d0), d, n),
                      v, [-d0 - d * n, d0 - d * n, -d0 + d], "%s + %d × %d = %s m." % (sn(-d0), n, d, sn(v)), unit="m")
        if k == 4:
            u, r = ri(3, 9) * 1000, ri(1, 4) * 1000
            n1, n2 = ri(3, 8), ri(2, 6)
            v = n1 * u - n2 * r
            return MN("Seorang pedagang untung %s per hari selama %d hari, lalu rugi %s per hari selama %d hari. Hasil totalnya …" % (rp(u), n1, rp(r), n2),
                      v, [n1 * u + n2 * r, (n1 - n2) * (u - r), n1 * u - r], "%d × %s + %d × (−%s) = %s." % (n1, num(u), n2, num(r), sn(v)), unit="rupiah")
        a, b = ri(-450, -100), ri(100, 600)
        return MN("Kapal selam di kedalaman %s m dan pesawat di ketinggian %d m. Berapa selisih ketinggian keduanya?" % (sn(a), b), b - a,
                  [b + a, a - b, b - a + 100], "%d − (%s) = %d m." % (b, sn(a), b - a), unit="m")

    sets = [("Penjumlahan bilangan bulat", [(tambah, 20)]),
            ("Pengurangan bilangan bulat", [(kurang, 14), (tambah, 6)]),
            ("Perkalian dan pembagian", [(kali, 10), (bagi, 10)]),
            ("Operasi campuran dan sifat", [(campur, 14), (sifat, 6)]),
            ("Soal cerita", [(cerita, 20)])]
    return unit("operasi-bilangan-bulat", "B", 2, "Operasi Hitung Bilangan Bulat", "Operasi Bilangan Bulat",
                "Peserta didik melakukan operasi aritmetika (penjumlahan, pengurangan, perkalian, pembagian) pada bilangan bulat dan menggunakan sifat-sifat operasi.",
                "Latihan operasi hitung bilangan bulat kelas 7 SMP: penjumlahan, pengurangan, perkalian, pembagian bilangan negatif, operasi campuran, sifat operasi, dan soal cerita. 100 soal dengan kunci jawaban.",
                "a − b = a + (lawan b)", "Tanda sama × atau : hasilnya positif, tanda beda negatif.", sets,
                ["Menjumlahkan bilangan bertanda sama: jumlahkan angkanya dan pakai tanda itu. Bertanda beda: kurangkan angkanya dan pakai tanda bilangan yang angkanya lebih besar.",
                 "Mengurangi sama dengan menambah lawannya: 5 − (−3) = 5 + 3 = 8.",
                 "Perkalian dan pembagian: tanda sama hasilnya positif, tanda beda hasilnya negatif. Pada operasi campuran, kerjakan kurung, lalu × dan :, lalu + dan −."],
                [("−8 + 3 = …", ["Tanda beda: 8 − 3 = 5", "Angka yang lebih besar 8, tandanya negatif"], "−5"),
                 ("−4 − (−9) = …", ["= −4 + 9"], "5"),
                 ("(−6) × (−7) = …", ["Tanda sama, hasilnya positif"], "42")],
                [["−7 − 5 = −2", "−7 − 5 = −7 + (−5) = −12"],
                 ["(−3) × (−4) = −12", "Tanda sama hasilnya positif: 12"],
                 ["−2 + 3 × (−4) = 1 × (−4) = −4", "Kalikan dulu: −2 + (−12) = −14"]],
                [("Mengapa negatif dikali negatif hasilnya positif?", "Perkalian dengan −1 membalik arah pada garis bilangan. Membalik dua kali kembali ke arah positif."),
                 ("Apa beda −3² dan (−3)²?", "(−3)² = (−3) × (−3) = 9, sedangkan −3² = −(3 × 3) = −9."),
                 ("Bagaimana urutan operasi campuran?", "Kerjakan yang di dalam kurung dulu, lalu perkalian dan pembagian dari kiri, terakhir penjumlahan dan pengurangan dari kiri.")])


# ============================================================ 3. bilangan rasional
def u3():
    PCS = [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 5), Fr(2, 5), Fr(3, 5), Fr(4, 5), Fr(1, 8), Fr(3, 8), Fr(5, 8), Fr(7, 8), Fr(1, 20), Fr(3, 20), Fr(7, 20),
           Fr(9, 25), Fr(3, 25), Fr(1, 10), Fr(7, 10), Fr(9, 10), Fr(5, 4), Fr(7, 4), Fr(6, 5), Fr(9, 8), Fr(3, 2), Fr(5, 2)]

    def kedes():
        v = ch(PCS) * ch([1, 1, -1])
        w1 = Fr(v.numerator, 10) if abs(v.numerator) < 10 else v / 10
        return M("Bentuk desimal dari %s adalah …" % fq(v), dz(v), [dz(w1) if endl(w1) else None, dz(-v), dz(v + Fr(1, 10)) if endl(v + Fr(1, 10)) else None, dz(v * 10)],
                 "Bagi pembilang dengan penyebut: %s : %d = %s." % (sn(v.numerator), v.denominator, dz(v)))

    def endl(v):
        return S.endlich(v)

    def kepecahan():
        v = ch(PCS) * ch([1, 1, -1])
        h = dz(v)
        k = len(h.split(",")[1]) if "," in h else 0
        raw = abs(int(h.replace(MINUS, "").replace(",", "").replace(".", "")))
        sg = MINUS if v < 0 else ""
        ws = [fq(-v), sg + S.fr(raw, 10 ** k) if Fr(raw, 10 ** k) != abs(v) or raw == abs(v.numerator) else None,
              fq(Fr(v.denominator, v.numerator)) if abs(v.numerator) != 1 else fq(v * 2), fq(v / 2), fq(v + Fr(1, v.denominator) if v > 0 else v - Fr(1, v.denominator))]
        return M("Bentuk pecahan paling sederhana dari %s adalah …" % h, fq(v), ws,
                 "%s = %s%s, lalu sederhanakan menjadi %s." % (h, sg, S.fr(raw, 10 ** k), fq(v)))

    def persen():
        p = ch([5, 10, 12, 15, 20, 25, 30, 35, 40, 45, 60, 65, 75, 80, 120, 125, 150])
        v = Fr(p, 100)
        k = ri(0, 2)
        if k == 0:
            return M("%d%% dalam bentuk pecahan paling sederhana adalah …" % p, fq(v), [fq(Fr(p, 10)), fq(v * 2), fq(Fr(1, p)) if p < 100 else fq(v / 2), fq(1 - v) if v < 1 else fq(v + 1)],
                     "%d%% = %s = %s." % (p, S.fr(p, 100), fq(v)))
        if k == 1:
            return M("%d%% dalam bentuk desimal adalah …" % p, dz(v), [dz(Fr(p, 10)), dz(Fr(p, 1000)), str(p), dz(v + Fr(1, 10))],
                     "%d%% = %d : 100 = %s." % (p, p, dz(v)))
        return M("Bentuk persen dari %s adalah …" % fq(v), "%d%%" % p, ["%s%%" % dz(v), "%d%%" % (p // 10 if p % 10 == 0 else p + 10), "%d%%" % (v.numerator * 10 + v.denominator), "%d%%" % (p * 10)],
                 "%s × 100%% = %d%%." % (fq(v), p))

    def banding():
        while True:
            a = Fr(nz(-9, 9), ri(2, 9))
            b = Fr(nz(-9, 9), ri(2, 9))
            if a != b and a.denominator != 1 and b.denominator != 1 and (a < 0 or b < 0):
                break
        hb = ri(0, 1)
        fa = dz(a) if hb and endl(a) else fq(a)
        fb = dz(b) if hb and endl(b) and not endl(a) else fq(b)
        c = lt(fa, fb) if a < b else gt(fa, fb)
        ws = [gt(fa, fb) if a < b else lt(fa, fb), "%s = %s" % (fa, fb), lt(fb, fa) if a < b else gt(fb, fa)]
        return M("Mana yang benar untuk %s dan %s?" % (fa, fb), c, ws, "Ubah ke desimal: %s ≈ %s dan %s ≈ %s. Jadi %s." % (fa, dz(a, 2), fb, dz(b, 2), c))

    def urut():
        xs = set()
        while len(xs) < 4:
            xs.add(Fr(nz(-12, 12), ch([2, 4, 5, 10])))
        xs = sorted(xs)
        disp = {x: (dz(x) if ri(0, 1) else fq(x)) for x in xs}
        f = lambda l: "; ".join(disp[x] for x in l)
        c = f(xs)
        return M("Urutkan dari yang terkecil: %s" % f(sh(xs)), c, [f(xs[::-1]), f(sorted(xs, key=abs)), f(sorted(xs, key=lambda x: (x < 0, abs(x))))],
                 "Ubah semua ke desimal: %s. Urutannya %s." % ("; ".join(dz(x) for x in xs), c))

    def antara():
        a = Fr(nz(-9, 6), ch([2, 4, 5]))
        b = a + Fr(ri(1, 3), 2)
        mid = (a + b) / 2
        out1, out2 = a - Fr(1, 4), b + Fr(1, 4)
        return M("Bilangan rasional yang terletak di antara %s dan %s adalah …" % (dz(a), dz(b)), dz(mid), [dz(out1), dz(out2), dz(-mid) if -mid < a or -mid > b else dz(b + 1)],
                 "%s ada di antara %s dan %s, misalnya rata-rata keduanya." % (dz(mid), dz(a), dz(b)))

    def jenis():
        k = ri(0, 3)
        if k == 0:
            n = ri(2, 30)
            return M("Bilangan %d termasuk …" % n, "bilangan asli, bulat, dan rasional", ["hanya bilangan asli", "bilangan rasional tetapi bukan bulat", "bukan bilangan rasional"],
                     "%d = %d/1, jadi %d adalah bilangan asli, bulat, dan juga rasional." % (n, n, n))
        if k == 1:
            n = ri(2, 30)
            return M("Bilangan %s termasuk …" % sn(-n), "bilangan bulat dan rasional, tetapi bukan asli", ["bilangan asli", "bukan bilangan bulat", "bukan bilangan rasional"],
                     "Bilangan negatif bukan bilangan asli, tetapi %s = %s/1 adalah bilangan bulat dan rasional." % (sn(-n), sn(-n)))
        v = Fr(nz(-9, 9), ri(2, 9))
        if v.denominator == 1:
            return None
        h = fq(v) if k == 2 else (dz(v) if endl(v) else fq(v))
        return M("Bilangan %s termasuk …" % h, "bilangan rasional tetapi bukan bulat", ["bilangan bulat", "bilangan asli", "bukan bilangan rasional"],
                 "%s dapat ditulis sebagai pecahan a/b, tetapi bukan bilangan bulat." % h)

    sets = [("Pecahan dan desimal", [(kedes, 10), (kepecahan, 10)]),
            ("Persen", [(persen, 20)]),
            ("Membandingkan bilangan rasional", [(banding, 20)]),
            ("Mengurutkan dan di antara", [(urut, 12), (antara, 8)]),
            ("Jenis bilangan", [(jenis, 8), (kedes, 6), (persen, 6)])]
    return unit("bilangan-rasional", "B", 3, "Bilangan Rasional: Pecahan, Desimal, dan Persen", "Bilangan Rasional",
                "Peserta didik membaca, menulis, membandingkan, dan mengurutkan bilangan rasional, serta mengubah bentuk pecahan, desimal, dan persen.",
                "Latihan bilangan rasional kelas 7 SMP: mengubah pecahan ke desimal dan persen, membandingkan dan mengurutkan pecahan dan desimal negatif, serta jenis bilangan. 100 soal dengan kunci jawaban.",
                "Rasional = dapat ditulis a/b", "Ubah ke desimal untuk membandingkan: −3/4 = −0,75.", sets,
                ["Bilangan rasional adalah bilangan yang dapat ditulis sebagai a/b dengan a dan b bulat dan b ≠ 0. Bilangan bulat, pecahan, desimal berakhir, dan persen semuanya rasional.",
                 "Untuk mengubah pecahan ke desimal, bagi pembilang dengan penyebut. Persen berarti per seratus: 35% = 35/100 = 0,35.",
                 "Untuk membandingkan, ubah ke bentuk yang sama (desimal atau penyebut sama). Pada bilangan negatif, yang lebih jauh dari 0 lebih kecil."],
                [("Ubah 3/8 ke desimal.", ["3 : 8 = 0,375"], "0,375"),
                 ("Bandingkan −2/3 dan −3/4.", ["−2/3 ≈ −0,67", "−3/4 = −0,75"], "−3/4 &lt; −2/3")],
                [["−1/2 &lt; −1/3 dianggap salah karena 2 &lt; 3", "−1/2 = −0,5 &lt; −0,33..., jadi −1/2 &lt; −1/3 benar"],
                 ["0,4 = 4/100", "0,4 = 4/10 = 2/5"],
                 ["8% = 0,8", "8% = 8/100 = 0,08"]],
                [("Apakah semua pecahan bilangan rasional?", "Ya, selama pembilang dan penyebutnya bilangan bulat dan penyebutnya bukan 0."),
                 ("Bagaimana mengubah desimal ke pecahan?", "Tulis angkanya di atas 10, 100, atau 1.000 sesuai banyak angka di belakang koma, lalu sederhanakan."),
                 ("Apa itu bilangan rasional negatif?", "Bilangan rasional yang kurang dari 0, misalnya −3/4 atau −2,5.")])


# ============================================================ 4. operasi bilangan rasional
def u4():
    def den():
        return ch([2, 3, 4, 5, 6, 8, 10, 12])

    def tk():
        a = Fr(nz(-9, 9), den())
        b = Fr(nz(-9, 9), den())
        if a.denominator == 1 or b.denominator == 1 or a.denominator == b.denominator:
            return None
        op = ri(0, 1)
        v = a + b if op == 0 else a - b
        q = "%s %s %s = …" % (fq(a), "+" if op == 0 else "−", "(%s)" % fq(b) if b < 0 else fq(b))
        naive = Fr(a.numerator + (b.numerator if op == 0 else -b.numerator), a.denominator + b.denominator)
        return M(q, fq(v), [fq(naive), fq(a - b if op == 0 else a + b), fq(-v)],
                 "Samakan penyebut (KPK %d), lalu %s pembilangnya: hasilnya %s." % ((a.denominator * b.denominator) // __import__("math").gcd(a.denominator, b.denominator), "jumlahkan" if op == 0 else "kurangkan", fq(v)))

    def kb():
        a = Fr(nz(-9, 9), den())
        b = Fr(nz(-9, 9), den())
        if a.denominator == 1 or b.denominator == 1:
            return None
        op = ri(0, 1)
        bb = "(%s)" % fq(b) if b < 0 else fq(b)
        if op == 0:
            v = a * b
            return M("%s × %s = …" % (fq(a), bb), fq(v), [fq(-v), fq(a / b), fq(Fr(a.numerator * b.numerator, a.denominator + b.denominator)) if a.denominator + b.denominator else None, fq(a + b)],
                     "Kalikan pembilang dengan pembilang dan penyebut dengan penyebut: %s." % fq(v))
        v = a / b
        return M("%s : %s = …" % (fq(a), bb), fq(v), [fq(a * b), fq(-v), fq(b / a)], "Membagi = mengalikan dengan kebalikan: %s × %s = %s." % (fq(a), "(%s)" % fq(1 / b) if b < 0 else fq(1 / b), fq(v)))

    def desimal():
        k = ri(0, 2)
        a = Fr(nz(-95, 95), 10)
        b = Fr(nz(-95, 95), 10)
        if k == 0:
            v = a + b
            return MD("%s + %s = …" % (dz(a), pd(b)), v, [a - b, -v, v + 1], "Jumlahkan dengan memperhatikan tanda: %s." % dz(v))
        if k == 1:
            v = a - b
            return MD("%s − %s = …" % (dz(a), pd(b)), v, [a + b, -v, v - 1], "%s + %s = %s." % (dz(a), pd(-b), dz(v)))
        b = Fr(nz(-9, 9), 1) if ri(0, 1) else Fr(nz(-9, 9), 10)
        v = a * b
        return MD("%s × %s = …" % (dz(a), pd(b)), v, [-v, v * 10, v / 10], "Kalikan tanpa koma, lalu hitung angka di belakang koma. Tanda: %s." % ("positif" if v > 0 else "negatif"))

    def campur():
        a = Fr(nz(-5, 5), ch([2, 3, 4]))
        b = Fr(nz(-5, 5), ch([2, 3, 4]))
        c = Fr(nz(-5, 5), ch([2, 3]))
        if a.denominator == 1 or b.denominator == 1:
            return None
        v = a + b * c
        return M("%s + %s × %s = …" % (fq(a), "(%s)" % fq(b) if b < 0 else fq(b), "(%s)" % fq(c) if c < 0 else fq(c)), fq(v), [fq((a + b) * c), fq(a - b * c), fq(-v)],
                 "Kalikan dulu: %s × %s = %s, lalu tambahkan %s. Hasilnya %s." % (fq(b), "(%s)" % fq(c) if c < 0 else fq(c), fq(b * c), fq(a), fq(v)))

    def cerita():
        k = ri(0, 4)
        if k == 0:
            t = Fr(ri(3, 9), 1) + Fr(ri(1, 3), 4)
            p = Fr(ri(1, 3), 4) + ri(0, 1)
            n = ri(2, 4)
            v = t - n * p
            if v <= 0:
                return None
            return M("Pita sepanjang %s m. Dipotong %d kali, setiap potongan %s m. Sisa pita …" % (fq(t, True), n, fq(p, True)), fq(v, True) + " m",
                     [fq(t - p, True) + " m", fq(t + n * p, True) + " m", fq(v + p, True) + " m"], "%s − %d × %s = %s m." % (fq(t, True), n, fq(p, True), fq(v, True)))
        if k == 1:
            h = Fr(ri(-30, -5), 10)
            d = Fr(ri(5, 25), 10)
            v = h + d
            return MD("Suhu malam %s°C, lalu naik %s°C. Suhu sekarang …" % (dz(h), dz(d)), v, [h - d, -v, -h + d], "%s + %s = %s." % (dz(h), dz(d), dz(v)), unit="°C")
        if k == 2:
            n = ri(3, 8)
            p = Fr(ch([1, 3]), 4) + ri(0, 1)
            v = n * p
            return M("Setiap botol berisi %s liter jus. Berapa liter jus dalam %d botol?" % (fq(p, True), n), fq(v, True) + " liter",
                     [fq(n + p, True) + " liter", fq(v + 1, True) + " liter", fq(p / n, True) + " liter"], "%d × %s = %s liter." % (n, fq(p, True), fq(v, True)))
        if k == 3:
            tot = ri(3, 9)
            p = Fr(1, ch([2, 3, 4, 6, 8]))
            v = tot / p
            return MN("Ada %d kg gula. Gula dibungkus masing-masing %s kg. Berapa bungkus yang didapat?" % (tot, fq(p)), v, [tot * p if (tot * p).denominator == 1 else v + 2, v - 1, v + 1],
                      "%d : %s = %d × %d = %s bungkus." % (tot, fq(p), tot, p.denominator, sn(v)), unit="bungkus")
        a = Fr(ri(1, 5), 6)
        b = Fr(ri(1, 3), 4)
        if a + b >= 1:
            return None
        v = 1 - a - b
        return M("Uang saku Rina digunakan %s bagian untuk makan dan %s bagian untuk transportasi. Bagian yang tersisa …" % (fq(a), fq(b)), fq(v),
                 [fq(a + b), fq(Fr(1, 1) - a), fq(Fr(1, 1) - b)], "1 − %s − %s = %s." % (fq(a), fq(b), fq(v)))

    sets = [("Penjumlahan dan pengurangan pecahan", [(tk, 20)]),
            ("Perkalian dan pembagian pecahan", [(kb, 20)]),
            ("Operasi desimal", [(desimal, 20)]),
            ("Operasi campuran", [(campur, 12), (tk, 8)]),
            ("Soal cerita", [(cerita, 20)])]
    return unit("operasi-bilangan-rasional", "B", 4, "Operasi Hitung Bilangan Rasional", "Operasi Bilangan Rasional",
                "Peserta didik melakukan operasi aritmetika pada bilangan rasional (pecahan dan desimal, termasuk bilangan negatif) dan menggunakannya untuk menyelesaikan masalah.",
                "Latihan operasi bilangan rasional kelas 7 SMP: penjumlahan, pengurangan, perkalian, dan pembagian pecahan dan desimal negatif, operasi campuran, dan soal cerita. 100 soal dengan kunci jawaban.",
                "Samakan penyebut dulu", "Membagi pecahan = mengalikan dengan kebalikannya.", sets,
                ["Untuk menjumlahkan atau mengurangkan pecahan, samakan penyebutnya dulu (pakai KPK), lalu jumlahkan atau kurangkan pembilangnya.",
                 "Untuk mengalikan, kalikan pembilang dengan pembilang dan penyebut dengan penyebut. Untuk membagi, kalikan dengan kebalikan pembaginya.",
                 "Aturan tanda sama seperti bilangan bulat: tanda sama hasilnya positif, tanda beda negatif."],
                [("−1/2 + 2/3 = …", ["= −3/6 + 4/6"], "1/6"),
                 ("−3/4 : 1/2 = …", ["= −3/4 × 2/1 = −6/4"], "−3/2")],
                [["1/2 + 1/3 = 2/5", "1/2 + 1/3 = 3/6 + 2/6 = 5/6"],
                 ["2/3 : 4/5 = 8/15", "2/3 × 5/4 = 10/12 = 5/6"],
                 ["−0,5 × (−0,4) = −0,2", "Tanda sama, hasilnya positif: 0,2"]],
                [("Bagaimana menjumlahkan pecahan negatif?", "Samakan penyebutnya, lalu jumlahkan pembilang seperti bilangan bulat. Contoh −1/4 + 3/4 = 2/4 = 1/2."),
                 ("Apa itu kebalikan suatu pecahan?", "Kebalikan dari a/b adalah b/a. Hasil kali suatu bilangan dengan kebalikannya selalu 1."),
                 ("Bagaimana mengalikan desimal?", "Kalikan seperti bilangan bulat, lalu banyak angka di belakang koma hasil = jumlah angka di belakang koma kedua bilangan.")])


# ============================================================ 5. rasio
def u5():
    import math

    def sederhana():
        g = ri(2, 12)
        a, b = ri(1, 9), ri(1, 9)
        if math.gcd(a, b) != 1 or a == b:
            return None
        A, B = a * g, b * g
        k = ri(0, 1)
        if k == 0:
            return M("Bentuk paling sederhana dari rasio %d : %d adalah …" % (A, B), "%d : %d" % (a, b), ["%d : %d" % (b, a), "%d : %d" % (A // math.gcd(A, B) * 2, B // math.gcd(A, B) * 2) if g % 2 == 0 else "%d : %d" % (a + 1, b), "%d : %d" % (A - B if A > B else a, b + 1)],
                     "Bagi kedua bilangan dengan FPB %d: %d : %d." % (g, a, b))
        u1_, u2_ = ch([("cm", "m", 100), ("gram", "kg", 1000), ("menit", "jam", 60)][:3]) if False else (None, None)
        x, (s1, s2, f) = ri(2, 9) * 10, ch([("cm", "m", 100), ("menit", "jam", 60), ("gram", "kg", 1000)])
        y = ri(1, 3)
        A, B = x, y * f
        gg = math.gcd(A, B)
        return M("Rasio %d %s terhadap %d %s adalah …" % (A, s1, y, s2), "%d : %d" % (A // gg, B // gg), ["%d : %d" % (A, y), "%d : %d" % (B // gg, A // gg), "%d : %d" % (A // gg + 1, B // gg)],
                 "Samakan satuan dulu: %d %s = %s %s. Rasio %s : %s = %d : %d." % (y, s2, num(B), s1, num(A), num(B), A // gg, B // gg))

    def bagian():
        a, b = ri(1, 7), ri(1, 7)
        if a == b or math.gcd(a, b) != 1:
            return None
        n = ri(2, 15)
        tot = (a + b) * n
        who = ri(0, 1)
        it = ch(["kelereng", "buku", "kartu", "permen", "manik-manik"])
        p1, p2 = ch([("Adi", "Budi"), ("Rani", "Sinta"), ("Tono", "Dewi"), ("Made", "Putu")])
        v = (a if who == 0 else b) * n
        return MN("Perbandingan %s %s dan %s adalah %d : %d. Jumlah %s mereka %d. Banyak %s %s adalah …" % (it, p1, p2, a, b, it, tot, it, p1 if who == 0 else p2),
                  v, [(b if who == 0 else a) * n, tot // 2 if tot % 2 == 0 and tot // 2 != v else v + n * 2, a * b * n if a * b * n != v else v + n], "Satu bagian = %d : %d = %d. Jadi %d × %d = %d." % (tot, a + b, n, a if who == 0 else b, n, v))

    def satuan():
        k = ri(0, 2)
        if k == 0:
            n = ri(3, 12)
            p = ri(2, 15) * 500
            return MN("Harga %d buku tulis %s. Berapa harga 1 buku tulis?" % (n, rp(n * p)), p, [p + 500, p - 500, n * p // (n - 1) if (n * p) % (n - 1) == 0 and n * p // (n - 1) != p else p * 2], "%s : %d = %s." % (num(n * p), n, rp(p)), unit="rupiah") if True else None
        if k == 1:
            t = ri(2, 5)
            v = ri(4, 16) * 5
            return MN("Sebuah mobil menempuh %d km dalam %d jam. Kecepatan rata-ratanya …" % (v * t, t), v, [v * t * t if False else v + 5, v * t, v - 5], "%d : %d = %d km/jam." % (v * t, t, v), unit="km/jam")
        a, pa, b, pb = ri(2, 5), ri(3, 9) * 1000, ri(6, 10), 0
        pb = ri(3, 9) * 1000
        ua, ub = Fr(pa, a), Fr(pb * b // b, 1)
        n1, n2 = ri(2, 6), ri(7, 12)
        h1, h2 = n1 * ri(20, 45) * 100, n2 * ri(20, 45) * 100
        e1, e2 = Fr(h1, n1), Fr(h2, n2)
        if e1 == e2:
            return None
        c = "Kemasan %d buah" % (n1 if e1 < e2 else n2)
        return M("Kemasan %d buah dijual %s, kemasan %d buah dijual %s. Mana yang lebih murah per buah?" % (n1, rp(h1), n2, rp(h2)), c,
                 ["Kemasan %d buah" % (n2 if e1 < e2 else n1), "Sama murahnya", "Tidak dapat ditentukan"], "Per buah: %s dan %s." % (rp(int(e1)) if e1.denominator == 1 else "≈ " + rp(int(e1)), rp(int(e2)) if e2.denominator == 1 else "≈ " + rp(int(e2))))

    def senilai():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(2, 6), ri(7, 15)
            p = ri(11, 18) * 1000
            return MN("Harga %d kg beras %s. Berapa harga %d kg beras?" % (a, rp(a * p * 1), b), b * p, [a * p + (b - a), b * p + p, (b - a) * p], "Harga 1 kg = %s. %d × %s = %s." % (rp(p), b, num(p), rp(b * p)), unit="rupiah") if False else \
                MN("Harga %d kg beras %s. Berapa harga %d kg beras?" % (a, rp(a * p), b), b * p, [b * p + p, (b - a) * p, a * p + (b - a) * 1000], "Harga 1 kg = %s. %d × %s = %s." % (rp(p), b, num(p), rp(b * p)), unit="rupiah")
        if k == 1:
            a = ri(2, 5)
            km = ri(8, 15) * a
            b = ri(6, 12)
            if b == a:
                return None
            return MN("Sebuah motor menghabiskan %d liter bensin untuk %d km. Berapa km yang ditempuh dengan %d liter?" % (a, km, b), km * b // a if km * b % a == 0 else None,
                      [km + (b - a), km * b, km // a * (b + 1)], "1 liter untuk %d km. %d × %d = %d km." % (km // a, b, km // a, km * b // a), unit="km")
        s = ch([100, 200, 250, 500])
        cm = ri(3, 12)
        v = cm * s * 1000
        return MN("Resep kue untuk %d orang memakai %d gram tepung. Untuk %d orang perlu tepung …" % (4, s, cm), s * cm // 4 if s * cm % 4 == 0 else None,
                  [s * cm, s + cm, s * cm // 2], "Untuk 1 orang %s gram. Untuk %d orang: %s gram." % (dz(Fr(s, 4)), cm, num(s * cm // 4)), unit="gram")

    def balik():
        k = ri(0, 1)
        if k == 0:
            a, d = ri(3, 12), ri(4, 20)
            b = ch([x for x in range(2, 25) if (a * d) % x == 0 and x != a])
            v = a * d // b
            return MN("Pekerjaan dapat diselesaikan %d pekerja dalam %d hari. Jika dikerjakan %d pekerja, pekerjaan selesai dalam …" % (a, d, b), v,
                      [d * b // a if (d * b) % a == 0 and d * b // a != v else v + 2, d + a - b if d + a - b > 0 and d + a - b != v else v + 1, v - 1 if v > 1 else v + 3], "%d × %d = %d hari-pekerja. %d : %d = %d hari." % (a, d, a * d, a * d, b, v), unit="hari")
        v1 = ri(4, 12) * 10
        t1 = ri(2, 6)
        v2 = ch([x for x in range(30, 130, 10) if (v1 * t1) % x == 0 and x != v1])
        t2 = v1 * t1 // v2
        return MN("Dengan kecepatan %d km/jam, perjalanan memakan waktu %d jam. Jika kecepatannya %d km/jam, waktu yang diperlukan …" % (v1, t1, v2), t2,
                  [t1 * v2 // v1 if (t1 * v2) % v1 == 0 and t1 * v2 // v1 != t2 else t2 + 2, t2 + 1, t1 + 1 if t1 + 1 != t2 else t2 + 3], "Jarak %d × %d = %d km. %d : %d = %d jam." % (v1, t1, v1 * t1, v1 * t1, v2, t2), unit="jam")

    def jenis():
        pairs = [("banyak buku dan harga total", "senilai"), ("kecepatan dan waktu tempuh untuk jarak yang sama", "berbalik nilai"),
                 ("banyak pekerja dan waktu menyelesaikan pekerjaan yang sama", "berbalik nilai"), ("jarak tempuh dan bensin yang dipakai", "senilai"),
                 ("banyak anak dan bagian kue yang diterima setiap anak", "berbalik nilai"), ("lama bekerja dan upah harian yang diterima", "senilai"),
                 ("sisi persegi dan kelilingnya", "senilai"), ("banyak keran dan waktu mengisi bak", "berbalik nilai"),
                 ("banyak telur dan berat totalnya", "senilai"), ("banyak ternak dan lama persediaan pakan habis", "berbalik nilai")]
        p, c = ch(pairs)
        return M("Hubungan antara %s termasuk perbandingan …" % p, c, ["berbalik nilai" if c == "senilai" else "senilai", "tidak ada hubungan", "sama dengan selisih"],
                 "%s: jika yang satu bertambah, yang lain %s." % (c.capitalize(), "juga bertambah" if c == "senilai" else "berkurang"))

    sets = [("Menyederhanakan rasio", [(sederhana, 20)]),
            ("Membagi dengan rasio", [(bagian, 20)]),
            ("Laju dan harga satuan", [(satuan, 20)]),
            ("Perbandingan senilai", [(senilai, 14), (jenis, 6)]),
            ("Perbandingan berbalik nilai", [(balik, 16), (jenis, 4)])]
    return unit("rasio-dan-proporsi", "A", 5, "Rasio, Laju, dan Perbandingan", "Rasio dan Proporsi",
                "Peserta didik memahami dan menggunakan rasio, laju perubahan, dan perbandingan senilai serta berbalik nilai untuk menyelesaikan masalah.",
                "Latihan rasio dan proporsi kelas 7 SMP: menyederhanakan rasio, membagi dengan rasio, harga satuan, kecepatan, perbandingan senilai dan berbalik nilai. 100 soal dengan kunci jawaban.",
                "Senilai: dikali. Berbalik: dibagi", "Hitung dulu nilai untuk 1 satuan.", sets,
                ["Rasio membandingkan dua besaran dengan satuan yang sama, misalnya 12 : 18 = 2 : 3. Sederhanakan dengan membagi kedua bilangan dengan FPB.",
                 "Laju adalah rasio dua besaran berbeda, misalnya km per jam atau rupiah per kg. Hitung nilai untuk 1 satuan dulu.",
                 "Perbandingan senilai: jika satu bertambah, yang lain bertambah dengan kelipatan sama. Berbalik nilai: jika satu bertambah, yang lain berkurang, dan hasil kalinya tetap."],
                [("Rasio uang A : B = 3 : 5, jumlah Rp80.000. Uang A?", ["Satu bagian = 80.000 : 8 = 10.000", "A = 3 × 10.000"], "Rp30.000"),
                 ("6 pekerja selesai dalam 10 hari. 4 pekerja selesai dalam?", ["6 × 10 = 60", "60 : 4 = 15"], "15 hari")],
                [["Rasio 50 cm : 2 m = 50 : 2 = 25 : 1", "Samakan satuan: 50 cm : 200 cm = 1 : 4"],
                 ["Berbalik nilai dihitung seperti senilai", "Pada berbalik nilai, hasil kali tetap"],
                 ["Rasio 3 : 5 dari 80 dihitung 80 : 3", "Bagi dengan jumlah bagian: 80 : (3 + 5)"]],
                [("Apa beda rasio dan laju?", "Rasio membandingkan besaran yang satuannya sama. Laju membandingkan besaran yang satuannya berbeda, misalnya km/jam."),
                 ("Bagaimana mengenali perbandingan berbalik nilai?", "Jika satu besaran dikali 2, besaran lain menjadi setengahnya. Hasil kali kedua besaran selalu sama."),
                 ("Apakah urutan rasio penting?", "Ya. Rasio laki-laki : perempuan = 2 : 3 berbeda dengan perempuan : laki-laki = 3 : 2.")])


# ============================================================ 6. bentuk aljabar
def u6():
    V = ["x", "y", "a", "b", "p", "m"]

    def unsur():
        v = ch(V)
        a, b, c = nz(-9, 9), nz(-9, 9), nz(-15, 15)
        e = expr([(a, v + "²"), (b, v), (c, "")])
        k = ri(0, 3)
        if k == 0:
            return MN("Koefisien %s pada bentuk %s adalah …" % (v, e), b, [a, c, -b], "Koefisien %s adalah bilangan di depan %s, termasuk tandanya: %s." % (v, v, sn(b)))
        if k == 1:
            return MN("Konstanta pada bentuk %s adalah …" % e, c, [a, b, -c], "Konstanta adalah suku tanpa variabel: %s." % sn(c))
        if k == 2:
            return MN("Koefisien %s² pada bentuk %s adalah …" % (v, e), a, [b, c, 2 if a != 2 else -a], "Bilangan di depan %s² adalah %s." % (v, sn(a)))
        e2 = expr([(a, v + "²"), (b, v), (c, ""), (nz(-5, 5), ch([w for w in V if w != v]))])
        return MN("Berapa banyak suku pada bentuk %s?" % e2, 4, [3, 2, 5], "Suku-suku dipisahkan oleh + atau −. Ada 4 suku.")

    def sejenis():
        v = ch(V)
        w = ch([x for x in V if x != v])
        a, b, c, d = nz(-9, 9), nz(-9, 9), nz(-9, 9), nz(-9, 9)
        k = ri(0, 1)
        if k == 0:
            q = expr([(a, v), (c, ""), (b, v), (d, "")])
            r = expr([(a + b, v), (c + d, "")])
            ws = [expr([(a + b + c + d, v)]), expr([(a - b, v), (c - d, "")]), expr([(a + b, v), (c - d, "")]), expr([(a + b, v), (-(c + d), "")])]
        else:
            q = expr([(a, v), (c, w), (b, v), (d, w)])
            r = expr([(a + b, v), (c + d, w)])
            ws = [expr([(a + b + c + d, v + w)]), expr([(a - b, v), (c - d, w)]), expr([(a + c, v), (b + d, w)]), expr([(a + b, v), (c - d, w)])]
        return M("Bentuk sederhana dari %s adalah …" % q, r, ws, "Jumlahkan suku-suku sejenis saja: %s." % r)

    def distributif():
        v = ch(V)
        a, b, c = nz(-7, 7), nz(-6, 6), nz(-9, 9)
        q = "%s(%s)" % (sn(a) if a != -1 else MINUS, lin(b, c, v))
        if a == 1:
            return None
        r = lin(a * b, a * c, v)
        return M("Hasil dari %s adalah …" % q, r, [lin(a * b, c, v), lin(a * b, -a * c, v), lin(a + b, a + c, v), lin(-a * b, a * c, v)],
                 "Kalikan %s dengan setiap suku: %s × %s dan %s × %s. Hasilnya %s." % (sn(a), sn(a), "(%s)" % expr([(b, v)]) if b < 0 else expr([(b, v)]), sn(a), par(c), r))

    def gabung():
        v = ch(V)
        a, b, c, d, e = nz(-5, 5), nz(-5, 5), nz(-6, 6), nz(-6, 6), nz(-9, 9)
        if a == 1:
            return None
        q = "%s(%s) %s %s" % (sn(a), lin(b, c, v), "+" if d > 0 else MINUS, expr([(abs(d), v), (e, "")]))
        r = lin(a * b + d, a * c + e, v)
        return M("Bentuk sederhana dari %s adalah …" % q, r, [lin(a * b + d, c + e, v), lin(a * b - d, a * c - e, v), lin(b + d, a * c + e, v)],
                 "Sebarkan dulu: %s, lalu gabungkan suku sejenis: %s." % (lin(a * b, a * c, v), r))

    def subst():
        v = ch(V)
        x = nz(-5, 5)
        a, b, c = nz(-4, 4), nz(-7, 7), nz(-9, 9)
        k = ri(0, 1)
        if k == 0:
            e = lin(a, b, v) if True else ""
            val = a * x + b
            return MN("Nilai %s untuk %s = %s adalah …" % (e, v, sn(x)), val, [a * (-x) + b, a + x + b, a * x - b], "%s × %s %s %d = %s." % (sn(a), par(x), "+" if b > 0 else "−", abs(b), sn(val)))
        e = expr([(a, v + "²"), (b, v), (c, "")])
        val = a * x * x + b * x + c
        return MN("Nilai %s untuk %s = %s adalah …" % (e, v, sn(x)), val, [-a * x * x + b * x + c, a * 2 * x + b * x + c, a * x * x - b * x + c],
                  "%s² = %s, jadi %s × %s + %s × %s + %s = %s." % (par(x), sn(x * x), sn(a), sn(x * x), par(b), par(x), par(c), sn(val)))

    def kalimat():
        n = ri(2, 9)
        m = ri(2, 12)
        ops = [("%d lebihnya dari x" % m, "x + %d" % m, ["%dx" % m, "x − %d" % m, "%d − x" % m]),
               ("%d kurangnya dari x" % m, "x − %d" % m, ["%d − x" % m, "x + %d" % m, "%dx" % m]),
               ("%d kali x ditambah %d" % (n, m), "%dx + %d" % (n, m), ["%d(x + %d)" % (n, m), "%dx + %d" % (m, n), "%dx − %d" % (n, m)]),
               ("%d kali jumlah x dan %d" % (n, m), "%d(x + %d)" % (n, m), ["%dx + %d" % (n, m), "%d + %dx" % (n, m), "%dx + %d" % (m, n)]),
               ("setengah dari x dikurangi %d" % m, "%s − %d" % (S.fr("x", 2), m), ["2x − %d" % m, "%s" % S.fr("x − %d" % m, 2) if False else "x − %s" % S.fr(m, 2), "%d − %s" % (m, S.fr("x", 2))]),
               ("kuadrat dari x ditambah %d" % m, "x² + %d" % m, ["2x + %d" % m, "(x + %d)²" % m, "x + %d²" % m]),
               ("harga %d buku dengan harga x rupiah per buku dan %d pensil dengan harga y rupiah per pensil" % (n, m), "%dx + %dy" % (n, m), ["%dxy" % (n * m), "%dx + %dy" % (m, n), "%d(x + y)" % (n + m)])]
        t, c, ws = ch(ops)
        return M("Bentuk aljabar dari “%s” adalah …" % t, c, ws, "Terjemahkan kata demi kata: %s." % c)

    def bangun():
        v = ch(["x", "a", "p"])
        a, b = ri(1, 4), ri(1, 9)
        c = ri(1, 9)
        k = ri(0, 2)
        if k == 0:
            r = lin(2 * a + 2, 2 * b, v)
            return M("Panjang persegi panjang (%s) cm dan lebarnya %s cm. Kelilingnya …" % (lin(a, b, v), v), r + " cm", [lin(a + 1, b, v) + " cm", lin(2 * a + 2, b, v) + " cm", lin(2 * a, 2 * b, v) + " cm"],
                     "K = 2 × (p + l) = 2 × (%s + %s) = %s cm." % (lin(a, b, v), v, r))
        if k == 1:
            r = lin(4 * a, 4 * b, v)
            return M("Sisi persegi (%s) cm. Kelilingnya …" % lin(a, b, v), r + " cm", [lin(4 * a, b, v) + " cm", lin(a + 4, b, v) + " cm", lin(4 * a, 4 * b + 4, v) + " cm"], "K = 4 × (%s) = %s cm." % (lin(a, b, v), r))
        r = expr([(3 * a, v), (b + c + b, "")])
        return M("Sisi-sisi segitiga (%s) cm, (%s) cm, dan (%s) cm. Kelilingnya …" % (lin(a, b, v), lin(a, c, v), lin(a, b, v)), r + " cm",
                 [expr([(3 * a, v), (b + c, "")]) + " cm", expr([(a, v), (2 * b + c, "")]) + " cm", expr([(3 * a + 2 * b + c, v)]) + " cm"], "Jumlahkan ketiga sisi: %s cm." % r)

    sets = [("Unsur bentuk aljabar", [(unsur, 20)]),
            ("Suku sejenis", [(sejenis, 20)]),
            ("Sifat distributif", [(distributif, 12), (gabung, 8)]),
            ("Substitusi nilai", [(subst, 20)]),
            ("Menulis bentuk aljabar", [(kalimat, 12), (bangun, 8)])]
    return unit("bentuk-aljabar", "A", 6, "Bentuk Aljabar: Suku, Koefisien, dan Penyederhanaan", "Bentuk Aljabar",
                "Peserta didik mengenali unsur bentuk aljabar, menyederhanakan bentuk aljabar dengan suku sejenis dan sifat distributif, serta menghitung nilai bentuk aljabar.",
                "Latihan bentuk aljabar kelas 7 SMP: variabel, koefisien, konstanta, suku sejenis, sifat distributif, substitusi nilai, dan menulis bentuk aljabar dari kalimat. 100 soal dengan kunci jawaban.",
                "Hanya suku sejenis yang dijumlahkan", "3x + 2x = 5x, tetapi 3x + 2 tidak bisa digabung.", sets,
                ["Pada 3x² − 5x + 7: x adalah variabel, 3 dan −5 adalah koefisien, 7 adalah konstanta. Setiap bagian yang dipisahkan + atau − disebut suku.",
                 "Suku sejenis memiliki variabel dan pangkat yang sama, misalnya 4x dan −x. Hanya suku sejenis yang dapat dijumlahkan atau dikurangkan.",
                 "Sifat distributif: a(b + c) = ab + ac. Untuk menghitung nilai bentuk aljabar, ganti variabel dengan bilangannya (substitusi)."],
                [("Sederhanakan 5x + 3 − 2x + 4.", ["5x − 2x = 3x", "3 + 4 = 7"], "3x + 7"),
                 ("Hasil −3(2x − 5) = …", ["−3 × 2x = −6x", "−3 × (−5) = 15"], "−6x + 15")],
                [["3x + 4 = 7x", "3x dan 4 bukan suku sejenis, jadi tetap 3x + 4"],
                 ["−2(x − 3) = −2x − 6", "−2 × (−3) = 6, jadi −2x + 6"],
                 ["Koefisien x pada 5 − 4x adalah 4", "Koefisiennya −4 (tanda ikut)"]],
                [("Apa itu variabel?", "Variabel adalah lambang (biasanya huruf) untuk bilangan yang belum diketahui atau dapat berubah, misalnya x atau n."),
                 ("Apakah 3x dan 3x² suku sejenis?", "Bukan. Pangkat x-nya berbeda, jadi tidak dapat dijumlahkan."),
                 ("Mengapa koefisien x pada −x adalah −1?", "Karena −x sama dengan −1 × x. Angka 1 biasanya tidak ditulis.")])


# ============================================================ 7. persamaan linear satu variabel
def u7():
    V = ["x", "y", "n", "a", "p"]

    def satu():
        v = ch(V)
        x = nz(-12, 12)
        k = ri(0, 2)
        if k == 0:
            b = nz(-20, 20)
            c = x + b
            return MN("Penyelesaian dari %s = %s adalah %s = …" % (lin(1, b, v), sn(c), v), x, [c + b, -x, b - c], "Kedua ruas %s %d: %s = %s." % ("dikurangi" if b > 0 else "ditambah", abs(b), v, sn(x)))
        if k == 1:
            a = nz(-9, 9)
            if a in (1, -1):
                return None
            return MN("Penyelesaian dari %s = %s adalah %s = …" % (expr([(a, v)]), sn(a * x), v), x, [a * x - a, -x, a * x * a if abs(a * a * x) < 200 else x + 1],
                      "Kedua ruas dibagi %s: %s = %s." % (par(a), v, sn(x)))
        a = ri(2, 6)
        return MN("Penyelesaian dari %s = %s adalah %s = …" % (S.fr(v, a), sn(x), v), a * x, [x + a, Fr(x, a) if Fr(x, a).denominator == 1 else x - a, -a * x], "Kedua ruas dikali %d: %s = %s." % (a, v, sn(a * x)))

    def dua():
        v = ch(V)
        x = nz(-10, 10)
        a, b = nz(-9, 9), nz(-20, 20)
        if a in (1, -1, 0):
            return None
        c = a * x + b
        return MN("Penyelesaian dari %s = %s adalah %s = …" % (lin(a, b, v), sn(c), v), x,
                  [Fr(c + b, a) if Fr(c + b, a).denominator == 1 else None, -x, Fr(c, a) - b if Fr(c, a).denominator == 1 else None, x + 1, x - 1],
                  "%s = %s %s %d = %s, lalu %s = %s : %s = %s." % (expr([(a, v)]), sn(c), "−" if b > 0 else "+", abs(b), sn(c - b), v, sn(c - b), par(a), sn(x)))

    def kedua():
        v = ch(V)
        x = nz(-9, 9)
        a, c = nz(-8, 8), nz(-8, 8)
        if a == c:
            return None
        b = nz(-15, 15)
        d = (a - c) * x + b
        return MN("Penyelesaian dari %s = %s adalah %s = …" % (lin(a, b, v), lin(c, d, v), v), x,
                  [Fr(d - b, a + c) if a + c and Fr(d - b, a + c).denominator == 1 else None, -x, Fr(d + b, a - c) if Fr(d + b, a - c).denominator == 1 else None, x + 2, x - 2],
                  ("Kumpulkan %s di kiri: %s = %s, jadi %s = %s." % (v, expr([(a - c, v)]), sn(d - b), v, sn(x)) if a - c != 1 else "Kumpulkan %s di kiri: %s = %s." % (v, v, sn(x))))

    def kurung():
        v = ch(V)
        x = nz(-8, 8)
        a, b = ch([2, 3, 4, 5, -2, -3]), nz(-9, 9)
        c = a * (x + b)
        return MN("Penyelesaian dari %s(%s) = %s adalah %s = …" % (sn(a), lin(1, b, v), sn(c), v), x,
                  [Fr(c, a) + b if Fr(c, a).denominator == 1 else None, Fr(c - b, a) if Fr(c - b, a).denominator == 1 else None, -x, x + 1],
                  "Bagi kedua ruas dengan %s: %s = %s, lalu %s = %s." % (par(a), lin(1, b, v), sn(Fr(c, a)), v, sn(x)))

    def cek():
        v = "x"
        x = nz(-8, 8)
        a, b = nz(-6, 6), nz(-12, 12)
        if a in (0, 1, -1):
            return None
        c = a * x + b
        return MN("Manakah yang merupakan penyelesaian dari %s = %s?" % (lin(a, b), sn(c)), x, [x + 1, -x, x - 2, x + 3], "Substitusi x = %s: %s × %s %s %d = %s. Benar." % (sn(x), sn(a), par(x), "+" if b > 0 else "−", abs(b), sn(c)))

    def cerita():
        k = ri(0, 5)
        if k == 0:
            x = ri(5, 40)
            d = ri(2, 15)
            return MN("Jumlah dua bilangan adalah %d. Bilangan yang satu %d lebihnya dari yang lain. Bilangan yang lebih kecil adalah …" % (2 * x + d, d), x,
                      [x + d, (2 * x + d) // 2, x - d if x - d > 0 else x + 1], "x + (x + %d) = %d, 2x = %d, x = %d." % (d, 2 * x + d, 2 * x, x))
        if k == 1:
            l = ri(4, 20)
            d = ri(2, 10)
            K = 2 * (2 * l + d)
            return MN("Keliling persegi panjang %d cm. Panjangnya %d cm lebih dari lebarnya. Lebarnya …" % (K, d), l, [l + d, K // 4, K // 2 - d], "2(l + %d + l) = %d → 4l + %d = %d → l = %d cm." % (d, K, 2 * d, K, l), unit="cm")
        if k == 2:
            a = ri(8, 15)
            t = ri(2, 5)
            n = ri(3, 12)
            return MN("Umur ayah %d kali umur Dito. Jumlah umur mereka %d tahun. Umur Dito …" % (t, (t + 1) * a), a, [t * a, (t + 1) * a // 2 if ((t + 1) * a) % 2 == 0 else a + 1, a + t], "x + %dx = %d, %dx = %d, x = %d tahun." % (t, (t + 1) * a, t + 1, (t + 1) * a, a), unit="tahun")
        if k == 3:
            p = ri(3, 9) * 1000
            n = ri(2, 6)
            s = ri(1, 5) * 1000
            tot = n * p + s
            return MN("Sinta membeli %d buku dan membayar ongkos kirim %s. Total %s. Harga satu buku …" % (n, rp(s), rp(tot)), p, [tot // n if tot % n == 0 and tot // n != p else p + 1000, (tot + s) // n if (tot + s) % n == 0 else p - 500, tot - s], "%dx + %s = %s → %dx = %s → x = %s." % (n, num(s), num(tot), n, num(n * p), num(p)), unit="rupiah")
        if k == 4:
            x = ri(10, 40)
            return MN("Tiga bilangan bulat berurutan jumlahnya %d. Bilangan terkecil adalah …" % (3 * x + 3), x, [x + 1, x + 2, x - 1], "n + (n + 1) + (n + 2) = %d → 3n + 3 = %d → n = %d." % (3 * x + 3, 3 * x + 3, x))
        a = ri(20, 60)
        b = ri(5, 15)
        n = ri(2, 8)
        return MN("Tabungan Andi Rp%s dan bertambah Rp%s setiap minggu. Setelah berapa minggu tabungannya menjadi Rp%s?" % (num(a * 1000), num(b * 1000), num((a + n * b) * 1000)), n,
                  [n + 1, (a + n * b) // b, n * 2], "%s + %sx = %s → x = %d minggu." % (num(a * 1000), num(b * 1000), num((a + n * b) * 1000), n), unit="minggu")

    sets = [("Persamaan satu langkah", [(satu, 20)]),
            ("Persamaan dua langkah", [(dua, 14), (cek, 6)]),
            ("Variabel di kedua ruas", [(kedua, 20)]),
            ("Persamaan dengan kurung", [(kurung, 14), (dua, 6)]),
            ("Soal cerita", [(cerita, 20)])]
    return unit("persamaan-linear-satu-variabel", "A", 7, "Persamaan Linear Satu Variabel", "Persamaan Linear Satu Variabel",
                "Peserta didik menyelesaikan persamaan linear satu variabel dan menggunakannya untuk menyelesaikan masalah kontekstual.",
                "Latihan persamaan linear satu variabel (PLSV) kelas 7 SMP: persamaan satu dan dua langkah, variabel di kedua ruas, persamaan dengan kurung, dan soal cerita. 100 soal dengan kunci jawaban.",
                "Lakukan hal yang sama di kedua ruas", "Persamaan tetap seimbang seperti timbangan.", sets,
                ["Persamaan seperti timbangan yang seimbang. Jika kita menambah, mengurangi, mengalikan, atau membagi kedua ruas dengan bilangan yang sama (bukan 0), persamaan tetap benar.",
                 "Langkah umum: buka kurung, kumpulkan suku bervariabel di satu ruas dan konstanta di ruas lain, lalu bagi dengan koefisien variabel.",
                 "Periksa jawaban dengan mensubstitusikannya ke persamaan awal."],
                [("3x − 7 = 11", ["3x = 11 + 7 = 18", "x = 18 : 3"], "x = 6"),
                 ("5x + 2 = 2x − 10", ["5x − 2x = −10 − 2", "3x = −12"], "x = −4")],
                [["x + 5 = 12 → x = 12 + 5", "Kurangi kedua ruas dengan 5: x = 7"],
                 ["−2x = 8 → x = 4", "Bagi dengan −2: x = −4"],
                 ["3(x + 2) = 15 → 3x + 2 = 15", "3(x + 2) = 3x + 6"]],
                [("Apa itu persamaan linear satu variabel?", "Persamaan dengan satu variabel berpangkat satu, misalnya 2x + 5 = 13."),
                 ("Mengapa pindah ruas tandanya berubah?", "Karena sebenarnya kita mengurangi atau menambah kedua ruas dengan bilangan yang sama."),
                 ("Bagaimana memeriksa jawaban?", "Ganti variabel dengan jawabanmu. Jika ruas kiri sama dengan ruas kanan, jawabannya benar.")])


# ============================================================ 8. pertidaksamaan
def u8():
    SG = {"<": "&lt;", ">": "&gt;", "≤": "≤", "≥": "≥"}
    FLIP = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}

    def sol_txt(s, v, x):
        return "%s %s %s" % (v, SG[s], sn(x))

    def langkah():
        v = ch(["x", "y", "n", "p"])
        x = nz(-10, 10)
        s = ch(list(SG))
        k = ri(0, 2)
        if k == 0:
            b = nz(-15, 15)
            q = "%s %s %s" % (lin(1, b, v), SG[s], sn(x + b))
            c = sol_txt(s, v, x)
            ws = [sol_txt(FLIP[s], v, x), sol_txt(s, v, x + 2 * b), sol_txt(s, v, -x)]
            e = ("Kurangi kedua ruas dengan %d: %s." % (b, c)) if b > 0 else ("Tambahkan %d ke kedua ruas: %s." % (-b, c))
        elif k == 1:
            a = ch([2, 3, 4, 5, 6])
            b = nz(-12, 12)
            q = "%s %s %s" % (lin(a, b, v), SG[s], sn(a * x + b))
            c = sol_txt(s, v, x)
            ws = [sol_txt(FLIP[s], v, x), sol_txt(s, v, Fr(a * x + 2 * b, a)) if Fr(a * x + 2 * b, a).denominator == 1 else sol_txt(s, v, x + 1), sol_txt(s, v, a * x)]
            e = "%s %s %s, lalu bagi dengan %d: %s." % (expr([(a, v)]), SG[s], sn(a * x), a, c)
        else:
            a = ch([-2, -3, -4, -5])
            b = nz(-12, 12)
            q = "%s %s %s" % (lin(a, b, v), SG[s], sn(a * x + b))
            c = sol_txt(FLIP[s], v, x)
            ws = [sol_txt(s, v, x), sol_txt(FLIP[s], v, -x), sol_txt(s, v, -x)]
            e = "%s %s %s. Dibagi bilangan negatif %s, tanda dibalik: %s." % (expr([(a, v)]), SG[s], sn(a * x), sn(a), c)
        return M("Penyelesaian dari %s adalah …" % q, c, ws, e)

    def kedua():
        v = "x"
        x = nz(-8, 8)
        a, c = nz(-7, 7), nz(-7, 7)
        if a == c:
            return None
        b = nz(-12, 12)
        d = (a - c) * x + b
        s = ch(list(SG))
        q = "%s %s %s" % (lin(a, b), SG[s], lin(c, d))
        r = s if a - c > 0 else FLIP[s]
        c_ = sol_txt(r, v, x)
        return M("Penyelesaian dari %s adalah …" % q, c_, [sol_txt(FLIP[r], v, x), sol_txt(r, v, -x), sol_txt(FLIP[r], v, -x)],
                 ("%s %s %s%s: %s." % (expr([(a - c, v)]), SG[s], sn(d - b), ", dibagi bilangan negatif sehingga tanda dibalik" if a - c < 0 else "", c_) if a - c != 1 else "Kumpulkan x di kiri: %s." % c_))

    def anggota():
        x = nz(-6, 8)
        s = ch(list(SG))
        a, b = ch([2, 3, -2, -3]), nz(-9, 9)
        q = "%s %s %s" % (lin(a, b), SG[s], sn(a * x + b))
        r = s if a > 0 else FLIP[s]
        good = [n for n in range(x - 4, x + 5) if {"<": n < x, ">": n > x, "≤": n <= x, "≥": n >= x}[r]]
        bad = [n for n in range(x - 4, x + 5) if n not in good]
        g = ch(good)
        return MN("Manakah yang merupakan anggota himpunan penyelesaian %s?" % q, g, sh(bad)[:3], "Penyelesaiannya %s, dan %s memenuhi." % (sol_txt(r, "x", x), sn(g)))

    def garis():
        x = nz(-4, 4)
        s = ch(list(SG))
        W = 420
        X = lambda v: 40 + (v + 6) * 28
        s_ = [line(20, 50, W - 10, 50, INK, 2)]
        for i in range(-6, 7):
            s_.append(line(X(i), 44, X(i), 56, INK, 1.4) + text(X(i), 78, num(i), 13, weight=400))
        right = s in (">", "≥")
        end = X(6.6) if right else X(-6.6)
        s_.append(line(X(x), 50, end, 50, RED, 5))
        s_.append("<circle cx='%.1f' cy='50' r='7' fill='%s' stroke='%s' stroke-width='3'/>" % (X(x), RED if s in ("≤", "≥") else "#fff", RED))
        pic = wrap(W, 92, "".join(s_), "garis bilangan himpunan penyelesaian")
        c = sol_txt(s, "x", x)
        others = [sol_txt(t, "x", x) for t in SG if t != s]
        return M("Garis bilangan berikut menunjukkan penyelesaian …" + pic, c, others, "Arah ke %s berarti %s; titik %s berarti %s termasuk." % ("kanan" if right else "kiri", "lebih besar" if right else "lebih kecil", "penuh" if s in ("≤", "≥") else "kosong", sn(x) if s in ("≤", "≥") else "tidak"))

    def kalimat():
        ks = [("paling sedikit", "≥"), ("tidak kurang dari", "≥"), ("paling banyak", "≤"), ("tidak lebih dari", "≤"), ("lebih dari", ">"), ("kurang dari", "<")]
        t, s = ch(ks)
        w, v = ch([("Banyak peserta lomba (x) %s %s orang.", ri(10, 60)), ("Berat muatan truk (x) %s %s kg.", ri(4, 40) * 250),
                   ("Nilai ujian (x) %s %s.", ri(12, 16) * 5), ("Umur penonton film (x) %s %s tahun.", ri(10, 21)),
                   ("Kecepatan kendaraan (x) %s %s km/jam.", ri(4, 12) * 10), ("Tinggi badan pengunjung wahana (x) %s %s cm.", ri(10, 16) * 10)])
        what = w % (t, num(v))
        c = "x %s %s" % (SG[s], num(v))
        return M("Kalimat \u201c%s\u201d ditulis …" % what, c, ["x %s %s" % (SG[t2], num(v)) for t2 in SG if t2 != s], "\u201c%s\u201d berarti %s." % (t.capitalize(), c))

    def cerita():
        k = ri(0, 3)
        if k == 0:
            m = ri(5, 9) * 100
            p = ri(40, 80)
            b = ri(55, 75)
            n = (m - b) // p
            return MN("Lift dapat mengangkut paling banyak %d kg. Petugas lift beratnya %d kg dan setiap kotak beratnya %d kg. Paling banyak berapa kotak yang dapat diangkut bersama petugas?" % (m, b, p),
                      n, [n + 1, m // p, n - 1], "%d + %dx ≤ %d → x ≤ %s. Jadi paling banyak %d kotak." % (b, p, m, dz(Fr(m - b, p), 1) if (m - b) % p else num((m - b) // p), n), unit="kotak")
        if k == 1:
            u = ri(5, 15) * 10000
            p = ri(3, 9) * 1000
            t = ri(1, 4) * 5000
            n = (u - t) // p
            return MN("Dina punya %s. Ia membayar tiket %s, lalu ingin membeli buku seharga %s per buku. Paling banyak berapa buku yang dapat dibeli?" % (rp(u), rp(t), rp(p)),
                      n, [n + 1, u // p, n - 1], "%s + %sx ≤ %s → x ≤ %s. Paling banyak %d buku." % (num(t), num(p), num(u), dz(Fr(u - t, p), 1) if (u - t) % p else num(n), n), unit="buku")
        if k == 2:
            a, b = ri(60, 80), ri(60, 85)
            t = ri(70, 80)
            need = 3 * t - a - b
            if need > 100 or need < 40:
                return None
            return MN("Nilai dua ulangan Raka %d dan %d. Agar rata-rata tiga ulangan paling sedikit %d, nilai ulangan ketiga paling sedikit …" % (a, b, t),
                      need, [need - 1, t, need + 3], "(%d + %d + x) : 3 ≥ %d → x ≥ %d." % (a, b, t, need))
        l = ri(3, 10)
        K = ri(30, 60)
        n = (K - 2 * l) // 2
        return MN("Keliling persegi panjang tidak lebih dari %d cm dan lebarnya %d cm. Panjang terbesar yang mungkin (bilangan bulat) adalah …" % (K, l),
                  n, [n + 1, K - 2 * l, K // 2], "2(p + %d) ≤ %d → p ≤ %s." % (l, K, dz(Fr(K - 2 * l, 2))), unit="cm")

    sets = [("Pertidaksamaan sederhana", [(langkah, 20)]),
            ("Variabel di kedua ruas", [(kedua, 14), (anggota, 6)]),
            ("Garis bilangan", [(garis, 12), (anggota, 8)]),
            ("Menulis pertidaksamaan", [(kalimat, 20)]),
            ("Soal cerita", [(cerita, 20)])]
    return unit("pertidaksamaan-linear-satu-variabel", "A", 8, "Pertidaksamaan Linear Satu Variabel", "Pertidaksamaan Linear Satu Variabel",
                "Peserta didik menyelesaikan pertidaksamaan linear satu variabel, menyajikan penyelesaiannya pada garis bilangan, dan menggunakannya untuk menyelesaikan masalah.",
                "Latihan pertidaksamaan linear satu variabel (PtLSV) kelas 7 SMP: menyelesaikan pertidaksamaan, membalik tanda, garis bilangan, menulis pertidaksamaan dari kalimat, dan soal cerita. 100 soal dengan kunci jawaban.",
                "Dikali atau dibagi negatif? Balik!", "−2x < 6 menjadi x > −3.", sets,
                ["Pertidaksamaan memakai tanda &lt;, &gt;, ≤, atau ≥. Cara menyelesaikannya mirip persamaan: lakukan hal yang sama di kedua ruas.",
                 "Aturan penting: jika kedua ruas dikali atau dibagi bilangan negatif, tanda pertidaksamaan harus dibalik.",
                 "Pada garis bilangan, titik penuh berarti bilangan itu termasuk (≤, ≥), titik kosong berarti tidak termasuk (&lt;, &gt;)."],
                [("2x + 3 &lt; 11", ["2x &lt; 8", "x &lt; 4"], "x &lt; 4"),
                 ("−3x ≥ 12", ["Bagi dengan −3, tanda dibalik"], "x ≤ −4")],
                [["−2x &gt; 8 → x &gt; −4", "Dibagi −2, tanda dibalik: x &lt; −4"],
                 ["“Paling sedikit 10” ditulis x ≤ 10", "Paling sedikit 10 berarti x ≥ 10"],
                 ["Titik penuh dipakai untuk x &gt; 2", "x &gt; 2 memakai titik kosong"]],
                [("Mengapa tanda dibalik jika dibagi bilangan negatif?", "Karena 2 &lt; 5, tetapi −2 &gt; −5. Mengalikan dengan bilangan negatif membalik urutan bilangan."),
                 ("Apa arti tanda ≤?", "Kurang dari atau sama dengan. Bilangan batasnya ikut menjadi penyelesaian."),
                 ("Apakah penyelesaian pertidaksamaan hanya satu bilangan?", "Tidak. Biasanya ada banyak bilangan yang memenuhi, misalnya semua bilangan yang kurang dari 4.")])


# ============================================================ 9. aritmetika sosial
def u9():
    def untung():
        b = ri(4, 40) * 5000
        p = ch([5, 10, 12, 15, 20, 25, 30, 40])
        up = ri(0, 1)
        d = b * p // 100
        j = b + d if up else b - d
        k = ri(0, 2)
        if k == 0:
            return M("Pedagang membeli barang %s dan menjualnya %s. Ia mendapat …" % (rp(b), rp(j)), "%s %s" % ("untung" if up else "rugi", rp(d)),
                     ["%s %s" % ("rugi" if up else "untung", rp(d)), "%s %s" % ("untung" if up else "rugi", rp(j)), "%s %s" % ("untung" if up else "rugi", rp(d * 2))],
                     "Selisih %s − %s = %s. Harga jual %s harga beli, jadi %s." % (rp(max(b, j)), rp(min(b, j)), rp(d), "lebih dari" if up else "kurang dari", "untung" if up else "rugi"))
        if k == 1:
            return M("Barang dibeli %s dan dijual %s. Persentase %s …" % (rp(b), rp(j), "untungnya" if up else "ruginya"), "%d%%" % p,
                     ["%s%%" % dz(Fr(d * 100, j), 1) if d * 100 % j else "%d%%" % (d * 100 // j), "%d%%" % (p + 5), "%d%%" % (p * 2)],
                     "%s = %s : %s × 100%% = %d%% (dibandingkan dengan harga beli)." % ("Untung" if up else "Rugi", rp(d), rp(b), p))
        return M("Harga beli %s. Agar untung %d%%, harga jualnya …" % (rp(b), p) if up else "Harga beli %s dan dijual rugi %d%%. Harga jualnya …" % (rp(b), p),
                 rp(j), [rp(b - d if up else b + d), rp(d), rp(b + 2 * d if up else b - 2 * d)], "%s %d%% = %s. Harga jual = %s %s %s = %s." % ("Untung" if up else "Rugi", p, rp(d), rp(b), "+" if up else "−", rp(d), rp(j)))

    def diskon():
        h = ri(4, 40) * 10000
        p = ch([10, 15, 20, 25, 30, 40, 50])
        d = h * p // 100
        k = ri(0, 2)
        if k == 0:
            return M("Sepatu seharga %s mendapat diskon %d%%. Harga yang dibayar …" % (rp(h), p), rp(h - d), [rp(d), rp(h - p * 1000), rp(h + d)], "Diskon = %d%% × %s = %s. Dibayar %s − %s = %s." % (p, rp(h), rp(d), rp(h), rp(d), rp(h - d)))
        if k == 1:
            return M("Harga tas %s, setelah diskon menjadi %s. Besar diskonnya …" % (rp(h), rp(h - d)), "%d%%" % p, ["%d%%" % (100 - p), "%d%%" % (p + 5), "%d%%" % (p // 2 if p % 2 == 0 else p + 10)],
                     "Potongan %s. %s : %s × 100%% = %d%%." % (rp(d), rp(d), rp(h), p))
        q = ch([10, 20])
        if p + q > 70:
            return None
        h2 = (h - d) * (100 - q) // 100
        if (h - d) * (100 - q) % 100:
            return None
        return M("Harga baju %s didiskon %d%%, lalu didiskon lagi %d%% dari harga setelah diskon pertama. Harga akhirnya …" % (rp(h), p, q), rp(h2),
                 [rp(h * (100 - p - q) // 100), rp(h - d), rp(h2 - 5000)], "%s − %d%% = %s, lalu %s − %d%% = %s." % (rp(h), p, rp(h - d), rp(h - d), q, rp(h2)))

    def bunga():
        m = ri(2, 20) * 500000
        p = ch([4, 5, 6, 8, 10, 12])
        k = ri(0, 2)
        if k == 0:
            t = ri(1, 3)
            b = m * p * t // 100
            return M("Tabungan %s di bank dengan bunga tunggal %d%% per tahun. Besar bunga setelah %d tahun …" % (rp(m), p, t), rp(b),
                     [rp(m * p // 100) if t > 1 else rp(m * p // 1000), rp(m + b), rp(b * 2)], "Bunga = %s × %d%% × %d = %s." % (rp(m), p, t, rp(b)))
        if k == 1:
            n = ch([3, 4, 6, 8, 9])
            b = m * p * n // 1200
            if m * p * n % 1200:
                return None
            return M("Tabungan %s dengan bunga %d%% per tahun. Jumlah tabungan setelah %d bulan …" % (rp(m), p, n), rp(m + b),
                     [rp(m + m * p // 100), rp(b), rp(m + m * p * n // 100)], "Bunga %d bulan = %d/12 × %d%% × %s = %s. Total %s." % (n, n, p, rp(m), rp(b), rp(m + b)))
        n = ri(2, 6) * 6
        b = m * p * n // 1200
        if m * p * n % 1200:
            return None
        return M("Modal %s ditabung dan setelah %d bulan bunganya %s. Persentase bunga per tahun …" % (rp(m), n, rp(b)), "%d%%" % p,
                 ["%s%%" % dz(Fr(b * 100, m), 1) if (b * 100) % m else "%d%%" % (b * 100 // m), "%d%%" % (p + 2), "%d%%" % (p * 2)], "%s : %s × 12/%d × 100%% = %d%%." % (rp(b), rp(m), n, p))

    def pajak():
        k = ri(0, 2)
        if k == 0:
            h = ri(2, 30) * 10000
            p = ch([10, 11, 12])
            return M("Harga barang %s belum termasuk pajak %d%%. Harga setelah pajak …" % (rp(h), p), rp(h + h * p // 100),
                     [rp(h * p // 100), rp(h - h * p // 100), rp(h + p * 1000)], "Pajak %d%% × %s = %s. Total %s." % (p, rp(h), rp(h * p // 100), rp(h + h * p // 100)))
        if k == 1:
            g = ri(3, 12) * 1000000
            p = 5
            return M("Gaji Pak Budi %s per bulan dan dipotong pajak %d%%. Gaji yang diterima …" % (rp(g), p), rp(g - g * p // 100),
                     [rp(g * p // 100), rp(g + g * p // 100), rp(g - 50000)], "Pajak = %s. Diterima %s − %s = %s." % (rp(g * p // 100), rp(g), rp(g * p // 100), rp(g - g * p // 100)))
        t = ri(2, 8) * 100 if False else ri(4, 20) * 5
        n = ri(2, 12) * 5
        b = n * 100 + t * 10
        bruto, tara = ri(40, 120), ri(1, 5)
        return MN("Berat sebuah karung beras (bruto) %d kg dan beratnya karung (tara) %d kg. Berat bersih (neto) beras …" % (bruto, tara), bruto - tara,
                  [bruto + tara, bruto, tara * 10], "Neto = bruto − tara = %d − %d = %d kg." % (bruto, tara, bruto - tara), unit="kg")

    def tara():
        n = ri(2, 10)
        br = ri(20, 60)
        p = ch([1, 2, 3, 4, 5])
        tr = br * p // 100 if br * p % 100 == 0 else None
        if tr is None:
            br = 50 * ri(1, 4)
            tr = br * p // 100
        return MN("Bruto %d karung gula masing-masing %d kg dengan tara %d%%. Neto seluruhnya …" % (n, br, p), n * (br - tr),
                  [n * br, n * tr, n * (br + tr)], "Tara 1 karung = %d%% × %d = %s kg. Neto = %d × (%d − %s) = %s kg." % (p, br, num(tr), n, br, num(tr), num(n * (br - tr))), unit="kg")

    sets = [("Untung dan rugi", [(untung, 20)]),
            ("Diskon", [(diskon, 20)]),
            ("Bunga tunggal", [(bunga, 20)]),
            ("Pajak, bruto, tara, dan neto", [(pajak, 12), (tara, 8)]),
            ("Campuran", [(untung, 7), (diskon, 7), (bunga, 6)])]
    return unit("aritmetika-sosial", "B", 9, "Aritmetika Sosial: Untung, Rugi, Diskon, Bunga, dan Pajak", "Aritmetika Sosial",
                "Peserta didik menggunakan persentase untuk menyelesaikan masalah keuangan sehari-hari: untung, rugi, diskon, bunga tunggal, pajak, serta bruto, tara, dan neto (literasi finansial).",
                "Latihan aritmetika sosial kelas 7 SMP: untung dan rugi, persentase untung, diskon, bunga tunggal tabungan, pajak, bruto, tara, dan neto. 100 soal dengan kunci jawaban.",
                "Persentase dari harga awal", "Untung, rugi, dan diskon dihitung dari harga awal.", sets,
                ["Untung jika harga jual lebih dari harga beli, rugi jika kurang. Persentase untung atau rugi = besar untung atau rugi : harga beli × 100%.",
                 "Diskon adalah potongan harga. Harga bayar = harga awal − diskon. Pajak menambah harga: harga setelah pajak = harga + pajak.",
                 "Bunga tunggal = modal × persen bunga per tahun × lama (dalam tahun). Untuk bulan, lama = banyak bulan : 12. Neto = bruto − tara."],
                [("Dibeli Rp80.000, dijual Rp92.000. Persentase untung?", ["Untung Rp12.000", "12.000 : 80.000 × 100%"], "15%"),
                 ("Rp2.000.000 dengan bunga 6% per tahun, 8 bulan. Bunganya?", ["8/12 × 6% × 2.000.000"], "Rp80.000")],
                [["Persentase untung dihitung dari harga jual", "Hitung dari harga beli"],
                 ["Diskon 20% lalu 10% = diskon 30%", "Diskon kedua dihitung dari harga setelah diskon pertama"],
                 ["Bunga 6 bulan dihitung 6 × persen per tahun", "6 bulan = 6/12 tahun"]],
                [("Apa beda bunga tunggal dan bunga majemuk?", "Bunga tunggal selalu dihitung dari modal awal. Bunga majemuk dihitung dari modal ditambah bunga sebelumnya."),
                 ("Apa itu bruto, tara, dan neto?", "Bruto adalah berat kotor (isi dan kemasan), tara adalah berat kemasan, dan neto adalah berat bersih isinya."),
                 ("Apakah diskon 50% + 50% berarti gratis?", "Tidak. Diskon kedua dihitung dari harga yang sudah dipotong, jadi harga akhir 25% dari harga awal.")])


# ============================================================ 10. garis dan sudut
def u10():
    def komplemen():
        a = ri(5, 85)
        k = ri(0, 2)
        if k == 0:
            return MN("Pelurus (suplemen) sudut %d° adalah …" % a, 180 - a, [90 - a, 360 - a, 180 + a], "Dua sudut berpelurus jumlahnya 180°: 180° − %d° = %d°." % (a, 180 - a), unit="°") if True else None
        if k == 1:
            return MN("Penyiku (komplemen) sudut %d° adalah …" % a, 90 - a, [180 - a, 90 + a, 360 - a], "Dua sudut berpenyiku jumlahnya 90°: 90° − %d° = %d°." % (a, 90 - a), unit="°")
        b = ri(95, 175)
        return MN("Pelurus sudut %d° adalah …" % b, 180 - b, [b - 90, 360 - b, 90 - (b - 90) if 180 - b != 180 - (b - 90) else 10], "180° − %d° = %d°." % (b, 180 - b), unit="°")

    def jenis():
        a = ri(1, 359)
        if a in (90, 180):
            return None
        c = "lancip" if a < 90 else ("tumpul" if a < 180 else "refleks")
        return M("Sudut %d° termasuk sudut …" % a, c, [x for x in ["lancip", "siku-siku", "tumpul", "lurus", "refleks"] if x != c][:4],
                 "Lancip &lt; 90°, siku-siku = 90°, tumpul antara 90° dan 180°, lurus = 180°, refleks antara 180° dan 360°. %d° adalah sudut %s." % (a, c))

    def aljabar():
        k = ri(0, 2)
        x = ri(5, 30)
        a, b = ri(2, 5), ri(1, 4)
        if k == 0:
            c = 180 - (a + b) * x
            if c < -40 or c > 60 or c == 0:
                return None
            # (ax + c1) + (bx + c2) = 180
            c1 = ri(-10, 30)
            c2 = 180 - (a + b) * x - c1
            if c2 < -30 or c2 > 60 or a * x + c1 <= 0 or b * x + c2 <= 0:
                return None
            return MN("Dua sudut berpelurus besarnya (%s)° dan (%s)°. Nilai x adalah …" % (lin(a, c1), lin(b, c2)), x, [x + 2, Fr(90 - c1 - c2, a + b) if Fr(90 - c1 - c2, a + b).denominator == 1 and 90 - c1 - c2 > 0 else x + 5, x - 3],
                      "(%s) + (%s) = 180 → %dx %s %d = 180 → x = %d." % (lin(a, c1), lin(b, c2), a + b, "+" if c1 + c2 >= 0 else "−", abs(c1 + c2), x))
        if k == 1:
            c1 = ri(-5, 20)
            c2 = 90 - (a + b) * x - c1
            if a * x + c1 <= 0 or b * x + c2 <= 0 or abs(c2) > 50:
                return None
            return MN("Dua sudut berpenyiku besarnya (%s)° dan (%s)°. Nilai x adalah …" % (lin(a, c1), lin(b, c2)), x, [x + 2, x - 2, Fr(180 - c1 - c2, a + b) if Fr(180 - c1 - c2, a + b).denominator == 1 else x + 4],
                      "Jumlahnya 90: %dx %s %d = 90 → x = %d." % (a + b, "+" if c1 + c2 >= 0 else "−", abs(c1 + c2), x))
        c1 = ri(0, 40)
        c2 = (a - b) * x + c1
        if a == b or b * x + c2 <= 0 or a * x + c1 >= 180:
            return None
        return MN("Dua sudut bertolak belakang besarnya (%s)° dan (%s)°. Nilai x adalah …" % (lin(a, c1), lin(b, c2)), x, [x + 3, x - 2, x * 2],
                  "Sudut bertolak belakang sama besar: %s = %s → x = %d." % (lin(a, c1), lin(b, c2), x))

    NAMES = {frozenset((1, 5)): "sehadap", frozenset((2, 6)): "sehadap", frozenset((3, 7)): "sehadap", frozenset((4, 8)): "sehadap",
             frozenset((3, 5)): "dalam berseberangan", frozenset((4, 6)): "dalam berseberangan",
             frozenset((1, 7)): "luar berseberangan", frozenset((2, 8)): "luar berseberangan",
             frozenset((4, 5)): "dalam sepihak", frozenset((3, 6)): "dalam sepihak",
             frozenset((1, 8)): "luar sepihak", frozenset((2, 7)): "luar sepihak",
             frozenset((1, 3)): "bertolak belakang", frozenset((2, 4)): "bertolak belakang", frozenset((5, 7)): "bertolak belakang", frozenset((6, 8)): "bertolak belakang",
             frozenset((1, 2)): "berpelurus", frozenset((5, 6)): "berpelurus", frozenset((3, 4)): "berpelurus", frozenset((7, 8)): "berpelurus"}

    def val(p, th):
        return th if p % 2 == 1 else 180 - th

    def sejajar_hitung():
        th = ri(35, 80)
        p, qp = ri(1, 8), ri(1, 8)
        key = frozenset((p, qp))
        if p == qp or key not in NAMES:
            return None
        known = val(p, th)
        v = val(qp, th)
        pic = sejajar(th, {p: "%d°" % known, qp: "x"})
        return MN("Garis g sejajar garis h. Besar sudut x adalah …" + pic, v, [180 - v, 90 - th if 90 - th != v else th + 10, v + 10 if v + 10 != 180 - v else v - 10],
                  "Kedua sudut %s, jadi %s. x = %d°." % (NAMES[key], "sama besar" if v == known else "jumlahnya 180°", v), unit="°")

    def sejajar_nama():
        th = ri(40, 75)
        key = ch([k for k, n in NAMES.items() if n not in ("berpelurus", "bertolak belakang")])
        p, qp = sorted(key)
        pic = sejajar(th, {p: "a", qp: "b"})
        c = NAMES[key]
        opts = ["sehadap", "dalam berseberangan", "luar berseberangan", "dalam sepihak", "luar sepihak"]
        return M("Garis g sejajar garis h. Pasangan sudut a dan b disebut sudut …" + pic, c, [o for o in sh(opts) if o != c],
                 "Sudut a dan b adalah sudut %s." % c)

    sets = [("Jenis sudut", [(jenis, 20)]),
            ("Penyiku dan pelurus", [(komplemen, 20)]),
            ("Hubungan antarsudut", [(aljabar, 20)]),
            ("Nama pasangan sudut pada garis sejajar", [(sejajar_nama, 20)]),
            ("Menghitung sudut pada garis sejajar", [(sejajar_hitung, 20)])]
    return unit("garis-dan-sudut", "G", 10, "Garis dan Sudut: Penyiku, Pelurus, dan Garis Sejajar", "Garis dan Sudut",
                "Peserta didik menjelaskan sifat-sifat sudut (berpenyiku, berpelurus, bertolak belakang) dan sudut yang terbentuk oleh dua garis sejajar yang dipotong oleh garis transversal.",
                "Latihan garis dan sudut kelas 7 SMP: jenis sudut, sudut berpenyiku dan berpelurus, sudut bertolak belakang, sudut sehadap, dalam berseberangan, dan dalam sepihak pada garis sejajar. 100 soal dengan kunci jawaban.",
                "Sehadap sama besar, sepihak 180°", "Penyiku jumlahnya 90°, pelurus jumlahnya 180°.", sets,
                ["Dua sudut berpenyiku jumlahnya 90°, dua sudut berpelurus jumlahnya 180°, dan dua sudut bertolak belakang sama besar.",
                 "Jika dua garis sejajar dipotong garis lain, sudut sehadap, dalam berseberangan, dan luar berseberangan sama besar.",
                 "Sudut dalam sepihak dan luar sepihak jumlahnya 180°."],
                [("Pelurus 65° adalah …", ["180° − 65°"], "115°"),
                 ("Sudut sehadap dengan sudut 72° besarnya …", ["Sudut sehadap sama besar"], "72°")],
                [["Penyiku 30° adalah 150°", "Penyiku 30° adalah 60° (jumlah 90°)"],
                 ["Sudut dalam sepihak sama besar", "Sudut dalam sepihak jumlahnya 180°"],
                 ["Sudut bertolak belakang jumlahnya 180°", "Sudut bertolak belakang sama besar"]],
                [("Apa itu garis transversal?", "Garis yang memotong dua garis atau lebih. Pada gambar, garis k memotong garis g dan h."),
                 ("Bagaimana mengenali sudut sehadap?", "Sudut sehadap berada di posisi yang sama pada setiap titik potong, misalnya sama-sama di kanan atas."),
                 ("Apa beda sudut dalam dan sudut luar?", "Sudut dalam berada di antara dua garis sejajar, sudut luar berada di luar kedua garis itu.")])


# ============================================================ 11. segitiga dan segi empat
def u11():
    def sudut3():
        a, b = ri(25, 95), ri(20, 80)
        c = 180 - a - b
        if c < 15:
            return None
        pts = [(0, 0), (ri(8, 12), 0), (ri(2, 7), ri(4, 7))]
        pic = poly_ang(pts, ["%d°" % a, "%d°" % b, "x"], label="segitiga dengan dua sudut diketahui")
        return MN("Besar sudut x pada segitiga berikut adalah …" + pic, c, [360 - a - b, 180 - a, 90 - (a + b) % 90 if 90 - (a + b) % 90 != c else c + 10, c + 10], "Jumlah sudut segitiga 180°: 180° − %d° − %d° = %d°." % (a, b, c), unit="°")

    def luar():
        a, b = ri(30, 80), ri(30, 80)
        k = ri(0, 1)
        if k == 0:
            return MN("Dua sudut dalam segitiga besarnya %d° dan %d°. Sudut luar di titik sudut ketiga besarnya …" % (a, b), a + b, [180 - a - b, 360 - a - b, abs(a - b) if abs(a - b) != a + b else 100],
                      "Sudut luar = jumlah dua sudut dalam yang tidak bersebelahan: %d° + %d° = %d°." % (a, b, a + b), unit="°")
        c = 180 - a - b
        if c < 20:
            return None
        return MN("Segitiga ABC dengan ∠A = %d° dan ∠B = %d°. Besar ∠C adalah …" % (a, b), c, [a + b, 360 - a - b - 90, 90 - c if 90 - c > 0 and 90 - c != c else c + 15], "∠C = 180° − %d° − %d° = %d°." % (a, b, c), unit="°")

    def jenis():
        k = ri(0, 3)
        if k == 0:
            a = ri(20, 70)
            return M("Segitiga sama kaki dengan sudut puncak %d°. Besar setiap sudut alasnya …" % (180 - 2 * a), "%d°" % a, ["%d°" % (180 - a), "%d°" % (180 - 2 * a), "%d°" % (90 - a if 90 - a != a else a + 10)],
                     "Sudut alas sama besar: (180° − %d°) : 2 = %d°." % (180 - 2 * a, a))
        if k == 1:
            a, b = ri(20, 85), ri(20, 85)
            c = 180 - a - b
            if c <= 0:
                return None
            m = max(a, b, c)
            t = "lancip" if m < 90 else ("siku-siku" if m == 90 else "tumpul")
            return M("Segitiga dengan sudut %d°, %d°, dan %d° termasuk segitiga …" % (a, b, c), t, [x for x in ["lancip", "siku-siku", "tumpul", "sama sisi"] if x != t],
                     "Sudut terbesar %d°, jadi segitiga %s." % (m, t))
        sides = sh([ri(3, 12)] * 2 + [ri(3, 12)]) if k == 2 else [ri(3, 12) for _ in range(3)]
        a, b, c = sides
        if max(sides) * 2 >= sum(sides):
            return None
        t = "sama sisi" if a == b == c else ("sama kaki" if len(set(sides)) == 2 else "sembarang")
        return M("Segitiga dengan panjang sisi %d cm, %d cm, dan %d cm termasuk segitiga …" % (a, b, c), t, [x for x in ["sama sisi", "sama kaki", "sembarang", "siku-siku sama kaki"] if x != t],
                 "%s." % ("Ketiga sisinya sama" if t == "sama sisi" else ("Dua sisinya sama panjang" if t == "sama kaki" else "Ketiga sisinya berbeda")))

    def sifat4():
        F = [("Semua sisinya sama panjang dan semua sudutnya siku-siku", "persegi"), ("Sisi yang berhadapan sama panjang dan semua sudutnya siku-siku", "persegi panjang"),
             ("Semua sisinya sama panjang dan diagonalnya berpotongan tegak lurus, tetapi sudutnya tidak siku-siku", "belah ketupat"),
             ("Sisi yang berhadapan sejajar dan sama panjang, tetapi sudutnya tidak siku-siku", "jajargenjang"),
             ("Hanya sepasang sisi yang sejajar", "trapesium"), ("Dua pasang sisi yang berdekatan sama panjang", "layang-layang")]
        d, c = ch(F)
        return M("Segi empat yang memiliki sifat berikut adalah … <br>“%s.”" % d, c, [x for x in sh([f[1] for f in F]) if x != c], "Sifat itu dimiliki oleh %s." % c)

    def luas():
        k = ri(0, 4)
        if k == 0:
            a, t = ri(4, 20) * 2, ri(3, 15)
            pic = figure({"A": (0, 0), "B": (a, 0), "C": (a * 0.35, t)}, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("A", "B", "%d cm" % a)], dashed=[("C", "H")] if False else (), label="segitiga")
            return MN("Luas segitiga dengan alas %d cm dan tinggi %d cm adalah …" % (a, t), a * t // 2, [a * t, a + t, a * t // 4 if a * t % 4 == 0 else a * t + 2], "L = ½ × %d × %d = %d cm²." % (a, t, a * t // 2), unit="cm²")
        if k == 1:
            a, t = ri(4, 20), ri(3, 15)
            return MN("Luas jajargenjang dengan alas %d cm dan tinggi %d cm adalah …" % (a, t), a * t, [a * t // 2 if a * t % 2 == 0 else a * t + 1, 2 * (a + t), a + t], "L = alas × tinggi = %d × %d = %d cm²." % (a, t, a * t), unit="cm²")
        if k == 2:
            a, b, t = ri(4, 15), ri(8, 25), ri(2, 12) * 2
            if a == b:
                return None
            return MN("Trapesium dengan sisi sejajar %d cm dan %d cm serta tinggi %d cm. Luasnya …" % (a, b, t), (a + b) * t // 2, [(a + b) * t, a * b * t // 2 if a * b * t % 2 == 0 else (a + b) * t + 1, (a + b + t)],
                      "L = ½ × (%d + %d) × %d = %d cm²." % (a, b, t, (a + b) * t // 2), unit="cm²")
        if k == 3:
            d1, d2 = ri(3, 15) * 2, ri(3, 15)
            return MN("Belah ketupat dengan diagonal %d cm dan %d cm. Luasnya …" % (d1, d2), d1 * d2 // 2, [d1 * d2, d1 + d2, 2 * (d1 + d2)], "L = ½ × %d × %d = %d cm²." % (d1, d2, d1 * d2 // 2), unit="cm²")
        d1, d2 = ri(3, 15) * 2, ri(4, 20)
        return MN("Layang-layang dengan diagonal %d cm dan %d cm. Luasnya …" % (d1, d2), d1 * d2 // 2, [d1 * d2, d1 + d2, d1 * d2 // 2 + d1], "L = ½ × d₁ × d₂ = ½ × %d × %d = %d cm²." % (d1, d2, d1 * d2 // 2), unit="cm²")

    def keliling():
        k = ri(0, 3)
        if k == 0:
            s = ri(3, 30)
            return MN("Keliling persegi dengan sisi %d cm adalah …" % s, 4 * s, [s * s, 2 * s, 4 * s + 4], "K = 4 × %d = %d cm." % (s, 4 * s), unit="cm")
        if k == 1:
            K, l = ri(10, 40) * 2, ri(2, 10)
            p = K // 2 - l
            if p <= l:
                return None
            return MN("Keliling persegi panjang %d cm dan lebarnya %d cm. Panjangnya …" % (K, l), p, [K - l, K // 2 + l, K // 4], "p = %d : 2 − %d = %d cm." % (K, l, p), unit="cm")
        if k == 2:
            s = ri(4, 25)
            L = s * s
            return MN("Luas persegi %d cm². Kelilingnya …" % L, 4 * s, [s, 2 * s, L // 4 if L % 4 == 0 else 4 * s + 2], "Sisi = %d cm (karena %d × %d = %d). K = 4 × %d = %d cm." % (s, s, s, L, s, 4 * s), unit="cm")
        a, b, c = ri(3, 15), ri(3, 15), ri(3, 15)
        if max(a, b, c) * 2 >= a + b + c:
            return None
        return MN("Keliling segitiga dengan sisi %d cm, %d cm, dan %d cm adalah …" % (a, b, c), a + b + c, [a * b * c // max(a, b, c), a + b, 2 * (a + b + c)], "%d + %d + %d = %d cm." % (a, b, c, a + b + c), unit="cm")

    def cerita():
        k = ri(0, 2)
        if k == 0:
            p, l = ri(5, 20), ri(3, 12)
            h = ri(3, 10) * 5000
            return MN("Lantai kamar berukuran %d m × %d m akan dipasang karpet seharga %s per m². Biaya seluruhnya …" % (p, l, rp(h)), p * l * h, [2 * (p + l) * h, (p + l) * h, p * l * h + h], "Luas %d m². %d × %s = %s." % (p * l, p * l, num(h), rp(p * l * h)), unit="") if False else \
                M("Lantai kamar berukuran %d m × %d m akan dipasang karpet seharga %s per m². Biaya seluruhnya …" % (p, l, rp(h)), rp(p * l * h), [rp(2 * (p + l) * h), rp((p + l) * h), rp(p * l * h + h)], "Luas %d m². %d × %s = %s." % (p * l, p * l, num(h), rp(p * l * h)))
        if k == 1:
            p, l = ri(10, 40), ri(6, 25)
            n = ri(2, 4)
            return MN("Kebun berbentuk persegi panjang %d m × %d m dipagari kawat %d putaran. Panjang kawat yang diperlukan …" % (p, l, n), 2 * (p + l) * n, [2 * (p + l), p * l * n, (p + l) * n], "Keliling %d m, dikali %d putaran: %d m." % (2 * (p + l), n, 2 * (p + l) * n), unit="m")
        s = ri(2, 6) * 10
        a, b = ri(2, 6) * 10, ri(7, 12) * 10
        t = ri(3, 8) * 10
        return MN("Sebidang tanah berbentuk trapesium dengan sisi sejajar %d m dan %d m serta jarak keduanya %d m. Luas tanah …" % (a, b, t), (a + b) * t // 2, [(a + b) * t, a * t, (a + b + t) * 2], "½ × (%d + %d) × %d = %s m²." % (a, b, t, num((a + b) * t // 2)), unit="m²")

    sets = [("Sudut dalam segitiga", [(sudut3, 12), (luar, 8)]),
            ("Jenis segitiga", [(jenis, 20)]),
            ("Sifat segi empat dan keliling", [(sifat4, 6), (keliling, 14)]),
            ("Luas segitiga dan segi empat", [(luas, 20)]),
            ("Soal cerita", [(cerita, 12), (luas, 8)])]
    return unit("segitiga-dan-segi-empat", "G", 11, "Segitiga dan Segi Empat: Sudut, Keliling, dan Luas", "Segitiga dan Segi Empat",
                "Peserta didik memahami sifat segitiga dan segi empat, menghitung sudut, keliling, dan luasnya, serta menyelesaikan masalah yang terkait.",
                "Latihan segitiga dan segi empat kelas 7 SMP: jumlah sudut segitiga, sudut luar, jenis segitiga, sifat segi empat, keliling, luas segitiga, jajargenjang, trapesium, belah ketupat, dan layang-layang. 100 soal dengan kunci jawaban.",
                "Jumlah sudut segitiga = 180°", "Luas segitiga = ½ × alas × tinggi.", sets,
                ["Jumlah ketiga sudut dalam segitiga selalu 180°. Sudut luar segitiga sama dengan jumlah dua sudut dalam yang tidak bersebelahan dengannya.",
                 "Luas segitiga = ½ × alas × tinggi, jajargenjang = alas × tinggi, trapesium = ½ × (jumlah sisi sejajar) × tinggi, belah ketupat dan layang-layang = ½ × d₁ × d₂.",
                 "Keliling adalah jumlah panjang semua sisi."],
                [("Segitiga dengan sudut 48° dan 67°. Sudut ketiga?", ["180° − 48° − 67°"], "65°"),
                 ("Trapesium: sisi sejajar 6 cm dan 10 cm, tinggi 5 cm. Luas?", ["½ × 16 × 5"], "40 cm²")],
                [["Luas segitiga = alas × tinggi", "Luas segitiga = ½ × alas × tinggi"],
                 ["Tinggi jajargenjang diganti sisi miringnya", "Tinggi selalu tegak lurus alas"],
                 ["Jumlah sudut segitiga 360°", "Jumlah sudut segitiga 180°, segi empat 360°"]],
                [("Apakah persegi termasuk persegi panjang?", "Ya. Persegi memiliki semua sifat persegi panjang, ditambah semua sisinya sama panjang."),
                 ("Mengapa luas segitiga setengah dari alas × tinggi?", "Dua segitiga yang sama dapat disusun menjadi jajargenjang dengan alas dan tinggi yang sama."),
                 ("Berapa jumlah sudut segi empat?", "360°, karena segi empat dapat dibagi menjadi dua segitiga.")])


# ============================================================ 12. kubus dan balok
def u12():
    def balok_pic(p, l, t, lab=True):
        import math
        sc = 150.0 / max(p + l * 0.5, t + l * 0.5)
        P, L, Tt = p * sc, l * sc * 0.5, t * sc
        x0, y0 = 62, 30 + L + Tt
        pts = lambda a: " ".join("%.1f,%.1f" % q for q in a)
        s = ["<polygon points='%s' fill='#dfeafc' stroke='%s' stroke-width='2'/>" % (pts([(x0, y0), (x0 + P, y0), (x0 + P, y0 - Tt), (x0, y0 - Tt)]), INK),
             "<polygon points='%s' fill='#c7d9f7' stroke='%s' stroke-width='2'/>" % (pts([(x0, y0 - Tt), (x0 + P, y0 - Tt), (x0 + P + L, y0 - Tt - L), (x0 + L, y0 - Tt - L)]), INK),
             "<polygon points='%s' fill='#b0c8f0' stroke='%s' stroke-width='2'/>" % (pts([(x0 + P, y0), (x0 + P + L, y0 - L), (x0 + P + L, y0 - Tt - L), (x0 + P, y0 - Tt)]), INK)]
        if lab:
            s.append(text(x0 + P / 2, y0 + 20, "%s cm" % num(p), 14, col=BLUE))
            s.append(text(x0 + P + L / 2 + 12, y0 - L / 2 + 14, "%s cm" % num(l), 14, col=BLUE, anchor="start"))
            s.append(text(x0 - 6, y0 - Tt / 2 + 5, "%s cm" % num(t), 14, col=BLUE, anchor="end"))
        return wrap(x0 + P + L + 70, y0 + 32, "".join(s), "balok")

    def vol():
        k = ri(0, 2)
        if k == 0:
            p, l, t = ri(3, 15), ri(2, 10), ri(2, 12)
            return MN("Volume balok berikut adalah …" + balok_pic(p, l, t), p * l * t, [2 * (p * l + p * t + l * t), p + l + t, p * l * t // 2 if p * l * t % 2 == 0 else p * l * t + p], "V = p × l × t = %d × %d × %d = %s cm³." % (p, l, t, num(p * l * t)), unit="cm³")
        if k == 1:
            s = ri(2, 15)
            return MN("Volume kubus dengan rusuk %d cm adalah …" % s, s ** 3, [6 * s * s, 3 * s, s * s], "V = s × s × s = %s cm³." % num(s ** 3), unit="cm³")
        p, l, t = ri(3, 15), ri(2, 10), ri(2, 12)
        return MN("Volume balok %s cm³, panjangnya %d cm, dan lebarnya %d cm. Tingginya …" % (num(p * l * t), p, l), t, [p * l, t + 1, p * l * t // p], "t = %s : (%d × %d) = %d cm." % (num(p * l * t), p, l, t), unit="cm")

    def lp():
        k = ri(0, 2)
        if k == 0:
            p, l, t = ri(3, 15), ri(2, 10), ri(2, 12)
            v = 2 * (p * l + p * t + l * t)
            return MN("Luas permukaan balok berikut adalah …" + balok_pic(p, l, t), v, [p * l * t, p * l + p * t + l * t, 2 * (p + l + t)], "LP = 2(pl + pt + lt) = 2(%d + %d + %d) = %s cm²." % (p * l, p * t, l * t, num(v)), unit="cm²")
        if k == 1:
            s = ri(2, 20)
            return MN("Luas permukaan kubus dengan rusuk %d cm adalah …" % s, 6 * s * s, [s ** 3, 4 * s * s, 12 * s], "LP = 6 × s² = 6 × %d = %s cm²." % (s * s, num(6 * s * s)), unit="cm²")
        s = ri(2, 15)
        return MN("Luas permukaan kubus %s cm². Panjang rusuknya …" % num(6 * s * s), s, [s * s, 6 * s, s + 1], "s² = %s : 6 = %d, jadi s = %d cm." % (num(6 * s * s), s * s, s), unit="cm")

    def rusuk():
        k = ri(0, 2)
        if k == 0:
            p, l, t = ri(3, 30), ri(2, 20), ri(2, 20)
            return MN("Jumlah panjang rusuk balok dengan ukuran %d cm × %d cm × %d cm adalah …" % (p, l, t), 4 * (p + l + t), [p + l + t, 2 * (p + l + t), 12 * (p + l + t) // 3 + 4], "Balok punya 12 rusuk: 4 × (%d + %d + %d) = %d cm." % (p, l, t, 4 * (p + l + t)), unit="cm")
        if k == 1:
            s = ri(2, 30)
            return MN("Jumlah panjang rusuk kubus dengan rusuk %d cm adalah …" % s, 12 * s, [6 * s, 8 * s, 4 * s], "Kubus punya 12 rusuk: 12 × %d = %d cm." % (s, 12 * s), unit="cm")
        f = ch([("sisi", "kubus", 6), ("rusuk", "kubus", 12), ("titik sudut", "kubus", 8), ("sisi", "balok", 6), ("rusuk", "balok", 12), ("titik sudut", "balok", 8),
                ("diagonal ruang", "balok", 4), ("diagonal bidang", "kubus", 12)])
        return MN("Banyak %s pada sebuah %s adalah …" % (f[0], f[1]), f[2], [x for x in [4, 6, 8, 12, 24] if x != f[2]], "%s memiliki %d %s." % (f[1].capitalize(), f[2], f[0]))

    def liter():
        p, l, t = ri(4, 20) * 5, ri(3, 12) * 5, ri(3, 10) * 10
        v = p * l * t
        k = ri(0, 1)
        if k == 0:
            return M("Akuarium berbentuk balok %d cm × %d cm × %d cm diisi penuh air. Volume air …" % (p, l, t), "%s liter" % dz(Fr(v, 1000)),
                     ["%s liter" % num(v), "%s liter" % dz(Fr(v, 100)), "%s liter" % dz(Fr(v, 10000))], "V = %s cm³ = %s dm³ = %s liter." % (num(v), dz(Fr(v, 1000)), dz(Fr(v, 1000))))
        f = ch([Fr(1, 2), Fr(3, 4), Fr(2, 5), Fr(3, 5)])
        w = v * f
        return M("Bak mandi %d cm × %d cm × %d cm diisi air %s bagian. Banyak air …" % (p, l, t, fq(f)), "%s liter" % dz(w / 1000),
                 ["%s liter" % dz(Fr(v, 1000)), "%s liter" % dz(w / 100), "%s liter" % dz((v - w) / 1000)], "%s × %s cm³ = %s cm³ = %s liter." % (fq(f), num(v), dz(w), dz(w / 1000)))

    def cerita():
        k = ri(0, 2)
        if k == 0:
            s, a = ri(2, 4) * 10, ri(1, 5) * 5
            if s % a:
                return None
            n = (s // a) ** 3
            return MN("Berapa kubus kecil berusuk %d cm yang dapat dimasukkan ke dalam kotak kubus berusuk %d cm?" % (a, s), n, [s // a, (s // a) ** 2, 6 * (s // a) ** 2], "%d : %d = %d kubus per rusuk. %d³ = %d." % (s, a, s // a, s // a, n), unit="kubus")
        if k == 1:
            p, l, t = ri(3, 8) * 10, ri(2, 6) * 10, ri(2, 5) * 10
            h = ri(2, 9) * 5
            luas = 2 * (p * l + p * t + l * t)
            return MN("Kotak tanpa tutup berukuran %d cm × %d cm × %d cm akan dibuat dari karton. Luas karton yang diperlukan …" % (p, l, t), luas - p * l, [luas, p * l * t, luas - 2 * p * l], "LP tanpa tutup = pl + 2pt + 2lt = %s cm²." % num(luas - p * l), unit="cm²")
        s = ri(2, 6)
        f = ri(2, 3)
        return M("Jika rusuk sebuah kubus diperbesar %d kali, volumenya menjadi … kali semula" % f, "%d" % f ** 3, ["%d" % f, "%d" % f ** 2, "%d" % (3 * f)], "(%ds)³ = %d s³, jadi %d kali." % (f, f ** 3, f ** 3))

    sets = [("Volume kubus dan balok", [(vol, 20)]),
            ("Luas permukaan", [(lp, 20)]),
            ("Rusuk, sisi, dan titik sudut", [(rusuk, 20)]),
            ("Volume dan liter", [(liter, 14), (vol, 6)]),
            ("Soal cerita", [(cerita, 10), (lp, 5), (liter, 5)])]
    return unit("luas-permukaan-dan-volume-kubus-dan-balok", "P", 12, "Luas Permukaan dan Volume Kubus dan Balok", "Kubus dan Balok",
                "Peserta didik menghitung luas permukaan dan volume kubus dan balok, serta menyelesaikan masalah kontekstual yang terkait.",
                "Latihan kubus dan balok kelas 7 SMP: volume, luas permukaan, jumlah panjang rusuk, banyak sisi dan titik sudut, mengubah cm³ ke liter, dan soal cerita. 100 soal dengan kunci jawaban.",
                "V balok = p × l × t", "LP balok = 2(pl + pt + lt), 1 liter = 1.000 cm³.", sets,
                ["Volume balok = p × l × t, volume kubus = s × s × s = s³.",
                 "Luas permukaan adalah jumlah luas semua sisi: balok 2(pl + pt + lt), kubus 6s².",
                 "1 liter = 1 dm³ = 1.000 cm³. Kubus dan balok masing-masing punya 6 sisi, 12 rusuk, dan 8 titik sudut."],
                [("Balok 8 cm × 5 cm × 3 cm. Volume dan luas permukaan?", ["V = 8 × 5 × 3 = 120", "LP = 2(40 + 24 + 15) = 158"], "120 cm³ dan 158 cm²"),
                 ("Akuarium 50 cm × 30 cm × 40 cm. Isinya?", ["60.000 cm³ = 60 dm³"], "60 liter")],
                [["Volume kubus = 6 × s", "Volume kubus = s × s × s"],
                 ["LP balok = p × l × t", "LP = 2(pl + pt + lt), satuannya cm²"],
                 ["1 liter = 100 cm³", "1 liter = 1.000 cm³"]],
                [("Apa beda luas permukaan dan volume?", "Luas permukaan mengukur luas kulit bangun (cm²). Volume mengukur isi bangun (cm³)."),
                 ("Bagaimana mengubah cm³ ke liter?", "Bagi dengan 1.000, karena 1 liter = 1.000 cm³."),
                 ("Apakah kubus termasuk balok?", "Ya. Kubus adalah balok khusus yang panjang, lebar, dan tingginya sama.")])


# ============================================================ 13. penyajian data
def u13():
    THINGS = [("Buah kesukaan", ["Mangga", "Pisang", "Jeruk", "Apel", "Salak"]), ("Olahraga favorit", ["Sepak bola", "Bulu tangkis", "Voli", "Basket", "Renang"]),
              ("Transportasi ke sekolah", ["Jalan kaki", "Sepeda", "Motor", "Angkot", "Mobil"]), ("Ekstrakurikuler", ["Pramuka", "Tari", "Musik", "PMR", "Futsal"])]

    def lingkaran():
        t, names = ch(THINGS)
        n = ri(3, 4)
        names = names[:n]
        while True:
            ps = [ch([5, 10, 15, 20, 25, 30, 35, 40]) for _ in range(n - 1)]
            last = 100 - sum(ps)
            if 5 <= last <= 50:
                break
        ps.append(last)
        tot = ch([40, 60, 80, 120, 200, 240, 300])
        i = ri(0, n - 1)
        k = ri(0, 2)
        data = list(zip(names, ps))
        if k == 0:
            pic = pie(data[:-1] + [(names[-1], 0)], label="diagram lingkaran " + t.lower())
            return MN("Diagram lingkaran menunjukkan %s siswa. Persentase %s adalah …" % (t.lower(), names[-1]) + pic, last, [100 - last, last + 5, sum(ps[:-1])],
                      "Jumlah semua bagian 100%%: 100%% − %d%% = %d%%." % (sum(ps[:-1]), last), unit="%")
        pic = pie(data, label="diagram lingkaran " + t.lower())
        if k == 1:
            v = tot * ps[i] // 100 if tot * ps[i] % 100 == 0 else None
            if v is None:
                return None
            return MN("Diagram lingkaran menunjukkan %s dari %d siswa. Banyak siswa yang memilih %s adalah …" % (t.lower(), tot, names[i]) + pic, v, [ps[i], tot - v, v * 2], "%d%% × %d = %d siswa." % (ps[i], tot, v), unit="siswa")
        return MN("Pada diagram lingkaran itu, besar sudut juring %s adalah …" % names[i] + pic, ps[i] * 360 // 100 if ps[i] * 360 % 100 == 0 else None, [ps[i], ps[i] * 3, 360 - ps[i] * 360 // 100],
                  "%d%% × 360° = %s°." % (ps[i], dz(Fr(ps[i] * 360, 100))), unit="°")

    def garis():
        months = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"]
        vals = [ri(2, 12) * 5 for _ in range(6)]
        if len(set(vals)) < 5:
            return None
        W, H = 380, 220
        mx = max(vals) + 10
        X = lambda i: 60 + i * 56
        Y = lambda v: 180 - v * 150.0 / mx
        s = []
        for g in range(0, mx + 1, 10):
            s.append(line(50, Y(g), 360, Y(g), "#d5dfec", 1) + text(44, Y(g) + 5, num(g), 12, anchor="end", weight=400))
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join("%.1f,%.1f" % (X(i), Y(v)) for i, v in enumerate(vals)), BLUE))
        for i, v in enumerate(vals):
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (X(i), Y(v), BLUE) + text(X(i), 202, months[i], 13, weight=400))
        pic = wrap(W, H, "".join(s), "diagram garis penjualan buku")
        k = ri(0, 3)
        if k == 0:
            i = vals.index(max(vals))
            if vals.count(max(vals)) > 1:
                return None
            return M("Diagram garis menunjukkan banyak buku yang terjual (buah). Penjualan tertinggi terjadi pada bulan …" + pic, months[i], [m for j, m in enumerate(months) if j != i][:3] if False else [months[(i + 1) % 6], months[(i + 2) % 6], months[vals.index(min(vals))]],
                     "Titik tertinggi ada pada %s." % months[i])
        if k == 1:
            i = ri(0, 4)
            d = vals[i + 1] - vals[i]
            if d == 0:
                return None
            return M("Diagram garis menunjukkan banyak buku yang terjual. Dari %s ke %s penjualan …" % (months[i], months[i + 1]) + pic,
                     "%s %d buah" % ("naik" if d > 0 else "turun", abs(d)), ["%s %d buah" % ("turun" if d > 0 else "naik", abs(d)), "%s %d buah" % ("naik" if d > 0 else "turun", vals[i + 1]), "tetap"],
                     "%d → %d, %s %d." % (vals[i], vals[i + 1], "naik" if d > 0 else "turun", abs(d)))
        if k == 2:
            return MN("Diagram garis menunjukkan banyak buku yang terjual. Jumlah buku yang terjual selama 6 bulan …" + pic, sum(vals), [sum(vals) - vals[0], max(vals) * 6, sum(vals) + 10],
                      "%s = %d." % (" + ".join(str(v) for v in vals), sum(vals)), unit="buah")
        i, j = sorted(sh(range(6))[:2])
        return MN("Berapa selisih penjualan bulan %s dan %s?" % (months[i], months[j]) + pic, abs(vals[i] - vals[j]), [vals[i] + vals[j], abs(vals[i] - vals[j]) + 5, max(vals) - min(vals) if max(vals) - min(vals) != abs(vals[i] - vals[j]) else 1],
                  "%d dan %d, selisihnya %d." % (vals[i], vals[j], abs(vals[i] - vals[j])), unit="buah")

    def jenis():
        F = [("warna kesukaan siswa", "kualitatif (kategori)"), ("tinggi badan siswa", "kuantitatif kontinu"), ("banyak saudara kandung", "kuantitatif diskrit"),
             ("jenis kendaraan yang lewat", "kualitatif (kategori)"), ("suhu udara setiap jam", "kuantitatif kontinu"), ("banyak buku yang dibaca dalam sebulan", "kuantitatif diskrit"),
             ("berat badan bayi", "kuantitatif kontinu"), ("merek telepon genggam", "kualitatif (kategori)"), ("banyak gol dalam pertandingan", "kuantitatif diskrit"),
             ("waktu tempuh ke sekolah", "kuantitatif kontinu"), ("nama provinsi asal", "kualitatif (kategori)"), ("banyak siswa per kelas", "kuantitatif diskrit")]
        d, c = ch(F)
        return M("Data tentang %s termasuk data …" % d, c, [x for x in ["kualitatif (kategori)", "kuantitatif diskrit", "kuantitatif kontinu", "bukan data"] if x != c],
                 "Data kategori berupa kata, data diskrit dihitung (bilangan bulat), data kontinu diukur.")

    def pilih():
        F = [("membandingkan bagian dari keseluruhan (persentase)", "diagram lingkaran"), ("menunjukkan perubahan suhu dari jam ke jam", "diagram garis"),
             ("membandingkan banyak siswa di setiap kelas", "diagram batang"), ("menunjukkan pertumbuhan tinggi tanaman setiap minggu", "diagram garis"),
             ("menunjukkan persentase pengeluaran keluarga", "diagram lingkaran"), ("membandingkan hasil panen beberapa desa", "diagram batang")]
        d, c = ch(F)
        q = ch(["Diagram yang paling tepat untuk %s adalah …", "Untuk %s, sebaiknya dipakai …"]) % d
        return M(q, c, [x for x in ["diagram lingkaran", "diagram garis", "diagram batang", "tabel turus saja"] if x != c], "%s cocok untuk %s." % (c.capitalize(), d))

    def populasi():
        F = [("Untuk mengetahui rata-rata tinggi siswa SMP di sebuah kota, diambil 200 siswa dari beberapa sekolah.", "sampel", "200 siswa yang diambil"),
             ("Untuk mengetahui kualitas beras dalam satu gudang, diambil 5 kg beras dari beberapa karung.", "sampel", "5 kg beras yang diambil"),
             ("Untuk mengetahui makanan kesukaan warga desa, ditanya 50 warga desa itu.", "sampel", "50 warga yang ditanya"),
             ("Untuk mengetahui rata-rata tinggi siswa SMP di sebuah kota, diambil 200 siswa dari beberapa sekolah.", "populasi", "seluruh siswa SMP di kota itu"),
             ("Untuk mengetahui kualitas beras dalam satu gudang, diambil 5 kg beras dari beberapa karung.", "populasi", "seluruh beras di gudang itu"),
             ("Untuk mengetahui makanan kesukaan warga desa, ditanya 50 warga desa itu.", "populasi", "seluruh warga desa itu"),
             ("Untuk mengetahui merek pasta gigi yang dipakai siswa kelas 7, ditanya 30 siswa kelas 7.", "sampel", "30 siswa kelas 7 yang ditanya"),
             ("Untuk mengetahui merek pasta gigi yang dipakai siswa kelas 7, ditanya 30 siswa kelas 7.", "populasi", "seluruh siswa kelas 7")]
        d, w, c = ch(F)
        other = [x[2] for x in F if x[0] == d and x[2] != c]
        return M("%s <br>%s penelitian ini adalah …" % (d, w.capitalize()), c, other + ["peneliti", "hasil penelitian", "sekolah-sekolah di kota itu" if "kota" in d else "petugas pendata"],
                 "Populasi adalah seluruh objek yang diteliti, sampel adalah sebagian populasi yang benar-benar diambil.")

    sets = [("Jenis data, populasi, dan sampel", [(jenis, 12), (populasi, 8)]),
            ("Diagram lingkaran", [(lingkaran, 20)]),
            ("Diagram garis", [(garis, 20)]),
            ("Memilih diagram yang tepat", [(pilih, 6), (lingkaran, 7), (garis, 7)]),
            ("Campuran", [(lingkaran, 10), (garis, 10)])]
    return unit("penyajian-data", "D", 13, "Penyajian Data: Diagram Garis dan Diagram Lingkaran", "Penyajian Data",
                "Peserta didik merumuskan pertanyaan, mengumpulkan, menyajikan, dan menganalisis data dengan diagram batang, diagram garis, dan diagram lingkaran, serta memahami populasi dan sampel.",
                "Latihan penyajian data kelas 7 SMP: jenis data, populasi dan sampel, membaca diagram garis, diagram lingkaran (persen dan sudut juring), dan memilih diagram yang tepat. 100 soal dengan kunci jawaban.",
                "Lingkaran utuh = 100% = 360°", "Bagian = persen × total. Sudut juring = persen × 360°.", sets,
                ["Data kategori (kualitatif) berupa kata, misalnya warna. Data kuantitatif berupa bilangan: diskrit jika dihitung, kontinu jika diukur.",
                 "Diagram garis cocok untuk menunjukkan perubahan dari waktu ke waktu. Diagram lingkaran cocok untuk menunjukkan bagian dari keseluruhan.",
                 "Pada diagram lingkaran, seluruh lingkaran = 100% = 360°. Banyak data suatu bagian = persennya × total data."],
                [("25% dari 120 siswa suka voli. Banyaknya?", ["25% × 120 = 30"], "30 siswa"),
                 ("Bagian 15% pada diagram lingkaran. Sudut juringnya?", ["15% × 360° = 54°"], "54°")],
                [["Sudut juring 20% = 20°", "20% × 360° = 72°"],
                 ["Sampel sama dengan populasi", "Sampel hanya sebagian dari populasi"],
                 ["Diagram lingkaran dipakai untuk perubahan suhu", "Perubahan dari waktu ke waktu memakai diagram garis"]],
                [("Kapan memakai diagram lingkaran?", "Saat ingin menunjukkan bagian dari keseluruhan, misalnya persentase siswa yang memilih setiap olahraga."),
                 ("Mengapa penelitian memakai sampel?", "Karena meneliti seluruh populasi sering terlalu mahal atau lama. Sampel yang baik mewakili populasi."),
                 ("Apa beda data diskrit dan kontinu?", "Data diskrit diperoleh dengan menghitung (banyak siswa). Data kontinu diperoleh dengan mengukur (tinggi badan).")])


# ============================================================ 14. peluang
def u14():
    def dadu():
        F = [("bilangan genap", [2, 4, 6]), ("bilangan ganjil", [1, 3, 5]), ("bilangan prima", [2, 3, 5]), ("faktor dari 6", [1, 2, 3, 6]),
             ("bilangan lebih dari 4", [5, 6]), ("bilangan kurang dari 3", [1, 2]), ("bilangan kelipatan 3", [3, 6]), ("bilangan 7", []),
             ("bilangan kurang dari 7", [1, 2, 3, 4, 5, 6]), ("bilangan 5", [5]), ("bilangan bukan 1", [2, 3, 4, 5, 6]), ("bilangan lebih dari 2", [3, 4, 5, 6])]
        t, a = ch(F)
        if ri(0, 2) == 0 and 0 < len(a) < 6:
            v = Fr(6 - len(a), 6)
            return M("Sebuah dadu dilempar sekali. Peluang tidak muncul mata dadu %s adalah …" % t, fq(v), [fq(1 - v), fq(Fr(6 - len(a), len(a))), fq(Fr(7 - len(a), 6)), fq(Fr(1, 6))],
                     "P(tidak A) = 1 − %d/6 = %s." % (len(a), fq(v)))
        v = Fr(len(a), 6)
        w = [Fr(len(a), 6 - len(a)) if len(a) not in (0, 6) else Fr(1, 2), Fr(6 - len(a), 6), Fr(len(a) + 1, 6), Fr(1, 6) if len(a) != 1 else Fr(1, 3)]
        return M("Sebuah dadu dilempar sekali. Peluang muncul mata dadu %s adalah …" % t, fq(v), [fq(x) for x in w],
                 "Ruang sampel {1, 2, 3, 4, 5, 6}, n(S) = 6. Yang memenuhi: %s, ada %d. P = %d/6 = %s." % ("{" + ", ".join(map(str, a)) + "}" if a else "tidak ada", len(a), len(a), fq(v)))

    def kantong():
        cols = ["merah", "biru", "hijau", "kuning", "putih"]
        n = ri(2, 4)
        cs = cols[:n]
        cnt = [ri(1, 9) for _ in cs]
        tot = sum(cnt)
        i = ri(0, n - 1)
        k = ri(0, 1)
        desc = ", ".join("%d bola %s" % (c, nm) for c, nm in zip(cnt, cs))
        if k == 0:
            v = Fr(cnt[i], tot)
            return M("Sebuah kantong berisi %s. Diambil satu bola secara acak. Peluang terambil bola %s adalah …" % (desc, cs[i]), fq(v),
                     [fq(Fr(cnt[i], tot - cnt[i])) if tot - cnt[i] else None, fq(1 - v), fq(Fr(1, n)), fq(Fr(cnt[i] + 1, tot))], "Ada %d bola %s dari %d bola. P = %s." % (cnt[i], cs[i], tot, fq(v) if v.numerator == cnt[i] else "%d/%d = %s" % (cnt[i], tot, fq(v))))
        v = Fr(tot - cnt[i], tot)
        return M("Sebuah kantong berisi %s. Diambil satu bola acak. Peluang terambil bola yang bukan %s adalah …" % (desc, cs[i]), fq(v),
                 [fq(1 - v), fq(Fr(tot - cnt[i], cnt[i])), fq(Fr(n - 1, n)), fq(Fr(tot - cnt[i] - 1, tot))], "P(bukan %s) = 1 − %d/%d = %s." % (cs[i], cnt[i], tot, fq(v)))

    def kartu():
        n = ri(10, 30)
        F = [("genap", lambda x: x % 2 == 0), ("ganjil", lambda x: x % 2), ("kelipatan 3", lambda x: x % 3 == 0), ("kelipatan 5", lambda x: x % 5 == 0),
             ("prima", lambda x: x > 1 and all(x % d for d in range(2, x))), ("lebih dari %d" % (n - 4), lambda x: x > n - 4), ("kelipatan 4", lambda x: x % 4 == 0)]
        t, f = ch(F)
        a = [x for x in range(1, n + 1) if f(x)]
        v = Fr(len(a), n)
        return M("Kartu bernomor 1 sampai %d dikocok, lalu diambil satu. Peluang terambil kartu bernomor %s adalah …" % (n, t), fq(v),
                 [fq(Fr(len(a), n - len(a))), fq(1 - v), fq(Fr(len(a) + 1, n)), fq(Fr(len(a), n + 1))], "Ada %d kartu yang memenuhi dari %d kartu. P = %s." % (len(a), n, fq(v) if Fr(len(a), n).numerator == len(a) else "%d/%d = %s" % (len(a), n, fq(v))))

    def ruang():
        F = [("sebuah koin dilempar sekali", 2, "{A, G}"), ("sebuah dadu dilempar sekali", 6, "{1, 2, 3, 4, 5, 6}"),
             ("dua koin dilempar bersama", 4, "{AA, AG, GA, GG}"), ("tiga koin dilempar bersama", 8, "2 × 2 × 2"), ("sebuah koin dan sebuah dadu dilempar bersama", 12, "2 × 6"),
             ("dua dadu dilempar bersama", 36, "6 × 6"), ("huruf diambil dari kata “MATEMATIKA” (huruf berbeda)", 5, "{M, A, T, E, I, K}" if False else "{M, A, T, E, I, K}")]
        F = F[:6] + [("sebuah dadu dan dua koin dilempar bersama", 24, "6 × 2 × 2"), ("satu hari dipilih acak dari satu minggu", 7, "Senin sampai Minggu"),
                     ("satu bulan dipilih acak dari satu tahun", 12, "Januari sampai Desember"), ("roda putar dengan 8 bagian bernomor 1 sampai 8 diputar sekali", 8, "{1, 2, …, 8}"),
                     ("satu huruf vokal dipilih acak", 5, "{a, i, u, e, o}")]
        t, n, s = ch(F)
        return MN("Banyak anggota ruang sampel jika %s adalah …" % t, n, sh([x for x in [2, 4, 5, 6, 7, 8, 12, 18, 24, 36] if x != n]),
                  "Ruang sampel: %s, jadi ada %d anggota." % (s, n))

    def nilai():
        F = [("matahari terbit dari timur", "1"), ("sebuah dadu menunjukkan mata 8", "0"), ("koin menunjukkan angka atau gambar", "1"),
             ("bulan Februari memiliki 32 hari", "0"), ("sebuah koin menunjukkan gambar", fq(Fr(1, 2))), ("terambil bola merah dari kantong yang semuanya bola merah", "1"),
             ("terambil bola biru dari kantong yang semuanya bola merah", "0"), ("dadu menunjukkan bilangan kurang dari 10", "1")]
        t, c = ch(F)
        return M("Peluang kejadian “%s” adalah …" % t, c, [x for x in ["0", "1", fq(Fr(1, 2)), fq(Fr(1, 6)), "2"] if x != c],
                 "Kejadian pasti berpeluang 1, kejadian mustahil berpeluang 0, kejadian lain di antara 0 dan 1.")

    def harapan():
        k = ri(0, 2)
        n = ch([60, 120, 180, 240, 300, 600])
        if k == 0:
            m = ri(1, 6)
            return MN("Sebuah dadu dilempar %d kali. Frekuensi harapan muncul mata dadu %d adalah …" % (n, m), n // 6, [n // 2, n // 3, n // 6 + 6], "Fh = P × n = 1/6 × %d = %d kali." % (n, n // 6), unit="kali")
        if k == 1:
            return MN("Sebuah koin dilempar %d kali. Frekuensi harapan muncul gambar adalah …" % n, n // 2, [n, n // 4, n // 2 + 10], "Fh = 1/2 × %d = %d kali." % (n, n // 2), unit="kali")
        return MN("Sebuah dadu dilempar %d kali. Frekuensi harapan muncul mata dadu genap adalah …" % n, n // 2, [n // 6, n // 3, n], "P(genap) = 3/6 = 1/2. Fh = 1/2 × %d = %d kali." % (n, n // 2), unit="kali")

    sets = [("Ruang sampel dan nilai peluang", [(ruang, 10), (nilai, 8), (kartu, 2)]),
            ("Peluang pada dadu", [(dadu, 12), (kartu, 8)]),
            ("Peluang pada kantong", [(kantong, 20)]),
            ("Peluang pada kartu", [(kartu, 20)]),
            ("Frekuensi harapan", [(harapan, 14), (dadu, 6)])]
    return unit("peluang", "D", 14, "Peluang Suatu Kejadian", "Peluang",
                "Peserta didik menentukan ruang sampel dan peluang suatu kejadian sederhana, serta memahami bahwa peluang bernilai antara 0 dan 1.",
                "Latihan peluang kelas 7 SMP: ruang sampel, nilai peluang 0 sampai 1, peluang pada dadu, koin, kantong bola, dan kartu bernomor, serta frekuensi harapan. 100 soal dengan kunci jawaban.",
                "P(A) = n(A) : n(S)", "Peluang selalu di antara 0 (mustahil) dan 1 (pasti).", sets,
                ["Ruang sampel (S) adalah himpunan semua hasil yang mungkin. Pada dadu, S = {1, 2, 3, 4, 5, 6}, jadi n(S) = 6.",
                 "Peluang kejadian A: P(A) = n(A) : n(S), dengan n(A) banyak hasil yang memenuhi A. Peluang kejadian bukan A = 1 − P(A).",
                 "Frekuensi harapan = P(A) × banyak percobaan."],
                [("Dadu dilempar. Peluang muncul bilangan prima?", ["Prima: 2, 3, 5 (3 hasil)", "P = 3/6"], "1/2"),
                 ("Kantong: 3 merah, 5 biru. Peluang terambil biru?", ["n(S) = 8", "P = 5/8"], "5/8")],
                [["Peluang biru dihitung 5/3 (biru : merah)", "Bagi dengan seluruh bola: 5/8"],
                 ["Peluang bisa lebih dari 1", "Peluang selalu antara 0 dan 1"],
                 ["1 bilangan prima pada dadu", "Bilangan prima pada dadu: 2, 3, 5"]],
                [("Apa itu ruang sampel?", "Himpunan semua hasil yang mungkin dari suatu percobaan."),
                 ("Apa arti peluang 0 dan 1?", "Peluang 0 berarti kejadian itu mustahil, peluang 1 berarti kejadian itu pasti terjadi."),
                 ("Apa itu frekuensi harapan?", "Perkiraan berapa kali suatu kejadian muncul jika percobaan diulang n kali: P(A) × n.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14]
