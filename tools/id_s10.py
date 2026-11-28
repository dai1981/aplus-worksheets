# -*- coding: utf-8 -*-
"""Indonesia / IPA Kelas 10（Fase E。Buku Siswa IPA Kelas X Kurikulum Merdeka edisi revisi）"""
from id_sci import H, nq, num, it

EL = [(1, "H", "hidrogen", 1), (2, "He", "helium", 4), (3, "Li", "litium", 7), (4, "Be", "berilium", 9), (5, "B", "boron", 11), (6, "C", "karbon", 12), (7, "N", "nitrogen", 14),
      (8, "O", "oksigen", 16), (9, "F", "fluorin", 19), (10, "Ne", "neon", 20), (11, "Na", "natrium", 23), (12, "Mg", "magnesium", 24), (13, "Al", "aluminium", 27), (14, "Si", "silikon", 28),
      (15, "P", "fosfor", 31), (16, "S", "belerang", 32), (17, "Cl", "klorin", 35), (18, "Ar", "argon", 40), (19, "K", "kalium", 39), (20, "Ca", "kalsium", 40)]
ROMAN = {1: "IA", 2: "IIA", 3: "IIIA", 4: "IVA", 5: "VA", 6: "VIA", 7: "VIIA", 8: "VIIIA"}


def shells(z):
    out, caps = [], [2, 8, 8, 2]
    for c in caps:
        if z <= 0:
            break
        out.append(min(c, z))
        z -= min(c, z)
    return out


def f_atom(R):
    z, sym, name, a = R.choice(EL[2:])
    k = R.choice(["p", "n", "e", "ion", "konf", "val", "gol", "per"])
    if k == "p":
        return nq("Atom %s memiliki nomor atom %d dan nomor massa %d. Berapa jumlah protonnya?" % (name, z, a), z, [a, a - z if a - z != z else a + z, a + z], "",
                  "Jumlah proton = nomor atom = %d." % z)
    if k == "n":
        if a - z == z:
            return None
        return nq("Atom %s memiliki nomor atom %d dan nomor massa %d. Berapa jumlah neutronnya?" % (name, z, a), a - z, [a, z, a + z], "", "Neutron = nomor massa − nomor atom = %d − %d = %d." % (a, z, a - z))
    if k == "e":
        return nq("Atom netral %s (nomor atom %d, nomor massa %d) memiliki berapa elektron?" % (name, z, a), z, [a, a - z if a - z != z else z + 1, z + 2], "", "Pada atom netral, jumlah elektron = jumlah proton = %d." % z)
    if k == "ion":
        if z not in (11, 12, 13, 19, 20, 8, 9, 16, 17):
            return None
        q = {11: 1, 12: 2, 13: 3, 19: 1, 20: 2, 8: -2, 9: -1, 16: -2, 17: -1}[z]
        lab = sym + ("⁺" if q == 1 else "²⁺" if q == 2 else "³⁺" if q == 3 else "⁻" if q == -1 else "²⁻")
        return nq("Berapa jumlah elektron pada ion %s (nomor atom %s = %d)?" % (lab, sym, z), z - q, [z + q, z, a - z], "", "Elektron = %d %s %d = %d." % (z, "−" if q > 0 else "+", abs(q), z - q))
    sh = shells(z)
    if k == "konf":
        right = " ".join(str(x) for x in sh)
        wr = set()
        if len(sh) >= 2:
            wr.add(" ".join(str(x) for x in sh[:-2] + [sh[-2] + sh[-1]]) if sh[-2] + sh[-1] <= 18 else "2 18")
        wr.add(" ".join(str(x) for x in [2] + [z - 2]) if z > 2 else "1 1")
        wr.add(" ".join(str(x) for x in ([2, 8, z - 10] if z > 10 else [2, z - 2, 0])))
        if z > 18:
            wr.add("2 8 9" if z == 19 else "2 8 10")
        wr.add(" ".join(str(x) for x in ([1] + sh[1:] + [1])))
        wr = sorted(x for x in wr if x != right)
        if len(wr) < 3:
            return None
        return it("Bagaimana konfigurasi elektron (kulit K L M N) atom %s dengan nomor atom %d?" % (name, z), right, R.sample(wr, 3), "Isi kulit K maksimal 2, L maksimal 8, lalu M: %s." % right)
    if k == "val":
        return nq("Berapa elektron valensi atom %s (nomor atom %d)?" % (name, z), sh[-1], [len(sh), z, sh[0], 8 - sh[-1] if sh[-1] != 4 else 2], "",
                  "Konfigurasi %s, jadi elektron valensinya %d." % (" ".join(map(str, sh)), sh[-1]))
    if k == "gol":
        g = 8 if z in (10, 18) else sh[-1]
        right = "golongan " + ROMAN[g]
        wr = sorted({"golongan " + ROMAN[x] for x in range(1, 9)} - {right})
        return it("Atom %s memiliki nomor atom %d. Termasuk golongan berapa dalam sistem periodik?" % (name, z), right, R.sample(wr, 3), "Konfigurasi %s; elektron valensi %d sehingga %s." % (" ".join(map(str, sh)), sh[-1], right))
    right = "periode %d" % len(sh)
    wr = sorted({"periode %d" % x for x in range(1, 7)} - {right})
    return it("Atom %s memiliki nomor atom %d. Terletak pada periode berapa?" % (name, z), right, R.sample(wr, 3), "Konfigurasi %s menempati %d kulit, jadi %s." % (" ".join(map(str, sh)), len(sh), right))


def f_angka(R):
    k = R.choice(["ap", "kali", "bulat"])
    if k == "ap":
        x, n = R.choice([("0,0045", 2), ("2,50", 3), ("1.200", 2), ("105", 3), ("0,800", 3), ("3,14", 3), ("60,0", 3), ("0,020", 2), ("4,005", 4), ("12,30", 4), ("0,0102", 3), ("7", 1)])
        return nq("Berapa banyak angka penting pada hasil pengukuran %s m?" % x, n, [n + 1, n - 1 if n > 1 else n + 3, len(x.replace(",", "").replace(".", "")), n + 2], "",
                  "Nol di depan angka bukan nol tidak penting, nol di antara atau di belakang koma setelah angka bukan nol penting. Jadi %s memiliki %d angka penting." % (x, n))
    if k == "kali":
        a, b, res, n = R.choice([("2,5", "3,2", "8,0", 2), ("4,0", "1,25", "5,0", 2), ("12,5", "2,0", "25", 2), ("3,14", "2,0", "6,3", 2), ("1,50", "2,00", "3,00", 3), ("6,0", "0,50", "3,0", 2)])
        wr = {"8,0": ["8", "8,00", "8,000"], "5,0": ["5", "5,00", "5,000"], "25": ["25,0", "25,00", "2,5"], "6,3": ["6,28", "6", "6,280"], "3,00": ["3", "3,0", "3,000"], "3,0": ["3", "3,00", "0,30"]}[res]
        return it("Panjang %s m dan lebar %s m. Berapa luasnya menurut aturan angka penting?" % (a, b), res + " m²", [w + " m²" for w in wr],
                  "Hasil perkalian mengikuti angka penting paling sedikit (%d angka penting), jadi %s m²." % (n, res))
    x, d, res = R.choice([("3,456", 2, "3,5"), ("12,349", 3, "12,3"), ("0,0675", 2, "0,068"), ("8,951", 2, "9,0"), ("2,345", 3, "2,35"), ("149,6", 2, "150")])
    wr = sorted({"3,5": ["3,4", "3,46", "3"], "12,3": ["12,35", "12", "12,4"], "0,068": ["0,067", "0,07", "0,0675"], "9,0": ["8,9", "8,95", "9"], "2,35": ["2,34", "2,3", "2,4"], "150": ["149", "140", "1,5"]}[res])
    return it("Bulatkan %s menjadi %d angka penting." % (x, d), res, wr, "%s dibulatkan menjadi %d angka penting adalah %s." % (x, d, res))


def f_hukum(R):
    k = R.choice(["lav", "proust", "proust2"])
    if k == "lav":
        names, ra, rb = R.choice([(("besi", "belerang", "besi(II) sulfida"), 7, 4), (("magnesium", "oksigen", "magnesium oksida"), 3, 2), (("karbon", "oksigen", "karbon dioksida"), 3, 8), (("hidrogen", "oksigen", "air"), 1, 8)])
        f = R.choice([0.4, 0.8, 1.2, 2, 3, 4])
        a, b = ra * f, rb * f
        return nq("Sebanyak %s g %s tepat bereaksi dengan %s g %s dalam wadah tertutup membentuk %s. Berapa massa %s yang terbentuk?" % (num(a), names[0], num(b), names[1], names[2], names[2]), a + b,
                  [a - b if a > b else b - a, a * b, (a + b) / 2], "g", "Hukum Lavoisier: massa hasil = %s + %s = %s g." % (num(a), num(b), num(a + b)))
    if k == "proust":
        r = R.choice([("air", "hidrogen", "oksigen", 1, 8), ("karbon dioksida", "karbon", "oksigen", 3, 8), ("besi(II) sulfida", "besi", "belerang", 7, 4), ("magnesium oksida", "magnesium", "oksigen", 3, 2)])
        m = R.choice([2, 3, 4, 5, 6])
        x = r[3] * m
        y = r[4] * m
        return nq("Perbandingan massa %s : %s dalam %s adalah %d : %d. Berapa gram %s yang diperlukan untuk bereaksi tepat dengan %d g %s?" % (r[1], r[2], r[0], r[3], r[4], r[2], x, r[1]), y,
                  [x * r[3] / r[4], x + r[4], x * r[3]], "g", "Hukum Proust: %d g × %d/%d = %d g %s." % (x, r[4], r[3], y, r[2]))
    r = R.choice([("air", "hidrogen", "oksigen", 1, 8), ("karbon dioksida", "karbon", "oksigen", 3, 8), ("magnesium oksida", "magnesium", "oksigen", 3, 2)])
    m = R.choice([2, 3, 4, 5])
    tot = (r[3] + r[4]) * m
    return nq("Perbandingan massa %s : %s dalam %s adalah %d : %d. Berapa gram %s yang terbentuk dari %d g %s yang bereaksi sempurna?" % (r[1], r[2], r[0], r[3], r[4], r[0], r[3] * m, r[1]), tot,
              [r[4] * m, r[3] * m, tot * 2], "g", "Oksigen yang diperlukan %d g, jadi massa %s = %d + %d = %d g." % (r[4] * m, r[0], r[3] * m, r[4] * m, tot))


def f_efisiensi(R):
    k = R.choice(["eff", "out", "P"])
    if k == "eff":
        i = R.choice([200, 400, 500, 800, 1000])
        p = R.choice([0.2, 0.25, 0.4, 0.5, 0.8, 0.9])
        o = i * p
        return nq("Sebuah alat menerima energi %d J dan menghasilkan energi berguna %s J. Berapa efisiensinya?" % (i, num(o)), p * 100, [i / o * 100, (1 - p) * 100, o], "%",
                  "Efisiensi = energi keluaran ÷ energi masukan × 100%% = %s ÷ %d × 100%% = %s%%." % (num(o), i, num(p * 100)))
    if k == "out":
        i = R.choice([1000, 2000, 5000])
        p = R.choice([20, 25, 40])
        return nq("Panel surya menerima energi cahaya %s J dengan efisiensi %d%%. Berapa energi listrik yang dihasilkan?" % (num(i), p), i * p / 100, [i - p, i * (100 - p) / 100, i / p], "J",
                  "Energi listrik = %d%% × %s J = %s J." % (p, num(i), num(i * p / 100)))
    P = R.choice([50, 100, 200, 500])
    t = R.choice([60, 120, 300, 600])
    return nq("Pompa air %d W bekerja selama %d s. Berapa energi listrik yang dipakai?" % (P, t), P * t, [P / t, P + t, P * t / 60], "J", "W = P × t = %d × %d = %s J." % (P, t, num(P * t)))


def UNITS(g):
    return [
        H("X", "besaran-satuan-dan-dimensi", "Besaran, Satuan, dan Dimensi", "Besaran dan Satuan",
          "Peserta didik menjelaskan sistem pengukuran dalam kerja ilmiah: alat ukur, besaran pokok dan turunan, satuan SI, dimensi, serta konversi satuan.",
          "alat ukur (jangka sorong, mikrometer sekrup, neraca), tujuh besaran pokok, besaran turunan, satuan SI, dimensi, awalan satuan",
          "Setiap besaran memiliki satuan dan dimensi", "Tujuh besaran pokok menjadi dasar semua besaran lain. Dimensi menunjukkan susunan besaran pokok dalam suatu besaran.",
          ["Besaran pokok dalam SI ada tujuh: panjang (m, [L]), massa (kg, [M]), waktu (s, [T]), kuat arus (A, [I]), suhu (K, [θ]), jumlah zat (mol, [N]), dan intensitas cahaya (cd, [J]).",
           "Besaran turunan disusun dari besaran pokok. Contoh: kecepatan m/s berdimensi [L][T]⁻¹, percepatan [L][T]⁻², gaya (newton = kg·m/s²) berdimensi [M][L][T]⁻².",
           "Awalan satuan memudahkan penulisan: kilo (10³), mega (10⁶), mili (10⁻³), mikro (10⁻⁶), nano (10⁻⁹). Jangka sorong teliti sampai 0,1 mm dan mikrometer sekrup sampai 0,01 mm."],
          [("Tentukan dimensi energi kinetik (½mv²).", ["Massa berdimensi [M].", "v² berdimensi [L]²[T]⁻².", "Angka ½ tidak berdimensi."], "[M][L]²[T]⁻²")],
          [("Gaya termasuk besaran pokok.", "Gaya diturunkan dari massa, panjang, dan waktu."), ("Mikrometer sekrup kurang teliti dibanding penggaris.", "Mikrometer sekrup teliti sampai 0,01 mm, jauh lebih teliti."),
           ("Satuan SI suhu adalah derajat Celsius.", "Satuan SI suhu adalah kelvin.")],
          [("Apa guna analisis dimensi?", "Untuk memeriksa apakah suatu rumus benar dan untuk menurunkan satuan besaran turunan."),
           ("Berapa 1 mikrometer?", "1 μm = 10⁻⁶ m = 0,001 mm."),
           ("Kapan memakai jangka sorong?", "Untuk mengukur diameter luar, diameter dalam, dan kedalaman benda kecil dengan ketelitian 0,1 mm.")],
          [("Dimensi besaran", [("kecepatan", "[L][T]⁻¹"), ("percepatan", "[L][T]⁻²"), ("gaya", "[M][L][T]⁻²"), ("luas", "[L]²"), ("volume", "[L]³"), ("massa jenis", "[M][L]⁻³"),
                               ("usaha atau energi", "[M][L]²[T]⁻²"), ("tekanan", "[M][L]⁻¹[T]⁻²"), ("daya", "[M][L]²[T]⁻³"), ("momentum", "[M][L][T]⁻¹")],
            "Apa dimensi ‘{k}’?", "Besaran apa yang berdimensi ‘{v}’?"),
           ("Alat ukur dan ketelitian", [("mistar", "0,1 cm atau 1 mm"), ("jangka sorong", "0,1 mm"), ("mikrometer sekrup", "0,01 mm"), ("neraca Ohaus tiga lengan", "0,1 g"), ("stopwatch digital", "0,01 s"),
                                        ("termometer laboratorium", "1 °C"), ("gelas ukur 100 mL", "1 mL")],
            "Berapa ketelitian ‘{k}’?", "Alat ukur apa yang ketelitiannya ‘{v}’?"),
           ("Awalan satuan", [("kilo (k)", "10³"), ("mega (M)", "10⁶"), ("giga (G)", "10⁹"), ("hekto (h)", "10²"), ("senti (c)", "10⁻²"), ("mili (m)", "10⁻³"), ("mikro (μ)", "10⁻⁶"), ("nano (n)", "10⁻⁹"), ("piko (p)", "10⁻¹²")],
            "Awalan ‘{k}’ bernilai ...", "Awalan apa yang bernilai ‘{v}’?")],
          ["Ada tujuh besaran pokok dalam SI.", "Satuan SI massa adalah kilogram.", "Gaya adalah besaran turunan.",
           "Dimensi kecepatan adalah [L][T]⁻¹.", "Mikrometer sekrup teliti sampai 0,01 mm.", "Awalan mili bernilai 10⁻³.",
           "Analisis dimensi dapat memeriksa kebenaran rumus.", "Satuan SI suhu adalah kelvin."],
          [("Kecepatan adalah besaran pokok.", "Kecepatan adalah besaran turunan."), ("Dimensi gaya adalah [M][L][T]⁻¹.", "Dimensi gaya adalah [M][L][T]⁻²; [M][L][T]⁻¹ adalah momentum."),
           ("Awalan mikro bernilai 10⁻³.", "Awalan mikro bernilai 10⁻⁶."), ("Jangka sorong teliti sampai 0,01 mm.", "Jangka sorong teliti sampai 0,1 mm."),
           ("Satuan SI waktu adalah jam.", "Satuan SI waktu adalah sekon."), ("Massa jenis berdimensi [M][L]³.", "Massa jenis berdimensi [M][L]⁻³.")],
          "besaran dan satuan", "working-scientifically"),

        H("X", "angka-penting-dan-ketidakpastian", "Angka Penting dan Ketidakpastian Pengukuran", "Angka Penting",
          "Peserta didik menerapkan aturan angka penting dalam penulisan dan perhitungan hasil pengukuran, membulatkan hasil, serta menentukan ketidakpastian pada pengukuran tunggal dan berulang.",
          "aturan angka penting, notasi ilmiah, pembulatan, operasi angka penting, ketidakpastian, akurasi dan presisi",
          "Hasil hitung ikut angka penting paling sedikit", "Angka penting menunjukkan ketelitian pengukuran. Hasil perkalian tidak boleh lebih teliti daripada data paling kasar.",
          ["Angka penting adalah semua angka hasil pengukuran, termasuk angka taksiran terakhir. Semua angka bukan nol penting; nol di antara angka bukan nol penting; nol di depan tidak penting; nol di belakang angka desimal penting.",
           "Hasil penjumlahan dan pengurangan mengikuti angka taksiran (desimal) paling sedikit. Hasil perkalian dan pembagian mengikuti jumlah angka penting paling sedikit.",
           "Setiap pengukuran memiliki ketidakpastian. Pada pengukuran tunggal, ketidakpastian setengah skala terkecil. Akurasi berarti dekat dengan nilai sebenarnya, presisi berarti hasil berulang saling dekat."],
          [("Tulis 0,000560 dalam notasi ilmiah dan tentukan angka pentingnya.", ["0,000560 = 5,60 × 10⁻⁴.", "Angka 5, 6, dan nol di belakang penting."], "5,60 × 10⁻⁴, tiga angka penting")],
          [("Semua angka nol tidak penting.", "Nol di antara angka bukan nol dan nol di belakang desimal termasuk penting."), ("Hasil kali harus ditulis dengan semua digit kalkulator.", "Hasil kali dibulatkan sesuai angka penting paling sedikit."),
           ("Akurasi dan presisi sama artinya.", "Akurasi dekat nilai sebenarnya; presisi berarti hasil berulang konsisten.")],
          [("Mengapa notasi ilmiah berguna?", "Memudahkan menulis angka sangat besar atau kecil dan memperjelas jumlah angka penting, misalnya 1,20 × 10³."),
           ("Apa itu kesalahan sistematis?", "Kesalahan yang selalu ke arah sama, misalnya alat yang tidak dikalibrasi atau titik nol yang bergeser."),
           ("Bagaimana mengurangi kesalahan acak?", "Dengan melakukan pengukuran berulang dan mengambil nilai rata-ratanya.")],
          [("Jumlah angka penting", [("4,52 kg", "3 angka penting"), ("0,0071 m", "2 angka penting"), ("100,5 g", "4 angka penting"), ("2,000 L", "4 angka penting"), ("0,30 s", "2 angka penting"),
                                    ("6,02 × 10²³", "3 angka penting"), ("7,0 × 10⁻³ m", "2 angka penting"), ("305 cm", "3 angka penting"), ("0,004060 kg", "4 angka penting")],
            "Berapa jumlah angka penting pada ‘{k}’?", None, ("1 angka penting", "5 angka penting")),
           ("Akurasi dan presisi", [("hasil berulang 9,8; 9,8; 9,9 dengan nilai sebenarnya 9,8", "akurat dan presisi"), ("hasil berulang 7,2; 7,2; 7,3 dengan nilai sebenarnya 9,8", "presisi tetapi tidak akurat"),
                                   ("hasil berulang 8,1; 11,3; 9,9 dengan rata-rata 9,8", "akurat tetapi tidak presisi"), ("hasil berulang 5,0; 12,4; 7,7 dengan nilai sebenarnya 9,8", "tidak akurat dan tidak presisi"),
                                   ("timbangan selalu menunjukkan 0,2 kg lebih berat", "kesalahan sistematis"), ("pembacaan berbeda-beda karena getaran meja", "kesalahan acak"), ("salah membaca skala karena posisi mata miring", "kesalahan paralaks")],
            "Data atau keadaan ‘{k}’ menunjukkan ...", None),
           ("Istilah pengukuran", [("angka penting", "angka hasil pengukuran termasuk angka taksiran"), ("angka taksiran", "angka terakhir yang diperkirakan"), ("notasi ilmiah", "penulisan a × 10ⁿ dengan 1 ≤ a < 10"),
                                  ("ketidakpastian", "rentang ragu-ragu dari hasil pengukuran"), ("akurasi", "kedekatan hasil dengan nilai sebenarnya"), ("presisi", "kedekatan hasil-hasil pengukuran berulang"),
                                  ("kalibrasi", "mencocokkan alat ukur dengan standar"), ("paralaks", "kesalahan karena posisi mata tidak tegak lurus skala")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Semua angka bukan nol adalah angka penting.", "Nol di depan angka bukan nol tidak penting.", "Hasil perkalian mengikuti angka penting paling sedikit.",
           "Ketidakpastian pengukuran tunggal adalah setengah skala terkecil.", "Pengukuran berulang mengurangi kesalahan acak.", "Presisi berarti hasil berulang saling dekat.",
           "Notasi ilmiah ditulis a × 10ⁿ dengan 1 ≤ a < 10.", "Kesalahan paralaks terjadi karena posisi mata miring."],
          [("0,0071 memiliki empat angka penting.", "0,0071 memiliki dua angka penting."), ("Kesalahan sistematis dihilangkan dengan mengulang pengukuran.", "Kesalahan sistematis diperbaiki dengan kalibrasi alat."),
           ("Hasil penjumlahan mengikuti angka penting terbanyak.", "Hasil penjumlahan mengikuti desimal paling sedikit."), ("Presisi berarti dekat dengan nilai sebenarnya.", "Itu akurasi."),
           ("Nol di belakang koma desimal tidak pernah penting.", "Nol di belakang angka desimal termasuk penting."), ("Notasi ilmiah boleh memakai a = 12.", "Nilai a harus 1 ≤ a < 10.")],
          "angka penting", "working-scientifically", calc=f_angka),

        H("L", "virus-dan-peranannya", "Virus dan Peranannya", "Virus",
          "Peserta didik menjelaskan ciri dan struktur virus, cara virus bereproduksi (daur litik dan lisogenik), peranan virus yang merugikan dan menguntungkan, serta cara mencegah penyebaran virus.",
          "ciri virus, kapsid, asam nukleat, daur litik dan lisogenik, penyakit karena virus, vaksin, pencegahan",
          "Virus hanya berkembang biak di sel hidup", "Virus tersusun atas asam nukleat dan selubung protein. Virus memakai sel inang untuk memperbanyak diri.",
          ["Virus berukuran sangat kecil (20–300 nm) dan hanya terlihat dengan mikroskop elektron. Virus tidak memiliki sel; tubuhnya terdiri dari asam nukleat (DNA atau RNA) yang diselubungi kapsid protein.",
           "Virus dapat dikristalkan seperti benda mati, tetapi dapat bereproduksi di dalam sel hidup seperti makhluk hidup. Karena itu virus disebut berada di peralihan benda mati dan makhluk hidup.",
           "Reproduksi virus: daur litik (adsorpsi, injeksi, sintesis, perakitan, lisis yang memecah sel) dan daur lisogenik (DNA virus bergabung dengan DNA inang dan ikut membelah). Vaksin mencegah penyakit akibat virus."],
          [("Mengapa antibiotik tidak dapat menyembuhkan flu?", ["Flu disebabkan oleh virus.", "Antibiotik hanya bekerja pada bakteri."], "karena flu disebabkan virus, bukan bakteri")],
          [("Virus adalah bakteri yang sangat kecil.", "Virus tidak bersel, sedangkan bakteri adalah sel prokariotik."), ("Virus dapat berkembang biak di luar sel hidup.", "Virus hanya bereproduksi di dalam sel inang."),
           ("Semua virus merugikan.", "Virus juga dimanfaatkan untuk membuat vaksin dan terapi gen.")],
          [("Apa beda daur litik dan lisogenik?", "Pada daur litik sel inang segera pecah. Pada daur lisogenik DNA virus menyatu dengan DNA inang dan baru aktif kemudian."),
           ("Apa itu bakteriofag?", "Virus yang menyerang bakteri, misalnya virus T4 yang menginfeksi Escherichia coli."),
           ("Bagaimana mencegah penyebaran virus?", "Mencuci tangan dengan sabun, memakai masker saat sakit, vaksinasi, dan menjaga daya tahan tubuh.")],
          [("Penyakit karena virus", [("influenza", "manusia"), ("campak", "manusia"), ("COVID-19", "manusia"), ("AIDS", "manusia"), ("demam berdarah dengue", "manusia"), ("hepatitis B", "manusia"),
                                     ("flu burung", "unggas"), ("penyakit mulut dan kuku", "sapi dan kambing"), ("rabies", "anjing dan manusia"), ("mosaik tembakau", "tumbuhan tembakau"), ("tungro", "tanaman padi")],
            "Penyakit ‘{k}’ menyerang ...", "Penyakit virus manakah yang menyerang ‘{v}’?"),
           ("Tahap daur litik", [("adsorpsi", "virus menempel pada dinding sel inang"), ("injeksi", "virus memasukkan asam nukleatnya ke sel inang"), ("sintesis", "sel inang membuat bagian-bagian virus baru"),
                                ("perakitan", "bagian-bagian virus disusun menjadi virus utuh"), ("lisis", "sel inang pecah dan virus baru keluar"), ("penggabungan (lisogenik)", "DNA virus bergabung dengan DNA sel inang")],
            "Apa yang terjadi pada tahap ‘{k}’?", "Tahap apa yang ditandai dengan ‘{v}’?"),
           ("Struktur dan istilah virus", [("kapsid", "selubung protein yang melindungi asam nukleat"), ("asam nukleat", "materi genetik virus berupa DNA atau RNA"), ("kapsomer", "subunit protein penyusun kapsid"),
                                          ("serabut ekor", "bagian bakteriofag untuk menempel pada sel inang"), ("sel inang", "sel hidup tempat virus memperbanyak diri"), ("vaksin", "bahan yang merangsang tubuh membentuk antibodi"),
                                          ("virion", "partikel virus utuh di luar sel"), ("bakteriofag", "virus yang menyerang bakteri")],
            "Apa yang dimaksud ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Virus tidak memiliki sel.", "Virus hanya bereproduksi di dalam sel hidup.", "Asam nukleat virus berupa DNA atau RNA.",
           "Kapsid adalah selubung protein virus.", "Pada daur litik sel inang pecah.", "Antibiotik tidak efektif melawan virus.",
           "Vaksin membantu tubuh membentuk kekebalan.", "Bakteriofag adalah virus yang menyerang bakteri."],
          [("Virus dapat dilihat dengan mikroskop cahaya biasa.", "Virus hanya terlihat dengan mikroskop elektron."), ("Antibiotik dapat membunuh virus influenza.", "Antibiotik bekerja pada bakteri, bukan virus."),
           ("Virus memiliki inti sel dan sitoplasma.", "Virus tidak bersel."), ("Pada daur lisogenik sel inang langsung pecah.", "Pada daur lisogenik DNA virus menyatu dengan DNA inang."),
           ("Tungro adalah penyakit pada sapi.", "Tungro menyerang tanaman padi."), ("Kapsid tersusun atas lemak.", "Kapsid tersusun atas protein.")],
          "virus", "living-things-and-ecosystems"),

        H("M", "struktur-atom", "Struktur Atom", "Struktur Atom",
          "Peserta didik menjelaskan perkembangan model atom (Dalton, Thomson, Rutherford, Bohr), partikel subatom, nomor atom dan nomor massa, isotop, isobar, isoton, serta konfigurasi elektron.",
          "model atom Dalton, Thomson, Rutherford, Bohr, proton, neutron, elektron, nomor atom dan massa, isotop, ion, konfigurasi elektron, elektron valensi",
          "Nomor atom = jumlah proton", "Inti atom berisi proton dan neutron, elektron mengelilingi inti pada kulit-kulit tertentu.",
          ["Model atom berkembang: Dalton (bola pejal), Thomson (roti kismis, muatan positif dengan elektron tersebar), Rutherford (inti kecil bermuatan positif dikelilingi elektron), Bohr (elektron pada lintasan berenergi tertentu).",
           "Atom terdiri dari proton (+), neutron (netral) di inti, dan elektron (−) di kulit. Nomor atom (Z) = jumlah proton. Nomor massa (A) = proton + neutron. Atom netral: elektron = proton.",
           "Isotop adalah atom unsur sama dengan nomor massa berbeda (C-12 dan C-14). Kulit K maksimal 2 elektron, L maksimal 8, M (sampai kalsium) diisi 8 lalu N. Elektron pada kulit terluar disebut elektron valensi."],
          [("Atom natrium bernomor atom 11 dan nomor massa 23. Berapa proton, elektron, dan neutronnya?", ["Proton = 11.", "Elektron atom netral = 11.", "Neutron = 23 − 11 = 12."], "11 proton, 11 elektron, 12 neutron")],
          [("Nomor massa sama dengan jumlah elektron.", "Nomor massa = jumlah proton + neutron."), ("Isotop memiliki jumlah proton berbeda.", "Isotop memiliki proton sama tetapi neutron berbeda."),
           ("Model Dalton sudah menjelaskan elektron.", "Elektron baru dijelaskan pada model Thomson.")],
          [("Apa yang ditemukan Rutherford?", "Dari percobaan hamburan sinar alfa pada lempeng emas, ia menemukan bahwa atom sebagian besar ruang kosong dengan inti kecil bermuatan positif."),
           ("Apa itu ion?", "Atom yang kehilangan elektron menjadi ion positif (kation), yang menerima elektron menjadi ion negatif (anion)."),
           ("Apa manfaat isotop C-14?", "Untuk menentukan umur fosil dan benda purba (penanggalan karbon).")],
          [("Model atom", [("atom adalah bola pejal yang tidak dapat dibagi", "Dalton"), ("atom seperti roti kismis dengan elektron tersebar", "Thomson"), ("atom memiliki inti kecil bermuatan positif", "Rutherford"),
                          ("elektron beredar pada lintasan dengan tingkat energi tertentu", "Bohr"), ("sebagian besar atom adalah ruang kosong", "Rutherford"), ("elektron ditemukan melalui sinar katode", "Thomson"),
                          ("atom unsur yang sama memiliki sifat sama", "Dalton"), ("elektron berpindah kulit dengan menyerap atau melepas energi", "Bohr")],
            "Gagasan ‘{k}’ dikemukakan oleh ...", "Manakah gagasan model atom ‘{v}’?", ("Mendel",)),
           ("Isotop, isobar, isoton", [("¹²C dan ¹⁴C", "isotop"), ("¹H dan ²H", "isotop"), ("³⁵Cl dan ³⁷Cl", "isotop"), ("¹⁴C dan ¹⁴N", "isobar"), ("⁴⁰Ar dan ⁴⁰Ca", "isobar"),
                                      ("¹³C dan ¹⁴N", "isoton"), ("³⁹K dan ⁴⁰Ca", "isoton"), ("²³Na dan ²⁴Mg", "isoton")],
            "Pasangan ‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("isomer", "isoelektron")),
           ("Partikel subatom", [("proton", "bermuatan positif dan berada di inti"), ("neutron", "tidak bermuatan dan berada di inti"), ("elektron", "bermuatan negatif dan mengelilingi inti"),
                                ("nomor atom", "jumlah proton dalam inti"), ("nomor massa", "jumlah proton dan neutron"), ("elektron valensi", "elektron pada kulit terluar"), ("kation", "ion bermuatan positif"), ("anion", "ion bermuatan negatif")],
            "Apa yang dimaksud ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Nomor atom menunjukkan jumlah proton.", "Nomor massa adalah jumlah proton dan neutron.", "Atom netral memiliki elektron sama dengan proton.",
           "Isotop memiliki jumlah proton yang sama.", "Rutherford menemukan inti atom.", "Bohr menyatakan elektron berada pada tingkat energi tertentu.",
           "Kulit K maksimal berisi 2 elektron.", "Kation terbentuk saat atom melepas elektron."],
          [("Neutron bermuatan negatif.", "Neutron tidak bermuatan."), ("Isobar memiliki nomor atom sama.", "Isobar memiliki nomor massa sama."), ("Kulit L maksimal berisi 18 elektron.", "Kulit L maksimal berisi 8 elektron."),
           ("Model atom roti kismis dikemukakan Bohr.", "Model roti kismis dikemukakan Thomson."), ("Anion terbentuk saat atom melepas elektron.", "Anion terbentuk saat atom menerima elektron."),
           ("Elektron berada di dalam inti atom.", "Elektron mengelilingi inti atom.")],
          "struktur atom", "matter", calc=f_atom),

        H("M", "sistem-periodik-unsur", "Sistem Periodik Unsur", "Sistem Periodik",
          "Peserta didik menjelaskan perkembangan sistem periodik, susunan golongan dan periode, letak unsur berdasarkan konfigurasi elektron, serta sifat keperiodikan unsur.",
          "triade Dobereiner, oktaf Newlands, Mendeleyev, sistem periodik modern, golongan dan periode, logam dan nonlogam, jari-jari atom, energi ionisasi, keelektronegatifan",
          "Unsur disusun menurut kenaikan nomor atom", "Golongan ditentukan elektron valensi, periode ditentukan jumlah kulit. Sifat unsur berulang secara periodik.",
          ["Sistem periodik modern menyusun unsur menurut kenaikan nomor atom. Lajur tegak disebut golongan (unsur dengan elektron valensi sama, sifat mirip), lajur mendatar disebut periode (jumlah kulit sama).",
           "Golongan IA alkali, IIA alkali tanah, VIIA halogen, dan VIIIA gas mulia yang stabil. Unsur logam berada di kiri, nonlogam di kanan, dan metaloid di antaranya.",
           "Dalam satu golongan dari atas ke bawah, jari-jari atom bertambah, sedangkan energi ionisasi dan keelektronegatifan berkurang. Dalam satu periode dari kiri ke kanan, jari-jari berkurang dan keelektronegatifan bertambah."],
          [("Unsur X memiliki konfigurasi 2 8 7. Di golongan dan periode berapa X berada?", ["Elektron valensi 7, jadi golongan VIIA.", "Tiga kulit, jadi periode 3."], "golongan VIIA, periode 3 (klorin)")],
          [("Unsur dalam satu periode memiliki sifat yang mirip.", "Unsur dalam satu golongan yang sifatnya mirip."), ("Jari-jari atom berkurang dari atas ke bawah dalam satu golongan.", "Jari-jari atom bertambah dari atas ke bawah."),
           ("Gas mulia mudah bereaksi.", "Gas mulia stabil karena kulit terluarnya penuh.")],
          [("Siapa Mendeleyev?", "Ilmuwan Rusia yang menyusun unsur berdasarkan massa atom dan menyisakan tempat kosong untuk unsur yang belum ditemukan."),
           ("Mengapa natrium sangat reaktif?", "Natrium memiliki satu elektron valensi yang mudah dilepas sehingga cepat bereaksi."),
           ("Apa itu keelektronegatifan?", "Kemampuan atom menarik elektron dalam ikatan; fluorin memiliki keelektronegatifan terbesar.")],
          [("Nama golongan", [("golongan IA", "alkali"), ("golongan IIA", "alkali tanah"), ("golongan IIIA", "boron"), ("golongan IVA", "karbon"), ("golongan VA", "nitrogen"), ("golongan VIA", "oksigen (kalkogen)"),
                             ("golongan VIIA", "halogen"), ("golongan VIIIA", "gas mulia")],
            "‘{k}’ disebut golongan ...", "Golongan berapa yang disebut ‘{v}’?"),
           ("Perkembangan sistem periodik", [("unsur dikelompokkan bertiga dengan massa tengah rata-rata dua lainnya", "Dobereiner"), ("sifat unsur berulang setiap unsur kedelapan", "Newlands"),
                                             ("disusun berdasarkan massa atom dengan tempat kosong untuk unsur baru", "Mendeleyev"), ("disusun berdasarkan kenaikan nomor atom", "Moseley (sistem periodik modern)"),
                                             ("hukum oktaf", "Newlands"), ("hukum triade", "Dobereiner")],
            "‘{k}’ dikemukakan oleh ...", "Gagasan apa yang dikemukakan ‘{v}’?", ("Lavoisier",)),
           ("Sifat keperiodikan", [("jari-jari atom dari atas ke bawah dalam satu golongan", "bertambah"), ("jari-jari atom dari kiri ke kanan dalam satu periode", "berkurang"),
                                  ("energi ionisasi dari atas ke bawah dalam satu golongan", "berkurang"), ("energi ionisasi dari kiri ke kanan dalam satu periode", "cenderung bertambah"),
                                  ("keelektronegatifan dari atas ke bawah dalam satu golongan", "berkurang"), ("keelektronegatifan dari kiri ke kanan dalam satu periode", "bertambah"),
                                  ("sifat logam dari atas ke bawah dalam satu golongan", "bertambah"), ("sifat logam dari kiri ke kanan dalam satu periode", "berkurang")],
            "Bagaimana kecenderungan ‘{k}’?", None, ("tetap sama", "berubah acak"))],
          ["Sistem periodik modern disusun menurut nomor atom.", "Unsur segolongan memiliki elektron valensi yang sama.", "Unsur seperiode memiliki jumlah kulit yang sama.",
           "Golongan VIIA disebut halogen.", "Gas mulia bersifat stabil.", "Jari-jari atom bertambah dari atas ke bawah dalam satu golongan.",
           "Fluorin memiliki keelektronegatifan terbesar.", "Logam terletak di bagian kiri sistem periodik."],
          [("Golongan IA disebut halogen.", "Golongan IA disebut alkali; halogen adalah VIIA."), ("Mendeleyev menyusun unsur menurut nomor atom.", "Mendeleyev menyusun menurut massa atom."),
           ("Energi ionisasi bertambah dari atas ke bawah.", "Energi ionisasi berkurang dari atas ke bawah."), ("Unsur seperiode memiliki elektron valensi sama.", "Unsur segolongan yang memiliki elektron valensi sama."),
           ("Nonlogam berada di bagian kiri sistem periodik.", "Nonlogam berada di bagian kanan."), ("Hukum oktaf dikemukakan Dobereiner.", "Hukum oktaf dikemukakan Newlands.")],
          "sistem periodik unsur", "matter", calc=f_atom),

        H("M", "hukum-dasar-kimia", "Hukum Dasar Kimia di Sekitar Kita", "Hukum Dasar Kimia",
          "Peserta didik menjelaskan ciri, jenis, dan cara menuliskan reaksi kimia, serta menerapkan hukum Lavoisier, Proust, Dalton, dan Gay-Lussac dalam perhitungan sederhana dan kehidupan sehari-hari.",
          "ciri reaksi kimia, persamaan reaksi, hukum kekekalan massa (Lavoisier), perbandingan tetap (Proust), perbandingan berganda (Dalton), perbandingan volume (Gay-Lussac)",
          "Massa zat sebelum dan sesudah reaksi sama", "Unsur dalam senyawa selalu bergabung dengan perbandingan massa tetap. Perbandingan volume gas sama dengan perbandingan koefisien.",
          ["Hukum Lavoisier: dalam sistem tertutup, massa zat sebelum dan sesudah reaksi sama. Hukum Proust: perbandingan massa unsur dalam suatu senyawa selalu tetap, misalnya H : O dalam air = 1 : 8.",
           "Hukum Dalton (perbandingan berganda): jika dua unsur membentuk lebih dari satu senyawa, perbandingan massa unsur yang satu dengan massa tetap unsur lain merupakan bilangan bulat sederhana, misalnya CO dan CO₂.",
           "Hukum Gay-Lussac: pada suhu dan tekanan sama, perbandingan volume gas-gas yang bereaksi dan hasil reaksi sama dengan perbandingan koefisiennya. Contoh: 2H₂ + O₂ → 2H₂O, volume 2 : 1 : 2."],
          [("Pada suhu dan tekanan sama, 10 L gas hidrogen bereaksi dengan gas nitrogen membentuk amonia: N₂ + 3H₂ → 2NH₃. Berapa liter amonia yang terbentuk?", ["Perbandingan volume H₂ : NH₃ = 3 : 2.", "10 × 2/3 = 6,67 L."], "6,67 L")],
          [("Massa berkurang saat kertas dibakar, jadi hukum Lavoisier tidak berlaku.", "Massa gas hasil pembakaran ikut dihitung dalam sistem tertutup."), ("Perbandingan massa unsur dalam air dapat berubah-ubah.", "Perbandingan H : O dalam air selalu 1 : 8."),
           ("Hukum Gay-Lussac berlaku untuk zat padat.", "Hukum Gay-Lussac berlaku untuk gas pada suhu dan tekanan sama.")],
          [("Apa contoh hukum Dalton?", "Karbon dan oksigen membentuk CO dan CO₂. Untuk massa karbon tetap, perbandingan massa oksigen dalam CO dan CO₂ adalah 1 : 2."),
           ("Mengapa hukum dasar kimia penting dalam industri?", "Untuk menghitung bahan baku agar reaksi efisien dan tidak ada bahan yang terbuang."),
           ("Apa ciri reaksi kimia?", "Terbentuk gas, endapan, perubahan warna, perubahan suhu, atau timbul bau.")],
          [("Hukum dasar kimia", [("massa sebelum dan sesudah reaksi sama dalam sistem tertutup", "hukum Lavoisier"), ("perbandingan massa unsur dalam senyawa selalu tetap", "hukum Proust"),
                                  ("perbandingan massa oksigen dalam CO dan CO₂ adalah 1 : 2", "hukum Dalton"), ("perbandingan volume gas sama dengan perbandingan koefisien", "hukum Gay-Lussac"),
                                  ("gas bervolume sama pada suhu dan tekanan sama mengandung jumlah molekul sama", "hipotesis Avogadro"), ("perbandingan H : O dalam air selalu 1 : 8", "hukum Proust"),
                                  ("12 g karbon dan 32 g oksigen menghasilkan 44 g karbon dioksida", "hukum Lavoisier")],
            "Pernyataan ‘{k}’ sesuai dengan ...", "Manakah pernyataan yang sesuai dengan ‘{v}’?"),
           ("Perbandingan volume gas", [("2H₂ + O₂ → 2H₂O (volume H₂ : O₂ : H₂O)", "2 : 1 : 2"), ("N₂ + 3H₂ → 2NH₃ (volume N₂ : H₂ : NH₃)", "1 : 3 : 2"), ("H₂ + Cl₂ → 2HCl (volume H₂ : Cl₂ : HCl)", "1 : 1 : 2"),
                                       ("CH₄ + 2O₂ → CO₂ + 2H₂O (volume CH₄ : O₂)", "1 : 2"), ("2CO + O₂ → 2CO₂ (volume CO : O₂ : CO₂)", "2 : 1 : 2"), ("N₂ + O₂ → 2NO (volume N₂ : O₂ : NO)", "1 : 1 : 2")],
            "Berapa perbandingan volume pada reaksi ‘{k}’?", None, ("3 : 1 : 2", "1 : 2 : 1")),
           ("Ciri reaksi", [("pita magnesium dibakar menghasilkan cahaya terang dan abu putih", "perubahan warna dan timbul cahaya"), ("larutan perak nitrat dicampur garam dapur menjadi keruh putih", "terbentuk endapan"),
                           ("pualam dimasukkan ke larutan HCl berbuih", "terbentuk gas"), ("larutan NaOH dicampur HCl terasa hangat", "perubahan suhu"), ("telur busuk mengeluarkan bau", "timbul bau"),
                           ("paku besi berubah kecokelatan", "perubahan warna")],
            "Ciri reaksi apa yang ditunjukkan ‘{k}’?", None, ("perubahan wujud tanpa zat baru",))],
          ["Hukum Lavoisier menyatakan massa sebelum dan sesudah reaksi sama.", "Hukum Proust menyatakan perbandingan massa unsur dalam senyawa tetap.", "Perbandingan massa H : O dalam air adalah 1 : 8.",
           "Hukum Gay-Lussac berlaku untuk gas.", "Perbandingan volume gas sama dengan perbandingan koefisien reaksi.", "CO dan CO₂ adalah contoh hukum Dalton.",
           "Terbentuknya endapan dapat menandai reaksi kimia.", "Hukum dasar kimia dipakai untuk menghitung bahan baku industri."],
          [("Hukum Proust menyatakan massa sebelum dan sesudah reaksi sama.", "Itu hukum Lavoisier; Proust tentang perbandingan tetap."), ("Perbandingan H : O dalam air adalah 2 : 1 menurut massa.", "Menurut massa 1 : 8; 2 : 1 adalah perbandingan jumlah atom."),
           ("Hukum Gay-Lussac berlaku untuk zat cair.", "Hukum Gay-Lussac berlaku untuk gas."), ("Pada reaksi N₂ + 3H₂ → 2NH₃ volume N₂ : NH₃ = 1 : 3.", "Volume N₂ : NH₃ = 1 : 2."),
           ("Massa zat dapat hilang dalam sistem tertutup.", "Massa tetap dalam sistem tertutup."), ("Hukum Dalton membahas perbandingan volume gas.", "Perbandingan volume gas adalah hukum Gay-Lussac.")],
          "hukum dasar kimia", "matter", calc=f_hukum),

        H("X", "kimia-hijau", "Kimia Hijau dalam Pembangunan Berkelanjutan", "Kimia Hijau",
          "Peserta didik menjelaskan pengertian dan pentingnya kimia hijau, dua belas prinsip kimia hijau, proses kimia sehari-hari yang tidak sesuai prinsip kimia hijau, serta kegiatan yang mendukungnya.",
          "kimia hijau, 12 prinsip kimia hijau, pencegahan limbah, ekonomi atom, bahan aman, energi efisien, bahan terbarukan, pembangunan berkelanjutan",
          "Lebih baik mencegah limbah daripada mengolahnya", "Kimia hijau merancang produk dan proses yang mengurangi zat berbahaya sejak awal.",
          ["Kimia hijau adalah rancangan produk dan proses kimia yang mengurangi atau menghilangkan penggunaan dan pembentukan zat berbahaya. Gagasan ini dirumuskan oleh Paul Anastas dan John Warner dalam 12 prinsip.",
           "Beberapa prinsip penting: mencegah limbah, memaksimalkan ekonomi atom, memakai pelarut dan bahan yang lebih aman, efisiensi energi, memakai bahan baku terbarukan, katalis, dan produk yang mudah terurai.",
           "Contoh penerapan: plastik biodegradabel dari pati, deterjen ramah lingkungan, pupuk organik, pestisida nabati, dan mengganti pelarut berbahaya dengan air. Kimia hijau mendukung Tujuan Pembangunan Berkelanjutan 2030."],
          [("Pabrik mengganti pelarut benzena yang beracun dengan air. Prinsip kimia hijau apa yang diterapkan?", ["Benzena berbahaya bagi kesehatan.", "Air adalah pelarut yang lebih aman."], "memakai pelarut yang lebih aman")],
          [("Kimia hijau berarti hanya memakai bahan berwarna hijau.", "Kimia hijau adalah rancangan proses kimia yang ramah lingkungan."), ("Mengolah limbah lebih baik daripada mencegahnya.", "Prinsip pertama kimia hijau adalah mencegah limbah."),
           ("Plastik biodegradabel sulit terurai.", "Plastik biodegradabel dirancang agar mudah terurai.")],
          [("Apa itu ekonomi atom?", "Ukuran seberapa banyak atom pereaksi menjadi produk yang diinginkan. Makin tinggi ekonomi atom, makin sedikit limbah."),
           ("Apa contoh kegiatan sehari-hari yang tidak sesuai kimia hijau?", "Membakar sampah plastik, memakai pestisida berlebihan, dan membuang limbah deterjen langsung ke sungai."),
           ("Apa itu pestisida nabati?", "Pestisida dari tumbuhan seperti daun mimba dan serai yang lebih mudah terurai daripada pestisida sintetis.")],
          [("Prinsip kimia hijau", [("merancang proses agar tidak menghasilkan limbah", "pencegahan limbah"), ("sebanyak mungkin atom pereaksi menjadi produk", "ekonomi atom"), ("mengganti pelarut beracun dengan air", "pelarut dan bahan pembantu yang lebih aman"),
                                   ("reaksi dilakukan pada suhu dan tekanan ruang", "efisiensi energi"), ("memakai minyak nabati sebagai bahan baku", "bahan baku terbarukan"), ("memakai katalis agar reaksi lebih efisien", "katalisis"),
                                   ("membuat plastik yang dapat terurai di tanah", "rancangan produk yang mudah terurai"), ("memantau proses agar tidak terbentuk zat berbahaya", "analisis waktu nyata untuk mencegah polusi"),
                                   ("memilih bahan yang tidak mudah meledak", "kimia yang lebih aman untuk mencegah kecelakaan")],
            "‘{k}’ sesuai dengan prinsip ...", "Manakah penerapan prinsip ‘{v}’?"),
           ("Sesuai atau tidak", {"kegiatan yang sesuai prinsip kimia hijau": ["membuat pupuk kompos dari sampah organik", "memakai pestisida nabati", "memakai kantong belanja kain", "memakai deterjen yang mudah terurai", "mengolah minyak jelantah menjadi biodiesel", "memakai pelarut air dalam praktikum"],
                                 "kegiatan yang tidak sesuai prinsip kimia hijau": ["membakar sampah plastik", "membuang limbah deterjen ke sungai", "memakai pestisida sintetis berlebihan", "memakai styrofoam untuk makanan panas", "membuang oli bekas ke tanah", "memakai pelarut benzena tanpa pengaman"]}),
           ("Istilah keberlanjutan", [("kimia hijau", "rancangan proses kimia yang mengurangi zat berbahaya"), ("pembangunan berkelanjutan", "pembangunan yang memenuhi kebutuhan kini tanpa merugikan generasi mendatang"),
                                     ("biodegradabel", "dapat diuraikan oleh mikroorganisme"), ("ekonomi atom", "persentase atom pereaksi yang menjadi produk"), ("limbah B3", "limbah bahan berbahaya dan beracun"),
                                     ("biodiesel", "bahan bakar dari minyak nabati"), ("SDGs", "Tujuan Pembangunan Berkelanjutan 2030")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Kimia hijau mengurangi pemakaian zat berbahaya.", "Mencegah limbah lebih baik daripada mengolahnya.", "Ekonomi atom yang tinggi menghasilkan sedikit limbah.",
           "Air dapat menjadi pelarut yang lebih aman.", "Plastik biodegradabel dapat terurai di alam.", "Katalis membantu proses kimia lebih efisien.",
           "Pupuk kompos mendukung prinsip kimia hijau.", "Kimia hijau mendukung pembangunan berkelanjutan."],
          [("Membakar sampah plastik sesuai kimia hijau.", "Membakar plastik menghasilkan zat beracun."), ("Kimia hijau tidak memperhatikan energi.", "Efisiensi energi adalah salah satu prinsip kimia hijau."),
           ("Ekonomi atom yang rendah lebih baik.", "Ekonomi atom yang tinggi lebih baik."), ("Bahan baku fosil lebih dianjurkan daripada bahan terbarukan.", "Kimia hijau menganjurkan bahan baku terbarukan."),
           ("Styrofoam mudah terurai di tanah.", "Styrofoam sangat sulit terurai."), ("Limbah B3 aman dibuang ke sungai.", "Limbah B3 harus diolah khusus.")],
          "kimia hijau", "earths-systems"),

        H("L", "keanekaragaman-hayati-dan-klasifikasi", "Keanekaragaman Hayati dan Klasifikasi", "Keanekaragaman Hayati",
          "Peserta didik menjelaskan tingkat keanekaragaman hayati (gen, jenis, ekosistem), keanekaragaman hayati Indonesia (garis Wallace dan Weber), klasifikasi makhluk hidup, serta upaya pelestariannya.",
          "keanekaragaman gen, jenis, ekosistem, flora dan fauna Indonesia, garis Wallace dan Weber, taksonomi, tata nama binomial, konservasi in situ dan ex situ",
          "Tiga tingkat: gen, jenis, dan ekosistem", "Indonesia dibagi menjadi wilayah fauna oriental, peralihan, dan australis oleh garis Wallace dan Weber.",
          ["Keanekaragaman gen adalah variasi dalam satu spesies (mangga arumanis dan manalagi). Keanekaragaman jenis adalah variasi antarspesies (harimau dan kucing). Keanekaragaman ekosistem adalah variasi tempat hidup (hutan, pantai, sawah).",
           "Fauna Indonesia barat (Sumatra, Jawa, Kalimantan, Bali) bertipe oriental, misalnya harimau dan gajah. Fauna timur (Papua) bertipe australis, misalnya kanguru pohon dan cenderawasih. Di antaranya (Sulawesi, Nusa Tenggara, Maluku) fauna peralihan, misalnya anoa dan komodo.",
           "Konservasi in situ dilakukan di habitat asli (taman nasional, cagar alam, suaka margasatwa). Konservasi ex situ dilakukan di luar habitat (kebun raya, kebun binatang, bank benih)."],
          [("Kucing angora, kucing persia, dan kucing kampung menunjukkan keanekaragaman tingkat apa?", ["Ketiganya satu spesies, Felis catus.", "Variasi dalam satu spesies disebut keanekaragaman gen."], "keanekaragaman gen")],
          [("Harimau dan kucing menunjukkan keanekaragaman gen.", "Harimau dan kucing berbeda spesies, jadi keanekaragaman jenis."), ("Komodo termasuk fauna australis.", "Komodo hidup di Nusa Tenggara, wilayah peralihan."),
           ("Kebun raya termasuk konservasi in situ.", "Kebun raya adalah konservasi ex situ.")],
          [("Apa itu garis Wallace?", "Garis khayal yang memisahkan fauna oriental di barat (Kalimantan, Bali) dengan fauna peralihan di timur (Sulawesi, Lombok)."),
           ("Apa itu spesies endemik?", "Spesies yang hanya hidup secara alami di daerah tertentu, misalnya anoa di Sulawesi."),
           ("Apa contoh konservasi ex situ di Indonesia?", "Kebun Raya Bogor, Taman Safari, dan penangkaran jalak bali.")],
          [("Tingkat keanekaragaman", [("mangga arumanis, manalagi, dan golek", "keanekaragaman gen"), ("padi pandanwangi, rojolele, dan IR64", "keanekaragaman gen"), ("ayam kampung, ayam cemani, dan ayam pelung", "keanekaragaman gen"),
                                      ("harimau, singa, dan kucing", "keanekaragaman jenis"), ("kelapa, pinang, dan aren", "keanekaragaman jenis"), ("kacang tanah, kacang hijau, dan kacang merah", "keanekaragaman jenis"),
                                      ("hutan hujan, padang rumput, dan terumbu karang", "keanekaragaman ekosistem"), ("sawah, rawa, dan hutan bakau", "keanekaragaman ekosistem")],
            "‘{k}’ menunjukkan ...", "Manakah contoh ‘{v}’?", ("keanekaragaman individu",)),
           ("Persebaran fauna", [("harimau sumatra", "fauna oriental (Asiatis)"), ("gajah sumatra", "fauna oriental (Asiatis)"), ("badak jawa", "fauna oriental (Asiatis)"), ("orangutan", "fauna oriental (Asiatis)"),
                                ("anoa", "fauna peralihan"), ("babirusa", "fauna peralihan"), ("komodo", "fauna peralihan"), ("burung maleo", "fauna peralihan"),
                                ("kanguru pohon", "fauna australis"), ("cenderawasih", "fauna australis"), ("kasuari", "fauna australis")],
            "‘{k}’ termasuk ...", "Manakah yang termasuk ‘{v}’?", ("fauna eropa",)),
           ("Konservasi", [("Taman Nasional Ujung Kulon", "konservasi in situ"), ("Taman Nasional Komodo", "konservasi in situ"), ("Cagar Alam Lembah Anai", "konservasi in situ"), ("Suaka Margasatwa Way Kambas", "konservasi in situ"),
                          ("Kebun Raya Bogor", "konservasi ex situ"), ("Taman Safari Indonesia", "konservasi ex situ"), ("bank benih", "konservasi ex situ"), ("kebun binatang Ragunan", "konservasi ex situ"),
                          ("penangkaran jalak bali", "konservasi ex situ")],
            "‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("konservasi digital",))],
          ["Keanekaragaman gen adalah variasi dalam satu spesies.", "Keanekaragaman jenis adalah variasi antarspesies.", "Harimau sumatra termasuk fauna oriental.",
           "Anoa termasuk fauna peralihan.", "Cenderawasih termasuk fauna australis.", "Taman nasional adalah konservasi in situ.",
           "Kebun Raya Bogor adalah konservasi ex situ.", "Garis Wallace memisahkan fauna oriental dan peralihan."],
          [("Cenderawasih termasuk fauna oriental.", "Cenderawasih termasuk fauna australis."), ("Kebun binatang adalah konservasi in situ.", "Kebun binatang adalah konservasi ex situ."),
           ("Mangga arumanis dan manalagi menunjukkan keanekaragaman jenis.", "Keduanya satu spesies, jadi keanekaragaman gen."), ("Garis Weber memisahkan Jawa dan Sumatra.", "Garis Weber berada di antara wilayah peralihan dan australis."),
           ("Gajah sumatra termasuk fauna australis.", "Gajah sumatra termasuk fauna oriental."), ("Spesies endemik tersebar di seluruh dunia.", "Spesies endemik hanya hidup di daerah tertentu.")],
          "keanekaragaman hayati", "living-things-and-ecosystems"),

        H("L", "bakteri-dan-fungi", "Bakteri dan Fungi", "Bakteri dan Fungi",
          "Peserta didik menjelaskan ciri, struktur, bentuk, dan cara reproduksi bakteri dan fungi, serta peranannya yang menguntungkan dan merugikan bagi manusia dan ekosistem.",
          "sel prokariotik, bentuk bakteri (kokus, basil, spirilum), pembelahan biner, fungi (Zygomycota, Ascomycota, Basidiomycota), hifa, spora, peranan bakteri dan fungi",
          "Bakteri prokariotik, fungi eukariotik", "Bakteri membelah diri dengan cepat. Fungi tidak berklorofil dan menyerap makanan dari lingkungannya.",
          ["Bakteri adalah makhluk hidup bersel satu yang prokariotik (tidak memiliki membran inti). Bentuknya bulat (kokus), batang (basil), atau spiral (spirilum). Bakteri berkembang biak dengan pembelahan biner.",
           "Fungi (jamur) eukariotik, tidak berklorofil, dan heterotrof. Tubuhnya dari benang hifa yang membentuk miselium, kecuali ragi yang bersel satu. Fungi berkembang biak dengan spora atau bertunas.",
           "Bakteri dan fungi berperan sebagai pengurai. Ada yang bermanfaat (Lactobacillus pada yoghurt, Rhizobium pengikat nitrogen, Rhizopus pada tempe, Penicillium penghasil antibiotik) dan ada yang merugikan (penyebab TBC, tifus, panu, kurap)."],
          [("Mengapa tanaman kacang-kacangan dapat menyuburkan tanah?", ["Akar kacang memiliki bintil akar.", "Bintil akar berisi bakteri Rhizobium yang mengikat nitrogen dari udara."], "karena bersimbiosis dengan bakteri Rhizobium pengikat nitrogen")],
          [("Jamur termasuk tumbuhan karena tidak bergerak.", "Jamur tidak berklorofil dan masuk kingdom Fungi."), ("Semua bakteri menyebabkan penyakit.", "Banyak bakteri bermanfaat, misalnya Lactobacillus dan Rhizobium."),
           ("Bakteri memiliki inti sel yang jelas.", "Bakteri prokariotik, tidak memiliki membran inti.")],
          [("Apa itu antibiotik?", "Zat yang menghambat atau membunuh bakteri. Penisilin pertama kali ditemukan dari jamur Penicillium oleh Alexander Fleming."),
           ("Mengapa jamur disebut heterotrof?", "Karena tidak dapat membuat makanan sendiri; jamur menyerap zat organik dari lingkungannya."),
           ("Apa itu mikoriza?", "Simbiosis jamur dengan akar tumbuhan yang membantu penyerapan air dan mineral.")],
          [("Peranan bakteri dan fungi", [("Lactobacillus bulgaricus", "membuat yoghurt"), ("Rhizobium", "mengikat nitrogen di bintil akar kacang"), ("Acetobacter xylinum", "membuat nata de coco"), ("Escherichia coli", "membantu membentuk vitamin K di usus"),
                                         ("Rhizopus oryzae", "membuat tempe"), ("Saccharomyces cerevisiae", "mengembangkan roti dan membuat tapai"), ("Penicillium notatum", "menghasilkan antibiotik penisilin"), ("Volvariella volvacea", "jamur merang yang dapat dimakan"),
                                         ("Mycobacterium tuberculosis", "menyebabkan TBC"), ("Salmonella typhi", "menyebabkan tifus"), ("Tinea versicolor", "menyebabkan panu"), ("Aspergillus flavus", "menghasilkan racun aflatoksin pada kacang")],
            "Apa peran ‘{k}’?", "Mikroorganisme apa yang berperan ‘{v}’?"),
           ("Bentuk bakteri", [("bulat tunggal", "monokokus"), ("bulat berpasangan", "diplokokus"), ("bulat membentuk rantai", "streptokokus"), ("bulat bergerombol seperti anggur", "stafilokokus"),
                              ("batang tunggal", "monobasil"), ("batang membentuk rantai", "streptobasil"), ("spiral", "spirilum"), ("seperti tanda koma", "vibrio")],
            "Bakteri berbentuk ‘{k}’ disebut ...", "Seperti apa bentuk bakteri ‘{v}’?"),
           ("Bakteri atau fungi", {"ciri bakteri": ["sel prokariotik tanpa membran inti", "berkembang biak dengan pembelahan biner", "ukurannya sekitar 1–5 mikrometer", "ada yang memiliki flagel untuk bergerak", "dinding sel dari peptidoglikan", "dapat membentuk endospora saat kondisi buruk"],
                                  "ciri fungi": ["sel eukariotik dengan membran inti", "tubuh tersusun atas hifa dan miselium", "berkembang biak dengan spora", "dinding sel dari kitin", "tubuh buahnya dapat terlihat seperti payung", "ada yang hidup bersimbiosis dengan ganggang sebagai lumut kerak"]})],
          ["Bakteri adalah makhluk hidup prokariotik.", "Bakteri berkembang biak dengan pembelahan biner.", "Fungi tidak memiliki klorofil.",
           "Tubuh jamur tersusun atas hifa.", "Penisilin dihasilkan oleh jamur Penicillium.", "Rhizobium mengikat nitrogen dari udara.",
           "Tempe dibuat dengan jamur Rhizopus.", "Bakteri dan fungi berperan sebagai pengurai."],
          [("Fungi dapat berfotosintesis.", "Fungi tidak berklorofil sehingga tidak berfotosintesis."), ("Dinding sel jamur tersusun atas selulosa.", "Dinding sel jamur tersusun atas kitin."),
           ("Salmonella typhi menyebabkan TBC.", "Salmonella typhi menyebabkan tifus; TBC disebabkan Mycobacterium tuberculosis."), ("Bakteri bulat berantai disebut stafilokokus.", "Bakteri bulat berantai disebut streptokokus."),
           ("Semua jamur bersel banyak.", "Ragi (Saccharomyces) adalah jamur bersel satu."), ("Bakteri memiliki membran inti.", "Bakteri tidak memiliki membran inti.")],
          "bakteri dan fungi", "living-things-and-ecosystems"),

        H("E", "energi-terbarukan", "Energi Terbarukan dan Konversi Energi", "Energi Terbarukan",
          "Peserta didik menjelaskan bentuk-bentuk energi, konversi energi dan efisiensinya, sumber energi terbarukan dan tak terbarukan, dampak eksplorasi energi, serta pemanfaatan potensi energi lokal.",
          "bentuk energi, konversi energi, efisiensi, energi surya, angin, air, panas bumi, biomassa, dampak bahan bakar fosil, potensi energi lokal",
          "Efisiensi = energi berguna ÷ energi masukan × 100%", "Tidak ada alat yang efisiensinya 100%. Indonesia kaya energi terbarukan seperti panas bumi dan surya.",
          ["Energi tidak dapat diciptakan atau dimusnahkan, tetapi dapat dikonversi. Pada setiap konversi sebagian energi berubah menjadi panas yang tidak berguna, sehingga efisiensi selalu kurang dari 100%.",
           "Sumber energi terbarukan: matahari (PLTS), angin (PLTB), air (PLTA), panas bumi (PLTP), biomassa, dan gelombang laut. Sumber tak terbarukan: minyak bumi, gas alam, batu bara, dan uranium.",
           "Penggunaan bahan bakar fosil menghasilkan gas rumah kaca dan polusi. Indonesia memiliki potensi panas bumi besar karena banyak gunung api, serta cahaya matahari sepanjang tahun."],
          [("Lampu LED menerima energi listrik 10 J dan menghasilkan cahaya 8 J. Berapa efisiensinya?", ["Efisiensi = 8 ÷ 10 × 100%.", "= 80%."], "80%")],
          [("Mesin yang baik memiliki efisiensi 100%.", "Selalu ada energi yang terbuang sebagai panas, jadi efisiensi kurang dari 100%."), ("Uranium termasuk energi terbarukan.", "Uranium adalah bahan tambang yang dapat habis."),
           ("Energi terbarukan sama sekali tidak berdampak pada lingkungan.", "Pembangunan bendungan PLTA, misalnya, dapat mengubah ekosistem sungai.")],
          [("Mengapa lampu LED lebih hemat daripada lampu pijar?", "Lampu LED mengubah lebih banyak energi listrik menjadi cahaya; lampu pijar banyak menghasilkan panas."),
           ("Apa itu PLTMH?", "Pembangkit listrik tenaga mikrohidro, PLTA kecil yang memanfaatkan aliran sungai di desa terpencil."),
           ("Apa contoh potensi energi lokal?", "Biogas dari kotoran ternak, mikrohidro dari sungai pegunungan, dan panel surya di daerah terpencil.")],
          [("Konversi energi", [("PLTA", "energi potensial air menjadi energi listrik"), ("PLTS", "energi cahaya menjadi energi listrik"), ("PLTB", "energi kinetik angin menjadi energi listrik"),
                               ("PLTP", "energi panas bumi menjadi energi listrik"), ("PLTU", "energi kimia batu bara menjadi panas lalu listrik"), ("aki yang diisi ulang", "energi listrik menjadi energi kimia"),
                               ("motor listrik", "energi listrik menjadi energi kinetik"), ("generator", "energi kinetik menjadi energi listrik"), ("kompor biogas", "energi kimia menjadi energi panas")],
            "Konversi energi apa yang terjadi pada ‘{k}’?", "Alat atau pembangkit apa yang mengubah ‘{v}’?"),
           ("Terbarukan atau tidak", [("panas bumi", "terbarukan"), ("cahaya matahari", "terbarukan"), ("angin", "terbarukan"), ("air terjun", "terbarukan"), ("biomassa", "terbarukan"), ("gelombang laut", "terbarukan"),
                                     ("minyak bumi", "tak terbarukan"), ("gas alam", "tak terbarukan"), ("batu bara", "tak terbarukan"), ("uranium", "tak terbarukan")],
            "Sumber energi ‘{k}’ termasuk ...", "Manakah sumber energi yang ‘{v}’?", ("setengah terbarukan", "buatan")),
           ("Dampak energi", {"dampak penggunaan bahan bakar fosil": ["menambah gas rumah kaca", "menyebabkan hujan asam", "polusi udara di kota", "cadangannya makin menipis", "tumpahan minyak di laut", "lubang bekas tambang batu bara"],
                             "kelebihan energi terbarukan": ["sumbernya tidak habis", "sedikit menghasilkan emisi", "dapat dibangun di desa terpencil", "mengurangi ketergantungan impor minyak", "biaya bahan bakarnya hampir nol", "mendukung pembangunan berkelanjutan"]})],
          ["Energi tidak dapat diciptakan atau dimusnahkan.", "Efisiensi alat selalu kurang dari 100%.", "PLTS mengubah energi cahaya menjadi energi listrik.",
           "Panas bumi adalah energi terbarukan.", "Indonesia memiliki potensi panas bumi yang besar.", "Bahan bakar fosil menghasilkan gas rumah kaca.",
           "Lampu LED lebih efisien daripada lampu pijar.", "Biogas dapat dibuat dari kotoran ternak."],
          [("Batu bara termasuk energi terbarukan.", "Batu bara tak terbarukan."), ("Generator mengubah energi listrik menjadi energi kinetik.", "Generator mengubah energi kinetik menjadi listrik."),
           ("Efisiensi dapat lebih dari 100%.", "Efisiensi selalu kurang dari 100%."), ("PLTB memanfaatkan panas bumi.", "PLTB memanfaatkan angin."),
           ("Lampu pijar lebih hemat daripada LED.", "LED lebih hemat."), ("Energi terbarukan selalu tanpa dampak lingkungan.", "Energi terbarukan juga dapat berdampak, misalnya bendungan PLTA.")],
          "energi terbarukan", "energy", calc=f_efisiensi),

        H("X", "perubahan-iklim", "Perubahan Iklim", "Perubahan Iklim",
          "Peserta didik menjelaskan perubahan iklim, gejala dan penyebabnya, efek rumah kaca, dampaknya bagi kehidupan, serta upaya mitigasi, adaptasi, dan kerja sama global.",
          "cuaca dan iklim, efek rumah kaca, gas rumah kaca, pemanasan global, dampak perubahan iklim, mitigasi, adaptasi, Perjanjian Paris",
          "Gas rumah kaca berlebih memicu perubahan iklim", "Mitigasi mengurangi penyebab perubahan iklim, adaptasi menyesuaikan diri dengan dampaknya.",
          ["Perubahan iklim adalah perubahan pola iklim dalam jangka panjang, terutama karena naiknya suhu rata-rata bumi akibat bertambahnya gas rumah kaca (CO₂, CH₄, N₂O) dari kegiatan manusia.",
           "Gejala dan dampaknya: suhu meningkat, es kutub dan gletser mencair, permukaan laut naik, cuaca ekstrem lebih sering, pemutihan terumbu karang, dan gagal panen.",
           "Mitigasi mengurangi emisi, misalnya energi terbarukan dan reboisasi. Adaptasi menyesuaikan diri, misalnya varietas padi tahan kekeringan dan tanggul pantai. Perjanjian Paris 2015 menargetkan kenaikan suhu di bawah 2 °C."],
          [("Petani menanam varietas padi tahan genangan karena banjir makin sering. Upaya apakah ini?", ["Petani tidak mengurangi emisi.", "Petani menyesuaikan diri dengan dampak perubahan iklim."], "adaptasi")],
          [("Efek rumah kaca selalu merugikan.", "Efek rumah kaca alami menjaga bumi cukup hangat; masalahnya jika berlebihan."), ("Mitigasi dan adaptasi adalah hal yang sama.", "Mitigasi mengurangi penyebab, adaptasi menyesuaikan dengan dampak."),
           ("Perubahan iklim hanya berdampak di kutub.", "Indonesia juga terdampak, misalnya banjir rob, kekeringan, dan pemutihan karang.")],
          [("Apa itu Perjanjian Paris?", "Kesepakatan global tahun 2015 untuk menahan kenaikan suhu bumi di bawah 2 °C dan berupaya 1,5 °C dibanding masa praindustri."),
           ("Apa itu banjir rob?", "Banjir air laut ke daratan pesisir saat pasang, makin parah karena naiknya permukaan laut dan penurunan tanah."),
           ("Apa itu karbon biru?", "Karbon yang diserap dan disimpan ekosistem pesisir seperti hutan bakau dan padang lamun.")],
          [("Mitigasi atau adaptasi", [("beralih ke pembangkit listrik tenaga surya", "mitigasi"), ("menanam kembali hutan yang gundul", "mitigasi"), ("memakai kendaraan listrik dan transportasi umum", "mitigasi"),
                                      ("mengurangi pembakaran sampah", "mitigasi"), ("menjaga hutan bakau sebagai penyimpan karbon", "mitigasi"), ("membangun tanggul laut di pesisir", "adaptasi"),
                                      ("menanam padi varietas tahan kekeringan", "adaptasi"), ("membuat rumah panggung di daerah rawan banjir", "adaptasi"), ("menyusun kalender tanam baru sesuai pola hujan", "adaptasi"),
                                      ("membuat embung untuk menampung air hujan", "adaptasi")],
            "‘{k}’ termasuk upaya ...", "Manakah contoh upaya ‘{v}’?", ("eksploitasi",)),
           ("Gejala dan dampak", [("suhu rata-rata bumi meningkat", "es di kutub dan gletser mencair"), ("es di kutub dan gletser mencair", "permukaan laut naik"), ("suhu air laut meningkat", "terumbu karang memutih"),
                                 ("pola hujan berubah", "petani sulit menentukan musim tanam"), ("kemarau lebih panjang", "kebakaran hutan dan lahan"), ("permukaan laut naik", "banjir rob di kota pesisir"),
                                 ("cuaca ekstrem lebih sering", "banjir dan badai lebih sering terjadi")],
            "Apa dampak dari ‘{k}’?", "Apa penyebab ‘{v}’?"),
           ("Istilah perubahan iklim", [("efek rumah kaca", "terperangkapnya panas matahari oleh gas di atmosfer"), ("gas rumah kaca", "gas seperti CO₂ dan CH₄ yang menahan panas"), ("pemanasan global", "naiknya suhu rata-rata bumi"),
                                       ("mitigasi", "upaya mengurangi penyebab perubahan iklim"), ("adaptasi", "upaya menyesuaikan diri dengan dampak perubahan iklim"), ("emisi", "pelepasan gas ke atmosfer"),
                                       ("jejak karbon", "jumlah gas rumah kaca dari kegiatan seseorang"), ("karbon biru", "karbon yang disimpan ekosistem pesisir")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Perubahan iklim terutama disebabkan bertambahnya gas rumah kaca.", "Karbon dioksida adalah gas rumah kaca.", "Pemanasan global membuat permukaan laut naik.",
           "Mitigasi mengurangi penyebab perubahan iklim.", "Adaptasi menyesuaikan diri dengan dampak perubahan iklim.", "Hutan bakau menyimpan karbon.",
           "Perjanjian Paris menargetkan kenaikan suhu di bawah 2 °C.", "Suhu laut yang naik dapat memutihkan terumbu karang."],
          [("Membangun tanggul laut adalah upaya mitigasi.", "Tanggul laut adalah adaptasi terhadap naiknya permukaan laut."), ("Gas oksigen adalah gas rumah kaca utama.", "Gas rumah kaca utama adalah CO₂, CH₄, dan N₂O."),
           ("Perubahan iklim menurunkan permukaan laut.", "Perubahan iklim menaikkan permukaan laut."), ("Menebang hutan termasuk mitigasi.", "Menebang hutan menambah emisi; reboisasi yang termasuk mitigasi."),
           ("Indonesia tidak terdampak perubahan iklim.", "Indonesia terdampak banjir rob, kekeringan, dan cuaca ekstrem."), ("Perjanjian Paris ditandatangani pada tahun 1990.", "Perjanjian Paris disepakati pada tahun 2015.")],
          "perubahan iklim", "earths-systems"),
    ]
