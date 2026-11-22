# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: I numeri fino a 10 (Numeri)
  python3 tools/gen_it_matematica_c1_numeri_fino_a_10.py
Contare oggetti, riconoscere quantità (dadi, schema del dieci), leggere e scrivere i numeri in cifre e in parole,
lo zero, uno in più e uno in meno, contare avanti e indietro.
Errori: contare due volte lo stesso oggetto, saltare un numero, confondere 6 e 9.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table
import it_c1 as C

R = random.Random(70101)
G = "classe-prima"


def w(n, hi=10):
    return [str(x) for x in (n + 1, n - 1, n + 2, n - 2, 9 if n == 6 else 6 if n == 9 else None) if x is not None and 0 <= x <= hi and x != n]


def s1_conta():
    n = R.randint(1, 10)
    k = R.choice(C.KINDS)
    pic = C.riga(n, k, 5) if R.random() < 0.5 else C.mucchio(n, k, R.randint(1, 999))
    return mcq(pic + "%s ci sono?" % C.Q(k), str(n), w(n), "Conta e tocca ogni oggetto una volta sola: <b>%d</b>." % n)


def s1_dadi():
    k = R.choice(["dado", "dieci", "dieci"])
    if k == "dado":
        a = R.randint(1, 6)
        if R.random() < 0.5:
            return mcq(C.dado([a]) + "Quanti puntini ci sono sul dado?", str(a), w(a, 6) + ["7"], "Riconosci la figura dei puntini: <b>%d</b>." % a)
        b = R.randint(1, 6)
        if a + b > 10:
            return None
        return mcq(C.dado([a, b]) + "Quanti puntini ci sono in tutto?", str(a + b), w(a + b), "%d e %d: in tutto <b>%d</b>." % (a, b, a + b))
    n = R.randint(1, 10)
    return mcq(C.dieci(n) + "Quanti pallini ci sono?", str(n), w(n), "Una riga piena ha 5 pallini. %s<b>%d</b>." % ("5 e %d: " % (n - 5) if n > 5 else "", n))


def s2_parole():
    n = R.randint(0, 10)
    if R.random() < 0.5:
        return mcq("Come si scrive in cifre «%s»?" % C.num_parola(n), str(n), w(n), "«%s» si scrive <b>%d</b>." % (C.num_parola(n), n))
    return mcq("Come si scrive in parole il numero %d?" % n, C.num_parola(n), [C.num_parola(int(x)) for x in w(n)], "%d si scrive <b>%s</b>." % (n, C.num_parola(n)))


def s2_zero():
    k = R.choice(C.KINDS)
    if R.random() < 0.5:
        return mcq(C.piatto(0, k) + "%s ci sono nel piatto?" % C.Q(k), "0", ["1", "10", "2"], "Il piatto è vuoto: <b>0</b> (zero).")
    n = R.randint(1, 5)
    return mcq(C.barrati(n, k, n) + "Togli tutti gli oggetti barrati. %s restano?" % C.Q(k), "0", [str(n), "1", str(n + 1)], "Sono barrati tutti: ne restano <b>0</b>.")


def s3_piu_meno():
    n = R.randint(1, 9)
    k = R.choice(C.KINDS)
    if R.random() < 0.5:
        return mcq(C.riga(n, k, 5) + "Aggiungi %s. %s ci sono adesso?" % (C.un_(k), C.Q(k)), str(n + 1), [str(n), str(n + 2), str(n - 1)] if n > 1 else ["1", "3", "0"],
                   "Uno in più: %d + 1 = <b>%d</b>." % (n, n + 1))
    n += 1
    return mcq(C.riga(n, k, 5) + "Togli %s. %s restano?" % (C.un_(k), C.Q(k)), str(n - 1), [str(n), str(n + 1), str(n - 2)],
               "Uno in meno: %d − 1 = <b>%d</b>." % (n, n - 1))


def s3_prima_dopo():
    n = R.randint(1, 9)
    if R.random() < 0.5:
        return mcq("Quale numero viene subito <b>dopo</b> il %d?" % n, str(n + 1), [str(n - 1), str(n + 2), str(n)], "Contando: %d, <b>%d</b>." % (n, n + 1))
    return mcq("Quale numero viene subito <b>prima</b> del %d?" % n, str(n - 1), [str(n + 1), str(n - 2) if n > 1 else "2", str(n)], "Contando: <b>%d</b>, %d." % (n - 1, n))


def s4_sequenza():
    a = R.randint(0, 6)
    up = R.random() < 0.6
    seq = list(range(a, a + 5)) if up else list(range(a + 4, a - 1, -1))
    i = R.randint(1, 4)
    ans = seq[i]
    show = [str(x) if j != i else "?" for j, x in enumerate(seq)]
    return mcq(C.carte(show) + "Quale numero manca?", str(ans), [str(x) for x in (ans + 1, ans - 1, ans + 2) if 0 <= x <= 10], "Si conta %s: manca il <b>%d</b>." % ("avanti" if up else "indietro", ans))


def s4_retta():
    n = R.randint(1, 9)
    marks = {v: str(v) for v in (0, 5, 10)}
    marks[n] = "?"
    return mcq(C.retta(0, 10, marks) + "Quale numero va al posto del «?»?", str(n), w(n), "Conta i trattini partendo da 0: <b>%d</b>." % n)


def s5():
    k = R.choice(C.KINDS)
    kind = R.choice(["scatola", "piatti", "dita", "dado", "fila"])
    if kind == "scatola":
        n = R.randint(2, 8)
        return mcq("Nella scatola ci sono %s. Ne metto dentro un’altra. Quante sono adesso?" % C.cose(k, n), str(n + 1), [str(n), str(n + 2), str(n - 1)], "%d e una in più: <b>%d</b>." % (n, n + 1))
    if kind == "piatti":
        a, b = R.randint(1, 5), R.randint(1, 5)
        if a == b:
            return None
        big = "il primo" if a > b else "il secondo"
        return mcq(C.due(a, k, b, k, "|") + "In quale gruppo ci sono più %s?" % C.nome(k), big, ["il secondo" if big == "il primo" else "il primo", "sono uguali", "nessuno"],
                   "%d e %d: ci sono più %s nel <b>%s</b> gruppo." % (a, b, C.nome(k), big.split()[1]))
    if kind == "dita":
        n = R.randint(6, 10)
        return mcq("Alzo tutte le dita di una mano e %d dita dell’altra. Quante dita alzo?" % (n - 5), str(n), w(n), "5 e %d: <b>%d</b>." % (n - 5, n))
    if kind == "dado":
        a = R.randint(1, 6)
        return mcq("Lancio un dado ed esce %d. Al lancio dopo esce un puntino in più. Che numero esce?" % a if a < 6 else "Il dado ha 6 facce. Qual è il numero più grande su un dado?", str(a + 1) if a < 6 else "6",
                   [str(a), str(a + 2), str(a - 1) if a > 1 else "0"] if a < 6 else ["5", "10", "7"], "La risposta è <b>%s</b>." % (str(a + 1) if a < 6 else "6"))
    n = R.randint(3, 9)
    p = R.randint(1, n)
    return mcq("In fila ci sono %d bambini. Marco è il %d° da sinistra. Quanti bambini ci sono prima di lui?" % (n, p), str(p - 1), [str(p), str(p + 1), str(n - p)] if n - p not in (p - 1, p, p + 1) else [str(p), str(p + 1), str(n)],
               "Se è il %d°, prima di lui ci sono <b>%d</b> bambini." % (p, p - 1))


def main():
    seen = set()
    sets = [
        ("Contare gli oggetti", mix(R, seen, [(s1_conta, 20)])),
        ("Dadi e schema del dieci", mix(R, seen, [(s1_dadi, 20)])),
        ("Numeri in cifre e in parole", mix(R, seen, [(s2_parole, 14), (s2_zero, 6)])),
        ("Uno in più, uno in meno", mix(R, seen, [(s3_piu_meno, 8), (s3_prima_dopo, 6), (s4_sequenza, 3), (s4_retta, 3)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Per contare tocca ogni oggetto <b>una volta sola</b> e di’ un numero per ogni oggetto. L’ultimo numero che dici è quanti sono.",
         "I numeri da 0 a 10: zero, uno, due, tre, quattro, cinque, sei, sette, otto, nove, dieci.",
         "<b>0</b> (zero) vuol dire «niente».",
         "Il numero che viene <b>dopo</b> è uno in più; quello che viene <b>prima</b> è uno in meno."],
        [("Quante mele? (3 mele e 2 mele)", ["conto: 1, 2, 3, 4, 5"], "5")],
        [["Contare due volte lo stesso oggetto", "Segna ogni oggetto dopo averlo contato."],
         ["Saltare un numero", "Conta piano, con il dito."],
         ["Confondere 6 e 9", "Il 6 ha la pancia in basso, il 9 in alto."]],
        table(["Cifra", "Parola"], [[str(n), C.num_parola(n)] for n in range(0, 11)]))
    faq = [("Come si aiuta un bambino a contare bene?", "Facendogli toccare o spostare ogni oggetto mentre dice il numero, una volta sola."),
           ("A che cosa serve lo schema del dieci?", "Aiuta a vedere i numeri senza contare uno per uno: 5 è una riga piena, 10 sono due righe.")]
    make_unit(R, "numeri-fino-a-10", "N",
              "Contare oggetti o eventi, a voce e mentalmente, in senso progressivo e regressivo; leggere e scrivere i numeri naturali in notazione decimale",
              "I numeri fino a 10", "Numeri fino a 10",
              "Schede di matematica per la classe prima sui numeri fino a 10: contare gli oggetti, dadi e schema del dieci, numeri in cifre e in parole, lo zero, uno in più e uno in meno, problemi con le figure. 100 esercizi con soluzioni.",
              "Conta ogni oggetto una volta sola.", "Dopo = uno in più, prima = uno in meno.",
              body, faq, sets, 1, grade=G)


if __name__ == "__main__":
    main()
