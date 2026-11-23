# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Radicali (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l2_radicali.py
Numeri irrazionali, semplificazione, trasporto fuori e dentro il segno di radice, radicali simili e somma algebrica,
prodotto e quoziente, radici cubiche, prodotti notevoli con i radicali, razionalizzazione del denominatore, confronto.
Errori: √(a + b) = √a + √b, sommare radicali non simili, razionalizzare moltiplicando solo il denominatore.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, FR, simp_root

R = random.Random(72204)
G = "seconda-liceo"


def rad(k, m, idx=2):
    """k·ⁿ√m semplificato già"""
    sym = {2: "√", 3: "∛", 4: "∜"}[idx]
    if m == 1:
        return fq(k)
    return ("" if k == 1 else ("−" if k == -1 else fq(k))) + sym + str(m)


def sroot(n, idx=2):
    k, m = 1, n
    for p in range(2, 50):
        while m % (p ** idx) == 0:
            m //= p ** idx
            k *= p
    return k, m


SQF = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]


def s1_fuori():
    m = R.choice(SQF)
    k = R.randint(2, 7)
    n = k * k * m
    w = [rad(k * k, m), rad(k, m * 2) if m * 2 not in (4, 9) else rad(k * 2, m), rad(k + 1, m), rad(2 * k, m)]
    return M("Porta fuori dal segno di radice: √%d" % n, rad(k, m), [x for x in w if x != rad(k, m)],
             "%d = %d · %d = %d² · %d, quindi √%d = <b>%s</b>." % (n, k * k, m, k, m, n, rad(k, m)))


def s1_dentro():
    k, m = R.randint(2, 6), R.choice(SQF)
    ans = "√%d" % (k * k * m)
    return M("Porta dentro il segno di radice: %s" % rad(k, m), ans, ["√%d" % (k * m), "√%d" % (k + m), "√%d" % (k * m * m), "√%d" % (k * k + m)],
             "Il fattore %d entra elevato al quadrato: √(%d² · %d) = <b>%s</b>." % (k, k, m, ans))


def s1_cubo():
    m = R.choice([2, 3, 4, 5, 6, 7])
    k = R.randint(2, 4)
    n = k ** 3 * m
    ans = rad(k, m, 3)
    return M("Semplifica: ∛%d" % n, ans, [rad(m, k, 3) if k != m else rad(k + 1, m, 3), rad(k * k, m, 3) if k * k * m != n else rad(k, m * 2, 3), "%s√%d" % (k, m)],
             "%d = %d³ · %d, quindi ∛%d = <b>%s</b>." % (n, k, m, n, ans))


def s2_somma():
    m = R.choice([2, 3, 5, 6, 7])
    cs = [R.choice([1, 2, 3, 4, 5]) for _ in range(3)]
    sq = [R.choice([1, 2, 3, 4]) for _ in range(3)]
    sg = [1, R.choice([1, -1]), R.choice([1, -1])]
    terms = []
    tot = 0
    for c, q, s in zip(cs, sq, sg):
        terms.append((s, c, q * q * m))
        tot += s * c * q
    if tot == 0:
        return None
    q_ = ""
    for i, (s, c, n) in enumerate(terms):
        q_ += ("" if i == 0 else (" + " if s > 0 else " − ")) + ("" if c == 1 else str(c)) + "√%d" % n
    wrong = sum(s * c for s, c, _ in terms)
    w = [rad(wrong, m) if wrong else "0", rad(tot, m * 2) if m * 2 not in (4, 8) else rad(tot + 1, m), rad(-tot, m), rad(tot + (1 if tot > 0 else -1), m)]
    return M("Calcola: %s" % q_, rad(tot, m), [x for x in w if x != rad(tot, m)],
             "Porto fuori: %s. Sono radicali simili (radicando %d): sommo i coefficienti, <b>%s</b>." % (" ".join(("" if i == 0 else ("+" if s > 0 else "−")) + " " + rad(c * int(math.isqrt(n // m)), m) for i, (s, c, n) in enumerate(terms)).strip(), m, rad(tot, m)))


def s2_prod():
    a, b = R.sample([2, 3, 5, 6, 7, 10, 12, 14, 15, 21, 18], 2)
    k, m = sroot(a * b)
    ans = rad(k, m)
    op = R.choice(["·", ":"])
    if op == ":":
        n = a * b
        q = "√%d : √%d" % (n * a, n) if False else "√%d : √%d" % (a * b * b, b)
        k2, m2 = sroot(a * b)
        ans = rad(k2, m2)
        return M("Calcola: %s" % q, ans, [rad(*sroot(a * b * b + b)) if False else "√%d" % (a * b * b - b), "√%d" % (a * b * b * b) if a * b ** 3 < 500 else "√%d" % (a + b), rad(b, a)],
                 "Stesso indice: √(%d : %d) = √%d = <b>%s</b>." % (a * b * b, b, a * b, ans))
    return M("Calcola: √%d · √%d" % (a, b), ans, ["√%d" % (a + b), rad(k + 1, m) if m > 1 else str(k + 1), "√%d" % (a * b) if m != a * b else rad(2 * k, m)],
             "Stesso indice: √(%d · %d) = √%d = <b>%s</b>." % (a, b, a * b, ans))


def s3_notev():
    a, b = R.sample([2, 3, 5, 6, 7], 2)
    k = R.choice(["q", "spd", "q2"])
    if k == "q":
        p = a * b
        kk, mm = sroot(p)
        ans = "%d + %s" % (a + b, rad(2 * kk, mm))
        w = ["%d" % (a + b), "%d + %s" % (a + b, rad(kk, mm)), "%d + %s" % (a * b, rad(2 * kk, mm))]
        return M("Calcola: (√%d + √%d)²" % (a, b), ans, w, "(A + B)² = A² + 2AB + B²: %d + 2√%d + %d = <b>%s</b>." % (a, a * b, b, ans))
    if k == "spd":
        v = a - b
        return M("Calcola: (√%d + √%d)(√%d − √%d)" % (a, b, a, b), fq(v), [fq(-v), fq(a + b), "√%d" % abs(a - b) if abs(a - b) not in (1, 4) else fq(v * v + 1), fq(a * b)],
                 "Somma per differenza: (√%d)² − (√%d)² = %d − %d = <b>%s</b>." % (a, b, a, b, fq(v)))
    c = R.randint(1, 5)
    ans = "%d − %s" % (c * c + a, rad(2 * c, a))
    return M("Calcola: (%d − √%d)²" % (c, a), ans, [fq(c * c - a) if c * c != a else fq(c * c + a), "%d − %s" % (c * c + a, rad(c, a)), "%d + %s" % (c * c + a, rad(2 * c, a))],
             "%d² − 2 · %d · √%d + %d = <b>%s</b>." % (c, c, a, a, ans))


def s4_raz():
    k = R.choice(["mono", "bino"])
    if k == "mono":
        m = R.choice(SQF)
        n = m * R.randint(1, 4)
        f = Fr(n, m)
        ans = rad(f, m) if f.denominator == 1 else FR(rad(f.numerator, m), f.denominator)
        w = [FR(str(n), str(m)), FR("√%d" % m, str(n)), rad(n, m), FR(rad(n, m), str(m * m))]
        return M("Razionalizza il denominatore: %s" % FR(str(n), "√%d" % m), ans, [x for x in w if x != ans],
                 "Moltiplico numeratore e denominatore per √%d: %s = <b>%s</b>." % (m, FR(rad(n, m), str(m)), ans))
    a = R.choice([2, 3, 5, 6, 7, 10])
    b = R.randint(1, 3)
    if b * b == a:
        return None
    den = a - b * b
    num = R.choice([x for x in range(1, 13) if x % den == 0] or [den])
    s = R.choice([1, -1])
    f = Fr(num, den)
    # num/(√a − s·b) · (√a + s·b) = num(√a + s b)/(a − b²)
    if f.denominator == 1:
        c = f.numerator
        ans = ("" if c == 1 else fq(c) if c > 0 else ("−" if c == -1 else fq(c))) + ("(√%d %s %d)" % (a, "+" if s > 0 else "−", b) if c != 1 else "√%d %s %d" % (a, "+" if s > 0 else "−", b))
    else:
        ans = FR("%d(√%d %s %d)" % (num, a, "+" if s > 0 else "−", b), fq(den))
    w = ["√%d %s %d" % (a, "−" if s > 0 else "+", b), FR(str(num), str(a - b)) if a != b else "%d" % num, FR("%d(√%d %s %d)" % (num, a, "+" if s > 0 else "−", b), str(a + b * b))]
    return M("Razionalizza: %s" % FR(str(num), "√%d %s %d" % (a, "−" if s > 0 else "+", b)), ans, [x for x in w if x != ans],
             "Moltiplico per il binomio coniugato (√%d %s %d): al denominatore %d − %d = %d, quindi <b>%s</b>." % (a, "+" if s > 0 else "−", b, a, b * b, den, ans))


def s5_conf():
    a, m1 = R.randint(2, 6), R.choice([2, 3, 5, 6, 7])
    b, m2 = R.randint(2, 6), R.choice([2, 3, 5, 6, 7])
    v1, v2 = a * a * m1, b * b * m2
    if v1 == v2 or m1 == m2:
        return None
    big = rad(a, m1) if v1 > v2 else rad(b, m2)
    return M("Qual è il maggiore tra %s e %s?" % (rad(a, m1), rad(b, m2)), big, [rad(b, m2) if v1 > v2 else rad(a, m1), "sono uguali", "dipende dall’approssimazione"],
             "Porto dentro: %s = √%d e %s = √%d. Il maggiore è <b>%s</b>." % (rad(a, m1), v1, rad(b, m2), v2, big))


def s5_irr():
    items = [("√2", "irrazionale"), ("√49", "razionale"), ("π", "irrazionale"), ("0,<span class='ov'>3</span>", "razionale"), ("√3 · √12", "razionale"),
             ("√5 + 1", "irrazionale"), ("∛27", "razionale"), ("√8 : √2", "razionale"), ("√6", "irrazionale"), ("2√3", "irrazionale"), ("1,4142", "razionale"), ("√0,25", "razionale")]
    x, t = R.choice(items)
    return M("Il numero %s è razionale o irrazionale?" % x, t, ["irrazionale" if t == "razionale" else "razionale", "né razionale né irrazionale", "dipende dalla calcolatrice"],
             "Un numero è razionale se si può scrivere come frazione (decimale finito o periodico): %s è <b>%s</b>." % (x, t))


def main():
    seen = set()
    sets = [
        ("Trasporto fuori e dentro", mix(R, seen, [(s1_fuori, 10), (s1_dentro, 5), (s1_cubo, 5)])),
        ("Somma algebrica di radicali", mix(R, seen, [(s2_somma, 14), (s5_irr, 6)])),
        ("Prodotto e quoziente", mix(R, seen, [(s2_prod, 12), (s5_conf, 8)])),
        ("Prodotti notevoli", mix(R, seen, [(s3_notev, 20)])),
        ("Razionalizzazione", mix(R, seen, [(s4_raz, 20)])),
    ]
    body = L(["I radicali come √2 sono numeri <b>irrazionali</b>: decimali illimitati non periodici. Con a, b ≥ 0: √a · √b = √(ab) e √a : √b = √(a : b).",
              "Per <b>portare fuori</b> si scompone il radicando e si estraggono i quadrati: √72 = √(36 · 2) = 6√2. Per <b>portare dentro</b> il fattore si eleva al quadrato: 3√2 = √18.",
              "Si sommano solo radicali <b>simili</b> (stesso indice e stesso radicando): 3√2 + 5√2 = 8√2. A volte diventano simili dopo aver portato fuori.",
              "<b>Razionalizzare</b> vuol dire togliere la radice dal denominatore: a/√b si moltiplica per √b; a/(√b − c) per il coniugato (√b + c)."],
             [("√12 + √27", ["2√3 + 3√3"], "5√3"),
              ("4/(√5 − 1)", ["· (√5 + 1)/(√5 + 1)", "4(√5 + 1)/(5 − 1)"], "√5 + 1")],
             [["√(9 + 16) = 3 + 4", "√25 = 5: la radice di una somma non è la somma delle radici."],
              ["√2 + √3 = √5", "Non sono simili: la somma resta √2 + √3."],
              ["6/√3 = 6√3/3 = 6", "6√3/3 = 2√3: si semplifica il 6 con il 3, il radicale resta."]])
    faq = [("Perché si razionalizza il denominatore?", "Per avere frazioni più facili da confrontare e da calcolare: 1/√2 e √2/2 sono lo stesso numero, ma la seconda forma si somma meglio con gli altri radicali."),
           ("Quando due radicali sono simili?", "Quando hanno lo stesso indice e lo stesso radicando, dopo averli semplificati e aver portato fuori i fattori: 2√3 e −5√3 sono simili, √3 e √6 no.")]
    unit(G, R, "radicali", "A",
         "I numeri reali; calcolo con i radicali: semplificazione, operazioni, razionalizzazione",
         "Radicali", "Radicali",
         "Schede di matematica per la seconda liceo sui radicali: numeri irrazionali, trasporto fuori e dentro il segno di radice, somma di radicali simili, prodotto e quoziente, prodotti notevoli, razionalizzazione. 100 esercizi con soluzioni.",
         "√a · √b = √(ab)", "Si sommano solo radicali simili; per razionalizzare si moltiplica per il coniugato.",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
