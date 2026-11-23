# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Multiplicação (Números, EF04MA06)
  python3 tools/gen_br_matematica_4_multiplicacao.py
Multiplicação com multiplicador de até 2 algarismos: adição de parcelas iguais, organização retangular, proporcionalidade
(dobro, triplo, «vezes mais»); multiplicar por 10, 100 e dezenas exatas; conta armada por 1 e por 2 algarismos; problemas.
Erros: somar em vez de multiplicar, esquecer o zero da segunda linha, achar que «3 vezes mais» é somar 3.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, reais, armada, arranjo, KINDS, COISAS, table, Kids, use, lim

R = random.Random(80405)
K = Kids(R)
L = (lim(99999, 0),)
s_dez, s_exatas, s_um, s_dois, s_prob5 = use("gen_br_matematica_5_multiplicacao", 80945, "s1_dez", "s1_exatas", "s2_um", "s2_dois", "s5_problema", preds=L)


def small_um():
    it = s_um()
    return it


def s2_ret():
    r, c = R.randint(3, 8), R.randint(4, 10)
    kind = R.choice(KINDS)
    s, p, g = COISAS[kind]
    return mcq(arranjo(r, c, kind) + "Quant%s %s há na figura? Escreva como multiplicação." % ("as" if g == "f" else "os", p), "%d × %d = %d" % (r, c, r * c),
               ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, c, r * c + c), "%d × %d = %d" % (r, c + 1, r * (c + 1))],
               "São %d linhas com %d em cada: <b>%d × %d = %d</b>." % (r, c, r, c, r * c))


def s2_ret_texto():
    k = R.choice(["cadeiras", "azulejos", "canteiro", "estacionamento", "caixa"])
    r, c = R.randint(8, 30), R.randint(12, 35)
    t = {"cadeiras": ("Um auditório tem %d fileiras com %d cadeiras cada.", "Quantas cadeiras há?"), "azulejos": ("Uma parede tem %d fileiras com %d azulejos cada.", "Quantos azulejos há?"),
         "canteiro": ("Uma horta tem %d fileiras com %d pés de alface cada.", "Quantos pés de alface há?"), "estacionamento": ("Um estacionamento tem %d fileiras com %d vagas cada.", "Quantas vagas há?"),
         "caixa": ("Numa caixa, os ovos ficam em %d fileiras de %d.", "Quantos ovos cabem?")}[k]
    if k == "caixa":
        r, c = R.randint(5, 12), R.randint(6, 12)
    return mcq((t[0] % (r, c)) + " " + t[1], num(r * c), [num(r + c), num(r * c + c), num(r * (c % 10) + r * (c // 10))],
               "Organização retangular: %d × %d = <b>%s</b>." % (r, c, num(r * c)))


def s4_vezes():
    p, g = K.next()
    q = K.next()[0]
    if p == q:
        return None
    a = R.randint(12, 99)
    m = R.choice([2, 3, 4, 5, 10, 12, 15, 20])
    obj = R.choice([("figurinhas", "f"), ("bolinhas de gude", "f"), ("selos", "m"), ("lápis de cor", "m"), ("livros", "m")])
    nome = {2: "o dobro de", 3: "o triplo de", 4: "o quádruplo de"}.get(m, "%d vezes o que" % m)
    if m in (2, 3, 4):
        q_txt = "%s tem %d %s. %s tem %s %s. Quant%s %s %s tem?" % (p, a, obj[0], q, nome, p, "as" if obj[1] == "f" else "os", obj[0], q)
    else:
        q_txt = "%s tem %d %s. %s tem %d vezes mais do que %s. Quant%s %s %s tem?" % (p, a, obj[0], q, m, p, "as" if obj[1] == "f" else "os", obj[0], q)
    return mcq(q_txt, num(a * m), [num(a + m), num(a * m + a), num(a * (m - 1)) if m > 2 else num(a * 4)],
               "%s: multiplique. %d × %d = <b>%s</b>." % ("«%s»" % nome if m in (2, 3, 4) else "«%d vezes mais»" % m, a, m, num(a * m)))


def s4_tabela():
    unit_ = R.choice([("pacotes", "figurinhas", R.choice([5, 6, 8, 12])), ("caixas", "lápis", R.choice([10, 12, 24])), ("dias", "km", R.choice([15, 25, 40])),
                      ("ingressos", "reais", R.choice([12, 15, 18, 25]))])
    a, b, per = unit_
    xs = sorted(R.sample(range(1, 13), 4))
    if xs[0] != 1 and R.random() < 0.5:
        xs[0] = 1
    xs = sorted(set(xs))
    if len(xs) < 4:
        return None
    hide = R.randrange(1, 4)
    ys = [x * per for x in xs]
    cells = [num(y) if i != hide else "?" for i, y in enumerate(ys)]
    tb = table([a.capitalize()] + [str(x) for x in xs], [[b.capitalize()] + cells])
    ans = ys[hide]
    return mcq(tb + "A tabela é de proporcionalidade. Que número fica no lugar do «?»?", num(ans),
               [num(ys[hide - 1] + (xs[hide] - xs[hide - 1])), num(ans + per), num(ans - per)],
               "Para 1 vale %s; para %d vale %d × %s = <b>%s</b>." % (num(per), xs[hide], xs[hide], num(per), num(ans)))


def s5_problema():
    k = R.choice(["onibus", "receita", "preco", "semana", "salto", "camisetas"])
    p, g = K.next()
    if k == "onibus":
        a, b = R.randint(12, 35), R.randint(38, 48)
        return mcq("Uma escola alugou %d ônibus para um passeio. Cada ônibus leva %d alunos. Quantos alunos podem ir?" % (a, b), num(a * b),
                   [num(a + b), num(a * (b % 10) + a * (b // 10)), num(a * b + b)], "%d × %d = <b>%s</b>." % (a, b, num(a * b)))
    if k == "receita":
        o = R.randint(2, 4)
        m = R.choice([2, 3, 4])
        return mcq("Uma receita de bolo usa %d ovos. Quantos ovos são necessários para %d receitas?" % (o, m), str(o * m), [str(o + m), str(o * m + o), str(o + m + 1)],
                   "%d receitas: %d × %d = <b>%d ovos</b>." % (m, m, o, o * m))
    if k == "preco":
        pr = R.randint(12, 89)
        n = R.randint(11, 25)
        return mcq("Um livro custa %s. Quanto custam %d livros iguais?" % (reais(pr * 100), n), reais(pr * n * 100),
                   [reais((pr + n) * 100), reais((pr * (n % 10) + pr * (n // 10)) * 100), reais(pr * (n - 1) * 100)], "%d × %s = <b>%s</b>." % (n, reais(pr * 100), reais(pr * n * 100)))
    if k == "semana":
        a = R.randint(25, 95)
        w = R.randint(2, 8)
        return mcq("Uma padaria vende %d pães de queijo por dia. Quantos vende em %d semanas?" % (a, w), num(a * 7 * w), [num(a * w), num(a * 7 + w), num(a * 5 * w)],
                   "%d semanas = %d × 7 = %d dias. %d × %d = <b>%s</b>." % (w, w, w * 7, a, w * 7, num(a * 7 * w)))
    if k == "salto":
        a = R.randint(3, 9)
        return mcq("Um sapo pula %d vezes mais longe que uma formiguinha. A formiguinha pulou %d cm. Quanto o sapo pulou?" % (a * 10, a), "%d cm" % (a * a * 10),
                   ["%d cm" % x for x in (a * 10 + a, a * a, a * 10)], "%d × %d = <b>%d cm</b>." % (a, a * 10, a * a * 10))
    n = R.randint(12, 60)
    c = R.randint(3, 6)
    return mcq("Uma escola comprou %d camisetas para cada uma das %d turmas. Quantas camisetas comprou?" % (n, c), num(n * c), [num(n + c), num(n * c + n), num(n * (c - 1))],
               "%d × %d = <b>%s</b>." % (c, n, num(n * c)))


def main():
    seen = set()
    sets = [
        ("Multiplicar por 10, 100 e dezenas exatas", mix(R, seen, [(s_dez, 12), (s_exatas, 8)])),
        ("Organização retangular", mix(R, seen, [(s2_ret, 10), (s2_ret_texto, 10)])),
        ("Conta armada", mix(R, seen, [(small_um, 8), (s_dois, 12)])),
        ("Dobro, triplo e proporcionalidade", mix(R, seen, [(s4_vezes, 10), (s4_tabela, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 12), (s_prob5, 8)])),
    ]
    body = lesson(
        ["Multiplicar é somar parcelas iguais: 4 × 23 = 23 + 23 + 23 + 23.",
         "Numa <b>organização retangular</b>, multiplique as linhas pelas colunas: 6 fileiras de 8 cadeiras = 6 × 8 = 48.",
         "«O triplo» ou «3 vezes mais» é multiplicar por 3.",
         "Para multiplicar por 2 algarismos, decomponha: 34 × 26 = 34 × 6 + 34 × 20."],
        [("Calcule 34 × 26.", ["34 × 6 = 204", "34 × 20 = 680", "204 + 680"], "884"),
         ("Ana tem 15 selos. Bia tem o triplo. Quantos selos Bia tem?", ["triplo = × 3", "15 × 3"], "45")],
        [["Somar em vez de multiplicar: 6 fileiras de 8 → 14", "Cada fileira tem 8: 6 × 8 = 48."],
         ["Esquecer o zero da segunda linha", "34 × 20 = 680, não 68."],
         ["Achar que «3 vezes mais» é somar 3", "«Vezes» pede multiplicação."]],
        arranjo(4, 6, "star"))
    faq = [("O que o 4º ano aprende de multiplicação?", "A BNCC pede problemas de multiplicação com multiplicador de até dois algarismos, usando adição de parcelas iguais, organização retangular e proporcionalidade, com cálculo por estimativa, cálculo mental e algoritmos."),
           ("Por que usar a organização retangular?", "Ela mostra por que 6 × 8 = 8 × 6 e prepara para a área do retângulo. As crianças veem as linhas e as colunas.")]
    make_unit(R, "multiplicacao", "N", ["EF04MA06"],
              "Resolver e elaborar problemas envolvendo diferentes significados da multiplicação (adição de parcelas iguais, organização retangular e proporcionalidade), utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos",
              "Multiplicação: organização retangular, proporcionalidade e conta armada", "Multiplicação",
              "Atividades de matemática para o 4º ano sobre multiplicação: por 10, 100 e dezenas exatas, organização retangular, dobro e triplo, proporcionalidade e conta armada com 2 algarismos. 100 exercícios com gabarito.",
              "Linhas × colunas; «vezes mais» é multiplicar.", "34 × 26 = 34 × 6 + 34 × 20",
              body, faq, sets, 5, grade="4-ano")


if __name__ == "__main__":
    main()
