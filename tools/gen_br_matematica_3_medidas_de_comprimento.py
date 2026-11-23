# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Medidas de comprimento (Grandezas e medidas, EF03MA17, EF03MA18, EF03MA19)
  python3 tools/gen_br_matematica_3_medidas_de_comprimento.py
Unidades não padronizadas (palmo, passo) e o resultado depende da unidade; metro, centímetro e milímetro;
escolher a unidade e o instrumento (régua, fita métrica, trena); medir com a régua; 1 m = 100 cm, 1 cm = 10 mm;
comparar e ordenar comprimentos; estimar; problemas.
Erros: começar a medir no 1 da régua, achar que palmos de pessoas diferentes dão o mesmo número, comparar 1 m e 90 cm pelo número.
"""
import random
import gen_fr_maths_ce2_longueurs_et_perimetres as FRL
from br_common import mcq, num, lesson, make_unit, mix, Kids, relabel, NB

R = random.Random(80316)
K = Kids(R)
OBJ = [("Um lápis mede cerca de", 15, "cm"), ("Uma borracha mede cerca de", 4, "cm"), ("Uma formiga mede cerca de", 5, "mm"), ("Uma joaninha mede cerca de", 7, "mm"),
       ("A porta da sala tem cerca de", 2, "m"), ("Um campo de futebol tem cerca de", 100, "m"), ("Um caderno mede cerca de", 28, "cm"),
       ("A grossura de uma moeda é de cerca de", 2, "mm"), ("Um ônibus mede cerca de", 12, "m"), ("Uma criança do 3º ano tem cerca de", 130, "cm"),
       ("Um clipe mede cerca de", 3, "cm"), ("Uma piscina olímpica mede", 50, "m"), ("A espessura de um livro é de cerca de", 15, "mm"),
       ("Uma sala de aula mede cerca de", 8, "m"), ("Um palito de fósforo mede cerca de", 4, "cm")]
UNITS = ["mm", "cm", "m"]


def L(v, u):
    return "%s%s%s" % (num(v), NB, u)


def regua(a, b):
    return relabel(FRL.regle(a, b), "régua em centímetros e um segmento vermelho")


def s1_unidade():
    o, v, u = R.choice(OBJ)
    return mcq("Que unidade completa a frase? %s %s …" % (o, num(v)), u, [x for x in UNITS if x != u] + ["km"],
               "%s %s <b>%s</b>." % (o, num(v), u))


INSTR = [("a altura da porta", "a trena ou a fita métrica"), ("o comprimento de um lápis", "a régua"), ("a cintura de uma pessoa", "a fita métrica"),
         ("o comprimento da quadra da escola", "a trena"), ("a largura de uma folha de caderno", "a régua"), ("o contorno de uma bola", "a fita métrica"),
         ("o comprimento de uma formiga", "a régua (em milímetros)"), ("a largura da sala de aula", "a trena")]


def s1_instrumento():
    o, a = R.choice(INSTR)
    w = [x for x in ["a régua", "a trena", "a fita métrica", "a balança", "o relógio", "o termômetro", "a régua (em milímetros)", "a trena ou a fita métrica"] if x != a and x not in a and a not in x]
    R.shuffle(w)
    return mcq("Qual é o instrumento mais adequado para medir %s?" % o, a, w, "Para medir %s usamos <b>%s</b>." % (o, a))


def s2_palmo():
    (p1, g1), (p2, g2) = K.two()
    dois = "as duas" if g1 == g2 == "ela" else "os dois"
    a = R.randint(6, 9)
    b = a + R.randint(2, 4)
    k = R.choice(["quem", "porque", "padrao"])
    if k == "quem":
        return mcq("%s mediu a mesa e encontrou %d palmos. %s mediu a mesma mesa e encontrou %d palmos. Quem tem o palmo maior?" % (p1, a, p2, b), p1,
                   [p2, "%s têm o mesmo palmo" % dois, "não dá para saber"],
                   "Quem precisou de <b>menos</b> palmos para a mesma mesa tem o palmo maior: <b>%s</b>." % p1)
    if k == "porque":
        return mcq("%s e %s mediram o mesmo corredor com passos: deu %d passos e %d passos. Por que deu diferente?" % (p1, p2, a * 2, b * 2),
                   "porque os passos d%s têm tamanhos diferentes" % dois, ["porque um%s d%s errou a conta" % ("a" if dois == "as duas" else "", dois), "porque o corredor mudou de tamanho", "porque passo não serve para medir"],
                   "O resultado da medida depende da unidade usada: <b>os passos têm tamanhos diferentes</b>.")
    return mcq("Por que usamos o metro em vez do palmo para comprar um tecido?", "porque o metro é igual para todos", ["porque o palmo é muito pequeno", "porque o metro é mais bonito", "porque o palmo só serve para crianças"],
               "O metro é uma unidade <b>padronizada</b>: é igual para todos, então todo mundo encontra a mesma medida.")


def s3_regua():
    a = R.choice([0, 0, 0, 10, 20, 30])
    b = a + R.choice([10, 20, 30, 40, 50, 60, 70, 80, 90]) + R.choice([0, 0, 5])
    if b > 140:
        return None
    ln = b - a
    fmt = lambda m: "%d cm" % (m // 10) if m % 10 == 0 else "%d cm e %d mm" % (m // 10, m % 10)
    w = [fmt(b), fmt(ln + 10), fmt(ln - 10) if ln > 10 else fmt(ln + 20), "%d mm" % (ln // 10)]
    return mcq(regua(a, b) + "Quanto mede o segmento vermelho?", fmt(ln), [x for x in w if x != fmt(ln)],
               "O segmento vai de %s até %s: %s." % (fmt(a) if a else "0", fmt(b), "<b>%s</b>" % fmt(ln)))


def s4_converter():
    k = R.choice(["m-cm", "cm-m", "cm-mm", "mm-cm", "mcm"])
    if k == "m-cm":
        v = R.randint(2, 9)
        return mcq("Quantos centímetros há em %d metros?" % v, L(100 * v, "cm"), [L(10 * v, "cm"), L(1000 * v, "cm"), L(v + 100, "cm")],
                   "1 m = 100 cm, então %d m = <b>%s</b>." % (v, L(100 * v, "cm")))
    if k == "cm-m":
        v = R.randint(2, 9)
        return mcq("%s são quantos metros?" % L(100 * v, "cm"), L(v, "m"), [L(10 * v, "m"), L(100 * v, "m"), L(v * 1000, "m")],
                   "100 cm = 1 m, então %s = <b>%s</b>." % (L(100 * v, "cm"), L(v, "m")))
    if k == "cm-mm":
        v = R.randint(2, 15)
        return mcq("Quantos milímetros há em %d centímetros?" % v, L(10 * v, "mm"), [L(100 * v, "mm"), L(v + 10, "mm"), L(v, "mm")],
                   "1 cm = 10 mm, então %d cm = <b>%s</b>." % (v, L(10 * v, "mm")))
    if k == "mm-cm":
        v = R.randint(2, 15)
        return mcq("%s são quantos centímetros?" % L(10 * v, "mm"), L(v, "cm"), [L(10 * v, "cm"), L(100 * v, "cm"), L(v * 100, "mm")],
                   "10 mm = 1 cm, então %s = <b>%s</b>." % (L(10 * v, "mm"), L(v, "cm")))
    m, c = R.randint(1, 3), R.randint(5, 95)
    return mcq("%d m e %d cm são quantos centímetros?" % (m, c), L(100 * m + c, "cm"), [L(m + c, "cm"), L(10 * m + c, "cm"), L(100 * m + c * 10, "cm")],
               "%d m = %d cm; %d + %d = <b>%s</b>." % (m, 100 * m, 100 * m, c, L(100 * m + c, "cm")))


def s4_comparar():
    k = R.choice(["mcm", "cmmm", "ordem"])
    if k == "mcm":
        m = R.randint(1, 3)
        c = 100 * m + R.choice([-30, -10, 10, 20, 50])
        big = "%s" % L(m, "m") if 100 * m > c else L(c, "cm")
        return mcq("O que é mais comprido: %s ou %s?" % (L(m, "m"), L(c, "cm")), big,
                   [L(c, "cm") if big == L(m, "m") else L(m, "m"), "são iguais", "não dá para comparar"],
                   "%s = %s; compare %s com %s: <b>%s</b>." % (L(m, "m"), L(100 * m, "cm"), L(100 * m, "cm"), L(c, "cm"), big))
    if k == "cmmm":
        c = R.randint(2, 9)
        mm = 10 * c + R.choice([-5, -2, 3, 6])
        big = L(c, "cm") if 10 * c > mm else L(mm, "mm")
        return mcq("O que é mais comprido: %s ou %s?" % (L(c, "cm"), L(mm, "mm")), big,
                   [L(mm, "mm") if big == L(c, "cm") else L(c, "cm"), "são iguais", "não dá para comparar"],
                   "%s = %s: <b>%s</b> é mais comprido." % (L(c, "cm"), L(10 * c, "mm"), big))
    m = R.choice([1, 2])
    c1, c2 = 100 * m - R.choice([5, 15, 25, 35]), 100 * m + R.choice([10, 20, 30])
    mmv = (100 * m - R.choice([40, 50, 60])) * 10
    xs = [("%d m" % m, 100 * m), ("%d cm" % c1, c1), ("%d cm" % c2, c2), ("%d mm" % mmv, mmv // 10)]
    R.shuffle(xs)
    ok = " &lt; ".join(x for x, _ in sorted(xs, key=lambda t: t[1]))
    by_num = " &lt; ".join(x for x, _ in sorted(xs, key=lambda t: int(t[0].split()[0])))
    rev = " &lt; ".join(x for x, _ in sorted(xs, key=lambda t: -t[1]))
    sw = sorted(xs, key=lambda t: t[1])
    sw[0], sw[1] = sw[1], sw[0]
    return mcq("Coloque do menor para o maior: %s." % ", ".join(x for x, _ in xs), ok.replace(" m", NB + "m").replace(" cm", NB + "cm").replace(" mm", NB + "mm"),
               [o.replace(" m", NB + "m").replace(" cm", NB + "cm").replace(" mm", NB + "mm") for o in (by_num, rev, " &lt; ".join(x for x, _ in sw))],
               "Passe tudo para centímetros: %d m = %d cm e %d mm = %d cm. Ordem: <b>%s</b>." % (m, 100 * m, mmv, mmv // 10, ok))


def s5_problema():
    p, _ = K.next()
    k = R.choice(["fita", "pulo", "corrida", "cerca", "planta", "tecido"])
    if k == "fita":
        t, u = R.choice([100, 200]), R.randint(15, 65)
        return mcq("%s tinha uma fita de %d cm e usou %d cm num laço. Quantos centímetros sobraram?" % (p, t, u), L(t - u, "cm"), [L(t + u, "cm"), L(t - u + 10, "cm"), L(u, "cm")],
                   "%d − %d = <b>%s</b>." % (t, u, L(t - u, "cm")))
    if k == "pulo":
        a, b = R.randint(95, 140), R.randint(95, 140)
        if a == b:
            return None
        return mcq("No salto em distância, %s pulou %d cm e a amiga pulou %d cm. Qual é a diferença entre os saltos?" % (p, a, b), L(abs(a - b), "cm"),
                   [L(a + b, "cm"), L(abs(a - b) + 10, "cm"), L(abs(a - b) + 1, "cm")], "%d − %d = <b>%s</b>." % (max(a, b), min(a, b), L(abs(a - b), "cm")))
    if k == "corrida":
        v, n = R.choice([50, 100, 200]), R.randint(2, 5)
        return mcq("Uma volta na quadra tem %d m. %s deu %d voltas. Quantos metros correu?" % (v, p, n), L(v * n, "m"), [L(v + n, "m"), L(v * (n + 1), "m"), L(v * n * 10, "m")],
                   "%d × %d = <b>%s</b>." % (n, v, L(v * n, "m")))
    if k == "cerca":
        a, b = R.randint(3, 9), R.randint(2, 6)
        return mcq("Uma horta retangular tem %d m de comprimento e %d m de largura. Quantos metros de cerca são necessários para contorná-la?" % (a, b), L(2 * (a + b), "m"),
                   [L(a + b, "m"), L(a * b, "m"), L(2 * a + b, "m")], "%d + %d + %d + %d = <b>%s</b>." % (a, b, a, b, L(2 * (a + b), "m")))
    if k == "planta":
        a, d, n = R.randint(5, 20), R.randint(2, 5), R.randint(3, 6)
        return mcq("Uma planta tinha %d cm e cresceu %d cm por semana durante %d semanas. Que altura ela tem agora?" % (a, d, n), L(a + d * n, "cm"),
                   [L(a + d, "cm"), L(d * n, "cm"), L(a + d + n, "cm")], "%d + %d × %d = <b>%s</b>." % (a, d, n, L(a + d * n, "cm")))
    m = R.randint(2, 5)
    c = R.randint(1, 3) * 25
    return mcq("Uma costureira tinha %d m de tecido e usou %d cm. Quantos centímetros sobraram?" % (m, c), L(100 * m - c, "cm"),
               [L(m * 10 - c, "cm") if m * 10 > c else L(100 * m + c, "cm"), L(100 * m + c, "cm"), L(m - c if m > c else 100 * m - c + 10, "cm")],
               "%d m = %d cm; %d − %d = <b>%s</b>." % (m, 100 * m, 100 * m, c, L(100 * m - c, "cm")))


def main():
    seen = set()
    sets = [
        ("Unidades e instrumentos", mix(R, seen, [(s1_unidade, 12), (s1_instrumento, 8)])),
        ("Medir com palmos e com a régua", mix(R, seen, [(s2_palmo, 6), (s3_regua, 14)])),
        ("Metro, centímetro e milímetro", mix(R, seen, [(s4_converter, 20)])),
        ("Comparar comprimentos", mix(R, seen, [(s4_comparar, 12), (s3_regua, 8)])),
        ("Problemas de comprimento", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Podemos medir com palmos ou passos, mas cada pessoa encontra um número diferente: <b>o resultado depende da unidade</b>. Por isso usamos unidades padronizadas.",
         "As unidades de comprimento mais usadas são o <b>metro</b> (m), o <b>centímetro</b> (cm) e o <b>milímetro</b> (mm): 1 m = 100 cm e 1 cm = 10 mm.",
         "Para medir com a régua, coloque o começo do objeto no <b>zero</b>. Cada número da régua marca um centímetro; os risquinhos pequenos são milímetros.",
         "Escolha o instrumento: régua para objetos pequenos, fita métrica para contornos, trena para distâncias maiores."],
        [("Quantos centímetros há em 3 m?", ["1 m = 100 cm", "3 × 100"], "300 cm"),
         ("O que é mais comprido: 1 m ou 90 cm?", ["1 m = 100 cm", "100 cm &gt; 90 cm"], "1 m")],
        [["Começar a medir no 1 da régua", "Comece no 0. Se começar em outro número, faça a subtração."],
         ["Achar que 90 cm é mais que 1 m porque 90 &gt; 1", "Compare na mesma unidade: 1 m = 100 cm."],
         ["Achar que dois palmos diferentes dão a mesma medida", "Palmos têm tamanhos diferentes; o metro é igual para todos."]],
        regua(0, 45))
    faq = [("Que medidas de comprimento a BNCC pede no 3º ano?", "Estimar, medir e comparar comprimentos com unidades não padronizadas e padronizadas mais usuais (metro, centímetro e milímetro) e escolher o instrumento adequado."),
           ("Como praticar medidas em casa?", "Peça para a criança medir objetos com a régua e com palmos, comparar os resultados e estimar antes de medir. Uma fita métrica de costura é ótima para isso.")]
    make_unit(R, "medidas-de-comprimento", "M", ["EF03MA17", "EF03MA18", "EF03MA19"],
              "Reconhecer que o resultado de uma medida depende da unidade de medida utilizada; escolher a unidade de medida e o instrumento mais apropriado para medições de comprimento; estimar, medir e comparar comprimentos, utilizando unidades de medida não padronizadas e padronizadas mais usuais (metro, centímetro e milímetro) e diversos instrumentos de medida",
              "Medidas de comprimento: metro, centímetro e milímetro", "Medidas de comprimento",
              "Atividades de matemática para o 3º ano sobre medidas de comprimento: palmos e passos, metro, centímetro e milímetro, régua, trena e fita métrica, transformar e comparar medidas, problemas. 100 exercícios com gabarito.",
              "1 m = 100 cm e 1 cm = 10 mm.", "Na régua, comece no zero.",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
