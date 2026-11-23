# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Comparar e ordenar frações e decimais (Números, EF05MA05)
  python3 tools/gen_br_matematica_5_comparar_e_ordenar_fracoes_e_decimais.py
Comparar e ordenar números decimais; comparar frações (mesmo denominador, mesmo numerador, com 1/2, por equivalência);
fração e decimal juntos (1/2 = 0,5; 1/4 = 0,25 …); reta numérica; problemas.
Erros: 0,45 > 0,5 porque 45 > 5; 1/8 > 1/4 porque 8 > 4; esquecer de igualar o número de casas decimais.
"""
import random
from fractions import Fraction as Fr
from br_common import mcq, lesson, make_unit, mix, dz, fr, reta, faixa, Kids

R = random.Random(80505)
K = Kids(R)
LT, GT = "&lt;", "&gt;"
FD = [(1, 2, 5, 1), (1, 4, 25, 2), (3, 4, 75, 2), (1, 5, 2, 1), (2, 5, 4, 1), (3, 5, 6, 1), (4, 5, 8, 1), (1, 10, 1, 1), (3, 10, 3, 1),
      (7, 10, 7, 1), (9, 10, 9, 1), (1, 20, 5, 2), (1, 25, 4, 2), (3, 20, 15, 2), (1, 100, 1, 2), (17, 100, 17, 2)]


def frases(x, y, sx, sy):
    """4 frases sobre x e y; a certa primeiro"""
    sign = "=" if x == y else (GT if x > y else LT)
    good = "%s %s %s" % (sx, sign, sy)
    others = ["%s %s %s" % (sx, s, sy) for s in ("=", GT, LT) if s != sign]
    other = "%s %s %s" % (sy, sign, sx) if sign != "=" else "%s %s %s" % (sy, GT, sx)
    return good, others + [other]


def dpair():
    k = R.choice(["casas", "casas", "inteiro", "zero", "igual"])
    if k == "casas":
        a = R.randint(1, 9)
        b = R.randint(10, 99)
        if b // 10 == a or b % 10 == 0:
            return None
        return (a * 10, 1, a), (b, 2, b)
    if k == "inteiro":
        ip = R.randint(1, 9)
        a, b = ip * 10 + R.randint(1, 9), ip * 100 + R.randint(1, 99)
        if b % 10 == 0 or b // 10 == a:
            return None
        return (a * 100, 1, a), (b * 10, 2, b)
    if k == "zero":
        a = R.randint(1, 9)
        b = R.randint(1, 9)
        return (a * 100, 1, a), (b * 10, 2, b)
    a = R.randint(1, 9)
    return (a * 100, 1, a), (a * 100, 2, a * 10)


def s1_comparar():
    p = dpair()
    if not p:
        return None
    (vx, kx, nx), (vy, ky, ny) = p
    X, Y = nx * 10 ** (3 - kx), ny * 10 ** (3 - ky)
    sx, sy = dz(nx, kx), dz(ny, ky, True)
    if R.random() < 0.5:
        sx, sy, X, Y = sy, sx, Y, X
    good, w = frases(X, Y, sx, sy)
    return mcq("Qual frase está certa? (Compare %s e %s.)" % (sx, sy), good, w,
               "Iguale as casas decimais: %s e %s. Compare: <b>%s</b>." % (dz(X, 3, True), dz(Y, 3, True), good))


def s1_maior():
    k = R.choice(["maior", "menor"])
    ip = R.randint(0, 5)
    vals = set()
    while len(vals) < 4:
        kk = R.choice([1, 2, 3])
        vals.add(ip * 1000 + R.randint(1, 10 ** kk - 1) * 10 ** (3 - kk))
    vs = sorted(vals)
    strs = {v: dz(v, 3) for v in vs}
    if len(set(strs.values())) < 4:
        return None
    sh = vs[:]
    R.shuffle(sh)
    ans = vs[-1] if k == "maior" else vs[0]
    return mcq("Qual é o %s número? %s" % (k, "; ".join(strs[v] for v in sh)), strs[ans], [strs[v] for v in vs if v != ans],
               "Escreva todos com 3 casas: %s. O %s é <b>%s</b>." % ("; ".join(dz(v, 3, True) for v in sh), k, strs[ans]))


def s2_ordem():
    k = R.choice(["crescente", "decrescente"])
    ip = R.randint(0, 9)
    vals = set()
    while len(vals) < 4:
        kk = R.choice([1, 2, 2, 3])
        vals.add(ip * 1000 + R.randint(1, 10 ** kk - 1) * 10 ** (3 - kk) + (R.choice([0, 1000]) if R.random() < 0.2 else 0))
    vs = sorted(vals)
    if len({dz(v, 3) for v in vs}) < 4:
        return None
    o = vs if k == "crescente" else vs[::-1]
    sep = " %s " % (LT if k == "crescente" else GT)
    sh = vs[:]
    R.shuffle(sh)
    good = sep.join(dz(v, 3) for v in o)
    byl = sorted(vs, key=lambda v: (v // 1000, int(dz(v, 3).split(",")[1]) if "," in dz(v, 3) else 0))
    if k == "decrescente":
        byl = byl[::-1]
    w = [sep.join(dz(v, 3) for v in byl), sep.join(dz(v, 3) for v in o[::-1]), sep.join(dz(v, 3) for v in [o[1], o[0], o[2], o[3]]), sep.join(dz(v, 3) for v in [o[0], o[2], o[1], o[3]])]
    return mcq("Escreva em ordem %s: %s" % (k, "; ".join(dz(v, 3) for v in sh)), good, w,
               "Com 3 casas decimais: %s. Ordem %s: <b>%s</b>." % ("; ".join(dz(v, 3, True) for v in sh), k, good))


def s3_fracoes():
    k = R.choice(["den", "num", "meio", "equiv", "um"])
    if k == "den":
        d = R.randint(5, 12)
        a, b = R.sample(range(1, d), 2)
        x, y, sx, sy, why = Fr(a, d), Fr(b, d), fr(a, d), fr(b, d), "Mesmo denominador: a maior é a que tem o maior numerador."
    elif k == "num":
        n = R.randint(1, 4)
        a, b = R.sample(range(n + 1, 13), 2)
        x, y, sx, sy, why = Fr(n, a), Fr(n, b), fr(n, a), fr(n, b), "Mesmo numerador: quanto maior o denominador, menores são as partes."
    elif k == "meio":
        d = R.randint(5, 12)
        a = R.randint(1, d - 1)
        if 2 * a == d:
            return None
        x, y, sx, sy, why = Fr(a, d), Fr(1, 2), fr(a, d), fr(1, 2), "Metade de %d é %s: compare %d com essa metade." % (d, dz(d * 5, 1), a)
    elif k == "equiv":
        b = R.choice([2, 3, 4, 5])
        a = R.randint(1, b - 1)
        m = R.choice([2, 3])
        c = a * m + R.choice([-1, 0, 1])
        if c <= 0 or c >= b * m:
            return None
        x, y, sx, sy = Fr(a, b), Fr(c, b * m), fr(a, b), fr(c, b * m)
        why = "Escreva %s com denominador %d: %s. Agora compare os numeradores." % (fr(a, b), b * m, fr(a * m, b * m))
    else:
        d = R.randint(3, 9)
        a = R.randint(d + 1, 2 * d)
        x, y, sx, sy, why = Fr(a, d), Fr(1), fr(a, d), "1", "Numerador maior que o denominador: a fração é maior que 1."
    if R.random() < 0.5:
        x, y, sx, sy = y, x, sy, sx
    good, w = frases(x, y, sx, sy)
    return mcq("Qual frase está certa? (Compare %s e %s.)" % (sx, sy), good, w, why + " <b>%s</b>." % good)


def s3_ordem_frac():
    d = R.randint(5, 12)
    k = R.choice(["den", "num"])
    if k == "den":
        ns = sorted(R.sample(range(1, d), 4))
        fs = [(n, d) for n in ns]
    else:
        n = R.randint(1, 3)
        ds = sorted(R.sample(range(n + 1, 13), 4), reverse=True)
        fs = [(n, x) for x in ds]
    sh = fs[:]
    R.shuffle(sh)
    good = " &lt; ".join(fr(*f) for f in fs)
    w = [" &lt; ".join(fr(*f) for f in fs[::-1]), " &lt; ".join(fr(*f) for f in [fs[1], fs[0], fs[2], fs[3]]), " &lt; ".join(fr(*f) for f in [fs[0], fs[1], fs[3], fs[2]])]
    return mcq("Escreva em ordem crescente: %s" % ", ".join(fr(*f) for f in sh), good, w,
               ("Mesmo denominador: ordene pelos numeradores." if k == "den" else "Mesmo numerador: quanto maior o denominador, menor a fração.") + " <b>%s</b>." % good)


def s4_frac_dec():
    a, b, n, k = R.choice(FD)
    if R.random() < 0.5:
        cands = (["%d,%d" % (a, b), "%d,%d" % (b, a)] if b <= 10 else []) + [dz(n, k + 1), dz(n, k - 1) if k > 1 else dz(n, 2), dz(10 ** k - n, k)]
        mid = "" if b == 10 ** k else " = %s" % fr(n, 10 ** k)
        return mcq("Que número decimal é igual a %s?" % fr(a, b), dz(n, k), cands, "%s%s = <b>%s</b>." % (fr(a, b), mid, dz(n, k)))
    c = R.choice([x for x in FD if x[:2] != (a, b)])
    X, Y = Fr(a, b), Fr(c[0], c[1])
    sx, sy = fr(a, b), dz(c[2], c[3])
    if X == Y:
        return None
    good, w = frases(X, Y, sx, sy)
    return mcq("Qual frase está certa? (Compare %s e %s.)" % (sx, sy), good, w,
               "Escreva %s como decimal: %s. Compare com %s: <b>%s</b>." % (fr(a, b), dz(n, k), sy, good))


def s4_reta():
    a, b, n, k = R.choice([x for x in FD if x[3] == 1 or x[2] in (25, 75)])
    if k == 1:
        svg = reta(0, 10, 1, [(n, "A")], labels=[0, 10]).replace(">10<", ">1<")
        return mcq(svg + "A reta vai de 0 a 1, dividida em décimos. Que número a letra A marca?", dz(n, 1), [dz(n, 2), dz(10 - n, 1), fr(1, n) if n > 1 else fr(1, 2), str(n)],
                   "A está no %dº risquinho: %s = <b>%s</b>%s." % (n, fr(n, 10), dz(n, 1), "" if b == 10 else " = %s" % fr(a, b)))
    svg = reta(0, 4, 1, [(n // 25, "A")], labels=[0, 4]).replace(">4<", ">1<")
    return mcq(svg + "A reta vai de 0 a 1, dividida em 4 partes iguais. Que número decimal a letra A marca?", dz(n, 2), [dz(n // 25, 1), dz(100 - n, 2), "0,4", dz(n // 25 * 2, 1)],
               "Cada parte vale %s = 0,25. A marca %s = <b>%s</b>." % (fr(1, 4), fr(a, b), dz(n, 2)))


def s5_problema():
    k = R.choice(["salto", "corrida", "chocolate", "suco", "peso", "pizza"])
    p, g = K.next()
    q, h = K.next()
    if p == q:
        return None
    if k in ("salto", "corrida", "peso"):
        u = {"salto": ("saltou", "m", "Quem saltou mais longe?"), "corrida": ("correu 100 m em", "s", "Quem foi mais rápido ou mais rápida?"), "peso": ("tem massa de", "kg", "Quem é mais pesado ou mais pesada?")}[k]
        if k == "salto":
            a, b = R.randint(250, 399), R.randint(25, 39) * 10
        elif k == "corrida":
            a, b = R.randint(140, 199), R.randint(14, 19) * 10
        else:
            a, b = R.randint(300, 459), R.randint(30, 45) * 10
        if a == b or abs(a - b) > 40:
            return None
        sa, sb = dz(a, 2), dz(b, 2)
        best = (p if a < b else q) if k == "corrida" else (p if a > b else q)
        return mcq("%s %s %s %s. %s %s %s %s. %s" % (p, u[0], sa, u[1], q, u[0], sb, u[1], u[2]), best, [q if best == p else p, "Empataram", "Não dá para saber"],
                   "%s %s e %s %s → %s. %s<b>%s</b>." % (sa, u[1], dz(b, 2, True), u[1], (GT if a > b else LT).join(["%s " % sa, " %s" % dz(b, 2, True)]),
                                                       "Na corrida, quem leva menos tempo chega primeiro: " if k == "corrida" else "", best))
    if k == "chocolate":
        d1, d2 = R.sample([3, 4, 5, 6, 8, 10], 2)
        return mcq("%s comeu %s de uma barra de chocolate e %s comeu %s de uma barra igual. Quem comeu mais?" % (p, fr(1, d1), q, fr(1, d2)), p if d1 < d2 else q,
                   [q if d1 < d2 else p, "Comeram a mesma quantidade", "Não dá para saber"],
                   "Mesmo numerador: a fração com o menor denominador é a maior. <b>%s</b>." % (p if d1 < d2 else q))
    if k == "suco":
        a, b, n, kk = R.choice([x for x in FD if x[1] <= 10])
        c = R.randint(1, 99)
        if c * 10 ** (3 - 2) == n * 10 ** (3 - kk):
            return None
        X, Y = n * 10 ** (3 - kk), c * 10
        return mcq("%s bebeu %s de litro de suco e %s bebeu %s L. Quem bebeu mais?" % (p, fr(a, b), q, dz(c, 2)), p if X > Y else q,
                   [q if X > Y else p, "Beberam a mesma quantidade", "Não dá para saber"],
                   "%s = %s L. Compare com %s L: <b>%s</b>." % (fr(a, b), dz(n, kk), dz(c, 2), p if X > Y else q))
    d = R.choice([6, 8, 10, 12])
    a, b = R.sample(range(1, d), 2)
    return mcq("Duas pizzas iguais foram cortadas em %d pedaços. %s comeu %s de uma e %s comeu %s da outra. Quem comeu menos?" % (d, p, fr(a, d), q, fr(b, d)), p if a < b else q,
               [q if a < b else p, "Comeram a mesma quantidade", "Não dá para saber"], "Mesmo denominador: menos pedaços = menos pizza. <b>%s</b>." % (p if a < b else q))


def main():
    seen = set()
    sets = [
        ("Comparar números decimais", mix(R, seen, [(s1_comparar, 12), (s1_maior, 8)])),
        ("Ordenar números decimais", mix(R, seen, [(s2_ordem, 20)])),
        ("Comparar e ordenar frações", mix(R, seen, [(s3_fracoes, 14), (s3_ordem_frac, 6)])),
        ("Frações e decimais juntos", mix(R, seen, [(s4_frac_dec, 14), (s4_reta, 6)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para comparar decimais, compare primeiro a parte inteira. Se for igual, <b>iguale o número de casas</b> e compare: 0,5 = 0,50 &gt; 0,45.",
         "Frações com o <b>mesmo denominador</b>: a maior tem o maior numerador (" + fr(5, 8) + " &gt; " + fr(3, 8) + ").",
         "Frações com o <b>mesmo numerador</b>: a maior tem o menor denominador (" + fr(1, 4) + " &gt; " + fr(1, 8) + "), porque as partes são maiores.",
         "Para comparar uma fração com um decimal, escreva a fração como decimal: " + fr(1, 2) + " = 0,5; " + fr(1, 4) + " = 0,25; " + fr(3, 4) + " = 0,75."],
        [("Compare 0,7 e 0,65.", ["0,7 = 0,70", "70 centésimos &gt; 65 centésimos"], "0,7 &gt; 0,65"),
         ("Compare " + fr(3, 4) + " e 0,8.", [fr(3, 4) + " = 0,75", "0,75 &lt; 0,80"], fr(3, 4) + " &lt; 0,8")],
        [["Achar que 0,45 &gt; 0,5 porque 45 &gt; 5", "Iguale as casas: 0,45 e 0,50."],
         ["Achar que " + fr(1, 8) + " &gt; " + fr(1, 4) + " porque 8 &gt; 4", "Dividir em 8 partes dá partes menores do que dividir em 4."],
         ["Esquecer a parte inteira: 2,1 &lt; 1,9", "Compare primeiro os inteiros: 2 &gt; 1."]],
        faixa(4, 1) + faixa(8, 1))
    faq = [("Como comparar números decimais?", "Compare a parte inteira; se for igual, complete com zeros para ter o mesmo número de casas e compare como números inteiros (0,5 = 0,50 > 0,45)."),
           ("Como comparar uma fração com um decimal?", "Transforme a fração em decimal (1/4 = 0,25) ou o decimal em fração (0,3 = 3/10) e compare na mesma forma.")]
    make_unit(R, "comparar-e-ordenar-fracoes-e-decimais", "N", ["EF05MA05"],
              "Comparar e ordenar números racionais positivos (representações fracionária e decimal), relacionando-os a pontos na reta numérica",
              "Comparar e ordenar frações e números decimais", "Comparar frações e decimais",
              "Atividades de matemática para o 5º ano sobre comparar e ordenar frações e números decimais: casas decimais, mesmo denominador, mesmo numerador, fração e decimal e reta numérica. 100 exercícios com gabarito.",
              "0,5 = 0,50 > 0,45: iguale as casas decimais.", "Mesmo numerador: menor denominador, fração maior.",
              body, faq, sets, 5, grade="5-ano")


if __name__ == "__main__":
    main()
