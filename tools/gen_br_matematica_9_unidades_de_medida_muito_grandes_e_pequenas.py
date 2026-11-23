# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Unidades de medida muito grandes e muito pequenas (Grandezas e medidas, EF09MA18)
  python3 tools/gen_br_matematica_9_unidades_de_medida_muito_grandes_e_pequenas.py
Prefixos (quilo, mega, giga, tera, mili, micro, nano) e potências de 10; ano-luz e unidade astronômica; micrômetro e
nanômetro (células, vírus, fios de cabelo); bytes (kB, MB, GB, TB) e armazenamento; conversões com notação científica.
Erros: contar errado os zeros, dividir quando é para multiplicar, confundir micro (10⁻⁶) com nano (10⁻⁹).
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, unit

R = random.Random(89018)
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
PRE = [("tera", "T", 12), ("giga", "G", 9), ("mega", "M", 6), ("quilo", "k", 3), ("mili", "m", -3), ("micro", "µ", -6), ("nano", "n", -9)]


def p10(e):
    return "10" + str(e).translate(SUP)


def nc(a, e):
    return "%s × %s" % (d(a), p10(e))


def s1_prefixo():
    nome, sim, e = R.choice(PRE)
    k = R.choice(["valor", "nome"])
    if k == "valor":
        return M("O prefixo <b>%s</b> (%s) significa multiplicar por…" % (nome, sim), p10(e), [p10(-e), p10(e + 3) if e != 9 else p10(6), p10(e - 3) if e != -9 else p10(-6), p10(e * 2) if abs(e) < 9 else p10(e // 3)],
                 "%s = <b>%s</b>." % (nome, p10(e)))
    return M("Qual prefixo indica %s?" % p10(e), "%s (%s)" % (nome, sim), ["%s (%s)" % (n, s) for n, s, x in PRE if x != e],
             "%s = <b>%s</b>." % (p10(e), nome))


def s2_espaco():
    k = R.choice(["al", "ua", "luz", "terra"])
    if k == "al":
        n = R.choice([2, 4, 5, 8, 10, 20, 100])
        return M("Um ano-luz é cerca de 9,5 × 10¹² km. Uma estrela está a %d anos-luz. Qual é a distância aproximada em km?" % n, nc(*norm(F(95, 10) * n, 12)),
                 [nc(F(95, 10) + n, 12) if F(95, 10) + n < 10 else nc(*norm(F(95, 10) + n, 12)), nc(*norm(F(95, 10) * n, 13)), nc(*norm(F(95, 10) * n, 11))],
                 "%d · 9,5 × 10¹² = %s × 10¹² = <b>%s km</b>." % (n, d(F(95, 10) * n), nc(*norm(F(95, 10) * n, 12))))
    if k == "ua":
        n = R.choice([F(5, 10), 2, 5, F(52, 10), 10, F(95, 10), 30])
        return M("A unidade astronômica (UA) é a distância média da Terra ao Sol, cerca de 1,5 × 10⁸ km. Um planeta está a %s UA do Sol. Qual é a distância em km?" % d(n), nc(*norm(F(15, 10) * n, 8)),
                 [nc(*norm(F(15, 10) * n, 9)), nc(*norm(F(15, 10) * n, 7)), nc(*norm(F(15, 10) + n, 8))],
                 "%s · 1,5 × 10⁸ = <b>%s km</b>." % (d(n), nc(*norm(F(15, 10) * n, 8))))
    if k == "luz":
        return M("A luz percorre cerca de 3 × 10⁵ km por segundo. Quantos km ela percorre em %d segundos?" % (s := R.choice([10, 100, 500, 1000, 60, 20])), nc(*norm(3 * s, 5)),
                 [nc(*norm(3 * s, 4)), nc(*norm(3 + s, 5)) if 3 + s < 10 else nc(*norm(3 * s, 6)), nc(*norm(F(3, s), 5))],
                 "%d · 3 × 10⁵ = <b>%s km</b>." % (s, nc(*norm(3 * s, 5))))
    q, a, w = R.choice([("Qual unidade é mais adequada para medir a distância entre estrelas?", "ano-luz", ["metro", "nanômetro", "gigabyte"]),
                        ("Qual unidade é mais adequada para medir a distância entre os planetas do sistema solar?", "unidade astronômica (UA)", ["milímetro", "micrômetro", "megabyte"]),
                        ("Um ano-luz mede…", "uma distância", ["um tempo", "uma velocidade", "uma massa"]),
                        ("A distância da Terra à Lua é cerca de 384.000 km. Em notação científica:", "3,84 × 10⁵ km", ["3,84 × 10⁴ km", "38,4 × 10⁶ km", "3,84 × 10⁶ km"])])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def norm(a, e):
    a = F(a)
    while a >= 10:
        a /= 10
        e += 1
    while a < 1:
        a *= 10
        e -= 1
    return a, e


def s3_pequeno():
    k = R.choice(["conv", "conv", "objeto", "quantos"])
    if k == "conv":
        n = R.choice([2, 5, 8, 15, 20, 50, 75, 100, 120, 250])
        u, e = R.choice([("µm", -6), ("nm", -9), ("mm", -3)])
        nome = {"µm": "micrômetros", "nm": "nanômetros", "mm": "milímetros"}[u]
        return M("Quanto são %d %s (%s) em metros, em notação científica?" % (n, nome, u), nc(*norm(n, e)) + " m", [nc(*norm(n, -e)) + " m", nc(*norm(n, e - 1)) + " m", nc(*norm(n, e + 1)) + " m"],
                 "1 %s = %s m; %d %s = %d × %s = <b>%s m</b>." % (u, p10(e), n, u, n, p10(e), nc(*norm(n, e))))
    if k == "objeto":
        q, a, w = R.choice([("Uma célula humana típica tem cerca de 10 micrômetros. Isso é quanto em metros?", "1 × 10⁻⁵ m", ["1 × 10⁻⁶ m", "1 × 10⁻⁴ m", "1 × 10⁵ m"]),
                            ("Um vírus mede cerca de 100 nanômetros. Isso é quanto em metros?", "1 × 10⁻⁷ m", ["1 × 10⁻⁹ m", "1 × 10⁻⁸ m", "1 × 10⁷ m"]),
                            ("Um fio de cabelo tem cerca de 0,07 mm de espessura. Em metros:", "7 × 10⁻⁵ m", ["7 × 10⁻² m", "7 × 10⁻⁴ m", "7 × 10⁵ m"]),
                            ("Uma bactéria mede cerca de 2 µm. Em metros:", "2 × 10⁻⁶ m", ["2 × 10⁻⁹ m", "2 × 10⁻³ m", "2 × 10⁶ m"]),
                            ("Qual unidade é mais adequada para medir um vírus?", "nanômetro", ["quilômetro", "metro", "ano-luz"]),
                            ("Qual unidade é mais adequada para medir uma célula?", "micrômetro", ["quilômetro", "ano-luz", "terabyte"]),
                            ("Um grão de areia fina tem 0,1 mm. Em micrômetros:", "100 µm", ["10 µm", "1.000 µm", "1 µm"]),
                            ("1 milímetro tem quantos micrômetros?", "1.000", ["100", "10", "1.000.000"]),
                            ("1 micrômetro tem quantos nanômetros?", "1.000", ["100", "1.000.000", "10"])])
        return M(q, a, w, "Resposta: <b>%s</b>." % a)
    big, small = R.choice([(F(1, 1000), F(1, 10 ** 6)), (F(1, 10 ** 6), F(1, 10 ** 9)), (F(1, 1000), F(1, 10 ** 9))])
    n = R.choice([2, 5, 10, 20, 50])
    nm = {F(1, 1000): ("mm", "milímetros"), F(1, 10 ** 6): ("µm", "micrômetros"), F(1, 10 ** 9): ("nm", "nanômetros")}
    r = n * big / small
    return M("Quantos %s cabem em %d %s?" % (nm[small][1], n, nm[big][1]), d(r), [d(r / 1000), d(r * 1000), d(n * 1000) if r != n * 1000 else d(n * 100)],
             "1 %s = %s %s; %d · %s = <b>%s</b>." % (nm[big][0], d(big / small), nm[small][0], n, d(big / small), d(r)))


def s4_bytes():
    k = R.choice(["conv", "fotos", "nome"])
    if k == "conv":
        u1, u2, e = R.choice([("GB", "MB", 3), ("TB", "GB", 3), ("MB", "kB", 3), ("TB", "MB", 6), ("GB", "kB", 6)])
        n = R.choice([2, 4, 8, 16, 32, 64, 128, 256, 500])
        return M("Usando 1 kB = 1.000 bytes (prefixos do Sistema Internacional), quantos %s há em %d %s?" % (u2, n, u1), d(n * 10 ** e), [d(n * 10 ** (e - 3)) if e > 3 else d(n * 100), d(n * 10 ** (e + 3)), d(n * 10 ** e // 10)],
                     "Cada degrau (k → M → G → T) multiplica por 1.000: %d · %s = <b>%s</b>." % (n, d(10 ** e), d(n * 10 ** e)))
    if k == "fotos":
        cap, unit_, foto = R.choice([(16, "GB", 4), (32, "GB", 8), (64, "GB", 4), (128, "GB", 5), (1, "TB", 5), (8, "GB", 2)])
        tot = cap * (1000 if unit_ == "GB" else 10 ** 6)
        n = tot // foto
        return M("Um cartão de memória tem %d %s. Cada foto ocupa %d MB. Quantas fotos cabem, no máximo? (Use 1 GB = 1.000 MB.)" % (cap, unit_, foto), d(n), [d(cap * foto), d(n * 10), d(n // 10), d(tot * foto)],
                 "%d %s = %s MB; %s ÷ %d = <b>%s fotos</b>." % (cap, unit_, d(tot), d(tot), foto, d(n)))
    q, a, w = R.choice([("Qual é maior: 1 TB ou 1.000 GB (usando 1 TB = 1.000 GB)?", "são iguais", ["1 TB", "1.000 GB", "não dá para comparar"]),
                        ("Um gigabyte (GB) tem quantos bytes, usando o Sistema Internacional?", "10⁹", ["10⁶", "10¹²", "10³"]),
                        ("Um terabyte (TB) tem quantos bytes, usando o Sistema Internacional?", "10¹²", ["10⁹", "10⁶", "10¹⁵"]),
                        ("Um arquivo de 2.500 kB tem quantos MB?", "2,5 MB", ["25 MB", "250 MB", "0,25 MB"]),
                        ("Um vídeo tem 1,2 GB. Quantos MB ele tem?", "1.200 MB", ["120 MB", "12 MB", "12.000 MB"]),
                        ("Um computador tem 512 GB de armazenamento. Isso é quanto em TB?", "0,512 TB", ["5,12 TB", "51,2 TB", "512.000 TB"])])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def s5_comparar():
    a1, e1 = R.randint(1, 9), R.randint(-9, 12)
    a2, e2 = R.randint(1, 9), R.randint(-9, 12)
    if (a1, e1) == (a2, e2) or e1 == e2:
        return None
    big = nc(a1, e1) if e1 > e2 else nc(a2, e2)
    return M("Qual medida é maior: %s m ou %s m?" % (nc(a1, e1), nc(a2, e2)), big + " m", [(nc(a2, e2) if e1 > e2 else nc(a1, e1)) + " m", "são iguais", "não dá para comparar"],
             "Compare os expoentes: o maior expoente dá a maior medida: <b>%s m</b>." % big)


def main():
    seen = set()
    sets = [
        ("Prefixos e potências de 10", mix(R, seen, [(s1_prefixo, 14), (s5_comparar, 6)])),
        ("Medidas no espaço", mix(R, seen, [(s2_espaco, 20)])),
        ("Medidas muito pequenas", mix(R, seen, [(s3_pequeno, 20)])),
        ("Armazenamento de dados", mix(R, seen, [(s4_bytes, 20)])),
        ("Revisão", mix(R, seen, [(s5_comparar, 10), (s3_pequeno, 6), (s4_bytes, 4)])),
    ]
    body = lesson(
        ["Para medidas muito grandes ou muito pequenas usamos <b>prefixos</b> e <b>potências de 10</b>.",
         "Grandes: quilo (10³), mega (10⁶), giga (10⁹), tera (10¹²). Pequenos: mili (10⁻³), micro (10⁻⁶), nano (10⁻⁹).",
         "No espaço usamos a <b>unidade astronômica</b> (≈ 1,5 × 10⁸ km) e o <b>ano-luz</b> (≈ 9,5 × 10¹² km). Células se medem em micrômetros; vírus, em nanômetros.",
         "Em computadores, a capacidade se mede em bytes: kB, MB, GB, TB (cada um é 1.000 vezes o anterior no Sistema Internacional)."],
        [("4 anos-luz", ["4 · 9,5 × 10¹² = 38 × 10¹²"], "3,8 × 10¹³ km"),
         ("50 nm em metros", ["50 × 10⁻⁹"], "5 × 10⁻⁸ m")],
        [["Contar errado os zeros", "Use as potências de 10 em vez de escrever os zeros."],
         ["Confundir micro com nano", "Micro é 10⁻⁶; nano é 10⁻⁹."],
         ["Esquecer de ajustar a notação científica", "38 × 10¹² = 3,8 × 10¹³."]])
    faq = [("O que é um ano-luz?", "É a distância que a luz percorre em um ano, cerca de 9,5 trilhões de quilômetros (9,5 × 10¹² km). Apesar do nome, é uma medida de distância, não de tempo."),
           ("Por que 1 GB às vezes aparece como 1.024 MB?", "Na computação também se usa a base 2 (1.024 = 2¹⁰). O Sistema Internacional usa 1.000. Nas atividades, usamos 1.000, e o enunciado sempre indica.")]
    unit(R, "unidades-de-medida-muito-grandes-e-pequenas", "M", ["EF09MA18"],
         "Reconhecer e empregar unidades usadas para expressar medidas muito grandes ou muito pequenas, tais como distância entre planetas e sistemas solares, tamanho de vírus ou de células, capacidade de armazenamento de computadores, entre outros",
         "Unidades de medida muito grandes e muito pequenas", "Medidas muito grandes e pequenas",
         "Atividades de matemática para o 9º ano sobre unidades de medida muito grandes e muito pequenas: prefixos, ano-luz, unidade astronômica, micrômetro, nanômetro e armazenamento em bytes. 100 exercícios com gabarito.",
         "Prefixos são potências de 10.", "giga = 10⁹, micro = 10⁻⁶, nano = 10⁻⁹",
         body, faq, sets, 18)


if __name__ == "__main__":
    main()
