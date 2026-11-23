# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Ângulos formados por retas paralelas e uma transversal (Geometria, EF09MA10)
  python3 tools/gen_br_matematica_9_angulos_e_retas_paralelas.py
Ângulos correspondentes, alternos internos, alternos externos, colaterais internos e opostos pelo vértice;
achar ângulos pela figura; equações (3x + 10 e 5x − 30); a soma dos ângulos do triângulo usando paralelas.
Erros: achar que colaterais são iguais (somam 180°), confundir alternos com correspondentes.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, expr, paralelas, unit

R = random.Random(89010)
P4 = ["tr", "tl", "bl", "br"]


def val(alpha, p):
    return alpha if p in ("tr", "bl") else 180 - alpha


def rel(i1, p1, i2, p2):
    if i1 == i2:
        if {p1, p2} in ({"tr", "bl"}, {"tl", "br"}):
            return "opostos pelo vértice"
        return "adjacentes suplementares"
    if p1 == p2:
        return "correspondentes"
    up, lo = (p1, p2) if i1 == 0 else (p2, p1)
    if (up, lo) in (("bl", "tr"), ("br", "tl")):
        return "alternos internos"
    if (up, lo) in (("tl", "br"), ("tr", "bl")):
        return "alternos externos"
    if (up, lo) in (("bl", "tl"), ("br", "tr")):
        return "colaterais internos"
    if (up, lo) in (("tl", "bl"), ("tr", "br")):
        return "colaterais externos"
    return None


def s1_nome():
    alpha = R.choice([50, 55, 60, 65, 70, 75])
    while True:
        i1, p1, i2, p2 = 0, R.choice(P4), 1, R.choice(P4)
        r = rel(i1, p1, i2, p2)
        if r:
            break
    pic = paralelas(alpha, {(i1, p1): "a", (i2, p2): "b"})
    return M(pic + "As retas r e s são paralelas. Como se chamam os ângulos a e b?", r,
             [x for x in ["correspondentes", "alternos internos", "alternos externos", "colaterais internos", "colaterais externos"] if x != r],
             "Veja a posição de a e b em relação às paralelas e à transversal: são <b>%s</b>." % r)


def s2_valor():
    alpha = R.choice([40, 45, 50, 55, 60, 65, 70, 72, 75, 80])
    while True:
        i1, p1 = R.choice([0, 1]), R.choice(P4)
        i2, p2 = R.choice([0, 1]), R.choice(P4)
        if (i1, p1) != (i2, p2):
            break
    v1, v2 = val(alpha, p1), val(alpha, p2)
    r = rel(i1, p1, i2, p2)
    if r is None:
        return None
    pic = paralelas(alpha, {(i1, p1): "%d°" % v1, (i2, p2): "x"})
    why = "Os ângulos x e %d° são %s, então %s" % (v1, r, "são iguais" if v1 == v2 else "somam 180°")
    return M(pic + "As retas r e s são paralelas. Quanto mede x?", "%d°" % v2, ["%d°" % (180 - v2), "%d°" % (90 - v2) if v2 < 90 else "%d°" % (v2 - 90), "%d°" % (360 - v2), "%d°" % (v2 + 10)],
             "%s. <b>x = %d°</b>." % (why, v2))


def s3_equacao():
    alpha = R.choice([40, 50, 60, 70, 80])
    kind = R.choice(["igual", "supl"])
    if kind == "igual":
        ps = R.choice([((0, "tr"), (1, "tr")), ((0, "bl"), (1, "tr")), ((0, "br"), (1, "tl")), ((0, "tl"), (1, "br"))])
        x = R.randint(10, 30)
        a, b = R.choice([(2, 3), (3, 5), (2, 4), (3, 4), (4, 5)])
        v = val(alpha, ps[0][1])
        c1 = v - a * x
        c2 = v - b * x
        e1, e2 = expr([(a, "x"), (c1, "")]), expr([(b, "x"), (c2, "")])
        pic = paralelas(alpha, {ps[0]: e1, ps[1]: e2})
        return M(pic + "As retas r e s são paralelas. Qual é o valor de x?", "%d°" % x, ["%d°" % v, "%d°" % (x + 5), "%d°" % abs(c1 - c2), "%d°" % (180 - v)],
                 "Os ângulos são %s, então são iguais: %s = %s → %dx = %s → <b>x = %d°</b>." % (rel(ps[0][0], ps[0][1], ps[1][0], ps[1][1]), e1, e2, b - a, d(c1 - c2), x))
    ps = R.choice([((0, "bl"), (1, "tl")), ((0, "br"), (1, "tr"))])
    v1 = val(alpha, ps[0][1])
    v2 = 180 - v1
    a = R.choice([2, 3, 4])
    x = R.randint(10, 25)
    c1 = v1 - a * x
    b = R.choice([1, 2, 3])
    c2 = v2 - b * x
    e1, e2 = expr([(a, "x"), (c1, "")]), expr([(b, "x"), (c2, "")])
    pic = paralelas(alpha, {ps[0]: e1, ps[1]: e2})
    return M(pic + "As retas r e s são paralelas. Qual é o valor de x?", "%d°" % x, ["%d°" % v1, "%s°" % d((180 - c1 - c2) // (a + b) + 3), "%d°" % v2, "%d°" % (x + 10)],
             "Colaterais internos somam 180°: %s + %s = 180 → %dx = %d → <b>x = %d°</b>." % (e1, e2, a + b, 180 - c1 - c2, x))


def s4_teoria():
    q, a, w = R.choice([
        ("Ângulos correspondentes formados por duas paralelas e uma transversal são…", "iguais (congruentes)", ["suplementares", "complementares", "sempre retos"]),
        ("Ângulos alternos internos formados por duas paralelas e uma transversal são…", "iguais (congruentes)", ["suplementares", "complementares", "sempre agudos"]),
        ("Ângulos colaterais internos formados por duas paralelas e uma transversal são…", "suplementares (somam 180°)", ["iguais", "complementares (somam 90°)", "sempre retos"]),
        ("Ângulos opostos pelo vértice são…", "iguais", ["suplementares", "complementares", "sempre obtusos"]),
        ("Se dois ângulos alternos internos são iguais, as retas cortadas pela transversal são…", "paralelas", ["perpendiculares", "concorrentes no mesmo ponto", "iguais à transversal"]),
        ("Uma transversal corta duas paralelas formando um ângulo de 90°. Os outros sete ângulos medem…", "90°", ["45°", "180°", "alguns 90° e outros 45°"]),
        ("Para mostrar que a soma dos ângulos internos de um triângulo é 180°, traçamos por um vértice…", "uma reta paralela ao lado oposto", ["uma reta perpendicular ao lado oposto", "a bissetriz do ângulo", "um círculo"]),
        ("Os ângulos colaterais internos ficam…", "do mesmo lado da transversal, entre as paralelas", ["em lados opostos da transversal, entre as paralelas", "fora das paralelas", "no mesmo vértice"]),
        ("Os ângulos alternos externos ficam…", "em lados opostos da transversal, fora das paralelas", ["do mesmo lado da transversal, entre as paralelas", "entre as paralelas", "no mesmo vértice"]),
        ("Dois ângulos colaterais internos medem 3x e 2x. Quanto vale x?", "36°", ["18°", "72°", "45°"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def s5_triangulo():
    a, b = R.choice([(40, 60), (50, 70), (35, 65), (55, 45), (30, 80), (62, 48), (75, 45)])
    k = R.choice(["tri", "zz"])
    if k == "tri":
        c = 180 - a - b
        return M("Num triângulo, dois ângulos medem %d° e %d°. Traçando uma paralela a um lado e usando ângulos alternos internos, quanto mede o terceiro ângulo?" % (a, b), "%d°" % c, ["%d°" % (a + b), "%d°" % (360 - a - b), "%d°" % (c + 10), "%d°" % (180 - a), "%d°" % (180 - b)],
                 "Os três ângulos formam um ângulo raso: %d + %d + x = 180 → <b>x = %d°</b>." % (a, b, c))
    return M("Num triângulo, dois ângulos internos medem %d° e %d°. Quanto mede o ângulo externo junto ao terceiro vértice?" % (a, b),
             "%d°" % (a + b), ["%d°" % (180 - a - b), "%d°" % abs(a - b), "%d°" % (360 - a - b), "%d°" % (180 - a)],
             "O ângulo externo é igual à soma dos dois internos não adjacentes (prova com uma paralela): <b>%d°</b>." % (a + b))


def main():
    seen = set()
    sets = [
        ("Nomes dos pares de ângulos", mix(R, seen, [(s1_nome, 16), (s4_teoria, 4)])),
        ("Achar o ângulo pela figura", mix(R, seen, [(s2_valor, 20)])),
        ("Ângulos iguais ou suplementares?", mix(R, seen, [(s2_valor, 10), (s4_teoria, 6), (s1_nome, 4)])),
        ("Equações com ângulos", mix(R, seen, [(s3_equacao, 20)])),
        ("Paralelas e triângulos", mix(R, seen, [(s5_triangulo, 12), (s3_equacao, 8)])),
    ]
    body = lesson(
        ["Quando uma <b>transversal</b> corta duas retas <b>paralelas</b>, formam-se 8 ângulos: 4 de medida a e 4 de medida 180° − a.",
         "<b>Correspondentes</b> (mesma posição), <b>alternos internos</b> e <b>alternos externos</b> são iguais.",
         "<b>Colaterais internos</b> (do mesmo lado, entre as paralelas) somam 180°.",
         "Com essas relações mostramos que a soma dos ângulos de um triângulo é 180°."],
        [("Alternos internos: 3x + 10 e 5x − 30", ["3x + 10 = 5x − 30", "40 = 2x"], "x = 20°"),
         ("Colaterais internos: 2x e x + 30", ["2x + x + 30 = 180", "3x = 150"], "x = 50°")],
        [["Dizer que colaterais são iguais", "Colaterais internos somam 180°."],
         ["Confundir alternos com correspondentes", "Alternos ficam em lados opostos da transversal."],
         ["Usar as relações sem retas paralelas", "As relações só valem se r e s forem paralelas."]],
        paralelas(60, {(0, "tr"): "60°", (1, "tr"): "60°", (1, "tl"): "120°"}))
    faq = [("Quais ângulos são iguais quando duas paralelas são cortadas por uma transversal?", "Os correspondentes, os alternos internos, os alternos externos e os opostos pelo vértice. Os colaterais internos e externos somam 180°."),
           ("O que a BNCC pede no 9º ano?", "Demonstrar relações simples entre os ângulos formados por retas paralelas cortadas por uma transversal (EF09MA10).")]
    unit(R, "angulos-e-retas-paralelas", "G", ["EF09MA10"],
         "Demonstrar relações simples entre os ângulos formados por retas paralelas cortadas por uma transversal",
         "Ângulos formados por retas paralelas e uma transversal", "Retas paralelas e transversal",
         "Atividades de matemática para o 9º ano sobre ângulos formados por retas paralelas cortadas por uma transversal: correspondentes, alternos, colaterais, equações e soma dos ângulos do triângulo. 100 exercícios com gabarito.",
         "Correspondentes e alternos são iguais.", "Colaterais internos somam 180°.",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
