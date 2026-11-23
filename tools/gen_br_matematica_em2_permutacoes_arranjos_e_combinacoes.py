# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Permutações, arranjos e combinações (EM13MAT310)
  python3 tools/gen_br_matematica_em2_permutacoes_arranjos_e_combinacoes.py
Permutação simples (n!) e com repetição (anagramas com letras repetidas); arranjo (a ordem importa);
combinação (a ordem não importa): comissões, apertos de mão, diagonais, jogos de loteria; escolher o tipo de agrupamento.
Erros: usar arranjo quando a ordem não importa, esquecer de dividir pelas letras repetidas, confundir C(n, p) e A(n, p).
"""
import random
import math
from collections import Counter
from br_em import M, bank, mix, lesson, unit, num

R = random.Random(92012)
PALAVRAS = ["BRASIL", "AMOR", "LIVRO", "ESCOLA", "PRAIA", "BANANA", "ARARA", "CASA", "MACACO", "SAPATO", "PIPOCA", "CABANA", "PATO", "GATO", "SOL", "MAPA", "BOLO", "CAJU", "RECIFE", "PANELA"]


def s1_anagrama():
    w = R.choice(PALAVRAS)
    c = Counter(w)
    n = len(w)
    v = math.factorial(n)
    rep = [k for k, x in c.items() if x > 1]
    for k in rep:
        v //= math.factorial(c[k])
    k = R.choice(["total", "total", "comeca"])
    if k == "total":
        return M("Quantos anagramas tem a palavra %s?" % w, num(v), [num(math.factorial(n)) if rep else num(v * 2), num(n * n), num(v // 2) if v % 2 == 0 and v // 2 != v else num(v + n)],
                 "%d letras%s: %d!%s = <b>%s</b>." % (n, (" com " + ", ".join("%s repetida %d vezes" % (k, c[k]) for k in rep)) if rep else ", todas diferentes", n, "".join(" ÷ %d!" % c[k] for k in rep), num(v)))
    if rep:
        return None
    return M("Quantos anagramas da palavra %s começam por %s?" % (w, w[0]), num(math.factorial(n - 1)), [num(math.factorial(n)), num(n - 1), num(math.factorial(n - 2))], "%s fixo; as outras %d letras: %d! = <b>%s</b>." % (w[0], n - 1, n - 1, num(math.factorial(n - 1))))


def s2_arr_comb():
    k = R.choice(["comissao", "diretoria", "aperto", "diag", "pizza", "time", "podio", "loteria"])
    if k == "comissao":
        n, p = R.randint(6, 12), R.choice([2, 3, 4])
        return M("De quantas maneiras se pode formar uma comissão de %d pessoas escolhidas entre %d?" % (p, n), num(math.comb(n, p)), [num(math.perm(n, p)), num(n * p), num(math.comb(n, p - 1))], "A ordem não importa: C(%d, %d) = %s ÷ %d! = <b>%s</b>." % (n, p, num(math.perm(n, p)), p, num(math.comb(n, p))))
    if k == "diretoria":
        n, p = R.randint(6, 12), R.choice([2, 3])
        cargos = "presidente e vice" if p == 2 else "presidente, vice e tesoureiro"
        return M("Num grupo de %d pessoas, de quantas maneiras se pode escolher %s?" % (n, cargos), num(math.perm(n, p)), [num(math.comb(n, p)), num(n ** p), num(n * p)], "A ordem importa (cargos diferentes): A(%d, %d) = <b>%s</b>." % (n, p, num(math.perm(n, p))))
    if k == "aperto":
        n = R.randint(5, 20)
        return M("Numa reunião com %d pessoas, cada uma aperta a mão de todas as outras uma vez. Quantos apertos de mão há?" % n, num(math.comb(n, 2)), [num(n * (n - 1)), num(n * n), num(n)], "C(%d, 2) = %d · %d ÷ 2 = <b>%s</b>." % (n, n, n - 1, num(math.comb(n, 2))))
    if k == "diag":
        n = R.choice([5, 6, 7, 8, 10, 12, 15, 20])
        return M("Quantas diagonais tem um polígono convexo de %d lados?" % n, num(n * (n - 3) // 2), [num(math.comb(n, 2)), num(n * (n - 3)), num(n - 3)], "C(%d, 2) − %d lados = %s − %d = <b>%s</b>." % (n, n, num(math.comb(n, 2)), n, num(n * (n - 3) // 2)))
    if k == "pizza":
        n, p = R.choice([(8, 2), (10, 2), (10, 3), (12, 2), (6, 3), (9, 3)])
        return M("Uma pizzaria tem %d sabores. Quantas pizzas de %d sabores diferentes podem ser montadas?" % (n, p), num(math.comb(n, p)), [num(math.perm(n, p)), num(n ** p), num(n * p)], "A ordem dos sabores não importa: C(%d, %d) = <b>%s</b>." % (n, p, num(math.comb(n, p))))
    if k == "time":
        g, b = R.randint(4, 8), R.randint(4, 8)
        p, q = R.choice([(2, 2), (2, 3), (3, 2), (1, 2)])
        v = math.comb(g, p) * math.comb(b, q)
        return M("Uma turma tem %d meninas e %d meninos. Quantas equipes com %d %s e %d %s podem ser formadas?" % (g, b, p, "menina" if p == 1 else "meninas", q, "menino" if q == 1 else "meninos"), num(v), [num(math.comb(g + b, p + q)), num(math.comb(g, p) + math.comb(b, q)), num(math.perm(g, p) * math.perm(b, q))],
                 "C(%d, %d) · C(%d, %d) = %d · %d = <b>%s</b>." % (g, p, b, q, math.comb(g, p), math.comb(b, q), num(v)))
    if k == "podio":
        n = R.randint(6, 12)
        return M("Numa competição com %d equipes, quantos pódios (ouro, prata e bronze) são possíveis?" % n, num(math.perm(n, 3)), [num(math.comb(n, 3)), num(n ** 3), num(3 * n)], "A ordem importa: %d · %d · %d = <b>%s</b>." % (n, n - 1, n - 2, num(math.perm(n, 3))))
    n, p = R.choice([(60, 6), (25, 15), (80, 5), (50, 5)])
    nm = {60: "Mega-Sena", 25: "Lotofácil", 80: "Quina", 50: "um jogo"}[n]
    return M("Na %s, escolhem-se %d números entre %d. A ordem importa?" % (nm, p, n) if n != 50 else "Num jogo, escolhem-se %d números entre %d. A ordem importa?" % (p, n), "não, é uma combinação C(%d, %d)" % (n, p), ["sim, é um arranjo A(%d, %d)" % (n, p), "sim, é uma permutação %d!" % n, "não, é %d · %d" % (n, p)],
             "Sorteio de números sem ordem: <b>combinação</b>.")


def s3_formula():
    k = R.choice(["C", "A", "P", "C", "prop"])
    n = R.randint(5, 12)
    p = R.randint(2, min(4, n - 1))
    if k == "C":
        return M("Quanto vale C(%d, %d)?" % (n, p), num(math.comb(n, p)), [num(math.perm(n, p)), num(math.comb(n, p + 1)), num(n * p)], "C(n, p) = n! ÷ (p!(n − p)!) = <b>%s</b>." % num(math.comb(n, p)))
    if k == "A":
        return M("Quanto vale A(%d, %d)?" % (n, p), num(math.perm(n, p)), [num(math.comb(n, p)), num(n ** p), num(math.perm(n, p - 1))], "A(n, p) = n! ÷ (n − p)! = %s = <b>%s</b>." % (" · ".join(str(n - i) for i in range(p)), num(math.perm(n, p))))
    if k == "P":
        m = R.randint(3, 7)
        return M("Quanto vale P%s?" % "₃₄₅₆₇"[m - 3], num(math.factorial(m)), [num(m * m), num(math.factorial(m - 1)), num(2 ** m)], "P%s = %d! = <b>%s</b>." % ("₃₄₅₆₇"[m - 3], m, num(math.factorial(m))))
    return M("C(%d, %d) é igual a…" % (n, p), "C(%d, %d)" % (n, n - p), ["C(%d, %d)" % (n, p + 1), "A(%d, %d)" % (n, p), "C(%d, %d)" % (n - p, p), "C(%d, %d)" % (n - 1, p), "A(%d, %d)" % (n, n - p)], "Escolher %d é o mesmo que deixar de fora %d: <b>C(%d, %d)</b> (combinações complementares)." % (p, n - p, n, n - p))


s4_tipo = bank(R, [
    ("Escolher 3 livros de uma estante de 10 para levar numa viagem é um problema de…", "combinação", ["arranjo", "permutação", "princípio aditivo"]),
    ("Formar senhas de 4 algarismos distintos com 0 a 9 é um problema de…", "arranjo", ["combinação", "permutação com repetição", "fatorial de 4"]),
    ("Organizar 6 livros diferentes numa prateleira é um problema de…", "permutação", ["combinação", "arranjo de 6 tomados 2 a 2", "princípio aditivo"]),
    ("Na combinação, a ordem dos elementos…", "não importa", ["importa", "importa só no início", "é sempre crescente"]),
    ("No arranjo, a ordem dos elementos…", "importa", ["não importa", "é sempre alfabética", "não existe"]),
    ("C(n, p) = A(n, p) ÷ …", "p!", ["n!", "(n − p)!", "2"]),
    ("Quantos subconjuntos de 2 elementos tem um conjunto de 4 elementos?", "6", ["12", "8", "4"]),
    ("Escolher capitão e goleiro entre 11 jogadores é um problema de…", "arranjo", ["combinação", "permutação de 11", "princípio aditivo"]),
], "s4_tipo")


def main():
    seen = set()
    sets = [
        ("Permutações e anagramas", mix(R, seen, [(s1_anagrama, 20)])),
        ("Arranjo ou combinação?", mix(R, seen, [(s4_tipo, 8), (s2_arr_comb, 12)])),
        ("Calcular A, C e P", mix(R, seen, [(s3_formula, 20)])),
        ("Problemas de combinação", mix(R, seen, [(s2_arr_comb, 20)])),
        ("Revisão", mix(R, seen, [(s2_arr_comb, 10), (s1_anagrama, 6), (s3_formula, 4)])),
    ]
    body = lesson(
        ["<b>Permutação</b>: ordenar todos os n elementos: Pₙ = n!. Com repetição: divida pelos fatoriais das repetições (BANANA: 6! ÷ (3! · 2!) = 60).",
         "<b>Arranjo</b> (a ordem importa): A(n, p) = n! ÷ (n − p)!. Ex.: presidente e vice, pódio, senhas sem repetição.",
         "<b>Combinação</b> (a ordem não importa): C(n, p) = n! ÷ (p!(n − p)!). Ex.: comissões, sabores de pizza, loteria.",
         "Teste: trocar a ordem dá outro resultado? Se sim, arranjo; se não, combinação."],
        [("Comissão de 3 entre 8", ["C(8, 3) = 8 · 7 · 6 ÷ 3!"], "56"),
         ("Presidente, vice e tesoureiro entre 8", ["A(8, 3) = 8 · 7 · 6"], "336")],
        [["Arranjo quando a ordem não importa", "Comissão {Ana, Bia} = {Bia, Ana}: é combinação."],
         ["Esquecer as letras repetidas", "Divida por k! para cada letra que aparece k vezes."],
         ["Confundir C(n, p) e A(n, p)", "C = A ÷ p!."]])
    faq = [("Qual é a diferença entre arranjo e combinação?", "No arranjo a ordem importa (pódio, cargos); na combinação não importa (comissão, loteria). Por isso C(n, p) = A(n, p) ÷ p!."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas de contagem envolvendo agrupamentos ordenáveis ou não de elementos, por meio dos princípios multiplicativo e aditivo, recorrendo a estratégias diversas, como o diagrama de árvore (EM13MAT310).")]
    unit(R, "permutacoes-arranjos-e-combinacoes", "E", ["EM13MAT310"],
         "Resolver e elaborar problemas de contagem envolvendo agrupamentos ordenáveis ou não de elementos, por meio dos princípios multiplicativo e aditivo, recorrendo a estratégias diversas, como o diagrama de árvore",
         "Permutações, arranjos e combinações", "Permutações, arranjos e combinações",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre análise combinatória: permutações, anagramas, arranjos, combinações, comissões, pódios e loterias. 100 exercícios com gabarito.",
         "Ordem importa: arranjo; não importa: combinação", "C(n, p) = n! ÷ (p!(n − p)!).",
         body, faq, sets, 12, grade="2-serie")


if __name__ == "__main__":
    main()
