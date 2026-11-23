# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Progressão aritmética (EM13MAT507)
  python3 tools/gen_br_matematica_em1_progressao_aritmetica.py
Razão, termo geral aₙ = a₁ + (n − 1)r, posição de um termo, soma dos n primeiros termos Sₙ = (a₁ + aₙ)n ÷ 2,
PA como função afim de domínio discreto (pontos alinhados), problemas (economias, poltronas de um teatro, degraus).
Erros: usar n · r em vez de (n − 1)r, somar só o primeiro e o último sem multiplicar por n ÷ 2, razão com o sinal trocado.
"""
import random
from fractions import Fraction as F
from br_em import M, d, par, expr, bank, mix, lesson, unit, kosy, R2, num, curva

R = random.Random(91008)


def seq(a, r, n=4):
    return "(%s, …)" % ", ".join(d(a + i * r) for i in range(n))


def s1_termo():
    a = R.randint(-10, 20)
    r = R.choice([x for x in range(-6, 9) if x])
    k = R.choice(["razao", "termo", "termo", "pos", "geral"])
    if k == "razao":
        return M("Qual é a razão da PA %s?" % seq(a, r), d(r), [d(-r), d(a), d(a + r)], "%s − %s = <b>%s</b>." % (d(a + r), par(a), d(r)))
    n = R.randint(8, 40)
    an = a + (n - 1) * r
    if k == "termo":
        return M("Qual é o %dº termo da PA %s?" % (n, seq(a, r)), d(an), [d(a + n * r), d(n * r), d(a + (n - 2) * r)], "a%s = %s + (%d − 1) · %s = <b>%s</b>." % ("ₙ", d(a), n, par(r), d(an)))
    if k == "pos":
        return M("Na PA %s, qual é a posição do termo %s?" % (seq(a, r), d(an)), "%dº" % n, ["%dº" % (n - 1), "%dº" % (n + 1), "%dº" % abs(F(an, r)) if F(an, r).denominator == 1 and F(an, r) > 0 and F(an, r) not in (n, n - 1, n + 1) else "%dº" % (n + 2)],
                 "%s = %s + (n − 1) · %s ⇒ n − 1 = %d ⇒ <b>n = %d</b>." % (d(an), d(a), par(r), n - 1, n))
    b = a - r
    ans = "aₙ = " + expr([(r, "n"), (b, "")])
    return M("Qual é o termo geral da PA %s?" % seq(a, r), ans,
             ["aₙ = " + expr([(r, "n"), (a, "")]), "aₙ = " + expr([(a if a else 1, "n"), (r, "")]), "aₙ = " + expr([(a + r if a + r else 1, "n")])],
             "aₙ = %s + (n − 1) · %s = <b>%s</b>." % (d(a), par(r), ans[5:]))


def s2_soma():
    k = R.choice(["pa", "naturais", "pares", "ctx"])
    if k == "pa":
        a = R.randint(1, 15)
        r = R.randint(1, 6)
        n = R.choice([10, 12, 15, 20, 25, 30])
        an = a + (n - 1) * r
        S = (a + an) * n // 2
        return M("Qual é a soma dos %d primeiros termos da PA %s?" % (n, seq(a, r, 3)), num(S), [num((a + an) * n), num(a + an), num(n * an)], "a%d = %d; S = (%d + %d) · %d ÷ 2 = <b>%s</b>." % (n, an, a, an, n, num(S)))
    if k == "naturais":
        n = R.choice([50, 60, 80, 100, 200])
        return M("Quanto é 1 + 2 + 3 + … + %d?" % n, num(n * (n + 1) // 2), [num(n * n), num(n * (n + 1)), num(n * (n - 1) // 2)], "(1 + %d) · %d ÷ 2 = <b>%s</b>." % (n, n, num(n * (n + 1) // 2)))
    if k == "pares":
        n = R.choice([10, 20, 25, 30, 50])
        tipo = R.choice(["pares", "ímpares"])
        S = n * (n + 1) if tipo == "pares" else n * n
        return M("Qual é a soma dos %d primeiros números %s positivos?" % (n, tipo), num(S), [num(S * 2), num(n * (n + 1) // 2), num(S + n) if tipo == "ímpares" else num(n * n)],
                 "PA de razão 2: S = (%d + %d) · %d ÷ 2 = <b>%s</b>." % (2 if tipo == "pares" else 1, 2 * n if tipo == "pares" else 2 * n - 1, n, num(S)))
    a = R.choice([5, 10, 20, 50])
    r = R.choice([5, 10, 20])
    n = R.choice([6, 10, 12])
    an = a + (n - 1) * r
    S = (a + an) * n // 2
    return M("Bia guardou R$ %d no 1º mês e, a cada mês, R$ %d a mais que no mês anterior. Quanto ela guardou ao todo em %d meses?" % (a, r, n), R2(S), [R2(an), R2(a * n), R2((a + an) * n)],
             "a%d = %d + %d · %d = %d; S = (%d + %d) · %d ÷ 2 = <b>%s</b>." % (n, a, n - 1, r, an, a, an, n, R2(S)))


def s3_funcao():
    a = R.randint(-3, 5)
    r = R.choice([-2, -1, 1, 2, 3])
    pts = [(n, a + (n - 1) * r) for n in range(1, 5)]
    if any(abs(y) > 5 for _, y in pts):
        return None
    g = kosy(pts=[(x, y, "") for x, y in pts], lo=-5, hi=5, label="pontos (n, aₙ) de uma progressão aritmética")
    k = R.choice(["razao", "a5", "lei"])
    if k == "razao":
        return M(g + "Os pontos (n, aₙ) de uma PA estão no gráfico. Qual é a razão?", d(r), [d(-r), d(a), d(r + 1) if r + 1 else "2"], "De um ponto para o seguinte, y muda %s: <b>r = %s</b>." % (d(r), d(r)))
    if k == "a5":
        return M(g + "Os pontos (n, aₙ) de uma PA estão no gráfico. Qual é o 5º termo?", d(a + 4 * r), [d(a + 5 * r), d(a + 3 * r), d(5 * r)], "a₅ = a₄ + r = %s + %s = <b>%s</b>." % (d(a + 3 * r), par(r), d(a + 4 * r)))
    b = a - r
    ans = "f(x) = " + expr([(r, "x"), (b, "")])
    return M(g + "Os pontos (n, aₙ) de uma PA ficam sobre a reta de qual função afim?", ans,
             ["f(x) = " + expr([(a if a not in (0, r) else r + 2, "x")]), "f(x) = " + expr([(-r, "x"), (a, "")]), "f(x) = " + expr([(1, "x"), (abs(r) + 3, "")])],
             "A razão é o coeficiente angular (%s) e f(1) = a₁ = %s: <b>%s</b>." % (d(r), d(a), ans))


s4_problemas = bank(R, [
    ("Um teatro tem 20 poltronas na 1ª fila e 2 a mais em cada fila seguinte. Quantas poltronas há na 15ª fila?", "48", ["50", "30", "300"]),
    ("Um teatro tem 20 poltronas na 1ª fila e 2 a mais em cada fila seguinte, num total de 15 filas. Quantas poltronas há ao todo?", "510", ["480", "720", "300"]),
    ("Uma pilha de latas tem 1 lata no topo, 2 na camada de baixo, 3 na seguinte, até 12 na base. Quantas latas há?", "78", ["72", "144", "66"]),
    ("Um atleta corre 2 km no 1º dia e aumenta 500 m por dia. Quantos km corre no 9º dia?", "6 km", ["6,5 km", "4,5 km", "18 km"]),
    ("Os múltiplos de 7 entre 10 e 100 são quantos?", "13", ["14", "12", "90"]),
    ("Quantos números pares há de 2 a 200?", "100", ["99", "200", "101"]),
    ("Numa PA, a₁ = 3 e a₁₀ = 30. Qual é a razão?", "3", ["2,7", "27", "10"]),
    ("Três números em PA somam 21. Qual é o termo do meio?", "7", ["3", "10,5", "21"]),
    ("Um táxi cobra R$ 5 de bandeirada e R$ 3 por km. Os preços para 1, 2, 3… km formam uma PA de razão…", "3", ["5", "8", "2"]),
    ("Interpolando 4 meios aritméticos entre 2 e 17, a razão é…", "3", ["5", "15", "4"]),
], "s4_problemas")


def main():
    seen = set()
    sets = [
        ("Razão e termos", mix(R, seen, [(s1_termo, 20)])),
        ("Termo geral e posição", mix(R, seen, [(s1_termo, 20)])),
        ("Soma dos termos", mix(R, seen, [(s2_soma, 20)])),
        ("PA e função afim", mix(R, seen, [(s3_funcao, 20)])),
        ("Problemas", mix(R, seen, [(s4_problemas, 10), (s2_soma, 10)])),
    ]
    body = lesson(
        ["Numa <b>progressão aritmética</b> (PA), cada termo é o anterior <b>mais</b> uma constante, a razão r.",
         "<b>Termo geral</b>: aₙ = a₁ + (n − 1) · r.",
         "<b>Soma</b> dos n primeiros termos: Sₙ = (a₁ + aₙ) · n ÷ 2.",
         "Os pontos (n, aₙ) de uma PA ficam sobre uma reta: a PA é uma <b>função afim</b> com domínio nos naturais, e a razão é o coeficiente angular."],
        [("PA (5, 9, 13, …): a₂₀ e S₂₀", ["a₂₀ = 5 + 19 · 4 = 81", "S₂₀ = (5 + 81) · 20 ÷ 2"], "a₂₀ = 81; S₂₀ = 860")],
        [["Usar n · r", "São (n − 1) saltos de a₁ até aₙ."],
         ["Esquecer o n ÷ 2 na soma", "Sₙ = (a₁ + aₙ) · n ÷ 2."],
         ["Errar o sinal da razão", "r = a₂ − a₁ (pode ser negativa)."]])
    faq = [("Como calcular a soma dos termos de uma PA?", "Some o primeiro e o último termo, multiplique pela quantidade de termos e divida por 2: Sₙ = (a₁ + aₙ) · n ÷ 2."),
           ("O que a BNCC pede?", "Associar progressões aritméticas (PA) a funções afins de domínios discretos, para análise de propriedades, dedução de algumas fórmulas e resolução de problemas (EM13MAT507).")]
    unit(R, "progressao-aritmetica", "A", ["EM13MAT507"],
         "Identificar e associar progressões aritméticas (PA) a funções afins de domínios discretos, para análise de propriedades, dedução de algumas fórmulas e resolução de problemas",
         "Progressão aritmética (PA): termo geral e soma", "Progressão aritmética",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre progressão aritmética: razão, termo geral, posição de um termo, soma dos termos, PA e função afim e problemas. 100 exercícios com gabarito.",
         "aₙ = a₁ + (n − 1) · r", "Sₙ = (a₁ + aₙ) · n ÷ 2.",
         body, faq, sets, 8, grade="1-serie")


if __name__ == "__main__":
    main()
