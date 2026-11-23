# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Números reais e irracionais (Números, EF09MA01, EF09MA02)
  python3 tools/gen_br_matematica_9_numeros_reais.py
Naturais, inteiros, racionais e irracionais; dízimas periódicas (racionais) e não periódicas (irracionais); √n entre dois inteiros;
localizar irracionais na reta; π e a diagonal do quadrado (segmentos incomensuráveis).
Erros: achar que toda raiz é irracional (√16 = 4), achar que dízima periódica é irracional, achar que π = 3,14 exatamente.
"""
import math
import random
from fractions import Fraction as F
from br_common import reta, lesson
from br_9 import M, d, fq, sq, unit

R = random.Random(89001)
CONJ = ["natural", "inteiro", "racional", "irracional"]


def menor_conj(kind):
    k = R.choice(kind)
    if k == "nat":
        n = R.randint(0, 50)
        return str(n), "natural (e também inteiro, racional e real)", "natural"
    if k == "int":
        n = -R.randint(1, 30)
        return d(n), "inteiro, mas não natural", "inteiro"
    if k == "rac":
        a, b = R.randint(1, 9), R.choice([3, 4, 5, 7, 8])
        if math.gcd(a, b) != 1:
            return None
        x = F(a, b) * R.choice([1, -1])
        if R.random() < 0.5 and b in (4, 5, 8):
            return d(x), "racional (decimal exato)", "racional"
        return fq(x), "racional (fração de inteiros)", "racional"
    if k == "raiz":
        n = R.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18, 20])
        return "√%d" % n, "irracional (%d não é quadrado perfeito)" % n, "irracional"
    if k == "rq":
        m = R.randint(2, 12)
        return "√%d" % (m * m), "natural, pois √%d = %d" % (m * m, m), "natural"
    return R.choice([("π", "irracional", "irracional"), ("0,333…", "racional (dízima periódica = 1/3)", "racional"), ("0,1010010001…", "irracional (não periódica)", "irracional"),
                     ("2,7181818…", "racional (dízima periódica)", "racional"), ("1,41421356…", "irracional (é √2)", "irracional")])


def s1_classificar():
    r = menor_conj(["nat", "int", "rac", "raiz", "rq", "esp"])
    if not r:
        return None
    x, why, k = r
    labs = {"natural": "número natural", "inteiro": "inteiro negativo (não natural)", "racional": "racional não inteiro", "irracional": "irracional"}
    return M("Qual é a melhor classificação do número <b>%s</b>?" % x, labs[k], [v for kk, v in labs.items() if kk != k], "%s é %s. Resposta: <b>%s</b>." % (x, why, labs[k]))


def s1_quem():
    k = R.choice(["irr", "rac"])
    pool_irr = ["√2", "√3", "√5", "π", "√7", "0,1010010001…", "√10"]
    pool_rac = ["√9", "0,5", "−3", "<span class='fr'><span class='fn'>2</span><span class='fd'>7</span></span>", "0,777…", "√25", "1,25", "√49"]
    if k == "irr":
        ok = R.choice(pool_irr)
        w = R.sample(pool_rac, 3)
        lst = sorted([ok] + w)
        return M("Entre %s, qual número é <b>irracional</b>?" % ", ".join(lst), ok, w, "%s tem infinitas casas decimais sem repetir um período: é <b>irracional</b>." % ok)
    ok = R.choice(pool_rac)
    w = R.sample(pool_irr, 3)
    lst = sorted([ok] + w)
    return M("Entre %s, qual número é <b>racional</b>?" % ", ".join(lst), ok, w, "%s pode ser escrito como fração de inteiros: é <b>racional</b>." % ok)


def s2_entre():
    n = R.randint(2, 150)
    r = math.isqrt(n)
    if r * r == n:
        return None
    return M("Entre quais inteiros consecutivos está √%d?" % n, "%d e %d" % (r, r + 1), ["%d e %d" % (r - 1, r) if r > 1 else "%d e %d" % (r + 1, r + 2), "%d e %d" % (r + 1, r + 2), "%d e %d" % (n // 2, n // 2 + 1)],
             "%d² = %d e %d² = %d; %d está entre eles. Então √%d está entre <b>%d e %d</b>." % (r, r * r, r + 1, (r + 1) ** 2, n, n, r, r + 1))


def s2_aprox():
    n = R.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24])
    v = math.sqrt(n)
    ans = d(F(round(v, 1)).limit_denominator(10), 1, keep=True)
    return M("Qual é o valor aproximado de √%d com uma casa decimal?" % n, ans, [d(F(round(v, 1)).limit_denominator(10) + F(1, 10), 1, keep=True), d(F(round(v, 1)).limit_denominator(10) - F(1, 10), 1, keep=True), d(F(n, 2), 1, keep=True)],
             "%s² = %s, o mais perto de %d. Resposta: <b>%s</b>." % (ans, d(F(round(v, 1)).limit_denominator(10) ** 2), n, ans))


def s3_reta():
    n = R.choice([2, 3, 5, 7, 8, 10, 11, 12, 13, 15])
    v = math.sqrt(n)
    lo = 0
    marks = {"A": None, "B": None, "C": None, "D": None}
    vals = sorted(R.sample([x / 2 for x in range(1, 9)], 3) + [v])
    labs = "ABCD"
    i = vals.index(v)
    pic = reta(0, 4, 1, [(x, l) for x, l in zip(vals, labs)], [0, 1, 2, 3, 4], width=440)
    others = [l for l in labs if l != labs[i]]
    return M(pic + "Qual letra marca melhor o número √%d (≈ %s)?" % (n, d(F(round(v, 2)).limit_denominator(100), 2)), labs[i], others,
             "√%d ≈ %s fica entre %d e %d: <b>%s</b>." % (n, d(F(round(v, 2)).limit_denominator(100), 2), int(v), int(v) + 1, labs[i]))


def s4_dizima():
    a, b = R.randint(1, 8), R.choice([3, 9, 11, 6])
    if math.gcd(a, b) != 1 or a >= b:
        return None
    x = F(a, b)
    s = str(a * 10 ** 6 // b).rjust(6, "0")
    dz = "0," + s[:4] + "…"
    k = R.choice(["fr", "tipo"])
    if k == "fr":
        return M("Que fração gera a dízima %s?" % dz, fq(x), [fq(F(a + 1, b)), fq(F(int(s[:2]), 100)), fq(F(a, b + 1))],
                 "%s ÷ %d = %s Resposta: <b>%s</b>." % (a, b, dz, fq(x)))
    return M("A dízima periódica %s é um número…" % dz, "racional", ["irracional", "natural", "inteiro"], "Toda dízima periódica vem de uma fração (%s): é <b>racional</b>." % fq(x))


CONCEITO = [("A diagonal de um quadrado de lado 1 mede…", "√2, um número irracional", ["1,5 exatamente", "2", "um número natural"]),
            ("O número π é a razão entre…", "o comprimento da circunferência e o diâmetro", ["o raio e o diâmetro", "a área e o raio", "o diâmetro e a área"]),
            ("π = 3,14 é…", "um valor aproximado, porque π é irracional", ["o valor exato de π", "uma fração exata", "um número natural"]),
            ("Todo número natural também é…", "inteiro, racional e real", ["irracional", "negativo", "só natural"]),
            ("O conjunto dos números reais é formado pelos…", "racionais e irracionais", ["naturais e negativos", "só pelas frações", "inteiros e naturais"]),
            ("Dois segmentos são incomensuráveis quando…", "não existe uma unidade que caiba um número inteiro de vezes nos dois", ["têm o mesmo tamanho", "um é o dobro do outro", "são perpendiculares"]),
            ("A soma de um racional com um irracional (por exemplo 2 + √3) é…", "irracional", ["racional", "inteira", "natural"]),
            ("√2 · √2 é igual a…", "2, um número racional", ["√4 irracional", "2√2", "4"])]


def s5_conceito():
    q, a, w = R.choice(CONCEITO)
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    from br_common import mix
    seen = set()
    sets = [
        ("Classificar números", mix(R, seen, [(s1_classificar, 14), (s1_quem, 6)])),
        ("Raízes entre inteiros", mix(R, seen, [(s2_entre, 12), (s2_aprox, 8)])),
        ("Irracionais na reta", mix(R, seen, [(s3_reta, 14), (s2_aprox, 6)])),
        ("Dízimas periódicas", mix(R, seen, [(s4_dizima, 14), (s1_quem, 6)])),
        ("Números reais", mix(R, seen, [(s5_conceito, 7), (s1_classificar, 7), (s2_entre, 6)])),
    ]
    body = lesson(
        ["Os números <b>racionais</b> podem ser escritos como fração de inteiros: decimais exatos e dízimas periódicas (0,333… = 1/3).",
         "Os <b>irracionais</b> têm infinitas casas decimais sem período: √2, √3, π.",
         "√n só é racional quando n é um quadrado perfeito: √49 = 7, mas √50 é irracional.",
         "Para localizar √n, procure os quadrados vizinhos: 7² = 49 &lt; 50 &lt; 64 = 8², então 7 &lt; √50 &lt; 8."],
        [("√30", ["5² = 25", "6² = 36"], "entre 5 e 6"),
         ("0,454545…", ["é periódica"], "racional (5/11)")],
        [["Achar que toda raiz é irracional", "√16 = 4 é natural."],
         ["Achar que dízima periódica é irracional", "Periódica vem de fração: é racional."],
         ["Achar que π = 3,14", "3,14 é só uma aproximação."]],
        reta(0, 4, 1, [(math.sqrt(2), "√2"), (math.sqrt(10), "√10")], [0, 1, 2, 3, 4], width=440))
    faq = [("O que é um número irracional?", "É um número real que não pode ser escrito como fração de inteiros. Sua representação decimal é infinita e não periódica, como √2 = 1,41421356… e π."),
           ("Como saber entre quais inteiros fica uma raiz?", "Procure os quadrados perfeitos mais próximos: √40 fica entre 6 e 7, porque 36 &lt; 40 &lt; 49.")]
    unit(R, "numeros-reais", "N", ["EF09MA01", "EF09MA02"],
         "Reconhecer que, uma vez fixada uma unidade de comprimento, existem segmentos de reta cujo comprimento não é expresso por número racional (como as medidas de diagonais de um polígono e alturas de um triângulo, quando se toma a medida de cada lado como unidade); reconhecer um número irracional como um número real cuja representação decimal é infinita e não periódica, e estimar a localização de alguns deles na reta numérica",
         "Números reais: racionais e irracionais", "Números reais",
         "Atividades de matemática para o 9º ano sobre números reais: naturais, inteiros, racionais e irracionais, dízimas periódicas, raízes entre inteiros e irracionais na reta numérica. 100 exercícios com gabarito.",
         "Irracional: decimal infinito e não periódico.", "√n é racional só se n for quadrado perfeito.",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
