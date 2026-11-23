# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Proporcionalidade direta e inversa (Álgebra, EF07MA17)
  python3 tools/gen_br_matematica_7_proporcionalidade.py
Grandezas diretamente e inversamente proporcionais; tabelas; regra de três simples; razão e proporção (propriedade fundamental);
escalas e receitas.
Usa geradores do 9º ano (grandezas proporcionais) com outro sorteio.
Erros: usar a regra direta quando é inversa, achar que toda relação crescente é proporcional, montar a proporção invertida.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, bank, unit

R = random.Random(87010)
p_tipo, p_tab, p_dir, p_inv = use("gen_br_matematica_9_grandezas_proporcionais", 87910, "s1_tipo", "s1_tabela", "s2_direta", "s3_inversa")


def s1_proporcao():
    a, b = R.randint(2, 9), R.randint(2, 12)
    m = R.randint(2, 6)
    c, e = a * m, b * m
    pos = R.choice([0, 1, 2, 3])
    vals = [a, b, c, e]
    ans = vals[pos]
    vs = [str(v) for v in vals]
    vs[pos] = "x"
    q = "Na proporção %s/%s = %s/%s, qual é o valor de x?" % tuple(vs)
    other = {0: F(b * c, e), 1: F(a * e, c), 2: F(a * e, b), 3: F(b * c, a)}[pos]
    return M(q, d(ans), [d(ans + 1), d(F(vals[{0: 1, 1: 0, 2: 3, 3: 2}[pos]] * vals[{0: 2, 1: 3, 2: 0, 3: 1}[pos]], vals[{0: 3, 1: 2, 2: 1, 3: 0}[pos]]), 1), d(ans * 2)],
             "Produto dos meios = produto dos extremos: x = <b>%s</b>." % d(other))


def s2_razao():
    k = R.choice(["escala", "velocidade", "receita"])
    if k == "escala":
        e, cm = R.choice([100, 200, 500, 1000]), R.randint(2, 12)
        return M("Num desenho na escala 1 : %s, um muro mede %d cm. Quantos metros mede o muro real?" % (d(e), cm), "%s m" % d(F(cm * e, 100)), ["%s m" % d(F(cm * e, 10)), "%s m" % d(cm * e), "%s m" % d(F(cm * e, 1000), 3)],
                 "%d × %s = %s cm = <b>%s m</b>." % (cm, d(e), d(cm * e), d(F(cm * e, 100))))
    if k == "velocidade":
        v, t = R.choice([60, 80, 90, 100]), R.randint(2, 5)
        t2 = R.randint(2, 8)
        if t2 == t:
            return None
        return M("Um carro, sempre na mesma velocidade, percorre %d km em %d horas. Quantos km percorre em %d horas?" % (v * t, t, t2), "%d km" % (v * t2), ["%d km" % (v * t + t2 - t), "%s km" % d(F(v * t * t, t2), 1), "%d km" % (v * t * t2)],
                 "Direta: %d km por hora; %d × %d = <b>%d km</b>." % (v, v, t2, v * t2))
    o, n = R.choice([(4, 6), (6, 9), (8, 12), (4, 10), (6, 15)])
    g = R.choice([200, 300, 240, 120])
    return M("Uma receita para %d pessoas usa %d g de farinha. Quanto de farinha para %d pessoas?" % (o, g, n), "%s g" % d(F(g * n, o)), ["%d g" % (g + n - o), "%s g" % d(F(g * o, n), 1), "%d g" % (g * n)],
             "%d ÷ %d = %s g por pessoa; × %d = <b>%s g</b>." % (g, o, d(F(g, o), 1), n, d(F(g * n, o))))


s3_conceitos = bank(R, [
    ("Em uma proporção a/b = c/d, vale sempre…", "a · d = b · c", ["a + d = b + c", "a · b = c · d", "a/d = b/c"]),
    ("Se x e y são diretamente proporcionais e x dobra, y…", "dobra", ["cai pela metade", "não muda", "aumenta 2"]),
    ("Se x e y são inversamente proporcionais e x triplica, y…", "fica dividido por 3", ["triplica", "não muda", "aumenta 3"]),
    ("Na proporção direta, o que é constante?", "o quociente y ÷ x", ["o produto x · y", "a soma x + y", "a diferença y − x"]),
    ("Na proporção inversa, o que é constante?", "o produto x · y", ["o quociente y ÷ x", "a soma x + y", "a diferença"]),
    ("O lado de um quadrado e a sua área são grandezas…", "não proporcionais", ["diretamente proporcionais", "inversamente proporcionais", "iguais"]),
], "s3_conceitos")


def main():
    seen = set()
    sets = [
        ("Direta, inversa ou nenhuma?", mix(R, seen, [(p_tipo, 8), (p_tab, 8), (s3_conceitos, 4)])),
        ("Proporções", mix(R, seen, [(s1_proporcao, 20)])),
        ("Grandezas diretamente proporcionais", mix(R, seen, [(p_dir, 12), (s2_razao, 8)])),
        ("Grandezas inversamente proporcionais", mix(R, seen, [(p_inv, 20)])),
        ("Revisão", mix(R, seen, [(s2_razao, 8), (p_dir, 4), (p_inv, 4), (s3_conceitos, 2), (p_tab, 2)])),
    ]
    body = lesson(
        ["Duas grandezas são <b>diretamente proporcionais</b> quando uma dobra e a outra também dobra (y ÷ x é constante).",
         "São <b>inversamente proporcionais</b> quando uma dobra e a outra cai pela metade (x · y é constante).",
         "Numa <b>proporção</b> a/b = c/d, o produto dos extremos é igual ao produto dos meios: a · d = b · c. Isso resolve a regra de três."],
        [("3/5 = x/20", ["5x = 60"], "x = 12"),
         ("4 torneiras: 6 h. 3 torneiras?", ["inversa: 4 · 6 = 3 · x"], "8 h")],
        [["Usar a direta na inversa", "Pergunte: se uma aumenta, a outra aumenta ou diminui?"],
         ["Achar que tudo que cresce é proporcional", "Lado e área de um quadrado não são proporcionais."],
         ["Montar a proporção invertida", "Mantenha a mesma ordem das grandezas nas duas razões."]])
    faq = [("Como saber se a regra de três é direta ou inversa?", "Pense no que acontece quando uma grandeza aumenta: se a outra também aumenta na mesma proporção, é direta; se diminui na mesma proporção, é inversa."),
           ("O que a BNCC pede no 7º ano?", "Resolver e elaborar problemas que envolvam variação de proporcionalidade direta e de proporcionalidade inversa entre duas grandezas, utilizando sentença algébrica para expressar a relação entre elas (EF07MA17).")]
    unit(R, "proporcionalidade-direta-e-inversa", "A", ["EF07MA17"],
         "Resolver e elaborar problemas que envolvam variação de proporcionalidade direta e de proporcionalidade inversa entre duas grandezas, utilizando sentença algébrica para expressar a relação entre elas",
         "Proporcionalidade direta e inversa", "Proporcionalidade",
         "Atividades de matemática para o 7º ano sobre proporcionalidade: grandezas diretamente e inversamente proporcionais, proporções, regra de três, escalas e receitas. 100 exercícios com gabarito.",
         "Direta: y ÷ x constante. Inversa: x · y constante.", "a/b = c/d → a · d = b · c",
         body, faq, sets, 10, grade="7-ano")


if __name__ == "__main__":
    main()
