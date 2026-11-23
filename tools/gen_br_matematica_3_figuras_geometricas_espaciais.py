# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Figuras geométricas espaciais (Geometria, EF03MA13, EF03MA14)
  python3 tools/gen_br_matematica_3_figuras_geometricas_espaciais.py
Cubo, bloco retangular, pirâmide, cone, cilindro e esfera; objetos do dia a dia; faces, arestas e vértices;
formas das faces; planificações (cubo, bloco, pirâmide, cilindro, cone); empilhamento de cubinhos.
Erros: chamar a esfera de círculo, confundir cone e pirâmide, contar a mesma aresta duas vezes.
"""
import random
import gen_de_mathe_k3_koerper_und_figuren as DE
from br_common import mcq, lesson, make_unit, mix, solido_svg, table

R = random.Random(80314)
NOME = {"cubo": "cubo", "bloco": "bloco retangular", "esfera": "esfera", "cilindro": "cilindro", "cone": "cone", "piramide": "pirâmide"}
ART = {"cubo": "um cubo", "bloco retangular": "um bloco retangular", "esfera": "uma esfera", "cilindro": "um cilindro", "cone": "um cone", "pirâmide": "uma pirâmide"}
FAV = {"o cubo": (6, 12, 8), "o bloco retangular": (6, 12, 8), "a pirâmide de base quadrada": (5, 8, 5), "a pirâmide de base triangular": (4, 6, 4),
       "o prisma de base triangular": (5, 9, 6)}


def s1_nome():
    k = R.choice(sorted(NOME))
    col = R.choice(["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"])
    ans = NOME[k]
    conf = {"cubo": "bloco retangular", "bloco": "cubo", "esfera": "círculo", "cilindro": "cone", "cone": "pirâmide", "piramide": "cone"}[k]
    w = [conf] + [n for n in sorted(NOME.values()) if n not in (ans, conf)]
    why = {"cubo": "Tem 6 faces quadradas iguais.", "bloco": "Tem 6 faces retangulares, nem todas iguais.",
           "esfera": "É toda arredondada, sem faces planas.", "cilindro": "Tem dois círculos iguais e uma parte curva.",
           "cone": "Tem um círculo e uma ponta.", "piramide": "As faces laterais são triângulos que se encontram numa ponta."}[k]
    return mcq(solido_svg(k, R.choice([28, 32, 36]), col) + "Qual é o nome desta figura geométrica espacial?", ans, w, "%s É <b>%s</b>." % (why, ART[ans]))


OBJ = [("uma bola de futebol", "esfera"), ("uma laranja", "esfera"), ("uma lata de molho de tomate", "cilindro"), ("uma vela", "cilindro"),
       ("uma caixa de sapatos", "bloco retangular"), ("um tijolo", "bloco retangular"), ("um dado", "cubo"), ("um cubo mágico", "cubo"),
       ("uma casquinha de sorvete", "cone"), ("um chapéu de aniversário", "cone"), ("um cone de trânsito", "cone"), ("uma caixa de leite", "bloco retangular"),
       ("uma bolinha de gude", "esfera"), ("um rolo de papel-toalha", "cilindro"), ("as pirâmides do Egito", "pirâmide"), ("um tubo de cola", "cilindro"),
       ("um copo", "cilindro"), ("uma melancia redonda", "esfera"), ("uma caixa de fósforos", "bloco retangular"), ("um tablete de manteiga", "bloco retangular")]


def s1_objeto():
    thing, ans = R.choice(OBJ)
    w = [x for x in ["esfera", "cilindro", "bloco retangular", "cubo", "cone", "pirâmide"] if x != ans]
    R.shuffle(w)
    v = "parecem" if thing.startswith(("as ", "os ")) else "parece"
    return mcq("Com que figura geométrica espacial se %s %s?" % (v, thing), ans, w, "%s %s %s: <b>%s</b>." % (thing[0].upper() + thing[1:], v, ART[ans], ans))


def s2_contar():
    n = R.choice(sorted(FAV))
    i = R.randint(0, 2)
    word = ["faces", "arestas", "vértices"][i]
    v = FAV[n][i]
    others = [x for x in FAV[n] if x != v] + [v + 2, v - 2, 4]
    return mcq("Quant%s %s tem %s?" % ("as" if word in ("faces", "arestas") else "os", word, n), str(v), [str(x) for x in others if x != v and x > 0],
               "%s tem %d faces, %d arestas e %d vértices. A pergunta é sobre %s: <b>%d</b>." % (n[0].upper() + n[1:], FAV[n][0], FAV[n][1], FAV[n][2],
                                                                                              "as " + word if word != "vértices" else "os vértices", v))


QUIZ = [("Que figura não tem faces planas, nem arestas, nem vértices?", "a esfera", ["o cubo", "o cilindro", "o cone"]),
        ("Que figura tem duas bases em forma de círculo?", "o cilindro", ["o cone", "a esfera", "o bloco retangular"]),
        ("Que figura tem uma ponta (vértice) e uma base em forma de círculo?", "o cone", ["a pirâmide", "o cilindro", "a esfera"]),
        ("Que figura tem 6 faces quadradas e iguais?", "o cubo", ["o bloco retangular", "a pirâmide", "o cilindro"]),
        ("Que figura pode rolar para todos os lados?", "a esfera", ["o cilindro", "o cone", "o cubo"]),
        ("Que figura tem faces triangulares que se encontram num vértice?", "a pirâmide", ["o cone", "o cubo", "o cilindro"]),
        ("Como se chama a linha onde duas faces se encontram?", "aresta", ["vértice", "base", "face"]),
        ("Como se chama o ponto onde as arestas se encontram?", "vértice", ["aresta", "face", "lado"]),
        ("Que figura pode rolar e também ficar em pé, sem ponta?", "o cilindro", ["a esfera", "o cone", "o cubo"]),
        ("Que figuras são «corpos redondos»?", "esfera, cone e cilindro", ["cubo, pirâmide e cone", "cubo e bloco retangular", "pirâmide e cilindro"])]


def s2_quiz():
    q, a, w = R.choice(QUIZ)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


PLAN = [("Uma planificação tem 2 círculos e 1 retângulo. Que figura ela forma?", "o cilindro", ["o cone", "o bloco retangular", "a esfera"]),
        ("Uma planificação tem 6 quadrados iguais. Que figura ela forma?", "o cubo", ["o bloco retangular", "a pirâmide", "o cilindro"]),
        ("Uma planificação tem 1 quadrado e 4 triângulos. Que figura ela forma?", "a pirâmide de base quadrada", ["o cubo", "o cone", "a pirâmide de base triangular"]),
        ("Uma planificação tem 1 círculo e uma parte curva em forma de leque. Que figura ela forma?", "o cone", ["o cilindro", "a pirâmide", "a esfera"]),
        ("Uma planificação tem 6 retângulos, iguais dois a dois. Que figura ela forma?", "o bloco retangular", ["o cubo", "a pirâmide", "o cilindro"]),
        ("Uma planificação tem 4 triângulos iguais. Que figura ela forma?", "a pirâmide de base triangular", ["a pirâmide de base quadrada", "o cone", "o cubo"]),
        ("Uma planificação tem 2 triângulos e 3 retângulos. Que figura ela forma?", "o prisma de base triangular", ["a pirâmide de base triangular", "o bloco retangular", "o cone"]),
        ("Que figura espacial NÃO pode ser planificada (aberta sobre a mesa sem rasgar)?", "a esfera", ["o cubo", "o cilindro", "o cone"]),
        ("Que figuras planas aparecem na planificação de um cilindro?", "2 círculos e 1 retângulo", ["2 círculos e 1 triângulo", "1 círculo e 1 retângulo", "2 retângulos"]),
        ("Que figuras planas aparecem na planificação de uma pirâmide de base quadrada?", "1 quadrado e 4 triângulos", ["4 quadrados e 1 triângulo", "6 quadrados", "1 círculo e 4 triângulos"])]


def s3_plan():
    q, a, w = R.choice(PLAN)
    return mcq(q, a, w, "Monte a figura na imaginação, dobrando as partes: <b>%s</b>." % a)


def s3_cubo():
    it = DE.wuerfelnetz()
    if not it:
        return None
    q = it["q"].replace("aria-label='vier Netze A bis D'", "aria-label='quatro planificações A, B, C, D'")
    good = "Welches Netz kann man zu einem Würfel falten?" in q
    q = q.replace("Welches Netz kann man zu einem Würfel falten?", "Qual planificação pode ser dobrada para formar um cubo?")
    q = q.replace("Drei Netze ergeben einen Würfel. Welches Netz ergibt <b>keinen</b> Würfel?", "Três planificações formam um cubo. Qual <b>não</b> forma um cubo?")
    k = it["c"][0]
    e = ("Com a planificação %s, ao dobrar, cada uma das 6 faces vai para um lugar diferente do cubo." % k if good else
         "Com a planificação %s, ao dobrar, duas faces ficam uma em cima da outra e falta uma face." % k)
    return mcq(q, k, it["c"][1:], e + " Resposta: <b>%s</b>." % k)


def tr(it, pairs):
    if not it:
        return None
    for a, b in pairs:
        it["q"], it["e"] = it["q"].replace(a, b), it["e"].replace(a, b)
        it["c"] = [c.replace(a, b) for c in it["c"]]
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"])


def s4_alto():
    return tr(DE.bauplan_hoch(), [("Bauplan eines Würfelgebäudes: Wie hoch ist der höchste Turm?", "Vista de cima de uma construção de cubinhos: quantos cubinhos tem a torre mais alta?"),
                                  ("Die größte Zahl im Bauplan ist", "O maior número da vista de cima é"), ("Der höchste Turm ist", "A torre mais alta tem"),
                                  (" Würfel</b> hoch.", " cubinhos</b>."), (" Würfel", " cubinhos"), ("aria-label='Bauplan'", "aria-label='vista de cima'")])


def s4_total():
    return tr(DE.bauplan(), [("Ein Bauplan zeigt ein Würfelgebäude von oben. Die Zahl sagt, wie viele Würfel übereinander stehen. Wie viele Würfel sind es?",
                              "A figura mostra uma construção de cubinhos vista de cima. Cada número diz quantos cubinhos estão empilhados. Quantos cubinhos há ao todo?"),
                             ("Addiere alle Zahlen im Bauplan:", "Some todos os números:"), ("aria-label='Bauplan'", "aria-label='vista de cima'")])


FACES = [("Que forma têm as faces do cubo?", "quadrados", ["retângulos não quadrados", "triângulos", "círculos"]),
         ("Que forma têm as faces de um bloco retangular (que não é cubo)?", "retângulos", ["triângulos", "círculos", "losangos"]),
         ("Que forma tem a base do cone?", "círculo", ["quadrado", "triângulo", "retângulo"]),
         ("Que forma têm as faces laterais de uma pirâmide?", "triângulos", ["quadrados", "círculos", "retângulos"]),
         ("Se você contornar com lápis a base de um cilindro, que figura desenha?", "um círculo", ["um quadrado", "um triângulo", "um retângulo"]),
         ("Se você contornar uma face do cubo, que figura desenha?", "um quadrado", ["um círculo", "um triângulo", "um losango"]),
         ("Quantas faces triangulares tem uma pirâmide de base quadrada?", "4", ["5", "3", "8"]),
         ("Quantas arestas saem de cada vértice do cubo?", "3", ["4", "2", "6"])]


def s5_faces():
    q, a, w = R.choice(FACES)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    DE.R = random.Random(80914)
    seen = set()
    sets = [
        ("Nome das figuras espaciais", mix(R, seen, [(s1_nome, 8), (s1_objeto, 12)])),
        ("Faces, arestas e vértices", mix(R, seen, [(s2_contar, 12), (s2_quiz, 8)])),
        ("Planificações", mix(R, seen, [(s3_plan, 10), (s3_cubo, 10)])),
        ("Construções com cubinhos", mix(R, seen, [(s4_alto, 8), (s4_total, 12)])),
        ("Revisão das figuras espaciais", mix(R, seen, [(s5_faces, 8), (s1_objeto, 6), (s2_quiz, 2), (s1_nome, 4)])),
    ]
    body = lesson(
        ["As <b>figuras geométricas espaciais</b> não são planas: têm comprimento, largura e altura. As principais são cubo, bloco retangular, pirâmide, cilindro, cone e esfera.",
         "Nos poliedros (cubo, bloco, pirâmide) há <b>faces</b> (partes planas), <b>arestas</b> (onde duas faces se encontram) e <b>vértices</b> (pontas).",
         "Esfera, cone e cilindro têm partes arredondadas: são os <b>corpos redondos</b>.",
         "A <b>planificação</b> é a figura aberta sobre a mesa: o cilindro tem 2 círculos e 1 retângulo; o cubo tem 6 quadrados."],
        [("Quantos vértices tem o cubo?", ["4 em cima e 4 embaixo"], "8"),
         ("Planificação com 1 quadrado e 4 triângulos", ["Base quadrada e faces triangulares"], "pirâmide de base quadrada")],
        [["Chamar a esfera de círculo", "O círculo é plano; a esfera é espacial (como uma bola)."],
         ["Confundir cone e pirâmide", "O cone tem base redonda; a pirâmide tem base de polígono e faces triangulares."],
         ["Contar a mesma aresta duas vezes", "Conte as arestas de cima, de baixo e as de pé, uma de cada vez: no cubo são 4 + 4 + 4 = 12."]],
        table(["Figura", "Faces", "Arestas", "Vértices"], [["Cubo", "6", "12", "8"], ["Bloco retangular", "6", "12", "8"], ["Pirâmide de base quadrada", "5", "8", "5"]]))
    faq = [("Qual é a diferença entre figura plana e figura espacial?", "A figura plana (quadrado, círculo) está toda no papel. A espacial (cubo, esfera) ocupa espaço, como uma caixa ou uma bola."),
           ("Como ajudar a entender as planificações?", "Desmonte embalagens de verdade (caixa de creme dental, de leite) e veja quais figuras planas aparecem. Depois tente montar de novo.")]
    make_unit(R, "figuras-geometricas-espaciais", "G", ["EF03MA13", "EF03MA14"],
              "Associar figuras geométricas espaciais (cubo, bloco retangular, pirâmide, cone, cilindro e esfera) a objetos do mundo físico e nomear essas figuras; descrever características de algumas figuras geométricas espaciais (prismas retos, pirâmides, cilindros, cones), relacionando-as com suas planificações",
              "Figuras geométricas espaciais e planificações", "Figuras geométricas espaciais",
              "Atividades de matemática para o 3º ano sobre figuras geométricas espaciais: cubo, bloco retangular, pirâmide, cilindro, cone e esfera, faces, arestas e vértices, planificações e construções com cubinhos. 100 exercícios com gabarito.",
              "Faces são planas, arestas são linhas, vértices são pontas.", "Planificação do cilindro: 2 círculos e 1 retângulo.",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
