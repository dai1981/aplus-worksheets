# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Prismas e pirâmides (Geometria, EF04MA17)
  python3 tools/gen_br_matematica_4_prismas_e_piramides.py
Reconhecer e nomear prismas e pirâmides pela base; faces, arestas e vértices; associar a figura à sua planificação;
comparar prismas e pirâmides; objetos do dia a dia. Usa os geradores do 5º ano com outro sorteio.
Erros: chamar todo prisma de cubo, contar só as faces laterais, esquecer as arestas escondidas, confundir cone e pirâmide.
"""
import random
import gen_br_matematica_5_figuras_espaciais_e_planificacoes as F5
from br_common import lesson, make_unit, mix, use

R = random.Random(80413)
M = "gen_br_matematica_5_figuras_espaciais_e_planificacoes"
s_nome, s_base, s_contar, s_qual, s_planif, s_texto, s_comp, s_tab, s_prob = use(M, 80954, "s1_nome", "s1_base", "s2_contar", "s2_qual", "s3_planif", "s3_texto", "s4_comparar", "s4_tabela", "s5_problema")


def main():
    seen = set()
    sets = [
        ("Nomes de prismas e pirâmides", mix(R, seen, [(s_nome, 14), (s_base, 6)])),
        ("Faces, arestas e vértices", mix(R, seen, [(s_contar, 20)])),
        ("Planificações", mix(R, seen, [(s_planif, 12), (s_texto, 8)])),
        ("Comparar prismas e pirâmides", mix(R, seen, [(s_comp, 8), (s_tab, 12)])),
        ("Problemas", mix(R, seen, [(s_qual, 8), (s_prob, 12)])),
    ]
    body = lesson(
        ["Um <b>prisma</b> tem duas bases iguais e faces laterais retangulares. Uma <b>pirâmide</b> tem uma base e faces laterais triangulares que se encontram num vértice.",
         "O nome vem da forma da base: prisma de base triangular, pirâmide de base quadrangular…",
         "<b>Faces</b> são as partes planas; <b>arestas</b> são os segmentos onde duas faces se encontram; <b>vértices</b> são os cantos.",
         "A <b>planificação</b> é a figura aberta no papel: o prisma dá retângulos e 2 bases; a pirâmide dá 1 base e triângulos."],
        [("Quantas faces tem uma pirâmide de base quadrangular?", ["1 base quadrada", "4 triângulos"], "5"),
         ("Planificação com 2 triângulos e 3 retângulos.", ["2 bases triangulares", "faces retangulares"], "prisma de base triangular")],
        [["Contar só as faces laterais", "Some também as bases."],
         ["Esquecer as arestas escondidas", "As linhas tracejadas também são arestas."],
         ["Confundir cone e pirâmide", "O cone tem base redonda; a pirâmide tem base de polígono."]],
        F5.solido("prisma", 3, F5.COL[0]) + F5.solido("piramide", 4, F5.COL[2]))
    faq = [("O que o 4º ano estuda sobre figuras espaciais?", "A BNCC pede associar prismas e pirâmides às suas planificações e analisar, nomear e comparar seus atributos, relacionando as representações planas e espaciais."),
           ("Como contar as arestas de um prisma?", "Conte as arestas da base de baixo, as da base de cima e as laterais. Num prisma de base triangular: 3 + 3 + 3 = 9.")]
    make_unit(R, "prismas-e-piramides", "G", ["EF04MA17"],
              "Associar prismas e pirâmides a suas planificações e analisar, nomear e comparar seus atributos, estabelecendo relações entre as representações planas e espaciais",
              "Prismas e pirâmides: faces, arestas, vértices e planificações", "Prismas e pirâmides",
              "Atividades de matemática para o 4º ano sobre prismas e pirâmides: nomes pela base, faces, arestas e vértices, planificações e comparação. 100 exercícios com gabarito.",
              "Prisma: 2 bases e faces retangulares. Pirâmide: 1 base e faces triangulares.", "O nome vem da forma da base.",
              body, faq, sets, 13, grade="4-ano")


if __name__ == "__main__":
    main()
