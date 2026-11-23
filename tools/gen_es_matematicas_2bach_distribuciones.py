# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Distribución binomial y distribución normal (Sentido estocástico)
build(k): k = "binomial" → «distribucion-binomial»: variables aleatorias discretas, función de probabilidad, media y varianza, B(n, p), P(X = k), P(X ≤ k), «al menos uno»;
k = "normal" → «distribucion-normal»: N(μ, σ), tipificación, uso de la tabla N(0, 1), probabilidades de intervalos, valores críticos, aproximación de la binomial por la normal.
Errores: olvidar el número combinatorio, P(X ≥ 1) = 1 − P(X = 0) y no 1 − P(X = 1), restar mal al tipificar, olvidar la corrección por continuidad.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, nf, fq, d, r2, tabla, kurve, BLUE, W

R = None


def P4(x):
    return r2(x, 4)


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def tz(z):
    """valor de la tabla (4 decimales) para z con 2 decimales"""
    return round(phi(round(z, 2)), 4)


def Wp(xs):
    """quita duplicados y probabilidades imposibles (menores que 0 o mayores que 1)"""
    out = []
    for x in W(xs):
        try:
            v = float(x.replace("−", "-").replace(",", "."))
        except ValueError:
            out.append(x)
            continue
        if 0 <= v <= 1:
            out.append(x)
    return out


def binom(n, k, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


# ------------------------------------------------ binomial

def s_va():
    t = R.choice(["media", "media", "falta", "varianza"])
    xs = sorted(R.sample(range(0, 6), 4))
    while True:
        ps = [R.randint(1, 5) for _ in range(4)]
        s = sum(ps)
        if 10 % s == 0 or s in (10, 20, 5, 4):
            break
    ps = [F(x, s) for x in ps]
    mu = sum(x * p for x, p in zip(xs, ps))
    if t == "falta":
        k = R.randint(0, 3)
        tab = tabla(["x"] + [str(x) for x in xs], [["P(X = x)"] + [("a" if i == k else (d(p) if (p * 100).denominator == 1 else fq(p))) for i, p in enumerate(ps)]])
        v = ps[k]
        return M(tab + "¿Cuánto vale a para que sea una distribución de probabilidad? (x = %s)" % ", ".join(map(str, xs)), d(v) if (v * 100).denominator == 1 else fq(v), W([d(1 - v) if ((1 - v) * 100).denominator == 1 else fq(1 - v), "1", "0", d(v + F(1, 10)) if ((v + F(1, 10)) * 100).denominator == 1 else fq(v + F(1, 10))]), "Las probabilidades suman 1: <b>a = %s</b>." % (d(v) if (v * 100).denominator == 1 else fq(v)))
    tab = tabla(["x"] + [str(x) for x in xs], [["P(X = x)"] + [d(p) if (p * 100).denominator == 1 else fq(p) for p in ps]])
    if t == "media":
        return M(tab + "Calcula la media (esperanza) de X. (x = %s)" % ", ".join(map(str, xs)), r2(float(mu)), W([r2(sum(xs) / 4), r2(float(mu) + 0.5), r2(float(sum(ps))), r2(float(mu) * 2)]), "μ = Σ x · P(X = x) = <b>%s</b>." % r2(float(mu)))
    var = sum(x * x * p for x, p in zip(xs, ps)) - mu * mu
    return M(tab + "Calcula la varianza de X. (x = %s)" % ", ".join(map(str, xs)), r2(float(var)), W([r2(float(sum(x * x * p for x, p in zip(xs, ps)))), r2(math.sqrt(float(var))), r2(float(var) + float(mu)), r2(float(mu))]), "σ² = Σ x² P − μ² = %s − %s² = <b>%s</b>." % (r2(float(sum(x * x * p for x, p in zip(xs, ps)))), r2(float(mu)), r2(float(var))))


def s_identificar():
    t = R.choice(["param", "param", "es", "media"])
    if t == "param":
        n, pp, txt = R.choice([(10, "1/6", "Se lanza un dado 10 veces y X es el número de seises"), (20, "0,3", "El 30 % de los alumnos usa gafas; se eligen 20 al azar y X es cuántos usan gafas"),
                               (8, "0,5", "Se lanza una moneda 8 veces y X es el número de caras"), (15, "0,05", "El 5 % de las piezas son defectuosas; se revisan 15 y X es el número de defectuosas"),
                               (12, "0,25", "En un test de 12 preguntas con 4 opciones se responde al azar; X es el número de aciertos"), (50, "0,02", "El 2 % de los envíos se retrasa; de 50 envíos, X es cuántos se retrasan")])
        return M("%s. ¿Qué distribución sigue X?" % txt, "B(%d; %s)" % (n, pp), W(["B(%s; %d)" % (pp, n), "N(%d; %s)" % (n, pp), "B(%d; %s)" % (n + 1, pp)]), "n = %d repeticiones independientes con probabilidad de éxito p = %s: <b>B(%d; %s)</b>." % (n, pp, n, pp))
    if t == "es":
        q, a, w = R.choice([("¿Cuál de estas variables es binomial?", "número de caras al lanzar 10 monedas", ["la altura de un alumno", "el tiempo de espera en una cola", "el peso de una manzana"]),
                            ("¿Qué condición NO es necesaria en una binomial?", "que p = 0,5", ["que los ensayos sean independientes", "que p sea la misma en cada ensayo", "que solo haya dos resultados"]),
                            ("Sacar 5 bolas de una urna SIN devolverlas, ¿sigue una binomial?", "no, porque la probabilidad cambia en cada extracción", ["sí, siempre", "sí, si hay más de 5 bolas", "solo si son todas del mismo color"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    n = R.choice([10, 20, 25, 40, 50, 100])
    p = R.choice([F(1, 2), F(1, 5), F(1, 4), F(1, 10), F(3, 10)])
    mu = n * p
    var = n * p * (1 - p)
    k = R.choice(["mu", "sigma"])
    if k == "mu":
        return M("Si X ~ B(%d; %s), ¿cuál es su media?" % (n, d(p)), nf(mu) if mu.denominator == 1 else d(mu), W([d(p), nf(var) if var.denominator == 1 else d(var), num(n), nf(mu + 1) if mu.denominator == 1 else d(mu + 1)]), "μ = n · p = %d · %s = <b>%s</b>." % (n, d(p), nf(mu) if mu.denominator == 1 else d(mu)))
    return M("Si X ~ B(%d; %s), ¿cuál es su desviación típica (a las centésimas)?" % (n, d(p)), r2(math.sqrt(var)), W([r2(float(var)), r2(float(mu)), r2(math.sqrt(float(mu))), r2(math.sqrt(var) + 1)]), "σ = √(npq) = √%s ≈ <b>%s</b>." % (r2(float(var)), r2(math.sqrt(var))))


def s_binomial():
    n = R.randint(4, 10)
    p = R.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7])
    t = R.choice(["igual", "igual", "cero", "almenos", "max"])
    ps = "%s" % r2(p, 2)
    if t == "igual":
        k = R.randint(1, n - 1)
        v = binom(n, k, p)
        return M("Si X ~ B(%d; %s), calcula P(X = %d) (a las diezmilésimas)." % (n, ps, k), P4(v), Wp([P4(p ** k * (1 - p) ** (n - k)), P4(math.comb(n, k) * p ** k), P4(binom(n, k - 1, p)), P4(binom(n, k + 1, p)) if k + 1 <= n else P4(v / 2)]),
                 "C<sub>%d,%d</sub> · %s<sup>%d</sup> · %s<sup>%d</sup> = %d · … ≈ <b>%s</b>." % (n, k, ps, k, r2(1 - p, 2), n - k, math.comb(n, k), P4(v)))
    if t == "cero":
        v = (1 - p) ** n
        return M("Si X ~ B(%d; %s), calcula P(X = 0) (a las diezmilésimas)." % (n, ps), P4(v), Wp([P4(p ** n), "0", P4(1 - v), P4(1 - p)]), "P(X = 0) = q<sup>n</sup> = %s<sup>%d</sup> ≈ <b>%s</b>." % (r2(1 - p, 2), n, P4(v)))
    if t == "almenos":
        v = 1 - (1 - p) ** n
        return M("Si X ~ B(%d; %s), calcula P(X ≥ 1) (a las diezmilésimas)." % (n, ps), P4(v), Wp([P4((1 - p) ** n), P4(1 - binom(n, 1, p)), P4(n * p) if n * p < 1 else P4(binom(n, 1, p)), P4(p)]), "P(X ≥ 1) = 1 − P(X = 0) = 1 − %s<sup>%d</sup> ≈ <b>%s</b>." % (r2(1 - p, 2), n, P4(v)))
    k = R.randint(1, 2)
    v = sum(binom(n, i, p) for i in range(k + 1))
    return M("Si X ~ B(%d; %s), calcula P(X ≤ %d) (a las diezmilésimas)." % (n, ps, k), P4(v), Wp([P4(binom(n, k, p)), P4(1 - v), P4(v - binom(n, 0, p)), P4(sum(binom(n, i, p) for i in range(k)))]), "P(X = 0) + … + P(X = %d) ≈ <b>%s</b>." % (k, P4(v)))


def s_bin_problema():
    t = R.choice(["dado", "test", "piezas", "familia"])
    if t == "dado":
        n, k = R.choice([(4, 1), (5, 2), (6, 2), (3, 1), (6, 1)])
        v = binom(n, k, 1 / 6)
        return M("Se lanza un dado %d veces. ¿Cuál es la probabilidad de sacar exactamente %d seis%s? (a las diezmilésimas)" % (n, k, "es" if k != 1 else ""), P4(v), Wp([P4((1 / 6) ** k), P4(k / 6), P4(binom(n, k + 1, 1 / 6)), P4(1 - v)]), "X ~ B(%d; 1/6): P(X = %d) ≈ <b>%s</b>." % (n, k, P4(v)))
    if t == "test":
        n = R.choice([5, 6, 8, 10])
        k = n // 2 + 1
        v = sum(binom(n, i, 0.25) for i in range(k, n + 1))
        return M("Un test tiene %d preguntas con 4 opciones. Respondiendo al azar, ¿qué probabilidad hay de acertar %d o más? (a las diezmilésimas)" % (n, k), P4(v), Wp([P4(binom(n, k, 0.25)), P4(1 - v), P4(0.25 ** k), P4(v * 2)]), "X ~ B(%d; 0,25): P(X ≥ %d) ≈ <b>%s</b>." % (n, k, P4(v)))
    if t == "piezas":
        n, p = R.choice([(10, 0.05), (20, 0.02), (8, 0.1), (15, 0.04)])
        v = 1 - (1 - p) ** n
        return M("El %s %% de las piezas son defectuosas. En una caja de %d, ¿qué probabilidad hay de que haya al menos una defectuosa? (a las diezmilésimas)" % (r2(p * 100, 0), n), P4(v), Wp([P4((1 - p) ** n), P4(n * p), P4(binom(n, 1, p)), P4(p)]), "1 − 0,%s<sup>%d</sup> ≈ <b>%s</b>." % (str(round((1 - p) * 100)), n, P4(v)))
    n = R.choice([3, 4, 5])
    k = R.randint(1, n - 1)
    v = F(math.comb(n, k), 2 ** n)
    return M("En una familia de %d hijos (chico o chica con probabilidad 1/2), ¿qué probabilidad hay de que haya exactamente %d chica%s?" % (n, k, "s" if k > 1 else ""), fq(v), Wp([fq(F(1, 2 ** n)), fq(F(k, n)), fq(F(math.comb(n, k), 2 ** (n + 1))), fq(F(1, 2))]), "C<sub>%d,%d</sub>/2<sup>%d</sup> = <b>%s</b>." % (n, k, n, fq(v)))


# ------------------------------------------------ normal

def zs():
    return round(R.uniform(0.1, 2.6), 2)


def s_tabla():
    t = R.choice(["le", "ge", "neg", "entre", "entre2"])
    z = zs()
    zs_ = r2(z, 2)
    if t == "le":
        return M("Si Z ~ N(0, 1), calcula P(Z ≤ %s)." % zs_, P4(tz(z)), Wp([P4(1 - tz(z)), P4(tz(z) - 0.5), P4(tz(z + 0.1)), P4(tz(z) / 2)]), "Se lee directamente en la tabla: <b>%s</b>." % P4(tz(z)))
    if t == "ge":
        return M("Si Z ~ N(0, 1), calcula P(Z ≥ %s)." % zs_, P4(1 - tz(z)), Wp([P4(tz(z)), P4(tz(z) - 0.5), P4(1 - tz(z + 0.1)), P4(0.5 - tz(z) / 2)]), "P(Z ≥ z) = 1 − P(Z ≤ z) = 1 − %s = <b>%s</b>." % (P4(tz(z)), P4(1 - tz(z))))
    if t == "neg":
        return M("Si Z ~ N(0, 1), calcula P(Z ≤ −%s)." % zs_, P4(1 - tz(z)), Wp([P4(tz(z)), P4(-tz(z) + 0.5) if tz(z) < 0.5 else P4(tz(z) - 0.5), P4(1 - tz(z) + 0.01), "0"]), "Por simetría, P(Z ≤ −z) = 1 − P(Z ≤ z) = <b>%s</b>." % P4(1 - tz(z)))
    if t == "entre":
        z2 = zs()
        a, b = sorted([z, z2])
        if a == b:
            return None
        v = tz(b) - tz(a)
        return M("Si Z ~ N(0, 1), calcula P(%s ≤ Z ≤ %s)." % (r2(a, 2), r2(b, 2)), P4(v), Wp([P4(tz(b) + tz(a) - 1), P4(tz(b)), P4(1 - v), P4(tz(b) - (1 - tz(a)))]), "P(Z ≤ %s) − P(Z ≤ %s) = %s − %s = <b>%s</b>." % (r2(b, 2), r2(a, 2), P4(tz(b)), P4(tz(a)), P4(v)))
    v = 2 * tz(z) - 1
    return M("Si Z ~ N(0, 1), calcula P(−%s ≤ Z ≤ %s)." % (zs_, zs_), P4(v), Wp([P4(tz(z)), P4(tz(z) - 0.5), P4(1 - v), P4(2 * tz(z))]) if 2 * tz(z) <= 1 else Wp([P4(tz(z)), P4(tz(z) - 0.5), P4(1 - v), P4(v / 2)]), "2 · P(Z ≤ %s) − 1 = <b>%s</b>." % (zs_, P4(v)))


def s_tipificar():
    mu = R.choice([50, 60, 70, 100, 170, 500, 20, 12])
    sig = R.choice([5, 10, 4, 8, 2, 20, 15])
    t = R.choice(["z", "le", "ge", "entre"])
    k = R.choice([0.5, 1, 1.25, 1.5, 2, 0.8, 1.2, 0.3, 0.75])
    s = R.choice([1, -1])
    x = mu + s * k * sig
    if x != int(x):
        return None
    x = int(x)
    z = (x - mu) / sig
    if t == "z":
        return M("Si X ~ N(%d, %d), ¿qué valor tipificado corresponde a x = %d?" % (mu, sig, x), r2(z, 2), W([r2((x - mu) / sig ** 2, 2), r2((mu - x) / sig, 2), r2(x / sig, 2), r2(z + 1, 2)]), "z = (x − μ)/σ = (%d − %d)/%d = <b>%s</b>." % (x, mu, sig, r2(z, 2)))
    if t == "le":
        v = tz(z) if z >= 0 else 1 - tz(-z)
        return M("Si X ~ N(%d, %d), calcula P(X ≤ %d)." % (mu, sig, x), P4(v), Wp([P4(1 - v), P4(tz(abs(z))) if z < 0 else P4(tz(z) - 0.5), P4(tz(abs(z) / 2)), P4(v + 0.01)]), "Tipificamos: z = %s → P(Z ≤ %s) = <b>%s</b>." % (r2(z, 2), r2(z, 2), P4(v)))
    if t == "ge":
        v = 1 - (tz(z) if z >= 0 else 1 - tz(-z))
        return M("Si X ~ N(%d, %d), calcula P(X ≥ %d)." % (mu, sig, x), P4(v), Wp([P4(1 - v), P4(abs(0.5 - v)), P4(v / 2), P4(v + 0.01)]), "z = %s → P(Z ≥ %s) = <b>%s</b>." % (r2(z, 2), r2(z, 2), P4(v)))
    k2 = R.choice([0.5, 1, 1.5, 2])
    a, b = mu - k2 * sig, mu + k * sig
    if a != int(a) or b != int(b):
        return None
    v = tz(k) - (1 - tz(k2))
    return M("Si X ~ N(%d, %d), calcula P(%d ≤ X ≤ %d)." % (mu, sig, int(a), int(b)), P4(v), Wp([P4(tz(k) - tz(k2)) if tz(k) != tz(k2) else P4(v / 2), P4(tz(k)), P4(1 - v), P4(tz(k) + tz(k2) - 0.5)]), "z₁ = −%s, z₂ = %s → %s − (1 − %s) = <b>%s</b>." % (r2(k2, 2), r2(k, 2), P4(tz(k)), P4(tz(k2)), P4(v)))


def s_inversa():
    t = R.choice(["k", "k", "percentil", "teo"])
    pv, zv = R.choice([(0.9, 1.28), (0.95, 1.645), (0.975, 1.96), (0.99, 2.33), (0.8, 0.84), (0.75, 0.67), (0.85, 1.04)])
    if t == "k":
        return M("Si Z ~ N(0, 1), ¿qué valor k cumple P(Z ≤ k) = %s?" % r2(pv, 3), r2(zv, 3), W([r2(-zv, 3), r2(pv, 3), r2(zv / 2, 3), r2(zv + 0.5, 3)]), "Buscamos %s dentro de la tabla: <b>k ≈ %s</b>." % (r2(pv, 3), r2(zv, 3)))
    if t == "percentil":
        mu, sig = R.choice([(100, 15), (170, 8), (500, 100), (60, 10), (20, 4)])
        x = mu + zv * sig
        return M("Las notas siguen N(%d, %d). ¿Qué nota deja por debajo al %s %% de los alumnos? (a las décimas)" % (mu, sig, r2(pv * 100, 1)), r2(x, 1), W([r2(mu - zv * sig, 1), r2(mu + pv * sig, 1), r2(mu + zv, 1), r2(x + sig, 1)]), "z = %s → x = μ + zσ = %d + %s · %d ≈ <b>%s</b>." % (r2(zv, 3), mu, r2(zv, 3), sig, r2(x, 1)))
    q, a, w = R.choice([("¿Qué porcentaje de datos queda entre μ − σ y μ + σ en una normal?", "aproximadamente el 68 %", ["el 50 %", "el 95 %", "el 99,7 %"]), ("¿Qué porcentaje queda entre μ − 2σ y μ + 2σ?", "aproximadamente el 95 %", ["el 68 %", "el 50 %", "el 100 %"]),
                        ("¿Cuánto vale P(Z ≤ 0) en una N(0, 1)?", "0,5", ["0", "1", "0,3413"]), ("En una variable normal, P(X = a) vale…", "0 (la variable es continua)", ["1", "0,5", "depende de a"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_aprox():
    n = R.choice([100, 200, 400, 50, 150])
    p = R.choice([0.5, 0.4, 0.3, 0.2, 0.1])
    mu = n * p
    sig = math.sqrt(n * p * (1 - p))
    t = R.choice(["param", "param", "prob", "cond"])
    if t == "param":
        return M("Para aproximar B(%d; %s) por una normal, ¿qué N(μ, σ) se usa? (σ a las centésimas)" % (n, r2(p, 2)), "N(%s; %s)" % (r2(mu, 1), r2(sig)), W(["N(%s; %s)" % (r2(mu, 1), r2(sig * sig)), "N(%s; %s)" % (r2(p, 2), r2(sig)), "N(%s; %s)" % (r2(mu, 1), r2(math.sqrt(mu)))]), "μ = np = %s y σ = √(npq) ≈ %s: <b>N(%s; %s)</b>." % (r2(mu, 1), r2(sig), r2(mu, 1), r2(sig)))
    if t == "prob":
        k = int(mu + R.choice([0.5, 1, 1.5]) * sig)
        z = (k + 0.5 - mu) / sig
        v = tz(z)
        return M("X ~ B(%d; %s). Con la aproximación normal y la corrección por continuidad, calcula P(X ≤ %d)." % (n, r2(p, 2), k), P4(v), W([P4(tz((k - mu) / sig)), P4(1 - v), P4(tz((k - 0.5 - mu) / sig)), P4(v - 0.05)]), "P(X′ ≤ %s) con X′ ~ N(%s; %s): z = %s → <b>%s</b>." % (r2(k + 0.5, 1), r2(mu, 1), r2(sig), r2(z, 2), P4(v)))
    q, a, w = R.choice([("¿Cuándo se puede aproximar una binomial por una normal?", "cuando n·p ≥ 5 y n·q ≥ 5", ["siempre", "solo si p = 0,5", "cuando n &lt; 10"]),
                        ("¿Por qué se usa la corrección por continuidad?", "porque se pasa de una variable discreta a una continua", ["para redondear la media", "porque σ es pequeña", "porque la binomial es simétrica"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def build(kind):
    global R
    R = random.Random(52013 if kind == "binomial" else 52014)
    seen = set()
    if kind == "binomial":
        sets = [("Variables aleatorias discretas", mix(R, seen, [(s_va, 20)])), ("Reconocer una binomial", mix(R, seen, [(s_identificar, 20)])), ("Calcular probabilidades", mix(R, seen, [(s_binomial, 20)])),
                ("Media y «al menos uno»", mix(R, seen, [(s_binomial, 10), (s_identificar, 10)])), ("Problemas", mix(R, seen, [(s_bin_problema, 20)]))]
        think = ["Una <b>variable aleatoria discreta</b> toma valores sueltos con probabilidades que suman 1. Media: μ = Σ x · P(X = x).",
                 "<b>Binomial</b> B(n, p): se repite n veces un experimento con dos resultados (éxito con probabilidad p), de forma independiente. X cuenta los éxitos.",
                 "P(X = k) = C<sub>n,k</sub> · p<sup>k</sup> · q<sup>n−k</sup>, con q = 1 − p. Media μ = np; desviación σ = √(npq).",
                 "«Al menos uno»: P(X ≥ 1) = 1 − P(X = 0) = 1 − q<sup>n</sup>."]
        ex = [("X ~ B(5; 0,2), P(X = 2)", ["C<sub>5,2</sub> · 0,2² · 0,8³ = 10 · 0,04 · 0,512"], "0,2048")]
        mist = [["Olvidar C<sub>n,k</sub>", "Hay varias formas de colocar los éxitos."], ["P(X ≥ 1) = 1 − P(X = 1)", "Es 1 − P(X = 0)."], ["Usar la binomial sin reemplazamiento", "La probabilidad debe ser la misma en cada prueba."]]
        body = L(think, ex, mist)
        faq = [("¿Cómo sé si un problema es binomial?", "Si hay n pruebas independientes, cada una con dos resultados y la misma probabilidad de éxito, y se cuentan los éxitos."),
               ("¿Qué significa la media de una binomial?", "El número de éxitos que se espera por término medio: en 100 lanzamientos de moneda, 50 caras.")]
        unit(2, R, "distribucion-binomial", "S", "Variables aleatorias discretas; distribución binomial: función de probabilidad, media, desviación típica y cálculo de probabilidades",
             "Distribución binomial", "Distribución binomial", "Fichas de Matemáticas II (2.º de Bachillerato): variables aleatorias, distribución binomial, P(X = k), media, desviación típica y problemas. 100 ejercicios con soluciones.",
             "P(X = k) = C(n, k) · pᵏ · qⁿ⁻ᵏ", "Media np; al menos uno: 1 − qⁿ.", body, faq, sets, 13)
    else:
        sets = [("Tabla de la N(0, 1)", mix(R, seen, [(s_tabla, 20)])), ("Tipificar", mix(R, seen, [(s_tipificar, 20)])), ("Valores a partir de probabilidades", mix(R, seen, [(s_inversa, 20)])),
                ("Probabilidades de intervalos", mix(R, seen, [(s_tabla, 8), (s_tipificar, 12)])), ("Aproximación de la binomial", mix(R, seen, [(s_aprox, 20)]))]
        think = ["La <b>distribución normal</b> N(μ, σ) tiene forma de campana, simétrica respecto a la media μ. El área total bajo la curva es 1.",
                 "<b>Tipificar</b>: z = (x − μ)/σ convierte X ~ N(μ, σ) en Z ~ N(0, 1), cuyas probabilidades P(Z ≤ z) da la tabla.",
                 "P(Z ≥ z) = 1 − P(Z ≤ z); P(Z ≤ −z) = 1 − P(Z ≤ z); P(a ≤ Z ≤ b) = P(Z ≤ b) − P(Z ≤ a).",
                 "Si np ≥ 5 y nq ≥ 5, B(n, p) ≈ N(np, √(npq)), con corrección por continuidad (± 0,5)."]
        ex = [("X ~ N(60, 10), P(X ≤ 75)", ["z = (75 − 60)/10 = 1,5"], "P(Z ≤ 1,5) = 0,9332")]
        mist = [["Restar al revés al tipificar", "z = (x − μ)/σ."], ["Buscar valores negativos en la tabla", "Usa la simetría: P(Z ≤ −z) = 1 − P(Z ≤ z)."], ["Olvidar la corrección por continuidad", "P(X ≤ 30) en la binomial → P(X′ ≤ 30,5) en la normal."]]
        body = L(think, ex, mist, kurve([(lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi) * 5, BLUE, "")], (-3.5, 3.5, 1), (0, 2.5, 1), W=330, H=200, label="campana de Gauss N(0, 1)"))
        faq = [("¿Dónde aparece la distribución normal?", "En estaturas, pesos, notas de exámenes, errores de medida… muchas magnitudes que dependen de muchos factores pequeños."),
               ("¿Para qué sirve tipificar?", "Para usar una sola tabla, la de N(0, 1), con cualquier distribución normal.")]
        unit(2, R, "distribucion-normal", "S", "Distribución normal: tipificación, cálculo de probabilidades con la tabla N(0, 1), valores críticos y aproximación de la binomial por la normal",
             "Distribución normal", "Distribución normal", "Fichas de Matemáticas II (2.º de Bachillerato): tabla N(0, 1), tipificación, probabilidades de intervalos, percentiles y aproximación de la binomial. 100 ejercicios.",
             "Tipifica: z = (x − μ) / σ", "Usa la simetría para los valores negativos.", body, faq, sets, 14)


if __name__ == "__main__":
    build("binomial")
