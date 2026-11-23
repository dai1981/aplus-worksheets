# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Trigonometria no triângulo retângulo (EM13MAT308)
  python3 tools/gen_br_matematica_em2_trigonometria_no_triangulo_retangulo.py
Seno, cosseno e tangente como razões entre lados; ângulos notáveis 30°, 45°, 60°; calcular lados com valores da tabela;
problemas (rampas, escadas, sombras, altura de prédios, ângulo de elevação).
Usa geradores do 9º ano (Pitágoras) com outro sorteio.
Erros: trocar cateto oposto e adjacente, usar a hipotenusa na tangente, esquecer que seno e cosseno são menores que 1.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, bank, mix, lesson, use, unit, tri_ret, sq

R = random.Random(92001)
pit_hip, pit_cat = use("gen_br_matematica_9_teorema_de_pitagoras", 92901, "s1_hip", "s2_cat")
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25), (9, 12, 15), (20, 21, 29)]
NOT = {30: ("1/2", "√3/2", "√3/3"), 45: ("√2/2", "√2/2", "1"), 60: ("√3/2", "1/2", "√3")}
TAB = {20: (F(342, 1000), F(940, 1000), F(364, 1000)), 25: (F(423, 1000), F(906, 1000), F(466, 1000)), 35: (F(574, 1000), F(819, 1000), F(700, 1000)),
       40: (F(643, 1000), F(766, 1000), F(839, 1000)), 50: (F(766, 1000), F(643, 1000), F(1192, 1000)), 55: (F(819, 1000), F(574, 1000), F(1428, 1000)),
       70: (F(940, 1000), F(342, 1000), F(2747, 1000))}


def s1_razoes():
    a, b, c = R.choice(TRIPLES)
    if R.random() < 0.5:
        a, b = b, a
    # cateto BC = a (adjacente a B), cateto AC = b (oposto a B), hipotenusa AB = c
    g = tri_ret(a, b, [("A", "B", str(c)), ("B", "C", str(a)), ("C", "A", str(b))], "α", label="triângulo retângulo ABC com ângulo α em B")
    k = R.choice(["sen", "cos", "tg"])
    v = {"sen": F(b, c), "cos": F(a, c), "tg": F(b, a)}[k]
    nome = {"sen": "sen α", "cos": "cos α", "tg": "tg α"}[k]
    w = [fq(x) for x in (F(b, c), F(a, c), F(b, a), F(a, b)) if x != v]
    exp = {"sen": "oposto ÷ hipotenusa = %d/%d" % (b, c), "cos": "adjacente ÷ hipotenusa = %d/%d" % (a, c), "tg": "oposto ÷ adjacente = %d/%d" % (b, a)}[k]
    return M(g + "Qual é o valor de %s?" % nome, fq(v), w, "%s = %s = <b>%s</b>." % (nome, exp, fq(v)))


def s2_notaveis():
    ang = R.choice([30, 45, 60])
    k = R.choice(["valor", "lado", "lado", "angulo"])
    if k == "valor":
        f = R.choice(["sen", "cos", "tg"])
        v = NOT[ang][["sen", "cos", "tg"].index(f)]
        w = sorted({NOT[a][i] for a in NOT for i in range(3)} - {v})
        R.shuffle(w)
        return M("Quanto vale %s %d°?" % (f, ang), v, w, "Tabela dos ângulos notáveis: %s %d° = <b>%s</b>." % (f, ang, v))
    if k == "lado":
        h = R.choice([4, 6, 8, 10, 12, 20])
        t = R.choice(["op", "adj"])
        if t == "op":
            ans = {30: str(h // 2), 45: "%s√2" % (h // 2), 60: "%s√3" % (h // 2)}[ang]
            g = tri_ret(1.7 if ang == 30 else (1 if ang == 45 else 0.6), 1, [("A", "B", str(h)), ("C", "A", "x")], "%d°" % ang, label="triângulo retângulo com hipotenusa %d e ângulo de %d°" % (h, ang))
            w = [str(h), {30: "%s√3" % (h // 2), 45: str(h // 2), 60: str(h // 2)}[ang], "%d√3" % h if ang != 30 else "%s√2" % (h // 2)]
            return M(g + "Qual é a medida x?", ans, w, "x = %d · sen %d° = %d · %s = <b>%s</b>." % (h, ang, h, NOT[ang][0], ans))
        ans = {30: "%s√3" % (h // 2), 45: "%s√2" % (h // 2), 60: str(h // 2)}[ang]
        g = tri_ret(1.7 if ang == 30 else (1 if ang == 45 else 0.6), 1, [("A", "B", str(h)), ("B", "C", "x")], "%d°" % ang, label="triângulo retângulo com hipotenusa %d e ângulo de %d°" % (h, ang))
        w = [str(h), {30: str(h // 2), 45: str(h // 2), 60: "%s√3" % (h // 2)}[ang], "%d√2" % h]
        return M(g + "Qual é a medida x?", ans, w, "x = %d · cos %d° = %d · %s = <b>%s</b>." % (h, ang, h, NOT[ang][1], ans))
    a = R.choice([3, 5, 7, 10])
    q, ans = R.choice([("O cateto oposto a α mede %d e a hipotenusa mede %d. Quanto mede α?" % (a, 2 * a), "30°"),
                       ("Os dois catetos medem %d. Quanto mede o ângulo agudo α?" % a, "45°"),
                       ("O cateto adjacente a α mede %d e a hipotenusa mede %d. Quanto mede α?" % (a, 2 * a), "60°")])
    return M("Num triângulo retângulo, " + q[0].lower() + q[1:], ans, [x for x in ("30°", "45°", "60°", "90°") if x != ans], "A razão dá o valor de um ângulo notável: <b>%s</b>." % ans)


def s3_tabela():
    ang = R.choice(list(TAB))
    s, c, t = TAB[ang]
    k = R.choice(["rampa", "escada", "predio", "sombra", "aviao"])
    if k == "rampa":
        L = R.choice([5, 8, 10, 12, 20])
        h = s * L
        return M("Uma rampa de %d m de comprimento faz um ângulo de %d° com o chão. A que altura ela chega? (sen %d° ≈ %s)" % (L, ang, ang, d(s)), "%s m" % d(h, 2), ["%s m" % d(c * L, 2), "%s m" % d(F(L) / s, 2), "%s m" % d(t * L, 2)],
                 "h = %d · sen %d° ≈ %d · %s = <b>%s m</b>." % (L, ang, L, d(s), d(h, 2)))
    if k == "escada":
        L = R.choice([4, 5, 6, 8, 10])
        x = c * L
        return M("Uma escada de %d m está apoiada numa parede, fazendo %d° com o chão. A que distância da parede está o pé da escada? (cos %d° ≈ %s)" % (L, ang, ang, d(c)), "%s m" % d(x, 2), ["%s m" % d(s * L, 2), "%s m" % d(F(L) / c, 2), "%s m" % d(t * L, 2)],
                 "x = %d · cos %d° ≈ <b>%s m</b>." % (L, ang, d(x, 2)))
    if k in ("predio", "sombra"):
        D = R.choice([10, 20, 30, 40, 50])
        h = t * D
        q = ("A %d m de um prédio, uma pessoa vê o topo sob um ângulo de %d° com a horizontal. Qual é a altura do prédio, sem contar a altura dos olhos? (tg %d° ≈ %s)" % (D, ang, ang, d(t)) if k == "predio" else
             "Uma árvore projeta uma sombra de %d m quando os raios de sol fazem %d° com o chão. Qual é a altura da árvore? (tg %d° ≈ %s)" % (D, ang, ang, d(t)))
        return M(q, "%s m" % d(h, 2), ["%s m" % d(s * D, 2), "%s m" % d(F(D) / t, 2), "%s m" % d(c * D, 2)], "h = %d · tg %d° ≈ %d · %s = <b>%s m</b>." % (D, ang, D, d(t), d(h, 2)))
    dist = R.choice([1000, 2000, 3000, 5000])
    h = s * dist
    return M("Um avião decola sob um ângulo de %d° e percorre %s m em linha reta. A que altura ele está? (sen %d° ≈ %s)" % (ang, d(dist), ang, d(s)), "%s m" % d(h), ["%s m" % d(c * dist), "%s m" % d(t * dist), "%s m" % d(dist)], "h = %s · %s = <b>%s m</b>." % (d(dist), d(s), d(h)))


s4_conceitos = bank(R, [
    ("Num triângulo retângulo, o seno de um ângulo agudo é…", "cateto oposto ÷ hipotenusa", ["cateto adjacente ÷ hipotenusa", "cateto oposto ÷ cateto adjacente", "hipotenusa ÷ cateto oposto"]),
    ("A tangente de um ângulo agudo é…", "cateto oposto ÷ cateto adjacente", ["cateto oposto ÷ hipotenusa", "hipotenusa ÷ cateto adjacente", "cateto adjacente ÷ hipotenusa"]),
    ("Para todo ângulo agudo α, sen² α + cos² α = …", "1", ["0", "2", "tg α"]),
    ("Se α e β são os ângulos agudos de um triângulo retângulo, sen α é igual a…", "cos β", ["sen β", "tg β", "1 − cos β"]),
    ("O seno de um ângulo agudo é sempre…", "maior que 0 e menor que 1", ["maior que 1", "igual a 1", "negativo"]),
    ("tg α = sen α ÷ …", "cos α", ["1", "sen α", "hipotenusa"]),
    ("Quando o ângulo agudo aumenta de 0° para 90°, o seno…", "aumenta", ["diminui", "fica igual", "vira negativo"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Seno, cosseno e tangente", mix(R, seen, [(s1_razoes, 20)])),
        ("Ângulos notáveis", mix(R, seen, [(s2_notaveis, 20)])),
        ("Calcular lados", mix(R, seen, [(s2_notaveis, 10), (pit_hip, 5), (pit_cat, 5)])),
        ("Problemas com a tabela trigonométrica", mix(R, seen, [(s3_tabela, 20)])),
        ("Revisão", mix(R, seen, [(s1_razoes, 6), (s3_tabela, 7), (s4_conceitos, 7)])),
    ]
    body = lesson(
        ["Num triângulo retângulo, para um ângulo agudo α: <b>sen α</b> = cateto oposto ÷ hipotenusa; <b>cos α</b> = cateto adjacente ÷ hipotenusa; <b>tg α</b> = cateto oposto ÷ cateto adjacente.",
         "Ângulos notáveis: sen 30° = 1/2, cos 30° = √3/2, tg 30° = √3/3; sen 45° = cos 45° = √2/2, tg 45° = 1; sen 60° = √3/2, cos 60° = 1/2, tg 60° = √3.",
         "Para achar um lado: escolha a razão que liga o lado conhecido ao lado procurado."],
        [("Hipotenusa 10, ângulo de 30°: cateto oposto", ["x = 10 · sen 30° = 10 · 1/2"], "5"),
         ("Sombra de 20 m, sol a 35° (tg 35° ≈ 0,7)", ["h = 20 · 0,7"], "14 m")],
        [["Trocar oposto e adjacente", "O oposto fica em frente ao ângulo; o adjacente encosta nele."],
         ["Usar a hipotenusa na tangente", "tg = oposto ÷ adjacente."],
         ["Seno ou cosseno maior que 1", "A hipotenusa é o maior lado: sen e cos ficam entre 0 e 1."]],
        tri_ret(4, 3, [("A", "B", "hipotenusa"), ("B", "C", "adjacente"), ("C", "A", "oposto")], "α", label="triângulo retângulo com os nomes dos lados em relação a α"))
    faq = [("Como lembrar seno, cosseno e tangente?", "Seno = oposto ÷ hipotenusa; cosseno = adjacente ÷ hipotenusa; tangente = oposto ÷ adjacente. Muitos usam a sigla SOH-CAH-TOA."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas em variados contextos, envolvendo triângulos nos quais se aplicam as relações métricas ou as noções de congruência e semelhança (EM13MAT308).")]
    unit(R, "trigonometria-no-triangulo-retangulo", "G", ["EM13MAT308"],
         "Aplicar as relações métricas, incluindo as leis do seno e do cosseno ou as noções de congruência e semelhança, para resolver e elaborar problemas que envolvem triângulos, em variados contextos",
         "Trigonometria no triângulo retângulo", "Trigonometria no triângulo retângulo",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre trigonometria no triângulo retângulo: seno, cosseno e tangente, ângulos notáveis, cálculo de lados e problemas com rampas, escadas e sombras. 100 exercícios com gabarito.",
         "sen = oposto ÷ hipotenusa", "cos = adjacente ÷ hipotenusa; tg = oposto ÷ adjacente.",
         body, faq, sets, 1, grade="2-serie")


if __name__ == "__main__":
    main()
