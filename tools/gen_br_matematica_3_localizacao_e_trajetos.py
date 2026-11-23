# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Localização e trajetos (Geometria, EF03MA12)
  python3 tools/gen_br_matematica_3_localizacao_e_trajetos.py
Localizar objetos numa malha quadriculada (coluna e linha), descrever deslocamentos com passos e mudanças de direção,
seguir e escrever um código de setas, virar à direita e à esquerda, pontos de referência num croqui.
Erros: ler primeiro a linha e depois a coluna, contar a casa de partida, confundir direita e esquerda ao virar.
"""
import random
import gen_fr_maths_ce2_se_reperer_et_se_deplacer as FRP
from br_common import mcq, lesson, make_unit, mix, relabel, Kids

R = random.Random(80313)
FRP.R = random.Random(80913)
K = Kids(R)
GC, GR = FRP.COLS, FRP.ROWS
LET = FRP.LET
FIG = {"a estrela": "l’étoile", "o círculo": "le rond", "o triângulo": "le triangle", "o quadrado": "le carré", "o losango": "le losange", "o coração": "le cœur"}
AO = {"a estrela": "até a estrela", "o círculo": "até o círculo", "o triângulo": "até o triângulo", "o quadrado": "até o quadrado", "o losango": "até o losango", "o coração": "até o coração"}
DIRS = {"para a direita": (1, 0), "para a esquerda": (-1, 0), "para cima": (0, 1), "para baixo": (0, -1)}


def cell(c):
    return FRP.cell(c)


def malha(objs, start=None):
    s = FRP.grille({FIG[k]: v for k, v in objs.items()}, start=start)
    return relabel(s, "malha quadriculada: colunas de A a F, linhas de 1 a 5")


def place(n):
    cells = R.sample([(c, r) for c in range(GC) for r in range(GR)], n)
    kinds = R.sample(sorted(FIG), n)
    return dict(zip(kinds, cells))


def ok(c):
    return 0 <= c[0] < GC and 0 <= c[1] < GR


def near(cur):
    return [(cur[0] + dx, cur[1] + dy) for dx, dy in ((1, 0), (0, -1), (-1, 0), (0, 1), (1, 1), (-1, -1))]


def s1_onde():
    objs = place(R.randint(3, 5))
    k = R.choice(sorted(objs))
    c = objs[k]
    right = cell(c)
    w = ["%d%s" % (c[1] + 1, LET[c[0]]), "%s%d" % (LET[c[1]], c[0] + 1) if c[1] < GC and c[0] + 1 <= GR else None,
         "%s%d" % (LET[c[0]], GR - c[1]) if GR - c[1] != c[1] + 1 else None, "%s%d" % (LET[(c[0] + 1) % GC], c[1] + 1)]
    return mcq(malha(objs) + "Em que casa está %s?" % k, right, [x for x in w if x and x != right],
               "Leia primeiro a letra da coluna e depois o número da linha: %s está em <b>%s</b>." % (k, right))


def s1_oque():
    objs = place(4)
    k = R.choice(sorted(objs))
    c = objs[k]
    return mcq(malha(objs) + "O que há na casa %s?" % cell(c), k, [x for x in sorted(objs) if x != k] + ["nada"],
               "Coluna %s, linha %d: <b>%s</b>." % (LET[c[0]], c[1] + 1, k))


def s2_passos():
    st = (R.randint(0, GC - 1), R.randint(0, GR - 1))
    steps, cur = [], st
    for _ in range(R.randint(1, 2)):
        d = R.choice(sorted(DIRS))
        n = R.randint(1, 4)
        nx = (cur[0] + DIRS[d][0] * n, cur[1] + DIRS[d][1] * n)
        if not ok(nx):
            return None
        steps.append((n, d))
        cur = nx
    if cur == st:
        return None
    n0, d0 = steps[0]
    w1 = (st[0] + DIRS[d0][0] * (n0 + 1), st[1] + DIRS[d0][1] * (n0 + 1))
    opp = (st[0] - DIRS[d0][0] * n0, st[1] - DIRS[d0][1] * n0)
    for a, b in steps[1:]:
        w1 = (w1[0] + DIRS[b][0] * a, w1[1] + DIRS[b][1] * a)
        opp = (opp[0] + DIRS[b][0] * a, opp[1] + DIRS[b][1] * a)
    txt = " e depois ".join("%d %s %s" % (n, "casa" if n == 1 else "casas", d) for n, d in steps)
    return mcq(malha({}, start=st) + "O robô (ponto vermelho) está na casa %s. Ele anda %s. Em que casa ele chega?" % (cell(st), txt),
               cell(cur), [cell(x) for x in [w1, opp] + near(cur) if ok(x) and x != cur],
               "Não conte a casa de partida. O robô chega em <b>%s</b>." % cell(cur))


def s3_codigo():
    st = (R.randint(0, GC - 1), R.randint(0, GR - 1))
    code = FRP.rand_code()
    end = FRP.walk(st, code)
    if not end or end == st:
        return None
    flip = {"→": "←", "←": "→", "↑": "↑", "↓": "↓"}
    w1 = FRP.walk(st, [flip[a] for a in code])
    w2 = FRP.walk(st, code[:-1])
    w3 = FRP.walk(st, code + [code[-1]])
    return mcq(malha({}, start=st) + "O robô sai de %s e segue o código %s. Em que casa ele chega?" % (cell(st), " ".join(code)),
               cell(end), [cell(x) for x in [w1, w2, w3] + near(end) if x and ok(x) and x != end],
               "Cada seta é um passo de uma casa. O robô chega em <b>%s</b>." % cell(end))


def s3_escrever():
    st = (R.randint(0, GC - 1), R.randint(0, GR - 1))
    code = FRP.rand_code()
    end = FRP.walk(st, code)
    if not end or end == st:
        return None
    k = R.choice(sorted(FIG))
    dx, dy = end[0] - st[0], end[1] - st[1]
    good = ["→" if dx > 0 else "←"] * abs(dx) + ["↑" if dy > 0 else "↓"] * abs(dy)
    bad1 = ["←" if dx > 0 else "→"] * abs(dx) + ["↑" if dy > 0 else "↓"] * abs(dy)
    bad2 = ["→" if dx > 0 else "←"] * abs(dx) + ["↓" if dy > 0 else "↑"] * abs(dy)
    bad3 = ["→" if dx > 0 else "←"] * (abs(dx) + 1) + ["↑" if dy > 0 else "↓"] * abs(dy)
    if not dx or not dy:
        bad3 = good + [good[-1]]
    opts = [" ".join(x) for x in (good, bad1, bad2, bad3)]
    if len(set(opts)) < 4:
        return None
    cs = lambda n: "casa" if n == 1 else "casas"
    return mcq(malha({k: end}, start=st) + "Que código leva o robô de %s %s?" % (cell(st), AO[k]), opts[0], opts[1:],
               "São %d %s %s e %d %s %s: <b>%s</b>." % (abs(dx), cs(abs(dx)), "para a direita" if dx > 0 else "para a esquerda", abs(dy), cs(abs(dy)), "para cima" if dy > 0 else "para baixo", opts[0]))


POS = ["norte", "leste", "sul", "oeste"]
FRENTE = {"norte": "a escola", "leste": "a padaria", "sul": "o parque", "oeste": "a farmácia"}


def s4_virar():
    p, g = K.next()
    start = R.choice(POS)
    turns = [R.choice(["direita", "esquerda"]) for _ in range(R.randint(1, 2))]
    i = POS.index(start)
    for t in turns:
        i = (i + (1 if t == "direita" else -1)) % 4
    end = POS[i]
    j = POS.index(start)
    for t in turns:
        j = (j + (-1 if t == "direita" else 1)) % 4
    wrong = POS[j]
    txt = " e depois ".join("vira à %s" % t for t in turns)
    return mcq("Numa praça, a escola fica ao norte, a padaria a leste, o parque ao sul e a farmácia a oeste. %s está de frente para %s e %s. Para onde %s fica de frente agora?" % (
                   p, FRENTE[start], txt, "ela" if g == "ela" else "ele"),
               FRENTE[end], [FRENTE[x] for x in POS if x != end],
               "Virar à direita é girar como os ponteiros do relógio (norte → leste → sul → oeste). %s fica de frente para <b>%s</b>%s." % (
                   p, FRENTE[end], "" if wrong == end else " (quem confunde direita e esquerda responde %s)" % FRENTE[wrong]))


def s4_lado():
    p, g = K.next()
    k = R.choice(["mao", "frente", "costas", "meia"])
    if k == "mao":
        return mcq("%s está de costas para você e levanta a mão direita. De que lado do seu corpo fica a mão que %s levantou?" % (p, "ela" if g == "ela" else "ele"),
                   "do meu lado direito", ["do meu lado esquerdo", "na minha frente", "atrás de mim"],
                   "Quando a pessoa está de costas, os lados dela e os seus são os mesmos: <b>do meu lado direito</b>.")
    if k == "frente":
        return mcq("%s está de frente para você e levanta a mão direita. De que lado ela aparece para você?" % p,
                   "do meu lado esquerdo", ["do meu lado direito", "em cima", "atrás"],
                   "Quem está de frente tem os lados trocados em relação aos seus: aparece <b>do meu lado esquerdo</b>.")
    if k == "costas":
        return mcq("Você está olhando para o norte e dá meia-volta. Para onde fica olhando?", "para o sul", ["para o norte", "para o leste", "para o oeste"],
                   "Meia-volta é girar metade de uma volta: do norte vai para <b>o sul</b>.")
    return mcq("Você está olhando para o leste e dá um quarto de volta para a esquerda. Para onde fica olhando?", "para o norte", ["para o sul", "para o oeste", "para o leste"],
               "Um quarto de volta para a esquerda: do leste vai para <b>o norte</b>.")


MAPA = [("A padaria fica entre o banco e a farmácia. A farmácia fica na esquina. O que fica ao lado da padaria, mas não na esquina?", "o banco", ["a farmácia", "a escola", "o mercado"]),
        ("Na rua de Davi, as casas são numeradas: 10, 12, 14, 16. Ele mora na casa entre a 12 e a 16. Qual é o número da casa?", "14", ["12", "16", "13"]),
        ("Saindo de casa, Laura anda 2 quarteirões para a frente e vira à direita. A escola fica logo depois. Quantas vezes ela virou?", "1 vez", ["2 vezes", "nenhuma vez", "3 vezes"]),
        ("No croqui da sala, a mesa da professora fica na frente, perto do quadro. A porta fica do lado direito de quem olha para o quadro. Onde fica a porta para quem está na mesa olhando para os alunos?", "do lado esquerdo", ["do lado direito", "atrás do quadro", "no meio da sala"]),
        ("Gael mora no 3º andar. Sua avó mora 2 andares acima. Em que andar mora a avó?", "no 5º andar", ["no 1º andar", "no 2º andar", "no 6º andar"]),
        ("Na fila da cantina, Alice é a 4ª. Há 3 crianças depois dela. Quantas crianças há na fila?", "7", ["6", "4", "8"]),
        ("O cinema fica à direita do teatro e o teatro fica à direita da biblioteca. Qual prédio fica no meio?", "o teatro", ["o cinema", "a biblioteca", "não dá para saber"]),
        ("Pedro sobe 4 degraus, desce 2 e sobe mais 3. Quantos degraus acima do ponto de partida ele está?", "5", ["9", "3", "1"])]


def s5_croqui():
    q, a, w = R.choice(MAPA)
    return mcq(q, a, w, "Desenhe o caminho ou a situação e siga as informações uma de cada vez: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Localizar na malha quadriculada", mix(R, seen, [(s1_onde, 12), (s1_oque, 8)])),
        ("Andar casas na malha", mix(R, seen, [(s2_passos, 20)])),
        ("Códigos de setas", mix(R, seen, [(s3_codigo, 10), (s3_escrever, 10)])),
        ("Virar à direita e à esquerda", mix(R, seen, [(s4_virar, 16), (s4_lado, 4)])),
        ("Croquis e trajetos", mix(R, seen, [(s5_croqui, 8), (s2_passos, 6), (s3_codigo, 6)])),
    ]
    body = lesson(
        ["Numa <b>malha quadriculada</b>, cada casa tem um nome: primeiro a letra da coluna, depois o número da linha (B3 = coluna B, linha 3).",
         "Para descrever um trajeto, diga quantas casas e para que lado: «3 casas para a direita e 2 para cima». Não conte a casa de onde sai.",
         "Virar à <b>direita</b> é girar no sentido dos ponteiros do relógio; virar à <b>esquerda</b>, no sentido contrário.",
         "Quem está de frente para você tem a direita do seu lado esquerdo."],
        [("Robô em A1 com o código → → ↑", ["→ → : C1", "↑ : C2"], "C2"),
         ("De frente para o norte, virar à direita", ["norte → leste"], "fica de frente para o leste")],
        [["Ler 3B em vez de B3", "Primeiro a coluna (letra), depois a linha (número)."],
         ["Contar a casa de partida", "Cada passo leva para a casa seguinte; a de partida não conta."],
         ["Trocar direita e esquerda ao virar", "Imagine-se no lugar da pessoa e gire o corpo."]])
    faq = [("O que a BNCC pede de localização no 3º ano?", "Descrever e representar, por meio de esboços de trajetos ou de croquis e maquetes, a movimentação de pessoas ou objetos no espaço, incluindo mudanças de direção e sentido, com base em pontos de referência."),
           ("Como praticar em casa?", "Desenhe o caminho de casa até a escola, marcando onde se vira à direita ou à esquerda, ou brinque de dar comandos de setas para alguém chegar a um objeto escondido.")]
    make_unit(R, "localizacao-e-trajetos", "G", ["EF03MA12"],
              "Descrever e representar, por meio de esboços de trajetos ou utilizando croquis e maquetes, a movimentação de pessoas ou de objetos no espaço, incluindo mudanças de direção e sentido, com base em diferentes pontos de referência",
              "Localização e trajetos na malha quadriculada", "Localização e trajetos",
              "Atividades de matemática para o 3º ano sobre localização e trajetos: malha quadriculada, colunas e linhas, códigos de setas, virar à direita e à esquerda, croquis. 100 exercícios com gabarito.",
              "Primeiro a coluna, depois a linha: B3.", "Direita: sentido dos ponteiros do relógio.",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
