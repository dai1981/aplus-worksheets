# -*- coding: utf-8 -*-
"""Indonesia / Kelas 11（Fase F, mata pelajaran pilihan Fisika, Kimia, dan Biologi）"""
import math
from id_sci import H, nq, num, it


# ------------------------------------------------------------ Fisika
def f_vektor(R):
    k = R.choice(["res", "hmax", "range", "waktu", "komp"])
    if k == "res":
        a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)])
        return nq("Dua gaya %d N dan %d N bekerja saling tegak lurus pada satu titik. Berapa resultannya?" % (a, b), c, [a + b, abs(a - b), (a + b) / 2], "N",
                  "R = √(%d² + %d²) = √%d = %d N." % (a, b, a * a + b * b, c))
    v0 = R.choice([10, 20, 30, 40])
    if k == "komp":
        ang, s, c = R.choice([(30, 0.5, math.sqrt(3) / 2), (60, math.sqrt(3) / 2, 0.5), (37, 0.6, 0.8), (53, 0.8, 0.6)])
        return nq("Bola ditendang dengan kecepatan %d m/s membentuk sudut %d° terhadap tanah (sin %d° = %s, cos %d° = %s). Berapa komponen kecepatan mendatarnya?" % (v0, ang, ang, num(s), ang, num(c)),
                  v0 * c, [v0 * s, v0, v0 * s * c], "m/s", "vx = v₀ cos θ = %d × %s = %s m/s." % (v0, num(c), num(v0 * c)))
    ang, s, c = R.choice([(30, 0.5, math.sqrt(3) / 2), (37, 0.6, 0.8), (53, 0.8, 0.6), (90, 1, 0)])
    if k == "hmax":
        h = (v0 * s) ** 2 / 20
        return nq("Peluru ditembakkan dengan kecepatan %d m/s dan sudut elevasi %d° (sin %d° = %s). Berapa tinggi maksimumnya? (g = 10 m/s²)" % (v0, ang, ang, num(s)), h,
                  [v0 * s / 10, (v0 * s) ** 2 / 10, v0 ** 2 / 20 if s != 1 else v0 ** 2 / 5], "m", "h = (v₀ sin θ)² ÷ 2g = (%s)² ÷ 20 = %s m." % (num(v0 * s), num(h)))
    if ang == 90:
        return None
    if k == "range":
        x = 2 * v0 * v0 * s * c / 10
        return nq("Bola ditendang %d m/s dengan sudut %d° (sin %d° = %s, cos %d° = %s). Berapa jarak mendatar terjauhnya? (g = 10 m/s²)" % (v0, ang, ang, num(s), ang, num(c)), x,
                  [v0 * v0 * s * c / 10, v0 * v0 / 10, 2 * v0 * s / 10], "m", "x = 2v₀² sin θ cos θ ÷ g = 2 × %d × %s × %s ÷ 10 = %s m." % (v0 * v0, num(s), num(c), num(x)))
    t = 2 * v0 * s / 10
    return nq("Bola dilempar %d m/s dengan sudut %d° (sin %d° = %s). Berapa lama bola di udara sampai jatuh kembali? (g = 10 m/s²)" % (v0, ang, ang, num(s)), t,
              [v0 * s / 10, 2 * v0 / 10, v0 * s], "s", "t = 2v₀ sin θ ÷ g = 2 × %d × %s ÷ 10 = %s s." % (v0, num(s), num(t)))


def f_newton(R):
    k = R.choice(["gesek", "lift-naik", "lift-turun", "dua", "miring"])
    g = 10
    if k == "gesek":
        m = R.choice([2, 4, 5, 10])
        mu = R.choice([0.1, 0.2, 0.3])
        F = R.choice([30, 40, 50, 60])
        a = (F - mu * m * g) / m
        if a <= 0:
            return None
        return nq("Balok %d kg ditarik mendatar dengan gaya %d N. Koefisien gesek kinetis %s. Berapa percepatan balok? (g = 10 m/s²)" % (m, F, num(mu)), a,
                  [F / m, (F + mu * m * g) / m, mu * g], "m/s²", "a = (F − μmg) ÷ m = (%d − %s) ÷ %d = %s m/s²." % (F, num(mu * m * g), m, num(a)))
    if k in ("lift-naik", "lift-turun"):
        m = R.choice([40, 50, 60])
        a = R.choice([1, 2, 3])
        N = m * (g + a) if k == "lift-naik" else m * (g - a)
        return nq("Anak bermassa %d kg berdiri di lift yang bergerak %s dengan percepatan %d m/s². Berapa gaya normal lantai lift? (g = 10 m/s²)" % (m, "naik" if k == "lift-naik" else "turun", a), N,
                  [m * g, m * (g - a) if k == "lift-naik" else m * (g + a), m * a], "N", "N = m(g %s a) = %d × %d = %d N." % ("+" if k == "lift-naik" else "−", m, g + a if k == "lift-naik" else g - a, N))
    if k == "dua":
        m1, m2 = R.choice([(2, 3), (1, 4), (3, 5), (2, 6)])
        F = R.choice([20, 40, 60])
        a = F / (m1 + m2)
        return nq("Dua balok %d kg dan %d kg bersentuhan di lantai licin dan didorong gaya %d N. Berapa percepatan sistem?" % (m1, m2, F), a, [F / m1, F / m2, F * (m1 + m2)], "m/s²",
                  "a = F ÷ (m₁ + m₂) = %d ÷ %d = %s m/s²." % (F, m1 + m2, num(a)))
    ang, s = R.choice([(30, 0.5), (37, 0.6), (53, 0.8)])
    return nq("Balok meluncur pada bidang miring licin bersudut %d° (sin %d° = %s). Berapa percepatannya? (g = 10 m/s²)" % (ang, ang, num(s)), g * s, [g, g * (1 - s), g / s], "m/s²",
              "a = g sin θ = 10 × %s = %s m/s²." % (num(s), num(g * s)))


def f_melingkar(R):
    k = R.choice(["v", "as", "Fs", "f"])
    r = R.choice([0.5, 1, 2, 4, 5])
    if k == "v":
        T = R.choice([2, 4, 5, 10])
        v = 2 * math.pi * r / T
        return nq("Benda bergerak melingkar beraturan dengan jari-jari %s m dan periode %d s. Berapa kelajuan linearnya? (π = 3,14)" % (num(r), T), 2 * 3.14 * r / T,
                  [3.14 * r / T, 2 * 3.14 * T / r, r / T], "m/s", "v = 2πr ÷ T = 2 × 3,14 × %s ÷ %d = %s m/s." % (num(r), T, num(2 * 3.14 * r / T)))
    v = R.choice([2, 4, 5, 10])
    if k == "as":
        return nq("Mobil mainan bergerak melingkar dengan kelajuan %d m/s pada jari-jari %s m. Berapa percepatan sentripetalnya?" % (v, num(r)), v * v / r, [v / r, v * r, v * v * r], "m/s²",
                  "as = v² ÷ r = %d ÷ %s = %s m/s²." % (v * v, num(r), num(v * v / r)))
    if k == "Fs":
        m = R.choice([0.5, 1, 2])
        return nq("Batu %s kg diikat tali dan diputar dengan kelajuan %d m/s pada jari-jari %s m. Berapa gaya sentripetalnya?" % (num(m), v, num(r)), m * v * v / r, [m * v / r, m * v * v, v * v / r], "N",
                  "Fs = m v² ÷ r = %s × %d ÷ %s = %s N." % (num(m), v * v, num(r), num(m * v * v / r)))
    n = R.choice([30, 60, 120, 300])
    t = R.choice([10, 30, 60])
    return nq("Roda berputar %d kali dalam %d s. Berapa frekuensinya?" % (n, t), n / t, [t / n, n * t, n / 60], "Hz", "f = n ÷ t = %d ÷ %d = %s Hz." % (n, t, num(n / t)))


def f_momentum(R):
    k = R.choice(["p", "I", "lenting", "tak"])
    if k == "p":
        m = R.choice([0.2, 0.5, 2, 60, 1000])
        v = R.choice([2, 5, 10, 20])
        return nq("Benda bermassa %s kg bergerak dengan kecepatan %d m/s. Berapa momentumnya?" % (num(m), v), m * v, [m / v, m * v * v / 2, m + v], "kg·m/s", "p = m × v = %s × %d = %s kg·m/s." % (num(m), v, num(m * v)))
    if k == "I":
        F = R.choice([50, 100, 200, 500])
        t = R.choice([0.01, 0.02, 0.05, 0.1])
        return nq("Bola ditendang dengan gaya %d N selama %s s. Berapa impuls yang diberikan?" % (F, num(t)), F * t, [F / t, F + t, F * t * 10], "N·s", "I = F × Δt = %d × %s = %s N·s." % (F, num(t), num(F * t)))
    m1, v1, m2 = R.choice([(2, 6, 1), (1, 9, 2), (3, 4, 1), (4, 5, 1), (2, 10, 3)])
    if k == "tak":
        v = m1 * v1 / (m1 + m2)
        return nq("Troli %d kg bergerak %d m/s menabrak troli %d kg yang diam, lalu keduanya menempel. Berapa kecepatan keduanya setelah tumbukan?" % (m1, v1, m2), v,
                  [v1, m1 * v1 / m2, v1 / 2 if v1 / 2 != v else v1 / 3], "m/s", "m₁v₁ = (m₁ + m₂)v′ → v′ = %d × %d ÷ %d = %s m/s." % (m1, v1, m1 + m2, num(v)))
    M, m, vp = R.choice([(4, 0.02, 400), (3, 0.01, 300), (5, 0.05, 200), (2, 0.01, 500)])
    vr = m * vp / M
    return nq("Senapan %d kg menembakkan peluru %s kg dengan kecepatan %d m/s. Berapa kecepatan mundur senapan?" % (M, num(m), vp), vr, [vp, M * vp / m, m * vp], "m/s",
              "Kekekalan momentum: M v_s = m v_p → v_s = %s × %d ÷ %d = %s m/s." % (num(m), vp, M, num(vr)))


def f_fluida_s(R):
    k = R.choice(["ph", "pt", "fa", "pas"])
    if k == "ph":
        rho, nm = R.choice([(1000, "air"), (1025, "air laut"), (800, "minyak")])
        h = R.choice([2, 5, 10, 20])
        return nq("Berapa tekanan hidrostatis pada kedalaman %d m di dalam %s (ρ = %s kg/m³, g = 10 m/s²)?" % (h, nm, num(rho)), rho * 10 * h, [rho * h, rho * 10 / h, 10 * h], "Pa",
                  "ph = ρgh = %s × 10 × %d = %s Pa." % (num(rho), h, num(rho * 10 * h)))
    if k == "pt":
        h = R.choice([5, 10, 20])
        return nq("Berapa tekanan total pada kedalaman %d m di danau jika tekanan udara 100.000 Pa? (ρ air = 1.000 kg/m³, g = 10 m/s²)" % h, 100000 + 10000 * h, [10000 * h, 100000, 100000 * h], "Pa",
                  "p = p₀ + ρgh = 100.000 + %s = %s Pa." % (num(10000 * h), num(100000 + 10000 * h)))
    if k == "fa":
        V = R.choice([0.002, 0.005, 0.01, 0.05])
        rho = R.choice([1000, 800])
        return nq("Benda bervolume %s m³ tercelup seluruhnya dalam zat cair bermassa jenis %d kg/m³. Berapa gaya apungnya? (g = 10 m/s²)" % (num(V), rho), rho * 10 * V, [rho * V, 10 * V, rho * 10 / V], "N",
                  "FA = ρ g V = %d × 10 × %s = %s N." % (rho, num(V), num(rho * 10 * V)))
    d1, d2 = R.choice([(2, 20), (4, 40), (5, 50), (1, 10)])
    F2 = R.choice([10000, 20000, 50000])
    F1 = F2 * (d1 / d2) ** 2
    return nq("Pengisap kecil dongkrak hidrolik berdiameter %d cm dan pengisap besar %d cm. Berapa gaya pada pengisap kecil untuk mengangkat beban %s N?" % (d1, d2, num(F2)), F1,
              [F2 * d1 / d2, F2 * (d2 / d1) ** 2, F2 / d2], "N", "F₁ = F₂ × (d₁/d₂)² = %s × (%d/%d)² = %s N." % (num(F2), d1, d2, num(F1)))


def f_fluida_d(R):
    k = R.choice(["Q", "kont", "tor", "volume"])
    if k == "Q":
        A = R.choice([0.01, 0.02, 0.05])
        v = R.choice([2, 3, 4, 5])
        return nq("Air mengalir dalam pipa berpenampang %s m² dengan kecepatan %d m/s. Berapa debitnya?" % (num(A), v), A * v, [A / v, v / A, A + v], "m³/s", "Q = A × v = %s × %d = %s m³/s." % (num(A), v, num(A * v)))
    if k == "kont":
        A1, A2 = R.choice([(4, 2), (6, 2), (10, 5), (8, 2)])
        v1 = R.choice([2, 3, 5])
        return nq("Pipa berpenampang %d cm² menyempit menjadi %d cm². Jika kecepatan air di bagian besar %d m/s, berapa kecepatan di bagian kecil?" % (A1, A2, v1), A1 * v1 / A2,
                  [A2 * v1 / A1, v1, A1 * v1], "m/s", "A₁v₁ = A₂v₂ → v₂ = %d × %d ÷ %d = %s m/s." % (A1, v1, A2, num(A1 * v1 / A2)))
    if k == "tor":
        h = R.choice([0.2, 0.45, 0.8, 1.25, 1.8, 3.2, 5])
        v = math.sqrt(20 * h)
        return nq("Tangki berisi air memiliki lubang kecil %s m di bawah permukaan air. Berapa kecepatan air keluar dari lubang? (g = 10 m/s²)" % num(h), v, [20 * h, 10 * h, math.sqrt(10 * h)], "m/s",
                  "Torricelli: v = √(2gh) = √(2 × 10 × %s) = %s m/s." % (num(h), num(v)))
    Q = R.choice([0.002, 0.005, 0.01])
    t = R.choice([60, 100, 300])
    return nq("Keran mengalirkan air dengan debit %s m³/s selama %d s. Berapa liter air yang keluar?" % (num(Q), t), Q * t * 1000, [Q * t, Q * 1000, Q * t * 100], "L",
              "V = Q × t = %s × %d = %s m³ = %s L." % (num(Q), t, num(Q * t), num(Q * t * 1000)))


def f_gelombang(R):
    k = R.choice(["v", "f", "dopp", "kedalaman"])
    if k == "v":
        lam = R.choice([0.5, 1.2, 2, 3])
        f = R.choice([5, 10, 50, 100])
        return nq("Gelombang memiliki panjang gelombang %s m dan frekuensi %d Hz. Berapa cepat rambatnya?" % (num(lam), f), lam * f, [lam / f, f / lam, lam + f], "m/s", "v = λf = %s × %d = %s m/s." % (num(lam), f, num(lam * f)))
    if k == "f":
        n = R.choice([10, 20, 30, 40])
        t = R.choice([2, 4, 5])
        return nq("Gabus di permukaan air naik turun %d kali dalam %d s. Berapa frekuensi gelombangnya?" % (n, t), n / t, [t / n, n * t, n - t], "Hz", "f = n ÷ t = %d ÷ %d = %s Hz." % (n, t, num(n / t)))
    if k == "dopp":
        fs = R.choice([680, 850, 1020])
        vs = R.choice([10, 20, 30])
        fp = fs * 340 / (340 - vs)
        return nq("Ambulans membunyikan sirene %d Hz dan mendekati pengamat yang diam dengan kecepatan %d m/s. Berapa frekuensi yang didengar pengamat? (cepat rambat bunyi 340 m/s)" % (fs, vs), fp,
                  [fs, fs * 340 / (340 + vs), fs + vs], "Hz", "fp = fs × v ÷ (v − vs) = %d × 340 ÷ %d = %s Hz." % (fs, 340 - vs, num(fp)))
    t = R.choice([0.2, 0.4, 1, 2, 4])
    v = 1500
    return nq("Sonar kapal menerima pantulan bunyi dari dasar laut %s s setelah dipancarkan. Berapa kedalaman laut? (cepat rambat bunyi di air 1.500 m/s)" % num(t), v * t / 2, [v * t, v / t, v * t * 2], "m",
              "d = v × t ÷ 2 = 1.500 × %s ÷ 2 = %s m (dibagi 2 karena bunyi pergi dan kembali)." % (num(t), num(v * t / 2)))


def f_termo(R):
    k = R.choice(["W", "dU", "carnot", "Q"])
    if k == "W":
        p = R.choice([100000, 200000, 150000])
        dV = R.choice([0.002, 0.005, 0.01])
        return nq("Gas memuai pada tekanan tetap %s Pa dari volume awal hingga bertambah %s m³. Berapa usaha yang dilakukan gas?" % (num(p), num(dV)), p * dV, [p / dV, p * dV * 10, dV / p * 1e9], "J",
                  "W = p × ΔV = %s × %s = %s J." % (num(p), num(dV), num(p * dV)))
    if k == "dU":
        Q = R.choice([500, 800, 1200, 2000])
        W = R.choice([200, 300, 400])
        return nq("Gas menyerap kalor %d J dan melakukan usaha %d J. Berapa perubahan energi dalamnya?" % (Q, W), Q - W, [Q + W, W - Q if W > Q else Q * W, Q], "J",
                  "Hukum I Termodinamika: ΔU = Q − W = %d − %d = %d J." % (Q, W, Q - W))
    if k == "carnot":
        Th, Tc = R.choice([(500, 300), (600, 300), (800, 400), (400, 300), (1000, 600)])
        e = (1 - Tc / Th) * 100
        return nq("Mesin Carnot bekerja di antara reservoir %d K dan %d K. Berapa efisiensi maksimumnya?" % (Th, Tc), e, [Tc / Th * 100, (Th - Tc), Th / Tc * 10], "%",
                  "η = (1 − T₂/T₁) × 100%% = (1 − %d/%d) × 100%% = %s%%." % (Tc, Th, num(e)))
    e = R.choice([0.2, 0.25, 0.4, 0.5])
    Qh = R.choice([1000, 2000, 4000])
    return nq("Mesin kalor berefisiensi %d%% menyerap kalor %s J dari reservoir panas. Berapa usaha yang dihasilkan?" % (int(e * 100), num(Qh)), e * Qh, [Qh - e * Qh, Qh / e, e * 100], "J",
              "W = η × Q₁ = %s × %s = %s J." % (num(e), num(Qh), num(e * Qh)))


# ------------------------------------------------------------ Kimia
MR = [("H₂O", 18), ("CO₂", 44), ("NaCl", 58.5), ("CH₄", 16), ("NH₃", 17), ("O₂", 32), ("C₆H₁₂O₆", 180), ("CaCO₃", 100), ("H₂SO₄", 98), ("NaOH", 40)]


def f_mol(R):
    k = R.choice(["n", "m", "N", "V", "Mr"])
    f, mr = R.choice(MR)
    if k == "Mr":
        parts = {"H₂O": "2(1) + 16", "CO₂": "12 + 2(16)", "CH₄": "12 + 4(1)", "NH₃": "14 + 3(1)", "CaCO₃": "40 + 12 + 3(16)", "NaOH": "23 + 16 + 1", "H₂SO₄": "2(1) + 32 + 4(16)", "C₆H₁₂O₆": "6(12) + 12(1) + 6(16)"}
        if f not in parts:
            return None
        return nq("Berapa massa molekul relatif (Mr) %s? (Ar H = 1, C = 12, N = 14, O = 16, Na = 23, S = 32, Ca = 40)" % f, mr, [mr - 16 if mr > 16 else mr + 16, mr + 2, mr * 2], "",
                  "Mr %s = %s = %s." % (f, parts[f], num(mr)))
    nmol = R.choice([0.1, 0.2, 0.5, 1, 2, 3])
    if k == "n":
        return nq("Berapa mol %s yang terdapat dalam %s g %s? (Mr = %s)" % (f, num(nmol * mr), f, num(mr)), nmol, [nmol * mr * mr, mr / (nmol * mr) if nmol != 1 else 2, nmol * mr], "mol",
                  "n = m ÷ Mr = %s ÷ %s = %s mol." % (num(nmol * mr), num(mr), num(nmol)))
    if k == "m":
        return nq("Berapa massa %s mol %s? (Mr = %s)" % (num(nmol), f, num(mr)), nmol * mr, [mr / nmol, nmol + mr, mr], "g", "m = n × Mr = %s × %s = %s g." % (num(nmol), num(mr), num(nmol * mr)))
    if k == "N":
        return nq("Berapa jumlah molekul dalam %s mol %s? (L = 6,02 × 10²³)" % (num(nmol), f), nmol * 6.02e23, [6.02e23 / nmol, nmol * 6.02e22, 6.02e23], "molekul",
                  "N = n × L = %s × 6,02 × 10²³ = %s molekul." % (num(nmol), num(nmol * 6.02e23)))
    if f not in ("CO₂", "CH₄", "NH₃", "O₂"):
        return None
    return nq("Berapa volume %s mol gas %s pada keadaan STP (0 °C, 1 atm)?" % (num(nmol), f), nmol * 22.4, [nmol * 24, 22.4 / nmol, nmol * 2.24], "L", "V = n × 22,4 L = %s × 22,4 = %s L." % (num(nmol), num(nmol * 22.4)))


def f_termokimia(R):
    k = R.choice(["q", "dH", "hess", "lepas"])
    if k == "q":
        m = R.choice([100, 200, 250, 500])
        dT = R.choice([5, 10, 12, 20])
        q = m * 4.2 * dT
        return nq("Sebanyak %d g air di kalorimeter naik suhunya %d °C. Berapa kalor yang diserap air? (c = 4,2 J/g°C)" % (m, dT), q, [m * dT, m * 4.2, q / 1000], "J", "q = m c ΔT = %d × 4,2 × %d = %s J." % (m, dT, num(q)))
    if k == "dH":
        q = R.choice([4200, 8400, 12600, 21000])
        n = R.choice([0.05, 0.1, 0.2])
        dh = q / n / 1000
        return nq("Reaksi %s mol zat melepaskan kalor %s J. Berapa ΔH reaksi per mol? (tulis nilai mutlaknya dalam kJ/mol)" % (num(n), num(q)), dh, [q * n / 1000, q / 1000, dh * 1000], "kJ/mol",
                  "ΔH = q ÷ n = %s J ÷ %s mol = %s kJ/mol (negatif karena eksoterm)." % (num(q), num(n), num(dh)))
    if k == "hess":
        a = R.choice([-394, -286, -110, -242])
        b = R.choice([-283, -92, -46, -572])
        return it("Reaksi A memiliki ΔH₁ = %s kJ dan reaksi B memiliki ΔH₂ = %s kJ. Jika reaksi C = A + B, berapa ΔH reaksi C?" % (num(a), num(b)), num(a + b) + " kJ",
                  [num(a - b) + " kJ", num(b - a) + " kJ", num(a * 2) + " kJ"], "Hukum Hess: ΔH₃ = ΔH₁ + ΔH₂ = %s + (%s) = %s kJ." % (num(a), num(b), num(a + b)))
    dh = R.choice([-890, -1368, -2220, -286])
    n = R.choice([0.5, 2, 3])
    return nq("Pembakaran 1 mol bahan bakar memiliki ΔH = %s kJ. Berapa kalor yang dilepaskan oleh %s mol bahan bakar itu?" % (num(dh), num(n)), -dh * n, [-dh / n, -dh, -dh * n * 1000], "kJ",
              "Kalor = %s mol × %s kJ/mol = %s kJ dilepaskan." % (num(n), num(-dh), num(-dh * n)))


def f_orde(R):
    k = R.choice(["satu", "dua", "nol", "kc", "gab"])
    x = R.choice([2, 3, 4, 5, 10])
    if k == "gab":
        y = R.choice([2, 3])
        return nq("Persamaan laju reaksi v = k[A][B]². Jika [A] dinaikkan %d kali dan [B] dinaikkan %d kali, laju menjadi berapa kali semula?" % (x, y), x * y * y, [x * y, x * x * y, x + y * y], "kali",
                  "Laju = %d × %d² = %d kali." % (x, y, x * y * y))
    if k == "satu":
        return nq("Laju reaksi berorde satu terhadap A. Jika konsentrasi A dinaikkan %d kali, laju reaksi menjadi berapa kali semula?" % x, x, [x * x, 1, x * x * x], "kali", "Orde satu: laju sebanding [A], jadi %d kali." % x)
    if k == "dua":
        return nq("Laju reaksi berorde dua terhadap A. Jika konsentrasi A dinaikkan %d kali, laju reaksi menjadi berapa kali semula?" % x, x * x, [x, 2 * x, x * x * x], "kali", "Orde dua: laju sebanding [A]², jadi %d² = %d kali." % (x, x * x))
    if k == "nol":
        return nq("Laju reaksi berorde nol terhadap B. Jika konsentrasi B dinaikkan %d kali, laju reaksi menjadi berapa kali semula?" % x, 1, [x, x * x, 0.5], "kali", "Orde nol: laju tidak bergantung pada [B], jadi tetap 1 kali.")
    a, b, c = R.choice([(0.2, 0.4, 0.4), (0.5, 0.5, 1), (0.1, 0.2, 0.6), (0.3, 0.6, 0.9)])
    Kc = c * c / (a * b)
    return nq("Pada kesetimbangan A(g) + B(g) ⇌ 2C(g), [A] = %s M, [B] = %s M, dan [C] = %s M. Berapa nilai Kc?" % (num(a), num(b), num(c)), Kc, [c / (a * b), a * b / (c * c), 2 * c / (a * b)], "",
              "Kc = [C]² ÷ ([A][B]) = %s² ÷ (%s × %s) = %s." % (num(c), num(a), num(b), num(Kc)))


def UNITS(g):
    return [
        H("F", "vektor-dan-gerak-parabola", "Vektor dan Gerak Parabola", "Vektor dan Gerak Parabola",
          "Peserta didik menerapkan konsep vektor (penjumlahan, penguraian, resultan) untuk menganalisis gerak dua dimensi, terutama gerak parabola, beserta tinggi maksimum, waktu, dan jangkauan.",
          "besaran vektor dan skalar, resultan vektor, penguraian vektor, gerak parabola, tinggi maksimum, jarak terjauh",
          "Gerak parabola = GLB mendatar + GLBB vertikal", "Pada arah mendatar kecepatannya tetap, pada arah tegak dipengaruhi gravitasi.",
          ["Besaran vektor memiliki nilai dan arah (perpindahan, kecepatan, gaya), sedangkan besaran skalar hanya nilai (jarak, massa, suhu). Dua vektor tegak lurus dijumlahkan dengan rumus Pythagoras.",
           "Vektor dapat diuraikan: vx = v cos θ dan vy = v sin θ. Gerak parabola adalah gabungan gerak lurus beraturan pada sumbu x dan gerak lurus berubah beraturan pada sumbu y.",
           "Tinggi maksimum h = (v₀ sin θ)² ÷ 2g, waktu di udara t = 2v₀ sin θ ÷ g, dan jarak terjauh x = v₀² sin 2θ ÷ g. Jangkauan terjauh dicapai pada sudut 45°."],
          [("Bola ditendang 20 m/s dengan sudut 30°. Berapa komponen kecepatan vertikal awalnya?", ["vy = v₀ sin θ.", "vy = 20 × 0,5 = 10 m/s."], "10 m/s")],
          [("Pada titik tertinggi kecepatan peluru nol.", "Pada titik tertinggi hanya kecepatan vertikal yang nol; kecepatan mendatar tetap ada."), ("Massa adalah besaran vektor.", "Massa tidak memiliki arah, jadi skalar."),
           ("Jangkauan terjauh dicapai pada sudut 60°.", "Jangkauan terjauh dicapai pada sudut 45°.")],
          [("Mengapa sudut 30° dan 60° menghasilkan jangkauan sama?", "Karena sin 60° = sin 120°; sudut yang jumlahnya 90° menghasilkan jarak mendatar sama."),
           ("Apa contoh gerak parabola?", "Bola basket yang dilempar ke ring, peluru meriam, dan air dari selang yang diarahkan miring."),
           ("Bagaimana menjumlahkan vektor yang tidak tegak lurus?", "Dengan rumus kosinus R² = A² + B² + 2AB cos θ atau dengan menguraikan ke sumbu x dan y.")],
          [("Vektor atau skalar", [("perpindahan", "besaran vektor"), ("kecepatan", "besaran vektor"), ("gaya", "besaran vektor"), ("percepatan", "besaran vektor"), ("momentum", "besaran vektor"),
                                  ("jarak", "besaran skalar"), ("kelajuan", "besaran skalar"), ("massa", "besaran skalar"), ("waktu", "besaran skalar"), ("energi", "besaran skalar"), ("suhu", "besaran skalar")],
            "‘{k}’ termasuk ...", "Manakah yang termasuk ‘{v}’?", ("besaran tensor",)),
           ("Gerak parabola", [("kecepatan pada arah mendatar", "tetap sepanjang lintasan"), ("kecepatan vertikal di titik tertinggi", "nol"), ("percepatan pada arah vertikal", "g ke bawah"),
                              ("percepatan pada arah mendatar", "nol"), ("sudut untuk jangkauan terjauh", "45°"), ("lintasan gerak", "berbentuk parabola"), ("gerak pada sumbu x", "gerak lurus beraturan"),
                              ("gerak pada sumbu y", "gerak lurus berubah beraturan")],
            "Pada gerak parabola, bagaimana ‘{k}’?", None, ("bertambah terus", "sama dengan v₀")),
           ("Rumus gerak dua dimensi", [("komponen kecepatan mendatar", "vx = v₀ cos θ"), ("komponen kecepatan tegak awal", "vy = v₀ sin θ"), ("tinggi maksimum", "h = (v₀ sin θ)² ÷ 2g"),
                                       ("waktu mencapai titik tertinggi", "t = v₀ sin θ ÷ g"), ("jarak mendatar terjauh", "x = v₀² sin 2θ ÷ g"), ("resultan dua vektor tegak lurus", "R = √(A² + B²)")],
            "Rumus apa untuk ‘{k}’?", "Rumus ‘{v}’ dipakai untuk menghitung ...")],
          ["Vektor memiliki nilai dan arah.", "Kecepatan mendatar pada gerak parabola tetap.", "Di titik tertinggi kecepatan vertikal nol.",
           "Jangkauan terjauh dicapai pada sudut 45°.", "vx = v₀ cos θ.", "Gerak parabola adalah gabungan GLB dan GLBB.",
           "Massa adalah besaran skalar.", "Resultan dua vektor tegak lurus dihitung dengan Pythagoras."],
          [("Kelajuan adalah besaran vektor.", "Kelajuan tidak memiliki arah, jadi skalar."), ("Kecepatan mendatar parabola berkurang terus.", "Kecepatan mendatar tetap jika gesekan udara diabaikan."),
           ("Di titik tertinggi kecepatan total nol.", "Kecepatan mendatar tetap ada di titik tertinggi."), ("Percepatan mendatar gerak parabola sama dengan g.", "Percepatan mendatar nol."),
           ("Resultan 3 N dan 4 N yang tegak lurus adalah 7 N.", "Resultannya √(9 + 16) = 5 N."), ("Sudut 30° dan 60° menghasilkan jangkauan berbeda.", "Kedua sudut itu menghasilkan jangkauan yang sama.")],
          "vektor dan gerak parabola", "forces-and-motion", calc=f_vektor),

        H("F", "dinamika-gerak-hukum-newton", "Dinamika Gerak: Penerapan Hukum Newton", "Dinamika Gerak",
          "Peserta didik menerapkan hukum Newton untuk menganalisis gerak benda pada bidang datar, bidang miring, lift, dan sistem benda, termasuk gaya normal, gaya gesek statis dan kinetis.",
          "hukum I, II, III Newton, gaya berat, gaya normal, gaya gesek statis dan kinetis, bidang miring, lift, sistem benda",
          "ΣF = m × a", "Gambarkan semua gaya pada benda, jumlahkan sesuai arah, lalu bagi dengan massa untuk mendapat percepatan.",
          ["Hukum II Newton: ΣF = m × a. Gaya-gaya yang bekerja antara lain gaya berat (w = mg), gaya normal (N) yang tegak lurus bidang, gaya tegang tali (T), dan gaya gesek (f).",
           "Gaya gesek statis bekerja saat benda masih diam (fs maks = μs N); gaya gesek kinetis bekerja saat benda bergerak (fk = μk N). Biasanya μs lebih besar daripada μk.",
           "Pada bidang miring licin, percepatan a = g sin θ. Di dalam lift yang dipercepat ke atas, gaya normal N = m(g + a) sehingga kita merasa lebih berat; ke bawah N = m(g − a)."],
          [("Balok 5 kg di lantai datar ditarik 30 N. Koefisien gesek kinetis 0,2. Berapa percepatannya? (g = 10 m/s²)", ["f = 0,2 × 50 = 10 N.", "ΣF = 30 − 10 = 20 N.", "a = 20 ÷ 5 = 4 m/s²."], "4 m/s²")],
          [("Gaya normal selalu sama dengan berat benda.", "Gaya normal bergantung keadaan, misalnya di bidang miring N = mg cos θ."), ("Gaya gesek selalu searah gerak benda.", "Gaya gesek berlawanan dengan arah gerak."),
           ("Di lift yang turun dipercepat kita merasa lebih berat.", "Di lift yang turun dipercepat gaya normal berkurang, kita merasa lebih ringan.")],
          [("Mengapa sulit mendorong lemari dari diam?", "Gaya gesek statis maksimum lebih besar daripada gaya gesek kinetis, sehingga awal menggeser butuh gaya lebih besar."),
           ("Apa itu diagram gaya bebas?", "Gambar satu benda dengan semua gaya yang bekerja padanya, dipakai untuk menyusun persamaan ΣF = ma."),
           ("Apa pasangan aksi-reaksi gaya berat?", "Gaya tarik bumi pada benda dan gaya tarik benda pada bumi; gaya normal bukan pasangan reaksi gaya berat.")],
          [("Jenis gaya", [("gaya tarik bumi pada benda", "gaya berat"), ("gaya tegak lurus permukaan bidang sentuh", "gaya normal"), ("gaya pada tali yang menegang", "gaya tegang tali"),
                          ("gaya penghambat saat benda masih diam", "gaya gesek statis"), ("gaya penghambat saat benda bergerak", "gaya gesek kinetis"), ("gaya ke arah pusat lingkaran", "gaya sentripetal"),
                          ("gaya pemulih pada pegas yang diregangkan", "gaya pegas"), ("gaya hambat udara pada benda jatuh", "gaya gesek udara")],
            "‘{k}’ disebut ...", "Apa yang dimaksud ‘{v}’?"),
           ("Gaya normal pada berbagai keadaan", [("benda diam di lantai datar", "N = mg"), ("benda di bidang miring bersudut θ", "N = mg cos θ"), ("orang di lift yang naik dipercepat", "N = m(g + a)"),
                                                ("orang di lift yang turun dipercepat", "N = m(g − a)"), ("orang di lift yang bergerak dengan kecepatan tetap", "N = mg"), ("benda di lantai ditekan ke bawah dengan gaya F", "N = mg + F"),
                                                ("benda di lantai ditarik ke atas dengan gaya F kurang dari berat", "N = mg − F")],
            "Berapa gaya normal untuk ‘{k}’?", None, ("N = 0 selalu", "N = ma")),
           ("Hukum Newton", [("benda diam tetap diam bila resultan gaya nol", "hukum I Newton"), ("penumpang terdorong ke depan saat mobil mengerem", "hukum I Newton"), ("percepatan sebanding dengan resultan gaya", "hukum II Newton"),
                            ("percepatan berbanding terbalik dengan massa", "hukum II Newton"), ("roket terdorong ke atas karena menyemburkan gas", "hukum III Newton"), ("tangan terasa sakit saat memukul meja", "hukum III Newton"),
                            ("ΣF = m × a", "hukum II Newton"), ("F aksi = −F reaksi", "hukum III Newton")],
            "‘{k}’ sesuai dengan ...", "Manakah pernyataan yang sesuai dengan ‘{v}’?", ("hukum gravitasi Newton",))],
          ["ΣF = m × a adalah hukum II Newton.", "Gaya gesek berlawanan dengan arah gerak.", "Pada bidang miring licin a = g sin θ.",
           "Gaya normal di bidang miring adalah mg cos θ.", "Di lift yang naik dipercepat gaya normal lebih besar dari berat.", "Gaya gesek kinetis = μk × N.",
           "Gaya aksi dan reaksi bekerja pada benda berbeda.", "Koefisien gesek statis biasanya lebih besar daripada kinetis."],
          [("Gaya normal selalu sama dengan mg.", "Gaya normal bergantung pada keadaan benda."), ("Di lift yang naik dengan kecepatan tetap kita merasa lebih berat.", "Pada kecepatan tetap N = mg."),
           ("Gaya gesek kinetis lebih besar daripada statis maksimum.", "Biasanya gesek statis maksimum lebih besar."), ("Percepatan pada bidang miring licin adalah g cos θ.", "Percepatannya g sin θ."),
           ("Gaya normal adalah reaksi dari gaya berat.", "Reaksi gaya berat adalah tarikan benda pada bumi."), ("Massa yang lebih besar membuat percepatan lebih besar untuk gaya yang sama.", "Untuk gaya sama, massa besar menghasilkan percepatan kecil.")],
          "dinamika gerak", "forces-and-motion", calc=f_newton),

        H("F", "gerak-melingkar", "Gerak Melingkar", "Gerak Melingkar",
          "Peserta didik menganalisis gerak melingkar beraturan: periode, frekuensi, kecepatan sudut, kelajuan linear, percepatan dan gaya sentripetal, serta hubungan roda-roda.",
          "periode, frekuensi, kecepatan sudut ω, kelajuan linear v = ωr, percepatan sentripetal, gaya sentripetal, hubungan roda-roda",
          "Gaya sentripetal selalu mengarah ke pusat lingkaran", "Pada gerak melingkar beraturan kelajuannya tetap tetapi arah kecepatannya terus berubah.",
          ["Periode (T) adalah waktu untuk satu putaran, frekuensi (f) adalah banyak putaran tiap sekon, f = 1/T. Kecepatan sudut ω = 2πf, dan kelajuan linear v = ωr = 2πr/T.",
           "Walaupun kelajuannya tetap, arah kecepatan selalu berubah sehingga ada percepatan sentripetal as = v²/r yang mengarah ke pusat. Gaya penyebabnya disebut gaya sentripetal Fs = mv²/r.",
           "Roda-roda yang sepusat memiliki kecepatan sudut sama. Roda yang bersinggungan atau dihubungkan rantai memiliki kelajuan linear sama, misalnya gir sepeda."],
          [("Roda berjari-jari 0,5 m berputar 2 kali per sekon. Berapa kelajuan linear titik di tepinya? (π = 3,14)", ["ω = 2πf = 2 × 3,14 × 2 = 12,56 rad/s.", "v = ωr = 12,56 × 0,5 = 6,28 m/s."], "6,28 m/s")],
          [("Gerak melingkar beraturan tidak memiliki percepatan.", "Arah kecepatan berubah sehingga ada percepatan sentripetal."), ("Gaya sentripetal mengarah keluar lingkaran.", "Gaya sentripetal mengarah ke pusat lingkaran."),
           ("Roda bersinggungan memiliki kecepatan sudut sama.", "Roda bersinggungan memiliki kelajuan linear sama; roda sepusat yang ω-nya sama.")],
          [("Apa yang menyediakan gaya sentripetal pada mobil di tikungan?", "Gaya gesek antara ban dan jalan. Jalan sering dibuat miring agar lebih aman."),
           ("Mengapa air di ember yang diputar vertikal tidak tumpah?", "Pada titik tertinggi, gaya berat dan gaya normal ember berperan sebagai gaya sentripetal jika putarannya cukup cepat."),
           ("Apa satuan kecepatan sudut?", "Radian per sekon (rad/s). Satu putaran = 2π radian.")],
          [("Besaran gerak melingkar", [("periode", "waktu untuk satu putaran"), ("frekuensi", "banyak putaran setiap sekon"), ("kecepatan sudut", "besar sudut yang ditempuh setiap sekon"),
                                       ("kelajuan linear", "panjang busur yang ditempuh setiap sekon"), ("percepatan sentripetal", "percepatan yang mengarah ke pusat lingkaran"), ("gaya sentripetal", "gaya yang menyebabkan benda bergerak melingkar"),
                                       ("radian", "satuan sudut, satu putaran sama dengan 2π")],
            "Apa arti ‘{k}’?", "Besaran apa yang berarti ‘{v}’?"),
           ("Rumus gerak melingkar", [("hubungan frekuensi dan periode", "f = 1/T"), ("kecepatan sudut", "ω = 2πf"), ("kelajuan linear", "v = ωr"), ("percepatan sentripetal", "as = v²/r"),
                                     ("gaya sentripetal", "Fs = mv²/r"), ("roda sepusat", "ω₁ = ω₂"), ("roda bersinggungan atau dihubungkan rantai", "v₁ = v₂")],
            "Rumus apa untuk ‘{k}’?", "Rumus ‘{v}’ menyatakan ...", ("F = ma²",)),
           ("Penyedia gaya sentripetal", [("mobil berbelok di tikungan datar", "gaya gesek ban dan jalan"), ("bulan mengelilingi bumi", "gaya gravitasi"), ("batu diikat tali dan diputar", "gaya tegang tali"),
                                         ("elektron mengelilingi inti atom", "gaya listrik"), ("satelit mengorbit bumi", "gaya gravitasi"), ("penumpang komidi putar", "gaya dorong dinding atau sandaran kursi")],
            "Gaya apa yang menjadi gaya sentripetal pada ‘{k}’?", None, ("gaya apung", "gaya magnet bumi"))],
          ["Pada gerak melingkar beraturan kelajuan tetap.", "Arah kecepatan pada gerak melingkar selalu berubah.", "Percepatan sentripetal mengarah ke pusat.",
           "Frekuensi adalah kebalikan periode.", "v = ωr.", "Roda sepusat memiliki kecepatan sudut sama.",
           "Gaya gravitasi menjadi gaya sentripetal pada satelit.", "Satu putaran sama dengan 2π radian."],
          [("Percepatan sentripetal mengarah keluar lingkaran.", "Percepatan sentripetal mengarah ke pusat."), ("Gerak melingkar beraturan tidak memiliki percepatan.", "Ada percepatan sentripetal."),
           ("Roda yang dihubungkan rantai memiliki ω sama.", "Roda yang dihubungkan rantai memiliki kelajuan linear sama."), ("Periode adalah banyak putaran tiap sekon.", "Itu frekuensi; periode adalah waktu satu putaran."),
           ("as = v × r.", "as = v² ÷ r."), ("Satu putaran sama dengan π radian.", "Satu putaran sama dengan 2π radian.")],
          "gerak melingkar", "forces-and-motion", calc=f_melingkar),

        H("F", "momentum-dan-impuls", "Momentum dan Impuls", "Momentum dan Impuls",
          "Peserta didik menjelaskan momentum, impuls, hubungan impuls dengan perubahan momentum, hukum kekekalan momentum, dan jenis tumbukan serta penerapannya.",
          "momentum p = mv, impuls I = FΔt, I = Δp, hukum kekekalan momentum, tumbukan lenting sempurna, lenting sebagian, tidak lenting, roket",
          "Impuls = perubahan momentum", "Jika tidak ada gaya luar, momentum total sistem sebelum dan sesudah tumbukan sama.",
          ["Momentum adalah hasil kali massa dan kecepatan: p = m × v (kg·m/s), dan merupakan besaran vektor. Impuls adalah hasil kali gaya dan selang waktu: I = F × Δt (N·s).",
           "Impuls sama dengan perubahan momentum: F × Δt = m(v₂ − v₁). Memperpanjang waktu tumbukan memperkecil gaya, seperti airbag mobil dan matras lompat tinggi.",
           "Hukum kekekalan momentum: m₁v₁ + m₂v₂ = m₁v₁′ + m₂v₂′. Pada tumbukan lenting sempurna energi kinetik kekal, pada tumbukan tidak lenting kedua benda menyatu setelah tumbukan."],
          [("Bola 0,2 kg datang 10 m/s lalu dipukul balik 15 m/s. Berapa besar impulsnya?", ["Arah balik diberi tanda negatif.", "Δp = 0,2 × (−15 − 10) = −5 kg·m/s."], "5 N·s")],
          [("Momentum adalah besaran skalar.", "Momentum memiliki arah, jadi vektor."), ("Airbag memperbesar gaya tumbukan.", "Airbag memperpanjang waktu tumbukan sehingga gayanya kecil."),
           ("Pada semua tumbukan energi kinetik kekal.", "Energi kinetik hanya kekal pada tumbukan lenting sempurna.")],
          [("Apa itu koefisien restitusi?", "Ukuran kelentingan tumbukan, e = −(v₂′ − v₁′)/(v₂ − v₁). Lenting sempurna e = 1, tidak lenting e = 0."),
           ("Bagaimana roket bergerak di ruang hampa?", "Roket menyemburkan gas ke belakang dengan momentum besar, sehingga roket mendapat momentum ke depan (kekekalan momentum)."),
           ("Mengapa kaki ditekuk saat mendarat dari lompatan?", "Agar waktu perubahan momentum lebih lama sehingga gaya pada kaki lebih kecil.")],
          [("Jenis tumbukan", [("koefisien restitusi e = 1", "lenting sempurna"), ("energi kinetik total kekal", "lenting sempurna"), ("tumbukan antarmolekul gas ideal", "lenting sempurna"),
                              ("koefisien restitusi 0 < e < 1", "lenting sebagian"), ("bola dijatuhkan dan memantul makin rendah", "lenting sebagian"), ("koefisien restitusi e = 0", "tidak lenting sama sekali"),
                              ("dua benda menyatu setelah bertumbukan", "tidak lenting sama sekali"), ("peluru bersarang di balok kayu", "tidak lenting sama sekali")],
            "‘{k}’ menunjukkan tumbukan ...", "Manakah ciri tumbukan ‘{v}’?", ("tumbukan magnetik",)),
           ("Penerapan impuls", [("airbag mobil", "memperpanjang waktu tumbukan agar gaya kecil"), ("matras lompat tinggi", "memperpanjang waktu tumbukan agar gaya kecil"), ("helm berlapis busa", "memperpanjang waktu tumbukan agar gaya kecil"),
                                ("menekuk lutut saat mendarat", "memperpanjang waktu tumbukan agar gaya kecil"), ("palu dari besi keras", "memperpendek waktu tumbukan agar gaya besar"), ("karate memukul papan dengan cepat", "memperpendek waktu tumbukan agar gaya besar"),
                                ("roket menyemburkan gas", "kekekalan momentum"), ("senapan terdorong ke belakang saat ditembakkan", "kekekalan momentum")],
            "Prinsip apa yang dimanfaatkan ‘{k}’?", "Manakah contoh ‘{v}’?"),
           ("Istilah momentum", [("momentum", "hasil kali massa dan kecepatan"), ("impuls", "hasil kali gaya dan selang waktu"), ("hukum kekekalan momentum", "momentum total tetap jika tidak ada gaya luar"),
                                ("koefisien restitusi", "ukuran kelentingan tumbukan"), ("satuan momentum", "kg·m/s"), ("satuan impuls", "N·s"), ("teorema impuls-momentum", "impuls sama dengan perubahan momentum")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Momentum adalah besaran vektor.", "Impuls sama dengan perubahan momentum.", "Airbag memperkecil gaya dengan memperpanjang waktu tumbukan.",
           "Pada tumbukan lenting sempurna energi kinetik kekal.", "Pada tumbukan tidak lenting kedua benda menyatu.", "Momentum total tetap jika tidak ada gaya luar.",
           "Satuan impuls adalah N·s.", "Roket bergerak berdasarkan kekekalan momentum."],
          [("Satuan momentum adalah N/s.", "Satuan momentum adalah kg·m/s."), ("Pada tumbukan tidak lenting energi kinetik kekal.", "Energi kinetik hanya kekal pada lenting sempurna."),
           ("Matras memperpendek waktu tumbukan.", "Matras memperpanjang waktu tumbukan."), ("Koefisien restitusi lenting sempurna adalah 0.", "Lenting sempurna e = 1."),
           ("Momentum benda diam sangat besar.", "Benda diam momentumnya nol."), ("Roket memerlukan udara untuk terdorong.", "Roket terdorong karena kekekalan momentum, tanpa perlu udara.")],
          "momentum dan impuls", "forces-and-motion", calc=f_momentum),

        H("F", "fluida-statis", "Fluida Statis", "Fluida Statis",
          "Peserta didik menerapkan konsep tekanan hidrostatis, hukum utama hidrostatis, hukum Pascal, hukum Archimedes, tegangan permukaan, dan kapilaritas dalam menyelesaikan masalah.",
          "tekanan hidrostatis p = ρgh, tekanan total, hukum Pascal, hukum Archimedes, terapung, melayang, tenggelam, tegangan permukaan, kapilaritas, viskositas",
          "Tekanan zat cair bergantung pada kedalaman", "Hukum Pascal meneruskan tekanan ke segala arah. Gaya apung sama dengan berat zat cair yang dipindahkan.",
          ["Tekanan hidrostatis p = ρgh. Tekanan total di kedalaman h adalah p = p₀ + ρgh dengan p₀ tekanan udara. Titik-titik pada kedalaman sama dalam zat cair sejenis bertekanan sama (hukum utama hidrostatis).",
           "Hukum Pascal: F₁/A₁ = F₂/A₂, dipakai pada dongkrak dan rem hidrolik. Hukum Archimedes: FA = ρ zat cair × g × V tercelup.",
           "Tegangan permukaan membuat nyamuk dapat berdiri di atas air. Kapilaritas adalah naik atau turunnya zat cair dalam pipa sempit, misalnya minyak naik pada sumbu kompor."],
          [("Pengisap kecil dongkrak berdiameter 2 cm dan besar 20 cm. Berapa gaya untuk mengangkat mobil 10.000 N?", ["Perbandingan luas = (20/2)² = 100.", "F₁ = 10.000 ÷ 100 = 100 N."], "100 N")],
          [("Tekanan hidrostatis bergantung pada bentuk wadah.", "Tekanan hidrostatis hanya bergantung pada ρ, g, dan kedalaman."), ("Gaya apung bergantung pada massa benda.", "Gaya apung bergantung pada volume yang tercelup dan massa jenis zat cair."),
           ("Perbandingan gaya pada dongkrak sama dengan perbandingan diameter.", "Perbandingan gaya sama dengan perbandingan luas, yaitu kuadrat diameter.")],
          [("Mengapa telur terapung di air garam?", "Air garam bermassa jenis lebih besar, sehingga gaya apung pada telur lebih besar daripada beratnya."),
           ("Apa itu viskositas?", "Kekentalan fluida, yaitu besarnya gesekan di dalam fluida. Madu lebih kental daripada air."),
           ("Mengapa kapal selam bisa melayang?", "Kapal selam mengatur jumlah air di tangki pemberat sehingga massa jenis rata-ratanya sama dengan air laut.")],
          [("Hukum dan penerapannya", [("dongkrak hidrolik", "hukum Pascal"), ("rem hidrolik", "hukum Pascal"), ("pompa hidrolik ban", "hukum Pascal"), ("kapal laut", "hukum Archimedes"),
                                      ("hidrometer", "hukum Archimedes"), ("galangan kapal terapung", "hukum Archimedes"), ("balon udara", "hukum Archimedes"), ("pipa U dua zat cair", "hukum utama hidrostatis"),
                                      ("nyamuk berdiri di atas air", "tegangan permukaan"), ("minyak naik pada sumbu kompor", "kapilaritas")],
            "‘{k}’ berkaitan dengan ...", "Manakah penerapan ‘{v}’?", ("hukum Bernoulli",)),
           ("Terapung, melayang, tenggelam", [("massa jenis benda lebih kecil dari zat cair", "terapung"), ("gaya apung maksimum lebih besar dari berat benda", "terapung"), ("massa jenis benda sama dengan zat cair", "melayang"),
                                             ("gaya apung sama dengan berat dan benda di tengah zat cair", "melayang"), ("massa jenis benda lebih besar dari zat cair", "tenggelam"), ("berat benda lebih besar dari gaya apung maksimum", "tenggelam")],
            "Benda akan ... jika ‘{k}’.", "Manakah syarat benda ‘{v}’?", ("larut",)),
           ("Istilah fluida statis", [("tekanan hidrostatis", "tekanan zat cair diam karena beratnya"), ("hukum utama hidrostatis", "titik pada kedalaman sama bertekanan sama"), ("gaya apung", "gaya ke atas oleh zat cair pada benda tercelup"),
                                     ("tegangan permukaan", "kecenderungan permukaan zat cair untuk menegang"), ("kapilaritas", "naik turunnya zat cair dalam pipa sempit"), ("viskositas", "ukuran kekentalan fluida"),
                                     ("meniskus cekung", "permukaan air di dalam pipa kaca yang melengkung ke bawah")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Tekanan hidrostatis p = ρgh.", "Tekanan total = tekanan udara + tekanan hidrostatis.", "Dongkrak hidrolik bekerja berdasarkan hukum Pascal.",
           "Gaya apung sama dengan berat zat cair yang dipindahkan.", "Benda melayang jika massa jenisnya sama dengan zat cair.", "Minyak naik pada sumbu kompor karena kapilaritas.",
           "Titik pada kedalaman sama dalam zat cair sejenis bertekanan sama.", "Viskositas menyatakan kekentalan fluida."],
          [("Tekanan hidrostatis bergantung pada luas dasar wadah.", "Tekanan hidrostatis tidak bergantung pada luas wadah."), ("Benda tenggelam jika massa jenisnya lebih kecil dari zat cair.", "Benda tenggelam jika massa jenisnya lebih besar."),
           ("Hidrometer bekerja berdasarkan hukum Pascal.", "Hidrometer bekerja berdasarkan hukum Archimedes."), ("Tegangan permukaan membuat minyak naik di sumbu.", "Itu kapilaritas."),
           ("Gaya apung tidak bergantung pada massa jenis zat cair.", "FA = ρ g V, jadi bergantung pada massa jenis zat cair."), ("Air lebih kental daripada madu.", "Madu lebih kental daripada air.")],
          "fluida statis", "forces-and-motion", calc=f_fluida_s),

        H("F", "fluida-dinamis", "Fluida Dinamis", "Fluida Dinamis",
          "Peserta didik menjelaskan fluida ideal, debit, persamaan kontinuitas, asas Bernoulli, teorema Torricelli, serta penerapannya pada venturimeter, gaya angkat pesawat, dan alat penyemprot.",
          "fluida ideal, debit Q = Av, kontinuitas A₁v₁ = A₂v₂, asas Bernoulli, Torricelli v = √(2gh), venturimeter, gaya angkat sayap",
          "Di pipa yang sempit aliran lebih cepat", "Persamaan kontinuitas: A₁v₁ = A₂v₂. Asas Bernoulli: tempat yang alirannya cepat bertekanan rendah.",
          ["Fluida ideal tidak kompresibel, tidak kental, dan alirannya tunak. Debit adalah volume fluida yang mengalir tiap sekon: Q = V/t = A × v.",
           "Persamaan kontinuitas: A₁v₁ = A₂v₂. Karena itu saat ujung selang dipencet, air memancar lebih cepat.",
           "Asas Bernoulli: p + ½ρv² + ρgh tetap sepanjang aliran. Kecepatan besar berarti tekanan kecil. Teorema Torricelli: kecepatan air dari lubang tangki v = √(2gh)."],
          [("Air keluar dari lubang tangki yang berada 5 m di bawah permukaan air. Berapa kecepatannya? (g = 10 m/s²)", ["v = √(2gh).", "v = √(2 × 10 × 5) = √100 = 10 m/s."], "10 m/s")],
          [("Di bagian pipa yang sempit kecepatan aliran lebih kecil.", "Di bagian sempit kecepatan lebih besar (kontinuitas)."), ("Tekanan fluida lebih besar di tempat alirannya cepat.", "Menurut Bernoulli, aliran cepat bertekanan rendah."),
           ("Debit adalah kecepatan aliran.", "Debit adalah volume fluida yang mengalir tiap sekon.")],
          [("Bagaimana sayap pesawat menghasilkan gaya angkat?", "Udara di atas sayap mengalir lebih cepat sehingga tekanannya lebih kecil daripada di bawah sayap, menghasilkan gaya angkat."),
           ("Apa itu venturimeter?", "Alat untuk mengukur kecepatan aliran fluida dalam pipa berdasarkan perbedaan tekanan di bagian lebar dan sempit."),
           ("Mengapa atap rumah bisa terangkat saat angin kencang?", "Angin cepat di atas atap menurunkan tekanan, sedangkan tekanan udara di dalam rumah lebih besar.")],
          [("Penerapan fluida dinamis", [("gaya angkat sayap pesawat", "asas Bernoulli"), ("penyemprot obat nyamuk", "asas Bernoulli"), ("karburator kendaraan", "asas Bernoulli"), ("venturimeter", "asas Bernoulli"),
                                        ("tabung pitot pengukur kecepatan pesawat", "asas Bernoulli"), ("ujung selang dipencet agar air memancar jauh", "persamaan kontinuitas"), ("aliran sungai lebih deras di bagian sempit", "persamaan kontinuitas"),
                                        ("air memancar dari lubang tangki", "teorema Torricelli")],
            "‘{k}’ dijelaskan dengan ...", "Manakah penerapan ‘{v}’?", ("hukum Pascal",)),
           ("Rumus fluida dinamis", [("debit", "Q = A × v"), ("debit dari volume dan waktu", "Q = V ÷ t"), ("persamaan kontinuitas", "A₁v₁ = A₂v₂"), ("kecepatan air dari lubang tangki", "v = √(2gh)"),
                                    ("asas Bernoulli", "p + ½ρv² + ρgh = tetap"), ("jarak pancaran air dari lubang tangki", "x = 2√(h × H)")],
            "Rumus apa untuk ‘{k}’?", "Rumus ‘{v}’ dipakai untuk ...", ("F₁/A₁ = F₂/A₂",)),
           ("Ciri fluida", [("tidak dapat dimampatkan", "fluida ideal"), ("tidak memiliki kekentalan", "fluida ideal"), ("alirannya tunak (stasioner)", "fluida ideal"),
                           ("kecepatan di setiap titik tetap terhadap waktu", "aliran laminar"), ("aliran berputar-putar dan tidak teratur", "aliran turbulen"), ("asap rokok yang mula-mula lurus lalu bergolak", "aliran laminar berubah menjadi turbulen")],
            "Ciri ‘{k}’ dimiliki ...", None, ("fluida padat", "gas mulia"))],
          ["Debit adalah volume fluida tiap satuan waktu.", "Di pipa sempit kecepatan aliran lebih besar.", "Aliran cepat memiliki tekanan rendah.",
           "Gaya angkat pesawat dijelaskan dengan asas Bernoulli.", "Kecepatan air dari lubang tangki v = √(2gh).", "Fluida ideal tidak kompresibel.",
           "Penyemprot obat nyamuk memanfaatkan asas Bernoulli.", "A₁v₁ = A₂v₂ adalah persamaan kontinuitas."],
          [("Di pipa lebar aliran lebih cepat.", "Di pipa lebar aliran lebih lambat."), ("Aliran cepat bertekanan tinggi.", "Aliran cepat bertekanan rendah."),
           ("Torricelli menyatakan v = 2gh.", "Torricelli menyatakan v = √(2gh)."), ("Dongkrak hidrolik bekerja berdasarkan Bernoulli.", "Dongkrak hidrolik bekerja berdasarkan hukum Pascal."),
           ("Fluida ideal sangat kental.", "Fluida ideal tidak kental."), ("Debit satuannya m/s.", "Debit satuannya m³/s.")],
          "fluida dinamis", "forces-and-motion", calc=f_fluida_d),

        H("F", "gelombang-mekanik-dan-bunyi", "Gelombang Mekanik dan Bunyi", "Gelombang dan Bunyi",
          "Peserta didik menjelaskan ciri gelombang mekanik, gelombang berjalan dan stasioner, sifat-sifat gelombang, intensitas dan taraf intensitas bunyi, efek Doppler, serta pemanfaatan gelombang bunyi.",
          "gelombang transversal dan longitudinal, v = λf, pemantulan, pembiasan, difraksi, interferensi, gelombang stasioner, efek Doppler, sonar",
          "Cepat rambat gelombang = panjang gelombang × frekuensi", "Sumber bunyi yang mendekat terdengar lebih tinggi, yang menjauh terdengar lebih rendah (efek Doppler).",
          ["Gelombang mekanik memerlukan medium. Gelombang transversal arah getarnya tegak lurus arah rambat, longitudinal sejajar. Cepat rambat v = λf.",
           "Sifat gelombang: pemantulan, pembiasan, difraksi (pelenturan melewati celah), dan interferensi (perpaduan). Gelombang stasioner terbentuk dari perpaduan gelombang datang dan pantul dengan simpul dan perut.",
           "Efek Doppler: frekuensi yang didengar berubah jika sumber atau pendengar bergerak. fp = fs (v ± vp)/(v ∓ vs). Sonar memakai pantulan bunyi: kedalaman d = v × t ÷ 2."],
          [("Pantulan sonar diterima 2 s setelah dipancarkan. Cepat rambat bunyi di air 1.500 m/s. Berapa kedalaman laut?", ["Bunyi pergi dan pulang.", "d = 1.500 × 2 ÷ 2 = 1.500 m."], "1.500 m")],
          [("Gelombang memindahkan medium perantaranya.", "Gelombang memindahkan energi, bukan mediumnya."), ("Sumber bunyi yang menjauh terdengar lebih tinggi.", "Sumber yang menjauh terdengar lebih rendah."),
           ("Kedalaman sonar = v × t.", "Hasil v × t dibagi 2 karena bunyi pergi dan kembali.")],
          [("Apa itu difraksi?", "Pelenturan gelombang saat melewati celah atau penghalang, sehingga bunyi dapat terdengar dari balik tembok."),
           ("Apa itu pelayangan bunyi?", "Kuat lemahnya bunyi yang bergantian karena dua bunyi berfrekuensi hampir sama terdengar bersamaan."),
           ("Apa itu taraf intensitas?", "Ukuran kuat bunyi dalam desibel (dB). Percakapan biasa sekitar 60 dB; di atas 85 dB berbahaya untuk pendengaran jangka panjang.")],
          [("Sifat gelombang", [("bunyi gema di gua", "pemantulan"), ("sonar mengukur kedalaman laut", "pemantulan"), ("gelombang laut berbelok saat mendekati pantai yang dangkal", "pembiasan"),
                               ("bunyi lebih jelas terdengar pada malam hari", "pembiasan"), ("bunyi terdengar dari balik tembok", "difraksi"), ("gelombang air melentur setelah melewati celah", "difraksi"),
                               ("bunyi dua pengeras suara terdengar keras dan lemah bergantian", "interferensi"), ("pola terang gelap riak air dari dua sumber", "interferensi")],
            "Peristiwa ‘{k}’ menunjukkan ...", "Manakah contoh ‘{v}’?", ("polarisasi",)),
           ("Efek Doppler", [("ambulans mendekati pendengar yang diam", "frekuensi terdengar lebih tinggi"), ("ambulans menjauhi pendengar yang diam", "frekuensi terdengar lebih rendah"),
                            ("pendengar bergerak mendekati sumber yang diam", "frekuensi terdengar lebih tinggi"), ("pendengar bergerak menjauhi sumber yang diam", "frekuensi terdengar lebih rendah"),
                            ("sumber dan pendengar diam", "frekuensi terdengar sama dengan sumber"), ("sumber dan pendengar bergerak searah dengan kecepatan sama", "frekuensi terdengar sama dengan sumber")],
            "Apa yang terjadi jika ‘{k}’?", None, ("bunyi tidak terdengar sama sekali", "cepat rambat bunyi menjadi nol")),
           ("Istilah gelombang", [("simpul", "titik pada gelombang stasioner yang simpangannya nol"), ("perut", "titik pada gelombang stasioner yang simpangannya terbesar"), ("panjang gelombang", "jarak satu bukit dan satu lembah"),
                                 ("frekuensi", "banyaknya gelombang tiap sekon"), ("amplitudo", "simpangan terbesar"), ("efek Doppler", "perubahan frekuensi karena gerak relatif sumber dan pendengar"),
                                 ("pelayangan", "kuat lemah bunyi bergantian dari dua frekuensi yang berdekatan"), ("desibel", "satuan taraf intensitas bunyi")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Gelombang mekanik memerlukan medium.", "v = λf.", "Gelombang memindahkan energi.",
           "Sumber bunyi yang mendekat terdengar lebih tinggi.", "Difraksi adalah pelenturan gelombang.", "Gelombang stasioner memiliki simpul dan perut.",
           "Sonar memanfaatkan pemantulan bunyi.", "Taraf intensitas bunyi dinyatakan dalam desibel."],
          [("Gelombang bunyi dapat merambat di ruang hampa.", "Bunyi memerlukan medium."), ("Pada simpul simpangannya paling besar.", "Pada simpul simpangannya nol."),
           ("Sumber bunyi menjauh terdengar lebih tinggi.", "Sumber bunyi menjauh terdengar lebih rendah."), ("Interferensi adalah pelenturan gelombang.", "Pelenturan adalah difraksi; interferensi adalah perpaduan."),
           ("Taraf intensitas diukur dalam hertz.", "Taraf intensitas diukur dalam desibel."), ("Bunyi adalah gelombang transversal.", "Bunyi di udara adalah gelombang longitudinal.")],
          "gelombang mekanik dan bunyi", "waves-and-light", calc=f_gelombang),

        H("F", "termodinamika", "Teori Kinetik Gas dan Termodinamika", "Termodinamika",
          "Peserta didik menjelaskan gas ideal, hukum Boyle, Charles, dan Gay-Lussac, hukum I dan II termodinamika, proses-proses termodinamika, mesin kalor, efisiensi Carnot, dan mesin pendingin.",
          "gas ideal pV = nRT, hukum Boyle–Gay-Lussac, energi dalam, usaha gas W = pΔV, hukum I termodinamika ΔU = Q − W, isobarik, isokhorik, isotermal, adiabatik, mesin Carnot",
          "ΔU = Q − W", "Kalor yang diserap gas dipakai untuk menambah energi dalam dan melakukan usaha. Tidak ada mesin kalor yang efisiensinya 100%.",
          ["Gas ideal memenuhi pV = nRT. Hukum Boyle (suhu tetap): pV tetap. Hukum Charles (tekanan tetap): V/T tetap. Hukum Gay-Lussac (volume tetap): p/T tetap. Suhu harus dalam kelvin.",
           "Hukum I termodinamika: ΔU = Q − W. Q positif jika gas menyerap kalor, W positif jika gas melakukan usaha. Pada proses isobarik W = pΔV, isokhorik W = 0, isotermal ΔU = 0, adiabatik Q = 0.",
           "Hukum II termodinamika: kalor mengalir spontan dari benda panas ke dingin, dan tidak ada mesin kalor yang mengubah seluruh kalor menjadi usaha. Efisiensi Carnot η = 1 − T₂/T₁."],
          [("Gas menyerap kalor 1.000 J dan melakukan usaha 400 J. Berapa perubahan energi dalamnya?", ["ΔU = Q − W.", "ΔU = 1.000 − 400 = 600 J."], "600 J")],
          [("Suhu dalam rumus gas ideal boleh memakai °C.", "Suhu harus dalam kelvin."), ("Mesin Carnot dapat berefisiensi 100%.", "Efisiensi Carnot selalu kurang dari 100% karena T₂ tidak mungkin 0 K."),
           ("Pada proses isokhorik gas melakukan usaha besar.", "Volume tetap, jadi usahanya nol.")],
          [("Bagaimana kulkas bekerja?", "Mesin pendingin memindahkan kalor dari dalam kulkas yang dingin ke luar dengan bantuan usaha kompresor."),
           ("Mengapa ban mobil lebih keras setelah perjalanan jauh?", "Suhu udara di dalam ban naik sehingga tekanannya bertambah (hukum Gay-Lussac)."),
           ("Apa itu proses adiabatik?", "Proses tanpa pertukaran kalor dengan lingkungan, misalnya pemampatan cepat udara di dalam pompa.")],
          [("Proses termodinamika", [("tekanan tetap", "isobarik"), ("volume tetap", "isokhorik"), ("suhu tetap", "isotermal"), ("tidak ada pertukaran kalor", "adiabatik"),
                                    ("usaha gas W = 0", "isokhorik"), ("perubahan energi dalam ΔU = 0", "isotermal"), ("W = p × ΔV", "isobarik"), ("Q = 0", "adiabatik")],
            "Proses dengan ‘{k}’ disebut ...", "Apa ciri proses ‘{v}’?", ("isentalpi",)),
           ("Hukum gas", [("p × V tetap pada suhu tetap", "hukum Boyle"), ("V ÷ T tetap pada tekanan tetap", "hukum Charles"), ("p ÷ T tetap pada volume tetap", "hukum Gay-Lussac"), ("pV ÷ T tetap", "hukum Boyle–Gay-Lussac"),
                         ("pV = nRT", "persamaan gas ideal"), ("ban makin keras saat panas", "hukum Gay-Lussac"), ("balon mengecil saat dimasukkan ke lemari es", "hukum Charles"), ("gelembung udara membesar saat naik ke permukaan air", "hukum Boyle")],
            "‘{k}’ sesuai dengan ...", "Manakah yang sesuai dengan ‘{v}’?", ("hukum Hooke",)),
           ("Istilah termodinamika", [("energi dalam", "jumlah energi kinetik seluruh partikel gas"), ("hukum I termodinamika", "kalor = perubahan energi dalam + usaha"), ("hukum II termodinamika", "kalor mengalir spontan dari panas ke dingin"),
                                     ("efisiensi mesin kalor", "perbandingan usaha dengan kalor yang diserap"), ("mesin Carnot", "mesin ideal dengan efisiensi tertinggi"), ("koefisien performansi", "ukuran kinerja mesin pendingin"),
                                     ("entropi", "ukuran ketidakteraturan sistem")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Gas ideal memenuhi pV = nRT.", "Suhu pada rumus gas harus dalam kelvin.", "ΔU = Q − W.",
           "Pada proses isokhorik usaha gas nol.", "Pada proses isotermal energi dalam tetap.", "Pada proses adiabatik tidak ada pertukaran kalor.",
           "Efisiensi Carnot η = 1 − T₂/T₁.", "Tidak ada mesin kalor yang efisiensinya 100%."],
          [("Pada proses isobarik volume tetap.", "Pada isobarik tekanan tetap; isokhorik volume tetap."), ("Kalor mengalir spontan dari benda dingin ke panas.", "Kalor mengalir spontan dari panas ke dingin."),
           ("Efisiensi mesin Carnot dapat mencapai 100%.", "Efisiensi selalu kurang dari 100%."), ("Hukum Boyle berlaku pada tekanan tetap.", "Hukum Boyle berlaku pada suhu tetap."),
           ("Pada proses adiabatik Q sangat besar.", "Pada adiabatik Q = 0."), ("Energi dalam gas ideal tidak bergantung pada suhu.", "Energi dalam gas ideal bergantung pada suhu.")],
          "termodinamika", "energy", calc=f_termo),

        H("K", "ikatan-kimia-dan-bentuk-molekul", "Ikatan Kimia dan Bentuk Molekul", "Ikatan Kimia",
          "Peserta didik menjelaskan kestabilan atom (oktet dan duplet), ikatan ion, kovalen, kovalen koordinasi, dan logam, struktur Lewis, bentuk molekul (VSEPR), kepolaran, dan gaya antarmolekul.",
          "aturan oktet, struktur Lewis, ikatan ion, kovalen tunggal dan rangkap, kovalen koordinasi, ikatan logam, bentuk molekul VSEPR, polar dan nonpolar, ikatan hidrogen, gaya London",
          "Atom berikatan agar konfigurasinya stabil", "Ikatan ion terbentuk dari serah terima elektron, ikatan kovalen dari pemakaian bersama pasangan elektron.",
          ["Atom cenderung mencapai konfigurasi gas mulia: 8 elektron valensi (oktet) atau 2 (duplet). Logam cenderung melepas elektron, nonlogam cenderung menerima elektron.",
           "Ikatan ion terjadi antara logam dan nonlogam melalui serah terima elektron (NaCl). Ikatan kovalen terjadi antara nonlogam dengan pemakaian bersama elektron (H₂O, CH₄). Ikatan kovalen koordinasi: pasangan elektron hanya dari satu atom (NH₄⁺).",
           "Bentuk molekul ditentukan tolakan pasangan elektron (VSEPR): CH₄ tetrahedral, NH₃ piramida trigonal, H₂O bentuk V, CO₂ linear, BF₃ segitiga datar. Molekul polar memiliki momen dipol, misalnya H₂O."],
          [("Apa jenis ikatan dalam MgO?", ["Mg adalah logam golongan IIA dan melepas 2 elektron.", "O adalah nonlogam dan menerima 2 elektron."], "ikatan ion")],
          [("Semua senyawa kovalen polar.", "CH₄ dan CO₂ adalah molekul kovalen nonpolar."), ("Ikatan ion terjadi antara dua atom nonlogam.", "Ikatan ion terjadi antara logam dan nonlogam."),
           ("Molekul air berbentuk linear.", "Air berbentuk V (bengkok) karena ada dua pasangan elektron bebas.")],
          [("Mengapa titik didih air tinggi?", "Molekul air saling berikatan hidrogen yang kuat, sehingga perlu banyak energi untuk memisahkannya."),
           ("Apa itu pasangan elektron bebas?", "Pasangan elektron valensi yang tidak dipakai untuk berikatan dan memengaruhi bentuk molekul."),
           ("Mengapa logam menghantarkan listrik?", "Elektron valensi logam bergerak bebas seperti lautan elektron di antara ion-ion positif.")],
          [("Jenis ikatan", [("NaCl", "ikatan ion"), ("MgO", "ikatan ion"), ("KBr", "ikatan ion"), ("CaCl₂", "ikatan ion"), ("H₂O", "ikatan kovalen"), ("CH₄", "ikatan kovalen"), ("CO₂", "ikatan kovalen"),
                            ("NH₃", "ikatan kovalen"), ("Cl₂", "ikatan kovalen"), ("NH₄⁺", "ikatan kovalen koordinasi"), ("H₃O⁺", "ikatan kovalen koordinasi"), ("besi (Fe)", "ikatan logam"), ("tembaga (Cu)", "ikatan logam")],
            "Ikatan dalam ‘{k}’ adalah ...", "Manakah zat dengan ‘{v}’?", ("ikatan hidrogen",)),
           ("Bentuk molekul", [("CH₄", "tetrahedral"), ("CCl₄", "tetrahedral"), ("NH₃", "piramida trigonal"), ("PCl₃", "piramida trigonal"), ("H₂O", "bentuk V (bengkok)"), ("H₂S", "bentuk V (bengkok)"),
                              ("CO₂", "linear"), ("BeCl₂", "linear"), ("BF₃", "segitiga datar (trigonal planar)"), ("PCl₅", "bipiramida trigonal"), ("SF₆", "oktahedral")],
            "Bagaimana bentuk molekul ‘{k}’?", "Molekul manakah yang berbentuk ‘{v}’?"),
           ("Gaya antarmolekul dan kepolaran", [("H₂O", "polar dengan ikatan hidrogen"), ("HF", "polar dengan ikatan hidrogen"), ("NH₃", "polar dengan ikatan hidrogen"), ("HCl", "polar dengan gaya dipol-dipol"),
                                               ("CH₄", "nonpolar dengan gaya London"), ("CO₂", "nonpolar dengan gaya London"), ("N₂", "nonpolar dengan gaya London"), ("CCl₄", "nonpolar dengan gaya London")],
            "Bagaimana sifat molekul ‘{k}’?", "Molekul manakah yang ‘{v}’?")],
          ["Atom berikatan untuk mencapai konfigurasi stabil.", "Ikatan ion terbentuk melalui serah terima elektron.", "Ikatan kovalen terbentuk dari pemakaian bersama elektron.",
           "NaCl memiliki ikatan ion.", "CH₄ berbentuk tetrahedral.", "H₂O berbentuk V.",
           "Air memiliki ikatan hidrogen antarmolekul.", "Logam menghantarkan listrik karena elektronnya bebas bergerak."],
          [("CO₂ berbentuk bengkok.", "CO₂ berbentuk linear."), ("NH₃ berbentuk segitiga datar.", "NH₃ berbentuk piramida trigonal karena satu pasangan elektron bebas."),
           ("CH₄ adalah molekul polar.", "CH₄ simetris sehingga nonpolar."), ("Ikatan kovalen terjadi antara logam dan nonlogam.", "Ikatan kovalen terjadi antara nonlogam."),
           ("Ikatan hidrogen lebih lemah daripada gaya London.", "Ikatan hidrogen jauh lebih kuat daripada gaya London."), ("NH₄⁺ hanya memiliki ikatan ion.", "NH₄⁺ memiliki ikatan kovalen dan kovalen koordinasi.")],
          "ikatan kimia", "matter"),

        H("K", "stoikiometri", "Konsep Mol dan Stoikiometri", "Stoikiometri",
          "Peserta didik menerapkan konsep mol, massa atom relatif dan massa molekul relatif, bilangan Avogadro, volume molar gas, rumus empiris dan molekul, serta perhitungan kimia dalam reaksi.",
          "Ar dan Mr, mol, bilangan Avogadro, volume molar STP, kemolaran, rumus empiris dan molekul, pereaksi pembatas, kadar zat",
          "n = m ÷ Mr", "Mol menghubungkan massa, jumlah partikel, dan volume gas. 1 mol = 6,02 × 10²³ partikel = 22,4 L gas pada STP.",
          ["Satu mol zat mengandung 6,02 × 10²³ partikel (bilangan Avogadro, L). Massa satu mol zat sama dengan Mr dalam gram, sehingga n = m ÷ Mr.",
           "Pada keadaan standar (STP: 0 °C, 1 atm), volume satu mol gas apa pun adalah 22,4 L. Kemolaran larutan M = n ÷ V (mol/L).",
           "Dalam reaksi, perbandingan koefisien sama dengan perbandingan mol. Pereaksi yang habis lebih dahulu disebut pereaksi pembatas dan menentukan jumlah hasil reaksi."],
          [("Berapa massa 0,5 mol CO₂? (Mr CO₂ = 44)", ["m = n × Mr.", "m = 0,5 × 44 = 22 g."], "22 g")],
          [("Volume 1 mol semua zat pada STP adalah 22,4 L.", "Volume molar 22,4 L hanya berlaku untuk gas."), ("Mr H₂O adalah 17.", "Mr H₂O = 2(1) + 16 = 18."),
           ("Perbandingan koefisien sama dengan perbandingan massa.", "Perbandingan koefisien sama dengan perbandingan mol.")],
          [("Apa itu rumus empiris?", "Rumus perbandingan paling sederhana jumlah atom dalam senyawa; rumus empiris glukosa C₆H₁₂O₆ adalah CH₂O."),
           ("Apa itu pereaksi pembatas?", "Pereaksi yang habis lebih dahulu sehingga membatasi jumlah produk yang terbentuk."),
           ("Bagaimana membuat larutan NaOH 0,1 M sebanyak 1 L?", "Larutkan 0,1 mol NaOH, yaitu 4 g, dalam air hingga volumenya 1 L.")],
          [("Mr senyawa", [("H₂O", "18"), ("CO₂", "44"), ("CH₄", "16"), ("NH₃", "17"), ("NaCl", "58,5"), ("CaCO₃", "100"), ("H₂SO₄", "98"), ("NaOH", "40"), ("C₆H₁₂O₆", "180"), ("O₂", "32")],
            "Berapa Mr ‘{k}’? (Ar H = 1, C = 12, N = 14, O = 16, Na = 23, S = 32, Cl = 35,5, Ca = 40)", "Senyawa manakah yang Mr-nya ‘{v}’? (Ar H = 1, C = 12, N = 14, O = 16, Na = 23, S = 32, Cl = 35,5, Ca = 40)"),
           ("Rumus empiris", [("C₆H₁₂O₆", "CH₂O"), ("C₂H₄", "CH₂"), ("C₂H₆", "CH₃"), ("H₂O₂", "HO"), ("C₆H₆", "CH"), ("N₂O₄", "NO₂"), ("C₄H₁₀", "C₂H₅"), ("P₄O₁₀", "P₂O₅")],
            "Apa rumus empiris ‘{k}’?", "Senyawa manakah yang rumus empirisnya ‘{v}’?"),
           ("Istilah stoikiometri", [("mol", "jumlah zat yang mengandung 6,02 × 10²³ partikel"), ("bilangan Avogadro", "6,02 × 10²³ partikel per mol"), ("massa molar", "massa satu mol zat dalam gram"),
                                    ("volume molar STP", "22,4 L per mol gas"), ("kemolaran", "jumlah mol zat terlarut dalam satu liter larutan"), ("rumus empiris", "perbandingan paling sederhana jumlah atom"),
                                    ("rumus molekul", "jumlah atom sebenarnya dalam satu molekul"), ("pereaksi pembatas", "pereaksi yang habis lebih dahulu")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Satu mol mengandung 6,02 × 10²³ partikel.", "n = m ÷ Mr.", "Volume satu mol gas pada STP adalah 22,4 L.",
           "Perbandingan koefisien reaksi sama dengan perbandingan mol.", "Mr H₂O adalah 18.", "Rumus empiris glukosa adalah CH₂O.",
           "Pereaksi pembatas habis lebih dahulu.", "Kemolaran = mol ÷ volume larutan dalam liter."],
          [("Volume satu mol air cair pada STP adalah 22,4 L.", "22,4 L hanya untuk gas."), ("Mr CO₂ adalah 28.", "Mr CO₂ = 12 + 2(16) = 44."), ("Rumus empiris C₂H₄ adalah C₂H₄.", "Rumus empiris C₂H₄ adalah CH₂."),
           ("n = Mr ÷ m.", "n = m ÷ Mr."), ("Pereaksi pembatas adalah pereaksi yang tersisa.", "Pereaksi pembatas habis lebih dahulu."), ("Bilangan Avogadro adalah 6,02 × 10²².", "Bilangan Avogadro adalah 6,02 × 10²³.")],
          "stoikiometri", "matter", calc=f_mol),

        H("K", "termokimia", "Termokimia", "Termokimia",
          "Peserta didik menjelaskan sistem dan lingkungan, reaksi eksoterm dan endoterm, perubahan entalpi standar, kalorimetri, hukum Hess, dan energi ikatan.",
          "sistem dan lingkungan, eksoterm dan endoterm, ΔH, entalpi pembentukan, penguraian, pembakaran standar, kalorimeter, q = mcΔT, hukum Hess, energi ikatan",
          "Eksoterm ΔH negatif, endoterm ΔH positif", "Kalor reaksi dapat diukur dengan kalorimeter atau dihitung dengan hukum Hess.",
          ["Sistem adalah bagian yang diamati (zat yang bereaksi), lingkungan adalah segala sesuatu di luar sistem. Reaksi eksoterm melepas kalor ke lingkungan (ΔH < 0), endoterm menyerap kalor (ΔH > 0).",
           "Kalor reaksi dapat diukur dengan kalorimeter: q = m × c × ΔT. Entalpi standar diukur pada 25 °C dan 1 atm, misalnya entalpi pembentukan standar (ΔHf°) dan pembakaran standar (ΔHc°).",
           "Hukum Hess: ΔH reaksi hanya bergantung pada keadaan awal dan akhir, tidak pada jalannya reaksi, sehingga ΔH dapat dijumlahkan. ΔH juga dapat dihitung dari energi ikatan: ΣE ikatan putus − ΣE ikatan terbentuk."],
          [("Saat NaOH dilarutkan, gelas terasa panas. Apakah reaksi ini eksoterm atau endoterm?", ["Gelas (lingkungan) menjadi panas.", "Kalor berpindah dari sistem ke lingkungan."], "eksoterm, ΔH negatif")],
          [("Pada reaksi eksoterm ΔH bernilai positif.", "Reaksi eksoterm memiliki ΔH negatif."), ("Gelas yang terasa dingin berarti reaksi melepas kalor.", "Gelas dingin berarti sistem menyerap kalor dari lingkungan (endoterm)."),
           ("ΔH bergantung pada jalannya reaksi.", "Menurut hukum Hess, ΔH hanya bergantung pada keadaan awal dan akhir.")],
          [("Apa itu entalpi pembentukan standar?", "Perubahan entalpi saat 1 mol senyawa terbentuk dari unsur-unsurnya pada keadaan standar."),
           ("Apa contoh reaksi endoterm sehari-hari?", "Kompres dingin instan, fotosintesis, dan pelarutan amonium nitrat dalam air."),
           ("Mengapa nilai energi ikatan berguna?", "Untuk memperkirakan ΔH reaksi tanpa percobaan, dari ikatan yang diputus dan dibentuk.")],
          [("Eksoterm atau endoterm", [("pembakaran bensin", "eksoterm"), ("pelarutan NaOH dalam air", "eksoterm"), ("respirasi sel", "eksoterm"), ("reaksi penetralan asam basa", "eksoterm"), ("pengembunan uap air", "eksoterm"),
                                      ("fotosintesis", "endoterm"), ("pelarutan amonium nitrat dalam air", "endoterm"), ("penguraian CaCO₃ dengan pemanasan", "endoterm"), ("es mencair", "endoterm"), ("elektrolisis air", "endoterm")],
            "Proses ‘{k}’ termasuk ...", "Manakah contoh proses ‘{v}’?", ("isoterm", "netral")),
           ("Jenis entalpi standar", [("C(s) + O₂(g) → CO₂(g)", "entalpi pembentukan standar CO₂"), ("H₂(g) + ½O₂(g) → H₂O(l)", "entalpi pembentukan standar H₂O"), ("CH₄ + 2O₂ → CO₂ + 2H₂O", "entalpi pembakaran standar CH₄"),
                                     ("C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O", "entalpi pembakaran standar etanol"), ("H₂O(l) → H₂(g) + ½O₂(g)", "entalpi penguraian standar H₂O"), ("NaCl(s) → Na(s) + ½Cl₂(g)", "entalpi penguraian standar NaCl"),
                                     ("HCl + NaOH → NaCl + H₂O", "entalpi penetralan")],
            "Persamaan ‘{k}’ menyatakan ...", None, ("entalpi pelarutan standar",)),
           ("Istilah termokimia", [("sistem", "bagian alam semesta yang diamati"), ("lingkungan", "segala sesuatu di luar sistem"), ("entalpi", "jumlah energi yang dimiliki sistem pada tekanan tetap"),
                                  ("reaksi eksoterm", "reaksi yang melepas kalor ke lingkungan"), ("reaksi endoterm", "reaksi yang menyerap kalor dari lingkungan"), ("kalorimeter", "alat untuk mengukur kalor reaksi"),
                                  ("hukum Hess", "ΔH hanya bergantung pada keadaan awal dan akhir"), ("energi ikatan", "energi untuk memutuskan 1 mol ikatan dalam wujud gas")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Reaksi eksoterm melepas kalor ke lingkungan.", "Reaksi endoterm memiliki ΔH positif.", "Pembakaran adalah reaksi eksoterm.",
           "Kalorimeter dipakai untuk mengukur kalor reaksi.", "q = m × c × ΔT.", "Hukum Hess memungkinkan ΔH dijumlahkan.",
           "Entalpi standar diukur pada 25 °C dan 1 atm.", "Fotosintesis adalah reaksi endoterm."],
          [("Es mencair adalah proses eksoterm.", "Es mencair menyerap kalor, jadi endoterm."), ("Reaksi endoterm membuat lingkungan menjadi panas.", "Reaksi endoterm membuat lingkungan dingin."),
           ("Kalorimeter mengukur massa zat.", "Kalorimeter mengukur kalor reaksi."), ("Energi ikatan adalah energi yang dilepas saat ikatan putus.", "Memutus ikatan memerlukan energi."),
           ("Entalpi standar diukur pada 0 °C.", "Entalpi standar diukur pada 25 °C dan 1 atm."), ("Penetralan asam basa adalah reaksi endoterm.", "Penetralan melepas kalor, jadi eksoterm.")],
          "termokimia", "matter", calc=f_termokimia),

        H("K", "laju-reaksi-dan-kesetimbangan", "Laju Reaksi dan Kesetimbangan Kimia", "Laju dan Kesetimbangan",
          "Peserta didik menjelaskan laju reaksi, persamaan laju dan orde reaksi, teori tumbukan, faktor yang memengaruhi laju, kesetimbangan dinamis, tetapan kesetimbangan, dan asas Le Chatelier.",
          "laju reaksi, orde reaksi, persamaan laju v = k[A]^m[B]^n, energi aktivasi, katalis, kesetimbangan dinamis, Kc, asas Le Chatelier, proses Haber",
          "Sistem setimbang bergeser untuk mengurangi gangguan", "Laju reaksi bergantung pada konsentrasi sesuai ordenya. Kesetimbangan bergeser jika konsentrasi, suhu, atau tekanan diubah.",
          ["Laju reaksi dinyatakan v = k[A]ᵐ[B]ⁿ, dengan m dan n orde reaksi yang ditentukan dari percobaan. Orde nol: laju tetap; orde satu: laju sebanding konsentrasi; orde dua: laju sebanding kuadrat konsentrasi.",
           "Kesetimbangan dinamis terjadi pada reaksi bolak-balik saat laju reaksi maju sama dengan laju reaksi balik. Untuk aA + bB ⇌ cC + dD, Kc = [C]ᶜ[D]ᵈ ÷ ([A]ᵃ[B]ᵇ); zat padat dan cair murni tidak dimasukkan.",
           "Asas Le Chatelier: jika sistem setimbang diganggu, sistem bergeser untuk mengurangi gangguan. Menambah pereaksi menggeser ke kanan, menaikkan suhu menggeser ke arah endoterm, menaikkan tekanan menggeser ke arah jumlah mol gas lebih kecil."],
          [("Pada N₂(g) + 3H₂(g) ⇌ 2NH₃(g), ΔH = −92 kJ, ke arah mana kesetimbangan bergeser jika tekanan dinaikkan?", ["Mol gas kiri = 4, kanan = 2.", "Tekanan naik menggeser ke arah mol gas lebih kecil."], "ke kanan (ke arah NH₃)")],
          [("Pada kesetimbangan reaksi berhenti.", "Reaksi tetap berlangsung; laju maju dan balik sama (dinamis)."), ("Katalis menggeser kesetimbangan ke kanan.", "Katalis hanya mempercepat tercapainya kesetimbangan."),
           ("Orde reaksi selalu sama dengan koefisien reaksi.", "Orde reaksi ditentukan dari percobaan.")],
          [("Apa itu proses Haber-Bosch?", "Pembuatan amonia dari N₂ dan H₂ pada suhu sekitar 400–450 °C, tekanan tinggi, dan katalis besi."),
           ("Mengapa suhu tinggi menurunkan hasil amonia?", "Reaksi pembentukan amonia eksoterm, sehingga suhu tinggi menggeser kesetimbangan ke kiri; suhu dipilih sedang agar laju tetap cukup."),
           ("Apa itu waktu paruh?", "Waktu yang diperlukan agar konsentrasi pereaksi tinggal setengahnya.")],
          [("Pergeseran kesetimbangan", [("konsentrasi pereaksi ditambah", "bergeser ke kanan (ke arah hasil reaksi)"), ("konsentrasi hasil reaksi ditambah", "bergeser ke kiri (ke arah pereaksi)"), ("hasil reaksi diambil terus-menerus", "bergeser ke kanan (ke arah hasil reaksi)"),
                                        ("suhu dinaikkan pada reaksi eksoterm", "bergeser ke kiri (ke arah pereaksi)"), ("suhu diturunkan pada reaksi eksoterm", "bergeser ke kanan (ke arah hasil reaksi)"),
                                        ("tekanan dinaikkan pada N₂ + 3H₂ ⇌ 2NH₃", "bergeser ke kanan (ke arah hasil reaksi)"), ("tekanan diturunkan pada N₂ + 3H₂ ⇌ 2NH₃", "bergeser ke kiri (ke arah pereaksi)"),
                                        ("katalis ditambahkan", "tidak bergeser"), ("tekanan dinaikkan pada H₂ + I₂ ⇌ 2HI", "tidak bergeser")],
            "Ke arah mana kesetimbangan bergeser jika ‘{k}’?", None, ("bergeser ke atas",)),
           ("Rumus Kc", [("N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", "Kc = [NH₃]² ÷ ([N₂][H₂]³)"), ("H₂(g) + I₂(g) ⇌ 2HI(g)", "Kc = [HI]² ÷ ([H₂][I₂])"), ("2SO₂(g) + O₂(g) ⇌ 2SO₃(g)", "Kc = [SO₃]² ÷ ([SO₂]²[O₂])"),
                        ("CaCO₃(s) ⇌ CaO(s) + CO₂(g)", "Kc = [CO₂]"), ("N₂O₄(g) ⇌ 2NO₂(g)", "Kc = [NO₂]² ÷ [N₂O₄]"), ("PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)", "Kc = [PCl₃][Cl₂] ÷ [PCl₅]")],
            "Bagaimana rumus Kc untuk ‘{k}’?", "Reaksi manakah yang memiliki rumus ‘{v}’?"),
           ("Istilah laju dan kesetimbangan", [("orde reaksi", "pangkat konsentrasi dalam persamaan laju"), ("tetapan laju (k)", "konstanta dalam persamaan laju"), ("energi aktivasi", "energi minimum agar tumbukan menghasilkan reaksi"),
                                              ("kesetimbangan dinamis", "laju reaksi maju sama dengan laju reaksi balik"), ("kesetimbangan homogen", "semua zat dalam kesetimbangan berwujud sama"),
                                              ("kesetimbangan heterogen", "zat dalam kesetimbangan berwujud berbeda"), ("asas Le Chatelier", "sistem setimbang bergeser untuk mengurangi gangguan"), ("katalis", "zat yang menurunkan energi aktivasi")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Orde reaksi ditentukan dari percobaan.", "Pada orde dua laju sebanding kuadrat konsentrasi.", "Pada kesetimbangan dinamis laju maju sama dengan laju balik.",
           "Katalis tidak menggeser kesetimbangan.", "Menambah pereaksi menggeser kesetimbangan ke kanan.", "Menaikkan suhu menggeser kesetimbangan ke arah endoterm.",
           "Zat padat murni tidak dimasukkan ke rumus Kc.", "Menaikkan tekanan menggeser ke arah jumlah mol gas yang lebih kecil."],
          [("Pada kesetimbangan semua reaksi berhenti.", "Kesetimbangan bersifat dinamis; reaksi tetap berlangsung."), ("Katalis menambah hasil kesetimbangan.", "Katalis hanya mempercepat tercapainya kesetimbangan."),
           ("Zat padat dimasukkan ke rumus Kc.", "Zat padat dan cair murni tidak dimasukkan."), ("Menaikkan suhu menggeser ke arah eksoterm.", "Menaikkan suhu menggeser ke arah endoterm."),
           ("Pada orde nol laju naik jika konsentrasi naik.", "Pada orde nol laju tidak bergantung konsentrasi."), ("Menaikkan tekanan menggeser ke arah mol gas lebih besar.", "Menaikkan tekanan menggeser ke arah mol gas lebih kecil.")],
          "laju reaksi dan kesetimbangan", "matter", calc=f_orde),

        H("K", "hidrokarbon-dan-minyak-bumi", "Hidrokarbon dan Minyak Bumi", "Hidrokarbon",
          "Peserta didik menjelaskan kekhasan atom karbon, penggolongan hidrokarbon (alkana, alkena, alkuna), tata nama IUPAC, isomer, reaksi hidrokarbon, serta pembentukan, pengolahan, dan dampak pembakaran minyak bumi.",
          "atom C primer, sekunder, tersier, kuarterner, alkana CₙH₂ₙ₊₂, alkena CₙH₂ₙ, alkuna CₙH₂ₙ₋₂, tata nama IUPAC, isomer, distilasi bertingkat, bilangan oktan",
          "Alkana tunggal, alkena rangkap dua, alkuna rangkap tiga", "Minyak bumi dipisahkan dengan distilasi bertingkat berdasarkan perbedaan titik didih.",
          ["Atom karbon memiliki 4 elektron valensi sehingga dapat membentuk 4 ikatan kovalen dan rantai panjang. Atom C primer terikat pada 1 atom C lain, sekunder 2, tersier 3, dan kuarterner 4.",
           "Alkana (CₙH₂ₙ₊₂) berikatan tunggal: metana, etana, propana, butana. Alkena (CₙH₂ₙ) memiliki ikatan rangkap dua: etena, propena. Alkuna (CₙH₂ₙ₋₂) memiliki ikatan rangkap tiga: etuna (asetilena).",
           "Minyak bumi terbentuk dari sisa organisme laut selama jutaan tahun. Minyak mentah dipisahkan dengan distilasi bertingkat menjadi LPG, bensin, kerosin, solar, oli, dan aspal. Mutu bensin dinyatakan dengan bilangan oktan."],
          [("Apa rumus molekul alkana dengan 5 atom karbon?", ["Rumus alkana CₙH₂ₙ₊₂.", "n = 5: H = 2(5) + 2 = 12."], "C₅H₁₂ (pentana)")],
          [("Alkena memiliki ikatan rangkap tiga.", "Alkena memiliki ikatan rangkap dua; alkuna rangkap tiga."), ("Bensin dipisahkan dari minyak mentah dengan penyaringan.", "Minyak mentah dipisahkan dengan distilasi bertingkat."),
           ("Bilangan oktan tinggi berarti bensin mudah mengetuk.", "Bilangan oktan tinggi berarti bensin tahan ketukan (knocking).")],
          [("Apa itu isomer?", "Senyawa dengan rumus molekul sama tetapi struktur berbeda, misalnya n-butana dan 2-metilpropana (C₄H₁₀)."),
           ("Mengapa pembakaran tidak sempurna berbahaya?", "Menghasilkan karbon monoksida (CO) yang mengikat hemoglobin dan menghalangi pengangkutan oksigen."),
           ("Apa itu cracking?", "Pemecahan rantai hidrokarbon panjang menjadi rantai pendek untuk menambah produksi bensin.")],
          [("Rumus hidrokarbon", [("metana", "CH₄"), ("etana", "C₂H₆"), ("propana", "C₃H₈"), ("butana", "C₄H₁₀"), ("pentana", "C₅H₁₂"), ("heksana", "C₆H₁₄"), ("oktana", "C₈H₁₈"),
                                  ("etena", "C₂H₄"), ("propena", "C₃H₆"), ("butena", "C₄H₈"), ("etuna", "C₂H₂"), ("propuna", "C₃H₄")],
            "Apa rumus molekul ‘{k}’?", "Apa nama senyawa ‘{v}’?"),
           ("Golongan hidrokarbon", [("CH₄", "alkana"), ("C₃H₈", "alkana"), ("C₆H₁₄", "alkana"), ("C₁₀H₂₂", "alkana"), ("C₂H₄", "alkena"), ("C₃H₆", "alkena"), ("C₅H₁₀", "alkena"),
                                    ("C₂H₂", "alkuna"), ("C₃H₄", "alkuna"), ("C₄H₆", "alkuna")],
            "‘{k}’ termasuk golongan ...", "Manakah yang termasuk ‘{v}’?", ("alkohol", "aromatik")),
           ("Fraksi minyak bumi", [("LPG", "bahan bakar kompor gas rumah tangga"), ("bensin", "bahan bakar mobil dan motor"), ("avtur", "bahan bakar pesawat jet"), ("kerosin", "minyak tanah untuk kompor dan lampu"),
                                  ("solar", "bahan bakar mesin diesel"), ("oli", "pelumas mesin"), ("aspal", "pelapis jalan"), ("lilin parafin", "bahan lilin dan semir")],
            "Apa kegunaan fraksi ‘{k}’?", "Fraksi minyak bumi manakah yang dipakai sebagai ‘{v}’?")],
          ["Atom karbon dapat membentuk empat ikatan kovalen.", "Alkana hanya memiliki ikatan tunggal.", "Rumus umum alkena adalah CₙH₂ₙ.",
           "Etuna memiliki ikatan rangkap tiga.", "Minyak bumi dipisahkan dengan distilasi bertingkat.", "Bilangan oktan menunjukkan mutu bensin.",
           "Pembakaran tidak sempurna menghasilkan karbon monoksida.", "Isomer memiliki rumus molekul sama tetapi struktur berbeda."],
          [("Metana termasuk alkena.", "Metana (CH₄) termasuk alkana."), ("Rumus umum alkuna adalah CₙH₂ₙ₊₂.", "Rumus umum alkuna adalah CₙH₂ₙ₋₂."),
           ("Solar dipakai sebagai bahan bakar pesawat jet.", "Pesawat jet memakai avtur."), ("Atom C tersier terikat pada satu atom C lain.", "Atom C tersier terikat pada tiga atom C lain."),
           ("Karbon monoksida aman dihirup.", "CO beracun karena mengikat hemoglobin."), ("Minyak bumi terbentuk dalam beberapa tahun.", "Minyak bumi terbentuk selama jutaan tahun.")],
          "hidrokarbon", "matter"),

        H("B", "sel-dan-organel", "Sel sebagai Unit Kehidupan", "Sel",
          "Peserta didik menjelaskan teori sel, perbedaan sel prokariotik dan eukariotik, sel hewan dan tumbuhan, struktur dan fungsi organel sel, serta komponen kimia penyusun sel.",
          "teori sel, prokariotik dan eukariotik, membran sel, nukleus, mitokondria, ribosom, retikulum endoplasma, badan Golgi, lisosom, kloroplas, vakuola, dinding sel",
          "Sel adalah unit struktural dan fungsional kehidupan", "Setiap organel memiliki tugas khusus, misalnya mitokondria menghasilkan energi dan ribosom membuat protein.",
          ["Teori sel: semua makhluk hidup tersusun atas sel, sel adalah unit struktural dan fungsional, dan setiap sel berasal dari sel sebelumnya (Rudolf Virchow).",
           "Sel prokariotik (bakteri) tidak memiliki membran inti dan organel bermembran. Sel eukariotik (hewan, tumbuhan, jamur) memiliki inti dan organel bermembran.",
           "Sel tumbuhan memiliki dinding sel, kloroplas, dan vakuola besar yang tidak dimiliki sel hewan. Sel hewan memiliki sentriol dan lisosom yang lebih banyak."],
          [("Organel apa yang banyak ditemukan pada sel otot yang aktif?", ["Sel otot memerlukan banyak energi.", "Energi (ATP) dihasilkan oleh mitokondria."], "mitokondria")],
          [("Semua sel memiliki inti sel.", "Sel prokariotik tidak memiliki membran inti."), ("Sel hewan memiliki dinding sel.", "Dinding sel dimiliki sel tumbuhan, jamur, dan bakteri."),
           ("Ribosom menghasilkan energi.", "Ribosom membuat protein; energi dihasilkan mitokondria.")],
          [("Mengapa mitokondria disebut pembangkit tenaga sel?", "Karena di mitokondria terjadi respirasi seluler yang menghasilkan ATP."),
           ("Apa fungsi badan Golgi?", "Mengemas, memodifikasi, dan mengirim protein dan lemak ke tempat tujuan, termasuk membentuk lisosom."),
           ("Siapa yang pertama melihat sel?", "Robert Hooke pada tahun 1665 melihat sel-sel gabus dengan mikroskop sederhana.")],
          [("Organel dan fungsinya", [("nukleus", "mengendalikan seluruh kegiatan sel dan menyimpan DNA"), ("mitokondria", "tempat respirasi seluler yang menghasilkan ATP"), ("ribosom", "tempat sintesis protein"),
                                     ("retikulum endoplasma kasar", "mengangkut protein hasil ribosom"), ("retikulum endoplasma halus", "membuat lemak dan menetralkan racun"), ("badan Golgi", "mengemas dan mengirim zat ke luar sel"),
                                     ("lisosom", "mencerna zat dan organel rusak dengan enzim"), ("kloroplas", "tempat fotosintesis"), ("vakuola", "menyimpan air, cadangan makanan, dan zat sisa"),
                                     ("membran sel", "mengatur keluar masuknya zat"), ("dinding sel", "melindungi dan memberi bentuk tetap pada sel tumbuhan"), ("sentriol", "membentuk benang spindel saat pembelahan sel hewan")],
            "Apa fungsi ‘{k}’?", "Organel apa yang berfungsi ‘{v}’?"),
           ("Sel hewan atau tumbuhan", {"hanya terdapat pada sel tumbuhan": ["dinding sel", "kloroplas", "vakuola sentral yang besar", "plasmodesmata", "plastida penyimpan pati", "amiloplas", "kromoplas pemberi warna buah"],
                                       "terutama terdapat pada sel hewan": ["sentriol", "lisosom yang banyak", "vakuola kecil atau tidak ada", "bentuk sel tidak tetap", "glikogen sebagai cadangan makanan", "silia dan flagela pada beberapa sel", "tidak memiliki plastida"]}),
           ("Prokariotik atau eukariotik", [("bakteri Escherichia coli", "prokariotik"), ("bakteri Lactobacillus", "prokariotik"), ("sianobakteri", "prokariotik"), ("sel kulit manusia", "eukariotik"),
                                           ("sel daun mangga", "eukariotik"), ("sel ragi", "eukariotik"), ("Amoeba", "eukariotik"), ("sel darah putih", "eukariotik")],
            "Sel ‘{k}’ termasuk sel ...", "Manakah contoh sel ‘{v}’?", ("aseluler", "mesokariotik"))],
          ["Semua makhluk hidup tersusun atas sel.", "Sel prokariotik tidak memiliki membran inti.", "Mitokondria menghasilkan ATP.",
           "Ribosom adalah tempat sintesis protein.", "Kloroplas adalah tempat fotosintesis.", "Sel tumbuhan memiliki dinding sel.",
           "Lisosom mengandung enzim pencerna.", "Membran sel mengatur keluar masuknya zat."],
          [("Kloroplas terdapat pada sel hewan.", "Kloroplas terdapat pada sel tumbuhan."), ("Bakteri adalah sel eukariotik.", "Bakteri adalah sel prokariotik."),
           ("Badan Golgi tempat fotosintesis.", "Badan Golgi mengemas dan mengirim zat."), ("Sentriol hanya terdapat pada sel tumbuhan.", "Sentriol terutama terdapat pada sel hewan."),
           ("Dinding sel mengatur keluar masuknya zat.", "Membran sel yang mengatur keluar masuk zat; dinding sel melindungi dan memberi bentuk."), ("Nukleus tempat respirasi sel.", "Respirasi sel terjadi di mitokondria.")],
          "sel", "living-things-and-ecosystems"),

        H("B", "transpor-membran", "Transpor Membran", "Transpor Membran",
          "Peserta didik menjelaskan struktur membran sel (model mosaik fluida) dan mekanisme transpor zat: difusi, osmosis, difusi terfasilitasi, transpor aktif, endositosis, dan eksositosis.",
          "model mosaik fluida, fosfolipid, protein membran, difusi, osmosis, larutan hipotonik, isotonik, hipertonik, transpor aktif, pompa natrium-kalium, endositosis, eksositosis",
          "Transpor pasif tanpa energi, transpor aktif memerlukan ATP", "Pada osmosis air bergerak dari larutan encer ke larutan pekat melewati membran semipermeabel.",
          ["Membran sel tersusun atas lapisan ganda fosfolipid dengan protein yang tersebar (model mosaik fluida). Membran bersifat selektif permeabel.",
           "Transpor pasif tidak memerlukan energi dan zat bergerak mengikuti gradien konsentrasi: difusi, difusi terfasilitasi (melalui protein), dan osmosis (perpindahan air melalui membran semipermeabel).",
           "Transpor aktif memerlukan ATP untuk memindahkan zat melawan gradien konsentrasi, misalnya pompa natrium-kalium. Zat besar masuk dengan endositosis (fagositosis, pinositosis) dan keluar dengan eksositosis."],
          [("Sel darah merah dimasukkan ke air murni dan akhirnya pecah. Mengapa?", ["Air murni hipotonik dibanding isi sel.", "Air masuk ke sel melalui osmosis sampai sel pecah (lisis)."], "air masuk ke sel karena osmosis")],
          [("Osmosis adalah perpindahan zat terlarut.", "Osmosis adalah perpindahan air melalui membran semipermeabel."), ("Difusi memerlukan ATP.", "Difusi adalah transpor pasif tanpa energi."),
           ("Sel tumbuhan pecah di air murni seperti sel darah merah.", "Dinding sel menahan sel tumbuhan sehingga sel hanya menjadi tegang (turgid).")],
          [("Apa itu plasmolisis?", "Lepasnya membran sel dari dinding sel tumbuhan karena sel kehilangan air dalam larutan hipertonik."),
           ("Mengapa sayur layu bisa segar lagi jika direndam air?", "Air masuk ke sel-sel sayur melalui osmosis sehingga sel kembali tegang."),
           ("Apa contoh fagositosis?", "Sel darah putih menelan bakteri dengan cara menjulurkan membran selnya.")],
          [("Jenis transpor", [("pergerakan oksigen dari alveolus ke darah", "difusi"), ("bau parfum menyebar di ruangan", "difusi"), ("air masuk ke akar tumbuhan", "osmosis"), ("sayur layu segar kembali setelah direndam air", "osmosis"),
                              ("glukosa masuk ke sel melalui protein pembawa", "difusi terfasilitasi"), ("pompa natrium-kalium pada sel saraf", "transpor aktif"), ("penyerapan mineral oleh akar dari tanah yang miskin mineral", "transpor aktif"),
                              ("sel darah putih menelan bakteri", "fagositosis (endositosis)"), ("sel menelan cairan dalam gelembung kecil", "pinositosis (endositosis)"), ("pelepasan hormon dari sel kelenjar", "eksositosis")],
            "‘{k}’ adalah contoh ...", "Manakah contoh ‘{v}’?"),
           ("Larutan dan sel", [("sel darah merah dalam larutan hipotonik", "sel menggembung dan dapat pecah"), ("sel darah merah dalam larutan hipertonik", "sel mengerut (krenasi)"), ("sel darah merah dalam larutan isotonik", "bentuk sel tetap normal"),
                               ("sel tumbuhan dalam larutan hipotonik", "sel menjadi tegang (turgid)"), ("sel tumbuhan dalam larutan hipertonik", "terjadi plasmolisis"), ("sel tumbuhan dalam larutan isotonik", "sel lembek (flaksid)")],
            "Apa yang terjadi pada ‘{k}’?", "Dalam keadaan apa ‘{v}’?"),
           ("Istilah membran", [("fosfolipid", "molekul penyusun utama lapisan ganda membran"), ("model mosaik fluida", "membran berupa lapisan fosfolipid dengan protein yang dapat bergerak"), ("selektif permeabel", "hanya dapat dilewati zat tertentu"),
                               ("hipotonik", "larutan yang konsentrasi zat terlarutnya lebih rendah"), ("hipertonik", "larutan yang konsentrasi zat terlarutnya lebih tinggi"), ("isotonik", "larutan yang konsentrasinya sama"),
                               ("plasmolisis", "lepasnya membran sel dari dinding sel karena kehilangan air"), ("eksositosis", "pengeluaran zat dari sel dengan gelembung membran")],
            "Apa arti ‘{k}’?", "Istilah apa yang berarti ‘{v}’?")],
          ["Membran sel bersifat selektif permeabel.", "Difusi tidak memerlukan energi.", "Osmosis adalah perpindahan air melalui membran semipermeabel.",
           "Transpor aktif memerlukan ATP.", "Sel darah merah pecah dalam larutan hipotonik.", "Plasmolisis terjadi pada sel tumbuhan dalam larutan hipertonik.",
           "Pompa natrium-kalium adalah transpor aktif.", "Fagositosis termasuk endositosis."],
          [("Transpor aktif bergerak mengikuti gradien konsentrasi tanpa energi.", "Transpor aktif melawan gradien dan memerlukan ATP."), ("Sel darah merah mengerut dalam larutan hipotonik.", "Dalam larutan hipotonik sel menggembung."),
           ("Plasmolisis terjadi dalam larutan hipotonik.", "Plasmolisis terjadi dalam larutan hipertonik."), ("Eksositosis memasukkan zat ke dalam sel.", "Eksositosis mengeluarkan zat dari sel."),
           ("Membran sel tersusun atas selulosa.", "Membran sel tersusun atas fosfolipid dan protein."), ("Osmosis memindahkan air dari larutan pekat ke encer.", "Air berpindah dari larutan encer ke pekat.")],
          "transpor membran", "living-things-and-ecosystems"),

        H("B", "jaringan-tumbuhan", "Struktur dan Fungsi Jaringan Tumbuhan", "Jaringan Tumbuhan",
          "Peserta didik menjelaskan jaringan meristem dan jaringan dewasa pada tumbuhan (epidermis, parenkim, kolenkim, sklerenkim, xilem, floem), struktur organ akar, batang, dan daun, serta totipotensi.",
          "meristem apikal, lateral, interkalar, epidermis, parenkim, kolenkim, sklerenkim, xilem, floem, struktur akar, batang, daun, stomata",
          "Xilem mengangkut air, floem mengangkut hasil fotosintesis", "Jaringan meristem terus membelah, jaringan dewasa sudah memiliki fungsi khusus.",
          ["Jaringan meristem selalu membelah: meristem apikal di ujung akar dan batang (pertumbuhan memanjang), meristem lateral atau kambium (pertumbuhan membesar), dan meristem interkalar di ruas rumput.",
           "Jaringan dewasa: epidermis (pelindung), parenkim (pengisi, tempat fotosintesis dan penyimpanan), kolenkim dan sklerenkim (penguat), serta jaringan pengangkut xilem dan floem.",
           "Daun memiliki jaringan palisade dan bunga karang tempat fotosintesis, serta stomata untuk pertukaran gas. Pada tumbuhan dikotil xilem dan floem tersusun melingkar dengan kambium di antaranya; pada monokotil berkas pengangkut tersebar."],
          [("Batang jagung tidak dapat tumbuh membesar seperti pohon mangga. Mengapa?", ["Pertumbuhan membesar memerlukan kambium.", "Jagung monokotil tidak memiliki kambium."], "karena monokotil tidak memiliki kambium")],
          [("Xilem mengangkut hasil fotosintesis.", "Xilem mengangkut air dan mineral; floem mengangkut hasil fotosintesis."), ("Sklerenkim adalah jaringan yang masih aktif membelah.", "Sklerenkim adalah jaringan penguat yang selnya sudah mati."),
           ("Stomata terdapat terutama pada akar.", "Stomata terdapat terutama pada daun.")],
          [("Apa itu totipotensi?", "Kemampuan sel tumbuhan untuk tumbuh menjadi tumbuhan utuh, dasar dari kultur jaringan."),
           ("Apa itu lingkaran tahun?", "Lingkaran pada batang kayu yang terbentuk karena aktivitas kambium berbeda pada musim berbeda."),
           ("Mengapa daun memiliki lapisan kutikula?", "Lapisan lilin kutikula mengurangi penguapan air dari permukaan daun.")],
          [("Jaringan dan fungsinya", [("epidermis", "melindungi bagian dalam tumbuhan"), ("parenkim", "mengisi tubuh tumbuhan dan menyimpan cadangan makanan"), ("kolenkim", "menguatkan bagian tumbuhan yang masih muda"),
                                      ("sklerenkim", "menguatkan bagian tumbuhan yang sudah dewasa"), ("xilem", "mengangkut air dan mineral dari akar ke daun"), ("floem", "mengangkut hasil fotosintesis ke seluruh tubuh"),
                                      ("palisade", "tempat utama fotosintesis di daun"), ("stomata", "tempat pertukaran gas dan penguapan"), ("rambut akar", "memperluas bidang penyerapan air"), ("kambium", "membentuk xilem ke dalam dan floem ke luar")],
            "Apa fungsi ‘{k}’?", "Jaringan apa yang berfungsi ‘{v}’?"),
           ("Jenis meristem", [("ujung akar", "meristem apikal"), ("ujung batang", "meristem apikal"), ("kambium pembuluh", "meristem lateral"), ("kambium gabus", "meristem lateral"),
                              ("pangkal ruas batang rumput", "meristem interkalar"), ("pangkal ruas batang bambu", "meristem interkalar")],
            "Meristem di ‘{k}’ termasuk ...", "Di mana terdapat ‘{v}’?", ("meristem dermal",)),
           ("Dikotil atau monokotil", {"ciri batang dikotil": ["berkas pengangkut tersusun melingkar", "memiliki kambium", "dapat tumbuh membesar", "memiliki lingkaran tahun", "contohnya batang mangga", "berkas pengangkut kolateral terbuka", "contohnya batang kacang tanah"],
                                      "ciri batang monokotil": ["berkas pengangkut tersebar", "tidak memiliki kambium", "tidak dapat tumbuh membesar", "contohnya batang jagung", "batas korteks dan stele tidak jelas", "berkas pengangkut kolateral tertutup", "contohnya batang tebu"]})],
          ["Xilem mengangkut air dan mineral.", "Floem mengangkut hasil fotosintesis.", "Meristem apikal terdapat di ujung akar dan batang.",
           "Kambium menyebabkan batang tumbuh membesar.", "Stomata berfungsi untuk pertukaran gas.", "Jaringan palisade adalah tempat utama fotosintesis.",
           "Batang monokotil tidak memiliki kambium.", "Sel tumbuhan bersifat totipotensi."],
          [("Floem mengangkut air dari akar.", "Air diangkut xilem."), ("Batang jagung memiliki kambium.", "Jagung monokotil tidak memiliki kambium."),
           ("Kolenkim adalah jaringan pengangkut.", "Kolenkim adalah jaringan penguat."), ("Meristem interkalar terdapat di ujung akar.", "Meristem interkalar terdapat di pangkal ruas batang rumput."),
           ("Epidermis adalah tempat utama fotosintesis.", "Tempat utama fotosintesis adalah jaringan palisade."), ("Rambut akar memperkecil bidang penyerapan.", "Rambut akar memperluas bidang penyerapan.")],
          "jaringan tumbuhan", "living-things-and-ecosystems"),

        H("B", "jaringan-hewan", "Struktur dan Fungsi Jaringan Hewan", "Jaringan Hewan",
          "Peserta didik menjelaskan empat jaringan dasar hewan (epitel, ikat, otot, saraf), jenis dan fungsinya, serta organisasi kehidupan dari sel, jaringan, organ, hingga sistem organ.",
          "jaringan epitel, jaringan ikat (tulang, tulang rawan, darah, lemak), jaringan otot polos, lurik, jantung, jaringan saraf, organ dan sistem organ",
          "Hewan tersusun atas empat jaringan dasar", "Epitel melapisi, jaringan ikat menghubungkan, otot menggerakkan, dan saraf menghantarkan rangsang.",
          ["Jaringan hewan dasar ada empat: epitel (pelapis permukaan dan rongga), jaringan ikat (penghubung dan penyokong), jaringan otot (penggerak), dan jaringan saraf (penghantar rangsang).",
           "Jaringan ikat meliputi tulang, tulang rawan, darah, jaringan lemak, dan tendon. Jaringan otot ada tiga: otot polos (organ dalam, tidak sadar), otot lurik (rangka, sadar), dan otot jantung (lurik tetapi tidak sadar).",
           "Organisasi kehidupan: sel → jaringan → organ → sistem organ → organisme. Misalnya lambung adalah organ yang tersusun atas jaringan epitel, otot, ikat, dan saraf."],
          [("Otot apa yang menyusun dinding usus?", ["Usus bergerak tanpa kita sadari.", "Otot yang bekerja tidak sadar dan tidak bergaris adalah otot polos."], "otot polos")],
          [("Darah bukan jaringan karena cair.", "Darah termasuk jaringan ikat dengan matriks cair (plasma)."), ("Otot jantung bekerja di bawah kesadaran.", "Otot jantung bekerja tanpa disadari."),
           ("Satu organ hanya terdiri dari satu jenis jaringan.", "Organ tersusun atas beberapa jenis jaringan.")],
          [("Apa fungsi epitel pipih berlapis?", "Melindungi permukaan yang sering bergesekan, misalnya kulit dan rongga mulut."),
           ("Apa itu neuron?", "Sel saraf yang menghantarkan impuls, terdiri dari badan sel, dendrit, dan akson."),
           ("Apa fungsi jaringan lemak?", "Menyimpan cadangan energi, menjaga suhu tubuh, dan melindungi organ dari benturan.")],
          [("Jenis jaringan", [("kulit ari", "jaringan epitel"), ("lapisan dalam usus", "jaringan epitel"), ("dinding alveolus", "jaringan epitel"), ("tulang paha", "jaringan ikat"), ("darah", "jaringan ikat"),
                              ("tulang rawan telinga", "jaringan ikat"), ("tendon", "jaringan ikat"), ("lemak di bawah kulit", "jaringan ikat"), ("otot bisep", "jaringan otot"), ("dinding lambung yang berkontraksi", "jaringan otot"),
                              ("otak", "jaringan saraf"), ("sumsum tulang belakang", "jaringan saraf")],
            "‘{k}’ terutama tersusun atas ...", "Manakah yang terutama tersusun atas ‘{v}’?", ("jaringan meristem",)),
           ("Jenis otot", [("otot pada rangka", "otot lurik"), ("otot bisep dan trisep", "otot lurik"), ("otot pada dinding usus", "otot polos"), ("otot pada dinding pembuluh darah", "otot polos"), ("otot pada rahim", "otot polos"),
                          ("otot penyusun jantung", "otot jantung"), ("bergaris, bekerja sadar, inti banyak di tepi", "otot lurik"), ("tidak bergaris, bekerja tidak sadar, inti satu di tengah", "otot polos"),
                          ("bergaris, bercabang, bekerja tidak sadar", "otot jantung")],
            "‘{k}’ adalah ...", "Manakah ciri atau contoh ‘{v}’?", ("otot rangka polos",)),
           ("Tingkat organisasi", [("neuron", "sel"), ("sel darah merah", "sel"), ("jaringan otot jantung", "jaringan"), ("jaringan epitel usus", "jaringan"), ("jantung", "organ"), ("lambung", "organ"), ("ginjal", "organ"),
                                  ("sistem pencernaan", "sistem organ"), ("sistem peredaran darah", "sistem organ"), ("seekor kucing", "organisme")],
            "‘{k}’ termasuk tingkat organisasi ...", "Manakah contoh tingkat ‘{v}’?", ("populasi",))],
          ["Hewan memiliki empat jaringan dasar.", "Darah termasuk jaringan ikat.", "Otot jantung bekerja tidak sadar.",
           "Otot lurik melekat pada rangka.", "Jaringan saraf menghantarkan rangsang.", "Organ tersusun atas beberapa jaringan.",
           "Epitel melapisi permukaan tubuh dan rongga.", "Otot polos terdapat pada dinding usus."],
          [("Otot polos bekerja di bawah kesadaran.", "Otot polos bekerja tidak sadar."), ("Tulang termasuk jaringan epitel.", "Tulang termasuk jaringan ikat."),
           ("Jantung adalah sistem organ.", "Jantung adalah organ; sistem peredaran darah adalah sistem organnya."), ("Otot jantung tidak bergaris.", "Otot jantung bergaris dan bercabang."),
           ("Jaringan lemak tidak memiliki fungsi.", "Jaringan lemak menyimpan energi dan menjaga suhu."), ("Neuron adalah jaringan ikat.", "Neuron adalah sel saraf.")],
          "jaringan hewan", "living-things-and-ecosystems"),

        H("B", "sistem-imun", "Sistem Pertahanan Tubuh", "Sistem Imun",
          "Peserta didik menjelaskan sistem pertahanan tubuh nonspesifik dan spesifik, sel-sel imun, antigen dan antibodi, imunitas aktif dan pasif, vaksinasi, serta gangguan sistem imun.",
          "pertahanan nonspesifik (kulit, lendir, fagositosis, inflamasi), pertahanan spesifik (limfosit B dan T), antigen, antibodi, imunitas aktif dan pasif, vaksin, alergi, autoimun, AIDS",
          "Tubuh memiliki pertahanan nonspesifik dan spesifik", "Kulit dan fagosit melawan semua kuman. Limfosit B dan T mengenali kuman tertentu dan mengingatnya.",
          ["Pertahanan nonspesifik melawan semua jenis kuman: kulit, lendir, rambut hidung, enzim lisozim di air mata, sel fagosit (neutrofil, makrofag), demam, dan inflamasi (peradangan).",
           "Pertahanan spesifik dilakukan limfosit. Limfosit B menghasilkan antibodi (imunitas humoral). Limfosit T menghancurkan sel terinfeksi dan mengatur respons imun (imunitas seluler). Sel memori membuat respons kedua lebih cepat.",
           "Imunitas aktif dibentuk tubuh sendiri setelah sakit atau vaksinasi. Imunitas pasif diterima dari luar, misalnya antibodi dari ibu melalui ASI atau suntikan serum antibisa. Gangguan sistem imun: alergi, autoimun, dan AIDS."],
          [("Mengapa orang yang pernah cacar air jarang terkena lagi?", ["Tubuh membentuk sel memori setelah infeksi pertama.", "Saat virus datang lagi, sel memori segera membentuk antibodi."], "karena terbentuk sel memori (imunitas aktif)")],
          [("Antibodi dihasilkan oleh sel darah merah.", "Antibodi dihasilkan oleh limfosit B (sel plasma)."), ("Vaksin memberi imunitas pasif.", "Vaksin merangsang tubuh membentuk antibodi sendiri, jadi imunitas aktif."),
           ("Demam selalu merugikan tubuh.", "Demam ringan membantu melawan kuman sebagai pertahanan nonspesifik.")],
          [("Apa itu antigen?", "Zat asing, biasanya protein pada permukaan kuman, yang memicu pembentukan antibodi."),
           ("Bagaimana HIV melemahkan kekebalan?", "HIV menyerang limfosit T pembantu sehingga sistem imun tidak dapat bekerja dengan baik, dan penderita mudah terkena infeksi lain."),
           ("Apa itu alergi?", "Reaksi berlebihan sistem imun terhadap zat yang sebenarnya tidak berbahaya, misalnya debu, serbuk sari, atau makanan tertentu.")],
          [("Komponen pertahanan", [("kulit", "penghalang fisik masuknya kuman"), ("lendir saluran napas", "menjebak debu dan kuman"), ("lisozim pada air mata", "enzim yang merusak dinding bakteri"),
                                   ("neutrofil", "fagosit yang pertama datang ke tempat infeksi"), ("makrofag", "fagosit besar yang memakan kuman dan sel mati"), ("limfosit B", "menghasilkan antibodi"),
                                   ("limfosit T sitotoksik", "menghancurkan sel yang terinfeksi virus"), ("limfosit T pembantu", "mengaktifkan limfosit B dan T lainnya"), ("sel memori", "mengingat antigen agar respons berikutnya cepat"),
                                   ("inflamasi", "peradangan berupa merah, panas, bengkak, dan nyeri")],
            "Apa peran ‘{k}’ dalam pertahanan tubuh?", "Komponen apa yang berperan ‘{v}’?"),
           ("Jenis kekebalan", [("kekebalan setelah sembuh dari campak", "imunitas aktif alami"), ("kekebalan setelah imunisasi polio", "imunitas aktif buatan"), ("kekebalan setelah vaksin COVID-19", "imunitas aktif buatan"),
                               ("antibodi dari ibu melalui plasenta", "imunitas pasif alami"), ("antibodi dari ASI", "imunitas pasif alami"), ("suntikan serum antibisa ular", "imunitas pasif buatan"),
                               ("suntikan serum antitetanus", "imunitas pasif buatan")],
            "‘{k}’ termasuk ...", "Manakah contoh ‘{v}’?", ("imunitas bawaan semu",)),
           ("Gangguan sistem imun", [("reaksi berlebihan terhadap debu atau serbuk sari", "alergi"), ("sistem imun menyerang sel tubuh sendiri", "autoimun"), ("limfosit T pembantu dirusak virus HIV", "AIDS"),
                                    ("sistem imun menyerang sel penghasil insulin", "diabetes tipe 1"), ("sistem imun menyerang sendi", "rematik (artritis reumatoid)"), ("tubuh menolak organ hasil transplantasi", "penolakan cangkok organ")],
            "‘{k}’ disebut ...", "Apa yang dimaksud ‘{v}’?")],
          ["Kulit adalah pertahanan nonspesifik.", "Limfosit B menghasilkan antibodi.", "Limfosit T menghancurkan sel yang terinfeksi.",
           "Vaksin menghasilkan imunitas aktif buatan.", "Antibodi dari ASI memberi imunitas pasif.", "Sel memori mempercepat respons imun berikutnya.",
           "HIV menyerang limfosit T pembantu.", "Alergi adalah reaksi berlebihan sistem imun."],
          [("Antibodi dihasilkan oleh trombosit.", "Antibodi dihasilkan oleh limfosit B."), ("Suntikan serum antibisa termasuk imunitas aktif.", "Serum antibisa memberi imunitas pasif buatan."),
           ("Autoimun adalah reaksi terhadap debu.", "Reaksi terhadap debu disebut alergi; autoimun menyerang sel tubuh sendiri."), ("Kulit termasuk pertahanan spesifik.", "Kulit termasuk pertahanan nonspesifik."),
           ("Antigen dihasilkan oleh tubuh untuk melawan kuman.", "Antigen adalah zat asing; tubuh menghasilkan antibodi."), ("Neutrofil menghasilkan antibodi.", "Neutrofil adalah fagosit yang memakan kuman.")],
          "sistem pertahanan tubuh", "living-things-and-ecosystems"),
    ]
