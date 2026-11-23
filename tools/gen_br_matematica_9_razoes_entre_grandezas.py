# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Razões entre grandezas de espécies diferentes (Números, EF09MA07)
  python3 tools/gen_br_matematica_9_razoes_entre_grandezas.py
Velocidade média (km/h, m/s), densidade demográfica (hab/km²), densidade (g/cm³), consumo (km/L), escala, vazão (L/min), preço por unidade.
Erros: dividir na ordem errada, esquecer de converter unidades (min → h), achar que 1 m/s = 1 km/h.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, unit

R = random.Random(89006)
CID = ["Campinas", "Londrina", "Joinville", "Uberlândia", "Feira de Santana", "Juiz de Fora", "Caxias do Sul", "Maringá", "Petrolina", "Santarém"]


def hh(t):
    return d(t) + (" hora" if t < 2 else " horas")


def s1_vel():
    v = R.choice([40, 50, 60, 72, 80, 90, 100])
    t = R.choice([F(1, 2), 1, F(3, 2), 2, F(5, 2), 3, 4])
    dist = v * t
    if dist.denominator != 1:
        return None
    k = R.choice(["v", "d", "t"])
    th = hh(t)
    if k == "v":
        return M("Um carro percorreu %s km em %s. Qual foi a velocidade média?" % (d(dist), th), "%d km/h" % v, ["%s km/h" % d(dist * t), "%s km/h" % d(dist + t), "%d km/h" % (v // 2) if v % 2 == 0 else "%d km/h" % (v + 10)],
                 "v = distância ÷ tempo = %s ÷ %s = <b>%d km/h</b>." % (d(dist), d(t), v))
    if k == "d":
        return M("Um ônibus viaja a %d km/h durante %s. Que distância percorre?" % (v, th), "%s km" % d(dist), ["%s km" % d(F(v) / t), "%s km" % d(v + t), "%s km" % d(dist + v)],
                 "d = v · t = %d · %s = <b>%s km</b>." % (v, d(t), d(dist)))
    return M("Uma moto percorre %s km a %d km/h. Quanto tempo leva?" % (d(dist), v), th, [hh(t + 1), hh(t * 2), hh(t + F(1, 2)), hh(t + 2)],
             "t = d ÷ v = %s ÷ %d = <b>%s</b>." % (d(dist), v, th))


def s1_min():
    v = R.choice([60, 72, 90, 120, 48, 84])
    m = R.choice([10, 15, 20, 30, 40, 45, 50])
    dist = F(v * m, 60)
    if dist.denominator != 1:
        return None
    return M("Um trem anda a %d km/h. Quantos km percorre em %d minutos?" % (v, m), "%s km" % d(dist), ["%d km" % (v * m), "%s km" % d(F(v, m)) if v % m == 0 else "%d km" % (v - m), "%s km" % d(dist * 2)],
             "%d min = %s h; %d · %s = <b>%s km</b>." % (m, d(F(m, 60))if (F(m, 60) * 100).denominator == 1 else "%d/60" % m, v, d(F(m, 60)) if (F(m, 60) * 100).denominator == 1 else "%d/60" % m, d(dist)))


def s2_ms():
    v = R.choice([18, 36, 54, 72, 90, 108, 144])
    if R.random() < 0.5:
        return M("Quanto é %d km/h em metros por segundo?" % v, "%d m/s" % int(F(v * 10, 36)), ["%s m/s" % d(F(v * 36, 10)), "%d m/s" % v, "%d m/s" % (v // 6)],
                 "Divida por 3,6: %d ÷ 3,6 = <b>%d m/s</b>." % (v, int(F(v * 10, 36))))
    w = int(F(v * 10, 36))
    return M("Quanto é %d m/s em km/h?" % w, "%d km/h" % v, ["%d km/h" % w, "%d km/h" % (w * 10), "%d km/h" % (w * 60)],
             "Multiplique por 3,6: %d · 3,6 = <b>%d km/h</b>." % (w, v))


def s2_dens_dem():
    c = R.choice(CID)
    area = R.choice([400, 500, 800, 1000, 1250, 1600, 2000])
    dd = R.choice([200, 250, 300, 400, 450, 500, 600, 750])
    pop = area * dd
    return M("O município de %s tem cerca de %s habitantes e área de %s km². Qual é a densidade demográfica?" % (c, d(pop), d(area)), "%s hab/km²" % d(dd),
             ["%s hab/km²" % d(dd * 10), "%s km²/hab" % d(dd), "%s hab/km²" % d(dd // 2) if dd % 2 == 0 else "%s hab/km²" % d(dd + 50)],
             "densidade = habitantes ÷ área = %s ÷ %s = <b>%s hab/km²</b>." % (d(pop), d(area), d(dd)))


MAT = [("alumínio", F(27, 10)), ("ferro", F(79, 10)), ("cobre", F(89, 10)), ("chumbo", F(113, 10)), ("vidro", F(25, 10)), ("gelo", F(9, 10)), ("ouro", F(193, 10))]


def s3_densidade():
    m, dn = R.choice(MAT)
    vol = R.choice([10, 20, 30, 40, 50, 100])
    mass = dn * vol
    k = R.choice(["dens", "massa", "vol"])
    if k == "dens":
        return M("Um bloco de %s tem massa de %s g e volume de %d cm³. Qual é a sua densidade?" % (m, d(mass), vol), "%s g/cm³" % d(dn), ["%s g/cm³" % d(mass * vol), "%s g/cm³" % d(F(vol) / mass, 2), "%s g/cm³" % d(dn * 10)],
                 "densidade = massa ÷ volume = %s ÷ %d = <b>%s g/cm³</b>." % (d(mass), vol, d(dn)))
    if k == "massa":
        return M("A densidade do %s é %s g/cm³. Qual é a massa de %d cm³ desse material?" % (m, d(dn), vol), "%s g" % d(mass), ["%s g" % d(dn + vol), "%s g" % d(F(vol) / dn, 1), "%s g" % d(mass / 10)],
                 "massa = densidade · volume = %s · %d = <b>%s g</b>." % (d(dn), vol, d(mass)))
    return M("Uma peça de %s (densidade %s g/cm³) tem massa de %s g. Qual é o volume?" % (m, d(dn), d(mass)), "%d cm³" % vol, ["%s cm³" % d(mass * dn, 1), "%d cm³" % (vol * 10), "%d cm³" % (vol + 10)],
             "volume = massa ÷ densidade = %s ÷ %s = <b>%d cm³</b>." % (d(mass), d(dn), vol))


def s4_outras():
    k = R.choice(["consumo", "vazao", "preco", "escala", "batimento"])
    if k == "consumo":
        c, L = R.choice([10, 12, 13, 14, 15]), R.choice([20, 25, 30, 40])
        return M("Um carro percorreu %d km gastando %d litros de gasolina. Qual é o consumo?" % (c * L, L), "%d km/L" % c, ["%d L/km" % c, "%d km/L" % (c * 2), "%d km/L" % (c + L)],
                 "%d ÷ %d = <b>%d km/L</b>." % (c * L, L, c))
    if k == "vazao":
        q, t = R.choice([8, 12, 15, 20, 25]), R.choice([6, 10, 12, 20, 30])
        return M("Uma torneira enche um tanque de %d litros em %d minutos. Qual é a vazão?" % (q * t, t), "%d L/min" % q, ["%d min/L" % q, "%d L/min" % (q * t), "%d L/min" % (q + t)],
                 "%d ÷ %d = <b>%d L/min</b>." % (q * t, t, q))
    if k == "preco":
        p, kg = R.choice([450, 690, 850, 1290, 2390]), R.choice([2, 3, 4, 5])
        return M("Uma loja vende %d kg de carne por %s. Qual é o preço por quilo?" % (kg, reais(p * kg)), reais(p), [reais(p * kg * kg), reais(p + 100), reais(p * kg // 10)],
                 "%s ÷ %d = <b>%s</b> por kg." % (reais(p * kg), kg, reais(p)))
    if k == "escala":
        e = R.choice([100000, 200000, 500000, 1000000])
        cm = R.randint(2, 9)
        km = F(cm * e, 100000)
        return M("Num mapa na escala 1 : %s, duas cidades estão a %d cm. Qual é a distância real?" % (d(e), cm), "%s km" % d(km), ["%s km" % d(km * 10), "%s km" % d(km / 10), "%d km" % (cm * 100)],
                 "%d cm · %s = %s cm = <b>%s km</b>." % (cm, d(e), d(cm * e), d(km)))
    b, s = R.choice([15, 18, 20, 22]), R.choice([4, 5])
    return M("Em 15 segundos o coração de um atleta bateu %d vezes. Quantos batimentos por minuto?" % b,
             "%d bpm" % (b * 4), ["%d bpm" % (b * 15), "%d bpm" % (b + 60), "%d bpm" % (b * 2)], "1 minuto = 4 · 15 s; %d · 4 = <b>%d bpm</b>." % (b, b * 4))


def s5_comparar():
    v1, t1 = R.choice([(180, 3), (240, 4), (150, 2), (210, 3)])
    v2, t2 = R.choice([(260, 4), (200, 2), (300, 5), (330, 6)])
    a, b = F(v1, t1), F(v2, t2)
    if a == b:
        return None
    w = "Ana" if a > b else "Bruno"
    return M("Ana dirigiu %d km em %d h. Bruno dirigiu %d km em %d h. Quem teve maior velocidade média?" % (v1, t1, v2, t2), w, ["Bruno" if w == "Ana" else "Ana", "os dois foram iguais", "quem andou mais km"],
             "Ana: %s km/h; Bruno: %s km/h. Maior: <b>%s</b>." % (d(a), d(b), w))


def main():
    seen = set()
    sets = [
        ("Velocidade média", mix(R, seen, [(s1_vel, 20)])),
        ("Minutos, horas, km/h e m/s", mix(R, seen, [(s1_min, 10), (s2_ms, 10)])),
        ("Densidade demográfica", mix(R, seen, [(s2_dens_dem, 14), (s5_comparar, 6)])),
        ("Densidade de materiais", mix(R, seen, [(s3_densidade, 20)])),
        ("Outras razões no dia a dia", mix(R, seen, [(s4_outras, 20)])),
    ]
    body = lesson(
        ["Uma <b>razão entre grandezas de espécies diferentes</b> divide uma grandeza por outra de outro tipo, e a unidade junta as duas: km/h, hab/km², g/cm³, km/L.",
         "Velocidade média = distância ÷ tempo. Densidade demográfica = habitantes ÷ área. Densidade = massa ÷ volume.",
         "Antes de dividir, confira as unidades: 30 minutos são 0,5 hora. Para passar de km/h para m/s, divida por 3,6."],
        [("240 km em 3 h", ["240 ÷ 3"], "80 km/h"),
         ("54 g em 20 cm³", ["54 ÷ 20"], "2,7 g/cm³"),
         ("72 km/h em m/s", ["72 ÷ 3,6"], "20 m/s")],
        [["Dividir na ordem errada", "A unidade mostra a ordem: km/h é km ÷ h."],
         ["Esquecer de converter minutos em horas", "20 min = 1/3 h."],
         ["Achar que 1 m/s = 1 km/h", "1 m/s = 3,6 km/h."]])
    faq = [("O que são razões entre grandezas de espécies diferentes?", "São divisões entre grandezas de tipos diferentes, como distância e tempo (velocidade) ou população e área (densidade demográfica). A BNCC pede resolver problemas com essas razões no 9º ano."),
           ("Como converter km/h em m/s?", "Divida por 3,6, porque 1 km = 1.000 m e 1 h = 3.600 s. Para voltar de m/s para km/h, multiplique por 3,6.")]
    unit(R, "razoes-entre-grandezas", "N", ["EF09MA07"],
         "Resolver problemas que envolvam a razão entre duas grandezas de espécies diferentes, como velocidade e densidade demográfica",
         "Razões entre grandezas: velocidade, densidade e escala", "Razões entre grandezas",
         "Atividades de matemática para o 9º ano sobre razões entre grandezas de espécies diferentes: velocidade média, km/h e m/s, densidade demográfica, densidade, consumo e vazão. 100 exercícios com gabarito.",
         "Divida uma grandeza pela outra e junte as unidades.", "km/h, hab/km², g/cm³, km/L",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
