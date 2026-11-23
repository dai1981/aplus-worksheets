# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Probabilidade (Probabilidade e estatística, EF08MA22)
  python3 tools/gen_br_matematica_8_probabilidade.py
Espaço amostral com o princípio multiplicativo; a soma das probabilidades de todos os elementos do espaço amostral é 1;
evento complementar P(não A) = 1 − P(A); probabilidade em fração, decimal e porcentagem.
Usa geradores do 6º (urna, dado), 7º (dois dados) e 9º ano (espaço amostral) com outro sorteio.
Erros: somar as probabilidades e passar de 1, fazer 100 − P com P em fração, contar (1, 2) e (2, 1) como um só.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, fq, bank, unit

R = random.Random(88017)
p_urna, p_dado = use("gen_br_matematica_6_probabilidade", 88917, "s1_urna", "s2_dado")
p_dois = use("gen_br_matematica_7_probabilidade_e_frequencia", 88927, "s1_dois_dados")
p_esp = use("gen_br_matematica_9_probabilidade", 88937, "s1_espaco")
CORES = ["azuis", "vermelhas", "verdes", "amarelas", "brancas", "pretas"]
SG = {"azuis": "azul", "vermelhas": "vermelha", "verdes": "verde", "amarelas": "amarela", "brancas": "branca", "pretas": "preta"}


def pct(p):
    v = p * 100
    return ("%s%%" % d(v)) if (v * 10).denominator == 1 else None


def s1_complementar():
    k = R.choice(["frac", "pct", "dec", "urna"])
    if k == "frac":
        n = R.choice([5, 6, 8, 10, 12, 20])
        a = R.randint(1, n - 1)
        p = F(a, n)
        return M("A probabilidade de um evento A é %s. Qual é a probabilidade de A não acontecer?" % fq(p), fq(1 - p), [fq(p), fq(F(n - a, n * 2)) if n - a != a else fq(F(1, n)), "%d/%d" % (a, n - a) if F(a, n - a) != 1 - p else fq(F(a + 1, n))],
                 "P(não A) = 1 − %s = <b>%s</b>." % (fq(p), fq(1 - p)))
    if k == "pct":
        a = R.choice(range(5, 96, 5))
        return M("A previsão diz que a chance de chover amanhã é de %d%%. Qual é a chance de não chover?" % a, "%d%%" % (100 - a), ["%d%%" % a, "%d%%" % (100 - a + 10) if a > 10 else "%d%%" % (100 - a - 5), "%s" % d(F(100 - a, 100))],
                 "100%% − %d%% = <b>%d%%</b>." % (a, 100 - a))
    if k == "dec":
        a = R.randint(1, 19) * 5
        return M("Num sorteio, P(ganhar) = %s. Quanto vale P(não ganhar)?" % d(F(a, 100)), d(F(100 - a, 100)), [d(F(a, 100)), d(1 + F(a, 100)), d(F(100 - a, 10)) if 100 - a < 100 else "1"],
                 "1 − %s = <b>%s</b>." % (d(F(a, 100)), d(F(100 - a, 100))))
    c1, c2 = R.sample(CORES, 2)
    a, b = R.randint(2, 9), R.randint(2, 9)
    return M("Uma urna tem %d bolas %s e %d bolas %s. Qual é a probabilidade de <b>não</b> sortear uma bola %s?" % (a, c1, b, c2, SG[c1]), fq(F(b, a + b)), [fq(F(a, a + b)), "%d/%d" % (b, a), fq(F(1, 2)) if a != b else fq(F(1, a + b))],
             "Não %s = %s: %d em %d, <b>%s</b>." % (SG[c1], SG[c2], b, a + b, fq(F(b, a + b))))


def s2_soma1():
    k = R.choice(["falta", "roleta", "valido"])
    if k == "falta":
        n = R.choice([10, 12, 20])
        xs = sorted(R.sample(range(1, n), 2))
        a, b, c = xs[0], xs[1] - xs[0], n - xs[1]
        cs = R.sample(CORES, 3)
        return M("Numa urna só há bolas %s, %s e %s. P(%s) = %s e P(%s) = %s. Qual é P(%s)?" % (cs[0], cs[1], cs[2], SG[cs[0]], fq(F(a, n)), SG[cs[1]], fq(F(b, n)), SG[cs[2]]),
                 fq(F(c, n)), [fq(F(a + b, n)), fq(F(1, 3)) if F(c, n) != F(1, 3) else fq(F(1, 2)), fq(F(abs(a - b), n)) if a != b and F(abs(a - b), n) != F(c, n) else fq(F(c + 1, n))],
                 "A soma é 1: 1 − %s − %s = <b>%s</b>." % (fq(F(a, n)), fq(F(b, n)), fq(F(c, n))))
    if k == "roleta":
        a, b = R.choice([(25, 40), (30, 45), (20, 50), (15, 35), (10, 60), (35, 40)])
        return M("Numa roleta, P(azul) = %d%%, P(verde) = %d%% e o resto é amarelo. Qual é P(amarelo)?" % (a, b), "%d%%" % (100 - a - b), ["%d%%" % (a + b), "%d%%" % (100 - a), "%d%%" % (100 - b)],
                 "100%% − %d%% − %d%% = <b>%d%%</b>." % (a, b, 100 - a - b))
    ok = R.choice([True, False])
    if ok:
        ps = R.choice([(F(1, 2), F(1, 4), F(1, 4)), (F(1, 3), F(1, 3), F(1, 3)), (F(1, 5), F(2, 5), F(2, 5)), (F(1, 6), F(1, 3), F(1, 2))])
    else:
        ps = R.choice([(F(1, 2), F(1, 3), F(1, 4)), (F(1, 2), F(1, 2), F(1, 3)), (F(2, 5), F(2, 5), F(2, 5)), (F(1, 3), F(1, 4), F(1, 6))])
    s = sum(ps)
    return M("Um experimento tem só três resultados, com probabilidades %s, %s e %s. Essas probabilidades podem estar corretas?" % tuple(fq(p) for p in ps),
             "sim, a soma é 1" if ok else "não, a soma é %s" % fq(s), ["não, a soma é %s" % fq(s + F(1, 6)), "sim, a soma é %s" % fq(s + F(1, 12)) if ok else "sim, a soma é 1", "não, a soma é 0"],
             "%s + %s + %s = %s. %s" % (tuple(fq(p) for p in ps) + (fq(s), "A soma de todas as probabilidades deve ser 1: <b>sim</b>." if ok else "Deveria ser 1: <b>não</b>.")))


def s3_formas():
    n = R.choice([4, 5, 8, 10, 20, 25, 40, 50])
    a = R.randint(1, n - 1)
    p = F(a, n)
    if pct(p) is None:
        return None
    k = R.choice(["dec", "pct"])
    if k == "dec":
        return M("Escreva a probabilidade %s na forma decimal." % fq(p), d(p), [d(p * 10) if p * 10 < 10 else d(p / 10), d(1 - p), "%d,%d" % (a, n) if n < 100 else d(p + F(1, 10))],
                 "%d ÷ %d = <b>%s</b>." % (a, n, d(p)))
    return M("Escreva a probabilidade %s em porcentagem." % fq(p), pct(p), [pct(1 - p) if 1 - p != p else "%d%%" % a, "%d%%" % a if pct(p) != "%d%%" % a else "%d%%" % n, d(p)],
             "%s = %s = <b>%s</b>." % (fq(p), d(p), pct(p)))


s4_conceitos = bank(R, [
    ("A soma das probabilidades de todos os resultados de um experimento é…", "1", ["0", "100", "o número de resultados"]),
    ("Se P(A) = 0,3, então P(não A) é…", "0,7", ["0,3", "1,3", "70"]),
    ("Um evento e seu complementar…", "não acontecem juntos e um deles sempre acontece", ["acontecem sempre juntos", "têm sempre a mesma probabilidade", "têm probabilidades que somam 0"]),
    ("Lançando dois dados, (1, 2) e (2, 1) são…", "dois resultados diferentes", ["o mesmo resultado", "impossíveis", "o complementar um do outro"]),
    ("Lançando uma moeda e um dado, cada resultado do espaço amostral tem probabilidade…", "1/12", ["1/8", "1/6", "1/2"]),
    ("A probabilidade de tirar um número menor que 7 num dado comum é…", "1", ["0", "6/7", "1/6"]),
    ("Uma probabilidade pode ser 1,2?", "não, fica sempre entre 0 e 1", ["sim", "só em dados", "sim, se for porcentagem"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Espaço amostral", mix(R, seen, [(p_esp, 14), (p_dado, 6)])),
        ("Probabilidade de um evento", mix(R, seen, [(p_urna, 12), (p_dois, 8)])),
        ("Evento complementar", mix(R, seen, [(s1_complementar, 20)])),
        ("A soma das probabilidades é 1", mix(R, seen, [(s2_soma1, 14), (s4_conceitos, 6)])),
        ("Fração, decimal e porcentagem", mix(R, seen, [(s3_formas, 12), (s1_complementar, 4), (s2_soma1, 4)])),
    ]
    body = lesson(
        ["O <b>espaço amostral</b> é o conjunto de todos os resultados. Em etapas, use o princípio multiplicativo: moeda e dado = 2 · 6 = 12.",
         "A <b>soma das probabilidades</b> de todos os resultados é <b>1</b> (ou 100%).",
         "O <b>evento complementar</b> de A é «A não acontece»: P(não A) = 1 − P(A).",
         "Uma probabilidade pode ser escrita em fração, decimal ou porcentagem: 1/4 = 0,25 = 25%."],
        [("P(chover) = 30%", ["100% − 30%"], "P(não chover) = 70%"),
         ("P(azul) = 1/2, P(verde) = 1/3, resto amarelo", ["1 − 1/2 − 1/3"], "P(amarelo) = 1/6")],
        [["Somas que passam de 1", "Se a soma de todas as probabilidades não dá 1, algo está errado."],
         ["Fazer 100 − P com P em fração", "Use 1 − P para frações e decimais, 100% − P para porcentagens."],
         ["Contar (1, 2) e (2, 1) como um só", "Com dois dados há 36 resultados."]])
    faq = [("O que é evento complementar?", "É o evento «A não acontece». Sua probabilidade é 1 − P(A). Se a chance de chover é 30%, a de não chover é 70%."),
           ("O que a BNCC pede no 8º ano?", "Calcular a probabilidade de eventos, com base na construção do espaço amostral, utilizando o princípio multiplicativo, e reconhecer que a soma das probabilidades de todos os elementos do espaço amostral é igual a 1 (EF08MA22).")]
    unit(R, "probabilidade", "E", ["EF08MA22"],
         "Calcular a probabilidade de eventos, com base na construção do espaço amostral, utilizando o princípio multiplicativo, e reconhecer que a soma das probabilidades de todos os elementos do espaço amostral é igual a 1",
         "Probabilidade e evento complementar", "Probabilidade",
         "Atividades de matemática para o 8º ano sobre probabilidade: espaço amostral, princípio multiplicativo, evento complementar, soma das probabilidades igual a 1 e porcentagem. 100 exercícios com gabarito.",
         "A soma das probabilidades é 1", "P(não A) = 1 − P(A)",
         body, faq, sets, 17, grade="8-ano")


if __name__ == "__main__":
    main()
