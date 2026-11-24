# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 6): problemas estadísticos, fuentes de datos y tipos de variables."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100106))
var = src("gen_es_matematicas_1eso_estadistica", 100306, "s_variable", lv=4)
unit("tipos-de-variables", 6, ("Estadística", 6, "Fuentes de datos y tipos de variables"),
     "Plantea un problema estadístico, obtiene datos de fuentes confiables y clasifica las variables en cualitativas (nominales u ordinales) y cuantitativas (discretas o continuas)",
     "Tipos de variables y fuentes de datos", "Tipos de variables",
     "Ejercicios de Pensamiento Matemático I: población, muestra y variable, variables cualitativas nominales y ordinales, cuantitativas discretas y continuas, y fuentes de datos confiables. 100 ejercicios con respuestas.",
     "¿Se cuenta, se mide o se nombra?", "Discreta se cuenta; continua se mide.",
     ["<b>Cualitativa</b>: el dato es una categoría. <b>Nominal</b> si no tiene orden (color), <b>ordinal</b> si sí (talla CH, M, G).",
      "<b>Cuantitativa</b>: el dato es un número. <b>Discreta</b> si se cuenta (hermanos), <b>continua</b> si se mide (estatura).",
      "Busca datos en fuentes <b>confiables</b>: oficiales (INEGI, Banco de México) o que expliquen cómo los obtuvieron."],
     [("Número de mascotas", ["Se cuenta: 0, 1, 2…"], "cuantitativa discreta"), ("Nivel de satisfacción: bueno, regular, malo", ["Categorías con orden"], "cualitativa ordinal")],
     [["Pensar que un número siempre es cuantitativo", "Un código postal es una etiqueta: cualitativa."], ["Confundir discreta con continua", "¿Se cuenta o se mide?"], ["Usar redes sociales como fuente", "Verifica el origen de los datos."]],
     [("¿Un código postal es cuantitativo?", "No: es una etiqueta, no tiene sentido sumarlo ni promediarlo. Es cualitativa nominal."),
      ("¿Qué datos ofrece el INEGI?", "Censos de población, encuestas de hogares, empleo, precios y muchos otros datos oficiales de México.")],
     [("Clasificar variables", [(lambda: S.p6("tipo"), 20)]), ("Clasificar con datos", [(lambda: S.p6("cual"), 20)]), ("Más variables", [(var, 8), (lambda: S.p6("cual"), 12)]),
      ("Población, muestra y variable", [(lambda: S.p6("pobl"), 12), (lambda: S.p6("cual"), 8)]), ("Fuentes de datos", [(lambda: S.p6("fuente"), 10), (lambda: S.p6("cual"), 10)])],
     100006, lv=10)
