# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Le misure (Misure)
  python3 tools/gen_it_matematica_c2_misure.py
Confrontare lunghezze, misurare con unità non convenzionali (quadretti, mattoncini, passi, spanne), il centimetro
e il metro, il righello, confrontare pesi con la bilancia a due piatti, capacità (quanti bicchieri), problemi.
Errori: misurare senza partire dallo 0, contare le tacche invece degli spazi, pensare che più grande = più pesante.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, relabel
import it_c2 as C
import k_pics
import gen_fr_maths_ce2_longueurs_et_perimetres as FRL

R = random.Random(70214)
G = "classe-seconda"
K = Kids(R)
L4 = "ABCD"


def s1_confronta():
    n = R.randint(3, 4)
    ls = R.sample(range(2, 10), n)
    pic = C.it(k_pics.pencils_svg(ls), "%d matite di lunghezza diversa, %s" % (n, ", ".join(L4[:n])))
    lungo = R.random() < 0.5
    t = ls.index(max(ls) if lungo else min(ls))
    return mcq(pic + "Quale matita è la più %s?" % ("lunga" if lungo else "corta"), L4[t], [L4[i] for i in range(n) if i != t] + ["sono uguali"],
               "Le matite partono dalla stessa linea: la più %s è la <b>%s</b>." % ("lunga" if lungo else "corta", L4[t]))


def s1_torri():
    hs = R.sample(range(2, 9), 3)
    pic = C.it(k_pics.towers_svg(hs), "3 torri di mattoncini A, B, C")
    i = R.randrange(3)
    return mcq(pic + "Quanti mattoncini è alta la torre %s?" % L4[i], str(hs[i]), [str(hs[i] + 1), str(hs[i] - 1), str(hs[(i + 1) % 3])],
               "Conta i mattoncini della torre %s: <b>%d</b>." % (L4[i], hs[i]))


def s2_non_conv():
    k = R.choice(["passi", "spanne", "matite"])
    if k == "passi":
        a, b = R.randint(8, 15), R.randint(10, 20)
        p1, p2 = K.two()
        return mcq("%s misura l’aula: %d passi. %s, che ha le gambe più corte, la misura: quanti passi farà?" % (p1[0], a, p2[0]), "più di %d" % a, ["meno di %d" % a, "esattamente %d" % a, "zero"],
                   "Con passi più corti ne servono di più: <b>più di %d</b>. Per questo servono unità uguali per tutti, come il metro." % a)
    if k == "spanne":
        n = R.randint(4, 9)
        return mcq("Il banco è lungo %d spanne di Luca. La maestra, che ha la mano più grande, misura con le sue spanne. Il numero sarà…" % n, "più piccolo", ["più grande", "uguale", "zero"],
                   "Con una spanna più lunga ne servono di meno: <b>più piccolo</b>.")
    a, b = R.randint(3, 8), R.randint(2, 4)
    return mcq("Un tavolo è lungo come %d matite. Ogni matita è lunga come %d gomme. Quante gomme è lungo il tavolo?" % (a, b), str(a * b), [str(a + b), str(a), str(a * b + 1)],
               "%d matite %s %d gomme = <b>%d</b> gomme." % (a, "×", b, a * b))


def s2_righello():
    a = R.choice([0, 0, 0, 10, 20])
    ln = R.randint(2, 12) * 10
    b = a + ln
    if b > 140:
        return None
    pic = relabel(FRL.regle(a, b), "righello in centimetri e un segmento rosso")
    return mcq(pic + "Quanto è lungo il segmento rosso?", "%d cm" % (ln // 10), ["%d cm" % (b // 10), "%d cm" % (ln // 10 + 1), "%d cm" % (ln // 10 - 1) if ln > 10 else "%d cm" % (ln // 10 + 2), "%d m" % (ln // 10)],
               "Il segmento va da %d a %d: %d − %d = <b>%d cm</b>." % (a // 10, b // 10, b // 10, a // 10, ln // 10))


UNI = [("La lunghezza di una gomma", "cm"), ("La lunghezza della lavagna", "m"), ("La lunghezza di una matita", "cm"), ("L’altezza della porta", "m"), ("La lunghezza di una formica", "cm"),
       ("La lunghezza del corridoio della scuola", "m"), ("La lunghezza di un quaderno", "cm"), ("La lunghezza di un campo da calcio", "m"), ("La larghezza di un francobollo", "cm"), ("L’altezza di un albero", "m")]


def s3_cm_m():
    k = R.choice(["uni", "uni", "conv", "confr"])
    if k == "uni":
        t, u = R.choice(UNI)
        return mcq("%s si misura meglio in…" % t, "metri (m)" if u == "m" else "centimetri (cm)", ["centimetri (cm)" if u == "m" else "metri (m)", "chili (kg)", "litri (l)"],
                   "%s si misura in <b>%s</b>." % (t, "metri" if u == "m" else "centimetri"))
    if k == "conv":
        a = R.randint(1, 5)
        return mcq("Quanti centimetri ci sono in %d %s?" % (a, "metro" if a == 1 else "metri"), "%d cm" % (a * 100), ["%d cm" % (a * 10), "%d cm" % a, "%d cm" % (a * 1000)], "1 m = 100 cm: <b>%d cm</b>." % (a * 100))
    a = R.randint(1, 2)
    b = a * 100 + R.choice([-30, -10, 20, 40])
    big = "%d m" % a if a * 100 > b else "%d cm" % b
    return mcq("Che cosa è più lungo: %d m o %d cm?" % (a, b), big, ["%d cm" % b if big.endswith(" m") else "%d m" % a, "sono uguali", "non si può dire"],
               "%d m = %d cm: è più lungo <b>%s</b>." % (a, a * 100, big))


def s4_peso():
    kinds = R.sample(["apple", "ball", "fish", "cup", "duck"], 2)
    tilt = R.choice(["left", "right", "equal"])
    a, b = R.randint(1, 3), R.randint(1, 3)
    pic = C.it(k_pics.balance_svg((kinds[0], a), (kinds[1], b), tilt), "bilancia a due piatti: %s a sinistra e %s a destra" % (C.cose(kinds[0], a), C.cose(kinds[1], b)))
    ans = {"left": "il piatto di sinistra", "right": "il piatto di destra", "equal": "pesano uguale"}[tilt]
    return mcq(pic + "Quale piatto è più pesante?", ans, [x for x in ("il piatto di sinistra", "il piatto di destra", "pesano uguale") if x != ans] + ["quello con più oggetti"],
               "Il piatto più pesante va giù. %s" % ("Sono in equilibrio: <b>pesano uguale</b>." if tilt == "equal" else "Va giù <b>%s</b>." % ans))


CAP = [("una piscina", "una vasca da bagno", "un secchio", "una tazza"), ("un secchio", "una bottiglia", "un bicchiere", "un cucchiaio"), ("una vasca da bagno", "un secchio", "una bottiglia", "un bicchiere")]


def s4_capacita():
    k = R.choice(["ordine", "bicchieri"])
    if k == "ordine":
        c = list(R.choice(CAP))
        big = R.random() < 0.5
        ans = c[0] if big else c[-1]
        sh = c[:]
        R.shuffle(sh)
        return mcq("Quale contiene %s acqua: %s?" % ("più" if big else "meno", ", ".join(sh)), ans, [x for x in c if x != ans], "Contiene %s acqua <b>%s</b>." % ("più" if big else "meno", ans))
    a, b = R.randint(3, 9), R.randint(2, 4)
    return mcq("Una bottiglia riempie %d bicchieri. Quanti bicchieri si riempiono con %d bottiglie uguali?" % (a, b), str(a * b), [str(a + b), str(a), str(a * b + 1)], "%d %s %d = <b>%d</b> bicchieri." % (a, "×", b, a * b))


def s5():
    p = K.next()
    k = R.choice(["nastro", "salto", "piante", "corsa", "bilancia"])
    if k == "nastro":
        a, b = R.randint(30, 90), R.randint(5, 25)
        return mcq("%s ha un nastro di %d cm. Ne taglia %d cm. Quanti cm restano?" % (p[0], a, b), "%d cm" % (a - b), ["%d cm" % (a + b), "%d cm" % (a - b + 10), "%d m" % (a - b)], "%d − %d = <b>%d cm</b>." % (a, b, a - b))
    if k == "salto":
        a, b = R.randint(80, 150), R.randint(5, 30)
        return mcq("%s salta %d cm, la sua amica %d cm in più. Quanto salta l’amica?" % (p[0], a, b), "%d cm" % (a + b), ["%d cm" % (a - b), "%d cm" % (a + b + 10), "%d cm" % b], "%d + %d = <b>%d cm</b>." % (a, b, a + b))
    if k == "piante":
        a, b = R.randint(10, 40), R.randint(5, 20)
        return mcq("Una piantina è alta %d cm. In un mese cresce di %d cm. Quanto è alta ora?" % (a, b), "%d cm" % (a + b), ["%d cm" % (a - b), "%d cm" % b, "%d cm" % (a + b + 1)], "%d + %d = <b>%d cm</b>." % (a, b, a + b))
    if k == "corsa":
        n = R.randint(2, 6)
        return mcq("Il giro del cortile è lungo 20 m. %s fa %d giri. Quanti metri corre?" % (p[0], n), "%d m" % (20 * n), ["%d m" % (20 + n), "%d m" % (20 * n + 20), "%d cm" % (20 * n)], "20 %s %d = <b>%d m</b>." % ("×", n, 20 * n))
    a, b = R.randint(2, 6), R.randint(2, 6)
    if a == b:
        return None
    return mcq("Su una bilancia, una scatola pesa come %d mele. Un’altra scatola pesa come %d mele. Quale scatola è più pesante?" % (a, b), "la prima" if a > b else "la seconda",
               ["la seconda" if a > b else "la prima", "pesano uguale", "non si può dire"], "%d mele pesano più di %d: è più pesante <b>%s</b>." % (max(a, b), min(a, b), "la prima" if a > b else "la seconda"))


def main():
    FRL.R = R
    seen = set()
    sets = [
        ("Più lungo, più corto", mix(R, seen, [(s1_confronta, 12), (s1_torri, 8)])),
        ("Misurare con passi, spanne e oggetti", mix(R, seen, [(s2_non_conv, 8), (s2_righello, 12)])),
        ("Centimetri e metri", mix(R, seen, [(s3_cm_m, 20)])),
        ("Peso e capacità", mix(R, seen, [(s4_peso, 12), (s4_capacita, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Per confrontare due lunghezze mettile una accanto all’altra, partendo dalla stessa linea.",
         "Si può misurare con passi, spanne o mattoncini, ma ognuno ha passi diversi: per questo si usano il <b>centimetro</b> (cm) e il <b>metro</b> (m). 1 m = 100 cm.",
         "Con il righello parti sempre dallo <b>0</b>.",
         "Sulla bilancia a due piatti il piatto più pesante va giù."],
        [("Un segmento va dallo 0 al 7 del righello.", ["conto gli spazi tra 0 e 7"], "7 cm")],
        [["Misurare partendo dall’1", "Lo 0 deve stare all’inizio dell’oggetto."],
         ["Contare le tacche invece degli spazi", "Conta i centimetri, cioè gli spazi tra le tacche."],
         ["Pensare che più grande = più pesante", "Un pallone grande può pesare meno di una piccola pietra: usa la bilancia."]])
    faq = [("Perché si misura prima con passi e spanne?", "Per capire che serve un’unità uguale per tutti: con i passi ognuno trova un numero diverso."),
           ("Quando si usa il metro e quando il centimetro?", "Il metro per le cose grandi (aula, corridoio), il centimetro per le cose piccole (matita, quaderno).")]
    make_unit(R, "misure", "M",
              "Misurare grandezze (lunghezze, tempo, ecc.) utilizzando sia unità arbitrarie sia unità e strumenti convenzionali (metro, righello); confrontare pesi e capacità",
              "Le misure: lunghezza, peso e capacità", "Misure",
              "Schede di matematica per la classe seconda sulle misure: più lungo e più corto, passi e spanne, righello, centimetri e metri, bilancia, capacità e problemi. 100 esercizi con soluzioni.",
              "Con il righello parti dallo 0.", "1 metro = 100 centimetri.",
              body, faq, sets, 14, grade=G)


if __name__ == "__main__":
    main()
