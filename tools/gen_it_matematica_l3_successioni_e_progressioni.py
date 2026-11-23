# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: Successioni e progressioni (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l3_successioni_e_progressioni.py
Successioni per espressione analitica e per ricorrenza, termine generale, progressioni aritmetiche (ragione, n-esimo termine,
somma dei primi n termini), progressioni geometriche (ragione, n-esimo termine, somma), riconoscere il tipo, problemi.
Errori: aₙ = a₁ + nd, ragione geometrica come differenza, Sₙ aritmetica senza dividere per 2.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, d, P2

R = random.Random(72303)
G = "terza-liceo"


def A(i):
    return "a<sub>%s</sub>" % i


def seq(xs):
    return "; ".join(fq(x) for x in xs) + "; …"


def s1_ric():
    a1 = R.randint(-3, 5)
    k = R.choice(["lin", "dop"])
    if k == "lin":
        m, c = R.choice([2, 3, -1, -2]), R.randint(-3, 4)
        f = lambda x: m * x + c
        rule = "%s = %s" % (A("n+1"), P2(0, m, c).replace("x", A("n")))
    else:
        c = R.randint(1, 4)
        f = lambda x: x * x - c
        rule = "%s = (%s)² − %d" % (A("n+1"), A("n"), c)
    xs = [a1]
    for _ in range(3):
        xs.append(f(xs[-1]))
    if abs(xs[3]) > 400:
        return None
    return M("Una successione è definita per ricorrenza: %s = %s e %s. Calcola %s." % (A(1), fq(a1), rule, A(4)), fq(xs[3]), [fq(x) for x in W(xs[2], f(xs[3]) if abs(f(xs[3])) < 1000 else None, xs[3] + 1, -xs[3] if xs[3] else 1, xs[3] - 1, xs[3] + 2, xs[1])],
             "%s = %s, %s = %s, %s = <b>%s</b>." % (A(2), fq(xs[1]), A(3), fq(xs[2]), A(4), fq(xs[3])))


def s1_gen():
    d_, a1 = nz(R, -6, 6), R.randint(-5, 9)
    xs = [a1 + i * d_ for i in range(4)]
    q0 = a1 - d_
    ans = "%s = %s" % (A("n"), P2(0, d_, q0).replace("x", "n"))
    w = ["%s = %s" % (A("n"), P2(0, d_, a1).replace("x", "n")), "%s = %s" % (A("n"), P2(0, a1, d_).replace("x", "n")) if a1 else "%s = %dn" % (A("n"), d_ + 1), "%s = %s" % (A("n"), P2(0, -d_, a1 + d_).replace("x", "n"))]
    return M("Qual è il termine generale della successione %s (con n ≥ 1)?" % seq(xs), ans, [x for x in w if x != ans],
             "La differenza tra due termini consecutivi è %s: %s = %s + (n − 1) · %s = <b>%s</b>." % (fq(d_), A("n"), fq(a1), "(%s)" % fq(d_) if d_ < 0 else fq(d_), P2(0, d_, q0).replace("x", "n")))


def s2_arit():
    a1, d_ = R.randint(-10, 15), nz(R, -5, 6)
    n = R.randint(8, 40)
    an = a1 + (n - 1) * d_
    k = R.choice(["an", "d", "a1"])
    if k == "an":
        return M("In una progressione aritmetica %s = %s e la ragione è d = %s. Calcola %s." % (A(1), fq(a1), fq(d_), A(n)), fq(an), [fq(x) for x in W(a1 + n * d_, a1 + (n - 2) * d_, a1 * n) if x != an] + [fq(-an)],
                 "%s = %s + (n − 1)d = %s + %d · %s = <b>%s</b>." % (A("n"), A(1), fq(a1), n - 1, "(%s)" % fq(d_) if d_ < 0 else fq(d_), fq(an)))
    m = R.randint(2, 6)
    am = a1 + (m - 1) * d_
    if k == "d":
        return M("In una progressione aritmetica %s = %s e %s = %s. Qual è la ragione?" % (A(m), fq(am), A(n), fq(an)), "d = %s" % fq(d_), ["d = %s" % fq(x) for x in W(Fr(an - am, n - m + 1), Fr(an - am, n), Fr(an, am) if am else None, d_ + 1) if x != d_],
                 "%s − %s = (%d − %d)d → %s = %d · d → <b>d = %s</b>." % (A(n), A(m), n, m, fq(an - am), n - m, fq(d_)))
    return M("In una progressione aritmetica di ragione %s si ha %s = %s. Quanto vale %s?" % (fq(d_), A(n), fq(an), A(1)), fq(a1), [fq(x) for x in W(an - n * d_, an + (n - 1) * d_, an - (n - 2) * d_, a1 + 1) if x != a1],
             "%s = %s − (n − 1)d = %s − %d · %s = <b>%s</b>." % (A(1), A(n), fq(an), n - 1, "(%s)" % fq(d_) if d_ < 0 else fq(d_), fq(a1)))


def s2_somma():
    k = R.choice(["gen", "nat", "disp"])
    if k == "gen":
        a1, d_ = R.randint(-5, 10), nz(R, -3, 5)
        n = R.randint(10, 30)
        an = a1 + (n - 1) * d_
        S = Fr(n * (a1 + an), 2)
        return M("Calcola la somma dei primi %d termini della progressione aritmetica con %s = %s e d = %s." % (n, A(1), fq(a1), fq(d_)), d(S), [d(x) for x in W(n * (a1 + an), Fr(n * (a1 + an - d_), 2), Fr((n - 1) * (a1 + an), 2), S + n)],
                     "%s = %s, S<sub>n</sub> = n(%s + %s)/2 = %d · (%s + %s)/2 = <b>%s</b>." % (A(n), fq(an), A(1), A("n"), n, fq(a1), fq(an), d(S)))
    n = R.choice([20, 30, 40, 50, 100, 25, 60])
    if k == "nat":
        S = n * (n + 1) // 2
        return M("Quanto vale la somma dei numeri naturali da 1 a %d?" % n, d(S), [d(x) for x in (n * n, n * (n - 1) // 2, n * (n + 1))],
                 "1 + 2 + … + n = n(n + 1)/2 = %d · %d/2 = <b>%s</b>." % (n, n + 1, d(S)))
    S = n * n
    return M("Quanto vale la somma dei primi %d numeri dispari?" % n, d(S), [d(x) for x in (n * (n + 1) // 2, n * (n + 1), 2 * n * n)],
             "1 + 3 + 5 + … (n termini) = n² = <b>%s</b>." % d(S))


def s3_geom():
    a1 = R.choice([1, 2, 3, 5, -2, 4])
    q = R.choice([2, 3, -2, Fr(1, 2), -3, Fr(1, 3)])
    n = R.randint(4, 7)
    an = a1 * q ** (n - 1)
    if abs(an.numerator if isinstance(an, Fr) else an) > 5000:
        return None
    k = R.choice(["an", "q"])
    if k == "an":
        return M("In una progressione geometrica %s = %s e la ragione è q = %s. Calcola %s." % (A(1), fq(a1), fq(q), A(n)), fq(an), [fq(x) for x in W(a1 * q ** n, a1 + (n - 1) * q, a1 * q * (n - 1), -an if q > 0 else abs(an)) if x != an],
                 "%s = %s · q<sup>n−1</sup> = %s · %s<sup>%d</sup> = <b>%s</b>." % (A("n"), A(1), fq(a1), "(%s)" % fq(q) if (q < 0 or Fr(q).denominator != 1) else fq(q), n - 1, fq(an)))
    xs = [a1 * q ** i for i in range(4)]
    return M("Qual è la ragione della progressione geometrica %s?" % seq(xs), "q = %s" % fq(q), ["q = %s" % fq(x) for x in W(xs[1] - xs[0], Fr(1) / q, -q, q * q) if x != q],
             "q = %s : %s = %s : %s = <b>%s</b>." % (A(2), A(1), fq(xs[1]), "(%s)" % fq(xs[0]) if xs[0] < 0 else fq(xs[0]), fq(q)))


def s3_gsomma():
    a1 = R.choice([1, 2, 3, 5])
    q = R.choice([2, 3, -2])
    n = R.randint(4, 8)
    S = a1 * Fr(q ** n - 1, q - 1)
    if abs(S) > 10000:
        return None
    return M("Calcola la somma dei primi %d termini della progressione geometrica con %s = %d e q = %s." % (n, A(1), a1, fq(q)), d(S), [d(x) for x in W(a1 * Fr(q ** (n + 1) - 1, q - 1), a1 * q ** n, a1 * Fr(q ** n - 1, q), S + a1)],
             "S<sub>n</sub> = %s · (q<sup>n</sup> − 1)/(q − 1) = %d · (%s<sup>%d</sup> − 1)/(%s − 1) = <b>%s</b>." % (A(1), a1, "(%s)" % fq(q) if q < 0 else fq(q), n, fq(q), d(S)))


def s4_tipo():
    k = R.choice(["ar", "ge", "ne"])
    if k == "ar":
        a1, dd = R.randint(-5, 9), nz(R, -5, 5)
        xs = [a1 + i * dd for i in range(4)]
        ans = "aritmetica di ragione %s" % fq(dd)
    elif k == "ge":
        a1, q = R.choice([1, 2, 3, -1, 5]), R.choice([2, 3, -2, -3, 4])
        xs = [a1 * q ** i for i in range(4)]
        ans = "geometrica di ragione %s" % fq(q)
    else:
        xs = R.choice([[1, 4, 9, 16], [1, 2, 4, 7], [2, 3, 5, 8], [1, 3, 7, 15], [0, 1, 3, 6], [1, 8, 27, 64]])
        ans = "né aritmetica né geometrica"
    w = ["aritmetica di ragione %s" % fq(xs[1] - xs[0]), "geometrica di ragione %s" % fq(Fr(xs[1], xs[0]) if xs[0] else 2), "né aritmetica né geometrica"]
    return M("Com’è la successione %s?" % seq(xs), ans, [x for x in w if x != ans] + ["aritmetica e geometrica"],
             "Controllo le differenze (%s) e i rapporti tra termini consecutivi: è <b>%s</b>." % (", ".join(fq(xs[i + 1] - xs[i]) for i in range(3)), ans))


def s5_probl():
    k = R.choice(["teatro", "risp", "batteri", "auto"])
    if k == "teatro":
        a1, dd, n = R.randint(10, 20), R.randint(1, 3), R.randint(12, 25)
        an = a1 + (n - 1) * dd
        S = n * (a1 + an) // 2 if n * (a1 + an) % 2 == 0 else None
        if S is None:
            return None
        q = "Un teatro ha %d file: la prima ha %d posti e ogni fila ha %d posti in più della precedente. Quanti posti ci sono in tutto?" % (n, a1, dd)
        return M(q, d(S), [d(x) for x in (n * an, n * a1, n * (a1 + an))], "Progressione aritmetica: ultima fila %d posti; S = %d · (%d + %d)/2 = <b>%s</b>." % (an, n, a1, an, d(S)))
    if k == "risp":
        a1, dd, n = R.choice([5, 10, 20]), R.choice([2, 5, 10]), R.randint(10, 24)
        an = a1 + (n - 1) * dd
        S = n * (a1 + an) // 2
        q = "Marco risparmia %d € la prima settimana e ogni settimana %d € in più della precedente. Quanto ha risparmiato dopo %d settimane?" % (a1, dd, n)
        return M(q, "%s €" % d(S), ["%s €" % d(x) for x in (n * an, n * a1 + dd, an)], "S = n(a<sub>1</sub> + a<sub>n</sub>)/2 con a<sub>n</sub> = %d: %d · (%d + %d)/2 = <b>%s €</b>." % (an, n, a1, an, d(S)))
    if k == "batteri":
        a1, h = R.choice([100, 200, 500, 50]), R.randint(4, 8)
        v = a1 * 2 ** h
        q = "Una colonia di %d batteri raddoppia ogni ora. Quanti batteri ci sono dopo %d ore?" % (a1, h)
        return M(q, d(v), [d(x) for x in (a1 * 2 * h, a1 * 2 ** (h - 1), a1 + 2 ** h, a1 * 2 ** (h + 1))], "Progressione geometrica di ragione 2: %d · 2<sup>%d</sup> = <b>%s</b>." % (a1, h, d(v)))
    v0, p, n = R.choice([20000, 16000, 25000, 30000]), R.choice([Fr(1, 10), Fr(1, 5), Fr(1, 4)]), R.randint(2, 4)
    v = v0 * (1 - p) ** n
    if v.denominator != 1:
        return None
    q = "Un’auto vale %s € e perde il %d%% del valore ogni anno. Quanto vale dopo %d anni?" % (d(v0), int(p * 100), n)
    return M(q, "%s €" % d(v), ["%s €" % d(x) for x in W(v0 * (1 - p * n), v0 * (1 - p) ** (n - 1), v0 * p ** n)], "Ogni anno il valore si moltiplica per %s: %s · %s<sup>%d</sup> = <b>%s €</b>." % (d(1 - p), d(v0), d(1 - p), n, d(v)))


def main():
    seen = set()
    sets = [
        ("Successioni e termine generale", mix(R, seen, [(s1_ric, 10), (s1_gen, 10)])),
        ("Progressioni aritmetiche", mix(R, seen, [(s2_arit, 20)])),
        ("Somme aritmetiche", mix(R, seen, [(s2_somma, 14), (s4_tipo, 6)])),
        ("Progressioni geometriche", mix(R, seen, [(s3_geom, 12), (s3_gsomma, 8)])),
        ("Problemi con le progressioni", mix(R, seen, [(s5_probl, 14), (s4_tipo, 6)])),
    ]
    body = L(["Una <b>successione</b> è una funzione da ℕ a ℝ: a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>, … Si può dare con il termine generale (a<sub>n</sub> = 2n + 1) o per ricorrenza (a<sub>1</sub> e la regola per passare da a<sub>n</sub> ad a<sub>n+1</sub>).",
              "<b>Progressione aritmetica</b>: differenza costante d. a<sub>n</sub> = a<sub>1</sub> + (n − 1)d, S<sub>n</sub> = n(a<sub>1</sub> + a<sub>n</sub>)/2.",
              "<b>Progressione geometrica</b>: rapporto costante q. a<sub>n</sub> = a<sub>1</sub> · q<sup>n−1</sup>, S<sub>n</sub> = a<sub>1</sub>(q<sup>n</sup> − 1)/(q − 1) con q ≠ 1.",
              "Le progressioni geometriche descrivono la crescita (o la diminuzione) percentuale costante."],
             [("a<sub>1</sub> = 3, d = 4: a<sub>20</sub> e S<sub>20</sub>", ["a<sub>20</sub> = 3 + 19 · 4 = 79", "S<sub>20</sub> = 20 · (3 + 79)/2"], "a<sub>20</sub> = 79, S<sub>20</sub> = 820"),
              ("2; 6; 18; …: a<sub>6</sub>", ["q = 3", "2 · 3<sup>5</sup>"], "486")],
             [["a<sub>n</sub> = a<sub>1</sub> + nd", "Dal primo all’n-esimo termine ci sono n − 1 passi: a<sub>1</sub> + (n − 1)d."],
              ["Ragione geometrica come differenza", "q è il rapporto tra un termine e il precedente."],
              ["S<sub>n</sub> = n(a<sub>1</sub> + a<sub>n</sub>)", "Va divisa per 2 (Gauss: si sommano le coppie dagli estremi)."]])
    faq = [("Come si capisce se una successione è aritmetica o geometrica?", "Si calcolano le differenze tra termini consecutivi: se sono costanti è aritmetica. Se invece sono costanti i rapporti, è geometrica."),
           ("Da dove viene la formula della somma aritmetica?", "Si scrive la somma due volte, una in ordine e una al contrario: ogni coppia ha somma a<sub>1</sub> + a<sub>n</sub>; le coppie sono n, e si divide per 2.")]
    unit(G, R, "successioni-e-progressioni", "F",
         "Successioni numeriche definite per ricorrenza e con il termine generale; progressioni aritmetiche e geometriche",
         "Successioni e progressioni", "Successioni e progressioni",
         "Schede di matematica per la terza liceo su successioni e progressioni: ricorrenza e termine generale, progressioni aritmetiche e geometriche, n-esimo termine, ragione, somma dei primi n termini, problemi. 100 esercizi con soluzioni.",
         "aₙ = a₁ + (n − 1)d e aₙ = a₁ · qⁿ⁻¹", "Aritmetica: differenza costante. Geometrica: rapporto costante.",
         body, faq, sets, 3)


if __name__ == "__main__":
    main()
