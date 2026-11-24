# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 11): muestreo aleatorio, tipos de muestreo, sesgo y variabilidad muestral."""
import random
import mx_pm1 as S
from mx_common import src, unit, nomoney

S.setup(random.Random(100111))
mue, dis = src("gen_es_matematicas_2ccss_muestreo_y_distribucion_de_medias", 100311, "s_muestreo", "s_distribucion", extra=(nomoney,))
unit("muestreo", 11, ("Estadística", 11, "Muestreo y variabilidad muestral"),
     "Explica la importancia del muestreo aleatorio para obtener muestras representativas, reconoce tipos de muestreo y sesgos, y describe la variabilidad muestral",
     "Muestreo y variabilidad muestral", "Muestreo",
     "Ejercicios de Pensamiento Matemático I: población y muestra, muestreo aleatorio simple, sistemático, estratificado y por conglomerados, sesgo y variabilidad muestral. 100 ejercicios con respuestas.",
     "Al azar, la muestra representa", "Cada muestra da un resultado un poco distinto.",
     ["Una <b>muestra</b> es una parte de la población. Si se elige <b>al azar</b>, representa mejor a todos y evita el sesgo.",
      "Tipos: <b>aleatorio simple</b> (sorteo), <b>sistemático</b> (uno de cada k), <b>estratificado</b> (al azar dentro de cada grupo) y <b>por conglomerados</b> (grupos completos al azar).",
      "Cada muestra da un resultado algo distinto: es la <b>variabilidad muestral</b>. Con muestras más grandes, varía menos."],
     [("1 200 alumnos: 600, 400 y 200 por semestre; muestra de 60", ["60 ÷ 1 200 = 1 de cada 20", "600 ÷ 20, 400 ÷ 20, 200 ÷ 20"], "30, 20 y 10")],
     [["Encuestar solo a quien es fácil", "Eso produce una muestra sesgada."], ["Creer que una muestra grande no tiene sesgo", "Si no es aleatoria, sigue sesgada."], ["Esperar que dos muestras den lo mismo", "La variabilidad muestral es normal."]],
     [("¿Qué tamaño debe tener una muestra?", "Depende del error que se acepte; más grande da estimaciones más precisas, pero lo más importante es que sea aleatoria."),
      ("¿Qué es un sesgo?", "Un error sistemático: la muestra favorece a un tipo de personas y el resultado se aleja de la realidad.")],
     [("Población y muestra", [(mue, 10), (lambda: S.p11("var"), 5), (lambda: S.p11("tam"), 5)]), ("Tipos de muestreo", [(lambda: S.p11("tipo"), 7), (lambda: S.p11("sesgo"), 5), (lambda: S.p11("tam"), 8)]),
      ("Muestreo estratificado", [(lambda: S.p11("est"), 20)]), ("Variabilidad muestral", [(dis, 20)]),
      ("Repaso", [(lambda: S.p11("est"), 8), (lambda: S.p11("tam"), 8), (mue, 4)])],
     100011, lv=10)
