# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Localização e movimentação (Geometria, EF04MA16)
  python3 tools/gen_br_matematica_4_localizacao_e_movimentacao.py
Localizar e descrever deslocamentos na malha quadriculada, em croquis e mapas; direita e esquerda, mudanças de direção e sentido;
ruas paralelas, perpendiculares e transversais num mapa. Usa geradores do 3º ano (malha, códigos, virar) com outro sorteio.
Erros: ler a linha antes da coluna, contar a casa de partida, confundir paralelas (nunca se cruzam) com perpendiculares (cruzam em ângulo reto).
"""
import random
from br_common import mcq, lesson, make_unit, mix, wrap, line, text, INK, use

R = random.Random(80412)
M3 = "gen_br_matematica_3_localizacao_e_trajetos"
s_onde, s_oque, s_passos, s_codigo, s_escrever, s_virar, s_lado, s_croqui = use(M3, 80953, "s1_onde", "s1_oque", "s2_passos", "s3_codigo", "s3_escrever", "s4_virar", "s4_lado", "s5_croqui")
NOMES = ["Rua das Flores", "Rua do Sol", "Rua da Paz", "Rua das Palmeiras", "Rua do Rio", "Rua da Escola", "Rua dos Ipês", "Rua da Lua", "Rua do Comércio", "Rua das Acácias"]


def mapa():
    """2 ruas horizontais, 2 verticais e 1 avenida inclinada; letras na ponta de cada rua e legenda embaixo"""
    ns = R.sample(NOMES, 4) + ["Avenida Central"]
    hy = [70, 170]
    vx = [130, 290]
    s = ["<rect x='0' y='0' width='400' height='240' fill='#f3f6ee'/>"]
    for y in hy:
        s.append("<rect x='0' y='%d' width='400' height='18' fill='#d9d9d9'/>" % (y - 9))
    for x in vx:
        s.append("<rect x='%d' y='0' width='18' height='240' fill='#d9d9d9'/>" % (x - 9))
    s.append("<polygon points='0,230 22,240 400,40 400,20' fill='#c7c7c7'/>")
    pos = [(16, hy[0]), (16, hy[1]), (vx[0], 226), (vx[1], 226), (380, 44)]
    for (x, y), L in zip(pos, "ABCDE"):
        s.append("<circle cx='%d' cy='%d' r='11' fill='#fff' stroke='%s' stroke-width='1.6'/>" % (x, y, INK))
        s.append(text(x, y + 5, L, 13))
    for i, (L, n) in enumerate(zip("ABCDE", ns)):
        s.append(text(10 + (i % 2) * 200, 262 + (i // 2) * 18, "%s = %s" % (L, n), 12, anchor="start"))
    return wrap(400, 310, "".join(s), "mapa com ruas paralelas, perpendiculares e uma avenida inclinada; legenda: " + "; ".join("%s = %s" % (L, n) for L, n in zip("ABCDE", ns)), lg=True), ns


def s5_ruas():
    pic, ns = mapa()
    pairs = [((0, 1), "paralelas"), ((2, 3), "paralelas"), ((0, 2), "perpendiculares"), ((0, 3), "perpendiculares"), ((1, 2), "perpendiculares"), ((1, 3), "perpendiculares"),
             ((4, 0), "transversais (se cruzam sem formar ângulo reto)"), ((4, 2), "transversais (se cruzam sem formar ângulo reto)")]
    (a, b), ans = R.choice(pairs)
    opts = ["paralelas", "perpendiculares", "transversais (se cruzam sem formar ângulo reto)", "a mesma rua"]
    return mcq(pic + "No mapa, a %s (%s) e a %s (%s) são…" % (ns[a], "ABCDE"[a], ns[b], "ABCDE"[b]), ans, [o for o in opts if o != ans],
               "Paralelas nunca se cruzam; perpendiculares se cruzam formando ângulo reto; a avenida inclinada cruza as ruas sem ângulo reto. Resposta: <b>%s</b>." % ans)


def s5_conceito():
    q, a, w = R.choice([("Duas ruas que nunca se cruzam, por mais que sejam prolongadas, são…", "paralelas", ["perpendiculares", "transversais", "curvas"]),
                        ("Duas ruas que se cruzam formando um ângulo reto (como o canto de uma folha) são…", "perpendiculares", ["paralelas", "iguais", "curvas"]),
                        ("Os trilhos de um trem dão a ideia de linhas…", "paralelas", ["perpendiculares", "que se cruzam", "curvas"]),
                        ("As linhas de um caderno são…", "paralelas", ["perpendiculares", "que se cruzam no meio", "inclinadas"]),
                        ("Os lados vizinhos de uma folha de papel são…", "perpendiculares", ["paralelos", "curvos", "inclinados"]),
                        ("O lugar onde duas ruas se cruzam se chama…", "cruzamento (intersecção)", ["paralela", "calçada", "quarteirão"]),
                        ("Uma rua que corta duas ruas paralelas é chamada de…", "transversal", ["paralela", "circular", "vizinha"]),
                        ("Para ir da escola à praça, Lia anda 2 quarteirões, vira à direita e anda mais 1. Ela mudou de…", "direção", ["cor", "tamanho", "nome"]),
                        ("Ir para o norte e depois voltar para o sul é mudar de…", "sentido (na mesma direção)", ["rua paralela", "ângulo reto", "quarteirão"]),
                        ("Uma planta baixa mostra uma casa vista…", "de cima", ["de lado", "de frente", "de baixo"])])
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Localizar na malha quadriculada", mix(R, seen, [(s_onde, 12), (s_oque, 8)])),
        ("Deslocamentos na malha", mix(R, seen, [(s_passos, 12), (s_codigo, 8)])),
        ("Direita, esquerda e mudança de direção", mix(R, seen, [(s_virar, 14), (s_lado, 6)])),
        ("Paralelas, perpendiculares e transversais", mix(R, seen, [(s5_ruas, 12), (s5_conceito, 8)])),
        ("Croquis e trajetos", mix(R, seen, [(s_croqui, 8), (s_escrever, 12)])),
    ]
    pic, _ = mapa()
    body = lesson(
        ["Numa <b>malha quadriculada</b>, cada casa tem um nome: a letra da coluna e o número da linha (B3).",
         "Para descrever um trajeto, diga quantas casas (ou quarteirões) e para que lado, e quando virar à direita ou à esquerda.",
         "Ruas <b>paralelas</b> nunca se cruzam. Ruas <b>perpendiculares</b> se cruzam formando ângulo reto. Uma rua <b>transversal</b> corta outras ruas.",
         "Mudar de <b>direção</b> é virar (de norte–sul para leste–oeste); mudar de <b>sentido</b> é voltar pelo mesmo caminho."],
        [("Robô em A1 com o código → → ↑", ["→ → : C1", "↑ : C2"], "C2"),
         ("Duas ruas formam um canto como o de uma folha. Como elas são?", ["cruzam em ângulo reto"], "perpendiculares")],
        [["Ler 3B em vez de B3", "Primeiro a coluna (letra), depois a linha (número)."],
         ["Contar a casa de onde sai", "Comece a contar na casa seguinte."],
         ["Chamar de paralelas ruas que se cruzam", "Paralelas nunca se encontram."]],
        pic)
    faq = [("O que o 4º ano aprende sobre localização?", "A BNCC pede descrever deslocamentos e localizações em malhas, mapas, plantas e croquis, usando direita e esquerda, mudanças de direção e sentido, e termos como paralelas, perpendiculares e transversais."),
           ("Como ensinar paralelas e perpendiculares?", "Use o mapa do bairro: ruas que nunca se cruzam são paralelas; ruas que se cruzam formando um canto reto são perpendiculares.")]
    make_unit(R, "localizacao-e-movimentacao", "G", ["EF04MA16"],
              "Descrever deslocamentos e localização de pessoas e de objetos no espaço, por meio de malhas quadriculadas e representações como desenhos, mapas, planta baixa e croquis, empregando termos como direita e esquerda, mudanças de direção e sentido, intersecção, transversais, paralelas e perpendiculares",
              "Localização e movimentação: malhas, mapas e croquis", "Localização e movimentação",
              "Atividades de matemática para o 4º ano sobre localização e movimentação: malha quadriculada, deslocamentos, direita e esquerda, ruas paralelas, perpendiculares e transversais, croquis. 100 exercícios com gabarito.",
              "Paralelas nunca se cruzam; perpendiculares formam ângulo reto.", "Na malha: primeiro a coluna, depois a linha.",
              body, faq, sets, 12, grade="4-ano")


if __name__ == "__main__":
    main()
