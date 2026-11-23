# -*- coding: utf-8 -*-
"""México 4.º grado: Comparar, ordenar y redondear números de hasta cinco cifras (Estudio de los números). Reutiliza España 4.º con otra semilla."""
import random
from mx_common import src, unit, mcq, num, mx_text
import es_common as ES

signo, verdad, redondear, entre, recta, probl = src("gen_es_matematicas_4_comparar_y_redondear_numeros", 64202, "s1_signo", "s1_verdad", "s3_redondear", "s4_entre", "s4_recta", "s5_problema", mx_=99999)
R = random.Random(64102)


def near(n):
    s = list(str(n))
    i = R.randrange(1, len(s))
    s[i] = str((int(s[i]) + R.choice([1, 2, 7, 8, 9])) % 10)
    return int("".join(s))


def orden():
    base = R.randint(10, 99) * 1000 + R.randint(0, 999)
    xs = sorted({base, near(base), near(base), base // 10})
    if len(xs) < 4:
        return None
    R.shuffle(xs)
    k = R.choice(["mayor", "menor", "asc", "desc"])
    lst = ", ".join(num(x) for x in xs)
    if k == "mayor":
        return mcq("¿Cuál es el número mayor? %s" % lst, num(max(xs)), [num(x) for x in xs], "Comparamos cifra por cifra desde la izquierda: el mayor es <b>%s</b>." % num(max(xs)))
    if k == "menor":
        return mcq("¿Cuál es el número menor? %s" % lst, num(min(xs)), [num(x) for x in xs], "El que tiene menos cifras es el menor: <b>%s</b>." % num(min(xs)))
    seq = sorted(xs) if k == "asc" else sorted(xs)[::-1]
    sep = " &lt; " if k == "asc" else " &gt; "
    f = lambda L: sep.join(num(x) for x in L)
    return mcq("Ordena de %s: %s" % ("menor a mayor" if k == "asc" else "mayor a menor", lst), f(seq),
               [f([seq[0], seq[2], seq[1], seq[3]]), f([seq[1], seq[0], seq[2], seq[3]]), f([seq[3], seq[1], seq[2], seq[0]])], "<b>%s</b>." % f(seq))


unit("comparar-y-redondear-numeros", 2, "N",
     "Compara y ordena números de hasta cinco cifras con los signos mayor que, menor que e igual; los ubica en la recta numérica; redondea a la decena, la centena y la unidad de millar",
     "Comparar, ordenar y redondear números", "Comparar y redondear",
     "Ejercicios de matemáticas de 4.º grado de primaria: comparar números de cinco cifras con &lt; y &gt;, ordenar, la recta numérica y redondear. 100 ejercicios con respuestas.",
     "Compara desde la izquierda", "Redondea mirando la cifra de la derecha.",
     ["Un número con más cifras es mayor. Si tienen las mismas cifras, compara de izquierda a derecha: 45 812 &gt; 45 279 porque 8 &gt; 2 en las centenas.",
      "El signo abre la boca hacia el número mayor: 3 450 &lt; 3 540.",
      "Para <b>redondear</b> a la centena, mira la cifra de las decenas: si es 5 o más, sube; si es menor que 5, se queda. 4 271 → 4 300; 4 231 → 4 200."],
     [("Compara 62 405 y 62 450", ["62 = 62; 4 = 4", "decenas: 0 &lt; 5"], "62 405 &lt; 62 450"), ("Redondea 38 640 a la unidad de millar", ["La cifra de las centenas es 6", "6 ≥ 5: sube"], "39 000")],
     [["Comparar solo la primera cifra", "Si es igual, mira la siguiente."], ["Mirar la cifra equivocada al redondear", "A la centena, mira las decenas."], ["Olvidar los ceros", "4 271 a la centena es 4 300, no 43."]],
     [("¿Qué significan los signos &lt; y &gt;?", "«&lt;» es «menor que» y «&gt;» es «mayor que». La punta señala al número menor."),
      ("¿Cómo se redondea a la unidad de millar?", "Mira la cifra de las centenas: si es 5 o más, suma 1 a los millares; si no, se quedan igual. Lo de la derecha pasa a ser 0.")],
     [("Mayor, menor o igual", [(signo, 12), (verdad, 8)]), ("Ordenar números", [(orden, 20)]), ("La recta numérica", [(recta, 12), (entre, 8)]), ("Redondear", [(redondear, 20)]), ("Problemas", [(probl, 20)])],
     64002, pic=mx_text(ES.recta(45000, 46000, 100, marks=[(45300, "")], every=500)), lv=4)
