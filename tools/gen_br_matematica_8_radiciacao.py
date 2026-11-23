# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Radiciação e potência de expoente fracionário (Números, EF08MA02)
  python3 tools/gen_br_matematica_8_radiciacao.py
Raiz quadrada e cúbica exatas; raiz como operação inversa da potência; potência de expoente fracionário (a^(1/2) = √a, a^(1/3) = ∛a,
a^(2/3)); estimar raízes não exatas entre dois inteiros; raiz de frações e decimais; problemas (lado do quadrado, aresta do cubo).
Usa geradores do 9º ano (números reais) com outro sorteio.
Erros: √16 = 8, ∛27 = 9, √(9 + 16) = √9 + √16, achar que 8^(1/3) = 8/3.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, fq, bank, unit

R = random.Random(88002)
r_entre, r_aprox = use("gen_br_matematica_9_numeros_reais", 88903, "s2_entre", "s2_aprox")


def s1_exatas():
    k = R.choice(["q", "q", "c", "q4"])
    if k == "q":
        n = R.randint(2, 25)
        return M("Quanto é √%s?" % d(n * n), d(n), [d(F(n * n, 2)) if (n * n) % 2 == 0 else d(n + 1), d(n * n * n) if n < 8 else d(n - 1), d(n * 2)], "%d × %d = %s, então √%s = <b>%d</b>." % (n, n, d(n * n), d(n * n), n))
    if k == "c":
        n = R.randint(2, 10) * R.choice([1, 1, -1])
        return M("Quanto é ∛%s?" % d(n ** 3), d(n), [d(F(n ** 3, 3), 1) if (F(n ** 3, 3) * 10).denominator == 1 else d(n * n), d(-n), d(n * 3)], "%s × %s × %s = %s, então ∛%s = <b>%s</b>." % (d(n), d(n), d(n), d(n ** 3), d(n ** 3), d(n)))
    n = R.randint(2, 5)
    return M("Quanto é ⁴√%s?" % d(n ** 4), d(n), [d(n * n), d(F(n ** 4, 4)) if n ** 4 % 4 == 0 else d(n + 1), d(n * 4)], "%d⁴ = %s: <b>%d</b>." % (n, d(n ** 4), n))


def s2_fracionario():
    k = R.choice(["12", "13", "23", "32"])
    if k == "12":
        n = R.randint(2, 15)
        return M("Quanto é %s<sup>1/2</sup>?" % d(n * n), d(n), [d(F(n * n, 2)) if n * n % 2 == 0 else d(n * n * 2), d(n * n * n) if n < 6 else d(n + 2), d(n - 1)], "a<sup>1/2</sup> = √a: √%s = <b>%d</b>." % (d(n * n), n))
    if k == "13":
        n = R.randint(2, 6)
        return M("Quanto é %s<sup>1/3</sup>?" % d(n ** 3), d(n), [d(F(n ** 3, 3), 1) if (F(n ** 3, 3) * 10).denominator == 1 else d(n * n), d(n * n), d(n + 1)], "a<sup>1/3</sup> = ∛a: ∛%s = <b>%d</b>." % (d(n ** 3), n))
    if k == "23":
        n = R.randint(2, 5)
        return M("Quanto é %s<sup>2/3</sup>?" % d(n ** 3), d(n * n), [d(n), d(F(2 * n ** 3, 3), 1) if (F(2 * n ** 3, 3) * 10).denominator == 1 else d(n ** 3 * 2), d(n ** 6) if n ** 6 < 100000 else d(n * n + 1)], "∛%s = %d; %d² = <b>%d</b>." % (d(n ** 3), n, n, n * n))
    n = R.randint(2, 6)
    return M("Quanto é %s<sup>3/2</sup>?" % d(n * n), d(n ** 3), [d(n), d(F(3 * n * n, 2)) if (3 * n * n) % 2 == 0 else d(n ** 3 + n), d(n ** 4)], "√%s = %d; %d³ = <b>%s</b>." % (d(n * n), n, n, d(n ** 3)))


def s3_fr_dec():
    k = R.choice(["fr", "dec"])
    if k == "fr":
        a, b = R.randint(1, 9), R.randint(2, 12)
        if a == b or F(a, b).denominator != b:
            return None
        return M("Quanto é a raiz quadrada de %s?" % fq(F(a * a, b * b)), fq(F(a, b)), [fq(F(a * a, b)) if F(a * a, b) != F(a, b) else fq(F(a, b * b)), fq(F(a, b * b)), fq(F(a * a, 2 * b)) if F(a * a, 2 * b) != F(a, b) else fq(F(b, a))],
                 "Raiz do numerador sobre raiz do denominador: <b>%s</b>." % fq(F(a, b)))
    n = R.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15])
    p = R.choice([1, 2])
    x = F(n * n, 10 ** (2 * p))
    return M("Quanto é √%s?" % d(x), d(F(n, 10 ** p)), [d(F(n * n, 10 ** p * 2)) if (F(n * n, 10 ** p * 2) * 10 ** 4).denominator == 1 else d(F(n, 10 ** (p + 1))), d(F(n, 10 ** (p + 1))), d(F(n, 10 ** p) * 10)],
             "%s × %s = %s: <b>%s</b>." % (d(F(n, 10 ** p)), d(F(n, 10 ** p)), d(x), d(F(n, 10 ** p))))


def s4_problemas():
    k = R.choice(["quad", "cubo", "soma"])
    if k == "quad":
        L = R.randint(3, 30)
        return M("Um terreno quadrado tem %s m² de área. Quanto mede cada lado?" % d(L * L), "%d m" % L, ["%s m" % d(F(L * L, 4)) if (L * L) % 4 == 0 else "%d m" % (L + 2), "%s m" % d(F(L * L, 2)) if (L * L) % 2 == 0 else "%d m" % (L * 2), "%d m" % (L - 1)],
                     "Lado = √%s = <b>%d m</b>." % (d(L * L), L))
    if k == "cubo":
        a = R.randint(2, 12)
        return M("Um cubo tem %s cm³ de volume. Quanto mede a aresta?" % d(a ** 3), "%d cm" % a, ["%s cm" % d(F(a ** 3, 3), 1) if (F(a ** 3, 3) * 10).denominator == 1 else "%d cm" % (a * a), "%d cm" % (a * a), "%d cm" % (a + 1)],
                     "Aresta = ∛%s = <b>%d cm</b>." % (d(a ** 3), a))
    a, b = R.choice([(9, 16), (36, 64), (25, 144), (16, 9), (81, 144), (144, 256)])
    return M("Quanto é √(%d + %d)?" % (a, b), d(int((a + b) ** 0.5)), [d(int(a ** 0.5) + int(b ** 0.5)), d(a + b), d(int((a + b) ** 0.5) + 1)],
             "Primeiro some: √%d = <b>%d</b> (e não √%d + √%d)." % (a + b, int((a + b) ** 0.5), a, b))


def main():
    seen = set()
    sets = [
        ("Raízes exatas", mix(R, seen, [(s1_exatas, 20)])),
        ("Expoente fracionário", mix(R, seen, [(s2_fracionario, 20)])),
        ("Raízes de frações e decimais", mix(R, seen, [(s3_fr_dec, 20)])),
        ("Estimar raízes", mix(R, seen, [(r_entre, 10), (r_aprox, 10)])),
        ("Problemas", mix(R, seen, [(s4_problemas, 20)])),
    ]
    body = lesson(
        ["A <b>raiz</b> é a operação inversa da potência: √49 = 7 porque 7² = 49; ∛64 = 4 porque 4³ = 64.",
         "Potência de expoente fracionário: a<sup>1/2</sup> = √a, a<sup>1/3</sup> = ∛a e a<sup>m/n</sup> = (ⁿ√a)<sup>m</sup>.",
         "Raiz de fração: √(9/25) = 3/5. Raiz de decimal: √0,49 = 0,7.",
         "Quando a raiz não é exata, estime entre dois inteiros: 6² = 36 &lt; 40 &lt; 49 = 7², então √40 está entre 6 e 7."],
        [("8<sup>2/3</sup>", ["∛8 = 2", "2² = 4"], "4"),
         ("√0,0081", ["0,09 × 0,09 = 0,0081"], "0,09")],
        [["√16 = 8", "8 × 8 = 64; √16 = 4."],
         ["√(9 + 16) = √9 + √16", "√25 = 5, não 3 + 4."],
         ["8<sup>1/3</sup> = 8/3", "8<sup>1/3</sup> = ∛8 = 2."]])
    faq = [("O que significa um expoente fracionário?", "a<sup>1/n</sup> é a raiz de índice n de a; a<sup>m/n</sup> é essa raiz elevada a m. Por exemplo, 27<sup>2/3</sup> = (∛27)² = 9."),
           ("O que a BNCC pede no 8º ano?", "Resolver e elaborar problemas usando a relação entre potenciação e radiciação, para representar uma raiz como potência de expoente fracionário (EF08MA02).")]
    unit(R, "radiciacao", "N", ["EF08MA02"],
         "Resolver e elaborar problemas usando a relação entre potenciação e radiciação, para representar uma raiz como potência de expoente fracionário",
         "Radiciação e potência de expoente fracionário", "Radiciação",
         "Atividades de matemática para o 8º ano sobre radiciação: raízes quadradas e cúbicas exatas, potência de expoente fracionário, raízes de frações e decimais, estimativas e problemas. 100 exercícios com gabarito.",
         "a^(1/n) = raiz de índice n de a", "√49 = 7 porque 7² = 49.",
         body, faq, sets, 2, grade="8-ano")


if __name__ == "__main__":
    main()
