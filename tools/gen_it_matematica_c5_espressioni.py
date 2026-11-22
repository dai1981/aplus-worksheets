# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Le espressioni (Numeri)
  python3 tools/gen_it_matematica_c5_espressioni.py
Ordine delle operazioni (prima × e :, poi + e −, da sinistra a destra), parentesi tonde e quadre, scrivere
l’espressione di un problema, proprietà (distributiva), problemi risolti con un’espressione.
Errori: calcolare da sinistra a destra ignorando × e :, togliere le parentesi senza calcolarle, 20 − 5 + 3 = 12.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, eur, FOIS, DIV

R = random.Random(70510)
G = "classe-quinta"
K = Kids(R)
X, Dv = " %s " % FOIS, " %s " % DIV


def ltr(tokens):
    """errore: tutto da sinistra a destra"""
    v = tokens[0]
    for i in range(1, len(tokens), 2):
        op, b = tokens[i], tokens[i + 1]
        v = v + b if op == "+" else v - b if op == "−" else v * b if op == FOIS else (v // b if b and v % b == 0 else None)
        if v is None:
            return None
    return v


def ok(tokens):
    t = list(tokens)
    i = 1
    while i < len(t):
        if t[i] in (FOIS, DIV):
            a, b = t[i - 1], t[i + 1]
            if t[i] == DIV and (b == 0 or a % b):
                return None
            t[i - 1:i + 2] = [a * b if t[i] == FOIS else a // b]
        else:
            i += 2
    v = t[0]
    for i in range(1, len(t), 2):
        v = v + t[i + 1] if t[i] == "+" else v - t[i + 1]
    return v


def show(tokens):
    return " ".join(str(x) for x in tokens)


def s1_semplice():
    k = R.choice(["+x", "x+", "-:", ":+", "+-"])
    a, b, c = R.randint(2, 30), R.randint(2, 9), R.randint(2, 9)
    t = {"+x": [a, "+", b, FOIS, c], "x+": [b, FOIS, c, "+", a], "-:": [a + 40, "−", b * c, DIV, c], ":+": [b * c, DIV, b, "+", a], "+-": [a + 20, "−", b, "+", c]}[k]
    r, wl = ok(t), ltr(t)
    w = [wl if wl != r else None, r + 1, r - 1, r + 10]
    e = ("Prima la moltiplicazione o la divisione, poi l’addizione o la sottrazione" if k != "+-" else "Solo + e −: si calcola da sinistra a destra")
    return mcq("Calcola: %s" % show(t), num(r), [num(x) for x in w if x is not None and x >= 0], "%s. <b>%s</b>." % (e, num(r)))


def s2_quattro():
    for _ in range(50):
        ops = [R.choice(["+", "−", FOIS, DIV]) for _ in range(3)]
        nums = [R.randint(2, 12) for _ in range(4)]
        t = [nums[0], ops[0], nums[1], ops[1], nums[2], ops[2], nums[3]]
        for i in range(1, 7, 2):
            if t[i] == DIV:
                t[i - 1] = t[i + 1] * R.randint(2, 9)
        r = ok(t)
        if r is not None and 0 <= r <= 200 and any(o in (FOIS, DIV) for o in ops) and any(o in ("+", "−") for o in ops):
            break
    else:
        return None
    wl = ltr(t)
    return mcq("Calcola: %s" % show(t), num(r), [num(x) for x in (wl, r + 2, r - 2, r + 10) if x is not None and x >= 0 and x != r],
               "Prima %s e %s, da sinistra a destra; poi + e −. Risultato: <b>%s</b>." % (FOIS, DIV, num(r)))


def s3_parentesi():
    k = R.choice(["t1", "t2", "q"])
    a, b, c, d = R.randint(2, 20), R.randint(2, 15), R.randint(2, 9), R.randint(1, 9)
    if k == "t1":
        e = "(%d + %d)%s%d" % (a, b, X, c)
        r, w = (a + b) * c, a + b * c
        st = "(%d + %d) = %d; %d %s %d = %d" % (a, b, a + b, a + b, FOIS, c, r)
    elif k == "t2":
        if a <= b:
            a, b = b + 3, a
        e = "%d%s(%d − %d) + %d" % (c, X, a, b, d)
        r, w = c * (a - b) + d, c * a - b + d
        st = "(%d − %d) = %d; %d %s %d = %d; + %d = %d" % (a, b, a - b, c, FOIS, a - b, c * (a - b), d, r)
    else:
        e = "[(%d + %d)%s%d − %d]%s%d" % (a, b, X, c, d, Dv, 1)
        inner = (a + b) * c - d
        dv = R.choice([x for x in (2, 3, 4, 5) if inner % x == 0] or [1])
        if dv == 1:
            return None
        e = "[(%d + %d)%s%d − %d]%s%d" % (a, b, X, c, d, Dv, dv)
        r = inner // dv
        w = (a + b * c - d) // dv if (a + b * c - d) % dv == 0 else inner
        st = "tonde: %d; quadre: %d %s %d − %d = %d; poi %s %d = %d" % (a + b, a + b, FOIS, c, d, inner, DIV, dv, r)
    return mcq("Calcola: %s" % e, num(r), [num(x) for x in (w, r + 1, r * 2, r - 1) if x >= 0 and x != r],
               "Prima le parentesi tonde, poi le quadre: %s. <b>%s</b>." % (st, num(r)))


def s4_scrivi():
    p = K.next()
    k = R.choice(["libri", "spesa", "fiori", "resto"])
    if k == "libri":
        a, b, c = R.randint(3, 9), R.randint(4, 12), R.randint(5, 20)
        q = "%s compra %d libri da %d € e un astuccio da %d €. Quale espressione calcola la spesa?" % (p[0], a, b, c)
        okx = "%d%s%d + %d" % (a, X, b, c)
        w = ["(%d + %d)%s%d" % (a, b, X, c), "%d + %d + %d" % (a, b, c), "%d%s(%d + %d)" % (a, X, b, c)]
        r = a * b + c
    elif k == "spesa":
        a, b, c = R.randint(3, 8), R.randint(2, 6), R.randint(2, 9)
        q = "Ogni bambino porta %d mele e %d pere. I bambini sono %d. Quale espressione calcola i frutti?" % (a, b, c)
        okx = "(%d + %d)%s%d" % (a, b, X, c)
        w = ["%d + %d%s%d" % (a, b, X, c), "%d%s%d + %d" % (a, X, b, c), "(%d + %d)%s%d" % (a, c, X, b)]
        r = (a + b) * c
    elif k == "fiori":
        n, g, t = R.randint(5, 9), R.randint(3, 6), R.randint(2, 5)
        q = "Un fioraio ha %d rose. Ne usa %d per un mazzo e divide le altre in %d vasi uguali. Quale espressione dà le rose in ogni vaso?" % (n * t + g, g, t)
        okx = "(%d − %d)%s%d" % (n * t + g, g, Dv, t)
        w = ["%d − %d%s%d" % (n * t + g, g, Dv, t), "%d%s%d − %d" % (n * t + g, Dv, t, g), "(%d + %d)%s%d" % (n * t + g, g, Dv, t)]
        r = n
    else:
        a, b = R.randint(2, 5), R.randint(3, 8)
        have = a * b + R.randint(5, 30)
        q = "%s ha %d €. Compra %d quaderni da %d €. Quale espressione calcola i soldi che restano?" % (p[0], have, a, b)
        okx = "%d − %d%s%d" % (have, a, X, b)
        w = ["(%d − %d)%s%d" % (have, a, X, b), "%d − %d − %d" % (have, a, b), "%d + %d%s%d" % (have, a, X, b)]
        r = have - a * b
    return mcq(q, okx, w, "L’espressione è <b>%s</b> = %s." % (okx, num(r)))


def s4_distributiva():
    a, b, c = R.randint(2, 9), R.randint(10, 40), R.randint(2, 9)
    okx = "%d%s%d + %d%s%d" % (a, X, b, a, X, c)
    return mcq("Quale espressione ha lo stesso valore di %d%s(%d + %d)?" % (a, X, b, c), okx, ["%d%s%d + %d" % (a, X, b, c), "%d + %d%s%d" % (a, b, X, c), "%d%s%d%s%d" % (a, X, b, X, c)],
               "Proprietà distributiva: moltiplichi %d per ogni addendo. <b>%s</b> = %s." % (a, okx, num(a * (b + c))))


def s5():
    p = K.next()
    k = R.choice(["cinema", "gita", "torte", "sconto", "punti"])
    if k == "cinema":
        a, b, pa, pb = R.randint(2, 3), R.randint(2, 4), R.choice([9, 10, 12]), R.choice([6, 7, 8])
        r = a * pa + b * pb
        return mcq("Al cinema vanno %d adulti (biglietto %d €) e %d bambini (biglietto %d €). Quanto spendono? (%d%s%d + %d%s%d)" % (a, pa, b, pb, a, X, pa, b, X, pb), "%d €" % r,
                   ["%d €" % ((a + b) * (pa + pb)), "%d €" % ((a + b) * pa), "%d €" % (a * pa + b)], "%d + %d = <b>%d €</b>." % (a * pa, b * pb, r))
    if k == "gita":
        cost, n, cont = R.choice([400, 480, 600, 720]), R.choice([20, 24, 30]), R.choice([40, 60, 120])
        if (cost - cont) % n:
            return None
        r = (cost - cont) // n
        return mcq("Il pullman costa %d €. La scuola paga %d € e il resto si divide tra %d bambini. Quanto paga ogni bambino? (%d − %d)%s%d" % (cost, cont, n, cost, cont, Dv, n), "%d €" % r,
                   ["%d €" % (cost - cont // n) if cont % n == 0 else "%d €" % (cost // n), "%d €" % (cost // n) if cost % n == 0 else "%d €" % (r + 2), "%d €" % (r + 1)],
                   "(%d − %d) = %d; %d %s %d = <b>%d €</b>." % (cost, cont, cost - cont, cost - cont, DIV, n, r))
    if k == "torte":
        t, f, m = R.randint(3, 6), R.choice([8, 10, 12]), R.randint(5, 15)
        r = t * f - m
        return mcq("Per la festa ci sono %d torte da %d fette. Se ne mangiano %d. Quante fette avanzano? (%d%s%d − %d)" % (t, f, m, t, X, f, m), str(r),
                   [str(t * (f - m)) if f > m else str(r + 10), str(t + f - m), str(r + 1)], "%d %s %d = %d; %d − %d = <b>%d</b>." % (t, FOIS, f, t * f, t * f, m, r))
    if k == "sconto":
        pr, n, sc = R.choice([15, 20, 25]), R.randint(2, 4), R.choice([5, 8, 10])
        r = (pr - sc) * n
        return mcq("Una maglietta costa %d €; oggi c’è uno sconto di %d € su ogni maglietta. %s ne compra %d. Quanto spende? (%d − %d)%s%d" % (pr, sc, p[0], n, pr, sc, X, n), "%d €" % r,
                   ["%d €" % (pr - sc * n), "%d €" % (pr * n), "%d €" % (pr * n - sc)], "(%d − %d) = %d; %d %s %d = <b>%d €</b>." % (pr, sc, pr - sc, pr - sc, FOIS, n, r))
    a, b, c = R.randint(3, 8), R.randint(2, 5), R.randint(5, 20)
    r = a * 3 + b * 2 - c
    if r < 0:
        return None
    return mcq("In una partita %s fa %d canestri da 3 punti e %d da 2 punti, ma ha %d punti di penalità. Quanti punti fa? (%d%s3 + %d%s2 − %d)" % (p[0], a, b, c, a, X, b, X, c), str(r),
               [str(a * 3 + b * 2 + c), str((a + b) * 5 - c), str(a + b - c) if a + b > c else str(r + 2)], "%d + %d − %d = <b>%d</b>." % (a * 3, b * 2, c, r))


def main():
    seen = set()
    sets = [
        ("Prima × e :, poi + e −", mix(R, seen, [(s1_semplice, 20)])),
        ("Espressioni senza parentesi", mix(R, seen, [(s2_quattro, 20)])),
        ("Espressioni con le parentesi", mix(R, seen, [(s3_parentesi, 20)])),
        ("Scrivere un’espressione", mix(R, seen, [(s4_scrivi, 14), (s4_distributiva, 6)])),
        ("Problemi con le espressioni", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["In un’espressione l’ordine conta: prima le <b>parentesi</b> (tonde, poi quadre), poi %s e %s, poi + e −." % (FOIS, DIV),
         "Operazioni dello stesso livello (solo + e −, oppure solo %s e %s) si fanno <b>da sinistra a destra</b>." % (FOIS, DIV),
         "Un problema con più domande si può scrivere con una sola espressione: 3 %s 4 + 2 vuol dire «3 quaderni da 4 € e una gomma da 2 €»." % FOIS],
        [("5 + 3 %s 4" % FOIS, ["3 %s 4 = 12" % FOIS, "5 + 12 = 17"], "17"),
         ("(5 + 3) %s 4" % FOIS, ["5 + 3 = 8", "8 %s 4 = 32" % FOIS], "32")],
        [["5 + 3 %s 4 = 32" % FOIS, "La moltiplicazione va prima: 5 + 12 = 17."],
         ["20 − 5 + 3 = 12", "Solo + e −: da sinistra, 15 + 3 = 18."],
         ["Togliere le parentesi senza calcolarle", "Calcola prima ciò che c’è dentro la parentesi."]])
    faq = [("Perché la moltiplicazione si fa prima dell’addizione?", "È una regola comune a tutti: così ogni espressione ha un solo risultato. 3 × 4 + 2 vuol dire «3 gruppi da 4, più 2»."),
           ("A che cosa servono le parentesi?", "A cambiare l’ordine: ciò che è tra parentesi si calcola per primo, (3 + 4) × 2 = 14.")]
    make_unit(R, "espressioni", "N",
              "Eseguire le quattro operazioni rispettando l’ordine di esecuzione, anche con le parentesi; rappresentare problemi con espressioni aritmetiche",
              "Le espressioni: ordine delle operazioni e parentesi", "Espressioni",
              "Schede di matematica per la classe quinta sulle espressioni: ordine delle operazioni, parentesi tonde e quadre, scrivere un’espressione, proprietà distributiva e problemi. 100 esercizi con soluzioni.",
              "Prima le parentesi, poi × e :, poi + e −.", "A parità di livello, da sinistra a destra.",
              body, faq, sets, 10, grade=G)


if __name__ == "__main__":
    main()
