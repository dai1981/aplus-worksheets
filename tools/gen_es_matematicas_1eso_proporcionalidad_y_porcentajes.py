# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Proporcionalidad y porcentajes (Sentido numérico)
Razones y proporciones, magnitudes directamente proporcionales, regla de tres directa, reducción a la unidad, porcentaje de una cantidad, descuentos y aumentos, escalas.
Errores: usar regla de tres con magnitudes que no son proporcionales, calcular el 20 % dividiendo entre 20, restar el porcentaje en lugar del descuento.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, d, num, eur, unit, L, Kids, tabla

R = random.Random(47006)
K = Kids(R)


def s_razon():
    t = R.choice(["cuarto", "cuarto", "es_prop", "razon", "constante"])
    if t == "cuarto":
        a, b = R.randint(2, 12), R.randint(2, 12)
        k = R.randint(2, 9)
        c = a * k
        x = b * k
        return M("Calcula x en la proporción %d/%d = %d/x." % (a, b, c), str(x), [str(c + b - a), str(a * c // b) if (a * c) % b == 0 and a * c // b != x else str(x + 1), str(b * c)],
                 "Productos cruzados: %d · x = %d · %d, x = %d : %d = <b>%d</b>." % (a, b, c, b * c, a, x))
    if t == "es_prop":
        a, b = R.randint(2, 9), R.randint(2, 9)
        k = R.randint(2, 6)
        ok = R.random() < 0.5
        c, e = a * k, b * k + (0 if ok else R.choice([1, 2]))
        return M("¿Forman proporción %d/%d y %d/%d?" % (a, b, c, e), "sí" if ok else "no", ["no" if ok else "sí", "solo si se simplifican", "no se puede saber"],
                 "%d · %d = %d y %d · %d = %d: <b>%s</b>." % (a, e, a * e, b, c, b * c, "sí, son iguales" if ok else "no, son distintos"))
    if t == "razon":
        a, b = R.randint(8, 30), R.randint(8, 30)
        if a == b:
            return None
        g = __import__("math").gcd(a, b)
        return M("En un grupo hay %d chicas y %d chicos. ¿Cuál es la razón entre chicas y chicos, simplificada?" % (a, b), "%d/%d" % (a // g, b // g), ["%d/%d" % (b // g, a // g), "%d/%d" % (a // g, (a + b) // g), "%d/%d" % (a - b if a > b else b - a, b)],
                 "%d/%d = <b>%d/%d</b>." % (a, b, a // g, b // g))
    k = R.randint(2, 9)
    xs = R.sample(range(1, 10), 3)
    rows = [[str(x) for x in xs], [str(x * k) for x in xs]]
    return M("Dos magnitudes directamente proporcionales toman estos pares de valores: %s → %s, %s → %s, %s → %s. ¿Cuál es la constante de proporcionalidad?" % (rows[0][0], rows[1][0], rows[0][1], rows[1][1], rows[0][2], rows[1][2]),
             str(k), [str(k + 1), str(xs[0] * k + xs[1] * k), str(xs[1] * k - xs[0] * k) if xs[1] - xs[0] != 1 else str(k * 2)], "Dividimos cada valor de la segunda entre el de la primera: <b>%d</b>." % k)


def s_regla():
    t = R.choice(["precio", "receta", "coche", "sueldo"])
    k = R.randint(2, 9)
    a = R.randint(2, 9)
    b = R.randint(2, 15)
    if a == b:
        return None
    if t == "precio":
        pa = a * R.randint(80, 400)
        pb = pa * b // a
        if pa * b % a:
            return None
        return M("%d kg de naranjas cuestan %s. ¿Cuánto cuestan %d kg?" % (a, eur(pa), b), eur(pb), [eur(pa + (b - a) * 100), eur(pa * b), eur(pb + 50)], "1 kg cuesta %s; %d kg cuestan <b>%s</b>." % (eur(pa // a), b, eur(pb)))
    if t == "receta":
        per = R.randint(2, 6)
        g = R.choice([50, 75, 100, 120, 150, 200, 250])
        n = R.randint(2, 12)
        if n == per:
            return None
        r = F(g * n, per)
        if r.denominator != 1:
            return None
        return M("Una receta para %d personas lleva %d g de harina. ¿Cuántos gramos hacen falta para %d personas?" % (per, g, n), "%d g" % r, ["%d g" % (g + n - per), "%d g" % (g * n), "%d g" % (int(r) + per)], "%d : %d · %d = <b>%d g</b>." % (g, per, n, int(r)))
    if t == "coche":
        km = a * R.randint(10, 30)
        L_ = a * R.randint(2, 5)
        km2 = b * km // a
        if b * km % a:
            return None
        return M("Un coche gasta %d litros en %d km. ¿Cuántos litros gasta en %d km?" % (L_, km, km2), "%s L" % d(F(L_ * km2, km)), ["%s L" % d(F(L_ * km2, km) + 1), "%d L" % (L_ + km2 - km) if L_ + km2 - km > 0 else "%d L" % (L_ * 2), "%s L" % d(F(km2, L_)) if F(km2, L_).denominator in (1, 2, 4, 5, 10) else "%d L" % km2],
                 "Regla de tres directa: %d · %d : %d = <b>%s L</b>." % (L_, km2, km, d(F(L_ * km2, km)))) if F(L_ * km2, km).denominator in (1, 2, 4, 5, 10) else None
    h = a
    e = a * R.randint(8, 15)
    h2 = b
    r = F(e * h2, h)
    if r.denominator != 1:
        return None
    return M("Por %d horas de trabajo, %s cobra %d €. ¿Cuánto cobra por %d horas?" % (h, K.next()[0], e, h2), "%d €" % r, ["%d €" % (e + h2 - h), "%d €" % (e * h2), "%d €" % (int(r) + 10)], "%d : %d = %d € por hora; %d · %d = <b>%d €</b>." % (e, h, e // h, e // h, h2, int(r)))


def s_porc():
    t = R.choice(["de", "de", "que", "frac", "dec"])
    if t == "de":
        p = R.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 12, 8])
        n = R.choice([40, 60, 80, 120, 150, 200, 240, 300, 400, 500, 600, 800])
        r = F(p * n, 100)
        if r.denominator != 1:
            return None
        return M("Calcula el %d %% de %d." % (p, n), num(int(r)), [num(n // p) if n % p == 0 and n // p != r else num(int(r) + 10), num(n - int(r)), num(p * n)], "%d · %d : 100 = <b>%d</b>." % (p, n, int(r)))
    if t == "que":
        n = R.choice([20, 25, 40, 50, 80, 200])
        p = R.choice([10, 20, 25, 40, 50, 75])
        part = p * n // 100
        if p * n % 100:
            return None
        return M("¿Qué porcentaje de %d es %d?" % (n, part), "%d %%" % p, ["%d %%" % part, "%d %%" % (100 - p), "%d %%" % (p * 2) if p * 2 <= 100 else "%d %%" % (p // 2)], "%d : %d = %s = <b>%d %%</b>." % (part, n, d(F(part, n)), p))
    if t == "frac":
        f, p = R.choice([(F(1, 2), 50), (F(1, 4), 25), (F(3, 4), 75), (F(1, 5), 20), (F(2, 5), 40), (F(1, 10), 10), (F(3, 10), 30), (F(1, 20), 5), (F(3, 5), 60), (F(7, 10), 70)])
        from es_eso import fq
        return M("¿Qué porcentaje equivale a %s?" % fq(f), "%d %%" % p, ["%d %%" % (f.numerator * 10 + f.denominator), "%d %%" % (100 - p), "%d %%" % f.denominator], "%s = %s = <b>%d %%</b>." % (fq(f), d(F(p, 100)), p))
    p = R.randint(1, 99)
    return M("¿Qué número decimal es el %d %%?" % p, d(F(p, 100)), [d(F(p, 10)), str(p), d(F(p, 1000))], "%d %% = %d/100 = <b>%s</b>." % (p, p, d(F(p, 100))))


def s_desc():
    p = R.choice([10, 15, 20, 25, 30, 40, 50])
    pr = R.choice([20, 30, 40, 50, 60, 80, 120, 150, 200, 250])
    t = R.choice(["desc", "desc", "aum", "escala"])
    if t == "desc":
        r = F(pr * (100 - p), 100)
        if r.denominator != 1:
            return None
        return M("Unas zapatillas cuestan %d € y tienen un descuento del %d %%. ¿Cuánto cuestan ahora?" % (pr, p), "%d €" % r, ["%d €" % (pr * p // 100), "%d €" % (pr - p), "%d €" % (pr + pr * p // 100)], "Descuento: %d €. Precio final: %d − %d = <b>%d €</b>." % (pr * p // 100, pr, pr * p // 100, int(r)))
    if t == "aum":
        p = R.choice([5, 10, 20, 25])
        r = F(pr * (100 + p), 100)
        if r.denominator != 1:
            return None
        return M("Un abono de %d € sube un %d %%. ¿Cuánto cuesta ahora?" % (pr, p), "%d €" % r, ["%d €" % (pr * p // 100), "%d €" % (pr + p), "%d €" % (pr - pr * p // 100)], "Aumento: %d €. Nuevo precio: <b>%d €</b>." % (pr * p // 100, int(r)))
    e = R.choice([100, 200, 500, 1000, 50000, 100000])
    cm = R.randint(2, 15)
    real = cm * e
    from es_eso import num as n_
    if real >= 100000:
        ok = "%s km" % n_(real // 100000) if real % 100000 == 0 else "%s m" % n_(real // 100)
    else:
        ok = "%s m" % d(F(real, 100))
    return M("En un plano a escala 1 : %s, una distancia mide %d cm. ¿Cuánto mide en la realidad?" % (n_(e), cm), ok, ["%s m" % d(F(real, 1000)), "%s m" % d(F(real, 10)), "%d cm" % (cm + e)] if real < 100000 else ["%s m" % n_(real // 1000), "%s km" % n_(real // 1000), "%d cm" % (cm + e)],
             "%d · %s = %s cm = <b>%s</b>." % (cm, n_(e), n_(real), ok))


def s_problema():
    p = K.next()[0]
    t = R.choice(["iva", "aprob", "obreros", "rebaja", "ahorro"])
    if t == "iva":
        b = R.choice([100, 200, 300, 400, 500, 1000])
        r = b * 121 // 100
        return M("Un patinete cuesta %d € sin IVA. Con un IVA del 21 %%, ¿cuánto cuesta?" % b, "%d €" % r, ["%d €" % (b + 21), "%d €" % (b * 21 // 100), "%d €" % (b - b * 21 // 100)], "21 %% de %d = %d; %d + %d = <b>%d €</b>." % (b, b * 21 // 100, b, b * 21 // 100, r))
    if t == "aprob":
        n = R.choice([20, 25, 28, 30])
        a = R.randint(n // 2, n)
        pc = F(100 * a, n)
        if pc.denominator != 1:
            return None
        return M("En una clase de %d alumnos han aprobado %d. ¿Qué porcentaje ha aprobado?" % (n, a), "%d %%" % pc, ["%d %%" % a, "%d %%" % (100 - pc), "%d %%" % (pc + 5) if pc <= 95 else "%d %%" % (pc - 10)], "%d : %d = %s → <b>%d %%</b>." % (a, n, d(F(a, n)), int(pc)))
    if t == "rebaja":
        pr = R.choice([40, 60, 80, 100, 120, 200])
        fin = R.choice([x for x in range(pr // 2, pr, 2) if (pr - x) * 100 % pr == 0])
        p = (pr - fin) * 100 // pr
        return M("Un abrigo costaba %d € y ahora cuesta %d €. ¿Qué descuento se ha aplicado?" % (pr, fin), "%d %%" % p, ["%d %%" % (pr - fin), "%d %%" % (100 - p), "%d %%" % (p + 5)], "Descuento de %d € sobre %d €: %d : %d = <b>%d %%</b>." % (pr - fin, pr, pr - fin, pr, p))
    if t == "ahorro":
        s_ = R.choice([800, 1000, 1200, 1500, 2000])
        pc = R.choice([10, 15, 20, 25])
        r = s_ * pc // 100
        return M("%s gana %s € al mes y ahorra el %d %%. ¿Cuánto ahorra cada mes?" % (p, num(s_), pc), "%d €" % r, ["%d €" % (s_ // pc), "%s €" % num(s_ - r), "%d €" % (r + 10)], "%d %% de %s = <b>%d €</b>." % (pc, num(s_), r))
    v = R.randint(2, 6)
    km = v * R.randint(20, 60)
    t2 = R.randint(2, 8)
    if t2 == v:
        return None
    return M("Un ciclista recorre %d km en %d horas a velocidad constante. ¿Cuántos km recorre en %d horas?" % (km, v, t2), "%d km" % (km // v * t2), ["%d km" % (km + t2 - v), "%d km" % (km * t2), "%d km" % (km // v)], "%d : %d = %d km cada hora; %d · %d = <b>%d km</b>." % (km, v, km // v, km // v, t2, km // v * t2))


seen = set()
sets = [("Razones y proporciones", mix(R, seen, [(s_razon, 20)])), ("Regla de tres directa", mix(R, seen, [(s_regla, 20)])), ("Porcentajes", mix(R, seen, [(s_porc, 20)])),
        ("Descuentos, aumentos y escalas", mix(R, seen, [(s_desc, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
body = L(["Dos magnitudes son <b>directamente proporcionales</b> si al multiplicar una por un número, la otra queda multiplicada por el mismo número.",
          "En una <b>proporción</b> a/b = c/d, los productos cruzados son iguales: a · d = b · c.",
          "El <b>porcentaje</b> es una fracción de denominador 100: el 20 % de 150 es 20 · 150 : 100 = 30."],
         [("3 kg cuestan 7,50 €. ¿Cuánto cuestan 5 kg?", ["1 kg cuesta 2,50 €", "5 · 2,50"], "12,50 €"), ("Descuento del 15 % sobre 80 €", ["15 % de 80 = 12", "80 − 12"], "68 €")],
         [["Usar la regla de tres cuando no hay proporcionalidad", "La edad y la altura no son proporcionales."], ["Calcular el 20 % dividiendo entre 20", "20 % es multiplicar por 20 y dividir entre 100."], ["Dar el descuento como precio final", "Resta el descuento al precio."]],
         tabla(["Porcentaje", "50 %", "25 %", "20 %", "10 %"], [["Fracción", "1/2", "1/4", "1/5", "1/10"]]))
faq = [("¿Cómo se calcula un porcentaje?", "Se multiplica la cantidad por el porcentaje y se divide entre 100."), ("¿Qué es una escala 1 : 1000?", "Que 1 cm en el plano son 1000 cm (10 m) en la realidad.")]
unit(1, R, "proporcionalidad-y-porcentajes", "N", "Razones y proporciones; magnitudes directamente proporcionales; regla de tres y reducción a la unidad; porcentajes, descuentos y aumentos; escalas",
     "Proporcionalidad y porcentajes", "Proporcionalidad",
     "Fichas de matemáticas de 1.º de ESO: razones, proporciones, regla de tres directa, porcentajes, descuentos, IVA y escalas. 100 ejercicios con soluciones.",
     "a/b = c/d ⇔ a · d = b · c", "El 20 % es 20 de cada 100.", body, faq, sets, 6)
