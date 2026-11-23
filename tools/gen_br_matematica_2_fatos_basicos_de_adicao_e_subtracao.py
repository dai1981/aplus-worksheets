# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Fatos básicos de adição e subtração (Números, EF02MA05)
  python3 tools/gen_br_matematica_2_fatos_basicos_de_adicao_e_subtracao.py
Somas e subtrações até 20; pares que formam 10; dobros e quase dobros; passar pelo 10 (8 + 5 = 8 + 2 + 3);
família de fatos (7 + 5 = 12, 12 − 5 = 7); dezenas exatas (30 + 40, 70 − 20); cálculo mental com o fato básico.
Usa geradores do 3º ano (cálculo mental) com outro sorteio.
Erros: contar o primeiro número de novo, errar a subtração por não pensar na adição, trocar 7 + 5 por 7 + 6 nos quase dobros.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, lim
from br_common import relabel, fig, coisas, KINDS
import k_pics

R = random.Random(80205)
M3 = "gen_br_matematica_3_calculo_mental"
c_fatos, c_completar = use(M3, 80901, "s1_fatos", "s1_completar", preds=(lim(100, 0),))


def s1_soma():
    a, b = R.randint(2, 9), R.randint(2, 9)
    s = a + b
    if R.random() < 0.4:
        kind = R.choice(KINDS)
        pic = fig(relabel(k_pics.two_groups_svg(a, kind, b, kind, "+"), "%s mais %s" % (coisas(kind, a), coisas(kind, b))))
        return mcq(pic + "Quanto é %d + %d?" % (a, b), str(s), [str(s + 1), str(s - 1), str(abs(a - b)) if a != b else str(s + 2)], "%d + %d = <b>%d</b>." % (a, b, s))
    return mcq("Quanto é %d + %d?" % (a, b), str(s), [str(s + 1), str(s - 1), str(s + 10) if s < 10 else str(s - 10)],
               ("Passe pelo 10: %d + %d = 10, e mais %d = <b>%d</b>." % (max(a, b), 10 - max(a, b), s - 10, s)) if s > 10 else "%d + %d = <b>%d</b>." % (a, b, s))


def s1_sub():
    a, b = R.randint(2, 9), R.randint(2, 9)
    s = a + b
    return mcq("Quanto é %d − %d?" % (s, a), str(b), [str(b + 1), str(b - 1), str(s + a) if s + a < 20 else str(b + 2)],
               "Pense na adição: %d + ___ = %d. Resposta: <b>%d</b>." % (a, s, b))


def s2_dez():
    a = R.randint(1, 9)
    k = R.choice(["falta", "par", "soma3"])
    if k == "falta":
        return mcq("Complete: %d + ___ = 10" % a, str(10 - a), [str(a), str(11 - a), str(9 - a) if a < 9 else "2"], "%d + %d = 10. Resposta: <b>%d</b>." % (a, 10 - a, 10 - a))
    if k == "par":
        opts = ["%d + %d" % (a, 10 - a), "%d + %d" % (a, 11 - a), "%d + %d" % (a, 9 - a) if a < 9 else "9 + 2", "%d + %d" % (a + 1, 10 - a) if a < 9 else "8 + 3"]
        return mcq("Qual destas somas dá exatamente 10?", opts[0], opts[1:], "<b>%s</b> = 10." % opts[0])
    b = R.randint(1, 9)
    c = 10 - a
    if b in (a, c):
        return None
    return mcq("Calcule %d + %d + %d (dica: junte primeiro os que dão 10)." % (a, b, c), str(10 + b), [str(10 + b + 1), str(a + b + c - 1), str(b + 9)],
               "%d + %d = 10; 10 + %d = <b>%d</b>." % (a, c, b, 10 + b))


def s2_dobro():
    a = R.randint(2, 10)
    k = R.choice(["dobro", "quase", "quase"])
    if k == "dobro":
        return mcq("Quanto é %d + %d?" % (a, a), str(2 * a), [str(2 * a + 1), str(2 * a - 1), str(a + 2)], "Dobro de %d: <b>%d</b>." % (a, 2 * a))
    b = a + 1
    return mcq("Quanto é %d + %d? (dica: %d + %d = %d)" % (a, b, a, a, 2 * a), str(2 * a + 1), [str(2 * a), str(2 * a + 2), str(2 * b + 1)],
               "%d + %d é o dobro de %d mais 1: %d + 1 = <b>%d</b>." % (a, b, a, 2 * a, 2 * a + 1))


def s3_familia():
    a, b = R.randint(3, 9), R.randint(3, 9)
    if a == b:
        return None
    s = a + b
    k = R.choice(["sub", "add", "qual"])
    if k == "sub":
        return mcq("Se %d + %d = %d, então %d − %d = ___" % (a, b, s, s, b), str(a), [str(b), str(s), str(a + 1)], "A subtração desfaz a adição: %d − %d = <b>%d</b>." % (s, b, a))
    if k == "add":
        return mcq("Se %d − %d = %d, então %d + %d = ___" % (s, a, b, b, a), str(s), [str(b - a) if b > a else str(a - b + 10), str(s + 1), str(a)],
                   "%d + %d volta para o número do começo: <b>%d</b>." % (b, a, s))
    ok = "%d − %d = %d" % (s, a, b)
    return mcq("Qual conta é da mesma família de %d + %d = %d?" % (a, b, s), ok, ["%d − %d = %d" % (s, a + 1, b), "%d + %d = %d" % (a, s, a + s), "%d − %d = %d" % (a + b + 1, a, b)],
               "Com os números %d, %d e %d: <b>%s</b>." % (a, b, s, ok))


def s3_falta():
    a, b = R.randint(2, 9), R.randint(2, 9)
    s = a + b
    if R.random() < 0.5:
        return mcq("Complete: %d + ___ = %d" % (a, s), str(b), [str(s), str(b + 1), str(s + a) if s + a < 20 else str(b - 1)], "%d + %d = %d. Resposta: <b>%d</b>." % (a, b, s, b))
    return mcq("Complete: %d − ___ = %d" % (s, a), str(b), [str(s), str(b + 1), str(a)], "%d − %d = %d. Resposta: <b>%d</b>." % (s, b, a, b))


def s4_dezenas():
    a, b = R.randint(1, 8), R.randint(1, 8)
    if R.random() < 0.5:
        if a + b > 10:
            return None
        return mcq("Quanto é %d + %d?" % (10 * a, 10 * b), str(10 * (a + b)), [str(a + b), str(10 * (a + b) + 10), str(10 * (a + b) - 10)],
                   "%d dezenas + %d dezenas = %d dezenas = <b>%d</b>. (Como %d + %d = %d.)" % (a, b, a + b, 10 * (a + b), a, b, a + b))
    s = a + b
    if s > 10:
        return None
    return mcq("Quanto é %d − %d?" % (10 * s, 10 * a), str(10 * b), [str(b), str(10 * b + 10), str(10 * s + 10 * a) if 10 * s + 10 * a <= 100 else str(10 * b - 10)],
               "%d dezenas − %d dezenas = <b>%d</b>. (Como %d − %d = %d.)" % (s, a, 10 * b, s, a, b))


def s4_usar():
    a, b = R.randint(2, 9), R.randint(2, 9)
    t = R.randint(1, 7) * 10
    if a + b >= 10:
        return None
    return mcq("Sabendo que %d + %d = %d, quanto é %d + %d?" % (a, b, a + b, t + a, b), str(t + a + b), [str(t + a + b + 10), str(a + b), str(t + a + b - 1)],
               "%d + %d = %d, e %s continua%s: <b>%d</b>." % (a, b, a + b, "a 1 dezena" if t == 10 else "as %d dezenas" % (t // 10), "" if t == 10 else "m", t + a + b))


def s5_problema():
    k = R.choice(["balas", "passaros", "pontos", "lapis", "carrinhos", "peixes"])
    a, b = R.randint(3, 9), R.randint(3, 9)
    s = a + b
    if k == "balas":
        return mcq("Rui tinha %d balas e ganhou %d. Com quantas ficou?" % (a, b), str(s), [str(s + 1), str(abs(a - b)) if a != b else str(s - 1), str(s - 1)], "%d + %d = <b>%d</b>." % (a, b, s))
    if k == "passaros":
        return mcq("Havia %d passarinhos no fio. Voaram %d. Quantos ficaram?" % (s, a), str(b), [str(s), str(b + 1), str(b - 1)], "%d − %d = <b>%d</b>." % (s, a, b))
    if k == "pontos":
        return mcq("Ana fez %d pontos na 1ª rodada e %d na 2ª. Quantos pontos fez ao todo?" % (a, b), str(s), [str(s - 1), str(s + 1), str(a * b) if a * b != s else str(s + 2)], "%d + %d = <b>%d</b>." % (a, b, s))
    if k == "lapis":
        return mcq("Um estojo tem %d lápis. %d são azuis e o resto é vermelho. Quantos são vermelhos?" % (s, a), str(b), [str(s), str(b + 1), str(a)], "%d − %d = <b>%d</b>." % (s, a, b))
    if k == "carrinhos":
        return mcq("Téo tem %d carrinhos. Quantos faltam para ele ter %d?" % (a, s), str(b), [str(s), str(b - 1), str(b + 1)], "%d + ___ = %d. Faltam <b>%d</b>." % (a, s, b))
    return mcq("No aquário há %d peixes vermelhos e %d amarelos. Quantos peixes há?" % (a, b), str(s), [str(s - 1), str(s + 1), str(s + 10)], "%d + %d = <b>%d</b>." % (a, b, s))


def main():
    seen = set()
    sets = [
        ("Somar e subtrair até 20", mix(R, seen, [(s1_soma, 10), (s1_sub, 6), (c_fatos, 4)])),
        ("Formar 10 e dobros", mix(R, seen, [(s2_dez, 10), (s2_dobro, 6), (c_completar, 4)])),
        ("Família de fatos", mix(R, seen, [(s3_familia, 10), (s3_falta, 10)])),
        ("Dezenas exatas", mix(R, seen, [(s4_dezenas, 12), (s4_usar, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Os <b>fatos básicos</b> são as contas com números de 0 a 10, como 7 + 5 e 12 − 5. Saber de cor ajuda em todas as outras contas.",
         "Para passar do 10, complete o 10 primeiro: 8 + 5 = 8 + 2 + 3 = 13.",
         "Use os <b>dobros</b>: 6 + 6 = 12, então 6 + 7 = 13.",
         "A subtração desfaz a adição: se 7 + 5 = 12, então 12 − 5 = 7 e 12 − 7 = 5."],
        [("9 + 6", ["9 + 1 = 10", "10 + 5"], "15"),
         ("50 − 20", ["5 dezenas − 2 dezenas = 3 dezenas"], "30")],
        [["Contar o 8 de novo: 8 + 3 → 8, 9, 10", "Comece depois do 8: 9, 10, 11. 8 + 3 = 11."],
         ["Errar a subtração", "Pense na adição: 5 + ___ = 12."],
         ["Esquecer o zero nas dezenas exatas", "30 + 40 = 70, não 7."]],
        fig(relabel(k_pics.two_groups_svg(8, "apple", 5, "apple", "+"), "8 maçãs mais 5 maçãs")))
    faq = [("O que são fatos básicos?", "São as adições e subtrações com números de um algarismo (como 6 + 7 e 13 − 6). A BNCC pede que o 2º ano construa esses fatos e os use no cálculo mental e escrito."),
           ("Como decorar os fatos básicos?", "Brinque um pouco todo dia com cartas ou dados: primeiro os pares que formam 10, depois os dobros e por fim os quase dobros.")]
    make_unit(R, "fatos-basicos-de-adicao-e-subtracao", "N", ["EF02MA05"],
              "Construir fatos básicos da adição e subtração e utilizá-los no cálculo mental ou escrito",
              "Fatos básicos de adição e subtração", "Fatos básicos",
              "Atividades de matemática para o 2º ano sobre fatos básicos de adição e subtração: somas até 20, pares que formam 10, dobros, família de fatos e dezenas exatas. 100 exercícios com gabarito.",
              "Complete o 10 primeiro.", "Se 7 + 5 = 12, então 12 − 5 = 7.",
              body, faq, sets, 5, grade="2-ano")


if __name__ == "__main__":
    main()
