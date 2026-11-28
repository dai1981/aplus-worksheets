# -*- coding: utf-8 -*-
"""Deutschland / Klasse 9（Biologie, Chemie, Physik）"""
from de_sci import H, nq, num

STOFFE = [("Wasser", "H₂O", 18), ("Kohlenstoffdioxid", "CO₂", 44), ("Sauerstoff", "O₂", 32), ("Wasserstoff", "H₂", 2), ("Methan", "CH₄", 16),
          ("Natriumchlorid", "NaCl", 58.5), ("Ammoniak", "NH₃", 17), ("Stickstoff", "N₂", 28), ("Calciumcarbonat", "CaCO₃", 100), ("Natriumhydroxid", "NaOH", 40),
          ("Kohlenstoff", "C", 12), ("Magnesium", "Mg", 24), ("Eisen", "Fe", 56), ("Schwefelsäure", "H₂SO₄", 98), ("Glucose", "C₆H₁₂O₆", 180)]


def f_mol(R):
    k = R.choice(["n", "n", "m", "M", "teilchen", "c"])
    name, f, M = R.choice(STOFFE)
    if k == "n":
        n = R.choice([0.5, 2, 3, 0.25, 4, 0.1, 5, 1.5])
        m = n * M
        return nq("Wie viel Stoffmenge sind %s g %s (%s, M = %s g/mol)?" % (num(m), name, f, num(M)), n, [m * M, M / m, m - M], "mol",
                  "n = m : M = %s g : %s g/mol = %s mol." % (num(m), num(M), num(n)))
    if k == "m":
        n = R.choice([0.5, 2, 3, 0.2, 4, 10, 0.25])
        return nq("Welche Masse haben %s mol %s (%s, M = %s g/mol)?" % (num(n), name, f, num(M)), n * M, [M / n, n + M, n * M * 10], "g",
                  "m = n · M = %s mol · %s g/mol = %s g." % (num(n), num(M), num(n * M)))
    if k == "M":
        return nq("Wie groß ist die molare Masse von %s (%s)? Nutze die Atommassen H = 1, C = 12, N = 14, O = 16, Na = 23, Mg = 24, S = 32, Cl = 35,5, Ca = 40, Fe = 56." % (name, f), M,
                  [M + 16, M - 1 if M > 2 else M + 2, M * 2], "g/mol", "Die molare Masse ist die Summe der Atommassen in g/mol: %s hat %s g/mol." % (f, num(M)))
    if k == "teilchen":
        n = R.choice([2, 3, 0.5, 4, 10, 0.1])
        return ("sci", n)
    V, n = R.choice([(0.5, 1), (2, 0.5), (0.25, 0.5), (1, 2), (0.2, 0.1), (0.1, 0.05), (5, 1)])
    return nq("In %s l Lösung sind %s mol Natriumchlorid gelöst. Wie groß ist die Stoffmengenkonzentration?" % (num(V), num(n)), n / V,
              [V / n, n * V, n / V * 10], "mol/l", "c = n : V = %s mol : %s l = %s mol/l." % (num(n), num(V), num(n / V)))


def f_mol2(R):
    r = f_mol(R)
    if isinstance(r, tuple) and r and r[0] == "sci":
        n = r[1]
        z = n * 6.02
        e = 23
        while z >= 10:
            z /= 10
            e += 1
        while z < 1:
            z *= 10
            e -= 1
        sup = str(e).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
        a = "%s · 10%s" % (num(round(z, 2)), sup)
        w = ["%s · 10%s" % (num(round(z, 2)), str(e - 1).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))),
             "%s · 10%s" % (num(round(z, 2)), str(e + 1).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))), "%s" % num(n * 6.02)]
        from de_sci import it
        return it("Wie viele Teilchen sind in %s mol eines Stoffes enthalten? (1 mol = 6,02 · 10²³ Teilchen)" % num(n), a, w,
                  "N = n · 6,02 · 10²³ = %s mol · 6,02 · 10²³ = %s Teilchen." % (num(n), a))
    return r


def f_ohm(R):
    k = R.choice(["R", "R", "I", "U", "reihe", "parallel"])
    if k == "R":
        U, I = R.choice([(12, 0.5), (230, 0.1), (6, 0.2), (9, 0.3), (4.5, 0.15), (24, 2), (3, 0.06), (230, 2.3)])
        return nq("An einem Widerstand liegen %s V, es fließen %s A. Wie groß ist der Widerstand?" % (num(U), num(I)), U / I, [U * I, I / U, U - I], "Ω",
                  "R = U : I = %s V : %s A = %s Ω." % (num(U), num(I), num(U / I)))
    if k == "I":
        U, Rr = R.choice([(12, 24), (230, 46), (9, 45), (6, 30), (4.5, 9), (24, 120), (230, 1150)])
        return nq("Ein Widerstand von %s Ω liegt an %s V. Wie groß ist die Stromstärke?" % (num(Rr), num(U)), U / Rr, [U * Rr, Rr / U, U + Rr], "A",
                  "I = U : R = %s V : %s Ω = %s A." % (num(U), num(Rr), num(U / Rr)))
    if k == "U":
        Rr, I = R.choice([(50, 0.2), (100, 0.12), (20, 0.5), (470, 0.01), (15, 0.4), (220, 0.05)])
        return nq("Durch einen Widerstand von %s Ω fließen %s A. Welche Spannung liegt an?" % (num(Rr), num(I)), Rr * I, [Rr / I, I / Rr, Rr + I], "V",
                  "U = R · I = %s Ω · %s A = %s V." % (num(Rr), num(I), num(Rr * I)))
    if k == "reihe":
        a, b = R.choice([(10, 20), (30, 60), (47, 53), (100, 150), (12, 18), (5, 15), (220, 330)])
        return nq("Zwei Widerstände (%s Ω und %s Ω) sind in Reihe geschaltet. Wie groß ist der Gesamtwiderstand?" % (num(a), num(b)), a + b, [a * b / (a + b), abs(b - a), a * b], "Ω",
                  "In Reihe addieren sich die Widerstände: %s Ω + %s Ω = %s Ω." % (num(a), num(b), num(a + b)))
    a, b = R.choice([(10, 10), (20, 30), (60, 30), (12, 6), (100, 100), (40, 10), (6, 3)])
    return nq("Zwei Widerstände (%s Ω und %s Ω) sind parallel geschaltet. Wie groß ist der Gesamtwiderstand?" % (num(a), num(b)), a * b / (a + b), [a + b, abs(a - b) or a / 4, (a + b) / 2], "Ω",
              "Parallel gilt: 1/R = 1/%s Ω + 1/%s Ω, also R = %s Ω. Er ist kleiner als der kleinste Einzelwiderstand." % (num(a), num(b), num(a * b / (a + b))))


def f_leistung(R):
    k = R.choice(["P", "P", "I", "E", "kosten", "kosten"])
    if k == "P":
        U, I = R.choice([(230, 2), (230, 0.5), (12, 3), (230, 10), (5, 2), (230, 4), (3.7, 0.5)])
        return nq("Ein Gerät wird mit %s V betrieben, es fließen %s A. Wie groß ist die elektrische Leistung?" % (num(U), num(I)), U * I, [U / I, I / U * 1000, U + I], "W",
                  "P = U · I = %s V · %s A = %s W." % (num(U), num(I), num(U * I)))
    if k == "I":
        P = R.choice([2300, 460, 1150, 690, 23, 920, 2070])
        return nq("Ein Gerät mit %s W hängt an 230 V. Welcher Strom fließt?" % num(P), P / 230, [P * 230, 230 / P, P / 23], "A",
                  "I = P : U = %s W : 230 V = %s A." % (num(P), num(P / 230)))
    if k == "E":
        P, t = R.choice([(2000, 0.5), (100, 10), (1500, 2), (60, 5), (800, 0.25), (10, 8), (3000, 1.5)])
        return nq("Ein Gerät mit %s W läuft %s h. Wie viel elektrische Energie braucht es?" % (num(P), num(t)), P * t / 1000, [P * t, P / t / 1000, P * t / 100], "kWh",
                  "E = P · t = %s kW · %s h = %s kWh." % (num(P / 1000), num(t), num(P * t / 1000)))
    P, t, c = R.choice([(2000, 1, 40), (1000, 3, 30), (500, 4, 35), (2500, 2, 40), (100, 20, 30), (1500, 2, 35), (60, 50, 40), (750, 4, 30)])
    E = P * t / 1000
    return nq("Ein Gerät mit %s W läuft %s h. 1 kWh kostet %d Cent. Was kostet der Strom?" % (num(P), num(t), c), E * c, [P * t * c, E, E * c / 10], "Cent",
              "E = %s kW · %s h = %s kWh; Kosten: %s kWh · %d Cent = %s Cent." % (num(P / 1000), num(t), num(E), num(E), c, num(E * c)))


def UNITS(grade):
    return [
        H("B", "hormone-und-regelung", "Hormone und Regelung", "Hormone",
          "Die Schülerinnen und Schüler beschreiben die Wirkung von Hormonen, die Regelung des Blutzuckerspiegels durch Insulin und Glukagon, Diabetes und den Vergleich von Hormon- und Nervensystem.",
          "Hormondrüsen, Hormone als Botenstoffe, Schlüssel-Schloss-Prinzip, Regelkreis, Blutzuckerregulation, Insulin und Glukagon, Diabetes mellitus, Stresshormone",
          "Hormone sind Botenstoffe, die mit dem Blut wirken", "Insulin senkt den Blutzucker, Glukagon erhöht ihn. So bleibt der Spiegel fast gleich.",
          ["Hormone werden in Hormondrüsen gebildet und mit dem Blut im Körper verteilt. Sie wirken nur an Zellen mit passenden Rezeptoren (Schlüssel-Schloss-Prinzip).",
           "Der Blutzucker wird in einem Regelkreis geregelt: Steigt er nach dem Essen, schüttet die Bauchspeicheldrüse Insulin aus. Sinkt er, bildet sie Glukagon.",
           "Bei Diabetes Typ 1 bildet der Körper kein Insulin mehr. Bei Typ 2 wirkt das Insulin schlechter. Nerven wirken schnell und gezielt, Hormone langsamer und länger."],
          [("Nach einem süßen Frühstück steigt der Blutzucker. Welches Hormon wird ausgeschüttet?", ["Der Blutzucker soll wieder sinken.", "Insulin senkt den Blutzucker."], "Insulin")],
          [("Insulin erhöht den Blutzucker.", "Insulin senkt ihn, Glukagon erhöht ihn."), ("Hormone wirken auf alle Zellen.", "Sie wirken nur an Zellen mit passenden Rezeptoren."),
           ("Hormone werden über Nerven geleitet.", "Hormone werden mit dem Blut transportiert.")],
          [("Was ist Adrenalin?", "Ein Stresshormon aus dem Nebennierenmark. Es beschleunigt Herzschlag und Atmung und stellt Energie bereit."),
           ("Was ist ein Regelkreis?", "Ein System, das einen Wert misst und Abweichungen ausgleicht, damit er fast gleich bleibt."), ("Was macht die Schilddrüse?", "Ihr Hormon Thyroxin regt den Stoffwechsel an.")],
          [("Drüsen und Hormone", [("Bauchspeicheldrüse", "Insulin und Glukagon"), ("Nebenniere", "Adrenalin"), ("Schilddrüse", "Thyroxin"), ("Hoden", "Testosteron"),
                                   ("Eierstöcke", "Östrogen"), ("Hirnanhangsdrüse", "Wachstumshormon"), ("Zirbeldrüse", "Melatonin")],
            "Welches Hormon bildet: {k}?", "Welche Drüse bildet: {v}?"),
           ("Wirkungen", [("Insulin", "senkt den Blutzucker"), ("Glukagon", "erhöht den Blutzucker"), ("Adrenalin", "beschleunigt den Herzschlag bei Stress"), ("Thyroxin", "regt den Stoffwechsel an"),
                          ("Melatonin", "macht müde und steuert den Schlaf-Wach-Rhythmus"), ("Testosteron", "lässt beim Jungen die Muskeln wachsen und die Stimme tiefer werden"), ("Wachstumshormon", "fördert das Längenwachstum")],
            "Was bewirkt {k}?", "Welches Hormon {v}?"),
           ("Nerven oder Hormone?", {"dem Nervensystem": ["leitet elektrische Signale", "wirkt in Millisekunden", "wirkt sehr gezielt auf einzelne Muskeln", "Reflex beim Stolpern", "Signale laufen durch Axone"],
                                     "dem Hormonsystem": ["Botenstoffe im Blut", "wirkt oft erst nach Minuten", "wirkt lange anhaltend", "regelt das Wachstum", "steuert die Pubertät", "regelt den Blutzucker"]})],
          ["Hormone werden mit dem Blut transportiert.", "Insulin senkt den Blutzucker.", "Glukagon erhöht den Blutzucker.", "Die Bauchspeicheldrüse bildet Insulin.",
           "Hormone wirken nach dem Schlüssel-Schloss-Prinzip.", "Adrenalin ist ein Stresshormon.", "Bei Diabetes Typ 1 fehlt Insulin.", "Nerven wirken schneller als Hormone."],
          [("Insulin erhöht den Blutzucker.", "Insulin senkt ihn."), ("Hormone wirken auf jede Zelle.", "Nur auf Zellen mit Rezeptor."), ("Hormone wirken schneller als Nerven.", "Nerven wirken schneller."),
           ("Die Schilddrüse bildet Insulin.", "Insulin kommt aus der Bauchspeicheldrüse."), ("Adrenalin beruhigt den Herzschlag.", "Adrenalin beschleunigt ihn."),
           ("Hormone werden über Nerven geleitet.", "Sie werden mit dem Blut transportiert.")],
          "Hormone", "living-things-and-ecosystems"),

        H("B", "genetik-dna-und-zellteilung", "DNA, Chromosomen und Zellteilung", "DNA und Zellteilung",
          "Die Schülerinnen und Schüler beschreiben Bau der DNA, Chromosomen und Gene, Mitose und Meiose sowie die Proteinbiosynthese im Überblick.",
          "Zellkern, Chromosomen, DNA-Doppelhelix, Basenpaarung, Gen, Mitose, Meiose, diploid und haploid, Karyogramm, Mutation",
          "Die DNA trägt die Erbinformation als Basenfolge", "Bei der Mitose entstehen gleiche Zellen, bei der Meiose Keimzellen mit halbem Chromosomensatz.",
          ["Die DNA ist eine Doppelhelix. Ihre Basen bilden Paare: Adenin mit Thymin, Guanin mit Cytosin. Ein Gen ist ein Abschnitt, der die Information für ein Protein trägt.",
           "Der Mensch hat 46 Chromosomen in 23 Paaren. Bei der Mitose wird die DNA verdoppelt und gleich aufgeteilt: Es entstehen zwei identische Tochterzellen.",
           "Die Meiose bildet Keimzellen mit 23 Chromosomen (haploid). Bei der Befruchtung entsteht wieder ein doppelter Satz (diploid)."],
          [("Ein DNA-Strang hat die Basenfolge A-T-G-C. Wie lautet der Gegenstrang?", ["A paart mit T, G mit C.", "A→T, T→A, G→C, C→G"], "T-A-C-G")],
          [("Keimzellen haben 46 Chromosomen.", "Keimzellen haben 23 Chromosomen."), ("Adenin paart mit Cytosin.", "Adenin paart mit Thymin."),
           ("Bei der Mitose entstehen verschiedene Zellen.", "Die Tochterzellen der Mitose sind genetisch gleich.")],
          [("Was ist ein Karyogramm?", "Ein geordnetes Bild aller Chromosomen einer Zelle."), ("Was ist Trisomie 21?", "Das Chromosom 21 liegt dreimal vor. Menschen mit Down-Syndrom haben 47 Chromosomen."),
           ("Was ist eine Mutation?", "Eine Veränderung der Erbinformation, zum Beispiel durch Strahlung oder Kopierfehler.")],
          [("Basenpaarung", [("Adenin", "Thymin"), ("Thymin", "Adenin"), ("Guanin", "Cytosin"), ("Cytosin", "Guanin"), ("A-T-T-G", "T-A-A-C"), ("G-G-C-A", "C-C-G-T"),
                             ("C-A-T-G", "G-T-A-C"), ("T-T-G-C", "A-A-C-G"), ("A-C-G-T", "T-G-C-A"), ("G-A-C-C", "C-T-G-G")],
            "Was paart mit {k}?", None),
           ("Mitose oder Meiose?", {"der Mitose": ["zwei identische Tochterzellen", "Wachstum und Wundheilung", "Chromosomenzahl bleibt gleich", "läuft in Hautzellen ab", "eine Teilung"],
                                    "der Meiose": ["bildet Ei- und Samenzellen", "halbiert die Chromosomenzahl", "vier Tochterzellen", "zwei Teilungsschritte", "neue Kombination der Erbanlagen"]}),
           ("Begriffe", [("Gen", "Abschnitt der DNA mit der Information für ein Merkmal"), ("Chromosom", "Verpackungsform der DNA im Zellkern"), ("diploid", "doppelter Chromosomensatz"),
                         ("haploid", "einfacher Chromosomensatz"), ("Doppelhelix", "Form der DNA"), ("Mutation", "Veränderung der Erbinformation"), ("Karyogramm", "geordnetes Bild aller Chromosomen"),
                         ("Allel", "Ausprägung eines Gens")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Die DNA ist eine Doppelhelix.", "Adenin paart mit Thymin.", "Der Mensch hat 46 Chromosomen.", "Keimzellen sind haploid.",
           "Die Mitose bildet identische Tochterzellen.", "Ein Gen ist ein Abschnitt der DNA.", "Die Meiose halbiert die Chromosomenzahl.", "Mutationen verändern die Erbinformation."],
          [("Adenin paart mit Guanin.", "Adenin paart mit Thymin."), ("Keimzellen haben 46 Chromosomen.", "Sie haben 23."), ("Die Mitose halbiert die Chromosomenzahl.", "Das macht die Meiose."),
           ("Die DNA ist ein einfacher Faden.", "Sie ist eine Doppelhelix."), ("Hautzellen entstehen durch Meiose.", "Sie entstehen durch Mitose."), ("Ein Chromosom ist ein Protein.", "Es besteht vor allem aus DNA.")],
          "die DNA", "living-things-and-ecosystems"),

        H("B", "vererbung-und-mendel", "Vererbung und Mendelsche Regeln", "Vererbung",
          "Die Schülerinnen und Schüler wenden die Mendelschen Regeln an, unterscheiden dominante, rezessive und intermediäre Erbgänge und werten Kreuzungsschemata und Stammbäume aus.",
          "Gregor Mendel, Allele, Genotyp und Phänotyp, reinerbig und mischerbig, dominant, rezessiv, intermediär, Uniformitätsregel, Spaltungsregel, Stammbaum, Blutgruppen",
          "Jedes Merkmal hat zwei Allele, eines von jedem Elternteil", "Kreuzt man zwei Mischerbige, spalten die Merkmale 3 : 1 auf.",
          ["Ein Merkmal wird durch zwei Allele bestimmt. Das dominante Allel (Großbuchstabe) setzt sich gegen das rezessive (Kleinbuchstabe) durch.",
           "Uniformitätsregel: Kreuzt man zwei reinerbige Eltern (AA × aa), sind alle Nachkommen gleich (Aa). Spaltungsregel: Aa × Aa ergibt AA, Aa, Aa, aa, also 3 : 1.",
           "Beim intermediären Erbgang mischen sich die Merkmale, zum Beispiel rot × weiß ergibt rosa. Die Spaltung ist dann 1 : 2 : 1."],
          [("Zwei braunäugige Eltern (Bb) bekommen ein Kind. Wie wahrscheinlich hat es blaue Augen (bb)?", ["Bb × Bb ergibt BB, Bb, Bb, bb.", "Nur einer von vier Fällen ist bb."], "25 Prozent")],
          [("Das dominante Merkmal ist häufiger.", "Dominant heißt nur, dass es sich durchsetzt, nicht, dass es häufiger ist."), ("Mischerbige zeigen beide Merkmale halb.", "Beim dominanten Erbgang zeigen sie das dominante Merkmal."),
           ("Der Phänotyp ist die Erbanlage.", "Der Phänotyp ist das Erscheinungsbild, der Genotyp die Erbanlage.")],
          [("Wer war Gregor Mendel?", "Ein Mönch, der um 1865 mit Erbsen experimentierte und die Grundregeln der Vererbung fand."),
           ("Warum kann ein Kind andere Merkmale als seine Eltern haben?", "Die Eltern können rezessive Allele tragen, die beim Kind zusammenkommen."), ("Wie wird die Blutgruppe vererbt?", "A und B sind dominant über 0, A und B untereinander gleichwertig.")],
          [("Kreuzungen", [("reinerbig dominant × reinerbig rezessiv (AA × aa)", "nur Aa (mischerbig)"), ("mischerbig × mischerbig (Aa × Aa)", "AA : Aa : aa = 1 : 2 : 1"), ("mischerbig × reinerbig rezessiv (Aa × aa)", "1 : 1 mischerbig zu reinerbig rezessiv"), ("reinerbig dominant × reinerbig dominant (AA × AA)", "nur AA (reinerbig dominant)"),
                           ("reinerbig dominant × mischerbig (AA × Aa)", "1 : 1 reinerbig dominant zu mischerbig"), ("reinerbig rezessiv × reinerbig rezessiv (aa × aa)", "nur aa (reinerbig rezessiv)"), ("rot × weiß bei intermediärem Erbgang", "nur rosa Nachkommen"),
                           ("rosa × rosa bei intermediärem Erbgang", "rot : rosa : weiß = 1 : 2 : 1")],
            "Was ergibt die Kreuzung {k}?", None),
           ("Begriffe", [("Genotyp", "die Erbanlagen eines Lebewesens"), ("Phänotyp", "das Erscheinungsbild"), ("reinerbig", "zwei gleiche Allele"), ("mischerbig", "zwei verschiedene Allele"),
                         ("dominant", "setzt sich im Erscheinungsbild durch"), ("rezessiv", "wird von einem anderen Allel überdeckt"), ("intermediär", "Mischform der beiden Merkmale"),
                         ("Allel", "eine Variante eines Gens")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?"),
           ("Genotyp und Wahrscheinlichkeit", [("Blutgruppen-Genotyp AA", "Blutgruppe A", "b"), ("Blutgruppen-Genotyp A0", "Blutgruppe A", "b"), ("Blutgruppen-Genotyp BB", "Blutgruppe B", "b"), ("Blutgruppen-Genotyp B0", "Blutgruppe B", "b"), ("Blutgruppen-Genotyp AB", "Blutgruppe AB", "b"), ("Blutgruppen-Genotyp 00", "Blutgruppe 0", "b"), ("Aa × Aa: Anteil mit rezessivem Merkmal", "25 Prozent", "p"), ("Aa × Aa: Anteil mit dominantem Merkmal", "75 Prozent", "p"), ("Aa × Aa: Anteil mischerbiger Nachkommen", "50 Prozent", "p"), ("Aa × aa: Anteil mit rezessivem Merkmal", "50 Prozent", "p"), ("Aa × aa: Anteil mit dominantem Merkmal", "50 Prozent", "p"), ("AA × aa: Anteil mischerbiger Nachkommen", "100 Prozent", "p"), ("AA × aa: Anteil mit rezessivem Merkmal", "0 Prozent", "p"), ("AA × Aa: Anteil mit dominantem Merkmal", "100 Prozent", "p"), ("AA × Aa: Anteil reinerbiger Nachkommen", "50 Prozent", "p"), ("aa × aa: Anteil mit dominantem Merkmal", "0 Prozent", "p"), ("Aa × Aa: Anteil reinerbig dominanter Nachkommen", "25 Prozent", "p"), ("Aa × aa: Anteil reinerbiger Nachkommen", "50 Prozent", "p"), ("Aa × Aa: Anteil reinerbiger Nachkommen", "50 Prozent", "p"), ("AA × aa: Anteil mit dominantem Merkmal", "100 Prozent", "p"), ("AA × AA: Anteil mischerbiger Nachkommen", "0 Prozent", "p"), ("aa × aa: Anteil mit rezessivem Merkmal", "100 Prozent", "p"), ("Aa × aa: Anteil mischerbiger Nachkommen", "50 Prozent", "p"), ("AA × Aa: Anteil mit rezessivem Merkmal", "0 Prozent", "p"), ("Kind der Eltern AA × BB", "Blutgruppe AB", "b"), ("Kind der Eltern AA × 00", "Blutgruppe A", "b"), ("Kind der Eltern BB × 00", "Blutgruppe B", "b"), ("Kind der Eltern 00 × 00", "Blutgruppe 0", "b")],
            "Was gilt? {k}", None, (), False)],
          ["Jedes Merkmal wird von zwei Allelen bestimmt.", "Aa × Aa ergibt im Erscheinungsbild 3 : 1.", "AA × aa ergibt nur mischerbige Nachkommen.", "Der Phänotyp ist das Erscheinungsbild.",
           "Rezessive Merkmale können eine Generation überspringen.", "Mendel experimentierte mit Erbsen.", "Beim intermediären Erbgang ergibt rot × weiß rosa.", "Blutgruppe 0 ist rezessiv."],
          [("Aa × Aa ergibt nur dominante Nachkommen.", "Es ergibt 3 : 1."), ("Der Genotyp ist das Erscheinungsbild.", "Das ist der Phänotyp."), ("Dominante Merkmale sind immer häufiger.", "Dominant heißt nicht häufig."),
           ("Mendel experimentierte mit Mäusen.", "Er nutzte Erbsen."), ("Blutgruppe 0 ist dominant.", "Sie ist rezessiv."), ("Reinerbig heißt zwei verschiedene Allele.", "Reinerbig heißt zwei gleiche Allele.")],
          "die Vererbung", "living-things-and-ecosystems"),

        H("B", "oekologie-und-stoffkreislaeufe", "Ökologie und Stoffkreisläufe", "Ökologie",
          "Die Schülerinnen und Schüler beschreiben abiotische und biotische Umweltfaktoren, Toleranzbereiche, Räuber-Beute-Beziehungen, Kohlenstoff- und Energiefluss sowie den Einfluss des Menschen.",
          "abiotische und biotische Faktoren, Toleranzkurve, ökologische Nische, Konkurrenz, Symbiose, Parasitismus, Räuber-Beute-Beziehung, Kohlenstoffkreislauf, Energiefluss, Treibhauseffekt",
          "Stoffe kreisen, die Energie fließt hindurch", "Auf jeder Stufe der Nahrungskette geht viel Energie als Wärme verloren.",
          ["Abiotische Faktoren sind unbelebte Einflüsse wie Licht, Temperatur und Wasser. Biotische Faktoren kommen von Lebewesen: Konkurrenz, Fressfeinde, Symbiose, Parasiten.",
           "Jede Art hat einen Toleranzbereich. Das Optimum liegt in der Mitte. Räuber und Beute beeinflussen sich: Mehr Beute bedeutet später mehr Räuber.",
           "Kohlenstoff kreist: Pflanzen binden CO₂ bei der Fotosynthese, Lebewesen geben es bei der Atmung ab. Fossile Brennstoffe setzen zusätzlich CO₂ frei."],
          [("Von 1000 kJ in Gras kommen etwa 10 Prozent beim Hasen an. Wie viel ist das?", ["10 Prozent von 1000 kJ", "1000 kJ · 0,1 = 100 kJ"], "100 kJ")],
          [("Energie kreist im Ökosystem wie Stoffe.", "Stoffe kreisen, Energie fließt hindurch und geht als Wärme verloren."), ("Parasiten töten ihren Wirt immer sofort.", "Meist schädigen sie ihn nur."),
           ("Je mehr Räuber, desto mehr Beute.", "Viele Räuber verringern die Beute.")],
          [("Was ist eine Symbiose?", "Ein Zusammenleben zum Vorteil beider Partner, zum Beispiel bei Flechten aus Pilz und Alge."), ("Warum gibt es wenige Endkonsumenten?", "Auf jeder Stufe geht Energie verloren, für die oberste Stufe bleibt wenig übrig."),
           ("Was ist eine ökologische Nische?", "Die Gesamtheit der Ansprüche einer Art an ihre Umwelt.")],
          [("Abiotisch oder biotisch?", {"den abiotischen Faktoren": ["Lichtmenge", "Temperatur", "Niederschlag", "pH-Wert des Bodens", "Wind", "Mineralstoffgehalt"],
                                         "den biotischen Faktoren": ["Fressfeinde", "Konkurrenz um Nahrung", "Parasiten", "Bestäuber", "Krankheitserreger", "Symbiosepartner"]}),
           ("Beziehungen", [("Pilz und Alge in der Flechte", "Symbiose"), ("Biene und Blüte", "Symbiose"), ("Bandwurm im Darm", "Parasitismus"), ("Zecke am Reh", "Parasitismus"),
                            ("Fuchs und Hase", "Räuber-Beute-Beziehung"), ("Luchs und Reh", "Räuber-Beute-Beziehung"), ("zwei Buchen um Licht", "Konkurrenz"), ("Amsel und Drossel um Regenwürmer", "Konkurrenz")],
            "Welche Beziehung ist das: {k}?", None),
           ("Kohlenstoffkreislauf", [("Fotosynthese", "bindet Kohlenstoffdioxid aus der Luft"), ("Zellatmung", "gibt Kohlenstoffdioxid an die Luft ab"), ("Verbrennen von Kohle und Erdöl", "setzt gespeicherten Kohlenstoff frei"),
                                     ("Zersetzung durch Destruenten", "gibt Kohlenstoff toter Lebewesen frei"), ("Moore und Wälder", "speichern viel Kohlenstoff"), ("Ozean", "löst Kohlenstoffdioxid aus der Luft")],
            "Welche Rolle spielt im Kohlenstoffkreislauf: {k}?", "Was {v}?")],
          ["Licht ist ein abiotischer Faktor.", "Konkurrenz ist ein biotischer Faktor.", "Energie geht in der Nahrungskette als Wärme verloren.", "Flechten sind eine Symbiose.",
           "Pflanzen binden Kohlenstoffdioxid.", "Verbrennen fossiler Stoffe setzt Kohlenstoffdioxid frei.", "Jede Art hat einen Toleranzbereich.", "Der Bandwurm ist ein Parasit."],
          [("Energie kreist im Ökosystem.", "Energie fließt hindurch."), ("Temperatur ist ein biotischer Faktor.", "Sie ist abiotisch."), ("Viele Räuber vermehren die Beute.", "Sie verringern die Beute."),
           ("Die Zellatmung bindet Kohlenstoffdioxid.", "Sie gibt es ab."), ("Bei der Symbiose schadet ein Partner dem anderen.", "Beide haben Vorteile."), ("Auf jeder Stufe bleibt die ganze Energie erhalten.", "Viel geht als Wärme verloren.")],
          "die Ökologie", "living-things-and-ecosystems"),

        H("C", "saeuren-und-laugen", "Säuren und Laugen", "Säuren und Laugen",
          "Die Schülerinnen und Schüler beschreiben Eigenschaften von sauren und alkalischen Lösungen, die pH-Skala, Indikatoren und wichtige Säuren und Laugen im Alltag.",
          "saure und alkalische Lösungen, pH-Skala, Indikatoren, Oxoniumionen und Hydroxidionen, Salzsäure, Schwefelsäure, Natronlauge, Kalkwasser, Sicherheit",
          "pH unter 7 ist sauer, über 7 alkalisch", "Saure Lösungen enthalten Oxoniumionen (H₃O⁺), alkalische Lösungen Hydroxidionen (OH⁻).",
          ["Die pH-Skala reicht von 0 bis 14. pH 7 ist neutral wie reines Wasser. Je kleiner der pH-Wert, desto saurer die Lösung.",
           "Saure Lösungen enthalten Oxoniumionen H₃O⁺. Alkalische Lösungen (Laugen) enthalten Hydroxidionen OH⁻. Beide sind ätzend, darum gilt: Schutzbrille tragen.",
           "Indikatoren zeigen den pH-Wert durch ihre Farbe. Universalindikator ist im Sauren rot, im Neutralen grün und im Alkalischen blau bis violett."],
          [("Ein Universalindikator färbt sich in einer Lösung blau. Was folgt daraus?", ["Blau zeigt einen pH-Wert über 7.", "Über 7 ist alkalisch."], "Die Lösung ist alkalisch.")],
          [("pH 2 ist schwach sauer.", "pH 2 ist stark sauer, je kleiner der Wert, desto saurer."), ("Laugen sind harmlos, weil sie nicht sauer sind.", "Laugen sind genauso ätzend wie Säuren."),
           ("Man gießt Wasser in konzentrierte Säure.", "Immer erst das Wasser, dann die Säure: Sonst spritzt es gefährlich.")],
          [("Warum schmeckt Zitronensaft sauer?", "Er enthält Zitronensäure und hat einen pH-Wert um 2."), ("Was ist Rotkohlsaft?", "Ein natürlicher Indikator: rot im Sauren, violett im Neutralen, grün bis gelb im Alkalischen."),
           ("Was ist saurer Regen?", "Regen, der durch gelöste Schwefel- und Stickstoffoxide einen pH-Wert unter 5,6 hat.")],
          [("pH-Werte", [("Magensaft", "etwa 1"), ("Zitronensaft", "etwa 2"), ("Cola", "etwa 3"), ("Kaffee", "etwa 5"), ("reines Wasser", "7"), ("Blut", "etwa 7,4"),
                         ("Seifenlauge", "etwa 10"), ("Natronlauge", "etwa 14"), ("Meerwasser", "etwa 8")],
            "Welchen pH-Wert hat ungefähr: {k}?", None),
           ("Sauer, neutral oder alkalisch?", {"den sauren Lösungen": ["Essig", "Zitronensaft", "Salzsäure", "Cola", "Magensaft", "Sauerkrautsaft"],
                                               "den neutralen Lösungen": ["destilliertes Wasser", "Kochsalzlösung", "Zuckerlösung"],
                                               "den alkalischen Lösungen": ["Natronlauge", "Kalkwasser", "Seifenlauge", "Ammoniaklösung", "Rohrreiniger"]}),
           ("Säuren und Laugen", [("Salzsäure", "HCl in Wasser"), ("Schwefelsäure", "H₂SO₄"), ("Kohlensäure", "H₂CO₃"), ("Salpetersäure", "HNO₃"), ("Natronlauge", "NaOH in Wasser"),
                                  ("Kalkwasser", "Ca(OH)₂ in Wasser"), ("Phosphorsäure", "H₃PO₄")],
            "Welche Formel gehört zu {k}?", "Welcher Stoff hat die Formel {v}?")],
          ["pH 7 ist neutral.", "Saure Lösungen haben einen pH-Wert unter 7.", "Laugen enthalten Hydroxidionen.", "Saure Lösungen enthalten Oxoniumionen.",
           "Universalindikator ist im Sauren rot.", "Laugen sind ätzend.", "Erst das Wasser, dann die Säure.", "Magensaft ist stark sauer."],
          [("pH 12 ist sauer.", "pH 12 ist alkalisch."), ("Laugen sind harmlos.", "Laugen sind ätzend."), ("Man gießt Wasser in die Säure.", "Erst das Wasser, dann die Säure."),
           ("Universalindikator ist im Alkalischen rot.", "Im Alkalischen ist er blau."), ("Zuckerlösung ist sauer.", "Sie ist neutral."), ("Je größer der pH-Wert, desto saurer.", "Je kleiner, desto saurer.")],
          "Säuren und Laugen", "matter"),

        H("C", "neutralisation-und-stoffmenge", "Neutralisation und Stoffmenge", "Neutralisation und Mol",
          "Die Schülerinnen und Schüler beschreiben die Neutralisation, rechnen mit Stoffmenge, molarer Masse und Konzentration und nutzen die Avogadro-Konstante.",
          "Neutralisation, Salzbildung, Titration, Stoffmenge, Mol, molare Masse, Avogadro-Konstante, Stoffmengenkonzentration",
          "Säure und Lauge reagieren zu Salz und Wasser", "1 mol sind 6,02 · 10²³ Teilchen. n = m : M.",
          ["Bei der Neutralisation reagieren Oxoniumionen und Hydroxidionen zu Wasser: H₃O⁺ + OH⁻ → 2 H₂O. Dazu entsteht ein Salz, zum Beispiel Natriumchlorid aus Salzsäure und Natronlauge.",
           "Die Stoffmenge n wird in Mol gemessen. 1 mol enthält 6,02 · 10²³ Teilchen. Die molare Masse M gibt die Masse von 1 mol an, zum Beispiel 18 g/mol für Wasser.",
           "Es gilt n = m : M. Die Stoffmengenkonzentration einer Lösung ist c = n : V in mol/l."],
          [("Wie viel Stoffmenge sind 36 g Wasser (M = 18 g/mol)?", ["n = m : M", "36 g : 18 g/mol = 2 mol"], "2 mol")],
          [("1 mol ist 1 Gramm.", "1 mol ist eine Teilchenanzahl, seine Masse hängt vom Stoff ab."), ("Bei der Neutralisation entsteht immer Kochsalz.", "Welches Salz entsteht, hängt von Säure und Lauge ab."),
           ("Neutralisation heißt, die Lösung verdampft.", "Neutralisation ist eine Reaktion von Säure und Lauge.")],
          [("Was ist eine Titration?", "Ein Verfahren, bei dem man Lauge tropfenweise zu einer Säure gibt, bis der Indikator umschlägt. So bestimmt man die Konzentration."),
           ("Wozu Neutralisation im Alltag?", "Gegen Sodbrennen, zum Kalken saurer Böden und zur Abwasserreinigung."), ("Woher kommt die molare Masse?", "Aus den Atommassen im Periodensystem, in g/mol.")],
          [("Salzbildung", [("Salzsäure + Natronlauge", "Natriumchlorid + Wasser"), ("Schwefelsäure + Natronlauge", "Natriumsulfat + Wasser"), ("Salzsäure + Kalilauge", "Kaliumchlorid + Wasser"),
                            ("Salpetersäure + Natronlauge", "Natriumnitrat + Wasser"), ("Salzsäure + Kalkwasser", "Calciumchlorid + Wasser"), ("Phosphorsäure + Natronlauge", "Natriumphosphat + Wasser")],
            "Was entsteht? {k} →", "Woraus entsteht: {v}?"),
           ("Molare Massen", [("Wasser H₂O", "18 g/mol"), ("Kohlenstoffdioxid CO₂", "44 g/mol"), ("Sauerstoff O₂", "32 g/mol"), ("Methan CH₄", "16 g/mol"), ("Natriumchlorid NaCl", "58,5 g/mol"),
                              ("Natriumhydroxid NaOH", "40 g/mol"), ("Calciumcarbonat CaCO₃", "100 g/mol"), ("Schwefelsäure H₂SO₄", "98 g/mol"), ("Ammoniak NH₃", "17 g/mol")],
            "Welche molare Masse hat {k}?", "Welcher Stoff hat die molare Masse {v}?"),
           ("Begriffe", [("Mol", "Einheit der Stoffmenge"), ("Avogadro-Konstante", "6,02 · 10²³ Teilchen pro Mol"), ("molare Masse", "Masse von 1 mol eines Stoffes"), ("Neutralisation", "Reaktion von Säure und Lauge"),
                         ("Titration", "Bestimmung einer Konzentration durch tropfenweise Zugabe"), ("Stoffmengenkonzentration", "Stoffmenge pro Liter Lösung"), ("Äquivalenzpunkt", "Säure und Lauge sind genau neutralisiert")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Säure und Lauge reagieren zu Salz und Wasser.", "1 mol enthält 6,02 · 10²³ Teilchen.", "Wasser hat die molare Masse 18 g/mol.", "Die Stoffmenge ist Masse durch molare Masse.",
           "Salzsäure und Natronlauge ergeben Kochsalz und Wasser.", "Bei der Titration schlägt der Indikator um.", "Die Konzentration ist Stoffmenge durch Volumen.", "Kalk neutralisiert saure Böden."],
          [("1 mol wiegt immer 1 g.", "Die Masse hängt vom Stoff ab."), ("Bei jeder Neutralisation entsteht Kochsalz.", "Das Salz hängt von Säure und Lauge ab."), ("Wasser hat die molare Masse 10 g/mol.", "Es hat 18 g/mol."),
           ("Für die Stoffmenge gilt n = M : m.", "Es gilt n = m : M."), ("1 mol sind 6,02 · 10²³ Kilogramm.", "1 mol sind 6,02 · 10²³ Teilchen."), ("Bei der Neutralisation entsteht Sauerstoff.", "Es entstehen Wasser und Salz.")],
          "die Neutralisation", "matter", calc=f_mol2),

        H("C", "molekuele-und-elektronenpaarbindung", "Moleküle und Elektronenpaarbindung", "Elektronenpaarbindung",
          "Die Schülerinnen und Schüler erklären die Elektronenpaarbindung, zeichnen Lewis-Formeln, unterscheiden polare und unpolare Bindungen und erklären Wasserstoffbrücken und Eigenschaften des Wassers.",
          "Elektronenpaarbindung, Lewis-Formel, Einfach-, Doppel- und Dreifachbindung, Elektronegativität, polare Bindung, Dipol, räumlicher Bau, Wasserstoffbrücken",
          "Nichtmetalle teilen sich Elektronenpaare", "Sind die Elektronen ungleich verteilt, ist die Bindung polar. Wasser ist ein Dipol.",
          ["Nichtmetallatome erreichen die Edelgasschale, indem sie gemeinsame Elektronenpaare bilden. So entstehen Moleküle wie H₂, Cl₂ oder H₂O.",
           "Die Elektronegativität gibt an, wie stark ein Atom Bindungselektronen anzieht. Sauerstoff zieht stärker als Wasserstoff. Die O–H-Bindung ist polar.",
           "Das Wassermolekül ist gewinkelt und ein Dipol. Zwischen Wassermolekülen bilden sich Wasserstoffbrücken. Darum hat Wasser eine hohe Siedetemperatur."],
          [("Wie viele gemeinsame Elektronenpaare hat das Stickstoffmolekül N₂?", ["Stickstoff hat 5 Außenelektronen.", "Jedem Atom fehlen 3, also teilen sie 3 Paare."], "drei (Dreifachbindung)")],
          [("Bei der Elektronenpaarbindung werden Elektronen ganz abgegeben.", "Die Elektronen werden geteilt, nicht abgegeben."), ("Das Wassermolekül ist gestreckt.", "Es ist gewinkelt."),
           ("Wasserstoffbrücken sind Bindungen im Molekül.", "Sie wirken zwischen Molekülen.")],
          [("Warum löst sich Zucker in Wasser, Öl aber nicht?", "Zucker ist polar wie Wasser. Öl ist unpolar. Ähnliches löst sich in Ähnlichem."), ("Warum schwimmt Eis?", "Im Eis bilden die Wasserstoffbrücken ein lockeres Gitter mit viel Raum."),
           ("Was ist ein freies Elektronenpaar?", "Ein Elektronenpaar, das nicht an einer Bindung beteiligt ist, zum Beispiel zwei am Sauerstoff im Wasser.")],
          [("Bindungen", [("H₂", "Einfachbindung"), ("Cl₂", "Einfachbindung"), ("HCl", "Einfachbindung"), ("O₂", "Doppelbindung"), ("CO₂", "zwei Doppelbindungen"), ("N₂", "Dreifachbindung"),
                          ("H₂O", "zwei Einfachbindungen"), ("NH₃", "drei Einfachbindungen"), ("CH₄", "vier Einfachbindungen")],
            "Welche Bindung hat {k}?", None),
           ("Polar oder unpolar?", {"den polaren Stoffen": ["Wasser", "Chlorwasserstoff", "Ammoniak", "Ethanol", "Zucker"],
                                    "den unpolaren Stoffen": ["Methan", "Sauerstoff", "Speiseöl", "Benzin", "Stickstoff", "Wachs"]}),
           ("Begriffe", [("Elektronenpaarbindung", "gemeinsame Elektronenpaare zwischen Nichtmetallatomen"), ("Lewis-Formel", "Darstellung mit Strichen für Elektronenpaare"), ("Elektronegativität", "Maß für die Anziehung von Bindungselektronen"),
                         ("Dipol", "Molekül mit positivem und negativem Ende"), ("Wasserstoffbrücke", "Anziehung zwischen Wassermolekülen"), ("freies Elektronenpaar", "Elektronenpaar ohne Bindung"),
                         ("Molekül", "Teilchen aus fest verbundenen Atomen")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Nichtmetalle bilden gemeinsame Elektronenpaare.", "Stickstoff N₂ hat eine Dreifachbindung.", "Das Wassermolekül ist gewinkelt.", "Wasser ist ein Dipol.",
           "Sauerstoff hat eine höhere Elektronegativität als Wasserstoff.", "Öl ist unpolar.", "Wasserstoffbrücken wirken zwischen Molekülen.", "Methan hat vier Einfachbindungen."],
          [("Bei der Elektronenpaarbindung werden Elektronen abgegeben.", "Sie werden geteilt."), ("Das Wassermolekül ist gestreckt.", "Es ist gewinkelt."), ("Öl ist polar.", "Öl ist unpolar."),
           ("N₂ hat eine Einfachbindung.", "N₂ hat eine Dreifachbindung."), ("Wasserstoffbrücken liegen im Molekül.", "Sie wirken zwischen Molekülen."), ("Methan ist ein Dipol.", "Methan ist unpolar.")],
          "Molekülbindungen", "matter"),

        H("P", "elektrischer-widerstand-und-ohmsches-gesetz", "Widerstand und ohmsches Gesetz", "Ohmsches Gesetz",
          "Die Schülerinnen und Schüler messen Stromstärke und Spannung, berechnen Widerstände mit R = U : I und bestimmen Gesamtwiderstände in Reihen- und Parallelschaltung.",
          "Stromstärke, Spannung, Widerstand, Ohm, ohmsches Gesetz, Kennlinie, Reihenschaltung, Parallelschaltung, Messgeräte",
          "Der Widerstand ist Spannung durch Stromstärke", "R = U : I. In Reihe addieren sich die Widerstände, parallel wird der Gesamtwiderstand kleiner.",
          ["Die Stromstärke I misst man in Ampere mit einem Amperemeter in Reihe. Die Spannung U misst man in Volt mit einem Voltmeter parallel zum Bauteil.",
           "Der Widerstand R = U : I wird in Ohm (Ω) angegeben. Bei einem ohmschen Widerstand ist I proportional zu U: Die Kennlinie ist eine Gerade.",
           "Reihenschaltung: Der Strom ist überall gleich, die Widerstände addieren sich. Parallelschaltung: Die Spannung ist überall gleich, die Ströme addieren sich."],
          [("Wie groß ist der Widerstand einer Lampe bei 6 V und 0,3 A?", ["R = U : I", "6 V : 0,3 A = 20 Ω"], "20 Ω")],
          [("Das Amperemeter wird parallel geschaltet.", "Das Amperemeter wird in Reihe geschaltet."), ("In der Parallelschaltung addieren sich die Widerstände.", "Dort wird der Gesamtwiderstand kleiner."),
           ("Der Strom wird im Bauteil verbraucht.", "Die Stromstärke ist vor und nach dem Bauteil gleich.")],
          [("Warum sind Haushaltsgeräte parallel geschaltet?", "So bekommt jedes Gerät die volle Spannung von 230 V und kann einzeln geschaltet werden."),
           ("Wovon hängt der Widerstand eines Drahtes ab?", "Vom Material, der Länge und dem Querschnitt. Lange, dünne Drähte haben einen großen Widerstand."), ("Ist Strom gefährlich?", "Schon kleine Ströme durch den Körper können lebensgefährlich sein.")],
          [("Größen und Einheiten", [("Stromstärke", "Ampere"), ("Spannung", "Volt"), ("Widerstand", "Ohm"), ("Leistung", "Watt"), ("Ladung", "Coulomb"), ("elektrische Energie", "Kilowattstunde")],
            "In welcher Einheit misst man {k}?", "Welche Größe misst man in {v}?"),
           ("Reihe oder parallel?", {"der Reihenschaltung": ["Strom ist überall gleich", "Widerstände addieren sich", "fällt ein Bauteil aus, ist der Kreis unterbrochen", "Teilspannungen addieren sich zur Gesamtspannung", "alte Lichterkette"],
                                     "der Parallelschaltung": ["Spannung ist überall gleich", "Teilströme addieren sich", "Gesamtwiderstand ist kleiner als jeder Einzelwiderstand", "Steckdosen im Haushalt", "Geräte lassen sich einzeln schalten"]}),
           ("Widerstand eines Drahtes", [("Draht doppelt so lang", "Widerstand doppelt so groß"), ("Draht doppelt so dick im Querschnitt", "Widerstand halb so groß"), ("Kupfer statt Eisen", "Widerstand kleiner"),
                                         ("Draht wird stark erhitzt", "Widerstand meist größer"), ("Draht halb so lang", "Widerstand halb so groß"), ("Konstantan statt Kupfer", "Widerstand größer")],
            "Wie ändert sich der Widerstand? {k}", None)],
          ["Der Widerstand ist Spannung durch Stromstärke.", "Das Amperemeter wird in Reihe geschaltet.", "Das Voltmeter wird parallel geschaltet.", "In Reihe addieren sich die Widerstände.",
           "Parallel ist die Spannung überall gleich.", "Ein langer Draht hat einen größeren Widerstand.", "Der Widerstand wird in Ohm angegeben.", "Steckdosen sind parallel geschaltet."],
          [("Das Voltmeter wird in Reihe geschaltet.", "Es wird parallel geschaltet."), ("Für den Widerstand gilt R = U · I.", "Es gilt R = U : I."), ("Parallel addieren sich die Widerstände.", "Parallel wird der Gesamtwiderstand kleiner."),
           ("Ein dicker Draht hat einen größeren Widerstand.", "Er hat einen kleineren Widerstand."), ("Der Strom wird in der Lampe verbraucht.", "Die Stromstärke bleibt gleich."),
           ("Der Widerstand wird in Volt angegeben.", "Er wird in Ohm angegeben.")],
          "elektrische Widerstände", "energy", calc=f_ohm),

        H("P", "elektrische-energie-und-leistung", "Elektrische Energie und Leistung", "Elektrische Leistung",
          "Die Schülerinnen und Schüler berechnen elektrische Leistung und Energie, Stromkosten in kWh und vergleichen den Energiebedarf von Geräten.",
          "elektrische Leistung, P = U · I, elektrische Energie, Kilowattstunde, Stromkosten, Energieeffizienzklassen, Stand-by, Sicherung",
          "Leistung ist Spannung mal Stromstärke", "P = U · I. Die Energie ist Leistung mal Zeit, gemessen in kWh.",
          ["Die elektrische Leistung ist P = U · I und wird in Watt angegeben. Ein Wasserkocher hat etwa 2000 W, eine LED-Lampe etwa 8 W.",
           "Die elektrische Energie ist E = P · t. Der Stromzähler misst sie in Kilowattstunden: 1 kWh = 1000 W · 1 h.",
           "Stromkosten = Energie mal Preis pro kWh. Sparsame Geräte, LED-Lampen und Ausschalten statt Stand-by senken die Kosten."],
          [("Ein Föhn hat 2000 W und läuft 15 Minuten. Wie viel Energie braucht er?", ["2000 W = 2 kW, 15 min = 0,25 h", "2 kW · 0,25 h = 0,5 kWh"], "0,5 kWh")],
          [("Eine Kilowattstunde ist eine Leistung.", "Die Kilowattstunde ist eine Energieeinheit."), ("Ein Gerät mit hoher Leistung braucht immer viel Energie.", "Die Energie hängt auch von der Laufzeit ab."),
           ("Watt und Volt sind dasselbe.", "Watt ist die Einheit der Leistung, Volt die der Spannung.")],
          [("Was macht eine Sicherung?", "Sie unterbricht den Stromkreis, wenn ein zu großer Strom fließt, und schützt so vor Bränden."), ("Wie viel kostet 1 kWh?", "In Deutschland je nach Tarif etwa 30 bis 40 Cent."),
           ("Was bedeutet die Energieeffizienzklasse?", "Sie zeigt, wie sparsam ein Gerät ist, von A (sehr sparsam) bis G.")],
          [("Leistung von Geräten", [("LED-Lampe", "etwa 8 W"), ("Smartphone-Ladegerät", "etwa 10 W"), ("Laptop", "etwa 50 W"), ("Fernseher", "etwa 100 W"), ("Staubsauger", "etwa 800 W"),
                                     ("Wasserkocher", "etwa 2000 W"), ("Backofen", "etwa 3000 W"), ("Kühlschrank", "etwa 100 W im Betrieb")],
            "Welche Leistung hat ungefähr: {k}?", None),
           ("Formeln und Einheiten", [("P = U · I", "elektrische Leistung"), ("E = P · t", "elektrische Energie"), ("R = U : I", "Widerstand"), ("1 kWh", "1000 W eine Stunde lang"),
                                      ("1 kW", "1000 W"), ("Kosten = E · Preis", "Stromkosten")],
            "Was berechnet oder bedeutet: {k}?", "Was gehört zu: {v}?"),
           ("Energie sparen", [("LED statt Glühlampe", "braucht bis zu 90 Prozent weniger Energie"), ("Gerät ganz ausschalten", "kein Stand-by-Verbrauch"), ("Deckel auf den Topf", "Wasser kocht schneller"),
                               ("Wäsche an der Luft trocknen", "kein Wäschetrockner nötig"), ("Kühlschrank nicht neben den Herd", "muss weniger kühlen"), ("Energieeffizienzklasse A", "sehr sparsames Gerät")],
            "Was bringt das? {k}", "Welche Maßnahme {v}?")],
          ["Die Leistung ist Spannung mal Stromstärke.", "Die Kilowattstunde ist eine Energieeinheit.", "Die Energie ist Leistung mal Zeit.", "Ein Wasserkocher hat eine hohe Leistung.",
           "LED-Lampen sind sparsam.", "Eine Sicherung schützt vor zu großem Strom.", "Stand-by verbraucht Energie.", "1 kW sind 1000 W."],
          [("Die Kilowattstunde ist eine Einheit der Leistung.", "Sie ist eine Energieeinheit."), ("Für die Leistung gilt P = U : I.", "Es gilt P = U · I."), ("Stand-by verbraucht keinen Strom.", "Stand-by verbraucht Energie."),
           ("Eine LED braucht mehr Energie als eine Glühlampe.", "Sie braucht viel weniger."), ("1 kW sind 100 W.", "1 kW sind 1000 W."), ("Die Sicherung erhöht den Strom.", "Sie unterbricht den Stromkreis.")],
          "elektrische Leistung", "energy", calc=f_leistung),

        H("P", "elektromagnetismus", "Elektromagnetismus", "Elektromagnetismus",
          "Die Schülerinnen und Schüler beschreiben das Magnetfeld eines stromdurchflossenen Leiters und einer Spule, den Elektromagneten, die Lorentzkraft und den Elektromotor.",
          "Magnetfeld, Feldlinien, Oersted-Versuch, Spule, Eisenkern, Elektromagnet, Lorentzkraft, Elektromotor, Relais, Lautsprecher",
          "Jeder elektrische Strom erzeugt ein Magnetfeld", "Eine Spule mit Eisenkern wird zum starken Elektromagneten, den man ein- und ausschalten kann.",
          ["Oersted entdeckte 1820: Ein stromdurchflossener Draht lenkt eine Kompassnadel ab. Um den Leiter entsteht ein kreisförmiges Magnetfeld.",
           "Eine Spule wirkt wie ein Stabmagnet. Mehr Windungen, ein größerer Strom und ein Eisenkern machen den Elektromagneten stärker.",
           "Auf einen stromdurchflossenen Leiter im Magnetfeld wirkt eine Kraft, die Lorentzkraft. Sie treibt Elektromotoren und Lautsprecher an."],
          [("Wie macht man einen Elektromagneten stärker?", ["Die Stärke hängt von Windungen, Strom und Kern ab.", "Mehr Windungen oder mehr Strom oder ein Eisenkern."], "mehr Windungen, mehr Strom oder ein Eisenkern")],
          [("Ein Elektromagnet ist immer magnetisch.", "Er ist nur magnetisch, solange Strom fließt."), ("Magnetfelder entstehen nur bei Dauermagneten.", "Auch jeder Strom erzeugt ein Magnetfeld."),
           ("Ein Kupferkern verstärkt die Spule.", "Nur ein Kern aus Eisen verstärkt das Magnetfeld deutlich.")],
          [("Wie funktioniert ein Lautsprecher?", "Wechselstrom fließt durch eine Spule an der Membran. Im Feld eines Dauermagneten bewegt sie sich hin und her und erzeugt Schall."),
           ("Was ist ein Relais?", "Ein Schalter, den ein Elektromagnet betätigt. Ein kleiner Strom schaltet so einen großen."), ("Wo braucht man Elektromagnete?", "In Schrottkränen, Türöffnern, Klingeln, Motoren und Magnetschwebebahnen.")],
          [("Anwendungen", [("Elektromotor", "Lorentzkraft dreht eine Spule"), ("Lautsprecher", "Spule bewegt eine Membran"), ("Schrottkran", "starker Elektromagnet hebt Eisen"),
                            ("Relais", "Elektromagnet betätigt einen Schalter"), ("Klingel", "Elektromagnet zieht einen Hammer an"), ("Türöffner", "Elektromagnet gibt die Falle frei"),
                            ("Magnetschwebebahn", "Magnetkräfte heben den Zug an")],
            "Wie funktioniert: {k}?", "Welches Gerät nutzt: {v}?"),
           ("Stärker oder schwächer?", [("mehr Windungen", "stärker"), ("größere Stromstärke", "stärker"), ("Eisenkern einsetzen", "stärker"), ("weniger Windungen", "schwächer"),
                                        ("kleinere Stromstärke", "schwächer"), ("Eisenkern entfernen", "schwächer"), ("Strom ausschalten", "kein Magnetfeld")],
            "Wie wird der Elektromagnet? {k}", None, ("gleich stark",)),
           ("Begriffe", [("Magnetfeld", "Raum, in dem magnetische Kräfte wirken"), ("Feldlinien", "zeigen Richtung und Form des Magnetfelds"), ("Spule", "aufgewickelter Draht"),
                         ("Elektromagnet", "Spule mit Eisenkern, die bei Strom magnetisch ist"), ("Lorentzkraft", "Kraft auf einen Strom im Magnetfeld"), ("Kommutator", "polt den Strom im Motor um"),
                         ("Oersted-Versuch", "Strom lenkt eine Kompassnadel ab")],
            "Was bedeutet {k}?", "Welcher Begriff passt: {v}?")],
          ["Jeder Strom erzeugt ein Magnetfeld.", "Eine Spule wirkt wie ein Stabmagnet.", "Ein Eisenkern verstärkt den Elektromagneten.", "Ein Elektromagnet lässt sich abschalten.",
           "Die Lorentzkraft treibt Elektromotoren an.", "Ein Lautsprecher enthält eine Spule.", "Oersted lenkte mit Strom eine Kompassnadel ab.", "Mehr Windungen machen den Elektromagneten stärker."],
          [("Ein Elektromagnet ist ohne Strom magnetisch.", "Ohne Strom ist er nicht magnetisch."), ("Ein Kupferkern verstärkt die Spule stark.", "Ein Eisenkern verstärkt sie."),
           ("Nur Dauermagnete erzeugen Magnetfelder.", "Auch Ströme erzeugen Magnetfelder."), ("Weniger Windungen machen den Elektromagneten stärker.", "Mehr Windungen machen ihn stärker."),
           ("Ein Elektromotor wandelt Bewegung in Strom um.", "Er wandelt Strom in Bewegung um."), ("Die Lorentzkraft wirkt nur auf ruhende Drähte ohne Strom.", "Sie wirkt auf Ströme im Magnetfeld.")],
          "den Elektromagnetismus", "energy"),
    ]
