# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Insiemi e logica (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l1_insiemi_e_logica.py
Rappresentazione per elencazione e per caratteristica, cardinalità, sottoinsiemi e insieme delle parti, unione, intersezione,
differenza, complementare, prodotto cartesiano, problemi con i diagrammi di Venn; proposizioni, connettivi (non, e, o, se… allora),
tavole di verità, leggi di De Morgan, quantificatori e loro negazione.
Errori: 0 ∉ ℕ, contare due volte gli elementi comuni, confondere A × B con B × A, negare «tutti» con «nessuno».
"""
import random
from it_liceo import M, L, unit, mix, table, W, fq

R = random.Random(72101)
G = "prima-liceo"


def S(xs):
    xs = sorted(xs)
    return "{" + ", ".join(fq(x) for x in xs) + "}" if xs else "∅"


def rset(lo=0, hi=12, k=None):
    k = k or R.randint(3, 6)
    return set(R.sample(range(lo, hi + 1), k))


CAR = [
    ("x ∈ ℕ | x &lt; %d", lambda n: set(range(0, n)), (3, 7)),
    ("x ∈ ℕ | x ≤ %d", lambda n: set(range(0, n + 1)), (2, 6)),
    ("x ∈ ℕ | 1 ≤ x ≤ %d", lambda n: set(range(1, n + 1)), (3, 7)),
    ("x ∈ ℤ | −%d ≤ x ≤ 1", lambda n: set(range(-n, 2)), (1, 4)),
    ("x ∈ ℤ | |x| ≤ %d", lambda n: set(range(-n, n + 1)), (1, 3)),
    ("x ∈ ℕ | x è un divisore di %d", lambda n: set(k for k in range(1, n + 1) if n % k == 0), (6, 30)),
    ("x = 2n, n ∈ ℕ, n &lt; %d", lambda n: set(2 * k for k in range(n)), (3, 6)),
    ("x ∈ ℕ | x è un numero primo minore di %d", lambda n: set(k for k in range(2, n) if all(k % p for p in range(2, k))), (8, 20)),
]


def s1_elenca():
    f, g, (lo, hi) = R.choice(CAR)
    n = R.randint(lo, hi)
    A = g(n)
    if len(A) < 2 or len(A) > 8:
        return None
    w = [S(A - {min(A)}), S(A | {max(A) + 1}) if "primo" not in f else S(A | {1}), S(A - {max(A)}), S(A | {min(A) - 1}) if min(A) > 0 or "ℤ" in f else S(A | {0}) if 0 not in A else None]
    return M("Scrivi per elencazione l’insieme A = {%s}." % (f % n), S(A), W(*w), "Gli elementi che verificano la proprietà sono: A = <b>%s</b>." % S(A))


def s1_card():
    f, g, (lo, hi) = R.choice(CAR)
    n = R.randint(lo, hi)
    A = g(n)
    if not 2 <= len(A) <= 10:
        return None
    c = len(A)
    return M("Quanti elementi ha l’insieme A = {%s}?" % (f % n), str(c), W(c - 1, c + 1, c + 2), "A = %s: la cardinalità è |A| = <b>%d</b>." % (S(A), c))


def s1_parti():
    n = R.randint(2, 6)
    A = sorted(R.sample("abcdefg", n))
    c = 2 ** n
    q = R.choice(["Quanti sono i sottoinsiemi di A = {%s} (compresi ∅ e A)?", "Quanti elementi ha l’insieme delle parti 𝒫(A), con A = {%s}?"]) % ", ".join(A)
    return M(q, str(c), W(2 * n, c - 1, n * n if n * n != c else c + 2, c // 2), "Con %d elementi i sottoinsiemi sono 2<sup>%d</sup> = <b>%d</b> (∅ e A compresi)." % (n, n, c))


def s2_op():
    A, B = rset(), rset()
    if not (A & B) or A == B or A <= B or B <= A:
        return None
    op = R.choice(["∪", "∩", "−", "−r"])
    if op == "∪":
        a, w, nm = A | B, [A & B, A ^ B, A - B], "l’unione: gli elementi di A o di B (presi una volta)"
    elif op == "∩":
        a, w, nm = A & B, [A | B, A - B, B - A], "l’intersezione: gli elementi comuni"
    elif op == "−":
        a, w, nm = A - B, [B - A, A & B, A ^ B], "la differenza A − B: gli elementi di A che non stanno in B"
    else:
        a, w, nm = B - A, [A - B, A & B, A | B], "la differenza B − A: gli elementi di B che non stanno in A"
    o = "B − A" if op == "−r" else "A %s B" % op
    return M("A = %s, B = %s. Trova %s." % (S(A), S(B), o), S(a), W(*[S(x) for x in w if x != a]), "È %s: %s = <b>%s</b>." % (nm, o, S(a)))


def s2_compl():
    U = set(range(1, R.randint(8, 12) + 1))
    A = set(R.sample(sorted(U), R.randint(3, 6)))
    a = U - A
    w = [A, set(sorted(a)[1:]) if len(a) > 1 else None, a | {min(A)}, U]
    return M("U = {1, 2, …, %d} è l’insieme universo e A = %s. Trova il complementare di A rispetto a U." % (max(U), S(A)), S(a), W(*[S(x) for x in w if x is not None and x != a]),
             "Il complementare contiene gli elementi di U che non stanno in A: <b>%s</b>." % S(a))


def s2_venn():
    tot = R.choice([24, 25, 28, 30, 32])
    both = R.randint(3, 8)
    a = R.randint(both + 4, tot - 6)
    b = R.randint(both + 3, tot - a + both - 1)
    nessuno = tot - (a + b - both)
    if nessuno < 0:
        return None
    vb, x1, x2, act = R.choice([("giocano", "a calcio", "a pallavolo", ""), ("studiano", "il tedesco", "lo spagnolo", "studiano"),
                                ("suonano", "il pianoforte", "la chitarra", "suonano"), ("fanno", "nuoto", "atletica", "fanno")])
    k = R.choice(["solo", "nessuno", "almeno"])
    if k == "solo":
        ans, w, q = a - both, [a, a + both, b - both], "Quanti %s solo %s?" % (vb, x1)
        e = "Solo %s: %d − %d = <b>%d</b> (tolgo chi %s)." % (x1, a, both, a - both, {"giocano": "gioca a tutti e due gli sport", "studiano": "studia entrambe le lingue", "suonano": "suona entrambi gli strumenti", "fanno": "fa entrambe le attività"}[vb])
    elif k == "almeno":
        ans, w, q = a + b - both, [a + b, a + b - 2 * both, tot - both, tot], {"giocano": "Quanti giocano ad almeno uno dei due sport?", "studiano": "Quanti studiano almeno una delle due lingue?", "suonano": "Quanti suonano almeno uno dei due strumenti?", "fanno": "Quanti fanno almeno una delle due attività?"}[vb]
        e = "|A ∪ B| = |A| + |B| − |A ∩ B| = %d + %d − %d = <b>%d</b>." % (a, b, both, a + b - both)
    else:
        ans, w, q = nessuno, [tot - a - b if tot - a - b >= 0 else None, tot - both, tot - (a + b - 2 * both), both, tot - a], "Quanti non %s né %s né %s?" % (vb, x1, x2.replace("a pallavolo", "pallavolo") if False else x2)
        e = "Almeno uno: %d + %d − %d = %d; nessuno dei due: %d − %d = <b>%d</b>." % (a, b, both, a + b - both, tot, a + b - both, nessuno)
    return M("In una classe di %d studenti, %d %s %s, %d %s e %d entrambi. %s" % (tot, a, vb, x1, b, x2, both, q), str(ans), W(*w), e)


def s3_cart():
    A = sorted(R.sample([1, 2, 3, 4, 5], R.randint(2, 3)))
    B = sorted(R.sample("abcd", R.randint(2, 3)))
    k = R.choice(["card", "el", "no"])
    if k == "card":
        c = len(A) * len(B)
        return M("A = {%s}, B = {%s}. Quanti elementi ha A × B?" % (", ".join(map(str, A)), ", ".join(B)), str(c), W(len(A) + len(B), c * 2, c - 1, c + 1, 2 ** (len(A) * len(B)) if len(A) * len(B) < 7 else None),
                 "|A × B| = |A| · |B| = %d · %d = <b>%d</b>." % (len(A), len(B), c))
    x, y = R.choice(A), R.choice(B)
    if k == "el":
        return M("A = {%s}, B = {%s}. Quale coppia appartiene ad A × B?" % (", ".join(map(str, A)), ", ".join(B)), "(%d; %s)" % (x, y),
                 ["(%s; %d)" % (y, x), "(%s; %s)" % (B[0], B[1]), "(%d; %d)" % (A[0], A[1])],
                 "In A × B il primo elemento viene da A e il secondo da B: <b>(%d; %s)</b>." % (x, y))
    return M("A = {%s}, B = {%s}. Quale coppia appartiene a B × A?" % (", ".join(map(str, A)), ", ".join(B)), "(%s; %d)" % (y, x),
             ["(%d; %s)" % (x, y), "(%s; %s)" % (B[0], B[-1]), "(%d; %d)" % (A[0], A[-1])],
             "In B × A il primo elemento viene da B: <b>(%s; %d)</b>. B × A è diverso da A × B." % (y, x))


PROPS = [("Roma è la capitale d’Italia", True), ("7 è un numero pari", False), ("Il triangolo ha tre lati", True), ("2 + 3 = 6", False),
         ("Ogni quadrato è un rettangolo", True), ("9 è un numero primo", False), ("Il Po è un fiume", True), ("Il numero 15 è divisibile per 4", False),
         ("Un anno ha 12 mesi", True), ("La somma degli angoli interni di un triangolo è 360°", False), ("√16 = 4", True), ("Lo zero è un numero negativo", False)]
NOPROP = ["Che ore sono?", "Chiudi la finestra!", "Questo film è bello", "x + 2 = 5", "Studia matematica!", "Che bella giornata!", "Il blu è il colore più elegante", "Quanti anni hai?"]


def s3_prop():
    if R.random() < 0.45:
        t = R.choice(NOPROP)
        return M("«%s» è una proposizione logica?" % t, "no", ["sì, vera", "sì, falsa", "sì, ma solo a volte"],
                 "Una proposizione è un enunciato di cui si può dire con certezza se è vero o falso. Domande, ordini, giudizi personali ed enunciati aperti non lo sono: <b>no</b>.")
    t, v = R.choice(PROPS)
    a = "sì, vera" if v else "sì, falsa"
    return M("«%s» è una proposizione logica?" % t, a, ["sì, falsa" if v else "sì, vera", "no", "dipende da chi la legge"],
             "Si può stabilire se è vera o falsa, quindi è una proposizione: <b>%s</b>." % a)


def V(b):
    return "V" if b else "F"


CONN = [("p ∧ q", lambda p, q: p and q, "∧ (e) è vera solo se sono vere entrambe"),
        ("p ∨ q", lambda p, q: p or q, "∨ (o) è falsa solo se sono false entrambe"),
        ("¬p ∧ q", lambda p, q: (not p) and q, "prima nego p, poi applico ∧"),
        ("p ∨ ¬q", lambda p, q: p or not q, "prima nego q, poi applico ∨"),
        ("p → q", lambda p, q: (not p) or q, "→ (se… allora) è falsa solo se p è vera e q è falsa"),
        ("¬(p ∧ q)", lambda p, q: not (p and q), "calcolo p ∧ q e poi nego"),
        ("¬(p ∨ q)", lambda p, q: not (p or q), "calcolo p ∨ q e poi nego"),
        ("p ↔ q", lambda p, q: p == q, "↔ è vera quando p e q hanno lo stesso valore"),
        ("q → p", lambda p, q: (not q) or p, "→ è falsa solo se l’antecedente (q) è vero e il conseguente (p) è falso"),
        ("¬p ∨ ¬q", lambda p, q: (not p) or (not q), "nego p e q, poi applico ∨")]


def s4_val():
    f, g, why = R.choice(CONN)
    p, q = R.choice([True, False]), R.choice([True, False])
    v = g(p, q)
    return M("p è %s e q è %s. Che valore di verità ha %s?" % ("vera" if p else "falsa", "vera" if q else "falsa", f), "vero" if v else "falso",
             ["falso" if v else "vero", "non si può stabilire", "vero solo se p = q"], "%s: con p = %s e q = %s risulta <b>%s</b>." % (why[0].upper() + why[1:], V(p), V(q), "vero" if v else "falso"))


def s4_righe():
    n = R.randint(2, 5)
    c = 2 ** n
    return M("Quante righe ha la tavola di verità di una proposizione composta con %d proposizioni elementari diverse?" % n, str(c), W(2 * n, c * 2, n + 1, n * n, c - 1),
             "Ogni proposizione può essere V o F: 2<sup>%d</sup> = <b>%d</b> righe." % (n, c))


SOGG = [("gli studenti della classe hanno superato la verifica", "uno studente della classe", "ha superato la verifica", "nessuno studente della classe"),
        ("i numeri primi sono dispari", "un numero primo", "è dispari", "nessun numero primo"),
        ("i quadrilateri hanno le diagonali uguali", "un quadrilatero", "ha le diagonali uguali", "nessun quadrilatero"),
        ("i gatti del cortile sono neri", "un gatto del cortile", "è nero", "nessun gatto del cortile"),
        ("le auto del parcheggio sono rosse", "un’auto del parcheggio", "è rossa", "nessuna auto del parcheggio"),
        ("i triangoli sono isosceli", "un triangolo", "è isoscele", "nessun triangolo"),
        ("i libri dello scaffale sono in italiano", "un libro dello scaffale", "è in italiano", "nessun libro dello scaffale")]


def s5_neg():
    tutti, sing, pr, nes = R.choice(SOGG)
    if R.random() < 0.5:
        return M("Qual è la negazione di «Tutti %s»?" % tutti, "Esiste almeno %s che non %s" % (sing, pr),
                 ["%s %s" % (nes[0].upper() + nes[1:], pr), "Esiste almeno %s che %s" % (sing, pr), "Non esiste %s che non %s" % (sing, pr)],
                 "La negazione di «per ogni x vale P» è «esiste almeno un x per cui P non vale». Basta un controesempio: <b>esiste almeno %s che non %s</b>." % (sing, pr))
    return M("Qual è la negazione di «Esiste almeno %s che %s»?" % (sing, pr), "%s %s" % (nes[0].upper() + nes[1:], pr),
             ["Esiste almeno %s che non %s" % (sing, pr), "Tutti %s" % tutti, "Non tutti %s" % tutti],
             "Negare «esiste almeno uno che…» vuol dire che non ce n’è nessuno: <b>%s %s</b>." % (nes, pr))


DM = [("¬(p ∧ q)", "¬p ∨ ¬q", ["¬p ∧ ¬q", "p ∨ q", "¬p ∧ q"]), ("¬(p ∨ q)", "¬p ∧ ¬q", ["¬p ∨ ¬q", "p ∧ q", "¬p ∨ q"]),
      ("¬(¬p)", "p", ["¬p", "p ∧ ¬p", "p ∨ ¬p"]), ("¬(p ∧ ¬q)", "¬p ∨ q", ["¬p ∧ q", "p ∨ ¬q", "¬p ∨ ¬q"]),
      ("¬(¬p ∨ q)", "p ∧ ¬q", ["¬p ∧ q", "p ∨ ¬q", "¬p ∧ ¬q"]), ("p → q", "¬p ∨ q", ["p ∨ ¬q", "¬p ∧ q", "q → p"]),
      ("¬(p → q)", "p ∧ ¬q", ["¬p ∧ q", "¬p → ¬q", "¬p ∨ q"])]
DM_IT = [("«Non è vero che piove e fa freddo»", "Non piove o non fa freddo", ["Non piove e non fa freddo", "Piove o fa freddo", "Piove e non fa freddo"]),
         ("«Non è vero che studio o leggo»", "Non studio e non leggo", ["Non studio o non leggo", "Studio e leggo", "Studio ma non leggo"]),
         ("«Non è vero che Marco è alto e biondo»", "Marco non è alto o non è biondo", ["Marco non è alto e non è biondo", "Marco è basso e moro", "Marco è alto ma non biondo"]),
         ("«Non è vero che prendo il treno o l’autobus»", "Non prendo il treno e non prendo l’autobus", ["Non prendo il treno o non prendo l’autobus", "Prendo il treno e l’autobus", "Prendo solo il treno"])]


def s5_dm():
    if R.random() < 0.6:
        f, a, w = R.choice(DM)
        return M("Quale proposizione è equivalente a %s?" % f, a, w,
                 "Per le leggi di De Morgan (e la doppia negazione) %s equivale a <b>%s</b>: hanno la stessa tavola di verità." % (f, a))
    f, a, w = R.choice(DM_IT)
    return M("Quale frase è la negazione equivalente di %s?" % f, a, w,
             "Leggi di De Morgan: negando «e» si ottiene «o» (e viceversa) e si negano le due parti: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Elencazione, caratteristica, cardinalità", mix(R, seen, [(s1_elenca, 10), (s1_card, 6), (s1_parti, 4)])),
        ("Unione, intersezione, differenza", mix(R, seen, [(s2_op, 14), (s2_compl, 6)])),
        ("Prodotto cartesiano e problemi", mix(R, seen, [(s3_cart, 8), (s2_venn, 12)])),
        ("Proposizioni e connettivi", mix(R, seen, [(s3_prop, 6), (s4_val, 10), (s4_righe, 4)])),
        ("De Morgan e quantificatori", mix(R, seen, [(s5_dm, 8), (s5_neg, 6), (s2_venn, 6)])),
    ]
    body = L(["Un <b>insieme</b> si descrive per <b>elencazione</b> (A = {1, 2, 3}) o con una <b>proprietà caratteristica</b> (A = {x ∈ ℕ | x &lt; 4}). In Italia ℕ contiene lo 0.",
              "<b>Unione</b> A ∪ B: elementi di A o di B. <b>Intersezione</b> A ∩ B: elementi comuni. <b>Differenza</b> A − B: elementi di A che non stanno in B. Un insieme di n elementi ha 2<sup>n</sup> sottoinsiemi.",
              "Per contare: |A ∪ B| = |A| + |B| − |A ∩ B|. Il prodotto cartesiano A × B contiene le coppie (a; b) e ha |A| · |B| elementi.",
              "Una <b>proposizione</b> è vera o falsa. ¬p (non), p ∧ q (e: vera se entrambe vere), p ∨ q (o: falsa se entrambe false), p → q (falsa solo se p vera e q falsa).",
              "<b>De Morgan</b>: ¬(p ∧ q) = ¬p ∨ ¬q e ¬(p ∨ q) = ¬p ∧ ¬q. La negazione di «tutti» è «almeno uno non»."],
             [("A = {1, 2, 3, 4}, B = {3, 4, 5}. Trova A ∪ B e A ∩ B.", ["Unione: tutti gli elementi, una volta.", "Intersezione: solo quelli comuni."], "A ∪ B = {1, 2, 3, 4, 5}; A ∩ B = {3, 4}"),
              ("Su 30 studenti, 18 giocano a calcio, 12 a tennis e 5 a entrambi. Quanti a nessuno?", ["Almeno uno: 18 + 12 − 5 = 25."], "30 − 25 = 5")],
             [["Contare due volte gli elementi comuni", "Nell’unione ogni elemento si scrive una volta: sottrai |A ∩ B|."],
              ["Pensare che A − B = B − A", "A − B toglie da A gli elementi di B: in generale è diverso da B − A."],
              ["Negare «tutti» con «nessuno»", "Basta un controesempio: «esiste almeno uno che non…»."],
              ["Credere p → q falsa quando p è falsa", "Se p è falsa l’implicazione è vera."]],
             table(["p", "q", "p ∧ q", "p ∨ q", "p → q"], [["V", "V", "V", "V", "V"], ["V", "F", "F", "V", "F"], ["F", "V", "F", "V", "V"], ["F", "F", "F", "F", "V"]]))
    faq = [("Lo 0 appartiene a ℕ?", "Sì: nei libri italiani di solito ℕ = {0, 1, 2, 3, …}. ℕ senza lo 0 si indica con ℕ<sub>0</sub> o ℕ*."),
           ("Perché «se piove allora prendo l’ombrello» è vera se non piove?", "L’implicazione p → q è falsa solo quando p è vera e q è falsa. Se p è falsa non c’è nessuna promessa tradita, quindi è vera.")]
    unit(G, R, "insiemi-e-logica", "F",
         "Il linguaggio degli insiemi; operazioni tra insiemi; elementi di logica: proposizioni, connettivi, quantificatori",
         "Insiemi e logica", "Insiemi e logica",
         "Schede di matematica per la prima liceo su insiemi e logica: elencazione e proprietà caratteristica, unione, intersezione, differenza, complementare, prodotto cartesiano, diagrammi di Venn, proposizioni, connettivi, tavole di verità, De Morgan e quantificatori. 100 esercizi con soluzioni.",
         "|A ∪ B| = |A| + |B| − |A ∩ B|", "¬(p ∧ q) = ¬p ∨ ¬q e ¬(p ∨ q) = ¬p ∧ ¬q.",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
