# -*- coding: utf-8 -*-
"""España / Biología y Geología y Física y Química: 3.º de ESO"""
from es_sci import H, nq, num, it

D = "¿Qué corresponde a esta descripción: {v}?"

EL = [("H", "hidrógeno", 1, 1), ("He", "helio", 2, 4), ("Li", "litio", 3, 7), ("C", "carbono", 6, 12), ("N", "nitrógeno", 7, 14), ("O", "oxígeno", 8, 16), ("F", "flúor", 9, 19),
      ("Na", "sodio", 11, 23), ("Mg", "magnesio", 12, 24), ("Al", "aluminio", 13, 27), ("S", "azufre", 16, 32), ("Cl", "cloro", 17, 35), ("K", "potasio", 19, 39), ("Ca", "calcio", 20, 40),
      ("Fe", "hierro", 26, 56), ("Cu", "cobre", 29, 64), ("Zn", "cinc", 30, 65)]


def f_atomo(R):
    s, n, Z, A = R.choice(EL)
    k = R.choice(["n", "n", "e", "A", "ion"])
    if k == "n":
        return nq("Un átomo de %s tiene Z = %d y A = %d. ¿Cuántos neutrones tiene?" % (n, Z, A), A - Z, [A + Z, Z, A], "neutrones", "N = A − Z = %d − %d = %d." % (A, Z, A - Z))
    if k == "e":
        return nq("¿Cuántos electrones tiene un átomo neutro de %s (Z = %d)?" % (n, Z), Z, [A, A - Z, Z + 1], "electrones", "En un átomo neutro hay tantos electrones como protones: %d." % Z)
    if k == "A":
        return nq("Un átomo de %s tiene %d protones y %d neutrones. ¿Cuál es su número másico?" % (n, Z, A - Z), A, [A - Z, Z, 2 * A], "", "A = Z + N = %d + %d = %d." % (Z, A - Z, A))
    s, n, Z, A, q = R.choice([("Na", "sodio", 11, 23, 1), ("Mg", "magnesio", 12, 24, 2), ("Cl", "cloro", 17, 35, -1), ("O", "oxígeno", 8, 16, -2), ("Al", "aluminio", 13, 27, 3),
                              ("Ca", "calcio", 20, 40, 2), ("F", "flúor", 9, 19, -1), ("K", "potasio", 19, 39, 1)])
    sig = ("%d" % abs(q) if abs(q) > 1 else "") + ("+" if q > 0 else "−")
    return nq("¿Cuántos electrones tiene el ion %s%s (Z = %d)?" % (s, sig.translate(str.maketrans("0123456789+−", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")), Z), Z - q, [Z + q, Z, A - Z], "electrones",
              ("El ion tiene carga positiva: ha perdido %d electrones, %d − %d = %d." if q > 0 else "El ion tiene carga negativa: ha ganado %d electrones, %d + %d = %d.") % (abs(q), Z, abs(q), Z - q))


MOL = [("H₂O", "agua", 18), ("CO₂", "dióxido de carbono", 44), ("NaCl", "cloruro de sodio", 58.5), ("O₂", "oxígeno", 32), ("CH₄", "metano", 16), ("NH₃", "amoniaco", 17),
       ("H₂SO₄", "ácido sulfúrico", 98), ("CaCO₃", "carbonato de calcio", 100), ("N₂", "nitrógeno", 28), ("C₆H₁₂O₆", "glucosa", 180)]


def f_mol(R):
    f, n, M = R.choice(MOL)
    k = R.choice(["n", "n", "m", "M", "N", "conc"])
    if k == "n":
        m = R.choice([1, 2, 0.5, 3, 0.25, 4, 5]) * M
        return nq("¿Cuántos moles hay en %s g de %s (%s, M = %s g/mol)?" % (num(m), n, f, num(M)), m / M, [m * M, M / m, m / M * 2], "mol",
                  "n = m : M = %s : %s = %s mol." % (num(m), num(M), num(m / M)))
    if k == "m":
        x = R.choice([2, 0.5, 3, 0.1, 1.5, 4])
        return nq("¿Qué masa tienen %s mol de %s (M = %s g/mol)?" % (num(x), n, num(M)), x * M, [x / M, M / x, x + M], "g", "m = n · M = %s · %s = %s g." % (num(x), num(M), num(x * M)))
    if k == "M":
        a = {"H₂O": "2 · 1 + 16", "CO₂": "12 + 2 · 16", "O₂": "2 · 16", "CH₄": "12 + 4 · 1", "NH₃": "14 + 3 · 1", "N₂": "2 · 14", "CaCO₃": "40 + 12 + 3 · 16"}
        if f not in a:
            return None
        return nq("Calcula la masa molar de %s (H = 1, C = 12, N = 14, O = 16, Ca = 40)." % f, M, [M / 2, M + 16, M - 1], "g/mol", "M = %s = %s g/mol." % (a[f], num(M)))
    if k == "N":
        x = R.choice([1, 2, 0.5, 3, 0.1])
        return nq("¿Cuántas moléculas hay en %s mol de %s? (Nₐ = 6,02 · 10²³)" % (num(x), n), x * 6.02e23, [x * 6.02e22, x / 6.02e23, x * 6.02e24], "moléculas",
                  "N = n · Nₐ = %s · 6,02 · 10²³ = %s moléculas." % (num(x), num(x * 6.02e23)))
    n_, V = R.choice([(0.5, 0.25), (2, 1), (0.1, 0.5), (1, 0.5), (0.3, 0.2), (0.6, 1.5)])
    return nq("Se disuelven %s mol de soluto hasta %s L de disolución. ¿Cuál es la molaridad?" % (num(n_), num(V)), n_ / V, [n_ * V, V / n_, n_ / V / 1000], "mol/L",
              "M = n : V = %s : %s = %s mol/L." % (num(n_), num(V), num(n_ / V)))


def f_elec(R):
    k = R.choice(["I", "V", "R", "P", "E", "serie", "q"])
    if k == "I":
        V, Rr = R.choice([(12, 4), (9, 3), (230, 46), (6, 12), (4.5, 9), (24, 8)])
        return nq("Una resistencia de %s Ω se conecta a %s V. ¿Qué intensidad circula?" % (num(Rr), num(V)), V / Rr, [V * Rr, Rr / V, V - Rr], "A", "I = V : R = %s : %s = %s A." % (num(V), num(Rr), num(V / Rr)))
    if k == "V":
        I, Rr = R.choice([(2, 6), (0.5, 20), (3, 4), (0.2, 50), (1.5, 8)])
        return nq("Por una resistencia de %s Ω circulan %s A. ¿Qué voltaje tiene entre sus extremos?" % (num(Rr), num(I)), I * Rr, [I / Rr, Rr / I, I + Rr], "V", "V = I · R = %s · %s = %s V." % (num(I), num(Rr), num(I * Rr)))
    if k == "R":
        V, I = R.choice([(12, 3), (230, 2), (9, 0.5), (6, 0.2), (24, 4)])
        return nq("Un aparato a %s V consume %s A. ¿Qué resistencia tiene?" % (num(V), num(I)), V / I, [V * I, I / V, V - I], "Ω", "R = V : I = %s : %s = %s Ω." % (num(V), num(I), num(V / I)))
    if k == "P":
        V, I = R.choice([(230, 2), (12, 0.5), (230, 10), (9, 0.2), (230, 0.3)])
        return nq("Un aparato conectado a %s V consume %s A. ¿Qué potencia tiene?" % (num(V), num(I)), V * I, [V / I, I / V, V + I], "W", "P = V · I = %s · %s = %s W." % (num(V), num(I), num(V * I)))
    if k == "E":
        P, t, pr = R.choice([(2000, 2, 0.15), (100, 10, 0.2), (1500, 3, 0.15), (60, 5, 0.2), (2500, 1, 0.12)])
        E = P / 1000 * t
        return nq("Un aparato de %s W funciona %s h. Si el kWh cuesta %s €, ¿cuánto cuesta?" % (num(P), num(t), num(pr)), E * pr, [P * t * pr, E, E / pr], "€",
                  "E = %s kW · %s h = %s kWh; coste = %s · %s = %s €." % (num(P / 1000), num(t), num(E), num(E), num(pr), num(E * pr)))
    if k == "serie":
        a, b = R.choice([(4, 6), (10, 20), (3, 9), (12, 12), (5, 15)])
        if R.random() < 0.5:
            return nq("Dos resistencias de %s Ω y %s Ω están en serie. ¿Cuál es la resistencia equivalente?" % (a, b), a + b, [a * b / (a + b), a * b, abs(a - b)], "Ω", "En serie se suman: %s + %s = %s Ω." % (a, b, a + b))
        return nq("Dos resistencias de %s Ω y %s Ω están en paralelo. ¿Cuál es la resistencia equivalente?" % (a, b), a * b / (a + b), [a + b, a * b, abs(a - b) + 1], "Ω",
                  "En paralelo: R = (%s · %s) : (%s + %s) = %s Ω." % (a, b, a, b, num(a * b / (a + b))))
    I, t = R.choice([(2, 10), (0.5, 60), (3, 20), (0.1, 100), (1.5, 40)])
    return nq("Por un cable pasa una corriente de %s A durante %s s. ¿Qué carga ha circulado?" % (num(I), t), I * t, [I / t, t / I, I + t], "C", "Q = I · t = %s · %s = %s C." % (num(I), t, num(I * t)))


def f_kcal(R):
    k = R.choice(["e", "e", "imc", "pct"])
    if k == "e":
        g, p, h = R.choice([(10, 5, 30), (20, 10, 50), (5, 25, 10), (15, 8, 60), (2, 20, 40), (30, 15, 20), (1, 3, 25), (8, 12, 45), (25, 6, 15), (12, 18, 0)])
        e = 9 * g + 4 * p + 4 * h
        return nq("Un alimento tiene %s g de grasas, %s g de proteínas y %s g de hidratos de carbono. ¿Cuántas kcal aporta? (grasas 9 kcal/g; proteínas e hidratos 4 kcal/g)" % (g, p, h), e,
                  [4 * (g + p + h), 9 * (g + p + h), g + p + h], "kcal", "9 · %s + 4 · %s + 4 · %s = %s kcal." % (g, p, h, e))
    if k == "imc":
        m, h = R.choice([(60, 1.6), (72, 1.8), (45, 1.5), (81, 1.8), (50, 1.6), (64, 1.6), (70, 1.75), (55, 1.65), (90, 1.9)])
        return nq("Calcula el índice de masa corporal de una persona de %s kg y %s m. (IMC = masa : altura²)" % (m, num(h)), m / (h * h), [m / h, m * h * h, m / (2 * h)], "kg/m²",
                  "IMC = %s : %s² = %s kg/m²." % (m, num(h), num(m / (h * h))))
    tot, part = R.choice([(2000, 1100), (2400, 720), (1800, 540), (2500, 1250), (2000, 600)])
    return nq("Una dieta tiene %s kcal y %s kcal proceden de los hidratos de carbono. ¿Qué porcentaje es?" % (num(tot), num(part)), part / tot * 100, [tot / part * 100, part / 100, (tot - part) / tot * 100], "%",
              "%s : %s · 100 = %s %%." % (num(part), num(tot), num(part / tot * 100)))


def UNITS(grade):
    return [
        H("B", "la-organizacion-del-cuerpo-humano", "La organización del cuerpo humano", "Organización del cuerpo",
          "Los alumnos describen los niveles de organización del cuerpo humano, la célula eucariota animal, los tipos de tejidos y los aparatos y sistemas que realizan las funciones de nutrición, relación y reproducción.",
          "niveles de organización, célula, orgánulos, tejido epitelial, conectivo, muscular, nervioso, óseo, sanguíneo, órgano, aparato, sistema, funciones vitales",
          "Células → tejidos → órganos → aparatos", "Cada tejido tiene células especializadas en una función.",
          ["El cuerpo humano se organiza en niveles: células, tejidos, órganos, aparatos o sistemas y organismo.",
           "Los tejidos principales son el epitelial (recubre), el conectivo (une y sostiene, como el óseo o el sanguíneo), el muscular (contrae) y el nervioso (transmite impulsos).",
           "Los aparatos digestivo, respiratorio, circulatorio y excretor realizan la nutrición; el sistema nervioso, el endocrino y el locomotor, la relación; el reproductor, la reproducción."],
          [("¿Qué tejido forma la piel y el interior del estómago?", ["Son capas que recubren.", "Sus células están muy unidas."], "El tejido epitelial.")],
          [("La sangre no es un tejido.", "Es un tejido conectivo líquido."), ("Las neuronas se dividen como las demás células.", "La mayoría de las neuronas apenas se dividen.")],
          [("¿Qué es la célula madre?", "Una célula no especializada que puede convertirse en otros tipos de células."), ("¿Qué diferencia un aparato de un sistema?", "Un aparato tiene órganos distintos; un sistema, órganos del mismo tejido.")],
          [("Tejidos", [("tejido epitelial", "recubre superficies y forma glándulas"), ("tejido muscular", "permite el movimiento al contraerse"), ("tejido nervioso", "recibe y transmite impulsos"),
                        ("tejido óseo", "forma los huesos, duro por las sales de calcio"), ("tejido sanguíneo", "transporta sustancias por el cuerpo"), ("tejido adiposo", "almacena grasa y aísla"),
                        ("tejido cartilaginoso", "forma el cartílago flexible de la oreja y las articulaciones")],
            "¿Qué función tiene el {k}?", D),
           ("Funciones de los aparatos", [("aparato digestivo", "nutrición"), ("aparato respiratorio", "nutrición"), ("aparato circulatorio", "nutrición"), ("aparato excretor", "nutrición"),
                                          ("sistema nervioso", "relación"), ("sistema endocrino", "relación"), ("aparato locomotor", "relación"), ("aparato reproductor", "reproducción")],
            "¿En qué función vital participa el {k}?", None, ["excreción de energía"]),
           ("Células especializadas", [("neurona", "transmitir impulsos nerviosos"), ("glóbulo rojo", "transportar oxígeno"), ("espermatozoide", "fecundar el óvulo"), ("célula muscular", "contraerse"),
                                       ("célula epitelial del intestino", "absorber nutrientes"), ("osteocito", "mantener el hueso"), ("adipocito", "almacenar grasa"), ("glóbulo blanco", "defender de infecciones")],
            "¿Para qué está especializada la célula: {k}?", "¿Qué célula está especializada en {v}?")],
          ["El cuerpo humano está formado por células.", "La sangre es un tejido conectivo.", "El tejido muscular permite el movimiento.", "El aparato reproductor realiza la reproducción.",
           "Las neuronas transmiten impulsos.", "Varios tejidos forman un órgano.", "El tejido óseo forma los huesos."],
          [("La sangre no es un tejido.", "Es un tejido conectivo."), ("El sistema nervioso realiza la nutrición.", "Realiza la relación."), ("Un órgano está formado por un solo tipo de célula.", "Tiene varios tejidos."),
           ("Los glóbulos rojos defienden de infecciones.", "Transportan oxígeno."), ("El tejido adiposo transmite impulsos.", "Almacena grasa.")],
          "la organización del cuerpo humano", "living-things-and-ecosystems"),

        H("B", "alimentacion-y-nutricion", "Alimentación y nutrición: nutrientes y dieta equilibrada", "Alimentación y nutrición",
          "Los alumnos distinguen alimentación y nutrición, clasifican los nutrientes y su función, calculan el aporte energético de los alimentos, interpretan etiquetas y analizan dietas y trastornos.",
          "alimento, nutriente, glúcidos, lípidos, proteínas, vitaminas, sales minerales, agua, fibra, kilocaloría, dieta equilibrada, dieta mediterránea, etiquetado, conservación de alimentos",
          "Grasas 9 kcal/g; proteínas e hidratos 4 kcal/g", "La dieta mediterránea es variada y rica en vegetales y aceite de oliva.",
          ["Alimentarse es tomar alimentos (voluntario). Nutrirse es el conjunto de procesos que llevan los nutrientes a las células (involuntario).",
           "Glúcidos y lípidos aportan energía; las proteínas construyen y reparan tejidos; vitaminas y sales minerales regulan; el agua es imprescindible.",
           "Un gramo de grasa aporta 9 kcal; un gramo de proteínas o de hidratos de carbono, 4 kcal. Las etiquetas indican la energía y los nutrientes por 100 g."],
          [("Un yogur tiene 3 g de grasa, 4 g de proteínas y 5 g de hidratos. ¿Energía?", ["9 · 3 + 4 · 4 + 4 · 5.", "27 + 16 + 20 = 63."], "63 kcal.")],
          [("Alimentación y nutrición son lo mismo.", "La alimentación es elegir y comer; la nutrición son los procesos internos."), ("Las grasas son siempre malas.", "Son necesarias; conviene que sean sobre todo insaturadas, como el aceite de oliva.")],
          [("¿Qué vitamina falta en el escorbuto?", "La vitamina C, presente en cítricos y verduras frescas."), ("¿Qué son los alimentos ultraprocesados?", "Productos industriales con mucho azúcar, sal o grasas añadidas.")],
          [("Nutrientes", [("glúcidos", "principal fuente de energía rápida"), ("lípidos", "reserva de energía y aislamiento"), ("proteínas", "construyen y reparan tejidos"), ("vitaminas", "regulan reacciones del organismo"),
                           ("sales minerales", "forman huesos y regulan funciones"), ("agua", "disolvente y medio de las reacciones"), ("fibra", "facilita el tránsito intestinal")],
            "¿Qué función tienen: {k}?", D),
           ("Alimentos ricos en", [("pan", "glúcidos"), ("arroz", "glúcidos"), ("patata", "glúcidos"), ("aceite de oliva", "lípidos"), ("mantequilla", "lípidos"), ("frutos secos", "lípidos"),
                                   ("huevo", "proteínas"), ("pescado", "proteínas"), ("lentejas", "proteínas"), ("naranja", "vitaminas"), ("leche", "sales minerales de calcio")],
            "¿En qué nutriente es rico: {k}?", None),
           ("Enfermedades", [("escorbuto", "falta de vitamina C"), ("anemia ferropénica", "falta de hierro"), ("raquitismo", "falta de vitamina D y calcio"), ("bocio", "falta de yodo"),
                             ("obesidad", "exceso de energía ingerida"), ("caries", "exceso de azúcares y mala higiene"), ("diabetes tipo 2", "relacionada con exceso de azúcar y sedentarismo")],
            "¿Con qué se relaciona: {k}?", "¿Qué trastorno se relaciona con {v}?")],
          ["Las grasas aportan 9 kcal por gramo.", "Las proteínas construyen tejidos.", "El escorbuto se debe a la falta de vitamina C.", "La fibra facilita el tránsito intestinal.", "El agua es un nutriente.",
           "La nutrición es involuntaria.", "La dieta mediterránea usa aceite de oliva."],
          [("Las grasas aportan 4 kcal por gramo.", "Aportan 9."), ("Alimentación y nutrición son lo mismo.", "Son distintas."), ("Las vitaminas dan mucha energía.", "Regulan, no dan energía."),
           ("El bocio se debe a la falta de hierro.", "Se debe a la falta de yodo."), ("Las lentejas son ricas en lípidos.", "Son ricas en proteínas e hidratos.")],
          "la alimentación y la nutrición", "living-things-and-ecosystems", calc=f_kcal),

        H("B", "aparatos-digestivo-y-respiratorio", "Los aparatos digestivo y respiratorio", "Digestivo y respiratorio",
          "Los alumnos describen los órganos de los aparatos digestivo y respiratorio, la digestión mecánica y química, la absorción, la ventilación pulmonar, el intercambio de gases y sus enfermedades.",
          "boca, faringe, esófago, estómago, intestino delgado, hígado, páncreas, enzimas, quimo, absorción, vellosidades, laringe, tráquea, bronquios, alvéolos, ventilación, inspiración, espiración",
          "La digestión rompe los alimentos en nutrientes", "En los alvéolos el oxígeno pasa a la sangre y el CO₂ sale.",
          ["La digestión mecánica tritura y mezcla; la química, con enzimas, rompe las moléculas en nutrientes sencillos. El intestino delgado absorbe los nutrientes por sus vellosidades.",
           "El hígado fabrica la bilis, que emulsiona las grasas; el páncreas vierte jugo pancreático al intestino.",
           "En la inspiración el diafragma baja y entra aire; en la espiración sube y sale. En los alvéolos se produce el intercambio de gases con la sangre."],
          [("¿Dónde se absorben la mayoría de los nutrientes?", ["En el estómago casi no hay absorción.", "Las vellosidades aumentan mucho la superficie."], "En el intestino delgado.")],
          [("La digestión termina en el estómago.", "Continúa en el intestino delgado."), ("Respiramos para tomar oxígeno y nada más.", "También eliminamos el CO₂ que producen las células.")],
          [("¿Por qué no hay que hablar con la boca llena?", "La epiglotis podría no cerrar la tráquea y nos atragantaríamos."), ("¿Qué daña el tabaco?", "Los bronquios y los alvéolos; causa bronquitis, enfisema y cáncer.")],
          [("Digestivo", [("boca", "mastica y empieza a digerir el almidón con la saliva"), ("esófago", "lleva el bolo al estómago con movimientos peristálticos"), ("estómago", "digiere proteínas con jugo gástrico ácido"),
                          ("intestino delgado", "termina la digestión y absorbe los nutrientes"), ("intestino grueso", "absorbe agua y forma las heces"), ("hígado", "produce la bilis"), ("páncreas", "produce jugo pancreático"),
                          ("vesícula biliar", "almacena la bilis")],
            "¿Qué función tiene: {k}?", D),
           ("Respiratorio", [("fosas nasales", "filtran, calientan y humedecen el aire"), ("laringe", "contiene las cuerdas vocales"), ("epiglotis", "cierra la tráquea al tragar"), ("tráquea", "tubo con anillos de cartílago"),
                             ("bronquiolos", "ramificaciones finas de los bronquios"), ("alvéolos", "intercambian gases con la sangre"), ("diafragma", "músculo que permite la ventilación"), ("pleura", "membrana que envuelve los pulmones")],
            "¿Qué es o qué hace: {k}?", D),
           ("Enfermedades", {"las enfermedades del aparato digestivo": ["gastritis", "úlcera", "hepatitis", "apendicitis", "gastroenteritis", "cirrosis"],
                             "las enfermedades del aparato respiratorio": ["asma", "bronquitis", "neumonía", "enfisema", "faringitis", "tuberculosis"]})],
          ["El intestino delgado absorbe los nutrientes.", "La bilis emulsiona las grasas.", "La epiglotis cierra la tráquea al tragar.", "En los alvéolos se intercambian gases.", "El diafragma baja en la inspiración.",
           "El estómago digiere proteínas.", "El tabaco daña los alvéolos."],
          [("La digestión termina en el estómago.", "Termina en el intestino delgado."), ("La bilis se fabrica en el páncreas.", "Se fabrica en el hígado."), ("El diafragma sube en la inspiración.", "Baja."),
           ("El asma es una enfermedad digestiva.", "Es respiratoria."), ("El intestino grueso absorbe la mayoría de los nutrientes.", "Lo hace el delgado.")],
          "la digestión y la respiración", "living-things-and-ecosystems"),

        H("B", "aparatos-circulatorio-y-excretor", "Los aparatos circulatorio y excretor", "Circulatorio y excretor",
          "Los alumnos describen la sangre, los vasos sanguíneos, el corazón, la circulación doble y completa, el sistema linfático, el aparato excretor y la formación de la orina, y cómo prevenir sus enfermedades.",
          "plasma, glóbulos rojos, glóbulos blancos, plaquetas, arterias, venas, capilares, aurículas, ventrículos, válvulas, circulación pulmonar y general, sistema linfático, riñón, nefrona, orina",
          "Circulación doble: pulmonar y general", "La nefrona filtra la sangre y forma la orina.",
          ["La sangre tiene plasma, glóbulos rojos (oxígeno), glóbulos blancos (defensa) y plaquetas (coagulación).",
           "El corazón tiene dos aurículas y dos ventrículos. La circulación pulmonar lleva la sangre a los pulmones; la general, al resto del cuerpo.",
           "Los riñones filtran la sangre en las nefronas y forman la orina, que baja por los uréteres a la vejiga y sale por la uretra."],
          [("¿Qué cavidad del corazón envía la sangre a todo el cuerpo?", ["La circulación general empieza en la arteria aorta.", "La aorta sale del ventrículo izquierdo."], "El ventrículo izquierdo.")],
          [("Las arterias siempre llevan sangre oxigenada.", "La arteria pulmonar lleva sangre pobre en oxígeno."), ("La orina se forma en la vejiga.", "Se forma en los riñones.")],
          [("¿Qué es la tensión arterial?", "La presión de la sangre contra las paredes de las arterias."), ("¿Cómo se cuida el corazón?", "Con ejercicio, dieta con poca sal y grasa saturada y sin tabaco.")],
          [("Sangre y vasos", [("plasma", "parte líquida de la sangre"), ("glóbulos rojos", "transportan oxígeno con la hemoglobina"), ("glóbulos blancos", "defienden contra los microbios"), ("plaquetas", "intervienen en la coagulación"),
                               ("arterias", "vasos de paredes gruesas que salen del corazón"), ("venas", "vasos con válvulas que vuelven al corazón"), ("capilares", "vasos finísimos donde se intercambian sustancias")],
            "¿Qué es o qué hace: {k}?", D),
           ("Corazón y circulación", [("aurícula derecha", "recibe la sangre de las venas cavas"), ("ventrículo derecho", "envía la sangre a los pulmones"), ("aurícula izquierda", "recibe la sangre de las venas pulmonares"),
                                      ("ventrículo izquierdo", "envía la sangre por la aorta"), ("arteria pulmonar", "lleva sangre pobre en oxígeno a los pulmones"), ("venas pulmonares", "traen sangre oxigenada al corazón"),
                                      ("aorta", "mayor arteria del cuerpo")],
            "¿Qué función tiene: {k}?", D),
           ("Excretor", [("riñón", "filtra la sangre"), ("nefrona", "unidad que forma la orina"), ("uréter", "lleva la orina a la vejiga"), ("vejiga urinaria", "almacena la orina"), ("uretra", "expulsa la orina al exterior"),
                         ("glándulas sudoríparas", "eliminan agua y sales con el sudor"), ("hígado", "transforma sustancias tóxicas y fabrica urea")],
            "¿Qué función tiene: {k}?", D)],
          ["El ventrículo izquierdo envía la sangre por la aorta.", "Las plaquetas intervienen en la coagulación.", "La circulación humana es doble.", "La nefrona forma la orina.", "Los capilares intercambian sustancias.",
           "La arteria pulmonar lleva sangre pobre en oxígeno.", "Las venas tienen válvulas."],
          [("Todas las arterias llevan sangre oxigenada.", "La pulmonar no."), ("La orina se forma en la vejiga.", "Se forma en los riñones."), ("Los glóbulos blancos transportan oxígeno.", "Los rojos lo transportan."),
           ("El corazón tiene tres cavidades.", "Tiene cuatro."), ("Las venas salen del corazón.", "Vuelven a él.")],
          "la circulación y la excreción", "living-things-and-ecosystems"),

        H("B", "sistema-nervioso-y-endocrino", "La relación: sistema nervioso, endocrino y sentidos", "Nervioso y endocrino",
          "Los alumnos describen los receptores sensoriales, la neurona y el impulso nervioso, el sistema nervioso central y periférico, los actos reflejos, las glándulas endocrinas y sus hormonas, y los efectos de las drogas.",
          "estímulo, receptor, neurona, sinapsis, encéfalo, cerebro, cerebelo, bulbo raquídeo, médula espinal, nervios, acto reflejo, hormona, hipófisis, tiroides, páncreas, insulina, drogas",
          "Nervioso: rápido. Endocrino: lento y duradero", "Las hormonas viajan por la sangre hasta sus órganos diana.",
          ["Los receptores captan estímulos y los nervios sensitivos los llevan al sistema nervioso central (encéfalo y médula), que elabora una respuesta.",
           "La neurona tiene dendritas, cuerpo y axón. Se comunica con otras en la sinapsis mediante neurotransmisores.",
           "Las glándulas endocrinas fabrican hormonas que van por la sangre: la insulina del páncreas baja el azúcar en sangre; la tiroxina regula el metabolismo."],
          [("Alguien no puede mantener el equilibrio tras un golpe. ¿Qué parte del encéfalo pudo dañarse?", ["El equilibrio y la coordinación dependen de una zona.", "Es el cerebelo."], "El cerebelo.")],
          [("Los actos reflejos los decide el cerebro.", "Los controla la médula espinal, sin intervención consciente."), ("Las hormonas actúan solo cerca de la glándula.", "Viajan por la sangre a todo el cuerpo.")],
          [("¿Qué hace el alcohol en el sistema nervioso?", "Lo deprime: disminuye los reflejos y la coordinación."), ("¿Qué es la diabetes tipo 1?", "Una enfermedad en la que el páncreas no fabrica suficiente insulina.")],
          [("Partes del sistema nervioso", [("cerebro", "controla los actos voluntarios, la memoria y el pensamiento"), ("cerebelo", "coordina los movimientos y el equilibrio"), ("bulbo raquídeo", "controla el latido y la respiración"),
                                            ("médula espinal", "controla los actos reflejos"), ("nervios sensitivos", "llevan información desde los receptores"), ("nervios motores", "llevan órdenes a los músculos"),
                                            ("sinapsis", "conexión entre dos neuronas")],
            "¿Qué función tiene: {k}?", D),
           ("Glándulas y hormonas", [("páncreas", "insulina"), ("tiroides", "tiroxina"), ("glándulas suprarrenales", "adrenalina"), ("ovarios", "estrógenos"), ("testículos", "testosterona"),
                                     ("hipófisis", "hormona del crecimiento"), ("glándula pineal", "melatonina")],
            "¿Qué hormona fabrica: {k}?", "¿Qué glándula fabrica: {v}?"),
           ("Receptores", [("conos y bastones de la retina", "luz"), ("caracol del oído interno", "sonido"), ("pituitaria amarilla de la nariz", "olores"), ("papilas gustativas", "sabores"),
                           ("corpúsculos de la piel", "tacto, presión y temperatura"), ("canales semicirculares", "equilibrio")],
            "¿Qué estímulo capta: {k}?", "¿Qué receptor capta: {v}?")],
          ["El cerebelo coordina el equilibrio.", "La insulina la fabrica el páncreas.", "Las hormonas viajan por la sangre.", "Los actos reflejos los controla la médula.", "La sinapsis conecta neuronas.",
           "El bulbo raquídeo controla el latido del corazón.", "El alcohol disminuye los reflejos."],
          [("Los actos reflejos los decide el cerebro.", "Los controla la médula."), ("La insulina la fabrica el tiroides.", "La fabrica el páncreas."), ("Las hormonas actúan muy rápido y poco tiempo.", "Son lentas y duraderas."),
           ("El cerebelo controla la respiración.", "La controla el bulbo raquídeo."), ("El caracol del oído capta la luz.", "Capta el sonido.")],
          "la función de relación", "living-things-and-ecosystems"),

        H("B", "la-reproduccion-humana", "La reproducción humana y la salud sexual", "Reproducción humana",
          "Los alumnos describen los aparatos reproductores, la gametogénesis, el ciclo menstrual, la fecundación, el embarazo y el parto, los métodos anticonceptivos y la prevención de infecciones de transmisión sexual.",
          "aparato reproductor, gametos, óvulo, espermatozoide, ciclo menstrual, ovulación, fecundación, embarazo, parto, métodos anticonceptivos, preservativo, infecciones de transmisión sexual, reproducción asistida",
          "La ovulación ocurre hacia la mitad del ciclo", "El preservativo es el único método que también protege de las infecciones de transmisión sexual.",
          ["Los ovarios producen óvulos y hormonas; los testículos, espermatozoides y testosterona.",
           "El ciclo menstrual dura unos 28 días: hacia el día 14 se libera un óvulo (ovulación). Si no hay fecundación, se produce la menstruación.",
           "La fecundación ocurre en las trompas de Falopio. El embrión se implanta en el útero y la gestación dura unas 40 semanas. El preservativo previene embarazos e ITS."],
          [("En un ciclo de 28 días, ¿cuándo suele producirse la ovulación?", ["La menstruación empieza el día 1.", "La ovulación ocurre hacia la mitad."], "Hacia el día 14.")],
          [("La píldora protege de las infecciones de transmisión sexual.", "Solo el preservativo protege de las ITS."), ("La fecundación ocurre en el útero.", "Ocurre en las trompas de Falopio.")],
          [("¿Qué es la reproducción asistida?", "Técnicas médicas, como la fecundación in vitro, para ayudar a tener hijos."), ("¿Qué son las ITS?", "Infecciones que se transmiten por contacto sexual, como el VIH o la sífilis.")],
          [("Órganos", [("ovarios", "producen óvulos y hormonas sexuales femeninas"), ("trompas de Falopio", "lugar donde ocurre la fecundación"), ("útero", "lugar donde se desarrolla el embrión"),
                        ("testículos", "producen espermatozoides y testosterona"), ("epidídimo", "donde maduran los espermatozoides"), ("próstata", "produce parte del líquido seminal"), ("placenta", "intercambia sustancias entre la madre y el feto")],
            "¿Qué función tiene: {k}?", D),
           ("Métodos anticonceptivos", [("preservativo", "barrera que también previene las ITS"), ("diafragma", "barrera que se coloca en el cuello del útero"), ("píldora", "método hormonal que impide la ovulación"),
                                        ("DIU", "dispositivo colocado en el útero"), ("vasectomía", "método quirúrgico masculino"), ("ligadura de trompas", "método quirúrgico femenino")],
            "¿Cómo es este método: {k}?", D),
           ("ITS", [("VIH", "virus"), ("virus del papiloma humano", "virus"), ("herpes genital", "virus"), ("hepatitis B", "virus"), ("sífilis", "bacteria"), ("gonorrea", "bacteria"), ("clamidia", "bacteria"),
                    ("tricomoniasis", "protozoo")],
            "¿Qué tipo de microorganismo causa: {k}?", None, ["hongo"])],
          ["La ovulación ocurre hacia la mitad del ciclo.", "La fecundación ocurre en las trompas de Falopio.", "El preservativo protege de las ITS.", "Los testículos producen testosterona.", "La gestación dura unas 40 semanas.",
           "El VIH es un virus.", "La placenta intercambia sustancias con el feto."],
          [("La píldora protege de las ITS.", "Solo el preservativo."), ("La fecundación ocurre en el útero.", "En las trompas."), ("La sífilis es un virus.", "Es una bacteria."), ("El ciclo menstrual dura una semana.", "Dura unos 28 días."),
           ("Los ovarios producen espermatozoides.", "Producen óvulos.")],
          "la reproducción humana", "living-things-and-ecosystems"),

        H("B", "salud-y-enfermedad", "Salud, enfermedad y sistema inmunitario", "Salud y enfermedad",
          "Los alumnos distinguen enfermedades infecciosas y no infecciosas, sus agentes y transmisión, describen las defensas del cuerpo, la inmunidad, las vacunas y los antibióticos, y valoran los trasplantes y los hábitos saludables.",
          "salud, enfermedad infecciosa, patógeno, contagio, barreras, respuesta inmunitaria, linfocitos, anticuerpos, antígeno, vacuna, suero, antibiótico, resistencias, donación, trasplantes",
          "Las vacunas preparan al sistema inmunitario", "Los antibióticos solo actúan contra bacterias; su mal uso crea resistencias.",
          ["Las enfermedades infecciosas las causan patógenos (bacterias, virus, hongos, protozoos) y se contagian. Las no infecciosas, como el cáncer o la diabetes, no.",
           "El cuerpo se defiende con barreras (piel, mucosas), con la respuesta inespecífica (inflamación, fagocitos) y con la específica (linfocitos y anticuerpos).",
           "Una vacuna introduce antígenos inofensivos para que el cuerpo fabrique memoria inmunitaria. Un suero aporta anticuerpos ya hechos."],
          [("¿Por qué no se toman antibióticos para el resfriado?", ["El resfriado lo causa un virus.", "Los antibióticos actúan contra bacterias."], "Porque no sirven y crean resistencias.")],
          [("Las vacunas curan enfermedades.", "Las previenen; los sueros y medicamentos tratan."), ("La fiebre es siempre mala.", "Es una defensa que dificulta la multiplicación de los microbios.")],
          [("¿Qué es la inmunidad de grupo?", "Cuando muchas personas están vacunadas, el patógeno circula poco y protege a quien no puede vacunarse."), ("¿España es líder en trasplantes?", "Sí: la Organización Nacional de Trasplantes es referencia mundial en donación.")],
          [("Agentes", [("tuberculosis", "bacteria"), ("tétanos", "bacteria"), ("salmonelosis", "bacteria"), ("gripe", "virus"), ("sarampión", "virus"), ("COVID-19", "virus"), ("pie de atleta", "hongo"),
                        ("candidiasis", "hongo"), ("malaria", "protozoo"), ("toxoplasmosis", "protozoo")],
            "¿Qué tipo de patógeno causa: {k}?", None),
           ("Defensas", [("piel", "barrera física externa"), ("lágrimas y saliva", "contienen lisozima que destruye bacterias"), ("fagocitos", "glóbulos blancos que engullen microbios"), ("linfocitos B", "fabrican anticuerpos"),
                         ("anticuerpos", "proteínas que se unen a los antígenos"), ("células de memoria", "recuerdan al patógeno para una respuesta rápida"), ("inflamación", "llegan más sangre y defensas a la zona")],
            "¿Qué papel tiene: {k}?", D),
           ("Infecciosa o no", {"las enfermedades infecciosas": ["gripe", "tuberculosis", "hepatitis", "sarampión", "varicela", "malaria"],
                                "las enfermedades no infecciosas": ["diabetes", "cáncer", "infarto", "alergia", "artrosis", "hipertensión"]})],
          ["Las vacunas previenen enfermedades.", "Los antibióticos actúan contra bacterias.", "Los linfocitos B fabrican anticuerpos.", "La piel es una barrera.", "La gripe es infecciosa.",
           "La diabetes no es contagiosa.", "El mal uso de antibióticos crea resistencias."],
          [("Los antibióticos curan la gripe.", "La gripe es vírica."), ("Las vacunas curan.", "Previenen."), ("El cáncer es contagioso.", "No es infeccioso."), ("Los anticuerpos son glóbulos rojos.", "Son proteínas."),
           ("La malaria la causa un virus.", "La causa un protozoo.")],
          "la salud y la enfermedad", "living-things-and-ecosystems"),

        H("B", "el-relieve-y-los-agentes-geologicos", "El relieve y los agentes geológicos externos", "Agentes geológicos",
          "Los alumnos describen la meteorización, la erosión, el transporte y la sedimentación, la acción de ríos, aguas subterráneas, glaciares, viento y mar, y las formas de relieve que originan, con ejemplos españoles.",
          "geodinámica externa, meteorización, erosión, transporte, sedimentación, torrente, río, meandro, delta, karst, glaciar, morrena, duna, acantilado, playa, riesgos geológicos",
          "Erosión, transporte y sedimentación modelan el relieve", "Los agentes geológicos externos funcionan con la energía del Sol y la gravedad.",
          ["La meteorización rompe o altera las rocas en el lugar. Los agentes geológicos (agua, hielo, viento, seres vivos) erosionan, transportan y sedimentan.",
           "Un río erosiona en su curso alto (valles en V), forma meandros en el curso medio y deposita sedimentos en la desembocadura, como el delta del Ebro.",
           "Las aguas subterráneas disuelven la caliza y crean paisajes kársticos con cuevas y estalactitas. Los glaciares forman valles en U; el viento, dunas; el mar, acantilados y playas."],
          [("¿Qué agente formó la Ciudad Encantada de Cuenca?", ["Es un paisaje en roca caliza.", "El agua disuelve la caliza."], "El agua, por disolución kárstica.")],
          [("La erosión solo la produce el agua.", "También el hielo, el viento y los seres vivos."), ("Las estalactitas crecen desde el suelo.", "Cuelgan del techo; las estalagmitas crecen desde el suelo.")],
          [("¿Qué es una morrena?", "Un depósito de rocas arrastradas por un glaciar."), ("¿Qué riesgos geológicos externos hay en España?", "Inundaciones, deslizamientos de laderas y avance de las dunas o erosión de la costa.")],
          [("Formas y agentes", [("valle en V", "río"), ("meandro", "río"), ("delta", "río"), ("valle en U", "glaciar"), ("morrena", "glaciar"), ("circo glaciar", "glaciar"), ("duna", "viento"),
                                 ("roca en forma de seta", "viento"), ("acantilado", "mar"), ("playa", "mar"), ("estalactita", "aguas subterráneas"), ("dolina", "aguas subterráneas")],
            "¿Qué agente geológico forma: {k}?", None),
           ("Procesos", [("meteorización", "rotura o alteración de la roca en su lugar"), ("erosión", "arranque de materiales por un agente"), ("transporte", "traslado de los materiales"),
                         ("sedimentación", "depósito de los materiales cuando el agente pierde energía"), ("gelifracción", "rotura por el hielo que se forma en las grietas"), ("disolución", "el agua disuelve rocas como la caliza"),
                         ("diagénesis", "los sedimentos se compactan y forman roca")],
            "¿Qué es: {k}?", D),
           ("Lugares de España", [("delta del Ebro", "sedimentación de un río"), ("Ciudad Encantada de Cuenca", "modelado kárstico"), ("cueva de Nerja", "modelado kárstico"), ("valle de Ordesa", "modelado glaciar"),
                                  ("dunas de Maspalomas", "acción del viento"), ("acantilados de Barbate", "erosión marina"), ("Torcal de Antequera", "modelado kárstico")],
            "¿Qué proceso explica el paisaje de: {k}?", None)],
          ["Los glaciares forman valles en U.", "El viento forma dunas.", "El agua disuelve la caliza.", "Los ríos forman deltas en la desembocadura.", "La meteorización rompe la roca en su lugar.",
           "Las estalactitas cuelgan del techo de las cuevas.", "El mar forma acantilados."],
          [("Los ríos forman valles en U.", "Forman valles en V."), ("Las estalactitas crecen desde el suelo.", "Cuelgan del techo."), ("El viento forma morrenas.", "Las forman los glaciares."),
           ("La erosión solo la produce el agua.", "También el hielo y el viento."), ("La sedimentación ocurre cuando el agente gana energía.", "Ocurre cuando la pierde.")],
          "el relieve y los agentes geológicos", "earths-systems"),

        H("F", "el-atomo-y-la-tabla-periodica", "El átomo y la tabla periódica", "El átomo",
          "Los alumnos describen los modelos atómicos (Dalton, Thomson, Rutherford, Bohr), las partículas subatómicas, el número atómico y másico, los isótopos, los iones y la organización de la tabla periódica.",
          "átomo, protón, neutrón, electrón, número atómico Z, número másico A, isótopo, ion, catión, anión, modelos atómicos, tabla periódica, grupos, periodos, metales, no metales, gases nobles",
          "Z = protones; A = protones + neutrones", "Los isótopos tienen el mismo Z y distinto número de neutrones.",
          ["El átomo tiene un núcleo con protones (+) y neutrones (sin carga), y una corteza con electrones (−).",
           "El número atómico Z es el número de protones; el número másico A es la suma de protones y neutrones. Si un átomo gana electrones es un anión; si los pierde, un catión.",
           "La tabla periódica ordena los elementos por Z en periodos (filas) y grupos (columnas). Los del mismo grupo tienen propiedades parecidas."],
          [("El carbono-14 tiene Z = 6. ¿Cuántos neutrones tiene?", ["A = 14.", "N = A − Z = 14 − 6."], "8 neutrones.")],
          [("Los isótopos son elementos distintos.", "Son el mismo elemento con distinto número de neutrones."), ("Un ion positivo ha ganado protones.", "Ha perdido electrones; los protones no cambian.")],
          [("¿Qué descubrió Rutherford?", "Que el átomo tiene un núcleo pequeño y denso con carga positiva."), ("¿Por qué los gases nobles casi no reaccionan?", "Tienen su capa externa de electrones completa.")],
          [("Modelos atómicos", [("Dalton", "átomos indivisibles como esferas macizas"), ("Thomson", "esfera positiva con electrones incrustados"), ("Rutherford", "núcleo pequeño y positivo con electrones alrededor"),
                                 ("Bohr", "electrones en órbitas de energía fija"), ("modelo actual", "electrones en orbitales de probabilidad")],
            "¿Cómo era el modelo de {k}?", D, ["átomo con forma de cubo"]),
           ("Elementos", [("H", "hidrógeno"), ("He", "helio"), ("C", "carbono"), ("N", "nitrógeno"), ("O", "oxígeno"), ("Na", "sodio"), ("K", "potasio"), ("Fe", "hierro"), ("Cu", "cobre"), ("Ag", "plata"),
                          ("Au", "oro"), ("Hg", "mercurio"), ("Pb", "plomo"), ("S", "azufre")],
            "¿Qué elemento tiene el símbolo {k}?", "¿Cuál es el símbolo químico de: {v}?"),
           ("Grupos", {"los metales alcalinos": ["litio", "sodio", "potasio", "rubidio", "cesio"], "los halógenos": ["flúor", "cloro", "bromo", "yodo", "astato"],
                       "los gases nobles": ["helio", "neón", "argón", "kriptón", "xenón"]})],
          ["El protón tiene carga positiva.", "Z es el número de protones.", "Los isótopos tienen distinto número de neutrones.", "Un anión ha ganado electrones.", "El sodio es un metal alcalino.",
           "Los gases nobles casi no reaccionan.", "Rutherford descubrió el núcleo."],
          [("El neutrón tiene carga negativa.", "No tiene carga."), ("Los isótopos tienen distinto Z.", "Tienen el mismo Z."), ("Un catión ha ganado electrones.", "Los ha perdido."), ("El símbolo del hierro es H.", "Es Fe."),
           ("El cloro es un gas noble.", "Es un halógeno.")],
          "el átomo", "matter", calc=f_atomo),

        H("F", "enlace-quimico-y-formulacion", "El enlace químico y la formulación inorgánica", "Enlace y formulación",
          "Los alumnos explican por qué se unen los átomos, distinguen enlace iónico, covalente y metálico y sus propiedades, y nombran y formulan óxidos, hidruros y compuestos binarios según la IUPAC.",
          "regla del octeto, enlace iónico, enlace covalente, enlace metálico, molécula, cristal, masa molecular, óxidos, hidruros, sales binarias, nomenclatura IUPAC, prefijos multiplicadores",
          "Los átomos se unen para ser más estables", "Iónico: metal y no metal. Covalente: no metales. Metálico: metales.",
          ["Los átomos se unen para completar su capa externa (regla del octeto).",
           "Enlace iónico: un metal cede electrones a un no metal (NaCl). Enlace covalente: no metales comparten electrones (H₂O). Enlace metálico: electrones compartidos por muchos átomos metálicos.",
           "Los compuestos binarios se nombran con prefijos: CO₂ es dióxido de carbono; Fe₂O₃, trióxido de dihierro u óxido de hierro(III)."],
          [("Nombra CO con prefijos.", ["Un carbono y un oxígeno.", "Mono-óxido de carbono."], "Monóxido de carbono.")],
          [("La sal es una molécula.", "Es un cristal iónico; no forma moléculas sueltas."), ("Los compuestos covalentes conducen la electricidad.", "En general no la conducen.")],
          [("¿Por qué los metales conducen la electricidad?", "Sus electrones se mueven libremente."), ("¿Por qué el agua es un líquido y no un gas?", "Sus moléculas se atraen mucho entre sí por enlaces de hidrógeno.")],
          [("Tipo de enlace", [("cloruro de sodio", "iónico"), ("óxido de magnesio", "iónico"), ("fluoruro de calcio", "iónico"), ("agua", "covalente"), ("dióxido de carbono", "covalente"), ("metano", "covalente"),
                               ("diamante", "covalente"), ("cobre", "metálico"), ("hierro", "metálico"), ("aluminio", "metálico")],
            "¿Qué enlace tiene: {k}?", None, ["nuclear"]),
           ("Fórmulas", [("CO₂", "dióxido de carbono"), ("CO", "monóxido de carbono"), ("H₂O", "agua"), ("NH₃", "amoniaco"), ("CH₄", "metano"), ("NaCl", "cloruro de sodio"), ("CaO", "óxido de calcio"),
                         ("Fe₂O₃", "trióxido de dihierro"), ("SO₃", "trióxido de azufre"), ("HCl", "cloruro de hidrógeno"), ("MgO", "óxido de magnesio")],
            "¿Cómo se nombra {k}?", "¿Cuál es la fórmula del {v}?"),
           ("Propiedades", {"las propiedades de los compuestos iónicos": ["sólidos con puntos de fusión altos", "conducen disueltos o fundidos", "frágiles", "solubles en agua a menudo", "forman cristales"],
                            "las propiedades de las sustancias covalentes moleculares": ["puntos de fusión bajos", "a menudo gases o líquidos", "no conducen la electricidad", "forman moléculas", "muchas no se disuelven en agua"],
                            "las propiedades de los metales": ["conducen calor y electricidad", "brillo metálico", "dúctiles y maleables", "sólidos salvo el mercurio", "electrones libres"]})],
          ["El NaCl tiene enlace iónico.", "El agua tiene enlace covalente.", "Los metales conducen la electricidad.", "CO₂ es dióxido de carbono.", "Los átomos se unen para ser más estables.",
           "Los compuestos iónicos tienen puntos de fusión altos.", "El enlace covalente comparte electrones."],
          [("La sal es una molécula.", "Es un cristal iónico."), ("El agua tiene enlace iónico.", "Es covalente."), ("CO es dióxido de carbono.", "Es monóxido."), ("Los iónicos conducen en estado sólido.", "Conducen disueltos o fundidos."),
           ("El cobre tiene enlace covalente.", "Es metálico.")],
          "el enlace químico", "matter"),

        H("F", "el-mol-y-las-reacciones-quimicas", "El mol y las reacciones químicas", "El mol",
          "Los alumnos usan la masa molecular y el mol, el número de Avogadro y la molaridad, ajustan ecuaciones químicas sencillas y aplican la conservación de la masa a cálculos estequiométricos.",
          "masa atómica, masa molecular, mol, número de Avogadro, masa molar, molaridad, ecuación química, ajuste, coeficientes estequiométricos, ley de Lavoisier",
          "n = m : M", "Un mol contiene 6,02 · 10²³ partículas.",
          ["Un mol es la cantidad de sustancia que contiene 6,02 · 10²³ partículas (número de Avogadro).",
           "La masa molar (M) es la masa de un mol en gramos: n = m : M. La molaridad es moles de soluto por litro de disolución.",
           "En una ecuación química ajustada hay los mismos átomos de cada elemento a cada lado: 2 H₂ + O₂ → 2 H₂O."],
          [("¿Cuántos moles son 36 g de agua (M = 18 g/mol)?", ["n = m : M.", "36 : 18 = 2."], "2 mol.")],
          [("En una reacción se conservan las moléculas.", "Se conservan los átomos y la masa; las moléculas cambian."), ("Para ajustar se cambian los subíndices.", "Solo se cambian los coeficientes delante de las fórmulas.")],
          [("¿Para qué sirve el mol?", "Para contar partículas pesando, porque son demasiado pequeñas para contarlas."), ("¿Qué significa 2 H₂O?", "Dos moléculas o dos moles de agua.")],
          [("Ecuaciones ajustadas", [("_ H₂ + O₂ → 2 H₂O", "2"), ("CH₄ + _ O₂ → CO₂ + 2 H₂O", "2"), ("N₂ + _ H₂ → 2 NH₃", "3"), ("2 Na + Cl₂ → _ NaCl", "2"), ("C + O₂ → _ CO₂", "1"),
                                     ("_ Mg + O₂ → 2 MgO", "2"), ("4 Fe + _ O₂ → 2 Fe₂O₃", "3"), ("C₃H₈ + _ O₂ → 3 CO₂ + 4 H₂O", "5")],
            "¿Qué coeficiente falta en «{k}»?", None, ["4", "6"]),
           ("Masas molares", [("H₂O", "18 g/mol"), ("CO₂", "44 g/mol"), ("O₂", "32 g/mol"), ("CH₄", "16 g/mol"), ("NH₃", "17 g/mol"), ("NaCl", "58,5 g/mol"), ("CaCO₃", "100 g/mol"), ("H₂SO₄", "98 g/mol")],
            "¿Cuál es la masa molar de {k}?", "¿Qué sustancia tiene una masa molar de {v}?"),
           ("Conceptos", [("mol", "cantidad con 6,02 · 10²³ partículas"), ("masa molar", "masa en gramos de un mol"), ("molaridad", "moles de soluto por litro de disolución"), ("reactivo limitante", "el que se acaba primero"),
                          ("coeficiente estequiométrico", "número delante de una fórmula en la ecuación"), ("número de Avogadro", "6,02 · 10²³")],
            "¿Qué es: {k}?", D)],
          ["Un mol tiene 6,02 · 10²³ partículas.", "La masa molar del agua es 18 g/mol.", "En una reacción se conservan los átomos.", "Para ajustar se cambian los coeficientes.", "n = m : M.",
           "La molaridad se mide en mol/L.", "El reactivo limitante se acaba primero."],
          [("Para ajustar se cambian los subíndices.", "Se cambian los coeficientes."), ("En una reacción se conservan las moléculas.", "Se conservan los átomos."), ("Un mol de agua pesa 1 g.", "Pesa 18 g."),
           ("La molaridad son gramos por litro.", "Son moles por litro."), ("La masa disminuye en las reacciones.", "Se conserva.")],
          "el mol y las reacciones", "matter", calc=f_mol),

        H("F", "la-electricidad", "La electricidad: carga, corriente y circuitos", "La electricidad",
          "Los alumnos describen la carga eléctrica y la electrización, la ley de Ohm, los circuitos en serie y paralelo, la potencia y la energía eléctrica, el consumo doméstico y las centrales eléctricas.",
          "carga eléctrica, culombio, electrización, ley de Coulomb, intensidad, amperio, voltaje, voltio, resistencia, ohmio, ley de Ohm, serie, paralelo, potencia, kWh, centrales, seguridad",
          "Ley de Ohm: V = I · R", "La potencia es P = V · I y la energía consumida, E = P · t.",
          ["Las cargas del mismo signo se repelen y las de distinto signo se atraen. Un cuerpo se electriza al ganar o perder electrones.",
           "La intensidad (A) es la carga que pasa por segundo; el voltaje (V) es la energía por unidad de carga; la resistencia (Ω) se opone al paso de la corriente. Ley de Ohm: V = I · R.",
           "La potencia de un aparato es P = V · I. La factura se paga en kWh: E = P · t."],
          [("Una plancha de 2000 W funciona 1,5 h. ¿Cuánta energía gasta?", ["E = P · t = 2 kW · 1,5 h.", "= 3 kWh."], "3 kWh.")],
          [("La corriente se gasta en la bombilla.", "La intensidad es la misma antes y después; se transforma la energía."), ("En paralelo la resistencia total aumenta.", "En paralelo disminuye.")],
          [("¿Para qué sirve el diferencial?", "Corta la corriente si hay una fuga, para evitar electrocuciones."), ("¿Qué es un cortocircuito?", "Una conexión de muy baja resistencia que hace circular una corriente enorme.")],
          [("Magnitudes", [("carga eléctrica", "culombio"), ("intensidad", "amperio"), ("voltaje", "voltio"), ("resistencia", "ohmio"), ("potencia", "vatio"), ("energía", "julio o kWh")],
            "¿En qué unidad se mide: {k}?", "¿Qué magnitud se mide en {v}?", ["newton", "kelvin"]),
           ("Instrumentos y componentes", [("amperímetro", "mide la intensidad en serie"), ("voltímetro", "mide el voltaje en paralelo"), ("óhmetro", "mide la resistencia"), ("fusible", "se funde si la corriente es excesiva"),
                                           ("interruptor diferencial", "corta la corriente si hay fugas"), ("pila", "generador de corriente continua"), ("resistencia", "se opone al paso de la corriente")],
            "¿Qué hace: {k}?", D),
           ("Centrales", [("central hidroeléctrica", "energía potencial del agua"), ("central térmica de ciclo combinado", "combustión de gas natural"), ("central nuclear", "fisión del uranio"),
                          ("parque eólico", "energía cinética del viento"), ("central solar fotovoltaica", "luz del Sol en paneles"), ("central termosolar", "calor del Sol concentrado con espejos")],
            "¿Qué energía aprovecha: {k}?", "¿Qué central aprovecha {v}?")],
          ["Las cargas iguales se repelen.", "V = I · R.", "El amperímetro se conecta en serie.", "En paralelo la resistencia equivalente disminuye.", "La factura eléctrica se mide en kWh.",
           "El diferencial protege de fugas.", "La resistencia se mide en ohmios."],
          [("Las cargas iguales se atraen.", "Se repelen."), ("El voltímetro se conecta en serie.", "En paralelo."), ("La corriente se gasta en la bombilla.", "Se transforma la energía."), ("La intensidad se mide en voltios.", "En amperios."),
           ("En paralelo la resistencia aumenta.", "Disminuye.")],
          "la electricidad", "energy", calc=f_elec),
    ]
