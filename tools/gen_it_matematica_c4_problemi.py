# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Problemi (Problemi)
  python3 tools/gen_it_matematica_c4_problemi.py
Dati utili, inutili e mancanti, la domanda giusta, problemi con due o più operazioni, domande nascoste,
problemi al contrario, problemi con l’età e con il tempo.
Errori: usare tutti i numeri del testo, fermarsi alla prima operazione, scegliere l’operazione dalle parole chiave.
"""
import random
from it_common import lesson, make_unit, mix, table, Kids
import gen_it_matematica_c3_problemi as P3
import gen_it_matematica_c5_problemi as P5

R = random.Random(70410)
G = "classe-quarta"


def main():
    for m in (P3, P5):
        m.R = R
        m.K = Kids(R)
    seen = set()
    sets = [
        ("Dati e domande", mix(R, seen, [(P3.s2_dati, 12), (P3.s2_domanda, 8)])),
        ("Problemi con più operazioni", mix(R, seen, [(P5.s1_passi, 20)])),
        ("Domande nascoste", mix(R, seen, [(P5.s2_nascosto, 20)])),
        ("Problemi al contrario e con l’età", mix(R, seen, [(P5.s4_contrario, 12), (P5.s3_eta, 8)])),
        ("Problemi con i soldi e con il tempo", mix(R, seen, [(P3.s4_soldi, 8), (P5.s5_tempo, 12)])),
    ]
    body = lesson(
        ["Leggi il testo due volte. Sottolinea la <b>domanda</b> e cerchia i <b>dati utili</b>; cancella quelli inutili.",
         "Se per rispondere ti serve un dato che il testo non dice subito, c’è una <b>domanda nascosta</b>: rispondi prima a quella.",
         "Scrivi le operazioni una alla volta, con il loro significato (che cosa trovi), poi la risposta completa.",
         "Controlla: il risultato è ragionevole? Ha l’unità di misura giusta?"],
        [("Luca compra 3 quaderni da 2 € e un astuccio da 9 €. Paga con 20 €. Quanto riceve di resto?", ["domanda nascosta: quanto spende per i quaderni? 3 × 2 = 6 €", "spesa totale: 6 + 9 = 15 €", "resto: 20 − 15 = 5 €"], "5 €")],
        [["Usare tutti i numeri del testo", "Alcuni dati sono inutili: cancellali."],
         ["Fermarsi alla prima operazione", "Rileggi la domanda: hai davvero risposto?"],
         ["Scegliere l’operazione da una parola («in tutto» = +)", "Pensa alla situazione: «in tutto» può voler dire anche ×."]],
        table(["Fase", "Che cosa fai"], [["capire", "leggi, sottolinea la domanda"], ["dati", "cerchia quelli utili"], ["piano", "scegli le operazioni"], ["calcolo e risposta", "calcola e scrivi la risposta completa"], ["controllo", "il risultato è ragionevole?"]]))
    faq = [("Che cos’è un dato inutile?", "Un numero che c’è nel testo ma non serve per rispondere alla domanda, come l’età di chi compra le figurine."),
           ("Come si risolve un problema «al contrario»?", "Si parte dalla fine e si fanno le operazioni inverse: se alla fine ho aggiunto 5, torno indietro togliendo 5.")]
    make_unit(R, "problemi", "P",
              "Risolvere problemi con più operazioni, individuando dati utili, inutili, mancanti e domande nascoste; spiegare il procedimento seguito",
              "Problemi con più operazioni e domande nascoste", "Problemi",
              "Schede di matematica per la classe quarta sui problemi: dati utili e inutili, domande, problemi con più operazioni, domande nascoste, problemi al contrario, con l’età, con i soldi e con il tempo. 100 esercizi con soluzioni.",
              "Prima la domanda, poi i dati utili.", "Domanda nascosta: rispondi prima a quella.",
              body, faq, sets, 10, grade=G)


if __name__ == "__main__":
    main()
