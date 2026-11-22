# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Statistica (Dati e previsioni)
  python3 tools/gen_it_matematica_m1_statistica.py
Indagine statistica, popolazione e carattere (qualitativo e quantitativo), frequenza assoluta, relativa e percentuale,
moda, media, mediana e campo di variazione, istogrammi, aerogrammi e tabelle a doppia entrata.
Errori: dimenticare di ordinare i dati per la mediana, dividere per il numero sbagliato nella media, sommare le frequenze relative oltre 1.
"""
import random
from it_media import M, L, unit, mix, table, W, fq, d, Kids
from fractions import Fraction as Fr
import gen_it_matematica_c5_statistica_e_probabilita as ST5
import gen_it_matematica_c3_dati_e_probabilita as D3

R = random.Random(71115)
G = "prima-media"


def s1_carattere():
    q, a, w = R.choice([("Il colore preferito dei ragazzi di una classe è un carattere…", "qualitativo", ["quantitativo", "numerico", "continuo"]),
                        ("L’altezza degli alunni di una scuola è un carattere…", "quantitativo", ["qualitativo", "nominale", "non misurabile"]),
                        ("Il numero di fratelli è un carattere…", "quantitativo", ["qualitativo", "non misurabile", "nominale"]),
                        ("Lo sport preferito è un carattere…", "qualitativo", ["quantitativo", "numerico", "misurabile"]),
                        ("In un’indagine sugli studenti di una scuola, gli studenti sono…", "la popolazione (le unità statistiche)", ["il carattere", "la frequenza", "la moda"]),
                        ("Quando si intervista solo una parte della popolazione si usa…", "un campione", ["un censimento", "una moda", "un aerogramma"]),
                        ("Per rappresentare le parti di un tutto in percentuale è adatto…", "l’aerogramma (grafico a torta)", ["il diagramma cartesiano", "la tabella a doppia entrata", "nessun grafico"]),
                        ("Per mostrare come cambia una temperatura nel tempo è adatto…", "il diagramma cartesiano (a linee)", ["l’aerogramma", "l’ideogramma", "il diagramma di Venn"])])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s2_freq():
    cats = R.choice([["calcio", "nuoto", "danza", "basket"], ["rosso", "blu", "verde", "giallo"], ["cane", "gatto", "pesce", "nessuno"], ["pizza", "pasta", "riso", "insalata"]])
    tot = R.choice([20, 25, 40, 50])
    vals = [R.randint(1, tot // 2) for _ in cats[:-1]]
    if sum(vals) >= tot:
        return None
    vals.append(tot - sum(vals))
    i = R.randrange(len(cats))
    tab = table(["Risposta", "Frequenza assoluta"], [[c, str(v)] for c, v in zip(cats, vals)])
    k = R.choice(["rel", "perc", "tot"])
    if k == "rel":
        return M("%sQual è la frequenza relativa di «%s»?" % (tab, cats[i]), fq(Fr(vals[i], tot)), W(fq(Fr(vals[i], 100)), str(vals[i]), fq(Fr(tot, vals[i])) if vals[i] else None, fq(Fr(vals[i] + 1, tot))),
                 "Frequenza relativa = frequenza assoluta : totale = %d/%d = <b>%s</b>." % (vals[i], tot, fq(Fr(vals[i], tot))))
    if k == "perc":
        p = Fr(vals[i] * 100, tot)
        if p.denominator != 1:
            return None
        return M("%sQual è la frequenza percentuale di «%s»?" % (tab, cats[i]), "%d%%" % p, W("%d%%" % vals[i], "%d%%" % (100 - p), "%d%%" % (p + 5)), "%d : %d = %s = <b>%d%%</b>." % (vals[i], tot, d(Fr(vals[i], tot)), p))
    return M("%sQuante persone sono state intervistate?" % tab, str(tot), W(len(cats), max(vals), tot + 1, tot - min(vals)), "Somma delle frequenze assolute: %s = <b>%d</b>." % (" + ".join(map(str, vals)), tot))


def s3_indici():
    return ST5.s1_moda_media()


def s3_media_inversa():
    n = R.randint(4, 6)
    m = R.randint(6, 9)
    vals = [R.randint(5, 10) for _ in range(n - 1)]
    x = m * n - sum(vals)
    if not 1 <= x <= 10:
        return None
    return M("I voti di Luca sono %s. Che voto deve prendere nella prossima verifica per avere la media del %d?" % (", ".join(map(str, vals)), m), str(x), W(m, x + 1, x - 1, m * (n - 1) - sum(vals) if m * (n - 1) - sum(vals) > 0 else None),
             "Con %d voti la somma deve essere %d × %d = %d; %d − %d = <b>%d</b>." % (n, n, m, m * n, m * n, sum(vals), x))


def main():
    for m in (ST5, D3):
        m.R = R
    ST5.K = Kids(R)
    seen = set()
    sets = [
        ("Indagine e carattere", mix(R, seen, [(s1_carattere, 8), (D3.s1_tabella, 12)])),
        ("Frequenze assolute, relative, percentuali", mix(R, seen, [(s2_freq, 20)])),
        ("Moda, media, mediana", mix(R, seen, [(s3_indici, 16), (s3_media_inversa, 4)])),
        ("Leggere i grafici", mix(R, seen, [(ST5.s2_grafico, 10), (ST5.s3_torta, 10)])),
        ("Tabelle a doppia entrata e problemi", mix(R, seen, [(D3.s3_doppia, 10), (s3_media_inversa, 10)])),
    ]
    body = L(["Un’<b>indagine statistica</b> studia un <b>carattere</b> (qualitativo, come il colore, o quantitativo, come l’altezza) su una <b>popolazione</b> o su un <b>campione</b>.",
              "<b>Frequenza assoluta</b>: quante volte compare un dato. <b>Frequenza relativa</b>: frequenza assoluta : totale. <b>Percentuale</b>: relativa × 100.",
              "<b>Moda</b>: il dato più frequente. <b>Media</b>: somma dei dati : numero dei dati. <b>Mediana</b>: il dato centrale dei dati ordinati (con un numero pari di dati, la media dei due centrali).",
              "I dati si rappresentano con istogrammi, ideogrammi, aerogrammi e diagrammi cartesiani."],
             [("Dati: 4, 7, 7, 8, 9", ["moda 7", "media 35 : 5 = 7", "mediana 7", "campo 9 − 4 = 5"], "moda, media e mediana 7")],
             [["Calcolare la mediana senza ordinare i dati", "Prima ordina, poi prendi il centrale."],
              ["Dividere la somma per il numero sbagliato", "Conta tutti i dati, anche quelli ripetuti."],
              ["Pensare che la moda sia la frequenza più alta", "La moda è il dato, non il numero di volte."]],
             table(["Indice", "Come si calcola"], [["moda", "dato più frequente"], ["media", "somma : numero dei dati"], ["mediana", "dato centrale dei dati ordinati"], ["campo di variazione", "massimo − minimo"]]))
    faq = [("Quando conviene la mediana invece della media?", "Quando ci sono dati molto diversi dagli altri: in 2, 3, 3, 4, 40 la media (10,4) è «tirata su» dal 40, la mediana (3) rappresenta meglio il gruppo."),
           ("La somma delle frequenze relative quanto fa?", "Sempre 1 (cioè 100%), perché ogni dato è stato contato una volta.")]
    unit(G, R, "statistica", "Q",
         "Rappresentare insiemi di dati; in situazioni significative confrontare dati usando le distribuzioni delle frequenze e delle frequenze relative; scegliere e utilizzare valori medi (moda, mediana, media aritmetica)",
         "Statistica: frequenze, moda, media e mediana", "Statistica",
         "Schede di matematica per la prima media sulla statistica: indagine e carattere, frequenze assolute, relative e percentuali, moda, media, mediana, campo di variazione, istogrammi, aerogrammi e problemi. 100 esercizi con soluzioni.",
         "Moda: il più frequente. Media: somma : numero dei dati.", "Mediana: il centrale dei dati ordinati.",
         body, faq, sets, 15)


if __name__ == "__main__":
    main()
