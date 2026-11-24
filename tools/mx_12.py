# -*- coding: utf-8 -*-
"""
México 1.er y 2.º grado de primaria (Fase 3) の共通部品。
・BIG: src の mx_ に渡す（ES の 1.º・2.º は数の範囲が決まっているので、lim の数え方で落とさない）
・std_units: cm・m・kg・L などの標準単位を落とす（Fase 3 は任意単位で測る）
・q_le(n): 問題文の数が n 以下のものだけ
・calendario_svg・s_calendario・s_ayer: カレンダーと「昨日・今日・明日」
・s_iguales: 同じ数のたし算とかけ算（1.º）
"""
import re
import random
from mx_common import mcq, fig, svg_wrap, NB
from ws_common import text

BIG = 10 ** 30
DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"]
CORTO = ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
LARGO = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def plain(it):
    return re.sub(r"<[^>]*>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])


def std_units(it):
    """True si no usa unidades convencionales (cm, metro, kg, litro…)"""
    return not re.search(r"\d\s?(cm|mm|m|km|kg|g|L|mL|ml|l)\b|metro|kilo|gramo|litro|regla", plain(it))


def q_le(n):
    def ok(it):
        t = re.sub(r"<svg.*?</svg>", " ", it["q"])
        t = re.sub(r"<[^>]*>", " ", t)
        return all(int(x) <= n for x in re.findall(r"\d+", t.replace(NB, "")))
    return ok


def all_le(n):
    """todos los números de la pregunta, las opciones y la explicación (sin dibujos) ≤ n"""
    def ok(it):
        t = re.sub(r"<svg.*?</svg>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
        t = re.sub(r"<[^>]*>", " ", t).replace(NB, "")
        return all(int(x) <= n for x in re.findall(r"\d+", t))
    return ok


def calendario_svg(mes, inicio, marks=()):
    """mes: índice 0–11; inicio: día de la semana del día 1 (0 = domingo); marks: días con círculo"""
    W, cw, ch, top = 7 * 46 + 8, 46, 34, 52
    n = LARGO[mes]
    rows = (inicio + n + 6) // 7
    s = ["<rect x='4' y='4' width='%d' height='28' rx='4' fill='#1d6b3a'/>" % (W - 8), text(W // 2, 23, MESES[mes].capitalize(), 15, col="#ffffff")]
    for i, d in enumerate(CORTO):
        s.append(text(4 + cw * i + cw // 2, top - 6, d, 12, col="#c0392b" if i == 0 else "#333"))
    for d in range(1, n + 1):
        k = inicio + d - 1
        r, c = divmod(k, 7)
        x, y = 4 + cw * c, top + ch * r
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='#cfd8dc'/>" % (x, y, cw, ch))
        if d in marks:
            s.append("<circle cx='%d' cy='%d' r='13' fill='none' stroke='#c0392b' stroke-width='2.5'/>" % (x + cw // 2, y + ch // 2))
        s.append(text(x + cw // 2, y + ch // 2 + 5, str(d), 13, weight=400))
    H = top + ch * rows + 6
    svg = svg_wrap(W, H, "".join(s), "calendario de %s" % MESES[mes])
    return fig(svg.replace("<svg ", "<svg data-pf='lg' ", 1))


def s_calendario(R, lv):
    def mk():
        mes = R.randrange(12)
        ini = R.randrange(7)
        n = LARGO[mes]
        k = R.choice(["dia", "dia", "cuantos", "semana", "lunes"] + (["despues", "fecha"] if lv == 2 else []))
        if k == "dia":
            d = R.randint(1, n)
            w = (ini + d - 1) % 7
            return mcq(calendario_svg(mes, ini, [d]) + "¿Qué día de la semana es el %d de %s?" % (d, MESES[mes]), DIAS[w], [DIAS[(w + 1) % 7], DIAS[w - 1], DIAS[(w + 3) % 7]],
                       "Busca el %d y sube a la fila de arriba: es <b>%s</b>." % (d, DIAS[w]))
        if k == "cuantos":
            w = R.randrange(7)
            c = sum(1 for d in range(1, n + 1) if (ini + d - 1) % 7 == w)
            return mcq(calendario_svg(mes, ini) + "¿Cuántos %s tiene %s?" % (DIAS[w] if DIAS[w].endswith("s") else DIAS[w] + "s", MESES[mes]), str(c), [str(9 - c) if 9 - c != c else "3", "7", str(c + 1) if c < 5 else "6"],
                       "Cuenta los números de la columna «%s»: <b>%d</b>." % (CORTO[w], c))
        if k == "semana":
            d = R.randint(1, n - 7)
            w = (ini + d - 1) % 7
            return mcq(calendario_svg(mes, ini, [d]) + "Hoy es %s %d de %s. ¿Qué fecha será dentro de una semana?" % (DIAS[w], d, MESES[mes]), "el %d" % (d + 7),
                       ["el %d" % (d + 1), "el %d" % (d + 6), "el %d" % (d + 10 if d + 10 <= n else d - 1)], "Una semana son 7 días: %d + 7 = <b>%d</b>, otra vez %s." % (d, d + 7, DIAS[w]))
        if k == "lunes":
            w = R.choice([1, 2, 3, 4, 5])
            firsts = [d for d in range(1, n + 1) if (ini + d - 1) % 7 == w]
            i = R.randrange(len(firsts) - 1)
            nom = ["primer", "segundo", "tercer", "cuarto"][i] if i < 4 else None
            if not nom:
                return None
            d = firsts[i]
            return mcq(calendario_svg(mes, ini) + "¿En qué fecha cae el %s %s de %s?" % (nom, DIAS[w], MESES[mes]), "el %d" % d,
                       ["el %d" % x for x in (d + 7, d - 7 if d > 7 else d + 14, d + 1)], "En la columna «%s», el %s número es el <b>%d</b>." % (CORTO[w], nom, d))
        if k == "despues":
            d = R.randint(1, n - 3)
            a = R.randint(2, 3)
            w = (ini + d - 1) % 7
            return mcq(calendario_svg(mes, ini, [d]) + "Hoy es %d de %s. ¿Qué día de la semana será dentro de %d días?" % (d, MESES[mes], a), DIAS[(w + a) % 7],
                       [DIAS[(w + a + 1) % 7], DIAS[(w + a - 1) % 7], DIAS[w]], "%d + %d = %d: es <b>%s</b>." % (d, a, d + a, DIAS[(w + a) % 7]))
        if mes == 11:
            return None
        return mcq(calendario_svg(mes, ini) + "¿Qué día es el siguiente al último día de %s?" % MESES[mes], "el 1 de %s" % MESES[mes + 1],
                   ["el %d de %s" % (n + 1, MESES[mes]), "el 1 de %s" % MESES[mes], "el 2 de %s" % MESES[mes + 1]],
                   "%s tiene %d días; después empieza <b>%s</b>." % (MESES[mes].capitalize(), n, "el 1 de " + MESES[mes + 1]))
    mk.__name__ = "s_calendario"
    return mk


def s_ayer(R):
    def mk():
        i = R.randrange(7)
        k = R.choice(["ayer", "manana", "pasado", "antier"])
        if k == "ayer":
            return mcq("Hoy es %s. ¿Qué día fue ayer?" % DIAS[i], DIAS[i - 1], [DIAS[(i + 1) % 7], DIAS[i], DIAS[i - 2]], "Ayer es el día de antes: <b>%s</b>." % DIAS[i - 1])
        if k == "manana":
            return mcq("Hoy es %s. ¿Qué día será mañana?" % DIAS[i], DIAS[(i + 1) % 7], [DIAS[i - 1], DIAS[i], DIAS[(i + 2) % 7]], "Mañana es el día de después: <b>%s</b>." % DIAS[(i + 1) % 7])
        if k == "pasado":
            return mcq("Hoy es %s. ¿Qué día será pasado mañana?" % DIAS[i], DIAS[(i + 2) % 7], [DIAS[(i + 1) % 7], DIAS[i - 2], DIAS[(i + 3) % 7]],
                       "Pasado mañana son 2 días después: <b>%s</b>." % DIAS[(i + 2) % 7])
        return mcq("Hoy es %s. ¿Qué día fue antier (antes de ayer)?" % DIAS[i], DIAS[i - 2], [DIAS[i - 1], DIAS[(i + 2) % 7], DIAS[i - 3]],
                   "Antier son 2 días antes: <b>%s</b>." % DIAS[i - 2])
    mk.__name__ = "s_ayer"
    return mk


def s_iguales(R):
    """sumas de sumandos iguales y diferentes; multiplicación hasta 10"""
    def mk():
        k = R.choice(["cual", "cual", "escribe", "valor"])
        a, n = R.randint(2, 5), R.randint(2, 5)
        if a * n > 10 and k != "cual":
            return None
        suma = " + ".join([str(a)] * n)
        if k == "cual":
            if a * n > 10:
                return None
            cosa, cont = R.choice([("galletas", "platos"), ("flores", "macetas"), ("lápices", "estuches"), ("pelotas", "cajas"), ("dulces", "bolsas"), ("peces", "peceras")])
            cont = cont.replace("estuches", "vasos")
            cada = "cada uno" if cont in ("platos", "vasos") else "cada una"
            w = ["%d + %d" % (n, a), " + ".join([str(a)] * (n + 1)), " + ".join([str(a + 1)] * n)]
            return mcq("Hay %d %s con %d %s %s. ¿Qué suma da el total?" % (n, cont, a, cosa, cada), suma, w,
                       "Son %d veces el %d: <b>%s</b> = %d." % (n, a, suma, a * n))
        if k == "escribe":
            return mcq("¿Qué multiplicación es igual a %s?" % suma, "%d × %d" % (n, a), ["%d × %d" % (a + n, 1), "%d + %d" % (n, a), "%d × %d" % (n, a + 1)],
                       "Hay %d veces el %d: <b>%d × %d</b> = %d." % (n, a, n, a, n * a))
        return mcq("¿Cuánto es %d × %d?" % (n, a), str(n * a), [str(n + a), str(n * a + a), str(n * a - 1)], "%d × %d = %s = <b>%d</b>." % (n, a, suma, n * a))
    mk.__name__ = "s_iguales"
    return mk
