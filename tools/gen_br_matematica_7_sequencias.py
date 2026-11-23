# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Sequências (Álgebra, EF07MA14, EF07MA15)
  python3 tools/gen_br_matematica_7_sequencias.py
Sequências recursivas (cada termo a partir do anterior) e não recursivas (termo pela posição n); termo geral de sequências
de primeiro grau (aₙ = 3n + 2); achar um termo distante; sequências de figuras (palitos, bolinhas); quadrados e triângulos.
Erros: somar a diferença à posição em vez do termo, usar n − 1 errado, achar o termo geral só olhando o primeiro termo.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, expr, bank, unit, _svg

R = random.Random(87008)


def an(r, c):
    return "aₙ = %s" % expr([(r, "n"), (c, "")])


def s1_proximo():
    k = R.choice(["ar", "ar", "geo", "quad", "fib"])
    if k == "ar":
        a, r = R.randint(-10, 20), R.choice([-7, -5, -4, -3, 2, 3, 4, 5, 6, 8, 11])
        t = [a + r * i for i in range(5)]
        v = a + r * 5
        why = "some %s a cada termo" % d(r)
    elif k == "geo":
        a, r = R.randint(1, 5), R.choice([2, 3])
        t = [a * r ** i for i in range(5)]
        v = a * r ** 5
        why = "multiplique por %d a cada termo" % r
    elif k == "quad":
        s0 = R.randint(1, 4)
        t = [(s0 + i) ** 2 for i in range(5)]
        v = (s0 + 5) ** 2
        why = "são quadrados perfeitos"
    else:
        a, b = R.randint(1, 3), R.randint(1, 4)
        t = [a, b]
        while len(t) < 5:
            t.append(t[-1] + t[-2])
        v = t[-1] + t[-2]
        why = "cada termo é a soma dos dois anteriores"
    return M("Qual é o próximo termo da sequência %s, …?" % ", ".join(d(x) for x in t), d(v), [d(v + 1), d(2 * t[-1] - t[-2] if k != "ar" else v + (t[1] - t[0])), d(t[-1] + 1) if t[-1] + 1 != v else d(v - 2)],
             "Regra: %s → <b>%s</b>." % (why, d(v)))


def s2_geral():
    r, c = R.choice([2, 3, 4, 5, 6, -2, -3]), R.randint(-5, 10)
    t = [r * n + c for n in range(1, 5)]
    k = R.choice(["lei", "termo"])
    if k == "lei":
        ok = an(r, c)
        return M("Qual é o termo geral da sequência %s, …? (n = 1, 2, 3, …)" % ", ".join(d(x) for x in t), ok, [an(r, t[0]), an(t[0], r) if t[0] != r else an(r + 1, c), an(r, c + r)],
                 "A diferença é %s, então aₙ = %sn + b; para n = 1: %s + b = %s → b = %s. <b>%s</b>." % (d(r), d(r), d(r), d(t[0]), d(c), ok))
    n = R.choice([10, 15, 20, 25, 50, 100])
    v = r * n + c
    return M("Na sequência %s, …, qual é o %dº termo?" % (", ".join(d(x) for x in t), n), d(v), [d(t[0] + r * n), d(r * n), d(v + r)],
             "Termo geral %s; para n = %d: <b>%s</b>." % (an(r, c), n, d(v)))


def palitos_svg(n):
    """quadrados de palitos em fila"""
    s = []
    for i in range(n):
        x = 15 + i * 34
        s.append("<rect x='%d' y='15' width='34' height='34' fill='none' stroke='#8a5a2b' stroke-width='3.5'/>" % x)
    return _svg(30 + n * 34, 64, "".join(s), "%d quadrados feitos com palitos" % n)


def s3_figuras():
    k = R.choice(["palitos", "bolas"])
    if k == "palitos":
        f = R.randint(1, 3)
        n = R.choice([6, 8, 10, 12, 15, 20, 25, 30])
        pics = "".join(palitos_svg(i) for i in (f, f + 1))
        return M(pics + "Com 1 quadrado usamos 4 palitos; com 2 quadrados em fila, 7; com 3, 10. Quantos palitos são necessários para %d quadrados em fila?" % n, d(3 * n + 1), [d(4 * n), d(3 * n), d(3 * n + 4)],
                 "Termo geral 3n + 1 (cada quadrado novo usa 3 palitos): 3 · %d + 1 = <b>%d</b>." % (n, 3 * n + 1))
    a, r = R.randint(1, 5), R.randint(2, 5)
    n = R.choice([10, 12, 15, 20, 30])
    return M("Uma sequência de figuras tem %d, %d, %d e %d bolinhas. Mantendo o padrão, quantas bolinhas terá a figura %d?" % (a, a + r, a + 2 * r, a + 3 * r, n), d(a + r * (n - 1)), [d(a + r * n), d(r * n), d(a * n)],
             "Começa com %d e aumenta %d por figura: %d + %d · (%d − 1) = <b>%d</b>." % (a, r, a, r, n, a + r * (n - 1)))


s4_conceitos = bank(R, [
    ("Uma sequência é <b>recursiva</b> quando…", "cada termo é obtido a partir do anterior", ["cada termo depende só da posição", "não tem regra", "todos os termos são iguais"]),
    ("A regra «aₙ = 5n − 1» é…", "não recursiva (depende da posição n)", ["recursiva", "uma sequência de primos", "um polinômio de grau 2"]),
    ("Na sequência aₙ = 2n + 3, o 1º termo é…", "5", ["3", "2", "6"]),
    ("A sequência 1, 4, 9, 16, … é formada por…", "quadrados perfeitos", ["múltiplos de 4", "números primos", "termos de diferença 3"]),
    ("As sequências 3n + 2 e 3(n + 1) − 1 são…", "equivalentes (dão os mesmos termos)", ["diferentes", "iguais só para n = 1", "recursivas"]),
    ("«Comece em 2 e some 4 a cada passo» dá a sequência…", "2, 6, 10, 14, …", ["4, 8, 12, 16, …", "2, 4, 6, 8, …", "2, 8, 32, …"]),
    ("Qual sequência é recursiva: «a₁ = 1; aₙ = 2 · aₙ₋₁»?", "1, 2, 4, 8, …", ["1, 3, 5, 7, …", "2, 4, 6, 8, …", "1, 2, 3, 4, …"]),
    ("Na sequência dos números ímpares, o 50º termo é…", "99", ["100", "101", "51"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Próximo termo", mix(R, seen, [(s1_proximo, 20)])),
        ("Termo geral", mix(R, seen, [(s2_geral, 20)])),
        ("Termos distantes", mix(R, seen, [(s2_geral, 14), (s4_conceitos, 6)])),
        ("Sequências de figuras", mix(R, seen, [(s3_figuras, 20)])),
        ("Revisão", mix(R, seen, [(s1_proximo, 8), (s3_figuras, 8), (s4_conceitos, 2), (s2_geral, 2)])),
    ]
    body = lesson(
        ["Numa sequência <b>recursiva</b>, cada termo vem do anterior («some 3»). Numa <b>não recursiva</b>, o termo depende da posição n («aₙ = 3n + 1»).",
         "Se a diferença entre termos seguidos é sempre r, o termo geral é aₙ = r · n + b. Use o 1º termo para achar b.",
         "Com o termo geral, calcule qualquer termo sem escrever todos: o 100º termo de 3n + 1 é 301."],
        [("4, 7, 10, 13, …", ["diferença 3", "3 · 1 + b = 4 → b = 1"], "aₙ = 3n + 1"),
         ("20º termo de aₙ = 5n − 2", ["5 · 20 − 2"], "98")],
        [["Somar a diferença à posição", "Some a diferença ao termo anterior."],
         ["Errar o ponto de partida", "Confira: n = 1 dá o primeiro termo?"],
         ["Olhar só o primeiro termo", "Veja quanto a sequência aumenta a cada passo."]],
        palitos_svg(3))
    faq = [("Como achar o termo geral de uma sequência?", "Calcule a diferença entre termos seguidos (r). O termo geral é r · n + b; substitua n = 1 e o primeiro termo para descobrir b."),
           ("O que a BNCC pede no 7º ano?", "Classificar sequências em recursivas e não recursivas (EF07MA15) e utilizar a simbologia algébrica para expressar regularidades encontradas em sequências numéricas (EF07MA14).")]
    unit(R, "sequencias", "A", ["EF07MA14", "EF07MA15"],
         "Classificar sequências em recursivas e não recursivas, reconhecendo que o conceito de recursão está presente não apenas na matemática, mas também nas artes e na literatura; utilizar a simbologia algébrica para expressar regularidades encontradas em sequências numéricas",
         "Sequências: recursivas, termo geral e padrões", "Sequências",
         "Atividades de matemática para o 7º ano sobre sequências: próximo termo, sequências recursivas e não recursivas, termo geral, termos distantes e sequências de figuras. 100 exercícios com gabarito.",
         "aₙ = r · n + b", "Recursiva: a partir do anterior.",
         body, faq, sets, 8, grade="7-ano")


if __name__ == "__main__":
    main()
