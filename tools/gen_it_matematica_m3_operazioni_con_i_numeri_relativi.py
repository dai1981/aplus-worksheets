# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Operazioni con i numeri relativi (Numeri)
  python3 tools/gen_it_matematica_m3_operazioni_con_i_numeri_relativi.py
Addizione e sottrazione (somma algebrica, togliere le parentesi), moltiplicazione e divisione (regola dei segni),
potenze con base negativa ed esponente pari/dispari, espressioni con i numeri relativi, numeri razionali relativi.
Errori: (−3) − (−5) = −8, (−2)⁴ = −16, −2⁴ = 16, applicare la regola dei segni all’addizione.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, fq, sgn, par, Kids

R = random.Random(71302)
G = "terza-media"
K = Kids(R)
SUP = {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}


def t(x):
    return sgn(x) if x else "0"


def nz(lo=-15, hi=15):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1_add():
    a, b = nz(), nz()
    op = R.choice(["+", "−"])
    r = a + b if op == "+" else a - b
    q = "(%s) %s (%s)" % (t(a), op, t(b))
    wrong = [a - b if op == "+" else a + b, -r, (abs(a) + abs(b)) * (1 if a > 0 else -1), r + 1]
    return M("Calcola: %s" % q, t(r), W(*[t(x) for x in wrong if x != r]),
             "%s = %s %s %d = <b>%s</b>." % (q, t(a), "+" if (b > 0) == (op == "+") else "−", abs(b), t(r)))


def s1_somma():
    xs = [nz(-12, 12) for _ in range(R.randint(3, 4))]
    r = sum(xs)
    q = " ".join(["%d" % xs[0] if xs[0] > 0 else "−%d" % -xs[0]] + [("+ %d" % x if x > 0 else "− %d" % -x) for x in xs[1:]])
    pos, neg = sum(x for x in xs if x > 0), sum(x for x in xs if x < 0)
    return M("Calcola la somma algebrica: %s" % q, t(r), W(t(sum(abs(x) for x in xs)), t(-r) if r else "+1", t(r + 2), t(pos)),
             "Positivi: %s; negativi: %s; %s %s = <b>%s</b>." % (t(pos), t(neg), t(pos), ("− %d" % -neg) if neg else "", t(r)))


def s2_molt():
    a, b = nz(-12, 12), nz(-12, 12)
    if abs(a) == 1 or abs(b) == 1:
        return None
    if R.random() < 0.5:
        r = a * b
        q = "(%s) × (%s)" % (t(a), t(b))
        return M("Calcola: %s" % q, t(r), W(t(-r), t(a + b), t(abs(a) + abs(b)) if a + b != abs(a) + abs(b) else t(r + 1)),
                 "Segni %s: risultato %s; %d × %d = %d. <b>%s</b>." % ("uguali" if (a > 0) == (b > 0) else "diversi", "positivo" if r > 0 else "negativo", abs(a), abs(b), abs(r), t(r)))
    p = a * b
    q = "(%s) : (%s)" % (t(p), t(b))
    return M("Calcola: %s" % q, t(a), W(t(-a), t(p - b), t(p * b) if abs(p * b) < 200 else t(a + 1)),
             "Segni %s: risultato %s; %d : %d = %d. <b>%s</b>." % ("uguali" if (p > 0) == (b > 0) else "diversi", "positivo" if a > 0 else "negativo", abs(p), abs(b), abs(a), t(a)))


def s2_tre():
    xs = [nz(-6, 6) for _ in range(3)]
    r = xs[0] * xs[1] * xs[2]
    q = " × ".join("(%s)" % t(x) for x in xs)
    n = sum(1 for x in xs if x < 0)
    return M("Calcola: %s" % q, t(r), W(t(-r), t(sum(xs)), t(r + 1) if r + 1 else "+2"),
             "%d fattor%s negativ%s: il segno è %s. <b>%s</b>." % (n, "e" if n == 1 else "i", "o" if n == 1 else "i", "+" if n % 2 == 0 else "−", t(r)))


def s3_pot():
    b = R.choice([-1, -2, -3, -4, -5, -10, 2, 3])
    e = R.choice([2, 3, 4, 5]) if abs(b) <= 3 else R.choice([2, 3])
    if b == -1:
        e = R.randint(2, 15)
    k = R.choice(["par", "nopar"]) if b < 0 else "par"
    v = b ** e
    es = SUP.get(e, "<sup>%d</sup>" % e)
    if k == "par":
        q = "(%s)%s" % (t(b), es)
        r = v
    else:
        q = "−%d%s" % (abs(b), es)
        r = -(abs(b) ** e)
    return M("Calcola: %s" % q, t(r), W(t(-r), t(b * e), t(abs(b) ** e) if abs(b) ** e != r else t(-(abs(b) ** e)), t(b ** (e - 1)) if e > 2 else t(b * 2), t(-abs(b) * e), t(abs(b) * e), t(r * 10), t(r + 1), t(-r - 1)),
             ("La base è %s; esponente %s: risultato %s. <b>%s</b>." % (t(b), "pari" if e % 2 == 0 else "dispari", "positivo" if r > 0 else "negativo", t(r))) if k == "par" else
             "Senza parentesi l’esponente vale solo per %d: −(%d%s) = <b>%s</b>." % (abs(b), abs(b), es, t(r)))


def s4_espr():
    a, b, c, dd = nz(-9, 9), nz(-9, 9), nz(-5, 5), nz(-5, 5)
    k = R.choice([1, 2, 3, 4])
    if k == 1:
        q = "%s + (%s) × (%s)" % (t(a), t(b), t(c))
        r = a + b * c
        w = [(a + b) * c, a - b * c, a + b + c]
        e = "Prima la moltiplicazione: (%s) × (%s) = %s; poi %s + (%s) = <b>%s</b>." % (t(b), t(c), t(b * c), t(a), t(b * c), t(r))
    elif k == 2:
        q = "(%s − %s) × (%s)" % (t(a), par(b) if b < 0 else str(b), t(c))
        r = (a - b) * c
        w = [(a + b) * c, a - b * c, -(a - b) * c]
        e = "Parentesi: %s = %s; × (%s) = <b>%s</b>." % ("%s − %s" % (t(a), par(b) if b < 0 else str(b)), t(a - b), t(c), t(r))
    elif k == 3:
        q = "(%s)² − (%s) × (%s)" % (t(c), t(a), t(dd))
        r = c * c - a * dd
        w = [-c * c - a * dd, c * c + a * dd, 2 * c - a * dd]
        e = "(%s)² = %d; (%s) × (%s) = %s; %d − (%s) = <b>%s</b>." % (t(c), c * c, t(a), t(dd), t(a * dd), c * c, t(a * dd), t(r))
    else:
        p = b * c
        q = "(%s) : (%s) − (%s)" % (t(p), t(c), t(a))
        r = b - a
        w = [b + a, -b - a, p // c * -1 - a]
        e = "(%s) : (%s) = %s; %s − (%s) = <b>%s</b>." % (t(p), t(c), t(b), t(b), t(a), t(r))
    return M("Calcola: %s" % q, t(r), W(*[t(x) for x in w + [r + 1, r - 2] if x != r]), e)


def s5_raz():
    a = Fr(nz(-9, 9), R.choice([2, 3, 4, 5, 6]))
    b = Fr(nz(-9, 9), R.choice([2, 3, 4, 5, 6]))
    if a.denominator == 1 or b.denominator == 1:
        return None
    op = R.choice(["+", "−", "×", ":"])
    r = {"+": a + b, "−": a - b, "×": a * b, ":": a / b}[op]
    f = lambda x: ("+" if x > 0 else "") + fq(x) if x else "0"
    q = "(%s) %s (%s)" % (f(a), op, f(b))
    w = [-r, {"+": a - b, "−": a + b, "×": a / b, ":": a * b}[op], Fr(a.numerator + b.numerator, a.denominator + b.denominator), Fr(a.numerator * b.numerator, a.denominator + b.denominator), r * 2, r + 1]
    return M("Calcola: %s" % q, f(r), W(*[f(x) for x in w if x is not None and x != r]), "%s = <b>%s</b>." % (q, f(r)))


def s5_quiz():
    q, a, w = R.choice([
        ("Il prodotto di due numeri negativi è…", "positivo", ["negativo", "zero", "dipende dai numeri"]),
        ("Il quoziente tra un numero positivo e uno negativo è…", "negativo", ["positivo", "zero", "dipende dai numeri"]),
        ("Una potenza con base negativa ed esponente pari è…", "positiva", ["negativa", "zero", "dipende dalla base"]),
        ("Una potenza con base negativa ed esponente dispari è…", "negativa", ["positiva", "zero", "uguale alla base"]),
        ("Sottrarre −5 equivale ad…", "aggiungere +5", ["aggiungere −5", "sottrarre +5", "moltiplicare per −5"]),
        ("Il prodotto di 5 fattori negativi è…", "negativo", ["positivo", "zero", "non si può dire"]),
        ("La somma di due numeri opposti è…", "zero", ["il doppio del primo", "negativa", "uno"]),
        ("(−1)¹⁰⁰ vale…", "+1", ["−1", "+100", "−100"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Addizione e sottrazione", mix(R, seen, [(s1_add, 12), (s1_somma, 8)])),
        ("Moltiplicazione e divisione", mix(R, seen, [(s2_molt, 14), (s2_tre, 6)])),
        ("Potenze", mix(R, seen, [(s3_pot, 14), (s5_quiz, 6)])),
        ("Espressioni", mix(R, seen, [(s4_espr, 20)])),
        ("Numeri razionali relativi", mix(R, seen, [(s5_raz, 20)])),
    ]
    body = L(["<b>Addizione</b>: segni uguali → si sommano i valori assoluti e si tiene il segno; segni diversi → si sottraggono e si tiene il segno del valore assoluto maggiore.",
              "<b>Sottrazione</b>: si aggiunge l’opposto: (+3) − (−5) = +3 + 5 = +8.",
              "<b>Moltiplicazione e divisione</b> (regola dei segni): segni uguali → +; segni diversi → −.",
              "<b>Potenze</b>: base negativa con esponente pari → positivo; dispari → negativo. Attenzione: (−2)⁴ = +16 ma −2⁴ = −16."],
             [("(−7) − (−3)", ["−7 + 3"], "−4"), ("(−4) × (+6)", ["segni diversi → −", "4 × 6 = 24"], "−24")],
             [["(−3) − (−5) = −8", "Togli la parentesi cambiando il segno: −3 + 5 = +2."],
              ["(−2)⁴ = −16", "Esponente pari: il risultato è positivo, +16."],
              ["Usare la regola dei segni nell’addizione", "(−3) + (−4) = −7, non +7."]],
             table(["×  :", "+", "−"], [["+", "+", "−"], ["−", "−", "+"]]))
    faq = [("Perché meno per meno fa più?", "Moltiplicare per −1 significa prendere l’opposto; l’opposto dell’opposto torna al segno di partenza."),
           ("Che differenza c’è tra (−3)² e −3²?", "(−3)² = (−3) × (−3) = +9; −3² = −(3 × 3) = −9: senza parentesi il segno non fa parte della base.")]
    unit(G, R, "operazioni-con-i-numeri-relativi", "N",
         "Eseguire addizioni, sottrazioni, moltiplicazioni, divisioni e potenze con i numeri relativi; eseguire semplici espressioni di calcolo con i numeri conosciuti",
         "Operazioni con i numeri relativi", "Operazioni con i relativi",
         "Schede di matematica per la terza media sulle operazioni con i numeri relativi: somma algebrica, regola dei segni, potenze con base negativa, espressioni e numeri razionali relativi. 100 esercizi con soluzioni.",
         "Segni uguali: +. Segni diversi: −.", "(−2)⁴ = +16, ma −2⁴ = −16.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
