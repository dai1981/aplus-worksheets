# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: El dinero (Sentido de la medida)
Monedas y billetes de euro, euros y céntimos, comparar precios, compras y vueltas, problemas.
Reutiliza los generadores de 4.º (mismo ciclo).
"""
from es_low import unit, src
from es_common import dinero_svg

SEED = 33914
cont, eq, comp, compra, mon, prob = src("el_dinero", SEED, "s1_contar", "s1_equiv", "s2_comparar", "s3_compra", "s4_monedas", "s5_problema", mx=99999, dec=True)

unit(3, "el-dinero", 14, "M", "El sistema monetario: monedas y billetes de euro; equivalencias entre euros y céntimos; compras, vueltas y presupuestos sencillos",
     "El dinero: euros y céntimos", "El dinero",
     "Fichas de matemáticas de 3.º de Primaria: contar monedas y billetes, euros y céntimos, comparar precios, compras y vueltas. 100 ejercicios con soluciones.",
     "1 € = 100 céntimos", "Cuenta primero los billetes.",
     ["Hay monedas de 1, 2, 5, 10, 20 y 50 céntimos y de 1 y 2 €. Billetes de 5, 10, 20, 50… €.", "<b>1 € = 100 céntimos</b>. 3,50 € son 3 euros y 50 céntimos.",
      "Para contar, empieza por lo que vale más.", "Las <b>vueltas</b> son lo que pagas menos lo que cuesta."],
     [("Un billete de 5 €, dos monedas de 1 € y una de 50 c", ["5 + 2 = 7 €", "+ 50 céntimos"], "7,50 €"), ("Cuesta 3,20 € y pagas con 5 €", ["5,00 − 3,20"], "1,80 €")],
     [["Contar las monedas sin mirar su valor", "Tres monedas no son 3 €: mira cuánto vale cada una."], ["Pensar que 1 € = 10 céntimos", "1 € = 100 céntimos."], ["Restar mal las vueltas", "Comprueba: precio + vueltas = lo que pagas."]],
     [("¿Cuántos céntimos tiene un euro?", "Un euro tiene 100 céntimos."), ("¿Cómo se calculan las vueltas?", "Se resta el precio de lo que se ha pagado. Por ejemplo, 5 € − 3,20 € = 1,80 €.")],
     [("Contar dinero", [(cont, 20)]), ("Euros y céntimos", [(eq, 20)]), ("Comparar precios", [(comp, 12), (mon, 8)]), ("Compras y vueltas", [(compra, 20)]), ("Problemas", [(prob, 20)])],
     33014, dinero_svg([500, 100, 100, 50]))
