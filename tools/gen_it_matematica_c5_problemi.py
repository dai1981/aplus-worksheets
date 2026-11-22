# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: I problemi (Problemi)
  python3 tools/gen_it_matematica_c5_problemi.py
Problemi con più operazioni, dati nascosti (dozzina, paio, settimana, anno), somma e differenza di due numeri,
problemi con la media, problemi con le misure e il tempo, problemi «al contrario», strategie (tabella, tentativi).
Errori: usare tutti i dati, non vedere il dato nascosto, nei problemi somma-differenza dividere subito la somma per 2.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, eur, ora, dur, FOIS, DIV

R = random.Random(70515)
G = "classe-quinta"
K = Kids(R)


def s1_passi():
    p = K.next()
    k = R.choice(["scuola", "libreria", "bus", "festa", "orto"])
    if k == "scuola":
        c, a = R.randint(4, 8), R.randint(18, 26)
        m = R.randint(10, 30)
        r = c * a - m
        return mcq("Una scuola ha %d classi da %d alunni. Oggi %d alunni sono in gita. Quanti alunni sono a scuola?" % (c, a, m), num(r), [num(c * a), num(c * (a - m)) if a > m else num(r + 10), num(c + a - m) if c + a > m else num(r - 1)],
                   "%d %s %d = %d; %d − %d = <b>%s</b>." % (c, FOIS, a, c * a, c * a, m, num(r)))
    if k == "libreria":
        a, b, pa, pb = R.randint(2, 5), R.randint(2, 6), R.randint(8, 18), R.randint(3, 9)
        pay = 100 if a * pa + b * pb < 100 else 200
        r = pay - a * pa - b * pb
        return mcq("%s compra %d libri da %d € e %d quaderni da %d €. Paga con %d €. Quanto riceve di resto?" % (p[0], a, pa, b, pb, pay), "%d €" % r,
                   ["%d €" % (a * pa + b * pb), "%d €" % (pay - a * pa), "%d €" % (pay - (a + b) * (pa + pb)) if pay > (a + b) * (pa + pb) else "%d €" % (r + 5)],
                   "%d + %d = %d €; %d − %d = <b>%d €</b>." % (a * pa, b * pb, a * pa + b * pb, pay, a * pa + b * pb, r))
    if k == "bus":
        s0, up, down, up2 = R.randint(10, 30), R.randint(5, 15), R.randint(3, 12), R.randint(2, 10)
        r = s0 + up - down + up2
        return mcq("Su un autobus ci sono %d persone. Alla prima fermata salgono %d persone e ne scendono %d; alla seconda ne salgono %d. Quante persone ci sono ora?" % (s0, up, down, up2), str(r),
                   [str(s0 + up + down + up2), str(s0 + up - down), str(r - 1)], "%d + %d − %d + %d = <b>%d</b>." % (s0, up, down, up2, r))
    if k == "festa":
        n, x, pr = R.randint(15, 25), R.randint(2, 4), R.choice([150, 200, 250])
        tot = n * x * pr
        return mcq("A una festa ci sono %d bambini; ognuno usa %d bicchieri. I bicchieri si comprano a pacchi da 10 a %s il pacco. Quanto si spende al minimo?" % (n, x, eur(pr)),
                   eur(((n * x + 9) // 10) * pr), [eur(n * x * pr), eur((n * x // 10) * pr) if n * x % 10 else eur(((n * x) // 10 + 1) * pr), eur(n * pr)],
                   "Bicchieri: %d; pacchi: %d (%s); spesa: %d %s %s = <b>%s</b>." % (n * x, (n * x + 9) // 10, "si arrotonda per eccesso" if n * x % 10 else "esatti", (n * x + 9) // 10, FOIS, eur(pr), eur(((n * x + 9) // 10) * pr)))
    f, pf, sp = R.randint(4, 9), R.randint(6, 15), R.randint(20, 40)
    return mcq("In un orto ci sono %d file con %d piante di pomodoro. Ogni pianta dà circa 3 kg di pomodori. Se ne vendono %d kg, quanti kg restano?" % (f, pf, sp), "%d kg" % (f * pf * 3 - sp),
               ["%d kg" % (f * pf * 3), "%d kg" % (f * pf - sp) if f * pf > sp else "%d kg" % (f * pf * 3 + sp), "%d kg" % (f * pf * 3 - sp + 10)],
               "%d %s %d = %d piante; %d %s 3 = %d kg; %d − %d = <b>%d kg</b>." % (f, FOIS, pf, f * pf, f * pf, FOIS, f * pf * 3, f * pf * 3, sp, f * pf * 3 - sp))


def s2_nascosto():
    p = K.next()
    k = R.choice(["dozzina", "paio", "settimana", "anno", "ora", "decina"])
    if k == "dozzina":
        n = R.randint(3, 9)
        return mcq("La mamma di %s compra %d dozzine di uova. Ne usa 10 per le torte. Quante uova restano?" % (p[0], n), str(n * 12 - 10), [str(n - 10 + 12) if n * 12 > 0 else "0", str(n * 10 - 10), str(n * 12)],
                   "Dato nascosto: 1 dozzina = 12. %d %s 12 = %d; %d − 10 = <b>%d</b>." % (n, FOIS, n * 12, n * 12, n * 12 - 10))
    if k == "paio":
        return _paio(R.randint(3, 8))
    if k == "settimana":
        w, m = R.randint(2, 6), R.randint(10, 30)
        return mcq("%s si allena %d minuti al giorno, tutti i giorni, per %d settimane. Quanti minuti in tutto?" % (p[0], m, w), num(w * 7 * m), [num(w * m), num(w * 5 * m), num(7 * m)],
                   "Dato nascosto: 1 settimana = 7 giorni. %d %s 7 = %d giorni; %d %s %d = <b>%s</b> minuti." % (w, FOIS, w * 7, w * 7, FOIS, m, num(w * 7 * m)))
    if k == "anno":
        m = R.randint(15, 60)
        return mcq("La famiglia di %s spende %d € al mese per l’abbonamento dei mezzi. Quanto spende in un anno?" % (p[0], m), "%s €" % num(m * 12), ["%s €" % num(m * 10), "%s €" % num(m * 365), "%s €" % num(m * 52)],
                   "Dato nascosto: 1 anno = 12 mesi. %d %s 12 = <b>%s €</b>." % (m, FOIS, num(m * 12)))
    if k == "ora":
        h = R.randint(2, 5)
        return mcq("Un rubinetto perde 2 litri ogni minuto. Quanti litri perde in %d ore?" % h, num(h * 60 * 2),
                   [num(h * 2), num(h * 100 * 2), num(h * 60)], "Dato nascosto: 1 ora = 60 minuti. %d %s 60 = %d minuti; %d %s 2 = <b>%s</b> litri." % (h, FOIS, h * 60, h * 60, FOIS, num(h * 120)))
    n = R.randint(3, 9)
    return mcq("%s ha %d decine di figurine e ne regala 15. Quante ne ha ora?" % (p[0], n), str(n * 10 - 15), [str(n - 15 + 10) if n + 10 > 15 else str(n * 10 + 15), str(n * 10), str(n * 10 - 5)],
               "%d decine = %d; %d − 15 = <b>%d</b>." % (n, n * 10, n * 10, n * 10 - 15))


def _paio(n):
    n = n + 8
    return mcq("Una squadra di %d bambini compra un paio di scarpe da calcio a testa. Quante scarpe sono in tutto?" % n, str(n * 2), [str(n), str(n + 2), str(n * 4)],
               "Dato nascosto: un paio = 2. %d %s 2 = <b>%d</b>." % (n, FOIS, n * 2))


def s3_somdiff():
    a = R.randint(20, 300)
    d = R.randint(4, 80)
    b = a + d
    s = a + b
    p1, p2 = K.two()
    ctx = R.choice(["figurine", "euro", "punti", "libri"])
    return mcq("%s e %s hanno in tutto %s %s. %s ne ha %d più di %s. %s %s ha %s?" % (p1[0], p2[0], num(s), ctx, p2[0], d, p1[0], "Quante" if ctx == "figurine" else "Quanti", ctx, p1[0]), num(a),
               [num(b), num(s // 2), num(s - d)], "Togli la differenza e dividi per 2: (%s − %d) %s 2 = <b>%s</b>; %s ne ha %s." % (num(s), d, DIV, num(a), p2[0], num(b)))


def s3_eta():
    p = K.next()
    a = R.randint(8, 11)
    k = R.choice(["somma", "volte"])
    if k == "somma":
        d = R.randint(25, 35)
        return mcq("%s ha %d anni. Sua madre ha %d anni più di %s. Tra 5 anni, quanti anni avranno in tutto?" % (p[0], a, d, "lei" if p[1] == "lei" else "lui"), str(2 * a + d + 10),
                   [str(2 * a + d), str(2 * a + d + 5), str(a + d + 5)], "Oggi: %d + %d = %d. Tra 5 anni ognuno ha 5 anni in più: %d + 10 = <b>%d</b>." % (a, a + d, 2 * a + d, 2 * a + d, 2 * a + d + 10))
    k2 = R.randint(3, 4)
    return mcq("%s ha %d anni; il nonno ha %d volte la sua età più 7 anni. Quanti anni ha il nonno?" % (p[0], a + 7, k2), str((a + 7) * k2 + 7),
               [str((a + 7) * k2), str((a + 7) * (k2 + 7)), str((a + 7) + k2 + 7)], "%d %s %d = %d; + 7 = <b>%d</b>." % (a + 7, FOIS, k2, (a + 7) * k2, (a + 7) * k2 + 7))


def s4_media():
    p = K.next()
    k = R.choice(["voti", "km", "spesa"])
    n = R.randint(3, 5)
    m = R.randint(6, 9) if k == "voti" else R.randint(5, 40)
    vals = [m + d for d in R.sample(range(-3, 4), n)]
    shift = sum(vals) - m * n
    vals[-1] -= shift
    if any(v <= 0 for v in vals) or (k == "voti" and any(v > 10 for v in vals)):
        return None
    lab = {"voti": "Nelle verifiche %s ha preso questi voti: %s. Qual è la media?", "km": "In %d giorni %s percorre in bici %s km. Quanti km in media al giorno?", "spesa": "In %d settimane %s spende %s €. Qual è la spesa media?"}[k]
    q = lab % (p[0], ", ".join(map(str, vals))) if k == "voti" else lab % (n, p[0], ", ".join(map(str, vals)))
    return mcq(q, str(m), [str(sum(vals)), str(max(vals)), str(m + 1), str(sum(vals) // 2)],
               "Media = somma %s numero dei dati: %d %s %d = <b>%d</b>." % (DIV, sum(vals), DIV, n, m))


def s4_contrario():
    p = K.next()
    x = R.randint(10, 60)
    a, b, c = R.randint(5, 30), R.randint(2, 5), R.randint(3, 20)
    r = (x + a) * b - c
    return mcq("%s pensa un numero, aggiunge %d, moltiplica per %d e toglie %d. Ottiene %d. Che numero ha pensato?" % (p[0], a, b, c, r), str(x),
               [str((r - c) // b - a) if (r - c) % b == 0 else str(x + 2), str(r // b - a + c) if r // b - a + c != x else str(x + 1), str((r + c) // b + a)],
               "Fai le operazioni al contrario: %d + %d = %d; %d %s %d = %d; %d − %d = <b>%d</b>." % (r, c, r + c, r + c, DIV, b, (r + c) // b, (r + c) // b, a, x))


def s5_tempo():
    p = K.next()
    k = R.choice(["treno", "compiti", "viaggio"])
    if k == "treno":
        h, m = R.randint(7, 16), R.choice([5, 10, 15, 20, 25, 35, 40, 50])
        d = R.choice([85, 95, 110, 125, 140, 155, 170])
        e = h * 60 + m + d
        return mcq("Un treno parte da Milano alle %s e arriva a Roma dopo %s. A che ora arriva?" % (ora(h, m), dur(d)) if d >= 170 else
                   "Un treno parte da Bologna alle %s e arriva a Napoli dopo %s. A che ora arriva?" % (ora(h, m), dur(d)), ora(e // 60, e % 60),
                   [ora(e // 60 - 1, e % 60), ora(h + d // 100, (m + d % 100) % 60), ora(e // 60, (e % 60 + 10) % 60)],
                   "%s + %s = <b>%s</b>." % (ora(h, m), dur(d), ora(e // 60, e % 60)))
    if k == "compiti":
        a, b, c = R.choice([20, 25, 30, 35]), R.choice([15, 20, 25, 40]), R.choice([10, 15, 20])
        tot = a + b + c
        return mcq("%s fa i compiti di matematica per %d minuti, di italiano per %d e di inglese per %d. Quanto tempo in tutto?" % (p[0], a, b, c), dur(tot),
                   [dur(tot + 40) if tot >= 60 else dur(tot + 10), "%d h %d min" % (tot // 100, tot % 100) if tot >= 100 else dur(tot - 5), dur(tot + 5)],
                   "%d + %d + %d = %d minuti = <b>%s</b>." % (a, b, c, tot, dur(tot)))
    km, v = R.choice([(240, 80), (300, 100), (180, 60), (360, 90), (210, 70)])
    return mcq("Un’auto percorre %d km alla velocità media di %d km all’ora. Quanto dura il viaggio?" % (km, v), "%d ore" % (km // v), ["%d ore" % (km // v + 1), "%d ore" % (km - v), "%d ore" % (km // 10)],
               "%d %s %d = <b>%d ore</b>." % (km, DIV, v, km // v))


def main():
    seen = set()
    sets = [
        ("Problemi con più operazioni", mix(R, seen, [(s1_passi, 20)])),
        ("Dati nascosti", mix(R, seen, [(s2_nascosto, 20)])),
        ("Somma e differenza, età", mix(R, seen, [(s3_somdiff, 12), (s3_eta, 8)])),
        ("Media e problemi al contrario", mix(R, seen, [(s4_media, 10), (s4_contrario, 10)])),
        ("Problemi con il tempo", mix(R, seen, [(s5_tempo, 20)])),
    ]
    body = lesson(
        ["Leggi bene, trova la <b>domanda finale</b> e le <b>domande nascoste</b> (i passaggi intermedi).",
         "Cerca i <b>dati nascosti</b>: una dozzina = 12, un paio = 2, una settimana = 7 giorni, un anno = 12 mesi, un’ora = 60 minuti.",
         "Somma e differenza: togli la differenza dalla somma e dividi per 2: trovi il numero più piccolo.",
         "Media = somma dei dati %s numero dei dati. Nei problemi «al contrario» fai le operazioni inverse partendo dalla fine." % DIV],
        [("Due numeri hanno somma 50 e differenza 10.", ["50 − 10 = 40", "40 %s 2 = 20" % DIV, "20 + 10 = 30"], "20 e 30")],
        [["Usare tutti i dati del testo", "Chiediti quali dati servono per la domanda."],
         ["Non vedere il dato nascosto", "Parole come dozzina, paio, settimana nascondono un numero."],
         ["Dividere subito la somma per 2", "Prima togli la differenza, poi dividi per 2."]])
    faq = [("Come si risolve un problema con più domande?", "Si scrivono le domande nascoste in ordine e si risponde una alla volta, oppure si scrive un’unica espressione."),
           ("Che cos’è un dato nascosto?", "È un numero che non è scritto in cifre ma si capisce da una parola: «una dozzina» vuol dire 12.")]
    make_unit(R, "problemi", "P",
              "Risolvere problemi in contesti diversi, anche con più passaggi; individuare dati utili, nascosti e superflui; descrivere il procedimento seguito e riconoscere strategie di soluzione diverse",
              "I problemi: più operazioni, dati nascosti e media", "Problemi",
              "Schede di matematica per la classe quinta sui problemi: più operazioni, dati nascosti, somma e differenza, età, media, problemi al contrario e problemi con il tempo. 100 esercizi con soluzioni.",
              "Trova le domande nascoste e rispondi una alla volta.", "Somma e differenza: (somma − differenza) : 2.",
              body, faq, sets, 15, grade=G)


if __name__ == "__main__":
    main()
