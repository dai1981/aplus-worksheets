# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Goniometria — angoli, radianti e funzioni goniometriche (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l4_goniometria.py
Misura in gradi e in radianti, lunghezza dell’arco, circonferenza goniometrica, seno, coseno e tangente degli angoli notevoli,
segno nei quadranti, relazione fondamentale sen²α + cos²α = 1, tg α = sen α / cos α, archi associati, periodo delle funzioni.
Errori: π = 180 come numero, segno del coseno nel II quadrante, tg 90° = 0, sen(π − α) = −sen α.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, FR, pif

R = random.Random(72404)
G = "quarta-liceo"
NOT = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
R3 = "√3"


def ex_val(fn, deg):
    """valore esatto come (testo, float)"""
    v = {"sen": math.sin, "cos": math.cos, "tg": math.tan}[fn](math.radians(deg))
    if fn == "tg" and deg % 180 == 90:
        return "non esiste", None
    table_ = [(0, "0"), (1, "1"), (-1, "−1"), (0.5, FR(1, 2)), (-0.5, "−" + FR(1, 2)), (math.sqrt(2) / 2, FR("√2", 2)), (-math.sqrt(2) / 2, "−" + FR("√2", 2)),
              (math.sqrt(3) / 2, FR(R3, 2)), (-math.sqrt(3) / 2, "−" + FR(R3, 2)), (math.sqrt(3), R3), (-math.sqrt(3), "−" + R3), (math.sqrt(3) / 3, FR(R3, 3)), (-math.sqrt(3) / 3, "−" + FR(R3, 3))]
    for val, t in table_:
        if abs(v - val) < 1e-9:
            return t, val
    raise ValueError


def sen_txt(fn):
    return fn


def s1_rad():
    deg = R.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 18, 36, 72, 15, 75, 20, 40])
    t = Fr(deg, 180)
    if R.random() < 0.5:
        return M("Converti %d° in radianti." % deg, pif(t), [pif(x) for x in W(Fr(180, deg), t * 2, t / 2, Fr(deg, 360) if Fr(deg, 360) != t / 2 else t + 1) if x != t],
                 "α<sub>rad</sub> = α° · π / 180° = %d · π / 180 = <b>%s</b>." % (deg, pif(t)))
    return M("Converti %s rad in gradi." % pif(t), "%d°" % deg, ["%s°" % d(x) for x in W(Fr(deg, 2), deg * 2, 180 - deg if deg < 180 else deg - 180, Fr(deg * 3, 2)) if x != deg],
             "α° = α<sub>rad</sub> · 180° / π = <b>%d°</b>." % deg)


def s1_arco():
    r = R.randint(2, 12)
    t = R.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(5, 6), Fr(1), Fr(3, 2)])
    l = r * t
    return M("Quanto è lungo l’arco di una circonferenza di raggio %d cm che corrisponde a un angolo al centro di %s rad?" % (r, pif(t)), "%s cm" % pif(l), ["%s cm" % pif(x) for x in W(l * 2, t, r * t / 2, l * 180 if False else r * r * t / 2) if x != l],
             "l = r · α = %d · %s = <b>%s cm</b>." % (r, pif(t), pif(l)))


def s2_val():
    fn = R.choice(["sen", "cos", "tg"])
    deg = R.choice(NOT)
    a, v = ex_val(fn, deg)
    opts = set()
    for other in ("sen", "cos", "tg"):
        try:
            opts.add(ex_val(other, deg)[0])
        except ValueError:
            pass
    pool = ["0", "1", "−1", FR(1, 2), "−" + FR(1, 2), FR("√2", 2), FR(R3, 2), "−" + FR(R3, 2), R3, FR(R3, 3), "non esiste"]
    if a.startswith("−"):
        opts.add(a[1:])
    else:
        opts.add("−" + a if a not in ("0", "non esiste") else "1")
    w = [x for x in sorted(opts) + pool if x != a]
    R.shuffle(w)
    q = "Quanto vale %s %d°?" % (fn, deg) if R.random() < 0.6 else "Quanto vale %s %s?" % (fn, pif(Fr(deg, 180)))
    return M(q, a, w[:6], "Dalla circonferenza goniometrica (angolo di riferimento e segno del quadrante): %s %d° = <b>%s</b>." % (fn, deg, a))


def quadr(deg):
    return 1 + (deg % 360) // 90


def s2_segno():
    deg = R.choice([x for x in range(10, 360, 5) if x % 90])
    fn = R.choice(["sen", "cos", "tg"])
    v = {"sen": math.sin, "cos": math.cos, "tg": math.tan}[fn](math.radians(deg))
    ans = "positivo" if v > 0 else "negativo"
    q = quadr(deg)
    return M("Un angolo di %d° si trova nel %s quadrante. Che segno ha %s %d°?" % (deg, ["primo", "secondo", "terzo", "quarto"][q - 1], fn, deg), ans, ["negativo" if v > 0 else "positivo", "nullo", "dipende dal raggio"],
             "Nel %s quadrante: sen %s, cos %s, tg %s. Quindi <b>%s</b>." % (["I", "II", "III", "IV"][q - 1], "+" if q in (1, 2) else "−", "+" if q in (1, 4) else "−", "+" if q in (1, 3) else "−", ans))


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]


def s3_fond():
    a, b, c = R.choice(TRIPLES)
    if R.random() < 0.5:
        a, b = b, a
    q = R.randint(1, 4)
    sgn_s = 1 if q in (1, 2) else -1
    sgn_c = 1 if q in (1, 4) else -1
    s, co = Fr(a * sgn_s, c), Fr(b * sgn_c, c)
    k = R.choice(["cos", "tg"])
    qn = ["primo", "secondo", "terzo", "quarto"][q - 1]
    if k == "cos":
        return M("Sapendo che sen α = %s e che α è nel %s quadrante, calcola cos α." % (fq(s), qn), fq(co), [fq(x) for x in W(-co, Fr(a, c) if Fr(a, c) != abs(s) else s, 1 - abs(s), Fr(c, b)) if x != co],
                 "cos²α = 1 − sen²α = 1 − %s = %s; nel %s quadrante il coseno è %s: <b>%s</b>." % (fq(s * s), fq(co * co), qn, "positivo" if sgn_c > 0 else "negativo", fq(co)))
    t = s / co
    return M("Sapendo che cos α = %s e che α è nel %s quadrante, calcola tg α." % (fq(co), qn), fq(t), [fq(x) for x in W(-t, 1 / t, s, co / s) if x != t],
             "sen α = %s (segno del %s quadrante), tg α = sen α / cos α = <b>%s</b>." % (fq(s), qn, fq(t)))


ASS = [("sen(π − α)", "sen α"), ("cos(π − α)", "−cos α"), ("sen(π + α)", "−sen α"), ("cos(π + α)", "−cos α"), ("sen(−α)", "−sen α"), ("cos(−α)", "cos α"),
       ("sen(π/2 − α)", "cos α"), ("cos(π/2 − α)", "sen α"), ("tg(π − α)", "−tg α"), ("tg(π + α)", "tg α"), ("sen(2π − α)", "−sen α"), ("cos(2π − α)", "cos α"),
       ("sen(π/2 + α)", "cos α"), ("cos(π/2 + α)", "−sen α"), ("tg(−α)", "−tg α")]


def s4_ass():
    f, a = R.choice(ASS)
    pool = ["sen α", "−sen α", "cos α", "−cos α", "tg α", "−tg α"]
    w = [x for x in pool if x != a]
    R.shuffle(w)
    return M("Semplifica con gli archi associati: %s" % f, a, w[:3], "Disegna α e l’angolo associato sulla circonferenza goniometrica: %s = <b>%s</b>." % (f, a))


def s4_rid():
    deg = R.choice([x for x in NOT if x > 90] + [390, 405, 420, 480, 510, 570, 600, 690, 720 + 45])
    fn = R.choice(["sen", "cos"])
    a, _ = ex_val(fn, deg)
    ref = deg % 360
    pool = ["0", "1", "−1", FR(1, 2), "−" + FR(1, 2), FR("√2", 2), "−" + FR("√2", 2), FR(R3, 2), "−" + FR(R3, 2)]
    w = [x for x in pool if x != a]
    R.shuffle(w)
    if a.startswith("−") and a[1:] in w:
        w.remove(a[1:])
        w.insert(0, a[1:])
    elif not a.startswith("−") and "−" + a in w:
        w.remove("−" + a)
        w.insert(0, "−" + a)
    return M("Calcola %s %d°." % (fn, deg), a, w[:3], "%s%s %d° → angolo di riferimento e segno del quadrante: <b>%s</b>." % ("%d° = %d° + 360°·%d; " % (deg, ref, deg // 360) if deg >= 360 else "", fn, ref, a))


def s5_per():
    k = R.choice([2, 3, 4, Fr(1, 2), 6])
    fn = R.choice(["sen", "cos", "tg"])
    base = Fr(2) if fn != "tg" else Fr(1)
    T = base / k
    ks = fq(k) if Fr(k).denominator == 1 else "(%s)" % fq(k)
    ks = ks.replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", "")
    return M("Qual è il periodo della funzione y = %s(%sx)?" % (fn, ks), pif(T), [pif(x) for x in W(base * k, base, T * 2 if fn != "tg" else Fr(2) / k) if x != T],
             "Il periodo di %s x è %s; con %sx diventa %s : %s = <b>%s</b>." % (fn, pif(base), ks, pif(base), fq(k), pif(T)))


def main():
    seen = set()
    sets = [
        ("Gradi e radianti", mix(R, seen, [(s1_rad, 14), (s1_arco, 6)])),
        ("Valori degli angoli notevoli", mix(R, seen, [(s2_val, 20)])),
        ("Segni e relazione fondamentale", mix(R, seen, [(s2_segno, 8), (s3_fond, 12)])),
        ("Archi associati", mix(R, seen, [(s4_ass, 12), (s4_rid, 8)])),
        ("Angoli qualsiasi e periodo", mix(R, seen, [(s4_rid, 12), (s5_per, 8)])),
    ]
    body = L(["Un angolo si misura in gradi o in <b>radianti</b>: 180° = π rad. Un radiante è l’angolo che stacca un arco lungo quanto il raggio; l’arco è l = r · α.",
              "Sulla <b>circonferenza goniometrica</b> (raggio 1, centro O) il punto P associato ad α ha coordinate (cos α; sen α). Inoltre tg α = sen α / cos α.",
              "<b>Relazione fondamentale</b>: sen²α + cos²α = 1. Segni: I quadrante tutti positivi; II solo il seno; III solo la tangente; IV solo il coseno.",
              "Gli <b>archi associati</b> (π − α, π + α, −α, π/2 − α …) riportano ogni angolo al primo quadrante. sen e cos hanno periodo 2π, tg ha periodo π."],
             [("sen α = 3/5, α nel II quadrante", ["cos²α = 1 − 9/25 = 16/25", "Nel II quadrante cos &lt; 0"], "cos α = −4/5"),
              ("cos 150°", ["150° = 180° − 30°", "cos(180° − α) = −cos α"], "−√3/2")],
             [["Scrivere π = 180", "π è un numero (≈ 3,14): si scrive 180° = π rad."],
              ["Coseno positivo nel II quadrante", "Nel II quadrante l’ascissa è negativa: cos α &lt; 0."],
              ["tg 90° = 0", "cos 90° = 0: la tangente non esiste."]],
             table(["α", "0", "π/6", "π/4", "π/3", "π/2"], [["sen α", "0", "1/2", "√2/2", "√3/2", "1"], ["cos α", "1", "√3/2", "√2/2", "1/2", "0"], ["tg α", "0", "√3/3", "1", "√3", "non esiste"]]))
    faq = [("Perché si usano i radianti?", "Perché sono il rapporto tra arco e raggio, quindi un numero puro: le formule dell’analisi (derivate, limiti) e della lunghezza dell’arco diventano semplici."),
           ("Come si ricordano i segni nei quadranti?", "Basta ricordare che cos α è l’ascissa e sen α l’ordinata del punto sulla circonferenza goniometrica; la tangente è positiva dove seno e coseno hanno lo stesso segno.")]
    unit(G, R, "goniometria", "F",
         "Le funzioni circolari: misura degli angoli in radianti, seno, coseno e tangente, relazioni fondamentali, archi associati, periodicità",
         "Goniometria: angoli, radianti e funzioni goniometriche", "Goniometria",
         "Schede di matematica per la quarta liceo sulla goniometria: gradi e radianti, lunghezza dell’arco, seno, coseno e tangente degli angoli notevoli, segni nei quadranti, relazione fondamentale, archi associati, periodo. 100 esercizi con soluzioni.",
         "sen²α + cos²α = 1", "180° = π rad; tg α = sen α / cos α.",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
