# -*- coding: utf-8 -*-
"""España / 1.º de Bachillerato: Biología, Geología y Ciencias Ambientales; Física y Química"""
import math
from es_sci import H, nq, num, it

D = "¿Qué corresponde a esta descripción: {v}?"
G = 9.8
RG = 0.082


def f_gases(R):
    k = R.choice(["pv", "n", "boyle", "charles", "dens", "molar"])
    if k == "pv":
        n, T, V = R.choice([(1, 273, 22.4), (2, 300, 10), (0.5, 400, 5), (3, 250, 20), (1, 350, 8), (0.2, 300, 1)])
        p = n * RG * T / V
        return nq("¿Qué presión ejercen %s mol de gas a %s K en %s L? (R = 0,082 atm·L/(mol·K))" % (num(n), T, num(V)), p, [n * RG * V / T, n * T / V, p * 760], "atm",
                  "p = n · R · T : V = %s · 0,082 · %s : %s = %s atm." % (num(n), T, num(V), num(p)))
    if k == "n":
        p, V, T = R.choice([(1, 24.6, 300), (2, 10, 273), (0.5, 41, 500), (3, 8.2, 300), (1.5, 20, 350)])
        n = p * V / (RG * T)
        return nq("Un gas ocupa %s L a %s atm y %s K. ¿Cuántos moles hay? (R = 0,082 atm·L/(mol·K))" % (num(V), num(p), T), n, [p * V * RG * T, p * V / T, RG * T / (p * V)], "mol",
                  "n = p · V : (R · T) = %s · %s : (0,082 · %s) = %s mol." % (num(p), num(V), T, num(n)))
    if k == "boyle":
        p1, V1, p2 = R.choice([(1, 10, 2), (2, 6, 3), (1, 20, 4), (3, 4, 1), (0.5, 8, 2)])
        return nq("Un gas ocupa %s L a %s atm. A temperatura constante se lleva a %s atm. ¿Qué volumen ocupa?" % (V1, num(p1), num(p2)), p1 * V1 / p2, [p2 * V1 / p1, p1 * p2 / V1, V1], "L",
                  "Boyle: p₁ · V₁ = p₂ · V₂ → V₂ = %s · %s : %s = %s L." % (num(p1), V1, num(p2), num(p1 * V1 / p2)))
    if k == "charles":
        V1, T1, T2 = R.choice([(2, 300, 450), (10, 273, 546), (5, 250, 300), (3, 400, 200), (6, 300, 350)])
        return nq("Un gas ocupa %s L a %s K. A presión constante se calienta a %s K. ¿Qué volumen ocupa?" % (V1, T1, T2), V1 * T2 / T1, [V1 * T1 / T2, V1 + (T2 - T1), V1], "L",
                  "Charles: V₁ : T₁ = V₂ : T₂ → V₂ = %s · %s : %s = %s L." % (V1, T2, T1, num(V1 * T2 / T1)))
    if k == "dens":
        M, T = R.choice([(32, 273), (44, 300), (28, 273), (2, 300), (16, 400)])
        d = M / (RG * T)
        return nq("¿Qué densidad tiene un gas de masa molar %s g/mol a 1 atm y %s K?" % (M, T), d, [M * RG * T, M / T, RG * T / M], "g/L",
                  "d = p · M : (R · T) = 1 · %s : (0,082 · %s) = %s g/L." % (M, T, num(d)))
    m, M = R.choice([(16, 32), (8.8, 44), (2, 2), (5.6, 28), (3.4, 17)])
    n = m / M
    return nq("¿Qué volumen ocupan %s g de un gas de masa molar %s g/mol en condiciones normales? (22,4 L/mol)" % (num(m), M), n * 22.4, [m * 22.4, 22.4 / n, n * 24.5], "L",
              "n = %s : %s = %s mol; V = %s · 22,4 = %s L." % (num(m), M, num(n), num(n), num(n * 22.4)))


def f_disol(R):
    k = R.choice(["M", "M", "dil", "pct", "x"])
    if k == "M":
        m, Mm, V = R.choice([(5.85, 58.5, 0.5), (4, 40, 0.25), (9.8, 98, 2), (18, 180, 0.5), (11.7, 58.5, 1), (2, 40, 0.1)])
        c = m / Mm / V
        return nq("Se disuelven %s g de soluto (M = %s g/mol) hasta %s L. ¿Molaridad?" % (num(m), num(Mm), num(V)), c, [m / V, m / Mm * V, c * 1000], "mol/L",
                  "n = %s : %s = %s mol; c = %s : %s = %s mol/L." % (num(m), num(Mm), num(m / Mm), num(m / Mm), num(V), num(c)))
    if k == "dil":
        c1, V1, V2 = R.choice([(2, 0.1, 0.5), (1, 0.05, 0.25), (6, 0.02, 0.6), (0.5, 0.2, 1), (3, 0.01, 0.15)])
        return nq("Se diluyen %s L de una disolución %s M hasta %s L. ¿Nueva concentración?" % (num(V1), num(c1), num(V2)), c1 * V1 / V2, [c1 * V2 / V1, c1, c1 * V1], "mol/L",
                  "c₁ · V₁ = c₂ · V₂ → c₂ = %s · %s : %s = %s mol/L." % (num(c1), num(V1), num(V2), num(c1 * V1 / V2)))
    if k == "pct":
        ms, md = R.choice([(15, 135), (20, 80), (5, 245), (30, 170), (12, 188)])
        p = ms / (ms + md) * 100
        return nq("Se mezclan %s g de soluto con %s g de disolvente. ¿Porcentaje en masa?" % (ms, md), p, [ms / md * 100, md / (ms + md) * 100, ms + md], "%",
                  "%% = %s : %s · 100 = %s %%." % (ms, ms + md, num(p)))
    na, nb = R.choice([(1, 4), (2, 8), (0.5, 4.5), (1, 9), (3, 7)])
    return nq("Una disolución tiene %s mol de soluto y %s mol de disolvente. ¿Fracción molar del soluto?" % (num(na), num(nb)), na / (na + nb), [na / nb, nb / (na + nb), na * nb], "",
              "χ = %s : (%s + %s) = %s." % (num(na), num(na), num(nb), num(na / (na + nb))))


def f_termo(R):
    k = R.choice(["dh", "dh", "limit", "rend"])
    if k == "dh":
        f, Mm, dH = R.choice([("metano", 16, -890), ("propano", 44, -2220), ("butano", 58, -2878), ("etanol", 46, -1367), ("glucosa", 180, -2803)])
        m = R.choice([1, 2, 0.5, 3, 0.25]) * Mm
        q = m / Mm * dH
        return nq("La entalpía de combustión del %s es %s kJ/mol (M = %s g/mol). ¿Qué energía desprenden %s g?" % (f, num(dH), Mm, num(m)), abs(q), [abs(dH), abs(dH) * m, abs(dH) / m], "kJ",
                  "n = %s : %s = %s mol; Q = %s · %s = %s kJ (se desprenden)." % (num(m), Mm, num(m / Mm), num(m / Mm), num(abs(dH)), num(abs(q))))
    if k == "limit":
        a, b = R.choice([(4, 16), (4, 64), (6, 32), (2, 32), (8, 32)])
        nH, nO = a / 2, b / 32
        lim = "H₂" if nH / 2 < nO else "O₂"
        w = 18 * min(nH, 2 * nO)
        return nq("Reaccionan %s g de H₂ con %s g de O₂ (2 H₂ + O₂ → 2 H₂O). ¿Qué masa de agua se forma como máximo?" % (a, b), w, [(a + b), 18 * max(nH, 2 * nO), 18 * nH * 2], "g",
                  "n(H₂) = %s mol y n(O₂) = %s mol; el reactivo limitante es el %s: se forman %s g de agua." % (num(nH), num(nO), lim, num(w)))
    t, r = R.choice([(88, 70.4), (36, 30.6), (120, 96), (56, 50.4), (200, 170)])
    return nq("Se esperaban %s g de producto y se obtienen %s g. ¿Rendimiento?" % (num(t), num(r)), r / t * 100, [t / r * 100, (t - r) / t * 100, r / t], "%",
              "Rendimiento = %s : %s · 100 = %s %%." % (num(r), num(t), num(r / t * 100)))


def f_cine(R):
    k = R.choice(["alc", "tvuelo", "hmax", "vert", "horiz", "omega"])
    if k in ("alc", "tvuelo", "hmax"):
        v0, ang = R.choice([(20, 30), (20, 45), (30, 60), (10, 45), (25, 30), (40, 45), (15, 60), (30, 30), (12, 45), (35, 40), (18, 50)])
        a = math.radians(ang)
        tv = 2 * v0 * math.sin(a) / G
        if k == "alc":
            x = v0 * v0 * math.sin(2 * a) / G
            return nq("Se lanza un proyectil a %s m/s con %s° sobre la horizontal. ¿Qué alcance tiene en terreno llano? (g = 9,8 m/s²)" % (v0, ang), x, [v0 * v0 / G, x / 2, v0 * tv], "m",
                      "x = v₀² · sen(2α) : g = %s² · sen %s° : 9,8 = %s m." % (v0, 2 * ang, num(x)))
        if k == "tvuelo":
            return nq("Un proyectil sale a %s m/s con %s°. ¿Cuánto tiempo está en el aire? (g = 9,8 m/s²)" % (v0, ang), tv, [tv / 2, v0 / G, 2 * v0 / G * math.cos(a)], "s",
                      "t = 2 · v₀ · sen α : g = 2 · %s · sen %s° : 9,8 = %s s." % (v0, ang, num(tv)))
        h = (v0 * math.sin(a)) ** 2 / (2 * G)
        return nq("Un proyectil sale a %s m/s con %s°. ¿Qué altura máxima alcanza? (g = 9,8 m/s²)" % (v0, ang), h, [v0 * v0 / (2 * G), 2 * h, (v0 * math.sin(a)) ** 2 / G], "m",
                  "h = (v₀ · sen α)² : (2g) = %s m." % num(h))
    if k == "vert":
        v0 = R.choice([10, 20, 15, 30, 25, 12, 8, 18])
        return nq("Se lanza una pelota hacia arriba a %s m/s. ¿Qué altura máxima alcanza? (g = 9,8 m/s²)" % v0, v0 * v0 / (2 * G), [v0 * v0 / G, v0 / G, v0 * v0 / (2 * G) * 2], "m",
                  "h = v₀² : (2g) = %s : 19,6 = %s m." % (v0 * v0, num(v0 * v0 / (2 * G))))
    if k == "horiz":
        v0, h = R.choice([(10, 20), (5, 45), (20, 5), (15, 80), (8, 10), (12, 30), (6, 1.2), (25, 60)])
        t = math.sqrt(2 * h / G)
        return nq("Una bola sale horizontalmente a %s m/s desde %s m de altura. ¿A qué distancia horizontal cae? (g = 9,8 m/s²)" % (v0, h), v0 * t, [v0 * h / G, v0 * 2 * h / G, t], "m",
                  "t = √(2h : g) = %s s; x = v₀ · t = %s · %s = %s m." % (num(t), v0, num(t), num(v0 * t)))
    rpm, r = R.choice([(60, 0.5), (120, 0.2), (30, 2), (300, 0.1), (45, 0.15), (90, 0.3), (600, 0.05)])
    w = rpm * 2 * math.pi / 60
    return nq("Una rueda de %s m de radio gira a %s rpm. ¿Qué velocidad lineal tiene un punto del borde?" % (num(r), rpm), w * r, [rpm * r, w, rpm / 60 * r], "m/s",
              "ω = %s · 2π : 60 = %s rad/s; v = ω · r = %s m/s." % (rpm, num(w), num(w * r)))


def f_dina(R):
    k = R.choice(["plano", "plano", "polea", "ascensor", "curva", "mu"])
    if k == "plano":
        ang, mu = R.choice([(30, 0), (30, 0.2), (45, 0.1), (37, 0.3), (60, 0.2), (20, 0)])
        a = G * (math.sin(math.radians(ang)) - mu * math.cos(math.radians(ang)))
        if a <= 0:
            return None
        return nq("Un bloque baja por un plano inclinado %s° con μ = %s. ¿Qué aceleración tiene? (g = 9,8 m/s²)" % (ang, num(mu)), a, [G * math.sin(math.radians(ang)) if mu else G * math.cos(math.radians(ang)), G, G * math.tan(math.radians(ang))], "m/s²",
                  "a = g · (sen α − μ · cos α) = 9,8 · (sen %s° − %s · cos %s°) = %s m/s²." % (ang, num(mu), ang, num(a)))
    if k == "polea":
        m1, m2 = R.choice([(3, 2), (5, 3), (4, 1), (6, 4), (10, 5)])
        a = (m1 - m2) * G / (m1 + m2)
        return nq("En una máquina de Atwood cuelgan %s kg y %s kg. ¿Qué aceleración tiene el sistema? (g = 9,8 m/s²)" % (m1, m2), a, [(m1 - m2) * G / m1, G, (m1 + m2) * G / (m1 - m2)], "m/s²",
                  "a = (m₁ − m₂) · g : (m₁ + m₂) = %s · 9,8 : %s = %s m/s²." % (m1 - m2, m1 + m2, num(a)))
    if k == "ascensor":
        m, a = R.choice([(60, 2), (70, 1.5), (50, 3), (80, 1), (65, 2.5)])
        return nq("Una persona de %s kg está en un ascensor que sube acelerando a %s m/s². ¿Qué marca la báscula, en newtons? (g = 9,8 m/s²)" % (m, num(a)), m * (G + a), [m * G, m * (G - a), m * a], "N",
                  "N − P = m · a → N = m · (g + a) = %s · %s = %s N." % (m, num(G + a), num(m * (G + a))))
    if k == "curva":
        r, mu = R.choice([(50, 0.5), (100, 0.4), (30, 0.6), (80, 0.8), (200, 0.3)])
        v = math.sqrt(mu * G * r)
        return nq("¿Qué velocidad máxima puede llevar un coche en una curva plana de %s m de radio si μ = %s? (g = 9,8 m/s²)" % (r, num(mu)), v, [mu * G * r, math.sqrt(G * r), v * 3.6], "m/s",
                  "μ · m · g = m · v² : r → v = √(μ · g · r) = %s m/s." % num(v))
    F, m, a = R.choice([(100, 20, 3), (60, 10, 4), (200, 40, 4), (150, 25, 5)])
    mu = (F - m * a) / (m * G)
    if mu <= 0:
        return None
    return nq("Se arrastra una caja de %s kg con %s N horizontales y acelera a %s m/s². ¿Cuál es el coeficiente de rozamiento? (g = 9,8 m/s²)" % (m, F, a), mu, [F / (m * G), (F + m * a) / (m * G), m * a / F], "",
              "F − μ · m · g = m · a → μ = (%s − %s) : (%s · 9,8) = %s." % (F, m * a, m, num(mu)))


def f_ener(R):
    k = R.choice(["cons", "roz", "muelle", "P", "W"])
    if k == "cons":
        h1, h2 = R.choice([(20, 5), (45, 0), (30, 10), (12, 2), (80, 35)])
        v = math.sqrt(2 * G * (h1 - h2))
        return nq("Una vagoneta parte del reposo a %s m de altura. ¿Qué velocidad tiene a %s m, sin rozamiento? (g = 9,8 m/s²)" % (h1, h2), v, [math.sqrt(2 * G * h1), 2 * G * (h1 - h2), math.sqrt(G * (h1 - h2))], "m/s",
                  "m · g · (h₁ − h₂) = ½ · m · v² → v = √(2 · 9,8 · %s) = %s m/s." % (h1 - h2, num(v)))
    if k == "roz":
        m, v0, d = R.choice([(2, 10, 20), (1000, 20, 50), (5, 6, 9), (0.5, 8, 4), (80, 5, 10)])
        Fr = 0.5 * m * v0 * v0 / d
        return nq("Un cuerpo de %s kg a %s m/s se para tras recorrer %s m. ¿Qué fuerza de rozamiento media actuó?" % (num(m), v0, d), Fr, [m * v0 / d, 0.5 * m * v0 * v0, m * v0 * v0 / d], "N",
                  "Teorema de las fuerzas vivas: Fr · d = ½ · m · v₀² → Fr = %s N." % num(Fr))
    if k == "muelle":
        kk, x = R.choice([(200, 0.1), (500, 0.05), (1000, 0.2), (50, 0.3), (800, 0.15)])
        return nq("¿Qué energía potencial elástica tiene un muelle de %s N/m comprimido %s m?" % (kk, num(x)), 0.5 * kk * x * x, [kk * x, kk * x * x, 0.5 * kk * x], "J",
                  "Ep = ½ · k · x² = 0,5 · %s · %s² = %s J." % (kk, num(x), num(0.5 * kk * x * x)))
    if k == "P":
        m, h, t = R.choice([(500, 10, 20), (100, 20, 10), (1000, 15, 30), (60, 3, 4), (200, 5, 8)])
        P = m * G * h / t
        return nq("Una grúa sube %s kg a %s m en %s s. ¿Qué potencia útil desarrolla? (g = 9,8 m/s²)" % (m, h, t), P, [m * h / t, m * G * h, m * G * h * t], "W",
                  "P = m · g · h : t = %s · 9,8 · %s : %s = %s W." % (m, h, t, num(P)))
    F, d, ang = R.choice([(100, 5, 60), (50, 10, 30), (200, 3, 45), (80, 4, 0)])
    W = F * d * math.cos(math.radians(ang))
    return nq("Una fuerza de %s N forma %s° con un desplazamiento de %s m. ¿Qué trabajo realiza?" % (F, ang, d), W, [F * d, F * d * math.sin(math.radians(ang)) if ang else F * d / 2, F * math.cos(math.radians(ang))], "J",
              "W = F · d · cos α = %s · %s · cos %s° = %s J." % (F, d, ang, num(W)))


def UNITS(grade):
    return [
        H("BG", "ecologia-y-sostenibilidad", "Ecología y sostenibilidad", "Ecología",
          "Los alumnos analizan el medio ambiente como sistema, la dinámica de los ecosistemas, los ciclos biogeoquímicos, la huella ecológica y los impactos y medidas de sostenibilidad, con indicadores ambientales.",
          "sistema, ecosfera, biotopo, biocenosis, flujo de energía, producción primaria, ciclos biogeoquímicos, sucesión, autorregulación, huella ecológica, desarrollo sostenible, Agenda 2030",
          "La energía fluye; la materia circula en ciclos", "La sostenibilidad es satisfacer nuestras necesidades sin comprometer las de las generaciones futuras.",
          ["La ecosfera es un sistema con subsistemas (atmósfera, hidrosfera, geosfera, biosfera) que intercambian materia y energía.",
           "La producción primaria es la materia orgánica que fabrican los productores. La energía se pierde en cada nivel trófico (regla del 10 %).",
           "Los ciclos del carbono, nitrógeno, fósforo y agua reciclan la materia. Las actividades humanas los alteran: cambio climático, eutrofización, pérdida de biodiversidad."],
          [("¿Qué bacterias fijan el nitrógeno atmosférico?", ["Las plantas no pueden usar el N₂ del aire.", "Algunas bacterias viven en nódulos de las leguminosas."], "Las bacterias del género Rhizobium, entre otras.")],
          [("La huella ecológica mide solo la contaminación.", "Mide la superficie productiva necesaria para mantener nuestro consumo."), ("Los ecosistemas maduros crecen sin límite.", "Alcanzan un equilibrio con alta biomasa y baja productividad neta.")],
          [("¿Qué es la Agenda 2030?", "El plan de Naciones Unidas con 17 Objetivos de Desarrollo Sostenible."), ("¿Qué es un bucle de realimentación positiva?", "Un efecto que refuerza su causa, como el deshielo que reduce el albedo y calienta más.")],
          [("Ciclos biogeoquímicos", [("fijación del nitrógeno", "bacterias transforman N₂ en compuestos utilizables"), ("nitrificación", "bacterias oxidan el amonio a nitratos"), ("desnitrificación", "bacterias devuelven N₂ a la atmósfera"),
                                      ("fotosíntesis", "retira CO₂ y fija el carbono en materia orgánica"), ("respiración", "devuelve CO₂ a la atmósfera"), ("meteorización de las rocas", "libera fósforo al suelo"),
                                      ("sedimentación de carbonatos", "almacena carbono en rocas calizas")],
            "¿Qué ocurre en: {k}?", D),
           ("Conceptos", [("producción primaria bruta", "materia orgánica total que fabrican los productores"), ("producción neta", "lo que queda tras la respiración"), ("biomasa", "masa de materia orgánica"),
                          ("huella ecológica", "superficie necesaria para sostener el consumo"), ("capacidad de carga", "población máxima que soporta un ambiente"), ("resiliencia", "capacidad de recuperarse tras una perturbación"),
                          ("bioacumulación", "concentración de un tóxico a lo largo de la cadena trófica")],
            "¿Qué es: {k}?", D),
           ("Realimentación", {"los bucles de realimentación positiva": ["deshielo que reduce el albedo y calienta más", "incendios que liberan CO₂ y aumentan el calentamiento", "deshielo del permafrost que libera metano",
                                                                       "deforestación que reduce las lluvias", "erosión que empobrece el suelo y reduce la vegetación"],
                               "los bucles de realimentación negativa": ["más CO₂ estimula la fotosíntesis", "más depredadores reducen las presas y luego a sí mismos", "más evaporación forma nubes que enfrían",
                                                                         "la sudoración que enfría el cuerpo", "la meteorización de silicatos que retira CO₂"]})],
          ["La energía fluye y la materia circula en ciclos.", "Rhizobium fija nitrógeno.", "La desnitrificación devuelve N₂ a la atmósfera.", "La huella ecológica mide superficie productiva.", "Los ecosistemas maduros tienen alta biomasa.",
           "La Agenda 2030 tiene 17 objetivos.", "La bioacumulación aumenta en los niveles tróficos superiores."],
          [("La energía se recicla en los ecosistemas.", "Fluye y se disipa."), ("La desnitrificación fija nitrógeno.", "Lo devuelve a la atmósfera."), ("La huella ecológica mide solo la contaminación.", "Mide superficie productiva."),
           ("La bioacumulación disminuye en la cadena.", "Aumenta."), ("Los ecosistemas jóvenes tienen máxima biomasa.", "La tienen los maduros.")],
          "la ecología y la sostenibilidad", "living-things-and-ecosystems"),

        H("BG", "historia-de-la-tierra-y-de-la-vida", "La historia de la Tierra y de la vida", "Historia de la Tierra",
          "Los alumnos aplican métodos de datación relativa y absoluta, interpretan cortes geológicos, describen los grandes eones y eras, las extinciones masivas y la evolución de la vida y de la atmósfera.",
          "datación relativa y absoluta, principios estratigráficos, discordancia, isótopos radiactivos, semivida, fósiles guía, tabla cronoestratigráfica, eones, extinciones masivas, Gran Oxidación",
          "Datación absoluta con isótopos radiactivos", "La atmósfera se enriqueció en oxígeno gracias a las cianobacterias.",
          ["Los principios de superposición, horizontalidad original, continuidad lateral, intersección e inclusión permiten ordenar los acontecimientos de un corte geológico.",
           "La datación absoluta usa isótopos con semivida conocida: tras una semivida queda la mitad del isótopo inicial.",
           "Eones: Hádico, Arcaico, Proterozoico y Fanerozoico. La Gran Oxidación (hace unos 2400 millones de años) llenó de oxígeno la atmósfera. Ha habido cinco extinciones masivas."],
          [("Una muestra conserva 1/4 del carbono-14 inicial (semivida 5730 años). ¿Qué edad tiene?", ["1/4 son dos semividas.", "2 · 5730 = 11 460."], "Unos 11 460 años.")],
          [("El carbono-14 sirve para datar dinosaurios.", "Solo sirve hasta unos 50 000 años; para rocas antiguas se usan uranio-plomo o potasio-argón."), ("Una discordancia es un estrato.", "Es una superficie de erosión o interrupción entre series de estratos.")],
          [("¿Qué son los estromatolitos?", "Estructuras de capas formadas por cianobacterias; algunas tienen más de 3000 millones de años."), ("¿Cuál fue la mayor extinción?", "La del final del Pérmico, hace unos 252 millones de años.")],
          [("Eones y eras", [("Hádico", "formación de la Tierra y la Luna"), ("Arcaico", "primeras células procariotas"), ("Proterozoico", "Gran Oxidación y primeras eucariotas"), ("Paleozoico", "explosión del Cámbrico y conquista de la tierra"),
                             ("Mesozoico", "dinosaurios y primeras plantas con flores"), ("Cenozoico", "diversificación de mamíferos y aparición humana")],
            "¿Qué ocurrió en el {k}?", "¿En qué división del tiempo hubo {v}?", ["Cuaternario sin vida"]),
           ("Métodos de datación", [("carbono-14", "restos orgánicos de hasta unos 50 000 años"), ("uranio-plomo", "rocas muy antiguas, de millones de años"), ("potasio-argón", "rocas volcánicas"),
                                    ("dendrocronología", "anillos de crecimiento de los árboles"), ("varvas", "capas anuales de sedimentos en lagos glaciares"), ("fósiles guía", "datación relativa de estratos")],
            "¿Para qué se usa: {k}?", "¿Qué método se usa para {v}?"),
           ("Extinciones", [("extinción del Ordovícico", "glaciación que eliminó mucha vida marina"), ("extinción del Devónico", "crisis de los arrecifes marinos"), ("extinción del Pérmico", "la mayor, con grandes erupciones en Siberia"),
                            ("extinción del Triásico", "abrió paso al dominio de los dinosaurios"), ("extinción del Cretácico", "impacto de un asteroide en Yucatán")],
            "¿Qué caracteriza a la {k}?", D, ["no hubo extinción"])],
          ["Tras una semivida queda la mitad del isótopo.", "El carbono-14 data restos de hasta unos 50 000 años.", "Las cianobacterias causaron la Gran Oxidación.", "La mayor extinción fue la del Pérmico.",
           "Los dinosaurios dominaron el Mesozoico.", "Ha habido cinco grandes extinciones masivas.", "Lo que corta a un estrato es posterior a él."],
          [("El carbono-14 data dinosaurios.", "Solo hasta unos 50 000 años."), ("La atmósfera primitiva tenía mucho oxígeno.", "Casi no tenía."), ("La extinción del Cretácico fue la mayor.", "Fue la del Pérmico."),
           ("Tras una semivida no queda isótopo.", "Queda la mitad."), ("Una discordancia es un fósil.", "Es una superficie de interrupción.")],
          "la historia de la Tierra", "earths-systems"),

        H("BG", "dinamica-y-composicion-terrestre", "Dinámica terrestre: minerales, rocas y procesos", "Dinámica terrestre",
          "Los alumnos describen los métodos de estudio del interior terrestre, la tectónica de placas, los procesos magmáticos, metamórficos y sedimentarios, la clasificación de minerales y rocas y los riesgos geológicos.",
          "ondas sísmicas, discontinuidades, modelo geoquímico y dinámico, tectónica de placas, magmatismo, metamorfismo, sedimentación, silicatos, rocas ígneas, metamórficas y sedimentarias, riesgos geológicos",
          "Las ondas sísmicas revelan el interior de la Tierra", "Las ondas S no atraviesan el núcleo externo porque es líquido.",
          ["Las ondas sísmicas P y S cambian de velocidad en las discontinuidades: Mohorovičić (corteza-manto) y Gutenberg (manto-núcleo).",
           "Los procesos internos (magmatismo, metamorfismo, tectónica) y externos (meteorización, erosión, sedimentación) forman el ciclo de las rocas.",
           "Los silicatos son los minerales más abundantes. Las rocas ígneas pueden ser plutónicas (granito) o volcánicas (basalto)."],
          [("¿Por qué las ondas S no llegan al lado opuesto de la Tierra?", ["Las ondas S no se propagan en líquidos.", "El núcleo externo es líquido."], "Porque el núcleo externo es líquido.")],
          [("El granito y el basalto se forman igual.", "El granito se enfría lento en profundidad; el basalto, rápido en la superficie."), ("El metamorfismo funde las rocas.", "Las transforma en estado sólido.")],
          [("¿Qué es la discontinuidad de Mohorovičić?", "El límite entre la corteza y el manto."), ("¿Qué riesgo volcánico es más peligroso?", "Las nubes ardientes o flujos piroclásticos.")],
          [("Rocas", [("granito", "ígnea plutónica"), ("gabro", "ígnea plutónica"), ("basalto", "ígnea volcánica"), ("riolita", "ígnea volcánica"), ("pizarra", "metamórfica"), ("mármol", "metamórfica"),
                      ("gneis", "metamórfica"), ("arenisca", "sedimentaria detrítica"), ("conglomerado", "sedimentaria detrítica"), ("caliza", "sedimentaria química u orgánica"), ("yeso", "sedimentaria química u orgánica")],
            "¿Qué tipo de roca es: {k}?", None),
           ("Interior terrestre", [("discontinuidad de Mohorovičić", "límite entre corteza y manto"), ("discontinuidad de Gutenberg", "límite entre manto y núcleo"), ("discontinuidad de Lehmann", "límite entre núcleo externo e interno"),
                                   ("ondas P", "ondas longitudinales que atraviesan sólidos y líquidos"), ("ondas S", "ondas transversales que no atraviesan líquidos"), ("astenosfera", "zona del manto superior más plástica"),
                                   ("zona de sombra", "región donde no llegan ondas P o S directas")],
            "¿Qué es: {k}?", D),
           ("Procesos", [("enfriamiento lento del magma en profundidad", "formación de rocas plutónicas"), ("erupción y enfriamiento rápido de lava", "formación de rocas volcánicas"),
                         ("presión y temperatura sin fusión", "metamorfismo"), ("compactación y cementación de sedimentos", "diagénesis"), ("rotura de rocas por hielo en las grietas", "gelifracción"),
                         ("disolución de la caliza por agua con CO₂", "karstificación"), ("una placa se hunde bajo otra", "subducción")],
            "¿Qué proceso es: {k}?", None)],
          ["Las ondas S no atraviesan líquidos.", "La discontinuidad de Gutenberg separa manto y núcleo.", "El granito es una roca plutónica.", "El mármol es metamórfico.", "Los silicatos son los minerales más abundantes.",
           "El metamorfismo ocurre en estado sólido.", "El basalto se enfría rápido."],
          [("Las ondas S atraviesan el núcleo externo.", "No lo atraviesan."), ("El metamorfismo funde las rocas.", "Ocurre en estado sólido."), ("El basalto es plutónico.", "Es volcánico."),
           ("La Mohorovičić separa manto y núcleo.", "Separa corteza y manto."), ("La caliza es metamórfica.", "Es sedimentaria.")],
          "la dinámica terrestre", "earths-systems"),

        H("BG", "fisiologia-e-histologia-animal", "Fisiología e histología animal", "Fisiología animal",
          "Los alumnos describen los tejidos animales y comparan la nutrición (digestión, respiración, circulación, excreción), la relación (nervios y hormonas) y la reproducción en distintos grupos animales.",
          "tejido epitelial, conectivo, muscular, nervioso, respiración branquial, traqueal, cutánea y pulmonar, circulación abierta y cerrada, simple y doble, excreción, osmorregulación, homeostasis",
          "Cada grupo animal resuelve la nutrición a su manera", "La circulación doble y completa separa la sangre oxigenada de la no oxigenada.",
          ["Los animales tienen cuatro tipos de tejidos: epitelial, conectivo (óseo, cartilaginoso, adiposo, sanguíneo), muscular y nervioso.",
           "Respiración: branquial (peces), traqueal (insectos), cutánea (anfibios) y pulmonar (vertebrados terrestres). Circulación: abierta (artrópodos, moluscos) o cerrada; simple (peces) o doble (aves y mamíferos).",
           "La excreción elimina desechos nitrogenados: amoniaco (peces), urea (mamíferos) o ácido úrico (aves, reptiles e insectos)."],
          [("¿Qué desecho nitrogenado excretan las aves?", ["Necesitan ahorrar agua y peso.", "Es casi insoluble."], "Ácido úrico.")],
          [("Todos los animales tienen sangre roja.", "Muchos invertebrados tienen hemolinfa sin hemoglobina."), ("Los insectos respiran por pulmones.", "Respiran por tráqueas.")],
          [("¿Qué es la homeostasis?", "El mantenimiento de un medio interno estable."), ("¿Por qué el corazón de los peces tiene dos cavidades?", "Su circulación es simple: la sangre pasa una vez por el corazón en cada vuelta.")],
          [("Respiración", [("trucha", "branquial"), ("tiburón", "branquial"), ("renacuajo", "branquial"), ("saltamontes", "traqueal"), ("hormiga", "traqueal"), ("lombriz de tierra", "cutánea"),
                            ("rana adulta", "pulmonar y cutánea"), ("lagarto", "pulmonar"), ("paloma", "pulmonar con sacos aéreos"), ("ballena", "pulmonar")],
            "¿Qué respiración tiene: {k}?", None),
           ("Circulación", [("insecto", "abierta"), ("caracol", "abierta"), ("lombriz", "cerrada sencilla sin corazón definido"), ("pez", "cerrada simple"), ("anfibio", "cerrada doble incompleta"),
                            ("ave", "cerrada doble completa"), ("mamífero", "cerrada doble completa")],
            "¿Qué tipo de circulación tiene: {k}?", None),
           ("Tejidos", [("epitelio de revestimiento", "células muy unidas que cubren superficies"), ("tejido óseo", "matriz dura de fosfato cálcico"), ("tejido cartilaginoso", "matriz flexible sin vasos sanguíneos"),
                        ("tejido adiposo", "células llenas de grasa"), ("músculo estriado esquelético", "contracción voluntaria"), ("músculo liso", "contracción involuntaria lenta"),
                        ("músculo cardíaco", "estriado e involuntario"), ("tejido nervioso", "neuronas y células de glía")],
            "¿Cómo es: {k}?", D)],
          ["Los insectos respiran por tráqueas.", "Las aves excretan ácido úrico.", "Los peces tienen circulación simple.", "Los mamíferos tienen circulación doble y completa.", "El músculo liso es involuntario.",
           "La homeostasis mantiene estable el medio interno.", "El cartílago no tiene vasos sanguíneos."],
          [("Los insectos respiran por pulmones.", "Por tráqueas."), ("Los peces tienen circulación doble.", "Es simple."), ("Las aves excretan amoniaco.", "Ácido úrico."), ("El músculo cardíaco es voluntario.", "Es involuntario."),
           ("Todos los animales tienen sangre roja.", "No todos.")],
          "la fisiología animal", "living-things-and-ecosystems"),

        H("BG", "fisiologia-e-histologia-vegetal", "Fisiología e histología vegetal", "Fisiología vegetal",
          "Los alumnos describen los tejidos vegetales, la absorción y el transporte de savia, la fotosíntesis y sus fases, la respiración, las hormonas vegetales, los tropismos y la reproducción de las plantas.",
          "meristemos, parénquima, colénquima, esclerénquima, xilema, floema, epidermis, estomas, savia bruta y elaborada, transpiración, fotosíntesis, fase luminosa, ciclo de Calvin, fitohormonas, tropismos",
          "El xilema sube savia bruta; el floema reparte la elaborada", "La transpiración por los estomas tira del agua desde la raíz.",
          ["Los meristemos tienen células que se dividen. El xilema transporta savia bruta hacia arriba; el floema, savia elaborada a toda la planta.",
           "La fotosíntesis tiene una fase luminosa (en los tilacoides: se rompe el agua y se libera O₂) y otra oscura o ciclo de Calvin (en el estroma: se fija el CO₂).",
           "Las fitohormonas regulan el desarrollo: auxinas (crecimiento y tropismos), giberelinas (germinación), citoquininas (división), etileno (maduración) y ácido abscísico (cierre de estomas)."],
          [("¿De dónde procede el oxígeno que liberan las plantas?", ["En la fase luminosa se rompe una molécula.", "Es la fotólisis del agua."], "Del agua.")],
          [("El oxígeno de la fotosíntesis procede del CO₂.", "Procede de la ruptura del agua."), ("Las plantas solo transpiran de noche.", "Transpiran sobre todo de día, con los estomas abiertos.")],
          [("¿Por qué una manzana madura hace madurar a otras?", "Libera etileno, una hormona gaseosa."), ("¿Qué es el fotoperiodo?", "La duración del día, que controla la floración de muchas plantas.")],
          [("Tejidos", [("meristemo", "células que se dividen y permiten crecer"), ("parénquima clorofílico", "tejido que hace la fotosíntesis"), ("colénquima", "sostén flexible en tallos jóvenes"),
                        ("esclerénquima", "sostén rígido con paredes lignificadas"), ("xilema", "conduce la savia bruta"), ("floema", "conduce la savia elaborada"), ("epidermis", "recubre y protege la planta"),
                        ("súber", "corcho que protege tallos leñosos")],
            "¿Qué función tiene: {k}?", D),
           ("Fitohormonas", [("auxinas", "crecimiento por alargamiento y tropismos"), ("giberelinas", "germinación y alargamiento del tallo"), ("citoquininas", "división celular y retraso del envejecimiento"),
                             ("etileno", "maduración de los frutos"), ("ácido abscísico", "cierre de estomas y latencia de semillas")],
            "¿Qué efecto tienen: {k}?", "¿Qué fitohormona controla: {v}?", ["fotosíntesis nocturna"]),
           ("Fotosíntesis", {"los procesos de la fase luminosa": ["captación de luz por la clorofila", "fotólisis del agua", "liberación de oxígeno", "síntesis de ATP", "formación de NADPH"],
                             "los procesos del ciclo de Calvin": ["fijación del CO₂", "acción de la enzima rubisco", "síntesis de glucosa", "consumo de ATP y NADPH", "ocurre en el estroma"]})],
          ["El xilema transporta savia bruta.", "El oxígeno de la fotosíntesis procede del agua.", "El etileno madura los frutos.", "El ciclo de Calvin fija CO₂.", "Los meristemos permiten crecer.", "El ácido abscísico cierra los estomas.",
           "La fase luminosa ocurre en los tilacoides."],
          [("El oxígeno procede del CO₂.", "Procede del agua."), ("El floema transporta savia bruta.", "Transporta elaborada."), ("El etileno cierra los estomas.", "Lo hace el ácido abscísico."),
           ("El ciclo de Calvin libera oxígeno.", "Fija CO₂."), ("Las auxinas maduran los frutos.", "Regulan el crecimiento.")],
          "la fisiología vegetal", "living-things-and-ecosystems"),

        H("BG", "los-microorganismos-y-formas-acelulares", "Los microorganismos y las formas acelulares", "Microorganismos",
          "Los alumnos describen bacterias, arqueas, protistas y hongos microscópicos, los virus, viroides y priones, su papel en los ciclos, la salud y la industria, y las técnicas de cultivo y esterilización.",
          "bacterias, arqueas, protozoos, algas microscópicas, levaduras, mohos, virus, cápsida, ciclo lítico y lisogénico, viroides, priones, fermentación, biorremediación, esterilización",
          "Los virus no son células: necesitan una célula huésped", "Los microorganismos reciclan materia, producen alimentos y causan enfermedades.",
          ["Las bacterias y las arqueas son procariotas. Los protozoos, algas microscópicas y hongos como las levaduras son eucariotas.",
           "Los virus tienen material genético (ADN o ARN) dentro de una cápsida de proteínas y solo se multiplican dentro de células. Los viroides son ARN sin cápsida; los priones, proteínas mal plegadas.",
           "Los microorganismos se usan para fermentar (pan, yogur, vino), producir antibióticos y limpiar contaminantes (biorremediación)."],
          [("¿Por qué los antibióticos no curan una infección vírica?", ["Los antibióticos atacan estructuras bacterianas.", "Los virus no tienen pared ni ribosomas propios."], "Porque los virus no son bacterias.")],
          [("Los virus son las bacterias más pequeñas.", "No son células ni tienen metabolismo propio."), ("Las arqueas son bacterias raras.", "Son un dominio distinto, aunque también procariotas.")],
          [("¿Qué es un bacteriófago?", "Un virus que infecta bacterias."), ("¿Cómo se esteriliza material de laboratorio?", "Con autoclave: vapor a 121 °C y alta presión.")],
          [("Grupos", [("Escherichia coli", "bacteria"), ("Lactobacillus", "bacteria"), ("Streptococcus", "bacteria"), ("arquea metanógena", "arquea"), ("arquea halófila de las salinas", "arquea"),
                       ("Plasmodium", "protozoo"), ("paramecio", "protozoo"), ("Saccharomyces cerevisiae", "hongo levadura"), ("Penicillium", "hongo moho"), ("virus del sarampión", "virus"), ("prion de las vacas locas", "prion")],
            "¿A qué grupo pertenece: {k}?", None),
           ("Usos", [("Saccharomyces cerevisiae", "fermentación del pan, el vino y la cerveza"), ("Lactobacillus", "elaboración del yogur"), ("Penicillium chrysogenum", "producción de penicilina"),
                     ("bacterias que degradan petróleo", "biorremediación de vertidos"), ("Escherichia coli modificada", "producción de insulina"), ("Rhizobium", "fijación de nitrógeno en leguminosas"),
                     ("bacterias metanógenas", "producción de biogás")],
            "¿Para qué se usa o qué hace: {k}?", D),
           ("Ciclos víricos", [("adsorción", "el virus se une a la célula"), ("penetración", "el material genético entra en la célula"), ("replicación", "se copian los ácidos nucleicos víricos"),
                               ("ensamblaje", "se forman nuevos virus"), ("liberación", "los virus salen y suelen romper la célula"), ("ciclo lisogénico", "el ADN vírico se integra en el de la célula y queda latente")],
            "¿Qué ocurre en: {k}?", D)],
          ["Los virus no son células.", "Las arqueas son procariotas.", "Las levaduras son hongos.", "Los priones son proteínas.", "Penicillium produce penicilina.", "El autoclave esteriliza con vapor a presión.",
           "Los bacteriófagos infectan bacterias."],
          [("Los virus son bacterias pequeñas.", "No son células."), ("Las levaduras son bacterias.", "Son hongos."), ("Los antibióticos curan los virus.", "No actúan sobre virus."), ("Los priones tienen ADN.", "Son solo proteínas."),
           ("Las arqueas son eucariotas.", "Son procariotas.")],
          "los microorganismos", "living-things-and-ecosystems"),

        H("FQ", "estructura-atomica-y-enlace-quimico", "Estructura atómica, tabla periódica y enlace químico", "Átomo y enlace",
          "Los alumnos describen el modelo cuántico del átomo, escriben configuraciones electrónicas, explican las propiedades periódicas y los tipos de enlace y relacionan la estructura con las propiedades de las sustancias.",
          "modelo de Bohr, números cuánticos, orbitales, configuración electrónica, regla de Aufbau, propiedades periódicas, radio atómico, energía de ionización, electronegatividad, enlace iónico, covalente, metálico, fuerzas intermoleculares",
          "La configuración electrónica explica la tabla periódica", "La electronegatividad aumenta hacia arriba y hacia la derecha.",
          ["Los electrones ocupan orbitales s, p, d y f en orden de energía creciente (1s 2s 2p 3s 3p 4s 3d…). Los del mismo grupo tienen la misma configuración externa.",
           "El radio atómico aumenta hacia abajo y hacia la izquierda; la energía de ionización y la electronegatividad, hacia arriba y a la derecha.",
           "Enlace iónico: transferencia de electrones; covalente: compartición; metálico: nube electrónica. Entre moléculas actúan fuerzas de Van der Waals y puentes de hidrógeno."],
          [("Escribe la configuración del sodio (Z = 11).", ["Se llenan 1s, 2s, 2p y luego 3s.", "1s² 2s² 2p⁶ 3s¹."], "1s² 2s² 2p⁶ 3s¹.")],
          [("El orbital 4s se llena después del 3d.", "El 4s tiene menos energía y se llena antes."), ("Los puentes de hidrógeno son enlaces dentro de la molécula.", "Son fuerzas entre moléculas.")],
          [("¿Por qué el agua tiene un punto de ebullición tan alto?", "Por los puentes de hidrógeno entre sus moléculas."), ("¿Qué es la electronegatividad?", "La tendencia de un átomo a atraer los electrones de un enlace.")],
          [("Configuraciones", [("H (Z = 1)", "1s¹"), ("He (Z = 2)", "1s²"), ("C (Z = 6)", "1s² 2s² 2p²"), ("N (Z = 7)", "1s² 2s² 2p³"), ("O (Z = 8)", "1s² 2s² 2p⁴"), ("Ne (Z = 10)", "1s² 2s² 2p⁶"),
                                ("Na (Z = 11)", "1s² 2s² 2p⁶ 3s¹"), ("Mg (Z = 12)", "1s² 2s² 2p⁶ 3s²"), ("Cl (Z = 17)", "1s² 2s² 2p⁶ 3s² 3p⁵"), ("K (Z = 19)", "1s² 2s² 2p⁶ 3s² 3p⁶ 4s¹")],
            "¿Cuál es la configuración electrónica de {k}?", "¿Qué elemento tiene la configuración {v}?"),
           ("Propiedades periódicas", [("radio atómico", "aumenta hacia abajo y hacia la izquierda"), ("energía de ionización", "aumenta hacia arriba y hacia la derecha"), ("electronegatividad", "máxima en el flúor"),
                                       ("carácter metálico", "aumenta hacia abajo y hacia la izquierda"), ("afinidad electrónica", "energía al captar un electrón"), ("electrones de valencia", "iguales en todo un grupo")],
            "¿Qué ocurre con: {k}?", D),
           ("Fuerzas y enlaces", [("NaCl sólido", "enlace iónico"), ("diamante", "enlace covalente en red"), ("cobre", "enlace metálico"), ("agua líquida", "puentes de hidrógeno entre moléculas"),
                                  ("metano", "fuerzas de dispersión entre moléculas"), ("HCl", "fuerzas dipolo-dipolo entre moléculas"), ("cuarzo", "enlace covalente en red")],
            "¿Qué mantiene unidas las partículas en: {k}?", None)],
          ["El 4s se llena antes que el 3d.", "El flúor es el elemento más electronegativo.", "El radio atómico aumenta al bajar en un grupo.", "El agua forma puentes de hidrógeno.", "El NaCl tiene enlace iónico.",
           "Los elementos de un grupo tienen los mismos electrones de valencia.", "El diamante es una red covalente."],
          [("El 3d se llena antes que el 4s.", "El 4s va primero."), ("El cesio es el más electronegativo.", "Lo es el flúor."), ("El radio disminuye al bajar en un grupo.", "Aumenta."),
           ("Los puentes de hidrógeno son enlaces intramoleculares.", "Son intermoleculares."), ("El cobre tiene enlace iónico.", "Es metálico.")],
          "la estructura atómica y el enlace", "matter"),

        H("FQ", "gases-y-disoluciones", "Leyes de los gases y disoluciones", "Gases y disoluciones",
          "Los alumnos aplican las leyes de Boyle, Charles y Gay-Lussac, la ecuación de los gases ideales y la ley de Dalton, y expresan la concentración de disoluciones (molaridad, % en masa, fracción molar) y sus propiedades coligativas.",
          "ley de Boyle-Mariotte, ley de Charles, ley de Gay-Lussac, ecuación de los gases ideales, R = 0,082 atm·L/(mol·K), presión parcial, molaridad, porcentaje en masa, fracción molar, dilución, propiedades coligativas",
          "p · V = n · R · T", "La temperatura de los gases siempre en kelvin.",
          ["Boyle: a T constante, p · V es constante. Charles: a p constante, V : T es constante. Gay-Lussac: a V constante, p : T es constante.",
           "La ecuación de los gases ideales es p · V = n · R · T, con R = 0,082 atm·L/(mol·K) y T en kelvin.",
           "La molaridad es n(soluto) : V(disolución en L). Al diluir se conserva el número de moles: c₁ · V₁ = c₂ · V₂."],
          [("¿Qué volumen ocupan 2 mol de gas a 300 K y 1 atm?", ["V = n · R · T : p.", "2 · 0,082 · 300 : 1 = 49,2."], "49,2 L.")],
          [("La temperatura de la ecuación puede ir en °C.", "Siempre en kelvin."), ("Al diluir cambian los moles de soluto.", "Los moles se conservan; cambia el volumen.")],
          [("¿Por qué el agua con sal hierve a más temperatura?", "Es una propiedad coligativa: el soluto eleva el punto de ebullición."), ("¿Qué dice la ley de Dalton?", "La presión total de una mezcla es la suma de las presiones parciales.")],
          [("Leyes", [("ley de Boyle-Mariotte", "a T constante, p · V = constante"), ("ley de Charles", "a p constante, V : T = constante"), ("ley de Gay-Lussac", "a V constante, p : T = constante"),
                      ("ecuación de los gases ideales", "p · V = n · R · T"), ("ley de Dalton", "p total = suma de presiones parciales"), ("hipótesis de Avogadro", "volúmenes iguales de gases en las mismas condiciones tienen igual número de moléculas")],
            "¿Qué establece: {k}?", "¿Qué ley expresa: {v}?"),
           ("Unidades de concentración", [("molaridad", "mol de soluto por litro de disolución"), ("molalidad", "mol de soluto por kilogramo de disolvente"), ("porcentaje en masa", "gramos de soluto por 100 g de disolución"),
                                          ("fracción molar", "moles de un componente entre moles totales"), ("concentración en g/L", "gramos de soluto por litro de disolución"), ("partes por millón", "miligramos de soluto por kilogramo de disolución")],
            "¿Qué es: {k}?", "¿Qué forma de expresar la concentración es: {v}?"),
           ("Propiedades coligativas", {"las propiedades coligativas": ["descenso de la presión de vapor", "aumento del punto de ebullición", "descenso del punto de congelación", "presión osmótica"],
                                        "las aplicaciones de las propiedades coligativas": ["echar sal en carreteras heladas", "anticongelante en el radiador", "suero fisiológico isotónico", "conservar alimentos en salmuera"],
                                        "las leyes de los gases": ["Boyle-Mariotte", "Charles", "Gay-Lussac", "Dalton"]})],
          ["p · V = n · R · T.", "La temperatura va en kelvin en las leyes de los gases.", "Al diluir se conservan los moles.", "La sal eleva el punto de ebullición del agua.", "R vale 0,082 atm·L/(mol·K).",
           "La molaridad son moles por litro de disolución.", "A T constante p · V es constante."],
          [("La temperatura va en °C.", "Va en kelvin."), ("Al diluir aumentan los moles.", "Se conservan."), ("La sal baja el punto de ebullición.", "Lo eleva."), ("La molaridad son gramos por litro.", "Son moles por litro."),
           ("A T constante V : T es constante.", "Es p · V.")],
          "los gases y las disoluciones", "matter", calc=lambda R: (f_gases if R.random() < 0.6 else f_disol)(R)),

        H("FQ", "estequiometria-y-termoquimica", "Reacciones químicas: estequiometría y termoquímica", "Estequiometría y energía",
          "Los alumnos realizan cálculos estequiométricos con reactivo limitante, pureza y rendimiento, describen tipos de reacciones y calculan la energía de reacción con entalpías, valorando la química industrial.",
          "estequiometría, reactivo limitante, reactivo en exceso, pureza, rendimiento, entalpía, reacción exotérmica y endotérmica, diagrama energético, combustión, industria química, química verde",
          "El reactivo limitante determina la cantidad de producto", "Si ΔH es negativo, la reacción desprende calor.",
          ["Para calcular con una ecuación ajustada: gramos → moles → proporción estequiométrica → moles → gramos.",
           "El reactivo limitante se acaba primero y fija la cantidad de producto. El rendimiento real casi siempre es menor del 100 %.",
           "La entalpía de reacción ΔH es el calor a presión constante: ΔH < 0 exotérmica, ΔH > 0 endotérmica."],
          [("Reaccionan 2 mol de H₂ con 2 mol de O₂ (2 H₂ + O₂ → 2 H₂O). ¿Cuál es el limitante?", ["2 mol de H₂ necesitan 1 mol de O₂.", "Sobra 1 mol de O₂."], "El H₂.")],
          [("El reactivo limitante es el que tiene menos masa.", "Es el que da menos producto según la proporción en moles."), ("Las reacciones exotérmicas no necesitan energía para empezar.", "Muchas necesitan una energía de activación.")],
          [("¿Qué es la química verde?", "Diseñar procesos que reducen residuos y sustancias peligrosas."), ("¿Para qué sirve el proceso Haber?", "Para obtener amoniaco con el que se fabrican fertilizantes.")],
          [("Conceptos", [("reactivo limitante", "el que se consume por completo primero"), ("reactivo en exceso", "el que sobra al final"), ("rendimiento", "producto real entre producto teórico"),
                          ("pureza", "porcentaje de sustancia útil en una muestra"), ("entalpía de reacción", "calor intercambiado a presión constante"), ("energía de activación", "energía mínima para que empiece la reacción"),
                          ("catalizador", "sustancia que reduce la energía de activación")],
            "¿Qué es: {k}?", D),
           ("Procesos industriales", [("proceso Haber-Bosch", "obtención de amoniaco"), ("método de contacto", "obtención de ácido sulfúrico"), ("alto horno", "obtención de hierro"), ("electrólisis de la bauxita", "obtención de aluminio"),
                                      ("craqueo del petróleo", "obtención de gasolinas y alquenos"), ("proceso Ostwald", "obtención de ácido nítrico")],
            "¿Para qué sirve: {k}?", "¿Qué proceso permite la {v}?"),
           ("Signo de ΔH", {"las reacciones exotérmicas": ["combustión del metano", "respiración celular", "neutralización", "oxidación del hierro", "síntesis del amoniaco"],
                            "las reacciones endotérmicas": ["fotosíntesis", "descomposición del carbonato de calcio", "electrólisis del agua", "fusión del hielo", "disolución del nitrato de amonio"]})],
          ["El reactivo limitante se consume primero.", "Si ΔH es negativo la reacción es exotérmica.", "El rendimiento suele ser menor del 100 %.", "El proceso Haber obtiene amoniaco.", "La fotosíntesis es endotérmica.",
           "Un catalizador reduce la energía de activación.", "La combustión desprende calor."],
          [("El limitante es el de menor masa.", "Es el que da menos producto."), ("ΔH positivo es exotérmico.", "Es endotérmico."), ("El rendimiento siempre es del 100 %.", "Suele ser menor."),
           ("El catalizador aumenta la energía de activación.", "La reduce."), ("La fotosíntesis es exotérmica.", "Es endotérmica.")],
          "las reacciones químicas", "matter", calc=f_termo),

        H("FQ", "quimica-organica", "Química orgánica: formulación y reacciones", "Química orgánica",
          "Los alumnos formulan y nombran hidrocarburos y compuestos con grupos funcionales según la IUPAC, reconocen isómeros y describen reacciones orgánicas y la importancia de los compuestos del carbono.",
          "hidrocarburos, alcanos, alquenos, alquinos, aromáticos, grupos funcionales, alcoholes, aldehídos, cetonas, ácidos carboxílicos, ésteres, aminas, isomería, combustión, polímeros",
          "El grupo funcional determina las propiedades", "Los isómeros tienen la misma fórmula molecular y distinta estructura.",
          ["Los alcanos (CₙH₂ₙ₊₂) tienen enlaces simples; los alquenos, dobles; los alquinos, triples. El benceno es el aromático más sencillo.",
           "Grupos funcionales: -OH (alcohol, -ol), -CHO (aldehído, -al), -CO- (cetona, -ona), -COOH (ácido, -oico), -COO- (éster, -oato de -ilo), -NH₂ (amina).",
           "Los isómeros tienen la misma fórmula molecular pero distinta estructura, como el butano y el metilpropano."],
          [("¿Qué grupo funcional tiene la propanona?", ["Termina en -ona.", "Es la acetona."], "Cetona (C=O en un carbono intermedio).")],
          [("La acetona es un alcohol.", "Es una cetona."), ("Todos los compuestos orgánicos son naturales.", "Muchos se sintetizan en la industria.")],
          [("¿Qué son los ésteres?", "Compuestos de olor afrutado formados por un ácido y un alcohol."), ("¿Qué es un polímero de adición?", "Una cadena larga que se forma uniendo alquenos, como el polietileno.")],
          [("Grupos funcionales", [("etanol", "alcohol"), ("propan-2-ol", "alcohol"), ("metanal", "aldehído"), ("etanal", "aldehído"), ("propanona", "cetona"), ("butanona", "cetona"), ("ácido etanoico", "ácido carboxílico"),
                                   ("etanoato de etilo", "éster"), ("metilamina", "amina"), ("benceno", "hidrocarburo aromático"), ("eteno", "alqueno")],
            "¿Qué tipo de compuesto es: {k}?", None),
           ("Fórmulas", [("CH₃–CH₂OH", "etanol"), ("CH₃–CHO", "etanal"), ("CH₃–CO–CH₃", "propanona"), ("CH₃–COOH", "ácido etanoico"), ("CH₃–COO–CH₃", "etanoato de metilo"), ("CH₃–NH₂", "metilamina"),
                         ("CH₂=CH₂", "eteno"), ("CH≡CH", "etino"), ("CH₃–CH₂–CH₃", "propano")],
            "¿Cómo se nombra {k}?", "¿Cuál es la fórmula semidesarrollada de: {v}?"),
           ("Reacciones", [("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "combustión"), ("CH₂=CH₂ + H₂ → CH₃–CH₃", "adición"), ("CH₂=CH₂ + H₂O → CH₃–CH₂OH", "adición"), ("CH₃–COOH + CH₃OH → CH₃–COO–CH₃ + H₂O", "esterificación"),
                           ("CH₃–CH₂OH → CH₂=CH₂ + H₂O", "eliminación"), ("CH₄ + Cl₂ → CH₃Cl + HCl", "sustitución"), ("n CH₂=CH₂ → (–CH₂–CH₂–)ₙ", "polimerización")],
            "¿Qué tipo de reacción orgánica es {k}?", None)],
          ["La propanona es una cetona.", "Los alcanos solo tienen enlaces simples.", "Los ésteres se forman con un ácido y un alcohol.", "Los isómeros tienen la misma fórmula molecular.", "El polietileno se forma por polimerización.",
           "El grupo -OH es de los alcoholes.", "El benceno es aromático."],
          [("La acetona es un alcohol.", "Es una cetona."), ("Los alquinos tienen enlaces dobles.", "Tienen triples."), ("Los isómeros tienen distinta fórmula molecular.", "Tienen la misma."), ("El grupo -COOH es de las aminas.", "Es de los ácidos."),
           ("Todos los compuestos orgánicos son naturales.", "Muchos son sintéticos.")],
          "la química orgánica", "matter"),

        H("FQ", "cinematica-del-punto-material", "Cinemática: movimientos en el plano", "Cinemática",
          "Los alumnos usan vectores de posición, velocidad y aceleración, estudian la composición de movimientos, el tiro horizontal y el parabólico, y el movimiento circular con sus magnitudes angulares.",
          "vector de posición, desplazamiento, velocidad media e instantánea, aceleración tangencial y normal, composición de movimientos, tiro horizontal, tiro parabólico, alcance, altura máxima, MCU, MCUA, velocidad angular",
          "Un tiro parabólico es MRU en x más MRUA en y", "El alcance máximo en terreno llano se logra a 45°.",
          ["El tiro parabólico combina un MRU horizontal (vₓ = v₀ · cos α) y un MRUA vertical con aceleración −g.",
           "El alcance en terreno llano es x = v₀² · sen(2α) : g; es máximo a 45°. La altura máxima es (v₀ · sen α)² : (2g).",
           "En el movimiento circular, v = ω · r. La aceleración normal o centrípeta vale aₙ = v² : r."],
          [("Un balón sale a 20 m/s con 45°. ¿Alcance?", ["x = v₀² · sen 90° : g.", "400 : 9,8 ≈ 40,8 m."], "Unos 40,8 m.")],
          [("En el punto más alto la velocidad es cero.", "Solo se anula la componente vertical; la horizontal sigue."), ("Un MCU no tiene aceleración.", "Tiene aceleración normal porque cambia la dirección.")],
          [("¿Por qué 30° y 60° dan el mismo alcance?", "Porque sen 60° = sen 120°: los ángulos complementarios dan igual alcance."), ("¿Qué es un radián?", "El ángulo cuyo arco mide lo mismo que el radio.")],
          [("Magnitudes", [("velocidad angular", "ángulo girado por unidad de tiempo"), ("aceleración normal", "cambio de dirección de la velocidad"), ("aceleración tangencial", "cambio del módulo de la velocidad"),
                           ("periodo", "tiempo de una vuelta"), ("frecuencia", "vueltas por segundo"), ("alcance", "distancia horizontal recorrida en un tiro"), ("altura máxima", "punto donde la velocidad vertical es cero")],
            "¿Qué es: {k}?", D),
           ("Ecuaciones del tiro", [("velocidad horizontal", "vₓ = v₀ · cos α"), ("velocidad vertical inicial", "v₀ᵧ = v₀ · sen α"), ("alcance en terreno llano", "x = v₀² · sen(2α) : g"),
                                    ("altura máxima", "h = (v₀ · sen α)² : (2g)"), ("tiempo de vuelo", "t = 2 · v₀ · sen α : g"), ("velocidad lineal en MCU", "v = ω · r"), ("aceleración centrípeta", "aₙ = v² : r")],
            "¿Qué expresión da: {k}?", "¿Qué magnitud se calcula con {v}?"),
           ("Composición", {"los movimientos con MRU en un eje y MRUA en otro": ["tiro horizontal", "tiro parabólico", "lanzar un balón a canasta", "un paquete soltado desde un avión", "un chorro de agua de una manguera"],
                            "los movimientos circulares": ["noria", "Luna alrededor de la Tierra", "rueda de bicicleta", "satélite geoestacionario", "centrifugadora"]})],
          ["El alcance máximo se logra a 45°.", "En el tiro parabólico la velocidad horizontal es constante.", "En el MCU hay aceleración normal.", "v = ω · r.", "En el punto más alto se anula la velocidad vertical.",
           "30° y 60° dan el mismo alcance.", "La aceleración vertical en un tiro es g hacia abajo."],
          [("En el punto más alto la velocidad es cero.", "Solo la vertical."), ("El alcance máximo se logra a 90°.", "A 45°."), ("En el MCU no hay aceleración.", "Hay aceleración normal."),
           ("La velocidad horizontal cambia en el tiro.", "Es constante."), ("La aceleración tangencial cambia la dirección.", "Cambia el módulo.")],
          "la cinemática", "forces-and-motion", calc=f_cine),

        H("FQ", "dinamica", "Dinámica: fuerzas y movimiento", "Dinámica",
          "Los alumnos aplican las leyes de Newton con diagramas de fuerzas a planos inclinados, poleas, ascensores y curvas, y usan el momento lineal, el impulso y la ley de Hooke.",
          "diagrama de fuerzas, fuerza neta, peso, normal, tensión, rozamiento estático y dinámico, plano inclinado, poleas, fuerza centrípeta, momento lineal, impulso, conservación del momento",
          "Σ F = m · a en cada eje", "En un sistema aislado el momento lineal total se conserva.",
          ["Se dibujan todas las fuerzas sobre el cuerpo y se aplica Σ F = m · a en cada eje.",
           "En un plano inclinado sin rozamiento, a = g · sen α. Con rozamiento dinámico, Fr = μ · N.",
           "El momento lineal es p = m · v. El impulso F · Δt cambia el momento. En choques y explosiones, si no hay fuerzas externas, el momento total se conserva."],
          [("Un patinador de 60 kg empuja a otro de 40 kg y este sale a 3 m/s. ¿Y el primero?", ["El momento inicial es 0.", "60 · v = 40 · 3 → v = 2 m/s en sentido contrario."], "2 m/s hacia atrás.")],
          [("La normal siempre es igual al peso.", "En un plano inclinado o un ascensor acelerado es distinta."), ("Un cuerpo en reposo no tiene fuerzas.", "Tiene fuerzas que se anulan.")],
          [("¿Por qué los airbags reducen las lesiones?", "Alargan el tiempo del choque y reducen la fuerza para el mismo impulso."), ("¿Por qué retrocede un fusil al disparar?", "Por la conservación del momento lineal.")],
          [("Fuerzas", [("peso", "atracción de la Tierra, vertical hacia abajo"), ("normal", "reacción de la superficie, perpendicular a ella"), ("tensión", "fuerza a lo largo de una cuerda"),
                        ("rozamiento dinámico", "se opone al deslizamiento y vale μ · N"), ("rozamiento estático", "impide que empiece el movimiento"), ("fuerza centrípeta", "resultante dirigida al centro de la curva"),
                        ("fuerza elástica", "fuerza de un muelle, F = −k · x")],
            "¿Qué es o cómo es: {k}?", D),
           ("Situaciones", [("ascensor que sube acelerando", "la báscula marca más que el peso"), ("ascensor que baja acelerando", "la báscula marca menos que el peso"), ("ascensor a velocidad constante", "la báscula marca el peso"),
                            ("caída libre dentro del ascensor", "la báscula marca cero"), ("cuerpo en reposo en un plano inclinado", "el rozamiento estático equilibra la componente del peso")],
            "¿Qué ocurre en esta situación: {k}?", None, ["la masa cambia"]),
           ("Momento e impulso", [("momento lineal", "producto de la masa por la velocidad"), ("impulso", "producto de la fuerza por el tiempo que actúa"), ("teorema del impulso", "el impulso es igual a la variación del momento"),
                                  ("conservación del momento", "en un sistema aislado el momento total no cambia"), ("choque inelástico", "los cuerpos quedan unidos tras chocar"), ("choque elástico", "se conserva también la energía cinética")],
            "¿Qué es: {k}?", D)],
          ["Σ F = m · a.", "En un plano sin rozamiento a = g · sen α.", "El momento lineal se conserva en un sistema aislado.", "El airbag alarga el tiempo del choque.", "En caída libre la báscula marca cero.",
           "En un ascensor que sube acelerando pesamos aparentemente más.", "Un cuerpo en reposo tiene fuerzas que se anulan."],
          [("La normal siempre es igual al peso.", "No siempre."), ("Un cuerpo en reposo no tiene fuerzas.", "Tiene fuerzas que se anulan."), ("En un choque inelástico se conserva la energía cinética.", "Se conserva el momento, no la Ec."),
           ("El airbag aumenta la fuerza del choque.", "La reduce."), ("En el ascensor que baja acelerando la báscula marca más.", "Marca menos.")],
          "la dinámica", "forces-and-motion", calc=f_dina),

        H("FQ", "energia-mecanica-y-trabajo", "Energía: trabajo, conservación y potencia", "Trabajo y energía",
          "Los alumnos relacionan trabajo y energía, aplican el teorema de las fuerzas vivas, la conservación de la energía mecánica con y sin rozamiento, la energía potencial elástica, la potencia y el rendimiento.",
          "trabajo, fuerzas conservativas y no conservativas, teorema de las fuerzas vivas, energía cinética, potencial gravitatoria y elástica, conservación de la energía mecánica, potencia, rendimiento, primer principio",
          "W total = Δ Ec", "Si solo actúan fuerzas conservativas, la energía mecánica se conserva.",
          ["El trabajo es W = F · d · cos α. El teorema de las fuerzas vivas dice que el trabajo total es igual a la variación de energía cinética.",
           "El peso y la fuerza elástica son conservativos: si solo actúan ellos, Ec + Ep es constante. El rozamiento transforma energía mecánica en térmica.",
           "La energía potencial elástica de un muelle es ½ · k · x². La potencia es P = W : t y el rendimiento, útil entre total."],
          [("Un bloque cae 5 m sin rozamiento. ¿Velocidad final?", ["m · g · h = ½ · m · v².", "v = √(2 · 9,8 · 5) ≈ 9,9 m/s."], "Unos 9,9 m/s.")],
          [("La energía mecánica siempre se conserva.", "Solo sin fuerzas no conservativas como el rozamiento."), ("El trabajo del peso depende del camino.", "Solo depende de la diferencia de alturas.")],
          [("¿Qué es una fuerza conservativa?", "Una cuyo trabajo no depende del camino seguido."), ("¿Qué dice el primer principio de la termodinámica?", "La variación de energía interna es el calor más el trabajo intercambiados.")],
          [("Conceptos", [("fuerza conservativa", "fuerza cuyo trabajo no depende del camino"), ("teorema de las fuerzas vivas", "el trabajo total iguala la variación de energía cinética"),
                          ("energía potencial elástica", "energía almacenada en un muelle deformado"), ("energía mecánica", "suma de cinética y potencial"), ("potencia", "rapidez con que se realiza trabajo"),
                          ("rendimiento", "cociente entre la energía útil y la consumida"), ("energía interna", "suma de las energías de las partículas de un sistema")],
            "¿Qué es: {k}?", D),
           ("¿Conservativa o no?", [("peso", "conservativa"), ("fuerza elástica de un muelle", "conservativa"), ("fuerza eléctrica", "conservativa"), ("fuerza gravitatoria del Sol", "conservativa"),
                                    ("rozamiento", "no conservativa"), ("resistencia del aire", "no conservativa"), ("fuerza de un motor", "no conservativa"), ("empuje de una persona", "no conservativa")],
            "¿Qué tipo de fuerza es: {k}?", None, ["nuclear débil", "ficticia"]),
           ("Transformaciones", [("péndulo que baja", "potencial gravitatoria en cinética"), ("pértiga que se dobla", "cinética en potencial elástica"), ("frenada de un coche", "cinética en térmica"),
                                 ("muelle de un juguete que salta", "potencial elástica en cinética"), ("embalse que mueve una turbina", "potencial gravitatoria en eléctrica"), ("ciclista que sube un puerto", "química en potencial gravitatoria")],
            "¿Qué transformación ocurre en: {k}?", None)],
          ["El trabajo total es igual a la variación de Ec.", "El peso es una fuerza conservativa.", "El rozamiento no es conservativo.", "La Ep elástica vale ½ · k · x².", "Sin rozamiento la energía mecánica se conserva.",
           "El trabajo del peso solo depende de la diferencia de alturas.", "El rendimiento es siempre menor del 100 %."],
          [("La energía mecánica siempre se conserva.", "No con rozamiento."), ("El rozamiento es conservativo.", "No lo es."), ("La Ep elástica vale k · x.", "Vale ½ · k · x²."), ("El trabajo del peso depende del camino.", "No depende."),
           ("El rendimiento puede ser del 120 %.", "Siempre es menor del 100 %.")],
          "la energía", "energy", calc=f_ener),
    ]
