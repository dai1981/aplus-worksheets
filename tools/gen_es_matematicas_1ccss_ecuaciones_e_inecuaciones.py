# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Ecuaciones e inecuaciones (Sentido algebraico)
Factorización (Ruffini), fracciones algebraicas, ecuaciones polinómicas y racionales, inecuaciones; problemas de economía (beneficios, tarifas, repartos).
Reutiliza los generadores de Matemáticas I con otra semilla.
Errores: cerrar el intervalo en una desigualdad estricta, dar solo una raíz, plantear mal «cada uno paga menos».
"""
import random
from es_ccss import M, mix, num, unit, L, r2, W, eu, use_, sg, E

R = random.Random(53003)
s_factorizar, s_ecuacion, s_inecuacion, s_fraccion = use_("gen_es_matematicas_1bach_ecuaciones_e_inecuaciones", 53203, "s_factorizar", "s_ecuacion", "s_inecuacion", "s_fraccion")


def bx(a, b, c):
    """−x² + bx − c → texto"""
    return "−x² + %dx %s %d" % (b, "−" if c > 0 else "+", abs(c))


def s_problema():
    t = R.choice(["beneficio", "beneficio", "minimo", "regalo", "tarifa", "tarifa", "taller"])
    if t in ("beneficio", "minimo"):
        r1, r2_ = sorted(R.sample(range(1, 15), 2))
        if r2_ - r1 < 3:
            return None
        b, c = r1 + r2_, r1 * r2_
        if t == "beneficio":
            ok = "entre %d y %d cientos de unidades" % (r1, r2_)
            return M("El beneficio de una empresa es B(x) = %s (miles de euros), con x en cientos de unidades. ¿Para qué producción hay beneficios (B(x) &gt; 0)?" % bx(1, b, c), ok,
                     ["menos de %d o más de %d cientos de unidades" % (r1, r2_), "más de %d cientos de unidades" % r1, "entre 0 y %d cientos de unidades" % r2_],
                     "−x² + %dx − %d = 0 → x = %d y x = %d. La parábola abre hacia abajo: es positiva <b>%s</b>." % (b, c, r1, r2_, ok))
        k = R.randint(1, 4)
        # B(x) ≥ k  →  −x² + bx − c − k ≥ 0 ; elegimos raíces enteras
        s1, s2 = r1 + 1, r2_ - 1
        if s2 <= s1:
            return None
        b2, c2 = s1 + s2, s1 * s2
        if b2 != b:
            return None
        k = c2 - c
        if k <= 0:
            return None
        ok = "entre %d y %d cientos de unidades (incluidos)" % (s1, s2)
        return M("El beneficio es B(x) = %s (miles de euros), x en cientos de unidades. ¿Qué producción da un beneficio de al menos %d mil euros?" % (bx(1, b, c), k), ok,
                 ["entre %d y %d cientos de unidades" % (r1, r2_), "menos de %d o más de %d cientos de unidades" % (s1, s2), "%d cientos de unidades exactamente" % ((s1 + s2) // 2)],
                 "−x² + %dx − %d ≥ %d → x² − %dx + %d ≤ 0 → raíces %d y %d: <b>%s</b>." % (b, c, k, b, c2, s1, s2, ok))
    if t == "regalo":
        n, k = R.randint(4, 12), R.randint(1, 4)
        c = R.choice([1, 2, 3, 4, 5, 6])
        P = c * n * (n + k)
        if P % k:
            return None
        P //= k
        return M("Unos amigos compran un regalo de %s y lo pagan a partes iguales. Si hubiera %s más, cada uno pagaría %s menos. ¿Cuántos amigos son?" % (eu(P, 0), "un amigo" if k == 1 else "%d amigos" % k, eu(c, 0)), "%d amigos" % n,
                 W(["%d amigos" % (n + k), "%d amigos" % (n - 1), "%d amigos" % (P // (c * 10)) if P // (c * 10) not in (n, n + k, n - 1) else None, "%d amigos" % (n + 1), "%d amigos" % (2 * n)]),
                 "%d/x − %d/(x + %d) = %d → %dx² + %dx − %d = 0 → x = <b>%d</b> (la otra raíz es negativa)." % (P, P, k, c, c, c * k, P * k, n))
    if t == "tarifa":
        f = R.choice([10, 12, 15, 20, 25])
        a, b = R.choice([(5, 10), (4, 8), (6, 10), (3, 8), (5, 15), (2, 6)])
        x0 = f * 100 / (b - a)
        if x0 != int(x0):
            return None
        x0 = int(x0)
        ok = "más de %d minutos" % x0
        return M("Tarifa A: %s al mes más %d céntimos por minuto. Tarifa B: %d céntimos por minuto, sin cuota. ¿Cuándo es más barata la tarifa A?" % (eu(f * 100 / 100, 0), a, b), ok,
                 W(["menos de %d minutos" % x0, "más de %d minutos" % int(f * 100 / b), "más de %d minutos" % int(f * 100 / a) if f * 100 % a == 0 else "más de %d minutos" % (2 * x0)]),
                 "%d + %s x &lt; %s x → %s x &gt; %d → x &gt; %d: <b>%s</b>." % (f, r2(a / 100), r2(b / 100), r2((b - a) / 100), f, x0, ok))
    pre = R.choice([20, 25, 30, 40])
    ex = R.randint(8, 30)
    fij = pre * ex
    v = R.choice([5, 8, 10, 12])
    pv = pre + v
    n = fij // v + 1
    return M("Un taller tiene %s de gastos fijos al mes. Cada mueble le cuesta %s y lo vende por %s. ¿Cuántos muebles debe vender, como mínimo, para no perder dinero?" % (eu(fij, 0), eu(pre, 0), eu(pv, 0)),
             "%d muebles" % (fij // v if fij % v == 0 else n),
             W(["%d muebles" % (fij // pv + 1), "%d muebles" % (fij // pre), "%d muebles" % ((fij // v if fij % v == 0 else n) + 1), "%d muebles" % ((fij // v if fij % v == 0 else n) * 2)]),
             "Gana %s por mueble: %d x ≥ %d → x ≥ %s → <b>%d muebles</b>." % (eu(v, 0), v, fij, r2(fij / v), fij // v if fij % v == 0 else n))


seen = set()
sets = [("Factorizar polinomios", mix(R, seen, [(s_factorizar, 20)])), ("Fracciones algebraicas", mix(R, seen, [(s_fraccion, 20)])), ("Ecuaciones", mix(R, seen, [(s_ecuacion, 20)])),
        ("Inecuaciones", mix(R, seen, [(s_inecuacion, 20)])), ("Problemas de economía", mix(R, seen, [(s_problema, 20)]))]
think = ["Para <b>factorizar</b> un polinomio se buscan sus raíces entre los divisores del término independiente (Ruffini).",
         "Las <b>ecuaciones racionales</b> se resuelven quitando denominadores; luego se comprueba que ninguna solución anula un denominador.",
         "Una <b>inecuación</b> se resuelve buscando dónde vale 0 y estudiando el signo en cada trozo de la recta. &lt; y &gt; dan intervalos abiertos; ≤ y ≥, cerrados.",
         "En los problemas, la incógnita debe tener sentido: no hay −3 amigos ni 2,5 muebles."]
ex = [("B(x) = −x² + 12x − 20 &gt; 0", ["raíces x = 2 y x = 10", "abre hacia abajo"], "2 &lt; x &lt; 10"), ("Regalo de 120 € entre x amigos; con 2 más, cada uno paga 5 € menos", ["120/x − 120/(x + 2) = 5", "x² + 2x − 48 = 0"], "x = 6")]
mist = [["Cerrar el intervalo con &gt;", "Si es estricta, los extremos no entran."], ["Dar la raíz negativa", "En los problemas, descarta las soluciones sin sentido."],
        ["Olvidar el cambio de sentido", "Al multiplicar por un número negativo, &lt; pasa a &gt;."]]
body = L(think, ex, mist)
faq = [("¿Cómo se resuelve una inecuación de segundo grado?", "Se resuelve la ecuación igualada a cero y se estudia el signo en los intervalos que forman las raíces (o se dibuja la parábola)."),
       ("¿Qué es el umbral de rentabilidad?", "La producción a partir de la cual los ingresos cubren los costes: beneficio ≥ 0.")]
unit(1, R, "ecuaciones-e-inecuaciones", "A", "Polinomios y fracciones algebraicas; ecuaciones polinómicas y racionales; inecuaciones; problemas de beneficios, tarifas y repartos",
     "Ecuaciones e inecuaciones", "Ecuaciones e inecuaciones", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: factorización, ecuaciones, inecuaciones y problemas de beneficios y tarifas. 100 ejercicios con soluciones.",
     "Inecuación: estudia el signo", "Descarta las soluciones sin sentido.", body, faq, sets, 3)
