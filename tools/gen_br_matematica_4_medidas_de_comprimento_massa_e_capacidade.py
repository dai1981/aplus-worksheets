# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Medidas de comprimento, massa e capacidade (Grandezas e medidas, EF04MA20)
  python3 tools/gen_br_matematica_4_medidas_de_comprimento_massa_e_capacidade.py
Escolher a unidade e estimar (km, m, cm, mm; kg, g; L, mL); medir com a régua; perímetro; transformar unidades; comparar; problemas.
Usa geradores do 3º ano (comprimento, massa e capacidade) e do 5º ano (transformações, perímetro) com outro sorteio e limites do 4º ano.
Erros: começar a medir no 1 da régua, usar 100 em vez de 1.000 (1 km = 100 m), achar que o objeto maior é sempre mais pesado, somar só dois lados no perímetro.
"""
import random
from br_common import lesson, make_unit, mix, use, lim, table

R = random.Random(80416)
L = (lim(99999, 2),)
MC = "gen_br_matematica_3_medidas_de_comprimento"
MM = "gen_br_matematica_3_massa_e_capacidade"
M5 = "gen_br_matematica_5_medidas_e_transformacoes"
P5 = "gen_br_matematica_5_perimetro_e_area"
c_unid, c_regua, c_conv, c_comp, c_prob = use(MC, 80957, "s1_unidade", "s3_regua", "s4_converter", "s4_comparar", "s5_problema", preds=L)
m_massa, m_cap, m_conv, m_comp, m_bal, m_copo, m_prob = use(MM, 80958, "s1_massa", "s1_cap", "s2_converter", "s3_comparar", "s4_balanca", "s4_copo", "s5_problema", preds=L)
t_comp, t_prob = use(M5, 80959, "s1_comp", "s5_problema", preds=L)


def so_per(it):
    return "perímetro" in it["q"]


p_ret = use(P5, 80960, "s1_ret", preds=L + (so_per,))


def main():
    seen = set()
    sets = [
        ("Escolher a unidade e estimar", mix(R, seen, [(c_unid, 7), (m_massa, 7), (m_cap, 6)])),
        ("Régua e perímetro", mix(R, seen, [(c_regua, 10), (p_ret, 10)])),
        ("Transformar unidades", mix(R, seen, [(c_conv, 7), (m_conv, 7), (t_comp, 6)])),
        ("Comparar medidas", mix(R, seen, [(c_comp, 7), (m_comp, 7), (m_bal, 3), (m_copo, 3)])),
        ("Problemas", mix(R, seen, [(c_prob, 7), (m_prob, 7), (t_prob, 6)])),
    ]
    body = lesson(
        ["Comprimento: km, m, cm, mm. Massa: kg, g. Capacidade: L, mL. Escolha a unidade de acordo com o tamanho do que vai medir.",
         "1 km = 1.000 m; 1 m = 100 cm; 1 cm = 10 mm; 1 kg = 1.000 g; 1 L = 1.000 mL.",
         "Na régua, comece a medir no <b>0</b>.",
         "O <b>perímetro</b> é a medida do contorno: some todos os lados."],
        [("Quantos metros são 3 km?", ["1 km = 1.000 m", "3 × 1.000"], "3.000 m"),
         ("Perímetro de um retângulo de 8 cm por 5 cm", ["8 + 5 + 8 + 5"], "26 cm")],
        [["Começar a medir no 1 da régua", "Encoste o objeto no 0."],
         ["Usar 100 em vez de 1.000: 1 km = 100 m", "«Quilo» quer dizer mil: 1 km = 1.000 m, 1 kg = 1.000 g."],
         ["Achar que o objeto maior é sempre mais pesado", "Um travesseiro é grande e leve; uma pedra pequena pode ser pesada."]],
        table(["Grandeza", "Unidades"], [["Comprimento", "1 km = 1.000 m; 1 m = 100 cm; 1 cm = 10 mm"], ["Massa", "1 kg = 1.000 g"], ["Capacidade", "1 L = 1.000 mL"]]))
    faq = [("O que o 4º ano mede?", "A BNCC pede medir e estimar comprimentos (incluindo perímetros), massas e capacidades com as unidades padronizadas mais usuais: km, m, cm, mm, kg, g, L e mL."),
           ("Como ajudar a estimar medidas?", "Use referências: uma porta tem cerca de 2 m, um pacote de arroz tem 1 kg ou 5 kg, uma garrafa de água tem 500 mL ou 1,5 L.")]
    make_unit(R, "medidas-de-comprimento-massa-e-capacidade", "M", ["EF04MA20"],
              "Medir e estimar comprimentos (incluindo perímetros), massas e capacidades, utilizando unidades de medida padronizadas mais usuais, valorizando e respeitando a cultura local",
              "Medidas de comprimento, massa e capacidade", "Comprimento, massa e capacidade",
              "Atividades de matemática para o 4º ano sobre medidas de comprimento, massa e capacidade: escolher a unidade, estimar, régua, perímetro, transformar unidades e problemas. 100 exercícios com gabarito.",
              "1 km = 1.000 m; 1 kg = 1.000 g; 1 L = 1.000 mL.", "Perímetro: some todos os lados.",
              body, faq, sets, 16, grade="4-ano")


if __name__ == "__main__":
    main()
