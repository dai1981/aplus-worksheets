# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Números decimais (Números, EF06MA01, EF06MA08)
  python3 tools/gen_br_matematica_6_numeros_decimais.py
Décimos, centésimos e milésimos; ler e escrever decimais; fração decimal ↔ número decimal; frações com denominador 2, 4, 5, 20, 25
para decimal; porcentagem como centésimos; comparar e ordenar decimais; reta numérica.
Erros: achar que 0,25 &gt; 0,3 porque 25 &gt; 3, escrever 3/100 como 0,3, ler 2,05 como «dois e cinco décimos».
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, fq, bank, unit

R = random.Random(86007)
NOM = {1: "décimos", 2: "centésimos", 3: "milésimos"}


def fr(n, dd):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (d(n), d(dd))


def rdec(p):
    return F(R.randint(1, 10 ** p * R.choice([1, 1, 10, 30]) - 1), 10 ** p)


def s1_ler():
    p = R.choice([1, 2, 3])
    x = rdec(p)
    if (x * 10 ** (p - 1)).denominator == 1:
        return None
    ip = int(x)
    fp = int((x - ip) * 10 ** p)
    w = ("%d inteiro%s e " % (ip, "" if ip == 1 else "s") if ip else "") + "%d %s" % (fp, NOM[p][:-1] if fp == 1 else NOM[p])
    if R.random() < 0.5:
        return M("Como se escreve «%s» com algarismos?" % w, d(x), [d(x * 10) if (x * 10).denominator != 1 else d(x / 10, 4), d(x / 10, 4), d(ip + F(fp, 10 ** (p + 1)) if p < 3 else ip + F(fp, 100))],
                 "%s = <b>%s</b>." % (w, d(x)))
    return M("Como se lê %s?" % d(x), w, [("%d inteiro%s e " % (ip, "" if ip == 1 else "s") if ip else "") + "%d %s" % (fp, NOM[p % 3 + 1]), ("%d inteiro%s e " % (ip, "" if ip == 1 else "s") if ip else "") + "%d %s" % (fp, NOM[(p + 1) % 3 + 1]), "%d %s" % (int(x * 10 ** p), NOM[p]) if ip else "%d inteiros" % fp],
             "Três casas: milésimos; duas: centésimos; uma: décimos. <b>%s</b>." % w)


def s2_fracao():
    k = R.choice(["fd", "df", "outro"])
    if k == "fd":
        p = R.choice([1, 2, 3])
        n = R.randint(1, 10 ** p * 3)
        if n % 10 == 0:
            return None
        x = F(n, 10 ** p)
        return M("Escreva %s como número decimal." % fr(n, 10 ** p), d(x), [d(x * 10), d(x / 10, 4), d(F(n, 10 ** max(1, p - 1)))],
                 "Divida por %s: o número fica com %d casa%s decimal%s: <b>%s</b>." % (d(10 ** p), p, "" if p == 1 else "s", "" if p == 1 else "is", d(x)))
    if k == "df":
        p = R.choice([1, 2, 3])
        n = R.randint(1, 10 ** p - 1)
        if n % 10 == 0:
            return None
        x = F(n, 10 ** p)
        return M("Qual fração decimal é igual a %s?" % d(x), fr(n, 10 ** p), [fr(n, 10 ** (p % 3 + 1)), fr(n, 10 ** ((p + 1) % 3 + 1)), fr(10 ** p, n) if n > 1 else fr(1, 10)],
                 "%s tem %d casa%s decimal%s: <b>%d/%s</b>." % (d(x), p, "" if p == 1 else "s", "" if p == 1 else "is", n, d(10 ** p)))
    f = R.choice([F(1, 2), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5), F(4, 5), F(1, 20), F(3, 20), F(7, 20), F(1, 25), F(6, 25), F(1, 8), F(3, 8), F(7, 4), F(9, 5)])
    return M("Qual número decimal é igual a %s?" % fq(f), d(f), [d(F(f.numerator, 10)) if f.numerator < 10 else d(f + 1), "%d,%d" % (f.numerator, f.denominator), d(f / 10, 4)],
             "%d ÷ %d = <b>%s</b> (ou multiplique para ter denominador 10, 100 ou 1.000)." % (f.numerator, f.denominator, d(f)))


def s3_comparar():
    a = F(R.randint(1, 9), 10) + R.randint(0, 5)
    xs = sorted({a, a + F(R.randint(1, 9), 100) - F(R.randint(0, 1), 10), int(a) + F(R.randint(10, 99), 100), int(a) + F(R.randint(1, 9), 1000) + F(R.randint(0, 9), 10)})
    xs = [x for x in xs if x > 0]
    if len(xs) < 4:
        return None
    sh = xs[:]
    R.shuffle(sh)
    k = R.choice(["maior", "menor", "ordem"])
    if k == "ordem":
        ok = " &lt; ".join(d(x) for x in xs)
        return M("Qual é a ordem crescente de %s?" % "; ".join(d(x) for x in sh), ok, [" &lt; ".join(d(x) for x in xs[::-1]), " &lt; ".join(d(x) for x in sorted(xs, key=lambda t: len(d(t)))), " &lt; ".join(d(x) for x in [xs[1], xs[0], xs[3], xs[2]])],
                 "Compare casa por casa (iguale as casas com zeros): <b>%s</b>." % ok)
    t = xs[-1] if k == "maior" else xs[0]
    return M("Qual é o %s número: %s?" % (k, "; ".join(d(x) for x in sh)), d(t), [d(x) for x in xs if x != t],
             "Compare a parte inteira; depois décimos, centésimos e milésimos: <b>%s</b>." % d(t))


def s4_reta():
    st = R.choice([F(1, 10), F(1, 100), F(5, 100)])
    lo = R.randint(0, 5) + (R.randint(0, 9) * F(1, 10) if st != F(1, 10) else 0)
    k = R.randint(1, 9)
    x = lo + k * st
    return M("Na reta numérica, entre %s e %s há 10 espaços iguais. Que número está no %dº tracinho depois de %s?" % (d(lo), d(lo + 10 * st), k, d(lo)), d(x),
             [d(lo + k * st * 10), d(lo + k * st / 10, 4), d(x + st)], "Cada espaço vale %s; %s + %d × %s = <b>%s</b>." % (d(st), d(lo), k, d(st), d(x)))


s5_conceitos = bank(R, [
    ("Quantos centésimos há em 1 décimo?", "10", ["100", "1", "1.000"]),
    ("Quantos milésimos há em 1 inteiro?", "1.000", ["100", "10", "10.000"]),
    ("0,5 e 0,50 são…", "iguais", ["diferentes: 0,50 é maior", "diferentes: 0,5 é maior", "impossíveis de comparar"]),
    ("Qual número é maior: 0,3 ou 0,25?", "0,3", ["0,25", "são iguais", "depende"]),
    ("Em 4,072, o algarismo 7 está na casa dos…", "centésimos", ["décimos", "milésimos", "inteiros"]),
    ("3/100 escrito como decimal é…", "0,03", ["0,3", "3,00", "0,003"]),
    ("25% escrito como decimal é…", "0,25", ["2,5", "0,025", "25,0"]),
    ("Qual decimal está entre 1,4 e 1,5?", "1,45", ["1,54", "1,04", "1,6"]),
    ("Um número com 3 casas decimais termina na ordem dos…", "milésimos", ["centésimos", "décimos", "milhares"]),
    ("R$ 2,05 é igual a…", "2 reais e 5 centavos", ["2 reais e 50 centavos", "205 reais", "20 reais e 5 centavos"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Ler e escrever decimais", mix(R, seen, [(s1_ler, 20)])),
        ("Frações e decimais", mix(R, seen, [(s2_fracao, 20)])),
        ("Comparar e ordenar", mix(R, seen, [(s3_comparar, 20)])),
        ("Reta numérica", mix(R, seen, [(s4_reta, 14), (s5_conceitos, 6)])),
        ("Revisão", mix(R, seen, [(s5_conceitos, 4), (s2_fracao, 8), (s3_comparar, 8)])),
    ]
    body = lesson(
        ["Depois da vírgula vêm os <b>décimos</b> (1/10), os <b>centésimos</b> (1/100) e os <b>milésimos</b> (1/1.000).",
         "Uma fração decimal vira número decimal pelo número de zeros do denominador: 37/100 = 0,37; 5/1.000 = 0,005.",
         "Outras frações: divida o numerador pelo denominador, ou procure um denominador 10, 100 ou 1.000: 3/4 = 75/100 = 0,75.",
         "Para comparar, iguale o número de casas com zeros: 0,3 = 0,30 &gt; 0,25."],
        [("2,047", ["2 inteiros", "47 milésimos"], "dois inteiros e quarenta e sete milésimos"),
         ("3/5", ["3/5 = 6/10"], "0,6")],
        [["Achar que 0,25 &gt; 0,3", "Compare 0,30 e 0,25."],
         ["Escrever 3/100 como 0,3", "Duas casas para centésimos: 0,03."],
         ["Ler 2,05 como «dois e cinco décimos»", "São cinco centésimos."]])
    faq = [("Como transformar uma fração em número decimal?", "Divida o numerador pelo denominador. Se o denominador for 10, 100 ou 1.000, basta escrever o numerador com uma, duas ou três casas decimais."),
           ("O que a BNCC pede no 6º ano?", "Ler, escrever, comparar e ordenar números racionais na forma decimal (EF06MA01) e reconhecer que os números racionais positivos podem ser expressos nas formas fracionária e decimal, associando-os a pontos da reta numérica (EF06MA08).")]
    unit(R, "numeros-decimais", "N", ["EF06MA01", "EF06MA08"],
         "Reconhecer que os números racionais positivos podem ser expressos nas formas fracionária e decimal, estabelecer relações entre essas representações, passando de uma representação para outra, e relacioná-los a pontos na reta numérica; comparar, ordenar, ler e escrever números racionais cuja representação decimal é finita",
         "Números decimais: frações decimais, comparação e reta", "Números decimais",
         "Atividades de matemática para o 6º ano sobre números decimais: décimos, centésimos e milésimos, leitura e escrita, frações e decimais, comparação, ordem e reta numérica. 100 exercícios com gabarito.",
         "Décimos, centésimos, milésimos.", "Para comparar, iguale as casas decimais.",
         body, faq, sets, 7, grade="6-ano")


if __name__ == "__main__":
    main()
