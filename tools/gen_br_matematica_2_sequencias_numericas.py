# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Sequências numéricas (Álgebra, EF02MA09, EF02MA11)
  python3 tools/gen_br_matematica_2_sequencias_numericas.py
Sequências crescentes e decrescentes a partir de um número qualquer (de 2 em 2, de 5 em 5, de 10 em 10, de 100 em 100);
descobrir a regra; números que faltam; número que não segue a regra; sequências de figuras.
Usa geradores do 3º ano (sequências) com outro sorteio.
Erros: aplicar a regra só uma vez, esquecer que a sequência decrescente diminui, contar a partir do número errado.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, use, lim, reta

R = random.Random(80210)
M3 = "gen_br_matematica_3_sequencias_numericas"
q_prox, q_regra, q_falta, q_errado, q_fig = use(M3, 80905, "s1_proximo", "s1_regra", "s2_falta", "s2_errado", "s4_figuras", preds=(lim(999, 0),))


def seq(start=None):
    d = R.choice([2, 3, 5, 10, 100])
    up = R.random() < 0.6
    n = 5
    if start is None:
        start = R.randint(2, 60) if d < 10 else R.randint(10, 300) if d == 10 else R.randint(1, 4) * 100 + R.randint(0, 99)
    if not up:
        start += d * (n + 1)
    xs = [start + (d if up else -d) * i for i in range(n + 1)]
    if min(xs) < 0 or max(xs) > 999:
        return None
    return d, up, xs


def s1_proximo():
    r = seq()
    if not r:
        return None
    d, up, xs = r
    return mcq("Qual é o próximo número? %s, ___" % ", ".join(num(x) for x in xs[:5]), num(xs[5]), [num(xs[4] + (-d if up else d)), num(xs[5] + (d if up else -d)), num(xs[4] + (1 if up else -1))],
               "A regra é %s %d: %s %s %d = <b>%s</b>." % ("somar" if up else "tirar", d, num(xs[4]), "+" if up else "−", d, num(xs[5])))


def s1_regra():
    r = seq()
    if not r:
        return None
    d, up, xs = r
    ans = "%s %d" % ("somar" if up else "tirar", d)
    return mcq("Qual é a regra da sequência %s?" % ", ".join(num(x) for x in xs[:5]), ans, ["%s %d" % ("tirar" if up else "somar", d), "%s %d" % ("somar" if up else "tirar", d * 2 if d < 100 else 10), "%s 1" % ("somar" if up else "tirar")],
               "De um número para o seguinte %s %d. Regra: <b>%s</b>." % ("aumenta" if up else "diminui", d, ans))


def s2_falta():
    r = seq()
    if not r:
        return None
    d, up, xs = r
    i = R.randint(1, 4)
    shown = ["___" if j == i else num(x) for j, x in enumerate(xs)]
    return mcq("Que número falta? %s" % ", ".join(shown), num(xs[i]), [num(xs[i] + 1), num(xs[i] + (d if up else -d)), num(xs[i - 1] - (d if up else -d))],
               "%s %d a cada passo: <b>%s</b>." % ("Some" if up else "Tire", d, num(xs[i])))


def s2_comecar():
    d = R.choice([2, 5, 10, 100])
    a = R.randint(3, 80) if d < 100 else R.randint(1, 4) * 100 + R.randint(1, 99)
    up = R.random() < 0.6
    if not up:
        a += 4 * d
    xs = [a + (d if up else -d) * i for i in range(4)]
    if min(xs) < 0 or max(xs) > 999:
        return None
    ok = ", ".join(num(x) for x in xs)
    w1 = ", ".join(num(a + (-d if up else d) * i) for i in range(4))
    w2 = ", ".join(num(a + (d + 1 if up else -d - 1) * i) for i in range(4))
    w3 = ", ".join(num(x) for x in [a] + [a + (d if up else -d) * i + (1 if up else -1) for i in range(1, 4)])
    return mcq("Comece em %s e %s de %d em %d. Qual sequência está certa?" % (num(a), "conte" if up else "volte", d, d), ok, [w1, w2, w3],
               "%s %d cada vez: <b>%s</b>." % ("Some" if up else "Tire", d, ok))


def s3_reta():
    d = R.choice([2, 5, 10])
    lo = R.randint(0, 8) * 10
    step = d
    hi = lo + 8 * step
    hops = [lo + step * i for i in range(1, 4)]
    nxt = lo + step * 4
    pic = reta(lo, hi, step, [(nxt, "?")], [lo] + hops, width=440)
    return mcq(pic + "A reta está marcada de %d em %d. Que número fica no ponto «?»" % (step, step), num(nxt), [num(nxt + step), num(hops[-1] + 1), num(nxt - 1)],
               "%s, %s: <b>%s</b>." % (num(lo), ", ".join(num(h) for h in hops), num(nxt)))


def s5_problema():
    k = R.choice(["cofre", "escada", "planta", "casas", "pulos"])
    if k == "cofre":
        a, d, w = R.choice([2, 5, 10]), R.choice([2, 5]), R.randint(4, 7)
        v = a + d * (w - 1)
        return mcq("Ana guardou %d reais na 1ª semana. A cada semana guarda %d reais a mais que na anterior. Quanto guarda na %dª semana?" % (a, d, w), "%d reais" % v,
                   ["%d reais" % (a + d * w), "%d reais" % (d * w), "%d reais" % (v - d)], "%s: <b>%d reais</b>." % (", ".join(str(a + d * i) for i in range(w)), v))
    if k == "escada":
        n = R.randint(4, 8)
        return mcq("Num prédio, cada andar tem 10 degraus. Quantos degraus sobe quem vai do térreo ao %dº andar?" % n, "%d degraus" % (10 * n), ["%d degraus" % (10 * n + 10), "%d degraus" % (n + 10), "%d degraus" % (10 * n - 10)],
                   "Conte de 10 em 10: %s = <b>%d degraus</b>." % (", ".join(str(10 * i) for i in range(1, n + 1)), 10 * n))
    if k == "planta":
        h, d, s = R.randint(2, 9), R.choice([2, 3]), R.randint(3, 6)
        return mcq("Um pé de feijão tem %d cm e cresce %d cm por dia. Quantos centímetros terá daqui a %d dias?" % (h, d, s), "%d cm" % (h + d * s), ["%d cm" % (d * s), "%d cm" % (h + d * s + d), "%d cm" % (h + d + s)],
                   "%s: <b>%d cm</b>." % (", ".join(str(h + d * i) for i in range(s + 1)), h + d * s))
    if k == "casas":
        a = R.randint(101, 151) // 2 * 2 + 1
        return mcq("Numa rua, as casas de um lado têm números ímpares: %d, %d, %d, %d… Qual é o número da próxima casa?" % (a, a + 2, a + 4, a + 6), str(a + 8), [str(a + 7), str(a + 10), str(a + 9)],
                   "De 2 em 2: %d + 2 = <b>%d</b>." % (a + 6, a + 8))
    s = R.randint(30, 60)
    d = R.choice([3, 5])
    n = R.randint(3, 6)
    return mcq("Um sapo está no número %d e pula para trás de %d em %d. Onde ele estará depois de %d pulos?" % (s, d, d, n), str(s - d * n), [str(s + d * n), str(s - d * (n - 1)), str(s - n)],
               "%s: <b>%d</b>." % (", ".join(str(s - d * i) for i in range(n + 1)), s - d * n))


def main():
    seen = set()
    sets = [
        ("Próximo número", mix(R, seen, [(s1_proximo, 12), (q_prox, 8)])),
        ("Descobrir a regra", mix(R, seen, [(s1_regra, 10), (q_regra, 4), (s2_comecar, 6)])),
        ("Números que faltam", mix(R, seen, [(s2_falta, 12), (q_falta, 4), (q_errado, 4)])),
        ("Sequências na reta e com figuras", mix(R, seen, [(s3_reta, 12), (q_fig, 8)])),
        ("Problemas com sequências", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Uma <b>sequência</b> segue uma regra, como «somar 5» ou «tirar 10».",
         "Na sequência <b>crescente</b> os números aumentam; na <b>decrescente</b>, diminuem.",
         "Para achar a regra, veja quanto muda de um número para o seguinte.",
         "Para achar um número que falta, use a regra a partir do número anterior."],
        [("35, 40, 45, 50, ___", ["regra: somar 5", "50 + 5"], "55"),
         ("700, 600, 500, ___", ["regra: tirar 100", "500 − 100"], "400")],
        [["Achar a regra só olhando o primeiro passo", "Confira a regra em todos os números."],
         ["Somar numa sequência decrescente", "Se diminui, tire."],
         ["Errar a passagem da dezena (95, 100, 115)", "Some com cuidado: 100 + 5 = 105."]],
        reta(0, 50, 5, [(25, "?")], [0, 5, 10, 15, 20], width=440))
    faq = [("O que são sequências no 2º ano?", "São listas de números que seguem uma regra, como contar de 5 em 5 a partir de 23. A BNCC pede construir sequências crescentes e decrescentes e descobrir os números que faltam."),
           ("Como praticar em casa?", "Conte de 2 em 2, de 5 em 5 ou de 10 em 10 a partir de qualquer número, para frente e para trás. Depois esconda um número e peça para a criança descobrir.")]
    make_unit(R, "sequencias-numericas", "A", ["EF02MA09", "EF02MA11"],
              "Construir sequências de números naturais em ordem crescente ou decrescente a partir de um número qualquer, utilizando uma regularidade estabelecida; descrever os elementos ausentes em sequências repetitivas e em sequências recursivas de números naturais, objetos ou figuras",
              "Sequências numéricas crescentes e decrescentes", "Sequências numéricas",
              "Atividades de matemática para o 2º ano sobre sequências numéricas: crescentes e decrescentes, de 2 em 2, de 5 em 5, de 10 em 10, regra da sequência e números que faltam. 100 exercícios com gabarito.",
              "Descubra a regra e use-a em cada passo.", "Crescente aumenta, decrescente diminui.",
              body, faq, sets, 10, grade="2-ano")


if __name__ == "__main__":
    main()
