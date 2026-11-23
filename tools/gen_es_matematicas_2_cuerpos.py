# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Cuerpos geométricos (Sentido espacial)
build(lv): lv = 1 → cubo, prisma (caja), pirámide, esfera, cilindro y cono; ruedan o no ruedan; objetos de casa;
lv = 2 → también caras, aristas y vértices del cubo y del prisma, caras planas y curvas, huellas de las caras.
Errores: llamar «cuadrado» al cubo o «círculo» a la esfera, pensar que el cilindro no rueda.
"""
import random
from es_common import mcq, mix, lesson, make_unit, cuerpo_svg

R = None
LV = 2
NOM = {"cubo": "cubo", "prisma": "prisma", "piramide": "pirámide", "esfera": "esfera", "cilindro": "cilindro", "cono": "cono"}
PLANO = {"cubo": "cuadrado", "esfera": "círculo", "cilindro": "rectángulo", "cono": "triángulo", "prisma": "rectángulo", "piramide": "triángulo"}
COLS = ["#cfe6d6", "#f6d8b8", "#d6e2f6", "#f3d1dc", "#fff2b3"]
RUEDA = {"esfera": "sí, rueda", "cilindro": "sí, rueda", "cono": "sí, rueda en círculo", "cubo": "no, no rueda", "prisma": "no, no rueda", "piramide": "no, no rueda"}
OBJ = [("un balón", "esfera"), ("una canica", "esfera"), ("una naranja", "esfera"), ("un dado", "cubo"), ("un terrón de azúcar", "cubo"), ("una lata de refresco", "cilindro"),
       ("un rollo de papel", "cilindro"), ("una vela", "cilindro"), ("un cucurucho de helado", "cono"), ("un gorro de fiesta", "cono"), ("un cono de tráfico", "cono"),
       ("una caja de zapatos", "prisma"), ("un brik de leche", "prisma"), ("un libro", "prisma"), ("una tienda de campaña", "pirámide"), ("el tejado de una torre", "pirámide")]


def art(n):
    return "una" if n in ("esfera", "pirámide") else "un"


def s_nombre():
    k = R.choice(list(NOM))
    nm = NOM[k]
    return mcq(cuerpo_svg(k, color=R.choice(COLS)) + "¿Cómo se llama este cuerpo?", nm, [PLANO[k]] + [NOM[x] for x in NOM if x != k], "Es %s <b>%s</b>." % (art(nm), nm))


def s_objeto():
    o, k = R.choice(OBJ)
    k = k.replace("pirámide", "piramide")
    nm = NOM[k]
    return mcq("¿Qué forma tiene %s?" % o, nm, [PLANO[k]] + [NOM[x] for x in NOM if x != k], "%s tiene forma de <b>%s</b>." % (o[0].upper() + o[1:], nm))


def s_rueda():
    k = R.choice(list(NOM))
    t = R.choice(["rueda", "planas"]) if LV == 2 else "rueda"
    if t == "rueda":
        ok = RUEDA[k]
        return mcq(cuerpo_svg(k, color=R.choice(COLS)) + "Si empujamos este cuerpo, ¿rueda?", ok, [x for x in ("sí, rueda", "no, no rueda", "sí, rueda en círculo", "solo si es pequeño") if x != ok],
                   "Ruedan los cuerpos que tienen una parte curva. Respuesta: <b>%s</b>." % ok)
    ok = {"cubo": "todas planas", "prisma": "todas planas", "piramide": "todas planas", "esfera": "solo curva", "cilindro": "planas y curva", "cono": "planas y curva"}[k]
    if k == "cono":
        ok = "una plana y una curva"
    opts = ["todas planas", "solo curva", "planas y curva", "una plana y una curva"]
    return mcq(cuerpo_svg(k, color=R.choice(COLS)) + "¿Cómo son las superficies de %s %s?" % ("este" if k not in ("esfera", "piramide") else "esta", NOM[k]), ok, [x for x in opts if x != ok], "Respuesta: <b>%s</b>." % ok)


def s_saber():
    items = [("¿Qué cuerpo tiene forma de pelota?", "la esfera", ["el cubo", "el cono", "el círculo"]),
             ("¿Qué cuerpo tiene 6 caras cuadradas iguales?", "el cubo", ["el prisma", "la pirámide", "el cilindro"]),
             ("¿Qué cuerpo tiene una punta y una base redonda?", "el cono", ["el cilindro", "la pirámide", "la esfera"]),
             ("¿Qué cuerpo tiene dos bases redondas?", "el cilindro", ["el cono", "la esfera", "el cubo"]),
             ("¿Qué cuerpo no tiene ninguna parte plana?", "la esfera", ["el cilindro", "el cono", "el cubo"]),
             ("¿Cuál es una figura plana y no un cuerpo?", "el cuadrado", ["el cubo", "la esfera", "el cono"]),
             ("¿Cuál de estos cuerpos se puede apilar bien, uno encima de otro?", "el cubo", ["la esfera", "el cono", "una pelota"]),
             ("¿Qué cuerpo tiene una base y caras de triángulo que acaban en punta?", "la pirámide", ["el prisma", "el cono", "el cubo"])]
    if LV == 2:
        items += [("¿Cuántas caras tiene un cubo?", "6", ["4", "8", "12"]), ("¿Cuántos vértices (esquinas) tiene un cubo?", "8", ["6", "4", "12"]),
                  ("¿Cuántas aristas tiene un cubo?", "12", ["6", "8", "10"]), ("¿Cuántas caras tiene una caja de zapatos?", "6", ["4", "5", "8"]),
                  ("¿Qué huella deja la base de un cilindro si la pintamos y la estampamos?", "un círculo", ["un cuadrado", "un triángulo", "un rectángulo"]),
                  ("¿Qué huella deja una cara de un cubo?", "un cuadrado", ["un círculo", "un triángulo", "un rectángulo"]),
                  ("¿Qué huella deja la base de un cono?", "un círculo", ["un triángulo", "un cuadrado", "un punto"]),
                  ("¿Cómo se llaman las líneas donde se juntan dos caras de un cubo?", "aristas", ["vértices", "bases", "lados curvos"]),
                  ("¿Cómo se llaman las esquinas de un cuerpo?", "vértices", ["aristas", "caras", "bases"]),
                  ("¿Cuántas bases tiene un cilindro?", "2", ["1", "3", "0"]), ("¿Cuántas bases tiene un cono?", "1", ["2", "0", "3"])]
    q, a, w = R.choice(items)
    return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_cuantos():
    ks = [R.choice(list(NOM)) for _ in range(R.randint(5, 7))]
    target = R.choice(ks)
    n = ks.count(target)
    import re

    def inner(svg):
        return re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    s = "".join("<g transform='translate(%d,0)'>%s</g>" % (i * 70, inner(cuerpo_svg(k, r=26, color=COLS[i % 5]))) for i, k in enumerate(ks))
    h = float(re.search(r"viewBox='0 0 [\d.]+ ([\d.]+)'", cuerpo_svg("cubo", r=26)).group(1))
    pic = "<div class='qfig'><svg viewBox='0 0 %d %d' width='%d' role='img' aria-label='cuerpos geométricos'>%s</svg></div>" % (70 * len(ks) + 10, h, 70 * len(ks) + 10, s)
    nm = NOM[target]
    pl = {"cubo": "cubos", "prisma": "prismas", "piramide": "pirámides", "esfera": "esferas", "cilindro": "cilindros", "cono": "conos"}[target]
    return mcq(pic + "¿Cuántos %s hay?" % pl if nm not in ("esfera", "pirámide") else pic + "¿Cuántas %s hay?" % pl, str(n), [str(n + 1), str(n - 1) if n > 1 else str(n + 2), str(len(ks))], "Hay <b>%d</b> %s." % (n, pl if n != 1 else nm))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30018 + lv * 1000)
    seen = set()
    sets = [("¿Cómo se llama?", mix(R, seen, [(s_nombre, 20)])), ("Objetos de casa", mix(R, seen, [(s_objeto, 16), (s_saber, 4)])), ("¿Rueda o no rueda?" if lv == 1 else "Caras planas y curvas", mix(R, seen, [(s_rueda, 20)])),
            ("Contar cuerpos", mix(R, seen, [(s_cuantos, 20)])), ("Repaso" if lv == 1 else "Caras, aristas y vértices", mix(R, seen, [(s_saber, 12), (s_cuantos, 8)] if lv == 2 else [(s_saber, 4), (s_rueda, 6), (s_cuantos, 10)]))]
    if lv == 1:
        think = ["Los <b>cuerpos</b> no son planos: se pueden coger con la mano.", "La <b>esfera</b> es como una pelota. El <b>cubo</b>, como un dado. El <b>cilindro</b>, como una lata. El <b>cono</b>, como un cucurucho.",
                 "Los cuerpos con partes curvas <b>ruedan</b>. Los que solo tienen caras planas, no."]
        kb, ks = "Esfera, cubo, cilindro y cono", "Lo que tiene partes curvas rueda."
        meta = "Fichas de matemáticas de 1.º de Primaria: esfera, cubo, cilindro, cono, prisma y pirámide, ruedan o no ruedan y objetos de casa. 100 ejercicios con soluciones."
        std = "Cuerpos geométricos: esfera, cubo, prisma, pirámide, cilindro y cono; reconocimiento en objetos del entorno"
    else:
        think = ["Los <b>cuerpos geométricos</b> ocupan espacio. Tienen <b>caras</b>, <b>aristas</b> (donde se juntan dos caras) y <b>vértices</b> (esquinas).",
                 "El cubo, el prisma y la pirámide tienen todas sus caras planas. La esfera, el cilindro y el cono tienen partes curvas.", "Si estampas una cara, su huella es una figura plana: el cubo deja un cuadrado."]
        kb, ks = "Caras, aristas y vértices", "Cubo: 6 caras, 12 aristas, 8 vértices."
        meta = "Fichas de matemáticas de 2.º de Primaria: cubo, prisma, pirámide, esfera, cilindro y cono, caras, aristas y vértices. 100 ejercicios con soluciones."
        std = "Cuerpos geométricos: elementos (caras, aristas, vértices); superficies planas y curvas; reconocimiento en el entorno"
    ex = [("Un dado", ["6 caras cuadradas iguales"], "cubo"), ("Una lata de refresco", ["Dos bases redondas y una parte curva"], "cilindro")]
    mist = [["Llamar «cuadrado» al cubo", "El cuadrado es plano; el cubo es un cuerpo."], ["Llamar «círculo» a la esfera", "El círculo es plano; la esfera es como una pelota."], ["Pensar que el cilindro no rueda", "Tumbado, rueda."]]
    body = lesson(think, ex, mist, cuerpo_svg("cilindro"))
    faq = [("¿Qué diferencia hay entre el cubo y el cuadrado?", "El cuadrado es una figura plana. El cubo es un cuerpo con 6 caras cuadradas."), ("¿Qué cuerpos ruedan?", "Los que tienen alguna parte curva: la esfera, el cilindro y el cono.")]
    make_unit(R, "cuerpos-geometricos", "E", std, "Cuerpos geométricos", "Cuerpos geométricos", meta, kb, ks, body, faq, sets, 12 if lv == 1 else 15, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
