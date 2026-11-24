# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Múltiplos y submúltiplos del metro, litro y kilogramo; sistema inglés."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67118))
cam, comp, prob = src("gen_es_matematicas_6_medidas", 67471, "s1_cambio", "s3_comparar", "s5_problema", lv=6, extra=(nomoney,))

unit("conversion-de-unidades", 18, "6ME",
     "Resuelve problemas que implican conversiones entre múltiplos y submúltiplos del metro, litro y kilogramo, y entre unidades del sistema inglés (yarda, pulgada, galón, onza y libra)",
     "Conversión de unidades: métrico e inglés", "Conversión de unidades",
     "Ejercicios de matemáticas de 1.er grado de secundaria: múltiplos y submúltiplos del metro, el litro y el kilogramo, y conversiones con yardas, pulgadas, galones, onzas y libras. 100 ejercicios con respuestas.",
     "Unidad mayor a menor: multiplica", "1 pulgada = 2.54 cm; 1 galón = 3.785 L",
     ["En el sistema métrico cada unidad es 10 veces la siguiente: km, hm, dam, <b>m</b>, dm, cm, mm (igual con litros y gramos). Para pasar a una unidad <b>menor</b>, multiplica; a una <b>mayor</b>, divide.",
      "<b>Sistema inglés</b>: 1 pulgada = 2.54 cm, 1 yarda = 0.9144 m (36 pulgadas), 1 galón = 3.785 L, 1 libra = 0.4536 kg (16 onzas), 1 onza = 28.35 g.",
      "Para convertir, multiplica por la equivalencia; para volver, divide."],
     [("3.5 km a m", ["× 1 000"], "3 500 m"), ("5 galones a litros", ["5 × 3.785"], "18.925 L"), ("12 pulgadas a cm", ["12 × 2.54"], "30.48 cm")],
     [["Dividir cuando hay que multiplicar", "De unidad mayor a menor, el número crece."], ["Mover mal el punto", "1 hm = 100 m, no 10 m."], ["Mezclar unidades al comparar", "Pasa las dos cantidades a la misma unidad."]],
     [("¿Dónde se usa el sistema inglés en México?", "En pantallas y tubos (pulgadas), en el futbol americano (yardas), en algunos garrafones (galones) y en recetas o productos importados (onzas y libras)."),
      ("¿Cuántos mililitros tiene un litro?", "1 000 mL.")],
     [("Metro, litro y kilogramo", [(cam, 20)]), ("Comparar medidas", [(comp, 20)]), ("Del sistema inglés al métrico", [(lambda: S.ingles("a_metrico", "a_ingles"), 20)]), ("Equivalencias y comparaciones", [(lambda: S.ingles("interno", "comparar"), 20)]), ("Problemas", [(prob, 10), (S.ingles, 10)])],
     67018, lv=7)
