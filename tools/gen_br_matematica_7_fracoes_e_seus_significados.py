# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Frações e seus significados (Números, EF07MA05–EF07MA09)
  python3 tools/gen_br_matematica_7_fracoes_e_seus_significados.py
Fração como parte de um todo, como quociente, como razão (comparar duas grandezas) e como operador (fração de uma quantidade e
fração de fração); problemas em etapas («gastou 1/3 e depois 1/4 do resto»); multiplicação e divisão de frações em problemas.
Erros: aplicar a segunda fração ao total e não ao resto, inverter a razão, somar quando é «fração de fração».
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, fq, bank, unit

R = random.Random(87004)


def s1_razao():
    a, b = R.randint(2, 20), R.randint(2, 20)
    if a == b:
        return None
    k = R.choice(["pp", "pt"])
    ctx = R.choice([("meninas", "meninos", "alunos"), ("gols de cabeça", "gols de pé", "gols"), ("bolas azuis", "bolas vermelhas", "bolas")])
    if k == "pp":
        return M("Num grupo há %d %s e %d %s. Qual é a razão entre %s e %s?" % (a, ctx[0], b, ctx[1], ctx[0], ctx[1]), fq(F(a, b)), [fq(F(b, a)), fq(F(a, a + b)), fq(F(b, a + b))],
                 "Razão de %s para %s: %d/%d = <b>%s</b>." % (ctx[0], ctx[1], a, b, fq(F(a, b))))
    return M("Num grupo há %d %s e %d %s. Que fração do total de %s são %s?" % (a, ctx[0], b, ctx[1], ctx[2], ctx[0]), fq(F(a, a + b)), [fq(F(a, b)), fq(F(b, a + b)), fq(F(b, a))],
             "Parte ÷ todo: %d/%d = <b>%s</b>." % (a, a + b, fq(F(a, a + b))))


def s2_operador():
    f1 = F(R.randint(1, 4), R.randint(2, 6))
    f2 = F(R.randint(1, 4), R.randint(2, 6))
    if f1 >= 1 or f2 >= 1:
        return None
    k = R.choice(["ff", "fq"])
    if k == "ff":
        r = f1 * f2
        return M("Quanto é %s de %s?" % (fq(f1), fq(f2)), fq(r), [fq(f1 + f2) if f1 + f2 != r else fq(r * 2), fq(f1 / f2) if f1 != f2 else fq(r + F(1, 10)), fq(abs(f2 - f1)) if f1 != f2 and abs(f2 - f1) != r else fq(F(1, 2)) if r != F(1, 2) else fq(F(1, 3))],
                 "«De» é multiplicação: %s × %s = <b>%s</b>." % (fq(f1), fq(f2), fq(r)))
    q = f1.denominator * f2.denominator * R.randint(2, 6)
    r = q * f1 * f2
    return M("Quanto é %s de %s de %d?" % (fq(f1), fq(f2), q), d(r), [d(q * f2), d(q * (f1 + f2)) if (q * (f1 + f2)).denominator == 1 else d(r + 1), d(q * f1)],
             "%s de %d = %s; %s disso = <b>%s</b>." % (fq(f2), q, d(q * f2), fq(f1), d(r)))


def s3_etapas():
    a, b = R.choice([(F(1, 3), F(1, 4)), (F(1, 4), F(1, 3)), (F(1, 2), F(1, 3)), (F(2, 5), F(1, 2)), (F(1, 3), F(1, 2)), (F(3, 8), F(2, 5)), (F(1, 5), F(1, 4))])
    t = a.denominator * b.denominator * R.randint(2, 10) * (10 if R.random() < 0.5 else 1)
    g1 = t * a
    g2 = (t - g1) * b
    sobra = t - g1 - g2
    if g2.denominator != 1:
        return None
    k = R.choice(["dinheiro", "livro"])
    if k == "dinheiro":
        return M("Leo tinha %s. Gastou %s com roupas e %s do que sobrou com livros. Com quanto ficou?" % (reais(t * 100), fq(a), fq(b)), reais(int(sobra) * 100), [reais(int(t - t * a - t * b) * 100), reais(int(g2) * 100), reais(int(t - g1) * 100)],
                 "Roupas: %s; sobram %s; livros: %s de %s = %s; fica com <b>%s</b>." % (d(g1), d(t - g1), fq(b), d(t - g1), d(g2), reais(int(sobra) * 100)))
    return M("Um livro tem %d páginas. No 1º dia, Ana leu %s do livro; no 2º, leu %s do que faltava. Quantas páginas ainda faltam?" % (t, fq(a), fq(b)), d(sobra), [d(t - t * a - t * b), d(g1 + g2), d(t - g1)],
             "1º dia: %s; faltam %s; 2º dia: %s; faltam <b>%s</b>." % (d(g1), d(t - g1), d(g2), d(sobra)))


def s4_mult_div():
    k = R.choice(["vezes", "quantos"])
    if k == "vezes":
        n, f = R.randint(2, 12), F(R.randint(1, 5), R.randint(2, 8))
        if f >= 1:
            return None
        return M("Uma receita usa %s de xícara de açúcar. Quanto açúcar vai em %d receitas?" % (fq(f), n), fq(n * f) + (" xícara" if n * f <= 1 else " xícaras") if (n * f).denominator != 1 else d(n * f) + (" xícara" if n * f == 1 else " xícaras"),
                 [fq(F(f.numerator, f.denominator * n)) + " de xícara", fq(f + n) + " xícaras", fq(F(n, f.denominator)) + " de xícara" if F(n, f.denominator) != n * f else fq(f) + " de xícara"],
                 "%d × %s = <b>%s</b>." % (n, fq(f), fq(n * f) if (n * f).denominator != 1 else d(n * f)))
    tot, f = R.randint(2, 9), R.choice([F(1, 2), F(1, 3), F(1, 4), F(3, 4), F(2, 3), F(1, 5)])
    n = tot / f
    if n.denominator != 1:
        return None
    return M("Quantas garrafas de %s de litro enchemos com %d litros de suco?" % (fq(f), tot), d(n), [d(tot * f) if (tot * f).denominator == 1 else fq(tot * f), d(n + 1), d(tot + f.denominator)],
             "%d ÷ %s = %d × %s = <b>%s</b>." % (tot, fq(f), tot, fq(1 / f), d(n)))


s5_significados = bank(R, [
    ("Em «3/4 de uma pizza», a fração é…", "parte de um todo", ["razão entre duas grandezas", "um número negativo", "uma porcentagem acima de 100%"]),
    ("Dividir 3 chocolates igualmente entre 4 crianças dá 3/4 para cada uma. Aqui a fração é…", "um quociente (divisão)", ["uma razão de escala", "um número inteiro", "um operador sobre 100"]),
    ("Em «para cada 2 copos de água, 3 de suco», a fração 2/3 é…", "uma razão", ["uma parte do total de 2 copos", "um quociente de 3 por 2", "um número maior que 1"]),
    ("Em «2/5 dos 30 alunos», a fração age como…", "operador sobre uma quantidade", ["razão de escala", "número negativo", "denominador"]),
    ("Numa escala 1 : 500, a fração 1/500 indica…", "uma razão entre o desenho e o real", ["parte de uma pizza", "um número maior que 1", "uma divisão por zero"]),
    ("Se a razão entre meninas e meninos é 3/5, a fração de meninas na turma é…", "3/8", ["3/5", "5/8", "5/3"]),
    ("Multiplicar um número por 1/2 é o mesmo que…", "dividir por 2", ["multiplicar por 2", "somar 1/2", "subtrair 2"]),
    ("Dividir por 1/3 é o mesmo que…", "multiplicar por 3", ["dividir por 3", "multiplicar por 1/3", "somar 3"]),
], "s5_significados")


def main():
    seen = set()
    sets = [
        ("Fração como razão", mix(R, seen, [(s1_razao, 20)])),
        ("Fração de fração", mix(R, seen, [(s2_operador, 20)])),
        ("Problemas em etapas", mix(R, seen, [(s3_etapas, 20)])),
        ("Multiplicar e dividir em problemas", mix(R, seen, [(s4_mult_div, 14), (s5_significados, 6)])),
        ("Revisão", mix(R, seen, [(s1_razao, 6), (s2_operador, 6), (s3_etapas, 6), (s5_significados, 2)])),
    ]
    body = lesson(
        ["Uma fração pode ser <b>parte de um todo</b> (3/4 da pizza), <b>quociente</b> (3 ÷ 4), <b>razão</b> (3 meninas para 4 meninos) ou <b>operador</b> (3/4 de 40).",
         "«Fração de fração» é multiplicação: 2/3 de 3/5 = 2/3 × 3/5 = 2/5.",
         "Em problemas em etapas, leia com atenção: «1/4 do que sobrou» é calculado sobre o resto, não sobre o total."],
        [("R$ 120,00: gasta 1/3, depois 1/4 do resto", ["1/3 de 120 = 40", "sobra 80", "1/4 de 80 = 20"], "fica com R$ 60,00"),
         ("6 meninas e 9 meninos", ["razão 6/9 = 2/3", "fração do total 6/15 = 2/5"], "2/3 e 2/5")],
        [["Aplicar a segunda fração ao total", "«Do resto» muda a base do cálculo."],
         ["Inverter a razão", "A ordem importa: meninas para meninos."],
         ["Somar «fração de fração»", "«De» quer dizer multiplicar."]])
    faq = [("Quais são os significados de uma fração?", "Parte de um todo, quociente de uma divisão, razão entre duas grandezas e operador que age sobre uma quantidade (por exemplo, 2/5 de 30)."),
           ("O que a BNCC pede no 7º ano?", "Resolver problemas que envolvam frações com diferentes significados (EF07MA05–EF07MA07), comparar e ordenar frações associadas às ideias de parte de inteiros, resultado da divisão, razão e operador (EF07MA08) e utilizar a fração como operador (EF07MA09).")]
    unit(R, "fracoes-e-seus-significados", "N", ["EF07MA05", "EF07MA06", "EF07MA07", "EF07MA08", "EF07MA09"],
         "Resolver um mesmo problema utilizando diferentes algoritmos; comparar e ordenar frações associadas às ideias de partes de inteiros, resultado da divisão, razão e operador; utilizar, na resolução de problemas, a associação entre razão e fração, como a fração 2/3 para expressar a razão de duas partes de uma grandeza para três partes da mesma ou três partes de outra grandeza",
         "Frações: parte, quociente, razão e operador", "Frações e seus significados",
         "Atividades de matemática para o 7º ano sobre frações e seus significados: razão, fração de fração, fração de uma quantidade, problemas em etapas e multiplicação e divisão de frações. 100 exercícios com gabarito.",
         "«De» é multiplicar.", "«Do resto»: calcule sobre o que sobrou.",
         body, faq, sets, 4, grade="7-ano")


if __name__ == "__main__":
    main()
