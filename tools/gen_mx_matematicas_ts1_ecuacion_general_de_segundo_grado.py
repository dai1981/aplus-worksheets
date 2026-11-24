# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 8): ecuación general de segundo grado con dos variables e identificación de cónicas."""
import random
import mx_tsm as S
from mx_common import src, unit

S.setup(random.Random(130108))
rec, hip = src("gen_es_matematicas_1bach_conicas", 130308, "s_reconocer", "s_hiperbola", rep=[("Halla ", "Encuentra ")])
unit("ecuacion-general-de-segundo-grado", 8, ("Cónicas", 8, "Ecuación general de segundo grado"),
     "Identifica la cónica que representa la ecuación general Ax² + Bxy + Cy² + Dx + Ey + F = 0 por sus coeficientes y su discriminante B² − 4AC",
     "Ecuación general y tipos de cónicas", "Ecuación general de cónicas",
     "Ejercicios de Temas Selectos de Matemáticas I: reconocer circunferencias, elipses, parábolas e hipérbolas en la ecuación general, discriminante B² − 4AC e hipérbolas. 100 ejercicios con respuestas.",
     "B² − 4AC decide la cónica", "&lt; 0 elipse, = 0 parábola, &gt; 0 hipérbola",
     ["Toda cónica se escribe <b>Ax² + Bxy + Cy² + Dx + Ey + F = 0</b>.",
      "Sin término xy (B = 0): si A = C es circunferencia; si A y C tienen el mismo signo, elipse; si uno es 0, parábola; si tienen signos contrarios, hipérbola.",
      "En general se usa el <b>discriminante</b> B² − 4AC: negativo → elipse, cero → parábola, positivo → hipérbola."],
     [("4x² − 9y² + 8x − 36 = 0", ["A = 4, C = −9: signos contrarios"], "hipérbola")],
     [["Fijarse solo en D y E", "Los que deciden son A, B y C."], ["Decir parábola si A ≠ C", "Parábola: una de las dos variables no está al cuadrado."], ["Olvidar el término xy", "Si B ≠ 0, usa B² − 4AC."]],
     [("¿Qué hace el término Bxy?", "Gira la cónica; sin él, los ejes de la cónica son paralelos a los ejes x e y."), ("¿Puede la ecuación no tener gráfica?", "Sí, por ejemplo x² + y² + 1 = 0 no tiene puntos reales (cónica degenerada).")],
     [("Identificar la cónica", [(lambda: S.t8("tipo"), 20)]), ("Discriminante", [(lambda: S.t8("disc"), 20)]), ("Reconocer cónicas", [(rec, 20)]),
      ("Hipérbolas", [(hip, 20)]), ("Repaso", [(lambda: S.t8("tipo"), 10), (lambda: S.t8("disc"), 10)])],
     130008, lv=13)
