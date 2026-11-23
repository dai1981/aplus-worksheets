# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Cuerpos geométricos, áreas y volúmenes (Sentido de la medida)
build(lv): lv = 2 → «areas-y-volumenes-de-cuerpos»: poliedros y fórmula de Euler, áreas de prismas, pirámides, cilindros y conos, volúmenes, unidades de volumen y capacidad, problemas;
lv = 3 → «geometria-del-espacio»: generatriz y apotema con Pitágoras, esfera, volúmenes compuestos, coordenadas geográficas y husos horarios.
π ≈ 3,14.
Errores: sumar solo el área lateral, olvidar dividir entre 3 en pirámides y conos, confundir 1 dm³ con 1 cm³ (1 dm³ = 1 L).
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, d, num, unit, L, Kids, cuerpo_svg

R = None
LV = 2
K = None
PI = F(314, 100)


def r2(x):
    v = int(math.floor(float(x) * 100 + 0.5))
    return d(F(v, 100))


def s_euler():
    t = R.choice(["euler", "prisma", "piramide", "regular"])
    if t == "euler":
        C, V = R.choice([(6, 8), (5, 6), (5, 5), (7, 10), (8, 12), (4, 4), (8, 6), (6, 6), (7, 7), (12, 20), (20, 12)])
        A = C + V - 2
        return M("Un poliedro tiene %d caras y %d vértices. ¿Cuántas aristas tiene?" % (C, V), str(A), [str(C + V), str(C + V + 2), str(abs(C - V) + 2)], "Fórmula de Euler: C + V = A + 2 → A = %d + %d − 2 = <b>%d</b>." % (C, V, A))
    n = R.randint(3, 8)
    nm = {3: "triangular", 4: "cuadrangular", 5: "pentagonal", 6: "hexagonal", 7: "heptagonal", 8: "octogonal"}[n]
    if t == "prisma":
        k = R.choice(["caras", "vértices", "aristas"])
        v = {"caras": n + 2, "vértices": 2 * n, "aristas": 3 * n}[k]
        return M("¿Cuántas %s tiene un prisma %s?" % (k, nm), str(v), [str(n + 1) if v != n + 1 else str(n), str(2 * n + 1), str(3 * n + 2)] if k == "caras" else [str(n), str(3 * n) if v != 3 * n else str(2 * n), str(v + 2)],
                 "Un prisma de base con %d lados: %d caras, %d vértices y %d aristas. <b>%d</b>." % (n, n + 2, 2 * n, 3 * n, v))
    if t == "piramide":
        k = R.choice(["caras", "vértices", "aristas"])
        v = {"caras": n + 1, "vértices": n + 1, "aristas": 2 * n}[k]
        return M("¿Cuántas %s tiene una pirámide %s?" % (k, nm), str(v), [str(n + 2), str(2 * n) if v != 2 * n else str(n + 1), str(3 * n)], "Una pirámide de base con %d lados: %d caras, %d vértices y %d aristas. <b>%d</b>." % (n, n + 1, n + 1, 2 * n, v))
    q, a, w = R.choice([("¿Cuántos poliedros regulares hay?", "5", ["4", "6", "infinitos"]), ("¿Qué polígonos forman las caras de un octaedro?", "triángulos equiláteros", ["cuadrados", "pentágonos", "hexágonos"]),
                        ("¿Qué polígonos forman las caras de un dodecaedro?", "pentágonos regulares", ["triángulos", "cuadrados", "hexágonos"]), ("¿Cuántas caras tiene un icosaedro?", "20", ["12", "8", "10"]),
                        ("¿Qué cuerpo se obtiene al girar un rectángulo alrededor de un lado?", "un cilindro", ["un cono", "una esfera", "un prisma"]), ("¿Qué cuerpo se obtiene al girar un triángulo rectángulo alrededor de un cateto?", "un cono", ["un cilindro", "una pirámide", "una esfera"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_areas():
    t = R.choice(["ortoedro", "cubo", "cilindro", "cono", "piramide"])
    if t == "ortoedro":
        a, b, c = R.randint(2, 12), R.randint(2, 12), R.randint(2, 12)
        A = 2 * (a * b + a * c + b * c)
        return M("¿Cuál es el área total de un ortoedro de %d cm × %d cm × %d cm?" % (a, b, c), "%s cm²" % num(A), ["%s cm²" % num(a * b * c), "%s cm²" % num(a * b + a * c + b * c), "%s cm²" % num(A + 2 * a * b)], "2(ab + ac + bc) = 2(%d + %d + %d) = <b>%s cm²</b>." % (a * b, a * c, b * c, num(A)))
    if t == "cubo":
        l = R.randint(2, 15)
        return M("¿Cuál es el área total de un cubo de %d cm de arista?" % l, "%s cm²" % num(6 * l * l), ["%s cm²" % num(l ** 3), "%s cm²" % num(4 * l * l), "%s cm²" % num(12 * l)], "6 caras de %d²: <b>%s cm²</b>." % (l, num(6 * l * l)))
    if t == "cilindro":
        r, h = R.randint(1, 10), R.randint(2, 15)
        k = R.choice(["lat", "tot"])
        Al = 2 * PI * r * h
        At = Al + 2 * PI * r * r
        if k == "lat":
            return M("¿Cuál es el área lateral de un cilindro de radio %d cm y altura %d cm? (π ≈ 3,14)" % (r, h), "%s cm²" % r2(Al), ["%s cm²" % r2(At), "%s cm²" % r2(PI * r * r * h), "%s cm²" % r2(PI * r * h)], "A<sub>L</sub> = 2πrh = 2 · 3,14 · %d · %d = <b>%s cm²</b>." % (r, h, r2(Al)))
        return M("¿Cuál es el área total de un cilindro de radio %d cm y altura %d cm? (π ≈ 3,14)" % (r, h), "%s cm²" % r2(At), ["%s cm²" % r2(Al), "%s cm²" % r2(Al + PI * r * r), "%s cm²" % r2(PI * r * r * h)], "A = 2πrh + 2πr² = <b>%s cm²</b>." % r2(At))
    if t == "cono":
        r, h, g = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)])
        Al = PI * r * g
        At = Al + PI * r * r
        if LV == 2:
            return M("Un cono tiene radio %d cm y generatriz %d cm. ¿Cuál es su área total? (π ≈ 3,14)" % (r, g), "%s cm²" % r2(At), ["%s cm²" % r2(Al), "%s cm²" % r2(PI * r * h + PI * r * r), "%s cm²" % r2(2 * PI * r * g)], "A = πrg + πr² = <b>%s cm²</b>." % r2(At))
        return M("Un cono tiene radio %d cm y altura %d cm. ¿Cuál es su área lateral? (π ≈ 3,14)" % (r, h), "%s cm²" % r2(Al), ["%s cm²" % r2(PI * r * h), "%s cm²" % r2(At), "%s cm²" % r2(2 * PI * r * g)], "g = √(%d² + %d²) = %d; A<sub>L</sub> = πrg = <b>%s cm²</b>." % (r, h, g, r2(Al)))
    l, ap = R.choice([(6, 5), (10, 13), (8, 5), (12, 10), (16, 17), (6, 4), (10, 12)])
    Al = 4 * l * ap // 2
    At = Al + l * l
    return M("Una pirámide de base cuadrada de %d cm de lado tiene una apotema lateral de %d cm. ¿Cuál es su área total?" % (l, ap), "%s cm²" % num(At), ["%s cm²" % num(Al), "%s cm²" % num(4 * l * ap + l * l), "%s cm²" % num(l * l * ap // 3)], "4 triángulos (%d · %d : 2) + base %d² = <b>%s cm²</b>." % (l, ap, l, num(At)))


def s_volumen():
    t = R.choice(["prisma", "cilindro", "piramide", "cono", "esfera"] if LV >= 3 else ["prisma", "prisma", "cilindro", "piramide", "cono"])
    if t == "prisma":
        a, b, c = R.randint(2, 15), R.randint(2, 12), R.randint(2, 12)
        if R.random() < 0.5:
            V = F(a * b, 2) * c
            return M("Un prisma tiene como base un triángulo rectángulo de catetos %d cm y %d cm, y %d cm de altura. ¿Cuál es su volumen?" % (a, b, c), "%s cm³" % d(V), ["%s cm³" % num(a * b * c), "%s cm³" % d(V / 3), "%s cm³" % num(a + b + c)], "V = área de la base · altura = %s · %d = <b>%s cm³</b>." % (d(F(a * b, 2)), c, d(V)))
        return M("¿Cuál es el volumen de un ortoedro de %d cm × %d cm × %d cm?" % (a, b, c), "%s cm³" % num(a * b * c), ["%s cm³" % num(2 * (a * b + a * c + b * c)), "%s cm³" % num(a * b * c // 3) if a * b * c % 3 == 0 else "%s cm³" % num(a * b * c + a), "%s cm³" % num(a + b + c)], "V = %d · %d · %d = <b>%s cm³</b>." % (a, b, c, num(a * b * c)))
    r, h = R.randint(1, 10), R.randint(3, 15)
    if t == "cilindro":
        V = PI * r * r * h
        return M("¿Cuál es el volumen de un cilindro de radio %d cm y altura %d cm? (π ≈ 3,14)" % (r, h), "%s cm³" % r2(V), ["%s cm³" % r2(V / 3), "%s cm³" % r2(2 * PI * r * h), "%s cm³" % r2(PI * r * h)], "V = πr²h = 3,14 · %d · %d = <b>%s cm³</b>." % (r * r, h, r2(V)))
    if t == "cono":
        V = PI * r * r * h / 3
        return M("¿Cuál es el volumen de un cono de radio %d cm y altura %d cm? (π ≈ 3,14)" % (r, h), "%s cm³" % r2(V), ["%s cm³" % r2(V * 3), "%s cm³" % r2(V / 2), "%s cm³" % r2(PI * r * h / 3)], "V = πr²h / 3 = <b>%s cm³</b>." % r2(V))
    if t == "piramide":
        l = R.randint(2, 12)
        h = 3 * R.randint(1, 6)
        V = l * l * h // 3
        return M("¿Cuál es el volumen de una pirámide de base cuadrada de %d cm de lado y %d cm de altura?" % (l, h), "%s cm³" % num(V), ["%s cm³" % num(l * l * h), "%s cm³" % num(l * l * h // 2) if l * l * h % 2 == 0 else "%s cm³" % num(V + l), "%s cm³" % num(l * h)], "V = área de la base · altura / 3 = %d · %d / 3 = <b>%s cm³</b>." % (l * l, h, num(V)))
    V = 4 * PI * r ** 3 / 3
    return M("¿Cuál es el volumen de una esfera de %d cm de radio? (π ≈ 3,14)" % r, "%s cm³" % r2(V), ["%s cm³" % r2(4 * PI * r * r), "%s cm³" % r2(PI * r ** 3), "%s cm³" % r2(4 * PI * r ** 3)], "V = 4πr³/3 = <b>%s cm³</b>." % r2(V))


def s_unidades():
    t = R.choice(["dm3L", "m3L", "cm3", "mL", "m3dm3"])
    if t == "dm3L":
        v = R.randint(2, 900)
        return M("¿Cuántos litros son %d dm³?" % v, "%d L" % v, ["%s L" % num(v * 1000), "%s L" % d(F(v, 1000)), "%s L" % num(v * 10)], "1 dm³ = 1 L: <b>%d L</b>." % v)
    if t == "m3L":
        v = F(R.randint(1, 90), R.choice([1, 10]))
        return M("¿Cuántos litros caben en un depósito de %s m³?" % d(v), "%s L" % num(int(v * 1000)) if (v * 1000).denominator == 1 else "%s L" % d(v * 1000), ["%s L" % d(v * 100), "%s L" % d(v * 10), "%s L" % num(int(v * 1000000))], "1 m³ = 1000 dm³ = 1000 L: <b>%s L</b>." % num(int(v * 1000)))
    if t == "cm3":
        v = R.randint(2, 99)
        return M("¿Cuántos cm³ son %d dm³?" % v, "%s cm³" % num(v * 1000), ["%s cm³" % num(v * 100), "%s cm³" % num(v * 10), "%s cm³" % num(v * 1000000)], "Cada unidad de volumen es 1000 veces la siguiente: <b>%s cm³</b>." % num(v * 1000))
    if t == "mL":
        v = R.randint(50, 990)
        return M("¿Cuántos mL son %d cm³?" % v, "%d mL" % v, ["%s mL" % num(v * 1000), "%s mL" % d(F(v, 10)), "%s mL" % num(v * 10)], "1 cm³ = 1 mL: <b>%d mL</b>." % v)
    v = F(R.randint(11, 999), 100)
    return M("Expresa %s m³ en dm³." % d(v), "%s dm³" % d(v * 1000), ["%s dm³" % d(v * 100), "%s dm³" % d(v * 10), "%s dm³" % d(v * 1000000)], "Multiplicamos por 1000: <b>%s dm³</b>." % d(v * 1000))


def s_esfera_geo():
    t = R.choice(["area", "vol", "lat", "huso", "lon"])
    if t == "area":
        r = R.randint(1, 15)
        return M("¿Cuál es el área de una esfera de %d cm de radio? (π ≈ 3,14)" % r, "%s cm²" % r2(4 * PI * r * r), ["%s cm²" % r2(PI * r * r), "%s cm²" % r2(4 * PI * r ** 3 / 3), "%s cm²" % r2(2 * PI * r * r)], "A = 4πr² = 4 · 3,14 · %d = <b>%s cm²</b>." % (r * r, r2(4 * PI * r * r)))
    if t == "vol":
        return s_volumen()
    if t == "lat":
        q, a, w = R.choice([("¿Qué latitud tiene el ecuador?", "0°", ["90°", "180°", "45°"]), ("¿Qué latitud tiene el polo norte?", "90° N", ["0°", "180° N", "45° N"]),
                            ("¿Desde qué meridiano se mide la longitud?", "el de Greenwich", ["el ecuador", "el trópico de Cáncer", "el de Madrid"]),
                            ("¿Qué mide la latitud de un punto?", "la distancia angular al ecuador", ["la distancia al meridiano de Greenwich", "la altitud", "la hora"]),
                            ("¿Qué mide la longitud de un punto?", "la distancia angular al meridiano de Greenwich", ["la distancia al ecuador", "la altitud", "el radio de la Tierra"]),
                            ("Madrid está aproximadamente en 40° N, 4° O. ¿En qué hemisferios está?", "norte y oeste", ["sur y este", "norte y este", "sur y oeste"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    if t == "huso":
        n = R.randint(1, 9)
        h = R.randint(8, 20)
        este = R.random() < 0.5
        r = (h + n) % 24 if este else (h - n) % 24
        return M("Son las %d:00 en Greenwich. ¿Qué hora es en un lugar situado %d husos horarios al %s?" % (h, n, "este" if este else "oeste"), "las %d:00" % r, ["las %d:00" % ((h - n) % 24 if este else (h + n) % 24), "las %d:00" % h, "las %d:00" % ((r + 1) % 24)], "Cada huso son 15° y 1 hora; al %s se %s: <b>las %d:00</b>." % ("este" if este else "oeste", "suma" if este else "resta", r))
    n = R.randint(1, 11)
    return M("Dos ciudades están en meridianos separados %d°. ¿Cuántas horas de diferencia hay entre ellas?" % (15 * n), "%d h" % n, ["%d h" % (15 * n), "%d h" % (n + 1), "%d h" % (24 - n)], "Cada 15° es una hora: %d : 15 = <b>%d h</b>." % (15 * n, n))


def s_problema():
    t = R.choice(["piscina", "lata", "caja", "helado", "pelota", "pintar"])
    if t == "piscina":
        a, b, h = R.randint(5, 25), R.randint(3, 12), F(R.randint(10, 25), 10)
        V = a * b * h
        return M("Una piscina mide %d m × %d m y tiene %s m de profundidad. ¿Cuántos litros de agua caben?" % (a, b, d(h)), "%s L" % num(int(V * 1000)), ["%s L" % d(V), "%s L" % num(int(V * 100)), "%s L" % num(int(V * 1000) + 1000)], "V = %s m³ = <b>%s L</b>." % (d(V), num(int(V * 1000))))
    if t == "lata":
        r, h = R.choice([(3, 10), (4, 12), (3, 11), (5, 8)])
        V = PI * r * r * h
        return M("Una lata cilíndrica tiene %d cm de radio y %d cm de altura. ¿Cuántos mL caben (redondea a las unidades)?" % (r, h), "%d mL" % round(float(V)), ["%d mL" % round(float(2 * PI * r * h)), "%d mL" % round(float(V / 3)), "%d mL" % round(float(V * 10))], "V = πr²h ≈ %s cm³ ≈ <b>%d mL</b>." % (r2(V), round(float(V))))
    if t == "caja":
        a, b, c = R.randint(10, 40), R.randint(10, 30), R.randint(5, 20)
        A = 2 * (a * b + a * c + b * c)
        return M("¿Cuánto cartón se necesita para fabricar una caja cerrada de %d cm × %d cm × %d cm?" % (a, b, c), "%s cm²" % num(A), ["%s cm³" % num(a * b * c), "%s cm²" % num(A // 2), "%s cm²" % num(A - a * b)], "Área total: <b>%s cm²</b>." % num(A))
    if t == "helado":
        r, h = R.randint(2, 4), R.randint(8, 14)
        V = PI * r * r * h / 3
        return M("Un cucurucho cónico mide %d cm de radio y %d cm de altura. ¿Qué volumen de helado cabe dentro? (π ≈ 3,14)" % (r, h), "%s cm³" % r2(V), ["%s cm³" % r2(V * 3), "%s cm³" % r2(PI * r * h), "%s cm³" % r2(V / 2)], "V = πr²h/3 = <b>%s cm³</b>." % r2(V))
    if t == "pelota" and LV >= 3:
        r = R.randint(3, 12)
        return M("¿Cuánto material se necesita para fabricar la superficie de un balón de %d cm de radio? (π ≈ 3,14)" % r, "%s cm²" % r2(4 * PI * r * r), ["%s cm³" % r2(4 * PI * r ** 3 / 3), "%s cm²" % r2(PI * r * r), "%s cm²" % r2(2 * PI * r)], "A = 4πr² = <b>%s cm²</b>." % r2(4 * PI * r * r))
    a, b, h = R.randint(3, 8), R.randint(3, 6), R.choice([F(25, 10), F(3), F(28, 10)])
    A = 2 * (a + b) * h
    return M("Queremos pintar las cuatro paredes de una habitación de %d m × %d m y %s m de alto (sin techo ni suelo). ¿Cuántos m² hay que pintar?" % (a, b, d(h)), "%s m²" % d(A), ["%s m²" % d(A + a * b), "%s m³" % d(a * b * h), "%s m²" % d(A + 2 * a * b)], "2(%d + %d) · %s = <b>%s m²</b>." % (a, b, d(h), d(A)))


def build(lv):
    global R, LV, K
    LV = lv
    R = random.Random(48011 + (lv - 2) * 1000)
    K = Kids(R)
    seen = set()
    if lv == 2:
        sets = [("Poliedros y fórmula de Euler", mix(R, seen, [(s_euler, 20)])), ("Áreas de cuerpos", mix(R, seen, [(s_areas, 20)])), ("Volúmenes", mix(R, seen, [(s_volumen, 20)])),
                ("Unidades de volumen y capacidad", mix(R, seen, [(s_unidades, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["<b>Fórmula de Euler</b> para poliedros: caras + vértices = aristas + 2.",
                 "Área total = área lateral + área de las bases. Cilindro: 2πrh + 2πr². Cono: πrg + πr² (g, generatriz).",
                 "Volumen de prismas y cilindros: área de la base · altura. De pirámides y conos: la tercera parte.", "1 dm³ = 1 L y 1 cm³ = 1 mL."]
        slug, title, short, kb, ks, sort = "areas-y-volumenes-de-cuerpos", "Áreas y volúmenes de cuerpos", "Áreas y volúmenes", "Pirámide y cono: base · altura / 3", "Prisma y cilindro: base · altura.", 11
        meta = "Fichas de matemáticas de 2.º de ESO: poliedros, fórmula de Euler, áreas y volúmenes de prismas, pirámides, cilindros y conos, litros y m³. 100 ejercicios con soluciones."
        std = "Cuerpos geométricos: poliedros y cuerpos de revolución; áreas y volúmenes; unidades de volumen y capacidad; resolución de problemas"
    else:
        sets = [("Áreas con Pitágoras", mix(R, seen, [(s_areas, 20)])), ("Volúmenes", mix(R, seen, [(s_volumen, 20)])), ("La esfera", mix(R, seen, [(s_esfera_geo, 10), (s_volumen, 10)])),
                ("Coordenadas geográficas", mix(R, seen, [(s_esfera_geo, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["En conos y pirámides, la generatriz o la apotema se calculan con Pitágoras a partir del radio (o media arista) y la altura.",
                 "<b>Esfera</b>: área 4πr²; volumen 4πr³/3.",
                 "Un punto de la Tierra se localiza por su <b>latitud</b> (respecto al ecuador) y su <b>longitud</b> (respecto al meridiano de Greenwich). Cada 15° de longitud hay una hora de diferencia."]
        slug, title, short, kb, ks, sort = "geometria-del-espacio", "Geometría del espacio", "Geometría del espacio", "Esfera: A = 4πr², V = 4πr³/3", "Conos y pirámides: g y apotema con Pitágoras.", 10
        meta = "Fichas de matemáticas de 3.º de ESO: áreas y volúmenes con Pitágoras, esfera, coordenadas geográficas, husos horarios y problemas. 100 ejercicios con soluciones."
        std = "Áreas y volúmenes de cuerpos geométricos; la esfera; coordenadas geográficas y husos horarios; resolución de problemas"
    ex = [("Cilindro r = 3 cm, h = 10 cm", ["V = 3,14 · 9 · 10"], "282,6 cm³"), ("Cono r = 3 cm, h = 4 cm", ["g = 5 cm", "A<sub>L</sub> = 3,14 · 3 · 5"], "47,1 cm²")]
    mist = [["Calcular solo el área lateral", "El área total incluye las bases."], ["Olvidar dividir entre 3", "Pirámides y conos: la tercera parte del prisma o cilindro."], ["Confundir dm³ y cm³", "1 dm³ = 1000 cm³ = 1 L."]]
    body = L(think, ex, mist, cuerpo_svg("cilindro"))
    faq = [("¿Qué relación hay entre litros y dm³?", "1 litro es exactamente 1 dm³; por eso 1 m³ = 1000 L."), ("¿Por qué el volumen del cono es un tercio del cilindro?", "Porque caben tres conos en el cilindro de la misma base y altura.")]
    unit(lv, R, slug, "M", std, title, short, meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(2)
