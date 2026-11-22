# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Lunghezza della circonferenza e area del cerchio (Spazio e figure)
  python3 tools/gen_it_matematica_m3_lunghezza_della_circonferenza_e_area_del_cerchio.py
C = 2πr, A = πr² (risultati in funzione di π e con π ≈ 3,14), formule inverse (r dalla circonferenza e dall’area),
lunghezza di un arco e area di un settore (proporzione con l’angolo al centro), corona circolare, figure composte.
Errori: A = 2πr, usare il diametro nella formula dell’area, dimenticare di elevare al quadrato il raggio.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, d, num, Kids

R = random.Random(71309)
G = "terza-media"
K = Kids(R)
PI = Fr(314, 100)


def pi(k, u=""):
    k = Fr(k)
    s = "π" if k == 1 else "%sπ" % d(k)
    return s + ((" " + u) if u else "")


def s1_circ():
    r = R.randint(2, 25)
    if R.random() < 0.5:
        return M("Calcola la lunghezza della circonferenza di raggio %d cm (in funzione di π)." % r, pi(2 * r, "cm"), W(pi(r, "cm"), pi(r * r, "cm"), pi(4 * r, "cm"), pi(2 * r + 2, "cm")),
                 "C = 2πr = 2 × %d × π = <b>%s</b>." % (r, pi(2 * r, "cm")))
    dd = 2 * r
    return M("Calcola la lunghezza della circonferenza di diametro %d cm (usa π = 3,14)." % dd, "%s cm" % d(dd * PI), W("%s cm" % d(2 * dd * PI), "%s cm" % d(r * r * PI), "%s cm" % d(r * PI), "%s cm" % d(dd + PI)),
             "C = π × d = 3,14 × %d = <b>%s cm</b>." % (dd, d(dd * PI)))


def s1_area():
    r = R.randint(2, 20)
    if R.random() < 0.5:
        return M("Calcola l’area del cerchio di raggio %d cm (in funzione di π)." % r, pi(r * r, "cm²"), W(pi(2 * r, "cm²"), pi(4 * r * r, "cm²"), pi(r * r * 2, "cm²"), pi(r, "cm²")),
                 "A = πr² = π × %d² = <b>%s</b>." % (r, pi(r * r, "cm²")))
    dd = 2 * r
    return M("Calcola l’area del cerchio di diametro %d cm (usa π = 3,14)." % dd, "%s cm²" % d(r * r * PI), W("%s cm²" % d(dd * dd * PI), "%s cm²" % d(dd * PI), "%s cm²" % d(2 * r * PI * r * 2), "%s cm²" % d(r * PI), "%s cm²" % d(r * r), "%s cm²" % d(r * r * PI + 1)),
             "r = %d cm; A = 3,14 × %d² = 3,14 × %d = <b>%s cm²</b>." % (r, r, r * r, d(r * r * PI)))


def s2_inverse():
    r = R.randint(2, 30)
    k = R.choice(["rC", "rA", "rC314", "AdaC"])
    if k == "rC":
        return M("Una circonferenza è lunga %s. Quanto misura il raggio?" % pi(2 * r, "cm"), "%d cm" % r, W("%d cm" % (2 * r), "%d cm" % (r * r) if r * r < 1000 else None, "%s cm" % d(Fr(r, 2)), "%d cm" % (r + 1)), "r = C : 2π = %s : 2π = <b>%d cm</b>." % (pi(2 * r), r))
    if k == "rA":
        return M("Un cerchio ha area %s. Quanto misura il raggio?" % pi(r * r, "cm²"), "%d cm" % r, W("%d cm" % (r * r // 2) if r * r % 2 == 0 and r * r // 2 != r else "%d cm" % (r * 2), "%d cm" % (2 * r), "%d cm" % (r + 2), "%d cm" % (r * r) if r * r != r else None),
                     "r² = %d, quindi r = √%d = <b>%d cm</b>." % (r * r, r * r, r))
    if k == "rC314":
        C = 2 * r * PI
        return M("Una circonferenza è lunga %s cm. Quanto misura il raggio (π = 3,14)?" % d(C), "%d cm" % r, W("%d cm" % (2 * r), "%s cm" % d(C / PI), "%d cm" % (r + 1), "%s cm" % d(Fr(r, 2))), "r = %s : (2 × 3,14) = %s : 6,28 = <b>%d cm</b>." % (d(C), d(C), r))
    return M("Una circonferenza è lunga %s. Qual è l’area del cerchio?" % pi(2 * r, "cm"), pi(r * r, "cm²"), W(pi(4 * r * r, "cm²"), pi(2 * r, "cm²"), pi(r * r * 2, "cm²"), pi(r, "cm²")),
             "r = %s : 2π = %d cm; A = π × %d² = <b>%s</b>." % (pi(2 * r), r, r, pi(r * r, "cm²")))


def s3_arco():
    r = R.randint(2, 18)
    a = R.choice([30, 36, 40, 45, 60, 72, 90, 120, 135, 150, 180, 210, 240, 270, 300])
    k = R.choice(["arco", "settore", "angolo"])
    if k == "arco":
        l_ = Fr(2 * r * a, 360)
        return M("In una circonferenza di raggio %d cm, quanto è lungo l’arco che corrisponde a un angolo al centro di %d° (in funzione di π)?" % (r, a), pi(l_, "cm"), W(pi(Fr(r * r * a, 360), "cm"), pi(2 * r, "cm"), pi(Fr(r * a, 360), "cm"), pi(l_ * 2, "cm")),
                 "l = 2πr × α : 360 = %s × %d : 360 = <b>%s</b>." % (pi(2 * r), a, pi(l_, "cm")))
    if k == "settore":
        A = Fr(r * r * a, 360)
        return M("Calcola l’area del settore circolare con raggio %d cm e angolo al centro %d° (in funzione di π)." % (r, a), pi(A, "cm²"), W(pi(Fr(2 * r * a, 360), "cm²"), pi(r * r, "cm²"), pi(A * 2, "cm²"), pi(Fr(r * a, 360), "cm²")),
                 "A = πr² × α : 360 = %s × %d : 360 = <b>%s</b>." % (pi(r * r), a, pi(A, "cm²")))
    l_ = Fr(2 * r * a, 360)
    return M("In una circonferenza di raggio %d cm un arco è lungo %s. Quanto misura l’angolo al centro corrispondente?" % (r, pi(l_, "cm")), "%d°" % a, W("%d°" % (360 - a), "%d°" % (a // 2) if a % 2 == 0 else None, "%d°" % (a * 2) if a * 2 <= 360 else "%d°" % (a - 30), "%s°" % d(l_ * 10) if (l_ * 10).denominator == 1 and l_ * 10 != a else None),
             "α = l : C × 360 = %s : %s × 360 = <b>%d°</b>." % (pi(l_), pi(2 * r), a))


def s4_corona():
    R1 = R.randint(4, 20)
    r1 = R.randint(1, R1 - 1)
    k = R.choice(["corona", "corona314", "quadrato"])
    if k == "corona":
        return M("Calcola l’area della corona circolare con raggi %d cm e %d cm (in funzione di π)." % (R1, r1), pi(R1 * R1 - r1 * r1, "cm²"), W(pi((R1 - r1) ** 2, "cm²"), pi(R1 * R1 + r1 * r1, "cm²"), pi(2 * (R1 - r1), "cm²"), pi(R1 * R1, "cm²")),
                 "A = π(R² − r²) = π(%d − %d) = <b>%s</b>." % (R1 * R1, r1 * r1, pi(R1 * R1 - r1 * r1, "cm²")))
    if k == "corona314":
        return M("Un’aiuola a forma di corona circolare ha raggi %d m e %d m. Quanti m² misura (π = 3,14)?" % (R1, r1), "%s m²" % d((R1 * R1 - r1 * r1) * PI), W("%s m²" % d((R1 - r1) ** 2 * PI), "%s m²" % d((R1 * R1 + r1 * r1) * PI), "%s m²" % d(2 * (R1 - r1) * PI)),
                 "A = 3,14 × (%d − %d) = 3,14 × %d = <b>%s m²</b>." % (R1 * R1, r1 * r1, R1 * R1 - r1 * r1, d((R1 * R1 - r1 * r1) * PI)))
    l_ = R.randint(2, 20) * 2
    r = l_ // 2
    return M("In un quadrato di lato %d cm è inscritto un cerchio. Qual è l’area della parte di quadrato fuori dal cerchio (π = 3,14)?" % l_, "%s cm²" % d(l_ * l_ - r * r * PI), W("%s cm²" % d(l_ * l_ - l_ * l_ * PI) if l_ * l_ * PI < l_ * l_ else "%s cm²" % d(r * r * PI), "%s cm²" % d(l_ * l_ - 2 * r * PI), "%s cm²" % d(l_ * l_), "%s cm²" % d(r * r * PI)),
             "Quadrato: %d cm²; cerchio (r = %d): 3,14 × %d = %s cm²; differenza: <b>%s cm²</b>." % (l_ * l_, r, r * r, d(r * r * PI), d(l_ * l_ - r * r * PI)))


def s5():
    p = K.next()
    k = R.choice(["ruota", "pista", "pizza", "aiuola", "orologio"])
    if k == "ruota":
        dd = R.choice([50, 60, 64, 70, 80])
        n = R.choice([100, 200, 250, 500, 1000])
        C = dd * PI
        return M("La ruota di una bicicletta ha diametro %d cm. Quanti metri percorre facendo %d giri (π = 3,14)?" % (dd, n), "%s m" % d(C * n / 100), W("%s m" % d(C * n / 50), "%s m" % d(C * n / 1000), "%s m" % d(dd * n / Fr(100)), "%s m" % d((dd // 2) ** 2 * PI * n / 100)),
                 "Un giro: 3,14 × %d = %s cm; %d giri: %s cm = <b>%s m</b>." % (dd, d(C), n, d(C * n), d(C * n / 100)))
    if k == "pista":
        r = R.choice([10, 15, 20, 25, 30, 50])
        g = R.randint(2, 10)
        return M("%s corre %d giri intorno a una fontana circolare di raggio %d m. Quanti metri percorre (π = 3,14)?" % (p[0], g, r), "%s m" % d(2 * r * PI * g), W("%s m" % d(r * PI * g), "%s m" % d(r * r * PI * g), "%s m" % d(2 * r * PI), "%s m" % d(2 * r * g)),
                 "Un giro: 2 × 3,14 × %d = %s m; × %d = <b>%s m</b>." % (r, d(2 * r * PI), g, d(2 * r * PI * g)))
    if k == "pizza":
        d1, d2 = R.choice([(30, 40), (20, 30), (30, 45), (24, 36), (20, 40)])
        ratio = Fr(d2 * d2, d1 * d1)
        return M("Una pizza ha diametro %d cm, un’altra %d cm. Quante volte è più grande l’area della seconda?" % (d1, d2), d(ratio) if (ratio * 100).denominator == 1 else None, W(d(Fr(d2, d1)) if (Fr(d2, d1) * 100).denominator == 1 else None, d(ratio * 2) if (ratio * 200).denominator == 1 else None, str(d2 - d1), d(Fr(d2 - d1, d1) * 2) if (Fr(d2 - d1, d1) * 200).denominator == 1 else None, d(ratio + 1) if (ratio * 100).denominator == 1 else None),
                 "Le aree stanno come i quadrati dei diametri: (%d : %d)² = %s² = <b>%s</b>." % (d2, d1, d(Fr(d2, d1)), d(ratio))) if (ratio * 100).denominator == 1 and (Fr(d2, d1) * 100).denominator == 1 else None
    if k == "aiuola":
        r = R.randint(2, 10)
        pr = R.choice([2, 3, 4, 5])
        return M("Un’aiuola circolare ha raggio %d m. Per seminarla servono %d € al m². Quanto si spende (π = 3,14)?" % (r, pr), "%s €" % d(r * r * PI * pr) if (r * r * PI * pr * 100).denominator == 1 else None, W("%s €" % d(2 * r * PI * pr), "%s €" % d(4 * r * r * PI * pr), "%s €" % d(r * r * PI)),
                 "A = 3,14 × %d = %s m²; × %d = <b>%s €</b>." % (r * r, d(r * r * PI), pr, d(r * r * PI * pr)))
    l_ = R.choice([6, 8, 9, 10, 12, 15])
    m_ = R.choice([10, 15, 20, 30, 40, 45])
    a = m_ * 6
    return M("La lancetta dei minuti di un orologio è lunga %d cm. Quanti cm percorre la sua punta in %d minuti (in funzione di π)?" % (l_, m_), pi(Fr(2 * l_ * a, 360), "cm"), W(pi(2 * l_, "cm"), pi(Fr(l_ * l_ * a, 360), "cm"), pi(Fr(l_ * a, 360), "cm"), pi(Fr(2 * l_ * m_, 360), "cm")),
             "In %d minuti la lancetta ruota di %d°: l = %s × %d : 360 = <b>%s</b>." % (m_, a, pi(2 * l_), a, pi(Fr(2 * l_ * a, 360), "cm")))


def main():
    seen = set()
    sets = [
        ("Lunghezza della circonferenza", mix(R, seen, [(s1_circ, 20)])),
        ("Area del cerchio", mix(R, seen, [(s1_area, 14), (s2_inverse, 6)])),
        ("Formule inverse", mix(R, seen, [(s2_inverse, 20)])),
        ("Archi, settori e corone", mix(R, seen, [(s3_arco, 12), (s4_corona, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["La <b>lunghezza della circonferenza</b> è C = 2πr = πd. L’<b>area del cerchio</b> è A = πr². π ≈ 3,14 è il rapporto tra circonferenza e diametro.",
              "Spesso il risultato si scrive <b>in funzione di π</b> (per esempio 10π cm) e si sostituisce 3,14 solo alla fine.",
              "Arco e settore sono proporzionali all’angolo al centro α: l = C × α : 360°, A<sub>settore</sub> = A × α : 360°.",
              "<b>Corona circolare</b>: A = π(R² − r²)."],
             [("r = 5 cm", ["C = 2π × 5", "A = π × 5²"], "C = 10π cm, A = 25π cm²"), ("Settore di 90° con r = 4 cm", ["16π × 90 : 360"], "4π cm²")],
             [["A = 2πr", "2πr è la circonferenza; l’area è πr²."],
              ["Usare il diametro nell’area", "Prima dimezza: con d = 10 cm, r = 5 cm e A = 25π cm²."],
              ["π × 5² = (π × 5)²", "Si eleva al quadrato solo il raggio."]],
             table(["Che cosa", "Formula"], [["circonferenza", "C = 2πr"], ["area del cerchio", "A = πr²"], ["arco", "l = C × α : 360"], ["settore", "A × α : 360"], ["corona", "π(R² − r²)"]]))
    faq = [("Perché si lascia il risultato in funzione di π?", "Perché π ha infinite cifre decimali: scrivendo 10π il risultato è esatto; con 3,14 è approssimato."),
           ("Se il raggio raddoppia, l’area raddoppia?", "No: diventa 4 volte più grande, perché il raggio è elevato al quadrato.")]
    unit(G, R, "lunghezza-della-circonferenza-e-area-del-cerchio", "S",
         "Conoscere il numero π e alcuni modi per approssimarlo; calcolare l’area del cerchio e la lunghezza della circonferenza, conoscendo il raggio, e viceversa",
         "Lunghezza della circonferenza e area del cerchio", "Circonferenza e area del cerchio",
         "Schede di matematica per la terza media sulla lunghezza della circonferenza e l’area del cerchio: π, formule dirette e inverse, archi, settori circolari, corona circolare e problemi. 100 esercizi con soluzioni.",
         "C = 2πr; A = πr²", "Arco e settore: × α : 360°.",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
