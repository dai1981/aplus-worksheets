# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Disequazioni lineari (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l1_disequazioni_lineari.py
Principi di equivalenza (cambio del verso moltiplicando per un numero negativo), disequazioni intere e con le frazioni,
soluzioni intere, sistemi di disequazioni, segno di un prodotto di fattori di primo grado, problemi.
Errori: non cambiare il verso dividendo per un negativo, sbagliare l’intersezione nei sistemi, includere gli estremi.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show, d

R = random.Random(72108)
G = "prima-liceo"
OPS = ["&lt;", "&gt;", "≤", "≥"]
FLIP = {"&lt;": "&gt;", "&gt;": "&lt;", "≤": "≥", "≥": "≤"}
STRICT = {"&lt;": "≤", "&gt;": "≥", "≤": "&lt;", "≥": "&gt;"}


def lin(a, b, v="x"):
    return show(P([(a, {v: 1}), (b, {})]))


def ds(op, k):
    return "x %s %s" % (op, fq(k))


def s1_base():
    a = nz(R, -9, 9)
    if abs(a) == 1:
        return None
    b = R.randint(-15, 15)
    k = Fr(R.randint(-8, 8)) if R.random() < 0.7 else Fr(nz(R, -9, 9), abs(a))
    c = a * k + b
    if c.denominator != 1:
        return None
    op = R.choice(OPS)
    res = op if a > 0 else FLIP[op]
    ans = ds(res, k)
    w = [ds(FLIP[res], k), ds(res, -k) if k else ds(STRICT[res], k), ds(STRICT[res], k), ds(res, (c + b) / a) if (c + b) / a != k else ds(res, k + 1)]
    return M("Risolvi: %s %s %s" % (lin(a, b), op, fq(c)), ans, W(*w),
             "%s = %s, poi divido per %s%s: <b>%s</b>." % (show(P([(a, {"x": 1})])), fq(c - b), fq(a), " e <b>cambio il verso</b> perché è negativo" if a < 0 else "", ans))


def s1_due():
    a, c = nz(R, -7, 7), nz(R, -7, 7)
    if a == c:
        return None
    k = Fr(R.randint(-6, 6))
    b = R.randint(-12, 12)
    dd = (a - c) * k + b
    op = R.choice(OPS)
    co = a - c
    res = op if co > 0 else FLIP[op]
    ans = ds(res, k)
    w = [ds(FLIP[res], k), ds(STRICT[res], k), ds(res, -k) if k else ds(res, 1), ds(op, Fr(dd + b, co)) if Fr(dd + b, co) != k else None]
    return M("Risolvi: %s %s %s" % (lin(a, b), op, lin(c, dd)), ans, W(*w),
             "Porto le x a sinistra: %s %s %s → <b>%s</b>.%s" % (show(P([(co, {"x": 1})])), op, fq(dd - b), ans, " Ho diviso per un numero negativo, quindi il verso è cambiato." if co < 0 else ""))


def s2_fraz():
    d1, d2 = R.choice([(2, 3), (3, 4), (2, 5), (4, 6), (3, 6), (2, 4), (5, 2)])
    a = nz(R, -4, 4)
    k = Fr(R.randint(-6, 8))
    # (x + a)/d1 − x/d2  op  rhs
    co = Fr(1, d1) - Fr(1, d2)
    if co == 0:
        return None
    rhs = (k + a) / d1 - k / d2
    if rhs.denominator not in (1, 2, 3, 4, 6, 12, 5, 10):
        return None
    op = R.choice(OPS)
    res = op if co > 0 else FLIP[op]
    ans = ds(res, k)
    q = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span> − <span class='fr'><span class='fn'>x</span><span class='fd'>%d</span></span> %s %s" % (lin(1, a), d1, d2, op, fq(rhs) if rhs >= 0 else "−" + fq(-rhs))
    m = d1 * d2 // math.gcd(d1, d2)
    return M("Risolvi: %s" % q, ans, W(ds(FLIP[res], k), ds(STRICT[res], k), ds(res, -k) if k else ds(res, 2), ds(res, k * m) if k * m != k else ds(res, k - 1)),
             "Moltiplico per il m.c.m. %d (positivo, il verso non cambia), poi risolvo: %s<b>%s</b>." % (m, "il coefficiente di x è negativo, quindi il verso cambia: " if co < 0 else "", ans))


def s2_intere():
    a = R.randint(2, 7)
    b = R.randint(-10, 10)
    k = Fr(nz(R, -20, 20), a)
    if k.denominator == 1:
        return None
    c = a * k + b
    op = R.choice(["&lt;", "≤"])
    if R.random() < 0.5:
        lo = math.floor(k) + 1 if True else None
        q = "Qual è il più piccolo numero intero che verifica %s %s %s?" % (lin(-a, -b), op, fq(-c)) if False else "Qual è il più grande numero intero che verifica %s %s %s?" % (lin(a, b), op, fq(c))
        ans = math.floor(k)
        w = [ans + 1, ans - 1, math.ceil(k) + 1]
        e = "x %s %s: il più grande intero è <b>%s</b>." % (op, fq(k), fq(ans))
    else:
        q = "Qual è il più piccolo numero intero che verifica %s %s %s?" % (lin(a, b), "&gt;" if op == "&lt;" else "≥", fq(c))
        ans = math.ceil(k)
        w = [ans - 1, ans + 1, math.floor(k) - 1]
        e = "x %s %s: il più piccolo intero è <b>%s</b>." % ("&gt;" if op == "&lt;" else "≥", fq(k), fq(ans))
    return M(q, fq(ans), [fq(x) for x in w], e)


def s3_sist():
    p, q = sorted(R.sample(range(-8, 9), 2))
    k = R.choice(["int", "int", "vuoto", "uno"])
    a1, a2 = nz(R, -4, 4), nz(R, -4, 4)
    if k == "int":
        r1, r2 = ("&gt;", "&lt;")
        lo_op, hi_op = R.choice(["&gt;", "≥"]), R.choice(["&lt;", "≤"])
        ans = "%s %s x %s %s" % (fq(p), "&lt;" if lo_op == "&gt;" else "≤", "&lt;" if hi_op == "&lt;" else "≤", fq(q))
        w = ["x %s %s" % (lo_op, fq(p)), "x %s %s ∨ x %s %s" % (hi_op, fq(p), lo_op, fq(q)), "impossibile", "%s ≤ x ≤ %s" % (fq(p), fq(q)) if not (lo_op == "≥" and hi_op == "≤") else "%s &lt; x &lt; %s" % (fq(p), fq(q))]
        s1, s2 = (p, lo_op), (q, hi_op)
    elif k == "vuoto":
        lo_op, hi_op = "&gt;", "&lt;"
        s1, s2 = (q, R.choice(["&gt;", "≥"])), (p, R.choice(["&lt;", "≤"]))
        ans = "impossibile (nessuna soluzione)"
        w = ["%s &lt; x &lt; %s" % (fq(p), fq(q)), "x &lt; %s ∨ x &gt; %s" % (fq(p), fq(q)), "x &gt; %s" % fq(q)]
    else:
        s1, s2 = (p, R.choice(["&gt;", "≥"])), (q, R.choice(["&gt;", "≥"]))
        ans = "x %s %s" % (s2[1], fq(q))
        w = ["x %s %s" % (s1[1], fq(p)), "%s &lt; x &lt; %s" % (fq(p), fq(q)), "x %s %s" % (FLIP[s2[1]], fq(q))]
    rows = []
    for (val, op), a in ((s1, a1), (s2, a2)):
        b = R.randint(-6, 6)
        c = a * val + b
        o = op if a > 0 else FLIP[op]
        rows.append("%s %s %s" % (lin(a, b), o, fq(c)))
    q_ = "Risolvi il sistema: <span class='sys'>%s<br>%s</span>" % tuple(rows)
    return M(q_, ans, [x for x in w if x != ans],
             "Risolvo ciascuna disequazione (x %s %s e x %s %s) e prendo le soluzioni comuni (intersezione): <b>%s</b>." % (s1[1], fq(s1[0]), s2[1], fq(s2[0]), ans))


def s4_segno():
    a, b = sorted(R.sample(range(-7, 8), 2))
    op = R.choice(["&gt;", "&lt;", "≥", "≤"])
    q = "(%s)(%s) %s 0" % (lin(1, -a), lin(1, -b), op)
    if op in ("&gt;", "≥"):
        o1, o2 = ("&lt;", "&gt;") if op == "&gt;" else ("≤", "≥")
        ans = "x %s %s ∨ x %s %s" % (o1, fq(a), o2, fq(b))
        w = ["%s %s x %s %s" % (fq(a), o1, o1, fq(b)), "x %s %s" % (o2, fq(b)), "x %s %s ∨ x %s %s" % (o1, fq(-b), o2, fq(-a))]
        e = "Il prodotto è positivo dove i fattori hanno lo stesso segno, cioè fuori dalle radici %s e %s: <b>%s</b>." % (fq(a), fq(b), ans)
    else:
        o = "&lt;" if op == "&lt;" else "≤"
        ans = "%s %s x %s %s" % (fq(a), o, o, fq(b))
        w = ["x %s %s ∨ x %s %s" % (o, fq(a), FLIP[o], fq(b)), "x %s %s" % (o, fq(a)), "%s %s x %s %s" % (fq(-b), o, o, fq(-a))]
        e = "Il prodotto è negativo dove i fattori hanno segno opposto, cioè tra le radici %s e %s: <b>%s</b>." % (fq(a), fq(b), ans)
    return M("Risolvi con lo studio del segno: %s" % q, ans, [x for x in w if x != ans], e)


def s5_probl():
    k = R.choice(["bigl", "voto", "tariffa", "rett"])
    if k == "bigl":
        p = R.choice([6, 7, 8, 9, 12, 15])
        f = R.choice([5, 10, 12, 20])
        bud = R.randint(60, 200)
        n = (bud - f) // p
        q = "Per una gita si pagano %d € di prenotazione più %d € a biglietto. Con %d € al massimo, quanti biglietti si possono comprare al massimo?" % (f, p, bud)
        e = "%d + %dx ≤ %d → x ≤ %s: al massimo <b>%d</b> biglietti." % (f, p, bud, fq(Fr(bud - f, p)), n)
        return M(q, str(n), W(n + 1, bud // p, n - 1, (bud + f) // p), e)
    if k == "voto":
        vs = [R.randint(4, 8) for _ in range(3)]
        t = R.choice([6, 7])
        need = 4 * t - sum(vs)
        if not 1 <= need <= 10:
            return None
        q = "Luca ha preso %d, %d e %d in tre verifiche. Quale voto minimo deve prendere nella quarta per avere una media almeno di %d?" % (vs[0], vs[1], vs[2], t)
        e = "(%d + x)/4 ≥ %d → x ≥ %d − %d = <b>%d</b>." % (sum(vs), t, 4 * t, sum(vs), need)
        return M(q, str(need), W(need - 1, need + 1, t, 3 * t - sum(vs) if 3 * t - sum(vs) > 0 else None, need + 2), e)
    if k == "tariffa":
        a, pa = R.choice([(10, 1), (15, 0.5), (20, 0.25)])
        b, pb = R.choice([(0, 2), (5, 1.5)])
        if pa >= pb:
            return None
        x0 = Fr(a - b) / Fr(pb - pa).limit_denominator(100)
        n = math.floor(x0) + 1
        q = "La palestra A costa %d € al mese più %s € a ingresso; la palestra B %s%s € a ingresso. Da quanti ingressi al mese in su conviene A?" % (a, str(pa).replace(".", ","), ("%d € al mese più " % b) if b else "", str(pb).replace(".", ","))
        e = "%d + %sx &lt; %s%sx → x &gt; %s: conviene da <b>%d</b> ingressi in su." % (a, str(pa).replace(".", ","), ("%d + " % b) if b else "", str(pb).replace(".", ","), fq(x0), n)
        return M(q, str(n), W(n - 1, n + 1, math.floor(x0) if math.floor(x0) != n - 1 else n + 2), e)
    b = R.randint(4, 12)
    per = R.randint(30, 60)
    hmax = Fr(per, 2) - b
    if hmax <= 0:
        return None
    q = "Un rettangolo ha la base di %d cm. Quanto può misurare al massimo l’altezza se il perimetro non deve superare %d cm?" % (b, per)
    e = "2(%d + h) ≤ %d → h ≤ %s cm: al massimo <b>%s cm</b>." % (b, per, d(hmax), d(hmax))
    return M(q, "%s cm" % d(hmax), ["%s cm" % d(x) for x in (Fr(per, 2) + b, per - b, Fr(per - b, 2))], e)


def main():
    seen = set()
    sets = [
        ("Disequazioni intere", mix(R, seen, [(s1_base, 20)])),
        ("Incognita nei due membri", mix(R, seen, [(s1_due, 14), (s2_intere, 6)])),
        ("Con le frazioni e soluzioni intere", mix(R, seen, [(s2_fraz, 12), (s2_intere, 8)])),
        ("Sistemi e studio del segno", mix(R, seen, [(s3_sist, 12), (s4_segno, 8)])),
        ("Problemi con le disequazioni", mix(R, seen, [(s5_probl, 20)])),
    ]
    body = L(["Una disequazione si risolve come un’equazione, con una regola in più: se si moltiplicano o dividono i due membri per un <b>numero negativo</b>, il verso <b>cambia</b> (&lt; diventa &gt;).",
              "Le soluzioni sono di solito infinite: x &gt; 3 vuol dire tutti i numeri maggiori di 3 (3 escluso); x ≥ 3 comprende anche 3.",
              "In un <b>sistema</b> di disequazioni si risolve ogni disequazione e si prendono le soluzioni <b>comuni</b> (intersezione). Se non ce ne sono, il sistema è impossibile.",
              "Per un prodotto (x − a)(x − b) si studia il segno di ogni fattore: il prodotto è positivo fuori dalle radici e negativo tra le radici."],
             [("−3x + 5 &gt; 11", ["−3x &gt; 6", "Divido per −3 e cambio il verso."], "x &lt; −2"),
              ("Sistema x − 1 &gt; 0 e 2x ≤ 8", ["x &gt; 1 e x ≤ 4"], "1 &lt; x ≤ 4")],
             [["−2x &lt; 6 → x &lt; −3", "Dividendo per −2 il verso cambia: x &gt; −3."],
              ["Prendere l’unione nel sistema", "Nel sistema valgono tutte le condizioni insieme: intersezione."],
              ["Confondere &lt; e ≤", "Con ≤ l’estremo è compreso, con &lt; no."]])
    faq = [("Perché il verso cambia con un numero negativo?", "Perché moltiplicare per un negativo scambia l’ordine: 2 &lt; 5, ma −2 &gt; −5. Per questo, dividendo per −3, x &lt; … diventa x &gt; …"),
           ("Come si rappresentano le soluzioni?", "Sulla retta dei numeri: un pallino pieno se l’estremo è compreso (≤, ≥), vuoto se è escluso (&lt;, &gt;), e una linea dalla parte delle soluzioni.")]
    unit(G, R, "disequazioni-lineari", "A",
         "Disequazioni di primo grado e sistemi di disequazioni; studio del segno di un prodotto",
         "Disequazioni lineari", "Disequazioni lineari",
         "Schede di matematica per la prima liceo sulle disequazioni lineari: principi di equivalenza e cambio del verso, disequazioni intere e con le frazioni, sistemi di disequazioni, studio del segno, problemi. 100 esercizi con soluzioni.",
         "Per un negativo il verso cambia.", "Nei sistemi si prendono le soluzioni comuni a tutte le disequazioni.",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
