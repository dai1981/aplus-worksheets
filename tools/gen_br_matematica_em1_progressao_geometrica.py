# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Progressão geométrica (EM13MAT508)
  python3 tools/gen_br_matematica_em1_progressao_geometrica.py
Razão q, termo geral aₙ = a₁ · qⁿ⁻¹, soma finita Sₙ = a₁(qⁿ − 1) ÷ (q − 1), soma infinita a₁ ÷ (1 − q) com 0 < q < 1,
PG como função exponencial de domínio discreto, problemas (bactérias, desvalorização, juros compostos).
Erros: calcular a razão como diferença, usar qⁿ em vez de qⁿ⁻¹, usar a soma infinita com |q| ≥ 1.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, bank, mix, lesson, unit, R2, num, curva

R = random.Random(91009)
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def seq(a, q, n=4):
    return "(%s, …)" % ", ".join(fq(a * q ** i) for i in range(n))


def s1_termo():
    a = R.choice([1, 2, 3, 4, 5, -2, 6, 64, 81, 128])
    q = R.choice([2, 3, -2, F(1, 2), F(1, 3), 4, F(-1, 2)])
    if (q.denominator if isinstance(q, F) else 1) > 1 and (a * F(q) ** 3).denominator != 1:
        return None
    k = R.choice(["razao", "termo", "termo", "pos"])
    if k == "razao":
        return M("Qual é a razão da PG %s?" % seq(a, q), fq(q), [fq(a * q - a), fq(1 / F(q)), fq(-F(q))], "%s ÷ %s = <b>%s</b>." % (fq(a * q), par(a) if a > 0 else "(%s)" % d(a), fq(q)))
    n = R.randint(5, 8)
    an = a * F(q) ** (n - 1)
    if abs(an) > 10 ** 6 or (an * 10 ** 6).denominator != 1 and an.denominator > 1000:
        return None
    if k == "termo":
        return M("Qual é o %dº termo da PG %s?" % (n, seq(a, q)), fq(an), [fq(a * F(q) ** n), fq(a + (n - 1) * q), fq(a * F(q) ** (n - 2))],
                 "a%s = %s · %s%s = <b>%s</b>." % (str(n).translate(SUB), fq(a), par(q) if F(q).denominator == 1 else "(%s)" % fq(q), str(n - 1).translate(SUP), fq(an)))
    return M("Na PG %s, qual é a posição do termo %s?" % (seq(a, q), fq(an)), "%dº" % n, ["%dº" % (n - 1), "%dº" % (n + 1), "%dº" % (n + 2)],
             "%s = %s · q%s; q%s = %s ⇒ <b>n = %d</b>." % (fq(an), fq(a), "ⁿ⁻¹", "ⁿ⁻¹", fq(an / a), n))


def s2_soma():
    k = R.choice(["fin", "fin", "inf"])
    if k == "fin":
        a = R.choice([1, 2, 3, 5])
        q = R.choice([2, 3])
        n = R.choice([5, 6, 7, 8]) if q == 2 else R.choice([4, 5, 6])
        S = a * (q ** n - 1) // (q - 1)
        return M("Qual é a soma dos %d primeiros termos da PG %s?" % (n, seq(a, q, 3)), num(S), [num(a * q ** (n - 1)), num(a * q ** n), num(a * n * q)],
                 "Sₙ = %d · (%d%s − 1) ÷ (%d − 1) = <b>%s</b>." % (a, q, str(n).translate(SUP), q, num(S)))
    a = R.choice([2, 4, 6, 8, 10, 12, 18, 20, 30])
    q = R.choice([F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(1, 5)])
    S = a / (1 - q)
    if S.denominator != 1:
        return None
    return M("Qual é a soma infinita da PG %s?" % seq(a, q, 3), fq(S), [fq(a / q) if (a / q) != S else fq(S + 1), fq(a * (1 + q)), "não existe"],
             "|q| &lt; 1: S = a₁ ÷ (1 − q) = %d ÷ %s = <b>%s</b>." % (a, fq(1 - q), fq(S)))


def s3_ctx():
    k = R.choice(["bact", "desval", "juros", "papel", "graf"])
    if k == "bact":
        n0 = R.choice([100, 200, 500, 1000])
        h = R.choice([1, 2, 3])
        t = h * R.choice([3, 4, 5, 6])
        v = n0 * 2 ** (t // h)
        return M("Uma colônia tem %s bactérias e dobra a cada %s. Quantas bactérias haverá depois de %d horas?" % (num(n0), "hora" if h == 1 else "%d horas" % h, t), num(v), [num(n0 * 2 * t // h), num(n0 * 2 ** (t // h - 1)), num(n0 * 2 ** t) if h > 1 else num(v * 2)],
                 "%d dobras: %s · 2%s = <b>%s</b>." % (t // h, num(n0), str(t // h).translate(SUP), num(v)))
    if k == "desval":
        v0 = R.choice([40000, 50000, 60000, 80000, 100000])
        p = R.choice([10, 20])
        n = R.choice([2, 3])
        v = v0 * F(100 - p, 100) ** n
        return M("Um carro de R$ %s perde %d%% do valor a cada ano. Quanto ele valerá depois de %d anos?" % (num(v0), p, n), R2(v), [R2(v0 * F(100 - p * n, 100)), R2(v0 * F(100 - p, 100) ** (n + 1)), R2(v0 * F(p, 100) ** n)],
                 "PG de razão %s: %s · %s%s = <b>%s</b>." % (d(F(100 - p, 100)), num(v0), d(F(100 - p, 100)), str(n).translate(SUP), R2(v)))
    if k == "juros":
        c = R.choice([1000, 2000, 5000, 10000])
        i = R.choice([5, 10])
        n = R.choice([2, 3])
        m = c * F(100 + i, 100) ** n
        return M("R$ %s aplicados a juros compostos de %d%% ao mês formam uma PG. Qual é o montante depois de %d meses?" % (num(c), i, n), R2(m), [R2(c * F(100 + i * n, 100)), R2(c * F(100 + i, 100) ** (n - 1)), R2(c * F(i, 100) * n)],
                 "Razão %s: %s · %s%s = <b>%s</b>." % (d(F(100 + i, 100)), num(c), d(F(100 + i, 100)), str(n).translate(SUP), R2(m)))
    if k == "papel":
        n = R.randint(3, 8)
        return M("Uma folha é dobrada ao meio %d vezes. Em quantas camadas ela fica?" % n, str(2 ** n), [str(2 * n), str(2 ** (n - 1)), str(n * n)], "Cada dobra multiplica por 2: 2%s = <b>%d</b>." % (str(n).translate(SUP), 2 ** n))
    a = R.choice([1, 2])
    q = R.choice([2, F(1, 2)])
    pts = [(n, a * F(q) ** (n - 1)) for n in range(1, 5)]
    top = max(y for _, y in pts)
    yr = (0, 2, 0.5) if top <= 2 else ((0, 8, 1) if top <= 8 else (0, 16, 2))
    g = curva([(lambda x: None, "")], (0, 5, 1), yr, pts=[(x, y, "") for x, y in pts], label="pontos (n, aₙ) de uma progressão geométrica")
    return M(g + "Os pontos (n, aₙ) de uma progressão estão no gráfico. Que tipo de progressão é, e qual a razão?", "PG de razão %s" % fq(q), ["PA de razão %s" % fq(pts[1][1] - pts[0][1]), "PG de razão %s" % fq(1 / F(q)), "PA de razão %s" % fq(q)],
             "Cada termo é o anterior × %s, e os pontos não estão alinhados: <b>PG de razão %s</b>." % (fq(q), fq(q)))


s4_conceitos = bank(R, [
    ("Numa PG, cada termo é obtido…", "multiplicando o anterior pela razão", ["somando a razão ao anterior", "dividindo pelo primeiro termo", "somando os dois anteriores"]),
    ("Os pontos (n, aₙ) de uma PG de razão positiva ficam sobre o gráfico de uma função…", "exponencial", ["afim", "quadrática", "constante"]),
    ("A PG (5, 5, 5, …) tem razão…", "1", ["0", "5", "não é PG"]),
    ("A PG (3, −6, 12, −24, …) é…", "alternante (razão negativa)", ["crescente", "decrescente", "constante"]),
    ("A soma infinita de uma PG existe quando…", "−1 &lt; q &lt; 1", ["q &gt; 1", "q = 1", "q é inteiro"]),
    ("Se a₁ = 2 e q = 3, então a₄ é…", "54", ["18", "162", "11"]),
    ("A PG (100, 50, 25, …) é…", "decrescente, de razão 1/2", ["crescente, de razão 2", "decrescente, de razão −50", "uma PA"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Razão e termos", mix(R, seen, [(s1_termo, 20)])),
        ("Termo geral e posição", mix(R, seen, [(s1_termo, 15), (s4_conceitos, 5)])),
        ("Soma dos termos", mix(R, seen, [(s2_soma, 20)])),
        ("PG no dia a dia", mix(R, seen, [(s3_ctx, 20)])),
        ("Revisão", mix(R, seen, [(s1_termo, 8), (s2_soma, 6), (s3_ctx, 4), (s4_conceitos, 2)])),
    ]
    body = lesson(
        ["Numa <b>progressão geométrica</b> (PG), cada termo é o anterior <b>multiplicado</b> por uma constante, a razão q = a₂ ÷ a₁.",
         "<b>Termo geral</b>: aₙ = a₁ · qⁿ⁻¹.",
         "<b>Soma</b> dos n primeiros termos: Sₙ = a₁ · (qⁿ − 1) ÷ (q − 1). Se −1 &lt; q &lt; 1, a soma infinita é a₁ ÷ (1 − q).",
         "Os pontos (n, aₙ) de uma PG com q &gt; 0 ficam sobre o gráfico de uma <b>função exponencial</b>. Crescimento e desvalorização por porcentagem fixa são PGs."],
        [("PG (3, 6, 12, …): a₈ e S₈", ["a₈ = 3 · 2⁷ = 384", "S₈ = 3 · (2⁸ − 1) ÷ 1"], "a₈ = 384; S₈ = 765"),
         ("Soma infinita de (10, 5, 2,5, …)", ["10 ÷ (1 − 1/2)"], "20")],
        [["Achar a razão por diferença", "Na PG, q = a₂ ÷ a₁."],
         ["Usar qⁿ no termo geral", "O expoente é n − 1."],
         ["Somar infinitos termos com q ≥ 1", "A soma infinita só existe com −1 &lt; q &lt; 1."]])
    faq = [("Qual é a diferença entre PA e PG?", "Na PA somamos sempre o mesmo número (razão r); na PG multiplicamos sempre pelo mesmo número (razão q). A PA é ligada à função afim; a PG, à função exponencial."),
           ("O que a BNCC pede?", "Identificar e associar progressões geométricas (PG) a funções exponenciais de domínios discretos, para análise de propriedades, dedução de algumas fórmulas e resolução de problemas (EM13MAT508).")]
    unit(R, "progressao-geometrica", "A", ["EM13MAT508"],
         "Identificar e associar progressões geométricas (PG) a funções exponenciais de domínios discretos, para análise de propriedades, dedução de algumas fórmulas e resolução de problemas",
         "Progressão geométrica (PG): termo geral e soma", "Progressão geométrica",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre progressão geométrica: razão, termo geral, soma finita e infinita, PG e função exponencial, bactérias, desvalorização e juros compostos. 100 exercícios com gabarito.",
         "aₙ = a₁ · qⁿ⁻¹", "Na PG, multiplica-se sempre pela razão q.",
         body, faq, sets, 9, grade="1-serie")


if __name__ == "__main__":
    main()
