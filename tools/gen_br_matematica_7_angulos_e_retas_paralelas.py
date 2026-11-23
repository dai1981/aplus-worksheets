# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Ângulos e retas paralelas cortadas por uma transversal (Geometria, EF07MA23)
  python3 tools/gen_br_matematica_7_angulos_e_retas_paralelas.py
Ângulos complementares, suplementares e opostos pelo vértice; ângulos formados por duas paralelas e uma transversal
(correspondentes, alternos, colaterais); calcular ângulos e resolver equações simples.
Usa geradores do 9º ano (ângulos e retas paralelas) com outro sorteio.
Erros: confundir complementar (90°) com suplementar (180°), achar que colaterais são iguais.
"""
import random
from br_common import lesson, mix, use
from br_9 import M, d, paralelas, unit

R = random.Random(87012)
a_nome, a_valor, a_eq, a_teoria = use("gen_br_matematica_9_angulos_e_retas_paralelas", 87912, "s1_nome", "s2_valor", "s3_equacao", "s4_teoria")


def s1_comp_supl():
    a = R.randint(5, 85) if R.random() < 0.5 else R.randint(5, 175)
    k = R.choice(["comp", "supl"]) if a < 90 else "supl"
    r = 90 - a if k == "comp" else 180 - a
    return M("Qual é o %s de um ângulo de %d°?" % ("complemento" if k == "comp" else "suplemento", a), "%d°" % r, ["%d°" % (180 - a if k == "comp" else 90 - a) if (k == "comp" or a < 90) else "%d°" % (360 - a), "%d°" % a, "%d°" % (r + 10)],
             "%s somam %d°: %d − %d = <b>%d°</b>." % ("Complementares" if k == "comp" else "Suplementares", 90 if k == "comp" else 180, 90 if k == "comp" else 180, a, r))


def s2_opv():
    a = R.choice(range(25, 156, 5))
    alpha = a if a < 90 else 180 - a
    pos = "tr" if a < 90 else "tl"
    k = R.choice(["opv", "adj"])
    if k == "opv":
        pic = paralelas(alpha, {(0, pos): "%d°" % a, (0, "bl" if pos == "tr" else "br"): "x"}, label="duas retas que se cruzam")
        return M(pic + "Quanto mede x? (Olhe só o cruzamento de cima.)", "%d°" % a, ["%d°" % (180 - a), "%d°" % (90 - a) if a < 90 else "%d°" % (a - 90), "%d°" % (360 - a)],
                 "Ângulos opostos pelo vértice são iguais: <b>x = %d°</b>." % a)
    pic = paralelas(alpha, {(0, pos): "%d°" % a, (0, "tl" if pos == "tr" else "tr"): "x"}, label="duas retas que se cruzam")
    return M(pic + "Quanto mede x? (Olhe só o cruzamento de cima.)", "%d°" % (180 - a), ["%d°" % a, "%d°" % (90 - a) if a < 90 else "%d°" % (a - 90), "%d°" % (360 - a)],
             "Ângulos adjacentes numa reta somam 180°: 180 − %d = <b>%d°</b>." % (a, 180 - a))


def s3_eq_simples():
    x = R.randint(10, 40)
    k = R.choice(["comp", "supl", "opv"])
    if k == "comp":
        a, b = R.choice([(2, 1), (3, 2), (1, 2), (4, 1)])
        if (a + b) * x >= 90 or 90 - (a + b) * x <= 0:
            return None
        c = 90 - (a + b) * x
        return M("Dois ângulos complementares medem %sx e %sx + %d°. Quanto vale x?" % ("" if a == 1 else a, "" if b == 1 else b, c), "%d°" % x, ["%d°" % ((180 - c) // (a + b)) if (180 - c) % (a + b) == 0 else "%d°" % (x + 5), "%d°" % (90 - c), "%d°" % (x * 2)],
                 "%sx + %sx + %d = 90 → %dx = %d → <b>x = %d°</b>." % ("" if a == 1 else a, "" if b == 1 else b, c, a + b, 90 - c, x))
    if k == "supl":
        a, b = R.choice([(2, 1), (3, 1), (2, 3), (4, 1), (3, 2)])
        c = 180 - (a + b) * x
        if c <= 0:
            return None
        return M("Dois ângulos suplementares medem %sx e %sx + %d°. Quanto vale x?" % ("" if a == 1 else a, "" if b == 1 else b, c), "%d°" % x, ["%d°" % ((90 - c) // (a + b)) if c < 90 and (90 - c) % (a + b) == 0 else "%d°" % (x + 5), "%d°" % (180 - c), "%d°" % (x * 2)],
                 "%sx + %sx + %d = 180 → %dx = %d → <b>x = %d°</b>." % ("" if a == 1 else a, "" if b == 1 else b, c, a + b, 180 - c, x))
    a, b = R.choice([(3, 2), (4, 3), (5, 2), (2, 1), (5, 3)])
    c = R.randint(5, 30)
    e = (a - b) * x + c
    return M("Dois ângulos opostos pelo vértice medem %dx + %d° e %sx + %d°. Quanto vale x?" % (b, e, "" if a == 1 else a, c), "%d°" % x, ["%d°" % (b * x + e), "%d°" % (x + 4), "%d°" % ((e + c) // (a - b)) if (e + c) % (a - b) == 0 else "%d°" % (x * 2)],
             "Opostos pelo vértice são iguais: %sx + %d = %dx + %d → %dx = %d → <b>x = %d°</b>." % ("" if a == 1 else a, c, b, e, a - b, e - c, x))


def main():
    seen = set()
    sets = [
        ("Complementares e suplementares", mix(R, seen, [(s1_comp_supl, 20)])),
        ("Opostos pelo vértice e adjacentes", mix(R, seen, [(s2_opv, 20)])),
        ("Paralelas e transversal", mix(R, seen, [(a_nome, 10), (a_teoria, 4), (a_valor, 6)])),
        ("Achar o ângulo", mix(R, seen, [(a_valor, 20)])),
        ("Equações com ângulos", mix(R, seen, [(s3_eq_simples, 10), (a_eq, 10)])),
    ]
    body = lesson(
        ["Ângulos <b>complementares</b> somam 90°; <b>suplementares</b> somam 180°.",
         "Quando duas retas se cruzam, os ângulos <b>opostos pelo vértice</b> são iguais e os adjacentes somam 180°.",
         "Com duas <b>paralelas</b> cortadas por uma transversal: correspondentes, alternos internos e alternos externos são iguais; colaterais somam 180°."],
        [("Suplemento de 65°", ["180 − 65"], "115°"),
         ("Opostos: 3x + 10 e 5x − 30", ["3x + 10 = 5x − 30", "40 = 2x"], "x = 20°")],
        [["Confundir complemento e suplemento", "Complemento: 90°. Suplemento: 180°."],
         ["Achar que colaterais são iguais", "Colaterais somam 180°."],
         ["Esquecer que opostos pelo vértice são iguais", "Não precisa medir: são iguais."]],
        paralelas(60, {(0, "tr"): "60°", (1, "tr"): "60°", (1, "bl"): "60°"}))
    faq = [("O que são ângulos opostos pelo vértice?", "São os ângulos que ficam um em frente ao outro quando duas retas se cruzam. Eles têm sempre a mesma medida."),
           ("O que a BNCC pede no 7º ano?", "Verificar relações entre os ângulos formados por retas paralelas cortadas por uma transversal, com e sem uso de softwares de geometria dinâmica (EF07MA23).")]
    unit(R, "angulos-e-retas-paralelas", "G", ["EF07MA23"],
         "Verificar relações entre os ângulos formados por retas paralelas cortadas por uma transversal, com e sem uso de softwares de geometria dinâmica",
         "Ângulos: complementares, suplementares e retas paralelas", "Ângulos e retas paralelas",
         "Atividades de matemática para o 7º ano sobre ângulos: complementares, suplementares, opostos pelo vértice e ângulos formados por retas paralelas cortadas por uma transversal, com equações. 100 exercícios com gabarito.",
         "Complementares: 90°. Suplementares: 180°.", "Opostos pelo vértice são iguais.",
         body, faq, sets, 12, grade="7-ano")


if __name__ == "__main__":
    main()
