# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Sistemas de ecuaciones (Sentido algebraico)
Sistemas lineales con tres incógnitas: comprobar soluciones, sistemas escalonados, método de Gauss, clasificación; problemas de ventas, inversiones y repartos.
Reutiliza los generadores de Matemáticas I con otra semilla.
Errores: operar mal al eliminar, confundir sistema incompatible con indeterminado, desordenar las incógnitas en la respuesta.
"""
import random
from es_ccss import M, mix, num, unit, L, W, eu, use_, pc

R = random.Random(53004)
s_comprobar, s_escalonado, s_gauss, s_clasificar, s_problema = use_("gen_es_matematicas_1bach_sistemas_metodo_de_gauss", 53204, "s_comprobar", "s_escalonado", "s_gauss", "s_clasificar", "s_problema")


def s_economia():
    t = R.choice(["teatro", "teatro", "fondos", "fondos", "fabrica"])
    if t == "teatro":
        z = R.randint(20, 80)
        k = R.choice([2, 3])
        x = k * z
        y = R.randint(30, 150)
        pa, pj, pi = R.choice([(12, 8, 5), (10, 7, 4), (15, 10, 6), (9, 6, 4), (14, 9, 5)])
        N, T = x + y + z, pa * x + pj * y + pi * z
        ok = "%d de adulto, %d de joven y %d infantiles" % (x, y, z)
        return M("Un teatro vendió %d entradas: de adulto (%d €), de joven (%d €) e infantiles (%d €), y recaudó %s. Las de adulto fueron el %s de las infantiles. ¿Cuántas se vendieron de cada tipo?" % (N, pa, pj, pi, eu(T, 0), "doble" if k == 2 else "triple"), ok,
                 W(["%d de adulto, %d de joven y %d infantiles" % v for v in ((z, y, x), (y, x, z), (x + k, y - k - 1, z + 1), (x - k, y + k + 1, z - 1))]),
                 "x + y + z = %d; %dx + %dy + %dz = %d; x = %dz → <b>%s</b>." % (N, pa, pj, pi, T, k, ok))
    if t == "fondos":
        a, b = R.randrange(2000, 9001, 1000), R.randrange(2000, 9001, 1000)
        c = a + b
        r1, r2_, r3 = R.choice([(2, 3, 5), (1, 3, 4), (2, 4, 6), (3, 4, 5)])
        C = a + b + c
        I = (a * r1 + b * r2_ + c * r3) / 100
        ok = "%s, %s y %s" % (eu(a, 0), eu(b, 0), eu(c, 0))
        return M("Se invierten %s en tres fondos al %d %%, %d %% y %d %% anual. En el tercero se pone lo mismo que en los otros dos juntos y los intereses del año son %s. ¿Cuánto se invierte en cada fondo?" % (eu(C, 0), r1, r2_, r3, eu(I)), ok,
                 W(["%s, %s y %s" % (eu(b, 0), eu(a, 0), eu(c, 0)) if a != b else None, "%s, %s y %s" % (eu(C / 3, 0), eu(C / 3, 0), eu(C / 3, 0)) if C % 3 == 0 else "%s, %s y %s" % (eu(c, 0), eu(a, 0), eu(b, 0)), "%s, %s y %s" % (eu(a + 1000, 0), eu(b - 1000, 0), eu(c, 0)) if b > 1000 else None,
                    "%s, %s y %s" % (eu(a - 1000, 0), eu(b + 1000, 0), eu(c, 0)) if a > 1000 else None, "%s, %s y %s" % (eu(a, 0), eu(c, 0), eu(b, 0))]),
                 "x + y + z = %s; %s x + %s y + %s z = %s; z = x + y → <b>%s</b>." % (num(C), "0,0%d" % r1, "0,0%d" % r2_, "0,0%d" % r3, eu(I), ok))
    x, y, z = R.randint(2, 9), R.randint(2, 9), R.randint(2, 9)
    m = [(1, 2, 1), (2, 1, 1), (1, 1, 3)]
    h = [sum(a * v for a, v in zip(row, (x, y, z))) for row in m]
    ok = "%d mesas, %d sillas y %d estanterías" % (x, y, z)
    return M("Una carpintería fabrica mesas, sillas y estanterías. Una mesa necesita 1 h de corte, 2 h de montaje y 1 h de pintura; una silla, 2 h, 1 h y 1 h; una estantería, 1 h, 1 h y 3 h. "
             "Esta semana se usaron %d h de corte, %d h de montaje y %d h de pintura. ¿Cuántos muebles de cada tipo se hicieron?" % (h[0], h[1], h[2]), ok,
             W(["%d mesas, %d sillas y %d estanterías" % v for v in ((y, x, z), (z, y, x), (x, z, y), (x + 1, y - 1, z), (x, y + 1, z - 1))]),
             "x + 2y + z = %d; 2x + y + z = %d; x + y + 3z = %d → <b>%s</b>." % (h[0], h[1], h[2], ok))


seen = set()
sets = [("Comprobar soluciones y sistemas escalonados", mix(R, seen, [(s_comprobar, 8), (s_escalonado, 12)])), ("Método de Gauss", mix(R, seen, [(s_gauss, 20)])),
        ("Clasificar sistemas", mix(R, seen, [(s_clasificar, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)])), ("Problemas de economía", mix(R, seen, [(s_economia, 20)]))]
think = ["Un <b>sistema lineal</b> con tres incógnitas se resuelve con el <b>método de Gauss</b>: se eliminan incógnitas hasta dejarlo <b>escalonado</b>.",
         "Después se despeja de abajo arriba: z, luego y, luego x.",
         "Si aparece 0 = 0, el sistema es <b>compatible indeterminado</b> (infinitas soluciones); si aparece 0 = 5, es <b>incompatible</b> (sin solución).",
         "En un problema: elige las incógnitas, escribe una ecuación por cada dato y comprueba la solución en el enunciado."]
ex = [("Entradas de 10 €, 7 € y 4 €: 200 entradas, 1 580 €; adulto = doble de infantil", ["x + y + z = 200", "10x + 7y + 4z = 1580", "x = 2z → y = 200 − 3z → 3z + 1400 = 1580"], "x = 120, y = 20, z = 60")]
mist = [["Equivocarse de signo al eliminar", "Escribe la operación: E2 − 2E1."], ["Confundir 0 = 0 con 0 = 5", "0 = 0: infinitas soluciones; 0 = 5: ninguna."], ["Cambiar el orden de las respuestas", "Di qué es x, qué es y y qué es z."]]
body = L(think, ex, mist)
faq = [("¿Qué tipos de sistemas hay?", "Compatible determinado (una solución), compatible indeterminado (infinitas) e incompatible (ninguna)."),
       ("¿Para qué sirven los sistemas en ciencias sociales?", "Para repartos, mezclas, presupuestos, inversiones o producción: cuando varias cantidades desconocidas cumplen varias condiciones a la vez.")]
unit(1, R, "sistemas-de-ecuaciones", "A", "Sistemas de ecuaciones lineales con tres incógnitas: método de Gauss, clasificación y resolución de problemas de economía y ciencias sociales",
     "Sistemas de ecuaciones", "Sistemas de ecuaciones", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: método de Gauss, clasificación de sistemas y problemas de ventas, inversiones y producción. 100 ejercicios.",
     "Gauss: escalona y despeja", "0 = 0: infinitas; 0 = 5: ninguna.", body, faq, sets, 4)
