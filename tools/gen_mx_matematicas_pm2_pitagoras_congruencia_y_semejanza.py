# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 10): teorema de Pitágoras, congruencia, semejanza y cuadriláteros cíclicos (problema del triángulo de Napoleón)."""
import random
import mx_pm2 as S
from mx_common import src, unit, nomoney

S.setup(random.Random(110110))
hip, cat, rec, fig_, pro = src("gen_es_matematicas_2eso_teorema_de_pitagoras", 110310, "s_hip", "s_cateto", "s_rect", "s_figuras", "s_problema")
raz, tal, cri = src("gen_es_matematicas_2eso_semejanza", 110320, "s_razon", "s_tales", "s_criterios", lv=2, extra=(nomoney,))
unit("pitagoras-congruencia-y-semejanza", 10, ("Geometría", 10, "Pitágoras, congruencia y semejanza"),
     "Aplica el teorema de Pitágoras, los criterios de congruencia y semejanza de triángulos y las propiedades de los cuadriláteros cíclicos en problemas como el del triángulo de Napoleón",
     "Pitágoras, congruencia y semejanza", "Pitágoras y semejanza",
     "Ejercicios de Pensamiento Matemático II: teorema de Pitágoras y su recíproco, triángulos equiláteros, semejanza, teorema de Tales y cuadriláteros cíclicos. 100 ejercicios con respuestas.",
     "a² + b² = c²", "Semejantes: lados proporcionales.",
     ["<b>Pitágoras</b>: en un triángulo rectángulo, a² + b² = c² (c es la hipotenusa). Si a² + b² = c², el triángulo es rectángulo (recíproco).",
      "Dos triángulos son <b>semejantes</b> si tienen ángulos iguales y lados proporcionales; son <b>congruentes</b> si además son del mismo tamaño (criterios LLL, LAL, ALA).",
      "En un <b>cuadrilátero cíclico</b> (inscrito en una circunferencia) los ángulos opuestos suman 180°. El triángulo de Napoleón usa todo esto."],
     [("Catetos 9 y 12", ["9² + 12² = 81 + 144 = 225", "√225"], "15"), ("Cuadrilátero cíclico con ∠A = 70°", ["∠C = 180° − 70°"], "110°")],
     [["Sumar los lados sin elevar al cuadrado", "Primero cuadrados, luego raíz."], ["Usar Pitágoras en triángulos no rectángulos", "Solo vale con un ángulo de 90°."], ["Comparar lados que no se corresponden", "Ordena los lados de menor a mayor."]],
     [("¿Qué dice el teorema de Napoleón?", "Si sobre los lados de cualquier triángulo se construyen triángulos equiláteros hacia afuera, sus centros forman otro triángulo equilátero."),
      ("¿Cuándo un cuadrilátero es cíclico?", "Cuando sus ángulos opuestos suman 180°, como en todos los rectángulos.")],
     [("Hipotenusa y catetos", [(hip, 10), (cat, 10)]), ("¿Es rectángulo? y figuras", [(rec, 10), (fig_, 6), (lambda: S.lp10("equi"), 4)]), ("Triángulos equiláteros y problemas", [(lambda: S.lp10("equi"), 10), (pro, 10)]),
      ("Semejanza y Tales", [(raz, 8), (tal, 8), (cri, 4)]), ("Cuadriláteros cíclicos", [(lambda: S.lp10("ciclico"), 10), (lambda: S.lp10("es_ciclico"), 6), (lambda: S.lp10("angulos"), 4)])],
     110010, lv=11)
