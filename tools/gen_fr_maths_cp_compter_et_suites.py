# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Compter, suites de nombres, rangs (CE1 : pair et impair)
  python3 tools/gen_fr_maths_cp_compter_et_suites.py
Erreurs : après 39 écrire 310 ou 30, compter de 10 en 10 en ajoutant 1, confondre 3e et 3 devant.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, ch, KINDS, nom, un, CHOSE, le
import k_pics as KP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53003 + 100 * lv)
    K = Kids(R)


def top():
    return 100 if L == 0 else 999


def rang(n):
    return "1<sup>er</sup>" if n == 1 else "%d<sup>e</sup>" % n


def s1():
    if L == 0:
        n = R.choice([R.randint(10, 98), R.choice([19, 29, 39, 49, 59, 69, 79, 89, 99]), R.choice([20, 30, 40, 50, 60, 70, 80, 90])])
    else:
        n = R.choice([R.randint(100, 998), R.choice([109, 199, 299, 409, 599, 699, 809, 899, 990, 499]), R.choice([200, 300, 410, 500, 700, 610, 900])])
    after = R.random() < 0.55
    if after:
        if n + 1 > top():
            return None
        v = n + 1
        w = [n - 1, n + 10, int(str(n // 10) + str(n % 10 + 1)) if n % 10 == 9 else n + 2]
        return mcq("Quel nombre vient juste après %s ?" % num(n), num(v), [num(x) for x in w if x > 0 and x != v],
                   "Juste après, c’est 1 de plus : %s + 1 = <b>%s</b>." % (num(n), num(v)))
    v = n - 1
    w = [n + 1, n - 10, n // 10 * 10 + 9 if n % 10 == 0 and n >= 10 else n - 2]
    return mcq("Quel nombre vient juste avant %s ?" % num(n), num(v), [num(x) for x in w if x > 0 and x != v],
               "Juste avant, c’est 1 de moins : %s − 1 = <b>%s</b>." % (num(n), num(v)))


def s2():
    step = R.choice([2, 10, 10, 5] if L == 0 else [2, 5, 10, 100, 100])
    start = R.randint(0, 60) if L == 0 else R.randint(0, 600)
    if step == 5:
        start = start // 5 * 5
    if step == 2 and L == 0:
        start = R.randint(0, 40)
    seq = [start + i * step for i in range(5)]
    if seq[-1] > top():
        return None
    down = L == 1 and R.random() < 0.3
    if down:
        seq = seq[::-1]
    nxt = seq[-1] + (-step if down else step)
    if nxt < 0:
        return None
    sgn = -1 if down else 1
    w = [seq[-1] + sgn * 1, seq[-1] + sgn * 2 * step, seq[-1] + sgn * (10 if step != 10 else 100 if L else 1)]
    return mcq("Continue la suite : %s, …" % ", ".join(num(v) for v in seq[:4]), num(seq[4]) if False else num(seq[4]), [num(seq[3] + sgn * x) for x in (1, 2 * step, step + 1)],
               "On %s %d à chaque fois : %s %s %d = <b>%s</b>." % ("enlève" if down else "ajoute", step, num(seq[3]), "−" if down else "+", step, num(seq[4])))


def s3():
    step = 1 if L == 0 or R.random() < 0.4 else R.choice([10, 2])
    n = R.randint(5, 95) if L == 0 else R.randint(105, 995)
    if R.random() < 0.5:
        seq = [n + i * step for i in range(5)]
    else:
        seq = [n - i * step for i in range(5)]
    if min(seq) < 0 or max(seq) > top():
        return None
    i = R.randint(1, 3)
    v = seq[i]
    shown = ", ".join("…" if j == i else num(x) for j, x in enumerate(seq))
    d = seq[1] - seq[0]
    return mcq("Quel nombre manque ? %s" % shown, num(v), [num(seq[i - 1]), num(seq[i + 1]), num(v + 10 if d in (1, -1) else v + 1)],
               "On %s %d à chaque fois : le nombre qui manque est <b>%s</b>." % ("ajoute" if d > 0 else "enlève", abs(d), num(v)))


def s4_rang():
    n = R.randint(5, 8)
    a, b = R.sample(KINDS, 2)
    i = R.randrange(n)
    kinds = [a] * n
    kinds[i] = b
    svg = KP.kinds_row_svg(kinds)
    return mcq("<div class='qfig'>%s</div>En partant de la gauche, à quelle place est %s ?" % (pic(svg, "une rangée d’objets"), le(b)),
               rang(i + 1), [rang(i) if i else rang(n), rang(i + 2), rang(n - i) if n - i != i + 1 else rang(i + 3)],
               "On compte depuis la gauche : 1<sup>er</sup>, 2<sup>e</sup>… Il est <b>%s</b>." % rang(i + 1))


def s4_motif():
    pat = R.sample(KINDS, R.choice([2, 3]))
    if R.random() < 0.3 and len(pat) == 2:
        pat = [pat[0], pat[0], pat[1]]
    L_ = R.randint(5, 8)
    seq = [pat[i % len(pat)] for i in range(L_ + 1)]
    svg = KP.kinds_row_svg(seq[:L_])
    ans = seq[L_]
    others = [k for k in dict.fromkeys(pat) if k != ans] + [k for k in KINDS if k not in pat]
    return mcq("<div class='qfig'>%s</div>Quel objet vient ensuite ?" % pic(svg, "une suite d’objets qui se répète"), un(ans), [un(k) for k in others[:3]],
               "Le motif se répète : %s. Ensuite vient <b>%s</b>." % (", ".join(un(k) for k in pat), un(ans)))


def s4_pair():
    n = R.randint(10, 999)
    k = R.choice(["is", "which", "next"])
    if k == "is":
        ans = "pair" if n % 2 == 0 else "impair"
        return mcq("%s est-il pair ou impair ?" % num(n), ans, ["impair" if ans == "pair" else "pair", "les deux", "on ne peut pas savoir"],
                   "On regarde le chiffre des unités : %d. %s est <b>%s</b>." % (n % 10, num(n), ans))
    if k == "which":
        want = R.choice(["pair", "impair"])
        good = n if (n % 2 == 0) == (want == "pair") else n + 1
        bads = [good + 1, good + 3, good - 1 if good > 10 else good + 5]
        return mcq("Lequel est un nombre %s ?" % want, num(good), [num(x) for x in bads],
                   "Un nombre pair se termine par 0, 2, 4, 6 ou 8. <b>%s</b> est %s." % (num(good), want))
    if n % 2:
        n += 1
    return mcq("Quel est le nombre pair qui vient juste après %s ?" % num(n), num(n + 2), [num(n + 1), num(n), num(n + 10)],
               "Les nombres pairs vont de 2 en 2 : %s, <b>%s</b>." % (num(n), num(n + 2)))


def s5():
    p = K.next()
    k = R.choice(["file", "saut", "dit", "monte"])
    if k == "file":
        n = R.randint(3, 15 if L == 0 else 20)
        return mcq("Dans la file, %s est %s. Combien d’enfants sont devant %s ?" % (p[0], rang(n), "elle" if p[1] == "elle" else "lui"), str(n - 1), [str(n), str(n + 1), str(n - 2) if n > 2 else str(n + 2)],
                   "%s est %s : il y a <b>%d</b> enfants devant (pas %d)." % (p[0], rang(n), n - 1, n))
    if k == "saut":
        step = 10 if L == 0 else R.choice([10, 100])
        a = R.randint(1, 9) if L == 0 else R.randint(1, 99)
        t = R.randint(3, 6 if L == 0 else 8)
        if a + t * step > top():
            return None
        return mcq("%s part de %s et compte de %d en %d. Il fait %d bonds. Où arrive-t-%s ?" % (p[0], num(a), step, step, t, p[1]) if p[1] == "il" else
                   "%s part de %s et compte de %d en %d. Elle fait %d bonds. Où arrive-t-elle ?" % (p[0], num(a), step, step, t),
                   num(a + t * step), [num(a + t), num(a + (t + 1) * step), num(a + (t - 1) * step)],
                   "%s, puis %d bonds de %d : <b>%s</b>." % (num(a), t, step, num(a + t * step)))
    if k == "dit":
        step = R.choice([2, 5, 10])
        x = R.randint(11, 99 if L == 0 else 300)
        yes = x % step == 0
        return mcq("%s compte de %d en %d en partant de 0. Va-t-%s dire %s ?" % (p[0], step, step, p[1], num(x)), "oui" if yes else "non", ["non" if yes else "oui", "seulement s’%s compte à rebours" % p[1], "on ne peut pas savoir"],
                   "De %d en %d depuis 0, on dit les nombres %s. %s : <b>%s</b>." % (step, step, {2: "pairs", 5: "qui finissent par 0 ou 5", 10: "qui finissent par 0"}[step], num(x), "oui" if yes else "non"))
    n = R.randint(20, 90) if L == 0 else R.randint(200, 900)
    t = R.randint(3, 9)
    return mcq("%s compte à rebours de 1 en 1 à partir de %s. %s recule de %d nombres. Où arrive-t-%s ?" % (p[0], num(n), p[1].capitalize(), t, p[1]), num(n - t), [num(n + t), num(n - t + 1), num(n - 10 * t) if n - 10 * t > 0 else num(n - t - 1)],
               "À rebours, on enlève 1 à chaque nombre : %s − %d = <b>%s</b>." % (num(n), t, num(n - t)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Juste avant, juste après", mix(R, seen, [(s1, 20)])),
        ("Compter de 2 en 2, de 10 en 10" if lv == 0 else "Compter de 2, 5, 10 ou 100 en 100", mix(R, seen, [(s2, 20)])),
        ("Le nombre qui manque", mix(R, seen, [(s3, 20)])),
        ("Rangs et motifs" if lv == 0 else "Pair et impair, rangs", mix(R, seen, [(s4_rang, 10), (s4_motif, 10)] if lv == 0 else [(s4_pair, 14), (s4_rang, 6)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    th = ["Juste après un nombre, il y a 1 de plus ; juste avant, 1 de moins.",
          "Compter de 10 en 10 : seul le chiffre des dizaines change (7, 17, 27…).",
          "Le 3<sup>e</sup> d’une file a 2 personnes devant lui."]
    if lv == 1:
        th = ["Après 199 vient 200 ; après 309 vient 310.",
              "Compter de 100 en 100 : seul le chiffre des centaines change (45, 145, 245…).",
              "Un nombre <b>pair</b> se termine par 0, 2, 4, 6 ou 8 ; sinon il est <b>impair</b>."]
    body = lesson(th, [example("Continue : 23, 33, 43, …", ["+10 à chaque fois"], "53")] if lv == 0 else [example("Continue : 145, 245, 345, …", ["+100 à chaque fois"], "445")],
                  [["Après 39, écrire 310", "39 + 1 = 40 : 4 dizaines."],
                   ["Compter de 10 en 10 en ajoutant 1", "Le chiffre des dizaines augmente de 1, pas celui des unités."],
                   ["Croire que le 5<sup>e</sup> a 5 personnes devant lui", "Il en a 4 : on ne se compte pas soi-même."]])
    faq = [("Comment compter de 10 en 10 ?", "On ajoute 1 au chiffre des dizaines : 6, 16, 26, 36…"),
           ("Qu’est-ce qu’un motif qui se répète ?" if lv == 0 else "Comment savoir si un nombre est pair ?",
            "Une suite où le même groupe d’objets revient toujours dans le même ordre." if lv == 0 else "On regarde seulement le chiffre des unités : 0, 2, 4, 6, 8 → pair.")]
    unit(lv, R, "compter-et-suites" if lv == 0 else "compter-pair-et-impair", "N",
         ("Compter de 1 en 1, de 2 en 2, de 10 en 10, en avançant et en reculant ; connaître les nombres ordinaux ; reconnaître et continuer des suites qui se répètent" if lv == 0 else
          "Compter de 1 en 1, de 2 en 2, de 5 en 5, de 10 en 10 et de 100 en 100 jusqu’à 999 ; nombres pairs et impairs ; nombres ordinaux"),
         "Compter et suites de nombres" if lv == 0 else "Compter, pair et impair", "Compter et suites" if lv == 0 else "Compter, pair et impair",
         ("Fiches de maths CP pour compter : juste avant, juste après, de 2 en 2, de 10 en 10, le nombre qui manque, rangs, motifs et problèmes. 100 exercices corrigés." if lv == 0 else
          "Fiches de maths CE1 pour compter de 1, 2, 5, 10 et 100 en 100, trouver le nombre qui manque, pair et impair, rangs et problèmes. 100 exercices corrigés."),
         "Après 39 vient 40." if lv == 0 else "Après 199 vient 200.", "De 10 en 10 : 7, 17, 27, 37…" if lv == 0 else "Pair : se termine par 0, 2, 4, 6 ou 8.",
         body, faq, sets, 3)


if __name__ == "__main__":
    build(0)
