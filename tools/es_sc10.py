# -*- coding: utf-8 -*-
"""España / Biología y Geología y Física y Química: 4.º de ESO"""
from es_sci import H, nq, num, it

D = "¿Qué corresponde a esta descripción: {v}?"
G = 9.8


def f_gen(R):
    k = R.choice(["cruce", "cruce", "fen", "sangre", "sexo"])
    if k == "cruce":
        p1, p2, rasgo, dom, rec = R.choice([("Aa", "Aa", "semillas", "amarillas", "verdes"), ("Aa", "aa", "semillas", "lisas", "rugosas"), ("Aa", "Aa", "flores", "moradas", "blancas"),
                                            ("Aa", "aa", "ojos", "oscuros", "claros"), ("Aa", "Aa", "pelo de cobaya", "negro", "blanco")])
        pr = (0.25 if p2 == "Aa" else 0.5) * 100
        return nq("Se cruzan %s × %s para el color de %s (%s domina sobre %s). ¿Qué porcentaje de la descendencia tendrá %s %s?" % (p1, p2, rasgo, dom, rec, rasgo, rec), pr,
                  [100 - pr, pr / 2, 100 if pr == 50 else 50, 75 if pr == 50 else 100], "%", "Solo los aa muestran el carácter recesivo: %s %% de la descendencia." % num(pr))
    if k == "fen":
        p1, p2 = R.choice([("AA", "aa"), ("Aa", "Aa"), ("Aa", "aa"), ("AA", "Aa")])
        dom = {("AA", "aa"): 100, ("Aa", "Aa"): 75, ("Aa", "aa"): 50, ("AA", "Aa"): 100}[(p1, p2)]
        het = {("AA", "aa"): 100, ("Aa", "Aa"): 50, ("Aa", "aa"): 50, ("AA", "Aa"): 50}[(p1, p2)]
        if R.random() < 0.5:
            return nq("En el cruce %s × %s, ¿qué porcentaje de hijos será heterocigoto (Aa)?" % (p1, p2), het, [25, 75, 100 if het != 100 else 50], "%",
                      "Con un cuadro de Punnett se ve que el %s %% es Aa." % num(het))
        return nq("En el cruce %s × %s (A dominante), ¿qué porcentaje mostrará el carácter dominante?" % (p1, p2), dom, [25, 50 if dom != 50 else 75, 100 if dom != 100 else 75], "%",
                  "Muestran el carácter dominante los AA y los Aa: %s %%." % num(dom))
    if k == "sangre":
        a, b, ans, w = R.choice([("IᴬIᴬ", "ii", "A", ["0", "AB", "B"]), ("IᴬIᴮ", "ii", "A y B", ["AB y 0", "solo AB", "A, B, AB y 0"]),
                                 ("IᴬIᴬ", "IᴮIᴮ", "AB", ["A y B", "0", "solo A"]), ("ii", "ii", "0", ["A", "AB", "A y 0"]),
                                 ("Iᴬi", "Iᴮi", "A, B, AB y 0", ["solo AB", "A y B", "AB y 0"])])
        return it("Un padre %s y una madre %s. ¿Qué grupos sanguíneos pueden tener sus hijos?" % (a, b), ans, w,
                  "Los alelos Iᴬ e Iᴮ son codominantes y dominan sobre i: los hijos pueden ser %s." % ans)
    return it("Un hombre (XY) y una mujer (XX) esperan un bebé. ¿Qué probabilidad hay de que sea niña?", "50 %", ["25 %", "75 %", "100 %"],
              "La madre siempre da X; el padre da X o Y con la misma probabilidad: 50 %.")


def f_cine(R):
    k = R.choice(["caida_v", "caida_t", "frenado", "mrua_d", "encuentro", "vmedia"])
    if k == "caida_v":
        t = R.choice([1, 2, 3, 1.5, 2.5, 4])
        return nq("Se deja caer una piedra. ¿Qué velocidad tiene a los %s s? (g = 9,8 m/s², sin rozamiento)" % num(t), G * t, [G * t * t, G / t, 0.5 * G * t * t], "m/s",
                  "v = g · t = 9,8 · %s = %s m/s." % (num(t), num(G * t)))
    if k == "caida_t":
        t = R.choice([1, 2, 3, 1.5, 2.5])
        h = 0.5 * G * t * t
        return nq("Se deja caer un objeto desde %s m. ¿Cuánto tarda en llegar al suelo? (g = 9,8 m/s²)" % num(h), t, [h / G, 2 * h / G, h / G / 2], "s",
                  "h = ½ · g · t²; t = √(2h : g) = √(2 · %s : 9,8) = %s s." % (num(h), num(t)))
    if k == "frenado":
        v0, a = R.choice([(20, 5), (30, 6), (15, 3), (25, 5), (10, 2), (40, 8)])
        d = v0 * v0 / (2 * a)
        return nq("Un coche a %s m/s frena con una aceleración de −%s m/s². ¿Qué distancia recorre hasta parar?" % (v0, a), d, [v0 * v0 / a, v0 / a, v0 * a], "m",
                  "v² = v₀² + 2 · a · d → d = v₀² : (2a) = %s : %s = %s m." % (v0 * v0, 2 * a, num(d)))
    if k == "mrua_d":
        v0, a, t = R.choice([(0, 2, 10), (5, 2, 4), (10, 3, 6), (0, 4, 5), (2, 1, 8), (0, 3, 4)])
        d = v0 * t + 0.5 * a * t * t
        return nq("Un móvil parte a %s m/s con a = %s m/s². ¿Qué distancia recorre en %s s?" % (v0, a, t), d, [v0 * t + a * t * t, v0 * t, a * t], "m",
                  "x = v₀ · t + ½ · a · t² = %s · %s + 0,5 · %s · %s² = %s m." % (v0, t, a, t, num(d)))
    if k == "encuentro":
        d, v1, v2 = R.choice([(300, 20, 10), (1000, 30, 20), (600, 15, 15), (900, 25, 20), (120, 4, 2)])
        t = d / (v1 + v2)
        return nq("Dos ciclistas separados %s m van uno hacia el otro a %s m/s y %s m/s. ¿Cuándo se encuentran?" % (num(d), v1, v2), t, [d / abs(v1 - v2) if v1 != v2 else d / v1, d / v1, d * (v1 + v2)], "s",
                  "Se acercan a %s + %s = %s m/s: t = %s : %s = %s s." % (v1, v2, v1 + v2, num(d), v1 + v2, num(t)))
    d1, t1, d2, t2 = R.choice([(100, 10, 100, 40), (60, 2, 60, 1), (200, 20, 300, 30), (50, 5, 150, 5)])
    return nq("Un móvil recorre %s m en %s s y luego %s m en %s s. ¿Cuál es su velocidad media total?" % (d1, t1, d2, t2), (d1 + d2) / (t1 + t2), [(d1 / t1 + d2 / t2) / 2, d1 / t1, (d1 + d2) / t1], "m/s",
              "v = (%s + %s) : (%s + %s) = %s m/s." % (d1, d2, t1, t2, num((d1 + d2) / (t1 + t2))))


def f_newt(R):
    k = R.choice(["F", "a", "m", "roz", "plano", "circ"])
    if k == "F":
        m, a = R.choice([(10, 2), (1200, 3), (0.5, 4), (70, 1.5), (2, 9.8), (800, 2.5)])
        return nq("¿Qué fuerza neta hace falta para que %s kg aceleren a %s m/s²?" % (num(m), num(a)), m * a, [m / a, a / m, m + a], "N", "F = m · a = %s · %s = %s N." % (num(m), num(a), num(m * a)))
    if k == "a":
        F, m = R.choice([(100, 20), (600, 1200), (30, 5), (2000, 800), (45, 15)])
        return nq("Una fuerza neta de %s N actúa sobre %s kg. ¿Qué aceleración produce?" % (num(F), num(m)), F / m, [F * m, m / F, F - m], "m/s²", "a = F : m = %s : %s = %s m/s²." % (num(F), num(m), num(F / m)))
    if k == "m":
        F, a = R.choice([(50, 2), (300, 1.5), (24, 3), (980, 9.8), (120, 4)])
        return nq("Una fuerza neta de %s N produce una aceleración de %s m/s². ¿Cuál es la masa?" % (num(F), num(a)), F / a, [F * a, a / F, F - a], "kg", "m = F : a = %s : %s = %s kg." % (num(F), num(a), num(F / a)))
    if k == "roz":
        m, mu = R.choice([(10, 0.2), (50, 0.3), (5, 0.4), (20, 0.1), (100, 0.5)])
        return nq("Una caja de %s kg se arrastra por el suelo con μ = %s. ¿Cuánto vale la fuerza de rozamiento? (g = 9,8 m/s²)" % (m, num(mu)), mu * m * G, [mu * m, m * G, m * G / mu], "N",
                  "Fr = μ · m · g = %s · %s · 9,8 = %s N." % (num(mu), m, num(mu * m * G)))
    if k == "plano":
        F, Fr, m = R.choice([(100, 40, 20), (50, 20, 10), (300, 100, 50), (80, 30, 25), (200, 80, 40)])
        return nq("Empujas una caja de %s kg con %s N y el rozamiento es de %s N. ¿Qué aceleración tiene?" % (m, F, Fr), (F - Fr) / m, [F / m, (F + Fr) / m, (F - Fr) * m], "m/s²",
                  "F neta = %s − %s = %s N; a = %s : %s = %s m/s²." % (F, Fr, F - Fr, F - Fr, m, num((F - Fr) / m)))
    m, v, r = R.choice([(1000, 20, 50), (0.5, 4, 2), (70, 10, 20), (2, 6, 3), (1200, 15, 75)])
    return nq("Un cuerpo de %s kg gira a %s m/s en una curva de radio %s m. ¿Qué fuerza centrípeta necesita?" % (num(m), v, r), m * v * v / r, [m * v / r, m * v * v * r, v * v / r], "N",
              "Fc = m · v² : r = %s · %s² : %s = %s N." % (num(m), v, r, num(m * v * v / r)))


def f_pres(R):
    k = R.choice(["p", "hid", "hid", "arq", "pascal", "atm"])
    if k == "p":
        F, S = R.choice([(600, 0.04), (500, 0.02), (60, 0.0005), (800, 0.2), (1000, 0.5), (700, 0.01)])
        return nq("Una fuerza de %s N actúa sobre %s m². ¿Qué presión ejerce?" % (num(F), num(S)), F / S, [F * S, S / F, F / S / 100], "Pa", "p = F : S = %s : %s = %s Pa." % (num(F), num(S), num(F / S)))
    if k == "hid":
        h, d = R.choice([(10, 1000), (5, 1000), (20, 1030), (2, 1000), (50, 1030), (0.5, 13600)])
        return nq("¿Qué presión hidrostática hay a %s m de profundidad en un líquido de densidad %s kg/m³? (g = 9,8 m/s²)" % (num(h), num(d)), d * G * h, [d * h, d * G, d * G / h], "Pa",
                  "p = d · g · h = %s · 9,8 · %s = %s Pa." % (num(d), num(h), num(d * G * h)))
    if k == "arq":
        V, d = R.choice([(0.002, 1000), (0.01, 1000), (0.5, 1030), (0.001, 1000), (0.03, 800)])
        return nq("Un objeto de %s m³ está totalmente sumergido en un líquido de %s kg/m³. ¿Qué empuje recibe? (g = 9,8 m/s²)" % (num(V), num(d)), d * G * V, [d * V, d * G, V * G], "N",
                  "E = d · g · V = %s · 9,8 · %s = %s N (principio de Arquímedes)." % (num(d), num(V), num(d * G * V)))
    if k == "pascal":
        F1, S1, S2 = R.choice([(100, 0.01, 0.5), (50, 0.02, 1), (20, 0.005, 0.2), (200, 0.04, 2), (10, 0.001, 0.1)])
        return nq("En una prensa hidráulica se aplican %s N sobre %s m². ¿Qué fuerza sale en el émbolo de %s m²?" % (F1, num(S1), num(S2)), F1 * S2 / S1, [F1 * S1 / S2, F1, F1 * S2], "N",
                  "F₂ = F₁ · S₂ : S₁ = %s · %s : %s = %s N." % (F1, num(S2), num(S1), num(F1 * S2 / S1)))
    p = R.choice([101300, 50650, 202600, 151950, 303900])
    return nq("Expresa %s Pa en atmósferas (1 atm = 101 300 Pa)." % num(p), p / 101300, [p * 101300, p / 1000, p / 760], "atm", "%s : 101 300 = %s atm." % (num(p), num(p / 101300)))


def f_trab(R):
    k = R.choice(["W", "P", "ec", "caida", "rend", "Wang"])
    if k == "W":
        F, d = R.choice([(50, 10), (200, 3), (15, 4), (100, 25), (80, 1.5)])
        return nq("Una fuerza de %s N desplaza un cuerpo %s m en su misma dirección. ¿Qué trabajo realiza?" % (F, num(d)), F * d, [F / d, d / F, F + d], "J", "W = F · d = %s · %s = %s J." % (F, num(d), num(F * d)))
    if k == "Wang":
        F, d, ang, c = R.choice([(100, 10, 60, 0.5), (50, 4, 60, 0.5), (200, 5, 90, 0), (80, 3, 0, 1)])
        if ang == 90:
            return it("Llevas una bolsa de %s N horizontalmente %s m. ¿Qué trabajo hace la fuerza vertical con que la sujetas?" % (F, d), "0 J", ["%s J" % (F * d), "%s J" % (F // 2 * d), "%s J" % F],
                      "La fuerza es perpendicular al desplazamiento: cos 90° = 0, el trabajo es nulo.")
        return nq("Una fuerza de %s N forma %s° con el desplazamiento de %s m. ¿Qué trabajo realiza?" % (F, ang, d), F * d * c, [F * d, F * d * 0.87 if c != 1 else F * d / 2, F * c], "J",
                  "W = F · d · cos α = %s · %s · %s = %s J." % (F, d, num(c), num(F * d * c)))
    if k == "P":
        W, t = R.choice([(3000, 60), (12000, 30), (500, 10), (90000, 120), (1800, 4)])
        return nq("Un motor realiza %s J en %s s. ¿Qué potencia tiene?" % (num(W), t), W / t, [W * t, t / W, W / t / 1000], "W", "P = W : t = %s : %s = %s W." % (num(W), t, num(W / t)))
    if k == "ec":
        m, v = R.choice([(1000, 20), (60, 8), (0.2, 30), (1500, 10), (80, 5)])
        return nq("¿Qué energía cinética tiene un cuerpo de %s kg a %s m/s?" % (num(m), v), 0.5 * m * v * v, [m * v * v, 0.5 * m * v, m * v], "J",
                  "Ec = ½ · m · v² = %s J." % num(0.5 * m * v * v))
    if k == "caida":
        h = R.choice([5, 20, 45, 10, 80, 1.8])
        v = (2 * G * h) ** 0.5
        return nq("Un objeto cae desde %s m sin rozamiento. ¿Con qué velocidad llega al suelo? (g = 9,8 m/s²)" % num(h), v, [2 * G * h, G * h, (G * h) ** 0.5], "m/s",
                  "Conservación: m · g · h = ½ · m · v² → v = √(2 · 9,8 · %s) = %s m/s." % (num(h), num(v)))
    u, t = R.choice([(400, 1000), (300, 1200), (90, 100), (1800, 2000), (35, 100)])
    return nq("Una máquina recibe %s J y aprovecha %s J. ¿Cuál es su rendimiento?" % (num(t), num(u)), u / t * 100, [t / u * 100, (t - u) / t * 100, u / t], "%",
              "Rendimiento = útil : total · 100 = %s : %s · 100 = %s %%." % (num(u), num(t), num(u / t * 100)))


MM = {"H₂": 2, "O₂": 32, "H₂O": 18, "CH₄": 16, "CO₂": 44, "C₃H₈": 44, "N₂": 28, "NH₃": 17, "Mg": 24, "MgO": 40, "Zn": 65, "HCl": 36.5, "ZnCl₂": 136, "CaCO₃": 100, "CaO": 56}


def f_esteq(R):
    k = R.choice(["m", "m", "gas", "conc", "rend"])
    if k == "m":
        eq, a, b, ca, cb = R.choice([("2 H₂ + O₂ → 2 H₂O", "H₂", "H₂O", 2, 2), ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "CH₄", "CO₂", 1, 1), ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "CH₄", "H₂O", 1, 2),
                                     ("N₂ + 3 H₂ → 2 NH₃", "N₂", "NH₃", 1, 2), ("2 Mg + O₂ → 2 MgO", "Mg", "MgO", 2, 2), ("CaCO₃ → CaO + CO₂", "CaCO₃", "CaO", 1, 1),
                                     ("CaCO₃ → CaO + CO₂", "CaCO₃", "CO₂", 1, 1), ("Zn + 2 HCl → ZnCl₂ + H₂", "Zn", "H₂", 1, 1)])
        na = R.choice([1, 2, 0.5, 3, 0.25])
        ma = na * MM[a]
        mb = na * cb / ca * MM[b]
        return nq("Según %s, ¿qué masa de %s se obtiene a partir de %s g de %s? (masas molares: %s = %s g/mol, %s = %s g/mol)" % (eq, b, num(ma), a, a, num(MM[a]), b, num(MM[b])), mb,
                  [ma, na * MM[b], na * ca / cb * MM[b] * 2 if ca != cb else ma * 2], "g",
                  "n(%s) = %s : %s = %s mol → n(%s) = %s mol → m = %s g." % (a, num(ma), num(MM[a]), num(na), b, num(na * cb / ca), num(mb)))
    if k == "gas":
        n_ = R.choice([0.5, 2, 1.5, 0.25, 3])
        return nq("¿Qué volumen ocupan %s mol de gas en condiciones normales? (1 mol = 22,4 L)" % num(n_), n_ * 22.4, [22.4 / n_, n_ * 24, n_ + 22.4], "L",
                  "V = n · 22,4 = %s · 22,4 = %s L." % (num(n_), num(n_ * 22.4)))
    if k == "conc":
        M, V = R.choice([(0.5, 0.2), (2, 0.1), (0.1, 0.5), (1, 0.25), (0.2, 2)])
        return nq("¿Cuántos moles de soluto hay en %s L de disolución %s M?" % (num(V), num(M)), M * V, [M / V, V / M, M + V], "mol", "n = M · V = %s · %s = %s mol." % (num(M), num(V), num(M * V)))
    t, r = R.choice([(44, 33), (100, 80), (36, 27), (88, 66), (50, 45)])
    return nq("En teoría se deberían obtener %s g de producto, pero se obtienen %s g. ¿Cuál es el rendimiento?" % (t, r), r / t * 100, [t / r * 100, (t - r) / t * 100, r / t], "%",
              "Rendimiento = real : teórico · 100 = %s : %s · 100 = %s %%." % (r, t, num(r / t * 100)))


def UNITS(grade):
    return [
        H("B", "la-celula-y-el-ciclo-celular", "La célula, el ciclo celular, la mitosis y la meiosis", "Mitosis y meiosis",
          "Los alumnos describen la célula, el núcleo y los cromosomas, el ciclo celular, y comparan la mitosis y la meiosis y su papel en el crecimiento y la reproducción sexual.",
          "célula eucariota, núcleo, cromatina, cromosomas, cromátidas, cariotipo, diploide, haploide, ciclo celular, interfase, mitosis, meiosis, gametos, sobrecruzamiento",
          "Mitosis: 2 células iguales. Meiosis: 4 gametos", "La meiosis reduce a la mitad el número de cromosomas y crea variedad.",
          ["El ADN se guarda en el núcleo como cromatina; antes de dividirse se condensa en cromosomas. Las células humanas tienen 46 cromosomas (23 pares): son diploides (2n).",
           "El ciclo celular tiene la interfase (crece y duplica el ADN) y la división. En la mitosis salen dos células hijas idénticas a la madre.",
           "La meiosis forma cuatro células haploides (n) distintas: los gametos. El sobrecruzamiento y el reparto al azar de cromosomas crean variabilidad."],
          [("Una célula con 46 cromosomas hace meiosis. ¿Cuántos tiene cada gameto?", ["La meiosis reduce a la mitad.", "46 : 2 = 23."], "23 cromosomas.")],
          [("La mitosis forma gametos.", "Los gametos se forman por meiosis."), ("Los cromosomas existen siempre condensados.", "Solo se condensan durante la división.")],
          [("¿Qué es un cariotipo?", "La imagen ordenada de los cromosomas de una célula."), ("¿Qué es el cáncer?", "Una división celular descontrolada por fallos en la regulación del ciclo.")],
          [("Fases de la mitosis", [("profase", "los cromosomas se condensan y desaparece la membrana nuclear"), ("metafase", "los cromosomas se alinean en el centro"),
                                    ("anafase", "las cromátidas se separan hacia los polos"), ("telofase", "se forman dos núcleos nuevos"), ("citocinesis", "se divide el citoplasma"), ("interfase", "la célula crece y duplica su ADN")],
            "¿Qué ocurre en la {k}?", "¿En qué fase {v}?", ["meiosis II"]),
           ("Mitosis o meiosis", {"las características de la mitosis": ["dos células hijas", "células idénticas a la madre", "mantiene el número de cromosomas", "sirve para crecer y reparar tejidos", "una sola división"],
                                  "las características de la meiosis": ["cuatro células hijas", "células haploides", "reduce a la mitad los cromosomas", "forma gametos", "hay sobrecruzamiento"]}),
           ("Conceptos", [("cromosoma", "ADN muy condensado y empaquetado"), ("cromátida", "cada una de las dos copias de un cromosoma duplicado"), ("centrómero", "zona que une las dos cromátidas"),
                          ("diploide", "célula con pares de cromosomas, 2n"), ("haploide", "célula con un solo juego de cromosomas, n"), ("cariotipo", "conjunto ordenado de los cromosomas"), ("gameto", "célula sexual haploide")],
            "¿Qué es: {k}?", D)],
          ["Las células humanas tienen 46 cromosomas.", "La mitosis forma dos células idénticas.", "La meiosis forma gametos.", "Los gametos son haploides.", "En la interfase se duplica el ADN.",
           "En la metafase los cromosomas se alinean en el centro.", "El sobrecruzamiento crea variabilidad."],
          [("La mitosis forma gametos.", "Los forma la meiosis."), ("Los gametos humanos tienen 46 cromosomas.", "Tienen 23."), ("La meiosis forma dos células idénticas.", "Forma cuatro distintas."),
           ("El ADN se duplica en la anafase.", "Se duplica en la interfase."), ("Las células somáticas son haploides.", "Son diploides.")],
          "la división celular", "living-things-and-ecosystems"),

        H("B", "genetica-mendeliana", "La herencia: las leyes de Mendel", "Genética mendeliana",
          "Los alumnos usan los conceptos de gen, alelo, genotipo y fenotipo, resuelven cruces de un carácter con cuadros de Punnett, y estudian la herencia del sexo, de los grupos sanguíneos y ligada al sexo.",
          "gen, alelo, dominante, recesivo, homocigoto, heterocigoto, genotipo, fenotipo, leyes de Mendel, cuadro de Punnett, codominancia, herencia ligada al sexo, daltonismo, hemofilia",
          "Aa × Aa da 3 dominantes por cada recesivo", "El genotipo son los alelos; el fenotipo, lo que se ve.",
          ["Un gen tiene variantes llamadas alelos. Si un individuo tiene dos alelos iguales es homocigoto (AA, aa); si son distintos, heterocigoto (Aa).",
           "El alelo dominante (A) se manifiesta aunque haya uno solo; el recesivo (a), solo en homocigosis. Del cruce Aa × Aa sale 1 AA : 2 Aa : 1 aa.",
           "En los grupos sanguíneos, Iᴬ e Iᴮ son codominantes y dominan sobre i. El daltonismo y la hemofilia se heredan ligados al cromosoma X."],
          [("Dos padres de ojos oscuros (Aa) tienen un hijo. ¿Probabilidad de ojos claros (aa)?", ["Cuadro de Punnett: AA, Aa, Aa, aa.", "1 de 4."], "25 %.")],
          [("Lo dominante es lo más frecuente.", "Dominante solo significa que se manifiesta en heterocigosis."), ("El padre decide si el hijo es heterocigoto.", "Cada progenitor aporta un alelo al azar.")],
          [("¿Por qué el daltonismo es más frecuente en hombres?", "Tienen un solo cromosoma X: basta un alelo recesivo."), ("¿Qué es un cruce prueba?", "Cruzar con un homocigoto recesivo para averiguar el genotipo de un dominante.")],
          [("Conceptos", [("gen", "fragmento de ADN que lleva información de un carácter"), ("alelo", "cada variante de un gen"), ("genotipo", "conjunto de alelos de un individuo"), ("fenotipo", "carácter que se manifiesta"),
                          ("homocigoto", "tiene dos alelos iguales"), ("heterocigoto", "tiene dos alelos distintos"), ("dominante", "alelo que se manifiesta con una sola copia"), ("recesivo", "alelo que solo se manifiesta en homocigosis")],
            "¿Qué es: {k}?", D),
           ("Genotipos", [("AA", "homocigoto dominante"), ("Aa", "heterocigoto"), ("aa", "homocigoto recesivo"), ("IᴬIᴮ", "grupo sanguíneo AB"), ("ii", "grupo sanguíneo 0"), ("XY", "hombre"), ("XX", "mujer"),
                          ("XᵈY", "hombre daltónico")],
            "¿Qué indica el genotipo {k}?", "¿Qué genotipo corresponde a: {v}?"),
           ("Leyes de Mendel", [("primera ley", "uniformidad: cruzando dos razas puras, toda la F1 es igual"), ("segunda ley", "segregación: los alelos se separan al formar los gametos"),
                                ("tercera ley", "independencia: los caracteres se heredan por separado"), ("generación F1", "primera generación filial"), ("proporción 3 : 1", "fenotipos de la F2 de Aa × Aa"),
                                ("proporción 1 : 2 : 1", "genotipos de la F2 de Aa × Aa")],
            "¿Qué es o qué dice: {k}?", D)],
          ["Aa es heterocigoto.", "El fenotipo es lo que se manifiesta.", "Del cruce Aa × Aa el 25 % es aa.", "El daltonismo está ligado al cromosoma X.", "Los alelos Iᴬ e Iᴮ son codominantes.",
           "Cada progenitor aporta un alelo.", "Una mujer es XX."],
          [("Aa es homocigoto.", "Es heterocigoto."), ("El genotipo es lo que se ve.", "Es el fenotipo."), ("Del cruce Aa × Aa todos son aa.", "Solo el 25 %."), ("El grupo 0 es dominante.", "El alelo i es recesivo."),
           ("La madre decide el sexo del bebé.", "Lo decide el espermatozoide del padre.")],
          "la genética", "living-things-and-ecosystems", calc=f_gen),

        H("B", "adn-y-biotecnologia", "El ADN, la expresión génica y la biotecnología", "ADN y biotecnología",
          "Los alumnos describen la estructura del ADN, su replicación, la síntesis de proteínas, las mutaciones y las aplicaciones de la ingeniería genética, con sus implicaciones éticas.",
          "ADN, nucleótidos, bases nitrogenadas, doble hélice, replicación, ARN, transcripción, traducción, código genético, mutaciones, ingeniería genética, transgénicos, CRISPR, clonación, bioética",
          "ADN → ARN → proteína", "A se une con T y C se une con G en la doble hélice.",
          ["El ADN es una doble hélice de nucleótidos con cuatro bases: adenina (A), timina (T), citosina (C) y guanina (G). A se une con T y C con G.",
           "La información de un gen se copia en ARN (transcripción) y se traduce en una proteína en los ribosomas (traducción).",
           "Una mutación es un cambio en el ADN. La ingeniería genética modifica genes: se usa para fabricar insulina, crear transgénicos o editar genes con CRISPR."],
          [("Una cadena de ADN es ATGCCA. ¿Cuál es la complementaria?", ["A–T y C–G.", "A→T, T→A, G→C, C→G, C→G, A→T."], "TACGGT.")],
          [("Todas las mutaciones son perjudiciales.", "Muchas son neutras y algunas son beneficiosas; son la base de la evolución."), ("El ARN tiene timina.", "El ARN tiene uracilo en lugar de timina.")],
          [("¿Qué es un organismo transgénico?", "Uno al que se le ha introducido un gen de otra especie."), ("¿Qué es la PCR?", "Una técnica que copia millones de veces un fragmento de ADN.")],
          [("Bases complementarias", [("adenina en el ADN", "timina"), ("timina", "adenina"), ("citosina", "guanina"), ("guanina", "citosina"), ("adenina en el ARN", "uracilo")],
            "¿Con qué base se empareja: {k}?", None, ["ribosa", "fosfato"]),
           ("Procesos", [("replicación", "copia del ADN antes de la división"), ("transcripción", "copia de un gen en ARN mensajero"), ("traducción", "síntesis de una proteína en el ribosoma"),
                         ("mutación", "cambio en la secuencia del ADN"), ("clonación", "obtención de individuos genéticamente idénticos"), ("PCR", "multiplicación de un fragmento de ADN en el laboratorio"),
                         ("terapia génica", "introducción de genes para tratar una enfermedad")],
            "¿Qué es: {k}?", D),
           ("Aplicaciones", [("insulina humana fabricada por bacterias", "medicina"), ("vacunas de ARN mensajero", "medicina"), ("pruebas de paternidad", "medicina forense"), ("identificar a un sospechoso por su ADN", "medicina forense"),
                             ("maíz resistente a plagas", "agricultura"), ("arroz dorado con vitamina A", "agricultura"), ("bacterias que degradan petróleo", "medio ambiente"), ("biocombustibles con algas", "medio ambiente")],
            "¿En qué campo se aplica: {k}?", None, ["astronomía"])],
          ["La adenina se une con la timina.", "El ADN tiene forma de doble hélice.", "El ARN tiene uracilo.", "La traducción ocurre en los ribosomas.", "Una mutación es un cambio en el ADN.",
           "Las bacterias pueden fabricar insulina humana.", "CRISPR permite editar genes."],
          [("La adenina se une con la citosina.", "Se une con la timina."), ("Todas las mutaciones son malas.", "Muchas son neutras."), ("El ARN tiene timina.", "Tiene uracilo."), ("La transcripción fabrica proteínas.", "Fabrica ARN."),
           ("El ADN está formado por aminoácidos.", "Está formado por nucleótidos.")],
          "el ADN", "living-things-and-ecosystems"),

        H("B", "la-evolucion", "La evolución de los seres vivos", "La evolución",
          "Los alumnos comparan el fijismo, el lamarckismo, el darwinismo y la teoría sintética, interpretan pruebas de la evolución y explican la selección natural, la especiación y la evolución humana.",
          "fijismo, lamarckismo, darwinismo, selección natural, neodarwinismo, variabilidad, mutación, adaptación, especiación, fósiles, órganos homólogos y análogos, evolución humana, Atapuerca",
          "La selección natural favorece a los mejor adaptados", "La variabilidad surge de las mutaciones y de la reproducción sexual.",
          ["Lamarck pensaba que los caracteres adquiridos se heredan. Darwin y Wallace propusieron la selección natural: sobreviven y se reproducen más los mejor adaptados.",
           "La teoría sintética une la selección natural con la genética: las mutaciones y la recombinación crean variabilidad.",
           "Pruebas: fósiles, órganos homólogos (mismo origen), análogos (misma función), embriología y ADN. En Atapuerca hay fósiles humanos de hace más de 800 000 años."],
          [("Las jirafas de cuello largo alcanzaban más hojas y tenían más crías. ¿Qué teoría lo explica?", ["No es que estiraran el cuello y lo heredaran.", "Hay variación y la naturaleza selecciona."], "La selección natural de Darwin.")],
          [("Los individuos evolucionan a lo largo de su vida.", "Evolucionan las poblaciones a lo largo de generaciones."), ("El ser humano desciende del chimpancé.", "Ambos tienen un antepasado común.")],
          [("¿Qué es Atapuerca?", "Un yacimiento de Burgos con fósiles de Homo antecessor y otros homínidos."), ("¿Por qué las bacterias se hacen resistentes a los antibióticos?", "Sobreviven las que tienen mutaciones de resistencia y se multiplican.")],
          [("Teorías", [("fijismo", "las especies no cambian desde su creación"), ("lamarckismo", "los caracteres adquiridos por el uso se heredan"), ("darwinismo", "la selección natural actúa sobre la variación"),
                        ("teoría sintética", "selección natural más genética y mutaciones"), ("catastrofismo", "grandes catástrofes eliminaban especies"), ("equilibrio puntuado", "largos periodos estables con cambios rápidos")],
            "¿Qué propone: {k}?", D),
           ("Pruebas", [("ala de murciélago y brazo humano", "órganos homólogos"), ("ala de mariposa y ala de ave", "órganos análogos"), ("coxis humano", "órgano vestigial"), ("Archaeopteryx", "fósil de transición"),
                        ("embriones de vertebrados muy parecidos", "prueba embriológica"), ("ADN muy parecido entre humano y chimpancé", "prueba molecular"), ("pinzones de las Galápagos", "prueba biogeográfica")],
            "¿Qué prueba de la evolución es: {k}?", None),
           ("Homínidos", [("Australopithecus afarensis", "bípedo africano de hace 3 millones de años, como Lucy"), ("Homo habilis", "primeros útiles de piedra"), ("Homo erectus", "dominó el fuego y salió de África"),
                          ("Homo antecessor", "homínido de Atapuerca de hace más de 800 000 años"), ("Homo neanderthalensis", "vivió en Europa y convivió con los sapiens"), ("Homo sapiens", "nuestra especie, de hace unos 300 000 años")],
            "¿Qué rasgo tiene: {k}?", D)],
          ["La selección natural favorece a los mejor adaptados.", "Las poblaciones evolucionan.", "El ala del murciélago y el brazo humano son homólogos.", "Las mutaciones crean variabilidad.", "Homo antecessor se encontró en Atapuerca.",
           "Darwin propuso la selección natural.", "Humanos y chimpancés tienen un antepasado común."],
          [("Los individuos evolucionan en su vida.", "Evolucionan las poblaciones."), ("Descendemos del chimpancé.", "Tenemos un antepasado común."), ("Lamarck propuso la selección natural.", "Fue Darwin."),
           ("El ala del ave y la de la mariposa son homólogas.", "Son análogas."), ("Los caracteres adquiridos se heredan.", "No se heredan.")],
          "la evolución", "living-things-and-ecosystems"),

        H("B", "la-tectonica-de-placas", "La estructura de la Tierra y la tectónica de placas", "Tectónica de placas",
          "Los alumnos describen la estructura interna de la Tierra, la deriva continental, la tectónica de placas, los tipos de bordes, y relacionan volcanes, terremotos y cordilleras con los límites de placas.",
          "corteza, manto, núcleo, litosfera, astenosfera, ondas sísmicas, deriva continental, Wegener, placas litosféricas, dorsales, subducción, fallas, pliegues, volcanes, terremotos",
          "La litosfera está dividida en placas que se mueven", "En los bordes de placas se concentran volcanes y terremotos.",
          ["La Tierra tiene corteza, manto y núcleo. Mecánicamente, la litosfera rígida flota sobre la astenosfera más plástica.",
           "Wegener propuso la deriva continental. Hoy sabemos que la litosfera se divide en placas que se mueven unos centímetros al año, impulsadas por el calor interno.",
           "En los bordes divergentes (dorsales) se crea litosfera; en los convergentes se destruye (subducción) o se forman cordilleras; en los transformantes las placas se deslizan."],
          [("¿Por qué hay tantos volcanes en Japón?", ["Japón está en un borde convergente.", "Una placa se hunde bajo otra: subducción."], "Por la subducción entre placas.")],
          [("Los continentes flotan sobre lava líquida.", "El manto es sólido aunque se deforma muy lentamente."), ("Las placas se mueven muy deprisa.", "Se mueven pocos centímetros al año, como crecen las uñas.")],
          [("¿Por qué Canarias tiene volcanes?", "Por un punto caliente del manto bajo la placa africana."), ("¿Qué es el epicentro?", "El punto de la superficie situado encima del hipocentro de un terremoto.")],
          [("Capas", [("corteza", "capa externa sólida de rocas silicatadas"), ("manto", "capa intermedia de silicatos de hierro y magnesio"), ("núcleo externo", "hierro y níquel líquidos"),
                      ("núcleo interno", "hierro y níquel sólidos por la enorme presión"), ("litosfera", "capa rígida formada por corteza y manto superior"), ("astenosfera", "parte del manto más plástica bajo la litosfera")],
            "¿Qué es o cómo es: {k}?", D),
           ("Bordes de placas", [("dorsal mesoatlántica", "borde divergente"), ("rift de África oriental", "borde divergente"), ("Andes", "borde convergente con subducción"), ("Japón", "borde convergente con subducción"),
                                 ("Himalaya", "borde convergente entre continentes"), ("Alpes", "borde convergente entre continentes"), ("falla de San Andrés", "borde transformante")],
            "¿Qué tipo de borde hay en: {k}?", None, ["centro de una placa sin actividad"]),
           ("Pruebas de la deriva", {"las pruebas de Wegener": ["encaje de las costas de África y Sudamérica", "fósiles iguales en continentes separados", "rocas iguales a ambos lados del Atlántico", "huellas de glaciares en zonas hoy tropicales", "Pangea"],
                                     "las pruebas modernas": ["edad de los fondos oceánicos", "bandas magnéticas de las dorsales", "medidas por GPS", "distribución de los terremotos", "sondeos del fondo marino"]})],
          ["La litosfera está dividida en placas.", "En las dorsales se crea litosfera.", "El Himalaya se formó por choque de continentes.", "Wegener propuso la deriva continental.", "El núcleo externo es líquido.",
           "Las placas se mueven pocos centímetros al año.", "Canarias se formó por un punto caliente."],
          [("El manto es lava líquida.", "Es sólido y plástico."), ("En las dorsales se destruye litosfera.", "Se crea."), ("Las placas se mueven metros al día.", "Centímetros al año."), ("El núcleo interno es líquido.", "Es sólido."),
           ("La falla de San Andrés es un borde divergente.", "Es transformante.")],
          "la tectónica de placas", "earths-systems"),

        H("B", "la-historia-de-la-tierra", "La historia de la Tierra: tiempo geológico y fósiles", "Historia de la Tierra",
          "Los alumnos aplican los principios de la estratigrafía y la datación relativa y absoluta, interpretan cortes geológicos sencillos y describen las eras geológicas y los grandes acontecimientos de la historia de la vida.",
          "tiempo geológico, estratos, principio de superposición, datación relativa y absoluta, radiactividad, fósiles guía, eones, eras, Precámbrico, Paleozoico, Mesozoico, Cenozoico, extinciones",
          "Los estratos de abajo son los más antiguos", "La Tierra tiene unos 4600 millones de años.",
          ["Principio de superposición: en una serie sin deformar, los estratos inferiores son más antiguos. Un fósil guía vivió poco tiempo y en muchos lugares, y data los estratos.",
           "La datación absoluta usa elementos radiactivos que se desintegran a un ritmo conocido.",
           "La Tierra tiene unos 4600 millones de años. Eras: Precámbrico, Paleozoico (trilobites), Mesozoico (dinosaurios) y Cenozoico (mamíferos y humanos)."],
          [("Un estrato con ammonites está bajo otro con mamuts. ¿Cuál es más antiguo?", ["El de abajo es más antiguo.", "Los ammonites son del Mesozoico y los mamuts del Cenozoico."], "El estrato con ammonites.")],
          [("Los humanos convivieron con los dinosaurios.", "Los dinosaurios no avianos se extinguieron hace 66 millones de años; los humanos aparecieron mucho después."), ("Todos los fósiles sirven para datar.", "Solo los fósiles guía son útiles.")],
          [("¿Qué causó la extinción de los dinosaurios?", "Principalmente el impacto de un gran asteroide hace 66 millones de años."), ("¿Qué es el periodo de semidesintegración?", "El tiempo en que se desintegra la mitad de los átomos radiactivos de una muestra.")],
          [("Eras", [("primeras bacterias", "Precámbrico"), ("estromatolitos", "Precámbrico"), ("trilobites", "Paleozoico"), ("primeros anfibios", "Paleozoico"), ("bosques de helechos gigantes del carbón", "Paleozoico"),
                     ("dinosaurios", "Mesozoico"), ("ammonites", "Mesozoico"), ("primeras aves", "Mesozoico"), ("mamuts", "Cenozoico"), ("primeros homínidos", "Cenozoico"), ("nummulites", "Cenozoico")],
            "¿En qué era vivieron o aparecieron: {k}?", None),
           ("Principios", [("superposición", "los estratos de abajo son más antiguos"), ("horizontalidad", "los estratos se depositan horizontales"), ("continuidad lateral", "un estrato tiene la misma edad en toda su extensión"),
                           ("intersección", "lo que corta a un estrato es posterior a él"), ("sucesión faunística", "cada época tiene fósiles característicos"), ("actualismo", "los procesos del pasado son como los de hoy")],
            "¿Qué dice el principio de {k}?", D),
           ("Acontecimientos", [("formación de la Tierra", "hace unos 4600 millones de años"), ("primeros seres vivos", "hace unos 3800 millones de años"), ("explosión del Cámbrico", "hace unos 540 millones de años"),
                                ("extinción del Pérmico", "hace unos 252 millones de años"), ("extinción de los dinosaurios", "hace unos 66 millones de años"), ("aparición de Homo sapiens", "hace unos 300 000 años")],
            "¿Cuándo ocurrió: {k}?", "¿Qué ocurrió {v}?")],
          ["Los estratos inferiores son más antiguos.", "Los dinosaurios vivieron en el Mesozoico.", "La Tierra tiene unos 4600 millones de años.", "Los trilobites son del Paleozoico.", "Los fósiles guía sirven para datar.",
           "Un asteroide contribuyó a extinguir a los dinosaurios.", "Lo que corta un estrato es posterior a él."],
          [("Los humanos convivieron con los dinosaurios.", "No coincidieron."), ("Los estratos de arriba son más antiguos.", "Son más modernos."), ("Los trilobites son del Cenozoico.", "Son del Paleozoico."),
           ("La Tierra tiene 6000 años.", "Tiene unos 4600 millones de años."), ("Todos los fósiles son fósiles guía.", "Solo algunos.")],
          "la historia de la Tierra", "earths-systems"),

        H("B", "ecologia-y-medio-ambiente", "Ecología y medio ambiente", "Ecología",
          "Los alumnos analizan los factores limitantes, las adaptaciones, el flujo de energía y los ciclos de la materia, las pirámides tróficas, la sucesión ecológica y los impactos humanos con medidas de sostenibilidad.",
          "factor limitante, nicho ecológico, hábitat, adaptaciones, cadena y red trófica, pirámides, eficiencia, ciclo del carbono, sucesión ecológica, biodiversidad, impactos ambientales, desarrollo sostenible",
          "Solo el 10 % de la energía pasa al nivel siguiente", "La materia circula en ciclos; la energía fluye y se pierde como calor.",
          ["Un factor limitante (agua, luz, temperatura) controla el tamaño de una población. El nicho es el papel de una especie en el ecosistema.",
           "En cada nivel trófico solo pasa alrededor del 10 % de la energía al siguiente; por eso las cadenas son cortas.",
           "La materia se recicla en ciclos como el del carbono. La sucesión ecológica lleva un ecosistema hacia la comunidad clímax. Los impactos humanos alteran el equilibrio."],
          [("Los productores tienen 10 000 kJ. ¿Cuánta energía llega a los consumidores secundarios?", ["Primarios: 10 % de 10 000 = 1000 kJ.", "Secundarios: 10 % de 1000 = 100 kJ."], "Unos 100 kJ.")],
          [("La energía se recicla como la materia.", "La energía fluye y se disipa; la materia se recicla."), ("Una especie invasora aumenta siempre la biodiversidad.", "Suele desplazar especies autóctonas y reducirla.")],
          [("¿Qué es la huella ecológica?", "La superficie necesaria para producir lo que consumimos y absorber nuestros residuos."), ("¿Qué es la sucesión secundaria?", "La recuperación de un ecosistema tras una perturbación, como un incendio.")],
          [("Impactos", [("quema de combustibles fósiles", "cambio climático"), ("vertido de plásticos al mar", "contaminación marina"), ("tala de bosques", "deforestación y pérdida de suelo"),
                         ("exceso de abonos en los campos", "eutrofización de las aguas"), ("introducción del cangrejo americano", "pérdida de especies autóctonas"), ("emisiones de CFC", "destrucción de la capa de ozono"),
                         ("sobreexplotación de acuíferos", "salinización y desecación de humedales")],
            "¿Qué impacto ambiental produce: {k}?", "¿Qué actividad causa {v}?"),
           ("Conceptos", [("factor limitante", "factor que controla el tamaño de una población"), ("nicho ecológico", "papel que desempeña una especie en el ecosistema"), ("hábitat", "lugar donde vive una especie"),
                          ("pirámide de energía", "representa la energía de cada nivel trófico"), ("comunidad clímax", "etapa final y estable de la sucesión"), ("biomasa", "masa de materia orgánica de un nivel"),
                          ("productividad", "biomasa producida por unidad de tiempo")],
            "¿Qué es: {k}?", D),
           ("Ciclo del carbono", {"los procesos que retiran CO₂ de la atmósfera": ["fotosíntesis", "disolución en los océanos", "formación de caliza", "crecimiento de bosques", "formación de carbón y petróleo"],
                                  "los procesos que devuelven CO₂ a la atmósfera": ["respiración", "combustión", "erupciones volcánicas", "descomposición", "incendios forestales"]})],
          ["Solo pasa un 10 % de la energía al nivel siguiente.", "La materia se recicla en el ecosistema.", "La fotosíntesis retira CO₂ de la atmósfera.", "La sucesión lleva al clímax.", "El exceso de abonos causa eutrofización.",
           "Los CFC destruyen la capa de ozono.", "El nicho es el papel de una especie."],
          [("La energía se recicla.", "Fluye y se pierde como calor."), ("Pasa el 90 % de la energía al nivel siguiente.", "Pasa en torno al 10 %."), ("La respiración retira CO₂.", "Lo devuelve."),
           ("Las especies invasoras aumentan la biodiversidad.", "Suelen reducirla."), ("La eutrofización la causan los CFC.", "La causa el exceso de nutrientes.")],
          "la ecología", "living-things-and-ecosystems"),

        H("F", "cinematica", "Cinemática: movimientos rectilíneos y circulares", "Cinemática",
          "Los alumnos describen el movimiento con magnitudes vectoriales, resuelven problemas de MRU, MRUA y caída libre, interpretan gráficas x-t y v-t y describen el movimiento circular uniforme.",
          "sistema de referencia, vector de posición, desplazamiento, velocidad, aceleración, MRU, MRUA, caída libre, gráficas x-t y v-t, movimiento circular uniforme, velocidad angular, periodo",
          "v = v₀ + a · t y x = x₀ + v₀ · t + ½ · a · t²", "En caída libre todos los cuerpos aceleran con g = 9,8 m/s².",
          ["MRU: x = x₀ + v · t. MRUA: v = v₀ + a · t y x = x₀ + v₀ · t + ½ · a · t². Sin el tiempo: v² = v₀² + 2 · a · Δx.",
           "En caída libre, sin rozamiento, todos los cuerpos caen con la misma aceleración g = 9,8 m/s².",
           "En el movimiento circular uniforme la rapidez es constante, pero hay aceleración centrípeta porque cambia la dirección. El periodo es el tiempo de una vuelta."],
          [("Un coche a 20 m/s frena con −4 m/s². ¿Cuánto tarda en parar?", ["v = v₀ + a · t → 0 = 20 − 4t.", "t = 5 s."], "5 s.")],
          [("Los objetos pesados caen antes.", "Sin aire, todos caen igual; en la Luna lo comprobó un astronauta con un martillo y una pluma."), ("Si la velocidad es cero, la aceleración es cero.", "En el punto más alto de un lanzamiento v = 0 pero a = g.")],
          [("¿Qué es la velocidad angular?", "El ángulo que gira un cuerpo por segundo, en rad/s."), ("¿Qué indica el área bajo una gráfica v-t?", "El desplazamiento.")],
          [("Ecuaciones", [("MRU", "x = x₀ + v · t"), ("velocidad en el MRUA", "v = v₀ + a · t"), ("posición en el MRUA", "x = x₀ + v₀ · t + ½ · a · t²"), ("MRUA sin tiempo", "v² = v₀² + 2 · a · Δx"),
                           ("caída libre", "a = g = 9,8 m/s²"), ("velocidad lineal en un MCU", "v = ω · r")],
            "¿Qué ecuación corresponde a: {k}?", "¿Qué expresa la ecuación {v}?"),
           ("Gráficas", [("x-t con recta horizontal", "reposo"), ("x-t con recta inclinada", "MRU"), ("v-t con recta horizontal", "MRU"), ("v-t con recta de pendiente positiva", "MRUA acelerado"),
                         ("v-t con recta de pendiente negativa", "MRUA que frena"), ("x-t con parábola", "MRUA"), ("a-t con recta horizontal distinta de cero", "MRUA")],
            "¿Qué movimiento representa una gráfica {k}?", None),
           ("Magnitudes", [("velocidad angular", "rad/s"), ("periodo", "s"), ("frecuencia", "Hz"), ("aceleración", "m/s²"), ("velocidad", "m/s"), ("desplazamiento", "m")],
            "¿En qué unidad del SI se mide: {k}?", "¿Qué magnitud se mide en {v}?", ["N", "J"])],
          ["En caída libre todos los cuerpos aceleran igual.", "En el MRU la velocidad es constante.", "En el MCU hay aceleración centrípeta.", "El área bajo la gráfica v-t es el desplazamiento.",
           "g vale unos 9,8 m/s² en la Tierra.", "El periodo es el tiempo de una vuelta.", "En el punto más alto de un lanzamiento la aceleración es g."],
          [("Los cuerpos pesados caen antes en el vacío.", "Caen igual."), ("En el MCU no hay aceleración.", "Hay aceleración centrípeta."), ("Si v = 0, entonces a = 0.", "No necesariamente."),
           ("La frecuencia se mide en segundos.", "Se mide en hercios."), ("En el MRUA la aceleración cambia.", "Es constante.")],
          "la cinemática", "forces-and-motion", calc=f_cine),

        H("F", "las-leyes-de-newton", "Las leyes de Newton y las fuerzas", "Leyes de Newton",
          "Los alumnos aplican las tres leyes de Newton, la fuerza de rozamiento, la fuerza centrípeta y la ley de gravitación universal para explicar y calcular movimientos.",
          "inercia, fuerza neta, F = m · a, acción y reacción, peso, normal, tensión, rozamiento, coeficiente de rozamiento, fuerza centrípeta, gravitación universal, satélites",
          "F = m · a", "A toda acción le corresponde una reacción igual y de sentido contrario.",
          ["Primera ley (inercia): si la fuerza neta es cero, un cuerpo sigue en reposo o en MRU.",
           "Segunda ley: la fuerza neta produce una aceleración, F = m · a. El rozamiento vale Fr = μ · N.",
           "Tercera ley: si A empuja a B, B empuja a A con la misma fuerza y sentido contrario. La gravitación universal: F = G · m₁ · m₂ / d²."],
          [("Empujas un carro de 20 kg con 60 N sin rozamiento. ¿Aceleración?", ["a = F : m.", "60 : 20 = 3."], "3 m/s².")],
          [("Acción y reacción se anulan.", "Actúan sobre cuerpos distintos, así que no se anulan."), ("Hace falta fuerza para mantener la velocidad.", "Solo para vencer el rozamiento; sin él seguiría en MRU.")],
          [("¿Por qué vas hacia delante cuando el autobús frena?", "Por la inercia: tu cuerpo tiende a seguir moviéndose."), ("¿Por qué la Luna no cae a la Tierra?", "Cae continuamente, pero su velocidad la hace girar en órbita.")],
          [("Leyes", [("primera ley de Newton", "principio de inercia"), ("segunda ley de Newton", "principio fundamental: F = m · a"), ("tercera ley de Newton", "principio de acción y reacción"),
                      ("ley de gravitación universal", "dos masas se atraen con una fuerza inversa al cuadrado de la distancia"), ("ley de Hooke", "la deformación de un muelle es proporcional a la fuerza")],
            "¿Qué dice la {k}?", D, ["principio de Arquímedes"]),
           ("Ejemplos", [("el cohete expulsa gases hacia abajo y sube", "tercera ley"), ("al remar, el agua empuja la barca", "tercera ley"), ("el pasajero se va hacia delante al frenar", "primera ley"),
                         ("el mantel sale de un tirón y la vajilla se queda", "primera ley"), ("un camión cargado acelera menos con la misma fuerza", "segunda ley"), ("al chutar más fuerte el balón sale más rápido", "segunda ley")],
            "¿Qué ley de Newton explica que {k}?", None, ["ley de Ohm"]),
           ("Fuerzas", [("peso", "atracción gravitatoria de la Tierra"), ("normal", "fuerza perpendicular de la superficie de apoyo"), ("tensión", "fuerza que transmite una cuerda tensa"),
                        ("rozamiento", "fuerza que se opone al deslizamiento"), ("fuerza centrípeta", "fuerza dirigida al centro de una curva"), ("empuje", "fuerza hacia arriba de un fluido")],
            "¿Qué es: {k}?", D)],
          ["F = m · a.", "Acción y reacción actúan sobre cuerpos distintos.", "Sin fuerza neta un cuerpo mantiene su velocidad.", "El rozamiento se opone al deslizamiento.", "La fuerza centrípeta apunta al centro.",
           "La Luna cae continuamente hacia la Tierra en su órbita.", "El cohete sube por acción y reacción."],
          [("Acción y reacción se anulan.", "Actúan sobre cuerpos distintos."), ("Hace falta fuerza para mantener la velocidad sin rozamiento.", "No hace falta."), ("La masa cambia en la Luna.", "Cambia el peso."),
           ("La fuerza centrípeta apunta hacia fuera.", "Apunta al centro."), ("A más masa, más aceleración con la misma fuerza.", "Menos aceleración.")],
          "las leyes de Newton", "forces-and-motion", calc=f_newt),

        H("F", "presion-y-fluidos", "La presión y los fluidos: Pascal y Arquímedes", "Presión y fluidos",
          "Los alumnos calculan presiones en sólidos y líquidos, aplican el principio fundamental de la hidrostática, el principio de Pascal y el de Arquímedes, y explican la presión atmosférica y sus aplicaciones meteorológicas.",
          "presión, pascal, superficie, presión hidrostática, principio de Pascal, prensa hidráulica, principio de Arquímedes, empuje, flotación, presión atmosférica, barómetro, borrascas y anticiclones",
          "p = F : S y p = d · g · h", "Un cuerpo flota si el empuje iguala su peso antes de hundirse del todo.",
          ["La presión es la fuerza por unidad de superficie: p = F : S, en pascales (Pa). Un cuchillo afilado corta mejor porque tiene menos superficie.",
           "En un líquido la presión aumenta con la profundidad: p = d · g · h. Principio de Pascal: la presión se transmite igual en todo el fluido (prensa hidráulica).",
           "Principio de Arquímedes: un cuerpo sumergido recibe un empuje igual al peso del líquido desalojado, E = d · g · V. La presión atmosférica normal es 101 300 Pa."],
          [("¿Qué presión hay a 10 m bajo el agua (sin contar el aire)?", ["p = d · g · h = 1000 · 9,8 · 10.", "= 98 000 Pa."], "98 000 Pa, casi 1 atm.")],
          [("El empuje depende del peso del objeto.", "Depende del volumen sumergido y de la densidad del líquido."), ("La presión del agua depende de la forma del recipiente.", "Solo depende de la profundidad y la densidad.")],
          [("¿Qué es un anticiclón?", "Una zona de altas presiones que suele traer buen tiempo."), ("¿Por qué flota un barco de acero?", "Su forma desaloja mucha agua: el empuje iguala su peso.")],
          [("Aplicaciones", [("frenos hidráulicos del coche", "principio de Pascal"), ("elevador hidráulico del taller", "principio de Pascal"), ("barco que flota", "principio de Arquímedes"),
                             ("submarino que sube y baja", "principio de Arquímedes"), ("globo aerostático", "principio de Arquímedes"), ("presa más gruesa en la base", "presión hidrostática"),
                             ("los oídos duelen al bucear", "presión hidrostática"), ("raquetas de nieve", "presión en sólidos")],
            "¿Qué principio explica: {k}?", None),
           ("Meteorología", [("anticiclón", "altas presiones y tiempo estable"), ("borrasca", "bajas presiones con nubes y lluvias"), ("isobaras", "líneas que unen puntos de igual presión"),
                             ("barómetro", "instrumento que mide la presión atmosférica"), ("viento", "aire que va de las altas a las bajas presiones"), ("hectopascal", "unidad de presión de los mapas del tiempo")],
            "¿Qué es: {k}?", D),
           ("Flota o se hunde", {"los objetos que flotan en agua": ["corcho", "barco de acero", "hielo", "madera de pino", "pelota de playa", "huevo en agua muy salada"],
                                 "los objetos que se hunden en agua": ["moneda", "piedra", "llave de hierro", "anillo de oro", "canica de vidrio", "huevo fresco en agua del grifo"]})],
          ["La presión es fuerza entre superficie.", "La presión en un líquido aumenta con la profundidad.", "El empuje es igual al peso del líquido desalojado.", "Los frenos hidráulicos usan el principio de Pascal.",
           "Un anticiclón tiene altas presiones.", "La presión atmosférica normal es de unos 101 300 Pa.", "Un cuchillo afilado ejerce más presión."],
          [("El empuje depende del peso del objeto.", "Depende del volumen sumergido."), ("La presión del agua depende de la forma del recipiente.", "Depende de la profundidad."), ("Una borrasca tiene altas presiones.", "Tiene bajas presiones."),
           ("El viento va de bajas a altas presiones.", "Va de altas a bajas."), ("Un barco de acero no puede flotar.", "Flota por su forma.")],
          "la presión y los fluidos", "forces-and-motion", calc=f_pres),

        H("F", "trabajo-energia-y-potencia", "Trabajo, energía mecánica y potencia", "Trabajo y energía",
          "Los alumnos calculan el trabajo, la potencia y el rendimiento, aplican la conservación de la energía mecánica, relacionan trabajo y calor y analizan la degradación de la energía en las máquinas.",
          "trabajo, julio, energía cinética, energía potencial, energía mecánica, conservación, rozamiento, potencia, vatio, kilovatio hora, rendimiento, calor, degradación de la energía",
          "W = F · d · cos α", "Sin rozamiento, la energía mecánica (Ec + Ep) se conserva.",
          ["Una fuerza realiza trabajo si desplaza su punto de aplicación: W = F · d · cos α. Si la fuerza es perpendicular al desplazamiento, no hay trabajo.",
           "La energía mecánica es la suma de la cinética (½ · m · v²) y la potencial (m · g · h). Sin rozamiento se conserva.",
           "La potencia es el trabajo por segundo, P = W : t. Ninguna máquina aprovecha toda la energía: el rendimiento es la energía útil entre la total."],
          [("Una bola cae 20 m sin rozamiento. ¿Con qué velocidad llega?", ["m · g · h = ½ · m · v².", "v = √(2 · 9,8 · 20) ≈ 19,8 m/s."], "Unos 19,8 m/s.")],
          [("Sujetar una mochila quieta es trabajo.", "En física no hay trabajo si no hay desplazamiento."), ("El rozamiento destruye energía.", "La transforma en energía térmica.")],
          [("¿Qué es un caballo de vapor?", "Una unidad antigua de potencia: 1 CV ≈ 735 W."), ("¿Por qué las bombillas LED son más eficientes?", "Transforman más energía en luz y menos en calor.")],
          [("Conceptos", [("trabajo", "producto de la fuerza por el desplazamiento en su dirección"), ("energía cinética", "energía que tiene un cuerpo por su velocidad"), ("energía potencial gravitatoria", "energía por la altura"),
                          ("energía mecánica", "suma de las energías cinética y potencial"), ("potencia", "trabajo realizado por unidad de tiempo"), ("rendimiento", "energía útil entre energía consumida"),
                          ("degradación de la energía", "pérdida de calidad de la energía al transformarse en calor")],
            "¿Qué es: {k}?", D),
           ("Unidades", [("trabajo", "julio"), ("potencia", "vatio"), ("energía eléctrica de la factura", "kilovatio hora"), ("energía de los alimentos", "kilocaloría"), ("fuerza", "newton"),
                         ("potencia de un coche antiguo", "caballo de vapor")],
            "¿En qué unidad se suele medir: {k}?", None, ["pascal", "amperio"]),
           ("Transformaciones", [("montaña rusa que baja", "potencial en cinética"), ("pelota lanzada hacia arriba", "cinética en potencial"), ("frenado de un coche", "cinética en térmica"),
                                 ("arco tenso que dispara una flecha", "potencial elástica en cinética"), ("agua de un embalse que cae", "potencial en cinética y luego eléctrica"), ("péndulo que sube", "cinética en potencial")],
            "¿Qué transformación ocurre en: {k}?", None)],
          ["Sin rozamiento la energía mecánica se conserva.", "La potencia se mide en vatios.", "Si no hay desplazamiento no hay trabajo.", "Al frenar la energía cinética se transforma en calor.",
           "El rendimiento siempre es menor del 100 %.", "1 CV equivale a unos 735 W.", "La Ec depende del cuadrado de la velocidad."],
          [("Sujetar una mochila quieta es trabajo.", "No hay desplazamiento."), ("El rozamiento destruye energía.", "La transforma en calor."), ("El rendimiento puede superar el 100 %.", "Siempre es menor."),
           ("La potencia se mide en julios.", "Se mide en vatios."), ("La Ec es proporcional a la velocidad.", "Es proporcional a su cuadrado.")],
          "el trabajo y la energía", "energy", calc=f_trab),

        H("F", "reacciones-quimicas-y-estequiometria", "Reacciones químicas y cálculos estequiométricos", "Estequiometría",
          "Los alumnos ajustan ecuaciones químicas, realizan cálculos de masa, volumen y concentración a partir de ellas, y estudian tipos de reacciones (ácido-base, combustión, redox), su energía y su velocidad.",
          "ecuación química, ajuste, mol, masa molar, estequiometría, volumen molar, molaridad, rendimiento, reacciones exotérmicas y endotérmicas, ácidos y bases, pH, neutralización, combustión",
          "Los coeficientes indican la proporción en moles", "Una reacción exotérmica desprende energía; una endotérmica la absorbe.",
          ["Los coeficientes de una ecuación ajustada indican en qué proporción reaccionan los moles: en 2 H₂ + O₂ → 2 H₂O, 2 mol de H₂ dan 2 mol de agua.",
           "Para calcular: gramos → moles (n = m : M) → proporción de la ecuación → moles → gramos. En condiciones normales un mol de gas ocupa 22,4 L.",
           "Los ácidos tienen pH menor que 7 y las bases mayor que 7; al mezclarlos se neutralizan. Las combustiones son exotérmicas."],
          [("¿Cuántos gramos de agua dan 4 g de H₂? (2 H₂ + O₂ → 2 H₂O)", ["4 g : 2 g/mol = 2 mol de H₂.", "2 mol de H₂ dan 2 mol de agua = 36 g."], "36 g.")],
          [("Los coeficientes indican gramos.", "Indican moles o moléculas."), ("Un pH 2 es menos ácido que un pH 5.", "Cuanto menor es el pH, más ácido.")],
          [("¿Qué es un indicador?", "Una sustancia que cambia de color según el pH, como la fenolftaleína."), ("¿Por qué se pone bicarbonato para la acidez de estómago?", "Es una base que neutraliza el exceso de ácido.")],
          [("Tipos de reacciones", [("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "combustión"), ("HCl + NaOH → NaCl + H₂O", "neutralización"), ("CaCO₃ → CaO + CO₂", "descomposición"), ("2 H₂ + O₂ → 2 H₂O", "síntesis"),
                                    ("Zn + 2 HCl → ZnCl₂ + H₂", "sustitución"), ("4 Fe + 3 O₂ → 2 Fe₂O₃", "oxidación")],
            "¿Qué tipo de reacción es {k}?", None, ["fusión nuclear"]),
           ("pH", [("zumo de limón", "ácido"), ("vinagre", "ácido"), ("ácido del estómago", "ácido"), ("agua pura", "neutro"), ("sangre", "ligeramente básico"), ("lejía", "básico"), ("amoniaco", "básico"),
                   ("bicarbonato disuelto", "básico")],
            "¿Cómo es el pH de: {k}?", None, ["sin pH"]),
           ("Exotérmica o endotérmica", {"las reacciones exotérmicas": ["combustión del butano", "respiración celular", "oxidación del hierro", "neutralización de un ácido", "explosión de la pólvora"],
                                         "las reacciones endotérmicas": ["fotosíntesis", "cocción de un huevo", "descomposición de la caliza", "electrólisis del agua", "bolsa de frío instantáneo"]})],
          ["Los coeficientes indican proporciones en moles.", "Un mol de gas en condiciones normales ocupa 22,4 L.", "La combustión es exotérmica.", "El vinagre es ácido.", "La lejía es básica.",
           "Un ácido y una base se neutralizan.", "La fotosíntesis es endotérmica."],
          [("Los coeficientes indican gramos.", "Indican moles."), ("pH 2 es menos ácido que pH 5.", "Es más ácido."), ("La fotosíntesis es exotérmica.", "Es endotérmica."), ("La lejía es ácida.", "Es básica."),
           ("En una reacción se crea masa.", "La masa se conserva.")],
          "las reacciones químicas", "matter", calc=f_esteq),

        H("F", "quimica-del-carbono", "La química del carbono", "Química del carbono",
          "Los alumnos describen las características del átomo de carbono, los hidrocarburos y los grupos funcionales más sencillos, nombran compuestos orgánicos simples y valoran su importancia en la vida y la industria.",
          "átomo de carbono, enlaces simples, dobles y triples, hidrocarburos, alcanos, alquenos, alquinos, grupos funcionales, alcoholes, ácidos carboxílicos, polímeros, plásticos, biomoléculas",
          "El carbono forma cuatro enlaces", "Alcanos: enlaces simples; alquenos: dobles; alquinos: triples.",
          ["El carbono forma cuatro enlaces covalentes y puede unirse a otros carbonos formando cadenas y anillos: por eso hay millones de compuestos orgánicos.",
           "Los hidrocarburos tienen solo C e H: alcanos (-ano, enlaces simples), alquenos (-eno, dobles) y alquinos (-ino, triples). Prefijos: met- (1), et- (2), prop- (3), but- (4).",
           "Grupos funcionales: alcoholes (-OH, -ol), ácidos (-COOH, ácido -oico). Los polímeros, como los plásticos, son cadenas muy largas de monómeros."],
          [("Nombra CH₃–CH₂–CH₃.", ["Tres carbonos: prop-.", "Solo enlaces simples: -ano."], "Propano.")],
          [("Orgánico significa natural.", "Orgánico significa compuesto de carbono; muchos se fabrican."), ("El etanol es un hidrocarburo.", "Tiene oxígeno: es un alcohol.")],
          [("¿De dónde salen los plásticos?", "La mayoría se fabrican a partir del petróleo."), ("¿Qué es el ácido acético?", "El ácido del vinagre, CH₃COOH.")],
          [("Nombres", [("CH₄", "metano"), ("C₂H₆", "etano"), ("C₃H₈", "propano"), ("C₄H₁₀", "butano"), ("C₂H₄", "eteno o etileno"), ("C₂H₂", "etino o acetileno"), ("CH₃OH", "metanol"),
                        ("C₂H₅OH", "etanol"), ("CH₃COOH", "ácido acético")],
            "¿Cómo se nombra {k}?", "¿Cuál es la fórmula del {v}?"),
           ("Tipos", [("metano", "alcano"), ("butano", "alcano"), ("propano", "alcano"), ("eteno", "alqueno"), ("propeno", "alqueno"), ("etino", "alquino"), ("etanol", "alcohol"), ("metanol", "alcohol"),
                      ("ácido acético", "ácido carboxílico"), ("ácido fórmico", "ácido carboxílico")],
            "¿Qué tipo de compuesto es: {k}?", None),
           ("Usos", [("butano", "combustible doméstico"), ("etanol", "desinfectante y bebidas"), ("etileno", "fabricar polietileno"), ("acetileno", "soldadura"), ("ácido acético", "vinagre"),
                     ("polietileno", "bolsas y envases"), ("PVC", "tuberías"), ("glucosa", "fuente de energía de las células")],
            "¿Para qué se usa: {k}?", "¿Qué sustancia se usa para {v}?")],
          ["El carbono forma cuatro enlaces.", "Los alcanos solo tienen enlaces simples.", "El etanol es un alcohol.", "El butano es un alcano.", "Los plásticos son polímeros.", "El vinagre contiene ácido acético.",
           "El metano tiene un átomo de carbono."],
          [("El carbono forma dos enlaces.", "Forma cuatro."), ("Los alquenos tienen enlaces triples.", "Tienen dobles."), ("El etanol es un hidrocarburo.", "Es un alcohol."), ("Orgánico significa natural.", "Significa compuesto de carbono."),
           ("El propano tiene cuatro carbonos.", "Tiene tres.")],
          "la química del carbono", "matter"),
    ]
