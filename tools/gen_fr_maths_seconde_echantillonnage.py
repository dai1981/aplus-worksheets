# -*- coding: utf-8 -*-
"""
France Maths Seconde : Échantillonnage (fréquence observée, fluctuation, loi des grands nombres, écart |f − p| ⩽ 1/√n, estimation)
  python3 tools/gen_fr_maths_seconde_echantillonnage.py
Erreurs : croire que la fréquence d’un échantillon est égale à p, 1/n au lieu de 1/√n, conclure trop vite sur un petit échantillon.
"""
import random
import math
from fr_c4 import *

R = random.Random(60520)
K = Kids(R)


def s1():
    n = R.choice([50, 100, 200, 400, 500, 1000, 2500])
    p = R.choice([Fr(1, 5), Fr(1, 4), Fr(3, 10), Fr(2, 5), Fr(1, 2), Fr(3, 5)])
    m = int(n * p) + R.randint(-n // 20, n // 20)
    k = R.choice(["freq", "freq", "ecart"])
    f = Fr(m, n)
    if k == "freq":
        return M("Dans un échantillon de %s pièces, %s sont défectueuses. Quelle est la fréquence observée de pièces défectueuses ?" % (num(n), num(m)), d(f) if (f * 10000).denominator == 1 else fq(f), [num(m), d(Fr(n - m, n)) if (Fr(n - m, n) * 10000).denominator == 1 else fq(Fr(n - m, n)), d(Fr(m, 100)) if n != 100 else d(Fr(m, 1000))],
                 "f = %s ÷ %s = <b>%s</b>." % (num(m), num(n), d(f) if (f * 10000).denominator == 1 else fq(f)))
    return M("La probabilité théorique est p = %s. Sur %s essais, la fréquence observée est f = %s. Quel est l’écart |f − p| ?" % (d(p), num(n), d(f)), d(abs(f - p)), [d(f - p) if f - p < 0 else d(f + p) if f + p <= 1 else d(abs(f - p) + Fr(1, 100)), d(p), d(abs(f - p) * n) if abs(f - p) * n <= n else "0"],
             "|%s − %s| = <b>%s</b>." % (d(f), d(p), d(abs(f - p))))


def s2():
    n = R.choice([25, 100, 400, 625, 2500, 10000])
    k = R.choice(["borne", "borne", "dans"])
    b = Fr(1, int(math.isqrt(n)))
    if k == "borne":
        return M("Pour un échantillon de taille n = %s, que vaut 1/√n ?" % num(n), d(b), [d(Fr(1, n)), d(Fr(2, int(math.isqrt(n)))), d(Fr(1, int(math.isqrt(n)) * 2)) if (Fr(1, int(math.isqrt(n)) * 2) * 10 ** 6).denominator == 1 else d(b * 10)],
                 "√%s = %d, donc 1/√n = <b>%s</b>." % (num(n), math.isqrt(n), d(b)))
    p = R.choice([Fr(1, 2), Fr(3, 10), Fr(2, 5), Fr(1, 4)])
    f = p + R.choice([1, -1]) * b * R.choice([Fr(1, 2), Fr(3, 2)])
    if not 0 < f < 1 or (f * 10000).denominator != 1:
        return None
    ok = abs(f - p) <= b
    return M("p = %s, n = %s et f = %s. L’écart |f − p| est-il inférieur ou égal à 1/√n ?" % (d(p), num(n), d(f)), "oui" if ok else "non", ["non" if ok else "oui", "on ne peut pas savoir", "seulement si n &gt; 1 000"],
             "|f − p| = %s et 1/√n = %s : <b>%s</b>." % (d(abs(f - p)), d(b), "oui" if ok else "non"))


def s3():
    V = [("Quand la taille de l’échantillon augmente, la fréquence observée…", "a tendance à se rapprocher de la probabilité", ["devient égale à 0,5", "s’éloigne de la probabilité", "ne change pas"]),
         ("Deux échantillons de même taille tirés dans la même population donnent…", "en général des fréquences différentes (fluctuation d’échantillonnage)", ["toujours la même fréquence", "toujours des fréquences opposées", "la probabilité exacte"]),
         ("On simule N échantillons de taille n. Environ quelle proportion vérifie |f − p| ⩽ 1/√n quand n est grand ?", "au moins 95 % des échantillons", ["environ 50 %", "exactement 100 %", "environ 5 %"]),
         ("Pour estimer la proportion de votants pour un candidat, on interroge…", "un échantillon aléatoire assez grand de la population", ["uniquement ses amis", "une seule personne", "les personnes d’un seul quartier"]),
         ("Une pièce donne 7 « pile » sur 10 lancers. Peut-on conclure qu’elle est truquée ?", "non : sur 10 lancers, une telle fréquence est fréquente", ["oui, car 0,7 ≠ 0,5", "oui, elle tombe trop souvent sur pile", "non, car 7 est impair"]),
         ("Que dit la loi des grands nombres ?", "la fréquence d’un événement se rapproche de sa probabilité quand le nombre d’essais augmente", ["un événement rare finit toujours par arriver", "après plusieurs « face », « pile » devient plus probable", "la probabilité dépend du nombre d’essais"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s3b():
    n = R.choice([100, 400, 625, 2500])
    f = Fr(R.randint(20, 80), 100)
    b = Fr(1, int(math.isqrt(n)))
    lo, hi = f - b, f + b
    return M("Sur un échantillon de taille %s, on observe une fréquence f = %s. Quel intervalle [f − 1/√n ; f + 1/√n] obtient-on pour estimer la proportion p ?" % (num(n), d(f)), "[%s ; %s]" % (d(lo), d(hi)), ["[%s ; %s]" % (d(f - Fr(1, n)), d(f + Fr(1, n))), "[%s ; %s]" % (d(f - 2 * b), d(f + 2 * b)), "[%s ; %s]" % (d(f), d(hi))],
             "1/√%s = %s : <b>[%s ; %s]</b>." % (num(n), d(b), d(lo), d(hi)))


def s4():
    p = R.choice([Fr(1, 2), Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 10)])
    n = R.choice([60, 120, 300, 600, 1200, 3000, 6000])
    k = R.choice(["att", "att", "sim"])
    if k == "att":
        return M("On répète %s fois une expérience de probabilité de succès %s. Combien de succès peut-on s’attendre à obtenir environ ?" % (num(n), fq(p)), num(n * p), [num(n * p * 2), num(n - n * p), num(int(n * p) + n // 10)], "%s × %s = <b>%s</b> (environ : la valeur fluctue)." % (num(n), fq(p), num(n * p)))
    V = [("En Python, random() renvoie…", "un nombre aléatoire de [0 ; 1[", ["un entier aléatoire entre 0 et 10", "toujours 0,5", "un nombre aléatoire de [0 ; 100["]),
         ("Pour simuler un succès de probabilité 0,3 en Python, on teste…", "random() &lt; 0.3", ["random() == 0.3", "random() &gt; 0.3", "randint(0, 3) == 1"]),
         ("Pour simuler un lancer de dé en Python, on utilise…", "randint(1, 6)", ["random(6)", "randint(0, 6)", "random() * 6"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s5():
    k = R.choice(["sondage", "sondage", "controle", "taille"])
    if k == "sondage":
        n = R.choice([400, 625, 2500])
        f = Fr(R.randint(35, 65), 100)
        b = Fr(1, int(math.isqrt(n)))
        return M("Dans un sondage auprès de %s personnes choisies au hasard, %s %% déclarent pratiquer un sport. Quelle estimation de la proportion réelle propose-t-on ?" % (num(n), d(f * 100)), "entre %s %% et %s %%" % (d((f - b) * 100), d((f + b) * 100)), ["exactement %s %%" % d(f * 100), "entre %s %% et %s %%" % (d((f - Fr(1, n)) * 100), d((f + Fr(1, n)) * 100)), "entre 0 %% et %s %%" % d(f * 100)],
                 "1/√%s = %s ; on propose [%s ; %s], soit <b>entre %s %% et %s %%</b>." % (num(n), d(b), d(f - b), d(f + b), d((f - b) * 100), d((f + b) * 100)))
    if k == "controle":
        p = Fr(R.choice([2, 3, 5]), 100)
        n = 400
        m = R.choice([int(n * p) + 2, int(n * p) + 40])
        f = Fr(m, n)
        ok = abs(f - p) <= Fr(1, 20)
        return M("Une usine annonce %s %% de pièces défectueuses. Sur 400 pièces prises au hasard, %d sont défectueuses. L’écart |f − p| dépasse-t-il 1/√n ?" % (d(p * 100), m), "non : l’annonce est compatible" if ok else "oui : l’annonce est douteuse", ["oui : l’annonce est douteuse" if ok else "non : l’annonce est compatible", "on ne peut pas savoir sans tout vérifier", "oui, car f ≠ p"],
                 "f = %s, |f − p| = %s et 1/√400 = 0,05 : <b>%s</b>." % (d(f), d(abs(f - p)), "l’écart reste dans la fluctuation" if ok else "l’écart est trop grand"))
    e = R.choice([Fr(1, 10), Fr(1, 20), Fr(1, 50), Fr(1, 100)])
    n = int(1 / (e * e))
    return M("Quelle taille d’échantillon faut-il pour que 1/√n = %s ?" % d(e), num(n), [num(int(1 / e)), num(n * 2), num(n // 2)], "1/√n = %s ⇔ √n = %d ⇔ <b>n = %s</b>." % (d(e), int(1 / e), num(n)))


def main():
    seen = set()
    sets = [("Fréquence observée", mix(R, seen, [(s1, 20)])), ("La borne 1/√n", mix(R, seen, [(s2, 20)])),
            ("Fluctuation et estimation", mix(R, seen, [(s3, 6), (s3b, 14)])), ("Simulation", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Un <b>échantillon</b> de taille n est formé de n répétitions indépendantes d’une expérience à deux issues. La fréquence observée f varie d’un échantillon à l’autre : c’est la <b>fluctuation d’échantillonnage</b>.",
              "Quand n est grand, f se rapproche de la probabilité p (loi des grands nombres) ; dans au moins 95 % des cas, |f − p| ⩽ 1/√n.",
              "On peut donc estimer une proportion inconnue p par l’intervalle [f − 1/√n ; f + 1/√n]."],
             [("n = 400, f = 0,42", ["1/√400 = 0,05"], "p ∈ [0,37 ; 0,47] (estimation)")],
             [["Croire que f = p", "f fluctue autour de p."], ["Utiliser 1/n au lieu de 1/√n", "Pour n = 400 : 1/√n = 0,05."], ["Conclure sur 10 essais", "Un petit échantillon fluctue beaucoup."]])
    faq = [("Pourquoi 1/√n ?", "C’est un ordre de grandeur de la fluctuation : pour diviser l’écart par 2, il faut multiplier la taille de l’échantillon par 4."),
           ("Est-ce une certitude ?", "Non : environ 95 % des échantillons vérifient |f − p| ⩽ 1/√n, pas tous.")]
    unit("seconde", R, "echantillonnage", "S",
         "Calculer une fréquence observée dans un échantillon ; comprendre la fluctuation d’échantillonnage et la loi des grands nombres ; utiliser la borne 1/√n pour estimer une proportion ou juger un écart ; simuler des échantillons",
         "Échantillonnage et estimation", "Échantillonnage",
         "Fiches de maths seconde sur l’échantillonnage : fréquence observée, fluctuation, loi des grands nombres, écart |f − p| ⩽ 1/√n, estimation et simulation. 100 exercices corrigés.",
         "|f − p| ⩽ 1/√n dans au moins 95 % des cas", "Estimation : [f − 1/√n ; f + 1/√n]", body, faq, sets, 20)


if __name__ == "__main__":
    main()
