# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Massa e capacidade (Grandezas e medidas, EF02MA17)
  python3 tools/gen_br_matematica_2_massa_e_capacidade.py
Mais pesado e mais leve na balança; quilograma e grama; litro e mililitro; medir com copos e xícaras (unidades não padronizadas);
qual recipiente tem mais água; estimar; balança em equilíbrio, copo medidor e problemas. Usa geradores do 3º ano com outro sorteio.
Erros: achar que o maior é sempre o mais pesado, comparar recipientes só pela altura da água, misturar kg e g.
"""
import random
import re
import k_pics
import f_common
from br_common import mcq, lesson, make_unit, mix, use, lim, relabel, fig, COISAS, KINDS

R = random.Random(80216)


def nomg(it):
    t = it["q"] + it["e"] + "".join(it["c"])
    return not re.search(r"\bmg\b|miligrama", t)


q_massa, q_cap, q_comp, q_bal, q_copo, q_prob = use("gen_br_matematica_3_massa_e_capacidade", 80910, "s1_massa", "s1_cap", "s3_comparar", "s4_balanca", "s4_copo", "s5_problema", preds=(lim(999, 0), nomg))


def art(k):
    return ("a " if COISAS[k][2] == "f" else "o ") + COISAS[k][0]


def s1_balanca():
    a, b = R.sample(KINDS, 2)
    tilt = R.choice(["left", "right"])
    na, nb = R.randint(1, 3), R.randint(1, 3)
    pic = fig(relabel(k_pics.balance_svg((a, na), (b, nb), tilt), "balança: à esquerda %d %s, à direita %d %s; o lado %s está mais baixo" % (na, COISAS[a][1] if na > 1 else COISAS[a][0], nb, COISAS[b][1] if nb > 1 else COISAS[b][0], "esquerdo" if tilt == "left" else "direito")))
    heavy = "o lado esquerdo" if tilt == "left" else "o lado direito"
    light = "o lado direito" if tilt == "left" else "o lado esquerdo"
    if R.random() < 0.5:
        return mcq(pic + "Na balança, qual lado é mais pesado?", heavy, [light, "os dois pesam o mesmo", "o lado mais alto"],
                   "O lado mais pesado desce. Resposta: <b>%s</b>." % heavy)
    return mcq(pic + "Na balança, qual lado é mais leve?", light, [heavy, "os dois pesam o mesmo", "o lado mais baixo"],
               "O lado mais leve sobe. Resposta: <b>%s</b>." % light)


def s1_equilibrio():
    a = R.choice(KINDS)
    b = R.choice([x for x in KINDS if x != a])
    na, nb = R.randint(1, 2), R.randint(2, 4)
    if na == nb:
        return None
    pic = fig(relabel(k_pics.balance_svg((a, na), (b, nb), "equal"), "balança equilibrada: %d %s de um lado e %d %s do outro" % (na, COISAS[a][1] if na > 1 else COISAS[a][0], nb, COISAS[b][1])))
    ans = "os dois lados pesam o mesmo"
    return mcq(pic + "A balança está reta. O que isso quer dizer?", ans, ["o lado esquerdo é mais pesado", "o lado direito é mais pesado", "a balança quebrou"],
               "Quando a balança fica reta (em equilíbrio), <b>os dois lados pesam o mesmo</b>.")


def s2_copos():
    rec, un, g = R.choice([("jarra", "copos", "m"), ("garrafa", "copos", "m"), ("balde", "jarras", "f"), ("panela", "xícaras", "f"), ("chaleira", "xícaras", "f"), ("leiteira", "copos", "m")])
    art_ = "um" if rec == "balde" else "uma"
    a, b = R.randint(3, 9), R.randint(3, 9)
    if a == b:
        return None
    if R.random() < 0.6:
        return mcq("A água de %s %s A enche %d %s. A de %s %s B enche %d %s iguais. Qual cabe mais?" % (art_, rec, a, un, art_, rec, b, un), "A" if a > b else "B",
                   ["B" if a > b else "A", "as duas cabem o mesmo", "não dá para saber"], "Quem enche mais %s cabe mais: %d %s %d. Resposta: <b>%s</b>." % (un, a, "&gt;" if a > b else "&lt;", b, "A" if a > b else "B"))
    n = R.randint(2, 3)
    num_w = ("Dois" if rec == "balde" else "Duas") if n == 2 else "Três"
    return mcq("%s %s enche %d %s. %s %ss iguais enchem quant%ss %s?" % (art_.capitalize(), rec, a, un, num_w, rec, "o" if g == "m" else "a", un),
               str(n * a), [str(a), str(a + n), str(n * a + 1)], "%s = <b>%d</b>." % (" + ".join([str(a)] * n), n * a))


def s2_recipientes():
    w = R.choice([30, 40])
    k = R.choice(["mesma_altura", "mesmo_pote", "cheio"])
    if k == "mesmo_pote":
        levs = R.sample([0.2, 0.35, 0.5, 0.65, 0.8, 0.95], 4)
        items = [(w, 90, l) for l in levs]
        i = levs.index(max(levs))
        q = "Os quatro potes são iguais. Qual tem mais água?"
        why = "Nos potes iguais, mais alto é mais água."
    elif k == "cheio":
        levs = R.sample([0.25, 0.4, 0.55, 0.7, 0.85], 4)
        items = [(w, 90, l) for l in levs]
        i = levs.index(min(levs))
        q = "Os quatro potes são iguais. Qual tem menos água?"
        why = "Nos potes iguais, mais baixo é menos água."
    else:
        ws = R.sample([24, 36, 50, 66], 4)
        items = [(x, 80, 0.6) for x in ws]
        i = ws.index(max(ws))
        q = "A água está na mesma altura nos quatro potes. Qual tem mais água?"
        why = "Com a mesma altura, o pote mais largo tem mais água."
    pic = fig(relabel(f_common.glasses_svg(items), "potes A, B, C e D com água"))
    return mcq(pic + q, "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]], "%s Resposta: <b>%s</b>." % (why, "ABCD"[i]))


PESO = [("O que é mais pesado: uma melancia ou uma uva?", "a melancia", ["a uva", "pesam o mesmo", "não dá para saber"]),
        ("Uma caixa grande cheia de pena ou uma caixa pequena cheia de pedras: qual costuma ser mais pesada?", "a caixa pequena com pedras", ["a caixa grande com penas", "pesam sempre o mesmo", "a maior, sempre"]),
        ("Para comprar arroz, usamos que unidade?", "quilograma (kg)", ["litro (L)", "metro (m)", "centímetro (cm)"]),
        ("Para comprar leite, usamos que unidade?", "litro (L)", ["quilograma (kg)", "metro (m)", "grama (g)"]),
        ("Um pacote de biscoito costuma ter cerca de…", "200 gramas", ["200 quilogramas", "200 litros", "2 gramas"]),
        ("Uma garrafa de água pequena tem cerca de…", "500 mililitros", ["500 litros", "5 mililitros", "500 quilogramas"]),
        ("Um copo de suco tem cerca de…", "200 mililitros", ["200 litros", "2 mililitros", "20 litros"]),
        ("Um saco de feijão de mercado costuma ter…", "1 quilograma", ["1 grama", "1 litro", "100 quilogramas"]),
        ("Uma colher de chá de açúcar tem cerca de…", "5 gramas", ["5 quilogramas", "500 gramas", "5 litros"]),
        ("Um balde de limpeza cheio tem cerca de…", "10 litros", ["10 mililitros", "100 litros", "1 mililitro"]),
        ("Uma criança do 2º ano pesa cerca de…", "25 quilogramas", ["25 gramas", "250 quilogramas", "2 quilogramas"]),
        ("1 kg de algodão e 1 kg de ferro…", "pesam o mesmo", ["o ferro pesa mais", "o algodão pesa mais", "não dá para saber"])]


def s3_estimar():
    q, a, w = R.choice(PESO)
    return mcq(q, a, w, "Pense em objetos de verdade. Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Mais pesado, mais leve", mix(R, seen, [(s1_balanca, 12), (s1_equilibrio, 4), (q_comp, 4)])),
        ("Quilograma e grama", mix(R, seen, [(q_massa, 10), (q_bal, 10)])),
        ("Cabe mais, cabe menos", mix(R, seen, [(s2_recipientes, 10), (s2_copos, 10)])),
        ("Litro e mililitro", mix(R, seen, [(q_cap, 8), (q_copo, 12)])),
        ("Estimar e resolver problemas", mix(R, seen, [(s3_estimar, 10), (q_prob, 10)])),
    ]
    body = lesson(
        ["A <b>massa</b> diz se algo é pesado ou leve. Medimos em <b>quilogramas (kg)</b> e <b>gramas (g)</b>.",
         "Na balança de pratos, o lado mais pesado <b>desce</b>. Se ela fica reta, os dois lados pesam o mesmo.",
         "A <b>capacidade</b> diz quanto cabe num recipiente. Medimos em <b>litros (L)</b> e <b>mililitros (mL)</b>.",
         "Podemos medir com copos ou xícaras: quem enche mais copos cabe mais."],
        [("A jarra enche 6 copos e a garrafa enche 4 copos iguais", ["6 &gt; 4"], "a jarra cabe mais"),
         ("Melancia ou laranja: qual pesa mais?", ["a melancia desce a balança"], "a melancia")],
        [["Achar que o maior é sempre o mais pesado", "Uma caixa grande de penas pode ser leve. Use a balança."],
         ["Comparar só pela altura da água", "Veja também a largura do recipiente."],
         ["Usar litro para pesar", "Litro mede o que cabe; quilograma mede o peso."]],
        fig(relabel(k_pics.balance_svg(("apple", 3), ("ball", 1), "left"), "balança: 3 maçãs de um lado mais baixo e 1 bola do outro")))
    faq = [("O que o 2º ano aprende sobre massa e capacidade?", "A BNCC pede estimar, medir e comparar capacidade e massa com estratégias pessoais e com unidades não padronizadas ou padronizadas: litro, mililitro, grama e quilograma."),
           ("Como praticar em casa?", "Leia os rótulos das embalagens (1 kg, 500 g, 1 L, 350 mL). Encha uma garrafa com copos e conte quantos couberam.")]
    make_unit(R, "massa-e-capacidade", "M", ["EF02MA17"],
              "Estimar, medir e comparar capacidade e massa, utilizando estratégias pessoais e unidades de medida não padronizadas ou padronizadas (litro, mililitro, grama e quilograma)",
              "Massa e capacidade: quilograma, grama, litro e mililitro", "Massa e capacidade",
              "Atividades de matemática para o 2º ano sobre massa e capacidade: mais pesado e mais leve, balança, quilograma e grama, litro e mililitro, cabe mais e cabe menos. 100 exercícios com gabarito.",
              "O lado mais pesado da balança desce.", "Massa: kg e g. Capacidade: L e mL.",
              body, faq, sets, 16, grade="2-ano")


if __name__ == "__main__":
    main()
