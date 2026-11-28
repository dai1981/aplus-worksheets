# -*- coding: utf-8 -*-
"""Brasil / Ensino Médio 2ª série: Física, Química e Biologia (BNCC EM13CNT)"""
from br_sci import H, it, nq, num

D = "A que corresponde esta descrição: {v}?"


def f_termo(R):
    k = R.choice(["q", "dt", "f", "lat", "dil", "gas"])
    if k == "q":
        m, c, dt = R.choice([(200, 1, 30), (500, 1, 20), (100, 0.2, 50), (1000, 1, 60), (300, 0.5, 40), (250, 0.09, 100), (400, 1, 25)])
        return nq("Quanto calor é preciso para aquecer %d g de uma substância de calor específico %s cal/g·°C em %d °C?" % (m, num(c), dt), m * c * dt, [m * c, m * dt, c * dt, m * c * dt / 1000], "cal",
                  "Q = m·c·ΔT = %d·%s·%d = %s cal." % (m, num(c), dt, num(m * c * dt)))
    if k == "dt":
        q, m = R.choice([(6000, 200), (10000, 500), (3000, 100), (12000, 400), (8000, 250)])
        return nq("Uma amostra de %d g de água (c = 1 cal/g·°C) recebe %s cal. Quanto sua temperatura aumenta?" % (m, num(q)), q / m, [q * m, m / q, q - m, q / m / 2], "°C",
                  "ΔT = Q ÷ (m·c) = %s ÷ %d = %s °C." % (num(q), m, num(q / m)))
    if k == "f":
        c = R.choice([0, 10, 20, 25, 30, 37, 40, 100])
        f = c * 9 / 5 + 32
        return nq("Quanto vale %d °C na escala Fahrenheit?" % c, f, [c + 32, c * 9 / 5, c * 5 / 9 + 32, c + 273], "°F", "F = 1,8·C + 32 = 1,8·%d + 32 = %s °F." % (c, num(f)))
    if k == "lat":
        m, l, nm = R.choice([(100, 80, "fundir gelo a 0 °C (L = 80 cal/g)"), (50, 80, "fundir gelo a 0 °C (L = 80 cal/g)"), (200, 540, "vaporizar água a 100 °C (L = 540 cal/g)"),
                             (10, 540, "vaporizar água a 100 °C (L = 540 cal/g)"), (300, 80, "fundir gelo a 0 °C (L = 80 cal/g)"), (20, 540, "vaporizar água a 100 °C (L = 540 cal/g)")])
        return nq("Quanto calor é preciso para %s, numa massa de %d g?" % (nm, m), m * l, [m + l, m * l / 10, l, m * l * 2], "cal", "Q = m·L = %d·%d = %s cal." % (m, l, num(m * l)))
    if k == "dil":
        l0, a, dt = R.choice([(100, 1.2e-5, 50), (10, 2.4e-5, 100), (50, 1.2e-5, 40), (200, 1.7e-5, 30), (20, 2.4e-5, 50)])
        return nq("Um trilho de %d m tem coeficiente de dilatação linear %s °C⁻¹ e esquenta %d °C. Quanto ele aumenta, em metros?" % (l0, num(a), dt), l0 * a * dt, [l0 * a, a * dt, l0 * dt, l0 * a * dt * 10], "m",
                  "ΔL = L₀·α·ΔT = %d·%s·%d = %s m." % (l0, num(a), dt, num(l0 * a * dt)))
    p1, v1, t1, t2 = R.choice([(1, 10, 300, 600), (2, 6, 300, 450), (1, 4, 200, 400), (3, 5, 300, 300), (2, 10, 400, 200)])
    v2 = p1 * v1 * t2 / (t1 * p1)
    return nq("Um gás a pressão constante ocupa %d L a %d K. Qual é o volume a %d K?" % (v1, t1, t2), v2, [v1 * t1 / t2, v1 + t2 - t1, v1, v2 * 2], "L",
              "A pressão constante, V/T é constante: V₂ = %d·%d ÷ %d = %s L." % (v1, t2, t1, num(v2)))


def f_opt(R):
    k = R.choice(["esp", "aum", "n", "camara", "planos", "conv"])
    if k == "esp":
        f, p = R.choice([(10, 30), (20, 60), (15, 30), (10, 20), (12, 36), (5, 15)])
        q = 1 / (1 / f - 1 / p)
        return nq("Um espelho côncavo tem foco de %d cm. Um objeto está a %d cm. A que distância do espelho se forma a imagem?" % (f, p), q, [p - f, f + p, 1 / (1 / f + 1 / p), p], "cm",
                  "1/f = 1/p + 1/p′ → 1/p′ = 1/%d − 1/%d → p′ = %s cm." % (f, p, num(q)))
    if k == "aum":
        p, q = R.choice([(30, 15), (60, 30), (20, 60), (40, 10), (15, 30)])
        return nq("Um objeto está a %d cm de uma lente e a imagem real se forma a %d cm. Qual é o aumento (em módulo)?" % (p, q), q / p, [p / q, p * q, p + q, q - p], "vezes",
                  "|A| = p′ ÷ p = %d ÷ %d = %s." % (q, p, num(q / p)))
    if k == "n":
        v, nm = R.choice([(225000, "na água"), (200000, "no vidro"), (125000, "no diamante"), (300000, "no vácuo")])
        return nq("A luz viaja a cerca de 300.000 km/s no vácuo e a %s km/s %s. Qual é o índice de refração desse meio?" % (num(v), nm), 300000 / v, [v / 300000, 300000 - v, v / 100000, 300000 / v + 1], "",
                  "n = c ÷ v = 300.000 ÷ %s = %s." % (num(v), num(300000 / v)))
    if k == "camara":
        o, p, q = R.choice([(2, 10, 20), (1.8, 6, 12), (10, 50, 10), (3, 15, 10), (5, 20, 8)])
        return nq("Numa câmara escura, um objeto de %s m está a %d m do furo. A caixa tem %d cm de profundidade. Qual é a altura da imagem, em cm?" % (num(o), p, q), o * 100 * q / (p * 100), [o * p / q, o * 100 / q, o * q, o * 100 * q / p], "cm",
                  "i/o = p′/p → i = %s cm·%d cm ÷ %s cm = %s cm." % (num(o * 100), q, num(p * 100), num(o * q / p)))
    if k == "planos":
        a = R.choice([90, 60, 45, 30, 72, 40])
        return nq("Dois espelhos planos formam um ângulo de %d°. Quantas imagens de um objeto entre eles se formam?" % a, 360 / a - 1, [360 / a, 360 / a + 1, a / 10, 180 / a], "imagens",
                  "N = 360°/α − 1 = 360/%d − 1 = %s." % (a, num(360 / a - 1)))
    f = R.choice([0.5, 0.25, 2, 1, 0.4, 0.2])
    return nq("Uma lente convergente tem distância focal de %s m. Qual é a sua vergência, em dioptrias (“graus”)?" % num(f), 1 / f, [f, f * 10, 1 / f + 1, 2 / f], "di",
              "V = 1 ÷ f = 1 ÷ %s = %s di." % (num(f), num(1 / f)))


def f_onda(R):
    k = R.choice(["v", "f", "l", "t", "eco", "har"])
    if k == "v":
        l, f = R.choice([(0.5, 680), (2, 170), (1.5, 1000), (0.2, 1700), (3, 100)])
        return nq("Uma onda tem λ = %s m e f = %s Hz. Qual é a velocidade?" % (num(l), num(f)), l * f, [l / f, f / l, l + f, l * f * 2], "m/s", "v = λ·f = %s m/s." % num(l * f))
    if k == "f":
        v, l = R.choice([(340, 0.5), (340, 2), (1500, 3), (3e8, 3), (340, 0.85), (3e8, 1.5)])
        return nq("Uma onda viaja a %s m/s com λ = %s m. Qual é a frequência?" % (num(v), num(l)), v / l, [v * l, l / v, v / l / 10, v / l * 2], "Hz", "f = v ÷ λ = %s Hz." % num(v / l))
    if k == "l":
        f = R.choice([88e6, 100e6, 1e6, 600e3, 2.4e9, 5e9])
        return nq("Uma rádio transmite em %s Hz. Qual é o comprimento de onda (c = 3 × 10⁸ m/s)?" % num(f), 3e8 / f, [f / 3e8, 3e8 * f, 3e8 / f * 10, 3e8 / f / 10], "m",
                  "λ = c ÷ f = 3 × 10⁸ ÷ %s = %s m." % (num(f), num(3e8 / f)))
    if k == "t":
        f = R.choice([2, 4, 5, 10, 20, 50, 0.5])
        return nq("Uma onda tem frequência de %s Hz. Qual é o período?" % num(f), 1 / f, [f, 2 / f, f / 2, 1 / f + 1], "s", "T = 1 ÷ f = %s s." % num(1 / f))
    if k == "eco":
        t = R.choice([0.2, 0.4, 1, 2, 3, 0.6])
        return nq("Um grito volta como eco depois de %s s. A que distância está o paredão (v do som = 340 m/s)?" % num(t), 340 * t / 2, [340 * t, 340 / t, 340 * t * 2, 170 / t], "m",
                  "O som vai e volta: d = 340·%s ÷ 2 = %s m." % (num(t), num(340 * t / 2)))
    n, f1 = R.choice([(2, 220), (3, 110), (2, 440), (3, 200), (4, 100), (5, 60)])
    return nq("Uma corda de violão vibra no 1º harmônico a %d Hz. Qual é a frequência do %dº harmônico?" % (f1, n), n * f1, [f1, f1 + n, f1 / n, (n + 1) * f1], "Hz",
              "fₙ = n·f₁ = %d·%d = %d Hz." % (n, f1, n * f1))


def f_hidro(R):
    k = R.choice(["d", "p", "ph", "emp", "pasc", "atm"])
    if k == "d":
        m, v = R.choice([(500, 250), (270, 100), (79, 10), (1930, 100), (90, 100), (1000, 1000)])
        return nq("Um corpo de %s g ocupa %s cm³. Qual é a sua densidade?" % (num(m), num(v)), m / v, [m * v, v / m, m - v, m / v * 10], "g/cm³", "d = m ÷ V = %s g/cm³." % num(m / v))
    if k == "p":
        f, a = R.choice([(600, 0.02), (100, 0.5), (800, 0.04), (50, 0.01), (1200, 0.3), (700, 0.07)])
        return nq("Uma força de %s N age sobre %s m². Qual é a pressão?" % (num(f), num(a)), f / a, [f * a, a / f, f - a, f / a / 10], "Pa", "p = F ÷ A = %s Pa." % num(f / a))
    if k == "ph":
        h = R.choice([2, 5, 10, 20, 30, 50])
        return nq("Qual é a pressão da água (d = 1.000 kg/m³, g = 10 m/s²) a %d m de profundidade, sem contar a atmosfera?" % h, 1000 * 10 * h, [1000 * h, 10 * h, 100000 * h, 10000 / h], "Pa",
                  "p = d·g·h = 1.000·10·%d = %s Pa." % (h, num(10000 * h)))
    if k == "emp":
        v = R.choice([0.001, 0.002, 0.005, 0.01, 0.0005, 0.02])
        return nq("Um objeto de %s m³ está totalmente submerso em água (d = 1.000 kg/m³, g = 10 m/s²). Qual é o empuxo?" % num(v), 1000 * v * 10, [1000 * v, v * 10, 1000 * v * 100, 10 / v], "N",
                  "E = d·V·g = 1.000·%s·10 = %s N." % (num(v), num(10000 * v)))
    if k == "pasc":
        f1, a1, a2 = R.choice([(100, 0.01, 0.5), (50, 0.02, 1), (200, 0.05, 2), (20, 0.01, 0.4), (80, 0.04, 1.2)])
        return nq("Numa prensa hidráulica, aplica-se %d N num êmbolo de %s m². Que força surge no êmbolo de %s m²?" % (f1, num(a1), num(a2)), f1 * a2 / a1, [f1 * a1 / a2, f1, f1 * a2, f1 / a2], "N",
                  "F₁/A₁ = F₂/A₂ → F₂ = %d·%s ÷ %s = %s N." % (f1, num(a2), num(a1), num(f1 * a2 / a1)))
    h = R.choice([10, 20, 30, 40])
    return nq("A cada 10 m de profundidade na água a pressão aumenta cerca de 1 atm. Qual é a pressão total a %d m, contando a atmosfera?" % h, h / 10 + 1, [h / 10, h, h + 1, h / 10 + 2], "atm",
              "1 atm do ar + %d atm da água = %s atm." % (h // 10, num(h / 10 + 1)))


def f_sol(R):
    k = R.choice(["c", "m", "molar", "dil", "pct", "ppm"])
    if k == "c":
        m, v = R.choice([(20, 0.5), (10, 0.2), (50, 2), (9, 1), (30, 0.25), (4, 0.1)])
        return nq("Dissolvem-se %d g de sal em água até %s L de solução. Qual é a concentração comum?" % (m, num(v)), m / v, [m * v, v / m, m + v, m / v / 10], "g/L", "C = m ÷ V = %s g/L." % num(m / v))
    if k == "m":
        c, v = R.choice([(9, 0.5), (40, 0.25), (20, 2), (5, 3), (50, 0.1), (12, 1.5)])
        return nq("Que massa de soluto há em %s L de uma solução de %d g/L?" % (num(v), c), c * v, [c / v, v / c, c + v, c * v * 10], "g", "m = C·V = %s g." % num(c * v))
    if k == "molar":
        n, v = R.choice([(0.5, 1), (2, 4), (0.1, 0.5), (1, 0.25), (3, 1.5), (0.2, 2)])
        return nq("Há %s mol de soluto em %s L de solução. Qual é a concentração em mol/L?" % (num(n), num(v)), n / v, [n * v, v / n, n + v, n / v * 2], "mol/L", "[ ] = n ÷ V = %s mol/L." % num(n / v))
    if k == "dil":
        c1, v1, v2 = R.choice([(2, 0.1, 0.4), (1, 0.5, 2), (6, 0.05, 0.3), (0.5, 1, 5), (4, 0.25, 1)])
        return nq("Diluem-se %s L de uma solução %s mol/L até %s L. Qual é a nova concentração?" % (num(v1), num(c1), num(v2)), c1 * v1 / v2, [c1 * v2 / v1, c1, c1 * v1 * v2, c1 / v2], "mol/L",
                  "C₁·V₁ = C₂·V₂ → C₂ = %s·%s ÷ %s = %s mol/L." % (num(c1), num(v1), num(v2), num(c1 * v1 / v2)))
    if k == "pct":
        s, t = R.choice([(10, 200), (5, 100), (30, 150), (9, 1000), (25, 500), (4, 80)])
        return nq("Uma solução tem %d g de soluto em %s g de solução. Qual é o título em porcentagem de massa?" % (s, num(t)), s * 100 / t, [s / t, t / s, s * 100 / (t + s), s * 10 / t], "%",
                  "τ = %d ÷ %s = %s, ou seja, %s%%." % (s, num(t), num(s / t), num(s * 100 / t)))
    m, kg = R.choice([(2, 1), (5, 2), (10, 4), (0.5, 1), (3, 6)])
    return nq("Uma amostra de %s kg de água tem %s mg de chumbo. Qual é a concentração em ppm (mg/kg)?" % (num(kg), num(m)), m / kg, [m * kg, kg / m, m * 1000 / kg, m / kg / 1000], "ppm",
              "ppm = mg ÷ kg = %s ÷ %s = %s ppm." % (num(m), num(kg), num(m / kg)))


def f_tq(R):
    k = R.choice(["hess", "exo", "lig", "mol", "comb"])
    if k == "hess":
        a, b = R.choice([(-394, 283), (-286, 44), (-110, -283), (-890, 50), (-242, -44)])
        return nq("Duas etapas de uma reação têm ΔH₁ = %s kJ e ΔH₂ = %s kJ. Pela lei de Hess, qual é o ΔH total?" % (num(a), num(b)), a + b, [a - b, b - a, a * b / 100, abs(a) + abs(b)], "kJ",
                  "ΔH = ΔH₁ + ΔH₂ = %s + (%s) = %s kJ." % (num(a), num(b), num(a + b)), neg=True)
    if k == "exo":
        h = R.choice([-890, -286, -394, -1368, 178, 131, 92, -92])
        a = "exotérmica" if h < 0 else "endotérmica"
        return it("Uma reação tem ΔH = %s kJ/mol. Ela é exotérmica ou endotérmica?" % num(h), a, ["endotérmica" if h < 0 else "exotérmica", "nem uma nem outra", "depende da cor"],
                  "ΔH %s 0 indica reação %s: %s." % ("<" if h < 0 else ">", a, "libera calor" if h < 0 else "absorve calor"))
    if k == "lig":
        r, p = R.choice([(1370, 1850), (680, 860), (436 + 243, 862), (2000, 2500), (900, 700)])
        return nq("Numa reação, quebram-se ligações que exigem %s kJ e formam-se ligações que liberam %s kJ. Qual é o ΔH?" % (num(r), num(p)), r - p, [p - r, r + p, r, p], "kJ",
                  "ΔH = energia absorvida − energia liberada = %s − %s = %s kJ." % (num(r), num(p), num(r - p)), neg=True)
    if k == "mol":
        h, n = R.choice([(890, 2), (286, 3), (1368, 0.5), (394, 4), (2220, 0.25)])
        return nq("A combustão de 1 mol de um combustível libera %s kJ. Quanto calor liberam %s mol?" % (num(h), num(n)), h * n, [h / n, h + n, h, h * n * 2], "kJ",
                  "%s·%s = %s kJ." % (num(h), num(n), num(h * n)))
    g, h, mm, nm = R.choice([(32, 890, 16, "metano (16 g/mol)"), (46, 1368, 46, "etanol (46 g/mol)"), (92, 1368, 46, "etanol (46 g/mol)"), (8, 890, 16, "metano (16 g/mol)"), (88, 2220, 44, "propano (44 g/mol)")])
    return nq("A combustão de 1 mol de %s libera %s kJ. Quanto calor liberam %d g?" % (nm, num(h), g), h * g / mm, [h * g, h / g, h * mm / g, h], "kJ",
              "%d g ÷ %d g/mol = %s mol; %s·%s = %s kJ." % (g, mm, num(g / mm), num(g / mm), num(h), num(h * g / mm)))


def f_cin(R):
    k = R.choice(["vel", "ordem", "temp", "media"])
    if k == "vel":
        c1, c2, t = R.choice([(1, 0.4, 10), (2, 1, 50), (0.8, 0.2, 30), (1.5, 0.5, 20), (3, 1.2, 60), (2, 0.5, 30), (1.2, 0.6, 20), (4, 1, 100)])
        return nq("A concentração de um reagente caiu de %s para %s mol/L em %d s. Qual é a velocidade média de consumo?" % (num(c1), num(c2), t), (c1 - c2) / t, [(c1 + c2) / t, (c1 - c2) * t, c1 / t, t / (c1 - c2)], "mol/L·s",
                  "v = Δ[ ] ÷ Δt = %s ÷ %d = %s mol/L·s." % (num(c1 - c2), t, num((c1 - c2) / t)))
    if k == "ordem":
        n, f = R.choice([(1, 2), (2, 2), (1, 3), (2, 3), (3, 2), (1, 4), (2, 4), (3, 3)])
        return nq("Numa lei v = k·[A]^%d, a concentração de A é multiplicada por %d. Por quanto se multiplica a velocidade?" % (n, f), f ** n, [f * n, f, f + n, f ** (n + 1)], "",
                  "%d^%d = %d." % (f, n, f ** n))
    if k == "temp":
        d = R.choice([10, 20, 30])
        return nq("Pela regra de Van’t Hoff, a cada 10 °C a mais a velocidade de muitas reações dobra. Quanto ela aumenta com %d °C a mais?" % d, 2 ** (d // 10), [2 * (d // 10), d, d // 10, 2 ** (d // 10) + 2], "vezes",
                  "2 elevado a %d = %d vezes." % (d // 10, 2 ** (d // 10)))
    m, t = R.choice([(12, 3), (20, 5), (6, 2), (45, 9), (30, 10), (16, 4), (50, 20), (9, 6)])
    return nq("Em %d min formaram-se %d g de produto. Qual é a velocidade média de formação?" % (t, m), m / t, [m * t, t / m, m - t, m / t / 60], "g/min", "%d ÷ %d = %s g/min." % (m, t, num(m / t)))


def f_eq(R):
    k = R.choice(["ph", "poh", "kc", "h"])
    if k == "ph":
        e = R.choice([1, 2, 3, 4, 5, 6])
        return nq("Uma solução tem [H⁺] = 1 × 10%s mol/L. Qual é o pH?" % ("⁻" + str(e).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))),
                  e, [14 - e, -e, e + 1, 10 * e], "", "pH = −log[H⁺] = %d." % e)
    if k == "poh":
        p = R.choice([2, 3, 4, 5, 9, 10, 11, 12])
        return nq("Uma solução a 25 °C tem pH = %d. Qual é o pOH?" % p, 14 - p, [p, 7 - p if 7 - p > 0 else p + 7, 14 + p, p - 1], "", "pH + pOH = 14 → pOH = 14 − %d = %d." % (p, 14 - p))
    if k == "kc":
        a, b, c = R.choice([(0.1, 0.2, 0.4), (0.5, 0.5, 1), (0.2, 0.1, 0.6), (1, 2, 4), (0.4, 0.5, 0.8)])
        return nq("No equilíbrio A + B ⇌ C, [A] = %s, [B] = %s e [C] = %s mol/L. Qual é Kc?" % (num(a), num(b), num(c)), c / (a * b), [a * b / c, c / (a + b), c * a * b, c], "",
                  "Kc = [C] ÷ ([A]·[B]) = %s ÷ (%s·%s) = %s." % (num(c), num(a), num(b), num(c / (a * b))))
    p = R.choice([1, 2, 3, 4])
    return nq("Uma solução tem pH %d e outra tem pH %d. Quantas vezes a primeira tem mais H⁺?" % (p, p + 2), 100, [2, 20, 10, 1000], "vezes",
              "Cada unidade de pH vale 10 vezes: 2 unidades = 100 vezes.")


def UNITS(grade):
    return [
        H("FI", "termologia", ["EM13CNT102"], "Termologia: calor, temperatura e gases", "Termologia",
          "Realizar previsões, avaliar intervenções e/ou construir protótipos de sistemas térmicos que visem à sustentabilidade, considerando sua composição e os efeitos das variáveis termodinâmicas sobre seu funcionamento, considerando também o uso de tecnologias digitais que auxiliem no cálculo de estimativas e no apoio à construção dos protótipos.",
          "escalas termométricas, calor sensível e latente, dilatação, propagação do calor, gases ideais e termodinâmica",
          "Q = m·c·ΔT e Q = m·L", "Calor sensível muda a temperatura; calor latente muda o estado físico.",
          ["Escalas: C/5 = (F − 32)/9 e K = C + 273. Calor sensível: Q = m·c·ΔT (c é o calor específico; a água tem c = 1 cal/g·°C).",
           "Calor latente muda o estado sem mudar a temperatura: Q = m·L (fusão do gelo: 80 cal/g; vaporização da água: 540 cal/g). Dilatação linear: ΔL = L₀·α·ΔT.",
           "Gases ideais: p·V/T é constante. 1ª lei da termodinâmica: Q = τ + ΔU. Uma máquina térmica nunca transforma todo o calor em trabalho (2ª lei)."],
          [("Quanto calor aquece 100 g de água de 20 °C para 70 °C?", ["Q = m·c·ΔT.", "100·1·50."], "5.000 cal.")],
          [("Durante a fusão a temperatura do gelo sobe.", "Fica em 0 °C até fundir tudo."), ("Calor e temperatura são a mesma coisa.", "Calor é energia transferida; temperatura mede a agitação.")],
          [("Por que os trilhos têm folgas?", "Para que possam dilatar no calor sem entortar."), ("Por que a água é usada para resfriar motores?", "Por ter calor específico alto: absorve muito calor esquentando pouco.")],
          [("Conceitos", [("o calor específico", "calor para elevar 1 g da substância em 1 °C"), ("a capacidade térmica", "calor para elevar o corpo inteiro em 1 °C"), ("o calor latente", "calor por grama na mudança de estado"),
                          ("o calor sensível", "calor que muda a temperatura"), ("a dilatação térmica", "aumento das dimensões com o aquecimento"), ("a transformação isotérmica", "transformação a temperatura constante"),
                          ("a transformação isobárica", "transformação a pressão constante"), ("a transformação isovolumétrica", "transformação a volume constante"), ("a transformação adiabática", "transformação sem troca de calor")],
            "O que é {k}?", D),
           ("Leis", [("a 1ª lei da termodinâmica", "Q = τ + ΔU"), ("a 2ª lei da termodinâmica", "nenhuma máquina térmica tem rendimento de 100%"), ("a lei de Boyle", "p·V constante a temperatura constante"),
                     ("a lei de Charles e Gay-Lussac", "V/T constante a pressão constante"), ("a equação de Clapeyron", "p·V = n·R·T"), ("a lei zero da termodinâmica", "corpos em equilíbrio com um terceiro estão em equilíbrio entre si"),
                     ("a dilatação linear", "ΔL = L₀·α·ΔT"), ("o calor sensível", "Q = m·c·ΔT")],
            "O que diz ou qual é a expressão de {k}?", D),
           ("Situações", {"os exemplos de calor sensível": ["aquecer água de 20 °C para 50 °C", "esfriar o café", "esquentar a areia ao sol", "aquecer o ferro de passar", "o leite esquentando sem ferver"],
                          "os exemplos de calor latente": ["o gelo fundindo a 0 °C", "a água fervendo a 100 °C", "o vapor condensando na tampa", "a água congelando no freezer", "o suor evaporando da pele"],
                          "os exemplos de dilatação térmica": ["as juntas das pontes", "a folga entre trilhos", "o termômetro de mercúrio", "a tampa metálica que solta na água quente", "o fio da rede elétrica mais caído no verão"]})],
          ["Q = m·c·ΔT.", "Na fusão a temperatura fica constante.", "A água tem calor específico alto.", "K = C + 273.", "p·V/T é constante para um gás ideal.", "Nenhuma máquina térmica tem rendimento de 100%.",
           "Os trilhos têm folgas por causa da dilatação."],
          [("Na fusão a temperatura do gelo sobe.", "Fica constante."), ("Calor latente muda a temperatura.", "Muda o estado físico."), ("A água tem calor específico baixo.", "Tem calor específico alto."),
           ("Uma máquina térmica pode ter rendimento de 100%.", "A 2ª lei impede."), ("K = C − 273.", "K = C + 273.")],
          "a termologia", "energy", calc=f_termo),

        H("FI", "optica-geometrica", ["EM13CNT103"], "Óptica geométrica: espelhos e lentes", "Óptica geométrica",
          "Utilizar o conhecimento sobre as radiações e suas origens para avaliar as potencialidades e os riscos de sua aplicação em equipamentos de uso cotidiano, na saúde, no ambiente, na indústria, na agricultura e na geração de energia elétrica, incluindo o funcionamento de instrumentos ópticos.",
          "propagação retilínea, reflexão, espelhos planos e esféricos, refração, lentes, olho humano e instrumentos ópticos",
          "1/f = 1/p + 1/p′", "Espelho côncavo e lente convergente concentram a luz; convexo e divergente espalham.",
          ["A luz se propaga em linha reta (câmara escura, sombras). Na reflexão, o ângulo de incidência é igual ao de reflexão.",
           "Espelhos esféricos e lentes seguem a equação de Gauss: 1/f = 1/p + 1/p′; aumento A = −p′/p. Côncavo e convergente têm foco real; convexo e divergente, virtual.",
           "Na refração a luz muda de velocidade e de direção: n = c/v. Vergência V = 1/f (em dioptrias, os graus dos óculos). Miopia usa lente divergente; hipermetropia, convergente."],
          [("Um objeto está a 30 cm de um espelho côncavo de foco 10 cm. Onde se forma a imagem?", ["1/p′ = 1/10 − 1/30 = 2/30.", "p′ = 15 cm."], "A 15 cm do espelho (imagem real).")],
          [("O espelho plano inverte em cima e embaixo.", "Ele troca direita e esquerda, sem inverter em cima e embaixo."), ("Lente convergente sempre aumenta.", "Depende da posição do objeto.")],
          [("Por que o retrovisor do lado direito é convexo?", "Porque aumenta o campo de visão, embora diminua as imagens."), ("Por que o lápis parece quebrado no copo d’água?", "Pela refração da luz ao passar da água para o ar.")],
          [("Instrumentos", [("o espelho do dentista", "côncavo, para ampliar"), ("o retrovisor de moto", "convexo, para ampliar o campo de visão"), ("o espelho de banheiro", "plano"),
                             ("o farol do carro", "côncavo, para concentrar o feixe"), ("a lupa", "lente convergente"), ("os óculos de míope", "lente divergente"),
                             ("os óculos de hipermetrope", "lente convergente"), ("o espelho de segurança na garagem", "convexo, para ampliar o campo de visão")],
            "Que tipo de espelho ou lente é usado em {k}?", None),
           ("Conceitos", [("a reflexão regular", "luz refletida em superfície polida, formando imagens"), ("a reflexão difusa", "luz espalhada em várias direções por superfície rugosa"),
                          ("a refração", "mudança de velocidade e direção da luz ao mudar de meio"), ("o índice de refração", "razão entre a velocidade da luz no vácuo e no meio"),
                          ("a reflexão total", "toda a luz volta para o meio de origem, como na fibra óptica"), ("o foco", "ponto onde raios paralelos se encontram"),
                          ("a vergência", "inverso da distância focal, em dioptrias"), ("a imagem virtual", "imagem formada pelos prolongamentos dos raios")],
            "O que é {k}?", D),
           ("Imagens", {"as características das imagens em espelho plano": ["imagem virtual", "mesmo tamanho do objeto", "mesma distância do espelho", "direita e esquerda trocadas", "imagem direita, não invertida"],
                        "as características das imagens em espelho convexo": ["sempre virtual", "sempre menor", "sempre direita", "campo de visão maior", "foco virtual"],
                        "os fenômenos da luz no dia a dia": ["o arco-íris", "a miragem no asfalto", "o lápis quebrado no copo", "o brilho do diamante", "a sombra ao meio-dia"]})],
          ["A luz se propaga em linha reta.", "O ângulo de incidência é igual ao de reflexão.", "O retrovisor convexo amplia o campo de visão.", "A miopia é corrigida com lente divergente.",
           "A fibra óptica usa reflexão total.", "n = c/v.", "A lupa é uma lente convergente."],
          [("O espelho plano inverte em cima e embaixo.", "Troca direita e esquerda."), ("A miopia se corrige com lente convergente.", "Com lente divergente."), ("O espelho convexo forma imagens maiores.", "Forma imagens menores."),
           ("Na refração a luz não muda de velocidade.", "Ela muda de velocidade."), ("A imagem no espelho plano é real.", "É virtual.")],
          "a óptica geométrica", "waves-and-light", calc=f_opt),

        H("FI", "ondulatoria", ["EM13CNT103"], "Ondulatória e acústica", "Ondulatória",
          "Utilizar o conhecimento sobre as radiações e suas origens para avaliar as potencialidades e os riscos de sua aplicação em equipamentos de uso cotidiano, na saúde, no ambiente, na indústria, na agricultura e na geração de energia elétrica.",
          "ondas mecânicas e eletromagnéticas, transversais e longitudinais, v = λ·f, período, reflexão, refração, difração, interferência, ressonância, efeito Doppler e qualidades do som",
          "v = λ·f e T = 1/f", "Altura (grave ou agudo) depende da frequência; intensidade depende da amplitude.",
          ["Ondas mecânicas precisam de meio (som); eletromagnéticas não (luz, rádio). Transversais vibram perpendicularmente à propagação; longitudinais, na mesma direção (som).",
           "Equação fundamental: v = λ·f. O período é T = 1/f. Fenômenos: reflexão (eco), refração, difração (contornar obstáculos), interferência, ressonância e efeito Doppler.",
           "Qualidades do som: altura (frequência: grave ou agudo), intensidade (amplitude: forte ou fraco, em decibéis) e timbre (forma da onda, que distingue instrumentos)."],
          [("Um som de 340 m/s e 170 Hz tem qual comprimento de onda?", ["λ = v ÷ f.", "340 ÷ 170."], "2 m.")],
          [("Som agudo é som alto em volume.", "Agudo é frequência alta; volume é intensidade."), ("A luz é onda longitudinal.", "É transversal.")],
          [("O que é o efeito Doppler?", "A mudança da frequência percebida quando a fonte se aproxima ou se afasta, como na sirene da ambulância."), ("Por que a ponte pode balançar com ventos?", "Por ressonância, quando a frequência coincide com a natural da estrutura.")],
          [("Fenômenos", [("o eco", "reflexão"), ("ouvir alguém atrás de um muro", "difração"), ("as cores numa bolha de sabão", "interferência"), ("a sirene que muda de tom ao passar", "efeito Doppler"),
                          ("a taça que quebra com uma nota cantada", "ressonância"), ("o som que muda de velocidade do ar para a água", "refração"), ("o fone com cancelamento de ruído", "interferência"),
                          ("a ultrassonografia", "reflexão"), ("o radar de velocidade", "efeito Doppler")],
            "Que fenômeno ondulatório explica {k}?", None, ("dilatação",)),
           ("Conceitos", [("a frequência", "número de oscilações por segundo"), ("o período", "tempo de uma oscilação completa"), ("o comprimento de onda", "distância entre duas cristas"),
                          ("a amplitude", "deslocamento máximo a partir do equilíbrio"), ("o timbre", "qualidade que distingue instrumentos na mesma nota"), ("a altura do som", "qualidade ligada à frequência"),
                          ("a intensidade do som", "qualidade ligada à amplitude e à energia"), ("o decibel", "unidade do nível sonoro"), ("o infrassom", "som abaixo de 20 Hz")],
            "O que é {k}?", D),
           ("Tipos", {"as ondas longitudinais": ["o som no ar", "o ultrassom", "a onda P dos terremotos", "a onda numa mola comprimida", "o infrassom dos elefantes"],
                      "as ondas transversais": ["a luz", "a onda numa corda", "as ondas de rádio", "a onda S dos terremotos", "os raios X"],
                      "as ondas eletromagnéticas": ["as micro-ondas", "o infravermelho", "a luz visível", "o ultravioleta", "os raios gama"]})],
          ["v = λ·f.", "O som é uma onda longitudinal.", "A luz é uma onda transversal.", "O eco é reflexão do som.", "O timbre distingue instrumentos.", "Frequência alta dá som agudo.",
           "O efeito Doppler muda a frequência percebida."],
          [("Agudo significa volume alto.", "Agudo é frequência alta."), ("O som se propaga no vácuo.", "Precisa de um meio."), ("A luz é onda longitudinal.", "É transversal."),
           ("O timbre depende só da frequência.", "Depende da forma da onda."), ("O período é igual à frequência.", "T = 1/f.")],
          "a ondulatória", "waves-and-light", calc=f_onda),

        H("FI", "hidrostatica", ["EM13CNT307"], "Hidrostática: pressão, densidade e empuxo", "Hidrostática",
          "Analisar as propriedades dos materiais para avaliar a adequação de seu uso em diferentes aplicações, considerando densidade, pressão, flutuação e equipamentos hidráulicos.",
          "densidade, pressão, pressão hidrostática, Stevin, pressão atmosférica, Pascal, prensa hidráulica e Arquimedes",
          "p = F ÷ A e E = d·V·g", "A pressão na água aumenta cerca de 1 atm a cada 10 m de profundidade.",
          ["Densidade: d = m ÷ V. Pressão: p = F ÷ A, em pascal (Pa). Quanto menor a área, maior a pressão (faca afiada, salto fino).",
           "Lei de Stevin: a pressão num líquido aumenta com a profundidade, p = p₀ + d·g·h. Torricelli mediu a pressão atmosférica: 1 atm ≈ 10⁵ Pa ≈ 76 cmHg.",
           "Princípio de Pascal: a pressão se transmite igualmente no líquido (prensa e freio hidráulico). Arquimedes: o empuxo é E = d_líquido·V_submerso·g."],
          [("Por que um navio de aço flutua?", ["O casco tem muito ar dentro.", "A densidade média do navio é menor que a da água."], "Porque a densidade média do navio é menor que a da água.")],
          [("Corpos pesados sempre afundam.", "Depende da densidade, não só do peso."), ("A pressão no fundo depende da forma do recipiente.", "Depende só da profundidade e do líquido.")],
          [("Por que os ouvidos doem no fundo da piscina?", "A pressão da água aumenta com a profundidade."), ("Por que o canudinho funciona?", "Reduzimos a pressão na boca e a pressão atmosférica empurra o líquido.")],
          [("Princípios", [("a prensa hidráulica", "princípio de Pascal"), ("o freio hidráulico do carro", "princípio de Pascal"), ("o elevador de carros do posto", "princípio de Pascal"),
                           ("o navio flutuando", "princípio de Arquimedes"), ("o submarino subindo e descendo", "princípio de Arquimedes"), ("o balão de ar quente", "princípio de Arquimedes"),
                           ("a caixa-d’água no alto da casa", "lei de Stevin"), ("a barragem mais grossa embaixo", "lei de Stevin"), ("os vasos comunicantes", "lei de Stevin")],
            "Que princípio ou lei explica {k}?", None, ("lei de Ohm",)),
           ("Conceitos", [("a densidade", "massa por unidade de volume"), ("a pressão", "força por unidade de área"), ("o pascal", "unidade de pressão no SI"), ("o empuxo", "força vertical para cima feita pelo fluido"),
                          ("a pressão atmosférica", "pressão do peso do ar sobre a superfície"), ("o barômetro", "aparelho que mede a pressão atmosférica"), ("o manômetro", "aparelho que mede a pressão de gases e líquidos"),
                          ("a pressão hidrostática", "pressão causada pela coluna de líquido")],
            "O que é {k}?", D),
           ("Flutua?", {"o que flutua na água": ["a madeira seca", "o gelo", "o isopor", "o óleo de cozinha", "a rolha"], "o que afunda na água": ["o ferro maciço", "a pedra", "o chumbo", "o vidro maciço", "a moeda"],
                        "o que aumenta a pressão sobre uma superfície": ["diminuir a área de contato", "aumentar a força", "afiar a faca", "usar salto fino", "afundar mais na água"]})],
          ["d = m ÷ V.", "p = F ÷ A.", "A pressão aumenta com a profundidade.", "O empuxo é igual ao peso do líquido deslocado.", "A prensa hidráulica usa o princípio de Pascal.",
           "O gelo flutua na água.", "1 atm é cerca de 10⁵ Pa."],
          [("A pressão no fundo depende da forma do recipiente.", "Depende da profundidade."), ("Corpos pesados sempre afundam.", "Depende da densidade."), ("Quanto maior a área, maior a pressão.", "Maior área, menor pressão."),
           ("O empuxo aponta para baixo.", "Aponta para cima."), ("A pressão atmosférica aumenta com a altitude.", "Diminui com a altitude.")],
          "a hidrostática", "forces-and-motion", calc=f_hidro),

        H("QU", "solucoes", ["EM13CNT307"], "Soluções e concentrações", "Soluções",
          "Analisar as propriedades dos materiais para avaliar a adequação de seu uso em diferentes aplicações, considerando a solubilidade, as concentrações e as diluições de soluções do cotidiano.",
          "soluto, solvente, solubilidade, curvas de solubilidade, concentração comum, molaridade, título, ppm e diluição",
          "C = m ÷ V e M = n ÷ V", "Na diluição, a quantidade de soluto não muda: C₁·V₁ = C₂·V₂.",
          ["Solução é mistura homogênea de soluto e solvente. Solubilidade é a quantidade máxima de soluto que se dissolve numa quantidade de solvente a uma temperatura.",
           "Concentração comum: C = m ÷ V (g/L). Concentração em quantidade de matéria: M = n ÷ V (mol/L). Título: τ = m soluto ÷ m solução. ppm: partes por milhão (mg/kg).",
           "Na diluição acrescenta-se solvente e a massa de soluto não muda: C₁·V₁ = C₂·V₂. Solução saturada já tem o máximo de soluto dissolvido."],
          [("O soro fisiológico tem 9 g/L de sal. Quanto sal há em 0,5 L?", ["m = C·V.", "9·0,5."], "4,5 g.")],
          [("Diluir muda a massa de soluto.", "Só aumenta o volume de solução."), ("Todo sólido fica mais solúvel com o calor.", "A maioria sim, mas há exceções; gases ficam menos solúveis no calor.")],
          [("Por que o refrigerante quente perde gás?", "A solubilidade dos gases diminui com o aumento da temperatura."), ("O que é solução supersaturada?", "Tem mais soluto dissolvido que o normal e é instável.")],
          [("Conceitos", [("o soluto", "substância dissolvida"), ("o solvente", "substância que dissolve, geralmente em maior quantidade"), ("a solução saturada", "solução com o máximo de soluto dissolvido"),
                          ("a solução insaturada", "solução com menos soluto que o máximo"), ("a solução supersaturada", "solução instável com soluto acima do máximo"),
                          ("a solubilidade", "máximo de soluto que se dissolve numa quantidade de solvente"), ("a diluição", "adição de solvente a uma solução"), ("o corpo de fundo", "soluto não dissolvido no fundo")],
            "O que é {k}?", D),
           ("Unidades", [("a concentração comum", "g/L"), ("a concentração em quantidade de matéria", "mol/L"), ("o título em massa", "sem unidade ou em %"), ("as partes por milhão", "ppm, ou mg/kg"),
                         ("a densidade da solução", "g/mL"), ("a massa molar", "g/mol"), ("o volume da solução", "litro (L)")],
            "Qual é a unidade de {k}?", D),
           ("Exemplos", {"as soluções do dia a dia": ["o soro fisiológico", "o vinagre", "a água do mar", "o álcool 70%", "o refrigerante sem bolhas aparentes"],
                         "os fatores que aumentam a dissolução de um sólido": ["agitar", "aquecer, na maioria dos casos", "triturar o sólido", "usar mais solvente", "usar solvente adequado"],
                         "os fatores que aumentam a solubilidade de um gás na água": ["baixar a temperatura", "aumentar a pressão do gás", "fechar bem a garrafa", "manter a bebida gelada", "comprimir o gás no líquido"]})],
          ["C = m ÷ V.", "Na diluição a massa de soluto não muda.", "Solução saturada tem o máximo de soluto.", "Gases ficam menos solúveis no calor.", "1 ppm é 1 mg por kg.",
           "M = n ÷ V.", "O soro fisiológico tem 9 g/L de NaCl."],
          [("Diluir aumenta a massa de soluto.", "A massa de soluto não muda."), ("Gases ficam mais solúveis no calor.", "Ficam menos solúveis."), ("A molaridade é medida em g/L.", "É medida em mol/L."),
           ("Solução supersaturada é estável.", "É instável."), ("O solvente é sempre o sal.", "O solvente geralmente é a água.")],
          "as soluções", "matter", calc=f_sol),

        H("QU", "termoquimica", ["EM13CNT101"], "Termoquímica", "Termoquímica",
          "Analisar e representar as transformações e conservações em sistemas que envolvam quantidade de matéria, de energia e de movimento para realizar previsões sobre seus comportamentos em situações cotidianas e em processos produtivos, considerando a energia das reações químicas.",
          "reações exotérmicas e endotérmicas, entalpia, ΔH, lei de Hess, energia de ligação e poder calorífico",
          "ΔH negativo: libera calor", "Exotérmica: ΔH negativo. Endotérmica: ΔH positivo. Lei de Hess: somam-se as etapas.",
          ["Reação exotérmica libera calor (combustão, ΔH < 0). Endotérmica absorve calor (fotossíntese, ΔH > 0).",
           "Entalpia (H) é o conteúdo de energia; ΔH = H produtos − H reagentes. A lei de Hess diz que o ΔH total é a soma dos ΔH das etapas.",
           "Quebrar ligações absorve energia e formar ligações libera energia: ΔH = energia das ligações quebradas − energia das ligações formadas."],
          [("A combustão do metano tem ΔH = −890 kJ/mol. Ela é exotérmica ou endotérmica?", ["ΔH negativo.", "A reação libera calor."], "Exotérmica.")],
          [("Quebrar ligações libera energia.", "Quebrar absorve; formar libera."), ("ΔH positivo indica liberação de calor.", "ΔH positivo é endotérmica.")],
          [("Por que a bolsa de gelo instantâneo esfria?", "Ocorre uma dissolução endotérmica, que absorve calor."), ("O que é poder calorífico?", "Energia liberada na queima de 1 kg ou 1 g de combustível.")],
          [("Exo ou endo", [("a combustão do gás de cozinha", "exotérmica"), ("a queima do etanol", "exotérmica"), ("a respiração celular", "exotérmica"), ("a neutralização ácido-base", "exotérmica"),
                            ("a condensação do vapor", "exotérmica"), ("a solidificação da água", "exotérmica"), ("a fotossíntese", "endotérmica"), ("a fusão do gelo", "endotérmica"),
                            ("a evaporação da água", "endotérmica"), ("o cozimento de um ovo", "endotérmica"), ("a decomposição do calcário em cal", "endotérmica"), ("a explosão da pólvora", "exotérmica"), ("a eletrólise da água", "endotérmica")],
            "Como se classifica {k}?", None, ("atérmica",)),
           ("Conceitos", [("a entalpia", "conteúdo de energia de um sistema a pressão constante"), ("o ΔH", "variação de entalpia: H produtos − H reagentes"), ("a lei de Hess", "o ΔH total é a soma dos ΔH das etapas"),
                          ("a energia de ligação", "energia para quebrar 1 mol de uma ligação"), ("o poder calorífico", "energia liberada por massa de combustível queimado"),
                          ("a entalpia de formação", "ΔH para formar 1 mol de substância a partir de substâncias simples"), ("a entalpia de combustão", "ΔH da queima completa de 1 mol"),
                          ("o calorímetro", "aparelho que mede o calor de reações")],
            "O que é {k}?", D),
           ("Situações", {"os processos que liberam calor": ["queimar carvão", "a ferrugem se formando", "a cal viva com água", "a respiração celular", "a bolsa térmica que esquenta"],
                          "os processos que absorvem calor": ["a fotossíntese", "derreter gelo", "a bolsa de gelo instantâneo", "cozinhar alimentos", "evaporar o suor"],
                          "os combustíveis": ["o etanol", "o gás natural", "a gasolina", "o hidrogênio", "o carvão"]})],
          ["Exotérmica tem ΔH negativo.", "A fotossíntese é endotérmica.", "Quebrar ligações absorve energia.", "A lei de Hess soma as etapas.", "A combustão é exotérmica.",
           "A fusão do gelo é endotérmica.", "O calorímetro mede o calor das reações."],
          [("Quebrar ligações libera energia.", "Absorve energia."), ("A fotossíntese é exotérmica.", "É endotérmica."), ("ΔH positivo indica reação exotérmica.", "Indica endotérmica."),
           ("A combustão absorve calor.", "Libera calor."), ("A lei de Hess vale só para uma etapa.", "Vale para a soma de etapas.")],
          "a termoquímica", "energy", calc=f_tq),

        H("QU", "cinetica-quimica", ["EM13CNT101"], "Cinética química", "Cinética química",
          "Analisar e representar as transformações em sistemas que envolvam quantidade de matéria e de energia para realizar previsões sobre a rapidez das reações em situações cotidianas e em processos produtivos.",
          "velocidade média, teoria das colisões, energia de ativação, temperatura, concentração, superfície de contato, catalisador e lei da velocidade",
          "Mais colisões eficazes, reação mais rápida", "Temperatura, concentração, superfície e catalisador aceleram as reações.",
          ["A velocidade média é a variação de concentração ou de quantidade por tempo. Pela teoria das colisões, as partículas precisam colidir com energia e orientação adequadas.",
           "Energia de ativação é a energia mínima para a reação começar. O catalisador oferece um caminho com menor energia de ativação e não é consumido.",
           "Aceleram a reação: aumentar a temperatura, a concentração, a superfície de contato (pó reage mais rápido) e usar catalisador. Lei da velocidade: v = k·[A]ᵃ·[B]ᵇ."],
          [("Por que o comprimido triturado dissolve mais rápido?", ["Triturar aumenta a superfície de contato.", "Mais partículas expostas colidem com a água."], "Pela maior superfície de contato.")],
          [("O catalisador é consumido na reação.", "Ele é recuperado no fim."), ("O catalisador muda o ΔH.", "Muda só a energia de ativação.")],
          [("Por que a geladeira conserva alimentos?", "A baixa temperatura deixa mais lentas as reações de decomposição."), ("Para que serve o catalisador do carro?", "Acelera a transformação de gases tóxicos em gases menos nocivos.")],
          [("Fatores", [("guardar alimentos na geladeira", "diminuir a temperatura"), ("cozinhar na panela de pressão", "aumentar a temperatura"), ("usar fermento em pó triturado", "aumentar a superfície de contato"),
                        ("a enzima da saliva digerindo o amido", "catalisador"), ("a lenha em gravetos que queima mais rápido", "aumentar a superfície de contato"),
                        ("o ácido mais concentrado que reage mais rápido", "aumentar a concentração"), ("o conversor catalítico do carro", "catalisador"), ("congelar a carne", "diminuir a temperatura")],
            "Que fator altera a velocidade em {k}?", None),
           ("Conceitos", [("a energia de ativação", "energia mínima para a reação ocorrer"), ("o complexo ativado", "estado intermediário de maior energia"), ("o catalisador", "substância que acelera sem ser consumida"),
                          ("o inibidor", "substância que torna a reação mais lenta"), ("a colisão eficaz", "choque com energia e orientação adequadas"), ("a enzima", "catalisador biológico"),
                          ("a velocidade média", "variação da quantidade de reagente ou produto por tempo"), ("a ordem de reação", "expoente da concentração na lei da velocidade")],
            "O que é {k}?", D),
           ("Efeito", {"o que acelera uma reação": ["aumentar a temperatura", "aumentar a concentração", "triturar o sólido", "adicionar catalisador", "agitar a mistura"],
                       "o que torna uma reação mais lenta": ["resfriar", "diluir os reagentes", "usar pedaços grandes", "adicionar inibidor", "guardar no escuro reações sensíveis à luz"],
                       "o que o catalisador não muda": ["o ΔH da reação", "a quantidade de produto no fim", "a sua própria massa no fim", "os reagentes envolvidos", "a energia dos produtos"]})],
          ["O catalisador diminui a energia de ativação.", "Aquecer acelera as reações.", "Triturar aumenta a superfície de contato.", "Enzimas são catalisadores biológicos.",
           "O catalisador não é consumido.", "A geladeira deixa as reações mais lentas.", "Maior concentração aumenta as colisões."],
          [("O catalisador é consumido.", "Não é consumido."), ("O catalisador muda o ΔH.", "Muda só a energia de ativação."), ("Resfriar acelera a reação.", "Deixa mais lenta."),
           ("Pedaços grandes reagem mais rápido que pó.", "O pó tem mais superfície e reage mais rápido."), ("Toda colisão produz reação.", "Só as colisões eficazes.")],
          "a cinética química", "matter", calc=f_cin),

        H("QU", "equilibrio-quimico", ["EM13CNT101"], "Equilíbrio químico e pH", "Equilíbrio químico",
          "Analisar e representar as transformações em sistemas que envolvam quantidade de matéria e de energia para realizar previsões sobre seus comportamentos, considerando reações reversíveis, o equilíbrio químico e o pH.",
          "reações reversíveis, constante de equilíbrio, princípio de Le Chatelier, pH, pOH e soluções-tampão",
          "No equilíbrio as velocidades se igualam", "Le Chatelier: o sistema reage para diminuir a perturbação. pH + pOH = 14.",
          ["Numa reação reversível, o equilíbrio é atingido quando as velocidades direta e inversa se igualam; as concentrações ficam constantes.",
           "Kc é o produto das concentrações dos produtos dividido pelo dos reagentes, cada uma elevada ao seu coeficiente. Princípio de Le Chatelier: ao mudar concentração, pressão ou temperatura, o equilíbrio se desloca para diminuir a mudança.",
           "pH = −log[H⁺] e pOH = −log[OH⁻]; a 25 °C, pH + pOH = 14. Cada unidade de pH é 10 vezes mais ou menos H⁺. Tampões resistem a variações de pH (o sangue tem pH ≈ 7,4)."],
          [("Se [H⁺] = 1 × 10⁻³ mol/L, qual é o pH?", ["pH = −log[H⁺].", "−log 10⁻³ = 3."], "pH = 3.")],
          [("No equilíbrio a reação para.", "As duas reações continuam com a mesma velocidade."), ("pH 4 tem o dobro de H⁺ de pH 5.", "Tem 10 vezes mais H⁺.")],
          [("Por que o refrigerante faz espuma ao abrir?", "A pressão cai e o equilíbrio do CO₂ dissolvido se desloca para liberar gás."), ("O que é tampão?", "Solução que resiste a mudanças de pH, como a do sangue.")],
          [("Le Chatelier", [("adicionar reagente", "desloca para os produtos"), ("retirar produto", "desloca para os produtos"), ("adicionar produto", "desloca para os reagentes"),
                             ("aquecer uma reação exotérmica", "desloca para os reagentes"), ("aquecer uma reação endotérmica", "desloca para os produtos"),
                             ("aumentar a pressão com menos mols de gás nos produtos", "desloca para os produtos"), ("adicionar catalisador", "não desloca o equilíbrio"),
                             ("diminuir a pressão com menos mols de gás nos produtos", "desloca para os reagentes")],
            "Para onde se desloca o equilíbrio ao {k}?", None),
           ("Conceitos", [("o equilíbrio químico", "estado com velocidades direta e inversa iguais"), ("a constante de equilíbrio", "razão entre concentrações de produtos e reagentes no equilíbrio"),
                          ("o princípio de Le Chatelier", "o sistema se desloca para diminuir a perturbação"), ("o pH", "−log da concentração de H⁺"), ("o pOH", "−log da concentração de OH⁻"),
                          ("a solução-tampão", "solução que resiste a variações de pH"), ("a reação reversível", "reação que ocorre nos dois sentidos"), ("o indicador ácido-base", "substância que muda de cor com o pH")],
            "O que é {k}?", D),
           ("pH", {"as soluções ácidas a 25 °C": ["pH 2", "pH 4", "[H⁺] maior que 10⁻⁷ mol/L", "pOH 12", "pH 6"], "as soluções básicas a 25 °C": ["pH 10", "pH 12", "[H⁺] menor que 10⁻⁷ mol/L", "pOH 3", "pH 8"],
                   "as soluções neutras a 25 °C": ["pH 7", "pOH 7", "[H⁺] igual a 10⁻⁷ mol/L", "[H⁺] igual a [OH⁻]", "água pura"]})],
          ["No equilíbrio as velocidades se igualam.", "O catalisador não desloca o equilíbrio.", "pH + pOH = 14 a 25 °C.", "pH 3 tem 10 vezes mais H⁺ que pH 4.", "O sangue é tamponado.",
           "Aquecer uma reação endotérmica favorece os produtos.", "Adicionar reagente desloca para os produtos."],
          [("No equilíbrio a reação para.", "Continua nos dois sentidos."), ("O catalisador desloca o equilíbrio.", "Só acelera a chegada ao equilíbrio."), ("pH 4 tem o dobro de H⁺ de pH 5.", "Tem 10 vezes mais."),
           ("Adicionar produto desloca para os produtos.", "Desloca para os reagentes."), ("pH + pOH = 7.", "pH + pOH = 14 a 25 °C.")],
          "o equilíbrio químico", "matter", calc=f_eq),

        H("BI", "fisiologia-humana", ["EM13CNT207", "EM13CNT202"], "Fisiologia humana", "Fisiologia humana",
          "Identificar, analisar e discutir vulnerabilidades vinculadas às vivências e aos desafios contemporâneos aos quais as juventudes estão expostas, considerando os aspectos físico, psicoemocional e social, a fim de desenvolver e divulgar ações de prevenção e de promoção da saúde e do bem-estar; analisar o funcionamento integrado dos sistemas do corpo humano.",
          "digestão, respiração, circulação, excreção, sistema nervoso, sistema endócrino, sistema imunitário e saúde",
          "Os sistemas trabalham integrados", "Hormônios e nervos regulam o corpo; o sistema imunitário o defende.",
          ["Digestão: enzimas quebram os alimentos (amilase na boca, pepsina no estômago, lipase no intestino). Os nutrientes são absorvidos no intestino delgado.",
           "Respiração e circulação levam oxigênio às células e retiram CO₂. A circulação humana é dupla e completa: o sangue passa duas vezes pelo coração. Os rins filtram o sangue nos néfrons.",
           "O sistema nervoso usa impulsos rápidos; o endócrino, hormônios (insulina, adrenalina, tiroxina). O sistema imunitário usa glóbulos brancos e anticorpos; as vacinas criam memória imunológica."],
          [("Que hormônio reduz a glicose no sangue?", ["É produzido pelo pâncreas.", "Facilita a entrada da glicose nas células."], "A insulina.")],
          [("As veias sempre levam sangue pobre em oxigênio.", "As veias pulmonares levam sangue oxigenado."), ("Antibiótico combate vírus.", "Combate bactérias.")],
          [("Por que o diabetes tipo 1 exige insulina?", "Porque o pâncreas produz pouca ou nenhuma insulina."), ("O que faz a adrenalina?", "Prepara o corpo para luta ou fuga: acelera o coração e a respiração.")],
          [("Hormônios", [("a insulina", "diminui a glicose no sangue"), ("o glucagon", "aumenta a glicose no sangue"), ("a adrenalina", "prepara o corpo para luta ou fuga"), ("a tiroxina", "regula o metabolismo"),
                          ("o hormônio do crescimento", "estimula o crescimento"), ("o ADH", "reduz a perda de água na urina"), ("a testosterona", "desenvolve características sexuais masculinas"),
                          ("o estrogênio", "desenvolve características sexuais femininas")],
            "Qual é a função de {k}?", D),
           ("Órgãos e funções", [("o néfron", "unidade de filtração do rim"), ("o alvéolo pulmonar", "local da troca de gases"), ("as vilosidades intestinais", "aumentam a absorção de nutrientes"),
                                 ("o pâncreas", "produz insulina e suco pancreático"), ("o fígado", "produz bile e armazena glicogênio"), ("o timo", "amadurece linfócitos T"),
                                 ("o hipotálamo", "controla a temperatura e a hipófise"), ("o bulbo", "controla a respiração e os batimentos cardíacos")],
            "O que é ou o que faz {k}?", D),
           ("Sistemas", {"as defesas do corpo": ["a pele", "os glóbulos brancos", "os anticorpos", "a febre", "o muco das vias respiratórias"],
                         "as enzimas digestivas": ["a amilase salivar", "a pepsina", "a lipase", "a tripsina", "a lactase"],
                         "as glândulas endócrinas": ["a hipófise", "a tireoide", "as suprarrenais", "os ovários", "os testículos"]})],
          ["A insulina reduz a glicose no sangue.", "A circulação humana é dupla e completa.", "O néfron filtra o sangue.", "A pepsina age no estômago.", "Vacinas criam memória imunológica.",
           "A adrenalina acelera o coração.", "As trocas gasosas ocorrem nos alvéolos."],
          [("A insulina aumenta a glicose no sangue.", "Ela diminui."), ("Antibióticos curam viroses.", "Combatem bactérias."), ("As veias pulmonares levam sangue pobre em oxigênio.", "Levam sangue oxigenado."),
           ("A digestão do amido começa no intestino grosso.", "Começa na boca, com a amilase."), ("Os rins produzem a bile.", "Quem produz a bile é o fígado.")],
          "a fisiologia humana", "living-things-and-ecosystems"),

        H("BI", "botanica", ["EM13CNT202"], "Botânica: grupos e fisiologia das plantas", "Botânica",
          "Analisar as diversas formas de manifestação da vida em seus diferentes níveis de organização, bem como as condições ambientais favoráveis e os fatores limitantes a elas, considerando os grupos vegetais e sua fisiologia.",
          "briófitas, pteridófitas, gimnospermas, angiospermas, tecidos vegetais, xilema, floema, fotossíntese, hormônios vegetais",
          "Briófitas, pteridófitas, gimnospermas, angiospermas", "Xilema leva seiva bruta; floema leva seiva elaborada.",
          ["Briófitas (musgos) não têm vasos. Pteridófitas (samambaias) têm vasos, mas não sementes. Gimnospermas (pinheiros, araucária) têm sementes nuas. Angiospermas têm flores e frutos.",
           "O xilema leva a seiva bruta (água e sais) da raiz às folhas; o floema leva a seiva elaborada (açúcares) das folhas para o resto da planta.",
           "Os estômatos controlam as trocas gasosas e a transpiração. Hormônios: auxina (crescimento e fototropismo), giberelina, citocinina, etileno (amadurecimento dos frutos)."],
          [("A araucária é gimnosperma ou angiosperma?", ["A araucária tem pinhões.", "As sementes não ficam dentro de um fruto."], "Gimnosperma.")],
          [("O fruto é só o que é doce.", "Fruto é o ovário desenvolvido da flor: o tomate e o feijão também são frutos."), ("Plantas só respiram à noite.", "Respiram o tempo todo; de dia também fazem fotossíntese.")],
          [("Por que colocar banana verde num saco com fruta madura?", "A fruta madura libera etileno, que acelera o amadurecimento."), ("O que é fototropismo?", "O crescimento da planta em direção à luz, comandado pela auxina.")],
          [("Grupo", [("o musgo", "briófita"), ("a hepática", "briófita"), ("a samambaia", "pteridófita"), ("a avenca", "pteridófita"), ("o xaxim", "pteridófita"), ("a araucária", "gimnosperma"),
                      ("o pinheiro", "gimnosperma"), ("o cipreste", "gimnosperma"), ("o ipê", "angiosperma"), ("o milho", "angiosperma"), ("a laranjeira", "angiosperma"), ("o feijoeiro", "angiosperma")],
            "A que grupo vegetal pertence {k}?", None, ("alga",)),
           ("Estruturas", [("o xilema", "transporta a seiva bruta"), ("o floema", "transporta a seiva elaborada"), ("o estômato", "controla trocas gasosas e transpiração"), ("o meristema", "tecido que produz novas células"),
                           ("a epiderme", "reveste e protege a planta"), ("o parênquima clorofiliano", "tecido onde ocorre a fotossíntese"), ("a auxina", "hormônio do crescimento e do fototropismo"),
                           ("o etileno", "hormônio do amadurecimento dos frutos"), ("o súber", "cortiça que protege troncos")],
            "O que é ou o que faz {k}?", D),
           ("Características", {"as características das briófitas": ["sem vasos condutores", "vivem em locais úmidos", "são pequenas", "fase dominante é o gametófito", "dependem da água para a fecundação"],
                                "as características das angiospermas": ["têm flores", "têm frutos", "sementes protegidas no fruto", "são o grupo mais diverso", "incluem monocotiledôneas e eudicotiledôneas"],
                                "as características das gimnospermas": ["sementes nuas", "não têm frutos", "muitas têm folhas em agulha", "formam pinhas ou estróbilos", "incluem a araucária"]})],
          ["Os musgos não têm vasos.", "As samambaias não têm sementes.", "A araucária é gimnosperma.", "As angiospermas têm frutos.", "O xilema leva a seiva bruta.",
           "O etileno amadurece os frutos.", "A auxina comanda o fototropismo."],
          [("O floema leva a seiva bruta.", "O xilema leva a seiva bruta."), ("As samambaias têm sementes.", "Reproduzem-se por esporos."), ("As gimnospermas têm frutos.", "Têm sementes nuas."),
           ("As plantas só respiram à noite.", "Respiram o tempo todo."), ("O tomate não é fruto.", "É fruto: vem do ovário da flor.")],
          "a botânica", "living-things-and-ecosystems"),

        H("BI", "zoologia", ["EM13CNT202"], "Zoologia: diversidade dos animais", "Zoologia",
          "Analisar as diversas formas de manifestação da vida em seus diferentes níveis de organização, bem como as condições ambientais favoráveis e os fatores limitantes a elas, considerando a diversidade dos animais.",
          "poríferos, cnidários, platelmintos, nematódeos, anelídeos, moluscos, artrópodes, equinodermos e cordados",
          "Dos poríferos aos cordados", "Artrópodes são o maior filo; vertebrados são cordados com coluna vertebral.",
          ["Invertebrados: poríferos (esponjas), cnidários (águas-vivas), platelmintos (tênia), nematódeos (lombriga), anelídeos (minhoca), moluscos (caramujo, polvo), artrópodes (insetos, aranhas, crustáceos) e equinodermos (estrela-do-mar).",
           "Artrópodes têm exoesqueleto de quitina e patas articuladas; é o filo com mais espécies.",
           "Cordados com coluna vertebral formam os vertebrados: peixes, anfíbios, répteis, aves e mamíferos. Aves e mamíferos são endotérmicos (temperatura do corpo constante)."],
          [("A aranha é inseto?", ["Insetos têm 6 patas e antenas.", "A aranha tem 8 patas e não tem antenas."], "Não: é um aracnídeo.")],
          [("Todo animal que vive na água é peixe.", "Baleias são mamíferos; polvos são moluscos."), ("Répteis mantêm a temperatura constante.", "Répteis são ectotérmicos.")],
          [("Por que os artrópodes trocam de pele?", "O exoesqueleto não cresce; eles fazem muda para crescer."), ("Que verminoses estão ligadas à falta de saneamento?", "Ascaridíase, esquistossomose e teníase, entre outras.")],
          [("Filo", [("a esponja-do-mar", "poríferos"), ("a água-viva", "cnidários"), ("o coral", "cnidários"), ("a tênia", "platelmintos"), ("a planária", "platelmintos"), ("a lombriga", "nematódeos"),
                     ("a minhoca", "anelídeos"), ("a sanguessuga", "anelídeos"), ("o polvo", "moluscos"), ("o caramujo", "moluscos"), ("o camarão", "artrópodes"), ("a borboleta", "artrópodes"),
                     ("o ouriço-do-mar", "equinodermos"), ("a estrela-do-mar", "equinodermos"), ("o sapo", "cordados")],
            "A que filo pertence {k}?", None),
           ("Características", [("os poríferos", "corpo cheio de poros e sem tecidos verdadeiros"), ("os cnidários", "células urticantes nos tentáculos"), ("os platelmintos", "corpo achatado"),
                                ("os nematódeos", "corpo cilíndrico, não segmentado"), ("os anelídeos", "corpo dividido em anéis"), ("os moluscos", "corpo mole, muitos com concha"),
                                ("os artrópodes", "exoesqueleto e patas articuladas"), ("os equinodermos", "pele com espinhos e sistema ambulacral"), ("os cordados", "notocorda em alguma fase da vida")],
            "Qual característica marca {k}?", D),
           ("Artrópodes e vertebrados", {"os insetos": ["a abelha", "a formiga", "o gafanhoto", "a barata", "o mosquito"], "os aracnídeos": ["a aranha", "o escorpião", "o carrapato", "o ácaro", "a caranguejeira"],
                                         "os crustáceos": ["o camarão", "o caranguejo", "a lagosta", "o tatuzinho-de-jardim", "o siri"]})],
          ["Os artrópodes têm exoesqueleto.", "A aranha tem 8 patas.", "A minhoca é anelídeo.", "O polvo é molusco.", "As aves são endotérmicas.", "A água-viva tem células urticantes.",
           "A estrela-do-mar é equinodermo."],
          [("A aranha é inseto.", "É aracnídeo."), ("O polvo é peixe.", "É molusco."), ("Répteis são endotérmicos.", "São ectotérmicos."), ("A minhoca é platelminto.", "É anelídeo."),
           ("O camarão é inseto.", "É crustáceo.")],
          "a zoologia", "living-things-and-ecosystems"),
    ]
