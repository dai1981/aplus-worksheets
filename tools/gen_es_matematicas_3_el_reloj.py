# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: El reloj y el calendario (Sentido de la medida)
Reloj de agujas y digital, horas de la tarde (24 horas), horas, minutos y días, duraciones, problemas.
Reutiliza los generadores de 4.º (mismo ciclo).
"""
from es_low import unit, src
from es_common import reloj

SEED = 33913
ag, dig, h24, uni, dur, prob = src("el_tiempo_y_el_reloj", SEED, "s1_agujas", "s1_digital", "s2_24", "s3_unidades", "s4_duracion", "s5_problema", mx=99999)

unit(3, "el-reloj-y-el-calendario", 13, "M", "Lectura del reloj analógico y digital; horas, minutos, días, semanas y meses; duración de actividades cotidianas",
     "El reloj y el calendario", "El reloj",
     "Fichas de matemáticas de 3.º de Primaria: leer el reloj de agujas y el digital, las horas de la tarde, días y meses, y duraciones. 100 ejercicios con soluciones.",
     "La aguja corta marca la hora", "La larga marca los minutos.",
     ["La aguja <b>corta</b> marca la hora y la <b>larga</b>, los minutos. Cada número de la esfera son 5 minutos.", "Y cuarto = 15 min; y media = 30 min; menos cuarto = faltan 15 min.",
      "Por la tarde, el reloj digital suma 12: las 5 de la tarde son las 17:00.", "1 hora = 60 minutos; 1 día = 24 horas; 1 semana = 7 días."],
     [("La aguja corta pasa del 3 y la larga está en el 6", ["Las 3 y 30 minutos"], "las tres y media"), ("De 9:15 a 10:00", ["Faltan 45 minutos para las 10"], "45 minutos")],
     [["Confundir las agujas", "La corta es la hora."], ["Leer «menos cuarto» con la hora anterior", "Las 6 menos cuarto son las 5:45."], ["Pensar que 1 hora = 100 minutos", "1 hora = 60 minutos."]],
     [("¿Qué hora es «menos cuarto»?", "Faltan 15 minutos para la hora. Las 4 menos cuarto son las 3:45."), ("¿Cómo se pasa a 24 horas?", "Por la tarde y por la noche se suma 12: las 8 de la tarde son las 20:00.")],
     [("El reloj de agujas", [(ag, 20)]), ("El reloj digital y las 24 horas", [(dig, 10), (h24, 10)]), ("Horas, minutos y días", [(uni, 20)]), ("¿Cuánto dura?", [(dur, 20)]), ("Problemas", [(prob, 20)])],
     33013, reloj(3, 30))
