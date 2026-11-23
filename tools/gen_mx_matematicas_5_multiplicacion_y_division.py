# -*- coding: utf-8 -*-
"""México 5.º grado: Multiplicación y división de números naturales (algoritmos, divisor de dos cifras, problemas). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit, mx_text
import es_common as ES

dos, tres = src("gen_es_matematicas_4_multiplicacion", 65206, "s3_dos", "s3_tres", mx_=99999999, extra=(lambda it: "× 0 = 0" not in it["e"],))
propm, probm = src("gen_es_matematicas_4_multiplicacion", 65206, "s4_prop", "s5_problema", mx_=999999)
ddos, dterm, dceros, dprob = src("gen_es_matematicas_4_division", 65207, "s2_dos", "s3_terminos", "s4_ceros", "s5_problema", mx_=999999)

unit("multiplicacion-y-division", 2, "P",
     "Resuelve multiplicaciones con factores de hasta tres cifras y divisiones con divisor de hasta dos cifras usando los algoritmos convencionales; interpreta el cociente y el residuo; resuelve problemas",
     "Multiplicación y división", "Multiplicación y división",
     "Ejercicios de matemáticas de 5.º grado de primaria: multiplicar por dos y tres cifras, dividir entre dos cifras, cociente y residuo, la prueba y problemas. 100 ejercicios con respuestas.",
     "Divisor × cociente + residuo", "El residuo siempre es menor que el divisor.",
     ["Para multiplicar por un número de varias cifras, haz un producto parcial por cada cifra y <b>córrelo un lugar</b> a la izquierda cada vez; al final suma.",
      "Para dividir entre dos cifras, mira cuántas cifras del dividendo necesitas, estima cuántas veces cabe el divisor y comprueba multiplicando.",
      "La <b>prueba de la división</b>: divisor × cociente + residuo = dividendo."],
     [("Calcula 236 × 145", ["236 × 5 = 1 180", "236 × 40 = 9 440", "236 × 100 = 23 600", "suma"], "34 220"), ("Calcula 1 896 ÷ 24", ["189 ÷ 24 = 7, sobran 21", "216 ÷ 24 = 9"], "79")],
     [["No correr los productos parciales", "236 × 40 se escribe un lugar a la izquierda."], ["Olvidar un cero en el cociente", "2 448 ÷ 24 = 102, no 12."], ["Dejar un residuo mayor que el divisor", "Si sobra más, cabe una vez más."]],
     [("¿Cómo estimo cuántas veces cabe el divisor?", "Redondea: para 189 ÷ 24, piensa 18 ÷ 2 ≈ 9 y prueba con 24 × 8 = 192 (no cabe) y 24 × 7 = 168 (sí cabe)."),
      ("¿Cómo compruebo una multiplicación?", "Puedes estimar redondeando: 236 × 145 ≈ 200 × 150 = 30 000, así que 34 220 es razonable.")],
     [("Multiplicar por dos cifras", [(dos, 20)]), ("Multiplicar por tres cifras", [(tres, 14), (propm, 6)]), ("Dividir entre dos cifras", [(ddos, 20)]), ("Términos y cálculo mental", [(dterm, 10), (dceros, 10)]),
      ("Problemas", [(probm, 10), (dprob, 10)])],
     65002, pic=mx_text(ES.vertical(["236", "145"], op="×")), lv=5)
