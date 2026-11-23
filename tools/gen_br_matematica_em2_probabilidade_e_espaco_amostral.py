# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Probabilidade e espaço amostral (EM13MAT311, EM13MAT511)
  python3 tools/gen_br_matematica_em2_probabilidade_e_espaco_amostral.py
Espaço amostral e eventos; probabilidade em espaços equiprováveis e não equiprováveis (dado viciado, roleta com setores diferentes);
probabilidade com contagem (combinações); união de eventos P(A ∪ B) = P(A) + P(B) − P(A ∩ B); evento complementar.
Usa geradores do 8º ano (complementar) e do 9º ano (espaço amostral) com outro sorteio.
Erros: tratar resultados não equiprováveis como iguais, somar P(A) + P(B) sem tirar a interseção, contar a ordem quando não importa.
"""
import random
import math
from fractions import Fraction as F
from br_em import M, d, fq, bank, mix, lesson, use, unit, tab, num

R = random.Random(92013)
p_esp = use("gen_br_matematica_9_probabilidade", 92910, "s1_espaco")
p_comp = use("gen_br_matematica_8_probabilidade", 92911, "s1_complementar")


def s1_classica():
    k = R.choice(["dado", "cartas", "numeros", "dois_dados"])
    if k == "dado":
        ev, fav = R.choice([("um número primo", 3), ("um múltiplo de 3", 2), ("um número maior que 4", 2), ("um número par", 3), ("um divisor de 6", 4), ("um número menor que 3", 2)])
        p = F(fav, 6)
        return M("Lançando um dado comum, qual é a probabilidade de sair %s?" % ev, fq(p), [fq(F(fav, 12)), fq(1 - p) if 1 - p != p else fq(F(1, 6)), fq(F(1, fav)) if F(1, fav) != p else fq(F(5, 6))], "%d resultados favoráveis em 6: <b>%s</b>." % (fav, fq(p)))
    if k == "numeros":
        n = R.choice([20, 30, 50, 100])
        m = R.choice([3, 4, 5, 6, 7])
        fav = n // m
        return M("Sorteia-se um número de 1 a %d. Qual é a probabilidade de ser múltiplo de %d?" % (n, m), fq(F(fav, n)), [fq(F(1, m) + F(1, n)) if F(fav, n) != F(1, m) + F(1, n) else fq(F(fav + 1, n)), fq(F(m, n)), fq(F(fav + 1, n))], "Há %d múltiplos de %d: <b>%s</b>." % (fav, m, fq(F(fav, n))))
    if k == "dois_dados":
        s = R.randint(3, 11)
        fav = 6 - abs(7 - s)
        return M("Lançando dois dados, qual é a probabilidade de a soma ser %d?" % s, fq(F(fav, 36)), [fq(F(1, 11)), fq(F(fav, 12)) if F(fav, 12) != F(fav, 36) else fq(F(1, 6)), fq(F(1, 36)) if fav != 1 else fq(F(2, 36))], "%d pares em 36: <b>%s</b>." % (fav, fq(F(fav, 36))))
    ev, fav = R.choice([("um ás", 4), ("uma carta de copas", 13), ("uma figura (valete, dama ou rei)", 12), ("um rei de espadas", 1), ("uma carta vermelha", 26)])
    return M("De um baralho de 52 cartas, tira-se uma carta. Qual é a probabilidade de ser %s?" % ev, fq(F(fav, 52)), [fq(F(1, fav)) if fav > 1 else fq(F(1, 13)), fq(F(fav, 13)) if fav < 13 else fq(F(1, 4) + F(1, 13)), fq(F(52 - fav, 52))], "%d cartas em 52: <b>%s</b>." % (fav, fq(F(fav, 52))))


def s2_nao_equi():
    k = R.choice(["viciado", "roleta", "urna"])
    if k == "viciado":
        m = R.choice([2, 3, 4, 5])
        f = R.choice([1, 6, 3])
        p = F(m, 5 + m)
        return M("Um dado é viciado: o %d sai %d vezes mais que cada um dos outros números (que têm a mesma chance entre si). Qual é a probabilidade de sair %d?" % (f, m, f), fq(p), [fq(F(1, 6)), fq(F(m, 6)), fq(F(1, 5 + m)), fq(F(5, 5 + m))],
                 "Pesos: cinco números com peso 1 e o %d com peso %d (total %d): P = <b>%s</b>." % (f, m, 5 + m, fq(p)))
    if k == "roleta":
        angs = R.choice([(180, 90, 90), (120, 120, 120), (180, 120, 60), (90, 90, 180), (240, 60, 60), (150, 150, 60), (60, 120, 180), (90, 180, 90)])
        cores = ["azul", "verde", "amarelo"]
        i = R.randrange(3)
        p = F(angs[i], 360)
        return M("Uma roleta tem setores azul (%d°), verde (%d°) e amarelo (%d°). Qual é a probabilidade de parar no %s?" % (angs[0], angs[1], angs[2], cores[i]), fq(p), [fq(F(1, 3)), fq(F(angs[i], 180)), fq(1 - p), fq(F(1, 4)), fq(F(2, 3)), fq(F(1, 2))], "%d° de 360°: <b>%s</b>." % (angs[i], fq(p)))
    a, b = R.sample(range(1, 9), 2)
    return M("Numa urna há %d bolas brancas e %d bolas pretas. Os resultados «branca» e «preta» são equiprováveis?" % (a, b), "não, P(branca) = %s e P(preta) = %s" % (fq(F(a, a + b)), fq(F(b, a + b))),
             ["sim, cada um tem 1/2", "sim, porque são duas cores", "não, P(branca) = %s e P(preta) = %s" % (fq(F(b, a + b)), fq(F(a, a + b)))],
             "<b>Não</b>: P(branca) = %d/%d = %s." % (a, a + b, fq(F(a, a + b))))


def s3_combinacao():
    k = R.choice(["urna", "comissao", "loteria"])
    if k == "urna":
        b, v = R.randint(3, 7), R.randint(3, 7)
        p = F(math.comb(b, 2), math.comb(b + v, 2))
        return M("Uma urna tem %d bolas brancas e %d vermelhas. Tiram-se 2 bolas ao mesmo tempo. Qual é a probabilidade de as duas serem brancas?" % (b, v), fq(p), [fq(F(b, b + v) ** 2), fq(F(b, b + v)), fq(F(math.comb(b, 2), math.comb(b + v, 2) + 1))], "C(%d, 2) ÷ C(%d, 2) = %d ÷ %d = <b>%s</b>." % (b, b + v, math.comb(b, 2), math.comb(b + v, 2), fq(p)))
    if k == "comissao":
        g, m = R.randint(3, 6), R.randint(3, 6)
        p = F(math.comb(g, 1) * math.comb(m, 1), math.comb(g + m, 2))
        return M("De %d meninas e %d meninos, sorteiam-se 2 pessoas. Qual é a probabilidade de sair um menino e uma menina?" % (g, m), fq(p), [fq(F(1, 2)) if p != F(1, 2) else fq(F(1, 4)), fq(F(g * m, (g + m) ** 2)), fq(F(2, g + m))], "%d · %d ÷ C(%d, 2) = %d ÷ %d = <b>%s</b>." % (g, m, g + m, g * m, math.comb(g + m, 2), fq(p)))
    return M("Na Mega-Sena (6 números entre 60), quantas apostas simples diferentes existem?", num(math.comb(60, 6)), [num(math.perm(60, 6)), num(60 * 6), num(60 ** 6)], "C(60, 6) = <b>%s</b>; a chance de acertar com 1 aposta é 1 em %s." % (num(math.comb(60, 6)), num(math.comb(60, 6))))


def s4_uniao():
    k = R.choice(["dado", "num", "tab"])
    if k == "dado":
        return M("Lançando um dado, qual é a probabilidade de sair um número par ou maior que 3?", "2/3", ["1", "1/2", "5/6"], "Par: {2, 4, 6}; maior que 3: {4, 5, 6}; união {2, 4, 5, 6}: <b>4/6 = 2/3</b>.")
    if k == "num":
        n = R.choice([20, 30, 60])
        a, b = R.choice([(2, 3), (2, 5), (3, 5), (3, 4)])
        pa, pb, pab = n // a, n // b, n // (a * b)
        p = F(pa + pb - pab, n)
        return M("Sorteia-se um número de 1 a %d. Qual é a probabilidade de ser múltiplo de %d ou de %d?" % (n, a, b), fq(p), [fq(F(pa + pb, n)), fq(F(pab, n)), fq(F(1, a) * F(1, b)), fq(F(pa, n)), fq(F(pb, n)), fq(1 - p)], "%d + %d − %d (múltiplos de %d) = %d em %d: <b>%s</b>." % (pa, pb, pab, a * b, pa + pb - pab, n, fq(p)))
    tot = R.choice([40, 50, 100])
    a = R.randint(10, tot // 2)
    b = R.randint(10, tot // 2)
    ab = R.randint(2, min(a, b) - 1)
    p = F(a + b - ab, tot)
    return M("Numa turma de %d alunos, %d jogam futebol, %d jogam vôlei e %d jogam os dois. Sorteando um aluno, qual é a probabilidade de jogar futebol ou vôlei?" % (tot, a, b, ab), fq(p), [fq(F(a + b, tot)), fq(F(ab, tot)), fq(1 - p)], "(%d + %d − %d) ÷ %d = <b>%s</b>." % (a, b, ab, tot, fq(p)))


s5_conceitos = bank(R, [
    ("Um espaço amostral é equiprovável quando…", "todos os resultados têm a mesma probabilidade", ["tem poucos resultados", "tem resultados impossíveis", "os resultados são números"]),
    ("Lançando duas moedas, os resultados «duas caras», «duas coroas» e «uma de cada» são…", "não equiprováveis (1/4, 1/4 e 1/2)", ["equiprováveis (1/3 cada)", "impossíveis", "todos com probabilidade 1/2"]),
    ("P(A ∪ B) = P(A) + P(B) quando A e B…", "não têm resultados em comum (são mutuamente exclusivos)", ["são independentes", "são complementares sempre", "têm a mesma probabilidade"]),
    ("A soma das probabilidades de todos os resultados do espaço amostral é…", "1", ["0", "100", "o número de resultados"]),
    ("Escolher um ponto ao acaso num segmento de 10 cm e ele cair nos primeiros 3 cm tem probabilidade…", "3/10", ["1/3", "3", "1/10"]),
    ("Um espaço amostral com infinitos resultados contínuos (como um ponto num segmento) é…", "contínuo", ["discreto e finito", "vazio", "equiprovável e finito"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Espaço amostral e probabilidade", mix(R, seen, [(p_esp, 8), (s1_classica, 12)])),
        ("Probabilidade clássica", mix(R, seen, [(s1_classica, 16), (p_comp, 4)])),
        ("Resultados não equiprováveis", mix(R, seen, [(s2_nao_equi, 14), (s5_conceitos, 6)])),
        ("Probabilidade com combinações", mix(R, seen, [(s3_combinacao, 20)])),
        ("União de eventos", mix(R, seen, [(s4_uniao, 16), (p_comp, 4)])),
    ]
    body = lesson(
        ["<b>Espaço amostral</b>: todos os resultados possíveis. Num espaço <b>equiprovável</b>, P(A) = casos favoráveis ÷ casos possíveis.",
         "Quando os resultados <b>não</b> têm a mesma chance (dado viciado, roleta com setores diferentes), use os pesos ou as frações de cada um.",
         "Com sorteios de vários elementos ao mesmo tempo, conte com <b>combinações</b>: P = C(favoráveis) ÷ C(total).",
         "<b>União</b>: P(A ∪ B) = P(A) + P(B) − P(A ∩ B). <b>Complementar</b>: P(não A) = 1 − P(A)."],
        [("Urna: 4 brancas e 6 pretas; 2 bolas ao mesmo tempo, ambas brancas", ["C(4, 2) ÷ C(10, 2) = 6 ÷ 45"], "2/15"),
         ("1 a 30: múltiplo de 2 ou de 3", ["15 + 10 − 5 = 20"], "20/30 = 2/3")],
        [["Tratar resultados diferentes como iguais", "Veja se cada resultado tem mesmo peso."],
         ["Somar sem tirar a interseção", "Quem está nos dois foi contado duas vezes."],
         ["Contar a ordem num sorteio simultâneo", "Tirar ao mesmo tempo: combinação."]])
    faq = [("O que é um espaço amostral equiprovável?", "É aquele em que todos os resultados têm a mesma chance, como um dado não viciado. Aí P(A) = casos favoráveis ÷ casos possíveis."),
           ("O que a BNCC pede?", "Identificar e descrever o espaço amostral de eventos aleatórios, realizando contagem das possibilidades, para resolver e elaborar problemas que envolvem o cálculo da probabilidade (EM13MAT311), e reconhecer a existência de diferentes tipos de espaços amostrais, discretos ou não, e de eventos, equiprováveis ou não, e investigar implicações no cálculo de probabilidades (EM13MAT511).")]
    unit(R, "probabilidade-e-espaco-amostral", "E", ["EM13MAT311", "EM13MAT511"],
         "Identificar e descrever o espaço amostral de eventos aleatórios, realizando contagem das possibilidades, para resolver e elaborar problemas que envolvem o cálculo da probabilidade; reconhecer a existência de diferentes tipos de espaços amostrais, discretos ou não, e de eventos, equiprováveis ou não, e investigar implicações no cálculo de probabilidades",
         "Probabilidade e espaço amostral", "Probabilidade e espaço amostral",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre probabilidade: espaço amostral, eventos equiprováveis e não equiprováveis, probabilidade com combinações, união de eventos e complementar. 100 exercícios com gabarito.",
         "P(A) = favoráveis ÷ possíveis", "P(A ∪ B) = P(A) + P(B) − P(A ∩ B).",
         body, faq, sets, 13, grade="2-serie")


if __name__ == "__main__":
    main()
