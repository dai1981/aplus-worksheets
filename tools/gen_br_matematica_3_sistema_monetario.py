# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Sistema monetário brasileiro (Grandezas e medidas, EF03MA24)
  python3 tools/gen_br_matematica_3_sistema_monetario.py
Moedas (5, 10, 25 e 50 centavos, 1 real) e cédulas (2, 5, 10, 20, 50, 100 e 200 reais); contar dinheiro;
equivalências (2 moedas de 50 centavos = 1 real); comparar valores; comprar, vender e trocar; calcular o troco.
Erros: contar moedas e não o valor, achar que 100 centavos é menos que 1 real, esquecer que 1 real = 100 centavos no troco.
"""
import random
from br_common import mcq, lesson, make_unit, mix, dinheiro_svg, reais, Kids, num

R = random.Random(80320)
K = Kids(R)
COINS = [5, 10, 25, 50, 100]
NOTES = [200, 500, 1000, 2000, 5000, 10000, 20000]


def nome(c):
    if c >= 200:
        return "cédula de %s" % reais(c).replace(",00", "")
    if c == 100:
        return "moeda de 1 real"
    return "moeda de %d centavos" % c


def s1_contar_moedas():
    items = sorted([R.choice(COINS) for _ in range(R.randint(3, 6))], reverse=True)
    t = sum(items)
    return mcq(dinheiro_svg(items) + "Quanto dinheiro há na figura?", reais(t), [reais(len(items) * 100), reais(t + 5), reais(t - 10) if t > 10 else reais(t + 25), reais(t + 25)],
               "Some os valores das moedas: %s = <b>%s</b>." % (" + ".join(reais(c) if c >= 100 else "%d centavos" % c for c in items), reais(t)))


def s1_contar_notas():
    items = sorted(R.sample(NOTES[:6], R.randint(2, 4)) + [R.choice(COINS)] * R.randint(0, 2), reverse=True)
    t = sum(items)
    return mcq(dinheiro_svg(items) + "Quanto dinheiro há na figura?", reais(t), [reais(t + 500), reais(t - 100) if t > 100 else reais(t + 100), reais(t * 10) if t < 1000 else reais(t + 1000)],
               "Some primeiro as cédulas e depois as moedas: <b>%s</b>." % reais(t))


EQ = [("Quantas moedas de 50 centavos formam 1 real?", "2", ["5", "50", "4"]), ("Quantas moedas de 25 centavos formam 1 real?", "4", ["25", "5", "2"]),
      ("Quantas moedas de 10 centavos formam 1 real?", "10", ["100", "5", "20"]), ("Quantas moedas de 5 centavos formam 1 real?", "20", ["5", "10", "50"]),
      ("Quantas cédulas de 2 reais formam 10 reais?", "5", ["2", "8", "20"]), ("Quantas cédulas de 5 reais formam 20 reais?", "4", ["5", "15", "2"]),
      ("Quantas cédulas de 10 reais formam 50 reais?", "5", ["10", "4", "40"]), ("Quantas cédulas de 20 reais formam 100 reais?", "5", ["20", "4", "80"]),
      ("Quantas cédulas de 50 reais formam 200 reais?", "4", ["2", "5", "150"]), ("Quantas moedas de 25 centavos formam 50 centavos?", "2", ["25", "5", "4"]),
      ("1 real é igual a quantos centavos?", "100 centavos", ["10 centavos", "1.000 centavos", "50 centavos"]),
      ("Quantas cédulas de 5 reais formam 100 reais?", "20", ["5", "10", "50"])]


def s2_equivalencia():
    q, a, w = R.choice(EQ)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def s2_troca():
    k = R.choice(["igual", "falta"])
    if k == "igual":
        v = R.choice([100, 200, 500, 1000, 2000, 5000])
        good = {100: "2 moedas de 50 centavos", 200: "4 moedas de 50 centavos", 500: "2 cédulas de 2 reais e 1 moeda de 1 real", 1000: "2 cédulas de 5 reais",
                2000: "2 cédulas de 10 reais", 5000: "2 cédulas de 20 reais e 1 de 10 reais"}[v]
        bad = {100: ["5 moedas de 10 centavos", "3 moedas de 25 centavos", "1 moeda de 50 centavos e 2 de 10 centavos"],
               200: ["2 moedas de 50 centavos", "5 moedas de 25 centavos", "1 moeda de 1 real e 1 de 25 centavos"],
               500: ["2 cédulas de 2 reais", "5 moedas de 50 centavos", "1 cédula de 2 reais e 2 moedas de 1 real"],
               1000: ["5 cédulas de 1 real", "1 cédula de 5 reais e 2 de 2 reais", "4 cédulas de 2 reais"],
               2000: ["2 cédulas de 5 reais", "1 cédula de 10 reais e 2 de 2 reais", "3 cédulas de 5 reais"],
               5000: ["2 cédulas de 20 reais", "5 cédulas de 5 reais", "1 cédula de 20 reais e 2 de 10 reais"]}[v]
        bad = [b.replace("cédulas de 1 real", "moedas de 1 real") for b in bad]
        return mcq("Qual destas opções vale o mesmo que %s?" % reais(v), good, bad, "Some cada opção: só <b>%s</b> dá %s." % (good, reais(v)))
    t = R.choice([500, 1000])
    a = R.choice([150, 175, 225, 275, 350, 425, 480, 620, 735, 860])
    if a >= t:
        return None
    return mcq("%s tem %s. Quanto falta para ter %s?" % (K.next()[0], reais(a), reais(t)), reais(t - a), [reais(t - a + 50), reais(t + a), reais(abs(t - a - 25))],
               "%s − %s = <b>%s</b>." % (reais(t), reais(a), reais(t - a)))


def s3_comparar():
    a = R.choice([125, 175, 230, 350, 480, 510, 999, 1050])
    b = a + R.choice([-75, -25, 25, 60, 100])
    if b <= 0:
        return None
    (p1, _), (p2, _) = K.two()
    win = p1 if a > b else p2
    return mcq("%s tem %s e %s tem %s. Quem tem mais dinheiro?" % (p1, reais(a), p2, reais(b)), win, [p2 if win == p1 else p1, "os dois têm o mesmo valor", "quem tem mais moedas"],
               "%s %s %s: <b>%s</b>." % (reais(a), "&gt;" if a > b else "&lt;", reais(b), win))


def s3_centavos():
    k = R.choice(["mais", "eq"])
    if k == "mais":
        r = R.randint(1, 3)
        c = R.choice([80, 150, 250, 300, 350])
        big = reais(r * 100) if r * 100 > c else ("%d centavos" % c if c < 100 else reais(c))
        other = "%d centavos" % c if c < 100 else reais(c)
        if r * 100 == c:
            return None
        return mcq("O que vale mais: %s ou %d centavos?" % (reais(r * 100), c), big if r * 100 > c else "%d centavos" % c,
                   [reais(r * 100) if r * 100 < c else "%d centavos" % c, "valem o mesmo", "não dá para comparar"],
                   "%s = %d centavos: %s." % (reais(r * 100), r * 100, "<b>%s</b> vale mais" % (reais(r * 100) if r * 100 > c else "%d centavos" % c)))
    c = R.choice([150, 225, 375, 410, 1250, 505])
    return mcq("%d centavos é o mesmo que…" % c, reais(c), [reais(c * 10), reais(c + 100), reais(c // 10), reais(c * 100)],
               "100 centavos = 1 real: %d centavos = <b>%s</b>." % (c, reais(c)))


def s4_troco():
    p, _ = K.next()
    preco = R.choice([350, 475, 620, 799, 1250, 1590, 2380, 3490, 875, 1120])
    pago = [x for x in (500, 1000, 2000, 5000) if x > preco][0]
    tr = pago - preco
    obj = R.choice(["um caderno", "uma bola", "um livro", "um sorvete", "um brinquedo", "um suco", "uma caixa de lápis"])
    return mcq("%s comprou %s de %s e pagou com uma cédula de %s. Quanto recebeu de troco?" % (p, obj, reais(preco), reais(pago).replace(",00", "")), reais(tr),
               [reais(tr + 100), reais(abs(tr - 10)), reais(pago + preco), reais((pago - preco) // 100 * 100) if tr % 100 else reais(tr + 50)],
               "%s − %s = <b>%s</b>." % (reais(pago), reais(preco), reais(tr)))


ITENS = [("pão de queijo", 350), ("suco", 500), ("pastel", 650), ("pipoca", 400), ("água", 250), ("picolé", 300), ("coxinha", 550), ("pedaço de bolo", 450)]
FEM = {"pipoca", "água", "coxinha"}


def um(x):
    return ("uma " if x in FEM else "um ") + x


def s5_compra():
    p, _ = K.next()
    k = R.choice(["dois", "vezes", "da", "sobra"])
    (a, pa), (b, pb) = R.sample(ITENS, 2)
    if k == "dois":
        return mcq("Na cantina, %s custa %s e %s custa %s. Quanto %s gasta ao todo?" % (um(a), reais(pa), um(b), reais(pb), p), reais(pa + pb),
                   [reais(abs(pa - pb)), reais(pa + pb + 100), reais(pa + pb - 50)], "%s + %s = <b>%s</b>." % (reais(pa), reais(pb), reais(pa + pb)))
    if k == "vezes":
        n = R.randint(2, 4)
        return mcq("Na cantina, %s custa %s. Quanto custam %d?" % (um(a), reais(pa), n), reais(pa * n), [reais(pa + n * 100), reais(pa * (n + 1)), reais(pa * n + 50)],
                   "%d × %s = <b>%s</b>." % (n, reais(pa), reais(pa * n)))
    if k == "da":
        t = R.choice([1000, 1500, 2000])
        n = t // pa
        sobra = t - n * pa
        return mcq("%s tem %s. Quantas unidades de %s, que custa %s, dá para comprar, no máximo?" % (p, reais(t), a, reais(pa)), str(n),
                   [str(n + 1), str(n - 1) if n > 1 else "3", str(t // 100)],
                   ("%d × %s = %s; sobram %s, que não dá para mais um. Resposta: <b>%d</b>." % (n, reais(pa), reais(n * pa), reais(sobra), n)) if sobra else
                   "%d × %s = %s: <b>%d</b>." % (n, reais(pa), reais(t), n))
    t = R.choice([1000, 2000])
    return mcq("%s levou %s à cantina e comprou %s (%s) e %s (%s). Quanto sobrou?" % (p, reais(t), um(a), reais(pa), um(b), reais(pb)), reais(t - pa - pb),
               [reais(t - pa), reais(pa + pb), reais(t - pa - pb + 100)], "%s + %s = %s; %s − %s = <b>%s</b>." % (reais(pa), reais(pb), reais(pa + pb), reais(t), reais(pa + pb), reais(t - pa - pb)))


def main():
    seen = set()
    sets = [
        ("Contar moedas e cédulas", mix(R, seen, [(s1_contar_moedas, 12), (s1_contar_notas, 8)])),
        ("Trocas e equivalências", mix(R, seen, [(s2_equivalencia, 12), (s2_troca, 8)])),
        ("Reais e centavos: comparar", mix(R, seen, [(s3_comparar, 10), (s3_centavos, 10)])),
        ("Calcular o troco", mix(R, seen, [(s4_troco, 20)])),
        ("Problemas de compra e venda", mix(R, seen, [(s5_compra, 20)])),
    ]
    body = lesson(
        ["O dinheiro do Brasil é o <b>real</b> (R$). 1 real = 100 centavos.",
         "Moedas: 5, 10, 25 e 50 centavos e 1 real. Cédulas: 2, 5, 10, 20, 50, 100 e 200 reais.",
         "Para contar, some primeiro as cédulas de maior valor e depois as moedas. Escrevemos R$ 3,50: 3 reais e 50 centavos.",
         "O <b>troco</b> é o valor pago menos o preço: pagou R$ 10,00 por algo de R$ 6,75 → troco de R$ 3,25."],
        [("1 cédula de R$ 10, 2 moedas de R$ 1 e 1 moeda de 50 centavos", ["10 + 2 = 12 reais", "mais 50 centavos"], "R$ 12,50"),
         ("Troco de R$ 20,00 para uma compra de R$ 13,40", ["R$ 13,40 → R$ 14,00: 60 centavos", "R$ 14,00 → R$ 20,00: 6 reais"], "R$ 6,60")],
        [["Contar as moedas em vez do valor", "Cinco moedas não são 5 reais: some o valor de cada uma."],
         ["Achar que 100 centavos é menos que 1 real", "100 centavos = 1 real."],
         ["Errar o troco ao passar dos centavos", "Complete primeiro até o real seguinte e depois conte os reais."]],
        dinheiro_svg([1000, 100, 100, 50]))
    faq = [("O que a BNCC pede sobre dinheiro no 3º ano?", "Resolver e elaborar problemas que envolvam a comparação e a equivalência de valores monetários do sistema brasileiro em situações de compra, venda e troca."),
           ("Como praticar com dinheiro em casa?", "Brinque de mercadinho com moedas e cédulas de brinquedo: a criança paga, confere o preço e calcula o troco.")]
    make_unit(R, "sistema-monetario", "M", ["EF03MA24"],
              "Resolver e elaborar problemas que envolvam a comparação e a equivalência de valores monetários do sistema brasileiro em situações de compra, venda e troca",
              "Sistema monetário brasileiro: reais e centavos", "Sistema monetário",
              "Atividades de matemática para o 3º ano sobre o sistema monetário brasileiro: moedas e cédulas, contar dinheiro, equivalências, reais e centavos, troco, compra e venda. 100 exercícios com gabarito.",
              "1 real = 100 centavos.", "Troco = valor pago − preço.",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
