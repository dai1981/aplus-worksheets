# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Retas paralelas, perpendiculares e algoritmos de deslocamento (Geometria, EF06MA22, EF06MA23)
  python3 tools/gen_br_matematica_6_retas_paralelas_e_perpendiculares.py
Retas paralelas, perpendiculares e concorrentes (figuras e situações do dia a dia); construção com régua e esquadro (passos);
algoritmos de deslocamento numa malha (andar e virar 90°), com a posição final e a direção.
Erros: achar que retas que não se cruzam no desenho são sempre paralelas, achar que toda concorrente é perpendicular, virar para o lado errado.
"""
import random
import math
from br_common import lesson, mix
from br_9 import M, bank, unit, _svg, _ln, _t, INK, RED

R = random.Random(86016)


def par_svg(kind):
    W, H = 260, 170
    t = math.radians(R.uniform(-35, 35))
    cx, cy = 130, 85
    ux, uy = math.cos(t), math.sin(t)
    s = []
    if kind == "paralelas":
        off = R.uniform(32, 55)
        for o in (-off, off):
            px, py = cx - uy * o, cy + ux * o
            s.append(_ln(px - ux * 110, py - uy * 110, px + ux * 110, py + uy * 110, INK, 2.4))
    else:
        s.append(_ln(cx - ux * 115, cy - uy * 115, cx + ux * 115, cy + uy * 115, INK, 2.4))
        a = math.radians(90 if kind == "perpendiculares" else R.choice([40, 55, 125, 140]))
        vx, vy = math.cos(t + a), math.sin(t + a)
        s.append(_ln(cx - vx * 75, cy - vy * 75, cx + vx * 75, cy + vy * 75, INK, 2.4))
        if kind == "perpendiculares":
            q = 12
            s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>" % (cx + ux * q, cy + uy * q, cx + ux * q + vx * q, cy + uy * q + vy * q, cx + vx * q, cy + vy * q, RED))
    return _svg(W, H, "".join(s), "duas retas")


def s1_figura():
    kind = R.choice(["paralelas", "perpendiculares", "concorrentes"])
    pic = par_svg(kind)
    ans = {"paralelas": "paralelas", "perpendiculares": "perpendiculares", "concorrentes": "concorrentes, mas não perpendiculares"}[kind]
    return M(pic + "Como são estas duas retas? (O quadradinho vermelho marca ângulo reto.)", ans, [x for x in ["paralelas", "perpendiculares", "concorrentes, mas não perpendiculares", "coincidentes"] if x != ans],
             {"paralelas": "Elas nunca se encontram e mantêm a mesma distância: <b>paralelas</b>.", "perpendiculares": "Elas se cruzam formando ângulos retos: <b>perpendiculares</b>.",
              "concorrentes": "Elas se cruzam, mas sem ângulo reto: <b>concorrentes, mas não perpendiculares</b>."}[kind])


s2_dia_a_dia = bank(R, [
    ("Os trilhos de uma ferrovia reta lembram retas…", "paralelas", ["perpendiculares", "concorrentes não perpendiculares", "curvas"]),
    ("A borda de cima e a borda lateral de uma folha de caderno lembram retas…", "perpendiculares", ["paralelas", "coincidentes", "que nunca se cruzam"]),
    ("As linhas de um caderno pautado lembram retas…", "paralelas", ["perpendiculares", "concorrentes", "inclinadas umas para as outras"]),
    ("Os ponteiros de um relógio às 3h em ponto formam um ângulo…", "reto (estão perpendiculares)", ["raso", "nulo", "agudo"]),
    ("Duas ruas que se cruzam formando um «X» inclinado lembram retas…", "concorrentes", ["paralelas", "coincidentes", "que nunca se cruzam"]),
    ("Duas retas perpendiculares formam quantos ângulos retos no cruzamento?", "4", ["1", "2", "nenhum"]),
    ("Duas retas paralelas a uma terceira reta são…", "paralelas entre si", ["perpendiculares entre si", "sempre concorrentes", "iguais à terceira"]),
    ("Duas retas perpendiculares a uma mesma reta (no plano) são…", "paralelas entre si", ["perpendiculares entre si", "concorrentes", "coincidentes"]),
    ("Retas que se cruzam num único ponto são chamadas…", "concorrentes", ["paralelas", "coincidentes", "segmentos"]),
    ("Duas retas no mesmo plano que não têm nenhum ponto comum são…", "paralelas", ["perpendiculares", "concorrentes", "secantes"]),
], "s2_dia_a_dia")


s3_construcao = bank(R, [
    ("Para traçar uma reta <b>perpendicular</b> a r com régua e esquadro, apoiamos…", "um lado do ângulo reto do esquadro sobre r", ["a régua inclinada sobre r", "o compasso no meio de r", "o transferidor em 45°"]),
    ("Para traçar uma reta <b>paralela</b> a r passando por P, depois de apoiar o esquadro em r, devemos…", "deslizar o esquadro apoiado na régua até P", ["girar o esquadro 90°", "apoiar o compasso em P", "levantar a régua"]),
    ("Qual instrumento tem um ângulo reto e ajuda a traçar perpendiculares?", "esquadro", ["compasso", "transferidor sem marcações", "borracha"]),
    ("Na construção de paralelas com régua e esquadro, a régua fica…", "parada, servindo de guia", ["girando", "sobre a reta r sempre", "em pé"]),
    ("Um algoritmo é…", "uma sequência de passos para resolver um problema", ["um tipo de reta", "um número primo", "um instrumento de desenho"]),
    ("Num fluxograma para desenhar um quadrado, o passo que se repete 4 vezes é…", "andar um lado e virar 90°", ["andar e virar 60°", "virar 180°", "desenhar um círculo"]),
    ("Para desenhar um retângulo de 5 por 3, o robô anda 5, vira 90°, anda 3, vira 90°, anda 5, vira 90° e…", "anda 3", ["anda 5", "vira 180°", "para"]),
], "s3_construcao")

DIRS = ["norte", "leste", "sul", "oeste"]
VEC = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def s4_robo():
    x, y = R.randint(0, 3), R.randint(0, 3)
    dr = R.randrange(4)
    steps = []
    cx, cy, cd = x, y, dr
    for _ in range(R.randint(2, 4)):
        n = R.randint(1, 4)
        steps.append("ande %d" % n)
        cx += VEC[cd][0] * n
        cy += VEC[cd][1] * n
        t = R.choice(["direita", "esquerda"])
        steps.append("vire à %s" % t)
        cd = (cd + (1 if t == "direita" else -1)) % 4
    steps.pop()
    fx, fy, fd = x, y, dr
    for s_ in steps:
        if s_.startswith("ande"):
            n = int(s_.split()[1])
            fx += VEC[fd][0] * n
            fy += VEC[fd][1] * n
        else:
            fd = (fd + (1 if "direita" in s_ else -1)) % 4
    k = R.choice(["pos", "dir"])
    txt = "Um robô está no ponto (%d, %d) virado para o %s (norte é para cima, leste para a direita). Comandos: %s." % (x, y, DIRS[dr], "; ".join(steps))
    if k == "pos":
        alt = [(fy, fx), (fx + 1, fy), (fx, fy - 1), (2 * x - fx, fy)]
        ws = ["(%d, %d)" % p for p in alt if p != (fx, fy)]
        return M(txt + " Em que ponto ele termina?", "(%d, %d)" % (fx, fy), ws, "Siga os comandos um a um, mudando o x para leste/oeste e o y para norte/sul: <b>(%d, %d)</b>." % (fx, fy))
    return M(txt + " Para onde ele está virado no final?", DIRS[fd], [z for z in DIRS if z != DIRS[fd]], "Cada «vire à direita» gira 90° no sentido horário: no final ele olha para o <b>%s</b>." % DIRS[fd])


def main():
    seen = set()
    sets = [
        ("Paralelas, perpendiculares ou concorrentes?", mix(R, seen, [(s1_figura, 10), (s2_dia_a_dia, 10)])),
        ("Retas no dia a dia", mix(R, seen, [(s1_figura, 10), (s3_construcao, 4), (s4_robo, 6)])),
        ("Construções e algoritmos", mix(R, seen, [(s3_construcao, 3), (s4_robo, 17)])),
        ("Deslocamentos na malha", mix(R, seen, [(s4_robo, 20)])),
        ("Revisão", mix(R, seen, [(s1_figura, 8), (s4_robo, 12)])),
    ]
    body = lesson(
        ["Retas <b>paralelas</b> estão no mesmo plano e nunca se encontram. Retas <b>concorrentes</b> se cruzam num ponto; se formam ângulos retos, são <b>perpendiculares</b>.",
         "Com <b>régua e esquadro</b>: para a perpendicular, apoie um lado do ângulo reto do esquadro na reta; para a paralela, deslize o esquadro ao longo da régua parada.",
         "Um <b>algoritmo</b> de deslocamento é uma lista de comandos (ande, vire 90°). Siga um comando por vez e anote a posição e a direção."],
        [("Robô em (0, 0) virado para leste: ande 3, vire à esquerda, ande 2", ["(3, 0)", "virado para o norte", "(3, 2)"], "termina em (3, 2)")],
        [["Achar que retas que não se cruzam no desenho são paralelas", "Prolongue as retas: elas podem se cruzar fora do papel."],
         ["Achar que toda concorrente é perpendicular", "Perpendicular precisa de ângulo reto."],
         ["Virar para o lado errado", "Direita = sentido horário."]],
        par_svg("perpendiculares"))
    faq = [("Qual é a diferença entre retas concorrentes e perpendiculares?", "Retas concorrentes se cruzam num ponto. As perpendiculares são concorrentes especiais: o cruzamento forma quatro ângulos retos."),
           ("O que a BNCC pede no 6º ano?", "Utilizar instrumentos, como réguas e esquadros, ou softwares para representações de retas paralelas e perpendiculares (EF06MA22) e construir algoritmo para resolver situações passo a passo, como deslocamentos no plano cartesiano (EF06MA23).")]
    unit(R, "retas-paralelas-e-perpendiculares", "G", ["EF06MA22", "EF06MA23"],
         "Utilizar instrumentos, como réguas e esquadros, ou softwares para representações de retas paralelas e perpendiculares e construção de quadriláteros, entre outros; construir algoritmo para resolver situações passo a passo (como na construção de dobraduras ou na indicação de deslocamento de um objeto no plano segundo pontos de referência e distâncias fornecidas etc.)",
         "Retas paralelas, perpendiculares e deslocamentos", "Retas paralelas e perpendiculares",
         "Atividades de matemática para o 6º ano sobre retas paralelas, perpendiculares e concorrentes, construções com régua e esquadro e algoritmos de deslocamento na malha. 100 exercícios com gabarito.",
         "Paralelas nunca se encontram.", "Perpendiculares se cruzam em ângulo reto.",
         body, faq, sets, 16, grade="6-ano")


if __name__ == "__main__":
    main()
