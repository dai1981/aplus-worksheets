# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Volume de prismas e cilindros (Grandezas e medidas, EF09MA19)
  python3 tools/gen_br_matematica_9_volume_de_prismas_e_cilindros.py
V = área da base × altura: paralelepípedo, cubo, prisma triangular, cilindro (π = 3,14 ou resposta com π);
litros e cm³ / m³; problemas de caixas d’água, latas e piscinas; achar a altura a partir do volume.
Erros: usar o diâmetro como raio, esquecer de elevar o raio ao quadrado, esquecer que 1 dm³ = 1 L e 1 m³ = 1.000 L.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, unit, _svg, _t, _ln, INK, RED, BLUE

R = random.Random(89019)
PI = F(314, 100)


def caixa(c, l, a, labs=None):
    labs = labs or ("%s cm" % d(c), "%s cm" % d(l), "%s cm" % d(a))
    m = max(c, l, a)
    sc = 150.0 / float(m)
    W, H = 360, 240
    cw, lw, ah = float(c) * sc, float(l) * sc * 0.55, float(a) * sc
    x0, y0 = 50, 215
    dx, dy = lw * 0.8, -lw * 0.6
    P = lambda x, y: "%.1f,%.1f" % (x, y)
    front = [(x0, y0), (x0 + cw, y0), (x0 + cw, y0 - ah), (x0, y0 - ah)]
    top = [(x0, y0 - ah), (x0 + cw, y0 - ah), (x0 + cw + dx, y0 - ah + dy), (x0 + dx, y0 - ah + dy)]
    side = [(x0 + cw, y0), (x0 + cw + dx, y0 + dy), (x0 + cw + dx, y0 - ah + dy), (x0 + cw, y0 - ah)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (" ".join(P(*p) for p in pg), f, INK) for pg, f in ((front, "#dceaf7"), (top, "#f3f8fd"), (side, "#bcd4ef"))]
    s.append(_t(x0 + cw / 2, y0 + 20, labs[0], 15, BLUE if not labs[0].startswith("x") else RED))
    s.append(_t(x0 + cw + dx / 2 + 8, y0 + dy / 2 + 14, labs[1], 15, BLUE if not labs[1].startswith("x") else RED, anchor="start"))
    s.append(_t(x0 - 8, y0 - ah / 2 + 5, labs[2], 15, BLUE if not labs[2].startswith(("x", "h")) else RED, anchor="end"))
    return _svg(int(max(W, x0 + cw + dx + 90)), H, "".join(s), "paralelepípedo com as medidas das arestas")


def cil(r, h, labs=None, diam=False):
    labs = labs or ("%s cm" % d(2 * r if diam else r), "%s cm" % d(h))
    sc = min(120.0 / float(2 * r), 150.0 / float(h))
    rw, ry, hh = float(r) * sc, float(r) * sc * 0.3, float(h) * sc
    cx, yb = 150, 200
    s = ["<path d='M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 0 %.1f %.1f L%.1f %.1f' fill='#dceaf7' stroke='%s' stroke-width='2'/>" % (cx - rw, yb - hh, cx - rw, yb, rw, ry, cx + rw, yb, cx + rw, yb - hh, INK),
         "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#f3f8fd' stroke='%s' stroke-width='2'/>" % (cx, yb - hh, rw, ry, INK),
         "<path d='M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f' fill='none' stroke='%s' stroke-width='1.4' stroke-dasharray='5 4'/>" % (cx - rw, yb, rw, ry, cx + rw, yb, INK)]
    if diam:
        s.append(_ln(cx - rw, yb - hh, cx + rw, yb - hh, RED, 1.8))
        s.append(_t(cx, yb - hh - ry - 6, labs[0], 15, BLUE))
    else:
        s.append(_ln(cx, yb - hh, cx + rw, yb - hh, RED, 1.8))
        s.append("<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (cx, yb - hh, INK))
        s.append(_t(cx + rw / 2, yb - hh - ry - 6, labs[0], 15, BLUE))
    s.append(_t(cx + rw + 10, yb - hh / 2 + 5, labs[1], 15, RED if labs[1].startswith(("x", "h")) else BLUE, anchor="start"))
    return _svg(320, 235, "".join(s), "cilindro com %s e altura" % ("diâmetro" if diam else "raio"))


def s1_paral():
    c, l, a = R.randint(3, 15), R.randint(2, 10), R.randint(2, 12)
    if c == l == a:
        return None
    V = c * l * a
    return M(caixa(c, l, a) + "Qual é o volume deste paralelepípedo?", "%s cm³" % d(V), ["%s cm³" % d(c + l + a), "%s cm³" % d(2 * (c * l + c * a + l * a)), "%s cm³" % d(c * l), "%s cm³" % d(V + c)],
             "V = %d · %d · %d = <b>%s cm³</b>." % (c, l, a, d(V)))


def s1_cubo_altura():
    k = R.choice(["cubo", "alt"])
    if k == "cubo":
        a = R.randint(2, 12)
        return M("Qual é o volume de um cubo de aresta %d cm?" % a, "%s cm³" % d(a ** 3), ["%s cm³" % d(a * a), "%s cm³" % d(3 * a), "%s cm³" % d(6 * a * a) if a != 6 else "%s cm³" % d(a ** 3 + a)],
                     "V = %d³ = <b>%s cm³</b>." % (a, d(a ** 3)))
    c, l, a = R.randint(3, 12), R.randint(2, 10), R.randint(2, 12)
    return M(caixa(c, l, a, ("%d cm" % c, "%d cm" % l, "h")) + "O volume deste paralelepípedo é %s cm³. Qual é a altura h?" % d(c * l * a), "%d cm" % a, ["%s cm" % d(c * l * a - c * l), "%d cm" % (c * l), "%d cm" % (a + 1)],
             "h = V ÷ (área da base) = %s ÷ %d = <b>%d cm</b>." % (d(c * l * a), c * l, a))


def s2_prisma():
    k = R.choice(["tri", "base"])
    if k == "tri":
        b, ht, h = R.randint(3, 12), R.randint(2, 10), R.randint(4, 20)
        Ab = F(b * ht, 2)
        V = Ab * h
        return M("Um prisma tem como base um triângulo de base %d cm e altura %d cm. A altura do prisma é %d cm. Qual é o volume?" % (b, ht, h), "%s cm³" % d(V), ["%s cm³" % d(b * ht * h), "%s cm³" % d(Ab + h), "%s cm³" % d(V / 3, 1) if (V / 3 * 10).denominator == 1 else "%s cm³" % d(V + h)],
                 "Base: %d · %d ÷ 2 = %s cm²; V = %s · %d = <b>%s cm³</b>." % (b, ht, d(Ab), d(Ab), h, d(V)))
    Ab, h = R.choice([12, 15, 18, 20, 24, 30, 36, 40, 45, 50]), R.randint(3, 15)
    shape = R.choice(["hexagonal", "pentagonal", "trapezoidal", "triangular"])
    return M("Um prisma %s tem área da base %d cm² e altura %d cm. Qual é o volume?" % (shape, Ab, h), "%s cm³" % d(Ab * h), ["%s cm³" % d(Ab + h), "%s cm³" % d(F(Ab * h, 3), 1) if (Ab * h) % 3 == 0 else "%s cm³" % d(Ab * h + 10), "%s cm³" % d(Ab * h * 2)],
             "V = área da base · altura = %d · %d = <b>%s cm³</b>." % (Ab, h, d(Ab * h)))


def s3_cil():
    r, h = R.randint(1, 10), R.randint(2, 20)
    k = R.choice(["pi", "num", "diam"])
    if k == "pi":
        return M(cil(r, h) + "Qual é o volume do cilindro? (Deixe a resposta com π.)", "%sπ cm³" % d(r * r * h), ["%sπ cm³" % d(2 * r * h), "%sπ cm³" % d(r * h), "%sπ cm³" % d(4 * r * r * h), "%sπ cm³" % d(r * r * h + h)],
                 "V = π · r² · h = π · %d² · %d = <b>%sπ cm³</b>." % (r, h, d(r * r * h)))
    if k == "diam":
        r = R.randint(1, 8)
        return M(cil(r, h, diam=True) + "O diâmetro da base mede %d cm. Qual é o volume do cilindro? (Deixe a resposta com π.)" % (2 * r), "%sπ cm³" % d(r * r * h), ["%sπ cm³" % d(4 * r * r * h), "%sπ cm³" % d(2 * r * h), "%sπ cm³" % d(r * h)],
                 "Raio = %d ÷ 2 = %d; V = π · %d² · %d = <b>%sπ cm³</b>." % (2 * r, r, r, h, d(r * r * h)))
    V = PI * r * r * h
    return M(cil(r, h) + "Qual é o volume do cilindro? (Use π = 3,14.)", "%s cm³" % d(V), ["%s cm³" % d(PI * 2 * r * h), "%s cm³" % d(PI * r * h), "%s cm³" % d(PI * 4 * r * r * h)],
             "V = 3,14 · %d² · %d = 3,14 · %d = <b>%s cm³</b>." % (r, h, r * r * h, d(V)))


def s4_litros():
    k = R.choice(["caixa", "lata", "piscina", "caixa_dagua"])
    if k == "caixa":
        c, l, a = R.choice([(10, 10, 10), (20, 10, 5), (30, 20, 10), (25, 20, 10), (40, 25, 20), (50, 20, 30)])
        V = c * l * a
        return M("Um aquário tem %d cm de comprimento, %d cm de largura e %d cm de altura. Quantos litros cabem nele? (1 L = 1.000 cm³)" % (c, l, a), "%s L" % d(F(V, 1000)), ["%s L" % d(V), "%s L" % d(F(V, 100)), "%s L" % d(F(V, 10000), 3) if (F(V, 10000) * 1000).denominator == 1 else "%s L" % d(V // 1000 + 1)],
                     "V = %s cm³; ÷ 1.000 = <b>%s L</b>." % (d(V), d(F(V, 1000))))
    if k == "lata":
        r, h = R.choice([(3, 10), (4, 12), (5, 10), (5, 20), (10, 10), (2, 15)])
        V = PI * r * r * h
        return M("Uma lata cilíndrica tem raio %d cm e altura %d cm. Quantos mililitros cabem nela? (π = 3,14; 1 cm³ = 1 mL)" % (r, h), "%s mL" % d(V), ["%s mL" % d(PI * 2 * r * h), "%s mL" % d(PI * r * h), "%s mL" % d(V / 1000, 3) if (V / 1000 * 1000).denominator == 1 else "%s mL" % d(V + 10)],
                     "V = 3,14 · %d² · %d = <b>%s mL</b>." % (r, h, d(V)))
    if k == "piscina":
        c, l, p = R.choice([(10, 5, F(3, 2)), (8, 4, 2), (12, 6, F(3, 2)), (6, 3, 1), (25, 10, 2), (5, 4, F(6, 5))])
        V = c * l * p
        return M("Uma piscina tem %d m de comprimento, %d m de largura e %s m de profundidade. Quantos litros de água ela comporta? (1 m³ = 1.000 L)" % (c, l, d(p)), "%s L" % d(V * 1000), ["%s L" % d(V), "%s L" % d(V * 100), "%s L" % d(V * 10000)],
                     "V = %d · %d · %s = %s m³ = <b>%s L</b>." % (c, l, d(p), d(V), d(V * 1000)))
    r, h = R.choice([(F(1, 2), 2), (1, 1), (F(1, 2), 1), (1, 2), (F(3, 2), 2)])
    V = PI * r * r * h
    return M("Uma caixa d’água cilíndrica tem raio %s m e altura %s m. Qual é a capacidade em litros? (π = 3,14; 1 m³ = 1.000 L)" % (d(r), d(h)), "%s L" % d(V * 1000), ["%s L" % d(V), "%s L" % d(PI * 2 * r * h * 1000), "%s L" % d(PI * r * h * 1000)],
             "V = 3,14 · %s² · %s = %s m³ = <b>%s L</b>." % (d(r), d(h), d(V), d(V * 1000)))


def s5_problemas():
    k = R.choice(["dobro", "comparar", "altura_cil", "nivel"])
    if k == "dobro":
        q, a, w = R.choice([("Se dobrarmos o raio de um cilindro e mantivermos a altura, o volume fica…", "4 vezes maior", ["2 vezes maior", "8 vezes maior", "igual"]),
                            ("Se dobrarmos a altura de um cilindro e mantivermos o raio, o volume fica…", "2 vezes maior", ["4 vezes maior", "8 vezes maior", "igual"]),
                            ("Se dobrarmos as três arestas de um paralelepípedo, o volume fica…", "8 vezes maior", ["2 vezes maior", "4 vezes maior", "6 vezes maior"]),
                            ("Se triplicarmos a aresta de um cubo, o volume fica…", "27 vezes maior", ["3 vezes maior", "9 vezes maior", "6 vezes maior"])])
        return M(q, a, w, "Resposta: <b>%s</b>." % a)
    if k == "comparar":
        a = R.randint(2, 8)
        r = a / 2
        return M("Um cubo de aresta %d cm e um cilindro de diâmetro %d cm e altura %d cm. Qual tem maior volume?" % (a, a, a), "o cubo", ["o cilindro", "os dois têm o mesmo volume", "depende da cor"],
                 "Cubo: %d cm³. Cilindro: π · %s² · %d ≈ %s cm³. O cilindro cabe dentro do cubo: <b>o cubo</b>." % (a ** 3, d(F(a, 2)), a, d(PI * F(a, 2) ** 2 * a, 2)))
    if k == "altura_cil":
        r, h = R.randint(1, 6), R.randint(2, 15)
        return M("Um cilindro tem volume %sπ cm³ e raio %d cm. Qual é a altura?" % (d(r * r * h), r), "%d cm" % h, ["%s cm" % d(F(r * r * h, r)) if r > 1 else "%d cm" % (h + 2), "%d cm" % (r * r * h), "%d cm" % (h + 1)],
                 "h = V ÷ (π · r²) = %sπ ÷ %dπ = <b>%d cm</b>." % (d(r * r * h), r * r, h))
    c, l = R.choice([(50, 40), (60, 30), (40, 25), (80, 50)])
    L = R.choice([12, 18, 24, 30, 36])
    h = F(L * 1000, c * l)
    if (h * 10).denominator != 1:
        return None
    return M("Num aquário de %d cm por %d cm de base, colocamos %d litros de água. Até que altura sobe a água?" % (c, l, L), "%s cm" % d(h), ["%s cm" % d(h * 10), "%s cm" % d(h / 10, 2), "%d cm" % (L)],
             "%d L = %s cm³; h = %s ÷ %d = <b>%s cm</b>." % (L, d(L * 1000), d(L * 1000), c * l, d(h)))


def main():
    seen = set()
    sets = [
        ("Volume do paralelepípedo e do cubo", mix(R, seen, [(s1_paral, 14), (s1_cubo_altura, 6)])),
        ("Volume de prismas", mix(R, seen, [(s2_prisma, 16), (s1_cubo_altura, 4)])),
        ("Volume do cilindro", mix(R, seen, [(s3_cil, 20)])),
        ("Volume e capacidade em litros", mix(R, seen, [(s4_litros, 20)])),
        ("Problemas com volume", mix(R, seen, [(s5_problemas, 14), (s3_cil, 6)])),
    ]
    body = lesson(
        ["O volume de um <b>prisma</b> ou de um <b>cilindro</b> é a área da base vezes a altura: V = A<sub>b</sub> · h.",
         "Paralelepípedo: V = comprimento · largura · altura. Cubo: V = a³.",
         "Cilindro: a base é um círculo, então V = π · r² · h.",
         "Capacidade: 1 cm³ = 1 mL, 1 dm³ = 1 L e 1 m³ = 1.000 L."],
        [("Cilindro com r = 5 cm e h = 10 cm", ["V = 3,14 · 25 · 10"], "785 cm³ = 785 mL"),
         ("Caixa de 50 cm × 40 cm × 30 cm", ["V = 60.000 cm³"], "60 L")],
        [["Usar o diâmetro como raio", "O raio é a metade do diâmetro."],
         ["Esquecer de elevar o raio ao quadrado", "π · r² · h: o r aparece duas vezes."],
         ["Errar a conversão para litros", "1 m³ = 1.000 L e 1.000 cm³ = 1 L."]],
        cil(5, 10))
    faq = [("Como calcular o volume de um cilindro?", "Multiplique a área da base (π · r²) pela altura: V = π · r² · h. Use o raio, que é a metade do diâmetro."),
           ("O que a BNCC pede no 9º ano?", "Resolver e elaborar problemas que envolvam medidas de volumes de prismas e de cilindros retos, inclusive com uso de expressões de cálculo, em situações cotidianas (EF09MA19).")]
    unit(R, "volume-de-prismas-e-cilindros", "M", ["EF09MA19"],
         "Resolver e elaborar problemas que envolvam medidas de volumes de prismas e de cilindros retos, inclusive com uso de expressões de cálculo, em situações cotidianas",
         "Volume de prismas e cilindros", "Volume de prismas e cilindros",
         "Atividades de matemática para o 9º ano sobre volume de prismas e cilindros: paralelepípedo, cubo, prisma triangular, cilindro com π, capacidade em litros e problemas do dia a dia. 100 exercícios com gabarito.",
         "V = área da base × altura", "Cilindro: V = π · r² · h",
         body, faq, sets, 19)


if __name__ == "__main__":
    main()
