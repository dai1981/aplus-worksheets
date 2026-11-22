# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Linee e figure (Spazio e figure)
  python3 tools/gen_it_matematica_c1_linee_e_figure.py
Linee rette, curve e spezzate; linee aperte e chiuse; dentro, fuori e sul confine; le figure piane (cerchio, quadrato,
rettangolo, triangolo); figure negli oggetti di tutti i giorni; lati e vertici.
Errori: chiamare chiusa una linea che quasi si chiude, chiamare quadrato ogni rettangolo, confondere il cerchio con la palla.
"""
import random
from it_common import lesson, make_unit, mix, table
import gen_it_matematica_c2_linee_e_regioni as L2
import gen_it_matematica_c2_figure_e_solidi as F2

R = random.Random(70112)
G = "classe-prima"


def main():
    L2.R = R
    L2.L3.R = R
    F2.R = R
    for m in (F2.F3, F2.S3, F2.FRF):
        m.R = R
    F2.S3.DE.R = R
    seen = set()
    sets = [
        ("Linee rette, curve e spezzate", mix(R, seen, [(L2.s1_tipo, 20)])),
        ("Linee aperte e chiuse", mix(R, seen, [(L2.s1_chiusa, 20)])),
        ("Dentro, fuori, sul confine", mix(R, seen, [(L2.s2_regione, 14), (L2.s2_quiz, 6)])),
        ("Le figure piane", mix(R, seen, [(F2.s1_nome, 14), (F2.s1_lati, 6)])),
        ("Figure intorno a noi", mix(R, seen, [(F2.s2_oggetti, 12), (F2.s2_quiz, 4), (L2.s5_vita, 4)])),
    ]
    body = lesson(
        ["Le linee possono essere <b>rette</b>, <b>curve</b> o <b>spezzate</b>.",
         "Una linea <b>chiusa</b> torna al punto di partenza e fa da <b>confine</b>: c’è un dentro (regione interna) e un fuori (regione esterna).",
         "Le figure piane più comuni sono il <b>cerchio</b>, il <b>quadrato</b>, il <b>rettangolo</b> e il <b>triangolo</b>.",
         "Il triangolo ha 3 lati, il quadrato e il rettangolo ne hanno 4; il cerchio non ha lati."],
        [("Un recinto chiuso con dentro le pecore", ["il recinto è il confine", "le pecore sono dentro"], "le pecore sono nella regione interna")],
        [["Chiamare chiusa una linea con un’apertura", "Segui la linea con il dito: torna al punto di partenza?"],
         ["Chiamare quadrato ogni rettangolo", "Nel quadrato i 4 lati sono tutti uguali."],
         ["Chiamare cerchio una palla", "Il cerchio è piatto, la palla è un solido (sfera)."]],
        table(["Figura", "Lati"], [["triangolo", "3"], ["quadrato", "4 uguali"], ["rettangolo", "4 (2 lunghi e 2 corti)"], ["cerchio", "nessuno"]]))
    faq = [("Come si fa pratica con le linee?", "Camminando sulle linee in palestra, disegnando percorsi aperti e chiusi e giocando a «dentro e fuori» con un cerchio di corda."),
           ("Dove si trovano le figure piane?", "Nelle finestre (rettangoli), nelle piastrelle (quadrati), nei cartelli stradali (triangoli e cerchi), nelle monete (cerchi).")]
    make_unit(R, "linee-e-figure", "S",
              "Riconoscere, denominare e descrivere linee e figure geometriche; riconoscere confine, regione interna ed esterna",
              "Linee e figure piane", "Linee e figure",
              "Schede di matematica per la classe prima su linee e figure: linee rette, curve e spezzate, aperte e chiuse, dentro e fuori, cerchio, quadrato, rettangolo e triangolo, figure negli oggetti. 100 esercizi con soluzioni.",
              "Una linea chiusa ha un dentro e un fuori.", "Triangolo: 3 lati. Quadrato e rettangolo: 4 lati.",
              body, faq, sets, 12, grade=G)


if __name__ == "__main__":
    main()
