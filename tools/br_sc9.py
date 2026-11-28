# -*- coding: utf-8 -*-
"""Brasil / Ciências: 9º ano (BNCC EF09CI01–EF09CI17)"""
from br_sci import H, it, nq, num

D = "A que corresponde esta descrição: {v}?"

ATOMS = [("hidrogênio", "H", 1, 1), ("hélio", "He", 2, 4), ("carbono", "C", 6, 12), ("nitrogênio", "N", 7, 14), ("oxigênio", "O", 8, 16), ("sódio", "Na", 11, 23),
         ("magnésio", "Mg", 12, 24), ("alumínio", "Al", 13, 27), ("enxofre", "S", 16, 32), ("cloro", "Cl", 17, 35), ("potássio", "K", 19, 39), ("cálcio", "Ca", 20, 40),
         ("ferro", "Fe", 26, 56), ("cobre", "Cu", 29, 64), ("zinco", "Zn", 30, 65), ("neônio", "Ne", 10, 20)]


def f_massa(R):
    k = R.choice(["prod", "reag", "aberto", "carvao"])
    if k == "prod":
        a, b = R.choice([(4, 32), (12, 32), (56, 32), (2, 16), (24, 16), (27, 24), (10, 40), (6, 48)])
        return nq("Numa reação em sistema fechado, %d g de um reagente reagem com %d g de outro. Qual é a massa total dos produtos?" % (a, b), a + b, [abs(b - a), a * b, b, a + b + 10], "g",
                  "Lei de Lavoisier: a massa se conserva. %d + %d = %d g." % (a, b, a + b))
    if k == "reag":
        t, a = R.choice([(44, 12), (18, 2), (80, 48), (36, 4), (100, 56), (58, 23)])
        return nq("Num recipiente fechado, um reagente de %d g e outro reagente formaram %d g de produto. Qual era a massa do segundo reagente?" % (a, t), t - a, [t + a, t, a, (t - a) * 2], "g",
                  "%d − %d = %d g." % (t, a, t - a))
    if k == "aberto":
        m, g = R.choice([(100, 2), (50, 3), (200, 4), (80, 1), (150, 5)])
        return nq("Num copo aberto, %d g de vinagre com bicarbonato liberaram %d g de gás para o ar. Quanto a balança marca no fim?" % (m, g), m - g, [m, m + g, g, m - 2 * g], "g",
                  "O gás escapou do sistema aberto: %d − %d = %d g. Num sistema fechado a massa seria a mesma." % (m, g, m - g))
    c, o = R.choice([(12, 32), (24, 64), (6, 16), (36, 96), (3, 8)])
    return nq("%d g de carbono queimam completamente com %d g de oxigênio, formando gás carbônico. Quanto gás carbônico se forma?" % (c, o), c + o, [o - c, c, o, c * o], "g",
              "Conservação da massa: %d + %d = %d g." % (c, o, c + o))


def f_atomo(R):
    n, s, z, a = R.choice(ATOMS)
    k = R.choice(["p", "n", "e", "a", "ion"])
    if k == "p":
        return nq("O átomo de %s (%s) tem número atômico %d. Quantos prótons ele tem?" % (n, s, z), z, [a, a - z, z + 1, 2 * z], "",
                  "O número atômico Z é o número de prótons: %d." % z)
    if k == "n":
        return nq("O %s (%s) tem Z = %d e número de massa A = %d. Quantos nêutrons ele tem?" % (n, s, z, a), a - z, [a, z, a + z, a - z + 1], "",
                  "Nêutrons = A − Z = %d − %d = %d." % (a, z, a - z))
    if k == "e":
        return nq("Um átomo neutro de %s tem %d prótons. Quantos elétrons ele tem?" % (n, z), z, [a, a - z, z * 2, z + 2], "",
                  "No átomo neutro, elétrons = prótons = %d." % z)
    if k == "a":
        return nq("Um átomo de %s tem %d prótons e %d nêutrons. Qual é o seu número de massa?" % (n, z, a - z), a, [a - z, z, a - 2 * z if a - 2 * z > 0 else a + 1, a + z], "",
                  "A = prótons + nêutrons = %d + %d = %d." % (z, a - z, a))
    if s in ("Na", "K"):
        return nq("O íon %s⁺ vem do átomo de %s (Z = %d), que perdeu 1 elétron. Quantos elétrons tem o íon?" % (s, n, z), z - 1, [z, z + 1, a - z, z - 2], "",
                  "Perdeu 1 elétron: %d − 1 = %d." % (z, z - 1))
    if s in ("Cl",):
        return nq("O íon Cl⁻ vem do átomo de cloro (Z = 17), que ganhou 1 elétron. Quantos elétrons tem o íon?", 18, [17, 16, 35, 19], "", "Ganhou 1 elétron: 17 + 1 = 18.")
    return nq("Quantos prótons tem o núcleo de um átomo de %s (Z = %d, A = %d)?" % (n, z, a), z, [a, a - z, a + z, z + 2], "", "Os prótons são dados por Z = %d." % z)


def f_onda(R):
    k = R.choice(["v", "f", "l", "luz"])
    if k == "v":
        l, f = R.choice([(2, 170), (0.5, 680), (1.7, 200), (0.85, 400), (3.4, 100), (0.34, 1000)])
        return nq("Uma onda sonora tem comprimento de onda %s m e frequência %s Hz. Qual é a sua velocidade?" % (num(l), num(f)), l * f, [l / f, f / l, l + f, l * f / 10], "m/s",
                  "v = λ × f = %s × %s = %s m/s." % (num(l), num(f), num(l * f)))
    if k == "f":
        v, l = R.choice([(340, 2), (340, 0.5), (340, 1.7), (1500, 3), (340, 0.34), (1500, 1.5)])
        return nq("Uma onda viaja a %s m/s com comprimento de onda %s m. Qual é a frequência?" % (num(v), num(l)), v / l, [v * l, l / v, v - l, v / l / 2], "Hz",
                  "f = v ÷ λ = %s ÷ %s = %s Hz." % (num(v), num(l), num(v / l)))
    if k == "l":
        v, f = R.choice([(340, 170), (340, 680), (340, 85), (1500, 750), (340, 34), (1500, 300)])
        return nq("Um som de %s Hz se propaga a %s m/s. Qual é o comprimento de onda?" % (num(f), num(v)), v / f, [v * f, f / v, v - f, v / f * 2], "m",
                  "λ = v ÷ f = %s ÷ %s = %s m." % (num(v), num(f), num(v / f)))
    t = R.choice([1, 2, 5, 8, 10, 3])
    return nq("A luz viaja a cerca de 300.000 km/s. Que distância ela percorre em %d s?" % t, 300000 * t, [300000 / t, 300 * t, 3000000 * t, 300000 + t], "km",
              "300.000 × %d = %s km." % (t, num(300000 * t)))


def f_gen(R):
    k = R.choice(["Aa", "AAaa", "aa", "rec", "num", "num", "dom", "het", "AAAa"])
    if k == "dom":
        return it("Cruzando Aa com Aa, qual é a chance de um filho mostrar a característica dominante?", "3/4 (75%)", ["1/4 (25%)", "1/2 (50%)", "100%"],
                  "AA, Aa e Aa mostram o dominante: 3 em 4.")
    if k == "het":
        return it("Cruzando Aa com Aa, qual é a chance de um filho ser heterozigoto (Aa)?", "1/2 (50%)", ["1/4 (25%)", "3/4 (75%)", "100%"], "Aa aparece em 2 das 4 combinações.")
    if k == "AAAa":
        return it("Cruzando AA com Aa, qual é a chance de nascer um filho aa?", "0%", ["1/4 (25%)", "1/2 (50%)", "100%"], "O genitor AA só passa A: nenhum filho será aa.")
    if k == "Aa":
        return it("Cruzando dois indivíduos Aa (heterozigotos), qual é a chance de nascer um filho aa?", "1/4 (25%)", ["1/2 (50%)", "3/4 (75%)", "0%"],
                  "Os filhos podem ser AA, Aa, Aa ou aa: 1 em 4 é aa.")
    if k == "AAaa":
        return it("Cruzando AA com aa, qual é a proporção dos filhos?", "100% Aa", ["50% AA e 50% aa", "25% AA, 50% Aa e 25% aa", "100% aa"],
                  "Todos recebem A de um genitor e a do outro: todos são Aa.")
    if k == "aa":
        return it("Cruzando Aa com aa, qual é a chance de um filho ser aa?", "1/2 (50%)", ["1/4 (25%)", "3/4 (75%)", "100%"], "Os filhos podem ser Aa ou aa, metade de cada.")
    if k == "rec":
        c = R.choice([("olhos azuis", "olhos castanhos"), ("sementes rugosas", "sementes lisas"), ("flor branca", "flor roxa"), ("pelo curto", "pelo longo")])
        if c[0] == "pelo curto":
            c = ("pelo longo", "pelo curto")
        return it("Num caso simplificado em que %s é recessivo e %s é dominante, dois genitores heterozigotos (Aa) podem ter um filho com %s?" % (c[0], c[1], c[0]),
                  "Sim, com chance de 1/4", ["Não, nunca", "Sim, sempre", "Sim, com chance de 3/4"], "Aa × Aa dá 1/4 de aa, que mostra a característica recessiva.")
    n = R.choice([4, 8, 12, 16, 20, 24, 32, 40, 48, 60, 80, 100])
    return nq("Num cruzamento Aa × Aa nasceram %d filhotes. Quantos se espera que sejam aa?" % n, n / 4, [n / 2, 3 * n / 4, n, n / 4 + 1], "",
              "Espera-se 1/4: %d ÷ 4 = %s." % (n, num(n / 4)))


def f_astro(R):
    k = R.choice(["ual", "luz", "ano", "dist"])
    if k == "ual":
        p, d = R.choice([("Marte", 1.5), ("Júpiter", 5.2), ("Saturno", 9.5), ("Vênus", 0.7), ("Mercúrio", 0.4), ("Netuno", 30), ("Urano", 19), ("o cinturão de asteroides", 2.7)])
        return nq("Uma unidade astronômica (UA) vale cerca de 150 milhões de km. %s está a cerca de %s UA do Sol. Quantos milhões de km são?" % (p, num(d)), 150 * d,
                  [150 / d, 150 + d, d, 1500 * d], "milhões de km", "150 × %s = %s milhões de km." % (num(d), num(150 * d)))
    if k == "luz":
        return it("A luz do Sol leva cerca de quanto tempo para chegar à Terra?", "8 minutos", ["8 segundos", "8 horas", "8 dias"], "A Terra está a cerca de 150 milhões de km; a luz leva uns 8 minutos.")
    if k == "ano":
        d = R.choice([4, 8, 9, 10, 25, 100, 310, 640])
        return nq("Uma estrela está a %d anos-luz da Terra. Há quantos anos saiu a luz que vemos hoje?" % d, d, [d * 365, d / 2, d * 12, d + 365], "anos",
                  "Ano-luz é a distância que a luz percorre em um ano: a luz saiu há %d anos." % d)
    t = R.choice([2, 3, 4, 6])
    return nq("Uma nave viaja 1 milhão de km por dia. Quantos dias levaria para percorrer a distância Terra–Lua %d vezes, se essa distância é de cerca de 384 mil km?" % t,
              0.384 * t, [384 * t, t, 3.84 * t, 0.384 / t], "dias", "%d × 0,384 milhão de km ÷ 1 milhão de km por dia = %s dias." % (t, num(0.384 * t)))


def UNITS(grade):
    return [
        H("M", "estados-fisicos-e-modelo-de-particulas", ["EF09CI01"], "Estados físicos e modelo de partículas", "Estados físicos",
          "Investigar as mudanças de estado físico da matéria e explicar essas transformações com base no modelo de constituição submicroscópica.",
          "sólido, líquido, gasoso, fusão, vaporização, condensação, solidificação, sublimação e agitação das partículas",
          "A matéria é feita de partículas em movimento", "Aquecer aumenta a agitação das partículas e muda o estado físico.",
          ["No sólido as partículas estão muito unidas e só vibram; no líquido estão próximas mas deslizam; no gás estão afastadas e se movem livremente.",
           "Aquecendo, as partículas se agitam mais: o sólido funde, o líquido vaporiza. Resfriando, o gás condensa e o líquido solidifica. A passagem direta sólido ↔ gás é a sublimação.",
           "A água pura funde a 0 °C e ferve a 100 °C ao nível do mar. Durante a mudança de estado de uma substância pura a temperatura fica constante."],
          [("Por que a naftalina diminui no armário?", ["Ela não derrete.", "Passa direto de sólido para gás."], "Por sublimação.")],
          [("As partículas do gelo ficam paradas.", "Elas vibram, mas presas nas posições."), ("Na fervura a temperatura continua subindo.", "Na água pura ela fica em 100 °C enquanto ferve.")],
          [("Por que a garrafa gelada fica molhada por fora?", "O vapor de água do ar condensa na superfície fria."), ("Por que a água ferve a menos de 100 °C em La Paz?", "Porque a pressão do ar é menor em lugares altos.")],
          [("Mudanças", [("a fusão", "sólido para líquido"), ("a solidificação", "líquido para sólido"), ("a vaporização", "líquido para gasoso"), ("a condensação", "gasoso para líquido"),
                         ("a sublimação", "sólido para gasoso"), ("a ressublimação", "gasoso para sólido"), ("a ebulição", "vaporização com bolhas em todo o líquido"),
                         ("a evaporação", "vaporização lenta pela superfície")],
            "O que acontece em {k}?", D),
           ("Exemplos", [("o sorvete derretendo", "fusão"), ("a água virando gelo no congelador", "solidificação"), ("a roupa secando no varal", "evaporação"), ("a água fervendo na panela", "ebulição"),
                         ("o espelho embaçado depois do banho", "condensação"), ("a naftalina sumindo no armário", "sublimação"), ("a geada formada direto do vapor", "ressublimação"),
                         ("o orvalho nas folhas de manhã", "condensação"), ("a lava esfriando e virando rocha", "solidificação")],
            "Que mudança de estado ocorre em {k}?", None),
           ("Estados", {"as características do estado sólido": ["forma própria", "volume próprio", "partículas bem organizadas", "partículas só vibram", "difícil de comprimir"],
                        "as características do estado líquido": ["forma do recipiente", "volume constante", "partículas deslizam umas sobre as outras", "escorre", "superfície plana em repouso"],
                        "as características do estado gasoso": ["ocupa todo o recipiente", "fácil de comprimir", "partículas muito afastadas", "partículas se movem livremente", "volume variável"]})],
          ["No gás as partículas estão afastadas.", "Aquecer aumenta a agitação das partículas.", "A sublimação vai de sólido para gás.", "A água pura ferve a 100 °C ao nível do mar.",
           "O orvalho é uma condensação.", "Na mudança de estado de uma substância pura a temperatura fica constante.", "O sólido tem forma própria."],
          [("As partículas do sólido ficam totalmente paradas.", "Elas vibram."), ("A condensação vai de líquido para gás.", "Vai de gás para líquido."),
           ("Na ebulição a temperatura da água pura sobe sem parar.", "Fica constante."), ("O gás tem forma própria.", "Ocupa todo o recipiente."), ("A naftalina some por fusão.", "Some por sublimação.")],
          "os estados físicos da matéria", "matter"),

        H("M", "reacoes-quimicas-e-conservacao-da-massa", ["EF09CI02"], "Reações químicas e conservação da massa", "Reações químicas",
          "Comparar quantidades de reagentes e produtos envolvidos em transformações químicas, estabelecendo a proporção entre as suas massas.",
          "reagentes, produtos, equação química, lei de Lavoisier, lei de Proust e sistemas abertos e fechados",
          "Nada se perde, tudo se transforma", "Em sistema fechado, massa dos reagentes = massa dos produtos.",
          ["Numa reação química, os reagentes se transformam em produtos. A equação química mostra isso: reagentes → produtos.",
           "Lei de Lavoisier: em sistema fechado, a massa total se conserva. Se um gás escapa num sistema aberto, a balança mostra menos massa.",
           "Lei de Proust: as substâncias reagem sempre na mesma proporção de massa. Se 2 g de hidrogênio reagem com 16 g de oxigênio, 4 g reagem com 32 g."],
          [("1 g de hidrogênio reage com 8 g de oxigênio. Quanto oxigênio reage com 3 g de hidrogênio?", ["A proporção é sempre 1 : 8.", "3 × 8 = 24."], "24 g.")],
          [("A palha de aço queimada fica mais leve.", "Fica mais pesada: o ferro se combina com o oxigênio do ar."), ("A massa some quando a lenha queima.", "Gases e cinzas juntos têm a mesma massa.")],
          [("Quem foi Lavoisier?", "Químico francês do século XVIII que mostrou a conservação da massa."), ("O que é catalisador?", "Substância que acelera a reação sem ser consumida.")],
          [("Conceitos", [("o reagente", "substância que é consumida na reação"), ("o produto", "substância formada na reação"), ("a lei de Lavoisier", "a massa total se conserva em sistema fechado"),
                          ("a lei de Proust", "as substâncias reagem em proporção de massa constante"), ("o sistema fechado", "não troca matéria com o ambiente"), ("o sistema aberto", "troca matéria com o ambiente"),
                          ("o catalisador", "acelera a reação sem ser consumido"), ("a equação química", "representação da reação com fórmulas")],
            "O que é {k}?", D),
           ("Reações", [("a queima do carvão", "carbono + oxigênio → gás carbônico"), ("a formação da água", "hidrogênio + oxigênio → água"), ("a ferrugem", "ferro + oxigênio + água → óxido de ferro"),
                        ("a fotossíntese", "gás carbônico + água → glicose + oxigênio"), ("a respiração celular", "glicose + oxigênio → gás carbônico + água"),
                        ("o vinagre com bicarbonato", "ácido + bicarbonato → sal + água + gás carbônico"), ("a combustão do gás de cozinha", "butano + oxigênio → gás carbônico + água")],
            "Qual é a reação de {k}?", D),
           ("Massa", {"as situações em que a balança mostra a mesma massa": ["reação em frasco bem tampado", "reação em balão fechado", "dissolução de sal num pote fechado", "ferrugem dentro de um pote lacrado", "comprimido efervescente em garrafa fechada"],
                      "as situações em que a balança mostra menos massa": ["comprimido efervescente em copo aberto", "vinagre e bicarbonato em copo aberto", "papel queimando ao ar livre", "álcool evaporando de um prato", "lenha queimando na fogueira"],
                      "as situações em que a balança mostra mais massa": ["palha de aço queimada ao ar", "prego enferrujando ao ar", "magnésio queimando ao ar", "cobre escurecendo ao aquecer ao ar", "ferro oxidando na umidade"]})],
          ["Em sistema fechado a massa se conserva.", "Os reagentes se transformam em produtos.", "A lei de Proust fala de proporções constantes.", "O catalisador não é consumido.",
           "A palha de aço queimada fica mais pesada.", "Num copo aberto o gás escapa e a massa medida diminui.", "Lavoisier estudou a conservação da massa."],
          [("Em sistema fechado a massa diminui.", "Ela se conserva."), ("A palha de aço queimada fica mais leve.", "Ganha oxigênio e fica mais pesada."), ("O catalisador é consumido na reação.", "Não é consumido."),
           ("Os produtos existem antes da reação.", "São formados na reação."), ("A proporção entre reagentes muda a cada vez.", "É constante, pela lei de Proust.")],
          "as reações químicas", "matter", calc=f_massa),

        H("M", "estrutura-atomica", ["EF09CI03"], "Estrutura atômica e modelos de átomo", "Estrutura atômica",
          "Identificar modelos que descrevem a estrutura da matéria (constituição do átomo e composição de moléculas simples) e reconhecer sua evolução histórica.",
          "Dalton, Thomson, Rutherford e Bohr, prótons, nêutrons, elétrons, número atômico, número de massa e moléculas",
          "Núcleo com prótons e nêutrons; elétrons em volta", "Z = prótons; A = prótons + nêutrons.",
          ["Os modelos evoluíram: Dalton (esfera maciça), Thomson (pudim com elétrons), Rutherford (núcleo pequeno e denso com elétrons ao redor) e Bohr (elétrons em níveis de energia).",
           "O núcleo tem prótons (+) e nêutrons (sem carga). Os elétrons (−) ficam na eletrosfera. O número atômico Z é o número de prótons; o número de massa A é prótons + nêutrons.",
           "No átomo neutro, elétrons = prótons. Átomos se unem em moléculas: H₂O tem 2 hidrogênios e 1 oxigênio; CO₂ tem 1 carbono e 2 oxigênios."],
          [("Quantos nêutrons tem o sódio, com Z = 11 e A = 23?", ["Nêutrons = A − Z.", "23 − 11 = 12."], "12 nêutrons.")],
          [("O átomo é maciço como uma bolinha.", "Rutherford mostrou que é quase todo vazio."), ("A massa de um átomo vem dos elétrons.", "Quase toda a massa está no núcleo.")],
          [("O que mostrou o experimento de Rutherford?", "Que quase todas as partículas alfa atravessam a lâmina de ouro: o átomo tem um núcleo pequeno e muito espaço vazio."), ("O que é íon?", "Átomo que ganhou ou perdeu elétrons e ficou com carga.")],
          [("Modelos", [("Dalton", "átomo como esfera maciça e indivisível"), ("Thomson", "esfera positiva com elétrons espalhados, como um pudim de passas"),
                        ("Rutherford", "núcleo pequeno e denso com elétrons ao redor e muito espaço vazio"), ("Bohr", "elétrons em órbitas com níveis de energia definidos"),
                        ("Chadwick", "descobriu o nêutron"), ("Demócrito", "propôs na Grécia Antiga que a matéria é feita de átomos")],
            "Qual modelo ou ideia está ligado a {k}?", D),
           ("Partículas", [("o próton", "partícula positiva do núcleo"), ("o nêutron", "partícula sem carga do núcleo"), ("o elétron", "partícula negativa da eletrosfera"),
                           ("o número atômico", "número de prótons do átomo"), ("o número de massa", "soma de prótons e nêutrons"), ("o íon positivo", "átomo que perdeu elétrons"),
                           ("o íon negativo", "átomo que ganhou elétrons"), ("os isótopos", "átomos com mesmo número de prótons e nêutrons diferentes")],
            "O que é {k}?", D),
           ("Moléculas", {"as substâncias simples": ["o gás oxigênio (O₂)", "o gás hidrogênio (H₂)", "o ozônio (O₃)", "o gás nitrogênio (N₂)", "o diamante (C)"],
                          "as substâncias compostas": ["a água (H₂O)", "o gás carbônico (CO₂)", "o sal de cozinha (NaCl)", "o metano (CH₄)", "a amônia (NH₃)"],
                          "as partículas que formam o átomo": ["o próton", "o nêutron", "o elétron", "o núcleo atômico", "a eletrosfera"]})],
          ["O núcleo tem prótons e nêutrons.", "O elétron tem carga negativa.", "Z é o número de prótons.", "No átomo neutro, elétrons = prótons.", "Rutherford propôs o núcleo atômico.",
           "Bohr propôs níveis de energia.", "A água tem dois átomos de hidrogênio."],
          [("O nêutron tem carga positiva.", "O nêutron não tem carga."), ("O elétron fica no núcleo.", "Fica na eletrosfera."), ("A massa do átomo vem dos elétrons.", "Vem quase toda do núcleo."),
           ("Dalton descobriu o núcleo.", "Foi Rutherford."), ("O O₂ é uma substância composta.", "É uma substância simples.")],
          "a estrutura atômica", "matter", calc=f_atomo),

        H("M", "ondas-luz-e-cores", ["EF09CI04", "EF09CI05"], "Ondas, luz e cores", "Ondas, luz e cores",
          "Planejar e executar experimentos que evidenciem que todas as cores de luz podem ser formadas pela composição das três cores primárias da luz e que a cor de um objeto está relacionada também à cor da luz que o ilumina; investigar os principais mecanismos envolvidos na transmissão e recepção de imagem e som que revolucionaram os sistemas de comunicação humana.",
          "ondas, amplitude, frequência, comprimento de onda, som e luz, cores primárias da luz, dispersão e transmissão de sinais",
          "Ondas transportam energia", "Cores primárias da luz: vermelho, verde e azul. v = λ × f.",
          ["Uma onda transporta energia sem transportar matéria. Tem amplitude, comprimento de onda (λ) e frequência (f). A velocidade é v = λ × f.",
           "O som é uma onda mecânica: precisa de um meio. A luz é uma onda eletromagnética: atravessa o vácuo a cerca de 300.000 km/s.",
           "As cores primárias da luz são vermelho, verde e azul (RGB): juntas formam o branco. Um objeto parece vermelho porque reflete a luz vermelha e absorve as outras."],
          [("Que cor parece uma camiseta branca iluminada só por luz vermelha?", ["O branco reflete todas as cores.", "Só chega luz vermelha."], "Vermelha.")],
          [("As cores primárias da luz são vermelho, amarelo e azul.", "Na luz são vermelho, verde e azul; vermelho, amarelo e azul são as das tintas."), ("O som viaja no vácuo.", "O som precisa de um meio.")],
          [("Por que vemos o arco-íris?", "As gotas de chuva separam a luz branca em cores (dispersão)."), ("Como a TV forma as cores?", "Combinando pontinhos de luz vermelha, verde e azul.")],
          [("Cores", [("luz vermelha + luz verde", "amarelo"), ("luz vermelha + luz azul", "magenta"), ("luz verde + luz azul", "ciano"), ("luz vermelha + luz verde + luz azul", "branco"),
                      ("objeto vermelho sob luz verde", "preto"), ("objeto branco sob luz azul", "azul"), ("objeto verde sob luz branca", "verde"), ("objeto preto sob luz branca", "preto")],
            "Que cor resulta de {k}?", None),
           ("Ondas", [("a amplitude", "altura da onda, ligada à intensidade"), ("a frequência", "número de oscilações por segundo"), ("o comprimento de onda", "distância entre duas cristas"),
                      ("o hertz", "unidade de frequência"), ("a onda mecânica", "precisa de um meio para se propagar"), ("a onda eletromagnética", "propaga-se até no vácuo"),
                      ("a dispersão da luz", "separação da luz branca em cores"), ("o eco", "reflexão do som")],
            "O que é {k}?", D),
           ("Tipos", {"as ondas mecânicas": ["o som", "a onda do mar", "a onda numa corda", "a onda de um terremoto", "o ultrassom"],
                      "as ondas eletromagnéticas": ["a luz visível", "as ondas de rádio", "as micro-ondas", "os raios X", "a radiação ultravioleta"],
                      "os meios de comunicação que usam ondas eletromagnéticas": ["o celular", "o rádio FM", "a TV aberta", "o wi-fi", "o GPS"]})],
          ["Ondas transportam energia.", "O som precisa de um meio.", "A luz atravessa o vácuo.", "Vermelho, verde e azul são as cores primárias da luz.", "Luz vermelha e verde formam amarelo.",
           "Um objeto vermelho reflete luz vermelha.", "v = λ × f."],
          [("O som atravessa o vácuo.", "Precisa de um meio."), ("Ondas transportam matéria.", "Transportam energia."), ("As cores primárias da luz são vermelho, amarelo e azul.", "São vermelho, verde e azul."),
           ("Um objeto preto reflete todas as cores.", "Ele absorve quase toda a luz."), ("A luz é uma onda mecânica.", "É eletromagnética.")],
          "as ondas e as cores", "waves-and-light", calc=f_onda),

        H("M", "radiacoes-e-tecnologia", ["EF09CI06", "EF09CI07"], "Radiações e suas aplicações", "Radiações",
          "Classificar as radiações eletromagnéticas por suas frequências, fontes e aplicações, discutindo e avaliando as implicações de seu uso em controle remoto, telefone celular, raio X, forno de micro-ondas, fotocélulas etc.; discutir o papel do avanço tecnológico na aplicação das radiações na medicina diagnóstica e no tratamento de doenças.",
          "espectro eletromagnético, rádio, micro-ondas, infravermelho, luz visível, ultravioleta, raios X e gama, aplicações e riscos",
          "Do rádio aos raios gama", "Quanto maior a frequência, mais energia tem a radiação.",
          ["O espectro eletromagnético vai das ondas de rádio (baixa frequência) aos raios gama (alta frequência), passando por micro-ondas, infravermelho, luz visível, ultravioleta e raios X.",
           "Quanto maior a frequência, maior a energia: ultravioleta, raios X e gama podem danificar células e o DNA.",
           "Aplicações: rádio e TV, micro-ondas (forno e celular), infravermelho (controle remoto), raios X (radiografia), radioterapia com raios gama no tratamento do câncer."],
          [("Que radiação o controle remoto da TV usa?", ["Não a vemos, mas a câmera do celular às vezes mostra uma luzinha.", "É uma radiação logo abaixo do vermelho."], "Infravermelho.")],
          [("Toda radiação faz mal.", "A luz visível e as ondas de rádio são usadas no dia a dia sem perigo."), ("O forno de micro-ondas deixa a comida radioativa.", "Ele só aquece a água dos alimentos.")],
          [("Por que o técnico de raio X sai da sala?", "Para evitar exposição repetida à radiação."), ("O que é radioterapia?", "Tratamento que usa radiação para destruir células de tumores.")],
          [("Aplicações", [("as ondas de rádio", "transmissão de rádio e TV"), ("as micro-ondas", "aquecer alimentos e comunicação de celulares"), ("o infravermelho", "controle remoto e câmeras térmicas"),
                           ("a luz visível", "visão e fibra óptica"), ("a radiação ultravioleta", "esterilização e bronzeamento"), ("os raios X", "radiografias e tomografias"),
                           ("os raios gama", "radioterapia e esterilização de equipamentos médicos")],
            "Qual é uma aplicação de {k}?", "Que radiação é usada em {v}?"),
           ("Ordem", [("as ondas de rádio", "a menor frequência do espectro"), ("os raios gama", "a maior frequência e energia do espectro"), ("o infravermelho", "entre as micro-ondas e a luz vermelha"),
                      ("a radiação ultravioleta", "entre a luz violeta e os raios X"), ("a luz vermelha", "a cor visível de menor frequência"), ("a luz violeta", "a cor visível de maior frequência"),
                      ("as micro-ondas", "entre as ondas de rádio e o infravermelho"), ("os raios X", "entre o ultravioleta e os raios gama")],
            "Onde fica {k} no espectro eletromagnético?", D),
           ("Riscos e cuidados", {"as radiações ionizantes, de alta energia": ["os raios X", "os raios gama", "a radiação ultravioleta de alta energia", "a radiação de materiais radioativos", "a radiação cósmica"],
                                  "as radiações não ionizantes, de baixa energia": ["as ondas de rádio", "as micro-ondas", "o infravermelho", "a luz visível", "as ondas do wi-fi"],
                                  "os cuidados com radiações": ["usar avental de chumbo no raio X", "usar protetor solar", "não ligar o micro-ondas aberto", "limitar exames de raio X ao necessário", "respeitar placas de área radioativa"]})],
          ["Os raios gama têm a maior frequência.", "O controle remoto usa infravermelho.", "As micro-ondas aquecem a água dos alimentos.", "Os raios X são usados em radiografias.",
           "Quanto maior a frequência, maior a energia.", "A radioterapia trata tumores.", "As ondas de rádio têm a menor frequência."],
          [("As ondas de rádio têm a maior frequência.", "Têm a menor."), ("O micro-ondas deixa a comida radioativa.", "Só aquece a água."), ("O controle remoto usa raios X.", "Usa infravermelho."),
           ("A luz visível tem mais energia que os raios X.", "Os raios X têm mais energia."), ("Radiação ultravioleta não afeta a pele.", "Pode causar queimaduras e câncer de pele.")],
          "as radiações", "waves-and-light"),

        H("V", "hereditariedade", ["EF09CI08", "EF09CI09"], "Hereditariedade e genética", "Hereditariedade",
          "Associar os gametas à transmissão das características hereditárias, estabelecendo relações entre ancestrais e descendentes; discutir as ideias de Mendel sobre hereditariedade (fatores hereditários, segregação, gametas, fecundação), considerando-as para resolver problemas envolvendo a transmissão de características hereditárias em diferentes organismos.",
          "genes, cromossomos, DNA, alelos dominantes e recessivos, genótipo, fenótipo, Mendel e cruzamentos",
          "Genes passam dos pais aos filhos", "Cada um recebe um alelo do pai e um da mãe; Aa × Aa dá 1/4 de aa.",
          ["As características hereditárias são passadas pelos genes, trechos do DNA que ficam nos cromossomos. Os gametas levam metade dos cromossomos de cada genitor.",
           "Cada gene tem duas versões (alelos), uma de cada genitor. O alelo dominante (A) se manifesta mesmo em dose única; o recessivo (a) só aparece em dose dupla (aa).",
           "Mendel estudou ervilhas e mostrou que os fatores se separam nos gametas. No cruzamento Aa × Aa, os filhos são 1/4 AA, 1/2 Aa e 1/4 aa."],
          [("Pais de olhos castanhos podem ter um filho de olhos azuis (num modelo simplificado)?", ["Se os dois forem Aa.", "1/4 dos filhos pode ser aa."], "Sim, se os dois forem heterozigotos.")],
          [("O filho é a soma igual de tudo dos pais.", "Recebe metade dos cromossomos de cada um, ao acaso."), ("Dominante quer dizer mais comum.", "Quer dizer que se manifesta com um só alelo.")],
          [("Quem foi Mendel?", "Um monge que, no século XIX, descobriu as leis básicas da hereditariedade estudando ervilhas."), ("Quantos cromossomos tem a célula humana?", "46, em 23 pares; os gametas têm 23.")],
          [("Conceitos", [("o gene", "trecho do DNA que determina uma característica"), ("o cromossomo", "estrutura de DNA enrolado no núcleo"), ("o alelo", "uma das versões de um gene"),
                          ("o genótipo", "a combinação de alelos de um indivíduo"), ("o fenótipo", "a característica que se observa"), ("o homozigoto", "indivíduo com dois alelos iguais"),
                          ("o heterozigoto", "indivíduo com dois alelos diferentes"), ("o alelo recessivo", "só se manifesta em dose dupla"), ("o alelo dominante", "manifesta-se com uma só cópia")],
            "O que é {k}?", D),
           ("Genótipo", [("AA", "homozigoto dominante"), ("Aa", "heterozigoto"), ("aa", "homozigoto recessivo"), ("BB", "homozigoto dominante"), ("Bb", "heterozigoto"),
                         ("bb", "homozigoto recessivo"), ("VV", "homozigoto dominante"), ("Vv", "heterozigoto"), ("vv", "homozigoto recessivo"), ("RR", "homozigoto dominante"), ("Rr", "heterozigoto"), ("rr", "homozigoto recessivo")],
            "Como se classifica o genótipo {k}?", None, ("haploide",), True, "O genótipo {k} é {v}"),
           ("Herança", {"as características hereditárias": ["o tipo sanguíneo", "a cor natural dos olhos", "o formato do lóbulo da orelha", "o daltonismo", "a cor da flor da ervilha"],
                        "as características adquiridas": ["uma cicatriz", "músculos desenvolvidos pela academia", "o bronzeado", "falar um idioma", "o cabelo pintado"],
                        "as estruturas onde está a informação genética": ["o DNA", "os genes", "os cromossomos", "o núcleo da célula", "os gametas"]})],
          ["Os genes ficam nos cromossomos.", "Cada filho recebe um alelo de cada genitor.", "Aa é heterozigoto.", "O recessivo só aparece em dose dupla.", "Mendel estudou ervilhas.",
           "A célula humana tem 46 cromossomos.", "Os gametas têm 23 cromossomos."],
          [("O recessivo aparece com uma só cópia.", "Precisa de duas cópias."), ("Aa é homozigoto.", "É heterozigoto."), ("Uma cicatriz é hereditária.", "É adquirida."),
           ("Os gametas têm 46 cromossomos.", "Têm 23."), ("Dominante significa mais comum.", "Significa que se manifesta com uma cópia.")],
          "a hereditariedade", "living-things-and-ecosystems", calc=f_gen, s4="Faça os cruzamentos"),

        H("V", "evolucao", ["EF09CI10", "EF09CI11"], "Evolução dos seres vivos", "Evolução",
          "Comparar as ideias evolucionistas de Lamarck e Darwin apresentadas em textos científicos e históricos, identificando semelhanças e diferenças entre essas ideias e sua importância para explicar a diversidade biológica; discutir a evolução e a diversidade das espécies com base na atuação da seleção natural sobre as variantes de uma mesma espécie, resultantes de processo reprodutivo.",
          "Lamarck, Darwin, seleção natural, variabilidade, adaptação, fósseis e especiação",
          "A seleção natural age sobre a variação", "Indivíduos mais adaptados deixam mais descendentes.",
          ["Lamarck propôs o uso e desuso e a herança das características adquiridas: a girafa esticaria o pescoço e passaria isso aos filhos. Essa ideia não se confirmou.",
           "Darwin e Wallace propuseram a seleção natural: os indivíduos variam; os que têm características vantajosas sobrevivem e se reproduzem mais, e essas características se tornam comuns.",
           "Com o tempo, populações isoladas podem acumular diferenças e formar espécies novas. Fósseis e semelhanças entre espécies são evidências da evolução."],
          [("Como Darwin explicaria o pescoço longo das girafas?", ["As girafas variavam no tamanho do pescoço.", "As de pescoço longo comiam mais folhas altas e deixavam mais filhotes."], "Por seleção natural das girafas com pescoço mais longo.")],
          [("O indivíduo evolui durante a vida.", "Quem evolui são as populações, ao longo das gerações."), ("O ser humano veio do chimpanzé.", "Os dois têm um ancestral comum.")],
          [("O que Darwin observou em Galápagos?", "Tentilhões com bicos diferentes em cada ilha, adaptados ao alimento."), ("Por que bactérias ficam resistentes a antibióticos?", "As poucas resistentes sobrevivem e se multiplicam.")],
          [("Lamarck ou Darwin", [("uso e desuso dos órgãos", "Lamarck"), ("herança das características adquiridas", "Lamarck"), ("a girafa estica o pescoço e passa isso aos filhos", "Lamarck"),
                                  ("a vontade do ser vivo de mudar o corpo", "Lamarck"), ("seleção natural", "Darwin"), ("sobrevivência dos mais adaptados ao ambiente", "Darwin"),
                                  ("a variação entre indivíduos da mesma espécie", "Darwin"), ("os tentilhões de Galápagos", "Darwin"), ("A origem das espécies, de 1859", "Darwin")],
            "A ideia “{k}” é de Lamarck ou de Darwin?", None, ("Mendel", "Wegener")),
           ("Conceitos", [("a seleção natural", "o ambiente favorece os indivíduos mais adaptados"), ("a adaptação", "característica que aumenta a chance de sobreviver e se reproduzir"),
                          ("a variabilidade", "diferenças entre indivíduos de uma população"), ("a mutação", "mudança no DNA que pode gerar novas características"),
                          ("a especiação", "formação de uma nova espécie"), ("o fóssil", "vestígio de ser vivo do passado"), ("o ancestral comum", "espécie da qual descendem duas ou mais espécies"),
                          ("a seleção artificial", "o ser humano escolhe quem se reproduz, como nas raças de cães")],
            "O que é {k}?", D),
           ("Evidências", {"as evidências fósseis, anatômicas e moleculares da evolução": ["os fósseis", "os órgãos homólogos", "as semelhanças no DNA", "os órgãos vestigiais", "as semelhanças entre embriões"],
                           "os exemplos de seleção natural": ["bactérias resistentes a antibióticos", "insetos resistentes a inseticidas", "mariposas escuras em áreas poluídas", "bicos dos tentilhões após secas", "camuflagem de presas"],
                           "os exemplos de seleção artificial": ["raças de cães", "milho com espigas grandes", "gado leiteiro", "variedades de couve e brócolis", "rosas de muitas cores"]})],
          ["A seleção natural age sobre a variação.", "Darwin propôs a seleção natural.", "Lamarck propôs o uso e desuso.", "Os fósseis são evidências da evolução.",
           "Bactérias resistentes mostram seleção natural.", "As populações evoluem ao longo das gerações.", "Humanos e chimpanzés têm um ancestral comum."],
          [("O ser humano veio do chimpanzé.", "Os dois têm um ancestral comum."), ("O indivíduo evolui durante a vida.", "Quem evolui é a população."), ("Darwin defendia o uso e desuso.", "Essa ideia é de Lamarck."),
           ("Características adquiridas passam aos filhos.", "Não passam pelos genes."), ("A seleção natural cria a variação.", "Ela age sobre a variação que já existe.")],
          "a evolução", "living-things-and-ecosystems"),

        H("V", "biodiversidade-e-unidades-de-conservacao", ["EF09CI12", "EF09CI13"], "Biodiversidade e unidades de conservação", "Unidades de conservação",
          "Justificar a importância das unidades de conservação para a preservação da biodiversidade e do patrimônio nacional, considerando os diferentes tipos de unidades (parques, reservas e florestas nacionais), as populações humanas e as atividades a eles relacionados; propor iniciativas individuais e coletivas para a solução de problemas ambientais da cidade ou da comunidade, com base na análise de ações de consumo consciente e de sustentabilidade bem-sucedidas.",
          "biodiversidade, SNUC, proteção integral e uso sustentável, parques nacionais, reservas extrativistas e sustentabilidade",
          "Proteger áreas protege espécies", "Proteção integral: sem uso direto. Uso sustentável: uso com regras.",
          ["O Brasil é um dos países com maior biodiversidade do mundo. As unidades de conservação (UCs) são áreas protegidas por lei, organizadas no SNUC.",
           "As UCs de proteção integral (parque nacional, reserva biológica, estação ecológica) não permitem uso direto dos recursos, só pesquisa, educação e, em parques, turismo.",
           "As de uso sustentável (reserva extrativista, floresta nacional, área de proteção ambiental) permitem usar recursos com regras, como na coleta de castanha pelas comunidades."],
          [("Um parque nacional permite derrubar árvores para vender madeira?", ["O parque é de proteção integral.", "Nele não há uso direto dos recursos."], "Não.")],
          [("Unidade de conservação proíbe sempre a presença de pessoas.", "Muitas permitem turismo e comunidades tradicionais."), ("Biodiversidade é só o número de animais.", "Inclui plantas, fungos, microrganismos e a variedade genética.")],
          [("Qual foi o primeiro parque nacional do Brasil?", "O Parque Nacional do Itatiaia, criado em 1937 entre RJ e MG."), ("O que é uma reserva extrativista?", "UC onde populações tradicionais vivem e usam recursos, como seringueiros.")],
          [("Tipo de UC", [("o parque nacional", "proteção integral"), ("a reserva biológica", "proteção integral"), ("a estação ecológica", "proteção integral"), ("o monumento natural", "proteção integral"),
                           ("a reserva extrativista", "uso sustentável"), ("a floresta nacional", "uso sustentável"), ("a área de proteção ambiental", "uso sustentável"),
                           ("a reserva de desenvolvimento sustentável", "uso sustentável"), ("a reserva particular do patrimônio natural", "uso sustentável")],
            "Em que grupo do SNUC está {k}?", None, ("área urbana", "terra devoluta")),
           ("Exemplos", [("o Parque Nacional do Iguaçu", "cataratas na Mata Atlântica do Paraná"), ("o Parque Nacional da Chapada Diamantina", "serras e cachoeiras na Bahia"),
                         ("a Reserva Extrativista Chico Mendes", "seringueiros no Acre"), ("o Parque Nacional de Fernando de Noronha", "arquipélago com golfinhos e tartarugas"),
                         ("o Parque Nacional do Jaú", "floresta e rios de água preta na Amazônia"), ("o Parque Nacional da Serra da Capivara", "pinturas rupestres no Piauí"),
                         ("o Parque Nacional do Itatiaia", "o primeiro parque nacional do Brasil"), ("o Parque Nacional da Chapada dos Veadeiros", "Cerrado de altitude em Goiás")],
            "O que caracteriza {k}?", D),
           ("Sustentabilidade", {"as iniciativas sustentáveis na comunidade": ["horta comunitária", "compostagem na escola", "coleta seletiva", "captação de água da chuva", "carona solidária"],
                                 "as ameaças à biodiversidade": ["o desmatamento", "a caça ilegal", "o tráfico de animais silvestres", "as espécies invasoras", "a poluição dos rios"],
                                 "as unidades de proteção integral": ["o parque nacional", "a reserva biológica", "a estação ecológica", "o monumento natural", "o refúgio de vida silvestre"]})],
          ["O Brasil tem grande biodiversidade.", "Parques nacionais são de proteção integral.", "Reservas extrativistas são de uso sustentável.", "O SNUC organiza as unidades de conservação.",
           "Biodiversidade inclui a variedade genética.", "O tráfico de animais ameaça a biodiversidade.", "O Itatiaia foi o primeiro parque nacional do Brasil."],
          [("Parques nacionais permitem exploração de madeira.", "São de proteção integral."), ("Reserva extrativista é de proteção integral.", "É de uso sustentável."),
           ("Biodiversidade inclui só animais.", "Inclui todos os seres vivos e sua variedade genética."), ("Nenhuma UC permite visitação.", "Parques permitem turismo."),
           ("O tráfico de animais ajuda as espécies.", "É uma grave ameaça.")],
          "as unidades de conservação", "living-things-and-ecosystems"),

        H("T", "sistema-solar-e-universo", ["EF09CI14", "EF09CI15", "EF09CI16", "EF09CI17"], "Sistema Solar, Universo e vida", "Sistema Solar e Universo",
          "Descrever a composição e a estrutura do Sistema Solar (Sol, planetas rochosos, planetas gigantes gasosos e corpos menores), assim como a localização do Sistema Solar na nossa Galáxia (a Via Láctea) e dela no Universo (apenas uma galáxia dentre bilhões); relacionar diferentes leituras do céu e explicações sobre a origem da Terra, do Sol ou do Sistema Solar às necessidades de distintas culturas; selecionar argumentos sobre a viabilidade da sobrevivência humana fora da Terra; analisar o ciclo evolutivo do Sol (nascimento, vida e morte) baseado no conhecimento das etapas de evolução de estrelas de diferentes dimensões e os efeitos desse processo no nosso planeta.",
          "Sol, planetas rochosos e gasosos, corpos menores, Via Láctea, galáxias, ano-luz, evolução estelar e vida fora da Terra",
          "Uma estrela entre bilhões, numa galáxia entre bilhões", "Rochosos: Mercúrio, Vênus, Terra, Marte. Gasosos: Júpiter, Saturno, Urano, Netuno.",
          ["O Sistema Solar tem o Sol, oito planetas (quatro rochosos e quatro gigantes gasosos), planetas-anões como Plutão, luas, asteroides e cometas.",
           "O Sol é uma das bilhões de estrelas da Via Láctea, que é apenas uma entre bilhões de galáxias. Distâncias tão grandes são medidas em anos-luz.",
           "Estrelas nascem em nebulosas. O Sol vai brilhar por mais uns 5 bilhões de anos, virar gigante vermelha e terminar como anã branca. Estrelas muito maiores explodem como supernovas."],
          [("Júpiter é um planeta rochoso ou gasoso?", ["Júpiter é o maior planeta.", "É formado principalmente por hidrogênio e hélio."], "Gasoso.")],
          [("Plutão é o nono planeta.", "Desde 2006 é classificado como planeta-anão."), ("Ano-luz é medida de tempo.", "É a distância que a luz percorre em um ano.")],
          [("Por que é difícil viver em Marte?", "Ar rarefeito de gás carbônico, frio extremo, radiação e falta de água líquida na superfície."), ("Como os povos indígenas leem o céu?", "Muitos usam constelações próprias, como a Ema dos guaranis, para marcar estações e plantios.")],
          [("Planetas", [("Mercúrio", "o planeta mais próximo do Sol"), ("Vênus", "o planeta mais quente, com atmosfera densa"), ("a Terra", "o único planeta com vida conhecida"),
                         ("Marte", "o planeta vermelho, com o vulcão Olimpo"), ("Júpiter", "o maior planeta, com a Grande Mancha Vermelha"), ("Saturno", "o planeta com os anéis mais visíveis"),
                         ("Urano", "gigante gelado que gira deitado"), ("Netuno", "o planeta mais distante do Sol")],
            "O que caracteriza {k}?", D),
           ("Universo", [("a Via Láctea", "a galáxia onde está o Sistema Solar"), ("o ano-luz", "a distância que a luz percorre em um ano"), ("a unidade astronômica", "a distância média Terra–Sol"),
                         ("a nebulosa", "nuvem de gás e poeira onde estrelas nascem"), ("a gigante vermelha", "fase futura do Sol, quando ele vai se expandir"), ("a anã branca", "o que restará do Sol no fim"),
                         ("a supernova", "explosão de uma estrela muito grande"), ("o buraco negro", "região com gravidade tão forte que nem a luz escapa"), ("o cometa", "corpo de gelo e poeira com cauda perto do Sol")],
            "O que é {k}?", D),
           ("Classificação", {"os planetas rochosos": ["Mercúrio", "Vênus", "a Terra", "Marte"], "os planetas gasosos": ["Júpiter", "Saturno", "Urano", "Netuno"],
                              "os corpos menores do Sistema Solar": ["os asteroides", "os cometas", "os meteoroides", "Plutão", "Ceres"]})],
          ["O Sistema Solar tem oito planetas.", "Júpiter é o maior planeta.", "Marte é rochoso.", "A Via Láctea é a nossa galáxia.", "Ano-luz é uma distância.",
           "O Sol terminará como anã branca.", "Plutão é um planeta-anão."],
          [("Plutão é o nono planeta.", "É um planeta-anão."), ("Ano-luz mede tempo.", "Mede distância."), ("Júpiter é rochoso.", "É gasoso."), ("O Sol vai explodir como supernova.", "Ele vai virar anã branca."),
           ("A Via Láctea é a única galáxia.", "Há bilhões de galáxias.")],
          "o Sistema Solar e o Universo", "earth-and-space", calc=f_astro),
    ]
