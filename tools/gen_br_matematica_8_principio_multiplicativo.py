# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Princípio multiplicativo da contagem (Números, EF08MA03)
  python3 tools/gen_br_matematica_8_principio_multiplicativo.py
Contar possibilidades com árvore e tabela; princípio multiplicativo (roupas, cardápios, senhas, placas, números com algarismos
distintos, caminhos); quando a ordem importa e quando há repetição; filas e anagramas pequenos.
Erros: somar em vez de multiplicar, permitir repetição quando não pode, esquecer que o número não pode começar com 0.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, bank, unit

R = random.Random(88003)


def s1_combinar():
    k = R.choice(["roupa", "lanche", "viagem", "time"])
    if k == "roupa":
        a, b, c = R.randint(2, 6), R.randint(2, 5), R.randint(2, 4)
        return M("Com %d camisetas, %d bermudas e %d bonés, de quantas maneiras diferentes uma pessoa pode se vestir usando uma peça de cada?" % (a, b, c), d(a * b * c), [d(a + b + c), d(a * b + c), d(a * b)],
                 "Princípio multiplicativo: %d × %d × %d = <b>%d</b>." % (a, b, c, a * b * c))
    if k == "lanche":
        a, b, c = R.randint(2, 5), R.randint(2, 6), R.randint(2, 4)
        return M("Uma lanchonete oferece %d tipos de pão, %d recheios e %d sucos. Quantos lanches diferentes (pão, recheio e suco) podem ser montados?" % (a, b, c), d(a * b * c), [d(a + b + c), d(a * b), d((a + b) * c)],
                 "%d × %d × %d = <b>%d</b>." % (a, b, c, a * b * c))
    if k == "viagem":
        a, b = R.randint(2, 5), R.randint(2, 5)
        return M("De A para B há %d estradas e de B para C há %d estradas. De quantas maneiras se pode ir de A até C passando por B?" % (a, b), d(a * b), [d(a + b), d(a * b * 2), d(a * a)],
                 "Para cada estrada de A a B, há %d de B a C: %d × %d = <b>%d</b>." % (b, a, b, a * b))
    n = R.randint(4, 9)
    return M("Num clube com %d pessoas, de quantas maneiras se pode escolher um presidente e um vice (pessoas diferentes)?" % n, d(n * (n - 1)), [d(n * n), d(2 * n), d(n * (n - 1) // 2)],
             "%d escolhas para presidente e %d para vice: <b>%d</b>." % (n, n - 1, n * (n - 1)))


def s2_senhas():
    k = R.choice(["rep", "norep", "letras", "placa"])
    if k == "rep":
        n = R.choice([2, 3, 4])
        return M("Quantas senhas de %d algarismos (0 a 9) existem, podendo repetir algarismos?" % n, d(10 ** n), [d(10 * n), d(10 * 9 * 8 * 7 // 10 ** (4 - n)) if n > 1 else "9", d(9 * 10 ** (n - 1))],
                 "10 escolhas em cada posição: 10%s = <b>%s</b>." % ({2: "²", 3: "³", 4: "⁴"}[n], d(10 ** n)))
    if k == "norep":
        n = R.choice([2, 3, 4])
        v = 1
        for i in range(n):
            v *= 10 - i
        return M("Quantas senhas de %d algarismos <b>diferentes</b> (0 a 9) existem?" % n, d(v), [d(10 ** n), d(10 * n), d(v // 2)],
                 "%s = <b>%s</b>." % (" × ".join(str(10 - i) for i in range(n)), d(v)))
    if k == "letras":
        n = R.choice([2, 3])
        return M("Quantos códigos de %d letras (26 letras, podendo repetir) existem?" % n, d(26 ** n), [d(26 * n), d(26 * 25 if n == 2 else 26 * 25 * 24), d(26 + n)],
                 "26 escolhas em cada posição: <b>%s</b>." % d(26 ** n))
    return M("Uma placa tem 2 letras (26 opções cada) seguidas de 2 algarismos (10 opções cada), podendo repetir. Quantas placas diferentes existem?", d(26 * 26 * 100), [d(26 * 2 + 10 * 2), d(26 * 25 * 10 * 9), d(26 * 26 + 100)],
             "26 × 26 × 10 × 10 = <b>%s</b>." % d(26 * 26 * 100))


def s3_numeros():
    ds = sorted(R.sample(range(0, 10), R.choice([3, 4, 5])))
    n = len(ds)
    k = R.choice(["dist", "rep", "pares"])
    has0 = 0 in ds
    if k == "dist":
        v = (n - 1) * (n - 1) * (n - 2) if has0 else n * (n - 1) * (n - 2)
        return M("Com os algarismos %s, quantos números de 3 algarismos <b>distintos</b> podemos formar?" % ", ".join(map(str, ds)), d(v), [d(n * (n - 1) * (n - 2)) if has0 else d(n ** 3), d(n ** 3), d(v + n)],
                 ("O 0 não pode começar: %d × %d × %d" % (n - 1, n - 1, n - 2) if has0 else "%d × %d × %d" % (n, n - 1, n - 2)) + " = <b>%d</b>." % v)
    if k == "rep":
        v = (n - 1) * n * n if has0 else n ** 3
        return M("Com os algarismos %s, quantos números de 3 algarismos podemos formar, <b>podendo repetir</b>?" % ", ".join(map(str, ds)), d(v), [d(n ** 3) if has0 else d(n * (n - 1) * (n - 2)), d(n * (n - 1) * (n - 2)), d(3 * n)],
                 ("O 0 não pode começar: %d × %d × %d" % (n - 1, n, n) if has0 else "%d × %d × %d" % (n, n, n)) + " = <b>%d</b>." % v)
    if has0:
        return None
    ev = [x for x in ds if x % 2 == 0]
    if not ev:
        return None
    v = len(ev) * (n - 1) * (n - 2)
    return M("Com os algarismos %s, quantos números <b>pares</b> de 3 algarismos distintos podemos formar?" % ", ".join(map(str, ds)), d(v), [d(n * (n - 1) * (n - 2)), d(len(ev) * n * n), d(v + len(ev))],
             "Comece pela unidade (par): %d opções; depois %d e %d: <b>%d</b>." % (len(ev), n - 1, n - 2, v))


def s4_filas():
    n = R.randint(3, 6)
    k = R.choice(["fila", "anagrama", "foto"])
    f = 1
    for i in range(2, n + 1):
        f *= i
    if k == "fila":
        return M("De quantas maneiras %d amigos podem formar uma fila?" % n, d(f), [d(n * n), d(n), d(f // 2)], "%s = <b>%d</b>." % (" × ".join(str(i) for i in range(n, 0, -1)), f))
    if k == "anagrama":
        w = R.choice(["SOL", "MAR", "LUA", "RIO", "GATO", "PATO", "BOLA", "MESA", "ROSA", "LIVRO", "CARTA", "FESTA", "PRATO"])
        n = len(w)
        f = 1
        for i in range(2, n + 1):
            f *= i
        if len(set(w)) < n:
            return None
        return M("Quantos anagramas (trocas de ordem das letras) tem a palavra %s?" % w, d(f), [d(n * n), d(n), d(f - 1)], "%d letras diferentes: %s = <b>%d</b>." % (n, " × ".join(str(i) for i in range(n, 0, -1)), f))
    return M("Numa foto, %d pessoas vão ficar lado a lado, mas Ana precisa ficar na ponta esquerda. De quantas maneiras podem se posicionar?" % n, d(f // n), [d(f), d(n - 1), d(f // 2)],
             "Ana fixa; as outras %d se organizam: <b>%d</b>." % (n - 1, f // n))


def main():
    seen = set()
    sets = [
        ("Combinar escolhas", mix(R, seen, [(s1_combinar, 20)])),
        ("Senhas e placas", mix(R, seen, [(s2_senhas, 9), (s1_combinar, 11)])),
        ("Formar números", mix(R, seen, [(s3_numeros, 20)])),
        ("Filas e anagramas", mix(R, seen, [(s4_filas, 18), (s1_combinar, 2)])),
        ("Revisão", mix(R, seen, [(s3_numeros, 14), (s1_combinar, 6)])),
    ]
    body = lesson(
        ["<b>Princípio multiplicativo</b>: se uma escolha tem m opções e outra tem n, as duas juntas têm m × n possibilidades.",
         "Pergunte: <b>pode repetir?</b> Senha com repetição: 10 × 10 × 10. Sem repetição: 10 × 9 × 8.",
         "Números não começam com 0. Comece pelas posições com restrição (primeiro algarismo, número par…).",
         "Filas e anagramas com n elementos diferentes: n × (n − 1) × … × 1."],
        [("Algarismos 0, 1, 2, 3: números de 3 algarismos distintos", ["1º: 3 opções (sem o 0)", "2º: 3", "3º: 2"], "18"),
         ("Fila com 4 pessoas", ["4 × 3 × 2 × 1"], "24")],
        [["Somar em vez de multiplicar", "Escolhas em sequência se multiplicam."],
         ["Repetir quando não pode", "«Distintos» diminui uma opção a cada passo."],
         ["Começar o número com 0", "Trate primeiro a posição com restrição."]])
    faq = [("O que é o princípio multiplicativo?", "Se uma decisão pode ser tomada de m maneiras e, depois dela, outra de n maneiras, as duas juntas podem ser tomadas de m × n maneiras."),
           ("O que a BNCC pede no 8º ano?", "Resolver e elaborar problemas de contagem cuja resolução envolva a aplicação do princípio multiplicativo (EF08MA03).")]
    unit(R, "principio-multiplicativo", "N", ["EF08MA03"],
         "Resolver e elaborar problemas de contagem cuja resolução envolva a aplicação do princípio multiplicativo",
         "Princípio multiplicativo da contagem", "Princípio multiplicativo",
         "Atividades de matemática para o 8º ano sobre o princípio multiplicativo: combinar roupas e cardápios, senhas e placas, formar números, filas e anagramas. 100 exercícios com gabarito.",
         "m opções × n opções = m × n possibilidades.", "Pode repetir? O número pode começar com 0?",
         body, faq, sets, 3, grade="8-ano")


if __name__ == "__main__":
    main()
