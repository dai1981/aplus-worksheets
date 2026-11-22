# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Figure piane e solidi (Spazio e figure)
  python3 tools/gen_it_matematica_c2_figure_e_solidi.py
Quadrato, rettangolo, triangolo, cerchio; contare lati e vertici; figure negli oggetti; solidi (cubo,
parallelepipedo, sfera, cilindro, cono, piramide); l’impronta di un solido; solidi negli oggetti di tutti i giorni.
Errori: chiamare «quadrato» un rettangolo, «cerchio» la sfera, contare due volte un vertice.
"""
import random
from it_common import mcq, lesson, make_unit, mix, solido_svg
import gen_it_matematica_c3_figure_piane_e_perimetro as F3
import gen_it_matematica_c3_solidi as S3
import gen_fr_maths_ce2_figures_planes_et_angles_droits as FRF
import it_c2 as C
import k_pics

R = R0 = random.Random(70216)
G = "classe-seconda"
BASE = {"carré": "un quadrato", "rectangle": "un rettangolo", "triangle": "un triangolo", "triangle rectangle": "un triangolo"}


def s1_nome():
    k = R.choice(list(BASE) + ["cerchio", "cerchio"])
    if k == "cerchio":
        pic = C.it(k_pics.one_shape_svg("circle", R.choice(["red", "blue", "yellow", "green"]), R.randint(30, 45)), "una figura piana")
        return mcq(pic + "Come si chiama questa figura?", "un cerchio", ["un quadrato", "un triangolo", "una sfera"], "È tonda e non ha lati né vertici: è <b>un cerchio</b>.")
    ans = BASE[k]
    pic = F3.shape(k)
    w = [x for x in ("un quadrato", "un rettangolo", "un triangolo", "un cerchio") if x != ans]
    why = {"un quadrato": "4 lati tutti uguali", "un rettangolo": "4 lati, due lunghi e due corti", "un triangolo": "3 lati"}[ans]
    return mcq(pic + "Come si chiama questa figura?", ans, w, "Ha %s: è <b>%s</b>." % (why, ans))


def s1_lati():
    k = R.choice(list(BASE))
    n = 4 if k in ("carré", "rectangle") else 3
    word = R.choice(["lati", "vertici"])
    return mcq(F3.shape(k) + "Quanti %s ha questa figura?" % word, str(n), [str(n + 1), str(n - 1), "0"], "Conta i %s: <b>%d</b>." % (word, n))


OGG = [("una finestra", "un rettangolo"), ("una fetta di pizza triangolare", "un triangolo"), ("una moneta", "un cerchio"), ("la faccia di un dado", "un quadrato"),
       ("una porta", "un rettangolo"), ("un cartello di pericolo", "un triangolo"), ("l’orologio della cucina", "un cerchio"), ("una piastrella quadrata", "un quadrato"),
       ("un foglio del quaderno", "un rettangolo"), ("la ruota di una bici", "un cerchio"), ("una vela di barca", "un triangolo"), ("un fazzoletto quadrato", "un quadrato")]


def s2_oggetti():
    o, a = R.choice(OGG)
    return mcq("Che forma ha %s?" % o, a, [x for x in ("un quadrato", "un rettangolo", "un triangolo", "un cerchio") if x != a], "%s ha la forma di <b>%s</b>." % (o[0].upper() + o[1:], a))


QUIZ = [("Quale figura non ha lati?", "il cerchio", ["il quadrato", "il triangolo", "il rettangolo"]),
        ("Quale figura ha 3 lati?", "il triangolo", ["il quadrato", "il cerchio", "il rettangolo"]),
        ("Quale figura ha 4 lati tutti uguali?", "il quadrato", ["il rettangolo", "il triangolo", "il cerchio"]),
        ("Quale figura ha 4 lati, due lunghi e due corti?", "il rettangolo", ["il quadrato", "il triangolo", "il cerchio"]),
        ("Come si chiama il punto dove si incontrano due lati?", "vertice", ["lato", "centro", "spigolo"]),
        ("Quante figure piane servono per fare le facce di un cubo?", "6 quadrati", ["4 quadrati", "6 cerchi", "3 triangoli"])]


def s2_quiz():
    q, a, w = R.choice(QUIZ)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s3_solido():
    return S3.s1()


IMP = [("un cubo", "un quadrato"), ("un cilindro", "un cerchio"), ("un cono (dalla base)", "un cerchio"), ("un parallelepipedo (dalla faccia lunga)", "un rettangolo"),
       ("una piramide (dalla base quadrata)", "un quadrato"), ("una piramide (da una faccia laterale)", "un triangolo")]


def s4_impronta():
    s, f = R.choice(IMP)
    return mcq("Appoggi %s sulla sabbia. Che impronta lascia?" % s, f, [x for x in ("un quadrato", "un rettangolo", "un triangolo", "un cerchio") if x != f], "Resta il contorno della faccia appoggiata: <b>%s</b>." % f)


def s4_rotola():
    k = R.choice(list(S3.NOME))
    rot = k in ("sfera", "cilindro", "cono")
    return mcq(solido_svg(k, 32, "#c9dcf2") + "Questo solido può rotolare?", "sì" if rot else "no", ["no" if rot else "sì", "solo se è grande", "solo in salita"],
               "È %s: %s." % (S3.NOME[k], "ha una parte curva, <b>può rotolare</b>" if rot else "ha solo facce piane, <b>non rotola</b> (scivola)"))


def main():
    for m in (F3, S3, FRF):
        m.R = R
    S3.DE.R = R
    seen = set()
    sets = [
        ("Le figure piane", mix(R, seen, [(s1_nome, 12), (s1_lati, 8)])),
        ("Figure intorno a noi", mix(R, seen, [(s2_oggetti, 12), (s2_quiz, 6), (s1_lati, 2)])),
        ("I solidi", mix(R, seen, [(s3_solido, 20)])),
        ("Impronte e solidi che rotolano", mix(R, seen, [(s4_impronta, 6), (s4_rotola, 6), (S3.s5_vita, 8)])),
        ("Solidi intorno a noi", mix(R, seen, [(S3.s5_vita, 8), (S3.s3_quiz, 6), (s3_solido, 6)])),
    ]
    body = lesson(
        ["Le <b>figure piane</b> sono «piatte»: quadrato, rettangolo, triangolo, cerchio. Hanno <b>lati</b> e <b>vertici</b> (il cerchio no).",
         "I <b>solidi</b> occupano spazio e si possono prendere in mano: cubo, parallelepipedo, piramide, sfera, cilindro, cono.",
         "Se appoggi un solido sulla sabbia o lo ricalchi, la sua faccia lascia una figura piana: il cubo un quadrato, il cilindro un cerchio.",
         "Sfera, cilindro e cono hanno parti curve e possono rotolare."],
        [("Un dado da gioco", ["ha 6 facce quadrate", "non rotola"], "è un cubo")],
        [["Chiamare «quadrato» un rettangolo", "Nel quadrato i 4 lati sono tutti uguali."],
         ["Chiamare «cerchio» una palla", "La palla è un solido: è una sfera."],
         ["Contare due volte lo stesso vertice", "Segna ogni vertice con il dito mentre conti."]])
    faq = [("Che differenza c’è tra una figura piana e un solido?", "La figura piana si disegna sul foglio; il solido ha anche lo spessore e si può prendere in mano."),
           ("Come si possono esplorare i solidi a casa?", "Cercando scatole, palle, barattoli e coni del gelato: si contano le facce e si prova a farli rotolare.")]
    make_unit(R, "figure-e-solidi", "S",
              "Riconoscere, denominare e descrivere figure geometriche piane e solide; individuarle negli oggetti dell’ambiente",
              "Figure piane e solidi", "Figure e solidi",
              "Schede di matematica per la classe seconda su figure piane e solidi: quadrato, rettangolo, triangolo, cerchio, lati e vertici, cubo, sfera, cilindro, cono, piramide, impronte e oggetti. 100 esercizi con soluzioni.",
              "Le figure piane sono piatte, i solidi occupano spazio.", "Sfera, cilindro e cono rotolano.",
              body, faq, sets, 16, grade=G)


if __name__ == "__main__":
    main()
