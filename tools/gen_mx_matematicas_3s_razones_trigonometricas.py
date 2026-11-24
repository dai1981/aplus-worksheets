# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Seno, coseno y tangente; resolver triángulos rectángulos."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69116))
TAN = [("tg ", "tan "), ("tg<", "tan<")]
raz, val, res, prob = src("gen_es_matematicas_4eso_trigonometria", 69401, "s_razones", "s_valores", "s_resolver", "s_problema", lv=4, rep=TAN, extra=(lambda it: not re.search(r"cuadrante|rad|π|sec|cosec|cotg|(?<!\d)(9[1-9]|[1-3]\d\d)°", it["q"] + " ".join(it["c"])),))
unit("razones-trigonometricas", 16, "6ME",
     "Resuelve problemas que impliquen el uso de las razones trigonométricas seno, coseno y tangente",
     "Razones trigonométricas: seno, coseno y tangente", "Razones trigonométricas",
     "Ejercicios de matemáticas de 3.er grado de secundaria: seno, coseno y tangente en triángulos rectángulos, ángulos de 30°, 45° y 60°, calcular lados y problemas de alturas. 100 ejercicios con respuestas.",
     "sen = op/hip   tan = op/ady", "cos = ady/hip, desde el ángulo elegido.",
     ["En un triángulo rectángulo, desde un ángulo agudo A: <b>sen A</b> = cateto opuesto ÷ hipotenusa, <b>cos A</b> = cateto adyacente ÷ hipotenusa, <b>tan A</b> = cateto opuesto ÷ cateto adyacente.",
      "Para calcular un lado, elige la razón que relaciona lo que conoces con lo que buscas y despeja. Usa la calculadora en modo grados.",
      "Valores clave: sen 30° = 1/2, cos 60° = 1/2, tan 45° = 1."],
     [("Hipotenusa 20, A = 30°: opuesto", ["sen 30° = x ÷ 20", "x = 20 × 0.5"], "10"), ("Sombra 12 m, ángulo 40°: altura", ["tan 40° = h ÷ 12", "h = 12 × 0.839"], "≈ 10.07 m")],
     [["Confundir opuesto y adyacente", "Dependen del ángulo que usas."], ["Calculadora en radianes", "Revisa que esté en grados (DEG)."], ["Usar la hipotenusa en la tangente", "La tangente usa los dos catetos."]],
     [("¿Para qué sirven?", "Para medir alturas y distancias que no se pueden medir directamente: edificios, montañas, rampas."), ("¿Por qué no dependen del tamaño del triángulo?", "Porque los triángulos rectángulos con el mismo ángulo son semejantes.")],
     [("Calcular razones", [(raz, 20)]), ("Valores notables y calculadora", [(val, 8), (lambda: S.trig_calc("val"), 12)]), ("Calcular lados", [(res, 20)]), ("Problemas", [(prob, 20)]), ("Ángulo a partir de la razón", [(lambda: S.trig_calc("ang"), 20)])],
     69016, lv=9)
