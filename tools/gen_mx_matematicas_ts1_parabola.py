# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 5): la parábola como sección cónica y en modelos cuadráticos."""
import random
import mx_tsm as S
from mx_common import src, unit

S.setup(random.Random(130105))
par = src("gen_es_matematicas_1bach_conicas", 130305, "s_parabola")
unit("parabola", 5, ("Cónicas", 5, "La parábola"),
     "Reconoce la parábola como sección cónica y lugar geométrico, determina vértice, foco, directriz y lado recto, y la usa en modelos cuadráticos",
     "Parábola: vértice, foco y directriz", "Parábola",
     "Ejercicios de Temas Selectos de Matemáticas I: ecuación ordinaria de la parábola, vértice, foco, directriz, lado recto, hacia dónde abre y antenas parabólicas. 100 ejercicios con respuestas.",
     "(x − h)² = 4p(y − k)", "Foco a p del vértice; directriz al otro lado.",
     ["La <b>parábola</b> es el conjunto de puntos que están a la misma distancia de un punto (<b>foco</b>) y de una recta (<b>directriz</b>).",
      "Forma ordinaria: (x − h)² = 4p(y − k) abre hacia arriba (p &gt; 0) o abajo; (y − k)² = 4p(x − h) abre a la derecha o a la izquierda. El vértice es (h, k).",
      "El foco está a p del vértice y la directriz a p del otro lado. El <b>lado recto</b> mide |4p|."],
     [("(x − 2)² = 12(y + 1)", ["Vértice (2, −1)", "4p = 12 → p = 3"], "foco (2, 2), directriz y = −4")],
     [["Confundir el signo de h y k", "(x − 2)² tiene h = 2; (x + 2)², h = −2."], ["Tomar 4p como p", "Divide entre 4."], ["Poner la directriz del lado del foco", "Va del lado contrario."]],
     [("¿Por qué las antenas son parabólicas?", "Porque toda señal que llega paralela al eje se refleja hacia el foco, donde está el receptor."), ("¿Qué es una sección cónica?", "La curva que resulta al cortar un cono con un plano: circunferencia, elipse, parábola o hipérbola.")],
     [("Vértice", [(lambda: S.t5("vertice"), 10), (lambda: S.t5("abre"), 10)]), ("Foco", [(lambda: S.t5("foco"), 20)]), ("Directriz y lado recto", [(lambda: S.t5("directriz"), 12), (lambda: S.t5("lado"), 8)]),
      ("Más parábolas", [(par, 20)]), ("Modelos", [(lambda: S.t5("modelo"), 14), (lambda: S.t5("foco"), 6)])],
     130005, lv=13)
