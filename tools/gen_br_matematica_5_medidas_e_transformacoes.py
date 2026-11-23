# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Medidas e transformações de unidades (Grandezas e medidas, EF05MA19)
  python3 tools/gen_br_matematica_5_medidas_e_transformacoes.py
Comprimento (km, m, cm, mm), massa (t, kg, g, mg), capacidade (L, mL), tempo (h, min, s; dia, semana, ano, década, século)
e temperatura (°C); transformar unidades com decimais; comparar medidas; problemas do dia a dia.
Erros: multiplicar quando é para dividir, usar 100 em vez de 1.000 (1 km = 100 m), achar que 1 h = 100 min, 2,5 h = 2 h 50 min.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, dz, dur, table, Kids

R = random.Random(80518)
K = Kids(R)
NB = " "
FAT = {("km", "m"): 1000, ("m", "cm"): 100, ("cm", "mm"): 10, ("m", "mm"): 1000, ("t", "kg"): 1000, ("kg", "g"): 1000, ("g", "mg"): 1000, ("L", "mL"): 1000}


def U(v, u):
    return v + NB + u


def conv(big, small):
    f = FAT[(big, small)]
    z = len(str(f)) - 1
    if R.random() < 0.5:
        a = R.randint(2, 99)
        k = R.choice([0, 1, 2]) if z >= 2 else R.choice([0, 1])
        val = dz(a, k)
        ans = num(a * f // 10 ** k)
        w = [num(a * f // 10 ** k // 10) if a * f // 10 ** k >= 10 else None, num(a * f // 10 ** k * 10), num(a * 100 // 10 ** k) if f == 1000 else num(a * 1000 // 10 ** k), num(a * 10 // 10 ** k) if a * 10 // 10 ** k else None]
        if a * f % 10 ** k:
            return None
        return mcq("Quantos %s são %s?" % (small, U(val, big)), U(ans, small), [U(x, small) for x in w if x and x != ans],
                   "1 %s = %s %s. Multiplique por %s: %s × %s = <b>%s %s</b>." % (big, num(f), small, num(f), val, num(f), ans, small))
    n = R.randint(5, 9999)
    if n % 10 == 0 and R.random() < 0.5:
        return None
    ans = dz(n, z)
    w = [dz(n, z - 1) if z > 1 else dz(n, z + 2), dz(n, z + 1), num(n * f), num(n)]
    return mcq("Quantos %s são %s?" % (big, U(num(n), small)), U(ans, big), [U(x, big) for x in w if x != ans],
               "1 %s = %s %s. Divida por %s: %s ÷ %s = <b>%s %s</b>." % (big, num(f), small, num(f), num(n), num(f), ans, big))


def s1_comp():
    big, small = R.choice([("km", "m"), ("m", "cm"), ("cm", "mm"), ("m", "mm")])
    return conv(big, small)


def s2_massa():
    if R.random() < 0.2:
        big, small = "t", "kg"
    elif R.random() < 0.15:
        big, small = "g", "mg"
    else:
        big, small = "kg", "g"
    return conv(big, small)


def s2_cap():
    return conv("L", "mL")


def s3_comparar():
    k = R.choice(["comp", "massa", "cap"])
    if k == "comp":
        a = R.randint(101, 999)
        b = a + R.choice([-30, 30, 0, 100, -100, 9, -9])
        sx, sy = U(dz(a, 2), "m"), U(num(b), "cm")
        cx, cy = a, b
    elif k == "massa":
        a = R.randint(11, 99)
        b = a * 100 + R.choice([-200, 200, 0, 50, -50])
        sx, sy = U(dz(a, 1), "kg"), U(num(b), "g")
        cx, cy = a * 100, b
    else:
        a = R.randint(11, 99)
        b = a * 100 + R.choice([-150, 150, 0, 250, -250])
        sx, sy = U(dz(a, 1), "L"), U(num(b), "mL")
        cx, cy = a * 100, b
    sign = "=" if cx == cy else ("&gt;" if cx > cy else "&lt;")
    good = "%s %s %s" % (sx, sign, sy)
    w = ["%s %s %s" % (sx, s_, sy) for s_ in ("=", "&gt;", "&lt;") if s_ != sign] + ["%s %s %s" % (sy, sign if sign != "=" else "&gt;", sx)]
    return mcq("Qual frase está certa? (Compare %s e %s.)" % (sx, sy), good, w,
               "Escreva as duas medidas na mesma unidade e compare: <b>%s</b>." % good)


def s4_tempo():
    k = R.choice(["h_min", "min_h", "min_s", "dias", "semana", "anos", "decimal", "seculo"])
    if k == "h_min":
        h = R.randint(2, 9)
        return mcq("Quantos minutos há em %d horas?" % h, "%d min" % (h * 60), ["%d min" % x for x in (h * 100, h * 60 + 60, h + 60, h * 30)],
                   "1 h = 60 min: %d × 60 = <b>%d min</b>." % (h, h * 60))
    if k == "min_h":
        m = R.randint(65, 400)
        if m % 60 == 0:
            return None
        return mcq("Quanto é %d minutos em horas e minutos?" % m, dur(m), [dur(m // 100 * 60 + m % 100) if m % 100 < 60 and m >= 100 else dur(m + 10), dur(m - 60), dur(m + 60), dur(m // 60 * 60 + (m % 60) // 10)],
                   "%d ÷ 60 = %d e resto %d: <b>%s</b>." % (m, m // 60, m % 60, dur(m)))
    if k == "min_s":
        m = R.randint(2, 10)
        return mcq("Quantos segundos há em %d minutos?" % m, "%d s" % (m * 60), ["%d s" % x for x in (m * 100, m * 60 + 60, m * 10)],
                   "1 min = 60 s: %d × 60 = <b>%d s</b>." % (m, m * 60))
    if k == "dias":
        d = R.randint(2, 7)
        return mcq("Quantas horas há em %d dias?" % d, "%d h" % (d * 24), ["%d h" % x for x in (d * 12, d * 60, d * 24 + 24, d * 20)],
                   "1 dia = 24 h: %d × 24 = <b>%d h</b>." % (d, d * 24))
    if k == "semana":
        w = R.randint(2, 12)
        return mcq("Quantos dias há em %d semanas?" % w, "%d dias" % (w * 7), ["%d dias" % x for x in (w * 5, w * 10, w * 7 + 7, w * 30)],
                   "1 semana = 7 dias: %d × 7 = <b>%d dias</b>." % (w, w * 7))
    if k == "anos":
        n = R.randint(2, 9)
        return mcq("Quantos meses há em %d anos?" % n, "%d meses" % (n * 12), ["%d meses" % x for x in (n * 10, n * 365, n * 12 + 12, n * 4)],
                   "1 ano = 12 meses: %d × 12 = <b>%d meses</b>." % (n, n * 12))
    if k == "decimal":
        h, m = R.choice([(1, 30), (2, 30), (3, 30), (1, 15), (2, 15), (1, 45), (3, 45), (4, 30)])
        dec = {30: "5", 15: "25", 45: "75"}[m]
        return mcq("%d,%s h são quantas horas e minutos?" % (h, dec), dur(h * 60 + m), [dur(h * 60 + int(dec)) if int(dec) < 60 else dur(h * 60 + 50), dur(h * 60 + int(dec[0]) * 10), dur(h * 60 + 60 - m) if 60 - m != m else dur(h * 60 + 20)],
                   "0,%s h = %s de 60 min = %d min. <b>%s</b>." % (dec, {30: "metade", 15: "um quarto", 45: "três quartos"}[m], m, dur(h * 60 + m)))
    n = R.choice([1, 2, 3])
    k2 = R.choice(["década", "século"])
    v = 10 if k2 == "década" else 100
    return mcq("Quantos anos há em %d %s?" % (n, k2 if n == 1 else ("décadas" if k2 == "década" else "séculos")), "%d anos" % (n * v),
               ["%s anos" % num(x) for x in (n * (100 if v == 10 else 10), n * 1000, n * v + v)], "1 %s = %d anos: %d × %d = <b>%d anos</b>." % (k2, v, n, v, n * v))


def s4_temp():
    a = R.randint(16, 32)
    d = R.randint(3, 12)
    k = R.choice(["sobe", "desce", "dif"])
    if k == "sobe":
        return mcq("De manhã a temperatura era %d °C. À tarde subiu %d graus. Qual era a temperatura à tarde?" % (a, d), "%d °C" % (a + d), ["%d °C" % x for x in (a - d, a + d + 1, d)],
                   "%d + %d = <b>%d °C</b>." % (a, d, a + d))
    if k == "desce":
        return mcq("À tarde fazia %d °C. À noite a temperatura caiu %d graus. Quanto marcava o termômetro à noite?" % (a, d), "%d °C" % (a - d), ["%d °C" % x for x in (a + d, a - d - 1, d)],
                   "%d − %d = <b>%d °C</b>." % (a, d, a - d))
    b = a + d
    return mcq("Num dia, a mínima foi %d °C e a máxima foi %d °C. Qual foi a diferença?" % (a, b), "%d graus" % d, ["%d graus" % x for x in (a + b, d + 1, b)],
               "%d − %d = <b>%d graus</b>." % (b, a, d))


def s5_problema():
    k = R.choice(["corrida", "garrafa", "receita", "viagem", "fita", "saco", "filme", "remedio"])
    p, g = K.next()
    if k == "corrida":
        v = R.randint(3, 9)
        n = R.randint(2, 6)
        return mcq("Uma pista tem %d00 m. %s deu %d voltas. Quantos quilômetros correu?" % (v, p, n), U(dz(v * n, 1), "km"), [U(x, "km") for x in (dz(v * n, 2), num(v * n * 100), dz(v * n, 0))],
                   "%d × %d00 m = %s m = <b>%s km</b>." % (n, v, num(v * n * 100), dz(v * n, 1)))
    if k == "garrafa":
        a = R.choice([250, 300, 350, 500, 200])
        n = R.randint(3, 10)
        return mcq("%s bebeu %d copos de %d mL de água. Quantos litros bebeu?" % (p, n, a), U(dz(a * n, 3), "L"), [U(x, "L") for x in (dz(a * n, 2), num(a * n), dz(a * n, 1))],
                   "%d × %d mL = %s mL = <b>%s L</b>." % (n, a, num(a * n), dz(a * n, 3)))
    if k == "receita":
        a = R.choice([250, 500, 750, 125, 400])
        n = R.randint(2, 8)
        return mcq("Uma receita usa %d g de farinha. Para %d receitas, quantos quilogramas são necessários?" % (a, n), U(dz(a * n, 3), "kg"), [U(x, "kg") for x in (dz(a * n, 2), num(a * n), dz(a * n, 1))],
                   "%d × %d g = %s g = <b>%s kg</b>." % (n, a, num(a * n), dz(a * n, 3)))
    if k == "viagem":
        h1, m1 = R.randint(6, 10), R.choice([0, 15, 30, 45])
        d = R.randint(70, 300)
        if d % 5:
            return None
        t = h1 * 60 + m1 + d
        return mcq("Uma viagem de ônibus começou às %dh%s e durou %s. A que horas terminou?" % (h1, "%02d" % m1 if m1 else "", dur(d)), "%dh%02d" % divmod(t, 60) if t % 60 else "%dh" % (t // 60),
                   ["%dh%02d" % divmod(t + 40, 60) if (t + 40) % 60 else "%dh" % ((t + 40) // 60), "%dh%02d" % divmod(t - 60, 60) if (t - 60) % 60 else "%dh" % ((t - 60) // 60), "%dh%02d" % divmod(t + 60, 60) if (t + 60) % 60 else "%dh" % ((t + 60) // 60)],
                   "%dh%s + %s = <b>%s</b>." % (h1, "%02d" % m1 if m1 else "", dur(d), "%dh%02d" % divmod(t, 60) if t % 60 else "%dh" % (t // 60)))
    if k == "fita":
        L = R.randint(2, 9)
        c = R.choice([20, 25, 40, 50])
        return mcq("Um rolo tem %d m de fita. Quantos pedaços de %d cm dá para cortar?" % (L, c), str(L * 100 // c), [str(x) for x in (L * 10 // c if L * 10 // c else L * 2, L * 1000 // c, L * c)],
                   "%d m = %d cm. %d ÷ %d = <b>%d pedaços</b>." % (L, L * 100, L * 100, c, L * 100 // c))
    if k == "saco":
        t = R.randint(2, 9)
        s = R.choice([5, 10, 20, 25, 50])
        return mcq("Um caminhão leva %d t de arroz em sacos de %d kg. Quantos sacos são?" % (t, s), num(t * 1000 // s), [num(x) for x in (t * 100 // s, t * s, t * 1000 // s * 10)],
                   "%d t = %s kg. %s ÷ %d = <b>%s sacos</b>." % (t, num(t * 1000), num(t * 1000), s, num(t * 1000 // s)))
    if k == "filme":
        a, b = R.randint(85, 150), R.randint(85, 150)
        if a == b:
            return None
        return mcq("Um filme dura %d minutos e outro dura %s. Quanto tempo os dois duram juntos?" % (a, dur(b)), dur(a + b), [dur(x) for x in (a + b + 40, a + b - 60, a + b + 60)],
                   "%d min + %d min = %d min = <b>%s</b>." % (a, b, a + b, dur(a + b)))
    d = R.choice([5, 10, 7, 15])
    n = R.choice([3, 4, 2])
    return mcq("Um xarope deve ser tomado %d vezes por dia, %d mL de cada vez, durante 7 dias. Quantos mililitros serão tomados?" % (n, d), "%d mL" % (d * n * 7), ["%d mL" % x for x in (d * n, d * 7, d * n * 7 + d)],
               "%d × %d × 7 = <b>%d mL</b>." % (n, d, d * n * 7))


def main():
    seen = set()
    sets = [
        ("Comprimento", mix(R, seen, [(s1_comp, 20)])),
        ("Massa e capacidade", mix(R, seen, [(s2_massa, 12), (s2_cap, 8)])),
        ("Comparar medidas", mix(R, seen, [(s3_comparar, 20)])),
        ("Tempo e temperatura", mix(R, seen, [(s4_tempo, 14), (s4_temp, 6)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para ir de uma unidade <b>maior</b> para uma <b>menor</b>, multiplique (2 km = 2.000 m). Da menor para a maior, divida (350 cm = 3,5 m).",
         "Lembre: 1 km = 1.000 m; 1 m = 100 cm; 1 cm = 10 mm; 1 kg = 1.000 g; 1 t = 1.000 kg; 1 L = 1.000 mL.",
         "O tempo <b>não é decimal</b>: 1 h = 60 min, 1 min = 60 s. Por isso 1,5 h = 1 h 30 min.",
         "Para comparar medidas, escreva as duas na mesma unidade."],
        [("Quantos metros são 2,5 km?", ["1 km = 1.000 m", "2,5 × 1.000"], "2.500 m"),
         ("Quanto é 150 minutos?", ["150 ÷ 60 = 2 e resto 30"], "2 h 30 min")],
        [["Usar 100 em vez de 1.000: 1 km = 100 m", "Quilo quer dizer mil: 1 km = 1.000 m, 1 kg = 1.000 g."],
         ["Multiplicar quando é para dividir", "Da unidade menor para a maior, o número fica menor: divida."],
         ["Achar que 2,5 h = 2 h 50 min", "0,5 h é meia hora = 30 min."]],
        table(["Grandeza", "Unidades"], [["Comprimento", "1 km = 1.000 m; 1 m = 100 cm; 1 cm = 10 mm"], ["Massa", "1 t = 1.000 kg; 1 kg = 1.000 g"],
                                         ["Capacidade", "1 L = 1.000 mL"], ["Tempo", "1 h = 60 min; 1 min = 60 s; 1 dia = 24 h"]]))
    faq = [("Quais unidades o 5º ano transforma?", "A BNCC pede problemas com comprimento, área, massa, tempo, temperatura e capacidade, transformando as unidades mais usuais (km, m, cm, mm; t, kg, g; L, mL; h, min, s)."),
           ("Por que 1,5 hora não é 1 hora e 50 minutos?", "Porque a hora tem 60 minutos, não 100. Meia hora (0,5 h) são 30 minutos.")]
    make_unit(R, "medidas-e-transformacoes", "M", ["EF05MA19"],
              "Resolver e elaborar problemas envolvendo medidas das grandezas comprimento, área, massa, tempo, temperatura e capacidade, recorrendo a transformações entre as unidades mais usuais em contextos socioculturais",
              "Medidas e transformações de unidades", "Transformar unidades",
              "Atividades de matemática para o 5º ano sobre transformações de unidades: km, m, cm e mm; t, kg e g; L e mL; horas, minutos e segundos; temperatura e problemas. 100 exercícios com gabarito.",
              "Da maior para a menor: multiplique. Da menor para a maior: divida.", "1 h = 60 min (o tempo não é decimal).",
              body, faq, sets, 18, grade="5-ano")


if __name__ == "__main__":
    main()
