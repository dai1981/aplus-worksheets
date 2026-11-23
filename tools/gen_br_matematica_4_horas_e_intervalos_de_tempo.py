# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Horas e intervalos de tempo (Grandezas e medidas, EF04MA22)
  python3 tools/gen_br_matematica_4_horas_e_intervalos_de_tempo.py
Ler horas em relógios de ponteiros e digitais; horários depois do meio-dia; duração de eventos (início, fim, quanto tempo);
horas, minutos e segundos e as transformações (1 h = 60 min, 1 min = 60 s); estimar durações; problemas do dia a dia.
Usa geradores do 3º ano (horas) e do 5º ano (tempo) com outro sorteio.
Erros: trocar os ponteiros, contar a duração como se a hora tivesse 100 minutos, achar que 1,5 h = 1 h 50 min.
"""
import random
from br_common import lesson, make_unit, mix, use, lim, relogio

R = random.Random(80418)
H3 = "gen_br_matematica_3_horas_e_intervalos_de_tempo"
M5 = "gen_br_matematica_5_medidas_e_transformacoes"
h_pont, h_dig, h_tarde, h_unid, h_dur, h_rel, h_est, h_prob = use(H3, 80963, "s1_ponteiros", "s1_digital", "s2_tarde", "s2_unidades", "s3_duracao", "s3_relogios", "s4_unidade", "s5_problema")


def so_tempo(it):
    t = it["q"]
    return any(w in t for w in ("hora", "minuto", "segundo", "dia", "semana", "mês", "meses", "ano")) and "década" not in t and "século" not in t


t_tempo = use(M5, 80964, "s4_tempo", preds=(lim(99999, 2), so_tempo))


def main():
    seen = set()
    sets = [
        ("Ler as horas", mix(R, seen, [(h_pont, 12), (h_dig, 8)])),
        ("Horas, minutos e segundos", mix(R, seen, [(h_unid, 10), (t_tempo, 10)])),
        ("Duração de eventos", mix(R, seen, [(h_dur, 14), (h_rel, 6)])),
        ("Depois do meio-dia e estimativas", mix(R, seen, [(h_tarde, 12), (h_est, 8)])),
        ("Problemas", mix(R, seen, [(h_prob, 20)])),
    ]
    body = lesson(
        ["No relógio de ponteiros, o ponteiro <b>pequeno</b> mostra as horas e o <b>grande</b>, os minutos.",
         "1 hora = 60 minutos; 1 minuto = 60 segundos; 1 dia = 24 horas.",
         "Para saber quanto tempo durou um evento, conte do início até o fim: primeiro as horas inteiras, depois os minutos.",
         "Depois do meio-dia, some 12: 3 horas da tarde = 15h."],
        [("A aula começa às 7h20 e termina às 11h50. Quanto tempo dura?", ["7h20 → 11h20: 4 h", "11h20 → 11h50: 30 min"], "4 h 30 min"),
         ("Quantos minutos há em 2 horas e meia?", ["2 × 60 = 120", "120 + 30"], "150 minutos")],
        [["Trocar os ponteiros", "O ponteiro pequeno é o das horas."],
         ["Contar como se a hora tivesse 100 minutos: 8h50 + 20 min = 8h70", "60 minutos formam 1 hora: 8h50 + 20 min = 9h10."],
         ["Achar que 1,5 h = 1 h 50 min", "Meia hora são 30 minutos: 1,5 h = 1 h 30 min."]],
        relogio(7, 20))
    faq = [("O que o 4º ano aprende sobre o tempo?", "A BNCC pede medir, estimar e comparar intervalos de tempo de eventos do dia a dia, em horas, minutos e segundos, e fazer conversões simples entre essas unidades."),
           ("Como calcular a duração de um evento?", "Conte primeiro as horas inteiras desde o início e depois os minutos que faltam até o fim. Uma linha do tempo ajuda bastante.")]
    make_unit(R, "horas-e-intervalos-de-tempo", "M", ["EF04MA22"],
              "Medir, estimar e comparar intervalos de tempo de duração de eventos cotidianos, como o tempo gasto para ir à escola, utilizando horas, minutos e segundos, e realizar conversões simples entre essas unidades",
              "Horas e intervalos de tempo: relógios, duração e conversões", "Horas e duração",
              "Atividades de matemática para o 4º ano sobre horas e intervalos de tempo: relógios de ponteiros e digitais, duração de eventos, horas, minutos e segundos e problemas. 100 exercícios com gabarito.",
              "1 h = 60 min; 1 min = 60 s.", "Duração: conte as horas inteiras e depois os minutos.",
              body, faq, sets, 18, grade="4-ano")


if __name__ == "__main__":
    main()
