# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: I solidi (Spazio e figure)
  python3 tools/gen_it_matematica_c3_solidi.py
Cubo, parallelepipedo, sfera, cilindro, cono, piramide; facce, spigoli e vertici; solidi che rotolano;
oggetti di tutti i giorni; sviluppo del cubo; costruzioni con i cubetti.
Errori: confondere cubo e parallelepipedo, chiamare «cerchio» la sfera, contare solo le facce che si vedono.
"""
import random
import gen_de_mathe_k3_koerper_und_figuren as DE
from it_common import mcq, lesson, make_unit, mix, solido_svg, table

R = random.Random(70319)
NOME = {"cubo": "un cubo", "parallelepipedo": "un parallelepipedo", "sfera": "una sfera", "cilindro": "un cilindro", "cono": "un cono", "piramide": "una piramide"}
FSV = {"un cubo": (6, 12, 8), "un parallelepipedo": (6, 12, 8), "una piramide a base quadrata": (5, 8, 5), "una piramide a base triangolare": (4, 6, 4)}


def s1():
    k = R.choice(list(NOME))
    col = R.choice(["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"])
    ans = NOME[k]
    conf = {"cubo": "un parallelepipedo", "parallelepipedo": "un cubo", "sfera": "un cerchio", "cilindro": "un cono", "cono": "una piramide", "piramide": "un cono"}[k]
    w = [conf] + [n for n in NOME.values() if n not in (ans, conf)]
    why = {"cubo": "Ha 6 facce quadrate tutte uguali.", "parallelepipedo": "Ha 6 facce rettangolari, non tutte uguali.",
           "sfera": "È tutta rotonda, senza facce piane.", "cilindro": "Ha due cerchi uguali e una superficie curva.",
           "cono": "Ha un cerchio e una punta.", "piramide": "Le sue facce laterali sono triangoli che si uniscono in una punta."}[k]
    return mcq(solido_svg(k, R.choice([28, 32, 36]), col) + "Come si chiama questo solido?", ans, w, "%s È <b>%s</b>." % (why, ans))


def s2():
    n = R.choice(list(FSV))
    i = R.randint(0, 2)
    word = ["facce", "spigoli", "vertici"][i]
    v = FSV[n][i]
    others = [x for x in FSV[n] if x != v] + [v + 2, v - 2, 4]
    return mcq("%s %s ha %s?" % ("Quante" if word == "facce" else "Quanti", word, n), str(v), [str(x) for x in others if x != v and x > 0],
               "%s ha %d facce, %d spigoli e %d vertici. Si chiedono i %s: <b>%d</b>." % (n[0].upper() + n[1:], FSV[n][0], FSV[n][1], FSV[n][2], word, v))


QUIZ = [("Quale solido non ha facce piane, né spigoli, né vertici?", "la sfera", ["il cubo", "il cilindro", "il cono"]),
        ("Quale solido ha due facce a forma di cerchio?", "il cilindro", ["il cono", "la sfera", "il parallelepipedo"]),
        ("Quale solido ha una punta e un cerchio?", "il cono", ["la piramide", "il cilindro", "la sfera"]),
        ("Quale solido ha 6 facce quadrate tutte uguali?", "il cubo", ["il parallelepipedo", "la piramide", "il cilindro"]),
        ("Quale solido ha 6 facce rettangolari, non tutte uguali?", "il parallelepipedo", ["il cubo", "la piramide", "il cono"]),
        ("Quale solido può rotolare in tutte le direzioni?", "la sfera", ["il cilindro", "il cono", "il cubo"]),
        ("Quale solido ha facce triangolari che si uniscono in un vertice?", "la piramide", ["il cono", "il cubo", "il cilindro"]),
        ("Quale solido può rotolare e anche stare in piedi, senza punta?", "il cilindro", ["la sfera", "il cono", "il cubo"]),
        ("Come si chiama la linea dove si incontrano due facce?", "spigolo", ["vertice", "base", "lato curvo"]),
        ("Come si chiama il punto dove si incontrano gli spigoli?", "vertice", ["spigolo", "faccia", "centro"])]


def s3_quiz():
    q, a, w = R.choice(QUIZ)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


FACCE = [("Che forma hanno le facce del cubo?", "quadrati", ["rettangoli non quadrati", "triangoli", "cerchi"]),
         ("Che forma hanno le facce di un parallelepipedo (non cubo)?", "rettangoli", ["triangoli", "cerchi", "rombi"]),
         ("Che forma ha la base del cono?", "un cerchio", ["un quadrato", "un triangolo", "un rettangolo"]),
         ("Che forma hanno le facce laterali di una piramide?", "triangoli", ["quadrati", "cerchi", "rettangoli"]),
         ("Se ricalchi il contorno della base di un cilindro, che figura ottieni?", "un cerchio", ["un quadrato", "un triangolo", "un rettangolo"]),
         ("Se ricalchi il contorno di una faccia del cubo, che figura ottieni?", "un quadrato", ["un cerchio", "un triangolo", "un rombo"]),
         ("Se ricalchi la base di una piramide a base quadrata, che figura ottieni?", "un quadrato", ["un triangolo", "un cerchio", "un pentagono"])]


def s3_facce():
    q, a, w = R.choice(FACCE)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


CONTA = [("Quante facce triangolari ha una piramide a base quadrata?", 4, [5, 3, 8]),
         ("Quante facce quadrate ha un cubo?", 6, [4, 8, 12]),
         ("Quanti cerchi ha un cilindro?", 2, [1, 3, 0]),
         ("Quanti cerchi ha un cono?", 1, [2, 0, 3]),
         ("Quanti spigoli partono da un vertice del cubo?", 3, [4, 2, 6]),
         ("Un parallelepipedo ha 2 facce quadrate. Quante facce non sono quadrate?", 4, [6, 2, 8]),
         ("Quante facce triangolari ha una piramide a base triangolare?", 4, [3, 5, 6])]


def s3_conta():
    q, a, w = R.choice(CONTA)
    return mcq(q, str(a), [str(x) for x in w], "Risposta: <b>%d</b>." % a)


def s4():
    it = DE.wuerfelnetz()
    if not it:
        return None
    q = it["q"].replace("aria-label='vier Netze A bis D'", "aria-label='quattro sviluppi A, B, C, D'")
    good = "Welches Netz kann man zu einem Würfel falten?" in q
    q = q.replace("Welches Netz kann man zu einem Würfel falten?", "Quale sviluppo si può piegare per formare un cubo?")
    q = q.replace("Drei Netze ergeben einen Würfel. Welches Netz ergibt <b>keinen</b> Würfel?", "Tre sviluppi formano un cubo. Quale <b>non</b> forma un cubo?")
    k = it["c"][0]
    e = ("Con lo sviluppo %s, piegando, ognuna delle 6 facce va in un posto diverso del cubo." % k if good else
         "Con lo sviluppo %s, piegando, due facce vanno una sopra l’altra e ne manca una." % k)
    return mcq(q, k, it["c"][1:], e)


def tr(it, pairs):
    if not it:
        return None
    for a, b in pairs:
        it["q"], it["e"] = it["q"].replace(a, b), it["e"].replace(a, b)
        it["c"] = [c.replace(a, b) for c in it["c"]]
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"])


def s4_alto():
    return tr(DE.bauplan_hoch(), [("Bauplan eines Würfelgebäudes: Wie hoch ist der höchste Turm?", "Pianta di una costruzione di cubetti vista dall’alto: quanti cubetti ha la torre più alta?"),
                                  ("Die größte Zahl im Bauplan ist", "Il numero più grande della pianta è"), ("Der höchste Turm ist", "La torre più alta ha"),
                                  (" Würfel</b> hoch.", " cubetti</b>."), (" Würfel", " cubetti")])


def s4_pianta():
    return tr(DE.bauplan(), [("Ein Bauplan zeigt ein Würfelgebäude von oben. Die Zahl sagt, wie viele Würfel übereinander stehen. Wie viele Würfel sind es?",
                              "La pianta mostra una costruzione di cubetti vista dall’alto. Ogni numero dice quanti cubetti sono impilati. Quanti cubetti ci sono in tutto?"),
                             ("Addiere alle Zahlen im Bauplan:", "Somma tutti i numeri della pianta:")])


VITA = [("un pallone da calcio", "una sfera"), ("un’arancia", "una sfera"), ("una lattina di pomodori", "un cilindro"), ("una candela", "un cilindro"),
        ("una scatola delle scarpe", "un parallelepipedo"), ("un mattone", "un parallelepipedo"), ("un dado da gioco", "un cubo"), ("una zolletta di zucchero", "un cubo"),
        ("un cono gelato", "un cono"), ("un cappellino da festa", "un cono"), ("un cono stradale", "un cono"), ("un cartone del latte", "un parallelepipedo"),
        ("una biglia", "una sfera"), ("un rotolo di carta da cucina", "un cilindro"), ("le piramidi d’Egitto", "una piramide"), ("un tubetto di colla", "un cilindro")]


def s5_vita():
    thing, ans = R.choice(VITA)
    w = [x for x in ["una sfera", "un cilindro", "un parallelepipedo", "un cubo", "un cono", "una piramide"] if x != ans]
    R.shuffle(w)
    return mcq("Che forma ha %s?" % thing, ans, w, "%s ha la forma di <b>%s</b>." % (thing[0].upper() + thing[1:], ans))


def main():
    DE.R = R
    seen = set()
    sets = [
        ("Riconoscere i solidi", mix(R, seen, [(s1, 20)])),
        ("Facce, spigoli e vertici", mix(R, seen, [(s2, 8), (s3_conta, 7), (s3_facce, 5)])),
        ("Indovina il solido", mix(R, seen, [(s3_quiz, 10), (s5_vita, 10)])),
        ("Sviluppi e costruzioni", mix(R, seen, [(s4, 8), (s4_alto, 4), (s4_pianta, 8)])),
        ("Solidi intorno a noi", mix(R, seen, [(s5_vita, 6), (s1, 6), (s2, 4), (s4_pianta, 4)])),
    ]
    body = lesson(
        ["I <b>solidi</b> sono figure che occupano spazio: si possono prendere in mano.",
         "Alcuni solidi hanno solo facce piane: <b>cubo</b>, <b>parallelepipedo</b>, <b>piramide</b>. Altri hanno superfici curve: <b>sfera</b>, <b>cilindro</b>, <b>cono</b>, e possono rotolare.",
         "Le <b>facce</b> sono le superfici piane; gli <b>spigoli</b> sono le linee dove due facce si incontrano; i <b>vertici</b> sono le punte.",
         "Lo <b>sviluppo</b> di un solido è la sua superficie aperta e stesa sul piano: il cubo si sviluppa in 6 quadrati."],
        [("Quante facce, spigoli e vertici ha un cubo?", ["facce: 6 quadrati", "spigoli: 12", "vertici: 8"], "6, 12, 8")],
        [["Confondere cubo e parallelepipedo", "Il cubo ha 6 facce quadrate uguali; il parallelepipedo ha facce rettangolari."],
         ["Chiamare «cerchio» la sfera", "Il cerchio è una figura piana; la sfera è un solido."],
         ["Contare solo le facce che si vedono nel disegno", "Pensa anche alle facce dietro e sotto."]],
        table(["Solido", "Facce", "Spigoli", "Vertici"], [["cubo", "6", "12", "8"], ["parallelepipedo", "6", "12", "8"], ["piramide a base quadrata", "5", "8", "5"]]))
    faq = [("Che differenza c’è tra figura piana e solido?", "La figura piana è disegnata su un foglio (quadrato, cerchio); il solido occupa spazio (cubo, sfera)."),
           ("Perché la sfera rotola in tutte le direzioni?", "Perché è tutta curva e non ha facce piane: il cilindro e il cono invece rotolano solo in alcune direzioni.")]
    make_unit(R, "solidi", "S",
              "Riconoscere, denominare e descrivere figure geometriche solide; individuare facce, spigoli e vertici; riconoscere i solidi negli oggetti di tutti i giorni e costruire modelli",
              "I solidi: facce, spigoli e vertici", "Solidi",
              "Schede di matematica per la classe terza sui solidi: cubo, parallelepipedo, piramide, sfera, cilindro e cono, facce, spigoli e vertici, sviluppo del cubo e costruzioni con i cubetti. 100 esercizi con soluzioni.",
              "Facce piane, spigoli e vertici.", "Sfera, cilindro e cono possono rotolare.",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
