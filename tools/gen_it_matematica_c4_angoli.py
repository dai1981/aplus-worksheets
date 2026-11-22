# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Gli angoli (Spazio e figure)
  python3 tools/gen_it_matematica_c4_angoli.py
Angolo come rotazione, angoli retto, acuto, ottuso, piatto, giro; il grado; misurare con il goniometro
(scala interna ed esterna); stimare; angoli complementari, supplementari ed esplementari; lancette dell’orologio.
Errori: leggere la scala sbagliata del goniometro (180° − x), pensare che l’angolo dipenda dalla lunghezza dei lati.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, relabel, fig
import gen_it_matematica_c3_linee_e_angoli as A3
import gen_au_maths_y5_angles as AU

R = random.Random(70414)
G = "classe-quarta"


def gradi(v):
    return "%d°" % v


def tipo(d):
    return "retto" if d == 90 else "acuto" if d < 90 else "ottuso" if d < 180 else "piatto" if d == 180 else "concavo" if d < 360 else "giro"


def s1_tipo():
    if R.random() < 0.5:
        return A3.s3_angoli()
    d = R.choice(list(range(10, 90, 5)) + list(range(95, 180, 5)) + [90, 180, 360])
    t = tipo(d)
    others = [x for x in ("acuto", "retto", "ottuso", "piatto", "giro") if x != t]
    return mcq("Un angolo misura %s. Come si chiama?" % gradi(d), "angolo " + t, ["angolo " + x for x in others],
               "Acuto: meno di 90°; retto: 90°; ottuso: tra 90° e 180°; piatto: 180°; giro: 360°. %s è un <b>angolo %s</b>." % (gradi(d), t))


def s1_quanti():
    q, a, w = R.choice([("Quanti gradi misura un angolo retto?", "90°", ["180°", "45°", "100°"]), ("Quanti gradi misura un angolo piatto?", "180°", ["90°", "360°", "100°"]),
                        ("Quanti gradi misura un angolo giro?", "360°", ["180°", "100°", "400°"]), ("Quanti gradi misura mezzo angolo retto?", "45°", ["90°", "30°", "50°"]),
                        ("Un quarto di giro misura…", "90°", ["45°", "180°", "25°"]), ("Tre quarti di giro misurano…", "270°", ["180°", "300°", "75°"]),
                        ("Quanti angoli retti formano un angolo giro?", "4", ["2", "3", "360"]), ("Con quale strumento si misurano gli angoli?", "il goniometro", ["il compasso", "il righello", "la bilancia"]),
                        ("Come si chiama il punto in cui si incontrano i lati di un angolo?", "vertice", ["lato", "centro", "spigolo"]),
                        ("Se allunghi i lati di un angolo di 40°, quanto misura l’angolo?", "40°", ["80°", "più di 40°", "meno di 40°"])])
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def scale_cands(v):
    return [gradi(180 - v), gradi(v + 10), gradi(v - 10), gradi(v + 5)]


def s2_goniometro():
    v = R.choice(list(range(20, 165, 5)))
    if v == 90:
        return None
    if R.random() < 0.5:
        pic = AU.protractor_svg([0, v], "goniometro che misura un angolo")
        e = "Un lato è sullo 0 a destra: leggi la scala <b>interna</b>, che parte da 0 a destra. L’altro lato passa su %d. L’angolo è %s, quindi misura <b>%s</b>." % (v, tipo(v), gradi(v))
    else:
        pic = AU.protractor_svg([180, 180 - v], "goniometro che misura un angolo")
        e = "Un lato è sullo 0 a sinistra: leggi la scala <b>esterna</b>, che parte da 0 a sinistra. L’altro lato passa su %d. L’angolo è %s, quindi misura <b>%s</b>." % (v, tipo(v), gradi(v))
    pic = relabel(pic, "goniometro che misura un angolo")
    return mcq(fig(pic) + "Quanto misura l’angolo?", gradi(v), scale_cands(v), e + " (%s è la lettura sull’altra scala.)" % gradi(180 - v))


def s2_stima():
    v = R.choice([20, 30, 40, 45, 60, 70, 100, 120, 135, 150, 160])
    rot = R.choice([0, 0, 10, 20, 30])
    pic = relabel(AU.angle_fig(v, rot), "un angolo")
    opts = [x for x in (20, 45, 70, 100, 135, 160, 30, 120, 60, 150) if abs(x - v) >= 25]
    R.shuffle(opts)
    return mcq(fig(pic) + "Stima: quale misura è la più vicina a questo angolo?", gradi(v), [gradi(x) for x in opts],
               "Confronta con l’angolo retto (90°): l’angolo è %s. La misura più vicina è <b>%s</b>." % (tipo(v), gradi(v)))


def s3_compl():
    k = R.choice(["compl", "suppl", "espl", "suppl", "compl"])
    if k == "compl":
        a = R.randint(5, 85)
        return mcq("Due angoli sono <b>complementari</b>: insieme fanno 90°. Uno misura %s. Quanto misura l’altro?" % gradi(a), gradi(90 - a),
                   [gradi(180 - a), gradi(a), gradi(100 - a)], "90° − %s = <b>%s</b>." % (gradi(a), gradi(90 - a)))
    if k == "suppl":
        a = R.randint(10, 170)
        if a == 90:
            return None
        return mcq("Due angoli sono <b>supplementari</b>: insieme fanno 180°. Uno misura %s. Quanto misura l’altro?" % gradi(a), gradi(180 - a),
                   [gradi(90 - a) if a < 90 else gradi(360 - a), gradi(a), gradi(200 - a)], "180° − %s = <b>%s</b>." % (gradi(a), gradi(180 - a)))
    a = R.randint(20, 340)
    if a in (180,):
        return None
    return mcq("Due angoli sono <b>esplementari</b>: insieme fanno 360°. Uno misura %s. Quanto misura l’altro?" % gradi(a), gradi(360 - a),
               [gradi(180 - a) if a < 180 else gradi(a - 180), gradi(a), gradi(400 - a)], "360° − %s = <b>%s</b>." % (gradi(a), gradi(360 - a)))


def s3_somma():
    a, b = R.randint(15, 80), R.randint(15, 80)
    if R.random() < 0.5:
        return mcq("Un angolo di %s e uno di %s sono uno accanto all’altro (hanno lo stesso vertice e un lato in comune). Quanto misura l’angolo che formano insieme?" % (gradi(a), gradi(b)), gradi(a + b),
                   [gradi(abs(a - b)) if a != b else gradi(a + b + 10), gradi(180 - a - b), gradi(a + b + 10)], "%s + %s = <b>%s</b>." % (gradi(a), gradi(b), gradi(a + b)))
    s = a + b + R.randint(20, 60)
    return mcq("Un angolo di %s è diviso in due parti. Una parte misura %s. Quanto misura l’altra?" % (gradi(s), gradi(a)), gradi(s - a),
               [gradi(s + a), gradi(180 - a), gradi(s - a + 10)], "%s − %s = <b>%s</b>." % (gradi(s), gradi(a), gradi(s - a)))


def s4_orologio():
    h = R.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    d = h * 30 if h <= 6 else 360 - h * 30
    return mcq("Alle %d:00 la lancetta delle ore e quella dei minuti formano un angolo di quanti gradi (il più piccolo)?" % h, gradi(d),
               [gradi(h * 5), gradi(d + 30), gradi(360 - d) if d != 180 else gradi(90), gradi(d - 30) if d > 30 else gradi(45)],
               "Tra due numeri dell’orologio ci sono 360° : 12 = 30°. Alle %d:00 le lancette sono separate da %d numeri: %d × 30° = <b>%s</b>." % (h, d // 30, d // 30, gradi(d)))


def s4_giri():
    k = R.choice(["giri", "rot", "rot", "giri"])
    if k == "giri":
        f, v = R.choice([("un quarto di giro", 90), ("mezzo giro", 180), ("tre quarti di giro", 270), ("un giro completo", 360)])
        return mcq("Un robot gira su sé stesso di %s. Di quanti gradi ruota?" % f, gradi(v), [gradi(x) for x in (90, 180, 270, 360, 45) if x != v],
                   "Un giro completo è 360°: %s = <b>%s</b>." % (f, gradi(v)))
    a, b = R.choice([(90, 90), (90, 180), (45, 45), (180, 90), (90, 45), (45, 90), (180, 180)])
    return mcq("Una ballerina ruota di %s, poi di altri %s nello stesso verso. Di quanti gradi ha ruotato in tutto?" % (gradi(a), gradi(b)), gradi(a + b),
               [gradi(abs(a - b)) if a != b else gradi(a + b + 90), gradi(a + b + 45), gradi(a * b // 45) if a * b // 45 not in (a + b, abs(a - b)) else gradi(a + b - 45)],
               "%s + %s = <b>%s</b>%s." % (gradi(a), gradi(b), gradi(a + b), " (mezzo giro)" if a + b == 180 else " (un giro completo)" if a + b == 360 else ""))


def main():
    A3.R = R
    seen = set()
    sets = [
        ("Retto, acuto, ottuso, piatto, giro", mix(R, seen, [(s1_tipo, 12), (s1_quanti, 8)])),
        ("Misurare con il goniometro", mix(R, seen, [(s2_goniometro, 20)])),
        ("Stimare l’ampiezza", mix(R, seen, [(s2_stima, 12), (s3_somma, 8)])),
        ("Complementari, supplementari, esplementari", mix(R, seen, [(s3_compl, 20)])),
        ("Rotazioni e orologio", mix(R, seen, [(s4_orologio, 10), (s4_giri, 10)])),
    ]
    body = lesson(
        ["Un <b>angolo</b> è la parte di piano tra due semirette che partono dallo stesso punto, il <b>vertice</b>. Si può pensare come una rotazione.",
         "L’ampiezza si misura in <b>gradi</b> (°) con il <b>goniometro</b>. Retto = 90°, piatto = 180°, giro = 360°; acuto: meno di 90°; ottuso: tra 90° e 180°.",
         "Con il goniometro metti il centro sul vertice e lo 0 su un lato; leggi la scala che parte da 0 su quel lato.",
         "Due angoli che insieme fanno 90° sono <b>complementari</b>, 180° <b>supplementari</b>, 360° <b>esplementari</b>."],
        [("Un angolo misura 65°. Il supplementare?", ["insieme fanno 180°", "180° − 65°"], "115°")],
        [["Leggere la scala sbagliata del goniometro", "Un angolo acuto non può misurare 115°: controlla con il tipo di angolo."],
         ["Pensare che un angolo con i lati lunghi sia più grande", "Conta solo quanto è aperto."],
         ["Confondere complementare (90°) e supplementare (180°)", "«Supplementare» ricorda «piatto»: 180°."]],
        table(["Angolo", "Ampiezza"], [["acuto", "meno di 90°"], ["retto", "90°"], ["ottuso", "più di 90° e meno di 180°"], ["piatto", "180°"], ["giro", "360°"]]))
    faq = [("Perché un giro completo misura 360°?", "È una convenzione antichissima, nata dai Babilonesi: 360 si divide facilmente per 2, 3, 4, 5, 6, 8, 9, 10, 12…"),
           ("Che cos’è un angolo concavo?", "Un angolo più grande di un angolo piatto (più di 180°): i suoi lati non bastano a «chiuderlo» con una linea retta.")]
    make_unit(R, "angoli", "S",
              "Confrontare e misurare angoli utilizzando proprietà e strumenti (il goniometro); riconoscere l’angolo come rotazione",
              "Gli angoli: misurare con il goniometro", "Angoli",
              "Schede di matematica per la classe quarta sugli angoli: retto, acuto, ottuso, piatto e giro, il grado, misurare con il goniometro, stimare, angoli complementari, supplementari ed esplementari, rotazioni. 100 esercizi con soluzioni.",
              "Retto 90°, piatto 180°, giro 360°.", "Goniometro: centro sul vertice, 0 su un lato.",
              body, faq, sets, 14, grade=G)


if __name__ == "__main__":
    main()
