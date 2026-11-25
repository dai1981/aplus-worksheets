# -*- coding: utf-8 -*-
"""
Indonesia / Matematika / TK (Taman Kanak-kanak, TK B, 5–6 tahun, Fase Fondasi, Kurikulum Merdeka CP 2025)。
10 まで（数えるのは 20 まで）。とても短い文、ほぼ全問に絵。
python3 tools/id_tk.py [番号…]   seed は 40000 + sort。
問題関数の多くは id_k12（Kelas 1・2）を範囲を絞って再利用。分類・分配・時間・容量は自前。
"""
import random
import sys
import k_pics as P
from f_common import sky_svg, days_svg, glasses_svg
import id_k4a as A
import id_k12 as K
from id_k12 import (ri, ch, pool, named, b, pic, baris, nm, cap, KINDS, WARNA, SHAPE,
                    m_hitung, m_kata, m_sesudah, m_urut, m_ekstrem, m_urutkan, m_tambah_gambar, m_coret,
                    m_lompat, m_kotak, m_ikatan, m_cerita, m_nama_datar, m_cari_datar, m_hitung_datar, m_datar_nyata,
                    m_ruang, m_ruang_nyata, m_gelinding, m_meja, m_kardus, m_rak, m_kanan_kiri, m_panjang, m_tinggi,
                    m_berat, m_seimbang, m_pola, m_pola_bil, m_data, dadu, near)
from id_common import mcq, mix, lesson, example, make_unit


def R():
    return A.R


BASIC = ("circle", "triangle", "square", "rectangle")


# ------------------------------------------------------------ 自前の問題関数
def m_dadu():
    def f():
        v = [ri(1, 6)] + ([ri(1, 4)] if R().random() < 0.4 else [])
        if sum(v) > 10:
            return None
        return mcq("Berapa banyak titik pada dadu?" + dadu(v), str(sum(v)), near(sum(v), 1, 12, (1, -1, 2)), "Hitung titiknya: %d." % sum(v))
    return named(f, "dadu")


def m_banyak_sedikit(hi, few_=None):
    def f():
        a, c = ri(1, hi), ri(1, hi)
        k1, k2 = pool(KINDS)[:2]
        if a == c and R().random() < 0.7:
            return None
        few = (R().random() < 0.5) if few_ is None else few_
        if a == c:
            g = "Sama banyak"
        elif few:
            g = "%s lebih sedikit" % cap(b(k1 if a < c else k2))
        else:
            g = "%s lebih banyak" % cap(b(k1 if a > c else k2))
        w = "sedikit" if few else "banyak"
        opts = ["%s lebih %s" % (cap(b(k1)), w), "%s lebih %s" % (cap(b(k2)), w), "Sama banyak", "Tidak bisa dihitung"]
        return mcq("Mana yang lebih %s?%s%s" % (w, baris(a, k1), baris(c, k2)), g, [o for o in opts if o != g],
                   "Ada %d %s dan %d %s." % (a, b(k1), c, b(k2)))
    return named(f, "banyak_sedikit")


def m_besar():
    def f():
        a, c = pool(range(1, 11))[:2]
        big = R().random() < 0.5
        g = max(a, c) if big else min(a, c)
        return mcq("Bilangan mana yang lebih %s, %d atau %d?" % ("besar" if big else "kecil", a, c), str(g), [str(a + c - g), "Sama besar", "Tidak bisa dibandingkan"],
                   "Saat berhitung, %d disebut lebih %s daripada %d." % (max(a, c), "akhir", min(a, c)) if big else "Saat berhitung, %d disebut lebih dulu daripada %d." % (min(a, c), max(a, c)))
    return named(f, "besar")


def m_bagi():
    def f():
        k = ch([2, 2, 3])
        g = ri(1, 5 if k == 2 else 3)
        n = k * g
        kind = ch(KINDS)
        return mcq("Ada %d %s. Dibagi sama banyak untuk %d anak. Setiap anak mendapat berapa?%s" % (n, b(kind), k, baris(n, kind)), str(g),
                   [str(x) for x in (g + 1, g - 1, n, k, g + 2) if x != g and x > 0], "%d %s dibagi %d sama banyak: setiap anak %d." % (n, b(kind), k, g))
    return named(f, "bagi")


def m_adil():
    def f():
        kind = ch(KINDS)
        a, c = ri(1, 5), ri(1, 5)
        if a != c and R().random() < 0.45:
            return None
        p = pic(P.groups_svg([(a, kind), (c, kind)]), "dua kelompok %s" % b(kind))
        g = "Sama banyak" if a == c else "Tidak sama banyak"
        return mcq("Apakah kedua kelompok %s ini sama banyak?%s" % (b(kind), p), g,
                   [x for x in ("Sama banyak", "Tidak sama banyak") if x != g] + ["Kelompok kiri kosong", "Tidak bisa diketahui"],
                   "Kiri %d, kanan %d. Jadi %s." % (a, c, g.lower()))
    return named(f, "adil")


def m_isi():
    def f():
        n = ri(3, 4)
        levs = pool([0.2, 0.35, 0.5, 0.65, 0.8, 0.95])[:n]
        w, h = 46, 80
        full = R().random() < 0.5
        c = max(levs) if full else min(levs)
        i = levs.index(c)
        p = pic(glasses_svg([(w, h, x) for x in levs]), "gelas A sampai %s berisi air" % "ABCD"[n - 1])
        return mcq("Gelas mana yang airnya paling %s?%s" % ("banyak" if full else "sedikit", p), "Gelas " + "ABCD"[i],
                   ["Gelas " + "ABCD"[j] for j in range(n) if j != i] + ["Semua sama banyak"],
                   "Gelasnya sama besar. Air gelas %s paling %s." % ("ABCD"[i], "tinggi" if full else "rendah"))
    return named(f, "isi")


WAKTU = {"morning": "pagi", "lunchtime": "siang", "afternoon": "sore", "night": "malam"}
KEGIATAN = [("bangun tidur", "pagi"), ("sarapan", "pagi"), ("berangkat ke sekolah", "pagi"), ("makan siang", "siang"),
            ("tidur siang", "siang"), ("bermain layang-layang", "sore"), ("mandi sore", "sore"), ("melihat bulan dan bintang", "malam"),
            ("tidur malam", "malam"), ("makan malam", "malam")]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
URUTAN = [["bangun tidur", "mandi", "sarapan", "berangkat ke sekolah"],
          ["menanam biji", "menyiram tanaman", "tanaman tumbuh", "tanaman berbunga"],
          ["mencuci tangan", "makan", "mencuci piring", "menyimpan piring"],
          ["pulang sekolah", "mengganti baju", "makan siang", "tidur siang"],
          ["memakai kaus kaki", "memakai sepatu", "mengikat tali sepatu", "berjalan ke luar rumah"]]
LAMA = [("tidur malam", "makan permen"), ("perjalanan naik kereta ke kota lain", "menutup pintu"), ("satu hari", "satu jam"),
        ("sekolah dari pagi sampai siang", "mencuci tangan"), ("menunggu padi dipanen", "menunggu air mendidih"), ("satu minggu", "satu hari")]


def m_waktu(kinds=(0, 1, 2, 3, 4, 5)):
    def f():
        k = ch(kinds)
        if k == 0:
            w = ch(list(WAKTU))
            return mcq("Gambar ini menunjukkan waktu …" + pic(sky_svg(w), "langit pada waktu %s" % WAKTU[w]), WAKTU[w], [x for x in WAKTU.values() if x != WAKTU[w]],
                       "Lihat matahari atau bulan di langit: %s." % WAKTU[w])
        if k == 1:
            a, g = ch(KEGIATAN)
            return mcq("Kita biasanya %s pada waktu …" % a, g, [x for x in WAKTU.values() if x != g], "%s biasanya dilakukan pada %s hari." % (cap(a), g))
        if k == 2:
            i = ri(0, 6)
            if R().random() < 0.5:
                g = HARI[(i + 1) % 7]
                return mcq("Hari ini hari %s. Besok hari …" % HARI[i], g, [h for h in pool(HARI) if h not in (g, HARI[i], HARI[i - 1])][:2] + [HARI[i - 1]],
                           "Sesudah %s adalah %s." % (HARI[i], g))
            g = HARI[i - 1]
            return mcq("Hari ini hari %s. Kemarin hari …" % HARI[i], g, [h for h in pool(HARI) if h not in (g, HARI[i], HARI[(i + 1) % 7])][:2] + [HARI[(i + 1) % 7]],
                       "Sebelum %s adalah %s." % (HARI[i], g))
        if k == 3:
            s = ri(0, 6)
            nn = ri(4, 5)
            ds = [HARI[(s + j) % 7] for j in range(nn)]
            hd = ri(0, nn - 1)
            g = ds[hd]
            return mcq("Hari apa yang tepat untuk tanda ?" + pic(days_svg(ds, hd), "urutan hari: " + ", ".join(d if j != hd else "?" for j, d in enumerate(ds))), g,
                       [h for h in pool(HARI) if h not in ds][:2] + [ds[hd - 1] if hd else ds[1]], "Urutan hari: %s." % ", ".join(ds))
        if k == 4:
            u = ch(URUTAN)
            j = ri(0, 4)
            if j == 0:
                return mcq("Urutan ini diacak: %s. Mana yang paling awal?" % ", ".join(sorted(u)), u[0], [x for x in u if x != u[0]], "Urutannya: %s." % ", ".join(u))
            if j == 4:
                return mcq("Urutan ini diacak: %s. Mana yang paling akhir?" % ", ".join(sorted(u)), u[3], [x for x in u if x != u[3]], "Urutannya: %s." % ", ".join(u))
            return mcq("Sesudah %s, lalu …" % u[j - 1], u[j], [x for x in u if x != u[j]], "Urutannya: %s." % ", ".join(u))
        a, c = ch(LAMA)
        x, y = sorted([a, c])
        return mcq("Mana yang lebih lama: %s atau %s?" % (x, y), cap(a), [cap(c), "Sama lama", "Tidak bisa dibandingkan"], "%s memerlukan waktu lebih lama." % cap(a))
    return named(f, "waktu")


KELOMPOK = {"buah": ["apel", "jeruk", "pisang", "mangga", "semangka", "pepaya", "rambutan", "salak"],
            "hewan": ["kucing", "ayam", "sapi", "kambing", "bebek", "kelinci", "gajah", "kuda"],
            "kendaraan": ["mobil", "sepeda", "bus", "kereta", "perahu", "becak", "pesawat", "motor"],
            "alat tulis": ["pensil", "penghapus", "penggaris", "buku tulis", "krayon", "pulpen", "rautan"],
            "pakaian": ["baju", "celana", "topi", "kaus kaki", "sepatu", "jaket", "rok"]}


def m_klasifikasi(kinds=(0, 1)):
    def f():
        cat, other = pool(list(KELOMPOK))[:2]
        k = ch(kinds)
        if k == 0:
            three = pool(KELOMPOK[cat])[:3]
            odd = ch(KELOMPOK[other])
            items = sorted(three + [odd])
            return mcq("Manakah yang bukan %s? (%s)" % (cat, ", ".join(items)), odd, three, "%s termasuk %s, bukan %s." % (cap(odd), other, cat))
        three = pool(KELOMPOK[cat])[:3]
        return mcq("%s, %s, dan %s termasuk kelompok …" % (cap(three[0]), three[1], three[2]), cat, [x for x in KELOMPOK if x != cat][:3],
                   "Semuanya %s." % cat)
    return named(f, "klasifikasi")


def m_warna():
    def f():
        col = ch(list(WARNA))
        n = ri(1, 5)
        others = [c for c in WARNA if c != col]
        items = [(ch(BASIC), col) for _ in range(n)] + [(ch(BASIC), ch(others)) for _ in range(ri(3, 6))]
        R().shuffle(items)
        return mcq("Ada berapa bangun berwarna %s?%s" % (WARNA[col], pic(P.shapes_mix_svg(items, ri(1, 9999)), "berbagai bangun berwarna")), str(n),
                   [str(x) for x in (n + 1, n - 1, n + 2, len(items)) if x != n and x >= 0], "Hitung yang berwarna %s saja: %d." % (WARNA[col], n))
    return named(f, "warna")


def le(mk, n):
    """答えと選択肢に n を超える数がある問題を落とす"""
    import re

    def f():
        it = mk()
        if it is None:
            return None
        for c in it["c"]:
            for x in re.findall(r"\d+", re.sub(r"<[^>]+>", "", c)):
                if int(x) > n:
                    return None
        return it
    return named(f, mk.__name__)


# ------------------------------------------------------------ 単元
def UNITS():
    U = []
    U.append(dict(slug="membilang-sampai-10", dom="B", title="Membilang Benda sampai 10", short="Membilang sampai 10",
                  std="Anak mengenal dan membilang banyak benda sampai 10, serta menghubungkan banyak benda dengan lambang bilangan.",
                  meta="Latihan membilang sampai 10 untuk anak TK: menghitung benda, bingkai sepuluh, titik dadu, serta membaca dan menulis lambang bilangan. 100 soal bergambar dengan kunci jawaban.",
                  kb="Hitung satu per satu", ks="Bilangan terakhir yang disebut = banyaknya benda.",
                  sets=[("Menghitung benda berjajar", [(m_hitung(1, 10), 20)]), ("Menghitung benda", [(m_hitung(1, 10), 20)]),
                        ("Titik dadu", [(m_dadu(), 12), (m_hitung(1, 10), 8)]), ("Lambang bilangan", [(m_kata(1, 10), 20)]),
                        ("Campuran", [(m_hitung(1, 10), 14), (m_dadu(), 6)])],
                  think=["Tunjuk setiap benda satu kali sambil menyebut bilangan.", "Bilangan terakhir yang disebut adalah banyaknya benda.", "Setiap banyak benda punya lambang bilangan: tiga benda ditulis 3."],
                  ex=[("Ada berapa bola? (5 bola)", ["satu, dua, tiga, empat, lima"], "5"), ("Lambang bilangan <i>tujuh</i>?", ["tujuh ditulis 7"], "7")],
                  mist=[["Benda dihitung dua kali", "Tandai benda yang sudah dihitung"], ["Ada benda yang terlewat", "Hitung dari kiri ke kanan"], ["Angka 6 dan 9 tertukar", "Bulatan 6 di bawah, bulatan 9 di atas"]],
                  faq=[["Bagaimana membantu anak menghitung?", "Ajak anak menunjuk atau memindahkan benda satu per satu sambil menyebut bilangan."], ["Apa itu bingkai sepuluh?", "Kotak dengan 10 tempat (2 baris berisi 5). Anak bisa melihat banyak benda tanpa menghitung satu per satu."], ["Sampai berapa anak TK berhitung?", "Anak TK biasanya membilang benda sampai 10 dan menyebut urutan bilangan sampai 20."]]))
    U.append(dict(slug="bilangan-sampai-20", dom="B", title="Mengenal Bilangan sampai 20", short="Bilangan sampai 20",
                  std="Anak menyebutkan urutan bilangan sampai 20, membilang benda, dan mengenal lambang bilangan 11 sampai 20.",
                  meta="Latihan bilangan sampai 20 untuk anak TK: menghitung benda 11–20, dua bingkai sepuluh, membaca lambang bilangan, sebelum dan sesudah. 100 soal bergambar dengan kunci jawaban.",
                  kb="10 dan beberapa lagi", ks="13 = sepuluh dan tiga lagi.",
                  sets=[("Menghitung benda 11 sampai 20", [(m_hitung(11, 20), 20)]), ("Membaca lambang bilangan", [(m_kata(11, 20), 20)]),
                        ("Sesudah dan sebelum", [(m_sesudah(0, 20), 20)]), ("Bilangan yang hilang", [(m_urut(0, 20), 20)]),
                        ("Campuran", [(m_hitung(11, 20), 10), (m_sesudah(0, 20), 10)])],
                  think=["Bilangan 11 sampai 20 adalah sepuluh dan beberapa lagi.", "Penuhi bingkai sepuluh dulu, lalu hitung sisanya.", "Sesudah berarti satu lebih banyak. Sebelum berarti satu lebih sedikit."],
                  ex=[("Satu bingkai penuh dan 4 titik lagi", ["10 dan 4"], "14"), ("Sesudah 15?", ["15, 16"], "16")],
                  mist=[["12 ditulis 21", "Tulis angka 1 dulu, lalu 2"], ["Sesudah 19 dijawab 110", "Sesudah 19 adalah 20"], ["Menghitung ulang dari 1 setiap kali", "Mulai dari 10, lalu lanjutkan"]],
                  faq=[["Mengapa bilangan belasan sulit?", "Karena namanya (sebelas, dua belas) tidak sama dengan cara menulisnya. Bingkai sepuluh membantu anak melihat sepuluh dan sisanya."], ["Apa itu bilangan sebelum?", "Bilangan yang tepat satu lebih sedikit, misalnya sebelum 12 adalah 11."], ["Bagaimana berlatih di rumah?", "Hitung anak tangga, kancing baju, atau buah sambil menyebut bilangan."]]))
    U.append(dict(slug="membandingkan-banyak-benda", dom="B", title="Membandingkan Banyak Benda", short="Membandingkan Banyak Benda",
                  std="Anak membandingkan dua kumpulan benda dan menggunakan kata lebih banyak, lebih sedikit, dan sama banyak.",
                  meta="Latihan membandingkan banyak benda untuk anak TK: lebih banyak, lebih sedikit, sama banyak, serta bilangan terbesar dan terkecil sampai 10. 100 soal bergambar dengan kunci jawaban.",
                  kb="Lebih banyak, lebih sedikit, sama banyak", ks="Pasangkan satu-satu. Yang bersisa lebih banyak.",
                  sets=[("Lebih banyak", [(m_banyak_sedikit(9, False), 20)]), ("Lebih sedikit", [(m_banyak_sedikit(9, True), 20)]),
                        ("Bilangan lebih besar", [(m_besar(), 20)]), ("Terbesar dan terkecil", [(m_ekstrem(1, 10), 20)]),
                        ("Campuran", [(m_banyak_sedikit(10), 20)])],
                  think=["Pasangkan benda satu dengan satu. Kelompok yang masih bersisa lebih banyak.", "Kalau semua punya pasangan, kedua kelompok sama banyak.", "Bilangan yang disebut lebih akhir saat berhitung lebih besar."],
                  ex=[("5 apel dan 3 jeruk", ["5 lebih dari 3"], "Apel lebih banyak"), ("Mana lebih besar: 7 atau 4?", ["4, 5, 6, 7"], "7")],
                  mist=[["Benda besar dianggap lebih banyak", "Yang dihitung banyaknya, bukan besarnya"], ["Barisan panjang dianggap lebih banyak", "Hitung bendanya, bukan panjang barisan"], ["Lebih sedikit dan lebih banyak tertukar", "Sedikit berarti kurang"]],
                  faq=[["Apa itu korespondensi satu-satu?", "Memasangkan setiap benda di satu kelompok dengan tepat satu benda di kelompok lain."], ["Mengapa ukuran benda tidak berpengaruh?", "Lima semut dan lima gajah sama banyak; yang dibandingkan adalah banyaknya."], ["Apa tanda &lt; dan &gt;?", "Anak TK cukup memakai kata lebih banyak dan lebih sedikit. Tanda dipelajari di SD."]]))
    U.append(dict(slug="urutan-bilangan", dom="B", title="Urutan Bilangan dan Urutan Ke-", short="Urutan Bilangan",
                  std="Anak menyebutkan urutan bilangan, melengkapi bilangan yang hilang, dan mengenal urutan pertama, kedua, ketiga.",
                  meta="Latihan urutan bilangan untuk anak TK: sebelum, sesudah, di antara, bilangan yang hilang, mengurutkan bilangan sampai 10, dan urutan ke- dari kiri dan kanan. 100 soal dengan kunci jawaban.",
                  kb="1, 2, 3, 4, 5 …", ks="Sesudah: tambah satu. Sebelum: kurang satu.",
                  sets=[("Sesudah dan sebelum", [(m_sesudah(0, 10), 20)]), ("Bilangan yang hilang", [(m_urut(0, 10), 20)]),
                        ("Mengurutkan bilangan", [(m_urutkan(1, 10), 20)]), ("Urutan ke-", [(m_kanan_kiri(), 20)]),
                        ("Campuran", [(m_urutkan(1, 10), 10), (m_kanan_kiri(), 10)])],
                  think=["Bilangan selalu berurutan: 0, 1, 2, 3, … 10.", "Bilangan sesudah satu lebih banyak, bilangan sebelum satu lebih sedikit.", "Urutan ke- dihitung dari sisi yang disebut: dari kiri atau dari kanan."],
                  ex=[("3, 4, …, 6", ["sesudah 4 adalah 5"], "5"), ("Urutkan dari terkecil: 6, 2, 9, 4", ["2 paling kecil"], "2, 4, 6, 9")],
                  mist=[["Urutan dari kanan dihitung dari kiri", "Mulai dari sisi yang disebut"], ["Sebelum 7 dijawab 8", "Sebelum berarti kurang satu: 6"], ["Mengurutkan tanpa membandingkan semua", "Cari yang terkecil dulu, lalu berikutnya"]],
                  faq=[["Apa beda bilangan dan urutan ke-?", "Bilangan menyatakan banyak (3 bola), urutan ke- menyatakan posisi (bola ketiga)."], ["Bagaimana melatih urutan bilangan?", "Lompat di petak bernomor, menyusun kartu angka, atau menghitung anak tangga."], ["Apa itu bilangan di antara?", "Bilangan yang terletak di tengah dua bilangan, misalnya di antara 4 dan 6 adalah 5."]]))
    U.append(dict(slug="menambah-benda", dom="B", title="Menggabungkan dan Menambah Benda", short="Menambah Benda",
                  std="Anak menggabungkan dua kumpulan benda dan menyebutkan banyaknya setelah ditambah, sampai 10.",
                  meta="Latihan menambah benda untuk anak TK: menggabungkan dua kelompok gambar, lompat maju di garis bilangan, pasangan bilangan, dan cerita sederhana sampai 10. 100 soal bergambar dengan kunci jawaban.",
                  kb="Tambah = digabung jadi lebih banyak", ks="Mulai dari yang banyak, lalu hitung maju.",
                  sets=[("Menggabungkan gambar", [(m_tambah_gambar(10), 20)]), ("Lompat maju", [(m_lompat("+", 10), 20)]),
                        ("Menggabungkan lagi", [(m_tambah_gambar(10), 20)]), ("Pasangan bilangan", [(m_ikatan(10), 20)]),
                        ("Cerita", [(le(m_cerita(10, "+"), 10), 20)])],
                  think=["Menambah berarti menggabungkan, jadi bendanya bertambah banyak.", "Mulai dari kelompok yang lebih banyak, lalu hitung maju satu per satu.", "Bilangan 5 bisa dipecah menjadi 2 dan 3, atau 1 dan 4."],
                  ex=[("3 bola dan 2 bola", ["3, lalu 4, 5"], "5"), ("4 burung, datang 3 lagi", ["4, lalu 5, 6, 7"], "7")],
                  mist=[["Menghitung ulang dari 1", "Mulai dari bilangan yang lebih besar"], ["Ditambah malah berkurang", "Digabung pasti bertambah"], ["Lompatan pertama ikut dihitung dari angka awal", "Lompat dulu, baru hitung"]],
                  faq=[["Apakah anak TK perlu menulis 3 + 2?", "Belum harus. Yang penting anak paham menggabungkan dan menghitung hasilnya; lambang + dikenalkan perlahan."], ["Apa itu pasangan bilangan?", "Dua bilangan yang digabung menjadi bilangan tertentu, misalnya 6 dan 4 menjadi 10."], ["Benda apa yang cocok untuk berlatih?", "Kelereng, kancing, biji-bijian, atau balok mainan."]]))
    U.append(dict(slug="mengurangi-benda", dom="B", title="Memisahkan dan Mengurangi Benda", short="Mengurangi Benda",
                  std="Anak mengambil sebagian benda dari suatu kumpulan dan menyebutkan banyak benda yang tersisa, sampai 10.",
                  meta="Latihan mengurangi benda untuk anak TK: mencoret gambar, lompat mundur di garis bilangan, benda di dalam kotak, dan cerita sederhana sampai 10. 100 soal bergambar dengan kunci jawaban.",
                  kb="Kurang = diambil jadi lebih sedikit", ks="Hitung benda yang tidak dicoret.",
                  sets=[("Mencoret gambar", [(m_coret(10), 20)]), ("Lompat mundur", [(m_lompat("-", 10), 20)]),
                        ("Benda di dalam kotak", [(m_kotak(10), 20)]), ("Mencoret lagi", [(m_coret(10), 20)]),
                        ("Cerita", [(le(m_cerita(10, "-"), 10), 20)])],
                  think=["Mengurangi berarti mengambil sebagian benda, jadi bendanya berkurang.", "Coret benda yang diambil, lalu hitung yang tersisa.", "Bisa juga mundur di garis bilangan."],
                  ex=[("7 kue, dimakan 2", ["coret 2, hitung sisanya"], "5"), ("Mulai 6, mundur 3", ["5, 4, 3"], "3")],
                  mist=[["Yang dicoret ikut dihitung", "Hitung yang tidak dicoret saja"], ["Mundur dihitung maju", "Mengurangi berarti mundur"], ["Menjawab banyak yang diambil", "Pertanyaannya: berapa yang tersisa"]],
                  faq=[["Bagaimana mengenalkan pengurangan?", "Pakai benda nyata: ambil beberapa, lalu hitung yang tersisa."], ["Apa hubungan menambah dan mengurangi?", "Keduanya kebalikan: 3 dan 2 menjadi 5, 5 diambil 2 tersisa 3."], ["Kapan anak menulis tanda −?", "Lambang − mulai dipakai di kelas 1 SD. Di TK cukup dengan benda dan gambar."]]))
    U.append(dict(slug="membagi-sama-banyak", dom="B", title="Membagi Sama Banyak", short="Membagi Sama Banyak",
                  std="Anak membagi benda sama banyak kepada beberapa teman dan membandingkan apakah dua kelompok sama banyak.",
                  meta="Latihan membagi sama banyak untuk anak TK: membagi benda kepada 2 atau 3 anak dan memeriksa kelompok yang sama banyak. 100 soal bergambar dengan kunci jawaban.",
                  kb="Setiap anak mendapat sama banyak", ks="Bagikan satu-satu bergiliran.",
                  sets=[("Membagi untuk 2 atau 3 anak", [(m_bagi(), 20)]), ("Sama banyak atau tidak", [(m_adil(), 20)]),
                        ("Membagi lagi", [(m_bagi(), 20)]), ("Memeriksa kelompok", [(m_adil(), 20)]),
                        ("Campuran", [(m_bagi(), 10), (m_adil(), 10)])],
                  think=["Membagi sama banyak berarti setiap anak mendapat jumlah yang sama.", "Bagikan satu benda untuk setiap anak bergiliran sampai habis.", "Hitung bagian setiap anak untuk memeriksa."],
                  ex=[("6 kue untuk 2 anak", ["bergiliran: 1, 1, 2, 2, 3, 3"], "3 kue"), ("Kelompok 4 dan 3", ["4 bukan 3"], "Tidak sama banyak")],
                  mist=[["Yang satu mendapat lebih banyak", "Periksa: semua harus sama"], ["Menjawab jumlah semua benda", "Pertanyaannya: bagian setiap anak"], ["Ada benda yang tidak dibagikan", "Bagikan sampai habis"]],
                  faq=[["Mengapa anak TK belajar membagi?", "Membagi sama banyak adalah awal dari konsep pembagian, dan dekat dengan kebiasaan berbagi."], ["Bagaimana berlatih di rumah?", "Minta anak membagi biskuit atau kelereng sama banyak untuk anggota keluarga."], ["Bagaimana jika ada sisa?", "Di TK dipakai jumlah yang dapat dibagi habis. Sisa dipelajari kemudian."]]))
    U.append(dict(slug="mengenal-bentuk", dom="G", title="Mengenal Bentuk Datar dan Bangun Ruang", short="Mengenal Bentuk",
                  std="Anak mengenal bentuk lingkaran, segitiga, persegi, dan persegi panjang serta bola, kubus, balok, tabung, dan kerucut pada benda di sekitarnya.",
                  meta="Latihan mengenal bentuk untuk anak TK: lingkaran, segitiga, persegi, persegi panjang, bola, kubus, balok, tabung, kerucut, dan bentuk benda di sekitar. 100 soal bergambar dengan kunci jawaban.",
                  kb="Lingkaran, segitiga, persegi", ks="Lihat sisi dan sudutnya.",
                  sets=[("Nama bentuk datar", [(m_nama_datar(BASIC), 10), (m_cari_datar(BASIC), 10)]), ("Menghitung bentuk", [(m_hitung_datar(), 20)]),
                        ("Bentuk benda di sekitar", [(m_datar_nyata(), 14), (m_nama_datar(BASIC), 6)]), ("Bangun ruang", [(m_ruang(), 10), (m_ruang_nyata(), 10)]),
                        ("Menggelinding atau tidak", [(m_gelinding(), 20)])],
                  think=["Lingkaran bulat tanpa sudut. Segitiga punya 3 sisi. Persegi punya 4 sisi sama panjang.", "Bangun ruang bisa dipegang: bola, kubus, balok, tabung, kerucut.", "Benda bersisi lengkung dapat menggelinding."],
                  ex=[("Bentuk roda?", ["bulat, tanpa sudut"], "lingkaran"), ("Bentuk kaleng susu?", ["atas dan bawah lingkaran"], "tabung")],
                  mist=[["Persegi yang diputar dianggap bukan persegi", "Diputar tetap persegi"], ["Lingkaran dan bola tertukar", "Lingkaran datar, bola bisa dipegang"], ["Kubus dan balok tertukar", "Sisi kubus semua sama"]],
                  faq=[["Apa beda bentuk datar dan bangun ruang?", "Bentuk datar seperti gambar di kertas; bangun ruang punya isi dan bisa dipegang."], ["Bagaimana mengenalkan bentuk?", "Ajak anak mencari bentuk di rumah: jam dinding, pintu, kotak, bola."], ["Apa itu sudut?", "Titik tempat dua sisi bertemu, seperti pojok buku."]]))
    U.append(dict(slug="posisi-dan-arah", dom="G", title="Posisi dan Arah", short="Posisi dan Arah",
                  std="Anak menyebutkan posisi benda dengan kata di atas, di bawah, di depan, di belakang, di samping, kiri, dan kanan.",
                  meta="Latihan posisi dan arah untuk anak TK: di atas, di bawah, di depan, di belakang, di samping, kiri, kanan, dan urutan benda di rak. 100 soal bergambar dengan kunci jawaban.",
                  kb="Atas, bawah, depan, belakang", ks="Kiri dan kanan dilihat dari kita.",
                  sets=[("Di atas, di bawah, di samping", [(m_meja(), 20)]), ("Di depan dan di belakang", [(m_kardus(), 20)]),
                        ("Rak bertingkat", [(m_rak(), 20)]), ("Kiri dan kanan", [(m_kanan_kiri(), 20)]),
                        ("Campuran", [(m_rak(), 10), (m_kanan_kiri(), 10)])],
                  think=["Posisi benda disebut dari benda lain: bola di atas meja.", "Depan adalah yang lebih dekat dengan kita, belakang yang lebih jauh.", "Kiri dan kanan dilihat dari arah kita melihat gambar."],
                  ex=[("Kucing di bawah meja", ["meja di atas, kucing di bawahnya"], "di bawah meja"), ("Apel, bola, ikan. Di sebelah kanan apel?", ["apel, lalu bola"], "bola")],
                  mist=[["Kiri dan kanan tertukar", "Tangan yang dipakai makan biasanya kanan"], ["Di depan dan di belakang tertukar", "Depan lebih dekat dengan kita"], ["Rak dihitung dari bawah", "Baca pertanyaan: dari atas atau dari bawah"]],
                  faq=[["Mengapa posisi penting?", "Kata posisi dipakai untuk mengikuti petunjuk, membaca peta, dan bermain."], ["Bagaimana melatih kiri dan kanan?", "Pakai gelang di tangan kanan atau bermain 'angkat tangan kanan'."], ["Apa itu di samping?", "Di sebelah kiri atau kanan benda lain."]]))
    U.append(dict(slug="membandingkan-ukuran", dom="P", title="Membandingkan Panjang, Tinggi, Berat, dan Isi", short="Membandingkan Ukuran",
                  std="Anak membandingkan panjang, tinggi, berat, dan isi benda dengan kata panjang-pendek, tinggi-rendah, berat-ringan, dan banyak-sedikit.",
                  meta="Latihan membandingkan ukuran untuk anak TK: paling panjang dan pendek, paling tinggi dan rendah, berat dan ringan dengan timbangan, serta isi air di gelas. 100 soal bergambar dengan kunci jawaban.",
                  kb="Panjang-pendek, berat-ringan", ks="Jajarkan ujung benda sebelum membandingkan.",
                  sets=[("Panjang dan pendek", [(m_panjang(), 20)]), ("Tinggi dan rendah", [(m_tinggi(), 20)]),
                        ("Berat dan ringan", [(m_berat(), 14), (m_seimbang(), 6)]), ("Isi air di gelas", [(m_isi(), 20)]),
                        ("Campuran", [(m_panjang(), 6), (m_tinggi(), 6), (m_isi(), 8)])],
                  think=["Untuk membandingkan panjang, jajarkan ujung benda di garis yang sama.", "Pada timbangan, sisi yang turun lebih berat.", "Pada gelas yang sama besar, air yang lebih tinggi lebih banyak."],
                  ex=[("Pensil A ujungnya paling jauh", ["ujung kiri sejajar"], "Pensil A paling panjang"), ("Timbangan turun di sisi bola", ["yang turun lebih berat"], "Bola lebih berat")],
                  mist=[["Ujung tidak dijajarkan", "Mulai dari garis yang sama"], ["Benda besar dianggap pasti berat", "Lihat timbangannya"], ["Sisi timbangan yang naik dianggap berat", "Yang turun lebih berat"]],
                  faq=[["Apakah anak TK memakai penggaris?", "Belum harus. Anak TK membandingkan langsung atau dengan satuan tidak baku seperti jengkal."], ["Bagaimana berlatih membandingkan berat?", "Minta anak memegang dua benda dengan kedua tangan dan merasakan mana yang lebih berat."], ["Apa itu isi atau kapasitas?", "Banyaknya air atau pasir yang dapat dimuat suatu wadah."]]))
    U.append(dict(slug="waktu-sehari-hari", dom="P", title="Waktu dan Kegiatan Sehari-hari", short="Waktu Sehari-hari",
                  std="Anak mengenal waktu pagi, siang, sore, dan malam, nama hari, serta urutan kegiatan sehari-hari.",
                  meta="Latihan waktu untuk anak TK: pagi, siang, sore, malam, nama-nama hari, besok dan kemarin, urutan kegiatan, dan mana yang lebih lama. 100 soal dengan kunci jawaban.",
                  kb="Pagi, siang, sore, malam", ks="Senin, Selasa, Rabu, Kamis, Jumat, Sabtu, Minggu.",
                  sets=[("Pagi, siang, sore, malam", [(m_waktu((0, 1)), 14), (m_waktu((5,)), 6)]), ("Nama hari", [(m_waktu((2,)), 14), (m_waktu((3,)), 6)]),
                        ("Urutan hari", [(m_waktu((3,)), 20)]), ("Urutan kegiatan", [(m_waktu((4,)), 20)]),
                        ("Campuran", [(m_waktu((1, 2, 3, 4)), 20)])],
                  think=["Matahari terbit pada pagi hari dan terbenam pada sore hari. Malam hari langit gelap.", "Ada 7 hari dalam satu minggu, selalu berurutan.", "Kegiatan dilakukan berurutan: sesudah bangun tidur, kita mandi."],
                  ex=[("Hari ini Rabu. Besok?", ["Rabu, lalu Kamis"], "Kamis"), ("Kapan kita sarapan?", ["sarapan sesudah bangun tidur"], "pagi")],
                  mist=[["Besok dan kemarin tertukar", "Besok sesudah hari ini, kemarin sebelum hari ini"], ["Minggu dianggap hari pertama sekolah", "Sekolah mulai hari Senin"], ["Urutan kegiatan diacak", "Pikirkan apa yang harus dilakukan lebih dulu"]],
                  faq=[["Kapan anak belajar membaca jam?", "Membaca jam dimulai di kelas 1 SD. Di TK anak mengenal pagi, siang, sore, malam, dan nama hari."], ["Bagaimana mengenalkan nama hari?", "Nyanyikan lagu nama hari dan tandai kegiatan setiap hari di kalender."], ["Apa itu urutan kegiatan?", "Langkah-langkah yang dilakukan berurutan, misalnya mencuci tangan sebelum makan."]]))
    U.append(dict(slug="pola", dom="A", title="Mengenal dan Melanjutkan Pola", short="Pola",
                  std="Anak mengenal, meniru, dan melanjutkan pola berulang dari gambar, bentuk, warna, dan bilangan sederhana.",
                  meta="Latihan pola untuk anak TK: pola gambar berulang AB, ABC, AAB, pola bentuk dan warna, serta pola bilangan sampai 20. 100 soal bergambar dengan kunci jawaban.",
                  kb="Cari bagian yang berulang", ks="Ulangi bagian itu untuk melanjutkan pola.",
                  sets=[("Pola gambar", [(m_pola(), 20)]), ("Pola bentuk dan warna", [(m_pola(), 20)]), ("Pola lagi", [(m_pola(), 20)]),
                        ("Pola bilangan", [(m_pola_bil(20, (1, 2)), 20)]), ("Campuran", [(m_pola(), 12), (m_pola_bil(20, (1,)), 8)])],
                  think=["Pola adalah susunan yang bagian-bagiannya berulang.", "Cari bagian yang berulang, misalnya merah, biru, merah, biru.", "Pada pola bilangan, setiap langkah bertambah atau berkurang sama banyak."],
                  ex=[("bola, apel, bola, apel, …", ["bagian berulang: bola, apel"], "bola"), ("2, 4, 6, …", ["tambah 2"], "8")],
                  mist=[["Hanya melihat gambar terakhir", "Lihat bagian yang berulang dari awal"], ["Pola AAB diteruskan AB", "Ulangi bagian lengkapnya: A, A, B"], ["Pola bilangan turun diteruskan naik", "Lihat apakah bilangannya makin besar atau kecil"]],
                  faq=[["Mengapa pola penting?", "Mengenali pola melatih anak berpikir teratur dan menjadi dasar aljabar."], ["Di mana ada pola?", "Motif batik, ubin lantai, kalung manik-manik, dan lagu."], ["Bagaimana berlatih pola?", "Ajak anak menyusun manik-manik atau balok warna dengan pola, lalu melanjutkannya."]]))
    U.append(dict(slug="mengelompokkan-dan-data", dom="D", title="Mengelompokkan Benda dan Membaca Data", short="Mengelompokkan Benda",
                  std="Anak mengelompokkan benda berdasarkan jenis, warna, dan bentuk, serta membaca data sederhana dalam gambar.",
                  meta="Latihan mengelompokkan untuk anak TK: kelompok buah, hewan, kendaraan, benda yang bukan anggota kelompok, menghitung warna, dan membaca piktogram. 100 soal bergambar dengan kunci jawaban.",
                  kb="Kelompokkan menurut jenis, warna, bentuk", ks="Cari yang berbeda dari yang lain.",
                  sets=[("Bukan anggota kelompok", [(m_klasifikasi((0,)), 20)]), ("Nama kelompok", [(m_klasifikasi((1,)), 20)]),
                        ("Menghitung menurut warna", [(m_warna(), 20)]), ("Membaca piktogram", [(m_data(6, "pikto", (0, 1)), 20)]),
                        ("Campuran", [(m_klasifikasi((0, 1)), 10), (m_warna(), 10)])],
                  think=["Benda dapat dikelompokkan menurut jenisnya: buah, hewan, kendaraan.", "Benda juga dapat dikelompokkan menurut warna atau bentuk.", "Gambar berjajar (piktogram) menunjukkan banyak benda setiap kelompok."],
                  ex=[("apel, jeruk, mobil, pisang", ["mobil bukan buah"], "mobil"), ("Ada 3 bangun merah dan 2 biru", ["hitung yang merah saja"], "3")],
                  mist=[["Mengelompokkan menurut ukuran saja", "Perhatikan aturan pengelompokannya"], ["Semua bangun dihitung", "Hitung yang warnanya diminta saja"], ["Membaca baris yang salah pada piktogram", "Ikuti baris dari namanya"]],
                  faq=[["Apa manfaat mengelompokkan?", "Melatih anak melihat persamaan dan perbedaan, dasar dari berpikir logis dan membaca data."], ["Bagaimana berlatih di rumah?", "Minta anak merapikan mainan menurut jenis atau warna."], ["Apa itu piktogram?", "Data yang ditampilkan dengan gambar; setiap gambar mewakili satu benda."]]))
    return U


def build(i):
    rnd = random.Random(40000 + i)
    A.setup(rnd)
    d = UNITS()[i - 1]
    body = lesson(d["think"], [example(q, s, a) for q, s, a in d["ex"]], d["mist"])
    faq = [{"q": q, "a": a} for q, a in d["faq"]]
    seen = set()
    sets = []
    for t, parts in d["sets"]:
        try:
            sets.append((t, mix(rnd, seen, parts)))
        except AssertionError as e:
            raise AssertionError("%s / %s / %s: %s" % (d["slug"], t, [m.__name__ for m, _ in parts], e))
    make_unit(rnd, d["slug"], d["dom"], d["std"] + " (Capaian Pembelajaran Fase Fondasi)", d["title"], d["short"], d["meta"], d["kb"], d["ks"],
              body, faq, sets, i, grade="tk", fase="Fase Fondasi")
    return d["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    for i in range(1, len(UNITS()) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(i), flush=True)
