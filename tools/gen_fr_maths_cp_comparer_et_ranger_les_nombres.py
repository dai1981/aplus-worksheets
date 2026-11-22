# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Comparer et ranger les nombres
  python3 tools/gen_fr_maths_cp_comparer_et_ranger_les_nombres.py
Erreurs : comparer le chiffre des unités (39 > 41), confondre &lt; et &gt;, ranger dans le mauvais sens.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, droite, pic, ch, KINDS, nom
import k_pics as KP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53002 + 100 * lv)
    K = Kids(R)


def pair():
    """deux nombres « pièges » : même dizaine ou chiffres inversés"""
    if L == 0:
        k = R.choice(["inv", "dz", "u"])
        a = R.randint(12, 98)
        if k == "inv" and a % 10 and a % 10 != a // 10:
            b = (a % 10) * 10 + a // 10
        elif k == "dz":
            b = a // 10 * 10 + R.choice([x for x in range(10) if x != a % 10])
        else:
            b = R.randint(max(10, a - 15), min(99, a + 15))
    else:
        k = R.choice(["inv", "c", "d"])
        a = R.randint(102, 989)
        if k == "inv" and a % 10 and a % 10 != a // 100:
            b = int(str(a)[::-1])
        elif k == "c":
            b = a // 100 * 100 + R.randint(0, 99)
        else:
            b = R.randint(max(100, a - 120), min(999, a + 120))
    if a == b:
        return None
    return a, b


def s1():
    if L == 0 and R.random() < 0.5:
        a, b = R.sample(range(6, 21), 2)
        kind = R.choice(KINDS)
        top = KP.row_svg(a, kind)
        bot = KP.row_svg(b, kind)
        q = "<div class='qfig'>%s</div><div class='qfig'>%s</div>Où y a-t-il le plus %s ?" % (pic(top, "rangée du haut"), pic(bot, "rangée du bas"), ("de " if nom(kind)[0] not in "aeiouéœ" else "d’") + nom(kind))
        return mcq(q, "en haut" if a > b else "en bas", ["en bas" if a > b else "en haut", "autant en haut et en bas", "on ne peut pas savoir"],
                   "En haut : %d. En bas : %d. %d &gt; %d, donc <b>%s</b>." % (a, b, max(a, b), min(a, b), "en haut" if a > b else "en bas"))
    p = pair()
    if not p:
        return None
    a, b = p
    big = R.random() < 0.6
    ans = max(a, b) if big else min(a, b)
    return mcq("Quel est le plus %s nombre : %s ou %s ?" % ("grand" if big else "petit", num(a), num(b)), num(ans), [num(min(a, b) if big else max(a, b)), "ils sont égaux", "on ne peut pas savoir"],
               "On compare d’abord %s : %s est le plus %s." % ("les dizaines" if L == 0 else "les centaines, puis les dizaines", num(ans), "grand" if big else "petit"))


def s2():
    p = pair()
    if not p:
        return None
    a, b = p
    if R.random() < 0.6:
        good = "%s &lt; %s" % (num(min(a, b)), num(max(a, b))) if R.random() < 0.5 else "%s &gt; %s" % (num(max(a, b)), num(min(a, b)))
        bads = ["%s &gt; %s" % (num(min(a, b)), num(max(a, b))), "%s &lt; %s" % (num(max(a, b)), num(min(a, b))), "%s = %s" % (num(a), num(b))]
        return mcq("Quelle écriture est vraie ?", good, bads,
                   "%s est plus petit que %s. La pointe de &lt; ou &gt; montre le plus petit nombre : <b>%s</b>." % (num(min(a, b)), num(max(a, b)), good))
    x = a
    if R.random() < 0.5:
        ok = [v for v in range(x + 1, min(x + 30, 100 if L == 0 else 1000))]
        if not ok:
            return None
        g = R.choice(ok)
        bad = [x - R.randint(1, 9), x, x - 10 if x > 20 else x - 2]
        return mcq("Quel nombre peut-on écrire ? %s &lt; …" % num(x), num(g), [num(v) for v in bad if v > 0],
                   "Il faut un nombre plus grand que %s : <b>%s</b> convient (%s est égal, il ne convient pas)." % (num(x), num(g), num(x)))
    g = x - R.randint(1, 9)
    if g <= 0:
        return None
    return mcq("Quel nombre peut-on écrire ? %s &gt; …" % num(x), num(g), [num(x), num(x + R.randint(1, 9)), num(x + 10)],
               "Il faut un nombre plus petit que %s : <b>%s</b>." % (num(x), num(g)))


def s3():
    lo, hi = (10, 99) if L == 0 else (100, 999)
    base = R.randint(lo, hi)
    xs = set([base])
    while len(xs) < 4:
        v = R.choice([base % 10 * 10 + base // 10 if L == 0 else int(str(base)[::-1]), base + R.randint(-15, 15), base // 10 * 10 + R.randint(0, 9), R.randint(lo, hi)])
        if lo <= v <= hi:
            xs.add(v)
    xs = sorted(xs)
    up = R.random() < 0.5
    good = xs if up else xs[::-1]
    sh = list(xs)
    R.shuffle(sh)
    if sh == good:
        sh = sh[::-1]
    by_u = sorted(xs, key=lambda v: (v % 10, v))
    bads = [xs[::-1] if up else xs, by_u if up else by_u[::-1], [good[0], good[2], good[1], good[3]]]
    fmt = lambda l: (" &lt; " if up else " &gt; ").join(num(v) for v in l)
    return mcq("Range dans l’ordre %s : %s" % ("croissant (du plus petit au plus grand)" if up else "décroissant (du plus grand au plus petit)", ", ".join(num(v) for v in sh)),
               fmt(good), [fmt(b) for b in bads if b != good], "Ordre %s : <b>%s</b>." % ("croissant" if up else "décroissant", fmt(good)))


def s4():
    if R.random() < 0.5:
        if L == 0:
            lo = R.choice(range(0, 81, 10))
            step, hi = 1, lo + 20
        else:
            lo = R.choice(range(0, 901, 100))
            step, hi = 10, lo + 100
            if hi > 1000:
                return None
        v = lo + step * R.randint(1, (hi - lo) // step - 1)
        if (v - lo) % (step * 10) == 0:
            return None
        svg = droite(lo, hi, step, marks=[(v, "A")], every=step * 5 if L == 0 else step * 5)
        return mcq("<div class='qfig'>%s</div>Quel nombre est sous la lettre A ?" % svg, num(v), [num(v + step), num(v - step), num(lo + (v - lo) // step) if L == 1 else num(v + 10)],
                   "On compte les graduations de %s en %s à partir de %s : <b>%s</b>." % (step, step, num(lo), num(v)))
    if L == 0:
        n = R.randint(11, 99)
        if n % 10 == 0:
            return None
        a = n // 10 * 10
        return mcq("%d est entre quelles dizaines ?" % n, "%d et %d" % (a, a + 10), ["%d et %d" % (n, n + 1), "%d et %d" % (a - 10, a) if a > 10 else "%d et %d" % (a + 10, a + 20), "%d et %d" % (n % 10 * 10, n % 10 * 10 + 10) if n % 10 != n // 10 else "%d et %d" % (a + 10, a + 20)],
                   "%d = %s et %s. Il est entre <b>%d et %d</b>." % (n, pl(n // 10, "dizaine"), pl(n % 10, "unité"), a, a + 10))
    n = R.randint(101, 999)
    if R.random() < 0.5:
        if n % 100 == 0:
            return None
        a = n // 100 * 100
        return mcq("%s est entre quelles centaines ?" % num(n), "%d et %d" % (a, a + 100), ["%d et %d" % (n // 10 * 10, n // 10 * 10 + 10), "%d et %d" % (a - 100, a) if a > 100 else "%d et %d" % (a + 100, a + 200), "%d et %d" % (a + 100, a + 200) if a < 800 else "%d et %d" % (a - 200, a - 100)],
                   "%s a %s : il est entre <b>%d et %d</b>." % (num(n), pl(n // 100, "centaine"), a, a + 100))
    if n % 10 == 0:
        return None
    a = n // 10 * 10
    return mcq("%s est entre quelles dizaines ?" % num(n), "%s et %s" % (num(a), num(a + 10)), ["%s et %s" % (num(n // 100 * 100), num(n // 100 * 100 + 100)), "%s et %s" % (num(n), num(n + 1)), "%s et %s" % (num(a + 10), num(a + 20))],
               "Le chiffre des dizaines de %s est %d : il est entre <b>%s et %s</b>." % (num(n), n // 10 % 10, num(a), num(a + 10)))


def s5():
    a, b = K.two()
    k = R.choice(["qui", "chiffres", "score"])
    if k == "qui":
        p = pair()
        if not p:
            return None
        x, y = p
        thing = R.choice(["cartes", "billes", "images", "points"] if L == 0 else ["points", "timbres", "perles", "pas"])
        win = a[0] if x > y else b[0]
        return mcq("%s a %s %s. %s en a %s. Qui en a le plus ?" % (a[0], num(x), thing, b[0], num(y)), win, [b[0] if x > y else a[0], "ils en ont autant", "on ne peut pas savoir"],
                   "%s %s %s, donc <b>%s</b> en a le plus." % (num(max(x, y)), "&gt;", num(min(x, y)), win))
    if k == "chiffres":
        ds = R.sample(range(1, 10), 2 if L == 0 else 3)
        big = R.random() < 0.5
        s = sorted(ds, reverse=big)
        ans = int("".join(map(str, s)))
        other = int("".join(map(str, sorted(ds, reverse=not big))))
        mid = int("".join(map(str, ds))) if int("".join(map(str, ds))) not in (ans, other) else ans + 1
        return mcq("Avec les chiffres %s, quel est le plus %s nombre possible (chaque chiffre une fois) ?" % (" et ".join(map(str, ds)) if L == 0 else "%d, %d et %d" % tuple(ds), "grand" if big else "petit"),
                   num(ans), [num(other), num(mid), num(sum(ds))],
                   "On met le plus %s chiffre à gauche : <b>%s</b>." % ("grand" if big else "petit", num(ans)))
    xs = R.sample(range(20 if L == 0 else 200, 99 if L == 0 else 999), 3)
    ns = [a[0], b[0], K.next()[0]]
    if len(set(ns)) < 3:
        return None
    i = xs.index(max(xs))
    return mcq("Au jeu, %s a %s points, %s a %s points et %s a %s points. Qui a gagné (le plus de points) ?" % (ns[0], num(xs[0]), ns[1], num(xs[1]), ns[2], num(xs[2])), ns[i],
               [ns[j] for j in range(3) if j != i] + ["personne"], "Le plus grand nombre est %s : <b>%s</b> a gagné." % (num(max(xs)), ns[i]))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Le plus grand, le plus petit", mix(R, seen, [(s1, 20)])),
        ("Les signes &lt; et &gt;", mix(R, seen, [(s2, 20)])),
        ("Ranger des nombres", mix(R, seen, [(s3, 20)])),
        ("Droite graduée et encadrement", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    if lv == 0:
        ex = example("Compare 47 et 52", ["4 dizaines &lt; 5 dizaines"], "47 &lt; 52")
        th = ["On compare d’abord les <b>dizaines</b>. Si elles sont égales, on compare les unités.",
              "&lt; veut dire « plus petit que », &gt; veut dire « plus grand que ». La pointe montre le plus petit.",
              "Ordre croissant : du plus petit au plus grand."]
    else:
        ex = example("Compare 386 et 412", ["3 centaines &lt; 4 centaines"], "386 &lt; 412")
        th = ["On compare d’abord les <b>centaines</b>, puis les dizaines, puis les unités.",
              "&lt; veut dire « plus petit que », &gt; veut dire « plus grand que ». La pointe montre le plus petit.",
              "Ordre croissant : du plus petit au plus grand ; décroissant : du plus grand au plus petit."]
    body = lesson(th, [ex], [["Regarder les unités d’abord : 39 &gt; 41", "On regarde d’abord les dizaines : 3 &lt; 4, donc 39 &lt; 41."],
                             ["Tourner le signe à l’envers", "La pointe est du côté du plus petit nombre : 12 &lt; 21."],
                             ["Ranger dans le mauvais sens", "Croissant, c’est en montant : le plus petit en premier."]])
    faq = [("Comment ne pas confondre &lt; et &gt; ?", "La pointe du signe montre toujours le plus petit nombre ; le côté ouvert est du côté du plus grand."),
           ("Que veut dire « ordre croissant » ?", "Ranger du plus petit au plus grand.")]
    unit(lv, R, "comparer-et-ranger-les-nombres", "N",
         "Comparer, ranger et encadrer des nombres entiers jusqu’à %s ; utiliser les symboles &lt;, &gt; et = ; repérer des nombres sur une droite graduée" % ("100" if lv == 0 else "1 000"),
         "Comparer et ranger les nombres", "Comparer et ranger les nombres",
         "Fiches de maths %s pour comparer et ranger les nombres jusqu’à %s : plus grand, plus petit, signes &lt; et &gt;, ordre croissant, droite graduée et problèmes. 100 exercices corrigés." % (GN(lv), "100" if lv == 0 else "1 000"),
         "On compare d’abord le chiffre de gauche.", "47 &lt; 52 car 4 dizaines &lt; 5 dizaines." if lv == 0 else "386 &lt; 412 car 3 centaines &lt; 4 centaines.",
         body, faq, sets, 2)


if __name__ == "__main__":
    build(0)
