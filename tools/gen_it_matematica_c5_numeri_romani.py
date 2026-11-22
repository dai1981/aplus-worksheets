# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: I numeri romani (Numeri)
  python3 tools/gen_it_matematica_c5_numeri_romani.py
Simboli I V X L C D M, regole (aggiungere a destra, togliere a sinistra, al massimo tre uguali), da romano a
decimale e viceversa, confrontare, date e capitoli, sistema additivo e posizionale.
Errori: IIII invece di IV, IC invece di XCIX, leggere XL come 60.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, table

R = random.Random(70503)
G = "classe-quinta"
VALS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
SYM = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def rom(n):
    s = ""
    for v, t in VALS:
        while n >= v:
            s += t
            n -= v
    return s


def naive(n):
    """errore: solo addizione (IIII, VIIII, XXXX)"""
    s = ""
    for v, t in [(1000, "M"), (500, "D"), (100, "C"), (50, "L"), (10, "X"), (5, "V"), (1, "I")]:
        while n >= v:
            s += t
            n -= v
    return s


def add_read(s):
    """errore: leggere tutto in addizione (XL = 60)"""
    return sum(SYM[c] for c in s)


def wrong_rom(n):
    w = [naive(n)]
    r = rom(n)
    for a, b in (("IV", "VI"), ("IX", "XI"), ("XL", "LX"), ("XC", "CX"), ("CD", "DC"), ("CM", "MC")):
        if a in r:
            w.append(r.replace(a, b, 1))
    w += [rom(n + 1), rom(n - 1) if n > 1 else rom(n + 2), rom(n + 10), rom(n - 10) if n > 10 else rom(n + 5)]
    return [x for x in w if x != r]


def wrong_num(n):
    r = rom(n)
    w = [add_read(r), n + 10, n - 10 if n > 10 else n + 5, n + 1, n - 1 if n > 1 else n + 2]
    if "IX" in r or "XC" in r:
        w.insert(0, n + 2 if "IX" in r else n + 20)
    return [num(x) for x in w if x != n]


def s1_simboli():
    t, v = R.choice(list(SYM.items()))
    if R.random() < 0.5:
        return mcq("Quanto vale il simbolo romano <b>%s</b>?" % t, num(v), [num(x) for x in SYM.values() if x != v][:6], "%s vale <b>%s</b>." % (t, num(v)))
    return mcq("Con quale simbolo romano si scrive %s?" % num(v), t, [x for x in SYM if x != t], "%s si scrive <b>%s</b>." % (num(v), t))


def s1_piccoli():
    n = R.randint(2, 39)
    if R.random() < 0.5:
        return mcq("Quanto vale <b>%s</b>?" % rom(n), num(n), wrong_num(n), "%s = <b>%s</b>." % (rom(n), num(n)))
    return mcq("Come si scrive %d in numeri romani?" % n, rom(n), wrong_rom(n), "%d = <b>%s</b>." % (n, rom(n)))


def s2_leggi():
    n = R.choice([R.randint(40, 399), R.randint(400, 3999)])
    return mcq("Quanto vale <b>%s</b>?" % rom(n), num(n), wrong_num(n),
               "Dividi in gruppi: %s. Totale <b>%s</b>." % (" + ".join("%s = %s" % (t * rom_count(n, v), num(v * rom_count(n, v))) for v, t in VALS if rom_count(n, v)), num(n)))


def rom_count(n, v):
    c = 0
    for vv, t in VALS:
        k, n = divmod(n, vv)
        if vv == v:
            c = k
    return c


def s2_scrivi():
    n = R.choice([R.randint(40, 399), R.randint(400, 3999)])
    return mcq("Come si scrive %s in numeri romani?" % num(n), rom(n), wrong_rom(n),
               "Scomponi: %s. Quindi <b>%s</b>." % (" + ".join("%s = %s" % (num(v * rom_count(n, v)), t * rom_count(n, v)) for v, t in VALS if rom_count(n, v)), rom(n)))


REGOLE = [("Quante volte al massimo si può ripetere di seguito lo stesso simbolo?", "3 volte", ["2 volte", "4 volte", "quante si vuole"]),
          ("Quali simboli non si ripetono mai?", "V, L e D", ["I, X e C", "M e C", "tutti si ripetono"]),
          ("Un simbolo più piccolo scritto a sinistra di uno più grande…", "si sottrae", ["si addiziona", "si moltiplica", "non si può scrivere"]),
          ("Un simbolo più piccolo scritto a destra di uno più grande…", "si addiziona", ["si sottrae", "si raddoppia", "non conta"]),
          ("Quale scrittura è corretta per 4?", "IV", ["IIII", "VI", "IIV"]),
          ("Quale scrittura è corretta per 99?", "XCIX", ["IC", "LXXXXVIIII", "XCVIIII"]),
          ("Quale scrittura è corretta per 49?", "XLIX", ["IL", "XXXXVIIII", "LIX"]),
          ("Quale scrittura è corretta per 900?", "CM", ["DCCCC", "MC", "CCM"]),
          ("Il sistema dei numeri romani è…", "additivo, senza lo zero", ["posizionale, con lo zero", "posizionale, senza lo zero", "additivo, con lo zero"]),
          ("Quale numero non si può scrivere con i numeri romani classici?", "0", ["4", "1000", "999"]),
          ("Qual è il numero più grande che si scrive con i simboli classici senza barre?", "3999", ["1000", "4000", "9999"]),
          ("Quale simbolo vale 500?", "D", ["M", "C", "L"])]


def s3_regole():
    q, a, w = R.choice(REGOLE)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s3_confronta():
    a, b = R.sample(range(10, 1999), 2)
    if abs(a - b) > 300:
        return None
    g = max(a, b)
    return mcq("Quale numero è maggiore: %s o %s?" % (rom(a), rom(b)), rom(g), [rom(min(a, b)), "sono uguali", "non si può sapere"],
               "%s = %s e %s = %s: il maggiore è <b>%s</b>." % (rom(a), num(a), rom(b), num(b), rom(g)))


def s4_calcolo():
    a, b = R.randint(5, 600), R.randint(5, 400)
    op = R.choice(["+", "−"])
    if op == "−" and a <= b:
        a, b = b, a
    r = a + b if op == "+" else a - b
    if r <= 0 or a == b:
        return None
    return mcq("Calcola e scrivi il risultato in numeri romani: %s %s %s" % (rom(a), op, rom(b)), rom(r), wrong_rom(r),
               "%s %s %s = %s, cioè <b>%s</b>." % (num(a), op, num(b), num(r), rom(r)))


EVENTI = [("Il Colosseo fu inaugurato nell’anno", 80), ("Il Pantheon fu ricostruito intorno all’anno", 125), ("Carlo Magno fu incoronato imperatore nell’anno", 800),
          ("Dante nacque nell’anno", 1265), ("Cristoforo Colombo arrivò in America nell’anno", 1492), ("Leonardo da Vinci nacque nell’anno", 1452),
          ("Galileo Galilei nacque nell’anno", 1564), ("L’Italia è diventata un regno unito nell’anno", 1861), ("Roma diventò capitale d’Italia nell’anno", 1871),
          ("La Repubblica italiana nacque nell’anno", 1946), ("Michelangelo finì la volta della Cappella Sistina nell’anno", 1512)]


def s5():
    k = R.choice(["evento", "evento", "secolo", "capitolo", "orologio"])
    if k == "evento":
        t, y = R.choice(EVENTI)
        if R.random() < 0.5:
            return mcq("%s %s. Come si scrive in numeri romani?" % (t, num(y)), rom(y), wrong_rom(y), "%s = <b>%s</b>." % (num(y), rom(y)))
        return mcq("Su una lapide c’è scritto: %s %s. Che anno è?" % (t, rom(y)), num(y), wrong_num(y), "%s = <b>%s</b>." % (rom(y), num(y)))
    if k == "secolo":
        c = R.randint(5, 21)
        return mcq("Il secolo %s va…" % rom(c), "dal %s al %s" % (num((c - 1) * 100 + 1), num(c * 100)),
                   ["dal %s al %s" % (num(c * 100), num(c * 100 + 99)), "dal %s al %s" % (num((c - 1) * 100), num((c - 1) * 100 + 99)), "dal %s al %s" % (num((c - 2) * 100 + 1), num((c - 1) * 100))],
                   "%s = %d. Il secolo %d va <b>dal %s al %s</b>." % (rom(c), c, c, num((c - 1) * 100 + 1), num(c * 100)))
    if k == "capitolo":
        a, b = R.randint(3, 19), R.randint(21, 49)
        return mcq("Un libro ha i capitoli numerati in romano. %s legge dal capitolo %s al capitolo %s compresi. Quanti capitoli legge?" % (R.choice(["Luca", "Sofia", "Marco", "Anna"]), rom(a), rom(b)),
                   num(b - a + 1), [num(b - a), num(b - a + 2), num(add_read(rom(b)) - a + 1) if add_read(rom(b)) != b else num(b + a)],
                   "%s = %d e %s = %d: %d − %d + 1 = <b>%d</b>." % (rom(a), a, rom(b), b, b, a, b - a + 1))
    h = R.randint(1, 12)
    return mcq("Su un orologio con i numeri romani la lancetta corta indica %s. Che ora è (la lancetta lunga è sul XII)?" % rom(h), "le %d" % h if h != 1 else "l’una",
               ["le %d" % (h + 1) if h < 12 else "l’una", "le %d" % add_read(rom(h)) if add_read(rom(h)) != h else "le %d" % (h - 1 if h > 2 else h + 2), "le %d" % (h + 5 if h + 5 <= 12 else h - 5)],
               "%s = %d: sono <b>%s</b>." % (rom(h), h, "le %d" % h if h != 1 else "l’una"))


def main():
    seen = set()
    sets = [
        ("Simboli e numeri piccoli", mix(R, seen, [(s1_simboli, 8), (s1_piccoli, 12)])),
        ("Da romano a decimale", mix(R, seen, [(s2_leggi, 20)])),
        ("Da decimale a romano", mix(R, seen, [(s2_scrivi, 20)])),
        ("Regole e confronti", mix(R, seen, [(s3_regole, 10), (s3_confronta, 6), (s4_calcolo, 4)])),
        ("Date, secoli e problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["I Romani usavano sette simboli: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000.",
         "Un simbolo uguale o più piccolo a <b>destra</b> si <b>addiziona</b> (VI = 6); un simbolo più piccolo a <b>sinistra</b> si <b>sottrae</b> (IV = 4).",
         "I, X, C, M si ripetono al massimo tre volte; V, L, D non si ripetono. Si sottraggono solo I (da V e X), X (da L e C), C (da D e M).",
         "Il sistema romano è <b>additivo</b> e non ha lo zero; il nostro è <b>posizionale</b>."],
        [("Scrivi 1492", ["1000 = M", "400 = CD", "90 = XC", "2 = II"], "MCDXCII")],
        [["Scrivere 4 come IIII", "Dopo tre simboli uguali si usa la sottrazione: IV."],
         ["Scrivere 99 come IC", "Scomponi: 90 + 9 = XC + IX = XCIX."],
         ["Leggere XL come 60", "X prima di L si sottrae: 50 − 10 = 40."]],
        table(["I", "V", "X", "L", "C", "D", "M"], [["1", "5", "10", "50", "100", "500", "1000"]]))
    faq = [("Perché i Romani non avevano lo zero?", "Il loro sistema serviva a contare e a scrivere quantità: lo zero come cifra è arrivato in Europa più tardi, con le cifre indo-arabe."),
           ("Dove si usano ancora i numeri romani?", "Nei secoli (XXI secolo), nei capitoli dei libri, sugli orologi, sui monumenti e nei nomi dei re e dei papi.")]
    make_unit(R, "numeri-romani", "N",
              "Conoscere sistemi di notazione dei numeri che sono o sono stati in uso in luoghi, tempi e culture diverse dalla nostra (numeri romani)",
              "I numeri romani: simboli e regole", "Numeri romani",
              "Schede di matematica per la classe quinta sui numeri romani: simboli, regole di addizione e sottrazione, da romano a decimale e viceversa, date, secoli e problemi. 100 esercizi con soluzioni.",
              "A destra si addiziona, a sinistra si sottrae.", "Al massimo tre simboli uguali di seguito.",
              body, faq, sets, 3, grade=G)


if __name__ == "__main__":
    main()
