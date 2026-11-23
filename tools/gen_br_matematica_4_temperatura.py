# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Temperatura (Grandezas e medidas, Probabilidade e estatística, EF04MA23, EF04MA24)
  python3 tools/gen_br_matematica_4_temperatura.py
Temperatura e o grau Celsius (°C); ler o termômetro; temperaturas de referência (água congela a 0 °C e ferve a 100 °C, corpo ≈ 36 °C);
comparar temperaturas de cidades do Brasil; máxima, mínima e variação do dia; tabelas e gráficos de colunas de temperatura.
Erros: ler a escala do termômetro de 1 em 1 quando vai de 2 em 2, confundir máxima e mínima, somar a máxima e a mínima em vez de subtrair.
"""
import random
from br_common import mcq, lesson, make_unit, mix, wrap, line, text, INK, RED, table, grafico, Kids

R = random.Random(80419)
K = Kids(R)
CID = [("Manaus", 27, 34), ("Belém", 24, 33), ("Fortaleza", 24, 31), ("Recife", 23, 30), ("Salvador", 23, 30), ("Cuiabá", 22, 36), ("Brasília", 15, 28),
       ("Belo Horizonte", 15, 27), ("Rio de Janeiro", 20, 30), ("São Paulo", 13, 25), ("Curitiba", 8, 21), ("Florianópolis", 13, 23), ("Porto Alegre", 10, 24),
       ("Campo Grande", 15, 30), ("Goiânia", 16, 31), ("Teresina", 22, 36), ("Natal", 23, 30), ("Gramado", 5, 18)]


def termometro(t, step):
    lo, hi = 0, 40
    H, y0 = 240, 220
    s = ["<rect x='52' y='14' width='16' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='2'/>" % (y0 - 4, INK),
         "<circle cx='60' cy='%d' r='16' fill='%s' stroke='%s' stroke-width='2'/>" % (y0 + 10, RED, INK)]
    ty = y0 - (t - lo) * (y0 - 24) / (hi - lo)
    s.append("<rect x='56' y='%.1f' width='8' height='%.1f' fill='%s'/>" % (ty, y0 + 4 - ty, RED))
    for v in range(lo, hi + 1, step):
        y = y0 - (v - lo) * (y0 - 24) / (hi - lo)
        big = v % 10 == 0
        s.append(line(68, y, 68 + (14 if big else 8), y, INK, 1.4))
        if big:
            s.append(text(90, y + 4, "%d °C" % v, 12, anchor="start"))
    return wrap(140, H + 16, "".join(s), "termômetro em graus Celsius", lg=True)


def s1_termometro():
    step = R.choice([1, 2])
    t = R.randrange(4, 39, step)
    if t % 10 == 0:
        return None
    w = [t + step, t - step, t + 10 if t + 10 <= 40 else t - 10, t // 10 * 10 + (t % 10) // 2 if step == 2 else t + 2]
    return mcq(termometro(t, step) + "Que temperatura o termômetro marca? (Cada risquinho vale %d grau%s.)" % (step, "" if step == 1 else "s"), "%d °C" % t,
               ["%d °C" % x for x in w if x != t and 0 < x <= 40], "Conte os risquinhos a partir do %d: cada um vale %d. <b>%d °C</b>." % (t // 10 * 10, step, t))


REF = [("Em que temperatura a água congela?", "0 °C", ["10 °C", "100 °C", "36 °C"]), ("Em que temperatura a água ferve?", "100 °C", ["50 °C", "0 °C", "36 °C"]),
       ("Qual é a temperatura normal do corpo humano, mais ou menos?", "36 °C", ["20 °C", "50 °C", "10 °C"]),
       ("Um dia muito quente no verão do Rio de Janeiro pode chegar a…", "38 °C", ["8 °C", "100 °C", "0 °C"]),
       ("Uma noite fria de inverno em Curitiba pode ter…", "5 °C", ["35 °C", "60 °C", "100 °C"]),
       ("Que instrumento mede a temperatura?", "o termômetro", ["a balança", "a régua", "o relógio"]),
       ("A unidade de temperatura que usamos no Brasil é…", "o grau Celsius (°C)", ["o metro (m)", "o quilograma (kg)", "o litro (L)"]),
       ("Uma pessoa com 39 °C de temperatura provavelmente está…", "com febre", ["com frio normal", "muito bem", "dormindo"]),
       ("A temperatura dentro de uma geladeira é mais ou menos…", "5 °C", ["35 °C", "60 °C", "90 °C"]),
       ("O aumento da temperatura média da Terra é chamado de…", "aquecimento global", ["chuva ácida", "eclipse", "maré alta"])]


def s1_ref():
    q, a, w = R.choice(REF)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def s2_comparar():
    cs = R.sample(CID, 4)
    k = R.choice(["max", "min", "quente", "fria"])
    if k in ("max", "quente"):
        vals = [c[2] for c in cs]
        lab = "Temperatura máxima"
    else:
        vals = [c[1] for c in cs]
        lab = "Temperatura mínima"
    if len(set(vals)) < 4:
        return None
    tb = table(["Cidade", lab], [[c[0], "%d °C" % v] for c, v in zip(cs, vals)])
    i = vals.index(max(vals)) if k in ("max", "quente") else vals.index(min(vals))
    pal = "mais quente" if k in ("max", "quente") else "mais fria"
    return mcq(tb + "Num mesmo dia, qual destas cidades ficou %s?" % pal, cs[i][0], [c[0] for j, c in enumerate(cs) if j != i],
               "Compare as temperaturas: a %s é %s, com <b>%d °C</b>." % (pal, cs[i][0], vals[i]))


def s2_dif():
    a, b = R.sample(CID, 2)
    k = R.choice(["max", "min"])
    va, vb = (a[2], b[2]) if k == "max" else (a[1], b[1])
    if va == vb:
        return None
    return mcq("Num dia, a temperatura %s foi %d °C em %s e %d °C em %s. Qual foi a diferença?" % ("máxima" if k == "max" else "mínima", va, a[0], vb, b[0]), "%d graus" % abs(va - vb),
               ["%d graus" % x for x in (va + vb, abs(va - vb) + 1, max(va, vb))], "%d − %d = <b>%d graus</b>." % (max(va, vb), min(va, vb), abs(va - vb)))


def s3_variacao():
    c = R.choice(CID)
    lo, hi = c[1] + R.randint(-2, 2), c[2] + R.randint(-2, 2)
    k = R.choice(["amp", "sobe", "desce"])
    if k == "amp":
        return mcq("Em %s, a mínima do dia foi %d °C e a máxima foi %d °C. Quantos graus a temperatura variou?" % (c[0], lo, hi), "%d graus" % (hi - lo),
                   ["%d graus" % x for x in (hi + lo, hi - lo + 2, hi)], "Variação = máxima − mínima = %d − %d = <b>%d graus</b>." % (hi, lo, hi - lo))
    d = R.randint(3, 9)
    if k == "sobe":
        return mcq("Às 7h, em %s, fazia %d °C. Até o meio-dia, a temperatura subiu %d graus. Quanto marcava ao meio-dia?" % (c[0], lo, d), "%d °C" % (lo + d),
                   ["%d °C" % x for x in (lo - d, lo + d + 1, d)], "%d + %d = <b>%d °C</b>." % (lo, d, lo + d))
    return mcq("Às 15h, em %s, fazia %d °C. À noite a temperatura caiu %d graus. Quanto passou a marcar?" % (c[0], hi, d), "%d °C" % (hi - d),
               ["%d °C" % x for x in (hi + d, hi - d - 1, d)], "%d − %d = <b>%d °C</b>." % (hi, d, hi - d))


DIAS = ["seg.", "ter.", "qua.", "qui.", "sex."]


def s4_grafico():
    c = R.choice(CID)
    vals = [R.randint(c[1] + 2, c[2] + 2) for _ in DIAS]
    if len(set(vals)) < 5:
        return None
    pic = "<p><b>Temperatura máxima em %s (°C)</b></p>" % c[0] + grafico(list(zip(DIAS, vals)), "°C", 5)
    k = R.choice(["max", "min", "um", "dif"])
    if k == "max":
        i = vals.index(max(vals))
        return mcq(pic + "Em que dia a máxima foi mais alta?", DIAS[i], [d for j, d in enumerate(DIAS) if j != i][:3], "A coluna mais alta é a de <b>%s</b> (%d °C)." % (DIAS[i], vals[i]))
    if k == "min":
        i = vals.index(min(vals))
        return mcq(pic + "Em que dia a máxima foi mais baixa?", DIAS[i], [d for j, d in enumerate(DIAS) if j != i][:3], "A coluna mais baixa é a de <b>%s</b> (%d °C)." % (DIAS[i], vals[i]))
    if k == "um":
        i = R.randrange(5)
        return mcq(pic + "Qual foi a temperatura máxima na %s?" % DIAS[i].replace("seg.", "segunda").replace("ter.", "terça").replace("qua.", "quarta").replace("qui.", "quinta").replace("sex.", "sexta"),
                   "%d °C" % vals[i], ["%d °C" % x for x in (vals[i] + 1, vals[i] - 1, vals[(i + 1) % 5])], "Siga a coluna e leia na escala: <b>%d °C</b>." % vals[i])
    i, j = R.sample(range(5), 2)
    return mcq(pic + "Quantos graus de diferença há entre a máxima de %s e a de %s?" % (DIAS[i], DIAS[j]), "%d graus" % abs(vals[i] - vals[j]),
               ["%d graus" % x for x in (vals[i] + vals[j], abs(vals[i] - vals[j]) + 2, max(vals[i], vals[j]))], "%d − %d = <b>%d graus</b>." % (max(vals[i], vals[j]), min(vals[i], vals[j]), abs(vals[i] - vals[j])))


def s4_tabela():
    c = R.choice(CID)
    mins = [R.randint(c[1] - 2, c[1] + 3) for _ in DIAS[:4]]
    maxs = [R.randint(c[2] - 3, c[2] + 2) for _ in DIAS[:4]]
    if any(a >= b for a, b in zip(mins, maxs)):
        return None
    amps = [b - a for a, b in zip(mins, maxs)]
    if len(set(amps)) < 4:
        return None
    tb = "<p><b>Temperaturas em %s</b></p>" % c[0] + table(["Dia", "Mínima", "Máxima"], [[d, "%d °C" % a, "%d °C" % b] for d, a, b in zip(DIAS, mins, maxs)])
    i = amps.index(max(amps))
    return mcq(tb + "Em que dia a temperatura variou mais (máxima − mínima)?", DIAS[i], [d for j, d in enumerate(DIAS[:4]) if j != i],
               "Variações: %s. A maior é em <b>%s</b>." % ("; ".join("%s %d" % (d, v) for d, v in zip(DIAS, amps)), DIAS[i]))


def s5_problema():
    k = R.choice(["febre", "forno", "viagem", "agua", "piscina"])
    p, g = K.next()
    if k == "febre":
        t = R.choice([37, 38, 39])
        d = R.randint(1, 3)
        return mcq("%s estava com %d °C de febre. Depois do remédio, a temperatura baixou %d grau%s. Quanto ficou?" % (p, t, d, "" if d == 1 else "s"), "%d °C" % (t - d),
                   ["%d °C" % x for x in (t + d, t - d - 1, d)], "%d − %d = <b>%d °C</b>." % (t, d, t - d))
    if k == "forno":
        a = R.choice([20, 22, 25, 28])
        b = R.choice([180, 200, 220])
        return mcq("Um forno estava a %d °C e foi aquecido até %d °C para assar um bolo. Quantos graus a temperatura subiu?" % (a, b), "%d graus" % (b - a),
                   ["%d graus" % x for x in (a + b, b - a + 10, b)], "%d − %d = <b>%d graus</b>." % (b, a, b - a))
    if k == "viagem":
        a, b = R.sample(CID, 2)
        if a[2] == b[2]:
            return None
        return mcq("%s saiu de %s, onde fazia %d °C, e chegou a %s, onde fazia %d °C. A temperatura subiu ou desceu? Quanto?" % (p, a[0], a[2], b[0], b[2]),
                   ("subiu %d graus" if b[2] > a[2] else "desceu %d graus") % abs(a[2] - b[2]),
                   [("desceu %d graus" if b[2] > a[2] else "subiu %d graus") % abs(a[2] - b[2]), ("subiu %d graus" if b[2] > a[2] else "desceu %d graus") % (a[2] + b[2]), "não mudou"],
                   "%d °C → %d °C: <b>%s %d graus</b>." % (a[2], b[2], "subiu" if b[2] > a[2] else "desceu", abs(a[2] - b[2])))
    if k == "agua":
        t = R.randint(15, 30)
        return mcq("Uma panela de água está a %d °C. Quantos graus ainda faltam para a água ferver (100 °C)?" % t, "%d graus" % (100 - t),
                   ["%d graus" % x for x in (100 + t, 100 - t + 10, t)], "100 − %d = <b>%d graus</b>." % (t, 100 - t))
    a = R.randint(24, 30)
    b = a + R.randint(2, 6)
    return mcq("A água da piscina estava a %d °C de manhã e a %d °C à tarde. Quantos graus esquentou?" % (a, b), "%d graus" % (b - a),
               ["%d graus" % x for x in (a + b, b - a + 1, b)], "%d − %d = <b>%d graus</b>." % (b, a, b - a))


def main():
    seen = set()
    sets = [
        ("Ler o termômetro", mix(R, seen, [(s1_termometro, 14), (s1_ref, 6)])),
        ("Comparar temperaturas", mix(R, seen, [(s2_comparar, 12), (s2_dif, 8)])),
        ("Máxima, mínima e variação", mix(R, seen, [(s3_variacao, 14), (s4_tabela, 6)])),
        ("Gráficos de temperatura", mix(R, seen, [(s4_grafico, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 16), (s1_ref, 4)])),
    ]
    body = lesson(
        ["A <b>temperatura</b> mede o quanto algo está quente ou frio. No Brasil usamos o <b>grau Celsius (°C)</b> e medimos com o <b>termômetro</b>.",
         "Referências: a água congela a 0 °C e ferve a 100 °C; o corpo humano fica perto de 36 °C.",
         "Antes de ler o termômetro, veja quanto vale cada risquinho (1 grau, 2 graus…).",
         "A <b>variação</b> do dia é a máxima menos a mínima."],
        [("Mínima 18 °C, máxima 29 °C. Quanto variou?", ["máxima − mínima", "29 − 18"], "11 graus"),
         ("Estava 24 °C e caiu 6 graus.", ["24 − 6"], "18 °C")],
        [["Ler a escala de 1 em 1 quando vai de 2 em 2", "Conte quanto vale cada risquinho antes."],
         ["Confundir máxima e mínima", "Máxima é a mais alta do dia; mínima, a mais baixa."],
         ["Somar a máxima e a mínima para achar a variação", "Variação é uma subtração: máxima − mínima."]],
        termometro(26, 2))
    faq = [("O que o 4º ano estuda sobre temperatura?", "A BNCC pede reconhecer o grau Celsius, comparar temperaturas de regiões do Brasil e do exterior, registrar máximas e mínimas e fazer gráficos de colunas com as variações diárias."),
           ("Como fazer um registro de temperatura em casa?", "Anote a máxima e a mínima da previsão do tempo durante uma semana e faça um gráfico de colunas. Depois compare os dias.")]
    make_unit(R, "temperatura", "M", ["EF04MA23", "EF04MA24"],
              "Reconhecer temperatura como grandeza e o grau Celsius como unidade de medida a ela associada e utilizá-lo em comparações de temperaturas em diferentes regiões do Brasil ou no exterior ou, ainda, em discussões que envolvam problemas relacionados ao aquecimento global; registrar as temperaturas máxima e mínima diárias, em locais do seu cotidiano, e elaborar gráficos de colunas com as variações diárias da temperatura",
              "Temperatura: termômetro, máxima, mínima e gráficos", "Temperatura",
              "Atividades de matemática para o 4º ano sobre temperatura: grau Celsius, ler o termômetro, comparar cidades do Brasil, máxima, mínima, variação e gráficos de colunas. 100 exercícios com gabarito.",
              "Temperatura em graus Celsius (°C).", "Variação do dia = máxima − mínima.",
              body, faq, sets, 19, grade="4-ano")


if __name__ == "__main__":
    main()
