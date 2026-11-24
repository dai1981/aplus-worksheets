# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Leer, interpretar y comunicar información de distintas gráficas."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69117))
interp = src("gen_es_matematicas_1eso_coordenadas_y_graficas", 69411, "s_interpretar", lv=1)
graf = src("gen_es_matematicas_6_estadistica", 69412, "s4_graficos", lv=6)
unit("interpretacion-de-graficas", 17, "6OR",
     "Lee, interpreta y comunica información mediante cualquier tipo de gráfica",
     "Interpretación de gráficas", "Interpretación de gráficas",
     "Ejercicios de matemáticas de 3.er grado de secundaria: interpretar gráficas de línea, de barras, circulares, histogramas y gráficas de distancia y tiempo. 100 ejercicios con respuestas.",
     "Lee el título, los ejes y la escala", "Antes de mirar los datos.",
     ["Antes de responder, lee el <b>título</b>, qué representa cada <b>eje</b> y la <b>escala</b> (cuánto vale cada división).",
      "En una gráfica de distancia y tiempo, un tramo horizontal es una pausa y un tramo más empinado indica mayor velocidad.",
      "Elige la gráfica según el mensaje: línea para cambios en el tiempo, barras para comparar, circular para partes de un todo, histograma para datos agrupados."],
     [("Tramo horizontal de 10 a 25 min", ["no cambia la distancia"], "estuvo detenido 15 min"), ("Barra a 4 líneas, cada una vale 5", ["4 × 5"], "20")],
     [["No mirar la escala", "Cada línea puede valer 2, 5 o 10."], ["Confundir valor con cambio", "Subir más no es lo mismo que estar más alto."], ["Sacar conclusiones con pocos datos", "Una gráfica muestra lo que se midió, no todo."]],
     [("¿Una gráfica puede engañar?", "Sí: si el eje no empieza en 0 o la escala cambia, las diferencias parecen más grandes."), ("¿Qué gráfica uso para porcentajes?", "La circular, si las partes forman un total.")],
     [("Gráficas de distancia y tiempo", [(interp, 20)]), ("Gráficas de línea", [(S.graf_linea, 20)]), ("Gráficas de barras y circulares", [(graf, 20)]), ("Histogramas", [(S.histograma, 20)]),
      ("Repaso", [(S.graf_linea, 7), (S.histograma, 7), (graf, 6)])],
     69017, lv=9)
