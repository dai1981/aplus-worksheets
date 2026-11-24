# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Desigualdades lineales con una incógnita."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68107))
unit("desigualdades", 7, "6EC",
     "Resuelve desigualdades con expresiones algebraicas",
     "Desigualdades lineales", "Desigualdades",
     "Ejercicios de matemáticas de 2.º grado de secundaria: resolver desigualdades lineales, invertir el signo al multiplicar o dividir entre un negativo, comprobar valores y problemas. 100 ejercicios con respuestas.",
     "Entre negativo: el signo se invierte", "−2x &gt; 6 → x &lt; −3",
     ["Una <b>desigualdad</b> usa &lt;, &gt;, ≤ o ≥. Su solución no es un solo número sino un conjunto: x &gt; 4 significa todos los números mayores que 4.",
      "Se resuelve como una ecuación: sumas, restas, multiplicas o divides en los dos lados.",
      "Pero si <b>multiplicas o divides entre un número negativo</b>, el signo de la desigualdad se invierte: −3x ≤ 12 → x ≥ −4."],
     [("2x + 5 &gt; 17", ["2x &gt; 12"], "x &gt; 6"), ("−4x + 1 ≤ 9", ["−4x ≤ 8", "÷ (−4), se invierte"], "x ≥ −2")],
     [["No invertir el signo con un negativo", "−x &gt; 3 es x &lt; −3."], ["Invertir el signo al restar", "Solo se invierte al multiplicar o dividir entre negativos."], ["Dar un solo número", "La solución es un conjunto de valores."]],
     [("¿Cómo compruebo mi respuesta?", "Prueba un número de la solución y otro fuera de ella en la desigualdad original."), ("¿Qué diferencia hay entre &lt; y ≤?", "Con ≤ el número del límite también es solución.")],
     [("Resolver desigualdades", [(lambda: S.desig("res"), 20)]), ("Con coeficiente negativo", [(lambda: S.desig("neg"), 20)]), ("¿Qué valores cumplen?", [(lambda: S.desig("check"), 20)]),
      ("Repaso", [(lambda: S.desig("res", "neg"), 20)]), ("Problemas", [(lambda: S.desig("prob"), 20)])],
     68007, lv=8)
