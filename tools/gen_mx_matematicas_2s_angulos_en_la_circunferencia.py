# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Ángulos centrales, inscritos y arcos."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68114))
unit("angulos-en-la-circunferencia", 14, "6CC",
     "Investiga figuras y propiedades relacionadas con el círculo; determina la medida de ángulos inscritos, centrales y de arcos",
     "Ángulos centrales, inscritos y arcos", "Ángulos en la circunferencia",
     "Ejercicios de matemáticas de 2.º grado de secundaria: ángulo central, ángulo inscrito, medida de arcos y relaciones entre ellos. 100 ejercicios con respuestas.",
     "Inscrito = mitad del central", "Si abarcan el mismo arco.",
     ["El <b>ángulo central</b> tiene el vértice en el centro; mide lo mismo que el arco que abarca.",
      "El <b>ángulo inscrito</b> tiene el vértice sobre la circunferencia; mide la <b>mitad</b> del arco (o del central) que abarca.",
      "Un ángulo inscrito que abarca un diámetro mide 90°. Toda la circunferencia mide 360°."],
     [("Central de 110°", ["inscrito: 110 ÷ 2"], "55°"), ("Circunferencia en 8 arcos iguales", ["360 ÷ 8"], "45°")],
     [["Pensar que el inscrito y el central son iguales", "El inscrito es la mitad."], ["Usar 180° para toda la circunferencia", "Son 360°."], ["Confundir el arco con la cuerda", "El arco es la curva; se mide en grados."]],
     [("¿Por qué el inscrito es la mitad?", "Al trazar el radio al vértice se forman triángulos isósceles; sus ángulos muestran que el central es el doble."), ("¿Todos los inscritos que abarcan el mismo arco son iguales?", "Sí.")],
     [("En la figura", [(lambda: S.circ_ang("fig"), 20)]), ("Ángulos inscritos", [(lambda: S.circ_ang("ins", "semi"), 20)]), ("Ángulos centrales", [(lambda: S.circ_ang("cen", "arco"), 20)]),
      ("Arcos", [(lambda: S.circ_ang("suma", "arco"), 20)]), ("Repaso", [(S.circ_ang, 20)])],
     68014, lv=8)
