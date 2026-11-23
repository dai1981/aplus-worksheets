# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Proporcionalidade e partilha (Álgebra, EF05MA12, EF05MA13)
  python3 tools/gen_br_matematica_5_proporcionalidade_e_partilha.py
Grandezas diretamente proporcionais (dobro, triplo, metade): receitas, preços, tempo e distância; tabelas de proporcionalidade;
partilha de uma quantidade em duas partes desiguais (uma é o dobro, o triplo ou tem mais 10 que a outra); problemas.
Erros: somar em vez de multiplicar (2 ovos → 4 ovos para 2 bolos, então 3 bolos → 5 ovos), dividir em partes iguais quando uma é o dobro.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, reais, table, Kids, pl, wrap, INK, text

R = random.Random(80513)
K = Kids(R)
RECEITAS = [("bolo", "bolos", [("ovo", "ovos", 3), ("xícara de farinha", "xícaras de farinha", 2), ("colher de manteiga", "colheres de manteiga", 2)]),
            ("pudim", "pudins", [("ovo", "ovos", 4), ("lata de leite condensado", "latas de leite condensado", 1)]),
            ("jarra de suco", "jarras de suco", [("laranja", "laranjas", 6), ("copo de água", "copos de água", 2)]),
            ("panela de brigadeiro", "panelas de brigadeiro", [("lata de leite condensado", "latas de leite condensado", 1), ("colher de chocolate", "colheres de chocolate", 4)]),
            ("receita de pão de queijo", "receitas de pão de queijo", [("ovo", "ovos", 2), ("xícara de polvilho", "xícaras de polvilho", 3)])]


def s1_receita():
    s, p_, ings = R.choice(RECEITAS)
    i1, ip, q = R.choice(ings)
    m = R.choice([2, 3, 4, 5])
    n0 = R.choice([1, 1, 2])
    q0 = q * n0
    n1 = n0 * m
    return mcq("Para fazer %s, usamos %s. Para fazer %s, quanto é preciso?" % (pl(n0, s, p_), pl(q0, i1, ip), pl(n1, s, p_)),
               pl(q0 * m, i1, ip), [pl(x, i1, ip) for x in (q0 + n1 - n0, q0 * m + q, q0 + m, q0 * m - q0)],
               "%d é %d vezes %d; então a quantidade também fica %d vezes maior: %d × %d = <b>%d</b>." % (n1, m, n0, m, q0, m, q0 * m))


def s1_preco():
    obj = R.choice([("caderno", "cadernos"), ("lápis", "lápis"), ("sorvete", "sorvetes"), ("pão de queijo", "pães de queijo"), ("bombom", "bombons"), ("pastel", "pastéis")])
    a = R.choice([2, 3, 4, 5])
    pr = R.randint(2, 12) * a * 50
    m = R.choice([2, 3, 4])
    if R.random() < 0.5:
        return mcq("%s custam %s. Quanto custam %s?" % (pl(a, *obj), reais(pr), pl(a * m, *obj)), reais(pr * m),
                   [reais(x) for x in (pr + (a * m - a) * 100, pr * m + pr, pr * (m - 1), pr + a * m * 100)],
                   "%d é %d vezes %d; o preço também fica %d vezes maior: %d × %s = <b>%s</b>." % (a * m, m, a, m, m, reais(pr), reais(pr * m)))
    return mcq("%s custam %s. Quanto custa 1 %s?" % (pl(a, *obj), reais(pr), obj[0]), reais(pr // a),
               [reais(x) for x in (pr - a * 100, pr * a, pr // a + 100, pr // 2 if a != 2 else pr // 4)], "%s ÷ %d = <b>%s</b>." % (reais(pr), a, reais(pr // a)))


def s2_tabela():
    k = R.choice(["km", "kg", "litros", "páginas"])
    u = {"km": ("Tempo (h)", "Distância (km)", R.choice([60, 70, 80, 90])), "kg": ("Pacotes", "Massa (kg)", R.choice([2, 3, 5])),
         "litros": ("Garrafas", "Água (L)", R.choice([2, 3])), "páginas": ("Dias", "Páginas lidas", R.choice([12, 15, 20, 25]))}[k]
    xs = sorted(R.sample(range(1, 9), 4))
    hide = R.randrange(1, 4)
    ys = [x * u[2] for x in xs]
    cells = [num(y) if i != hide else "?" for i, y in enumerate(ys)]
    tb = table([u[0]] + [str(x) for x in xs], [[u[1]] + cells])
    ans = ys[hide]
    return mcq(tb + "As grandezas da tabela são diretamente proporcionais. Que número fica no lugar do «?»?", num(ans),
               [num(x) for x in (ys[hide - 1] + (xs[hide] - xs[hide - 1]), ans + u[2], ans - u[2], ys[0] * xs[hide] + 1)],
               "Para 1 vale %s; para %d vale %d × %s = <b>%s</b>." % (num(u[2]), xs[hide], xs[hide], num(u[2]), num(ans)))


def s2_eh():
    k = R.choice(["sim", "nao"])
    a = R.randint(2, 9)
    xs = [1, 2, 3, 4]
    if k == "sim":
        ys = [x * a for x in xs]
    else:
        ys = [x * a for x in xs]
        ys[R.randrange(1, 4)] += R.choice([1, 2, -1])
    tb = table(["Quantidade"] + [str(x) for x in xs], [["Preço (R$)"] + [str(y) for y in ys]])
    ok = all(ys[i] == xs[i] * ys[0] for i in range(4))
    return mcq(tb + "Os valores desta tabela são diretamente proporcionais?", "Sim: todos são %d vezes a quantidade" % a if ok else "Não: um valor não segue a regra",
               ["Não: um valor não segue a regra" if ok else "Sim: todos são %d vezes a quantidade" % a, "Sim, porque os números aumentam", "Não, porque não começa no zero"],
               "Veja se cada valor é a quantidade × %d: %s. <b>%s</b>." % (ys[0], "; ".join("%d × %d = %d" % (x, ys[0], x * ys[0]) for x in xs), "Sim" if ok else "Não"))


def s3_partilha():
    m = R.choice([2, 3, 4])
    small = R.randint(5, 60)
    tot = small * (m + 1)
    nome = {2: "o dobro", 3: "o triplo", 4: "o quádruplo"}[m]
    p, q = K.next()[0], K.next()[0]
    if p == q:
        return None
    obj = R.choice(["figurinhas", "bolinhas de gude", "reais", "balas", "selos", "livros"])
    big = small * m
    if R.random() < 0.5:
        return mcq("%s e %s têm, ao todo, %d %s. %s tem %s de %s. Quantas %s tem %s?" % (p, q, tot, obj, q, nome, p, obj, p) if obj not in ("selos", "livros", "reais") else
                   "%s e %s têm, ao todo, %d %s. %s tem %s de %s. Quantos %s tem %s?" % (p, q, tot, obj, q, nome, p, obj, p),
                   str(small), [str(tot // 2), str(big), str(tot // m), str(small + m)],
                   "%s tem 1 parte e %s tem %d partes: são %d partes. %d ÷ %d = <b>%d</b>." % (p, q, m, m + 1, tot, m + 1, small))
    return mcq("Divida %d em duas partes de modo que uma seja %s da outra. Quais são as partes?" % (tot, nome), "%d e %d" % (small, big),
               ["%d e %d" % (tot // 2, tot - tot // 2), "%d e %d" % (tot // m, tot - tot // m) if tot % m == 0 else "%d e %d" % (small + 1, big - 1), "%d e %d" % (small, small * (m + 1))],
               "1 parte + %d partes = %d partes. %d ÷ %d = %d e %d × %d = %d: <b>%d e %d</b>." % (m, m + 1, tot, m + 1, small, small, m, big, small, big))


def s3_diferenca():
    a = R.randint(10, 80)
    d = R.choice([4, 6, 8, 10, 12, 20])
    tot = 2 * a + d
    p, q = K.next()[0], K.next()[0]
    if p == q:
        return None
    return mcq("%s e %s juntaram %s. %s tem %s a mais que %s. Quanto tem cada pessoa?" % (p, q, reais(tot * 100), q, reais(d * 100), p),
               "%s: %s; %s: %s" % (p, reais(a * 100), q, reais((a + d) * 100)),
               ["%s: %s; %s: %s" % (p, reais(tot * 50), q, reais(tot * 50)), "%s: %s; %s: %s" % (p, reais((tot - d) * 100), q, reais(d * 100)),
                "%s: %s; %s: %s" % (p, reais((a - d // 2) * 100), q, reais((a + d + d // 2) * 100))],
               "Tire a diferença: %d − %d = %d. Divida por 2: %d. %s tem %s e %s tem %d + %d = %s." % (tot, d, tot - d, a, p, reais(a * 100), q, a, d, reais((a + d) * 100)))


def s4_misturas():
    k = R.choice(["tinta", "suco", "cimento"])
    a, b = R.randint(1, 3), R.randint(2, 5)
    if a == b:
        return None
    m = R.choice([2, 3, 4, 5])
    w = {"tinta": ("Para fazer tinta verde, misturamos %s de tinta azul com %s de tinta amarela." % (pl(a, "lata", "latas"), pl(b, "lata", "latas")), "latas de tinta amarela", "latas de tinta azul", "lata"),
         "suco": ("Um suco é feito com %s de concentrado para %s de água." % (pl(a, "copo", "copos"), pl(b, "copo", "copos")), "copos de água", "copos de concentrado", "copo"),
         "cimento": ("Um pedreiro mistura %s de cimento com %s de areia." % (pl(a, "balde", "baldes"), pl(b, "balde", "baldes")), "baldes de areia", "baldes de cimento", "balde")}[k]
    return mcq("%s Usando %d %s, quantos %s são necessários para a mistura ficar igual?" % (w[0], a * m, w[2], w[1]), str(b * m), [str(b + a * m - a), str(b * m + b), str(a * m), str(b + m)],
               "%d é %d vezes %d; então também usamos %d vezes %d: <b>%d</b>." % (a * m, m, a, m, b, b * m))


def s5_problema():
    k = R.choice(["carro", "torneira", "salario", "metade", "fotos", "triplo", "escala"])
    p, g = K.next()
    if k == "carro":
        v = R.choice([60, 70, 80, 90, 100])
        h = R.randint(2, 6)
        return mcq("Um carro anda %d km em 1 hora, sempre na mesma velocidade. Quantos quilômetros anda em %d horas?" % (v, h), "%s km" % num(v * h),
                   ["%s km" % num(x) for x in (v + h, v * h + v, v * (h - 1), v + h * 10)], "%d × %d = <b>%s km</b>." % (h, v, num(v * h)))
    if k == "torneira":
        L = R.choice([6, 8, 10, 12, 15])
        mins = R.randint(3, 12)
        return mcq("Uma torneira enche %d litros em 1 minuto. Em quantos minutos ela enche %d litros?" % (L, L * mins), "%d minutos" % mins,
                   ["%d minutos" % x for x in (L * mins - L, mins + 1, L, mins * 2)], "%d ÷ %d = <b>%d minutos</b>." % (L * mins, L, mins))
    if k == "salario":
        h = R.randint(3, 8)
        pr = R.randint(15, 40) * 100
        return mcq("%s ganha %s por hora de trabalho. Quanto ganha em %d horas?" % (p, reais(pr), h), reais(pr * h), [reais(x) for x in (pr + h * 100, pr * h + pr, pr * (h - 1))],
                   "%d × %s = <b>%s</b>." % (h, reais(pr), reais(pr * h)))
    if k == "metade":
        s, p_, ings = R.choice(RECEITAS)
        i1, ip, q = R.choice(ings)
        q2 = q * 2
        return mcq("Uma receita de %s usa %s. Para fazer meia receita, quanto é preciso?" % (s.replace("receita de ", ""), pl(q2, i1, ip)), pl(q, i1, ip),
                   [pl(x, i1, ip) for x in (q2 - 1, q2 * 2, q2 + 2 if q2 + 2 != q else q2 + 1, q + 1)], "Metade de %d é <b>%d</b>." % (q2, q))
    if k == "fotos":
        a = R.randint(2, 5)
        fotos = R.randint(6, 12) * a
        return mcq("Num álbum, cabem %d fotos em %s. Quantas fotos cabem em %s?" % (fotos, pl(a, "página", "páginas"), pl(a * 3, "página", "páginas")), str(fotos * 3),
                   [str(fotos + a * 2), str(fotos * 3 + fotos), str(fotos * 2)], "%d páginas é o triplo de %d; as fotos também triplicam: <b>%d</b>." % (a * 3, a, fotos * 3))
    if k == "triplo":
        small = R.randint(6, 40)
        tot = small * 4
        return mcq("Num estacionamento há %d veículos, entre carros e motos. Há o triplo de carros em relação às motos. Quantos carros há?" % tot, str(small * 3),
                   [str(small), str(tot // 3) if tot % 3 == 0 else str(tot // 2), str(tot // 2), str(small * 2), str(tot - small + 1)], "1 parte de motos + 3 partes de carros = 4 partes. %d ÷ 4 = %d; carros: 3 × %d = <b>%d</b>." % (tot, small, small, small * 3))
    m = R.choice([10, 100])
    d = R.randint(2, 9)
    return mcq("Num mapa, cada 1 cm representa %s m. Duas cidades estão a %d cm no mapa. Qual é a distância real?" % (num(m * 100), d), "%s m" % num(m * 100 * d),
               ["%s m" % num(x) for x in (m * 100 + d, m * 100 * d * 10, m * 10 * d)], "%d × %s = <b>%s m</b>." % (d, num(m * 100), num(m * 100 * d)))


def main():
    seen = set()
    sets = [
        ("Dobro, triplo e metade", mix(R, seen, [(s1_receita, 12), (s1_preco, 8)])),
        ("Tabelas de proporcionalidade", mix(R, seen, [(s2_tabela, 14), (s2_eh, 6)])),
        ("Partilha em partes desiguais", mix(R, seen, [(s3_partilha, 14), (s3_diferenca, 6)])),
        ("Misturas e receitas", mix(R, seen, [(s4_misturas, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Duas grandezas são <b>diretamente proporcionais</b> quando, se uma dobra, a outra também dobra; se uma fica a metade, a outra também.",
         "Numa receita: 2 bolos usam 6 ovos; 4 bolos (o dobro) usam 12 ovos (o dobro). Multiplique, não some.",
         "Para <b>partilhar em partes desiguais</b>, pense em partes iguais: se uma pessoa tem o dobro da outra, são 1 + 2 = 3 partes.",
         "Se uma parte tem 10 a mais, tire os 10 primeiro e depois divida o resto por 2."],
        [("Divida 60 em duas partes, uma o dobro da outra.", ["1 parte + 2 partes = 3 partes", "60 ÷ 3 = 20", "20 e 40"], "20 e 40"),
         ("3 cadernos custam R$ 24,00. Quanto custam 9 cadernos?", ["9 é o triplo de 3", "R$ 24,00 × 3"], "R$ 72,00")],
        [["Somar em vez de multiplicar: 2 bolos → 6 ovos, 3 bolos → 7 ovos", "Ache quanto vai em 1 bolo (3 ovos) e multiplique: 3 × 3 = 9."],
         ["Dividir em partes iguais quando uma é o dobro", "Conte as partes: 1 + 2 = 3."],
         ["Esquecer de tirar a diferença antes de dividir", "Primeiro tire o que um tem a mais; depois divida por 2."]],
        table(["Bolos", "1", "2", "3", "4"], [["Ovos", "3", "6", "9", "12"]]))
    faq = [("O que é proporcionalidade direta no 5º ano?", "É reconhecer que, quando uma quantidade dobra, triplica ou fica a metade, a outra muda da mesma forma — como em receitas, preços e escalas."),
           ("Como ensinar a partilha em partes desiguais?", "Desenhe as partes como barrinhas (bar model): uma barrinha para quem tem menos e duas para quem tem o dobro. Depois divida o total pelo número de barrinhas.")]
    make_unit(R, "proporcionalidade-e-partilha", "A", ["EF05MA12", "EF05MA13"],
              "Resolver problemas que envolvam variação de proporcionalidade direta entre duas grandezas, para associar a quantidade de um produto ao valor a pagar, alterar as quantidades de ingredientes de receitas, ampliar ou reduzir escala em mapas, entre outros; resolver problemas envolvendo a partilha de uma quantidade em duas partes desiguais, tais como dividir uma quantidade em duas partes, de modo que uma seja o dobro da outra, com compreensão da ideia de razão entre as partes e delas com o todo",
              "Proporcionalidade e partilha em partes desiguais", "Proporcionalidade e partilha",
              "Atividades de matemática para o 5º ano sobre proporcionalidade direta e partilha: receitas, preços, tabelas, misturas, dobro e triplo e divisão em partes desiguais. 100 exercícios com gabarito.",
              "Se uma grandeza dobra, a outra também dobra.", "Partes desiguais: conte as partes (1 + 2 = 3).",
              body, faq, sets, 13, grade="5-ano")


if __name__ == "__main__":
    main()
