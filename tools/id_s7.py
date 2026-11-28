# -*- coding: utf-8 -*-
"""Indonesia / IPA Kelas 7（Fase D。Buku Siswa IPA Kelas VII Kurikulum Merdeka edisi revisi）"""
from id_sci import H, nq, num


def f_konversi(R):
    k = R.choice(["cm-m", "g-kg", "mL-L", "km-m", "menit-s", "jam-menit", "mg-g", "dm3-L"])
    if k == "cm-m":
        x = R.choice([25, 40, 75, 120, 150, 250, 350, 480])
        return nq("Panjang meja %s cm. Berapa meter panjang meja itu?" % num(x), x / 100, [x / 10, x * 100, x / 1000], "m", "1 m = 100 cm, jadi %s cm = %s ÷ 100 = %s m." % (num(x), num(x), num(x / 100)))
    if k == "g-kg":
        x = R.choice([250, 500, 750, 1200, 1500, 2500, 3200, 4800])
        return nq("Massa sekantong gula %s g. Berapa kilogram massanya?" % num(x), x / 1000, [x / 100, x * 1000, x / 10], "kg", "1 kg = 1.000 g, jadi %s g = %s kg." % (num(x), num(x / 1000)))
    if k == "mL-L":
        x = R.choice([250, 600, 750, 1500, 1800, 2400, 3500])
        return nq("Sebuah botol berisi %s mL air. Berapa liter volumenya?" % num(x), x / 1000, [x / 100, x * 1000, x / 10], "L", "1 L = 1.000 mL, jadi %s mL = %s L." % (num(x), num(x / 1000)))
    if k == "km-m":
        x = R.choice([2, 3, 5, 8, 12, 15])
        y = R.choice([0.5, 1.5, 2.5, 4.5])
        v = x + y
        return nq("Jarak rumah ke sekolah %s km. Berapa meter jaraknya?" % num(v), v * 1000, [v * 100, v * 10, v * 10000], "m", "1 km = 1.000 m, jadi %s km = %s m." % (num(v), num(v * 1000)))
    if k == "menit-s":
        x = R.choice([2, 3, 5, 7, 12, 15, 20])
        return nq("Seorang siswa berlari selama %d menit. Berapa sekon lamanya?" % x, x * 60, [x * 100, x * 10, x * 30], "s", "1 menit = 60 s, jadi %d menit = %d s." % (x, x * 60))
    if k == "jam-menit":
        x = R.choice([1.5, 2.5, 3, 4, 0.75, 1.25])
        return nq("Perjalanan bus berlangsung %s jam. Berapa menit lamanya?" % num(x), x * 60, [x * 100, x * 30, x * 10], "menit", "1 jam = 60 menit, jadi %s jam = %s menit." % (num(x), num(x * 60)))
    if k == "mg-g":
        x = R.choice([500, 250, 750, 1500, 2000])
        return nq("Sebuah tablet vitamin bermassa %s mg. Berapa gram massanya?" % num(x), x / 1000, [x / 100, x * 1000, x / 10], "g", "1 g = 1.000 mg, jadi %s mg = %s g." % (num(x), num(x / 1000)))
    x = R.choice([2, 5, 8, 12, 20])
    return nq("Sebuah akuarium bervolume %d dm³. Berapa liter volumenya?" % x, x, [x * 1000, x / 1000, x * 10], "L", "1 dm³ = 1 L, jadi %d dm³ = %d L." % (x, x))


def f_massa_jenis(R):
    k = R.choice(["rho", "m", "V"])
    mat = R.choice([("air", 1), ("aluminium", 2.7), ("besi", 7.9), ("minyak goreng", 0.9), ("kayu jati", 0.7), ("kaca", 2.5), ("es", 0.92)])
    V = R.choice([10, 20, 40, 50, 100, 200, 250])
    m = mat[1] * V
    if k == "rho":
        return nq("Sebuah benda bermassa %s g dan bervolume %s cm³. Berapa massa jenisnya?" % (num(m), num(V)), mat[1], [V / m, m * V, m - V if m > V else m + V], "g/cm³",
                  "ρ = m ÷ V = %s ÷ %s = %s g/cm³ (seperti %s)." % (num(m), num(V), num(mat[1]), mat[0]))
    if k == "m":
        return nq("Massa jenis %s %s g/cm³. Berapa massa %s cm³ %s?" % (mat[0], num(mat[1]), num(V), mat[0]), m, [V / mat[1], V + mat[1], V], "g",
                  "m = ρ × V = %s × %s = %s g." % (num(mat[1]), num(V), num(m)))
    return nq("Massa jenis %s %s g/cm³. Berapa volume %s g %s?" % (mat[0], num(mat[1]), num(m), mat[0]), V, [m * mat[1], m - mat[1], m], "cm³",
              "V = m ÷ ρ = %s ÷ %s = %s cm³." % (num(m), num(mat[1]), num(V)))


def f_suhu(R):
    c = R.choice([10, 20, 25, 30, 35, 40, 50, 60, 75, 80, 100])
    k = R.choice(["F", "K", "R", "CfromF"])
    if k == "F":
        f = c * 9 / 5 + 32
        return nq("Suhu air %d °C. Berapa suhunya dalam skala Fahrenheit?" % c, f, [c * 9 / 5, c * 5 / 9 + 32, c + 32], "°F", "°F = (9/5 × %d) + 32 = %s °F." % (c, num(f)))
    if k == "K":
        return nq("Suhu ruangan %d °C. Berapa suhunya dalam kelvin?" % c, c + 273, [c - 273 if c > 273 else c + 237, c + 100, c * 2 + 32], "K", "K = °C + 273 = %d + 273 = %d K." % (c, c + 273))
    if k == "R":
        r = c * 4 / 5
        return nq("Suhu sup %d °C. Berapa suhunya dalam skala Reamur?" % c, r, [c * 5 / 4, c, c * 9 / 5], "°R", "°R = 4/5 × %d = %s °R." % (c, num(r)))
    f = c * 9 / 5 + 32
    return nq("Termometer menunjukkan %s °F. Berapa suhunya dalam °C?" % num(f), c, [f - 32, (f - 32) * 9 / 5, f * 5 / 9], "°C", "°C = 5/9 × (%s − 32) = %d °C." % (num(f), c))


def f_kalor(R):
    mat = R.choice([("air", 4200), ("aluminium", 900), ("besi", 450), ("tembaga", 390), ("es", 2100)])
    m = R.choice([0.2, 0.5, 1, 2, 3, 4])
    dT = R.choice([5, 10, 20, 25, 30, 40]) if mat[0] != "es" else R.choice([5, 10, 20])
    Q = m * mat[1] * dT
    if R.random() < 0.6:
        return nq("Berapa kalor yang diperlukan untuk menaikkan suhu %s kg %s sebesar %d °C? (c %s = %s J/kg°C)" % (num(m), mat[0], dT, mat[0], num(mat[1])), Q,
                  [mat[1] * dT, m * mat[1], m * dT, Q * 10], "J", "Q = m × c × ΔT = %s × %s × %d = %s J." % (num(m), num(mat[1]), dT, num(Q)))
    return nq("Sebanyak %s J kalor diberikan pada %s kg %s (c = %s J/kg°C). Berapa kenaikan suhunya?" % (num(Q), num(m), mat[0], num(mat[1])), dT,
              [Q / mat[1], Q / m, Q / (m * mat[1]) * 10], "°C", "ΔT = Q ÷ (m × c) = %s ÷ (%s × %s) = %d °C." % (num(Q), num(m), num(mat[1]), dT))


def f_gerak(R):
    k = R.choice(["v", "s", "t", "kmh"])
    if k == "v":
        t = R.choice([4, 5, 8, 10, 20, 25])
        v = R.choice([2, 3, 4, 5, 6, 8, 12])
        s = v * t
        return nq("Seekor kuda berlari menempuh %d m dalam %d s. Berapa kecepatannya?" % (s, t), v, [s * t, t / s, s - t], "m/s", "v = s ÷ t = %d ÷ %d = %d m/s." % (s, t, v))
    if k == "s":
        v = R.choice([40, 50, 60, 80])
        t = R.choice([1.5, 2, 2.5, 3, 4])
        return nq("Mobil melaju tetap %d km/jam selama %s jam. Berapa jarak yang ditempuh?" % (v, num(t)), v * t, [v / t, v + t, t / v * 1000], "km", "s = v × t = %d × %s = %s km." % (v, num(t), num(v * t)))
    if k == "t":
        v = R.choice([4, 5, 10, 20])
        s = v * R.choice([15, 30, 60, 90, 120])
        return nq("Sepeda melaju tetap %d m/s. Berapa sekon waktu untuk menempuh %s m?" % (v, num(s)), s / v, [s * v, s - v, v / s * 100], "s", "t = s ÷ v = %s ÷ %d = %s s." % (num(s), v, num(s / v)))
    kmh = R.choice([18, 36, 54, 72, 90, 108])
    return nq("Kecepatan sebuah motor %d km/jam. Berapa m/s kecepatannya?" % kmh, kmh / 3.6, [kmh * 3.6, kmh / 60, kmh * 1000], "m/s", "%d km/jam = %d × 1.000 m ÷ 3.600 s = %s m/s." % (kmh, kmh, num(kmh / 3.6)))


def f_gaya(R):
    k = R.choice(["F", "a", "w", "res"])
    if k == "F":
        m = R.choice([2, 5, 10, 20, 50])
        a = R.choice([0.5, 1, 2, 3, 4])
        return nq("Benda bermassa %d kg dipercepat %s m/s². Berapa gaya total yang bekerja?" % (m, num(a)), m * a, [m / a, a / m, m + a], "N", "F = m × a = %d × %s = %s N." % (m, num(a), num(m * a)))
    if k == "a":
        m = R.choice([2, 4, 5, 10, 25])
        F = m * R.choice([2, 3, 4, 6])
        return nq("Gaya %d N bekerja pada benda bermassa %d kg. Berapa percepatannya?" % (F, m), F / m, [F * m, m / F, F - m], "m/s²", "a = F ÷ m = %d ÷ %d = %s m/s²." % (F, m, num(F / m)))
    if k == "w":
        m = R.choice([3, 5, 12, 40, 50, 65])
        return nq("Berapa berat benda bermassa %d kg di bumi? (g = 10 m/s²)" % m, m * 10, [m, m / 10, m * 100], "N", "w = m × g = %d × 10 = %d N." % (m, m * 10))
    F1 = R.choice([20, 30, 45, 60, 80])
    F2 = R.choice([10, 15, 25, 35])
    if F2 >= F1:
        return None
    return nq("Andi mendorong meja ke kanan dengan gaya %d N, sedangkan Beni mendorong ke kiri dengan gaya %d N. Berapa resultan gayanya?" % (F1, F2), F1 - F2, [F1 + F2, F1 * F2, (F1 + F2) / 2], "N",
              "Gaya berlawanan arah dikurangkan: %d − %d = %d N ke kanan." % (F1, F2, F1 - F2))


def UNITS(g):
    return [
        H("X", "hakikat-sains-dan-metode-ilmiah", "Hakikat Ilmu Sains dan Metode Ilmiah", "Metode Ilmiah",
          "Peserta didik menjelaskan hakikat sains, langkah-langkah metode ilmiah (mengamati, merumuskan masalah, hipotesis, percobaan, analisis, kesimpulan), variabel percobaan, dan cara melaporkan hasil percobaan.",
          "sains, metode ilmiah, hipotesis, variabel bebas, terikat, dan kontrol, data kualitatif dan kuantitatif, laporan percobaan",
          "Sains dibangun dari pengamatan dan percobaan", "Ilmuwan mengamati, membuat pertanyaan dan hipotesis, menguji dengan percobaan, lalu menarik kesimpulan dari data.",
          ["Sains adalah cara mempelajari alam secara sistematis melalui pengamatan dan percobaan. Hasilnya berupa pengetahuan yang dapat diuji ulang oleh orang lain.",
           "Langkah metode ilmiah: mengamati, merumuskan masalah, menyusun hipotesis (dugaan sementara), melakukan percobaan, menganalisis data, lalu menarik kesimpulan dan melaporkannya.",
           "Dalam percobaan ada variabel bebas (yang sengaja diubah), variabel terikat (yang diamati atau diukur), dan variabel kontrol (yang dijaga tetap sama agar percobaan adil)."],
          [("Siti menyelidiki pengaruh banyaknya air terhadap tinggi tanaman kacang. Ia memakai pot, tanah, dan jenis kacang yang sama. Apa variabel bebasnya?", ["Yang sengaja diubah adalah banyaknya air.", "Tinggi tanaman yang diukur adalah variabel terikat.", "Pot, tanah, dan jenis kacang adalah variabel kontrol."], "banyaknya air")],
          [("Hipotesis selalu benar.", "Hipotesis adalah dugaan sementara yang harus diuji dan bisa saja salah."), ("Percobaan cukup dilakukan sekali.", "Percobaan sebaiknya diulang agar hasilnya dapat dipercaya."),
           ("Semua hal boleh diubah sekaligus dalam percobaan.", "Hanya satu variabel bebas yang diubah; yang lain dijaga tetap.")],
          [("Apa beda data kualitatif dan kuantitatif?", "Data kualitatif berupa sifat atau keterangan, misalnya warna dan bau. Data kuantitatif berupa angka hasil pengukuran, misalnya suhu 30 °C."),
           ("Apa itu kesimpulan?", "Jawaban atas rumusan masalah berdasarkan data percobaan; kesimpulan dapat mendukung atau menolak hipotesis."),
           ("Mengapa percobaan perlu diulang?", "Agar hasilnya tidak kebetulan dan kesalahan pengukuran dapat diperkecil.")],
          [("Langkah metode ilmiah", [("mencatat bahwa roti cepat berjamur di tempat lembap", "mengamati"), ("bertanya apakah kelembapan memengaruhi pertumbuhan jamur", "merumuskan masalah"),
                                     ("menduga roti di tempat lembap lebih cepat berjamur", "menyusun hipotesis"), ("menyimpan dua roti di tempat lembap dan kering selama 5 hari", "melakukan percobaan"),
                                     ("membuat tabel dan grafik jumlah bercak jamur setiap hari", "menganalisis data"), ("menyatakan bahwa kelembapan mempercepat pertumbuhan jamur", "menarik kesimpulan"),
                                     ("menuliskan tujuan, alat, langkah, hasil, dan kesimpulan", "membuat laporan")],
            "Kegiatan ‘{k}’ termasuk langkah ...", "Manakah contoh langkah ‘{v}’?"),
           ("Variabel percobaan", [("jenis pupuk yang sengaja diganti pada percobaan pupuk", "variabel bebas"), ("tinggi tanaman yang diukur pada percobaan pupuk", "variabel terikat"),
                                  ("jenis tanaman dan banyaknya air yang dibuat sama pada percobaan pupuk", "variabel kontrol"), ("suhu air yang sengaja diubah pada percobaan melarutkan gula", "variabel bebas"),
                                  ("waktu larutnya gula yang dicatat pada percobaan melarutkan gula", "variabel terikat"), ("massa gula dan volume air yang dibuat sama pada percobaan melarutkan gula", "variabel kontrol"),
                                  ("ketinggian jatuh bola yang sengaja diubah", "variabel bebas"), ("tinggi pantulan bola yang diukur", "variabel terikat"), ("jenis bola yang dibuat sama", "variabel kontrol")],
            "‘{k}’ disebut ...", "Manakah yang merupakan ‘{v}’?", ("variabel acak",)),
           ("Data kualitatif atau kuantitatif", [("warna larutan berubah menjadi merah muda", "data kualitatif"), ("bau gas yang dihasilkan menyengat", "data kualitatif"), ("permukaan daun terasa kasar", "data kualitatif"),
                                                ("larutan tampak keruh", "data kualitatif"), ("bunga berwarna kuning", "data kualitatif"), ("suhu air 36 °C", "data kuantitatif"), ("tinggi tanaman 12,5 cm", "data kuantitatif"),
                                                ("massa batu 250 g", "data kuantitatif"), ("waktu larut gula 45 s", "data kuantitatif"), ("volume gas 20 mL", "data kuantitatif")],
            "‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("data hipotesis",))],
          ["Hipotesis adalah dugaan sementara yang harus diuji.", "Variabel bebas adalah variabel yang sengaja diubah.", "Variabel terikat adalah variabel yang diukur atau diamati.",
           "Variabel kontrol dijaga tetap sama.", "Percobaan perlu diulang agar hasilnya dapat dipercaya.", "Data kuantitatif berupa angka hasil pengukuran.",
           "Kesimpulan ditarik berdasarkan data percobaan.", "Hasil percobaan perlu dilaporkan agar dapat diuji orang lain."],
          [("Hipotesis adalah kesimpulan akhir percobaan.", "Hipotesis adalah dugaan sementara sebelum percobaan."), ("Variabel kontrol adalah variabel yang sengaja diubah.", "Yang sengaja diubah adalah variabel bebas."),
           ("Warna bunga termasuk data kuantitatif.", "Warna adalah data kualitatif."), ("Kesimpulan boleh dibuat tanpa data.", "Kesimpulan harus berdasarkan data."),
           ("Percobaan yang baik mengubah banyak variabel sekaligus.", "Percobaan yang adil hanya mengubah satu variabel bebas."), ("Sains tidak dapat diuji ulang.", "Pengetahuan sains dapat diuji ulang oleh orang lain.")],
          "metode ilmiah", "working-scientifically"),

        H("X", "laboratorium-dan-pengukuran", "Laboratorium IPA dan Pengukuran", "Pengukuran",
          "Peserta didik mengenal alat laboratorium dan keselamatan kerja, besaran pokok dan turunan, satuan Sistem Internasional, alat ukur, serta konversi satuan.",
          "alat laboratorium, simbol bahaya, besaran pokok dan turunan, satuan SI, alat ukur, konversi satuan",
          "Setiap besaran punya satuan dan alat ukur", "Panjang diukur dalam meter, massa dalam kilogram, waktu dalam sekon. Satuan harus diubah dengan benar sebelum dihitung.",
          ["Besaran adalah sesuatu yang dapat diukur dan dinyatakan dengan angka dan satuan. Besaran pokok antara lain panjang (m), massa (kg), waktu (s), suhu (K), kuat arus listrik (A), jumlah zat (mol), dan intensitas cahaya (cd).",
           "Besaran turunan diturunkan dari besaran pokok, misalnya luas (m²), volume (m³), kecepatan (m/s), dan massa jenis (kg/m³).",
           "Di laboratorium kita memakai alat sesuai fungsinya dan mematuhi aturan keselamatan: memakai jas lab, tidak mencicipi bahan kimia, dan memperhatikan simbol bahaya pada label."],
          [("Ubah 2,5 kg menjadi gram.", ["1 kg = 1.000 g.", "2,5 × 1.000 = 2.500."], "2.500 g")],
          [("Kecepatan termasuk besaran pokok.", "Kecepatan diturunkan dari panjang dan waktu, jadi besaran turunan."), ("Satuan SI untuk massa adalah gram.", "Satuan SI untuk massa adalah kilogram."),
           ("Bahan kimia boleh dicicipi untuk mengenalinya.", "Bahan kimia tidak boleh dicicipi karena berbahaya.")],
          [("Apa beda neraca dan timbangan berat badan?", "Neraca (misalnya neraca Ohaus) mengukur massa dengan teliti di laboratorium, sedangkan timbangan badan dipakai untuk massa orang."),
           ("Apa arti simbol tengkorak pada label?", "Bahan tersebut beracun (toksik) dan berbahaya jika tertelan, terhirup, atau terkena kulit."),
           ("Mengapa perlu satuan baku?", "Agar hasil pengukuran sama di mana pun, tidak seperti jengkal atau depa yang berbeda tiap orang.")],
          [("Alat ukur", [("panjang buku", "penggaris"), ("diameter dalam tabung", "jangka sorong"), ("tebal selembar kertas", "mikrometer sekrup"), ("massa batu di laboratorium", "neraca"),
                         ("waktu lari 100 m", "stopwatch"), ("suhu badan", "termometer"), ("volume cairan", "gelas ukur"), ("kuat arus listrik", "amperemeter"), ("lebar lapangan", "meteran")],
            "Alat apa yang paling tepat untuk mengukur ‘{k}’?", "Alat ‘{v}’ paling tepat untuk mengukur ...", ("barometer",)),
           ("Besaran dan satuan SI", [("panjang", "meter (m)", "p"), ("massa", "kilogram (kg)", "p"), ("waktu", "sekon (s)", "p"), ("suhu", "kelvin (K)", "p"), ("kuat arus listrik", "ampere (A)", "p"),
                                     ("jumlah zat", "mol", "p"), ("intensitas cahaya", "kandela (cd)", "p"), ("luas", "meter persegi (m²)", "t"), ("volume", "meter kubik (m³)", "t"),
                                     ("kecepatan", "meter per sekon (m/s)", "t"), ("massa jenis", "kilogram per meter kubik (kg/m³)", "t"), ("gaya", "newton (N)", "t")],
            "Apa satuan SI untuk besaran ‘{k}’?", "Besaran apa yang satuan SI-nya ‘{v}’?"),
           ("Pokok atau turunan", {"besaran pokok": ["panjang", "massa", "waktu", "suhu", "kuat arus listrik", "jumlah zat", "intensitas cahaya"],
                                  "besaran turunan": ["luas", "volume", "kecepatan", "massa jenis", "gaya", "percepatan", "tekanan"]})],
          ["Massa memiliki satuan SI kilogram.", "Panjang memiliki satuan SI meter.", "Luas adalah besaran turunan.",
           "Kecepatan memiliki satuan meter per sekon.", "Stopwatch dipakai untuk mengukur waktu.", "Jangka sorong dapat mengukur diameter dalam tabung.",
           "Bahan kimia di laboratorium tidak boleh dicicipi.", "1 kg sama dengan 1.000 g."],
          [("Satuan SI untuk waktu adalah menit.", "Satuan SI untuk waktu adalah sekon."), ("Volume termasuk besaran pokok.", "Volume adalah besaran turunan."),
           ("Termometer dipakai untuk mengukur massa.", "Termometer dipakai untuk mengukur suhu."), ("1 m sama dengan 10 cm.", "1 m sama dengan 100 cm."),
           ("Gelas ukur dipakai untuk mengukur panjang.", "Gelas ukur dipakai untuk mengukur volume cairan."), ("Jas lab tidak perlu dipakai di laboratorium.", "Jas lab melindungi tubuh dan pakaian dari bahan kimia.")],
          "besaran dan pengukuran", "working-scientifically", calc=f_konversi),

        H("M", "wujud-zat-dan-model-partikel", "Wujud Zat dan Model Partikel", "Wujud Zat",
          "Peserta didik menjelaskan sifat zat padat, cair, dan gas berdasarkan model partikel (susunan, jarak, dan gerak partikel) serta mengaitkannya dengan bentuk dan volume zat.",
          "zat padat, cair, gas, susunan dan gerak partikel, bentuk dan volume, difusi",
          "Susunan partikel menentukan wujud zat", "Partikel padat rapat dan bergetar, cair agak renggang dan bergeser, gas sangat renggang dan bergerak bebas.",
          ["Semua zat tersusun atas partikel yang sangat kecil dan selalu bergerak. Wujud zat ditentukan oleh susunan, jarak, dan gaya tarik antarpartikelnya.",
           "Zat padat: partikel sangat rapat dan hanya bergetar, sehingga bentuk dan volumenya tetap. Zat cair: partikel agak renggang dan dapat bergeser, sehingga volumenya tetap tetapi bentuknya mengikuti wadah.",
           "Gas: partikel sangat renggang dan bergerak bebas ke segala arah, sehingga bentuk dan volumenya mengikuti wadah dan mudah dimampatkan. Bau parfum yang menyebar adalah contoh difusi."],
          [("Air dari botol dituang ke piring. Apa yang berubah?", ["Air adalah zat cair.", "Zat cair bentuknya mengikuti wadah, tetapi volumenya tetap."], "bentuknya berubah, volumenya tetap")],
          [("Partikel zat padat tidak bergerak sama sekali.", "Partikel zat padat tetap bergetar di tempatnya."), ("Gas tidak memiliki massa.", "Gas memiliki massa, misalnya bola yang dipompa menjadi lebih berat."),
           ("Zat cair mudah dimampatkan.", "Zat cair hampir tidak dapat dimampatkan; gas yang mudah dimampatkan.")],
          [("Apa itu difusi?", "Penyebaran partikel dari tempat berkonsentrasi tinggi ke rendah, misalnya bau parfum menyebar di ruangan atau teh menyebar di air."),
           ("Mengapa gas mudah dimampatkan?", "Jarak antarpartikel gas sangat jauh, sehingga partikelnya dapat didesak lebih rapat."),
           ("Mengapa pasir dapat dituang padahal padat?", "Setiap butir pasir adalah zat padat dengan bentuk tetap; yang mengalir adalah kumpulan butirnya.")],
          [("Sifat wujud zat", [("bentuk tetap dan volume tetap", "zat padat"), ("partikel tersusun sangat rapat dan teratur", "zat padat"), ("partikel hanya bergetar di tempatnya", "zat padat"),
                               ("bentuk mengikuti wadah tetapi volume tetap", "zat cair"), ("partikel agak renggang dan dapat bergeser", "zat cair"), ("permukaannya selalu datar saat diam", "zat cair"),
                               ("bentuk dan volume mengikuti wadah", "gas"), ("partikel sangat renggang dan bergerak bebas", "gas"), ("paling mudah dimampatkan", "gas")],
            "Ciri ‘{k}’ dimiliki oleh ...", "Manakah ciri ‘{v}’?", ("plasma",)),
           ("Contoh wujud zat", [("batu", "zat padat"), ("es batu", "zat padat"), ("kayu", "zat padat"), ("garam dapur", "zat padat"), ("minyak goreng", "zat cair"), ("air teh", "zat cair"),
                                ("susu", "zat cair"), ("raksa", "zat cair"), ("oksigen", "gas"), ("uap air", "gas"), ("udara di dalam ban", "gas"), ("karbon dioksida", "gas")],
            "Pada suhu ruang, ‘{k}’ berwujud ...", "Manakah yang berwujud ‘{v}’ pada suhu ruang?", ("plasma",)),
           ("Istilah partikel", [("partikel", "bagian terkecil penyusun zat"), ("difusi", "penyebaran partikel dari konsentrasi tinggi ke rendah"), ("kohesi", "gaya tarik antarpartikel sejenis"),
                                ("adhesi", "gaya tarik antarpartikel tidak sejenis"), ("pemampatan", "pengurangan volume karena ditekan"), ("model partikel", "gambaran zat sebagai kumpulan partikel kecil yang bergerak"),
                                ("gerak Brown", "gerak acak partikel kecil di dalam zat cair atau gas")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Zat padat memiliki bentuk dan volume tetap.", "Zat cair memiliki volume tetap tetapi bentuknya mengikuti wadah.", "Gas mudah dimampatkan.",
           "Partikel zat padat tersusun sangat rapat.", "Partikel gas bergerak bebas ke segala arah.", "Bau parfum yang menyebar adalah contoh difusi.",
           "Semua zat tersusun atas partikel kecil yang selalu bergerak.", "Gas memiliki massa."],
          [("Zat cair memiliki bentuk tetap.", "Bentuk zat cair mengikuti wadahnya."), ("Partikel gas tersusun rapat.", "Partikel gas sangat renggang."),
           ("Zat padat paling mudah dimampatkan.", "Gas yang paling mudah dimampatkan."), ("Raksa berwujud gas pada suhu ruang.", "Raksa berwujud cair pada suhu ruang."),
           ("Difusi hanya terjadi pada zat padat.", "Difusi terjadi pada gas dan zat cair."), ("Partikel zat padat bergerak bebas.", "Partikel zat padat hanya bergetar.")],
          "wujud zat", "matter"),

        H("M", "perubahan-wujud-zat", "Perubahan Wujud Zat", "Perubahan Wujud",
          "Peserta didik menjelaskan perubahan wujud zat (mencair, membeku, menguap, mengembun, menyublim, mengkristal), kaitannya dengan pelepasan atau penyerapan kalor, serta contohnya dalam kehidupan sehari-hari.",
          "mencair, membeku, menguap, mengembun, menyublim, mengkristal, titik lebur, titik didih, kalor",
          "Perubahan wujud memerlukan atau melepas kalor", "Mencair, menguap, dan menyublim menyerap kalor. Membeku, mengembun, dan mengkristal melepas kalor.",
          ["Zat dapat berubah wujud jika menerima atau melepaskan kalor. Contohnya es mencair saat dipanaskan dan air membeku di freezer.",
           "Perubahan yang menyerap kalor: mencair (padat → cair), menguap (cair → gas), menyublim (padat → gas). Perubahan yang melepas kalor: membeku (cair → padat), mengembun (gas → cair), mengkristal atau deposisi (gas → padat).",
           "Air murni mencair pada 0 °C dan mendidih pada 100 °C (pada tekanan 1 atmosfer). Selama mendidih atau mencair, suhunya tetap walaupun terus dipanaskan."],
          [("Kaca jendela mobil ber-AC basah di bagian luar saat hujan. Perubahan wujud apakah ini?", ["Udara luar yang lembap menyentuh kaca dingin.", "Uap air berubah menjadi titik air."], "mengembun")],
          [("Menguap hanya terjadi saat air mendidih.", "Air dapat menguap pada suhu berapa pun, misalnya jemuran yang mengering."), ("Air membeku menyerap kalor.", "Saat membeku air melepaskan kalor."),
           ("Kapur barus yang mengecil berarti mencair.", "Kapur barus menyublim, langsung berubah dari padat menjadi gas.")],
          [("Mengapa suhu air tidak naik saat mendidih?", "Kalor yang diberikan dipakai untuk mengubah wujud air menjadi uap, bukan untuk menaikkan suhu."),
           ("Apa contoh menyublim?", "Kapur barus di lemari mengecil, es kering (dry ice) berasap, dan pengharum ruangan padat yang habis."),
           ("Mengapa embun muncul di gelas berisi es?", "Uap air di udara mendingin saat menyentuh gelas yang dingin lalu mengembun.")],
          [("Nama perubahan wujud", [("padat menjadi cair", "mencair"), ("cair menjadi padat", "membeku"), ("cair menjadi gas", "menguap"), ("gas menjadi cair", "mengembun"),
                                    ("padat menjadi gas", "menyublim"), ("gas menjadi padat", "mengkristal")],
            "Perubahan ‘{k}’ disebut ...", "Perubahan wujud apa yang terjadi saat ‘{v}’?", ("memuai", "melarut")),
           ("Contoh perubahan wujud", [("es krim meleleh di bawah matahari", "mencair"), ("lilin yang dipanaskan menjadi lunak dan cair", "mencair"), ("air di freezer menjadi es", "membeku"),
                                      ("agar-agar cair mendingin dan mengeras", "membeku"), ("pakaian basah menjadi kering", "menguap"), ("air laut di tambak garam berkurang", "menguap"),
                                      ("titik air di rumput pada pagi hari", "mengembun"), ("kaca kamar mandi berembun setelah mandi air hangat", "mengembun"), ("kapur barus di lemari mengecil", "menyublim"),
                                      ("es kering berubah menjadi gas", "menyublim"), ("terbentuk salju dari uap air di awan yang sangat dingin", "mengkristal")],
            "Peristiwa ‘{k}’ adalah contoh ...", "Manakah contoh ‘{v}’?"),
           ("Menyerap atau melepas kalor", {"perubahan yang menyerap kalor": ["mencair", "menguap", "menyublim", "es batu meleleh", "air mendidih menjadi uap", "pakaian basah mengering"],
                                           "perubahan yang melepas kalor": ["membeku", "mengembun", "mengkristal", "air menjadi es di freezer", "uap air menjadi embun", "lilin cair mengeras"]})],
          ["Mencair adalah perubahan padat menjadi cair.", "Menguap memerlukan kalor.", "Membeku melepaskan kalor.",
           "Kapur barus yang mengecil adalah contoh menyublim.", "Embun pagi terbentuk karena mengembun.", "Air murni mendidih pada 100 °C pada tekanan 1 atmosfer.",
           "Selama mendidih suhu air tetap.", "Pakaian kering karena airnya menguap."],
          [("Mengembun adalah perubahan cair menjadi gas.", "Mengembun adalah perubahan gas menjadi cair."), ("Membeku memerlukan kalor.", "Membeku melepaskan kalor."),
           ("Es mencair pada 100 °C.", "Es murni mencair pada 0 °C."), ("Kapur barus mengecil karena mencair.", "Kapur barus menyublim."),
           ("Suhu air terus naik selama mendidih.", "Suhu air tetap selama mendidih."), ("Menyublim adalah perubahan gas menjadi padat.", "Menyublim adalah perubahan padat menjadi gas.")],
          "perubahan wujud zat", "matter"),

        H("M", "perubahan-fisika-dan-kimia", "Perubahan Fisika dan Kimia", "Fisika dan Kimia",
          "Peserta didik membedakan perubahan fisika dan perubahan kimia, mengidentifikasi ciri-ciri reaksi kimia, serta memberikan contoh dalam kehidupan sehari-hari.",
          "perubahan fisika, perubahan kimia, zat baru, ciri reaksi kimia (warna, gas, suhu, endapan, bau)",
          "Perubahan kimia menghasilkan zat baru", "Perubahan fisika tidak menghasilkan zat baru, misalnya es mencair. Perubahan kimia menghasilkan zat baru, misalnya kayu terbakar.",
          ["Perubahan fisika adalah perubahan yang tidak menghasilkan zat baru. Biasanya hanya bentuk, ukuran, atau wujudnya yang berubah, misalnya kertas digunting dan gula dilarutkan.",
           "Perubahan kimia menghasilkan zat baru yang sifatnya berbeda dari zat asal, misalnya besi berkarat, nasi basi, dan kertas dibakar menjadi abu.",
           "Ciri-ciri perubahan kimia: terjadi perubahan warna, terbentuk gas, terjadi perubahan suhu, terbentuk endapan, atau timbul bau."],
          [("Cuka dicampur soda kue lalu muncul banyak gelembung. Perubahan apakah ini?", ["Gelembung menandakan terbentuk gas.", "Terbentuk zat baru, yaitu gas karbon dioksida."], "perubahan kimia")],
          [("Setiap perubahan warna pasti perubahan kimia.", "Mencampur cat merah dan putih hanya perubahan fisika."), ("Melarutkan gula adalah perubahan kimia.", "Gula masih ada dan rasa manis tetap, jadi perubahan fisika."),
           ("Es mencair menghasilkan zat baru.", "Air tetap air, jadi perubahan fisika.")],
          [("Mengapa besi berkarat termasuk perubahan kimia?", "Besi bereaksi dengan oksigen dan air menjadi karat, zat baru yang rapuh dan berwarna cokelat."),
           ("Apakah memasak telur perubahan kimia?", "Ya. Putih telur yang bening berubah menjadi putih padat dan tidak dapat kembali seperti semula."),
           ("Bagaimana mengenali perubahan fisika?", "Tidak ada zat baru, dan sering kali dapat dikembalikan, misalnya air dibekukan lalu dicairkan lagi.")],
          [("Fisika atau kimia", [("kertas digunting", "perubahan fisika"), ("es batu mencair", "perubahan fisika"), ("gula larut dalam teh", "perubahan fisika"), ("kaca pecah", "perubahan fisika"),
                                 ("lilin meleleh", "perubahan fisika"), ("garam dihaluskan", "perubahan fisika"), ("kayu terbakar", "perubahan kimia"), ("besi berkarat", "perubahan kimia"),
                                 ("nasi menjadi basi", "perubahan kimia"), ("singkong menjadi tapai", "perubahan kimia"), ("telur digoreng", "perubahan kimia"), ("susu menjadi yoghurt", "perubahan kimia")],
            "‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("perubahan biologi",)),
           ("Ciri reaksi kimia", [("soda kue dicampur cuka berbuih", "terbentuk gas"), ("tablet vitamin C berbuih di air", "terbentuk gas"), ("apel yang dipotong menjadi cokelat", "perubahan warna"),
                                 ("besi berubah menjadi cokelat kemerahan", "perubahan warna"), ("kayu terbakar terasa panas", "perubahan suhu"), ("semen dicampur air terasa hangat", "perubahan suhu"),
                                 ("air kapur ditiup dengan sedotan menjadi keruh", "terbentuk endapan"), ("telur busuk berbau menyengat", "timbul bau"), ("makanan basi berbau asam", "timbul bau")],
            "Ciri reaksi kimia pada ‘{k}’ adalah ...", "Peristiwa manakah yang menunjukkan ‘{v}’?"),
           ("Zat baru", {"menghasilkan zat baru": ["kertas menjadi abu", "kedelai menjadi tempe", "besi menjadi karat", "kayu menjadi arang", "susu menjadi keju", "gula dipanaskan menjadi karamel"],
                        "tidak menghasilkan zat baru": ["air menjadi es", "batu dipecah menjadi kerikil", "kain dijahit menjadi baju", "garam dilarutkan dalam air", "kaca dilelehkan lalu dibentuk", "kayu dipotong menjadi papan"]})],
          ["Perubahan fisika tidak menghasilkan zat baru.", "Perubahan kimia menghasilkan zat baru.", "Besi berkarat adalah perubahan kimia.",
           "Es mencair adalah perubahan fisika.", "Terbentuknya gas dapat menjadi tanda reaksi kimia.", "Nasi basi adalah contoh perubahan kimia.",
           "Melarutkan gula adalah perubahan fisika.", "Kayu terbakar menghasilkan abu dan gas."],
          [("Kertas dibakar adalah perubahan fisika.", "Kertas yang dibakar menjadi abu dan gas, jadi perubahan kimia."), ("Kaca pecah menghasilkan zat baru.", "Pecahan kaca tetap kaca, jadi perubahan fisika."),
           ("Singkong menjadi tapai adalah perubahan fisika.", "Terbentuk zat baru dengan rasa dan bau berbeda, jadi perubahan kimia."), ("Semua perubahan wujud adalah perubahan kimia.", "Perubahan wujud termasuk perubahan fisika."),
           ("Endapan tidak pernah menjadi tanda reaksi kimia.", "Terbentuknya endapan dapat menjadi tanda reaksi kimia."), ("Lilin meleleh adalah perubahan kimia.", "Lilin meleleh hanya berubah wujud, jadi perubahan fisika.")],
          "perubahan fisika dan kimia", "matter"),

        H("M", "massa-jenis", "Kerapatan Zat (Massa Jenis)", "Massa Jenis",
          "Peserta didik menjelaskan konsep massa jenis sebagai perbandingan massa dan volume, menghitung massa jenis, serta mengaitkannya dengan peristiwa terapung, melayang, dan tenggelam.",
          "massa jenis ρ = m/V, satuan g/cm³ dan kg/m³, terapung, melayang, tenggelam",
          "Massa jenis = massa ÷ volume", "Benda yang massa jenisnya lebih kecil dari air akan terapung, yang lebih besar akan tenggelam.",
          ["Massa jenis (ρ) adalah massa zat setiap satuan volume: ρ = m ÷ V. Satuannya g/cm³ atau kg/m³. Massa jenis air sekitar 1 g/cm³ atau 1.000 kg/m³.",
           "Massa jenis adalah sifat khas suatu zat. Sepotong besi kecil dan besar memiliki massa jenis yang sama, walaupun massanya berbeda.",
           "Benda terapung di air jika massa jenisnya lebih kecil dari air, melayang jika sama, dan tenggelam jika lebih besar. Minyak (0,9 g/cm³) mengapung di atas air."],
          [("Balok kayu bermassa 140 g dan bervolume 200 cm³. Berapa massa jenisnya, dan apakah terapung di air?", ["ρ = 140 ÷ 200 = 0,7 g/cm³.", "0,7 lebih kecil dari 1 g/cm³ (air)."], "0,7 g/cm³, terapung")],
          [("Benda yang lebih berat selalu tenggelam.", "Yang menentukan adalah massa jenis, misalnya kapal besi yang besar dapat terapung."), ("Paku kecil memiliki massa jenis lebih kecil dari batang besi besar.", "Massa jenis besi sama, berapa pun ukurannya."),
           ("Massa jenis dihitung dengan volume dibagi massa.", "Massa jenis = massa dibagi volume.")],
          [("Mengapa kapal dari besi dapat terapung?", "Kapal berongga berisi udara, sehingga massa jenis rata-rata kapal lebih kecil dari massa jenis air."),
           ("Berapa 1 g/cm³ dalam kg/m³?", "1 g/cm³ = 1.000 kg/m³."),
           ("Mengapa telur dapat terapung di air garam?", "Garam menaikkan massa jenis air, sehingga air garam lebih rapat daripada telur.")],
          [("Massa jenis zat", [("air", "1 g/cm³"), ("minyak goreng", "0,9 g/cm³"), ("es", "0,92 g/cm³"), ("aluminium", "2,7 g/cm³"), ("besi", "7,9 g/cm³"), ("raksa", "13,6 g/cm³"),
                               ("emas", "19,3 g/cm³"), ("gabus", "0,24 g/cm³"), ("kayu jati", "0,7 g/cm³")],
            "Massa jenis ‘{k}’ kira-kira ...", "Zat manakah yang massa jenisnya sekitar ‘{v}’?"),
           ("Terapung, melayang, atau tenggelam di air", [("gabus", "terapung"), ("kayu jati", "terapung"), ("es batu", "terapung"), ("minyak goreng", "terapung"), ("bola pingpong", "terapung"),
                                                         ("paku besi", "tenggelam"), ("batu kali", "tenggelam"), ("koin logam", "tenggelam"), ("kelereng kaca", "tenggelam"),
                                                         ("benda yang massa jenisnya sama dengan air", "melayang"), ("ikan yang mengatur gelembung renangnya", "melayang"), ("kapal selam yang tangkinya berisi air sebagian", "melayang")],
            "Jika dimasukkan ke air, ‘{k}’ akan ...", "Manakah yang ‘{v}’ di air?", ("larut",)),
           ("Istilah massa jenis", [("massa jenis", "massa setiap satuan volume"), ("terapung", "benda sebagian berada di atas permukaan zat cair"), ("melayang", "benda berada di tengah zat cair tanpa menyentuh dasar"),
                                   ("tenggelam", "benda turun sampai ke dasar zat cair"), ("gelas berpancuran", "alat untuk mengukur volume benda tak beraturan"), ("neraca", "alat untuk mengukur massa benda"),
                                   ("ρ (rho)", "lambang massa jenis")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Massa jenis adalah massa dibagi volume.", "Massa jenis air sekitar 1 g/cm³.", "Minyak terapung di atas air karena massa jenisnya lebih kecil.",
           "Besi tenggelam di air karena massa jenisnya lebih besar.", "Massa jenis suatu zat tidak bergantung pada ukurannya.", "Es terapung di air.",
           "1 g/cm³ sama dengan 1.000 kg/m³.", "Kapal besi dapat terapung karena berongga."],
          [("Benda besar selalu memiliki massa jenis besar.", "Massa jenis tidak bergantung pada ukuran benda."), ("Es tenggelam di air.", "Massa jenis es lebih kecil dari air, jadi es terapung."),
           ("Massa jenis = volume ÷ massa.", "Massa jenis = massa ÷ volume."), ("Raksa terapung di atas air.", "Raksa jauh lebih rapat daripada air, jadi tenggelam."),
           ("Air garam memiliki massa jenis lebih kecil dari air tawar.", "Air garam lebih rapat daripada air tawar."), ("1 g/cm³ sama dengan 1 kg/m³.", "1 g/cm³ sama dengan 1.000 kg/m³.")],
          "massa jenis", "matter", calc=f_massa_jenis),

        H("E", "suhu-dan-termometer", "Suhu dan Termometer", "Suhu",
          "Peserta didik menjelaskan konsep suhu, jenis termometer dan zat pengisinya, skala Celsius, Reamur, Fahrenheit, dan Kelvin, serta mengonversi suhu antarskala.",
          "suhu, termometer raksa dan alkohol, termometer klinis, skala Celsius, Reamur, Fahrenheit, Kelvin",
          "Suhu menyatakan derajat panas suatu benda", "Termometer mengukur suhu. Air membeku pada 0 °C = 32 °F = 273 K dan mendidih pada 100 °C = 212 °F = 373 K.",
          ["Suhu adalah ukuran derajat panas atau dinginnya suatu benda. Tangan tidak dapat mengukur suhu dengan tepat, jadi kita memakai termometer.",
           "Termometer zat cair memakai raksa atau alkohol karena memuai teratur saat dipanaskan. Termometer klinis dipakai untuk suhu badan, rentangnya 35–42 °C.",
           "Skala suhu: Celsius (beku 0, didih 100), Reamur (0 dan 80), Fahrenheit (32 dan 212), dan Kelvin (273 dan 373). Rumus: °F = 9/5 °C + 32, K = °C + 273, °R = 4/5 °C."],
          [("Suhu badan normal sekitar 37 °C. Berapa dalam kelvin?", ["K = °C + 273.", "37 + 273 = 310."], "310 K")],
          [("Suhu dan kalor adalah hal yang sama.", "Suhu adalah derajat panas, kalor adalah energi panas yang berpindah."), ("Kelvin dapat bernilai negatif.", "Skala kelvin dimulai dari nol mutlak, tidak ada nilai negatif."),
           ("Mengonversi °C ke °F cukup ditambah 32.", "Kalikan dulu dengan 9/5, baru ditambah 32.")],
          [("Mengapa raksa dipakai di termometer?", "Raksa mudah dilihat karena mengilap, memuai teratur, dan tidak membasahi dinding kaca. Namun raksa beracun, sehingga kini banyak termometer digital."),
           ("Apa itu nol mutlak?", "Suhu terendah yang mungkin, yaitu 0 K atau −273 °C."),
           ("Kapan termometer alkohol dipakai?", "Untuk mengukur suhu yang sangat rendah karena alkohol membeku pada suhu sekitar −114 °C.")],
          [("Titik tetap skala suhu", [("titik beku air dalam Celsius", "0 °C"), ("titik didih air dalam Celsius", "100 °C"), ("titik beku air dalam Fahrenheit", "32 °F"),
                                      ("titik didih air dalam Fahrenheit", "212 °F"), ("titik beku air dalam kelvin", "273 K"), ("titik didih air dalam kelvin", "373 K"),
                                      ("titik beku air dalam Reamur", "0 °R"), ("titik didih air dalam Reamur", "80 °R")],
            "Berapa ‘{k}’?", None),
           ("Raksa atau alkohol", {"kelebihan raksa sebagai pengisi termometer": ["mengilap sehingga mudah dilihat", "tidak membasahi dinding kaca", "dapat mengukur suhu tinggi sampai sekitar 357 °C", "merupakan penghantar panas yang baik",
                                                                               "cepat menyesuaikan dengan suhu benda", "titik didihnya tinggi", "pemuaiannya teratur"],
                                  "kelebihan alkohol sebagai pengisi termometer": ["dapat mengukur suhu sangat rendah sampai sekitar −114 °C", "harganya lebih murah", "tidak beracun seperti raksa", "pemuaiannya besar sehingga skalanya mudah dibaca",
                                                                                 "dapat diberi warna agar mudah dilihat", "cocok untuk mengukur suhu di daerah kutub", "mudah didapat"]}),
           ("Istilah suhu", [("suhu", "derajat panas atau dinginnya benda"), ("termometer", "alat pengukur suhu"), ("nol mutlak", "suhu terendah, 0 K"), ("titik tetap bawah", "titik beku air murni"),
                            ("titik tetap atas", "titik didih air murni"), ("kalibrasi", "menyesuaikan skala alat ukur dengan acuan"), ("termoskop", "alat sederhana yang menunjukkan perubahan suhu tanpa angka")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Suhu adalah ukuran derajat panas benda.", "Termometer dipakai untuk mengukur suhu.", "Air murni membeku pada 0 °C.",
           "Air murni mendidih pada 212 °F.", "K = °C + 273.", "Termometer klinis dipakai untuk mengukur suhu badan.",
           "Alkohol cocok untuk mengukur suhu yang sangat rendah.", "Tangan tidak dapat mengukur suhu dengan tepat."],
          [("Air mendidih pada 100 °F.", "Air mendidih pada 212 °F atau 100 °C."), ("0 K sama dengan 0 °C.", "0 K sama dengan −273 °C."),
           ("Termometer klinis dipakai untuk mengukur suhu oven.", "Termometer klinis hanya untuk suhu badan."), ("Titik didih air dalam Reamur adalah 100 °R.", "Titik didih air dalam Reamur adalah 80 °R."),
           ("Suhu dapat diukur dengan tepat memakai tangan.", "Perasaan tangan tidak tepat; gunakan termometer."), ("Raksa tidak berbahaya bagi tubuh.", "Raksa beracun, jadi termometer raksa harus ditangani hati-hati.")],
          "suhu", "energy", calc=f_suhu),

        H("E", "kalor-dan-perpindahannya", "Kalor dan Perpindahannya", "Kalor",
          "Peserta didik menjelaskan kalor sebagai energi yang berpindah karena perbedaan suhu, menghitung kalor dengan Q = m × c × ΔT, serta menjelaskan perpindahan kalor secara konduksi, konveksi, dan radiasi.",
          "kalor, kalor jenis, Q = m × c × ΔT, konduksi, konveksi, radiasi, konduktor dan isolator",
          "Kalor berpindah dari suhu tinggi ke suhu rendah", "Kalor berpindah melalui konduksi, konveksi, dan radiasi. Kalor yang diperlukan dihitung dengan Q = m × c × ΔT.",
          ["Kalor adalah energi panas yang berpindah dari benda bersuhu tinggi ke benda bersuhu rendah. Satuannya joule (J); 1 kalori = 4,2 J.",
           "Kalor yang diperlukan untuk menaikkan suhu: Q = m × c × ΔT. m adalah massa (kg), c kalor jenis (J/kg°C), dan ΔT perubahan suhu. Air memiliki kalor jenis besar, 4.200 J/kg°C.",
           "Konduksi: perpindahan kalor tanpa disertai perpindahan zat (sendok panas di gelas teh). Konveksi: disertai aliran zat (air mendidih, angin laut). Radiasi: tanpa perantara (panas matahari)."],
          [("Berapa kalor untuk menaikkan suhu 2 kg air dari 20 °C menjadi 70 °C? (c air = 4.200 J/kg°C)", ["ΔT = 70 − 20 = 50 °C.", "Q = 2 × 4.200 × 50 = 420.000 J."], "420.000 J")],
          [("Dingin adalah energi yang masuk ke tangan saat memegang es.", "Kalor dari tangan berpindah ke es, sehingga tangan terasa dingin."), ("Radiasi memerlukan udara sebagai perantara.", "Radiasi dapat terjadi tanpa perantara, misalnya panas matahari melalui ruang hampa."),
           ("ΔT adalah suhu akhir saja.", "ΔT adalah selisih suhu akhir dan suhu awal.")],
          [("Mengapa panci dibuat dari logam dengan pegangan plastik?", "Logam adalah konduktor yang menghantarkan panas ke makanan, sedangkan plastik adalah isolator yang melindungi tangan."),
           ("Apa itu angin laut?", "Pada siang hari darat lebih cepat panas, udara di atasnya naik, lalu udara dari laut bergerak ke darat. Ini contoh konveksi."),
           ("Mengapa termos dapat menjaga air tetap panas?", "Dinding termos dibuat dua lapis dengan ruang hampa dan permukaan mengilap untuk mengurangi konduksi, konveksi, dan radiasi.")],
          [("Cara perpindahan kalor", [("sendok terasa panas saat dicelupkan ke teh panas", "konduksi"), ("ujung besi yang dipanaskan merambat panas ke pegangan", "konduksi"), ("tangan memegang setrika panas", "konduksi"),
                                      ("air di panci bergerak naik turun saat dipanaskan", "konveksi"), ("angin laut pada siang hari", "konveksi"), ("asap dari cerobong naik ke atas", "konveksi"), ("AC dipasang di bagian atas ruangan", "konveksi"),
                                      ("panas matahari sampai ke bumi", "radiasi"), ("badan terasa hangat di dekat api unggun", "radiasi"), ("panas dari lampu pijar terasa di tangan", "radiasi")],
            "Peristiwa ‘{k}’ adalah contoh ...", "Manakah contoh ‘{v}’?", ("evaporasi",)),
           ("Konduktor atau isolator", [("besi", "konduktor"), ("tembaga", "konduktor"), ("aluminium", "konduktor"), ("perak", "konduktor"), ("baja", "konduktor"),
                                       ("kayu", "isolator"), ("plastik", "isolator"), ("kain wol", "isolator"), ("gabus", "isolator"), ("karet", "isolator"), ("styrofoam", "isolator")],
            "‘{k}’ termasuk ...", "Manakah yang termasuk ‘{v}’?", ("semikonduktor", "superkonduktor")),
           ("Istilah kalor", [("kalor", "energi panas yang berpindah karena perbedaan suhu"), ("kalor jenis", "kalor untuk menaikkan suhu 1 kg zat sebesar 1 °C"), ("kapasitas kalor", "kalor untuk menaikkan suhu suatu benda sebesar 1 °C"),
                             ("konduksi", "perpindahan kalor tanpa perpindahan partikel zat"), ("konveksi", "perpindahan kalor disertai aliran zat"), ("radiasi", "perpindahan kalor tanpa zat perantara"),
                             ("kalori", "satuan kalor yang setara 4,2 J"), ("isolator", "bahan yang sulit menghantarkan kalor")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Kalor berpindah dari benda bersuhu tinggi ke bersuhu rendah.", "Kalor dihitung dengan Q = m × c × ΔT.", "Satuan kalor adalah joule.",
           "Konduksi tidak disertai perpindahan zat.", "Konveksi disertai aliran zat.", "Panas matahari sampai ke bumi secara radiasi.",
           "Logam adalah konduktor kalor yang baik.", "Air memiliki kalor jenis yang besar."],
          [("Kalor berpindah dari benda dingin ke benda panas.", "Kalor berpindah dari benda panas ke benda dingin."), ("Kayu adalah konduktor kalor yang baik.", "Kayu adalah isolator."),
           ("Panas matahari sampai ke bumi secara konveksi.", "Panas matahari sampai secara radiasi."), ("Satuan kalor adalah newton.", "Satuan kalor adalah joule."),
           ("Angin laut adalah contoh konduksi.", "Angin laut adalah contoh konveksi."), ("Kalor jenis air lebih kecil daripada besi.", "Kalor jenis air (4.200 J/kg°C) jauh lebih besar daripada besi (450 J/kg°C).")],
          "kalor", "energy", calc=f_kalor),

        H("E", "pemuaian", "Pemuaian", "Pemuaian",
          "Peserta didik menjelaskan pemuaian zat padat, cair, dan gas akibat kenaikan suhu, faktor yang memengaruhi pemuaian, bimetal, serta penerapan dan cara mengatasi pemuaian dalam kehidupan.",
          "muai panjang, luas, volume, pemuaian zat cair dan gas, keping bimetal, celah sambungan rel dan jembatan",
          "Zat memuai saat dipanaskan", "Saat dipanaskan partikel bergerak lebih cepat dan saling menjauh sehingga ukuran zat bertambah.",
          ["Pemuaian adalah bertambahnya ukuran zat karena suhunya naik. Saat dipanaskan partikel bergerak lebih cepat dan jaraknya makin jauh.",
           "Zat padat dapat memuai panjang, luas, dan volume. Besarnya pemuaian bergantung pada jenis zat, panjang awal, dan kenaikan suhu. Gas memuai paling besar, lalu zat cair, lalu zat padat.",
           "Keping bimetal terdiri dari dua logam berbeda yang dilekatkan. Saat dipanaskan bimetal melengkung ke arah logam yang muainya lebih kecil. Bimetal dipakai di setrika otomatis dan alarm kebakaran."],
          [("Sambungan rel kereta api diberi celah. Mengapa?", ["Siang hari rel memuai karena panas.", "Celah memberi ruang agar rel tidak melengkung."], "agar rel tidak melengkung saat memuai")],
          [("Semua zat memuai sama besar.", "Besar pemuaian bergantung pada jenis zat."), ("Bimetal melengkung ke arah logam yang muainya lebih besar.", "Bimetal melengkung ke arah logam yang muainya lebih kecil."),
           ("Gas tidak dapat memuai.", "Gas memuai paling besar dibanding zat cair dan padat.")],
          [("Mengapa kabel listrik dipasang kendur?", "Saat malam yang dingin kabel menyusut. Jika dipasang kencang, kabel dapat putus."),
           ("Mengapa tutup botol logam mudah dibuka setelah direndam air panas?", "Tutup logam memuai lebih besar daripada botol kaca, sehingga menjadi longgar."),
           ("Mengapa ban sepeda bisa meletus di bawah terik matahari?", "Udara di dalam ban memuai karena panas, sehingga tekanannya bertambah.")],
          [("Penerapan pemuaian", [("celah pada sambungan rel kereta", "memberi ruang saat rel memuai"), ("celah pada sambungan jembatan", "mencegah jembatan retak saat memuai"), ("kabel listrik dipasang kendur", "mencegah kabel putus saat menyusut"),
                                  ("memasang ring besi panas pada roda pedati", "ring menyusut dan mencengkeram roda saat dingin"), ("bimetal pada setrika otomatis", "memutus arus saat suhu terlalu tinggi"),
                                  ("pemasangan kaca jendela diberi ruang", "mencegah kaca pecah saat memuai"), ("tutup botol logam direndam air panas", "tutup memuai sehingga mudah dibuka"),
                                  ("bimetal pada alarm kebakaran", "menyambung rangkaian bel saat suhu naik")],
            "Apa tujuan ‘{k}’?", "Penerapan apa yang bertujuan ‘{v}’?"),
           ("Jenis pemuaian", [("rel kereta bertambah panjang", "muai panjang"), ("kawat telepon bertambah panjang", "muai panjang"), ("kaca jendela bertambah luas", "muai luas"),
                              ("pelat besi bertambah luas", "muai luas"), ("bola logam bertambah besar", "muai volume"), ("air di panci meluap saat dipanaskan", "muai volume zat cair"),
                              ("raksa naik di pipa termometer", "muai volume zat cair"), ("balon mengembang di dekat api", "muai volume gas"), ("ban sepeda meletus di bawah terik matahari", "muai volume gas")],
            "Peristiwa ‘{k}’ menunjukkan ...", "Manakah contoh ‘{v}’?"),
           ("Bimetal", [("bimetal besi dan tembaga dipanaskan", "melengkung ke arah besi"), ("bimetal besi dan tembaga didinginkan", "melengkung ke arah tembaga"),
                       ("bimetal besi dan aluminium dipanaskan", "melengkung ke arah besi"), ("bimetal besi dan aluminium didinginkan", "melengkung ke arah aluminium"),
                       ("bimetal kuningan dan baja dipanaskan", "melengkung ke arah baja"), ("bimetal kuningan dan baja didinginkan", "melengkung ke arah kuningan")],
            "Apa yang terjadi jika ‘{k}’? (Besi dan baja memuai lebih kecil daripada tembaga, aluminium, dan kuningan.)", None, ("tetap lurus",))],
          ["Zat memuai jika dipanaskan.", "Gas memuai paling besar dibanding zat cair dan padat.", "Sambungan rel diberi celah karena pemuaian.",
           "Bimetal melengkung ke arah logam yang muainya lebih kecil.", "Kabel listrik dipasang kendur agar tidak putus saat menyusut.", "Besar pemuaian bergantung pada jenis zat.",
           "Termometer memanfaatkan pemuaian zat cair.", "Setrika otomatis memakai keping bimetal."],
          [("Zat menyusut jika dipanaskan.", "Zat memuai jika dipanaskan."), ("Zat padat memuai lebih besar daripada gas.", "Gas memuai paling besar."),
           ("Kabel listrik dipasang kencang agar tidak putus.", "Kabel dipasang kendur agar tidak putus saat menyusut."), ("Bimetal dibuat dari dua logam yang sama.", "Bimetal dibuat dari dua logam yang berbeda."),
           ("Pemuaian tidak bergantung pada kenaikan suhu.", "Makin besar kenaikan suhu, makin besar pemuaian."), ("Celah pada jembatan tidak berguna.", "Celah mencegah jembatan retak saat memuai.")],
          "pemuaian", "energy"),

        H("E", "gerak-lurus", "Gerak Benda", "Gerak Lurus",
          "Peserta didik menjelaskan gerak sebagai perubahan posisi terhadap titik acuan, membedakan jarak dan perpindahan, kelajuan dan kecepatan, serta gerak lurus beraturan dan berubah beraturan.",
          "titik acuan, jarak dan perpindahan, kelajuan dan kecepatan, v = s/t, GLB, GLBB, percepatan",
          "Kecepatan = jarak ÷ waktu", "Benda bergerak jika posisinya berubah terhadap titik acuan. GLB memiliki kecepatan tetap, GLBB memiliki percepatan tetap.",
          ["Benda dikatakan bergerak jika kedudukannya berubah terhadap titik acuan. Penumpang bus bergerak terhadap pohon di tepi jalan, tetapi diam terhadap sopir.",
           "Jarak adalah panjang lintasan yang ditempuh, sedangkan perpindahan adalah perubahan posisi dari awal ke akhir. Kelajuan = jarak ÷ waktu, kecepatan memperhatikan arah.",
           "Gerak lurus beraturan (GLB) memiliki kecepatan tetap. Gerak lurus berubah beraturan (GLBB) kecepatannya bertambah atau berkurang secara tetap, misalnya buah jatuh atau sepeda direm."],
          [("Rudi berjalan 3 m ke timur lalu 4 m ke barat. Berapa jarak dan perpindahannya?", ["Jarak = 3 + 4 = 7 m.", "Perpindahan = 4 − 3 = 1 m ke barat."], "jarak 7 m, perpindahan 1 m ke barat")],
          [("Jarak dan perpindahan selalu sama besar.", "Jika lintasan berbalik arah, perpindahan lebih kecil daripada jarak."), ("Benda diam tidak mungkin dikatakan bergerak.", "Diam atau bergerak bergantung pada titik acuan."),
           ("Buah jatuh adalah gerak lurus beraturan.", "Kecepatan buah jatuh makin besar, jadi GLBB dipercepat.")],
          [("Apa satuan kecepatan?", "Satuan SI kecepatan adalah m/s. Dalam kehidupan sehari-hari sering dipakai km/jam; 36 km/jam = 10 m/s."),
           ("Apa itu gerak semu?", "Gerak yang hanya tampak, misalnya pohon di tepi jalan tampak bergerak saat kita naik mobil."),
           ("Apa itu percepatan?", "Perubahan kecepatan setiap satuan waktu, satuannya m/s².")],
          [("GLB atau GLBB", [("mobil melaju dengan spidometer tetap 60 km/jam di jalan tol lurus", "GLB"), ("kereta melaju dengan kecepatan tetap di rel lurus", "GLB"), ("eskalator yang bergerak tetap", "GLB"),
                             ("buah kelapa jatuh dari pohon", "GLBB dipercepat"), ("sepeda meluncur menuruni bukit tanpa dikayuh", "GLBB dipercepat"), ("bola dilempar vertikal ke atas saat naik", "GLBB diperlambat"),
                             ("motor direm menjelang lampu merah", "GLBB diperlambat"), ("bola menggelinding naik ke bidang miring", "GLBB diperlambat"), ("pesawat mulai lepas landas di landasan", "GLBB dipercepat")],
            "Gerak ‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("gerak melingkar",)),
           ("Istilah gerak", [("titik acuan", "tempat atau benda yang dipakai sebagai patokan gerak"), ("jarak", "panjang seluruh lintasan yang ditempuh"), ("perpindahan", "perubahan posisi dari titik awal ke titik akhir"),
                             ("kelajuan", "jarak yang ditempuh setiap satuan waktu"), ("kecepatan", "perpindahan setiap satuan waktu dengan arah tertentu"), ("percepatan", "perubahan kecepatan setiap satuan waktu"),
                             ("gerak semu", "gerak yang hanya tampak padahal benda diam"), ("gerak relatif", "benda dapat bergerak terhadap satu acuan tetapi diam terhadap acuan lain")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?"),
           ("Acuan gerak", [("penumpang kereta terhadap kursinya", "diam"), ("penumpang kereta terhadap stasiun", "bergerak"), ("sopir bus terhadap penumpang di dalam bus", "diam"),
                           ("sopir bus terhadap tiang listrik di jalan", "bergerak"), ("pohon di tepi jalan terhadap tanah", "diam"), ("pohon di tepi jalan terhadap mobil yang melaju", "bergerak semu"),
                           ("bulan terhadap bumi", "bergerak"), ("matahari yang tampak terbit dan terbenam terhadap bumi", "bergerak semu")],
            "‘{k}’ dikatakan ...", None, ("berputar",))],
          ["Benda bergerak jika posisinya berubah terhadap titik acuan.", "Kecepatan memperhatikan arah gerak.", "GLB memiliki kecepatan tetap.",
           "Buah jatuh dari pohon adalah contoh GLBB dipercepat.", "Satuan SI kecepatan adalah m/s.", "Perpindahan dapat lebih kecil daripada jarak.",
           "36 km/jam sama dengan 10 m/s.", "Percepatan adalah perubahan kecepatan setiap satuan waktu."],
          [("Kelajuan memperhatikan arah gerak.", "Kecepatanlah yang memperhatikan arah; kelajuan tidak."), ("Motor yang direm mengalami GLBB dipercepat.", "Motor yang direm mengalami GLBB diperlambat."),
           ("Jarak selalu lebih kecil daripada perpindahan.", "Jarak selalu sama atau lebih besar daripada perpindahan."), ("Satuan percepatan adalah m/s.", "Satuan percepatan adalah m/s²."),
           ("Penumpang kereta selalu diam terhadap stasiun.", "Penumpang bergerak terhadap stasiun."), ("GLB memiliki percepatan yang besar.", "GLB tidak memiliki percepatan karena kecepatannya tetap.")],
          "gerak", "forces-and-motion", calc=f_gerak),

        H("E", "gaya-dan-hukum-newton", "Gaya dan Hukum Newton", "Gaya dan Hukum Newton",
          "Peserta didik menjelaskan jenis-jenis gaya, resultan gaya, massa dan berat, serta hukum I, II, dan III Newton dan penerapannya dalam kehidupan sehari-hari.",
          "gaya sentuh dan tak sentuh, resultan gaya, massa dan berat (w = m × g), hukum Newton I, II, III, F = m × a",
          "F = m × a", "Benda tetap diam atau bergerak lurus beraturan jika resultan gayanya nol. Setiap aksi menimbulkan reaksi yang sama besar dan berlawanan arah.",
          ["Gaya adalah tarikan atau dorongan, satuannya newton (N). Ada gaya sentuh (gaya otot, gaya gesek, gaya pegas) dan gaya tak sentuh (gaya gravitasi, gaya magnet, gaya listrik).",
           "Massa adalah banyaknya zat (kg) dan tetap di mana pun. Berat adalah gaya gravitasi pada benda: w = m × g. Di bumi g ≈ 10 m/s², jadi benda 50 kg beratnya 500 N.",
           "Hukum I Newton (kelembaman): benda cenderung mempertahankan keadaannya. Hukum II: F = m × a. Hukum III: gaya aksi dan reaksi sama besar dan berlawanan arah."],
          [("Saat bus mengerem mendadak, penumpang terdorong ke depan. Hukum Newton yang mana?", ["Tubuh penumpang cenderung terus bergerak ke depan.", "Kecenderungan mempertahankan keadaan adalah kelembaman."], "Hukum I Newton")],
          [("Massa dan berat adalah hal yang sama.", "Massa dalam kg dan tetap; berat adalah gaya dalam N yang bergantung pada gravitasi."), ("Benda yang bergerak selalu memerlukan gaya agar tetap bergerak.", "Tanpa gesekan, benda bergerak lurus beraturan tanpa gaya tambahan."),
           ("Gaya aksi dan reaksi bekerja pada benda yang sama.", "Gaya aksi dan reaksi bekerja pada dua benda yang berbeda.")],
          [("Mengapa berat badan di bulan lebih kecil?", "Gravitasi bulan sekitar 1/6 gravitasi bumi, sehingga berat menjadi 1/6, tetapi massa tetap sama."),
           ("Apa contoh hukum III Newton?", "Roket menyemburkan gas ke bawah dan terdorong ke atas; saat berenang tangan mendorong air ke belakang dan tubuh terdorong ke depan."),
           ("Bagaimana menghitung resultan gaya?", "Gaya searah dijumlahkan, gaya berlawanan arah dikurangkan.")],
          [("Hukum Newton yang berlaku", [("penumpang terdorong ke depan saat bus mengerem", "Hukum I Newton"), ("koin di atas kertas tetap di tempat saat kertas ditarik cepat", "Hukum I Newton"), ("penumpang terdorong ke belakang saat mobil tiba-tiba melaju", "Hukum I Newton"),
                                         ("troli kosong lebih mudah dipercepat daripada troli penuh", "Hukum II Newton"), ("bola ditendang lebih keras melaju lebih cepat", "Hukum II Newton"), ("truk bermuatan berat sulit dipercepat", "Hukum II Newton"),
                                         ("roket terdorong ke atas saat menyemburkan gas ke bawah", "Hukum III Newton"), ("perahu bergerak maju saat dayung mendorong air ke belakang", "Hukum III Newton"), ("senapan terdorong ke belakang saat ditembakkan", "Hukum III Newton")],
            "Peristiwa ‘{k}’ menunjukkan ...", "Manakah contoh ‘{v}’?", ("Hukum Archimedes",)),
           ("Gaya sentuh atau tak sentuh", [("gaya otot", "gaya sentuh"), ("gaya gesek", "gaya sentuh"), ("gaya pegas", "gaya sentuh"), ("gaya dorong angin pada layar perahu", "gaya sentuh"),
                                           ("gaya gravitasi", "gaya tak sentuh"), ("gaya magnet", "gaya tak sentuh"), ("gaya listrik statis", "gaya tak sentuh")],
            "‘{k}’ termasuk ...", "Manakah yang termasuk ‘{v}’?", ("gaya semu", "gaya kimia")),
           ("Massa dan berat", [("satuan SI massa", "kilogram"), ("satuan SI berat", "newton"), ("alat ukur massa", "neraca"), ("alat ukur berat", "neraca pegas (dinamometer)"),
                               ("besaran yang tetap di bumi dan di bulan", "massa"), ("besaran yang berubah jika gravitasi berubah", "berat"), ("rumus berat", "w = m × g"), ("percepatan gravitasi bumi", "sekitar 10 m/s²")],
            "Apa ‘{k}’?", None)],
          ["Satuan gaya adalah newton.", "Berat adalah gaya gravitasi pada benda.", "Massa benda tetap di bumi dan di bulan.",
           "Hukum II Newton dirumuskan F = m × a.", "Gaya aksi dan reaksi sama besar dan berlawanan arah.", "Gaya magnet adalah gaya tak sentuh.",
           "Gaya searah dijumlahkan untuk mencari resultan.", "Penumpang terdorong ke depan saat bus mengerem karena kelembaman."],
          [("Berat diukur dalam kilogram.", "Berat adalah gaya, satuannya newton."), ("Massa benda di bulan menjadi 1/6.", "Massa tetap; beratnya yang menjadi 1/6."),
           ("Gaya gesek adalah gaya tak sentuh.", "Gaya gesek terjadi karena permukaan bersentuhan, jadi gaya sentuh."), ("Gaya aksi dan reaksi saling meniadakan karena bekerja pada benda yang sama.", "Aksi dan reaksi bekerja pada dua benda yang berbeda."),
           ("Troli penuh lebih mudah dipercepat daripada troli kosong.", "Massa yang lebih besar memerlukan gaya lebih besar untuk dipercepat."), ("Gaya berlawanan arah dijumlahkan.", "Gaya berlawanan arah dikurangkan.")],
          "gaya dan hukum Newton", "forces-and-motion", calc=f_gaya),

        H("L", "klasifikasi-makhluk-hidup", "Karakteristik dan Klasifikasi Makhluk Hidup", "Klasifikasi Makhluk Hidup",
          "Peserta didik menjelaskan ciri-ciri makhluk hidup, tujuan klasifikasi, tingkatan takson, tata nama binomial, serta pengelompokan makhluk hidup ke dalam kingdom.",
          "ciri makhluk hidup, tujuan klasifikasi, takson, tata nama ganda (binomial nomenklatur), lima kingdom, kunci determinasi",
          "Klasifikasi memudahkan mempelajari makhluk hidup", "Makhluk hidup dikelompokkan dari kingdom sampai spesies. Nama ilmiah terdiri dari dua kata: genus dan spesies.",
          ["Ciri makhluk hidup: bernapas, bergerak, memerlukan makanan, tumbuh dan berkembang, berkembang biak, peka terhadap rangsang, mengeluarkan zat sisa, dan beradaptasi.",
           "Klasifikasi adalah pengelompokan makhluk hidup berdasarkan persamaan dan perbedaan ciri. Tingkatan takson dari besar ke kecil: kingdom, filum (divisi), kelas, ordo, famili, genus, spesies.",
           "Nama ilmiah memakai tata nama ganda: kata pertama genus (huruf besar), kata kedua penunjuk spesies (huruf kecil), ditulis miring. Contoh: Oryza sativa (padi) dan Homo sapiens (manusia)."],
          [("Nama ilmiah harimau sumatra adalah Panthera tigris sumatrae dan singa Panthera leo. Apa persamaan takson keduanya?", ["Kata pertama keduanya Panthera.", "Kata pertama nama ilmiah adalah genus."], "genus yang sama, Panthera")],
          [("Nama ilmiah boleh ditulis dengan huruf kecil semua.", "Huruf pertama genus ditulis kapital, dan nama ditulis miring."), ("Makin tinggi takson, makin banyak persamaan cirinya.", "Makin rendah takson (misalnya spesies), makin banyak persamaannya."),
           ("Jamur termasuk kingdom tumbuhan.", "Jamur termasuk kingdom Fungi karena tidak berklorofil.")],
          [("Mengapa makhluk hidup perlu diklasifikasikan?", "Agar keanekaragaman yang sangat banyak lebih mudah dipelajari, dikenali, dan dibandingkan."),
           ("Siapa pencetus tata nama ganda?", "Carolus Linnaeus, ilmuwan Swedia, pada abad ke-18."),
           ("Apa itu kunci determinasi?", "Daftar pertanyaan berpasangan tentang ciri makhluk hidup yang dipakai untuk menentukan nama atau kelompoknya.")],
          [("Kingdom makhluk hidup", [("bakteri Escherichia coli", "Monera"), ("Lactobacillus pada yoghurt", "Monera"), ("Amoeba", "Protista"), ("Paramecium", "Protista"), ("ganggang hijau Chlorella", "Protista"),
                                     ("jamur tiram", "Fungi"), ("ragi roti", "Fungi"), ("jamur tempe (Rhizopus)", "Fungi"), ("padi", "Plantae"), ("paku-pakuan", "Plantae"), ("lumut", "Plantae"),
                                     ("kucing", "Animalia"), ("ikan mas", "Animalia"), ("cacing tanah", "Animalia")],
            "‘{k}’ termasuk kingdom ...", "Manakah yang termasuk kingdom ‘{v}’?"),
           ("Urutan takson", [("kingdom", "filum atau divisi"), ("filum atau divisi", "kelas"), ("kelas", "ordo"), ("ordo", "famili"), ("famili", "genus"), ("genus", "spesies")],
            "Takson apa yang berada tepat di bawah ‘{k}’?", "Takson apa yang berada tepat di atas ‘{v}’?"),
           ("Nama ilmiah", [("padi", "Oryza sativa"), ("manusia", "Homo sapiens"), ("jagung", "Zea mays"), ("kucing", "Felis catus"), ("mangga", "Mangifera indica"), ("komodo", "Varanus komodoensis"),
                           ("kelapa", "Cocos nucifera"), ("singa", "Panthera leo"), ("orangutan sumatra", "Pongo abelii"), ("bunga bangkai raksasa", "Amorphophallus titanum")],
            "Apa nama ilmiah ‘{k}’?", "Makhluk hidup apa yang nama ilmiahnya ‘{v}’?")],
          ["Klasifikasi adalah pengelompokan makhluk hidup berdasarkan ciri.", "Spesies adalah takson terendah.", "Nama ilmiah terdiri dari dua kata.",
           "Kata pertama nama ilmiah adalah genus.", "Jamur termasuk kingdom Fungi.", "Bakteri termasuk kingdom Monera.",
           "Makhluk hidup dalam satu spesies memiliki paling banyak persamaan.", "Oryza sativa adalah nama ilmiah padi."],
          [("Kingdom adalah takson terendah.", "Kingdom adalah takson tertinggi; spesies yang terendah."), ("Nama ilmiah terdiri dari tiga kata genus.", "Nama ilmiah terdiri dari dua kata: genus dan penunjuk spesies."),
           ("Amoeba termasuk kingdom Animalia.", "Amoeba termasuk kingdom Protista."), ("Kata kedua nama ilmiah ditulis dengan huruf kapital.", "Kata kedua ditulis dengan huruf kecil."),
           ("Lumut termasuk kingdom Fungi.", "Lumut berklorofil dan termasuk kingdom Plantae."), ("Ordo berada di bawah famili.", "Famili berada di bawah ordo.")],
          "klasifikasi makhluk hidup", "living-things-and-ecosystems"),

        H("L", "ekologi-dan-interaksi", "Ekologi dan Pelestarian Lingkungan", "Ekologi",
          "Peserta didik menjelaskan pengaruh lingkungan terhadap organisme, satuan ekologi, interaksi antarkomponen ekosistem (rantai makanan, simbiosis, kompetisi, predasi), serta pengaruh manusia terhadap ekosistem.",
          "individu, populasi, komunitas, ekosistem, biosfer, simbiosis, predasi, kompetisi, aliran energi, pencemaran",
          "Semua komponen ekosistem saling bergantung", "Organisme berinteraksi melalui makan-dimakan, simbiosis, dan persaingan. Kegiatan manusia dapat menjaga atau merusak keseimbangan ini.",
          ["Satuan ekologi dari kecil ke besar: individu, populasi, komunitas, ekosistem, bioma, dan biosfer.",
           "Interaksi antarorganisme antara lain predasi (pemangsaan), kompetisi (persaingan memperebutkan makanan atau tempat), dan simbiosis (mutualisme, komensalisme, parasitisme).",
           "Energi mengalir dari matahari ke produsen, lalu ke konsumen. Pada setiap tingkat trofik sebagian besar energi hilang sebagai panas, sehingga jumlah konsumen puncak sedikit."],
          [("Rumput, kambing, dan sapi di padang yang sama memakan rumput. Interaksi apa antara kambing dan sapi?", ["Keduanya memakan makanan yang sama.", "Memperebutkan sumber daya disebut kompetisi."], "kompetisi")],
          [("Energi dalam rantai makanan bertambah pada setiap tingkat.", "Sebagian besar energi hilang sebagai panas pada setiap tingkat trofik."), ("Biosfer adalah satuan ekologi terkecil.", "Biosfer adalah satuan terbesar; individu yang terkecil."),
           ("Predasi menguntungkan kedua pihak.", "Predasi menguntungkan pemangsa dan merugikan mangsa.")],
          [("Apa itu tingkat trofik?", "Kedudukan makhluk hidup dalam rantai makanan: produsen tingkat I, herbivora tingkat II, dan seterusnya."),
           ("Apa itu biomagnifikasi?", "Penumpukan zat beracun seperti pestisida yang makin banyak pada konsumen di tingkat trofik yang lebih tinggi."),
           ("Bagaimana manusia menjaga ekosistem?", "Membuat kawasan konservasi, reboisasi, mengolah limbah, membatasi perburuan, dan memakai pupuk organik.")],
          [("Jenis interaksi", [("burung jalak memakan kutu di punggung kerbau", "mutualisme"), ("bakteri Rhizobium di bintil akar kacang", "mutualisme"), ("anggrek menempel di batang pohon", "komensalisme"),
                               ("ikan remora menempel pada ikan hiu", "komensalisme"), ("benalu pada pohon mangga", "parasitisme"), ("cacing pita di usus manusia", "parasitisme"),
                               ("singa memangsa rusa", "predasi"), ("burung hantu memangsa tikus", "predasi"), ("padi dan gulma memperebutkan unsur hara", "kompetisi"), ("dua ekor ayam jantan memperebutkan makanan", "kompetisi")],
            "Interaksi ‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("netralisme",)),
           ("Satuan ekologi", [("seekor banteng", "individu"), ("sekelompok banteng di padang rumput", "populasi"), ("banteng, rusa, rumput, dan pohon di savana", "komunitas"),
                              ("savana beserta tanah, air, udara, dan makhluk hidupnya", "ekosistem"), ("hutan hujan tropis di seluruh dunia", "bioma"), ("seluruh lapisan bumi yang dihuni makhluk hidup", "biosfer"),
                              ("sebatang pohon pinus", "individu"), ("semua ikan nila di satu kolam", "populasi")],
            "‘{k}’ termasuk satuan ekologi ...", "Manakah contoh ‘{v}’?"),
           ("Pengaruh manusia", {"kegiatan yang merusak ekosistem": ["membuang limbah ke sungai", "membakar hutan untuk lahan", "menangkap ikan dengan racun", "memakai pestisida berlebihan", "perburuan liar", "menimbun pantai untuk bangunan"],
                                "kegiatan yang menjaga ekosistem": ["reboisasi", "membuat taman nasional", "mengolah limbah di IPAL", "memakai pupuk organik", "menanam mangrove", "melepasliarkan satwa hasil penangkaran"]})],
          ["Individu adalah satuan ekologi terkecil.", "Populasi adalah kumpulan individu sejenis.", "Predasi adalah interaksi pemangsaan.",
           "Kompetisi terjadi karena memperebutkan sumber daya yang sama.", "Energi mengalir dari produsen ke konsumen.", "Sebagian energi hilang sebagai panas pada setiap tingkat trofik.",
           "Bakteri Rhizobium dan tanaman kacang bersimbiosis mutualisme.", "Pestisida berlebihan dapat merusak ekosistem."],
          [("Biosfer lebih kecil daripada ekosistem.", "Biosfer adalah satuan ekologi terbesar."), ("Benalu dan pohon adalah contoh komensalisme.", "Benalu merugikan pohon, jadi parasitisme."),
           ("Energi bertambah pada konsumen puncak.", "Energi berkurang pada setiap tingkat trofik."), ("Membakar hutan menjaga keseimbangan ekosistem.", "Membakar hutan merusak ekosistem."),
           ("Kompetisi hanya terjadi antara hewan yang berbeda jenis.", "Kompetisi juga terjadi antara individu sejenis."), ("Anggrek merugikan pohon tempatnya menempel.", "Anggrek tidak merugikan pohon, jadi komensalisme.")],
          "ekologi", "living-things-and-ecosystems"),

        H("S", "sistem-tata-surya", "Sistem Tata Surya", "Tata Surya",
          "Peserta didik menjelaskan karakteristik matahari, planet, dan benda langit lain dalam tata surya, hukum gravitasi yang menjaga orbit, serta karakteristik planet dalam dan planet luar.",
          "matahari, lapisan matahari, planet dalam dan luar, satelit, asteroid, komet, meteoroid, gravitasi dan orbit",
          "Gravitasi matahari menjaga orbit planet", "Planet dalam berbatu dan kecil, planet luar besar dan berupa gas atau es. Semua beredar mengelilingi matahari.",
          ["Matahari adalah bintang yang menghasilkan energi dari reaksi fusi hidrogen menjadi helium. Lapisan matahari antara lain inti, fotosfer, kromosfer, dan korona.",
           "Planet dalam (Merkurius, Venus, Bumi, Mars) berukuran kecil, berbatu, dan memiliki sedikit atau tanpa satelit. Planet luar (Yupiter, Saturnus, Uranus, Neptunus) berukuran besar, tersusun atas gas atau es, memiliki banyak satelit, dan bercincin.",
           "Gaya gravitasi matahari menarik planet, sedangkan gerak planet membuatnya tidak jatuh ke matahari. Akibatnya planet beredar pada orbit berbentuk elips."],
          [("Mengapa Merkurius beredar paling cepat mengelilingi matahari?", ["Merkurius paling dekat dengan matahari.", "Orbitnya paling pendek dan tarikan gravitasinya paling kuat."], "karena paling dekat dengan matahari")],
          [("Matahari adalah planet terbesar.", "Matahari adalah bintang."), ("Planet luar berbatu seperti bumi.", "Planet luar tersusun atas gas atau es."),
           ("Orbit planet berbentuk lingkaran sempurna.", "Orbit planet berbentuk elips.")],
          [("Dari mana energi matahari berasal?", "Dari reaksi fusi nuklir di intinya, saat inti hidrogen bergabung menjadi helium."),
           ("Apa itu kala revolusi?", "Waktu yang diperlukan planet untuk sekali mengelilingi matahari; bumi 365¼ hari, Yupiter sekitar 12 tahun."),
           ("Apa beda meteoroid, meteor, dan meteorit?", "Meteoroid adalah batuan di angkasa, meteor adalah meteoroid yang terbakar di atmosfer, meteorit adalah sisa yang jatuh ke bumi.")],
          [("Planet dalam atau luar", [("Merkurius", "planet dalam"), ("Venus", "planet dalam"), ("Bumi", "planet dalam"), ("Mars", "planet dalam"),
                                      ("Yupiter", "planet luar"), ("Saturnus", "planet luar"), ("Uranus", "planet luar"), ("Neptunus", "planet luar")],
            "‘{k}’ termasuk ...", "Manakah yang termasuk ‘{v}’?", ("planet kerdil", "satelit")),
           ("Lapisan dan aktivitas matahari", [("inti matahari", "tempat terjadinya reaksi fusi"), ("fotosfer", "lapisan yang tampak terang dari bumi"), ("kromosfer", "lapisan kemerahan di atas fotosfer"),
                                              ("korona", "lapisan terluar yang tampak saat gerhana matahari total"), ("bintik matahari", "daerah yang lebih dingin dan tampak gelap di fotosfer"),
                                              ("prominensa", "semburan gas berbentuk lengkung dari permukaan matahari"), ("angin matahari", "aliran partikel bermuatan dari matahari ke ruang angkasa")],
            "Apa yang dimaksud ‘{k}’?", "Bagian atau aktivitas matahari apa yang dimaksud: ‘{v}’?"),
           ("Benda langit", [("Ganymede", "satelit Yupiter"), ("Titan", "satelit Saturnus"), ("Phobos", "satelit Mars"), ("Bulan", "satelit Bumi"), ("Ceres", "planet kerdil di sabuk asteroid"),
                            ("Pluto", "planet kerdil di luar Neptunus"), ("komet Halley", "komet yang tampak dari bumi setiap sekitar 76 tahun"), ("Vesta", "asteroid besar di antara Mars dan Yupiter")],
            "‘{k}’ adalah ...", "Benda langit manakah yang merupakan ‘{v}’?")],
          ["Matahari adalah bintang pusat tata surya.", "Energi matahari berasal dari reaksi fusi.", "Planet dalam berukuran kecil dan berbatu.",
           "Planet luar memiliki banyak satelit.", "Orbit planet berbentuk elips.", "Gravitasi matahari menjaga planet tetap di orbitnya.",
           "Korona tampak saat gerhana matahari total.", "Meteor adalah meteoroid yang terbakar di atmosfer."],
          [("Mars termasuk planet luar.", "Mars termasuk planet dalam."), ("Energi matahari berasal dari pembakaran batu bara.", "Energi matahari berasal dari reaksi fusi nuklir."),
           ("Titan adalah satelit Bumi.", "Titan adalah satelit Saturnus."), ("Planet luar tidak memiliki satelit.", "Planet luar memiliki banyak satelit."),
           ("Meteorit adalah batuan yang masih di angkasa.", "Meteorit adalah sisa meteor yang jatuh ke bumi."), ("Bintik matahari lebih panas daripada sekitarnya.", "Bintik matahari lebih dingin sehingga tampak gelap.")],
          "sistem tata surya", "earth-and-space"),

        H("S", "pengaruh-gerak-bumi-dan-bulan", "Pengaruh Gerak Bumi dan Bulan", "Gerak Bumi dan Bulan",
          "Peserta didik menjelaskan pengaruh rotasi dan revolusi bumi, gerak bulan, gerhana, dan pasang surut air laut terhadap kehidupan di bumi, serta pengaruh benda langit terhadap iklim.",
          "rotasi dan revolusi bumi, kemiringan sumbu bumi, musim, fase bulan, gerhana, pasang surut, kalender",
          "Gerak bumi dan bulan memengaruhi kehidupan", "Rotasi menimbulkan siang dan malam, revolusi menimbulkan musim, dan gravitasi bulan menimbulkan pasang surut.",
          ["Rotasi bumi (sekitar 24 jam) menyebabkan siang dan malam, gerak semu harian matahari, perbedaan waktu, dan pembelokan arah angin.",
           "Revolusi bumi (sekitar 365¼ hari) dengan sumbu yang miring 23,5° menyebabkan pergantian musim di daerah subtropis, perbedaan lama siang dan malam, serta gerak semu tahunan matahari.",
           "Gravitasi bulan dan matahari menyebabkan pasang surut air laut. Pasang tertinggi (pasang purnama) terjadi saat bulan baru dan bulan purnama, ketika matahari, bumi, dan bulan segaris."],
          [("Nelayan ingin melaut saat air laut pasang tinggi. Pada fase bulan apa pasang tertinggi terjadi?", ["Pasang tertinggi terjadi jika matahari, bumi, dan bulan segaris.", "Itu terjadi saat bulan baru dan bulan purnama."], "bulan baru dan bulan purnama")],
          [("Musim di daerah subtropis terjadi karena jarak bumi ke matahari berubah.", "Musim terjadi karena kemiringan sumbu bumi saat revolusi."), ("Pasang surut disebabkan angin.", "Pasang surut disebabkan gravitasi bulan dan matahari."),
           ("Kalender hijriah berdasarkan revolusi bumi.", "Kalender hijriah berdasarkan peredaran bulan.")],
          [("Mengapa ada kalender masehi dan hijriah?", "Kalender masehi berdasarkan revolusi bumi (365 hari), sedangkan kalender hijriah berdasarkan peredaran bulan (sekitar 354 hari)."),
           ("Apa itu gerak semu tahunan matahari?", "Matahari tampak bergeser antara 23,5° LU dan 23,5° LS selama setahun karena revolusi bumi dan kemiringan sumbunya."),
           ("Mengapa gerhana tidak terjadi setiap bulan?", "Orbit bulan miring sekitar 5° terhadap orbit bumi, sehingga matahari, bumi, dan bulan jarang tepat segaris.")],
          [("Akibat gerak", [("siang dan malam", "rotasi bumi"), ("perbedaan waktu antarwilayah", "rotasi bumi"), ("pembelokan arah angin", "rotasi bumi"), ("bentuk bumi agak pepat di kutub", "rotasi bumi"),
                            ("pergantian musim di daerah subtropis", "revolusi bumi"), ("perbedaan lama siang dan malam", "revolusi bumi"), ("gerak semu tahunan matahari", "revolusi bumi"),
                            ("pasang surut air laut", "gravitasi bulan dan matahari"), ("fase bulan", "revolusi bulan")],
            "‘{k}’ disebabkan oleh ...", "Manakah akibat dari ‘{v}’?", ("gravitasi Mars",)),
           ("Pasang surut dan gerhana", [("bulan baru saat matahari, bumi, dan bulan segaris", "pasang purnama (pasang tertinggi)"), ("bulan purnama saat matahari, bumi, dan bulan segaris", "pasang purnama (pasang tertinggi)"),
                                        ("bulan kuartir pertama saat posisi membentuk sudut siku", "pasang perbani (pasang terendah)"), ("bulan kuartir ketiga saat posisi membentuk sudut siku", "pasang perbani (pasang terendah)"),
                                        ("bulan berada di antara matahari dan bumi dalam satu garis", "gerhana matahari"), ("bumi berada di antara matahari dan bulan dalam satu garis", "gerhana bulan"),
                                        ("bulan tampak kemerahan saat masuk umbra bumi", "gerhana bulan total"), ("bulan tampak lebih kecil sehingga matahari terlihat seperti cincin", "gerhana matahari cincin")],
            "Keadaan ‘{k}’ menyebabkan ...", "Kapan terjadi ‘{v}’?"),
           ("Istilah gerak benda langit", [("rotasi", "perputaran benda langit pada sumbunya"), ("revolusi", "gerak benda langit mengelilingi benda langit lain"), ("umbra", "bayangan inti yang sangat gelap"),
                                          ("penumbra", "bayangan kabur di sekitar umbra"), ("pasang purnama", "pasang naik yang sangat tinggi"), ("pasang perbani", "pasang naik yang rendah"),
                                          ("ekuinoks", "saat matahari tepat di atas khatulistiwa"), ("solstis", "saat matahari berada paling utara atau paling selatan")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Rotasi bumi menyebabkan siang dan malam.", "Revolusi bumi berlangsung sekitar 365¼ hari.", "Sumbu bumi miring sekitar 23,5°.",
           "Pasang surut disebabkan gravitasi bulan dan matahari.", "Pasang tertinggi terjadi saat bulan baru dan purnama.", "Gerhana bulan terjadi saat bulan purnama.",
           "Kalender hijriah berdasarkan peredaran bulan.", "Musim di daerah subtropis disebabkan kemiringan sumbu bumi."],
          [("Gerhana matahari terjadi saat bulan purnama.", "Gerhana matahari terjadi saat bulan baru."), ("Pasang perbani adalah pasang tertinggi.", "Pasang perbani adalah pasang terendah."),
           ("Siang dan malam disebabkan revolusi bumi.", "Siang dan malam disebabkan rotasi bumi."), ("Umbra adalah bayangan kabur.", "Umbra adalah bayangan inti yang gelap."),
           ("Kalender masehi berdasarkan peredaran bulan.", "Kalender masehi berdasarkan revolusi bumi."), ("Gerhana terjadi setiap bulan.", "Orbit bulan miring, jadi gerhana tidak terjadi setiap bulan.")],
          "gerak bumi dan bulan", "earth-and-space"),
    ]
