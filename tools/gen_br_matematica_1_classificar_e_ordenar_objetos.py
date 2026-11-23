# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Classificar e ordenar objetos (Álgebra, EF01MA09)
  python3 tools/gen_br_matematica_1_classificar_e_ordenar_objetos.py
Separar figuras por cor, forma ou tamanho; descobrir o atributo usado na separação; achar a figura que não combina;
ordenar do menor para o maior (torres, lápis, números de figuras).
Erros: olhar só a cor quando a regra é a forma, ordenar ao contrário, contar duas vezes a mesma figura.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, text, KINDS, COISAS
from ws_common import svg_wrap, GREEN
from br_1 import pic, torres, lapis
from br_2 import FORMAS, CORES

R = random.Random(80109)
K4 = ["circle", "square", "triangle", "rectangle"]
COR4 = sorted(CORES)
TAM = {16: "pequeno", 28: "grande"}


def nome_fig(k, c, r=None):
    s = "%s %s" % (FORMAS[k][0], CORES[c][0])
    return s + (" %s" % TAM[r] if r else "")


def letras(items):
    """items = [(forma, cor, raio)] com A, B, C, D embaixo"""
    sp = 92
    s = []
    for i, (k, c, r) in enumerate(items):
        cx = 8 + sp / 2 + i * sp
        s.append(k_pics.shape(k, cx, 44, r, c))
        s.append(text(cx, 104, "ABCD"[i], 18, col=GREEN))
    return pic(svg_wrap(16 + len(items) * sp, 114, "".join(s), "x"), "figuras A, B, C e D: " + "; ".join(nome_fig(k, c, r if any(x[2] != items[0][2] for x in items) else None) for k, c, r in items))


def s1_diferente():
    attr = R.choice(["cor", "forma", "tamanho"])
    k, c, r = R.choice(K4), R.choice(COR4), 24
    if attr == "cor":
        c2 = R.choice([x for x in COR4 if x != c])
        items = [(k, c, r)] * 3 + [(k, c2, r)]
        why = "as outras são %s" % {"red": "vermelhas", "blue": "azuis", "yellow": "amarelas", "green": "verdes"}[c]
    elif attr == "forma":
        k2 = R.choice([x for x in K4 if x != k and not ({x, k} == {"square", "rectangle"})])
        items = [(k, c, r)] * 3 + [(k2, c, r)]
        why = "as outras são %s" % FORMAS[k][1]
    else:
        items = [(k, c, 28)] * 3 + [(k, c, 16)] if R.random() < 0.5 else [(k, c, 16)] * 3 + [(k, c, 28)]
        why = "as outras são de outro tamanho"
    odd = items[3]
    R.shuffle(items)
    i = items.index(odd)
    return mcq(letras(items) + "Qual figura não combina com as outras?", "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]], "A figura %s é diferente: %s. Resposta: <b>%s</b>." % ("ABCD"[i], why, "ABCD"[i]))


def s2_quantos_grupos():
    attr = R.choice(["cor", "forma"])
    ncor = R.randint(2, 4)
    cores = R.sample(COR4, ncor)
    formas = R.sample(["circle", "triangle", "square"], R.randint(2, 3))
    items = [(R.choice(formas), R.choice(cores)) for _ in range(R.randint(7, 11))]
    usadas = len({x[1] for x in items}) if attr == "cor" else len({x[0] for x in items})
    p = pic(k_pics.shapes_mix_svg(items, R.randint(1, 99999)), "figuras de várias formas e cores")
    return mcq(p + "Separando as figuras por %s, quantos grupos se formam?" % attr, str(usadas), [str(x) for x in (1, 2, 3, 4, 5) if x != usadas][:3] + [str(len(items))],
               "Há %d %s diferentes: <b>%d grupos</b>." % (usadas, "cores" if attr == "cor" else "formas", usadas))


def s2_contar_grupo():
    items = [(R.choice(["circle", "triangle", "square"]), R.choice(COR4)) for _ in range(R.randint(8, 12))]
    if R.random() < 0.5:
        c = R.choice([x[1] for x in items])
        n = sum(1 for x in items if x[1] == c)
        q = "Quantas figuras %s há?" % {"red": "vermelhas", "blue": "azuis", "yellow": "amarelas", "green": "verdes"}[c]
        oth = sum(1 for x in items if x[0] == items[0][0])
    else:
        k = R.choice([x[0] for x in items])
        n = sum(1 for x in items if x[0] == k)
        q = "Quantos %s há (de qualquer cor)?" % FORMAS[k][1]
        oth = len(items) - n
    p = pic(k_pics.shapes_mix_svg(items, R.randint(1, 99999)), "figuras de várias formas e cores")
    return mcq(p + q, str(n), [str(n + 1), str(n - 1) if n > 1 else str(n + 2), str(len(items)), str(oth)], "Conte só as figuras do grupo pedido: <b>%d</b>." % n)


REGRA = [("Num grupo ficaram só bolas vermelhas e no outro só bolas azuis. A separação foi por…", "cor", ["forma", "tamanho", "número"]),
         ("Num grupo ficaram os triângulos e no outro os círculos, de várias cores. A separação foi por…", "forma", ["cor", "tamanho", "nome"]),
         ("Num grupo ficaram as caixas grandes e no outro as pequenas. A separação foi por…", "tamanho", ["cor", "forma", "peso"]),
         ("Para guardar os brinquedos, Lia pôs os carrinhos numa caixa e as bonecas em outra. Ela separou por…", "tipo de brinquedo", ["cor", "tamanho", "número"]),
         ("Na fruteira, as bananas ficaram juntas e as maçãs juntas. A separação foi por…", "tipo de fruta", ["cor", "tamanho", "peso"]),
         ("Os lápis foram separados: os compridos num pote e os curtos em outro. A separação foi por…", "tamanho", ["cor", "forma", "tipo"]),
         ("Na estante, os livros azuis ficaram juntos e os vermelhos juntos. A separação foi por…", "cor", ["tamanho", "forma", "título"]),
         ("Na turma, as crianças de tênis ficaram de um lado e as de sandália do outro. A separação foi por…", "tipo de calçado", ["altura", "idade", "cor do cabelo"])]


def s3_regra():
    q, a, w = R.choice(REGRA)
    return mcq(q, a, w, "Veja o que é igual dentro de cada grupo. Resposta: <b>%s</b>." % a)


def s4_torres():
    hs = R.sample(range(1, 8), 4)
    k = R.choice(["alta", "baixa", "ordem"])
    if k == "alta":
        i = hs.index(max(hs))
        return mcq(torres(hs) + "Qual torre é a mais alta?", "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]], "A torre %s tem %d cubinhos: <b>%s</b>." % ("ABCD"[i], max(hs), "ABCD"[i]))
    if k == "baixa":
        i = hs.index(min(hs))
        return mcq(torres(hs) + "Qual torre é a mais baixa?", "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]], "A torre %s tem %d: <b>%s</b>." % ("ABCD"[i], min(hs), "ABCD"[i]))
    order = sorted(range(4), key=lambda i: hs[i])
    ok = ", ".join("ABCD"[i] for i in order)
    rev = ", ".join("ABCD"[i] for i in order[::-1])
    w2 = order[:]
    w2[0], w2[1] = w2[1], w2[0]
    return mcq(torres(hs) + "Coloque as torres em ordem, da mais baixa para a mais alta.", ok, [rev, ", ".join("ABCD"[i] for i in w2), "A, B, C, D" if ok != "A, B, C, D" else "D, C, B, A"],
               "Alturas: %s. Ordem: <b>%s</b>." % (", ".join("%s = %d" % ("ABCD"[i], hs[i]) for i in range(4)), ok))


def s4_lapis():
    ls = R.sample(range(2, 8), 4)
    k = R.choice(["longo", "curto", "ordem"])
    if k in ("longo", "curto"):
        i = ls.index(max(ls) if k == "longo" else min(ls))
        return mcq(lapis(ls) + "Qual lápis é o mais %s?" % ("comprido" if k == "longo" else "curto"), "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]],
                   "Os lápis começam no mesmo lugar; veja onde terminam: <b>%s</b>." % "ABCD"[i])
    order = sorted(range(4), key=lambda i: -ls[i])
    ok = ", ".join("ABCD"[i] for i in order)
    return mcq(lapis(ls) + "Coloque os lápis em ordem, do mais comprido para o mais curto.", ok, [", ".join("ABCD"[i] for i in order[::-1]), ", ".join("ABCD"[i] for i in order[1:] + order[:1]), "A, B, C, D" if ok != "A, B, C, D" else "B, A, C, D"],
               "Do mais comprido ao mais curto: <b>%s</b>." % ok)


def main():
    seen = set()
    sets = [
        ("Qual não combina?", mix(R, seen, [(s1_diferente, 20)])),
        ("Separar por cor e por forma", mix(R, seen, [(s2_quantos_grupos, 10), (s2_contar_grupo, 10)])),
        ("Qual foi a regra?", mix(R, seen, [(s3_regra, 8), (s1_diferente, 6), (s2_contar_grupo, 6)])),
        ("Do menor para o maior", mix(R, seen, [(s4_torres, 20)])),
        ("Ordenar comprimentos", mix(R, seen, [(s4_lapis, 20)])),
    ]
    body = lesson(
        ["<b>Classificar</b> é separar em grupos pelo que as coisas têm de igual: a <b>cor</b>, a <b>forma</b> ou o <b>tamanho</b>.",
         "Para descobrir a regra de um grupo, veja o que é igual em todas as figuras dele.",
         "<b>Ordenar</b> é colocar em fila: do menor para o maior ou do maior para o menor.",
         "Para comparar comprimentos, coloque as coisas lado a lado, começando no mesmo lugar."],
        [("Bola vermelha, carro vermelho, dado azul", ["dois são vermelhos"], "o dado não combina pela cor"),
         ("Torres com 2, 5 e 3 cubinhos", ["menor primeiro"], "2, 3, 5")],
        [["Olhar só a cor quando a regra é a forma", "Veja o que todas do grupo têm igual."],
         ["Ordenar ao contrário", "Leia se é do menor para o maior ou do maior para o menor."],
         ["Contar a mesma figura duas vezes", "Marque cada figura ao contar."]],
        letras([("circle", "red", 24), ("triangle", "red", 24), ("square", "blue", 24), ("circle", "red", 24)]))
    faq = [("O que é classificar no 1º ano?", "É separar objetos em grupos por características como cor, forma e tamanho. A BNCC pede organizar e ordenar objetos familiares ou figuras por meio desses atributos."),
           ("Como praticar em casa?", "Peça para a criança arrumar os brinquedos por tipo, as meias por cor ou os lápis do menor para o maior, e explicar a regra que usou.")]
    make_unit(R, "classificar-e-ordenar-objetos", "A", ["EF01MA09"],
              "Organizar e ordenar objetos familiares ou representações por figuras, por meio de atributos, tais como cor, forma e medida",
              "Classificar e ordenar objetos por cor, forma e tamanho", "Classificar e ordenar",
              "Atividades de matemática para o 1º ano sobre classificar e ordenar: separar por cor, forma e tamanho, achar a figura que não combina, ordenar do menor para o maior. 100 exercícios com gabarito.",
              "Classificar é separar pelo que é igual.", "Ordenar é pôr em fila do menor para o maior.",
              body, faq, sets, 9, grade="1-ano")


if __name__ == "__main__":
    main()
