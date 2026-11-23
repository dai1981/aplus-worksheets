# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Problemas de contagem (Números, EF05MA09)
  python3 tools/gen_br_matematica_5_problemas_de_contagem.py
Princípio multiplicativo: combinar elementos de duas ou três coleções (roupas, lanches, caminhos);
árvore de possibilidades e tabela de dupla entrada; formar números e senhas com algarismos (com e sem repetição); problemas.
Erros: somar em vez de multiplicar (3 camisetas e 4 bermudas → 7), esquecer uma coleção, repetir algarismos quando não pode.
"""
import random
from itertools import product
from br_common import mcq, lesson, make_unit, mix, wrap, text, line, INK, GREEN, table, Kids, pl

R = random.Random(80511)
K = Kids(R)

GRUPOS = [
    (("camiseta", "camisetas", ["branca", "azul", "verde", "amarela", "preta", "vermelha"]), ("bermuda", "bermudas", ["jeans", "cinza", "marrom", "preta", "azul"]), "maneiras diferentes de se vestir"),
    (("sabor de sorvete", "sabores de sorvete", ["chocolate", "morango", "creme", "coco", "manga", "limão"]), ("cobertura", "coberturas", ["caramelo", "chocolate", "morango", "leite condensado"]), "sorvetes diferentes com 1 sabor e 1 cobertura"),
    (("tipo de pão", "tipos de pão", ["francês", "de forma", "integral", "de queijo"]), ("recheio", "recheios", ["queijo", "presunto", "frango", "ovo", "requeijão"]), "sanduíches diferentes com 1 pão e 1 recheio"),
    (("prato", "pratos", ["arroz com feijão", "macarrão", "peixe", "frango", "salada"]), ("suco", "sucos", ["laranja", "uva", "caju", "maracujá", "acerola"]), "refeições diferentes com 1 prato e 1 suco"),
    (("caminho de casa até a praça", "caminhos de casa até a praça", None), ("caminho da praça até a escola", "caminhos da praça até a escola", None), "caminhos diferentes de casa até a escola, passando pela praça"),
]
TERCEIRO = {0: ("par de tênis", "pares de tênis"), 1: ("tipo de casquinha", "tipos de casquinha"), 2: ("bebida", "bebidas"), 3: ("sobremesa", "sobremesas")}


def arvore(a_labels, b_labels):
    """árvore de possibilidades: raiz → a ramos → b folhas cada"""
    n = len(a_labels) * len(b_labels)
    rowh = 24
    H = n * rowh + 16
    s = []
    ys = []
    for i, a in enumerate(a_labels):
        y0 = 8 + i * len(b_labels) * rowh
        ya = y0 + len(b_labels) * rowh / 2
        s.append(line(20, H / 2, 120, ya - 4, INK, 1.4))
        s.append(text(124, ya, a, 13, anchor="start"))
        for j, b in enumerate(b_labels):
            yb = y0 + j * rowh + rowh / 2 + 4
            s.append(line(220, ya - 4, 300, yb - 4, GREEN, 1.2))
            s.append(text(304, yb, b, 13, anchor="start"))
            ys.append(yb)
    s.append("<circle cx='18' cy='%.1f' r='4' fill='%s'/>" % (H / 2, INK))
    return wrap(420, H, "".join(s), "árvore de possibilidades com %d ramos de %d" % (len(a_labels), len(b_labels)))


def s1_dois():
    g = R.randrange(len(GRUPOS))
    (s1, p1, l1), (s2, p2, l2), what = GRUPOS[g]
    a = R.randint(2, 6 if l1 is None else len(l1))
    b = R.randint(2, 5 if l2 is None else len(l2))
    if a * b < 6:
        return None
    if l1 is None:
        q = "Há %s e %s. Quantos são os %s?" % (pl(a, s1, p1), pl(b, s2, p2), what)
    else:
        q = "%s tem %s e %s. Quantas são as %s?" % (K.next()[0], pl(a, s1, p1), pl(b, s2, p2), what) if g == 0 else \
            "Uma lanchonete oferece %s e %s. %s %s ela pode montar?" % (pl(a, s1, p1), pl(b, s2, p2), "Quantas" if what.startswith("refeições") else "Quantos", what)
    return mcq(q, str(a * b), [str(a + b), str(a * b + a), str(a * b - b) if a * b - b != a + b else str(a * b * 2)],
               "Para cada um dos %d, há %d escolhas: %d × %d = <b>%d</b>." % (a, b, a, b, a * b))


def s1_tabela():
    a = R.randint(2, 4)
    b = R.randint(2, 4)
    if a * b < 6:
        return None
    L1 = sorted(R.sample(["A", "B", "C", "D"], a))
    L2 = [str(x) for x in range(1, b + 1)]
    rows = [[x] + [x + y for y in L2] for x in L1]
    tb = table([""] + L2, rows)
    hide = R.choice(["linha", "total"])
    if hide == "total":
        return mcq(tb + "Uma rifa combina uma letra (%s) com um número (%s), como na tabela. Quantos bilhetes diferentes existem?" % (", ".join(L1), ", ".join(L2)),
                   str(a * b), [str(a + b), str(a * b + 1), str(a * b * 2)], "%d letras × %d números = <b>%d</b> bilhetes." % (a, b, a * b))
    x = R.choice(L1)
    return mcq(tb + "Na tabela, quantos bilhetes começam com a letra %s?" % x, str(b), [str(a), str(a * b), str(b + 1), str(a + b), str(b * 2)],
               "A linha da letra %s tem um bilhete para cada número: <b>%d</b>." % (x, b))


def s2_arvore():
    g = R.choice([0, 1, 3])
    (s1, p1, l1), (s2, p2, l2), what = GRUPOS[g]
    a = R.randint(2, 3)
    b = R.randint(2, 4)
    if a * b < 6:
        return None
    A, B = R.sample(l1, a), R.sample(l2, b)
    k = R.choice(["total", "com"])
    pic = arvore(A, B)
    if k == "total":
        return mcq(pic + "A árvore mostra as combinações de %s com %s. Quantas são as possibilidades?" % (p1, p2), str(a * b), [str(a + b), str(a * b + b), str(b), str(a * b - 1), str(a * b + 1)],
                   "%d ramos, cada um com %d: %d × %d = <b>%d</b>." % (a, b, a, b, a * b))
    x = R.choice(A)
    return mcq(pic + "Na árvore, quantas possibilidades têm «%s»?" % x, str(b), [str(a), str(a * b), str(a + b), str(b + 1), str(b * 2), str(b - 1) if b > 2 else str(b + 2)],
               "Do ramo «%s» saem <b>%d</b> possibilidades, uma para cada %s." % (x, b, s2))


def s2_lista():
    g = R.choice([0, 1, 2, 3])
    (s1, p1, l1), (s2, p2, l2), what = GRUPOS[g]
    A, B = R.sample(l1, 2), R.sample(l2, 2)
    good = "; ".join("%s e %s" % (x, y) for x, y in product(A, B))
    w1 = "; ".join("%s e %s" % (x, y) for x, y in [(A[0], B[0]), (A[1], B[1])])
    w2 = "; ".join("%s e %s" % (x, y) for x, y in [(A[0], B[0]), (A[0], B[1]), (A[1], B[0])])
    w3 = "; ".join([A[0], A[1], B[0], B[1]])
    return mcq("Com %s (%s) e %s (%s), qual lista mostra <b>todas</b> as combinações?" % (pl(2, s1, p1), " ou ".join(A), pl(2, s2, p2), " ou ".join(B)), good, [w1, w2, w3],
               "Combine cada %s com cada %s: 2 × 2 = 4. <b>%s</b>." % (s1, s2, good))


def s3_tres():
    g = R.choice([0, 1, 2, 3])
    (s1, p1, _), (s2, p2, _), what = GRUPOS[g]
    s3, p3 = TERCEIRO[g]
    a, b, c = R.randint(2, 5), R.randint(2, 4), R.randint(2, 3)
    return mcq("É possível escolher entre %s, %s e %s. Quantas combinações diferentes, com um de cada, existem?" % (pl(a, s1, p1), pl(b, s2, p2), pl(c, s3, p3)), str(a * b * c),
               [str(a + b + c), str(a * b), str(a * b + c), str(a * b * c + c)],
               "Multiplique as três quantidades: %d × %d × %d = <b>%d</b>." % (a, b, c, a * b * c))


def s3_falta():
    g = R.choice([1, 2, 3])
    (s1, p1, l1), (s2, p2, l2), what = GRUPOS[g]
    a, b = R.randint(2, 6), R.randint(2, 6)
    if a * b < 6:
        return None
    return mcq("Com %s e algumas opções de %s, dá para formar %d %s. Quantas são as opções de %s?" % (pl(a, s1, p1), s2, a * b, what.split(" com ")[0] if " com " in what else what, s2),
               str(b), [str(a * b - a), str(a), str(a * b // 2), str(b + 1), str(a * b + a), str(a * b - 1)],
               "%d × ? = %d → %d ÷ %d = <b>%d</b>." % (a, a * b, a * b, a, b))


def s4_numeros():
    k = R.choice(["sem", "com", "par", "senha"])
    ds = sorted(R.sample(range(1, 10), R.choice([3, 4])))
    n = len(ds)
    lst = ", ".join(str(x) for x in ds)
    if k == "sem":
        return mcq("Quantos números de 2 algarismos <b>diferentes</b> podemos formar com os algarismos %s?" % lst, str(n * (n - 1)), [str(n * n), str(n + n - 1), str(n * (n - 1) // 2)],
                   "Para as dezenas há %d escolhas; para as unidades sobram %d. %d × %d = <b>%d</b>." % (n, n - 1, n, n - 1, n * (n - 1)))
    if k == "com":
        return mcq("Quantos números de 2 algarismos podemos formar com os algarismos %s, <b>podendo repetir</b>?" % lst, str(n * n), [str(n * (n - 1)), str(n + n), str(n * n * n), str(n * (n - 1) // 2), str(n * n + n)],
                   "%d escolhas para as dezenas e %d para as unidades: %d × %d = <b>%d</b>." % (n, n, n, n, n * n))
    if k == "par":
        ev = [x for x in ds if x % 2 == 0]
        if not ev or len(ev) == n:
            return None
        return mcq("Com os algarismos %s, sem repetir, quantos números de 2 algarismos são <b>pares</b>?" % lst, str(len(ev) * (n - 1)), [str(n * (n - 1)), str(len(ev)), str(len(ev) * n), str(n * n), str(len(ev) * (n - 1) + 1)],
                   "A unidade tem que ser par: %d escolhas (%s). Para as dezenas sobram %d. %d × %d = <b>%d</b>." % (len(ev), ", ".join(map(str, ev)), n - 1, len(ev), n - 1, len(ev) * (n - 1)))
    m = R.choice([2, 3])
    return mcq("Uma senha tem %d algarismos e cada um pode ser %s (podendo repetir). Quantas senhas diferentes existem?" % (m, lst), str(n ** m), [str(n * m), str(n + m), str(n ** (m - 1)), str(n * (n - 1) * (n - 2) if m == 3 else n * (n - 1)), str(n ** m - 1)],
               "%s = <b>%d</b>." % (" × ".join([str(n)] * m), n ** m))


def s5_problema():
    k = R.choice(["fila", "placas", "cardapio", "dados", "bandeira", "time"])
    if k == "fila":
        n = R.choice([3, 4])
        names = [K.next()[0] for _ in range(n)]
        if len(set(names)) < n:
            return None
        f = 1
        for i in range(2, n + 1):
            f *= i
        return mcq("De quantas maneiras %s podem formar uma fila?" % (", ".join(names[:-1]) + " e " + names[-1]), str(f), [str(n * n), str(n), str(n + n), str(f * 2)],
                   "1º lugar: %d escolhas; 2º: %d; %s. %s = <b>%d</b>." % (n, n - 1, "3º: %d; 4º: 1" % (n - 2) if n == 4 else "3º: 1", " × ".join(str(i) for i in range(n, 0, -1)), f))
    if k == "placas":
        a, b = R.randint(2, 4), R.randint(3, 6)
        return mcq("Um jogo usa fichas com uma cor (%d cores) e um número (de 1 a %d). Quantas fichas diferentes há?" % (a, b), str(a * b), [str(a + b), str(a * b + a), str(b)],
                   "%d × %d = <b>%d</b> fichas." % (a, b, a * b))
    if k == "cardapio":
        a, b = R.randint(2, 4), R.randint(2, 5)
        c = a * b
        return mcq("No almoço da escola há %d opções de prato principal e %d de sobremesa. Um aluno quer comer uma combinação diferente por dia. Por quantos dias ele consegue?" % (a, b),
                   "%d dias" % c, ["%d dias" % x for x in (a + b, c + 1, c * 2)], "%d × %d = <b>%d</b> combinações, uma por dia." % (a, b, c))
    if k == "dados":
        return mcq("Lançamos um dado comum e uma moeda (cara ou coroa). Quantos resultados diferentes podem sair?", "12", ["8", "6", "36"],
                   "6 resultados do dado × 2 da moeda = <b>12</b>.") if R.random() < 0.5 else \
            mcq("Lançamos dois dados comuns, um azul e um vermelho. Quantos resultados diferentes podem sair?", "36", ["12", "6", "18"],
                "6 resultados do dado azul × 6 do vermelho = <b>36</b>.")
    if k == "bandeira":
        c = R.choice([3, 4, 5])
        return mcq("Uma bandeira tem 2 faixas, e cada faixa deve ter uma cor diferente. Há %d cores para escolher. Quantas bandeiras diferentes podemos fazer?" % c,
                   str(c * (c - 1)), [str(c * c), str(c + c - 1), str(c * 2), str(c * c - 1), str(c * (c - 1) // 2)], "1ª faixa: %d cores; 2ª faixa: %d (não pode repetir). %d × %d = <b>%d</b>." % (c, c - 1, c, c - 1, c * (c - 1)))
    a = R.randint(3, 6)
    b = R.randint(2, 4)
    return mcq("Para formar uma dupla, a professora escolhe 1 menino entre %d e 1 menina entre %d. Quantas duplas diferentes ela pode formar?" % (a, b), str(a * b), [str(a + b), str(a * b - 1), str(a * b * 2), str(a * b + 1)],
               "%d × %d = <b>%d</b> duplas." % (a, b, a * b))


def main():
    seen = set()
    sets = [
        ("Combinar duas coleções", mix(R, seen, [(s1_dois, 14), (s1_tabela, 6)])),
        ("Árvore de possibilidades", mix(R, seen, [(s2_arvore, 12), (s2_lista, 8)])),
        ("Três coleções e número que falta", mix(R, seen, [(s3_tres, 12), (s3_falta, 8)])),
        ("Formar números e senhas", mix(R, seen, [(s4_numeros, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para saber quantas combinações existem, <b>multiplique</b> o número de escolhas de cada etapa: é o <b>princípio multiplicativo</b>.",
         "3 camisetas e 4 bermudas: para cada camiseta há 4 bermudas → 3 × 4 = 12 maneiras.",
         "A <b>árvore de possibilidades</b> e a <b>tabela de dupla entrada</b> ajudam a ver e a listar todas as combinações.",
         "Quando não pode repetir, a cada etapa sobra uma escolha a menos: com 4 algarismos diferentes, 4 × 3 = 12 números."],
        [("Com 3 sabores de sorvete e 2 coberturas, quantos sorvetes diferentes?", ["para cada sabor, 2 coberturas", "3 × 2"], "6"),
         ("Quantos números de 2 algarismos diferentes com 1, 2, 3 e 4?", ["dezenas: 4 escolhas", "unidades: sobram 3", "4 × 3"], "12")],
        [["Somar em vez de multiplicar: 3 + 4 = 7", "Cada camiseta combina com todas as bermudas: 3 × 4 = 12."],
         ["Esquecer uma coleção", "Multiplique todas as etapas: 3 × 4 × 2."],
         ["Repetir algarismos quando não pode", "Depois de usar um algarismo, sobra um a menos."]],
        arvore(["branca", "azul", "verde"], ["jeans", "cinza"]))
    faq = [("O que é o princípio multiplicativo?", "É a ideia de que, se uma escolha pode ser feita de a maneiras e outra de b maneiras, as duas juntas podem ser feitas de a × b maneiras."),
           ("Por que usar a árvore de possibilidades?", "A árvore mostra cada combinação num ramo. Contando as pontas, as crianças veem por que a resposta é uma multiplicação.")]
    make_unit(R, "problemas-de-contagem", "N", ["EF05MA09"],
              "Resolver e elaborar problemas simples de contagem envolvendo o princípio multiplicativo, como a determinação do número de agrupamentos possíveis ao se combinar cada elemento de uma coleção com todos os elementos de outra coleção, por meio de diagramas de árvore ou por tabelas",
              "Problemas de contagem: princípio multiplicativo e árvore de possibilidades", "Problemas de contagem",
              "Atividades de matemática para o 5º ano sobre problemas de contagem: princípio multiplicativo, combinações de roupas e lanches, árvore de possibilidades, tabelas, números e senhas. 100 exercícios com gabarito.",
              "Multiplique o número de escolhas de cada etapa.", "3 camisetas × 4 bermudas = 12 maneiras.",
              body, faq, sets, 11, grade="5-ano")


if __name__ == "__main__":
    main()
