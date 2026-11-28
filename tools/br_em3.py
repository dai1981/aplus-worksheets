# -*- coding: utf-8 -*-
"""Brasil / Ensino Médio 3ª série: Física, Química e Biologia (BNCC EM13CNT)"""
from br_sci import H, it, nq, num

D = "A que corresponde esta descrição: {v}?"
K9 = 9e9


def f_estat(R):
    k = R.choice(["coul", "dist", "campo", "carga", "e", "pot"])
    if k == "coul":
        q1, q2, d = R.choice([(2e-6, 3e-6, 0.1), (1e-6, 1e-6, 0.3), (4e-6, 5e-6, 0.2), (3e-6, 6e-6, 0.3), (1e-6, 2e-6, 0.1), (5e-6, 2e-6, 0.5)])
        f = K9 * q1 * q2 / (d * d)
        return nq("Duas cargas de %s C e %s C estão a %s m. Qual é a força elétrica entre elas (k = 9 × 10⁹ N·m²/C²)?" % (num(q1), num(q2), num(d)), f,
                  [f * d, K9 * q1 * q2 / d, f / 10, f * 2], "N", "F = k·q₁·q₂/d² = %s N." % num(f))
    if k == "dist":
        n = R.choice([2, 3, 4, 5])
        return it("Duas cargas se atraem com força F. Se a distância for multiplicada por %d, qual será a nova força?" % n, "F/%d" % (n * n), ["F/%d" % n, "%d·F" % n, "%d·F" % (n * n)],
                  "A força é inversamente proporcional ao quadrado da distância: F/%d² = F/%d." % (n, n * n))
    if k == "campo":
        f, q = R.choice([(0.02, 2e-6), (0.5, 1e-6), (6, 3e-6), (0.1, 5e-6), (0.9, 3e-6)])
        return nq("Uma carga de %s C sofre uma força de %s N num campo elétrico. Qual é a intensidade do campo?" % (num(q), num(f)), f / q, [f * q, q / f, f / q / 10, f / q * 2], "N/C",
                  "E = F ÷ q = %s N/C." % num(f / q))
    if k == "carga":
        n = R.choice([1e12, 2e13, 5e12, 3e14, 6.25e18, 1e15])
        return nq("Um corpo perdeu %s elétrons. Qual é a sua carga (e = 1,6 × 10⁻¹⁹ C)?" % num(n), n * 1.6e-19, [n / 1.6e-19, 1.6e-19, n * 1.6e-18, n * 1.6e-20], "C",
                  "Q = n·e = %s·1,6 × 10⁻¹⁹ = %s C (positiva, pois perdeu elétrons)." % (num(n), num(n * 1.6e-19)))
    if k == "e":
        q, d = R.choice([(2e-6, 0.3), (1e-6, 0.1), (4e-6, 0.2), (9e-9, 0.3), (5e-6, 0.5)])
        e = K9 * q / (d * d)
        return nq("Qual é o campo elétrico de uma carga puntiforme de %s C a %s m dela (k = 9 × 10⁹ N·m²/C²)?" % (num(q), num(d)), e, [K9 * q / d, e * d * d, e / 2, e * 10], "N/C",
                  "E = k·Q/d² = %s N/C." % num(e))
    q, u = R.choice([(2e-6, 100), (5e-6, 20), (1e-3, 12), (3e-6, 1000), (4e-6, 50)])
    return nq("Uma carga de %s C é levada entre dois pontos com diferença de potencial de %d V. Qual é o trabalho da força elétrica?" % (num(q), u), q * u, [q / u, u / q, q * u * 10, q * u / 10], "J",
              "τ = q·U = %s J." % num(q * u))


def f_eletro(R):
    k = R.choice(["ohm", "serie", "par", "pot", "kwh", "q"])
    if k == "ohm":
        u, i = R.choice([(12, 2), (220, 4), (9, 0.3), (110, 2.5), (24, 0.5), (127, 10)])
        return nq("Um resistor ligado a %d V é percorrido por %s A. Qual é a resistência?" % (u, num(i)), u / i, [u * i, i / u, u - i, u / i / 2], "Ω", "R = U ÷ I = %s Ω." % num(u / i))
    if k == "serie":
        a, b, c = R.choice([(2, 3, 5), (10, 20, 30), (4, 6, 10), (100, 200, 300), (1, 2, 3), (5, 5, 10)])
        return nq("Três resistores de %d Ω, %d Ω e %d Ω estão em série. Qual é a resistência equivalente?" % (a, b, c), a + b + c, [1 / (1 / a + 1 / b + 1 / c), a * b * c, (a + b + c) / 3, a + b], "Ω",
                  "Em série soma-se: %d + %d + %d = %d Ω." % (a, b, c, a + b + c))
    if k == "par":
        a, b = R.choice([(6, 3), (4, 4), (12, 6), (10, 10), (20, 5), (30, 60)])
        r = a * b / (a + b)
        return nq("Dois resistores de %d Ω e %d Ω estão em paralelo. Qual é a resistência equivalente?" % (a, b), r, [a + b, a * b, (a + b) / 2, abs(a - b) if a != b else a * 2], "Ω",
                  "Req = R₁·R₂ ÷ (R₁ + R₂) = %d ÷ %d = %s Ω." % (a * b, a + b, num(r)))
    if k == "pot":
        u, r = R.choice([(220, 10), (12, 6), (110, 22), (220, 44), (9, 3), (127, 12.7)])
        return nq("Um resistor de %s Ω está ligado a %d V. Qual é a potência dissipada?" % (num(r), u), u * u / r, [u * r, u / r, u * u * r, u * u / r / 2], "W",
                  "P = U²/R = %s W." % num(u * u / r))
    if k == "kwh":
        p, h, d = R.choice([(4400, 0.5, 30), (1000, 2, 30), (100, 8, 30), (2000, 1, 20), (5500, 0.25, 30)])
        return nq("Um aparelho de %s W funciona %s h por dia durante %d dias. Quanto consome, em kWh?" % (num(p), num(h), d), p * h * d / 1000, [p * h * d, p * h / 1000, p * d / 1000, p * h * d / 100], "kWh",
                  "E = %s kW·%s h·%d = %s kWh." % (num(p / 1000), num(h), d, num(p * h * d / 1000)))
    i, t = R.choice([(2, 10), (0.5, 60), (3, 20), (10, 5), (0.2, 100)])
    return nq("Uma corrente de %s A passa por um fio durante %d s. Que carga atravessa o fio?" % (num(i), t), i * t, [i / t, t / i, i + t, i * t * 10], "C", "Q = i·Δt = %s C." % num(i * t))


def f_mag(R):
    k = R.choice(["f", "fio", "fem", "trafo", "v"])
    if k == "f":
        b, q, v = R.choice([(0.5, 2e-6, 1000), (2, 1e-6, 500), (0.1, 3e-6, 2000), (1, 4e-6, 100), (0.2, 5e-6, 3000)])
        return nq("Uma carga de %s C entra perpendicularmente num campo de %s T com velocidade %s m/s. Qual é a força magnética?" % (num(q), num(b), num(v)), q * v * b,
                  [q * v / b, b * v, q * b, q * v * b * 10], "N", "F = q·v·B = %s N." % num(q * v * b))
    if k == "fio":
        b, i, l = R.choice([(0.5, 2, 0.4), (0.2, 5, 1), (1, 3, 0.5), (0.1, 10, 2), (2, 1, 0.3)])
        return nq("Um fio de %s m com corrente de %s A está perpendicular a um campo de %s T. Qual é a força sobre o fio?" % (num(l), num(i), num(b)), b * i * l, [b * i, i * l, b * l, b * i * l * 2], "N",
                  "F = B·i·L = %s N." % num(b * i * l))
    if k == "fem":
        d, t = R.choice([(0.6, 0.2), (2, 0.5), (0.3, 0.1), (5, 1), (1.2, 0.4)])
        return nq("O fluxo magnético numa espira varia %s Wb em %s s. Qual é a força eletromotriz induzida (em módulo)?" % (num(d), num(t)), d / t, [d * t, t / d, d + t, d / t / 2], "V",
                  "Lei de Faraday: ε = ΔΦ ÷ Δt = %s V." % num(d / t))
    if k == "trafo":
        n1, n2, u1 = R.choice([(1000, 100, 220), (500, 50, 127), (200, 1000, 12), (100, 2000, 110), (2000, 100, 220)])
        return nq("Um transformador tem %s espiras no primário e %s no secundário. Se a tensão no primário é %d V, qual é a tensão no secundário?" % (num(n1), num(n2), u1), u1 * n2 / n1,
                  [u1 * n1 / n2, u1, u1 * n2, n2 / n1], "V", "U₂/U₁ = N₂/N₁ → U₂ = %d·%s ÷ %s = %s V." % (u1, num(n2), num(n1), num(u1 * n2 / n1)))
    b, l, v = R.choice([(0.5, 0.2, 10), (1, 0.5, 4), (0.2, 1, 5), (2, 0.1, 20), (0.4, 0.5, 8)])
    return nq("Uma barra de %s m se move a %d m/s perpendicular a um campo de %s T. Qual é a fem induzida?" % (num(l), v, num(b)), b * l * v, [b * l, l * v, b * v, b * l * v * 2], "V",
              "ε = B·L·v = %s V." % num(b * l * v))


def f_mod(R):
    k = R.choice(["fot", "gamma", "emc", "lambda", "foto"])
    h = 6.6e-34
    if k == "fot":
        f = R.choice([5e14, 6e14, 1e15, 4e14, 3e15, 7.5e14])
        return nq("Qual é a energia de um fóton de frequência %s Hz (h = 6,6 × 10⁻³⁴ J·s)?" % num(f), h * f, [h / f, f / h, h * f * 10, h * f / 10], "J", "E = h·f = %s J." % num(h * f))
    if k == "gamma":
        v, g = R.choice([("0,6c", 1.25), ("0,8c", 1 / 0.6), ("0,866c", 2), ("0,28c", 1 / 0.96)])
        t = R.choice([1, 2, 5, 10])
        return nq("Um relógio numa nave a %s marca %d s. Quanto tempo passa para um observador na Terra (γ = %s)?" % (v, t, num(g)), g * t, [t / g, t, g, t + g], "s",
                  "Dilatação do tempo: Δt = γ·Δt₀ = %s·%d = %s s." % (num(g), t, num(g * t)))
    if k == "emc":
        m = R.choice([1e-3, 1, 2e-3, 0.5, 1e-6, 0.01])
        return nq("Quanta energia corresponde a uma massa de %s kg (E = m·c², c = 3 × 10⁸ m/s)?" % num(m), m * 9e16, [m * 3e8, m * 9e8, m * 9e17, m * 3e16], "J", "E = m·c² = %s·9 × 10¹⁶ = %s J." % (num(m), num(m * 9e16)))
    if k == "lambda":
        f = R.choice([5e14, 6e14, 1e15, 3e8, 1e18, 1.5e15])
        return nq("Qual é o comprimento de onda de uma radiação de %s Hz (c = 3 × 10⁸ m/s)?" % num(f), 3e8 / f, [f / 3e8, 3e8 * f, 3e8 / f * 10, 3e8 / f / 10], "m", "λ = c ÷ f = %s m." % num(3e8 / f))
    e, w = R.choice([(5, 2), (8, 3), (6, 4.5), (10, 2.3), (4, 2.2), (3.5, 2)])
    return nq("Fótons de %s eV incidem num metal com função trabalho %s eV. Qual é a energia cinética máxima dos elétrons emitidos?" % (num(e), num(w)), e - w, [e + w, e, w, e * w], "eV",
              "Efeito fotoelétrico: Ec = h·f − φ = %s − %s = %s eV." % (num(e), num(w), num(e - w)))


def f_eq(R):
    k = R.choice(["ddp", "mass", "carga", "pilha"])
    if k == "ddp":
        a, b, na, nb = R.choice([(0.34, -0.76, "o cobre", "o zinco"), (0.80, 0.34, "a prata", "o cobre"), (0.34, -0.44, "o cobre", "o ferro"), (0.80, -0.76, "a prata", "o zinco"), (-0.13, -0.76, "o chumbo", "o zinco"),
                                 (0.34, -2.37, "o cobre", "o magnésio")])
        return nq("Numa pilha, o potencial de redução de %s é %s V e o de %s é %s V. Qual é a ddp da pilha?" % (na, num(a, 2) if a else "0", nb, num(b, 2)), a - b, [a + b, b - a, abs(a) + abs(b) + 0.5, a], "V",
                  "ΔE = E(cátodo) − E(ânodo) = %s − (%s) = %s V." % (num(a, 2), num(b, 2), num(a - b, 3)), neg=True)
    if k == "carga":
        i, t = R.choice([(2, 965), (5, 1930), (1, 9650), (10, 965), (4, 4825)])
        return nq("Numa eletrólise passa uma corrente de %d A durante %s s. Quantos mols de elétrons circulam (F = 96.500 C/mol)?" % (i, num(t)), i * t / 96500, [i * t, i * t / 9650, 96500 / (i * t), i * t / 965000], "mol",
                  "Q = i·t = %s C; n = %s ÷ 96.500 = %s mol de e⁻." % (num(i * t), num(i * t), num(i * t / 96500)))
    if k == "mass":
        n = R.choice([0.2, 0.4, 1, 2, 0.1])
        return nq("Na eletrólise, Cu²⁺ + 2 e⁻ → Cu. Que massa de cobre se deposita com %s mol de elétrons (Cu = 63,5 g/mol)?" % num(n), n / 2 * 63.5, [n * 63.5, n * 2 * 63.5, 63.5 / n, n / 2], "g",
                  "%s mol de e⁻ ÷ 2 = %s mol de Cu → %s·63,5 = %s g." % (num(n), num(n / 2), num(n / 2), num(n / 2 * 63.5)))
    p = R.choice([("zinco e cobre", "o zinco", "o cobre"), ("ferro e cobre", "o ferro", "o cobre"), ("magnésio e prata", "o magnésio", "a prata"), ("zinco e prata", "o zinco", "a prata"),
                  ("alumínio e cobre", "o alumínio", "o cobre")])
    if R.random() < 0.5:
        return it("Numa pilha de %s, qual metal é o ânodo (sofre oxidação)?" % p[0], p[1], [p[2], "os dois", "nenhum"], "O metal mais reativo (menor potencial de redução), %s, perde elétrons." % p[1])
    return it("Numa pilha de %s, em qual eletrodo ocorre a redução (cátodo)?" % p[0], p[2], [p[1], "nos dois", "em nenhum"], "No cátodo, o metal de maior potencial de redução, %s, recebe elétrons." % p[2])


def f_radio(R):
    k = R.choice(["meia", "frac", "tempo", "alfa", "beta"])
    if k == "meia":
        m, n = R.choice([(80, 2), (100, 3), (64, 4), (200, 1), (320, 5), (40, 3)])
        return nq("Uma amostra de %d g de um isótopo passa por %d meias-vidas. Quanto resta?" % (m, n), m / 2 ** n, [m / (2 * n), m - m / 2 ** n, m / 2, m / 2 ** (n + 1)], "g",
                  "%d ÷ 2^%d = %s g." % (m, n, num(m / 2 ** n)))
    if k == "frac":
        n = R.choice([1, 2, 3, 4, 5])
        return it("Depois de %d meias-vidas, que fração de um isótopo radioativo ainda resta?" % n, "1/%d" % 2 ** n, ["1/%d" % (2 * n) if 2 * n != 2 ** n else "1/%d" % (2 * n + 1), "%d/%d" % (2 ** n - 1, 2 ** n), "1/%d" % 2 ** (n + 1)],
                  "A cada meia-vida a quantidade cai à metade: (1/2)^%d = 1/%d." % (n, 2 ** n))
    if k == "tempo":
        p, n = R.choice([(8, 3), (5730, 2), (30, 2), (8, 4), (28, 3), (1600, 2)])
        return nq("Um isótopo tem meia-vida de %s anos. Quanto tempo leva para restar 1/%d da amostra?" % (num(p), 2 ** n), p * n, [p * 2 ** n, p / n, p, p * (n + 1)], "anos",
                  "1/%d = (1/2)^%d: são %d meias-vidas, %d·%s = %s." % (2 ** n, n, n, n, num(p), num(p * n)))
    if k == "alfa":
        e, z, a = R.choice([("urânio-238", 92, 238), ("rádio-226", 88, 226), ("polônio-210", 84, 210), ("tório-232", 90, 232), ("plutônio-239", 94, 239)])
        return it("O %s (Z = %d) emite uma partícula alfa. Quais são o novo Z e o novo A?" % (e, z), "Z = %d e A = %d" % (z - 2, a - 4), ["Z = %d e A = %d" % (z - 1, a), "Z = %d e A = %d" % (z + 1, a), "Z = %d e A = %d" % (z - 4, a - 2)],
                  "A partícula alfa tem 2 prótons e 2 nêutrons: Z diminui 2 e A diminui 4.")
    e, z, a = R.choice([("carbono-14", 6, 14), ("iodo-131", 53, 131), ("estrôncio-90", 38, 90), ("césio-137", 55, 137)])
    return it("O %s (Z = %d) emite uma partícula beta. Quais são o novo Z e o novo A?" % (e, z), "Z = %d e A = %d" % (z + 1, a), ["Z = %d e A = %d" % (z - 1, a), "Z = %d e A = %d" % (z - 2, a - 4), "Z = %d e A = %d" % (z, a - 1)],
              "Na emissão beta um nêutron vira próton: Z aumenta 1 e A não muda.")


def f_gen(R):
    k = R.choice(["mono", "di", "sang", "sexo", "prob", "dalt"])
    if k == "mono":
        a, b, ans, w = R.choice([("Aa", "Aa", "1/4", ["1/2", "3/4", "0"]), ("Aa", "aa", "1/2", ["1/4", "3/4", "1"]), ("AA", "aa", "0", ["1/4", "1/2", "1"]), ("Aa", "AA", "0", ["1/4", "1/2", "3/4"])])
        return it("No cruzamento %s × %s, qual é a probabilidade de um filho aa?" % (a, b), ans, w, "Montando o quadro de Punnett para %s × %s, a fração aa é %s." % (a, b, ans))
    if k == "di":
        return it(R.choice(["No cruzamento AaBb × AaBb, qual é a proporção fenotípica esperada?", "Pela 2ª lei de Mendel, que proporção resulta de AaBb × AaBb?"]), "9 : 3 : 3 : 1", ["3 : 1", "1 : 2 : 1", "1 : 1 : 1 : 1"],
                  "Os dois genes se segregam de forma independente: 9 : 3 : 3 : 1.")
    if k == "sang":
        p, f = R.choice([("A (IAi) × B (IBi)", "A, B, AB e O"), ("AB × O", "A e B"), ("O × O", "só O"), ("A (IAIA) × B (IBIB)", "só AB"), ("AB × AB", "A, B e AB")])
        w = [x for x in ["A, B, AB e O", "A e B", "só O", "só AB", "A, B e AB"] if x != f]
        return it("Quais tipos sanguíneos podem ter os filhos de um casal %s?" % p, f, R.sample(w, 3), "Combinando os alelos de cada genitor, os filhos podem ser: %s." % f)
    if k == "sexo":
        n = R.choice([1, 2, 3])
        return it("Qual é a probabilidade de um casal ter %d %s, todos meninos?" % (n, "filho" if n == 1 else "filhos"), "1/%d" % 2 ** n, ["1/%d" % (2 ** n * 2), "1/%d" % (n + 1) if n + 1 != 2 ** n else "1/%d" % (n + 3), "%d/%d" % (2 ** n - 1, 2 ** n)] if n > 1 else ["1/4", "1/3", "1"],
                  "Cada filho tem 1/2 de chance de ser menino: (1/2)^%d = 1/%d." % (n, 2 ** n))
    if k == "dalt":
        return it("Uma mulher portadora de daltonismo (XᴰXᵈ) e um homem de visão normal (XᴰY) têm um filho homem. Qual é a chance de ele ser daltônico?", "1/2", ["1/4", "0", "1"],
                  "O filho homem recebe o Y do pai e um X da mãe: metade das vezes o Xᵈ.")
    n = R.choice([16, 32, 64, 160, 320])
    return nq("Num cruzamento AaBb × AaBb nasceram %d descendentes. Quantos se espera com os dois caracteres recessivos (aabb)?" % n, n / 16, [n / 4, n * 9 / 16, n * 3 / 16, n / 8], "",
              "aabb é 1/16: %d ÷ 16 = %s." % (n, num(n / 16)))


def UNITS(grade):
    return [
        H("FI", "eletrostatica", ["EM13CNT107"], "Eletrostática", "Eletrostática",
          "Realizar previsões qualitativas e quantitativas sobre o funcionamento de geradores, motores elétricos e seus componentes, bobinas, transformadores, pilhas, baterias e dispositivos eletrônicos, com base na análise dos processos de transformação e condução de energia envolvidos, começando pelas cargas elétricas e seus campos.",
          "carga elementar, eletrização, condutores e isolantes, lei de Coulomb, campo elétrico, potencial e para-raios",
          "Cargas iguais se repelem, opostas se atraem", "F = k·q₁·q₂/d² e E = F/q.",
          ["A carga elétrica é quantizada: Q = n·e, com e = 1,6 × 10⁻¹⁹ C. Um corpo que perde elétrons fica positivo; que ganha, negativo.",
           "Eletrização por atrito (cargas opostas), contato (mesmo sinal) e indução. Condutores deixam as cargas se moverem; isolantes não.",
           "Lei de Coulomb: F = k·q₁·q₂/d², com k = 9 × 10⁹ N·m²/C². Campo elétrico: E = F/q, e de uma carga puntiforme E = k·Q/d². Trabalho: τ = q·U."],
          [("Uma régua atritada com papel atrai pedacinhos de papel. Por quê?", ["A régua fica carregada.", "Ela induz cargas no papel, que é atraído."], "Por eletrização por atrito e indução.")],
          [("O corpo positivo ganhou prótons.", "Ele perdeu elétrons; os prótons não saem do núcleo."), ("Dobrar a distância divide a força por 2.", "Divide por 4.")],
          [("Como funciona o para-raios?", "Oferece um caminho condutor para as descargas irem ao solo, pelo poder das pontas."), ("Por que dentro do carro estamos protegidos de raios?", "Pela blindagem eletrostática da carroceria metálica (gaiola de Faraday).")],
          [("Eletrização", [("passar o pente no cabelo seco", "atrito"), ("o balão esfregado na blusa", "atrito"), ("encostar uma esfera carregada em outra neutra", "contato"),
                            ("tocar uma esfera neutra com outra carregada e separá-las", "contato"), ("aproximar um corpo carregado e ligar o outro à terra", "indução"),
                            ("o papel atraído por uma régua carregada sem encostar", "indução"), ("tocar a maçaneta e levar um choque depois de andar no tapete", "atrito")],
            "Qual processo de eletrização está em jogo nesta situação: {k}?", None, ("convecção",)),
           ("Conceitos", [("a carga elementar", "1,6 × 10⁻¹⁹ C"), ("o coulomb", "unidade de carga elétrica"), ("o campo elétrico", "região onde uma carga sofre força elétrica"),
                          ("o potencial elétrico", "energia potencial por unidade de carga"), ("o eletroscópio", "aparelho que indica se um corpo está carregado"),
                          ("a gaiola de Faraday", "condutor oco que blinda o interior de campos elétricos"), ("o poder das pontas", "acúmulo de cargas nas pontas dos condutores"),
                          ("a constante eletrostática", "9 × 10⁹ N·m²/C² no vácuo")],
            "O que é {k}?", D),
           ("Materiais", {"os condutores elétricos": ["o cobre", "o alumínio", "o corpo humano", "a água com sais", "o grafite"], "os isolantes elétricos": ["a borracha", "o vidro", "o plástico", "a porcelana", "a madeira seca"],
                          "as aplicações da eletrostática": ["o para-raios", "a impressora a laser", "a pintura eletrostática de carros", "o filtro eletrostático de chaminé", "a fotocopiadora"]})],
          ["Cargas iguais se repelem.", "Q = n·e.", "Na eletrização por atrito os corpos ficam com cargas opostas.", "F = k·q₁·q₂/d².", "O para-raios usa o poder das pontas.",
           "A carroceria do carro funciona como gaiola de Faraday.", "Um corpo positivo perdeu elétrons."],
          [("Corpo positivo ganhou prótons.", "Perdeu elétrons."), ("Dobrar a distância divide a força por 2.", "Divide por 4."), ("A borracha é boa condutora.", "É isolante."),
           ("Na eletrização por contato os corpos ficam com cargas opostas.", "Ficam com cargas de mesmo sinal."), ("Cargas opostas se repelem.", "Cargas opostas se atraem.")],
          "a eletrostática", "energy", calc=f_estat),

        H("FI", "eletrodinamica", ["EM13CNT107", "EM13CNT106"], "Eletrodinâmica: corrente, resistores e potência", "Eletrodinâmica",
          "Realizar previsões qualitativas e quantitativas sobre o funcionamento de dispositivos elétricos com base na análise dos processos de transformação e condução de energia; avaliar tecnologias e possíveis soluções para as demandas que envolvem a geração, o transporte, a distribuição e o consumo de energia elétrica.",
          "corrente, tensão, leis de Ohm, associação de resistores, potência, efeito Joule, consumo e segurança elétrica",
          "U = R·i e P = U·i", "Série: resistências somam. Paralelo: 1/Req = 1/R₁ + 1/R₂.",
          ["Corrente é carga por tempo: i = Q/Δt (ampère). A 1ª lei de Ohm diz que U = R·i. A 2ª lei: R = ρ·L/A (fios longos e finos resistem mais).",
           "Em série a corrente é a mesma e as resistências somam. Em paralelo a tensão é a mesma e 1/Req = 1/R₁ + 1/R₂ (para dois: R₁·R₂/(R₁ + R₂)).",
           "Potência: P = U·i = R·i² = U²/R. Energia consumida: E = P·Δt, cobrada em kWh. No efeito Joule a energia elétrica vira calor (chuveiro, ferro)."],
          [("Qual é a resistência equivalente de 6 Ω e 3 Ω em paralelo?", ["Req = 6·3 ÷ (6 + 3).", "18 ÷ 9."], "2 Ω.")],
          [("Em paralelo a resistência equivalente aumenta.", "Fica menor que a menor resistência."), ("O chuveiro na posição inverno tem resistência maior.", "Tem resistência menor, para mais potência.")],
          [("Para que serve o disjuntor?", "Desliga o circuito quando a corrente passa do limite, evitando incêndios."), ("Por que não ligar muitos aparelhos no mesmo benjamim?", "A corrente total esquenta os fios e pode causar incêndio.")],
          [("Grandezas", [("a corrente elétrica", "ampère"), ("a tensão elétrica", "volt"), ("a resistência elétrica", "ohm"), ("a potência", "watt"), ("a energia consumida na conta", "quilowatt-hora"),
                          ("a carga elétrica", "coulomb"), ("a resistividade", "ohm·metro"), ("a frequência da rede", "hertz")],
            "Qual é a unidade de {k}?", "Que grandeza se mede em {v}?"),
           ("Aparelhos", [("o chuveiro elétrico", "efeito Joule"), ("o ferro de passar", "efeito Joule"), ("o fusível", "efeito Joule"), ("a torradeira", "efeito Joule"),
                          ("o motor do ventilador", "força magnética sobre correntes"), ("o liquidificador", "força magnética sobre correntes"), ("a lâmpada LED", "emissão de luz por semicondutor"),
                          ("o painel solar", "efeito fotovoltaico")],
            "Em que efeito se baseia {k}?", None),
           ("Circuitos", {"as características da associação em série": ["mesma corrente em todos", "resistências se somam", "tensão se divide", "se um queimar, todos param", "resistência equivalente maior"],
                          "as características da associação em paralelo": ["mesma tensão em todos", "corrente se divide", "resistência equivalente menor", "usada nas casas", "cada aparelho funciona sozinho"],
                          "os dispositivos de segurança elétrica": ["o disjuntor", "o fusível", "o fio terra", "o DR (dispositivo diferencial residual)", "a tomada com três pinos"]})],
          ["U = R·i.", "Em série as resistências somam.", "Em paralelo a tensão é a mesma.", "P = U·i.", "O chuveiro usa o efeito Joule.", "A conta de luz cobra kWh.", "O disjuntor protege contra sobrecarga."],
          [("Em paralelo a resistência equivalente aumenta.", "Diminui."), ("Em série a tensão é a mesma em todos.", "A corrente é a mesma."), ("A conta cobra em watts.", "Cobra em kWh."),
           ("Fios mais finos têm menor resistência.", "Têm maior resistência."), ("O chuveiro na posição inverno tem resistência maior.", "Tem resistência menor.")],
          "a eletrodinâmica", "energy", calc=f_eletro),

        H("FI", "magnetismo-e-inducao", ["EM13CNT107"], "Magnetismo e indução eletromagnética", "Eletromagnetismo",
          "Realizar previsões qualitativas e quantitativas sobre o funcionamento de geradores, motores elétricos e seus componentes, bobinas, transformadores, pilhas, baterias e dispositivos eletrônicos, com base na análise dos processos de transformação e condução de energia envolvidos.",
          "ímãs, campo magnético, Oersted, força magnética, motores, lei de Faraday, lei de Lenz, geradores e transformadores",
          "Corrente gera campo; campo variável gera corrente", "Faraday: ε = ΔΦ/Δt. Transformador: U₂/U₁ = N₂/N₁.",
          ["Ímãs têm polos norte e sul que não se separam. Oersted mostrou que corrente elétrica cria campo magnético (eletroímã).",
           "Uma carga em movimento num campo sofre força F = q·v·B; um fio com corrente, F = B·i·L. Isso faz girar os motores elétricos.",
           "Faraday: variar o fluxo magnético induz corrente (ε = ΔΦ/Δt). Lenz: a corrente induzida se opõe à variação. Assim funcionam geradores e transformadores (só com corrente alternada)."],
          [("Um transformador tem 1.000 espiras no primário e 100 no secundário. Com 220 V na entrada, quanto sai?", ["U₂/U₁ = N₂/N₁.", "220·100 ÷ 1.000."], "22 V.")],
          [("Quebrando um ímã, separamos o polo norte do sul.", "Cada pedaço vira um ímã com dois polos."), ("O transformador funciona com pilha.", "Precisa de corrente alternada, que varia o fluxo.")],
          [("Como a bússola funciona?", "A agulha é um ímã que se alinha ao campo magnético da Terra."), ("O que gera a eletricidade numa hidrelétrica?", "Ímãs girando perto de bobinas induzem corrente (gerador).")],
          [("Cientistas e leis", [("Oersted", "corrente elétrica cria campo magnético"), ("Faraday", "variação do fluxo magnético induz corrente"), ("Lenz", "a corrente induzida se opõe à variação do fluxo"),
                                  ("Ampère", "relação entre correntes e campos magnéticos"), ("Maxwell", "unificou eletricidade, magnetismo e luz"), ("Tesla", "desenvolveu sistemas de corrente alternada")],
            "Qual contribuição está ligada a {k}?", "Quem mostrou ou desenvolveu: {v}?"),
           ("Aparelhos", [("o motor elétrico", "transforma energia elétrica em movimento"), ("o gerador", "transforma movimento em energia elétrica"), ("o transformador", "aumenta ou reduz a tensão alternada"),
                          ("o eletroímã", "ímã que funciona com corrente elétrica"), ("a bússola", "agulha imantada que aponta o norte magnético"), ("o alto-falante", "bobina e ímã fazem a membrana vibrar"),
                          ("o fogão de indução", "campo magnético variável aquece a panela"), ("o cartão por aproximação", "indução eletromagnética transmite dados")],
            "O que faz {k}?", D),
           ("Situações", {"o que induz corrente numa bobina": ["aproximar um ímã", "afastar um ímã", "girar a bobina perto de um ímã", "variar a corrente numa bobina vizinha", "girar um ímã dentro da bobina"],
                          "o que não induz corrente numa bobina": ["ímã parado dentro da bobina", "corrente contínua constante na bobina vizinha", "bobina parada sem campo", "ímã parado longe", "bobina e ímã movendo-se juntos"],
                          "os materiais atraídos por ímãs": ["o ferro", "o níquel", "o cobalto", "o aço", "a magnetita"]})],
          ["Corrente elétrica cria campo magnético.", "Variar o fluxo magnético induz corrente.", "O transformador precisa de corrente alternada.", "Ímãs têm sempre dois polos.",
           "F = B·i·L num fio perpendicular ao campo.", "O gerador transforma movimento em eletricidade.", "A corrente induzida se opõe à variação do fluxo."],
          [("Ímã parado dentro da bobina induz corrente.", "É preciso variar o fluxo."), ("O transformador funciona com pilha.", "Precisa de corrente alternada."),
           ("Quebrar um ímã separa os polos.", "Cada pedaço tem dois polos."), ("O ímã atrai o alumínio.", "Não atrai alumínio."), ("O motor transforma movimento em eletricidade.", "Isso é o gerador.")],
          "o eletromagnetismo", "energy", calc=f_mag),

        H("FI", "fisica-moderna", ["EM13CNT103", "EM13CNT209"], "Física moderna: relatividade e quântica", "Física moderna",
          "Utilizar o conhecimento sobre as radiações e suas origens para avaliar as potencialidades e os riscos de sua aplicação em equipamentos de uso cotidiano, na saúde, no ambiente, na indústria, na agricultura e na geração de energia elétrica; analisar a evolução estelar associando-a aos modelos de origem e distribuição dos elementos químicos no Universo.",
          "relatividade restrita, dilatação do tempo, E = m·c², quantização, fóton, efeito fotoelétrico, dualidade onda-partícula e modelo de Bohr",
          "A luz é onda e partícula", "Fóton: E = h·f. Einstein: E = m·c² e o tempo se dilata a altas velocidades.",
          ["Relatividade restrita: a velocidade da luz no vácuo é a mesma para todos os observadores. Perto dela o tempo se dilata (Δt = γ·Δt₀) e os comprimentos se contraem.",
           "Massa e energia se equivalem: E = m·c². É a base da energia das estrelas e das usinas nucleares.",
           "Planck e Einstein: a luz vem em pacotes (fótons) com energia E = h·f. No efeito fotoelétrico, Ec = h·f − φ. Bohr: o elétron só ocupa níveis de energia definidos."],
          [("Um fóton tem frequência 5 × 10¹⁴ Hz. Qual é sua energia (h = 6,6 × 10⁻³⁴ J·s)?", ["E = h·f.", "6,6 × 10⁻³⁴·5 × 10¹⁴."], "3,3 × 10⁻¹⁹ J.")],
          [("Luz mais intensa arranca elétrons de qualquer metal.", "Depende da frequência, não da intensidade."), ("A relatividade só vale no espaço.", "Vale sempre; os efeitos só são grandes perto da velocidade da luz.")],
          [("O GPS precisa da relatividade?", "Sim: os relógios dos satélites são corrigidos pelos efeitos da relatividade."), ("Por que as cores dos fogos de artifício são diferentes?", "Cada elemento emite fótons de energias próprias quando seus elétrons voltam de níveis excitados.")],
          [("Cientistas", [("Planck", "energia emitida em pacotes, os quanta"), ("Einstein", "explicou o efeito fotoelétrico e criou a relatividade"), ("Bohr", "níveis de energia do elétron no átomo"),
                           ("De Broglie", "partículas também se comportam como ondas"), ("Heisenberg", "princípio da incerteza"), ("Michelson e Morley", "experimento que não detectou o éter"),
                           ("Rutherford", "núcleo atômico pequeno e denso")],
            "Qual ideia está ligada a {k}?", "Quem propôs: {v}?"),
           ("Conceitos", [("o fóton", "pacote de energia da luz"), ("o efeito fotoelétrico", "emissão de elétrons por um metal iluminado"), ("a função trabalho", "energia mínima para arrancar o elétron do metal"),
                          ("a dilatação do tempo", "relógios em movimento rápido marcam menos tempo"), ("a contração do comprimento", "objetos rápidos ficam mais curtos na direção do movimento"),
                          ("a dualidade onda-partícula", "luz e matéria se comportam como onda e como partícula"), ("a constante de Planck", "6,6 × 10⁻³⁴ J·s"), ("o laser", "luz de uma só frequência, coerente e concentrada")],
            "O que é {k}?", D),
           ("Aplicações", {"as tecnologias que usam o efeito fotoelétrico": ["o painel solar", "o sensor da porta automática", "a câmera digital", "o fotômetro", "o sensor de luz do poste"],
                           "as tecnologias ligadas à relatividade": ["o GPS", "os aceleradores de partículas", "a energia nuclear", "o PET-scan", "os relógios atômicos em satélites"],
                           "as tecnologias quânticas do dia a dia": ["o laser", "o LED", "o transistor", "o micro-ondas com magnetron", "a ressonância magnética"]})],
          ["A velocidade da luz é a mesma para todos.", "E = h·f.", "E = m·c².", "O efeito fotoelétrico depende da frequência.", "O GPS corrige efeitos da relatividade.", "Bohr propôs níveis de energia.",
           "A luz tem comportamento de onda e de partícula."],
          [("Luz mais intensa sempre arranca elétrons.", "Depende da frequência."), ("A relatividade só vale no espaço.", "Vale sempre."), ("O fóton tem massa como uma bolinha.", "O fóton não tem massa de repouso."),
           ("Relógios rápidos marcam mais tempo.", "Marcam menos tempo."), ("E = m·c mostra a equivalência.", "A equação é E = m·c².")],
          "a física moderna", "waves-and-light", calc=f_mod),

        H("QU", "eletroquimica", ["EM13CNT107"], "Eletroquímica: pilhas e eletrólise", "Eletroquímica",
          "Realizar previsões qualitativas e quantitativas sobre o funcionamento de pilhas, baterias e processos de eletrólise, com base na análise dos processos de transformação e condução de energia envolvidos, e avaliar seus impactos ambientais.",
          "oxidação e redução, número de oxidação, pilha de Daniell, ânodo e cátodo, potenciais de redução, ddp, eletrólise e corrosão",
          "Oxida no ânodo, reduz no cátodo", "Pilha: química vira elétrica. Eletrólise: elétrica força a reação.",
          ["Oxidação é perda de elétrons; redução é ganho. Quem se oxida é o agente redutor; quem se reduz é o oxidante.",
           "Na pilha de Daniell o zinco (ânodo) se oxida e o cobre (cátodo) se reduz; os elétrons vão do ânodo ao cátodo. ddp = E(cátodo) − E(ânodo).",
           "Na eletrólise a corrente elétrica força uma reação não espontânea (produção de alumínio, cobre puro, galvanoplastia). Pilhas e baterias usadas devem ir para coleta especial."],
          [("Numa pilha de zinco e cobre, quem é o ânodo?", ["O zinco tem menor potencial de redução.", "Ele perde elétrons."], "O zinco.")],
          [("O ânodo é sempre positivo.", "Na pilha o ânodo é o polo negativo; na eletrólise é o positivo."), ("Oxidação é ganho de elétrons.", "Oxidação é perda de elétrons.")],
          [("Por que a galvanização protege o ferro?", "O zinco se oxida antes do ferro e o protege."), ("Por que não jogar pilhas no lixo comum?", "Têm metais pesados que contaminam solo e água.")],
          [("Conceitos", [("a oxidação", "perda de elétrons"), ("a redução", "ganho de elétrons"), ("o ânodo", "eletrodo onde ocorre a oxidação"), ("o cátodo", "eletrodo onde ocorre a redução"),
                          ("a ponte salina", "mantém a neutralidade elétrica das soluções da pilha"), ("o agente oxidante", "espécie que se reduz"), ("o agente redutor", "espécie que se oxida"),
                          ("a eletrólise", "reação química forçada pela corrente elétrica"), ("o metal de sacrifício", "metal que se oxida para proteger outro")],
            "O que é {k}?", D),
           ("Aplicações", [("a pilha alcalina", "transforma energia química em elétrica"), ("a bateria de lítio do celular", "pilha recarregável"), ("a galvanoplastia", "eletrólise para revestir objetos com metal"),
                           ("a produção de alumínio", "eletrólise da bauxita fundida"), ("o refino do cobre", "eletrólise para obter cobre puro"), ("os blocos de zinco no casco dos navios", "proteção do aço por metal de sacrifício"),
                           ("o bafômetro antigo", "reação redox que muda de cor com o álcool"), ("a ferrugem", "oxidação do ferro pelo oxigênio e pela água")],
            "O que é ou como funciona {k}?", D),
           ("Processos", {"os processos espontâneos": ["a pilha de Daniell funcionando", "a ferrugem se formando", "a pilha alcalina descarregando", "o zinco protegendo o ferro", "a prata escurecendo"],
                          "os processos que precisam de corrente externa": ["a eletrólise da água", "a produção de alumínio", "a galvanoplastia", "a recarga da bateria do celular", "o refino eletrolítico do cobre"],
                          "as formas de evitar a corrosão": ["pintar o ferro", "galvanizar com zinco", "usar metal de sacrifício", "aplicar óleo ou graxa", "usar aço inoxidável"]})],
          ["Oxidação é perda de elétrons.", "No cátodo ocorre redução.", "Na pilha os elétrons vão do ânodo ao cátodo.", "A eletrólise precisa de corrente externa.", "O zinco protege o ferro da corrosão.",
           "O alumínio é obtido por eletrólise.", "Pilhas usadas vão para coleta especial."],
          [("Oxidação é ganho de elétrons.", "É perda."), ("No ânodo ocorre redução.", "Ocorre oxidação."), ("A eletrólise é espontânea.", "Precisa de corrente externa."),
           ("O agente oxidante se oxida.", "Ele se reduz."), ("Pilhas podem ir no lixo comum.", "Vão para coleta especial.")],
          "a eletroquímica", "matter", calc=f_eq),

        H("QU", "quimica-organica", ["EM13CNT307"], "Química orgânica: cadeias e funções", "Química orgânica",
          "Analisar as propriedades dos materiais para avaliar a adequação de seu uso em diferentes aplicações (industriais, cotidianas, arquitetônicas ou tecnológicas), considerando os compostos orgânicos, suas cadeias e funções.",
          "carbono tetravalente, cadeias carbônicas, hidrocarbonetos, nomenclatura, funções oxigenadas e nitrogenadas, isomeria",
          "O carbono faz 4 ligações", "Cada função tem um grupo: álcool −OH, ácido −COOH, amina −NH₂.",
          ["O carbono faz 4 ligações e forma cadeias longas, abertas ou fechadas, com ligações simples, duplas ou triplas.",
           "Hidrocarbonetos têm só C e H: alcanos (simples, como o metano), alcenos (dupla, como o eteno), alcinos (tripla, como o etino). Prefixos: met (1 C), et (2), prop (3), but (4), pent (5).",
           "Funções: álcool (−OH, etanol), aldeído (−CHO, metanal), cetona (C=O no meio, propanona), ácido carboxílico (−COOH, ácido acético), éster (aromas de frutas), amina (−NH₂). Isômeros têm mesma fórmula molecular e estruturas diferentes."],
          [("Quantos carbonos tem o propano?", ["O prefixo prop indica 3 carbonos.", "O sufixo ano indica só ligações simples."], "3 carbonos.")],
          [("Todo composto com carbono é orgânico.", "CO₂ e carbonatos são estudados como inorgânicos."), ("Etanol e etano são a mesma substância.", "O etanol tem o grupo −OH; o etano é hidrocarboneto.")],
          [("De onde vem o cheiro de banana dos doces?", "De um éster, o acetato de isoamila."), ("O que é a acetona?", "A propanona, uma cetona usada como solvente.")],
          [("Funções", [("o etanol", "álcool"), ("o metanol", "álcool"), ("o ácido acético", "ácido carboxílico"), ("o ácido fórmico", "ácido carboxílico"), ("a propanona (acetona)", "cetona"),
                        ("o metanal (formol)", "aldeído"), ("o acetato de etila", "éster"), ("a metilamina", "amina"), ("o metano", "hidrocarboneto"), ("o eteno", "hidrocarboneto"),
                        ("o benzeno", "hidrocarboneto"), ("o fenol comum", "fenol")],
            "A que função orgânica pertence {k}?", None),
           ("Nomenclatura", [("o metano", "1 carbono, só ligações simples"), ("o etano", "2 carbonos, só ligações simples"), ("o propano", "3 carbonos, só ligações simples"),
                             ("o butano", "4 carbonos, só ligações simples"), ("o eteno", "2 carbonos com uma ligação dupla"), ("o propeno", "3 carbonos com uma ligação dupla"),
                             ("o etino", "2 carbonos com uma ligação tripla"), ("o pentano", "5 carbonos, só ligações simples")],
            "Como é a cadeia de {k}?", "Que composto tem {v}?"),
           ("Grupos", {"os grupos funcionais oxigenados": ["−OH do álcool", "−COOH do ácido carboxílico", "−CHO do aldeído", "C=O da cetona", "−COO− do éster"],
                       "os grupos funcionais nitrogenados": ["−NH₂ da amina", "−CONH₂ da amida", "−NO₂ do nitrocomposto", "−CN da nitrila", "a ligação peptídica"],
                       "os hidrocarbonetos": ["o metano", "o propano", "o eteno", "o acetileno", "o benzeno"]})],
          ["O carbono faz 4 ligações.", "O metano tem 1 carbono.", "O etanol é um álcool.", "O ácido acético é ácido carboxílico.", "Ésteres dão aroma às frutas.", "Alcenos têm ligação dupla.",
           "Isômeros têm a mesma fórmula molecular."],
          [("O carbono faz 2 ligações.", "Faz 4 ligações."), ("A acetona é um álcool.", "É uma cetona."), ("Alcanos têm ligação tripla.", "Alcanos têm só ligações simples."),
           ("Isômeros têm fórmulas moleculares diferentes.", "Têm a mesma fórmula molecular."), ("O propano tem 2 carbonos.", "Tem 3 carbonos.")],
          "a química orgânica", "matter"),

        H("QU", "reacoes-organicas-e-polimeros", ["EM13CNT309", "EM13CNT307"], "Reações orgânicas, polímeros e biocombustíveis", "Polímeros",
          "Analisar questões socioambientais, políticas e econômicas relativas à dependência do mundo atual em relação aos recursos não renováveis e discutir a necessidade de introdução de alternativas e novas tecnologias energéticas e de materiais, comparando diferentes tipos de motores e processos de produção de novos materiais.",
          "combustão, adição, substituição, esterificação, saponificação, polímeros de adição e condensação, plásticos, petróleo e biocombustíveis",
          "Monômeros se unem e formam polímeros", "Petróleo dá plásticos e combustíveis; etanol e biodiesel são renováveis.",
          ["Reações orgânicas: combustão (com O₂), adição (em duplas ligações), substituição, esterificação (ácido + álcool → éster + água) e saponificação (gordura + base → sabão).",
           "Polímeros são moléculas gigantes formadas por monômeros: polietileno (sacolas), PVC (canos), PET (garrafas), náilon. Naturais: amido, celulose, proteínas, borracha.",
           "O petróleo é separado por destilação fracionada (gás, gasolina, querosene, diesel). O etanol da cana e o biodiesel são biocombustíveis renováveis."],
          [("Como se faz sabão em casa?", ["Óleo ou gordura reage com soda cáustica.", "Essa reação é a saponificação."], "Pela saponificação de gordura com uma base.")],
          [("Todo plástico é igual.", "Cada polímero tem propriedades e símbolo de reciclagem próprios."), ("O biodiesel é fóssil.", "É feito de óleos vegetais ou gordura: é renovável.")],
          [("O que é polímero biodegradável?", "Plástico que microrganismos conseguem decompor, como o PLA de milho."), ("O que é craqueamento?", "Quebra de moléculas grandes do petróleo em menores, como as da gasolina.")],
          [("Polímeros", [("o polietileno", "sacolas e embalagens"), ("o PVC", "canos e tubos"), ("o PET", "garrafas de refrigerante"), ("o poliestireno expandido", "isopor"),
                          ("o náilon", "fios e tecidos"), ("o teflon", "revestimento antiaderente de panelas"), ("a borracha natural", "látex da seringueira"), ("o polipropileno", "para-choques e cadeiras de plástico")],
            "Para que se usa {k}?", "Que polímero é usado em {v}?"),
           ("Reações", [("ácido carboxílico + álcool → éster + água", "esterificação"), ("gordura + base forte → sabão + glicerol", "saponificação"), ("metano + oxigênio → gás carbônico + água", "combustão"),
                        ("eteno + hidrogênio → etano", "adição"), ("metano + cloro → clorometano + HCl", "substituição"), ("muitos etenos → polietileno", "polimerização por adição"),
                        ("glicose → etanol + gás carbônico", "fermentação"), ("óleo vegetal + metanol → biodiesel + glicerol", "transesterificação")],
            "Que tipo de reação é esta: {k}?", None),
           ("Origem", {"os produtos da destilação do petróleo": ["a gasolina", "o querosene", "o óleo diesel", "o gás de cozinha", "o asfalto"],
                       "os biocombustíveis": ["o etanol de cana", "o biodiesel", "o biogás", "o etanol de milho", "o bioquerosene"],
                       "os polímeros naturais": ["o amido", "a celulose", "as proteínas", "a borracha natural", "o DNA"]})],
          ["Polímeros são formados por monômeros.", "A saponificação produz sabão.", "Ácido + álcool forma éster.", "O PET é usado em garrafas.", "O etanol de cana é renovável.",
           "O petróleo é separado por destilação fracionada.", "A celulose é um polímero natural."],
          [("O biodiesel é fóssil.", "É renovável."), ("A esterificação produz sabão.", "Produz éster; o sabão vem da saponificação."), ("A celulose é polímero sintético.", "É natural."),
           ("O PVC é usado em garrafas de refrigerante.", "Essas garrafas são de PET."), ("Monômeros são moléculas gigantes.", "Os polímeros são as moléculas gigantes.")],
          "os polímeros e as reações orgânicas", "matter"),

        H("QU", "radioatividade", ["EM13CNT103"], "Radioatividade e energia nuclear", "Radioatividade",
          "Utilizar o conhecimento sobre as radiações e suas origens para avaliar as potencialidades e os riscos de sua aplicação em equipamentos de uso cotidiano, na saúde, no ambiente, na indústria, na agricultura e na geração de energia elétrica.",
          "emissões alfa, beta e gama, meia-vida, fissão, fusão, usinas nucleares, datação por carbono-14, acidente de Goiânia e usos na medicina",
          "Núcleos instáveis emitem radiação", "Alfa: Z − 2, A − 4. Beta: Z + 1. A cada meia-vida resta a metade.",
          ["Núcleos instáveis emitem radiação. Alfa (2 prótons e 2 nêutrons): Z diminui 2 e A diminui 4. Beta (elétron do núcleo): Z aumenta 1 e A não muda. Gama: onda eletromagnética, sem mudar Z nem A.",
           "Meia-vida é o tempo para metade dos núcleos decair. O carbono-14 (meia-vida de cerca de 5.730 anos) data fósseis e objetos antigos.",
           "Fissão divide núcleos pesados (usinas de Angra); fusão une núcleos leves (estrelas). Usos: radioterapia, radiografia, esterilização. Riscos: o acidente com césio-137 em Goiânia, em 1987."],
          [("Restam quanto de 80 g de um isótopo após 3 meias-vidas?", ["80 → 40 → 20 → 10.", "Divide-se por 2 três vezes."], "10 g.")],
          [("Radiação gama muda o número de massa.", "Gama não muda Z nem A."), ("Alimento irradiado fica radioativo.", "Ele não fica radioativo; a radiação só mata microrganismos.")],
          [("O que aconteceu em Goiânia em 1987?", "Uma cápsula de césio-137 de um aparelho de radioterapia abandonado foi aberta e contaminou muitas pessoas."), ("Como o Sol produz energia?", "Pela fusão de núcleos de hidrogênio em hélio.")],
          [("Emissões", [("a partícula alfa", "2 prótons e 2 nêutrons"), ("a partícula beta", "elétron emitido pelo núcleo"), ("a radiação gama", "onda eletromagnética de alta energia"),
                         ("a emissão alfa", "Z diminui 2 e A diminui 4"), ("a emissão beta", "Z aumenta 1 e A não muda"), ("a emissão gama", "não altera Z nem A"),
                         ("a radiação mais penetrante", "gama"), ("a radiação menos penetrante", "alfa")],
            "O que caracteriza {k}?", D),
           ("Usos", [("a radioterapia", "tratamento de tumores"), ("o carbono-14", "datação de fósseis e objetos"), ("o iodo-131", "diagnóstico e tratamento da tireoide"), ("o urânio-235", "combustível de usinas nucleares"),
                     ("o cobalto-60", "esterilização de materiais e alimentos"), ("a fissão nuclear", "energia de Angra 1 e 2"), ("a fusão nuclear", "energia do Sol"), ("o tecnécio-99m", "exames de cintilografia")],
            "Qual é a aplicação de {k}?", D),
           ("Classifique", {"os processos de fissão": ["a usina de Angra", "a bomba atômica de urânio", "o reator de submarino nuclear", "a quebra do urânio-235 por nêutrons", "o reator de pesquisa"],
                            "os processos de fusão": ["a energia do Sol", "a energia das estrelas", "a união de núcleos de hidrogênio", "a bomba de hidrogênio", "os reatores experimentais tipo tokamak"],
                            "as medidas de proteção contra radiação": ["aumentar a distância da fonte", "diminuir o tempo de exposição", "usar blindagem de chumbo", "usar dosímetro", "isolar o lixo radioativo"]})],
          ["Na emissão alfa, Z diminui 2.", "Na emissão beta, Z aumenta 1.", "A gama não muda Z nem A.", "A cada meia-vida resta a metade.", "O Sol produz energia por fusão.",
           "Angra usa fissão nuclear.", "O carbono-14 data fósseis."],
          [("Na emissão beta, A diminui 4.", "A não muda; Z aumenta 1."), ("Alimento irradiado fica radioativo.", "Não fica."), ("O Sol produz energia por fissão.", "Produz por fusão."),
           ("A radiação alfa é a mais penetrante.", "A gama é a mais penetrante."), ("Após 2 meias-vidas não resta nada.", "Resta 1/4.")],
          "a radioatividade", "matter", calc=f_radio),

        H("BI", "genetica", ["EM13CNT205", "EM13CNT202"], "Genética: leis de Mendel e heranças", "Genética",
          "Interpretar resultados e realizar previsões sobre atividades experimentais, fenômenos naturais e processos tecnológicos, com base nas noções de probabilidade e incerteza, reconhecendo os limites explicativos das ciências, aplicadas à transmissão de características hereditárias.",
          "1ª e 2ª leis de Mendel, probabilidade, heredogramas, grupos sanguíneos ABO e Rh, herança ligada ao sexo e codominância",
          "Cada característica: dois alelos", "1ª lei: Aa × Aa dá 3 : 1. 2ª lei: AaBb × AaBb dá 9 : 3 : 3 : 1.",
          ["1ª lei de Mendel: os alelos de um gene se separam na formação dos gametas. Aa × Aa dá 1 AA : 2 Aa : 1 aa (fenótipos 3 : 1).",
           "2ª lei: genes em cromossomos diferentes se segregam de forma independente: AaBb × AaBb dá 9 : 3 : 3 : 1. Probabilidades de eventos independentes se multiplicam.",
           "Grupos sanguíneos ABO têm alelos múltiplos (Iᴬ, Iᴮ codominantes e i recessivo). O daltonismo e a hemofilia são ligados ao cromossomo X, por isso são mais comuns em homens."],
          [("Um casal Aa × Aa quer ter um filho aa. Qual é a chance?", ["Gametas A e a de cada um.", "Só 1 das 4 combinações é aa."], "1/4.")],
          [("Se o primeiro filho é aa, o próximo não será.", "Cada filho é um evento independente: sempre 1/4."), ("Pais de sangue A não podem ter filho O.", "Se ambos forem Iᴬi, podem.")],
          [("Por que o daltonismo é mais comum em homens?", "Os homens têm um só cromossomo X; basta um alelo recessivo."), ("O que é um heredograma?", "Um diagrama da família que mostra como uma característica passa entre as gerações.")],
          [("Conceitos", [("o alelo", "forma alternativa de um gene"), ("o genótipo", "composição genética do indivíduo"), ("o fenótipo", "característica observável"), ("o homozigoto", "dois alelos iguais"),
                          ("o heterozigoto", "dois alelos diferentes"), ("a codominância", "os dois alelos se manifestam juntos"), ("a herança ligada ao sexo", "gene localizado no cromossomo X"),
                          ("o heredograma", "diagrama da herança numa família"), ("o locus gênico", "posição do gene no cromossomo")],
            "O que é {k}?", D),
           ("Sangue", [("o tipo A", "genótipos IᴬIᴬ ou Iᴬi"), ("o tipo B", "genótipos IᴮIᴮ ou Iᴮi"), ("o tipo AB", "genótipo IᴬIᴮ"), ("o tipo O", "genótipo ii"),
                       ("o doador universal", "tipo O negativo"), ("o receptor universal", "tipo AB positivo"), ("o fator Rh positivo", "presença do antígeno Rh"), ("a eritroblastose fetal", "mãe Rh− com filho Rh+")],
            "O que corresponde a {k}?", D),
           ("Heranças", {"as heranças ligadas ao cromossomo X": ["o daltonismo", "a hemofilia", "a distrofia muscular de Duchenne", "a deficiência de G6PD", "a síndrome do X frágil"],
                         "os exemplos de codominância": ["o tipo sanguíneo AB", "a pelagem ruão do gado", "o sistema MN de grupos sanguíneos", "a anemia falciforme no nível das hemácias", "as flores manchadas de camélia"],
                         "as leis e proporções de Mendel": ["3 : 1 no cruzamento Aa × Aa", "9 : 3 : 3 : 1 no diibridismo", "segregação dos alelos", "segregação independente", "1 : 1 no cruzamento Aa × aa"]})],
          ["Aa × Aa dá 3 : 1 nos fenótipos.", "AaBb × AaBb dá 9 : 3 : 3 : 1.", "Iᴬ e Iᴮ são codominantes.", "O tipo O tem genótipo ii.", "O daltonismo é ligado ao X.",
           "Cada filho é um evento independente.", "Os alelos se separam nos gametas."],
          [("Se o primeiro filho é aa, o segundo não pode ser.", "Cada filho é independente."), ("O tipo AB é recessivo.", "Iᴬ e Iᴮ são codominantes."), ("O daltonismo é mais comum em mulheres.", "É mais comum em homens."),
           ("Aa × Aa dá 1 : 1.", "Dá 3 : 1 nos fenótipos."), ("O tipo O é doador universal com qualquer Rh.", "O doador universal é O negativo.")],
          "a genética", "living-things-and-ecosystems", calc=f_gen, s4="Resolva os cruzamentos"),

        H("BI", "biotecnologia", ["EM13CNT304"], "Biotecnologia e ética", "Biotecnologia",
          "Analisar e debater situações controversas sobre a aplicação de conhecimentos da área de Ciências da Natureza (tais como tecnologias do DNA, tratamentos com células-tronco, neurotecnologias, produção de tecnologias de defesa, estratégias de controle de pragas, entre outros), com base em argumentos consistentes, legais, éticos e responsáveis, distinguindo diferentes pontos de vista.",
          "DNA recombinante, transgênicos, clonagem, células-tronco, PCR, testes de DNA, vacinas, CRISPR e bioética",
          "Tecnologias do DNA mudam a saúde e o campo", "Transgênico recebe gene de outra espécie; célula-tronco pode se diferenciar.",
          ["Engenharia genética: enzimas de restrição cortam o DNA e o gene de interesse é inserido em outro organismo (DNA recombinante). Assim bactérias produzem insulina humana.",
           "Transgênicos têm genes de outra espécie, como o milho resistente a insetos. Clones são cópias genéticas (ovelha Dolly). Células-tronco podem originar vários tipos de célula.",
           "PCR multiplica o DNA para testes de paternidade, perícias e diagnósticos. CRISPR edita genes com precisão. Essas técnicas exigem debate ético e regras (no Brasil, a CTNBio e a Lei de Biossegurança)."],
          [("Como se produz insulina humana em larga escala?", ["O gene da insulina humana é inserido em bactérias.", "As bactérias se multiplicam e fabricam a proteína."], "Com bactérias transgênicas (DNA recombinante).")],
          [("Clone é uma cópia com a mesma idade e memórias.", "É só uma cópia genética; nasce e cresce como qualquer indivíduo."), ("Todo transgênico é perigoso.", "Cada um é avaliado por órgãos técnicos.")],
          [("Para que serve a PCR?", "Multiplicar trechos de DNA para análise, como em testes de COVID-19 e de paternidade."), ("O que a Lei de Biossegurança regula?", "O uso de transgênicos e a pesquisa com células-tronco embrionárias no Brasil.")],
          [("Técnicas", [("a enzima de restrição", "corta o DNA em pontos específicos"), ("a DNA ligase", "une pedaços de DNA"), ("o plasmídeo", "DNA circular de bactérias usado como vetor"),
                         ("a PCR", "multiplica trechos de DNA"), ("a eletroforese", "separa fragmentos de DNA pelo tamanho"), ("o CRISPR-Cas9", "edita genes com precisão"),
                         ("a clonagem reprodutiva", "produz um indivíduo geneticamente idêntico"), ("a terapia gênica", "corrige ou substitui genes defeituosos")],
            "O que faz {k}?", D),
           ("Aplicações", [("a insulina humana", "produzida por bactérias transgênicas"), ("o milho Bt", "resistente a insetos"), ("a ovelha Dolly", "primeiro mamífero clonado de célula adulta"),
                           ("o teste de paternidade", "comparação de DNA"), ("a vacina de RNA mensageiro", "faz as células produzirem um antígeno"), ("o transplante de medula", "usa células-tronco do sangue"),
                           ("a perícia criminal", "identificação por DNA"), ("a soja tolerante a herbicida", "transgênico usado no campo")],
            "O que é {k}?", D),
           ("Temas", {"as aplicações médicas da biotecnologia": ["insulina recombinante", "vacinas de RNA", "terapia gênica", "células-tronco em transplantes", "testes genéticos"],
                      "as aplicações agrícolas da biotecnologia": ["milho Bt", "soja tolerante a herbicida", "feijão resistente a vírus", "plantas tolerantes à seca", "controle biológico de pragas"],
                      "as questões bioéticas": ["privacidade dos dados genéticos", "edição de embriões humanos", "uso de células-tronco embrionárias", "patentes de genes", "rotulagem de transgênicos"]})],
          ["Bactérias transgênicas produzem insulina humana.", "A PCR multiplica o DNA.", "Transgênicos recebem genes de outra espécie.", "Dolly foi clonada de célula adulta.",
           "Células-tronco podem originar vários tipos de célula.", "No Brasil a CTNBio avalia transgênicos.", "O CRISPR edita genes."],
          [("Clone tem as memórias do original.", "É só uma cópia genética."), ("A PCR destrói o DNA.", "Multiplica o DNA."), ("Transgênico é o mesmo que clone.", "Transgênico recebe gene de outra espécie."),
           ("Células-tronco só formam um tipo de célula.", "Podem originar vários tipos."), ("Enzimas de restrição unem o DNA.", "Elas cortam; quem une é a ligase.")],
          "a biotecnologia", "living-things-and-ecosystems"),

        H("BI", "evolucao-biologica", ["EM13CNT208", "EM13CNT201"], "Evolução biológica e origem da vida", "Evolução biológica",
          "Aplicar os princípios da evolução biológica para analisar a história humana, considerando sua origem, diversificação, dispersão pelo planeta e diferentes formas de interação com a natureza, valorizando e respeitando a diversidade étnica e cultural humana; analisar modelos sobre a origem da vida.",
          "origem da vida, Miller e Urey, Lamarck, Darwin, teoria sintética, especiação, evidências, evolução humana",
          "Mutação e recombinação geram variação", "A seleção natural age sobre a variação; o isolamento gera espécies novas.",
          ["Hipóteses sobre a origem da vida: a sopa primordial de Oparin e Haldane foi testada por Miller e Urey (1953), que produziram aminoácidos simulando a Terra primitiva. Pasteur refutou a geração espontânea.",
           "Lamarck propôs uso e desuso; Darwin e Wallace, a seleção natural. A teoria sintética une Darwin à genética: mutações e recombinação geram variação, e a seleção, a deriva e a migração mudam as populações.",
           "O isolamento geográfico e reprodutivo leva à especiação. Evidências: fósseis, órgãos homólogos e vestigiais, DNA e embriologia. Os humanos modernos surgiram na África há cerca de 300 mil anos."],
          [("Asas de morcego e braços humanos são homólogos ou análogos?", ["Têm os mesmos ossos.", "Vêm de um ancestral comum."], "Homólogos.")],
          [("A evolução tem um objetivo.", "Não há direção predefinida; há adaptação ao ambiente."), ("O homem descende do macaco atual.", "Humanos e macacos atuais têm ancestrais comuns.")],
          [("O que provou o experimento de Pasteur?", "Que microrganismos não surgem espontaneamente no caldo esterilizado."), ("O que é deriva genética?", "Mudança ao acaso das frequências de alelos, forte em populações pequenas.")],
          [("Conceitos", [("a abiogênese", "geração espontânea de vida a partir de matéria não viva"), ("a biogênese", "todo ser vivo vem de outro ser vivo"), ("a especiação", "formação de novas espécies"),
                          ("a deriva genética", "mudança ao acaso das frequências de alelos"), ("o órgão homólogo", "mesma origem embrionária, funções que podem diferir"), ("o órgão análogo", "mesma função, origens diferentes"),
                          ("o órgão vestigial", "órgão reduzido sem função importante, como o apêndice"), ("a irradiação adaptativa", "diversificação de um ancestral em muitas espécies"),
                          ("a convergência evolutiva", "espécies diferentes ficam parecidas por viverem em ambientes semelhantes")],
            "O que é {k}?", D),
           ("Cientistas", [("Pasteur", "refutou a geração espontânea com frascos de pescoço de cisne"), ("Miller e Urey", "produziram aminoácidos simulando a Terra primitiva"), ("Oparin", "propôs a sopa primordial"),
                           ("Lamarck", "lei do uso e desuso"), ("Darwin", "seleção natural e A origem das espécies"), ("Wallace", "propôs a seleção natural ao mesmo tempo que Darwin"),
                           ("Redi", "mostrou que larvas não surgem da carne podre se protegida de moscas"), ("Mendel", "leis da hereditariedade, base da teoria sintética")],
            "Qual contribuição está ligada a {k}?", "Quem: {v}?"),
           ("Órgãos", {"os pares de órgãos homólogos": ["braço humano e asa de morcego", "nadadeira de baleia e pata de cavalo", "asa de ave e braço humano", "pata de gato e nadadeira de golfinho", "folha e espinho do cacto"],
                       "os pares de órgãos análogos": ["asa de inseto e asa de ave", "nadadeira de peixe e nadadeira de golfinho", "olho de polvo e olho humano", "asa de borboleta e asa de morcego", "espinho de cacto e espinho de roseira"],
                       "os órgãos vestigiais humanos": ["o apêndice", "o cóccix", "os dentes do siso", "os músculos que movem as orelhas", "a prega semilunar do olho"]})],
          ["Pasteur refutou a geração espontânea.", "Miller e Urey produziram aminoácidos em laboratório.", "Mutações geram variação genética.", "O isolamento leva à especiação.",
           "Asa de morcego e braço humano são homólogos.", "Os humanos modernos surgiram na África.", "A deriva genética é forte em populações pequenas."],
          [("A evolução tem um objetivo final.", "Não tem direção predefinida."), ("O homem descende do macaco atual.", "Têm ancestrais comuns."), ("Asa de inseto e de ave são homólogas.", "São análogas."),
           ("Pasteur provou a geração espontânea.", "Ele a refutou."), ("Mutações nunca ocorrem.", "Ocorrem e geram variação.")],
          "a evolução biológica", "living-things-and-ecosystems"),
    ]
