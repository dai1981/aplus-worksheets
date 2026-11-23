# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de ESO: Combinatoria (Sentido estocástico)
Principio multiplicativo y diagramas de árbol, factorial, permutaciones (con y sin repetición), variaciones (con y sin repetición), combinaciones y números combinatorios, problemas
y probabilidad con técnicas de recuento.
Errores: usar combinaciones cuando importa el orden, olvidar si se pueden repetir los elementos, confundir n! con n · 2.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, num, fq, unit, L, Kids

R = random.Random(50012)
K = Kids(R)


def V(n, k):
    return math.perm(n, k)


def C(n, k):
    return math.comb(n, k)


def cnk(n, k):
    return "C<sub>%d,%d</sub>" % (n, k)


def s_multiplicativo():
    t = R.choice(["menu", "ropa", "matricula", "codigo", "caminos", "dados"])
    if t == "menu":
        a, b, c = R.randint(2, 6), R.randint(2, 6), R.randint(2, 5)
        n = a * b * c
        return M("Un menú tiene %d primeros, %d segundos y %d postres. ¿Cuántos menús distintos se pueden elegir?" % (a, b, c), num(n), [num(a + b + c), num(a * b + c), num(C(a + b + c, 3))], "Principio multiplicativo: %d · %d · %d = <b>%d</b>." % (a, b, c, n))
    if t == "ropa":
        a, b, c = R.randint(2, 7), R.randint(2, 6), R.randint(2, 4)
        return M("Tienes %d camisetas, %d pantalones y %d pares de zapatillas. ¿De cuántas formas puedes vestirte?" % (a, b, c), num(a * b * c), [num(a + b + c), num(a * b), num((a + b) * c)], "%d · %d · %d = <b>%d</b>." % (a, b, c, a * b * c))
    if t == "matricula":
        return M("Las matrículas españolas tienen 4 cifras y 3 letras (de un alfabeto de 20 letras). ¿Cuántas matrículas distintas hay?", num(10 ** 4 * 20 ** 3), [num(10 * 4 * 20 * 3), num(V(10, 4) * V(20, 3)), num(10 ** 4 + 20 ** 3)], "10⁴ · 20³ = 10 000 · 8000 = <b>%s</b>." % num(10 ** 4 * 20 ** 3)) if R.random() < 0.3 else None
    if t == "codigo":
        n = R.randint(3, 6)
        return M("¿Cuántos códigos de %d cifras (del 0 al 9) se pueden formar si las cifras se pueden repetir?" % n, num(10 ** n), [num(V(10, n)), num(10 * n), num(C(10, n))], "10 posibilidades en cada cifra: 10<sup>%d</sup> = <b>%s</b>." % (n, num(10 ** n)))
    if t == "caminos":
        a, b = R.randint(2, 5), R.randint(2, 5)
        return M("De A a B hay %d caminos y de B a C hay %d. ¿De cuántas formas se puede ir de A a C pasando por B, y volver por caminos distintos a los de ida?" % (a, b), num(a * b * (a - 1) * (b - 1)), [num(a * b), num((a * b) ** 2), num(a * b * 2)], "Ida: %d · %d; vuelta: %d · %d. Total: <b>%d</b>." % (a, b, b - 1, a - 1, a * b * (a - 1) * (b - 1)))
    k = R.randint(2, 4)
    return M("Se lanzan %d dados. ¿Cuántos resultados distintos (en orden) hay?" % k, num(6 ** k), [num(6 * k), num(C(6 + k - 1, k)), num(V(6, k))], "6<sup>%d</sup> = <b>%s</b>." % (k, num(6 ** k)))


def s_factorial():
    t = R.choice(["fact", "cociente", "perm", "perm", "rep", "circ"])
    if t == "fact":
        n = R.randint(3, 9)
        return M("¿Cuánto vale %d!?" % n, num(math.factorial(n)), [num(n * (n - 1)), num(math.factorial(n - 1)), num(n * 2)], "%s = <b>%s</b>." % (" · ".join(str(i) for i in range(n, 0, -1)), num(math.factorial(n))))
    if t == "cociente":
        n = R.randint(6, 15)
        k = R.randint(2, 4)
        v = math.factorial(n) // math.factorial(n - k)
        return M("Calcula %d! / %d!." % (n, n - k), num(v), [num(math.factorial(k)), num(n - (n - k)), num(n * k)], "Se simplifica: %s = <b>%s</b>." % (" · ".join(str(i) for i in range(n, n - k, -1)), num(v)))
    if t == "perm":
        n = R.randint(3, 8)
        ctx = R.choice(["libros en una estantería", "amigos en una fila de butacas", "corredores en la llegada (sin empates)", "letras distintas de una palabra"])
        return M("¿De cuántas formas se pueden ordenar %d %s?" % (n, ctx), num(math.factorial(n)), [num(n * n), num(n ** n), num(n * (n - 1))], "Permutaciones: P<sub>%d</sub> = %d! = <b>%s</b>." % (n, n, num(math.factorial(n))))
    if t == "rep":
        w = R.choice([("CASA", {"A": 2}), ("PAPEL", {"P": 2}), ("RIORIO", None), ("ANA", {"A": 2}), ("PERRO", {"R": 2}), ("BANANA", {"A": 3, "N": 2}), ("TOMATE", {"T": 2}), ("COCO", {"C": 2, "O": 2}), ("SALSA", {"S": 2, "A": 2}), ("PAPAYA", {"A": 3, "P": 2})])
        if w[1] is None:
            return None
        n = len(w[0])
        den = 1
        for v in w[1].values():
            den *= math.factorial(v)
        ok = math.factorial(n) // den
        return M("¿Cuántas palabras distintas (con o sin sentido) se pueden formar con las letras de %s?" % w[0], num(ok), [num(math.factorial(n)), num(math.factorial(n) // 2) if den != 2 else num(math.factorial(n - 1)), num(n ** 2)],
                 "Permutaciones con repetición: %d! / %s = <b>%s</b>." % (n, " · ".join("%d!" % v for v in w[1].values()), num(ok)))
    n = R.randint(4, 8)
    return M("¿De cuántas formas se pueden sentar %d personas alrededor de una mesa redonda (importa solo quién está al lado de quién)?" % n, num(math.factorial(n - 1)), [num(math.factorial(n)), num(n * (n - 1)), num(math.factorial(n) // 2)], "Permutación circular: (%d − 1)! = <b>%s</b>." % (n, num(math.factorial(n - 1))))


def s_variaciones():
    t = R.choice(["podio", "cargos", "numeros", "rep", "banderas"])
    if t == "podio":
        n = R.randint(5, 12)
        return M("En una carrera participan %d atletas. ¿De cuántas formas se pueden repartir el oro, la plata y el bronce?" % n, num(V(n, 3)), [num(C(n, 3)), num(n ** 3), num(3 * n)], "Importa el orden y no se repite: V<sub>%d,3</sub> = %d · %d · %d = <b>%s</b>." % (n, n, n - 1, n - 2, num(V(n, 3))))
    if t == "cargos":
        n, k = R.randint(6, 25), 2
        return M("En una clase de %d alumnos se elige delegado y subdelegado. ¿De cuántas formas?" % n, num(V(n, 2)), [num(C(n, 2)), num(n * n), num(2 * n)], "V<sub>%d,2</sub> = %d · %d = <b>%s</b>." % (n, n, n - 1, num(V(n, 2))))
    if t == "numeros":
        digs = sorted(R.sample(range(1, 10), R.randint(4, 6)))
        k = R.randint(2, 3)
        n = len(digs)
        return M("¿Cuántos números de %d cifras distintas se pueden formar con las cifras %s?" % (k, ", ".join(map(str, digs))), num(V(n, k)), [num(n ** k), num(C(n, k)), num(math.factorial(n))], "Importa el orden y no se repiten: V<sub>%d,%d</sub> = <b>%s</b>." % (n, k, num(V(n, k))))
    if t == "rep":
        n, k = R.randint(2, 5), R.randint(3, 6)
        ctx = R.choice(["Una quiniela tiene %d partidos con 3 resultados posibles (1, X, 2)" % k, "Un código de %d símbolos usa solo 0 y 1" % k])
        base = 3 if "quiniela" in ctx else 2
        return M("%s. ¿Cuántas posibilidades hay?" % ctx, num(base ** k), [num(base * k), num(k ** base), num(V(base + k, k)), num(base ** (k - 1))], "Variaciones con repetición: %d<sup>%d</sup> = <b>%s</b>." % (base, k, num(base ** k)))
    n = R.randint(4, 7)
    return M("Con %d colores distintos, ¿cuántas banderas de 3 franjas horizontales de colores distintos se pueden hacer?" % n, num(V(n, 3)), [num(C(n, 3)), num(n ** 3), num(3 ** n)], "V<sub>%d,3</sub> = %d · %d · %d = <b>%s</b>." % (n, n, n - 1, n - 2, num(V(n, 3))))


def s_combinaciones():
    t = R.choice(["num", "num", "equipo", "saludos", "pizza", "loteria", "diag"])
    if t == "num":
        n = R.randint(4, 12)
        k = R.randint(2, n - 2)
        return M("Calcula %s (combinaciones de %d elementos tomados de %d en %d)." % (cnk(n, k), n, k, k), num(C(n, k)), [num(V(n, k)), num(n * k), num(C(n, k - 1)) if C(n, k - 1) != C(n, k) else num(C(n, k) + n)], "%s = %d! / (%d! · %d!) = <b>%s</b>." % (cnk(n, k), n, k, n - k, num(C(n, k))))
    if t == "equipo":
        n, k = R.randint(6, 15), R.randint(2, 5)
        return M("¿De cuántas formas se puede elegir un grupo de %d alumnos entre %d?" % (k, n), num(C(n, k)), [num(V(n, k)), num(n ** k), num(n * k)], "No importa el orden: C<sub>%d,%d</sub> = <b>%s</b>." % (n, k, num(C(n, k))))
    if t == "saludos":
        n = R.randint(4, 20)
        return M("En una reunión hay %d personas y cada una saluda a todas las demás una vez. ¿Cuántos saludos hay?" % n, num(C(n, 2)), [num(n * (n - 1)), num(n * n), num(n - 1)], "Cada saludo es una pareja: C<sub>%d,2</sub> = %d · %d / 2 = <b>%s</b>." % (n, n, n - 1, num(C(n, 2))))
    if t == "pizza":
        n, k = R.randint(5, 10), R.randint(2, 4)
        return M("Una pizzería ofrece %d ingredientes. ¿Cuántas pizzas distintas de %d ingredientes diferentes se pueden pedir?" % (n, k), num(C(n, k)), [num(V(n, k)), num(n ** k), num(math.factorial(k))], "No importa el orden: C<sub>%d,%d</sub> = <b>%s</b>." % (n, k, num(C(n, k))))
    if t == "loteria":
        n, k = R.choice([(49, 6), (40, 5), (30, 4), (20, 3), (50, 5)])
        return M("En un sorteo se eligen %d números distintos entre 1 y %d, sin importar el orden. ¿Cuántas combinaciones posibles hay?" % (k, n), num(C(n, k)), [num(V(n, k)), num(n ** k), num(n * k)], "C<sub>%d,%d</sub> = <b>%s</b>." % (n, k, num(C(n, k))))
    n = R.randint(5, 12)
    return M("¿Cuántas diagonales tiene un polígono de %d lados?" % n, num(C(n, 2) - n), [num(C(n, 2)), num(n * (n - 3)), num(n - 3)], "Segmentos entre vértices menos lados: C<sub>%d,2</sub> − %d = <b>%d</b>." % (n, n, C(n, 2) - n))


def s_elegir():
    t = R.choice(["tipo", "tipo", "prob", "prob"])
    if t == "tipo":
        q, a = R.choice([("Elegir 3 libros para llevar de vacaciones entre 10", "combinaciones"), ("Ordenar a 6 personas en una foto", "permutaciones"), ("Asignar presidente, secretario y tesorero entre 12 socios", "variaciones sin repetición"),
                         ("Escribir números de 4 cifras con las cifras del 1 al 5, pudiendo repetir", "variaciones con repetición"), ("Formar un equipo de 5 jugadores entre 9", "combinaciones"), ("Repartir los tres primeros puestos de un concurso entre 15", "variaciones sin repetición"),
                         ("Rellenar una quiniela de 14 partidos", "variaciones con repetición"), ("Colocar 7 coches distintos en 7 plazas de garaje", "permutaciones"), ("Elegir 2 sabores de helado distintos entre 8", "combinaciones"),
                         ("Crear un PIN de 4 cifras", "variaciones con repetición")])
        return M("¿Qué técnica de recuento hay que usar? %s." % q, a, [x for x in ["combinaciones", "permutaciones", "variaciones sin repetición", "variaciones con repetición"] if x != a],
                 "¿Importa el orden? ¿Se pueden repetir? ¿Entran todos? <b>%s</b>." % a)
    k = R.choice(["pin", "orden", "comite", "podio"])
    if k == "pin":
        n = R.randint(3, 4)
        return M("Un candado tiene una clave de %d cifras. Si pruebas una al azar, ¿qué probabilidad tienes de acertar?" % n, fq(F(1, 10 ** n)), [fq(F(1, V(10, n))), fq(F(n, 10)), fq(F(1, 10 * n))], "Casos posibles 10<sup>%d</sup>: P = <b>%s</b>." % (n, fq(F(1, 10 ** n))))
    if k == "orden":
        n = R.randint(3, 6)
        return M("Se colocan al azar %d libros distintos en una estantería. ¿Cuál es la probabilidad de que queden en orden alfabético?" % n, fq(F(1, math.factorial(n))), [fq(F(1, n)), fq(F(1, n * n)), fq(F(2, math.factorial(n))), fq(F(1, 2 ** n))], "Solo 1 de las %d! = %d ordenaciones: <b>%s</b>." % (n, math.factorial(n), fq(F(1, math.factorial(n)))))
    if k == "comite":
        n = R.randint(6, 12)
        return M("Se eligen al azar 2 alumnos entre %d. ¿Qué probabilidad hay de que salgan Ana y Luis (que están en el grupo)?" % n, fq(F(1, C(n, 2))), [fq(F(1, V(n, 2))), fq(F(2, n)), fq(F(1, n))], "1 pareja favorable entre C<sub>%d,2</sub> = %d: <b>%s</b>." % (n, C(n, 2), fq(F(1, C(n, 2)))))
    n = R.randint(5, 10)
    return M("En una carrera de %d corredores igual de buenos, ¿qué probabilidad hay de acertar el orden exacto de los tres primeros?" % n, fq(F(1, V(n, 3))), [fq(F(1, C(n, 3))), fq(F(3, n)), fq(F(1, n ** 3))], "1 entre V<sub>%d,3</sub> = %d: <b>%s</b>." % (n, V(n, 3), fq(F(1, V(n, 3)))))


seen = set()
sets = [("Principio multiplicativo", mix(R, seen, [(s_multiplicativo, 20)])), ("Factorial y permutaciones", mix(R, seen, [(s_factorial, 20)])), ("Variaciones", mix(R, seen, [(s_variaciones, 20)])),
        ("Combinaciones", mix(R, seen, [(s_combinaciones, 20)])), ("Elegir la técnica y probabilidad", mix(R, seen, [(s_elegir, 20)]))]
think = ["<b>Principio multiplicativo</b>: si una elección tiene a opciones y otra b, juntas tienen a · b.",
         "<b>Permutaciones</b> (ordenar todos): P<sub>n</sub> = n! = n · (n − 1) · … · 1.",
         "<b>Variaciones</b> (elegir k de n, importa el orden): V<sub>n,k</sub> = n · (n − 1) · … (k factores). Con repetición: n<sup>k</sup>.",
         "<b>Combinaciones</b> (elegir k de n, no importa el orden): C<sub>n,k</sub> = n! / (k! · (n − k)!).",
         "Preguntas clave: ¿importa el orden? ¿se pueden repetir? ¿entran todos los elementos?"]
ex = [("Oro, plata y bronce entre 8", ["importa el orden"], "V<sub>8,3</sub> = 8 · 7 · 6 = 336"), ("Grupo de 3 entre 8", ["no importa el orden"], "C<sub>8,3</sub> = 56")]
mist = [["Usar combinaciones cuando importa el orden", "Delegado y subdelegado no es lo mismo que subdelegado y delegado."], ["Olvidar si se repiten", "Un PIN puede repetir cifras: 10⁴."], ["Calcular n! como n · 2", "5! = 5 · 4 · 3 · 2 · 1 = 120."]]
body = L(think, ex, mist)
faq = [("¿Cuál es la diferencia entre variaciones y combinaciones?", "En las variaciones importa el orden (podio); en las combinaciones no (un grupo)."),
       ("¿Para qué sirve la combinatoria en probabilidad?", "Para contar los casos posibles y los favorables cuando son muchos y aplicar la regla de Laplace.")]
unit(4, R, "combinatoria", "S", "Técnicas de recuento: principio multiplicativo, diagramas de árbol, permutaciones, variaciones y combinaciones; aplicación al cálculo de probabilidades",
     "Combinatoria", "Combinatoria", "Fichas de matemáticas de 4.º de ESO: principio multiplicativo, factorial, permutaciones, variaciones, combinaciones y probabilidad. 100 ejercicios con soluciones.",
     "¿Importa el orden? ¿Se repiten?", "Variaciones, permutaciones o combinaciones.", body, faq, sets, 12)
