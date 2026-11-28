# -*- coding: utf-8 -*-
"""Indonesia / Kelas 12（Fase F, mata pelajaran pilihan Fisika, Kimia, dan Biologi）"""
from id_sci import H, nq, num, it


# ------------------------------------------------------------ Fisika
def f_listrik_statis(R):
    k = R.choice(["F", "E", "C", "seri", "W"])
    if k == "F":
        q1, q2, r = R.choice([(2, 3, 0.3), (4, 5, 0.2), (1, 9, 0.3), (6, 2, 0.6), (3, 3, 0.1)])
        F = 9e9 * q1 * q2 * 1e-12 / (r * r)
        return nq("Dua muatan %d μC dan %d μC terpisah sejauh %s m. Berapa gaya Coulomb di antara keduanya? (k = 9 × 10⁹ N·m²/C²)" % (q1, q2, num(r)), F,
                  [F * r, 9e9 * q1 * q2 * 1e-12 / r, F * 1e6], "N", "F = k q₁q₂ ÷ r² = 9 × 10⁹ × %d × 10⁻⁶ × %d × 10⁻⁶ ÷ %s² = %s N." % (q1, q2, num(r), num(F)))
    if k == "E":
        q, r = R.choice([(2, 0.3), (4, 0.2), (9, 0.3), (1, 0.1), (5, 0.5)])
        E = 9e9 * q * 1e-6 / (r * r)
        return nq("Berapa kuat medan listrik pada jarak %s m dari muatan %d μC? (k = 9 × 10⁹ N·m²/C²)" % (num(r), q), E, [E * r, 9e9 * q * 1e-6 / r, E / 1000], "N/C",
                  "E = kq ÷ r² = 9 × 10⁹ × %d × 10⁻⁶ ÷ %s² = %s N/C." % (q, num(r), num(E)))
    if k == "C":
        C = R.choice([2, 4, 5, 10, 20])
        V = R.choice([6, 9, 12, 20])
        return nq("Kapasitor %d μF dihubungkan dengan tegangan %d V. Berapa muatan yang tersimpan?" % (C, V), C * V, [C / V, V / C, C + V], "μC", "Q = C × V = %d × %d = %d μC." % (C, V, C * V))
    if k == "seri":
        a, b = R.choice([(6, 3), (4, 4), (12, 6), (10, 10), (20, 5)])
        cs = a * b / (a + b)
        return nq("Dua kapasitor %d μF dan %d μF dirangkai seri. Berapa kapasitas penggantinya?" % (a, b), cs, [a + b, (a + b) / 2 if (a + b) / 2 != cs else a * b, a * b], "μF",
                  "Seri: 1/Cs = 1/%d + 1/%d, jadi Cs = %s μF (kebalikan aturan hambatan)." % (a, b, num(cs)))
    C = R.choice([2, 4, 10])
    V = R.choice([10, 20, 50])
    W = 0.5 * C * 1e-6 * V * V
    return nq("Kapasitor %d μF diisi sampai tegangan %d V. Berapa energi yang tersimpan?" % (C, V), W, [C * 1e-6 * V * V, 0.5 * C * 1e-6 * V, W * 1e6], "J",
              "W = ½CV² = ½ × %d × 10⁻⁶ × %d² = %s J." % (C, V, num(W)))


def f_arus(R):
    k = R.choice(["ggl", "kirchhoff", "P", "paralel3"])
    if k == "ggl":
        E = R.choice([6, 9, 12, 24])
        r = R.choice([0.5, 1, 2])
        Rr = R.choice([2, 3, 5, 10])
        I = E / (Rr + r)
        return nq("Baterai bertegangan %d V dengan hambatan dalam %s Ω dihubungkan ke hambatan %d Ω. Berapa kuat arusnya?" % (E, num(r), Rr), I, [E / Rr, E / r, E * (Rr + r)], "A",
                  "I = ε ÷ (R + r) = %d ÷ (%d + %s) = %s A." % (E, Rr, num(r), num(I)))
    if k == "kirchhoff":
        a, b = R.choice([(2, 3), (1.5, 2.5), (4, 1), (0.5, 1.5), (3, 5)])
        return nq("Arus %s A dan %s A masuk ke sebuah titik cabang. Berapa arus yang keluar dari titik itu?" % (num(a), num(b)), a + b, [abs(a - b), a * b, (a + b) / 2], "A",
                  "Hukum I Kirchhoff: ΣI masuk = ΣI keluar = %s + %s = %s A." % (num(a), num(b), num(a + b)))
    if k == "P":
        V = R.choice([12, 220])
        Rr = R.choice([4, 6, 12]) if V == 12 else R.choice([44, 110, 484])
        return nq("Alat berhambatan %d Ω dipasang pada tegangan %d V. Berapa dayanya?" % (Rr, V), V * V / Rr, [V / Rr, V * Rr, V * V * Rr], "W", "P = V² ÷ R = %d² ÷ %d = %s W." % (V, Rr, num(V * V / Rr)))
    a, b, c = R.choice([(6, 6, 6), (4, 4, 2), (12, 6, 4), (3, 6, 6)])
    rp = 1 / (1 / a + 1 / b + 1 / c)
    return nq("Tiga hambatan %d Ω, %d Ω, dan %d Ω dirangkai paralel. Berapa hambatan penggantinya?" % (a, b, c), rp, [a + b + c, (a + b + c) / 3, 1 / a + 1 / b + 1 / c], "Ω",
              "1/Rp = 1/%d + 1/%d + 1/%d, jadi Rp = %s Ω." % (a, b, c, num(rp)))


def f_magnet(R):
    k = R.choice(["B", "ggl", "trafo", "F"])
    if k == "B":
        I = R.choice([5, 10, 20])
        a = R.choice([0.02, 0.05, 0.1])
        B = 2e-7 * I / a
        return nq("Kawat lurus panjang dialiri arus %d A. Berapa induksi magnet pada jarak %s m dari kawat? (μ₀ = 4π × 10⁻⁷ Wb/A·m)" % (I, num(a)), B, [2e-7 * I * a, 4e-7 * I / a, B * 1e7], "T",
                  "B = μ₀I ÷ 2πa = 2 × 10⁻⁷ × %d ÷ %s = %s T." % (I, num(a), num(B)))
    if k == "ggl":
        N = R.choice([50, 100, 200, 500])
        dp = R.choice([0.01, 0.02, 0.05])
        dt = R.choice([0.1, 0.2, 0.5])
        e = N * dp / dt
        return nq("Kumparan %d lilitan mengalami perubahan fluks magnet %s Wb dalam %s s. Berapa besar GGL induksinya?" % (N, num(dp), num(dt)), e, [dp / dt, N * dp * dt, N * dt / dp], "V",
                  "ε = N × ΔΦ ÷ Δt = %d × %s ÷ %s = %s V." % (N, num(dp), num(dt), num(e)))
    if k == "trafo":
        Vp, Np, Ns = R.choice([(220, 1000, 50), (220, 1100, 60), (110, 500, 1000), (220, 2200, 100), (12, 100, 1000)])
        Vs = Vp * Ns / Np
        return nq("Transformator memiliki %d lilitan primer dan %d lilitan sekunder. Jika tegangan primer %d V, berapa tegangan sekundernya?" % (Np, Ns, Vp), Vs, [Vp * Np / Ns, Vp, Vp * Ns], "V",
                  "Vs = Vp × Ns ÷ Np = %d × %d ÷ %d = %s V." % (Vp, Ns, Np, num(Vs)))
    B = R.choice([0.1, 0.2, 0.5])
    I = R.choice([2, 4, 5])
    L = R.choice([0.5, 1, 2])
    return nq("Kawat sepanjang %s m berarus %d A berada tegak lurus di dalam medan magnet %s T. Berapa gaya Lorentz pada kawat?" % (num(L), I, num(B)), B * I * L, [B * I / L, B * L, I * L / B], "N",
              "F = B × I × L = %s × %d × %s = %s N." % (num(B), I, num(L), num(B * I * L)))


def f_gem(R):
    k = R.choice(["f", "lam", "E", "fe"])
    c = 3e8
    if k == "f":
        lam = R.choice([1, 2, 3, 6, 10, 300])
        return nq("Gelombang radio memiliki panjang gelombang %s m. Berapa frekuensinya? (c = 3 × 10⁸ m/s)" % num(lam), c / lam, [c * lam, lam / c, c / lam / 1000], "Hz", "f = c ÷ λ = 3 × 10⁸ ÷ %s = %s Hz." % (num(lam), num(c / lam)))
    if k == "lam":
        f = R.choice([1e8, 1.5e8, 3e9, 6e14, 1e6])
        return nq("Gelombang elektromagnetik berfrekuensi %s Hz. Berapa panjang gelombangnya? (c = 3 × 10⁸ m/s)" % num(f), c / f, [c * f, f / c, c / f * 100], "m", "λ = c ÷ f = 3 × 10⁸ ÷ %s = %s m." % (num(f), num(c / f)))
    if k == "E":
        f = R.choice([4e14, 5e14, 6e14, 1e15])
        E = 6.6e-34 * f
        return nq("Berapa energi satu foton cahaya berfrekuensi %s Hz? (h = 6,6 × 10⁻³⁴ J·s)" % num(f), E, [6.6e-34 / f, E * 10, f / 6.6e-34], "J", "E = hf = 6,6 × 10⁻³⁴ × %s = %s J." % (num(f), num(E)))
    hf, w = R.choice([(4, 2.3), (5, 2.1), (3.5, 1.8), (6, 4.3), (4.5, 2.5)])
    return nq("Cahaya dengan energi foton %s eV menyinari logam berfungsi kerja %s eV. Berapa energi kinetik maksimum elektron yang terlepas?" % (num(hf), num(w)), hf - w, [hf + w, hf, hf / w], "eV",
              "Ek = hf − W₀ = %s − %s = %s eV." % (num(hf), num(w), num(hf - w)))


def f_inti(R):
    k = R.choice(["sisa", "T", "persen", "nukleon"])
    if k == "sisa":
        N0 = R.choice([80, 160, 200, 320, 640])
        T = R.choice([2, 5, 8, 10])
        n = R.choice([1, 2, 3, 4])
        return nq("Zat radioaktif bermassa %d g memiliki waktu paruh %d hari. Berapa massa yang tersisa setelah %d hari?" % (N0, T, n * T), N0 / 2 ** n, [N0 / (2 * n), N0 - N0 / 2 ** n, N0 / 2], "g",
                  "Setelah %d kali waktu paruh: %d × (½)^%d = %s g." % (n, N0, n, num(N0 / 2 ** n)))
    if k == "T":
        n = R.choice([2, 3, 4])
        T = R.choice([3, 5, 6, 8])
        return nq("Aktivitas suatu zat radioaktif tinggal 1/%d dari semula setelah %d jam. Berapa waktu paruhnya?" % (2 ** n, n * T), T, [n * T, n * T / 2 ** n, n * T * 2], "jam",
                  "1/%d = (½)^%d, berarti %d kali waktu paruh dalam %d jam, jadi T = %d jam." % (2 ** n, n, n, n * T, T))
    if k == "persen":
        n = R.choice([1, 2, 3])
        return nq("Berapa persen zat radioaktif yang tersisa setelah %d kali waktu paruh?" % n, 100 / 2 ** n, [100 - 100 / 2 ** n, 100 / (2 * n), 50 * n], "%", "Sisa = (½)^%d × 100%% = %s%%." % (n, num(100 / 2 ** n)))
    z, a, nm = R.choice([(6, 14, "karbon-14"), (92, 235, "uranium-235"), (88, 226, "radium-226"), (19, 40, "kalium-40"), (53, 131, "iodin-131"), (27, 60, "kobalt-60")])
    return nq("Berapa jumlah neutron dalam inti %s (nomor atom %d)?" % (nm, z), a - z, [a, z, a + z], "", "Neutron = A − Z = %d − %d = %d." % (a, z, a - z))


# ------------------------------------------------------------ Kimia
def f_ph(R):
    k = R.choice(["kuat", "basa", "h2so4", "h"])
    if k == "kuat":
        n = R.choice([1, 2, 3, 4])
        acid = R.choice(["HCl", "HNO₃"])
        return nq("Berapa pH larutan %s 10⁻%s M?" % (acid, str(n).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))), n, [14 - n, n + 1, -n + 7 if n != 7 - n else n + 2], "",
                  "Asam kuat: [H⁺] = 10⁻%d M, jadi pH = %d." % (n, n)) if False else nq("Berapa pH larutan %s %s M?" % (acid, num(10 ** -n)), n, [14 - n, n + 1, 7 + n if 7 + n != 14 - n else n + 2], "",
                                                                                     "Asam kuat: [H⁺] = %s M = 10⁻%s M, jadi pH = %d." % (num(10 ** -n), str(n).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")), n))
    if k == "basa":
        n = R.choice([1, 2, 3, 4])
        base = R.choice(["NaOH", "KOH"])
        return nq("Berapa pH larutan %s %s M?" % (base, num(10 ** -n)), 14 - n, [n, 7 - n if n < 7 else n + 1, 14 + n], "", "[OH⁻] = %s M, pOH = %d, pH = 14 − %d = %d." % (num(10 ** -n), n, n, 14 - n))
    if k == "h2so4":
        c, ph = R.choice([(0.05, 1), (0.005, 2), (0.0005, 3)])
        return nq("Berapa pH larutan H₂SO₄ %s M (terionisasi sempurna)?" % num(c), ph, [ph + 0.301, ph + 1, 14 - ph], "", "[H⁺] = 2 × %s = %s M, jadi pH = %d." % (num(c), num(2 * c), ph))
    ph = R.choice([2, 3, 5, 9, 11, 12])
    return nq("Suatu larutan memiliki pH %d. Berapa pOH-nya?" % ph, 14 - ph, [ph, ph + 7 if ph + 7 != 14 - ph else ph + 1, 7], "", "pH + pOH = 14, jadi pOH = 14 − %d = %d." % (ph, 14 - ph))


def f_koligatif(R):
    k = R.choice(["Tb", "Tf", "m", "elektrolit"])
    zat, mr, g = R.choice([("glukosa", 180, 18), ("glukosa", 180, 36), ("urea", 60, 6), ("urea", 60, 12), ("sukrosa", 342, 34.2)])
    p = R.choice([250, 500, 1000])
    m = g / mr * 1000 / p
    if k == "m":
        return nq("Sebanyak %s g %s (Mr = %d) dilarutkan dalam %d g air. Berapa molalitas larutan?" % (num(g), zat, mr, p), m, [g / mr, g / mr * p / 1000, m * 10], "m", "m = (%s ÷ %d) × (1.000 ÷ %d) = %s molal." % (num(g), mr, p, num(m)))
    if k == "Tb":
        dt = 0.52 * m
        return nq("Sebanyak %s g %s (Mr = %d) dilarutkan dalam %d g air. Berapa kenaikan titik didihnya? (Kb air = 0,52 °C/m)" % (num(g), zat, mr, p), dt, [0.52 * g / mr, dt + 100, 1.86 * m], "°C",
                  "ΔTb = Kb × m = 0,52 × %s = %s °C." % (num(m), num(dt)))
    if k == "Tf":
        dt = 1.86 * m
        return nq("Sebanyak %s g %s (Mr = %d) dilarutkan dalam %d g air. Berapa penurunan titik bekunya? (Kf air = 1,86 °C/m)" % (num(g), zat, mr, p), dt, [1.86 * g / mr, 0.52 * m, dt * 2], "°C",
                  "ΔTf = Kf × m = 1,86 × %s = %s °C." % (num(m), num(dt)))
    mm = R.choice([0.1, 0.2, 0.5])
    return nq("Larutan NaCl %s m terionisasi sempurna (i = 2). Berapa penurunan titik bekunya? (Kf air = 1,86 °C/m)" % num(mm), 1.86 * mm * 2, [1.86 * mm, 0.52 * mm * 2, 1.86 * mm * 3], "°C",
              "ΔTf = Kf × m × i = 1,86 × %s × 2 = %s °C." % (num(mm), num(1.86 * mm * 2)))


EO = {"Mg": -2.37, "Al": -1.66, "Zn": -0.76, "Fe": -0.44, "Ni": -0.25, "Pb": -0.13, "Cu": 0.34, "Ag": 0.80}


def f_volta(R):
    a, b = R.sample(sorted(EO), 2)
    if EO[a] > EO[b]:
        a, b = b, a
    e = EO[b] - EO[a]
    if R.random() < 0.6:
        return nq("Sel Volta tersusun atas elektrode %s (E° = %s V) dan %s (E° = %s V). Berapa potensial sel standarnya?" % (a, num(EO[a]), b, num(EO[b])), e,
                  [abs(EO[a] + EO[b]), abs(EO[a]), EO[b] + 1], "V", "E°sel = E°katode − E°anode = %s − (%s) = %s V." % (num(EO[b]), num(EO[a]), num(e)))
    return it("Pada sel Volta dengan elektrode %s (E° = %s V) dan %s (E° = %s V), logam mana yang menjadi anode?" % (a, num(EO[a]), b, num(EO[b])), "%s (mengalami oksidasi)" % a,
              ["%s (mengalami oksidasi)" % b, "%s (mengalami reduksi)" % a, "keduanya menjadi katode"], "Logam dengan E° lebih kecil (%s) mudah teroksidasi dan menjadi anode." % a)


def UNITS(g):
    return [
        H("F", "listrik-statis-dan-kapasitor", "Listrik Statis dan Kapasitor", "Listrik Statis",
          "Peserta didik menerapkan hukum Coulomb, medan listrik, potensial listrik, dan kapasitor (kapasitas, rangkaian seri-paralel, energi) dalam menyelesaikan masalah.",
          "hukum Coulomb F = kq₁q₂/r², medan listrik E = kq/r², potensial listrik, kapasitor C = Q/V, kapasitor seri dan paralel, energi kapasitor",
          "Gaya Coulomb berbanding terbalik dengan kuadrat jarak", "Jika jarak dua muatan dijadikan dua kali, gayanya menjadi seperempat.",
          ["Hukum Coulomb: F = k q₁q₂ ÷ r² dengan k = 9 × 10⁹ N·m²/C². Muatan sejenis tolak-menolak, muatan berbeda tarik-menarik.",
           "Medan listrik adalah gaya per satuan muatan uji: E = F/q = kq/r². Arah medan keluar dari muatan positif dan masuk ke muatan negatif. Potensial listrik V = kq/r.",
           "Kapasitor menyimpan muatan: C = Q/V (farad). Kapasitor paralel dijumlahkan (Cp = C₁ + C₂), kapasitor seri: 1/Cs = 1/C₁ + 1/C₂. Energi kapasitor W = ½CV²."],
          [("Gaya antara dua muatan 8 N. Jika jaraknya dijadikan dua kali, berapa gayanya?", ["F sebanding 1/r².", "r menjadi 2r → F menjadi 1/4."], "2 N")],
          [("Gaya Coulomb berbanding terbalik dengan jarak.", "Gaya Coulomb berbanding terbalik dengan kuadrat jarak."), ("Kapasitor seri dijumlahkan langsung.", "Kapasitor paralel yang dijumlahkan langsung; seri memakai kebalikan."),
           ("Medan listrik masuk ke muatan positif.", "Medan listrik keluar dari muatan positif.")],
          [("Di mana kapasitor dipakai?", "Pada lampu kilat kamera, perata arus pada adaptor, penyimpan memori, dan rangkaian penala radio."),
           ("Apa satuan kapasitas?", "Farad (F). Kapasitor sehari-hari biasanya dalam mikrofarad (μF) atau pikofarad (pF)."),
           ("Apa itu bidang ekuipotensial?", "Bidang yang semua titiknya memiliki potensial sama, sehingga memindahkan muatan di atasnya tidak memerlukan usaha.")],
          [("Besaran listrik statis", [("gaya Coulomb", "F = kq₁q₂/r²"), ("kuat medan listrik", "E = kq/r²"), ("potensial listrik", "V = kq/r"), ("energi potensial listrik", "Ep = kq₁q₂/r"),
                                      ("kapasitas kapasitor", "C = Q/V"), ("energi kapasitor", "W = ½CV²"), ("kapasitor paralel", "Cp = C₁ + C₂"), ("kapasitor seri", "1/Cs = 1/C₁ + 1/C₂")],
            "Rumus apa untuk ‘{k}’?", "Rumus ‘{v}’ menyatakan ...", ("F = ma",)),
           ("Perubahan gaya Coulomb", [("jarak dijadikan 2 kali", "gaya menjadi 1/4 kali"), ("jarak dijadikan 3 kali", "gaya menjadi 1/9 kali"), ("jarak dijadikan 1/2 kali", "gaya menjadi 4 kali"),
                                      ("salah satu muatan dijadikan 2 kali", "gaya menjadi 2 kali"), ("kedua muatan dijadikan 2 kali", "gaya menjadi 4 kali"), ("kedua muatan dan jarak dijadikan 2 kali", "gaya tetap"),
                                      ("salah satu muatan dijadikan 3 kali", "gaya menjadi 3 kali")],
            "Jika ‘{k}’, bagaimana gaya Coulombnya?", None),
           ("Istilah listrik statis", [("medan listrik", "daerah di sekitar muatan yang masih dipengaruhi gaya listrik"), ("garis gaya listrik", "garis khayal yang keluar dari muatan positif"), ("potensial listrik", "energi potensial per satuan muatan"),
                                      ("kapasitor", "komponen penyimpan muatan listrik"), ("dielektrik", "bahan isolator di antara keping kapasitor"), ("farad", "satuan kapasitas kapasitor"), ("hukum Gauss", "fluks listrik sebanding dengan muatan yang dilingkupi")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Muatan sejenis tolak-menolak.", "Gaya Coulomb berbanding terbalik dengan kuadrat jarak.", "Medan listrik keluar dari muatan positif.",
           "Kapasitor menyimpan muatan listrik.", "Kapasitor paralel dijumlahkan langsung.", "Energi kapasitor W = ½CV².",
           "Satuan kapasitas adalah farad.", "Bahan dielektrik memperbesar kapasitas kapasitor."],
          [("Gaya Coulomb sebanding dengan jarak.", "Gaya Coulomb berbanding terbalik dengan kuadrat jarak."), ("Kapasitor seri dijumlahkan langsung.", "Kapasitor seri memakai rumus kebalikan."),
           ("Satuan kapasitas adalah ohm.", "Satuan kapasitas adalah farad."), ("Jarak dua kali membuat gaya setengah.", "Jarak dua kali membuat gaya seperempat."),
           ("Medan listrik masuk ke muatan positif.", "Medan listrik keluar dari muatan positif."), ("Energi kapasitor W = CV.", "Energi kapasitor W = ½CV².")],
          "listrik statis", "energy", calc=f_listrik_statis),

        H("F", "rangkaian-arus-searah", "Rangkaian Arus Searah", "Arus Searah",
          "Peserta didik menganalisis rangkaian arus searah: kuat arus, hambatan jenis, hukum Ohm, hukum I dan II Kirchhoff, GGL dan hambatan dalam, rangkaian seri-paralel, serta energi dan daya listrik.",
          "arus listrik, hambatan jenis R = ρL/A, hukum Ohm, hukum Kirchhoff, GGL dan hambatan dalam, rangkaian seri dan paralel, daya listrik",
          "Arus yang masuk titik cabang = arus yang keluar", "Hukum I Kirchhoff tentang titik cabang, hukum II Kirchhoff tentang jumlah tegangan pada loop tertutup.",
          ["Kuat arus I = Q/t (ampere). Hambatan kawat R = ρL/A: makin panjang dan makin kecil penampang, hambatannya makin besar. Hukum Ohm V = IR.",
           "Hukum I Kirchhoff: jumlah arus masuk titik cabang sama dengan jumlah arus keluar. Hukum II Kirchhoff: dalam loop tertutup, jumlah GGL sama dengan jumlah penurunan tegangan (Σε = ΣIR).",
           "Sumber tegangan memiliki hambatan dalam r, sehingga I = ε/(R + r) dan tegangan jepit V = ε − Ir. Daya listrik P = VI = I²R = V²/R."],
          [("Baterai 12 V dengan hambatan dalam 1 Ω dihubungkan ke hambatan 5 Ω. Berapa tegangan jepitnya?", ["I = 12 ÷ (5 + 1) = 2 A.", "V = ε − Ir = 12 − 2 × 1 = 10 V."], "10 V")],
          [("Tegangan jepit sama dengan GGL.", "Tegangan jepit lebih kecil karena ada penurunan tegangan pada hambatan dalam."), ("Kawat yang lebih tebal hambatannya lebih besar.", "Kawat lebih tebal (A besar) hambatannya lebih kecil."),
           ("Pada titik cabang arus dapat hilang.", "Arus yang masuk sama dengan arus yang keluar (kekekalan muatan).")],
          [("Apa itu hambatan jenis?", "Sifat khas bahan dalam menghambat arus; tembaga memiliki hambatan jenis kecil sehingga dipakai untuk kabel."),
           ("Mengapa baterai yang lama tegangannya turun?", "Hambatan dalamnya makin besar sehingga tegangan jepit saat dipakai makin kecil."),
           ("Bagaimana amperemeter dan voltmeter dipasang?", "Amperemeter dipasang seri dan berhambatan sangat kecil; voltmeter dipasang paralel dan berhambatan sangat besar.")],
          [("Hukum dan rumus", [("jumlah arus masuk titik cabang sama dengan arus keluar", "hukum I Kirchhoff"), ("jumlah GGL dalam loop sama dengan jumlah IR", "hukum II Kirchhoff"), ("V = IR", "hukum Ohm"),
                               ("R = ρL/A", "hambatan kawat"), ("I = ε/(R + r)", "arus pada rangkaian dengan hambatan dalam"), ("V = ε − Ir", "tegangan jepit"), ("P = V²/R", "daya listrik"), ("I = Q/t", "kuat arus")],
            "‘{k}’ menyatakan ...", "Bagaimana rumus atau pernyataan ‘{v}’?"),
           ("Faktor hambatan kawat", [("panjang kawat dijadikan 2 kali", "hambatan menjadi 2 kali"), ("luas penampang dijadikan 2 kali", "hambatan menjadi 1/2 kali"), ("diameter kawat dijadikan 2 kali", "hambatan menjadi 1/4 kali"),
                                     ("panjang dan luas penampang dijadikan 2 kali", "hambatan tetap"), ("kawat diganti bahan berhambatan jenis 3 kali", "hambatan menjadi 3 kali"), ("panjang kawat dijadikan 1/2 kali", "hambatan menjadi 1/2 kali")],
            "Bagaimana hambatan kawat jika ‘{k}’?", None, ("hambatan menjadi 4 kali", "hambatan menjadi nol")),
           ("Alat ukur listrik", [("amperemeter", "dipasang seri dan berhambatan sangat kecil"), ("voltmeter", "dipasang paralel dan berhambatan sangat besar"), ("ohmmeter", "mengukur hambatan tanpa arus dari rangkaian"),
                                 ("multimeter", "mengukur arus, tegangan, dan hambatan"), ("galvanometer", "mendeteksi arus listrik yang sangat kecil"), ("hambatan shunt", "dipasang paralel untuk memperbesar batas ukur amperemeter"),
                                 ("hambatan muka", "dipasang seri untuk memperbesar batas ukur voltmeter")],
            "Apa ciri atau fungsi ‘{k}’?", "Alat atau komponen apa yang ‘{v}’?")],
          ["Hukum I Kirchhoff berkaitan dengan titik cabang.", "Hukum II Kirchhoff berlaku pada loop tertutup.", "R = ρL/A.",
           "Kawat yang lebih panjang hambatannya lebih besar.", "Tegangan jepit lebih kecil daripada GGL saat ada arus.", "Amperemeter dipasang seri.",
           "Voltmeter dipasang paralel.", "P = I²R."],
          [("Voltmeter dipasang seri.", "Voltmeter dipasang paralel."), ("Kawat yang lebih panjang hambatannya lebih kecil.", "Kawat yang lebih panjang hambatannya lebih besar."),
           ("Hambatan shunt dipasang seri pada amperemeter.", "Hambatan shunt dipasang paralel."), ("Tegangan jepit selalu lebih besar dari GGL saat baterai dipakai.", "Tegangan jepit lebih kecil dari GGL."),
           ("Arus yang masuk titik cabang lebih besar dari yang keluar.", "Arus masuk sama dengan arus keluar."), ("Diameter dua kali membuat hambatan dua kali.", "Diameter dua kali membuat hambatan seperempat.")],
          "rangkaian arus searah", "energy", calc=f_arus),

        H("F", "medan-magnet-dan-induksi-elektromagnetik", "Medan Magnet dan Induksi Elektromagnetik", "Induksi Elektromagnetik",
          "Peserta didik menjelaskan medan magnet di sekitar kawat berarus, gaya Lorentz, induksi elektromagnetik (hukum Faraday dan Lenz), generator, transformator, serta arus bolak-balik.",
          "induksi magnet kawat lurus, kawat melingkar, solenoida, gaya Lorentz F = BIL, fluks magnet, hukum Faraday, hukum Lenz, generator AC, transformator",
          "Perubahan fluks magnet menimbulkan GGL induksi", "Makin banyak lilitan dan makin cepat perubahan fluks, makin besar GGL induksi (hukum Faraday).",
          ["Kawat berarus menimbulkan medan magnet. Untuk kawat lurus panjang B = μ₀I/(2πa), dengan arah sesuai kaidah tangan kanan. Kawat berarus dalam medan magnet mengalami gaya Lorentz F = BIL sin θ.",
           "Fluks magnet Φ = BA cos θ. Hukum Faraday: GGL induksi ε = −N ΔΦ/Δt. Hukum Lenz: arus induksi menimbulkan medan magnet yang melawan perubahan fluks penyebabnya.",
           "Generator mengubah energi gerak menjadi energi listrik bolak-balik. Transformator mengubah tegangan AC: Vs/Vp = Ns/Np. Pada trafo ideal daya primer sama dengan daya sekunder."],
          [("Kumparan 200 lilitan mengalami perubahan fluks 0,03 Wb dalam 0,1 s. Berapa GGL induksinya?", ["ε = N ΔΦ/Δt.", "ε = 200 × 0,03 ÷ 0,1 = 60 V."], "60 V")],
          [("GGL induksi timbul pada magnet yang diam di dalam kumparan.", "GGL induksi hanya timbul jika fluks berubah."), ("Trafo dapat menaikkan daya listrik.", "Trafo ideal tidak menambah daya; tegangan naik, arus turun."),
           ("Gaya Lorentz terbesar saat kawat sejajar medan magnet.", "Gaya Lorentz terbesar saat kawat tegak lurus medan (sin 90° = 1).")],
          [("Apa tanda negatif pada hukum Faraday?", "Menunjukkan hukum Lenz: GGL induksi melawan perubahan fluks yang menyebabkannya."),
           ("Apa itu efisiensi transformator?", "Perbandingan daya sekunder dengan daya primer. Trafo nyata kehilangan sebagian energi sebagai panas."),
           ("Bagaimana kompor induksi bekerja?", "Medan magnet bolak-balik menimbulkan arus pusar di dasar panci logam sehingga panci menjadi panas.")],
          [("Rumus kemagnetan", [("induksi magnet kawat lurus panjang", "B = μ₀I/(2πa)"), ("induksi magnet di pusat kawat melingkar", "B = μ₀I/(2a)"), ("induksi magnet di tengah solenoida", "B = μ₀IN/L"),
                                ("gaya Lorentz pada kawat berarus", "F = BIL sin θ"), ("gaya Lorentz pada muatan bergerak", "F = qvB sin θ"), ("fluks magnet", "Φ = BA cos θ"), ("GGL induksi", "ε = −N ΔΦ/Δt"), ("transformator", "Vs/Vp = Ns/Np")],
            "Rumus apa untuk ‘{k}’?", "Rumus ‘{v}’ menyatakan ..."),
           ("Faktor GGL induksi", [("jumlah lilitan diperbanyak", "GGL induksi bertambah"), ("magnet digerakkan lebih cepat", "GGL induksi bertambah"), ("magnet yang lebih kuat dipakai", "GGL induksi bertambah"),
                                  ("magnet diam di dalam kumparan", "tidak ada GGL induksi"), ("kumparan dan magnet bergerak bersama dengan kecepatan sama", "tidak ada GGL induksi"), ("magnet digerakkan lebih lambat", "GGL induksi berkurang"),
                                  ("lilitan dikurangi", "GGL induksi berkurang")],
            "Bagaimana GGL induksi jika ‘{k}’?", None, ("GGL induksi berubah arah menjadi DC",)),
           ("Penerapan induksi", [("generator PLTA", "mengubah energi gerak menjadi energi listrik"), ("dinamo sepeda", "mengubah energi gerak roda menjadi listrik lampu"), ("transformator", "mengubah besar tegangan AC"),
                                 ("kompor induksi", "memanaskan panci dengan arus pusar"), ("pengisi daya nirkabel ponsel", "memindahkan energi dengan induksi antarkumparan"), ("motor listrik", "mengubah energi listrik menjadi gerak dengan gaya Lorentz"),
                                 ("detektor logam di bandara", "mendeteksi logam dari perubahan medan magnet")],
            "Apa fungsi ‘{k}’?", "Alat apa yang ‘{v}’?")],
          ["Kawat berarus menimbulkan medan magnet.", "Gaya Lorentz F = BIL sin θ.", "GGL induksi timbul jika fluks magnet berubah.",
           "Makin banyak lilitan, makin besar GGL induksi.", "Hukum Lenz menyatakan arus induksi melawan perubahan fluks.", "Generator menghasilkan arus bolak-balik.",
           "Vs/Vp = Ns/Np pada transformator.", "Trafo ideal tidak mengubah daya."],
          [("Magnet diam di dalam kumparan menghasilkan GGL induksi.", "Perlu perubahan fluks untuk GGL induksi."), ("Trafo dapat bekerja dengan arus searah.", "Trafo memerlukan arus bolak-balik."),
           ("Gaya Lorentz terbesar saat kawat sejajar medan.", "Gaya Lorentz terbesar saat kawat tegak lurus medan."), ("Generator mengubah energi listrik menjadi gerak.", "Generator mengubah energi gerak menjadi listrik."),
           ("Hukum Lenz menyatakan arus induksi memperkuat perubahan fluks.", "Arus induksi melawan perubahan fluks."), ("Induksi magnet makin besar saat menjauhi kawat.", "Induksi magnet makin kecil saat menjauhi kawat.")],
          "medan magnet dan induksi elektromagnetik", "energy", calc=f_magnet),

        H("F", "gelombang-elektromagnetik", "Gelombang Elektromagnetik", "Gelombang Elektromagnetik",
          "Peserta didik menjelaskan sifat gelombang elektromagnetik, spektrum elektromagnetik dari gelombang radio hingga sinar gamma, pemanfaatan dan bahayanya, serta hubungan c = λf.",
          "sifat gelombang elektromagnetik, spektrum (radio, mikro, inframerah, cahaya tampak, ultraviolet, sinar X, gamma), c = λf, pemanfaatan dan bahaya radiasi",
          "Gelombang elektromagnetik merambat secepat cahaya", "Makin kecil panjang gelombang, makin besar frekuensi dan energinya.",
          ["Gelombang elektromagnetik adalah gelombang transversal yang terdiri dari medan listrik dan medan magnet yang saling tegak lurus. Gelombang ini tidak memerlukan medium dan di ruang hampa merambat dengan c = 3 × 10⁸ m/s.",
           "Urutan spektrum dari frekuensi terkecil: gelombang radio, gelombang mikro, inframerah, cahaya tampak, ultraviolet, sinar X, sinar gamma. Rumus c = λf.",
           "Gelombang radio untuk siaran, gelombang mikro untuk radar dan oven, inframerah untuk remote dan kamera termal, ultraviolet untuk sterilisasi, sinar X untuk rontgen, sinar gamma untuk terapi kanker. Radiasi berenergi tinggi dapat merusak sel."],
          [("Berapa panjang gelombang radio FM 100 MHz? (c = 3 × 10⁸ m/s)", ["λ = c ÷ f.", "λ = 3 × 10⁸ ÷ 10⁸ = 3 m."], "3 m")],
          [("Gelombang elektromagnetik memerlukan medium.", "Gelombang elektromagnetik dapat merambat di ruang hampa."), ("Sinar gamma memiliki frekuensi terkecil.", "Sinar gamma memiliki frekuensi terbesar."),
           ("Cahaya tampak berbeda kecepatannya dengan gelombang radio di ruang hampa.", "Semua gelombang elektromagnetik merambat dengan kecepatan sama di ruang hampa.")],
          [("Mengapa sinar ultraviolet berbahaya bagi kulit?", "Energinya cukup tinggi untuk merusak DNA sel kulit sehingga dapat menyebabkan kulit terbakar dan kanker kulit."),
           ("Apa warna cahaya tampak dengan panjang gelombang terbesar?", "Merah. Panjang gelombang terkecil pada cahaya tampak adalah ungu."),
           ("Bagaimana oven microwave memasak?", "Gelombang mikro menggetarkan molekul air dalam makanan sehingga makanan menjadi panas.")],
          [("Pemanfaatan spektrum", [("siaran radio dan televisi", "gelombang radio"), ("radar dan oven", "gelombang mikro"), ("komunikasi satelit dan Wi-Fi", "gelombang mikro"), ("remote televisi", "inframerah"),
                                    ("kamera penglihatan malam", "inframerah"), ("fotosintesis dan penglihatan", "cahaya tampak"), ("sterilisasi alat kedokteran", "ultraviolet"), ("mendeteksi uang palsu", "ultraviolet"),
                                    ("foto rontgen tulang", "sinar X"), ("pemeriksaan barang di bandara", "sinar X"), ("terapi kanker", "sinar gamma"), ("sterilisasi makanan dengan radiasi", "sinar gamma")],
            "‘{k}’ memanfaatkan ...", "Manakah pemanfaatan ‘{v}’?", ("gelombang bunyi",)),
           ("Urutan spektrum", [("gelombang radio", "gelombang mikro"), ("gelombang mikro", "inframerah"), ("inframerah", "cahaya tampak"), ("cahaya tampak", "ultraviolet"), ("ultraviolet", "sinar X"), ("sinar X", "sinar gamma")],
            "Jika diurutkan dari frekuensi kecil ke besar, gelombang apa yang berada tepat setelah ‘{k}’?", "Jika diurutkan dari frekuensi kecil ke besar, gelombang apa yang berada tepat sebelum ‘{v}’?"),
           ("Sifat gelombang elektromagnetik", [("cepat rambat di ruang hampa", "3 × 10⁸ m/s"), ("jenis gelombang", "transversal"), ("perlu medium atau tidak", "tidak memerlukan medium"),
                                               ("komponen penyusunnya", "medan listrik dan medan magnet yang saling tegak lurus"), ("muatan listriknya", "tidak bermuatan"), ("pengaruh medan magnet", "tidak dibelokkan medan magnet"),
                                               ("hubungan energi dan frekuensi", "makin besar frekuensi, makin besar energi")],
            "Bagaimana ‘{k}’ gelombang elektromagnetik?", None, ("340 m/s", "longitudinal"))],
          ["Gelombang elektromagnetik tidak memerlukan medium.", "Cepat rambat gelombang elektromagnetik di ruang hampa 3 × 10⁸ m/s.", "Gelombang elektromagnetik adalah gelombang transversal.",
           "Sinar gamma memiliki frekuensi terbesar.", "Gelombang radio memiliki panjang gelombang terbesar.", "Ultraviolet dipakai untuk sterilisasi.",
           "Sinar X dipakai untuk foto rontgen.", "c = λf."],
          [("Gelombang radio memiliki frekuensi terbesar.", "Gelombang radio memiliki frekuensi terkecil."), ("Remote televisi memakai sinar X.", "Remote televisi memakai inframerah."),
           ("Gelombang elektromagnetik adalah gelombang longitudinal.", "Gelombang elektromagnetik adalah gelombang transversal."), ("Gelombang elektromagnetik dibelokkan medan magnet.", "Gelombang elektromagnetik tidak bermuatan sehingga tidak dibelokkan."),
           ("Cahaya merah memiliki frekuensi lebih besar dari ungu.", "Cahaya ungu memiliki frekuensi lebih besar."), ("Sinar gamma tidak berbahaya bagi sel.", "Sinar gamma berenergi tinggi dan dapat merusak sel.")],
          "gelombang elektromagnetik", "waves-and-light", calc=f_gem),

        H("F", "fisika-kuantum", "Fisika Kuantum dan Efek Fotolistrik", "Fisika Kuantum",
          "Peserta didik menjelaskan radiasi benda hitam, teori kuantum Planck, energi foton, efek fotolistrik, efek Compton, dualisme gelombang-partikel, dan model atom Bohr.",
          "radiasi benda hitam, hukum Wien, kuantum Planck E = hf, efek fotolistrik, fungsi kerja, efek Compton, panjang gelombang de Broglie, model atom Bohr",
          "Energi cahaya datang dalam paket yang disebut foton", "Efek fotolistrik hanya terjadi jika frekuensi cahaya melebihi frekuensi ambang logam.",
          ["Benda yang dipanaskan memancarkan radiasi. Hukum Wien: makin panas benda, makin pendek panjang gelombang puncaknya (λmaks T = tetap). Planck menyatakan energi dipancarkan dalam paket: E = hf.",
           "Efek fotolistrik: elektron terlepas dari logam jika disinari cahaya berfrekuensi lebih dari frekuensi ambang. Ek maks = hf − W₀. Intensitas cahaya hanya menambah jumlah elektron, bukan energinya.",
           "Cahaya bersifat gelombang dan partikel (dualisme). De Broglie menyatakan partikel juga bersifat gelombang: λ = h/(mv). Model Bohr: elektron menyerap atau memancarkan foton saat berpindah tingkat energi."],
          [("Cahaya dengan energi foton 5 eV menyinari logam berfungsi kerja 3 eV. Berapa energi kinetik maksimum elektron?", ["Ek = hf − W₀.", "Ek = 5 − 3 = 2 eV."], "2 eV")],
          [("Cahaya yang lebih terang selalu dapat melepaskan elektron.", "Elektron lepas hanya jika frekuensi melebihi frekuensi ambang, berapa pun terangnya."), ("Energi foton tidak bergantung pada frekuensi.", "E = hf, sebanding dengan frekuensi."),
           ("Benda yang lebih panas memancarkan panjang gelombang puncak lebih panjang.", "Makin panas, panjang gelombang puncak makin pendek (hukum Wien).")],
          [("Apa itu fungsi kerja?", "Energi minimum yang diperlukan untuk melepaskan elektron dari permukaan logam."),
           ("Di mana efek fotolistrik dimanfaatkan?", "Pada panel surya, sensor cahaya, pintu otomatis, dan kamera digital."),
           ("Apa itu efek Compton?", "Bertambahnya panjang gelombang sinar X setelah menumbuk elektron, membuktikan bahwa foton memiliki momentum.")],
          [("Tokoh dan gagasan", [("energi radiasi dipancarkan dalam paket diskret", "Max Planck"), ("cahaya terdiri dari foton yang dapat melepaskan elektron logam", "Albert Einstein"), ("panjang gelombang puncak bergeser saat suhu naik", "Wilhelm Wien"),
                                  ("panjang gelombang sinar X bertambah setelah menumbuk elektron", "Arthur Compton"), ("partikel bergerak memiliki sifat gelombang", "Louis de Broglie"), ("elektron berada pada tingkat energi tertentu", "Niels Bohr"),
                                  ("posisi dan momentum tidak dapat diketahui tepat bersamaan", "Werner Heisenberg")],
            "Gagasan ‘{k}’ dikemukakan oleh ...", "Apa gagasan ‘{v}’?"),
           ("Efek fotolistrik", [("frekuensi cahaya di bawah frekuensi ambang", "tidak ada elektron yang lepas"), ("frekuensi cahaya di atas frekuensi ambang", "elektron lepas dari logam"),
                                ("intensitas cahaya diperbesar dengan frekuensi tetap di atas ambang", "jumlah elektron bertambah"), ("frekuensi cahaya diperbesar", "energi kinetik elektron bertambah"),
                                ("logam dengan fungsi kerja lebih besar dipakai", "energi kinetik elektron berkurang"), ("cahaya dengan frekuensi tepat sama dengan ambang", "elektron lepas dengan energi kinetik nol")],
            "Apa yang terjadi jika ‘{k}’?", None, ("logam meleleh seketika",)),
           ("Rumus kuantum", [("energi foton", "E = hf"), ("energi kinetik fotoelektron", "Ek = hf − W₀"), ("fungsi kerja", "W₀ = hf₀"), ("hukum pergeseran Wien", "λmaks × T = tetap"),
                             ("panjang gelombang de Broglie", "λ = h/(mv)"), ("energi foton dari panjang gelombang", "E = hc/λ"), ("momentum foton", "p = h/λ")],
            "Rumus apa untuk ‘{k}’?", "Rumus ‘{v}’ menyatakan ...")],
          ["Energi foton E = hf.", "Efek fotolistrik membuktikan cahaya bersifat partikel.", "Elektron lepas hanya jika frekuensi melebihi frekuensi ambang.",
           "Intensitas cahaya menambah jumlah elektron yang lepas.", "Makin panas benda, panjang gelombang puncaknya makin pendek.", "Partikel juga dapat bersifat gelombang.",
           "Fungsi kerja adalah energi minimum untuk melepaskan elektron.", "Panel surya memanfaatkan efek fotolistrik."],
          [("Intensitas cahaya menambah energi kinetik elektron.", "Intensitas menambah jumlah elektron; frekuensi yang menambah energi kinetik."), ("Energi foton berbanding lurus dengan panjang gelombang.", "E = hc/λ, jadi berbanding terbalik dengan panjang gelombang."),
           ("Efek Compton dikemukakan oleh Planck.", "Efek Compton dikemukakan oleh Arthur Compton."), ("Cahaya hanya bersifat gelombang.", "Cahaya bersifat gelombang dan partikel."),
           ("Frekuensi di bawah ambang dapat melepas elektron jika cahayanya sangat terang.", "Di bawah frekuensi ambang tidak ada elektron yang lepas."), ("Ek fotoelektron = hf + W₀.", "Ek = hf − W₀.")],
          "fisika kuantum", "waves-and-light", calc=f_gem),

        H("F", "fisika-inti-dan-radioaktivitas", "Fisika Inti dan Radioaktivitas", "Fisika Inti",
          "Peserta didik menjelaskan struktur inti, defek massa dan energi ikat, radioaktivitas (sinar alfa, beta, gamma), waktu paruh, reaksi fisi dan fusi, serta pemanfaatan dan bahaya radioisotop.",
          "nukleon, nomor atom dan massa, defek massa, energi ikat, peluruhan alfa, beta, gamma, waktu paruh, fisi, fusi, reaktor nuklir, radioisotop",
          "Setiap waktu paruh, zat radioaktif tinggal setengahnya", "Inti tidak stabil meluruh dengan memancarkan sinar alfa, beta, atau gamma.",
          ["Inti atom tersusun atas proton dan neutron (nukleon). Massa inti lebih kecil daripada jumlah massa nukleonnya (defek massa); selisih ini menjadi energi ikat inti, E = Δm c².",
           "Inti tidak stabil meluruh: sinar alfa (inti helium, daya tembus kecil), sinar beta (elektron, daya tembus sedang), dan sinar gamma (gelombang elektromagnetik, daya tembus besar).",
           "Waktu paruh adalah waktu agar setengah zat radioaktif meluruh: N = N₀(½)^(t/T). Fisi adalah pembelahan inti berat (reaktor nuklir), fusi adalah penggabungan inti ringan (energi matahari)."],
          [("Zat radioaktif 200 g berwaktu paruh 5 tahun. Berapa yang tersisa setelah 15 tahun?", ["15 tahun = 3 kali waktu paruh.", "200 × (½)³ = 25 g."], "25 g")],
          [("Sinar alfa memiliki daya tembus paling besar.", "Sinar gamma memiliki daya tembus paling besar; alfa paling kecil."), ("Setelah dua kali waktu paruh zat habis.", "Setelah dua kali waktu paruh masih tersisa seperempat."),
           ("Energi matahari berasal dari reaksi fisi.", "Energi matahari berasal dari reaksi fusi hidrogen.")],
          [("Apa manfaat radioisotop?", "Iodin-131 untuk mendeteksi gangguan tiroid, kobalt-60 untuk terapi kanker, karbon-14 untuk menentukan umur fosil, dan radiasi untuk pengawetan makanan."),
           ("Apa itu reaksi berantai?", "Reaksi fisi yang menghasilkan neutron baru yang memicu fisi berikutnya; dalam reaktor reaksi ini dikendalikan dengan batang kendali."),
           ("Bagaimana melindungi diri dari radiasi?", "Menjaga jarak, membatasi waktu paparan, dan memakai pelindung seperti timbal atau beton.")],
          [("Sinar radioaktif", [("sinar alfa", "inti helium bermuatan positif dengan daya tembus terkecil"), ("sinar beta", "elektron berkecepatan tinggi dengan daya tembus sedang"), ("sinar gamma", "gelombang elektromagnetik dengan daya tembus terbesar"),
                                 ("positron", "partikel bermassa sama dengan elektron tetapi bermuatan positif"), ("neutron", "partikel tidak bermuatan penyebab reaksi fisi")],
            "Apa ciri ‘{k}’?", "Partikel atau sinar apa yang merupakan ‘{v}’?", ("proton bebas tanpa massa", "foton bermuatan negatif")),
           ("Fisi atau fusi", [("pembelahan inti uranium-235 oleh neutron", "reaksi fisi"), ("reaksi di reaktor PLTN", "reaksi fisi"), ("bom atom", "reaksi fisi"), ("pembelahan inti plutonium", "reaksi fisi"),
                              ("penggabungan inti hidrogen menjadi helium", "reaksi fusi"), ("sumber energi matahari dan bintang", "reaksi fusi"), ("bom hidrogen", "reaksi fusi"), ("penggabungan deuterium dan tritium", "reaksi fusi")],
            "‘{k}’ adalah contoh ...", "Manakah contoh ‘{v}’?", ("reaksi kimia biasa",)),
           ("Pemanfaatan radioisotop", [("iodin-131", "mendeteksi gangguan kelenjar tiroid"), ("kobalt-60", "terapi radiasi kanker"), ("karbon-14", "menentukan umur fosil"), ("natrium-24", "mendeteksi kebocoran pipa dan penyumbatan darah"),
                                       ("fosfor-32", "mempelajari penyerapan pupuk oleh tanaman"), ("uranium-235", "bahan bakar reaktor nuklir"), ("teknetium-99m", "pencitraan organ dalam kedokteran nuklir")],
            "Radioisotop ‘{k}’ dipakai untuk ...", "Radioisotop apa yang dipakai untuk ‘{v}’?")],
          ["Inti atom tersusun atas proton dan neutron.", "Defek massa berubah menjadi energi ikat inti.", "Sinar gamma memiliki daya tembus terbesar.",
           "Sinar alfa adalah inti helium.", "Setelah satu waktu paruh zat tinggal setengahnya.", "Reaktor nuklir memanfaatkan reaksi fisi.",
           "Energi matahari berasal dari reaksi fusi.", "Karbon-14 dipakai untuk menentukan umur fosil."],
          [("Sinar beta adalah inti helium.", "Sinar alfa adalah inti helium; sinar beta adalah elektron."), ("PLTN memakai reaksi fusi.", "PLTN memakai reaksi fisi."),
           ("Setelah dua waktu paruh zat tinggal setengah.", "Setelah dua waktu paruh zat tinggal seperempat."), ("Sinar gamma bermuatan positif.", "Sinar gamma tidak bermuatan."),
           ("Massa inti sama persis dengan jumlah massa nukleonnya.", "Massa inti lebih kecil (defek massa)."), ("Iodin-131 dipakai untuk umur fosil.", "Iodin-131 dipakai untuk mendeteksi gangguan tiroid.")],
          "fisika inti", "energy", calc=f_inti),

        H("K", "asam-basa-dan-ph", "Larutan Asam Basa dan pH", "Asam Basa dan pH",
          "Peserta didik menjelaskan teori asam basa Arrhenius, Brønsted-Lowry, dan Lewis, kekuatan asam basa, menghitung pH larutan asam dan basa kuat, serta titrasi asam basa dan indikator.",
          "teori Arrhenius, Brønsted-Lowry (pasangan konjugasi), Lewis, asam kuat dan lemah, pH = −log[H⁺], pOH, Kw, titrasi, indikator",
          "pH = −log[H⁺]", "Asam kuat terionisasi sempurna. pH + pOH = 14 pada suhu 25 °C.",
          ["Menurut Arrhenius, asam melepas H⁺ dan basa melepas OH⁻ dalam air. Menurut Brønsted-Lowry, asam adalah donor proton dan basa akseptor proton. Menurut Lewis, asam adalah akseptor pasangan elektron.",
           "Asam kuat (HCl, HNO₃, H₂SO₄) dan basa kuat (NaOH, KOH) terionisasi sempurna. Asam lemah (CH₃COOH) hanya terionisasi sebagian. pH = −log[H⁺], pOH = −log[OH⁻], dan pH + pOH = 14.",
           "Titrasi asam basa dipakai untuk menentukan konsentrasi larutan. Titik ekuivalen terjadi saat mol H⁺ sama dengan mol OH⁻ dan ditandai perubahan warna indikator, misalnya fenolftalein."],
          [("Berapa pH larutan HCl 0,01 M?", ["HCl asam kuat, [H⁺] = 0,01 = 10⁻² M.", "pH = −log 10⁻² = 2."], "2")],
          [("Asam lemah berarti larutannya encer.", "Asam lemah adalah asam yang terionisasi sebagian; encer berarti konsentrasinya kecil."), ("Makin besar pH makin asam.", "Makin kecil pH makin asam."),
           ("Pada reaksi NH₃ + H₂O, air adalah basa.", "Air memberikan proton kepada NH₃, jadi air bertindak sebagai asam Brønsted-Lowry.")],
          [("Apa itu pasangan asam-basa konjugasi?", "Pasangan zat yang berbeda satu proton, misalnya HCl dan Cl⁻, atau NH₄⁺ dan NH₃."),
           ("Apa itu Kw?", "Tetapan kesetimbangan air, Kw = [H⁺][OH⁻] = 10⁻¹⁴ pada 25 °C."),
           ("Apa indikator untuk titrasi asam kuat dan basa kuat?", "Fenolftalein atau metil merah, karena titik ekuivalennya di sekitar pH 7.")],
          [("Kekuatan asam basa", [("HCl", "asam kuat"), ("HNO₃", "asam kuat"), ("H₂SO₄", "asam kuat"), ("HBr", "asam kuat"), ("CH₃COOH", "asam lemah"), ("HF", "asam lemah"), ("H₂CO₃", "asam lemah"),
                                  ("NaOH", "basa kuat"), ("KOH", "basa kuat"), ("Ca(OH)₂", "basa kuat"), ("NH₃", "basa lemah"), ("Al(OH)₃", "basa lemah")],
            "‘{k}’ termasuk ...", "Manakah yang termasuk ‘{v}’?", ("garam netral",)),
           ("Teori asam basa", [("asam melepas ion H⁺ dalam air", "teori Arrhenius"), ("basa melepas ion OH⁻ dalam air", "teori Arrhenius"), ("asam adalah donor proton", "teori Brønsted-Lowry"),
                               ("basa adalah akseptor proton", "teori Brønsted-Lowry"), ("asam adalah akseptor pasangan elektron", "teori Lewis"), ("basa adalah donor pasangan elektron", "teori Lewis"),
                               ("menjelaskan pasangan asam-basa konjugasi", "teori Brønsted-Lowry"), ("menjelaskan reaksi BF₃ dengan NH₃", "teori Lewis")],
            "‘{k}’ sesuai dengan ...", "Manakah pernyataan sesuai ‘{v}’?", ("teori Dalton",)),
           ("Pasangan konjugasi", [("HCl", "Cl⁻"), ("H₂O sebagai asam", "OH⁻"), ("H₂O sebagai basa", "H₃O⁺"), ("NH₃ sebagai basa", "NH₄⁺"), ("CH₃COOH", "CH₃COO⁻"), ("H₂SO₄", "HSO₄⁻"), ("HCO₃⁻ sebagai asam", "CO₃²⁻"), ("NH₄⁺ sebagai asam", "NH₃")],
            "Apa pasangan konjugasi dari ‘{k}’?", "Zat ‘{v}’ adalah pasangan konjugasi dari ...")],
          ["pH = −log[H⁺].", "pH + pOH = 14 pada 25 °C.", "Asam kuat terionisasi sempurna.",
           "Asam menurut Brønsted-Lowry adalah donor proton.", "Basa menurut Lewis adalah donor pasangan elektron.", "CH₃COOH adalah asam lemah.",
           "Titik ekuivalen titrasi terjadi saat mol H⁺ sama dengan mol OH⁻.", "Kw = 10⁻¹⁴ pada 25 °C."],
          [("pH 2 lebih basa daripada pH 5.", "pH 2 lebih asam daripada pH 5."), ("NH₃ adalah basa kuat.", "NH₃ adalah basa lemah."),
           ("Menurut Lewis, asam adalah donor pasangan elektron.", "Asam Lewis adalah akseptor pasangan elektron."), ("Asam lemah terionisasi sempurna.", "Asam lemah terionisasi sebagian."),
           ("Pasangan konjugasi HCl adalah H₂O.", "Pasangan konjugasi HCl adalah Cl⁻."), ("pH + pOH = 7.", "pH + pOH = 14 pada 25 °C.")],
          "asam basa dan pH", "matter", calc=f_ph),

        H("K", "larutan-penyangga-dan-hidrolisis", "Larutan Penyangga dan Hidrolisis Garam", "Penyangga dan Hidrolisis",
          "Peserta didik menjelaskan larutan penyangga (komposisi, cara kerja, dan peranannya dalam tubuh), hidrolisis garam dan sifat larutannya, serta kelarutan dan hasil kali kelarutan (Ksp).",
          "larutan penyangga asam dan basa, cara kerja penyangga, penyangga dalam darah, hidrolisis garam, garam asam, basa, netral, kelarutan, Ksp, pengendapan",
          "Penyangga mempertahankan pH", "Larutan penyangga pH-nya hampir tidak berubah jika ditambah sedikit asam, basa, atau diencerkan.",
          ["Larutan penyangga (buffer) terdiri dari asam lemah dengan basa konjugasinya (CH₃COOH dan CH₃COONa) atau basa lemah dengan asam konjugasinya (NH₃ dan NH₄Cl). Penyangga mempertahankan pH.",
           "Darah dijaga pada pH sekitar 7,4 oleh penyangga karbonat (H₂CO₃/HCO₃⁻) dan fosfat. Hidrolisis garam adalah reaksi ion garam dengan air: garam dari asam kuat dan basa lemah bersifat asam, dari asam lemah dan basa kuat bersifat basa.",
           "Garam dari asam kuat dan basa kuat (NaCl) tidak terhidrolisis dan bersifat netral. Kelarutan garam sukar larut dinyatakan dengan Ksp; endapan terbentuk jika hasil kali konsentrasi ion lebih besar dari Ksp."],
          [("Larutan NH₄Cl bersifat asam, basa, atau netral?", ["NH₄Cl berasal dari NH₃ (basa lemah) dan HCl (asam kuat).", "Ion NH₄⁺ terhidrolisis menghasilkan H₃O⁺."], "asam")],
          [("Larutan penyangga tidak berubah pH-nya walaupun ditambah banyak asam.", "Penyangga hanya tahan terhadap sedikit asam atau basa."), ("Semua garam bersifat netral.", "Sifat garam bergantung pada asam dan basa pembentuknya."),
           ("NaCl dan air bereaksi menghasilkan larutan asam.", "NaCl tidak terhidrolisis dan larutannya netral.")],
          [("Mengapa darah memerlukan penyangga?", "Enzim dalam tubuh bekerja pada pH tertentu; perubahan pH darah sedikit saja dapat berbahaya."),
           ("Apa contoh penyangga dalam kehidupan?", "Penyangga pada obat tetes mata, sampo, dan minuman kemasan agar pH tetap stabil."),
           ("Apa pengaruh ion senama terhadap kelarutan?", "Penambahan ion yang sama memperkecil kelarutan garam sukar larut.")],
          [("Penyangga atau bukan", [("CH₃COOH dan CH₃COONa", "larutan penyangga asam"), ("H₂CO₃ dan NaHCO₃", "larutan penyangga asam"), ("NaH₂PO₄ dan Na₂HPO₄", "larutan penyangga asam"),
                                    ("NH₃ dan NH₄Cl", "larutan penyangga basa"), ("NH₄OH dan (NH₄)₂SO₄", "larutan penyangga basa"), ("HCl dan NaCl", "bukan penyangga"), ("NaOH dan NaCl", "bukan penyangga"),
                                    ("HNO₃ dan KNO₃", "bukan penyangga")],
            "Campuran ‘{k}’ termasuk ...", "Manakah campuran yang termasuk ‘{v}’?", ("larutan koloid",)),
           ("Sifat larutan garam", [("NaCl", "netral"), ("KNO₃", "netral"), ("Na₂SO₄", "netral"), ("NH₄Cl", "asam"), ("(NH₄)₂SO₄", "asam"), ("NH₄NO₃", "asam"),
                                   ("CH₃COONa", "basa"), ("Na₂CO₃", "basa"), ("KCN", "basa"), ("CH₃COOK", "basa")],
            "Larutan garam ‘{k}’ bersifat ...", "Garam manakah yang larutannya bersifat ‘{v}’?", ("amfoter",)),
           ("Istilah larutan", [("larutan penyangga", "larutan yang mempertahankan pH"), ("hidrolisis", "reaksi ion garam dengan air"), ("kelarutan", "jumlah maksimum zat yang dapat larut"),
                               ("Ksp", "hasil kali konsentrasi ion dalam larutan jenuh"), ("larutan jenuh", "larutan yang tidak dapat melarutkan zat lagi"), ("ion senama", "ion yang sama dengan ion garam sukar larut"),
                               ("pengendapan", "terbentuknya padatan karena hasil kali ion melebihi Ksp")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Larutan penyangga mempertahankan pH.", "Campuran CH₃COOH dan CH₃COONa adalah penyangga.", "pH darah dijaga sekitar 7,4.",
           "NH₄Cl bersifat asam dalam air.", "CH₃COONa bersifat basa dalam air.", "NaCl bersifat netral.",
           "Endapan terbentuk jika hasil kali ion melebihi Ksp.", "Ion senama memperkecil kelarutan."],
          [("HCl dan NaCl membentuk penyangga.", "Penyangga perlu asam lemah atau basa lemah dengan konjugasinya."), ("Na₂CO₃ bersifat asam.", "Na₂CO₃ bersifat basa."),
           ("NaCl terhidrolisis menjadi asam.", "NaCl tidak terhidrolisis."), ("Ion senama memperbesar kelarutan.", "Ion senama memperkecil kelarutan."),
           ("pH darah sekitar 5.", "pH darah sekitar 7,4."), ("Penyangga tahan terhadap penambahan asam berapa pun banyaknya.", "Penyangga hanya tahan terhadap sedikit asam atau basa.")],
          "larutan penyangga dan hidrolisis", "matter"),

        H("K", "sifat-koligatif-larutan", "Sifat Koligatif Larutan", "Sifat Koligatif",
          "Peserta didik menjelaskan sifat koligatif larutan (penurunan tekanan uap, kenaikan titik didih, penurunan titik beku, tekanan osmotik), molalitas dan fraksi mol, serta faktor van't Hoff untuk elektrolit.",
          "molalitas, fraksi mol, penurunan tekanan uap, ΔTb = Kb·m, ΔTf = Kf·m, tekanan osmotik, faktor van't Hoff, penerapan sifat koligatif",
          "Sifat koligatif bergantung pada jumlah partikel zat terlarut", "Zat terlarut menaikkan titik didih dan menurunkan titik beku pelarut.",
          ["Sifat koligatif hanya bergantung pada jumlah partikel zat terlarut, bukan jenisnya. Molalitas m = mol zat terlarut ÷ kg pelarut.",
           "Kenaikan titik didih ΔTb = Kb × m (Kb air 0,52 °C/m), penurunan titik beku ΔTf = Kf × m (Kf air 1,86 °C/m), dan tekanan osmotik π = MRT.",
           "Larutan elektrolit menghasilkan lebih banyak partikel, sehingga dikalikan faktor van't Hoff i. NaCl yang terionisasi sempurna memiliki i = 2."],
          [("Sebanyak 18 g glukosa (Mr 180) dilarutkan dalam 500 g air. Berapa titik didih larutan? (Kb = 0,52)", ["m = 0,1 mol ÷ 0,5 kg = 0,2 m.", "ΔTb = 0,52 × 0,2 = 0,104 °C.", "Tb = 100 + 0,104."], "100,104 °C")],
          [("Sifat koligatif bergantung pada jenis zat terlarut.", "Sifat koligatif hanya bergantung pada jumlah partikel."), ("Zat terlarut menaikkan titik beku.", "Zat terlarut menurunkan titik beku."),
           ("NaCl dan glukosa dengan molalitas sama memberi ΔTf sama.", "NaCl terionisasi menjadi 2 ion, jadi ΔTf-nya dua kali.")],
          [("Mengapa garam ditaburkan di jalan bersalju?", "Garam menurunkan titik beku air, sehingga salju mencair walaupun suhu di bawah 0 °C."),
           ("Apa itu osmosis balik?", "Pemberian tekanan lebih besar dari tekanan osmotik agar air murni terpisah dari air laut, dipakai untuk desalinasi."),
           ("Mengapa cairan infus harus isotonik?", "Agar tekanan osmotiknya sama dengan darah sehingga sel darah tidak mengerut atau pecah.")],
          [("Penerapan sifat koligatif", [("garam ditaburkan di jalan bersalju", "penurunan titik beku"), ("antibeku pada radiator mobil", "penurunan titik beku"), ("membuat es puter dengan garam dan es", "penurunan titik beku"),
                                         ("cairan infus dibuat isotonik", "tekanan osmotik"), ("desalinasi air laut dengan osmosis balik", "tekanan osmotik"), ("mengawetkan ikan dengan garam", "tekanan osmotik"),
                                         ("air bergula mendidih di atas 100 °C", "kenaikan titik didih"), ("pembuatan garam dengan penguapan", "penurunan tekanan uap")],
            "‘{k}’ memanfaatkan ...", "Manakah penerapan ‘{v}’?", ("penurunan massa jenis",)),
           ("Faktor van't Hoff", [("glukosa", "i = 1"), ("urea", "i = 1"), ("sukrosa", "i = 1"), ("NaCl", "i = 2"), ("KCl", "i = 2"), ("CaCl₂", "i = 3"), ("Na₂SO₄", "i = 3"), ("AlCl₃", "i = 4")],
            "Berapa faktor van't Hoff (ionisasi sempurna) untuk ‘{k}’?", "Zat manakah yang memiliki ‘{v}’?"),
           ("Istilah koligatif", [("sifat koligatif", "sifat yang bergantung pada jumlah partikel zat terlarut"), ("molalitas", "mol zat terlarut per kilogram pelarut"), ("fraksi mol", "perbandingan mol suatu zat dengan mol total"),
                                 ("tekanan osmotik", "tekanan untuk mencegah osmosis"), ("larutan isotonik", "larutan dengan tekanan osmotik sama"), ("faktor van't Hoff", "jumlah partikel yang dihasilkan satu satuan zat terlarut"),
                                 ("Kb", "tetapan kenaikan titik didih molal"), ("Kf", "tetapan penurunan titik beku molal")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Sifat koligatif bergantung pada jumlah partikel zat terlarut.", "ΔTb = Kb × m.", "ΔTf = Kf × m.",
           "Zat terlarut menurunkan titik beku pelarut.", "Kb air 0,52 °C/m.", "NaCl memiliki faktor van't Hoff 2.",
           "Garam menurunkan titik beku salju di jalan.", "Cairan infus harus isotonik dengan darah."],
          [("Zat terlarut menurunkan titik didih.", "Zat terlarut menaikkan titik didih."), ("Glukosa memiliki faktor van't Hoff 2.", "Glukosa bukan elektrolit, i = 1."),
           ("Molalitas adalah mol per liter larutan.", "Molalitas adalah mol per kilogram pelarut; mol per liter adalah molaritas."), ("Kf air 0,52 °C/m.", "Kf air 1,86 °C/m."),
           ("Sifat koligatif bergantung pada warna zat terlarut.", "Sifat koligatif hanya bergantung pada jumlah partikel."), ("CaCl₂ memiliki faktor van't Hoff 2.", "CaCl₂ menghasilkan 3 ion, i = 3.")],
          "sifat koligatif larutan", "matter", calc=f_koligatif),

        H("K", "redoks-dan-elektrokimia", "Reaksi Redoks dan Elektrokimia", "Redoks dan Elektrokimia",
          "Peserta didik menjelaskan konsep oksidasi dan reduksi, bilangan oksidasi, penyetaraan reaksi redoks, sel Volta, potensial sel, korosi, dan sel elektrolisis.",
          "oksidasi dan reduksi, bilangan oksidasi, oksidator dan reduktor, sel Volta, deret Volta, E°sel, aki, baterai, korosi, elektrolisis, penyepuhan",
          "Oksidasi terjadi di anode, reduksi terjadi di katode", "Pada sel Volta logam dengan E° lebih kecil menjadi anode. E°sel = E°katode − E°anode.",
          ["Oksidasi adalah pelepasan elektron atau kenaikan bilangan oksidasi; reduksi adalah penerimaan elektron atau penurunan bilangan oksidasi. Zat yang mengalami reduksi disebut oksidator.",
           "Sel Volta mengubah energi kimia menjadi listrik. Anode (−) tempat oksidasi, katode (+) tempat reduksi. E°sel = E°katode − E°anode; reaksi spontan jika E°sel positif. Contoh sel Daniell: Zn | Zn²⁺ || Cu²⁺ | Cu.",
           "Sel elektrolisis memakai listrik untuk menjalankan reaksi tidak spontan, misalnya penyepuhan dan pemurnian logam. Korosi adalah oksidasi logam oleh oksigen dan air; dicegah dengan pengecatan, galvanisasi, atau perlindungan katodik."],
          [("Berapa bilangan oksidasi Mn dalam KMnO₄?", ["K = +1, O = −2.", "+1 + Mn + 4(−2) = 0 → Mn = +7."], "+7")],
          [("Oksidator adalah zat yang mengalami oksidasi.", "Oksidator mengalami reduksi; reduktor yang mengalami oksidasi."), ("Pada sel Volta anode bermuatan positif.", "Pada sel Volta anode bermuatan negatif."),
           ("Korosi dapat terjadi tanpa air dan oksigen.", "Korosi besi memerlukan oksigen dan air.")],
          [("Apa itu galvanisasi?", "Pelapisan besi dengan seng. Seng lebih mudah teroksidasi sehingga melindungi besi dari karat."),
           ("Bagaimana aki bekerja?", "Aki adalah sel Volta sekunder dengan elektrode Pb dan PbO₂ dalam H₂SO₄ yang dapat diisi ulang."),
           ("Apa itu penyepuhan?", "Pelapisan logam dengan logam lain melalui elektrolisis, misalnya melapisi cincin dengan emas; benda yang disepuh dipasang sebagai katode.")],
          [("Bilangan oksidasi", [("S dalam H₂SO₄", "+6"), ("Mn dalam KMnO₄", "+7"), ("Cr dalam K₂Cr₂O₇", "+6"), ("N dalam HNO₃", "+5"), ("Cl dalam NaClO₃", "+5"), ("C dalam CO₂", "+4"),
                                  ("Fe dalam Fe₂O₃", "+3"), ("O dalam H₂O₂", "−1"), ("H dalam NaH", "−1"), ("N dalam NH₃", "−3"), ("Cl dalam Cl₂", "0")],
            "Berapa bilangan oksidasi ‘{k}’?", None, ("+2", "+1", "−2")),
           ("Sel Volta dan elektrolisis", [("anode pada sel Volta", "kutub negatif tempat oksidasi"), ("katode pada sel Volta", "kutub positif tempat reduksi"), ("anode pada sel elektrolisis", "kutub positif tempat oksidasi"),
                                          ("katode pada sel elektrolisis", "kutub negatif tempat reduksi"), ("jembatan garam", "menjaga kenetralan muatan larutan"), ("E°sel positif", "reaksi berlangsung spontan"),
                                          ("benda yang disepuh", "dipasang sebagai katode"), ("logam penyepuh", "dipasang sebagai anode")],
            "Apa ciri atau fungsi ‘{k}’?", "Bagian apa yang merupakan ‘{v}’?"),
           ("Pencegahan korosi", [("mengecat pagar besi", "menghalangi kontak dengan udara dan air"), ("melapisi besi dengan seng", "galvanisasi"), ("melapisi kaleng dengan timah", "pelapisan timah"),
                                 ("memasang magnesium pada pipa bawah tanah", "perlindungan katodik"), ("melumuri mesin dengan oli", "menghalangi kontak dengan udara dan air"), ("melapisi besi dengan krom", "penyepuhan krom")],
            "Cara ‘{k}’ disebut atau bekerja dengan ...", "Manakah cara pencegahan korosi dengan ‘{v}’?")],
          ["Oksidasi adalah pelepasan elektron.", "Reduksi adalah penurunan bilangan oksidasi.", "Oksidator mengalami reduksi.",
           "Pada sel Volta oksidasi terjadi di anode.", "E°sel = E°katode − E°anode.", "Reaksi sel spontan jika E°sel positif.",
           "Galvanisasi melindungi besi dengan seng.", "Benda yang disepuh dipasang sebagai katode."],
          [("Reduksi adalah pelepasan elektron.", "Reduksi adalah penerimaan elektron."), ("Pada sel Volta katode bermuatan negatif.", "Pada sel Volta katode bermuatan positif."),
           ("Bilangan oksidasi unsur bebas adalah +1.", "Bilangan oksidasi unsur bebas adalah 0."), ("Reaksi dengan E°sel negatif berlangsung spontan.", "E°sel negatif berarti tidak spontan."),
           ("Pada penyepuhan benda dipasang sebagai anode.", "Benda yang disepuh dipasang sebagai katode."), ("Oksidator mengalami oksidasi.", "Oksidator mengalami reduksi.")],
          "redoks dan elektrokimia", "matter", calc=f_volta),

        H("K", "senyawa-karbon-dan-gugus-fungsi", "Senyawa Karbon dan Gugus Fungsi", "Gugus Fungsi",
          "Peserta didik menjelaskan gugus fungsi senyawa karbon (alkohol, eter, aldehida, keton, asam karboksilat, ester, haloalkana, amina), tata nama, isomer, reaksi, dan kegunaannya, serta senyawa benzena.",
          "alkohol, eter, aldehida, keton, asam karboksilat, ester, haloalkana, amina, isomer fungsi, reaksi oksidasi dan esterifikasi, benzena dan turunannya",
          "Gugus fungsi menentukan sifat senyawa karbon", "Alkohol bergugus −OH, asam karboksilat −COOH, ester −COO−. Gugus fungsi berbeda menghasilkan sifat berbeda.",
          ["Gugus fungsi adalah atom atau kelompok atom yang menentukan sifat khas senyawa karbon. Alkohol (R−OH), eter (R−O−R′), aldehida (R−CHO), keton (R−CO−R′), asam karboksilat (R−COOH), ester (R−COO−R′).",
           "Isomer fungsi adalah senyawa dengan rumus molekul sama tetapi gugus fungsi berbeda: alkohol dengan eter, aldehida dengan keton, asam karboksilat dengan ester.",
           "Esterifikasi adalah reaksi asam karboksilat dengan alkohol menghasilkan ester dan air; ester sering beraroma buah. Benzena (C₆H₆) berbentuk cincin dengan ikatan terdelokalisasi; turunannya antara lain fenol, toluena, dan asam benzoat."],
          [("Asam asetat bereaksi dengan etanol membentuk zat beraroma buah. Apa nama reaksinya?", ["Asam karboksilat + alkohol → ester + air.", "Reaksi pembentukan ester disebut esterifikasi."], "esterifikasi (menghasilkan etil asetat)")],
          [("Alkohol dan eter memiliki gugus fungsi yang sama.", "Alkohol bergugus −OH, eter bergugus −O−; keduanya isomer fungsi."), ("Aldehida dan keton tidak dapat dibedakan.", "Aldehida bereaksi dengan pereaksi Tollens dan Fehling, keton tidak."),
           ("Benzena memiliki ikatan tunggal saja.", "Benzena memiliki ikatan terdelokalisasi dalam cincin.")],
          [("Apa kegunaan formalin?", "Formalin (larutan metanal) untuk mengawetkan spesimen biologi; tidak boleh dipakai untuk makanan karena beracun."),
           ("Apa itu etanol?", "Alkohol yang dipakai sebagai pelarut, antiseptik, dan bahan bakar (bioetanol)."),
           ("Bagaimana membedakan aldehida dan keton?", "Aldehida menghasilkan cermin perak dengan pereaksi Tollens dan endapan merah bata dengan Fehling; keton tidak.")],
          [("Gugus fungsi", [("R−OH", "alkohol"), ("R−O−R′", "eter"), ("R−CHO", "aldehida"), ("R−CO−R′", "keton"), ("R−COOH", "asam karboksilat"), ("R−COO−R′", "ester"), ("R−X (X = halogen)", "haloalkana"), ("R−NH₂", "amina")],
            "Gugus ‘{k}’ dimiliki oleh golongan ...", "Bagaimana gugus fungsi ‘{v}’?"),
           ("Senyawa dan kegunaannya", [("etanol", "pelarut, antiseptik, dan bahan bakar"), ("metanal (formalin)", "pengawet spesimen biologi"), ("propanon (aseton)", "pembersih cat kuku"), ("asam asetat (cuka)", "pemberi rasa asam makanan"),
                                       ("etil butirat", "pemberi aroma nanas"), ("dietil eter", "obat bius pada masa lalu"), ("kloroform", "pelarut di laboratorium"), ("asam benzoat", "pengawet makanan"), ("fenol", "bahan desinfektan")],
            "Apa kegunaan ‘{k}’?", "Senyawa apa yang dipakai sebagai ‘{v}’?"),
           ("Isomer fungsi", [("alkohol", "eter"), ("eter", "alkohol"), ("aldehida", "keton"), ("keton", "aldehida"), ("asam karboksilat", "ester"), ("ester", "asam karboksilat")],
            "Golongan ‘{k}’ berisomer fungsi dengan ...", None, ("alkana", "amina", "haloalkana"))],
          ["Alkohol memiliki gugus −OH.", "Asam karboksilat memiliki gugus −COOH.", "Esterifikasi menghasilkan ester dan air.",
           "Alkohol berisomer fungsi dengan eter.", "Aldehida berisomer fungsi dengan keton.", "Ester banyak beraroma buah.",
           "Aldehida bereaksi positif dengan pereaksi Tollens.", "Formalin tidak boleh dipakai untuk mengawetkan makanan."],
          [("Keton memiliki gugus −CHO.", "Gugus −CHO dimiliki aldehida; keton −CO−."), ("Asam karboksilat berisomer fungsi dengan eter.", "Asam karboksilat berisomer fungsi dengan ester."),
           ("Esterifikasi adalah reaksi alkohol dengan eter.", "Esterifikasi adalah reaksi asam karboksilat dengan alkohol."), ("Keton bereaksi positif dengan Tollens.", "Tollens positif untuk aldehida."),
           ("Aseton dipakai untuk mengawetkan makanan.", "Aseton dipakai sebagai pembersih cat kuku."), ("Benzena hanya memiliki ikatan rangkap terpisah yang tetap.", "Ikatan pada benzena terdelokalisasi.")],
          "gugus fungsi senyawa karbon", "matter"),

        H("K", "polimer-dan-biomolekul", "Polimer dan Biomolekul", "Polimer dan Biomolekul",
          "Peserta didik menjelaskan polimer alam dan sintetis, polimerisasi adisi dan kondensasi, serta biomolekul (karbohidrat, protein, lipid, asam nukleat) dan uji identifikasinya.",
          "monomer dan polimer, polimerisasi adisi dan kondensasi, plastik, karet, nilon, karbohidrat (monosakarida, disakarida, polisakarida), protein dan asam amino, lipid, uji biuret, Fehling, iodin",
          "Polimer tersusun atas banyak monomer", "Polimer adisi dari monomer berikatan rangkap; polimer kondensasi melepaskan molekul kecil seperti air.",
          ["Polimer adalah molekul besar yang tersusun atas banyak monomer. Polimer alam: amilum, selulosa, protein, karet alam, DNA. Polimer sintetis: polietena, PVC, nilon, teflon.",
           "Polimerisasi adisi terjadi pada monomer berikatan rangkap tanpa hasil samping (etena → polietena). Polimerisasi kondensasi melepaskan molekul kecil seperti air (asam amino → protein, nilon).",
           "Karbohidrat terdiri dari monosakarida (glukosa, fruktosa), disakarida (sukrosa, laktosa), dan polisakarida (amilum, glikogen, selulosa). Protein tersusun atas asam amino yang dihubungkan ikatan peptida."],
          [("Monomer apa yang menyusun amilum?", ["Amilum adalah polisakarida pada tumbuhan.", "Amilum tersusun atas banyak glukosa."], "glukosa")],
          [("Semua polimer adalah plastik buatan.", "Ada polimer alam seperti amilum, protein, dan karet alam."), ("Polimerisasi adisi menghasilkan air.", "Yang menghasilkan air adalah polimerisasi kondensasi."),
           ("Sukrosa adalah monosakarida.", "Sukrosa adalah disakarida dari glukosa dan fruktosa.")],
          [("Mengapa plastik sulit terurai?", "Rantai polimer sintetis sangat panjang dan stabil sehingga sulit diuraikan mikroorganisme."),
           ("Apa itu ikatan peptida?", "Ikatan antara gugus karboksil satu asam amino dan gugus amino asam amino lain dengan melepas air."),
           ("Apa itu lipid?", "Golongan senyawa yang tidak larut dalam air, seperti lemak, minyak, fosfolipid, dan steroid.")],
          [("Polimer dan monomernya", [("polietena (PE)", "etena"), ("polivinil klorida (PVC)", "vinil klorida"), ("teflon", "tetrafluoroetena"), ("polipropena", "propena"), ("karet alam", "isoprena"),
                                      ("amilum", "glukosa"), ("selulosa", "glukosa"), ("protein", "asam amino"), ("asam nukleat", "nukleotida")],
            "Monomer penyusun ‘{k}’ adalah ...", "Polimer apa yang tersusun atas monomer ‘{v}’?"),
           ("Adisi atau kondensasi", [("polietena", "polimerisasi adisi"), ("PVC", "polimerisasi adisi"), ("teflon", "polimerisasi adisi"), ("polistirena", "polimerisasi adisi"), ("karet alam", "polimerisasi adisi"),
                                     ("nilon", "polimerisasi kondensasi"), ("protein", "polimerisasi kondensasi"), ("amilum", "polimerisasi kondensasi"), ("dakron (poliester)", "polimerisasi kondensasi")],
            "‘{k}’ terbentuk melalui ...", "Manakah polimer yang terbentuk melalui ‘{v}’?", ("polimerisasi radiasi",)),
           ("Karbohidrat dan uji biomolekul", [("glukosa", "monosakarida"), ("fruktosa", "monosakarida"), ("galaktosa", "monosakarida"), ("sukrosa", "disakarida"), ("laktosa", "disakarida"), ("maltosa", "disakarida"),
                                              ("amilum", "polisakarida"), ("glikogen", "polisakarida"), ("selulosa", "polisakarida")],
            "‘{k}’ termasuk ...", "Manakah yang termasuk ‘{v}’?", ("trigliserida",))],
          ["Polimer tersusun atas banyak monomer.", "Polietena terbentuk dari etena.", "Polimerisasi kondensasi melepaskan molekul kecil seperti air.",
           "Protein tersusun atas asam amino.", "Amilum tersusun atas glukosa.", "Sukrosa adalah disakarida.",
           "Karet alam adalah polimer alam.", "Lipid tidak larut dalam air."],
          [("Nilon terbentuk melalui polimerisasi adisi.", "Nilon terbentuk melalui polimerisasi kondensasi."), ("Glukosa adalah polisakarida.", "Glukosa adalah monosakarida."),
           ("Protein tersusun atas nukleotida.", "Protein tersusun atas asam amino; asam nukleat tersusun atas nukleotida."), ("PVC adalah polimer alam.", "PVC adalah polimer sintetis."),
           ("Selulosa tersusun atas fruktosa.", "Selulosa tersusun atas glukosa."), ("Plastik mudah diuraikan mikroorganisme.", "Plastik sintetis sulit terurai.")],
          "polimer dan biomolekul", "matter"),

        H("B", "enzim-dan-metabolisme", "Enzim dan Metabolisme", "Enzim dan Metabolisme",
          "Peserta didik menjelaskan metabolisme (katabolisme dan anabolisme), ATP sebagai sumber energi sel, sifat dan cara kerja enzim, serta faktor yang memengaruhi kerja enzim.",
          "metabolisme, katabolisme, anabolisme, ATP, enzim sebagai biokatalisator, sisi aktif, teori gembok-kunci dan kecocokan induksi, suhu, pH, konsentrasi, inhibitor",
          "Enzim mempercepat reaksi dengan menurunkan energi aktivasi", "Enzim bekerja spesifik dan dipengaruhi suhu, pH, konsentrasi, serta inhibitor.",
          ["Metabolisme adalah seluruh reaksi kimia di dalam sel. Katabolisme menguraikan molekul besar dan melepas energi (respirasi), anabolisme menyusun molekul besar dan memerlukan energi (fotosintesis, sintesis protein).",
           "ATP (adenosin trifosfat) adalah pembawa energi sel; pemutusan ikatan fosfatnya melepas energi untuk kegiatan sel.",
           "Enzim adalah protein biokatalisator yang mempercepat reaksi dengan menurunkan energi aktivasi. Enzim bekerja spesifik pada substratnya (teori gembok-kunci dan kecocokan induksi) dan rusak (terdenaturasi) pada suhu tinggi atau pH yang tidak sesuai."],
          [("Mengapa enzim pepsin tidak bekerja di usus halus?", ["Pepsin bekerja optimal pada pH asam lambung.", "pH usus halus basa sehingga pepsin tidak aktif."], "karena pH usus halus tidak sesuai bagi pepsin")],
          [("Enzim ikut habis setelah bereaksi.", "Enzim tidak ikut berubah dan dapat dipakai berulang kali."), ("Makin tinggi suhu makin cepat kerja enzim tanpa batas.", "Di atas suhu optimum enzim terdenaturasi."),
           ("Satu enzim dapat bekerja pada semua jenis substrat.", "Enzim bekerja spesifik pada substrat tertentu.")],
          [("Apa itu inhibitor kompetitif?", "Zat yang mirip substrat dan menempati sisi aktif enzim sehingga menghambat kerja enzim."),
           ("Apa itu kofaktor?", "Zat nonprotein yang membantu kerja enzim, misalnya ion logam atau koenzim dari vitamin."),
           ("Apa contoh enzim dalam kehidupan?", "Katalase yang menguraikan hidrogen peroksida di hati, amilase di ludah, dan enzim pada deterjen.")],
          [("Katabolisme atau anabolisme", [("respirasi seluler", "katabolisme"), ("pencernaan amilum menjadi glukosa", "katabolisme"), ("fermentasi alkohol", "katabolisme"), ("penguraian lemak menjadi asam lemak", "katabolisme"),
                                           ("fotosintesis", "anabolisme"), ("kemosintesis", "anabolisme"), ("sintesis protein", "anabolisme"), ("pembentukan glikogen di hati", "anabolisme")],
            "‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("homeostasis",)),
           ("Faktor kerja enzim", [("suhu dinaikkan sampai optimum", "kerja enzim meningkat"), ("suhu jauh di atas optimum", "enzim terdenaturasi dan tidak bekerja"), ("suhu sangat rendah", "enzim tidak aktif tetapi tidak rusak"),
                                  ("pH tidak sesuai dengan pH optimum", "kerja enzim menurun"), ("konsentrasi substrat ditambah saat enzim belum jenuh", "laju reaksi meningkat"), ("inhibitor kompetitif ditambahkan", "kerja enzim terhambat"),
                                  ("kofaktor yang diperlukan ditambahkan", "kerja enzim meningkat")],
            "Apa yang terjadi jika ‘{k}’?", None, ("enzim berubah menjadi substrat",)),
           ("Istilah enzim", [("enzim", "protein yang berfungsi sebagai biokatalisator"), ("substrat", "zat yang diubah oleh enzim"), ("sisi aktif", "bagian enzim tempat substrat terikat"), ("apoenzim", "bagian protein dari enzim"),
                             ("koenzim", "kofaktor berupa molekul organik seperti vitamin"), ("denaturasi", "rusaknya struktur enzim karena suhu tinggi atau pH ekstrem"), ("energi aktivasi", "energi minimum agar reaksi berlangsung"),
                             ("ATP", "molekul pembawa energi di dalam sel")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Metabolisme adalah seluruh reaksi kimia di dalam sel.", "Katabolisme melepaskan energi.", "Anabolisme memerlukan energi.",
           "Enzim menurunkan energi aktivasi.", "Enzim bekerja spesifik pada substratnya.", "Suhu terlalu tinggi dapat merusak enzim.",
           "ATP adalah pembawa energi sel.", "Fotosintesis termasuk anabolisme."],
          [("Respirasi termasuk anabolisme.", "Respirasi menguraikan glukosa, jadi katabolisme."), ("Enzim menaikkan energi aktivasi.", "Enzim menurunkan energi aktivasi."),
           ("Enzim tersusun atas karbohidrat.", "Enzim adalah protein."), ("Suhu rendah merusak enzim secara permanen.", "Suhu rendah hanya menonaktifkan enzim sementara."),
           ("Enzim habis setelah satu reaksi.", "Enzim dapat dipakai berulang kali."), ("Inhibitor mempercepat kerja enzim.", "Inhibitor menghambat kerja enzim.")],
          "enzim dan metabolisme", "living-things-and-ecosystems"),

        H("B", "respirasi-seluler-dan-fotosintesis", "Respirasi Seluler dan Fotosintesis", "Respirasi dan Fotosintesis",
          "Peserta didik menjelaskan tahap respirasi aerob (glikolisis, dekarboksilasi oksidatif, siklus Krebs, transpor elektron), respirasi anaerob (fermentasi), serta reaksi terang dan gelap fotosintesis.",
          "glikolisis, siklus Krebs, transpor elektron, ATP, fermentasi asam laktat dan alkohol, reaksi terang, siklus Calvin, kloroplas, kemosintesis",
          "Respirasi memecah glukosa, fotosintesis membentuk glukosa", "Respirasi aerob menghasilkan sekitar 36–38 ATP per glukosa. Fotosintesis terdiri dari reaksi terang dan siklus Calvin.",
          ["Respirasi aerob: glikolisis di sitoplasma (glukosa → 2 piruvat, 2 ATP), dekarboksilasi oksidatif dan siklus Krebs di matriks mitokondria, lalu transpor elektron di membran dalam mitokondria yang menghasilkan ATP terbanyak.",
           "Respirasi anaerob (fermentasi) berlangsung tanpa oksigen dan hanya menghasilkan 2 ATP. Fermentasi asam laktat terjadi di otot yang kelelahan, fermentasi alkohol dilakukan ragi.",
           "Fotosintesis di kloroplas: reaksi terang di tilakoid memerlukan cahaya, memecah air (fotolisis), menghasilkan O₂, ATP, dan NADPH. Siklus Calvin (reaksi gelap) di stroma memakai CO₂, ATP, dan NADPH untuk membentuk glukosa."],
          [("Mengapa otot terasa pegal setelah berlari jauh?", ["Otot kekurangan oksigen.", "Terjadi fermentasi asam laktat yang menumpuk di otot."], "karena penumpukan asam laktat")],
          [("Oksigen dihasilkan pada siklus Calvin.", "Oksigen dihasilkan dari fotolisis air pada reaksi terang."), ("Glikolisis terjadi di mitokondria.", "Glikolisis terjadi di sitoplasma."),
           ("Fermentasi menghasilkan lebih banyak ATP daripada respirasi aerob.", "Fermentasi hanya menghasilkan 2 ATP.")],
          [("Apa akseptor elektron terakhir pada respirasi aerob?", "Oksigen. Oksigen menerima elektron dan H⁺ lalu membentuk air."),
           ("Apa itu kemosintesis?", "Pembentukan zat organik dengan energi dari reaksi kimia, misalnya oleh bakteri nitrifikasi."),
           ("Faktor apa yang memengaruhi fotosintesis?", "Intensitas cahaya, konsentrasi CO₂, suhu, air, dan jumlah klorofil.")],
          [("Tahap dan tempatnya", [("glikolisis", "sitoplasma"), ("dekarboksilasi oksidatif", "matriks mitokondria"), ("siklus Krebs", "matriks mitokondria"), ("transpor elektron", "membran dalam mitokondria"),
                                   ("fermentasi", "sitoplasma"), ("reaksi terang", "membran tilakoid kloroplas"), ("siklus Calvin", "stroma kloroplas"), ("fotolisis air", "membran tilakoid kloroplas")],
            "Tahap ‘{k}’ berlangsung di ...", "Tahap apa yang berlangsung di ‘{v}’?"),
           ("Hasil tiap tahap", [("glikolisis", "2 piruvat, 2 ATP, dan 2 NADH"), ("dekarboksilasi oksidatif", "asetil-KoA, CO₂, dan NADH"), ("siklus Krebs", "CO₂, ATP, NADH, dan FADH₂"), ("transpor elektron", "ATP terbanyak dan air"),
                               ("fermentasi asam laktat", "asam laktat dan 2 ATP"), ("fermentasi alkohol", "etanol, CO₂, dan 2 ATP"), ("reaksi terang", "ATP, NADPH, dan O₂"), ("siklus Calvin", "glukosa (dari G3P)")],
            "Apa hasil ‘{k}’?", "Tahap apa yang menghasilkan ‘{v}’?"),
           ("Respirasi atau fotosintesis", {"ciri respirasi seluler": ["memecah glukosa", "menghasilkan CO₂", "memerlukan O₂ pada respirasi aerob", "berlangsung di mitokondria", "berlangsung siang dan malam", "melepaskan energi"],
                                           "ciri fotosintesis": ["membentuk glukosa", "menghasilkan O₂", "memerlukan cahaya pada reaksi terang", "berlangsung di kloroplas", "memakai CO₂", "menyimpan energi dalam zat organik"]})],
          ["Glikolisis terjadi di sitoplasma.", "Siklus Krebs terjadi di matriks mitokondria.", "Transpor elektron menghasilkan ATP terbanyak.",
           "Oksigen adalah akseptor elektron terakhir pada respirasi aerob.", "Fermentasi hanya menghasilkan 2 ATP per glukosa.", "Oksigen fotosintesis berasal dari fotolisis air.",
           "Siklus Calvin berlangsung di stroma.", "Ragi melakukan fermentasi alkohol."],
          [("Siklus Calvin terjadi di tilakoid.", "Siklus Calvin terjadi di stroma."), ("Fermentasi memerlukan oksigen.", "Fermentasi berlangsung tanpa oksigen."),
           ("Oksigen fotosintesis berasal dari CO₂.", "Oksigen berasal dari pemecahan air."), ("Glikolisis menghasilkan 36 ATP.", "Glikolisis menghasilkan 2 ATP."),
           ("Otot yang lelah melakukan fermentasi alkohol.", "Otot yang lelah melakukan fermentasi asam laktat."), ("Respirasi hanya terjadi pada siang hari.", "Respirasi terjadi siang dan malam.")],
          "respirasi seluler dan fotosintesis", "living-things-and-ecosystems"),

        H("B", "dna-dan-sintesis-protein", "Materi Genetik dan Sintesis Protein", "Sintesis Protein",
          "Peserta didik menjelaskan struktur dan fungsi DNA, RNA, gen, dan kromosom, replikasi DNA, serta tahap sintesis protein (transkripsi dan translasi) dan kode genetik.",
          "struktur DNA (double helix, nukleotida, pasangan basa A-T, G-C), RNA (mRNA, tRNA, rRNA), replikasi semikonservatif, transkripsi, translasi, kodon dan antikodon",
          "DNA → mRNA → protein", "Transkripsi menyalin DNA menjadi mRNA di inti sel; translasi menerjemahkan mRNA menjadi protein di ribosom.",
          ["DNA berbentuk tangga berpilin ganda. Nukleotidanya terdiri dari gula deoksiribosa, fosfat, dan basa nitrogen. Pasangan basa selalu A dengan T dan G dengan C.",
           "RNA berantai tunggal dengan gula ribosa dan basa urasil (U) menggantikan timin. mRNA membawa kode genetik, tRNA membawa asam amino, dan rRNA menyusun ribosom. Replikasi DNA bersifat semikonservatif.",
           "Sintesis protein: transkripsi (DNA → mRNA) di inti, lalu translasi di ribosom. Setiap kodon (tiga basa mRNA) menentukan satu asam amino; tRNA dengan antikodon yang sesuai membawa asam amino itu. AUG adalah kodon awal."],
          [("Urutan DNA pencetak adalah TAC GGA. Bagaimana urutan mRNA hasil transkripsinya?", ["Pasangan T–A, A–U, C–G, G–C.", "TAC → AUG, GGA → CCU."], "AUG CCU")],
          [("RNA memiliki basa timin.", "RNA memiliki urasil sebagai pengganti timin."), ("Translasi terjadi di inti sel.", "Translasi terjadi di ribosom pada sitoplasma."),
           ("Satu kodon terdiri dari dua basa.", "Satu kodon terdiri dari tiga basa.")],
          [("Apa arti replikasi semikonservatif?", "Setiap DNA baru terdiri dari satu rantai lama dan satu rantai baru."),
           ("Apa itu kodon stop?", "Kodon UAA, UAG, dan UGA yang menghentikan translasi karena tidak mengkode asam amino."),
           ("Siapa penemu model DNA double helix?", "James Watson dan Francis Crick pada tahun 1953, berdasarkan data difraksi sinar X Rosalind Franklin.")],
          [("Pasangan basa", [("A pada DNA berpasangan dengan", "T pada DNA"), ("G pada DNA berpasangan dengan", "C pada DNA"), ("T pada DNA pencetak ditranskripsi menjadi", "A pada mRNA"),
                             ("A pada DNA pencetak ditranskripsi menjadi", "U pada mRNA"), ("G pada DNA pencetak ditranskripsi menjadi", "C pada mRNA"), ("C pada DNA pencetak ditranskripsi menjadi", "G pada mRNA"),
                             ("kodon AUG berpasangan dengan antikodon", "UAC pada tRNA"), ("kodon GCU berpasangan dengan antikodon", "CGA pada tRNA")],
            "‘{k}’ ...", None, ("U pada DNA", "T pada mRNA")),
           ("DNA atau RNA", {"ciri DNA": ["berantai ganda", "gula deoksiribosa", "memiliki basa timin", "terutama di inti sel", "dapat bereplikasi", "jumlahnya tetap dalam sel"],
                            "ciri RNA": ["berantai tunggal", "gula ribosa", "memiliki basa urasil", "terdapat di inti dan sitoplasma", "dibentuk melalui transkripsi", "jumlahnya berubah sesuai sintesis protein"]}),
           ("Tahap sintesis protein", [("transkripsi", "DNA disalin menjadi mRNA di inti sel"), ("translasi", "mRNA diterjemahkan menjadi rantai asam amino di ribosom"), ("inisiasi translasi", "ribosom menempel pada kodon awal AUG"),
                                      ("elongasi", "asam amino ditambahkan satu per satu"), ("terminasi", "translasi berhenti pada kodon stop"), ("replikasi", "DNA menggandakan diri sebelum pembelahan sel"),
                                      ("RNA polimerase", "enzim yang membuat mRNA dari DNA")],
            "Apa yang terjadi pada ‘{k}’?", "Tahap atau enzim apa yang dimaksud: ‘{v}’?")],
          ["DNA berbentuk tangga berpilin ganda.", "Basa A berpasangan dengan T pada DNA.", "RNA memiliki basa urasil.",
           "Transkripsi terjadi di inti sel.", "Translasi terjadi di ribosom.", "Satu kodon terdiri dari tiga basa.",
           "AUG adalah kodon awal.", "Replikasi DNA bersifat semikonservatif."],
          [("DNA berantai tunggal.", "DNA berantai ganda."), ("G berpasangan dengan T.", "G berpasangan dengan C."), ("tRNA membawa kode genetik dari inti.", "mRNA membawa kode genetik; tRNA membawa asam amino."),
           ("Transkripsi terjadi di ribosom.", "Transkripsi terjadi di inti sel."), ("DNA memiliki gula ribosa.", "DNA memiliki gula deoksiribosa."), ("UAA adalah kodon awal.", "UAA adalah kodon stop.")],
          "materi genetik dan sintesis protein", "living-things-and-ecosystems"),

        H("B", "pembelahan-sel", "Pembelahan Sel: Mitosis dan Meiosis", "Pembelahan Sel",
          "Peserta didik menjelaskan siklus sel, tahap mitosis dan meiosis, perbedaan keduanya, serta gametogenesis (spermatogenesis dan oogenesis) pada manusia.",
          "siklus sel (interfase G1, S, G2), profase, metafase, anafase, telofase, sitokinesis, meiosis I dan II, pindah silang, spermatogenesis, oogenesis",
          "Mitosis: 2 sel identik. Meiosis: 4 sel haploid", "Mitosis untuk pertumbuhan dan perbaikan, meiosis untuk membentuk sel kelamin.",
          ["Siklus sel terdiri dari interfase (G1 tumbuh, S replikasi DNA, G2 persiapan) dan fase mitosis. Mitosis: profase (kromosom tampak), metafase (kromosom berjajar di bidang ekuator), anafase (kromatid berpisah ke kutub), telofase (inti baru terbentuk).",
           "Meiosis terdiri dari dua kali pembelahan (meiosis I dan II) dan menghasilkan 4 sel haploid (n). Pada profase I terjadi pindah silang (crossing over) yang menambah variasi genetik.",
           "Spermatogenesis di testis menghasilkan 4 sperma dari satu spermatosit. Oogenesis di ovarium menghasilkan 1 ovum dan 3 badan polar."],
          [("Pada tahap apa kromosom berjajar di bidang ekuator?", ["Kromosom bergerak ke tengah sel.", "Tahap ini mudah dipakai untuk menghitung kromosom."], "metafase")],
          [("Replikasi DNA terjadi pada profase.", "Replikasi DNA terjadi pada fase S interfase."), ("Oogenesis menghasilkan 4 ovum.", "Oogenesis menghasilkan 1 ovum dan 3 badan polar."),
           ("Pindah silang terjadi pada mitosis.", "Pindah silang terjadi pada profase I meiosis.")],
          [("Mengapa meiosis penting untuk keragaman?", "Pindah silang dan pemisahan kromosom secara acak menghasilkan kombinasi gen yang berbeda pada setiap gamet."),
           ("Apa itu sel diploid dan haploid?", "Sel diploid (2n) memiliki kromosom berpasangan seperti sel tubuh; sel haploid (n) hanya satu set seperti sel kelamin."),
           ("Di mana mitosis mudah diamati?", "Pada ujung akar bawang merah yang sel-selnya aktif membelah.")],
          [("Tahap mitosis", [("kromosom mulai tampak dan membran inti menghilang", "profase"), ("benang spindel mulai terbentuk", "profase"), ("kromosom berjajar di bidang ekuator", "metafase"),
                             ("kromatid saudara berpisah menuju kutub", "anafase"), ("membran inti terbentuk kembali", "telofase"), ("sitoplasma terbagi menjadi dua", "sitokinesis"), ("DNA bereplikasi", "fase S interfase"),
                             ("sel tumbuh dan membentuk organel", "fase G1 interfase")],
            "Peristiwa ‘{k}’ terjadi pada ...", "Apa yang terjadi pada ‘{v}’?"),
           ("Mitosis atau meiosis", [("menghasilkan 2 sel anak", "mitosis"), ("sel anak diploid dan identik", "mitosis"), ("terjadi pada sel tubuh", "mitosis"), ("untuk pertumbuhan dan perbaikan jaringan", "mitosis"),
                                    ("menghasilkan 4 sel anak", "meiosis"), ("sel anak haploid", "meiosis"), ("terjadi pindah silang", "meiosis"), ("terjadi pada pembentukan gamet", "meiosis"), ("terdiri dari dua kali pembelahan", "meiosis")],
            "‘{k}’ adalah ciri ...", "Manakah ciri ‘{v}’?", ("amitosis", "fragmentasi")),
           ("Gametogenesis", [("spermatogonium", "sel induk sperma yang diploid"), ("spermatosit primer", "sel yang mengalami meiosis I pada pembentukan sperma"), ("spermatid", "sel haploid yang berkembang menjadi sperma"),
                             ("oogonium", "sel induk telur yang diploid"), ("oosit sekunder", "sel hasil meiosis I yang dilepas saat ovulasi"), ("badan polar", "sel kecil hasil oogenesis yang tidak berkembang"),
                             ("ovum", "sel telur haploid yang dapat dibuahi"), ("hasil satu spermatosit primer", "empat sperma")],
            "Apa yang dimaksud ‘{k}’?", "Sel atau hasil apa yang merupakan ‘{v}’?")],
          ["Replikasi DNA terjadi pada fase S.", "Pada metafase kromosom berjajar di bidang ekuator.", "Pada anafase kromatid berpisah ke kutub.",
           "Mitosis menghasilkan 2 sel identik.", "Meiosis menghasilkan 4 sel haploid.", "Pindah silang terjadi pada profase I.",
           "Spermatogenesis menghasilkan 4 sperma.", "Oogenesis menghasilkan 1 ovum dan 3 badan polar."],
          [("Mitosis menghasilkan sel haploid.", "Mitosis menghasilkan sel diploid."), ("Kromatid berpisah pada metafase.", "Kromatid berpisah pada anafase."),
           ("Meiosis hanya satu kali pembelahan.", "Meiosis terdiri dari dua kali pembelahan."), ("Oogenesis menghasilkan 4 ovum.", "Oogenesis menghasilkan 1 ovum."),
           ("Membran inti terbentuk pada profase.", "Membran inti menghilang pada profase dan terbentuk kembali pada telofase."), ("Pindah silang mengurangi variasi genetik.", "Pindah silang menambah variasi genetik.")],
          "pembelahan sel", "living-things-and-ecosystems"),

        H("B", "pola-pewarisan-sifat", "Pola-Pola Hereditas", "Pola Hereditas",
          "Peserta didik menjelaskan hukum Mendel, penyimpangan semu hukum Mendel (kodominan, epistasis, polimeri, komplementer), pautan dan pindah silang, determinasi seks, serta hereditas pada manusia.",
          "hukum Mendel I dan II, monohibrid dan dihibrid, intermediet, kodominan, epistasis-hipostasis, polimeri, gen komplementer, pautan seks, buta warna, hemofilia, golongan darah ABO",
          "Penyimpangan semu Mendel mengubah perbandingan fenotipe", "Interaksi gen dapat menghasilkan perbandingan 9 : 3 : 4, 12 : 3 : 1, 15 : 1, atau 9 : 7.",
          ["Hukum Mendel I (segregasi): pasangan alel berpisah saat pembentukan gamet. Hukum Mendel II (asortasi bebas): gen-gen untuk sifat berbeda berpasangan secara bebas, sehingga F2 dihibrid berfenotipe 9 : 3 : 3 : 1.",
           "Penyimpangan semu: kriptomeri (9 : 3 : 4), epistasis dominan (12 : 3 : 1), polimeri (15 : 1), dan gen komplementer (9 : 7). Pada kodominan kedua alel tampak, misalnya golongan darah AB.",
           "Gen buta warna dan hemofilia terpaut kromosom X dan resesif, sehingga lebih banyak diderita laki-laki (XᶜY). Perempuan pembawa (carrier) bergenotipe XᶜX."],
          [("Ibu pembawa buta warna (XᶜX) menikah dengan ayah normal (XY). Berapa peluang anak laki-lakinya buta warna?", ["Anak laki-laki menerima Y dari ayah.", "Dari ibu ia menerima Xᶜ atau X dengan peluang sama."], "50% dari anak laki-laki")],
          [("Buta warna lebih banyak diderita perempuan.", "Buta warna terpaut X resesif, sehingga lebih banyak diderita laki-laki."), ("Golongan darah AB menunjukkan sifat dominan penuh.", "IA dan IB kodominan sehingga keduanya tampak."),
           ("Perbandingan 15 : 1 berasal dari epistasis.", "15 : 1 adalah perbandingan polimeri.")],
          [("Apa itu pautan gen?", "Gen-gen yang terletak pada kromosom yang sama cenderung diwariskan bersama."),
           ("Apa itu gen letal?", "Gen yang menyebabkan kematian individu yang memilikinya dalam keadaan homozigot."),
           ("Bisakah orang tua bergolongan darah A dan B memiliki anak O?", "Bisa, jika ayah IAIO dan ibu IBIO, peluang anak IOIO adalah 25%.")],
          [("Perbandingan F2", [("dihibrid dominan penuh", "9 : 3 : 3 : 1"), ("kriptomeri", "9 : 3 : 4"), ("epistasis dominan", "12 : 3 : 1"), ("polimeri", "15 : 1"), ("gen komplementer", "9 : 7"),
                               ("monohibrid dominan penuh", "3 : 1"), ("monohibrid intermediet", "1 : 2 : 1"), ("epistasis resesif", "9 : 3 : 4")],
            "Berapa perbandingan fenotipe F2 pada ‘{k}’?", None, ("1 : 1 : 1 : 1", "13 : 3 : 0")),
           ("Golongan darah", [("IAIA", "golongan darah A"), ("IAIO", "golongan darah A"), ("IBIB", "golongan darah B"), ("IBIO", "golongan darah B"), ("IAIB", "golongan darah AB"), ("IOIO", "golongan darah O")],
            "Genotipe ‘{k}’ menghasilkan ...", "Genotipe mana yang menghasilkan ‘{v}’?", ("golongan darah Rh",)),
           ("Pewarisan pada manusia", [("buta warna", "terpaut kromosom X resesif"), ("hemofilia", "terpaut kromosom X resesif"), ("hipertrikosis (rambut di telinga)", "terpaut kromosom Y"),
                                      ("albinisme", "autosom resesif"), ("anemia sel sabit", "autosom resesif"), ("polidaktili", "autosom dominan"), ("brakidaktili", "autosom dominan"), ("thalasemia", "autosom resesif")],
            "Sifat ‘{k}’ diwariskan secara ...", "Manakah kelainan yang diwariskan secara ‘{v}’?")],
          ["Hukum Mendel I disebut hukum segregasi.", "F2 dihibrid dominan penuh berfenotipe 9 : 3 : 3 : 1.", "Golongan darah AB menunjukkan kodominan.",
           "Polimeri menghasilkan perbandingan 15 : 1.", "Buta warna terpaut kromosom X.", "Hemofilia lebih banyak diderita laki-laki.",
           "Gen pada kromosom yang sama cenderung diwariskan bersama.", "Albinisme diwariskan secara autosom resesif."],
          [("Hemofilia terpaut kromosom Y.", "Hemofilia terpaut kromosom X."), ("Gen komplementer menghasilkan 15 : 1.", "Gen komplementer menghasilkan 9 : 7."),
           ("Genotipe IAIO bergolongan darah O.", "IAIO bergolongan darah A."), ("Hukum Mendel II disebut hukum segregasi.", "Hukum Mendel II adalah asortasi bebas."),
           ("Polidaktili diwariskan secara resesif.", "Polidaktili diwariskan secara autosom dominan."), ("Perempuan carrier buta warna bergenotipe XᶜXᶜ.", "Perempuan carrier bergenotipe XᶜX.")],
          "pola hereditas", "living-things-and-ecosystems"),

        H("B", "mutasi", "Mutasi", "Mutasi",
          "Peserta didik menjelaskan pengertian mutasi, jenis mutasi gen dan kromosom, penyebab mutasi (mutagen), contoh kelainan akibat mutasi, serta dampak dan manfaatnya.",
          "mutasi gen (substitusi, insersi, delesi), mutasi kromosom (delesi, duplikasi, inversi, translokasi), aneuploidi dan euploidi, mutagen, sindrom Down, Turner, Klinefelter, poliploidi",
          "Mutasi adalah perubahan materi genetik", "Mutasi dapat terjadi pada gen atau kromosom, dan dapat merugikan, netral, atau menguntungkan.",
          ["Mutasi adalah perubahan materi genetik yang dapat diwariskan. Mutasi gen mengubah urutan basa DNA (substitusi, insersi, delesi). Mutasi kromosom mengubah struktur atau jumlah kromosom.",
           "Perubahan struktur kromosom: delesi, duplikasi, inversi, dan translokasi. Perubahan jumlah: aneuploidi (kelebihan atau kekurangan satu kromosom, misalnya sindrom Down 47,XX,+21) dan euploidi atau poliploidi (penggandaan set kromosom).",
           "Penyebab mutasi (mutagen) antara lain radiasi (sinar UV, sinar X), zat kimia (kolkisin, asap rokok), dan virus. Mutasi poliploidi dimanfaatkan untuk tanaman unggul, misalnya semangka tanpa biji."],
          [("Penderita sindrom Down memiliki 47 kromosom karena kelebihan kromosom nomor 21. Termasuk mutasi apakah ini?", ["Jumlah kromosom berubah satu.", "Perubahan satu kromosom disebut aneuploidi (trisomi)."], "aneuploidi (trisomi 21)")],
          [("Semua mutasi merugikan.", "Ada mutasi netral dan menguntungkan, misalnya tanaman poliploid yang buahnya besar."), ("Mutasi selalu diwariskan ke anak.", "Mutasi pada sel tubuh tidak diwariskan; hanya mutasi pada sel kelamin."),
           ("Sindrom Turner disebabkan kelebihan kromosom X.", "Sindrom Turner (45,X) disebabkan kekurangan satu kromosom X.")],
          [("Apa itu kolkisin?", "Zat kimia dari tanaman Colchicum yang menghambat benang spindel sehingga menghasilkan sel poliploid."),
           ("Apa contoh mutasi gen pada manusia?", "Anemia sel sabit akibat substitusi satu basa pada gen hemoglobin."),
           ("Bagaimana mencegah mutasi yang merugikan?", "Menghindari paparan radiasi berlebihan, tidak merokok, dan berhati-hati dengan zat kimia berbahaya.")],
          [("Jenis mutasi", [("satu basa diganti basa lain", "substitusi"), ("satu basa disisipkan", "insersi"), ("satu basa hilang", "delesi basa"), ("sebagian kromosom hilang", "delesi kromosom"),
                            ("sebagian kromosom berlipat ganda", "duplikasi"), ("sebagian kromosom terbalik urutannya", "inversi"), ("bagian kromosom berpindah ke kromosom lain yang bukan homolog", "translokasi"),
                            ("kelebihan atau kekurangan satu kromosom", "aneuploidi"), ("penggandaan seluruh set kromosom", "poliploidi")],
            "Perubahan ‘{k}’ disebut ...", "Apa yang dimaksud ‘{v}’?"),
           ("Kelainan kromosom", [("47,XX,+21 atau 47,XY,+21", "sindrom Down"), ("45,X", "sindrom Turner"), ("47,XXY", "sindrom Klinefelter"), ("47,XYY", "sindrom Jacobs"), ("47,+18", "sindrom Edwards"), ("47,+13", "sindrom Patau")],
            "Susunan kromosom ‘{k}’ menyebabkan ...", "Bagaimana susunan kromosom pada ‘{v}’?"),
           ("Mutagen", [("sinar ultraviolet", "mutagen fisika"), ("sinar X", "mutagen fisika"), ("sinar gamma", "mutagen fisika"), ("suhu tinggi", "mutagen fisika"), ("kolkisin", "mutagen kimia"), ("asap rokok", "mutagen kimia"),
                       ("pestisida tertentu", "mutagen kimia"), ("gas mustard", "mutagen kimia"), ("virus", "mutagen biologi"), ("bakteri tertentu", "mutagen biologi")],
            "‘{k}’ termasuk ...", "Manakah yang termasuk ‘{v}’?", ("mutagen gravitasi",))],
          ["Mutasi adalah perubahan materi genetik.", "Substitusi adalah penggantian satu basa.", "Sindrom Down disebabkan kelebihan kromosom 21.",
           "Sindrom Turner bersusunan kromosom 45,X.", "Kolkisin dapat menghasilkan tanaman poliploid.", "Sinar UV termasuk mutagen fisika.",
           "Mutasi pada sel kelamin dapat diwariskan.", "Semangka tanpa biji adalah hasil poliploidi."],
          [("Sindrom Klinefelter bersusunan 45,X.", "Sindrom Klinefelter bersusunan 47,XXY."), ("Kolkisin adalah mutagen biologi.", "Kolkisin adalah mutagen kimia."),
           ("Mutasi pada sel tubuh selalu diwariskan.", "Mutasi sel tubuh tidak diwariskan."), ("Inversi adalah hilangnya sebagian kromosom.", "Inversi adalah terbaliknya urutan bagian kromosom."),
           ("Semua mutasi bersifat menguntungkan.", "Mutasi dapat merugikan, netral, atau menguntungkan."), ("Virus termasuk mutagen kimia.", "Virus termasuk mutagen biologi.")],
          "mutasi", "living-things-and-ecosystems"),

        H("B", "evolusi", "Teori Evolusi", "Evolusi",
          "Peserta didik menjelaskan teori asal usul kehidupan, teori evolusi Lamarck dan Darwin, bukti evolusi (fosil, homologi, embriologi, molekuler), mekanisme evolusi (seleksi alam, mutasi, isolasi), dan spesiasi.",
          "abiogenesis dan biogenesis, Lamarck, Darwin, seleksi alam, bukti evolusi, organ homolog dan analog, hukum Hardy-Weinberg, spesiasi, isolasi reproduksi",
          "Seleksi alam memilih individu yang paling sesuai", "Variasi, perkembangbiakan berlebih, dan seleksi alam menyebabkan perubahan populasi dari generasi ke generasi.",
          ["Percobaan Redi, Spallanzani, dan Pasteur membuktikan biogenesis: makhluk hidup berasal dari makhluk hidup sebelumnya. Teori evolusi kimia Oparin dan percobaan Miller menjelaskan asal usul molekul organik.",
           "Lamarck berpendapat sifat yang diperoleh selama hidup diwariskan (teori ini tidak terbukti). Darwin menyatakan individu bervariasi, dan seleksi alam membuat individu yang paling sesuai bertahan dan berkembang biak.",
           "Bukti evolusi: fosil, organ homolog (asal sama, fungsi berbeda, misalnya tangan manusia dan sayap kelelawar), embriologi perbandingan, dan kemiripan DNA serta protein. Spesiasi terjadi karena isolasi geografis dan reproduksi."],
          [("Sayap burung dan sayap serangga sama-sama untuk terbang tetapi asal strukturnya berbeda. Termasuk organ apakah ini?", ["Fungsinya sama.", "Asal struktur berbeda disebut analog."], "organ analog")],
          [("Darwin menyatakan sifat yang dilatih diwariskan.", "Itu pendapat Lamarck; Darwin menekankan seleksi alam."), ("Evolusi terjadi pada satu individu selama hidupnya.", "Evolusi terjadi pada populasi dari generasi ke generasi."),
           ("Organ homolog memiliki fungsi yang sama.", "Organ homolog memiliki asal sama tetapi fungsi dapat berbeda.")],
          [("Apa contoh seleksi alam yang teramati?", "Ngengat Biston betularia di Inggris yang berwarna gelap menjadi lebih banyak saat pohon menghitam oleh polusi pabrik."),
           ("Apa itu hukum Hardy-Weinberg?", "Frekuensi alel dalam populasi tetap jika populasi besar, kawin acak, tidak ada mutasi, migrasi, dan seleksi."),
           ("Mengapa bakteri bisa kebal antibiotik?", "Bakteri yang secara kebetulan tahan antibiotik bertahan hidup dan berkembang biak, sehingga populasi menjadi kebal.")],
          [("Tokoh dan teori", [("menyatakan sifat yang sering dipakai diwariskan", "Jean-Baptiste Lamarck"), ("mengemukakan teori seleksi alam", "Charles Darwin"), ("membuktikan biogenesis dengan labu leher angsa", "Louis Pasteur"),
                               ("menguji abiogenesis dengan daging dalam toples tertutup", "Francesco Redi"), ("membuat percobaan pembentukan asam amino dari gas", "Stanley Miller"), ("mengemukakan teori evolusi kimia", "Alexander Oparin"),
                               ("meneliti fauna Indonesia dan seleksi alam bersama Darwin", "Alfred Russel Wallace"), ("memperkenalkan pola pewarisan dalam populasi", "Hardy dan Weinberg")],
            "Siapa yang ‘{k}’?", "Apa sumbangan ‘{v}’?"),
           ("Homolog atau analog", [("tangan manusia dan sayap kelelawar", "organ homolog"), ("sirip paus dan kaki depan kuda", "organ homolog"), ("kaki depan kucing dan sayap burung", "organ homolog"),
                                   ("tangan manusia dan kaki depan buaya", "organ homolog"), ("sayap burung dan sayap kupu-kupu", "organ analog"), ("sirip ikan dan sirip paus", "organ analog"), ("mata gurita dan mata manusia", "organ analog"),
                                   ("sayap kelelawar dan sayap serangga", "organ analog")],
            "‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("organ vestigial",)),
           ("Mekanisme evolusi", [("individu dalam spesies memiliki perbedaan sifat", "variasi"), ("individu yang sesuai lingkungan lebih banyak bertahan", "seleksi alam"), ("perubahan acak pada DNA", "mutasi"),
                                 ("populasi terpisah oleh laut atau gunung", "isolasi geografis"), ("dua populasi tidak lagi dapat kawin", "isolasi reproduksi"), ("terbentuknya spesies baru", "spesiasi"),
                                 ("perpindahan individu antarpopulasi", "migrasi (aliran gen)"), ("perubahan frekuensi alel secara kebetulan pada populasi kecil", "hanyutan genetik")],
            "‘{k}’ disebut ...", "Apa yang dimaksud ‘{v}’?")],
          ["Seleksi alam adalah gagasan utama Darwin.", "Evolusi terjadi pada populasi.", "Fosil adalah salah satu bukti evolusi.",
           "Organ homolog memiliki asal struktur yang sama.", "Sayap burung dan kupu-kupu adalah organ analog.", "Isolasi geografis dapat menyebabkan spesiasi.",
           "Pasteur membuktikan biogenesis.", "Mutasi menjadi sumber variasi genetik."],
          [("Lamarck mengemukakan seleksi alam.", "Seleksi alam dikemukakan Darwin; Lamarck tentang pewarisan sifat yang diperoleh."), ("Sayap burung dan sayap kelelawar adalah organ analog.", "Keduanya berasal dari kaki depan, jadi homolog."),
           ("Evolusi terjadi pada satu individu.", "Evolusi terjadi pada populasi."), ("Percobaan Miller membuktikan biogenesis.", "Percobaan Miller menunjukkan pembentukan molekul organik dari gas."),
           ("Spesiasi tidak memerlukan isolasi.", "Spesiasi umumnya terjadi karena isolasi geografis atau reproduksi."), ("Bakteri kebal antibiotik karena sengaja beradaptasi.", "Bakteri yang kebal terpilih oleh seleksi alam.")],
          "evolusi", "living-things-and-ecosystems"),
    ]
