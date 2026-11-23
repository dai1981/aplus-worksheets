# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Equazioni differenziali (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_equazioni_differenziali.py
Verifica di una soluzione, equazioni del tipo y′ = f(x), y′ = ky (crescita e decadimento esponenziale), equazioni
lineari del primo ordine y′ = ay + b, equazioni a variabili separabili, problema di Cauchy, equazioni del secondo
ordine lineari omogenee a coefficienti costanti (equazione caratteristica).
Errori: dimenticare la costante, y = e^{kx} + C invece di C e^{kx}, sbagliare il caso Δ &lt; 0.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, nz, FR, poly

R = random.Random(72512)
G = "quinta-liceo"


def ekx(k, v="x"):
    return "e<sup>%s</sup>" % poly([k, 0], v) if k != 0 else "1"


def cf(c, x):
    return x if c == 1 else ("−" + x if c == -1 else "%s%s" % (fq(c), x))


def s1_ver():
    k = nz(R, -4, 4)
    T = R.choice(["exp", "sen", "poly", "cos"])
    if T == "exp":
        y = cf(R.choice([1, 2, 3, 5]), ekx(k))
        eqs = ["y′ = %sy" % ("" if k == 1 else ("−" if k == -1 else fq(k))), "y′ = %sy" % fq(-k) if k != -1 else "y′ = y", "y′ = %s" % poly([1, k], "y"), "y′ = %s" % poly([k, 0])]
        return M("Di quale equazione differenziale è soluzione y = %s?" % y, eqs[0], eqs[1:], "y′ = %s · y: <b>%s</b>." % (fq(k), eqs[0]))
    if T in ("sen", "cos"):
        w = R.randint(2, 5)
        y = "%s(%dx)" % ("sen" if T == "sen" else "cos", w)
        a = "y″ + %dy = 0" % (w * w)
        return M("Di quale equazione differenziale è soluzione y = %s?" % y, a, ["y″ − %dy = 0" % (w * w), "y″ + %dy = 0" % w, "y′ + %dy = 0" % w],
                 "y″ = −%d %s = −%dy, quindi <b>%s</b>." % (w * w, y, w * w, a))
    a = R.randint(1, 5)
    return M("Quale funzione è soluzione di x y′ = 2y?", "y = %sx²" % (a if a > 1 else ""), ["y = x² + %d" % a, "y = %sx" % (2 * a), "y = %s" % ekx(2)],
             "Con y = %sx²: x · %sx = 2 · %sx², vero. <b>y = %sx²</b>." % (a if a > 1 else "", 2 * a, a if a > 1 else "", a if a > 1 else ""))


def s2_fx():
    a, b = nz(R, -3, 3), R.randint(-5, 5)
    x0 = R.choice([0, 0, 1, -1])
    y0 = R.randint(-6, 6)
    c = y0 - a * x0 * x0 - b * x0
    f = lambda cc: "y = %s" % poly([a, b, cc])
    return M("Risolvi il problema di Cauchy y′ = %s, y(%s) = %s." % (poly([2 * a, b]), fq(x0), fq(y0)), f(c),
             [f(v) for v in W(-c, y0, c + 1, c - 2, y0 + 2 * a * x0 + b, c + 3) if v != c][:3],
             "Integro: y = %s + c; imponendo y(%s) = %s si ottiene c = %s. <b>%s</b>." % (poly([a, b, 0]), fq(x0), fq(y0), fq(c), f(c)))


def s3_exp():
    k = R.choice([1, 2, 3, -1, -2, Fr(1, 2), -Fr(1, 2)])
    y0 = R.choice([1, 2, 3, 5, 10, 4])
    kk = fq(k) if k not in (1, -1) else ("" if k == 1 else "−")
    ans = "y = %s" % cf(y0, ekx(k))
    return M("Risolvi y′ = %sy con y(0) = %d." % (kk, y0), ans,
             ["y = %s + %d" % (ekx(k), y0 - 1) if y0 > 1 else "y = %s + 1" % ekx(k), "y = %s" % cf(y0, ekx(-k)), "y = %s" % cf(k, ekx(y0)) if k not in (1, -1, y0) else "y = %s" % cf(y0 + 1, ekx(k))],
             "La soluzione generale è y = C %s; y(0) = C = %d: <b>%s</b>." % (ekx(k), y0, ans))


def s3_dec():
    T = R.choice(["dimezza", "raddoppia", "valore"])
    if T == "dimezza":
        k = R.choice([2, 3, 5, 10])
        return M("Una sostanza decade secondo N′ = −kN con k = ln 2 / %d (t in anni). Qual è il tempo di dimezzamento?" % k, "%d anni" % k,
                 ["%d anni" % x for x in W(2 * k, k * k, k + 1) if x != k][:3] if k > 2 else ["4 anni", "1 anno", "3 anni"],
                 "N(t) = N<sub>0</sub> e<sup>−kt</sup> = N<sub>0</sub>/2 per kt = ln 2, cioè t = ln 2/k = <b>%d anni</b>." % k)
    if T == "raddoppia":
        d = R.choice([2, 3, 4, 5, 6])
        n = R.choice([2, 3, 4])
        return M("Una popolazione cresce secondo P′ = kP e raddoppia ogni %d ore. Di quante volte è aumentata dopo %d ore?" % (d, d * n), "%d volte" % (2 ** n),
                 ["%d volte" % x for x in W(2 * n, n + 1, 2 ** (n + 1), 2 ** n + 1) if x != 2 ** n][:3],
                 "P(t) = P<sub>0</sub> · 2<sup>t/%d</sup>; dopo %d ore 2<sup>%d</sup> = <b>%d volte</b>." % (d, d * n, n, 2 ** n))
    p0 = R.choice([100, 200, 500, 1000])
    k = R.choice([2, 3])
    return M("y′ = %sy, y(0) = %d. Quanto vale y(ln 2)?" % (fq(k), p0), str(p0 * 2 ** k), [str(x) for x in W(p0 * 2, p0 * k, p0 * 2 ** k * 2, p0 + 2 ** k) if x != p0 * 2 ** k][:3],
             "y = %d e<sup>%dx</sup>; y(ln 2) = %d · e<sup>%d ln 2</sup> = %d · 2<sup>%d</sup> = <b>%d</b>." % (p0, k, p0, k, p0, k, p0 * 2 ** k))


def s3_lin():
    a = R.choice([1, 2, 3, -1, -2, -3])
    b = nz(R, -8, 8)
    if b % a:
        return None
    e0 = Fr(-b, a)
    ask = R.choice(["gen", "eq"])
    aa = cf(a, "y")
    if ask == "eq":
        return M("Qual è la soluzione costante (di equilibrio) di y′ = %s %s %d?" % (aa, "+" if b > 0 else "−", abs(b)), "y = %s" % fq(e0),
                 ["y = %s" % fq(v) for v in W(-e0, Fr(b), Fr(a), e0 + 1, e0 - 1, 2 * e0) if v != e0][:3], "Pongo y′ = 0: %s %s %d = 0, quindi <b>y = %s</b>." % (aa, "+" if b > 0 else "−", abs(b), fq(e0)))
    ans = "y = C %s %s %s" % (ekx(a), "+" if e0 > 0 else "−", fq(abs(e0)))
    w = ["y = C %s %s %s" % (ekx(a), "−" if e0 > 0 else "+", fq(abs(e0))), "y = C %s %s %s" % (ekx(-a), "+" if e0 > 0 else "−", fq(abs(e0))), "y = %s + C" % ekx(a)]
    return M("Qual è la soluzione generale di y′ = %s %s %d?" % (aa, "+" if b > 0 else "−", abs(b)), ans, w,
             "Equazione lineare: soluzione dell’omogenea C %s più la soluzione costante y = %s. <b>%s</b>." % (ekx(a), fq(e0), ans))


def s4_sep():
    T = R.choice(["xy", "x_y", "xy2", "y_x", "ey"])
    k = R.randint(1, 4)
    if T == "xy":
        ans = "y = C e<sup>%s</sup>" % (FR("x²", "2") if k == 1 else ("x²" if k == 2 else "%s x²" % FR(str(k), "2")))
        return M("Risolvi l’equazione a variabili separabili y′ = %sxy." % (k if k > 1 else ""), ans,
                 ["y = C e<sup>%sx</sup>" % (k if k > 1 else ""), "y = %s + C" % ("x²" if k == 2 else ("%s x²" % FR(str(k), "2"))), "y = C x<sup>%d</sup>" % (k + 1)],
                 "dy/y = %sx dx; ln |y| = %s x² + c, quindi <b>%s</b>." % (k if k > 1 else "", fq(Fr(k, 2)), ans))
    if T == "x_y":
        ans = "y² = x² + C" if k == 1 else "y² = %dx² + C" % k
        return M("Risolvi y′ = %s." % FR("%sx" % (k if k > 1 else ""), "y"), ans, ["y = %sx + C" % (k if k > 1 else ""), "y² = −%sx² + C" % (k if k > 1 else ""), "y = C e<sup>x²</sup>"],
                 "y dy = %sx dx; y²/2 = %s x²/2 + c: <b>%s</b>." % (k if k > 1 else "", k if k > 1 else "", ans))
    if T == "xy2":
        y0 = R.choice([1, 2, -1])
        # y′ = −x/y? use y′ = x/y with y(0) = y0 → y² = x² + y0²
        return M("Risolvi il problema di Cauchy y′ = x/y, y(0) = %s." % fq(y0), "y = %s√(x² + %d)" % ("" if y0 > 0 else "−", y0 * y0),
                 ["y = %s√(x² − %d)" % ("" if y0 > 0 else "−", y0 * y0), "y = x + %d" % y0 if y0 > 0 else "y = x − 1", "y = %s√(x² + %d)" % ("−" if y0 > 0 else "", y0 * y0)],
                 "y² = x² + C, y(0) = %s dà C = %d; si sceglie il segno di y(0): <b>y = %s√(x² + %d)</b>." % (fq(y0), y0 * y0, "" if y0 > 0 else "−", y0 * y0))
    if T == "y_x":
        return M("Risolvi y′ = %s (x &gt; 0)." % FR("%sy" % (k if k > 1 else ""), "x"), "y = C x<sup>%d</sup>" % k if k > 1 else "y = C x",
                 ["y = C e<sup>%sx</sup>" % (k if k > 1 else ""), "y = x<sup>%d</sup> + C" % k if k > 1 else "y = x + C", "y = C ln x"],
                 "dy/y = %s dx/x; ln |y| = %s ln x + c: <b>%s</b>." % (k if k > 1 else "", k if k > 1 else "", "y = C x<sup>%d</sup>" % k if k > 1 else "y = C x"))
    return M("Risolvi y′ = %s e<sup>−y</sup>." % (k if k > 1 else ""), "y = ln(%sx + C)" % (k if k > 1 else ""), ["y = −ln(%sx + C)" % (k if k > 1 else ""), "y = e<sup>%sx</sup> + C" % (k if k > 1 else ""), "y = ln %sx + C" % (k if k > 1 else "")],
             "e<sup>y</sup> dy = %s dx; e<sup>y</sup> = %sx + C: <b>y = ln(%sx + C)</b>." % (k if k > 1 else "", k if k > 1 else "", k if k > 1 else ""))


def ode(p, q):
    t = "y″"
    for c, v in ((p, "y′"), (q, "y")):
        if c:
            t += " %s %s%s" % ("+" if c > 0 else "−", abs(c) if abs(c) != 1 else "", v)
    return t + " = 0"


def s5_car():
    kind = R.choice(["dist", "dist", "dopp", "compl", "osc"])
    if kind == "dist":
        r1, r2 = R.sample([-4, -3, -2, -1, 1, 2, 3, 4, 0], 2)
        p, q = -(r1 + r2), r1 * r2
        eq = ode(p, q)
        term = lambda r: ("C e<sup>%s</sup>" % poly([r, 0])) if r else "C"
        ans = "y = %s + %s" % (term(r1).replace("C", "C<sub>1</sub>"), term(r2).replace("C", "C<sub>2</sub>"))
        wr = ["y = %s + %s" % (term(-r1).replace("C", "C<sub>1</sub>"), term(-r2).replace("C", "C<sub>2</sub>")),
              "y = (C<sub>1</sub> + C<sub>2</sub>x) e<sup>%s</sup>" % poly([r1, 0]) if r1 else "y = C<sub>1</sub> + C<sub>2</sub>x",
              "y = C<sub>1</sub> cos %sx + C<sub>2</sub> sen %sx" % (abs(r1) if abs(r1) > 1 else "", abs(r1) if abs(r1) > 1 else "") if r1 else "y = C<sub>1</sub> e<sup>x</sup>"]
        return M("Risolvi %s." % eq, ans, wr, "Equazione caratteristica %s = 0 con radici %s e %s: <b>%s</b>." % (poly([1, p, q], "r"), fq(r1), fq(r2), ans))
    if kind == "dopp":
        r = nz(R, -3, 3)
        p, q = -2 * r, r * r
        eq = ode(p, q)
        ans = "y = (C<sub>1</sub> + C<sub>2</sub>x) e<sup>%s</sup>" % poly([r, 0])
        return M("Risolvi %s." % eq, ans, ["y = C<sub>1</sub> e<sup>%s</sup> + C<sub>2</sub> e<sup>%s</sup>" % (poly([r, 0]), poly([-r, 0])), "y = (C<sub>1</sub> + C<sub>2</sub>x) e<sup>%s</sup>" % poly([-r, 0]), "y = C e<sup>%s</sup>" % poly([r, 0])],
                 "r² %s %sr + %d = (r %s %d)² = 0: radice doppia r = %s, quindi <b>%s</b>." % ("+" if p > 0 else "−", abs(p), q, "−" if r > 0 else "+", abs(r), fq(r), ans))
    if kind == "compl":
        al = R.choice([-2, -1, 1, 2])
        be = R.choice([1, 2, 3])
        p, q = -2 * al, al * al + be * be
        eq = ode(p, q)
        bx = "%sx" % (be if be > 1 else "")
        ans = "y = e<sup>%s</sup>(C<sub>1</sub> cos %s + C<sub>2</sub> sen %s)" % (poly([al, 0]), bx, bx)
        return M("Risolvi %s." % eq, ans, [z for z in ["y = e<sup>%s</sup>(C<sub>1</sub> cos %s + C<sub>2</sub> sen %s)" % (poly([be, 0]), "%sx" % (abs(al) if abs(al) > 1 else ""), "%sx" % (abs(al) if abs(al) > 1 else "")),
                                           "y = C<sub>1</sub> e<sup>%s</sup> + C<sub>2</sub> e<sup>%s</sup>" % (poly([al + be, 0]), poly([al - be, 0])), "y = e<sup>%s</sup>(C<sub>1</sub> cos %s + C<sub>2</sub> sen %s)" % (poly([-al, 0]), bx, bx), "y = C<sub>1</sub> cos %s + C<sub>2</sub> sen %s" % (bx, bx)] if "e<sup>0</sup>" not in z],
                 "Δ &lt; 0: le radici sono r = %s ± %si; la soluzione è <b>%s</b>." % (fq(al), be if be > 1 else "", ans))
    w = R.randint(2, 6)
    ans = "y = C<sub>1</sub> cos %dx + C<sub>2</sub> sen %dx" % (w, w)
    return M("Risolvi y″ + %dy = 0." % (w * w), ans, ["y = C<sub>1</sub> e<sup>%dx</sup> + C<sub>2</sub> e<sup>−%dx</sup>" % (w, w), "y = C<sub>1</sub> cos %dx + C<sub>2</sub> sen %dx" % (w * w, w * w), "y = (C<sub>1</sub> + C<sub>2</sub>x) e<sup>%dx</sup>" % w],
             "r² + %d = 0 dà r = ±%di: <b>%s</b> (moto armonico)." % (w * w, w, ans))


def main():
    seen = set()
    sets = [
        ("Soluzioni di un’equazione differenziale", mix(R, seen, [(s1_ver, 10), (s2_fx, 10)])),
        ("Crescita e decadimento esponenziale", mix(R, seen, [(s3_exp, 12), (s3_dec, 8)])),
        ("Equazioni lineari del primo ordine", mix(R, seen, [(s3_lin, 14), (s3_exp, 6)])),
        ("Equazioni a variabili separabili", mix(R, seen, [(s4_sep, 16), (s2_fx, 4)])),
        ("Equazioni del secondo ordine", mix(R, seen, [(s5_car, 20)])),
    ]
    body = L(["Un’<b>equazione differenziale</b> lega una funzione y(x) alle sue derivate. La soluzione generale contiene costanti arbitrarie; il <b>problema di Cauchy</b> fissa le costanti con condizioni iniziali come y(x<sub>0</sub>) = y<sub>0</sub>.",
              "y′ = ky ha soluzione y = C e<sup>kx</sup> (crescita se k &gt; 0, decadimento se k &lt; 0). y′ = ay + b ha soluzione y = C e<sup>ax</sup> − b/a.",
              "<b>Variabili separabili</b> y′ = g(x) h(y): si scrive dy/h(y) = g(x) dx e si integrano i due membri.",
              "y″ + py′ + qy = 0: equazione caratteristica r² + pr + q = 0. Radici reali distinte: C<sub>1</sub>e<sup>r<sub>1</sub>x</sup> + C<sub>2</sub>e<sup>r<sub>2</sub>x</sup>; doppia: (C<sub>1</sub> + C<sub>2</sub>x)e<sup>rx</sup>; complesse α ± βi: e<sup>αx</sup>(C<sub>1</sub> cos βx + C<sub>2</sub> sen βx)."],
             [("y′ = 3y, y(0) = 2", ["y = C e<sup>3x</sup>", "C = 2"], "y = 2e<sup>3x</sup>"),
              ("y″ − 5y′ + 6y = 0", ["r² − 5r + 6 = 0, r = 2 e r = 3"], "y = C<sub>1</sub>e<sup>2x</sup> + C<sub>2</sub>e<sup>3x</sup>")],
             [["Scrivere y = e<sup>kx</sup> + C", "La costante moltiplica: y = C e<sup>kx</sup>."],
              ["Dimenticare la costante quando si integra", "Senza costante si trova una sola soluzione, non la soluzione generale."],
              ["Usare esponenziali reali con Δ &lt; 0", "Con radici complesse compaiono seno e coseno."]])
    faq = [("A che cosa servono le equazioni differenziali?", "Descrivono fenomeni in cui la velocità di variazione dipende dallo stato: crescita di popolazioni, decadimento radioattivo, raffreddamento, moto armonico di una molla."),
           ("Quante condizioni servono per un’equazione del secondo ordine?", "Due, per esempio y(0) e y′(0), perché la soluzione generale contiene due costanti C<sub>1</sub> e C<sub>2</sub>.")]
    unit(G, R, "equazioni-differenziali", "F",
         "Equazioni differenziali del primo ordine e del secondo ordine lineari a coefficienti costanti; problema di Cauchy",
         "Equazioni differenziali", "Equazioni differenziali",
         "Schede di matematica per la quinta liceo sulle equazioni differenziali: verifica delle soluzioni, problema di Cauchy, crescita e decadimento esponenziale, equazioni lineari del primo ordine, variabili separabili, equazioni del secondo ordine a coefficienti costanti. 100 esercizi con soluzioni.",
         "y′ = ky ⇒ y = C e^(kx)", "Secondo ordine: equazione caratteristica r² + pr + q = 0.",
         body, faq, sets, 12)


if __name__ == "__main__":
    main()
