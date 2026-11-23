# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Equazioni e disequazioni esponenziali e logaritmiche (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l4_equazioni_esponenziali_e_logaritmiche.py
Equazioni esponenziali riconducibili alla stessa base, con l’incognita ausiliaria t = aˣ, risolte con i logaritmi;
disequazioni esponenziali (verso secondo la base); equazioni logaritmiche (condizioni di esistenza, proprietà);
disequazioni logaritmiche; problemi con la crescita.
Errori: dimenticare le C.E. nelle logaritmiche, non cambiare verso con base minore di 1, accettare t < 0 per t = aˣ.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, nz, P2, sol

R = random.Random(72403)
G = "quarta-liceo"


def pw(b, e):
    return "%s<sup>%s</sup>" % (b, e)


def s1_base():
    b = R.choice([2, 3, 5])
    a, c = R.choice([1, 2, 3]), R.randint(-3, 3)
    x = Fr(R.randint(-3, 4))
    n = a * x + c
    if n.denominator != 1 or not -4 <= n <= 6:
        return None
    val = Fr(b) ** n
    rhs = fq(val) if val.denominator == 1 else fq(val)
    expo = P2(0, a, c)
    w = [Fr(n), Fr(n - c, 1) if n - c != x else x + 1, (n + c) / a, -x, x + 1, x - 1]
    return M("Risolvi: %s = %s" % (pw(b, expo), rhs), "x = %s" % fq(x), ["x = %s" % fq(t) for t in W(*w) if t != x],
             "%s = %s<sup>%s</sup>: uguaglio gli esponenti, %s = %s → <b>x = %s</b>." % (rhs, b, fq(n), expo, fq(n), fq(x)))


def s1_aus():
    b = R.choice([2, 3])
    r1 = R.randint(1, 3)
    t1 = b ** r1
    t2 = R.choice([-1, -2, -3, -t1 - 1])
    # t² − (t1 + t2)t + t1 t2 = 0, t = bˣ
    s_, p = t1 + t2, t1 * t2
    q = "%s %s %s %s = 0" % (pw(b * b, "x"), "−" if s_ > 0 else "+", ("" if abs(s_) == 1 else str(abs(s_))) + pw(b, "x"), ("− %d" % -p) if p < 0 else "+ %d" % p)
    return M("Risolvi: %s" % q, "x = %d" % r1, ["x = %s ∨ x = %d" % (fq(t2), r1), "x = %d" % t1, "impossibile"],
             "Pongo t = %s (t &gt; 0): t² %s %st %s = 0 → t = %d ∨ t = %s. t = %s è da scartare; %s = %d → <b>x = %d</b>." % (pw(b, "x"), "−" if s_ > 0 else "+", "" if abs(s_) == 1 else str(abs(s_)), ("− %d" % -p) if p < 0 else "+ %d" % p, t1, fq(t2), fq(t2), pw(b, "x"), t1, r1))


def s2_log():
    b, c = R.sample([2, 3, 5, 7, 10], 2)
    k = R.choice(["s", "e"])
    if k == "s":
        return M("Risolvi: %s = %d" % (pw(b, "x"), c), "x = log<sub>%d</sub> %d" % (b, c) if b != 10 else "x = log %d" % c, ["x = log<sub>%d</sub> %d" % (c, b) if c != 10 else "x = log<sub>10</sub> %d" % b, "x = %s" % fq(Fr(c, b)), "impossibile"],
                     "Non c’è una base comune: per definizione <b>x = %s %d</b> (≈ %s)." % ("log<sub>%d</sub>" % b if b != 10 else "log", c, ("%.3f" % (__import__("math").log(c) / __import__("math").log(b))).replace(".", ",")))
    n = R.randint(2, 9)
    return M("Risolvi: e<sup>x</sup> = %d" % n, "x = ln %d" % n, ["x = log %d" % n, "x = %s" % fq(Fr(n, 3)), "x = e<sup>%d</sup>" % n],
             "Applico il logaritmo naturale: <b>x = ln %d</b>." % n)


def s2_dis():
    b = R.choice([2, 3, Fr(1, 2), Fr(1, 3), 5])
    n = R.randint(-3, 4)
    op = R.choice(["&gt;", "&lt;", "≥", "≤"])
    val = Fr(b) ** n
    res = op if b > 1 else {"&gt;": "&lt;", "&lt;": "&gt;", "≥": "≤", "≤": "≥"}[op]
    bs = fq(b) if Fr(b).denominator == 1 else "(%s)" % fq(b)
    ans = "x %s %s" % (res, fq(n))
    return M("Risolvi: %s %s %s" % (pw(bs, "x"), op, fq(val)), ans, W("x %s %s" % ({"&gt;": "&lt;", "&lt;": "&gt;", "≥": "≤", "≤": "≥"}[res], fq(n)), "x %s %s" % (res, fq(-n)) if n else "x %s 1" % res, "x %s %s" % (res, fq(val)) if val != n else "x %s %s" % (res, fq(n + 1)), "∀x ∈ ℝ"),
             "%s = %s<sup>%s</sup>. La base è %s 1, quindi %s: <b>%s</b>." % (fq(val), bs, fq(n), "maggiore di" if b > 1 else "minore di", "il verso resta" if b > 1 else "il verso cambia", ans))


def s3_logeq():
    b = R.choice([2, 3, 10, 5])
    k = R.choice(["sempl", "somma"])
    if k == "sempl":
        a = R.randint(-5, 5)
        n = R.randint(1, 4) if b != 10 else R.randint(1, 3)
        x = b ** n + a
        arg = P2(0, 1, -a)
        lg = "log<sub>%d</sub>" % b if b != 10 else "log"
        return M("Risolvi: %s(%s) = %d" % (lg, arg, n), "x = %s" % d(x), ["x = %s" % d(t) for t in W(b * n + a, b ** n - a, n + a if n + a != x else x + 1, b ** (n + 1) + a)],
                 "C.E.: %s &gt; 0. %s = %d<sup>%d</sup> = %s → <b>x = %s</b>, accettabile." % (arg, arg, b, n, d(b ** n), d(x)))
    # log(x) + log(x − a) = log(N)  → x(x − a) = N
    a = R.randint(1, 6)
    x = R.randint(a + 1, a + 7)
    N = x * (x - a)
    other = -(x - a)
    lg = "log<sub>%d</sub>" % b if b != 10 else "log"
    return M("Risolvi: %s x + %s(x − %d) = %s %d" % (lg, lg, a, lg, N), "x = %d" % x, ["x = %s ∨ x = %d" % (fq(other), x), "x = %s" % fq(other), "x = %s" % d(Fr(N + a, 2))],
             "C.E.: x &gt; %d. x(x − %d) = %d → x² − %dx − %d = 0 → x = %s ∨ x = %d. Solo <b>x = %d</b> rispetta le C.E." % (a, a, N, a, N, fq(other), x, x))


def s4_logdis():
    b = R.choice([2, 3, Fr(1, 2), Fr(1, 3)])
    n = R.randint(1, 3)
    a = R.randint(-4, 4)
    op = R.choice(["&gt;", "&lt;"])
    arg = P2(0, 1, -a)
    bs = fq(b) if Fr(b).denominator == 1 else fq(b).replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", "")
    v = Fr(b) ** n + a
    up = (op == "&gt;") == (b > 1)
    if up:
        ans = "x &gt; %s" % fq(v)
        w = ["%s &lt; x &lt; %s" % (fq(a), fq(v)), "x &lt; %s" % fq(v), "x &gt; %s" % fq(a)]
    else:
        ans = "%s &lt; x &lt; %s" % (fq(a), fq(v))
        w = ["x &lt; %s" % fq(v), "x &gt; %s" % fq(v), "x &gt; %s" % fq(a)]
    return M("Risolvi: log<sub>%s</sub>(%s) %s %d" % (bs, arg, op, n), ans, w,
             "C.E.: x &gt; %s. Scrivo %d come logaritmo: %d = log<sub>%s</sub> %s. La base è %s 1, quindi %s: %s %s %s. Insieme alle C.E.: <b>%s</b>." % (fq(a), n, n, bs, fq(Fr(b) ** n), "maggiore di" if b > 1 else "minore di", "il verso resta" if b > 1 else "il verso cambia", arg, "&gt;" if up else "&lt;", fq(Fr(b) ** n), ans))


def s5_probl():
    k = R.choice(["capitale", "pop"])
    if k == "capitale":
        r = R.choice([2, 3, 4, 5])
        C = R.choice([1000, 2000, 5000])
        return M("Un capitale di %s € è investito al %d%% annuo composto: C(t) = %s · (1,%02d)<sup>t</sup>. Dopo quanti anni raddoppia? (Scegli l’espressione esatta)" % (d(C), r, d(C), r),
                 "t = ln 2 / ln 1,%02d" % r, ["t = 2 / 1,%02d" % r, "t = ln 1,%02d / ln 2" % r, "t = %s / %d" % (d(C), r)],
                 "%s · 1,%02d<sup>t</sup> = %s → 1,%02d<sup>t</sup> = 2 → <b>t = ln 2 / ln 1,%02d</b> (≈ %s anni)." % (d(C), r, d(2 * C), r, r, ("%.1f" % (__import__("math").log(2) / __import__("math").log(1 + r / 100))).replace(".", ",")))
    n0 = R.choice([100, 500, 1000])
    k2 = R.choice([2, 3])
    m = R.choice([4, 8, 9, 16, 27])
    import math
    t = round(math.log(m, k2))
    if k2 ** t != m:
        return None
    return M("Una popolazione di %d individui si moltiplica per %d ogni anno. Dopo quanti anni arriva a %s individui?" % (n0, k2, d(n0 * m)), "%d anni" % t, ["%d anni" % x for x in W(m // k2, t + 1, m, t - 1 if t > 1 else t + 2)],
             "%d · %d<sup>t</sup> = %s → %d<sup>t</sup> = %d → <b>t = %d</b>." % (n0, k2, d(n0 * m), k2, m, t))


def main():
    seen = set()
    sets = [
        ("Equazioni esponenziali", mix(R, seen, [(s1_base, 14), (s2_log, 6)])),
        ("Incognita ausiliaria e logaritmi", mix(R, seen, [(s1_aus, 10), (s2_log, 10)])),
        ("Disequazioni esponenziali", mix(R, seen, [(s2_dis, 20)])),
        ("Equazioni logaritmiche", mix(R, seen, [(s3_logeq, 20)])),
        ("Disequazioni logaritmiche e problemi", mix(R, seen, [(s4_logdis, 14), (s5_probl, 6)])),
    ]
    body = L(["<b>Equazioni esponenziali</b>: se si possono scrivere i due membri con la stessa base, si uguagliano gli esponenti (a<sup>f(x)</sup> = a<sup>g(x)</sup> ⟺ f(x) = g(x)). Altrimenti si usano i logaritmi: a<sup>x</sup> = b ⟺ x = log<sub>a</sub> b.",
              "Con termini come 4<sup>x</sup> e 2<sup>x</sup> si pone t = 2<sup>x</sup> (con t &gt; 0) e si risolve un’equazione di secondo grado.",
              "Nelle <b>disequazioni</b> esponenziali e logaritmiche il verso resta se la base è maggiore di 1 e <b>cambia</b> se la base è tra 0 e 1.",
              "Nelle <b>equazioni logaritmiche</b> si scrivono prima le condizioni di esistenza (argomenti positivi) e alla fine si controllano le soluzioni."],
             [("2<sup>x+1</sup> = 32", ["32 = 2<sup>5</sup>", "x + 1 = 5"], "x = 4"),
              ("log<sub>3</sub>(x − 1) &lt; 2", ["C.E. x &gt; 1", "x − 1 &lt; 9"], "1 &lt; x &lt; 10")],
             [["(1/2)<sup>x</sup> &gt; 4 → x &gt; −2", "Con base minore di 1 il verso cambia: x &lt; −2."],
              ["Non scrivere le C.E.", "Gli argomenti dei logaritmi devono essere positivi: alcune soluzioni si scartano."],
              ["Accettare t = 2<sup>x</sup> = −1", "Un’esponenziale è sempre positiva: quella soluzione si scarta."]])
    faq = [("Perché nelle disequazioni con base minore di 1 il verso cambia?", "Perché le funzioni y = a<sup>x</sup> e y = log<sub>a</sub> x con 0 &lt; a &lt; 1 sono decrescenti: a valori più grandi della x corrispondono valori più piccoli della y."),
           ("Come si risolve 3<sup>x</sup> = 7?", "Non si può scrivere 7 come potenza intera di 3: si usa la definizione di logaritmo, x = log<sub>3</sub> 7 = ln 7 / ln 3 ≈ 1,77.")]
    unit(G, R, "equazioni-esponenziali-e-logaritmiche", "F",
         "Equazioni e disequazioni esponenziali e logaritmiche; modelli di crescita",
         "Equazioni e disequazioni esponenziali e logaritmiche", "Equazioni esponenziali e logaritmiche",
         "Schede di matematica per la quarta liceo su equazioni e disequazioni esponenziali e logaritmiche: stessa base, incognita ausiliaria, uso dei logaritmi, condizioni di esistenza, verso delle disequazioni, problemi di crescita. 100 esercizi con soluzioni.",
         "Base < 1: il verso cambia.", "aˣ = b ⟺ x = logₐ b; nelle logaritmiche prima le condizioni di esistenza.",
         body, faq, sets, 3)


if __name__ == "__main__":
    main()
