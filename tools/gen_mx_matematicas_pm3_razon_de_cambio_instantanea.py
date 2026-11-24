# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 9): la derivada como razón de cambio instantánea: velocidad, aceleración, costo marginal."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120109))
mar = src("gen_es_matematicas_1ccss_derivadas", 120309, "s_marginal")
unit("razon-de-cambio-instantanea", 9, ("Derivadas", 9, "La derivada como razón de cambio"),
     "Interpreta la derivada como razón de cambio instantánea en situaciones de movimiento, economía, geometría y crecimiento de poblaciones",
     "Velocidad, aceleración y costo marginal", "Razón de cambio",
     "Ejercicios de Pensamiento Matemático III: velocidad y aceleración a partir de la posición, costo e ingreso marginal, cambio del área y ritmo de crecimiento. 100 ejercicios con respuestas.",
     "v(t) = s′(t);  a(t) = v′(t)", "Costo marginal = C′(q).",
     ["La derivada mide qué tan rápido cambia una cantidad en un instante.",
      "Si s(t) es la posición, <b>v(t) = s′(t)</b> es la velocidad y <b>a(t) = v′(t)</b> la aceleración.",
      "En economía, el <b>costo marginal</b> C′(q) es, aproximadamente, lo que cuesta producir una pieza más."],
     [("s(t) = −4.9t² + 20t + 2", ["v(t) = −9.8t + 20", "v(1) = 10.2"], "10.2 m/s; a = −9.8 m/s²")],
     [["Usar s(t) como velocidad", "La velocidad es la derivada de la posición."], ["Olvidar las unidades", "m/s para velocidad, m/s² para aceleración."], ["Confundir costo total con marginal", "El marginal es la derivada."]],
     [("¿Por qué la aceleración en caída libre es −9.8 m/s²?", "Porque la gravedad cambia la velocidad 9.8 m/s cada segundo, hacia abajo."), ("¿Qué indica una derivada negativa?", "Que la cantidad está disminuyendo en ese instante.")],
     [("Velocidad", [(lambda: S.q9("vel"), 20)]), ("Aceleración", [(lambda: S.q9("acel"), 10), (lambda: S.q9("vel"), 10)]), ("Costo marginal", [(lambda: S.q9("costo"), 10), (mar, 10)]),
      ("Geometría y crecimiento", [(lambda: S.q9("area"), 10), (lambda: S.q9("poblacion"), 10)]), ("Repaso", [(mar, 8), (lambda: S.q9("poblacion"), 6), (lambda: S.q9("costo"), 6)])],
     120009, lv=12)
