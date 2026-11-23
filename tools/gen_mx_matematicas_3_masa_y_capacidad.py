# -*- coding: utf-8 -*-
"""México 3.er grado: Medición de masa y capacidad (kg, g, L, mL; medios y cuartos). Reutiliza España 4.º con otra semilla."""
import re
import random
from mx_common import src, unit, mx_text, mcq, num


def units_ok(it):
    t = re.sub(r"<[^>]*>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
    return not re.search(r"\d\s?(hL|daL|dL|cL|hg|dag|dg|cg|mg)\b|hecto|deca|deci|centi", t)

import gen_es_matematicas_4_masa_y_capacidad as M4

leer, unid, prob = src("gen_es_matematicas_4_masa_y_capacidad", 63213, "s3_leer", "s4_unidad", "s5_problema", extra=(units_ok,))
R = random.Random(63313)


def masa():
    t = R.choice(["kgg", "kgg", "gkg", "mixto", "frac", "comp"])
    if t == "kgg":
        n = R.randint(2, 9)
        return mcq("¿Cuántos gramos son %d kg?" % n, "%s g" % num(n * 1000), ["%s g" % num(n * 100), "%s g" % num(n * 10), "%s g" % num(n * 10000)], "1 kg = 1 000 g, así que %d kg = <b>%s g</b>." % (n, num(n * 1000)))
    if t == "gkg":
        n = R.randint(2, 9)
        return mcq("¿Cuántos kilos son %s g?" % num(n * 1000), "%d kg" % n, ["%d kg" % (n * 10), "%d kg" % (n * 100), "%s kg" % num(n * 1000)], "Cada 1 000 g son 1 kg: <b>%d kg</b>." % n)
    if t == "mixto":
        a, b = R.randint(1, 5), R.choice([100, 200, 250, 300, 400, 500, 600, 750, 800])
        return mcq("¿Cuántos gramos son %d kg y %d g?" % (a, b), "%s g" % num(a * 1000 + b), ["%s g" % num(a * 100 + b), "%s g" % num(a + b), "%s g" % num(a * 1000 + b * 10)],
                   "%d kg = %s g; %s + %d = <b>%s g</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if t == "frac":
        nm, v = R.choice([("medio kilo", 500), ("un cuarto de kilo", 250), ("tres cuartos de kilo", 750), ("kilo y medio", 1500), ("dos kilos y medio", 2500), ("tres kilos y cuarto", 3250)])
        return mcq("¿Cuántos gramos son %s?" % nm, "%s g" % num(v), ["%s g" % num(w) for w in (50, 200, 400, 1250, 2050, 150, 5000, 3025) if w != v][R.randint(0, 3):][:3] + ["%s g" % num(v * 2)],
                   "1 kg = 1 000 g; %s = <b>%s g</b>." % (nm, num(v)))
    a = R.randint(1, 4)
    b = R.choice([600, 800, 900, 1200, 1500, 2500, 3500])
    if a * 1000 == b:
        return None
    ok = "%d kg" % a if a * 1000 > b else "%s g" % num(b)
    return mcq("¿Qué pesa más: %d kg de frijol o %s g de arroz?" % (a, num(b)), ok, ["%s g" % num(b) if ok.endswith("kg") else "%d kg" % a, "pesan lo mismo", "no se puede saber"],
               "%d kg = %s g, y %s g %s %s g: <b>%s</b>." % (a, num(a * 1000), num(a * 1000), "&gt;" if a * 1000 > b else "&lt;", num(b), ok))


def cap():
    t = R.choice(["Lml", "Lml", "mlL", "mixto", "frac", "comp"])
    if t == "Lml":
        n = R.randint(2, 9)
        return mcq("¿Cuántos mililitros son %d L?" % n, "%s mL" % num(n * 1000), ["%s mL" % num(n * 100), "%s mL" % num(n * 10), "%s mL" % num(n * 10000)], "1 L = 1 000 mL, así que %d L = <b>%s mL</b>." % (n, num(n * 1000)))
    if t == "mlL":
        n = R.randint(2, 9)
        return mcq("¿Cuántos litros son %s mL?" % num(n * 1000), "%d L" % n, ["%d L" % (n * 10), "%d L" % (n * 100), "%s L" % num(n * 1000)], "Cada 1 000 mL son 1 L: <b>%d L</b>." % n)
    if t == "mixto":
        a, b = R.randint(1, 5), R.choice([100, 200, 250, 300, 400, 500, 600, 750, 800])
        return mcq("¿Cuántos mililitros son %d L y %d mL?" % (a, b), "%s mL" % num(a * 1000 + b), ["%s mL" % num(a * 100 + b), "%s mL" % num(a + b), "%s mL" % num(a * 1000 + b * 10)],
                   "%d L = %s mL; %s + %d = <b>%s mL</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if t == "frac":
        k, nm, v = R.choice([(1, "medio litro", 500), (2, "un cuarto de litro", 250), (3, "tres cuartos de litro", 750), (4, "litro y medio", 1500), (5, "dos litros y medio", 2500)])
        return mcq("¿Cuántos mililitros son %s?" % nm, "%s mL" % num(v), ["%s mL" % num(w) for w in (50, 200, 400, 1250, 2050, 150, 5000) if w != v][R.randint(0, 3):][:3] + ["%s mL" % num(v * 2)],
                   "1 L = 1 000 mL; %s = <b>%s mL</b>." % (nm, num(v)))
    a = R.randint(1, 4)
    b = R.choice([600, 800, 900, 1200, 1500, 2500, 3500])
    if a * 1000 == b:
        return None
    ok = "%d L" % a if a * 1000 > b else "%s mL" % num(b)
    return mcq("¿Qué es más: %d L o %s mL?" % (a, num(b)), ok, ["%s mL" % num(b) if ok.endswith(" L") else "%d L" % a, "son iguales", "no se puede saber"],
               "%d L = %s mL, y %s mL %s %s mL: <b>%s</b>." % (a, num(a * 1000), num(a * 1000), "&gt;" if a * 1000 > b else "&lt;", num(b), ok))

unit("masa-y-capacidad", 13, "L",
     "Mide, estima y compara masas con el kilogramo, el medio kilo y el cuarto de kilo, y capacidades con el litro, el medio litro y el cuarto de litro; resuelve problemas de su contexto",
     "Masa y capacidad", "Masa y capacidad",
     "Ejercicios de matemáticas de 3.er grado de primaria: kilos y gramos, litros y mililitros, medio y cuarto, leer básculas y jarras y problemas. 100 ejercicios con respuestas.",
     "1 kg = 1 000 g; 1 L = 1 000 mL", "Medio kilo son 500 g.",
     ["La <b>masa</b> se mide en kilogramos (kg) y gramos (g): 1 kg = 1 000 g.", "La <b>capacidad</b> se mide en litros (L) y mililitros (mL): 1 L = 1 000 mL.",
      "Medio kilo = 500 g y un cuarto de kilo = 250 g. Medio litro = 500 mL y un cuarto de litro = 250 mL."],
     [("2 kg 300 g en gramos", ["2 kg = 2 000 g", "2 000 + 300"], "2 300 g"), ("¿Cuántos vasos de 250 mL llenan 1 L?", ["1 000 ÷ 250"], "4 vasos")],
     [["Pensar que 1 kg = 100 g", "Son 1 000 g."], ["Leer mal la báscula", "Mira cuánto vale cada rayita."], ["Comparar sin pasar a la misma unidad", "1 L y 800 mL: 1 000 mL &gt; 800 mL."]],
     [("¿Cuántos gramos tiene un kilo?", "Un kilogramo tiene 1 000 gramos. Medio kilo son 500 g."), ("¿Cuántos mililitros tiene un litro?", "Un litro tiene 1 000 mililitros. Medio litro son 500 mL.")],
     [("Kilos y gramos", [(masa, 20)]), ("Litros y mililitros", [(cap, 20)]), ("Básculas y jarras", [(leer, 20)]), ("Elegir la unidad", [(unid, 8), (masa, 6), (cap, 6)]), ("Problemas", [(prob, 20)])],
     63013, pic=mx_text(M4.bascula(1500)))
