# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Posizioni e percorsi (Spazio e figure)
  python3 tools/gen_it_matematica_c1_posizioni_e_percorsi.py
Sopra, sotto, davanti, dietro, accanto, dentro, fuori; destra e sinistra; in fila; le caselle del reticolo;
percorsi con le frecce.
Errori: confondere destra e sinistra, contare la casella di partenza, scambiare davanti e dietro.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table
import gen_it_matematica_c2_simmetria_e_percorsi as P2
import it_c1 as C
import k_pics

R = random.Random(70113)
G = "classe-prima"


def s1_tavolo():
    k = R.choice(C.KINDS)
    rel = R.choice(["above", "below", "beside"])
    ans = {"above": "sopra il tavolo", "below": "sotto il tavolo", "beside": "accanto al tavolo"}[rel]
    pic = C.it(k_pics.table_scene_svg(k, rel), "un tavolo e %s" % C.un_(k))
    return mcq(pic + "Dove si trova l’oggetto?", ans,
               [x for x in ("sopra il tavolo", "sotto il tavolo", "accanto al tavolo", "dentro il tavolo") if x != ans], "L’oggetto è <b>%s</b>." % ans)


def s1_scatola():
    k = R.choice(C.KINDS)
    rel = R.choice(["front", "behind", "beside", "above"])
    ans = {"front": "davanti alla scatola", "behind": "dietro la scatola", "beside": "accanto alla scatola", "above": "sopra la scatola"}[rel]
    pic = C.it(k_pics.box_scene_svg(k, rel), "una scatola e un oggetto")
    return mcq(pic + "Dove si trova l’oggetto?", ans, [x for x in ("davanti alla scatola", "dietro la scatola", "accanto alla scatola", "sopra la scatola") if x != ans],
               "L’oggetto è <b>%s</b>%s." % (ans, " (si vede solo una parte)" if rel == "behind" else ""))


def main():
    P2.R = R
    for m in (P2.S3, P2.S3.DE, P2.S3.FRP):
        m.R = R
    seen = set()
    sets = [
        ("Sopra, sotto, accanto", mix(R, seen, [(s1_tavolo, 6), (s1_scatola, 8), (P2.s1_posizioni, 6)])),
        ("Destra e sinistra", mix(R, seen, [(P2.s1_scaffale, 20)])),
        ("Le caselle del reticolo", mix(R, seen, [(P2.S3.s4_dove, 10), (P2.S3.s4_cosa, 10)])),
        ("Percorsi con le frecce", mix(R, seen, [(P2.S3.s4_passi, 10), (P2.S3.s5_codice, 10)])),
        ("Posizioni intorno a noi", mix(R, seen, [(P2.s1_posizioni, 4), (s1_tavolo, 4), (s1_scatola, 4), (P2.s1_scaffale, 8)])),
    ]
    body = lesson(
        ["Per dire dove si trova una cosa si usano parole come <b>sopra, sotto, davanti, dietro, accanto, dentro, fuori</b>.",
         "La <b>destra</b> è la mano con cui di solito si scrive (per la maggior parte dei bambini); la <b>sinistra</b> è l’altra.",
         "Nel <b>reticolo</b> ogni casella ha un nome: prima la lettera (colonna), poi il numero (riga): B3.",
         "Le frecce → ← ↑ ↓ fanno spostare di una casella. Non si conta la casella di partenza."],
        [("Il robot è in A1 ed esegue → ↑", ["→ : va in B1", "↑ : va in B2"], "B2")],
        [["Confondere destra e sinistra", "Alza la mano con cui scrivi: di solito è la destra."],
         ["Contare la casella di partenza", "Ogni freccia è un passo nuovo."],
         ["Leggere 3B invece di B3", "Prima la lettera, poi il numero."]],
        table(["Parola", "Il contrario"], [["sopra", "sotto"], ["davanti", "dietro"], ["dentro", "fuori"], ["destra", "sinistra"], ["vicino", "lontano"]]))
    faq = [("Come si impara la destra e la sinistra?", "Con giochi di movimento: «alza la mano destra», «salta a sinistra»; un braccialetto sul polso destro aiuta all’inizio."),
           ("A che cosa servono i percorsi con le frecce?", "Ad allenare l’orientamento e il pensiero computazionale: si danno istruzioni precise, come a un robot.")]
    make_unit(R, "posizioni-e-percorsi", "S",
              "Comunicare la posizione di oggetti nello spazio fisico, usando termini adeguati (sopra/sotto, davanti/dietro, destra/sinistra, dentro/fuori); eseguire un semplice percorso",
              "Posizioni e percorsi: sopra, sotto, destra, sinistra", "Posizioni e percorsi",
              "Schede di matematica per la classe prima su posizioni e percorsi: sopra, sotto, accanto, davanti, dietro, destra e sinistra, le caselle del reticolo e percorsi con le frecce. 100 esercizi con soluzioni.",
              "Prima la lettera, poi il numero.", "Ogni freccia è un passo.",
              body, faq, sets, 13, grade=G)


if __name__ == "__main__":
    main()
