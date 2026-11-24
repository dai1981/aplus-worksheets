# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 8): reglas de derivación: suma, producto, cociente y regla de la cadena."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120108))
reg, pro, cad = src("gen_es_matematicas_1bach_derivadas", 120308, "s_reglas", "s_prod", "s_cadena", lv=1, rep=[("Deriva ", "Deriva "), (" sen ", " sen ")])
unit("reglas-de-derivacion", 8, ("Derivadas", 8, "Reglas de derivación"),
     "Aplica de forma heurística las reglas de derivación de la suma, el producto, el cociente y la regla de la cadena",
     "Reglas de derivación", "Reglas de derivación",
     "Ejercicios de Pensamiento Matemático III: derivar potencias y raíces, regla del producto, regla del cociente y regla de la cadena con polinomios, exponenciales y trigonométricas. 100 ejercicios con respuestas.",
     "(f · g)′ = f′g + fg′", "Cadena: derivada de fuera × derivada de dentro.",
     ["<b>Suma</b>: se deriva cada término. <b>Potencia</b>: (xⁿ)′ = n·xⁿ⁻¹, también para n negativo o fraccionario (√x = x<sup>1/2</sup>).",
      "<b>Producto</b>: (f · g)′ = f′·g + f·g′. <b>Cociente</b>: (f/g)′ = (f′·g − f·g′) ÷ g².",
      "<b>Cadena</b>: si y = f(g(x)), y′ = f′(g(x)) · g′(x). Ejemplo: [(3x + 1)⁵]′ = 5(3x + 1)⁴ · 3."],
     [("(x² + 1)(x − 3)", ["2x(x − 3) + (x² + 1)·1"], "3x² − 6x + 1"), ("sen(4x)", ["cos(4x) · 4"], "4 cos(4x)")],
     [["(f · g)′ = f′ · g′", "Falta sumar los dos términos."], ["Olvidar la derivada de dentro", "En la cadena se multiplica por g′(x)."], ["Restar al revés en el cociente", "Es f′g − fg′, en ese orden."]],
     [("¿Cuál es la derivada de eˣ?", "La misma: eˣ. Por eso es tan útil en los modelos de crecimiento."), ("¿Qué es la notación de Leibniz?", "dy/dx: cambio de y entre cambio de x; con ella la cadena es dy/dx = dy/du · du/dx.")],
     [("Potencias y raíces", [(reg, 20)]), ("Producto y cociente", [(pro, 20)]), ("Regla de la cadena", [(cad, 20)]),
      ("Repaso de reglas", [(reg, 10), (cad, 10)]), ("Mezcla", [(pro, 8), (cad, 6), (reg, 6)])],
     120008, lv=12)
