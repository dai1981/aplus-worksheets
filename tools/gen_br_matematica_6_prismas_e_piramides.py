# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Prismas e pirâmides (Geometria, EF06MA17)
  python3 tools/gen_br_matematica_6_prismas_e_piramides.py
Nome pelo polígono da base; número de vértices, faces e arestas (prisma: n + 2 faces, 2n vértices, 3n arestas;
pirâmide: n + 1 faces, n + 1 vértices, 2n arestas); relação de Euler V + F = A + 2; planificações; poliedros e corpos redondos.
Usa os desenhos do 5º ano (figuras espaciais) com outro sorteio.
Erros: contar só as faces visíveis, trocar vértices e arestas, achar que o cilindro é prisma.
"""
import random
from br_common import lesson, mix, use
from br_9 import M, bank, unit

R = random.Random(86013)
s_nome, s_contar, s_planif, s_tabela = use("gen_br_matematica_5_figuras_espaciais_e_planificacoes", 86913, "s1_nome", "s2_contar", "s3_planif", "s4_tabela")
BASE = {3: ("triangular", "triângulo"), 4: ("quadrangular", "quadrilátero"), 5: ("pentagonal", "pentágono"), 6: ("hexagonal", "hexágono"), 7: ("heptagonal", "heptágono"), 8: ("octogonal", "octógono"), 9: ("eneagonal", "eneágono"), 10: ("decagonal", "decágono"), 12: ("dodecagonal", "dodecágono")}


def vfa(kind, n):
    return (2 * n, n + 2, 3 * n) if kind == "prisma" else (n + 1, n + 1, 2 * n)


def s1_formula():
    kind = R.choice(["prisma", "pirâmide"])
    n = R.choice(sorted(BASE))
    nm = "%s %s" % ("um prisma" if kind == "prisma" else "uma pirâmide", "de base " + BASE[n][0])
    V, F_, A = vfa(kind, n)
    k = R.choice(["V", "F", "A"])
    lab = {"V": "vértices", "F": "faces", "A": "arestas"}[k]
    val = {"V": V, "F": F_, "A": A}[k]
    ws = {str(x) for x in (V, F_, A, n, val + 1, val - 1)} - {str(val)}
    why = {"prisma": {"V": "2 × %d" % n, "F": "%d laterais + 2 bases" % n, "A": "3 × %d" % n}, "pirâmide": {"V": "%d da base + 1 (vértice)" % n, "F": "%d laterais + 1 base" % n, "A": "2 × %d" % n}}[kind][k]
    return M("Quantas %s tem %s?" % (lab, nm), str(val), sorted(ws), "A base tem %d lados: %s = <b>%d %s</b>." % (n, why, val, lab))


def s2_euler():
    kind = R.choice(["prisma", "pirâmide"])
    n = R.choice(sorted(BASE))
    V, F_, A = vfa(kind, n)
    miss = R.choice(["V", "F", "A"])
    known = {"V": V, "F": F_, "A": A}
    lab = {"V": "vértices", "F": "faces", "A": "arestas"}
    txt = " e ".join("%d %s" % (known[k], lab[k]) for k in "VFA" if k != miss)
    val = known[miss]
    return M("Um poliedro tem %s. Pela relação de Euler (V + F = A + 2), quantas %s ele tem?" % (txt, lab[miss]), str(val), [str(val + 2), str(val - 2), str(val + 4)],
             "V + F = A + 2: %d + %d = %d + 2. Resposta: <b>%d</b>." % (V, F_, A, val))


def s3_base():
    kind = R.choice(["prisma", "pirâmide"])
    n = R.choice(sorted(BASE))
    V, F_, A = vfa(kind, n)
    q = "Um%s %s tem %d arestas. Qual é o polígono da base?" % ("" if kind == "prisma" else "a", kind, A)
    ws = [BASE[m][1] for m in sorted(BASE) if m != n][:6]
    R.shuffle(ws)
    return M(q, BASE[n][1], ws, "No %s, arestas = %s × lados da base: %d ÷ %d = %d lados: <b>%s</b>." % (kind, "3" if kind == "prisma" else "2", A, 3 if kind == "prisma" else 2, n, BASE[n][1]))


s4_conceitos = bank(R, [
    ("Um cubo é um prisma de base…", "quadrada", ["triangular", "circular", "hexagonal"]),
    ("As faces laterais de um prisma reto são…", "retângulos", ["triângulos", "círculos", "pentágonos"]),
    ("As faces laterais de uma pirâmide são…", "triângulos", ["retângulos", "círculos", "quadrados sempre"]),
    ("O cilindro é um poliedro?", "não, é um corpo redondo", ["sim, é um prisma", "sim, é uma pirâmide", "sim, tem 3 faces planas"]),
    ("Quantas bases tem um prisma?", "2", ["1", "3", "nenhuma"]),
    ("Quantas bases tem uma pirâmide?", "1", ["2", "3", "nenhuma"]),
    ("O segmento onde duas faces se encontram chama-se…", "aresta", ["vértice", "base", "diagonal"]),
    ("O ponto onde três ou mais arestas se encontram chama-se…", "vértice", ["face", "aresta", "base"]),
    ("Qual sólido tem 5 faces, 6 vértices e 9 arestas?", "prisma de base triangular", ["pirâmide de base quadrada", "cubo", "pirâmide de base pentagonal"]),
    ("Qual sólido tem 5 faces, 5 vértices e 8 arestas?", "pirâmide de base quadrada", ["prisma de base triangular", "cubo", "prisma de base quadrada"]),
    ("Uma caixa de sapatos lembra um…", "paralelepípedo (prisma de base retangular)", ["cilindro", "cone", "pirâmide"]),
    ("Na planificação de um prisma de base pentagonal, há…", "2 pentágonos e 5 retângulos", ["1 pentágono e 5 triângulos", "2 pentágonos e 5 triângulos", "5 pentágonos e 2 retângulos"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Reconhecer prismas e pirâmides", mix(R, seen, [(s_nome, 12), (s4_conceitos, 8)])),
        ("Contar vértices, faces e arestas", mix(R, seen, [(s_contar, 10), (s1_formula, 10)])),
        ("Fórmulas e relação de Euler", mix(R, seen, [(s1_formula, 8), (s2_euler, 12)])),
        ("Planificações", mix(R, seen, [(s_planif, 10), (s_tabela, 4), (s4_conceitos, 4), (s3_base, 2)])),
        ("Descobrir a base", mix(R, seen, [(s3_base, 12), (s2_euler, 8)])),
    ]
    body = lesson(
        ["Um <b>prisma</b> tem duas bases iguais e paralelas; as faces laterais são retângulos. Uma <b>pirâmide</b> tem uma base e faces laterais triangulares que se encontram num vértice.",
         "O nome vem do polígono da base: prisma de base hexagonal, pirâmide de base quadrada…",
         "Com n lados na base — prisma: 2n vértices, n + 2 faces, 3n arestas; pirâmide: n + 1 vértices, n + 1 faces, 2n arestas.",
         "Em todo poliedro convexo vale a <b>relação de Euler</b>: V + F = A + 2."],
        [("Prisma de base pentagonal", ["V = 10", "F = 7", "A = 15"], "10 + 7 = 15 + 2"),
         ("Pirâmide de base hexagonal", ["V = 7", "F = 7", "A = 12"], "7 + 7 = 12 + 2")],
        [["Contar só o que aparece no desenho", "Imagine as faces de trás."],
         ["Trocar vértices e arestas", "Vértice é ponto; aresta é segmento."],
         ["Achar que cilindro é prisma", "Ele tem superfície curva: é corpo redondo."]])
    faq = [("Qual é a relação de Euler?", "Em poliedros convexos, o número de vértices mais o de faces é igual ao número de arestas mais 2: V + F = A + 2."),
           ("O que a BNCC pede no 6º ano?", "Quantificar e estabelecer relações entre o número de vértices, faces e arestas de prismas e pirâmides, em função do seu polígono da base (EF06MA17).")]
    unit(R, "prismas-e-piramides", "G", ["EF06MA17"],
         "Quantificar e estabelecer relações entre o número de vértices, faces e arestas de prismas e pirâmides, em função do seu polígono da base, para resolver problemas e desenvolver a percepção espacial",
         "Prismas e pirâmides: vértices, faces e arestas", "Prismas e pirâmides",
         "Atividades de matemática para o 6º ano sobre prismas e pirâmides: nomes, vértices, faces e arestas, fórmulas pelo polígono da base, relação de Euler e planificações. 100 exercícios com gabarito.",
         "V + F = A + 2", "Prisma: 3n arestas. Pirâmide: 2n arestas.",
         body, faq, sets, 13, grade="6-ano")


if __name__ == "__main__":
    main()
