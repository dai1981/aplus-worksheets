# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Probabilità condizionata e teorema di Bayes (Dati e previsioni)
  python3 tools/gen_it_matematica_l4_probabilita_condizionata_e_bayes.py
Probabilità condizionata P(A|B) = P(A ∩ B)/P(B) (da formula e da tabella a doppia entrata), teorema del prodotto,
eventi indipendenti (verifica), estrazioni senza reimmissione, teorema delle probabilità totali (diagrammi ad albero),
teorema di Bayes (test diagnostici, urne, macchine).
Errori: confondere P(A|B) con P(B|A), dividere per il totale generale, sommare i rami invece di moltiplicarli.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, albero

R = random.Random(72411)
G = "quarta-liceo"


def il(n):
    n = int(n)
    return "l’%d%%" % n if (str(n)[0] == "8" or n in (1, 11)) else "il %d%%" % n


def PW(*xs):
    return [x for x in W(*xs) if 0 < Fr(x) < 1]


def s1_form():
    pb = Fr(R.randint(3, 9), 10)
    pab = Fr(R.randint(1, int(pb * 10) - 1), 10)
    v = pab / pb
    k = R.choice(["cond", "prod"])
    if k == "cond":
        return M("Si sa che P(B) = %s e P(A ∩ B) = %s. Calcola P(A|B)." % (d(pb), d(pab)), fq(v), [fq(x) for x in PW(pab * pb, pb / pab if pab else None, pab, 1 - v) if x != v] + [fq(pab + pb) if pab + pb < 1 else fq(v / 2)],
                     "P(A|B) = P(A ∩ B) / P(B) = %s / %s = <b>%s</b>." % (d(pab), d(pb), fq(v)))
    pa = Fr(R.randint(2, 9), 10)
    pba = Fr(R.randint(1, 9), 10)
    v = pa * pba
    return M("P(A) = %s e P(B|A) = %s. Calcola P(A ∩ B)." % (d(pa), d(pba)), d(v), [d(x) for x in PW(pa + pba if pa + pba < 1 else None, pba / pa if pba < pa else None, pa * (1 - pba), 1 - v, (1 - pa) * pba, (pa + pba) / 2) if x != v],
             "Teorema del prodotto: P(A ∩ B) = P(A) · P(B|A) = <b>%s</b>." % d(v))


def s2_tab():
    a, b, c, dd = [R.randint(5, 40) for _ in range(4)]
    righe = R.choice([("Maschi", "Femmine"), ("Liceo", "Istituto tecnico")])
    col = R.choice([("Fa sport", "Non fa sport", "faccia sport", "fa sport"), ("Usa il bus", "Non usa il bus", "usi il bus", "usa il bus")])
    t = table(["", col[0], col[1], "Totale"], [[righe[0], str(a), str(b), str(a + b)], [righe[1], str(c), str(dd), str(c + dd)], ["Totale", str(a + c), str(b + dd), str(a + b + c + dd)]])
    k = R.choice(["rc", "cr"])
    tot = a + b + c + dd
    if k == "rc":
        v = Fr(a, a + b)
        q = "Si sceglie a caso una persona tra i «%s». Qual è la probabilità che %s?" % (righe[0], col[2])
        e = "Si guarda solo la riga «%s»: %d su %d, <b>%s</b>." % (righe[0], a, a + b, fq(v))
        w = [Fr(a, tot), Fr(a, a + c), Fr(a + c, tot)]
    else:
        v = Fr(a, a + c)
        q = "Si sceglie a caso una persona che %s. Qual è la probabilità che sia tra i «%s»?" % (col[3], righe[0])
        e = "Si guarda solo la colonna «%s»: %d su %d, <b>%s</b>." % (col[0], a, a + c, fq(v))
        w = [Fr(a, tot), Fr(a, a + b), Fr(a + b, tot)]
    return M("%s%s" % (t, q), fq(v), [fq(x) for x in PW(*w) if x != v] + [fq(1 - v)], e)


def s3_indip():
    pa, pb = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
    ind = R.random() < 0.5
    pab = pa * pb if ind else pa * pb + Fr(R.choice([-1, 1]), 100)
    if not 0 < pab < min(pa, pb):
        return None
    ans = "sì" if ind else "no"
    return M("P(A) = %s, P(B) = %s, P(A ∩ B) = %s. Gli eventi A e B sono indipendenti?" % (d(pa), d(pb), d(pab)), ans, ["no" if ind else "sì", "sono incompatibili", "non si può stabilire"],
             "Indipendenti se P(A ∩ B) = P(A) · P(B) = %s: %s, quindi <b>%s</b>." % (d(pa * pb), "è uguale" if ind else "è diverso", ans))


def s3_estr():
    r, b = R.randint(2, 7), R.randint(2, 7)
    tot = r + b
    k = R.choice(["rb", "rr", "seconda"])
    if k == "rr":
        v = Fr(r, tot) * Fr(r - 1, tot - 1)
        return M("Un’urna contiene %d palline rosse e %d bianche. Si estraggono due palline senza reimmissione. Qual è la probabilità che siano entrambe rosse?" % (r, b), fq(v), [fq(x) for x in PW(Fr(r, tot) ** 2, Fr(r - 1, tot - 1), Fr(r * (r - 1), tot * tot)) if x != v],
                     "P(R<sub>1</sub>) · P(R<sub>2</sub>|R<sub>1</sub>) = %d/%d · %d/%d = <b>%s</b>." % (r, tot, r - 1, tot - 1, fq(v)))
    if k == "rb":
        v = Fr(r, tot) * Fr(b, tot - 1) + Fr(b, tot) * Fr(r, tot - 1)
        return M("Un’urna contiene %d palline rosse e %d bianche. Si estraggono due palline senza reimmissione. Qual è la probabilità che siano di colori diversi?" % (r, b), fq(v), [fq(x) for x in PW(Fr(r, tot) * Fr(b, tot - 1), 2 * Fr(r * b, tot * tot), Fr(1, 2) if v != Fr(1, 2) else Fr(1, 3)) if x != v],
                     "Due casi: (R, B) oppure (B, R): %d/%d · %d/%d + %d/%d · %d/%d = <b>%s</b>." % (r, tot, b, tot - 1, b, tot, r, tot - 1, fq(v)))
    v = Fr(r, tot)
    return M("Un’urna contiene %d palline rosse e %d bianche. Si estraggono due palline senza reimmissione, senza guardare la prima. Qual è la probabilità che la seconda sia rossa?" % (r, b), fq(v), [fq(x) for x in PW(Fr(r - 1, tot - 1), Fr(r, tot - 1), Fr(r * (r - 1), tot * (tot - 1))) if x != v],
             "Probabilità totali: %d/%d · %d/%d + %d/%d · %d/%d = <b>%s</b> (come per la prima estrazione)." % (r, tot, r - 1, tot - 1, b, tot, r, tot - 1, fq(v)))


def s4_tot():
    pa = Fr(R.choice([1, 2, 3, 4, 6]), 10)
    pba, pbna = Fr(R.randint(5, 9), 10), Fr(R.randint(1, 4), 10)
    v = pa * pba + (1 - pa) * pbna
    k = R.choice(["urne", "macchine", "meteo"])
    if k == "urne":
        q = "Si sceglie l’urna A con probabilità %s (altrimenti l’urna Ā). La probabilità di estrarre una pallina bianca (B) è %s dall’urna A e %s dall’altra. Qual è la probabilità di estrarre una pallina bianca?" % (d(pa), d(pba), d(pbna))
    elif k == "macchine":
        q = "Una macchina A produce %s dei pezzi, la macchina Ā il resto. I pezzi buoni (B) sono %s per A e %s per Ā. Qual è la probabilità che un pezzo a caso sia buono?" % (il(pa * 100), il(pba * 100), il(pbna * 100))
    else:
        q = "La probabilità che domani piova (A) è %s. Se piove, Luca prende l’autobus (B) con probabilità %s; se non piove, con probabilità %s. Qual è la probabilità che prenda l’autobus?" % (d(pa), d(pba), d(pbna))
    fig = albero(pa, pba, pbna, fmt=d)
    return M("%s%s" % (fig, q), d(v), [d(x) for x in PW(pa * pba, (pba + pbna) / 2, pba + pbna if pba + pbna < 1 else None, pa * pba + pbna) if x != v],
             "Probabilità totali: P(B) = P(A)P(B|A) + P(Ā)P(B|Ā) = %s · %s + %s · %s = <b>%s</b>." % (d(pa), d(pba), d(1 - pa), d(pbna), d(v)))


def s5_bayes():
    k = R.choice(["test", "macch"])
    if k == "test":
        prev = Fr(R.choice([1, 2, 5, 10]), 100)
        sens = Fr(R.choice([90, 95, 99]), 100)
        fp = Fr(R.choice([5, 10, 2]), 100)
        num = prev * sens
        den = num + (1 - prev) * fp
        v = num / den
        q = "Una malattia colpisce %s della popolazione. Un test è positivo nel %d%% dei malati e nel %d%% dei sani (falsi positivi). Una persona risulta positiva: qual è la probabilità che sia malata?" % (il(prev * 100), sens * 100, fp * 100)
        w = [sens, prev, 1 - fp, num]
        e = "Bayes: P(M|+) = P(M)P(+|M) / P(+) = %s / (%s + %s) = <b>%s</b> (≈ %s%%): molto meno di %d%%!" % (d(num), d(num), d((1 - prev) * fp), fq(v), d(Fr(round(float(v) * 1000), 10)), sens * 100)
        return M(q, fq(v), [fq(x) for x in PW(*w) if x != v], e)
    pa = Fr(R.choice([3, 4, 6, 7]), 10)
    da, db = Fr(R.randint(1, 5), 100), Fr(R.randint(1, 5), 100)
    num = pa * da
    v = num / (num + (1 - pa) * db)
    q = "La macchina A produce %s dei pezzi e la macchina B il resto. Sono difettosi %s dei pezzi di A e %s di quelli di B. Un pezzo è difettoso: qual è la probabilità che venga da A?" % (il(pa * 100), il(da * 100), il(db * 100))
    return M(q, fq(v), [fq(x) for x in PW(pa, da, num, da / (da + db)) if x != v],
             "P(A|D) = P(A)P(D|A) / [P(A)P(D|A) + P(B)P(D|B)] = %s / (%s + %s) = <b>%s</b>." % (d(num), d(num), d((1 - pa) * db), fq(v)))


def main():
    seen = set()
    sets = [
        ("Probabilità condizionata", mix(R, seen, [(s1_form, 10), (s2_tab, 10)])),
        ("Eventi indipendenti ed estrazioni", mix(R, seen, [(s3_indip, 8), (s3_estr, 12)])),
        ("Tabelle a doppia entrata", mix(R, seen, [(s2_tab, 12), (s1_form, 8)])),
        ("Probabilità totali", mix(R, seen, [(s4_tot, 16), (s3_estr, 4)])),
        ("Teorema di Bayes", mix(R, seen, [(s5_bayes, 14), (s4_tot, 6)])),
    ]
    body = L(["La <b>probabilità condizionata</b> P(A|B) è la probabilità di A sapendo che B si è verificato: P(A|B) = P(A ∩ B) / P(B). In una tabella si guarda solo la riga (o colonna) di B.",
              "<b>Teorema del prodotto</b>: P(A ∩ B) = P(A) · P(B|A). A e B sono <b>indipendenti</b> se P(A|B) = P(A), cioè P(A ∩ B) = P(A) · P(B).",
              "<b>Probabilità totali</b>: se A e Ā dividono i casi, P(B) = P(A)P(B|A) + P(Ā)P(B|Ā). Nel diagramma ad albero si moltiplica lungo i rami e si sommano i percorsi.",
              "<b>Teorema di Bayes</b>: P(A|B) = P(A)P(B|A) / P(B). Permette di «tornare indietro» dall’effetto alla causa."],
             [("P(B) = 0,4, P(A ∩ B) = 0,1", ["0,1 / 0,4"], "P(A|B) = 1/4"),
              ("Malattia 1%, test positivo 99% malati, 5% sani", ["P(+) = 0,0099 + 0,0495", "0,0099 / 0,0594"], "P(M|+) = 1/6")],
             [["P(A|B) = P(B|A)", "Sono diverse: «malato se positivo» non è «positivo se malato»."],
              ["Dividere per il totale generale", "Nella condizionata si divide per i casi di B."],
              ["Sommare lungo i rami", "Lungo un ramo si moltiplica; si sommano i rami diversi."]])
    faq = [("Perché un test molto preciso può dare tanti falsi allarmi?", "Se la malattia è rara, i sani sono moltissimi: anche una piccola percentuale di falsi positivi tra loro supera i veri positivi. Il teorema di Bayes lo mostra."),
           ("Eventi indipendenti e incompatibili sono la stessa cosa?", "No. Incompatibili: non possono accadere insieme. Indipendenti: il verificarsi di uno non cambia la probabilità dell’altro. Due eventi incompatibili con probabilità positive non sono mai indipendenti.")]
    unit(G, R, "probabilita-condizionata-e-bayes", "Q",
         "Probabilità condizionata e composta, formula di Bayes e sue applicazioni",
         "Probabilità condizionata e teorema di Bayes", "Probabilità condizionata e Bayes",
         "Schede di matematica per la quarta liceo sulla probabilità condizionata: formula e tabelle a doppia entrata, teorema del prodotto, eventi indipendenti, estrazioni senza reimmissione, probabilità totali, teorema di Bayes. 100 esercizi con soluzioni.",
         "P(A|B) = P(A ∩ B) / P(B)", "Bayes: P(A|B) = P(A) · P(B|A) / P(B).",
         body, faq, sets, 11)


if __name__ == "__main__":
    main()
