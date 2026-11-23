# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Probabilidade – chances (Probabilidade e estatística, EF03MA25)
  python3 tools/gen_br_matematica_3_probabilidade.py
Eventos certos, possíveis e impossíveis; todos os resultados possíveis de dados, moedas, roletas e sacos de bolinhas;
mais chance e menos chance; jogos justos; combinações simples.
Erros: achar que o que é «difícil» é impossível, contar resultados repetidos, achar que a cor que saiu antes não sai mais.
"""
import random
from br_common import mcq, lesson, make_unit, mix, wrap, text, line, INK, GREEN, Kids

R = random.Random(80322)
K = Kids(R)
CORES = {"vermelha": "#e57373", "azul": "#64b5f6", "verde": "#81c784", "amarela": "#ffd54f"}
PL = {"vermelha": "vermelhas", "azul": "azuis", "verde": "verdes", "amarela": "amarelas"}


def cor(c, n):
    return "%d %s" % (n, c if n == 1 else PL[c])


def saco(cnt):
    s = ["<path d='M30 40 Q20 150 60 170 L180 170 Q220 150 210 40 Z' fill='#f6efd6' stroke='%s' stroke-width='2'/>" % INK]
    balls = [c for c, n in cnt for _ in range(n)]
    R.shuffle(balls)
    for i, c in enumerate(balls):
        x = 56 + (i % 6) * 26
        y = 70 + (i // 6) * 26
        s.append("<circle cx='%d' cy='%d' r='11' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x, y, CORES[c], INK))
    return wrap(240, 180, "".join(s), "saco com bolinhas: " + ", ".join(cor(c, n) for c, n in cnt), lg=True)


def roleta(parts):
    import math
    s = []
    n = len(parts)
    cx, cy, r = 90, 90, 78
    for i, c in enumerate(parts):
        a0, a1 = 2 * math.pi * i / n - math.pi / 2, 2 * math.pi * (i + 1) / n - math.pi / 2
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, x0, y0, r, r, x1, y1, CORES[c], INK))
    s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (cx - 6, cy, cx + 6, cy, cx, cy - 50, INK))
    return wrap(180, 180, "".join(s), "roleta dividida em %d partes iguais" % n, lg=True)


EV = [("Amanhã o sol vai nascer.", "certo"), ("Jogando um dado comum, sair o número 7.", "impossível"), ("Jogando um dado, sair um número par.", "possível"),
      ("Jogando uma moeda, sair cara.", "possível"), ("Tirar uma bolinha azul de um saco só com bolinhas vermelhas.", "impossível"),
      ("Tirar uma bolinha vermelha de um saco só com bolinhas vermelhas.", "certo"), ("Chover amanhã na sua cidade.", "possível"),
      ("Jogando um dado, sair um número menor que 7.", "certo"), ("Um gato aprender a falar português.", "impossível"),
      ("Depois de segunda-feira vir terça-feira.", "certo"), ("Ganhar uma partida de futebol.", "possível"), ("Jogando dois dados, a soma ser 13.", "impossível"),
      ("Sortear um nome de menino numa turma com meninos e meninas.", "possível"), ("Um mês ter 40 dias.", "impossível")]


def s1_evento():
    f, a = R.choice(EV)
    return mcq("«%s» é um evento…" % f, a, [x for x in ("certo", "possível", "impossível", "muito provável e impossível") if x != a],
               "Certo: sempre acontece. Impossível: nunca acontece. Possível: pode ou não acontecer. Resposta: <b>%s</b>." % a)


def s2_resultados():
    k = R.choice(["dado", "moeda", "duas", "roleta", "dado_par", "cartas"])
    if k == "dado":
        return mcq("Quais são todos os resultados possíveis ao jogar um dado comum?", "1, 2, 3, 4, 5 e 6", ["1, 2, 3, 4 e 5", "0, 1, 2, 3, 4, 5 e 6", "só 6"],
                   "O dado tem 6 faces: <b>1, 2, 3, 4, 5 e 6</b>.")
    if k == "moeda":
        return mcq("Quantos resultados possíveis há ao jogar uma moeda?", "2 (cara ou coroa)", ["1", "3", "4"], "Pode sair cara ou coroa: <b>2</b>.")
    if k == "duas":
        return mcq("Jogando duas moedas, quais são todos os resultados possíveis?", "cara-cara, cara-coroa, coroa-cara, coroa-coroa",
                   ["cara-cara e coroa-coroa", "cara-coroa e coroa-cara", "cara, coroa"], "São 4 resultados: <b>cara-cara, cara-coroa, coroa-cara, coroa-coroa</b>.")
    if k == "roleta":
        cs = R.sample(sorted(CORES), R.randint(2, 4))
        return mcq(roleta(cs) + "Quais cores podem sair nesta roleta?", ", ".join(sorted(cs)),
                   [", ".join(sorted(cs[:-1])), ", ".join(sorted(cs + [x for x in sorted(CORES) if x not in cs][:1])) if len(cs) < 4 else "só " + cs[0], "só " + cs[-1]],
                   "Podem sair todas as cores que estão na roleta: <b>%s</b>." % ", ".join(sorted(cs)))
    if k == "dado_par":
        return mcq("Jogando um dado, quais resultados são números pares?", "2, 4 e 6", ["1, 3 e 5", "2 e 4", "4 e 6"], "Pares do dado: <b>2, 4 e 6</b>.")
    n = R.randint(3, 6)
    return mcq("Numa caixa há cartões numerados de 1 a %d. Tirando um cartão, quantos resultados são possíveis?" % n, str(n), [str(n - 1), str(n + 1), "1"],
               "Pode sair qualquer cartão de 1 a %d: <b>%d</b> resultados." % (n, n))


def s3_chance():
    a, b = R.sample(sorted(CORES), 2)
    na, nb = R.sample(range(1, 9), 2)
    ask = R.choice(["mais", "menos"])
    win = a if (na > nb) == (ask == "mais") else b
    return mcq(saco([(a, na), (b, nb)]) + "Tirando uma bolinha sem olhar, que cor tem %s chance de sair?" % ask, "a %s" % win,
               ["a %s" % (b if win == a else a), "as duas têm a mesma chance", "não dá para saber nada"],
               "Há %s e %s. A cor com %s bolinhas tem %s chance: <b>a %s</b>." % (cor(a, na), cor(b, nb), ask, ask, win))


def s3_roleta():
    n = R.choice([4, 6, 8])
    a, b = R.sample(sorted(CORES), 2)
    ka = R.randint(1, n - 1)
    if ka * 2 == n:
        return None
    parts = [a] * ka + [b] * (n - ka)
    R.shuffle(parts)
    win = a if ka > n - ka else b
    return mcq(roleta(parts) + "Girando a roleta, que cor tem mais chance de sair?", "a %s" % win, ["a %s" % (b if win == a else a), "as duas têm a mesma chance", "a que saiu da última vez"],
               "A %s ocupa %d de %d partes; a outra, %d: <b>a %s</b>." % (win, max(ka, n - ka), n, min(ka, n - ka), win))


def s4_justo():
    k = R.choice(["dado", "moeda", "roleta", "saco"])
    (p1, _), (p2, _) = K.two()
    if k == "dado":
        return mcq("%s ganha se o dado der 1 ou 2. %s ganha se der 3, 4, 5 ou 6. O jogo é justo?" % (p1, p2), "não, %s tem mais chance" % p2,
                   ["sim, os dois têm a mesma chance", "não, %s tem mais chance" % p1, "depende da sorte de cada um"],
                   "%s tem 2 resultados e %s tem 4: <b>não, %s tem mais chance</b>." % (p1, p2, p2))
    if k == "moeda":
        return mcq("%s ganha se sair cara e %s ganha se sair coroa. O jogo é justo?" % (p1, p2), "sim, os dois têm a mesma chance",
                   ["não, %s tem mais chance" % p1, "não, %s tem mais chance" % p2, "não, coroa sai mais"], "Cara e coroa têm a mesma chance: <b>sim, é justo</b>.")
    if k == "roleta":
        return mcq("%s ganha com número par no dado e %s com número ímpar. O jogo é justo?" % (p1, p2), "sim, os dois têm a mesma chance",
                   ["não, %s tem mais chance" % p1, "não, %s tem mais chance" % p2, "não, o 6 sai mais"], "3 pares (2, 4, 6) e 3 ímpares (1, 3, 5): <b>sim, é justo</b>.")
    a, b = R.randint(2, 6), R.randint(2, 6)
    if a == b:
        return mcq("Num saco há %d bolinhas azuis e %d vermelhas. %s ganha se sair azul e %s se sair vermelha. O jogo é justo?" % (a, b, p1, p2), "sim, os dois têm a mesma chance",
                   ["não, %s tem mais chance" % p1, "não, %s tem mais chance" % p2, "não dá para saber"], "Há o mesmo número de cada cor: <b>sim, é justo</b>.")
    win = p1 if a > b else p2
    return mcq("Num saco há %d bolinhas azuis e %d vermelhas. %s ganha se sair azul e %s se sair vermelha. O jogo é justo?" % (a, b, p1, p2), "não, %s tem mais chance" % win,
               ["sim, os dois têm a mesma chance", "não, %s tem mais chance" % (p2 if win == p1 else p1), "não dá para saber"],
               "%d azuis e %d vermelhas: <b>não, %s tem mais chance</b>." % (a, b, win))


def s5_combinar():
    k = R.choice(["roupa", "lanche", "sorvete", "placa"])
    if k == "roupa":
        a, b = R.randint(2, 4), R.randint(2, 3)
        return mcq("%s tem %d camisetas e %d bermudas. De quantas maneiras diferentes pode se vestir com uma camiseta e uma bermuda?" % (K.next()[0], a, b), str(a * b),
                   [str(a + b), str(a * b + 1), str(max(a, b))], "Cada camiseta combina com %d bermudas: %d × %d = <b>%d</b>." % (b, a, b, a * b))
    if k == "lanche":
        a, b = R.randint(2, 4), R.randint(2, 3)
        return mcq("Na cantina há %d tipos de sanduíche e %d tipos de suco. Quantos lanches diferentes (1 sanduíche e 1 suco) podem ser montados?" % (a, b), str(a * b),
                   [str(a + b), str(a * b - 1), str(a)], "%d × %d = <b>%d</b>." % (a, b, a * b))
    if k == "sorvete":
        a, b = R.randint(3, 5), 2
        return mcq("Uma sorveteria tem %d sabores e 2 tipos de casquinha. Quantos sorvetes diferentes de 1 bola dá para montar?" % a, str(a * b), [str(a + b), str(a), str(a * b + 2)],
                   "%d × 2 = <b>%d</b>." % (a, a * b))
    return mcq("Com os algarismos 1, 2 e 3, sem repetir, quantos números de 2 algarismos dá para formar?", "6", ["3", "9", "4"],
               "12, 13, 21, 23, 31, 32: <b>6</b> números.")


def main():
    seen = set()
    sets = [
        ("Certo, possível ou impossível", mix(R, seen, [(s1_evento, 14)]) + mix(R, seen, [(s2_resultados, 6)])),
        ("Todos os resultados possíveis", mix(R, seen, [(s2_resultados, 6), (s3_roleta, 14)])),
        ("Mais chance, menos chance", mix(R, seen, [(s3_chance, 20)])),
        ("O jogo é justo?", mix(R, seen, [(s4_justo, 12), (s3_roleta, 8)])),
        ("Combinações", mix(R, seen, [(s5_combinar, 12), (s3_chance, 8)])),
    ]
    body = lesson(
        ["Um evento <b>certo</b> sempre acontece; um <b>impossível</b> nunca acontece; um <b>possível</b> pode ou não acontecer.",
         "Antes de responder, liste <b>todos os resultados possíveis</b>: num dado, 1, 2, 3, 4, 5 e 6; numa moeda, cara ou coroa.",
         "Quem tem mais bolinhas no saco (ou mais partes na roleta) tem <b>mais chance</b> de sair.",
         "Um jogo é <b>justo</b> quando todos os jogadores têm a mesma chance de ganhar."],
        [("Saco com 5 vermelhas e 2 azuis", ["5 &gt; 2"], "vermelha tem mais chance"),
         ("Ganha com 1 ou 2 no dado; o outro com 3, 4, 5 ou 6", ["2 resultados contra 4"], "não é justo")],
        [["Achar que «difícil» é impossível", "Se pode acontecer, mesmo raramente, é possível."],
         ["Achar que a cor que saiu antes não sai mais", "Se a bolinha volta para o saco, as chances continuam as mesmas."],
         ["Esquecer resultados ao listar", "Organize: cara-cara, cara-coroa, coroa-cara, coroa-coroa."]],
        roleta(["azul", "azul", "azul", "vermelha"]))
    faq = [("O que a BNCC pede de probabilidade no 3º ano?", "Identificar, em eventos familiares aleatórios, todos os resultados possíveis, estimando os que têm maiores ou menores chances de ocorrência."),
           ("Como trabalhar chances em casa?", "Jogue dados e moedas, anote os resultados e converse: o que pode sair? O que nunca sai? Quem tem mais chance de ganhar?")]
    make_unit(R, "probabilidade", "E", ["EF03MA25"],
              "Identificar, em eventos familiares aleatórios, todos os resultados possíveis, estimando os que têm maiores ou menores chances de ocorrência",
              "Probabilidade: chances e resultados possíveis", "Probabilidade",
              "Atividades de matemática para o 3º ano sobre probabilidade: eventos certos, possíveis e impossíveis, resultados possíveis de dados, moedas e roletas, mais e menos chance, jogos justos e combinações. 100 exercícios com gabarito.",
              "Certo, possível ou impossível?", "Mais bolinhas, mais chance.",
              body, faq, sets, 22)


if __name__ == "__main__":
    main()
