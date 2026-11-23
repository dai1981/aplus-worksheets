# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Comparar e ordenar números (Números, EF03MA01, EF03MA04)
  python3 tools/gen_br_matematica_3_comparar_e_ordenar_numeros.py
Sinais &gt; e &lt;, maior e menor número, ordem crescente e decrescente, antecessor e sucessor, números na reta numérica,
maior e menor número formado com algarismos dados, problemas de comparação.
Erros: olhar só o último algarismo, achar que o número com mais algarismos grandes é maior, confundir crescente e decrescente.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, reta, pl, Kids, reais

R = random.Random(80302)
K = Kids(R)


def close_pair():
    a = R.randint(1000, 9999)
    k = R.choice(["c", "d", "u", "m"])
    s = list(str(a))
    i = {"m": 0, "c": 1, "d": 2, "u": 3}[k]
    alt = [x for x in "0123456789" if x != s[i] and not (i == 0 and x == "0")]
    s[i] = R.choice(alt)
    return a, int("".join(s))


def s1_sinal():
    a, b = close_pair() if R.random() < 0.7 else (R.randint(100, 999), R.randint(1000, 9999))
    if R.random() < 0.5:
        a, b = b, a
    sg = "&gt;" if a > b else "&lt;"
    i = next(k for k in range(4) if str(a).rjust(4)[k] != str(b).rjust(4)[k])
    why = ("%s tem mais algarismos" % num(max(a, b))) if len(str(a)) != len(str(b)) else "compare da esquerda para a direita: a primeira diferença está na ordem das %s" % ["unidades de milhar", "centenas", "dezenas", "unidades"][i]
    A, B = num(a), num(b)
    ok = "%s %s %s" % (A, sg, B)
    other = "&lt;" if sg == "&gt;" else "&gt;"
    return mcq("Compare %s e %s. Qual frase está certa?" % (A, B), ok, ["%s %s %s" % (A, other, B), "%s = %s" % (A, B), "%s %s %s" % (B, sg, A)],
               "%s; então <b>%s</b>." % (why[0].upper() + why[1:], ok))


def s1_maior():
    base = R.randint(1, 8) * 1000 + R.randint(0, 9) * 100
    xs = sorted({base + R.randint(0, 99) for _ in range(6)})
    if len(xs) < 4:
        return None
    xs = R.sample(xs, 4)
    ask = R.choice(["maior", "menor"])
    a = max(xs) if ask == "maior" else min(xs)
    return mcq("Qual é o %s número: %s?" % (ask, ", ".join(num(x) for x in xs[:3]) + " ou " + num(xs[3])), num(a), [num(x) for x in xs if x != a],
               "Os milhares e as centenas são iguais; compare as dezenas e as unidades. O %s é <b>%s</b>." % (ask, num(a)))


def s2_ordem():
    xs = R.sample(range(1000, 9999), 4)
    if R.random() < 0.5:
        m = R.randint(1, 9) * 1000
        xs = [m + R.randint(0, 999) for _ in range(4)]
        if len(set(xs)) < 4:
            return None
    cres = R.random() < 0.5
    ok = sorted(xs, reverse=not cres)
    f = lambda l: " ; ".join(num(x) for x in l)
    w1 = sorted(xs, reverse=cres)
    w2 = sorted(xs, key=lambda x: x % 10, reverse=not cres)
    w3 = ok[:]
    w3[1], w3[2] = w3[2], w3[1]
    return mcq("Coloque em ordem %s: %s." % ("crescente (do menor para o maior)" if cres else "decrescente (do maior para o menor)", ", ".join(num(x) for x in xs)),
               f(ok), [f(w1), f(w2), f(w3)],
               "Ordem %s: <b>%s</b>." % ("crescente" if cres else "decrescente", f(ok)))


def s2_vizinhos():
    n = R.randint(1001, 9998)
    k = R.choice(["suc", "ant", "suc0", "ant0", "entre"])
    if k == "suc0":
        n = n // 100 * 100 + 99
    if k == "ant0":
        n = n // 100 * 100
    if n < 1001 or n > 9998:
        return None
    if k in ("suc", "suc0"):
        return mcq("Qual é o sucessor de %s?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 11)],
                   "O sucessor é %s + 1 = <b>%s</b>." % (num(n), num(n + 1)))
    if k in ("ant", "ant0"):
        return mcq("Qual é o antecessor de %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 11)],
                   "O antecessor é %s − 1 = <b>%s</b>." % (num(n), num(n - 1)))
    a = n - 1
    return mcq("Que número está entre %s e %s?" % (num(a), num(n + 1)), num(n), [num(n + 2), num(a - 1), num(n + 10)],
               "Entre %s e %s está <b>%s</b>." % (num(a), num(n + 1), num(n)))


def s3_reta():
    k = R.choice(["10", "100", "1000"])
    if k == "10":
        lo = R.randint(100, 899) * 10
        v = lo + R.randint(1, 9)
        return mcq(reta(lo, lo + 10, 1, [(v, "A")], [lo, lo + 10]) + "Que número a seta A indica?", num(v),
                   [num(v + 1), num(v - 1), num(lo + 10 * (v - lo))],
                   "Cada risquinho vale 1. Contando a partir de %s: <b>%s</b>." % (num(lo), num(v)))
    if k == "100":
        lo = R.randint(10, 89) * 100
        v = lo + R.randint(1, 9) * 10
        return mcq(reta(lo, lo + 100, 10, [(v, "A")], [lo, lo + 100]) + "Que número a seta A indica?", num(v),
                   [num(lo + (v - lo) // 10), num(v + 10), num(v - 10)],
                   "Cada risquinho vale 10. De %s, conte %s: <b>%s</b>." % (num(lo), pl((v - lo) // 10, "risquinho", "risquinhos"), num(v)))
    v = R.randint(1, 9) * 1000
    return mcq(reta(0, 10000, 1000, [(v, "A")], [0, 10000]) + "Que número a seta A indica?", num(v),
               [num(v // 10), num(v + 1000), num(v - 1000) if v > 1000 else num(v * 10)],
               "Cada risquinho vale 1.000. A seta está no %dº risquinho: <b>%s</b>." % (v // 1000, num(v)))


def s3_perto():
    lo = R.randint(1, 8) * 1000
    v = lo + R.choice([100, 200, 300, 400, 600, 700, 800, 900])
    ask = R.choice(["perto", "entre"])
    if ask == "perto":
        a = lo if v - lo < 500 else lo + 1000
        return mcq("Na reta numérica, %s está mais perto de qual milhar?" % num(v), num(a), [num(lo + 1000 if a == lo else lo), num(v // 100 * 100), num(lo - 1000) if lo > 1000 else num(lo + 2000)],
                   "%s está a %s de %s e a %s de %s: fica mais perto de <b>%s</b>." % (num(v), num(v - lo), num(lo), num(lo + 1000 - v), num(lo + 1000), num(a)))
    return mcq("Entre quais milhares exatos está %s?" % num(v + R.randint(1, 99)), "%s e %s" % (num(lo), num(lo + 1000)),
               ["%s e %s" % (num(lo + 1000), num(lo + 2000)), "%s e %s" % (num(lo - 1000), num(lo)) if lo > 1000 else "0 e %s" % num(lo + 2000), "%s e %s" % (num(v // 100 * 100), num(v // 100 * 100 + 100))],
               "O algarismo das unidades de milhar é %d: o número está entre <b>%s e %s</b>." % (lo // 1000, num(lo), num(lo + 1000)))


def s4_algarismos():
    ds = R.sample(range(1, 10), 4) if R.random() < 0.6 else R.sample(range(0, 10), 4)
    if R.random() < 0.3 and 0 not in ds:
        ds[R.randrange(4)] = 0
    ask = R.choice(["maior", "menor"])
    if ask == "maior":
        a = int("".join(str(x) for x in sorted(ds, reverse=True)))
        w = [int("".join(str(x) for x in sorted(ds))), int("".join(str(x) for x in ds)), a - 9 * (a % 100 // 10 - a % 10) if a % 100 // 10 != a % 10 else None]
    else:
        s = sorted(ds)
        if s[0] == 0:
            s[0], s[1] = s[1], s[0]
        a = int("".join(str(x) for x in s))
        w = [int("".join(str(x) for x in sorted(ds))) if 0 in ds else None, int("".join(str(x) for x in sorted(ds, reverse=True))), int("".join(str(x) for x in ds))]
    return mcq("Com os algarismos %s, sem repetir, qual é o %s número de 4 algarismos?" % (", ".join(str(x) for x in ds), ask), num(a),
               [num(x) if x and x >= 1000 else (str(x) if x else None) for x in w if x != a],
               "Para o %s número, coloque os algarismos do %s para o %s%s: <b>%s</b>." % (ask, "maior" if ask == "maior" else "menor", "menor" if ask == "maior" else "maior",
                                                                                     " (o 0 não pode ficar na frente)" if 0 in ds and ask == "menor" else "", num(a)))


def s5_problema():
    k = R.choice(["cidade", "pontos", "loja", "km", "escola"])
    (p1, _), (p2, _) = K.two()
    if k == "cidade":
        a, b = close_pair()
        c1, c2 = R.sample(["Serra Azul", "Rio Claro", "Vila Nova", "Monte Alegre", "Santa Rita", "Bom Jesus", "Pedra Branca"], 2)
        ans = c1 if a > b else c2
        return mcq("A cidade de %s tem %s habitantes e a de %s tem %s. Qual cidade tem mais habitantes?" % (c1, num(a), c2, num(b)), ans,
                   [c2 if ans == c1 else c1, "As duas têm o mesmo número", "Não dá para saber"],
                   "%s %s %s: <b>%s</b> tem mais habitantes." % (num(a), "&gt;" if a > b else "&lt;", num(b), ans))
    if k == "pontos":
        a, b = close_pair()
        win = p1 if a > b else p2
        return mcq("Num jogo, %s fez %s pontos e %s fez %s. Quem fez mais pontos?" % (p1, num(a), p2, num(b)), win,
                   [p2 if win == p1 else p1, "Empataram", "Quem jogou primeiro"],
                   "%s %s %s: quem fez mais pontos foi <b>%s</b>." % (num(a), "&gt;" if a > b else "&lt;", num(b), win))
    if k == "loja":
        ps = sorted(R.sample(range(1000, 4000, 10), 3))
        ART = {"geladeira": "Uma", "fogão": "Um", "televisão": "Uma", "sofá": "Um", "bicicleta elétrica": "Uma", "computador": "Um"}
        nomes = R.sample(sorted(ART), 3)
        order = [1, 0, 2]
        ps_ = ["%s %s custa %s" % (ART[nomes[i]] if j == 0 else ART[nomes[i]].lower(), nomes[i], reais(ps[i] * 100)) for j, i in enumerate(order)]
        frase = ps_[0] + ", " + ps_[1] + " e " + ps_[2]
        return mcq("%s. Qual é o mais barato?" % frase, nomes[0], [nomes[1], nomes[2], "Todos custam o mesmo"],
                   "O menor preço é %s: <b>%s</b>." % (reais(ps[0] * 100), nomes[0]))
    if k == "km":
        a = R.randint(1000, 9000)
        b = a + R.choice([-1, 1]) * R.randint(10, 900)
        r1, r2 = R.sample(["São Paulo", "Recife", "Manaus", "Porto Alegre", "Belém", "Fortaleza", "Curitiba"], 2)
        ans = r1 if a < b else r2
        return mcq("Um caminhoneiro está a %s km de %s e a %s km de %s. De qual cidade ele está mais perto?" % (num(a), r1, num(b), r2), ans,
                   [r2 if ans == r1 else r1, "Está à mesma distância", "Não dá para saber"],
                   "Mais perto é a menor distância: %s km. Resposta: <b>%s</b>." % (num(min(a, b)), ans))
    xs = R.sample(range(1100, 1900), 3)
    es = ["Escola A", "Escola B", "Escola C"]
    big = es[xs.index(max(xs))]
    return mcq("A Escola A tem %s alunos, a Escola B tem %s e a Escola C tem %s. Qual escola tem mais alunos?" % tuple(num(x) for x in xs), big,
               [e for e in es if e != big] + ["Todas têm o mesmo número"],
               "O maior número é %s: <b>%s</b>." % (num(max(xs)), big))


def main():
    seen = set()
    sets = [
        ("Maior que e menor que", mix(R, seen, [(s1_sinal, 12), (s1_maior, 8)])),
        ("Ordem crescente, antecessor e sucessor", mix(R, seen, [(s2_ordem, 10), (s2_vizinhos, 10)])),
        ("Números na reta numérica", mix(R, seen, [(s3_reta, 12), (s3_perto, 8)])),
        ("Formar números com algarismos", mix(R, seen, [(s4_algarismos, 14), (s1_sinal, 6)])),
        ("Problemas de comparação", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para comparar dois números, conte os algarismos: o que tem <b>mais algarismos</b> é maior (1.000 &gt; 999).",
         "Com a mesma quantidade de algarismos, compare <b>da esquerda para a direita</b>: primeiro os milhares, depois as centenas, as dezenas e as unidades.",
         "O sinal &gt; quer dizer «maior que» e &lt; quer dizer «menor que». A ponta do sinal aponta para o número menor.",
         "Ordem <b>crescente</b>: do menor para o maior. Ordem <b>decrescente</b>: do maior para o menor."],
        [("Compare 4.528 e 4.582.", ["Milhares iguais (4), centenas iguais (5)", "Dezenas: 2 &lt; 8"], "4.528 &lt; 4.582"),
         ("Maior número com 3, 9, 0 e 6", ["Do maior algarismo para o menor"], "9.630")],
        [["Olhar só o último algarismo: 2.199 &gt; 3.001", "Comece pela esquerda: 2 milhares &lt; 3 milhares."],
         ["Confundir crescente e decrescente", "Crescente cresce: começa pelo menor."],
         ["Colocar o 0 na frente do menor número", "Um número de 4 algarismos não começa com 0: o menor com 0, 3, 6, 9 é 3.069."]])
    faq = [("Como ensinar a comparar números grandes?", "Coloque os dois números no quadro de valor posicional, um embaixo do outro, e compare ordem por ordem, começando pelos milhares."),
           ("Para que serve a reta numérica?", "Ela mostra que os números estão em ordem e ajuda a ver qual está mais perto de um milhar exato ou de uma centena exata.")]
    make_unit(R, "comparar-e-ordenar-numeros", "N", ["EF03MA01", "EF03MA04"],
              "Ler, escrever e comparar números naturais até a ordem de unidade de milhar; estabelecer a relação entre números naturais e pontos da reta numérica para utilizá-la na ordenação dos números naturais",
              "Comparar e ordenar números até 9.999", "Comparar e ordenar números",
              "Atividades de matemática para o 3º ano sobre comparar e ordenar números: sinais maior que e menor que, ordem crescente e decrescente, antecessor e sucessor, reta numérica. 100 exercícios com gabarito.",
              "Compare da esquerda para a direita: milhares, centenas, dezenas, unidades.", "A ponta do sinal aponta para o menor.",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
