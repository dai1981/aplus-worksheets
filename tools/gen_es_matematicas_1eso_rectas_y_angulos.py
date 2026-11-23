# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Rectas y ángulos (Sentido espacial)
Complementarios y suplementarios, ángulos entre paralelas cortadas por una secante, suma de ángulos de triángulos y polígonos,
sistema sexagesimal, mediatriz y bisectriz.
Reutiliza problemas de 6.º de Primaria (relaciones, triángulos, sexagesimal) con otra semilla.
Errores: confundir alternos internos y correspondientes, sumar 360° en el triángulo, usar 180° · n para los polígonos.
"""
import math
import random
from es_eso import M, mix, unit, L, Kids, fig, use_

R = random.Random(47010)
rel, tri, sexa, prob = use_("gen_es_matematicas_6_angulos", 47910, "s2_relaciones", "s3_triangulo", "s4_sexagesimal", "s5_problema")


def g(v):
    return "%d°" % v


def paralelas(a, mark, ask):
    """dos paralelas horizontales y una secante; a = ángulo agudo de la secante con las paralelas.
    mark/ask: posición del ángulo dado y del pedido: (recta 0|1, cuadrante 'ar_d','ar_i','ab_d','ab_i')"""
    W, H = 330, 200
    ys = [60, 140]
    t = math.radians(a)
    cx = [165 + 40 / math.tan(t), 165 - 40 / math.tan(t)]
    s = ["<line x1='20' y1='%d' x2='310' y2='%d' stroke='#1565c0' stroke-width='2.4'/>" % (y, y) for y in ys]
    dx, dy = math.cos(t), -math.sin(t)
    x0, y0 = cx[1] - dx * 70, ys[1] - dy * 70
    x1, y1 = cx[0] + dx * 70, ys[0] + dy * 70
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#333' stroke-width='2.4'/>" % (x0, y0, x1, y1))

    def arc(i, q, txt, col):
        X, Y = cx[i], ys[i]
        ang = {"ar_d": (0, a), "ar_i": (a, 180), "ab_i": (180, 180 + a), "ab_d": (180 + a, 360)}[q]
        r = 22
        a1, a2 = math.radians(ang[0]), math.radians(ang[1])
        p1 = (X + r * math.cos(a1), Y - r * math.sin(a1))
        p2 = (X + r * math.cos(a2), Y - r * math.sin(a2))
        large = 1 if ang[1] - ang[0] > 180 else 0
        mid = math.radians((ang[0] + ang[1]) / 2)
        out = "<path d='M%.1f %.1f A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (p1[0], p1[1], r, r, large, p2[0], p2[1], col)
        out += "<text x='%.1f' y='%.1f' font-size='15' text-anchor='middle' fill='%s' font-family='Arial, Helvetica, sans-serif'>%s</text>" % (X + 40 * math.cos(mid), Y - 40 * math.sin(mid) + 5, col, txt)
        return out
    s.append(arc(mark[0], mark[1], g(a if mark[1] in ("ar_d", "ab_i") else 180 - a), "#c62828"))
    s.append(arc(ask[0], ask[1], "x", "#2e7d32"))
    return fig("<svg viewBox='0 0 %d %d' width='%d' role='img' aria-label='dos rectas paralelas cortadas por una secante'>%s</svg>" % (W, H, W, "".join(s)))


QS = ["ar_d", "ar_i", "ab_i", "ab_d"]


def s_paralelas():
    a = R.choice([35, 40, 45, 50, 55, 60, 65, 70, 75])
    m = (R.randint(0, 1), R.choice(QS))
    k = (1 - m[0] if R.random() < 0.7 else m[0], R.choice(QS))
    if k == m:
        return None
    vm = a if m[1] in ("ar_d", "ab_i") else 180 - a
    vk = a if k[1] in ("ar_d", "ab_i") else 180 - a
    return M(paralelas(a, m, k) + "Las rectas azules son paralelas. ¿Cuánto mide el ángulo x?", g(vk), [g(180 - vk), g(90 - min(vk, 180 - vk)), g(vk + 10)],
             "Con paralelas, los ángulos agudos son todos iguales y los obtusos también; agudo + obtuso = 180°. <b>x = %s</b>." % g(vk))


def s_poligonos():
    t = R.choice(["suma", "regular", "lados", "exterior"])
    n = R.randint(5, 12)
    S = (n - 2) * 180
    nom = {5: "pentágono", 6: "hexágono", 7: "heptágono", 8: "octógono", 9: "eneágono", 10: "decágono", 11: "endecágono", 12: "dodecágono"}[n]
    if t == "suma":
        return M("¿Cuánto suman los ángulos interiores de un %s?" % nom, g(S), [g(n * 180), g(360), g(S - 180)], "(n − 2) · 180° = %d · 180° = <b>%s</b>." % (n - 2, g(S)))
    if t == "regular":
        if S % n:
            return None
        return M("¿Cuánto mide cada ángulo interior de un %s regular?" % nom, g(S // n), [g(360 // n) if 360 % n == 0 else g(S // n - 10), g(S), g(180 - S // n) if 180 - S // n != S // n else g(S // n + 10)],
                 "%s : %d = <b>%s</b>." % (g(S), n, g(S // n)))
    if t == "exterior":
        if 360 % n:
            return None
        return M("¿Cuánto mide cada ángulo exterior de un %s regular?" % nom, g(360 // n), [g(S // n) if S % n == 0 else g(360 // n + 10), g(180 // n) if 180 % n == 0 else g(360 // n - 5), g(360)], "Los exteriores suman 360°: 360° : %d = <b>%s</b>." % (n, g(360 // n)))
    return M("Los ángulos interiores de un polígono suman %s. ¿Cuántos lados tiene?" % g(S), str(n), [str(n - 2), str(S // 180), str(n + 1)] if S // 180 != n - 2 else [str(n - 2), str(n + 2), str(n + 1)], "(n − 2) · 180° = %s → n − 2 = %d → <b>n = %d</b>." % (g(S), n - 2, n))


def s_rectas():
    q, a, w = R.choice([("¿Cómo se llama la recta perpendicular a un segmento por su punto medio?", "mediatriz", ["bisectriz", "mediana", "altura"]),
                        ("¿Cómo se llama la semirrecta que divide un ángulo en dos ángulos iguales?", "bisectriz", ["mediatriz", "mediana", "secante"]),
                        ("Los puntos de la mediatriz de AB están…", "a la misma distancia de A que de B", ["más cerca de A", "sobre el segmento AB", "a 90° de A"]),
                        ("Los puntos de la bisectriz de un ángulo están…", "a la misma distancia de los dos lados", ["sobre uno de los lados", "a la misma distancia del vértice", "fuera del ángulo"]),
                        ("Dos rectas del plano que no se cortan nunca son…", "paralelas", ["perpendiculares", "secantes", "coincidentes"]),
                        ("Dos rectas que se cortan formando cuatro ángulos rectos son…", "perpendiculares", ["paralelas", "oblicuas", "coincidentes"]),
                        ("¿Cuántos ángulos rectos tiene un ángulo llano?", "2", ["1", "3", "4"]),
                        ("El punto donde se cortan las tres mediatrices de un triángulo se llama…", "circuncentro", ["incentro", "baricentro", "ortocentro"]),
                        ("El punto donde se cortan las tres bisectrices de un triángulo se llama…", "incentro", ["circuncentro", "baricentro", "ortocentro"]),
                        ("¿Qué centro del triángulo es el centro de la circunferencia que pasa por los tres vértices?", "el circuncentro", ["el incentro", "el baricentro", "el ortocentro"]),
                        ("Si un ángulo mide 90° 0′ 0″ − 35° 20′, ¿cuánto queda?", "54° 40′", ["55° 20′", "65° 40′", "54° 80′"]),
                        ("Si un ángulo es el doble de su complementario, ¿cuánto mide?", "60°", ["45°", "30°", "120°"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


seen = set()
sets = [("Complementarios, suplementarios y opuestos", mix(R, seen, [(rel, 14), (s_rectas, 6)])), ("Ángulos entre paralelas", mix(R, seen, [(s_paralelas, 20)])),
        ("Triángulos y polígonos", mix(R, seen, [(tri, 10), (s_poligonos, 10)])), ("Grados, minutos y segundos", mix(R, seen, [(sexa, 16), (s_rectas, 4)])), ("Problemas", mix(R, seen, [(prob, 14), (s_poligonos, 6)]))]
body = L(["Complementarios: suman 90°. Suplementarios: suman 180°. Opuestos por el vértice: son iguales.",
          "Si una secante corta a dos paralelas, todos los ángulos agudos que forma son iguales, y los obtusos también.",
          "Los ángulos de un triángulo suman 180°. Los de un polígono de n lados suman (n − 2) · 180°."],
         [("Ángulos de un hexágono", ["(6 − 2) · 180°"], "720°; cada uno, si es regular, 120°"), ("45° 50′ + 30° 25′", ["75° 75′", "75′ = 1° 15′"], "76° 15′")],
         [["Confundir complementario y suplementario", "Complementario: 90°. Suplementario: 180°."], ["Sumar 360° en el triángulo", "Triángulo: 180°. Cuadrilátero: 360°."], ["Pasar 60′ como 100′", "1° = 60′ y 1′ = 60″."]],
         paralelas(55, (0, "ar_d"), (1, "ar_d")))
faq = [("¿Cuánto suman los ángulos de un polígono?", "(n − 2) · 180°, siendo n el número de lados. Un pentágono: 3 · 180° = 540°."),
       ("¿Qué ángulos son iguales entre paralelas?", "Los correspondientes, los alternos internos y los alternos externos.")]
unit(1, R, "rectas-y-angulos", "E", "Rectas y ángulos: relaciones entre ángulos, ángulos entre rectas paralelas y secantes, mediatriz y bisectriz; suma de los ángulos de un polígono; sistema sexagesimal",
     "Rectas y ángulos", "Rectas y ángulos",
     "Fichas de matemáticas de 1.º de ESO: complementarios y suplementarios, ángulos entre paralelas, ángulos de polígonos, grados y minutos. 100 ejercicios con soluciones.",
     "Polígono de n lados: (n − 2) · 180°", "Triángulo 180°, cuadrilátero 360°.", body, faq, sets, 10)
