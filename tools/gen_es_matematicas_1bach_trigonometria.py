# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Trigonometría (Sentido de la medida)
Grados y radianes, razones de cualquier ángulo (reducción al primer cuadrante), identidades, razones de la suma y del ángulo doble,
ecuaciones trigonométricas, funciones seno, coseno y tangente (periodo, amplitud).
Errores: sen (a + b) = sen a + sen b, dar solo una solución de sen x = 1/2, signo equivocado según el cuadrante.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, fq, num, unit, L, MINUS, pi_txt, nf, kurve, BLUE, RED, W

R = random.Random(51005)
VAL = {0: ("0", "1", "0"), 30: ("1/2", "√3/2", "√3/3"), 45: ("√2/2", "√2/2", "1"), 60: ("√3/2", "1/2", "√3"), 90: ("1", "0", "no existe")}
RZ = ["sen", "cos", "tg"]


def neg(s):
    return s if s in ("0", "no existe") else (s[1:] if s.startswith(MINUS) else MINUS + s)


def val(g, rz):
    g %= 360
    i = RZ.index(rz)
    if g in (0, 90, 180, 270):
        tab = {0: ("0", "1", "0"), 90: ("1", "0", "no existe"), 180: ("0", MINUS + "1", "0"), 270: (MINUS + "1", "0", "no existe")}
        return tab[g][i]
    q = g // 90
    ref = [g, 180 - g, g - 180, 360 - g][q]
    sgn = [(1, 1, 1), (1, -1, -1), (-1, -1, 1), (-1, 1, -1)][q][i]
    v = VAL[ref][i]
    return v if sgn > 0 else neg(v)


def s_radianes():
    g = R.choice([15, 18, 20, 36, 40, 72, 75, 105, 135, 210, 225, 240, 300, 315, 330, 450, 540, 720])
    f = F(g, 180)
    if R.random() < 0.5:
        return M("Expresa %d° en radianes." % g, pi_txt(f) + " rad", W([pi_txt(F(g, 360)) + " rad", pi_txt(f * 2) + " rad", pi_txt(F(180, g)) + " rad", "%d rad" % g]), "%d° · π/180 = <b>%s rad</b>." % (g, pi_txt(f)))
    return M("Expresa %s rad en grados." % pi_txt(f), "%d°" % g, W(["%d°" % (g // 2), "%d°" % (2 * g), "%d°" % (360 - g) if g < 360 else "%d°" % (g - 180), "%d°" % (g + 90)]), "%s · 180/π = <b>%d°</b>." % (pi_txt(f), g))


def s_cualquier():
    g = R.choice([120, 135, 150, 210, 225, 240, 300, 315, 330, 390, 405, 420, 480, 495, 510, -30, -45, -60, -120, -150, 180, 270])
    rz = R.choice(["sen", "cos"] if g % 180 == 90 else RZ)
    ok = val(g, rz)
    other = val(g, "cos" if rz == "sen" else "sen")
    w = W([neg(ok), other, neg(other), "1/2", "√3/2", "√2/2", MINUS + "1/2"])
    w = [x for x in w if x != ok]
    gg = g % 360
    q = gg // 90 + 1
    gt = "(%s°)" % sg(g) if g < 0 else "%d°" % g
    pre = "%s equivale a %d°, " % (gt.strip("()"), gg) if g != gg else "%d° está " % g
    return M("Calcula el valor exacto de %s %s." % (rz, gt), ok, w, "%sen el %d.º cuadrante; se reduce al primero y se pone el signo: <b>%s</b>." % (pre, q, ok) if gg % 90 else "%s° equivale a %d°: <b>%s</b>." % (sg(g), gg, ok))


TR = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]


def s_identidades():
    a, b, c = R.choice(TR)
    if R.random() < 0.5:
        a, b = b, a
    q = R.choice([1, 2, 3, 4])
    ss = 1 if q in (1, 2) else -1
    cs = 1 if q in (1, 4) else -1
    t = R.choice(["cos", "tg", "sen", "simp"])
    S = (MINUS if ss < 0 else "") + fq(F(a, c))
    Cc = (MINUS if cs < 0 else "") + fq(F(b, c))
    Tg = (MINUS if ss * cs < 0 else "") + fq(F(a, b))
    if t == "cos":
        return M("Si sen α = %s y α está en el %d.º cuadrante, ¿cuánto vale cos α?" % (S, q), Cc, W([neg(Cc), Tg, (MINUS if cs < 0 else "") + fq(F(c - a, c))]), "cos² α = 1 − sen² α = %d/%d; en el %d.º cuadrante el coseno es %s: <b>%s</b>." % (b * b, c * c, q, "negativo" if cs < 0 else "positivo", Cc))
    if t == "tg":
        return M("Si cos α = %s y α está en el %d.º cuadrante, ¿cuánto vale tg α?" % (Cc, q), Tg, W([neg(Tg), (MINUS if ss * cs < 0 else "") + fq(F(b, a)), S]), "sen α = %s; tg α = sen α / cos α = <b>%s</b>." % (S, Tg))
    if t == "sen":
        return M("Si tg α = %s y α está en el %d.º cuadrante, ¿cuánto vale sen α?" % (Tg, q), S, W([neg(S), Cc, (MINUS if ss < 0 else "") + fq(F(a, b))]), "1 + tg² α = 1/cos² α → cos α = %s → sen α = <b>%s</b>." % (Cc, S))
    e, ok, w = R.choice([("(1 − cos² α)/sen α", "sen α", ["cos α", "1", "tg α"]), ("sen α · cos α / cos² α", "tg α", ["sen α", "cos α", "1"]), ("sen² α + cos² α + tg α · cos α", "1 + sen α", ["2", "1 + cos α", "sen α"]),
                        ("(sen α + cos α)² − 2 sen α cos α", "1", ["0", "2 sen α cos α", "sen² α"]), ("tg α · cos α", "sen α", ["cos α", "1", "tg² α"]), ("1/cos² α − tg² α", "1", ["0", "sen² α", "2"])])
    return M("Simplifica %s." % e, ok, w, "Usamos sen² α + cos² α = 1 y tg α = sen α / cos α: <b>%s</b>." % ok)


def s_suma():
    t = R.choice(["75", "15", "105", "doble", "doble", "dif"])
    if t in ("75", "15", "105"):
        g = int(t)
        rz = R.choice(["sen", "cos"])
        tab = {(75, "sen"): "(√6 + √2)/4", (75, "cos"): "(√6 − √2)/4", (15, "sen"): "(√6 − √2)/4", (15, "cos"): "(√6 + √2)/4", (105, "sen"): "(√6 + √2)/4", (105, "cos"): "(√2 − √6)/4"}
        ok = tab[(g, rz)]
        how = {75: "45° + 30°", 15: "45° − 30°", 105: "60° + 45°"}[g]
        return M("Calcula el valor exacto de %s %d°." % (rz, g), ok, W([x for x in ["(√6 + √2)/4", "(√6 − √2)/4", "(√2 − √6)/4", "(√3 + 1)/2", "(√2 + √3)/2"] if x != ok][:3] + ["(√2 + √3)/2"]), "%d° = %s y usamos la fórmula de %s %s: <b>%s</b>." % (g, how, rz, "de la suma" if "+" in how else "de la diferencia", ok))
    a, b, c = R.choice(TR)
    if R.random() < 0.5:
        a, b = b, a
    if t == "doble":
        rz = R.choice(["sen", "cos"])
        v = F(2 * a * b, c * c) if rz == "sen" else F(b * b - a * a, c * c)
        return M("Si sen α = %s y α es agudo, calcula %s 2α." % (fq(F(a, c)), rz), nf(v), W([nf(F(2 * a, c)), nf(-v), nf(F(a * a, c * c)), nf(F(2 * b, c))]), "%s → <b>%s</b>." % ("sen 2α = 2 sen α cos α = 2 · %s · %s" % (fq(F(a, c)), fq(F(b, c))) if rz == "sen" else "cos 2α = cos² α − sen² α = %d/%d − %d/%d" % (b * b, c * c, a * a, c * c), nf(v)))
    rz = R.choice(["sen", "cos"])
    q, ok, w = R.choice([("sen (90° − α)", "cos α", ["sen α", "−cos α", "−sen α"]), ("cos (180° − α)", "−cos α", ["cos α", "sen α", "−sen α"]), ("sen (180° + α)", "−sen α", ["sen α", "cos α", "−cos α"]),
                         ("cos (90° + α)", "−sen α", ["sen α", "cos α", "−cos α"]), ("tg (180° + α)", "tg α", ["−tg α", "1/tg α", "−1/tg α"]), ("sen (360° − α)", "−sen α", ["sen α", "cos α", "−cos α"])])
    ok, w = ok.replace("−", MINUS), [x.replace("−", MINUS) for x in w]
    return M("Simplifica %s." % q, ok, w, "Ángulos relacionados (o fórmula de la suma): <b>%s</b>." % ok)


def s_ecuaciones():
    t = R.choice(["sen", "cos", "tg", "cuad", "fact"])
    if t == "sen":
        v, sols = R.choice([("1/2", (30, 150)), ("√2/2", (45, 135)), ("√3/2", (60, 120)), (MINUS + "1/2", (210, 330)), (MINUS + "√3/2", (240, 300)), ("1", (90,)), (MINUS + "1", (270,))])
    elif t == "cos":
        v, sols = R.choice([("1/2", (60, 300)), ("√2/2", (45, 315)), ("√3/2", (30, 330)), (MINUS + "1/2", (120, 240)), (MINUS + "√2/2", (135, 225)), ("0", (90, 270))])
    elif t == "tg":
        v, sols = R.choice([("1", (45, 225)), ("√3", (60, 240)), (MINUS + "1", (135, 315)), ("√3/3", (30, 210))])
    elif t == "cuad":
        v, sols = None, (0, 90, 180) if False else None
        k = R.choice(["s2", "c2"])
        if k == "s2":
            sols = (45, 135, 225, 315)
            q = "2 sen² x = 1"
        else:
            sols = (30, 150, 210, 330)
            q = "4 sen² x = 1"
        return M("Resuelve %s en [0°, 360°)." % q, ", ".join("%d°" % s for s in sols), [", ".join("%d°" % s for s in sols[:2]), ", ".join("%d°" % s for s in sols[::2]), ", ".join("%d°" % s for s in (60, 120, 240, 300)) if k == "c2" else ", ".join("%d°" % s for s in (30, 150, 210, 330))],
                 "sen x = ± … → hay solución en los cuatro cuadrantes: <b>%s</b>." % ", ".join("%d°" % s for s in sols))
    else:
        return M("Resuelve sen x · cos x = 0 en [0°, 360°)." if R.random() < 0.5 else "Resuelve sen 2x = 0 en [0°, 360°).", "0°, 90°, 180°, 270°", ["0°, 180°", "90°, 270°", "0°, 90°"], "sen x = 0 → 0°, 180°; cos x = 0 → 90°, 270°: <b>0°, 90°, 180°, 270°</b>.")
    ok = ", ".join("%d°" % s for s in sols)
    alts = {1: [", ".join("%d°" % s for s in (sols[0],)), "%d°, %d°" % (sols[0], (sols[0] + 180) % 360), "%d°, %d°" % (sols[0], 360 - sols[0])]}
    pair = lambda a, b: "%d°, %d°" % (min(a, b), max(a, b))
    w = W(["%d°" % sols[0], pair(sols[0], (sols[0] + 180) % 360), pair(sols[0], (360 - sols[0]) % 360), pair((180 - sols[0]) % 360, (180 + sols[0]) % 360)])
    if len(sols) == 1:
        o = (sols[0] + 180) % 360
        w = ["%d°" % o, "%d°, %d°" % (min(sols[0], o), max(sols[0], o)), "%d°, %d°" % ((sols[0] + 90) % 360, (sols[0] + 270) % 360)]
    w = [x for x in w if x != ok]
    return M("Resuelve %s x = %s en [0°, 360°)." % (t, v), ok, w, "Buscamos el ángulo del primer cuadrante y los cuadrantes donde %s tiene ese signo: <b>%s</b>." % (t, ok))


def s_funciones():
    t = R.choice(["periodo", "amp", "graf", "rango"])
    k = R.choice([2, 3, 4, F(1, 2)])
    A = R.choice([2, 3, 4, 5])
    if t == "periodo":
        f = R.choice(["sen", "cos", "tg"])
        base = F(1) if f == "tg" else F(2)
        per = base / k
        return M("¿Cuál es el periodo de f(x) = %s (%sx)?" % (f, nf(k)), pi_txt(per), W([pi_txt(base * k), pi_txt(base), pi_txt(per / 2), pi_txt(per * 2)]), "Periodo de %s x: %s; dividido entre %s: <b>%s</b>." % (f, pi_txt(base), nf(k), pi_txt(per)))
    if t == "amp":
        c = R.randint(-3, 3)
        f = "%d sen x%s" % (A, (" + %d" % c) if c > 0 else (" − %d" % -c) if c < 0 else "")
        return M("¿Entre qué valores oscila f(x) = %s?" % f, "entre %s y %s" % (sg(c - A), sg(c + A)), ["entre %s y %s" % (sg(-A), sg(A)) if c else "entre −1 y 1", "entre %s y %s" % (sg(c - 1), sg(c + 1)), "entre %s y %s" % (sg(-A - c), sg(A - c)) if c else "entre 0 y %d" % A, "entre 0 y %d" % (A + c) if A + c > 0 else "entre %s y 0" % sg(c - A)],
                 "sen x va de −1 a 1; multiplicado por %d y sumando %s: <b>entre %s y %s</b>." % (A, sg(c), sg(c - A), sg(c + A)))
    if t == "rango":
        q, a, w = R.choice([("¿Cuál es el recorrido de f(x) = cos x?", "[−1, 1]", ["ℝ", "[0, 1]", "[0, 2π]"]), ("¿Cuál es el dominio de f(x) = tg x?", "ℝ menos los múltiplos impares de π/2", ["ℝ", "[−1, 1]", "ℝ menos los múltiplos de π"]),
                            ("¿Qué función es par?", "cos x", ["sen x", "tg x", "sen x + cos x"]), ("¿Cuánto vale el máximo de f(x) = sen x + 2?", "3", ["2", "1", "4"]),
                            ("¿Dónde corta f(x) = sen x al eje X en [0, 2π)?", "en 0 y en π", ["en π/2 y en 3π/2", "solo en 0", "en 0, π/2 y π"])])
        a, w = a.replace("−", MINUS), [x.replace("−", MINUS) for x in w]
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    f = R.choice(["sen", "cos"])
    A = R.choice([1, 2, 3])
    k = R.choice([1, 2])
    fn = (lambda x: A * math.sin(k * x)) if f == "sen" else (lambda x: A * math.cos(k * x))
    lab = "%s%s %s" % ("" if A == 1 else "%d " % A, f, "x" if k == 1 else "2x")
    pic = kurve([(fn, BLUE, "")], (0, 2 * math.pi, math.pi / 2), (-3, 3, 1), W=360, H=220, label="gráfica de una función trigonométrica", xlab=lambda x: pi_txt(F(round(x / math.pi * 2), 2)))
    opts = W(["%s%s %s" % ("" if a_ == 1 else "%d " % a_, g, "x" if kk == 1 else "2x") for a_, g, kk in ((A, f, k), (A, "cos" if f == "sen" else "sen", k), (A, f, 3 - k), (A % 3 + 1, f, k))])
    return M(pic + "¿Qué función está representada?", lab, [o for o in opts if o != lab], "Empieza en %s, llega a %d y repite cada %s: <b>%s</b>." % ("0" if f == "sen" else "su máximo", A, pi_txt(F(2, k)), lab))


seen = set()
sets = [("Radianes y ángulos de cualquier cuadrante", mix(R, seen, [(s_radianes, 8), (s_cualquier, 12)])), ("Relaciones e identidades", mix(R, seen, [(s_identidades, 20)])), ("Suma, diferencia y ángulo doble", mix(R, seen, [(s_suma, 20)])),
        ("Ecuaciones trigonométricas", mix(R, seen, [(s_ecuaciones, 20)])), ("Funciones trigonométricas", mix(R, seen, [(s_funciones, 20)]))]
think = ["180° = π rad. Para un ángulo de cualquier cuadrante se busca su <b>ángulo de referencia</b> en el primero y se pone el signo del cuadrante (seno: signo de y; coseno: signo de x).",
         "<b>Suma</b>: sen (a + b) = sen a cos b + cos a sen b; cos (a + b) = cos a cos b − sen a sen b. <b>Ángulo doble</b>: sen 2α = 2 sen α cos α; cos 2α = cos² α − sen² α.",
         "Una <b>ecuación trigonométrica</b> suele tener dos soluciones en cada vuelta: búscalas en los dos cuadrantes con el signo correcto."]
ex = [("sen 75°", ["sen (45° + 30°)", "√2/2 · √3/2 + √2/2 · 1/2"], "(√6 + √2)/4"), ("sen x = 1/2 en [0°, 360°)", ["primer y segundo cuadrante"], "30° y 150°")]
mist = [["sen (a + b) = sen a + sen b", "Falso: usa la fórmula de la suma."], ["Dar solo 30° en sen x = 1/2", "También 150° (segundo cuadrante)."], ["Signo equivocado", "cos 120° = −1/2: en el 2.º cuadrante el coseno es negativo."]]
body = L(think, ex, mist, kurve([(math.sin, BLUE, "sen x"), (math.cos, RED, "cos x")], (0, 2 * math.pi, math.pi / 2), (-1.5, 1.5, 0.5), W=360, H=220, label="funciones seno y coseno", xlab=lambda x: pi_txt(F(round(x / math.pi * 2), 2))))
faq = [("¿Por qué se usan radianes?", "Porque simplifican las fórmulas de arcos, áreas de sectores y derivadas: la longitud del arco es radio · ángulo."),
       ("¿Cuántas soluciones tiene sen x = 1/2?", "Infinitas: 30° + 360°k y 150° + 360°k. En una sola vuelta, dos.")]
unit(1, R, "trigonometria", "M", "Razones trigonométricas de cualquier ángulo; radianes; identidades; razones de la suma, la diferencia y el ángulo doble; ecuaciones trigonométricas; funciones trigonométricas",
     "Trigonometría", "Trigonometría", "Fichas de Matemáticas I (1.º de Bachillerato): radianes, ángulos de cualquier cuadrante, identidades, fórmulas de la suma y del ángulo doble, ecuaciones y funciones trigonométricas. 100 ejercicios.",
     "sen² α + cos² α = 1", "Reduce al primer cuadrante y pon el signo.", body, faq, sets, 5)
