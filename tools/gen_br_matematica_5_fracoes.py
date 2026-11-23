# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Frações (Números, EF05MA03)
  python3 tools/gen_br_matematica_5_fracoes.py
Parte de um todo (figuras), leitura de frações, numerador e denominador; frações maiores que a unidade e números mistos;
fração como resultado de uma divisão; fração de uma quantidade; frações na reta numérica; problemas.
Erros: trocar numerador e denominador, contar as partes não pintadas, achar que 7/4 é menor que 1, 1/3 de 12 = 12 ÷ 1.
"""
import random
from br_common import mcq, num, pl, lesson, make_unit, mix, fr, faixa, disco, reta_frac, extenso, Kids

R = random.Random(80503)
K = Kids(R)
DEN = {2: ("meio", "meios"), 3: ("terço", "terços"), 4: ("quarto", "quartos"), 5: ("quinto", "quintos"), 6: ("sexto", "sextos"),
       7: ("sétimo", "sétimos"), 8: ("oitavo", "oitavos"), 9: ("nono", "nonos"), 10: ("décimo", "décimos"), 100: ("centésimo", "centésimos")}


def ler(a, b):
    """3/4 → três quartos, 5/12 → cinco doze avos"""
    na = "um" if a == 1 else extenso(a)
    if b in DEN:
        return na + " " + DEN[b][0 if a == 1 else 1]
    return na + " " + extenso(b) + " avos"


def fig(d, k):
    if k > d or d > 8 or R.random() < 0.5:
        return faixa(d, k)
    return disco(d, k)


def s1_figura():
    d = R.randint(3, 10)
    k = R.randint(1, d - 1)
    if R.random() < 0.5:
        return mcq(fig(d, k) + "Que fração da figura está pintada?", fr(k, d), [fr(d, k), fr(d - k, d) if d - k != k else fr(k, d + 1), fr(k, d - k) if d - k != k else fr(k + 1, d)],
                   "A figura tem %d partes iguais (denominador) e %d estão pintadas (numerador): <b>%s</b>." % (d, k, fr(k, d)))
    return mcq(fig(d, k) + "Que fração da figura <b>não</b> está pintada?", fr(d - k, d), [fr(k, d) if d - k != k else fr(k, d + 1), fr(d, d - k), fr(d - k, k) if d - k != k else fr(d - k + 1, d)],
               "Das %d partes, %d não estão pintadas: <b>%s</b>." % (d, d - k, fr(d - k, d)))


def s2_ler():
    b = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 100])
    a = R.randint(1, b - 1) if b < 100 else R.randint(1, 99)
    if R.random() < 0.5:
        w = [ler(b, a) if a > 1 else ler(a, b + 1), ler(a, b + 1) if b + 1 in DEN or b + 1 > 10 else ler(a + 1, b), ler(a + 1, b) if a + 1 < b else ler(a, b - 1), ler(b - a, b), ler(a, 2 * b)]
        return mcq("Como se lê %s?" % fr(a, b), ler(a, b), w, "%s se lê <b>%s</b>." % (fr(a, b), ler(a, b)))
    return mcq("Escreva a fração: <b>%s</b>." % ler(a, b), fr(a, b), [fr(b, a), fr(a, b + 1) if a < b + 1 else fr(a + 1, b), fr(a + 1, b) if a + 1 < b else fr(a, b - 1)],
               "«%s» = <b>%s</b>." % (ler(a, b), fr(a, b)))


TERMOS = [("Em %s, o numerador é…", "n"), ("Em %s, o denominador é…", "d"), ("Em %s, em quantas partes iguais o inteiro foi dividido?", "d"),
          ("Em %s, quantas partes foram tomadas?", "n")]


def s2_termos():
    b = R.randint(3, 12)
    a = R.randint(1, b - 1)
    if a == b - a:
        return None
    t, k = R.choice(TERMOS)
    ans, o = (a, b) if k == "n" else (b, a)
    return mcq(t % fr(a, b), str(ans), [str(o), str(a + b), str(b - a)],
               "O denominador (%d) diz em quantas partes iguais o inteiro foi dividido; o numerador (%d) diz quantas partes foram tomadas. Resposta: <b>%d</b>." % (b, a, ans))


def s3_impropria():
    d = R.randint(2, 6)
    k = R.randint(d + 1, 2 * d - 1)
    if R.random() < 0.5:
        return mcq(faixa(d, k) + "Cada faixa é 1 inteiro. Que fração está pintada ao todo?", fr(k, d), [fr(k, 2 * d), fr(d, k), fr(k - d, d)],
                   "Cada inteiro tem %d partes. Foram pintadas %d partes: <b>%s</b>, uma fração maior que 1." % (d, k, fr(k, d)))
    if d == 2:
        return None
    return mcq(faixa(d, k) + "Cada faixa é 1 inteiro. Que número misto representa a parte pintada?", "1 " + fr(k - d, d), ["%d %s" % (k - d, fr(1, d)), fr(k - d, d), "2 " + fr(k - d, d), "1 " + fr(2 * d - k, d)],
               "1 inteiro e mais %d de %d partes: <b>1 %s</b> (= %s)." % (k - d, d, fr(k - d, d), fr(k, d)))


def s3_misto():
    d = R.randint(2, 9)
    n = R.randint(1, 3)
    r = R.randint(1, d - 1)
    k = n * d + r
    if R.random() < 0.5:
        return mcq("Escreva %s como número misto." % fr(k, d), "%d %s" % (n, fr(r, d)), ["%d %s" % (r, fr(n, d)) if r != n else "%d %s" % (n + 1, fr(r, d)), "%d %s" % (n, fr(r, k)), "%d %s" % (k // 2, fr(r, d)) if k // 2 != n else "%d %s" % (n - 1 if n > 1 else n + 2, fr(r, d))],
                   "%d ÷ %d = %d e resto %d: %d inteiros e %s → <b>%d %s</b>." % (k, d, n, r, n, fr(r, d), n, fr(r, d)))
    if R.random() < 0.5:
        return mcq("Escreva %d %s como fração." % (n, fr(r, d)), fr(k, d), [fr(n + r, d), fr(n * r + d, d), fr(k, n * d), fr(n * d - r, d), fr(k + d, d)],
                   "%d inteiros = %d × %d = %d partes; mais %d: <b>%s</b>." % (n, n, d, n * d, r, fr(k, d)))
    ws = sorted({fr(x, d) for x in (r, d, 1, d - 1)})
    opts = [fr(k, d)] + ws[:3]
    if len(opts) < 4:
        return None
    R.shuffle(opts)
    return mcq("Qual destas frações é <b>maior que 1</b>? %s" % ", ".join(opts), fr(k, d), ws,
               "Uma fração é maior que 1 quando o numerador é maior que o denominador: <b>%s</b>." % fr(k, d))


COISA = [("pizzas", "pizza", "crianças", "criança"), ("barras de chocolate", "barra", "amigos", "amigo"), ("bolos", "bolo", "pessoas", "pessoa"),
         ("folhas de papel", "folha", "alunos", "aluno"), ("tortas", "torta", "vizinhos", "vizinho"), ("rapaduras", "rapadura", "primos", "primo")]


def s4_divisao():
    a = R.randint(2, 7)
    b = R.randint(a + 1, 9) if R.random() < 0.7 else R.randint(2, a - 1) if a > 2 else 3
    if a == b or a % b == 0:
        return None
    c, c1, quem, q1 = R.choice(COISA)
    um = "um" if c1 == "bolo" else "uma"
    return mcq("%d %s foram %s igualmente entre %d %s. Que parte de %s %s recebe cada %s?" % (a, c, "divididos" if c1 == "bolo" else "divididas", b, quem, um, c1, q1), fr(a, b),
               [fr(b, a), fr(1, b), fr(1, a)],
               "Dividir %d por %d dá a fração %s: %d ÷ %d = <b>%s</b>%s." % (a, b, fr(a, b), a, b, fr(a, b), "" if a < b else " (mais de %s %s %s)" % (um, c1, "inteiro" if c1 == "bolo" else "inteira")))


def s4_quantidade():
    d = R.choice([2, 3, 4, 5, 6, 8, 10])
    k = R.randint(1, d - 1)
    tot = d * R.randint(2, 12)
    obj = R.choice(["bolinhas de gude", "figurinhas", "lápis", "balas", "livros", "selos"])
    ans = tot // d * k
    return mcq("Quanto é %s de %d %s?" % (fr(k, d), tot, obj), "%d %s" % (ans, obj), ["%d %s" % (x, obj) for x in (tot // d, tot - ans, tot * k if tot * k < 500 else None, tot - tot // d, ans + d, tot + d) if x],
               "%d ÷ %d = %d (é %s); %d × %d = <b>%d</b>." % (tot, d, tot // d, fr(1, d), tot // d, k, ans))


def s5_reta():
    d = R.choice([2, 3, 4, 5, 6, 8])
    p = R.randint(1, 2 * d - 1)
    if p == d:
        return None
    svg = reta_frac(d, 2, [(p, "A")], width=360 if d <= 4 else 420)
    ans = fr(p, d)
    return mcq(svg + "Cada inteiro da reta foi dividido em %d partes iguais. Que fração a letra A marca?" % d, ans,
               [fr(p, 2 * d), fr(d, p), fr(p + 1, d), fr(p - 1, d) if p > 1 else fr(p, d + 1)],
               "Cada risquinho vale %s. A está no %dº risquinho depois do 0: <b>%s</b>%s." % (fr(1, d), p, ans, " (maior que 1)" if p > d else ""))


def s5_problema():
    k = R.choice(["pagina", "garrafa", "turma", "maior1", "pizza"])
    p, g = K.next()
    if k == "pagina":
        d = R.choice([4, 5, 8, 10])
        a = R.randint(1, d - 1)
        tot = d * R.randint(5, 20)
        return mcq("Um livro tem %d páginas. %s já leu %s do livro. Quantas páginas %s já leu?" % (tot, p, fr(a, d), g), str(tot // d * a),
                   [str(tot // d), str(tot - tot // d * a), str(tot * a), str(tot // d * (a + 1))], "%d ÷ %d × %d = <b>%d</b> páginas." % (tot, d, a, tot // d * a))
    if k == "garrafa":
        d = R.choice([3, 4, 5])
        n = R.randint(d + 1, 2 * d - 1)
        return mcq("%s encheu %d copos de %s de litro de suco. Quantos litros %s usou?" % (p, n, fr(1, d), g), fr(n, d) + " L",
                   [fr(1, n) + " L", fr(d, n) + " L", "%d L" % n, fr(1, d) + " L"],
                   "%d copos de %s = %s L, ou seja, 1 %s L. Resposta: <b>%s L</b>." % (n, fr(1, d), fr(n, d), fr(n - d, d), fr(n, d)))
    if k == "turma":
        tot = R.choice([24, 28, 30, 32, 36])
        d = R.choice([x for x in (2, 3, 4, 5, 6) if tot % x == 0])
        return mcq("Numa turma de %d alunos, %s dos alunos vão à escola de bicicleta. Quantos alunos vão de bicicleta?" % (tot, fr(1, d)), str(tot // d),
                   [str(tot - tot // d), str(tot * d) if tot * d < 300 else str(tot // d + d), str(d), str(tot // d * 2), str(tot + d)], "%s de %d = %d ÷ %d = <b>%d</b>." % (fr(1, d), tot, tot, d, tot // d))
    if k == "pizza":
        d = R.choice([4, 6, 8])
        a = R.randint(1, d - 2)
        b = R.randint(1, d - a - 1)
        q = K.next()[0]
        if q == p:
            return None
        return mcq("Uma pizza foi cortada em %d pedaços iguais. %s comeu %s e %s comeu %d. Que fração da pizza sobrou?" % (d, p, pl(a, "pedaço", "pedaços"), q, b), fr(d - a - b, d),
                   [fr(a + b, d), fr(d - a - b, a + b), fr(d - a, d), fr(d - b, d), fr(d - a - b, a + b + d)],
                   "Foram comidos %d de %d pedaços; sobraram %d: <b>%s</b>." % (a + b, d, d - a - b, fr(d - a - b, d)))
    d = R.randint(3, 8)
    a = R.randint(d + 1, 2 * d + 2)
    return mcq("%s disse que %s é menor que 1. Isso está certo?" % (p, fr(a, d)), "Não: %s é maior que 1" % fr(a, d), ["Sim: %s é menor que 1" % fr(a, d), "Não: %s é igual a 1" % fr(a, d), "Sim: o denominador é menor"],
               "O numerador %d é maior que o denominador %d: %s passa de 1 inteiro. <b>Não, é maior que 1.</b>" % (a, d, fr(a, d)))


def main():
    seen = set()
    sets = [
        ("Parte de um todo", mix(R, seen, [(s1_figura, 20)])),
        ("Ler frações", mix(R, seen, [(s2_ler, 12), (s2_termos, 8)])),
        ("Frações maiores que 1 e números mistos", mix(R, seen, [(s3_impropria, 8), (s3_misto, 12)])),
        ("Fração e divisão", mix(R, seen, [(s4_divisao, 10), (s4_quantidade, 10)])),
        ("Reta numérica e problemas", mix(R, seen, [(s5_reta, 8), (s5_problema, 12)])),
    ]
    body = lesson(
        ["O <b>denominador</b> (embaixo) diz em quantas partes iguais o inteiro foi dividido. O <b>numerador</b> (em cima) diz quantas partes foram tomadas.",
         "Quando o numerador é maior que o denominador, a fração é <b>maior que 1</b>: " + fr(7, 4) + " = 1 inteiro e " + fr(3, 4) + " = 1 " + fr(3, 4) + ".",
         "Uma fração também é uma <b>divisão</b>: 3 pizzas para 4 crianças → 3 ÷ 4 = " + fr(3, 4) + " de pizza para cada uma.",
         "Para achar " + fr(2, 5) + " de 20: 20 ÷ 5 = 4 e 4 × 2 = 8."],
        [("Escreva " + fr(11, 4) + " como número misto.", ["11 ÷ 4 = 2 e resto 3", "2 inteiros e " + fr(3, 4)], "2 " + fr(3, 4)),
         ("Quanto é " + fr(3, 8) + " de 40?", ["40 ÷ 8 = 5", "5 × 3 = 15"], "15")],
        [["Trocar numerador e denominador", "Embaixo fica o número de partes iguais do inteiro."],
         ["Contar as partes não pintadas", "Leia a pergunta: parte pintada ou parte que sobrou?"],
         ["Achar que " + fr(7, 4) + " é menor que 1", "7 partes de quartos passam de 4 quartos = 1 inteiro."]],
        faixa(4, 7))
    faq = [("O que o 5º ano estuda sobre frações?", "A BNCC pede identificar e representar frações menores e maiores que a unidade, ligando-as à divisão e à ideia de parte de um todo, e usar a reta numérica."),
           ("Como se lê " + "5/12" + "?", "Cinco doze avos. Para denominadores maiores que 10 (exceto 100, 1.000…) usamos a palavra «avos».")]
    make_unit(R, "fracoes", "N", ["EF05MA03"],
              "Identificar e representar frações (menores e maiores que a unidade), associando-as ao resultado de uma divisão ou à ideia de parte de um todo, utilizando a reta numérica como recurso",
              "Frações: parte de um todo, números mistos e divisão", "Frações",
              "Atividades de matemática para o 5º ano sobre frações: parte de um todo, leitura, frações maiores que 1, números mistos, fração como divisão, fração de uma quantidade e reta numérica. 100 exercícios com gabarito.",
              "Denominador: partes iguais do inteiro. Numerador: partes tomadas.", "Numerador maior que o denominador: a fração é maior que 1.",
              body, faq, sets, 3, grade="5-ano")


if __name__ == "__main__":
    main()
