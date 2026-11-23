# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Semejanza y teorema de Tales (Sentido espacial)
build(lv): lv = 2 → «semejanza-y-teorema-de-tales»: figuras semejantes y razón de semejanza, teorema de Tales, triángulos en posición de Tales, escalas, áreas y volúmenes de figuras semejantes, problemas;
lv = 4 → «semejanza»: criterios de semejanza de triángulos, Tales con ecuaciones, razón de áreas y volúmenes, alturas inaccesibles.
Errores: sumar en lugar de multiplicar por la razón, usar la misma razón para áreas (k²) y volúmenes (k³), emparejar mal los lados correspondientes.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, d, fq, num, unit, L, Kids, figure

R = None
LV = 2
K = None


def cm(x):
    return "%s cm" % (d(x) if F(x).denominator in (1, 2, 4, 5, 10) else fq(x))


def s_razon():
    a, b = R.randint(2, 12), R.randint(2, 12)
    k = F(R.choice([2, 3, 4, 5, 3, 5]), R.choice([1, 1, 2]))
    if k == 1:
        return None
    t = R.choice(["k", "lado", "per", "si_no"])
    if t == "k":
        return M("Un rectángulo de %d cm × %d cm es semejante a otro de %s × %s. ¿Cuál es la razón de semejanza (grande / pequeño)?" % (a, b, cm(a * k), cm(b * k)), d(k), [d(1 / k) if (1 / k).denominator in (1, 2, 4, 5, 10) else fq(1 / k), d(a * k - a), d(k * k)],
                 "%s : %d = <b>%s</b>." % (cm(a * k).replace(" cm", ""), a, d(k)))
    if t == "lado":
        return M("Dos triángulos son semejantes con razón %s. Un lado del pequeño mide %d cm. ¿Cuánto mide el lado correspondiente del grande?" % (d(k), a), cm(a * k), [cm(a + k), cm(a * k * k), cm(F(a) / k)], "%d · %s = <b>%s</b>." % (a, d(k), cm(a * k)))
    if t == "per":
        p = 2 * (a + b)
        return M("Un polígono tiene %d cm de perímetro. ¿Cuál es el perímetro de otro semejante con razón %s?" % (p, d(k)), cm(p * k), [cm(p * k * k), cm(p + k), cm(F(p) / k)], "Los perímetros están en la misma razón k: <b>%s</b>." % cm(p * k))
    c = R.randint(2, 9)
    ok = R.random() < 0.5
    e = c * k if ok else c * k + R.choice([1, 2])
    return M("¿Son semejantes dos rectángulos de %d × %d y %s × %s?" % (a, c, d(a * k), d(e)), "sí" if ok else "no", ["no" if ok else "sí", "solo si son cuadrados", "no se puede saber"],
             "%s : %d = %s y %s : %d = %s: <b>%s</b>." % (d(a * k), a, d(k), d(e), c, d(F(e, c)) if F(e, c).denominator in (1, 2, 4, 5, 10) else fq(F(e, c)), "sí, la razón es la misma" if ok else "no, las razones son distintas"))


def tales_fig(a, b, c, x_side):
    """triángulo en posición de Tales: A arriba, AB = a + …"""
    k = F(a + b, a)
    pts = {"A": (0, 6), "B": (-3, 0), "C": (5, 0), "D": (-3 * F(a, a + b), 6 - 6 * F(a, a + b)), "E": (5 * F(a, a + b), 6 - 6 * F(a, a + b))}
    pts = {kk: (float(v[0]), float(v[1])) for kk, v in pts.items()}
    sides = [("A", "D", "%d" % a), ("D", "B", "%d" % b)]
    sides.append(("A", "E", "%s" % (fq(c) if x_side != "AE" else "x")))
    return figure(pts, [("A", "B"), ("A", "C"), ("B", "C"), ("D", "E")], sides=sides, label="triángulo con un segmento paralelo a la base")


def s_tales():
    a, b = R.randint(2, 9), R.randint(2, 9)
    c = R.randint(2, 12)
    x = F(c * b, a)
    t = R.choice(["frac", "ec"]) if LV >= 4 else R.choice(["frac", "frac", "fig"])
    if t == "fig":
        if x.denominator not in (1, 2):
            return None
        return M(tales_fig(a, b, c, "") + "DE es paralelo a BC. AD = %d, DB = %d y AE = %d. ¿Cuánto mide EC?" % (a, b, c), d(x), [d(F(c * a, b)) if F(c * a, b).denominator in (1, 2, 4, 5, 10) else fq(F(c * a, b)), d(c + b - a) if c + b - a > 0 else d(x + 1), d(x + 1)],
                 "Tales: AD/DB = AE/EC → %d/%d = %d/EC → EC = <b>%s</b>." % (a, b, c, d(x)))
    if t == "frac":
        if x.denominator not in (1, 2, 4, 5):
            return None
        return M("Tres rectas paralelas cortan a dos secantes. En la primera los segmentos miden %d cm y %d cm; en la segunda, el primero mide %d cm. ¿Cuánto mide el segundo?" % (a, b, c), cm(x), [cm(F(c * a, b)), cm(c + b - a) if c + b - a > 0 else cm(x + 1), cm(x + 2)],
                 "Los segmentos son proporcionales: %d/%d = %d/x → x = <b>%s</b>." % (a, b, c, cm(x)))
    # «ec»: Tales con una incógnita en dos segmentos
    xv = R.randint(2, 8)
    k = R.randint(2, 4)
    p1, p2 = xv, xv + R.randint(1, 4)
    return M("Con rectas paralelas, los segmentos de una secante miden x y x + %d, y los de la otra %d y %d. ¿Cuánto vale x?" % (p2 - p1, p1 * k, p2 * k), "x = %d" % xv, ["x = %d" % (xv * k), "x = %d" % (xv + 1), "x = %d" % (p2 - p1)] if p2 - p1 != xv else ["x = %d" % (xv * k), "x = %d" % (xv + 1), "x = %d" % (xv + 2)],
             "x/(x + %d) = %d/%d; productos cruzados: <b>x = %d</b>." % (p2 - p1, p1 * k, p2 * k, xv))


def s_escala():
    t = R.choice(["real", "plano", "escala", "area"])
    e = R.choice([100, 200, 500, 1000, 25000, 50000, 100000, 200000])
    if t == "real":
        c = R.randint(2, 18)
        real = c * e
        ok = ("%s km" % d(F(real, 100000))) if real >= 100000 else ("%s m" % d(F(real, 100)))
        return M("En un mapa a escala 1 : %s, dos pueblos están a %d cm. ¿Qué distancia real los separa?" % (num(e), c), ok, ["%s m" % d(F(real, 1000)) if real < 100000 else "%s km" % d(F(real, 10000)), "%s cm" % num(c + e), "%s km" % d(F(real, 1000)) if real >= 100000 else "%s m" % d(F(real, 10))],
                 "%d · %s = %s cm = <b>%s</b>." % (c, num(e), num(real), ok))
    if t == "plano":
        km = R.randint(2, 30)
        e = R.choice([50000, 100000, 200000, 250000])
        c = F(km * 100000, e)
        return M("¿Cuántos centímetros mide en un mapa 1 : %s una distancia real de %d km?" % (num(e), km), cm(c), [cm(c * 10), cm(F(km * 1000, e)), cm(c + 1)], "%d km = %s cm; %s : %s = <b>%s</b>." % (km, num(km * 100000), num(km * 100000), num(e), cm(c)))
    if t == "escala":
        c = R.randint(2, 10)
        real_m = c * e // 100
        if c * e % 100:
            return None
        return M("En un plano, %d cm representan %s m reales. ¿Cuál es la escala?" % (c, num(real_m)), "1 : %s" % num(e), ["1 : %s" % num(e // 10), "1 : %s" % num(e * 10), "1 : %s" % num(real_m)], "%s m = %s cm; %s : %d = <b>1 : %s</b>." % (num(real_m), num(real_m * 100), num(real_m * 100), c, num(e)))
    k = R.choice([2, 3, 4, 5, 10])
    A = R.randint(3, 40)
    return M("Una maqueta está a escala 1 : %d. Un jardín de la maqueta mide %d cm². ¿Cuánto mide en la realidad?" % (k, A), "%s cm²" % num(A * k * k), ["%s cm²" % num(A * k), "%s cm²" % num(A * k ** 3), "%s cm²" % num(A + k)], "Las áreas se multiplican por k² = %d: <b>%s cm²</b>." % (k * k, num(A * k * k)))


def s_area_vol():
    k = R.choice([2, 3, 4, 5, F(1, 2), F(3, 2)])
    t = R.choice(["area", "vol", "k_de_area"])
    if t == "area":
        A = R.randint(4, 50)
        return M("Dos figuras semejantes tienen razón de semejanza %s. La pequeña tiene %d cm² de área. ¿Qué área tiene la grande?" % (d(k), A) if k > 1 else
                 "Dos figuras semejantes tienen razón de semejanza %s. La primera tiene %d cm² de área. ¿Qué área tiene la segunda?" % (d(k), A), "%s cm²" % d(A * k * k), ["%s cm²" % d(A * k), "%s cm²" % d(A * k ** 3), "%s cm²" % d(A * 2 * k)],
                 "Razón de áreas = k² = %s: <b>%s cm²</b>." % (d(k * k), d(A * k * k)))
    if t == "vol":
        V = R.randint(2, 30)
        return M("Dos cuerpos semejantes tienen razón de semejanza %s. El primero tiene %d cm³ de volumen. ¿Qué volumen tiene el segundo?" % (d(k), V), "%s cm³" % d(V * k ** 3), ["%s cm³" % d(V * k), "%s cm³" % d(V * k * k), "%s cm³" % d(V * 3 * k)],
                 "Razón de volúmenes = k³ = %s: <b>%s cm³</b>." % (d(k ** 3), d(V * k ** 3)))
    k = R.choice([2, 3, 4, 5])
    return M("Las áreas de dos figuras semejantes están en razón %d. ¿Cuál es la razón de semejanza?" % (k * k), str(k), [str(k * k), str(k ** 3), str(k * k // 2) if k * k // 2 != k else str(k + 1)], "k² = %d → <b>k = %d</b>." % (k * k, k))


def s_criterios():
    q, a, w = R.choice([("Dos triángulos con dos ángulos iguales son…", "semejantes", ["iguales", "rectángulos", "no se puede saber"]),
                        ("Dos triángulos con los tres lados proporcionales son…", "semejantes", ["iguales", "isósceles", "no se puede saber"]),
                        ("Dos triángulos con dos lados proporcionales y el ángulo comprendido igual son…", "semejantes", ["iguales", "equiláteros", "no se puede saber"]),
                        ("¿Son semejantes dos triángulos equiláteros cualesquiera?", "sí, siempre", ["no, nunca", "solo si tienen el mismo lado", "solo si son pequeños"]),
                        ("¿Son semejantes dos rectángulos cualesquiera?", "no, no siempre", ["sí, siempre", "sí, porque sus ángulos son rectos", "solo si son grandes"]),
                        ("Al trazar la altura sobre la hipotenusa de un triángulo rectángulo se forman…", "dos triángulos semejantes al original", ["dos triángulos iguales", "un cuadrado", "dos triángulos isósceles"]),
                        ("Un triángulo tiene ángulos de 40° y 75°. Otro tiene ángulos de 75° y 65°. ¿Son semejantes?", "sí: los dos tienen 40°, 65° y 75°", ["no, tienen ángulos distintos", "solo si los lados son iguales", "no se puede saber"]),
                        ("Si dos figuras son semejantes con razón 1, entonces son…", "iguales (congruentes)", ["distintas", "proporcionales con k = 2", "rectángulos"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_problema():
    t = R.choice(["sombra", "sombra", "espejo", "foto", "maqueta"])
    if t == "sombra":
        h1 = F(R.randint(14, 19), 10)
        s1 = F(R.randint(8, 30), 10)
        k = R.randint(4, 12)
        s2 = s1 * k
        h2 = h1 * k
        return M("Una persona de %s m de altura proyecta una sombra de %s m. A la misma hora, un árbol proyecta una sombra de %s m. ¿Cuánto mide el árbol?" % (d(h1), d(s1), d(s2)), "%s m" % d(h2), ["%s m" % d(s2 * s1 / h1) if (s2 * s1 / h1).denominator in (1, 2, 4, 5, 10) else "%s m" % d(h2 + 1), "%s m" % d(h1 + s2 - s1), "%s m" % d(h2 * 2)],
                 "Triángulos semejantes: h/%s = %s/%s → h = <b>%s m</b>." % (d(s2), d(h1), d(s1), d(h2)))
    if t == "espejo":
        e = R.randint(1, 3)
        o = F(R.randint(15, 18), 10)
        k = R.randint(3, 10)
        return M("Para medir una farola, ponemos un espejo en el suelo. Una persona cuyos ojos están a %s m del suelo se ve reflejada a %d m del espejo; la farola está a %d m del espejo. ¿Cuánto mide la farola?" % (d(o), e, e * k),
                 "%s m" % d(o * k), ["%s m" % d(o + e * k - e), "%s m" % d(F(e * k, 1) / o) if (F(e * k) / o).denominator in (1, 2, 4, 5, 10) else "%s m" % d(o * k + 1), "%s m" % d(o * k * k)], "%s/%d = h/%d → h = <b>%s m</b>." % (d(o), e, e * k, d(o * k)))
    if t == "foto":
        a, b = R.choice([(10, 15), (9, 13), (13, 18), (20, 30), (15, 20)])
        k = R.choice([2, 3, F(3, 2)])
        return M("Una foto de %d cm × %d cm se amplía con razón %s. ¿Qué medidas tiene la ampliación?" % (a, b, d(k)), "%s cm × %s cm" % (d(a * k), d(b * k)), ["%s cm × %s cm" % (d(a + k), d(b + k)), "%s cm × %s cm" % (d(a * k * k), d(b * k * k)), "%s cm × %d cm" % (d(a * k), b)],
                 "Multiplicamos cada lado por %s: <b>%s cm × %s cm</b>." % (d(k), d(a * k), d(b * k)))
    e = R.choice([50, 100, 200])
    h = R.randint(10, 60)
    return M("La maqueta de un edificio a escala 1 : %d mide %d cm de alto. ¿Cuánto mide el edificio real?" % (e, h), "%s m" % d(F(h * e, 100)), ["%s m" % d(F(h * e, 1000)), "%s cm" % num(h + e), "%s m" % d(F(h * e, 10))], "%d · %d = %s cm = <b>%s m</b>." % (h, e, num(h * e), d(F(h * e, 100))))


def build(lv):
    global R, LV, K
    LV = lv
    R = random.Random(48010 + (lv - 2) * 1000)
    K = Kids(R)
    seen = set()
    if lv == 2:
        sets = [("Figuras semejantes", mix(R, seen, [(s_razon, 20)])), ("Teorema de Tales", mix(R, seen, [(s_tales, 20)])), ("Escalas", mix(R, seen, [(s_escala, 20)])),
                ("Áreas y volúmenes semejantes", mix(R, seen, [(s_area_vol, 14), (s_criterios, 6)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        slug, title, short, sort = "semejanza-y-teorema-de-tales", "Semejanza y teorema de Tales", "Semejanza", 10
        meta = "Fichas de matemáticas de 2.º de ESO: figuras semejantes, razón de semejanza, teorema de Tales, escalas, áreas y volúmenes y problemas. 100 ejercicios con soluciones."
        std = "Semejanza: figuras semejantes y razón de semejanza; teorema de Tales; escalas; relación entre longitudes, áreas y volúmenes de figuras semejantes"
    else:
        sets = [("Criterios de semejanza", mix(R, seen, [(s_criterios, 8), (s_razon, 12)])), ("Teorema de Tales", mix(R, seen, [(s_tales, 20)])), ("Áreas y volúmenes", mix(R, seen, [(s_area_vol, 20)])),
                ("Escalas", mix(R, seen, [(s_escala, 20)])), ("Alturas y distancias", mix(R, seen, [(s_problema, 20)]))]
        slug, title, short, sort = "semejanza", "Semejanza de triángulos", "Semejanza", 6
        meta = "Fichas de matemáticas de 4.º de ESO: criterios de semejanza, teorema de Tales, razón de áreas y volúmenes, escalas y alturas inaccesibles. 100 ejercicios con soluciones."
        std = "Semejanza de triángulos: criterios; teorema de Tales; razón de semejanza entre longitudes, áreas y volúmenes; cálculo de medidas indirectas"
    body = L(["Dos figuras son <b>semejantes</b> si tienen la misma forma: ángulos iguales y lados proporcionales. La razón entre lados correspondientes es la <b>razón de semejanza</b> k.",
              "<b>Teorema de Tales</b>: si varias rectas paralelas cortan a dos secantes, los segmentos que determinan son proporcionales.",
              "Si la razón de semejanza es k, las áreas están en razón k² y los volúmenes en razón k³."],
             [("Razón 3; área pequeña 5 cm²", ["5 · 3²"], "45 cm²"), ("Sombra de 1,5 m para 1,8 m; árbol con sombra de 6 m", ["1,8/1,5 = h/6"], "h = 7,2 m")],
             [["Sumar en lugar de multiplicar por la razón", "Semejanza es multiplicar por k."], ["Usar k para áreas o volúmenes", "Áreas: k². Volúmenes: k³."], ["Emparejar mal los lados", "Compara el lado menor con el menor, y así."]],
             tales_fig(3, 2, 4, ""))
    faq = [("¿Qué es la razón de semejanza?", "El número por el que se multiplican las longitudes de una figura para obtener la otra."),
           ("¿Cuándo son semejantes dos triángulos?", "Si tienen dos ángulos iguales, o los tres lados proporcionales, o dos lados proporcionales y el ángulo que forman igual.")]
    unit(lv, R, slug, "E", std, title, short, meta, "Áreas: k². Volúmenes: k³.", "k es la razón de semejanza.", body, faq, sets, sort)


if __name__ == "__main__":
    build(2)
