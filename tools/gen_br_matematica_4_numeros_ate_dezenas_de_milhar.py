# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Números até dezenas de milhar (Números, EF04MA01, EF04MA02)
  python3 tools/gen_br_matematica_4_numeros_ate_dezenas_de_milhar.py
Classes e ordens (DM UM C D U); ler e escrever por extenso; compor e decompor; valor posicional;
comparar e ordenar; antecessor e sucessor; arredondar para a dezena de milhar e o milhar mais próximo; problemas.
Erros: esquecer o zero numa ordem vazia, confundir algarismo e valor, comparar pelo primeiro algarismo sem olhar o número de ordens.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, quadro_valor, extenso, pl

R = random.Random(80401)
ORD = [("dezenas de milhar", 10000), ("unidades de milhar", 1000), ("centenas", 100), ("dezenas", 10), ("unidades", 1)]
ORD1 = {"centenas de milhar": "centena de milhar", "dezenas de milhar": "dezena de milhar", "unidades de milhar": "unidade de milhar",
        "centenas": "centena", "dezenas": "dezena", "unidades": "unidade"}


def six(lo=10000):
    return R.randint(lo, 99999)


def digs(n):
    return [int(c) for c in str(n).rjust(5, "0")]


def wrong(n):
    d = digs(n)
    out = []
    z = int("".join(str(x) for x in d if x) or "0")
    if z != n:
        out.append(z)
    for i in range(4):
        if d[i] != d[i + 1]:
            e = d[:]
            e[i], e[i + 1] = e[i + 1], e[i]
            out.append(int("".join(map(str, e))))
    out += [n + 10000 if n < 90000 else n - 10000, n + 1000, n - 100, n * 10 if n < 10000 else None, n // 10]
    return [num(x) for x in out if x and 1000 <= x < 100000 and x != n]


def s1_quadro():
    n = six(10000)
    if R.random() < 0.5:
        d = digs(n)
        d[R.randint(2, 4)] = 0
        n = int("".join(map(str, d)))
    cols = 5 if n >= 10000 else 4
    return mcq(quadro_valor(n, cols) + "Que número está no quadro de valor posicional?", num(n), wrong(n),
               "Leia as ordens da esquerda para a direita e separe as classes com ponto: <b>%s</b>." % num(n))


def s1_partes():
    d = [R.randint(1, 9)] + [R.choice([0, R.randint(1, 9)]) for _ in range(4)]
    n = int("".join(map(str, d)))
    words = [pl(v, ORD1[nome], nome) for v, (nome, _) in zip(d, ORD) if v]
    if len(words) < 3:
        return None
    return mcq("Que número tem " + ", ".join(words[:-1]) + " e " + words[-1] + "?", num(n), wrong(n),
               "Coloque cada quantidade na sua ordem e escreva 0 nas ordens vazias: <b>%s</b>." % num(n))


def s1_algarismo():
    n = six()
    d = digs(n)
    if len(set(d)) < 4:
        return None
    i = R.randrange(5)
    nome, v = ORD[i]
    if R.random() < 0.5:
        return mcq("Em %s, qual é o algarismo das %s?" % (num(n), nome), str(d[i]), [str(x) for x in d if x != d[i]],
                   "Contando da direita: unidades, dezenas, centenas, unidades de milhar, dezenas de milhar. O algarismo das %s é <b>%d</b>." % (nome, d[i]))
    if d[i] == 0 or i == 4:
        return None
    w = [str(d[i]), num(d[i] * v // 10), num(d[i] * v * 10) if v < 10000 else num(d[i] * v // 100), num(d[i] * v * 100) if v < 1000 else num(d[i] * v // 100)]
    return mcq("Em %s, quanto vale o algarismo %d?" % (num(n), d[i]), num(d[i] * v), w,
               "O %d está na ordem das %s: vale %d × %s = <b>%s</b>." % (d[i], nome, d[i], num(v), num(d[i] * v)))


def s2_do_extenso():
    n = six(10000)
    if R.random() < 0.5:
        d = digs(n)
        for k in R.sample(range(1, 5), 2):
            d[k] = 0
        n = int("".join(map(str, d)))
    if n < 10000:
        return None
    return mcq("Escreva com algarismos: <b>%s</b>." % extenso(n), num(n), wrong(n), "«%s» se escreve <b>%s</b>." % (extenso(n), num(n)))


def s2_por_extenso():
    n = six(10000)
    d = digs(n)
    w = [n + 1000 if d[1] < 9 else n - 1000, n + 100 if d[2] < 9 else n - 100, n // 1000 * 1000 + (n % 1000) // 10, (n % 1000) * 1000 + n // 1000]
    return mcq("Como se escreve %s por extenso?" % num(n), extenso(n), [extenso(x) for x in w if 0 < x < 100000 and x != n],
               "%s = %s mil e %s: <b>%s</b>." % (num(n), num(n // 1000), num(n % 1000), extenso(n)))


def s3_decompor():
    n = six()
    d = digs(n)
    if d.count(0) > 2:
        return None
    terms = [x * w for x, (_, w) in zip(d, ORD) if x]
    sh = " + ".join(num(t) for t in terms)
    if R.random() < 0.5:
        return mcq("Que número é igual a %s?" % sh, num(n), wrong(n), "%s = <b>%s</b>." % (sh, num(n)))
    t2 = [x * w for x, (_, w) in zip(d, ORD)]
    w1 = " + ".join(num(t // 10 if i == 1 else t) for i, t in enumerate(t2) if t)
    w2 = " + ".join(num(t * 10 if i == 3 else t) for i, t in enumerate(t2) if t)
    w3 = " + ".join(num(x) for x in d if x)
    w4 = " + ".join(num(t * 10 if i == 4 else t) for i, t in enumerate(t2) if t)
    w5 = " + ".join(num(t * 10 if i == 2 else t) for i, t in enumerate(t2) if t)
    return mcq("Qual é a decomposição de %s?" % num(n), sh, [w1, w2, w3, w4, w5], "Cada algarismo vale conforme a sua ordem: <b>%s</b>." % sh)


def s3_compor():
    a, b, c = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
    k = R.choice(["mil", "dm", "cm"])
    if k == "mil":
        m = R.randint(12, 99)
        return mcq("%s mil, %s e %s formam que número?" % (num(m), pl(a, "centena", "centenas"), pl(b, "unidade", "unidades")), num(m * 1000 + a * 100 + b),
                   [num(m * 1000 + a * 10 + b), num(m * 100 + a * 10 + b), num(m * 1000 + a * 100 + b * 10)],
                   "%s + %s + %d = <b>%s</b>." % (num(m * 1000), num(a * 100), b, num(m * 1000 + a * 100 + b)))
    if k == "dm":
        n = a * 10000 + b * 1000 + c * 10
        return mcq("%s, %s e %s formam que número?" % (pl(a, "dezena de milhar", "dezenas de milhar"), pl(b, "unidade de milhar", "unidades de milhar"), pl(c, "dezena", "dezenas")),
                   num(n), [num(a * 10000 + b * 1000 + c * 100), num(a * 1000 + b * 100 + c * 10), num(a * 10000 + b * 1000 + c)],
                   "%s + %s + %d = <b>%s</b>." % (num(a * 10000), num(b * 1000), c * 10, num(n)))
    n = a * 10000 + b * 100 + c
    return mcq("%s, %s e %s formam que número?" % (pl(a, "dezena de milhar", "dezenas de milhar"), pl(b, "centena", "centenas"), pl(c, "unidade", "unidades")),
               num(n), [num(a * 1000 + b * 100 + c), num(a * 10000 + b * 1000 + c), num(a * 10000 + b * 10 + c)],
               "%s + %d + %d = <b>%s</b>. As ordens vazias levam 0." % (num(a * 10000), b * 100, c, num(n)))


def s4_comparar():
    k = R.choice(["maior", "menor", "crescente", "decrescente"])
    base = six(12000)
    ns = {base}
    while len(ns) < 4:
        d = digs(base)
        i = R.choice([1, 2, 3])
        d[i] = R.randint(0, 9)
        x = int("".join(map(str, d)))
        if R.random() < 0.3:
            x = x // 10
        ns.add(x)
    ns = sorted(ns)
    if len(set(len(str(x)) for x in ns)) == 1 and R.random() < 0.3:
        return None
    sh = ns[:]
    R.shuffle(sh)
    lst = "; ".join(num(x) for x in sh)
    if k in ("maior", "menor"):
        ans = ns[-1] if k == "maior" else ns[0]
        return mcq("Qual é o %s número? %s" % (k, lst), num(ans), [num(x) for x in ns if x != ans],
                   "Primeiro conte as ordens; com o mesmo número de ordens, compare da esquerda para a direita. O %s é <b>%s</b>." % (k, num(ans)))
    o = ns if k == "crescente" else ns[::-1]
    good = " &lt; ".join(num(x) for x in o) if k == "crescente" else " &gt; ".join(num(x) for x in o)
    sep = " &lt; " if k == "crescente" else " &gt; "
    w = [o[1], o[0], o[2], o[3]], [o[0], o[2], o[1], o[3]], [o[3], o[2], o[1], o[0]]
    return mcq("Qual é a ordem %s de %s?" % (k, lst), good, [sep.join(num(x) for x in v) for v in w],
               "Compare as dezenas de milhar, depois as unidades de milhar e assim por diante: <b>%s</b>." % good)


def s4_vizinhos():
    k = R.choice(["ant", "suc", "dm", "mil"])
    if k in ("ant", "suc"):
        n = R.choice([R.randint(10, 99) * 1000, R.randint(100, 999) * 100, R.randint(1000, 9999) * 10])
        if k == "ant":
            return mcq("Qual é o antecessor de %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 1000 + 1), num(n - 100)],
                       "O antecessor vem logo antes: %s − 1 = <b>%s</b>." % (num(n), num(n - 1)))
        n -= 1
        return mcq("Qual é o sucessor de %s?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 1000) if n < 90000 else num(n + 2), num(n + 100)],
                   "O sucessor vem logo depois: %s + 1 = <b>%s</b>." % (num(n), num(n + 1)))
    n = six()
    if k == "dm":
        r = (n + 5000) // 10000 * 10000
        if r >= 100000:
            return None
        if n % 10000 == 5000 or r == n:
            return None
        return mcq("Arredonde %s para a dezena de milhar mais próxima." % num(n), num(r), [num(n // 10000 * 10000 if r != n // 10000 * 10000 else r + 10000), num((n + 500) // 1000 * 1000), num(r + 10000) if r < 100000 else None, num(r - 10000) if r > 10000 else None, num((n + 50) // 100 * 100)],
                   "Olhe o algarismo das unidades de milhar (%d): %s, então fica <b>%s</b>." % (n // 1000 % 10, "5 ou mais, arredonde para cima" if n // 1000 % 10 >= 5 else "menos de 5, arredonde para baixo", num(r)))
    r = (n + 500) // 1000 * 1000
    if n % 1000 == 500 or r == n:
        return None
    return mcq("Arredonde %s para o milhar mais próximo." % num(n), num(r), [num(n // 1000 * 1000 if r != n // 1000 * 1000 else r + 1000), num((n + 50) // 100 * 100), num((n + 5000) // 10000 * 10000), num(r + 1000), num(r - 1000)],
               "Olhe o algarismo das centenas (%d): %s, então fica <b>%s</b>." % (n // 100 % 10, "5 ou mais, arredonde para cima" if n // 100 % 10 >= 5 else "menos de 5, arredonde para baixo", num(r)))


CID = ["Petrópolis", "Juazeiro", "Marabá", "Caruaru", "Anápolis", "Bauru", "Chapecó", "Itajaí", "Santarém", "Mossoró", "Dourados", "Parnaíba"]


def s5_problema():
    k = R.choice(["pop", "estadio", "cofre", "km", "pistas"])
    if k == "pop":
        a, b = R.sample(CID, 2)
        x, y = R.randint(12, 98) * 1000 + R.randint(0, 999), R.randint(12, 98) * 1000 + R.randint(0, 999)
        if abs(x - y) < 1000:
            return None
        big = a if x > y else b
        return mcq("%s tem %s habitantes e %s tem %s habitantes. Qual cidade tem mais habitantes?" % (a, num(x), b, num(y)), big,
                   [b if big == a else a, "as duas têm o mesmo número", "não dá para saber"],
                   "Compare as dezenas de milhar e depois as unidades de milhar: <b>%s</b> tem mais." % big)
    if k == "estadio":
        n = R.randint(40, 78) * 1000 + R.randint(1, 999)
        return mcq("Um estádio recebeu %s torcedores. Qual é esse número arredondado para o milhar mais próximo?" % num(n),
                   num((n + 500) // 1000 * 1000), [num(n // 1000 * 1000 if (n + 500) // 1000 * 1000 != n // 1000 * 1000 else n // 1000 * 1000 + 1000), num((n + 5000) // 10000 * 10000), num((n + 50) // 100 * 100), num((n + 500) // 1000 * 1000 + 1000), num((n + 500) // 1000 * 1000 - 1000), num(n // 100 * 100)],
                   "O algarismo das centenas é %d: <b>%s</b>." % (n // 100 % 10, num((n + 500) // 1000 * 1000)))
    if k == "cofre":
        a, b, c = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
        tot = a * 10000 + b * 1000 + c * 100
        return mcq("Um banco tem %s pacotes de R$ 10.000, %s pacotes de R$ 1.000 e %s cédulas de R$ 100. Quantos reais há ao todo?" % (a, b, c),
                   "R$ " + num(tot), ["R$ " + num(a * 1000 + b * 100 + c * 10), "R$ " + num(a * 10000 + b * 100 + c * 1000), "R$ " + num(a + b + c)],
                   "%s + %s + %s = <b>R$ %s</b>." % (num(a * 10000), num(b * 1000), num(c * 100), num(tot)))
    if k == "km":
        n = R.randint(10, 89) * 1000
        return mcq("Um carro já rodou %s km. Depois de rodar mais 10.000 km, quanto marcará?" % num(n), num(n + 10000) + " km",
                   [num(n + 1000) + " km", num(n + 100) + " km", num(n + 10) + " km"],
                   "Somar 10.000 muda o algarismo das dezenas de milhar: <b>%s km</b>." % num(n + 10000))
    d = [R.randint(1, 9)] + [R.randint(0, 9) for _ in range(4)]
    if len(set(d)) < 5:
        return None
    n = int("".join(map(str, d)))
    pistas = ["o algarismo das %s é %d" % (nome, v) for v, (nome, _) in zip(d, ORD)]
    R.shuffle(pistas)
    return mcq("Adivinha: tenho 5 algarismos; %s. Quem sou eu?" % "; ".join(pistas), num(n), wrong(n),
               "Coloque cada algarismo na sua ordem: <b>%s</b>." % num(n))


def main():
    seen = set()
    sets = [
        ("Classes e ordens", mix(R, seen, [(s1_quadro, 8), (s1_partes, 6), (s1_algarismo, 6)])),
        ("Ler e escrever números", mix(R, seen, [(s2_do_extenso, 10), (s2_por_extenso, 10)])),
        ("Compor e decompor", mix(R, seen, [(s3_decompor, 10), (s3_compor, 10)])),
        ("Comparar, ordenar e arredondar", mix(R, seen, [(s4_comparar, 10), (s4_vizinhos, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Os números são lidos em <b>classes</b> de 3 ordens: a classe dos milhares (DM, UM) e a classe das unidades simples (C, D, U).",
         "Cada ordem vale <b>10 vezes</b> a ordem da sua direita: 10 unidades de milhar = 1 dezena de milhar = 10.000.",
         "Para ler 45.208, leia a classe dos milhares e diga «mil», depois a outra classe: quarenta e cinco mil duzentos e oito.",
         "Um número pode ser decomposto em adições e multiplicações por 10, 100 e 1.000: 45.208 = 4 × 10.000 + 5 × 1.000 + 2 × 100 + 8."],
        [("Escreva com algarismos: trinta mil e sessenta.", ["classe dos milhares: 30", "classe das unidades: 060"], "30.060"),
         ("Quanto vale o 7 em 57.218?", ["o 7 está nas unidades de milhar", "7 × 1.000"], "7.000")],
        [["Esquecer o zero: 30 mil e 60 → 3.060", "Cada classe tem 3 ordens: 30.060."],
         ["Confundir algarismo e valor", "O algarismo é 7; o valor do 7 em 57.218 é 7.000."],
         ["Comparar só o primeiro algarismo: 9.800 &gt; 12.000", "Primeiro veja quantas ordens tem cada número: 12.000 tem 5."]],
        quadro_valor(57218, 5))
    faq = [("Até que número se trabalha no 4º ano?", "A BNCC indica números naturais até a ordem das dezenas de milhar, ou seja, até 99.999: ler, escrever, ordenar e decompor."),
           ("O que é decompor um número?", "É escrever o número como soma das partes de cada ordem, por exemplo 45.208 = 40.000 + 5.000 + 200 + 8, ou com multiplicações por 10, 100 e 1.000.")]
    make_unit(R, "numeros-ate-dezenas-de-milhar", "N", ["EF04MA01", "EF04MA02"],
              "Ler, escrever e ordenar números naturais até a ordem de dezenas de milhar; mostrar, por decomposição e composição, que todo número natural pode ser escrito por meio de adições e multiplicações por potências de dez, para compreender o sistema de numeração decimal e desenvolver estratégias de cálculo",
              "Números até dezenas de milhar: ler, escrever, comparar e decompor", "Números até 99.999",
              "Atividades de matemática para o 4º ano sobre números até dezenas de milhar: classes e ordens, números por extenso, decomposição, comparação e arredondamento. 100 exercícios com gabarito.",
              "Cada ordem vale 10 vezes a ordem da sua direita.", "Leia por classes: milhares e unidades simples.",
              body, faq, sets, 1, grade="4-ano")


if __name__ == "__main__":
    main()
