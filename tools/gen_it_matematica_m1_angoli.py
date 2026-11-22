# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Gli angoli (Spazio e figure)
  python3 tools/gen_it_matematica_m1_angoli.py
Angoli acuti, retti, ottusi, piatti, giro, concavi e convessi; misura in gradi, primi e secondi (sistema sessagesimale),
addizione e sottrazione di angoli, angoli complementari, supplementari, esplementari, opposti al vertice, bisettrice.
Errori: trattare i primi come decimali (30° 50′ + 20′ = 30° 70′), confondere complementare e supplementare.
"""
import random
from it_media import M, L, unit, mix, table, W, FOIS, DIV
import gen_it_matematica_c4_angoli as A4

R = random.Random(71111)
G = "prima-media"


def gp(m, s=None):
    """minuti totali (o secondi) → 35° 20′"""
    if s is None:
        g, p = divmod(m, 60)
        return "%d° %d′" % (g, p) if p else "%d°" % g
    g, r = divmod(s, 3600)
    p, sec = divmod(r, 60)
    return "%d° %d′ %d″" % (g, p, sec)


def s1_conv():
    k = R.choice(["g2p", "p2g", "gp2p", "sec"])
    if k == "g2p":
        g = R.randint(2, 15)
        return M("Quanti primi ci sono in %d°?" % g, "%d′" % (g * 60), W("%d′" % (g * 100), "%d′" % (g * 10), "%d′" % (g * 360)), "1° = 60′: %d %s 60 = <b>%d′</b>." % (g, FOIS, g * 60))
    if k == "p2g":
        m = R.randint(70, 400)
        if m % 60 == 0:
            return None
        return M("Scrivi %d′ in gradi e primi." % m, gp(m), W("%d° %d′" % (m // 100, m % 100), gp(m + 60), "%d° %d′" % (m // 60, m % 60 + 10) if m % 60 + 10 < 60 else gp(m - 60)),
                 "%d : 60 = %d con resto %d: <b>%s</b>." % (m, m // 60, m % 60, gp(m)))
    if k == "gp2p":
        g, p = R.randint(1, 30), R.randint(1, 59)
        return M("Quanti primi sono %d° %d′?" % (g, p), "%d′" % (g * 60 + p), W("%d′" % (g * 100 + p), "%d′" % (g + p), "%d′" % (g * 60)), "%d %s 60 + %d = <b>%d′</b>." % (g, FOIS, p, g * 60 + p))
    p = R.randint(2, 9)
    return M("Quanti secondi ci sono in %d′?" % p, "%d″" % (p * 60), W("%d″" % (p * 100), "%d″" % (p * 3600), "%d″" % (p * 10)), "1′ = 60″: <b>%d″</b>." % (p * 60))


def s2_somma():
    a, b = R.randint(10 * 60, 120 * 60), R.randint(5 * 60, 80 * 60)
    if a % 60 == 0 or b % 60 == 0:
        return None
    if R.random() < 0.5:
        r = a + b
        naive = "%d° %d′" % (a // 60 + b // 60, a % 60 + b % 60)
        return M("Calcola: %s + %s" % (gp(a), gp(b)), gp(r), W(naive if a % 60 + b % 60 >= 60 else None, gp(r + 60), gp(r - 1), gp(r + 10)),
                 "Somma gradi e primi: %d° %d′; %s<b>%s</b>." % (a // 60 + b // 60, a % 60 + b % 60, "60′ = 1°: " if a % 60 + b % 60 >= 60 else "", gp(r)))
    if a < b:
        a, b = b, a
    r = a - b
    return M("Calcola: %s − %s" % (gp(a), gp(b)), gp(r), W("%d° %d′" % (a // 60 - b // 60, abs(a % 60 - b % 60)) if a % 60 < b % 60 else None, gp(r + 60), gp(r - 60) if r > 60 else None, gp(r + 1)),
             "%s<b>%s</b>." % ("I primi non bastano: trasforma 1° in 60′. " if a % 60 < b % 60 else "", gp(r)))


def s3_coppie():
    k = R.choice(["compl", "suppl", "espl"])
    tot = {"compl": 90, "suppl": 180, "espl": 360}[k] * 60
    a = R.randint(10 * 60, tot - 10 * 60)
    if a % 60 == 0 and R.random() < 0.7:
        a += R.randint(1, 59)
    name = {"compl": "complementare", "suppl": "supplementare", "espl": "esplementare"}[k]
    other = {"compl": 180 * 60, "suppl": 90 * 60, "espl": 180 * 60}[k]
    return M("Qual è l’angolo %s di %s?" % (name, gp(a)), gp(tot - a), W(gp(other - a) if other > a else gp(a - other), gp(tot - a + 60), "%d° %d′" % (tot // 60 - a // 60, 60 - a % 60) if a % 60 else None),
             "Insieme devono fare %d°: %d° − %s = <b>%s</b>." % (tot // 60, tot // 60, gp(a), gp(tot - a)))


def s4_vertice():
    a = R.randint(20, 160)
    k = R.choice(["opp", "adi", "bis", "bis2"])
    if k == "opp":
        return M("Due rette incidenti formano un angolo di %d°. Quanto misura l’angolo opposto al vertice?" % a, "%d°" % a, W("%d°" % (180 - a), "%d°" % (90 - a) if a < 90 else "%d°" % (360 - a), "%d°" % (2 * a)),
                 "Gli angoli opposti al vertice sono <b>congruenti</b>: %d°." % a)
    if k == "adi":
        return M("Due rette incidenti formano un angolo di %d°. Quanto misura ciascuno degli angoli adiacenti a esso?" % a, "%d°" % (180 - a), W("%d°" % a, "%d°" % (360 - a), "%d°" % abs(90 - a)),
                 "Angoli adiacenti formano un angolo piatto: 180° − %d° = <b>%d°</b>." % (a, 180 - a))
    a = R.randint(10, 89) * 2
    if k == "bis":
        return M("La bisettrice divide un angolo di %d° in due angoli. Quanto misura ciascuno?" % a, "%d°" % (a // 2), W("%d°" % a, "%d°" % (180 - a) if a < 180 else "%d°" % (a + 2), "%d°" % (a // 4) if a % 4 == 0 else "%d°" % (a // 2 + 1)),
                 "La bisettrice divide l’angolo in due parti congruenti: %d° : 2 = <b>%d°</b>." % (a, a // 2))
    return M("Due angoli adiacenti sono uno il doppio dell’altro. Quanto misura il minore?", "60°", W("90°", "120°", "45°"), "x + 2x = 180°, quindi 3x = 180° e x = <b>60°</b> (l’altro 120°).") if R.random() < 0.3 else \
        M("Un angolo supera il suo complementare di %d°. Quanto misura?" % (a % 80 + 2 if (a % 80) % 2 == 0 else a % 80 + 1), "%d°" % ((90 + (a % 80 + 2 if (a % 80) % 2 == 0 else a % 80 + 1)) // 2),
          W("%d°" % ((90 - (a % 80 + 2 if (a % 80) % 2 == 0 else a % 80 + 1)) // 2), "%d°" % (a % 80 + 2 if (a % 80) % 2 == 0 else a % 80 + 1), "45°"),
          "Somma 90°, differenza %d°: maggiore = (90 + %d) : 2 = <b>%d°</b>." % ((a % 80 + 2 if (a % 80) % 2 == 0 else a % 80 + 1), (a % 80 + 2 if (a % 80) % 2 == 0 else a % 80 + 1), (90 + (a % 80 + 2 if (a % 80) % 2 == 0 else a % 80 + 1)) // 2))


def main():
    A4.R = R
    seen = set()
    sets = [
        ("Classificare e misurare", mix(R, seen, [(A4.s1_tipo, 8), (A4.s2_goniometro, 12)])),
        ("Gradi, primi e secondi", mix(R, seen, [(s1_conv, 20)])),
        ("Addizione e sottrazione di angoli", mix(R, seen, [(s2_somma, 20)])),
        ("Complementari, supplementari, esplementari", mix(R, seen, [(s3_coppie, 20)])),
        ("Opposti al vertice, bisettrice e problemi", mix(R, seen, [(s4_vertice, 20)])),
    ]
    body = L(["L’<b>angolo</b> è ciascuna delle due parti di piano delimitate da due semirette con la stessa origine (il vertice). È <b>convesso</b> se non contiene i prolungamenti dei lati, <b>concavo</b> se li contiene.",
              "Si misura in <b>gradi</b> con il sistema <b>sessagesimale</b>: 1° = 60′ (primi), 1′ = 60″ (secondi). Retto 90°, piatto 180°, giro 360°.",
              "Nelle addizioni, ogni 60′ si trasformano in 1°; nelle sottrazioni, se i primi non bastano, si trasforma 1° in 60′.",
              "<b>Complementari</b>: somma 90°; <b>supplementari</b>: somma 180°; <b>esplementari</b>: somma 360°. Gli angoli <b>opposti al vertice</b> sono congruenti."],
             [("35° 40′ + 28° 50′", ["35° + 28° = 63°", "40′ + 50′ = 90′ = 1° 30′", "63° + 1° 30′"], "64° 30′")],
             [["Scrivere 63° 90′", "90′ = 1° 30′: il risultato è 64° 30′."],
              ["Trattare i primi come decimali (35° 40′ = 35,4°)", "40′ sono 40/60 di grado, non 4 decimi."],
              ["Confondere complementare e supplementare", "Complementare: 90°. Supplementare: 180°."]],
             table(["Coppia di angoli", "Somma"], [["complementari", "90°"], ["supplementari", "180°"], ["esplementari", "360°"]]))
    faq = [("Perché un grado ha 60 primi?", "Il sistema sessagesimale viene dai Babilonesi; si usa ancora per gli angoli e per il tempo (ore, minuti, secondi)."),
           ("Due angoli adiacenti sono sempre supplementari?", "Sì, se sono adiacenti nel senso geometrico (consecutivi con i lati non comuni sulla stessa retta): insieme formano un angolo piatto.")]
    unit(G, R, "angoli", "S",
         "Riconoscere, confrontare e misurare angoli utilizzando proprietà e strumenti; operare con le misure in gradi, primi e secondi; conoscere angoli complementari, supplementari, esplementari e opposti al vertice",
         "Gli angoli: gradi, primi e angoli particolari", "Angoli",
         "Schede di matematica per la prima media sugli angoli: classificazione, goniometro, gradi, primi e secondi, addizione e sottrazione di angoli, complementari, supplementari, esplementari, opposti al vertice e bisettrice. 100 esercizi con soluzioni.",
         "1° = 60′, 1′ = 60″.", "Complementari 90°, supplementari 180°, esplementari 360°.",
         body, faq, sets, 11)


if __name__ == "__main__":
    main()
