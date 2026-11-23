# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Medidas de longitud (Sentido de la medida)
El metro, sus múltiplos (km, hm, dam) y submúltiplos (dm, cm, mm); pasar de una unidad a otra; expresiones complejas
(2 m 35 cm); comparar longitudes; elegir la unidad adecuada; medir con la regla; estimar; problemas.
Errores: multiplicar cuando hay que dividir, olvidar que de una unidad a la siguiente se multiplica por 10.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, dz, bank, Kids
import es_medida as M
import fr_common as _F

R = random.Random(44014)
K = Kids(R)

PAIRS = [("km", "m"), ("m", "cm"), ("m", "dm"), ("dm", "cm"), ("cm", "mm"), ("m", "mm"), ("km", "hm"), ("hm", "m"), ("dam", "m"), ("dm", "mm")]
PAIRS_UP = [(b, a) for a, b in PAIRS]


def s1_unidades():
    k = R.choice(["eq", "eq", "orden", "nombre"])
    if k == "eq":
        a, b = R.choice(PAIRS)
        f = 10 ** (M.LON.index(b) - M.LON.index(a))
        return mcq("¿Cuántos %s hay en 1 %s?" % (b, a), num(f), [num(f * 10), num(f // 10) if f >= 100 else "1", num(f * 100) if f < 1000 else "100"], "1 %s = <b>%s %s</b>." % (a, num(f), b))
    if k == "orden":
        xs = R.sample(M.LON, 4)
        ok = " &gt; ".join(sorted(xs, key=M.LON.index))
        sh = list(xs)
        w = [" &gt; ".join(sorted(xs, key=M.LON.index)[::-1]), " &gt; ".join(sh) if " &gt; ".join(sh) != ok else None]
        s2 = sorted(xs, key=M.LON.index)
        s2[1], s2[2] = s2[2], s2[1]
        w.append(" &gt; ".join(s2))
        s3 = sorted(xs, key=M.LON.index)
        s3[0], s3[1] = s3[1], s3[0]
        w.append(" &gt; ".join(s3))
        return mcq("Ordena de mayor a menor estas unidades: %s" % ", ".join(xs), ok, w, "km &gt; hm &gt; dam &gt; m &gt; dm &gt; cm &gt; mm: <b>%s</b>." % ok)
    u = R.choice(M.LON)
    return mcq("¿Qué abreviatura tiene el %s?" % M.NOMBRE[u], u, [x for x in M.LON if x != u], "%s = <b>%s</b>." % (M.NOMBRE[u], u))


def s1_adecuada():
    return bank(R, [
        ("¿Qué unidad usarías para medir la distancia entre Madrid y Sevilla?", "kilómetro", ["metro", "centímetro", "milímetro"]),
        ("¿Qué unidad usarías para medir el largo de una hormiga?", "milímetro", ["kilómetro", "metro", "decámetro"]),
        ("¿Qué unidad usarías para medir el largo de un lápiz?", "centímetro", ["kilómetro", "hectómetro", "metro"]),
        ("¿Qué unidad usarías para medir el largo de una piscina?", "metro", ["milímetro", "kilómetro", "centímetro"]),
        ("¿Cuánto puede medir de alto la puerta de clase?", "2 m", ["2 cm", "2 km", "20 m"]),
        ("¿Cuánto puede medir un bolígrafo?", "14 cm", ["14 m", "14 mm", "14 km"]),
        ("¿Cuánto puede medir un campo de fútbol de largo?", "100 m", ["100 cm", "100 km", "10 mm"]),
        ("¿Cuánto mide aproximadamente un paso de un adulto?", "70 cm", ["70 mm", "70 m", "7 km"]),
        ("¿Cuánto puede medir de alto un niño de 4.º de Primaria?", "1,35 m", ["13,5 m", "1,35 cm", "135 m"]),
        ("¿Qué distancia hay, más o menos, en coche de Valencia a Barcelona?", "unos 350 km", ["unos 35 km", "unos 3500 km", "unos 350 m"]),
    ], "adecuada")()


def regla(cm, mm):
    """regla en cm con un lápiz de cm,mm"""
    W = 30 + 32 * 12
    s = []
    s.append("<rect x='10' y='40' width='%d' height='38' fill='#fff4d6' stroke='#333' stroke-width='1.5'/>" % (32 * 12 + 20))
    for i in range(0, 121):
        x = 20 + i * 3.2
        h = 14 if i % 10 == 0 else 9 if i % 5 == 0 else 5
        s.append("<line x1='%.1f' y1='40' x2='%.1f' y2='%d' stroke='#333' stroke-width='1'/>" % (x, x, 40 + h))
        if i % 10 == 0:
            s.append("<text x='%.1f' y='72' font-size='11' text-anchor='middle' fill='#333'>%d</text>" % (x, i // 10))
    L = (cm * 10 + mm) * 3.2
    s.append("<rect x='20' y='14' width='%.1f' height='16' rx='3' fill='#f2c14e' stroke='#333'/>" % (L - 12))
    s.append("<polygon points='%.1f,14 %.1f,22 %.1f,30' fill='#e8d5b0' stroke='#333'/>" % (20 + L - 12, 20 + L, 20 + L - 12))
    s.append("<text x='%d' y='92' font-size='11' fill='#333'>cm</text>" % (W - 10))
    return "<div class='fig'><svg viewBox='0 0 %d 100' width='%d' role='img' aria-label='regla y lápiz'>%s</svg></div>" % (W + 20, W + 20, "".join(s))


def s2_regla():
    cm = R.randint(3, 11)
    mm = R.choice([0, R.randint(1, 9)])
    t = cm * 10 + mm
    k = R.choice(["cm", "mm"])
    if k == "mm":
        return mcq(regla(cm, mm) + "¿Cuánto mide el lápiz en milímetros?", "%d mm" % t, ["%d mm" % (cm + mm), "%d mm" % (t + 10), "%d mm" % (cm * 100 + mm), "%d cm" % t],
                   "%d cm = %d mm; %d + %d = <b>%d mm</b>." % (cm, cm * 10, cm * 10, mm, t))
    if mm == 0:
        return mcq(regla(cm, 0) + "¿Cuánto mide el lápiz?", "%d cm" % cm, ["%d cm" % (cm + 1), "%d cm" % (cm - 1), "%d mm" % cm, "%d m" % cm], "Empieza en el 0 y llega al %d: <b>%d cm</b>." % (cm, cm))
    return mcq(regla(cm, mm) + "¿Cuánto mide el lápiz?", "%d cm y %d mm" % (cm, mm), ["%d cm y %d mm" % (cm + 1, mm), "%d cm y %d mm" % (mm, cm) if mm != cm else "%d cm" % cm, "%d cm" % cm, "%d cm y %d mm" % (cm, 10 - mm) if 10 - mm != mm else "%d cm y %d mm" % (cm - 1, mm)],
               "Llega %d mm después del %d: <b>%d cm y %d mm</b>." % (mm, cm, cm, mm))


def s3_pasar():
    if R.random() < 0.5:
        return M.conv(R, M.LON, PAIRS)
    return M.conv(R, M.LON, PAIRS_UP)


def s4_complejas():
    k = R.choice(["mcm", "kmm", "cmmm", "comp", "comp", "dec"])
    if k == "mcm":
        return M.compound(R, M.LON, "m", "cm", 100)
    if k == "kmm":
        return M.compound(R, M.LON, "km", "m", 1000)
    if k == "cmmm":
        return M.compound(R, M.LON, "cm", "mm", 10)
    if k == "dec":
        c = R.randint(101, 999)
        return mcq("¿Cuántos centímetros son %s m?" % dz(c, 2), "%d cm" % c, ["%d cm" % (c // 10), "%d cm" % (c * 10), "%s cm" % dz(c, 1), "%d cm" % (c % 100) if c % 100 else "%d cm" % (c + 100)],
                   "1 m = 100 cm; %s m = <b>%d cm</b>." % (dz(c, 2), c))
    pr = R.choice([("m", "cm"), ("km", "m"), ("cm", "mm"), ("m", "dm"), ("dm", "mm")])
    return M.comparar(R, M.LON, [pr])


def s5_problema():
    p, g = K.next()
    k = R.choice(["carrera", "cinta", "vueltas", "faltan", "pasos", "tela", "camino"])
    if k == "carrera":
        a = R.randint(2, 9)
        b = R.randint(100, 900)
        return mcq("%s corre %d km y %d m. ¿Cuántos metros corre?" % (p, a, b), "%s m" % num(a * 1000 + b), ["%s m" % num(a * 100 + b), "%s m" % num(a + b), "%s m" % num(a * 1000 + b * 10), "%s m" % num(a * 10000 + b)],
                   "%d km = %s m; %s + %d = <b>%s m</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if k == "cinta":
        L = R.choice([2, 3, 4, 5])
        c = R.choice([20, 25, 40, 50])
        return mcq("Una cinta mide %d m. La cortamos en trozos de %d cm. ¿Cuántos trozos salen?" % (L, c), str(L * 100 // c), [str(L * 10 // c) if L * 10 // c else str(L * 100 // c + 1), str(L * c), str(L * 100 // c * 10), str(L * 100 // c - 1)],
                   "%d m = %d cm; %d : %d = <b>%d</b>." % (L, L * 100, L * 100, c, L * 100 // c))
    if k == "vueltas":
        v = R.choice([200, 250, 400, 500])
        n = R.randint(3, 12)
        return mcq("Una pista mide %d m. %s da %d vueltas. ¿Cuántos kilómetros y metros recorre?" % (v, p, n), "%d km y %d m" % divmod(v * n, 1000) if v * n % 1000 else "%d km" % (v * n // 1000),
                   ["%d km y %d m" % (v * n // 100, v * n % 100) if v * n % 100 else "%d km" % (v * n // 100), "%d km y %d m" % (n, v), "%s km" % num(v * n), "%d km y %d m" % (v * n // 1000 + 1, v * n % 1000)],
                   "%d %s %d = %s m = <b>%s</b>." % (v, "×", n, num(v * n), "%d km y %d m" % divmod(v * n, 1000) if v * n % 1000 else "%d km" % (v * n // 1000)))
    if k == "faltan":
        t = R.randint(5, 25)
        d = R.randint(1000, t * 1000 - 100)
        return mcq("Una excursión tiene %d km. Ya hemos andado %s m. ¿Cuántos metros faltan?" % (t, num(d)), "%s m" % num(t * 1000 - d), ["%s m" % num(t * 100 - d) if t * 100 > d else "%s m" % num(t * 1000 + d), "%s m" % num(abs(t - d)), "%s m" % num(t * 1000 - d + 1000), "%s m" % num(t * 1000 - d - 100)],
                   "%d km = %s m; %s − %s = <b>%s m</b>." % (t, num(t * 1000), num(t * 1000), num(d), num(t * 1000 - d)))
    if k == "pasos":
        c = R.choice([50, 60, 70, 80])
        n = R.choice([100, 200, 500, 1000])
        return mcq("Cada paso de %s mide %d cm. ¿Cuántos metros recorre en %d pasos?" % (p, c, n), "%s m" % num(c * n // 100), ["%s m" % num(c * n), "%s m" % num(c * n // 10), "%s m" % num(c * n // 1000) if c * n // 1000 else "%s m" % num(c * n // 100 + 10), "%s m" % num(c + n)],
                   "%d %s %d = %s cm = <b>%s m</b>." % (c, "×", n, num(c * n), num(c * n // 100)))
    if k == "tela":
        a = R.randint(2, 6)
        b = R.randint(15, 85)
        u = R.randint(50, a * 100 - 10)
        r = a * 100 + b - u
        return mcq("Una modista tiene %d m y %d cm de tela. Usa %d cm para una falda. ¿Cuántos centímetros le quedan?" % (a, b, u), "%d cm" % r, ["%d cm" % (a * 100 + b + u), "%d cm" % (a * 10 + b - u) if a * 10 + b > u else "%d cm" % (r + 100), "%d cm" % (r + 10), "%d cm" % (r - 100)],
                   "%d m y %d cm = %d cm; %d − %d = <b>%d cm</b>." % (a, b, a * 100 + b, a * 100 + b, u, r))
    a, b = R.randint(1200, 4800), R.randint(1200, 4800)
    return mcq("De casa al colegio hay %s m y del colegio a la piscina, %s m. ¿Cuántos kilómetros y metros hay de casa a la piscina pasando por el colegio?" % (num(a), num(b)),
               "%d km y %d m" % divmod(a + b, 1000), ["%d km y %d m" % divmod(abs(a - b) + 1000, 1000), "%d km y %d m" % ((a + b) // 100, (a + b) % 100), "%d km y %d m" % divmod(a + b + 1000, 1000), "%d km" % ((a + b) // 1000)],
               "%s + %s = %s m = <b>%d km y %d m</b>." % (num(a), num(b), num(a + b), (a + b) // 1000, (a + b) % 1000)) if (a + b) % 1000 else None


def main():
    seen = set()
    sets = [
        ("Unidades de longitud", mix(R, seen, [(s1_unidades, 12), (s1_adecuada, 8)])),
        ("Medir con la regla", mix(R, seen, [(s2_regla, 20)])),
        ("Pasar de una unidad a otra", mix(R, seen, [(s3_pasar, 20)])),
        ("Expresiones complejas y comparar", mix(R, seen, [(s4_complejas, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["La unidad principal de longitud es el <b>metro</b> (m). Las unidades mayores son el kilómetro (km), el hectómetro (hm) y el decámetro (dam); las menores, el decímetro (dm), el centímetro (cm) y el milímetro (mm).",
         "km → hm → dam → m → dm → cm → mm: cada unidad es <b>10 veces</b> la siguiente.",
         "Para pasar a una unidad <b>menor</b>, multiplica (× 10, × 100, × 1000). Para pasar a una unidad <b>mayor</b>, divide."],
        [("¿Cuántos metros son 3 km y 250 m?", ["3 km = 3000 m", "3000 + 250"], "3250 m"),
         ("¿Cuántos metros son 4500 cm?", ["De cm a m dividimos entre 100", "4500 : 100"], "45 m")],
        [["Multiplicar al pasar a una unidad mayor", "De cm a m se divide: 400 cm = 4 m."],
         ["Pensar que 1 m = 10 cm", "1 m = 10 dm = 100 cm = 1000 mm."],
         ["No empezar a medir en el 0", "Coloca el principio del objeto en el 0 de la regla."]],
        _F.table(["km", "hm", "dam", "m", "dm", "cm", "mm"], [["1000 m", "100 m", "10 m", "1 m", "0,1 m", "0,01 m", "0,001 m"]]))
    faq = [("¿Cuántos centímetros tiene un metro?", "Un metro tiene 100 centímetros, 10 decímetros y 1000 milímetros."),
           ("¿Cómo se pasa de kilómetros a metros?", "Se multiplica por 1000: 5 km = 5000 m. Para pasar de metros a kilómetros se divide entre 1000.")]
    make_unit(R, "medidas-de-longitud", "M",
              "Unidades del Sistema Métrico Decimal de longitud: el metro, sus múltiplos y submúltiplos; equivalencias y conversiones; medición con instrumentos; estimación de longitudes; resolución de problemas",
              "Medidas de longitud", "Medidas de longitud",
              "Fichas de matemáticas de 4.º de Primaria: km, hm, dam, m, dm, cm y mm, medir con la regla, pasar de una unidad a otra, comparar longitudes y problemas. 100 ejercicios con soluciones.",
              "Cada unidad vale 10 de la siguiente", "A una menor, multiplica; a una mayor, divide.",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
