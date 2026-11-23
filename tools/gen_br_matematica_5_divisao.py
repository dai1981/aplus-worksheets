# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Divisão (Números, EF05MA08)
  python3 tools/gen_br_matematica_5_divisao.py
Dividir por 10, 100 e 1.000 e por dezenas exatas; divisão por 1 e por 2 algarismos (método da chave), quociente e resto;
prova real (quociente × divisor + resto); estimativa; o que fazer com o resto nos problemas.
Erros: esquecer o zero no quociente (816 ÷ 4 = 24), resto maior que o divisor, ignorar o resto num problema de ônibus.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, reais, Kids, wrap, text, line, INK, GREEN

R = random.Random(80509)
K = Kids(R)


def chave(dividendo, divisor):
    """método da chave (só a montagem, sem a resposta)"""
    a, b = num(dividendo), str(divisor)
    w = 26
    W = (len(a) + len(b) + 2) * w
    x0 = len(a) * w * 0.62 + 18
    s = [text(x0 - 6, 32, a, 22, anchor="end"),
         line(x0 + 4, 10, x0 + 4, 42, INK, 2), line(x0 + 4, 42, x0 + 14 + len(b) * 16, 42, INK, 2),
         text(x0 + 12, 32, b, 22, anchor="start")]
    return wrap(int(x0 + 30 + len(b) * 16), 56, "".join(s), "divisão de %s por %s pelo método da chave" % (a, b))


def zero_forgot(n, d):
    """quociente sem os zeros do meio (erro comum)"""
    q = str(n // d)
    z = q.replace("0", "")
    return int(z) if z and z != q else None


def s1_dez():
    m = R.choice([10, 100, 1000])
    q = R.randint(3, 999)
    n = q * m
    if n >= 1000000:
        return None
    return mcq("Calcule %s ÷ %s." % (num(n), num(m)), num(q), [num(x) for x in (q * 10, q // 10 if q >= 10 else q * 100, n // 10 if m != 10 else n // 100, q * 100, n) if x and x != q],
               "Dividir por %s é tirar %d zero%s do fim: <b>%s</b>." % (num(m), len(str(m)) - 1, "" if m == 10 else "s", num(q)))


def s1_exatas():
    d = R.randint(2, 9) * 10
    q = R.randint(2, 9) * R.choice([1, 10, 100])
    n = d * q
    return mcq("Calcule %s ÷ %d." % (num(n), d), num(q), [num(x) for x in (q * 10, q // 10 if q >= 10 else q + 10, n // (d // 10), q * 100, q + 10) if x and x != q],
               "%s ÷ %d = %s ÷ %d (tire um zero dos dois) = <b>%s</b>." % (num(n), d, num(n // 10), d // 10, num(q)))


def s2_um():
    d = R.randint(3, 9)
    q = R.randint(102, 9999)
    if "0" not in str(q) and R.random() < 0.5:
        return None
    r = R.choice([0, 0, R.randint(1, d - 1)])
    n = q * d + r
    ans = num(q) if r == 0 else "%s e resto %d" % (num(q), r)
    zf = zero_forgot(n, d)
    w = [num(zf) if zf and r == 0 else ("%s e resto %d" % (num(zf), r) if zf else None),
         num(q + 1) if r == 0 else "%s e resto %d" % (num(q + 1), r), num(q * 10) if r == 0 else "%s e resto %d" % (num(q), r + d),
         num(q - 1) if r == 0 else "%s e resto %d" % (num(q), d - r) if d - r != r else "%s e resto %d" % (num(q - 1), r)]
    return mcq(chave(n, d) + "Calcule %s ÷ %d." % (num(n), d), ans, w,
               "%s ÷ %d = %s%s. Prova real: %s × %d%s = %s." % (num(n), d, num(q), "" if r == 0 else " e resto %d" % r, num(q), d, "" if r == 0 else " + %d" % r, num(n)))


def s2_dois():
    d = R.randint(12, 48)
    q = R.randint(12, 250)
    r = R.choice([0, R.randint(1, d - 1)])
    n = q * d + r
    ans = num(q) if r == 0 else "%s e resto %d" % (num(q), r)
    w = [(num(x) if r == 0 else "%s e resto %d" % (num(x), r)) for x in (q + 1, q - 1, q * 10 if q < 100 else q // 10)]
    if r:
        w.append("%s e resto %d" % (num(q - 1), r + d))
    return mcq(chave(n, d) + "Calcule %s ÷ %d." % (num(n), d), ans, w,
               "Estime: %d × %d = %s%s. Prova real: %s × %d%s = %s. Resposta: <b>%s</b>." % (d, q, num(q * d), "" if r == 0 else "; sobram %d" % r, num(q), d, "" if r == 0 else " + %d" % r, num(n), ans))


def s3_prova():
    d = R.randint(3, 25)
    q = R.randint(20, 400)
    r = R.randint(1, d - 1)
    n = q * d + r
    k = R.choice(["dividendo", "conta", "resto"])
    if k == "dividendo":
        return mcq("Numa divisão, o divisor é %d, o quociente é %d e o resto é %d. Qual é o dividendo?" % (d, q, r), num(n), [num(x) for x in (q * d, q * d - r, q + d + r, n + d) if x != n],
                   "Dividendo = quociente × divisor + resto = %d × %d + %d = <b>%s</b>." % (q, d, r, num(n)))
    if k == "conta":
        return mcq("Qual conta confere que %s ÷ %d = %d e resto %d?" % (num(n), d, q, r), "%d × %d + %d = %s" % (q, d, r, num(n)),
                   ["%d × %d − %d = %s" % (q, d, r, num(q * d - r)), "%d + %d + %d = %s" % (q, d, r, num(q + d + r)), "%d × %d = %s" % (q, r, num(q * r))],
                   "Prova real da divisão: quociente × divisor + resto = dividendo. <b>%d × %d + %d = %s</b>." % (q, d, r, num(n)))
    rr = R.choice([r, d, d + r])
    ok = rr < d
    return mcq("%s dividiu um número por %d e achou resto %d. Isso é possível?" % (K.next()[0], d, rr),
               "Sim, o resto é menor que %d" % d if ok else "Não, o resto tem que ser menor que %d" % d,
               ["Não, o resto tem que ser menor que %d" % d if ok else "Sim, o resto é menor que %d" % d, "Sim, qualquer resto é possível", "Não, o resto tem que ser 0"],
               "O resto é sempre menor que o divisor. %d %s %d: <b>%s</b>." % (rr, "&lt;" if ok else "≥", d, "é possível" if ok else "não é possível"))


def s3_estimar():
    d = R.randint(12, 49)
    q = R.randint(20, 300)
    n = q * d + R.randint(0, d - 1)
    rd = (d + 5) // 10 * 10
    if d % 10 == 5:
        return None
    e = (n * 2 // rd + 10) // 20 * 10
    rn = e * rd
    if not e:
        return None
    opts = sorted({x for x in (e * 10, e // 10, e + 50, e * 2) if x and x != e})
    return mcq("Estime %s ÷ %d (arredonde o divisor para a dezena mais próxima)." % (num(n), d), "cerca de " + num(e), ["cerca de " + num(x) for x in opts],
               "%d ≈ %d e %s ≈ %s. %s ÷ %d = <b>%s</b> (a conta exata dá %d)." % (d, rd, num(n), num(rn), num(rn), rd, num(e), n // d))


def s4_resto():
    k = R.choice(["onibus", "caixas", "sobra", "mesas", "fitas"])
    if k == "onibus":
        n, c = R.randint(150, 600), R.choice([40, 42, 44, 45, 48])
        if n % c == 0:
            return None
        return mcq("%d pessoas vão a uma excursão. Cada ônibus leva %d pessoas. Quantos ônibus são necessários?" % (n, c), str(n // c + 1), [str(n // c), str(n % c), str(n // c + 2)],
                   "%d ÷ %d = %d e resto %d. As %d pessoas que sobram também precisam de um ônibus: <b>%d ônibus</b>." % (n, c, n // c, n % c, n % c, n // c + 1))
    if k == "caixas":
        n, c = R.randint(200, 900), R.choice([12, 15, 18, 24, 30])
        if n % c == 0:
            return None
        return mcq("Uma fábrica tem %d ovos e enche caixas de %d. Quantas caixas ficam <b>completas</b>?" % (n, c), str(n // c), [str(n // c + 1), str(n % c), str(n // c - 1)],
                   "%d ÷ %d = %d e resto %d. Só <b>%d</b> caixas ficam completas (sobram %d ovos)." % (n, c, n // c, n % c, n // c, n % c))
    if k == "sobra":
        n, c = R.randint(100, 500), R.randint(6, 15)
        if n % c == 0:
            return None
        return mcq("%d balas foram repartidas igualmente entre %d crianças, o máximo possível para cada uma. Quantas balas sobraram?" % (n, c), str(n % c), [str(n // c), str(c - n % c), str(n % c + c) if n % c + c != n // c else str(0)],
                   "%d ÷ %d = %d e resto %d: sobraram <b>%d balas</b>." % (n, c, n // c, n % c, n % c))
    if k == "mesas":
        n, c = R.randint(60, 250), R.choice([4, 6, 8])
        if n % c == 0:
            return None
        return mcq("Numa festa há %d convidados e cada mesa tem %d lugares. Quantas mesas são necessárias para todos se sentarem?" % (n, c), str(n // c + 1), [str(n // c), str(n % c), str(n * c) if n * c < 2000 else str(n // c + 2)],
                   "%d ÷ %d = %d e resto %d. Os %d que sobram precisam de mais uma mesa: <b>%d mesas</b>." % (n, c, n // c, n % c, n % c, n // c + 1))
    n, c = R.randint(500, 3000), R.choice([25, 30, 40, 50, 60])
    if n % c == 0:
        return None
    return mcq("Um rolo tem %s cm de fita. Quantos pedaços de %d cm dá para cortar?" % (num(n), c), str(n // c), [str(n // c + 1), str(n % c), num(n - c)],
               "%s ÷ %d = %d e resto %d. Dá para cortar <b>%d pedaços</b> inteiros." % (num(n), c, n // c, n % c, n // c))


def s5_problema():
    k = R.choice(["premio", "parcelas", "km", "livros", "dias", "times", "garrafas"])
    p, g = K.next()
    if k == "premio":
        n = R.randint(3, 8)
        tot = n * R.randint(120, 3000) * 100
        return mcq("Um prêmio de %s foi dividido igualmente entre %d pessoas. Quanto cada pessoa recebeu?" % (reais(tot), n), reais(tot // n),
                   [reais(x) for x in (tot // n * 10, tot // n + 100 * n, tot - n * 100, tot // (n + 1) // 100 * 100) if x != tot // n], "%s ÷ %d = <b>%s</b>." % (reais(tot), n, reais(tot // n)))
    if k == "parcelas":
        n = R.choice([10, 12, 5, 6, 8])
        par = R.randint(25, 180)
        tot = n * par * 100
        return mcq("Uma compra de %s pode ser paga em %d parcelas iguais, sem juros. Qual é o valor de cada parcela?" % (reais(tot), n), reais(tot // n),
                   [reais(x) for x in (tot // n // 10, tot // n * 2, tot // n + 1000, tot - n * 100) if x != tot // n], "%s ÷ %d = <b>%s</b>." % (reais(tot), n, reais(tot // n)))
    if k == "km":
        d = R.choice([12, 14, 15, 16, 18, 24])
        q = R.randint(20, 60)
        return mcq("Um carro rodou %s km com %d litros de gasolina. Quantos quilômetros ele rodou com cada litro?" % (num(q * d), d), "%d km" % q,
                   ["%d km" % x for x in (q + 1, q * 10, q - 2, d)], "%s ÷ %d = <b>%d km</b> por litro." % (num(q * d), d, q))
    if k == "livros":
        d = R.randint(12, 35)
        q = R.randint(15, 45)
        return mcq("Uma biblioteca tem %s livros para guardar em %d estantes, com o mesmo número em cada uma. Quantos livros vão em cada estante?" % (num(q * d), d), str(q),
                   [str(x) for x in (q + 1, q * 10, q - 1, q + d)], "%s ÷ %d = <b>%d</b>. Prova: %d × %d = %s." % (num(q * d), d, q, q, d, num(q * d)))
    if k == "dias":
        h = R.randint(100, 900)
        return mcq("Quantos dias completos há em %d horas? (1 dia = 24 horas)" % h, "%d dias" % (h // 24) if h // 24 != 1 else "1 dia",
                   ["%d dias" % x for x in (h // 24 + 1, h % 24, h // 12) if x != h // 24], "%d ÷ 24 = %d e resto %d: <b>%d dias</b> completos e %d horas." % (h, h // 24, h % 24, h // 24, h % 24))
    if k == "times":
        n, c = R.randint(5, 20) * 11, 11
        return mcq("Num campeonato há %d jogadores. Cada time de futebol tem %d jogadores. Quantos times podem ser formados?" % (n, c), str(n // c), [str(x) for x in (n // c + 1, n - c, n // 10, n // c - 1)],
                   "%d ÷ %d = <b>%d times</b>." % (n, c, n // c))
    tot, c = R.randint(20, 60) * 6, 6
    return mcq("Um mercado recebeu %d garrafas de água e vai vender em pacotes de %d. Quantos pacotes vai montar?" % (tot, c), str(tot // c), [str(x) for x in (tot // c + 1, tot - c, tot // 10, tot * c // 10)],
               "%d ÷ %d = <b>%d pacotes</b>." % (tot, c, tot // c))


def main():
    seen = set()
    sets = [
        ("Dividir por 10, 100 e 1.000", mix(R, seen, [(s1_dez, 12), (s1_exatas, 8)])),
        ("Divisão por 1 e 2 algarismos", mix(R, seen, [(s2_um, 10), (s2_dois, 10)])),
        ("Prova real e estimativa", mix(R, seen, [(s3_prova, 12), (s3_estimar, 8)])),
        ("O que fazer com o resto", mix(R, seen, [(s4_resto, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Dividir por 10, 100 ou 1.000 é tirar 1, 2 ou 3 zeros do fim: 4.700 ÷ 100 = 47.",
         "No <b>método da chave</b>, divida da esquerda para a direita. Se a ordem não dá para dividir, escreva <b>0</b> no quociente.",
         "O <b>resto</b> é sempre menor que o divisor.",
         "<b>Prova real</b>: quociente × divisor + resto = dividendo.",
         "Nos problemas, pense no resto: às vezes ele precisa de mais um ônibus; às vezes ele sobra."],
        [("Calcule 816 ÷ 4.", ["8 ÷ 4 = 2", "1 ÷ 4 não dá: escreva 0", "16 ÷ 4 = 4"], "204"),
         ("Calcule 1.000 ÷ 24.", ["24 × 40 = 960", "1.000 − 960 = 40; 24 × 1 = 24, sobram 16"], "41 e resto 16")],
        [["Esquecer o zero no quociente: 816 ÷ 4 = 24", "Quando a ordem não dá para dividir, escreva 0: 204."],
         ["Deixar um resto maior que o divisor", "Se o resto é maior, ainda cabe mais uma vez: aumente o quociente."],
         ["Ignorar o resto: 130 pessoas ÷ 40 = 3 ônibus", "As 10 pessoas que sobram precisam de mais um ônibus: 4."]],
        chave(816, 4))
    faq = [("Como ensinar a divisão por 2 algarismos?", "Use estimativas com o divisor arredondado (24 ≈ 20 ou 25) e a tabuada do divisor (24, 48, 72, 96…). Depois confira com a prova real."),
           ("O que é a prova real da divisão?", "É multiplicar o quociente pelo divisor e somar o resto. O resultado deve ser igual ao dividendo.")]
    make_unit(R, "divisao", "N", ["EF05MA08"],
              "Resolver e elaborar problemas de multiplicação e divisão com números naturais e com números racionais cuja representação decimal é finita (com multiplicador natural e divisor natural e diferente de zero), utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos",
              "Divisão: método da chave, resto e prova real", "Divisão",
              "Atividades de matemática para o 5º ano sobre divisão: por 10, 100 e 1.000, divisão por 1 e por 2 algarismos, resto, prova real, estimativa e problemas. 100 exercícios com gabarito.",
              "Prova real: quociente × divisor + resto = dividendo.", "O resto é sempre menor que o divisor.",
              body, faq, sets, 9, grade="5-ano")


if __name__ == "__main__":
    main()
