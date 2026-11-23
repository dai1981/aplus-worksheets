# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Princípio fundamental da contagem (EM13MAT310)
  python3 tools/gen_br_matematica_em2_principio_fundamental_da_contagem.py
Princípio multiplicativo e aditivo, árvore de possibilidades; senhas, placas, números com algarismos distintos,
restrições (começar por, ser par, não repetir), caminhos, cardápios; fatorial.
Usa geradores do 8º ano (combinar, senhas, números, filas) com outro sorteio.
Erros: somar quando é «e» (etapas), multiplicar quando é «ou» (casos), esquecer que o 0 não pode iniciar um número.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, num
import math

R = random.Random(92011)
c_comb, c_senha, c_num, c_fila = use("gen_br_matematica_8_principio_multiplicativo", 92909, "s1_combinar", "s2_senhas", "s3_numeros", "s4_filas")


def s1_placas():
    k = R.choice(["placa", "placa_br", "cod", "aditivo"])
    if k == "placa":
        L, N = R.choice([(2, 3), (3, 3), (3, 4), (2, 4)])
        v = 26 ** L * 10 ** N
        return M("Quantas placas com %d letras (26 possíveis) seguidas de %d algarismos podem ser formadas, podendo repetir?" % (L, N), num(v), [num(26 * L + 10 * N), num(26 ** L + 10 ** N), num(26 * L * 10 * N)],
                 "26%s · 10%s = <b>%s</b>." % ("²" if L == 2 else "³", "³" if N == 3 else "⁴", num(v)))
    if k == "placa_br":
        return M("No padrão Mercosul, uma placa tem 4 letras e 3 algarismos em posições fixas. Usando 26 letras e 10 algarismos, com repetição, quantas placas existem?", num(26 ** 4 * 10 ** 3), [num(26 * 4 + 10 * 3), num(26 ** 3 * 10 ** 4), num(26 ** 4 + 10 ** 3)], "26⁴ · 10³ = <b>%s</b>." % num(26 ** 4 * 10 ** 3))
    if k == "cod":
        n = R.choice([3, 4, 5])
        s = R.choice([2, 3])
        return M("Um código é formado por %d símbolos, cada um podendo ser um de %d tipos. Quantos códigos diferentes existem?" % (n, s), num(s ** n), [num(s * n), num(n ** s), num(s ** n - 1)], "%d%s = <b>%s</b>." % (s, "²³⁴⁵"[n - 2], num(s ** n)))
    a, b, c = R.randint(2, 8), R.randint(2, 8), R.randint(2, 6)
    return M("Para ir de A a C, pode-se passar por B (%d caminhos de A a B e %d de B a C) ou ir direto (%d caminhos de A a C). Quantos caminhos há de A a C?" % (a, b, c), str(a * b + c), [str(a + b + c), str(a * b * c), str(a * b)],
             "Por B: %d · %d = %d; direto: %d; total (ou): %d + %d = <b>%d</b>." % (a, b, a * b, c, a * b, c, a * b + c))


def s2_restricao():
    k = R.choice(["par", "dist", "comeca", "impar", "maior"])
    if k == "par":
        n = R.choice([3, 4])
        # algarismos 1..9 (sem zero), distintos, número par
        v = 4 * math.perm(8, n - 1)
        return M("Com os algarismos de 1 a 9, quantos números pares de %d algarismos distintos podem ser formados?" % n, num(v), [num(math.perm(9, n)), num(4 * 9 ** (n - 1)), num(5 * math.perm(8, n - 1))],
                 "Último: 4 opções (2, 4, 6, 8); os outros: %s = <b>%s</b>." % (" · ".join(str(8 - i) for i in range(n - 1)) + " · 4", num(v)))
    if k == "dist":
        n = R.choice([3, 4])
        v = 9 * math.perm(9, n - 1)
        return M("Quantos números de %d algarismos distintos existem (de 0 a 9, sem começar por 0)?" % n, num(v), [num(math.perm(10, n)), num(9 * 10 ** (n - 1)), num(10 ** n)],
                 "1º: 9 opções (sem 0); depois %s: %s = <b>%s</b>." % (", ".join(str(9 - i) for i in range(n - 1)), "9 · " + " · ".join(str(9 - i) for i in range(n - 1)), num(v)))
    if k == "comeca":
        n = R.choice([4, 5, 6])
        return M("De quantas maneiras %d pessoas podem formar uma fila se uma delas, Ana, deve ser a primeira?" % n, num(math.factorial(n - 1)), [num(math.factorial(n)), num(n - 1), num(math.factorial(n) - 1)], "Ana fixa; as outras %d: %d! = <b>%s</b>." % (n - 1, n - 1, num(math.factorial(n - 1))))
    if k == "impar":
        digs = sorted(R.sample(range(1, 10), R.choice([4, 5])))
        imp = [x for x in digs if x % 2]
        if not imp:
            return None
        n = len(digs)
        v = len(imp) * math.perm(n - 1, 2)
        return M("Com os algarismos %s, sem repetir, quantos números ímpares de 3 algarismos podem ser formados?" % ", ".join(map(str, digs)), num(v), [num(math.perm(n, 3)), num(len(imp) * n * n), num((n - len(imp)) * math.perm(n - 1, 2)) if n - len(imp) != len(imp) else num(v + n)],
                 "Último: %d ímpar%s; depois %d · %d: <b>%s</b>." % (len(imp), "es" if len(imp) > 1 else "", n - 1, n - 2, num(v)))
    n = R.choice([5, 6])
    return M("Numa corrida com %d atletas, de quantas maneiras podem ser ocupados o 1º, o 2º e o 3º lugares?" % n, num(n * (n - 1) * (n - 2)), [num(n ** 3), num(math.comb(n, 3)), num(3 * n)], "%d · %d · %d = <b>%s</b>." % (n, n - 1, n - 2, num(n * (n - 1) * (n - 2))))


def s3_fatorial():
    k = R.choice(["val", "razao", "simpl"])
    if k == "val":
        n = R.randint(3, 8)
        return M("Quanto vale %d!?" % n, num(math.factorial(n)), [num(n * (n + 1) // 2), num(n ** 2), num(math.factorial(n - 1))], "%s = <b>%s</b>." % (" · ".join(str(i) for i in range(n, 0, -1)), num(math.factorial(n))))
    if k == "razao":
        n = R.randint(5, 12)
        m = n - R.choice([1, 2, 3])
        v = math.factorial(n) // math.factorial(m)
        return M("Quanto vale %d! ÷ %d!?" % (n, m), num(v), [num(n - m), "%s!" % (n - m), num(n)], "%s = <b>%s</b>." % (" · ".join(str(i) for i in range(n, m, -1)), num(v)))
    n = R.randint(3, 9)
    return M("Simplifique (n + 1)! ÷ n! para n = %d." % n, str(n + 1), [str(n), num(math.factorial(n)), "1"], "(n + 1)! = (n + 1) · n!; o resultado é n + 1 = <b>%d</b>." % (n + 1))


def main():
    seen = set()
    sets = [
        ("Princípio multiplicativo", mix(R, seen, [(c_comb, 13), (c_senha, 7)])),
        ("Placas, códigos e caminhos", mix(R, seen, [(s1_placas, 20)])),
        ("Números e restrições", mix(R, seen, [(s2_restricao, 14), (c_num, 6)])),
        ("Filas e fatorial", mix(R, seen, [(s3_fatorial, 12), (c_fila, 8)])),
        ("Revisão", mix(R, seen, [(s2_restricao, 10), (s1_placas, 6), (s3_fatorial, 4)])),
    ]
    body = lesson(
        ["<b>Princípio multiplicativo</b>: se uma escolha é feita em etapas («e»), multiplique as possibilidades de cada etapa.",
         "<b>Princípio aditivo</b>: se há casos separados («ou»), some as possibilidades de cada caso.",
         "Comece pelas posições com <b>restrição</b> (o 1º algarismo não pode ser 0; o último deve ser par).",
         "<b>Fatorial</b>: n! = n · (n − 1) · … · 1. É o número de filas com n pessoas. 0! = 1."],
        [("Números pares de 3 algarismos distintos com 1 a 9", ["último: 4 opções", "depois 8 e 7"], "4 · 8 · 7 = 224")],
        [["Somar quando são etapas", "«E» multiplica; «ou» soma."],
         ["Começar por 0", "Um número de 3 algarismos não começa por 0."],
         ["Deixar a restrição para o fim", "Preencha primeiro a posição com restrição."]])
    faq = [("Quando somar e quando multiplicar na contagem?", "Multiplique quando a escolha é feita em etapas que acontecem juntas («e»). Some quando são casos que não acontecem juntos («ou»)."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas de contagem envolvendo agrupamentos ordenáveis ou não de elementos, por meio dos princípios multiplicativo e aditivo, recorrendo a estratégias diversas, como o diagrama de árvore (EM13MAT310).")]
    unit(R, "principio-fundamental-da-contagem", "E", ["EM13MAT310"],
         "Resolver e elaborar problemas de contagem envolvendo agrupamentos ordenáveis ou não de elementos, por meio dos princípios multiplicativo e aditivo, recorrendo a estratégias diversas, como o diagrama de árvore",
         "Princípio fundamental da contagem", "Princípio fundamental da contagem",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre contagem: princípio multiplicativo e aditivo, senhas, placas, números com restrições, filas e fatorial. 100 exercícios com gabarito.",
         "Etapas («e»): multiplique", "Casos («ou»): some.",
         body, faq, sets, 11, grade="2-serie")


if __name__ == "__main__":
    main()
