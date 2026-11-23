# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Problemas de contagem (Números, EF04MA08)
  python3 tools/gen_br_matematica_4_problemas_de_contagem.py
Combinar cada elemento de uma coleção com todos os elementos de outra (roupas, lanches, caminhos); listas, tabelas de dupla entrada
e árvore de possibilidades; formar números com algarismos; problemas. Usa os geradores do 5º ano com outro sorteio.
Erros: somar em vez de multiplicar, esquecer combinações na lista, contar duas vezes a mesma combinação.
"""
import random
import gen_br_matematica_5_problemas_de_contagem as C5
from br_common import lesson, make_unit, mix, use

R = random.Random(80407)
M = "gen_br_matematica_5_problemas_de_contagem"
s1_dois, s1_tabela, s2_arvore, s2_lista, s3_falta, s4_numeros, s5_problema = use(M, 80947, "s1_dois", "s1_tabela", "s2_arvore", "s2_lista", "s3_falta", "s4_numeros", "s5_problema")


def main():
    seen = set()
    sets = [
        ("Combinar duas coleções", mix(R, seen, [(s1_dois, 20)])),
        ("Listas e tabelas", mix(R, seen, [(s2_lista, 10), (s1_tabela, 10)])),
        ("Árvore de possibilidades", mix(R, seen, [(s2_arvore, 14), (s3_falta, 6)])),
        ("Formar números e senhas", mix(R, seen, [(s4_numeros, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para contar todas as combinações, junte <b>cada</b> elemento de um grupo com <b>todos</b> os elementos do outro.",
         "3 camisetas e 2 bermudas: cada camiseta vai com 2 bermudas → 3 × 2 = 6 maneiras de se vestir.",
         "Uma <b>lista organizada</b>, uma <b>tabela</b> ou uma <b>árvore de possibilidades</b> ajudam a não esquecer nenhuma combinação."],
        [("2 tipos de pão e 4 recheios. Quantos sanduíches diferentes?", ["cada pão com os 4 recheios", "2 × 4"], "8"),
         ("Quantos números de 2 algarismos diferentes com 1, 3 e 5?", ["dezenas: 3 escolhas", "unidades: sobram 2", "3 × 2"], "6")],
        [["Somar em vez de multiplicar: 3 + 2 = 5", "Cada camiseta combina com todas as bermudas: 3 × 2 = 6."],
         ["Esquecer combinações na lista", "Faça a lista em ordem: primeiro tudo com a camiseta branca, depois com a azul…"],
         ["Repetir algarismos quando não pode", "Depois de usar um algarismo, sobra um a menos."]],
        C5.arvore(["branca", "azul", "verde"], ["jeans", "cinza"]))
    faq = [("O que são problemas de contagem no 4º ano?", "São problemas em que se combina cada elemento de uma coleção com todos os elementos de outra, por exemplo roupas ou lanches, usando listas, tabelas e árvores de possibilidades."),
           ("Por que a resposta é uma multiplicação?", "Porque cada escolha do primeiro grupo se repete com todas as escolhas do segundo grupo: são grupos iguais, como na tabuada.")]
    make_unit(R, "problemas-de-contagem", "N", ["EF04MA08"],
              "Resolver, com o suporte de imagem e/ou material manipulável, problemas simples de contagem, como a determinação do número de agrupamentos possíveis ao se combinar cada elemento de uma coleção com todos os elementos de outra, utilizando estratégias e formas de registro pessoais",
              "Problemas de contagem: combinações, tabelas e árvore de possibilidades", "Problemas de contagem",
              "Atividades de matemática para o 4º ano sobre problemas de contagem: combinações de roupas e lanches, listas, tabelas, árvore de possibilidades, números e senhas. 100 exercícios com gabarito.",
              "Cada elemento com todos os outros: multiplique.", "3 camisetas × 2 bermudas = 6 maneiras.",
              body, faq, sets, 7, grade="4-ano")


if __name__ == "__main__":
    main()
