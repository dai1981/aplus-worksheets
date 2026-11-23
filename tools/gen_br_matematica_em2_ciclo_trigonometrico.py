# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Ciclo trigonométrico e radianos (EM13MAT306)
  python3 tools/gen_br_matematica_em2_ciclo_trigonometrico.py
Radiano e conversão graus ↔ radianos; comprimento de arco (ℓ = r · θ); quadrantes e sinais de seno e cosseno;
redução ao 1º quadrante (seno e cosseno de 120°, 210°, 315°…); arcos côngruos (primeira determinação positiva).
Erros: multiplicar por 180/π para ir de graus a radianos, achar que o seno é negativo no 2º quadrante, esquecer de tirar voltas inteiras.
"""
import random
import math
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, unit, pit, trig, _svg, _t, _ln, _arc, INK, BLUE, RED

R = random.Random(92003)
NOTAVEIS = [30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]


def ciclo(deg, label="ciclo trigonométrico"):
    W, H, cx, cy, r = 300, 260, 150, 130, 100
    s = [_ln(cx - r - 20, cy, cx + r + 20, cy), _ln(cx, cy + r + 20, cx, cy - r - 20),
         "<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2'/>" % (cx, cy, r, INK)]
    a = math.radians(deg)
    px, py = cx + r * math.cos(a), cy - r * math.sin(a)
    s.append(_ln(cx, cy, px, py, BLUE, 2.4))
    s.append(_ln(px, py, px, cy, "#888", 1.4))
    s.append(_ln(px, py, cx, py, "#888", 1.4))
    s.append(_arc(cx, cy, 24, 0, deg % 360, RED))
    s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (px, py, RED))
    s.append(_t(px + 14 * math.cos(a), py - 14 * math.sin(a) + 5, "P", 15, RED))
    for lab, x, y in (("I", cx + 60, cy - 60), ("II", cx - 60, cy - 60), ("III", cx - 60, cy + 70), ("IV", cx + 60, cy + 70)):
        s.append(_t(x, y, lab, 13, "#888", bold=False))
    s.append(_t(cx + r + 16, cy - 8, "cos", 13, INK, bold=False) + _t(cx + 18, cy - r - 10, "sen", 13, INK, bold=False))
    return _svg(W, H, "".join(s), label)


def s1_conv():
    k = R.choice(["g2r", "g2r", "r2g"])
    deg = R.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 20, 36, 72])
    v = F(deg, 180)
    if k == "g2r":
        return M("Quanto vale %d° em radianos?" % deg, pit(v) + " rad", [pit(1 / v) + " rad" if v != 1 else "2π rad", pit(v * 2) + " rad", "%s rad" % d(deg * 180)],
                 "%d° × π/180 = <b>%s rad</b>." % (deg, pit(v)))
    return M("Quanto vale %s rad em graus?" % pit(v), "%d°" % deg, ["%d°" % (deg * 2), "%s°" % d(F(deg, 2)), "%s°" % d(F(180 * 180, deg)) if (F(180 * 180, deg) * 10).denominator == 1 else "%d°" % (deg + 180)],
             "%s × 180°/π = <b>%d°</b>." % (pit(v), deg))


def s2_arco():
    r = R.choice([2, 3, 4, 5, 6, 10, 12])
    k = R.choice(["rad", "graus", "theta"])
    if k == "rad":
        th = R.choice([F(1, 2), F(3, 2), F(2), F(5, 2), F(3)])
        L = r * th
        return M("Numa circunferência de raio %d cm, qual é o comprimento de um arco de %s rad?" % (r, d(th)), "%s cm" % d(L), ["%s cm" % d(th), "%s cm" % d(L * 2), "%s cm" % d(F(r) / th, 2)], "ℓ = r · θ = %d · %s = <b>%s cm</b>." % (r, d(th), d(L)))
    if k == "graus":
        deg = R.choice([30, 45, 60, 90, 120, 180])
        L = F(deg, 180) * r
        return M("Numa circunferência de raio %d cm, qual é o comprimento de um arco de %d°? (Deixe com π.)" % (r, deg), pit(L) + " cm", [pit(L * 2) + " cm", "%d cm" % (deg * r), pit(F(deg, 180)) + " cm"],
                 "%d° = %s rad; ℓ = %d · %s = <b>%s cm</b>." % (deg, pit(F(deg, 180)), r, pit(F(deg, 180)), pit(L)))
    L = r * R.choice([1, 2, 3])
    return M("Um arco de %d cm numa circunferência de raio %d cm mede quantos radianos?" % (L, r), "%s rad" % d(F(L, r)), ["%s rad" % d(F(r, L), 2), "%d rad" % (L * r), "%s rad" % d(F(L, 2 * r), 2)], "θ = ℓ ÷ r = %d ÷ %d = <b>%s rad</b>." % (L, r, d(F(L, r))))


def s3_valores():
    deg = R.choice(NOTAVEIS)
    k = R.choice(["val", "val", "sinal", "quad"])
    if k == "val":
        fn = R.choice(["sen", "cos"])
        v = trig(deg, fn)
        other = trig(deg, "cos" if fn == "sen" else "sen")
        opp = v[1:] if v.startswith("−") else ("−" + v if v != "0" else "1")
        g = ciclo(deg, "ciclo trigonométrico com o ponto P de %d°" % deg)
        return M(g + "Quanto vale %s %d°?" % (fn, deg), v, [opp, other, "√3/2", "1/2", "√2/2", "−√3/2", "0", "1"],
                 "Ângulo de referência %d°, %s quadrante: %s %d° = <b>%s</b>." % (ref(deg), quad_nome(deg), fn, deg, v))
    if k == "sinal":
        if deg % 90 == 0:
            return None
        q = quad(deg)
        s_sen = "positivo" if q in (1, 2) else "negativo"
        s_cos = "positivo" if q in (1, 4) else "negativo"
        ans = "sen %s e cos %s" % (s_sen, s_cos)
        opts = ["sen %s e cos %s" % (a, b) for a in ("positivo", "negativo") for b in ("positivo", "negativo")]
        return M("Para um ângulo de %d°, quais são os sinais do seno e do cosseno?" % deg, ans, [o for o in opts if o != ans], "%d° está no %s quadrante: <b>%s</b>." % (deg, quad_nome(deg), ans))
    if deg % 90 == 0:
        return None
    return M("Em que quadrante fica a extremidade do arco de %d°?" % deg, "%s quadrante" % quad_nome(deg).replace("º", "º"), ["%s quadrante" % n for n in ("1º", "2º", "3º", "4º") if n != quad_nome(deg)], "%d° está entre %d° e %d°: <b>%s quadrante</b>." % (deg, (quad(deg) - 1) * 90, quad(deg) * 90, quad_nome(deg)))


def quad(deg):
    return int((deg % 360) // 90) + 1


def quad_nome(deg):
    return "%dº" % quad(deg)


def ref(deg):
    x = deg % 180
    return min(x, 180 - x) if deg % 90 else deg


def s4_congruos():
    base = R.choice(NOTAVEIS + [0, 10, 20, 40, 50, 80, 100])
    n = R.choice([1, 2, 3, -1])
    deg = base + 360 * n
    if deg == base:
        return None
    k = R.choice(["deg", "deg", "rad"])
    if k == "deg":
        return M("Qual é a primeira determinação positiva do arco de %d°?" % deg, "%d°" % base, ["%d°" % (deg - 180) if deg - 180 != base else "%d°" % (base + 180), "%d°" % abs(deg % 180) if deg % 180 != base else "%d°" % (base + 90), "%d°" % (abs(deg) - 360) if abs(deg) - 360 != base else "%d°" % (base + 30)],
                 "%d° %s %d · 360° = <b>%d°</b>." % (deg, "−" if n > 0 else "+", abs(n), base))
    v = F(base, 180) + 2 * n
    if base == 0:
        return None
    return M("Qual é a primeira determinação positiva do arco de %s rad?" % pit(v), pit(F(base, 180)) + " rad", [pit(F(base, 180) + 1) + " rad", pit(v - 1) + " rad", pit(F(base, 360)) + " rad", pit(v - 2 * n + F(1, 2)) + " rad", "2π rad"],
             "Tire %d volta%s (2π cada): <b>%s rad</b>." % (abs(n), "s" if abs(n) > 1 else "", pit(F(base, 180))))


s5_conceitos = bank(R, [
    ("Uma volta completa no ciclo trigonométrico mede…", "2π rad (360°)", ["π rad", "π/2 rad", "4π rad"]),
    ("1 radiano é o ângulo central cujo arco tem comprimento…", "igual ao raio", ["igual ao diâmetro", "igual a 1 cm", "igual a π"]),
    ("No ciclo trigonométrico, o seno de um ângulo é…", "a ordenada (y) do ponto", ["a abscissa (x) do ponto", "o raio", "o comprimento do arco"]),
    ("sen 90° vale…", "1", ["0", "−1", "1/2"]),
    ("cos 180° vale…", "−1", ["0", "1", "1/2"]),
    ("Arcos côngruos são arcos que…", "têm a mesma extremidade no ciclo", ["têm o mesmo comprimento", "somam 360°", "são complementares"]),
    ("sen 150° é igual a…", "sen 30°", ["−sen 30°", "cos 30°", "sen 60°"]),
    ("cos 210° é igual a…", "−cos 30°", ["cos 30°", "sen 30°", "−sen 60°"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Graus e radianos", mix(R, seen, [(s1_conv, 20)])),
        ("Comprimento de arco", mix(R, seen, [(s2_arco, 16), (s5_conceitos, 4)])),
        ("Seno e cosseno no ciclo", mix(R, seen, [(s3_valores, 20)])),
        ("Quadrantes e sinais", mix(R, seen, [(s3_valores, 16), (s5_conceitos, 4)])),
        ("Arcos côngruos", mix(R, seen, [(s4_congruos, 20)])),
    ]
    body = lesson(
        ["<b>Radiano</b>: ângulo cujo arco tem o comprimento do raio. 180° = π rad. Graus → radianos: × π/180. Radianos → graus: × 180/π.",
         "<b>Comprimento de arco</b>: ℓ = r · θ (θ em radianos).",
         "No <b>ciclo trigonométrico</b> (raio 1), o ponto P do ângulo θ tem coordenadas (cos θ, sen θ).",
         "Sinais: 1º quadrante, sen + e cos +; 2º, sen + e cos −; 3º, sen − e cos −; 4º, sen − e cos +. Para outros ângulos, use o ângulo de referência no 1º quadrante.",
         "<b>Arcos côngruos</b> diferem por voltas inteiras: 390° tem a mesma extremidade que 30°."],
        [("sen 210°", ["3º quadrante: seno negativo", "referência: 30°"], "−1/2"),
         ("135° em radianos", ["135 × π/180"], "3π/4 rad")],
        [["Usar 180/π de graus para radianos", "Graus → radianos: multiplique por π/180."],
         ["Seno negativo no 2º quadrante", "No 2º quadrante o seno é positivo (y &gt; 0)."],
         ["Não tirar as voltas", "Subtraia 360° (ou 2π) quantas vezes for preciso."]],
        ciclo(210, "ciclo trigonométrico com o ponto P de 210°"))
    faq = [("Como converter graus em radianos?", "Multiplique por π/180. Por exemplo, 60° = 60 · π/180 = π/3 rad."),
           ("O que a BNCC pede?", "Identificar características de fenômenos periódicos e resolver problemas sobre eles, comparando suas representações com as funções seno e cosseno, no plano cartesiano, com ou sem apoio de aplicativos de álgebra e geometria (EM13MAT306).")]
    unit(R, "ciclo-trigonometrico-e-radianos", "G", ["EM13MAT306"],
         "Resolver e elaborar problemas em contextos que envolvem fenômenos periódicos reais (ondas sonoras, fases da lua, movimentos cíclicos, entre outros) e comparar suas representações com as funções seno e cosseno, no plano cartesiano, com ou sem apoio de aplicativos de álgebra e geometria",
         "Ciclo trigonométrico, radianos e arcos", "Ciclo trigonométrico",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre o ciclo trigonométrico: graus e radianos, comprimento de arco, seno e cosseno no ciclo, quadrantes, sinais e arcos côngruos. 100 exercícios com gabarito.",
         "180° = π rad", "No ciclo, P = (cos θ, sen θ).",
         body, faq, sets, 3, grade="2-serie")


if __name__ == "__main__":
    main()
