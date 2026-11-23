# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Frações unitárias (Números, EF04MA09)
  python3 tools/gen_br_matematica_4_fracoes_unitarias.py
As frações unitárias mais usadas (1/2, 1/3, 1/4, 1/5, 1/10 e 1/100): nas figuras, na leitura, na reta numérica e na forma decimal
(0,5; 0,25; 0,2; 0,1; 0,01); fração de uma quantidade; comparar frações unitárias; medidas menores que a unidade (meio metro, um quarto de hora).
Erros: achar que 1/5 é maior que 1/3 porque 5 > 3, multiplicar em vez de dividir (1/4 de 20 = 80), escrever 1/4 = 0,4.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, fr, faixa, disco, reta_frac, reais, Kids

R = random.Random(80408)
K = Kids(R)
US = [2, 3, 4, 5, 10]
NOME = {2: "um meio (metade)", 3: "um terço", 4: "um quarto", 5: "um quinto", 10: "um décimo", 100: "um centésimo"}
DEC = {2: "0,5", 4: "0,25", 5: "0,2", 10: "0,1", 100: "0,01"}


def s1_figura():
    d = R.choice(US + [6, 8])
    pic = faixa(d, 1) if R.random() < 0.5 or d > 8 else disco(d, 1)
    w = [fr(1, x) for x in (d + 1, d - 1 if d > 2 else 5, 2 * d)] + [fr(d - 1, d) if d > 2 else fr(2, 1), fr(d, 1)]
    return mcq(pic + "Que fração da figura está pintada?", fr(1, d), w,
               "A figura foi dividida em %d partes iguais e 1 está pintada: <b>%s</b>." % (d, fr(1, d)))


def s1_nome():
    d = R.choice(US + [100])
    if R.random() < 0.5:
        return mcq("Como se lê %s?" % fr(1, d), NOME[d], [NOME[x] for x in US + [100] if x != d][:3] if d != 100 else [NOME[10], NOME[2], "um cem"],
                   "%s se lê <b>%s</b>." % (fr(1, d), NOME[d]))
    return mcq("Em quantas partes iguais o inteiro foi dividido na fração %s?" % fr(1, d), str(d), ["1", str(d + 1), str(d * 2)],
               "O denominador (%d) diz em quantas partes iguais o inteiro foi dividido: <b>%d</b>." % (d, d))


def s2_quantidade():
    d = R.choice(US)
    n = d * R.randint(2, 20)
    obj = R.choice(["balas", "figurinhas", "laranjas", "lápis", "alunos", "bolinhas"])
    return mcq("Quanto é %s de %d %s?" % (fr(1, d), n, obj), "%d %s" % (n // d, obj), ["%d %s" % (x, obj) for x in (n - n // d, n * d if n * d < 1000 else n // 2 + 1, n // d + d, n - d)],
               "%s de %d é dividir por %d: %d ÷ %d = <b>%d</b>." % (fr(1, d), n, d, n, d, n // d))


def s2_comparar():
    a, b = R.sample(US + [6, 8, 100], 2)
    big = a if a < b else b
    k = R.choice(["maior", "menor"])
    ans = fr(1, min(a, b)) if k == "maior" else fr(1, max(a, b))
    oth = fr(1, max(a, b)) if k == "maior" else fr(1, min(a, b))
    return mcq("Qual fração é %s: %s ou %s?" % (k, fr(1, a), fr(1, b)), ans, [oth, "são iguais", "não dá para comparar"],
               "Com numerador 1, quanto <b>maior</b> o denominador, <b>menor</b> a parte (o inteiro foi dividido em mais pedaços). Resposta: <b>%s</b>." % ans)


def s3_decimal():
    d = R.choice([2, 4, 5, 10, 100])
    if R.random() < 0.6:
        wr = {2: ["0,2", "1,2", "0,12"], 4: ["0,4", "1,4", "0,14"], 5: ["0,5", "1,5", "0,15"], 10: ["1,0", "0,01", "10"], 100: ["0,1", "100", "1,1"]}[d]
        return mcq("Que número decimal é igual a %s?" % fr(1, d), DEC[d], wr,
                   "%s = %s: <b>%s</b>." % (fr(1, d), {2: "5 décimos", 4: "25 centésimos", 5: "2 décimos", 10: "1 décimo", 100: "1 centésimo"}[d], DEC[d]))
    return mcq("Que fração unitária é igual a %s?" % DEC[d], fr(1, d), [fr(1, x) for x in (2, 4, 5, 10, 100) if x != d][:3],
               "%s = <b>%s</b>." % (DEC[d], fr(1, d)))


def s3_reta():
    d = R.choice([2, 3, 4, 5, 10])
    p = 1 if R.random() < 0.7 else R.randint(2, d - 1) if d > 2 else 1
    svg = reta_frac(d, 1, [(p, "A")], width=360)
    ans = fr(p, d)
    return mcq(svg + "A reta vai de 0 a 1, dividida em %d partes iguais. Que fração a letra A marca?" % d, ans,
               [fr(1, d + 1), fr(p, d + 1) if p > 1 else fr(1, d - 1) if d > 2 else fr(1, 3), fr(d - p, d) if d - p != p else fr(p + 1, d), fr(d, p) if p > 1 else fr(d, 1)],
               "Cada parte vale %s. A está no %dº risquinho: <b>%s</b>." % (fr(1, d), p, ans))


def s4_medida():
    k = R.choice(["metro", "hora", "real", "litro", "quilo", "dia"])
    d = {"metro": R.choice([2, 4, 5, 10, 100]), "hora": R.choice([2, 4, 3]), "real": R.choice([2, 4, 5, 10]), "litro": R.choice([2, 4, 5, 10]),
         "quilo": R.choice([2, 4, 5, 10]), "dia": R.choice([2, 3, 4])}[k]
    tot, un, nome = {"metro": (100, "cm", "1 metro (100 cm)"), "hora": (60, "minutos", "1 hora (60 minutos)"), "real": (100, "centavos", "1 real (100 centavos)"),
                     "litro": (1000, "mL", "1 litro (1.000 mL)"), "quilo": (1000, "g", "1 quilograma (1.000 g)"), "dia": (24, "horas", "1 dia (24 horas)")}[k]
    v = tot // d
    return mcq("Quanto é %s de %s?" % (fr(1, d), nome), "%s %s" % (num(v), un), ["%s %s" % (num(x), un) for x in (d, tot - v, v * 2 if v * 2 < tot else v // 2, tot // 10 if d != 10 else tot // 4)],
               "%s ÷ %d = <b>%s %s</b>." % (num(tot), d, num(v), un))


def s5_problema():
    k = R.choice(["pizza", "chocolate", "turma", "dinheiro", "garrafa", "caminho"])
    p, g = K.next()
    q = K.next()[0]
    if k == "pizza":
        a, b = R.sample([2, 3, 4, 6, 8], 2)
        if p == q:
            return None
        return mcq("%s comeu %s de uma pizza. %s comeu %s de uma pizza igual. Quem comeu mais?" % (p, fr(1, a), q, fr(1, b)), p if a < b else q, [q if a < b else p, "Comeram a mesma quantidade", "Não dá para saber"],
                   "Com numerador 1, o menor denominador indica a parte maior: <b>%s</b>." % (p if a < b else q))
    if k == "chocolate":
        d = R.choice([4, 5, 10])
        return mcq("Uma barra de chocolate tem %d pedaços iguais. %s comeu 1 pedaço. Que fração da barra %s comeu?" % (d, p, g), fr(1, d), [fr(d - 1, d), fr(1, d - 1), fr(d, 1)],
                   "1 de %d pedaços: <b>%s</b>." % (d, fr(1, d)))
    if k == "turma":
        d = R.choice([2, 3, 4, 5])
        n = d * R.randint(5, 9)
        return mcq("Numa turma de %d alunos, %s dos alunos usa óculos. Quantos alunos usam óculos?" % (n, fr(1, d)), str(n // d), [str(n - n // d), str(d), str(n // d + 1)],
                   "%s de %d = %d ÷ %d = <b>%d</b>." % (fr(1, d), n, n, d, n // d))
    if k == "dinheiro":
        d = R.choice([2, 4, 5, 10])
        v = R.choice([20, 40, 60, 100, 200]) * 100
        if v % (d * 100):
            return None
        return mcq("%s tinha %s e gastou %s desse dinheiro num livro. Quanto custou o livro?" % (p, reais(v), fr(1, d)), reais(v // d),
                   [reais(v - v // d), reais(d * 100), reais(v // d + 100)], "%s de %s = %s ÷ %d = <b>%s</b>." % (fr(1, d), reais(v), reais(v), d, reais(v // d)))
    if k == "garrafa":
        d = R.choice([2, 4, 5, 10])
        return mcq("Uma garrafa tem 1 litro de suco (1.000 mL). %s bebeu %s da garrafa. Quantos mililitros bebeu?" % (p, fr(1, d)), "%s mL" % num(1000 // d),
                   ["%s mL" % num(x) for x in (d * 100 if d != 10 else 10, 1000 - 1000 // d, 1000 // d // 10)], "1.000 ÷ %d = <b>%s mL</b>." % (d, num(1000 // d)))
    d = R.choice([2, 4, 5, 10])
    km = d * R.randint(2, 9)
    return mcq("O caminho até a escola tem %d km. %s já andou %s do caminho. Quantos quilômetros já andou?" % (km, p, fr(1, d)), "%d km" % (km // d),
               ["%d km" % x for x in (km - km // d, d, km // d + 1)], "%d ÷ %d = <b>%d km</b>." % (km, d, km // d))


def main():
    seen = set()
    sets = [
        ("Frações unitárias nas figuras", mix(R, seen, [(s1_figura, 12), (s1_nome, 8)])),
        ("Fração de uma quantidade", mix(R, seen, [(s2_quantidade, 20)])),
        ("Comparar frações unitárias", mix(R, seen, [(s2_comparar, 10), (s3_reta, 10)])),
        ("Frações, decimais e medidas", mix(R, seen, [(s3_decimal, 8), (s4_medida, 12)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Uma <b>fração unitária</b> tem numerador 1: é uma das partes iguais de um inteiro. " + fr(1, 4) + " é uma das 4 partes.",
         "Quanto mais partes, menores elas são: " + fr(1, 2) + " &gt; " + fr(1, 3) + " &gt; " + fr(1, 4) + " &gt; " + fr(1, 5) + " &gt; " + fr(1, 10) + " &gt; " + fr(1, 100) + ".",
         "Para achar " + fr(1, 5) + " de uma quantidade, divida por 5.",
         "Na forma decimal: " + fr(1, 2) + " = 0,5; " + fr(1, 4) + " = 0,25; " + fr(1, 5) + " = 0,2; " + fr(1, 10) + " = 0,1; " + fr(1, 100) + " = 0,01."],
        [("Quanto é " + fr(1, 4) + " de 1 hora?", ["1 hora = 60 minutos", "60 ÷ 4"], "15 minutos"),
         ("Qual é maior: " + fr(1, 3) + " ou " + fr(1, 5) + "?", ["o inteiro dividido em 3 dá partes maiores"], fr(1, 3))],
        [["Achar " + fr(1, 5) + " maior que " + fr(1, 3) + " porque 5 &gt; 3", "Dividir em 5 dá pedaços menores."],
         ["Escrever " + fr(1, 4) + " como 0,4", fr(1, 4) + " = 25 centésimos = 0,25."],
         ["Para achar " + fr(1, 4) + " de 20, multiplicar 20 × 4", "Divida: 20 ÷ 4 = 5."]],
        faixa(2, 1) + faixa(4, 1) + faixa(10, 1))
    faq = [("Quais frações o 4º ano estuda?", "A BNCC pede reconhecer as frações unitárias mais usuais — 1/2, 1/3, 1/4, 1/5, 1/10 e 1/100 — na forma de fração e decimal, como partes menores que a unidade, usando a reta numérica."),
           ("Por que 1/10 é menor que 1/2?", "Porque o inteiro foi dividido em 10 partes em vez de 2. Cada uma das 10 partes é bem menor que a metade.")]
    make_unit(R, "fracoes-unitarias", "N", ["EF04MA09"],
              "Reconhecer as frações unitárias mais usuais (1/2, 1/3, 1/4, 1/5, 1/10 e 1/100) como unidades de medida menores do que uma unidade, utilizando a reta numérica como recurso",
              "Frações unitárias: metade, terço, quarto, quinto, décimo e centésimo", "Frações unitárias",
              "Atividades de matemática para o 4º ano sobre frações unitárias: 1/2, 1/3, 1/4, 1/5, 1/10 e 1/100 em figuras, na reta numérica, em decimais, fração de quantidade e medidas. 100 exercícios com gabarito.",
              "Fração unitária: 1 parte de um inteiro dividido em partes iguais.", "Mais partes, partes menores: 1/2 > 1/4 > 1/10.",
              body, faq, sets, 8, grade="4-ano")


if __name__ == "__main__":
    main()
