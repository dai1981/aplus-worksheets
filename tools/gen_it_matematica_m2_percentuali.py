# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Percentuali (Numeri)
  python3 tools/gen_it_matematica_m2_percentuali.py
La percentuale come rapporto con denominatore 100 e come proporzione (p : 100 = parte : totale); calcolo della parte,
della percentuale e del totale; sconti, aumenti, IVA al 22%, interesse semplice in un anno; percentuali nei grafici.
Errori: 5% = 0,5; calcolare lo sconto e non il prezzo scontato; dividere per la percentuale invece che moltiplicare.
"""
import math
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, fq, d, dk, Kids

R = random.Random(71205)
G = "seconda-media"
K = Kids(R)
USED = set()


def pc(x):
    return "%s%%" % d(Fr(x))


def eu(x):
    x = Fr(x)
    return "%s €" % (d(x) if x.denominator == 1 else dk(x, 2))


def il(p):
    """l’8%, l’11%, l’80%, l’1%; il 15%"""
    n = int(Fr(p))
    return "l’" if n in (1, 8, 11) or 80 <= n <= 89 or 800 <= n <= 899 else "il "


def s1_conv():
    k = R.choice(["dec", "frac", "pc_dec", "pc_frac"])
    if k in ("dec", "pc_dec"):
        p = R.choice([1, 2, 5, 8, 12, 15, 35, 40, 75, 120, 150, Fr(5, 2), Fr(25, 2), Fr(1, 2)])
        x = Fr(p) / 100
        if k == "dec":
            return M("Scrivi %s come numero decimale." % pc(p), d(x), W(d(x * 10), d(x / 10), d(Fr(p))), "%s = %s : 100 = <b>%s</b>." % (pc(p), d(Fr(p)), d(x)))
        return M("Scrivi %s come percentuale." % d(x), pc(p), W(pc(Fr(p) / 10), pc(Fr(p) * 10), pc(x)), "%s × 100 = <b>%s</b>." % (d(x), pc(p)))
    f = R.choice([Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 5), Fr(2, 5), Fr(3, 5), Fr(1, 8), Fr(3, 8), Fr(1, 10), Fr(7, 10), Fr(1, 20), Fr(9, 20), Fr(1, 25), Fr(6, 25), Fr(1, 50)])
    p = f * 100
    if k == "frac":
        return M("Scrivi la frazione %s come percentuale." % fq(f), pc(p), W(pc(f.numerator * 10), pc(f.numerator + f.denominator), pc(f.denominator), pc(p / 10), pc(p * 10) if p * 10 <= 1000 else None),
                 "%s = %s/100 = <b>%s</b>." % (fq(f), d(p), pc(p)))
    return M("Scrivi %s come frazione ridotta ai minimi termini." % pc(p), fq(f), W(fq(Fr(f.numerator, f.denominator * 10)), fq(1 / f), fq(Fr(f.denominator, 100)) if Fr(f.denominator, 100) != f else None, fq(Fr(f.numerator, 100)), fq(f * 10) if f * 10 != 1 else fq(Fr(1, 1000))),
             "%s = %s/100 = <b>%s</b>." % (pc(p), d(p), fq(f)))


def s2_parte():
    p = R.choice([3, 4, 6, 8, 12, 15, 18, 22, 35, 45, 60, 65, 120, Fr(5, 2), Fr(15, 2)])
    n = R.randint(2, 60) * (40 if Fr(p).denominator == 2 else 20 if p % 5 else 4)
    r = Fr(p) * n / 100
    if r.denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100):
        return None
    return M("Calcola %s%s di %s." % (il(p), pc(p), num(n)), d(r), W(d(r * 10), d(r / 10), d(n - r) if n > r else None, d(Fr(n, 1) / Fr(p)) if (Fr(n, 1) / Fr(p)).denominator in (1, 2, 4, 5) else None),
             "%s × %s : 100 = <b>%s</b>." % (num(n), pc(p).rstrip("%"), d(r)))


def s2_quale():
    n = R.choice([20, 25, 40, 50, 80, 120, 150, 200, 250, 400, 500, 800])
    k = R.randint(1, n - 1)
    p = Fr(k * 100, n)
    if p.denominator not in (1, 2) or k * 2 == n:
        return None
    ctx = R.choice(["alunni su %d hanno un animale" % n, "studenti su %d vanno a scuola in bici" % n, "posti su %d sono occupati" % n, "semi su %d sono germogliati" % n])
    return M("%d %s. Che percentuale è?" % (k, ctx), pc(p), W(pc(k) if k <= 100 else None, pc(100 - p), pc(Fr(n, k)) if Fr(n, k).denominator in (1, 2) else None, pc(p * 2) if p * 2 <= 100 else pc(p / 2), pc(p + 10) if p <= 90 else pc(p - 10)),
             "%d : %d = p : 100; p = %d × 100 : %d = <b>%s</b>." % (k, n, k, n, pc(p)))


def s3_totale():
    p = R.choice([5, 10, 15, 20, 25, 30, 40, 60, 75, 12, 8])
    t = R.randint(3, 50) * (100 // math.gcd(100, p))
    r = t * p // 100
    ctx = R.choice(["Il %s degli alunni di una scuola, cioè %d alunni, fa sport. Quanti sono tutti gli alunni?",
                    "Uno sconto del %s corrisponde a %d €. Qual era il prezzo iniziale?",
                    "Il %s dei posti di un cinema, cioè %d posti, è libero. Quanti posti ha il cinema?",
                    "Nel paese il %s degli abitanti, cioè %d persone, ha meno di 14 anni. Quanti sono gli abitanti?"])
    if "abitanti" in ctx:
        t *= 20
        r = t * p // 100
    q = ctx.replace("%d", num(r)) % pc(p)
    if p in (8, 11):
        q = q.replace("Il %s" % pc(p), "L’%s" % pc(p)).replace("del %s" % pc(p), "dell’%s" % pc(p)).replace("il %s" % pc(p), "l’%s" % pc(p))
    unit_ = " €" if "€" in q else ""
    return M(q, num(t) + unit_, W(num(r * p) + unit_, num(r + p) + unit_, num(r * 100 // p + r) + unit_ if r * 100 % p == 0 else None, num(t - r) + unit_),
             "%s : 100 = %d : x; x = %d × 100 : %s = <b>%s%s</b>." % (d(Fr(p)), r, r, d(Fr(p)), num(t), unit_))


def s4_sconto():
    p = R.choice([10, 15, 20, 25, 30, 35, 40, 50])
    pr = R.randint(3, 60) * 4 if p in (25,) else R.randint(2, 50) * 10 if p in (10, 30, 40, 50, 20) else R.randint(2, 40) * 20
    sc = Fr(pr * p, 100)
    if (p, pr) in USED:
        return None
    USED.add((p, pr))
    it = R.choice(["Un giubbotto", "Una bicicletta", "Uno zaino", "Un paio di scarpe da ginnastica", "Un monopattino"])
    if R.random() < 0.5:
        return M("%s costa %s. Con lo sconto del %s, quanto si paga?" % (it, eu(pr), pc(p)), eu(pr - sc), W(eu(sc), eu(pr - p), eu(pr * (100 + p) / Fr(100))),
                 "Si paga il %s: %d × %d : 100 = <b>%s</b>." % (pc(100 - p), pr, 100 - p, eu(pr - sc)))
    np = Fr(pr * (100 - p), 100)
    return M("Con uno sconto del %s, %s si paga %s. Qual era il prezzo prima dello sconto?" % (pc(p), it[0].lower() + it[1:], eu(np)), eu(pr), W(eu(np + Fr(np * p, 100)), eu(np - Fr(np * p, 100)), eu(np + p)),
             "%s è il %s del prezzo: %s : %d × 100 = <b>%s</b>." % (eu(np), pc(100 - p), d(np), 100 - p, eu(pr)))


def s4_aumento():
    k = R.choice(["aum", "iva", "dim"])
    if k == "iva":
        pr = R.randint(1, 40) * 50
        iva = Fr(pr * 22, 100)
        return M("Un computer costa %s più IVA al 22%%. Quanto si paga in tutto?" % eu(pr), eu(pr + iva), W(eu(iva), eu(pr + 22), eu(pr - iva), eu(pr * Fr(122, 10))),
                 "IVA: %d × 22 : 100 = %s; totale: %s + %s = <b>%s</b>." % (pr, eu(iva), eu(pr), eu(iva), eu(pr + iva)))
    a = R.randint(2, 40) * 10
    b = a + a * R.choice([10, 20, 25, 30, 50, 5]) // 100 if k == "aum" else a - a * R.choice([10, 20, 25, 30, 50, 5]) // 100
    if (b - a) * 100 % a:
        return None
    p = Fr(abs(b - a) * 100, a)
    word = "aumento" if k == "aum" else "diminuzione"
    return M("Il prezzo di un abbonamento passa da %s a %s. Qual è la percentuale di %s?" % (eu(a), eu(b), word), pc(p), W(pc(abs(b - a)) if abs(b - a) <= 100 else None, pc(Fr(abs(b - a) * 100, b)) if Fr(abs(b - a) * 100, b).denominator in (1, 2) else None, pc(p * 2), pc(p + 5), pc(p - 5) if p > 5 else pc(p + 10)),
             "Differenza: %s; %d : %d × 100 = <b>%s</b>." % (eu(abs(b - a)), abs(b - a), a, pc(p)))


def s5():
    p = K.next()
    k = R.choice(["interesse", "voti", "succo", "grafico", "due", "colesterolo"])
    if k == "interesse":
        c = R.randint(2, 40) * 100
        t = R.choice([1, 2, 3, 4, 5])
        i = Fr(c * t, 100)
        return M("%s deposita %s in banca al tasso annuo del %s. Quanto interesse riceve dopo un anno?" % (p[0], eu(c), pc(t)), eu(i), W(eu(c + i), eu(i * 10), eu(t * 10)),
                 "%d × %d : 100 = <b>%s</b>." % (c, t, eu(i)))
    if k == "voti":
        n = R.choice([20, 25, 40, 50])
        a = R.randint(2, n // 2 - 1)
        if a * 100 % n:
            return None
        return M("In una verifica di %d domande %s ne ha sbagliate %d. Che percentuale di risposte giuste ha dato?" % (n, p[0], a), pc(Fr((n - a) * 100, n)), W(pc(Fr(a * 100, n)), pc(n - a), pc(100 - a)),
                 "Giuste: %d; %d : %d × 100 = <b>%s</b>." % (n - a, n - a, n, pc(Fr((n - a) * 100, n))))
    if k == "succo":
        v = R.choice([200, 250, 500, 750, 1000, 1500])
        pp = R.choice([12, 20, 30, 40, 60])
        r = Fr(v * pp, 100)
        return M("Una bottiglia da %s ml di succo contiene il %s di frutta. Quanti ml di frutta contiene?" % (num(v), pc(pp)), "%s ml" % d(r), W("%s ml" % d(r * 10), "%s ml" % d(v - r), "%d ml" % pp, "%s ml" % d(r / 10)),
                 "%s × %d : 100 = <b>%s ml</b>." % (num(v), pp, d(r)))
    if k == "grafico":
        tot = R.choice([200, 300, 400, 500, 600, 800])
        pp = R.choice([15, 20, 25, 30, 35, 40, 45])
        return M("In un sondaggio su %d ragazzi, il %s preferisce il calcio. In un aerogramma, quanti gradi ha il settore del calcio?" % (tot, pc(pp)), "%s°" % d(Fr(360 * pp, 100)), W("%d°" % pp, "%s°" % d(Fr(tot * pp, 100)), "%s°" % d(Fr(180 * pp, 100)), "%d°" % (pp * 10)),
                 "%s di 360° = 360 × %d : 100 = <b>%s°</b>." % (pc(pp), pp, d(Fr(360 * pp, 100))))
    if k == "due":
        pr = R.randint(2, 20) * 100
        a, b = R.choice([(10, 10), (20, 10), (10, 20), (20, 20), (50, 50), (25, 20)])
        fin = Fr(pr) * (100 + a) / 100 * (100 - b) / 100
        return M("Un prezzo di %s aumenta del %s e poi diminuisce del %s. Qual è il prezzo finale?" % (eu(pr), pc(a), pc(b)), eu(fin), W(eu(pr + Fr(pr * (a - b), 100)), eu(Fr(pr) * (100 + a) / 100), eu(fin + 1)),
                     "%s × %s = %s; poi × %s = <b>%s</b>. Le due percentuali si calcolano su prezzi diversi." % (eu(pr), d(Fr(100 + a, 100)), eu(Fr(pr) * (100 + a) / 100), d(Fr(100 - b, 100)), eu(fin)))
    m = R.choice([50, 60, 70, 80, 90])
    pp = R.choice([60, 65, 70, 75])
    return M("Il corpo di una persona di %d kg è fatto di acqua per circa il %s. Quanti kg di acqua sono?" % (m, pc(pp)), "%s kg" % d(Fr(m * pp, 100)), W("%s kg" % d(Fr(m * (100 - pp), 100)), "%d kg" % pp, "%s kg" % d(Fr(m * pp, 10))),
             "%d × %d : 100 = <b>%s kg</b>." % (m, pp, d(Fr(m * pp, 100))))


def main():
    seen = set()
    sets = [
        ("Percentuali, frazioni e decimali", mix(R, seen, [(s1_conv, 20)])),
        ("Calcolare la parte e la percentuale", mix(R, seen, [(s2_parte, 12), (s2_quale, 8)])),
        ("Calcolare il totale", mix(R, seen, [(s3_totale, 14), (s2_quale, 6)])),
        ("Sconti, aumenti e IVA", mix(R, seen, [(s4_sconto, 12), (s4_aumento, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["La <b>percentuale</b> p% è il rapporto p/100. Per esempio 12% = 12/100 = 0,12.",
              "Ogni problema si scrive con una proporzione: <b>p : 100 = parte : totale</b>. Conoscendo due termini trovi il terzo.",
              "Parte = totale × p : 100. Percentuale = parte : totale × 100. Totale = parte : p × 100.",
              "Sconto del 20%: si paga l’80% del prezzo. Aumento del 22% (IVA): si paga il 122%."],
             [("Il 15% di 240", ["240 × 15 : 100"], "36"), ("18 alunni su 24", ["18 : 24 × 100"], "75%"), ("Il 30% è 45 €", ["45 : 30 × 100"], "150 €")],
             [["5% = 0,5", "5% = 5/100 = 0,05."],
              ["Calcolare lo sconto e non il prezzo da pagare", "Dopo lo sconto si sottrae: prezzo − sconto."],
              ["+10% e poi −10% riporta al prezzo iniziale", "No: il secondo 10% si calcola su un prezzo diverso."]],
             table(["Cerco", "Calcolo"], [["la parte", "totale × p : 100"], ["la percentuale", "parte : totale × 100"], ["il totale", "parte : p × 100"]]))
    faq = [("Come si calcola l’IVA?", "In Italia l’aliquota ordinaria è del 22%: si calcola il 22% del prezzo e lo si aggiunge, oppure si moltiplica il prezzo per 1,22."),
           ("Un aumento del 10% e poi uno sconto del 10% si annullano?", "No. Da 100 € si passa a 110 €, poi il 10% di 110 € è 11 €: il prezzo finale è 99 €.")]
    unit(G, R, "percentuali", "N",
         "Utilizzare frazioni, numeri decimali e percentuali; calcolare percentuali, sconti, aumenti e interessi in situazioni concrete",
         "Percentuali", "Percentuali",
         "Schede di matematica per la seconda media sulle percentuali: percentuali, frazioni e decimali, calcolo della parte, della percentuale e del totale, sconti, aumenti, IVA e interesse. 100 esercizi con soluzioni.",
         "p : 100 = parte : totale.", "Sconto del 20%: si paga l’80%.",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
