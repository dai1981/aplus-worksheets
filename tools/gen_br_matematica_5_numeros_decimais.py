# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Números decimais (Números, EF05MA02)
  python3 tools/gen_br_matematica_5_numeros_decimais.py
Décimos, centésimos e milésimos; fração decimal e número decimal; quadro de valor posicional;
leitura por extenso; decimais na reta numérica, no dinheiro e nas medidas; problemas.
Erros: 0,5 = 5/100, 3/100 = 0,3, ler 2,35 como «dois vírgula trinta e cinco» sem saber o valor, 0,40 ≠ 0,4.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, dz, fr, quadro_decimal, extenso, reta, reais, wrap, text, line, INK, GREEN, Kids

R = random.Random(80502)
K = Kids(R)
NOME = {1: ("décimo", "décimos"), 2: ("centésimo", "centésimos"), 3: ("milésimo", "milésimos")}


def ler(n, k):
    """2,35 → dois inteiros e trinta e cinco centésimos"""
    ip, fp_ = divmod(n, 10 ** k)
    while k > 1 and fp_ % 10 == 0 and fp_:
        fp_ //= 10
        k -= 1
    parts = []
    if ip:
        parts.append("um inteiro" if ip == 1 else extenso(ip) + " inteiros")
    if fp_:
        s, p = NOME[k]
        w = extenso(fp_)
        if fp_ == 1:
            w = "um"
        parts.append(w + " " + (s if fp_ == 1 else p))
    return " e ".join(parts)


def grade100(k):
    """quadrado dividido em 100 partes, k pintadas"""
    c, s = 16, []
    for i in range(100):
        x, y = 6 + (i % 10) * c, 6 + (i // 10) * c
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='0.8'/>" % (x, y, c, c, "#7cc68f" if i < k else "#fff", INK))
    s.append("<rect x='6' y='6' width='160' height='160' fill='none' stroke='%s' stroke-width='2'/>" % INK)
    return wrap(172, 172, "".join(s), "quadrado dividido em 100 partes iguais, %d %s" % (k, "pintada" if k == 1 else "pintadas"))


def tira10(k, n=1):
    """n tiras divididas em 10, k décimos pintados ao todo"""
    c, s = 30, []
    for t in range(n):
        for i in range(10):
            x, y = 6 + i * c, 6 + t * 40
            s.append("<rect x='%d' y='%d' width='%d' height='30' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x, y, c, "#7cc68f" if t * 10 + i < k else "#fff", INK))
    return wrap(312, 6 + 40 * n, "".join(s), ("1 tira dividida" if n == 1 else "%d tiras divididas" % n) + " em 10 partes iguais, %d %s" % (k, "parte pintada" if k == 1 else "partes pintadas"))


def wd(n, k):
    """distratores para dz(n, k)"""
    out = [dz(n, k + 1), dz(n, k - 1) if k > 1 else None, dz(n * 10, k),
           dz(n + 1, k), dz(n - 1, k) if n > 1 else None, dz(n + 10 ** (k - 1), k)]
    return [x for x in out if x and x != dz(n, k)]


def s1_figura():
    k = R.choice(["g", "g", "t", "t2"])
    if k == "g":
        a = R.randint(3, 97)
        if a % 10 == 0:
            return None
        return mcq(grade100(a) + "O quadrado inteiro vale 1. Que número decimal representa a parte pintada?", dz(a, 2), [dz(a, 1) if a < 100 else None, dz(a, 3), dz(100 - a, 2), str(a)],
                   "%d das 100 partes: %s = <b>%s</b>." % (a, fr(a, 100), dz(a, 2)))
    if k == "t":
        a = R.randint(1, 9)
        return mcq(tira10(a) + "A tira inteira vale 1. Que número decimal representa a parte pintada?", dz(a, 1), [dz(a, 2), str(a), dz(10 - a, 1), "1," + str(a)],
                   "%d das 10 partes: %s = <b>%s</b>." % (a, fr(a, 10), dz(a, 1)))
    a = R.randint(11, 19)
    return mcq(tira10(a, 2) + "Cada tira inteira vale 1. Que número decimal representa a parte pintada?", dz(a, 1), [dz(a, 2), str(a), "0,%d" % a, dz(a - 10, 1)],
               "1 tira inteira e %d décimos: <b>%s</b>." % (a - 10, dz(a, 1)))


def s1_quantos():
    k = R.choice([1, 2, 3])
    n = R.randint(2, 9)
    big = {1: "1 inteiro", 2: "1 décimo", 3: "1 centésimo"}[k]
    small = {1: "décimos", 2: "centésimos", 3: "milésimos"}[k]
    if R.random() < 0.5:
        return mcq("Quantos %s formam %s?" % (small, big), "10", ["100", "1.000", "5"], "Cada ordem vale 10 vezes a ordem à sua direita: <b>10</b> %s." % small)
    t = {1: "inteiro", 2: "décimos", 3: "centésimos"}[k]
    return mcq("%d %s formam quantos %s?" % (n * 10, small, "inteiros" if k == 1 else t), str(n), [str(n * 10), str(n * 100), dz(n, 1)],
               "10 %s formam 1 %s: %d ÷ 10 = <b>%d</b>." % (small, "inteiro" if k == 1 else t[:-1], n * 10, n))


def s2_frac_para_dec():
    k = R.choice([1, 2, 2, 3])
    a = R.randint(1, 10 ** k - 1)
    if a % 10 == 0:
        return None
    if R.random() < 0.6:
        return mcq("Escreva %s como número decimal." % fr(a, 10 ** k), dz(a, k), wd(a, k),
                   "O denominador %s tem %d zero%s: %s casa%s depois da vírgula. %s = <b>%s</b>." % (num(10 ** k), k, "" if k == 1 else "s", k, "" if k == 1 else "s", fr(a, 10 ** k), dz(a, k)))
    alts = [fr(a, 10 ** (k + 1)) if k < 3 else fr(a, 10), fr(a, 10 ** (k - 1)) if k > 1 else fr(a, 100), fr(a * 10, 10 ** k) if a * 10 < 10 ** k else fr(10 ** k - a, 10 ** k), fr(a, 10 ** k).replace("fn'>%d" % a, "fn'>%d" % (a + 1))]
    return mcq("Qual fração decimal é igual a %s?" % dz(a, k), fr(a, 10 ** k), alts,
               "%s tem %d casa%s depois da vírgula: denominador %s. <b>%s = %s</b>." % (dz(a, k), k, "" if k == 1 else "s", num(10 ** k), dz(a, k), fr(a, 10 ** k)))


def s2_misto():
    ip = R.randint(1, 9)
    k = R.choice([1, 2])
    f = R.randint(1, 10 ** k - 1)
    if f % 10 == 0:
        return None
    n = ip * 10 ** k + f
    return mcq("Escreva com um número decimal: %d inteiros e %s." % (ip, ler(f, k)), dz(n, k),
               [dz(ip * 10 ** (k + 1) + f, k + 1) if k == 1 else dz(ip * 10 + f // 10, 1), "%d,%d" % (f, ip), dz(n, k + 1), dz(ip * 10 ** (3 - k) + f, 3) if k < 3 else None],
               "Inteiros antes da vírgula, %s depois: <b>%s</b>." % (NOME[k][1], dz(n, k)))


def s3_ordem():
    ip = R.randint(1, 99)
    fp_ = R.randint(101, 999)
    n = ip * 1000 + fp_
    d = [int(x) for x in str(fp_)]
    if len(set(d)) < 3:
        return None
    i = R.randrange(3)
    nome = ["décimos", "centésimos", "milésimos"][i]
    if R.random() < 0.6:
        return mcq(quadro_decimal(n, 3, 2 if ip >= 10 else 1) + "Qual é o algarismo dos %s em %s?" % (nome, dz(n, 3)), str(d[i]), [str(x) for x in d if x != d[i]] + [str(ip % 10), str((d[i] + 1) % 10)],
                   "Depois da vírgula vêm décimos, centésimos e milésimos. O algarismo dos %s é <b>%d</b>." % (nome, d[i]))
    if d[i] == 0:
        return None
    v = d[i] * 10 ** (2 - i)
    return mcq("Quanto vale o algarismo %d em %s?" % (d[i], dz(n, 3)), dz(v, 3), [dz(v * 10, 3) if i else str(d[i]), dz(v, 4) if i == 2 else dz(v // 10, 3), str(d[i])] + [dz(d[i], 0)],
               "O %d está na ordem dos %s: vale <b>%s</b> (%s)." % (d[i], nome, dz(v, 3), fr(d[i], 10 ** (i + 1))))


def s3_ler():
    k = R.choice([1, 2, 2, 3])
    ip = R.choice([0, R.randint(1, 30)])
    f = R.randint(1, 10 ** k - 1)
    if f % 10 == 0:
        return None
    n = ip * 10 ** k + f
    if R.random() < 0.5:
        w = [ler(n, k + 1) if k < 3 else ler(n * 10, 3).replace("milésimos", "centésimos"), ler(n, k - 1) if k > 1 else ler(n, 2), ler(ip * 10 ** k + (10 ** k - f), k) if 10 ** k - f != f else None, ler(f * 10 ** k + max(ip, 1), k)]
        return mcq("Como se lê %s?" % dz(n, k), ler(n, k), w, "%s: <b>%s</b>." % (dz(n, k), ler(n, k)))
    return mcq("Escreva com algarismos: <b>%s</b>." % ler(n, k), dz(n, k), wd(n, k), "«%s» = <b>%s</b>." % (ler(n, k), dz(n, k)))


def s4_reta():
    k = R.choice(["dec", "cent"])
    if k == "dec":
        a = R.randint(0, 4)
        p = R.randint(1, 9)
        marks = [(a * 10 + p, "A")]
        svg = reta(a * 10, a * 10 + 10, 1, [(a * 10 + p, "A")], labels=[a * 10, a * 10 + 10])
        svg = svg.replace(">%d<" % (a * 10 + 10), ">%d<" % (a + 1)).replace(">%d<" % (a * 10), ">%d<" % a, 1) if a else svg.replace(">10<", ">1<")
        return mcq(svg + "A reta vai de %d a %d, dividida em décimos. Que número a letra A marca?" % (a, a + 1), dz(a * 10 + p, 1),
                   [dz(a * 100 + p, 2), "%d,%d" % (a, 10 - p), str(a * 10 + p), "%d,%d" % (a + 1, p)],
                   "Cada risquinho vale 0,1. A está %d risquinhos depois de %d: <b>%s</b>." % (p, a, dz(a * 10 + p, 1)))
    a = R.randint(1, 9)
    b = R.randint(1, 9)
    lo = a * 10
    return mcq("Que número está exatamente no meio de %s e %s?" % (dz(lo, 2), dz(lo + 10, 2)), dz(lo * 10 + 50, 3),
               [dz(lo + 5, 1), dz(lo + 1, 2), dz(lo + 15, 2)],
               "Entre %s e %s há 10 milésimos; o meio está 5 milésimos depois: <b>%s</b>." % (dz(lo, 2), dz(lo + 10, 2), dz(lo * 10 + 50, 3)))


def s4_medidas():
    k = R.choice(["m", "reais", "kg", "zero"])
    if k == "m":
        m, c = R.randint(1, 3), R.randint(1, 99)
        if c % 10 == 0:
            return None
        n = m * 100 + c
        return mcq("%d m e %d cm escritos em metros são…" % (m, c), dz(n, 2) + " m", ["%d,%d m" % (m, c), "%d,%d m" % (c, m), "%d m" % n, dz(m * 1000 + c, 3) + " m"],
                   "1 cm = 0,01 m. %d m e %d cm = <b>%s m</b>." % (m, c, dz(n, 2)))
    if k == "reais":
        r, c = R.randint(1, 30), R.choice([5, 10, 25, 50, 75, 5, 95])
        return mcq("Como se escreve %d reais e %d centavos?" % (r, c), reais(r * 100 + c), [reais(r * 100 + c * 10) if c < 10 else "R$ %d,%d" % (r, c // 10), "R$ %d,%d" % (c, r), reais(r * 1000 + c)],
                   "Os centavos ocupam 2 casas depois da vírgula: <b>%s</b>." % reais(r * 100 + c))
    if k == "kg":
        kg, g = R.randint(1, 5), R.choice([5, 50, 250, 500, 750, 125, 75])
        n = kg * 1000 + g
        L = len(str(g))
        ws = [(kg * 10 ** L + g) * 10 ** (3 - L), kg * 1000 + g // 10, kg * 1000 + g * 10 if g < 100 else None]
        return mcq("%d kg e %d g escritos em quilogramas são…" % (kg, g), dz(n, 3) + " kg", [dz(x, 3) + " kg" for x in ws if x and x != n] + ["%d,%d kg" % (g, kg), num(n) + " kg"],
                   "1 g = 0,001 kg. %d kg e %d g = <b>%s kg</b>." % (kg, g, dz(n, 3)))
    a = R.randint(1, 9)
    return mcq("Qual número é igual a %s?" % dz(a * 10, 2, True), dz(a, 1), ["0,0%d" % a, "%d,0" % (a * 10), dz(a, 3)],
               "Um zero no fim da parte decimal não muda o valor: %s = <b>%s</b> (%d centésimos = %d décimos)." % (dz(a * 10, 2, True), dz(a, 1), a * 10, a))


def s5_problema():
    k = R.choice(["corrida", "chuva", "agua", "dinheiro", "pao", "altura"])
    p = K.next()[0]
    if k == "corrida":
        a = R.randint(11, 98)
        if a % 10 == 0:
            return None
        return mcq("Uma pista foi dividida em 100 partes iguais. %s já correu %d partes. Que número decimal mostra a parte que já foi corrida?" % (p, a), dz(a, 2),
                   [dz(a, 1), dz(a, 3), dz(100 - a, 2)], "%d de 100 partes: %s = <b>%s</b>." % (a, fr(a, 100), dz(a, 2)))
    if k == "chuva":
        a = R.randint(11, 99)
        if a % 10 == 0:
            return None
        return mcq("Choveu %s mm num dia. Quantos décimos de milímetro são?" % dz(a, 1), str(a), [str(a // 10), dz(a, 1), str(a * 10)],
                   "Cada milímetro tem 10 décimos: %s mm = <b>%d</b> décimos." % (dz(a, 1), a))
    if k == "agua":
        a = R.choice([125, 250, 375, 500, 750, 350, 600])
        return mcq("Uma garrafa tem %d mL de água. Quanto é isso em litros?" % a, dz(a, 3) + " L", [dz(a, 2) + " L", dz(a, 1) + " L", "%d L" % a],
                   "1 mL = 0,001 L: %d mL = <b>%s L</b>." % (a, dz(a, 3)))
    if k == "dinheiro":
        n = R.randint(3, 9)
        return mcq("%s juntou %d moedas de 10 centavos. Quantos reais são?" % (p, n),
                   reais(n * 10), [reais(n), reais(n * 100), reais(n * 100 + 10)], "10 centavos = R$ 0,10. %d × R$ 0,10 = <b>%s</b>." % (n, reais(n * 10)))
    if k == "pao":
        d = R.randint(2, 9)
        return mcq("Uma pizza foi cortada em 10 pedaços iguais. %s comeu %d pedaços. Que número decimal mostra a parte que sobrou?" % (p, d), dz(10 - d, 1),
                   [dz(d, 1), dz(10 - d, 2), str(10 - d)], "Sobraram %d de 10 pedaços: <b>%s</b>." % (10 - d, dz(10 - d, 1)))
    a, b = R.randint(120, 165), R.randint(120, 165)
    if a == b:
        return None
    q = K.next()[0]
    if q == p:
        return None
    big = p if a > b else q
    return mcq("%s mede %s m e %s mede %s m. Quem é mais alto ou mais alta?" % (p, dz(a, 2), q, dz(b, 2)), big, [q if big == p else p, "os dois têm a mesma altura", "não dá para saber"],
               "Compare os décimos e depois os centésimos: %s m %s %s m. <b>%s</b>." % (dz(max(a, b), 2), "&gt;", dz(min(a, b), 2), big))


def main():
    seen = set()
    sets = [
        ("Décimos e centésimos", mix(R, seen, [(s1_figura, 14), (s1_quantos, 6)])),
        ("Frações decimais", mix(R, seen, [(s2_frac_para_dec, 14), (s2_misto, 6)])),
        ("Valor posicional e leitura", mix(R, seen, [(s3_ordem, 10), (s3_ler, 10)])),
        ("Reta numérica e medidas", mix(R, seen, [(s4_reta, 8), (s4_medidas, 12)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Dividindo 1 inteiro em 10 partes iguais, cada parte é <b>1 décimo</b> = 0,1. Em 100 partes, cada parte é <b>1 centésimo</b> = 0,01. Em 1.000 partes, <b>1 milésimo</b> = 0,001.",
         "Depois da vírgula vêm, nessa ordem: décimos, centésimos, milésimos.",
         "O número de casas depois da vírgula é o número de zeros do denominador: " + fr(7, 10) + " = 0,7; " + fr(7, 100) + " = 0,07; " + fr(7, 1000) + " = 0,007.",
         "Zeros no fim da parte decimal não mudam o valor: 0,4 = 0,40 = 0,400."],
        [("Escreva 2 inteiros e 35 centésimos.", ["2 antes da vírgula", "35 centésimos ocupam 2 casas: 35"], "2,35"),
         ("Escreva " + fr(8, 100) + " como número decimal.", ["denominador 100 → 2 casas", "8 centésimos → 0,08"], "0,08")],
        [["Escrever " + fr(3, 100) + " como 0,3", "100 tem 2 zeros: são 2 casas. " + fr(3, 100) + " = 0,03."],
         ["Pensar que 0,40 é maior que 0,4", "0,40 = 40 centésimos = 4 décimos = 0,4."],
         ["Ler 2,35 como «dois vírgula trinta e cinco» sem pensar no valor", "Leia «dois inteiros e trinta e cinco centésimos»."]],
        quadro_decimal(2350, 3))
    faq = [("O que o 5º ano aprende sobre números decimais?", "A BNCC pede ler, escrever e ordenar números decimais até os milésimos, ligando a escrita decimal às frações decimais, ao dinheiro e às medidas."),
           ("Por que usar dinheiro para ensinar decimais?", "R$ 3,25 mostra bem os décimos (moedas de 10 centavos) e os centésimos (centavos). É um exemplo que as crianças conhecem.")]
    make_unit(R, "numeros-decimais", "N", ["EF05MA02"],
              "Ler, escrever e ordenar números racionais na forma decimal com compreensão das principais características do sistema de numeração decimal, utilizando, como recursos, a composição e decomposição e a reta numérica",
              "Números decimais: décimos, centésimos e milésimos", "Números decimais",
              "Atividades de matemática para o 5º ano sobre números decimais: décimos, centésimos e milésimos, frações decimais, quadro de valor posicional, leitura e reta numérica. 100 exercícios com gabarito.",
              "Depois da vírgula: décimos, centésimos, milésimos.", "1 = 10 décimos = 100 centésimos = 1.000 milésimos.",
              body, faq, sets, 2, grade="5-ano")


if __name__ == "__main__":
    main()
