# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Misure – lungo, alto, pesante, capiente (Misure)
  python3 tools/gen_it_matematica_c1_misure.py
Confrontare lunghezze (più lungo, più corto) e altezze, misurare con oggetti (mattoncini, passi, spanne),
pesante e leggero con la bilancia a due piatti, contiene di più o di meno, problemi.
Errori: non partire dalla stessa linea, pensare che il piatto con più oggetti sia il più pesante, confondere alto e largo.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, Kids
import gen_it_matematica_c2_misure as M2
import it_c1 as C
import k_pics

R = random.Random(70110)
G = "classe-prima"
L4 = "ABCD"


def s1_alta():
    hs = R.sample(range(2, 10), 3)
    pic = C.it(k_pics.towers_svg(hs), "3 torri di mattoncini A, B, C")
    alta = R.random() < 0.5
    t = hs.index(max(hs) if alta else min(hs))
    return mcq(pic + "Quale torre è la più %s?" % ("alta" if alta else "bassa"), L4[t], [L4[i] for i in range(3) if i != t] + ["sono uguali"],
               "Le torri partono dallo stesso pavimento: la più %s è la <b>%s</b> (%d mattoncini)." % ("alta" if alta else "bassa", L4[t], hs[t]))


def s2_mani():
    it = M2.s2_non_conv()
    return it if it and "matite" not in it["q"] else None


def s2_differenza():
    hs = R.sample(range(2, 10), 3)
    pic = C.it(k_pics.towers_svg(hs), "3 torri di mattoncini A, B, C")
    i, j = R.sample(range(3), 2)
    if hs[i] < hs[j]:
        i, j = j, i
    return mcq(pic + "Quanti mattoncini è più alta la torre %s della torre %s?" % (L4[i], L4[j]), str(hs[i] - hs[j]), [str(hs[i]), str(hs[i] + hs[j]), str(hs[j])],
               "%d − %d = <b>%d</b> mattoncini." % (hs[i], hs[j], hs[i] - hs[j]))


def s4_cap():
    it = M2.s4_capacita()
    return it if it and "bottiglie" not in it["q"] else None


QUIZ = [("Che cosa è più pesante?", "un’anguria", ["una fragola", "una piuma", "una foglia"]), ("Che cosa è più leggero?", "una piuma", ["un libro", "una sedia", "un mattone"]),
        ("Che cosa è più lungo?", "un treno", ["un’auto", "una bicicletta", "un monopattino"]), ("Che cosa è più alto?", "una giraffa", ["un cane", "un gatto", "una gallina"]),
        ("Che cosa è più corto?", "una formica", ["un serpente", "un lombrico", "una matita"]), ("Che cosa contiene più acqua?", "una vasca da bagno", ["un bicchiere", "una tazza", "un cucchiaio"]),
        ("Che cosa è più basso?", "un tavolino", ["un armadio", "una porta", "un albero"]), ("Che cosa è più pesante?", "un elefante", ["un topo", "un gatto", "un coniglio"])]


def s4_quiz():
    q, a, w = R.choice(QUIZ)
    return mcq(q + " " + ", ".join(sorted([a] + w)) + "?", a, w, "Risposta: <b>%s</b>." % a)


def s5():
    k = R.choice(["passi", "nastro", "torre", "bilancia", "bicchieri"])
    if k == "passi":
        a, b = R.randint(5, 12), R.randint(2, 6)
        return mcq("Dalla porta alla lavagna ci sono %d passi. Dalla lavagna alla finestra altri %d passi. Quanti passi in tutto?" % (a, b), str(a + b), [str(a - b), str(a + b + 1), str(a)], "%d + %d = <b>%d</b> passi." % (a, b, a + b))
    if k == "nastro":
        a, b = R.randint(8, 18), R.randint(2, 6)
        return mcq("Un nastro è lungo %d quadretti. Ne taglio %d quadretti. Quanti quadretti restano?" % (a, b), str(a - b), [str(a + b), str(a - b + 1), str(b)], "%d − %d = <b>%d</b> quadretti." % (a, b, a - b))
    if k == "torre":
        a, b = R.randint(4, 10), R.randint(2, 8)
        return mcq("Una torre è alta %d mattoncini. Ne aggiungo %d. Quanto è alta adesso?" % (a, b), "%d mattoncini" % (a + b), ["%d mattoncini" % (a - b) if a > b else "%d mattoncini" % (b - a + 1), "%d mattoncini" % (a + b + 1), "%d mattoncini" % a],
                   "%d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "bilancia":
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a == b:
            return None
        return mcq("Un sacchetto pesa come %d cubetti, un altro come %d cubetti. Quale sacchetto è più pesante?" % (a, b), "il primo" if a > b else "il secondo",
                   ["il secondo" if a > b else "il primo", "pesano uguale", "non si può dire"], "%d e %d: è più pesante <b>%s</b>." % (a, b, "il primo" if a > b else "il secondo"))
    a, b = R.randint(3, 8), R.randint(3, 8)
    if a == b:
        return None
    g = "la bottiglia rossa" if a > b else "la bottiglia blu"
    return mcq("Con la bottiglia rossa si riempiono %d bicchieri, con la bottiglia blu %d bicchieri. Quale bottiglia contiene più acqua?" % (a, b), g,
               ["la bottiglia blu" if a > b else "la bottiglia rossa", "contengono uguale", "non si può dire"], "%d e %d bicchieri: contiene di più <b>%s</b>." % (a, b, g))


def main():
    M2.R = R
    M2.K = Kids(R)
    seen = set()
    sets = [
        ("Più lungo, più corto", mix(R, seen, [(M2.s1_confronta, 20)])),
        ("Più alto, più basso", mix(R, seen, [(s1_alta, 8), (M2.s1_torri, 6), (s2_differenza, 6)])),
        ("Misurare con passi e spanne", mix(R, seen, [(s2_mani, 8), (s4_quiz, 8), (M2.s1_torri, 4)])),
        ("Pesante, leggero e capiente", mix(R, seen, [(M2.s4_peso, 14), (s4_cap, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Per confrontare due lunghezze mettile <b>una accanto all’altra</b>, partendo dalla stessa linea.",
         "Si può misurare con un oggetto che si ripete: mattoncini, quadretti, passi, spanne. Ma i passi e le spanne non sono uguali per tutti!",
         "Con la bilancia a due piatti, il piatto più <b>pesante</b> va giù; se sono in equilibrio pesano uguale.",
         "Un recipiente <b>contiene di più</b> se ci vuole più acqua per riempirlo."],
        [("Torre A: 7 mattoncini, torre B: 4", ["7 è più di 4", "7 − 4 = 3"], "A è più alta di 3 mattoncini")],
        [["Confrontare senza partire dalla stessa linea", "Allinea gli oggetti da un lato."],
         ["Pensare che più oggetti pesino sempre di più", "Guarda quale piatto va giù."],
         ["Misurare con passi diversi e confrontare i numeri", "Servono unità uguali per tutti."]],
        table(["Grandezza", "Parole"], [["lunghezza", "lungo, corto"], ["altezza", "alto, basso"], ["peso", "pesante, leggero"], ["capacità", "contiene di più, di meno"]]))
    faq = [("Perché in classe prima si misura con passi e spanne?", "Per scoprire che serve un’unità uguale per tutti: è il primo passo verso il metro."),
           ("Come si fa pratica a casa?", "Mettendo in fila oggetti dal più corto al più lungo, pesando frutta con le mani e travasando acqua tra bicchieri e bottiglie.")]
    make_unit(R, "misure", "M",
              "Misurare grandezze (lunghezze, tempo, ecc.) utilizzando sia unità arbitrarie sia unità e strumenti convenzionali; confrontare lunghezze, pesi e capacità",
              "Misure: lungo, alto, pesante, capiente", "Misure",
              "Schede di matematica per la classe prima sulle misure: più lungo e più corto, più alto e più basso, misurare con mattoncini, passi e spanne, pesante e leggero, contiene di più, problemi. 100 esercizi con soluzioni.",
              "Per confrontare, parti dalla stessa linea.", "Il piatto più pesante va giù.",
              body, faq, sets, 10, grade=G)


if __name__ == "__main__":
    main()
