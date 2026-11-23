# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Sistema monetário: compra, venda, troco e desconto (Grandezas e medidas, EF04MA25)
  python3 tools/gen_br_matematica_4_sistema_monetario.py
Contar cédulas e moedas; troco; desconto em reais; pagamento à vista e parcelado; comparar preços (qual compra vale mais a pena);
planejar gastos e consumo consciente. Usa geradores do 3º ano (dinheiro) com outro sorteio.
Erros: esquecer os centavos no troco, confundir o desconto com o preço final, achar que o parcelado custa o mesmo quando há acréscimo.
"""
import random
from br_common import mcq, lesson, make_unit, mix, reais, dinheiro_svg, Kids, use

R = random.Random(80420)
K = Kids(R)
M3 = "gen_br_matematica_3_sistema_monetario"
m_moedas, m_notas, m_troca, m_troco, m_compra = use(M3, 80965, "s1_contar_moedas", "s1_contar_notas", "s2_troca", "s4_troco", "s5_compra")
ITENS = [("uma bicicleta", 350, 900), ("um tênis", 120, 300), ("uma mochila", 60, 180), ("um jogo de tabuleiro", 50, 150), ("uma bola de futebol", 40, 120),
         ("um patinete", 150, 400), ("uma lancheira", 30, 90), ("um fone de ouvido", 50, 200), ("um livro de histórias", 25, 70), ("uma camiseta do time", 80, 200)]


def cap(s):
    return s[0].upper() + s[1:]


def s2_troco():
    c = R.randint(110, 9500)
    if c % 5:
        return None
    pago = min(x for x in (500, 1000, 2000, 5000, 10000) if x > c)
    t = pago - c
    return mcq("Uma compra custou %s e foi paga com %s. Qual é o troco?" % (reais(c), reais(pago)), reais(t),
               [reais(x) for x in (t + 100, abs(t - 10), pago + c, t + 10) if x > 0], "%s − %s = <b>%s</b>." % (reais(pago), reais(c), reais(t)))


def s3_desconto():
    obj, lo, hi = R.choice(ITENS)
    p = R.randint(lo, hi) * 100
    d = R.choice([5, 10, 15, 20, 25, 30, 50]) * 100
    if d >= p // 2:
        return None
    if R.random() < 0.5:
        return mcq("%s custava %s e teve um desconto de %s. Quanto passou a custar?" % (cap(obj), reais(p), reais(d)), reais(p - d),
                   [reais(p + d), reais(d), reais(p - d - 1000)], "Desconto é o que se tira do preço: %s − %s = <b>%s</b>." % (reais(p), reais(d), reais(p - d)))
    return mcq("%s custava %s e, com desconto, passou a custar %s. De quanto foi o desconto?" % (cap(obj), reais(p), reais(p - d)), reais(d),
               [reais(p - d), reais(p + p - d), reais(d + 1000)], "%s − %s = <b>%s</b>." % (reais(p), reais(p - d), reais(d)))


def s3_parcelas():
    obj, lo, hi = R.choice(ITENS)
    n = R.choice([2, 3, 4, 5, 6, 10])
    par = R.randint(lo // n + 5, hi // n + 5)
    tot = par * n
    dd = R.choice([0, 5, 10, 15, 20, 30])
    if dd > tot // 8:
        return None
    vista = tot - dd
    k = R.choice(["total", "dif", "parcela"])
    if k == "total":
        return mcq("%s pode ser pago em %d parcelas de %s. Quanto se paga ao todo?" % (cap(obj), n, reais(par * 100)), reais(tot * 100),
                   [reais((par + n) * 100), reais((tot + par) * 100), reais(par * 100)], "%d × %s = <b>%s</b>." % (n, reais(par * 100), reais(tot * 100)))
    if k == "dif":
        if vista == tot:
            return None
        return mcq("%s custa %s à vista ou %d parcelas de %s. Quanto se economiza pagando à vista?" % (cap(obj), reais(vista * 100), n, reais(par * 100)), reais((tot - vista) * 100),
                   [reais(tot * 100), reais(vista * 100), reais((tot - vista + par) * 100)], "Parcelado: %d × %s = %s. %s − %s = <b>%s</b>." % (n, reais(par * 100), reais(tot * 100), reais(tot * 100), reais(vista * 100), reais((tot - vista) * 100)))
    return mcq("%s custa %s, em %d parcelas iguais, sem juros. Qual é o valor de cada parcela?" % (cap(obj), reais(tot * 100), n), reais(par * 100),
               [reais((tot - n) * 100), reais(par * 1000) if par < 100 else reais((par + 10) * 100), reais((par + 1) * 100)], "%s ÷ %d = <b>%s</b>." % (reais(tot * 100), n, reais(par * 100)))


def s4_melhor():
    prod = R.choice([("iogurtes", "pacote"), ("sabonetes", "pacote"), ("lápis", "caixa"), ("sucos", "caixa"), ("biscoitos", "pacote")])
    a, b = R.choice([(2, 4), (3, 6), (4, 8), (2, 6), (3, 9), (5, 10)])
    ua = R.randint(150, 450)
    ub = ua + R.choice([-40, -25, -20, -15, 15, 20, 30])
    if ub <= 0 or ua % 5 or ub % 5:
        return None
    pa, pb = ua * a, ub * b
    melhor = "o %s com %d" % (prod[1], b) if ub < ua else "o %s com %d" % (prod[1], a)
    pior = "o %s com %d" % (prod[1], a) if ub < ua else "o %s com %d" % (prod[1], b)
    return mcq("Um %s com %d %s custa %s. Um %s com %d custa %s. Qual compra sai mais barata por unidade?" % (prod[1], a, prod[0], reais(pa), prod[1], b, reais(pb)), melhor,
               [pior, "os dois saem iguais", "o que tiver o maior preço total"],
               "Por unidade: %s ÷ %d = %s e %s ÷ %d = %s. Mais barato: <b>%s</b>." % (reais(pa), a, reais(ua), reais(pb), b, reais(ub), melhor))


def s4_planejar():
    p, g = K.next()
    m = R.randint(20, 60)
    itens = R.sample([("um caderno", R.randint(8, 18)), ("uma caneta", R.randint(2, 6)), ("um lanche", R.randint(7, 15)), ("um gibi", R.randint(6, 12)),
                      ("uma borracha", R.randint(1, 4)), ("um suco", R.randint(3, 8))], 3)
    tot = sum(v for _, v in itens)
    if tot == m:
        return None
    ok = tot <= m
    lst = ", ".join("%s de %s" % (n, reais(v * 100)) for n, v in itens)
    ans = "Sim, e sobram %s" % reais((m - tot) * 100) if ok else "Não, faltam %s" % reais((tot - m) * 100)
    return mcq("%s tem %s e quer comprar %s. O dinheiro dá?" % (p, reais(m * 100), lst), ans,
               ["Não, faltam %s" % reais(abs(m - tot) * 100) if ok else "Sim, e sobram %s" % reais(abs(m - tot) * 100), "Sim, e sobram %s" % reais((m + tot) * 100) if ok else "Não, faltam %s" % reais((tot - m + 1) * 100), "Só dá para saber no caixa"],
               "Some: %s. Compare com %s: <b>%s</b>." % (reais(tot * 100), reais(m * 100), ans))


CONSUMO = [("Antes de comprar algo, uma boa atitude é…", "pensar se você realmente precisa", ["comprar logo para não perder", "comprar o mais caro", "pedir emprestado sempre"]),
           ("Comparar preços em lojas diferentes ajuda a…", "gastar menos pelo mesmo produto", ["gastar mais", "perder tempo à toa", "comprar mais do que precisa"]),
           ("Guardar uma parte da mesada todo mês ajuda a…", "juntar dinheiro para algo que você quer", ["gastar mais rápido", "perder o dinheiro", "pagar mais caro"]),
           ("Na promoção «leve 3, pague 2», se você só precisa de 1, o melhor é…", "pensar se vai usar os outros antes de levar", ["levar 3 sempre", "levar 10", "não comprar nada nunca"]),
           ("Pagar à vista com desconto, em vez de parcelado, geralmente…", "sai mais barato", ["sai mais caro", "sai igual sempre", "não é permitido"]),
           ("Pedir a nota fiscal na compra é importante porque…", "prova a compra e ajuda a trocar o produto", ["deixa o produto mais barato", "aumenta o troco", "não serve para nada"])]


def s5_consumo():
    q, a, w = R.choice(CONSUMO)
    return mcq(q, a, w, "Consumo consciente é comprar o que precisa, comparar preços e planejar. Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Contar dinheiro", mix(R, seen, [(m_moedas, 8), (m_notas, 6), (m_troca, 6)])),
        ("Troco", mix(R, seen, [(s2_troco, 12), (m_troco, 8)])),
        ("Desconto e parcelas", mix(R, seen, [(s3_desconto, 10), (s3_parcelas, 10)])),
        ("Comparar e planejar", mix(R, seen, [(s4_melhor, 10), (s4_planejar, 10)])),
        ("Compras e consumo consciente", mix(R, seen, [(m_compra, 14), (s5_consumo, 6)])),
    ]
    body = lesson(
        ["O <b>troco</b> é o que sobra do dinheiro dado: valor pago − preço.",
         "O <b>desconto</b> é o que se tira do preço; o preço final é preço − desconto.",
         "No pagamento <b>parcelado</b>, some todas as parcelas para saber o total e compare com o preço à vista.",
         "Para comparar ofertas, veja o preço de cada unidade. Compre o que precisa: isso é <b>consumo consciente</b>."],
        [("Compra de R$ 37,50 paga com R$ 50,00", ["50,00 − 37,50"], "R$ 12,50 de troco"),
         ("Patinete: R$ 280,00 à vista ou 4 × R$ 75,00", ["4 × 75 = 300", "300 − 280"], "R$ 20,00 a mais no parcelado")],
        [["Esquecer os centavos no troco", "Faça a conta com os centavos: 50,00 − 37,50 = 12,50."],
         ["Responder o desconto quando pedem o preço final", "Depois de achar o desconto, tire do preço."],
         ["Achar que o parcelado custa sempre o mesmo", "Multiplique a parcela pelo número de parcelas e compare."]],
        dinheiro_svg([5000, 2000, 500, 100, 50]))
    faq = [("O que o 4º ano estuda sobre dinheiro?", "A BNCC pede resolver e elaborar problemas de compra e venda e formas de pagamento, usando termos como troco e desconto, com ênfase no consumo ético, consciente e responsável."),
           ("Como falar de consumo consciente com crianças?", "Peça que comparem preços, calculem o troco e pensem se precisam mesmo do produto antes de comprar. Guardar uma parte da mesada também ajuda.")]
    make_unit(R, "sistema-monetario", "M", ["EF04MA25"],
              "Resolver e elaborar problemas que envolvam situações de compra e venda e formas de pagamento, utilizando termos como troco e desconto, enfatizando o consumo ético, consciente e responsável",
              "Sistema monetário: compra, troco, desconto e parcelas", "Dinheiro e compras",
              "Atividades de matemática para o 4º ano sobre o sistema monetário brasileiro: contar dinheiro, troco, desconto, pagamento à vista e parcelado, comparar preços e consumo consciente. 100 exercícios com gabarito.",
              "Troco = valor pago − preço.", "Preço final = preço − desconto.",
              body, faq, sets, 20, grade="4-ano")


if __name__ == "__main__":
    main()
