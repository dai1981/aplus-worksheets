# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 12): funciones exponenciales y logarítmicas: gráficas, bases y relación de inversas."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120112))
ldef, lpro, lecu = src("gen_es_matematicas_1bach_numeros_reales_y_logaritmos", 120312, "s_log_def", "s_log_prop", "s_ecuaciones")
cre = src("gen_es_matematicas_1ccss_numeros_reales_y_logaritmos", 120322, "s_crecimiento")
unit("funciones-exponenciales-y-logaritmicas", 12, ("Funciones trascendentes", 12, "Funciones exponenciales y logarítmicas"),
     "Representa funciones exponenciales y logarítmicas de distintas bases, reconoce que son inversas y las usa para modelar crecimiento y decaimiento",
     "Exponenciales y logaritmos", "Exponenciales y logaritmos",
     "Ejercicios de Pensamiento Matemático III: gráficas de bˣ y log x, función inversa, logaritmos y sus propiedades, ecuaciones exponenciales y modelos de crecimiento. 100 ejercicios con respuestas.",
     "log_b x = y ⇔ bʸ = x", "Exponencial y logaritmo son inversas.",
     ["La <b>exponencial</b> f(x) = bˣ (b &gt; 0, b ≠ 1) pasa por (0, 1); crece si b &gt; 1 y decrece si 0 &lt; b &lt; 1. Su asíntota es y = 0.",
      "El <b>logaritmo</b> es su inversa: log<sub>b</sub> x = y significa bʸ = x. Pasa por (1, 0) y solo existe para x &gt; 0.",
      "Modelos: crecimiento P = P₀·bᵗ (bacterias, interés) y decaimiento (vida media)."],
     [("log₂ 32", ["2⁵ = 32"], "5"), ("Bacterias que se duplican cada 3 h, desde 100", ["P = 100 · 2^(t/3)", "t = 12: 100 · 2⁴"], "1 600")],
     [["Pensar que log(a + b) = log a + log b", "La propiedad es log(a · b)."], ["Calcular logaritmos de negativos", "No existen en los reales."], ["Confundir 2ˣ con x²", "En 2ˣ la variable está en el exponente."]],
     [("¿Qué es el número e?", "Una constante ≈ 2.718; la función eˣ es su propia derivada y aparece en el crecimiento continuo."), ("¿Para qué sirven los logaritmos?", "Para despejar exponentes y medir escalas muy amplias, como la de Richter o el pH.")],
     [("Logaritmos", [(lambda: S.q12("log"), 10), (ldef, 10)]), ("Gráficas e inversas", [(lambda: S.q12("grafica"), 7), (lambda: S.q12("inversa"), 13)]),
      ("Propiedades", [(lpro, 20)]), ("Ecuaciones", [(lambda: S.q12("ecuacion"), 10), (lecu, 10)]), ("Modelos", [(lambda: S.q12("modelo"), 12), (cre, 8)])],
     120012, lv=12)
