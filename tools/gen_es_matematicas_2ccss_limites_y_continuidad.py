# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Límites y continuidad (Sentido de la medida)
Límites en el infinito, indeterminaciones, asíntotas, continuidad de funciones a trozos; límites y continuidad en contextos económicos (coste medio, tarifas, aprendizaje).
Reutiliza los generadores de Matemáticas I y de 1.º CCSS con otra semilla.
Errores: decir que 0/0 = 0, comparar mal los grados, olvidar que una función a trozos debe coincidir en el punto de unión.
"""
import random
from es_ccss import M, mix, unit, L, use_, kurve, BLUE

R = random.Random(54004)
s_contexto, = use_("gen_es_matematicas_1ccss_limites_y_continuidad", 54304, "s_contexto"),
s_infinito, s_indet, s_asintotas, s_continuidad = use_("gen_es_matematicas_1bach_limites", 54104, "s_infinito", "s_indet", "s_asintotas", "s_continuidad")

seen = set()
sets = [("Límites en el infinito", mix(R, seen, [(s_infinito, 20)])), ("Indeterminaciones", mix(R, seen, [(s_indet, 20)])), ("Asíntotas", mix(R, seen, [(s_asintotas, 20)])),
        ("Continuidad", mix(R, seen, [(s_continuidad, 20)])), ("Límites en economía", mix(R, seen, [(s_contexto, 20)]))]
think = ["Cuando x → ±∞, en un cociente de polinomios mandan los términos de mayor grado: si el de arriba es mayor, el límite es ±∞; si son iguales, el cociente de coeficientes; si el de abajo es mayor, 0.",
         "<b>Indeterminaciones</b>: 0/0 (factoriza y simplifica), ∞/∞ (compara grados), ∞ − ∞ (opera o usa el conjugado).",
         "<b>Asíntotas</b>: vertical x = a si f → ±∞ cuando x → a; horizontal y = k si f → k cuando x → ±∞; oblicua y = mx + n si el grado de arriba es uno más.",
         "Una función a trozos es <b>continua</b> en el punto de unión si los límites laterales coinciden con el valor de la función."]
ex = [("Coste medio (3000 + 4x)/x, x → +∞", ["mismo grado: 4/1"], "4 €"), ("f(x) = 2x si x ≤ 5; a + x si x &gt; 5, continua", ["2 · 5 = a + 5"], "a = 5")]
mist = [["Decir que 0/0 = 0", "Es una indeterminación: hay que simplificar."], ["Comparar mal los grados", "Mira el exponente mayor arriba y abajo."], ["Olvidar los límites laterales", "En las funciones a trozos son clave."]]
body = L(think, ex, mist, kurve([(lambda x: (2 * x + 1) / (x - 1) if abs(x - 1) > 0.12 else None, BLUE, "")], (-5, 6, 1), (-5, 7, 1), W=330, H=280, label="función con asíntotas x = 1 e y = 2"))
faq = [("¿Qué indica una asíntota horizontal en un problema?", "El valor al que se acerca la magnitud a largo plazo: el coste medio por unidad, la población máxima o el rendimiento máximo."),
       ("¿Por qué deben ser continuas muchas tarifas?", "Para que no haya saltos de precio: al pasar de un tramo a otro, las dos fórmulas deben dar lo mismo en el punto de unión.")]
unit(2, R, "limites-y-continuidad", "M", "Límites de funciones: límites en el infinito, indeterminaciones y asíntotas; continuidad de funciones a trozos; aplicaciones a la economía",
     "Límites y continuidad", "Límites y continuidad", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: límites, indeterminaciones, asíntotas, continuidad y aplicaciones económicas. 100 ejercicios.",
     "∞/∞: compara los grados", "A trozos: los dos lados deben coincidir.", body, faq, sets, 4)
