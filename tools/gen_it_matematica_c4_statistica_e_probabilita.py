# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Statistica e probabilità (Relazioni, dati e previsioni)
  python3 tools/gen_it_matematica_c4_statistica_e_probabilita.py
Indagini, tabelle di frequenza, ideogrammi e istogrammi, tabelle a doppia entrata, moda, media e mediana,
eventi certi, possibili e impossibili, probabilità come frazione.
Errori: contare i simboli senza leggere la legenda, scambiare moda e media, dimenticare di ordinare i dati per la mediana.
"""
import random
from it_common import lesson, make_unit, mix, table, Kids
import gen_it_matematica_c3_dati_e_probabilita as D3
import gen_it_matematica_c5_statistica_e_probabilita as ST5

R = random.Random(70420)
G = "classe-quarta"


def main():
    for m in (D3, ST5):
        m.R = R
    ST5.K = Kids(R)
    if hasattr(D3, "K"):
        D3.K = Kids(R)
    seen = set()
    sets = [
        ("Tabelle e ideogrammi", mix(R, seen, [(D3.s1_tabella, 8), (D3.s2_ideogramma, 12)])),
        ("Istogrammi e tabelle a doppia entrata", mix(R, seen, [(ST5.s2_grafico, 12), (D3.s3_doppia, 8)])),
        ("Moda, media e mediana", mix(R, seen, [(ST5.s1_moda_media, 20)])),
        ("Certo, possibile, impossibile", mix(R, seen, [(D3.s4_eventi, 8), (D3.s4_sacchetto, 12)])),
        ("Calcolare la probabilità", mix(R, seen, [(ST5.s4_prob, 14), (ST5.s5_confronto, 6)])),
    ]
    body = lesson(
        ["Un’<b>indagine</b> raccoglie dati; si contano con le tacche, si scrivono in una <b>tabella</b> e si rappresentano con un <b>ideogramma</b> o un <b>istogramma</b>.",
         "La <b>moda</b> è il dato più frequente. La <b>media</b> si trova sommando i dati e dividendo per quanti sono. La <b>mediana</b> è il dato centrale, dopo averli ordinati.",
         "Un evento può essere <b>certo</b>, <b>possibile</b> o <b>impossibile</b>.",
         "La <b>probabilità</b> si scrive con una frazione: casi favorevoli su casi possibili. Con un dado, uscire 6 ha probabilità 1 su 6."],
        [("Voti: 5, 8, 7, 8, 6, 8, 7", ["moda: 8 (compare 3 volte)", "media: 49 : 7 = 7", "mediana: 5, 6, 7, 7, 8, 8, 8 → 7"], "moda 8, media 7, mediana 7")],
        [["Contare i simboli dell’ideogramma senza la legenda", "Guarda quanto vale ogni simbolo."],
         ["Confondere moda e media", "Moda: il più frequente. Media: somma : numero dei dati."],
         ["Cercare la mediana senza ordinare i dati", "Prima metti i dati in ordine."]],
        table(["Indice", "Come si trova"], [["moda", "il dato che compare più volte"], ["media", "somma dei dati : numero dei dati"], ["mediana", "il dato al centro, dopo averli ordinati"]]))
    faq = [("La media deve essere uno dei dati?", "No: la media di 2, 3 e 7 è 4, che non è nell’elenco."),
           ("Che differenza c’è tra «possibile» e «probabile»?", "Possibile vuol dire che può succedere; probabile che ha buone possibilità di succedere (più di altri eventi).")]
    make_unit(R, "statistica-e-probabilita", "D",
              "Rappresentare relazioni e dati e utilizzare le rappresentazioni per ricavare informazioni; usare le nozioni di moda, media aritmetica e mediana; in situazioni concrete, riconoscere eventi certi, possibili, impossibili e quantificare la probabilità",
              "Statistica e probabilità: grafici, moda e media", "Statistica e probabilità",
              "Schede di matematica per la classe quarta su statistica e probabilità: tabelle, ideogrammi, istogrammi, tabelle a doppia entrata, moda, media e mediana, eventi certi, possibili e impossibili, probabilità. 100 esercizi con soluzioni.",
              "Moda: il più frequente. Media: somma : numero dei dati.", "Probabilità = casi favorevoli su casi possibili.",
              body, faq, sets, 20, grade=G)


if __name__ == "__main__":
    main()
