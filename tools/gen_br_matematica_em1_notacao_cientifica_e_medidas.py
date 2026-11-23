# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Notação científica, algarismos significativos e medidas (EM13MAT313, EM13MAT103)
  python3 tools/gen_br_matematica_em1_notacao_cientifica_e_medidas.py
Notação científica e operações; ordem de grandeza; algarismos significativos e arredondamento; erro de uma medição
(precisão do instrumento); unidades de informática (bit, byte, kB, MB, GB) e tempo de download (Mbps).
Usa geradores do 9º ano (operações em notação científica, bytes) com outro sorteio.
Erros: contar os zeros à esquerda como significativos, confundir bit e byte (8 bits = 1 byte), esquecer que toda medida tem erro.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, num, unit

R = random.Random(91001)
nc_oper, nc_prob = use("gen_br_matematica_9_notacao_cientifica", 91901, "s4_operar", "s5_problema")
u_bytes = use("gen_br_matematica_9_unidades_de_medida_muito_grandes_e_pequenas", 91902, "s4_bytes")
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def p10(e):
    return "10" + str(e).translate(SUP).replace("⁻", "⁻")


def nc(m, e):
    return "%s · %s" % (d(m), p10(e))


def s1_ordem():
    k = R.randint(1, 9)
    m = F(R.randint(10, 99), 10)
    e = R.choice([x for x in range(-8, 13) if x])
    og = e + (1 if m >= F(316, 100) else 0)
    return M("Qual é a ordem de grandeza de %s? (Use 3,16 como limite.)" % nc(m, e), p10(og), [p10(e), p10(og + 1), p10(og - 1), p10(og + 2)],
             "%s %s 3,16, então a ordem de grandeza é <b>%s</b>." % (d(m), "≥" if m >= F(316, 100) else "<", p10(og)))


def sig_count(s):
    t = s.replace(",", "").lstrip("0")
    return len(t)


def s2_sig():
    k = R.choice(["contar", "contar", "arred"])
    if k == "contar":
        form = R.choice(["int", "dec0", "dec", "small"])
        if form == "int":
            s = str(R.randint(1, 9)) + "".join(str(R.randint(0, 9)) for _ in range(R.randint(1, 3)))
            s = s + "," + str(R.randint(0, 9))
        elif form == "dec0":
            s = str(R.randint(1, 99)) + "," + str(R.randint(1, 9)) + "0"
        elif form == "dec":
            s = str(R.randint(1, 9)) + "," + "".join(str(R.randint(0, 9)) for _ in range(R.randint(2, 3)))
        else:
            s = "0," + "0" * R.randint(1, 3) + str(R.randint(1, 9)) + str(R.randint(0, 9)) + ("0" if R.random() < 0.5 else "")
        n = sig_count(s)
        tot = len(s.replace(",", ""))
        return M("Quantos algarismos significativos tem a medida %s m?" % s, str(n), [str(tot) if tot != n else str(n + 1), str(n - 1), str(len(s.split(",")[1]))],
                 "Os zeros à esquerda não contam; os outros algarismos, inclusive zeros no fim depois da vírgula, contam: <b>%d</b>." % n)
    v = F(R.randint(10000, 99999), 1000)
    n = R.choice([2, 3])
    e = 0
    x = v
    while x >= 10:
        x /= 10
        e += 1
    places = n - 1 - e
    r = d(v, places, keep=True) if places > 0 else num(round(v))
    return M("Arredonde %s para %d algarismos significativos." % (d(v), n), r, [d(v, places + 1, keep=True) if places + 1 > 0 else d(v, 1, keep=True), d(int(v)), d(v, max(places - 1, 0), keep=True)],
             "Mantemos %d algarismos e olhamos o seguinte: <b>%s</b>." % (n, r))


def s3_erro():
    k = R.choice(["regua", "intervalo", "soma"])
    if k == "regua":
        inst, men, un = R.choice([("uma régua com marcas de milímetro", F(1, 10), "cm"), ("uma trena com marcas de centímetro", F(1, 100), "m"), ("uma balança que mostra décimos de grama", F(1, 10), "g"),
                                  ("um termômetro com marcas de 1 °C", 1, "°C"), ("um cronômetro que mostra centésimos de segundo", F(1, 100), "s")])
        return M("Qual é a menor divisão (precisão) de %s?" % inst, "%s %s" % (d(men), un), ["%s %s" % (d(F(men) * 10), un), "%s %s" % (d(F(men) / 10), un), "não há erro na medida"],
                 "A precisão é a menor divisão do instrumento: <b>%s %s</b>." % (d(men), un))
    if k == "intervalo":
        v = F(R.randint(100, 999), 10)
        er = R.choice([F(1, 10), F(5, 100), F(2, 10)])
        return M("Uma medida foi registrada como (%s ± %s) cm. Entre quais valores está a medida real?" % (d(v), d(er)), "entre %s cm e %s cm" % (d(v - er), d(v + er)), ["exatamente %s cm" % d(v), "entre %s cm e %s cm" % (d(v), d(v + er)), "entre %s cm e %s cm" % (d(v - 2 * er), d(v + 2 * er))],
                 "%s − %s e %s + %s: <b>entre %s cm e %s cm</b>." % (d(v), d(er), d(v), d(er), d(v - er), d(v + er)))
    n = R.choice([2, 3, 4])
    er = R.choice([F(1, 10), F(5, 100), F(1, 2), F(2, 10)])
    lados = {2: "Dois lados", 3: "Três lados", 4: "Quatro lados"}[n]
    return M("%s de uma figura foram medidos, cada um com erro de ± %s cm. Qual é o erro máximo da soma (perímetro)?" % (lados, d(er)), "± %s cm" % d(er * n), ["± %s cm" % d(er), "± %s cm" % d(er / n) if (er / n * 1000).denominator == 1 else "± 0 cm", "± %s cm" % d(er * n * 2)],
             "Os erros podem se somar: %d × %s = <b>± %s cm</b>." % (n, d(er), d(er * n)))


def s4_download():
    k = R.choice(["tempo", "bits", "cabem"])
    if k == "tempo":
        mb = R.choice([50, 100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000])
        mbps = R.choice([10, 20, 25, 40, 50, 80, 100, 200])
        t = F(mb * 8, mbps)
        if t.denominator != 1:
            return None
        return M("Um arquivo de %s MB será baixado numa internet de %d Mbps (megabits por segundo). Quanto tempo leva, no mínimo?" % (num(mb), mbps), "%s s" % num(t), ["%s s" % d(F(mb, mbps)), "%s s" % num(t * 8), "%s s" % num(mb * mbps) if mb * mbps < 10 ** 6 else "%s s" % num(t + 10)],
                 "%s MB = %s Mb (1 byte = 8 bits); %s ÷ %d = <b>%s s</b>." % (num(mb), num(mb * 8), num(mb * 8), mbps, num(t)))
    if k == "bits":
        n = R.choice([2, 4, 5, 10, 16, 32, 64, 100, 128])
        return M("Quantos bits há em %d bytes?" % n, num(n * 8), [num(n), num(n * 10), num(n // 8) if n >= 8 and n % 8 == 0 else num(n * 4)],
                 "1 byte = 8 bits: %d × 8 = <b>%s</b>." % (n, num(n * 8)))
    gb = R.choice([16, 32, 64, 128, 256])
    mb = R.choice([2, 4, 5, 8])
    n = gb * 1000 // mb
    return M("Um cartão de memória tem %d GB livres. Quantas fotos de %d MB cabem nele, aproximadamente? (Use 1 GB = 1.000 MB.)" % (gb, mb), num(n), [num(gb // mb) if gb // mb else "1", num(n * 10), num(gb * mb)],
             "%d GB = %s MB; %s ÷ %d = <b>%s</b>." % (gb, num(gb * 1000), num(gb * 1000), mb, num(n)))


s5_conceitos = bank(R, [
    ("Toda medida feita com um instrumento…", "tem um erro (incerteza)", ["é exata", "não tem algarismos significativos", "tem sempre 3 algarismos"]),
    ("Na medida 0,0052 kg, os zeros à esquerda…", "não são significativos", ["são significativos", "mostram o erro", "devem ser apagados da medida"]),
    ("A medida 2,50 m indica precisão de…", "centésimos de metro (1 cm)", ["décimos de metro", "metros", "milímetros"]),
    ("1 byte tem…", "8 bits", ["10 bits", "1.000 bits", "2 bits"]),
    ("A velocidade da internet costuma ser dada em…", "megabits por segundo (Mbps)", ["megabytes por hora", "quilômetros por hora", "gigabytes"]),
    ("Um algarismo duvidoso é…", "o último algarismo de uma medida, que foi estimado", ["o primeiro algarismo", "um zero à esquerda", "um erro de cálculo"]),
    ("Medir com uma régua comum (marcas de mm) e escrever 12,347 cm é…", "incorreto: a régua não tem essa precisão", ["correto", "mais preciso e por isso melhor", "obrigatório"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Operações em notação científica", mix(R, seen, [(nc_oper, 14), (s1_ordem, 6)])),
        ("Ordem de grandeza e problemas", mix(R, seen, [(s1_ordem, 10), (nc_prob, 10)])),
        ("Algarismos significativos", mix(R, seen, [(s2_sig, 16), (s5_conceitos, 4)])),
        ("Erro de uma medição", mix(R, seen, [(s3_erro, 17), (s5_conceitos, 3)])),
        ("Unidades de informática", mix(R, seen, [(s4_download, 12), (u_bytes, 8)])),
    ]
    body = lesson(
        ["<b>Notação científica</b>: a · 10ⁿ com 1 ≤ a < 10. Para multiplicar, multiplique os números e some os expoentes.",
         "<b>Ordem de grandeza</b>: a potência de 10 mais próxima. Se a ≥ 3,16, use 10ⁿ⁺¹; se não, 10ⁿ.",
         "<b>Algarismos significativos</b>: todos os algarismos de uma medida, menos os zeros à esquerda. O último é o duvidoso.",
         "Toda medida tem <b>erro</b>: a precisão é a menor divisão do instrumento.",
         "Informática: 1 byte = 8 bits; 1 kB = 1.000 bytes, 1 MB = 1.000 kB, 1 GB = 1.000 MB. A internet é medida em bits por segundo."],
        [("Algarismos significativos de 0,0250", ["zeros à esquerda não contam: 2, 5, 0"], "3"),
         ("Baixar 100 MB a 20 Mbps", ["100 MB = 800 Mb", "800 ÷ 20"], "40 s")],
        [["Contar os zeros à esquerda", "Em 0,005, só o 5 é significativo."],
         ["Confundir MB com Mb", "B (byte) = 8 b (bits). Converta antes de dividir."],
         ["Escrever mais casas do que o instrumento mede", "Use a precisão do instrumento."]])
    faq = [("O que são algarismos significativos?", "São os algarismos de uma medida que têm significado: todos os algarismos corretos mais o último, que é estimado (duvidoso). Zeros à esquerda não são significativos."),
           ("O que a BNCC pede?", "Utilizar os conceitos básicos de uma linguagem de medidas, com notação científica, algarismos significativos e algarismos duvidosos, reconhecendo que toda medida é aproximada (EM13MAT313), e interpretar textos com unidades de medida, inclusive de informática, como capacidade de armazenamento e velocidade de transferência de dados (EM13MAT103).")]
    unit(R, "notacao-cientifica-e-medidas", "M", ["EM13MAT313", "EM13MAT103"],
         "Utilizar, quando necessário, a notação científica para expressar uma medida, compreendendo as noções de algarismos significativos e algarismos duvidosos, e reconhecendo que toda medida é inevitavelmente acompanhada de erro; interpretar e compreender textos científicos ou divulgados pelas mídias, que empregam unidades de medida de diferentes grandezas e as conversões possíveis entre elas, como as de armazenamento e velocidade de transferência de dados",
         "Notação científica, algarismos significativos e medidas", "Notação científica e medidas",
         "Atividades de matemática para a 1ª série do Ensino Médio: notação científica, ordem de grandeza, algarismos significativos, erro de medição, bytes e tempo de download. 100 exercícios com gabarito.",
         "Toda medida tem erro", "Algarismos significativos: zeros à esquerda não contam.",
         body, faq, sets, 1, grade="1-serie")


if __name__ == "__main__":
    main()
