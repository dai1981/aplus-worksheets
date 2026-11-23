# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Comparar e ordenar números (Números, EF01MA05)
  python3 tools/gen_br_matematica_1_comparar_e_ordenar_numeros.py
Maior e menor até 100; comparar pelas dezenas e depois pelas unidades; ordem crescente e decrescente; reta numérica;
o número mais perto; problemas de comparação.
Erros: olhar só as unidades (29 &gt; 31?), confundir crescente e decrescente, ler a reta errado.
"""
import random
from br_common import mcq, lesson, make_unit, mix, reta, Kids
from br_1 import dois_grupos

R = random.Random(80104)
K = Kids(R)


def near(n):
    k = R.choice(["u", "d", "troca"])
    if k == "u":
        m = n // 10 * 10 + R.randint(0, 9)
    elif k == "d":
        m = R.randint(1, 9) * 10 + n % 10
    else:
        m = int(str(n)[::-1]) if n >= 10 and n % 10 else R.randint(1, 99)
    return m


def s1_maior():
    a = R.randint(10, 99)
    b = near(a)
    if a == b or b < 1:
        return None
    big = R.random() < 0.6
    ans = max(a, b) if big else min(a, b)
    return mcq("Qual é o %s: %d ou %d?" % ("maior" if big else "menor", a, b), str(ans), [str(a if ans == b else b), "são iguais", "não dá para saber"],
               ("As dezenas são iguais; compare as unidades" if a // 10 == b // 10 else "Compare primeiro as dezenas") + ": o %s é <b>%d</b>." % ("maior" if big else "menor", ans))


def s1_figuras():
    a, b = R.randint(2, 10), R.randint(2, 10)
    if a == b:
        return None
    p = dois_grupos(a, "star", b, "heart", "e")
    return mcq(p + "Qual número é maior: o das estrelas (%d) ou o dos corações (%d)?" % (a, b), str(max(a, b)), [str(min(a, b)), "são iguais", str(a + b)],
               "%d é maior que %d: <b>%d</b>." % (max(a, b), min(a, b), max(a, b)))


def s2_ordem():
    xs = set()
    base = R.randint(1, 8) * 10
    while len(xs) < 4:
        xs.add(R.choice([base + R.randint(0, 9), R.randint(1, 99)]))
    xs = list(xs)
    R.shuffle(xs)
    up = R.random() < 0.5
    s = sorted(xs, reverse=not up)
    w1 = sorted(xs, reverse=up)
    w2 = s[:]
    w2[1], w2[2] = w2[2], w2[1]
    w3 = s[:]
    w3[0], w3[3] = w3[3], w3[0]
    f = lambda L: ", ".join(map(str, L))
    return mcq("Coloque em ordem %s: %s" % ("crescente (do menor para o maior)" if up else "decrescente (do maior para o menor)", f(xs)), f(s), [f(w1), f(w2), f(w3)],
               "Ordem %s: <b>%s</b>." % ("crescente" if up else "decrescente", f(s)))


def s2_maior_de_quatro():
    xs = set()
    while len(xs) < 4:
        xs.add(R.randint(5, 99))
    xs = list(xs)
    big = R.random() < 0.5
    ans = max(xs) if big else min(xs)
    return mcq("Qual é o %s número? %s" % ("maior" if big else "menor", ", ".join(map(str, xs))), str(ans), [str(x) for x in xs if x != ans],
               "O %s é <b>%d</b>." % ("maior" if big else "menor", ans))


def s3_reta():
    step = R.choice([1, 10])
    lo = R.randint(0, 9) * 10 if step == 1 else 0
    hi = lo + 10 * step
    k = R.randint(1, 9)
    v = lo + k * step
    return mcq(reta(lo, hi, step, [(v, "A")], [lo, hi], width=420) + "Que número a seta A mostra?", str(v), [str(v + step), str(v - step), str(lo + k) if step == 10 else str(v + 2)],
               "Cada tracinho vale %d. Conte a partir do %d: <b>%d</b>." % (step, lo, v))


def s3_perto():
    n = R.randint(11, 98)
    if n % 10 in (0, 5):
        return None
    lo, hi = n // 10 * 10, n // 10 * 10 + 10
    ans = lo if n - lo < 5 else hi
    return mcq("O número %d está mais perto de %d ou de %d?" % (n, lo, hi), str(ans), [str(hi if ans == lo else lo), "dos dois igual", str(n + 1)],
               "%d está a %d de %d e a %d de %d: <b>%d</b>." % (n, n - lo, lo, hi - n, hi, ans))


def s5_problema():
    (a, ga), (b, gb) = K.two()
    x, y = R.randint(10, 99), R.randint(10, 99)
    if x == y:
        return None
    what = R.choice([("tem", "figurinhas"), ("fez", "pontos"), ("tem", "bolinhas de gude"), ("leu", "páginas")])
    big = R.random() < 0.6
    win = a if (x > y) == big else b
    dois = "as duas" if ga == gb == "ela" else "os dois"
    return mcq("%s %s %d %s e %s %s %d. Quem %s %s?" % (a, what[0], x, what[1], b, what[0], y, what[0], "mais" if big else "menos"), win, [b if win == a else a, "%s %s a mesma quantidade" % (dois, {"tem": "têm", "fez": "fizeram", "leu": "leram"}[what[0]]), "não dá para saber"],
               "%d %s %d: <b>%s</b>." % (x, "&gt;" if x > y else "&lt;", y, win))


def main():
    seen = set()
    sets = [
        ("Qual é maior?", mix(R, seen, [(s1_figuras, 8), (s1_maior, 12)])),
        ("Maior e menor", mix(R, seen, [(s1_maior, 10), (s2_maior_de_quatro, 10)])),
        ("Ordem crescente e decrescente", mix(R, seen, [(s2_ordem, 20)])),
        ("Reta numérica", mix(R, seen, [(s3_reta, 12), (s3_perto, 8)])),
        ("Problemas de comparação", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para comparar números de dois algarismos, olhe primeiro as <b>dezenas</b>: 52 &gt; 48, porque 5 dezenas é mais que 4.",
         "Se as dezenas forem iguais, olhe as <b>unidades</b>: 36 &lt; 38.",
         "Na ordem <b>crescente</b> os números vão do menor para o maior; na <b>decrescente</b>, do maior para o menor.",
         "Na reta numérica, os números aumentam para a direita."],
        [("41 ou 39?", ["dezenas: 4 &gt; 3"], "41 é maior"),
         ("Crescente: 25, 8, 61", ["menor primeiro"], "8, 25, 61")],
        [["Olhar só as unidades (29 &gt; 31?)", "Compare primeiro as dezenas: 3 &gt; 2, então 31 &gt; 29."],
         ["Trocar crescente e decrescente", "Crescente sobe como uma escada: do menor para o maior."],
         ["Contar o 0 da reta como 1", "O primeiro tracinho é o 0."]],
        reta(0, 10, 1, [(7, "A")], [0, 10], width=420))
    faq = [("Como ensinar a comparar números?", "Use o material dourado ou palitos em grupos de 10: quem tem mais grupos de 10 é maior; se for igual, compare os soltos."),
           ("O que é a reta numérica?", "É uma linha com os números em ordem. Ajuda a ver qual número é maior (fica mais à direita) e qual está mais perto.")]
    make_unit(R, "comparar-e-ordenar-numeros", "N", ["EF01MA05"],
              "Comparar números naturais de até duas ordens em situações cotidianas, com e sem suporte da reta numérica",
              "Comparar e ordenar números até 100", "Comparar e ordenar",
              "Atividades de matemática para o 1º ano sobre comparar e ordenar números até 100: maior e menor, ordem crescente e decrescente, reta numérica. 100 exercícios com gabarito.",
              "Compare primeiro as dezenas.", "Depois, as unidades.",
              body, faq, sets, 4, grade="1-ano")


if __name__ == "__main__":
    main()
