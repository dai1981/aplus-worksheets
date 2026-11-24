# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Histogramas, gráficas poligonales y de línea."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68116))
unit("histogramas-y-graficas-de-linea", 16, "6OR",
     "Recolecta, registra, lee y comunica información mediante histogramas, gráficas poligonales y de línea",
     "Histogramas y gráficas de línea", "Histogramas y gráficas de línea",
     "Ejercicios de matemáticas de 2.º grado de secundaria: leer e interpretar histogramas, polígonos de frecuencia y gráficas de línea; intervalos, totales, cambios y promedios. 100 ejercicios con respuestas.",
     "Histograma: datos en intervalos", "Gráfica de línea: cambios en el tiempo.",
     ["Un <b>histograma</b> agrupa datos numéricos en intervalos de la misma amplitud; la altura de cada barra es la frecuencia. Las barras van pegadas.",
      "Si unes los puntos medios de la parte de arriba de las barras obtienes un <b>polígono de frecuencias</b>.",
      "La <b>gráfica de línea</b> muestra cómo cambia una cantidad con el tiempo: los tramos que suben indican aumento y los que bajan, disminución."],
     [("Barras 3, 7, 5, 2", ["3 + 7 + 5 + 2"], "17 datos"), ("De 20 a 35 en un mes", ["35 − 20"], "aumento de 15")],
     [["Leer mal la escala", "Revisa cuánto vale cada línea del eje."], ["Contar el límite en dos intervalos", "Un dato de 60 va en «60 a 70», no en «50 a 60»."], ["Confundir el valor con el cambio", "El mayor aumento no es el mes con el valor más alto."]],
     [("¿Qué diferencia hay entre histograma y gráfica de barras?", "El histograma es para datos numéricos agrupados en intervalos y sus barras van juntas."), ("¿Cuándo uso una gráfica de línea?", "Para mostrar cambios a lo largo del tiempo.")],
     [("Leer gráficas de línea", [(lambda: S.graf_linea("lee", "max"), 20)]), ("Cambios en el tiempo", [(lambda: S.graf_linea("dif", "sube"), 20)]), ("Leer histogramas", [(lambda: S.histograma("clase", "tot"), 20)]),
      ("Intervalos", [(lambda: S.histograma("mas", "menos", "porc"), 20)]), ("Repaso", [(S.graf_linea, 10), (S.histograma, 10)])],
     68016, lv=8)
