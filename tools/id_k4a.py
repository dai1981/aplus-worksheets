# -*- coding: utf-8 -*-
"""Indonesia Kelas 4 (Fase B): 絵の部品と Bilangan の単元（1〜7）。id_k4.py から使う。"""
import math
from fractions import Fraction as F
from id_common import (num, rp, u, NB, Kids, mcq, mix, lesson, example, table, make_unit, wrap, fr,
                       garis_bilangan, nilai_tempat, blok, bersusun, text, line, INK, GREEN, FILL, RED, BLUE)

R = None
K = None


def setup(rnd):
    global R, K
    R = rnd
    K = Kids(rnd)


def ri(a, b):
    return R.randint(a, b)


def ch(xs):
    return R.choice(xs)


def pool(xs):
    """場面を 1 回ずつ使う：mk の中で pop() する"""
    xs = list(xs)
    R.shuffle(xs)
    return xs


# ------------------------------------------------------------ 数の読み方
_S = ["nol", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan"]


def terbilang(n):
    n = int(n)
    if n < 10:
        return _S[n]
    if n < 20:
        return "sepuluh" if n == 10 else "sebelas" if n == 11 else _S[n - 10] + " belas"
    if n < 100:
        p, s = divmod(n, 10)
        return _S[p] + " puluh" + (" " + _S[s] if s else "")
    if n < 1000:
        r, s = divmod(n, 100)
        head = "seratus" if r == 1 else _S[r] + " ratus"
        return head + (" " + terbilang(s) if s else "")
    if n < 1000000:
        r, s = divmod(n, 1000)
        head = "seribu" if r == 1 else terbilang(r) + " ribu"
        return head + (" " + terbilang(s) if s else "")
    raise ValueError(n)


def cap(s):
    return s[0].upper() + s[1:]


def rel(a, b):
    return "&lt;" if a < b else "&gt;" if a > b else "="


def stmt(sa, sb, a, b, e):
    """比較の 4 択（どれが正しい文か）"""
    r = rel(a, b)
    ops = ["&lt;", "&gt;", "="]
    good = "%s %s %s" % (sa, r, sb)
    bad = ["%s %s %s" % (sa, o, sb) for o in ops if o != r]
    rr = rel(b, a)
    flip = [o for o in ops if o != rr][0]
    bad.append("%s %s %s" % (sb, flip, sa))
    return mcq("Bandingkan %s dan %s. Pernyataan yang benar adalah …" % (sa, sb), good, bad, e)


# ------------------------------------------------------------ 絵
def titik(rows, cols, col="#e07a5f"):
    s = []
    for i in range(rows):
        for j in range(cols):
            s.append("<circle cx='%d' cy='%d' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (18 + j * 26, 18 + i * 26, col, INK))
    return wrap(cols * 26 + 10, rows * 26 + 10, "".join(s), "%d baris, setiap baris %d titik" % (rows, cols))


def kelompok(g, k, col="#f2c94c"):
    s, x = [], 6
    per = min(k, 5)
    rws = (k + per - 1) // per
    w, h = per * 18 + 14, rws * 18 + 14
    for i in range(g):
        s.append("<rect x='%d' y='6' width='%d' height='%d' rx='12' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, w, h, FILL, GREEN))
        for t in range(k):
            s.append("<circle cx='%d' cy='%d' r='6.5' fill='%s' stroke='%s'/>" % (x + 14 + (t % per) * 18, 20 + (t // per) * 18, col, INK))
        x += w + 10
    return wrap(x, h + 12, "".join(s), "%d kelompok, setiap kelompok %d benda" % (g, k))


def bar_frac(n, k, w=300, h=40, col="#7fb3d5"):
    s = []
    cw = w / float(n)
    for i in range(n):
        s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (6 + i * cw, cw, h, col if i < k else "#ffffff", INK))
    return wrap(w + 12, h + 12, "".join(s), "pita dibagi %d bagian sama besar, %d bagian diarsir" % (n, k))


def pie(n, k, r=60, col="#f4a261"):
    cx = cy = r + 6
    s = []
    for i in range(n):
        a0 = -math.pi / 2 + 2 * math.pi * i / n
        a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        large = 1 if a1 - a0 > math.pi else 0
        if n == 1:
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, col if k else "#fff", INK))
        else:
            s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (cx, cy, x0, y0, r, r, large, x1, y1, col if i < k else "#ffffff", INK))
    return wrap(2 * r + 12, 2 * r + 12, "".join(s), "lingkaran dibagi %d bagian sama besar, %d bagian diarsir" % (n, k))


def frac_pic(n, k):
    return pie(n, k) if R.random() < 0.5 else bar_frac(n, k)


# ============================================================ 1. bilangan cacah sampai 10.000
def wrong_reads(n):
    s = str(n)
    out = []
    for i in range(len(s) - 1):
        t = list(s)
        t[i], t[i + 1] = t[i + 1], t[i]
        t = "".join(t)
        if t[0] != "0" and int(t) != n:
            out.append(int(t))
    out += [n + 1000 if n < 9000 else n - 1000, n + 100 if n % 1000 < 900 else n - 100, n + 10 if n % 100 < 90 else n - 10]
    return out


def n4(zero=False):
    d = [ri(1, 9), ri(0, 9), ri(0, 9), ri(0, 9)]
    if zero:
        d[ch([1, 2, 3])] = 0
    return int("".join(map(str, d)))


def u1():
    def baca():
        n = n4(R.random() < 0.4)
        ws = [cap(terbilang(w)) for w in wrong_reads(n)]
        return mcq("Bilangan <b>%s</b> dibaca …" % num(n), cap(terbilang(n)), ws,
                   "%s = %s." % (num(n), terbilang(n)))

    def tulis():
        n = n4(R.random() < 0.6)
        return mcq("Lambang bilangan dari <i>%s</i> adalah …" % terbilang(n), num(n),
                   [num(w) for w in wrong_reads(n)] + [num(n * 10)],
                   "%s ditulis %s." % (cap(terbilang(n)), num(n)))

    PL = ["satuan", "puluhan", "ratusan", "ribuan"]

    def nilai():
        n = n4()
        s = str(n)
        i = ri(0, 3)
        d = int(s[i])
        if d == 0 or s.count(s[i]) > 1:
            return None
        p = 3 - i
        return mcq("Pada bilangan %s, angka %d bernilai …" % (num(n), d), num(d * 10 ** p),
                   [num(d * 10 ** q) for q in range(4) if q != p],
                   "Angka %d berada di tempat %s, jadi nilainya %s." % (d, PL[p], num(d * 10 ** p)))

    def tempat():
        n = n4()
        s = str(n)
        i = ri(0, 3)
        if s.count(s[i]) > 1:
            return None
        p = 3 - i
        return mcq("Pada bilangan %s, angka %s menempati tempat …" % (num(n), s[i]), PL[p],
                   [x for x in PL if x != PL[p]],
                   "Dari kanan: satuan, puluhan, ratusan, ribuan. Angka %s ada di tempat %s." % (s[i], PL[p]))

    def gambar():
        a, b, c, d = ri(1, 4), ri(0, 9), ri(0, 9), ri(0, 9)
        if b + c + d < 3:
            return None
        n = a * 1000 + b * 100 + c * 10 + d
        return mcq("Bilangan yang ditunjukkan gambar adalah …" + blok(b, c, d, ribu=a), num(n),
                   [num(w) for w in wrong_reads(n)] + [num(a * 1000 + b * 100 + d * 10 + c)],
                   "%d ribuan, %d ratusan, %d puluhan, %d satuan = %s." % (a, b, c, d, num(n)))

    def tabel():
        n = n4(R.random() < 0.5)
        return mcq("Bilangan pada tabel nilai tempat ini adalah …" + nilai_tempat(n), num(n),
                   [num(w) for w in wrong_reads(n)] + [num(int(str(n)[::-1])) if str(n)[-1] != "0" else None],
                   "Baca dari ribuan sampai satuan: %s." % num(n))

    def garis():
        lo = ri(1, 8) * 1000
        step = ch([100, 100, 10])
        if step == 10:
            lo = lo + ri(0, 9) * 100
        hi = lo + step * 10
        k = ri(1, 9)
        if k == 5:
            return None
        v = lo + k * step
        return mcq("Bilangan yang ditunjuk huruf A adalah …" + garis_bilangan(lo, hi, step, marks=[(v, "A")]), num(v),
                   [num(lo + (10 - k) * step), num(v + step), num(v - step), num(lo + k * step // 10 if step == 100 else lo + k)],
                   "Satu garis kecil = %s. A ada %d garis dari %s, jadi %s." % (num(step), k, num(lo), num(v)))

    def sesudah():
        n = n4()
        d = ch([1, 10, 100, 1000])
        up = R.random() < 0.5
        if (up and n + d > 10000) or (not up and n - d < 1000):
            return None
        v = n + d if up else n - d
        word = "lebih dari" if up else "kurang dari"
        return mcq("Bilangan yang %s %s %s adalah …" % (num(d), word, num(n)), num(v),
                   [num(n - d if up else n + d)] + [num(n + x if up else n - x) for x in (1, 10, 100, 1000) if x != d],
                   "%s %s %s = %s." % (num(n), "+" if up else "−", num(d), num(v)))

    def cerita():
        n = n4(R.random() < 0.4)
        ctx = ch(["Di perpustakaan sekolah ada %s buku.", "Sebuah stadion mini memiliki %s kursi.",
                  "Pada hari Minggu, %s orang mengunjungi kebun binatang.", "Panen padi Pak Slamet adalah %s kilogram.",
                  "Jarak dua desa adalah %s meter.", "Sebuah pabrik membuat %s botol minum dalam sehari."]) % num(n)
        return mcq(ctx + " Bilangan itu dibaca …", cap(terbilang(n)), [cap(terbilang(w)) for w in wrong_reads(n)],
                   "%s dibaca %s." % (num(n), terbilang(n)))

    sets = [("Membaca bilangan", [(baca, 14), (cerita, 6)]),
            ("Menulis lambang bilangan", [(tulis, 12), (tabel, 8)]),
            ("Nilai tempat", [(nilai, 10), (tempat, 6), (gambar, 4)]),
            ("Garis bilangan", [(garis, 12), (sesudah, 8)]),
            ("Campuran", [(gambar, 5), (tulis, 4), (nilai, 4), (sesudah, 4), (garis, 3)])]
    body = lesson(
        ["Bilangan sampai 10.000 punya empat tempat: ribuan, ratusan, puluhan, dan satuan.",
         "Baca dari kiri: ribuan dulu, lalu ratusan, puluhan, dan satuan. Angka 0 tidak dibaca.",
         "Untuk 1.000 kita baca <i>seribu</i>, dan untuk 100 kita baca <i>seratus</i>.",
         "Nilai sebuah angka bergantung pada tempatnya. Pada 4.536, angka 5 bernilai 500."],
        [example("Bacalah 3.208.", ["3 ribuan → tiga ribu", "2 ratusan → dua ratus", "0 puluhan → tidak dibaca", "8 satuan → delapan"],
                 "tiga ribu dua ratus delapan"),
         example("Tulislah <i>tujuh ribu empat puluh</i>.", ["ribuan 7, ratusan 0, puluhan 4, satuan 0"], "7.040")],
        [["7.040 ditulis 7.40 atau 740", "Tempat yang kosong diisi 0: 7.040"],
         ["1.500 dibaca <i>satu ribu lima ratus</i>", "1.000 dibaca <i>seribu</i>: seribu lima ratus"],
         ["Nilai angka 6 pada 6.245 adalah 6", "Angka 6 di tempat ribuan, nilainya 6.000"]],
        table(["Ribuan", "Ratusan", "Puluhan", "Satuan"], [["4", "5", "3", "6"]]))
    faq = [{"q": "Bagaimana cara membaca bilangan empat angka?", "a": "Baca dari kiri: ribuan, ratusan, puluhan, lalu satuan. Contoh: 4.536 dibaca empat ribu lima ratus tiga puluh enam."},
           {"q": "Kenapa 1.000 dibaca seribu?", "a": "Dalam bahasa Indonesia, satu ribu disingkat menjadi seribu, sama seperti satu ratus menjadi seratus dan satu puluh menjadi sepuluh."},
           {"q": "Apa itu nilai tempat?", "a": "Nilai tempat adalah nilai sebuah angka menurut posisinya. Angka 3 pada 3.000 bernilai tiga ribu, tetapi pada 30 bernilai tiga puluh."}]
    return dict(slug="bilangan-cacah-sampai-10000", dom="B", sort=1,
                std_text="Peserta didik menunjukkan pemahaman bilangan cacah sampai 10.000: membaca, menulis, dan menentukan nilai tempat.",
                title="Bilangan Cacah sampai 10.000", short_title="Bilangan Cacah sampai 10.000",
                meta_desc="Latihan membaca dan menulis bilangan sampai 10.000, nilai tempat, dan garis bilangan untuk kelas 4 SD. 100 soal pilihan ganda dengan kunci jawaban dan lembar kerja siap cetak.",
                key_big="Ribuan, ratusan, puluhan, satuan", key_sub="Baca dari kiri. Angka 0 tidak dibaca.",
                body=body, faq=faq, sets=sets)


# ============================================================ 2. membandingkan dan mengurutkan
def u2():
    def near(n):
        s = list(str(n))
        i = ri(1, 3)
        d = int(s[i])
        s[i] = str((d + ri(1, 8)) % 10)
        return int("".join(s))

    def banding():
        a = n4()
        b = ch([near(a), near(a), n4(), int(str(a)[:2] + str(a)[3] + str(a)[2])])
        if b == a:
            return None
        return stmt(num(a), num(b), a, b, "Bandingkan dari tempat ribuan. Jika sama, lihat ratusan, lalu puluhan. %s %s %s."
                    % (num(a), rel(a, b), num(b)))

    def banding3():
        a = n4()
        b = ri(100, 999)
        if R.random() < 0.5:
            a, b = b, a
        return stmt(num(a), num(b), a, b, "Bilangan dengan lebih banyak angka lebih besar. %s %s %s." % (num(a), rel(a, b), num(b)))

    def grp():
        base = ri(1, 9) * 1000 + ri(0, 8) * 100
        xs = set()
        while len(xs) < 4:
            xs.add(base + (ri(0, 99) if R.random() < 0.7 else ri(0, 9) * 10))
        return sorted(xs)

    def ekstrem():
        xs = grp()
        big = R.random() < 0.5
        c = max(xs) if big else min(xs)
        return mcq("Bilangan %s dari %s adalah …" % ("terbesar" if big else "terkecil", ", ".join(num(x) for x in pool(xs))),
                   num(c), [num(x) for x in xs if x != c],
                   "Ribuan dan ratusannya sama, jadi bandingkan puluhan dan satuan. Yang %s adalah %s."
                   % ("terbesar" if big else "terkecil", num(c)))

    def urut():
        xs = grp()
        up = R.random() < 0.5
        good = sorted(xs, reverse=not up)
        sh = pool(xs)
        w1 = sorted(xs, reverse=up)
        w2 = sorted(xs, key=lambda x: (x % 10, x), reverse=not up)
        w3 = list(good)
        w3[1], w3[2] = w3[2], w3[1]
        f = lambda ys: ", ".join(num(y) for y in ys)
        return mcq("Urutan bilangan %s dari yang %s adalah …" % (f(sh), "terkecil ke terbesar" if up else "terbesar ke terkecil"),
                   f(good), [f(w1), f(w2), f(w3)],
                   "Bandingkan tempat demi tempat dari kiri. Urutannya %s." % f(good))

    def lebih():
        a = n4()
        big = R.random() < 0.5
        cands = [near(a) for _ in range(12)]
        good = [c for c in cands if (c > a) == big and c != a]
        bad = [c for c in cands if (c < a) == big and c != a]
        if not good or len(set(bad)) < 3:
            return None
        g = good[0]
        return mcq("Bilangan yang %s dari %s adalah …" % ("lebih besar" if big else "lebih kecil", num(a)), num(g),
                   [num(b) for b in bad], "Bandingkan tempat demi tempat. %s %s %s." % (num(g), rel(g, a), num(a)))

    DAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    CTX = [("pengunjung museum", "orang"), ("botol air yang terjual", "botol"), ("buku yang dipinjam", "buku"),
           ("telur yang dihasilkan peternakan", "butir"), ("penumpang kereta", "orang"), ("bibit pohon yang ditanam", "bibit")]

    def cerita():
        thing, unit = ch(CTX)
        ds = pool(DAYS)[:4]
        xs = grp()
        R.shuffle(xs)
        big = R.random() < 0.5
        i = xs.index(max(xs) if big else min(xs))
        rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (d, num(x)) for d, x in zip(ds, xs))
        t = "<table class='sn-table' style='width:auto'><thead><tr><th>Hari</th><th>Banyak %s</th></tr></thead><tbody>%s</tbody></table>" % (unit, rows)
        return mcq("Tabel menunjukkan banyak %s. Pada hari apa %s paling %s?%s" % (thing, thing, "banyak" if big else "sedikit", t),
                   ds[i], [d for d in ds if d != ds[i]],
                   "%s adalah bilangan %s, yaitu pada hari %s." % (num(xs[i]), "terbesar" if big else "terkecil", ds[i]))

    def antara():
        lo = ri(1, 9) * 1000 + ri(0, 8) * 100
        hi = lo + 100
        g = lo + ri(1, 99)
        bad = [lo - ri(1, 99), hi + ri(1, 99), lo + 1000 + ri(1, 99), lo - 100 + ri(1, 99) if lo >= 1100 else hi + 200]
        return mcq("Bilangan yang terletak di antara %s dan %s adalah …" % (num(lo), num(hi)), num(g), [num(b) for b in bad],
                   "%s lebih besar dari %s dan lebih kecil dari %s." % (num(g), num(lo), num(hi)))

    sets = [("Membandingkan dua bilangan", [(banding, 14), (banding3, 6)]),
            ("Terbesar dan terkecil", [(ekstrem, 14), (lebih, 6)]),
            ("Mengurutkan bilangan", [(urut, 16), (antara, 4)]),
            ("Lebih besar atau lebih kecil", [(lebih, 8), (antara, 6), (banding, 6)]),
            ("Soal cerita", [(cerita, 14), (urut, 3), (ekstrem, 3)])]
    body = lesson(
        ["Untuk membandingkan dua bilangan, lihat banyak angkanya dulu. Bilangan empat angka selalu lebih besar dari bilangan tiga angka.",
         "Jika banyak angkanya sama, bandingkan dari kiri: ribuan, ratusan, puluhan, lalu satuan.",
         "Tanda &lt; berarti <i>kurang dari</i>, tanda &gt; berarti <i>lebih dari</i>. Ujung yang terbuka menghadap bilangan yang lebih besar."],
        [example("Bandingkan 5.372 dan 5.327.", ["Ribuan sama (5), ratusan sama (3)", "Puluhan: 7 &gt; 2"], "5.372 &gt; 5.327"),
         example("Urutkan dari terkecil: 2.418, 2.184, 2.481.", ["Ribuan sama, ratusan: 1 &lt; 4", "2.418 dan 2.481: puluhan 1 &lt; 8"], "2.184, 2.418, 2.481")],
        [["Membandingkan dari angka paling kanan", "Mulai dari tempat terbesar (paling kiri)"],
         ["999 &gt; 1.000 karena angkanya 9", "1.000 punya empat angka, jadi 1.000 &gt; 999"],
         ["Tertukar arah urutan", "Baca lagi soalnya: terkecil ke terbesar atau sebaliknya"]])
    faq = [{"q": "Bagaimana cara membandingkan bilangan empat angka?", "a": "Bandingkan angka ribuan terlebih dahulu. Jika sama, lanjutkan ke ratusan, puluhan, lalu satuan sampai ada yang berbeda."},
           {"q": "Apa arti tanda < dan >?", "a": "Tanda < dibaca kurang dari, dan tanda > dibaca lebih dari. Contoh: 3.200 < 3.500 dan 7.010 > 7.001."},
           {"q": "Apa bedanya urutan naik dan turun?", "a": "Urutan naik dari terkecil ke terbesar. Urutan turun dari terbesar ke terkecil."}]
    return dict(slug="membandingkan-dan-mengurutkan-bilangan", dom="B", sort=2,
                std_text="Peserta didik membandingkan dan mengurutkan bilangan cacah sampai 10.000.",
                title="Membandingkan dan Mengurutkan Bilangan", short_title="Membandingkan dan Mengurutkan Bilangan",
                meta_desc="Latihan membandingkan bilangan sampai 10.000 dengan tanda <, > dan =, mencari bilangan terbesar dan terkecil, dan mengurutkan bilangan. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Bandingkan dari kiri", key_sub="Ribuan, lalu ratusan, puluhan, dan satuan.",
                body=body, faq=faq, sets=sets)


# ============================================================ 3. menyusun dan menguraikan bilangan
def u3():
    def parts(n):
        s = str(n)
        return [int(d) * 10 ** (3 - i) for i, d in enumerate(s) if d != "0"]

    def panjang():
        n = n4(R.random() < 0.5)
        p = parts(n)
        if len(p) < 3:
            return None
        f = lambda ps: " + ".join(num(x) for x in ps)
        w1 = [x // 10 if x >= 10 and i == 1 else x for i, x in enumerate(p)]
        w2 = [x * 10 if x < 1000 and i == len(p) - 1 else x for i, x in enumerate(p)]
        w3 = [int(str(x)[0]) for x in p]
        return mcq("Bentuk panjang dari %s adalah …" % num(n), f(p), [f(w1), f(w2), f(w3), f(p[::-1])],
                   "Setiap angka ditulis sesuai nilainya: %s = %s." % (num(n), f(p)))

    def kosong():
        n = n4()
        p = parts(n)
        if len(p) < 4:
            return None
        i = ri(0, 3)
        shown = [num(x) if j != i else "…" for j, x in enumerate(p)]
        v = p[i]
        d = int(str(v)[0])
        return mcq("%s = %s. Bilangan yang tepat untuk … adalah …" % (num(n), " + ".join(shown)), num(v),
                   [num(d * 10 ** q) for q in range(4) if d * 10 ** q != v],
                   "Angka %d di tempat itu bernilai %s." % (d, num(v)))

    def susun():
        a, b, c, d = ri(1, 9), ri(0, 9), ri(0, 9), ri(0, 9)
        if [b, c, d].count(0) > 1:
            return None
        n = a * 1000 + b * 100 + c * 10 + d
        return mcq("%d ribuan + %d ratusan + %d puluhan + %d satuan = …" % (a, b, c, d), num(n),
                   [num(a * 1000 + c * 100 + b * 10 + d), num(a * 1000 + b * 100 + d * 10 + c), num(a + b * 10 + c * 100 + d * 1000) if d else num(n + 100)],
                   "%s + %s + %s + %d = %s." % (num(a * 1000), num(b * 100), num(c * 10), d, num(n)))

    def acak():
        a, b, c, d = ri(1, 9), ri(1, 9), ri(1, 9), ri(1, 9)
        p = [a * 1000, b * 100, c * 10, d]
        R.shuffle(p)
        if p[0] == a * 1000:
            return None
        n = a * 1000 + b * 100 + c * 10 + d
        wr = int("".join(str(int(str(x)[0])) for x in p))
        return mcq("%s = …" % " + ".join(num(x) for x in p), num(n), [num(wr), num(n + 90 if c == 0 else n - 10 * c + c), num(n + 1000) if a < 9 else num(n - 1000)],
                   "Susun menurut nilai tempat: %s." % num(n))

    def ratusan():
        h = ri(11, 99)
        r = ri(0, 99)
        n = h * 100 + r
        if R.random() < 0.5:
            return mcq("%s = … ratusan + %d satuan" % (num(n), r), num(h), [num(h // 10), num(h * 10), num(h + 1)],
                       "%s = %s + %d, dan %s = %d ratusan." % (num(n), num(h * 100), r, num(h * 100), h))
        t = ri(11, 999)
        n = t * 10 + ri(0, 9)
        return mcq("%s = … puluhan + %d satuan" % (num(n), n % 10), num(t), [num(t // 10), num(t * 10), num(t + 1)],
                   "%s = %s + %d, dan %s = %s puluhan." % (num(n), num(t * 10), n % 10, num(t * 10), num(t)))

    def uang():
        a, b, c = ri(1, 9), ri(0, 9), ri(0, 9)
        if a + b + c < 4:
            return None
        tot = a * 1000 + b * 500 + c * 100
        return mcq("%s punya %d lembar uang Rp1.000, %d keping uang Rp500, dan %d keping uang Rp100. Berapa jumlah uangnya?" % (K.next(), a, b, c),
                   rp(tot), [rp(a * 1000 + b * 100 + c * 500), rp(a * 1000 + b * 50 + c * 100), rp(a * 100 + b * 500 + c * 1000)],
                   "%s + %s + %s = %s." % (rp(a * 1000), rp(b * 500), rp(c * 100), rp(tot)))

    def urai():
        n = n4()
        th, rest = divmod(n, 1000)
        h = rest // 100
        good = "%s + %s" % (num(th * 1000), num(rest))
        bad = ["%s + %s" % (num(th * 100), num(rest)), "%s + %s" % (num(th * 1000), num(rest + 100)),
               "%s + %s" % (num((th + 1) * 1000), num(rest)) if th < 9 else "%s + %s" % (num(th * 1000), num(rest * 10 % 1000 or 10))]
        alt = "%s + %s" % (num(th * 1000 + h * 100), num(rest - h * 100))
        q = "Manakah yang sama dengan %s?" % num(n)
        if R.random() < 0.5 and rest - h * 100 > 0:
            good = alt
        return mcq(q, good, bad, "Jumlahkan kedua bilangan: hasilnya harus %s." % num(n))

    sets = [("Bentuk panjang", [(panjang, 14), (kosong, 6)]),
            ("Menyusun bilangan", [(susun, 12), (acak, 8)]),
            ("Mengurai dengan cara lain", [(ratusan, 12), (urai, 8)]),
            ("Mengisi bagian yang hilang", [(kosong, 12), (acak, 8)]),
            ("Uang dan soal cerita", [(uang, 14), (urai, 6)])]
    body = lesson(
        ["Menyusun bilangan berarti menggabungkan ribuan, ratusan, puluhan, dan satuan menjadi satu bilangan.",
         "Mengurai berarti memecah bilangan menurut nilai tempatnya. Bentuk ini disebut bentuk panjang.",
         "Satu bilangan bisa diurai dengan beberapa cara. 2.350 = 2.000 + 350 = 23 ratusan + 50."],
        [example("Tulis bentuk panjang 6.083.", ["6 ribuan = 6.000", "0 ratusan", "8 puluhan = 80", "3 satuan = 3"], "6.000 + 80 + 3"),
         example("900 + 4.000 + 7 = …", ["Urutkan: 4.000 + 900 + 7", "Puluhan 0"], "4.907")],
        [["4.000 + 900 + 7 = 4.97", "Tempat puluhan kosong diisi 0: 4.907"],
         ["Bentuk panjang 3.520 ditulis 3 + 5 + 2", "Tulis nilainya: 3.000 + 500 + 20"],
         ["Urutan bilangan yang dijumlahkan diikuti apa adanya", "Lihat nilainya, bukan urutannya"]])
    faq = [{"q": "Apa itu bentuk panjang bilangan?", "a": "Bentuk panjang adalah penjumlahan nilai tiap angka. Contoh: 5.264 = 5.000 + 200 + 60 + 4."},
           {"q": "Apakah bilangan bisa diurai dengan cara lain?", "a": "Bisa. Contoh: 3.400 = 3.000 + 400, atau 34 ratusan, atau 2.000 + 1.400."},
           {"q": "Bagaimana jika ada angka 0?", "a": "Angka 0 tidak ditulis dalam bentuk panjang, tetapi tetap harus ditulis saat menyusun bilangan agar tempatnya benar."}]
    return dict(slug="menyusun-dan-menguraikan-bilangan", dom="B", sort=3,
                std_text="Peserta didik melakukan komposisi (menyusun) dan dekomposisi (mengurai) bilangan cacah sampai 10.000.",
                title="Menyusun dan Mengurai Bilangan", short_title="Menyusun dan Mengurai Bilangan",
                meta_desc="Latihan bentuk panjang, menyusun dan mengurai bilangan sampai 10.000, dan menghitung uang. 100 soal dengan kunci jawaban dan lembar kerja siap cetak untuk kelas 4 SD.",
                key_big="4.536 = 4.000 + 500 + 30 + 6", key_sub="Setiap angka punya nilai menurut tempatnya.",
                body=body, faq=faq, sets=sets)


# ============================================================ 4. penjumlahan dan pengurangan
def nocarry_add(a, b):
    s, m = 0, 1
    while a or b:
        s += ((a % 10 + b % 10) % 10) * m
        a //= 10
        b //= 10
        m *= 10
    return s


def small_from_big(a, b):
    s, m = 0, 1
    while a or b:
        s += abs(a % 10 - b % 10) * m
        a //= 10
        b //= 10
        m *= 10
    return s


def carries(a, b):
    return any((a // 10 ** i) % 10 + (b // 10 ** i) % 10 >= 10 for i in range(3))


def borrows(a, b):
    return any((a // 10 ** i) % 10 < (b // 10 ** i) % 10 for i in range(3))


def u4():
    def tambah(carry, pic=False):
        def mk():
            a, b = ri(100, 899), ri(100, 899)
            if a + b > 1000 or carries(a, b) != carry:
                return None
            s = a + b
            w = [nocarry_add(a, b), s + 10, s - 10, s + 100]
            q = ("%s + %s = …" % (num(a), num(b))) if not pic else ("Hasil penjumlahan bersusun ini adalah …" + bersusun([str(a), str(b)], "+"))
            return mcq(q, num(s), [num(x) for x in w if 0 < x != s],
                       ("Jumlahkan satuan, puluhan, lalu ratusan. Jika hasilnya 10 atau lebih, simpan 1 ke tempat di kirinya. " if carry else
                        "Jumlahkan satuan, puluhan, lalu ratusan. ") + "%s + %s = %s." % (num(a), num(b), num(s)))
        return mk

    def kurang(borrow, pic=False):
        def mk():
            a, b = ri(200, 1000), ri(100, 899)
            if b >= a or borrows(a, b) != borrow:
                return None
            d = a - b
            w = [small_from_big(a, b), d + 10, d - 10, d + 100]
            q = ("%s − %s = …" % (num(a), num(b))) if not pic else ("Hasil pengurangan bersusun ini adalah …" + bersusun([str(a), str(b)], "−"))
            return mcq(q, num(d), [num(x) for x in w if 0 < x != d],
                       ("Jika angka atas lebih kecil, pinjam 1 dari tempat di kirinya. " if borrow else "Kurangkan satuan, puluhan, lalu ratusan. ")
                       + "%s − %s = %s." % (num(a), num(b), num(d)))
        return mk

    def mental():
        if R.random() < 0.5:
            a, b = ri(1, 8) * 100 + ch([0, 50]), ri(1, 4) * 100 + ch([0, 50])
            if a + b > 1000:
                return None
            return mcq("Hitung dalam hati: %s + %s = …" % (num(a), num(b)), num(a + b), [num(a + b + 100), num(a + b - 100), num(a + b + 50)],
                       "Jumlahkan ratusan dan puluhannya: %s." % num(a + b))
        a, b = ri(5, 10) * 100, ri(1, 4) * 100 + ch([0, 50])
        return mcq("Hitung dalam hati: %s − %s = …" % (num(a), num(b)), num(a - b), [num(a - b + 100), num(a - b - 100), num(a + b)],
                   "%s − %s = %s." % (num(a), num(b), num(a - b)))

    ADD = [("Di sekolah ada %s siswa laki-laki dan %s siswa perempuan. Berapa jumlah semua siswa?", "siswa"),
           ("Pak Slamet memanen %s buah mangga hari ini dan %s buah kemarin. Berapa jumlah mangga yang dipanen?", "buah"),
           ("Perpustakaan punya %s buku cerita. Sekolah membeli lagi %s buku. Berapa banyak buku cerita sekarang?", "buku"),
           ("Pada hari Sabtu ada %s pengunjung pantai dan hari Minggu %s pengunjung. Berapa jumlah pengunjung?", "orang"),
           ("Bu Dewi membuat %s kue lapis dan %s kue lumpur. Berapa banyak kue yang dibuat?", "kue"),
           ("Sebuah kereta membawa %s penumpang. Di stasiun naik lagi %s penumpang. Berapa penumpang sekarang?", "orang")]
    SUB = [("Toko punya %s butir telur. Sebanyak %s butir terjual. Berapa butir telur yang tersisa?", "butir"),
           ("Gedung pertunjukan punya %s kursi. Sebanyak %s kursi sudah terisi. Berapa kursi yang masih kosong?", "kursi"),
           ("Panjang jalan desa %s meter. Sebanyak %s meter sudah diaspal. Berapa meter yang belum diaspal?", "meter"),
           ("Andi mengumpulkan %s tutup botol, Candra %s tutup botol. Berapa selisih tutup botol mereka?", "tutup botol"),
           ("Ada %s bibit pohon. Sebanyak %s bibit sudah ditanam. Berapa bibit yang belum ditanam?", "bibit"),
           ("Sekolah memesan %s buku tulis. Yang sudah dibagikan %s buku. Berapa buku yang belum dibagikan?", "buku")]

    def cerita():
        if R.random() < 0.5:
            t, unit = ch(ADD)
            a, b = ri(120, 600), ri(110, 390)
            if a + b > 1000:
                return None
            return mcq(t % (num(a), num(b)), u(a + b, unit), [u(nocarry_add(a, b), unit) if carries(a, b) else u(a + b + 10, unit), u(abs(a - b), unit), u(a + b - 10, unit)],
                       "Gabungkan, jadi dijumlah: %s + %s = %s." % (num(a), num(b), num(a + b)))
        t, unit = ch(SUB)
        a, b = ri(300, 1000), ri(110, 290)
        return mcq(t % (num(a), num(b)), u(a - b, unit), [u(a + b, unit), u(small_from_big(a, b), unit) if borrows(a, b) else u(a - b + 10, unit), u(a - b - 10, unit)],
                   "Yang tersisa atau selisih dicari dengan pengurangan: %s − %s = %s." % (num(a), num(b), num(a - b)))

    def taksir():
        a, b = ri(1, 6) * 100 + ch([ri(1, 9), 100 - ri(1, 9)]), ri(1, 3) * 100 + ch([ri(1, 9), 100 - ri(1, 9)])
        ra, rb = int(round(a / 100.0)) * 100, int(round(b / 100.0)) * 100
        if ra + rb > 1000:
            return None
        g = ra + rb
        return mcq("Hasil %s + %s paling dekat dengan …" % (num(a), num(b)), num(g), [num(g + 100), num(g - 100), num(g + 200)],
                   "%s ≈ %s dan %s ≈ %s, jadi hasilnya sekitar %s." % (num(a), num(ra), num(b), num(rb), num(g)))

    sets = [("Penjumlahan tanpa menyimpan", [(tambah(False), 12), (mental, 8)]),
            ("Penjumlahan dengan menyimpan", [(tambah(True), 14), (tambah(True, True), 6)]),
            ("Pengurangan", [(kurang(False), 8), (kurang(True), 12)]),
            ("Bersusun dan menaksir", [(tambah(True, True), 6), (kurang(True, True), 8), (taksir, 6)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Tulis bilangan bersusun: satuan di bawah satuan, puluhan di bawah puluhan, ratusan di bawah ratusan.",
         "Penjumlahan dimulai dari satuan. Jika hasilnya 10 atau lebih, tulis satuannya dan simpan 1 ke tempat berikutnya.",
         "Pada pengurangan, jika angka atas lebih kecil, pinjam 1 dari tempat di kirinya. 1 puluhan = 10 satuan."],
        [example("456 + 278 = …", ["Satuan: 6 + 8 = 14, tulis 4 simpan 1", "Puluhan: 5 + 7 + 1 = 13, tulis 3 simpan 1", "Ratusan: 4 + 2 + 1 = 7"], "734"),
         example("702 − 345 = …", ["Satuan: 2 &lt; 5, pinjam dari puluhan (0), jadi pinjam dari ratusan dulu", "12 − 5 = 7, 9 − 4 = 5, 6 − 3 = 3"], "357")],
        [["Lupa menambahkan angka yang disimpan", "Tulis angka 1 kecil di atas, lalu ikut dijumlahkan"],
         ["Pada pengurangan, angka kecil dikurangi angka besar (2 − 5 menjadi 3)", "Pinjam 1 dari kiri: 12 − 5 = 7"],
         ["Angka tidak lurus sesuai tempatnya", "Satuan harus tepat di bawah satuan"]])
    faq = [{"q": "Apa itu menyimpan dalam penjumlahan?", "a": "Jika jumlah dalam satu tempat 10 atau lebih, angka puluhannya disimpan (dibawa) ke tempat di sebelah kiri. Contoh: 8 + 5 = 13, tulis 3 dan simpan 1."},
           {"q": "Apa itu meminjam dalam pengurangan?", "a": "Jika angka atas lebih kecil dari angka bawah, ambil 1 dari tempat di sebelah kiri. 1 puluhan menjadi 10 satuan."},
           {"q": "Bagaimana memeriksa hasil pengurangan?", "a": "Jumlahkan hasilnya dengan bilangan pengurang. Hasilnya harus sama dengan bilangan yang dikurangi."}]
    return dict(slug="penjumlahan-dan-pengurangan", dom="B", sort=4,
                std_text="Peserta didik melakukan operasi penjumlahan dan pengurangan bilangan cacah sampai 1.000.",
                title="Penjumlahan dan Pengurangan sampai 1.000", short_title="Penjumlahan dan Pengurangan",
                meta_desc="Latihan penjumlahan dan pengurangan bersusun sampai 1.000 dengan menyimpan dan meminjam, berhitung dalam hati, menaksir, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Mulai dari satuan", key_sub="Simpan 1 saat menjumlah, pinjam 1 saat mengurang.",
                body=body, faq=faq, sets=sets)


# ============================================================ 5. perkalian dan pembagian
def u5():
    def fact_w(a, b):
        p = a * b
        return [p + a, p - a, p + b, p - b, a + b, int(str(p)[::-1]) if p >= 10 else p + 1]

    def gambar():
        r, c = ri(2, 6), ri(2, 9)
        if R.random() < 0.5:
            good = "%d × %d = %d" % (r, c, r * c)
            bad = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, r, r * r), "%d × %d = %d" % (c, c, c * c), "%d × %d = %d" % (r, c + 1, r * (c + 1))]
            return mcq("Kalimat perkalian yang sesuai dengan gambar adalah …" + titik(r, c), good, bad,
                       "Ada %d baris, setiap baris %d titik: %d × %d = %d." % (r, c, r, c, r * c))
        return mcq("Ada %d kelompok. Berapa banyak benda semuanya?" % r + kelompok(r, c), str(r * c), [str(x) for x in fact_w(r, c)],
                   "%d kelompok masing-masing %d: %d × %d = %d." % (r, c, r, c, r * c))

    def berulang():
        a, b = ri(2, 9), ri(3, 9)
        rep = " + ".join([str(b)] * a)
        return mcq("%s = … × %d" % (rep, b), str(a), [str(b), str(a + 1), str(a * b)],
                   "Bilangan %d dijumlahkan %d kali, jadi %d × %d." % (b, a, a, b))

    def kali():
        a, b = ri(2, 10), ri(2, 10)
        return mcq("%d × %d = …" % (a, b), str(a * b), [str(x) for x in fact_w(a, b)], "%d × %d = %d." % (a, b, a * b))

    def bagi():
        a, b = ri(2, 10), ri(2, 10)
        p = a * b
        return mcq("%d : %d = …" % (p, b), str(a), [str(a + 1), str(a - 1), str(p - b), str(b)] if a != b else [str(a + 1), str(a - 1), str(p - b), str(a + 2)],
                   "Cari bilangan yang jika dikali %d hasilnya %d: %d × %d = %d." % (b, p, a, b, p))

    def hubungan():
        a, b = ri(3, 10), ri(3, 10)
        if a == b:
            return None
        p = a * b
        return mcq("Jika %d × %d = %d, maka %d : %d = …" % (a, b, p, p, b), str(a), [str(b), str(p), str(p - b), str(a + b)],
                   "Pembagian adalah kebalikan perkalian: %d : %d = %d." % (p, b, a))

    def kosong():
        a, b = ri(2, 10), ri(2, 10)
        p = a * b
        return mcq("%d × … = %d" % (a, p), str(b), [str(p - a), str(b + 1), str(b - 1), str(p + a)],
                   "%d × %d = %d." % (a, b, p))

    def sisa():
        b = ri(3, 9)
        q = ri(2, 9)
        r = ri(1, b - 1)
        n = q * b + r
        if n > 100:
            return None
        return mcq("%d : %d = %d sisa …" % (n, b, q), str(r), [str(r + 1), str(b - r) if b - r != r else str(r + 2), str(n - q)],
                   "%d × %d = %d, dan %d − %d = %d. Sisanya %d." % (q, b, q * b, n, q * b, r, r))

    KALI = ["Ada %d kotak. Setiap kotak berisi %d kue. Berapa banyak kue seluruhnya?",
            "Sebuah kelas punya %d baris meja. Setiap baris ada %d meja. Berapa banyak meja seluruhnya?",
            "Putu membeli %d ikat rambutan. Setiap ikat berisi %d buah. Berapa buah rambutan yang dibeli Putu?",
            "Ada %d mobil di parkiran. Setiap mobil punya %d roda. Berapa banyak roda seluruhnya?",
            "Bu guru membagikan %d bungkus pensil. Setiap bungkus berisi %d pensil. Berapa pensil seluruhnya?"]
    BAGI = ["Ada %d kelereng dibagikan sama banyak kepada %d anak. Berapa kelereng yang didapat setiap anak?",
            "Sebanyak %d siswa dibagi menjadi %d kelompok sama besar. Berapa siswa dalam setiap kelompok?",
            "Bu Wiwin punya %d telur. Setiap wadah diisi %d telur. Berapa wadah yang diperlukan?",
            "Sebanyak %d buku disusun sama banyak di %d rak. Berapa buku di setiap rak?",
            "Ada %d jeruk dimasukkan ke kantong, setiap kantong %d jeruk. Berapa kantong yang terisi?"]

    def cerita():
        a, b = ri(3, 10), ri(3, 10)
        if R.random() < 0.5:
            t = ch(KALI)
            if "roda" in t:
                b = 4
            return mcq(t % (a, b), str(a * b), [str(a + b), str(a * b + a), str(a * b - b)], "%d × %d = %d." % (a, b, a * b))
        t = ch(BAGI)
        return mcq(t % (a * b, b), str(a), [str(a * b - b), str(a + 1), str(b * 2)], "%d : %d = %d." % (a * b, b, a))

    sets = [("Gambar dan penjumlahan berulang", [(gambar, 12), (berulang, 8)]),
            ("Perkalian sampai 100", [(kali, 14), (kosong, 6)]),
            ("Pembagian sampai 100", [(bagi, 12), (hubungan, 8)]),
            ("Pembagian bersisa", [(sisa, 12), (bagi, 4), (kosong, 4)]),
            ("Soal cerita", [(cerita, 20)])]
    body = lesson(
        ["Perkalian adalah penjumlahan berulang. 4 × 3 berarti 3 + 3 + 3 + 3 = 12.",
         "Pembagian berarti membagi sama banyak atau membuat kelompok sama besar. 12 : 3 = 4 karena 4 × 3 = 12.",
         "Jika tidak bisa dibagi habis, ada sisa. Sisa selalu lebih kecil dari pembagi."],
        [example("6 × 7 = …", ["7 + 7 + 7 + 7 + 7 + 7", "atau 5 × 7 = 35, lalu 35 + 7"], "42"),
         example("29 : 4 = …", ["4 × 7 = 28, 4 × 8 = 32 (terlalu besar)", "29 − 28 = 1"], "7 sisa 1")],
        [["4 × 3 dihitung 4 + 3 = 7", "4 × 3 = 3 + 3 + 3 + 3 = 12"],
         ["Sisa lebih besar dari pembagi (29 : 4 = 6 sisa 5)", "Sisa harus lebih kecil dari 4: 7 sisa 1"],
         ["Membagi 35 : 5 dengan mengurangi 35 − 5", "Cari bilangan yang dikali 5 menjadi 35: 7"]])
    faq = [{"q": "Apa hubungan perkalian dan pembagian?", "a": "Pembagian adalah kebalikan dari perkalian. Jika 6 × 8 = 48, maka 48 : 8 = 6 dan 48 : 6 = 8."},
           {"q": "Bagaimana cara cepat menghafal perkalian?", "a": "Gunakan perkalian yang sudah dikenal. Contoh: 9 × 7 = 10 × 7 − 7 = 70 − 7 = 63."},
           {"q": "Apa itu sisa pembagian?", "a": "Sisa adalah bagian yang tidak bisa dibagi rata. Contoh: 17 : 5 = 3 sisa 2 karena 3 × 5 = 15 dan 17 − 15 = 2."}]
    return dict(slug="perkalian-dan-pembagian", dom="B", sort=5,
                std_text="Peserta didik melakukan operasi perkalian dan pembagian bilangan cacah sampai 100 menggunakan benda konkret, gambar, dan simbol matematika.",
                title="Perkalian dan Pembagian sampai 100", short_title="Perkalian dan Pembagian",
                meta_desc="Latihan perkalian dan pembagian sampai 100 dengan gambar, penjumlahan berulang, pembagian bersisa, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Perkalian = penjumlahan berulang", key_sub="12 : 3 = 4 karena 4 × 3 = 12.",
                body=body, faq=faq, sets=sets)


# ============================================================ 6. faktor dan kelipatan
def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def u6():
    NS = [n for n in range(6, 61) if len(factors(n)) >= 4]

    def daftar():
        n = ch(NS)
        fs = factors(n)
        f = lambda xs: ", ".join(map(str, xs))
        w1 = fs[1:]
        w2 = [x for x in fs if x not in (fs[len(fs) // 2],)]
        w3 = sorted(set(fs[:-1] + [n + fs[1]]))
        w4 = [n * k for k in range(1, 5)]
        return mcq("Semua faktor dari %d adalah …" % n, f(fs), [f(w2), f(w1), f(w3), f(w4)],
                   "Cari pasangan yang hasil kalinya %d: %s." % (n, ", ".join("%d × %d" % (a, n // a) for a in fs if a * a <= n)))

    def adalah():
        n = ch(NS)
        fs = factors(n)
        g = ch(fs[1:-1])
        bad = [x for x in range(2, n) if n % x]
        if len(bad) < 3:
            return None
        R.shuffle(bad)
        return mcq("Bilangan berikut yang merupakan faktor dari %d adalah …" % n, str(g), [str(b) for b in bad],
                   "%d : %d = %d tanpa sisa, jadi %d faktor dari %d." % (n, g, n // g, g, n))

    def bukan():
        n = ch(NS)
        fs = factors(n)
        bad = [x for x in range(2, n) if n % x]
        if len(fs) < 5 or not bad:
            return None
        g = ch(bad)
        return mcq("Bilangan berikut yang <b>bukan</b> faktor dari %d adalah …" % n, str(g), [str(x) for x in pool(fs[1:-1])],
                   "%d : %d tidak habis (ada sisa), jadi %d bukan faktor dari %d." % (n, g, g, n))

    def kelipatan():
        a = ri(2, 12)
        lim = a * ri(4, 7) + ri(1, a - 1) if a > 2 else a * ri(5, 9) + 1
        ks = list(range(a, lim, a))
        f = lambda xs: ", ".join(map(str, xs))
        return mcq("Kelipatan %d yang kurang dari %d adalah …" % (a, lim), f(ks),
                   [f(ks[:-1]), f([0] + ks if False else [x + 1 for x in ks]), f(factors(a * len(ks))[:len(ks)]) if len(factors(a * len(ks))) >= len(ks) else f(ks + [ks[-1] + a])],
                   "Kelipatan %d adalah %d, %d, %d, … (tambah %d terus)." % (a, a, 2 * a, 3 * a, a))

    def ke():
        a, k = ri(2, 12), ri(3, 9)
        if a * k > 100:
            return None
        return mcq("Kelipatan ke-%d dari %d adalah …" % (k, a), str(a * k), [str(a * (k - 1)), str(a * (k + 1)), str(a + k)],
                   "Kelipatan ke-%d dari %d = %d × %d = %d." % (k, a, k, a, a * k))

    def kelipatan_dari():
        n = ch([x for x in NS if x <= 60])
        g = ch(factors(n)[1:-1])
        bad = [x for x in range(2, 13) if n % x]
        R.shuffle(bad)
        return mcq("%d adalah kelipatan dari …" % n, str(g), [str(b) for b in bad],
                   "%d = %d × %d, jadi %d kelipatan dari %d." % (n, g, n // g, n, g))

    def cek():
        a = ri(3, 12)
        lim = ri(4, 9) * 10
        g = a * ri(2, (lim - 1) // a)
        bad = set()
        while len(bad) < 3:
            x = ri(10, lim - 1)
            if x % a:
                bad.add(x)
        return mcq("Bilangan berikut yang merupakan kelipatan %d dan kurang dari %d adalah …" % (a, lim), str(g), [str(b) for b in sorted(bad)],
                   "%d = %d × %d, jadi %d kelipatan %d." % (g, a, g // a, g, a))

    def susun():
        n = ch([12, 18, 20, 24, 30, 36, 40, 42, 48])
        fs = factors(n)
        thing = ch([("kursi", "baris"), ("pot bunga", "baris"), ("siswa", "kelompok"), ("kue", "piring")])
        g = ch(fs[1:-1])
        bad = [x for x in range(2, 13) if n % x]
        R.shuffle(bad)
        return mcq("Ada %d %s. Semua %s dibagi sama banyak ke beberapa %s tanpa sisa. Banyak %s setiap %s yang mungkin adalah …"
                   % (n, thing[0], thing[0], thing[1], thing[0], thing[1]), str(g), [str(b) for b in bad],
                   "Banyaknya harus faktor dari %d. %d : %d = %d." % (n, n, g, n // g))

    def jadwal():
        a = ch([2, 3, 4, 5, 6, 7])
        k = ri(3, 8)
        who = K.next()
        what = ch(["menyiram tanaman", "berenang", "membersihkan akuarium", "mengunjungi nenek", "bermain bulu tangkis"])
        return mcq("%s %s setiap %d hari sekali, mulai tanggal %d. Tanggal berapa %s %s untuk ke-%d kalinya?" % (who, what, a, a, who, what, k),
                   "tanggal %d" % (a * k), ["tanggal %d" % (a * k + 1), "tanggal %d" % (a * (k - 1)), "tanggal %d" % (a + k)],
                   "Tanggalnya adalah kelipatan %d: %s. Yang ke-%d adalah %d."
                   % (a, ", ".join(str(a * i) for i in range(1, 4)) + ", …", k, a * k))

    sets = [("Faktor sebuah bilangan", [(daftar, 12), (adalah, 8)]),
            ("Faktor atau bukan", [(adalah, 8), (bukan, 12)]),
            ("Kelipatan", [(kelipatan, 10), (ke, 10)]),
            ("Faktor dan kelipatan", [(kelipatan_dari, 8), (cek, 8), (daftar, 4)]),
            ("Soal cerita", [(susun, 10), (jadwal, 10)])]
    body = lesson(
        ["Faktor dari sebuah bilangan adalah bilangan yang dapat membaginya habis. Faktor dari 12: 1, 2, 3, 4, 6, 12.",
         "Cari faktor dengan pasangan perkalian: 1 × 12, 2 × 6, 3 × 4.",
         "Kelipatan sebuah bilangan didapat dengan menambahkan bilangan itu terus-menerus. Kelipatan 4: 4, 8, 12, 16, …"],
        [example("Tentukan faktor dari 18.", ["1 × 18", "2 × 9", "3 × 6"], "1, 2, 3, 6, 9, 18"),
         example("Tentukan kelipatan ke-6 dari 7.", ["6 × 7"], "42")],
        [["Lupa menulis 1 dan bilangan itu sendiri sebagai faktor", "Setiap bilangan punya faktor 1 dan dirinya sendiri"],
         ["Tertukar: menulis kelipatan saat diminta faktor", "Faktor ≤ bilangannya, kelipatan ≥ bilangannya"],
         ["Kelipatan 5 dimulai dari 0 atau 1", "Kelipatan 5 dimulai dari 5: 5, 10, 15, …"]])
    faq = [{"q": "Apa bedanya faktor dan kelipatan?", "a": "Faktor membagi habis sebuah bilangan, jadi faktor tidak lebih besar dari bilangan itu. Kelipatan didapat dari mengalikan, jadi kelipatan tidak lebih kecil dari bilangan itu."},
           {"q": "Bagaimana cara mencari semua faktor?", "a": "Cari pasangan perkalian mulai dari 1. Contoh untuk 24: 1 × 24, 2 × 12, 3 × 8, 4 × 6. Faktornya 1, 2, 3, 4, 6, 8, 12, 24."},
           {"q": "Apakah 0 kelipatan sebuah bilangan?", "a": "Di kelas 4 kita mulai menulis kelipatan dari bilangan itu sendiri, misalnya kelipatan 3 adalah 3, 6, 9, 12, …"}]
    return dict(slug="faktor-dan-kelipatan", dom="B", sort=6,
                std_text="Peserta didik dapat menyelesaikan masalah yang berkaitan dengan kelipatan dan faktor.",
                title="Faktor dan Kelipatan", short_title="Faktor dan Kelipatan",
                meta_desc="Latihan mencari faktor dan kelipatan sebuah bilangan, menentukan faktor atau bukan, kelipatan ke-n, dan soal cerita. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Faktor membagi habis", key_sub="Kelipatan: tambahkan bilangan itu terus.",
                body=body, faq=faq, sets=sets)


# ============================================================ 7. soal cerita (uang)
ITEMS = [("buku tulis", 4500, "buah"), ("pensil", 2500, "batang"), ("penghapus", 1500, "buah"), ("roti", 5000, "bungkus"),
         ("susu kotak", 4000, "kotak"), ("es teh", 3000, "gelas"), ("pisang goreng", 2000, "potong"), ("kerupuk", 1000, "bungkus"),
         ("salak", 8000, "kilogram"), ("penggaris", 3500, "buah"), ("bakso", 12000, "mangkuk"), ("kue cucur", 1500, "buah"),
         ("air mineral", 3000, "botol"), ("pulpen", 3000, "batang"), ("nasi uduk", 8000, "bungkus"), ("jeruk", 15000, "kilogram")]


def u7():
    def beli2():
        (a, pa, ua), (b, pb, ub) = R.sample(ITEMS, 2)
        if pa == pb:
            return None
        who = K.next()
        t = pa + pb
        return mcq("%s membeli 1 %s %s seharga %s dan 1 %s %s seharga %s. Berapa yang harus dibayar %s?" % (who, ua, a, rp(pa), ub, b, rp(pb), who),
                   rp(t), [rp(abs(pa - pb)), rp(t + 1000), rp(t - 500)], "%s + %s = %s." % (rp(pa), rp(pb), rp(t)))

    def tabung():
        who = K.next()
        a, b = ri(5, 40) * 500, ri(4, 30) * 500
        if a == b:
            return None
        return mcq("Uang tabungan %s %s. Ibu memberinya lagi %s. Berapa uang %s sekarang?" % (who, rp(a), rp(b), who),
                   rp(a + b), [rp(abs(a - b)), rp(a + b + 500), rp(a + b - 1000)], "%s + %s = %s." % (rp(a), rp(b), rp(a + b)))

    def kembali():
        it, p, un = ch(ITEMS)
        k = ri(1, 4)
        cost = p * k
        pay = ch([x for x in (5000, 10000, 20000, 50000) if x > cost])
        who = K.next()
        return mcq("%s membeli %d %s %s seharga %s per %s. %s membayar dengan uang %s. Berapa uang kembaliannya?" % (who, k, un, it, rp(p), un, who, rp(pay)),
                   rp(pay - cost), [rp(pay - p), rp(pay + cost), rp(pay - cost + 1000)],
                   "Harga %d %s = %s. Kembalian = %s − %s = %s." % (k, un, rp(cost), rp(pay), rp(cost), rp(pay - cost)))

    def sisa_uang():
        who = K.next()
        a = ri(10, 40) * 1000
        b = ri(2, a // 1000 - 1) * 1000 - ch([0, 500])
        what = ch(["buku cerita", "tas", "bola", "kaus kaki", "topi", "payung"])
        return mcq("%s punya uang %s. %s membeli %s seharga %s. Berapa sisa uang %s?" % (who, rp(a), who, what, rp(b), who),
                   rp(a - b), [rp(a + b), rp(a - b - 1000), rp(a - b + 500)], "%s − %s = %s." % (rp(a), rp(b), rp(a - b)))

    def kali():
        it, p, un = ch(ITEMS)
        k = ri(2, 9)
        who = K.next()
        return mcq("Harga 1 %s %s adalah %s. %s membeli %d %s. Berapa yang harus dibayar?" % (un, it, rp(p), who, k, un),
                   rp(p * k), [rp(p + k * 1000), rp(p * (k - 1)), rp(p * (k + 1))], "%d × %s = %s." % (k, rp(p), rp(p * k)))

    def bagi():
        it, p, un = ch([x for x in ITEMS if x[1] % 1000 == 0])
        k = ri(2, 9)
        return mcq("Harga %d %s %s adalah %s. Berapa harga 1 %s?" % (k, un, it, rp(p * k), un),
                   rp(p), [rp(p * k - p), rp(p + 1000), rp(p * 2)], "%s : %d = %s." % (rp(p * k), k, rp(p)))

    def patungan():
        n = ri(2, 6)
        each = ri(2, 15) * 1000
        what = ch(["kue ulang tahun", "bola voli", "hadiah untuk guru", "buah untuk teman yang sakit", "tanaman hias untuk kelas"])
        return mcq("%d anak membeli %s seharga %s. Mereka membayar sama banyak. Berapa yang dibayar setiap anak?" % (n, what, rp(n * each)),
                   rp(each), [rp(n * each - n * 1000), rp(each + 1000), rp(each * 2)], "%s : %d = %s." % (rp(n * each), n, rp(each)))

    def dua():
        (a, pa, ua), (b, pb, ub) = R.sample(ITEMS, 2)
        ka, kb = ri(2, 4), ri(1, 3)
        tot = pa * ka + pb * kb
        pay = ch([x for x in (20000, 50000, 100000) if x > tot])
        who = K.next()
        if R.random() < 0.5:
            return mcq("%s membeli %d %s %s (%s per %s) dan %d %s %s (%s per %s). Berapa jumlah harganya?"
                       % (who, ka, ua, a, rp(pa), ua, kb, ub, b, rp(pb), ub), rp(tot), [rp(pa + pb), rp(pa * ka + pb), rp(tot + pb)],
                       "%d × %s = %s dan %d × %s = %s. Jumlah = %s." % (ka, rp(pa), rp(pa * ka), kb, rp(pb), rp(pb * kb), rp(tot)))
        return mcq("%s membeli %d %s %s (%s per %s) dan %d %s %s (%s per %s). %s membayar dengan %s. Berapa kembaliannya?"
                   % (who, ka, ua, a, rp(pa), ua, kb, ub, b, rp(pb), ub, who, rp(pay)), rp(pay - tot), [rp(tot), rp(pay - pa - pb), rp(pay - tot - 1000)],
                   "Harga semua = %s. Kembalian = %s − %s = %s." % (rp(tot), rp(pay), rp(tot), rp(pay - tot)))

    sets = [("Menjumlah uang", [(beli2, 12), (tabung, 8)]),
            ("Sisa dan kembalian", [(kembali, 10), (sisa_uang, 10)]),
            ("Membeli beberapa barang", [(kali, 20)]),
            ("Membagi uang", [(bagi, 10), (patungan, 10)]),
            ("Soal dua langkah", [(dua, 20)])]
    body = lesson(
        ["Baca soal dengan teliti. Tentukan apa yang diketahui dan apa yang ditanyakan.",
         "Pilih operasinya: digabung → tambah, sisa atau kembalian → kurang, beberapa yang sama → kali, dibagi rata → bagi.",
         "Untuk uang ribuan, kamu bisa menghitung dalam ribuan: Rp4.000 + Rp3.500 = 4 ribu + 3 ribu 5 ratus = Rp7.500."],
        [example("Harga 1 pensil Rp2.500. Andi membeli 4 pensil dan membayar Rp20.000. Berapa kembaliannya?",
                 ["Harga 4 pensil = 4 × Rp2.500 = Rp10.000", "Kembalian = Rp20.000 − Rp10.000"], "Rp10.000"),
         example("3 anak membeli bola seharga Rp45.000 dan membayar sama banyak.", ["Rp45.000 : 3"], "Rp15.000 per anak")],
        [["Kembalian dihitung dengan menambah", "Kembalian = uang yang dibayar − harga"],
         ["Lupa mengalikan banyak barang", "Harga 4 pensil = 4 × harga 1 pensil"],
         ["Pada soal dua langkah, berhenti di langkah pertama", "Periksa lagi apa yang ditanyakan"]])
    faq = [{"q": "Bagaimana menentukan operasi pada soal cerita?", "a": "Perhatikan kata kuncinya: jumlah atau semua (tambah), sisa, selisih, kembalian (kurang), setiap ... sebanyak (kali), dibagi rata atau masing-masing (bagi)."},
           {"q": "Apa itu soal dua langkah?", "a": "Soal yang perlu dua perhitungan. Contoh: hitung harga semua barang dulu, lalu hitung kembaliannya."},
           {"q": "Bagaimana menghitung uang dengan mudah?", "a": "Hitung dalam ribuan. Rp12.000 adalah 12 ribu, jadi 3 × Rp12.000 = 36 ribu = Rp36.000."}]
    return dict(slug="soal-cerita", dom="B", sort=7,
                std_text="Peserta didik menyelesaikan masalah yang berkaitan dengan uang menggunakan ribuan sebagai satuan, dengan penjumlahan, pengurangan, perkalian, dan pembagian.",
                title="Soal Cerita Uang dan Operasi Hitung", short_title="Soal Cerita",
                meta_desc="Latihan soal cerita dengan uang rupiah: menjumlah harga, menghitung kembalian, membeli beberapa barang, membagi uang, dan soal dua langkah. 100 soal dengan kunci jawaban untuk kelas 4 SD.",
                key_big="Diketahui, ditanya, dijawab", key_sub="Pilih operasi yang tepat dari kata kunci soal.",
                body=body, faq=faq, sets=sets)
