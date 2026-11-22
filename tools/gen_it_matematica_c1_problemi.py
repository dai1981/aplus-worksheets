# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Problemi (Problemi)
  python3 tools/gen_it_matematica_c1_problemi.py
Situazioni di aggiungere, togliere, mettere insieme e confrontare entro il 20; scegliere tra + e −; la domanda giusta;
il dato che non serve; problemi con il disegno.
Errori: scegliere l’operazione da una sola parola, usare tutti i numeri del testo, rispondere senza la parola (5 invece di 5 mele).
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, Kids
import it_c1 as C

R = random.Random(70108)
G = "classe-prima"
K = Kids(R)
OPS = ["un’addizione (+)", "una sottrazione (−)"]


def s1_op():
    p = K.next()
    a, b = R.randint(5, 12), R.randint(2, 7)
    k = R.randint(0, 5)
    q = ["%s ha %d biglie. Ne trova altre %d. Quante biglie ha ora?" % (p[0], a, b),
         "Sull’albero ci sono %d mele. Ne cadono %d. Quante mele restano sull’albero?" % (a, b),
         "Nel cestino ci sono %d fragole e %d ciliegie. Quanti frutti ci sono in tutto?" % (a, b),
         "%s ha %d anni, il fratello %d. Quanti anni ha in più %s?" % (p[0], a, b, p[0]),
         "Alla festa ci sono %d bicchieri. Se ne rompono %d. Quanti bicchieri restano?" % (a, b),
         "In classe ci sono %d bambini. Ne arrivano altri %d. Quanti bambini ci sono adesso?" % (a, b)][k]
    plus = k in (0, 2, 5)
    e = "Si %s: <b>%s</b>, %d %s %d = %d." % ("aggiunge o si mette insieme" if plus else "toglie o si confronta", OPS[0] if plus else OPS[1], a, "+" if plus else "−", b, a + b if plus else a - b)
    return mcq(q + " Quale operazione serve?", OPS[0] if plus else OPS[1], [OPS[1] if plus else OPS[0], "nessuna", "tutte e due"], e)


def s2_risolvi():
    p = K.next()
    k = R.choice(["piu", "meno", "insieme", "confronto", "manca"])
    if k == "piu":
        a, b = R.randint(5, 14), R.randint(2, 6)
        return mcq("Nel pollaio ci sono %d galline. Ne arrivano %d. Quante galline ci sono adesso?" % (a, b), str(a + b), [str(a - b), str(a + b + 1), str(b)], "%d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "meno":
        a, b = R.randint(8, 20), R.randint(2, 7)
        return mcq("Sullo scaffale ci sono %d libri. %s ne prende %d. Quanti libri restano?" % (a, p[0], b), str(a - b), [str(a + b), str(a - b + 1), str(b)], "%d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "insieme":
        a, b = R.randint(3, 10), R.randint(3, 9)
        return mcq("In un giardino ci sono %d rose rosse e %d rose bianche. Quante rose ci sono in tutto?" % (a, b), str(a + b), [str(abs(a - b)), str(a + b - 1), str(a)], "%d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "confronto":
        a, b = R.randint(8, 18), R.randint(2, 7)
        return mcq("%s ha %d pennarelli, la sua amica ne ha %d. Quanti pennarelli ha in più %s?" % (p[0], a, b, p[0]), str(a - b), [str(a + b), str(a), str(b)], "%d − %d = <b>%d</b>." % (a, b, a - b))
    a, b = R.randint(2, 9), R.randint(10, 20)
    if a >= b:
        return None
    return mcq("%s vuole %d figurine. Ne ha già %d. Quante gliene mancano?" % (p[0], b, a), str(b - a), [str(a + b), str(b), str(b - a + 1)], "%d + ? = %d: mancano <b>%d</b> figurine (%d − %d)." % (a, b, b - a, b, a))


def s3_domanda():
    a, b = R.randint(6, 12), R.randint(2, 5)
    k = R.choice(["meno", "piu", "meno2", "piu2"])
    if k == "meno":
        return mcq("Nel prato ci sono %d farfalle e %d api. Il calcolo è %d − %d. Quale domanda va bene?" % (a, b, a, b), "Quante farfalle ci sono in più delle api?",
                   ["Quanti insetti ci sono in tutto?", "Quante api ci sono?", "Quante ali hanno?"], "%d − %d trova <b>quante farfalle in più</b>." % (a, b))
    if k == "meno2":
        return mcq("Nel frigo ci sono %d yogurt. La mamma ne mangia %d. Il calcolo è %d − %d. Quale domanda va bene?" % (a, b, a, b), "Quanti yogurt restano?",
                   ["Quanti yogurt c’erano?", "Quanti yogurt ha mangiato la mamma?", "Quanti yogurt compra?"], "%d − %d trova <b>quanti yogurt restano</b>." % (a, b))
    if k == "piu2":
        return mcq("In cortile giocano %d bambini; arrivano altri %d. Il calcolo è %d + %d. Quale domanda va bene?" % (a, b, a, b), "Quanti bambini giocano adesso?",
                   ["Quanti bambini sono arrivati?", "Quanti bambini vanno via?", "Quanti bambini c’erano prima?"], "%d + %d trova <b>quanti bambini ci sono adesso</b>." % (a, b))
    return mcq("Luca ha %d figurine e %d adesivi. Il calcolo è %d + %d. Quale domanda va bene?" % (a, b, a, b), "Quante cose ha in tutto?",
               ["Quante figurine ha in più degli adesivi?", "Quanti adesivi ha?", "Quante figurine regala?"], "%d + %d trova <b>quante cose in tutto</b>." % (a, b))


def s3_inutile():
    p = K.next()
    a, b, c = R.randint(8, 15), R.randint(2, 6), R.randint(6, 7)
    return mcq("%s ha %d anni. Ha %d caramelle e ne mangia %d. Quante caramelle restano? Quale numero non serve?" % (p[0], c, a, b), "%d (gli anni)" % c,
               ["%d (le caramelle che ha)" % a, "%d (le caramelle mangiate)" % b, "servono tutti"], "Servono solo le caramelle: %d − %d = %d. <b>Gli anni non servono</b>." % (a, b, a - b))


def s4_disegno():
    k = R.choice(C.KINDS)
    kind = R.choice(["barrati", "due", "scatola"])
    if kind == "barrati":
        a = R.randint(5, 12)
        b = R.randint(1, a - 2)
        return mcq(C.barrati(a, k, b) + "Le %s barrate sono state tolte. %s restano?" % (C.nome(k), C.Q(k)) if C.COSE[k][2] == "f" else
                   C.barrati(a, k, b) + "I %s barrati sono stati tolti. %s restano?" % (C.nome(k), C.Q(k)), str(a - b), [str(a), str(b), str(a + b)], "%d − %d = <b>%d</b>." % (a, b, a - b))
    if kind == "due":
        a, b = R.randint(2, 9), R.randint(2, 9)
        return mcq(C.due(a, k, b, k, "+") + "Quale problema racconta questo disegno?", "Ci sono %d %s e ne arrivano %d." % (a, C.nome(k, a), b),
                   ["Ci sono %d %s e ne vanno via %d." % (a, C.nome(k, a), b), "Ci sono %d %s in tutto." % (a, C.nome(k, a)), "Ci sono %d %s e ne arrivano %d." % (b, C.nome(k, b), b + 1)],
                   "Il segno + dice che si aggiunge: %d + %d = %d." % (a, b, a + b))
    tot = R.randint(6, 15)
    a = R.randint(2, min(10, tot - 1))
    return mcq(C.scatola(a, k) + "In tutto sono %d. %s sono nascost%s nella scatola?" % (tot, C.Q(k), "e" if C.COSE[k][2] == "f" else "i"), str(tot - a), [str(a), str(tot), str(tot + a)],
               "%d + ? = %d: nella scatola ce ne sono <b>%d</b>." % (a, tot, tot - a))


def s5_due_passi():
    p = K.next()
    a, b, c = R.randint(5, 10), R.randint(2, 5), R.randint(1, 4)
    k = R.choice(["vince", "bus", "fiori"])
    if k == "vince":
        return mcq("%s ha %d biglie. Ne vince %d, poi ne perde %d. Quante biglie ha alla fine?" % (p[0], a, b, c), str(a + b - c), [str(a + b), str(a + b + c), str(a - b - c) if a > b + c else str(a + b - c + 1)],
                   "%d + %d = %d; %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b - c))
    if k == "bus":
        return mcq("Sul pulmino ci sono %d bambini. Alla fermata ne salgono %d e ne scendono %d. Quanti bambini ci sono adesso?" % (a, b, c), str(a + b - c), [str(a + b + c), str(a + b), str(a - c)],
                   "%d + %d − %d = <b>%d</b>." % (a, b, c, a + b - c))
    return mcq("Nel vaso ci sono %d fiori. La nonna ne aggiunge %d e la mamma %d. Quanti fiori ci sono?" % (a, b, c), str(a + b + c), [str(a + b), str(a + b - c), str(a + b + c + 1)],
               "%d + %d + %d = <b>%d</b>." % (a, b, c, a + b + c))


def main():
    seen = set()
    sets = [
        ("Più o meno?", mix(R, seen, [(s1_op, 20)])),
        ("Risolvi", mix(R, seen, [(s2_risolvi, 20)])),
        ("La domanda e il dato che non serve", mix(R, seen, [(s3_domanda, 8), (s3_inutile, 12)])),
        ("Problemi con il disegno", mix(R, seen, [(s4_disegno, 20)])),
        ("Problemi in due passi", mix(R, seen, [(s5_due_passi, 20)])),
    ]
    body = lesson(
        ["Leggi bene la storia e la <b>domanda</b>. Immagina la scena o fai un disegno.",
         "Se si aggiunge o si mette insieme usi l’<b>addizione</b> (+). Se si toglie o si confronta usi la <b>sottrazione</b> (−).",
         "A volte nel testo c’è un numero che non serve: usa solo i dati che rispondono alla domanda.",
         "Rispondi con una frase completa: «Restano 7 mele»."],
        [("Ci sono 9 palloncini. Ne scoppiano 3. Quanti restano?", ["si toglie: −", "9 − 3 = 6"], "restano 6 palloncini")],
        [["Scegliere l’operazione da una sola parola", "Immagina la storia: si aggiunge o si toglie?"],
         ["Usare tutti i numeri del testo", "L’età o il giorno spesso non servono."],
         ["Rispondere solo con il numero", "Scrivi anche che cosa conti: 6 palloncini."]],
        table(["Parola nella storia", "Di solito…"], [["arrivano, trova, aggiunge, in tutto", "+"], ["restano, mangia, perde, scendono", "−"], ["quanti in più, quanti mancano", "−"]]))
    faq = [("Come si aiuta un bambino con i problemi?", "Facendogli raccontare la storia con parole sue, mimarla con oggetti o disegnarla prima di fare il calcolo."),
           ("Le parole chiave bastano?", "No: aiutano, ma bisogna capire la situazione. «In tutto» può anche voler dire che si conta quello che resta da comprare.")]
    make_unit(R, "problemi", "P",
              "Riconoscere, rappresentare e risolvere semplici problemi con addizioni e sottrazioni, descrivendo il procedimento seguito",
              "Problemi con addizioni e sottrazioni", "Problemi",
              "Schede di matematica per la classe prima sui problemi: aggiungere, togliere, mettere insieme e confrontare entro il 20, scegliere + o −, la domanda giusta, il dato che non serve, problemi con il disegno e in due passi. 100 esercizi con soluzioni.",
              "Si aggiunge? +. Si toglie? −.", "Rispondi con una frase completa.",
              body, faq, sets, 8, grade=G)


if __name__ == "__main__":
    main()
