# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Classificazioni, dati e previsioni (Relazioni, dati e previsioni)
  python3 tools/gen_it_matematica_c2_classificazioni_e_dati.py
Classificare in base a una proprietà (e a due: diagramma di Venn), l’intruso, tabelle e tacche, ideogrammi e
istogrammi semplici, la moda, eventi certi, possibili, impossibili.
Errori: dimenticare un elemento, mettere un elemento in due insiemi sbagliati, contare i simboli senza la legenda.
"""
import random
from it_common import mcq, lesson, make_unit, mix
import gen_it_matematica_c3_dati_e_probabilita as D3
import it_c2 as C

R = random.Random(70218)
G = "classe-seconda"

ANIMALI = {"vola": ["l’aquila", "il passero", "l’ape", "la farfalla", "il pipistrello"], "nuota": ["il pesce", "il delfino", "la balena", "lo squalo", "la medusa"],
           "cammina": ["il cane", "il gatto", "il cavallo", "la mucca", "il leone"]}
CIBI = {"frutta": ["la mela", "la pera", "la banana", "l’arancia", "la fragola"], "verdura": ["la carota", "la zucchina", "il pomodoro", "l’insalata", "il cavolo"],
        "dolci": ["la torta", "il gelato", "il biscotto", "la caramella", "il cioccolato"]}


def s1_intruso():
    grp = R.choice([ANIMALI, CIBI])
    a, b = R.sample(list(grp), 2)
    three = R.sample(grp[a], 3)
    x = R.choice(grp[b])
    items = three + [x]
    R.shuffle(items)
    return mcq("Chi è l’intruso? %s" % ", ".join(items), x, three, "%s non %s come gli altri: <b>%s</b> è l’intruso." % (x[0].upper() + x[1:], {"vola": "vola", "nuota": "nuota", "cammina": "cammina", "frutta": "è frutta", "verdura": "è verdura", "dolci": "è un dolce"}[a], x))


def s1_gruppo():
    grp = R.choice([ANIMALI, CIBI])
    a = R.choice(list(grp))
    x = R.choice(grp[a])
    lab = {"vola": "animali che volano", "nuota": "animali che nuotano", "cammina": "animali che camminano", "frutta": "frutta", "verdura": "verdura", "dolci": "dolci"}
    return mcq("In quale gruppo metti %s?" % x, lab[a], [lab[k] for k in grp if k != a] + ["in nessun gruppo"], "%s va tra <b>%s</b>." % (x[0].upper() + x[1:], lab[a]))


NUM_PROP = [("pari", lambda n: n % 2 == 0), ("dispari", lambda n: n % 2 == 1), ("maggiori di 50", lambda n: n > 50), ("minori di 20", lambda n: n < 20), ("con la cifra delle unità 5", lambda n: n % 10 == 5)]


def s2_numeri():
    name, f = R.choice(NUM_PROP)
    ns = R.sample(range(1, 100), 8)
    ok = [n for n in ns if f(n)]
    if not 1 <= len(ok) <= 5:
        return None
    return mcq("Quanti numeri sono %s? %s" % (name, ", ".join(map(str, ns))), str(len(ok)), [str(len(ok) + 1), str(len(ok) - 1) if len(ok) > 1 else "0", str(8 - len(ok))],
               "Sono: %s. In tutto <b>%d</b>." % (", ".join(map(str, ok)), len(ok)))


def s2_venn():
    ns = R.sample(range(1, 40), 9)
    pa = lambda n: n % 2 == 0
    pb = lambda n: n > 20
    both = [n for n in ns if pa(n) and pb(n)]
    q = R.choice(["entrambi", "nessuno"])
    if q == "entrambi":
        return mcq("Numeri: %s. Quanti sono pari <b>e</b> maggiori di 20?" % ", ".join(map(str, ns)), str(len(both)), [str(len([n for n in ns if pa(n)])), str(len([n for n in ns if pb(n)])), str(len(both) + 1)],
                   "Pari e maggiori di 20: %s. Sono <b>%d</b>." % (", ".join(map(str, both)) or "nessuno", len(both)))
    none = [n for n in ns if not pa(n) and not pb(n)]
    return mcq("Numeri: %s. Quanti non sono né pari né maggiori di 20?" % ", ".join(map(str, ns)), str(len(none)), [str(len(none) + 1), str(9 - len(none)), str(len(both))],
               "Dispari e minori o uguali a 20: %s. Sono <b>%d</b>." % (", ".join(map(str, none)) or "nessuno", len(none)))


def main():
    D3.R = R
    seen = set()
    sets = [
        ("Classificare", mix(R, seen, [(s1_intruso, 10), (s1_gruppo, 10)])),
        ("Classificare i numeri", mix(R, seen, [(s2_numeri, 12), (s2_venn, 8)])),
        ("Tabelle e tacche", mix(R, seen, [(D3.s1_tabella, 12), (D3.s1_tacche, 8)])),
        ("Ideogrammi e istogrammi", mix(R, seen, [(D3.s2_ideogramma, 10), (D3.s2_istogramma, 10)])),
        ("Certo, possibile, impossibile", mix(R, seen, [(D3.s4_eventi, 12), (D3.s4_sacchetto, 8)])),
    ]
    body = lesson(
        ["<b>Classificare</b> vuol dire mettere insieme le cose che hanno una stessa caratteristica (il colore, la forma, se volano…).",
         "Con il <b>diagramma di Venn</b> si vede chi ha una caratteristica, chi le ha tutte e due e chi nessuna.",
         "I dati di un’indagine si contano con le <b>tacche</b> e si scrivono in una <b>tabella</b>; poi si disegna un grafico.",
         "Un evento è <b>certo</b>, <b>possibile</b> o <b>impossibile</b>."],
        [("Chi è l’intruso? cane, gatto, pesce, cavallo", ["cane, gatto, cavallo camminano", "il pesce nuota"], "il pesce")],
        [["Dimenticare un elemento", "Segna ogni elemento quando lo metti in un gruppo."],
         ["Mettere un elemento nel gruppo sbagliato", "Controlla la caratteristica scritta nel gruppo."],
         ["Contare i simboli senza leggere la legenda", "Guarda quanto vale ogni simbolo."]])
    faq = [("Perché si impara a classificare?", "Perché aiuta a ordinare le idee: in matematica si classificano numeri, figure e dati."),
           ("Che cos’è un ideogramma?", "È un grafico che usa piccoli disegni: ogni disegno vale una o più unità, come dice la legenda.")]
    make_unit(R, "classificazioni-e-dati", "D",
              "Classificare numeri, figure, oggetti in base a una o più proprietà, utilizzando rappresentazioni opportune; leggere e rappresentare dati con diagrammi, schemi e tabelle; riconoscere eventi certi, possibili, impossibili",
              "Classificazioni, dati e previsioni", "Classificazioni e dati",
              "Schede di matematica per la classe seconda su classificazioni, dati e previsioni: l’intruso, gruppi, numeri pari e maggiori di…, tabelle, tacche, ideogrammi, istogrammi, certo, possibile e impossibile. 100 esercizi con soluzioni.",
              "Classificare = mettere insieme le cose con la stessa caratteristica.", "Nel grafico guarda sempre la legenda.",
              body, faq, sets, 18, grade=G)


if __name__ == "__main__":
    main()
