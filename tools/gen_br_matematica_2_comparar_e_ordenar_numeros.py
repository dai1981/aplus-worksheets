# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Comparar e ordenar números (Números, EF02MA01)
  python3 tools/gen_br_matematica_2_comparar_e_ordenar_numeros.py
Maior e menor com &gt; e &lt; até 1.000; ordem crescente e decrescente; antecessor e sucessor; reta numérica;
formar o maior e o menor número com três algarismos; problemas de comparação.
Erros: olhar só as unidades, achar que 99 &gt; 102 porque tem algarismos maiores, trocar crescente e decrescente.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, reta, Kids
from br_2 import wrong

R = random.Random(80202)
K = Kids(R)


def three():
    return R.randint(100, 999)


def near(n):
    k = R.choice(["d", "u", "c", "len"])
    if k == "d":
        m = n // 100 * 100 + R.randint(0, 9) * 10 + n % 10
    elif k == "u":
        m = n // 10 * 10 + R.randint(0, 9)
    elif k == "c":
        m = R.randint(1, 9) * 100 + n % 100
    else:
        m = R.randint(10, 99)
    return m


def s1_sinal():
    a = three()
    b = near(a)
    if a == b:
        return None
    if R.random() < 0.5:
        a, b = b, a
    s = "&gt;" if a > b else "&lt;"
    t = "&lt;" if s == "&gt;" else "&gt;"
    A, B = num(a), num(b)
    return mcq("Compare %s e %s. Qual frase está certa?" % (A, B), "%s %s %s" % (A, s, B), ["%s %s %s" % (A, t, B), "%s = %s" % (A, B), "%s %s %s" % (B, s, A)],
               "Compare as centenas, depois as dezenas, depois as unidades. <b>%s %s %s</b> (%s é %s que %s)." % (A, s, B, A, "maior" if s == "&gt;" else "menor", B))


def s1_maior():
    a = three()
    xs = {a}
    while len(xs) < 4:
        xs.add(near(a))
    xs = sorted(xs)
    big = R.random() < 0.6
    ans = xs[-1] if big else xs[0]
    R.shuffle(xs)
    return mcq("Qual é o %s número? %s" % ("maior" if big else "menor", ", ".join(num(x) for x in xs)), num(ans), [num(x) for x in xs if x != ans],
               "Comece pelas centenas. O %s é <b>%s</b>." % ("maior" if big else "menor", num(ans)))


def s2_ordem():
    a = three()
    xs = {a}
    while len(xs) < 4:
        xs.add(near(a))
    xs = list(xs)
    R.shuffle(xs)
    up = R.random() < 0.5
    s = sorted(xs, reverse=not up)
    w1 = sorted(xs, reverse=up)
    w2 = s[:]
    w2[1], w2[2] = w2[2], w2[1]
    w3 = s[:]
    w3[0], w3[1] = w3[1], w3[0]
    f = lambda L: ", ".join(num(x) for x in L)
    return mcq("Coloque em ordem %s: %s" % ("crescente (do menor para o maior)" if up else "decrescente (do maior para o menor)", f(xs)), f(s), [f(w1), f(w2), f(w3)],
               "Ordem %s: <b>%s</b>." % ("crescente" if up else "decrescente", f(s)))


def s2_vizinhos():
    n = R.randint(101, 998)
    if R.random() < 0.4:
        n = R.choice([R.randint(1, 9) * 100, R.randint(10, 99) * 10, R.randint(1, 9) * 100 + 99, R.randint(10, 99) * 10 + 9])
        if not 100 < n < 1000:
            return None
    k = R.choice(["ant", "suc", "entre"])
    if k == "ant":
        return mcq("Qual é o antecessor de %s (o número que vem logo antes)?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 100) if n > 200 else num(n + 10)],
                   "Antecessor = número − 1: <b>%s</b>." % num(n - 1))
    if k == "suc":
        return mcq("Qual é o sucessor de %s (o número que vem logo depois)?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 100) if n < 900 else num(n - 10)],
                   "Sucessor = número + 1: <b>%s</b>." % num(n + 1))
    return mcq("Que número fica entre %s e %s?" % (num(n - 1), num(n + 1)), num(n), [num(n + 2), num(n - 2), num(n + 10)],
               "%s, <b>%s</b>, %s." % (num(n - 1), num(n), num(n + 1)))


def s3_reta():
    step = R.choice([1, 10, 100])
    if step == 1:
        lo = R.randint(10, 98) * 10
    elif step == 10:
        lo = R.randint(1, 8) * 100
    else:
        lo = 0
    hi = lo + 10 * step
    k = R.randint(1, 9)
    v = lo + k * step
    pic = reta(lo, hi, step, [(v, "A")], [lo, hi], width=440)
    return mcq(pic + "Que número a seta A indica?", num(v), [num(lo + (k + 1) * step), num(lo + (k - 1) * step) if k > 1 else num(hi - step) if hi - step != v else num(lo), num(lo + k)],
               "Cada tracinho vale %d. %s + %d × %d = <b>%s</b>." % (step, num(lo), k, step, num(v)))


def s3_perto():
    n = R.randint(101, 989)
    if n % 10 == 5 or n % 10 == 0:
        return None
    lo, hi = n // 10 * 10, n // 10 * 10 + 10
    ans = lo if n - lo < hi - n else hi
    return mcq("%s está mais perto de %s ou de %s?" % (num(n), num(lo), num(hi)), num(ans), [num(hi if ans == lo else lo), "dos dois igual", num(n // 100 * 100)],
               "%s está a %d de %s e a %d de %s: mais perto de <b>%s</b>." % (num(n), n - lo, num(lo), hi - n, num(hi), num(ans)))


def s4_algarismos():
    ds = R.sample(range(10), 3)
    if R.random() < 0.3 and 0 not in ds:
        ds[R.randrange(3)] = 0
    if len(set(ds)) < 3:
        return None
    big = R.random() < 0.5
    s = sorted(ds, reverse=big)
    if not big and s[0] == 0:
        s[0], s[1] = s[1], s[0]
    ans = int("".join(map(str, s)))
    rev = int("".join(map(str, sorted(ds, reverse=not big)))) if sorted(ds, reverse=not big)[0] else None
    alt = [int("".join(map(str, p))) for p in ([s[0], s[2], s[1]], [s[1], s[0], s[2]]) if p[0]]
    return mcq("Usando os algarismos %s (uma vez cada), qual é o %s número que se pode formar?" % (", ".join(map(str, ds)), "maior" if big else "menor"), num(ans),
               [num(x) for x in [rev] + alt if x and x != ans] + [str(int("".join(map(str, sorted(ds)))))],
               "%s: <b>%s</b>." % ("Do maior algarismo para o menor" if big else "Do menor para o maior, sem começar com 0", num(ans)))


CENAS5 = [("fez", "pontos num jogo", "fez"), ("tem", "figurinhas", "tem"), ("leu", "páginas neste ano", "leu"), ("deu", "pulos de corda", "deu"), ("juntou", "tampinhas", "juntou")]


def s5_problema():
    (a, ga), (b, gb) = K.two()
    v, what, v2 = R.choice(CENAS5)
    x = three()
    y = near(x)
    if x == y or y < 100:
        return None
    big = R.random() < 0.6
    win = a if (x > y) == big else b
    dois = "as duas" if ga == gb == "ela" else "os dois"
    return mcq("%s %s %s %s e %s %s %s. Quem %s %s?" % (a, v, num(x), what, b, v, num(y), v2, "mais" if big else "menos"), win, [b if win == a else a, "%s a mesma quantidade" % dois, "não dá para saber"],
               "%s %s %s, então <b>%s</b> %s %s." % (num(x), "&gt;" if x > y else "&lt;", num(y), win, v2, "mais" if big else "menos"))


def main():
    seen = set()
    sets = [
        ("Maior que e menor que", mix(R, seen, [(s1_sinal, 12), (s1_maior, 8)])),
        ("Ordem, antecessor e sucessor", mix(R, seen, [(s2_ordem, 10), (s2_vizinhos, 10)])),
        ("Reta numérica", mix(R, seen, [(s3_reta, 12), (s3_perto, 8)])),
        ("Formar números com algarismos", mix(R, seen, [(s4_algarismos, 14), (s1_sinal, 6)])),
        ("Problemas de comparação", mix(R, seen, [(s5_problema, 14), (s1_maior, 6)])),
    ]
    body = lesson(
        ["Para comparar, olhe primeiro as <b>centenas</b>. Se forem iguais, olhe as dezenas; depois, as unidades.",
         "Um número com 3 algarismos é sempre maior que um número com 2 algarismos: 102 &gt; 99.",
         "<b>&gt;</b> quer dizer «maior que»; <b>&lt;</b> quer dizer «menor que». A ponta aberta fica do lado do maior.",
         "O <b>antecessor</b> vem logo antes (−1); o <b>sucessor</b> vem logo depois (+1)."],
        [("456 ou 465?", ["centenas iguais (4)", "dezenas: 5 &lt; 6"], "456 &lt; 465"),
         ("Sucessor de 399", ["399 + 1"], "400")],
        [["Olhar só as unidades", "Comece pelas centenas."],
         ["Achar 99 &gt; 102", "Quem tem mais algarismos é maior."],
         ["Trocar crescente e decrescente", "Crescente: do menor para o maior."]],
        reta(400, 500, 10, [(450, "A")], [400, 500], width=440))
    faq = [("Como ensinar os sinais > e <?", "Diga que a «boca» do sinal sempre abre para o número maior. Depois leia em voz alta: 345 > 299, «345 é maior que 299»."),
           ("O que é ordem crescente?", "É do menor para o maior, como uma escada que sobe. Decrescente é do maior para o menor.")]
    make_unit(R, "comparar-e-ordenar-numeros", "N", ["EF02MA01"],
              "Comparar e ordenar números naturais (até a ordem de centenas) pela compreensão de características do sistema de numeração decimal (valor posicional e função do zero)",
              "Comparar e ordenar números até 1.000", "Comparar e ordenar",
              "Atividades de matemática para o 2º ano sobre comparar e ordenar números até 1.000: maior e menor, sinais maior que e menor que, ordem crescente e decrescente, antecessor e sucessor, reta numérica. 100 exercícios com gabarito.",
              "Compare primeiro as centenas.", "> maior que, < menor que.",
              body, faq, sets, 2, grade="2-ano")


if __name__ == "__main__":
    main()
