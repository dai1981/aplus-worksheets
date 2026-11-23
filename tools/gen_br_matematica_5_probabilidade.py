# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Probabilidade (Probabilidade e estatística, EF05MA22, EF05MA23)
  python3 tools/gen_br_matematica_5_probabilidade.py
Espaço amostral (todos os resultados possíveis); eventos equiprováveis ou não; probabilidade como fração
(casos favoráveis ÷ casos possíveis) com dados, moedas, roletas, sacos de bolinhas e cartas; comparar chances; problemas.
Erros: esquecer resultados do espaço amostral, usar «favoráveis ÷ desfavoráveis», achar que a roleta com mais cores é mais justa.
"""
import random
from fractions import Fraction as Fr
import gen_br_matematica_3_probabilidade as P3
import re
from br_common import mcq as _mcq, lesson, make_unit, mix, fr, Kids


def _val(h):
    m = re.fullmatch(r"\s*<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>\s*", h)
    return Fr(int(m.group(1)), int(m.group(2))) if m else None


def mcq(q, correct, cands, e, *a, **k):
    """os distratores com o mesmo valor que a resposta (2/4 e 1/2) também seriam corretos: tira-os"""
    v = _val(correct)
    return _mcq(q, correct, [c for c in cands if v is None or _val(c) != v], e, *a, **k)

R = random.Random(80521)
K = Kids(R)
P3.R = random.Random(80921)
CORES = list(P3.CORES)
PL = P3.PL


def s1_espaco():
    k = R.choice(["dado", "moeda", "duas_moedas", "roleta", "dado_moeda", "letras"])
    if k == "dado":
        return mcq("Quais são todos os resultados possíveis ao lançar um dado comum?", "1, 2, 3, 4, 5 e 6", ["1, 2, 3, 4 e 5", "2, 4 e 6", "0, 1, 2, 3, 4, 5 e 6"],
                   "O espaço amostral do dado tem 6 resultados: <b>1, 2, 3, 4, 5 e 6</b>.")
    if k == "moeda":
        return mcq("Quantos resultados possíveis há ao lançar uma moeda?", "2 (cara ou coroa)", ["1", "3", "4"], "Cara ou coroa: <b>2 resultados</b>.")
    if k == "duas_moedas":
        return mcq("Lançando duas moedas, quais são os resultados possíveis?", "cara-cara, cara-coroa, coroa-cara e coroa-coroa", ["cara-cara e coroa-coroa", "cara-cara, cara-coroa e coroa-coroa", "cara e coroa"],
                   "Cada moeda tem 2 resultados: 2 × 2 = 4. <b>cara-cara, cara-coroa, coroa-cara e coroa-coroa</b>.")
    if k == "roleta":
        n = R.randint(3, 4)
        parts = R.sample(CORES, n)
        return mcq(P3.roleta(parts) + "Quais cores podem sair nesta roleta?", ", ".join(sorted(parts)), [", ".join(sorted(parts[:-1])), ", ".join(sorted(set(CORES) - {parts[0]})) if n == 3 else ", ".join(sorted(parts[1:])), ", ".join(sorted(CORES)) if n == 3 else "só " + parts[0]],
                   "Cada parte da roleta é um resultado possível: <b>%s</b>." % ", ".join(sorted(parts)))
    if k == "dado_moeda":
        return mcq("Lançando um dado e uma moeda, quantos resultados diferentes são possíveis?", "12", ["8", "6", "2"], "6 do dado × 2 da moeda = <b>12</b>.")
    w = R.choice(["BOLA", "MALA", "SAPO", "CASA", "LUA", "SOL"])
    s = sorted(set(w))
    return mcq("As letras da palavra %s foram escritas em cartões e colocadas num saco. Quais letras diferentes podem ser sorteadas?" % w, ", ".join(s),
               [", ".join(s[:-1]), ", ".join(list(w)), ", ".join(s + ["E"])], "As letras diferentes de %s são <b>%s</b>." % (w, ", ".join(s)))


def s1_justo():
    k = R.choice(["roleta_igual", "roleta_dif", "saco_igual", "saco_dif", "dado"])
    if k == "roleta_igual":
        n = R.choice([2, 3, 4])
        parts = R.sample(CORES, n)
        return mcq(P3.roleta(parts) + "Nesta roleta, todas as cores têm a mesma chance de sair?", "Sim, as partes são iguais", ["Não, a primeira cor tem mais chance", "Não, nunca é igual", "Só se girar devagar"],
                   "Cada cor ocupa 1 parte de %d iguais: os resultados são <b>equiprováveis</b>." % n)
    if k == "roleta_dif":
        a, b = R.sample(CORES, 2)
        m = R.randint(2, 3)
        parts = [a] * m + [b]
        R.shuffle(parts)
        return mcq(P3.roleta(parts) + "Nesta roleta, qual cor tem mais chance de sair?", a, [b, "as duas têm a mesma chance", "não dá para saber"],
                   "%s ocupa %d partes e %s ocupa 1: <b>%s</b> tem mais chance." % (a, m, b, a))
    if k == "saco_igual":
        a, b = R.sample(CORES, 2)
        n = R.randint(2, 6)
        return mcq(P3.saco([(a, n), (b, n)]) + "Tirando uma bolinha sem olhar, as duas cores têm a mesma chance?", "Sim, há %d de cada cor" % n, ["Não, %s tem mais chance" % a, "Não, %s tem mais chance" % b, "Não dá para saber"],
                   "Mesma quantidade de cada cor: chances iguais. <b>Sim</b>.")
    if k == "saco_dif":
        a, b = R.sample(CORES, 2)
        x, y = R.sample(range(1, 9), 2)
        big = a if x > y else b
        return mcq(P3.saco([(a, x), (b, y)]) + "Tirando uma bolinha sem olhar, que cor tem mais chance de sair?", big, [b if big == a else a, "as duas têm a mesma chance", "não dá para saber"],
                   "%s e %s: há mais bolinhas %s. <b>%s</b>." % (P3.cor(a, x), P3.cor(b, y), PL[big], big))
    return mcq("Ao lançar um dado comum, sair o 6 é mais difícil que sair o 1?", "Não, todos os números têm a mesma chance", ["Sim, o 6 é mais difícil", "Sim, o 1 é mais difícil", "Depende da cor do dado"],
               "Num dado comum, cada face tem 1 chance em 6: os resultados são <b>equiprováveis</b>.")


def s2_dado():
    k = R.choice(["num", "par", "maior", "menor", "mult3", "impar", "primo"])
    ev = {"num": ("o número %d" % R.randint(1, 6), 1), "par": ("um número par", 3), "maior": ("um número maior que %d", None), "menor": ("um número menor que %d", None),
          "mult3": ("um múltiplo de 3", 2), "impar": ("um número ímpar", 3), "primo": ("um número maior que 6", 0)}[k]
    if k in ("maior", "menor"):
        t = R.randint(1, 5) if k == "maior" else R.randint(2, 6)
        f = 6 - t if k == "maior" else t - 1
        name = ev[0] % t
    else:
        name, f = ev
    ans = fr(f, 6) if f else "0 (impossível)"
    w = [fr(1, f) if f > 1 else fr(6, 1), fr(f, 6 - f) if 0 < f < 6 else fr(1, 2), fr(6 - f, 6) if f != 3 and f else fr(1, 3), fr(f + 1, 6) if f < 6 else fr(5, 6)]
    return mcq("Ao lançar um dado comum, qual é a probabilidade de sair %s?" % name, ans, w,
               "Casos favoráveis: %d. Casos possíveis: 6. Probabilidade = <b>%s</b>." % (f, ans))


def s2_saco():
    n = R.randint(2, 3)
    cs = R.sample(CORES, n)
    cnt = [(c, R.randint(1, 6)) for c in cs]
    tot = sum(x for _, x in cnt)
    c, x = R.choice(cnt)
    return mcq(P3.saco(cnt) + "Tirando uma bolinha sem olhar, qual é a probabilidade de ela ser %s?" % c, fr(x, tot), [fr(x, tot - x) if tot - x != tot else fr(1, tot), fr(1, tot) if x != 1 else fr(1, n), fr(tot - x, tot), fr(1, n), fr(x + 1, tot), fr(x, tot + 1)],
               "Há %d bolinhas, e %d são %s: <b>%s</b>." % (tot, x, c if x == 1 else PL[c], fr(x, tot)))


def s3_roleta():
    n = R.choice([4, 5, 6, 8])
    a = R.choice(CORES)
    m = R.randint(1, n - 1)
    others = [c for c in CORES if c != a]
    parts = [a] * m + [R.choice(others) for _ in range(n - m)]
    R.shuffle(parts)
    return mcq(P3.roleta(parts) + "A roleta tem %d partes iguais. Qual é a probabilidade de o ponteiro parar no %s?" % (n, a.replace("vermelha", "vermelho").replace("amarela", "amarelo")),
               fr(m, n), [fr(m, n - m) if m != n - m else fr(1, n), fr(1, n) if m > 1 else fr(1, 2), fr(n - m, n), fr(1, m) if m > 1 else fr(2, n), fr(m + 1, n), fr(m, n + 1)],
               "%d das %d partes são dessa cor: <b>%s</b>." % (m, n, fr(m, n)))


def s3_cartas():
    n = R.randint(5, 12)
    k = R.choice(["par", "maior", "num"])
    if k == "par":
        f = n // 2
        name = "um número par"
    elif k == "maior":
        t = R.randint(2, n - 2)
        f = n - t
        name = "um número maior que %d" % t
    else:
        f = 1
        name = "o número %d" % R.randint(1, n)
    return mcq("Cartões numerados de 1 a %d estão numa caixa. Sorteando um cartão, qual é a probabilidade de sair %s?" % (n, name), fr(f, n),
               [fr(f, n - f) if n - f != n else fr(1, n + 1), fr(1, n) if f > 1 else fr(1, n - 1), fr(n - f, n), fr(f, 10) if n != 10 else fr(f + 1, n)],
               "Casos favoráveis: %d. Casos possíveis: %d. <b>%s</b>." % (f, n, fr(f, n)))


def s4_comparar():
    a, b = R.sample(CORES, 2)
    x1, y1 = R.randint(1, 5), R.randint(1, 5)
    x2, y2 = R.randint(1, 5), R.randint(1, 5)
    p1, p2 = Fr(x1, x1 + y1), Fr(x2, x2 + y2)
    if p1 == p2 and R.random() < 0.6:
        return None
    ans = "o saco 1" if p1 > p2 else "o saco 2" if p2 > p1 else "os dois dão a mesma chance"
    q = "Saco 1: %s e %s. Saco 2: %s e %s. Em qual saco é mais provável tirar uma bolinha %s?" % (P3.cor(a, x1), P3.cor(b, y1), P3.cor(a, x2), P3.cor(b, y2), a)
    return mcq(q, ans, [x for x in ["o saco 1", "o saco 2", "os dois dão a mesma chance", "o saco com mais bolinhas"] if x != ans],
               "Saco 1: %s. Saco 2: %s. %s" % (fr(x1, x1 + y1), fr(x2, x2 + y2), "Compare as frações: <b>%s</b>." % ans))


def s4_classificar():
    q, a, w = R.choice([("Uma roleta tem 3 partes azuis e 1 vermelha. Sair azul é…", "mais provável que sair vermelho", ["menos provável que sair vermelho", "tão provável quanto sair vermelho", "impossível"]),
                        ("Num saco só com bolinhas verdes, tirar uma verde é…", "certo (probabilidade 1)", ["impossível", "pouco provável", "provável, mas não certo"]),
                        ("Num dado comum, sair o número 8 tem probabilidade…", "0 (impossível)", ["1", fr(1, 6), fr(1, 8)]),
                        ("A probabilidade de um evento certo é…", "1", ["0", fr(1, 2), "100"]),
                        ("Se a probabilidade de chover é " + fr(9, 10) + ", chover é…", "muito provável", ["impossível", "pouco provável", "certo"]),
                        ("Se a probabilidade de ganhar um sorteio é " + fr(1, 100) + ", ganhar é…", "pouco provável", ["muito provável", "certo", "impossível"]),
                        ("Uma moeda foi lançada 5 vezes e deu cara todas as vezes. Na 6ª vez, a chance de dar cara é…", fr(1, 2), ["maior que " + fr(1, 2), "menor que " + fr(1, 2), "0"]),
                        ("Quais eventos são equiprováveis ao lançar um dado?", "sair 2 e sair 5", ["sair par e sair 1", "sair menor que 3 e sair 6", "sair 7 e sair 1"]),
                        ("Qual destes números pode ser uma probabilidade?", fr(3, 4), [fr(5, 4), "2", "10"]),
                        ("Numa turma com 12 meninas e 18 meninos, sorteando um nome, é mais provável sair…", "um menino", ["uma menina", "tanto faz", "um professor"])])
    return mcq(q, a, w, "A probabilidade vai de 0 (impossível) a 1 (certo). Resposta: <b>%s</b>." % a)


def s5_problema():
    k = R.choice(["rifa", "turma", "balas", "sorteio", "duas", "meias"])
    p, g = K.next()
    if k == "rifa":
        n = R.choice([50, 100, 200, 20])
        c = R.randint(1, 5)
        return mcq("Uma rifa tem %d números. %s comprou %d. Qual é a probabilidade de %s ganhar?" % (n, p, c, p), fr(c, n), [fr(1, n) if c > 1 else fr(1, n - 1), fr(c, n - c), fr(n - c, n), fr(1, c) if c > 1 else fr(c, 10)],
                   "%d números favoráveis em %d: <b>%s</b>." % (c, n, fr(c, n)))
    if k == "turma":
        m, h = R.randint(8, 18), R.randint(8, 18)
        return mcq("Numa turma há %d meninas e %d meninos. Sorteando um aluno, qual é a probabilidade de ser uma menina?" % (m, h), fr(m, m + h), [fr(m, h), fr(h, m + h), fr(1, m + h), fr(1, 2) if m != h else fr(1, m)],
                   "Total: %d + %d = %d alunos. Meninas: %d. <b>%s</b>." % (m, h, m + h, m, fr(m, m + h)))
    if k == "balas":
        a, b, c = R.randint(2, 8), R.randint(2, 8), R.randint(2, 8)
        t = a + b + c
        return mcq("Um pote tem %d balas de morango, %d de uva e %d de limão. Pegando uma bala sem olhar, qual é a probabilidade de ser de uva?" % (a, b, c), fr(b, t),
                   [fr(b, a + c), fr(1, 3), fr(a + c, t), fr(1, t)], "Total: %d balas. De uva: %d. <b>%s</b>." % (t, b, fr(b, t)))
    if k == "sorteio":
        n = R.choice([4, 5, 6])
        names = [K.next()[0] for _ in range(n)]
        if len(set(names)) < n:
            return None
        return mcq("Os nomes %s foram colocados numa caixa. Sorteando um nome, qual é a probabilidade de sair %s?" % (", ".join(names[:-1]) + " e " + names[-1], names[0]), fr(1, n),
                   [fr(1, n - 1), fr(n - 1, n), fr(1, 2), "1"], "1 nome favorável em %d: <b>%s</b>." % (n, fr(1, n)))
    if k == "duas":
        return mcq("Lançando duas moedas, qual é a probabilidade de saírem duas caras?", fr(1, 4), [fr(1, 2), fr(1, 3), fr(2, 4)],
                   "Resultados: cara-cara, cara-coroa, coroa-cara, coroa-coroa. Só 1 em 4 tem duas caras: <b>%s</b>." % fr(1, 4)) if R.random() < 0.5 else \
            mcq("Lançando duas moedas, qual é a probabilidade de sair uma cara e uma coroa?", fr(2, 4), [fr(1, 4), fr(1, 3), fr(3, 4)],
                "cara-coroa e coroa-cara: 2 de 4 resultados = <b>%s</b> (= %s)." % (fr(2, 4), fr(1, 2)))
    a, b = R.randint(2, 6), R.randint(2, 6)
    return mcq("Numa gaveta há %d meias brancas e %d meias pretas. %s tira uma meia sem olhar. Qual é a probabilidade de ser preta?" % (a, b, p), fr(b, a + b),
               [fr(b, a), fr(a, a + b) if a != b else fr(1, a + b), fr(1, 2) if a != b else fr(1, b), fr(1, a + b)], "%d pretas em %d meias: <b>%s</b>." % (b, a + b, fr(b, a + b)))


def main():
    seen = set()
    sets = [
        ("Espaço amostral e chances", mix(R, seen, [(s1_espaco, 8), (s1_justo, 12)])),
        ("Probabilidade com dados e sacos", mix(R, seen, [(s2_dado, 10), (s2_saco, 10)])),
        ("Roletas e cartões", mix(R, seen, [(s3_roleta, 12), (s3_cartas, 8)])),
        ("Comparar probabilidades", mix(R, seen, [(s4_comparar, 12), (s4_classificar, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["O <b>espaço amostral</b> é a lista de todos os resultados possíveis. No dado: 1, 2, 3, 4, 5 e 6.",
         "Resultados <b>equiprováveis</b> têm a mesma chance, como as faces de um dado ou as partes iguais de uma roleta.",
         "<b>Probabilidade</b> = casos favoráveis ÷ casos possíveis. Sair um número par no dado: 3 em 6 = " + fr(3, 6) + ".",
         "A probabilidade vai de 0 (impossível) a 1 (certo)."],
        [("Num saco há 3 bolinhas azuis e 5 vermelhas. Probabilidade de sair azul?", ["casos possíveis: 3 + 5 = 8", "casos favoráveis: 3"], fr(3, 8)),
         ("Probabilidade de sair um número maior que 4 num dado?", ["maiores que 4: 5 e 6", "2 em 6"], fr(2, 6))],
        [["Esquecer resultados do espaço amostral", "Liste todos: com duas moedas são 4 resultados, não 3."],
         ["Dividir favoráveis por desfavoráveis: 3 azuis e 5 vermelhas → " + fr(3, 5), "Divida pelo total: " + fr(3, 8) + "."],
         ["Achar que uma cor «está devendo»", "A moeda não tem memória: a chance continua " + fr(1, 2) + "."]],
        P3.roleta(["azul", "azul", "vermelha", "verde"]))
    faq = [("O que o 5º ano aprende sobre probabilidade?", "A BNCC pede apresentar todos os resultados possíveis de um experimento aleatório, estimar se são igualmente prováveis ou não e determinar a probabilidade de um resultado, quando todos são equiprováveis, como uma fração."),
           ("Como explicar probabilidade para crianças?", "Use sacos com bolinhas e roletas de papel. Conte quantas vezes cada resultado pode acontecer e escreva a fração «casos favoráveis sobre casos possíveis».")]
    make_unit(R, "probabilidade", "E", ["EF05MA22", "EF05MA23"],
              "Apresentar todos os possíveis resultados de um experimento aleatório, estimando se esses resultados são igualmente prováveis ou não; determinar a probabilidade de ocorrência de um resultado em eventos aleatórios, quando todos os resultados possíveis têm a mesma chance de ocorrer (equiprováveis)",
              "Probabilidade: espaço amostral e chances como fração", "Probabilidade",
              "Atividades de matemática para o 5º ano sobre probabilidade: espaço amostral, eventos equiprováveis, probabilidade como fração com dados, moedas, roletas, sacos de bolinhas e problemas. 100 exercícios com gabarito.",
              "Probabilidade = casos favoráveis ÷ casos possíveis.", "Vai de 0 (impossível) a 1 (certo).",
              body, faq, sets, 21, grade="5-ano")


if __name__ == "__main__":
    main()
