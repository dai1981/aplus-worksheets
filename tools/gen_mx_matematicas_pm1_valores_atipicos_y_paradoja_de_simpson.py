# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 10): lectura crítica de estadísticas, valores atípicos, variables de confusión y paradoja de Simpson."""
import random
import mx_pm1 as S
from mx_common import unit

S.setup(random.Random(100110))
unit("valores-atipicos-y-paradoja-de-simpson", 10, ("Estadística", 10, "Lectura crítica: atípicos y paradoja de Simpson"),
     "Cuestiona afirmaciones basadas en datos considerando valores atípicos, variables de confusión y la paradoja de Simpson",
     "Valores atípicos y paradoja de Simpson", "Atípicos y paradoja de Simpson",
     "Ejercicios de Pensamiento Matemático I: detectar valores atípicos, su efecto en la media, regla de 1.5 × RIC, variables de confusión y paradoja de Simpson. 100 ejercicios con respuestas.",
     "Un atípico mueve la media", "Revisa grupos y terceras variables.",
     ["Un <b>valor atípico</b> está muy lejos de los demás. Cambia mucho la media y el rango, pero poco la mediana.",
      "Regla: es atípico si es mayor que Q₃ + 1.5 × RIC o menor que Q₁ − 1.5 × RIC (RIC = Q₃ − Q₁).",
      "Una <b>variable de confusión</b> afecta a las dos variables. En la <b>paradoja de Simpson</b>, una tendencia de cada grupo se invierte al juntar los grupos."],
     [("Datos 12, 14, 15, 16, 18 y se agrega 95", ["Media sin 95: 15", "Media con 95: 170 ÷ 6 ≈ 28.3"], "la media casi se duplica")],
     [["Borrar un atípico sin revisar", "Puede ser un dato real importante."], ["Usar la media con atípicos", "La mediana representa mejor."], ["Juntar grupos distintos sin cuidado", "Compara también dentro de cada grupo."]],
     [("¿Por qué ocurre la paradoja de Simpson?", "Porque los grupos tienen tamaños muy distintos y una variable oculta (como la gravedad del caso) influye en el resultado."),
      ("¿Siempre hay que quitar los atípicos?", "No. Primero hay que saber si son errores o casos reales; un caso real puede ser la información más importante.")],
     [("Detectar atípicos", [(lambda: S.p10("cual"), 20)]), ("Efecto en la media", [(lambda: S.p10("media"), 15), (lambda: S.p10("robusta"), 5)]),
      ("Regla de 1.5 × RIC", [(lambda: S.p10("iqr"), 20)]), ("Variables de confusión", [(lambda: S.p10("confusion"), 6), (lambda: S.p10("iqr"), 6), (lambda: S.p10("simpson"), 8)]),
      ("Paradoja de Simpson", [(lambda: S.p10("simpson"), 20)])],
     100010, lv=10)
