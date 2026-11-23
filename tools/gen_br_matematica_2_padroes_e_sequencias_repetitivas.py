# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Padrões e sequências repetitivas (Álgebra, EF02MA10, EF02MA11)
  python3 tools/gen_br_matematica_2_padroes_e_sequencias_repetitivas.py
Sequências de figuras, cores, letras e gestos que se repetem; a parte que se repete; a figura que falta e a próxima;
qual figura fica numa posição (10ª, 12ª); contar figuras numa sequência; sequências que crescem (recursivas).
Erros: olhar só a última figura, achar que a parte que se repete tem só uma figura, perder a conta da posição.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, KINDS, COISAS, pl
from br_2 import padrao, item_nome, FORMAS, CORES

R = random.Random(80211)
q_fig = use("gen_br_matematica_3_sequencias_numericas", 80906, "s4_figuras")
ORD = {2: "2ª", 3: "3ª", 4: "4ª", 5: "5ª", 6: "6ª", 7: "7ª", 8: "8ª", 9: "9ª", 10: "10ª", 11: "11ª", 12: "12ª", 13: "13ª", 14: "14ª", 15: "15ª", 16: "16ª", 18: "18ª", 20: "20ª"}


def nucleo(k=None):
    """a parte que se repete: 2 a 4 figuras, pelo menos 2 diferentes"""
    k = k or R.choice([2, 3, 3, 4])
    if R.random() < 0.6:
        pool = [("shape", f, c) for f in FORMAS for c in CORES]
        if R.random() < 0.5:  # mesma forma, cores diferentes
            f = R.choice(sorted(FORMAS))
            pool = [("shape", f, c) for c in sorted(CORES)]
        elif R.random() < 0.5:  # mesma cor, formas diferentes
            c = R.choice(sorted(CORES))
            pool = [("shape", f, c) for f in sorted(FORMAS)]
    else:
        pool = [("obj", x) for x in KINDS]
    base = R.sample(pool, min(k, len(pool), 3))
    u = list(base)
    while len(u) < k:
        u.insert(R.randrange(len(u) + 1), R.choice(base))
    if len(set(u)) < 2 or any(u == u[:j] * (k // j) for j in range(1, k) if k % j == 0):
        return None
    return u


def nomes(u):
    return [item_nome(x) for x in u]


def fil(u, n):
    return [u[i % len(u)] for i in range(n)]


def s1_proximo():
    u = nucleo()
    if not u:
        return None
    n = len(u) * 2 + R.randint(0, len(u) - 1)
    items = fil(u, n)
    ans = item_nome(u[n % len(u)])
    others = sorted(set(nomes(u)) - {ans})
    extra = [item_nome(("shape", f, c)) for f in sorted(FORMAS) for c in sorted(CORES)] if u[0][0] == "shape" else [COISAS[x][0] for x in KINDS]
    R.shuffle(extra)
    return mcq(padrao(items, 1) + "Qual figura vem no lugar do «?»", ans, others + [x for x in extra if x != ans and x not in others],
               "A parte que se repete é: %s. Depois de %s vem <b>%s</b>." % (", ".join(nomes(u)), item_nome(items[-1]), ans))


def s1_falta():
    u = nucleo()
    if not u:
        return None
    n = len(u) * 3
    i = R.randint(len(u), n - 2)
    items = fil(u, n)
    ans = item_nome(items[i])
    shown = [("blank",) if j == i else x for j, x in enumerate(items)]
    others = sorted(set(nomes(u)) - {ans})
    extra = [item_nome(("shape", f, c)) for f in sorted(FORMAS) for c in sorted(CORES)] if u[0][0] == "shape" else [COISAS[x][0] for x in KINDS]
    R.shuffle(extra)
    return mcq(padrao(shown) + "Qual figura falta no «?»", ans, others + [x for x in extra if x != ans and x not in others],
               "A sequência repete %s. No «?» fica <b>%s</b>." % (", ".join(nomes(u)), ans))


def s2_parte():
    u = nucleo()
    if not u:
        return None
    items = fil(u, len(u) * 3)
    ok = ", ".join(nomes(u))
    w1 = ", ".join(nomes(u[:-1])) if len(u) > 2 else ", ".join(nomes(u[::-1]))
    w2 = ", ".join(nomes(u + u[:1]))
    w3 = ", ".join(nomes(u[1:] + u[:1]))
    return mcq(padrao(items) + "Qual é a parte que se repete, a partir da 1ª figura?", ok, [w1, w2, w3], "Olhe do começo: <b>%s</b>, e depois tudo de novo." % ok)


def s2_posicao():
    u = nucleo(R.choice([2, 3]))
    if not u:
        return None
    pos = R.choice([p for p in ORD if p > len(u) * 2 + 1])
    items = fil(u, len(u) * 2)
    ans = item_nome(u[(pos - 1) % len(u)])
    k = len(u)
    marks = ", ".join(str(k * j) for j in range(1, pos // k + 1))
    return mcq(padrao(items) + "A sequência continua igual. Qual será a %s figura?" % ORD[pos], ans, sorted(set(nomes(u)) - {ans}) + [x for x in ("quadrado verde", "círculo amarelo", "triângulo azul", "estrela", "pato") if x not in nomes(u)],
               "A parte que se repete tem %d figuras e termina nas posições %s. A %s figura é <b>%s</b>." % (k, marks, ORD[pos], ans))


def s3_contar():
    u = nucleo(R.choice([2, 3]))
    if not u:
        return None
    reps = R.randint(3, 5)
    n = len(u) * reps
    alvo = R.choice(u)
    c = sum(1 for x in fil(u, n) if x == alvo)
    nm = item_nome(alvo)
    return mcq(padrao(fil(u, len(u) * 2)) + "Se a sequência tiver %d figuras, quantas vezes aparece «%s»?" % (n, nm), str(c), [str(c + 1), str(n), str(reps + len(u)) if reps + len(u) != c else str(c - 1)],
               "A parte %s aparece %d vezes; em cada uma há %d «%s». Total: <b>%d</b>." % (", ".join(nomes(u)), reps, c // reps, nm, c))


LET = [["A", "B"], ["A", "B", "B"], ["A", "A", "B"], ["A", "B", "C"], ["X", "O"], ["X", "O", "O"], ["1", "2", "3"], ["M", "A", "R"]]
GESTOS = [["palma", "pé"], ["palma", "palma", "pé"], ["pula", "agacha"], ["palma", "estala os dedos", "pé"], ["mão na cabeça", "mão no ombro"]]


def s4_letras():
    if R.random() < 0.6:
        u = R.choice(LET)
        n = len(u) * 2 + R.randint(1, len(u))
        xs = fil(u, n)
        ans = u[n % len(u)]
        return mcq("Qual é a próxima letra ou número? <b>%s</b> ___" % " ".join(xs), ans, sorted(set(u) - {ans}) + [x for x in "BCDOZ" if x not in u],
                   "Repete %s. Depois de %s vem <b>%s</b>." % (" ".join(u), xs[-1], ans))
    u = R.choice(GESTOS)
    n = len(u) * 2 + R.randint(0, len(u) - 1)
    xs = fil(u, n)
    ans = u[n % len(u)]
    return mcq("Numa brincadeira, a turma faz: %s… O que vem depois?" % ", ".join(xs), ans, sorted(set(u) - {ans}) + ["senta", "gira", "grita"],
               "A parte que se repete é %s. Depois de «%s» vem <b>%s</b>." % (", ".join(u), xs[-1], ans))


def s4_criar():
    u = R.choice(LET[:6])
    ok = " ".join(fil(u, len(u) * 3))
    bad1 = " ".join(fil(u, len(u) * 2) + list(reversed(u)))
    bad2 = " ".join(fil(u[:-1] + [u[-1]] * 2, len(u) * 3)) if len(u) < 3 else " ".join(fil(u[1:], len(u) * 3))
    bad3 = " ".join(fil(u, len(u)) + list(reversed(u)) + fil(u, len(u)))
    return mcq("Qual sequência repete sempre «%s»?" % " ".join(u), ok, [bad1, bad2, bad3], "Leia de %d em %d: <b>%s</b>." % (len(u), len(u), ok))


def s5_crescer():
    k = R.choice(["torre", "escada", "palitos"])
    n = R.randint(4, 7)
    if k == "torre":
        a, d = R.randint(1, 3), R.choice([2, 3])
        v = a + d * (n - 1)
        return mcq("Uma torre tem %s. A cada dia, Lia põe mais %d. Quantos cubinhos terá no %dº dia?" % (pl(a, "cubinho", "cubinhos"), d, n), str(v), [str(v + d), str(d * n), str(v - d)],
                   "%s: <b>%d</b>." % (", ".join(str(a + d * i) for i in range(n)), v))
    if k == "escada":
        v = n * (n + 1) // 2
        return mcq("Uma escada de cubinhos tem 1 degrau com 1 cubinho, depois 2, depois 3… Quantos cubinhos tem o %dº degrau sozinho?" % n, str(n), [str(v), str(n + 1), str(n - 1)],
                   "O degrau 1 tem 1, o degrau 2 tem 2… o %dº degrau tem <b>%d</b>." % (n, n))
    v = 3 * n + 1
    return mcq("Com palitos, Davi faz quadradinhos em fila: 1 quadradinho usa 4 palitos, 2 usam 7, 3 usam 10. Quantos palitos para %d quadradinhos?" % n, str(v), [str(4 * n), str(v + 3), str(v - 3)],
               "Cada quadradinho novo usa mais 3 palitos: %s: <b>%d</b>." % (", ".join(str(3 * i + 1) for i in range(1, n + 1)), v))


def main():
    seen = set()
    sets = [
        ("Qual vem depois?", mix(R, seen, [(s1_proximo, 14), (s4_letras, 6)])),
        ("Qual figura falta?", mix(R, seen, [(s1_falta, 14), (s4_letras, 6)])),
        ("A parte que se repete", mix(R, seen, [(s2_parte, 15), (s4_criar, 5)])),
        ("Posições e contagem", mix(R, seen, [(s2_posicao, 12), (s3_contar, 8)])),
        ("Sequências que crescem", mix(R, seen, [(q_fig, 5), (s5_crescer, 15)])),
    ]
    body = lesson(
        ["Numa sequência <b>repetitiva</b>, uma parte se repete sempre igual: círculo, quadrado, círculo, quadrado…",
         "Para achar a parte que se repete, olhe <b>do começo</b> até a sequência voltar à 1ª figura.",
         "Para achar a figura de uma posição (a 10ª), conte de tantos em tantos: se a parte tem 2 figuras, a 10ª é a 2ª da parte.",
         "Numa sequência <b>que cresce</b>, cada figura tem um pouco mais que a anterior."],
        [("A, B, B, A, B, B, A, ___", ["parte que se repete: A, B, B"], "B"),
         ("Vermelho, azul, vermelho, azul… qual é a 8ª cor?", ["a parte tem 2 cores", "posições pares: azul"], "azul")],
        [["Olhar só a última figura", "Ache a parte que se repete inteira."],
         ["Achar que a parte tem 1 figura só", "Ela tem pelo menos 2 figuras diferentes."],
         ["Perder a conta da posição", "Marque as posições de 2 em 2 ou de 3 em 3."]],
        padrao([("shape", "circle", "red"), ("shape", "square", "blue"), ("shape", "square", "blue")] * 2 + [("shape", "circle", "red")], 1))
    faq = [("O que é uma sequência repetitiva?", "É uma sequência em que uma parte se repete sempre igual, como «palma, palma, pé». A BNCC pede que o 2º ano descreva o padrão com palavras, símbolos ou desenhos e descubra os elementos que faltam."),
           ("Como praticar padrões em casa?", "Monte filas com tampinhas de duas ou três cores, faça um colar de contas ou invente uma sequência de palmas e passos e peça para a criança continuar.")]
    make_unit(R, "padroes-e-sequencias-repetitivas", "A", ["EF02MA10", "EF02MA11"],
              "Descrever um padrão (ou regularidade) de sequências repetitivas e de sequências recursivas, por meio de palavras, símbolos ou desenhos; descrever os elementos ausentes em sequências repetitivas e em sequências recursivas de números naturais, objetos ou figuras",
              "Padrões e sequências repetitivas", "Padrões e sequências",
              "Atividades de matemática para o 2º ano sobre padrões e sequências repetitivas: figuras, cores, letras e gestos que se repetem, a parte que se repete, a figura que falta e sequências que crescem. 100 exercícios com gabarito.",
              "Ache a parte que se repete.", "Conte as posições de tantos em tantos.",
              body, faq, sets, 11, grade="2-ano")


if __name__ == "__main__":
    main()
