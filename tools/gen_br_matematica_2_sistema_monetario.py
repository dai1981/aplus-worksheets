# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Sistema monetário: moedas e cédulas (Grandezas e medidas, EF02MA20)
  python3 tools/gen_br_matematica_2_sistema_monetario.py
Reconhecer moedas e cédulas do real; contar dinheiro; equivalências (2 moedas de 50 centavos = 1 real, 5 cédulas de 2 reais = 10 reais);
comparar quantias; quanto falta; troco e compras simples até R$ 100. Usa geradores do 3º ano com outro sorteio.
Erros: contar a quantidade de moedas em vez do valor, achar que a moeda maior vale mais, esquecer que 100 centavos = 1 real.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim, reais, dinheiro_svg, Kids

R = random.Random(80219)
K = Kids(R)
M3 = "gen_br_matematica_3_sistema_monetario"
L = (lim(100, 2),)
d_moedas, d_notas, d_falta, d_comp, d_troco, d_compra = use(M3, 80912, "s1_contar_moedas", "s1_contar_notas", "s2_troca", "s3_comparar", "s4_troco", "s5_compra", preds=L)
NOTAS = [2, 5, 10, 20, 50, 100]
MOEDAS = [5, 10, 25, 50, 100]


def nome_moeda(c):
    return "1 real" if c == 100 else "%d centavos" % c


def s1_qual():
    if R.random() < 0.5:
        v = R.choice(NOTAS[:-1])
        return mcq(dinheiro_svg([v * 100]) + "Quanto vale esta cédula?", reais(v * 100), [reais(x * 100) for x in NOTAS if x != v][:3] + [reais(v * 10)],
                   "Está escrito na cédula: <b>%s</b>." % reais(v * 100))
    c = R.choice(MOEDAS)
    return mcq(dinheiro_svg([c]) + "Quanto vale esta moeda?", nome_moeda(c), [nome_moeda(x) for x in MOEDAS if x != c], "Leia o número da moeda: <b>%s</b>." % nome_moeda(c))


EQ = [(50, 2, 100), (25, 4, 100), (10, 10, 100), (5, 2, 10), (25, 2, 50), (10, 5, 50), (5, 10, 50), (10, 2, 20), (5, 5, 25)]


def s2_equiv():
    if R.random() < 0.5:
        c, n, tot = R.choice(EQ)
        return mcq("Quantas moedas de %s formam %s?" % (nome_moeda(c), "1 real" if tot == 100 else "%d centavos" % tot), str(n), [str(n + 1), str(n * 2), str(max(1, n - 1)) if n > 2 else str(n + 3)],
                   "%s = %s: <b>%d moedas</b>." % (" + ".join([str(c)] * n), tot, n))
    a, b = R.choice([(2, 10), (5, 10), (10, 20), (10, 50), (2, 20), (5, 20), (20, 100), (50, 100), (10, 100), (5, 50), (2, 50)])
    n = b // a
    return mcq("Quantas cédulas de %s formam %s?" % (reais(a * 100), reais(b * 100)), str(n), [str(n + 1), str(n - 1), str(n * 2)],
               "%d × %d = %d: <b>%d cédulas</b>." % (n, a, b, n))


def s2_trocar():
    v = R.choice([10, 20, 50, 100])
    ops = {10: [([5, 5], True), ([2, 2, 2, 2, 2], True), ([5, 2, 2], False), ([2, 2, 2, 2], False)],
           20: [([10, 10], True), ([10, 5, 5], True), ([10, 5, 2], False), ([5, 5, 5], False)],
           50: [([20, 20, 10], True), ([10, 10, 10, 10, 10], True), ([20, 20, 5], False), ([20, 10, 10], False)],
           100: [([50, 50], True), ([50, 20, 20, 10], True), ([50, 20, 20], False), ([20, 20, 20, 20], False)]}[v]
    good = [o for o, ok in ops if ok]
    bad = [o for o, ok in ops if not ok]
    g = R.choice(good)
    f = lambda xs: " + ".join(reais(x * 100) for x in xs)
    return mcq("Qual troca vale o mesmo que uma cédula de %s?" % reais(v * 100), f(g), [f(b) for b in bad] + [f([v // 2])],
               "%s = %s. Resposta: <b>%s</b>." % (f(g), reais(v * 100), f(g)))


def s3_quantia():
    notas = sorted(R.sample(NOTAS[:4], R.randint(1, 3)), reverse=True)
    moedas = sorted([R.choice(MOEDAS) for _ in range(R.randint(1, 3))], reverse=True)
    tot = sum(n * 100 for n in notas) + sum(moedas)
    if tot > 5000:
        return None
    pic = dinheiro_svg([n * 100 for n in notas] + moedas)
    return mcq(pic + "Quanto dinheiro há ao todo?", reais(tot), [reais(tot + 100), reais(tot - min(moedas)), reais(sum(n * 100 for n in notas) + 100 * len(moedas)) if sum(n * 100 for n in notas) + 100 * len(moedas) != tot else reais(tot + 50)],
               "Cédulas: %s. Moedas: %s. Total: <b>%s</b>." % (reais(sum(n * 100 for n in notas)), reais(sum(moedas)), reais(tot)))


def s4_pagar():
    p, g = K.next()
    preco = R.randint(3, 48)
    k = R.choice(["cedula", "falta"])
    if k == "cedula":
        n = min(x for x in (5, 10, 20, 50) if x > preco)
        return mcq("Um brinquedo custa %s. Qual é a menor cédula que %s pode usar para pagar com uma só cédula?" % (reais(preco * 100), p), reais(n * 100),
                   [reais(x * 100) for x in (2, 5, 10, 20, 50, 100) if x != n and (x < preco or x > n)][:3],
                   "Precisa ser maior ou igual a %s: <b>%s</b>." % (reais(preco * 100), reais(n * 100)))
    tem = R.randint(1, preco - 1)
    return mcq("%s tem %s e quer comprar um livro de %s. Quanto falta?" % (p, reais(tem * 100), reais(preco * 100)), reais((preco - tem) * 100),
               [reais((preco + tem) * 100), reais(tem * 100), reais((preco - tem + 1) * 100)], "%d − %d = %d: <b>%s</b>." % (preco, tem, preco - tem, reais((preco - tem) * 100)))


def main():
    seen = set()
    sets = [
        ("Moedas e cédulas do real", mix(R, seen, [(s1_qual, 10), (d_moedas, 10)])),
        ("Trocas e equivalências", mix(R, seen, [(s2_equiv, 16), (s2_trocar, 4)])),
        ("Contar dinheiro", mix(R, seen, [(d_notas, 8), (s3_quantia, 12)])),
        ("Comparar e quanto falta", mix(R, seen, [(d_comp, 8), (d_falta, 6), (s4_pagar, 6)])),
        ("Compras e troco", mix(R, seen, [(d_troco, 10), (d_compra, 10)])),
    ]
    body = lesson(
        ["O dinheiro do Brasil é o <b>real</b> (R$). Há cédulas de 2, 5, 10, 20, 50, 100 e 200 reais.",
         "As moedas são de 5, 10, 25 e 50 centavos e de 1 real. <b>100 centavos = 1 real</b>.",
         "Para contar, comece pelas cédulas de maior valor e depois some as moedas.",
         "Quantias iguais podem ser formadas de jeitos diferentes: 2 moedas de 50 centavos = 1 real."],
        [("1 cédula de 10, 1 de 5 e 2 moedas de 1 real", ["10 + 5 = 15", "15 + 2 = 17"], "R$ 17,00"),
         ("Quantas moedas de 25 centavos formam 1 real?", ["25 + 25 + 25 + 25 = 100"], "4 moedas")],
        [["Contar a quantidade de moedas em vez do valor", "Some o valor de cada moeda."],
         ["Achar que a moeda maior vale mais", "Leia o número escrito na moeda."],
         ["Esquecer que 100 centavos = 1 real", "2 moedas de 50 centavos = 1 real."]],
        dinheiro_svg([1000, 500, 100, 100]))
    faq = [("O que o 2º ano aprende sobre dinheiro?", "A BNCC pede estabelecer a equivalência de valores entre moedas e cédulas do sistema monetário brasileiro para resolver situações do dia a dia."),
           ("Como praticar com dinheiro em casa?", "Brinque de lojinha com dinheiro de brinquedo: a criança paga, troca cédulas por moedas e confere o troco.")]
    make_unit(R, "sistema-monetario", "M", ["EF02MA20"],
              "Estabelecer a equivalência de valores entre moedas e cédulas do sistema monetário brasileiro para resolver situações cotidianas",
              "Sistema monetário: moedas e cédulas do real", "Dinheiro",
              "Atividades de matemática para o 2º ano sobre o sistema monetário brasileiro: moedas e cédulas do real, contar dinheiro, trocas e equivalências, quanto falta e troco. 100 exercícios com gabarito.",
              "100 centavos = 1 real.", "Comece a contar pelas cédulas maiores.",
              body, faq, sets, 19, grade="2-ano")


if __name__ == "__main__":
    main()
