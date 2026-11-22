# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Gli insiemi (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m1_insiemi.py
Insiemi e rappresentazioni (elencazione, caratteristica, Venn), appartenenza ∈ ∉, sottoinsiemi ⊂, insieme vuoto,
unione ∪, intersezione ∩, differenza, numero degli elementi, problemi con i diagrammi di Venn.
Errori: contare due volte gli elementi comuni, confondere ∪ e ∩, scrivere un elemento più volte.
"""
import random
from it_media import M, L, unit, mix, table, W
import gen_it_matematica_c3_dati_e_probabilita as D3

R = random.Random(71101)
G = "prima-media"


def S(xs):
    xs = sorted(xs)
    return "{%s}" % "; ".join(map(str, xs)) if xs else "∅"


def two():
    U = list(range(1, 21))
    A = set(R.sample(U, R.randint(4, 7)))
    B = set(R.sample(U, R.randint(4, 7)))
    if not A & B or A == B or A <= B or B <= A:
        return None
    return A, B


def s1_appartiene():
    k = R.choice(["pari", "div3", "primi", "lettere", "mesi"])
    if k == "pari":
        A, name = {x for x in range(1, 20) if x % 2 == 0}, "dei numeri pari minori di 20"
    elif k == "div3":
        A, name = {x for x in range(1, 31) if x % 3 == 0}, "dei multipli di 3 minori di 31"
    elif k == "primi":
        A, name = {2, 3, 5, 7, 11, 13, 17, 19}, "dei numeri primi minori di 20"
    elif k == "lettere":
        A, name = set("aeiou"), "delle vocali"
    else:
        A, name = {"aprile", "giugno", "settembre", "novembre"}, "dei mesi con 30 giorni"
    if k in ("lettere", "mesi"):
        pool = list("aeioubcdfg") if k == "lettere" else ["aprile", "giugno", "settembre", "novembre", "marzo", "maggio", "agosto", "dicembre", "febbraio"]
    else:
        pool = list(range(1, 31))
    x = R.choice(pool)
    ok = x in A
    sym = "∈" if ok else "∉"
    return M("Sia A l’insieme %s. Quale scrittura è giusta per «%s»?" % (name, x), "%s %s A" % (x, sym), ["%s %s A" % (x, "∉" if ok else "∈"), "%s ⊂ A" % x, "A %s %s" % (sym, x)],
             "%s %s nell’insieme: <b>%s %s A</b>." % (x, "sta" if ok else "non sta", x, sym))


def s1_caratteristica():
    k = R.choice([("{2; 4; 6; 8}", "numeri pari compresi tra 1 e 9"), ("{1; 3; 5; 7; 9}", "numeri dispari minori di 10"), ("{5; 10; 15; 20}", "multipli di 5 compresi tra 1 e 20"),
                  ("{1; 2; 3; 6}", "divisori di 6"), ("{2; 3; 5; 7}", "numeri primi minori di 10"), ("{1; 4; 9; 16}", "quadrati dei numeri da 1 a 4"),
                  ("{1; 2; 4; 8; 16}", "divisori di 16"), ("{11; 13; 17; 19}", "numeri primi compresi tra 10 e 20"), ("{10; 20; 30; 40}", "multipli di 10 compresi tra 1 e 40")])
    s, c = k
    others = [y for x, y in [("", "numeri pari compresi tra 1 e 9"), ("", "numeri dispari minori di 10"), ("", "multipli di 5 compresi tra 1 e 20"), ("", "divisori di 6"), ("", "numeri primi minori di 10"),
                             ("", "quadrati dei numeri da 1 a 4"), ("", "divisori di 16"), ("", "numeri primi compresi tra 10 e 20"), ("", "multipli di 10 compresi tra 1 e 40")] if y != c]
    R.shuffle(others)
    return M("Quale proprietà caratteristica descrive l’insieme %s?" % s, "i " + c, ["i " + o for o in others[:3]], "Gli elementi sono proprio i %s: <b>i %s</b>." % (c, c))


def s2_op():
    t = two()
    if not t:
        return None
    A, B = t
    k = R.choice(["u", "i", "d", "n"])
    if k == "u":
        r = A | B
        return M("A = %s, B = %s. Qual è A ∪ B?" % (S(A), S(B)), S(r), W(S(A & B), S(A - B), S(r - {min(A & B)}), S(A)),
                 "L’unione contiene tutti gli elementi di A o di B, scritti una sola volta: <b>%s</b>." % S(r))
    if k == "i":
        r = A & B
        return M("A = %s, B = %s. Qual è A ∩ B?" % (S(A), S(B)), S(r), W(S(A | B), S(A - B), S(B - A), "∅"),
                 "L’intersezione contiene solo gli elementi comuni: <b>%s</b>." % S(r))
    if k == "d":
        r = A - B
        return M("A = %s, B = %s. Qual è A − B (elementi di A che non sono in B)?" % (S(A), S(B)), S(r), W(S(B - A), S(A & B), S(A | B)),
                 "Togli da A gli elementi che sono anche in B: <b>%s</b>." % S(r))
    r = len(A | B)
    return M("A = %s, B = %s. Quanti elementi ha A ∪ B?" % (S(A), S(B)), str(r), W(len(A) + len(B), len(A & B), r + 1, r - 1),
             "%d + %d − %d (comuni contati una volta) = <b>%d</b>." % (len(A), len(B), len(A & B), r))


def s3_sotto():
    k = R.choice(["sub", "sub", "vuoto", "quanti"])
    if k == "sub":
        A = set(R.sample(range(1, 13), 6))
        B = set(R.sample(sorted(A), 3)) if R.random() < 0.5 else set(R.sample(sorted(A), 2)) | {R.choice([x for x in range(1, 13) if x not in A])}
        ok = B <= A
        return M("A = %s e B = %s. B è un sottoinsieme di A?" % (S(A), S(B)), "sì, B ⊂ A" if ok else "no, B ⊄ A",
                 ["no, B ⊄ A" if ok else "sì, B ⊂ A", "sì, A ⊂ B", "solo se hanno lo stesso numero di elementi"],
                 "%s: <b>%s</b>." % ("Ogni elemento di B sta in A" if ok else "Non tutti gli elementi di B stanno in A", "B ⊂ A" if ok else "B ⊄ A"))
    if k == "vuoto":
        q, a, w = R.choice([("L’insieme dei numeri pari compresi tra 2 e 4 (esclusi)", "è vuoto", ["ha un elemento", "ha due elementi", "è infinito"]),
                            ("L’insieme dei mesi con 32 giorni", "è vuoto", ["ha 1 elemento", "ha 12 elementi", "è infinito"]),
                            ("L’insieme dei numeri naturali pari", "è infinito", ["è vuoto", "ha 10 elementi", "ha 50 elementi"]),
                            ("L’insieme dei giorni della settimana che cominciano con «m»", "ha 2 elementi", ["è vuoto", "ha 1 elemento", "ha 3 elementi"]),
                            ("L’insieme delle vocali della parola «mare»", "ha 2 elementi", ["ha 4 elementi", "ha 1 elemento", "è vuoto"]),
                            ("L’insieme dei numeri primi pari", "ha 1 elemento", ["è vuoto", "è infinito", "ha 2 elementi"])])
        return M(q + "…", a, w, "Risposta: <b>%s</b>." % a)
    n = R.randint(2, 4)
    return M("Quanti sottoinsiemi ha un insieme di %d elementi (contando anche l’insieme vuoto e l’insieme stesso)?" % n, str(2 ** n), W(n, 2 * n, n * n if n * n != 2 ** n else n + 1, 2 ** n - 1),
             "Ogni elemento può esserci o non esserci: 2 per %d volte = <b>%d</b>." % (n, 2 ** n))


def s4_venn():
    return D3.s3_venn()


def s5():
    a, b = R.randint(8, 20), R.randint(6, 18)
    c = R.randint(2, min(a, b) - 1)
    tot = a + b - c + R.randint(0, 5)
    k = R.choice(["entrambi", "almeno", "solo", "nessuno"])
    s1, s2, v = R.choice([("calcio", "nuoto", "praticano"), ("inglese", "francese", "studiano"), ("pianoforte", "chitarra", "suonano"), ("il cinema", "il teatro", "amano"), ("le mele", "le pere", "amano")])
    base = ("In una classe di %d ragazzi, %d %s %s, %d %s e %d entrambi." % (tot, a, v, s1, b, s2, c) if k != "entrambi" else
            "In una classe di %d ragazzi, %d %s %s, %d %s; %d nessuno dei due." % (tot, a, v, s1, b, s2, tot - (a + b - c)))
    if k == "entrambi":
        return M(base + " Quanti %s entrambi?" % v, str(c), W(a + b - tot, a + b, tot - a, c + 1),
                 "Almeno uno dei due: %d − %d = %d. Entrambi: %d + %d − %d = <b>%d</b>." % (tot, tot - (a + b - c), a + b - c, a, b, a + b - c, c))
    if k == "almeno":
        return M(base + " Quanti fanno almeno una delle due cose?", str(a + b - c), W(a + b, tot, a + b - 2 * c, c), "%d + %d − %d = <b>%d</b> (i comuni si contano una volta)." % (a, b, c, a + b - c))
    if k == "solo":
        return M(base + " Quanti fanno solo %s?" % s1, str(a - c), W(a, a + b - c, b - c, c), "%d − %d = <b>%d</b>." % (a, c, a - c))
    return M(base + " Quanti non fanno nessuna delle due cose?", str(tot - (a + b - c)), W(tot - a - b, tot - a - b + 2 * c, c, tot - a), "%d − (%d + %d − %d) = <b>%d</b>." % (tot, a, b, c, tot - (a + b - c)))


def main():
    D3.R = R
    seen = set()
    sets = [
        ("Appartenenza e rappresentazioni", mix(R, seen, [(s1_appartiene, 12), (s1_caratteristica, 8)])),
        ("Sottoinsiemi e insieme vuoto", mix(R, seen, [(s3_sotto, 20)])),
        ("Unione, intersezione, differenza", mix(R, seen, [(s2_op, 20)])),
        ("Diagrammi di Venn", mix(R, seen, [(s4_venn, 20)])),
        ("Problemi con gli insiemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["Un <b>insieme</b> è un raggruppamento di elementi per cui si può dire con certezza se un elemento ne fa parte o no. Si rappresenta per <b>elencazione</b> {2; 4; 6}, con la <b>proprietà caratteristica</b> o con un diagramma di <b>Eulero-Venn</b>.",
              "∈ si legge «appartiene», ∉ «non appartiene». B ⊂ A (B è sottoinsieme di A) se ogni elemento di B sta in A. ∅ è l’insieme vuoto.",
              "<b>Unione</b> A ∪ B: elementi di A o di B. <b>Intersezione</b> A ∩ B: elementi comuni. <b>Differenza</b> A − B: elementi di A che non stanno in B.",
              "Numero di elementi dell’unione: n(A) + n(B) − n(A ∩ B)."],
             [("A = {1; 2; 3; 4}, B = {3; 4; 5}", ["A ∪ B = {1; 2; 3; 4; 5}", "A ∩ B = {3; 4}", "A − B = {1; 2}"], "5 elementi nell’unione")],
             [["Contare due volte gli elementi comuni", "Nell’unione ogni elemento si scrive una volta sola."],
              ["Confondere ∪ e ∩", "∪ come una «U» di «unione»: si mette tutto insieme; ∩ prende solo i comuni."],
              ["Scrivere 3 ⊂ A", "Per un elemento si usa ∈: 3 ∈ A; ⊂ è per gli insiemi."]],
             table(["Simbolo", "Significato"], [["∈", "appartiene"], ["∉", "non appartiene"], ["⊂", "è sottoinsieme di"], ["∪", "unione"], ["∩", "intersezione"], ["∅", "insieme vuoto"]]))
    faq = [("Perché si studiano gli insiemi in prima media?", "Servono per ragionare con ordine: classificare, risolvere problemi con i diagrammi di Venn e capire i numeri (naturali, interi, razionali)."),
           ("«Le ragazze simpatiche della classe» è un insieme?", "No in senso matematico: «simpatico» non è un criterio oggettivo, quindi non si può dire con certezza chi ne fa parte.")]
    unit(G, R, "insiemi", "F",
         "Rappresentare insiemi e operare con essi (unione, intersezione, differenza); utilizzare i diagrammi di Eulero-Venn per risolvere problemi",
         "Gli insiemi: unione, intersezione e diagrammi di Venn", "Insiemi",
         "Schede di matematica per la prima media sugli insiemi: elencazione e proprietà caratteristica, appartenenza, sottoinsiemi, insieme vuoto, unione, intersezione, differenza, diagrammi di Venn e problemi. 100 esercizi con soluzioni.",
         "Unione: tutto insieme. Intersezione: solo i comuni.", "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
