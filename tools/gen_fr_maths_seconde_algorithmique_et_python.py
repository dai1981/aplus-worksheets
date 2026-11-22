# -*- coding: utf-8 -*-
"""
France Maths Seconde : Algorithmique et programmation en Python (variables, affectation, conditions, boucles for et while, fonctions)
  python3 tools/gen_fr_maths_seconde_algorithmique_et_python.py
Erreurs : confondre = et ==, range(1, n) qui s’arrête à n − 1, oublier que l’affectation remplace l’ancienne valeur, compter un tour de boucle de trop.
"""
import random
from fr_c4 import *

R = random.Random(60521)
K = Kids(R)
SP = NB * 4


def code(*lines):
    out = []
    for ln in lines:
        ind = len(ln) - len(ln.lstrip(" "))
        out.append(NB * ind + ln.lstrip(" ").replace("<", "&lt;").replace(">", "&gt;"))
    return "<span class='code'>%s</span>" % "<br>".join(out)


def s1():
    k = R.choice(["aff", "aff", "swap", "type"])
    a, b = R.randint(2, 9), R.randint(2, 9)
    if k == "aff":
        c = R.randint(2, 5)
        v = a + b
        v = v * c
        v = v - a
        return M("Que contient la variable x après ce programme ?%s" % code("x = %d" % a, "y = %d" % b, "x = x + y", "x = x * %d" % c, "x = x - %d" % a), str(v), [str((a + b) * c), str(a + b * c - a), str(a)],
                 "x vaut %d, puis %d, puis %d, puis <b>%d</b> (chaque affectation remplace l’ancienne valeur)." % (a, a + b, (a + b) * c, v))
    if k == "swap":
        return M("Que valent a et b à la fin ?%s" % code("a = %d" % a, "b = %d" % b, "a = b", "b = a"), "a = %d et b = %d" % (b, b), ["a = %d et b = %d" % (b, a), "a = %d et b = %d" % (a, a), "a = %d et b = %d" % (a, b)] if a != b else ["a = %d et b = %d" % (a + 1, b), "a = 0 et b = 0", "a = %d et b = %d" % (a, b + 1)],
                 "Après a = b, a vaut %d ; puis b = a donne aussi %d : <b>a = %d et b = %d</b> (l’ancienne valeur de a est perdue)." % (b, b, b, b))
    V = [("Quel est le type de la valeur 3.5 en Python ?", "float (nombre décimal)", ["int (entier)", "str (chaîne)", "bool (booléen)"]),
         ("Quel est le type de la valeur 'bonjour' en Python ?", "str (chaîne de caractères)", ["int (entier)", "float (décimal)", "bool (booléen)"]),
         ("Quel est le type de la valeur True en Python ?", "bool (booléen)", ["str (chaîne)", "int (entier)", "float (décimal)"]),
         ("Quel est le type de la valeur 12 en Python ?", "int (entier)", ["float (décimal)", "str (chaîne)", "bool (booléen)"]),
         ("Que vaut 17 // 5 en Python ?", "3", ["3.4", "2", "5"]),
         ("Que vaut 17 % 5 en Python ?", "2", ["3", "3.4", "0.2"]),
         ("Que vaut 2 ** 5 en Python ?", "32", ["10", "25", "7"]),
         ("Quelle instruction affecte la valeur 5 à la variable n ?", "n = 5", ["n == 5", "5 = n", "let n = 5"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s2():
    k = R.choice(["if", "if", "ifelif", "test"])
    x = R.randint(-10, 20)
    s_ = R.randint(0, 15)
    if k == "if":
        r = x * 2 if x > s_ else x + 10
        return M("Que renvoie f(%d) ?%s" % (x, code("def f(x):", "    if x > %d:" % s_, "        return 2 * x", "    else:", "        return x + 10")), d(r), [d(x + 10) if r != x + 10 else d(2 * x), d(x), d(r + 1)],
                 "%s %s %d, donc on calcule %s = <b>%s</b>." % (d(x), "&gt;" if x > s_ else "⩽", s_, "2 × %s" % par(x) if x > s_ else "%s + 10" % d(x), d(r)))
    if k == "ifelif":
        n = R.randint(0, 20)
        res = "TB" if n >= 16 else "B" if n >= 14 else "AB" if n >= 12 else "rien"
        return M("Que renvoie mention(%d) ?%s" % (n, code("def mention(n):", "    if n >= 16:", "        return 'TB'", "    elif n >= 14:", "        return 'B'", "    elif n >= 12:", "        return 'AB'", "    else:", "        return 'rien'")),
                 "'%s'" % res, ["'%s'" % o for o in ["TB", "B", "AB", "rien"] if o != res],
                 "On teste les conditions dans l’ordre ; la première vraie donne <b>'%s'</b>." % res)
    a, b = R.randint(1, 30), R.randint(1, 30)
    V = [("%d == %d" % (a, a), "True"), ("%d == %d" % (a, a + 1), "False"), ("%d < %d and %d > 0" % (a, b, a), str(a < b)), ("%d > %d or %d == %d" % (a, b, b, b), "True"), ("not (%d > %d)" % (a, b), str(not a > b)), ("%d %% 2 == 0" % a, str(a % 2 == 0))]
    e, r = R.choice(V)
    return M("Que vaut l’expression %s en Python ?" % e.replace("<", "&lt;").replace(">", "&gt;"), r, ["False" if r == "True" else "True", "une erreur", str(a)], "<b>%s</b>." % r)


def s3():
    k = R.choice(["sum", "sum", "prod", "count", "range"])
    n = R.randint(3, 10)
    if k == "sum":
        st = R.choice([0, 1])
        s_ = sum(range(st, n + 1))
        return M("Que contient s à la fin ?%s" % code("s = 0", "for i in range(%d, %d):" % (st, n + 1), "    s = s + i"), str(s_), [str(s_ - n), str(sum(range(st, n + 2))), str(n)],
                 "range(%d, %d) donne %s : la somme vaut <b>%d</b>." % (st, n + 1, ", ".join(map(str, range(st, n + 1))), s_))
    if k == "prod":
        m = R.randint(3, 6)
        p = 1
        for i in range(1, m + 1):
            p *= i
        return M("Que contient p à la fin ?%s" % code("p = 1", "for i in range(1, %d):" % (m + 1), "    p = p * i"), str(p), [str(p // m), str(sum(range(1, m + 1))), str(p * (m + 1))],
                 "p = 1 × 2 × … × %d = <b>%d</b>." % (m, p))
    if k == "count":
        a = R.randint(2, 5)
        c = len([i for i in range(n * 3) if i % a == 0])
        return M("Que contient c à la fin ?%s" % code("c = 0", "for i in range(%d):" % (n * 3), "    if i %% %d == 0:" % a, "        c = c + 1"), str(c), [str(c - 1), str(n * 3 // a), str(c + 1)] if n * 3 // a != c else [str(c - 1), str(c + 1), str(n * 3)],
                 "On compte les multiples de %d de 0 à %d : <b>%d</b>." % (a, n * 3 - 1, c))
    a = R.randint(0, 5)
    b = a + R.randint(3, 8)
    return M("Combien de fois la boucle « for i in range(%d, %d): » s’exécute-t-elle ?" % (a, b), str(b - a), [str(b - a + 1), str(b), str(b - a - 1)], "i prend les valeurs %d à %d : <b>%d</b> tours." % (a, b - 1, b - a))


def s4():
    k = R.choice(["dbl", "dbl", "seuil", "u"])
    if k == "dbl":
        x0 = R.choice([1, 2, 3, 5])
        L_ = R.choice([50, 100, 200, 1000])
        x, n = x0, 0
        while x < L_:
            x, n = x * 2, n + 1
        return M("Que contient n à la fin ?%s" % code("x = %d" % x0, "n = 0", "while x < %d:" % L_, "    x = 2 * x", "    n = n + 1"), str(n), [str(n + 1), str(n - 1), str(x)],
                 "x prend les valeurs %s ; la boucle s’arrête quand x ⩾ %d : <b>n = %d</b>." % (", ".join(str(x0 * 2 ** i) for i in range(n + 1)), L_, n))
    if k == "seuil":
        c = R.choice([100, 1000])
        t = R.choice([Fr(11, 10), Fr(12, 10), Fr(15, 10)])
        L_ = c * 2
        v, n = Fr(c), 0
        while v < L_:
            v, n = v * t, n + 1
        return M("Un capital de %s € augmente de %s %% par an. Ce programme cherche le nombre d’années pour le doubler. Que renvoie-t-il ?%s" % (num(c), d((t - 1) * 100), code("v = %d" % c, "n = 0", "while v < %d:" % L_, "    v = v * %s" % str(float(t)), "    n = n + 1", "print(n)")),
                 str(n), [str(n + 1), str(n - 1), str(int(100 / ((t - 1) * 100)))] if int(100 / ((t - 1) * 100)) not in (n, n + 1, n - 1) else [str(n + 1), str(n - 1), str(n + 2)],
                 "On multiplie par %s jusqu’à dépasser %s : <b>%d</b> années." % (d(t), num(L_), n))
    u0 = R.randint(1, 5)
    a = R.randint(2, 4)
    b = R.randint(1, 5)
    n = R.randint(2, 4)
    u = u0
    for _ in range(n):
        u = a * u + b
    return M("Que contient u à la fin ?%s" % code("u = %d" % u0, "for k in range(%d):" % n, "    u = %d * u + %d" % (a, b)), str(u), [str(a * u0 + b), str(u0 + n * (a + b)), str((u - b) // a) if (u - b) % a == 0 else str(u + 1)],
             "On applique %d fois u ← %du + %d à partir de %d : <b>%d</b>." % (n, a, b, u0, u))


def s5():
    k = R.choice(["func", "func", "complete", "random"])
    if k == "func":
        a, b, x = R.randint(2, 6), R.choice([v for v in range(-9, 10) if v]), R.randint(-5, 6)
        return M("Que renvoie f(%d) ?%s" % (x, code("def f(x):", "    y = %d * x ** 2 %s %d" % (a, "+" if b >= 0 else "-", abs(b)), "    return y")), d(a * x * x + b), [d((a * x) ** 2 + b), d(a * 2 * x + b), d(a * x * x - b)] if b else [d((a * x) ** 2), d(2 * a * x), d(a * x * x + 1)],
                 "%d × %s² %s %d = <b>%s</b> (** est la puissance)." % (a, par(x), "+" if b >= 0 else MINUS, abs(b), d(a * x * x + b)))
    if k == "complete":
        V = [("On veut une fonction qui renvoie True si n est pair. Que mettre à la place de … ?%s" % code("def pair(n):", "    return …"), "n % 2 == 0", ["n / 2 == 0", "n % 2 = 0", "n // 2"]),
             ("On veut que la boucle affiche 1, 2, …, 10. Que mettre à la place de … ?%s" % code("for i in …:", "    print(i)"), "range(1, 11)", ["range(10)", "range(1, 10)", "range(0, 11)"]),
             ("On veut calculer la moyenne de a, b, c. Quelle instruction convient ?", "m = (a + b + c) / 3", ["m = a + b + c / 3", "m = (a + b + c) // 3", "m = a + b + c, 3"]),
             ("On veut répéter tant que x est inférieur à 100. Quelle ligne convient ?", "while x < 100:", ["for x < 100:", "if x < 100:", "while x > 100:"])]
        q, a_, w = R.choice(V)
        return M(q, a_.replace("<", "&lt;"), [x.replace("<", "&lt;").replace(">", "&gt;") for x in w], "Réponse : <b>%s</b>." % a_.replace("<", "&lt;"))
    V = [("Après « from random import randint », que peut renvoyer randint(1, 6) ?", "un entier de 1 à 6", ["un entier de 1 à 5", "un décimal entre 1 et 6", "toujours 6"]),
         ("Que fait cette fonction ?%s" % code("from random import random", "def essai():", "    if random() < 0.3:", "        return 1", "    return 0"), "elle simule une épreuve de succès de probabilité 0,3", ["elle renvoie toujours 1", "elle renvoie 0,3", "elle simule un dé à 6 faces"]),
         ("Que calcule cette fonction ?%s" % code("def compte(n):", "    c = 0", "    for i in range(n):", "        c = c + essai()", "    return c"), "le nombre de succès sur n épreuves", ["la probabilité exacte de succès", "la moyenne de n nombres", "n fois la même valeur"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Variables et affectations", mix(R, seen, [(s1, 20)])), ("Conditions", mix(R, seen, [(s2, 20)])),
            ("Boucles bornées (for)", mix(R, seen, [(s3, 20)])), ("Boucles non bornées (while)", mix(R, seen, [(s4, 20)])), ("Fonctions et simulation", mix(R, seen, [(s5, 20)]))]
    body = L(["Une <b>variable</b> a un type (int, float, str, bool). L’affectation x = x + 1 remplace l’ancienne valeur de x. Le test d’égalité s’écrit ==.",
              "<b>if / elif / else</b> exécute un bloc selon une condition. <b>for i in range(a, b)</b> répète pour i = a, …, b − 1. <b>while condition</b> répète tant que la condition est vraie.",
              "Une <b>fonction</b> (def) prend des arguments et renvoie un résultat avec return. random() et randint() servent à simuler des expériences aléatoires."],
             [("s = 0 ; for i in range(1, 5): s = s + i", ["i = 1, 2, 3, 4", "s = 1 + 2 + 3 + 4"], "s = 10")],
             [["range(1, 5) va jusqu’à 5", "Il s’arrête à 4."], ["Écrire if x = 3:", "Le test d’égalité est ==."], ["Oublier l’indentation", "Le bloc d’une boucle ou d’une condition est décalé de 4 espaces."]])
    faq = [("Quand utiliser for ou while ?", "for quand on connaît le nombre de répétitions ; while quand on répète jusqu’à ce qu’une condition change (un seuil à dépasser)."),
           ("Que signifient // et % ?", "a // b est le quotient de la division euclidienne, a % b son reste.")]
    unit("seconde", R, "algorithmique-et-python", "P",
         "Utiliser des variables et des affectations ; écrire des instructions conditionnelles ; écrire des boucles bornées (for) et non bornées (while) ; écrire, lire et compléter des fonctions en Python ; simuler des expériences aléatoires",
         "Algorithmique et programmation en Python", "Algorithmique et Python",
         "Fiches de maths seconde sur l’algorithmique en Python : variables, affectations, conditions, boucles for et while, fonctions et simulation. 100 exercices corrigés.",
         "for : nombre de tours connu ; while : jusqu’à une condition", "range(a, b) : de a à b − 1", body, faq, sets, 21)


if __name__ == "__main__":
    main()
