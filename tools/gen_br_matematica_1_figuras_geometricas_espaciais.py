# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Figuras geométricas espaciais (Geometria, EF01MA13)
  python3 tools/gen_br_matematica_1_figuras_geometricas_espaciais.py
Cone, cilindro, esfera, bloco retangular (e cubo, pirâmide) ligados a objetos do dia a dia; o que rola e o que não rola;
nomes das figuras. Usa geradores do 2º e do 3º ano com outro sorteio.
Erros: chamar a bola de círculo, achar que o cilindro tem ponta, confundir cone e pirâmide.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, solido_svg, fig

R = random.Random(80112)


def basico(it):
    t = it["q"] + it["e"] + "".join(it["c"])
    return all(w not in t for w in ("planifica", "prisma", "aresta", "vértice", "faces", "face "))


e_nome, e_objeto, e_total = use("gen_br_matematica_3_figuras_geometricas_espaciais", 80979, "s1_nome", "s1_objeto", "s4_total", preds=(basico,))
e_rola, e_qual = use("gen_br_matematica_2_figuras_geometricas_espaciais", 80980, "s3_rola", "s3_qual_figura")
OBJ = [("Uma lata de refrigerante parece um…", "cilindro", ["cone", "cubo", "esfera"]),
       ("Uma casquinha de sorvete parece um…", "cone", ["cilindro", "cubo", "bloco retangular"]),
       ("Uma laranja parece uma…", "esfera", ["pirâmide", "caixa", "lata"]),
       ("Uma caixa de leite parece um…", "bloco retangular", ["cone", "cilindro", "esfera"]),
       ("Um chapéu de aniversário parece um…", "cone", ["cubo", "cilindro", "bloco retangular"]),
       ("Um rolo de papel higiênico parece um…", "cilindro", ["cone", "cubo", "esfera"]),
       ("Uma bola de gude parece uma…", "esfera", ["cone", "caixa", "lata"]),
       ("Um tijolo parece um…", "bloco retangular", ["cilindro", "cone", "esfera"]),
       ("Um dado parece um…", "cubo", ["cone", "cilindro", "esfera"]),
       ("Um globo terrestre parece uma…", "esfera", ["pirâmide", "caixa", "lata"])]


def s1_obj():
    q, a, w = R.choice(OBJ)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Que figura é esta?", mix(R, seen, [(e_qual, 6), (e_nome, 14)])),
        ("Objetos do dia a dia", mix(R, seen, [(s1_obj, 10), (e_objeto, 10)])),
        ("Rola ou não rola?", mix(R, seen, [(e_rola, 12), (e_nome, 8)])),
        ("Mais objetos", mix(R, seen, [(e_objeto, 10), (e_nome, 6), (e_total, 4)])),
        ("Construções com cubinhos", mix(R, seen, [(e_total, 20)])),
    ]
    body = lesson(
        ["As figuras espaciais têm volume, como os objetos que pegamos com a mão.",
         "A <b>esfera</b> parece uma bola. O <b>cilindro</b> parece uma lata. O <b>cone</b> parece uma casquinha de sorvete.",
         "O <b>bloco retangular</b> parece uma caixa de sapatos; o <b>cubo</b> parece um dado.",
         "A esfera rola para todos os lados; o cilindro rola e também fica em pé; o cubo não rola."],
        [("Uma lata de milho", ["redonda em cima e embaixo, rola"], "cilindro"),
         ("Uma bola de futebol", ["toda redonda"], "esfera")],
        [["Chamar a bola de círculo", "A bola é uma esfera; o círculo é plano, como um desenho."],
         ["Achar que o cilindro tem ponta", "Quem tem ponta é o cone."],
         ["Confundir cone e pirâmide", "A base do cone é redonda."]],
        fig(solido_svg("esfera")) + fig(solido_svg("cilindro")) + fig(solido_svg("cone")) + fig(solido_svg("bloco")))
    faq = [("Que figuras espaciais o 1º ano estuda?", "A BNCC pede relacionar cones, cilindros, esferas e blocos retangulares a objetos do dia a dia. Muitas escolas também mostram o cubo e a pirâmide."),
           ("Como ensinar em casa?", "Procure em casa uma bola (esfera), uma lata (cilindro), uma caixa (bloco retangular) e um chapéu de festa (cone). Veja quais rolam.")]
    make_unit(R, "figuras-geometricas-espaciais", "G", ["EF01MA13"],
              "Relacionar figuras geométricas espaciais (cones, cilindros, esferas e blocos retangulares) a objetos familiares do mundo físico",
              "Figuras geométricas espaciais: cone, cilindro, esfera e bloco", "Figuras espaciais",
              "Atividades de matemática para o 1º ano sobre figuras geométricas espaciais: cone, cilindro, esfera, bloco retangular e cubo, objetos do dia a dia e o que rola. 100 exercícios com gabarito.",
              "Bola: esfera. Lata: cilindro. Caixa: bloco retangular.", "A esfera rola para todos os lados.",
              body, faq, sets, 12, grade="1-ano")


if __name__ == "__main__":
    main()
