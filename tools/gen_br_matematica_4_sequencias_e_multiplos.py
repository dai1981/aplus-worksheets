# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Sequências e múltiplos (Álgebra, EF04MA11, EF04MA12)
  python3 tools/gen_br_matematica_4_sequencias_e_multiplos.py
Sequências formadas por múltiplos de um número (regra, próximo termo, termo que falta); reconhecer múltiplos;
grupos de números que deixam o mesmo resto numa divisão (pares e ímpares; resto 1 na divisão por 3 …); problemas com calendários e repetições.
Erros: achar a regra olhando só dois números, confundir múltiplo e divisor, achar que números com o mesmo último algarismo têm o mesmo resto por 3.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, Kids

R = random.Random(80410)
K = Kids(R)


def seq(m, start=None, n=5):
    s = start if start is not None else R.randint(1, 12)
    return [m * (s + i) for i in range(n)]


def s1_proximo():
    m = R.randint(3, 12)
    xs = seq(m, R.randint(1, 15))
    k = R.choice(["prox", "falta"])
    if k == "prox":
        return mcq("Qual é o próximo número da sequência %s, …?" % ", ".join(num(x) for x in xs[:4]), num(xs[4]), [num(xs[3] + m + 1), num(xs[3] + m - 1), num(xs[3] + 2 * m), num(xs[3] + xs[0])],
                   "A sequência aumenta de %d em %d (múltiplos de %d): %s + %d = <b>%s</b>." % (m, m, m, num(xs[3]), m, num(xs[4])))
    i = R.randint(1, 3)
    shown = [num(x) if j != i else "___" for j, x in enumerate(xs)]
    return mcq("Que número falta na sequência %s?" % ", ".join(shown), num(xs[i]), [num(xs[i] + 1), num(xs[i] - 1), num(xs[i] + m)],
               "Os números aumentam de %d em %d: <b>%s</b>." % (m, m, num(xs[i])))


def s1_regra():
    m = R.randint(2, 12)
    xs = seq(m, R.randint(1, 10))
    return mcq("A sequência %s, … é formada pelos múltiplos de que número?" % ", ".join(num(x) for x in xs), str(m), [str(xs[0]), str(m * 2), str(m + 1)],
               "Todos são resultados da tabuada do %d (e aumentam de %d em %d): <b>%d</b>." % (m, m, m, m))


def s2_decrescente():
    m = R.choice([5, 10, 25, 50, 100, 4, 6, 8])
    top = m * R.randint(10, 40)
    xs = [top - m * i for i in range(5)]
    return mcq("Qual é o próximo número da sequência %s, …?" % ", ".join(num(x) for x in xs[:4]), num(xs[4]), [num(xs[3] + m), num(xs[3] - m - 1), num(xs[3] - 2 * m)],
               "A sequência diminui de %d em %d: %s − %d = <b>%s</b>." % (m, m, num(xs[3]), m, num(xs[4])))


def s3_eh_multiplo():
    m = R.randint(3, 12)
    k = R.choice(["sim", "nao", "lista", "lista"])
    if k in ("sim", "nao"):
        n = m * R.randint(3, 15) + (0 if k == "sim" else R.randint(1, m - 1))
        ok = n % m == 0
        return mcq("%d é múltiplo de %d?" % (n, m), "Sim: %d ÷ %d = %d, sem resto" % (n, m, n // m) if ok else "Não: %d ÷ %d deixa resto %d" % (n, m, n % m),
                   ["Não: %d ÷ %d deixa resto %d" % (n, m, (n + 1) % m or 1) if ok else "Sim: %d ÷ %d = %d, sem resto" % (n, m, n // m), "Sim, porque %d é maior que %d" % (n, m), "Não, porque %d é ímpar" % m if m % 2 else "Não, porque %d é par" % n],
                   "Um número é múltiplo de %d quando a divisão por %d não deixa resto. <b>%s</b>." % (m, m, "Sim" if ok else "Não"))
    good = m * R.randint(3, 12)
    opts = [good] + [good + R.choice([1, 2, -1, m // 2 or 1]) for _ in range(3)]
    if len(set(opts)) < 4 or any(o % m == 0 for o in opts[1:]):
        return None
    return mcq("Qual destes números é múltiplo de %d? %s" % (m, ", ".join(map(str, sorted(opts)))), str(good), [str(o) for o in opts[1:]],
               "%d ÷ %d = %d, sem resto: <b>%d</b> está na tabuada do %d." % (good, m, good // m, good, m))


def s4_resto():
    d = R.choice([2, 3, 4, 5, 10])
    r = R.randint(0, d - 1)
    k = R.choice(["grupo", "qual", "resto"])
    if k == "resto":
        n = d * R.randint(4, 30) + r
        return mcq("Qual é o resto da divisão de %d por %d?" % (n, d), str(r), [str(x) for x in (r + 1 if r + 1 < d else r - 1, n // d, d)],
                   "%d ÷ %d = %d e resto <b>%d</b>." % (n, d, n // d, r))
    if k == "grupo":
        st = R.randint(1, 6)
        xs = [d * (st + i) + r for i in range(4)]
        return mcq("Os números %s deixam o mesmo resto quando divididos por %d. Que resto é esse?" % (", ".join(map(str, xs)), d), str(r),
                   [str(x) for x in (d, (r + 1) % d, xs[0] // d, d - 1 if d - 1 != r else 1)],
                   "%d ÷ %d = %d e resto %d. Os outros vão de %d em %d, então o resto é sempre <b>%d</b>." % (xs[0], d, xs[0] // d, r, d, d, r))
    good = d * R.randint(3, 20) + r
    ws = []
    while len(ws) < 3:
        x = d * R.randint(3, 20) + R.randint(0, d - 1)
        if x % d != r and x not in ws:
            ws.append(x)
    return mcq("Qual destes números deixa resto %d na divisão por %d? %s" % (r, d, ", ".join(map(str, sorted([good] + ws)))), str(good), [str(x) for x in ws],
               "%d ÷ %d = %d e resto %d: <b>%d</b>." % (good, d, good // d, r, good))


def s4_par():
    n = R.randint(100, 99999)
    k = "par" if n % 2 == 0 else "ímpar"
    return mcq("%s é par ou ímpar? (Qual é o resto da divisão por 2?)" % num(n), "%s: resto %d" % (k, n % 2), ["%s: resto %d" % ("ímpar" if k == "par" else "par", 1 - n % 2), "%s: resto 2" % k, "depende do primeiro algarismo"],
               "Olhe o último algarismo (%d). Pares deixam resto 0 na divisão por 2; ímpares deixam resto 1. <b>%s</b>." % (n % 10, k))


def s5_problema():
    k = R.choice(["onibus", "calendario", "pulos", "fila", "semaforo", "bolo"])
    p, g = K.next()
    if k == "onibus":
        m = R.choice([12, 15, 20, 25, 30])
        h = R.randint(6, 8)
        n = R.randint(4, 6)
        mins = h * 60 + m * n
        return mcq("Um ônibus sai do terminal a cada %d minutos. O primeiro sai às %dh. A que horas sai o %dº ônibus?" % (m, h, n + 1), "%dh%02d" % divmod(mins, 60) if mins % 60 else "%dh" % (mins // 60),
                   ["%dh%02d" % divmod(x, 60) if x % 60 else "%dh" % (x // 60) for x in (mins + m, mins - m, h * 60 + m * (n + 1) + 5)],
                   "Some %d minutos %d vezes: %d × %d = %d minutos depois das %dh → <b>%s</b>." % (m, n, n, m, m * n, h, "%dh%02d" % divmod(mins, 60) if mins % 60 else "%dh" % (mins // 60)))
    if k == "calendario":
        m = R.choice([2, 3, 4, 5, 7])
        s = R.randint(1, m)
        dias = [s + m * i for i in range(30) if s + m * i <= 30]
        q = R.choice([x for x in range(s + 1, 31)])
        ok = (q - s) % m == 0
        return mcq("%s treina natação a cada %d dias. Treinou no dia %d de abril. Vai treinar também no dia %d?" % (p, m, s, q), "Sim" if ok else "Não",
                   ["Não" if ok else "Sim", "Só se for sábado", "Não dá para saber"],
                   "Os dias de treino são %s, … (de %d em %d). <b>%s</b>." % (", ".join(map(str, dias[:6])), m, m, "Sim, o dia %d está na lista" % q if ok else "Não, %d não está na lista" % q))
    if k == "pulos":
        m = R.randint(3, 9)
        n = R.randint(5, 12)
        return mcq("Um sapo pula sempre %d casas na trilha, começando na casa 0. Em que casa ele estará depois de %d pulos?" % (m, n), str(m * n), [str(m + n), str(m * (n - 1)), str(m * n + m)],
                   "Ele visita os múltiplos de %d: %d × %d = <b>%d</b>." % (m, n, m, m * n))
    if k == "fila":
        d = R.randint(3, 6)
        n = R.randint(20, 60)
        return mcq("Numa brincadeira, os alunos contam de 1 a %d em roda, e quem fala um múltiplo de %d bate palmas. Quantos alunos batem palmas?" % (n, d), str(n // d),
                   [str(x) for x in (n // d + 1, n - n // d, d)], "Os múltiplos de %d até %d são %d ÷ %d = %d e resto %d: <b>%d alunos</b>." % (d, n, n, d, n // d, n % d, n // d))
    if k == "semaforo":
        c = R.choice(["vermelho", "amarelo", "verde"])
        pat = ["vermelho", "amarelo", "verde"]
        n = R.randint(10, 40)
        cor = pat[(n - 1) % 3]
        return mcq("Um colar tem contas na ordem vermelha, amarela, verde, vermelha, amarela, verde… De que cor é a %dª conta?" % n, cor.replace("o", "a") if cor != "verde" else "verde",
                   [x.replace("o", "a") if x != "verde" else "verde" for x in pat if x != cor] + ["branca"],
                   "O padrão se repete a cada 3. %d ÷ 3 = %d e resto %d: a conta é a %dª do padrão, <b>%s</b>." % (n, n // 3, n % 3, (n - 1) % 3 + 1, cor.replace("o", "a") if cor != "verde" else "verde"))
    m = R.choice([6, 8, 12])
    n = m * R.randint(3, 12) + R.randint(1, m - 1)
    return mcq("Uma confeitaria coloca %d docinhos em cada caixa. Tem %d docinhos. Quantos ficam fora das caixas completas?" % (m, n), str(n % m), [str(x) for x in (n // m, m - n % m, n % m + 1)],
               "%d ÷ %d = %d e resto %d: <b>%d docinhos</b> ficam de fora." % (n, m, n // m, n % m, n % m))


def main():
    seen = set()
    sets = [
        ("Sequências de múltiplos", mix(R, seen, [(s1_proximo, 14), (s1_regra, 6)])),
        ("Sequências crescentes e decrescentes", mix(R, seen, [(s2_decrescente, 10), (s1_regra, 10)])),
        ("Múltiplos de um número", mix(R, seen, [(s3_eh_multiplo, 20)])),
        ("Números com o mesmo resto", mix(R, seen, [(s4_resto, 14), (s4_par, 6)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Os <b>múltiplos</b> de um número são os resultados da sua tabuada: múltiplos de 4 são 0, 4, 8, 12, 16…",
         "Numa sequência de múltiplos, os números aumentam sempre do mesmo tanto.",
         "Um número é múltiplo de 6 quando a divisão por 6 <b>não deixa resto</b>.",
         "Os números que deixam o mesmo resto numa divisão também formam uma sequência: 2, 7, 12, 17… deixam resto 2 na divisão por 5."],
        [("Próximo número: 7, 14, 21, 28, …", ["aumenta de 7 em 7", "28 + 7"], "35"),
         ("Que resto 23 deixa na divisão por 5?", ["5 × 4 = 20", "23 − 20 = 3"], "3")],
        [["Achar a regra olhando só dois números", "Confira com todos os números da sequência."],
         ["Confundir múltiplo e divisor: 3 é múltiplo de 12", "12 é múltiplo de 3 (12 = 3 × 4)."],
         ["Achar que o resto pode ser maior que o divisor", "Na divisão por 5, o resto é 0, 1, 2, 3 ou 4."]])
    faq = [("O que são múltiplos para o 4º ano?", "São os números da tabuada de um número. A BNCC pede reconhecer as regularidades de sequências formadas por múltiplos de um número natural."),
           ("Por que estudar os restos?", "A BNCC pede reconhecer que há grupos de números que deixam o mesmo resto numa divisão, como os pares (resto 0 na divisão por 2) e os ímpares (resto 1).")]
    make_unit(R, "sequencias-e-multiplos", "A", ["EF04MA11", "EF04MA12"],
              "Identificar regularidades em sequências numéricas compostas por múltiplos de um número natural; reconhecer, por meio de investigações, que há grupos de números naturais para os quais as divisões por um determinado número resultam em restos iguais, identificando regularidades",
              "Sequências de múltiplos e números com o mesmo resto", "Sequências e múltiplos",
              "Atividades de matemática para o 4º ano sobre sequências de múltiplos, regra da sequência, múltiplos de um número, restos iguais, pares e ímpares e problemas. 100 exercícios com gabarito.",
              "Múltiplos de um número: os resultados da sua tabuada.", "Múltiplo de 6: a divisão por 6 não deixa resto.",
              body, faq, sets, 10, grade="4-ano")


if __name__ == "__main__":
    main()
