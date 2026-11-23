# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Formule goniometriche (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l4_formule_goniometriche.py
Formule di addizione e sottrazione (seno, coseno, tangente), valori di 15° e 75°, formule di duplicazione,
formule di bisezione (con il segno), riconoscere e semplificare espressioni, tg(α + β) con valori dati.
Errori: sen(α + β) = sen α + sen β, cos(α − β) con il segno meno, sen 2α = 2 sen α, segno nella bisezione.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, FR, simp_root

R = random.Random(72405)
G = "quarta-liceo"
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 35, 37), (9, 40, 41)]

SPEC = [("sen 75°", FR("√6 + √2", 4), "sen(45° + 30°) = sen 45° cos 30° + cos 45° sen 30°"),
        ("cos 75°", FR("√6 − √2", 4), "cos(45° + 30°) = cos 45° cos 30° − sen 45° sen 30°"),
        ("sen 15°", FR("√6 − √2", 4), "sen(45° − 30°) = sen 45° cos 30° − cos 45° sen 30°"),
        ("cos 15°", FR("√6 + √2", 4), "cos(45° − 30°) = cos 45° cos 30° + sen 45° sen 30°"),
        ("tg 75°", "2 + √3", "tg(45° + 30°) = (1 + √3/3)/(1 − √3/3)"),
        ("tg 15°", "2 − √3", "tg(45° − 30°) = (1 − √3/3)/(1 + √3/3)"),
        ("sen 105°", FR("√6 + √2", 4), "sen(60° + 45°) = sen 60° cos 45° + cos 60° sen 45°"),
        ("cos 105°", FR("√2 − √6", 4), "cos(60° + 45°) = cos 60° cos 45° − sen 60° sen 45°")]
SPEC_POOL = [FR("√6 + √2", 4), FR("√6 − √2", 4), FR("√2 − √6", 4), "2 + √3", "2 − √3", FR("√3 + 1", 2), FR("√2", 2)]


def s1_spec():
    f, a, e = R.choice(SPEC)
    w = [x for x in SPEC_POOL if x != a]
    R.shuffle(w)
    return M("Calcola %s con le formule di addizione o sottrazione." % f, a, w[:3], "%s = <b>%s</b>." % (e, a))


def tri_val():
    a, b, c = R.choice(TRIPLES)
    if R.random() < 0.5:
        a, b = b, a
    return Fr(a, c), Fr(b, c)


def s1_add():
    sa, ca = tri_val()
    sb, cb = tri_val()
    k = R.choice(["sen+", "sen-", "cos+", "cos-"])
    if k == "sen+":
        v, wr = sa * cb + ca * sb, [sa + sb, sa * cb - ca * sb, ca * cb - sa * sb]
        f = "sen(α + β)"
    elif k == "sen-":
        v, wr = sa * cb - ca * sb, [sa - sb, sa * cb + ca * sb, ca * cb + sa * sb]
        f = "sen(α − β)"
    elif k == "cos+":
        v, wr = ca * cb - sa * sb, [ca + cb, ca * cb + sa * sb, sa * cb + ca * sb]
        f = "cos(α + β)"
    else:
        v, wr = ca * cb + sa * sb, [ca - cb, ca * cb - sa * sb, sa * cb - ca * sb]
        f = "cos(α − β)"
    form = {"sen+": "sen α cos β + cos α sen β", "sen-": "sen α cos β − cos α sen β", "cos+": "cos α cos β − sen α sen β", "cos-": "cos α cos β + sen α sen β"}[k]
    return M("α e β sono angoli acuti con sen α = %s e sen β = %s. Calcola %s." % (fq(sa), fq(sb), f), fq(v), [fq(x) for x in W(*wr) if x != v] + [fq(-v)],
             "cos α = %s, cos β = %s (angoli acuti). %s = %s = <b>%s</b>." % (fq(ca), fq(cb), f, form, fq(v)))


def s2_dup():
    a, b, c = R.choice(TRIPLES)
    if R.random() < 0.5:
        a, b = b, a
    q = R.choice([1, 2])
    s = Fr(a, c)
    co = Fr(b, c) * (1 if q == 1 else -1)
    k = R.choice(["s2", "c2", "t2"])
    qn = "primo" if q == 1 else "secondo"
    if k == "s2":
        v = 2 * s * co
        return M("Sapendo che sen α = %s e che α è nel %s quadrante, calcola sen 2α." % (fq(s), qn), fq(v), [fq(x) for x in W(2 * s, -v, s * co, 1 - 2 * s * s) if x != v],
                 "cos α = %s. sen 2α = 2 sen α cos α = <b>%s</b>." % (fq(co), fq(v)))
    if k == "c2":
        v = 1 - 2 * s * s
        return M("Sapendo che sen α = %s, calcola cos 2α." % fq(s), fq(v), [fq(x) for x in W(2 * s * s - 1, 1 - s * s, 2 * Fr(b, c), Fr(b, c) ** 2) if x != v],
                 "cos 2α = 1 − 2 sen²α = 1 − 2 · %s = <b>%s</b> (non serve il quadrante)." % (fq(s * s), fq(v)))
    t = s / co
    v = 2 * t / (1 - t * t)
    return M("Sapendo che tg α = %s, calcola tg 2α." % fq(t), fq(v), [fq(x) for x in W(2 * t, 2 * t / (1 + t * t), -v, t * t) if x != v],
             "tg 2α = 2 tg α / (1 − tg²α) = %s / %s = <b>%s</b>." % (fq(2 * t), fq(1 - t * t), fq(v)))


def s3_bis():
    c_ = R.choice([Fr(1, 2), Fr(-1, 2), Fr(7, 25), Fr(-7, 25), Fr(1, 9), Fr(-1, 9), Fr(119, 169), Fr(17, 25), Fr(-17, 25), Fr(7, 9)])
    k = R.choice(["cos", "sen"])
    v2 = (1 + c_) / 2 if k == "cos" else (1 - c_) / 2
    import math
    num, den = v2.numerator, v2.denominator
    rn, rd = math.isqrt(num), math.isqrt(den)
    if rd * rd != den:
        return None
    kk, mm = simp_root(num)
    root = fq(Fr(rn, rd)) if rn * rn == num else (FR("%s√%d" % ("" if kk == 1 else kk, mm), str(rd)) if Fr(kk, rd).denominator != 1 else "%s√%d" % ("" if kk // rd == 1 else kk // rd, mm))
    w = [(fq(Fr(rn * rn, rd * rd)) if False else fq(v2)), "−" + root, FR("√%d" % (den - num) if math.isqrt(den - num) ** 2 != den - num else str(math.isqrt(den - num)), str(rd)) if den != num else "0", fq(c_ / 2)]
    return M("Sapendo che cos α = %s con 0 &lt; α &lt; π, calcola %s(α/2)." % (fq(c_), k), root, [x for x in W(*w) if x != root],
             "%s(α/2) = √[(1 %s cos α)/2] = √(%s); α/2 è nel primo quadrante, quindi il segno è +: <b>%s</b>." % (k, "+" if k == "cos" else "−", "%d/%d" % (v2.numerator, v2.denominator) if v2.denominator != 1 else str(v2), root))


IDS = [("2 sen α cos α", "sen 2α"), ("cos²α − sen²α", "cos 2α"), ("1 − 2 sen²α", "cos 2α"), ("2 cos²α − 1", "cos 2α"),
       ("sen α cos β + cos α sen β", "sen(α + β)"), ("cos α cos β + sen α sen β", "cos(α − β)"), ("sen 2α / (2 cos α)", "sen α"),
       ("(1 − cos 2α)/2", "sen²α"), ("(1 + cos 2α)/2", "cos²α"), ("sen 2α / (1 + cos 2α)", "tg α"), ("(sen α + cos α)² − 1", "sen 2α"),
       ("cos⁴α − sen⁴α", "cos 2α")]
POOL = ["sen 2α", "cos 2α", "sen(α + β)", "cos(α − β)", "sen α", "sen²α", "cos²α", "tg α", "1", "2 sen α", "tg 2α"]


def s4_id():
    e, a = R.choice(IDS)
    w = [x for x in POOL if x != a]
    R.shuffle(w)
    return M("Semplifica: %s" % e, a, w[:3], "Con le formule di addizione, duplicazione o bisezione: %s = <b>%s</b>." % (e, a))


def s5_tg():
    ta = Fr(R.choice([1, 2, 3, Fr(1, 2), Fr(1, 3), Fr(3, 4)]))
    tb = Fr(R.choice([1, 2, 3, Fr(1, 2), Fr(1, 3), Fr(1, 4)]))
    k = R.choice(["+", "−"])
    den = 1 - ta * tb if k == "+" else 1 + ta * tb
    if den == 0 or ta == tb:
        return None
    v = (ta + tb) / den if k == "+" else (ta - tb) / den
    return M("Sapendo che tg α = %s e tg β = %s, calcola tg(α %s β)." % (fq(ta), fq(tb), k), fq(v), [fq(x) for x in W(ta + tb if k == "+" else ta - tb, (ta + tb) / (1 + ta * tb) if k == "+" else (ta - tb) / (1 - ta * tb) if ta * tb != 1 else None, -v, ta * tb) if x != v],
             "tg(α %s β) = (tg α %s tg β)/(1 %s tg α tg β) = (%s) : (%s) = <b>%s</b>." % (k, "+" if k == "+" else "−", "−" if k == "+" else "+", fq(ta + tb if k == "+" else ta - tb), fq(den), fq(v)))


def main():
    seen = set()
    sets = [
        ("Formule di addizione e sottrazione", mix(R, seen, [(s1_spec, 8), (s1_add, 12)])),
        ("Tangente di una somma", mix(R, seen, [(s5_tg, 14), (s1_add, 6)])),
        ("Formule di duplicazione", mix(R, seen, [(s2_dup, 20)])),
        ("Formule di bisezione", mix(R, seen, [(s3_bis, 14), (s2_dup, 6)])),
        ("Identità e semplificazioni", mix(R, seen, [(s4_id, 12), (s3_bis, 4), (s5_tg, 4)])),
    ]
    body = L(["<b>Addizione</b>: sen(α ± β) = sen α cos β ± cos α sen β; cos(α ± β) = cos α cos β ∓ sen α sen β (segno opposto!); tg(α ± β) = (tg α ± tg β)/(1 ∓ tg α tg β).",
              "<b>Duplicazione</b>: sen 2α = 2 sen α cos α; cos 2α = cos²α − sen²α = 1 − 2 sen²α = 2 cos²α − 1; tg 2α = 2 tg α/(1 − tg²α).",
              "<b>Bisezione</b>: sen(α/2) = ±√[(1 − cos α)/2], cos(α/2) = ±√[(1 + cos α)/2]: il segno dipende dal quadrante di α/2.",
              "Con queste formule si calcolano valori come sen 15° e cos 75° e si semplificano le espressioni."],
             [("cos 15°", ["cos(45° − 30°) = √2/2 · √3/2 + √2/2 · 1/2"], "(√6 + √2)/4"),
              ("sen α = 3/5, α acuto: sen 2α", ["cos α = 4/5", "2 · 3/5 · 4/5"], "24/25")],
             [["sen(α + β) = sen α + sen β", "Si usa la formula: sen α cos β + cos α sen β."],
              ["cos(α + β) con il segno +", "Nel coseno della somma c’è il meno: cos α cos β − sen α sen β."],
              ["sen 2α = 2 sen α", "sen 2α = 2 sen α cos α."]])
    faq = [("Da quali formule si ricavano tutte le altre?", "Dalla formula del coseno della differenza, dimostrata con la distanza tra due punti sulla circonferenza goniometrica. Le altre si ottengono con gli archi associati e ponendo β = α."),
           ("Come si sceglie il segno nelle formule di bisezione?", "Si guarda in quale quadrante si trova l’angolo α/2: per esempio se 0 &lt; α &lt; π allora α/2 è nel primo quadrante e seno e coseno sono positivi.")]
    unit(G, R, "formule-goniometriche", "F",
         "Formule di addizione, sottrazione, duplicazione e bisezione; identità goniometriche",
         "Formule goniometriche", "Formule goniometriche",
         "Schede di matematica per la quarta liceo sulle formule goniometriche: addizione e sottrazione, valori di 15° e 75°, tangente della somma, duplicazione, bisezione e identità. 100 esercizi con soluzioni.",
         "sen 2α = 2 sen α cos α", "cos(α + β) = cos α cos β − sen α sen β: attenzione al segno.",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
