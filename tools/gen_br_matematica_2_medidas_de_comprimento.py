# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Medidas de comprimento (Grandezas e medidas, EF02MA16)
  python3 tools/gen_br_matematica_2_medidas_de_comprimento.py
Medir com palmos, pés e clipes (unidades não padronizadas); medir com a régua em centímetros; metro, centímetro e milímetro;
escolher a unidade e o instrumento; estimar e comparar comprimentos; problemas. Usa geradores do 3º ano com outro sorteio.
Erros: começar a medir no 1 da régua, achar que palmos de pessoas diferentes dão a mesma medida, misturar metro e centímetro.
"""
import random
import gen_br_matematica_3_medidas_de_comprimento as C3
from br_common import mcq, lesson, make_unit, mix, use, lim

R = random.Random(80215)
M3 = "gen_br_matematica_3_medidas_de_comprimento"
L = (lim(999, 0),)
m_unid, m_instr, m_palmo, m_regua, m_comp, m_conv, m_prob = use(M3, 80909, "s1_unidade", "s1_instrumento", "s2_palmo", "s3_regua", "s4_comparar", "s4_converter", "s5_problema", preds=L)

NP = [("Lia mediu a mesa com o palmo e achou 6 palmos. O pai dela mediu a mesma mesa e achou 4 palmos. Por quê?", "o palmo do pai é maior", ["a mesa mudou de tamanho", "o pai mediu errado", "Lia tem a mão maior"]),
      ("Para todos acharem a mesma medida, é melhor usar…", "uma unidade padronizada, como o centímetro", ["o palmo de cada um", "o pé de cada um", "o passo de cada um"]),
      ("Um lápis tem o comprimento de 4 clipes. Uma caneta tem 6 clipes. Qual é mais comprida?", "a caneta", ["o lápis", "são iguais", "não dá para saber"]),
      ("A sala tem 20 passos de Rui e 15 passos da professora. Quem dá passos maiores?", "a professora", ["Rui", "os dois iguais", "não dá para saber"]),
      ("Um barbante mede 8 palitos. Outro mede 8 lápis. Os palitos são menores que os lápis. Qual barbante é mais comprido?", "o que mede 8 lápis", ["o que mede 8 palitos", "são iguais", "não dá para saber"]),
      ("Para medir o comprimento de uma borracha com clipes, os clipes devem ficar…", "um encostado no outro, sem buracos", ["separados", "uns em cima dos outros", "em pé"]),
      ("Ana mediu a lousa com o braço aberto (braça) e achou 3 braças. Mediu com o palmo e achou um número…", "maior que 3", ["menor que 3", "igual a 3", "zero"]),
      ("Por que cada criança acha um número diferente de pés para medir a sala?", "os pés têm tamanhos diferentes", ["a sala muda", "contar pés é proibido", "os números mudam sozinhos"])]


def s2_nao_padrao():
    q, a, w = R.choice(NP)
    return mcq(q, a, w, "Unidades como palmo e pé mudam de pessoa para pessoa. Resposta: <b>%s</b>." % a)


EST = [("Qual é a altura mais provável de uma criança do 2º ano?", "cerca de 1 metro e 20 centímetros", ["cerca de 12 centímetros", "cerca de 12 metros", "cerca de 2 milímetros"]),
       ("Qual é o comprimento mais provável de um lápis novo?", "cerca de 18 centímetros", ["cerca de 18 metros", "cerca de 18 milímetros", "cerca de 1 metro"]),
       ("Qual é a altura mais provável de uma porta?", "cerca de 2 metros", ["cerca de 2 centímetros", "cerca de 20 metros", "cerca de 2 milímetros"]),
       ("Qual é o comprimento mais provável de uma formiga?", "cerca de 5 milímetros", ["cerca de 5 metros", "cerca de 50 centímetros", "cerca de 5 quilômetros"]),
       ("Qual é a largura mais provável de uma folha de caderno?", "cerca de 20 centímetros", ["cerca de 20 metros", "cerca de 2 milímetros", "cerca de 200 metros"]),
       ("Qual é o comprimento mais provável de uma quadra de futebol de salão?", "cerca de 40 metros", ["cerca de 40 centímetros", "cerca de 4 milímetros", "cerca de 400 centímetros"]),
       ("Qual é a espessura mais provável de uma moeda?", "cerca de 2 milímetros", ["cerca de 2 metros", "cerca de 20 centímetros", "cerca de 2 centímetros e meio"]),
       ("Qual é o comprimento mais provável de um ônibus?", "cerca de 12 metros", ["cerca de 12 centímetros", "cerca de 120 metros", "cerca de 12 milímetros"])]


def s4_estimar():
    q, a, w = R.choice(EST)
    return mcq(q, a, w, "Compare com coisas que você conhece: 1 metro é mais ou menos um passo grande de adulto; 1 centímetro é a largura de uma unha. Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Medir com palmos, pés e clipes", mix(R, seen, [(m_palmo, 8), (s2_nao_padrao, 8), (m_instr, 4)])),
        ("Medir com a régua", mix(R, seen, [(m_regua, 20)])),
        ("Metro, centímetro e milímetro", mix(R, seen, [(m_unid, 8), (m_instr, 4), (m_conv, 8)])),
        ("Estimar e comparar", mix(R, seen, [(s4_estimar, 8), (m_comp, 12)])),
        ("Problemas de comprimento", mix(R, seen, [(m_prob, 20)])),
    ]
    body = lesson(
        ["Podemos medir com o <b>palmo</b>, o pé ou clipes, mas cada pessoa acha um número diferente.",
         "Para todos acharem a mesma medida, usamos o <b>metro (m)</b>, o <b>centímetro (cm)</b> e o <b>milímetro (mm)</b>.",
         "Na <b>régua</b>, comece a medir no <b>0</b>, e não no 1.",
         "1 m = 100 cm e 1 cm = 10 mm. Use metros para coisas grandes e centímetros para coisas pequenas."],
        [("Lápis da marca 0 até a marca 9 da régua", ["começa no 0", "termina no 9"], "9 cm"),
         ("1 m ou 80 cm: qual é maior?", ["1 m = 100 cm", "100 &gt; 80"], "1 m")],
        [["Começar a medir no 1 da régua", "O começo do objeto fica no 0."],
         ["Achar que palmos diferentes dão a mesma medida", "Palmos têm tamanhos diferentes."],
         ["Comparar 1 m com 90 cm e achar que 90 é maior", "Transforme: 1 m = 100 cm."]],
        C3.regua(0, 45))
    faq = [("O que o 2º ano aprende sobre comprimento?", "A BNCC pede estimar, medir e comparar comprimentos usando unidades não padronizadas (palmo, passo) e padronizadas (metro, centímetro e milímetro) e instrumentos como a régua e a fita métrica."),
           ("Como praticar medidas em casa?", "Meça objetos com palmos e depois com a régua. Pergunte primeiro «quanto você acha que mede?» e depois confiram juntos.")]
    make_unit(R, "medidas-de-comprimento", "M", ["EF02MA16"],
              "Estimar, medir e comparar comprimentos de lados de salas (incluindo contorno) e de polígonos, utilizando unidades de medida não padronizadas e padronizadas (metro, centímetro e milímetro) e instrumentos adequados",
              "Medidas de comprimento: metro, centímetro e milímetro", "Medidas de comprimento",
              "Atividades de matemática para o 2º ano sobre medidas de comprimento: palmos e clipes, régua, metro, centímetro e milímetro, estimar e comparar. 100 exercícios com gabarito.",
              "Na régua, comece no 0.", "1 m = 100 cm; 1 cm = 10 mm.",
              body, faq, sets, 15, grade="2-ano")


if __name__ == "__main__":
    main()
