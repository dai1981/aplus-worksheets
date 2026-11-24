# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 2): recíproco de Pitágoras, ley de senos, ley de cosenos y círculo unitario."""
import random
from mx_common import src, unit

sen, cos_, are, pro = src("gen_es_matematicas_1bach_resolucion_de_triangulos", 130302, "s_seno", "s_coseno", "s_area", "s_problema",
                          rep=[("teorema del seno", "ley de senos"), ("teorema del coseno", "ley de cosenos"), ("Teorema del seno", "Ley de senos"), ("Teorema del coseno", "Ley de cosenos")])
cua = src("gen_es_matematicas_1bach_trigonometria", 130312, "s_cualquier")
rec = src("gen_es_matematicas_2eso_teorema_de_pitagoras", 130322, "s_rect")
unit("leyes-de-senos-y-cosenos", 2, ("Geometría y trigonometría", 2, "Leyes de senos y cosenos"),
     "Usa el recíproco del teorema de Pitágoras, la ley de senos, la ley de cosenos y el círculo unitario para resolver triángulos cualesquiera",
     "Ley de senos, ley de cosenos y círculo unitario", "Leyes de senos y cosenos",
     "Ejercicios de Temas Selectos de Matemáticas I: recíproco de Pitágoras, ley de senos, ley de cosenos, área de un triángulo y razones de cualquier ángulo en el círculo unitario. 100 ejercicios con respuestas.",
     "a/sen A = b/sen B = c/sen C", "c² = a² + b² − 2ab cos C",
     ["<b>Ley de senos</b>: a/sen A = b/sen B = c/sen C. Sirve si conoces un lado y su ángulo opuesto.",
      "<b>Ley de cosenos</b>: c² = a² + b² − 2ab cos C. Sirve con dos lados y el ángulo entre ellos, o con los tres lados. Si C = 90°, es Pitágoras.",
      "En el <b>círculo unitario</b>, el punto de ángulo θ es (cos θ, sen θ); así se definen las razones de cualquier ángulo."],
     [("a = 7, b = 9, C = 60°", ["c² = 49 + 81 − 2 × 7 × 9 × 0.5", "c² = 67"], "c ≈ 8.19")],
     [["Usar la ley de senos con dos lados y el ángulo entre ellos", "Ahí se usa la ley de cosenos."], ["Olvidar el signo del coseno en ángulos obtusos", "cos 120° = −0.5."], ["Emparejar lado y ángulo no opuestos", "Cada lado va con su ángulo opuesto."]],
     [("¿Para qué se usan en la vida real?", "En topografía, navegación y GPS: para calcular distancias que no se pueden medir directamente."), ("¿Qué es el caso ambiguo?", "Con dos lados y un ángulo no comprendido puede haber dos triángulos distintos.")],
     [("Recíproco de Pitágoras", [(rec, 20)]), ("Ley de senos", [(sen, 20)]), ("Ley de cosenos", [(cos_, 20)]), ("Círculo unitario", [(cua, 20)]),
      ("Áreas y problemas", [(are, 10), (pro, 10)])],
     130002, lv=13)
