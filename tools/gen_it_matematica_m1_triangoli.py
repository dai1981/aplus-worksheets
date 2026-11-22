# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: I triangoli (Spazio e figure)
  python3 tools/gen_it_matematica_m1_triangoli.py
Classificazione rispetto ai lati e agli angoli, somma degli angoli interni, angolo esterno, disuguaglianza triangolare,
altezze, mediane, bisettrici, assi e punti notevoli (ortocentro, baricentro, incentro, circocentro), criteri di congruenza.
Errori: pensare che l’angolo esterno sia supplementare a tutti gli interni, confondere mediana e altezza, credere che il baricentro sia sempre il punto medio.
"""
import random
from it_media import M, L, unit, mix, table, W
import gen_it_matematica_c4_triangoli as T4

R = random.Random(71113)
G = "prima-media"


def s3_esterno():
    a, b = R.randint(25, 85), R.randint(25, 85)
    c = 180 - a - b
    if c < 15:
        return None
    k = R.random()
    if k < 0.5:
        return M("In un triangolo due angoli interni misurano %d° e %d°. Quanto misura l’angolo esterno adiacente al terzo angolo?" % (a, b), "%d°" % (a + b), W("%d°" % c, "%d°" % (180 - a), "%d°" % (360 - a - b)),
                 "L’angolo esterno è uguale alla somma dei due interni non adiacenti: %d° + %d° = <b>%d°</b> (oppure 180° − %d°)." % (a, b, a + b, c))
    e = a + b
    return M("Un angolo esterno di un triangolo misura %d°; uno dei due angoli interni non adiacenti misura %d°. Quanto misura l’altro?" % (e, a), "%d°" % b, W("%d°" % (180 - e), "%d°" % (e + a), "%d°" % (180 - a)),
             "%d° − %d° = <b>%d°</b>." % (e, a, b))


NOTEV = [("Il punto in cui si incontrano le tre altezze si chiama…", "ortocentro", ["baricentro", "incentro", "circocentro"]),
         ("Il punto in cui si incontrano le tre mediane si chiama…", "baricentro", ["ortocentro", "incentro", "circocentro"]),
         ("Il punto in cui si incontrano le tre bisettrici si chiama…", "incentro", ["baricentro", "ortocentro", "circocentro"]),
         ("Il punto in cui si incontrano i tre assi dei lati si chiama…", "circocentro", ["incentro", "baricentro", "ortocentro"]),
         ("Il segmento che unisce un vertice al punto medio del lato opposto è…", "la mediana", ["l’altezza", "la bisettrice", "l’asse"]),
         ("Il segmento che parte da un vertice ed è perpendicolare al lato opposto è…", "l’altezza", ["la mediana", "la bisettrice", "l’asse"]),
         ("Il centro della circonferenza inscritta in un triangolo è…", "l’incentro", ["il baricentro", "l’ortocentro", "il circocentro"]),
         ("Il centro della circonferenza circoscritta a un triangolo è…", "il circocentro", ["l’incentro", "il baricentro", "l’ortocentro"]),
         ("In un triangolo rettangolo l’ortocentro coincide con…", "il vertice dell’angolo retto", ["il punto medio dell’ipotenusa", "il baricentro", "un punto esterno"]),
         ("In un triangolo ottusangolo l’ortocentro è…", "esterno al triangolo", ["interno al triangolo", "su un lato", "nel baricentro"]),
         ("Il baricentro divide ogni mediana in due parti di cui una è…", "il doppio dell’altra", ["uguale all’altra", "il triplo dell’altra", "la metà del lato"]),
         ("In un triangolo equilatero i quattro punti notevoli…", "coincidono", ["sono sempre esterni", "sono sui lati", "formano un quadrato"]),
         ("Quale punto notevole è sempre interno al triangolo?", "il baricentro", ["l’ortocentro", "il circocentro", "nessuno"]),
         ("Nel triangolo rettangolo il circocentro è…", "il punto medio dell’ipotenusa", ["il vertice dell’angolo retto", "il baricentro", "esterno al triangolo"])]


def s4_notevoli():
    q, a, w = R.choice(NOTEV)
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


CRIT = [("Due triangoli hanno congruenti due lati e l’angolo compreso tra essi. Sono congruenti?", "sì, per il 1° criterio", ["no, serve anche il terzo lato", "solo se sono rettangoli", "sì, per il 3° criterio"]),
        ("Due triangoli hanno congruenti un lato e i due angoli adiacenti a esso. Sono congruenti?", "sì, per il 2° criterio", ["no, servono tre lati", "solo se sono isosceli", "sì, per il 1° criterio"]),
        ("Due triangoli hanno i tre lati rispettivamente congruenti. Sono congruenti?", "sì, per il 3° criterio", ["no, servono anche gli angoli", "solo se sono equilateri", "sì, per il 2° criterio"]),
        ("Due triangoli hanno i tre angoli rispettivamente congruenti. Sono per forza congruenti?", "no, possono avere grandezze diverse", ["sì, sempre", "sì, per il 3° criterio", "solo se sono rettangoli"]),
        ("Che cosa vuol dire che due figure sono congruenti?", "si possono sovrapporre esattamente con un movimento rigido", ["hanno lo stesso perimetro", "hanno la stessa forma ma grandezze diverse", "hanno la stessa area"])]


def s4_crit():
    q, a, w = R.choice(CRIT)
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s5():
    k = R.choice(["perim", "iso", "eq", "rapp"])
    if k == "perim":
        a = R.randint(5, 25)
        b = a + R.randint(2, 10)
        c = R.randint(abs(b - a) + 1, a + b - 1)
        return M("In un triangolo il lato AB misura %d cm, BC supera AB di %d cm e CA misura %d cm. Qual è il perimetro?" % (a, b - a, c), "%d cm" % (a + b + c), W("%d cm" % (a + (b - a) + c), "%d cm" % (2 * a + c), "%d cm" % (a + b + c + 1)),
                 "BC = %d + %d = %d cm; perimetro = %d + %d + %d = <b>%d cm</b>." % (a, b - a, b, a, b, c, a + b + c))
    if k == "iso":
        x = R.randint(6, 30)
        y = R.randint(4, 2 * x - 1)
        p = 2 * x + y
        return M("Un triangolo isoscele ha il perimetro di %d cm e la base di %d cm. Quanto misura ciascun lato obliquo?" % (p, y), "%d cm" % x, W("%d cm" % (p - y), "%d cm" % (p // 3), "%d cm" % ((p + y) // 2)),
                 "(%d − %d) : 2 = <b>%d cm</b>." % (p, y, x))
    if k == "eq":
        a = R.randint(40, 80)
        return M("In un triangolo isoscele l’angolo al vertice è %d°. Quanto misura un angolo esterno adiacente a un angolo alla base?" % a, "%d°" % (180 - (180 - a) // 2), W("%d°" % ((180 - a) // 2), "%d°" % (180 - a), "%d°" % (180 + a)),
                 "Angolo alla base: (180° − %d°) : 2 = %d°; angolo esterno: 180° − %d° = <b>%d°</b>." % (a, (180 - a) // 2, (180 - a) // 2, 180 - (180 - a) // 2)) if (180 - a) % 2 == 0 else None
    m, n, o = R.choice([(1, 2, 3), (2, 3, 4), (1, 1, 2), (3, 4, 5), (1, 3, 5), (2, 2, 5)])
    k_ = 180 // (m + n + o)
    if 180 % (m + n + o):
        return None
    return M("Gli angoli di un triangolo sono proporzionali a %d, %d e %d (cioè sono %d, %d e %d parti uguali). Quanto misura l’angolo maggiore?" % (m, n, o, m, n, o), "%d°" % (o * k_), W("%d°" % (o * 10), "%d°" % (m * k_), "%d°" % (180 // 3)),
             "Parti in tutto: %d; una parte = 180° : %d = %d°; maggiore = %d × %d° = <b>%d°</b>." % (m + n + o, m + n + o, k_, o, k_, o * k_))


def main():
    T4.R = R
    seen = set()
    sets = [
        ("Classificare i triangoli", mix(R, seen, [(T4.s1_lati, 10), (T4.s2_angoli, 10)])),
        ("Somma degli angoli e angolo esterno", mix(R, seen, [(T4.s3_terzo, 8), (T4.s3_speciali, 4), (s3_esterno, 8)])),
        ("Disuguaglianza triangolare e criteri", mix(R, seen, [(T4.s4_esiste, 14), (s4_crit, 5), (T4.s4_quiz, 1)])),
        ("Altezze, mediane, bisettrici, punti notevoli", mix(R, seen, [(s4_notevoli, 14), (T4.s4_quiz, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["Rispetto ai lati un triangolo è <b>equilatero</b>, <b>isoscele</b> o <b>scaleno</b>; rispetto agli angoli è <b>acutangolo</b>, <b>rettangolo</b> o <b>ottusangolo</b>.",
              "La somma degli angoli interni è <b>180°</b>. Ogni <b>angolo esterno</b> è uguale alla somma dei due angoli interni non adiacenti.",
              "<b>Disuguaglianza triangolare</b>: ogni lato è minore della somma degli altri due.",
              "Le tre <b>altezze</b> si incontrano nell’ortocentro, le tre <b>mediane</b> nel baricentro, le tre <b>bisettrici</b> nell’incentro, i tre <b>assi</b> nel circocentro.",
              "<b>Criteri di congruenza</b>: due lati e l’angolo compreso (1°), un lato e i due angoli adiacenti (2°), tre lati (3°)."],
             [("Angoli interni: 50° e 70°", ["terzo angolo: 180° − 120° = 60°", "esterno vicino al terzo: 50° + 70° = 120°"], "60° e 120°")],
             [["Pensare che tre angoli congruenti bastino per la congruenza", "Con gli stessi angoli i triangoli possono essere grandi o piccoli."],
              ["Confondere mediana e altezza", "La mediana va al punto medio, l’altezza è perpendicolare."],
              ["Credere che l’ortocentro sia sempre interno", "Nell’ottusangolo è esterno, nel rettangolo è nel vertice dell’angolo retto."]],
             table(["Segmenti / rette", "Si incontrano in"], [["altezze", "ortocentro"], ["mediane", "baricentro"], ["bisettrici", "incentro"], ["assi dei lati", "circocentro"]]))
    faq = [("Perché la somma degli angoli è sempre 180°?", "Tracciando dal vertice la parallela al lato opposto si formano angoli alterni interni congruenti: i tre angoli del triangolo formano un angolo piatto."),
           ("A che cosa serve la disuguaglianza triangolare?", "A capire se con tre segmenti dati si può costruire un triangolo: con 3, 4 e 9 cm no, perché 9 > 3 + 4.")]
    unit(G, R, "triangoli", "S",
         "Conoscere definizioni e proprietà significative dei triangoli (angoli, disuguaglianza triangolare, punti notevoli); riconoscere triangoli congruenti",
         "I triangoli: angoli, punti notevoli e congruenza", "Triangoli",
         "Schede di matematica per la prima media sui triangoli: classificazione, somma degli angoli, angolo esterno, disuguaglianza triangolare, altezze, mediane, bisettrici, punti notevoli, criteri di congruenza e problemi. 100 esercizi con soluzioni.",
         "Somma degli angoli interni: 180°.", "Angolo esterno = somma dei due interni non adiacenti.",
         body, faq, sets, 13)


if __name__ == "__main__":
    main()
