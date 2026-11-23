# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Divisão (Números, EF03MA08)
  python3 tools/gen_br_matematica_3_divisao.py
Divisão como repartição em partes iguais e como medida (quantas vezes cabe), divisão exata e com resto
(divisor até 10), relação com a multiplicação, dividir dezenas exatas, problemas em que o resto importa.
Erros: resto maior que o divisor, esquecer o resto, confundir repartir com quantas vezes cabe, arredondar errado
(precisa de mais um ônibus para o resto).
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, grupos, KINDS, COISAS, coisas, Kids, reais

R = random.Random(80309)
K = Kids(R)


def qr(q, r):
    return str(q) if r == 0 else "%d e resto %d" % (q, r)


def s1_repartir():
    d = R.randint(2, 5)
    q = R.randint(2, 6)
    kind = R.choice(KINDS)
    n = d * q
    nome = coisas(kind, 2).split(" ", 1)[1]
    (p, _) = K.next()
    return mcq(grupos(d, q, kind) + "%s repartiu %d %s igualmente em %d pratos, como na figura. Quantas ficaram em cada prato?" % (p, n, nome, d) if COISAS[kind][2] == "f"
               else grupos(d, q, kind) + "%s repartiu %d %s igualmente em %d pratos, como na figura. Quantos ficaram em cada prato?" % (p, n, nome, d),
               str(q), [str(d), str(n - d), str(q + 1), str(n + d)],
               "%d ÷ %d = <b>%d</b>, porque %d × %d = %d." % (n, d, q, d, q, n))


def s1_exata():
    d = R.randint(2, 10)
    q = R.randint(2, 10)
    n = d * q
    return mcq("Quanto é %d ÷ %d?" % (n, d), str(q), [str(q + 1), str(q - 1), str(n - d), str(d) if d != q else str(q + 2)],
               "Pense na multiplicação: %d × ___ = %d. %d × %d = %d, então <b>%d</b>." % (d, n, d, q, n, q))


def s2_resto():
    d = R.randint(2, 9)
    q = R.randint(2, 9)
    r = R.randint(1, d - 1)
    n = d * q + r
    w = [qr(q + 1, 0), qr(q, r + 1) if r + 1 < d else qr(q - 1, r + d), qr(q - 1, r + d), str(q)]
    return mcq("Quanto é %d ÷ %d?" % (n, d), qr(q, r), w,
               "%d × %d = %d e sobram %d − %d = %d. O resto (%d) é menor que %d: <b>%s</b>." % (d, q, d * q, n, d * q, r, r, d, qr(q, r)))


def s2_resto_so():
    d = R.randint(2, 10)
    q = R.randint(2, 9)
    r = R.randint(0, d - 1)
    n = d * q + r
    return mcq("Qual é o resto de %d ÷ %d?" % (n, d), str(r), [str(x) for x in (r + 1, d - r if d - r != r else r + 2, q, r + d) if x != r],
               "%d × %d = %d; %d − %d = <b>%d</b>." % (d, q, d * q, n, d * q, r))


def s3_medida():
    d = R.choice([2, 3, 4, 5, 6, 10])
    q = R.randint(3, 9)
    n = d * q
    k = R.choice(["fitas", "saquinhos", "grupos", "times"])
    if k == "fitas":
        return mcq("Uma fita tem %d cm. Quantos pedaços de %d cm dá para cortar?" % (n, d), str(q), [str(n - d), str(q + 1), str(d)],
                   "Quantas vezes %d cabe em %d? %d ÷ %d = <b>%d</b>." % (d, n, n, d, q))
    if k == "saquinhos":
        return mcq("Há %d balas. Cada saquinho leva %d balas. Quantos saquinhos ficam cheios?" % (n, d), str(q), [str(n - d), str(q + 1), str(d)],
                   "%d ÷ %d = <b>%d</b> saquinhos." % (n, d, q))
    if k == "grupos":
        return mcq("Na turma há %d alunos. A professora forma grupos de %d. Quantos grupos são?" % (n, d), str(q), [str(n + d), str(q - 1), str(d)],
                   "%d ÷ %d = <b>%d</b> grupos." % (n, d, q))
    return mcq("Na gincana há %d crianças. Cada time tem %d crianças. Quantos times são?" % (n, d), str(q), [str(n - d), str(q + 2), str(d)],
               "%d ÷ %d = <b>%d</b> times." % (n, d, q))


def s3_dezenas():
    d = R.choice([2, 3, 4, 5])
    q = R.randint(2, 9) * 10
    n = d * q
    if n > 400:
        return None
    return mcq("Quanto é %d ÷ %d?" % (n, d), str(q), [str(q // 10), str(q + 10), str(n - d)],
               "%d dezenas ÷ %d = %d dezenas = <b>%d</b>." % (n // 10, d, q // 10, q))


def s4_relacao():
    d, q = R.randint(2, 9), R.randint(2, 9)
    n = d * q
    k = R.choice(["mult", "fam", "prova"])
    if k == "mult":
        return mcq("Sabendo que %d × %d = %d, quanto é %d ÷ %d?" % (d, q, n, n, d), str(q), [str(n - d), str(d) if d != q else str(q + 1), str(q + 1)],
                   "A divisão desfaz a multiplicação: %d ÷ %d = <b>%d</b>." % (n, d, q))
    if k == "fam":
        if d == q:
            return None
        return mcq("Qual conta NÃO é da mesma família de %d × %d = %d?" % (d, q, n), "%d ÷ %d = %d" % (d, q, q),
                   ["%d ÷ %d = %d" % (n, d, q), "%d ÷ %d = %d" % (n, q, d), "%d × %d = %d" % (q, d, n)],
                   "%d ÷ %d não dá %d. As outras usam os mesmos três números: <b>%d ÷ %d = %d</b> não é da família." % (d, q, q, d, q, q))
    r = R.randint(1, d - 1) if d > 1 else 0
    return mcq("%d ÷ %d = %d e resto %d. Como conferir?" % (n + r, d, q, r), "%d × %d + %d = %d" % (d, q, r, n + r),
               ["%d × %d = %d" % (d, q, n + r), "%d + %d + %d = %d" % (d, q, r, d + q + r), "%d × %d − %d = %d" % (d, q, r, n - r)],
               "Divisor × quociente + resto = dividendo: <b>%d × %d + %d = %d</b>." % (d, q, r, n + r))


def s5_problema():
    p, _ = K.next()
    k = R.choice(["onibus", "caixas", "dinheiro", "pizza", "barcos", "biscoitos", "mesas"])
    if k == "onibus":
        c = R.choice([4, 5, 6, 8, 10])
        n = c * R.randint(3, 8) + R.randint(1, c - 1)
        q = n // c
        return mcq("%d pessoas vão passear de van. Cada van leva %d pessoas. Quantas vans são necessárias?" % (n, c), str(q + 1), [str(q), str(n - c), str(q + 2)],
                   "%d ÷ %d = %d e resto %d. As %d pessoas que sobram também precisam de lugar: <b>%d</b> vans." % (n, c, q, n % c, n % c, q + 1))
    if k == "caixas":
        c = R.choice([4, 6, 8, 10])
        n = c * R.randint(3, 9) + R.randint(1, c - 1)
        return mcq("Uma granja tem %d ovos e enche caixas de %d. Quantas caixas ficam cheias e quantos ovos sobram?" % (n, c), "%d caixas e sobram %d" % (n // c, n % c),
                   ["%d caixas e sobram %d" % (n // c + 1, 0), "%d caixas e sobram %d" % (n // c - 1, n % c + c), "%d caixas e sobram %d" % (n // c, n % c + 1)],
                   "%d ÷ %d = %d e resto %d: <b>%d caixas e sobram %d</b>." % (n, c, n // c, n % c, n // c, n % c))
    if k == "dinheiro":
        d = R.randint(2, 5)
        q = R.randint(3, 12)
        return mcq("%s quer dividir %s igualmente entre %d amigos. Quanto cada um recebe?" % (p, reais(d * q * 100), d), reais(q * 100),
                   [reais((d * q - d) * 100), reais((q + 1) * 100), reais(d * 100) if d != q else reais((q + 2) * 100)],
                   "%d ÷ %d = %d: <b>%s</b>." % (d * q, d, q, reais(q * 100)))
    if k == "pizza":
        f = R.choice([4, 6, 8])
        pz = R.randint(2, 4)
        pes = R.choice([x for x in (2, 3, 4, 6, 8) if pz * f % x == 0 and x != f])
        return mcq("Há %d pizzas com %d fatias cada uma. As fatias serão repartidas igualmente entre %d pessoas. Quantas fatias cada pessoa come?" % (pz, f, pes),
                   str(pz * f // pes), [str(pz * f), str(f // pes) if f // pes and f % pes == 0 and f // pes != pz * f // pes else str(pz * f // pes + 1), str(pz * f - pes)],
                   "%d × %d = %d fatias; %d ÷ %d = <b>%d</b>." % (pz, f, pz * f, pz * f, pes, pz * f // pes))
    if k == "barcos":
        c = R.choice([3, 4, 5])
        n = c * R.randint(4, 9) + R.randint(1, c - 1)
        return mcq("No passeio de barco cabem %d crianças por barco. Há %d crianças. Quantos barcos são necessários para levar todas?" % (c, n), str(n // c + 1),
                   [str(n // c), str(n // c + 2), str(n - c)],
                   "%d ÷ %d = %d e resto %d: precisa de mais um barco para as que sobram. <b>%d</b> barcos." % (n, c, n // c, n % c, n // c + 1))
    if k == "biscoitos":
        d = R.randint(3, 6)
        q = R.randint(3, 8)
        r = R.randint(1, d - 1)
        n = d * q + r
        return mcq("%s tem %d biscoitos e quer dividir igualmente entre %d amigos. Quantos biscoitos sobram?" % (p, n, d), str(r), [str(q), str(r + 1), str(d - r) if d - r != r else str(r + 2)],
                   "%d ÷ %d = %d e resto %d. Sobram <b>%d</b>." % (n, d, q, r, r))
    m = R.randint(4, 9)
    c = R.choice([4, 6])
    return mcq("Numa festa, %d pessoas vão se sentar em mesas de %d lugares. Quantas mesas ficam completas?" % (m * c, c), str(m), [str(m * c - c), str(m + 1), str(c)],
               "%d ÷ %d = <b>%d</b> mesas." % (m * c, c, m))


def main():
    seen = set()
    sets = [
        ("Repartir em partes iguais", mix(R, seen, [(s1_repartir, 8), (s1_exata, 12)])),
        ("Divisão com resto", mix(R, seen, [(s2_resto, 12), (s2_resto_so, 8)])),
        ("Quantas vezes cabe? e dezenas exatas", mix(R, seen, [(s3_medida, 12), (s3_dezenas, 8)])),
        ("Divisão e multiplicação", mix(R, seen, [(s4_relacao, 20)])),
        ("Problemas de divisão", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Dividir é <b>repartir em partes iguais</b> (12 balas para 3 crianças: 4 para cada uma) ou ver <b>quantas vezes cabe</b> (em 12 cabem 3 grupos de 4).",
         "A divisão é a operação inversa da multiplicação: 20 ÷ 4 = 5 porque 4 × 5 = 20.",
         "Quando não dá exato, sobra um <b>resto</b>. O resto é sempre <b>menor que o divisor</b>: 17 ÷ 5 = 3 e resto 2.",
         "Leia a pergunta do problema: às vezes o resto precisa de mais um grupo (mais uma van, mais um barco)."],
        [("23 ÷ 4", ["4 × 5 = 20", "23 − 20 = 3"], "5 e resto 3"),
         ("26 pessoas em vans de 8 lugares", ["26 ÷ 8 = 3 e resto 2", "As 2 que sobram precisam de mais uma van"], "4 vans")],
        [["17 ÷ 5 = 2 e resto 7", "O resto não pode ser maior que 5: cabe mais um 5. Resposta: 3 e resto 2."],
         ["Esquecer o resto", "Confira: divisor × quociente + resto = dividendo."],
         ["Responder 3 vans para 26 pessoas", "Ninguém pode ficar de fora: são 4 vans."]])
    faq = [("O que a BNCC pede de divisão no 3º ano?", "Problemas de divisão de um número natural por outro (até 10), com resto zero e com resto diferente de zero, com os significados de repartição em partes iguais e de medida."),
           ("Como ensinar a divisão com resto?", "Use objetos de verdade: distribua feijões ou tampinhas em pratos até não dar mais para dar um para cada. O que sobra na mão é o resto.")]
    make_unit(R, "divisao", "N", ["EF03MA08"],
              "Resolver e elaborar problemas de divisão de um número natural por outro (até 10), com resto zero e com resto diferente de zero, com os significados de repartição equitativa e de medida, por meio de estratégias e registros pessoais",
              "Divisão exata e com resto", "Divisão",
              "Atividades de matemática para o 3º ano sobre divisão: repartir em partes iguais, quantas vezes cabe, divisão exata e com resto, relação com a multiplicação e problemas. 100 exercícios com gabarito.",
              "O resto é sempre menor que o divisor.", "Divisor × quociente + resto = dividendo.",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
