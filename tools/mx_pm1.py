# -*- coding: utf-8 -*-
"""
México, bachillerato: Pensamiento Matemático I (pensamiento estadístico y probabilístico, MCCEMS). Problemas propios.
setup(R) antes de usar. Cada función devuelve un problema en formato mexicano (punto decimal, 1 000 con espacio).
"""
import math
from fractions import Fraction as F
import mx_s1 as S1
from mx_s1 import M, fq, dexact, tabla_html, MINUS  # noqa: F401
from mx_common import num, dec, NB, CIUDADES  # noqa: F401
from ws_common import svg_wrap, text, line, fig

R = None
K = None


def setup(rnd):
    global R, K
    S1.setup(rnd)
    R = S1.R
    K = S1.K


def pick(ks, default):
    return R.choice(ks or default)


def name():
    return K.next()[0]


def d2(x, p=2):
    """decimal redondeado sin ceros de más: 0.40 → 0.4 (con signo −)"""
    if x < 0 and round(x, p) != 0:
        return MINUS + d2(-x, p)
    s = dec(round(x, p), p)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def pc(x, p=1):
    return d2(x, p) + NB + "%"


def mean(xs):
    return F(sum(xs), len(xs))


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def show(x):
    """Fraction → entero o decimal exacto; si no, 2 decimales"""
    x = F(x)
    return dexact(x) or d2(float(x), 2)


def lst(xs):
    return ", ".join(num(x) if x >= 0 else MINUS + num(-x) for x in xs)


def opt(q, ok, wrong, e):
    w = [x for x in dict.fromkeys(wrong) if x != ok]
    return M(q, ok, w[:3] if len(w) >= 3 else w, e)


def from_bank(items, prefix=""):
    q, a, w, e = R.choice(items)
    return opt(prefix + q, a, R.sample(w, min(3, len(w))) if len(w) > 3 else w, e)


# ============================================================ P1: variabilidad, aleatoriedad y decisiones
RANDOM = ["el número que sale al lanzar un dado", "el color de la siguiente canica que sacas de una bolsa sin mirar", "si mañana llueve en " + "Monterrey",
          "el número de clientes que llegan a una tienda en una hora", "la cara que cae al lanzar una moneda", "la carta que sale al revolver una baraja",
          "el tiempo que tarda el camión en llegar a la parada", "el número de goles de un partido", "el número premiado en un sorteo de lotería",
          "cuántos huevos pone una gallina en una semana", "el número de llamadas que recibe un call center en un día", "la estatura de un bebé al nacer"]
FIXED = ["la hora a la que sale el sol según el calendario astronómico", "el resultado de 25 × 4", "cuántos días tiene una semana", "el número de lados de un hexágono",
         "el área de un cuadrado de 5 cm de lado", "la temperatura a la que hierve el agua pura al nivel del mar", "cuántos minutos tiene una hora",
         "el perímetro de un rectángulo de 3 m por 7 m", "el precio de un artículo con el 10 % de descuento sobre $200", "cuántos meses tiene un año"]
STAT_Q = ["¿Cuántas horas duermen los alumnos de tu escuela?", "¿Cuánto gastan en transporte las familias de tu colonia?", "¿Qué deporte prefieren los estudiantes del grupo?",
          "¿Cuánto tiempo tardan los alumnos en llegar a la escuela?", "¿Cuántos libros leyeron este año los jóvenes de tu ciudad?", "¿Cuánto mide la mano de los alumnos del salón?",
          "¿Cuántos mensajes envían al día los estudiantes del plantel?", "¿Cuánta agua toman al día las personas de tu familia?"]
NONSTAT_Q = ["¿Cuántos años tiene mi hermana?", "¿A qué hora empieza hoy la clase de matemáticas?", "¿Cuánto mide el pizarrón del salón?", "¿Cuál es la capital de Jalisco?",
             "¿Cuántos alumnos hay en mi grupo hoy?", "¿Cuánto costó mi cuaderno?", "¿Cuántos lados tiene un triángulo?", "¿Qué día es hoy?"]


def p1(*ks):
    t = pick(ks, ["aleat", "fijo", "estad", "rango", "decide", "decide2"])
    if t in ("aleat", "fijo"):
        rnd = R.random() < .55
        sit = R.choice(RANDOM if rnd else FIXED)
        a = "aleatorio: no se puede saber el resultado antes" if rnd else "determinista: siempre da el mismo resultado"
        return opt("Fenómeno: <b>%s</b>. ¿Es aleatorio o determinista?" % sit, a,
                   ["determinista: siempre da el mismo resultado" if rnd else "aleatorio: no se puede saber el resultado antes", "aleatorio, porque tiene números", "determinista, porque se puede repetir"],
                   ("El resultado cambia cada vez y no se puede predecir: es <b>aleatorio</b>." if rnd else "Se calcula o se sabe con seguridad, sin variabilidad: es <b>determinista</b>."))
    if t == "estad":
        st = R.random() < .55
        qq = R.choice(STAT_Q if st else NONSTAT_Q)
        a = "sí, espera respuestas que varían" if st else "no, tiene una sola respuesta"
        return opt("«%s» ¿Es una pregunta estadística?" % qq, a, ["no, tiene una sola respuesta" if st else "sí, espera respuestas que varían", "sí, porque la respuesta es un número", "no, porque no se puede medir"],
                   ("Se espera que cada persona responda distinto: <b>sí es estadística</b>." if st else "Solo hay una respuesta, sin variabilidad: <b>no es estadística</b>."))
    if t == "rango":
        a = sorted(R.sample(range(10, 40), 5))
        b = sorted(R.sample(range(10, 40), 5))
        ra, rb = a[-1] - a[0], b[-1] - b[0]
        if ra == rb:
            return None
        ok = "la ruta A" if ra > rb else "la ruta B"
        return opt("Tiempos (minutos) de 5 viajes. Ruta A: %s. Ruta B: %s. ¿Qué ruta tiene <b>más variabilidad</b> (mayor rango)?" % (lst(a), lst(b)),
                   ok, ["la ruta B" if ok == "la ruta A" else "la ruta A", "las dos igual", "no se puede saber"],
                   "Rango A = %d − %d = %d; rango B = %d − %d = %d. Más variabilidad: <b>%s</b>." % (a[-1], a[0], ra, b[-1], b[0], rb, ok))
    # decide: misma media, distinta variabilidad → se prefiere la constante; decide2: elegir por media
    while True:
        m = R.randint(20, 35)
        da = [R.choice([-1, 0, 1]) for _ in range(4)]
        da.append(-sum(da))
        db = [R.choice([-8, -5, -3, 3, 5, 8]) for _ in range(4)]
        db.append(-sum(db))
        if abs(da[-1]) <= 2 and 0 < abs(db[-1]) <= 9:
            break
    A, B = [m + x for x in da], [m + x for x in db]
    if t == "decide":
        return opt("Dos camiones llevan a la escuela. Tiempos (min) en 5 días. Camión A: %s. Camión B: %s. Los dos tienen media de %d min. Si necesitas llegar siempre a tiempo, ¿cuál conviene?" % (lst(A), lst(B), m),
                   "el A, porque varía menos", ["el B, porque varía más", "da igual, tienen la misma media", "el B, porque a veces es más rápido"],
                   "Las medias son iguales, pero A va de %d a %d min y B de %d a %d min. Para llegar a tiempo conviene <b>el que varía menos (A)</b>." % (min(A), max(A), min(B), max(B)))
    B2 = [x + R.randint(4, 7) for x in A]
    mb = mean(B2)
    return opt("Tiempos (min) de dos trayectos en 5 días. Trayecto A: %s. Trayecto B: %s. ¿Cuál es más rápido en promedio?" % (lst(A), lst(B2)),
               "A, con media de %d min" % m, ["B, con media de %s min" % show(mb), "los dos tienen la misma media", "A, con media de %s min" % show(mb)],
               "Media A = %d ÷ 5 = %d min; media B = %d ÷ 5 = %s min. Más rápido: <b>A</b>." % (sum(A), m, sum(B2), show(mb)))


# ============================================================ P2: probabilidad frecuencial y simulación
EXPER = [("Se lanzó una tachuela %d veces y cayó con la punta hacia arriba %d veces.", "caiga con la punta hacia arriba"),
         ("Se lanzó un vaso de plástico %d veces y quedó de lado %d veces.", "quede de lado"),
         ("En una caseta de cobro pasaron %d carros y %d eran rojos.", "el siguiente carro sea rojo"),
         ("Se revisaron %d focos de una fábrica y %d salieron defectuosos.", "un foco salga defectuoso"),
         ("Un jugador tiró %d tiros libres y encestó %d.", "enceste el siguiente tiro libre"),
         ("En %d días de junio llovió %d días en la ciudad.", "llueva un día de junio"),
         ("Se lanzó un dado cargado %d veces y salió 6 en %d ocasiones.", "salga 6"),
         ("Una tienda registró %d compras y %d se pagaron con tarjeta.", "una compra se pague con tarjeta")]


def p2(*ks):
    t = pick(ks, ["fr", "fr", "pred", "pred", "concepto", "fiable", "pct"])
    if t == "concepto":
        items = [
            ("Si repites un experimento muchas más veces, la frecuencia relativa…", "se acerca cada vez más a la probabilidad", ["se aleja de la probabilidad", "siempre vale 0.5", "se vuelve exactamente igual a la probabilidad desde el inicio"], "Es la ley de los grandes números: con muchas repeticiones, la frecuencia relativa se estabiliza cerca de la probabilidad."),
            ("La frecuencia relativa de un resultado se calcula como…", "veces que ocurre ÷ total de repeticiones", ["total de repeticiones ÷ veces que ocurre", "veces que ocurre − total", "veces que ocurre × total"], "f<sub>r</sub> = número de veces que ocurre ÷ número total de repeticiones."),
            ("Una moneda se lanzó 10 veces y cayó águila 7 veces. ¿Qué se puede decir?", "con tan pocos lanzamientos es normal que no salga 5 de 10", ["la moneda está cargada con seguridad", "la probabilidad de águila es 0.7", "en los próximos 10 saldrá sol 7 veces"], "Con pocas repeticiones la frecuencia relativa varía mucho. Hacen falta muchos lanzamientos para estimar bien."),
            ("¿Para qué sirve una simulación (con dados, monedas o una computadora)?", "para estimar una probabilidad repitiendo un experimento muchas veces", ["para saber el resultado exacto del siguiente intento", "para evitar la variabilidad", "para que siempre gane el mismo"], "Simular permite repetir un experimento muchas veces de forma barata y estimar su probabilidad con la frecuencia relativa."),
            ("La probabilidad de un evento siempre está entre…", "0 y 1", ["−1 y 1", "1 y 100", "0 y 10"], "Una probabilidad es un número entre 0 (imposible) y 1 (seguro), o entre 0 % y 100 %."),
            ("Un evento con probabilidad 0.98 es…", "muy probable, pero no seguro", ["imposible", "seguro", "poco probable"], "0.98 está muy cerca de 1: es muy probable, pero puede no ocurrir."),
            ("¿Qué estimación de la probabilidad de que una tachuela caiga de punta es más confiable?", "la que se obtuvo con 2 000 lanzamientos", ["la que se obtuvo con 10 lanzamientos", "la que se obtuvo con 50 lanzamientos", "todas son igual de confiables"], "Más repeticiones → la frecuencia relativa se acerca más a la probabilidad."),
            ("La incertidumbre de un fenómeno aleatorio se debe a…", "su variabilidad: cada repetición puede dar un resultado distinto", ["un error de cálculo", "que nadie lo ha estudiado", "que no tiene resultados posibles"], "En lo aleatorio cada repetición puede cambiar; por eso no podemos saber el resultado con seguridad."),
        ]
        return from_bank(items)
    e, ev = R.choice(EXPER)
    n = R.choice([20, 25, 40, 50, 80, 100, 200, 250, 400, 500])
    k = R.randint(max(1, n // 10), n - n // 10)
    p = F(k, n)
    if t in ("fr", "pct"):
        if dexact(p) is None:
            return None
        if t == "fr":
            return opt((e % (n, k)) + " Estima la probabilidad de que %s." % ev, dexact(p), [dexact(F(n - k, n)), dexact(F(k, n * 10)) if k < n else "1", num(k)],
                       "Frecuencia relativa = %d ÷ %d = <b>%s</b>." % (k, n, dexact(p)))
        return opt((e % (n, k)) + " ¿Qué porcentaje de las veces ocurrió?", dexact(p * 100) + NB + "%", [dexact(F(n - k, n) * 100) + NB + "%", num(k) + NB + "%", dexact(p) + NB + "%"],
                   "%d ÷ %d = %s → <b>%s %%</b>." % (k, n, dexact(p), dexact(p * 100)))
    if t == "fiable":
        n1, n2 = R.choice([(10, 1000), (20, 500), (12, 1200), (30, 3000)])
        a = name()
        b = name()
        if a == b:
            return None
        return opt("Para estimar la probabilidad de que %s, %s hizo %d repeticiones y %s hizo %s. ¿Qué estimación es más confiable?" % (ev, a, n1, b, num(n2)),
                   "la de %s" % b, ["la de %s" % a, "son igual de confiables", "ninguna sirve"],
                   "Con más repeticiones la frecuencia relativa se acerca más a la probabilidad: <b>la de %s</b> (%s repeticiones)." % (b, num(n2)))
    m = R.choice([n * 2, n * 4, n * 5, n * 10, 1000, 2000])
    exp = p * m
    if exp.denominator != 1:
        return None
    return opt((e % (n, k)) + " Si se repite %s veces, ¿cuántas veces se espera que %s?" % (num(m), ev), num(int(exp)), [num(k), num(m - int(exp)), num(int(exp) + n)],
               "Probabilidad estimada = %d ÷ %d. Esperado = %s × %d ÷ %d = <b>%s</b>." % (k, n, num(m), k, n, num(int(exp))))


# ============================================================ P3: probabilidad teórica (equiprobabilidad)
def p3(*ks):
    t = pick(ks, ["dados", "urna", "equi", "comp", "ruleta", "grandes"])
    if t == "dados":
        s = R.randint(3, 11)
        k = 6 - abs(s - 7)
        p = F(k, 36)
        return opt("Se lanzan dos dados. ¿Cuál es la probabilidad de que la suma sea %d?" % s, fq(p), [fq(F(1, 11)), fq(F(k, 12)) if k != 3 else fq(F(1, 6)), fq(F(1, 36)) if k > 1 else fq(F(2, 36))],
                   "Hay 36 resultados igual de probables; %d dan suma %d. P = %d/36 = <b>%s</b>." % (k, s, k, fq(p)))
    if t == "urna":
        cols = R.sample(["rojas", "azules", "verdes", "amarillas", "blancas", "negras"], 3)
        n = [R.randint(2, 9) for _ in range(3)]
        tot = sum(n)
        i = R.randrange(3)
        p = F(n[i], tot)
        sing = {"rojas": "roja", "azules": "azul", "verdes": "verde", "amarillas": "amarilla", "blancas": "blanca", "negras": "negra"}
        return opt("Una bolsa tiene %d canicas %s, %d %s y %d %s. Se saca una sin mirar. ¿Cuál es la probabilidad de que sea %s?" % (n[0], cols[0], n[1], cols[1], n[2], cols[2], sing[cols[i]]),
                   fq(p), [fq(F(n[i], tot - n[i])) if tot - n[i] != n[i] else fq(F(1, 2)), fq(F(1, 3)), fq(F(tot - n[i], tot))],
                   "Casos favorables ÷ casos posibles = %d ÷ %d = <b>%s</b>." % (n[i], tot, fq(p)))
    if t == "equi":
        items = [
            ("¿En cuál de estos experimentos los resultados son <b>equiprobables</b>?", "lanzar un dado normal (sin cargar)", ["lanzar un dado cargado", "girar una ruleta con sectores de distinto tamaño", "lanzar una tachuela (punta arriba o de lado)"], "Un dado normal tiene 6 caras iguales: cada cara tiene probabilidad 1/6."),
            ("¿En cuál de estos experimentos los resultados <b>no</b> son equiprobables?", "girar una ruleta con un sector de 180° y dos de 90°", ["lanzar una moneda normal", "sacar una carta de una baraja revuelta", "lanzar un dado de 6 caras normal"], "El sector de 180° ocupa la mitad del círculo: tiene más probabilidad que los otros."),
            ("Suponer que todos los resultados son igual de probables es…", "una hipótesis que se puede comprobar con muchos ensayos", ["siempre verdadero", "siempre falso", "algo que no se puede comprobar"], "La equiprobabilidad es un supuesto. Si la frecuencia relativa se aleja mucho tras muchos ensayos, el supuesto es falso."),
            ("La regla de Laplace (favorables ÷ posibles) sirve cuando…", "todos los resultados son igual de probables", ["los resultados tienen distinta probabilidad", "hay infinitos resultados", "el experimento no es aleatorio"], "Solo podemos dividir favorables entre posibles si cada resultado es igual de probable."),
            ("Al lanzar dos monedas, ¿son equiprobables «dos águilas», «dos soles» y «un águila y un sol»?", "no: «un águila y un sol» tiene probabilidad 1/2", ["sí, cada uno tiene 1/3", "no: «dos águilas» tiene 1/2", "sí, cada uno tiene 1/4"], "Los resultados son AA, AS, SA, SS. «Un águila y un sol» ocurre de 2 formas: 2/4 = 1/2."),
            ("Se lanzó una moneda 5 000 veces y cayó águila 3 100 veces. ¿Qué puedes pensar?", "que la moneda probablemente no es equilibrada", ["que es normal, por azar", "que la probabilidad de águila es exactamente 1/2", "que la próxima vez caerá sol"], "Con 5 000 lanzamientos se esperaría cerca de 2 500 águilas. 3 100 (62 %) se aleja demasiado: la moneda parece cargada."),
        ]
        return from_bank(items)
    if t == "comp":
        a, b = sorted(R.sample(range(1, 20), 2))
        tot = b + R.randint(3, 20)
        p = F(a, tot)
        ev = R.choice(["ganar un premio", "sacar un boleto premiado", "que un foco salga defectuoso", "que el vuelo se retrase"])
        return opt("La probabilidad de %s es %s. ¿Cuál es la probabilidad de <b>no</b> %s?" % (ev, fq(p), ev.replace("que ", "") if ev.startswith("que") else ev),
                   fq(1 - p), [fq(p), fq(F(1, 2)), fq(1 - p + F(1, tot))],
                   "P(no A) = 1 − P(A) = 1 − %s = <b>%s</b>." % (fq(p), fq(1 - p)))
    if t == "ruleta":
        a_ = R.choice(range(30, 300, 30))
        b_ = R.choice(range(30, 330 - a_, 30))
        angs = (a_, b_, 360 - a_ - b_)
        cols = ["rojo", "azul", "verde"]
        i = R.randrange(3)
        p = F(angs[i], 360)
        return opt("Una ruleta tiene tres sectores: rojo de %d°, azul de %d° y verde de %d°. ¿Cuál es la probabilidad de que caiga en %s?" % (angs[0], angs[1], angs[2], cols[i]),
                   fq(p), [fq(F(1, 3)) if p != F(1, 3) else fq(F(1, 2)), fq(F(angs[i], 180)) if angs[i] < 180 else fq(F(1, 4)), fq(1 - p)],
                   "La probabilidad es la parte del círculo: %d ÷ 360 = <b>%s</b>." % (angs[i], fq(p)))
    n = R.choice([600, 1200, 1800, 3000, 6000])
    f = R.choice([1, 2, 3])
    exp = n * f // 6
    return opt("Se lanza un dado normal %s veces. ¿Alrededor de cuántas veces se espera que salga un número menor que %d?" % (num(n), f + 1), num(exp), [num(n // 6) if f > 1 else num(n // 3), num(n // 2) if f != 3 else num(n // 3), num(n - exp)],
               "P = %d/6. Esperado ≈ %s × %d/6 = <b>%s</b>. Con muchos lanzamientos la frecuencia se acerca a la probabilidad." % (f, num(n), f, num(exp)))


# ============================================================ P6: tipos de variables y fuentes de datos
VARS = [("el color favorito", "cualitativa nominal"), ("el estado de la república donde nació", "cualitativa nominal"), ("la marca de celular", "cualitativa nominal"),
        ("el tipo de sangre", "cualitativa nominal"), ("el medio de transporte a la escuela", "cualitativa nominal"), ("el deporte favorito", "cualitativa nominal"),
        ("el nivel de satisfacción (malo, regular, bueno, excelente)", "cualitativa ordinal"), ("el grado escolar", "cualitativa ordinal"), ("la talla de playera (CH, M, G)", "cualitativa ordinal"),
        ("el lugar de llegada en una carrera (1.º, 2.º, 3.º…)", "cualitativa ordinal"), ("el nivel de picor de una salsa (suave, medio, picante)", "cualitativa ordinal"),
        ("el número de hermanos", "cuantitativa discreta"), ("el número de mensajes enviados al día", "cuantitativa discreta"), ("el número de goles en un partido", "cuantitativa discreta"),
        ("el número de libros leídos en un año", "cuantitativa discreta"), ("el número de mascotas en casa", "cuantitativa discreta"), ("el número de faltas en el semestre", "cuantitativa discreta"),
        ("la estatura", "cuantitativa continua"), ("el peso de una mochila", "cuantitativa continua"), ("el tiempo de traslado a la escuela", "cuantitativa continua"),
        ("la temperatura máxima del día", "cuantitativa continua"), ("la cantidad de agua que toma al día", "cuantitativa continua"), ("la distancia de su casa a la escuela", "cuantitativa continua")]
TYPES = ["cualitativa nominal", "cualitativa ordinal", "cuantitativa discreta", "cuantitativa continua"]
SOURCES_OK = ["el INEGI (Instituto Nacional de Estadística y Geografía)", "el Banco de México", "el CONAPO (Consejo Nacional de Población)", "el Servicio Meteorológico Nacional",
              "la Secretaría de Salud", "una encuesta nacional con metodología publicada"]
SOURCES_BAD = ["un video viral en redes sociales", "un comentario en un foro", "una cadena de WhatsApp", "la opinión de un amigo", "un anuncio de publicidad", "una página sin autor ni fecha"]


def p6(*ks):
    t = pick(ks, ["tipo", "tipo", "tipo", "fuente", "pobl", "cual"])
    if t == "tipo":
        v, a = R.choice(VARS)
        return opt("En un estudio sobre los alumnos de un plantel se registra <b>%s</b>. ¿Qué tipo de variable es?" % v, a, [x for x in TYPES if x != a],
                   "Es <b>%s</b>: %s." % (a, {"cualitativa nominal": "son categorías sin orden", "cualitativa ordinal": "son categorías con un orden",
                                               "cuantitativa discreta": "es un número que se cuenta (0, 1, 2…)", "cuantitativa continua": "es un número que se mide y puede tener decimales"}[a]))
    if t == "cual":
        kind = R.choice(TYPES)
        if kind == "cuantitativa continua":
            lab, vals = R.choice([("estatura (m)", [dec(R.randint(148, 185) / 100, 2) for _ in range(5)]), ("peso de la mochila (kg)", [dec(R.randint(25, 90) / 10, 1) for _ in range(5)]),
                                  ("tiempo de traslado (min)", [dec(R.randint(50, 450) / 10, 1) for _ in range(5)]), ("temperatura (°C)", [dec(R.randint(150, 340) / 10, 1) for _ in range(5)])])
        elif kind == "cuantitativa discreta":
            lab, vals = R.choice([("número de hermanos", [str(R.randint(0, 5)) for _ in range(5)]), ("goles por partido", [str(R.randint(0, 6)) for _ in range(5)]),
                                  ("libros leídos en el año", [str(R.randint(0, 15)) for _ in range(5)]), ("faltas en el semestre", [str(R.randint(0, 9)) for _ in range(5)])])
        elif kind == "cualitativa nominal":
            lab, pool = R.choice([("color favorito", ["rojo", "azul", "verde", "negro", "morado", "blanco"]), ("estado de nacimiento", ["Jalisco", "Puebla", "Sonora", "Yucatán", "Oaxaca", "Nuevo León"]),
                                  ("deporte favorito", ["fútbol", "básquetbol", "voleibol", "natación", "béisbol", "atletismo"]), ("tipo de sangre", ["O+", "A+", "B+", "AB+", "O−", "A−"])])
            vals = [R.choice(pool) for _ in range(5)]
        else:
            lab, pool = R.choice([("talla de playera", ["CH", "M", "G", "EG"]), ("nivel de satisfacción", ["malo", "regular", "bueno", "excelente"]),
                                  ("nivel de inglés", ["básico", "intermedio", "avanzado"]), ("frecuencia de ejercicio", ["nunca", "a veces", "casi siempre", "siempre"])])
            vals = [R.choice(pool) for _ in range(5)]
        return opt("Datos de 5 alumnos (%s): %s. ¿Qué tipo de variable es?" % (lab, ", ".join(vals)), kind, [x for x in TYPES if x != kind],
                   "Es <b>%s</b>." % kind)
    if t == "fuente":
        a = R.choice(SOURCES_OK)
        tema = R.choice(["la población de tu estado", "la inflación del último año", "el número de hogares con internet", "las lluvias del mes pasado", "la tasa de desempleo",
                         "la esperanza de vida en México", "el tipo de cambio del peso", "los casos de dengue del año", "el número de migrantes por estado", "el promedio de escolaridad"])
        return opt("Quieres datos confiables sobre %s. ¿Qué fuente conviene?" % tema, a, R.sample(SOURCES_BAD, 3),
                   "Una fuente confiable es oficial o explica cómo obtuvo sus datos: <b>%s</b>." % a)
    pobl = R.choice([("los 1 200 alumnos de un plantel", "120 alumnos elegidos al azar", "las horas de sueño"), ("todos los hogares de Puebla", "800 hogares encuestados", "el gasto en luz"),
                     ("los clientes de un banco", "500 clientes elegidos al azar", "el saldo de ahorro"), ("los árboles de un parque", "60 árboles medidos", "la altura")])
    q = R.choice(["población", "muestra", "variable"])
    a = {"población": pobl[0], "muestra": pobl[1], "variable": pobl[2]}[q]
    w = [x for x in (pobl[0], pobl[1], pobl[2], "el promedio de los datos") if x != a]
    return opt("Se estudia %s de %s; para ello se toman datos de %s. ¿Cuál es la <b>%s</b>?" % (pobl[2], pobl[0], pobl[1], q), a, w,
               "Población: todos los que interesan (%s). Muestra: los que se estudian (%s). Variable: lo que se mide (%s)." % pobl)


# ============================================================ P7: gráficas (diagrama de puntos)
def dot_svg(vals, lab):
    lo, hi = min(vals), max(vals)
    w, h = 440, 170
    x0, x1 = 30, 410
    sx = lambda v: x0 + (v - lo) * (x1 - x0) / max(1, hi - lo)
    b = line(x0 - 10, 130, x1 + 10, 130)
    for v in range(lo, hi + 1):
        b += line(sx(v), 130, sx(v), 136) + text(sx(v), 154, str(v), 14, weight=400)
        c = vals.count(v)
        for j in range(c):
            b += "<circle cx='%.1f' cy='%.1f' r='6' fill='#2b6cb0'/>" % (sx(v), 120 - j * 14)
    b += text(w / 2, 168, lab, 13, weight=400)
    return svg_wrap(w, h + 4, b, "diagrama de puntos: " + lab)


def p7(*ks):
    t = pick(ks, ["moda", "cuantos", "mayor", "mediana", "cual"])
    if t == "cual":
        items = [
            ("Quieres mostrar cómo cambió la temperatura cada hora de un día. ¿Qué gráfica conviene?", "una gráfica de línea", ["una gráfica circular", "un diagrama de puntos de colores", "una tabla de doble entrada"], "Para cambios en el tiempo se usa una gráfica de línea."),
            ("Quieres mostrar qué parte del gasto mensual de una familia va a cada rubro. ¿Qué gráfica conviene?", "una gráfica circular", ["una gráfica de línea", "un histograma", "un diagrama de dispersión"], "Las partes de un total se ven bien en una gráfica circular."),
            ("Tienes las estaturas de 200 alumnos agrupadas en intervalos de 5 cm. ¿Qué gráfica conviene?", "un histograma", ["una gráfica circular", "una gráfica de línea", "un pictograma"], "Para datos cuantitativos continuos agrupados en intervalos se usa un histograma."),
            ("Quieres comparar el deporte favorito de los alumnos (fútbol, básquetbol, voleibol…). ¿Qué gráfica conviene?", "una gráfica de barras", ["un histograma", "una gráfica de línea", "un diagrama de dispersión"], "Para una variable cualitativa se usan barras separadas."),
            ("Quieres ver si hay relación entre horas de estudio y calificación. ¿Qué gráfica conviene?", "un diagrama de dispersión", ["una gráfica circular", "un histograma", "una gráfica de barras"], "Para dos variables cuantitativas se usa un diagrama de dispersión."),
            ("En un histograma, ¿por qué las barras van juntas (sin espacio)?", "porque los intervalos son continuos", ["para ahorrar espacio", "porque es una variable cualitativa", "porque todas las barras miden igual"], "Los intervalos de un histograma se tocan: la variable es continua."),
            ("Tienes las calificaciones (de 5 a 10) de 25 alumnos. ¿Qué gráfica muestra cada dato como un punto sobre una recta?", "un diagrama de puntos", ["una gráfica circular", "una gráfica de línea", "un diagrama de árbol"], "En un diagrama de puntos cada dato es un punto sobre su valor."),
        ]
        return from_bank(items)
    lab, lo = R.choice([("calificaciones del examen", 5), ("número de hermanos", 0), ("horas de sueño", 5), ("goles por partido", 0), ("libros leídos en el mes", 0)])
    hi = 10 if lab.startswith("calif") else lo + R.randint(4, 6)
    vals = []
    for v in range(lo, hi + 1):
        vals += [v] * R.randint(0, 6)
    if len(vals) < 8:
        return None
    cnt = {v: vals.count(v) for v in range(lo, hi + 1)}
    pic = fig(dot_svg(vals, lab))
    if t == "moda":
        mx = max(cnt.values())
        md = [v for v in cnt if cnt[v] == mx]
        if len(md) > 1:
            return None
        md = md[0]
        w = [str(v) for v in R.sample([v for v in cnt if v != md], 2)] + [str(mx)] if str(mx) != str(md) else [str(v) for v in R.sample([v for v in cnt if v != md], 3)]
        return opt(pic + "El diagrama muestra las %s de un grupo. ¿Cuál es la moda?" % lab, str(md), w, "La columna más alta está en <b>%d</b> (%d datos)." % (md, mx))
    if t == "cuantos":
        return opt(pic + "Cada punto es una persona (%s). ¿Cuántas personas hay?" % lab, str(len(vals)), [str(hi - lo + 1), str(max(cnt.values())), str(len(vals) + 1)],
                   "Contamos todos los puntos: <b>%d</b>." % len(vals))
    if t == "mayor":
        c = R.randint(lo + 1, hi)
        v = sum(1 for x in vals if x >= c)
        if v == 0:
            return None
        return opt(pic + "Datos: %s. ¿Cuántos datos valen %d o más?" % (lab, c), str(v), [str(cnt[c]), str(len(vals) - v), str(v + 1)],
                   "Sumamos los puntos desde %d: <b>%d</b>." % (c, v))
    m = median(vals)
    w = [show(mean(vals)), show(m + 1), show(m - 1) if m > lo else show(m + F(1, 2))]
    return opt(pic + "Datos: %s (%d datos). ¿Cuál es la mediana?" % (lab, len(vals)), show(m), w,
               "Ordenados, %s. Mediana = <b>%s</b>." % ("el dato central es el número %d" % (len(vals) // 2 + 1) if len(vals) % 2 else "se promedian los datos %d y %d" % (len(vals) // 2, len(vals) // 2 + 1), show(m)))


# ============================================================ P8: tablas de doble entrada, independencia y riesgo relativo
EXPO = [("Fuma", "No fuma", "Tos crónica", "Sin tos"), ("Duerme menos de 6 h", "Duerme 6 h o más", "Reprueba", "Aprueba"),
        ("Usa casco", "No usa casco", "Lesión grave", "Sin lesión grave"), ("Se vacunó", "No se vacunó", "Se enfermó", "No se enfermó"),
        ("Desayuna", "No desayuna", "Se cansa en clase", "No se cansa")]


def p8(*ks):
    t = pick(ks, ["rr", "riesgo", "indep", "marg", "interp"])
    ex, nex, out, nout = R.choice(EXPO)
    while True:
        n1, n2 = R.choice([50, 80, 100, 120, 150, 200, 250]), R.choice([50, 80, 100, 150, 200, 300])
        a = R.randint(2, n1 // 2)
        c = R.randint(2, n2 // 2)
        if t == "indep":
            if R.random() < .5:
                n2 = n1 * R.choice([1, 2, 3])
                c = a * (n2 // n1)
            break
        r1, r2 = F(a, n1), F(c, n2)
        if r1 != r2 and dexact(r1) and dexact(r2) and len(dexact(r1)) <= 5 and len(dexact(r2)) <= 5:
            break
    b, d = n1 - a, n2 - c
    tab = tabla_html(["", out, nout, "Total"], [[ex, num(a), num(b), num(n1)], [nex, num(c), num(d), num(n2)]])
    r1, r2 = F(a, n1), F(c, n2)
    if t == "riesgo":
        return opt(tab + "¿Cuál es el riesgo de «%s» en el grupo «%s»?" % (out.lower(), ex.lower()), dexact(r1), [d2(float(F(a, a + c)), 3), dexact(r2), d2(float(F(a, n1 + n2)), 3)],
                   "Riesgo = %d ÷ %d = <b>%s</b> (casos con el resultado ÷ total del grupo)." % (a, n1, dexact(r1)))
    if t == "rr":
        rr = r1 / r2
        return opt(tab + "Calcula el <b>riesgo relativo</b> de «%s» para «%s» respecto a «%s» (a dos decimales)." % (out.lower(), ex.lower(), nex.lower()),
                   d2(float(rr)), [d2(float(1 / rr)), d2(float(r1 - r2)), d2(float(F(a, c)))],
                   "RR = (%d/%d) ÷ (%d/%d) = %s ÷ %s ≈ <b>%s</b>." % (a, n1, c, n2, dexact(r1), dexact(r2), d2(float(rr))))
    if t == "interp":
        rr = R.choice([F(1, 2), F(2), F(3), F(1), F(3, 2), F(1, 4)])
        a_ = {F(2): "el riesgo es el doble en el grupo expuesto", F(3): "el riesgo es el triple en el grupo expuesto", F(1): "el riesgo es igual en los dos grupos",
              F(1, 2): "el riesgo es la mitad en el grupo expuesto", F(3, 2): "el riesgo es 1.5 veces mayor en el grupo expuesto", F(1, 4): "el riesgo es la cuarta parte en el grupo expuesto"}
        return opt("En un estudio, el riesgo relativo de enfermarse para quienes viven cerca de una fábrica es RR = %s. ¿Qué significa?" % show(rr), a_[rr], [v for k, v in a_.items() if k != rr][:3],
                   "RR = riesgo expuestos ÷ riesgo no expuestos = %s → <b>%s</b>." % (show(rr), a_[rr]))
    if t == "marg":
        return opt(tab + "¿Qué proporción de <b>todas</b> las personas tiene «%s»?" % out.lower(), dexact(F(a + c, n1 + n2)) or d2(float(F(a + c, n1 + n2)), 3),
                   [dexact(r1) or "0.5", dexact(F(a, a + c)) or d2(float(F(a, a + c)), 3), dexact(F(a + c, n1)) or d2(float(F(a + c, n1)), 3)],
                   "(%d + %d) ÷ %d = <b>%s</b>." % (a, c, n1 + n2, dexact(F(a + c, n1 + n2)) or d2(float(F(a + c, n1 + n2)), 3)))
    ok = "son independientes" if r1 == r2 else "no son independientes"
    return opt(tab + "¿Las variables «%s» y «%s» parecen independientes?" % (ex.lower() + " o no", out.lower() + " o no"), ok,
               ["son independientes" if ok != "son independientes" else "no son independientes", "no se puede saber con una tabla", "solo si los totales son iguales"],
               "Comparamos proporciones: %d/%d = %s y %d/%d = %s. %s" % (a, n1, dexact(r1) or d2(float(r1), 3), c, n2, dexact(r2) or d2(float(r2), 3),
                                                                          "Son iguales → <b>independientes</b>." if r1 == r2 else "Son distintas → <b>no son independientes</b>."))


# ============================================================ P10: valores atípicos, confusión y paradoja de Simpson
def p10(*ks):
    t = pick(ks, ["media", "cual", "iqr", "confusion", "simpson", "robusta"])
    if t in ("media", "cual"):
        xs = sorted(R.sample(range(10, 30), 5))
        out = R.choice([xs[-1] * R.randint(4, 8), 120, 150, 200])
        ys = xs + [out]
        if t == "cual":
            return opt("Sueldos semanales (en cientos de pesos) de 6 empleados: %s. ¿Cuál es un valor atípico?" % lst(sorted(ys, key=lambda _: R.random())), num(out),
                       [num(xs[0]), num(xs[2]), num(xs[-1])], "<b>%d</b> está muy lejos de los demás datos (de %d a %d)." % (out, xs[0], xs[-1]))
        m1, m2 = mean(xs), mean(ys)
        if m1.denominator not in (1, 2, 4, 5) or m2.denominator not in (1, 2, 4, 5):
            return None
        return opt("Datos: %s. Su media es %s. Si se agrega el dato %d, ¿cuál es la nueva media?" % (lst(xs), show(m1), out), show(m2), [show(m1), show(median(ys)), show(m2 + 5)],
                   "Nueva media = (%d + %d) ÷ 6 = <b>%s</b>. Un solo dato atípico cambia mucho la media." % (sum(xs), out, show(m2)))
    if t == "robusta":
        items = [
            ("Si en un conjunto de datos hay un valor atípico muy grande, ¿qué medida describe mejor el centro?", "la mediana", ["la media", "el rango", "el valor máximo"], "La mediana casi no cambia con un dato extremo; la media sí."),
            ("En una colonia, casi todos ganan entre $8 000 y $15 000, pero un vecino gana $900 000. ¿Qué pasa con la media?", "sube mucho y ya no representa a la mayoría", ["no cambia", "baja", "queda igual que la mediana"], "Un valor extremo jala la media hacia él. La mediana representa mejor."),
            ("Un valor atípico puede deberse a…", "un error de medición o un caso realmente excepcional", ["siempre a un error", "nunca a un error", "que la media está mal calculada"], "Antes de quitar un atípico hay que investigar: puede ser error o un dato real."),
            ("¿Qué medida de dispersión cambia más con un valor atípico?", "el rango", ["el rango intercuartílico", "la mediana", "la moda"], "El rango usa el mayor y el menor dato, así que un atípico lo cambia mucho."),
            ("Una variable de confusión es…", "una tercera variable que influye en las dos variables estudiadas", ["un error de cálculo", "la variable que se mide", "un dato atípico"], "Si una tercera variable afecta a las dos, puede parecer que una causa a la otra sin ser así."),
            ("Que dos variables estén correlacionadas significa que…", "varían juntas, pero no necesariamente una causa la otra", ["una causa la otra", "no tienen relación", "son la misma variable"], "Correlación no implica causalidad: puede haber una variable de confusión."),
        ]
        return from_bank(items)
    if t == "iqr":
        while True:
            xs = sorted(R.randint(10, 40) for _ in range(7))
            q1, q3 = xs[1], xs[5]
            if q3 > q1:
                break
        iq = q3 - q1
        up = q3 + F(3, 2) * iq
        out = int(up) + R.randint(2, 15)
        data = xs + [out]
        s = sorted(data)
        q1, q3 = median(s[:4]), median(s[4:])
        iq = q3 - q1
        lo_f, up_f = q1 - F(3, 2) * iq, q3 + F(3, 2) * iq
        if out <= up_f:
            return None
        return opt("Datos ordenados: %s. Q₁ = %s y Q₃ = %s. Según la regla de 1.5 × RIC, ¿a partir de qué valor un dato es atípico por arriba?" % (lst(s), show(q1), show(q3)),
                   show(up_f), [show(q3 + iq), show(q3), show(up_f + iq)],
                   "RIC = %s − %s = %s. Límite = Q₃ + 1.5 × RIC = %s + %s = <b>%s</b>. El dato %d es atípico." % (show(q3), show(q1), show(iq), show(q3), show(F(3, 2) * iq), show(up_f), out))
    if t == "confusion":
        items = [("En verano se venden más helados y también hay más accidentes en albercas.", "el calor"), ("Las ciudades con más bomberos tienen más incendios.", "el tamaño de la ciudad"),
                 ("Los niños con pies más grandes leen mejor.", "la edad"), ("Las personas que llevan encendedor tienen más enfermedades del pulmón.", "fumar"),
                 ("En los días con más paraguas en la calle hay más choques.", "la lluvia"), ("Las casas con más televisores tienen hijos con mejores calificaciones.", "el nivel de ingresos de la familia"),
                 ("Los municipios con más hospitales tienen más muertes.", "el número de habitantes")]
        s, a = R.choice(items)
        w = [x for _, x in items if x != a]
        return opt(s + " ¿Qué variable de confusión explica mejor esta relación?", a, R.sample(w, 3), "<b>%s</b> influye en las dos variables; por eso parecen relacionadas sin que una cause la otra." % (a[0].upper() + a[1:]))
    # Simpson
    a1, n1 = R.choice([(18, 20), (27, 30), (45, 50)])
    a2, n2 = R.choice([(70, 100), (140, 200), (56, 80)])
    b1, m1 = R.choice([(80, 100), (160, 200)])
    b2, m2 = R.choice([(6, 10), (12, 20), (15, 25)])
    if not (F(a1, n1) > F(b1, m1) and F(a2, n2) > F(b2, m2) and F(a1 + a2, n1 + n2) < F(b1 + b2, m1 + m2)):
        return None
    tab = tabla_html(["", "Casos leves", "Casos graves", "Total"],
                     [["Hospital A (recuperados)", "%d de %d" % (a1, n1), "%d de %d" % (a2, n2), "%d de %d" % (a1 + a2, n1 + n2)],
                      ["Hospital B (recuperados)", "%d de %d" % (b1, m1), "%d de %d" % (b2, m2), "%d de %d" % (b1 + b2, m1 + m2)]])
    q = R.choice(["total", "leves", "explica"])
    if q == "total":
        return opt(tab + "Considerando el total, ¿qué hospital tiene mayor porcentaje de recuperación?", "el B", ["el A", "los dos igual", "no se puede calcular"],
                   "A: %d/%d ≈ %s; B: %d/%d ≈ %s. En el total gana <b>el B</b>." % (a1 + a2, n1 + n2, pc(100 * (a1 + a2) / (n1 + n2)), b1 + b2, m1 + m2, pc(100 * (b1 + b2) / (m1 + m2))))
    if q == "leves":
        return opt(tab + "En cada tipo de caso (leves y graves), ¿qué hospital recupera mejor?", "el A en los dos tipos", ["el B en los dos tipos", "el A en leves y el B en graves", "son iguales"],
                   "Leves: A %s, B %s. Graves: A %s, B %s. <b>El A gana en los dos</b>, aunque en el total gana B: es la paradoja de Simpson." % (pc(100 * a1 / n1), pc(100 * b1 / m1), pc(100 * a2 / n2), pc(100 * b2 / m2)))
    return opt(tab + "A gana en casos leves y en graves, pero B gana en el total. ¿Por qué?", "porque A atiende muchos más casos graves", ["porque B tiene mejores doctores", "por un error de suma", "porque A atiende menos pacientes en total"],
               "A recibe %d casos graves de %d y B solo %d de %d. Los casos graves bajan el total de A: <b>paradoja de Simpson</b>." % (n2, n1 + n2, m2, m1 + m2))


# ============================================================ P11: muestreo y variabilidad muestral
SAMPLING = [("Se numeran los 900 alumnos y se eligen 90 números con un sorteo.", "aleatorio simple"),
            ("De una lista de 1 000 clientes se elige uno al azar entre los 10 primeros y después uno de cada 10.", "sistemático"),
            ("Se divide a los alumnos por semestre y se elige al azar el 10 % de cada semestre.", "estratificado"),
            ("Se eligen al azar 5 grupos completos de la escuela y se encuesta a todos sus alumnos.", "por conglomerados"),
            ("Se eligen al azar 200 números de teléfono del directorio de la ciudad.", "aleatorio simple"),
            ("En una fábrica se revisa cada pieza número 50 de la línea de producción.", "sistemático"),
            ("Se encuesta a hombres y mujeres en la misma proporción que hay en el municipio, eligiendo al azar en cada grupo.", "estratificado"),
            ("Se eligen al azar 8 colonias de la ciudad y se visitan todas sus casas.", "por conglomerados")]
SAMPLE_T = ["aleatorio simple", "sistemático", "estratificado", "por conglomerados"]
BIAS = [("Para saber cuánto ejercicio hacen los jóvenes, se encuesta solo a quienes están en un gimnasio.", "sí, porque esas personas hacen más ejercicio que el promedio"),
        ("Para saber qué música prefiere la escuela, se pregunta solo al grupo de banda de guerra.", "sí, porque ese grupo no representa a toda la escuela"),
        ("Un programa de radio pide que los oyentes llamen para opinar.", "sí, porque solo llaman quienes quieren y escuchan ese programa"),
        ("Para estimar el ingreso de una ciudad, se encuesta solo en una colonia residencial.", "sí, porque esa colonia tiene ingresos más altos"),
        ("Para saber si gusta la comida de la cafetería, se pregunta a quienes están comiendo ahí.", "sí, porque quienes no compran ahí quedan fuera")]


def p11(*ks):
    t = pick(ks, ["tipo", "sesgo", "var", "tam", "est"])
    if t == "tipo":
        s, a = R.choice(SAMPLING)
        return opt(s + " ¿Qué tipo de muestreo es?", a, [x for x in SAMPLE_T if x != a], "Es un muestreo <b>%s</b>." % a)
    if t == "sesgo":
        s, a = R.choice(BIAS)
        return opt(s + " ¿La muestra tiene sesgo?", a, ["no, porque se encuestó a muchas personas", "no, porque las personas eligieron participar", "no, siempre que se pregunte con respeto"],
                   "<b>%s</b>. Una muestra aleatoria evita este problema." % (a[0].upper() + a[1:]))
    if t == "var":
        items = [
            ("Cinco equipos toman muestras aleatorias distintas de 50 alumnos y calculan la estatura media. ¿Qué es lo esperado?", "que obtengan medias parecidas pero no iguales", ["que obtengan exactamente la misma media", "que las medias no se parezcan en nada", "que alguno se equivocó si no coincide"], "Es la <b>variabilidad muestral</b>: cada muestra da un resultado un poco distinto."),
            ("Si aumentas el tamaño de las muestras, las medias muestrales…", "varían menos entre sí", ["varían más entre sí", "dejan de variar por completo", "se alejan de la media de la población"], "Con muestras más grandes, las medias muestrales se agrupan más cerca de la media real."),
            ("¿Por qué es importante que la muestra sea aleatoria?", "para que todos tengan la misma oportunidad de ser elegidos y evitar sesgos", ["para que la muestra sea pequeña", "para que salgan los resultados que esperamos", "para no tener que calcular nada"], "Al azar, ningún grupo queda favorecido: la muestra representa mejor a la población."),
            ("Un parámetro es…", "un valor de la población (por ejemplo, la media de todos)", ["un valor de una muestra", "un tipo de gráfica", "una variable cualitativa"], "Parámetro: de la población. Estadístico: de la muestra."),
            ("Un estadístico es…", "un valor calculado con los datos de una muestra", ["un valor de toda la población", "una persona que encuesta", "una variable de confusión"], "El estadístico (como x̄) se calcula en la muestra y sirve para estimar el parámetro."),
            ("Un censo es…", "un estudio de toda la población", ["una muestra pequeña", "un muestreo sistemático", "una encuesta por teléfono"], "En un censo se toman datos de todos, como el Censo de Población del INEGI."),
        ]
        return from_bank(items)
    if t == "tam":
        n = R.choice([400, 600, 800, 1000, 1200, 1500, 2000])
        pp = R.choice([10, 15, 20, 25, 30, 40])
        return opt("Una escuela tiene %s alumnos y se quiere una muestra del %d %%. ¿Cuántos alumnos debe tener la muestra?" % (num(n), pp), num(n * pp // 100),
                   [num(pp), num(n // pp), num(n * pp // 10)], "%d %% de %s = %s × %s = <b>%s</b>." % (pp, num(n), num(n), d2(pp / 100), num(n * pp // 100)))
    # estratificado proporcional
    sz = [R.randrange(100, 700, 20) for _ in range(3)]
    tot = sum(sz)
    k = R.choice([10, 20])
    if tot % k:
        return None
    n = tot // k
    i = R.randrange(3)
    lab = ["primer semestre", "tercer semestre", "quinto semestre"]
    return opt("Un plantel tiene %s alumnos de %s, %s de %s y %s de %s. Se toma una muestra estratificada proporcional de %d alumnos. ¿Cuántos deben ser de %s?" % (num(sz[0]), lab[0], num(sz[1]), lab[1], num(sz[2]), lab[2], n, lab[i]),
               num(sz[i] // k), [num(n // 3) if n // 3 != sz[i] // k else num(n // 2), num(sz[i] // (k * 2)), num(sz[i] // k + 5)],
               "%s ÷ %s × %d = <b>%d</b> (la muestra es 1 de cada %d alumnos de cada semestre)." % (num(sz[i]), num(tot), n, sz[i] // k, k))


# ============================================================ P12: estudios observacionales y experimentos
TOPICS = [("tomar té verde", "la presión arterial"), ("usar una nueva app de estudio", "la calificación del examen"), ("hacer 30 minutos de ejercicio diario", "las horas de sueño"),
          ("tomar un nuevo medicamento", "el dolor de cabeza"), ("usar un fertilizante nuevo", "el crecimiento de las plantas"), ("escuchar música al estudiar", "la memoria"),
          ("desayunar avena", "el nivel de energía"), ("usar lentes con filtro de luz azul", "el cansancio de la vista")]


def p12(*ks):
    t = pick(ks, ["tipo", "tipo", "control", "causa", "concepto"])
    x, y = R.choice(TOPICS)
    n = R.choice([40, 60, 80, 100, 120, 200])
    if t == "tipo":
        exp = R.random() < .5
        if exp:
            s = "Se eligen %d voluntarios y se asignan <b>al azar</b> a dos grupos: uno debe %s y el otro no. Después se mide %s." % (n, x, y)
        else:
            s = "Se pregunta a %d personas si suelen %s y se registra %s, sin cambiar sus hábitos." % (n, x, y)
        a = "un experimento" if exp else "un estudio observacional"
        return opt(s + " ¿Qué tipo de estudio es?", a, ["un estudio observacional" if exp else "un experimento", "un censo", "una simulación"],
                   ("El investigador decide quién recibe el tratamiento: es <b>un experimento</b>." if exp else "Solo se observa lo que las personas ya hacen: es <b>un estudio observacional</b>."))
    if t == "control":
        return opt("En un experimento para saber si %s influye en %s, %d personas se dividen al azar en dos grupos. ¿Cuál es el grupo control?" % (x, y, n),
                   "el grupo que no recibe el tratamiento (o recibe un placebo)", ["el grupo que sí recibe el tratamiento", "el grupo con mejores resultados", "las personas que eligieron participar"],
                   "El grupo control sirve para comparar: <b>no recibe el tratamiento</b> o recibe un placebo.")
    if t == "causa":
        exp = R.random() < .5
        s = ("En un experimento con asignación al azar, quienes debían %s tuvieron mejores resultados en %s que el grupo control." if exp else
             "En un estudio observacional, las personas que suelen %s tienen mejores resultados en %s.") % (x, y)
        a = ("sí, el experimento aleatorizado permite concluir causa" if exp else "no, solo hay asociación: puede haber variables de confusión")
        w = ["no, nunca se puede concluir causa", "sí, siempre que haya muchas personas", "no, solo hay asociación: puede haber variables de confusión" if exp else "sí, el experimento aleatorizado permite concluir causa"]
        return opt(s + " ¿Se puede concluir que %s <b>causa</b> esa diferencia?" % x, a, w,
                   "Asignar al azar reparte por igual las demás variables; sin eso, otra variable podría explicar la diferencia." if exp else "En un estudio observacional los grupos pueden diferir en otras cosas (edad, dieta…).")
    items = [
        ("¿Para qué se asigna al azar a los participantes de un experimento?", "para que los grupos sean parecidos en todo, salvo el tratamiento", ["para que el estudio sea más barato", "para elegir a los más sanos", "para que todos reciban el tratamiento"], "La aleatorización reparte por igual las demás variables entre los grupos."),
        ("Un placebo es…", "una sustancia o tratamiento sin efecto que parece real", ["el medicamento que se prueba", "el grupo con más personas", "un error de medición"], "El placebo permite separar el efecto real del efecto de creer que te tratan."),
        ("En un estudio doble ciego…", "ni los participantes ni quienes miden saben quién recibe el tratamiento", ["los participantes no ven bien", "solo el investigador sabe el resultado", "se repite el estudio dos veces"], "Así se evita que las expectativas influyan en los resultados."),
        ("¿Cuál es una ventaja de un estudio observacional?", "se puede hacer cuando un experimento no sería ético o posible", ["demuestra causa y efecto", "no tiene variables de confusión", "no necesita datos"], "Por ejemplo, no se puede obligar a alguien a fumar: se observa a quienes ya fuman."),
        ("¿Cuál es una limitación de un estudio observacional?", "no permite concluir causa y efecto", ["no se pueden medir variables", "siempre usa pocas personas", "requiere un placebo"], "Puede haber variables de confusión que expliquen la relación."),
        ("¿Por qué no sería ético hacer un experimento para saber si fumar causa cáncer?", "porque habría que obligar a personas a fumar", ["porque es muy barato", "porque no hay fumadores", "porque los datos serían cualitativos"], "Cuando un tratamiento puede dañar, se usan estudios observacionales."),
        ("Replicar un experimento significa…", "repetirlo con otros participantes para ver si se obtiene lo mismo", ["copiar los resultados de otro", "usar un placebo", "elegir una muestra sesgada"], "Si un resultado se repite en varios estudios, es más confiable."),
    ]
    return from_bank(items)


# ============================================================ P13: medidas de tendencia central y dispersión
def p13(*ks):
    t = pick(ks, ["media", "mediana", "var", "sd", "ric", "interp"])
    n = R.choice([5, 6, 7, 8])
    xs = [R.randint(2, 20) for _ in range(n)]
    if t == "media":
        m = mean(xs)
        if m.denominator not in (1, 2, 4, 5, 8):
            return None
        return opt("Calcula la media de: %s." % lst(xs), show(m), [show(median(xs)) if median(xs) != m else show(m + 1), show(F(sum(xs), n - 1)), show(m + F(1, 2))],
                   "Media = %d ÷ %d = <b>%s</b>." % (sum(xs), n, show(m)))
    if t == "mediana":
        m = median(xs)
        return opt("Calcula la mediana de: %s." % lst(xs), show(m), [show(F(xs[n // 2])) if F(xs[n // 2]) != m else show(m + 1), show(mean(xs)) if mean(xs) != m else show(m - 1), show(m + F(1, 2))],
                   "Ordenados: %s. Mediana = <b>%s</b>." % (lst(sorted(xs)), show(m)))
    if t in ("var", "sd"):
        while True:
            m = R.randint(5, 15)
            ds = R.choice([[-2, -1, 0, 1, 2], [-3, -1, 1, 3], [-4, -2, 0, 2, 4], [-2, -2, 2, 2], [-3, 0, 0, 3], [-5, -1, 1, 5], [-1, -1, 1, 1], [-6, 0, 6], [-3, -3, 3, 3], [-4, 0, 0, 4]])
            xs = [m + d for d in ds]
            v = F(sum(d * d for d in ds), len(ds))
            if t == "var" or v.denominator == 1 and int(math.isqrt(int(v))) ** 2 == v:
                break
        R.shuffle(xs)
        if t == "var":
            return opt("Datos: %s (media %d). Calcula la varianza poblacional σ²." % (lst(xs), m), show(v), [show(F(sum(d * d for d in ds), len(ds) - 1)), show(F(sum(abs(d) for d in ds), len(ds))), show(F(math.sqrt(v)).limit_denominator(100))],
                       "σ² = (%s) ÷ %d = %d ÷ %d = <b>%s</b>." % (" + ".join("%d" % (d * d) for d in ds), len(ds), sum(d * d for d in ds), len(ds), show(v)))
        s = math.isqrt(int(v))
        return opt("Datos: %s (media %d). Calcula la desviación estándar poblacional σ." % (lst(xs), m), num(s), [show(v), show(F(sum(abs(d) for d in ds), len(ds))) if F(sum(abs(d) for d in ds), len(ds)) != s else num(s + 1), num(max(xs) - min(xs))],
                   "σ² = %d ÷ %d = %s; σ = √%s = <b>%d</b>." % (sum(d * d for d in ds), len(ds), show(v), show(v), s))
    if t == "ric":
        xs = sorted(R.sample(range(1, 60), 8))
        q1, q3 = median(xs[:4]), median(xs[4:])
        return opt("Datos ordenados: %s. Calcula el rango intercuartílico (Q₃ − Q₁)." % lst(xs), show(q3 - q1), [num(xs[-1] - xs[0]), show(q3), show(median(xs) - q1)],
                   "Q₁ = mediana de la primera mitad = %s; Q₃ = %s. RIC = <b>%s</b>." % (show(q1), show(q3), show(q3 - q1)))
    items = [
        ("Dos grupos tienen la misma media en un examen; el grupo A tiene σ = 2 y el B tiene σ = 9. ¿Qué significa?", "las calificaciones de A están más concentradas cerca de la media", ["el grupo B tiene mejores calificaciones", "el grupo A tiene más alumnos", "los dos grupos son iguales"], "Una σ menor indica datos más cercanos a la media."),
        ("Si a todos los datos se les suma 5, la desviación estándar…", "no cambia", ["aumenta en 5", "se multiplica por 5", "disminuye"], "Sumar lo mismo mueve todos los datos, pero no cambia qué tan separados están."),
        ("Si todos los datos se multiplican por 3, la desviación estándar…", "se multiplica por 3", ["no cambia", "aumenta en 3", "se multiplica por 9"], "Multiplicar estira la separación: σ se multiplica por 3 (y la varianza por 9)."),
        ("La desviación estándar es 0 cuando…", "todos los datos son iguales", ["la media es 0", "hay datos negativos", "hay pocos datos"], "σ = 0 significa que no hay variación."),
        ("¿Qué relación hay entre varianza y desviación estándar?", "la desviación estándar es la raíz cuadrada de la varianza", ["son iguales", "la varianza es la mitad", "la desviación estándar es el cuadrado de la varianza"], "σ = √σ². La σ tiene las mismas unidades que los datos."),
        ("¿Qué medida de tendencia central conviene para la variable «marca de celular favorita»?", "la moda", ["la media", "la mediana", "la desviación estándar"], "Para datos cualitativos nominales solo tiene sentido la moda."),
    ]
    return from_bank(items)


# ============================================================ P14: distribución normal (regla empírica)
def p14(*ks):
    t = pick(ks, ["regla", "regla", "z", "comp", "concepto"])
    ctx = R.choice([("la estatura de los jóvenes de 15 años", 160, 7, "cm"), ("el peso de las bolsas de café", 500, 4, "g"), ("la duración de unas pilas", 30, 3, "horas"),
                    ("la calificación del examen nacional", 70, 10, "puntos"), ("el tiempo de traslado de los empleados", 45, 8, "min"), ("el peso de los recién nacidos", 3200, 450, "g")])
    lab, mu, sd, u = ctx
    if t == "regla":
        k = R.choice([1, 2, 3])
        pct = {1: "68", 2: "95", 3: "99.7"}[k]
        kind = R.choice(["dentro", "arriba", "abajo"])
        lo, hi = mu - k * sd, mu + k * sd
        if kind == "dentro":
            return opt("%s sigue una distribución normal con media %s %s y desviación estándar %s %s. ¿Qué porcentaje aproximado está entre %s y %s %s?" % ((lab[0].upper() + lab[1:]), num(mu), u, num(sd), u, num(lo), num(hi), u),
                       pct + NB + "%", [x + NB + "%" for x in ("68", "95", "99.7", "50") if x != pct][:3], "Entre μ − %dσ y μ + %dσ está cerca del <b>%s %%</b> (regla 68-95-99.7)." % (k, k, pct))
        out = {1: "16", 2: "2.5", 3: "0.15"}[k]
        v = hi if kind == "arriba" else lo
        return opt("%s sigue una normal con μ = %s %s y σ = %s %s. ¿Qué porcentaje aproximado %s de %s %s?" % ((lab[0].upper() + lab[1:]), num(mu), u, num(sd), u, "está por encima" if kind == "arriba" else "está por debajo", num(v), u),
                   out + NB + "%", [x + NB + "%" for x in ("16", "2.5", "0.15", "34", "5", "32") if x != out][:3],
                   "Fuera de μ ± %dσ queda %s %%, la mitad a cada lado: <b>%s %%</b>." % (k, {1: "32", 2: "5", 3: "0.3"}[k], out))
    if t == "z":
        k = R.choice([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5])
        x = mu + k * sd
        if x != int(x):
            return None
        return opt("%s: μ = %s %s, σ = %s %s. ¿Cuál es el valor z (estandarizado) de %s %s?" % ((lab[0].upper() + lab[1:]), num(mu), u, num(sd), u, num(int(x)), u),
                   d2(k, 1), [d2(-k, 1), d2(k * 2, 1), d2(k + 1, 1)],
                   "z = (x − μ) ÷ σ = (%s − %s) ÷ %s = <b>%s</b>." % (num(int(x)), num(mu), num(sd), d2(k, 1)))
    if t == "comp":
        a, b = name(), name()
        if a == b:
            return None
        ma, sa, mb, sb = 70, 10, 60, 5
        xa, xb = R.choice([(85, 70), (80, 72), (90, 68), (75, 69)])
        za, zb = F(xa - ma, sa), F(xb - mb, sb)
        if za == zb:
            return None
        ok = a if za > zb else b
        return opt("%s sacó %d en un examen con μ = %d y σ = %d. %s sacó %d en otro examen con μ = %d y σ = %d. ¿Quién tuvo un mejor resultado <b>en relación con su grupo</b>?" % (a, xa, ma, sa, b, xb, mb, sb),
                   ok, [b if ok == a else a, "los dos igual", "no se puede comparar"],
                   "z de %s = (%d − %d) ÷ %d = %s; z de %s = (%d − %d) ÷ %d = %s. Mayor z: <b>%s</b>." % (a, xa, ma, sa, show(za), b, xb, mb, sb, show(zb), ok))
    items = [
        ("La curva de una distribución normal es…", "simétrica y con forma de campana", ["siempre creciente", "una recta", "más alta en los extremos"], "La normal tiene forma de campana y es simétrica respecto a la media."),
        ("En una distribución normal, la media, la mediana y la moda…", "son iguales", ["son siempre distintas", "suman 1", "no existen"], "Por la simetría, las tres coinciden en el centro."),
        ("El área total bajo la curva normal es…", "1 (el 100 %)", ["0", "la media", "infinita"], "El área bajo la curva representa probabilidad; el total es 1."),
        ("Si σ aumenta y μ no cambia, la campana…", "se hace más ancha y más baja", ["se mueve a la derecha", "se hace más alta y estrecha", "no cambia"], "Más dispersión: la campana se extiende."),
        ("La normal estándar Z tiene…", "media 0 y desviación estándar 1", ["media 1 y desviación 0", "media 100", "media 0 y desviación 10"], "Estandarizar (z = (x − μ)/σ) convierte cualquier normal en N(0, 1)."),
        ("Un valor con z = −2 está…", "2 desviaciones estándar por debajo de la media", ["2 unidades por debajo de la media", "por encima de la media", "en la media"], "z cuenta cuántas σ te alejas de la media."),
    ]
    return from_bank(items)


# ============================================================ P15: inferencia y prueba de hipótesis
def p15(*ks):
    t = pick(ks, ["h0", "pval", "sim", "z", "error", "concepto"])
    if t == "h0":
        cases = [("Una empresa dice que sus focos duran en promedio 1 000 horas. Crees que duran menos.", "H₀: μ = 1 000; H₁: μ &lt; 1 000"),
                 ("Una moneda parece cargada hacia águila.", "H₀: p = 0.5; H₁: p &gt; 0.5"),
                 ("Se dice que el 30 % de los alumnos usa transporte público; crees que el porcentaje cambió.", "H₀: p = 0.3; H₁: p ≠ 0.3"),
                 ("Un fabricante afirma que sus botellas tienen 600 ml; un inspector sospecha que traen más.", "H₀: μ = 600; H₁: μ &gt; 600"),
                 ("Una escuela afirma que su promedio de examen es 75; un padre cree que es menor.", "H₀: μ = 75; H₁: μ &lt; 75")]
        s, a = R.choice(cases)
        w = [b for _, b in cases if b != a]
        alt = a.replace("H₀", "X").replace("H₁", "H₀").replace("X", "H₁")
        return opt(s + " ¿Cuáles son las hipótesis?", a, [alt] + R.sample(w, 2), "H₀ es lo que se afirma (con =); H₁ es lo que se sospecha: <b>%s</b>." % a)
    if t == "pval":
        alpha = R.choice([0.05, 0.01, 0.1])
        p = R.choice([0.001, 0.003, 0.02, 0.04, 0.07, 0.12, 0.3, 0.008])
        rej = p < alpha
        return opt("En una prueba con nivel de significancia α = %s se obtuvo un valor p = %s. ¿Qué se decide?" % (d2(alpha), d2(p, 3)),
                   "se rechaza H₀" if rej else "no se rechaza H₀", ["no se rechaza H₀" if rej else "se rechaza H₀", "se acepta que H₀ es falsa sin duda", "se rechaza H₁ y se demuestra H₀"],
                   "Si p &lt; α se rechaza H₀. Aquí %s %s %s: <b>%s</b>." % (d2(p, 3), "&lt;" if rej else "≥", d2(alpha), "se rechaza H₀" if rej else "no se rechaza H₀"))
    if t == "sim":
        n = R.choice([20, 30, 40])
        k = R.choice([n * 7 // 10, n * 3 // 4, n * 8 // 10])
        sims = R.choice([500, 1000, 2000])
        extreme = R.choice([3, 8, 15, 25, 40, 90, 150, 300])
        p = F(extreme, sims)
        rej = p < F(5, 100)
        return opt("Una moneda cayó águila %d de %d veces. Se simularon %s series de %d lanzamientos con una moneda justa, y en %d series salieron %d águilas o más. Con α = 0.05, ¿la moneda parece cargada?" % (k, n, num(sims), n, extreme, k),
                   ("sí, porque p ≈ %s es menor que 0.05" if rej else "no hay evidencia suficiente: p ≈ %s no es menor que 0.05") % d2(float(p), 3),
                   ["no, porque salieron más águilas", "sí, porque %d es más de la mitad" % k, ("no hay evidencia suficiente: p ≈ %s no es menor que 0.05" if rej else "sí, porque p ≈ %s es menor que 0.05") % d2(float(p), 3)],
                   "Valor p ≈ %d ÷ %s = %s. %s" % (extreme, num(sims), d2(float(p), 3), "Es muy raro con una moneda justa: <b>parece cargada</b>." if rej else "No es tan raro con una moneda justa: <b>no hay evidencia suficiente</b>."))
    if t == "z":
        mu0, sd, n = R.choice([(500, 20, 64), (1000, 60, 36), (75, 12, 36), (250, 15, 25), (80, 8, 16)])
        se = F(sd) / int(math.isqrt(n))
        zz = R.choice([F(-5, 2), F(-2), F(-3, 2), F(-1), F(1, 2), F(3, 2), F(2), F(5, 2), F(3)])
        xbar = mu0 + zz * se
        if xbar.denominator not in (1, 2, 4, 5, 10):
            return None
        rej = abs(zz) > F(196, 100)
        return opt("H₀: μ = %s, con σ = %d. Una muestra de %d datos dio x̄ = %s. Calcula z = (x̄ − μ) ÷ (σ/√n) y decide con α = 0.05 (bilateral, |z| &gt; 1.96)." % (num(mu0), sd, n, show(xbar)),
                   "z = %s; %s" % (show(zz).replace("-", MINUS), "se rechaza H₀" if rej else "no se rechaza H₀"),
                   ["z = %s; %s" % (show(zz).replace("-", MINUS), "no se rechaza H₀" if rej else "se rechaza H₀"), "z = %s; %s" % (show(zz * int(math.isqrt(n))).replace("-", MINUS), "se rechaza H₀"),
                    "z = %s; %s" % (show(zz / int(math.isqrt(n))).replace("-", MINUS), "no se rechaza H₀")],
                   "σ/√n = %d ÷ %d = %s. z = (%s − %s) ÷ %s = %s. |z| %s 1.96 → <b>%s</b>." % (sd, math.isqrt(n), show(se), show(xbar), num(mu0), show(se), show(zz), "&gt;" if rej else "≤", "se rechaza H₀" if rej else "no se rechaza H₀"))
    if t == "error":
        items = [
            ("Rechazar H₀ cuando en realidad es verdadera se llama…", "error tipo I", ["error tipo II", "valor p", "nivel de confianza"], "El error tipo I es un «falso positivo». Su probabilidad es α."),
            ("No rechazar H₀ cuando en realidad es falsa se llama…", "error tipo II", ["error tipo I", "sesgo de muestreo", "valor atípico"], "El error tipo II es un «falso negativo»."),
            ("El nivel de significancia α es…", "la probabilidad de rechazar H₀ siendo verdadera", ["la probabilidad de que H₀ sea verdadera", "el tamaño de la muestra", "la media de la muestra"], "α es el riesgo de error tipo I que aceptamos (por ejemplo 0.05)."),
            ("Si α baja de 0.05 a 0.01, rechazar H₀…", "se vuelve más difícil", ["se vuelve más fácil", "no cambia", "es obligatorio"], "Con α menor hace falta más evidencia (un valor p más pequeño)."),
        ]
        return from_bank(items)
    items = [
        ("Un valor p pequeño significa que…", "los datos serían muy raros si H₀ fuera verdadera", ["H₀ es verdadera", "la muestra es pequeña", "no hay variabilidad"], "El valor p mide qué tan raros son los datos suponiendo H₀."),
        ("«No rechazar H₀» significa que…", "no hay evidencia suficiente contra H₀", ["H₀ quedó demostrada", "H₁ es verdadera", "el estudio está mal hecho"], "No rechazar no prueba H₀; solo indica que faltó evidencia."),
        ("La estadística inferencial sirve para…", "sacar conclusiones de una población a partir de una muestra", ["describir solo la muestra", "hacer gráficas", "evitar la variabilidad"], "Inferir: usar la muestra para hablar de la población, con un margen de error."),
        ("Al aumentar el tamaño de la muestra, una diferencia real pequeña…", "es más fácil de detectar", ["es más difícil de detectar", "desaparece", "se vuelve un error tipo I"], "Con más datos, el error estándar σ/√n es menor."),
        ("Un intervalo de confianza del 95 % para la media es (48; 56). ¿Cuál es la estimación puntual?", "52", ["48", "56", "95"], "Es el centro del intervalo: (48 + 56) ÷ 2 = 52."),
    ]
    return from_bank(items)


# ============================================================ P9: correlación y recta de ajuste (interpretación)
REG = [  # x, y (con artículo), unidad de y, unidad de x, (a posibles), (b posibles)
    ("horas de estudio", "la calificación", "puntos", "hora", (40, 50, 55, 60), (2, 2.5, 3, 4, 5)),
    ("temperatura (°C)", "los vasos de agua vendidos", "vasos", "grado", (10, 20, 30), (3, 4, 5, 6, 8)),
    ("años de antigüedad", "el sueldo mensual (miles de $)", "miles de pesos", "año", (8, 9, 10, 12), (0.5, 0.8, 1.2, 1.5)),
    ("kilómetros recorridos en taxi", "el costo del viaje ($)", "pesos", "kilómetro", (30, 35, 40, 45), (6, 7, 8, 9)),
    ("horas de pantalla al día", "las horas de sueño", "horas", "hora", (9, 10), (-0.3, -0.4, -0.5)),
    ("edad del carro (años)", "el precio (miles de $)", "miles de pesos", "año", (250, 300, 350), (-15, -20, -25)),
]


def p9(*ks):
    t = pick(ks, ["pend", "pred", "r", "signo"])
    x, y, uy, ux, As, Bs = R.choice(REG)
    neg = Bs[0] < 0
    b = R.choice(Bs)
    a = R.choice(As)
    y0 = y.split(" (")[0]
    eq = "ŷ = %s %s %sx" % (num(a), "−" if b < 0 else "+", d2(abs(b), 1))
    if t == "pend":
        ab = d2(abs(b), 1)
        pl_ = y0.startswith(("los ", "las "))
        up, dn, es = ("suben", "bajan", "son") if pl_ else ("sube", "baja", "es")
        ok = "por cada %s más, %s %s en promedio %s %s" % (ux, y0, dn if b < 0 else up, ab, uy)
        w = ["por cada %s más, %s %s en promedio %s %s" % (ux, y0, up if b < 0 else dn, ab, uy),
             "por cada %s más, %s %s en promedio %s %s" % (ux, y0, dn if b < 0 else up, num(a), uy),
             "cuando x = 0, %s %s %s %s" % (y0, es, ab, uy)]
        return opt("La recta de ajuste entre x = %s e y = %s es %s. ¿Qué significa la pendiente?" % (x, y0, eq), ok, w, "La pendiente %s indica el cambio promedio de y por cada unidad de x: <b>%s</b>." % (d2(b, 1), ok))
    if t == "pred":
        xv = R.randint(1, 12)
        yv = a + b * xv
        if yv <= 0:
            return None
        return opt("La recta de ajuste entre x = %s e y = %s es %s. Estima y cuando x = %d." % (x, y0, eq, xv), d2(yv, 1), [d2(a + b, 1), d2(a - b * xv, 1), d2(abs(b) * xv, 1)],
                   "ŷ = %s %s %s × %d = <b>%s</b>." % (num(a), "−" if b < 0 else "+", d2(abs(b), 1), xv, d2(yv, 1)))
    if t == "signo":
        return opt("Se estudia la relación entre x = %s e y = %s. ¿Qué signo esperas en la pendiente de la recta de ajuste?" % (x, y0), "negativo" if neg else "positivo", ["positivo" if neg else "negativo", "cero", "no tiene pendiente"],
                   "Cuando x aumenta, %s tiende a %s: pendiente <b>%s</b>." % (y0, "bajar" if neg else "subir", "negativa" if neg else "positiva"))
    r = R.choice([-0.95, -0.7, -0.3, 0.05, 0.4, 0.75, 0.98])
    desc = {-0.95: "negativa muy fuerte", -0.7: "negativa moderada", -0.3: "negativa débil", 0.05: "prácticamente nula", 0.4: "positiva débil", 0.75: "positiva moderada", 0.98: "positiva muy fuerte"}
    return opt("El coeficiente de correlación entre dos variables es r = %s. ¿Cómo es la correlación?" % d2(r, 2), desc[r], R.sample([v for k, v in desc.items() if k != r], 3),
               "|r| cerca de 1 indica relación lineal fuerte; el signo indica si sube o baja. r = %s: <b>%s</b>." % (d2(r, 2), desc[r]))
