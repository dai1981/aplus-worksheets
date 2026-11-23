# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Compor e decompor números (Números, EF02MA04)
  python3 tools/gen_br_matematica_2_compor_e_decompor_numeros.py
Decompor em centenas, dezenas e unidades (300 + 40 + 5); compor a partir de parcelas fora de ordem;
outras decomposições (2 centenas e 14 dezenas); material dourado e cédulas; parcela que falta.
Erros: juntar algarismos em vez de somar (300 + 5 → 3005), esquecer o zero, achar que só existe uma decomposição.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, reais, dinheiro_svg, pl
from br_2 import parts, wrong, md, cdu

R = random.Random(80203)


def three(zero=False):
    n = R.randint(101, 999)
    if zero and R.random() < 0.4:
        n = n // 100 * 100 + (n % 10 if R.random() < 0.5 else n // 10 % 10 * 10)
    return n


def soma(n):
    c, d, u = parts(n)
    return " + ".join(num(t) for t in (100 * c, 10 * d, u) if t)


def s1_decompor():
    n = three(True)
    c, d, u = parts(n)
    sh = soma(n)
    w1 = " + ".join(num(t) for t in (100 * c, d, u) if t)
    w2 = " + ".join(num(t) for t in (10 * c, 10 * d, u) if t)
    w3 = " + ".join(num(t) for t in (100 * c, u * 10, d) if t)
    w4 = " + ".join(num(t) for t in (100 * c, 10 * d + 10, u) if t)
    return mcq("Qual é a decomposição de %s?" % num(n), sh, [w1, w2, w3, w4], "%s = %s: <b>%s</b>." % (num(n), cdu(c, d, u), sh))


def s1_compor():
    n = three(True)
    sh = soma(n)
    if "+" not in sh:
        return None
    return mcq("Quanto é %s?" % sh, num(n), wrong(n), "Cada parcela vai para a sua ordem: <b>%s</b>." % num(n))


def s2_fora_de_ordem():
    n = three()
    c, d, u = parts(n)
    if not (d and u):
        return None
    ts = [100 * c, 10 * d, u]
    R.shuffle(ts)
    if ts == [100 * c, 10 * d, u]:
        ts = ts[::-1]
    sh = " + ".join(num(t) for t in ts)
    bad = int("".join(str(t) for t in ts)) if int("".join(str(t) for t in ts)) < 1000 else None
    return mcq("Quanto é %s?" % sh, num(n), [num(x) for x in (bad, u * 100 + d * 10 + c, d * 100 + c * 10 + u) if x and x != n] + wrong(n),
               "A ordem das parcelas não muda o total. Centenas: %d, dezenas: %d, unidades: %d. Total: <b>%s</b>." % (c, d, u, num(n)))


def s2_falta():
    n = three()
    c, d, u = parts(n)
    if not (d and u):
        return None
    k = R.choice(["c", "d", "u"])
    terms = {"c": 100 * c, "d": 10 * d, "u": u}
    shown = " + ".join("___" if x == k else num(terms[x]) for x in "cdu")
    ans = terms[k]
    return mcq("Complete: %s = %s" % (num(n), shown), num(ans), [str(x) for x in ({"c": c, "d": d, "u": u}[k], ans * 10 if ans * 10 < 1000 else ans + 1, ans // 10 if ans >= 10 else ans + 10, ans + 1) if x != ans],
               "%s = %s. Falta <b>%s</b>." % (num(n), soma(n), num(ans)))


def s3_outras():
    """outras decomposições: trocar 1 centena por 10 dezenas, 1 dezena por 10 unidades"""
    n = three()
    c, d, u = parts(n)
    if c < 2:
        return None
    k = R.choice(["cd", "du", "ad"])
    if k == "cd":
        txt = "%s e %s" % (pl(c - 1, "centena", "centenas"), pl(d + 10, "dezena", "dezenas")) + (" e %s" % pl(u, "unidade", "unidades") if u else "")
        why = "1 centena = 10 dezenas"
    elif k == "du":
        if not d:
            return None
        txt = "%s, %s e %s" % (pl(c, "centena", "centenas"), pl(d - 1, "dezena", "dezenas"), pl(u + 10, "unidade", "unidades"))
        why = "1 dezena = 10 unidades"
    else:
        txt = "%s e %s" % (pl(c, "centena", "centenas"), pl(10 * d + u, "unidade", "unidades"))
        if 10 * d + u < 10:
            return None
        why = "%d dezenas e %d unidades = %d unidades" % (d, u, 10 * d + u)
    w = [num(c * 100 + (d + 10) * 10 + u)] if k == "cd" else []
    return mcq("Que número tem %s?" % txt, num(n), w + wrong(n), "%s. O número é <b>%s</b>." % (why, num(n)))


def s3_qual_igual():
    n = three()
    c, d, u = parts(n)
    if c < 2 or not d:
        return None
    ok = R.choice(["%d + %d" % (100 * c, 10 * d + u), "%d + %d" % (100 * (c - 1), 100 + 10 * d + u), "%d + %d" % (100 * c + 10 * d, u) if u else "%d + %d + %d" % (100 * (c - 1), 100, 10 * d)])
    bad = ["%d + %d" % (100 * c, 10 * d + u + 10), "%d + %d" % (10 * c, 10 * d + u), "%d + %d" % (100 * c + 10 * (d - 1), u + 1) if u < 9 else "%d + %d" % (100 * (c + 1), 10 * d + u),
           "%d + %d" % (100 * (c - 1), 10 * d + u)]
    return mcq("Qual adição tem resultado %s?" % num(n), ok, bad, "%s = %s, que também se pode escrever <b>%s</b>." % (num(n), soma(n), ok))


def s4_material():
    c, d, u = R.randint(1, 4), R.randint(0, 6), R.randint(0, 9)
    n = 100 * c + 10 * d + u
    if R.random() < 0.5:
        return mcq(md(c, d, u) + "Qual decomposição mostra o material dourado?", soma(n), [" + ".join(num(t) for t in (10 * c, 10 * d, u) if t), " + ".join(num(t) for t in (c, d, u) if t) or "0",
                   " + ".join(num(t) for t in (100 * c, d, u) if t), " + ".join(num(t) for t in (100 * c, 10 * d + 10, u) if t)],
                   "%s: <b>%s</b>." % (cdu(c, d, u), soma(n)))
    return mcq(md(c, d, u) + "Que número o material dourado forma?", num(n), wrong(n), "%s = <b>%s</b>." % (soma(n), num(n)))


def s4_dinheiro():
    c, d, u = R.randint(1, 3), R.randint(1, 5), R.randint(1, 5)
    tot = 100 * c + 10 * d + u
    items = [10000] * c + [1000] * d + [100] * u
    pic = dinheiro_svg(items)
    return mcq(pic + "Quantos reais há?", reais(tot * 100), [reais((c + d + u) * 100), reais((10 * c + 10 * d + u) * 100), reais((100 * c + d + 10 * u) * 100)],
               "%s + %s + %s = <b>%s</b>." % (reais(c * 10000), reais(d * 1000), reais(u * 100), reais(tot * 100)))


def s5_problema():
    k = R.choice(["pacotes", "cedulas", "palitos", "lapis"])
    if k == "pacotes":
        c, d, u = R.randint(1, 6), R.randint(1, 9), R.randint(1, 9)
        n = 100 * c + 10 * d + u
        return mcq("Uma loja tem %s de 100 balas, %s de 10 balas e %s. Quantas balas há?" % (pl(c, "caixa", "caixas"), pl(d, "pacote", "pacotes"), pl(u, "bala solta", "balas soltas")),
                   num(n), [str(c + d + u), num(10 * c + 10 * d + u), num(100 * c + d + u)], "%s = <b>%s</b>." % (soma(n), num(n)))
    if k == "cedulas":
        a = R.choice([100, 10])
        n = R.randint(2, 9) * 100 if a == 100 else R.randint(12, 99) * 10
        ans = n // a
        return mcq("%s quer pagar %s só com cédulas de R$ %d. Quantas cédulas ela usa?" % (R.choice(["Ana", "Bia", "Lia", "Rita"]), reais(n * 100), a), str(ans),
                   [str(n // 100 if a == 10 else n // 10), str(ans + 1), str(n)], "%s = %d × %d: <b>%d cédulas</b>." % (num(n), ans, a, ans))
    if k == "palitos":
        d, u = R.randint(12, 35), R.randint(1, 9)
        n = 10 * d + u
        return mcq("Lia fez %d montinhos de 10 palitos e sobraram %s. Quantos palitos ela tem?" % (d, pl(u, "palito", "palitos")), num(n), [str(d + u), num(n + 10), num(d * 100 + u)],
                   "%d × 10 = %d; %d + %d = <b>%s</b>." % (d, 10 * d, 10 * d, u, num(n)))
    n = three()
    c, d, u = parts(n)
    if not (d and u):
        return None
    return mcq("Paulo tem %s lápis. Ele enche o maior número possível de caixas de 100 e depois de pacotes de 10. Quantos lápis ficam soltos?" % num(n), str(u),
               [str(d), str(c), str(10 * d + u)], "%s = %s: ficam <b>%d</b> soltos." % (num(n), soma(n), u))


def main():
    seen = set()
    sets = [
        ("Decompor em centenas, dezenas e unidades", mix(R, seen, [(s1_decompor, 12), (s1_compor, 8)])),
        ("Compor e completar", mix(R, seen, [(s2_fora_de_ordem, 10), (s2_falta, 10)])),
        ("Outras formas de decompor", mix(R, seen, [(s3_outras, 12), (s3_qual_igual, 8)])),
        ("Material dourado e dinheiro", mix(R, seen, [(s4_material, 12), (s4_dinheiro, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["<b>Decompor</b> é separar o número em partes: 345 = 300 + 40 + 5.",
         "<b>Compor</b> é juntar as partes: 600 + 20 + 7 = 627.",
         "Um número tem muitas decomposições: 345 = 300 + 45 = 200 + 145.",
         "1 centena = 10 dezenas e 1 dezena = 10 unidades. Por isso 2 centenas e 14 dezenas = 340."],
        [("Decompor 508", ["5 centenas, 0 dezena, 8 unidades"], "500 + 8"),
         ("1 centena e 23 dezenas", ["100 + 230"], "330")],
        [["Escrever 3005 para 300 + 5", "Some: 300 + 5 = 305."],
         ["Esquecer o zero: 400 + 6 = 46", "Não há dezenas: escreva 0. 406."],
         ["Achar que só existe uma decomposição", "345 = 300 + 45 também está certo."]],
        md(3, 4, 5))
    faq = [("O que é decompor um número?", "É escrever o número como uma soma de partes, por exemplo 345 = 300 + 40 + 5. A BNCC pede que o 2º ano faça isso com material manipulável e com diferentes adições."),
           ("Como praticar em casa?", "Use dinheiro de brinquedo: monte R$ 236 com cédulas de R$ 100 e R$ 10 e moedas de R$ 1, e depois monte o mesmo valor de outro jeito.")]
    make_unit(R, "compor-e-decompor-numeros", "N", ["EF02MA04"],
              "Compor e decompor números naturais de até três ordens, com suporte de material manipulável, por meio de diferentes adições",
              "Compor e decompor números até 1.000", "Compor e decompor",
              "Atividades de matemática para o 2º ano sobre compor e decompor números até 1.000: centenas, dezenas e unidades, diferentes adições, material dourado e dinheiro. 100 exercícios com gabarito.",
              "345 = 300 + 40 + 5.", "1 centena = 10 dezenas.",
              body, faq, sets, 3, grade="2-ano")


if __name__ == "__main__":
    main()
