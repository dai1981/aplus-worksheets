# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: La compravendita (Problemi)
  python3 tools/gen_it_matematica_c5_compravendita.py
Spesa, ricavo, guadagno e perdita; costo unitario e costo totale; peso lordo, netto e tara con il prezzo al kg;
problemi in più passaggi del commerciante.
Errori: confondere spesa e ricavo, guadagno = ricavo + spesa, costo unitario moltiplicando invece di dividere.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, eur, table, FOIS, DIV

R = random.Random(70514)
G = "classe-quinta"
K = Kids(R)
E = lambda x: "%s €" % num(x)
FEM = {"cassette di arance", "biciclette", "piante", "torte", "magliette", "scatole di colori"}
PRON = lambda c: "le" if c in FEM else "li"
UNO = lambda c: "l’una" if c in FEM else "l’uno"
OGNI = lambda c: "ognuna" if c in FEM else "ognuno"
MERCE = [("un fruttivendolo", "cassette di arance"), ("un libraio", "libri"), ("un negoziante", "biciclette"), ("un cartolaio", "zaini"),
         ("un fioraio", "piante"), ("una pasticceria", "torte"), ("un negozio di giochi", "puzzle"), ("un ferramenta", "trapani")]


def s1_gp():
    chi, cosa = R.choice(MERCE)
    sp = R.randint(20, 400) * 10
    k = R.choice(["guad", "guad", "perd", "ricavo", "spesa"])
    if k == "guad":
        g = R.randint(5, 150) * 10
        rv = sp + g
        return mcq("%s spende %s per comprare %s e %s rivende ricavando %s. Quanto guadagna?" % (chi.capitalize(), E(sp), cosa, PRON(cosa), E(rv)), E(g), [E(sp + rv), E(rv), E(g + 100)],
                   "Guadagno = ricavo − spesa: %s − %s = <b>%s</b>." % (num(rv), num(sp), E(g)))
    if k == "perd":
        pe = R.randint(2, 50) * 10
        rv = sp - pe
        if rv <= 0:
            return None
        return mcq("%s spende %s per %s ma riesce a ricavare solo %s. Guadagna o perde? Quanto?" % (chi.capitalize(), E(sp), cosa, E(rv)), "perde %s" % E(pe),
                   ["guadagna %s" % E(pe), "perde %s" % E(sp + rv), "guadagna %s" % E(rv)], "Il ricavo è minore della spesa: perdita = spesa − ricavo = %s − %s = <b>%s</b>." % (num(sp), num(rv), E(pe)))
    if k == "ricavo":
        g = R.randint(5, 150) * 10
        return mcq("%s ha speso %s e vuole guadagnare %s. Quanto deve ricavare?" % (chi.capitalize(), E(sp), E(g)), E(sp + g), [E(sp - g) if sp > g else E(g), E(g), E(sp + g + 100)],
                   "Ricavo = spesa + guadagno: %s + %s = <b>%s</b>." % (num(sp), num(g), E(sp + g)))
    g = R.randint(5, 150) * 10
    rv = sp + g
    return mcq("%s ha ricavato %s e ha guadagnato %s. Quanto aveva speso?" % (chi.capitalize(), E(rv), E(g)), E(sp), [E(rv + g), E(g), E(sp + 100)],
               "Spesa = ricavo − guadagno: %s − %s = <b>%s</b>." % (num(rv), num(g), E(sp)))


def s2_unitario():
    n = R.randint(2, 25)
    u = R.randint(2, 80)
    k = R.random() < 0.5
    cosa = R.choice(["quaderni", "magliette", "biglietti", "palloni", "vasi", "scatole di colori"])
    if k:
        return mcq("Si comprano %d %s a %s %s. Qual è il costo totale?" % (n, cosa, E(u), UNO(cosa)), E(n * u), [E(n + u), E(n * u + u), E(n * u // 10) if n * u >= 100 else E(n * u + 10)],
                   "Costo totale = costo unitario %s quantità: %d %s %d = <b>%s</b>." % (FOIS, u, FOIS, n, E(n * u)))
    return mcq("%d %s costano in tutto %s. Quanto costa %s?" % (n, cosa, E(n * u), "una" if cosa in FEM else "uno"), E(u), [E(n * u * n), E(n * u - n), E(u + 1)],
               "Costo unitario = costo totale %s quantità: %s %s %d = <b>%s</b>." % (DIV, num(n * u), DIV, n, E(u)))


def s2_kg():
    pr = R.randint(120, 990)
    if pr % 10:
        pr = pr // 10 * 10
    kg = R.randint(2, 9)
    if R.random() < 0.5:
        return mcq("Le ciliegie costano %s al kg. Quanto si spende per %d kg?" % (eur(pr), kg), eur(pr * kg), [eur(pr + kg * 100), eur(pr * kg + pr), eur(pr * kg // 10)],
                   "%s %s %d = <b>%s</b>." % (eur(pr), FOIS, kg, eur(pr * kg)))
    return mcq("Per %d kg di formaggio si spendono %s. Quanto costa al kg?" % (kg, eur(pr * kg)), eur(pr), [eur(pr * kg * kg), eur(pr + 100), eur(pr * kg - kg * 100)],
               "%s %s %d = <b>%s</b>." % (eur(pr * kg), DIV, kg, eur(pr)))


def s3_lnt():
    ne = R.randint(4, 40) * 5
    ta = R.randint(1, 6) * 5
    lo = ne + ta
    k = R.choice(["netto", "tara", "lordo", "prezzo"])
    if k == "netto":
        return mcq("Una cassa di mele pesa %d kg (peso lordo). La cassa vuota pesa %d kg. Qual è il peso netto?" % (lo, ta), "%d kg" % ne, ["%d kg" % (lo + ta), "%d kg" % ta, "%d kg" % lo],
                   "Netto = lordo − tara: %d − %d = <b>%d kg</b>." % (lo, ta, ne))
    if k == "tara":
        return mcq("Un sacco di farina pesa %d kg lordi; la farina pesa %d kg. Quanto pesa il sacco vuoto?" % (lo, ne), "%d kg" % ta, ["%d kg" % (lo + ne), "%d kg" % ne, "%d kg" % (ta + 5)],
                   "Tara = lordo − netto: %d − %d = <b>%d kg</b>." % (lo, ne, ta))
    if k == "lordo":
        return mcq("Una cassetta contiene %d kg di patate e pesa vuota %d kg. Qual è il peso lordo?" % (ne, ta), "%d kg" % lo, ["%d kg" % (ne - ta), "%d kg" % ne, "%d kg" % (lo + ta)],
                   "Lordo = netto + tara: %d + %d = <b>%d kg</b>." % (ne, ta, lo))
    pr = R.choice([2, 3, 4, 5])
    return mcq("Una cassa di pomodori pesa %d kg lordi, la tara è %d kg. I pomodori costano %d € al kg. Quanto costano i pomodori?" % (lo, ta, pr), E(ne * pr), [E(lo * pr), E(ta * pr), E(ne + pr)],
               "Netto: %d − %d = %d kg; %d %s %d = <b>%s</b>." % (lo, ta, ne, ne, FOIS, pr, E(ne * pr)))


def s4_passi():
    chi, cosa = R.choice(MERCE)
    n = R.randint(10, 60)
    cu = R.randint(5, 40)
    vu = cu + R.randint(2, 20)
    sp, rv = n * cu, n * vu
    k = R.choice(["guad", "guad", "vendita"])
    if k == "guad":
        return mcq("%s compra %d %s a %s %s e %s rivende a %s %s. Quanto guadagna in tutto?" % (chi.capitalize(), n, cosa, E(cu), UNO(cosa), PRON(cosa), E(vu), UNO(cosa)), E(rv - sp),
                   [E(vu - cu), E(rv), E(rv + sp)], "Spesa: %d %s %d = %s; ricavo: %d %s %d = %s; guadagno: <b>%s</b>." % (n, FOIS, cu, num(sp), n, FOIS, vu, num(rv), E(rv - sp)))
    g = n * (vu - cu)
    return mcq("%s compra %d %s spendendo %s e vuole guadagnare %s in tutto. A quanto deve vendere %s?" % (chi.capitalize(), n, cosa, E(sp), E(g), OGNI(cosa)), E(vu),
               [E((sp + g) * n) if (sp + g) * n < 100000 else E(vu + 5), E(cu), E(g // n)], "Ricavo: %s + %s = %s; %s %s %d = <b>%s</b>." % (num(sp), num(g), num(sp + g), num(sp + g), DIV, n, E(vu)))


def s5():
    p = K.next()
    k = R.choice(["bancarella", "mercatino", "limonata", "torte", "sconto"])
    if k == "bancarella":
        sp = R.randint(15, 60)
        n, pr = R.randint(15, 40), R.choice([2, 3])
        rv = n * pr
        g = rv - sp
        if g <= 0:
            return None
        return mcq("Al mercatino della scuola la classe spende %d € per il materiale e vende %d segnalibri a %d € l’uno. Quanto guadagna?" % (sp, n, pr), "%d €" % g,
                   ["%d €" % rv, "%d €" % (rv + sp), "%d €" % (g + pr)], "Ricavo: %d %s %d = %d €; guadagno: %d − %d = <b>%d €</b>." % (n, FOIS, pr, rv, rv, sp, g))
    if k == "mercatino":
        a, b, c = R.randint(8, 20), R.randint(5, 15), R.randint(3, 12)
        return mcq("%s vende %d libri usati a 3 €, %d giochi a 5 € e %d fumetti a 2 €. Quanto ricava?" % (p[0], a, b, c), "%d €" % (a * 3 + b * 5 + c * 2),
                   ["%d €" % (a + b + c), "%d €" % ((a + b + c) * 10), "%d €" % (a * 3 + b * 5)], "%d + %d + %d = <b>%d €</b>." % (a * 3, b * 5, c * 2, a * 3 + b * 5 + c * 2))
    if k == "limonata":
        sp = R.randint(6, 15)
        n, pr = R.randint(20, 50), R.choice([50, 100])
        rv = n * pr
        return mcq("%s spende %d € per limoni e zucchero e vende %d bicchieri di limonata a %s l’uno. Quanto guadagna?" % (p[0], sp, n, eur(pr, c=True)), eur(rv - sp * 100),
                   [eur(rv), eur(rv + sp * 100), eur(n * 100 - sp * 100) if pr == 50 else eur(rv // 2)], "Ricavo: %d %s %s = %s; guadagno: %s − %d € = <b>%s</b>." % (n, FOIS, eur(pr, c=True), eur(rv), eur(rv), sp, eur(rv - sp * 100)))
    if k == "torte":
        t, f, pr = R.randint(3, 8), R.choice([8, 10, 12]), R.choice([2, 3])
        sp = R.randint(15, 40)
        g = t * f * pr - sp
        return mcq("Per una festa si preparano %d torte da %d fette, spendendo %d €. Ogni fetta si vende a %d €. Se si vendono tutte, quanto si guadagna?" % (t, f, sp, pr), "%d €" % g,
                   ["%d €" % (t * f * pr), "%d €" % (t * pr - sp) if t * pr > sp else "%d €" % (g + 10), "%d €" % (t * f * pr + sp)], "Fette: %d; ricavo: %d €; guadagno: %d − %d = <b>%d €</b>." % (t * f, t * f * pr, t * f * pr, sp, g))
    pr = R.randint(4, 20) * 10
    sc = pr // 10
    n = R.randint(2, 4)
    return mcq("Un monopattino costa %d €; per i soci c’è uno sconto di %d €. Una famiglia ne compra %d con lo sconto. Quanto spende?" % (pr, sc, n), "%d €" % ((pr - sc) * n),
               ["%d €" % (pr * n - sc), "%d €" % (pr * n), "%d €" % (sc * n)], "(%d − %d) %s %d = <b>%d €</b>." % (pr, sc, FOIS, n, (pr - sc) * n))


def main():
    seen = set()
    sets = [
        ("Spesa, ricavo, guadagno, perdita", mix(R, seen, [(s1_gp, 20)])),
        ("Costo unitario e costo totale", mix(R, seen, [(s2_unitario, 12), (s2_kg, 8)])),
        ("Peso lordo, netto e tara", mix(R, seen, [(s3_lnt, 20)])),
        ("Problemi in più passaggi", mix(R, seen, [(s4_passi, 20)])),
        ("Problemi della vita di tutti i giorni", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["La <b>spesa</b> è quanto paga chi compra; il <b>ricavo</b> è quanto incassa chi vende.",
         "<b>Guadagno</b> = ricavo − spesa (se il ricavo è maggiore). <b>Perdita</b> = spesa − ricavo (se il ricavo è minore).",
         "Costo totale = costo unitario %s quantità; costo unitario = costo totale %s quantità." % (FOIS, DIV),
         "Peso lordo = peso netto + tara. Il prezzo si calcola sul peso netto."],
        [("Compro 20 penne a 2 € e le vendo a 3 €.", ["spesa: 20 %s 2 = 40 €" % FOIS, "ricavo: 20 %s 3 = 60 €" % FOIS, "guadagno: 60 − 40 = 20 €"], "20 €")],
        [["Confondere spesa e ricavo", "Chi compra spende, chi vende ricava."],
         ["Guadagno = ricavo + spesa", "Il guadagno è una differenza: ricavo − spesa."],
         ["Costo unitario moltiplicando", "Per trovare il prezzo di uno solo si divide."]],
        table(["Se conosci…", "Calcoli…"], [["spesa e ricavo", "guadagno = ricavo − spesa"], ["spesa e guadagno", "ricavo = spesa + guadagno"], ["ricavo e guadagno", "spesa = ricavo − guadagno"]]))
    faq = [("Qual è la differenza tra ricavo e guadagno?", "Il ricavo è tutto il denaro incassato; il guadagno è ciò che resta dopo aver tolto la spesa."),
           ("Quando c’è una perdita?", "Quando si ricava meno di quanto si è speso: la perdita è spesa − ricavo.")]
    make_unit(R, "compravendita", "P",
              "Risolvere problemi in contesti di compravendita (spesa, ricavo, guadagno, perdita; costo unitario e totale; peso lordo, netto e tara), rappresentando il procedimento",
              "La compravendita: spesa, ricavo, guadagno e perdita", "Compravendita",
              "Schede di matematica per la classe quinta sulla compravendita: spesa, ricavo, guadagno e perdita, costo unitario e totale, prezzo al kg, peso lordo, netto e tara, problemi. 100 esercizi con soluzioni.",
              "Guadagno = ricavo − spesa.", "Costo unitario = costo totale : quantità.",
              body, faq, sets, 14, grade=G)


if __name__ == "__main__":
    main()
