# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de ESO: Trigonometría (Sentido de la medida)
Grados y radianes, razones trigonométricas en el triángulo rectángulo, valores de 30°, 45° y 60°, relaciones fundamentales, signos y ángulos de los cuatro cuadrantes,
resolución de triángulos rectángulos y problemas de alturas y distancias.
Errores: confundir cateto opuesto y contiguo, usar la calculadora en radianes, olvidar el signo según el cuadrante.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, fq, d, num, unit, L, MINUS, figure

R = random.Random(50007)
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


def r2(x):
    return d(F(int(math.floor(x * 100 + 0.5)), 100))


def tri_pic(a, b, c, lab):
    pts = {"A": (0, 0), "C": (b, 0), "B": (b, a)}
    return figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("B", "C", lab[0]), ("A", "C", lab[1]), ("A", "B", lab[2])], right=[("C", "A", "B")], label="triángulo rectángulo con el ángulo recto en C")


def s_razones():
    a, b, c = R.choice(TRIPLES)
    if R.random() < 0.5:
        a, b = b, a
    k = R.choice([1, 1, 2, 3])
    a, b, c = a * k, b * k, c * k
    pic = tri_pic(a, b, c, ("%d cm" % a, "%d cm" % b, "%d cm" % c))
    rz = R.choice(["sen", "cos", "tg"])
    ang = R.choice(["A", "B"])
    op, co = (a, b) if ang == "A" else (b, a)
    v = {"sen": F(op, c), "cos": F(co, c), "tg": F(op, co)}
    ok = fq(v[rz])
    w = [fq(v[x]) for x in v if x != rz] + [fq(1 / v[rz])]
    txt = {"sen": "cateto opuesto / hipotenusa", "cos": "cateto contiguo / hipotenusa", "tg": "cateto opuesto / cateto contiguo"}[rz]
    return M(pic + "Calcula %s %s." % (rz, ang), ok, w, "%s %s = %s = <b>%s</b>." % (rz, ang, txt, ok))


def pi_txt(f):
    if f == 0:
        return "0"
    n, dd = f.numerator, f.denominator
    s = ("" if n == 1 else str(n)) + "π"
    return s if dd == 1 else s + "/" + str(dd)


def s_radianes():
    g = R.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 720])
    f = F(g, 180)
    if R.random() < 0.5:
        return M("Expresa %d° en radianes." % g, pi_txt(f) + " rad", [pi_txt(F(g, 360)) + " rad", pi_txt(f * 2) + " rad", "%d rad" % g if g < 100 else pi_txt(F(180, g)) + " rad", "%d rad" % g, pi_txt(f / 3) + " rad"], "%d° · π/180 = <b>%s rad</b>." % (g, pi_txt(f)))
    return M("Expresa %s rad en grados." % pi_txt(f), "%d°" % g, ["%d°" % (g // 2), "%d°" % (2 * g), "%d°" % (360 - g) if g != 180 else "90°"], "%s · 180/π = <b>%d°</b>." % (pi_txt(f), g))


VAL = {30: ("1/2", "√3/2", "√3/3"), 45: ("√2/2", "√2/2", "1"), 60: ("√3/2", "1/2", "√3"), 0: ("0", "1", "0"), 90: ("1", "0", "no existe")}


def neg(s):
    return s if s in ("0", "no existe") else MINUS + s


def val(g, rz):
    """valor exacto en los cuatro cuadrantes"""
    g %= 360
    if g in (0, 90, 180, 270):
        tab = {0: ("0", "1", "0"), 90: ("1", "0", "no existe"), 180: ("0", MINUS + "1", "0"), 270: (MINUS + "1", "0", "no existe")}
        return tab[g]["sen cos tg".split().index(rz)]
    q = g // 90
    ref = [g, 180 - g, g - 180, 360 - g][q]
    s, c, t = VAL[ref]
    sgn = [(1, 1, 1), (1, -1, -1), (-1, -1, 1), (-1, 1, -1)][q]
    out = [x if k > 0 else neg(x) for x, k in zip((s, c, t), sgn)]
    return out["sen cos tg".split().index(rz)]


def s_valores():
    t = R.choice(["agudo", "agudo", "cuad", "cuad", "signo"])
    if t == "agudo":
        g = R.choice([30, 45, 60])
        rz = R.choice(["sen", "cos", "tg"])
        ok = val(g, rz)
        w = sorted(set(["1/2", "√3/2", "√2/2", "√3", "√3/3", "1"]) - {ok})
        R.shuffle(w)
        return M("¿Cuánto vale %s %d°?" % (rz, g), ok, w, "Valor exacto: %s %d° = <b>%s</b>." % (rz, g, ok))
    if t == "cuad":
        g = R.choice([120, 135, 150, 210, 225, 240, 300, 315, 330])
        rz = R.choice(["sen", "cos"] if g in (90, 270) else ["sen", "cos", "tg"])
        ok = val(g, rz)
        w = [neg(ok) if not ok.startswith(MINUS) else ok[1:], val(g, "cos" if rz == "sen" else "sen"), neg(val(g, "cos" if rz == "sen" else "sen")) if not val(g, "cos" if rz == "sen" else "sen").startswith(MINUS) else val(g, "cos" if rz == "sen" else "sen")[1:], "1/2", "√3/2", "0"]
        q = (g % 360) // 90 + 1
        return M("¿Cuánto vale %s %d°?" % (rz, g), ok, w, "%d° está en el %d.º cuadrante; se reduce al primero y se pone el signo del cuadrante: <b>%s</b>." % (g, min(q, 4), ok))
    q = R.randint(1, 4)
    s, c = [(1, 1), (1, -1), (-1, -1), (-1, 1)][q - 1]
    tgs = s * c
    k = R.choice(["dos", "tg"])
    if k == "dos":
        return M("Si sen α %s 0 y cos α %s 0, ¿en qué cuadrante está α?" % ("&gt;" if s > 0 else "&lt;", "&gt;" if c > 0 else "&lt;"), "en el %d.º" % q, ["en el %d.º" % x for x in range(1, 5) if x != q], "Seno: signo de y; coseno: signo de x. <b>En el %d.º</b>." % q)
    ok = "positiva" if tgs > 0 else "negativa"
    return M("Si α está en el %d.º cuadrante, ¿cómo es tg α?" % q, ok, ["negativa" if tgs > 0 else "positiva", "cero", "no existe"], "tg = sen / cos: %s / %s → <b>%s</b>." % ("+" if s > 0 else MINUS, "+" if c > 0 else MINUS, ok))


def s_relaciones():
    a, b, c = R.choice(TRIPLES)
    if R.random() < 0.5:
        a, b = b, a
    t = R.choice(["sen_cos", "cos_tg", "tg_cos", "cuad", "ident"])
    if t == "sen_cos":
        return M("Si sen α = %s y α es agudo, ¿cuánto vale cos α?" % fq(F(a, c)), fq(F(b, c)), [fq(F(c - a, c)), fq(F(a, b)), fq(F(b, a))], "cos² α = 1 − sen² α = 1 − %d/%d = %d/%d → cos α = <b>%s</b>." % (a * a, c * c, b * b, c * c, fq(F(b, c))))
    if t == "cos_tg":
        return M("Si cos α = %s y α es agudo, ¿cuánto vale tg α?" % fq(F(b, c)), fq(F(a, b)), [fq(F(b, a)), fq(F(a, c)), fq(F(c, b))], "sen α = %s; tg α = sen α / cos α = <b>%s</b>." % (fq(F(a, c)), fq(F(a, b))))
    if t == "tg_cos":
        return M("Si tg α = %s y α es agudo, ¿cuánto vale cos α?" % fq(F(a, b)), fq(F(b, c)), [fq(F(a, c)), fq(F(b, a)), fq(F(c, b))], "1 + tg² α = 1/cos² α → cos² α = %d/%d → cos α = <b>%s</b>." % (b * b, c * c, fq(F(b, c))))
    if t == "cuad":
        q = R.choice([2, 3, 4])
        sgn_c = {2: -1, 3: -1, 4: 1}[q]
        sgn_s = {2: 1, 3: -1, 4: -1}[q]
        s_txt = (MINUS if sgn_s < 0 else "") + fq(F(a, c))
        ok = (MINUS if sgn_c < 0 else "") + fq(F(b, c))
        return M("Si sen α = %s y α está en el %d.º cuadrante, ¿cuánto vale cos α?" % (s_txt, q), ok, [ok[1:] if ok.startswith(MINUS) else MINUS + ok, (MINUS if sgn_c < 0 else "") + fq(F(a, b)), (MINUS if sgn_c > 0 else "") + fq(F(a, c))],
                 "|cos α| = %s y en el %d.º cuadrante el coseno es %s: <b>%s</b>." % (fq(F(b, c)), q, "negativo" if sgn_c < 0 else "positivo", ok))
    q, a_, w = R.choice([("¿Cuánto vale sen² α + cos² α?", "1", ["0", "2", "depende de α"]), ("tg α es igual a…", "sen α / cos α", ["cos α / sen α", "sen α · cos α", "1 − sen α"]),
                         ("¿Entre qué valores está el seno de cualquier ángulo?", "entre −1 y 1", ["entre 0 y 1", "entre 0 y 90", "puede ser cualquier número"]),
                         ("Si α y β son complementarios (suman 90°), sen α es igual a…", "cos β", ["sen β", "tg β", "−cos β"]),
                         ("sen (180° − α) es igual a…", "sen α", ["−sen α", "cos α", "−cos α"]), ("cos (−α) es igual a…", "cos α", ["−cos α", "sen α", "−sen α"]),
                         ("cos (180° − α) es igual a…", "−cos α", ["cos α", "sen α", "−sen α"]), ("sen (−α) es igual a…", "−sen α", ["sen α", "cos α", "−cos α"])])
    a_, w = a_.replace("−", MINUS), [x.replace("−", MINUS) for x in w]
    return M(q.replace("−", MINUS), a_, w, "Respuesta: <b>%s</b>." % a_)


def s_resolver():
    t = R.choice(["cat_ang", "hip_ang", "lados_ang", "hip_ang2"])
    g = R.choice([20, 25, 30, 35, 40, 50, 55, 60, 65, 70])
    rad = math.radians(g)
    if t == "cat_ang":
        b = R.randint(4, 30)
        a = b * math.tan(rad)
        pic = tri_pic(a, b, 0, ("a = ?", "b = %d m" % b, ""))
        return M(pic + "En el triángulo, A = %d° y b = %d m. ¿Cuánto mide el cateto a? (redondea a las centésimas)" % (g, b), "%s m" % r2(a), ["%s m" % r2(b * math.sin(rad)), "%s m" % r2(b / math.tan(rad)), "%s m" % r2(b * math.cos(rad))], "tg %d° = a / %d → a = %d · tg %d° ≈ <b>%s m</b>." % (g, b, b, g, r2(a)))
    if t in ("hip_ang", "hip_ang2"):
        c = R.randint(5, 40)
        a, b = c * math.sin(rad), c * math.cos(rad)
        want = "a" if t == "hip_ang" else "b"
        pic = tri_pic(a, b, c, ("a" if want != "a" else "a = ?", "b" if want != "b" else "b = ?", "c = %d m" % c))
        v = a if want == "a" else b
        o = b if want == "a" else a
        return M(pic + "En el triángulo, A = %d° y la hipotenusa c = %d m. ¿Cuánto mide %s? (redondea a las centésimas)" % (g, c, want), "%s m" % r2(v), ["%s m" % r2(o), "%s m" % r2(c * math.tan(rad)), "%s m" % r2(c / math.sin(rad) if want == "a" else c / math.cos(rad))],
                 "%s %d° = %s / %d → %s ≈ <b>%s m</b>." % ("sen" if want == "a" else "cos", g, want, c, want, r2(v)))
    a, b, c = R.choice(TRIPLES)
    if R.random() < 0.5:
        a, b = b, a
    A = math.degrees(math.atan2(a, b))
    gA = int(A)
    mA = int(round((A - gA) * 60))
    if mA == 60:
        gA, mA = gA + 1, 0
    pic = tri_pic(a, b, c, ("%d" % a, "%d" % b, "%d" % c))
    ok = "%d° %d′" % (gA, mA)
    o = 90 - A
    go, mo = int(o), int(round((o - int(o)) * 60))
    if mo == 60:
        go, mo = go + 1, 0
    return M(pic + "Con a = %d y b = %d, ¿cuánto mide el ángulo A?" % (a, b), ok, ["%d° %d′" % (go, mo), "%d° %d′" % (gA - 3, mA), "%d° %d′" % (gA + 3, mA)], "tg A = %d/%d → A = arctg(%d/%d) ≈ <b>%s</b>." % (a, b, a, b, ok))


def s_problema():
    t = R.choice(["arbol", "escalera", "rampa", "torre", "cometa", "faro"])
    g = R.choice([25, 30, 35, 40, 45, 50, 55, 60, 65])
    rad = math.radians(g)
    if t == "arbol":
        s = R.randint(5, 30)
        h = s * math.tan(rad)
        return M("Un árbol proyecta una sombra de %d m cuando los rayos del sol forman %d° con el suelo. ¿Cuánto mide el árbol?" % (s, g), "%s m" % r2(h), ["%s m" % r2(s * math.sin(rad)), "%s m" % r2(s / math.tan(rad)), "%s m" % r2(s * math.cos(rad))], "tg %d° = h / %d → h ≈ <b>%s m</b>." % (g, s, r2(h)))
    if t == "escalera":
        L_ = R.randint(3, 12)
        g = R.choice([60, 65, 70, 75, 80])
        rad = math.radians(g)
        k = R.choice(["alt", "pie"])
        v = L_ * math.sin(rad) if k == "alt" else L_ * math.cos(rad)
        o = L_ * math.cos(rad) if k == "alt" else L_ * math.sin(rad)
        return M("Una escalera de %d m está apoyada en una pared y forma %d° con el suelo. ¿%s?" % (L_, g, "A qué altura llega" if k == "alt" else "A qué distancia de la pared está el pie"), "%s m" % r2(v), ["%s m" % r2(o), "%s m" % r2(L_ * math.tan(rad)), "%s m" % r2(L_ / math.sin(rad))], "%s %d° · %d ≈ <b>%s m</b>." % ("sen" if k == "alt" else "cos", g, L_, r2(v)))
    if t == "rampa":
        h, dd = R.choice([(1, 12), (1, 10), (1, 8), (2, 15), (1, 20), (3, 20)])
        A = math.degrees(math.atan2(h, dd))
        ok = "%s°" % r2(A)
        return M("Una rampa sube %d m en una distancia horizontal de %d m. ¿Qué ángulo forma con el suelo? (en grados, a las centésimas)" % (h, dd), ok, ["%s°" % r2(math.degrees(math.asin(h / dd))) if h < dd else "%s°" % r2(A * 2), "%s°" % r2(90 - A), "%s°" % r2(A * 2)], "tg α = %d/%d → α ≈ <b>%s</b>." % (h, dd, ok))
    if t == "torre":
        dd = R.randint(20, 80)
        h = dd * math.tan(rad)
        return M("Desde un punto situado a %d m del pie de una torre, se ve su parte más alta con un ángulo de elevación de %d°. ¿Cuánto mide la torre?" % (dd, g), "%s m" % r2(h), ["%s m" % r2(dd * math.sin(rad)), "%s m" % r2(dd / math.tan(rad)), "%s m" % r2(dd * math.cos(rad))], "tg %d° = h / %d → h ≈ <b>%s m</b>." % (g, dd, r2(h)))
    if t == "cometa":
        L_ = R.randint(20, 60)
        if g == 45:
            return None
        h = L_ * math.sin(rad)
        return M("El hilo de una cometa mide %d m y forma %d° con el suelo. ¿A qué altura está la cometa (sin contar la altura de la mano)?" % (L_, g), "%s m" % r2(h), ["%s m" % r2(L_ * math.cos(rad)), "%s m" % r2(L_ * math.tan(rad)), "%s m" % r2(L_ / math.sin(rad))], "sen %d° = h / %d → h ≈ <b>%s m</b>." % (g, L_, r2(h)))
    h = R.randint(20, 60)
    g = R.choice([10, 15, 20, 25, 30])
    rad = math.radians(g)
    dd = h / math.tan(rad)
    return M("Desde lo alto de un faro de %d m se ve un barco con un ángulo de depresión de %d°. ¿A qué distancia del pie del faro está el barco?" % (h, g), "%s m" % r2(dd), ["%s m" % r2(h * math.tan(rad)), "%s m" % r2(h / math.sin(rad)), "%s m" % r2(h * math.cos(rad))], "tg %d° = %d / x → x = %d / tg %d° ≈ <b>%s m</b>." % (g, h, h, g, r2(dd)))


seen = set()
sets = [("Grados, radianes y razones", mix(R, seen, [(s_radianes, 8), (s_razones, 12)])), ("Valores de 30°, 45° y 60° y cuadrantes", mix(R, seen, [(s_valores, 20)])), ("Relaciones fundamentales", mix(R, seen, [(s_relaciones, 20)])),
        ("Resolver triángulos rectángulos", mix(R, seen, [(s_resolver, 20)])), ("Problemas de alturas y distancias", mix(R, seen, [(s_problema, 20)]))]
think = ["En un triángulo rectángulo, para un ángulo agudo α: <b>sen α</b> = opuesto / hipotenusa; <b>cos α</b> = contiguo / hipotenusa; <b>tg α</b> = opuesto / contiguo.",
         "<b>Relaciones fundamentales</b>: sen² α + cos² α = 1 y tg α = sen α / cos α.",
         "Valores exactos: sen 30° = 1/2, sen 45° = √2/2, sen 60° = √3/2 (el coseno, al revés).",
         "En los cuadrantes, el seno lleva el signo de y y el coseno el de x. 180° = π rad."]
ex = [("Triángulo de catetos 3 y 4", ["hipotenusa 5"], "sen A = 3/5, cos A = 4/5, tg A = 3/4"), ("Sombra de 10 m, ángulo de 35°", ["h = 10 · tg 35°"], "h ≈ 7 m")]
mist = [["Confundir opuesto y contiguo", "El contiguo toca al ángulo; el opuesto está enfrente."], ["Calculadora en radianes", "Comprueba que está en modo DEG."], ["Olvidar el signo del cuadrante", "cos 120° = −1/2."]]
body = L(think, ex, mist, tri_pic(3, 4, 5, ("a (opuesto a A)", "b (contiguo a A)", "c (hipotenusa)")))
faq = [("¿Para qué sirve la trigonometría?", "Para calcular alturas y distancias que no se pueden medir directamente: edificios, montañas, la anchura de un río…"),
       ("¿Qué es un radián?", "El ángulo cuyo arco mide lo mismo que el radio. Una vuelta completa son 2π radianes (360°).")]
unit(4, R, "trigonometria", "M", "Razones trigonométricas de ángulos agudos y de cualquier ángulo; relaciones fundamentales; grados y radianes; resolución de triángulos rectángulos; problemas de alturas y distancias",
     "Trigonometría", "Trigonometría", "Fichas de matemáticas de 4.º de ESO: seno, coseno y tangente, valores exactos, relaciones, cuadrantes, radianes y problemas de alturas. 100 ejercicios con soluciones.",
     "sen² α + cos² α = 1", "tg α = sen α / cos α", body, faq, sets, 7)
