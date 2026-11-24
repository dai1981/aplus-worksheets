# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 7): la derivada: interpretación y definición; derivadas de funciones constantes, lineales y polinomiales."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120107))
tvm = src("gen_es_matematicas_1bach_derivadas", 120307, "s_tvm", lv=1, extra=(lambda it: "definición" in it["q"],))
unit("la-derivada", 7, ("Derivadas", 7, "La derivada"),
     "Interpreta y define la derivada como límite del cociente de diferencias, y calcula derivadas de funciones constantes, lineales y polinomiales",
     "La derivada: definición y polinomios", "La derivada",
     "Ejercicios de Pensamiento Matemático III: definición de derivada con el límite, cociente de diferencias, derivadas de polinomios y su significado. 100 ejercicios con respuestas.",
     "f′(a) = lím [f(a + h) − f(a)] ÷ h", "Para xⁿ: n·xⁿ⁻¹.",
     ["La <b>derivada</b> f′(a) es el límite del cociente [f(a + h) − f(a)] ÷ h cuando h → 0: la pendiente de la tangente.",
      "Reglas básicas: constante → 0; mx + b → m; xⁿ → n·xⁿ⁻¹; y se deriva término a término.",
      "Si f′(a) &gt; 0 la función crece en a; si f′(a) &lt; 0, decrece; si f′(a) = 0, la tangente es horizontal."],
     [("f(x) = 3x² − 4x + 1", ["f′(x) = 6x − 4", "f′(2) = 8"], "8")],
     [["Derivar x² como x", "Es 2x."], ["Olvidar que la constante se va", "La derivada de 7 es 0."], ["Sustituir antes de derivar", "Primero deriva, luego sustituye."]],
     [("¿Qué significa f′(3) = 5?", "Que en x = 3 la función aumenta unas 5 unidades por cada unidad de x."), ("¿Quién usó la notación dy/dx?", "Leibniz; Newton usaba un punto sobre la letra.")],
     [("Por definición", [(lambda: S.q7("def"), 12), (tvm, 8)]), ("Cociente de diferencias", [(lambda: S.q7("cociente"), 20)]), ("Derivada de polinomios", [(lambda: S.q7("valor"), 20)]),
      ("Significado", [(lambda: S.q7("concepto"), 6), (lambda: S.q7("valor"), 14)]), ("Repaso", [(lambda: S.q7("def"), 10), (tvm, 10)])],
     120007, lv=12)
