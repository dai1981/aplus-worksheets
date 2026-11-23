# -*- coding: utf-8 -*-
"""México 4.º grado: Medición del tiempo (día, hora, minuto y segundo; duración; horarios y calendario). Reutiliza España 5.º/4.º con otra semilla."""
from mx_common import src, unit, hora_letra, mx_text
import es_common as ES

M = "gen_es_matematicas_5_medida_del_tiempo"
uni, compl, oper, cal = src(M, 64317, "s1_unidades", "s2_compleja", "s3_operar", "s5_calendario", mx_=99999)
dur, h24 = src("gen_es_matematicas_4_el_tiempo_y_el_reloj", 64218, "s4_duracion", "s2_24", mx_=99999, patch={"dicho": hora_letra})

unit("el-tiempo", 14, "T",
     "Usa el día, la hora, el minuto y el segundo para medir el tiempo; convierte unas unidades en otras; calcula la duración de actividades y usa el calendario, los años y los siglos",
     "El tiempo: horas, minutos y segundos", "El tiempo",
     "Ejercicios de matemáticas de 4.º grado de primaria: días, horas, minutos y segundos, convertir unidades de tiempo, duración de actividades, calendario y siglos. 100 ejercicios con respuestas.",
     "1 h = 60 min; 1 min = 60 s", "1 día = 24 horas; 1 semana = 7 días.",
     ["1 día = 24 horas; 1 hora = 60 minutos; 1 minuto = 60 <b>segundos</b>. Media hora son 30 minutos y un cuarto de hora, 15.",
      "Para pasar de horas a minutos, <b>multiplica por 60</b>: 3 h = 180 min. Para pasar de minutos a horas, divide entre 60: 150 min = 2 h 30 min.",
      "Para calcular cuánto dura algo, cuenta hasta la hora en punto y después el resto: de 9:40 a 11:15 son 20 min + 1 h + 15 min = 1 h 35 min."],
     [("¿Cuántos segundos son 4 minutos?", ["4 × 60"], "240 segundos"), ("De 10:45 a 12:20", ["10:45 → 11:00: 15 min", "11:00 → 12:20: 1 h 20 min"], "1 h 35 min")],
     [["Pensar que 1 hora = 100 minutos", "1 hora = 60 minutos."], ["Restar horas como números decimales", "De 9:40 a 11:15 no son 1 h 75 min."], ["Olvidar el día cuando pasa de medianoche", "De 22:00 a 1:00 son 3 horas."]],
     [("¿Cuántos segundos tiene una hora?", "3 600 segundos, porque 1 hora tiene 60 minutos y cada minuto tiene 60 segundos: 60 × 60 = 3 600."),
      ("¿Cómo calculo cuánto dura una actividad?", "Cuenta desde la hora de inicio hasta la siguiente hora en punto, luego las horas completas y al final los minutos que faltan.")],
     [("Días, horas, minutos y segundos", [(uni, 20)]), ("Horas y minutos juntos", [(compl, 20)]), ("¿Cuánto dura?", [(dur, 20)]), ("Sumar y restar tiempos", [(oper, 10), (h24, 10)]),
      ("Siglos, años y calendario", [(cal, 20)])],
     64014, pic=mx_text(ES.reloj(10, 45)), lv=4)
