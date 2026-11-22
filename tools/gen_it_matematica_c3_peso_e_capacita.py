# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Peso e capacità (Misure)
  python3 tools/gen_it_matematica_c3_peso_e_capacita.py
Il chilogrammo e il grammo (kg, hg, dag, g), il litro (l, dl, cl, ml), scegliere l’unità, equivalenze, confrontare,
leggere la bilancia a due piatti e il misurino, peso lordo, peso netto e tara, problemi.
Errori: 1 kg = 100 g, confrontare senza trasformare (800 g &gt; 2 kg), confondere peso e capacità, lordo = netto − tara.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, relabel, NB, table
import gen_fr_maths_ce2_masses_et_contenances as FRM

R = random.Random(70314)
K = Kids(R)


def U(v, u):
    return "%s%s%s" % (num(v), NB, u)


PESO = [("Un elefante pesa circa", 5000, "kg"), ("Un sacco di patate pesa", 10, "kg"), ("Una gomma pesa circa", 20, "g"), ("Un gatto pesa circa", 4, "kg"),
        ("Una piuma pesa circa", 1, "g"), ("Un panetto di burro pesa", 250, "g"), ("Un bambino di 8 anni pesa circa", 25, "kg"),
        ("Una mela pesa circa", 150, "g"), ("Un melone pesa circa", 1, "kg"), ("Una lettera pesa circa", 20, "g"), ("Una bicicletta pesa circa", 12, "kg"),
        ("Un pacco di pasta pesa", 500, "g"), ("Un cane grande pesa circa", 30, "kg"), ("Una fragola pesa circa", 15, "g")]
CAP = [("Una vasca da bagno contiene circa", 150, "l"), ("Un cucchiaio contiene circa", 15, "ml"), ("Un bicchiere d’acqua contiene circa", 20, "cl"),
       ("Un secchio contiene circa", 10, "l"), ("Una lattina contiene", 33, "cl"), ("Una bottiglia d’acqua contiene", 1, "l"), ("Una tazza contiene circa", 2, "dl"),
       ("Un acquario contiene circa", 60, "l"), ("Una tazzina da caffè contiene circa", 30, "ml"), ("Un annaffiatoio contiene circa", 8, "l"),
       ("Un cartone di latte contiene", 1, "l"), ("Un succo di frutta piccolo contiene", 20, "cl")]


def bilancia(obj, ws):
    s = FRM.balance_svg(obj, ws)
    return relabel(s, "bilancia a due piatti in equilibrio")


def misurino(level, top, step):
    s = FRM.verre(level, top, step).replace(" cL<", " ml<")
    return relabel(s, "misurino graduato in millilitri")


def s1_peso():
    o, v, u = R.choice(PESO)
    return mcq("Quale unità di misura è giusta? %s %s …" % (o, num(v)), u, [x for x in ["g", "kg", "hg", "l"] if x != u], "%s %s <b>%s</b>." % (o, num(v), u))


def s1_cap():
    o, v, u = R.choice(CAP)
    return mcq("Quale unità di misura è giusta? %s %s …" % (o, num(v)), u, [x for x in ["l", "dl", "cl", "ml", "kg"] if x != u], "%s %s <b>%s</b>." % (o, num(v), u))


def s2():
    k = R.choice(["kg_g", "kg_hg", "hg_g", "kgg", "g_kg", "l_cl", "l_dl", "dl_cl", "l_ml", "lcl", "cl_ml"])
    a = R.randint(2, 9)
    if k == "kg_g":
        return mcq("Completa l’equivalenza: %s = … g" % U(a, "kg"), num(a * 1000), [num(a * 100), num(a * 10), num(a + 1000)], "1 kg = 1000 g, quindi %d kg = <b>%s g</b>." % (a, num(a * 1000)))
    if k == "kg_hg":
        return mcq("Completa l’equivalenza: %s = … hg" % U(a, "kg"), num(a * 10), [num(a * 100), num(a * 1000), str(a)], "1 kg = 10 hg, quindi %d kg = <b>%s hg</b>." % (a, num(a * 10)))
    if k == "hg_g":
        return mcq("Completa l’equivalenza: %s = … g" % U(a, "hg"), num(a * 100), [num(a * 10), num(a * 1000), str(a)], "1 hg = 100 g, quindi %d hg = <b>%s g</b>." % (a, num(a * 100)))
    if k == "kgg":
        b = R.choice([50, 100, 200, 250, 300, 400, 500, 600, 750, 800, 900])
        return mcq("Completa l’equivalenza: %s %s = … g" % (U(a, "kg"), U(b, "g")), num(a * 1000 + b), [num(a * 100 + b), num(a + b), num(a * 1000 + b * 10)],
                   "%d kg = %s g; %s + %d = <b>%s g</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if k == "g_kg":
        return mcq("Completa l’equivalenza: %s = … kg" % U(a * 1000, "g"), str(a), [num(a * 10), num(a * 100), num(a * 1000)], "1000 g = 1 kg, quindi %s g = <b>%d kg</b>." % (num(a * 1000), a))
    if k == "l_cl":
        return mcq("Completa l’equivalenza: %s = … cl" % U(a, "l"), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)], "1 l = 100 cl, quindi %d l = <b>%s cl</b>." % (a, num(a * 100)))
    if k == "l_dl":
        return mcq("Completa l’equivalenza: %s = … dl" % U(a, "l"), num(a * 10), [num(a * 100), str(a), num(a * 1000)], "1 l = 10 dl, quindi %d l = <b>%s dl</b>." % (a, num(a * 10)))
    if k == "dl_cl":
        a = R.randint(2, 20)
        return mcq("Completa l’equivalenza: %s = … cl" % U(a, "dl"), num(a * 10), [num(a * 100), str(a), num(a + 10)], "1 dl = 10 cl, quindi %d dl = <b>%s cl</b>." % (a, num(a * 10)))
    if k == "l_ml":
        return mcq("Completa l’equivalenza: %s = … ml" % U(a, "l"), num(a * 1000), [num(a * 100), num(a * 10), num(a + 1000)], "1 l = 1000 ml, quindi %d l = <b>%s ml</b>." % (a, num(a * 1000)))
    if k == "cl_ml":
        a = R.randint(2, 50)
        return mcq("Completa l’equivalenza: %s = … ml" % U(a, "cl"), num(a * 10), [num(a * 100), str(a), num(a + 10)], "1 cl = 10 ml, quindi %d cl = <b>%s ml</b>." % (a, num(a * 10)))
    b = R.randint(5, 95)
    return mcq("Completa l’equivalenza: %s %s = … cl" % (U(a, "l"), U(b, "cl")), num(a * 100 + b), [num(a + b), num(a * 10 + b), num(a * 1000 + b)],
               "%d l = %d cl; %d + %d = <b>%s cl</b>." % (a, a * 100, a * 100, b, num(a * 100 + b)))


def s3():
    k = R.choice(["kgg", "lcl", "hgg", "lml"])
    if k == "kgg":
        a = R.randint(1, 5)
        x = a * 1000
        y = R.choice([a * 100, x + R.choice([-200, 200, 900]), x - 900, R.randint(2, 9) * 100])
        A, B = U(a, "kg"), U(y, "g")
    elif k == "hgg":
        a = R.randint(2, 9)
        x = a * 100
        y = x + R.choice([-50, -20, 30, 80])
        A, B = U(a, "hg"), U(y, "g")
    elif k == "lcl":
        a = R.randint(1, 4)
        x = a * 100
        y = R.choice([a * 10, x + R.choice([-25, 25, 50]), x - 67])
        A, B = U(a, "l"), U(y, "cl")
    else:
        a = R.randint(1, 3)
        x = a * 1000
        y = R.choice([a * 100, x + R.choice([-250, 250, 500])])
        A, B = U(a, "l"), U(y, "ml")
    if y == x or y <= 0:
        return None
    big = A if x > y else B
    small = B if big == A else A
    return mcq("Che cosa è di più: %s o %s?" % (A, B), big, [small, "sono uguali", "non si possono confrontare"],
               "Trasforma nella stessa unità prima di confrontare: <b>%s</b> è di più." % big)


def s4_bilancia():
    obj = R.choice(["pacco", "melone", "sacco", "zucca", "scatola"])
    pool = [1000, 500, 200, 100, 50, 20, 10]
    ws = sorted(R.sample(pool, R.randint(2, 3)), reverse=True)
    t = sum(ws)
    art = "la" if obj in ("zucca", "scatola") else "il"
    return mcq(bilancia(obj, ws) + "La bilancia è in equilibrio. Quanto pesa %s %s?" % (art, obj), U(t, "g"),
               [U(len(ws), "g"), U(t - ws[-1], "g"), U(t + ws[-1], "g"), U(max(ws), "g")],
               "Somma i pesi sul piatto: %s = <b>%s</b>." % (" + ".join("%s g" % num(w) for w in ws), U(t, "g")))


def s4_misurino():
    top, step = R.choice([(500, 50), (1000, 100), (400, 50), (600, 100)])
    lv = step * R.randint(1, top // step - 1)
    return mcq(misurino(lv, top, step) + "Quanta acqua c’è nel misurino?", "%d ml" % lv,
               ["%d ml" % (lv + step), "%d ml" % (lv - step) if lv > step else "%d ml" % (lv + 2 * step), "%d ml" % (lv // step), "%d l" % lv],
               "Ogni tacca piccola vale %d ml. L’acqua arriva a <b>%d ml</b>." % (step, lv))


def s5():
    p = K.next()
    k = R.choice(["netto", "lordo", "tara", "bottiglie", "spesa", "bicchieri"])
    if k == "netto":
        lo, ta = R.randint(4, 12) * 100 + R.choice([0, 50]), R.choice([50, 80, 100, 120, 150])
        return mcq("Un barattolo di miele ha un peso lordo di %s g. Il vasetto vuoto (la tara) pesa %d g. Qual è il peso netto?" % (num(lo), ta), U(lo - ta, "g"),
                   [U(lo + ta, "g"), U(lo - ta - 10, "g"), U(ta, "g")],
                   "Peso netto = peso lordo − tara: %s − %d = <b>%s g</b>." % (num(lo), ta, num(lo - ta)))
    if k == "lordo":
        ne, ta = R.choice([250, 500, 750, 1000]), R.choice([20, 30, 40, 50])
        return mcq("Un pacco di caffè contiene %s g di caffè (peso netto). La confezione pesa %d g. Qual è il peso lordo?" % (num(ne), ta), U(ne + ta, "g"),
                   [U(ne - ta, "g"), U(ne, "g"), U(ne + ta * 10, "g")],
                   "Peso lordo = peso netto + tara: %s + %d = <b>%s g</b>." % (num(ne), ta, num(ne + ta)))
    if k == "tara":
        ne = R.choice([300, 400, 500, 800])
        ta = R.choice([60, 70, 90, 120])
        return mcq("Una cassetta con le fragole pesa %s g. Le fragole pesano %d g. Quanto pesa la cassetta vuota (la tara)?" % (num(ne + ta), ne), U(ta, "g"),
                   [U(ne + ta + ne, "g") if ne * 2 + ta < 10000 else U(ta + 10, "g"), U(ne, "g"), U(ta + 100, "g")],
                   "Tara = peso lordo − peso netto: %s − %d = <b>%d g</b>." % (num(ne + ta), ne, ta))
    if k == "bottiglie":
        n, c = R.randint(3, 9), R.choice([2, 5])
        if R.random() < 0.5:
            return mcq("Una cassa contiene %d bottiglie da %d l. Quanti litri ci sono in tutto?" % (n, c), U(n * c, "l"), [U(n + c, "l"), U(n * c * 10, "l"), U(n * c + c, "l")],
                       "%d × %d = <b>%d l</b>." % (n, c, n * c))
        c = R.choice([25, 50])
        return mcq("%s riempie %d bicchieri da %d cl. Quanti centilitri versa?" % (p[0], n, c), U(n * c, "cl"), [U(n + c, "cl"), U(n * c * 10, "cl"), U(n * c - c, "cl")],
                   "%d × %d = <b>%d cl</b>." % (n, c, n * c))
    if k == "spesa":
        a, b = R.choice([500, 250, 750]), R.choice([200, 300, 500])
        r = 1000 * R.randint(1, 2) + a + b
        return mcq("La mamma di %s compra %d kg di patate, %d g di pane e %d g di formaggio. Quanto pesa la spesa in grammi?" % (p[0], (r - a - b) // 1000, a, b), U(r, "g"),
                   [U((r - a - b) // 1000 * 100 + a + b, "g"), U(a + b, "g"), U(r + 100, "g")],
                   "%d kg = %s g; %s + %d + %d = <b>%s g</b>." % ((r - a - b) // 1000, num(r - a - b), num(r - a - b), a, b, num(r)))
    b = R.choice([20, 25])
    n = R.randint(2, 4)
    if (100 * n) % b:
        return None
    return mcq("Una bottiglia contiene %d l di aranciata. Quanti bicchieri da %d cl si possono riempire?" % (n, b), str(100 * n // b),
               [str(n * b), str(100 * n // b + 1), str(10 * n // b) if 10 * n // b else str(n)],
               "%d l = %d cl; %d : %d = <b>%d</b> bicchieri." % (n, 100 * n, 100 * n, b, 100 * n // b))


def main():
    seen = set()
    sets = [
        ("Quale unità di misura?", mix(R, seen, [(s1_peso, 10), (s1_cap, 10)])),
        ("Equivalenze", mix(R, seen, [(s2, 20)])),
        ("Confrontare", mix(R, seen, [(s3, 20)])),
        ("Bilancia e misurino", mix(R, seen, [(s4_bilancia, 10), (s4_misurino, 10)])),
        ("Peso lordo, netto, tara e problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Il <b>peso</b> si misura in chilogrammi (kg) e grammi (g): 1 kg = 10 hg = 100 dag = 1000 g.",
         "La <b>capacità</b> (quanto liquido contiene un recipiente) si misura in litri (l): 1 l = 10 dl = 100 cl = 1000 ml.",
         "Per confrontare due misure trasformale nella stessa unità.",
         "<b>Peso lordo</b> = peso netto + tara. Il peso netto è la merce, la tara è la confezione."],
        [("2 kg 300 g = … g", ["2 kg = 2000 g", "2000 + 300 = 2300"], "2300 g"),
         ("Lordo 850 g, tara 50 g. Netto?", ["850 − 50 = 800"], "800 g")],
        [["1 kg = 100 g", "1 kg = 1000 g (e 1 hg = 100 g)."],
         ["Pensare che 800 g sia più di 2 kg", "2 kg = 2000 g, che è più di 800 g."],
         ["Calcolare il lordo togliendo la tara", "Il lordo è il peso più grande: netto + tara."]],
        table(["kg", "hg", "dag", "g"], [["1000 g", "100 g", "10 g", "1 g"]]) + table(["l", "dl", "cl", "ml"], [["1000 ml", "100 ml", "10 ml", "1 ml"]]))
    faq = [("Qual è la differenza tra peso lordo e peso netto?", "Il peso netto è solo la merce (per esempio il miele). Il peso lordo è la merce con la confezione. La tara è il peso della confezione."),
           ("Peso e capacità sono la stessa cosa?", "No: il peso dice quanto è pesante un oggetto (kg, g), la capacità dice quanto liquido entra in un recipiente (l, ml).")]
    make_unit(R, "peso-e-capacita", "M",
              "Misurare grandezze (peso e capacità) utilizzando unità arbitrarie e unità e strumenti convenzionali; conoscere il chilogrammo e il litro con multipli e sottomultipli; peso lordo, peso netto e tara",
              "Peso e capacità: chilogrammo, litro e peso netto", "Peso e capacità",
              "Schede di matematica per la classe terza su peso e capacità: chilogrammo e grammo, litro e millilitro, equivalenze, bilancia, misurino, peso lordo, netto e tara, problemi. 100 esercizi con soluzioni.",
              "1 kg = 1000 g e 1 l = 1000 ml.", "Peso lordo = peso netto + tara.",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
