# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Ángulos de polígonos regulares, construcción con compás y teselados."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69109))
unit("poligonos-regulares-y-teselados", 9, "6CF",
     "Construye polígonos regulares con regla y compás a partir de sus ángulos y lados; usa las relaciones entre figuras en teselados",
     "Polígonos regulares y teselados", "Polígonos regulares",
     "Ejercicios de matemáticas de 3.er grado de secundaria: ángulos interiores, centrales y exteriores de polígonos regulares, construcción con compás y teselados. 100 ejercicios con respuestas.",
     "Interior = 180(n − 2) ÷ n", "Central y exterior = 360 ÷ n.",
     ["En un polígono regular de n lados, los ángulos interiores suman 180°(n − 2) y cada uno mide 180°(n − 2) ÷ n.",
      "El <b>ángulo central</b> mide 360° ÷ n. Para construir el polígono, se traza una circunferencia, se marcan ángulos centrales iguales y se unen los puntos.",
      "Un <b>teselado</b> cubre el plano sin huecos ni encimarse: los ángulos que se juntan en un vértice suman 360°. Solo triángulos, cuadrados y hexágonos regulares lo logran solos."],
     [("Hexágono regular", ["180 × 4 = 720", "720 ÷ 6"], "120° cada interior"), ("Octágono: ángulo central", ["360 ÷ 8"], "45°")],
     [["Usar 180° × n", "La suma es 180° × (n − 2)."], ["Confundir central e interior", "En el hexágono, central 60° e interior 120°."], ["Creer que el pentágono tesela", "108° no divide a 360°."]],
     [("¿Por qué el hexágono tesela?", "Porque 3 × 120° = 360°."), ("¿Qué es un teselado semirregular?", "Uno con dos o más polígonos regulares distintos, como octágonos y cuadrados.")],
     [("Suma de ángulos y diagonales", [(lambda: S.poligonos("suma", "diag"), 20)]), ("Ángulo interior", [(lambda: S.poligonos("int", "lados"), 14), (lambda: S.poligonos("perim"), 6)]), ("Ángulo central y exterior", [(lambda: S.poligonos("cen", "ext"), 20)]), ("Construir con compás", [(lambda: S.poligonos("const"), 8), (lambda: S.poligonos("suma", "diag"), 12)]),
      ("Teselados y perímetro", [(lambda: S.poligonos("tesel"), 6), (lambda: S.poligonos("perim"), 14)])],
     69009, lv=9)
