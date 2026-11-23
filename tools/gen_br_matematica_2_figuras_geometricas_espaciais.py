# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Figuras geométricas espaciais (Geometria, EF02MA14)
  python3 tools/gen_br_matematica_2_figuras_geometricas_espaciais.py
Cubo, bloco retangular, pirâmide, cone, cilindro e esfera: nome, objetos do dia a dia com a mesma forma,
rola ou não rola, faces planas e curvas, comparar figuras, construções com cubinhos.
Usa geradores do 3º ano (figuras espaciais) com outro sorteio, sem planificações e prismas.
Erros: chamar o cubo de quadrado, achar que o cilindro tem ponta, confundir cone e pirâmide.
"""
import random
from br_common import mcq, lesson, make_unit, mix, use, solido_svg, fig

R = random.Random(80213)
M3 = "gen_br_matematica_3_figuras_geometricas_espaciais"


def sem_plan(it):
    t = it["q"] + it["e"] + "".join(it["c"])
    return "planifica" not in t and "prisma" not in t and "aresta" not in t.lower()


e_nome, e_objeto, e_quiz, e_alto, e_total, e_faces = use(M3, 80908, "s1_nome", "s1_objeto", "s2_quiz", "s4_alto", "s4_total", "s5_faces", preds=(sem_plan,))
NOMES = {"cubo": "cubo", "bloco": "bloco retangular", "piramide": "pirâmide", "cone": "cone", "cilindro": "cilindro", "esfera": "esfera"}

ROLA = [("Qual destas figuras rola para todos os lados?", "esfera", ["cubo", "pirâmide", "bloco retangular"]),
        ("Qual destas figuras rola, mas também fica em pé sobre uma base plana sem ponta?", "cilindro", ["esfera", "cubo", "pirâmide"]),
        ("Um dado, uma bola e uma lata: qual tem a forma de uma figura que NÃO rola?", "cubo", ["esfera", "cilindro", "cone"]),
        ("Qual figura com ponta NÃO rola de jeito nenhum?", "pirâmide", ["esfera", "cilindro", "cone"]),
        ("Que figura tem a forma de um tijolo e não rola?", "bloco retangular", ["esfera", "cilindro", "cone"]),
        ("Que figura tem uma ponta e uma base redonda?", "cone", ["cilindro", "pirâmide", "esfera"]),
        ("Que figura tem uma ponta e faces que são triângulos?", "pirâmide", ["cone", "cubo", "cilindro"]),
        ("Que figura não tem nenhuma parte plana?", "esfera", ["cilindro", "cone", "cubo"]),
        ("Que figura tem todas as faces quadradas e iguais?", "cubo", ["bloco retangular", "pirâmide", "cilindro"]),
        ("Que figura tem duas bases redondas iguais?", "cilindro", ["cone", "esfera", "cubo"]),
        ("Que figura se parece com uma caixa de sapatos?", "bloco retangular", ["cubo", "cilindro", "pirâmide"]),
        ("Empilhando figuras iguais, qual forma uma torre bem firme?", "cubo", ["esfera", "cone", "pirâmide"])]


def s3_rola():
    q, a, w = R.choice(ROLA)
    return mcq(q, a, w, "Pense na forma: partes curvas rolam, partes planas apoiam. Resposta: <b>%s</b>." % a)


def s3_qual_figura():
    k = R.choice(sorted(NOMES))
    pic = fig(solido_svg(k))
    return mcq(pic + "Como se chama esta figura?", NOMES[k], [NOMES[x] for x in sorted(NOMES) if x != k], "Esta figura é <b>%s</b>." % ("o " + NOMES[k] if k not in ("piramide", "esfera") else "a " + NOMES[k]))


def s4_comparar():
    pares = [("cubo", "bloco retangular", "o cubo tem todas as faces quadradas e iguais", ["o cubo rola", "o bloco tem ponta", "não há diferença"]),
             ("cone", "pirâmide", "a base do cone é redonda e a da pirâmide não", ["o cone não tem ponta", "a pirâmide rola", "não há diferença"]),
             ("cilindro", "cone", "o cilindro tem duas bases redondas e o cone tem uma", ["o cilindro tem ponta", "o cone não rola", "não há diferença"]),
             ("esfera", "cilindro", "a esfera não tem nenhuma parte plana", ["a esfera tem duas bases", "o cilindro rola para todos os lados", "não há diferença"]),
             ("cubo", "pirâmide", "a pirâmide tem uma ponta e o cubo não", ["o cubo tem ponta", "a pirâmide rola", "não há diferença"])]
    a, b, ok, w = R.choice(pares)
    return mcq("Qual é uma diferença entre %s e %s?" % (("o " if a not in ("esfera",) else "a ") + a, ("o " if b not in ("pirâmide",) else "a ") + b), ok, w, "Resposta: <b>%s</b>." % ok)


def main():
    seen = set()
    sets = [
        ("Nome das figuras espaciais", mix(R, seen, [(e_nome, 10), (s3_qual_figura, 6), (e_objeto, 4)])),
        ("Objetos do dia a dia", mix(R, seen, [(e_objeto, 14), (e_nome, 6)])),
        ("Rola ou não rola?", mix(R, seen, [(s3_rola, 12), (e_quiz, 6), (s4_comparar, 2)])),
        ("Comparar figuras", mix(R, seen, [(s4_comparar, 3), (e_faces, 7), (e_nome, 4), (e_alto, 6)])),
        ("Construções com cubinhos", mix(R, seen, [(e_alto, 6), (e_total, 14)])),
    ]
    body = lesson(
        ["As <b>figuras espaciais</b> ocupam lugar no espaço: cubo, bloco retangular, pirâmide, cone, cilindro e esfera.",
         "A <b>esfera</b> (como uma bola) rola para todos os lados. O <b>cilindro</b> (como uma lata) rola e também fica em pé.",
         "O <b>cone</b> (como um chapéu de festa) tem ponta e base redonda. A <b>pirâmide</b> tem ponta e faces triangulares.",
         "O <b>cubo</b> (como um dado) tem 6 faces quadradas iguais. O <b>bloco retangular</b> parece uma caixa de sapatos."],
        [("Uma lata de milho tem a forma de…", ["duas bases redondas", "rola e fica em pé"], "cilindro"),
         ("Um dado tem a forma de…", ["6 faces quadradas iguais"], "cubo")],
        [["Chamar o cubo de quadrado", "O quadrado é plano; o cubo ocupa espaço."],
         ["Achar que o cilindro tem ponta", "Quem tem ponta é o cone."],
         ["Confundir cone e pirâmide", "A base do cone é redonda; a da pirâmide tem lados retos."]],
        fig(solido_svg("cilindro")) + fig(solido_svg("cone")) + fig(solido_svg("cubo")))
    faq = [("Que figuras espaciais o 2º ano estuda?", "A BNCC pede reconhecer, nomear e comparar cubo, bloco retangular, pirâmide, cone, cilindro e esfera, relacionando-os com objetos do mundo físico."),
           ("Como ensinar em casa?", "Procure objetos com essas formas: bola (esfera), lata (cilindro), caixa de sapatos (bloco retangular), dado (cubo), casquinha de sorvete (cone). Veja quais rolam.")]
    make_unit(R, "figuras-geometricas-espaciais", "G", ["EF02MA14"],
              "Reconhecer, nomear e comparar figuras geométricas espaciais (cubo, bloco retangular, pirâmide, cone, cilindro e esfera), relacionando-as com objetos do mundo físico",
              "Figuras geométricas espaciais: cubo, cone, cilindro e esfera", "Figuras espaciais",
              "Atividades de matemática para o 2º ano sobre figuras geométricas espaciais: cubo, bloco retangular, pirâmide, cone, cilindro e esfera, objetos do dia a dia e o que rola. 100 exercícios com gabarito.",
              "Bola: esfera. Lata: cilindro. Dado: cubo.", "Partes curvas rolam; partes planas apoiam.",
              body, faq, sets, 13, grade="2-ano")


if __name__ == "__main__":
    main()
