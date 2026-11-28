# -*- coding: utf-8 -*-
"""Brasil / Ciências: 5º ano (BNCC EF05CI01–EF05CI13)"""
from br_sci import H, it, nq, num

D = "A que corresponde esta descrição: {v}?"


def f_agua(R):
    k = R.choice(["banho", "torneira", "descarga", "vazamento", "familia"])
    if k == "banho":
        m, v = R.choice([(15, 9), (20, 9), (10, 12), (12, 9), (8, 12), (25, 6)])
        a = R.choice([5, 4, 6])
        return nq("Um chuveiro gasta cerca de %d litros por minuto. Quantos litros se economizam se o banho cair de %d para %d minutos?" % (v, m, a), (m - a) * v,
                  [m * v, a * v, m - a, (m + a) * v], "L", "(%d − %d) × %d = %d litros economizados." % (m, a, v, (m - a) * v))
    if k == "torneira":
        v, t = R.choice([(12, 3), (10, 4), (12, 5), (8, 3), (6, 5), (15, 2)])
        return nq("Escovando os dentes com a torneira aberta, saem %d litros por minuto. Quanto se gasta em %d minutos?" % (v, t), v * t, [v + t, v * t * 2, v, v * (t + 1)], "L",
                  "%d × %d = %d litros. Fechar a torneira economiza quase tudo isso." % (v, t, v * t))
    if k == "descarga":
        v, n = R.choice([(6, 5), (12, 4), (6, 8), (9, 6), (12, 3), (6, 10)])
        return nq("Uma descarga usa %d litros. Quantos litros são usados em %d descargas?" % (v, n), v * n, [v + n, v * n // 2, v * (n - 1), v * n * 10], "L",
                  "%d × %d = %d litros." % (v, n, v * n))
    if k == "vazamento":
        g, d = R.choice([(20, 30), (40, 30), (30, 7), (50, 10), (25, 30), (60, 7)])
        return nq("Uma torneira pingando desperdiça %d litros por dia. Quanto ela desperdiça em %d dias?" % (g, d), g * d, [g + d, g * d // 10, g * (d - 1), g * d * 2], "L",
                  "%d × %d = %s litros." % (g, d, num(g * d)))
    p, v = R.choice([(4, 110), (3, 120), (5, 100), (2, 150), (6, 110), (4, 150)])
    return nq("Cada pessoa de uma família usa, em média, %d litros de água por dia. A família tem %d pessoas. Quantos litros a família usa por dia?" % (v, p), p * v,
              [p + v, v, p * v * 30, p * v // 2], "L", "%d × %d = %s litros por dia." % (p, v, num(p * v)))


def f_kcal(R):
    k = R.choice(["soma", "rest", "mult", "exerc"])
    F = [("uma banana", 90), ("um copo de leite", 120), ("um pão francês", 135), ("uma maçã", 70), ("um ovo cozido", 75), ("uma colher de arroz", 40),
         ("uma concha de feijão", 70), ("um copo de refrigerante", 85), ("uma fatia de queijo", 60), ("uma laranja", 50)]
    if k == "soma":
        (a, x), (b, y) = R.sample(F, 2)
        return nq("%s tem cerca de %d kcal e %s tem cerca de %d kcal. Quantas quilocalorias há nos dois juntos?" % (a[0].upper() + a[1:], x, b, y), x + y,
                  [abs(x - y), x * y // 10, x, x + y + 10], "kcal", "%d + %d = %d kcal." % (x, y, x + y))
    if k == "mult":
        (a, x) = R.choice(F)
        n = R.choice([2, 3, 4])
        return nq("Se %s tem cerca de %d kcal, quantas quilocalorias há em %d porções iguais?" % (a, x, n), x * n, [x + n, x, x * n + x, x * (n - 1)], "kcal",
                  "%d × %d = %d kcal." % (x, n, x * n))
    if k == "rest":
        t, u = R.choice([(2000, 450), (1800, 600), (2200, 700), (1600, 350), (2000, 800), (1900, 550)])
        return nq("Uma criança precisa de cerca de %s kcal por dia e já consumiu %d kcal no café da manhã e no lanche. Quanto falta para chegar ao total?" % (num(t), u), t - u,
                  [t + u, u, t // u, t - u - 100], "kcal", "%s − %d = %s kcal." % (num(t), u, num(t - u)))
    e, m = R.choice([("andar de bicicleta", 5), ("correr", 8), ("nadar", 7), ("caminhar", 4), ("pular corda", 10), ("jogar futebol", 7)])
    t = R.choice([20, 30, 40, 15])
    return nq("Ao %s, uma criança gasta cerca de %d kcal por minuto. Quanto ela gasta em %d minutos?" % (e, m, t), m * t, [m + t, m * t * 2, t, m * (t - 10)], "kcal",
              "%d × %d = %d kcal." % (m, t, m * t))


def UNITS(grade):
    return [
        H("M", "propriedades-dos-materiais", ["EF05CI01"], "Propriedades físicas dos materiais", "Propriedades dos materiais",
          "Explorar fenômenos da vida cotidiana que evidenciem propriedades físicas dos materiais, como densidade, condutibilidade térmica e elétrica, respostas a forças magnéticas, solubilidade, respostas a forças mecânicas (dureza, elasticidade etc.), entre outras.",
          "densidade, condução de calor e de eletricidade, magnetismo, dureza, elasticidade e solubilidade",
          "Cada material reage de um jeito", "Metais conduzem calor e eletricidade; o ímã atrai o ferro; o óleo flutua na água.",
          ["Densidade: materiais menos densos que a água flutuam (óleo, madeira, isopor); mais densos afundam (pedra, ferro).",
           "Condutores deixam passar calor e eletricidade (metais). Isolantes dificultam (plástico, borracha, madeira, isopor).",
           "Dureza é resistir a riscos; elasticidade é voltar ao formato depois de esticar; solubilidade é dissolver-se em um líquido."],
          [("Por que o cabo da panela é de plástico?", ["O metal da panela conduz muito calor.", "O plástico é isolante térmico."], "Para não queimar a mão: o plástico conduz pouco calor.")],
          [("Tudo que é pesado afunda.", "Um navio de aço flutua: depende da densidade e da forma."), ("O ímã atrai todos os metais.", "Atrai ferro, níquel e cobalto, mas não alumínio nem cobre.")],
          [("Por que o fio elétrico é de cobre com capa de plástico?", "O cobre conduz eletricidade e o plástico isola, evitando choques."), ("O que é mais duro, o diamante ou o vidro?", "O diamante: ele risca o vidro.")],
          [("Propriedade", [("o cobre do fio elétrico", "conduz eletricidade"), ("o plástico da capa do fio", "isola a eletricidade"), ("o elástico de borracha", "estica e volta ao formato"),
                            ("o diamante", "é o mais duro de todos"), ("o isopor da caixa térmica", "isola o calor"), ("o ferro do prego", "é atraído pelo ímã"),
                            ("o açúcar", "dissolve-se na água"), ("o óleo de cozinha", "flutua na água"), ("o vidro da janela", "é transparente")],
            "Que propriedade se destaca em {k}?", "Qual material {v}?"),
           ("Flutua ou afunda", [("a rolha de cortiça", "flutua"), ("a pedra", "afunda"), ("o isopor", "flutua"), ("a moeda", "afunda"), ("o óleo", "flutua"),
                                 ("o prego", "afunda"), ("o pedaço de madeira", "flutua"), ("a bolinha de gude", "afunda"), ("o gelo", "flutua"), ("a chave de metal", "afunda")],
            "Na água, {k} flutua ou afunda?", None, ("se dissolve", "fica no meio da água")),
           ("Condutor ou isolante", {"os bons condutores de calor": ["o alumínio", "o cobre", "o ferro", "a prata", "o aço inoxidável", "o ouro", "o bronze"],
                                     "os isolantes térmicos": ["o isopor", "a lã", "a madeira", "a borracha", "o plástico", "a cortiça", "o algodão"]})],
          ["Os metais conduzem calor.", "O ímã atrai o ferro.", "O óleo flutua na água.", "O isopor é isolante térmico.", "O diamante risca o vidro.",
           "A borracha é elástica.", "O cobre conduz eletricidade."],
          [("O ímã atrai o alumínio.", "O ímã não atrai alumínio."), ("O plástico conduz bem a eletricidade.", "O plástico é isolante."), ("A pedra flutua na água.", "A pedra afunda."),
           ("O vidro risca o diamante.", "O diamante é mais duro."), ("O isopor conduz muito calor.", "O isopor é isolante.")],
          "as propriedades dos materiais", "matter"),

        H("M", "ciclo-da-agua", ["EF05CI02", "EF05CI03"], "O ciclo da água e a vegetação", "Ciclo da água",
          "Aplicar os conhecimentos sobre as mudanças de estado físico da água para explicar o ciclo hidrológico e analisar suas implicações na agricultura, no clima, na geração de energia elétrica, no provimento de água potável e no equilíbrio dos ecossistemas regionais (ou locais); selecionar argumentos que justifiquem a importância da cobertura vegetal para a manutenção do ciclo da água, a conservação dos solos, dos cursos de água e da qualidade do ar atmosférico.",
          "evaporação, condensação, precipitação, infiltração, transpiração das plantas e rios voadores",
          "Evaporação, condensação, precipitação", "A vegetação mantém o ciclo da água e protege o solo.",
          ["O Sol aquece a água de rios e mares, que evapora. O vapor sobe, esfria e condensa em gotinhas que formam as nuvens.",
           "As gotas se juntam e caem como chuva (precipitação). A água infiltra no solo ou escorre para os rios.",
           "As plantas também soltam vapor (transpiração). A Floresta Amazônica forma os rios voadores que levam chuva para outras regiões."],
          [("Que mudança de estado forma as nuvens?", ["O vapor de água sobe e esfria.", "Vapor que vira líquido é condensação."], "A condensação.")],
          [("As nuvens são fumaça.", "São gotinhas de água ou cristais de gelo."), ("A água da chuva some do planeta.", "Ela continua circulando no ciclo.")],
          [("O que são os rios voadores?", "Massas de vapor de água vindas da Amazônia que levam umidade e chuva para o Centro-Oeste e o Sudeste."), ("Por que desmatar seca os rios?", "Sem plantas, a água escorre, o solo erode e menos água infiltra e evapora pelas folhas.")],
          [("Etapas", [("a evaporação", "a água líquida vira vapor com o calor do Sol"), ("a condensação", "o vapor esfria e vira gotinhas nas nuvens"), ("a precipitação", "a água cai das nuvens como chuva ou granizo"),
                       ("a infiltração", "a água da chuva penetra no solo"), ("a transpiração das plantas", "as folhas soltam vapor de água"), ("o escoamento", "a água corre pela superfície até os rios"),
                       ("a solidificação", "a água líquida vira gelo"), ("a fusão", "o gelo vira água líquida")],
            "O que acontece em {k}?", D),
           ("Importância", [("a hidrelétrica", "usa a força da água dos rios para gerar eletricidade"), ("a irrigação", "leva água às plantações"),
                            ("a estação de tratamento", "torna a água potável"), ("a mata ciliar", "protege as margens dos rios"), ("os aquíferos", "guardam água embaixo da terra"),
                            ("os rios voadores", "levam umidade da Amazônia para outras regiões"), ("o reflorestamento", "ajuda a água a infiltrar no solo"), ("a cisterna", "guarda a água da chuva")],
            "Qual é a importância de {k}?", D),
           ("Estados", {"a água no estado sólido": ["o gelo", "o granizo", "a neve", "a geada", "o iceberg"], "a água no estado líquido": ["a chuva", "o orvalho", "o rio", "o mar", "a garoa"],
                        "a água no estado gasoso": ["o vapor da chaleira", "a umidade do ar", "o vapor que sai das folhas", "o vapor da evaporação do mar", "o vapor do banho quente"]})],
          ["As nuvens se formam por condensação.", "A chuva é uma precipitação.", "As plantas soltam vapor pelas folhas.", "A vegetação protege o solo da erosão.",
           "Os rios voadores saem da Amazônia.", "A hidrelétrica usa a água para gerar eletricidade.", "O Sol aquece a água e provoca a evaporação."],
          [("As nuvens são fumaça.", "São gotinhas de água."), ("A evaporação acontece só nos mares.", "Rios, lagos, solo e plantas também perdem água."),
           ("Desmatar aumenta as chuvas.", "Desmatar diminui a umidade e as chuvas."), ("O granizo é água gasosa.", "O granizo é gelo."),
           ("A água da chuva é sempre potável.", "Ela pode ter sujeira e precisa de tratamento.")],
          "o ciclo da água", "earths-systems"),

        H("M", "consumo-consciente-e-reciclagem", ["EF05CI04", "EF05CI05"], "Consumo consciente e reciclagem", "Consumo e reciclagem",
          "Identificar os principais usos da água e de outros materiais nas atividades cotidianas para discutir e propor formas sustentáveis de utilização desses recursos; construir propostas coletivas para um consumo mais consciente e criar soluções tecnológicas para o descarte adequado e a reutilização ou reciclagem de materiais consumidos na escola e/ou na vida cotidiana.",
          "uso da água, reduzir, reutilizar e reciclar, coleta seletiva e cores das lixeiras",
          "Reduzir, reutilizar, reciclar", "Na coleta seletiva: azul papel, vermelho plástico, verde vidro, amarelo metal.",
          ["Reduzir é consumir menos; reutilizar é usar de novo; reciclar é transformar o material usado em um novo produto.",
           "Na coleta seletiva, cada cor de lixeira recebe um material: azul (papel), vermelho (plástico), verde (vidro), amarelo (metal), marrom (orgânico).",
           "Banhos curtos, torneira fechada e conserto de vazamentos economizam água."],
          [("Em que lixeira vai a lata de refrigerante?", ["A lata é de alumínio.", "Metal vai na amarela."], "Na amarela.")],
          [("Reciclar e reutilizar são a mesma coisa.", "Reutilizar é usar de novo; reciclar transforma o material."), ("Restos de comida vão na lixeira azul.", "Vão para o orgânico (marrom) ou para a compostagem.")],
          [("O que é compostagem?", "Transformar restos de comida e folhas em adubo."), ("Por que separar o lixo?", "Para que os materiais possam ser reciclados e não fiquem no aterro.")],
          [("Lixeira", [("o jornal velho", "azul"), ("a garrafa PET", "vermelha"), ("o pote de vidro", "verde"), ("a lata de alumínio", "amarela"), ("a casca de banana", "marrom"),
                        ("a caixa de papelão", "azul"), ("o copo plástico", "vermelha"), ("a garrafa de vidro", "verde"), ("a tampinha de metal", "amarela"), ("o resto de comida", "marrom")],
            "Em que cor de lixeira vai {k}?", None, ("preta",)),
           ("Os 3 R", [("usar a garrafa PET como vaso de planta", "reutilizar"), ("transformar latinhas em novas latas", "reciclar"), ("levar sacola de pano ao mercado", "reduzir"),
                       ("comprar só o necessário", "reduzir"), ("fazer papel novo com papel usado", "reciclar"), ("usar o verso da folha para rascunho", "reutilizar"),
                       ("fechar a torneira ao escovar os dentes", "reduzir"), ("derreter vidro velho para fazer garrafas", "reciclar"), ("doar roupas que não servem mais", "reutilizar")],
            "Qual dos 3 R é {k}?", None, ("descartar",)),
           ("Atitudes", {"as atitudes que economizam água": ["tomar banho curto", "consertar vazamentos", "reaproveitar a água da chuva", "fechar a torneira ao ensaboar a louça", "usar balde para lavar o carro", "usar a água da máquina de lavar para limpar o quintal", "regar as plantas no fim da tarde"],
                         "as atitudes que desperdiçam água": ["lavar a calçada com mangueira", "deixar a torneira pingando", "banho de meia hora", "escovar os dentes com a torneira aberta", "regar plantas ao meio-dia", "deixar a mangueira aberta no jardim", "lavar a louça com a torneira sempre aberta"]})],
          ["A lixeira azul recebe papel.", "A lixeira verde recebe vidro.", "Reciclar transforma o material usado.", "Banhos curtos economizam água.", "A compostagem transforma restos de comida em adubo.",
           "Reutilizar é usar de novo.", "Consertar vazamentos evita desperdício."],
          [("A lixeira azul recebe vidro.", "Recebe papel."), ("Reciclar é jogar no lixo comum.", "Reciclar é transformar em produto novo."), ("Lavar a calçada com mangueira economiza água.", "Desperdiça muita água."),
           ("A lata de alumínio vai na lixeira verde.", "Vai na amarela."), ("Reutilizar é o mesmo que reciclar.", "São coisas diferentes.")],
          "o consumo consciente", "earths-systems", calc=f_agua, s4="Calcule a água"),

        H("V", "digestao-e-respiracao", ["EF05CI06"], "Sistemas digestório e respiratório", "Digestão e respiração",
          "Selecionar argumentos que justifiquem por que os sistemas digestório e respiratório são considerados corresponsáveis pelo processo de nutrição do organismo, com base na identificação das funções desses sistemas.",
          "boca, esôfago, estômago, intestinos, nutrientes, nariz, traqueia, pulmões, alvéolos e trocas gasosas",
          "Nutrientes e oxigênio chegam às células", "O sistema digestório fornece nutrientes; o respiratório, oxigênio.",
          ["No sistema digestório o alimento passa por boca, esôfago, estômago, intestino delgado e intestino grosso. No intestino delgado os nutrientes passam para o sangue.",
           "No sistema respiratório o ar entra pelo nariz, passa pela faringe, laringe, traqueia e brônquios até os alvéolos dos pulmões, onde o oxigênio entra no sangue.",
           "As células usam os nutrientes e o oxigênio para obter energia. Por isso os dois sistemas trabalham juntos na nutrição."],
          [("Onde os nutrientes passam para o sangue?", ["O estômago mistura o alimento com o suco gástrico.", "O intestino delgado absorve os nutrientes."], "No intestino delgado.")],
          [("A digestão acontece só no estômago.", "Começa na boca e termina no intestino."), ("Expiramos só gás oxigênio.", "Expiramos mais gás carbônico.")],
          [("Por que mastigar bem?", "Pedaços menores são digeridos mais facilmente, e a saliva já começa a digestão."), ("Para que serve o diafragma?", "É o músculo que ajuda o ar a entrar e sair dos pulmões.")],
          [("Órgãos", [("a boca", "mastiga e começa a digestão com a saliva"), ("o esôfago", "leva o alimento até o estômago"), ("o estômago", "mistura o alimento com o suco gástrico"),
                       ("o intestino delgado", "absorve os nutrientes"), ("o intestino grosso", "absorve água e forma as fezes"), ("o fígado", "produz a bile"),
                       ("a traqueia", "leva o ar até os brônquios"), ("os alvéolos", "trocam oxigênio e gás carbônico com o sangue"), ("o diafragma", "ajuda o ar a entrar e sair")],
            "Qual é a função de {k}?", D),
           ("Caminho", [("o nariz", "a primeira parte por onde o ar entra"), ("a faringe", "o canal comum ao ar e ao alimento"), ("a laringe", "onde ficam as pregas vocais"),
                        ("os brônquios", "os tubos que levam o ar a cada pulmão"), ("os pulmões", "os órgãos onde estão os alvéolos"), ("a epiglote", "a tampa que impede o alimento de ir para a traqueia"),
                        ("o ânus", "por onde saem as fezes"), ("as glândulas salivares", "produzem a saliva")],
            "O que é {k}?", D),
           ("Sistemas", {"o sistema digestório": ["o esôfago", "o estômago", "o intestino delgado", "o fígado", "o pâncreas"],
                         "o sistema respiratório": ["a traqueia", "os brônquios", "os pulmões", "a laringe", "os alvéolos"],
                         "o que as células recebem para obter energia": ["o oxigênio", "a glicose", "os nutrientes absorvidos", "a água", "os sais minerais"]})],
          ["A digestão começa na boca.", "O intestino delgado absorve nutrientes.", "O oxigênio entra no sangue nos alvéolos.", "O fígado produz a bile.",
           "O diafragma ajuda na respiração.", "Expiramos gás carbônico.", "Os dois sistemas participam da nutrição."],
          [("A digestão começa no estômago.", "Começa na boca."), ("O esôfago absorve os nutrientes.", "Quem absorve é o intestino delgado."), ("Expiramos só oxigênio.", "Expiramos mais gás carbônico."),
           ("A traqueia leva o alimento ao estômago.", "Ela leva o ar aos brônquios."), ("O intestino grosso produz a saliva.", "A saliva vem das glândulas salivares.")],
          "a digestão e a respiração", "living-things-and-ecosystems"),

        H("V", "circulacao-e-excrecao", ["EF05CI07"], "Sistemas circulatório e urinário", "Circulação e excreção",
          "Justificar a relação entre o funcionamento do sistema circulatório, a distribuição dos nutrientes pelo organismo e a eliminação dos resíduos produzidos.",
          "coração, artérias, veias, capilares, sangue, rins, urina e suor",
          "O sangue leva e traz", "O coração bombeia o sangue; os rins filtram o sangue e formam a urina.",
          ["O coração é um músculo que bombeia o sangue. As artérias levam o sangue do coração para o corpo; as veias trazem de volta.",
           "O sangue leva oxigênio e nutrientes às células e recolhe os resíduos, como o gás carbônico e a ureia.",
           "Os rins filtram o sangue e formam a urina, que fica na bexiga até ser eliminada. A pele também elimina resíduos pelo suor."],
          [("Que órgão filtra o sangue?", ["O sangue passa pelos rins.", "Eles retiram resíduos e formam a urina."], "Os rins.")],
          [("As veias levam sangue do coração ao corpo.", "Quem faz isso são as artérias."), ("A urina se forma na bexiga.", "Ela se forma nos rins; a bexiga só guarda.")],
          [("Por que o coração bate mais rápido na corrida?", "Os músculos precisam de mais oxigênio e nutrientes."), ("O que fazem os glóbulos brancos?", "Defendem o corpo contra microrganismos.")],
          [("Funções", [("o coração", "bombeia o sangue"), ("as artérias", "levam o sangue do coração para o corpo"), ("as veias", "trazem o sangue de volta ao coração"),
                        ("os capilares", "vasos finos onde ocorrem as trocas com as células"), ("os rins", "filtram o sangue e formam a urina"), ("a bexiga", "armazena a urina"),
                        ("os ureteres", "levam a urina dos rins à bexiga"), ("a uretra", "leva a urina para fora do corpo"), ("as glândulas sudoríparas", "produzem o suor")],
            "Qual é a função de {k}?", D),
           ("Sangue", [("os glóbulos vermelhos", "transportam oxigênio"), ("os glóbulos brancos", "defendem o corpo"), ("as plaquetas", "ajudam a estancar sangramentos"),
                       ("o plasma", "a parte líquida do sangue"), ("o gás carbônico", "resíduo levado aos pulmões"), ("a ureia", "resíduo eliminado na urina"),
                       ("a glicose", "nutriente que dá energia às células")],
            "O que é ou o que faz {k}?", D),
           ("Sistema", {"o sistema circulatório": ["o coração", "as artérias", "as veias", "os capilares", "o sangue"], "o sistema urinário": ["os rins", "a bexiga", "os ureteres", "a uretra", "a urina"],
                        "os hábitos que ajudam esses sistemas": ["beber água", "praticar exercícios", "comer pouco sal", "não segurar a urina por muito tempo", "dormir bem"]})],
          ["O coração bombeia o sangue.", "As artérias saem do coração.", "Os rins formam a urina.", "A bexiga armazena a urina.", "Os glóbulos brancos defendem o corpo.",
           "As plaquetas ajudam a estancar sangramentos.", "O suor também elimina resíduos."],
          [("As veias saem do coração.", "As veias chegam ao coração."), ("A urina se forma na bexiga.", "Forma-se nos rins."), ("Os glóbulos brancos transportam oxigênio.", "Isso é feito pelos glóbulos vermelhos."),
           ("O coração é um osso.", "O coração é um músculo."), ("Os rins produzem o sangue.", "Os rins filtram o sangue.")],
          "a circulação e a excreção", "living-things-and-ecosystems"),

        H("V", "alimentacao-saudavel", ["EF05CI08", "EF05CI09"], "Alimentação saudável", "Alimentação saudável",
          "Organizar um cardápio equilibrado com base nas características dos grupos alimentares (nutrientes e calorias) e nas necessidades individuais (atividades realizadas, idade, sexo etc.) para a manutenção da saúde do organismo; discutir a ocorrência de distúrbios nutricionais (como obesidade, subnutrição etc.) entre crianças e jovens.",
          "carboidratos, proteínas, gorduras, vitaminas e minerais, calorias, alimentos ultraprocessados e distúrbios nutricionais",
          "Um prato variado e equilibrado", "Prefira alimentos naturais; evite ultraprocessados com muito açúcar, sal e gordura.",
          ["Os alimentos têm nutrientes: carboidratos dão energia, proteínas constroem o corpo, gorduras guardam energia, vitaminas e minerais regulam o organismo.",
           "A energia dos alimentos é medida em quilocalorias (kcal). Quem se movimenta mais gasta mais energia.",
           "O Guia Alimentar para a População Brasileira recomenda alimentos in natura, como arroz, feijão, frutas e verduras, e evitar ultraprocessados."],
          [("Que nutriente predomina no feijão?", ["O feijão é uma leguminosa.", "As leguminosas são ricas em proteínas."], "Proteínas (além de fibras e ferro).")],
          [("Gordura nenhuma faz bem.", "Um pouco de gordura é necessário."), ("Suco de caixinha é igual à fruta.", "Muitos têm açúcar e pouca fibra.")],
          [("O que é alimento ultraprocessado?", "Produto industrial com muitos aditivos, açúcar, sal ou gordura, como salgadinho e refrigerante."), ("O que é subnutrição?", "Falta de nutrientes ou de energia por comer pouco ou mal.")],
          [("Nutriente", [("o arroz", "carboidratos"), ("o pão", "carboidratos"), ("a mandioca", "carboidratos"), ("o feijão", "proteínas"), ("o ovo", "proteínas"), ("a carne", "proteínas"),
                          ("o óleo", "gorduras"), ("a manteiga", "gorduras"), ("a laranja", "vitaminas"), ("o leite", "cálcio"), ("a couve", "ferro e fibras")],
            "Que nutriente predomina em {k}?", None),
           ("Função", [("os carboidratos", "fornecem energia rápida"), ("as proteínas", "constroem e reparam o corpo"), ("as gorduras", "armazenam energia"),
                       ("as vitaminas", "regulam o funcionamento do corpo"), ("o cálcio", "fortalece ossos e dentes"), ("o ferro", "ajuda a formar o sangue"),
                       ("as fibras", "ajudam o intestino a funcionar"), ("a água", "mantém o corpo hidratado")],
            "Qual é a função de {k}?", D),
           ("Escolhas", {"os alimentos in natura ou minimamente processados": ["a banana", "o feijão", "o arroz", "o ovo", "a cenoura", "o leite", "a castanha"],
                         "os alimentos ultraprocessados": ["o refrigerante", "o salgadinho de pacote", "o biscoito recheado", "o macarrão instantâneo", "a salsicha", "o nugget", "o suco em pó"]})],
          ["O feijão é rico em proteínas.", "O arroz é rico em carboidratos.", "O cálcio fortalece os ossos.", "As fibras ajudam o intestino.", "A energia dos alimentos é medida em quilocalorias.",
           "O refrigerante é ultraprocessado.", "Quem se exercita gasta mais energia."],
          [("O óleo é rico em proteínas.", "É rico em gorduras."), ("Refrigerante é alimento in natura.", "É ultraprocessado."), ("Comer só doces é equilibrado.", "O cardápio precisa ser variado."),
           ("As vitaminas dão a maior parte da energia.", "A energia vem sobretudo de carboidratos e gorduras."), ("Subnutrição é comer demais.", "É falta de nutrientes.")],
          "a alimentação", "living-things-and-ecosystems", calc=f_kcal, s4="Calcule as calorias"),

        H("T", "constelacoes-e-movimentos-da-terra", ["EF05CI10", "EF05CI11"], "Constelações e movimentos da Terra", "Constelações",
          "Identificar algumas constelações no céu, com o apoio de recursos (como mapas celestes e aplicativos digitais, entre outros), e os períodos do ano em que elas são visíveis no início da noite; associar o movimento diário do Sol e das demais estrelas no céu ao movimento de rotação da Terra.",
          "constelações, Cruzeiro do Sul, Órion, mapa celeste, rotação da Terra e movimento aparente das estrelas",
          "As estrelas parecem girar porque a Terra gira", "O Cruzeiro do Sul aponta o sul; constelações mudam ao longo do ano.",
          ["Constelação é um grupo de estrelas que, vistas da Terra, formam um desenho. O Cruzeiro do Sul, as Três Marias (em Órion) e o Escorpião são bem visíveis no Brasil.",
           "O Sol e as estrelas parecem se mover no céu de leste para oeste porque a Terra gira de oeste para leste (rotação).",
           "Como a Terra também gira em volta do Sol (translação), as constelações visíveis no começo da noite mudam ao longo do ano."],
          [("Por que vemos o Sol nascer a leste?", ["A Terra gira de oeste para leste.", "Por isso o Sol parece surgir no lado leste."], "Por causa da rotação da Terra.")],
          [("As estrelas de uma constelação estão todas perto umas das outras.", "Só parecem próximas vistas da Terra."), ("O Sol gira em volta da Terra.", "É a Terra que gira em volta do Sol.")],
          [("Como achar o sul pelo Cruzeiro do Sul?", "Prolongue o braço maior da cruz cerca de quatro vezes e meia: perto dali fica o polo sul celeste."), ("O Sol é uma estrela?", "Sim, é a estrela mais próxima da Terra.")],
          [("Constelações", [("o Cruzeiro do Sul", "ajuda a achar o polo sul celeste"), ("as Três Marias", "três estrelas em linha no cinturão de Órion"), ("o Escorpião", "tem uma estrela vermelha, Antares"),
                             ("Órion", "a constelação do caçador"), ("a Ursa Maior", "é vista no hemisfério norte"), ("Sirius", "a estrela mais brilhante do céu noturno"),
                             ("a Via Láctea", "a nossa galáxia, vista como uma faixa clara"), ("o mapa celeste", "mostra as constelações visíveis em uma data e hora")],
            "O que é ou o que tem {k}?", D),
           ("Movimentos", [("a rotação", "a Terra gira em torno de si mesma"), ("a translação", "a Terra gira em torno do Sol"), ("o dia e a noite", "acontecem por causa da rotação"),
                           ("o movimento aparente do Sol", "parece ir de leste para oeste"), ("o eixo da Terra", "é inclinado"), ("o ano", "tempo de uma volta em torno do Sol"),
                           ("as estações do ano", "resultam da translação e da inclinação do eixo")],
            "O que é ou o que explica {k}?", D),
           ("Astros", {"as estrelas": ["o Sol", "Sirius", "Antares", "Betelgeuse", "Alfa Centauri"], "os planetas": ["Vênus", "Marte", "Júpiter", "Saturno", "Mercúrio"],
                       "os satélites naturais": ["a Lua", "Europa", "Titã", "Ganimedes", "Io"]})],
          ["O Cruzeiro do Sul ajuda a achar o sul.", "As Três Marias ficam em Órion.", "O dia e a noite resultam da rotação.", "O Sol é uma estrela.", "A Terra gira de oeste para leste.",
           "Sirius é a estrela mais brilhante do céu noturno.", "As constelações visíveis mudam ao longo do ano."],
          [("O Sol gira em volta da Terra.", "A Terra gira em volta do Sol."), ("O Cruzeiro do Sul aponta o norte.", "Aponta o sul."), ("A Lua é uma estrela.", "A Lua é um satélite."),
           ("O dia e a noite vêm da translação.", "Vêm da rotação."), ("As constelações são as mesmas a noite toda e o ano todo.", "Elas se movem no céu e mudam com as estações.")],
          "as constelações e os movimentos da Terra", "earth-and-space"),

        H("T", "fases-da-lua-e-instrumentos-opticos", ["EF05CI12", "EF05CI13"], "Fases da Lua e instrumentos ópticos", "Lua e instrumentos",
          "Concluir sobre a periodicidade das fases da Lua, com base na observação e no registro das formas aparentes da Lua no céu ao longo de, pelo menos, dois meses; projetar e construir dispositivos para observação à distância (luneta, periscópio etc.), para observação ampliada de objetos (lupas, microscópios) ou para registro de imagens (máquinas fotográficas) e discutir usos sociais desses dispositivos.",
          "lua nova, crescente, cheia e minguante, periodicidade, luneta, telescópio, microscópio, lupa e periscópio",
          "Nova, crescente, cheia, minguante", "O ciclo das fases dura cerca de 29 dias e meio; lentes ampliam imagens.",
          ["A Lua não tem luz própria: ela reflete a luz do Sol. Conforme gira em volta da Terra, vemos partes diferentes da face iluminada.",
           "As fases são lua nova, quarto crescente, lua cheia e quarto minguante. O ciclo completo dura cerca de 29 dias e meio.",
           "Instrumentos ópticos usam lentes e espelhos: a lupa e o microscópio ampliam objetos pequenos; a luneta e o telescópio aproximam objetos distantes; o periscópio usa espelhos para ver por cima de obstáculos."],
          [("Se hoje é lua cheia, quando será a próxima lua cheia?", ["O ciclo completo dura cerca de 29 dias e meio.", "Depois de um ciclo a fase se repete."], "Em cerca de 29 ou 30 dias.")],
          [("A Lua tem luz própria.", "Ela reflete a luz do Sol."), ("As fases são a sombra da Terra na Lua.", "A sombra da Terra na Lua é o eclipse; as fases dependem da posição da Lua.")],
          [("Quem usou a luneta para observar a Lua?", "Galileu Galilei, em 1609, viu crateras e montanhas na Lua."), ("Para que serve o microscópio?", "Para ver células, microrganismos e outros objetos muito pequenos.")],
          [("Fases", [("a lua nova", "a face iluminada fica voltada para o Sol e quase não a vemos"), ("a lua cheia", "vemos toda a face iluminada"),
                      ("o quarto crescente", "a parte iluminada aumenta noite após noite"), ("o quarto minguante", "a parte iluminada diminui noite após noite"),
                      ("o ciclo lunar", "dura cerca de 29 dias e meio"), ("a luz da Lua", "é luz do Sol refletida")],
            "O que caracteriza {k}?", D, ("a Lua some do céu para sempre",)),
           ("Instrumentos", [("a lupa", "amplia objetos próximos com uma lente"), ("o microscópio", "permite ver células e microrganismos"), ("a luneta", "aproxima objetos distantes"),
                             ("o telescópio", "observa astros muito distantes"), ("o periscópio", "usa espelhos para ver por cima de obstáculos"), ("a câmera fotográfica", "registra imagens"),
                             ("os óculos", "corrigem problemas de visão"), ("o binóculo", "aproxima objetos distantes com os dois olhos")],
            "Para que serve {k}?", D),
           ("Uso", {"os instrumentos para ver o que está longe": ["a luneta", "o telescópio", "o binóculo", "a luneta astronômica", "o telescópio espacial"],
                    "os instrumentos para ver o que é muito pequeno": ["a lupa", "o microscópio", "o microscópio eletrônico", "a lente de aumento do relojoeiro", "a lupa de mão do cientista"],
                    "as fases da Lua": ["lua nova", "quarto crescente", "lua cheia", "quarto minguante", "lua gibosa"]})],
          ["A Lua reflete a luz do Sol.", "O ciclo das fases dura cerca de 29 dias e meio.", "Na lua cheia vemos toda a face iluminada.", "O microscópio amplia células.",
           "A luneta aproxima objetos distantes.", "O periscópio usa espelhos.", "Galileu observou a Lua com uma luneta."],
          [("A Lua tem luz própria.", "Ela reflete a luz do Sol."), ("O ciclo lunar dura 7 dias.", "Dura cerca de 29 dias e meio."), ("O telescópio serve para ver células.", "Para células usamos o microscópio."),
           ("Na lua nova vemos a Lua inteira iluminada.", "Isso é a lua cheia."), ("O periscópio funciona sem espelhos.", "Ele usa espelhos.")],
          "a Lua e os instrumentos ópticos", "earth-and-space"),
    ]
