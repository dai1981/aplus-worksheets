# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Números inteiros (Números, EF07MA03)
  python3 tools/gen_br_matematica_7_numeros_inteiros.py
Números positivos e negativos em situações (temperatura, saldo, altitude, fuso, gols); reta numérica; oposto (simétrico) e módulo;
comparar e ordenar inteiros; distância entre dois pontos da reta.
Erros: achar que −8 &gt; −3 porque 8 &gt; 3, esquecer que o módulo nunca é negativo, contar a distância de −3 a 5 como 2.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, bank, unit, _svg, _ln, _t, INK, RED

R = random.Random(87002)


def reta_svg(lo, hi, marks):
    W, H = 420, 80
    n = hi - lo
    x = lambda v: 25 + (v - lo) * (W - 50) / float(n)
    s = [_ln(15, 40, W - 15, 40, INK, 2)]
    for v in range(lo, hi + 1):
        s.append(_ln(x(v), 34, x(v), 46, INK, 1.6))
        if (v - lo) % (2 if n > 12 else 1) == 0 or v == 0:
            s.append(_t(x(v), 64, d(v), 13, INK, bold=(v == 0)))
    for v, nm in marks:
        s.append("<circle cx='%.1f' cy='40' r='5' fill='%s'/>" % (x(v), RED))
        s.append(_t(x(v), 24, nm, 15, RED))
    return _svg(W, H, "".join(s), "reta numérica com números inteiros")


def s1_situacao():
    k = R.choice(["temp", "saldo", "alt", "elev"])
    if k == "temp":
        a, b = R.randint(-12, 5), R.randint(1, 15)
        return M("Às 6h, a temperatura numa cidade da serra era %d °C. Até o meio-dia, subiu %d °C. Qual era a temperatura ao meio-dia?" % (a, b) if a < 0 else None, "%s °C" % d(a + b), ["%s °C" % d(a - b), "%s °C" % d(-(a + b)) if a + b else "1 °C", "%s °C" % d(-a + b)],
                 "Partindo de %s, suba %d: <b>%s °C</b>." % (d(a), b, d(a + b))) if a < 0 else None
    if k == "saldo":
        s, g = R.randint(50, 400), R.randint(100, 900)
        if g == s:
            return None
        return M("Uma conta tinha saldo de R$ %d,00 e foi feito um pagamento de R$ %d,00. Qual é o novo saldo?" % (s, g), "R$ %s,00" % d(s - g), ["R$ %s,00" % d(g - s), "R$ %s,00" % d(s + g), "R$ %s,00" % d(-(s + g))],
                 "%d − %d = <b>%s</b>%s." % (s, g, d(s - g), " (saldo negativo, a conta fica devendo)" if s < g else ""))
    if k == "alt":
        a, b = R.randint(100, 900), R.randint(20, 200)
        return M("Um avião voa a %d m de altitude e um submarino está a %d m de profundidade (−%d m). Qual é a distância vertical entre eles?" % (a, b, b), "%d m" % (a + b), ["%d m" % (a - b), "%d m" % b, "%s m" % d(b - a)], "%d − (−%d) = <b>%d m</b>." % (a, b, a + b))
    a = R.randint(-8, -1)
    b = R.randint(1, 8)
    return M("Num prédio, o térreo é o andar 0 e as garagens são −1, −2… Um elevador estava no andar %d e subiu até o %dº andar. Quantos andares subiu?" % (a, b), str(b - a), [str(b + a) if b + a > 0 else str(b), str(b), str(b - a + 1)],
             "De %s até %d: %d − (%s) = <b>%d andares</b>." % (d(a), b, b, d(a), b - a))


def s2_reta():
    lo = R.randint(-10, -4)
    hi = lo + R.choice([10, 12])
    v = R.choice([x for x in range(lo + 1, hi) if x != 0])
    k = R.choice(["ler", "dist"])
    if k == "ler":
        return M(reta_svg(lo, hi, [(v, "A")]) + "Qual número inteiro o ponto A representa?", d(v), [d(-v), d(v + 1), d(v - 1)], "Conte os tracinhos a partir do 0: <b>%s</b>." % d(v))
    w = R.choice([x for x in range(lo, hi + 1) if x != v and (x < 0) != (v < 0)])
    return M(reta_svg(lo, hi, [(v, "A"), (w, "B")]) + "Qual é a distância entre A e B?", d(abs(v - w)), [d(abs(abs(v) - abs(w))) if abs(abs(v) - abs(w)) != abs(v - w) else d(abs(v - w) + 1), d(abs(v - w) + 2), d(v + w) if v + w > 0 else d(abs(v - w) - 1)],
             "Um está de cada lado do zero: %d + %d = <b>%d</b>." % (abs(v), abs(w), abs(v - w)))


def s3_oposto_modulo():
    a = R.choice([x for x in range(-50, 51) if x])
    k = R.choice(["op", "mod", "mod2"])
    if k == "op":
        return M("Qual é o oposto (simétrico) de %s?" % d(a), d(-a), [d(a), d(abs(a)) if a < 0 else d(-abs(a) - 1), "0"], "O oposto fica do outro lado do zero, à mesma distância: <b>%s</b>." % d(-a))
    if k == "mod":
        return M("Qual é o módulo |%s|?" % d(a), d(abs(a)), [d(-abs(a)), d(-a) if a > 0 else d(abs(a) + 1), "0"], "O módulo é a distância até o zero, nunca negativa: <b>%d</b>." % abs(a))
    b = R.randint(1, 30)
    return M("Quais números inteiros têm módulo %d?" % b, "%d e %s" % (b, d(-b)), ["só %d" % b, "só %s" % d(-b), "0 e %d" % b], "Os dois que estão a %d do zero: <b>%d e %s</b>." % (b, b, d(-b)))


def s4_comparar():
    xs = sorted(R.sample(range(-30, 31), 4))
    if all(x >= 0 for x in xs):
        return None
    sh = xs[:]
    R.shuffle(sh)
    k = R.choice(["maior", "menor", "ordem", "sinal"])
    if k == "sinal":
        a, b = R.sample([x for x in range(-20, 21) if x], 2)
        s = "&gt;" if a > b else "&lt;"
        return M("Qual sinal completa: %s ___ %s?" % (d(a), d(b)), s, ["&lt;" if s == "&gt;" else "&gt;", "=", "não dá para comparar"], "Na reta, o maior está mais à direita: %s %s %s." % (d(a), s, d(b)))
    if k == "ordem":
        ok = " &lt; ".join(d(x) for x in xs)
        bad = " &lt; ".join(d(x) for x in sorted(xs, key=abs))
        return M("Qual é a ordem crescente de %s?" % "; ".join(d(x) for x in sh), ok, [bad if bad != ok else " &lt; ".join(d(x) for x in xs[::-1]), " &lt; ".join(d(x) for x in xs[::-1]), " &lt; ".join(d(x) for x in [xs[1], xs[0], xs[2], xs[3]])],
                 "Os negativos vêm primeiro; quanto maior o módulo de um negativo, menor ele é: <b>%s</b>." % ok)
    t = xs[-1] if k == "maior" else xs[0]
    return M("Qual é o %s número: %s?" % (k, "; ".join(d(x) for x in sh)), d(t), [d(x) for x in xs if x != t], "Na reta, o %s fica mais à %s: <b>%s</b>." % (k, "direita" if k == "maior" else "esquerda", d(t)))


s5_conceitos = bank(R, [
    ("Qual é maior: −3 ou −8?", "−3", ["−8", "são iguais", "não dá para comparar"]),
    ("O zero é…", "nem positivo nem negativo", ["positivo", "negativo", "o menor inteiro"]),
    ("Todo número negativo é ___ que qualquer número positivo.", "menor", ["maior", "igual", "às vezes maior"]),
    ("O oposto do oposto de −7 é…", "−7", ["7", "0", "−14"]),
    ("A soma de um número com o seu oposto é…", "0", ["o dobro do número", "1", "−1"]),
    ("Quantos números inteiros há entre −3 e 3 (sem contar os dois)?", "5", ["6", "7", "4"]),
    ("Qual é o maior número inteiro negativo?", "−1", ["0", "−100", "não existe"]),
    ("Um saldo de −R$ 50,00 significa…", "uma dívida de R$ 50,00", ["R$ 50,00 disponíveis", "conta zerada", "R$ 500,00 de dívida"]),
    ("A temperatura de −5 °C é ___ que a de −2 °C.", "mais fria", ["mais quente", "igual", "o dobro"]),
    ("|−12| + |5| é igual a…", "17", ["−7", "7", "−17"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Inteiros no dia a dia", mix(R, seen, [(s1_situacao, 20)])),
        ("Reta numérica", mix(R, seen, [(s2_reta, 20)])),
        ("Oposto e módulo", mix(R, seen, [(s3_oposto_modulo, 20)])),
        ("Comparar e ordenar", mix(R, seen, [(s4_comparar, 20)])),
        ("Revisão", mix(R, seen, [(s5_conceitos, 10), (s2_reta, 5), (s4_comparar, 5)])),
    ]
    body = lesson(
        ["Os <b>números inteiros</b> são …, −3, −2, −1, 0, 1, 2, 3, … Os negativos aparecem em temperaturas abaixo de zero, dívidas, profundidades e andares de garagem.",
         "Na reta numérica, os negativos ficam à esquerda do zero. Quanto mais à direita, maior o número: −2 &gt; −7.",
         "O <b>oposto</b> de 5 é −5 (mesma distância do zero, do outro lado). O <b>módulo</b> |−5| = 5 é a distância até o zero."],
        [("Comparar −9 e −4", ["−4 está mais à direita"], "−4 &gt; −9"),
         ("Distância de −3 a 5", ["3 + 5"], "8")],
        [["Achar que −8 &gt; −3", "Com negativos, maior módulo é número menor."],
         ["Dar módulo negativo", "O módulo é distância: nunca negativo."],
         ["Calcular −3 a 5 como 2", "Passe pelo zero: 3 + 5 = 8."]],
        reta_svg(-6, 6, [(-4, "A"), (3, "B")]))
    faq = [("Como comparar números negativos?", "Imagine a reta numérica: o maior número é o que está mais à direita. Entre dois negativos, o de menor módulo é o maior: −2 &gt; −10."),
           ("O que a BNCC pede no 7º ano?", "Comparar e ordenar números inteiros em diferentes contextos, incluindo o histórico, associá-los a pontos da reta numérica e utilizá-los em situações que envolvam adição e subtração (EF07MA03).")]
    unit(R, "numeros-inteiros", "N", ["EF07MA03"],
         "Comparar e ordenar números inteiros em diferentes contextos, incluindo o histórico, associá-los a pontos da reta numérica e utilizá-los em situações que envolvam adição e subtração",
         "Números inteiros: reta numérica, oposto e módulo", "Números inteiros",
         "Atividades de matemática para o 7º ano sobre números inteiros: positivos e negativos no dia a dia, reta numérica, oposto, módulo, distância, comparar e ordenar. 100 exercícios com gabarito.",
         "Mais à direita na reta, maior.", "Módulo = distância até o zero.",
         body, faq, sets, 2, grade="7-ano")


if __name__ == "__main__":
    main()
