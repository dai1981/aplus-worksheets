# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Grandezas e medidas (Grandezas e medidas, EF06MA24)
  python3 tools/gen_br_matematica_6_grandezas_e_medidas.py
Transformação de unidades de comprimento (km, m, cm, mm), massa (t, kg, g, mg), capacidade (L, mL) e tempo (h, min, s, dias);
temperatura; problemas com medidas, inclusive com decimais.
Usa geradores do 5º ano (medidas e transformações) com outro sorteio.
Erros: multiplicar quando é para dividir, usar 100 em vez de 1.000, tratar 1 h 30 min como 1,30 h.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use, lim
from br_9 import M, d, bank, unit

R = random.Random(86017)
m_comp, m_massa, m_cap, m_tempo = use("gen_br_matematica_5_medidas_e_transformacoes", 86917, "s1_comp", "s2_massa", "s2_cap", "s4_tempo")
U = {"comp": [("km", 1000000), ("m", 1000), ("cm", 10), ("mm", 1)], "massa": [("t", 10 ** 9), ("kg", 10 ** 6), ("g", 1000), ("mg", 1)], "cap": [("L", 1000), ("mL", 1)]}


def s1_conv():
    g = R.choice(["comp", "comp", "massa", "massa", "cap"])
    (u1, f1), (u2, f2) = R.sample(U[g], 2)
    if max(f1, f2) // min(f1, f2) > 10 ** 6:
        return None
    x = F(R.randint(1, 999), R.choice([1, 10, 100]))
    y = x * f1 / f2
    if (y * 1000).denominator != 1 or y > 10 ** 7 or y < F(1, 1000):
        return None
    r = max(f1, f2) // min(f1, f2)
    return M("Quanto é %s %s em %s?" % (d(x), u1, u2), "%s %s" % (d(y), u2), ["%s %s" % (d(y * 10) if (y * 10 * 1000).denominator == 1 else d(y / 10, 4), u2), "%s %s" % (d(y / 10, 4) if (y / 10 * 10000).denominator == 1 else d(y * 100), u2), "%s %s" % (d(x * f2 / f1, 6), u2) if (x * f2 / f1 * 10 ** 6).denominator == 1 else "%s %s" % (d(y * 100), u2)],
             "1 %s = %s %s. De %s para %s, %s %s: <b>%s %s</b>." % (max((u1, f1), (u2, f2), key=lambda t: t[1])[0], d(r), min((u1, f1), (u2, f2), key=lambda t: t[1])[0], u1, u2, "multiplique por" if f1 > f2 else "divida por", d(r), d(y), u2))


def s2_tempo():
    k = R.choice(["hmin", "minh", "s", "dias"])
    if k == "hmin":
        h, m = R.randint(1, 5), R.choice([10, 15, 20, 30, 40, 45, 50])
        return M("Quantos minutos há em %d h %d min?" % (h, m), "%d min" % (60 * h + m), ["%d min" % (100 * h + m), "%d min" % (60 * h), "%d min" % (60 * (h + 1) + m)], "%d × 60 + %d = <b>%d min</b>." % (h, m, 60 * h + m))
    if k == "minh":
        t = R.randint(70, 400)
        h, m = divmod(t, 60)
        if m == 0:
            return None
        return M("Quanto é %d minutos em horas e minutos?" % t, "%d h %d min" % (h, m), ["%d h %d min" % (t // 100, t % 100) if t % 100 < 60 else "%d h %d min" % (h + 1, m), "%s h" % d(F(t, 100)), "%d h %d min" % (h, m + 10) if m < 50 else "%d h %d min" % (h - 1, m)],
                 "%d ÷ 60 = %d e resto %d: <b>%d h %d min</b>." % (t, h, m, h, m))
    if k == "s":
        m = R.randint(2, 15)
        s = R.choice([0, 10, 20, 30, 45])
        return M("Quantos segundos há em %d min%s?" % (m, " e %d s" % s if s else ""), "%d s" % (60 * m + s), ["%d s" % (100 * m + s), "%d s" % (60 * m), "%d s" % (m * 3600)] if s else ["%d s" % (100 * m), "%d s" % (m * 3600), "%d s" % (60 * m + 60)],
                 "%d × 60%s = <b>%d s</b>." % (m, " + %d" % s if s else "", 60 * m + s))
    w = R.randint(2, 9)
    return M("Quantos dias há em %d semanas e %d dias?" % (w, w % 6 + 1), "%d dias" % (7 * w + w % 6 + 1), ["%d dias" % (10 * w + w % 6 + 1), "%d dias" % (7 * w), "%d dias" % (5 * w + w % 6 + 1)], "%d × 7 + %d = <b>%d dias</b>." % (w, w % 6 + 1, 7 * w + w % 6 + 1))


def s3_problemas():
    k = R.choice(["garrafas", "fita", "pacotes", "corrida", "temp", "filme"])
    if k == "garrafas":
        L, ml = R.randint(2, 12), R.choice([200, 250, 300, 500])
        return M("Quantos copos de %d mL podemos encher com %d L de suco?" % (ml, L), d(L * 1000 // ml), [d(L * 100 // ml) if L * 100 // ml else "1", d(L * ml), d(L * 1000 // ml + 2)], "%d L = %s mL; %s ÷ %d = <b>%s copos</b>." % (L, d(L * 1000), d(L * 1000), ml, d(L * 1000 // ml)))
    if k == "fita":
        m, c = R.randint(2, 9), R.choice([20, 25, 40, 50])
        return M("Uma fita de %d m foi cortada em pedaços de %d cm. Quantos pedaços se obtêm?" % (m, c), d(m * 100 // c), [d(m * 10 // c) if m * 10 // c else "1", d(m * c), d(m * 100 // c + 1)], "%d m = %d cm; %d ÷ %d = <b>%d pedaços</b>." % (m, m * 100, m * 100, c, m * 100 // c))
    if k == "pacotes":
        n, g = R.randint(4, 30), R.choice([250, 500, 750, 200])
        return M("Uma caixa tem %d pacotes de %d g. Quantos quilogramas há na caixa?" % (n, g), "%s kg" % d(F(n * g, 1000)), ["%s kg" % d(F(n * g, 100)), "%s kg" % d(n * g), "%s kg" % d(F(n * g, 10000), 4)], "%d × %d = %s g = <b>%s kg</b>." % (n, g, d(n * g), d(F(n * g, 1000))))
    if k == "corrida":
        v, n = R.choice([400, 250, 800]), R.randint(3, 15)
        return M("Uma pista tem %d m. Quantos km percorre quem dá %d voltas?" % (v, n), "%s km" % d(F(v * n, 1000)), ["%s km" % d(F(v * n, 100)), "%s km" % d(v * n), "%s km" % d(F(v * n, 10000), 4)], "%d × %d = %s m = <b>%s km</b>." % (v, n, d(v * n), d(F(v * n, 1000))))
    if k == "temp":
        a, b = R.randint(12, 22), R.randint(25, 38)
        return M("De manhã fazia %d °C e à tarde %d °C. Quantos graus a temperatura subiu?" % (a, b), "%d °C" % (b - a), ["%d °C" % (a + b), "%d °C" % (b - a + 10), "%d °C" % (b - a - 1)], "%d − %d = <b>%d °C</b>." % (b, a, b - a))
    h1, m1 = R.randint(13, 20), R.choice([0, 10, 15, 20, 30, 40, 45])
    dur = R.randint(85, 170)
    t = h1 * 60 + m1 + dur
    return M("Um filme começou às %dh%02d e durou %d minutos. A que horas terminou?" % (h1, m1, dur), "%dh%02d" % divmod(t, 60), ["%dh%02d" % divmod(t + 40, 60), "%dh%02d" % ((h1 * 60 + m1 + dur // 100 * 60 + dur % 100) // 60, (h1 * 60 + m1 + dur // 100 * 60 + dur % 100) % 60), "%dh%02d" % divmod(t - 30, 60)],
             "%d min = %d h %d min; %dh%02d + %d h %d min = <b>%dh%02d</b>." % (dur, dur // 60, dur % 60, h1, m1, dur // 60, dur % 60, t // 60, t % 60))


s4_conceitos = bank(R, [
    ("Qual unidade é mais adequada para medir a distância entre duas cidades?", "quilômetro", ["centímetro", "milímetro", "grama"]),
    ("Qual unidade é mais adequada para medir a massa de um caminhão carregado?", "tonelada", ["miligrama", "grama", "mililitro"]),
    ("Qual unidade é mais adequada para a dose de um xarope?", "mililitro", ["litro", "quilômetro", "tonelada"]),
    ("1 tonelada tem quantos quilogramas?", "1.000", ["100", "10", "10.000"]),
    ("1 litro tem quantos mililitros?", "1.000", ["100", "10", "10.000"]),
    ("Meia hora são quantos minutos?", "30", ["50", "15", "60"]),
    ("1,5 h é igual a…", "1 h 30 min", ["1 h 50 min", "1 h 5 min", "15 min"]),
    ("Um quarto de hora são…", "15 minutos", ["25 minutos", "4 minutos", "40 minutos"]),
    ("A temperatura em que a água ferve (ao nível do mar) é…", "100 °C", ["0 °C", "37 °C", "212 °C"]),
    ("A temperatura normal do corpo humano é cerca de…", "36,5 °C", ["20 °C", "100 °C", "50 °C"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Comprimento, massa e capacidade", mix(R, seen, [(m_comp, 7), (m_massa, 7), (m_cap, 6)])),
        ("Transformar unidades", mix(R, seen, [(s1_conv, 20)])),
        ("Tempo", mix(R, seen, [(s2_tempo, 16), (m_tempo, 4)])),
        ("Unidades adequadas", mix(R, seen, [(s4_conceitos, 10), (s1_conv, 10)])),
        ("Problemas com medidas", mix(R, seen, [(s3_problemas, 20)])),
    ]
    body = lesson(
        ["Comprimento: 1 km = 1.000 m; 1 m = 100 cm; 1 cm = 10 mm. Massa: 1 t = 1.000 kg; 1 kg = 1.000 g; 1 g = 1.000 mg. Capacidade: 1 L = 1.000 mL.",
         "Da unidade maior para a menor, <b>multiplique</b>; da menor para a maior, <b>divida</b>.",
         "Tempo não é decimal: 1 h = 60 min e 1 min = 60 s. Assim, 1,5 h = 1 h 30 min."],
        [("2,5 km em metros", ["2,5 × 1.000"], "2.500 m"),
         ("750 g em kg", ["750 ÷ 1.000"], "0,75 kg"),
         ("135 min", ["135 ÷ 60 = 2 e resto 15"], "2 h 15 min")],
        [["Multiplicar quando é para dividir", "De g para kg o número diminui."],
         ["Usar 100 em vez de 1.000", "kg, km e L têm 1.000."],
         ["Ler 1,30 h como 1 h 30 min", "1,30 h = 1 h 18 min."]])
    faq = [("Como transformar unidades de medida?", "Descubra quantas vezes uma unidade cabe na outra (por exemplo, 1 km = 1.000 m). Para passar para a unidade menor, multiplique; para a maior, divida."),
           ("O que a BNCC pede no 6º ano?", "Resolver e elaborar problemas que envolvam as grandezas comprimento, massa, tempo, temperatura, área, capacidade e volume, sem uso de fórmulas, inseridos em contextos oriundos de situações reais (EF06MA24).")]
    unit(R, "grandezas-e-medidas", "M", ["EF06MA24"],
         "Resolver e elaborar problemas que envolvam as grandezas comprimento, massa, tempo, temperatura, área (triângulos e retângulos), capacidade e volume (sólidos formados por blocos retangulares), sem uso de fórmulas, inseridos, sempre que possível, em contextos oriundos de situações reais e/ou relacionadas às outras áreas do conhecimento",
         "Grandezas e medidas: transformação de unidades", "Grandezas e medidas",
         "Atividades de matemática para o 6º ano sobre grandezas e medidas: comprimento, massa, capacidade, tempo e temperatura, transformação de unidades e problemas. 100 exercícios com gabarito.",
         "Da maior para a menor: multiplique.", "1 h = 60 min, não 100.",
         body, faq, sets, 17, grade="6-ano")


if __name__ == "__main__":
    main()
