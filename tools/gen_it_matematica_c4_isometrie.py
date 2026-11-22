# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Simmetrie, traslazioni, rotazioni e piano cartesiano (Spazio e figure)
  python3 tools/gen_it_matematica_c4_isometrie.py
Coordinate nel primo quadrante, figure simmetriche e assi di simmetria, simmetria rispetto a un asse,
traslazioni (vettore: quanti quadretti e in che direzione), rotazioni di un quarto e di mezzo giro.
Errori: scambiare l’ordine delle coordinate, contare la casella di partenza, ribaltare invece di traslare.
"""
import random
from it_common import lesson, make_unit, mix, table
import gen_it_matematica_c5_trasformazioni_e_piano_cartesiano as T5
import gen_it_matematica_c3_simmetria_e_percorsi as S3

R = random.Random(70419)
G = "classe-quarta"


def main():
    for m in (T5, S3, S3.DE, S3.FRP):
        m.R = R
    seen = set()
    sets = [
        ("Coordinate nel piano", mix(R, seen, [(T5.s1_leggi, 12), (T5.s1_trova, 8)])),
        ("Figure simmetriche e assi", mix(R, seen, [(S3.s1, 8), (S3.s3_assi, 6), (S3.s1_lettere, 6)])),
        ("Simmetria rispetto a un asse", mix(R, seen, [(T5.s3_simmetria, 12), (S3.s2, 8)])),
        ("Traslazioni", mix(R, seen, [(T5.s2_traslazione, 12), (T5.s2_tri, 8)])),
        ("Rotazioni e trasformazioni miste", mix(R, seen, [(T5.s3_rotazione, 8), (T5.s1_leggi, 4), (T5.s2_traslazione, 4), (T5.s3_simmetria, 4)])),
    ]
    body = lesson(
        ["Nel <b>piano cartesiano</b> un punto si indica con due numeri, le <b>coordinate</b>: prima quanto ti sposti in orizzontale (x), poi in verticale (y). A(3; 5).",
         "Nella <b>simmetria</b> rispetto a un asse ogni punto va dall’altra parte, alla stessa distanza: la figura si «ribalta».",
         "Nella <b>traslazione</b> tutti i punti si spostano dello stesso numero di quadretti, nella stessa direzione: la figura «scivola».",
         "Nella <b>rotazione</b> la figura gira intorno a un punto (un quarto di giro = 90°, mezzo giro = 180°). In tutte queste trasformazioni la figura resta uguale (isometrie)."],
        [("A(2; 3) traslato di 4 a destra e 1 in alto", ["x: 2 + 4 = 6", "y: 3 + 1 = 4"], "A′(6; 4)")],
        [["Scrivere (y; x) invece di (x; y)", "Prima l’orizzontale, poi la verticale: «prima cammini, poi sali»."],
         ["Contare la casella di partenza", "Conta i passi, non le caselle."],
         ["Ribaltare la figura in una traslazione", "Nella traslazione la figura non cambia verso."]],
        table(["Trasformazione", "Che cosa fa", "La figura"], [["simmetria", "ribalta rispetto a un asse", "si capovolge"], ["traslazione", "sposta lungo una direzione", "scivola"], ["rotazione", "gira intorno a un punto", "ruota"]]))
    faq = [("Che cos’è un’isometria?", "Una trasformazione che non cambia forma e misure della figura: simmetria, traslazione e rotazione sono isometrie."),
           ("Perché si dice «prima x, poi y»?", "È la convenzione di tutto il mondo: la prima coordinata è sull’asse orizzontale, la seconda su quello verticale.")]
    make_unit(R, "isometrie", "S",
              "Riconoscere figure ruotate, traslate e riflesse; utilizzare il piano cartesiano per localizzare punti",
              "Simmetrie, traslazioni, rotazioni e piano cartesiano", "Isometrie e piano cartesiano",
              "Schede di matematica per la classe quarta su simmetria, traslazione e rotazione: coordinate nel piano cartesiano, assi di simmetria, figure simmetriche, traslazioni e rotazioni. 100 esercizi con soluzioni.",
              "Coordinate: prima x (orizzontale), poi y (verticale).", "Simmetria ribalta, traslazione sposta, rotazione gira.",
              body, faq, sets, 19, grade=G)


if __name__ == "__main__":
    main()
