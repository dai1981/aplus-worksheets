# -*- coding: utf-8 -*-
"""
Indonesia / Matematika / Kelas 3 (Fase B, Kurikulum Merdeka CP 2025)。14 単元。
数は 1.000 まで、かけ算・わり算は 10 × 10 まで、お金は Rp20.000 まで。
python3 tools/id_k3.py [番号…]
seed は 40300 + sort。Kelas 4 の問題関数（id_k4a・id_k4b・id_k4c）も lim() で 1.000 までに絞って使う。
"""
import random
import re
import sys
import id_k4a as A
import id_k4b as B
import id_k4c as C
from id_k4a import ri, ch, pool, terbilang, cap, rel, stmt, titik, kelompok, nocarry_add, small_from_big, carries, borrows
from id_common import (num, rp, u, mcq, mix, lesson, example, table, make_unit, wrap, fr,
                       garis_bilangan, nilai_tempat, blok, bersusun, INK, GREEN, FILL)

G = "kelas-3"


# ------------------------------------------------------------ 共通
def maker(d, name, i=0):
    """Kelas 4 の単元 dict から名前で問題関数を取り出す"""
    out = []
    for _, parts in d["sets"]:
        for m, _n in parts:
            if m.__name__ == name and m not in out:
                out.append(m)
    return out[i]


def nums(it):
    t = re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
    return [int(x.replace(".", "")) for x in re.findall(r"\d+(?:\.\d{3})*", t)]


def lim(mk, mx=1000, bad=()):
    def f():
        it = mk()
        if it is None or max(nums(it) or [0]) > mx:
            return None
        t = it["q"] + " ".join(it["c"]) + it["e"]
        if any(b in t for b in bad):
            return None
        return it
    f.__name__ = mk.__name__
    return f


def n3(zero=False):
    d = [ri(1, 9), ri(0, 9), ri(0, 9)]
    if zero:
        d[ch([1, 2])] = 0
    return int("".join(map(str, d)))


def wrong3(n):
    s = str(n)
    out = []
    for i in range(len(s) - 1):
        t = list(s)
        t[i], t[i + 1] = t[i + 1], t[i]
        t = "".join(t)
        if t[0] != "0" and int(t) != n:
            out.append(int(t))
    out += [n + 100 if n < 900 else n - 100, n + 10 if n % 100 < 90 else n - 10, n + 1 if n % 10 < 9 else n - 1]
    return out


def F(a, b):
    return fr(a, b)


# ============================================================ 1. bilangan sampai 1.000
def u1():
    def baca():
        n = n3(R().random() < 0.4)
        return mcq("Bilangan <b>%s</b> dibaca …" % num(n), cap(terbilang(n)), [cap(terbilang(w)) for w in wrong3(n)],
                   "%s = %s." % (num(n), terbilang(n)))

    def tulis():
        n = n3(R().random() < 0.6)
        return mcq("Lambang bilangan dari <i>%s</i> adalah …" % terbilang(n), num(n), [num(w) for w in wrong3(n)],
                   "%s ditulis %s." % (cap(terbilang(n)), num(n)))

    PL = ["satuan", "puluhan", "ratusan"]

    def nilai():
        n = n3()
        s = str(n)
        i = ri(0, 2)
        d = int(s[i])
        if d == 0 or s.count(s[i]) > 1:
            return None
        p = 2 - i
        return mcq("Pada bilangan %s, angka %d bernilai …" % (num(n), d), num(d * 10 ** p),
                   [num(d * 10 ** q) for q in range(4) if q != p],
                   "Angka %d berada di tempat %s, jadi nilainya %s." % (d, PL[p], num(d * 10 ** p)))

    def tempat():
        n = n3()
        s = str(n)
        i = ri(0, 2)
        if s.count(s[i]) > 1:
            return None
        p = 2 - i
        return mcq("Pada bilangan %s, angka %s menempati tempat …" % (num(n), s[i]), PL[p], [x for x in PL + ["ribuan"] if x != PL[p]],
                   "Dari kanan: satuan, puluhan, ratusan. Angka %s ada di tempat %s." % (s[i], PL[p]))

    def gambar():
        a, b, c = ri(1, 9), ri(0, 9), ri(0, 9)
        if b + c < 2:
            return None
        n = a * 100 + b * 10 + c
        return mcq("Bilangan yang ditunjukkan gambar adalah …" + blok(a, b, c), num(n),
                   [num(w) for w in wrong3(n)] + [num(a * 100 + c * 10 + b)],
                   "%d ratusan, %d puluhan, %d satuan = %s." % (a, b, c, num(n)))

    def tabel():
        n = n3(R().random() < 0.5)
        return mcq("Bilangan pada tabel nilai tempat ini adalah …" + nilai_tempat(n, 3), num(n),
                   [num(w) for w in wrong3(n)] + [num(int(str(n)[::-1])) if str(n)[-1] != "0" else None],
                   "Baca dari ratusan sampai satuan: %s." % num(n))

    def garis():
        step = ch([10, 10, 100, 1])
        if step == 100:
            lo = 0
        elif step == 10:
            lo = ri(0, 9) * 100
        else:
            lo = ri(1, 99) * 10
        hi = lo + step * 10
        k = ri(1, 9)
        if k == 5:
            return None
        v = lo + k * step
        return mcq("Bilangan yang ditunjuk huruf A adalah …" + garis_bilangan(lo, hi, step, marks=[(v, "A")]), num(v),
                   [num(lo + (10 - k) * step), num(v + step), num(v - step), num(lo + k)],
                   "Satu garis kecil = %s. A ada %d garis dari %s, jadi %s." % (num(step), k, num(lo), num(v)))

    def sesudah():
        n = n3()
        d = ch([1, 10, 100])
        up = R().random() < 0.5
        if (up and n + d > 1000) or (not up and n - d < 100):
            return None
        v = n + d if up else n - d
        return mcq("Bilangan yang %s %s %s adalah …" % (num(d), "lebih dari" if up else "kurang dari", num(n)), num(v),
                   [num(n - d if up else n + d)] + [num(n + x if up else n - x) for x in (1, 10, 100) if x != d],
                   "%s %s %s = %s." % (num(n), "+" if up else "−", num(d), num(v)))

    def panjang():
        n = n3(R().random() < 0.3)
        s = str(n)
        p = [int(c) * 10 ** (2 - i) for i, c in enumerate(s) if c != "0"]
        if len(p) < 2:
            return None
        f = lambda ps: " + ".join(num(x) for x in ps)
        w1 = [int(str(x)[0]) for x in p]
        w2 = [x * 10 if i == len(p) - 1 else x for i, x in enumerate(p)]
        w3 = [x // 10 if x >= 10 and i == 0 else x for i, x in enumerate(p)]
        return mcq("Bentuk panjang dari %s adalah …" % num(n), f(p), [f(w1), f(w2), f(w3)],
                   "Setiap angka ditulis sesuai nilainya: %s = %s." % (num(n), f(p)))

    def susun():
        a, b, c = ri(1, 9), ri(0, 9), ri(1, 9)
        n = a * 100 + b * 10 + c
        return mcq("%d ratusan + %d puluhan + %d satuan = …" % (a, b, c), num(n),
                   [num(a * 100 + c * 10 + b), num(c * 100 + b * 10 + a), num(a * 10 + b * 100 + c)],
                   "%d + %d + %d = %s." % (a * 100, b * 10, c, num(n)))

    CTX = ["Di perpustakaan kelas ada %s buku.", "Pak Slamet memanen %s buah jeruk.", "Ada %s siswa di sekolah Dayu.",
           "Bu Tini membuat %s kue untuk bazar.", "Sebuah gedung punya %s kursi.", "Di kebun ada %s pohon jagung."]

    def cerita():
        n = n3(R().random() < 0.4)
        return mcq(ch(CTX) % num(n) + " Bilangan itu dibaca …", cap(terbilang(n)), [cap(terbilang(w)) for w in wrong3(n)],
                   "%s dibaca %s." % (num(n), terbilang(n)))

    sets = [("Membaca dan menulis bilangan", [(baca, 10), (tulis, 6), (cerita, 4)]),
            ("Nilai tempat", [(nilai, 10), (tempat, 5), (tabel, 5)]),
            ("Balok bilangan", [(gambar, 14), (susun, 6)]),
            ("Garis bilangan", [(garis, 12), (sesudah, 8)]),
            ("Bentuk panjang", [(panjang, 12), (susun, 4), (sesudah, 4)])]
    body = lesson(
        ["Bilangan sampai 1.000 punya tiga tempat: ratusan, puluhan, dan satuan.",
         "10 satuan = 1 puluhan. 10 puluhan = 1 ratusan. 10 ratusan = 1 ribuan (1.000).",
         "Baca dari kiri: ratusan dulu, lalu puluhan, lalu satuan. Angka 0 tidak dibaca.",
         "100 dibaca <i>seratus</i>, 10 dibaca <i>sepuluh</i>, dan 11 dibaca <i>sebelas</i>."],
        [example("Bacalah 507.", ["5 ratusan → lima ratus", "0 puluhan → tidak dibaca", "7 satuan → tujuh"], "lima ratus tujuh"),
         example("Tulislah <i>tiga ratus empat puluh</i>.", ["ratusan 3, puluhan 4, satuan 0"], "340")],
        [["Lima ratus tujuh ditulis 57", "Tempat puluhan diisi 0: 507"],
         ["115 dibaca <i>seratus sepuluh lima</i>", "115 dibaca <i>seratus lima belas</i>"],
         ["Nilai angka 4 pada 482 adalah 4", "Angka 4 di tempat ratusan, nilainya 400"]],
        table(["Ratusan", "Puluhan", "Satuan"], [["4", "8", "2"]]))
    faq = [{"q": "Bagaimana cara membaca bilangan tiga angka?", "a": "Baca ratusan, puluhan, lalu satuan. Contoh: 482 dibaca empat ratus delapan puluh dua."},
           {"q": "Kenapa 100 dibaca seratus?", "a": "Satu ratus disingkat menjadi seratus, sama seperti satu puluh menjadi sepuluh."},
           {"q": "Berapa puluhan dalam 1 ratusan?", "a": "1 ratusan = 10 puluhan = 100 satuan."}]
    return dict(slug="bilangan-cacah-sampai-1000", dom="B", sort=1,
                std_text="Peserta didik menunjukkan pemahaman bilangan cacah sampai 1.000: membaca, menulis, menentukan nilai tempat, serta menyusun dan mengurai bilangan.",
                title="Bilangan Cacah sampai 1.000", short_title="Bilangan Cacah sampai 1.000",
                meta_desc="Latihan membaca dan menulis bilangan sampai 1.000, nilai tempat, balok bilangan, garis bilangan, dan bentuk panjang untuk kelas 3 SD. 100 soal dengan kunci jawaban.",
                key_big="Ratusan, puluhan, satuan", key_sub="10 puluhan = 1 ratusan. Angka 0 tidak dibaca.",
                body=body, faq=faq, sets=sets)


def R():
    return A.R


def K():
    return A.K


# ============================================================ 2. membandingkan dan mengurutkan
def u2():
    def near(n):
        s = list(str(n))
        i = ri(1, 2)
        s[i] = str((int(s[i]) + ri(1, 8)) % 10)
        return int("".join(s))

    def banding():
        a = n3()
        b = ch([near(a), near(a), n3(), int(str(a)[0] + str(a)[2] + str(a)[1])])
        if b == a:
            return None
        return stmt(num(a), num(b), a, b, "Bandingkan dari tempat ratusan. Jika sama, lihat puluhan, lalu satuan. %s %s %s." % (num(a), rel(a, b), num(b)))

    def banding2():
        a, b = n3(), ri(10, 99)
        if R().random() < 0.5:
            a, b = b, a
        return stmt(num(a), num(b), a, b, "Bilangan tiga angka lebih besar dari bilangan dua angka. %s %s %s." % (num(a), rel(a, b), num(b)))

    def grp():
        base = ri(1, 9) * 100
        xs = set()
        while len(xs) < 4:
            xs.add(base + ri(0, 99))
        return sorted(xs)

    def ekstrem():
        xs = grp()
        big = R().random() < 0.5
        c = max(xs) if big else min(xs)
        return mcq("Bilangan %s dari %s adalah …" % ("terbesar" if big else "terkecil", ", ".join(num(x) for x in pool(xs))),
                   num(c), [num(x) for x in xs if x != c],
                   "Ratusannya sama, jadi bandingkan puluhan dan satuan. Yang %s adalah %s." % ("terbesar" if big else "terkecil", num(c)))

    def urut():
        xs = grp() if R().random() < 0.7 else sorted(set(n3() for _ in range(4)))
        if len(xs) < 4:
            return None
        up = R().random() < 0.5
        good = sorted(xs, reverse=not up)
        w1 = sorted(xs, reverse=up)
        w2 = sorted(xs, key=lambda x: (x % 10, x), reverse=not up)
        w3 = list(good)
        w3[1], w3[2] = w3[2], w3[1]
        f = lambda ys: ", ".join(num(y) for y in ys)
        return mcq("Urutan bilangan %s dari yang %s adalah …" % (f(pool(xs)), "terkecil ke terbesar" if up else "terbesar ke terkecil"),
                   f(good), [f(w1), f(w2), f(w3)], "Bandingkan tempat demi tempat dari kiri. Urutannya %s." % f(good))

    def antara():
        lo = ri(1, 8) * 100 + ri(0, 9) * 10
        hi = lo + 10
        g = lo + ri(1, 9)
        bad = [lo - ri(1, 9), hi + ri(1, 9), lo + 100 + ri(1, 9), hi + 10 + ri(1, 9)]
        return mcq("Bilangan yang terletak di antara %s dan %s adalah …" % (num(lo), num(hi)), num(g), [num(b) for b in bad],
                   "%s lebih besar dari %s dan lebih kecil dari %s." % (num(g), num(lo), num(hi)))

    def tanda():
        a = n3()
        b = near(a)
        if a == b:
            return None
        r = rel(a, b)
        return mcq("%s … %s. Tanda yang tepat adalah …" % (num(a), num(b)), r, [x for x in ["&lt;", "&gt;", "=", "+"] if x != r],
                   "%s %s %s." % (num(a), r, num(b)))

    CTX = [("Siswa di kelas %s mengumpulkan sampah plastik", "gram"), ("Sekolah menjual tiket pentas seni pada hari", "lembar"),
           ("Peternak menghasilkan telur pada hari", "butir"), ("Toko buku menjual pensil pada hari", "batang")]
    DAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]

    def cerita():
        names = pool(["Asep", "Tiara", "Made", "Siti", "Beni", "Lina", "Rudi", "Dewi"])[:4]
        xs = grp()
        R().shuffle(xs)
        big = R().random() < 0.5
        what = ch(["kelereng", "tutup botol", "biji saga", "stik es krim"])
        i = xs.index(max(xs) if big else min(xs))
        rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (n, num(x)) for n, x in zip(names, xs))
        t = "<table class='sn-table' style='width:auto'><thead><tr><th>Nama</th><th>Banyak %s</th></tr></thead><tbody>%s</tbody></table>" % (what, rows)
        return mcq("Tabel menunjukkan banyak %s milik empat anak. Siapa yang punya %s paling %s?%s" % (what, what, "banyak" if big else "sedikit", t),
                   names[i], [n for n in names if n != names[i]],
                   "%s adalah bilangan %s, jadi %s." % (num(xs[i]), "terbesar" if big else "terkecil", names[i]))

    sets = [("Membandingkan dua bilangan", [(banding, 12), (banding2, 4), (tanda, 4)]),
            ("Terbesar dan terkecil", [(ekstrem, 16), (antara, 4)]),
            ("Mengurutkan bilangan", [(urut, 16), (antara, 4)]),
            ("Tanda &lt;, &gt;, dan =", [(tanda, 10), (banding, 6), (banding2, 4)]),
            ("Soal cerita", [(cerita, 14), (urut, 3), (ekstrem, 3)])]
    body = lesson(
        ["Bilangan tiga angka selalu lebih besar dari bilangan dua angka.",
         "Jika banyak angkanya sama, bandingkan dari kiri: ratusan, lalu puluhan, lalu satuan.",
         "Tanda &lt; berarti <i>kurang dari</i>, tanda &gt; berarti <i>lebih dari</i>. Mulut tanda terbuka ke bilangan yang lebih besar."],
        [example("Bandingkan 635 dan 653.", ["Ratusan sama (6)", "Puluhan: 3 &lt; 5"], "635 &lt; 653"),
         example("Urutkan dari terkecil: 418, 481, 408.", ["Ratusan sama (4)", "Puluhan: 0 &lt; 1 &lt; 8"], "408, 418, 481")],
        [["Membandingkan dari angka paling kanan", "Mulai dari ratusan (paling kiri)"],
         ["98 &gt; 102 karena angka 9 besar", "102 punya tiga angka, jadi 102 &gt; 98"],
         ["Arah tanda terbalik", "Mulut tanda menghadap bilangan yang lebih besar: 5 &lt; 8"]])
    faq = [{"q": "Bagaimana cara membandingkan bilangan tiga angka?", "a": "Bandingkan ratusan dulu. Jika sama, bandingkan puluhan. Jika masih sama, bandingkan satuan."},
           {"q": "Apa arti tanda < dan >?", "a": "Tanda < dibaca kurang dari dan tanda > dibaca lebih dari. Contoh: 245 < 254 dan 900 > 899."},
           {"q": "Apa bedanya urutan naik dan turun?", "a": "Urutan naik dari terkecil ke terbesar. Urutan turun dari terbesar ke terkecil."}]
    return dict(slug="membandingkan-dan-mengurutkan-bilangan", dom="B", sort=2,
                std_text="Peserta didik membandingkan dan mengurutkan bilangan cacah sampai 1.000.",
                title="Membandingkan dan Mengurutkan Bilangan sampai 1.000", short_title="Membandingkan dan Mengurutkan Bilangan",
                meta_desc="Latihan membandingkan bilangan sampai 1.000 dengan tanda <, > dan =, mencari terbesar dan terkecil, dan mengurutkan bilangan. 100 soal dengan kunci jawaban untuk kelas 3 SD.",
                key_big="Bandingkan dari ratusan", key_sub="Ratusan, lalu puluhan, lalu satuan.",
                body=body, faq=faq, sets=sets)


# ============================================================ 3. penjumlahan
def u3():
    def tambah(carry, pic=False, lo=100):
        def mk():
            a, b = ri(lo, 899), ri(lo if lo > 10 else 10, 899 if lo > 10 else 99)
            if a + b > 1000 or carries(a, b) != carry:
                return None
            s = a + b
            w = [nocarry_add(a, b), s + 10, s - 10, s + 100, s - 100]
            q = ("%s + %s = …" % (num(a), num(b))) if not pic else ("Hasil penjumlahan bersusun ini adalah …" + bersusun([str(a), str(b)], "+"))
            return mcq(q, num(s), [num(x) for x in w if 0 < x != s],
                       ("Jumlahkan satuan dulu. Jika 10 atau lebih, simpan 1 ke puluhan. " if carry else "Jumlahkan satuan, puluhan, lalu ratusan. ")
                       + "%s + %s = %s." % (num(a), num(b), num(s)))
        mk.__name__ = "tambah"
        return mk

    def dua():
        a, b = ri(11, 89), ri(11, 89)
        s = a + b
        return mcq("%d + %d = …" % (a, b), num(s), [num(s - 10) if carries(a, b) else num(s + 1), num(s + 10), num(s - 1), num(s + 1), num(s - 10)],
                   "Puluhan: %d + %d = %d. Satuan: %d + %d = %d. Jadi %d." % (a // 10 * 10, b // 10 * 10, a // 10 * 10 + b // 10 * 10, a % 10, b % 10, a % 10 + b % 10, s))

    def mental():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(1, 8) * 100, ri(1, 8) * 100
        elif k == 1:
            a, b = ri(1, 8) * 100 + ri(1, 9) * 10, ri(1, 9) * 10
        else:
            a, b = ri(1, 8) * 100 + ri(1, 9) * 10, ri(1, 3) * 100
        if a + b > 1000:
            return None
        return mcq("Hitung dalam hati: %s + %s = …" % (num(a), num(b)), num(a + b), [num(a + b + 100), num(a + b - 10), num(a + b + 10)],
                   "Jumlahkan ratusan dengan ratusan dan puluhan dengan puluhan: %s." % num(a + b))

    def kosong():
        a, s = ri(100, 700), 0
        b = ri(10, 290)
        s = a + b
        if s > 1000:
            return None
        return mcq("%s + … = %s" % (num(a), num(s)), num(b), [num(s + a) if s + a <= 1999 else num(b + 10), num(b + 10), num(b - 10), num(b + 100)],
                   "Bilangan yang hilang = %s − %s = %s." % (num(s), num(a), num(b)))

    def tiga():
        a, b, c = ri(10, 300), ri(10, 300), ri(10, 300)
        s = a + b + c
        if s > 1000:
            return None
        return mcq("%s + %s + %s = …" % (num(a), num(b), num(c)), num(s), [num(s + 10), num(s - 10), num(s + 100), num(a + b)],
                   "%s + %s = %s, lalu %s + %s = %s." % (num(a), num(b), num(a + b), num(a + b), num(c), num(s)))

    ADD = ["Di sekolah ada %s siswa laki-laki dan %s siswa perempuan. Berapa jumlah semua siswa?",
           "Pak Slamet memanen %s jeruk hari ini dan %s jeruk kemarin. Berapa jeruk yang dipanen?",
           "Perpustakaan punya %s buku cerita. Sekolah membeli lagi %s buku. Berapa banyak buku sekarang?",
           "Bu Dewi membuat %s kue lapis dan %s kue lumpur. Berapa banyak kue yang dibuat?",
           "Ada %s penonton di tribun utara dan %s penonton di tribun selatan. Berapa jumlah penonton?",
           "Made mengumpulkan %s tutup botol. Adiknya mengumpulkan %s tutup botol. Berapa tutup botol mereka?",
           "Sebuah bus membawa %s penumpang hari Sabtu dan %s penumpang hari Minggu. Berapa jumlah penumpang?",
           "Toko menjual %s bungkus roti pagi hari dan %s bungkus sore hari. Berapa bungkus roti yang terjual?"]
    UNIT = ["siswa", "jeruk", "buku", "kue", "orang", "tutup botol", "orang", "bungkus"]

    def cerita():
        i = ri(0, len(ADD) - 1)
        a, b = ri(105, 600), ri(105, 390)
        if a + b > 1000:
            return None
        s = a + b
        return mcq(ADD[i] % (num(a), num(b)), u(s, UNIT[i]), [u(nocarry_add(a, b), UNIT[i]) if carries(a, b) else u(s + 10, UNIT[i]), u(abs(a - b), UNIT[i]), u(s + 100, UNIT[i])],
                   "Digabung, jadi dijumlah: %s + %s = %s." % (num(a), num(b), num(s)))

    sets = [("Menjumlah bilangan dua angka", [(dua, 12), (mental, 8)]),
            ("Tanpa menyimpan", [(tambah(False), 12), (tambah(False, True), 8)]),
            ("Dengan menyimpan", [(tambah(True), 12), (tambah(True, True), 8)]),
            ("Bilangan yang hilang dan tiga bilangan", [(kosong, 10), (tiga, 10)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Tulis bersusun: satuan di bawah satuan, puluhan di bawah puluhan, ratusan di bawah ratusan.",
         "Mulai menjumlah dari satuan. Jika hasilnya 10 atau lebih, tulis satuannya dan simpan 1 ke puluhan.",
         "Untuk berhitung dalam hati, jumlahkan ratusan dengan ratusan, puluhan dengan puluhan."],
        [example("368 + 247 = …", ["Satuan: 8 + 7 = 15, tulis 5 simpan 1", "Puluhan: 6 + 4 + 1 = 11, tulis 1 simpan 1", "Ratusan: 3 + 2 + 1 = 6"], "615"),
         example("450 + 300 = …", ["4 ratusan + 3 ratusan = 7 ratusan", "puluhan 5"], "750")],
        [["Lupa menambahkan 1 yang disimpan (368 + 247 = 505)", "Tulis angka 1 kecil di atas: 615"],
         ["Angka tidak lurus: 45 + 213 ditulis 450 + 213", "Satuan harus di bawah satuan: 45 + 213 = 258"],
         ["Menjumlah 7 + 8 lalu menulis 15 di satu tempat", "Tulis 5, simpan 1 ke puluhan"]])
    faq = [{"q": "Apa itu menyimpan dalam penjumlahan?", "a": "Jika jumlah satuan 10 atau lebih, puluhannya dipindah ke kolom puluhan. Contoh: 8 + 7 = 15, tulis 5 dan simpan 1."},
           {"q": "Bagaimana cara menjumlah tiga bilangan?", "a": "Jumlahkan dua bilangan dulu, lalu tambahkan bilangan ketiga ke hasilnya."},
           {"q": "Kata apa yang menandakan penjumlahan dalam soal cerita?", "a": "Kata seperti jumlah, semua, digabung, ditambah, dan membeli lagi biasanya berarti penjumlahan."}]
    return dict(slug="penjumlahan", dom="B", sort=3,
                std_text="Peserta didik melakukan operasi penjumlahan bilangan cacah sampai 1.000 menggunakan benda konkret, gambar, dan simbol matematika.",
                title="Penjumlahan sampai 1.000", short_title="Penjumlahan",
                meta_desc="Latihan penjumlahan sampai 1.000: dua angka, bersusun dengan dan tanpa menyimpan, bilangan yang hilang, tiga bilangan, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 3 SD.",
                key_big="Mulai dari satuan", key_sub="Jika 10 atau lebih, simpan 1 ke kiri.",
                body=body, faq=faq, sets=sets)


# ============================================================ 4. pengurangan
def u4():
    def kurang(borrow, pic=False):
        def mk():
            a, b = ri(200, 1000), ri(100, 899)
            if b >= a or borrows(a, b) != borrow:
                return None
            d = a - b
            w = [small_from_big(a, b), d + 10, d - 10, d + 100, a + b]
            q = ("%s − %s = …" % (num(a), num(b))) if not pic else ("Hasil pengurangan bersusun ini adalah …" + bersusun([str(a), str(b)], "−"))
            return mcq(q, num(d), [num(x) for x in w if 0 < x != d and x <= 1000],
                       ("Jika angka atas lebih kecil, pinjam 1 dari tempat di kirinya. " if borrow else "Kurangkan satuan, puluhan, lalu ratusan. ")
                       + "%s − %s = %s." % (num(a), num(b), num(d)))
        mk.__name__ = "kurang"
        return mk

    def dua():
        a, b = ri(30, 99), ri(11, 89)
        if b >= a:
            return None
        d = a - b
        return mcq("%d − %d = …" % (a, b), num(d), [num(small_from_big(a, b)) if borrows(a, b) else num(d + 1), num(d + 10), num(d - 1), num(a + b)],
                   "%d − %d = %d." % (a, b, d))

    def mental():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(3, 10) * 100, ri(1, 2) * 100
        elif k == 1:
            a, b = ri(1, 9) * 100 + ri(5, 9) * 10, ri(1, 4) * 10
        else:
            a, b = ri(3, 9) * 100 + ri(1, 9) * 10, ri(1, 2) * 100
        if b >= a:
            return None
        return mcq("Hitung dalam hati: %s − %s = …" % (num(a), num(b)), num(a - b), [num(a - b + 100), num(a - b - 10), num(a + b) if a + b <= 1000 else num(a - b + 10)],
                   "%s − %s = %s." % (num(a), num(b), num(a - b)))

    def cek():
        a, b = ri(300, 1000), ri(100, 290)
        d = a - b
        good = "%s + %s = %s" % (num(d), num(b), num(a))
        return mcq("%s − %s = %s. Cara memeriksa hasilnya adalah …" % (num(a), num(b), num(d)), good,
                   ["%s − %s = %s" % (num(d), num(b), num(d - b)) if d > b else "%s + %s = %s" % (num(a), num(b), num(a + b)),
                    "%s + %s = %s" % (num(a), num(b), num(a + b)), "%s − %s = %s" % (num(a), num(d), num(b))],
                   "Hasil pengurangan ditambah bilangan pengurang harus kembali ke bilangan semula: %s." % good)

    def kosong():
        a, b = ri(300, 1000), ri(100, 290)
        d = a - b
        if R().random() < 0.5:
            return mcq("%s − … = %s" % (num(a), num(d)), num(b), [num(a + d) if a + d <= 1000 else num(b + 100), num(b + 10), num(b - 10)],
                       "Bilangan yang hilang = %s − %s = %s." % (num(a), num(d), num(b)))
        return mcq("… − %s = %s" % (num(b), num(d)), num(a), [num(d - b) if d > b else num(a - 100), num(a + 10), num(a - 10)],
                   "Bilangan yang hilang = %s + %s = %s." % (num(d), num(b), num(a)))

    SUB = [("Toko punya %s butir telur. Sebanyak %s butir terjual. Berapa butir telur yang tersisa?", "butir"),
           ("Gedung punya %s kursi. Sebanyak %s kursi sudah terisi. Berapa kursi yang masih kosong?", "kursi"),
           ("Ada %s bibit pohon. Sebanyak %s bibit sudah ditanam. Berapa bibit yang belum ditanam?", "bibit"),
           ("Sekolah memesan %s buku tulis. Yang sudah dibagikan %s buku. Berapa buku yang belum dibagikan?", "buku"),
           ("Pak Agus punya %s ekor ayam. Sebanyak %s ekor dijual. Berapa ekor ayam yang masih ada?", "ekor"),
           ("Ada %s lembar kertas lipat. Sebanyak %s lembar dipakai. Berapa lembar yang tersisa?", "lembar")]
    DIF = [("Asep mengumpulkan %s stik es krim dan Tiara %s stik. Berapa selisih stik mereka?", "stik"),
           ("Kelas 3A mengumpulkan %s botol bekas dan kelas 3B %s botol. Berapa selisih botol kedua kelas?", "botol"),
           ("Pada hari Senin ada %s pengunjung taman dan hari Selasa %s pengunjung. Berapa selisihnya?", "orang")]

    def cerita():
        if R().random() < 0.65:
            t, unit = ch(SUB)
        else:
            t, unit = ch(DIF)
        a, b = ri(300, 1000), ri(110, 290)
        d = a - b
        return mcq(t % (num(a), num(b)), u(d, unit), [u(a + b, unit) if a + b <= 1000 else u(d + 100, unit), u(small_from_big(a, b), unit) if borrows(a, b) else u(d + 10, unit), u(d - 10, unit)],
                   "Dicari dengan pengurangan: %s − %s = %s." % (num(a), num(b), num(d)))

    sets = [("Mengurang bilangan dua angka", [(dua, 12), (mental, 8)]),
            ("Tanpa meminjam", [(kurang(False), 12), (kurang(False, True), 8)]),
            ("Dengan meminjam", [(kurang(True), 12), (kurang(True, True), 8)]),
            ("Bilangan yang hilang dan memeriksa", [(kosong, 12), (cek, 8)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Tulis bersusun: satuan di bawah satuan, puluhan di bawah puluhan, ratusan di bawah ratusan.",
         "Mulai mengurang dari satuan. Jika angka atas lebih kecil, pinjam 1 dari tempat di kirinya. 1 puluhan = 10 satuan.",
         "Untuk memeriksa, jumlahkan hasil dengan bilangan pengurang. Hasilnya harus sama dengan bilangan semula."],
        [example("524 − 168 = …", ["Satuan: 4 &lt; 8, pinjam 1 puluhan: 14 − 8 = 6", "Puluhan: 1 &lt; 6, pinjam 1 ratusan: 11 − 6 = 5", "Ratusan: 4 − 1 = 3"], "356"),
         example("Periksa: 356 + 168 = …", ["356 + 168 = 524"], "Hasilnya benar")],
        [["Angka kecil dikurangi angka besar (4 − 8 menjadi 4)", "Pinjam 1 dari kiri: 14 − 8 = 6"],
         ["Lupa mengurangi 1 setelah meminjam", "Puluhan yang dipinjam berkurang 1"],
         ["Selisih dicari dengan penjumlahan", "Selisih = bilangan besar − bilangan kecil"]])
    faq = [{"q": "Apa itu meminjam dalam pengurangan?", "a": "Jika angka atas lebih kecil dari angka bawah, ambil 1 dari tempat di sebelah kiri. 1 puluhan menjadi 10 satuan."},
           {"q": "Bagaimana memeriksa hasil pengurangan?", "a": "Jumlahkan hasilnya dengan bilangan pengurang. Contoh: 524 − 168 = 356, dan 356 + 168 = 524."},
           {"q": "Kata apa yang menandakan pengurangan dalam soal cerita?", "a": "Kata seperti sisa, tersisa, selisih, dijual, diberikan, dan dimakan biasanya berarti pengurangan."}]
    return dict(slug="pengurangan", dom="B", sort=4,
                std_text="Peserta didik melakukan operasi pengurangan bilangan cacah sampai 1.000 menggunakan benda konkret, gambar, dan simbol matematika.",
                title="Pengurangan sampai 1.000", short_title="Pengurangan",
                meta_desc="Latihan pengurangan sampai 1.000: dua angka, bersusun dengan dan tanpa meminjam, bilangan yang hilang, memeriksa hasil, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 3 SD.",
                key_big="Pinjam 1 dari kiri", key_sub="1 puluhan = 10 satuan. Periksa dengan penjumlahan.",
                body=body, faq=faq, sets=sets)


# ============================================================ 5. perkalian
def u5(d4):
    gambar, berulang = maker(d4, "gambar"), maker(d4, "berulang")

    def fw(a, b):
        p = a * b
        return [str(x) for x in (p + a, p - a, p + b, p - b, a + b, p + 1) if x > 0]

    def tabel(lo, hi):
        def mk():
            a, b = ri(lo, hi), ri(1, 10)
            if R().random() < 0.5:
                a, b = b, a
            return mcq("%d × %d = …" % (a, b), str(a * b), fw(a, b), "%d × %d = %d." % (a, b, a * b))
        mk.__name__ = "tabel"
        return mk

    def tukar():
        a, b = ri(2, 10), ri(2, 10)
        if a == b:
            return None
        return mcq("%d × %d = %d × …" % (a, b, b), str(a), [str(b), str(a * b), str(a + b)],
                   "Urutan perkalian boleh ditukar: %d × %d = %d × %d = %d." % (a, b, b, a, a * b))

    def lompat():
        k = ri(2, 10)
        s = ri(1, 5)
        xs = [k * (s + i) for i in range(5)]
        j = ri(1, 4)
        show = [str(x) if i != j else "…" for i, x in enumerate(xs)]
        return mcq("Lompat %d-an: %s. Bilangan yang hilang adalah …" % (k, ", ".join(show)), str(xs[j]),
                   [str(xs[j] + 1), str(xs[j] + k), str(xs[j] - 1)], "Setiap lompatan ditambah %d, jadi %d." % (k, xs[j]))

    def kosong():
        a, b = ri(2, 10), ri(2, 10)
        return mcq("%d × … = %d" % (a, a * b), str(b), [str(a * b - a), str(b + 1), str(b - 1), str(a * b + a)], "%d × %d = %d." % (a, b, a * b))

    KALI = ["Ada %d piring. Setiap piring berisi %d kue. Berapa kue seluruhnya?",
            "Di kelas ada %d baris meja. Setiap baris ada %d meja. Berapa meja seluruhnya?",
            "Putu membeli %d ikat rambutan. Setiap ikat berisi %d buah. Berapa buah rambutan semuanya?",
            "Ada %d kotak pensil. Setiap kotak berisi %d pensil. Berapa pensil seluruhnya?",
            "Bu guru membagikan %d bungkus permen. Setiap bungkus berisi %d permen. Berapa permen seluruhnya?",
            "Sebuah rak punya %d susun. Setiap susun berisi %d buku. Berapa buku di rak itu?"]
    FIX = [("Ada %d becak di pangkalan. Setiap becak punya 3 roda. Berapa roda seluruhnya?", 3),
           ("Ada %d ekor kucing. Setiap kucing punya 4 kaki. Berapa kaki seluruhnya?", 4),
           ("Ada %d sepeda di parkiran sekolah. Setiap sepeda punya 2 roda. Berapa roda seluruhnya?", 2)]

    def cerita():
        a = ri(2, 10)
        if R().random() < 0.3:
            t, b = ch(FIX)
            q = t % a
        else:
            b = ri(2, 10)
            q = ch(KALI) % (a, b)
        return mcq(q, str(a * b), [str(a + b), str(a * b + a), str(a * b - b), str(a * b + b)], "%d × %d = %d." % (a, b, a * b))

    sets = [("Gambar dan penjumlahan berulang", [(gambar, 10), (berulang, 10)]),
            ("Perkalian 2, 3, 4, dan 5", [(tabel(2, 5), 14), (lompat, 6)]),
            ("Perkalian 6 sampai 10", [(tabel(6, 10), 14), (tukar, 6)]),
            ("Bilangan yang hilang", [(kosong, 12), (tukar, 4), (lompat, 4)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Perkalian adalah penjumlahan berulang dari bilangan yang sama. 4 × 3 berarti 3 + 3 + 3 + 3.",
         "Pada gambar, banyak kelompok × banyak benda di setiap kelompok = banyak benda semuanya.",
         "Urutan perkalian boleh ditukar: 3 × 7 = 7 × 3 = 21. Ini memudahkan menghafal."],
        [example("5 × 6 = …", ["6 + 6 + 6 + 6 + 6", "atau lompat 6-an: 6, 12, 18, 24, 30"], "30"),
         example("Ada 4 piring, setiap piring 7 kue. Berapa kue?", ["4 kelompok, setiap kelompok 7", "4 × 7 = 28"], "28 kue")],
        [["4 × 3 dihitung 4 + 3 = 7", "4 × 3 = 3 + 3 + 3 + 3 = 12"],
         ["Lompat 4-an ditulis 4, 8, 10, 12", "Setiap lompatan ditambah 4: 4, 8, 12, 16"],
         ["Membalik arti soal: 3 kotak isi 5 ditulis 3 + 5", "3 kotak isi 5 = 3 × 5 = 15"]])
    faq = [{"q": "Apa itu perkalian?", "a": "Perkalian adalah penjumlahan berulang. 3 × 5 artinya 5 + 5 + 5 = 15."},
           {"q": "Bagaimana cara menghafal perkalian?", "a": "Mulai dari perkalian 2, 5, dan 10, lalu gunakan sifat pertukaran. Contoh: jika tahu 5 × 8 = 40, maka 8 × 5 juga 40."},
           {"q": "Apa itu lompat hitung?", "a": "Lompat hitung adalah menghitung dengan menambah bilangan yang sama terus-menerus, misalnya lompat 3-an: 3, 6, 9, 12."}]
    return dict(slug="perkalian", dom="B", sort=5,
                std_text="Peserta didik melakukan operasi perkalian bilangan cacah sampai 100 menggunakan benda konkret, gambar, dan simbol matematika.",
                title="Perkalian sampai 10 × 10", short_title="Perkalian",
                meta_desc="Latihan perkalian untuk kelas 3 SD: gambar kelompok, penjumlahan berulang, perkalian 2 sampai 10, lompat hitung, bilangan yang hilang, dan soal cerita. 100 soal dengan kunci jawaban.",
                key_big="Perkalian = penjumlahan berulang", key_sub="4 × 3 = 3 + 3 + 3 + 3 = 12.",
                body=body, faq=faq, sets=sets)


# ============================================================ 6. pembagian
def u6(d4):
    bagi, hubungan = maker(d4, "bagi"), maker(d4, "hubungan")

    def gambar():
        g, k = ri(2, 5), ri(2, 6)
        n = g * k
        if R().random() < 0.5:
            return mcq("Ada %d kelereng dibagi sama banyak ke dalam %d kantong. Setiap kantong berisi …%s" % (n, g, kelompok(g, k)),
                       str(k), [str(g), str(n - g), str(k + 1)], "%d : %d = %d." % (n, g, k))
        return mcq("Kalimat pembagian yang sesuai dengan gambar adalah …" + kelompok(g, k), "%d : %d = %d" % (n, g, k),
                   ["%d : %d = %d" % (n, k + 1, g), "%d − %d = %d" % (n, g, n - g), "%d × %d = %d" % (g, k, n + g), "%d : %d = %d" % (g, k, n)],
                   "%d benda dibagi ke %d kelompok, setiap kelompok %d: %d : %d = %d." % (n, g, k, n, g, k))

    def ulang():
        b, a = ri(2, 6), ri(2, 6)
        n = a * b
        seq = ", ".join(str(n - b * i) for i in range(a + 1))
        return mcq("%d dikurangi %d terus sampai habis: %s. Jadi %d : %d = …" % (n, b, seq, n, b), str(a), [str(a + 1), str(b), str(n - b)],
                   "Ada %d kali pengurangan, jadi %d : %d = %d." % (a, n, b, a))

    def kosong():
        a, b = ri(2, 10), ri(2, 10)
        n = a * b
        if R().random() < 0.5:
            return mcq("%d : … = %d" % (n, a), str(b), [str(n - a), str(b + 1), str(b - 1), str(n + a)], "%d : %d = %d karena %d × %d = %d." % (n, b, a, a, b, n))
        return mcq("… : %d = %d" % (b, a), str(n), [str(a + b), str(n + b), str(n - b), str(a)], "%d × %d = %d, jadi %d : %d = %d." % (a, b, n, n, b, a))

    def satu():
        n = ri(2, 10)
        k = ri(0, 2)
        if k == 0:
            return mcq("%d : %d = …" % (n, n), "1", ["0", str(n), str(n * n)], "Bilangan dibagi dirinya sendiri hasilnya 1.")
        if k == 1:
            return mcq("%d : 1 = …" % n, str(n), ["1", "0", str(n + 1)], "Bilangan dibagi 1 hasilnya bilangan itu sendiri.")
        return mcq("0 : %d = …" % n, "0", ["1", str(n), "10"], "0 dibagi bilangan apa pun hasilnya 0.")

    BAGI = ["Ada %d jeruk dibagi sama banyak kepada %d anak. Berapa jeruk yang didapat setiap anak?",
            "Sebanyak %d siswa dibagi menjadi %d kelompok sama besar. Berapa siswa di setiap kelompok?",
            "Sebanyak %d buku disusun sama banyak di %d rak. Berapa buku di setiap rak?",
            "Bu Wiwin membagi %d kue sama banyak ke %d piring. Berapa kue di setiap piring?"]
    GRUP = ["Ada %d telur. Setiap wadah diisi %d telur. Berapa wadah yang diperlukan?",
            "Ada %d kelereng. Setiap kantong diisi %d kelereng. Berapa kantong yang terisi?",
            "Sebanyak %d siswa naik perahu. Setiap perahu memuat %d siswa. Berapa perahu yang diperlukan?",
            "Ada %d tangkai bunga. Setiap vas diisi %d tangkai. Berapa vas yang diperlukan?"]

    def cerita():
        a, b = ri(2, 10), ri(2, 10)
        n = a * b
        t = ch(BAGI if R().random() < 0.5 else GRUP)
        return mcq(t % (n, b), str(a), [str(n - b), str(n + b), str(a + 1), str(b * 2)], "%d : %d = %d." % (n, b, a))

    sets = [("Membagi sama banyak", [(gambar, 14), (ulang, 6)]),
            ("Pembagian dan perkalian", [(hubungan, 14), (bagi, 6)]),
            ("Fakta pembagian", [(bagi, 14), (satu, 6)]),
            ("Bilangan yang hilang", [(kosong, 14), (ulang, 6)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Pembagian berarti membagi sama banyak, atau membuat kelompok yang sama besar.",
         "Pembagian adalah kebalikan perkalian. 12 : 3 = 4 karena 4 × 3 = 12.",
         "Pembagian juga bisa dihitung dengan pengurangan berulang: 12 − 3 − 3 − 3 − 3 = 0, ada 4 kali."],
        [example("18 : 3 = …", ["Cari bilangan yang dikali 3 menjadi 18", "6 × 3 = 18"], "6"),
         example("Ada 20 telur, setiap wadah 5 telur. Berapa wadah?", ["20 : 5", "4 × 5 = 20"], "4 wadah")],
        [["18 : 3 dihitung 18 − 3 = 15", "Pembagian bukan pengurangan sekali: 18 : 3 = 6"],
         ["Urutan dibalik: 3 : 18", "Bilangan yang dibagi ditulis di depan: 18 : 3"],
         ["0 : 5 = 5", "Tidak ada yang dibagi, jadi 0 : 5 = 0"]])
    faq = [{"q": "Apa hubungan pembagian dan perkalian?", "a": "Pembagian adalah kebalikan perkalian. Jika 6 × 4 = 24, maka 24 : 4 = 6 dan 24 : 6 = 4."},
           {"q": "Apa bedanya membagi dan mengelompokkan?", "a": "Membagi: banyak kelompok sudah diketahui, dicari isi setiap kelompok. Mengelompokkan: isi setiap kelompok diketahui, dicari banyak kelompok. Keduanya dihitung dengan pembagian."},
           {"q": "Berapa hasil bilangan dibagi 1?", "a": "Bilangan dibagi 1 hasilnya bilangan itu sendiri. Contoh: 7 : 1 = 7."}]
    return dict(slug="pembagian", dom="B", sort=6,
                std_text="Peserta didik melakukan operasi pembagian bilangan cacah sampai 100 menggunakan benda konkret, gambar, dan simbol matematika.",
                title="Pembagian sampai 100", short_title="Pembagian",
                meta_desc="Latihan pembagian untuk kelas 3 SD: membagi sama banyak dengan gambar, hubungan perkalian dan pembagian, pengurangan berulang, bilangan yang hilang, dan soal cerita. 100 soal dengan kunci jawaban.",
                key_big="12 : 3 = 4 karena 4 × 3 = 12", key_sub="Bagi sama banyak, atau buat kelompok sama besar.",
                body=body, faq=faq, sets=sets)


# ============================================================ 7. pecahan
def u7(d4):
    arsir, nama, satu, gambar2, sama, ekstrem = (maker(d4, x) for x in ("arsir", "nama", "satu", "gambar2", "sama", "ekstrem"))
    small = lambda mk: lim(mk, 10)

    def dari():
        k = ch([2, 3, 4, 5])
        g = ri(2, 5)
        n = k * g
        w = ch(["kelereng", "jeruk", "permen", "kue"])
        return mcq("%s punya %d %s. %s dari %s itu diberikan kepada adiknya. Berapa %s yang diberikan?%s" % (K().next(), n, w, F(1, k), w, w, kelompok(k, g)),
                   str(g), [str(n - g), str(k), str(g + 1), str(n)],
                   "%d %s dibagi %d sama banyak, setiap bagian %d. Jadi %s dari %d = %d." % (n, w, k, g, F(1, k), n, g))

    def bagian():
        k = ch([2, 3, 4, 5, 6, 8])
        good = F(1, k)
        w = ch(["kue", "roti", "semangka", "pizza", "kertas", "pita"])
        return mcq("Sebuah %s dipotong menjadi %d bagian sama besar. Satu potong %s adalah … bagian." % (w, k, w), good,
                   [F(1, k + 1), F(1, k - 1) if k > 2 else F(2, 3), F(k - 1, k) if k > 2 else F(1, 4), F(k, 1)],
                   "Satu dari %d bagian sama besar adalah %s." % (k, good))

    WORD = {2: "seperdua (setengah)", 3: "sepertiga", 4: "seperempat", 5: "seperlima", 6: "seperenam", 8: "seperdelapan"}

    def kata():
        k = ch(list(WORD))
        others = [WORD[x] for x in WORD if x != k]
        if R().random() < 0.5:
            return mcq("Pecahan <i>%s</i> ditulis …" % WORD[k].split(" (")[0], F(1, k), [F(1, x) for x in pool([x for x in WORD if x != k])] ,
                       "%s ditulis %s." % (cap(WORD[k]), F(1, k)))
        return mcq("Pecahan %s dibaca …" % F(1, k), WORD[k].split(" (")[0] if k != 2 else "seperdua", [o.split(" (")[0] for o in pool(others)],
                   "%s dibaca %s." % (F(1, k), WORD[k]))

    sets = [("Membaca pecahan", [(small(arsir), 12), (kata, 8)]),
            ("Pecahan satuan", [(small(satu), 12), (bagian, 8)]),
            ("Bagian yang diarsir", [(small(gambar2), 10), (small(nama), 10)]),
            ("Membandingkan pecahan", [(small(sama), 10), (small(ekstrem), 10)]),
            ("Pecahan dari sekumpulan benda", [(dari, 20)])]
    body = lesson(
        ["Pecahan menunjukkan bagian dari satu benda utuh yang dibagi menjadi bagian-bagian <b>sama besar</b>.",
         "Bilangan bawah (penyebut) = banyak bagian semuanya. Bilangan atas (pembilang) = banyak bagian yang diambil atau diarsir.",
         "Pada pecahan berpembilang 1, makin besar penyebutnya, makin kecil bagiannya. " + F(1, 2) + " lebih besar dari " + F(1, 4) + "."],
        [example("Pita dibagi 4 bagian sama besar dan 3 bagian diarsir. Pecahannya?", ["Penyebut = 4 (semua bagian)", "Pembilang = 3 (bagian diarsir)"], F(3, 4)),
         example("Berapa " + F(1, 3) + " dari 12 jeruk?", ["12 jeruk dibagi 3 sama banyak", "12 : 3 = 4"], "4 jeruk")],
        [["Bagian yang tidak sama besar dianggap pecahan", "Bagian-bagiannya harus sama besar"],
         [F(1, 4) + " lebih besar dari " + F(1, 2) + " karena 4 lebih besar", "Makin banyak potongan, makin kecil tiap potongan: " + F(1, 2) + " &gt; " + F(1, 4)],
         ["Pembilang dan penyebut tertukar", "Penyebut (bawah) = semua bagian"]])
    faq = [{"q": "Apa itu pecahan?", "a": "Pecahan adalah bilangan yang menunjukkan bagian dari benda utuh yang dibagi sama besar, misalnya setengah atau seperempat."},
           {"q": "Apa itu pembilang dan penyebut?", "a": "Penyebut adalah bilangan di bawah, yaitu banyak bagian semuanya. Pembilang adalah bilangan di atas, yaitu banyak bagian yang diambil."},
           {"q": "Mengapa 1/2 lebih besar dari 1/3?", "a": "Benda yang dibagi 2 potongannya lebih besar daripada benda yang sama dibagi 3."}]
    return dict(slug="pecahan", dom="B", sort=7,
                std_text="Peserta didik membandingkan dan mengurutkan antarpecahan dengan pembilang satu, serta antarpecahan dengan penyebut yang sama.",
                title="Mengenal Pecahan", short_title="Pecahan",
                meta_desc="Latihan pecahan untuk kelas 3 SD: membaca pecahan, bagian yang diarsir, pecahan berpembilang satu, membandingkan pecahan, dan pecahan dari sekumpulan benda. 100 soal dengan kunci jawaban.",
                key_big="Dibagi menjadi bagian sama besar", key_sub="Bawah = semua bagian, atas = bagian yang diambil.",
                body=body, faq=faq, sets=sets)


# ============================================================ 8. uang
COIN = [100, 200, 500, 1000]
NOTE = [1000, 2000, 5000, 10000, 20000]
NCOL = {1000: "#c9d6a3", 2000: "#b9c4d8", 5000: "#d8b98f", 10000: "#c7a6d1", 20000: "#a9d1b6"}


def uang_svg(items):
    """items: [('c'|'n', nilai)]"""
    s, x, y, rowh = [], 6, 6, 0
    for kind, v in items:
        if kind == "c":
            w, h = 52, 52
            if x + w > 470:
                x, y = 6, y + rowh + 8
                rowh = 0
            col = "#d9d9d9" if v != 500 else "#e8c66a"
            s.append("<circle cx='%d' cy='%d' r='25' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x + 26, y + 26, col, INK))
            s.append("<text x='%d' y='%d' text-anchor='middle' font-size='12' font-weight='700'>%s</text>" % (x + 26, y + 30, num(v)))
        else:
            w, h = 104, 52
            if x + w > 470:
                x, y = 6, y + rowh + 8
                rowh = 0
            s.append("<rect x='%d' y='%d' width='100' height='50' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y, NCOL[v], INK))
            s.append("<text x='%d' y='%d' text-anchor='middle' font-size='15' font-weight='700'>%s</text>" % (x + 50, y + 31, rp(v)))
        x += w + 8
        rowh = max(rowh, h)
    W = 480 if y > 6 else x
    return wrap(W, y + rowh + 8, "".join(s), "uang: " + ", ".join(rp(v) for _, v in items))


def u8():
    def hitung():
        items = []
        for _ in range(ri(2, 5)):
            items.append(("n", ch(NOTE[:4])) if R().random() < 0.5 else ("c", ch(COIN)))
        tot = sum(v for _, v in items)
        if tot > 20000:
            return None
        items.sort(key=lambda t: -t[1])
        return mcq("Berapa jumlah uang pada gambar?" + uang_svg(items), rp(tot), [rp(tot + 1000), rp(tot - 100) if tot > 100 else rp(tot + 500), rp(tot + 500), rp(tot - 500)],
                   " + ".join(rp(v) for _, v in items) + " = %s." % rp(tot))

    def koin():
        a, b, c = ri(0, 4), ri(0, 4), ri(1, 5)
        if a + b == 0:
            return None
        tot = a * 500 + b * 200 + c * 100
        x = K().next()
        return mcq("%s punya %d koin Rp500, %d koin Rp200, dan %d koin Rp100. Berapa jumlah uangnya?" % (x, a, b, c), rp(tot),
                   [rp(a * 100 + b * 200 + c * 500), rp(tot + 100), rp(tot - 100) if tot > 100 else rp(tot + 300), rp((a + b + c) * 100)],
                   "%s + %s + %s = %s." % (rp(a * 500), rp(b * 200), rp(c * 100), rp(tot)))

    def tukar():
        big, small = ch([(1000, 500), (1000, 200), (1000, 100), (2000, 1000), (5000, 1000), (10000, 2000), (10000, 5000), (20000, 10000), (2000, 500), (5000, 500)])
        k = ri(1, 3) if big >= 5000 else ri(1, 4)
        if big * k > 20000:
            return None
        n = big * k // small
        return mcq("Uang %s ditukar dengan uang %s. Berapa lembar atau keping uang %s yang didapat?" % (rp(big * k), rp(small), rp(small)),
                   str(n), [str(n + 1), str(n - 1) if n > 1 else str(n + 2), str(n * 2), str(k)],
                   "%s : %s = %d." % (rp(big * k), rp(small), n))

    ITEMS = [("pensil", 2500), ("penghapus", 1500), ("buku tulis", 4000), ("penggaris", 3000), ("roti", 3500), ("susu kotak", 4500),
             ("permen", 500), ("kerupuk", 1000), ("es teh", 2000), ("rautan", 2000), ("pisang goreng", 1500), ("air mineral", 3000)]

    def beli():
        (a, pa), (b, pb) = pool(ITEMS)[:2]
        tot = pa + pb
        x = K().next()
        return mcq("%s membeli %s seharga %s dan %s seharga %s. Berapa yang harus dibayar?" % (x, a, rp(pa), b, rp(pb)), rp(tot),
                   [rp(tot + 1000), rp(abs(pa - pb)) if pa != pb else rp(tot - 500), rp(tot - 1000) if tot > 1000 else rp(tot + 500), rp(tot + 500)],
                   "%s + %s = %s." % (rp(pa), rp(pb), rp(tot)))

    def kembali():
        a, p = ch(ITEMS)
        pay = ch([x for x in (5000, 10000, 20000) if x > p])
        x = K().next()
        return mcq("%s membeli %s seharga %s. Ia membayar dengan uang %s. Berapa uang kembaliannya?" % (x, a, rp(p), rp(pay)), rp(pay - p),
                   [rp(pay + p), rp(pay - p + 1000), rp(pay - p - 500) if pay - p > 500 else rp(pay - p + 500), rp(p)],
                   "Kembalian = %s − %s = %s." % (rp(pay), rp(p), rp(pay - p)))

    def cukup():
        (a, pa), (b, pb) = pool(ITEMS)[:2]
        have = ch([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000])
        tot = pa + pb
        x = K().next()
        if have == tot:
            return None
        good = "Cukup, sisa %s" % rp(have - tot) if have > tot else "Tidak cukup, kurang %s" % rp(tot - have)
        bad = ["Cukup, sisa %s" % rp(abs(have - tot) + 500), "Tidak cukup, kurang %s" % rp(abs(have - tot) + 500),
               "Cukup, sisa %s" % rp(abs(have - tot)) if have < tot else "Tidak cukup, kurang %s" % rp(have - tot), "Uangnya pas"]
        return mcq("%s punya %s. Ia ingin membeli %s (%s) dan %s (%s). Apakah uangnya cukup?" % (x, rp(have), a, rp(pa), b, rp(pb)), good, bad,
                   "Harga semuanya %s + %s = %s. %s." % (rp(pa), rp(pb), rp(tot), good))

    def kali():
        a, p = ch(ITEMS)
        k = ri(2, 4)
        if p * k > 20000:
            return None
        x = K().next()
        return mcq("Harga satu %s adalah %s. %s membeli %d %s. Berapa harga semuanya?" % (a, rp(p), x, k, a), rp(p * k),
                   [rp(p + k), rp(p * (k + 1)), rp(p * (k - 1)), rp(p * k + 500)],
                   "%d × %s = %s." % (k, rp(p), rp(p * k)))

    sets = [("Menghitung uang", [(hitung, 14), (koin, 6)]),
            ("Menukar uang", [(tukar, 14), (hitung, 6)]),
            ("Membeli barang", [(beli, 14), (kali, 6)]),
            ("Uang kembalian", [(kembali, 14), (koin, 6)]),
            ("Cukup atau tidak?", [(cukup, 14), (kali, 6)])]
    body = lesson(
        ["Uang logam (koin) yang sering dipakai: Rp100, Rp200, Rp500, dan Rp1.000. Uang kertas: Rp1.000, Rp2.000, Rp5.000, Rp10.000, Rp20.000, dan seterusnya.",
         "Untuk menghitung uang, mulai dari nilai yang paling besar, lalu tambahkan yang lebih kecil.",
         "Uang kembalian = uang yang dibayarkan − harga barang."],
        [example("Rp5.000 + Rp2.000 + Rp500 + Rp500 = …", ["Rp5.000 + Rp2.000 = Rp7.000", "Rp500 + Rp500 = Rp1.000"], "Rp8.000"),
         example("Membeli roti Rp3.500 dengan uang Rp5.000. Kembaliannya?", ["Rp5.000 − Rp3.500"], "Rp1.500")],
        [["Menghitung banyak lembar, bukan nilainya (3 lembar = Rp3)", "Jumlahkan nilainya: 3 lembar Rp2.000 = Rp6.000"],
         ["Kembalian dihitung dengan menjumlah", "Kembalian = uang dibayar − harga"],
         ["Rp10.000 ditukar Rp5.000 dapat 5 lembar", "Rp10.000 : Rp5.000 = 2 lembar"]])
    faq = [{"q": "Uang apa saja yang ada di Indonesia?", "a": "Uang logam Rp100, Rp200, Rp500, dan Rp1.000, serta uang kertas Rp1.000, Rp2.000, Rp5.000, Rp10.000, Rp20.000, Rp50.000, dan Rp100.000."},
           {"q": "Bagaimana cara menghitung uang kembalian?", "a": "Kurangkan harga barang dari uang yang dibayarkan. Contoh: membayar Rp10.000 untuk barang Rp7.500, kembaliannya Rp2.500."},
           {"q": "Berapa koin Rp500 yang sama dengan Rp2.000?", "a": "4 koin, karena Rp2.000 : Rp500 = 4."}]
    return dict(slug="uang", dom="B", sort=8,
                std_text="Peserta didik menyelesaikan masalah berkaitan dengan uang menggunakan ribuan sebagai satuan.",
                title="Menghitung Uang dan Uang Kembalian", short_title="Uang",
                meta_desc="Latihan uang Rupiah untuk kelas 3 SD: menghitung uang logam dan kertas, menukar uang, membeli barang, uang kembalian, dan cukup atau tidak. 100 soal dengan kunci jawaban.",
                key_big="Kembalian = dibayar − harga", key_sub="Hitung uang dari nilai yang paling besar.",
                body=body, faq=faq, sets=sets)


# ============================================================ 9. pola（Kelas 4 の問題関数を 1.000 までに）
def u9(d4):
    m = {x: lim(maker(d4, x)) for x in ("naik", "turun", "aturan", "tengah", "gambar", "tumbuh", "cerita")}
    sets = [("Pola bilangan naik", [(m["naik"], 14), (m["tengah"], 6)]),
            ("Pola bilangan turun", [(m["turun"], 14), (m["tengah"], 6)]),
            ("Pola gambar", [(m["gambar"], 14), (m["tumbuh"], 6)]),
            ("Aturan pola", [(m["aturan"], 14), (m["naik"], 3), (m["turun"], 3)]),
            ("Soal cerita", [(m["cerita"], 12), (m["tumbuh"], 8)])]
    body = lesson(
        ["Pola adalah susunan yang berulang atau berubah dengan aturan yang sama.",
         "Pada pola bilangan, cari selisih dua bilangan yang berurutan. Jika bertambah, pola naik. Jika berkurang, pola turun.",
         "Pada pola gambar, lihat bagian mana yang berulang, atau berapa yang bertambah setiap langkah."],
        [example("5, 10, 15, 20, … Bilangan berikutnya?", ["Selisihnya 5, pola naik", "20 + 5"], "25"),
         example("90, 80, 70, … Bilangan berikutnya?", ["Selisihnya 10, pola turun", "70 − 10"], "60")],
        [["Hanya melihat dua bilangan pertama", "Periksa aturannya pada semua bilangan"],
         ["Menambah pada pola turun", "Pola turun berarti dikurangi"],
         ["Pola gambar ABAB diteruskan AABB", "Ulangi bagian yang sama: A, B, A, B"]])
    faq = [{"q": "Apa itu pola bilangan?", "a": "Pola bilangan adalah barisan bilangan yang mengikuti aturan tertentu, misalnya selalu ditambah 3: 3, 6, 9, 12."},
           {"q": "Bagaimana mencari bilangan yang hilang di tengah pola?", "a": "Cari aturannya dari bilangan lain, lalu gunakan aturan itu untuk mengisi bilangan yang hilang."},
           {"q": "Apa contoh pola dalam kehidupan sehari-hari?", "a": "Motif batik, susunan ubin lantai, nomor rumah di satu sisi jalan (2, 4, 6, 8), dan hari dalam seminggu."}]
    return dict(slug="pola-bilangan-dan-gambar", dom="A", sort=9,
                std_text="Peserta didik mengidentifikasi, meniru, dan mengembangkan pola gambar atau objek sederhana dan pola bilangan membesar dan mengecil yang melibatkan penjumlahan dan pengurangan pada bilangan cacah sampai 100.",
                title="Pola Bilangan dan Pola Gambar", short_title="Pola Bilangan dan Gambar",
                meta_desc="Latihan pola untuk kelas 3 SD: pola bilangan naik dan turun, pola gambar, aturan pola, dan soal cerita. 100 soal dengan kunci jawaban dan lembar kerja siap cetak.",
                key_big="Cari aturan yang sama", key_sub="Berapa yang ditambah atau dikurangi setiap langkah?",
                body=body, faq=faq, sets=sets)


# ============================================================ 10. kalimat matematika
def u10(d4):
    m = {x: lim(maker(d4, x)) for x in ("a_plus", "a_minus", "benar", "dua_sisi", "model", "selesai")}
    sets = [("Kotak pada penjumlahan", [(m["a_plus"], 20)]),
            ("Kotak pada pengurangan", [(m["a_minus"], 20)]),
            ("Benar atau salah?", [(m["benar"], 12), (m["dua_sisi"], 8)]),
            ("Dari cerita ke kalimat matematika", [(m["model"], 20)]),
            ("Soal cerita", [(m["selesai"], 12), (m["a_plus"], 4), (m["a_minus"], 4)])]
    body = lesson(
        ["Kalimat matematika adalah kalimat yang ditulis dengan bilangan dan tanda, misalnya 25 + □ = 40.",
         "Tanda = berarti kedua sisi sama nilainya.",
         "Untuk mencari □ pada penjumlahan, kurangkan. Untuk mencari □ pada pengurangan, pikirkan kebalikannya."],
        [example("35 + □ = 60", ["□ = 60 − 35"], "25"),
         example("□ − 18 = 30", ["□ = 30 + 18"], "48")],
        [["35 + □ = 60, □ diisi 95 (dijumlah)", "Kurangkan: 60 − 35 = 25"],
         ["Mengira tanda = berarti “hasilnya”", "= berarti kedua sisi sama: 10 + 5 = 12 + 3"],
         ["□ − 18 = 30, □ diisi 12", "□ = 30 + 18 = 48"]])
    faq = [{"q": "Apa itu kalimat matematika?", "a": "Kalimat yang memakai bilangan dan tanda operasi, seperti 12 + 8 = 20 atau 30 − □ = 10."},
           {"q": "Bagaimana cara mencari bilangan dalam kotak?", "a": "Gunakan kebalikannya. Penjumlahan dicek dengan pengurangan, dan pengurangan dicek dengan penjumlahan."},
           {"q": "Apa arti tanda sama dengan?", "a": "Tanda = berarti nilai di sebelah kiri sama dengan nilai di sebelah kanan."}]
    return dict(slug="kalimat-matematika", dom="A", sort=10,
                std_text="Peserta didik menemukan nilai yang belum diketahui dalam kalimat matematika yang berkaitan dengan penjumlahan dan pengurangan pada bilangan cacah sampai 100.",
                title="Kalimat Matematika dan Bilangan yang Hilang", short_title="Kalimat Matematika",
                meta_desc="Latihan kalimat matematika untuk kelas 3 SD: mengisi kotak pada penjumlahan dan pengurangan, arti tanda sama dengan, membuat kalimat matematika dari cerita. 100 soal dengan kunci jawaban.",
                key_big="35 + □ = 60, □ = 60 − 35", key_sub="Tanda = berarti kedua sisi sama nilainya.",
                body=body, faq=faq, sets=sets)


# ============================================================ 11. panjang dan berat
def u11(d4):
    m_cm, ukur, banding, satuan, cerita = (lim(maker(d4, x)) for x in ("m_cm", "ukur", "banding", "satuan", "cerita"))
    banding = lim(maker(d4, "banding"), bad=("kg", " g"))
    cerita = lim(maker(d4, "cerita"), bad=(" g", "kg"))

    BENDA = [("semangka", 4), ("karung beras", 25), ("tas sekolah", 3), ("kucing", 4), ("sekarung pasir", 50), ("adik bayi", 6),
             ("kambing", 30), ("televisi", 8), ("labu", 2), ("kardus buku", 10)]

    def kg():
        (a, wa), (b, wb) = pool(BENDA)[:2]
        if wa == wb:
            return None
        big = R().random() < 0.5
        g = a if (wa > wb) == big else b
        return mcq("Berat %s %d kg. Berat %s %d kg. Manakah yang lebih %s?" % (a, wa, b, wb, "berat" if big else "ringan"), cap(g),
                   [cap(b if g == a else a), "Sama berat", "Tidak bisa dibandingkan"],
                   "%d kg %s %d kg." % (wa, rel(wa, wb).replace("&lt;", "&lt;").replace("&gt;", "&gt;"), wb))

    def timbang():
        a, b = ri(3, 30), ri(2, 20)
        x = K().next()
        if R().random() < 0.5:
            return mcq("Berat %s %d kg. Berat tasnya %d kg. Jika %s menimbang badan sambil membawa tas, berapa kg hasilnya?" % (x, a + 20, b if b < 8 else 3, x),
                       "%d kg" % (a + 20 + (b if b < 8 else 3)), ["%d kg" % (a + 20), "%d kg" % (a + 20 - (b if b < 8 else 3)), "%d kg" % (a + 21 + (b if b < 8 else 3))],
                       "%d + %d = %d kg." % (a + 20, b if b < 8 else 3, a + 20 + (b if b < 8 else 3)))
        if a <= b:
            return None
        return mcq("Ibu membeli %d kg beras. Sebanyak %d kg sudah dimasak. Berapa kg beras yang tersisa?" % (a, b), "%d kg" % (a - b),
                   ["%d kg" % (a + b), "%d kg" % (a - b + 1), "%d kg" % (a - b - 1) if a - b > 1 else "%d kg" % (a - b + 2)],
                   "%d − %d = %d kg." % (a, b, a - b))

    def gram():
        a, b = ri(1, 9) * 100, ri(1, 9) * 50
        if a == b:
            return None
        return stmt("%d g" % a, "%d g" % b, a, b, "Bandingkan bilangannya: %d g %s %d g." % (a, rel(a, b), b))

    def satuan_berat():
        BG = [("berat sebutir telur", "g"), ("berat sepotong roti", "g"), ("berat karung beras", "kg"), ("berat seekor sapi", "kg"),
              ("berat sebatang pensil", "g"), ("berat badan ayah", "kg"), ("berat sebuah penghapus", "g"), ("berat sekarung jagung", "kg")]
        what, g = ch(BG)
        return mcq("Satuan yang tepat untuk %s adalah …" % what, g, [x for x in ["g", "kg", "cm", "m"] if x != g],
                   "%s diukur dengan %s." % (cap(what), "kilogram (kg) karena berat" if g == "kg" else "gram (g) karena ringan"))

    sets = [("Meter dan sentimeter", [(m_cm, 14), (satuan, 6)]),
            ("Mengukur dengan penggaris", [(ukur, 20)]),
            ("Membandingkan panjang", [(banding, 12), (cerita, 8)]),
            ("Kilogram dan gram", [(kg, 8), (gram, 6), (satuan_berat, 6)]),
            ("Soal cerita", [(timbang, 12), (cerita, 8)])]
    body = lesson(
        ["Panjang diukur dengan satuan sentimeter (cm) dan meter (m). 1 m = 100 cm.",
         "Saat mengukur dengan penggaris, letakkan ujung benda tepat di angka 0.",
         "Berat diukur dengan gram (g) untuk benda ringan dan kilogram (kg) untuk benda berat."],
        [example("2 m 35 cm = … cm", ["2 m = 200 cm", "200 cm + 35 cm"], "235 cm"),
         example("Satuan untuk berat karung beras?", ["Karung beras berat"], "kilogram (kg)")],
        [["Mengukur mulai dari angka 1 pada penggaris", "Mulai dari angka 0"],
         ["1 m = 10 cm", "1 m = 100 cm"],
         ["Berat telur ditulis dalam kg", "Benda ringan memakai gram"]])
    faq = [{"q": "Berapa sentimeter dalam 1 meter?", "a": "1 meter sama dengan 100 sentimeter."},
           {"q": "Kapan memakai gram dan kapan kilogram?", "a": "Gram dipakai untuk benda ringan seperti telur atau pensil. Kilogram dipakai untuk benda berat seperti beras atau badan."},
           {"q": "Bagaimana cara mengukur dengan penggaris?", "a": "Letakkan ujung benda di angka 0, lalu baca angka di ujung yang lain."}]
    return dict(slug="pengukuran-panjang-dan-berat", dom="P", sort=11,
                std_text="Peserta didik mengukur panjang dan berat benda menggunakan satuan baku, serta menentukan hubungan antarsatuan baku panjang (cm, m).",
                title="Mengukur Panjang dan Berat", short_title="Panjang dan Berat",
                meta_desc="Latihan pengukuran untuk kelas 3 SD: meter dan sentimeter, mengukur dengan penggaris, membandingkan panjang, kilogram dan gram, dan soal cerita. 100 soal dengan kunci jawaban.",
                key_big="1 m = 100 cm", key_sub="Benda ringan memakai gram, benda berat memakai kilogram.",
                body=body, faq=faq, sets=sets)


# ============================================================ 12. luas dan volume
def u12(d4):
    hitung, pp, banding, vol, nonbaku, ubin, kotak = (lim(maker(d4, x)) for x in ("hitung", "persegi_panjang", "banding", "vol", "nonbaku", "ubin", "kotak"))
    sets = [("Menghitung petak", [(hitung, 20)]),
            ("Lebih luas atau lebih sempit", [(banding, 14), (hitung, 6)]),
            ("Baris dan kolom petak", [(pp, 14), (ubin, 6)]),
            ("Kubus satuan", [(vol, 20)]),
            ("Satuan tidak baku", [(nonbaku, 10), (kotak, 10)])]
    body = lesson(
        ["Luas adalah besar daerah yang ditutupi sebuah bangun. Luas bisa diukur dengan menghitung petak satuan.",
         "Jika petak tersusun dalam baris dan kolom, luasnya = banyak baris × banyak petak di setiap baris.",
         "Volume adalah besar ruang yang ditempati benda. Volume bisa diukur dengan menghitung kubus satuan."],
        [example("Persegi panjang tersusun dari 3 baris, setiap baris 5 petak. Luasnya?", ["3 × 5"], "15 petak"),
         example("Balok tersusun dari 2 lapis, setiap lapis 6 kubus. Volumenya?", ["2 × 6"], "12 kubus satuan")],
        [["Menghitung sisi luar saja", "Hitung semua petak di dalam bangun"],
         ["Kubus yang tersembunyi tidak dihitung", "Kubus di belakang dan di bawah juga dihitung"],
         ["Membandingkan dengan satuan yang berbeda ukuran", "Pakai satuan yang sama untuk membandingkan"]])
    faq = [{"q": "Apa itu luas?", "a": "Luas adalah ukuran daerah permukaan. Di kelas 3, luas diukur dengan menghitung petak satuan atau benda yang sama ukurannya."},
           {"q": "Apa itu volume?", "a": "Volume adalah ukuran ruang yang ditempati benda. Kita bisa mengukurnya dengan menghitung kubus satuan."},
           {"q": "Apa itu satuan tidak baku?", "a": "Satuan tidak baku adalah benda sehari-hari yang dipakai untuk mengukur, misalnya ubin, buku, atau kotak korek api."}]
    return dict(slug="luas-dan-volume", dom="P", sort=12,
                std_text="Peserta didik mengukur dan mengestimasi luas dan volume menggunakan satuan tidak baku dan satuan baku berupa bilangan cacah.",
                title="Luas dengan Petak dan Volume dengan Kubus", short_title="Luas dan Volume",
                meta_desc="Latihan luas dan volume untuk kelas 3 SD: menghitung petak satuan, membandingkan luas, baris dan kolom, kubus satuan, dan satuan tidak baku. 100 soal dengan kunci jawaban.",
                key_big="Hitung petak dan kubus satuan", key_sub="Luas = baris × kolom petak.",
                body=body, faq=faq, sets=sets)


# ============================================================ 13. bangun datar
def u13(d15):
    m = {x: maker(d15, x) for x in ("nama_segi", "dari_sisi", "hitung", "nama_empat", "ciri", "benar", "siku")}
    sets = [("Mengenal bangun datar", [(m["nama_segi"], 14), (m["dari_sisi"], 6)]),
            ("Sisi dan titik sudut", [(m["hitung"], 20)]),
            ("Persegi dan persegi panjang", [(m["nama_empat"], 14), (m["ciri"], 6)]),
            ("Sudut siku-siku", [(m["siku"], 14), (m["benar"], 6)]),
            ("Benar atau salah?", [(m["benar"], 12), (m["dari_sisi"], 4), (m["hitung"], 4)])]
    body = lesson(
        ["Bangun datar adalah bangun yang rata, seperti segitiga, persegi, persegi panjang, dan lingkaran.",
         "Sisi adalah garis lurus pada tepi bangun. Titik sudut adalah tempat dua sisi bertemu.",
         "Persegi punya 4 sisi sama panjang dan 4 sudut siku-siku. Persegi panjang punya sisi berhadapan yang sama panjang dan 4 sudut siku-siku."],
        [example("Berapa sisi segi lima?", ["Segi lima punya 5 sisi dan 5 titik sudut"], "5"),
         example("Sudut siku-siku seperti apa?", ["Seperti pojok buku atau pojok meja"], "Tegak lurus seperti huruf L")],
        [["Lingkaran dikira punya sudut", "Lingkaran tidak punya sisi lurus dan titik sudut"],
         ["Semua bangun bersisi 4 disebut persegi", "Persegi harus punya 4 sisi sama panjang"],
         ["Menghitung titik sudut lebih dari sekali", "Beri tanda setiap titik yang sudah dihitung"]])
    faq = [{"q": "Apa beda persegi dan persegi panjang?", "a": "Keduanya punya 4 sudut siku-siku. Persegi punya 4 sisi sama panjang, persegi panjang hanya sisi yang berhadapan yang sama panjang."},
           {"q": "Berapa sisi segitiga?", "a": "Segitiga punya 3 sisi dan 3 titik sudut."},
           {"q": "Apa itu sudut siku-siku?", "a": "Sudut siku-siku adalah sudut seperti pojok buku atau pojok papan tulis."}]
    return dict(slug="bangun-datar", dom="G", sort=13,
                std_text="Peserta didik mendeskripsikan ciri berbagai bentuk bangun datar (segi empat, segitiga, segi banyak).",
                title="Mengenal Bangun Datar", short_title="Bangun Datar",
                meta_desc="Latihan bangun datar untuk kelas 3 SD: nama bangun datar, sisi dan titik sudut, persegi dan persegi panjang, sudut siku-siku. 100 soal dengan kunci jawaban dan lembar kerja.",
                key_big="Hitung sisi dan titik sudut", key_sub="Persegi: 4 sisi sama panjang, 4 sudut siku-siku.",
                body=body, faq=faq, sets=sets)


# ============================================================ 14. piktogram dan diagram batang
def u14(d17):
    ms = []
    for _, parts in d17["sets"]:
        for mk, _n in parts:
            if mk not in ms:
                ms.append(mk)
    by = {}
    for mk in ms:
        by.setdefault(mk.__name__, []).append(lim(mk, 100))
    turus, tabel, tinggi = by["turus"][0], by["tabel"][0], by["tinggi"][0]
    mks = by["mk"]
    sets = [("Turus dan tabel", [(turus, 12), (tabel, 8)]),
            ("Membaca piktogram", [(mks[0], 7), (mks[1], 7), (mks[2], 6)]),
            ("Membaca diagram batang", [(mks[4], 7), (mks[5], 7), (mks[6], 6)]),
            ("Membandingkan data", [(tinggi, 8), (mks[3], 6), (mks[7], 6)]),
            ("Campuran", [(mks[8], 7), (mks[9], 7), (tabel, 6)])]
    body = lesson(
        ["Data bisa dicatat dengan turus. Satu garis = 1, dan ikatan lima garis (IIII dengan garis miring) = 5.",
         "Piktogram memakai gambar. Lihat dulu keterangan: satu gambar mewakili berapa.",
         "Pada diagram batang, makin tinggi batangnya, makin banyak datanya. Baca angka pada sumbu tegak."],
        [example("Satu gambar mewakili 2 buku. Ada 4 gambar. Berapa bukunya?", ["4 × 2"], "8 buku"),
         example("Batang A sampai angka 7, batang B sampai 4. Selisihnya?", ["7 − 4"], "3")],
        [["Menghitung gambar tanpa melihat keterangan", "Kalikan banyak gambar dengan nilai satu gambar"],
         ["Membaca batang dari ujung yang salah", "Baca angka sejajar puncak batang"],
         ["Ikatan turus dihitung 4", "Ikatan turus (4 garis + 1 garis miring) = 5"]])
    faq = [{"q": "Apa itu piktogram?", "a": "Piktogram adalah penyajian data dengan gambar. Setiap gambar mewakili sejumlah benda sesuai keterangannya."},
           {"q": "Apa itu turus?", "a": "Turus adalah tanda garis untuk mencatat data satu per satu. Setiap lima turus diikat agar mudah dihitung."},
           {"q": "Bagaimana membaca diagram batang?", "a": "Lihat puncak setiap batang lalu baca angka di sumbu tegak yang sejajar dengan puncak itu."}]
    return dict(slug="piktogram-dan-diagram-batang", dom="D", sort=14,
                std_text="Peserta didik mengurutkan, membandingkan, menyajikan, dan menganalisis data banyak benda dalam bentuk tabel, diagram gambar, piktogram, dan diagram batang.",
                title="Turus, Piktogram, dan Diagram Batang", short_title="Piktogram dan Diagram Batang",
                meta_desc="Latihan data untuk kelas 3 SD: turus, tabel, membaca piktogram dan diagram batang, dan membandingkan data. 100 soal dengan kunci jawaban dan lembar kerja siap cetak.",
                key_big="Lihat keterangan gambarnya", key_sub="Batang makin tinggi, data makin banyak.",
                body=body, faq=faq, sets=sets)


# ------------------------------------------------------------
NEED4 = {5: 5, 6: 5, 7: 8, 9: 12, 10: 11, 11: 13, 12: 14, 13: 15, 14: 17}
UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14]


def build(i):
    import id_k4
    rnd = random.Random(40300 + i)
    A.setup(rnd)
    fn = UNITS[i - 1]
    if i in NEED4:
        d4 = id_k4.UNITS[NEED4[i] - 1]()
        d = fn(d4)
    else:
        d = fn()
    seen = set()
    sets = [(t, mix(rnd, seen, parts)) for t, parts in d["sets"]]
    make_unit(rnd, d["slug"], d["dom"], d["std_text"], d["title"], d["short_title"], d["meta_desc"],
              d["key_big"], d["key_sub"], d["body"], d["faq"], sets, d["sort"], grade=G, fase="Fase B")
    return d["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    for i in range(1, len(UNITS) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(i), flush=True)
