# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Pesquisa amostral (Probabilidade e estatística, EF08MA26, EF08MA27)
  python3 tools/gen_br_matematica_8_pesquisa_amostral.py
Por que usar amostra em vez de censo (custo, tempo, testes que destroem o produto); população e amostra;
amostragem casual simples, sistemática e estratificada (com tamanhos proporcionais); planejar e executar uma pesquisa e escrever o relatório.
Usa geradores do 9º ano (população e amostra, viés, tipos de amostragem) com outro sorteio.
Erros: achar que amostra grande sempre é boa, não respeitar a proporção dos grupos na estratificada, errar o passo da sistemática.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use, num
from br_9 import M, d, bank, unit

R = random.Random(88020)
p_pop, p_vies, p_tipos = use("gen_br_matematica_9_pesquisa_amostral", 88920, "s1_pop_amostra", "s2_vies", "s3_tipos")


s1_razoes = bank(R, [
    ("Uma fábrica quer saber quanto tempo duram suas lâmpadas. Por que ela testa só uma amostra?", "porque o teste destrói as lâmpadas testadas", ["porque as lâmpadas são todas iguais", "porque é proibido testar todas", "porque a amostra dá sempre o valor exato"]),
    ("Uma cozinheira prova uma colher da sopa para saber se está salgada. Ela usou…", "uma amostra", ["um censo", "uma população", "uma moda"]),
    ("Por que as pesquisas de intenção de voto usam amostras?", "porque ouvir todos os eleitores custaria muito e demoraria demais", ["porque só alguns eleitores votam", "porque a amostra nunca erra", "porque a lei proíbe o censo"]),
    ("Um laboratório analisa algumas gotas de sangue de uma pessoa, e não todo o sangue. Isso é usar…", "uma amostra", ["um censo", "uma estimativa errada", "uma frequência"]),
    ("Quando vale a pena fazer um censo em vez de uma amostra?", "quando a população é pequena e fácil de consultar", ["sempre", "quando o teste destrói o produto", "quando há pouco tempo e pouco dinheiro"]),
    ("Para saber a opinião dos 30 alunos de uma turma sobre o passeio, o melhor é…", "perguntar a todos (censo)", ["sortear 3 alunos", "perguntar só ao professor", "perguntar aos alunos de outra escola"]),
    ("Uma vantagem da pesquisa amostral é…", "ser mais rápida e mais barata", ["dar sempre o resultado exato", "não precisar de planejamento", "dispensar o sorteio"]),
    ("Uma amostra muito grande, mas toda escolhida num só lugar, é boa?", "não, o tamanho não corrige uma amostra viciada", ["sim, o tamanho resolve tudo", "sim, se tiver mais de 100 pessoas", "não, amostras grandes são sempre ruins"]),
    ("Uma usina testa algumas latas de cada lote para ver se o peso está certo. Por que não testa todas?", "seria caro e demorado abrir todas as latas", ["porque as latas não têm peso", "porque todas têm o mesmo peso com certeza", "porque testar uma basta para o lote inteiro sempre"]),
], "s1_razoes")


def s2_estrat():
    k = R.choice(["quantos", "total", "sist"])
    if k == "quantos":
        T = R.choice([400, 500, 600, 800, 1000, 1200])
        p = R.choice([F(1, 10), F(1, 20), F(1, 5)])
        g = R.choice([("meninas", "meninos", "Numa escola com %s alunos"), ("do turno da manhã", "do turno da tarde", "Numa escola com %s alunos"), ("moradores da zona urbana", "moradores da zona rural", "Num município com %s moradores")])
        a = R.choice(range(T // 5, 4 * T // 5 + 1, T // 20))
        n = int(T * p)
        na = F(a * n, T)
        if na.denominator != 1:
            return None
        na = int(na)
        return M((g[2] % num(T)) + ", %s são %s e o resto, %s. Uma amostra estratificada de %d pessoas deve ter %s %s?" % ( num(a), g[0], g[1], n, "quantas" if g[0] == "meninas" else "quantos", g[0]),
                 str(na), [str(n // 2) if n // 2 != na else str(na + 1), str(n - na) if n - na != na else str(na + 2), str(a // 2) if a // 2 != na else str(na + 3)],
                 "A proporção de %s é %s/%s; %s/%s × %d = <b>%d</b>." % (g[0], num(a), num(T), num(a), num(T), n, na))
    if k == "total":
        gs = R.choice([("do 6º ano", "do 7º ano", "do 8º ano", "do 9º ano"), ("da turma A", "da turma B", "da turma C")])
        frac = R.choice([10, 20]) if "ano" in gs[0] else 5
        vs = [R.randint(4, 16) * frac if frac > 5 else R.randint(5, 8) * 5 for _ in gs]
        tot = sum(vs) // frac
        i = R.randrange(len(gs))
        return M("Uma escola tem %s. Na amostra estratificada vai 1 aluno a cada %d de cada grupo. Quantos alunos %s vão para a amostra?" % (", ".join("%d alunos %s" % (v, g) for v, g in zip(vs, gs)).replace(", %d alunos %s" % (vs[-1], gs[-1]), " e %d alunos %s" % (vs[-1], gs[-1])), frac, gs[i]),
                 str(vs[i] // frac), [str(tot), str(tot // len(gs)) if tot // len(gs) != vs[i] // frac else str(vs[i] // frac + 1), str(vs[i] // 2) if vs[i] // 2 != vs[i] // frac else str(vs[i])],
                 "%d ÷ %d = <b>%d</b>." % (vs[i], frac, vs[i] // frac))
    N = R.choice([200, 300, 400, 500, 600, 800, 1000])
    n = R.choice([20, 25, 40, 50])
    k2 = N // n
    if N % n:
        return None
    ini = R.randint(1, k2)
    q = R.randint(2, 4)
    return M("Numa amostragem sistemática, de uma lista de %s nomes serão escolhidos %d. O primeiro sorteado foi o número %d. Qual é o %dº escolhido?" % (num(N), n, ini, q),
             str(ini + (q - 1) * k2), [str(ini + q * k2), str(ini + (q - 1) * n), str(ini * q)],
             "Passo: %s ÷ %d = %d. %d + %d × %d = <b>%d</b>." % (num(N), n, k2, ini, q - 1, k2, ini + (q - 1) * k2))


s3_planejar = bank(R, [
    ("Qual é a ordem correta das etapas de uma pesquisa amostral?", "objetivo → população e amostra → coleta → organização em tabelas e gráficos → relatório", ["coleta → objetivo → relatório → gráficos", "gráficos → coleta → objetivo → amostra", "relatório → amostra → coleta → objetivo"]),
    ("Para saber o lanche preferido dos 900 alunos de uma escola, Lia quer uma amostra de 90 alunos. Qual é a melhor forma de escolher?", "sortear 90 nomes da lista de todos os alunos", ["perguntar aos 90 primeiros da fila da cantina", "perguntar aos amigos dela", "deixar responder só quem quiser"]),
    ("Numa pesquisa, a pergunta «Qual é o seu meio de transporte para ir à escola?» com opções a pé, ônibus, carro, bicicleta e outro é uma pergunta…", "fechada, com opções", ["aberta", "tendenciosa", "sem resposta"]),
    ("Depois de coletar as respostas, o que deve ser feito?", "organizar os dados em tabelas e gráficos e calcular medidas", ["apagar as respostas diferentes", "mudar a população", "escolher só as respostas que confirmam a hipótese"]),
    ("O relatório de uma pesquisa amostral deve informar…", "a população, a amostra, como foi escolhida e as conclusões", ["só o gráfico", "só a opinião do pesquisador", "o nome e o endereço dos entrevistados"]),
    ("Numa amostra de 50 alunos, 20 preferem vôlei. Na escola há 1.000 alunos. Uma estimativa razoável é…", "cerca de 400 alunos preferem vôlei", ["exatamente 20 alunos preferem vôlei", "cerca de 20% preferem vôlei", "cerca de 50 alunos preferem vôlei"]),
    ("Antes de aplicar o questionário a toda a amostra, convém…", "testar as perguntas com algumas pessoas", ["publicar o relatório", "calcular a média", "fazer o gráfico"]),
    ("Uma pesquisa quer comparar o tempo de tela de meninos e meninas. Que tipo de amostragem garante os dois grupos na proporção certa?", "estratificada", ["por conveniência", "sistemática numa só turma", "censo de uma turma"]),
    ("Na conclusão de uma pesquisa amostral, devemos dizer que o resultado é…", "uma estimativa para a população", ["o valor exato da população", "válido só para quem respondeu e para mais ninguém", "sempre igual ao do censo"]),
], "s3_planejar")


def s4_estimar():
    n, s = R.choice([(40, 12), (50, 20), (80, 24), (60, 15), (100, 35), (200, 70), (120, 30), (25, 10)])
    N = R.choice([800, 1000, 1200, 2000, 4000, 600])
    e = F(s * N, n)
    if e.denominator != 1:
        return None
    tema = R.choice([("preferem o almoço com feijão", "alunos"), ("usam ônibus para ir à escola", "alunos"), ("leram um livro no mês", "alunos"), ("têm animal de estimação", "famílias")])
    return M("Numa amostra aleatória de %d %s, %d %s. Se há %s %s ao todo, %s devem %s, aproximadamente?" % (n, tema[1], s, tema[0], num(N), tema[1], "quantas" if tema[1] == "famílias" else "quantos", tema[0].split(" ", 1)[0].replace("preferem", "preferir").replace("usam", "usar").replace("leram", "ter lido").replace("têm", "ter") + " " + tema[0].split(" ", 1)[1]),
             num(int(e)), [num(s), num(N - int(e)), num(int(e) // 2) if int(e) // 2 != s else num(int(e) * 2)],
             "%d/%d = %s%% da amostra; %s%% de %s = <b>%s</b>." % (s, n, d(F(s * 100, n)), d(F(s * 100, n)), num(N), num(int(e))))


def main():
    seen = set()
    sets = [
        ("Por que usar uma amostra?", mix(R, seen, [(s1_razoes, 9), (p_pop, 11)])),
        ("Amostras representativas", mix(R, seen, [(p_vies, 8), (p_tipos, 12)])),
        ("Casual simples, sistemática e estratificada", mix(R, seen, [(s2_estrat, 14), (p_tipos, 6)])),
        ("Planejar a pesquisa", mix(R, seen, [(s3_planejar, 9), (s4_estimar, 11)])),
        ("Revisão", mix(R, seen, [(s2_estrat, 8), (s4_estimar, 6), (p_pop, 3), (p_tipos, 3)])),
    ]
    body = lesson(
        ["A <b>população</b> é o grupo todo; a <b>amostra</b> é a parte pesquisada. Usamos amostras quando o censo é caro, demorado ou quando o teste destrói o produto.",
         "<b>Casual simples</b>: sorteio entre todos. <b>Sistemática</b>: um a cada k da lista (k = população ÷ amostra). <b>Estratificada</b>: divide em grupos e sorteia em cada um, na mesma proporção da população.",
         "Uma boa amostra é aleatória e representativa. Uma amostra grande, mas viciada, continua ruim.",
         "Etapas: objetivo → população e amostra → coleta → tabelas e gráficos → relatório com as conclusões."],
        [("Escola com 600 meninas e 400 meninos, amostra de 50", ["600/1.000 × 50", "400/1.000 × 50"], "30 meninas e 20 meninos"),
         ("Lista de 500 nomes, amostra de 25", ["500 ÷ 25 = 20"], "um a cada 20")],
        [["Achar que amostra grande é sempre boa", "Se for escolhida só num lugar, continua viciada."],
         ["Não respeitar a proporção na estratificada", "Cada grupo entra na mesma proporção da população."],
         ["Errar o passo da sistemática", "Passo = tamanho da população ÷ tamanho da amostra."]])
    faq = [("Qual é a diferença entre amostragem sistemática e estratificada?", "Na sistemática, escolhe-se um elemento a cada k da lista. Na estratificada, a população é dividida em grupos (estratos) e sorteiam-se elementos de cada grupo, na mesma proporção da população."),
           ("O que a BNCC pede no 8º ano?", "Selecionar razões, de diferentes naturezas (física, ética ou econômica), que justificam a realização de pesquisas amostrais e não censitárias, e reconhecer que a seleção da amostra pode ser feita de diferentes maneiras (amostra casual simples, sistemática e estratificada) (EF08MA26), e planejar e executar pesquisa amostral, selecionando uma técnica de amostragem adequada, e escrever relatório (EF08MA27).")]
    unit(R, "pesquisa-amostral", "E", ["EF08MA26", "EF08MA27"],
         "Selecionar razões, de diferentes naturezas (física, ética ou econômica), que justificam a realização de pesquisas amostrais e não censitárias, e reconhecer que a seleção da amostra pode ser feita de diferentes maneiras (amostra casual simples, sistemática e estratificada); planejar e executar pesquisa amostral, selecionando uma técnica de amostragem adequada, e escrever relatório",
         "Pesquisa amostral e tipos de amostragem", "Pesquisa amostral",
         "Atividades de matemática para o 8º ano sobre pesquisa amostral: por que usar amostras, população e amostra, amostragem casual simples, sistemática e estratificada, estimativas e relatório. 100 exercícios com gabarito.",
         "Amostra: parte que representa o todo", "Sorteie e respeite as proporções.",
         body, faq, sets, 20, grade="8-ano")


if __name__ == "__main__":
    main()
