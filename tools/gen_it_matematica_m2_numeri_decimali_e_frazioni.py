# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Numeri decimali e frazioni (Numeri)
  python3 tools/gen_it_matematica_m2_numeri_decimali_e_frazioni.py
Dalla frazione al numero decimale: decimali limitati e periodici (semplici e misti); quando una frazione dà un decimale
limitato (denominatore con solo 2 e 5); frazione generatrice; confronto e approssimazione; numeri razionali.
Errori: 0,3 periodico = 3/10, dimenticare l’antiperiodo, pensare che 7/20 dia un periodico.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, fq, d, dk, FOIS, DIV

R = random.Random(71201)
G = "seconda-media"


def ov(s):
    return "<span class='ov'>%s</span>" % s


def dec_str(x):
    """Fraction → stringa con periodo sopralineato"""
    x = Fr(x)
    ip, r = divmod(x.numerator, x.denominator)
    den = x.denominator
    digits, seen = [], {}
    while r and r not in seen:
        seen[r] = len(digits)
        r *= 10
        digits.append(str(r // den))
        r %= den
    if not r:
        return d(x)
    st = seen[r]
    return "%d,%s%s" % (ip, "".join(digits[:st]), ov("".join(digits[st:])))


def tipo(x):
    t = Fr(x).denominator
    for p in (2, 5):
        while t % p == 0:
            t //= p
    if t == 1:
        return "decimale limitato"
    return "periodico semplice" if Fr(x).denominator % 2 and Fr(x).denominator % 5 else "periodico misto"


def rfrac():
    while True:
        b = R.choice([3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 18, 20, 22, 25, 30, 33, 40])
        a = R.randint(1, 3 * b)
        if gcd(a, b) == 1 and a % b:
            return Fr(a, b)


def s1_div():
    x = rfrac()
    s = dec_str(x)
    wrong = [d(Fr(x.numerator, 10)) if x.numerator < 1000 else None, d(Fr(x.denominator, 10 ** len(str(x.denominator)))) , "%s" % dk(x, 2)]
    return M("Trasforma in numero decimale: %s" % fq(x), s, W(*wrong, dec_str(x + Fr(1, 10))),
             "Dividi il numeratore per il denominatore: %d : %d = <b>%s</b>." % (x.numerator, x.denominator, s))


def s1_tipo():
    x = rfrac()
    t = tipo(x)
    why = {"decimale limitato": "il denominatore (ridotto) ha solo i fattori 2 e 5", "periodico semplice": "il denominatore non ha né 2 né 5",
           "periodico misto": "il denominatore ha i fattori 2 o 5 e anche altri fattori"}[t]
    return M("Senza fare la divisione: %s dà un numero…" % fq(x), t, W(*[y for y in ("decimale limitato", "periodico semplice", "periodico misto", "intero") if y != t]),
             "%s = %s: %s, quindi è un <b>%s</b>." % (fq(x), dec_str(x), why, t))


def s2_gen():
    k = R.choice(["lim", "sempl", "misto"])
    if k == "lim":
        n = R.randint(11, 999)
        p = R.choice([1, 2, 3])
        if n % 10 == 0:
            return None
        x = Fr(n, 10 ** p)
        return M("Qual è la frazione generatrice di %s?" % d(x), fq(x), W(fq(Fr(n, 10 ** (p + 1))), fq(Fr(n, 9)) if Fr(n, 9).denominator != 1 else None, fq(Fr(n, 10 ** max(p - 1, 0) or 1)) if p > 1 else fq(Fr(n, 100))),
                 "%s = %d/%d, ridotta ai minimi termini: <b>%s</b>." % (d(x), n, 10 ** p, fq(x)))
    if k == "sempl":
        ip, per = R.randint(0, 9), R.randint(1, 98)
        ps = str(per) if per > 9 else str(per)
        L_ = len(ps)
        num_ = int(str(ip) + ps) - ip
        den = int("9" * L_)
        x = Fr(num_, den)
        if x.denominator == 1:
            return None
        s = "%d,%s" % (ip, ov(ps))
        return M("Qual è la frazione generatrice di %s?" % s, fq(x), W(fq(Fr(int(str(ip) + ps), 10 ** L_)), fq(Fr(int(str(ip) + ps), den)) if Fr(int(str(ip) + ps), den) != x else None, fq(Fr(num_, den * 10))),
                 "Numeratore: %s − %d = %d; denominatore: tanti 9 quante le cifre del periodo (%s). %d/%d = <b>%s</b>." % (str(ip) + ps, ip, num_, "9" * L_, num_, den, fq(x)))
    ip, ant, per = R.randint(0, 5), R.randint(1, 9), R.randint(1, 9)
    if per == ant:
        return None
    num_ = int("%d%d%d" % (ip, ant, per)) - int("%d%d" % (ip, ant))
    x = Fr(num_, 90)
    s = "%d,%d%s" % (ip, ant, ov(per))
    return M("Qual è la frazione generatrice di %s?" % s, fq(x), W(fq(Fr(int("%d%d%d" % (ip, ant, per)) - ip, 99)), fq(Fr(int("%d%d%d" % (ip, ant, per)), 100)), fq(Fr(num_, 99)) if Fr(num_, 99) != x else None),
             "Numeratore: %d%d%d − %d%d = %d; denominatore: un 9 per la cifra del periodo e uno 0 per l’antiperiodo (90). <b>%s</b>." % (ip, ant, per, ip, ant, num_, fq(x)))


def s3_confronta():
    a = rfrac()
    b = Fr(int(a * 100) + R.choice([-3, -1, 1, 3, 10, -10]), 100)
    if b <= 0 or tipo(a) == "decimale limitato":
        return None
    if a == b:
        return None
    g = a if a > b else b
    return M("Qual è il numero maggiore: %s o %s?" % (dec_str(a), d(b)), dec_str(g) if g == a else d(b), W(dec_str(a) if g != a else d(b), "sono uguali", "non si può dire"),
             "%s ≈ %s e %s: il maggiore è <b>%s</b>." % (dec_str(a), dk(a, 3), d(b), dec_str(g) if g == a else d(b)))


def s3_appross():
    x = rfrac()
    k = R.choice([1, 2])
    v = dk(x, k)
    tr = Fr(int(x * 10 ** k), 10 ** k)
    return M("Approssima %s al %s." % (dec_str(x), "decimo" if k == 1 else "centesimo"), v, W(d(tr) if dk(tr, k) != v else dk(x + Fr(1, 10 ** k), k), dk(x, k + 1), dk(x, k - 1) if k > 1 else dk(x, 0)),
             "Guarda la cifra successiva: %s → <b>%s</b>." % (dk(x, k + 2), v))


def s4_quiz():
    q, a, w = R.choice([("0,<span class='ov'>9</span> è uguale a…", "1", ["0,9", "0,99", "9/10"]),
                        ("Un numero razionale è…", "un numero che si può scrivere come frazione", ["solo un numero intero", "un numero con infinite cifre non periodiche", "un numero negativo"]),
                        ("Le cifre che si ripetono in un numero periodico si chiamano…", "periodo", ["antiperiodo", "parte intera", "resto"]),
                        ("In 2,1<span class='ov'>6</span> la cifra 1 è…", "l’antiperiodo", ["il periodo", "la parte intera", "il resto"]),
                        ("Una frazione con denominatore 7 (ridotta) dà sempre…", "un numero periodico semplice", ["un decimale limitato", "un periodico misto", "un intero"]),
                        ("Una frazione con denominatore 40 (ridotta) dà…", "un decimale limitato", ["un periodico semplice", "un periodico misto", "un intero"]),
                        ("Quale tra questi NON è un numero razionale?", "√2", ["0,<span class='ov'>3</span>", "−5", "3/7"])])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Dalla frazione al decimale", mix(R, seen, [(s1_div, 20)])),
        ("Limitato o periodico?", mix(R, seen, [(s1_tipo, 14), (s4_quiz, 6)])),
        ("La frazione generatrice", mix(R, seen, [(s2_gen, 20)])),
        ("Confrontare e approssimare", mix(R, seen, [(s3_confronta, 10), (s3_appross, 10)])),
        ("Frazione generatrice e confronti", mix(R, seen, [(s2_gen, 10), (s3_confronta, 5), (s1_tipo, 5)])),
    ]
    body = L(["Ogni frazione, dividendo il numeratore per il denominatore, dà un numero <b>decimale limitato</b> (3/8 = 0,375) o <b>periodico</b> (2/3 = 0,<span class='ov'>6</span>).",
              "Frazione ridotta ai minimi termini: se il denominatore ha solo i fattori 2 e 5 il decimale è limitato; se non ha né 2 né 5 è <b>periodico semplice</b>; se ha 2 o 5 e altri fattori è <b>periodico misto</b>.",
              "<b>Frazione generatrice</b>: limitato → il numero senza virgola su 10, 100, 1000… Periodico → numero senza virgola meno la parte prima del periodo, fratto tanti 9 quante le cifre del periodo seguiti da tanti 0 quante le cifre dell’antiperiodo.",
              "Tutti questi numeri (frazioni, decimali limitati e periodici) sono <b>numeri razionali</b>."],
             [("1,2<span class='ov'>3</span>", ["numeratore: 123 − 12 = 111", "denominatore: 90"], "111/90 = 37/30")],
             [["0,<span class='ov'>3</span> = 3/10", "Il periodo vuole il 9: 0,<span class='ov'>3</span> = 3/9 = 1/3."],
              ["Dimenticare l’antiperiodo", "Per ogni cifra dell’antiperiodo si aggiunge uno 0 al denominatore."],
              ["Non ridurre prima di guardare il denominatore", "6/15 = 2/5: è limitato, anche se 15 ha il fattore 3."]],
             table(["Denominatore (ridotto)", "Numero decimale", "Esempio"], [["solo 2 e 5", "limitato", "7/20 = 0,35"], ["né 2 né 5", "periodico semplice", "5/11 = 0,<span class='ov'>45</span>"], ["2 o 5 e altri", "periodico misto", "1/6 = 0,1<span class='ov'>6</span>"]]))
    faq = [("Perché 0,9 periodico è uguale a 1?", "Con la regola della frazione generatrice 0,9 periodico = 9/9 = 1: è lo stesso numero scritto in due modi."),
           ("Tutti i numeri decimali sono razionali?", "No: quelli con infinite cifre non periodiche, come √2 o π, sono irrazionali.")]
    unit(G, R, "numeri-decimali-e-frazioni", "N",
         "Utilizzare frazioni equivalenti e numeri decimali per denotare uno stesso numero razionale in diversi modi; riconoscere decimali limitati e periodici e trovare la frazione generatrice",
         "Numeri decimali limitati e periodici, frazione generatrice", "Decimali e frazione generatrice",
         "Schede di matematica per la seconda media sui numeri decimali: dalla frazione al decimale, decimali limitati, periodici semplici e misti, frazione generatrice, confronto e approssimazione. 100 esercizi con soluzioni.",
         "Denominatore con solo 2 e 5: decimale limitato.", "Periodico: tanti 9 quante le cifre del periodo.",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
