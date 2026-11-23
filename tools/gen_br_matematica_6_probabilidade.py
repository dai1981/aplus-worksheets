# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Probabilidade (Probabilidade e estatística, EF06MA30)
  python3 tools/gen_br_matematica_6_probabilidade.py
Espaço amostral; probabilidade como fração (casos favoráveis ÷ casos possíveis), decimal e porcentagem; eventos certos e impossíveis
(probabilidade 1 e 0); dados, moedas, urnas, roletas e sorteios; frequência relativa de um experimento repetido.
Usa geradores do 5º ano (dado, saco, roleta) com outro sorteio.
Erros: dividir favoráveis por desfavoráveis, esquecer resultados do espaço amostral, achar que um resultado «está devendo».
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, fq, bank, unit

R = random.Random(86020)
p_dado, p_saco, p_roleta = use("gen_br_matematica_5_probabilidade", 86920, "s2_dado", "s2_saco", "s3_roleta")
CORES = [("azuis", "azul"), ("vermelhas", "vermelha"), ("verdes", "verde"), ("amarelas", "amarela"), ("pretas", "preta"), ("brancas", "branca")]


def s1_urna():
    cs = R.sample(CORES, 3)
    ns = [R.randint(1, 9) for _ in cs]
    t = sum(ns)
    i = R.randrange(3)
    p = F(ns[i], t)
    k = R.choice(["fr", "pct"])
    txt = "Uma urna tem %s. Tirando uma bola sem olhar, qual é a probabilidade de sair uma bola %s" % (", ".join("%d bolas %s" % (n, c[0]) for n, c in zip(ns[:-1], cs[:-1])) + " e %d bolas %s" % (ns[-1], cs[-1][0]), cs[i][1])
    if k == "pct":
        if (p * 100).denominator != 1:
            return None
        return M(txt + " (em porcentagem)?", "%s%%" % d(p * 100), ["%s%%" % d(ns[i]), "%s%%" % d(100 - p * 100), "%s%%" % d(F(ns[i] * 100, t - ns[i]), 1) if t != ns[i] else "50%"],
                 "%d em %d = %s = <b>%s%%</b>." % (ns[i], t, fq(p), d(p * 100)))
    return M(txt + "?", fq(p), [fq(F(ns[i], t - ns[i])) if t - ns[i] else "1", fq(F(1, 3)) if p != F(1, 3) else fq(F(1, t)), fq(1 - p) if p != F(1, 2) else fq(F(ns[i] + 1, t))],
             "Casos favoráveis ÷ casos possíveis: %d ÷ %d = <b>%s</b>." % (ns[i], t, fq(p)))


def s2_dado():
    ev = R.choice([("um número par", [2, 4, 6]), ("um número maior que 4", [5, 6]), ("um múltiplo de 3", [3, 6]), ("um número primo", [2, 3, 5]), ("um número menor que 3", [1, 2]),
                   ("o número 7", []), ("um número de 1 a 6", [1, 2, 3, 4, 5, 6]), ("um divisor de 6", [1, 2, 3, 6]), ("um número ímpar maior que 1", [3, 5])])
    p = F(len(ev[1]), 6)
    ans = fq(p) if 0 < p < 1 else ("0 (impossível)" if p == 0 else "1 (certo)")
    ws = [fq(F(len(ev[1]), 6 - len(ev[1]))) if 0 < len(ev[1]) < 6 and F(len(ev[1]), 6 - len(ev[1])) < 1 else "1/2", fq(F(1, 6)) if p != F(1, 6) else fq(F(1, 3)), "0 (impossível)" if p else "1 (certo)", fq(F(len(ev[1]) + 1, 6)) if len(ev[1]) < 5 else "5/6"]
    return M("Lançando um dado comum, qual é a probabilidade de sair %s?" % ev[0], ans, ws,
             "Favoráveis: %s (%d de 6): <b>%s</b>." % (", ".join(map(str, ev[1])) or "nenhum", len(ev[1]), ans))


def s3_formas():
    p = R.choice([F(1, 2), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5), F(1, 10), F(3, 10), F(7, 10), F(1, 20), F(1, 8), F(3, 8)])
    k = R.choice(["dec", "pct"])
    if k == "dec":
        return M("Uma probabilidade de %s, escrita como número decimal, é…" % fq(p), d(p), [d(F(p.numerator, 10)) if p.numerator < 10 else d(p + F(1, 10)), d(p / 10, 4), "%d,%d" % (p.numerator, p.denominator)], "%d ÷ %d = <b>%s</b>." % (p.numerator, p.denominator, d(p)))
    return M("Uma probabilidade de %s, escrita em porcentagem, é…" % fq(p), "%s%%" % d(p * 100), ["%d%%" % p.denominator, "%s%%" % d(p * 10), "%d%%" % (p.numerator * 10) if p.numerator * 10 != p * 100 else "%s%%" % d(p * 100 + 5)], "%s = %s/100 = <b>%s%%</b>." % (fq(p), d(p * 100), d(p * 100)))


def s4_frequencia():
    n = R.choice([20, 40, 50, 100, 200])
    c = R.randint(n // 5, n * 4 // 5)
    if (F(c * 100, n)).denominator != 1:
        return None
    obj = R.choice([("Uma moeda foi lançada %d vezes e deu cara %d vezes." % (n, c), "cara"), ("Um time cobrou %d pênaltis e acertou %d." % (n, c), "acerto"), ("Uma tachinha foi jogada %d vezes e caiu com a ponta para cima %d vezes." % (n, c), "ponta para cima")])
    return M("%s Qual é a frequência relativa de «%s», em porcentagem?" % obj, "%s%%" % d(F(c * 100, n)), ["%d%%" % c if c != F(c * 100, n) else "%d%%" % (c + 5), "%s%%" % d(F((n - c) * 100, n)), "50%" if F(c * 100, n) != 50 else "25%"],
             "%d ÷ %d = %s = <b>%s%%</b>." % (c, n, d(F(c, n)), d(F(c * 100, n))))


s5_conceitos = bank(R, [
    ("A probabilidade de um evento impossível é…", "0", ["1", "1/2", "100"]),
    ("A probabilidade de um evento certo é…", "1 (ou 100%)", ["0", "1/2", "10"]),
    ("Qualquer probabilidade fica entre…", "0 e 1", ["0 e 10", "1 e 100", "−1 e 1"]),
    ("Uma moeda deu cara 4 vezes seguidas. Na 5ª vez, a probabilidade de cara é…", "1/2", ["maior que 1/2", "menor que 1/2", "0"]),
    ("Espaço amostral é…", "o conjunto de todos os resultados possíveis", ["só os resultados favoráveis", "o resultado mais provável", "a soma dos resultados"]),
    ("Quantos resultados tem o espaço amostral de lançar um dado e uma moeda?", "12", ["8", "6", "36"]),
    ("Em 20 rifas vendidas, comprei 3. A probabilidade de eu ganhar é…", "3/20", ["3/17", "1/20", "17/20"]),
    ("Quanto mais vezes repetimos um experimento, a frequência relativa…", "fica mais perto da probabilidade", ["fica sempre igual a 1", "não muda", "fica mais longe da probabilidade"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Dados e espaço amostral", mix(R, seen, [(s2_dado, 9), (p_dado, 7), (s5_conceitos, 4)])),
        ("Urnas e sacos", mix(R, seen, [(s1_urna, 14), (p_saco, 6)])),
        ("Fração, decimal e porcentagem", mix(R, seen, [(s3_formas, 16), (p_roleta, 4)])),
        ("Frequência relativa", mix(R, seen, [(s4_frequencia, 16), (s5_conceitos, 4)])),
        ("Revisão", mix(R, seen, [(s1_urna, 10), (s3_formas, 6), (p_saco, 4)])),
    ]
    body = lesson(
        ["O <b>espaço amostral</b> é a lista de todos os resultados possíveis. Num dado: 1, 2, 3, 4, 5, 6.",
         "<b>Probabilidade</b> = casos favoráveis ÷ casos possíveis. Ela vai de 0 (impossível) a 1 (certo) e pode ser escrita como fração, decimal ou porcentagem.",
         "Repetindo um experimento muitas vezes, a <b>frequência relativa</b> (vezes que aconteceu ÷ total) fica perto da probabilidade."],
        [("Urna com 3 azuis e 5 vermelhas: azul", ["3 favoráveis", "8 possíveis"], "3/8 = 0,375 = 37,5%"),
         ("Dado: número maior que 4", ["5 e 6"], "2/6 = 1/3")],
        [["Dividir favoráveis por desfavoráveis", "Divida pelo total de casos possíveis."],
         ["Esquecer resultados", "Liste todo o espaço amostral."],
         ["Achar que o resultado «está devendo»", "Cada lançamento da moeda é independente."]])
    faq = [("Como calcular uma probabilidade?", "Conte os casos favoráveis e os casos possíveis (todos igualmente prováveis) e divida: favoráveis ÷ possíveis."),
           ("O que a BNCC pede no 6º ano?", "Calcular a probabilidade de um evento aleatório, expressando-a por número racional (forma fracionária, decimal e percentual) e comparar esse número com a probabilidade obtida por meio de experimentos sucessivos (EF06MA30).")]
    unit(R, "probabilidade", "E", ["EF06MA30"],
         "Calcular a probabilidade de um evento aleatório, expressando-a por número racional (forma fracionária, decimal e percentual) e comparar esse número com a probabilidade obtida por meio de experimentos sucessivos",
         "Probabilidade: fração, decimal e porcentagem", "Probabilidade",
         "Atividades de matemática para o 6º ano sobre probabilidade: espaço amostral, casos favoráveis e possíveis, dados, urnas e roletas, probabilidade em fração, decimal e porcentagem e frequência relativa. 100 exercícios com gabarito.",
         "Probabilidade = favoráveis ÷ possíveis.", "Vai de 0 (impossível) a 1 (certo).",
         body, faq, sets, 20, grade="6-ano")


if __name__ == "__main__":
    main()
