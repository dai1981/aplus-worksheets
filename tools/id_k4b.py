# -*- coding: utf-8 -*-
"""Indonesia Kelas 4 (Fase B): pecahan, aljabar, pengukuran, geometri, data（8〜17）。"""
import math
from fractions import Fraction as F
import id_k4a as A
from id_k4a import ri, ch, pool, stmt, frac_pic, bar_frac, pie
from id_common import (num, dec, u, NB, mcq, lesson, example, table, wrap, fr, diagram_batang, text, line,
                       INK, GREEN, FILL, RED, BLUE)
from de_common import strichliste


def K():
    return A.K


def R():
    return A.R


def f(a, b):
    return fr(a, b)


def fc(k, n):
    """分数の誤答の予備（よくある間違いの形）"""
    out = []
    for a, b in [(n - k, n), (k, n - k), (n, k), (k + 1, n), (k, n + 1), (k - 1, n), (k, n - 1), (k + 2, n), (k, 2 * n)]:
        if a > 0 and b > 1 and (a, b) != (k, n):
            out.append(f(a, b))
    return out


def ftxt(a, b):
    return "%d/%d" % (a, b)


# ============================================================ 8. pecahan
def u8():
    def arsir():
        n = ri(2, 10)
        k = ri(1, n - 1)
        return mcq("Bagian yang diarsir pada gambar adalah …" + frac_pic(n, k), f(k, n), [f(n - k, n), f(k, n - k), f(n, k) if k > 1 else f(k, n + 1)] + fc(k, n),
                   "Ada %d bagian sama besar dan %d bagian diarsir: %s." % (n, k, f(k, n)))

    def satu():
        a, b = R().sample(range(2, 11), 2)
        return stmt(f(1, a), f(1, b), F(1, a), F(1, b),
                    "Untuk pecahan berpembilang satu, penyebut lebih besar berarti bagiannya lebih kecil. %s %s %s."
                    % (f(1, a), A.rel(F(1, a), F(1, b)), f(1, b)))

    def sama():
        n = ri(4, 12)
        a, b = R().sample(range(1, n), 2)
        return stmt(f(a, n), f(b, n), F(a, n), F(b, n), "Penyebutnya sama, jadi bandingkan pembilangnya: %d %s %d." % (a, A.rel(a, b), b))

    def ekstrem():
        if R().random() < 0.5:
            ds = R().sample(range(2, 13), 4)
            fs = [(1, d) for d in ds]
            why = "Pecahan berpembilang satu: makin besar penyebutnya, makin kecil pecahannya."
        else:
            n = ri(6, 12)
            fs = [(a, n) for a in R().sample(range(1, n), 4)]
            why = "Penyebutnya sama: pembilang terbesar adalah pecahan terbesar."
        big = R().random() < 0.5
        key = lambda p: F(*p)
        c = max(fs, key=key) if big else min(fs, key=key)
        return mcq("Pecahan %s dari %s adalah …" % ("terbesar" if big else "terkecil", ", ".join(f(*p) for p in fs)), f(*c),
                   [f(*p) for p in fs if p != c], why)

    def urut():
        if R().random() < 0.5:
            fs = [(1, d) for d in R().sample(range(2, 13), 4)]
        else:
            n = ri(5, 12)
            fs = [(a, n) for a in R().sample(range(1, n), 4)]
        up = R().random() < 0.5
        g = sorted(fs, key=lambda p: F(*p), reverse=not up)
        j = lambda xs: ", ".join(f(*p) for p in xs)
        w1 = sorted(fs, key=lambda p: F(*p), reverse=up)
        w2 = sorted(fs, key=lambda p: (p[1], p[0]), reverse=not up) if fs[0][0] == 1 else list(reversed(g))
        w3 = list(g)
        w3[0], w3[1] = w3[1], w3[0]
        w4 = list(g)
        w4[2], w4[3] = w4[3], w4[2]
        return mcq("Urutan pecahan %s dari yang %s adalah …" % (j(pool(fs)), "terkecil ke terbesar" if up else "terbesar ke terkecil"),
                   j(g), [j(w1), j(w2), j(w3), j(w4)], "Urutannya: %s." % j(g))

    def gambar2():
        a, b = R().sample(range(2, 9), 2)
        pa, pb = bar_frac(a, 1, w=240, h=30), bar_frac(b, 1, w=240, h=30)
        return mcq("Pita pertama diarsir %s dan pita kedua diarsir %s. Pernyataan yang benar adalah …%s%s" % (f(1, a), f(1, b), pa, pb),
                   "%s %s %s" % (f(1, a), A.rel(F(1, a), F(1, b)), f(1, b)),
                   ["%s %s %s" % (f(1, a), A.rel(F(1, b), F(1, a)), f(1, b)), "%s = %s" % (f(1, a), f(1, b)), "%s %s %s" % (f(1, b), A.rel(F(1, a), F(1, b)), f(1, a))],
                   "Bagian dari pita yang dibagi %d lebih %s." % (max(a, b), "kecil"))

    def cerita():
        a, b = R().sample(range(2, 11), 2)
        x, y = K().two()
        food = ch(["kue bolu", "martabak", "semangka", "pizza", "roti", "pepaya"])
        if R().random() < 0.5:
            winner = x if a < b else y
            return mcq("%s memakan %s %s, dan %s memakan %s %s yang sama besar. Siapa yang makan lebih banyak?" % (x, f(1, a), food, y, f(1, b), food),
                       winner, [y if winner == x else x, "Sama banyak", "Tidak bisa ditentukan"],
                       "%s %s %s, jadi %s makan lebih banyak." % (f(1, min(a, b)), "&gt;", f(1, max(a, b)), winner))
        n = ri(5, 12)
        p, q = R().sample(range(1, n), 2)
        winner = x if p > q else y
        return mcq("Sebuah %s dipotong menjadi %d bagian sama besar. %s mengambil %s dan %s mengambil %s. Siapa yang mengambil lebih banyak?"
                   % (food, n, x, f(p, n), y, f(q, n)), winner, [y if winner == x else x, "Sama banyak", "Tidak bisa ditentukan"],
                   "Penyebutnya sama, bandingkan pembilang: %d dan %d." % (p, q))

    def nama():
        n = ri(2, 10)
        k = ri(1, n - 1)
        NM = ["", "", "setengah", "sepertiga", "seperempat", "seperlima", "seperenam", "sepertujuh", "seperdelapan", "sepersembilan", "sepersepuluh"]
        if k == 1:
            return mcq("Pecahan %s dibaca …" % f(1, n), NM[n], [NM[m] for m in R().sample(range(2, 11), 5) if m != n], "%s dibaca %s." % (f(1, n), NM[n]))
        w = "%s per%s" % (A.terbilang(k), A.terbilang(n))
        return mcq("Pecahan %s dibaca …" % f(k, n), w, ["%s per%s" % (A.terbilang(n), A.terbilang(k)), "%s per%s" % (A.terbilang(k), A.terbilang(n + 1)), "%s per%s" % (A.terbilang(k + 1), A.terbilang(n))],
                   "Pembilang %d dibaca dulu, lalu per dan penyebut %d." % (k, n))

    sets = [("Membaca dan menulis pecahan", [(arsir, 14), (nama, 6)]),
            ("Pecahan berpembilang satu", [(satu, 12), (gambar2, 8)]),
            ("Pecahan berpenyebut sama", [(sama, 14), (arsir, 6)]),
            ("Terbesar, terkecil, dan urutan", [(ekstrem, 10), (urut, 10)]),
            ("Soal cerita", [(cerita, 16), (urut, 4)])]
    body = lesson(
        ["Pecahan menunjukkan bagian dari satu benda yang dibagi sama besar. Pada " + f(3, 5) + ", penyebut 5 adalah banyak bagian, pembilang 3 adalah bagian yang diambil.",
         "Pecahan berpembilang satu: makin besar penyebutnya, makin kecil bagiannya. " + f(1, 3) + " &gt; " + f(1, 5) + ".",
         "Pecahan berpenyebut sama: bandingkan pembilangnya. " + f(4, 7) + " &gt; " + f(2, 7) + "."],
        [example("Bandingkan %s dan %s." % (f(1, 4), f(1, 6)), ["Pembilangnya sama-sama 1", "4 &lt; 6, jadi bagian per-empat lebih besar"], "%s &gt; %s" % (f(1, 4), f(1, 6))),
         example("Urutkan dari terkecil: %s, %s, %s." % (f(5, 8), f(1, 8), f(3, 8)), ["Penyebutnya sama, urutkan pembilang: 1, 3, 5"], "%s, %s, %s" % (f(1, 8), f(3, 8), f(5, 8)))],
        [["%s &gt; %s karena 8 &gt; 2" % (f(1, 8), f(1, 2)), "Dibagi 8 bagian lebih kecil: %s &lt; %s" % (f(1, 8), f(1, 2))],
         ["Bagian yang diarsir ditulis sebagai penyebut", "Penyebut = semua bagian, pembilang = bagian yang diarsir"],
         ["Bagian tidak sama besar tetap dianggap pecahan", "Pecahan hanya untuk bagian yang sama besar"]])
    faq = [{"q": "Apa itu pembilang dan penyebut?", "a": "Pada pecahan 3/4, angka 3 di atas adalah pembilang (bagian yang diambil) dan angka 4 di bawah adalah penyebut (banyak bagian sama besar)."},
           {"q": "Mengapa 1/2 lebih besar dari 1/5?", "a": "Jika benda yang sama dibagi 2, setiap bagian lebih besar daripada jika dibagi 5. Jadi 1/2 > 1/5."},
           {"q": "Bagaimana membandingkan pecahan berpenyebut sama?", "a": "Bandingkan pembilangnya saja. Contoh: 5/9 > 2/9 karena 5 > 2."}]
    return dict(slug="pecahan", dom="B", sort=8,
                std_text="Peserta didik dapat membandingkan dan mengurutkan antarpecahan dengan pembilang satu dan antarpecahan dengan penyebut yang sama.",
                title="Pecahan: Membandingkan dan Mengurutkan", short_title="Pecahan",
                meta_desc="Latihan membaca pecahan dari gambar, membandingkan pecahan berpembilang satu dan berpenyebut sama, dan mengurutkan pecahan. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Pembilang per penyebut", key_sub="1/3 > 1/5: penyebut besar, bagian kecil.",
                body=body, faq=faq, sets=sets)


# ============================================================ 9. pecahan senilai
BASE = [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 6), (5, 6)]


def u9():
    def isi_atas():
        a, b = ch(BASE)
        k = ri(2, 12 // b if b <= 6 else 2)
        if k < 2 or b * k > 24:
            return None
        return mcq("%s = %s" % (f(a, b), f("…", b * k)), str(a * k), [str(a + k), str(a * k + 1), str(b * k - a * k) if b * k - a * k != a * k else str(a * k + 2)],
                   "Penyebut dikali %d, jadi pembilang juga dikali %d: %d × %d = %d." % (k, k, a, k, a * k))

    def isi_bawah():
        a, b = ch(BASE)
        k = ri(2, 5)
        return mcq("%s = %s" % (f(a, b), f(a * k, "…")), str(b * k), [str(b + k), str(b * k + 1), str(a * k + b)],
                   "Pembilang dikali %d, jadi penyebut juga dikali %d: %d × %d = %d." % (k, k, b, k, b * k))

    def pilih():
        a, b = ch(BASE)
        m = ri(1, 2)
        k = ri(2, 4)
        if k == m:
            return None
        g = f(a * k, b * k)
        if m == 2:
            return mcq("Pecahan yang senilai dengan %s adalah …" % f(2 * a, 2 * b), g if k != 1 else f(a, b),
                       [f(2 * a + k, 2 * b + k), f(2 * a * k, b * k), f(a, 2 * b), f(2 * a, b * k)] + fc(a * k, b * k),
                       "%s = %s = %s (bagi atau kalikan pembilang dan penyebut dengan bilangan yang sama)." % (f(2 * a, 2 * b), f(a, b), g))
        bad = [f(a + k, b + k), f(a * k, b + k), f(a, b * k), f(b * k - a * k, b * k) if 2 * a != b else f(a * k + 1, b * k)]
        return mcq("Pecahan yang senilai dengan %s adalah …" % f(a, b), g, bad + fc(a * k, b * k),
                   "Kalikan pembilang dan penyebut dengan bilangan yang sama: %s." % ("%d × %d = %d, %d × %d = %d" % (a, k, a * k, b, k, b * k)))

    def bukan():
        a, b = ch(BASE + [(2, 7), (3, 8), (5, 8), (3, 10)])
        ks = R().sample([2, 3, 4, 5], 3)
        goods = [f(a * k, b * k) for k in ks]
        k = ri(2, 4)
        w = f(a + k, b + k)
        return mcq("Pecahan berikut yang <b>tidak</b> senilai dengan %s adalah …" % f(a, b), w, goods,
                   "%s didapat dengan menambah, bukan mengalikan. Pecahan senilai didapat dengan mengalikan pembilang dan penyebut dengan bilangan yang sama." % w)

    def sederhana():
        a, b = ch(BASE)
        k = ri(2, 5)
        return mcq("Bentuk paling sederhana dari %s adalah …" % f(a * k, b * k), f(a, b),
                   [f(a * k // 2, b * k // 2) if k % 2 == 0 and k > 2 else f(a, b * k), f(b, a) if a > 1 else f(a + 1, b), f(a * k, b)] + fc(a, b),
                   "Bagi pembilang dan penyebut dengan %d: %s." % (k, f(a, b)))

    def gambar():
        a, b = ch([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (1, 5), (3, 5), (4, 5), (1, 6), (5, 6)])
        k = ri(2, 4)
        if b * k > 16:
            return None
        p1, p2 = bar_frac(b, a, w=240, h=30), bar_frac(b * k, a * k, w=240, h=30)
        if R().random() < 0.5:
            return mcq("Kedua pita sama panjang. Pita atas menunjukkan %s. Pecahan pada pita bawah yang senilai adalah …%s%s" % (f(a, b), p1, p2),
                       f(a * k, b * k), [f(a, b * k), f(a * k, b), f(b * k - a * k, b * k) if 2 * a != b else f(a * k + 1, b * k)] + fc(a * k, b * k),
                       "Bagian yang diarsir sama panjang: %s = %s." % (f(a, b), f(a * k, b * k)))
        return mcq("Kedua pita sama panjang. Pita bawah menunjukkan %s. Pecahan pada pita atas yang senilai adalah …%s%s" % (f(a * k, b * k), p1, p2),
                   f(a, b), [f(a * k, b), f(a, b * k), f(b - a, b) if 2 * a != b else f(a + 1, b)] + fc(a, b),
                   "Bagian yang diarsir sama panjang: %s = %s." % (f(a * k, b * k), f(a, b)))

    def cerita():
        a, b = ch(BASE)
        k = ri(2, 3)
        x, y = K().two()
        food = ch(["roti", "kue lapis", "cokelat batang", "semangka", "martabak"])
        g = "Sama banyak"
        return mcq("%s memakan %s %s. %s memakan %s %s yang sama besar. Pernyataan yang benar adalah …" % (x, f(a, b), food, y, f(a * k, b * k), food),
                   g, ["%s makan lebih banyak" % x, "%s makan lebih banyak" % y, "%s makan dua kali lebih banyak" % y],
                   "%s = %s, jadi mereka makan sama banyak." % (f(a, b), f(a * k, b * k)))

    sets = [("Melengkapi pecahan senilai", [(isi_atas, 12), (isi_bawah, 8)]),
            ("Pecahan senilai dengan gambar", [(gambar, 14), (isi_atas, 6)]),
            ("Memilih pecahan senilai", [(pilih, 12), (bukan, 8)]),
            ("Bentuk paling sederhana", [(sederhana, 14), (pilih, 6)]),
            ("Soal cerita", [(cerita, 10), (bukan, 5), (isi_bawah, 5)])]
    body = lesson(
        ["Pecahan senilai adalah pecahan yang besarnya sama walaupun angkanya berbeda. " + f(1, 2) + " = " + f(2, 4) + " = " + f(4, 8) + ".",
         "Untuk mendapat pecahan senilai, kalikan (atau bagi) pembilang dan penyebut dengan bilangan yang sama.",
         "Bentuk paling sederhana didapat dengan membagi pembilang dan penyebut sampai tidak bisa dibagi lagi."],
        [example("%s = %s" % (f(2, 3), f("…", 12)), ["3 × 4 = 12", "2 × 4 = 8"], "8"),
         example("Sederhanakan %s." % f(6, 9), ["6 dan 9 sama-sama dibagi 3"], f(2, 3))],
        [["Menambahkan bilangan yang sama: %s = %s" % (f(1, 2), f(3, 4)), "Kalikan: %s = %s" % (f(1, 2), f(2, 4))],
         ["Hanya penyebut yang dikali", "Pembilang dan penyebut dikali bilangan yang sama"],
         ["Mengira %s lebih besar dari %s" % (f(4, 8), f(1, 2)), "Keduanya sama besar"]])
    faq = [{"q": "Apa itu pecahan senilai?", "a": "Pecahan-pecahan yang nilainya sama, misalnya 1/2, 2/4, 3/6, dan 4/8. Jika digambar pada pita yang sama panjang, bagian yang diarsir sama panjang."},
           {"q": "Bagaimana mencari pecahan senilai?", "a": "Kalikan pembilang dan penyebut dengan bilangan yang sama. Contoh: 2/5 = (2 × 3)/(5 × 3) = 6/15."},
           {"q": "Apa itu menyederhanakan pecahan?", "a": "Membagi pembilang dan penyebut dengan bilangan yang sama sampai tidak bisa dibagi lagi. Contoh: 8/12 = 2/3."}]
    return dict(slug="pecahan-senilai", dom="B", sort=9,
                std_text="Peserta didik dapat mengenali pecahan senilai menggunakan gambar dan simbol matematika.",
                title="Pecahan Senilai", short_title="Pecahan Senilai",
                meta_desc="Latihan pecahan senilai dengan gambar pita, melengkapi pecahan senilai, memilih pecahan yang senilai, dan menyederhanakan pecahan. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="1/2 = 2/4 = 4/8", key_sub="Kalikan pembilang dan penyebut dengan bilangan yang sama.",
                body=body, faq=faq, sets=sets)


# ============================================================ 10. desimal dan persen
def grid100(k, col="#7fb3d5"):
    s = []
    c = 18
    for i in range(100):
        r, q = divmod(i, 10)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='0.8'/>" % (6 + q * c, 6 + r * c, c, c, col if i < k else "#ffffff", INK))
    s.append("<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (10 * c, 10 * c, INK))
    return wrap(10 * c + 12, 10 * c + 12, "".join(s), "persegi dibagi 100 bagian, %d bagian diarsir" % k)


def u10():
    def persepuluh():
        k = ri(1, 9)
        if R().random() < 0.5:
            return mcq("<i>%s persepuluh</i> ditulis sebagai bilangan desimal …" % A.terbilang(k), "0,%d" % k, ["%d,0" % k, "0,0%d" % k, "%d,10" % k],
                       "%s persepuluh = %s = 0,%d." % (A.cap(A.terbilang(k)), f(k, 10), k))
        return mcq("%s dalam bentuk desimal adalah …" % f(k, 10), "0,%d" % k, ["%d,0" % k, "0,0%d" % k, "%d,10" % k],
                   "%s = %s persepuluh = 0,%d." % (f(k, 10), A.terbilang(k), k))

    def perseratus():
        k = ri(1, 99)
        if k % 10 == 0:
            return None
        d = "0,%02d" % k
        w = ["0,%d" % k if k >= 10 else "0,%d" % k, "%d,0" % k, "0,%03d" % k]
        return mcq("%s dalam bentuk desimal adalah …" % f(k, 100), d, w, "%s = %s perseratus = %s." % (f(k, 100), A.terbilang(k), d))

    def ke_pecahan():
        if R().random() < 0.5:
            k = ri(1, 9)
            return mcq("0,%d dalam bentuk pecahan adalah …" % k, f(k, 10), [f(k, 100), f(1, k) if k > 1 else f(10, k), f(k, 1)],
                       "Satu angka di belakang koma = persepuluhan: 0,%d = %s." % (k, f(k, 10)))
        k = ri(11, 99)
        if k % 10 == 0:
            return None
        return mcq("0,%02d dalam bentuk pecahan adalah …" % k, f(k, 100), [f(k, 10), f(k, 1000), f(100, k)],
                   "Dua angka di belakang koma = perseratusan: 0,%02d = %s." % (k, f(k, 100)))

    def kotak_desimal():
        k = ri(5, 95)
        if k % 10 == 0:
            return None
        return mcq("Persegi dibagi 100 bagian sama besar. Bagian yang diarsir dalam bentuk desimal adalah …" + grid100(k), "0,%02d" % k,
                   ["%d,0" % k, "0,%03d" % k, "0,%02d" % (100 - k)], "%d dari 100 bagian = %s = 0,%02d." % (k, f(k, 100), k))

    def kotak_persen():
        k = ri(5, 95)
        return mcq("Berapa persen bagian yang diarsir?" + grid100(k, "#f4a261"), "%d%%" % k, ["%d%%" % (100 - k), "%d%%" % (k + 10 if k < 90 else k - 10), "%d%%" % (k // 10 if k >= 20 else k + 1)],
                   "%d dari 100 bagian diarsir = %d%%." % (k, k))

    def persen_pecahan():
        k = ri(1, 99)
        if R().random() < 0.5:
            return mcq("%d%% = …" % k, f(k, 100), [f(k, 10), f(100, k), f(1, k)], "Persen berarti perseratus: %d%% = %s." % (k, f(k, 100)))
        return mcq("%s = …%%" % f(k, 100), "%d%%" % k, ["%d%%" % (100 - k), "%d%%" % (k * 10) if k * 10 < 1000 else "%d%%" % (k + 1), "%d%%" % (k + 10)],
                   "%s = %d perseratus = %d%%." % (f(k, 100), k, k))

    KN = [(1, 2, 50), (1, 4, 25), (3, 4, 75), (1, 5, 20), (2, 5, 40), (3, 5, 60), (4, 5, 80), (1, 10, 10), (3, 10, 30), (7, 10, 70), (9, 10, 90), (1, 20, 5), (1, 25, 4), (1, 50, 2)]

    def kenal():
        a, b, p = ch(KN)
        mode = ri(0, 2)
        if mode == 0:
            return mcq("%s = …%%" % f(a, b), "%d%%" % p, ["%d%%" % (a * 10 + b), "%d%%" % b, "%d%%" % (100 - p) if p != 50 else "%d%%" % (p + 5)],
                       "%s = %s = %d%%." % (f(a, b), f(p, 100), p))
        if mode == 1:
            return mcq("%s dalam bentuk desimal adalah …" % f(a, b), "0,%s" % ("%02d" % p).rstrip("0"), ["0,%d%d" % (a, b) if b < 10 else "0,%d" % a, "%d,%d" % (a, b), "0,0%d" % p if p >= 10 else "0,%d" % p],
                       "%s = %s = 0,%s." % (f(a, b), f(p, 100), ("%02d" % p).rstrip("0")))
        return mcq("%d%% sama dengan …" % p, f(a, b), [f(a, b + 1), f(p, 10), f(b, a) if a > 1 else f(1, p)],
                   "%d%% = %s = %s." % (p, f(p, 100), f(a, b)))

    def bandingkan():
        a, b = R().sample(range(1, 100), 2)
        sa, sb = "0,%02d" % a, "0,%02d" % b
        if R().random() < 0.5:
            sa = ("0,%02d" % a).rstrip("0") if a % 10 == 0 else sa
            sb = "%d%%" % b
        return stmt(sa, sb, a, b, "Ubah ke perseratus: %d dan %d perseratus." % (a, b))

    CT = [("Dari 100 siswa, %d siswa datang dengan sepeda.", "siswa"), ("Dari 100 bibit, %d bibit tumbuh.", "bibit"),
          ("Dari 100 soal, %s menjawab %d soal dengan benar.", "soal"), ("Dari 100 butir telur, %d butir berwarna cokelat.", "butir")]

    def cerita():
        k = ri(11, 99)
        t, _ = ch(CT)
        t = t % ((K().next(), k) if "%s" in t else (k,))
        if R().random() < 0.5:
            return mcq(t + " Berapa persen itu?", "%d%%" % k, ["%d%%" % (100 - k), "%d%%" % (k // 10 + 1), "%d%%" % (k + 10 if k < 90 else k - 10)],
                       "%d dari 100 = %d%%." % (k, k))
        return mcq(t + " Bilangan desimal yang menunjukkan bagian itu adalah …", "0,%02d" % k if k % 10 else "0,%d" % (k // 10),
                   ["%d,0" % k, "0,%03d" % k, "0,%02d" % (100 - k) if (100 - k) % 10 else "0,%d" % ((100 - k) // 10)],
                   "%d dari 100 = %s." % (k, f(k, 100)))

    sets = [("Desimal persepuluhan", [(persepuluh, 10), (ke_pecahan, 10)]),
            ("Desimal perseratusan", [(perseratus, 10), (kotak_desimal, 10)]),
            ("Persen", [(kotak_persen, 10), (persen_pecahan, 10)]),
            ("Pecahan, desimal, dan persen", [(kenal, 14), (bandingkan, 6)]),
            ("Soal cerita", [(cerita, 14), (kenal, 6)])]
    body = lesson(
        ["Pecahan berpenyebut 10 dapat ditulis sebagai desimal dengan satu angka di belakang koma: %s = 0,3." % f(3, 10),
         "Pecahan berpenyebut 100 ditulis dengan dua angka di belakang koma: %s = 0,47." % f(47, 100),
         "Persen (%) berarti perseratus. 47% = " + f(47, 100) + " = 0,47."],
        [example("%s = …%%" % f(3, 4), ["%s = %s" % (f(3, 4), f(75, 100)), "75 perseratus = 75%"], "75%"),
         example("Tulis 0,08 sebagai pecahan.", ["Dua angka di belakang koma → perseratus", "0,08 = 8 perseratus"], f(8, 100))],
        [["%s ditulis 0,7 (padahal 7 perseratus)" % f(7, 100), "%s = 0,07" % f(7, 100)],
         ["0,5 dibaca nol koma lima, lalu ditulis %s" % f(5, 100), "0,5 = %s = %s" % (f(5, 10), f(50, 100))],
         ["%s ditulis 12%%" % f(1, 2), "%s = %s = 50%%" % (f(1, 2), f(50, 100))]])
    faq = [{"q": "Apa hubungan pecahan, desimal, dan persen?", "a": "Ketiganya cara menulis bagian dari keseluruhan. Contoh: 1/4 = 25/100 = 0,25 = 25%."},
           {"q": "Bagaimana mengubah pecahan menjadi persen?", "a": "Ubah pecahan menjadi pecahan berpenyebut 100. Pembilangnya adalah persennya. Contoh: 3/5 = 60/100 = 60%."},
           {"q": "Mengapa desimal di Indonesia memakai koma?", "a": "Di Indonesia, tanda koma dipakai untuk desimal (0,5) dan tanda titik dipakai untuk pemisah ribuan (1.000)."}]
    return dict(slug="desimal-dan-persen", dom="B", sort=10,
                std_text="Peserta didik mengenali bilangan desimal dan persen serta hubungannya dengan pecahan (persepuluhan dan perseratusan).",
                title="Desimal dan Persen", short_title="Desimal dan Persen",
                meta_desc="Latihan mengubah pecahan persepuluhan dan perseratusan menjadi desimal, mengenal persen dengan gambar petak 100, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="47% = 47/100 = 0,47", key_sub="Persen berarti perseratus.",
                body=body, faq=faq, sets=sets)


# ============================================================ 11. kalimat matematika
BOX = "<span style='display:inline-block;width:1.4em;border:2px solid #333;border-radius:3px'>&nbsp;</span>"


def u11():
    def a_plus():
        a, c = ri(11, 80), ri(30, 100)
        b = c - a
        if b < 5:
            return None
        if R().random() < 0.5:
            q = "%d + %s = %d" % (a, BOX, c)
        else:
            q = "%s + %d = %d" % (BOX, a, c)
        return mcq("Bilangan yang tepat untuk kotak adalah …<br>" + q, str(b), [str(a + c) if a + c <= 200 else str(b + 10), str(b + 1), str(b - 10) if b > 10 else str(b + 2)],
                   "%d − %d = %d. Periksa: %d + %d = %d." % (c, a, b, a, b, c))

    def a_minus():
        a, b = ri(30, 100), ri(5, 60)
        if b >= a:
            return None
        c = a - b
        if R().random() < 0.5:
            return mcq("Bilangan yang tepat untuk kotak adalah …<br>%d − %s = %d" % (a, BOX, c), str(b), [str(a + c) if a + c <= 200 else str(b + 10), str(b + 1), str(b + 10)],
                       "%d − %d = %d. Periksa: %d − %d = %d." % (a, c, b, a, b, c))
        return mcq("Bilangan yang tepat untuk kotak adalah …<br>%s − %d = %d" % (BOX, b, c), str(a), [str(c - b) if c > b else str(a + 2), str(a + 1), str(a - 10)],
                   "%d + %d = %d. Periksa: %d − %d = %d." % (c, b, a, a, b, c))

    def dua_sisi():
        a, b = ri(10, 50), ri(10, 40)
        c = ri(5, a + b - 5)
        d = a + b - c
        return mcq("Bilangan yang tepat untuk kotak adalah …<br>%d + %d = %s + %d" % (a, b, BOX, c), str(d), [str(a + b), str(a + b + c), str(d + 1)],
                   "%d + %d = %d. Jadi %s + %d = %d, kotak = %d." % (a, b, a + b, BOX, c, a + b, d))

    SC = [("%s punya %d kelereng. Ia mendapat lagi beberapa kelereng, sekarang kelerengnya %d.", "+", "kelereng"),
          ("Di bus ada %d penumpang. Di halte naik beberapa penumpang, sekarang ada %d penumpang.", "+", "penumpang"),
          ("%s punya %d stiker. Beberapa stiker diberikan kepada adiknya, sisanya %d stiker.", "-", "stiker"),
          ("Di pohon ada %d burung. Beberapa burung terbang, tinggal %d burung.", "-", "burung"),
          ("%s sudah membaca %d halaman buku. Setelah membaca lagi, ia sudah membaca %d halaman.", "+", "halaman"),
          ("Bu Tini membuat %d kue. Sebagian terjual, sisanya %d kue.", "-", "kue")]

    def model():
        t, op, unit = ch(SC)
        a, c = ri(20, 60), ri(20, 60)
        if op == "+":
            c = a + ri(8, 35)
            good = "%d + %s = %d" % (a, BOX, c)
            bad = ["%d − %s = %d" % (a, BOX, c), "%d + %d = %s" % (a, c, BOX), "%s − %d = %d" % (BOX, a, c)]
        else:
            a = c + ri(8, 35)
            good = "%d − %s = %d" % (a, BOX, c)
            bad = ["%d + %s = %d" % (a, BOX, c), "%d + %d = %s" % (a, c, BOX), "%s − %d = %d" % (BOX, a, c)]
        args = (K().next(), a, c) if t.startswith("%s") else (a, c)
        return mcq((t % args) + " Kalimat matematika yang tepat adalah …", good, bad,
                   "Kotak adalah banyak %s yang %s." % (unit, "ditambahkan" if op == "+" else "berkurang"))

    def selesai():
        t, op, unit = ch(SC)
        a = ri(20, 60)
        b = ri(8, 35)
        c = a + b if op == "+" else a - b
        args = (K().next(), a, c) if t.startswith("%s") else (a, c)
        tail = "Berapa %s yang %s?" % (unit, "bertambah" if op == "+" else "berkurang")
        return mcq((t % args) + " " + tail, u(b, unit), [u(a + c, unit), u(b + 10, unit), u(b - 1, unit)],
                   "%s: %d − %d = %d." % ("%d + %s = %d" % (a, BOX, c) if op == "+" else "%d − %s = %d" % (a, BOX, c), max(a, c), min(a, c), b))

    def benar():
        a, b = ri(10, 60), ri(5, 39)
        if a == b:
            return None
        c = a + b
        good = ch(["%d − %d = %d" % (c, a, b), "%d − %d = %d" % (c, b, a), "%d + %d = %d" % (b, a, c)])
        bad = ["%d − %d = %d" % (a, b, c), "%d + %d = %d" % (c, a, b), "%d − %d = %d" % (b, c, a), "%d − %d = %d" % (c, a, c - a + 10)]
        return mcq("Diketahui %d + %d = %d. Kalimat matematika berikut yang juga benar adalah …" % (a, b, c), good, bad,
                   "Penjumlahan dan pengurangan saling berkebalikan: dari %d + %d = %d didapat %d − %d = %d dan %d − %d = %d."
                   % (a, b, c, c, a, b, c, b, a))

    sets = [("Kotak pada penjumlahan", [(a_plus, 20)]),
            ("Kotak pada pengurangan", [(a_minus, 20)]),
            ("Kalimat yang benar", [(benar, 10), (dua_sisi, 10)]),
            ("Membuat kalimat matematika", [(model, 20)]),
            ("Soal cerita", [(selesai, 14), (a_plus, 3), (a_minus, 3)])]
    body = lesson(
        ["Kalimat matematika seperti 25 + %s = 40 punya satu bilangan yang belum diketahui." % BOX,
         "Gunakan hubungan penjumlahan dan pengurangan: 25 + %s = 40 berarti %s = 40 − 25 = 15." % (BOX, BOX),
         "Selalu periksa: masukkan jawabanmu ke kotak, lalu hitung lagi."],
        [example("%s − 18 = 27" % BOX, ["Bilangan awal dikurangi 18 menjadi 27", "Jadi bilangan awal = 27 + 18"], "45"),
         example("60 − %s = 35" % BOX, ["60 − 35 = 25", "Periksa: 60 − 25 = 35"], "25")],
        [["25 + %s = 40, kotak diisi 65" % BOX, "Kurangkan: 40 − 25 = 15"],
         ["%s − 18 = 27, kotak diisi 9" % BOX, "Bilangan awal lebih besar: 27 + 18 = 45"],
         ["Tidak memeriksa jawaban", "Masukkan jawaban ke kotak dan hitung ulang"]])
    faq = [{"q": "Apa itu kalimat matematika?", "a": "Kalimat yang memakai bilangan dan tanda operasi, misalnya 34 + 15 = 49. Jika ada bilangan yang belum diketahui, kita tulis dengan kotak."},
           {"q": "Bagaimana mencari bilangan di dalam kotak?", "a": "Gunakan kebalikan operasinya. Untuk penjumlahan, kurangkan. Untuk pengurangan, lihat apakah kotak ada di depan (tambahkan) atau di belakang tanda minus (kurangkan)."},
           {"q": "Bagaimana membuat kalimat matematika dari soal cerita?", "a": "Tulis bilangan yang diketahui sesuai urutan cerita, beri kotak untuk bilangan yang ditanyakan, lalu pilih tanda tambah atau kurang."}]
    return dict(slug="kalimat-matematika", dom="A", sort=11,
                std_text="Peserta didik dapat mengisi nilai yang belum diketahui dalam sebuah kalimat matematika yang berkaitan dengan penjumlahan dan pengurangan pada bilangan cacah sampai 100.",
                title="Kalimat Matematika: Mencari Bilangan yang Belum Diketahui", short_title="Kalimat Matematika",
                meta_desc="Latihan mencari bilangan yang belum diketahui pada kalimat matematika penjumlahan dan pengurangan sampai 100, menulis kalimat matematika dari soal cerita. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="25 + □ = 40 → □ = 15", key_sub="Gunakan kebalikan operasinya, lalu periksa.",
                body=body, faq=faq, sets=sets)


# ============================================================ 12. pola gambar dan pola bilangan
SH = [("lingkaran", "circle"), ("segitiga", "tri"), ("persegi", "sq"), ("bintang", "star")]
CO = [("merah", "#e15759"), ("biru", "#4e79a7"), ("hijau", "#59a14f"), ("kuning", "#edc948")]


def shape(kind, cx, cy, col, r=15):
    if kind == "circle":
        return "<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, r, col, INK)
    if kind == "sq":
        return "<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx - r, cy - r, 2 * r, 2 * r, col, INK)
    if kind == "tri":
        return "<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy - r, cx + r, cy + r, cx - r, cy + r, col, INK)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(pts), col, INK)


def u12():
    def naik():
        step = ri(2, 12)
        a = ri(1, 40)
        n = 5
        seq = [a + step * i for i in range(n + 1)]
        if seq[-1] > 100:
            return None
        return mcq("Bilangan berikutnya pada pola %s, … adalah …" % ", ".join(map(str, seq[:n])), str(seq[n]),
                   [str(seq[n] + 1), str(seq[n] - step + 1), str(seq[n] + step)], "Polanya ditambah %d: %d + %d = %d." % (step, seq[n - 1], step, seq[n]))

    def turun():
        step = ri(2, 12)
        a = ri(50, 100)
        seq = [a - step * i for i in range(6)]
        if seq[-1] < 0:
            return None
        return mcq("Bilangan berikutnya pada pola %s, … adalah …" % ", ".join(map(str, seq[:5])), str(seq[5]),
                   [str(seq[5] - 1), str(seq[4] + step), str(seq[5] + 1)], "Polanya dikurangi %d: %d − %d = %d." % (step, seq[4], step, seq[5]))

    def tengah():
        step = ri(3, 15) * ch([1, -1])
        a = ri(5, 40) if step > 0 else ri(60, 100)
        seq = [a + step * i for i in range(5)]
        if min(seq) < 0 or max(seq) > 100:
            return None
        i = ri(1, 3)
        show = [str(x) if j != i else BOX for j, x in enumerate(seq)]
        return mcq("Bilangan yang tepat untuk kotak pada pola ini adalah …<br>%s" % ", ".join(show), str(seq[i]),
                   [str(seq[i] + 1), str(seq[i] - 1), str(seq[i] + step) if i < 4 else str(seq[i] + 2)],
                   "Setiap langkah %s %d." % ("ditambah" if step > 0 else "dikurangi", abs(step)))

    def aturan():
        step = ri(2, 12) * ch([1, -1])
        a = ri(5, 40) if step > 0 else ri(60, 100)
        seq = [a + step * i for i in range(4)]
        if min(seq) < 0 or max(seq) > 100:
            return None
        s = abs(step)
        g = ("ditambah %d" if step > 0 else "dikurangi %d") % s
        bad = [("dikurangi %d" if step > 0 else "ditambah %d") % s, ("ditambah %d" if step > 0 else "dikurangi %d") % (s + 1),
               ("ditambah %d" if step > 0 else "dikurangi %d") % (s - 1 if s > 2 else s + 2)]
        return mcq("Aturan pola %s adalah …" % ", ".join(map(str, seq)), g, bad, "%d %s %d = %d." % (seq[0], "+" if step > 0 else "−", s, seq[1]))

    def gambar():
        L = ch([2, 3, 4])
        unit_ = R().sample(range(16), L)
        items = [(SH[x % 4], CO[x // 4]) for x in unit_]
        shown = ri(L * 2, min(L * 2 + L - 1, 9))
        seq = [items[i % L] for i in range(shown)]
        nxt = items[shown % L]
        s = [shape(sh[1], 22 + i * 40, 24, co[1]) for i, (sh, co) in enumerate(seq)]
        x = 22 + shown * 40
        s.append("<rect x='%d' y='6' width='36' height='36' rx='4' fill='#fff' stroke='%s' stroke-dasharray='4 3' stroke-width='1.5'/>" % (x - 18, INK))
        s.append(text(x, 31, "?", 18))
        pic = wrap(x + 26, 50, "".join(s), "pola gambar")
        name = lambda it: "%s %s" % (it[0][0], it[1][0])
        cands = [name(it) for it in items if it != nxt]
        cands += [name((sh, co)) for sh in SH for co in CO if (sh, co) not in items]
        R().shuffle(cands)
        return mcq("Gambar berikutnya pada pola ini adalah …" + pic, name(nxt), cands,
                   "Pola berulang setiap %d gambar. Setelah %s datang %s." % (L, name(seq[-1]), name(nxt)))

    def tumbuh():
        a = ri(1, 4)
        d = ri(1, 4)
        k = ri(5, 8)
        cnt = [a + d * i for i in range(4)]
        s, x = [], 8
        for i, c in enumerate(cnt[:3]):
            for t in range(c):
                s.append("<rect x='%d' y='%d' width='12' height='12' fill='#f2c94c' stroke='%s'/>" % (x + (t % 5) * 14, 8 + (t // 5) * 14, INK))
            s.append(text(x + min(c, 5) * 7, 8 + ((c - 1) // 5 + 1) * 14 + 16, "ke-%d" % (i + 1), 12, weight=600))
            x += min(c, 5) * 14 + 24
        h = 8 + ((cnt[2] - 1) // 5 + 1) * 14 + 24
        pic = wrap(x, h, "".join(s), "pola persegi")
        v = a + d * (k - 1)
        return mcq("Pola ke-1 punya %d persegi, ke-2 punya %d, dan ke-3 punya %d. Berapa banyak persegi pada pola ke-%d?" % (cnt[0], cnt[1], cnt[2], k) + pic,
                   str(v), [str(v + d), str(v - d), str(a * k)], "Setiap pola bertambah %d persegi: %d + %d × %d = %d." % (d, a, k - 1, d, v))

    def cerita():
        who = K().next()
        a = ri(5, 30) * ch([1, 2])
        d = ri(2, 10)
        k = ri(4, 7)
        if a + d * (k - 1) > 100:
            return None
        if R().random() < 0.5:
            v = a + d * (k - 1)
            return mcq("%s menabung %s. Minggu pertama tabungannya %d ribu rupiah, dan setiap minggu bertambah %d ribu rupiah. Berapa ribu rupiah tabungannya pada minggu ke-%d?"
                       % (who, "setiap minggu", a, d, k), str(v), [str(v + d), str(a + d * k), str(a * k)],
                       "%s → tambah %d setiap minggu: %d." % (", ".join(str(a + d * i) for i in range(3)) + ", …", d, v))
        a = ri(60, 100)
        v = a - d * (k - 1)
        if v < 0:
            return None
        return mcq("Sebuah toko punya %d karung beras. Setiap hari terjual %d karung. Berapa karung yang tersisa pada hari ke-%d (setelah penjualan hari itu)?"
                   % (a, d, k - 1), str(v), [str(v + d), str(v - d), str(a - d * k + d * 2)],
                   "%d − %d × %d = %d." % (a, k - 1, d, v))

    sets = [("Pola bilangan naik", [(naik, 14), (tengah, 6)]),
            ("Pola bilangan turun", [(turun, 14), (tengah, 6)]),
            ("Aturan pola", [(aturan, 14), (tengah, 6)]),
            ("Pola gambar", [(gambar, 12), (tumbuh, 8)]),
            ("Soal cerita", [(cerita, 14), (tumbuh, 6)])]
    body = lesson(
        ["Pola bilangan naik bertambah dengan bilangan yang sama setiap langkah: 4, 7, 10, 13, … (ditambah 3).",
         "Pola bilangan turun berkurang dengan bilangan yang sama: 50, 45, 40, 35, … (dikurangi 5).",
         "Pada pola gambar, cari bagian yang berulang. Lalu lanjutkan bagian itu."],
        [example("Lanjutkan: 12, 19, 26, 33, …", ["19 − 12 = 7, 26 − 19 = 7", "Aturannya ditambah 7"], "40"),
         example("Lanjutkan: 90, 82, 74, 66, …", ["Setiap langkah dikurangi 8"], "58")],
        [["Hanya melihat dua bilangan pertama", "Periksa selisih semua bilangan yang berurutan"],
         ["Pola turun dikira ditambah", "Jika bilangannya mengecil, aturannya dikurangi"],
         ["Pada pola gambar hanya melihat bentuk", "Perhatikan bentuk dan warnanya"]])
    faq = [{"q": "Bagaimana menemukan aturan pola bilangan?", "a": "Hitung selisih dua bilangan yang berurutan. Jika selisihnya selalu sama, itulah aturannya. Bilangan makin besar berarti ditambah, makin kecil berarti dikurangi."},
           {"q": "Apa itu pola gambar berulang?", "a": "Pola yang bagian-bagiannya muncul lagi dengan urutan yang sama, misalnya merah, biru, merah, biru, …"},
           {"q": "Bagaimana mencari suku ke-10 tanpa menulis semuanya?", "a": "Mulai dari suku pertama, lalu tambahkan aturannya sebanyak 9 kali. Contoh: 3, 5, 7, … suku ke-10 = 3 + 9 × 2 = 21."}]
    return dict(slug="pola-gambar-dan-pola-bilangan", dom="A", sort=12,
                std_text="Peserta didik dapat mengidentifikasi, meniru, dan mengembangkan pola gambar atau objek sederhana dan pola bilangan membesar dan mengecil yang melibatkan penjumlahan dan pengurangan pada bilangan cacah sampai 100.",
                title="Pola Gambar dan Pola Bilangan", short_title="Pola Gambar dan Pola Bilangan",
                meta_desc="Latihan pola bilangan naik dan turun sampai 100, menemukan aturan pola, melanjutkan pola gambar, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Cari aturannya", key_sub="Hitung selisih bilangan yang berurutan.",
                body=body, faq=faq, sets=sets)


# ============================================================ 13. panjang dan berat
def penggaris(a, b, obj="pensil"):
    """penggaris 0–15 cm; benda dari a sampai b"""
    c = 26
    s = []
    x0 = 14
    s.append("<rect x='%d' y='44' width='%d' height='40' fill='#fdf3c7' stroke='%s' stroke-width='1.5'/>" % (x0 - 8, 15 * c + 16, INK))
    for i in range(0, 151):
        x = x0 + i * c / 10.0
        h = 14 if i % 10 == 0 else 9 if i % 5 == 0 else 5
        s.append(line(x, 44, x, 44 + h, INK, 1.4 if i % 10 == 0 else 0.8))
        if i % 10 == 0:
            s.append(text(x, 74, str(i // 10), 12, weight=600))
    xa, xb = x0 + a * c, x0 + b * c
    col = {"pensil": "#f2c94c", "pita": "#e15759", "paku": "#9aa5b1", "krayon": "#4e79a7", "sedotan": "#59a14f", "kunci": "#c9a227"}.get(obj, "#f2c94c")
    s.append("<rect x='%.1f' y='18' width='%.1f' height='16' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>" % (xa, xb - xa, col, INK))
    s.append(line(xa, 18, xa, 44, "#999", 1, " stroke-dasharray='3 2'"))
    s.append(line(xb, 18, xb, 44, "#999", 1, " stroke-dasharray='3 2'"))
    return wrap(15 * c + 28, 90, "".join(s), "%s di atas penggaris" % obj, lg=True)


def u13():
    def m_cm():
        m, cm = ri(1, 9), ri(0, 99)
        mode = ri(0, 2)
        if mode == 0:
            return mcq("%d m = … cm" % m, str(m * 100), [str(m * 10), str(m * 1000), str(m)], "1 m = 100 cm, jadi %d m = %d cm." % (m, m * 100))
        if cm == 0 or cm % 10 == 0 and R().random() < 0.5:
            return None
        if mode == 1:
            return mcq("%d m %d cm = … cm" % (m, cm), num(m * 100 + cm), [str(m * 10 + cm), num(m * 1000 + cm), str(m + cm)],
                       "%d m = %d cm, ditambah %d cm = %d cm." % (m, m * 100, cm, m * 100 + cm))
        t = m * 100 + cm
        return mcq("%s cm = … m … cm" % num(t), "%d m %d cm" % (m, cm), ["%d m %d cm" % (t // 10, t % 10), "%d m %d cm" % (m * 10 + cm // 10, cm % 10) if cm >= 10 else "%d m %d cm" % (m + 1, cm), "%d m %d cm" % (cm, m)],
                   "%s cm = %d cm + %d cm = %d m %d cm." % (num(t), m * 100, cm, m, cm))

    def kg_g():
        kg, g = ri(1, 9), ri(1, 999)
        mode = ri(0, 2)
        if mode == 0:
            return mcq("%d kg = … g" % kg, num(kg * 1000), [num(kg * 100), num(kg * 10), num(kg * 10000)], "1 kg = 1.000 g, jadi %d kg = %s g." % (kg, num(kg * 1000)))
        if mode == 1:
            return mcq("%d kg %d g = … g" % (kg, g), num(kg * 1000 + g), [num(kg * 100 + g), num(kg + g), num(kg * 1000 + g * 10) if g < 100 else num(kg * 1000 + g + 1000)],
                       "%d kg = %s g, ditambah %d g = %s g." % (kg, num(kg * 1000), g, num(kg * 1000 + g)))
        t = kg * 1000 + g
        return mcq("%s g = … kg … g" % num(t), "%d kg %d g" % (kg, g), ["%d kg %d g" % (t // 100, t % 100), "%d kg %d g" % (g, kg), "%d kg %d g" % (kg + 1, g)],
                   "%s g = %s g + %d g = %d kg %d g." % (num(t), num(kg * 1000), g, kg, g))

    OBJ = ["pensil", "pita", "paku", "krayon", "sedotan", "kunci"]

    def ukur():
        a = ch([0, 0, 0, 1, 2, 3])
        L = ri(3, 12 - a)
        obj = ch(OBJ)
        b = a + L
        bad = [str(b) + " cm", str(L + 1) + " cm", str(L - 1) + " cm"]
        return mcq("Berapa panjang %s ini?" % obj + penggaris(a, b, obj), "%d cm" % L, bad,
                   ("Ujung %s ada di angka 0 dan %d, jadi panjangnya %d cm." % (obj, b, L)) if a == 0 else
                   ("%s mulai dari angka %d sampai %d: %d − %d = %d cm." % (obj.capitalize(), a, b, b, a, L)))

    def banding():
        if R().random() < 0.5:
            m, cm = ri(1, 4), ri(5, 95)
            t = ri(100, 499)
            a = m * 100 + cm
            if a == t:
                return None
            return stmt("%d m %d cm" % (m, cm), "%s cm" % num(t), a, t, "Ubah ke cm: %d m %d cm = %d cm." % (m, cm, a))
        kg, g = ri(1, 4), ri(50, 950)
        t = ri(1000, 4999)
        a = kg * 1000 + g
        if a == t:
            return None
        return stmt("%d kg %d g" % (kg, g), "%s g" % num(t), a, t, "Ubah ke gram: %d kg %d g = %s g." % (kg, g, num(a)))

    SAT = [("panjang sebatang pensil", "cm"), ("panjang penghapus", "cm"), ("lebar buku tulis", "cm"), ("tinggi pintu kelas", "m"),
           ("panjang lapangan sepak bola", "m"), ("tinggi pohon kelapa", "m"), ("berat sebutir telur", "g"), ("berat sebuah semangka", "kg"),
           ("berat sekarung beras", "kg"), ("berat sebuah pensil", "g"), ("berat seorang anak kelas 4", "kg"), ("berat sebungkus permen", "g"),
           ("panjang sebuah paku", "cm"), ("panjang kolam renang", "m"), ("berat sebuah kelereng", "g"), ("berat sebuah sepeda", "kg")]

    def satuan():
        what, g = ch(SAT)
        return mcq("Satuan yang paling tepat untuk mengukur %s adalah …" % what, g, [x for x in ["cm", "m", "g", "kg"] if x != g],
                   "Untuk %s kita pakai %s." % (what, g))

    def cerita():
        x, y = K().two()
        if R().random() < 0.5:
            a, b = ri(110, 180), ri(100, 170)
            if a == b:
                return None
            ma, ca = divmod(a, 100)
            d = abs(a - b)
            return mcq("Tinggi badan %s %d m %d cm. Tinggi badan %s %d cm. Berapa selisih tinggi mereka?" % (x, ma, ca, y, b),
                       "%d cm" % d, ["%d cm" % (a + b), "%d cm" % abs(ca - b), "%d cm" % (d + 10)],
                       "%d m %d cm = %d cm. Selisih = %d cm." % (ma, ca, a, d))
        if R().random() < 0.5:
            a, b = ri(1, 3) * 1000 + ri(1, 9) * 100, ri(1, 9) * 100 + ri(0, 9) * 10
            t = a + b
            return mcq("Ibu membeli %d kg %d g daging dan %d g ikan. Berapa gram berat belanjaan itu?" % (a // 1000, a % 1000, b),
                       "%s g" % num(t), ["%s g" % num(a // 1000 * 100 + a % 1000 + b), "%s g" % num(t + 1000), "%s g" % num(abs(a - b))],
                       "%d kg %d g = %s g. %s + %d = %s g." % (a // 1000, a % 1000, num(a), num(a), b, num(t)))
        L = ri(2, 5) * 100
        k = ch([2, 4, 5])
        return mcq("Pita sepanjang %d m dipotong menjadi %d bagian sama panjang. Berapa cm panjang setiap potongan?" % (L // 100, k),
                   "%d cm" % (L // k), ["%d cm" % (L // 100 * k), "%d cm" % (L // k // 10), "%d cm" % (L - k)],
                   "%d m = %d cm. %d : %d = %d cm." % (L // 100, L, L, k, L // k))

    sets = [("Meter dan sentimeter", [(m_cm, 20)]),
            ("Kilogram dan gram", [(kg_g, 20)]),
            ("Mengukur dengan penggaris", [(ukur, 20)]),
            ("Membandingkan dan memilih satuan", [(banding, 12), (satuan, 8)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Panjang diukur dengan satuan baku sentimeter (cm) dan meter (m). 1 m = 100 cm.",
         "Berat diukur dengan gram (g) dan kilogram (kg). 1 kg = 1.000 g.",
         "Saat mengukur dengan penggaris, letakkan ujung benda di angka 0. Jika tidak di 0, kurangkan angka akhir dengan angka awal."],
        [example("2 m 35 cm = … cm", ["2 m = 200 cm", "200 cm + 35 cm"], "235 cm"),
         example("3.450 g = … kg … g", ["3.000 g = 3 kg", "sisa 450 g"], "3 kg 450 g")],
        [["1 m = 10 cm", "1 m = 100 cm"],
         ["1 kg = 100 g", "1 kg = 1.000 g"],
         ["Benda dari angka 2 sampai 9 dibaca 9 cm", "Panjangnya 9 − 2 = 7 cm"]])
    faq = [{"q": "Berapa sentimeter dalam satu meter?", "a": "1 meter sama dengan 100 sentimeter. Jadi 3 m = 300 cm dan 4 m 25 cm = 425 cm."},
           {"q": "Berapa gram dalam satu kilogram?", "a": "1 kilogram sama dengan 1.000 gram. Jadi 2 kg 500 g = 2.500 g."},
           {"q": "Kapan memakai gram dan kapan kilogram?", "a": "Gram untuk benda ringan, misalnya telur atau pensil. Kilogram untuk benda berat, misalnya beras, semangka, atau berat badan."}]
    return dict(slug="pengukuran-panjang-dan-berat", dom="P", sort=13,
                std_text="Peserta didik dapat mengukur panjang dan berat benda menggunakan satuan baku, serta menentukan hubungan antarsatuan baku panjang (cm, m) dan berat (g, kg).",
                title="Mengukur Panjang dan Berat", short_title="Pengukuran Panjang dan Berat",
                meta_desc="Latihan mengubah satuan m dan cm, kg dan g, mengukur dengan penggaris, membandingkan panjang dan berat, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="1 m = 100 cm, 1 kg = 1.000 g", key_sub="Ubah ke satuan yang sama sebelum membandingkan.",
                body=body, faq=faq, sets=sets)


# ============================================================ 14. luas dan volume
def petak(cells, W=10, H=7, col="#a8d5ba"):
    c = 22
    s = []
    for i in range(W + 1):
        s.append(line(6 + i * c, 6, 6 + i * c, 6 + H * c, "#bcd6e6", 1))
    for j in range(H + 1):
        s.append(line(6, 6 + j * c, 6 + W * c, 6 + j * c, "#bcd6e6", 1))
    for (x, y) in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>" % (6 + x * c, 6 + y * c, c, c, col, GREEN))
    return wrap(W * c + 12, H * c + 12, "".join(s), "bangun pada kertas berpetak")


def rect_cells(x, y, w, h):
    return [(x + i, y + j) for i in range(w) for j in range(h)]


def shape_cells():
    kind = ri(0, 2)
    if kind == 0:
        w, h = ri(2, 8), ri(2, 6)
        return rect_cells(ri(0, 9 - w), ri(0, 6 - h), w, h)
    if kind == 1:
        w, h = ri(3, 7), ri(3, 6)
        cw, chh = ri(1, w - 1), ri(1, h - 1)
        x0, y0 = ri(0, 9 - w), ri(0, 6 - h)
        return [c for c in rect_cells(x0, y0, w, h) if not (c[0] >= x0 + w - cw and c[1] < y0 + chh)]
    cells = set()
    x, y = ri(1, 3), ri(1, 2)
    for _ in range(ri(6, 14)):
        cells.add((x, y))
        dx, dy = ch([(1, 0), (0, 1), (-1, 0), (0, -1), (1, 0)])
        x, y = min(max(x + dx, 0), 9), min(max(y + dy, 0), 6)
    return sorted(cells)


def kubus(a, b, c, s=22):
    """balok dari a × b × c kubus satuan (isometrik)"""
    ox = b * s * 0.866 + 10
    oy = c * s + 10
    P = lambda x, y, z: (ox + (x - y) * s * 0.866, oy + (x + y) * s * 0.5 - z * s)
    out = []
    cubes = sorted([(i, j, k) for i in range(a) for j in range(b) for k in range(c)], key=lambda t: (t[0] + t[1] + t[2], t[2]))
    for i, j, k in cubes:
        faces = [([(i, j, k + 1), (i + 1, j, k + 1), (i + 1, j + 1, k + 1), (i, j + 1, k + 1)], "#fbe3a6"),
                 ([(i + 1, j, k), (i + 1, j + 1, k), (i + 1, j + 1, k + 1), (i + 1, j, k + 1)], "#e9b949"),
                 ([(i, j + 1, k), (i + 1, j + 1, k), (i + 1, j + 1, k + 1), (i, j + 1, k + 1)], "#f2cf72")]
        for pts, col in faces:
            out.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1'/>" % (" ".join("%.1f,%.1f" % P(*p) for p in pts), col, INK))
    W = (a + b) * s * 0.866 + 20
    H = (a + b) * s * 0.5 + c * s + 20
    return wrap(W, H, "".join(out), "balok dari %d kubus satuan" % (a * b * c))


def u14():
    def hitung():
        cells = shape_cells()
        n = len(cells)
        return mcq("Setiap petak adalah 1 petak satuan. Berapa luas bangun yang diarsir?" + petak(cells), "%d petak satuan" % n,
                   ["%d petak satuan" % x for x in (n + 1, n - 1, n + 2, 2 * n)], "Hitung semua petak yang diarsir: %d petak." % n)

    def persegi_panjang():
        w, h = ri(2, 9), ri(2, 9)
        if w == h and R().random() < 0.5:
            return None
        return mcq("Sebuah persegi panjang digambar pada kertas berpetak 1 cm. Panjangnya %d petak dan lebarnya %d petak. Berapa luasnya?" % (w, h),
                   "%d cm²" % (w * h), ["%d cm²" % (w + h), "%d cm²" % (2 * (w + h)), "%d cm²" % (w * h + w)],
                   "Ada %d baris, setiap baris %d petak: %d × %d = %d petak = %d cm²." % (h, w, h, w, w * h, w * h))

    def banding():
        a, b = shape_cells(), shape_cells()
        if len(a) == len(b):
            return None
        pa, pb = petak(a, col="#a8d5ba"), petak(b, col="#f4c095")
        big = "Bangun A" if len(a) > len(b) else "Bangun B"
        return mcq("Manakah yang lebih luas?<br>Bangun A:%sBangun B:%s" % (pa, pb), big,
                   ["Bangun B" if big == "Bangun A" else "Bangun A", "Sama luas", "Tidak bisa dibandingkan"],
                   "Bangun A = %d petak, bangun B = %d petak." % (len(a), len(b)))

    def vol():
        a, b, c = ri(1, 4), ri(1, 3), ri(1, 4)
        n = a * b * c
        if n < 4:
            return None
        vis = a * b + b * c + a * c
        bad = [vis, a * b, n + a, n - b, a + b + c]
        return mcq("Berapa banyak kubus satuan yang menyusun balok ini?" + kubus(a, b, c), "%d kubus" % n, ["%d kubus" % x for x in bad if x != n],
                   "Satu lapis berisi %d × %d = %d kubus. Ada %d lapis: %d × %d = %d kubus." % (a, b, a * b, c, a * b, c, n))

    def ubin():
        r, c = ri(3, 10), ri(3, 10)
        room = ch(["lantai kamar", "lantai teras", "dinding kamar mandi", "halaman sekolah", "lantai dapur"])
        return mcq("%s ditutup ubin persegi. Ada %d baris dan setiap baris berisi %d ubin. Berapa banyak ubin yang dipakai?" % (room.capitalize(), r, c),
                   "%d ubin" % (r * c), ["%d ubin" % (r + c), "%d ubin" % (2 * (r + c)), "%d ubin" % (r * c - c)],
                   "%d × %d = %d ubin. Luas %s adalah %d ubin." % (r, c, r * c, room, r * c))

    def kotak():
        a, b, c = ri(2, 5), ri(2, 4), ri(2, 4)
        what = ch(["kotak kardus", "kotak mainan", "laci", "peti kayu"])
        return mcq("Sebuah %s diisi kubus mainan. Satu lapis berisi %d baris, setiap baris %d kubus. Ada %d lapis. Berapa banyak kubus di dalam %s?" % (what, b, a, c, what),
                   "%d kubus" % (a * b * c), ["%d kubus" % (a * b + c), "%d kubus" % (a + b + c), "%d kubus" % (a * b)],
                   "Satu lapis: %d × %d = %d. %d lapis: %d × %d = %d kubus." % (b, a, a * b, c, a * b, c, a * b * c))

    def nonbaku():
        w, h = ri(2, 6), ri(2, 5)
        who = K().next()
        thing = ch(["buku tulis", "kertas origami", "kartu", "ubin plastik"])
        return mcq("%s menutup meja dengan %s tanpa celah. Ada %d baris dan setiap baris %d %s. Luas meja itu adalah …" % (who, thing, h, w, thing),
                   "%d %s" % (w * h, thing), ["%d %s" % (w + h, thing), "%d %s" % (w * h + h, thing), "%d %s" % (2 * (w + h), thing)],
                   "%d × %d = %d. Luas meja = %d %s." % (h, w, w * h, w * h, thing))

    sets = [("Luas dengan petak satuan", [(hitung, 20)]),
            ("Luas persegi panjang", [(persegi_panjang, 12), (banding, 8)]),
            ("Volume dengan kubus satuan", [(vol, 20)]),
            ("Satuan tidak baku", [(nonbaku, 10), (ubin, 10)]),
            ("Soal cerita", [(ubin, 8), (kotak, 12)])]
    body = lesson(
        ["Luas adalah banyaknya petak satuan yang menutupi sebuah bangun tanpa celah dan tanpa tumpang tindih.",
         "Pada persegi panjang, hitung banyak baris dikali banyak petak setiap baris. Jika setiap petak 1 cm × 1 cm, luasnya dalam cm².",
         "Volume adalah banyaknya kubus satuan yang mengisi sebuah bangun ruang. Hitung satu lapis, lalu kalikan dengan banyak lapis."],
        [example("Persegi panjang 6 petak × 4 petak (petak 1 cm).", ["4 baris × 6 petak = 24 petak"], "24 cm²"),
         example("Balok 3 kubus × 2 kubus, tingginya 4 lapis.", ["Satu lapis: 3 × 2 = 6", "4 lapis: 6 × 4"], "24 kubus")],
        [["Luas dihitung dengan menjumlah panjang dan lebar", "Luas = banyak baris × banyak petak setiap baris"],
         ["Pada balok, hanya menghitung kubus yang terlihat", "Ada kubus yang tersembunyi di belakang: hitung per lapis"],
         ["Bangun yang luasnya sama dikira harus sama bentuknya", "Bentuk berbeda bisa punya luas yang sama"]])
    faq = [{"q": "Apa itu luas?", "a": "Luas adalah ukuran besarnya permukaan. Kita mengukurnya dengan menghitung petak satuan, misalnya ubin, kartu, atau persegi 1 cm (cm²)."},
           {"q": "Apa itu volume?", "a": "Volume adalah ukuran besarnya ruang yang ditempati benda. Kita mengukurnya dengan menghitung kubus satuan yang mengisinya."},
           {"q": "Apa bedanya satuan baku dan tidak baku?", "a": "Satuan tidak baku bisa berbeda-beda, misalnya buku atau kartu. Satuan baku selalu sama di mana saja, misalnya cm² untuk luas."}]
    return dict(slug="luas-dan-volume", dom="P", sort=14,
                std_text="Peserta didik dapat mengukur dan mengestimasi luas dan volume menggunakan satuan tidak baku dan satuan baku berupa bilangan cacah.",
                title="Luas dan Volume dengan Satuan", short_title="Luas dan Volume",
                meta_desc="Latihan mengukur luas dengan petak satuan, luas persegi panjang dalam cm², volume dengan kubus satuan, dan soal cerita ubin dan kotak. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Hitung petak dan kubus satuan", key_sub="Luas: baris × kolom. Volume: satu lapis × banyak lapis.",
                body=body, faq=faq, sets=sets)
