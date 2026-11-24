# -*- coding: utf-8 -*-
"""México 1.er grado (días, semanas y meses) y 2.º grado (calendario): ayer, hoy y mañana, días de la semana, meses y leer un calendario (Medición del tiempo). Preguntas propias y España 1.º/2.º (gen_es_matematicas_2_el_reloj, sin leer relojes) con otra semilla."""
import random
from mx_common import src, unit
from mx_12 import BIG, s_calendario, s_ayer, calendario_svg

T = {1: dict(slug="dias-semanas-y-meses", sort=11, std="Identifica y usa las nociones de ayer, hoy y mañana, los días de la semana y los meses del año; ubica fechas y actividades en un calendario",
             title="Días de la semana y meses del año", short="Días, semanas y meses",
             meta="Ejercicios de matemáticas de 1.er grado de primaria: ayer, hoy y mañana, los días de la semana, mañana, tarde y noche y el calendario. 100 ejercicios con respuestas.",
             kb="La semana tiene 7 días", ks="Después del domingo vuelve el lunes.",
             think=["La semana tiene <b>7 días</b>: domingo, lunes, martes, miércoles, jueves, viernes y sábado.",
                    "<b>Ayer</b> es el día de antes, <b>hoy</b> es este día y <b>mañana</b> es el día de después.",
                    "En el <b>calendario</b>, cada columna es un día de la semana y cada número es una fecha."],
             ex=[("Hoy es martes", ["Ayer: lunes", "Mañana: miércoles"], "ayer lunes, mañana miércoles")],
             mist=[["Confundir ayer y mañana", "Ayer ya pasó; mañana todavía no llega."], ["Saltarse un día", "Di los días en orden."], ["Olvidar que la semana vuelve a empezar", "Después del sábado viene el domingo."]],
             faq=[("¿Cuántos días tiene una semana?", "Siete: domingo, lunes, martes, miércoles, jueves, viernes y sábado."), ("¿Qué es antier?", "El día antes de ayer.")]),
     2: dict(slug="calendario", sort=12, std="Lee y usa el calendario para ubicar meses, semanas y días; reconoce que el año tiene 12 meses y calcula fechas a partir de una fecha dada",
             title="El calendario: días, semanas y meses", short="Calendario",
             meta="Ejercicios de matemáticas de 2.º grado de primaria: leer un calendario, días de la semana, meses del año y qué fecha será dentro de una semana. 100 ejercicios con respuestas.",
             kb="Una semana después: suma 7", ks="Es el mismo día de la semana.",
             think=["En el calendario, cada <b>columna</b> es un día de la semana. Busca la fecha y sube a la fila de arriba.",
                    "Una semana tiene 7 días: dentro de una semana, la fecha aumenta 7 y el día de la semana es el mismo.",
                    "El año tiene <b>12 meses</b>. Unos tienen 30 días, otros 31 y febrero 28 (o 29)."],
             ex=[("Hoy es lunes 5", ["5 + 7 = 12"], "el lunes 12")],
             mist=[["Sumar 1 en vez de 7 para «una semana»", "Una semana son 7 días."], ["Leer la fila en vez de la columna", "El día de la semana está arriba de la columna."], ["Pensar que todos los meses tienen 30 días", "Mira el último número del mes."]],
             faq=[("¿Cuántos meses tiene un año?", "Doce, de enero a diciembre."), ("¿Qué mes tiene menos días?", "Febrero: 28 días, y 29 en los años bisiestos.")])}


def build(lv):
    t = T[lv]
    dias, momento = src("gen_es_matematicas_2_el_reloj", 61000 + 1000 * lv + 921, "dias", "momento", lv=lv, mx_=BIG)
    cal = s_calendario(random.Random(61000 + 1000 * lv + 922), lv)
    ay = s_ayer(random.Random(61000 + 1000 * lv + 923))
    if lv == 1:
        spec = [("Ayer, hoy y mañana", [(ay, 20)]), ("Los días de la semana", [(dias, 14), (cal, 6)]), ("Momentos del día", [(momento, 8), (ay, 6), (cal, 6)]), ("El calendario", [(cal, 20)]), ("Fechas en el calendario", [(cal, 20)])]
    else:
        spec = [("Días de la semana", [(ay, 10), (dias, 10)]), ("Días y meses", [(dias, 20)]), ("Leer el calendario", [(cal, 20)]), ("Fechas", [(cal, 20)]), ("Repaso", [(cal, 8), (dias, 6), (momento, 6)])]
    unit(t["slug"], t["sort"], "T", t["std"], t["title"], t["short"], t["meta"], t["kb"], t["ks"], t["think"], t["ex"], t["mist"], t["faq"], spec, 60000 + 1000 * lv + 11,
         pic=calendario_svg(4, 3, [15]), lv=lv)


if __name__ == "__main__":
    build(1)
