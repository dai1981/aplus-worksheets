# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Problemas de adição e subtração (Números, EF03MA06)
  python3 tools/gen_br_matematica_3_problemas_de_adicao_e_subtracao.py
Os seis significados da BNCC: juntar, acrescentar, separar, retirar, comparar e completar; escolher a operação;
problemas de duas etapas; dados desnecessários; transformação desconhecida.
Erros: somar sempre que aparece «mais», trocar a ordem na subtração, resolver só a primeira etapa.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, Kids, o, reais

R = random.Random(80306)
K = Kids(R)


def wr(r, a, b, extra=()):
    return [num(x) for x in (a + b, abs(a - b), r + 10, r - 10, r + 1) + tuple(extra) if x != r and x > 0]


def s1_juntar():
    k = R.choice(["frutas", "turma", "figurinhas", "ovos"])
    if k == "frutas":
        a, b = R.randint(120, 480), R.randint(120, 480)
        return mcq("Na feira, um barraqueiro tem %s laranjas e %s mangas. Quantas frutas ele tem ao todo?" % (num(a), num(b)), num(a + b), wr(a + b, a, b),
                   "Juntar: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "turma":
        a, b = R.randint(12, 19), R.randint(12, 19)
        return mcq("Numa turma há %d meninas e %d meninos. Quantos alunos há na turma?" % (a, b), str(a + b), wr(a + b, a, b),
                   "Juntar: %d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "figurinhas":
        (p1, _), (p2, _) = K.two()
        a, b = R.randint(45, 180), R.randint(45, 180)
        return mcq("%s tem %d figurinhas e %s tem %d. Quantas figurinhas há ao todo?" % (p1, a, p2, b), num(a + b), wr(a + b, a, b),
                   "Juntar: %d + %d = <b>%s</b>." % (a, b, num(a + b)))
    a, b = R.randint(130, 600), R.randint(130, 600)
    return mcq("Um sítio recolheu %s ovos brancos e %s ovos vermelhos. Quantos ovos recolheu?" % (num(a), num(b)), num(a + b), wr(a + b, a, b),
               "Juntar: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))


def s1_acrescentar():
    p, _ = K.next()
    k = R.choice(["cofre", "livros", "pontos", "plantas"])
    a, b = R.randint(120, 650), R.randint(30, 340)
    if k == "cofre":
        return mcq("%s tinha %s no cofrinho e colocou mais %s. Quanto tem agora?" % (p, reais(a * 100), reais(b * 100)), reais((a + b) * 100),
                   [reais(x * 100) for x in (a - b, a + b + 10, a + b - 10, a + b + 100)],
                   "Acrescentar: %d + %d = %d: <b>%s</b>." % (a, b, a + b, reais((a + b) * 100)))
    if k == "livros":
        return mcq("A biblioteca da escola tinha %s livros e ganhou mais %s. Quantos livros tem agora?" % (num(a), num(b)), num(a + b), wr(a + b, a, b),
                   "Acrescentar: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "pontos":
        return mcq("%s tinha %s pontos num jogo e ganhou mais %s. Com quantos pontos ficou?" % (p, num(a), num(b)), num(a + b), wr(a + b, a, b),
                   "Acrescentar: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    return mcq("Um viveiro tinha %s mudas e recebeu mais %s. Quantas mudas tem agora?" % (num(a), num(b)), num(a + b), wr(a + b, a, b),
               "Acrescentar: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))


def s2_retirar():
    p, _ = K.next()
    k = R.choice(["balas", "pao", "agua", "lapis"])
    a = R.randint(150, 900)
    b = R.randint(40, a - 30)
    if k == "balas":
        return mcq("Uma loja tinha %s pacotes de balas e vendeu %s. Quantos pacotes sobraram?" % (num(a), num(b)), num(a - b), wr(a - b, a, b),
                   "Retirar: %s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    if k == "pao":
        return mcq("Uma padaria fez %s pães e vendeu %s até o meio-dia. Quantos pães restam?" % (num(a), num(b)), num(a - b), wr(a - b, a, b),
                   "Retirar: %s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    if k == "agua":
        return mcq("Uma caixa-d’água tinha %s litros. Foram gastos %s litros. Quantos litros sobraram?" % (num(a), num(b)), num(a - b) + " litros",
                   [x + " litros" for x in wr(a - b, a, b)], "Retirar: %s − %s = <b>%s litros</b>." % (num(a), num(b), num(a - b)))
    x = R.randint(18, 36)
    y = R.randint(4, x - 6)
    return mcq("%s tinha %d lápis de cor e deu %d para a irmã. Com quantos ficou?" % (p, x, y), str(x - y), wr(x - y, x, y),
               "Retirar: %d − %d = <b>%d</b>." % (x, y, x - y))


def s2_separar():
    k = R.choice(["bolas", "alunos", "carros"])
    t = R.randint(120, 900)
    a = R.randint(30, t - 30)
    if k == "bolas":
        return mcq("Numa caixa há %s bolinhas: %s são azuis e as outras são verdes. Quantas são verdes?" % (num(t), num(a)), num(t - a), wr(t - a, t, a),
                   "Separar: %s − %s = <b>%s</b> verdes." % (num(t), num(a), num(t - a)))
    if k == "alunos":
        return mcq("Uma escola tem %s alunos. %s estudam de manhã e os outros à tarde. Quantos estudam à tarde?" % (num(t), num(a)), num(t - a), wr(t - a, t, a),
                   "Separar: %s − %s = <b>%s</b>." % (num(t), num(a), num(t - a)))
    return mcq("Num estacionamento há %s carros. %s são brancos. Quantos não são brancos?" % (num(t), num(a)), num(t - a), wr(t - a, t, a),
               "Separar: %s − %s = <b>%s</b>." % (num(t), num(a), num(t - a)))


def s3_comparar():
    (p1, g1), (p2, _) = K.two()
    k = R.choice(["mais", "menos", "altura", "km"])
    a = R.randint(300, 980)
    b = R.randint(100, a - 20)
    if k == "mais":
        return mcq("%s fez %s pontos e %s fez %s. Quantos pontos %s fez a mais?" % (p1, num(a), p2, num(b), p1), num(a - b), wr(a - b, a, b),
                   "Comparar: %s − %s = <b>%s</b> pontos a mais." % (num(a), num(b), num(a - b)))
    if k == "menos":
        return mcq("Uma loja vendeu %s sorvetes no sábado e %s no domingo. Quantos sorvetes vendeu a menos no domingo?" % (num(a), num(b)), num(a - b), wr(a - b, a, b),
                   "Comparar: %s − %s = <b>%s</b> a menos." % (num(a), num(b), num(a - b)))
    if k == "altura":
        x, y = R.randint(120, 145), R.randint(98, 119)
        return mcq("%s tem %d cm de altura e %s tem %d cm. Quantos centímetros %s é mais alt%s?" % (p1, x, p2, y, p1, "a" if g1 == "ela" else "o"),
                   "%d cm" % (x - y), ["%d cm" % v for v in (x + y, x - y + 10, x - y - 1) if v != x - y],
                   "Comparar: %d − %d = <b>%d cm</b>." % (x, y, x - y))
    return mcq("De ônibus, a cidade A fica a %s km e a cidade B fica a %s km. Quantos quilômetros a cidade A fica mais longe?" % (num(a), num(b)), num(a - b) + " km",
               [x + " km" for x in wr(a - b, a, b)], "Comparar: %s − %s = <b>%s km</b>." % (num(a), num(b), num(a - b)))


def s3_completar():
    p, _ = K.next()
    k = R.choice(["album", "bicicleta", "corrida", "livro"])
    t = R.randint(2, 9) * 100
    a = R.randint(40, t - 20)
    if k == "album":
        return mcq("O álbum tem %s figurinhas. %s já colou %s. Quantas faltam para completar?" % (num(t), p, num(a)), num(t - a), wr(t - a, t, a),
                   "Completar: %s − %s = <b>%s</b>. Confira: %s + %s = %s." % (num(t), num(a), num(t - a), num(a), num(t - a), num(t)))
    if k == "bicicleta":
        return mcq("Uma bicicleta custa %s. %s já juntou %s. Quanto falta?" % (reais(t * 100), p, reais(a * 100)), reais((t - a) * 100),
                   [reais(x * 100) for x in (t + a, t - a + 10, t - a - 10)],
                   "Completar: %d − %d = %d: <b>%s</b>." % (t, a, t - a, reais((t - a) * 100)))
    if k == "corrida":
        return mcq("Uma corrida tem %s metros. %s já correu %s metros. Quantos metros faltam?" % (num(t * 10), p, num(a * 10)), num((t - a) * 10) + " metros",
                   [x + " metros" for x in wr((t - a) * 10, t * 10, a * 10)],
                   "Completar: %s − %s = <b>%s metros</b>." % (num(t * 10), num(a * 10), num((t - a) * 10)))
    return mcq("Um livro tem %s páginas. %s já leu %s. Quantas páginas faltam?" % (num(t), p, num(a)), num(t - a), wr(t - a, t, a),
               "Completar: %s − %s = <b>%s</b>." % (num(t), num(a), num(t - a)))


def s4_operacao():
    p, _ = K.next()
    T = [("%s tinha {a} bolinhas de gude e ganhou {b}. Qual conta mostra com quantas ficou?", "+"),
         ("%s tinha {a} bolinhas de gude e perdeu {b}. Qual conta mostra com quantas ficou?", "−"),
         ("Uma caixa tem {a} lápis e outra tem {b}. Qual conta mostra quantos lápis há ao todo?", "+"),
         ("%s tem {a} reais e {q} tem {b}. Qual conta mostra quanto %s tem a mais?", "−"),
         ("Uma estante tem lugar para {a} livros e já tem {b}. Qual conta mostra quantos livros ainda cabem?", "−"),
         ("Numa festa havia {a} pessoas e chegaram mais {b}. Qual conta mostra quantas pessoas há agora?", "+")]
    t, op = R.choice(T)
    a = R.randint(60, 300)
    b = R.randint(20, a - 10)
    q = K.next()[0]
    txt = t.format(a=num(a), b=num(b), q=q)
    if "%s" in txt:
        txt = txt % ((p,) * txt.count("%s"))
    ok = "%s %s %s" % (num(a), op, num(b))
    return mcq(txt, ok, ["%s %s %s" % (num(a), "+" if op == "−" else "−", num(b)), "%s − %s" % (num(b), num(a)), "%s + %s + %s" % (num(a), num(b), num(b))],
               "%s: a conta é <b>%s</b> = %s." % ("Juntar ou acrescentar" if op == "+" else "Retirar, comparar ou completar", ok, num(a + b if op == "+" else a - b)))


def s4_desconhecido():
    p, _ = K.next()
    a = R.randint(25, 90)
    b = R.randint(12, 60)
    k = R.choice(["ganhou", "perdeu", "inicio"])
    if k == "ganhou":
        return mcq("%s tinha %d figurinhas. Ganhou algumas e ficou com %d. Quantas ganhou?" % (p, a, a + b), str(b), [str(a + b + a), str(b + 10), str(a)],
                   "%d + ? = %d. %d − %d = <b>%d</b>." % (a, a + b, a + b, a, b))
    if k == "perdeu":
        return mcq("%s tinha %d bolinhas. Perdeu algumas e ficou com %d. Quantas perdeu?" % (p, a + b, a), str(b), [str(a + a + b), str(b + 1), str(a)],
                   "%d − ? = %d. %d − %d = <b>%d</b>." % (a + b, a, a + b, a, b))
    return mcq("%s ganhou %d reais e ficou com %d reais. Quantos reais tinha antes?" % (p, b, a + b), str(a), [str(a + b + b), str(b), str(a + 10)],
               "? + %d = %d. %d − %d = <b>%d</b>." % (b, a + b, a + b, b, a))


def s5_duas():
    p, g = K.next()
    k = R.choice(["onibus", "compras", "estoque", "pontos", "dados"])
    if k == "onibus":
        a, b, c = R.randint(20, 40), R.randint(5, 15), R.randint(8, 20)
        return mcq("Um ônibus saiu com %d passageiros. No primeiro ponto desceram %d e no segundo subiram %d. Quantos passageiros há agora?" % (a, b, c),
                   str(a - b + c), [str(a - b), str(a + b + c), str(a - b - c)],
                   "%d − %d = %d; %d + %d = <b>%d</b>." % (a, b, a - b, a - b, c, a - b + c))
    if k == "compras":
        t = R.choice([50, 100])
        x, y = R.randint(8, 25), R.randint(8, 20)
        return mcq("%s levou %s ao mercado. Gastou %s com frutas e %s com pão. Quanto sobrou?" % (p, reais(t * 100), reais(x * 100), reais(y * 100)),
                   reais((t - x - y) * 100), [reais((t - x) * 100), reais((x + y) * 100), reais((t - x + y) * 100)],
                   "%d + %d = %d gastos; %d − %d = %d: sobraram <b>%s</b>." % (x, y, x + y, t, x + y, t - x - y, reais((t - x - y) * 100)))
    if k == "estoque":
        a, b, c = R.randint(500, 900), R.randint(100, 300), R.randint(100, 300)
        return mcq("Um mercado tinha %s garrafas de suco. Vendeu %s de manhã e %s à tarde. Quantas garrafas sobraram?" % (num(a), num(b), num(c)),
                   num(a - b - c), [num(a - b), num(a - b + c), num(b + c)],
                   "%s + %s = %s vendidas; %s − %s = <b>%s</b>." % (num(b), num(c), num(b + c), num(a), num(b + c), num(a - b - c)))
    if k == "pontos":
        a, b, c = R.randint(120, 300), R.randint(120, 300), R.randint(50, 150)
        return mcq("%s fez %d pontos na 1ª fase e %d na 2ª. Na 3ª fase perdeu %d. Com quantos pontos ficou?" % (p, a, b, c),
                   num(a + b - c), [num(a + b), num(a + b + c), num(a - c)],
                   "%d + %d = %d; %d − %d = <b>%s</b>." % (a, b, a + b, a + b, c, num(a + b - c)))
    a, b, idade = R.randint(150, 400), R.randint(150, 400), R.randint(8, 9)
    return mcq("%s tem %d anos. Na escola %s há %s alunos de manhã e %s à tarde. Quantos alunos há na escola?" % (p, idade, "dela" if g == "ela" else "dele", num(a), num(b)),
               num(a + b), [num(a + b + idade), num(abs(a - b)), num(a + b - idade)],
               "A idade não é usada no problema (dado desnecessário): %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))


def main():
    seen = set()
    sets = [
        ("Juntar e acrescentar", mix(R, seen, [(s1_juntar, 10), (s1_acrescentar, 10)])),
        ("Retirar e separar", mix(R, seen, [(s2_retirar, 10), (s2_separar, 10)])),
        ("Comparar e completar", mix(R, seen, [(s3_comparar, 10), (s3_completar, 10)])),
        ("Qual é a conta?", mix(R, seen, [(s4_operacao, 12), (s4_desconhecido, 8)])),
        ("Problemas de duas etapas", mix(R, seen, [(s5_duas, 20)])),
    ]
    body = lesson(
        ["Leia o problema e pergunte: as quantidades vão se <b>juntar</b> ou alguém <b>acrescenta</b> algo? Então é adição.",
         "Se algo é <b>retirado</b>, <b>separado</b>, se queremos <b>comparar</b> («quanto a mais?») ou <b>completar</b> («quanto falta?»), é subtração.",
         "Em problemas de <b>duas etapas</b>, faça uma conta de cada vez e escreva o resultado de cada uma.",
         "Nem todo número do problema é usado: risque os <b>dados desnecessários</b>."],
        [("Ana tem 245 figurinhas e Davi tem 180. Quantas Ana tem a mais?", ["Comparar: subtração", "245 − 180 = 65"], "65 figurinhas"),
         ("Um ônibus tinha 32 pessoas. Desceram 9 e subiram 6.", ["32 − 9 = 23", "23 + 6 = 29"], "29 pessoas")],
        [["Somar porque aparece «a mais»", "«Quantos a mais» compara as quantidades: é subtração."],
         ["Fazer só a primeira conta", "Releia a pergunta: ela pede o resultado final."],
         ["Tirar o maior do menor", "Na subtração, o número maior fica primeiro."]])
    faq = [("Quais são os significados da adição e da subtração na BNCC?", "Juntar, acrescentar, separar, retirar, comparar e completar quantidades. Trabalhar todos ajuda a criança a escolher a operação certa."),
           ("Como ajudar quando a criança não sabe qual conta fazer?", "Peça que ela conte o problema com as próprias palavras ou desenhe a situação. Depois pergunte: a quantidade aumenta, diminui ou estamos comparando?")]
    make_unit(R, "problemas-de-adicao-e-subtracao", "N", ["EF03MA06"],
              "Resolver e elaborar problemas de adição e subtração com os significados de juntar, acrescentar, separar, retirar, comparar e completar quantidades, utilizando diferentes estratégias de cálculo exato ou aproximado, incluindo cálculo mental",
              "Problemas de adição e subtração", "Problemas de adição e subtração",
              "Atividades de matemática para o 3º ano com problemas de adição e subtração: juntar, acrescentar, separar, retirar, comparar e completar, escolher a operação e problemas de duas etapas. 100 exercícios com gabarito.",
              "Juntar e acrescentar: adição. Retirar, comparar e completar: subtração.", "Em duas etapas, uma conta de cada vez.",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
