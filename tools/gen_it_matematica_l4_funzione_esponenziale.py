# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Potenze a esponente reale e funzione esponenziale (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l4_funzione_esponenziale.py
Potenze con esponente razionale (radici), proprietà delle potenze, funzione y = aˣ (dominio, codominio, monotonia, punto (0; 1),
asintoto), confronto di potenze, grafici traslati, il numero e, crescita e decadimento esponenziale (raddoppio, tempo di dimezzamento).
Errori: 8^(2/3) = 16/3, aˣ negativo, y = 2ˣ − 3 con asintoto y = 0, (1/2)ˣ crescente.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, kurve, relabel

R = random.Random(72401)
G = "quarta-liceo"
BLUE = "#1f6fd1"


def ex(b, e):
    return "%s<sup>%s</sup>" % (fq(b) if Fr(b).denominator == 1 and b >= 0 else "(%s)" % fq(b), fq(e).replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", ""))


def s1_raz():
    base, root = R.choice([(8, 2), (27, 3), (16, 2), (4, 2), (9, 3), (32, 2), (64, 4), (25, 5), (81, 3), (125, 5), (1000, 10), (16, 4)])
    # base = root^k
    k = 0
    t = base
    while t > 1:
        t //= root
        k += 1
    n = R.choice([1, 2, 3, -1, -2])
    dd = k if R.random() < 0.7 else R.choice([x for x in range(2, k + 1) if k % x == 0] or [k])
    e = Fr(n, dd)
    if e.denominator == 1:
        return None
    v = Fr(base) ** e if e.denominator == 1 else Fr(root) ** (k * e)
    if (k * e).denominator != 1 or abs(v) > 100000 or (v.numerator > 100000):
        return None
    w = [Fr(base) * e if (Fr(base) * e).denominator < 50 else None, Fr(root) ** abs(k * e) if e < 0 else (1 / v if v != 1 else Fr(2)), v * root, Fr(base, dd) if base % dd == 0 else None, -v, v * v if v * v < 10000 else None]
    return M("Calcola %s." % ex(base, e), fq(v), [fq(x) for x in W(*w) if x != v],
             "a<sup>m/n</sup> = <sup>n</sup>√(a<sup>m</sup>): %d = %d<sup>%d</sup>, quindi %s = %d<sup>%s</sup> = <b>%s</b>." % (base, root, k, ex(base, e), root, fq(k * e), fq(v)))


def s1_prop():
    a = R.choice([2, 3, 5])
    x, y = R.randint(1, 5), R.randint(1, 5)
    k = R.choice(["mul", "div", "pp"])
    s3 = "√%d" % R.choice([2, 3])
    if k == "mul":
        q = "%s<sup>%s + %d</sup> · %s<sup>%s − %d</sup>" % (a, s3, x, a, s3, y)
        ans = "%d<sup>2%s %s %d</sup>" % (a, s3, "+" if x - y >= 0 else "−", abs(x - y)) if x != y else "%d<sup>2%s</sup>" % (a, s3)
        w = ["%d<sup>%s</sup>" % (a * a, s3), "%d<sup>%d</sup>" % (a, x - y if x != y else 1), "%d<sup>2%s %s %d</sup>" % (a, s3, "+", x + y)]
        e = "Le proprietà delle potenze valgono anche con esponenti reali: si sommano gli esponenti, <b>%s</b>." % ans
    elif k == "div":
        q = "%d<sup>%s + %d</sup> : %d<sup>%s</sup>" % (a, s3, x, a, s3)
        ans = "%d<sup>%d</sup> = %s" % (a, x, d(a ** x))
        w = ["%d<sup>%d</sup> = %s" % (a, x + 1, d(a ** (x + 1))), "1", "%d<sup>2%s + %d</sup>" % (a, s3, x)]
        e = "Si sottraggono gli esponenti: (%s + %d) − %s = %d: <b>%s</b>." % (s3, x, s3, x, ans)
    else:
        q = "(%d<sup>%s</sup>)<sup>%s</sup>" % (a, s3, s3)
        n = int(s3[1:])
        ans = "%d<sup>%d</sup> = %s" % (a, n, d(a ** n))
        w = ["%d<sup>2%s</sup>" % (a, s3), "%d<sup>%d</sup> = %s" % (a, 2 * n, d(a ** (2 * n))), "%d" % a]
        e = "Si moltiplicano gli esponenti: %s · %s = %d: <b>%s</b>." % (s3, s3, n, ans)
    return M("Semplifica: %s" % q, ans, w, e)


FUN = [("y = 3<sup>x</sup>", "crescente", "ℝ", "y &gt; 0"), ("y = (1/2)<sup>x</sup>", "decrescente", "ℝ", "y &gt; 0"), ("y = 2<sup>x</sup>", "crescente", "ℝ", "y &gt; 0"),
       ("y = (2/3)<sup>x</sup>", "decrescente", "ℝ", "y &gt; 0"), ("y = e<sup>x</sup>", "crescente", "ℝ", "y &gt; 0"), ("y = 0,4<sup>x</sup>", "decrescente", "ℝ", "y &gt; 0"),
       ("y = 10<sup>x</sup>", "crescente", "ℝ", "y &gt; 0"), ("y = (3/4)<sup>x</sup>", "decrescente", "ℝ", "y &gt; 0")]


def s2_prop():
    f, mono, dom, cod = R.choice(FUN)
    k = R.choice(["mono", "cod", "punto"])
    if k == "mono":
        return M("La funzione %s è…" % f, mono, ["decrescente" if mono == "crescente" else "crescente", "costante", "prima crescente poi decrescente"],
                 "y = a<sup>x</sup> è crescente se a &gt; 1, decrescente se 0 &lt; a &lt; 1: <b>%s</b>." % mono)
    if k == "cod":
        return M("Qual è l’insieme immagine (codominio) di %s?" % f, cod, ["ℝ", "y ≥ 0", "y &gt; 1"],
                 "Una potenza con base positiva è sempre positiva e assume tutti i valori positivi: <b>y &gt; 0</b>.")
    return M("In quale punto il grafico di %s incontra l’asse y?" % f, "(0; 1)", ["(0; 0)", "(1; 0)", "non incontra l’asse y"],
             "Per x = 0: a<sup>0</sup> = 1, quindi <b>(0; 1)</b> (per ogni base).")


def s2_conf():
    a = R.choice([2, 3, Fr(1, 2), Fr(1, 3), Fr(3, 4), 5])
    x1, x2 = R.sample([-3, -2, -1, 2, 3, 4, 5, Fr(1, 2)], 2)
    v1, v2 = float(a) ** float(x1), float(a) ** float(x2)
    big = ex(a, x1) if v1 > v2 else ex(a, x2)
    sm = ex(a, x2) if v1 > v2 else ex(a, x1)
    return M("Qual è il maggiore tra %s e %s?" % (ex(a, x1), ex(a, x2)), big, [sm, "sono uguali", "non si può dire senza calcolatrice"],
             "La base è %s 1, quindi la funzione è %s: %s. Il maggiore è <b>%s</b>." % ("maggiore di" if a > 1 else "minore di", "crescente" if a > 1 else "decrescente", "esponente maggiore → valore maggiore" if a > 1 else "esponente maggiore → valore minore", big))


def s3_trasl():
    a = R.choice([2, 3])
    h, k = R.randint(-3, 3), R.randint(-4, 4)
    if k == 0:
        return None
    f = "y = %d<sup>x%s</sup> %s %d" % (a, "" if h == 0 else (" − %d" % h if h > 0 else " + %d" % -h), "+" if k > 0 else "−", abs(k))
    t = R.choice(["asint", "cod"])
    fig = relabel(kurve([(lambda x, a=a, h=h, k=k: a ** (x - h) + k, BLUE, "")], (-4, 4, 1), (-5, 7, 1), W=300, H=280), "grafico di una funzione esponenziale")
    if t == "asint":
        return M("%sQual è l’asintoto orizzontale di %s?" % (fig, f), "y = %s" % fq(k), ["y = 0", "y = %s" % fq(-k), "x = %s" % fq(h) if h else "x = %s" % fq(k)],
                 "Il grafico di y = %d<sup>x</sup> (asintoto y = 0) è traslato in verticale di %s: <b>y = %s</b>." % (a, fq(k), fq(k)))
    return M("Qual è l’insieme immagine di %s?" % f, "y &gt; %s" % fq(k), ["y &gt; 0", "ℝ", "y &gt; %s" % fq(-k)],
             "La potenza è sempre positiva, quindi y &gt; %s: <b>y &gt; %s</b>." % (fq(k), fq(k)))


def s4_cresc():
    k = R.choice(["batteri", "dimezz", "e"])
    if k == "batteri":
        N0 = R.choice([100, 200, 500, 1000])
        T = R.choice([2, 3, 4, 5])
        t = T * R.randint(2, 5)
        v = N0 * 2 ** (t // T)
        return M("Una popolazione di %d batteri raddoppia ogni %d ore: N(t) = %d · 2<sup>t/%d</sup>. Quanti batteri ci sono dopo %d ore?" % (N0, T, N0, T, t), d(v), [d(x) for x in W(N0 * 2 * t // T, N0 * 2 ** t if t < 12 else N0 * 2 ** (t // T + 1), N0 * (t // T) ** 2, N0 * 2 ** (t // T - 1))],
                 "t/%d = %d raddoppi: %d · 2<sup>%d</sup> = <b>%s</b>." % (T, t // T, N0, t // T, d(v)))
    if k == "dimezz":
        m0 = R.choice([80, 160, 200, 320, 640])
        T = R.choice([5, 8, 10, 12, 30])
        n = R.randint(2, 4)
        v = Fr(m0, 2 ** n)
        return M("Una sostanza radioattiva ha un tempo di dimezzamento di %d anni. Partendo da %d g, quanti grammi restano dopo %d anni?" % (T, m0, n * T), "%s g" % d(v), ["%s g" % d(x) for x in W(Fr(m0, 2 * n), m0 - n * T if m0 > n * T else None, Fr(m0, 2 ** (n - 1)), Fr(m0, 2 ** (n + 1)))],
                     "%d anni sono %d dimezzamenti: %d · (1/2)<sup>%d</sup> = <b>%s g</b>." % (n * T, n, m0, n, d(v)))
    qs = [("Quanto vale il numero e (numero di Nepero), arrotondato?", "2,718", ["3,141", "1,618", "2,236"]),
          ("Il numero e è…", "irrazionale (limite di (1 + 1/n)<sup>n</sup>)", ["un numero intero", "una frazione", "uguale a 22/7"]),
          ("La funzione y = e<sup>x</sup> è…", "crescente, perché e &gt; 1", ["decrescente, perché e &lt; 1", "costante", "definita solo per x &gt; 0"]),
          ("Quanto vale e<sup>0</sup>?", "1", ["0", "e", "non esiste"])]
    q, a, w = R.choice(qs)
    return M(q, a, w, "%s <b>%s</b>." % (q.rstrip("?…"), a))


def main():
    seen = set()
    sets = [
        ("Potenze con esponente razionale", mix(R, seen, [(s1_raz, 20)])),
        ("Proprietà delle potenze", mix(R, seen, [(s1_prop, 12), (s1_raz, 8)])),
        ("La funzione esponenziale", mix(R, seen, [(s2_prop, 12), (s2_conf, 8)])),
        ("Grafici traslati", mix(R, seen, [(s3_trasl, 14), (s2_conf, 6)])),
        ("Crescita e decadimento", mix(R, seen, [(s4_cresc, 16), (s2_prop, 4)])),
    ]
    body = L(["Con base a &gt; 0 si definisce la potenza con esponente razionale: a<sup>m/n</sup> = <sup>n</sup>√(a<sup>m</sup>), e poi con esponente reale. Le proprietà delle potenze restano valide.",
              "La <b>funzione esponenziale</b> y = a<sup>x</sup> (a &gt; 0, a ≠ 1) ha dominio ℝ, valori sempre positivi (y &gt; 0), passa per (0; 1) e ha l’asintoto orizzontale y = 0.",
              "Se a &gt; 1 è crescente, se 0 &lt; a &lt; 1 è decrescente. La base più usata è il numero <b>e</b> ≈ 2,718.",
              "Le funzioni esponenziali descrivono la crescita a percentuale costante: N(t) = N<sub>0</sub> · 2<sup>t/T</sup> (raddoppio ogni T), m(t) = m<sub>0</sub> · (1/2)<sup>t/T</sup> (dimezzamento)."],
             [("8<sup>2/3</sup>", ["8 = 2³", "2<sup>3 · 2/3</sup> = 2²"], "4"),
              ("Asintoto di y = 2<sup>x</sup> − 3", ["Traslazione verso il basso di 3"], "y = −3")],
             [["8<sup>2/3</sup> = 16/3", "L’esponente frazionario indica una radice: ∛(8²) = 4."],
              ["2<sup>−3</sup> = −8", "Esponente negativo: 1/8, sempre positivo."],
              ["(1/2)<sup>x</sup> crescente", "Con base minore di 1 la funzione decresce."]])
    faq = [("Perché la base di una funzione esponenziale deve essere positiva?", "Con base negativa molte potenze non sono definite nei reali (per esempio (−2)<sup>1/2</sup> = √(−2)). Con a = 1 la funzione sarebbe costante."),
           ("Che cos’è il numero e?", "È il limite di (1 + 1/n)<sup>n</sup> per n che cresce: circa 2,718. È irrazionale ed è la base naturale delle esponenziali e dei logaritmi.")]
    unit(G, R, "funzione-esponenziale", "F",
         "Potenze a esponente reale; funzione esponenziale e suo grafico; modelli di crescita e decadimento",
         "Potenze a esponente reale e funzione esponenziale", "Funzione esponenziale",
         "Schede di matematica per la quarta liceo sulla funzione esponenziale: potenze con esponente razionale e reale, proprietà, grafico di y = aˣ, confronto di potenze, asintoti, il numero e, crescita e decadimento. 100 esercizi con soluzioni.",
         "aᵐ⸍ⁿ = ⁿ√(aᵐ)", "y = aˣ: crescente se a > 1, decrescente se 0 < a < 1, sempre positiva.",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
