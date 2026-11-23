# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: El dinero (Sentido de la medida)
Monedas y billetes de euro, contar dinero, euros y céntimos, equivalencias (1 € = 100 céntimos), comparar precios,
calcular el total de una compra y la vuelta, el precio de varias unidades, presupuestos y ahorro.
Errores: contar las monedas en lugar de su valor, escribir 2,5 € como 2,05 €, olvidar que 1 € son 100 céntimos.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, eur, dinero_svg, POR, DIV, bank, Kids

R = random.Random(44017)
K = Kids(R)
COINS = [1, 2, 5, 10, 20, 50, 100, 200]
NOTES = [500, 1000, 2000, 5000, 10000, 20000]


def s1_contar():
    k = R.choice(["monedas", "billetes", "mixto"])
    if k == "monedas":
        it = [R.choice(COINS[3:]) for _ in range(R.randint(3, 6))]
    elif k == "billetes":
        it = [R.choice(NOTES[:4]) for _ in range(R.randint(2, 4))]
    else:
        it = [R.choice(NOTES[:3])] + [R.choice(COINS[2:]) for _ in range(R.randint(2, 4))]
    t = sum(it)
    return mcq(dinero_svg(it) + "¿Cuánto dinero hay?", eur(t), [eur(t + 100), eur(t - 10) if t > 10 else eur(t + 10), eur(t + 50), eur(len(it) * 100), eur(t * 10)],
               "Sumamos el valor de cada moneda y billete: <b>%s</b>." % eur(t))


def s1_equiv():
    k = R.choice(["cent", "euro", "cuantas", "cuantos_b"])
    if k == "cent":
        c = R.randint(105, 2999)
        return mcq("¿Cuántos céntimos son %s?" % eur(c), "%s céntimos" % num(c), ["%s céntimos" % num(c // 10), "%s céntimos" % num(c * 10), "%s céntimos" % num(c // 100 + c % 100), "%s céntimos" % num(c + 100)],
                   "1 € = 100 céntimos: <b>%s céntimos</b>." % num(c))
    if k == "euro":
        c = R.randint(105, 2999)
        return mcq("¿Cuántos euros son %s céntimos?" % num(c), eur(c), [eur(c * 10), "%s €" % num(c), eur(c // 10), "%d,%02d €" % (c // 1000, c % 1000 // 10) if c >= 1000 else eur(c + 100)],
                   "100 céntimos = 1 €: <b>%s</b>." % eur(c))
    if k == "cuantas":
        v = R.choice([10, 20, 50])
        t = R.choice([100, 200, 500, 1000])
        return mcq("¿Cuántas monedas de %d céntimos necesitas para tener %s?" % (v, eur(t)), str(t // v), [str(t // v // 10) if t // v >= 20 else str(t // v + 5), str(t // v * 10), str(v), str(t // v + 1)],
                   "%s = %d céntimos; %d %s %d = <b>%d</b>." % (eur(t), t, t, DIV, v, t // v))
    v = R.choice([500, 1000, 2000])
    t = v * R.randint(2, 10)
    return mcq("¿Cuántos billetes de %s hacen %s?" % (eur(v), eur(t)), str(t // v), [str(t // v + 1), str(t // v - 1), str(t // 100), str(t // v * 10)],
               "%s %s %s = <b>%d</b>." % (num(t // 100), DIV, num(v // 100), t // v))


def s2_comparar():
    k = R.choice(["barato", "caro", "dif", "suficiente"])
    if k in ("barato", "caro"):
        items = R.sample(["un balón", "una mochila", "un estuche", "un cómic", "una camiseta", "una gorra", "un puzle", "un libro"], 4)
        ps = R.sample(range(250, 2999), 4)
        f = min if k == "barato" else max
        i = ps.index(f(ps))
        lst = "; ".join("%s, %s" % (a, eur(b)) for a, b in zip(items, ps))
        return mcq("Precios: %s. ¿Qué es lo más %s?" % (lst, k), items[i], items, "%s es el precio %s: <b>%s</b>." % (eur(ps[i]), "menor" if k == "barato" else "mayor", items[i]))
    if k == "dif":
        a, b = R.randint(250, 4999), R.randint(250, 4999)
        if a == b:
            return None
        return mcq("Un patinete cuesta %s y una cometa %s. ¿Cuánto cuesta más el más caro?" % (eur(a), eur(b)), eur(abs(a - b)), [eur(a + b), eur(abs(a - b) + 100), eur(abs(a - b) + 10), eur(abs(a - b) - 1) if abs(a - b) > 1 else eur(2)],
                   "%s − %s = <b>%s</b>." % (eur(max(a, b)), eur(min(a, b)), eur(abs(a - b))))
    have = [R.choice([500, 1000, 200, 100, 50, 20]) for _ in range(R.randint(2, 4))]
    t = sum(have)
    pr = t + R.choice([-150, -50, -20, 30, 80, 120])
    if pr <= 0:
        return None
    ok = t >= pr
    return mcq(dinero_svg(have) + "Una entrada al zoo cuesta %s. ¿Tienes bastante dinero?" % eur(pr), "sí, y me sobran %s" % eur(t - pr) if ok else "no, me faltan %s" % eur(pr - t),
               ["no, me faltan %s" % eur(abs(t - pr)) if ok else "sí, y me sobran %s" % eur(abs(pr - t)), "sí, justo" if t != pr else "no", "no, me faltan %s" % eur(pr)],
               "Tienes %s: %s." % (eur(t), "<b>sí</b>, sobran %s" % eur(t - pr) if ok else "<b>no</b>, faltan %s" % eur(pr - t)))


def s3_compra():
    k = R.choice(["total", "vuelta", "vuelta", "varios"])
    p, g = K.next()
    if k == "total":
        it = R.sample([("pan", 120), ("leche", 95), ("huevos", 245), ("fruta", 360), ("queso", 475), ("arroz", 135), ("aceite", 890), ("yogures", 210)], 3)
        t = sum(c for _, c in it)
        return mcq("En el supermercado, %s compra %s." % (p, ", ".join("%s (%s)" % (a, eur(b)) for a, b in it)) + " ¿Cuánto paga?", eur(t), [eur(t + 100), eur(t - 10), eur(it[0][1] + it[1][1]), eur(t + 10)],
                   "%s = <b>%s</b>." % (" + ".join(eur(b) for _, b in it), eur(t)))
    if k == "vuelta":
        pr = R.randint(115, 1890)
        m = min(x for x in [500, 1000, 2000, 5000] if x > pr)
        return mcq("%s compra algo que cuesta %s y paga con un billete de %s. ¿Cuánto le devuelven?" % (p, eur(pr), eur(m)), eur(m - pr),
                   [eur(m - pr + 100), eur(m - pr - 10) if m - pr > 10 else eur(m - pr + 10), eur(pr), eur((m // 100 - pr // 100) * 100 - pr % 100) if (m // 100 - pr // 100) * 100 > pr % 100 and (m // 100 - pr // 100) * 100 - pr % 100 != m - pr else eur(m - pr + 1)],
                   "%s − %s = <b>%s</b>." % (eur(m), eur(pr), eur(m - pr)))
    n = R.randint(2, 9)
    pr = R.choice([45, 75, 125, 150, 199, 250, 320])
    return mcq("Un cuaderno cuesta %s. ¿Cuánto cuestan %d cuadernos?" % (eur(pr), n), eur(pr * n), [eur(pr + n), eur(pr * n + pr), eur(pr * (n - 1)), eur(pr * n * 10)],
               "%s %s %d = <b>%s</b>." % (eur(pr), POR, n, eur(pr * n)))


def s4_monedas():
    k = R.choice(["menos", "forma"])
    t = R.choice([35, 65, 85, 120, 175, 250, 315, 380, 460, 590, 745, 860])
    best = []
    r = t
    for c in [500, 200, 100, 50, 20, 10, 5, 2, 1]:
        while r >= c:
            best.append(c)
            r -= c
    if k == "menos":
        return mcq("Quieres pagar %s con el menor número de monedas y billetes. ¿Cuántos necesitas?" % eur(t, c=True), str(len(best)), [str(len(best) + 1), str(len(best) + 2), str(len(best) - 1), str(t // 10)],
                   "%s: <b>%d</b>." % (" + ".join(eur(x, c=True) for x in best), len(best)))
    ok = " + ".join(eur(x, c=True) for x in best)
    w1 = best[:-1] + [best[-1] * 2] if best[-1] in (5, 10, 20, 50, 100) else best[:-1]
    w2 = best[1:]
    w3 = best + [best[-1]]
    f = lambda L: " + ".join(eur(x, c=True) for x in L)
    return mcq("¿Qué grupo de monedas y billetes suma exactamente %s?" % eur(t, c=True), ok, [f(w1) if sum(w1) != t else None, f(w2) if w2 and sum(w2) != t else None, f(w3), f([x for x in best] + [1])],
               "%s = <b>%s</b>." % (ok, eur(t, c=True)))


def s5_problema():
    p, g = K.next()
    k = R.choice(["ahorro", "reparte", "presupuesto", "entradas", "oferta", "cumple"])
    if k == "ahorro":
        s, w, obj = R.choice([2, 3, 4, 5]), R.randint(4, 15), R.choice([4500, 6000, 8000, 3500])
        t = s * 100 * w
        return mcq("%s ahorra %d € cada semana durante %d semanas. Quiere unos patines de %s. ¿Cuánto %s?" % (p, s, w, eur(obj), "le sobra" if t >= obj else "le falta"), eur(abs(obj - t)),
                   [eur(t), eur(abs(obj - t) + 100), eur(obj), eur(abs(obj - s * 100))], "Ahorra %d %s %d = %s; %s." % (s, POR, w, eur(t), "le sobran <b>%s</b>" % eur(t - obj) if t >= obj else "le faltan <b>%s</b>" % eur(obj - t))) if t != obj else None
    if k == "reparte":
        n = R.choice([2, 3, 4, 5])
        c = R.randint(3, 20) * 100 + R.choice([0, 50])
        t = n * c
        return mcq("%d amigos compran un regalo de %s y lo pagan a partes iguales. ¿Cuánto paga cada uno?" % (n, eur(t)), eur(c), [eur(t - n * 100), eur(c + 100), eur(t), eur(c - 50)],
                   "%s %s %d = <b>%s</b>." % (eur(t), DIV, n, eur(c)))
    if k == "presupuesto":
        tot = R.choice([2000, 3000, 5000])
        a, b = R.randint(400, 900), R.randint(400, 900)
        if a + b >= tot:
            return None
        return mcq("Para una fiesta tenemos %s. Gastamos %s en comida y %s en bebida. ¿Cuánto dinero queda para la decoración?" % (eur(tot), eur(a), eur(b)), eur(tot - a - b),
                   [eur(a + b), eur(tot - a), eur(tot - a - b + 100), eur(tot - a + b)], "%s − %s − %s = <b>%s</b>." % (eur(tot), eur(a), eur(b), eur(tot - a - b)))
    if k == "entradas":
        ad, ni = R.choice([(850, 550), (900, 600), (1200, 700), (750, 450)])
        a, n = R.randint(1, 3), R.randint(1, 4)
        t = ad * a + ni * n
        return mcq("En el cine, la entrada de adulto cuesta %s y la de niño %s. ¿Cuánto pagan %d adulto%s y %d niño%s?" % (eur(ad), eur(ni), a, "" if a == 1 else "s", n, "" if n == 1 else "s"), eur(t),
                   [eur(ad + ni), eur((ad + ni) * (a + n)), eur(ad * n + ni * a) if ad * n + ni * a != t else eur(t + 100), eur(t - ni)],
                   "%d %s %s + %d %s %s = <b>%s</b>." % (a, POR, eur(ad), n, POR, eur(ni), eur(t)))
    if k == "oferta":
        pr = R.choice([120, 150, 180, 250, 300])
        return mcq("Una botella de zumo cuesta %s. Hay una oferta: «3 por el precio de 2». ¿Cuánto pagas por 3 botellas?" % eur(pr), eur(2 * pr), [eur(3 * pr), eur(pr), eur(2 * pr + 50), eur(3 * pr - 50)],
                   "Pagas solo 2: 2 %s %s = <b>%s</b>." % (POR, eur(pr), eur(2 * pr)))
    m = R.choice([1000, 2000])
    xs = [R.randint(150, 450) for _ in range(3)]
    t = sum(xs)
    if t >= m:
        return None
    return mcq("Para el cumpleaños de su hermano, %s compra un globo de %s, una tarjeta de %s y un juguete de %s. Paga con %s. ¿Cuánto le devuelven?" % (p, eur(xs[0]), eur(xs[1]), eur(xs[2]), eur(m)), eur(m - t),
               [eur(t), eur(m - t + 100), eur(m - xs[2]), eur(m - t - 10)], "%s; %s − %s = <b>%s</b>." % (" + ".join(eur(x) for x in xs) + " = " + eur(t), eur(m), eur(t), eur(m - t)))


def main():
    seen = set()
    sets = [
        ("Contar dinero", mix(R, seen, [(s1_contar, 20)])),
        ("Euros y céntimos", mix(R, seen, [(s1_equiv, 20)])),
        ("Comparar precios", mix(R, seen, [(s2_comparar, 12), (s4_monedas, 8)])),
        ("Compras y vueltas", mix(R, seen, [(s3_compra, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["En España usamos el <b>euro</b> (€). Hay monedas de 1, 2, 5, 10, 20 y 50 céntimos y de 1 y 2 euros, y billetes de 5, 10, 20, 50, 100, 200 y 500 euros.",
         "<b>1 € = 100 céntimos</b>. En 3,45 € hay 3 euros y 45 céntimos.",
         "Para contar dinero, empieza por los billetes y las monedas de más valor.",
         "La <b>vuelta</b> (el cambio) es lo que pagas menos lo que cuesta."],
        [("Cuesta 6,35 € y pagas con 10 €", ["10,00 − 6,35"], "te devuelven 3,65 €"),
         ("¿Cuántos céntimos son 2,50 €?", ["2 € = 200 céntimos", "200 + 50"], "250 céntimos")],
        [["Contar monedas en vez de su valor", "Tres monedas de 50 céntimos son 1,50 €, no 3 €."],
         ["Escribir 2 euros y 5 céntimos como 2,5 €", "Se escribe 2,05 €; 2,50 € son 2 euros y 50 céntimos."],
         ["Restar mal la vuelta", "Comprueba: precio + vuelta = lo que has pagado."]],
        dinero_svg([1000, 200, 50, 20]))
    faq = [("¿Cuántos céntimos tiene un euro?", "Un euro tiene 100 céntimos. Por eso 1,25 € son 125 céntimos."),
           ("¿Cómo se calcula la vuelta?", "Se resta el precio de lo que se ha pagado. Para comprobarlo, el precio más la vuelta debe dar el dinero entregado.")]
    make_unit(R, "el-dinero", "M",
              "El sistema monetario de la Unión Europea: monedas y billetes; equivalencias entre euros y céntimos; cálculos con dinero en situaciones de compra; presupuestos y ahorro",
              "El dinero: euros y céntimos", "El dinero",
              "Fichas de matemáticas de 4.º de Primaria: monedas y billetes de euro, contar dinero, euros y céntimos, comparar precios, compras, vueltas y problemas de ahorro. 100 ejercicios con soluciones.",
              "1 € = 100 céntimos", "La vuelta = lo que pagas − lo que cuesta.",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
