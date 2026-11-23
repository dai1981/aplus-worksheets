# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Massa e capacidade (Grandezas e medidas, EF03MA20)
  python3 tools/gen_br_matematica_3_massa_e_capacidade.py
Quilograma, grama e miligrama; litro e mililitro; estimar a massa e a capacidade de objetos do dia a dia;
1 kg = 1.000 g e 1 L = 1.000 mL; balança de pratos; copo medidor; meio quilo e meio litro; comparar e problemas.
Erros: achar que o objeto maior é sempre mais pesado, comparar 1 kg com 800 g pelo número, ler errado a graduação.
"""
import random
import gen_fr_maths_ce2_masses_et_contenances as FRM
from br_common import mcq, num, lesson, make_unit, mix, Kids, relabel, NB, table, reais

R = random.Random(80317)
K = Kids(R)


def U(v, u):
    return "%s%s%s" % (num(v), NB, u)


MASSA = [("Um elefante tem cerca de", 5000, "kg"), ("Um saco de arroz tem", 5, "kg"), ("Uma borracha tem cerca de", 20, "g"), ("Um gato tem cerca de", 4, "kg"),
         ("Uma pena tem cerca de", 1, "g"), ("Um tablete de manteiga tem", 200, "g"), ("Uma criança de 8 anos tem cerca de", 25, "kg"),
         ("Uma maçã tem cerca de", 150, "g"), ("Um melão tem cerca de", 1, "kg"), ("Uma carta tem cerca de", 20, "g"), ("Uma bicicleta tem cerca de", 12, "kg"),
         ("Um pacote de macarrão tem", 500, "g"), ("Um cachorro grande tem cerca de", 30, "kg"), ("Um comprimido de remédio tem cerca de", 500, "mg"),
         ("Um grão de feijão tem cerca de", 300, "mg"), ("Um pacote de feijão tem", 1, "kg")]
CAP = [("Uma banheira cheia tem cerca de", 150, "L"), ("Uma colher de sopa tem cerca de", 15, "mL"), ("Um copo de suco tem cerca de", 200, "mL"),
       ("Um balde tem cerca de", 10, "L"), ("Uma lata de refrigerante tem", 350, "mL"), ("Uma garrafa de água grande tem", 2, "L"), ("Uma xícara de café tem cerca de", 50, "mL"),
       ("Um aquário pequeno tem cerca de", 40, "L"), ("Um regador tem cerca de", 8, "L"), ("Uma caixa de leite tem", 1, "L"), ("Uma caixinha de suco tem", 200, "mL"),
       ("A caixa-d’água de uma casa tem cerca de", 1000, "L")]


def balanca(obj, ws):
    return relabel(FRM.balance_svg(obj, ws), "balança de pratos em equilíbrio")


def copo(level, top, step):
    s = FRM.verre(level, top, step).replace(" cL<", NB + "mL<")
    return relabel(s, "copo medidor graduado em mililitros")


def s1_massa():
    o, v, u = R.choice(MASSA)
    return mcq("Que unidade completa a frase? %s %s …" % (o, num(v)), u, [x for x in ["kg", "g", "mg", "L"] if x != u],
               "%s %s <b>%s</b>." % (o, num(v), u))


def s1_cap():
    o, v, u = R.choice(CAP)
    return mcq("Que unidade completa a frase? %s %s …" % (o, num(v)), u, [x for x in ["L", "mL", "kg", "g"] if x != u],
               "%s %s <b>%s</b>." % (o, num(v), u))


def s2_converter():
    k = R.choice(["kg-g", "g-kg", "L-mL", "mL-L", "meio", "meioL", "kgg"])
    if k == "kg-g":
        v = R.randint(2, 9)
        return mcq("Quantos gramas há em %d kg?" % v, U(1000 * v, "g"), [U(100 * v, "g"), U(10 * v, "g"), U(v + 1000, "g")],
                   "1 kg = 1.000 g, então %d kg = <b>%s</b>." % (v, U(1000 * v, "g")))
    if k == "g-kg":
        v = R.randint(2, 9)
        return mcq("%s são quantos quilogramas?" % U(1000 * v, "g"), U(v, "kg"), [U(10 * v, "kg"), U(100 * v, "kg"), U(1000 * v, "kg")],
                   "1.000 g = 1 kg, então %s = <b>%s</b>." % (U(1000 * v, "g"), U(v, "kg")))
    if k == "L-mL":
        v = R.randint(2, 9)
        return mcq("Quantos mililitros há em %d L?" % v, U(1000 * v, "mL"), [U(100 * v, "mL"), U(10 * v, "mL"), U(v + 1000, "mL")],
                   "1 L = 1.000 mL, então %d L = <b>%s</b>." % (v, U(1000 * v, "mL")))
    if k == "mL-L":
        v = R.randint(2, 9)
        return mcq("%s são quantos litros?" % U(1000 * v, "mL"), U(v, "L"), [U(10 * v, "L"), U(100 * v, "L"), U(1000 * v, "L")],
                   "1.000 mL = 1 L, então %s = <b>%s</b>." % (U(1000 * v, "mL"), U(v, "L")))
    if k == "meio":
        return mcq("Meio quilo são quantos gramas?", U(500, "g"), [U(50, "g"), U(200, "g"), U(1500, "g")], "Metade de 1.000 g: <b>500 g</b>.") if R.random() < 0.5 else \
            mcq("Quantos gramas há em 1 kg e meio?", U(1500, "g"), [U(1050, "g"), U(150, "g"), U(1200, "g")], "1.000 g + 500 g = <b>1.500 g</b>.")
    if k == "meioL":
        return mcq("Meio litro são quantos mililitros?", U(500, "mL"), [U(50, "mL"), U(250, "mL"), U(5000, "mL")], "Metade de 1.000 mL: <b>500 mL</b>.") if R.random() < 0.5 else \
            mcq("Quantos copos de 250 mL enchem uma garrafa de 1 L?", "4 copos", ["2 copos", "10 copos", "5 copos"], "250 + 250 + 250 + 250 = 1.000 mL: <b>4 copos</b>.")
    a, b = R.randint(1, 4), R.choice([100, 200, 250, 500, 750])
    return mcq("%d kg e %d g são quantos gramas?" % (a, b), U(1000 * a + b, "g"), [U(a + b, "g"), U(100 * a + b, "g"), U(1000 * a + 10 * b, "g")],
               "%d kg = %s; %s + %d = <b>%s</b>." % (a, U(1000 * a, "g"), num(1000 * a), b, U(1000 * a + b, "g")))


def s3_comparar():
    k = R.choice(["kg", "L", "grande"])
    if k == "kg":
        a = R.randint(1, 3)
        g = 1000 * a + R.choice([-300, -100, 200, 500])
        big = U(a, "kg") if 1000 * a > g else U(g, "g")
        return mcq("O que é mais pesado: %s ou %s?" % (U(a, "kg"), U(g, "g")), big, [U(g, "g") if big == U(a, "kg") else U(a, "kg"), "são iguais", "não dá para saber"],
                   "%s = %s; compare com %s: <b>%s</b>." % (U(a, "kg"), U(1000 * a, "g"), U(g, "g"), big))
    if k == "L":
        a = R.randint(1, 3)
        m = 1000 * a + R.choice([-400, -150, 250, 600])
        big = U(a, "L") if 1000 * a > m else U(m, "mL")
        return mcq("O que cabe mais: %s ou %s?" % (U(a, "L"), U(m, "mL")), big, [U(m, "mL") if big == U(a, "L") else U(a, "L"), "cabem igual", "não dá para saber"],
                   "%s = %s: <b>%s</b>." % (U(a, "L"), U(1000 * a, "mL"), big))
    T = [("Uma bola de isopor grande ou uma bolinha de gude: qual é mais pesada?", "a bolinha de gude", ["a bola de isopor", "as duas pesam igual", "a maior é sempre mais pesada"]),
         ("1 kg de algodão ou 1 kg de ferro: qual é mais pesado?", "pesam o mesmo", ["o ferro", "o algodão", "não dá para saber"]),
         ("Um travesseiro grande ou um tijolo: qual costuma ser mais pesado?", "o tijolo", ["o travesseiro", "pesam o mesmo", "o maior sempre"]),
         ("Uma garrafa alta e fina ou uma panela larga: qual cabe mais água?", "depende: é preciso medir", ["sempre a garrafa alta", "sempre a panela", "as duas cabem igual"])]
    q, a, w = R.choice(T)
    return mcq(q, a, w, "Tamanho não é o mesmo que massa ou capacidade: <b>%s</b>." % a)


def s4_balanca():
    obj = R.choice(["pacote", "melão", "saco", "abóbora", "caixa"])
    pool = [1000, 500, 200, 100, 50, 20, 10]
    ws = sorted(R.sample(pool, R.randint(2, 3)), reverse=True)
    t = sum(ws)
    art = "a" if obj in ("abóbora", "caixa") else "o"
    return mcq(balanca(obj, ws) + "A balança está em equilíbrio. Qual é a massa d%s %s?" % (art, obj), U(t, "g"),
               [U(len(ws), "g"), U(t - ws[-1], "g"), U(t + ws[-1], "g"), U(max(ws), "g")],
               "Some os pesos do prato: %s = <b>%s</b>." % (" + ".join("%s g" % num(w) for w in ws), U(t, "g")))


def s4_copo():
    top, step = R.choice([(500, 50), (1000, 100), (400, 50), (600, 100)])
    lv = step * R.randint(1, top // step - 1)
    return mcq(copo(lv, top, step) + "Quanta água há no copo medidor?", U(lv, "mL"),
               [U(lv + step, "mL"), U(lv - step, "mL") if lv > step else U(lv + 2 * step, "mL"), U(lv // step, "mL"), U(lv, "L")],
               "Cada risquinho vale %d mL. A água chega a <b>%s</b>." % (step, U(lv, "mL")))


def s5_problema():
    p, _ = K.next()
    k = R.choice(["farinha", "suco", "mala", "garrafas", "bolo", "agua", "frutas"])
    if k == "farinha":
        t, u = R.choice([1000, 2000]), R.choice([250, 300, 400, 600, 750])
        return mcq("Um pacote tem %s de farinha. A mãe de %s usou %s num bolo. Quanto sobrou?" % (U(t // 1000, "kg"), p, U(u, "g")), U(t - u, "g"),
                   [U(t // 1000 * 1000 + u, "g"), U(t - u + 100, "g"), U(abs(t // 1000 - u), "g")],
                   "%s = %s; %s − %d = <b>%s</b>." % (U(t // 1000, "kg"), U(t, "g"), num(t), u, U(t - u, "g")))
    if k == "suco":
        c, n = R.choice([200, 250, 300]), R.randint(3, 6)
        return mcq("%s encheu %d copos de %d mL com suco. Quantos mililitros usou?" % (p, n, c), U(c * n, "mL"), [U(c + n, "mL"), U(c * (n + 1), "mL"), U(c * n * 10, "mL")],
                   "%d × %d = <b>%s</b>." % (n, c, U(c * n, "mL")))
    if k == "mala":
        a, b = R.randint(8, 18), R.randint(3, 9)
        return mcq("A mala de %s tem %d kg. A mochila tem %d kg. Quantos quilogramas as duas têm juntas?" % (p, a, b), U(a + b, "kg"), [U(a - b, "kg"), U(a + b + 1, "kg"), U(a * b, "kg")],
                   "%d + %d = <b>%s</b>." % (a, b, U(a + b, "kg")))
    if k == "garrafas":
        n = R.randint(2, 6)
        return mcq("Para uma festa compraram %d garrafas de 2 L de refrigerante. Quantos litros compraram?" % n, U(2 * n, "L"), [U(n + 2, "L"), U(n, "L"), U(2 * n * 1000, "L")],
                   "%d × 2 = <b>%s</b>." % (n, U(2 * n, "L")))
    if k == "bolo":
        a, b, c = R.choice([200, 300, 400]), R.choice([100, 150, 200]), R.choice([50, 100])
        return mcq("Uma receita usa %d g de farinha, %d g de açúcar e %d g de manteiga. Qual é a massa desses ingredientes juntos?" % (a, b, c), U(a + b + c, "g"),
                   [U(a + b, "g"), U(a + b + c + 100, "g"), U((a + b + c) // 10, "g")], "%d + %d + %d = <b>%s</b>." % (a, b, c, U(a + b + c, "g")))
    if k == "agua":
        t, g = R.choice([1000, 2000]), R.choice([150, 250, 300, 400])
        return mcq("Uma garrafa tinha %s de água. %s bebeu %d mL. Quantos mililitros sobraram?" % (U(t // 1000, "L"), p, g), U(t - g, "mL"),
                   [U(t // 1000 * 1000 + g, "mL"), U(t - g - 100, "mL"), U(g, "mL")], "%s = %s; %s − %d = <b>%s</b>." % (U(t // 1000, "L"), U(t, "mL"), num(t), g, U(t - g, "mL")))
    pk = R.randint(4, 9)
    pr = R.randint(3, 8)
    return mcq("Na feira, 1 kg de banana custa %s. Quanto custam %d kg?" % (reais(pr * 100), pk), reais(pr * pk * 100), [reais((pr + pk) * 100), reais(pr * (pk + 1) * 100), reais(pr * pk * 10)],
               "%d × %d = %d: <b>%s</b>." % (pk, pr, pr * pk, reais(pr * pk * 100)))


def main():
    FRM.R = random.Random(80917)
    seen = set()
    sets = [
        ("Unidades de massa e capacidade", mix(R, seen, [(s1_massa, 10), (s1_cap, 10)])),
        ("Quilograma, grama, litro e mililitro", mix(R, seen, [(s2_converter, 20)])),
        ("Comparar massas e capacidades", mix(R, seen, [(s3_comparar, 12), (s2_converter, 8)])),
        ("Balança e copo medidor", mix(R, seen, [(s4_balanca, 10), (s4_copo, 10)])),
        ("Problemas de massa e capacidade", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["A <b>massa</b> diz quanto um objeto pesa. Unidades: <b>quilograma</b> (kg), <b>grama</b> (g) e <b>miligrama</b> (mg). 1 kg = 1.000 g.",
         "A <b>capacidade</b> diz quanto cabe num recipiente. Unidades: <b>litro</b> (L) e <b>mililitro</b> (mL). 1 L = 1.000 mL.",
         "Meio quilo = 500 g e meio litro = 500 mL.",
         "Um objeto grande nem sempre é mais pesado: uma bola de isopor é leve. Para comparar, use a balança."],
        [("Quantos gramas há em 3 kg?", ["1 kg = 1.000 g", "3 × 1.000"], "3.000 g"),
         ("O que é mais pesado: 1 kg ou 800 g?", ["1 kg = 1.000 g", "1.000 g &gt; 800 g"], "1 kg")],
        [["Achar que 800 g é mais que 1 kg", "Compare na mesma unidade: 1 kg = 1.000 g."],
         ["Achar que o maior é sempre mais pesado", "Tamanho e massa são coisas diferentes."],
         ["Ler o copo medidor errado", "Veja quanto vale cada risquinho antes de ler."]],
        table(["Massa", "Capacidade"], [["1 kg = 1.000 g", "1 L = 1.000 mL"], ["meio quilo = 500 g", "meio litro = 500 mL"]]))
    faq = [("Por que ensinar miligrama no 3º ano?", "A BNCC cita o miligrama porque ele aparece em embalagens de remédios e alimentos. No 3º ano basta reconhecer que é uma unidade para massas muito pequenas."),
           ("Como praticar em casa?", "Leia os rótulos das embalagens (500 g, 1 kg, 350 mL, 2 L) e compare. Na cozinha, use um copo medidor para medir água ou farinha.")]
    make_unit(R, "massa-e-capacidade", "M", ["EF03MA20"],
              "Estimar e medir capacidade e massa, utilizando unidades de medida não padronizadas e padronizadas mais usuais (litro, mililitro, quilograma, grama e miligrama), reconhecendo-as em leitura de rótulos e embalagens, entre outros",
              "Massa e capacidade: quilograma, grama, litro e mililitro", "Massa e capacidade",
              "Atividades de matemática para o 3º ano sobre massa e capacidade: quilograma, grama e miligrama, litro e mililitro, balança, copo medidor, comparar e problemas. 100 exercícios com gabarito.",
              "1 kg = 1.000 g e 1 L = 1.000 mL.", "Grande não quer dizer pesado.",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
