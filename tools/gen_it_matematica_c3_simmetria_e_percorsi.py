# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Simmetria e percorsi (Spazio e figure)
  python3 tools/gen_it_matematica_c3_simmetria_e_percorsi.py
Figure simmetriche, asse di simmetria, lettere simmetriche, completare per simmetria; posizione sulla griglia
(colonna e riga), percorsi descritti a parole, codici di frecce per un robot (semplici programmi).
Errori: specchiare spostando invece di ribaltare, leggere prima la riga e poi la colonna, contare la casella di partenza.
"""
import random
import gen_de_mathe_k3_achsensymmetrie as DE
import gen_fr_maths_ce2_se_reperer_et_se_deplacer as FRP
from it_common import mcq, lesson, make_unit, mix, wrap, text, relabel, GREEN

R = random.Random(70320)
COLS, ROWS, Q = DE.COLS, DE.ROWS, DE.Q
L4 = "ABCD"
FIG = {"la stella": "l’étoile", "il cerchio": "le rond", "il triangolo": "le triangle", "il quadrato": "le carré", "il rombo": "le losange", "il cuore": "le cœur"}
GC, GR = FRP.COLS, FRP.ROWS
LET = FRP.LET


def cell(c):
    return FRP.cell(c)


def griglia(objs, start=None):
    s = FRP.grille({FIG[k]: v for k, v in objs.items()}, start=start)
    return relabel(s, "griglia: colonne da A a F, righe da 1 a 5")


def four(figs):
    s = []
    for i, c in enumerate(figs):
        ox = 10 + i * 112
        s.append(DE.grid(ox, 10, c, True))
        s.append(text(ox + COLS * Q / 2.0, 10 + ROWS * Q + 24, L4[i], 16, col=GREEN))
    return wrap(10 + 4 * 112, 10 + ROWS * Q + 32, "".join(s), "quattro figure A, B, C, D sulla carta a quadretti", lg=True)


def s1():
    hs = [DE.half() for _ in range(4)]
    if not all(hs):
        return None
    good = DE.mirror(hs[0])
    bads = [DE.broken(DE.mirror(hs[1])), DE.shifted(hs[2]), DE.broken(DE.mirror(hs[3]))]
    if not all(bads) or any(b == DE.mirror({(x, y) for x, y in b if x < 3}) for b in bads):
        return None
    figs = bads + [good]
    R.shuffle(figs)
    k = figs.index(good)
    return mcq(four(figs) + "Quale figura è simmetrica rispetto alla linea rossa?", L4[k], [L4[i] for i in range(4) if i != k],
               "Solo nella figura %s i quadretti sono alla stessa distanza dall’asse, da una parte e dall’altra: se pieghi il foglio, le due metà combaciano." % L4[k])


VERT = list("AHIMOTUVWXY")
HORI = list("BCDEHIKOX")
NONE = list("FGJLNPQRSZ")


def s1_lettere():
    kind = R.choice(["v", "v", "h", "n"])
    if kind == "v":
        a, w = R.choice(VERT), R.sample(NONE, 3)
        q = "Quale lettera ha un asse di simmetria <b>verticale</b>: %s?" % ", ".join(sorted([a] + w))
        e = "Se pieghi %s lungo una linea verticale nel mezzo, le due metà combaciano: <b>%s</b>." % (a, a)
    elif kind == "h":
        a, w = R.choice([x for x in HORI if x not in VERT]), R.sample(NONE, 3)
        q = "Quale lettera ha un asse di simmetria <b>orizzontale</b>: %s?" % ", ".join(sorted([a] + w))
        e = "In %s la metà di sopra e quella di sotto combaciano: <b>%s</b>." % (a, a)
    else:
        a, w = R.choice(NONE), R.sample(VERT + [x for x in HORI if x not in VERT], 3)
        q = "Quale lettera <b>non</b> ha assi di simmetria: %s?" % ", ".join(sorted([a] + w))
        e = "%s non ha assi di simmetria; le altre lettere si possono piegare in due metà uguali: <b>%s</b>." % (a, a)
    return mcq(q, a, w, e)


def s2():
    h = DE.half()
    if not h:
        return None
    good = DE.mirror(h)
    sh = DE.shifted(h)
    near = DE.broken(good)
    flipped = set(h) | {(COLS - 1 - x, ROWS - 1 - y) for x, y in h}
    opts = [good, sh, near, flipped]
    if not near or len({frozenset(o) for o in opts}) < 4:
        return None
    pic = wrap(COLS * Q + 20, ROWS * Q + 20, DE.grid(10, 10, h), "metà di una figura e asse di simmetria")
    R.shuffle(opts)
    k = opts.index(good)
    return mcq(pic + "Questa è la metà sinistra di una figura. Quale disegno mostra la figura completata per simmetria?" + four(opts), L4[k], [L4[i] for i in range(4) if i != k],
               "Ogni quadretto va riportato dall’altra parte dell’asse, alla stessa distanza. È il disegno <b>%s</b>." % L4[k])


def qd(n):
    return "%d quadrett%s" % (n, "o" if n == 1 else "i")


def s2_distanza():
    kind = R.choice(["lato", "dist"])
    if kind == "lato":
        n = R.randint(1, 6)
        side, other = R.choice([("a sinistra", "a destra"), ("a destra", "a sinistra")])
        ans = "%s %s dell’asse" % (qd(n), other)
        w = ["%s %s dell’asse" % (qd(n), side), "%s %s dell’asse" % (qd(n + 1), other), "%s %s dell’asse" % (qd(2 * n), other)]
        return mcq("Un punto è a %s %s di un asse di simmetria verticale. Dove si trova il suo simmetrico?" % (qd(n), side), ans, w,
                   "Il simmetrico è alla stessa distanza, dall’altra parte: <b>%s</b>." % ans)
    n = R.randint(1, 7)
    return mcq("Un punto è a %s dall’asse. Quanti quadretti ci sono tra il punto e il suo simmetrico?" % qd(n), qd(2 * n),
               [qd(n), qd(n + 1), qd(2 * n + 2)], "%d fino all’asse e altri %d dall’altra parte: <b>%s</b>." % (n, n, qd(2 * n)))


ASSI = [("un quadrato", "4"), ("un rettangolo (non quadrato)", "2"), ("un triangolo con i 3 lati uguali", "3"), ("un cerchio", "infiniti"),
        ("un cuore", "1"), ("una farfalla", "1"), ("un esagono regolare", "6"), ("la lettera H", "2"), ("la lettera A", "1"), ("la lettera F", "nessuno"),
        ("il numero 8", "2"), ("il numero 3", "1"), ("un rombo (non quadrato)", "2"), ("la lettera X", "2")]


def s3_assi():
    thing, ans = R.choice(ASSI)
    near = {"4": ["2", "8"], "2": ["4", "1"], "3": ["1", "6"], "infiniti": ["1", "4"], "1": ["2", "nessuno"], "6": ["3", "12"], "nessuno": ["1", "2"]}[ans]
    rest = [x for x in ["nessuno", "1", "2", "3", "4", "6", "infiniti"] if x != ans and x not in near]
    R.shuffle(rest)
    return mcq("Quanti assi di simmetria ha %s?" % thing, ans, near + rest,
               "%s ha <b>%s</b> %s di simmetria." % (thing[0].upper() + thing[1:], ans, "asse" if ans in ("1", "nessuno") else "assi"))


def place(n):
    cells = R.sample([(c, r) for c in range(GC) for r in range(GR)], n)
    kinds = R.sample(list(FIG), n)
    return dict(zip(kinds, cells))


def s4_dove():
    objs = place(R.randint(3, 5))
    k = R.choice(list(objs))
    c = objs[k]
    right = cell(c)
    w = ["%d%s" % (c[1] + 1, LET[c[0]]), "%s%d" % (LET[c[1]], c[0] + 1) if c[1] < GC and c[0] + 1 <= GR and (c[1], c[0]) != c else None,
         "%s%d" % (LET[c[0]], GR - c[1]) if GR - c[1] != c[1] + 1 else None, "%s%d" % (LET[(c[0] + 1) % GC], c[1] + 1)]
    return mcq(griglia(objs) + "In quale casella si trova %s?" % k, right, [x for x in w if x and x != right],
               "Leggi prima la lettera della colonna, poi il numero della riga: %s è in <b>%s</b>." % (k, right))


def s4_cosa():
    objs = place(4)
    k = R.choice(list(objs))
    c = objs[k]
    return mcq(griglia(objs) + "Che cosa c’è nella casella %s?" % cell(c), k, [x for x in objs if x != k] + ["niente"],
               "Colonna %s, riga %d: c’è <b>%s</b>." % (LET[c[0]], c[1] + 1, k))


DIRS = {"a destra": (1, 0), "a sinistra": (-1, 0), "in alto": (0, 1), "in basso": (0, -1)}


def ok(c):
    return 0 <= c[0] < GC and 0 <= c[1] < GR


def near(cur):
    return [(cur[0] + dx, cur[1] + dy) for dx, dy in ((1, 0), (0, -1), (-1, 0), (0, 1), (1, 1), (-1, -1))]


def s4_passi():
    st = (R.randint(0, GC - 1), R.randint(0, GR - 1))
    steps, cur = [], st
    for _ in range(R.randint(1, 2)):
        d = R.choice(list(DIRS))
        n = R.randint(1, 4)
        nx = (cur[0] + DIRS[d][0] * n, cur[1] + DIRS[d][1] * n)
        if not ok(nx):
            return None
        steps.append((n, d))
        cur = nx
    if cur == st:
        return None
    n0, d0 = steps[0]
    wrong1 = (st[0] + DIRS[d0][0] * (n0 + 1), st[1] + DIRS[d0][1] * (n0 + 1))
    opp = (st[0] - DIRS[d0][0] * n0, st[1] - DIRS[d0][1] * n0)
    for a, b in steps[1:]:
        wrong1 = (wrong1[0] + DIRS[b][0] * a, wrong1[1] + DIRS[b][1] * a)
        opp = (opp[0] + DIRS[b][0] * a, opp[1] + DIRS[b][1] * a)
    txt = ", poi ".join("di %d %s %s" % (n, "casella" if n == 1 else "caselle", d) for n, d in steps)
    return mcq(griglia({}, start=st) + "Il robot (punto rosso) parte dalla casella %s. Si sposta %s. In quale casella arriva?" % (cell(st), txt),
               cell(cur), [cell(x) for x in [wrong1, opp] + near(cur) if ok(x) and x != cur],
               "Non si conta la casella di partenza. Il robot arriva in <b>%s</b>." % cell(cur))


def s5_codice():
    st = (R.randint(0, GC - 1), R.randint(0, GR - 1))
    code = FRP.rand_code()
    end = FRP.walk(st, code)
    if not end or end == st:
        return None
    flip = {"→": "←", "←": "→", "↑": "↑", "↓": "↓"}
    w1 = FRP.walk(st, [flip[a] for a in code])
    w2 = FRP.walk(st, code[:-1])
    w3 = FRP.walk(st, code + [code[-1]])
    return mcq(griglia({}, start=st) + "Il robot parte da %s ed esegue il programma %s. In quale casella arriva?" % (cell(st), " ".join(code)),
               cell(end), [cell(x) for x in [w1, w2, w3] + near(end) if x and ok(x) and x != end],
               "Ogni freccia è un passo di una casella. Il robot arriva in <b>%s</b>." % cell(end))


def s5_scrivi():
    st = (R.randint(0, GC - 1), R.randint(0, GR - 1))
    code = FRP.rand_code()
    end = FRP.walk(st, code)
    if not end or end == st:
        return None
    k = R.choice(list(FIG))
    dx, dy = end[0] - st[0], end[1] - st[1]
    good = ["→" if dx > 0 else "←"] * abs(dx) + ["↑" if dy > 0 else "↓"] * abs(dy)
    bad1 = ["←" if dx > 0 else "→"] * abs(dx) + ["↑" if dy > 0 else "↓"] * abs(dy)
    bad2 = ["→" if dx > 0 else "←"] * abs(dx) + ["↓" if dy > 0 else "↑"] * abs(dy)
    bad3 = ["→" if dx > 0 else "←"] * (abs(dx) + 1) + ["↑" if dy > 0 else "↓"] * abs(dy)
    if not dx or not dy:
        bad3 = good + [good[-1]]
    opts = [" ".join(x) for x in (good, bad1, bad2, bad3)]
    if len(set(opts)) < 4:
        return None
    art = {"la stella": "alla stella", "il cerchio": "al cerchio", "il triangolo": "al triangolo", "il quadrato": "al quadrato", "il rombo": "al rombo", "il cuore": "al cuore"}[k]
    cs = lambda n: "casella" if n == 1 else "caselle"
    return mcq(griglia({k: end}, start=st) + "Quale programma porta il robot da %s fino %s?" % (cell(st), art), opts[0], opts[1:],
               "Servono %d %s %s e %d %s %s: <b>%s</b>." % (abs(dx), cs(abs(dx)), "a destra" if dx > 0 else "a sinistra", abs(dy), cs(abs(dy)), "in alto" if dy > 0 else "in basso", opts[0]))


def main():
    DE.R = R
    FRP.R = R
    seen = set()
    sets = [
        ("Figure simmetriche", mix(R, seen, [(s1, 10), (s1_lettere, 10)])),
        ("Completare per simmetria", mix(R, seen, [(s2, 10), (s2_distanza, 10)])),
        ("Assi di simmetria e caselle", mix(R, seen, [(s3_assi, 12), (s4_cosa, 8)])),
        ("Posizioni e percorsi sulla griglia", mix(R, seen, [(s4_dove, 10), (s4_passi, 10)])),
        ("Programmi per il robot", mix(R, seen, [(s5_codice, 10), (s5_scrivi, 10)])),
    ]
    body = lesson(
        ["Una figura è <b>simmetrica</b> se, piegandola lungo una linea, le due metà combaciano. Quella linea è l’<b>asse di simmetria</b>.",
         "Per completare una figura per simmetria, ogni punto va riportato dall’altra parte dell’asse, <b>alla stessa distanza</b>.",
         "Sulla griglia ogni casella ha un nome: prima la <b>lettera della colonna</b>, poi il <b>numero della riga</b> (per esempio C4).",
         "Un <b>programma</b> è una sequenza di istruzioni: → ← ↑ ↓ fanno avanzare il robot di una casella. Non si conta la casella di partenza."],
        [("Il robot è in B2 ed esegue → → ↑", ["→ → : da B a D", "↑ : da 2 a 3"], "D3")],
        [["Spostare la figura invece di ribaltarla", "Il quadretto più vicino all’asse resta il più vicino anche dall’altra parte."],
         ["Leggere 4C invece di C4", "Prima la colonna (lettera), poi la riga (numero)."],
         ["Contare la casella di partenza", "Conta solo i passi: la prima casella contata è quella dopo la partenza."]])
    faq = [("Quanti assi di simmetria può avere una figura?", "Dipende: il cuore ne ha 1, il rettangolo 2, il quadrato 4, il cerchio infiniti; alcune figure non ne hanno nessuno."),
           ("Perché si fanno i percorsi con le frecce?", "Sono un primo passo verso il pensiero computazionale: si impara a dare istruzioni precise, una dopo l’altra, come in un programma.")]
    make_unit(R, "simmetria-e-percorsi", "S",
              "Riconoscere figure simmetriche e assi di simmetria; comunicare la posizione di oggetti nello spazio e sul piano quadrettato; eseguire, descrivere e rappresentare percorsi e semplici sequenze di istruzioni (programmi)",
              "Simmetria e percorsi sulla griglia", "Simmetria e percorsi",
              "Schede di matematica per la classe terza su simmetria e percorsi: figure simmetriche, asse di simmetria, completare per simmetria, caselle sulla griglia, percorsi e programmi con le frecce per il robot. 100 esercizi con soluzioni.",
              "Le due metà di una figura simmetrica combaciano.", "Sulla griglia: prima la colonna, poi la riga.",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
