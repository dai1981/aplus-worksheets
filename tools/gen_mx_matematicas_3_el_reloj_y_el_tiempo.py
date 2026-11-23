# -*- coding: utf-8 -*-
"""México 3.er grado: Medición del tiempo (relojes de manecillas y digitales, hora, media hora, cuarto de hora y minutos; duración de actividades). Reutiliza España 4.º con frases de México."""
from mx_common import src, unit, hora_letra, mx_text
import es_common as ES

ag, dig, h24, uni, dur, prob = src("gen_es_matematicas_4_el_tiempo_y_el_reloj", 63215, "s1_agujas", "s1_digital", "s2_24", "s3_unidades", "s4_duracion", "s5_problema", mx_=99999,
                                   patch={"dicho": hora_letra})

unit("el-reloj-y-el-tiempo", 15, "T",
     "Lee relojes de manecillas y digitales; usa la hora, la media hora, el cuarto de hora y los minutos; compara y ordena la duración de actividades cotidianas",
     "El reloj y el tiempo", "El reloj",
     "Ejercicios de matemáticas de 3.er grado de primaria: leer el reloj de manecillas y el digital, cuarto para las, horas de la tarde, días y duraciones. 100 ejercicios con respuestas.",
     "La manecilla corta marca la hora", "La larga marca los minutos.",
     ["La manecilla <b>corta</b> marca la hora y la <b>larga</b>, los minutos. Cada número de la carátula son 5 minutos.",
      "Y cuarto = 15 min; y media = 30 min; <b>cuarto para las 4</b> = faltan 15 minutos para las 4 (3:45).",
      "En el reloj de 24 horas, por la tarde se suma 12: las 5 de la tarde son las 17:00.", "1 hora = 60 minutos; 1 día = 24 horas; 1 semana = 7 días."],
     [("La manecilla corta pasa del 3 y la larga está en el 6", ["Las 3 y 30 minutos"], "las tres y media"), ("De 9:15 a 10:00", ["Faltan 45 minutos para las 10"], "45 minutos")],
     [["Confundir las manecillas", "La corta es la hora."], ["Leer «cuarto para las 6» como 6:15", "Faltan 15 minutos para las 6: son las 5:45."], ["Pensar que 1 hora = 100 minutos", "1 hora = 60 minutos."]],
     [("¿Qué hora es «cuarto para las cuatro»?", "Faltan 15 minutos para las cuatro: son las 3:45."), ("¿Cómo se pasa a 24 horas?", "Por la tarde y por la noche se suma 12: las 8 de la noche son las 20:00.")],
     [("El reloj de manecillas", [(ag, 20)]), ("El reloj digital y las 24 horas", [(dig, 10), (h24, 10)]), ("Horas, minutos y días", [(uni, 20)]), ("¿Cuánto dura?", [(dur, 20)]), ("Problemas", [(prob, 20)])],
     63015, pic=mx_text(ES.reloj(3, 30)))
