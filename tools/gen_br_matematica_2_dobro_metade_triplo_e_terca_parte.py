# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Dobro, metade, triplo e terça parte (Números, EF02MA08)
  python3 tools/gen_br_matematica_2_dobro_metade_triplo_e_terca_parte.py
Dobro (2 vezes) e triplo (3 vezes) com figuras; metade e terça parte repartindo em 2 ou 3 grupos iguais;
desfazer (o dobro é 16: qual é o número?); comparar dobro e triplo; problemas do dia a dia.
Erros: confundir dobro com metade, somar 2 em vez de dobrar, repartir em grupos diferentes.
"""
import random
from br_common import mcq, lesson, make_unit, mix, grupos, coisas, COISAS, KINDS, Kids

R = random.Random(80209)
K = Kids(R)
NOME = {2: "dobro", 3: "triplo"}
PARTE = {2: "metade", 3: "terça parte"}


def qt(kind):
    return "Quantas" if COISAS[kind][2] == "f" else "Quantos"


def s1_dobro_fig():
    kind = R.choice(KINDS)
    k = R.choice([2, 3])
    n = R.randint(2, 6)
    pic = grupos(k, n, kind)
    return mcq(pic + "Num grupo há %s. Os %d grupos juntos mostram o %s de %d. %s são?" % (coisas(kind, n), k, NOME[k], n, qt(kind)), str(k * n),
               [str(n + k), str(n * (5 - k)), str(k * n + 1)], "O %s de %d é %s = <b>%d</b>." % (NOME[k], n, " + ".join([str(n)] * k), k * n))


def s1_dobro():
    k = R.choice([2, 2, 3])
    n = R.randint(3, 15) if k == 2 else R.randint(2, 10)
    return mcq("Qual é o %s de %d?" % (NOME[k], n), str(k * n), [str(n + k), str(n * (5 - k)), str(k * n + 1)],
               "%s de %d = %s = <b>%d</b>." % (NOME[k].capitalize(), n, " + ".join([str(n)] * k), k * n))


def s2_parte_fig():
    kind = R.choice(KINDS)
    k = R.choice([2, 3])
    q = R.randint(2, 6)
    n = k * q
    pic = grupos(k, q, kind)
    return mcq(pic + "%s foram repartid%ss em %d grupos iguais. Qual é a %s de %d?" % (coisas(kind, n).capitalize(), "a" if COISAS[kind][2] == "f" else "o", k, PARTE[k], n),
               str(q), [str(k), str(n), str(q + 1)], "Cada grupo é a %s: <b>%d</b>." % (PARTE[k], q))


def s2_parte():
    k = R.choice([2, 2, 3])
    q = R.randint(2, 15) if k == 2 else R.randint(2, 10)
    n = k * q
    return mcq("Qual é a %s de %d?" % (PARTE[k], n), str(q), [str(n * 2), str(n - k), str(q + 1)],
               "Reparta %d em %d grupos iguais: cada um fica com <b>%d</b>, porque %s = %d." % (n, k, q, " + ".join([str(q)] * k), n))


def s3_desfazer():
    k = R.choice([2, 3])
    n = R.randint(3, 12)
    if R.random() < 0.5:
        return mcq("Pensei num número. O %s dele é %d. Que número pensei?" % (NOME[k], k * n), str(n), [str(k * k * n) if k * k * n < 100 else str(n + k), str(k * n - k), str(n + 1)],
                   "%s = %d. O número é <b>%d</b>." % (" + ".join([str(n)] * k), k * n, n))
    return mcq("A %s de um número é %d. Que número é esse?" % (PARTE[k], n), str(k * n), [str(n + k), str(n * (5 - k)), str(k * n + 1)],
               "São %d partes iguais a %d: %s = <b>%d</b>." % (k, n, " + ".join([str(n)] * k), k * n))


def s3_comparar():
    n = R.randint(2, 9)
    k = R.choice(["dt", "dm", "td"])
    if k == "dt":
        return mcq("O dobro de %d e o triplo de %d: qual é maior e quanto a mais?" % (n, n), "o triplo, %d a mais" % n, ["o dobro, %d a mais" % n, "o triplo, %d a mais" % (3 * n), "são iguais"],
                   "Dobro = %d, triplo = %d. O triplo tem <b>%d a mais</b>." % (2 * n, 3 * n, n))
    if k == "dm":
        m = 2 * n
        return mcq("Qual é o dobro da metade de %d?" % m, str(m), [str(n), str(2 * m), str(m + 2)], "Metade de %d = %d; dobro de %d = <b>%d</b>. Volta ao número!" % (m, n, n, m))
    return mcq("Qual é a terça parte do triplo de %d?" % n, str(n), [str(3 * n), str(9 * n) if 9 * n < 100 else str(n + 3), str(n + 1)],
               "Triplo de %d = %d; terça parte de %d = <b>%d</b>." % (n, 3 * n, 3 * n, n))


def s4_quantos():
    """dobro/triplo como «2 vezes mais» em comparações de quantidades"""
    (a, ga), (b, gb) = K.two()
    k = R.choice([2, 3])
    n = R.randint(3, 15)
    what = R.choice(["figurinhas", "bolinhas", "pipas", "balas", "conchas"])
    if R.random() < 0.5:
        return mcq("%s tem %d %s. %s tem o %s. Quantas %s tem %s?" % (a, n, what, b, NOME[k], what, b), str(k * n), [str(n + k), str(n * (5 - k)), str(k * n + n)],
                   "%s de %d = <b>%d</b>." % (NOME[k].capitalize(), n, k * n))
    return mcq("%s tem %d %s. %s tem a %s disso. Quantas %s tem %s?" % (a, k * n, what, b, PARTE[k], what, b), str(n), [str(k * n * 2), str(k * n - k), str(n + 1)],
               "%s de %d = <b>%d</b>." % (PARTE[k].capitalize(), k * n, n))


CENAS = [("Uma pizza tem {n} pedaços. {p} comeu a metade. Quantos pedaços comeu?", 2, "pedaços", True),
         ("Uma fita tem {n} cm. Ela foi cortada em 3 partes iguais. Quantos centímetros tem cada parte?", 3, "cm", True),
         ("Um pacote tem {n} biscoitos. {p} dividiu igualmente com o irmão. Quantos biscoitos cada um ganhou?", 2, "biscoitos", True),
         ("Um vaso tem {n} flores. Outro vaso tem o dobro. Quantas flores tem o outro vaso?", 2, "flores", False),
         ("Uma caixa tem {n} lápis. {p} comprou o triplo. Quantos lápis comprou?", 3, "lápis", False),
         ("{p} tem {n} anos. O primo tem o dobro dessa idade. Quantos anos tem o primo?", 2, "anos", False),
         ("Três amigos dividiram {n} figurinhas em partes iguais. Quantas ficaram para cada um?", 3, "figurinhas", True),
         ("Num ônibus há {n} pessoas. Desceu a metade. Quantas pessoas desceram?", 2, "pessoas", True),
         ("Uma garrafa tem {n} copos de suco. Uma jarra tem o dobro. Quantos copos tem a jarra?", 2, "copos", False)]


def s5_problema():
    t, k, u, part = R.choice(CENAS)
    p, _ = K.next()
    if "anos" in t:
        n = R.randint(4, 9)
    else:
        n = R.randint(3, 15) * k if part else R.randint(3, 15 if k == 2 else 10)
    ans = n // k if part else n * k
    w = [n * k if part else n // k if n % k == 0 else n + k, n + k if not part else n - k, ans + 1, n * (5 - k) if not part else ans - 1]
    return mcq(t.format(n=n, p=p), "%d %s" % (ans, u), ["%d %s" % (x, u) for x in w if x != ans and x > 0],
               ("A %s de %d é <b>%d %s</b>." % (PARTE[k], n, ans, u)) if part else "O %s de %d é <b>%d %s</b>." % (NOME[k], n, ans, u))


def main():
    seen = set()
    sets = [
        ("Dobro e triplo", mix(R, seen, [(s1_dobro_fig, 8), (s1_dobro, 12)])),
        ("Metade e terça parte", mix(R, seen, [(s2_parte_fig, 8), (s2_parte, 12)])),
        ("Desfazer e comparar", mix(R, seen, [(s3_desfazer, 12), (s3_comparar, 8)])),
        ("Dobro, triplo, metade e terça parte", mix(R, seen, [(s4_quantos, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["<b>Dobro</b> é 2 vezes: o dobro de 6 é 6 + 6 = 12.",
         "<b>Triplo</b> é 3 vezes: o triplo de 4 é 4 + 4 + 4 = 12.",
         "<b>Metade</b> é repartir em 2 partes iguais: a metade de 12 é 6.",
         "<b>Terça parte</b> é repartir em 3 partes iguais: a terça parte de 12 é 4."],
        [("Dobro de 7", ["7 + 7"], "14"),
         ("Terça parte de 15", ["3 grupos iguais: 5 + 5 + 5 = 15"], "5")],
        [["Confundir dobro com metade", "Dobro aumenta; metade diminui."],
         ["Somar 2 em vez de dobrar (dobro de 8 = 10)", "Dobro de 8 = 8 + 8 = 16."],
         ["Repartir em grupos diferentes", "As partes precisam ser iguais."]],
        grupos(3, 4, "apple"))
    faq = [("O que o 2º ano aprende sobre dobro e metade?", "A BNCC pede problemas com dobro, metade, triplo e terça parte, com apoio de imagens ou material manipulável, antes da divisão formal do 3º ano."),
           ("Como praticar em casa?", "Reparta frutas, biscoitos ou balas: metade para cada um de dois irmãos, ou em 3 pratos iguais. Depois junte tudo para ver o dobro ou o triplo.")]
    make_unit(R, "dobro-metade-triplo-e-terca-parte", "N", ["EF02MA08"],
              "Resolver e elaborar problemas envolvendo dobro, metade, triplo e terça parte, com o suporte de imagens ou material manipulável, utilizando estratégias pessoais",
              "Dobro, metade, triplo e terça parte", "Dobro, metade, triplo",
              "Atividades de matemática para o 2º ano sobre dobro, metade, triplo e terça parte, com figuras, grupos iguais e problemas do dia a dia. 100 exercícios com gabarito.",
              "Dobro = 2 vezes; triplo = 3 vezes.", "Metade = 2 partes iguais; terça parte = 3 partes iguais.",
              body, faq, sets, 9, grade="2-ano")


if __name__ == "__main__":
    main()
