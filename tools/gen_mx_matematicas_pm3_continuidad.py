# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 6): continuidad con límites y teorema del valor intermedio."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120106))
con, asi = src("gen_es_matematicas_1bach_limites", 120306, "s_continuidad", "s_asintotas", lv=1)
tro = src("gen_es_matematicas_1bach_funciones", 120316, "s_trozos")
unit("continuidad", 6, ("Límites y continuidad", 6, "Continuidad"),
     "Formaliza la continuidad con límites, reconoce tipos de discontinuidad y asíntotas, y aplica el teorema del valor intermedio para localizar ceros",
     "Continuidad y valor intermedio", "Continuidad",
     "Ejercicios de Pensamiento Matemático III: condiciones de continuidad, tipos de discontinuidad, funciones a trozos, asíntotas y teorema del valor intermedio. 100 ejercicios con respuestas.",
     "Continua: sin levantar el lápiz", "f(a) existe y es igual al límite.",
     ["f es <b>continua</b> en x = a si: 1) f(a) existe, 2) el límite en a existe y 3) son iguales.",
      "Discontinuidades: <b>evitable</b> (un hueco), de <b>salto</b> (los laterales no coinciden) o <b>infinita</b> (asíntota vertical).",
      "<b>Teorema del valor intermedio</b>: si f es continua en [a, b] y f(a) y f(b) tienen signos distintos, hay al menos un cero entre a y b."],
     [("f(x) = x³ − 2x − 5", ["f(2) = −1", "f(3) = 16"], "hay un cero entre 2 y 3")],
     [["Pensar que el teorema da el valor exacto", "Solo asegura que existe."], ["Olvidar comprobar f(a)", "Las tres condiciones son necesarias."], ["Usar el teorema sin continuidad", "Si hay un salto, puede no haber cero."]],
     [("¿Cómo se encuentra el cero con más precisión?", "Partiendo el intervalo a la mitad una y otra vez (método de bisección)."), ("¿Las funciones racionales son continuas?", "Sí, salvo donde se anula el denominador.")],
     [("Tipos de discontinuidad", [(con, 14), (lambda: S.q6("tipo"), 6)]), ("Funciones a trozos", [(tro, 10), (lambda: S.q6("param"), 10)]), ("Asíntotas", [(asi, 20)]),
      ("Teorema del valor intermedio", [(lambda: S.q6("tvi"), 20)]), ("Localizar ceros", [(lambda: S.q6("intervalo"), 20)])],
     120006, lv=12)
