# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Máximo e mínimo da função quadrática (EM13MAT503)
  python3 tools/gen_br_matematica_em1_maximo_e_minimo.py
Valor máximo ou mínimo (yᵥ) e ponto de máximo ou mínimo (xᵥ); imagem; problemas de otimização:
cercado com área máxima, altura máxima de um lançamento, lucro e receita máximos, produto máximo.
Erros: responder xᵥ quando a pergunta é o valor máximo (yᵥ), achar máximo quando a > 0, esquecer o lado da parede no cercado.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, P2, bank, mix, lesson, unit, curva, R2, num

R = random.Random(91006)


def vert(a, b, c):
    xv = F(-b, 2 * a)
    return xv, a * xv * xv + b * xv + c


def s1_valor():
    a = R.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    xv = R.randint(-4, 5)
    yv = R.randint(-9, 12)
    b, c = -2 * a * xv, a * xv * xv + yv
    k = R.choice(["valor", "ponto", "img", "tipo"])
    f = "f(x) = " + P2(a, b, c)
    mm = "máximo" if a < 0 else "mínimo"
    if k == "valor":
        return M("Qual é o valor %s de %s?" % (mm, f), d(yv), [d(xv) if xv != yv else d(yv + 1), d(c), d(-yv) if yv else "1"], "xᵥ = −b ÷ 2a = %s; f(%s) = <b>%s</b>." % (d(xv), d(xv), d(yv)))
    if k == "ponto":
        return M("Para qual valor de x a função %s atinge o valor %s?" % (f, mm), "x = %s" % d(xv), ["x = %s" % d(yv) if yv != xv else "x = %s" % d(xv + 1), "x = %s" % d(-xv) if xv else "x = 1", "x = %s" % fq(F(-b, a)) if b else "x = 2"],
                 "xᵥ = −b ÷ 2a = %s ÷ %s = <b>%s</b>." % (d(-b), par(2 * a), d(xv)))
    if k == "img":
        r = ("y ≥ %s" if a > 0 else "y ≤ %s") % d(yv)
        return M("Qual é o conjunto imagem de %s?" % f, r, [("y ≤ %s" if a > 0 else "y ≥ %s") % d(yv), ("y ≥ %s" if a > 0 else "y ≤ %s") % d(xv) if xv != yv else "todos os reais", "todos os reais"],
                 "O %s é %s, então Im = { <b>%s</b> }." % (mm, d(yv), r))
    return M("A função %s tem…" % f, "valor %s %s" % (mm, d(yv)), ["valor %s %s" % ("mínimo" if a < 0 else "máximo", d(yv)), "valor %s %s" % (mm, d(xv)) if xv != yv else "nem máximo nem mínimo", "nem máximo nem mínimo"],
             "a = %s: concavidade para %s, vértice é %s; yᵥ = <b>%s</b>." % (d(a), "baixo" if a < 0 else "cima", mm, d(yv)))


def s2_otim():
    k = R.choice(["cerca", "parede", "altura", "lucro", "produto", "preco"])
    if k == "cerca":
        p = R.choice([20, 24, 32, 36, 40, 60, 80, 100])
        l = F(p, 4)
        return M("Com %d m de tela, quer-se cercar um terreno retangular com a maior área possível. Qual é essa área?" % p, "%s m²" % d(l * l), ["%s m²" % d(F(p, 2) * F(p, 2)), "%s m²" % d(p * p), "%s m²" % d(l * (l + 2) - 4 if l > 2 else l)],
                 "x + y = %s ⇒ A = x(%s − x), máxima em x = %s (um quadrado): %s² = <b>%s m²</b>." % (d(F(p, 2)), d(F(p, 2)), d(l), d(l), d(l * l)))
    if k == "parede":
        p = R.choice([20, 40, 60, 80, 100, 120])
        x = F(p, 4)
        A = x * (p - 2 * x)
        return M("Um galinheiro retangular será feito junto a um muro, usando %d m de tela nos outros três lados. Qual é a maior área possível?" % p, "%s m²" % d(A), ["%s m²" % d(F(p, 4) ** 2), "%s m²" % d(F(p, 3) ** 2), "%s m²" % d(A * 2)],
                 "A(x) = x(%d − 2x), máxima em x = %s m; o outro lado mede %s m: A = <b>%s m²</b>." % (p, d(x), d(p - 2 * x), d(A)))
    if k == "altura":
        v = R.choice([10, 20, 30, 40])
        t = F(v, 10)
        h = v * t - 5 * t * t
        return M("A altura de uma bola é h(t) = −5t² + %dt (h em metros, t em segundos). Qual é a altura máxima?" % v, "%s m" % d(h), ["%s s" % d(t), "%s m" % d(v * v), "%s m" % d(2 * h)],
                 "tᵥ = −%d ÷ (−10) = %s s; h(%s) = <b>%s m</b>." % (v, d(t), d(t), d(h)))
    if k == "lucro":
        a = R.choice([1, 2, 5])
        xv = R.choice([10, 20, 25, 30, 40, 50])
        L = R.choice([200, 400, 500, 800, 1000])
        b, c = 2 * a * xv, a * xv * xv - L
        if c <= 0:
            return None
        pergunta = R.choice(["qtd", "lucro"])
        if pergunta == "qtd":
            return M("O lucro de uma fábrica é L(x) = −%sx² + %sx − %s, em reais, para x peças. Quantas peças dão o lucro máximo?" % (d(a) if a > 1 else "", num(b), num(c)), "%d peças" % xv, ["%s peças" % num(L), "%d peças" % (2 * xv), "%s peças" % num(b)],
                     "xᵥ = −%s ÷ (−%d) = <b>%d</b>." % (num(b), 2 * a, xv))
        return M("O lucro de uma fábrica é L(x) = −%sx² + %sx − %s, em reais, para x peças. Qual é o lucro máximo?" % (d(a) if a > 1 else "", num(b), num(c)), R2(L), [R2(xv), R2(c), R2(b * xv)],
                 "xᵥ = %d; L(%d) = <b>%s</b>." % (xv, xv, R2(L)))
    if k == "produto":
        s = R.choice([10, 12, 16, 20, 24, 30, 40])
        return M("Dois números somam %d. Qual é o maior produto possível entre eles?" % s, num(s * s // 4), [num(s * s), num(s * s // 2), num((s // 2 - 1) * (s // 2 + 1))], "P(x) = x(%d − x), máximo em x = %d: %d × %d = <b>%s</b>." % (s, s // 2, s // 2, s // 2, num(s * s // 4)))
    p0, q0, dq = R.choice([(20, 100, 5), (10, 200, 10), (30, 60, 2), (40, 100, 2)])
    # receita: (p0 + x)(q0 − dq·x)
    a, b = -dq, q0 - dq * p0
    xv = F(-b, 2 * a)
    if xv <= 0 or xv.denominator != 1:
        return None
    pr = p0 + xv
    Rv = pr * (q0 - dq * xv)
    return M("Um teatro vende %d ingressos a R$ %d. Para cada R$ 1 de aumento no preço, vende %d ingressos a menos. Qual preço dá a maior receita?" % (q0, p0, dq), R2(pr), [R2(p0), R2(Rv), R2(p0 + 2 * xv)],
             "R(x) = (%d + x)(%d − %dx); xᵥ = %s; preço = %d + %s = <b>%s</b>." % (p0, q0, dq, d(xv), p0, d(xv), R2(pr)))


s3_conceitos = bank(R, [
    ("Uma função quadrática com a > 0 tem…", "valor mínimo no vértice", ["valor máximo no vértice", "máximo e mínimo", "nem máximo nem mínimo"]),
    ("O valor máximo de f(x) = −x² + 4 é…", "4", ["0", "−4", "2"]),
    ("Entre todos os retângulos de mesmo perímetro, o de maior área é…", "o quadrado", ["o mais comprido", "o mais estreito", "qualquer um"]),
    ("No lançamento h(t) = −5t² + 20t, a altura máxima acontece em…", "t = 2 s", ["t = 4 s", "t = 20 s", "t = 0 s"]),
    ("Para achar o valor máximo de f, calculamos…", "yᵥ = f(xᵥ)", ["xᵥ apenas", "os zeros", "f(0)"]),
    ("O valor mínimo de f(x) = (x − 3)² + 1 é…", "1", ["3", "−3", "0"]),
], "s3_conceitos")


def main():
    seen = set()
    sets = [
        ("Valor máximo e valor mínimo", mix(R, seen, [(s1_valor, 20)])),
        ("Ponto de máximo, imagem", mix(R, seen, [(s1_valor, 14), (s3_conceitos, 6)])),
        ("Áreas máximas", mix(R, seen, [(s2_otim, 20)])),
        ("Lançamentos, lucro e receita", mix(R, seen, [(s2_otim, 20)])),
        ("Revisão", mix(R, seen, [(s1_valor, 8), (s2_otim, 12)])),
    ]
    body = lesson(
        ["O vértice da parábola é o ponto de <b>máximo</b> (se a < 0) ou de <b>mínimo</b> (se a > 0).",
         "<b>Ponto de máximo/mínimo</b>: xᵥ = −b ÷ 2a. <b>Valor máximo/mínimo</b>: yᵥ = f(xᵥ).",
         "Em problemas, escreva a grandeza (área, lucro, altura) como uma função quadrática de x e calcule o vértice.",
         "Com perímetro fixo, o retângulo de maior área é o quadrado."],
        [("Bola: h(t) = −5t² + 20t", ["tᵥ = −20 ÷ (−10) = 2", "h(2) = −20 + 40"], "altura máxima 20 m em t = 2 s"),
         ("Retângulo com perímetro 40 m", ["A = x(20 − x)", "xᵥ = 10"], "quadrado 10 × 10: 100 m²")],
        [["Responder xᵥ quando a pergunta pede o valor máximo", "Valor máximo é yᵥ; ponto de máximo é xᵥ."],
         ["Procurar máximo com a > 0", "Com a > 0 há só mínimo."],
         ["Esquecer o muro", "Junto a um muro, a tela cobre só 3 lados."]],
        curva([(lambda t: -5 * t * t + 20 * t, "h")], (0, 4, 1), (0, 25, 5), label="altura h(t) = −5t² + 20t"))
    faq = [("Qual é a diferença entre ponto de máximo e valor máximo?", "O ponto de máximo é o x em que a função é maior (xᵥ). O valor máximo é o maior valor de y (yᵥ = f(xᵥ))."),
           ("O que a BNCC pede?", "Investigar pontos de máximo ou de mínimo de funções quadráticas em contextos envolvendo superfícies, Matemática Financeira ou Cinemática, entre outros, com apoio de tecnologias digitais (EM13MAT503).")]
    unit(R, "maximo-e-minimo-da-funcao-quadratica", "A", ["EM13MAT503"],
         "Investigar pontos de máximo ou de mínimo de funções quadráticas em contextos envolvendo superfícies, Matemática Financeira ou Cinemática, entre outros, com apoio de tecnologias digitais",
         "Máximo e mínimo da função quadrática", "Máximo e mínimo",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre máximo e mínimo da função quadrática: vértice, imagem, área máxima, altura máxima, lucro e receita máximos. 100 exercícios com gabarito.",
         "Máximo ou mínimo: no vértice", "Valor máximo = yᵥ = f(−b ÷ 2a).",
         body, faq, sets, 6, grade="1-serie")


if __name__ == "__main__":
    main()
