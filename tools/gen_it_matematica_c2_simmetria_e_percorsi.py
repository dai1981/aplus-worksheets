# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Simmetria, posizioni e percorsi (Spazio e figure)
  python3 tools/gen_it_matematica_c2_simmetria_e_percorsi.py
Sopra/sotto, davanti/dietro, destra/sinistra; caselle del reticolo (colonna e riga); percorsi con frecce;
figure simmetriche e asse di simmetria; completare una figura simmetrica.
Errori: confondere destra e sinistra di chi è di fronte, leggere prima la riga, contare la casella di partenza.
"""
import random
from it_common import mcq, lesson, make_unit, mix
import gen_it_matematica_c3_simmetria_e_percorsi as S3
import it_c2 as C
import k_pics

R = random.Random(70217)
G = "classe-seconda"


def s1_posizioni():
    q, a, w = R.choice([("Il soffitto è … il pavimento.", "sopra", ["sotto", "davanti", "a destra"]), ("Il tappeto è … il tavolo.", "sotto", ["sopra", "dietro", "a sinistra"]),
                        ("Quando sei in fila, chi è prima di te è…", "davanti a te", ["dietro di te", "sotto di te", "sopra di te"]),
                        ("Quando sei in fila, chi viene dopo di te è…", "dietro di te", ["davanti a te", "sopra di te", "a destra"]),
                        ("Con quale mano scrive di solito chi è destrorso?", "con la destra", ["con la sinistra", "con tutte e due", "con nessuna"]),
                        ("Sei di fronte a un amico e alzi la mano destra. Per lui la tua mano è…", "alla sua sinistra", ["alla sua destra", "sopra", "dietro"]),
                        ("A mezzogiorno il sole è … la tua testa.", "sopra", ["sotto", "dietro", "a sinistra"]),
                        ("Le radici di un albero sono … il terreno.", "sotto", ["sopra", "davanti", "a destra"]),
                        ("Il tetto della casa è … le finestre.", "sopra", ["sotto", "dietro", "dentro"]),
                        ("Se giri su te stesso di mezzo giro, quello che era davanti ora è…", "dietro", ["davanti", "sopra", "sotto"])])
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s1_scaffale():
    kinds = R.sample(C.KINDS, 4)
    pic = C.it(k_pics.kinds_row_svg(kinds), "%s in fila" % ", ".join(C.un_(k) for k in kinds))
    i = R.randint(0, 3)
    if i in (0, 3):
        q = "Che cosa c’è all’estrema %s?" % ("sinistra" if i == 0 else "destra")
    else:
        q = "Che cosa c’è a destra di %s?" % C.un_(kinds[i - 1]).replace("un ", "un ", 1)
    return mcq(pic + q, C.un_(kinds[i]), [C.un_(k) for k in kinds if k != kinds[i]], "Guarda la fila da sinistra a destra: <b>%s</b>." % C.un_(kinds[i]))


def main():
    for m in (S3, S3.DE, S3.FRP):
        m.R = R
    seen = set()
    sets = [
        ("Sopra, sotto, destra, sinistra", mix(R, seen, [(s1_posizioni, 10), (s1_scaffale, 10)])),
        ("Le caselle del reticolo", mix(R, seen, [(S3.s4_dove, 10), (S3.s4_cosa, 10)])),
        ("Percorsi con le frecce", mix(R, seen, [(S3.s4_passi, 8), (S3.s5_codice, 12)])),
        ("Figure simmetriche", mix(R, seen, [(S3.s1, 10), (S3.s1_lettere, 10)])),
        ("Completare per simmetria", mix(R, seen, [(S3.s2, 10), (S3.s5_scrivi, 10)])),
    ]
    body = lesson(
        ["Per dire dove si trova una cosa si usano parole come <b>sopra, sotto, davanti, dietro, a destra, a sinistra</b>.",
         "Nel <b>reticolo</b> ogni casella ha un nome: prima la lettera della colonna, poi il numero della riga (B3).",
         "Le frecce → ← ↑ ↓ fanno spostare di una casella. Non si conta la casella di partenza.",
         "Una figura è <b>simmetrica</b> se, piegandola lungo l’<b>asse di simmetria</b>, le due metà combaciano."],
        [("Il robot è in A1 ed esegue → → ↑", ["→ → : da A a C", "↑ : da 1 a 2"], "C2")],
        [["Confondere destra e sinistra di chi ci sta di fronte", "La sua destra è dalla parte della tua sinistra."],
         ["Leggere 3B invece di B3", "Prima la colonna (lettera), poi la riga (numero)."],
         ["Contare la casella di partenza", "Ogni freccia è un passo: parti da dove sei."]])
    faq = [("Come si allena l’orientamento?", "Con giochi di percorsi in palestra o sul pavimento a quadrettoni: un bambino dà le istruzioni, l’altro le esegue."),
           ("Dove si trovano figure simmetriche?", "Nelle farfalle, nelle foglie, nelle lettere A, H, M, O e in molti edifici.")]
    make_unit(R, "simmetria-e-percorsi", "S",
              "Comunicare la posizione di oggetti nello spazio usando termini adeguati (sopra/sotto, davanti/dietro, destra/sinistra); eseguire e descrivere percorsi; riconoscere simmetrie",
              "Simmetria, posizioni e percorsi", "Simmetria e percorsi",
              "Schede di matematica per la classe seconda su posizioni, percorsi e simmetria: sopra e sotto, destra e sinistra, caselle del reticolo, percorsi con le frecce, figure simmetriche. 100 esercizi con soluzioni.",
              "Prima la colonna, poi la riga.", "Le due metà di una figura simmetrica combaciano.",
              body, faq, sets, 17, grade=G)


if __name__ == "__main__":
    main()
