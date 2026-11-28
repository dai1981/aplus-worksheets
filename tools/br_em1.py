# -*- coding: utf-8 -*-
"""Brasil / Ensino Médio 1ª série: Física, Química e Biologia (BNCC EM13CNT)"""
from br_sci import H, it, nq, num

D = "A que corresponde esta descrição: {v}?"


def f_cin(R):
    k = R.choice(["vm", "conv", "muv_v", "muv_s", "torr", "queda"])
    if k == "vm":
        d, t = R.choice([(240, 3), (150, 2), (360, 4), (90, 1.5), (420, 6), (100, 2.5)])
        return nq("Um ônibus percorre %s km em %s h. Qual é a velocidade média?" % (num(d), num(t)), d / t, [d * t, t / d, d - t, d / t / 3.6], "km/h",
                  "vm = Δs ÷ Δt = %s ÷ %s = %s km/h." % (num(d), num(t), num(d / t)))
    if k == "conv":
        v = R.choice([36, 72, 90, 108, 54, 18, 144])
        return nq("Quanto vale %d km/h em m/s?" % v, v / 3.6, [v * 3.6, v / 36, v / 60, v * 1000], "m/s", "Divida por 3,6: %d ÷ 3,6 = %s m/s." % (v, num(v / 3.6)))
    if k == "muv_v":
        v0, a, t = R.choice([(0, 2, 5), (10, 3, 4), (5, 2, 10), (0, 4, 6), (20, -2, 5), (12, -3, 4), (0, 5, 3)])
        v = v0 + a * t
        return nq("Um carro tem velocidade inicial %d m/s e aceleração %s m/s². Qual é a velocidade após %d s?" % (v0, num(a), t), v, [v0 + a, a * t * 2, v0 * t, v0 - a * t if v0 - a * t != v else v + 10], "m/s",
                  "v = v₀ + a·t = %d + (%s)·%d = %s m/s." % (v0, num(a), t, num(v)), neg=True)
    if k == "muv_s":
        a, t = R.choice([(2, 5), (4, 3), (2, 10), (6, 2), (3, 4), (1, 8)])
        return nq("Partindo do repouso com aceleração %d m/s², que distância um corpo percorre em %d s?" % (a, t), a * t * t / 2, [a * t * t, a * t, a * t / 2, a * t * t * 2], "m",
                  "s = a·t²/2 = %d·%d²/2 = %s m." % (a, t, num(a * t * t / 2)))
    if k == "torr":
        v0, a, d = R.choice([(0, 2, 25), (10, 2, 24), (0, 4, 50), (20, -4, 32), (0, 8, 16), (30, -5, 50)])
        v2 = v0 * v0 + 2 * a * d
        v = v2 ** 0.5
        return nq("Com velocidade inicial %d m/s e aceleração %s m/s², qual é a velocidade após percorrer %d m? (Torricelli)" % (v0, num(a), d), v, [v2, v0 + a * d, v / 2, v + v0 + 2], "m/s",
                  "v² = v₀² + 2·a·Δs = %d + 2·(%s)·%d = %s; v = %s m/s." % (v0 * v0, num(a), d, num(v2), num(v)))
    t = R.choice([1, 2, 3, 4, 5])
    return nq("Um objeto cai do repouso por %d s (despreze o ar e use g = 10 m/s²). Que altura ele percorre?" % t, 5 * t * t, [10 * t, 10 * t * t, 5 * t, 5 * t * t + 5], "m",
              "h = g·t²/2 = 10·%d²/2 = %d m." % (t, 5 * t * t))


def f_newton(R):
    k = R.choice(["f", "a", "m", "p", "atr", "res"])
    if k == "f":
        m, a = R.choice([(2, 3), (5, 2), (10, 1.5), (50, 2), (1200, 3), (0.5, 4), (80, 0.5)])
        return nq("Qual é a força resultante sobre um corpo de %s kg com aceleração %s m/s²?" % (num(m), num(a)), m * a, [m / a, a / m, m + a, m * a * 10], "N",
                  "F = m·a = %s·%s = %s N." % (num(m), num(a), num(m * a)))
    if k == "a":
        f, m = R.choice([(20, 4), (100, 25), (60, 12), (500, 250), (30, 6), (1500, 1000)])
        return nq("Uma força resultante de %s N age sobre %s kg. Qual é a aceleração?" % (num(f), num(m)), f / m, [f * m, m / f, f - m, f / m * 2], "m/s²",
                  "a = F ÷ m = %s ÷ %s = %s m/s²." % (num(f), num(m), num(f / m)))
    if k == "m":
        f, a = R.choice([(40, 2), (90, 3), (120, 4), (300, 5), (20, 0.5), (600, 1.5)])
        return nq("Uma força de %s N produz aceleração de %s m/s². Qual é a massa do corpo?" % (num(f), num(a)), f / a, [f * a, a / f, f - a, f / a / 2], "kg",
                  "m = F ÷ a = %s ÷ %s = %s kg." % (num(f), num(a), num(f / a)))
    if k == "p":
        m = R.choice([2, 5, 50, 60, 70, 0.5, 1000])
        return nq("Qual é o peso de um corpo de %s kg na Terra (g = 10 m/s²)?" % num(m), m * 10, [m, m / 10, m * 9.8 * 10, m * 100], "N", "P = m·g = %s·10 = %s N." % (num(m), num(m * 10)))
    if k == "atr":
        mu, m = R.choice([(0.2, 10), (0.3, 20), (0.5, 4), (0.1, 50), (0.4, 15), (0.25, 8)])
        return nq("Um bloco de %d kg está numa mesa horizontal com coeficiente de atrito %s. Qual é a força de atrito máxima (g = 10 m/s²)?" % (m, num(mu)), mu * m * 10,
                  [mu * m, m * 10, mu * 10, m * 10 / mu], "N", "Fat = μ·N = %s·%d·10 = %s N." % (num(mu), m, num(mu * m * 10)))
    f1, f2 = R.choice([(10, 4), (30, 12), (50, 20), (8, 3), (100, 45), (25, 10)])
    return nq("Duas forças de %d N e %d N agem num corpo, na mesma direção e em sentidos opostos. Qual é a resultante?" % (f1, f2), f1 - f2, [f1 + f2, f1 * f2, (f1 + f2) / 2, f2], "N",
              "Sentidos opostos: subtrai-se. %d − %d = %d N." % (f1, f2, f1 - f2))


def f_energ(R):
    k = R.choice(["ec", "ep", "cons", "trab", "pot", "mola"])
    if k == "ec":
        m, v = R.choice([(2, 3), (4, 5), (1000, 10), (60, 2), (0.5, 20), (80, 5), (10, 4)])
        return nq("Qual é a energia cinética de um corpo de %s kg a %d m/s?" % (num(m), v), m * v * v / 2, [m * v, m * v * v, m * v / 2, m * v * v / 4], "J",
                  "Ec = m·v²/2 = %s·%d²/2 = %s J." % (num(m), v, num(m * v * v / 2)))
    if k == "ep":
        m, h = R.choice([(2, 5), (10, 3), (50, 10), (0.5, 20), (70, 4), (5, 12)])
        return nq("Qual é a energia potencial gravitacional de %s kg a %d m de altura (g = 10 m/s²)?" % (num(m), h), m * 10 * h, [m * h, m * 10 * h / 2, m * 10 + h, m * h * 100], "J",
                  "Ep = m·g·h = %s·10·%d = %s J." % (num(m), h, num(m * 10 * h)))
    if k == "cons":
        h = R.choice([5, 20, 45, 80, 1.8, 3.2, 125])
        v = (20 * h) ** 0.5
        return nq("Um corpo cai do repouso de %s m de altura sem atrito (g = 10 m/s²). Com que velocidade chega ao chão?" % num(h), v, [20 * h, 10 * h, v * 2, h / 2], "m/s",
                  "m·g·h = m·v²/2, então v = √(2·g·h) = √%s = %s m/s." % (num(20 * h), num(v)))
    if k == "trab":
        f, d = R.choice([(50, 4), (20, 10), (100, 3), (250, 2), (15, 6), (80, 5)])
        return nq("Uma força de %d N desloca uma caixa %d m na mesma direção da força. Qual é o trabalho realizado?" % (f, d), f * d, [f / d, f + d, f * d / 2, f * d * 10], "J",
                  "τ = F·d = %d·%d = %d J." % (f, d, f * d))
    if k == "pot":
        t, s = R.choice([(600, 10), (1200, 60), (3000, 30), (900, 15), (500, 5), (2400, 40)])
        return nq("Um motor realiza %s J de trabalho em %d s. Qual é a potência?" % (num(t), s), t / s, [t * s, s / t, t - s, t / s / 60], "W",
                  "P = τ ÷ Δt = %s ÷ %d = %s W." % (num(t), s, num(t / s)))
    kk, x = R.choice([(200, 0.1), (100, 0.2), (500, 0.1), (400, 0.05), (1000, 0.02), (50, 0.4)])
    return nq("Uma mola de constante %s N/m é comprimida %s m. Qual é a energia potencial elástica?" % (num(kk), num(x)), kk * x * x / 2, [kk * x, kk * x * x, kk * x / 2, kk * x * x * 2], "J",
              "Ee = k·x²/2 = %s·%s²/2 = %s J." % (num(kk), num(x), num(kk * x * x / 2)))


def f_grav(R):
    k = R.choice(["peso", "dist", "massa", "kepler", "lua"])
    if k == "peso":
        p, g = R.choice([("na Lua", 1.6), ("em Marte", 3.7), ("em Júpiter", 25), ("em Vênus", 8.9), ("em Mercúrio", 3.7)])
        m = R.choice([10, 50, 60, 80, 100])
        return nq("Qual é o peso de um astronauta de %d kg %s, onde g ≈ %s m/s²?" % (m, p, num(g)), m * g, [m, m * 10, m / g, m * g * 10], "N",
                  "P = m·g = %d·%s = %s N. A massa continua %d kg." % (m, num(g), num(m * g), m))
    if k == "dist":
        n = R.choice([2, 3, 4, 5, 10])
        return it("Se a distância entre dois corpos for multiplicada por %d, a força gravitacional entre eles fica dividida por quanto?" % n, num(n * n), [num(n), num(2 * n), num(n ** 3)],
                  "F é inversamente proporcional a d²: dividida por %d² = %d." % (n, n * n))
    if k == "massa":
        n = R.choice([2, 3, 4, 5])
        return it("Se a massa de um dos corpos for multiplicada por %d, a força gravitacional fica multiplicada por quanto?" % n, str(n), [str(n * n), str(2 * n) if 2 * n != n * n else str(n + 3), "1"],
                  "F = G·m₁·m₂/d²: proporcional à massa, então fica %d vezes maior." % n)
    if k == "kepler":
        return it(R.choice(["Segundo Kepler, quando um planeta está mais perto do Sol, sua velocidade orbital…", "Pela segunda lei de Kepler, no periélio o planeta se move…"]),
                  "é maior", ["é menor", "é igual à do afélio", "é zero"], "A segunda lei diz que o raio vetor varre áreas iguais em tempos iguais: perto do Sol o planeta é mais rápido.")
    t = R.choice([1, 2, 3, 4])
    return nq("Na Lua (g ≈ 1,6 m/s²), um objeto cai do repouso por %d s. Que altura percorre?" % t, 0.8 * t * t, [1.6 * t, 5 * t * t, 1.6 * t * t, 0.8 * t], "m",
              "h = g·t²/2 = 1,6·%d²/2 = %s m." % (t, num(0.8 * t * t)))


MASS = [("H₂O", 18, "água"), ("CO₂", 44, "gás carbônico"), ("NaCl", 58.5, "cloreto de sódio"), ("O₂", 32, "gás oxigênio"), ("CH₄", 16, "metano"), ("NH₃", 17, "amônia"),
        ("C₆H₁₂O₆", 180, "glicose"), ("CaCO₃", 100, "carbonato de cálcio"), ("H₂SO₄", 98, "ácido sulfúrico"), ("NaOH", 40, "hidróxido de sódio")]


def f_esteq(R):
    k = R.choice(["mol", "massa", "molec", "agua", "co2", "mm"])
    f, mm, nm = R.choice(MASS)
    if k == "mol":
        n = R.choice([2, 3, 0.5, 4, 5, 0.25])
        return nq("Quantos mols há em %s g de %s (%s, M = %s g/mol)?" % (num(n * mm), nm, f, num(mm)), n, [n * mm, mm / (n * mm), n * 2, n + 1], "mol",
                  "n = m ÷ M = %s ÷ %s = %s mol." % (num(n * mm), num(mm), num(n)))
    if k == "massa":
        n = R.choice([2, 3, 0.5, 4, 10, 0.1])
        return nq("Qual é a massa de %s mol de %s (%s, M = %s g/mol)?" % (num(n), nm, f, num(mm)), n * mm, [mm / n, n + mm, mm, n * mm * 2], "g",
                  "m = n·M = %s·%s = %s g." % (num(n), num(mm), num(n * mm)))
    if k == "molec":
        n = R.choice([2, 0.5, 3, 0.1, 5])
        return nq("Quantas moléculas há em %s mol de %s? (Constante de Avogadro: 6,02 × 10²³)" % (num(n), nm), n * 6.02e23, [6.02e23, n * 6.02e22, 6.02e23 / n, n * 6.02e24], "",
                  "N = n·6,02 × 10²³ = %s moléculas." % num(n * 6.02e23))
    if k == "agua":
        n = R.choice([1, 2, 3, 4, 5])
        return nq("Na reação 2 H₂ + O₂ → 2 H₂O, quantos mols de água se formam com %d mol de O₂?" % n, 2 * n, [n, n / 2, 4 * n, 3 * n], "mol",
                  "A proporção O₂ : H₂O é 1 : 2. %d·2 = %d mol." % (n, 2 * n))
    if k == "co2":
        g = R.choice([16, 32, 8, 48, 4, 80])
        return nq("Na combustão CH₄ + 2 O₂ → CO₂ + 2 H₂O, que massa de CO₂ se forma com %d g de metano (CH₄ = 16 g/mol, CO₂ = 44 g/mol)?" % g, g / 16 * 44, [g, g / 16, g * 44, g / 44 * 16], "g",
                  "%d g ÷ 16 = %s mol de CH₄ → %s mol de CO₂ → %s × 44 = %s g." % (g, num(g / 16), num(g / 16), num(g / 16), num(g / 16 * 44)))
    return it("Qual é a massa molar de %s (%s)?" % (f, nm), num(mm) + " g/mol", [num(x) + " g/mol" for x in R.sample([m for _, m, _ in MASS if m != mm], 3)],
              "Somando as massas atômicas dos átomos de %s: %s g/mol." % (f, num(mm)))


def UNITS(grade):
    return [
        H("FI", "cinematica", ["EM13CNT204"], "Cinemática: movimento uniforme e variado", "Cinemática",
          "Elaborar explicações, previsões e cálculos a respeito dos movimentos de objetos na Terra, no Sistema Solar e no Universo com base na análise das interações gravitacionais, com ou sem o uso de dispositivos e aplicativos digitais.",
          "referencial, deslocamento, velocidade média, aceleração, MRU, MRUV, queda livre e gráficos",
          "v = Δs ÷ Δt e a = Δv ÷ Δt", "MRUV: v = v₀ + a·t, s = s₀ + v₀·t + a·t²/2, v² = v₀² + 2·a·Δs.",
          ["Movimento depende do referencial. Velocidade média é Δs ÷ Δt; para passar de km/h para m/s, divide-se por 3,6.",
           "No movimento uniforme (MRU) a velocidade é constante: s = s₀ + v·t. No uniformemente variado (MRUV) a aceleração é constante: v = v₀ + a·t e s = s₀ + v₀·t + a·t²/2.",
           "Sem o tempo, usa-se Torricelli: v² = v₀² + 2·a·Δs. Na queda livre a aceleração é g ≈ 10 m/s² (desprezando o ar)."],
          [("Um carro vai de 0 a 20 m/s em 5 s. Qual é a aceleração?", ["Δv = 20 − 0 = 20 m/s.", "a = 20 ÷ 5."], "4 m/s².")],
          [("Somar km/h com m/s.", "Converta antes: 1 m/s = 3,6 km/h."), ("Corpos pesados caem mais rápido no vácuo.", "Sem ar, todos caem com a mesma aceleração.")],
          [("O que mostra a inclinação do gráfico s × t?", "A velocidade."), ("O que mostra a área do gráfico v × t?", "O deslocamento.")],
          [("Grandezas", [("a velocidade média", "Δs ÷ Δt"), ("a aceleração média", "Δv ÷ Δt"), ("o deslocamento", "variação da posição"), ("o referencial", "corpo em relação ao qual se descreve o movimento"),
                          ("o MRU", "movimento com velocidade constante"), ("o MRUV", "movimento com aceleração constante"), ("a queda livre", "queda só sob a ação da gravidade"),
                          ("a trajetória", "caminho percorrido pelo corpo")],
            "O que é {k}?", D),
           ("Gráficos", [("reta inclinada no gráfico s × t", "MRU"), ("reta horizontal no gráfico v × t", "MRU"), ("parábola no gráfico s × t", "MRUV"),
                         ("reta inclinada no gráfico v × t", "MRUV"), ("reta horizontal no gráfico s × t", "repouso"), ("reta horizontal no eixo zero do gráfico v × t", "repouso"),
                         ("reta horizontal acima do zero no gráfico a × t", "MRUV"), ("reta sobre o eixo zero no gráfico a × t, com velocidade não nula", "MRU")],
            "Que movimento indica {k}?", None, ("movimento circular",)),
           ("Classifique", {"os exemplos de MRU": ["carro com o velocímetro parado em 80 km/h na reta", "esteira rolante com velocidade constante", "luz se propagando no vácuo", "avião em cruzeiro em linha reta", "som no ar parado"],
                            "os exemplos de MRUV": ["pedra em queda livre", "carro arrancando com aceleração constante", "bola subindo após ser lançada para cima", "trem freando de forma uniforme", "esfera descendo um plano inclinado sem atrito"],
                            "as unidades do SI": ["metro", "segundo", "metro por segundo", "metro por segundo ao quadrado", "quilograma"]})],
          ["Velocidade média é Δs ÷ Δt.", "Para converter km/h em m/s divide-se por 3,6.", "No MRU a velocidade é constante.", "No MRUV a aceleração é constante.",
           "Na queda livre a aceleração é g.", "A área do gráfico v × t dá o deslocamento.", "O movimento depende do referencial."],
          [("No MRU a aceleração é constante e diferente de zero.", "No MRU a aceleração é zero."), ("Para converter km/h em m/s multiplica-se por 3,6.", "Divide-se por 3,6."),
           ("No vácuo, corpos mais pesados caem mais rápido.", "Todos caem com a mesma aceleração."), ("O repouso não depende do referencial.", "Repouso e movimento dependem do referencial."),
           ("A inclinação do gráfico s × t dá a aceleração.", "Dá a velocidade.")],
          "a cinemática", "forces-and-motion", calc=f_cin),

        H("FI", "leis-de-newton", ["EM13CNT204"], "Leis de Newton e forças", "Leis de Newton",
          "Elaborar explicações, previsões e cálculos a respeito dos movimentos de objetos com base nas leis de Newton e nas interações entre os corpos.",
          "inércia, força resultante, F = m·a, ação e reação, peso, normal, atrito e tração",
          "F = m·a", "Inércia, princípio fundamental e ação e reação explicam os movimentos.",
          ["1ª lei (inércia): sem força resultante, um corpo mantém o repouso ou o MRU. Por isso usamos cinto de segurança.",
           "2ª lei: a força resultante é igual a massa vezes aceleração, F = m·a. O peso é P = m·g.",
           "3ª lei (ação e reação): toda força tem uma reação de mesma intensidade e sentido oposto, aplicada em outro corpo. O atrito é Fat = μ·N."],
          [("Por que o passageiro vai para a frente quando o ônibus freia?", ["O corpo tende a manter o movimento.", "É a inércia."], "Por inércia (1ª lei).")],
          [("Ação e reação se anulam.", "Agem em corpos diferentes, por isso não se anulam."), ("Sem força, o corpo para.", "Sem força resultante, ele mantém a velocidade.")],
          [("Massa e peso são a mesma coisa?", "Não: massa é em kg e não muda; peso é força, em N, e depende de g."), ("Como o foguete sobe no espaço?", "Expulsa gases para trás e recebe a reação para a frente.")],
          [("Leis", [("o cinto de segurança", "1ª lei, inércia"), ("o passageiro jogado para a frente na freada", "1ª lei, inércia"), ("um carrinho mais leve acelerando mais com a mesma força", "2ª lei, F = m·a"),
                     ("o chute que faz a bola acelerar", "2ª lei, F = m·a"), ("o remo empurrando a água para trás", "3ª lei, ação e reação"), ("o foguete expelindo gases", "3ª lei, ação e reação"),
                     ("o recuo da arma ao disparar", "3ª lei, ação e reação"), ("a toalha puxada rápido sob a louça", "1ª lei, inércia")],
            "Que lei de Newton explica {k}?", None),
           ("Forças", [("o peso", "força com que a Terra atrai o corpo"), ("a força normal", "força de apoio perpendicular à superfície"), ("o atrito", "força que se opõe ao deslizamento"),
                       ("a tração", "força transmitida por fios e cordas"), ("a força elástica", "força de uma mola deformada"), ("a força resultante", "soma vetorial de todas as forças"),
                       ("o newton", "unidade de força no SI"), ("a massa", "medida da inércia do corpo")],
            "O que é {k}?", D),
           ("Situações", {"as situações com força resultante nula": ["livro parado sobre a mesa", "paraquedista em velocidade constante", "carro em MRU numa reta", "lustre pendurado em repouso", "caixa empurrada em velocidade constante"],
                          "as situações com força resultante não nula": ["carro arrancando", "bola caindo em queda livre", "ônibus freando", "skate acelerando na descida", "elevador começando a subir"],
                          "os pares ação e reação": ["pé empurra o chão e o chão empurra o pé", "Terra atrai a maçã e a maçã atrai a Terra", "remo empurra a água e a água empurra o remo", "foguete empurra os gases e os gases empurram o foguete", "martelo bate no prego e o prego bate no martelo"]})],
          ["Sem força resultante, o corpo mantém sua velocidade.", "F = m·a.", "Ação e reação agem em corpos diferentes.", "O peso é P = m·g.", "O atrito se opõe ao deslizamento.",
           "O cinto de segurança protege contra a inércia.", "A massa não muda de planeta para planeta."],
          [("Ação e reação se anulam.", "Agem em corpos diferentes."), ("Sem força o corpo sempre para.", "Mantém o MRU."), ("Massa e peso são a mesma coisa.", "Massa é kg; peso é força em N."),
           ("Quanto maior a massa, maior a aceleração com a mesma força.", "A aceleração é menor."), ("O peso não depende da gravidade.", "P = m·g depende de g.")],
          "as leis de Newton", "forces-and-motion", calc=f_newton),

        H("FI", "energia-mecanica-e-trabalho", ["EM13CNT101"], "Trabalho, energia mecânica e potência", "Energia mecânica",
          "Analisar e representar, com ou sem o uso de dispositivos e de aplicativos digitais específicos, as transformações e conservações em sistemas que envolvam quantidade de matéria, de energia e de movimento para realizar previsões sobre seus comportamentos em situações cotidianas e em processos produtivos que priorizem o desenvolvimento sustentável, o uso consciente dos recursos naturais e a preservação da vida em todas as suas formas.",
          "trabalho, energia cinética, potencial gravitacional e elástica, conservação da energia mecânica, potência e rendimento",
          "Energia mecânica = cinética + potencial", "Sem atrito, a energia mecânica se conserva: Ec + Ep é constante.",
          ["Trabalho de uma força: τ = F·d (força na direção do deslocamento). Unidade: joule (J).",
           "Energia cinética: Ec = m·v²/2. Potencial gravitacional: Ep = m·g·h. Potencial elástica: Ee = k·x²/2.",
           "Sem atrito, a energia mecânica se conserva. Potência é energia por tempo: P = τ ÷ Δt, em watts. Rendimento = energia útil ÷ energia total."],
          [("Uma bola de 2 kg a 3 m/s tem quanta energia cinética?", ["Ec = m·v²/2.", "2·9/2 = 9."], "9 J.")],
          [("Dobrar a velocidade dobra a energia cinética.", "Ela fica quatro vezes maior (v²)."), ("Força sem deslocamento realiza trabalho.", "Sem deslocamento não há trabalho.")],
          [("Por que a montanha-russa não precisa de motor depois da primeira subida?", "A energia potencial do alto vira cinética e vice-versa."), ("O que é 1 cavalo-vapor?", "Cerca de 735 W.")],
          [("Fórmulas", [("a energia cinética", "m·v²/2"), ("a energia potencial gravitacional", "m·g·h"), ("a energia potencial elástica", "k·x²/2"), ("o trabalho de uma força constante", "F·d·cos θ"),
                         ("a potência média", "τ ÷ Δt"), ("o rendimento", "energia útil ÷ energia total"), ("o peso", "m·g"), ("a força elástica", "k·x")],
            "Qual é a expressão de {k}?", "Que grandeza se calcula por {v}?"),
           ("Transformações", [("a bola caindo do alto", "potencial em cinética"), ("o arco lançando a flecha", "elástica em cinética"), ("a bola subindo depois do chute para o alto", "cinética em potencial"),
                               ("a usina hidrelétrica", "potencial em elétrica"), ("o freio do carro", "cinética em térmica"), ("o atleta no salto com vara subindo", "cinética em potencial"),
                               ("o estilingue disparando", "elástica em cinética"), ("o carrinho da montanha-russa descendo", "potencial em cinética")],
            "Que transformação de energia ocorre em {k}?", None),
           ("Unidades", {"as unidades de energia": ["joule", "quilowatt-hora", "caloria", "quilocaloria", "elétron-volt"], "as unidades de potência": ["watt", "quilowatt", "cavalo-vapor", "horsepower", "megawatt"],
                         "as unidades de força": ["newton", "quilograma-força", "dina", "quilonewton", "meganewton"]})],
          ["Ec = m·v²/2.", "Ep = m·g·h.", "Sem atrito a energia mecânica se conserva.", "Potência é trabalho por tempo.", "O joule é unidade de energia.", "O watt é unidade de potência.",
           "Sem deslocamento não há trabalho."],
          [("Dobrar a velocidade dobra a energia cinética.", "Quadruplica."), ("O watt é unidade de energia.", "É unidade de potência."), ("A energia mecânica sempre se conserva, mesmo com atrito.", "Com atrito parte vira calor."),
           ("Segurar um peso parado realiza muito trabalho.", "Sem deslocamento o trabalho é zero."), ("Ep não depende da altura.", "Ep = m·g·h depende da altura.")],
          "a energia mecânica", "energy", calc=f_energ),

        H("FI", "gravitacao", ["EM13CNT204", "EM13CNT201"], "Gravitação universal e leis de Kepler", "Gravitação",
          "Analisar e discutir modelos, teorias e leis propostos em diferentes épocas e culturas para comparar distintas explicações sobre o surgimento e a evolução da Vida, da Terra e do Universo com as teorias científicas aceitas atualmente; elaborar previsões e cálculos sobre movimentos no Sistema Solar com base nas interações gravitacionais.",
          "modelos geocêntrico e heliocêntrico, leis de Kepler, lei da gravitação universal, peso em outros astros, satélites e marés",
          "F = G·M·m ÷ d²", "A força diminui com o quadrado da distância; planetas mais perto do Sol andam mais rápido.",
          ["Ptolomeu propôs o modelo geocêntrico; Copérnico, o heliocêntrico. Kepler mostrou que as órbitas são elipses com o Sol em um dos focos (1ª lei).",
           "2ª lei: o raio que liga o planeta ao Sol varre áreas iguais em tempos iguais, então o planeta é mais rápido perto do Sol. 3ª lei: T² é proporcional a R³.",
           "Newton: F = G·M·m/d². A força dobra se uma massa dobra e cai a 1/4 se a distância dobra. O peso varia de astro para astro; a massa não."],
          [("Se a distância entre a Terra e um satélite dobrar, o que acontece com a força?", ["F é proporcional a 1/d².", "(1/2)² = 1/4."], "Fica quatro vezes menor.")],
          [("No espaço não há gravidade.", "Os astronautas em órbita estão em queda livre contínua."), ("A órbita da Terra é um círculo perfeito.", "É uma elipse quase circular.")],
          [("Por que há marés?", "A atração da Lua e do Sol é diferente nos lados da Terra, deformando os oceanos."), ("Quem formulou a gravitação universal?", "Isaac Newton, em 1687.")],
          [("Cientistas", [("Ptolomeu", "modelo geocêntrico"), ("Copérnico", "modelo heliocêntrico"), ("Galileu", "observou as luas de Júpiter com luneta"), ("Kepler", "órbitas elípticas dos planetas"),
                           ("Newton", "lei da gravitação universal"), ("Tycho Brahe", "medições precisas das posições dos planetas"), ("Cavendish", "mediu a constante gravitacional G em laboratório")],
            "A que contribuição está ligado {k}?", "Quem está ligado a: {v}?"),
           ("Conceitos", [("a 1ª lei de Kepler", "as órbitas são elipses com o Sol em um foco"), ("a 2ª lei de Kepler", "áreas iguais em tempos iguais"), ("a 3ª lei de Kepler", "T² proporcional a R³"),
                          ("o periélio", "ponto da órbita mais próximo do Sol"), ("o afélio", "ponto da órbita mais distante do Sol"), ("a constante G", "constante da gravitação universal"),
                          ("o satélite geoestacionário", "gira junto com a Terra e parece parado no céu"), ("a imponderabilidade", "sensação de flutuar em queda livre na órbita")],
            "O que diz ou o que é {k}?", D),
           ("Variação", {"o que aumenta a força gravitacional": ["aumentar uma das massas", "diminuir a distância", "aumentar as duas massas", "aproximar os corpos", "dobrar a massa do planeta"],
                         "o que diminui a força gravitacional": ["aumentar a distância", "diminuir uma das massas", "afastar os corpos", "levar o corpo para longe do planeta", "dividir a massa do planeta"],
                         "o que não muda de um planeta para outro": ["a massa do corpo", "a quantidade de matéria", "a inércia do corpo", "o número de átomos do corpo", "o volume de um corpo rígido"]})],
          ["As órbitas dos planetas são elipses.", "No periélio o planeta é mais rápido.", "F = G·M·m/d².", "Dobrar a distância divide a força por quatro.", "O peso muda de astro para astro.",
           "A massa não muda de planeta para planeta.", "Copérnico propôs o modelo heliocêntrico."],
          [("No espaço não há gravidade.", "Os astronautas estão em queda livre."), ("Dobrar a distância divide a força por dois.", "Divide por quatro."), ("A massa muda na Lua.", "Muda o peso; a massa é a mesma."),
           ("Kepler propôs órbitas circulares perfeitas.", "Propôs órbitas elípticas."), ("No afélio o planeta é mais rápido.", "É mais lento.")],
          "a gravitação", "earth-and-space", calc=f_grav),

        H("QU", "modelos-atomicos-e-tabela-periodica", ["EM13CNT201"], "Modelos atômicos e tabela periódica", "Tabela periódica",
          "Analisar e discutir modelos, teorias e leis propostos em diferentes épocas e culturas para comparar distintas explicações sobre a constituição da matéria e compreender a organização dos elementos na tabela periódica.",
          "modelos atômicos, número atômico, isótopos, distribuição eletrônica, famílias, períodos, metais e propriedades periódicas",
          "A tabela segue o número atômico", "Período = camadas; família = elétrons de valência (nos representativos).",
          ["A tabela periódica organiza os elementos por número atômico crescente. As linhas são períodos (número de camadas) e as colunas, grupos ou famílias.",
           "Elementos do mesmo grupo têm propriedades parecidas: grupo 1 (metais alcalinos), 2 (alcalino-terrosos), 17 (halogênios), 18 (gases nobres).",
           "O raio atômico aumenta para baixo e para a esquerda; a eletronegatividade e a energia de ionização aumentam para cima e para a direita (o flúor é o mais eletronegativo)."],
          [("Em que período fica o sódio (Z = 11, camadas 2-8-1)?", ["Ele tem 3 camadas.", "O período é o número de camadas."], "No 3º período.")],
          [("Elementos do mesmo período têm propriedades iguais.", "Quem tem propriedades parecidas é o mesmo grupo."), ("Isótopos têm números de prótons diferentes.", "Têm o mesmo Z e nêutrons diferentes.")],
          [("Quem organizou a primeira tabela periódica?", "Dmitri Mendeleiev, em 1869."), ("Por que os gases nobres quase não reagem?", "Têm a camada de valência completa.")],
          [("Grupos", [("o sódio", "metais alcalinos"), ("o potássio", "metais alcalinos"), ("o cálcio", "metais alcalino-terrosos"), ("o magnésio", "metais alcalino-terrosos"),
                       ("o cloro", "halogênios"), ("o flúor", "halogênios"), ("o neônio", "gases nobres"), ("o argônio", "gases nobres"), ("o oxigênio", "calcogênios"), ("o enxofre", "calcogênios"),
                       ("o ferro", "metais de transição"), ("o cobre", "metais de transição")],
            "A que família pertence {k}?", None),
           ("Conceitos", [("o número atômico", "número de prótons do núcleo"), ("o período", "linha horizontal da tabela"), ("o grupo", "coluna vertical da tabela"),
                          ("os isótopos", "átomos com mesmo Z e massas diferentes"), ("a eletronegatividade", "tendência de atrair elétrons numa ligação"),
                          ("a energia de ionização", "energia para retirar um elétron do átomo"), ("o raio atômico", "tamanho do átomo"), ("a camada de valência", "a camada eletrônica mais externa")],
            "O que é {k}?", D),
           ("Propriedades", {"as características dos metais": ["bons condutores de eletricidade", "brilho metálico", "maleabilidade", "tendência a perder elétrons", "sólidos à temperatura ambiente, exceto o mercúrio"],
                             "as características dos não metais": ["maus condutores em geral", "tendência a ganhar elétrons", "alta eletronegatividade", "muitos são gases à temperatura ambiente", "formam ânions"],
                             "as características dos gases nobres": ["camada de valência completa", "baixíssima reatividade", "existem como átomos isolados", "usados em letreiros luminosos", "ficam no grupo 18"]})],
          ["A tabela é ordenada pelo número atômico.", "Período indica o número de camadas.", "O flúor é o elemento mais eletronegativo.", "Os gases nobres ficam no grupo 18.",
           "Isótopos têm o mesmo número de prótons.", "O raio atômico aumenta para baixo no grupo.", "Mendeleiev organizou a primeira tabela periódica."],
          [("A tabela é ordenada pela massa atômica.", "Hoje é ordenada pelo número atômico."), ("Isótopos têm números de prótons diferentes.", "Têm o mesmo Z."),
           ("O césio é mais eletronegativo que o flúor.", "O flúor é o mais eletronegativo."), ("O cloro é um gás nobre.", "É um halogênio."), ("Os metais tendem a ganhar elétrons.", "Tendem a perder.")],
          "a tabela periódica", "matter"),

        H("QU", "ligacoes-quimicas", ["EM13CNT307"], "Ligações químicas", "Ligações químicas",
          "Analisar as propriedades dos materiais para avaliar a adequação de seu uso em diferentes aplicações (industriais, cotidianas, arquitetônicas ou tecnológicas) e/ou propor soluções seguras e sustentáveis considerando seu contexto local e cotidiano.",
          "regra do octeto, ligação iônica, covalente e metálica, polaridade, forças intermoleculares e propriedades das substâncias",
          "Átomos se ligam para ficar estáveis", "Iônica: metal + não metal. Covalente: não metais. Metálica: metais.",
          ["Pela regra do octeto, muitos átomos ficam estáveis com 8 elétrons na camada de valência (como os gases nobres).",
           "Ligação iônica: um metal cede elétrons a um não metal, formando íons (NaCl). Ligação covalente: não metais compartilham elétrons (H₂O, CO₂). Ligação metálica: elétrons livres entre cátions de metal.",
           "Compostos iônicos têm alto ponto de fusão e conduzem eletricidade dissolvidos ou fundidos. As forças intermoleculares (como as ligações de hidrogênio na água) explicam pontos de ebulição."],
          [("Que tipo de ligação há no NaCl?", ["Na é metal e Cl é não metal.", "O sódio cede um elétron ao cloro."], "Iônica.")],
          [("O sal sólido conduz eletricidade.", "Só conduz fundido ou dissolvido, quando os íons ficam livres."), ("Toda molécula com ligações polares é polar.", "O CO₂ tem ligações polares, mas é apolar pela geometria.")],
          [("Por que os metais conduzem eletricidade?", "Porque têm elétrons livres, o mar de elétrons."), ("Por que a água tem ponto de ebulição alto?", "Pelas ligações de hidrogênio entre as moléculas.")],
          [("Tipo de ligação", [("o NaCl", "iônica"), ("o KBr", "iônica"), ("o CaO", "iônica"), ("o MgCl₂", "iônica"), ("a H₂O", "covalente"), ("o CO₂", "covalente"), ("o CH₄", "covalente"),
                                ("o NH₃", "covalente"), ("o O₂", "covalente"), ("o ferro metálico", "metálica"), ("o cobre do fio", "metálica"), ("o alumínio da lata", "metálica")],
            "Que tipo de ligação existe em {k}?", None, ("nuclear",)),
           ("Conceitos", [("a regra do octeto", "átomos tendem a ficar com 8 elétrons na valência"), ("o cátion", "íon positivo, que perdeu elétrons"), ("o ânion", "íon negativo, que ganhou elétrons"),
                          ("a ligação de hidrogênio", "atração forte entre H e F, O ou N de outra molécula"), ("a molécula polar", "molécula com distribuição desigual de cargas"),
                          ("a molécula apolar", "molécula com cargas distribuídas por igual"), ("o mar de elétrons", "elétrons livres da ligação metálica"), ("a ligação covalente", "compartilhamento de pares de elétrons")],
            "O que é {k}?", D),
           ("Propriedades", {"as propriedades dos compostos iônicos": ["alto ponto de fusão", "sólidos cristalinos à temperatura ambiente", "conduzem eletricidade quando dissolvidos em água", "quebradiços", "muitos se dissolvem em água"],
                             "as propriedades das substâncias metálicas": ["brilho metálico", "conduzem eletricidade no estado sólido", "maleáveis", "dúcteis", "bons condutores de calor"],
                             "as substâncias apolares": ["o gás oxigênio", "o metano", "o gás carbônico", "o óleo de cozinha", "a gasolina"]})],
          ["O NaCl tem ligação iônica.", "A água tem ligações covalentes.", "Metais têm elétrons livres.", "O cátion é um íon positivo.", "O CO₂ é apolar.",
           "Compostos iônicos dissolvidos conduzem eletricidade.", "A água forma ligações de hidrogênio."],
          [("O sal sólido conduz bem eletricidade.", "Só conduz fundido ou dissolvido."), ("A água tem ligação iônica.", "Tem ligações covalentes."), ("O ânion é um íon positivo.", "É negativo."),
           ("O CO₂ é polar.", "É apolar pela geometria linear."), ("Metais não conduzem eletricidade no estado sólido.", "Conduzem pelo mar de elétrons.")],
          "as ligações químicas", "matter"),

        H("QU", "funcoes-inorganicas", ["EM13CNT307"], "Funções inorgânicas: ácidos, bases, sais e óxidos", "Funções inorgânicas",
          "Analisar as propriedades dos materiais para avaliar a adequação de seu uso em diferentes aplicações, considerando ácidos, bases, sais e óxidos e o pH de materiais do cotidiano.",
          "ácidos de Arrhenius, bases, sais, óxidos, neutralização, pH e indicadores",
          "Ácido libera H⁺; base libera OH⁻", "pH abaixo de 7 é ácido, 7 é neutro, acima de 7 é básico.",
          ["Ácidos, em água, liberam H⁺ (HCl, H₂SO₄, ácido acético do vinagre). Bases liberam OH⁻ (NaOH, Mg(OH)₂ do leite de magnésia).",
           "Ácido + base → sal + água: é a neutralização (HCl + NaOH → NaCl + H₂O). Óxidos são compostos de oxigênio com outro elemento (CO₂, CaO).",
           "A escala de pH vai de 0 a 14: abaixo de 7 é ácido, 7 é neutro, acima de 7 é básico. Indicadores como a fenolftaleína e o repolho roxo mudam de cor."],
          [("O leite de magnésia é ácido ou básico?", ["Contém Mg(OH)₂.", "Libera OH⁻ e neutraliza a acidez do estômago."], "Básico.")],
          [("Todo ácido é perigoso.", "O suco de limão e o vinagre são ácidos fracos do dia a dia."), ("pH 3 é mais básico que pH 5.", "Quanto menor o pH, mais ácido.")],
          [("O que causa a chuva ácida?", "Óxidos de enxofre e de nitrogênio que reagem com a água do ar."), ("Para que se usa cal no solo?", "Para corrigir a acidez (calagem).")],
          [("Função", [("o HCl", "ácido"), ("o H₂SO₄", "ácido"), ("o HNO₃", "ácido"), ("o ácido acético do vinagre", "ácido"), ("o NaOH", "base"), ("o KOH", "base"), ("o Ca(OH)₂", "base"),
                       ("o Mg(OH)₂", "base"), ("o NaCl", "sal"), ("o CaCO₃", "sal"), ("o NaHCO₃", "sal"), ("o CO₂", "óxido"), ("o CaO", "óxido"), ("o SO₂", "óxido")],
            "A que função inorgânica pertence {k}?", None, ("hidrocarboneto",)),
           ("pH", [("o suco gástrico", "pH cerca de 1 a 2"), ("o suco de limão", "pH cerca de 2"), ("o vinagre", "pH cerca de 3"), ("a água pura a 25 °C", "pH 7"),
                   ("o sangue", "pH cerca de 7,4"), ("a água do mar", "pH cerca de 8"), ("o leite de magnésia", "pH cerca de 10"), ("a água sanitária", "pH cerca de 12")],
            "Qual é o pH aproximado de {k}?", None),
           ("Ácido ou básico", {"os materiais ácidos": ["o vinagre", "o suco de limão", "o refrigerante de cola", "o suco gástrico", "a chuva ácida"],
                                "os materiais básicos": ["o sabão", "o leite de magnésia", "a água sanitária", "o bicarbonato de sódio dissolvido", "a cal dissolvida em água"],
                                "os óxidos": ["o gás carbônico", "a cal viva", "o dióxido de enxofre", "a ferrugem", "o monóxido de carbono"]})],
          ["Ácidos liberam H⁺ em água.", "Bases liberam OH⁻ em água.", "Ácido + base forma sal + água.", "pH 7 é neutro.", "O vinagre é ácido.", "O leite de magnésia é básico.",
           "Óxidos de enxofre causam chuva ácida."],
          [("pH 2 é básico.", "pH 2 é ácido."), ("Bases liberam H⁺.", "Liberam OH⁻."), ("O NaCl é uma base.", "É um sal."), ("A água pura tem pH 1.", "Tem pH 7 a 25 °C."),
           ("A neutralização forma óxido e gás.", "Forma sal e água.")],
          "as funções inorgânicas", "matter"),

        H("QU", "estequiometria", ["EM13CNT101"], "Mol e estequiometria", "Estequiometria",
          "Analisar e representar as transformações e conservações em sistemas que envolvam quantidade de matéria, de energia e de movimento para realizar previsões sobre seus comportamentos em situações cotidianas e em processos produtivos.",
          "massa atômica, massa molar, mol, constante de Avogadro, balanceamento e cálculos estequiométricos",
          "1 mol = 6,02 × 10²³ partículas", "n = m ÷ M. Os coeficientes da equação dão a proporção em mols.",
          ["O mol é a unidade de quantidade de matéria: 1 mol tem 6,02 × 10²³ partículas (constante de Avogadro).",
           "A massa molar M (em g/mol) é a soma das massas atômicas: H₂O = 2·1 + 16 = 18 g/mol. Número de mols: n = m ÷ M.",
           "Numa equação balanceada, os coeficientes indicam a proporção em mols: em 2 H₂ + O₂ → 2 H₂O, 2 mol de H₂ reagem com 1 mol de O₂ e formam 2 mol de água."],
          [("Quantos mols há em 36 g de água?", ["M(H₂O) = 18 g/mol.", "n = 36 ÷ 18."], "2 mol.")],
          [("Os coeficientes indicam a proporção em massa.", "Indicam a proporção em mols."), ("Um mol de qualquer substância tem a mesma massa.", "Tem o mesmo número de partículas, não a mesma massa.")],
          [("O que é reagente limitante?", "O reagente que acaba primeiro e limita a quantidade de produto."), ("Por que balancear a equação?", "Para respeitar a conservação dos átomos e da massa.")],
          [("Conceitos", [("o mol", "quantidade com 6,02 × 10²³ partículas"), ("a massa molar", "massa de 1 mol da substância, em g/mol"), ("a constante de Avogadro", "6,02 × 10²³ por mol"),
                          ("o reagente limitante", "reagente que acaba primeiro"), ("o reagente em excesso", "reagente que sobra no fim"), ("o rendimento da reação", "porcentagem do produto obtido em relação ao esperado"),
                          ("o coeficiente estequiométrico", "número que indica a proporção em mols"), ("a equação balanceada", "equação com o mesmo número de átomos de cada lado")],
            "O que é {k}?", D),
           ("Massa molar", [("a água (H₂O)", "18 g/mol"), ("o gás carbônico (CO₂)", "44 g/mol"), ("o metano (CH₄)", "16 g/mol"), ("o gás oxigênio (O₂)", "32 g/mol"),
                            ("a glicose (C₆H₁₂O₆)", "180 g/mol"), ("o carbonato de cálcio (CaCO₃)", "100 g/mol"), ("o hidróxido de sódio (NaOH)", "40 g/mol"), ("a amônia (NH₃)", "17 g/mol")],
            "Qual é a massa molar de {k}?", "Qual substância tem massa molar de {v}?"),
           ("Balanceamento", {"as equações balanceadas": ["2 H₂ + O₂ → 2 H₂O", "CH₄ + 2 O₂ → CO₂ + 2 H₂O", "N₂ + 3 H₂ → 2 NH₃", "C + O₂ → CO₂", "2 Na + Cl₂ → 2 NaCl", "4 Fe + 3 O₂ → 2 Fe₂O₃", "CaCO₃ → CaO + CO₂"],
                              "as equações não balanceadas": ["H₂ + O₂ → H₂O", "CH₄ + O₂ → CO₂ + H₂O", "N₂ + H₂ → NH₃", "Na + Cl₂ → NaCl", "Fe + O₂ → Fe₂O₃", "Al + O₂ → Al₂O₃", "H₂O₂ → H₂O + O₂"]})],
          ["1 mol tem 6,02 × 10²³ partículas.", "A massa molar da água é 18 g/mol.", "n = m ÷ M.", "Os coeficientes indicam a proporção em mols.", "O reagente limitante acaba primeiro.",
           "A equação balanceada conserva os átomos.", "2 mol de H₂ reagem com 1 mol de O₂."],
          [("Os coeficientes indicam a proporção em massa.", "Indicam a proporção em mols."), ("1 mol de qualquer substância tem 18 g.", "A massa depende da massa molar."),
           ("O reagente em excesso acaba primeiro.", "Quem acaba primeiro é o limitante."), ("A massa molar do CO₂ é 28 g/mol.", "É 44 g/mol."), ("Um mol tem 6,02 × 10²³ gramas.", "Tem 6,02 × 10²³ partículas.")],
          "a estequiometria", "matter", calc=f_esteq),

        H("BI", "bioquimica-celular", ["EM13CNT202"], "Bioquímica: as moléculas da vida", "Bioquímica",
          "Analisar as diversas formas de manifestação da vida em seus diferentes níveis de organização, bem como as condições ambientais favoráveis e os fatores limitantes a elas, começando pelas substâncias que compõem os seres vivos.",
          "água, sais minerais, carboidratos, lipídios, proteínas, enzimas, vitaminas e ácidos nucleicos",
          "Carboidratos, lipídios, proteínas e ácidos nucleicos", "Enzimas são proteínas que aceleram as reações das células.",
          ["A água é a substância mais abundante nas células e participa de quase todas as reações. Sais minerais como cálcio e ferro têm funções específicas.",
           "Carboidratos (glicose, amido, celulose) fornecem energia e estrutura. Lipídios (gorduras, óleos, colesterol) reservam energia e formam membranas.",
           "Proteínas são formadas por aminoácidos e têm muitas funções; as enzimas são proteínas que aceleram reações. Os ácidos nucleicos (DNA e RNA) guardam e expressam a informação genética."],
          [("Que tipo de molécula é o amido?", ["É formado por muitas glicoses.", "É a reserva de energia das plantas."], "Um carboidrato (polissacarídeo).")],
          [("Enzimas são consumidas na reação.", "Elas são reutilizadas."), ("Todo lipídio faz mal.", "Lipídios formam membranas e hormônios e guardam energia.")],
          [("Por que a febre muito alta é perigosa?", "Pode desnaturar proteínas, inclusive enzimas."), ("Qual a diferença entre DNA e RNA?", "O DNA tem desoxirribose e timina; o RNA tem ribose e uracila.")],
          [("Classifique", [("a glicose", "carboidrato"), ("o amido", "carboidrato"), ("a celulose", "carboidrato"), ("o glicogênio", "carboidrato"), ("o colesterol", "lipídio"),
                            ("o óleo de soja", "lipídio"), ("a cera de abelha", "lipídio"), ("a hemoglobina", "proteína"), ("a insulina", "proteína"), ("a queratina", "proteína"),
                            ("a amilase", "proteína"), ("o DNA", "ácido nucleico"), ("o RNA", "ácido nucleico")],
            "A que grupo de moléculas pertence {k}?", None, ("sal mineral",), True, "{k}: {v}".replace("{k}", "Classificação de {k}")),
           ("Funções", [("a celulose", "forma a parede celular das plantas"), ("o glicogênio", "reserva de energia nos animais"), ("o amido", "reserva de energia nas plantas"),
                        ("a hemoglobina", "transporta oxigênio no sangue"), ("as enzimas", "aceleram as reações químicas"), ("os fosfolipídios", "formam as membranas celulares"),
                        ("o DNA", "guarda a informação genética"), ("o ferro", "faz parte da hemoglobina"), ("o cálcio", "forma ossos e dentes"), ("a vitamina C", "previne o escorbuto")],
            "Qual é a função de {k}?", D),
           ("Componentes", {"os monômeros e suas moléculas": ["aminoácidos formam proteínas", "glicoses formam amido", "nucleotídeos formam DNA", "ácidos graxos e glicerol formam triglicerídeos", "glicoses formam celulose"],
                            "as vitaminas e suas carências": ["falta de vitamina A causa cegueira noturna", "falta de vitamina C causa escorbuto", "falta de vitamina D causa raquitismo", "falta de vitamina B12 causa anemia", "falta de vitamina K prejudica a coagulação"],
                            "os fatores que desnaturam proteínas": ["temperatura muito alta", "pH muito ácido", "pH muito básico", "álcool concentrado", "metais pesados"]})],
          ["Enzimas são proteínas.", "O amido é um carboidrato.", "A hemoglobina transporta oxigênio.", "Os fosfolipídios formam as membranas.", "O DNA guarda a informação genética.",
           "A água é a substância mais abundante nas células.", "Proteínas são formadas por aminoácidos."],
          [("Enzimas são consumidas nas reações.", "São reutilizadas."), ("O amido é uma proteína.", "É um carboidrato."), ("O RNA tem timina.", "O RNA tem uracila."),
           ("A celulose é reserva dos animais.", "Nos animais a reserva é o glicogênio."), ("Proteínas são formadas por glicoses.", "São formadas por aminoácidos.")],
          "a bioquímica", "living-things-and-ecosystems"),

        H("BI", "citologia", ["EM13CNT202"], "Citologia: membrana, organelas e divisão celular", "Citologia",
          "Analisar as diversas formas de manifestação da vida em seus diferentes níveis de organização, bem como as condições ambientais favoráveis e os fatores limitantes a elas, com ou sem o uso de dispositivos e aplicativos digitais.",
          "teoria celular, membrana plasmática, transporte, organelas, núcleo, mitose e meiose",
          "A célula é a unidade da vida", "Mitose forma 2 células iguais; meiose forma 4 células com metade dos cromossomos.",
          ["Teoria celular: todos os seres vivos são formados por células, e toda célula vem de outra célula.",
           "A membrana plasmática é semipermeável. Difusão e osmose são transportes passivos; a bomba de sódio e potássio é transporte ativo, com gasto de ATP.",
           "Organelas: mitocôndria (respiração), cloroplasto (fotossíntese), ribossomo (proteínas), retículo e complexo golgiense (síntese e secreção), lisossomo (digestão). Mitose gera 2 células iguais; meiose gera 4 gametas haploides."],
          [("Uma célula com 46 cromossomos faz meiose. Quantos cromossomos tem cada célula final?", ["A meiose reduz o número à metade.", "46 ÷ 2 = 23."], "23 cromossomos.")],
          [("Osmose é passagem do soluto.", "Na osmose passa a água, do meio menos concentrado para o mais concentrado."), ("A mitose forma gametas.", "Os gametas vêm da meiose.")],
          [("O que acontece com uma hemácia em água pura?", "Recebe água por osmose, incha e pode estourar."), ("Por que as células musculares têm muitas mitocôndrias?", "Porque gastam muita energia.")],
          [("Organelas", [("a mitocôndria", "respiração celular e produção de ATP"), ("o cloroplasto", "fotossíntese"), ("o ribossomo", "síntese de proteínas"), ("o lisossomo", "digestão intracelular"),
                          ("o complexo golgiense", "armazena e secreta substâncias"), ("o retículo endoplasmático rugoso", "produz proteínas com ribossomos aderidos"),
                          ("o retículo endoplasmático liso", "produz lipídios"), ("o núcleo", "contém o DNA e controla a célula"), ("o centríolo", "participa da divisão celular em células animais")],
            "Qual é a função de {k}?", D),
           ("Transporte", [("a difusão simples", "passagem de soluto a favor do gradiente, sem gasto de energia"), ("a osmose", "passagem de água pela membrana semipermeável"),
                           ("a difusão facilitada", "passagem a favor do gradiente com ajuda de proteínas"), ("o transporte ativo", "passagem contra o gradiente com gasto de ATP"),
                           ("a fagocitose", "englobamento de partículas sólidas"), ("a pinocitose", "englobamento de gotículas de líquido"), ("a bomba de sódio e potássio", "exemplo de transporte ativo"),
                           ("a exocitose", "eliminação de substâncias em vesículas")],
            "O que é {k}?", D),
           ("Divisão", {"as características da mitose": ["forma 2 células-filhas", "mantém o número de cromossomos", "promove crescimento e regeneração", "ocorre em células do corpo", "células-filhas iguais à mãe"],
                        "as características da meiose": ["forma 4 células-filhas", "reduz o número de cromossomos à metade", "forma gametas", "tem duas divisões seguidas", "permite permutação entre cromossomos"],
                        "as estruturas exclusivas da célula vegetal": ["a parede de celulose", "o cloroplasto", "o vacúolo central grande", "os plasmodesmos", "o amiloplasto"]})],
          ["Toda célula vem de outra célula.", "A mitocôndria faz a respiração celular.", "Na osmose passa a água.", "O transporte ativo gasta ATP.", "A mitose forma 2 células iguais.",
           "A meiose forma gametas.", "O ribossomo produz proteínas."],
          [("Na osmose passa o soluto.", "Passa a água."), ("A mitose forma gametas.", "A meiose forma gametas."), ("O transporte ativo não gasta energia.", "Gasta ATP."),
           ("O lisossomo faz fotossíntese.", "O lisossomo faz digestão intracelular."), ("A meiose mantém o número de cromossomos.", "Reduz à metade.")],
          "a citologia", "living-things-and-ecosystems"),

        H("BI", "ecologia", ["EM13CNT203", "EM13CNT206"], "Ecologia: energia, ciclos e populações", "Ecologia",
          "Avaliar e prever efeitos de intervenções nos ecossistemas, e seus impactos nos seres vivos e no corpo humano, com base nos mecanismos de manutenção da vida, nos ciclos da matéria e nas transformações e transferências de energia; discutir a importância da preservação e conservação da biodiversidade.",
          "níveis tróficos, fluxo de energia, pirâmides, ciclos do carbono e do nitrogênio, relações ecológicas e sucessão",
          "A energia flui; a matéria circula", "Só cerca de 10% da energia passa de um nível trófico para o seguinte.",
          ["A energia entra pela fotossíntese e flui em um só sentido pelos níveis tróficos; em cada nível cerca de 90% se perde como calor.",
           "A matéria circula: no ciclo do carbono, a fotossíntese retira CO₂ e a respiração e a combustão o devolvem. No ciclo do nitrogênio, bactérias fixam o N₂ do ar.",
           "Relações ecológicas podem ser harmônicas (mutualismo, comensalismo) ou desarmônicas (predação, parasitismo, competição)."],
          [("Se os produtores têm 10.000 kJ, quanto chega aproximadamente aos consumidores secundários?", ["Passa cerca de 10% por nível.", "10.000 → 1.000 → 100."], "Cerca de 100 kJ.")],
          [("A energia é reciclada no ecossistema.", "A matéria é reciclada; a energia flui e se perde como calor."), ("Todo fungo é parasita.", "Muitos são decompositores ou formam mutualismos.")],
          [("O que é bioacumulação?", "O acúmulo de poluentes, como o mercúrio, que aumenta nos níveis tróficos mais altos."), ("O que é sucessão ecológica?", "A mudança gradual das comunidades até um estado mais estável, como no reflorestamento natural.")],
          [("Relações", [("a abelha e a flor", "mutualismo"), ("o líquen (alga e fungo)", "mutualismo"), ("as bactérias do intestino humano", "mutualismo"), ("a rêmora e o tubarão", "comensalismo"),
                         ("a bromélia sobre a árvore", "inquilinismo"), ("a onça e a capivara", "predação"), ("o carrapato e o boi", "parasitismo"), ("o cipó-chumbo na planta", "parasitismo"),
                         ("duas espécies de árvores disputando luz", "competição"), ("as formigas de um formigueiro", "sociedade")],
            "Que relação ecológica existe entre {k}?", None),
           ("Ciclos", [("a fotossíntese", "retira CO₂ da atmosfera"), ("a respiração", "devolve CO₂ à atmosfera"), ("a combustão de fósseis", "libera carbono guardado há milhões de anos"),
                       ("a fixação do nitrogênio", "bactérias transformam N₂ em compostos usados pelas plantas"), ("a desnitrificação", "bactérias devolvem N₂ à atmosfera"),
                       ("as leguminosas", "abrigam bactérias fixadoras de nitrogênio nas raízes"), ("a decomposição", "devolve nutrientes ao solo"), ("a transpiração das plantas", "devolve vapor de água à atmosfera")],
            "Qual é o papel de {k} nos ciclos da matéria?", D),
           ("Conceitos", {"os níveis tróficos": ["produtor", "consumidor primário", "consumidor secundário", "consumidor terciário", "decompositor"],
                          "as relações desarmônicas": ["predação", "parasitismo", "competição", "amensalismo", "canibalismo"],
                          "as relações harmônicas": ["mutualismo", "comensalismo", "inquilinismo", "protocooperação", "sociedade"]})],
          ["A energia flui num só sentido.", "A matéria é reciclada.", "Cerca de 10% da energia passa para o nível seguinte.", "A abelha e a flor têm mutualismo.", "Bactérias fixam o nitrogênio do ar.",
           "A fotossíntese retira CO₂ do ar.", "O carrapato é parasita."],
          [("A energia é reciclada no ecossistema.", "A energia flui e se perde como calor."), ("Os consumidores fixam o N₂ do ar.", "Quem fixa são bactérias."), ("A predação é uma relação harmônica.", "É desarmônica."),
           ("Toda a energia passa para o nível seguinte.", "Só cerca de 10%."), ("A respiração retira CO₂ do ar.", "A respiração libera CO₂.")],
          "a ecologia", "living-things-and-ecosystems"),
    ]
