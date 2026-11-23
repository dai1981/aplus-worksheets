# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Sequências numéricas (Álgebra, EF03MA10)
  python3 tools/gen_br_matematica_3_sequencias_numericas.py
Sequências crescentes e decrescentes por adições ou subtrações sucessivas (de 2 em 2, de 5 em 5, de 10, 25, 50, 100,
1.000 em 1.000), descobrir a regra, termo que falta, próximo termo, termo errado, sequências de figuras, números pares e ímpares.
Erros: achar a regra olhando só dois números, contar o salto errado quando muda a centena, confundir crescente e decrescente.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, wrap, text, INK, GREEN, FILL, reais

R = random.Random(80311)
STEPS = [2, 3, 4, 5, 10, 20, 25, 50, 100, 200, 500, 1000]


def seq(n=5):
    st = R.choice(STEPS)
    up = R.random() < 0.6
    lo = R.randint(1, 60) if st < 10 else R.randint(1, 40) * st // (5 if st >= 25 else 1)
    if st >= 100:
        lo = R.randint(1, 40) * 50
    a0 = lo if up else lo + st * (n + 2)
    xs = [a0 + (st if up else -st) * i for i in range(n)]
    if min(xs) < 0 or max(xs) > 9999:
        return None
    return xs, st, up


def s1_proximo():
    r = seq()
    if not r:
        return None
    xs, st, up = r
    nxt = xs[-1] + (st if up else -st)
    if nxt < 0:
        return None
    return mcq("Qual é o próximo número da sequência %s, ___?" % ", ".join(num(x) for x in xs), num(nxt),
               [num(xs[-1] + (st if not up else -st)), num(nxt + 1), num(nxt + 10) if st != 10 else num(nxt + 5)],
               "A sequência %s de %s em %s: %s %s %s = <b>%s</b>." % ("cresce" if up else "diminui", num(st), num(st), num(xs[-1]), "+" if up else "−", num(st), num(nxt)))


def s1_regra():
    r = seq()
    if not r:
        return None
    xs, st, up = r
    ok = "%s %s" % ("somar" if up else "subtrair", num(st))
    w = ["%s %s" % ("subtrair" if up else "somar", num(st)), "%s %s" % ("somar" if up else "subtrair", num(st * 2)),
         "%s %s" % ("somar" if up else "subtrair", num(st // 2)) if st % 2 == 0 and st > 2 else "%s %s" % ("somar" if up else "subtrair", num(st + 1))]
    return mcq("Qual é a regra da sequência %s?" % ", ".join(num(x) for x in xs), ok, w,
               "De um número para o seguinte: %s − %s = %s. Regra: <b>%s</b>." % (num(max(xs[1], xs[0])), num(min(xs[1], xs[0])), num(st), ok))


def s2_falta():
    r = seq(6)
    if not r:
        return None
    xs, st, up = r
    i = R.randint(1, 4)
    shown = [num(x) if j != i else "___" for j, x in enumerate(xs)]
    return mcq("Que número falta? %s" % ", ".join(shown), num(xs[i]), [num(xs[i] + st), num(xs[i] - st) if xs[i] - st >= 0 else num(xs[i] + 2 * st), num(xs[i] + 1)],
               "A sequência %s de %s em %s: <b>%s</b>." % ("cresce" if up else "diminui", num(st), num(st), num(xs[i])))


def s2_errado():
    r = seq(6)
    if not r:
        return None
    xs, st, up = r
    i = R.randint(1, 4)
    bad = xs[:]
    bad[i] = xs[i] + R.choice([1, -1, 10 if st != 10 else 5])
    if bad[i] < 0 or bad[i] in xs:
        return None
    return mcq("Na sequência %s, um número está errado. Qual?" % ", ".join(num(x) for x in bad), num(bad[i]),
               [num(bad[j]) for j in (0, 1, 2, 3, 4, 5) if j != i][:3] if i > 2 else [num(bad[j]) for j in (3, 4, 5)],
               "A regra é %s %s. No lugar de %s deveria estar <b>%s</b>; o número errado é <b>%s</b>." % ("somar" if up else "subtrair", num(st), num(bad[i]), num(xs[i]), num(bad[i])))


def s3_salto():
    k = R.choice(["10c", "100m", "1000"])
    if k == "10c":
        a = R.randint(1, 9) * 100 + 70 + R.randint(0, 9)
        xs = [a + 10 * i for i in range(4)]
        return mcq("Continue de 10 em 10: %s, ___" % ", ".join(num(x) for x in xs), num(xs[-1] + 10), [num(xs[-1] + 1), num(xs[-1] + 100), num(xs[-1] - 90)],
                   "%s + 10 = <b>%s</b> (passou de uma centena para a outra)." % (num(xs[-1]), num(xs[-1] + 10)))
    if k == "100m":
        a = R.randint(1, 8) * 1000 + 700 + R.randint(0, 99)
        xs = [a + 100 * i for i in range(3)]
        return mcq("Continue de 100 em 100: %s, ___" % ", ".join(num(x) for x in xs), num(xs[-1] + 100), [num(xs[-1] + 10), num(xs[-1] + 1000), num(xs[-1] - 900)],
                   "%s + 100 = <b>%s</b> (passou para o milhar seguinte)." % (num(xs[-1]), num(xs[-1] + 100)))
    a = R.randint(1, 5) * 1000 + R.randint(1, 999)
    xs = [a + 1000 * i for i in range(3)]
    return mcq("Continue de 1.000 em 1.000: %s, ___" % ", ".join(num(x) for x in xs), num(xs[-1] + 1000), [num(xs[-1] + 100), num(xs[-1] + 1), num(xs[-1] + 10)],
               "Somar 1.000 muda só o algarismo das unidades de milhar: <b>%s</b>." % num(xs[-1] + 1000))


def s3_par():
    k = R.choice(["par", "impar", "qual", "seq"])
    n = R.randint(100, 9998)
    if k == "par":
        if n % 2:
            n += 1
        return mcq("O número %s é…" % num(n), "par", ["ímpar", "nem par nem ímpar", "par e ímpar"],
                   "O algarismo das unidades é %d, que é par: <b>par</b>." % (n % 10))
    if k == "impar":
        if n % 2 == 0:
            n += 1
        return mcq("O número %s é…" % num(n), "ímpar", ["par", "nem par nem ímpar", "par e ímpar"],
                   "O algarismo das unidades é %d, que é ímpar: <b>ímpar</b>." % (n % 10))
    if k == "qual":
        xs = R.sample(range(101, 999, 2), 3)
        p = R.randrange(100, 998, 2)
        return mcq("Qual destes números é par: %s?" % ", ".join(num(x) for x in sorted(xs + [p])), num(p), [num(x) for x in xs],
                   "Par termina em 0, 2, 4, 6 ou 8: <b>%s</b>." % num(p))
    a = R.randrange(101, 990, 2)
    xs = [a + 2 * i for i in range(4)]
    return mcq("Os números %s são todos…" % ", ".join(num(x) for x in xs), "ímpares", ["pares", "múltiplos de 10", "maiores que 1.000"],
               "Terminam em algarismos ímpares e vão de 2 em 2: <b>ímpares</b>.")


def fig_seq(k, n):
    """sequência de figuras: k quadradinhos a mais em cada figura"""
    s, x = [], 10
    for i in range(n):
        m = 1 + k * i
        for j in range(m):
            s.append("<rect x='%d' y='%d' width='14' height='14' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x + (j % 5) * 16, 10 + (j // 5) * 16, FILL, GREEN))
        s.append(text(x + min(m, 5) * 8, 10 + ((m - 1) // 5 + 1) * 16 + 18, "Figura %d" % (i + 1), 12, col=INK))
        x += min(m, 5) * 16 + 24
    return wrap(x, 10 + ((1 + k * (n - 1) - 1) // 5 + 1) * 16 + 30, "".join(s), "sequência de figuras feitas de quadradinhos", lg=True)


def s4_figuras():
    k = R.choice([1, 2, 3])
    n = 3
    ask = R.randint(4, 7)
    v = 1 + k * (ask - 1)
    return mcq(fig_seq(k, n) + "Quantos quadradinhos terá a Figura %d?" % ask, str(v), [str(v + k), str(v - k), str(ask * k), str(v + 1)],
               "Cada figura tem %d %s a mais: 1, %s… A Figura %d tem <b>%d</b>." % (k, "quadradinho" if k == 1 else "quadradinhos", ", ".join(str(1 + k * i) for i in range(1, ask)), ask, v))


def s5_problema():
    k = R.choice(["cofre", "plantas", "corrida", "elevador", "agenda", "calendario"])
    if k == "cofre":
        a, d, w = R.choice([5, 10, 20]), R.choice([2, 5, 10]), R.randint(4, 8)
        tot = a + d * (w - 1)
        return mcq("Na 1ª semana, Lucas guardou %s. A cada semana ele guarda %s a mais que na semana anterior. Quanto vai guardar na %dª semana?" % (reais(a * 100), reais(d * 100), w),
                   reais(tot * 100), [reais((a + d * w) * 100), reais(d * w * 100), reais((tot - d) * 100)],
                   "%d, %s… Na %dª semana: <b>%s</b>." % (a, ", ".join(str(a + d * i) for i in range(1, w)), w, reais(tot * 100)))
    if k == "plantas":
        h, d, s = R.randint(2, 6), R.choice([2, 3, 4]), R.randint(4, 7)
        v = h + d * s
        return mcq("Um pé de feijão tem %d cm e cresce %d cm por dia. Que altura terá daqui a %d dias?" % (h, d, s), "%d cm" % v, ["%d cm" % (d * s), "%d cm" % (v + d), "%d cm" % (h + d + s)],
                   "%d + %d × %d = <b>%d cm</b>." % (h, d, s, v))
    if k == "corrida":
        d = R.choice([100, 200, 250, 500])
        n = R.randint(3, 6)
        return mcq("Num treino, Helena corre %s metros no 1º dia e aumenta %s metros a cada dia. Quantos metros corre no %dº dia?" % (num(d), num(d), n), "%s metros" % num(d * n),
                   ["%s metros" % num(d * (n - 1)), "%s metros" % num(d * (n + 1)), "%s metros" % num(d + n)],
                   "%s, %s, … no %dº dia: <b>%s metros</b>." % (num(d), num(2 * d), n, num(d * n)))
    if k == "elevador":
        a = R.randint(12, 20)
        st = R.choice([2, 3])
        n = R.randint(3, 5)
        return mcq("Um elevador está no %dº andar e desce parando de %d em %d andares. Em que andar ele estará depois de %d paradas?" % (a, st, st, n), "no %dº andar" % (a - st * n),
                   ["no %dº andar" % (a + st * n), "no %dº andar" % (a - st * (n - 1)), "no %dº andar" % (a - n)],
                   "%d − %d × %d = %d: <b>no %dº andar</b>." % (a, st, n, a - st * n, a - st * n))
    if k == "agenda":
        d = R.randint(1, 6)
        return mcq("Uma aula de natação acontece no dia %d e depois a cada 7 dias. Em qual destes dias também há aula: %d, %d, %d ou %d?" % (d, d + 6, d + 14, d + 15, d + 20),
                   str(d + 14), [str(d + 6), str(d + 15), str(d + 20)],
                   "%d, %d, %d, %d… Resposta: <b>%d</b>." % (d, d + 7, d + 14, d + 21, d + 14))
    a = R.randint(2010, 2020)
    return mcq("Uma festa acontece de 4 em 4 anos. A última foi em %d. Em que ano será a próxima depois de %d?" % (a, a + 4), str(a + 8),
               [str(a + 4), str(a + 5), str(a + 12)], "%d, %d, <b>%d</b>." % (a, a + 4, a + 8))


def main():
    seen = set()
    sets = [
        ("Próximo número e regra", mix(R, seen, [(s1_proximo, 10), (s1_regra, 10)])),
        ("Número que falta e número errado", mix(R, seen, [(s2_falta, 12), (s2_errado, 8)])),
        ("Saltos que mudam de ordem e números pares", mix(R, seen, [(s3_salto, 10), (s3_par, 10)])),
        ("Sequências de figuras", mix(R, seen, [(s4_figuras, 10), (s1_proximo, 5), (s2_falta, 5)])),
        ("Problemas com sequências", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Numa sequência, cada número vem do anterior por uma <b>regra</b>: somar ou subtrair sempre o mesmo número.",
         "Para achar a regra, calcule a diferença entre <b>vários</b> números seguidos, não só entre dois.",
         "Sequência <b>crescente</b> aumenta (somar); <b>decrescente</b> diminui (subtrair).",
         "Cuidado quando o salto passa de uma centena ou de um milhar: 380, 390, <b>400</b>, 410."],
        [("5, 9, 13, 17, ___", ["9 − 5 = 4, 13 − 9 = 4", "Regra: somar 4", "17 + 4"], "21"),
         ("2.750, 2.850, 2.950, ___", ["Regra: somar 100", "2.950 + 100"], "3.050")],
        [["2.950 + 100 = 2.1050", "Passou de 9 centenas: forma mais 1 milhar. 3.050."],
         ["Achar a regra olhando só dois números", "Confira a regra em todos os números."],
         ["Somar numa sequência decrescente", "Se os números diminuem, a regra é subtrair."]])
    faq = [("O que é uma sequência recursiva?", "É uma sequência em que cada termo é obtido a partir do anterior, por exemplo somando 5. A BNCC pede que a criança descubra e descreva essa regra."),
           ("Por que estudar sequências no 3º ano?", "Elas ajudam a pensar em regularidades e preparam para a álgebra, além de treinar o cálculo mental com saltos de 10, 100 e 1.000.")]
    make_unit(R, "sequencias-numericas", "A", ["EF03MA10"],
              "Identificar regularidades em sequências ordenadas de números naturais, resultantes da realização de adições ou subtrações sucessivas, por um mesmo número, descrever uma regra de formação da sequência e determinar elementos faltantes ou seguintes",
              "Sequências numéricas: descobrir a regra", "Sequências numéricas",
              "Atividades de matemática para o 3º ano sobre sequências numéricas: próximo número, regra de formação, número que falta, saltos de 10, 100 e 1.000, pares e ímpares, sequências de figuras. 100 exercícios com gabarito.",
              "A regra é somar ou subtrair sempre o mesmo número.", "Confira a regra em todos os números.",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
