# -*- coding: utf-8 -*-
"""
México, 3.er grado de preescolar (Fase 2): problemas propios con dibujos. Números hasta el 10 (contar hasta el 20).
setup(R) antes de usar. Cada función devuelve un problema ya en español de México (pasa por mx_item).
"""
import re
import k_pics
import es_pics as P
from es_pics import COSAS, KINDS, NUM, nombre, fem, cuantos, cosas
from mx_common import mcq, mx_item, dinero_svg, fig, svg_wrap, Kids
from ws_common import text

R = None
K = None
ORD = ["primero", "segundo", "tercero", "cuarto", "quinto", "sexto", "séptimo", "octavo", "noveno", "décimo"]
ORD_F = ["primera", "segunda", "tercera", "cuarta", "quinta", "sexta", "séptima", "octava", "novena", "décima"]
ORD_LUGAR = ["primer", "segundo", "tercer", "cuarto", "quinto", "sexto", "séptimo", "octavo", "noveno", "décimo"]


def setup(rnd):
    global R, K
    R = rnd
    K = Kids(rnd)


def M(q, ok, cands, e):
    q = re.sub(r"\b1 tachad([ao])s\b", r"1 tachad\1", q)
    w = [str(c) for c in dict.fromkeys(cands) if str(c) != str(ok)]
    if len(w) < 3:
        return None
    try:
        return mx_item(mcq(q, str(ok), w[:3], e))
    except AssertionError:
        return None


def nums_near(n, lo, hi):
    c = [x for x in (n - 1, n + 1, n - 2, n + 2, n + 3, n - 3) if lo <= x <= hi]
    R.shuffle(c)
    return c


def kid():
    return K.next()


# ============================================================ contar
def contar(*ks, hi=10):
    t = R.choice(ks or ["fila", "disperso", "marco", "dados", "caja", "plato"])
    n = R.randint(1, hi)
    kind = R.choice(KINDS)
    if t == "fila":
        pic = P.fila(n, kind)
    elif t == "disperso":
        pic = P.disperso(n, kind, R.randint(1, 10 ** 6))
    elif t == "marco":
        if n > 10:
            pic = P.marco10(n, 2)
        else:
            pic = P.marco10(n)
        return M(pic + "¿Cuántos puntos hay en el marco?", n, nums_near(n, 0, hi), "Cuenta cada punto una vez: hay <b>%d</b>." % n)
    elif t == "dados":
        vals = [R.randint(1, 6) for _ in range(R.choice([1, 2]))]
        n = sum(vals)
        if n > hi:
            return None
        return M(P.dados(vals) + "¿Cuántos puntos hay en %s?" % ("el dado" if len(vals) == 1 else "los dos dados"), n, nums_near(n, 1, 12),
                 "Contamos todos los puntos: <b>%d</b>." % n)
    elif t == "caja":
        pic = P.caja(n, kind)
    else:
        pic = P.plato(n, kind)
    return M(pic + "%s %s hay?" % (cuantos(kind), nombre(kind)), n, nums_near(n, 0, hi), "Señala y cuenta cada %s una sola vez: hay <b>%d</b>." % (nombre(kind, 1), n))


def palabra(*ks, hi=10):
    n = R.randint(0, hi)
    if R.random() < .5:
        return M("¿Qué número es «%s»?" % NUM[n], n, nums_near(n, 0, hi), "«%s» se escribe <b>%d</b>." % (NUM[n], n))
    w = [NUM[x] for x in nums_near(n, 0, hi)]
    return M("¿Cómo se dice el número %d?" % n, NUM[n], w, "%d se dice <b>%s</b>." % (n, NUM[n]))


def antes_despues(*ks, hi=20):
    t = R.choice(ks or ["despues", "antes", "entre"])
    n = R.randint(1, hi - 1)
    if t == "despues":
        return M("¿Qué número va después del %d?" % n, n + 1, [n - 1, n + 2, n], "Contando: %d, <b>%d</b>." % (n, n + 1))
    if t == "antes":
        return M("¿Qué número va antes del %d?" % n, n - 1, [n + 1, n - 2, n], "Contando: <b>%d</b>, %d." % (n - 1, n))
    if n < 1:
        return None
    return M("¿Qué número va entre el %d y el %d?" % (n - 1, n + 1), n, [n + 2, n - 2, n + 1], "%d, <b>%d</b>, %d." % (n - 1, n, n + 1))


def serie(*ks, hi=20):
    t = R.choice(ks or ["sube", "sube", "baja"])
    k = 5
    if t == "sube":
        a = R.randint(0, hi - k + 1)
        s = list(range(a, a + k))
    else:
        a = R.randint(k - 1, min(hi, 10))
        s = list(range(a, a - k, -1))
    i = R.randrange(1, k)
    ans = s[i]
    show = ", ".join("__" if j == i else str(v) for j, v in enumerate(s))
    return M("¿Qué número falta? %s" % show, ans, [ans + 1, ans - 1, ans + 2, s[i - 1]], "La serie %s de uno en uno: falta el <b>%d</b>." % ("sube" if t == "sube" else "baja", ans))


def salta(*ks):
    a = R.randint(0, 6)
    h = R.randint(1, 4)
    if a + h > 10:
        return None
    return M(P.salto(a, h) + "La rana empieza en el %d y da %d %s hacia adelante. ¿En qué número cae?" % (a, h, "salto" if h == 1 else "saltos"), a + h, [a + h - 1, a + h + 1, a, h],
             "%d y %d más: <b>%d</b>." % (a, h, a + h))


# ============================================================ comparar
def comparar(*ks):
    t = R.choice(ks or ["mas", "menos", "igual", "numero", "igualar"])
    ka, kb = R.sample(KINDS, 2)
    a, b = R.randint(1, 10), R.randint(1, 10)
    if t == "igual":
        b = a if R.random() < .5 else b
    if t in ("mas", "menos", "igual"):
        if t != "igual" and a == b:
            return None
        pic = fig(svg_wrap(*_two(a, ka, b, kb)))
        q = {"mas": "¿De qué hay <b>más</b>?", "menos": "¿De qué hay <b>menos</b>?", "igual": "¿Hay la misma cantidad de %s que de %s?" % (nombre(ka), nombre(kb))}[t]
        if t == "igual":
            ok = "sí, hay igual" if a == b else "no, hay más %s" % nombre(ka if a > b else kb)
            return M(pic + q, ok, ["sí, hay igual", "no, hay más %s" % nombre(ka), "no, hay más %s" % nombre(kb), "no se puede saber"],
                     "Hay %s y %s: %s." % (cosas(ka, a), cosas(kb, b), "<b>hay igual</b>" if a == b else "<b>no hay igual</b>"))
        big = (ka if a > b else kb) if t == "mas" else (ka if a < b else kb)
        return M(pic + q, "de " + nombre(big), ["de " + nombre(kb if big == ka else ka), "hay igual", "no se puede saber"],
                 "Hay %s y %s: hay %s <b>%s</b>." % (cosas(ka, a), cosas(kb, b), "más" if t == "mas" else "menos", nombre(big)))
    if t == "numero":
        if a == b:
            return None
        big = R.random() < .5
        ok = max(a, b) if big else min(a, b)
        return M("¿Qué número es %s: %d o %d?" % ("mayor" if big else "menor", a, b), ok, [min(a, b) if big else max(a, b), "son iguales", ok + 10],
                 "Al contar, el %d va %s del %d: el %s es <b>%d</b>." % (min(a, b), "antes", max(a, b), "mayor" if big else "menor", ok))
    lo, hi = sorted((a, b))
    if lo == hi:
        return None
    q = "En una mesa hay %s y %s. ¿%s %s faltan para que haya igual?" % (cosas(ka, hi), cosas(kb, lo), "Cuántas" if fem(kb) else "Cuántos", nombre(kb))
    return M(q, hi - lo, nums_near(hi - lo, 0, 10) + [hi], "De %d a %d faltan <b>%d</b>." % (lo, hi, hi - lo))


def _two(a, ka, b, kb):
    """dos grupos separados por una raya (sin signo)"""
    svg = k_pics.two_groups_svg(a, ka, b, kb, "|")
    import re
    m = re.search(r"viewBox='0 0 (\d+) (\d+)'", svg)
    body = re.search(r"<g[^>]*>(.*)</g></svg>", svg, re.S).group(1)
    return int(m.group(1)), int(m.group(2)), body, "%s y %s" % (cosas(ka, a), cosas(kb, b))


# ============================================================ ordinales
def fila_svg(kinds, hi=None):
    sp = 62
    s = []
    for i, k in enumerate(kinds):
        cx = 8 + sp / 2 + i * sp
        s.append(k_pics.obj(k, cx, 34, 19))
    s.append("<path d='M%d 70 L%d 70' stroke='#1d6b3a' stroke-width='2.5'/><path d='M%d 64 L%d 70 L%d 76' fill='none' stroke='#1d6b3a' stroke-width='2.5'/>" % (12, 12 + 70, 74, 82, 74))
    s.append(text(12 + 110, 76, "empieza aquí", 13, col="#1d6b3a"))
    return fig(svg_wrap(16 + len(kinds) * sp, 86, "".join(s), "fila: " + ", ".join(nombre(k, 1) for k in kinds)))


def ordinal(*ks):
    t = R.choice(ks or ["lugar", "que"])
    n = R.randint(4, 8)
    kinds = R.sample(KINDS, n)
    pic = fila_svg(kinds)
    i = R.randrange(n)
    k = kinds[i]
    if t == "lugar":
        art = "la" if fem(k) else "el"
        ords = ORD_F if fem(k) else ORD
        w = [ords[j] for j in range(n) if j != i]
        R.shuffle(w)
        return M(pic + "Cuenta desde la izquierda. ¿En qué lugar está %s %s?" % (art, nombre(k, 1)), ords[i], w,
                 "%s %s está en el <b>%s</b> lugar." % (art.capitalize(), nombre(k, 1), ORD_LUGAR[i]))
    w = [("la " if fem(x) else "el ") + nombre(x, 1) for x in kinds if x != k]
    R.shuffle(w)
    return M(pic + "Cuenta desde la izquierda. ¿Qué hay en el %s lugar?" % ORD_LUGAR[i], ("la " if fem(k) else "el ") + nombre(k, 1), w,
             "En el %s lugar está <b>%s %s</b>." % (ORD_LUGAR[i], "la" if fem(k) else "el", nombre(k, 1)))


def ordinal_carrera(*ks):
    names = [kid()[0] for _ in range(4)]
    if len(set(names)) < 4:
        return None
    i = R.randrange(4)
    llegada = ", ".join(names)
    return M("En una carrera llegaron en este orden: %s. ¿En qué lugar llegó %s?" % (llegada, names[i]), ["primer", "segundo", "tercer", "cuarto"][i] + " lugar",
             [x + " lugar" for x in ["primer", "segundo", "tercer", "cuarto", "quinto"] if x != ["primer", "segundo", "tercer", "cuarto"][i]],
             "%s es el número %d de la lista: <b>%s lugar</b>." % (names[i], i + 1, ["primer", "segundo", "tercer", "cuarto"][i]))


# ============================================================ agregar, quitar, juntar, separar, repartir
COSAS_H = [("globos", "globo"), ("canicas", "canica"), ("galletas", "galleta"), ("lápices", "lápiz"), ("estampas", "estampa"), ("carritos", "carrito"), ("paletas", "paleta"), ("crayolas", "crayola")]
PIC_OF = {"canicas": "ball", "estampas": "star"}


def historia(*ks):
    t = R.choice(ks or ["agregar", "quitar", "juntar", "separar"])
    who, pron = kid()
    pl, sg = R.choice(COSAS_H)
    a = R.randint(1, 8)
    b = R.randint(1, 10 - a) if t in ("agregar", "juntar") else R.randint(1, a)
    pick = PIC_OF.get(pl)
    if t == "agregar":
        ans = a + b
        q = "%s tiene %d %s. Le regalan %d más. ¿Cuántos %s tiene ahora?" % (who, a, pl if a != 1 else sg, b, pl) if not pl.endswith("as") else \
            "%s tiene %d %s. Le regalan %d más. ¿Cuántas %s tiene ahora?" % (who, a, pl if a != 1 else sg, b, pl)
        pic = P.dos_grupos(a, pick, b) if pick else ""
        e = "Agregar es juntar más: %d y %d son <b>%d</b>." % (a, b, ans)
        w = [a, b, ans + 1, ans - 1]
    elif t == "quitar":
        if b == a:
            return None
        ans = a - b
        q = "%s tenía %d %s y regaló %d. ¿Cuántas %s le quedan?" % (who, a, pl, b, pl) if pl.endswith("as") else "%s tenía %d %s y regaló %d. ¿Cuántos %s le quedan?" % (who, a, pl, b, pl)
        pic = P.tachados(a, pick, b) if pick else ""
        e = "Quitar es tachar: de %d quitamos %d y quedan <b>%d</b>." % (a, b, ans)
        w = [a + b, b, ans + 1, a]
    elif t == "juntar":
        who2 = kid()[0]
        if who2 == who:
            return None
        ans = a + b
        q = "%s tiene %d %s y %s tiene %d. Si los juntan, ¿cuántos %s son?" % (who, a, pl, who2, b, pl) if not pl.endswith("as") else \
            "%s tiene %d %s y %s tiene %d. Si las juntan, ¿cuántas %s son?" % (who, a, pl, who2, b, pl)
        pic = P.dos_grupos(a, pick, b) if pick else ""
        e = "Juntamos los dos grupos: %d y %d son <b>%d</b>." % (a, b, ans)
        w = [a, b, ans + 1, ans - 1]
    else:
        tot = R.randint(3, 10)
        a = R.randint(1, tot - 1)
        ans = tot - a
        q = "Hay %d %s: %d son rojas y las demás azules. ¿Cuántas son azules?" % (tot, "crayolas", a)
        pic = ""
        e = "Separamos %d en %d y <b>%d</b>." % (tot, a, ans)
        w = [tot, a, ans + 1, ans - 1]
    if ans > 10 or ans < 0:
        return None
    return M(pic + q, ans, [x for x in w if 0 <= x <= 12], e)


def descomponer(*ks):
    n = R.randint(3, 10)
    a = R.randint(1, n - 1)
    kind = R.choice(KINDS)
    if R.random() < .5:
        pic = P.pic(k_pics.crossed_row_svg(n, kind, n - a), "%s, %d %s" % (cosas(kind, n), n - a, "tachadas" if fem(kind) else "tachados"))
        return M(pic + "Hay %d %s en total. %d no %s tachad%s. ¿Cuánt%ss están tachad%ss?" % (n, nombre(kind), a, "está" if a == 1 else "están", ("a" if fem(kind) else "o") + ("" if a == 1 else "s"), "a" if fem(kind) else "o", "a" if fem(kind) else "o"),
                 n - a, nums_near(n - a, 0, 10) + [n], "%d y <b>%d</b> forman %d." % (a, n - a, n))
    return M("¿Qué número falta? %d y __ forman %d." % (a, n), n - a, nums_near(n - a, 0, 10) + [n, a], "%d y <b>%d</b> forman %d." % (a, n - a, n))


def repartir(*ks):
    g = R.choice([2, 2, 3])
    k = R.randint(1, 10 // g)
    n = g * k
    pl = R.choice(["galletas", "manzanas", "paletas", "canicas"])
    names = [kid()[0] for _ in range(g)]
    if len(set(names)) < g:
        return None
    kind = {"galletas": "button", "manzanas": "apple", "paletas": "heart", "canicas": "ball"}[pl]
    return M(P.grupos(g, k, kind) + "%s reparten %d %s por partes iguales. ¿Cuántas le tocan a cada uno?" % (" y ".join(names) if g == 2 else "%s, %s y %s" % tuple(names), n, pl),
             k, nums_near(k, 1, 10) + [n], "Damos de una en una hasta que se acaban: a cada uno le tocan <b>%d</b>." % k)


# ============================================================ monedas y billetes
PRECIOS = [("una paleta", 5), ("un chicle", 2), ("un jugo", 10), ("unas galletas", 8), ("un globo", 6), ("un lápiz", 4), ("una pelota", 15), ("un dulce", 1), ("una torta", 20), ("un elote", 12)]


def dinero(*ks):
    t = R.choice(ks or ["contar", "contar", "cual", "alcanza", "mas"])
    if t == "contar":
        items = sorted([R.choice([100, 100, 200, 500, 1000]) for _ in range(R.randint(2, 4))], reverse=True)
        tot = sum(items) // 100
        if tot > 20:
            return None
        return M(dinero_svg(items) + "¿Cuánto dinero hay?", "$%d" % tot, ["$%d" % x for x in (tot + 1, tot - 1, len(items), tot + 5) if x > 0],
                 "Sumamos: %s = <b>$%d</b>." % (" + ".join("$%d" % (v // 100) for v in items), tot))
    if t == "cual":
        v = R.choice([100, 200, 500, 1000, 2000])
        lab = {100: "$1", 200: "$2", 500: "$5", 1000: "$10", 2000: "$20"}[v]
        bill = v == 2000 and R.random() < .5
        return M(dinero_svg(["b2000"] if bill else [v]) + "¿Cuánto vale %s?" % ("este billete" if bill else "esta moneda"), lab, [x for x in ["$1", "$2", "$5", "$10", "$20", "$50"] if x != lab],
                 "Tiene escrito su valor: <b>%s</b>." % lab)
    if t == "monedas":
        c = R.choice([1, 1, 2, 5])
        p = R.choice([x for x in range(c, 11, c) if x // c >= 2])
        cosa = R.choice(["una paleta", "un jugo", "unas galletas", "un globo", "un lápiz", "una gelatina", "un yogur"])
        return M(dinero_svg([c * 100]) + "%s cuesta $%d. ¿Cuántas monedas de $%d necesitas para pagar?" % (cosa.capitalize(), p, c), p // c, nums_near(p // c, 1, 10) + [p],
                 "%s: <b>%d monedas</b>." % (" + ".join(["$%d" % c] * (p // c)), p // c))
    if t == "mas":
        a, b = R.sample([100, 200, 500, 1000], 2)
        return M(dinero_svg([a, b]) + "¿Qué moneda vale más?", "la de $%d" % (max(a, b) // 100), ["la de $%d" % (min(a, b) // 100), "valen igual", "la más grande siempre"],
                 "$%d vale más que $%d: mira el número, no el tamaño." % (max(a, b) // 100, min(a, b) // 100))
    cosa, p = R.choice(PRECIOS)
    items = sorted([R.choice([100, 200, 500, 1000]) for _ in range(R.randint(1, 3))], reverse=True)
    tot = sum(items) // 100
    if tot > 20 or tot == p:
        return None
    ok = "sí, le alcanza" if tot >= p else "no, le falta dinero"
    who = kid()[0]
    return M(dinero_svg(items) + "%s quiere comprar %s de $%d y tiene este dinero. ¿Le alcanza?" % (who, cosa, p), ok, ["sí, le alcanza", "no, le falta dinero", "solo si le dan cambio", "no se puede saber"],
             "Tiene $%d y cuesta $%d: <b>%s</b>." % (tot, p, ok))


# ============================================================ el tiempo
ACT = [("tomar el almuerzo en el recreo", "mañana"), ("ver la Luna", "noche"), ("escuchar un cuento para dormir", "noche"), ("salir al parque después de comer", "tarde"), ("ver salir el sol", "mañana"),
       ("desayunar", "mañana"), ("ir a la escuela", "mañana"), ("despertarse", "mañana"), ("comer", "tarde"), ("hacer la tarea", "tarde"), ("ver la puesta del sol", "tarde"),
       ("cenar", "noche"), ("ponerse la pijama", "noche"), ("dormir", "noche"), ("ver las estrellas", "noche")]
RUTINA = [["ponerse los calcetines", "ponerse los zapatos", "amarrarse las agujetas", "salir a jugar"], ["lavar la fruta", "pelarla", "partirla", "comerla"],
          ["inflar el globo", "amarrarlo", "jugar con él", "guardarlo"], ["despertarse", "bañarse", "desayunar", "ir a la escuela"], ["llegar a casa", "comer", "hacer la tarea", "jugar"], ["cenar", "lavarse los dientes", "ponerse la pijama", "dormir"],
          ["sembrar una semilla", "regarla", "ver salir una plantita", "ver una flor"], ["mezclar la masa", "hornear el pastel", "ponerle velas", "cantar las mañanitas"]]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def tiempo(*ks):
    t = R.choice(ks or ["parte", "antes", "despues", "dia", "dura"])
    if t == "parte":
        a, p = R.choice(ACT)
        return M("¿En qué parte del día solemos %s?" % a, "en la " + p, ["en la mañana", "en la tarde", "en la noche", "a mediodía"], "Normalmente se hace <b>en la %s</b>." % p)
    if t in ("antes", "despues"):
        r = R.choice(RUTINA)
        i = R.randrange(1, 4) if t == "antes" else R.randrange(0, 3)
        ok = r[i - 1] if t == "antes" else r[i + 1]
        return M("¿Qué pasa %s de «%s»?" % ("antes" if t == "antes" else "después", r[i]), ok, [x for x in r if x not in (ok, r[i])] + ["nada"],
                 "El orden es: %s." % " → ".join(r))
    if t == "instrumento":
        items = [("¿Qué usamos para saber qué día es hoy?", "un calendario", ["una balanza", "una regla", "un vaso"]),
                 ("¿Qué usamos para saber la hora?", "un reloj", ["una balanza", "un calendario", "una cuchara"]),
                 ("¿Qué nos ayuda a medir un ratito, mientras cae la arena?", "un reloj de arena", ["un termómetro", "una regla", "un calendario"]),
                 ("¿Cuántos días tiene una semana?", "7", ["5", "10", "30"]),
                 ("¿Qué día de la semana no hay escuela?", "el domingo", ["el lunes", "el miércoles", "el viernes"]),
                 ("¿Cuándo es de noche?", "cuando está oscuro y salen la Luna y las estrellas", ["cuando sale el sol", "a la hora del recreo", "cuando desayunamos"]),
                 ("Ayer, hoy y mañana: ¿cuál ya pasó?", "ayer", ["hoy", "mañana", "pasado mañana"])]
        q, a, w = R.choice(items)
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    if t == "dia":
        i = R.randrange(7)
        if R.random() < .5:
            return M("¿Qué día va después del %s?" % DIAS[i], DIAS[(i + 1) % 7], [DIAS[(i - 1) % 7], DIAS[(i + 2) % 7], DIAS[(i + 3) % 7]], "La semana: %s." % ", ".join(DIAS))
        return M("¿Qué día va antes del %s?" % DIAS[i], DIAS[(i - 1) % 7], [DIAS[(i + 1) % 7], DIAS[(i - 2) % 7], DIAS[(i + 3) % 7]], "La semana: %s." % ", ".join(DIAS))
    pares = [("lavarse las manos", "dormir en la noche"), ("comer un dulce", "ver una película"), ("aplaudir una vez", "ir de vacaciones"), ("parpadear", "comer"),
             ("abrir una puerta", "hacer un viaje en camión"), ("tomar un vaso de agua", "jugar un partido de fútbol"), ("ponerse un zapato", "pasar un día en la escuela")]
    a, b = R.choice(pares)
    larga = R.random() < .5
    return M("¿Qué dura <b>%s</b>: %s o %s?" % ("más" if larga else "menos", a, b), b if larga else a, [a if larga else b, "duran lo mismo", "no se puede saber"],
             "«%s» toma mucho más tiempo que «%s»." % (b, a))


# ============================================================ medidas
def medir(*ks):
    t = R.choice(ks or ["largo", "corto", "alto", "pesa", "cabe"])
    if t in ("largo", "corto"):
        ls = R.sample(range(2, 9), 3)
        i = ls.index(max(ls) if t == "largo" else min(ls))
        return M(P.lapices(ls) + "¿Qué lápiz es el más %s?" % t, "el " + "ABC"[i], ["el " + "ABC"[j] for j in range(3) if j != i] + ["todos miden igual"],
                 "Si empiezan en el mismo lugar, el más %s es el que %s: <b>el %s</b>." % (t, "llega más lejos" if t == "largo" else "llega menos lejos", "ABC"[i]))
    if t == "alto":
        hs = R.sample(range(2, 9), 3)
        low = R.random() < .5
        i = hs.index(min(hs) if low else max(hs))
        return M(P.torres(hs) + "¿Qué torre es la más %s?" % ("baja" if low else "alta"), "la " + "ABC"[i], ["la " + "ABC"[j] for j in range(3) if j != i] + ["miden igual"],
                 "Contamos cubos: %s. La más %s es <b>la %s</b>." % (", ".join("%s: %d" % (l, h) for l, h in zip("ABC", hs)), "baja" if low else "alta", "ABC"[i]))
    if t == "pesa":
        ka, kb = R.sample(KINDS, 2)
        tilt = R.choice(["left", "right"])
        svg = P.pic(k_pics.balance_svg((ka, R.randint(1, 3)), (kb, R.randint(1, 3)), tilt), "balanza con %s de un lado y %s del otro" % (nombre(ka), nombre(kb)))
        heavy = ka if tilt == "left" else kb
        return M(svg + "Mira la balanza. ¿Qué lado pesa más?", "el lado de las %s" % nombre(heavy) if fem(heavy) else "el lado de los %s" % nombre(heavy),
                 [("el lado de las %s" % nombre(x) if fem(x) else "el lado de los %s" % nombre(x)) for x in (ka, kb) if x != heavy] + ["pesan igual", "no se puede saber"],
                 "El lado que baja es el que pesa más.")
    import f_common
    ws = [(R.choice([44, 56]), R.choice([70, 80, 90]), R.choice([.3, .5, .7, .9])) for _ in range(3)]
    vols = [w * h * lev for w, h, lev in ws]
    if len(set(vols)) < 3:
        return None
    full = R.random() < .5
    i = vols.index(max(vols) if full else min(vols))
    if not all(w == ws[0][0] for w, _, _ in ws):
        return None
    return M(fig(f_common.glasses_svg(ws)) + "Los vasos son del mismo ancho. ¿Cuál tiene %s agua?" % ("más" if full else "menos"), "el " + "ABC"[i], ["el " + "ABC"[j] for j in range(3) if j != i] + ["todos igual"],
             "En vasos iguales, el agua más %s indica %s: <b>el %s</b>." % ("alta" if full else "baja", "más" if full else "menos", "ABC"[i]))


# ============================================================ clasificar
GRUPOS = {"frutas": ["plátano", "manzana", "naranja", "mango", "sandía", "uva"], "animales": ["perro", "gato", "vaca", "caballo", "pato", "conejo"],
          "ropa": ["playera", "pantalón", "calcetín", "suéter", "falda", "gorra"], "transportes": ["camión", "carro", "bicicleta", "avión", "barco", "tren"],
          "útiles escolares": ["lápiz", "cuaderno", "goma", "tijeras", "crayola", "regla"]}


def clasificar(*ks):
    g, o = R.sample(sorted(GRUPOS), 2)
    xs = R.sample(GRUPOS[g], 3)
    odd = R.choice(GRUPOS[o])
    lst = xs + [odd]
    R.shuffle(lst)
    return M("¿Cuál <b>no</b> es del mismo grupo? %s" % ", ".join(lst), odd, xs + ["todos son del mismo grupo"], "%s son %s; <b>%s</b> no." % (", ".join(xs).capitalize(), g, odd))
