# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Solidi di rotazione (Spazio e figure)
  python3 tools/gen_it_matematica_m3_solidi_di_rotazione.py
Solidi generati dalla rotazione di figure piane, cilindro (Al = 2πrh, At = 2πr(h + r), V = πr²h), cono (apotema con Pitagora,
Al = πra, At = πr(a + r), V = πr²h : 3), sfera (A = 4πr², V = 4/3 πr³), formule inverse e problemi (in funzione di π e con 3,14).
Errori: V del cono senza «: 3», usare l’altezza al posto dell’apotema nell’area laterale del cono, usare il diametro come raggio.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, d, num, Kids

R = random.Random(71311)
G = "terza-media"
K = Kids(R)
PI = Fr(314, 100)
TERNE = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25)]


def pi(k, u=""):
    k = Fr(k)
    s = "π" if k == 1 else "%sπ" % d(k)
    return s + ((" " + u) if u else "")


def s1_quiz():
    q, a, w = R.choice([
        ("Facendo ruotare un rettangolo attorno a un suo lato si ottiene…", "un cilindro", ["un cono", "una sfera", "un prisma"]),
        ("Facendo ruotare un triangolo rettangolo attorno a un cateto si ottiene…", "un cono", ["un cilindro", "una piramide", "una sfera"]),
        ("Facendo ruotare un semicerchio attorno al diametro si ottiene…", "una sfera", ["un cilindro", "un cono", "un cerchio"]),
        ("L’apotema di un cono è…", "il segmento dal vertice a un punto della circonferenza di base", ["l’altezza del cono", "il raggio di base", "il diametro di base"]),
        ("Lo sviluppo della superficie laterale di un cilindro è…", "un rettangolo", ["un cerchio", "un settore circolare", "un triangolo"]),
        ("Lo sviluppo della superficie laterale di un cono è…", "un settore circolare", ["un rettangolo", "un triangolo", "un cerchio"]),
        ("Un cono e un cilindro hanno la stessa base e la stessa altezza. Il volume del cono è…", "un terzo di quello del cilindro", ["la metà", "uguale", "il doppio"]),
        ("Un cilindro equilatero ha…", "l’altezza uguale al diametro di base", ["l’altezza uguale al raggio", "il raggio uguale a 1", "tutte le facce uguali"]),
        ("In un cono, altezza, raggio e apotema formano…", "un triangolo rettangolo con l’apotema come ipotenusa", ["un triangolo equilatero", "un triangolo rettangolo con l’altezza come ipotenusa", "un rettangolo"]),
        ("Se il raggio di una sfera raddoppia, il volume diventa…", "8 volte più grande", ["2 volte più grande", "4 volte più grande", "6 volte più grande"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s2_cil():
    r, h = R.randint(2, 12), R.randint(3, 20)
    if r == h:
        return None
    k = R.choice(["Al", "At", "V", "V314"])
    if k == "Al":
        return M("Un cilindro ha raggio %d cm e altezza %d cm. Calcola l’area laterale (in funzione di π)." % (r, h), pi(2 * r * h, "cm²"), W(pi(r * h, "cm²"), pi(r * r * h, "cm²"), pi(2 * r * h + 2 * r * r, "cm²"), pi(2 * r + h, "cm²")),
                 "Al = 2πr × h = 2π × %d × %d = <b>%s</b>." % (r, h, pi(2 * r * h, "cm²")))
    if k == "At":
        return M("Un cilindro ha raggio %d cm e altezza %d cm. Calcola l’area totale (in funzione di π)." % (r, h), pi(2 * r * h + 2 * r * r, "cm²"), W(pi(2 * r * h, "cm²"), pi(2 * r * h + r * r, "cm²"), pi(r * r * h, "cm²"), pi(2 * r * (h + 2 * r), "cm²")),
                 "Al = %s; 2Ab = 2π × %d = %s; At = <b>%s</b>." % (pi(2 * r * h), r * r, pi(2 * r * r), pi(2 * r * h + 2 * r * r, "cm²")))
    if k == "V":
        return M("Un cilindro ha raggio %d cm e altezza %d cm. Calcola il volume (in funzione di π)." % (r, h), pi(r * r * h, "cm³"), W(pi(2 * r * h, "cm³"), pi(Fr(r * r * h, 3), "cm³") if (Fr(r * r * h, 3) * 10).denominator == 1 else pi(r * h, "cm³"), pi(4 * r * r * h, "cm³"), pi(r * h, "cm³")),
                 "V = πr² × h = π × %d × %d = <b>%s</b>." % (r * r, h, pi(r * r * h, "cm³")))
    dd = 2 * r
    return M("Un barattolo cilindrico ha diametro %d cm e altezza %d cm. Calcola il volume (π = 3,14)." % (dd, h), "%s cm³" % d(r * r * h * PI), W("%s cm³" % d(dd * dd * h * PI), "%s cm³" % d(dd * h * PI), "%s cm³" % d(r * r * h * PI / 3)),
             "r = %d cm; V = 3,14 × %d × %d = <b>%s cm³</b>." % (r, r * r, h, d(r * r * h * PI)))


def s3_cono():
    r, h, a = R.choice(TERNE)
    if R.random() < 0.5:
        r, h = h, r
    k = R.choice(["apot", "Al", "At", "V"])
    if k == "apot":
        return M("Un cono ha raggio di base %d cm e altezza %d cm. Quanto misura l’apotema?" % (r, h), "%d cm" % a, W("%d cm" % (r + h), "%d cm" % (a + 1), "%d cm" % abs(h - r), "%d cm" % (a * a)), "a = √(%d² + %d²) = √%d = <b>%d cm</b>." % (r, h, a * a, a))
    if k == "Al":
        return M("Un cono ha raggio di base %d cm e apotema %d cm. Calcola l’area laterale (in funzione di π)." % (r, a), pi(r * a, "cm²"), W(pi(2 * r * a, "cm²"), pi(r * h, "cm²"), pi(r * a + r * r, "cm²"), pi(Fr(r * a, 2), "cm²")),
                 "Al = πr × a = π × %d × %d = <b>%s</b>." % (r, a, pi(r * a, "cm²")))
    if k == "At":
        return M("Un cono ha raggio di base %d cm e altezza %d cm. Calcola l’area totale (in funzione di π)." % (r, h), pi(r * a + r * r, "cm²"), W(pi(r * h + r * r, "cm²"), pi(r * a, "cm²"), pi(2 * r * a + r * r, "cm²"), pi(r * a + 2 * r * r, "cm²")),
                 "a = √(%d² + %d²) = %d cm; Al = π × %d × %d = %s; Ab = %s; At = <b>%s</b>." % (r, h, a, r, a, pi(r * a), pi(r * r), pi(r * a + r * r, "cm²")))
    V = Fr(r * r * h, 3)
    return M("Un cono ha raggio di base %d cm e altezza %d cm. Calcola il volume (in funzione di π)." % (r, h), pi(V, "cm³"), W(pi(r * r * h, "cm³"), pi(Fr(r * r * a, 3), "cm³") if (Fr(r * r * a, 3) * 10).denominator == 1 else pi(r * r * a, "cm³"), pi(Fr(r * h, 3), "cm³") if (Fr(r * h, 3) * 10).denominator == 1 else pi(r * h, "cm³"), pi(V * 2, "cm³")),
             "V = πr² × h : 3 = π × %d × %d : 3 = <b>%s</b>." % (r * r, h, pi(V, "cm³"))) if (V * 10).denominator == 1 else None


def s4_sfera():
    r = R.choice([1, 2, 3, 4, 5, 6, 9, 10, 12, 15])
    k = R.choice(["A", "V", "A2"])
    if k in ("A", "A2"):
        return M("Calcola l’area della superficie di una sfera di raggio %d cm (in funzione di π)." % r, pi(4 * r * r, "cm²"), W(pi(r * r, "cm²"), pi(2 * r * r, "cm²"), pi(Fr(4 * r ** 3, 3), "cm²") if (Fr(4 * r ** 3, 3)).denominator == 1 else pi(8 * r * r, "cm²"), pi(4 * r, "cm²")),
                 "A = 4πr² = 4π × %d = <b>%s</b>." % (r * r, pi(4 * r * r, "cm²")))
    V = Fr(4 * r ** 3, 3)
    if V.denominator != 1:
        return None
    return M("Calcola il volume di una sfera di raggio %d cm (in funzione di π)." % r, pi(V, "cm³"), W(pi(4 * r * r, "cm³"), pi(r ** 3, "cm³"), pi(4 * r ** 3, "cm³"), pi(Fr(4 * r * r, 3), "cm³") if Fr(4 * r * r, 3).denominator == 1 else pi(2 * r ** 3, "cm³")),
             "V = 4/3 πr³ = 4/3 × π × %d = <b>%s</b>." % (r ** 3, pi(V, "cm³")))


def s4_inverse():
    k = R.choice(["cil_h", "cono_h", "cil_r", "sfera_r"])
    if k == "cil_h":
        r, h = R.randint(2, 10), R.randint(3, 20)
        return M("Un cilindro ha volume %s e raggio %d cm. Quanto misura l’altezza?" % (pi(r * r * h, "cm³"), r), "%d cm" % h, W("%s cm" % d(Fr(r * r * h, r)), "%d cm" % (h * r) if h * r != h else None, "%s cm" % d(Fr(h, 2)), "%d cm" % (h + 1)) , "h = V : (πr²) = %s : %s = <b>%d cm</b>." % (pi(r * r * h), pi(r * r), h)) if r != 1 else None
    if k == "cono_h":
        r, h = R.randint(2, 10), R.randint(2, 12) * 3
        V = Fr(r * r * h, 3)
        return M("Un cono ha volume %s e raggio %d cm. Quanto misura l’altezza?" % (pi(V, "cm³"), r), "%d cm" % h, W("%d cm" % (h // 3), "%d cm" % (h * 3), "%s cm" % d(V / r), "%d cm" % (h + 3)), "h = V × 3 : (πr²) = %s × 3 : %s = <b>%d cm</b>." % (pi(V), pi(r * r), h))
    if k == "cil_r":
        r, h = R.randint(2, 12), R.randint(2, 10)
        return M("Un cilindro ha area laterale %s e altezza %d cm. Quanto misura il raggio?" % (pi(2 * r * h, "cm²"), h), "%d cm" % r, W("%d cm" % (2 * r), "%s cm" % d(Fr(r, 2)), "%d cm" % (r * h) if r * h != r else None, "%d cm" % (r + 1)), "r = Al : (2πh) = %s : %s = <b>%d cm</b>." % (pi(2 * r * h), pi(2 * h), r)) if h != 1 else None
    r = R.randint(2, 15)
    return M("Una sfera ha superficie %s. Quanto misura il raggio?" % pi(4 * r * r, "cm²"), "%d cm" % r, W("%d cm" % (2 * r), "%d cm" % (r * r), "%d cm" % (4 * r), "%d cm" % (r + 1)), "r² = %d : 4 = %d → <b>r = %d cm</b>." % (4 * r * r, r * r, r))


def s5():
    k = R.choice(["lattina", "gelato", "pallone", "silo", "tubo"])
    if k == "lattina":
        r, h = R.choice([(3, 10), (4, 12), (5, 10), (3, 11)])
        V = r * r * h * PI
        return M("Una lattina cilindrica ha raggio %d cm e altezza %d cm. Quanti ml contiene (π = 3,14)?" % (r, h), "%s ml" % d(V), W("%s ml" % d(2 * r * h * PI), "%s ml" % d(V / 10), "%s ml" % d(V * 10), "%s ml" % d(4 * r * r * h * PI)),
                 "V = 3,14 × %d × %d = %s cm³ = <b>%s ml</b>." % (r * r, h, d(V), d(V)))
    if k == "gelato":
        r, h = 3, R.choice([9, 12, 15])
        V = Fr(r * r * h, 3)
        return M("Un cono gelato ha raggio %d cm e altezza %d cm. Quanti cm³ di gelato contiene se è pieno fino all’orlo (in funzione di π)?" % (r, h), pi(V, "cm³"), W(pi(r * r * h, "cm³"), pi(Fr(r * h, 3), "cm³"), pi(V * 2, "cm³")),
                 "V = π × %d × %d : 3 = <b>%s</b>." % (r * r, h, pi(V, "cm³")))
    if k == "pallone":
        r = R.choice([10, 11, 12])
        return M("Un pallone da basket ha raggio di circa %d cm. Quanti cm² di materiale servono per la sua superficie (π = 3,14)?" % r, "%s cm²" % d(4 * r * r * PI), W("%s cm²" % d(r * r * PI), "%s cm²" % d(2 * r * r * PI), "%s cm²" % d(Fr(4, 3) * r ** 3 * PI) if (Fr(4, 3) * r ** 3 * PI * 100).denominator == 1 else "%s cm²" % d(8 * r * r * PI)),
                 "A = 4 × 3,14 × %d = <b>%s cm²</b>." % (r * r, d(4 * r * r * PI)))
    if k == "silo":
        r, h, hc = R.choice([(2, 6, 3), (3, 8, 3), (2, 9, 3), (4, 10, 6)])
        V = r * r * h + Fr(r * r * hc, 3)
        return M("Un silo è formato da un cilindro (r = %d m, h = %d m) sormontato da un cono con la stessa base e altezza %d m. Qual è il volume del silo (in funzione di π)?" % (r, h, hc), pi(V, "m³"), W(pi(r * r * (h + hc), "m³"), pi(r * r * h, "m³"), pi(Fr(r * r * (h + hc), 3), "m³") if (Fr(r * r * (h + hc), 3) * 10).denominator == 1 else pi(r * r * h * 2, "m³")),
                 "Cilindro: π × %d × %d = %s; cono: π × %d × %d : 3 = %s; totale <b>%s</b>." % (r * r, h, pi(r * r * h), r * r, hc, pi(Fr(r * r * hc, 3)), pi(V, "m³")))
    R1, r1, h = R.choice([(5, 4, 10), (10, 8, 20), (6, 5, 10), (7, 6, 20)])
    V = (R1 * R1 - r1 * r1) * h
    return M("Un tubo cilindrico è lungo %d cm, con raggio esterno %d cm e raggio interno %d cm. Qual è il volume del materiale (in funzione di π)?" % (h, R1, r1), pi(V, "cm³"), W(pi((R1 - r1) ** 2 * h, "cm³"), pi(R1 * R1 * h, "cm³"), pi(2 * (R1 - r1) * h, "cm³")),
             "V = π(R² − r²) × h = π × (%d − %d) × %d = <b>%s</b>." % (R1 * R1, r1 * r1, h, pi(V, "cm³")))


def main():
    seen = set()
    sets = [
        ("Solidi di rotazione", mix(R, seen, [(s1_quiz, 10), (s3_cono, 10)])),
        ("Il cilindro", mix(R, seen, [(s2_cil, 20)])),
        ("Il cono", mix(R, seen, [(s3_cono, 20)])),
        ("La sfera e le formule inverse", mix(R, seen, [(s4_sfera, 10), (s4_inverse, 10)])),
        ("Problemi", mix(R, seen, [(s5, 12), (s4_inverse, 8)])),
    ]
    body = L(["I <b>solidi di rotazione</b> nascono facendo ruotare una figura piana attorno a una retta: rettangolo → <b>cilindro</b>, triangolo rettangolo → <b>cono</b>, semicerchio → <b>sfera</b>.",
              "<b>Cilindro</b>: Al = 2πr × h, At = Al + 2πr², V = πr² × h.",
              "<b>Cono</b>: l’apotema a = √(r² + h²); Al = πr × a, At = Al + πr², V = πr² × h : 3.",
              "<b>Sfera</b>: A = 4πr², V = 4/3 πr³."],
             [("Cono con r = 6 cm e h = 8 cm", ["a = √(36 + 64) = 10 cm", "Al = π × 6 × 10", "V = π × 36 × 8 : 3"], "Al = 60π cm², V = 96π cm³")],
             [["Volume del cono senza : 3", "Il cono è un terzo del cilindro con stessa base e altezza."],
              ["Usare h al posto dell’apotema in Al del cono", "Al = πr × a, con a = √(r² + h²)."],
              ["Usare il diametro come raggio", "Se il testo dà il diametro, dividi per 2."]],
             table(["Solido", "Area laterale", "Volume"], [["cilindro", "2πrh", "πr²h"], ["cono", "πra", "πr²h : 3"], ["sfera", "4πr² (superficie)", "4/3 πr³"]]))
    faq = [("Perché il volume del cono è un terzo di quello del cilindro?", "Come per piramide e prisma: riempiendo un cono d’acqua e versandola in un cilindro con stessa base e altezza, servono tre coni per riempirlo."),
           ("Che cos’è un cilindro equilatero?", "Un cilindro in cui l’altezza è uguale al diametro di base: la sua sezione per l’asse è un quadrato.")]
    unit(G, R, "solidi-di-rotazione", "S",
         "Calcolare l’area e il volume delle figure solide più comuni e darne stime di oggetti della vita quotidiana",
         "Solidi di rotazione: cilindro, cono e sfera", "Cilindro, cono e sfera",
         "Schede di matematica per la terza media sui solidi di rotazione: cilindro, cono e sfera, area laterale, area totale, volume, formule inverse e problemi. 100 esercizi con soluzioni.",
         "Cilindro: V = πr²h. Cono: V = πr²h : 3.", "Sfera: A = 4πr², V = 4/3 πr³.",
         body, faq, sets, 11)


if __name__ == "__main__":
    main()
