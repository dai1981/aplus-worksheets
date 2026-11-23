# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Teorema de Pitágoras (Geometria, EF09MA14)
  python3 tools/gen_br_matematica_9_teorema_de_pitagoras.py
Hipotenusa e cateto; ternas pitagóricas; verificar se o triângulo é retângulo; diagonal do quadrado (l√2) e do retângulo;
altura do triângulo equilátero (l√3/2); escadas, rampas, TVs, terrenos.
Erros: somar os catetos sem elevar ao quadrado, subtrair quando é hipotenusa, esquecer a raiz.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, sq, formas, unit

R = random.Random(89014)
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25), (15, 20, 25), (10, 24, 26), (20, 21, 29), (9, 40, 41), (12, 35, 37), (18, 24, 30), (16, 30, 34)]


def tri(b, c, lab):
    """triângulo retângulo com catetos b (base) e c (altura); lab: textos para 'b', 'c', 'a'"""
    sc = min(260.0 / b, 150.0 / c)
    B, C, A = (75, 190), (75 + b * sc, 190), (75, 190 - c * sc)
    sh = {"pts": {"A": A, "B": B, "C": C}, "poly": "ABC", "right": [("B", "A", "C")], "sides": [("B", "C", lab["b"]), ("A", "B", lab["c"]), ("A", "C", lab["a"])]}
    return formas([sh], W=int(b * sc) + 150, H=220, label="triângulo retângulo ABC com ângulo reto em B")


def s1_hip():
    b, c, a = R.choice(TRIPLES)
    if R.random() < 0.5:
        b, c = c, b
    p = tri(b, c, {"b": "%d cm" % b, "c": "%d cm" % c, "a": "x"})
    return M(p + "Quanto mede a hipotenusa x?", "%d cm" % a, ["%d cm" % (b + c), "%d cm" % (b * b + c * c), "%s cm" % sq(abs(c * c - b * b)) if b != c else "1 cm", "%d cm" % (a + 1)],
             "x² = %d² + %d² = %d + %d = %d → <b>x = %d cm</b>." % (b, c, b * b, c * c, a * a, a))


def s2_cat():
    b, c, a = R.choice(TRIPLES)
    if R.random() < 0.5:
        b, c = c, b
    p = tri(b, c, {"b": "x", "c": "%d cm" % c, "a": "%d cm" % a})
    return M(p + "Quanto mede o cateto x?", "%d cm" % b, ["%d cm" % (a - c), "%s cm" % sq(a * a + c * c), "%d cm" % (a * a - c * c), "%d cm" % (b + 1)],
             "x² = %d² − %d² = %d − %d = %d → <b>x = %d cm</b>." % (a, c, a * a, c * c, b * b, b))


def s3_irr():
    b, c = R.choice([(1, 1), (1, 2), (2, 3), (1, 3), (2, 4), (3, 3), (2, 2), (4, 4), (1, 4), (3, 5), (2, 6), (4, 6)])
    k = R.choice(["hip", "cat"])
    if k == "hip":
        n = b * b + c * c
        return M("Os catetos de um triângulo retângulo medem %d cm e %d cm. Quanto mede a hipotenusa? (Deixe a raiz simplificada.)" % (b, c), "%s cm" % sq(n), ["%d cm" % (b + c), "%s cm" % sq(abs(c * c - b * b)) if b != c else "%d cm" % (2 * b), "%d cm" % n, "√%d cm" % n if sq(n) != "√%d" % n else "%s cm" % sq(n + 1)],
                     "a² = %d + %d = %d → a = √%d = <b>%s cm</b>." % (b * b, c * c, n, n, sq(n)))
    a = c + R.randint(1, 3)
    n = a * a - b * b if a > b else None
    if not n or b == a:
        return None
    return M("A hipotenusa de um triângulo retângulo mede %d cm e um cateto mede %d cm. Quanto mede o outro cateto? (Deixe a raiz simplificada.)" % (a, b), "%s cm" % sq(n), ["%s cm" % sq(a * a + b * b), "%d cm" % (a - b), "%d cm" % n, "√%d cm" % n if sq(n) != "√%d" % n else "%s cm" % sq(n + 1)],
             "x² = %d − %d = %d → <b>x = %s cm</b>." % (a * a, b * b, n, sq(n)))


def s4_retangulo():
    if R.random() < 0.5:
        b, c, a = R.choice(TRIPLES)
        ans = "sim, é retângulo"
        why = "%d² + %d² = %d = %d²" % (b, c, a * a, a)
    else:
        b, c, a = R.choice(TRIPLES)
        a = a + R.choice([-1, 1])
        ans = "não é retângulo"
        why = "%d² + %d² = %d, mas %d² = %d" % (b, c, b * b + c * c, a, a * a)
    ls = [b, c, a]
    R.shuffle(ls)
    return M("Um triângulo tem lados de %d cm, %d cm e %d cm. Ele é retângulo?" % tuple(ls), ans, ["sim, é retângulo" if ans != "sim, é retângulo" else "não é retângulo", "só se for isósceles", "não dá para saber sem os ângulos"],
             "Teste com o maior lado: %s. <b>%s</b>." % (why, ans[0].upper() + ans[1:]))


def s5_aplic():
    k = R.choice(["escada", "tv", "terreno", "quadrado", "equi", "rampa", "pipa"])
    if k == "escada":
        b, c, a = R.choice([(6, 8, 10), (3, 4, 5), (5, 12, 13), (9, 12, 15), (12, 16, 20)])
        unit_ = "m" if a <= 15 else "dm"
        return M("Uma escada de %d %s está apoiada num muro, com o pé a %d %s do muro. A que altura do chão ela toca o muro?" % (a, unit_, b, unit_), "%d %s" % (c, unit_), ["%d %s" % (a - b, unit_), "%s %s" % (sq(a * a + b * b), unit_), "%d %s" % (a + b, unit_)],
                 "h² = %d² − %d² = %d → <b>h = %d %s</b>." % (a, b, c * c, c, unit_))
    if k == "tv":
        b, c, a = R.choice([(48, 36, 60), (64, 48, 80), (80, 60, 100), (96, 72, 120)])
        return M("A tela de uma TV mede %d cm de largura e %d cm de altura. Quanto mede a diagonal?" % (b, c), "%d cm" % a, ["%d cm" % (b + c), "%d cm" % (b - c), "%d cm" % (a + 10)],
                 "d² = %d² + %d² = %d → <b>d = %d cm</b>." % (b, c, a * a, a))
    if k == "terreno":
        b, c, a = R.choice([(30, 40, 50), (24, 32, 40), (15, 20, 25), (60, 80, 100), (12, 35, 37)])
        return M("Um terreno retangular mede %d m por %d m. Quanto mede o caminho em linha reta de um canto ao canto oposto?" % (b, c), "%d m" % a, ["%d m" % (b + c), "%d m" % (2 * (b + c)), "%d m" % (c - b + 10)],
                 "d² = %d² + %d² = %d → <b>d = %d m</b>." % (b, c, a * a, a))
    if k == "quadrado":
        l = R.randint(2, 12)
        return M("Quanto mede a diagonal de um quadrado de lado %d cm?" % l, "%d√2 cm" % l, ["%d cm" % (2 * l), "%d√3 cm" % l, "%d cm" % (l * l), "√%d cm" % l],
                 "d² = %d² + %d² = %d → d = √%d = <b>%d√2 cm</b>." % (l, l, 2 * l * l, 2 * l * l, l))
    if k == "equi":
        l = R.choice([4, 6, 8, 10, 12, 14, 16, 18, 20])
        return M("Quanto mede a altura de um triângulo equilátero de lado %d cm?" % l, "%s√3 cm" % ("" if l == 2 else str(l // 2)), ["%d cm" % (l // 2), "%d√2 cm" % (l // 2), "%d√3 cm" % l, "%d cm" % l],
                 "A altura divide a base ao meio: h² = %d² − %d² = %d → <b>h = %s√3 cm</b>." % (l, l // 2, l * l - l * l // 4, "" if l == 2 else str(l // 2)))
    if k == "rampa":
        b, c, a = R.choice([(24, 7, 25), (12, 5, 13), (40, 9, 41), (15, 8, 17)])
        return M("Uma rampa sobe %d dm de altura e avança %d dm na horizontal. Qual é o comprimento da rampa?" % (c, b), "%d dm" % a, ["%d dm" % (b + c), "%d dm" % (b - c), "%d dm" % (a + 2)],
                 "r² = %d² + %d² = %d → <b>r = %d dm</b>." % (b, c, a * a, a))
    b, c, a = R.choice([(30, 40, 50), (24, 18, 30), (36, 48, 60), (21, 20, 29)])
    return M("Uma pipa está presa a uma linha esticada de %d m. Ela está bem acima de um ponto a %d m de quem segura a linha. A que altura está a pipa (desprezando a altura da mão)?" % (a, b), "%d m" % c, ["%d m" % (a - b), "%d m" % (a + b), "%s m" % sq(a * a + b * b)],
             "h² = %d² − %d² = %d → <b>h = %d m</b>." % (a, b, c * c, c))


def main():
    seen = set()
    sets = [
        ("Calcular a hipotenusa", mix(R, seen, [(s1_hip, 20)])),
        ("Calcular um cateto", mix(R, seen, [(s2_cat, 20)])),
        ("Raízes que não são exatas", mix(R, seen, [(s3_irr, 20)])),
        ("O triângulo é retângulo?", mix(R, seen, [(s4_retangulo, 20)])),
        ("Problemas com o teorema de Pitágoras", mix(R, seen, [(s5_aplic, 20)])),
    ]
    body = lesson(
        ["No triângulo retângulo, o quadrado da <b>hipotenusa</b> é igual à soma dos quadrados dos <b>catetos</b>: a² = b² + c².",
         "Para achar a hipotenusa, some os quadrados e tire a raiz. Para achar um cateto, subtraia: b² = a² − c².",
         "Se a² = b² + c² vale para os lados de um triângulo (com a o maior lado), o triângulo é retângulo.",
         "Casos úteis: diagonal do quadrado = l√2; altura do triângulo equilátero = l√3 ÷ 2."],
        [("Catetos 9 e 12", ["9² + 12² = 81 + 144 = 225", "√225"], "hipotenusa 15"),
         ("Hipotenusa 13, cateto 5", ["13² − 5² = 169 − 25 = 144", "√144"], "cateto 12")],
        [["Somar os catetos sem elevar ao quadrado", "3 + 4 = 7 não é a hipotenusa; 3² + 4² = 25, então ela é 5."],
         ["Somar quando é para subtrair", "Para o cateto: a² − c²."],
         ["Esquecer a raiz", "a² = 25 dá a = 5."]],
        tri(4, 3, {"b": "b", "c": "c", "a": "a"}))
    faq = [("O que diz o teorema de Pitágoras?", "Em todo triângulo retângulo, o quadrado da hipotenusa é igual à soma dos quadrados dos catetos: a² = b² + c²."),
           ("O que é uma terna pitagórica?", "São três números inteiros que satisfazem a² = b² + c², como 3, 4 e 5, ou 5, 12 e 13. Multiplicando uma terna por um número, obtemos outra: 6, 8 e 10.")]
    unit(R, "teorema-de-pitagoras", "G", ["EF09MA14"],
         "Resolver e elaborar problemas de aplicação do teorema de Pitágoras ou das relações de proporcionalidade envolvendo retas paralelas cortadas por secantes",
         "Teorema de Pitágoras: hipotenusa, catetos e problemas", "Teorema de Pitágoras",
         "Atividades de matemática para o 9º ano sobre o teorema de Pitágoras: hipotenusa, catetos, raízes simplificadas, verificar se o triângulo é retângulo, diagonal do quadrado, altura do triângulo equilátero e problemas. 100 exercícios com gabarito.",
         "a² = b² + c²", "A hipotenusa fica em frente ao ângulo reto e é o maior lado.",
         body, faq, sets, 14)


if __name__ == "__main__":
    main()
