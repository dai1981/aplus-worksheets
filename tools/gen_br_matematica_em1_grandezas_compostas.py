# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Grandezas determinadas por razão ou produto (EM13MAT314)
  python3 tools/gen_br_matematica_em1_grandezas_compostas.py
Velocidade média, densidade, densidade demográfica (razões); energia elétrica kWh = potência × tempo, conta de luz,
consumo de combustível (km/L), vazão (L/min) e produtividade.
Usa geradores do 9º ano (velocidade, densidade demográfica, densidade) com outro sorteio.
Erros: esquecer de passar W para kW, multiplicar quando é razão, misturar minutos e horas.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, num, unit, R2

R = random.Random(91002)
g_vel, g_dem, g_dens = use("gen_br_matematica_9_razoes_entre_grandezas", 91903, "s1_vel", "s2_dens_dem", "s3_densidade")
APAR = [("um chuveiro elétrico", 5500, [F(1, 2), F(1, 4), F(1, 3)]), ("um ar-condicionado", 1000, [8, 6, 4, 10]), ("uma geladeira", 150, [24]),
        ("uma lâmpada LED", 10, [5, 6, 8, 10]), ("um ferro de passar", 1000, [F(1, 2), 1]), ("um micro-ondas", 1200, [F(1, 4), F(1, 2)]),
        ("uma TV", 100, [4, 5, 6, 3]), ("um computador", 200, [8, 6, 4, 5])]


def hh(h):
    h = F(h)
    if h < 1:
        return "%d minutos" % (h * 60)
    return "%s hora%s" % (d(h), "s" if h >= 2 else "")


def s1_kwh():
    nome, w, hs = R.choice(APAR)
    h = R.choice(hs)
    dias = R.choice([30, 30, 20, 10])
    k = R.choice(["kwh", "conta"])
    kwh = F(w, 1000) * h * dias
    if k == "kwh":
        return M("%s de %s W fica %s %s por dia. Quanto %s consome em %d dias, em kWh?" % (nome[0].upper() + nome[1:], num(w), "ligada" if nome.startswith("uma") else "ligado", hh(h), "ela" if nome.startswith("uma") else "ele", dias), "%s kWh" % d(kwh, 2), ["%s kWh" % d(kwh * 1000, 2), "%s kWh" % d(F(w, 1000) * h, 2), "%s kWh" % d(F(w, 1000) * dias, 2)],
                 "%s W = %s kW; %s × %s × %d = <b>%s kWh</b>." % (num(w), d(F(w, 1000)), d(F(w, 1000)), d(h), dias, d(kwh, 2)))
    t = R.choice([F(80, 100), F(90, 100), F(75, 100), F(85, 100)])
    v = kwh * t
    return M("%s de %s W fica %s %s por dia, durante %d dias. Se o kWh custa %s, quanto %s custa na conta de luz?" % (nome[0].upper() + nome[1:], num(w), "ligada" if nome.startswith("uma") else "ligado", hh(h), dias, R2(t), "ela" if nome.startswith("uma") else "ele"), R2(v), [R2(v * 10), R2(kwh), R2(F(w, 1000) * h * t)],
             "Energia: %s kWh; %s × %s = <b>%s</b>." % (d(kwh, 2), d(kwh, 2), R2(t), R2(v)))


def s2_consumo():
    k = R.choice(["kml", "litros", "custo", "vazao", "tempo"])
    if k == "kml":
        km = R.choice([300, 360, 420, 450, 480, 520, 600])
        L = R.choice([30, 40, 35, 50, 45])
        c = F(km, L)
        return M("Um carro percorreu %d km gastando %d L de gasolina. Qual foi o consumo médio?" % (km, L), "%s km/L" % d(c, 1), ["%s L/km" % d(c, 1), "%s km/L" % d(F(L, km) * 100, 1), "%s km/L" % num(km * L)],
                 "%d ÷ %d ≈ <b>%s km/L</b>." % (km, L, d(c, 1)))
    if k == "litros":
        c = R.choice([8, 10, 12, 14, 15])
        km = c * R.choice([20, 25, 30, 35, 40])
        return M("Um carro faz %d km/L. Quantos litros ele gasta numa viagem de %d km?" % (c, km), "%d L" % (km // c), ["%s L" % num(km * c), "%d L" % (km // c + c), "%s L" % d(F(c, km), 3)],
                 "%d ÷ %d = <b>%d L</b>." % (km, c, km // c))
    if k == "custo":
        c = R.choice([10, 12, 15])
        km = c * R.choice([20, 30, 40, 50])
        p = R.choice([F(589, 100), F(612, 100), F(575, 100), F(6, 1)])
        v = F(km, c) * p
        return M("Um carro faz %d km/L e a gasolina custa %s o litro. Quanto custa a gasolina para %d km?" % (c, R2(p), km), R2(v), [R2(km * p), R2(F(km, c)), R2(c * p)],
                 "%d ÷ %d = %d L; %d × %s = <b>%s</b>." % (km, c, km // c, km // c, R2(p), R2(v)))
    if k == "vazao":
        L = R.choice([200, 300, 500, 1000, 1500, 2000])
        q = R.choice([10, 20, 25, 40, 50])
        t = F(L, q)
        return M("Uma torneira tem vazão de %d L/min. Em quanto tempo ela enche uma caixa de %s L?" % (q, num(L)), "%s min" % d(t), ["%s min" % num(L * q), "%s h" % d(t), "%s min" % d(t / 60, 2)],
                 "%s ÷ %d = <b>%s min</b>." % (num(L), q, d(t)))
    p = R.choice([12, 15, 18, 20, 24])
    h = R.choice([4, 5, 6, 8])
    n = R.choice([2, 3, 4])
    return M("Uma máquina produz %d peças por hora. Quantas peças %d máquinas iguais produzem em %d horas?" % (p, n, h), str(p * h * n), [str(p * h), str(p * n), str(p + h + n)],
             "%d × %d × %d = <b>%d</b>." % (p, n, h, p * h * n))


s3_conceitos = bank(R, [
    ("A densidade de um material é…", "massa ÷ volume", ["massa × volume", "volume ÷ massa", "massa + volume"]),
    ("A energia elétrica consumida é…", "potência × tempo", ["potência ÷ tempo", "tempo ÷ potência", "potência + tempo"]),
    ("1 kWh é a energia gasta por um aparelho de…", "1.000 W ligado por 1 hora", ["1 W ligado por 1 hora", "1.000 W ligado por 1 minuto", "100 W ligado por 1 dia"]),
    ("A densidade demográfica é medida em…", "habitantes por km²", ["km² por habitante", "habitantes por km", "km por hora"]),
    ("Velocidade média é…", "distância ÷ tempo", ["distância × tempo", "tempo ÷ distância", "distância + tempo"]),
    ("Um carro que faz 12 km/L é mais econômico que um que faz…", "9 km/L", ["15 km/L", "12 km/L", "14 km/L"]),
    ("Se a velocidade dobra e a distância é a mesma, o tempo…", "cai pela metade", ["dobra", "não muda", "quadruplica"]),
    ("Para passar de km/h para m/s, …", "divide-se por 3,6", ["multiplica-se por 3,6", "divide-se por 60", "multiplica-se por 1.000"]),
], "s3_conceitos")


def main():
    seen = set()
    sets = [
        ("Velocidade média", mix(R, seen, [(g_vel, 16), (s3_conceitos, 4)])),
        ("Densidade e densidade demográfica", mix(R, seen, [(g_dens, 10), (g_dem, 10)])),
        ("Energia elétrica (kWh)", mix(R, seen, [(s1_kwh, 20)])),
        ("Consumo, vazão e produção", mix(R, seen, [(s2_consumo, 16), (s3_conceitos, 4)])),
        ("Revisão", mix(R, seen, [(s1_kwh, 6), (s2_consumo, 6), (g_vel, 4), (g_dens, 4)])),
    ]
    body = lesson(
        ["Algumas grandezas são uma <b>razão</b> entre outras: velocidade = distância ÷ tempo; densidade = massa ÷ volume; densidade demográfica = habitantes ÷ área; consumo = km ÷ litros.",
         "Outras são um <b>produto</b>: energia = potência × tempo (kWh = kW × h); custo = quantidade × preço.",
         "Antes de calcular, deixe as unidades combinando: W → kW (÷ 1.000), minutos → horas (÷ 60)."],
        [("Chuveiro de 5.500 W, 30 min por dia, 30 dias", ["5,5 kW × 0,5 h × 30"], "82,5 kWh"),
         ("420 km com 35 L", ["420 ÷ 35"], "12 km/L")],
        [["Usar W em vez de kW", "Divida a potência por 1.000 antes."],
         ["Misturar minutos e horas", "30 min = 0,5 h."],
         ["Inverter a razão", "km/L: km em cima, litros embaixo."]])
    faq = [("Como calcular o consumo de energia de um aparelho?", "Multiplique a potência em kW pelo tempo de uso em horas: o resultado é em kWh. Depois multiplique pelo preço do kWh para saber o custo."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas que envolvem grandezas determinadas pela razão ou pelo produto de outras, como velocidade, densidade demográfica, energia elétrica etc. (EM13MAT314).")]
    unit(R, "grandezas-compostas", "M", ["EM13MAT314"],
         "Resolver e elaborar problemas que envolvem grandezas determinadas pela razão ou pelo produto de outras (velocidade, densidade demográfica, energia elétrica etc.)",
         "Grandezas determinadas por razão ou produto", "Velocidade, densidade e energia",
         "Atividades de matemática para a 1ª série do Ensino Médio: velocidade média, densidade, densidade demográfica, energia elétrica em kWh, conta de luz, consumo de combustível e vazão. 100 exercícios com gabarito.",
         "Energia = potência × tempo", "Velocidade = distância ÷ tempo.",
         body, faq, sets, 2, grade="1-serie")


if __name__ == "__main__":
    main()
