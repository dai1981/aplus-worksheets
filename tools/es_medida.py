# -*- coding: utf-8 -*-
"""España 4.º de Primaria: partes comunes para medidas (longitud, masa, capacidad)."""
from es_common import mcq, num, dz

LON = ["km", "hm", "dam", "m", "dm", "cm", "mm"]
MAS = ["kg", "hg", "dag", "g", "dg", "cg", "mg"]
CAP = ["kL", "hL", "daL", "L", "dL", "cL", "mL"]
NOMBRE = {"km": "kilómetro", "hm": "hectómetro", "dam": "decámetro", "m": "metro", "dm": "decímetro", "cm": "centímetro", "mm": "milímetro",
          "kg": "kilogramo", "hg": "hectogramo", "dag": "decagramo", "g": "gramo", "dg": "decigramo", "cg": "centigramo", "mg": "miligramo",
          "kL": "kilolitro", "hL": "hectolitro", "daL": "decalitro", "L": "litro", "dL": "decilitro", "cL": "centilitro", "mL": "mililitro"}


def conv(R, units, pairs, big=False):
    """pregunta de cambio de unidad entre dos unidades de la escala (resultado entero)"""
    a, b = R.choice(pairs)
    i, j = units.index(a), units.index(b)
    f = 10 ** abs(i - j)
    if i < j:     # de grande a pequeña: multiplicar
        v = R.randint(2, 99) if f >= 100 else R.randint(2, 999)
        r = v * f
        how = "multiplicamos por %s" % num(f)
    else:
        r = R.randint(2, 99) if f >= 100 else R.randint(2, 999)
        v = r * f
        how = "dividimos entre %s" % num(f)
    ws = [r * 10, r // 10 if r >= 10 and r % 10 == 0 else r * 100, r * 100 if r * 100 != r * 10 else r + 1, v]
    return mcq("¿Cuántos %s son %s %s?" % (b, num(v), a), "%s %s" % (num(r), b), ["%s %s" % (num(w), b) for w in ws if w != r],
               "De %s a %s %s: %s %s = <b>%s %s</b>." % (a, b, how, num(v), a, num(r), b))


def compound(R, units, big, small, f):
    """3 m 25 cm = ? cm"""
    a = R.randint(1, 9)
    b = R.randint(1, f - 1)
    t = a * f + b
    return mcq("¿Cuántos %s son %d %s y %d %s?" % (small, a, big, b, small), "%s %s" % (num(t), small),
               ["%s %s" % (num(a * 10 + b) if a * 10 + b != t else num(t + f), small), "%s %s" % (num(a + b), small), "%s %s" % (num(a * f * 10 + b), small), "%s %s" % (num(t + f), small)],
               "%d %s = %s %s; %s + %d = <b>%s %s</b>." % (a, big, num(a * f), small, num(a * f), b, num(t), small))


def comparar(R, units, pairs):
    a, b = R.choice(pairs)
    i, j = units.index(a), units.index(b)
    f = 10 ** abs(i - j)
    x = R.randint(2, 30)
    y = x * f + R.choice([-f // 2 if f > 1 else -1, f // 2 if f > 1 else 1, 0, 1, -1]) if i < j else None
    if y is None or y <= 0:
        return None
    A, B = "%s %s" % (num(x), a), "%s %s" % (num(y), b)
    vx = x * f
    ok = "%s %s %s" % (A, "&gt;" if vx > y else "&lt;" if vx < y else "=", B)
    opts = ["%s %s %s" % (A, s, B) for s in ("&gt;", "&lt;", "=") if s != ok.split(" ")[2]]
    return mcq("Compara %s y %s. ¿Qué es correcto?" % (A, B), ok, opts + ["no se pueden comparar"],
               "%s = %s %s: <b>%s</b>." % (A, num(vx), b, ok))
