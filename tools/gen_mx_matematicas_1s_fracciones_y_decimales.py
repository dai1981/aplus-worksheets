# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Convertir fracciones a decimales y decimales a fracciones; decimales periódicos."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67103))
frac = src("gen_es_matematicas_1eso_numeros_decimales", 67331, "s_frac", lv=1)
tipo, gen = src("gen_es_matematicas_2eso_fracciones_y_decimales", 67332, "s_tipo", "s_generatriz", lv=2)

unit("fracciones-y-decimales", 3, "6FD",
     "Usa diversas estrategias al convertir números fraccionarios a decimales y viceversa; distingue decimales finitos y periódicos",
     "Fracciones y decimales: convertir", "Fracciones y decimales",
     "Ejercicios de matemáticas de 1.er grado de secundaria: convertir fracciones a decimales y decimales a fracciones, decimales finitos y periódicos, comparar y ordenar. 100 ejercicios con respuestas.",
     "Divide numerador entre denominador", "0.75 = 75/100 = 3/4",
     ["Para pasar una <b>fracción a decimal</b>, divide el numerador entre el denominador: 3/8 = 3 ÷ 8 = 0.375.",
      "Para pasar un <b>decimal a fracción</b>, escribe el número sin punto sobre 10, 100 o 1 000 (según las cifras decimales) y simplifica: 0.45 = 45/100 = 9/20.",
      "Si el denominador (simplificado) solo tiene los factores 2 y 5, el decimal es <b>finito</b>. Si tiene otros (3, 7, 11…), es <b>periódico</b>: 2/3 = 0.666… = 0.<span class='ov'>6</span>."],
     [("5/8", ["5 ÷ 8"], "0.625"), ("0.24", ["24/100", "÷ 4"], "6/25"), ("7/9", ["7 ÷ 9 = 0.777…"], "0.<span class='ov'>7</span>")],
     [["Escribir 3/4 como 3.4", "La fracción es una división: 3 ÷ 4 = 0.75."], ["No simplificar", "0.5 = 5/10 = 1/2."], ["Redondear un periódico", "1/3 no es 0.33: es 0.<span class='ov'>3</span>."]],
     [("¿Toda fracción se puede escribir como decimal?", "Sí: el decimal es finito o periódico."), ("¿Qué significa la raya sobre las cifras?", "Indica el periodo, las cifras que se repiten sin fin: 0.<span class='ov'>18</span> = 0.181818…")],
     [("De fracción a decimal", [(S.fd_frac2dec, 14), (frac, 6)]), ("De decimal a fracción", [(S.fd_dec2frac, 20)]), ("Decimales periódicos", [(S.fd_periodic, 12), (tipo, 8)]),
      ("Comparar y ordenar", [(S.fd_compare, 12), (S.fd_problem, 8)]), ("Problemas", [(S.fd_problem, 14), (gen, 6)])],
     67003, lv=7)
