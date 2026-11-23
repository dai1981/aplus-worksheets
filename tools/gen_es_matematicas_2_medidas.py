# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Medir longitud, masa y capacidad (Sentido de la medida)
build(lv): lv = 1 → «medir-y-comparar»: más largo y más corto, medir con cubos, más pesado, dónde cabe más;
lv = 2 → «longitud-masa-y-capacidad»: medir con la regla en cm, metros y centímetros, kilos, litros, problemas.
Errores: medir sin empezar en el 0, pensar que lo más grande pesa siempre más, comparar sin la misma unidad.
"""
import random
from es_common import mcq, mix, lesson, make_unit
import es_pics as P
import k_pics
from f_common import glasses_svg
import gen_es_matematicas_4_medidas_de_longitud as L4

R = None
LV = 2
NOMBRES = ["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo", "Vega", "Leo", "Alba", "Mario"]


def s_largo():
    n = R.choice([3, 4])
    ls = R.sample(range(2, 10), n)
    t = R.choice(["largo", "corto", "cuantos"])
    if t == "cuantos" and LV == 1:
        i = R.randrange(n)
        return mcq(P.torres(ls) + "¿Cuántos cubos tiene la torre %s?" % "ABCD"[i], str(ls[i]), [str(ls[i] + 1), str(ls[i] - 1), str(max(ls)) if max(ls) != ls[i] else str(ls[i] + 2)], "Contamos los cubos: <b>%d</b>." % ls[i])
    if t == "cuantos":
        i = R.randrange(n)
        j = (i + 1) % n
        if ls[i] == ls[j]:
            return None
        d = abs(ls[i] - ls[j])
        return mcq(P.torres(ls) + "¿Cuántos cubos más tiene la torre %s que la torre %s?" % ("ABCD"[i], "ABCD"[j]) if ls[i] > ls[j] else P.torres(ls) + "¿Cuántos cubos más tiene la torre %s que la torre %s?" % ("ABCD"[j], "ABCD"[i]),
                   str(d), [str(d + 1), str(max(ls[i], ls[j])), str(ls[i] + ls[j])], "%d − %d = <b>%d</b>." % (max(ls[i], ls[j]), min(ls[i], ls[j]), d))
    k = ls.index(max(ls)) if t == "largo" else ls.index(min(ls))
    ok = "el lápiz %s" % "ABCD"[k]
    return mcq(P.lapices(ls) + "¿Qué lápiz es más %s?" % t, ok, ["el lápiz %s" % c for c in "ABCD"[:n] if c != "ABCD"[k]] + ["miden lo mismo"], "Están alineados por la izquierda: mira dónde acaba la punta. Es <b>%s</b>." % ok)


def s_regla():
    cm = R.randint(2, 11)
    return mcq(L4.regla(cm, 0) + "¿Cuánto mide el lápiz?", "%d cm" % cm, ["%d cm" % (cm + 1), "%d cm" % (cm - 1), "%d m" % cm], "Empieza en el 0 y acaba en el %d: mide <b>%d cm</b>." % (cm, cm))


def s_unidad():
    items = [("una goma de borrar", "cm"), ("un lápiz", "cm"), ("una cuchara", "cm"), ("un libro", "cm"), ("una hormiga", "cm"),
             ("el pasillo del colegio", "m"), ("una piscina", "m"), ("la altura de un árbol", "m"), ("un campo de fútbol", "m"), ("la clase", "m"),
             ("una sandía", "kg"), ("un niño", "kg"), ("un saco de patatas", "kg"), ("una bañera", "L"), ("una botella grande de agua", "L"), ("un cubo de fregar", "L")]
    if LV == 1:
        return None
    thing, u = R.choice(items)
    nom = {"cm": "centímetros (cm)", "m": "metros (m)", "kg": "kilos (kg)", "L": "litros (L)"}
    q = "¿Qué unidad usarías para medir %s?" % thing
    if u in ("kg",):
        q = "¿Qué unidad usarías para pesar %s?" % thing
    if u == "L":
        q = "¿Qué unidad usarías para saber cuánta agua cabe en %s?" % thing
    return mcq(q, nom[u], [v for k, v in nom.items() if k != u], "Respuesta: <b>%s</b>." % nom[u])


def s_metro():
    t = R.choice(["cm", "cmp", "comp", "falta"])
    if t == "cm":
        m = R.randint(1, 9)
        return mcq("¿Cuántos centímetros son %d %s?" % (m, "metro" if m == 1 else "metros"), "%d cm" % (100 * m), ["%d cm" % (10 * m), "%d cm" % (m), "%d cm" % (1000 * m)], "1 m = 100 cm: %d × 100 = <b>%d cm</b>." % (m, 100 * m))
    if t == "cmp":
        m, c = R.randint(1, 5), R.randint(10, 90)
        return mcq("¿Cuántos centímetros son %d m y %d cm?" % (m, c), "%d cm" % (100 * m + c), ["%d cm" % (m + c), "%d cm" % (10 * m + c), "%d cm" % (100 * m + c + 10)], "%d m = %d cm; %d + %d = <b>%d cm</b>." % (m, 100 * m, 100 * m, c, 100 * m + c))
    if t == "comp":
        a = R.randint(1, 4)
        b = R.choice([x for x in range(60, 480, 10) if x != 100 * a])
        ok = "%d m" % a if 100 * a > b else "%d cm" % b
        return mcq("¿Qué es más largo: %d m o %d cm?" % (a, b), ok, ["%d cm" % b if ok.endswith(" m") else "%d m" % a, "son iguales", "no se puede saber"], "%d m = %d cm. Es más largo <b>%s</b>." % (a, 100 * a, ok))
    c = R.randint(1, 9) * 10
    return mcq("¿Cuántos centímetros le faltan a %d cm para llegar a 1 metro?" % c, "%d cm" % (100 - c), ["%d cm" % (10 - c // 10), "%d cm" % (100 - c + 10), "%d cm" % c] if c != 50 else ["5 cm", "60 cm", "40 cm"], "100 − %d = <b>%d cm</b>." % (c, 100 - c))


def s_pesa():
    a, b = R.sample(P.KINDS, 2)
    na, nb = R.randint(1, 3), R.randint(1, 3)
    tilt = R.choice(["left", "right", "equal"] if LV == 2 else ["left", "right"])
    pic = P.pic(k_pics.balance_svg((a, na), (b, nb), tilt), "balanza: a la izquierda %s, a la derecha %s" % (P.cosas(a, na), P.cosas(b, nb)))
    if tilt == "equal":
        ok = "pesan lo mismo"
    else:
        ok = "pesa más %s" % ("lo de la izquierda" if tilt == "left" else "lo de la derecha")
    return mcq(pic + "Mira la balanza. ¿Qué pesa más?", ok, [x for x in ("pesa más lo de la izquierda", "pesa más lo de la derecha", "pesan lo mismo", "no se puede saber") if x != ok],
               "El lado que baja es el que pesa más; si está recta, pesan lo mismo: <b>%s</b>." % ok)


def s_pesa2():
    if LV == 1:
        q, a, w = R.choice([("¿Qué fruta pesa más?", "una sandía", ["una fresa", "una cereza", "una uva"]), ("¿Qué cosa pesa menos?", "una pluma", ["un libro", "una mochila", "un perro"]),
                            ("¿Qué animal pesa más?", "un elefante", ["un gato", "un ratón", "un pájaro"]), ("¿Qué objeto de la clase pesa menos?", "un lápiz", ["una silla", "una mesa", "una estantería"]),
                            ("¿Con qué se pesa?", "con una balanza", ["con una regla", "con un reloj", "con un vaso"]), ("¿Qué compra pesa más?", "un saco de patatas", ["una patata", "una goma", "una galleta"]),
                            ("Un globo grande y una canica. ¿Qué pesa más?", "la canica", ["el globo", "pesan lo mismo", "no pesan nada"])])
        return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)
    k = R.choice(["kg", "suma", "mas"])
    if k == "kg":
        x, y = R.randint(2, 30), R.randint(2, 30)
        if x == y:
            return None
        return mcq("Una caja pesa %d kg y otra pesa %d kg. ¿Cuál pesa más?" % (x, y), "la de %d kg" % max(x, y), ["la de %d kg" % min(x, y), "pesan lo mismo", "la más grande"], "%d &gt; %d: <b>la de %d kg</b>." % (max(x, y), min(x, y), max(x, y)))
    if k == "suma":
        x, y = R.randint(2, 20), R.randint(2, 20)
        return mcq("En la balanza ponemos un paquete de %d kg y otro de %d kg. ¿Cuánto pesan juntos?" % (x, y), "%d kg" % (x + y), ["%d kg" % abs(x - y) if x != y else "%d kg" % (x + y + 2), "%d kg" % (x + y + 1), "%d kg" % (x + y - 1)], "%d + %d = <b>%d kg</b>." % (x, y, x + y))
    x = R.randint(5, 40)
    d = R.randint(2, 9)
    return mcq("Un perro pesa %d kg. Un gato pesa %d kg menos. ¿Cuánto pesa el gato?" % (x, d), "%d kg" % (x - d), ["%d kg" % (x + d), "%d kg" % d, "%d kg" % (x - d + 1)], "%d − %d = <b>%d kg</b>." % (x, d, x - d))


def s_cabe():
    t = R.choice(["mas", "menos", "lleno"]) if LV == 1 else R.choice(["mas", "menos", "litros", "litros", "medio"])
    if t in ("mas", "menos"):
        hs = R.sample([30, 45, 60, 75, 90], 4)
        lev = R.uniform(0.3, 0.9)
        same = R.random() < 0.5
        if same:
            levs = R.sample([0.2, 0.35, 0.5, 0.65, 0.8, 0.95], 4)
            items = [(40, 90, l) for l in levs]
            k = levs.index(max(levs)) if t == "mas" else levs.index(min(levs))
            q = "¿Qué vaso tiene %s agua?" % ("más" if t == "mas" else "menos")
        else:
            items = [(40, h, 0) for h in hs]
            k = hs.index(max(hs)) if t == "mas" else hs.index(min(hs))
            q = "Los vasos son igual de anchos. ¿En cuál cabe %s agua?" % ("más" if t == "mas" else "menos")
        ok = "el %s" % "ABCD"[k]
        return mcq(P.pic(glasses_svg(items), "cuatro vasos A, B, C y D") + q, ok, ["el %s" % c for c in "ABCD" if c != "ABCD"[k]], "Respuesta: <b>%s</b>." % ok)
    if t == "lleno":
        q, a, w = R.choice([("¿Dónde cabe más agua?", "en una bañera", ["en un vaso", "en una taza", "en una cuchara"]), ("¿Dónde cabe menos agua?", "en una cuchara", ["en un cubo", "en una piscina", "en una botella"]),
                            ("¿Dónde cabe más agua?", "en una piscina", ["en una botella", "en un vaso", "en un plato"]), ("Si un vaso está lleno, ¿cabe más agua?", "no", ["sí, mucha", "sí, un poco", "sí, el doble"]),
                            ("Echamos el agua de un vaso lleno en una jarra y la jarra no se llena. ¿Dónde cabe más?", "en la jarra", ["en el vaso", "cabe lo mismo", "no se puede saber"])])
        return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)
    if t == "medio":
        q, a, w = R.choice([("¿Cuántas botellas de medio litro llenan 1 litro?", "2", ["1", "4", "5"]), ("¿Cuántas botellas de medio litro llenan 2 litros?", "4", ["2", "3", "6"]),
                            ("¿Cuántas botellas de medio litro llenan 3 litros?", "6", ["3", "4", "5"]), ("Medio litro más medio litro son…", "1 litro", ["2 litros", "medio litro", "100 litros"])])
        return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)
    x, y = R.randint(2, 12), R.randint(2, 12)
    k = R.choice(["junta", "gasta"])
    if k == "junta":
        return mcq("Tenemos una garrafa de %d L y otra de %d L. ¿Cuántos litros hay en total?" % (x, y), "%d L" % (x + y), ["%d L" % abs(x - y) if x != y else "%d L" % (x + y + 2), "%d L" % (x + y + 1), "%d L" % (x * 10)], "%d + %d = <b>%d L</b>." % (x, y, x + y))
    t2 = x + y
    return mcq("Un cubo tiene %d L de agua. Usamos %d L para regar. ¿Cuántos litros quedan?" % (t2, y), "%d L" % x, ["%d L" % (t2 + y), "%d L" % (x + 1), "%d L" % y if y != x else "%d L" % (x - 1)], "%d − %d = <b>%d L</b>." % (t2, y, x))


def s_problema():
    p = R.choice(NOMBRES)
    t = R.choice(["cinta", "salto", "torre"] if LV == 1 else ["cinta", "salto", "cuerda"])
    if t == "cinta":
        a, b = (R.randint(5, 15), R.randint(2, 4)) if LV == 1 else (R.randint(20, 90), R.randint(5, 19))
        return mcq("%s tiene una cinta de %d cm y corta %d cm. ¿Cuánto mide la cinta ahora?" % (p, a, b), "%d cm" % (a - b), ["%d cm" % (a + b), "%d cm" % (a - b + 1), "%d cm" % b], "%d − %d = <b>%d cm</b>." % (a, b, a - b))
    if t == "salto":
        a, b = (R.randint(2, 9), R.randint(2, 9)) if LV == 1 else (R.randint(20, 80), R.randint(20, 80))
        if a == b:
            return None
        return mcq("%s salta %d palmos y su amiga salta %d palmos. ¿Cuántos palmos más salta %s?" % (p, max(a, b), min(a, b), p), str(a - b if a > b else b - a), [str(a + b), str(abs(a - b) + 1), str(max(a, b))], "%d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))
    if t == "torre":
        a, b = R.randint(3, 9), R.randint(2, 9)
        return mcq("Una torre tiene %d cubos. Ponemos %d cubos más encima. ¿Cuántos cubos tiene ahora?" % (a, b), str(a + b), [str(abs(a - b)) if a != b else str(a + b + 2), str(a + b + 1), str(a + b - 1)], "%d + %d = <b>%d</b>." % (a, b, a + b))
    a, b = R.randint(2, 6), R.randint(10, 90)
    return mcq("Una cuerda mide %d m y otra mide %d cm. ¿Cuántos centímetros miden juntas?" % (a, b), "%d cm" % (100 * a + b), ["%d cm" % (a + b), "%d cm" % (10 * a + b), "%d m" % (a + b)], "%d m = %d cm; %d + %d = <b>%d cm</b>." % (a, 100 * a, 100 * a, b, 100 * a + b))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30011 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("Más largo, más corto", mix(R, seen, [(s_largo, 20)])), ("Medir con cubos y palmos", mix(R, seen, [(s_largo, 6), (s_problema, 14)])),
                ("Más pesado, más ligero", mix(R, seen, [(s_pesa, 14), (s_pesa2, 6)])), ("¿Dónde cabe más?", mix(R, seen, [(s_cabe, 20)])), ("Repaso", mix(R, seen, [(s_largo, 8), (s_pesa, 6), (s_cabe, 6)]))]
        think = ["Para comparar dos cosas, ponlas una al lado de la otra, empezando en el mismo sitio.", "Podemos medir con cubos, clips o palmos: contamos cuántos caben.",
                 "En la <b>balanza</b>, el lado que baja pesa más.", "Si echamos el agua de un vaso en otro y no se llena, en el segundo cabe más."]
        ex = [("Torre A de 5 cubos y torre B de 8 cubos", ["8 − 5 = 3"], "B tiene 3 cubos más"), ("La balanza baja por la izquierda", ["El lado que baja pesa más"], "pesa más lo de la izquierda")]
        mist = [["Comparar sin empezar en el mismo sitio", "Alinea las cosas por un extremo."], ["Pensar que lo más grande pesa más", "Un globo es grande y pesa poco."], ["Contar mal los cubos", "Señala cada cubo al contarlo."]]
        kb, ks = "En la balanza, baja lo que pesa más", "Para medir, cuenta cuántos caben."
        meta = "Fichas de matemáticas de 1.º de Primaria: más largo y más corto, medir con cubos, más pesado y más ligero, dónde cabe más. 100 ejercicios con soluciones."
        std = "Comparación de longitudes, masas y capacidades; medida con unidades no convencionales (cubos, palmos)"
        slug, title, short = "medir-y-comparar", "Medir y comparar", "Medir y comparar"
        pic = P.torres([5, 8, 3])
    else:
        sets = [("Medir con la regla", mix(R, seen, [(s_regla, 10), (s_largo, 10)])), ("Metros y centímetros", mix(R, seen, [(s_metro, 20)])),
                ("Kilos", mix(R, seen, [(s_pesa, 8), (s_pesa2, 12)])), ("Litros", mix(R, seen, [(s_cabe, 20)])), ("Elegir la unidad y problemas", mix(R, seen, [(s_unidad, 8), (s_problema, 12)]))]
        think = ["La longitud se mide en <b>metros</b> (m) y <b>centímetros</b> (cm): 1 m = 100 cm.", "Con la regla, empieza a medir en el <b>0</b>.",
                 "El peso se mide en <b>kilos</b> (kg) y lo que cabe en un recipiente, en <b>litros</b> (L)."]
        ex = [("2 m y 30 cm en cm", ["2 m = 200 cm", "200 + 30"], "230 cm"), ("¿Cuántas botellas de medio litro llenan 2 L?", ["2 en cada litro", "2 + 2"], "4 botellas")]
        mist = [["Medir desde el borde de la regla", "Coloca el objeto en el 0."], ["Pensar que 1 m = 10 cm", "1 m = 100 cm."], ["Comparar m y cm sin pasar a la misma unidad", "2 m = 200 cm &gt; 150 cm."]]
        kb, ks = "1 m = 100 cm", "Peso en kg; agua en litros (L)."
        meta = "Fichas de matemáticas de 2.º de Primaria: medir con la regla, metros y centímetros, kilos, litros y problemas de medida. 100 ejercicios con soluciones."
        std = "Unidades de longitud (m, cm), masa (kg) y capacidad (L); medida con la regla; comparación y problemas"
        slug, title, short = "longitud-masa-y-capacidad", "Longitud, masa y capacidad", "Medidas"
        pic = L4.regla(7, 0)
    body = lesson(think, ex, mist, pic)
    faq = [("¿Qué pesa más, lo grande o lo pequeño?", "No siempre lo grande: un globo es grande y pesa muy poco. Para saberlo, se usa la balanza."),
           ("¿Cuántos centímetros tiene un metro?", "Un metro tiene 100 centímetros.")]
    make_unit(R, slug, "M", std, title, short, meta, kb, ks, body, faq, sets, 8 if lv == 1 else 11, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
