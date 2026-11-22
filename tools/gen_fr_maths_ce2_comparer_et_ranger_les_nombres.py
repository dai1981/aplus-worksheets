# -*- coding: utf-8 -*-
"""
France Maths CE2 : Comparer et ranger les nombres (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_comparer_et_ranger_les_nombres.py
Signes < et >, ranger dans l’ordre croissant ou décroissant, encadrer à la centaine ou au millier, droite graduée,
le plus grand nombre avec des chiffres donnés.
Erreurs : comparer le dernier chiffre au lieu du premier, inverser < et >, lire la graduation de 1 en 1 au lieu de 10 en 10.
"""
import random
from fr_c2 import pl
from fr_common import mcq, num, lesson, example, make_unit, mix, droite

R = random.Random(51002)


def pair():
    a = R.randint(1000, 9999)
    k = R.random()
    if k < 0.4:
        b = int(str(a)[:2] + str(R.randint(0, 99)).rjust(2, "0"))
    elif k < 0.7:
        b = int(str(a)[::-1]) if str(a)[-1] != "0" else a + 90
    else:
        b = R.randint(100, 999)
    return (a, b) if a != b else None


def s1_signe():
    p = pair()
    if not p:
        return None
    a, b = p if R.random() < 0.5 else p[::-1]
    sg = "&lt;" if a < b else "&gt;"
    return mcq("Quel signe faut-il mettre ? %s … %s" % (num(a), num(b)), sg, ["&gt;" if sg == "&lt;" else "&lt;", "=", "on ne peut pas savoir"],
               "%s Donc %s <b>%s</b> %s." % ("Le nombre qui a le plus de chiffres est le plus grand." if len(str(a)) != len(str(b)) else
                                          "On compare les chiffres de gauche à droite : le premier chiffre différent décide.", num(a), sg, num(b)))


def s1_plusgrand():
    base = R.randint(1, 9) * 1000 + R.randint(0, 9) * 100
    xs = set()
    while len(xs) < 4:
        xs.add(base + R.choice([R.randint(0, 99), R.randint(10, 99) * 10 % 1000]))
    xs = list(xs)
    if R.random() < 0.5:
        r = max(xs)
        return mcq("Quel est le plus grand nombre : %s ?" % ", ".join(num(x) for x in xs), num(r), [num(x) for x in xs if x != r], "Les milliers et les centaines sont les mêmes : on regarde les dizaines puis les unités. <b>%s</b>." % num(r))
    r = min(xs)
    return mcq("Quel est le plus petit nombre : %s ?" % ", ".join(num(x) for x in xs), num(r), [num(x) for x in xs if x != r], "On compare chiffre par chiffre depuis la gauche : <b>%s</b>." % num(r))


def s2_ranger():
    xs = sorted(R.sample(range(1000, 9999), 4))
    if R.random() < 0.5:
        xs = sorted({xs[0], xs[0] // 1000 * 1000 + R.randint(0, 999), xs[2], xs[3]})
        if len(xs) < 4:
            return None
    show = xs[:]
    R.shuffle(show)
    cr = R.random() < 0.5
    right = (" &lt; " if cr else " &gt; ").join(num(x) for x in (xs if cr else xs[::-1]))
    w = []
    for _ in range(6):
        t = xs[:] if cr else xs[::-1]
        i = R.randrange(3)
        t[i], t[i + 1] = t[i + 1], t[i]
        w.append((" &lt; " if cr else " &gt; ").join(num(x) for x in t))
    by_last = sorted(xs, key=lambda x: x % 10)
    w.insert(0, (" &lt; " if cr else " &gt; ").join(num(x) for x in (by_last if cr else by_last[::-1])))
    return mcq("Range dans l’ordre %s : %s." % ("croissant" if cr else "décroissant", ", ".join(num(x) for x in show)), right, w,
               "Ordre %s = du %s : <b>%s</b>." % ("croissant" if cr else "décroissant", "plus petit au plus grand" if cr else "plus grand au plus petit", right))


def s3_encadrer():
    n = R.randint(1001, 9989)
    if n % 100 == 0:
        return None
    if R.random() < 0.5:
        lo = n // 100 * 100
        return mcq("Encadre %s entre deux centaines qui se suivent." % num(n), "%s &lt; %s &lt; %s" % (num(lo), num(n), num(lo + 100)),
                   ["%s &lt; %s &lt; %s" % (num(lo - 100), num(n), num(lo)), "%s &lt; %s &lt; %s" % (num(n // 10 * 10), num(n), num(n // 10 * 10 + 10)),
                    "%s &lt; %s &lt; %s" % (num(n // 1000 * 1000), num(n), num(n // 1000 * 1000 + 1000))],
                   "%s a %s centaines : il est entre <b>%s et %s</b>." % (num(n), num(n // 100), num(lo), num(lo + 100)))
    lo = n // 1000 * 1000
    return mcq("Encadre %s entre deux milliers qui se suivent." % num(n), "%s &lt; %s &lt; %s" % (num(lo), num(n), num(lo + 1000)),
               ["%s &lt; %s &lt; %s" % (num(n // 100 * 100), num(n), num(n // 100 * 100 + 100)), "%s &lt; %s &lt; %s" % (num(lo - 1000) if lo > 1000 else "0", num(n), num(lo)),
                "%s &lt; %s &lt; %s" % (num(lo + 1000), num(n), num(lo + 2000))],
               "Le chiffre des milliers est %d : %s est entre <b>%s et %s</b>." % (n // 1000, num(n), num(lo), num(lo + 1000)))


def s3_arrondi():
    n = R.randint(1010, 9940)
    if n % 100 == 50:
        return None
    near = (n + 50) // 100 * 100
    return mcq("Quelle est la centaine la plus proche de %s ?" % num(n), num(near), [num(near + 100) if near < n else num(near - 100), num(n // 10 * 10), num((n + 500) // 1000 * 1000)],
               "%s est entre %s et %s. Il est plus près de <b>%s</b>." % (num(n), num(n // 100 * 100), num(n // 100 * 100 + 100), num(near)))


def s4_droite():
    step = R.choice([10, 100, 1000])
    if step == 1000:
        lo, n = 0, 10
    else:
        lo = R.randint(1, 9) * 1000 + (R.randint(0, 9) * 100 if step == 10 else 0)
        n = 10
    hi = lo + step * n
    k = R.randint(1, 9)
    v = lo + k * step
    return mcq(droite(lo, hi, step, marks=[(v, "A")], labels=[lo, hi], every=step * 5) + "Quel nombre est au point A ?", num(v),
               [num(lo + k), num(lo + k * step // 10) if step > 10 else num(lo + k * 100), num(v + step), num(v - step)],
               "Entre %s et %s il y a %d graduations : chacune vaut %s. A est à %s de %s : <b>%s</b>." % (num(lo), num(hi), n, num(step), pl(k, "graduation"), num(lo), num(v)))


def s5_chiffres():
    ds = R.sample(range(0, 10), 4)
    if 0 in ds and R.random() < 0.7:
        pass
    big = "".join(map(str, sorted(ds, reverse=True)))
    small_list = sorted(ds)
    if small_list[0] == 0:
        i = next(i for i, d in enumerate(small_list) if d)
        small_list = [small_list[i]] + small_list[:i] + small_list[i + 1:]
    small = "".join(map(str, small_list))
    if R.random() < 0.5:
        return mcq("Avec les chiffres %s (une seule fois chacun), quel est le plus grand nombre de 4 chiffres ?" % ", ".join(map(str, ds)), num(int(big)),
                   [num(int(small)), num(int(big[0] + big[2] + big[1] + big[3])), num(int(big[1] + big[0] + big[2] + big[3])) if big[1] != "0" else num(int(big[0] + big[1] + big[3] + big[2]))],
                   "On met le plus grand chiffre aux milliers, puis le suivant aux centaines… : <b>%s</b>." % num(int(big)))
    wrong0 = "".join(map(str, sorted(ds)))
    return mcq("Avec les chiffres %s (une seule fois chacun), quel est le plus petit nombre de 4 chiffres ?" % ", ".join(map(str, ds)), num(int(small)),
               [num(int(big)), num(int(wrong0)) if wrong0[0] != "0" else num(int(small[0] + small[2] + small[1] + small[3])), num(int(small[0] + small[1] + small[3] + small[2]))],
               "On met le plus petit chiffre aux milliers (mais pas 0, sinon le nombre n’a que 3 chiffres) : <b>%s</b>." % num(int(small)))


def s5_prob():
    places = [("Lyon", "Lille"), ("Nice", "Brest"), ("Dijon", "Nantes"), ("Rouen", "Metz"), ("Tours", "Caen")]
    a, b = R.choice(places)
    x, y = R.sample(range(1200, 9800), 2)
    what = R.choice(["spectateurs au match de", "livres à la bibliothèque de", "coureurs au marathon de"])
    big = a if x > y else b
    return mcq("Il y a %s %s %s et %s %s %s. Où y en a-t-il le plus ?" % (num(x), what, a, num(y), what, b), big, [b if big == a else a, "autant dans les deux villes", "on ne peut pas savoir"],
               "%s %s %s, donc <b>%s</b>." % (num(max(x, y)), "&gt;", num(min(x, y)), big))


def main():
    seen = set()
    sets = [
        ("Comparer avec < et >", mix(R, seen, [(s1_signe, 12), (s1_plusgrand, 8)])),
        ("Ranger les nombres", mix(R, seen, [(s2_ranger, 20)])),
        ("Encadrer et arrondir", mix(R, seen, [(s3_encadrer, 12), (s3_arrondi, 8)])),
        ("La droite graduée", mix(R, seen, [(s4_droite, 20)])),
        ("Chiffres et problèmes", mix(R, seen, [(s5_chiffres, 12), (s5_prob, 8)])),
    ]
    body = lesson(
        ["Le nombre qui a le <b>plus de chiffres</b> est le plus grand : 1 250 &gt; 987.",
         "S’ils ont autant de chiffres, on compare <b>de gauche à droite</b> : d’abord les milliers, puis les centaines…",
         "&lt; se lit « est plus petit que », &gt; se lit « est plus grand que ». La pointe montre le plus petit nombre.",
         "Ordre croissant : du plus petit au plus grand. Ordre décroissant : du plus grand au plus petit."],
        [example("Compare 4 538 et 4 583.", ["Milliers : 4 = 4. Centaines : 5 = 5. Dizaines : 3 &lt; 8."], "4 538 &lt; 4 583"),
         example("Encadre 6 472 entre deux centaines.", ["6 472 a 64 centaines."], "6 400 &lt; 6 472 &lt; 6 500")],
        [["Comparer les unités en premier", "Commence toujours par le chiffre de gauche."],
         ["Inverser &lt; et &gt;", "La pointe du signe montre le plus petit nombre."],
         ["Compter les graduations de 1 en 1", "Regarde d’abord combien vaut une graduation."]])
    faq = [("Comment retenir le sens de &lt; et &gt; ?", "Le côté ouvert est tourné vers le plus grand nombre, la pointe vers le plus petit."),
           ("Qu’est-ce qu’encadrer un nombre ?", "C’est trouver deux nombres, l’un plus petit et l’autre plus grand, par exemple les deux centaines qui l’entourent.")]
    faq = [(q.replace("&lt;", "<").replace("&gt;", ">"), a) for q, a in faq]
    make_unit(R, "comparer-et-ranger-les-nombres", "N",
              "Comparer, ranger et encadrer des nombres entiers jusqu’à 10 000 en utilisant les symboles =, < et > ; repérer et placer des nombres sur une demi-droite graduée de 1 en 1, de 10 en 10 ou de 100 en 100 (résumé du programme 2024 du cycle 2).",
              "Comparer et ranger les nombres jusqu’à 10 000", "Comparer et ranger les nombres CE2 : fiches et exercices avec corrigé", "Comparer et ranger les nombres",
              "Fiches de maths CE2 pour comparer et ranger les nombres jusqu’à 10 000 : signes < et >, ordre croissant et décroissant, encadrer, droite graduée. 100 exercices corrigés.",
              "On compare les nombres chiffre par chiffre, en partant de la gauche.", "La pointe de < ou > montre le plus petit nombre.",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
