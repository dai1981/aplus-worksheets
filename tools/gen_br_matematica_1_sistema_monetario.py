# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Sistema monetário: moedas e cédulas (Grandezas e medidas, EF01MA19)
  python3 tools/gen_br_matematica_1_sistema_monetario.py
Reconhecer moedas e cédulas do real; contar dinheiro até R$ 50; qual vale mais; trocas simples (2 moedas de 50 centavos = 1 real);
dá para comprar? quanto falta? Usa geradores do 2º ano (sistema monetário) com outro sorteio.
Erros: achar que a moeda maior vale mais, contar moedas em vez de somar os valores, confundir reais e centavos.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim, reais, dinheiro_svg, Kids

R = random.Random(80117)
K = Kids(R)
M2 = "gen_br_matematica_2_sistema_monetario"
L = (lim(50, 2),)
d_qual, d_equiv, d_quantia = use(M2, 80984, "s1_qual", "s2_equiv", "s3_quantia", preds=L)
NOTAS = [2, 5, 10, 20, 50]


def s1_mais():
    a, b = R.sample(NOTAS + [1], 2)
    big = max(a, b)
    return mcq(dinheiro_svg([a * 100, b * 100]) + "Qual vale mais: %s ou %s?" % (reais(a * 100), reais(b * 100)), reais(big * 100), [reais(min(a, b) * 100), "valem o mesmo", reais((a + b) * 100)],
               "%s é mais que %s: <b>%s</b>." % (reais(big * 100), reais(min(a, b) * 100), reais(big * 100)))


def s2_notas():
    ns = sorted([R.choice([2, 5, 10]) for _ in range(R.randint(2, 4))], reverse=True)
    t = sum(ns)
    return mcq(dinheiro_svg([n * 100 for n in ns]) + "Quanto dinheiro há?", reais(t * 100), [reais((t + 1) * 100), reais(len(ns) * 100), reais((t - 1) * 100)],
               "%s = <b>%s</b>." % (" + ".join(str(n) for n in ns), reais(t * 100)))


def s3_comprar():
    p, g = K.next()
    tem = R.choice([2, 5, 10, 20])
    preco = R.randint(1, 25)
    if preco == tem:
        return None
    obj = R.choice(["um picolé", "um caderno", "uma bola", "um suco", "um gibi", "uma pipa"])
    ok = "sim" if tem > preco else "não"
    return mcq("%s tem uma cédula de %s. %s custa %s. Dá para comprar?" % (p, reais(tem * 100), obj[0].upper() + obj[1:], reais(preco * 100)),
               "sim, e sobra troco" if ok == "sim" else "não, falta dinheiro", ["não, falta dinheiro" if ok == "sim" else "sim, e sobra troco", "só se pagar com moedas", "não dá para saber"],
               "%s %s %s: <b>%s</b>." % (reais(tem * 100), "&gt;" if tem > preco else "&lt;", reais(preco * 100), "sim, e sobra troco" if ok == "sim" else "não, falta dinheiro"))


def s3_falta():
    p, g = K.next()
    tem = R.randint(1, 15)
    preco = tem + R.randint(1, 9)
    return mcq("%s tem %s e quer um brinquedo de %s. Quantos reais faltam?" % (p, reais(tem * 100), reais(preco * 100)), reais((preco - tem) * 100),
               [reais((preco + tem) * 100), reais(tem * 100), reais((preco - tem + 1) * 100)], "%d + ___ = %d. Faltam <b>%s</b>." % (tem, preco, reais((preco - tem) * 100)))


def main():
    seen = set()
    sets = [
        ("Moedas e cédulas", mix(R, seen, [(d_qual, 9), (s1_mais, 11)])),
        ("Qual vale mais?", mix(R, seen, [(s1_mais, 15), (s3_comprar, 5)])),
        ("Contar dinheiro", mix(R, seen, [(s2_notas, 12), (d_quantia, 8)])),
        ("Trocas", mix(R, seen, [(d_equiv, 12), (d_quantia, 8)])),
        ("Comprar", mix(R, seen, [(s3_comprar, 10), (s3_falta, 10)])),
    ]
    body = lesson(
        ["O dinheiro do Brasil é o <b>real</b>. Escrevemos <b>R$</b>: R$ 5,00 são cinco reais.",
         "As cédulas são de 2, 5, 10, 20, 50, 100 e 200 reais. As moedas são de 5, 10, 25 e 50 centavos e de 1 real.",
         "O que importa é o número escrito, não o tamanho: uma moeda grande pode valer menos.",
         "Para contar, some os valores: uma cédula de 5 e uma de 2 são 7 reais."],
        [("Cédula de 10 e cédula de 5", ["10 + 5"], "R$ 15,00"),
         ("2 moedas de 50 centavos", ["50 + 50 = 100 centavos"], "1 real")],
        [["Achar que a moeda maior vale mais", "Leia o número da moeda."],
         ["Contar as moedas em vez de somar os valores", "Some o valor de cada uma."],
         ["Confundir reais e centavos", "100 centavos = 1 real."]],
        dinheiro_svg([1000, 500, 200, 100, 50]))
    faq = [("O que o 1º ano aprende sobre dinheiro?", "A BNCC pede reconhecer e relacionar valores de moedas e cédulas do real para resolver situações simples do dia a dia."),
           ("Como praticar em casa?", "Brinque de mercadinho com dinheiro de brinquedo: dê preços aos objetos e peça para a criança pagar e conferir o troco.")]
    make_unit(R, "sistema-monetario", "M", ["EF01MA19"],
              "Reconhecer e relacionar valores de moedas e cédulas do sistema monetário brasileiro para resolver situações simples do cotidiano do estudante",
              "Sistema monetário: moedas e cédulas do real", "Dinheiro",
              "Atividades de matemática para o 1º ano sobre o dinheiro do Brasil: moedas e cédulas do real, qual vale mais, contar dinheiro, trocas e compras. 100 exercícios com gabarito.",
              "Vale o número escrito, não o tamanho.", "100 centavos = 1 real.",
              body, faq, sets, 17, grade="1-ano")


if __name__ == "__main__":
    main()
