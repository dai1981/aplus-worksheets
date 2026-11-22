# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Ritmi, classificazioni e dati (Relazioni, dati e previsioni)
  python3 tools/gen_it_matematica_c1_ritmi_classificazioni_e_dati.py
Ritmi (sequenze che si ripetono), l’intruso, classificare secondo una caratteristica, contare per gruppi,
leggere tabelle e grafici semplici, eventi certi, possibili, impossibili.
Errori: continuare il ritmo dall’inizio, contare due volte lo stesso oggetto, leggere la colonna sbagliata.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table
import gen_it_matematica_c2_classificazioni_e_dati as K2
import gen_it_matematica_c3_dati_e_probabilita as D3
import it_c1 as C
import k_pics

R = random.Random(70114)
G = "classe-prima"
PAT = ["AB", "AB", "ABC", "AAB", "ABB", "AABB"]


def s1_ritmo():
    p = R.choice(PAT)
    ks = R.sample(C.KINDS, len(set(p)))
    m = {ch: ks[i] for i, ch in enumerate(sorted(set(p)))}
    seq = [m[ch] for ch in (p * 4)][: R.randint(len(p) * 2, len(p) * 2 + len(p) - 1)]
    nxt = m[(p * 5)[len(seq)]]
    pic = C.ritmo([("obj", k) for k in seq], 1)
    others = [x for x in C.KINDS if x != nxt]
    R.shuffle(others)
    opts = [C.un_(k) for k in ks if k != nxt] + [C.un_(k) for k in others[:3]]
    return mcq(pic + "Che cosa viene dopo nel ritmo?", C.un_(nxt), opts, "Il ritmo si ripete: %s. Dopo viene <b>%s</b>." % (" ".join(C.nome(m[ch], 1) for ch in p), C.un_(nxt)))


def s1_numeri():
    a = R.randint(1, 5)
    st = R.choice([1, 2, 3])
    seq = [a + st * i for i in range(5)]
    if R.random() < 0.4:
        seq = [x for i in range(3) for x in (a, a + st)][:5]
        nxt = a if len(seq) % 2 == 0 else a + st
        return mcq(C.carte([str(x) for x in seq] + ["?"]) + "Che numero viene dopo?", str(nxt), [str(seq[-1]), str(seq[-1] + st), str(nxt + 1)],
                   "Si ripete %d, %d: viene <b>%d</b>." % (a, a + st, nxt))
    nxt = seq[-1] + st
    return mcq(C.carte([str(x) for x in seq] + ["?"]) + "Che numero viene dopo?", str(nxt), [str(nxt + 1), str(seq[-1] + 1) if st > 1 else str(nxt + 2), str(seq[-1])],
               "Ogni volta si aggiunge %d: %d + %d = <b>%d</b>." % (st, seq[-1], st, nxt))


def s3_conta():
    ks = R.sample(C.KINDS, 3)
    ns = [R.randint(2, 7) for _ in ks]
    if sum(ns) > 24:
        return None
    pic = C.it(k_pics.mixed_svg(list(zip(ks, ns)), R.randint(1, 9999)), "oggetti mescolati")
    i = R.randrange(3)
    k = R.random()
    if k < 0.6:
        return mcq(pic + "%s ci sono?" % C.Q(ks[i]), str(ns[i]), [str(ns[i] + 1), str(ns[i] - 1) if ns[i] > 1 else "3", str(sum(ns))], "Conta solo %s: <b>%d</b>." % (C.nome(ks[i]), ns[i]))
    if len(set(ns)) < 3:
        return None
    j = ns.index(max(ns))
    return mcq(pic + "Di quale oggetto ce ne sono di più?", C.nome(ks[j]), [C.nome(x) for x in ks if x != ks[j]] + ["sono tanti uguali"],
               "%s: ce ne sono di più di <b>%s</b>." % (", ".join("%d %s" % (n, C.nome(k, n)) for k, n in zip(ks, ns)), C.nome(ks[j])))


def s4_tab():
    it = D3.s1_tabella()
    return it


def s4_ist():
    return D3.s2_istogramma()


def main():
    K2.R = R
    D3.R = R
    seen = set()
    sets = [
        ("I ritmi", mix(R, seen, [(s1_ritmo, 14), (s1_numeri, 6)])),
        ("L’intruso e i gruppi", mix(R, seen, [(K2.s1_intruso, 10), (K2.s1_gruppo, 10)])),
        ("Contare per gruppi", mix(R, seen, [(s3_conta, 20)])),
        ("Tabelle e grafici", mix(R, seen, [(s4_tab, 10), (s4_ist, 10)])),
        ("Certo, possibile, impossibile", mix(R, seen, [(D3.s4_eventi, 10), (D3.s4_sacchetto, 10)])),
    ]
    body = lesson(
        ["Un <b>ritmo</b> è una sequenza che si ripete sempre uguale: mela, stella, mela, stella… Per continuarlo trova il pezzo che si ripete.",
         "<b>Classificare</b> vuol dire mettere insieme le cose che hanno una stessa caratteristica (colore, forma, se volano…). L’<b>intruso</b> è quello che non c’entra.",
         "Le risposte di un’indagine si contano e si scrivono in una <b>tabella</b> o in un <b>grafico</b>.",
         "Un evento può essere <b>certo</b> (succede sicuramente), <b>possibile</b> (può succedere) o <b>impossibile</b> (non può succedere)."],
        [("mela, stella, stella, mela, stella, stella, …", ["il pezzo che si ripete: mela, stella, stella"], "mela")],
        [["Ricominciare il ritmo dall’inizio a caso", "Guarda l’ultimo pezzo e continua da lì."],
         ["Contare due volte lo stesso oggetto", "Segna ogni oggetto dopo averlo contato."],
         ["Leggere la colonna sbagliata del grafico", "Metti il dito sotto il nome, poi sali."]],
        table(["Evento", "Tipo"], [["Domani sorge il sole", "certo"], ["Oggi piove", "possibile"], ["Il gatto vola", "impossibile"]]))
    faq = [("Perché si fanno i ritmi in classe prima?", "Perché allenano a scoprire regole: è la base per contare a salti, per le tabelline e per il ragionamento."),
           ("Che tipo di grafici si usano in classe prima?", "Grafici semplici con colonne o simboli, costruiti con i dati della classe: il colore preferito, la merenda, il tempo atmosferico.")]
    make_unit(R, "ritmi-classificazioni-e-dati", "D",
              "Riconoscere e costruire ritmi e sequenze; classificare oggetti in base a una proprietà; leggere e rappresentare dati con tabelle e grafici; riconoscere eventi certi, possibili, impossibili",
              "Ritmi, classificazioni e dati", "Ritmi, classificazioni e dati",
              "Schede di matematica per la classe prima su ritmi, classificazioni e dati: continuare un ritmo, l’intruso, classificare, contare per gruppi, tabelle e grafici, certo, possibile e impossibile. 100 esercizi con soluzioni.",
              "Nel ritmo trova il pezzo che si ripete.", "Certo, possibile, impossibile.",
              body, faq, sets, 14, grade=G)


if __name__ == "__main__":
    main()
