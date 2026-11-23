# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Recuento, tablas y gráficos (Sentido estocástico)
build(lv): lv = 1 → «recuento-y-graficos»: contar y clasificar, marcas de recuento, pictogramas de 1 en 1, ¿cuántos más?;
lv = 2 → «graficos-y-tablas»: también tablas, gráficos de barras y pictogramas en que cada dibujo vale 2 (reutiliza 4.º con números hasta 100).
Errores: contar dos veces el mismo dibujo, leer mal la escala, confundir «cuántos más» con el total.
"""
import random
from es_common import mcq, mix, lesson, make_unit, grafico
from es_low import src
from f_common import pictograph_svg
import es_pics as P
import k_pics

R = None
LV = 2


def tally(n):
    g, r = divmod(n, 5)
    return " ".join(["<s>||||</s>"] * g + (["|" * r] if r else []))


def s_picto():
    ks = R.sample(P.KINDS, R.choice([3, 4]))
    vals = [R.randint(1, 9) for _ in ks]
    pic = P.pic(pictograph_svg(list(zip(ks, vals))), "pictograma: " + ", ".join(P.cosas(k, v) for k, v in zip(ks, vals)))
    t = R.choice(["cuantos", "mas", "menos", "dif", "total"])
    if t == "cuantos":
        i = R.randrange(len(ks))
        return mcq(pic + "%s %s hay?" % (P.cuantos(ks[i]), P.nombre(ks[i])), str(vals[i]), [str(vals[i] + 1), str(vals[i] - 1) if vals[i] > 1 else str(vals[i] + 2), str(sum(vals))], "Contamos los dibujos de esa fila: <b>%d</b>." % vals[i])
    if t in ("mas", "menos"):
        f = max if t == "mas" else min
        if vals.count(f(vals)) > 1:
            return None
        i = vals.index(f(vals))
        ok = P.nombre(ks[i])
        return mcq(pic + "¿De qué hay %s?" % ("más" if t == "mas" else "menos"), ok, [P.nombre(k) for k in ks if k != ks[i]] + ["de todo igual"], "La fila más %s es la de las %s: <b>%s</b>." % ("larga" if t == "mas" else "corta", ok, ok) if P.fem(ks[i]) else
                   "La fila más %s es la de los %s: <b>%s</b>." % ("larga" if t == "mas" else "corta", ok, ok))
    if t == "dif":
        i, j = R.sample(range(len(ks)), 2)
        if vals[i] <= vals[j]:
            i, j = j, i
        if vals[i] == vals[j]:
            return None
        d = vals[i] - vals[j]
        return mcq(pic + "%s %s más que %s hay?" % (P.cuantos(ks[i]), P.nombre(ks[i]), P.nombre(ks[j])), str(d), [str(vals[i] + vals[j]), str(d + 1), str(vals[i])], "%d − %d = <b>%d</b>." % (vals[i], vals[j], d))
    s = sum(vals)
    return mcq(pic + "¿Cuántos dibujos hay en total?", str(s), [str(s + 1), str(s - 1), str(max(vals))], "%s = <b>%d</b>." % (" + ".join(map(str, vals)), s))


def s_marcas():
    n = R.randint(3, 19)
    t = R.choice(["leer", "escribir"])
    if t == "leer":
        return mcq("¿Qué número indican estas marcas de recuento? <span class='nw'>%s</span>" % tally(n), str(n), [str(n + 1), str(n - 1), str(n + 5) if n + 5 <= 25 else str(n - 5)], "Cada grupo tachado vale 5: <b>%d</b>." % n)
    if n % 5 not in (1, 2, 3):
        return None
    w = [tally(x) for x in (n + 1, n - 1, n + 5 if n < 15 else n - 5)]
    return mcq("¿Cómo se escribe %d con marcas de recuento?" % n, tally(n), w, "Grupos de 5 y lo que sobra: <b>%s</b>." % tally(n))


def s_clasificar():
    ks = R.sample(P.KINDS, 3)
    counts = [R.randint(1, 6) for _ in ks]
    sv = k_pics.mixed_svg(list(zip(ks, counts)), R.randint(1, 9999))
    pic = P.pic(sv, "dibujos mezclados")
    t = R.choice(["cuantos", "total", "mas"])
    if t == "cuantos":
        i = R.randrange(3)
        return mcq(pic + "%s %s hay?" % (P.cuantos(ks[i]), P.nombre(ks[i])), str(counts[i]), [str(counts[i] + 1), str(counts[i] - 1) if counts[i] > 1 else str(counts[i] + 2), str(sum(counts))], "Contamos solo los dibujos iguales: <b>%d</b>." % counts[i])
    if t == "total":
        return mcq(pic + "¿Cuántos dibujos hay en total?", str(sum(counts)), [str(sum(counts) + 1), str(sum(counts) - 1), str(max(counts))], "%s = <b>%d</b>." % (" + ".join(map(str, counts)), sum(counts)))
    if counts.count(max(counts)) > 1:
        return None
    i = counts.index(max(counts))
    return mcq(pic + "¿De qué hay más?", P.nombre(ks[i]), [P.nombre(k) for k in ks if k != ks[i]] + ["hay lo mismo de todo"], "Hay %d: <b>%s</b>." % (counts[i], P.nombre(ks[i])))


def s_barras():
    dep = R.random() < 0.5
    names = R.sample(["fútbol", "baloncesto", "natación", "tenis", "patinaje", "ciclismo"], 4) if dep else R.sample(["perro", "gato", "pez", "pájaro", "conejo", "tortuga"], 4)
    tit = "Deporte favorito de los alumnos de la clase. " if dep else "Animal favorito de los alumnos de la clase. "
    vals = [R.randint(1, 10) for _ in names]
    pic = grafico(list(zip(names, vals)), "alumnos")
    t = R.choice(["cuantos", "mas", "dif"])
    if t == "cuantos":
        i = R.randrange(4)
        return mcq(pic + tit + "¿Cuántos alumnos eligieron %s?" % names[i], str(vals[i]), [str(vals[i] + 1), str(vals[i] - 1) if vals[i] > 1 else str(vals[i] + 2), str(max(vals)) if max(vals) != vals[i] else str(vals[i] + 2)], "La barra llega al <b>%d</b>." % vals[i])
    if t == "mas":
        if vals.count(max(vals)) > 1:
            return None
        i = vals.index(max(vals))
        return mcq(pic + tit + "¿Qué fue lo más elegido?", names[i], [x for x in names if x != names[i]], "La barra más alta: <b>%s</b>." % names[i])
    i, j = R.sample(range(4), 2)
    if vals[i] <= vals[j]:
        return None
    return mcq(pic + tit + "¿Cuántos alumnos más eligieron %s que %s?" % (names[i], names[j]), str(vals[i] - vals[j]), [str(vals[i] + vals[j]), str(vals[i] - vals[j] + 1), str(vals[i])], "%d − %d = <b>%d</b>." % (vals[i], vals[j], vals[i] - vals[j]))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30020 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("Contar y clasificar", mix(R, seen, [(s_clasificar, 20)])), ("Marcas de recuento", mix(R, seen, [(s_marcas, 20)])), ("Pictogramas", mix(R, seen, [(s_picto, 20)])),
                ("Gráficos de barras", mix(R, seen, [(s_barras, 20)])), ("Repaso", mix(R, seen, [(s_picto, 8), (s_clasificar, 6), (s_barras, 6)]))]
        think = ["Para contar muchas cosas, sepáralas por grupos: las iguales juntas.", "Las <b>marcas de recuento</b> se hacen de 5 en 5: cuatro palitos y uno que los tacha.",
                 "En un <b>pictograma</b>, cada dibujo es una cosa. La fila más larga es la que tiene más."]
        ex = [("<s>||||</s> ||", ["Un grupo de 5 y 2 más"], "7"), ("5 perros y 3 gatos", ["5 − 3"], "2 perros más")]
        kb, ks = "Marcas de 5 en 5", "Cuatro palitos y uno que los tacha."
        meta = "Fichas de matemáticas de 1.º de Primaria: contar y clasificar, marcas de recuento, pictogramas y gráficos de barras sencillos. 100 ejercicios con soluciones."
        std = "Recogida y clasificación de datos; recuento con marcas; pictogramas y gráficos de barras sencillos"
        slug, title, short = "recuento-y-graficos", "Recuento y gráficos", "Recuento y gráficos"
        sort = 14
    else:
        tab, bar, pic = src("graficos_y_tablas", 32920, "s3_tablas", "s1_barras", "s2_picto", mx=100, rep=[("4.º", "2.º")])
        sets = [("Marcas de recuento y tablas", mix(R, seen, [(s_marcas, 6), (tab, 14)])), ("Pictogramas", mix(R, seen, [(s_picto, 20)])), ("Pictogramas con leyenda", mix(R, seen, [(pic, 20)])),
                ("Gráficos de barras", mix(R, seen, [(s_barras, 10), (bar, 10)])), ("Repaso con datos", mix(R, seen, [(bar, 8), (tab, 6), (s_picto, 6)]))]
        think = ["Con <b>marcas de recuento</b> contamos de 5 en 5. Luego escribimos el número en una <b>tabla</b>.", "En un gráfico de barras, mira hasta qué número llega cada barra.",
                 "En un pictograma, lee la <b>leyenda</b>: si cada dibujo vale 2, tres dibujos son 6."]
        ex = [("Cada dibujo vale 2 y hay 4 dibujos", ["2 + 2 + 2 + 2"], "8"), ("Barra de fútbol en 9 y de tenis en 4", ["9 − 4"], "5 más")]
        kb, ks = "Lee la leyenda y la escala", "Si un dibujo vale 2, cuenta de 2 en 2."
        meta = "Fichas de matemáticas de 2.º de Primaria: marcas de recuento, tablas, pictogramas y gráficos de barras. 100 ejercicios con soluciones."
        std = "Recogida y organización de datos: recuento, tablas, pictogramas y gráficos de barras; interpretación"
        slug, title, short = "graficos-y-tablas", "Gráficos y tablas", "Gráficos y tablas"
        sort = 17
    mist = [["Contar dos veces el mismo dibujo", "Tacha cada dibujo al contarlo."], ["Leer mal la escala", "Mira de cuánto en cuánto va."], ["Confundir «cuántos más» con el total", "«Cuántos más» es una resta."]]
    body = lesson(think, ex, mist, P.pic(pictograph_svg([("apple", 5), ("star", 3), ("fish", 4)]), "pictograma: 5 manzanas, 3 estrellas, 4 peces"))
    faq = [("¿Qué son las marcas de recuento?", "Palitos que se hacen al contar. Cada cinco se agrupan: cuatro palitos y uno que los tacha."), ("¿Qué es un pictograma?", "Un gráfico con dibujos. Cada dibujo representa una cantidad.")]
    make_unit(R, slug, "S", std, title, short, meta, kb, ks, body, faq, sets, sort, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
