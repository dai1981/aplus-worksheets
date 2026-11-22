# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Calcolo letterale e monomi (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m3_calcolo_letterale_monomi.py
Espressioni letterali e valore numerico, monomi: coefficiente, parte letterale, grado, monomi simili e opposti,
somma algebrica di monomi simili, prodotto, quoziente e potenza di monomi.
Errori: 3a + 2b = 5ab, 2a · 3a = 6a (dimenticare di sommare gli esponenti), (2a)² = 2a², sommare anche gli esponenti nella somma.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, fq, sgn, Kids
from it_m3 import mono, lett, P, show, mul, add, evalp, deg, key

R = random.Random(71303)
G = "terza-media"
K = Kids(R)
VARS = ["a", "b", "x", "y"]


def nz(lo=-9, hi=9):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def rex(maxe=3, nv=None):
    vs = R.sample(VARS[:2] if R.random() < 0.5 else VARS[2:], nv or R.randint(1, 2))
    return {v: R.randint(1, maxe) for v in vs}


def s1_parti():
    c, ex = nz(), rex()
    m = mono(c, ex)
    k = R.choice(["coef", "lett", "grado", "grado_v"])
    if k == "coef":
        return M("Qual è il coefficiente del monomio %s?" % m, sgn(c), W(sgn(-c), lett(ex), str(deg(key(ex)))), "Il coefficiente è il numero davanti alle lettere, con il segno: <b>%s</b>." % sgn(c))
    if k == "lett":
        return M("Qual è la parte letterale del monomio %s?" % m, lett(ex), W(m, lett({v: e + 1 for v, e in ex.items()}), "".join(sorted(ex))), "La parte letterale è formata dalle lettere con i loro esponenti: <b>%s</b>." % lett(ex))
    g = deg(key(ex))
    if k == "grado" or len(ex) == 1:
        return M("Qual è il grado del monomio %s?" % m, str(g), W(str(g + 1), str(len(ex)), str(max(ex.values())) if max(ex.values()) != g else str(g - 1), str(abs(c)) if abs(c) != g else str(g + 2), str(g - 1) if g > 1 else "0", str(g * 2)),
                 "Il grado è la somma degli esponenti delle lettere: <b>%d</b>." % g)
    v = R.choice(sorted(ex))
    return M("Qual è il grado del monomio %s rispetto alla lettera %s?" % (m, v), str(ex[v]), W(str(g) if g != ex[v] else None, str(ex[v] + 1), "1" if ex[v] != 1 else "0", "0" if ex[v] != 1 else "2", str(abs(c)) if abs(c) != ex[v] else None), "Si guarda solo l’esponente di %s: <b>%d</b>." % (v, ex[v]))


def s1_simili():
    ex = rex()
    c1, c2 = nz(), nz()
    k = R.choice(["sim", "nosim", "opp"])
    if k == "sim":
        q = "%s e %s" % (mono(c1, ex), mono(c2, ex))
        return M("I monomi %s sono…" % q, "simili", ["non simili", "opposti", "uguali"] if c2 != -c1 else ["non simili", "uguali", "di grado diverso"], "Hanno la stessa parte letterale %s: sono <b>simili</b>." % lett(ex)) if c1 != -c2 else None
    if k == "opp":
        q = "%s e %s" % (mono(c1, ex), mono(-c1, ex))
        return M("I monomi %s sono…" % q, "opposti", ["uguali", "non simili", "di grado diverso"], "Stessa parte letterale e coefficienti opposti: <b>opposti</b>.")
    ex2 = dict(ex)
    v = R.choice(sorted(ex2))
    ex2[v] += 1
    q = "%s e %s" % (mono(c1, ex), mono(c2, ex2))
    return M("I monomi %s sono…" % q, "non simili", ["simili", "opposti", "uguali"], "Le parti letterali %s e %s sono diverse: <b>non simili</b>." % (lett(ex), lett(ex2)))


def s2_somma():
    ex = rex()
    cs = [nz() for _ in range(R.randint(2, 3))]
    r = sum(cs)
    if r == 0:
        return None
    q = "".join(mono(c, ex, i == 0) for i, c in enumerate(cs))
    ex2 = {v: e * 2 for v, e in ex.items()}
    return M("Calcola: %s" % q, mono(r, ex), W(mono(r, ex2), mono(-r, ex), mono(sum(abs(c) for c in cs), ex) if sum(abs(c) for c in cs) != r else mono(r + 1, ex), fq(r)),
             "Monomi simili: si sommano i coefficienti (%s) e la parte letterale resta %s: <b>%s</b>." % (" ".join(sgn(c) for c in cs), lett(ex), mono(r, ex)))


def sh2(c1, c2, v1, v2):
    t = [(c1, v1), (c2, v2)]
    t = [(c, v) for c, v in t if c]
    return "".join(mono(c, {v: 1}, i == 0) for i, (c, v) in enumerate(t)) or "0"


def s2_misti():
    v1, v2 = R.sample(["a", "b", "x", "y"], 2)
    a, b, c, dd = nz(), nz(), nz(), nz()
    q = mono(a, {v1: 1}) + mono(b, {v2: 1}, False) + mono(c, {v1: 1}, False) + mono(dd, {v2: 1}, False)
    p = P([(a, {v1: 1}), (b, {v2: 1}), (c, {v1: 1}), (dd, {v2: 1})])
    if len(p) < 2:
        return None
    ans = "".join(mono(p[k_], dict(k_), i == 0) for i, k_ in enumerate(sorted(p, key=lambda k_: k_[0][0] != v1)))
    return M("Riduci i termini simili: %s" % q, ans, W(mono(a + b + c + dd, {v1: 1, v2: 1}) if a + b + c + dd else None, sh2(a - c, b - dd, v1, v2), sh2(a + c, -(b + dd), v1, v2)),
             "%s con %s, %s con %s: <b>%s</b>." % (v1, v1, v2, v2, ans))


def s3_prod():
    k = R.choice(["prod", "prod", "quoz", "pot"])
    if k == "prod":
        e1, e2 = rex(3), rex(3)
        c1, c2 = nz(-6, 6), nz(-6, 6)
        ex = dict(e1)
        for v, e in e2.items():
            ex[v] = ex.get(v, 0) + e
        exw = dict(e1)
        for v, e in e2.items():
            exw[v] = exw.get(v, 0) * e if v in exw else e
        r = mono(c1 * c2, ex)
        return M("Calcola: (%s) · (%s)" % (mono(c1, e1), mono(c2, e2)), r, W(mono(c1 * c2, exw) if exw != ex else None, mono(-c1 * c2, ex), mono(c1 + c2, ex) if c1 + c2 else None, mono(c1 * c2, {v: 1 for v in ex}), mono(c1 * c2, {v: 2 * e for v, e in ex.items()})),
                 "Coefficienti: (%s) · (%s) = %s; esponenti della stessa lettera si sommano: <b>%s</b>." % (sgn(c1), sgn(c2), sgn(c1 * c2), r))
    if k == "quoz":
        e2 = rex(2)
        e1 = {v: e + R.randint(0, 3) for v, e in e2.items()}
        c2 = nz(-6, 6)
        c1 = c2 * nz(-5, 5)
        ex = {v: e1[v] - e2[v] for v in e1}
        r = mono(Fr(c1, c2), ex)
        return M("Calcola: (%s) : (%s)" % (mono(c1, e1), mono(c2, e2)), r, W(mono(Fr(-c1, c2), ex), mono(Fr(c1, c2), {v: e1[v] + e2[v] for v in e1}), mono(c1 - c2, ex) if c1 != c2 else None, mono(Fr(c1, c2), {v: max(1, e1[v] // e2[v]) for v in e1}) if any(e1[v] // e2[v] != e1[v] - e2[v] for v in e1) else None),
                 "Coefficienti: %s : %s = %s; esponenti si sottraggono: <b>%s</b>." % (sgn(c1), sgn(c2), sgn(Fr(c1, c2)), r))
    e1 = rex(3)
    c = nz(-4, 4)
    n = R.choice([2, 3])
    ex = {v: e * n for v, e in e1.items()}
    r = mono(c ** n, ex)
    return M("Calcola: (%s)%s" % (mono(c, e1), "²" if n == 2 else "³"), r, W(mono(c, ex) if abs(c) != 1 else None, mono(c * n, ex), mono(c ** n, {v: e + n for v, e in e1.items()}), mono(-(c ** n), ex), mono(c ** n, e1)),
             "Si eleva il coefficiente (%s)%s = %s e si moltiplicano gli esponenti per %d: <b>%s</b>." % (sgn(c), "²" if n == 2 else "³", sgn(c ** n), n, r))


def s4_valore():
    k = R.choice(["mono", "espr"])
    a, b = nz(-5, 5), nz(-5, 5)
    if k == "mono":
        c = nz(-6, 6)
        e1, e2 = R.randint(1, 3), R.randint(0, 2)
        ex = {"a": e1, "b": e2}
        v = evalp(P([(c, ex)]), {"a": a, "b": b})
        return M("Calcola il valore del monomio %s per a = %s e b = %s." % (mono(c, ex), sgn(a), sgn(b)), sgn(v) if v else "0", W(sgn(-v) if v else "1", sgn(c * a * e1 * (b if e2 else 1)) if c * a * e1 * (b if e2 else 1) != v else None, sgn(c + a + b), sgn(v + c)),
                     "Sostituisci: %s · (%s)%s%s = <b>%s</b>." % (sgn(c), sgn(a), "²³"[e1 - 2] if e1 > 1 else "", (" · (%s)%s" % (sgn(b), "²" if e2 == 2 else "")) if e2 else "", sgn(v) if v else "0"))
    p = P([(nz(-4, 4), {"x": 2}), (nz(-6, 6), {"x": 1}), (nz(-9, 9), {})])
    x = nz(-4, 4)
    v = evalp(p, {"x": x})
    alt = sum(c * (2 * x if dict(k_).get("x") == 2 else x if dict(k_).get("x") == 1 else 1) for k_, c in p.items())
    alt2 = sum(c * (-(x * x) if dict(k_).get("x") == 2 and x < 0 else x ** dict(k_).get("x", 0)) for k_, c in p.items())
    return M("Calcola il valore di %s per x = %s." % (show(p), sgn(x)), sgn(v) if v else "0", W(sgn(alt) if alt != v and alt else None, sgn(alt2) if alt2 != v and alt2 else None, sgn(-v) if v else "1", sgn(v + 2), sgn(v - 2) if v != 2 else "+1", sgn(v * 2) if v else "+2"),
             "Sostituisci x = %s (tra parentesi): risultato <b>%s</b>." % (sgn(x), sgn(v) if v else "0"))


def main():
    seen = set()
    sets = [
        ("Coefficiente, parte letterale e grado", mix(R, seen, [(s1_parti, 20)])),
        ("Monomi simili e opposti", mix(R, seen, [(s1_simili, 8), (s2_somma, 12)])),
        ("Somma algebrica di monomi", mix(R, seen, [(s2_somma, 10), (s2_misti, 10)])),
        ("Prodotto, quoziente e potenza", mix(R, seen, [(s3_prod, 20)])),
        ("Valore numerico", mix(R, seen, [(s4_valore, 20)])),
    ]
    body = L(["Un <b>monomio</b> è un prodotto di un numero (il <b>coefficiente</b>) e di lettere (la <b>parte letterale</b>): in −3a²b il coefficiente è −3 e la parte letterale è a²b.",
              "Il <b>grado</b> è la somma degli esponenti delle lettere: −3a²b ha grado 3.",
              "Si possono sommare solo i monomi <b>simili</b> (stessa parte letterale): si sommano i coefficienti. 5x² − 2x² = 3x².",
              "Nel <b>prodotto</b> si moltiplicano i coefficienti e si <b>sommano gli esponenti</b> della stessa lettera; nel <b>quoziente</b> si sottraggono; nella <b>potenza</b> si moltiplicano."],
             [("(2a²b) · (−3ab³)", ["2 · (−3) = −6", "a²⁺¹ b¹⁺³"], "−6a³b⁴"), ("(−2x³)²", ["(−2)² = 4", "esponente 3 × 2 = 6"], "4x⁶")],
             [["3a + 2b = 5ab", "a e b non sono simili: 3a + 2b resta così."],
              ["2a · 3a = 6a", "Gli esponenti si sommano: 6a²."],
              ["(2a)² = 2a²", "Si eleva anche il coefficiente: 4a²."]],
             table(["Operazione", "Coefficienti", "Esponenti"], [["somma (simili)", "si sommano", "restano uguali"], ["prodotto", "si moltiplicano", "si sommano"], ["quoziente", "si dividono", "si sottraggono"], ["potenza", "si elevano", "si moltiplicano"]]))
    faq = [("Un numero da solo è un monomio?", "Sì: per esempio 7 è un monomio di grado 0 (non ha lettere)."),
           ("Perché nel valore numerico si mettono le parentesi?", "Per non sbagliare i segni: con x = −3, x² = (−3)² = 9, mentre −3² sarebbe −9.")]
    unit(G, R, "calcolo-letterale-monomi", "F",
         "Interpretare, costruire e trasformare formule che contengono lettere per esprimere in forma generale relazioni e proprietà; operare con i monomi",
         "Calcolo letterale e monomi", "Monomi",
         "Schede di matematica per la terza media sul calcolo letterale: monomi, coefficiente, parte letterale, grado, monomi simili, somma, prodotto, quoziente, potenza e valore numerico. 100 esercizi con soluzioni.",
         "Somma: solo monomi simili.", "Prodotto: esponenti si sommano.",
         body, faq, sets, 3)


if __name__ == "__main__":
    main()
