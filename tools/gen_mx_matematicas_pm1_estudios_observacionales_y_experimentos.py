# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 12): estudios observacionales y experimentos, grupo control, aleatorización y causalidad."""
import random
import mx_pm1 as S
from mx_common import unit

S.setup(random.Random(100112))
unit("estudios-observacionales-y-experimentos", 12, ("Estadística", 12, "Estudios observacionales y experimentos"),
     "Distingue estudios observacionales de experimentos, reconoce el papel del grupo control y de la asignación aleatoria, y valora qué conclusiones permite cada diseño",
     "Estudios observacionales y experimentos", "Observación y experimento",
     "Ejercicios de Pensamiento Matemático I: estudio observacional o experimento, grupo control, placebo, asignación aleatoria y cuándo se puede concluir causa y efecto. 100 ejercicios con respuestas.",
     "Al azar se puede hablar de causa", "Observar solo muestra asociación.",
     ["En un <b>estudio observacional</b> solo se registra lo que las personas ya hacen. En un <b>experimento</b> el investigador asigna el tratamiento.",
      "El <b>grupo control</b> no recibe el tratamiento (o recibe un placebo) y sirve para comparar.",
      "Si los grupos se forman <b>al azar</b>, las demás variables se reparten por igual: así se puede concluir causa y efecto."],
     [("Se pregunta a 200 personas si toman café y se mide su presión", ["No se asigna nada"], "estudio observacional")],
     [["Llamar experimento a una encuesta", "Si no se asigna el tratamiento, es observacional."], ["Concluir causa en un estudio observacional", "Puede haber variables de confusión."], ["Dejar que cada persona elija su grupo", "Los grupos deben formarse al azar."]],
     [("¿Qué es un placebo?", "Un tratamiento sin efecto que parece real; ayuda a separar el efecto real del efecto de creer que te tratan."),
      ("¿Por qué no siempre se hacen experimentos?", "A veces no es ético o no es posible, por ejemplo obligar a alguien a fumar.")],
     [("¿Observacional o experimento?", [(lambda: S.p12("tipo"), 20)]), ("Grupo control", [(lambda: S.p12("control"), 20)]),
      ("¿Se puede concluir causa?", [(lambda: S.p12("causa"), 12), (lambda: S.p12("tipo"), 8)]), ("Diseño de estudios", [(lambda: S.p12("concepto"), 6), (lambda: S.p12("control"), 14)]),
      ("Repaso", [(lambda: S.p12("tipo"), 20)])],
     100012, lv=10)
