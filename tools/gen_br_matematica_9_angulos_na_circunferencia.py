# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Ângulos na circunferência (Geometria, EF09MA11)
  python3 tools/gen_br_matematica_9_angulos_na_circunferencia.py
Ângulo central e arco; ângulo inscrito = metade do central (mesmo arco); inscrito no semicírculo = 90°;
inscritos no mesmo arco são iguais; quadrilátero inscrito (opostos somam 180°); tangente e raio; arcos e polígonos regulares.
Erros: achar que o inscrito é igual ao central, ou o dobro; esquecer que a circunferência tem 360°.
"""
import random
from br_common import lesson, mix
from br_9 import M, circulo, unit

R = random.Random(89011)


def pts(c):
    a, b = 270 - c / 2.0, 270 + c / 2.0
    top = R.uniform(b + 25 - 360, a - 25) if c < 180 else 90
    return {"A": a, "B": b, "C": top}


def s1_insc():
    c = R.choice(range(60, 172, 4))
    P = pts(c)
    k = R.choice(["ins", "cen"])
    if k == "ins":
        pic = circulo(P, [("A", "C"), ("B", "C"), ("O", "A"), ("O", "B")], arcs=[("O", "A", "B", "%d°" % c), ("C", "A", "B", "x")])
        return M(pic + "O é o centro da circunferência. O ângulo central AÔB mede %d°. Quanto mede o ângulo inscrito x?" % c, "%d°" % (c // 2), ["%d°" % c, "%d°" % (2 * c) if 2 * c < 360 else "%d°" % (180 - c // 2), "%d°" % (180 - c), "%d°" % (360 - c)],
                     "O ângulo inscrito é a metade do central que vê o mesmo arco: %d ÷ 2 = <b>%d°</b>." % (c, c // 2))
    pic = circulo(P, [("A", "C"), ("B", "C"), ("O", "A"), ("O", "B")], arcs=[("O", "A", "B", "x"), ("C", "A", "B", "%d°" % (c // 2))])
    return M(pic + "O é o centro. O ângulo inscrito AĈB mede %d°. Quanto mede o ângulo central x?" % (c // 2), "%d°" % c, ["%d°" % (c // 2), "%d°" % (c // 4) if c % 4 == 0 else "%d°" % (c + 10), "%d°" % (180 - c // 2), "%d°" % (360 - c)],
             "O central é o dobro do inscrito: 2 · %d = <b>%d°</b>." % (c // 2, c))


def s2_arco():
    k = R.choice(["arco", "insc_arco", "fracao"])
    if k == "arco":
        c = R.choice(range(40, 180, 5))
        return M("Um ângulo central mede %d°. Quanto mede o arco correspondente?" % c, "%d°" % c, ["%d°" % (c * 2), "%s°" % (c // 2) if c % 2 == 0 else "%d°" % (c + 5), "%d°" % (360 - c)],
                 "O arco tem a mesma medida do ângulo central: <b>%d°</b>." % c)
    if k == "insc_arco":
        a = R.choice(range(40, 300, 10))
        return M("Um ângulo inscrito vê um arco de %d°. Quanto mede o ângulo inscrito?" % a, "%d°" % (a // 2), ["%d°" % a, "%d°" % (2 * a) if 2 * a < 360 else "%d°" % (180 - a // 2), "%d°" % (360 - a)],
                 "Inscrito = metade do arco: <b>%d°</b>." % (a // 2))
    n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
    return M("Uma circunferência é dividida em %d arcos iguais. Quanto mede cada ângulo central?" % n, "%d°" % (360 // n), ["%d°" % (180 // n) if 180 % n == 0 else "%d°" % (360 // n + 10), "%d°" % (360 * n) if n < 4 else "%d°" % (360 // n * 2), "%d°" % (180 - 360 // n)],
             "360° ÷ %d = <b>%d°</b>." % (n, 360 // n))


def s3_semi():
    k = R.choice(["semi", "mesmo", "semi_outro"])
    if k == "semi":
        t = R.uniform(30, 150)
        pic = circulo({"A": 180, "B": 0, "C": t}, [("A", "B"), ("A", "C"), ("B", "C")], arcs=[("C", "A", "B", "x")])
        return M(pic + "AB é um diâmetro e C está na circunferência. Quanto mede o ângulo x?", "90°", ["180°", "45°", "60°", "depende de onde está C"],
                 "O ângulo inscrito vê uma semicircunferência (180°), então mede <b>90°</b>.")
    if k == "semi_outro":
        a = R.choice(range(20, 71, 2))
        t = 180 - 2 * a
        pic = circulo({"A": 180, "B": 0, "C": t}, [("A", "B"), ("A", "C"), ("B", "C")], arcs=[("A", "B", "C", "%d°" % a), ("B", "C", "A", "x")])
        return M(pic + "AB é um diâmetro. O ângulo em A mede %d°. Quanto mede o ângulo x, em B?" % a, "%d°" % (90 - a), ["%d°" % a, "%d°" % (180 - a), "%d°" % (180 - 2 * a), "%d°" % (90 + a)],
                 "O ângulo em C é 90°; então x = 180 − 90 − %d = <b>%d°</b>." % (a, 90 - a))
    c = R.choice(range(60, 160, 4))
    a, b = 270 - c / 2.0, 270 + c / 2.0
    t1, t2 = R.uniform(b + 20 - 360, 60), R.uniform(120, a - 20)
    pic = circulo({"A": a, "B": b, "C": t1, "D": t2}, [("A", "C"), ("B", "C"), ("A", "D"), ("B", "D")], center=False, arcs=[("D", "A", "B", "%d°" % (c // 2)), ("C", "A", "B", "x")], label="circunferência com pontos A, B, C e D")
    return M(pic + "C e D estão no mesmo arco. O ângulo AD̂B mede %d°. Quanto mede x = AĈB?" % (c // 2), "%d°" % (c // 2), ["%d°" % c, "%d°" % (180 - c // 2), "%d°" % (90 - c // 2), "%d°" % (c // 2 + 10)],
             "Ângulos inscritos que veem o mesmo arco são iguais: <b>%d°</b>." % (c // 2))


def s4_quad():
    k = R.choice(["quad", "quad", "tang"])
    if k == "quad":
        a = R.choice(range(64, 128, 2))
        tA = R.uniform(60, 130)
        o = tA + 180
        P = {"A": tA, "B": o - a, "C": o + R.uniform(-a + 25, a - 25), "D": o + a}
        pic = circulo(P, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], center=False, arcs=[("A", "D", "B", "%d°" % a), ("C", "B", "D", "x")], label="quadrilátero ABCD inscrito numa circunferência")
        return M(pic + "ABCD está inscrito na circunferência. O ângulo em A mede %d°. Quanto mede x, o ângulo em C?" % a, "%d°" % (180 - a), ["%d°" % a, "%d°" % (360 - a), "%d°" % (90 - a // 2), "%d°" % (2 * a) if 2 * a < 360 else "%d°" % (a // 2)],
                     "Num quadrilátero inscrito, ângulos opostos somam 180°: 180 − %d = <b>%d°</b>." % (a, 180 - a))
    a = R.choice(range(20, 80, 2))
    return M("Uma reta é tangente a uma circunferência no ponto T, e O é o centro. A corda TA faz %d° com o raio OT. Quanto mede o ângulo entre a corda TA e a tangente?" % a, "%d°" % (90 - a),
             ["%d°" % a, "%d°" % (180 - a), "%d°" % (90 + a), "%d°" % (2 * a)], "A tangente é perpendicular ao raio (90°): 90 − %d = <b>%d°</b>." % (a, 90 - a))


def s5_teoria():
    q, a, w = R.choice([
        ("O ângulo inscrito que vê o mesmo arco que um ângulo central mede…", "a metade do central", ["o mesmo que o central", "o dobro do central", "180° menos o central"]),
        ("Um ângulo inscrito numa semicircunferência é…", "reto (90°)", ["agudo", "obtuso", "raso (180°)"]),
        ("Num quadrilátero inscrito numa circunferência, dois ângulos opostos…", "somam 180°", ["são iguais", "somam 90°", "somam 360°"]),
        ("A reta tangente a uma circunferência é, em relação ao raio no ponto de tangência,…", "perpendicular", ["paralela", "oblíqua com 45°", "igual ao diâmetro"]),
        ("Dois ângulos inscritos que veem o mesmo arco são…", "iguais", ["suplementares", "complementares", "um o dobro do outro"]),
        ("O ângulo central de um hexágono regular inscrito mede…", "60°", ["120°", "90°", "30°"]),
        ("O ângulo central de um quadrado inscrito mede…", "90°", ["45°", "60°", "180°"]),
        ("O vértice de um ângulo inscrito fica…", "sobre a circunferência", ["no centro", "fora da circunferência", "no meio de uma corda"]),
        ("O vértice de um ângulo central fica…", "no centro da circunferência", ["sobre a circunferência", "fora da circunferência", "em qualquer ponto"]),
        ("Um ângulo inscrito mede 35°. O arco que ele vê mede…", "70°", ["35°", "17,5°", "145°"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Ângulo central e ângulo inscrito", mix(R, seen, [(s1_insc, 20)])),
        ("Arcos e ângulos", mix(R, seen, [(s2_arco, 14), (s5_teoria, 6)])),
        ("Semicircunferência e mesmo arco", mix(R, seen, [(s3_semi, 20)])),
        ("Quadrilátero inscrito e tangente", mix(R, seen, [(s4_quad, 16), (s5_teoria, 4)])),
        ("Revisão", mix(R, seen, [(s1_insc, 8), (s3_semi, 6), (s4_quad, 6)])),
    ]
    body = lesson(
        ["O <b>ângulo central</b> tem o vértice no centro; ele mede o mesmo que o arco que vê.",
         "O <b>ângulo inscrito</b> tem o vértice sobre a circunferência; ele mede <b>a metade</b> do arco (e do central) que vê.",
         "Consequências: um inscrito numa semicircunferência mede 90°; inscritos que veem o mesmo arco são iguais; num quadrilátero inscrito, ângulos opostos somam 180°."],
        [("Central de 110°", ["110 ÷ 2"], "inscrito de 55°"),
         ("Quadrilátero inscrito com ângulo de 75°", ["180 − 75"], "oposto de 105°")],
        [["Achar que o inscrito é igual ao central", "O inscrito é a metade."],
         ["Fazer o dobro em vez da metade", "Do central para o inscrito, divida por 2."],
         ["Esquecer que a volta inteira tem 360°", "Arcos iguais: 360° ÷ número de partes."]],
        circulo({"A": 215, "B": 325, "C": 100}, [("A", "C"), ("B", "C"), ("O", "A"), ("O", "B")], arcs=[("O", "A", "B", "110°"), ("C", "A", "B", "55°")]))
    faq = [("Qual é a relação entre ângulo central e ângulo inscrito?", "Quando os dois veem o mesmo arco, o ângulo inscrito mede a metade do ângulo central."),
           ("O que a BNCC pede no 9º ano?", "Resolver problemas por meio do estabelecimento de relações entre arcos, ângulos centrais e ângulos inscritos na circunferência (EF09MA11).")]
    unit(R, "angulos-na-circunferencia", "G", ["EF09MA11"],
         "Resolver problemas por meio do estabelecimento de relações entre arcos, ângulos centrais e ângulos inscritos na circunferência, fazendo uso, inclusive, de softwares de geometria dinâmica",
         "Ângulos na circunferência: central e inscrito", "Ângulos na circunferência",
         "Atividades de matemática para o 9º ano sobre ângulos na circunferência: ângulo central, ângulo inscrito, arcos, semicircunferência, quadrilátero inscrito e tangente. 100 exercícios com gabarito.",
         "Ângulo inscrito = metade do central.", "Inscrito na semicircunferência = 90°.",
         body, faq, sets, 11)


if __name__ == "__main__":
    main()
