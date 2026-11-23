# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Décimos e centésimos (Números, EF04MA10)
  python3 tools/gen_br_matematica_4_decimos_e_centesimos.py
O sistema de numeração decimal continua depois da vírgula: décimos e centésimos; quadro de valor (U, d c);
fração decimal e número decimal; leitura; décimos e centésimos no dinheiro (10 centavos = R$ 0,10 = um décimo do real); reta numérica.
Erros: 0,5 = 5/100, 3 centavos = R$ 0,30, ler 2,35 sem pensar no valor, achar que 0,40 &gt; 0,4.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, dz, fr, reais, quadro_decimal, dinheiro_svg, Kids, use, lim

R = random.Random(80409)
K = Kids(R)
L = (lim(99999, 2),)
M = "gen_br_matematica_5_numeros_decimais"
s_fig, s_frac, s_misto, s_ler, s_reta, s_medidas = use(M, 80949, "s1_figura", "s2_frac_para_dec", "s2_misto", "s3_ler", "s4_reta", "s4_medidas", preds=L)


def s1_quadro():
    ip = R.randint(0, 99)
    f = R.randint(1, 99)
    if f % 10 == 0:
        return None
    n = ip * 100 + f
    d = [f // 10, f % 10]
    if d[0] == d[1]:
        return None
    i = R.randrange(2)
    nome = ["décimos", "centésimos"][i]
    if R.random() < 0.6:
        return mcq(quadro_decimal(n * 10, 2, 2 if ip >= 10 else 1) + "Qual é o algarismo dos %s em %s?" % (nome, dz(n, 2)), str(d[i]), [str(d[1 - i]), str(ip % 10), str((d[i] + 1) % 10)],
                   "Depois da vírgula vêm os décimos e depois os centésimos. O algarismo dos %s é <b>%d</b>." % (nome, d[i]))
    if d[i] == 0:
        return None
    v = d[i] * (10 if i == 0 else 1)
    return mcq("Quanto vale o algarismo %d em %s?" % (d[i], dz(n, 2)), dz(v, 2), [str(d[i]), dz(v * 10, 2) if i == 1 else dz(v // 10, 2), dz(v, 3)],
               "O %d está na ordem dos %s: vale <b>%s</b> (%s)." % (d[i], nome, dz(v, 2), fr(d[i], 10 if i == 0 else 100)))


def s1_regra():
    q, a, w = R.choice([("Quantos décimos formam 1 inteiro?", "10", ["100", "1", "5"]), ("Quantos centésimos formam 1 décimo?", "10", ["100", "1", "1.000"]),
                        ("Quantos centésimos formam 1 inteiro?", "100", ["10", "1.000", "1"]), ("10 centésimos são iguais a…", "1 décimo", ["1 inteiro", "10 décimos", "1 centésimo"]),
                        ("10 décimos são iguais a…", "1 inteiro", ["1 centésimo", "100 centésimos e mais 1", "10 inteiros"]),
                        ("Como no sistema de numeração, cada ordem depois da vírgula vale…", "10 vezes menos que a ordem à esquerda", ["10 vezes mais que a ordem à esquerda", "o mesmo que a ordem à esquerda", "2 vezes menos"]),
                        ("Que número tem 4 unidades, 3 décimos e 7 centésimos?", "4,37", ["4,73", "43,7", "437"]), ("Que número tem 2 unidades e 5 centésimos?", "2,05", ["2,5", "2,50", "25"]),
                        ("Que número tem 6 décimos?", "0,6", ["0,06", "6,0", "60"]), ("Que número tem 8 centésimos?", "0,08", ["0,8", "8,0", "800"])])
    return mcq(q, a, w, "Cada ordem vale 10 vezes a ordem à sua direita, também depois da vírgula. Resposta: <b>%s</b>." % a)


def s4_moedas():
    k = R.choice(["moedas", "decimo", "centavos", "ler"])
    if k == "moedas":
        items = [100] * R.randint(0, 3) + [50] * R.randint(0, 2) + [25] * R.randint(0, 2) + [10] * R.randint(0, 4) + [5] * R.randint(0, 2)
        if len(items) < 3:
            return None
        t = sum(items)
        return mcq(dinheiro_svg(items) + "Quanto dinheiro há? Escreva em reais.", reais(t), [reais(t + 10), reais(t - 5) if t > 5 else reais(t + 5), "R$ %d,%d" % (t // 100, t % 100 // 10) if t % 10 == 0 and t % 100 else reais(t * 10 if t < 1000 else t + 100)],
                   "Some o valor das moedas: <b>%s</b>." % reais(t))
    if k == "decimo":
        n = R.randint(1, 9)
        return mcq("%d moedas de 10 centavos são que fração do real e quanto em reais?" % n, "%s do real = %s" % (fr(n, 10), reais(n * 10)),
                   ["%s do real = %s" % (fr(n, 100), reais(n)), "%s do real = %s" % (fr(n, 10), reais(n * 100)), "%s do real = %s" % (fr(1, n), reais(n * 10))],
                   "10 centavos = 1 décimo do real (R$ 0,10). %d moedas = %s = <b>%s</b>." % (n, fr(n, 10), reais(n * 10)))
    if k == "centavos":
        c = R.randint(1, 9)
        return mcq("Como se escreve %s em reais?" % ("%d centavos" % c), reais(c), ["R$ 0,%d" % (c * 10), "R$ %d,00" % c, "R$ 0,%d0" % c] if c != 0 else [],
                   "1 centavo é 1 centésimo do real: %d centavos = <b>%s</b>." % (c, reais(c)))
    v = R.randint(101, 9999)
    if v % 100 == 0:
        return None
    return mcq("Quanto é %s?" % reais(v), "%s %s e %d %s" % (num(v // 100), "real" if v // 100 == 1 else "reais", v % 100, "centavo" if v % 100 == 1 else "centavos"),
               ["%s reais e %d centavos" % (num(v % 100), v // 100) if v // 100 < 100 else "%s reais" % num(v), "%s reais" % num(v), "%s reais e %d centavos" % (num(v // 100), (v % 100) * 10 % 1000)],
               "Antes da vírgula, os reais; depois, os centavos: <b>%s</b>." % ("%s %s e %d %s" % (num(v // 100), "real" if v // 100 == 1 else "reais", v % 100, "centavo" if v % 100 == 1 else "centavos")))


def s5_problema():
    k = R.choice(["corrida", "compra", "altura", "chuva", "troco", "garrafa"])
    p, g = K.next()
    if k == "corrida":
        a = R.randint(11, 99)
        if a % 10 == 0:
            return None
        return mcq("Uma pista foi dividida em 100 partes iguais. %s já correu %d partes. Que número decimal mostra a parte que foi corrida?" % (p, a), dz(a, 2),
                   [dz(a, 1), dz(100 - a, 2), str(a)], "%d de 100 partes: %s = <b>%s</b>." % (a, fr(a, 100), dz(a, 2)))
    if k == "compra":
        a, b = R.randint(110, 990), R.randint(110, 990)
        return mcq("%s comprou um caderno de %s e uma caneta de %s. Qual dos dois custou mais?" % (p, reais(a), reais(b)), "o caderno" if a > b else "a caneta",
                   ["a caneta" if a > b else "o caderno", "custaram o mesmo", "não dá para saber"] if a != b else [], "Compare os reais e depois os centavos: <b>%s</b>." % ("o caderno" if a > b else "a caneta"))
    if k == "altura":
        a, b = R.randint(120, 160), R.randint(120, 160)
        q = K.next()[0]
        if a == b or p == q:
            return None
        big = p if a > b else q
        return mcq("%s mede %s m e %s mede %s m. Quem é mais alto?" % (p, dz(a, 2), q, dz(b, 2)), big, [q if big == p else p, "Têm a mesma altura", "Não dá para saber"],
                   "Compare os décimos e depois os centésimos: <b>%s</b>." % big)
    if k == "chuva":
        a = R.randint(11, 99)
        if a % 10 == 0:
            return None
        return mcq("Num dia choveu %s cm. Quantos décimos de centímetro são?" % dz(a, 1), str(a), [str(a // 10), dz(a, 1), str(a * 10)],
                   "Cada centímetro tem 10 décimos: %s cm = <b>%d</b> décimos." % (dz(a, 1), a))
    if k == "troco":
        c = R.randint(105, 495)
        if c % 5:
            return None
        return mcq("%s pagou %s com uma cédula de R$ 5,00. Quanto recebeu de troco?" % (p, reais(c)), reais(500 - c), [reais(500 - c + 10), reais(c - 100), reais(600 - c)],
                   "R$ 5,00 − %s = <b>%s</b>." % (reais(c), reais(500 - c)))
    a = R.choice([25, 50, 75])
    return mcq("Uma garrafa tem 1 litro de água. %s bebeu %s da garrafa. Escreva com número decimal a parte que %s bebeu." % (p, fr(a, 100), g), dz(a, 2), [dz(a, 1), "%d,0" % a, dz(100 - a, 2)],
               "%s = <b>%s</b>." % (fr(a, 100), dz(a, 2)))


def main():
    seen = set()
    sets = [
        ("Décimos e centésimos", mix(R, seen, [(s_fig, 12), (s1_regra, 8)])),
        ("Quadro de valor", mix(R, seen, [(s1_quadro, 12), (s_ler, 8)])),
        ("Frações decimais e reta numérica", mix(R, seen, [(s_frac, 10), (s_misto, 4), (s_reta, 6)])),
        ("Décimos e centésimos no dinheiro", mix(R, seen, [(s4_moedas, 14), (s_medidas, 6)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["O sistema de numeração continua depois da vírgula: dividindo 1 inteiro em 10 partes, cada parte é <b>1 décimo</b> (0,1); em 100 partes, <b>1 centésimo</b> (0,01).",
         "10 centésimos = 1 décimo; 10 décimos = 1 inteiro.",
         "No dinheiro: R$ 1,00 = 100 centavos. Uma moeda de 10 centavos é 1 décimo do real (R$ 0,10); 1 centavo é 1 centésimo (R$ 0,01).",
         "Zeros no fim da parte decimal não mudam o valor: 0,4 = 0,40."],
        [("Escreva 3 inteiros e 7 centésimos.", ["3 antes da vírgula", "7 centésimos: 0,07"], "3,07"),
         ("4 moedas de 10 centavos e 3 de 1 centavo.", ["40 centavos + 3 centavos", "43 centavos"], "R$ 0,43")],
        [["Escrever " + fr(5, 100) + " como 0,5", "100 tem 2 zeros: 2 casas. " + fr(5, 100) + " = 0,05."],
         ["Escrever 3 centavos como R$ 0,30", "3 centavos = R$ 0,03; R$ 0,30 são 30 centavos."],
         ["Achar que 0,40 é maior que 0,4", "40 centésimos = 4 décimos: são iguais."]],
        quadro_decimal(3070, 2))
    faq = [("O que o 4º ano estuda sobre números decimais?", "A BNCC pede reconhecer que as regras do sistema de numeração decimal continuam depois da vírgula, com décimos e centésimos, e relacioná-los ao sistema monetário brasileiro."),
           ("Por que usar o dinheiro?", "Porque R$ 3,45 mostra bem as ordens: 3 reais, 4 moedas de 10 centavos (décimos) e 5 centavos (centésimos).")]
    make_unit(R, "decimos-e-centesimos", "N", ["EF04MA10"],
              "Reconhecer que as regras do sistema de numeração decimal podem ser estendidas para a representação decimal de um número racional e relacionar décimos e centésimos com a representação do sistema monetário brasileiro",
              "Décimos e centésimos: números decimais e dinheiro", "Décimos e centésimos",
              "Atividades de matemática para o 4º ano sobre décimos e centésimos: números decimais, quadro de valor, frações decimais, leitura, reta numérica e o real. 100 exercícios com gabarito.",
              "1 = 10 décimos = 100 centésimos.", "R$ 0,10 é 1 décimo do real; R$ 0,01 é 1 centésimo.",
              body, faq, sets, 9, grade="4-ano")


if __name__ == "__main__":
    main()
