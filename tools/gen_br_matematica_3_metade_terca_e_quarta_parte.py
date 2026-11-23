# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Metade, terça, quarta, quinta e décima parte (Números, EF03MA09)
  python3 tools/gen_br_matematica_3_metade_terca_e_quarta_parte.py
Associar a divisão por 2, 3, 4, 5 e 10 às ideias de metade, terça parte, quarta parte, quinta parte e décima parte;
partes iguais de uma figura; parte de uma quantidade; dobro e metade; problemas.
Erros: confundir metade com dobro, achar que a terça parte é «dividir por 3 e multiplicar», partes não iguais na figura.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, faixa, disco, Kids, reais, grupos, KINDS, coisas

R = random.Random(80310)
K = Kids(R)
PARTE = {2: "metade", 3: "terça parte", 4: "quarta parte", 5: "quinta parte", 10: "décima parte"}


def s1_figura():
    d = R.choice([2, 3, 4, 5, 10])
    pic = faixa(d, 1) if R.random() < 0.6 else disco(d, 1)
    return mcq(pic + "A figura foi dividida em %d partes iguais. A parte pintada é…" % d, "a %s" % PARTE[d],
               ["a %s" % PARTE[x] for x in (2, 3, 4, 5, 10) if x != d],
               "Uma de %d partes iguais é a <b>%s</b>." % (d, PARTE[d]))


def s1_quantas():
    d = R.choice([2, 3, 4, 5, 10])
    nome = PARTE[d]
    return mcq("Em quantas partes iguais dividimos um inteiro para obter a %s?" % nome, str(d), [str(x) for x in (2, 3, 4, 5, 10) if x != d],
               "A %s é uma de <b>%d</b> partes iguais (dividir por %d)." % (nome, d, d))


def s2_quantidade():
    d = R.choice([2, 3, 4, 5, 10])
    q = R.randint(2, 12) if d != 10 else R.randint(2, 9)
    n = d * q
    return mcq("Quanto é a %s de %d?" % (PARTE[d], n), str(q), [str(n * 2) if d == 2 else str(n - d), str(q + 1), str(n // 2) if d != 2 and n % 2 == 0 and n // 2 != q else str(q + d)],
               "A %s de %d é %d ÷ %d = <b>%d</b>." % (PARTE[d], n, n, d, q))


def s2_figura_qtd():
    d = R.choice([2, 3, 4])
    q = R.randint(2, 5)
    kind = R.choice(KINDS)
    n = d * q
    return mcq(grupos(d, q, kind) + "Há %s separadas em %d grupos iguais. Quanto é a %s de %d?" % (coisas(kind, n), d, PARTE[d], n),
               str(q), [str(d), str(n - q), str(q + 1)],
               "Cada grupo é a %s: %d ÷ %d = <b>%d</b>." % (PARTE[d], n, d, q))


def s3_dobro_metade():
    n = R.randint(6, 60)
    k = R.choice(["metade", "dobro", "metade_de_dobro", "volta"])
    if k == "metade":
        if n % 2:
            n += 1
        return mcq("Qual é a metade de %d?" % n, str(n // 2), [str(2 * n), str(n - 2), str(n // 2 + 1)],
                   "Metade é dividir por 2: %d ÷ 2 = <b>%d</b>." % (n, n // 2))
    if k == "dobro":
        return mcq("Qual é o dobro de %d?" % n, str(2 * n), [str(n // 2) if n % 2 == 0 else str(n + 2), str(2 * n + 1), str(n + 2)],
                   "Dobro é multiplicar por 2: <b>%d</b>." % (2 * n))
    if k == "metade_de_dobro":
        return mcq("Pensei num número. O dobro dele é %d. Que número pensei?" % (2 * n), str(n), [str(4 * n), str(2 * n - 2), str(n + 1)],
                   "Se o dobro é %d, o número é a metade: %d ÷ 2 = <b>%d</b>." % (2 * n, 2 * n, n))
    n = R.randint(3, 12)
    return mcq("A metade de um número é %d. Que número é esse?" % n, str(2 * n), [str(n // 2) if n % 2 == 0 else str(n + 2), str(n + 2), str(3 * n)],
               "Se a metade é %d, o número é o dobro: 2 × %d = <b>%d</b>." % (n, n, 2 * n))


def s4_comparar():
    n = R.choice([12, 20, 24, 30, 36, 40, 60])
    ds = [d for d in (2, 3, 4, 5, 10) if n % d == 0]
    a, b = R.sample(ds, 2)
    big = a if n // a > n // b else b
    small = b if big == a else a
    return mcq("Com %d figurinhas, o que é mais: a %s ou a %s de %d?" % (n, PARTE[a], PARTE[b], n), "a %s" % PARTE[big],
               ["a %s" % PARTE[small], "as duas são iguais", "não dá para saber"],
               "%s de %d = %d; %s de %d = %d. Quanto mais partes, menor cada parte: <b>a %s</b>." % (PARTE[a].capitalize(), n, n // a, PARTE[b], n, n // b, PARTE[big]))


def s5_problema():
    p, g = K.next()
    k = R.choice(["dinheiro", "turma", "bolo", "livro", "pizza", "cordas", "lapis"])
    if k == "dinheiro":
        d = R.choice([2, 4, 5, 10])
        n = d * R.randint(2, 10)
        return mcq("%s tinha %s e gastou a %s. Quanto gastou?" % (p, reais(n * 100), PARTE[d]), reais(n // d * 100), [reais((n - n // d) * 100), reais(2 * n * 100) if d == 2 else reais(n * d * 100), reais((n // d + 1) * 100), reais((n // d + 2) * 100)],
                   "A %s de %d é %d ÷ %d = %d: <b>%s</b>." % (PARTE[d], n, n, d, n // d, reais(n // d * 100)))
    if k == "turma":
        d = R.choice([2, 3, 4, 5])
        n = d * R.randint(5, 8)
        return mcq("Numa turma de %d alunos, a %s usa óculos. Quantos alunos usam óculos?" % (n, PARTE[d]), str(n // d), [str(n - n // d), str(n // d + 1), str(d)],
                   "%d ÷ %d = <b>%d</b> alunos." % (n, d, n // d))
    if k == "bolo":
        d = R.choice([2, 3, 4])
        n = d * R.randint(3, 6)
        return mcq("Um bolo foi cortado em %d pedaços iguais. %s comeu a %s do bolo. Quantos pedaços comeu?" % (n, p, PARTE[d]), str(n // d), [str(n - n // d), str(d), str(n // d + 1)],
                   "A %s de %d pedaços: %d ÷ %d = <b>%d</b>." % (PARTE[d], n, n, d, n // d))
    if k == "livro":
        d = R.choice([2, 4, 5, 10])
        n = d * R.randint(10, 30)
        return mcq("Um livro tem %d páginas. %s já leu a %s. Quantas páginas %s leu?" % (n, p, PARTE[d], "ela" if g == "ela" else "ele"), str(n // d), [str(n - n // d), str(n // d + d), str(n * 2) if d == 2 else str(n // 2)],
                   "%d ÷ %d = <b>%d</b> páginas." % (n, d, n // d))
    if k == "pizza":
        return mcq("Uma pizza tem 8 fatias. %s comeu a quarta parte. Quantas fatias sobraram?" % p, "6", ["2", "4", "8"],
                   "A quarta parte de 8 é 8 ÷ 4 = 2; sobraram 8 − 2 = <b>6</b> fatias.")
    if k == "cordas":
        d = R.choice([2, 4, 5, 10])
        n = d * R.randint(3, 9)
        return mcq("Uma corda tem %d metros. Usaram a %s dela. Quantos metros sobraram?" % (n, PARTE[d]), "%d metros" % (n - n // d),
                   ["%d metros" % (n // d), "%d metros" % (n - d), "%d metros" % (n - n // d + 1)],
                   "A %s é %d ÷ %d = %d m; sobram %d − %d = <b>%d metros</b>." % (PARTE[d], n, d, n // d, n, n // d, n - n // d))
    d = R.choice([3, 5])
    n = d * R.randint(3, 6)
    return mcq("%s tem %d lápis. A %s são vermelhos. Quantos lápis NÃO são vermelhos?" % (p, n, PARTE[d]), str(n - n // d), [str(n // d), str(n - d), str(n + n // d)],
               "Vermelhos: %d ÷ %d = %d. Não vermelhos: %d − %d = <b>%d</b>." % (n, d, n // d, n, n // d, n - n // d))


def main():
    seen = set()
    sets = [
        ("Partes iguais de uma figura", mix(R, seen, [(s1_figura, 8), (s1_quantas, 4), (s2_figura_qtd, 8)])),
        ("Parte de uma quantidade", mix(R, seen, [(s2_quantidade, 12), (s2_figura_qtd, 8)])),
        ("Dobro e metade", mix(R, seen, [(s3_dobro_metade, 20)])),
        ("Comparar partes", mix(R, seen, [(s4_comparar, 10), (s2_quantidade, 10)])),
        ("Problemas com metade e partes", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para achar a <b>metade</b>, divida por 2. A <b>terça parte</b> é ÷ 3, a <b>quarta parte</b> é ÷ 4, a <b>quinta parte</b> é ÷ 5 e a <b>décima parte</b> é ÷ 10.",
         "As partes têm de ser <b>iguais</b>: um bolo cortado em 4 pedaços de tamanhos diferentes não está dividido em quartos.",
         "Quanto mais partes, <b>menor</b> cada parte: a quarta parte de 20 (5) é menor que a metade de 20 (10).",
         "Metade e dobro são contrários: a metade de 16 é 8, e o dobro de 8 é 16."],
        [("A terça parte de 18", ["18 ÷ 3"], "6"),
         ("A quarta parte de 20 reais", ["20 ÷ 4"], "5 reais")],
        [["Achar que a metade de 12 é 24", "24 é o dobro. A metade é 12 ÷ 2 = 6."],
         ["Contar partes de tamanhos diferentes", "Só vale se todas as partes forem iguais."],
         ["Achar que a quarta parte é maior que a metade", "Dividir em mais partes deixa cada parte menor."]],
        faixa(4, 1))
    faq = [("Por que estudar metade e terça parte no 3º ano?", "Porque essas ideias ligam a divisão às frações, que serão estudadas com mais detalhe no 4º e no 5º ano."),
           ("Como explicar a terça parte?", "Reparta 12 objetos em 3 grupos iguais: cada grupo (4 objetos) é a terça parte. Depois mostre que é o mesmo que 12 ÷ 3.")]
    make_unit(R, "metade-terca-e-quarta-parte", "N", ["EF03MA09"],
              "Associar o quociente de uma divisão com resto zero de um número natural por 2, 3, 4, 5 e 10 às ideias de metade, terça, quarta, quinta e décima partes",
              "Metade, terça, quarta, quinta e décima parte", "Metade, terça e quarta parte",
              "Atividades de matemática para o 3º ano sobre metade, terça parte, quarta parte, quinta parte e décima parte: partes iguais de figuras, parte de uma quantidade, dobro e metade, problemas. 100 exercícios com gabarito.",
              "Metade é ÷ 2, terça parte é ÷ 3, quarta parte é ÷ 4.", "As partes têm de ser iguais.",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
