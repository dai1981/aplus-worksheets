# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Cuerpos geométricos (Sentido espacial)
Poliedros (cubo, prismas y pirámides) y cuerpos redondos (cilindro, cono y esfera); caras, aristas y vértices;
la base de prismas y pirámides; objetos de la vida diaria; desarrollos planos.
Errores: confundir el prisma y la pirámide, contar las caras de un cuerpo redondo como en un poliedro, llamar «cuadrado» al cubo.
"""
import random
from es_common import mcq, mix, lesson, make_unit, cuerpo_svg, bank

R = random.Random(44021)
KIND = {"cubo": "cubo", "prisma": "prisma rectangular (ortoedro)", "esfera": "esfera", "cilindro": "cilindro", "cono": "cono", "piramide": "pirámide"}
DATA = {  # caras, aristas, vértices
    "cubo": (6, 12, 8), "prisma rectangular": (6, 12, 8), "prisma triangular": (5, 9, 6), "prisma pentagonal": (7, 15, 10), "prisma hexagonal": (8, 18, 12),
    "pirámide cuadrangular": (5, 8, 5), "pirámide triangular": (4, 6, 4), "pirámide pentagonal": (6, 10, 6), "pirámide hexagonal": (7, 12, 7),
}


def s1_nombre():
    k = R.choice(list(KIND))
    nm = KIND[k]
    w = [KIND[x] for x in KIND if x != k]
    near = {"cubo": ["cuadrado", "prisma rectangular (ortoedro)"], "prisma": ["cubo", "pirámide"], "esfera": ["círculo", "cilindro"], "cilindro": ["cono", "círculo"], "cono": ["pirámide", "cilindro"], "piramide": ["prisma rectangular (ortoedro)", "cono"]}[k]
    return mcq(cuerpo_svg(k, color=R.choice(["#cfe6d6", "#f6d8b8", "#d6e2f6", "#f3d1dc"])) + "¿Cómo se llama este cuerpo geométrico?", nm, near + w, "Es %s <b>%s</b>." % ("una" if nm in ("esfera", "pirámide") else "un", nm))


def s1_tipo():
    k = R.choice(list(KIND))
    poly = k in ("cubo", "prisma", "piramide")
    return mcq(cuerpo_svg(k, color=R.choice(["#cfe6d6", "#f6d8b8"])) + "¿Es un poliedro o un cuerpo redondo?", "poliedro" if poly else "cuerpo redondo", ["cuerpo redondo" if poly else "poliedro", "figura plana", "polígono"],
               "%s: es un <b>%s</b>." % ("Todas sus caras son planas (polígonos)" if poly else "Tiene alguna superficie curva", "poliedro" if poly else "cuerpo redondo"))


def s2_contar():
    c = R.choice(list(DATA))
    k = R.choice([0, 1, 2])
    w = ["caras", "aristas", "vértices"][k]
    v = DATA[c][k]
    others = [DATA[c][i] for i in range(3) if i != k]
    art = "un" if c in ("cubo",) or c.startswith("prisma") else "una"
    return mcq("¿Cuántas %s tiene %s %s?" % (w, art, c) if w != "vértices" else "¿Cuántos vértices tiene %s %s?" % (art, c), str(v), [str(x) for x in others] + [str(v + 1), str(v - 1), str(v + 2)],
               "%s %s tiene %d caras, %d aristas y %d vértices: <b>%d</b>." % (art.capitalize(), c, DATA[c][0], DATA[c][1], DATA[c][2], v))


def s2_dibujo():
    k = R.choice(["cubo", "prisma", "piramide"])
    nm = {"cubo": "cubo", "prisma": "prisma rectangular", "piramide": "pirámide cuadrangular"}[k]
    i = R.choice([0, 1, 2])
    w = ["caras", "aristas", "vértices"][i]
    v = DATA[nm][i]
    q = "¿Cuántos vértices tiene este cuerpo?" if w == "vértices" else "¿Cuántas %s tiene este cuerpo?" % w
    return mcq(cuerpo_svg(k) + q, str(v),
               [str(DATA[nm][j]) for j in range(3) if j != i] + [str(v + 2), str(v - 1)], "Es %s %s: <b>%d %s</b>." % ("una" if k == "piramide" else "un", nm, v, w))


def s3_prop():
    return bank(R, [
        ("¿Qué forma tienen las caras de un cubo?", "cuadrados", ["rectángulos", "triángulos", "círculos"]),
        ("¿Qué forma tienen las caras laterales de una pirámide?", "triángulos", ["rectángulos", "cuadrados", "círculos"]),
        ("¿Qué forma tienen las caras laterales de un prisma?", "rectángulos", ["triángulos", "círculos", "pentágonos"]),
        ("¿Cuántas bases tiene un prisma?", "2", ["1", "0", "4"]),
        ("¿Cuántas bases tiene una pirámide?", "1", ["2", "0", "3"]),
        ("¿Cuántas bases tiene un cilindro?", "2", ["1", "0", "3"]),
        ("¿Qué forma tienen las bases de un cilindro?", "círculos", ["cuadrados", "triángulos", "rectángulos"]),
        ("¿Qué cuerpo tiene una base circular y un vértice?", "el cono", ["el cilindro", "la esfera", "la pirámide"]),
        ("¿Qué cuerpo no tiene ni caras planas, ni aristas, ni vértices?", "la esfera", ["el cono", "el cilindro", "el cubo"]),
        ("Una pirámide con base hexagonal se llama…", "pirámide hexagonal", ["prisma hexagonal", "hexágono", "pirámide cuadrangular"]),
        ("Un prisma con bases triangulares se llama…", "prisma triangular", ["pirámide triangular", "triángulo", "prisma cuadrangular"]),
        ("¿Cómo se llama la línea donde se juntan dos caras de un poliedro?", "arista", ["vértice", "base", "lado"]),
        ("¿Cómo se llama el punto donde se juntan varias aristas?", "vértice", ["arista", "cara", "centro"]),
        ("¿Qué cuerpo puede rodar en cualquier dirección?", "la esfera", ["el cilindro", "el cubo", "el cono"]),
        ("¿En qué se diferencian un prisma y una pirámide?", "el prisma tiene 2 bases y la pirámide 1", ["la pirámide tiene más caras siempre", "el prisma no tiene aristas", "no hay diferencia"]),
        ("¿Cuántas caras iguales tiene un cubo?", "6", ["4", "8", "12"]),
    ], "prop")()


def s4_objetos():
    return bank(R, [
        ("¿Qué forma tiene un balón de fútbol?", "esfera", ["cilindro", "cono", "círculo"]),
        ("¿Qué forma tiene una lata de refresco?", "cilindro", ["cono", "prisma", "esfera"]),
        ("¿Qué forma tiene un dado?", "cubo", ["pirámide", "cilindro", "cuadrado"]),
        ("¿Qué forma tiene un cucurucho de helado?", "cono", ["cilindro", "pirámide", "esfera"]),
        ("¿Qué forma tiene una caja de zapatos?", "prisma rectangular (ortoedro)", ["cubo", "pirámide", "rectángulo"]),
        ("¿Qué forma tienen las pirámides de Egipto?", "pirámide cuadrangular", ["prisma triangular", "cono", "triángulo"]),
        ("¿Qué forma tiene un brik de leche?", "prisma rectangular (ortoedro)", ["cilindro", "cono", "pirámide"]),
        ("¿Qué forma tiene una naranja, aproximadamente?", "esfera", ["cilindro", "cono", "círculo"]),
        ("¿Qué forma tiene un rollo de papel de cocina?", "cilindro", ["esfera", "cono", "prisma"]),
        ("¿Qué forma tiene un gorro de cumpleaños?", "cono", ["cilindro", "pirámide", "triángulo"]),
        ("¿Qué forma tiene una tienda de campaña canadiense (con dos paredes inclinadas)?", "prisma triangular", ["pirámide", "cono", "cubo"]),
        ("¿Qué forma tiene un cubito de hielo?", "cubo", ["esfera", "cilindro", "cuadrado"]),
        ("¿Qué forma tiene un lápiz sin punta de seis caras?", "prisma hexagonal", ["cilindro", "pirámide hexagonal", "hexágono"]),
        ("¿Qué forma tiene una canica?", "esfera", ["cilindro", "círculo", "cono"]),
    ], "obj")()


def desarrollo(kind):
    """desarrollos planos sencillos (SVG)"""
    S = 34
    s = []
    def sq(x, y, w=S, h=S, fill="#d6e2f6"):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='#333' stroke-width='1.5'/>" % (x, y, w, h, fill))
    if kind == "cubo":
        for (i, j) in [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2)]:
            sq(10 + i * S, 10 + j * S)
        W, H = 10 + 4 * S + 10, 10 + 3 * S + 10
    elif kind == "piramide":
        sq(60, 60, S * 2, S * 2)
        x0, y0, L = 60, 60, S * 2
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='#f6d8b8' stroke='#333' stroke-width='1.5'/>" % (x0, y0, x0 + L, y0, x0 + L // 2, y0 - 50))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='#f6d8b8' stroke='#333' stroke-width='1.5'/>" % (x0, y0 + L, x0 + L, y0 + L, x0 + L // 2, y0 + L + 50))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='#f6d8b8' stroke='#333' stroke-width='1.5'/>" % (x0, y0, x0, y0 + L, x0 - 50, y0 + L // 2))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='#f6d8b8' stroke='#333' stroke-width='1.5'/>" % (x0 + L, y0, x0 + L, y0 + L, x0 + L + 50, y0 + L // 2))
        W, H = 200, 250
    elif kind == "cilindro":
        sq(20, 60, 150, 70, "#cfe6d6")
        s.append("<circle cx='95' cy='33' r='26' fill='#cfe6d6' stroke='#333' stroke-width='1.5'/>")
        s.append("<circle cx='95' cy='157' r='26' fill='#cfe6d6' stroke='#333' stroke-width='1.5'/>")
        W, H = 190, 195
    elif kind == "prisma":
        for (x, y, w, h) in [(10, 40, 30, 60), (40, 40, 60, 60), (100, 40, 30, 60), (130, 40, 60, 60), (40, 10, 60, 30), (40, 100, 60, 30)]:
            sq(x, y, w, h, "#f3d1dc")
        W, H = 200, 140
    else:  # cono
        s.append("<path d='M30 150 L110 20 L190 150 A92 92 0 0 1 30 150 Z' fill='#f6d8b8' stroke='#333' stroke-width='1.5'/>")
        s.append("<circle cx='110' cy='205' r='26' fill='#f6d8b8' stroke='#333' stroke-width='1.5'/>")
        W, H = 220, 240
    return "<div class='fig'><svg viewBox='0 0 %d %d' width='%d' role='img' aria-label='desarrollo plano de un cuerpo'>%s</svg></div>" % (W, H, W, "".join(s))


def art(c):
    return "un" if c == "cubo" or c.startswith("prisma") else "una"


def s6_cual():
    c = R.choice(list(DATA))
    f, a, v = DATA[c]
    ws = [x for x in DATA if DATA[x] != DATA[c]]
    R.shuffle(ws)
    near = [x for x in ws if x.split()[-1] == c.split()[-1] or x.split()[0] == c.split()[0]]
    return mcq("¿Qué poliedro tiene %d caras, %d aristas y %d vértices?" % (f, a, v), c, near + ws, "%s %s tiene %d caras, %d aristas y %d vértices: <b>%s</b>." % (art(c).capitalize(), c, f, a, v, c))


def s6_comparar():
    a, b = R.sample(list(DATA), 2)
    i = R.choice([0, 1, 2])
    w = ["caras", "aristas", "vértices"][i]
    if DATA[a][i] == DATA[b][i]:
        return None
    m = a if DATA[a][i] > DATA[b][i] else b
    return mcq("¿Qué tiene más %s: %s %s o %s %s?" % (w, art(a), a, art(b), b), "%s %s" % (art(m), m), ["%s %s" % (art(b if m == a else a), b if m == a else a), "los dos tienen el mismo número", "no se puede saber"],
               "%s %s: %d %s; %s %s: %d %s. Tiene más: <b>%s %s</b>." % (art(a).capitalize(), a, DATA[a][i], w, art(b), b, DATA[b][i], w, art(m), m))


def s5_desarrollo():
    k = R.choice(["cubo", "piramide", "cilindro", "prisma", "cono"])
    nm = {"cubo": "cubo", "piramide": "pirámide cuadrangular", "cilindro": "cilindro", "prisma": "prisma rectangular (ortoedro)", "cono": "cono"}[k]
    near = {"cubo": ["prisma rectangular (ortoedro)", "cuadrado"], "piramide": ["prisma rectangular (ortoedro)", "cono"], "cilindro": ["cono", "esfera"], "prisma": ["cubo", "pirámide cuadrangular"], "cono": ["cilindro", "pirámide cuadrangular"]}[k]
    return mcq(desarrollo(k) + "Si recortas y doblas este desarrollo plano, ¿qué cuerpo se forma?", nm, near + ["esfera", "cubo"], "Es el desarrollo de %s <b>%s</b>." % ("una" if k == "piramide" else "un", nm))


def main():
    seen = set()
    sets = [
        ("Reconocer cuerpos geométricos", mix(R, seen, [(s1_nombre, 6), (s1_tipo, 6), (s4_objetos, 8)])),
        ("Caras, aristas y vértices", mix(R, seen, [(s2_dibujo, 8), (s2_contar, 12)])),
        ("Propiedades de los cuerpos", mix(R, seen, [(s3_prop, 14), (s6_cual, 6)])),
        ("Comparar cuerpos", mix(R, seen, [(s6_comparar, 14), (s4_objetos, 6)])),
        ("Desarrollos planos y repaso", mix(R, seen, [(s5_desarrollo, 5), (s2_contar, 10), (s6_comparar, 5)])),
    ]
    body = lesson(
        ["Los <b>poliedros</b> tienen todas sus caras planas: el cubo, los prismas y las pirámides. Los <b>cuerpos redondos</b> tienen alguna superficie curva: el cilindro, el cono y la esfera.",
         "En un poliedro, las <b>caras</b> son los polígonos que lo forman, las <b>aristas</b> son las líneas donde se juntan dos caras y los <b>vértices</b> son los puntos donde se juntan las aristas.",
         "Un <b>prisma</b> tiene dos bases iguales y caras laterales rectangulares. Una <b>pirámide</b> tiene una base y caras laterales triangulares que se juntan en un vértice."],
        [("Prisma triangular", ["2 bases triangulares + 3 caras laterales", "aristas: 3 + 3 + 3", "vértices: 3 + 3"], "5 caras, 9 aristas y 6 vértices"),
         ("Pirámide cuadrangular", ["1 base cuadrada + 4 caras triangulares", "aristas: 4 + 4", "vértices: 4 + 1"], "5 caras, 8 aristas y 5 vértices")],
        [["Confundir prisma y pirámide", "El prisma tiene dos bases; la pirámide, una base y un vértice arriba."],
         ["Llamar «cuadrado» al cubo", "El cuadrado es plano; el cubo es un cuerpo con 6 caras cuadradas."],
         ["Contar aristas dos veces", "Cuenta las de la base, después las de arriba y luego las laterales."]],
        cuerpo_svg("prisma"))
    faq = [("¿Qué diferencia hay entre un poliedro y un cuerpo redondo?", "El poliedro tiene todas sus caras planas (polígonos); el cuerpo redondo tiene alguna superficie curva, como el cilindro, el cono y la esfera."),
           ("¿Cuántas caras, aristas y vértices tiene un cubo?", "Un cubo tiene 6 caras cuadradas, 12 aristas y 8 vértices.")]
    make_unit(R, "cuerpos-geometricos", "E",
              "Cuerpos geométricos: poliedros (prismas y pirámides) y cuerpos redondos (cilindro, cono y esfera); elementos (caras, aristas y vértices); identificación en objetos del entorno; desarrollos planos",
              "Cuerpos geométricos: poliedros y cuerpos redondos", "Cuerpos geométricos",
              "Fichas de matemáticas de 4.º de Primaria: poliedros y cuerpos redondos, prismas y pirámides, caras, aristas y vértices, objetos de la vida diaria y desarrollos planos. 100 ejercicios con soluciones.",
              "Poliedros: caras planas. Cuerpos redondos: superficie curva", "Prisma: 2 bases. Pirámide: 1 base y un vértice.",
              body, faq, sets, 21)


if __name__ == "__main__":
    main()
