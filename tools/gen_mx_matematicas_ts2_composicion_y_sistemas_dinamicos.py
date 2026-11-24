# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas II (progresión 1): composición de funciones, iteración, recurrencias y sistemas dinámicos discretos."""
import random
import mx_tsm as S
from mx_common import src, unit

S.setup(random.Random(140101))
com = src("gen_es_matematicas_1bach_funciones", 140301, "s_composicion")
unit("composicion-y-sistemas-dinamicos", 1, ("Sucesiones y sistemas dinámicos", 1, "Composición de funciones y sistemas dinámicos discretos"),
     "Compone una función consigo misma para obtener sistemas dinámicos discretos: iteraciones, órbitas, puntos fijos, recurrencias y sensibilidad a las condiciones iniciales",
     "Iteración, órbitas y puntos fijos", "Sistemas dinámicos",
     "Ejercicios de Temas Selectos de Matemáticas II: composición de funciones, iterar f(f(x)), órbitas, puntos fijos, sucesiones recurrentes, modelo logístico y caos. 100 ejercicios con respuestas.",
     "xₙ₊₁ = f(xₙ)", "Un punto fijo cumple f(x) = x.",
     ["Un <b>sistema dinámico discreto</b> aplica la misma regla una y otra vez: x₁ = f(x₀), x₂ = f(x₁) = f(f(x₀)), …",
      "La sucesión de valores es la <b>órbita</b> de x₀. Un <b>punto fijo</b> cumple f(x) = x: si llegas a él, ya no cambias.",
      "Algunas reglas sencillas, como el modelo logístico xₙ₊₁ = r·xₙ(1 − xₙ), producen comportamientos caóticos: pequeñas diferencias iniciales crecen mucho."],
     [("f(x) = x/2 + 3, x₀ = 2", ["x₁ = 4, x₂ = 5, x₃ = 5.5", "Punto fijo: x = x/2 + 3 → x = 6"], "la órbita se acerca a 6")],
     [["Confundir f(f(x)) con f(x)²", "Componer es aplicar f al resultado."], ["Resolver f(x) = 0 para el punto fijo", "Es f(x) = x."], ["Creer que una regla sencilla siempre da algo predecible", "Puede producir caos."]],
     [("¿Qué es el efecto mariposa?", "La idea de que un cambio mínimo al inicio (el aleteo de una mariposa) puede cambiar mucho el resultado, como en el clima."), ("¿Dónde se usan?", "En poblaciones, economía, clima y en gráficos de fractales.")],
     [("Composición", [(com, 20)]), ("Iterar una función", [(lambda: S.u1("iter"), 20)]), ("Puntos fijos y órbitas", [(lambda: S.u1("fijo"), 12), (lambda: S.u1("orbita"), 8)]),
      ("Recurrencias", [(lambda: S.u1("rec"), 20)]), ("Modelo logístico y caos", [(lambda: S.u1("logistica"), 14), (lambda: S.u1("concepto"), 6)])],
     140001, lv=14)
