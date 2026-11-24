# -*- coding: utf-8 -*-
"""
México, bachillerato: Pensamiento Matemático II (pensamiento aritmético, algebraico y geométrico, MCCEMS). Problemas propios.
setup(R) antes de usar.
"""
import math
from fractions import Fraction as F
import mx_pm1 as P1
from mx_pm1 import opt, from_bank, d2, show, lst, pick, name  # noqa: F401
from mx_s1 import fq, dexact, tabla_html, MINUS, sg  # noqa: F401
from mx_common import num, dec, peso, NB  # noqa: F401
from ws_common import svg_wrap, text, line, fig

R = None


def setup(rnd):
    global R
    P1.setup(rnd)
    R = P1.R


def money(x):
    """pesos con centavos solo si hacen falta: $12 500, $1 234.50"""
    c = int(round(x * 100))
    return "$" + (num(c // 100) if c % 100 == 0 else num(c // 100) + ".%02d" % (c % 100))


# ============================================================ P1: lenguaje natural y lenguaje matemático (lógica)
PROPS = [("Todos los números primos son impares.", False, "2 es primo y es par."), ("El cuadrado de cualquier número real es mayor o igual que 0.", True, "x² ≥ 0 para todo x."),
         ("Existe un número entero entre 3 y 4.", False, "Entre 3 y 4 no hay enteros."), ("Todo múltiplo de 4 es par.", True, "4k = 2(2k)."),
         ("Algún número par es primo.", True, "El 2."), ("Todo número que termina en 5 es múltiplo de 5.", True, "Criterio de divisibilidad del 5."),
         ("La suma de dos números impares es impar.", False, "3 + 5 = 8 es par."), ("Existe un número real cuyo cuadrado es −4.", False, "Ningún real al cuadrado da negativo."),
         ("Todo triángulo equilátero es isósceles.", True, "Tiene (al menos) dos lados iguales."), ("Todo rectángulo es un cuadrado.", False, "Un rectángulo de 2 × 5 no es cuadrado."),
         ("El producto de dos números negativos es positivo.", True, "(−a)(−b) = ab."), ("Todo número divisible entre 6 es divisible entre 3.", True, "6 = 2 × 3."),
         ("Todo número divisible entre 3 es divisible entre 6.", False, "9 es divisible entre 3, pero no entre 6."), ("√2 es un número racional.", False, "√2 es irracional.")]
NEG = [("Todos los alumnos aprobaron.", "Al menos un alumno no aprobó.", ["Ningún alumno aprobó.", "Todos los alumnos reprobaron.", "Algunos alumnos aprobaron."]),
       ("Algún perro es blanco.", "Ningún perro es blanco.", ["Algún perro no es blanco.", "Todos los perros son blancos.", "Ningún perro es negro."]),
       ("Hoy llueve y hace frío.", "Hoy no llueve o no hace frío.", ["Hoy no llueve y no hace frío.", "Hoy llueve o hace frío.", "Hoy no llueve y hace frío."]),
       ("Estudio o trabajo.", "No estudio y no trabajo.", ["No estudio o no trabajo.", "Estudio y trabajo.", "No estudio, pero trabajo."]),
       ("Todos los números pares son múltiplos de 4.", "Algún número par no es múltiplo de 4.", ["Ningún número par es múltiplo de 4.", "Todos los números impares son múltiplos de 4.", "Algún número par es múltiplo de 4."]),
       ("Existe un número primo par.", "Ningún número primo es par.", ["Existe un número primo impar.", "Todos los números primos son pares.", "Existe un número par que no es primo."]),
       ("x es mayor que 5.", "x es menor o igual que 5.", ["x es menor que 5.", "x es mayor o igual que 5.", "x es igual a −5."]),
       ("Todos los cuadrados son rectángulos.", "Algún cuadrado no es rectángulo.", ["Ningún cuadrado es rectángulo.", "Todos los rectángulos son cuadrados.", "Algún rectángulo no es cuadrado."]),
       ("El número es par y positivo.", "El número es impar o no es positivo.", ["El número es impar y negativo.", "El número es par o positivo.", "El número no es par y no es positivo."]),
       ("Si llueve, entonces llevo paraguas.", "Llueve y no llevo paraguas.", ["Si no llueve, no llevo paraguas.", "No llueve y llevo paraguas.", "Si llevo paraguas, entonces llueve."]),
       ("Ningún alumno llegó tarde.", "Al menos un alumno llegó tarde.", ["Todos los alumnos llegaron tarde.", "Ningún alumno llegó temprano.", "Algún alumno no llegó tarde."]),
       ("Para todo x real, x² ≥ 0.", "Existe un x real tal que x² &lt; 0.", ["Para todo x real, x² &lt; 0.", "Existe un x real tal que x² ≥ 0.", "Para ningún x real, x² ≥ 0."])]
TRAD = [("el doble de un número aumentado en 5", "2x + 5", ["2(x + 5)", "x² + 5", "2 + x + 5"]), ("el doble de la suma de un número y 5", "2(x + 5)", ["2x + 5", "x + 10", "2x + 10x"]),
        ("el cuadrado de un número menos 3", "x² − 3", ["(x − 3)²", "2x − 3", "3 − x²"]), ("el cuadrado de la diferencia de un número y 3", "(x − 3)²", ["x² − 3", "x² − 9", "2(x − 3)"]),
        ("la mitad de un número más 7", "x/2 + 7", ["(x + 7)/2", "2x + 7", "x + 7/2"]), ("la mitad de la suma de un número y 7", "(x + 7)/2", ["x/2 + 7", "2(x + 7)", "x + 3.5x"]),
        ("tres números consecutivos suman 48", "x + (x + 1) + (x + 2) = 48", ["3x = 48 + 3", "x + 2x + 3x = 48", "x + 1 + 2 = 48"]),
        ("el triple de un número es 12 más que el número", "3x = x + 12", ["3x + 12 = x", "3(x + 12) = x", "x + 3 = 12"]),
        ("la suma de un número y su recíproco", "x + 1/x", ["2x", "x + x²", "1/(2x)"]), ("el producto de dos números consecutivos", "x(x + 1)", ["x + (x + 1)", "2x + 1", "x²"]),
        ("un número disminuido en su cuarta parte", "x − x/4", ["x/4 − x", "x − 4", "4x − x"]), ("el cubo de un número más el doble del número", "x³ + 2x", ["(x + 2x)³", "3x + 2x", "x³ + x²"])]
CONN = [("p ∧ q", "p y q"), ("p ∨ q", "p o q"), ("¬p", "no p"), ("p → q", "si p, entonces q"), ("p ↔ q", "p si y solo si q")]


def lp1(*ks):
    t = pick(ks, ["valor", "neg", "trad", "conn", "verdad", "contra"])
    if t == "valor":
        s, v, why = R.choice(PROPS)
        a = "verdadera" if v else "falsa"
        return opt("Proposición: «%s» ¿Es verdadera o falsa?" % s, a, ["falsa" if v else "verdadera", "no es una proposición", "depende de quién la diga"], "Es <b>%s</b>: %s" % (a, why))
    if t == "neg":
        s, a, w = R.choice(NEG)
        return opt("¿Cuál es la negación de «%s»?" % s, a, w, "La negación de «todos» es «al menos uno no»; la de «y» es «o» con cada parte negada (leyes de De Morgan): <b>%s</b>" % a)
    if t == "trad":
        s, a, w = R.choice(TRAD)
        return opt("¿Qué expresión corresponde a «%s»?" % s, a, w, "«%s» se escribe <b>%s</b>. Fíjate en el orden: ¿qué se hace primero?" % (s, a))
    if t == "conn":
        sym, word = R.choice(CONN)
        w = [b for a, b in CONN if a != sym]
        return opt("¿Cómo se lee el conectivo lógico <b>%s</b>?" % sym, word, R.sample(w, 3), "<b>%s</b> se lee «%s»." % (sym, word))
    if t == "verdad":
        vp, vq = R.choice([True, False]), R.choice([True, False])
        sym = R.choice(["p ∧ q", "p ∨ q", "p → q", "p ↔ q", "¬p ∨ q", "¬(p ∧ q)"])
        val = {"p ∧ q": vp and vq, "p ∨ q": vp or vq, "p → q": (not vp) or vq, "p ↔ q": vp == vq, "¬p ∨ q": (not vp) or vq, "¬(p ∧ q)": not (vp and vq)}[sym]
        V = lambda b: "V" if b else "F"
        return opt("Si p es %s y q es %s, ¿qué valor de verdad tiene %s?" % ("verdadera" if vp else "falsa", "verdadera" if vq else "falsa", sym), "verdadera" if val else "falsa",
                   ["falsa" if val else "verdadera", "no se puede saber", "las dos a la vez"],
                   "Con p = %s y q = %s: %s es <b>%s</b>." % (V(vp), V(vq), sym, "verdadera" if val else "falsa"))
    s, v, why = R.choice([p for p in PROPS if not p[1] and p[2][0].isdigit()] or PROPS)
    return opt("Para mostrar que «%s» es falsa basta con…" % s, "dar un contraejemplo", ["dar un ejemplo que la cumpla", "repetir la frase", "dar muchos ejemplos que la cumplan"],
               "Un solo contraejemplo muestra que una afirmación general es falsa: %s" % why)


# ============================================================ P6: números reales y propiedades de campo
PROPS_F = [("a + b = b + a", "conmutativa de la suma"), ("a × b = b × a", "conmutativa del producto"), ("(a + b) + c = a + (b + c)", "asociativa de la suma"),
           ("(a × b) × c = a × (b × c)", "asociativa del producto"), ("a × (b + c) = a × b + a × c", "distributiva"), ("a + 0 = a", "neutro aditivo"),
           ("a × 1 = a", "neutro multiplicativo"), ("a + (−a) = 0", "inverso aditivo"), ("a × (1/a) = 1, si a ≠ 0", "inverso multiplicativo")]


def lp6(*ks):
    t = pick(ks, ["prop", "ejemplo", "inverso", "orden", "densidad"])
    if t == "prop":
        f, a = R.choice(PROPS_F)
        return opt("¿Qué propiedad de los números reales expresa <b>%s</b>?" % f, a, R.sample([b for _, b in PROPS_F if b != a], 3), "Es la propiedad <b>%s</b>." % a)
    if t == "ejemplo":
        x, y, z = R.sample(range(2, 15), 3)
        ex = R.choice([("%d + %d = %d + %d" % (x, y, y, x), "conmutativa de la suma"), ("%d × (%d + %d) = %d × %d + %d × %d" % (x, y, z, x, y, x, z), "distributiva"),
                       ("(%d + %d) + %d = %d + (%d + %d)" % (x, y, z, x, y, z), "asociativa de la suma"), ("%d × %d = %d × %d" % (x, y, y, x), "conmutativa del producto"),
                       ("%d + (−%d) = 0" % (x, x), "inverso aditivo"), ("%d × 1 = %d" % (x, x), "neutro multiplicativo"), ("(%d × %d) × %d = %d × (%d × %d)" % (x, y, z, x, y, z), "asociativa del producto")])
        return opt("¿Qué propiedad se usa en <b>%s</b>?" % ex[0], ex[1], R.sample([b for _, b in PROPS_F if b != ex[1]], 3), "Es la propiedad <b>%s</b>." % ex[1])
    if t == "inverso":
        n, d = R.randint(1, 9), R.randint(2, 9)
        if math.gcd(n, d) != 1:
            return None
        neg = R.random() < .5
        v = F(-n if neg else n, d)
        kind = R.choice(["aditivo", "multiplicativo"])
        a = fq(-v) if kind == "aditivo" else fq(1 / v)
        w = [fq(1 / v), fq(-1 / v), fq(v)] if kind == "aditivo" else [fq(-v), fq(-1 / v), fq(v)]
        return opt("¿Cuál es el inverso %s de %s?" % (kind, fq(v)), a, w,
                   ("El inverso aditivo cumple a + (−a) = 0: <b>%s</b>." if kind == "aditivo" else "El inverso multiplicativo cumple a × (1/a) = 1: <b>%s</b>.") % a)
    if t == "orden":
        a, b, c = R.sample(range(-9, 10), 3)
        if c == 0:
            return None
        rule = R.choice(["suma", "neg", "pos"])
        if rule == "suma":
            return opt("Si a &lt; b, ¿qué es siempre cierto?", "a + c &lt; b + c para cualquier c", ["a + c &gt; b + c", "a × c &lt; b × c para cualquier c", "a − c &gt; b − c"],
                       "Sumar el mismo número a los dos lados no cambia la desigualdad.") if R.random() < .5 else \
                opt("Si %s &lt; %s, ¿qué desigualdad se obtiene al sumar %s a los dos lados?" % (sg(min(a, b)), sg(max(a, b)), sg(c)), "%s &lt; %s" % (sg(min(a, b) + c), sg(max(a, b) + c)),
                    ["%s &gt; %s" % (sg(min(a, b) + c), sg(max(a, b) + c)), "%s &lt; %s" % (sg(min(a, b) - c), sg(max(a, b) + c)), "%s = %s" % (sg(min(a, b) + c), sg(max(a, b) + c))],
                    "Sumar lo mismo conserva el orden: <b>%s &lt; %s</b>." % (sg(min(a, b) + c), sg(max(a, b) + c)))
        k = R.randint(2, 6) * (-1 if rule == "neg" else 1)
        lo, hi = sorted(R.sample(range(-9, 10), 2))
        ok = "%s %s %s" % (sg(lo * k), "&gt;" if k < 0 else "&lt;", sg(hi * k))
        return opt("Si %s &lt; %s y multiplicas los dos lados por %s, ¿qué desigualdad obtienes?" % (sg(lo), sg(hi), sg(k)), ok,
                   ["%s %s %s" % (sg(lo * k), "&lt;" if k < 0 else "&gt;", sg(hi * k)), "%s = %s" % (sg(lo * k), sg(hi * k)), "%s %s %s" % (sg(lo + k), "&lt;", sg(hi + k))],
                   ("Al multiplicar por un negativo la desigualdad <b>se invierte</b>: %s." if k < 0 else "Multiplicar por un positivo conserva el orden: %s.") % ok)
    a, b = sorted(R.sample(range(1, 30), 2))
    d = R.choice([10, 100])
    m = F(a + b, 2 * d)
    return opt("¿Qué número está entre %s y %s?" % (dec(a / d, 1 if d == 10 else 2), dec(b / d, 1 if d == 10 else 2)), dexact(m) or d2(float(m), 3),
               [dexact(F(b + 1, d)) or "1", dexact(F(a - 1, d)) if a > 1 else dexact(F(b + 2, d)), dexact(F(a + b, d)) or "2"],
               "La media de los dos siempre está entre ellos: (%s + %s) ÷ 2 = <b>%s</b>. Entre dos reales siempre hay otro (densidad)." % (dec(a / d, 1 if d == 10 else 2), dec(b / d, 1 if d == 10 else 2), dexact(m) or d2(float(m), 3)))


# ============================================================ P8: matemática financiera (pesos)
def lp8(*ks):
    t = pick(ks, ["simple", "monto", "tasa", "tiempo", "comp", "comp_m", "ahorro", "tarjeta", "comparar"])
    C = R.choice([5000, 8000, 10000, 12000, 15000, 20000, 25000, 30000, 40000, 50000])
    r = R.choice([4, 5, 6, 8, 9, 10, 12, 15])
    n = R.choice([2, 3, 4, 5])
    if t == "simple":
        I = C * r * n // 100
        return opt("Se invierten %s al %d %% de interés simple anual durante %d años. ¿Cuánto interés se gana?" % (money(C), r, n), money(I),
                   [money(C * r // 100), money(C + I), money(C * ((1 + r / 100) ** n - 1))], "I = C × r × t = %s × %s × %d = <b>%s</b>." % (money(C), d2(r / 100, 2), n, money(I)))
    if t == "monto":
        M = C + C * r * n // 100
        return opt("Un préstamo de %s a interés simple del %d %% anual se paga en %d años. ¿Cuál es el monto total a pagar?" % (money(C), r, n), money(M),
                   [money(C * r * n // 100), money(C * (1 + r / 100) ** n), money(C + C * r // 100)], "M = C(1 + rt) = %s × (1 + %s × %d) = <b>%s</b>." % (money(C), d2(r / 100, 2), n, money(M)))
    if t == "tasa":
        I = C * r * n // 100
        return opt("Con %s a interés simple se ganaron %s en %d años. ¿Cuál fue la tasa de interés anual?" % (money(C), money(I), n), "%d %%" % r,
                   ["%d %%" % (r * n), "%s %%" % d2(r / n, 1), "%d %%" % (r + 1)], "r = I ÷ (C × t) = %s ÷ (%s × %d) = %s = <b>%d %%</b>." % (money(I), money(C), n, d2(r / 100, 2), r))
    if t == "tiempo":
        I = C * r * n // 100
        return opt("¿Cuántos años tarda un capital de %s en generar %s de interés simple al %d %% anual?" % (money(C), money(I), r), "%d años" % n,
                   ["%d años" % (n + 1), "%d años" % (n * 2), "%d año" % 1 if n != 1 else "3 años"], "t = I ÷ (C × r) = %s ÷ (%s × %s) = <b>%d años</b>." % (money(I), money(C), d2(r / 100, 2), n))
    if t == "comp":
        M = C * (1 + r / 100) ** n
        return opt("Se depositan %s al %d %% de interés compuesto anual. ¿Cuánto habrá al cabo de %d años? (redondea a pesos)" % (money(C), r, n), money(round(M)),
                   [money(C + C * r * n // 100), money(round(C * (1 + r * n / 100) ** 1.1)), money(round(C * (1 + r / 100) ** (n - 1)))],
                   "M = C(1 + i)<sup>n</sup> = %s × %s<sup>%d</sup> ≈ <b>%s</b>." % (money(C), d2(1 + r / 100, 2), n, money(round(M))))
    if t == "comp_m":
        rr = R.choice([6, 12, 18, 24])
        k = R.choice([1, 2])
        M = C * (1 + rr / 1200) ** (12 * k)
        return opt("Un banco paga %d %% anual capitalizable mensualmente. Si depositas %s, ¿cuánto tendrás en %d %s? (redondea a pesos)" % (rr, money(C), k, "año" if k == 1 else "años"), money(round(M)),
                   [money(round(C * (1 + rr / 100) ** k)), money(round(C * (1 + rr * k / 100))), money(round(C * (1 + rr / 1200) ** k))],
                   "Tasa mensual = %d %% ÷ 12 = %s %%. M = %s × (1 + %s)<sup>%d</sup> ≈ <b>%s</b>." % (rr, d2(rr / 12, 1), money(C), d2(rr / 1200, 3), 12 * k, money(round(M))))
    if t == "ahorro":
        d = R.choice([300, 500, 800, 1000, 1200, 1500, 2000])
        m = R.choice([6, 10, 12, 18, 24])
        meta = R.choice([d * m, d * m + d * R.randint(1, 4)])
        if meta == d * m:
            return opt("%s ahorra %s cada mes sin intereses. ¿Cuánto tendrá en %d meses?" % (name(), money(d), m), money(d * m), [money(d * (m - 1)), money(d * 12), money(d + m)],
                       "%s × %d = <b>%s</b>." % (money(d), m, money(d * m)))
        mm = math.ceil(meta / d)
        return opt("%s quiere juntar %s para su proyecto y ahorra %s al mes. ¿Cuántos meses necesita como mínimo?" % (name(), money(meta), money(d)), "%d meses" % mm,
                   ["%d meses" % (mm - 1), "%d meses" % (mm + 2), "%d meses" % (meta // 100)], "%s ÷ %s = %s → se redondea hacia arriba: <b>%d meses</b>." % (money(meta), money(d), d2(meta / d, 2), mm))
    if t == "tarjeta":
        saldo = R.choice([4000, 6000, 8000, 10000, 15000])
        im = R.choice([3, 4, 5])
        return opt("Una tarjeta de crédito cobra %d %% de interés mensual sobre el saldo. Si debes %s y no pagas nada en 2 meses, ¿cuánto deberás? (sin otros cargos)" % (im, money(saldo)),
                   money(round(saldo * (1 + im / 100) ** 2, 2)), [money(saldo * (1 + 2 * im / 100)), money(saldo * (1 + im / 100)), money(round(saldo * im * 2 / 100))],
                   "El interés se suma al saldo cada mes: %s × %s² = <b>%s</b>. Las deudas crecen igual que el interés compuesto." % (money(saldo), d2(1 + im / 100, 2), money(round(saldo * (1 + im / 100) ** 2, 2))))
    r2 = r + R.choice([1, 2, 3])
    ms = C * (1 + r2 * n / 100)
    mc = C * (1 + r / 100) ** n
    ok = "interés simple al %d %%" % r2 if ms > mc else "interés compuesto al %d %%" % r
    if abs(ms - mc) < 1:
        return None
    return opt("Para %s durante %d años, ¿qué conviene más: interés simple al %d %% anual o interés compuesto al %d %% anual?" % (money(C), n, r2, r), ok,
               ["interés compuesto al %d %%" % r if ok.startswith("interés simple") else "interés simple al %d %%" % r2, "dan lo mismo", "no se puede comparar"],
               "Simple: %s × (1 + %s × %d) = %s. Compuesto: %s × %s<sup>%d</sup> ≈ %s. Conviene <b>%s</b>." % (money(C), d2(r2 / 100, 2), n, money(round(ms)), money(C), d2(1 + r / 100, 2), n, money(round(mc)), ok))


# ============================================================ P10: cuadriláteros cíclicos y triángulos
def lp10(*ks):
    t = pick(ks, ["ciclico", "es_ciclico", "angulos", "equi"])
    if t == "equi":
        l = R.choice(range(4, 41, 2))
        q = R.choice(["h", "A"])
        h = l * math.sqrt(3) / 2
        if q == "h":
            return opt("En el triángulo de Napoleón se construyen triángulos equiláteros sobre los lados. ¿Cuánto mide la altura de un triángulo equilátero de lado %d cm? (a los décimos)" % l,
                       d2(h, 1) + " cm", [d2(l / 2, 1) + " cm", d2(l * math.sqrt(2) / 2, 1) + " cm", d2(h * 2, 1) + " cm"],
                       "Por Pitágoras: h = √(%d² − %d²) = %d√3/2 ≈ <b>%s cm</b>." % (l, l // 2, l, d2(h, 1)))
        return opt("¿Cuál es el área de un triángulo equilátero de lado %d cm? (a los décimos)" % l, d2(l * h / 2, 1) + " cm²",
                   [d2(l * l / 2, 1) + " cm²", d2(l * h, 1) + " cm²", d2(l * l * math.sqrt(3) / 2, 1) + " cm²" if False else d2(3 * l, 1) + " cm²"],
                   "h = %d√3/2 ≈ %s cm. A = base × altura ÷ 2 = (√3/4) × %d² ≈ <b>%s cm²</b>." % (l, d2(h, 2), l, d2(l * h / 2, 1)))
    if t == "ciclico":
        a = R.randint(50, 130)
        b = R.randint(50, 130)
        q = R.choice(["C", "D"])
        v = 180 - a if q == "C" else 180 - b
        return opt("El cuadrilátero ABCD está inscrito en una circunferencia (es cíclico). Si ∠A = %d° y ∠B = %d°, ¿cuánto mide ∠%s?" % (a, b, q), "%d°" % v,
                   ["%d°" % (360 - a - b), "%d°" % (180 - (b if q == "C" else a)), "%d°" % (a if q == "C" else b)],
                   "En un cuadrilátero cíclico los ángulos opuestos suman 180°: ∠%s = 180° − %d° = <b>%d°</b>." % (q, a if q == "C" else b, v))
    if t == "es_ciclico":
        a, c = R.randint(60, 120), 0
        cyc = R.random() < .5
        c = 180 - a if cyc else 180 - a + R.choice([-15, -10, 10, 15])
        b = R.randint(60, 120)
        d = 360 - a - b - c
        if d <= 20 or d >= 170:
            return None
        return opt("Un cuadrilátero tiene ángulos ∠A = %d°, ∠B = %d°, ∠C = %d° y ∠D = %d°. ¿Se puede inscribir en una circunferencia?" % (a, b, c, d),
                   "sí, porque ∠A + ∠C = 180°" if cyc else "no, porque ∠A + ∠C ≠ 180°", ["no, porque ∠A + ∠C ≠ 180°" if cyc else "sí, porque ∠A + ∠C = 180°", "sí, todos los cuadriláteros se pueden inscribir", "solo si es un cuadrado"],
                   "Un cuadrilátero es cíclico si sus ángulos opuestos suman 180°. ∠A + ∠C = %d° → <b>%s</b>." % (a + c, "sí" if cyc else "no"))
    a, b = R.randint(30, 80), R.randint(30, 80)
    return opt("En un triángulo, dos ángulos miden %d° y %d°. ¿Cuánto mide el tercero?" % (a, b), "%d°" % (180 - a - b),
               ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (180 - a)], "Los ángulos de un triángulo suman 180°: 180° − %d° − %d° = <b>%d°</b>." % (a, b, 180 - a - b))


# ============================================================ P11: geometría analítica (coordenadas)
def pt(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


def lp11(*ks):
    t = pick(ks, ["dist", "medio", "area", "perim", "extremo"])
    if t == "dist":
        dx, dy, dd = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25)])
        x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
        x2, y2 = x1 + dx * R.choice([1, -1]), y1 + dy * R.choice([1, -1])
        if R.random() < .5:
            x2, y2 = x1 + (y2 - y1), y1 + (x2 - x1)
        return opt("Calcula la distancia entre A%s y B%s." % (pt(x1, y1), pt(x2, y2)), num(dd), [num(dx + dy), num(dd * dd), num(abs(abs(x2 - x1) - abs(y2 - y1)))],
                   "d = √((%s)² + (%s)²) = √%d = <b>%d</b>." % (sg(x2 - x1), sg(y2 - y1), dd * dd, dd))
    if t == "medio":
        x1, y1, x2, y2 = [R.randint(-9, 9) for _ in range(4)]
        if (x1, y1) == (x2, y2):
            return None
        mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
        return opt("¿Cuál es el punto medio del segmento con extremos A%s y B%s?" % (pt(x1, y1), pt(x2, y2)), "(%s, %s)" % (fq(mx), fq(my)),
                   ["(%s, %s)" % (fq(F(x2 - x1, 2)), fq(F(y2 - y1, 2))), "(%s, %s)" % (sg(x1 + x2), sg(y1 + y2)), "(%s, %s)" % (fq(my), fq(mx))],
                   "M = ((x₁ + x₂)/2, (y₁ + y₂)/2) = <b>(%s, %s)</b>." % (fq(mx), fq(my)))
    if t == "extremo":
        x1, y1, mx, my = [R.randint(-6, 6) for _ in range(4)]
        if (x1, y1) == (mx, my):
            return None
        x2, y2 = 2 * mx - x1, 2 * my - y1
        return opt("El punto medio de AB es M%s y A = %s. ¿Cuáles son las coordenadas de B?" % (pt(mx, my), pt(x1, y1)), pt(x2, y2),
                   [pt(mx - x1, my - y1), "(%s, %s)" % (fq(F(mx + x1, 2)), fq(F(my + y1, 2))), pt(x1 - 2 * mx, y1 - 2 * my)],
                   "x₂ = 2 × %s − (%s) = %s; y₂ = 2 × %s − (%s) = %s. B = <b>%s</b>." % (sg(mx), sg(x1), sg(x2), sg(my), sg(y1), sg(y2), pt(x2, y2)))
    if t == "area":
        while True:
            P = [(R.randint(-6, 6), R.randint(-6, 6)) for _ in range(3)]
            A2 = abs(P[0][0] * (P[1][1] - P[2][1]) + P[1][0] * (P[2][1] - P[0][1]) + P[2][0] * (P[0][1] - P[1][1]))
            if A2 > 0:
                break
        A = F(A2, 2)
        return opt("Calcula el área del triángulo con vértices %s, %s y %s." % tuple(pt(*p) for p in P), fq(A) + " u²", [fq(A * 2) + " u²", fq(A + 1) + " u²", fq(A / 2) + " u²"],
                   "Con la fórmula del determinante: A = ½ |x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)| = ½ × %d = <b>%s u²</b>." % (A2, fq(A)))
    # perímetro de un rectángulo o triángulo rectángulo con catetos paralelos a los ejes
    x1, y1 = R.randint(-6, 3), R.randint(-6, 3)
    dx, dy, dd = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (4, 3, 5)])
    return opt("Calcula el perímetro del triángulo con vértices A%s, B%s y C%s." % (pt(x1, y1), pt(x1 + dx, y1), pt(x1 + dx, y1 + dy)), num(dx + dy + dd),
               [num(dx + dy), num(dx * dy // 2), num(2 * (dx + dy))], "AB = %d, BC = %d y AC = √(%d² + %d²) = %d. Perímetro = <b>%d</b>." % (dx, dy, dx, dy, dd, dx + dy + dd))


# ============================================================ P12: funciones polinomiales
def poly(cs):
    """[a_n, …, a_0] → «2x³ − x + 5»"""
    n = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        e = n - i
        if c == 0:
            continue
        v = "" if e == 0 else "x" if e == 1 else "x" + "⁰¹²³⁴⁵⁶⁷⁸⁹"[e]
        body = (num(abs(c)) if abs(c) != 1 or e == 0 else "") + v
        out += (MINUS if c < 0 else "") + body if not out else (" − " if c < 0 else " + ") + body
    return out or "0"


def lp12(*ks):
    t = pick(ks, ["eval", "grado", "raices", "corte", "tipo", "vertice"])
    if t == "eval":
        cs = [R.randint(-4, 4) or 1 for _ in range(R.choice([3, 4]))]
        x = R.randint(-3, 3)
        v = sum(c * x ** (len(cs) - 1 - i) for i, c in enumerate(cs))
        w = [sg(sum(c * (-x) ** (len(cs) - 1 - i) for i, c in enumerate(cs))), sg(sum(cs)), sg(v + 2)]
        return opt("Si f(x) = %s, ¿cuánto vale f(%s)?" % (poly(cs), sg(x)), sg(v), w, "Sustituimos x = %s: f(%s) = <b>%s</b>." % (sg(x), sg(x), sg(v)))
    if t == "grado":
        n = R.randint(1, 5)
        cs = [R.randint(1, 6) * R.choice([1, -1])] + [R.randint(-5, 5) for _ in range(n)]
        name_ = {1: "lineal", 2: "cuadrática", 3: "cúbica", 4: "de grado 4", 5: "de grado 5"}[n]
        return opt("¿Qué tipo de función polinomial es f(x) = %s?" % poly(cs), name_, R.sample([v for k, v in {1: "lineal", 2: "cuadrática", 3: "cúbica", 4: "de grado 4", 5: "de grado 5"}.items() if k != n], 3),
                   "El grado es el mayor exponente: %d → <b>%s</b>." % (n, name_))
    if t == "raices":
        rs = sorted(R.sample(range(-6, 7), R.choice([2, 3])))
        cs = [1]
        for r in rs:
            cs = [a - r * b for a, b in zip(cs + [0], [0] + cs)]
        fac = "".join("(x %s %d)" % ("−" if r > 0 else "+", abs(r)) if r else "x" for r in rs)
        ok = ", ".join(sg(r) for r in rs)
        return opt("¿Cuáles son los ceros (raíces) de f(x) = %s?" % fac, "x = " + ok, ["x = " + ", ".join(sg(-r) for r in rs), "x = " + ", ".join(sg(r + 1) for r in rs), "x = " + sg(cs[-1])],
                   "Cada factor se hace 0 cuando x = %s." % ok)
    if t == "corte":
        cs = [R.randint(-4, 4) or 1 for _ in range(R.choice([3, 4]))]
        return opt("¿En qué punto corta al eje y la gráfica de f(x) = %s?" % poly(cs), "(0, %s)" % sg(cs[-1]), ["(%s, 0)" % sg(cs[-1]), "(0, %s)" % sg(cs[0]), "(0, 0)"],
                   "Corta al eje y cuando x = 0: f(0) = <b>%s</b>." % sg(cs[-1]))
    if t == "tipo":
        items = [("Una función cuadrática f(x) = ax² + bx + c con a &lt; 0 tiene una gráfica que…", "abre hacia abajo y tiene un máximo", ["abre hacia arriba", "es una recta", "no corta al eje y"], "Si a &lt; 0, la parábola abre hacia abajo."),
                 ("La gráfica de una función lineal f(x) = mx + b es…", "una recta", ["una parábola", "una curva en forma de S", "un círculo"], "Grado 1: la gráfica es una recta con pendiente m."),
                 ("Una función cúbica puede cortar al eje x…", "hasta en 3 puntos", ["exactamente en 2 puntos", "nunca", "en infinitos puntos"], "Un polinomio de grado n tiene a lo más n raíces reales."),
                 ("¿Qué modelo describe mejor el área de un cuadrado en función de su lado?", "cuadrático: A = l²", ["lineal: A = 4l", "constante", "cúbico: A = l³"], "El área crece con el cuadrado del lado."),
                 ("¿Qué modelo describe el volumen de un cubo en función de su arista?", "cúbico: V = a³", ["cuadrático: V = a²", "lineal: V = 3a", "constante"], "El volumen es la arista al cubo."),
                 ("El costo de un taxi es $40 de banderazo más $8 por km. ¿Qué tipo de función es?", "lineal", ["cuadrática", "cúbica", "constante"], "C(x) = 8x + 40: grado 1.")]
        return from_bank(items)
    a = R.choice([1, -1, 2, -2])
    h, k = R.randint(-5, 5), R.randint(-8, 8)
    b, c = -2 * a * h, a * h * h + k
    return opt("¿Cuál es el vértice de la parábola f(x) = %s?" % poly([a, b, c]), pt(h, k), [pt(-h, k), pt(h, -k), pt(k, h)],
               "h = −b/(2a) = %s; k = f(%s) = %s. Vértice <b>%s</b>." % (sg(h), sg(h), sg(k), pt(h, k)))
