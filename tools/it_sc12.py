# -*- coding: utf-8 -*-
"""Italia / Liceo scientifico: quarta liceo（Fisica e Scienze naturali, secondo biennio）"""
import math
from it_sci import H, nq, num, it

D = "A che cosa corrisponde questa descrizione: {v}?"
KC = 8.99e9
E0 = 1.6e-19


def f_termo(R):
    k = R.choice(["primo", "lav", "rend", "carnot", "cop", "entr"])
    if k == "primo":
        q, l = R.choice([(500, 200), (1200, 400), (800, 800), (300, 450), (1000, 250), (600, 100)])
        du = q - l
        return nq("Un gas assorbe %d J di calore e compie un lavoro di %d J. Di quanto varia la sua energia interna?" % (q, l), du, [q + l, l - q, q, l], "J",
                  "Primo principio: ΔU = Q − L = %d − %d = %d J." % (q, l, du), neg=True) if du != 0 else it(
                  "Un gas assorbe %d J di calore e compie un lavoro di %d J. Di quanto varia la sua energia interna?" % (q, l), "0 J", ["%d J" % (q + l), "%d J" % q, "%d J" % (2 * q)], "ΔU = Q − L = 0: trasformazione con energia interna costante.")
    if k == "lav":
        p, v1, v2 = R.choice([(100000, 0.002, 0.005), (200000, 0.01, 0.03), (150000, 0.004, 0.006), (50000, 0.1, 0.3), (300000, 0.001, 0.004)])
        return nq("Un gas si espande a pressione costante di %s Pa da %s m³ a %s m³. Quanto lavoro compie?" % (num(p), num(v1), num(v2)), p * (v2 - v1), [p * v2, p * v1, p / (v2 - v1), p * (v2 + v1)], "J",
                  "L = p ΔV = %s × %s = %s J." % (num(p), num(v2 - v1), num(p * (v2 - v1))))
    if k == "rend":
        q1, l = R.choice([(1000, 250), (5000, 1500), (2000, 700), (800, 200), (12000, 3000), (600, 180)])
        return nq("Una macchina termica assorbe %d J e produce %d J di lavoro. Qual è il rendimento?" % (q1, l), l * 100 / q1, [q1 / l, (q1 - l) * 100 / q1, l / q1, l * 100 / (q1 - l)], "%",
                  "η = L : Q₁ = %d : %d = %s %%." % (l, q1, num(l * 100 / q1)))
    if k == "carnot":
        t1, t2 = R.choice([(600, 300), (500, 300), (800, 400), (400, 300), (1000, 250), (900, 300)])
        return nq("Una macchina di Carnot lavora tra %d K e %d K. Qual è il rendimento massimo?" % (t1, t2), (1 - t2 / t1) * 100, [t2 / t1 * 100, (t1 - t2), t1 / t2 * 10, (1 - t2 / t1) * 50], "%",
                  "η = 1 − T₂ : T₁ = 1 − %d : %d = %s %%." % (t2, t1, num((1 - t2 / t1) * 100)))
    if k == "cop":
        q1, l = R.choice([(3000, 1000), (2400, 600), (5000, 1250), (1800, 600)])
        q2 = q1 - l
        return nq("Un frigorifero assorbe %d J di lavoro e cede %d J all’ambiente. Quanto calore toglie all’interno?" % (l, q1), q2, [q1 + l, q1, l, q1 / l], "J",
                  "Q₂ = Q₁ − L = %d − %d = %d J." % (q1, l, q2))
    q, t = R.choice([(3000, 300), (6000, 400), (1000, 250), (9000, 300), (5000, 500)])
    return nq("Un corpo a %d K assorbe reversibilmente %d J. Quanto varia la sua entropia?" % (t, q), q / t, [q * t, t / q, q / t / 2, q - t], "J/K", "ΔS = Q : T = %d : %d = %s J/K." % (q, t, num(q / t)))


def f_onde(R):
    k = R.choice(["v", "f", "lam", "db", "dop", "corda"])
    if k == "v":
        f, l = R.choice([(440, 0.773), (50, 6.8), (1000, 0.34), (2, 1.5), (680, 0.5), (20, 17)])
        return nq("Un’onda ha frequenza %s Hz e lunghezza d’onda %s m. Quanto vale la velocità?" % (num(f), num(l)), f * l, [f / l, l / f, f + l, f * l * 2], "m/s",
                  "v = λ f = %s × %s = %s m/s." % (num(l), num(f), num(f * l)))
    if k == "f":
        t = R.choice([0.002, 0.01, 0.5, 0.025, 0.004, 0.2])
        return nq("Un’onda ha periodo %s s. Qual è la frequenza?" % num(t), 1 / t, [t, 1 / t / 10, 2 / t, t * 1000], "Hz", "f = 1 : T = %s Hz." % num(1 / t))
    if k == "lam":
        v, f = R.choice([(340, 170), (340, 440), (1480, 740), (340, 20000), (5000, 1000), (340, 85)])
        return nq("Un suono si propaga a %d m/s con frequenza %d Hz. Qual è la lunghezza d’onda?" % (v, f), v / f, [v * f, f / v, v / f * 2, v - f if v > f else v / f / 10], "m",
                  "λ = v : f = %d : %d = %s m." % (v, f, num(v / f)))
    if k == "db":
        a, n = R.choice([(60, 10), (70, 100), (50, 1000), (40, 10), (80, 100)])
        return nq("Un suono ha livello %d dB. Se l’intensità diventa %d volte più grande, quale livello sonoro si ha?" % (a, n), a + 10 * math.log10(n), [a * n, a + n, a + 10 * n, a * 2], "dB",
                  "Ogni fattore 10 di intensità aggiunge 10 dB: %d + %s = %s dB." % (a, num(10 * math.log10(n)), num(a + 10 * math.log10(n))))
    if k == "dop":
        f, vs = R.choice([(500, 20), (440, 34), (1000, 40), (600, 30), (800, 17)])
        fo = f * 340 / (340 - vs)
        return nq("Un’ambulanza emette %d Hz e si avvicina a %d m/s a un osservatore fermo. Che frequenza percepisce? (v suono = 340 m/s)" % (f, vs), fo, [f * (340 - vs) / 340, f, f * 340 / (340 + vs), f + vs], "Hz",
                  "Effetto Doppler: f′ = f × v : (v − vs) = %d × 340 : %d = %s Hz." % (f, 340 - vs, num(fo)))
    l, n = R.choice([(0.65, 1), (1, 2), (0.5, 1), (2, 3), (0.8, 2)])
    return nq("Una corda lunga %s m fissata agli estremi vibra nel modo con %d ventr%s. Quanto vale la lunghezza d’onda?" % (num(l), n, "e" if n == 1 else "i"), 2 * l / n, [l / n, l * n, 2 * l * n, l], "m",
              "Onde stazionarie: λ = 2L : n = 2 × %s : %d = %s m." % (num(l), n, num(2 * l / n)))


def f_ottonda(R):
    k = R.choice(["young", "young2", "ret", "c", "en"])
    if k == "young":
        lam, d, L = R.choice([(600e-9, 0.2e-3, 1), (500e-9, 0.5e-3, 2), (650e-9, 0.1e-3, 1.5), (450e-9, 0.3e-3, 1.2), (550e-9, 0.25e-3, 1)])
        y = lam * L / d
        return nq("Nell’esperimento di Young, λ = %s nm, d = %s mm, schermo a %s m. Quanto distano due frange chiare vicine?" % (num(lam * 1e9), num(d * 1e3), num(L)), y * 1000,
                  [lam * d / L * 1000, y * 100, y * 10000, d / (lam * L) / 1000], "mm", "Δy = λ L : d = %s m = %s mm." % (num(y), num(y * 1000)))
    if k == "young2":
        y, d, L = R.choice([(3e-3, 0.2e-3, 1), (2e-3, 0.5e-3, 2), (4.5e-3, 0.2e-3, 1.5), (1.2e-3, 0.5e-3, 1)])
        lam = y * d / L
        return nq("In una doppia fenditura con d = %s mm e schermo a %s m le frange distano %s mm. Qual è la lunghezza d’onda?" % (num(d * 1e3), num(L), num(y * 1e3)), lam * 1e9,
                  [y * L / d * 1e9 / 1e6, lam * 1e8, lam * 1e10, d / (y * L)], "nm", "λ = Δy d : L = %s m = %s nm." % (num(lam), num(lam * 1e9)))
    if k == "ret":
        n, lam = R.choice([(500, 600e-9), (300, 500e-9), (600, 550e-9), (400, 650e-9), (1000, 450e-9)])
        d = 1e-3 / n
        s = lam / d
        a = math.degrees(math.asin(s))
        return nq("Un reticolo ha %d righe/mm ed è illuminato con λ = %s nm. A quale angolo si trova il primo massimo?" % (n, num(lam * 1e9)), a, [s * 180, a * 2, 90 - a, math.degrees(math.atan(lam * n))], "°",
                  "d sen θ = λ con d = 1/%d mm: sen θ = %s → θ = %s°." % (n, num(s), num(a)))
    if k == "c":
        lam = R.choice([500e-9, 600e-9, 400e-9, 700e-9, 3e-2, 1])
        f = 3e8 / lam
        return nq("Qual è la frequenza di un’onda elettromagnetica con λ = %s m nel vuoto? (c = 3 × 10⁸ m/s)" % num(lam), f, [lam * 3e8, f / 1000, 3e8 / lam / 2, f * 10], "Hz", "f = c : λ = %s Hz." % num(f))
    lam = R.choice([500e-9, 600e-9, 400e-9, 700e-9, 300e-9])
    e = 6.63e-34 * 3e8 / lam
    return nq("Qual è l’energia di un fotone con λ = %s nm? (h = 6,63 × 10⁻³⁴ J·s, c = 3 × 10⁸ m/s)" % num(lam * 1e9), e, [6.63e-34 * lam / 3e8, e * 1e9, 6.63e-34 * 3e8, e / 2], "J",
              "E = h c : λ = %s J." % num(e))


def f_el(R):
    k = R.choice(["coul", "campo", "pot", "lav", "cond", "ener"])
    if k == "coul":
        q1, q2, r = R.choice([(2e-6, 3e-6, 0.1), (1e-6, 1e-6, 0.03), (5e-6, 4e-6, 0.2), (1e-9, 1e-9, 0.01), (3e-6, 6e-6, 0.3)])
        f = KC * q1 * q2 / r ** 2
        return nq("Due cariche di %s C e %s C sono a %s m nel vuoto. Quanto vale la forza tra loro? (k = 8,99 × 10⁹ N·m²/C²)" % (num(q1), num(q2), num(r)), f, [KC * q1 * q2 / r, f * 4, f / 2, KC * (q1 + q2) / r ** 2], "N",
                  "F = k q₁ q₂ : r² = %s N." % num(f))
    if k == "campo":
        q, r = R.choice([(2e-6, 0.3), (1e-9, 0.1), (5e-6, 1), (4e-6, 0.2), (1e-6, 0.05)])
        e = KC * q / r ** 2
        return nq("Quanto vale il campo elettrico a %s m da una carica di %s C? (k = 8,99 × 10⁹ N·m²/C²)" % (num(r), num(q)), e, [KC * q / r, e * 2, KC * q * r, e / 10], "N/C", "E = k q : r² = %s N/C." % num(e))
    if k == "pot":
        q, r = R.choice([(2e-9, 0.1), (1e-6, 1), (5e-9, 0.5), (3e-9, 0.3), (4e-9, 0.2)])
        v = KC * q / r
        return nq("Quanto vale il potenziale a %s m da una carica di %s C? (k = 8,99 × 10⁹ N·m²/C²)" % (num(r), num(q)), v, [KC * q / r ** 2, v * 2, KC * q * r, v / 100], "V", "V = k q : r = %s V." % num(v))
    if k == "lav":
        q, dv = R.choice([(2e-6, 100), (5e-3, 12), (1.6e-19, 1), (3e-6, 500), (1e-3, 230)])
        return nq("Una carica di %s C attraversa una differenza di potenziale di %d V. Quanto lavoro fa il campo?" % (num(q), dv), q * dv, [q / dv, dv / q, q * dv * 2, q * dv / 10], "J",
                  "L = q ΔV = %s J." % num(q * dv))
    if k == "cond":
        c, v = R.choice([(10e-6, 12), (100e-6, 9), (1e-6, 230), (47e-6, 5), (220e-6, 10)])
        return nq("Un condensatore da %s F è collegato a %d V. Quanta carica accumula?" % (num(c), v), c * v, [c / v, v / c, c * v * v, c * v / 2], "C", "Q = C V = %s C." % num(c * v))
    c, v = R.choice([(10e-6, 12), (100e-6, 9), (1e-6, 230), (47e-6, 5), (220e-6, 10)])
    return nq("Quanta energia immagazzina un condensatore da %s F a %d V?" % (num(c), v), 0.5 * c * v * v, [c * v, c * v * v, 0.5 * c * v, c / v], "J", "U = ½ C V² = %s J." % num(0.5 * c * v * v))


def f_cor(R):
    k = R.choice(["ohm", "serie", "par", "pot", "ris", "q", "joule"])
    if k == "ohm":
        v, r = R.choice([(12, 4), (230, 46), (9, 30), (4.5, 1.5), (24, 6), (6, 12)])
        return nq("Un resistore da %s Ω è sottoposto a %s V. Che corrente lo attraversa?" % (num(r), num(v)), v / r, [v * r, r / v, v / r * 10, v - r if v > r else r - v], "A", "I = V : R = %s A." % num(v / r))
    if k == "serie":
        a, b, c = R.choice([(10, 20, 30), (4, 6, 10), (100, 220, 330), (5, 5, 10), (12, 18, 30)])
        return nq("Tre resistori da %d Ω, %d Ω e %d Ω sono in serie. Quanto vale la resistenza equivalente?" % (a, b, c), a + b + c, [1 / (1 / a + 1 / b + 1 / c), a * b * c, (a + b + c) / 3, a + b], "Ω",
                  "In serie R = R₁ + R₂ + R₃ = %d Ω." % (a + b + c))
    if k == "par":
        a, b = R.choice([(6, 3), (10, 10), (4, 12), (20, 30), (60, 30), (8, 24)])
        return nq("Due resistori da %d Ω e %d Ω sono in parallelo. Quanto vale la resistenza equivalente?" % (a, b), a * b / (a + b), [a + b, (a + b) / 2, a * b, abs(a - b) if a != b else a * 2], "Ω",
                  "1/R = 1/%d + 1/%d → R = %s Ω." % (a, b, num(a * b / (a + b))))
    if k == "pot":
        v, i = R.choice([(230, 5), (12, 2), (230, 0.26), (9, 0.5), (230, 8.7), (5, 2)])
        return nq("Un apparecchio lavora a %s V con %s A. Quale potenza assorbe?" % (num(v), num(i)), v * i, [v / i, i / v, v * i * i, v + i], "W", "P = V I = %s W." % num(v * i))
    if k == "ris":
        e, ri, r = R.choice([(12, 1, 5), (9, 0.5, 4), (6, 0.2, 2.8), (1.5, 0.5, 2.5), (24, 2, 10)])
        return nq("Un generatore con fem %s V e resistenza interna %s Ω alimenta un carico da %s Ω. Che corrente circola?" % (num(e), num(ri), num(r)), e / (r + ri), [e / r, e / ri, e * (r + ri), e / (r - ri)], "A",
                  "I = fem : (R + r) = %s : %s = %s A." % (num(e), num(r + ri), num(e / (r + ri))))
    if k == "q":
        i, t = R.choice([(2, 10), (0.5, 60), (3, 20), (0.2, 300), (5, 4)])
        return nq("Una corrente di %s A circola per %d s. Quanta carica passa?" % (num(i), t), i * t, [i / t, t / i, i * t * 60, i + t], "C", "Q = I t = %s C." % num(i * t))
    i, r, t = R.choice([(2, 10, 60), (0.5, 100, 120), (3, 4, 30), (1, 50, 600)])
    return nq("Una corrente di %s A attraversa un resistore da %d Ω per %d s. Quanto calore si sviluppa per effetto Joule?" % (num(i), r, t), i * i * r * t, [i * r * t, i * i * r, i * r * r * t, i * i * t], "J",
              "Q = R I² t = %d × %s² × %d = %s J." % (r, num(i), t, num(i * i * r * t)))


def f_stech(R):
    k = R.choice(["mol", "molar", "dil", "mass", "lim", "resa"])
    if k == "mol":
        n, v = R.choice([(0.5, 0.25), (2, 1), (0.1, 0.5), (0.3, 0.2), (1.5, 3), (0.02, 0.1)])
        return nq("Sciogli %s mol di soluto fino a %s l di soluzione. Qual è la molarità?" % (num(n), num(v)), n / v, [n * v, v / n, n / v / 1000, n], "M", "M = n : V = %s mol/l." % num(n / v))
    if k == "molar":
        m, mm, v, f = R.choice([(5.85, 58.5, 0.5, "NaCl"), (4, 40, 0.25, "NaOH"), (9.8, 98, 1, "H₂SO₄"), (18, 180, 0.5, "glucosio"), (3.65, 36.5, 0.1, "HCl"), (10, 100, 0.2, "CaCO₃")])
        return nq("Sciogli %s g di %s (M = %s g/mol) fino a %s l. Qual è la molarità?" % (num(m), f, num(mm), num(v)), m / mm / v, [m / v, m / mm * v, mm / m / v, m / mm], "M",
                  "n = %s : %s = %s mol; M = %s : %s = %s mol/l." % (num(m), num(mm), num(m / mm), num(m / mm), num(v), num(m / mm / v)))
    if k == "dil":
        c1, v1, v2 = R.choice([(2, 0.1, 0.5), (1, 0.05, 0.25), (6, 0.01, 0.3), (0.5, 0.2, 1), (3, 0.04, 0.12)])
        return nq("Diluisci %s l di soluzione %s M fino a %s l. Qual è la nuova molarità?" % (num(v1), num(c1), num(v2)), c1 * v1 / v2, [c1 * v2 / v1, c1, c1 / v2, c1 * v1], "M",
                  "c₁ V₁ = c₂ V₂ → c₂ = %s × %s : %s = %s M." % (num(c1), num(v1), num(v2), num(c1 * v1 / v2)))
    if k == "mass":
        g, r = R.choice([(8, "2 H₂ + O₂ → 2 H₂O: quanti grammi d’acqua si ottengono da 8 g di idrogeno?"), (16, "CH₄ + 2 O₂ → CO₂ + 2 H₂O: quanti grammi di CO₂ da 16 g di metano?"),
                         (12, "C + O₂ → CO₂: quanti grammi di CO₂ da 12 g di carbonio?"), (46, "2 Na + Cl₂ → 2 NaCl: quanti grammi di NaCl da 46 g di sodio?"), (4, "2 H₂ + O₂ → 2 H₂O: quanti grammi d’acqua da 4 g di idrogeno?")])
        ans = {8: 72, 16: 44, 12: 44, 46: 117, 4: 36}[g]
        w = {8: [36, 18, 80], 16: [16, 88, 32], 12: [12, 32, 22], 46: [58.5, 46, 234], 4: [18, 72, 32]}[g]
        return nq(r + " (H = 1, C = 12, O = 16, Na = 23, Cl = 35,5)", ans, w, "g", "Si passa alle moli, si usa il rapporto dei coefficienti e si torna ai grammi: %s g." % num(ans))
    if k == "lim":
        a, b, ans, w, e = R.choice([(4, 4, "O₂", ["H₂", "nessuno", "H₂O"], "4 g di H₂ = 2 mol e servono 1 mol di O₂ = 32 g: con 4 g di O₂ l’ossigeno finisce prima."),
                                    (2, 32, "H₂", ["O₂", "nessuno", "H₂O"], "2 g di H₂ = 1 mol, 32 g di O₂ = 1 mol; ne servirebbero 2 di H₂ per 1 di O₂: finisce l’idrogeno."),
                                    (8, 64, "nessuno", ["H₂", "O₂", "H₂O"], "8 g di H₂ = 4 mol e 64 g di O₂ = 2 mol: rapporto 2 : 1 esatto, nessuno è in difetto.")])
        return it("Per 2 H₂ + O₂ → 2 H₂O si usano %d g di H₂ e %d g di O₂. Qual è il reagente limitante?" % (a, b), ans, w, e)
    t, o = R.choice([(50, 40), (100, 85), (80, 60), (20, 18), (64, 48)])
    return nq("Una reazione dovrebbe dare %d g di prodotto, ma se ne ottengono %d g. Qual è la resa percentuale?" % (t, o), o * 100 / t, [t * 100 / o, t - o, o, 100 - o * 100 / t], "%", "Resa = %d : %d × 100 = %s %%." % (o, t, num(o * 100 / t)))


def f_eq(R):
    k = R.choice(["kc", "ph", "ph2", "poh", "h", "kw"])
    if k == "kc":
        a, b, c, d = R.choice([(0.2, 0.4, 0.8, 1), (0.1, 0.1, 0.5, 1), (0.5, 0.2, 1, 1), (0.4, 0.5, 0.6, 1), (0.3, 0.3, 0.9, 1)])
        kc = c * c / (a * b)
        return nq("Per H₂ + I₂ ⇌ 2 HI all’equilibrio [H₂] = %s M, [I₂] = %s M, [HI] = %s M. Quanto vale Kc?" % (num(a), num(b), num(c)), kc, [c / (a * b), a * b / c ** 2, 2 * c / (a * b), c * c / (a + b)], "",
                  "Kc = [HI]² : ([H₂] [I₂]) = %s² : (%s × %s) = %s." % (num(c), num(a), num(b), num(kc)))
    if k == "ph":
        e = R.choice([1, 2, 3, 4, 5, 6])
        return nq("Una soluzione di acido forte ha [H⁺] = 10⁻%d M. Quanto vale il pH?" % e, e, [14 - e, -e if False else e + 1, e * 10, 7], "", "pH = −log [H⁺] = %d." % e)
    if k == "ph2":
        c, e = R.choice([(0.01, 2), (0.001, 3), (0.1, 1), (0.0001, 4)])
        return nq("Qual è il pH di una soluzione %s M di NaOH (base forte)?" % num(c), 14 - e, [e, 7 + e, 14 + e, 7], "", "pOH = %d, quindi pH = 14 − %d = %d." % (e, e, 14 - e))
    if k == "poh":
        p = R.choice([3, 5, 9, 11, 2, 12])
        return nq("Una soluzione ha pH %d. Quanto vale il pOH?" % p, 14 - p, [p, 7 - p if p < 7 else p - 7, 14 + p, p + 7 if p < 7 else p - 4], "", "pH + pOH = 14: pOH = %d." % (14 - p))
    if k == "h":
        p = R.choice([3, 5, 9, 11, 2, 12])
        return it("Una soluzione ha pH %d. Quanto vale [H⁺]?" % p, "10⁻%s M" % str(p).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")),
                  ["10⁻%s M" % str(14 - p).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")), "%d M" % p, "10%s M" % str(p).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))],
                  "[H⁺] = 10^(−pH) = 10⁻%s M." % str(p).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")))
    return it("Quanto vale il prodotto ionico dell’acqua Kw a 25 °C?", "1,0 × 10⁻¹⁴", ["1,0 × 10⁻⁷", "7", "14"], "Kw = [H⁺] [OH⁻] = 1,0 × 10⁻¹⁴ a 25 °C.")


def UNITS(grade):
    return [
        H("FI", "termodinamica", "I principi della termodinamica", "Termodinamica",
          "Lo studente applica il primo principio della termodinamica alle trasformazioni dei gas, studia macchine termiche e frigoriferi, il ciclo di Carnot, il secondo principio e l’entropia.",
          "sistema termodinamico, energia interna, lavoro termodinamico, primo principio, trasformazioni isoterme, isobare, isocore, adiabatiche, macchine termiche, rendimento, ciclo di Carnot, secondo principio, entropia",
          "ΔU = Q − L", "Nessuna macchina termica ha rendimento del 100 %.",
          ["Primo principio: ΔU = Q − L (Q assorbito positivo, L compiuto dal gas positivo).", "Una macchina termica assorbe Q₁ da una sorgente calda, produce lavoro e cede Q₂ alla fredda: η = L : Q₁.",
           "Secondo principio: non si può trasformare tutto il calore in lavoro. Il rendimento massimo è quello di Carnot, η = 1 − T₂ : T₁; l’entropia di un sistema isolato non diminuisce."],
          [("Una macchina di Carnot tra 500 K e 300 K: rendimento massimo?", ["η = 1 − 300 : 500.", "= 0,4."], "40 %.")],
          [("Il frigorifero crea il freddo.", "Toglie calore all’interno usando lavoro e lo cede all’esterno."), ("Nell’adiabatica la temperatura resta costante.", "Non c’è scambio di calore, ma la temperatura cambia.")],
          [("Perché le centrali hanno torri di raffreddamento?", "Devono cedere calore alla sorgente fredda: è inevitabile per il secondo principio."), ("Che cosa misura l’entropia?", "Il disordine e la dispersione dell’energia di un sistema.")],
          [("Trasformazioni", [("isoterma", "ΔU = 0 e Q = L"), ("isocora", "L = 0 e ΔU = Q"), ("adiabatica", "Q = 0 e ΔU = −L"), ("isobara", "L = p ΔV"), ("ciclica", "ΔU = 0 dopo un ciclo"),
                               ("espansione libera", "L = 0 e Q = 0")],
            "Che cosa vale in una trasformazione {k}?", "Quale trasformazione ha {v}?"),
           ("Concetti", [("energia interna", "somma delle energie delle molecole"), ("primo principio", "ΔU = Q − L"), ("secondo principio", "non tutto il calore diventa lavoro"), ("entropia", "misura della dispersione dell’energia"),
                         ("macchina termica", "trasforma calore in lavoro"), ("ciclo di Carnot", "ciclo reversibile di massimo rendimento"), ("pompa di calore", "porta calore dal freddo al caldo con lavoro"),
                         ("enunciato di Clausius", "il calore non passa da solo dal freddo al caldo")],
            "Che cos’è: {k}?", D),
           ("Esempi", {"le macchine termiche": ["motore a scoppio", "turbina a vapore", "motore diesel", "locomotiva a vapore"], "le macchine frigorifere": ["frigorifero", "condizionatore", "pompa di calore", "congelatore"],
                       "i processi irreversibili": ["attrito che scalda", "gas che si espande nel vuoto", "calore dal caldo al freddo", "mescolamento di due gas", "combustione"]})],
          ["ΔU = Q − L.", "Nessuna macchina termica ha rendimento 100 %.", "Il rendimento di Carnot è 1 − T₂ : T₁.", "In un’isoterma di un gas perfetto ΔU = 0.", "In un’adiabatica Q = 0.",
           "L’entropia di un sistema isolato non diminuisce.", "Il frigorifero usa lavoro per spostare calore."],
          [("Una macchina perfetta ha rendimento 100 %.", "È impossibile."), ("In un’isocora il lavoro è massimo.", "Il lavoro è nullo."), ("Il calore passa da solo dal freddo al caldo.", "Passa dal caldo al freddo."),
           ("In un’adiabatica la temperatura è costante.", "Q = 0, la temperatura cambia."), ("L’entropia di un sistema isolato diminuisce.", "Non diminuisce.")],
          "la termodinamica", "energy", calc=f_termo),

        H("FI", "onde-e-suono", "Onde meccaniche e suono", "Onde e suono",
          "Lo studente descrive onde trasversali e longitudinali, le grandezze delle onde, interferenza, onde stazionarie, il suono con intensità e livello sonoro e l’effetto Doppler.",
          "onde trasversali e longitudinali, ampiezza, periodo, frequenza, lunghezza d’onda, velocità, principio di sovrapposizione, interferenza, onde stazionarie, risonanza, suono, decibel, battimenti, effetto Doppler",
          "v = λ f", "Ogni 10 dB in più l’intensità del suono è 10 volte maggiore.",
          ["Un’onda trasporta energia senza trasportare materia. Trasversale: oscillazione perpendicolare alla propagazione; longitudinale: parallela.",
           "Quando due onde si incontrano si sommano (sovrapposizione): interferenza costruttiva o distruttiva. In una corda fissa si formano onde stazionarie, λ = 2L : n.",
           "Il livello sonoro si misura in decibel; l’effetto Doppler cambia la frequenza percepita se sorgente o osservatore si muovono."],
          [("Un suono di 340 Hz nell’aria (340 m/s): lunghezza d’onda?", ["λ = v : f.", "340 : 340."], "1 m.")],
          [("Il suono è un’onda trasversale.", "Nell’aria è longitudinale."), ("Un suono più acuto è più forte.", "Acuto vuol dire frequenza alta; forte vuol dire intensità alta.")],
          [("Perché la sirena cambia suono quando passa?", "Effetto Doppler: avvicinandosi la frequenza sembra più alta, allontanandosi più bassa."), ("Che cosa sono i battimenti?", "Variazioni periodiche di intensità tra due suoni di frequenze vicine.")],
          [("Grandezze", [("ampiezza", "massimo spostamento dalla posizione di equilibrio"), ("periodo", "tempo di un’oscillazione completa"), ("frequenza", "oscillazioni al secondo"), ("lunghezza d’onda", "distanza tra due creste"),
                          ("nodo", "punto fermo di un’onda stazionaria"), ("ventre", "punto di massima oscillazione"), ("decibel", "unità del livello sonoro"), ("risonanza", "grande oscillazione alla frequenza propria")],
            "Che cos’è: {k}?", D),
           ("Tipi di onda", [("onde in una corda di chitarra", "trasversale"), ("onde sismiche S", "trasversale"), ("onde elettromagnetiche", "trasversale"), ("onde su una molla tesa scossa di lato", "trasversale"),
                             ("suono nell’aria", "longitudinale"), ("onde sismiche P", "longitudinale"), ("ultrasuoni in acqua", "longitudinale"), ("molla compressa e rilasciata lungo l’asse", "longitudinale")],
            "Che tipo di onda è: {k}?", None, ("stazionaria pura", "elettrica")),
           ("Suono", {"le caratteristiche del suono": ["altezza", "intensità", "timbro"], "i suoni non udibili dall’uomo": ["infrasuoni", "ultrasuoni", "suoni sotto 20 Hz", "suoni sopra 20 000 Hz"],
                      "le applicazioni degli ultrasuoni": ["ecografia", "sonar", "pulizia a ultrasuoni", "ecolocalizzazione dei pipistrelli"]})],
          ["v = λ f.", "Il suono nell’aria è un’onda longitudinale.", "Le onde trasportano energia, non materia.", "In un’onda stazionaria i nodi sono fermi.", "L’effetto Doppler cambia la frequenza percepita.",
           "Gli ultrasuoni superano i 20 000 Hz.", "+10 dB significa intensità 10 volte maggiore."],
          [("Il suono è un’onda trasversale.", "È longitudinale."), ("Le onde trasportano materia.", "Trasportano energia."), ("+10 dB raddoppia l’intensità.", "La moltiplica per 10."),
           ("Avvicinandosi la sirena sembra più grave.", "Sembra più acuta."), ("Il suono si propaga nel vuoto.", "Serve un mezzo.")],
          "le onde", "waves-and-light", calc=f_onde),

        H("FI", "ottica-ondulatoria", "La luce come onda: interferenza e diffrazione", "Ottica ondulatoria",
          "Lo studente descrive il modello ondulatorio della luce, l’esperimento di Young, la diffrazione, il reticolo, la polarizzazione e lo spettro elettromagnetico.",
          "modello ondulatorio, principio di Huygens, interferenza, esperimento di Young, frange, diffrazione, reticolo di diffrazione, polarizzazione, spettro elettromagnetico, colore, lunghezza d’onda",
          "Interferenza: Δy = λ L : d", "La luce visibile va da circa 400 nm (violetto) a 700 nm (rosso).",
          ["Huygens: ogni punto di un fronte d’onda è sorgente di onde secondarie.", "Young: due fenditure producono frange chiare e scure; la distanza tra frange è Δy = λ L : d.",
           "La diffrazione è evidente quando la fenditura è confrontabile con λ. La polarizzazione dimostra che la luce è un’onda trasversale."],
          [("λ = 600 nm, d = 0,2 mm, L = 1 m: distanza tra le frange?", ["Δy = 600 × 10⁻⁹ × 1 : 0,0002.", "= 0,003 m."], "3 mm.")],
          [("La diffrazione avviene solo con le onde sonore.", "Avviene con tutte le onde, anche la luce."), ("La polarizzazione funziona anche con le onde longitudinali.", "Solo le onde trasversali si polarizzano.")],
          [("Perché le bolle di sapone sono colorate?", "Per l’interferenza della luce riflessa dalle due superfici della pellicola."), ("Come funzionano gli occhiali polarizzati?", "Lasciano passare una sola direzione di oscillazione e riducono i riflessi.")],
          [("Spettro", [("onde radio", "λ da metri a chilometri"), ("microonde", "λ da millimetri a decimetri"), ("infrarosso", "radiazione del calore"), ("luce visibile", "da 400 a 700 nm"),
                        ("ultravioletto", "abbronza e può danneggiare la pelle"), ("raggi X", "radiografie"), ("raggi gamma", "emessi dai nuclei radioattivi")],
            "Che cosa caratterizza: {k}?", "Quale radiazione ha questa caratteristica: {v}?"),
           ("Fenomeni", [("interferenza", "sovrapposizione di onde con frange chiare e scure"), ("diffrazione", "l’onda aggira un ostacolo o una fenditura"), ("polarizzazione", "oscillazione in una sola direzione"),
                         ("dispersione", "separazione dei colori in un prisma"), ("principio di Huygens", "ogni punto del fronte è una nuova sorgente"), ("reticolo di diffrazione", "molte fenditure che separano i colori"),
                         ("coerenza", "onde con differenza di fase costante")],
            "Che cos’è: {k}?", D),
           ("Colori ed esempi", {"i colori dalla λ più lunga alla più corta": ["rosso", "arancione", "giallo", "verde", "blu", "violetto"],
                                 "gli esempi di interferenza": ["bolle di sapone colorate", "macchia d’olio sull’asfalto bagnato", "colori delle ali di farfalla", "frange di Young"],
                                 "gli scienziati dell’ottica ondulatoria": ["Huygens", "Young", "Fresnel", "Maxwell"]})],
          ["La luce si comporta come un’onda.", "Δy = λ L : d.", "La polarizzazione dimostra che la luce è trasversale.", "Il rosso ha λ maggiore del violetto.", "Le bolle di sapone si colorano per interferenza.",
           "I raggi X hanno λ più corta della luce visibile.", "La diffrazione riguarda tutte le onde."],
          [("Il violetto ha λ maggiore del rosso.", "Il rosso ha λ maggiore."), ("Le onde longitudinali si polarizzano.", "Solo le trasversali."), ("La diffrazione non riguarda la luce.", "Riguarda anche la luce."),
           ("Le onde radio hanno λ più corta dei raggi X.", "È molto più lunga."), ("Δy = d L : λ.", "Δy = λ L : d.")],
          "l’ottica ondulatoria", "waves-and-light", calc=f_ottonda),

        H("FI", "campo-elettrico", "Cariche, campo e potenziale elettrico", "Campo elettrico",
          "Lo studente studia carica elettrica, elettrizzazione, legge di Coulomb, campo elettrico, energia potenziale e potenziale, condensatori e capacità.",
          "carica elettrica, conduttori e isolanti, elettrizzazione per strofinio, contatto e induzione, legge di Coulomb, campo elettrico, linee di campo, flusso, teorema di Gauss, potenziale, condensatore, capacità",
          "F = k q₁ q₂ : r²", "Il campo E = F : q si misura in N/C; il potenziale in volt.",
          ["La carica si conserva ed è multipla della carica elementare e = 1,6 × 10⁻¹⁹ C. Legge di Coulomb: F = k q₁ q₂ : r².",
           "Il campo elettrico è E = F : q; una carica puntiforme crea E = k q : r². Le linee di campo escono dalle cariche positive.",
           "Il potenziale è energia per unità di carica (V = U : q); un condensatore accumula Q = C V ed energia ½ C V²."],
          [("Se la distanza tra due cariche triplica, come cambia la forza?", ["F ∝ 1 : r².", "1 : 9."], "Diventa un nono.")],
          [("Le linee di campo entrano nelle cariche positive.", "Escono dalle positive ed entrano nelle negative."), ("Dentro un conduttore carico c’è un forte campo.", "In equilibrio il campo interno è nullo.")],
          [("Che cos’è la gabbia di Faraday?", "Un involucro conduttore che scherma il campo elettrico all’interno."), ("Perché i fulmini cadono sulle punte?", "Le cariche si concentrano dove la curvatura è maggiore (potere delle punte).")],
          [("Concetti", [("carica elementare", "1,6 × 10⁻¹⁹ C"), ("campo elettrico", "forza per unità di carica"), ("potenziale elettrico", "energia potenziale per unità di carica"), ("capacità", "carica per volt"),
                         ("teorema di Gauss", "il flusso dipende dalla carica interna"), ("gabbia di Faraday", "conduttore che scherma il campo interno"), ("elettronvolt", "energia di un elettrone accelerato da 1 V"),
                         ("costante di Coulomb", "8,99 × 10⁹ N·m²/C²")],
            "Che cos’è o quanto vale: {k}?", D),
           ("Unità", [("carica", "coulomb"), ("campo elettrico", "newton al coulomb"), ("potenziale", "volt"), ("capacità", "farad"), ("energia", "joule"), ("forza", "newton")],
            "In che unità si misura: {k}?", "Quale grandezza si misura in {v}?"),
           ("Elettrizzazione", {"i modi di elettrizzare un corpo": ["strofinio", "contatto", "induzione", "polarizzazione di un isolante"], "i buoni conduttori": ["rame", "argento", "alluminio", "acqua salata", "corpo umano"],
                                "gli isolanti": ["vetro", "plastica", "gomma", "aria secca", "ambra"]})],
          ["F = k q₁ q₂ : r².", "La carica si conserva.", "Il campo dentro un conduttore in equilibrio è nullo.", "Il potenziale si misura in volt.", "Q = C V.", "Le linee di campo escono dalle cariche positive.",
           "La carica elementare vale 1,6 × 10⁻¹⁹ C."],
          [("Se r raddoppia F dimezza.", "Diventa un quarto."), ("Le linee di campo escono dalle cariche negative.", "Escono dalle positive."), ("La capacità si misura in volt.", "Si misura in farad."),
           ("La carica si può creare dal nulla.", "Si conserva."), ("Dentro un conduttore carico il campo è massimo.", "È nullo.")],
          "il campo elettrico", "energy", calc=f_el),

        H("FI", "corrente-elettrica", "La corrente elettrica e i circuiti", "Corrente elettrica",
          "Lo studente definisce intensità di corrente e resistenza, applica le leggi di Ohm, risolve circuiti in serie e in parallelo, considera la resistenza interna e l’effetto Joule.",
          "intensità di corrente, ampere, generatore, forza elettromotrice, prima e seconda legge di Ohm, resistività, resistori in serie e in parallelo, leggi di Kirchhoff, resistenza interna, potenza, effetto Joule",
          "V = R I e P = V I", "In serie le resistenze si sommano; in parallelo si sommano gli inversi.",
          ["L’intensità di corrente è la carica al secondo: I = Q : t (ampere).", "Prima legge di Ohm: V = R I. Seconda: R = ρ L : S (la resistenza cresce con la lunghezza e diminuisce con la sezione).",
           "La potenza è P = V I = R I²; l’energia dissipata in calore è l’effetto Joule. Un generatore reale ha resistenza interna."],
          [("Due resistori da 6 Ω e 3 Ω in parallelo: R equivalente?", ["1/R = 1/6 + 1/3 = 1/2.", "R = 2."], "2 Ω.")],
          [("In parallelo la resistenza totale è maggiore.", "È minore della più piccola."), ("La corrente si consuma nei resistori.", "La corrente è la stessa in serie; si consuma l’energia.")],
          [("Perché i fili lunghi scaldano?", "Hanno resistenza maggiore e dissipano energia per effetto Joule."), ("Che cosa dice la legge dei nodi di Kirchhoff?", "La somma delle correnti entranti in un nodo è uguale alla somma di quelle uscenti.")],
          [("Leggi", [("prima legge di Ohm", "V = R I"), ("seconda legge di Ohm", "R = ρ L : S"), ("legge dei nodi", "somma delle correnti entranti = uscenti"), ("legge delle maglie", "somma delle tensioni in una maglia = 0"),
                      ("effetto Joule", "P = R I²"), ("resistori in serie", "R = R₁ + R₂"), ("resistori in parallelo", "1/R = 1/R₁ + 1/R₂")],
            "Che cosa esprime: {k}?", "Quale legge esprime {v}?"),
           ("Strumenti e componenti", [("amperometro", "misura la corrente, in serie"), ("voltmetro", "misura la tensione, in parallelo"), ("ohmmetro", "misura la resistenza"), ("fusibile", "si fonde se la corrente è eccessiva"),
                                       ("resistore", "limita la corrente"), ("generatore", "mantiene una differenza di potenziale"), ("interruttore differenziale", "interrompe la corrente in caso di dispersione")],
            "Che funzione ha: {k}?", D),
           ("Materiali", {"i conduttori metallici": ["rame", "argento", "alluminio", "oro", "tungsteno"], "i semiconduttori": ["silicio", "germanio", "arseniuro di gallio"],
                          "gli apparecchi che sfruttano l’effetto Joule": ["stufa elettrica", "ferro da stiro", "bollitore", "phon", "tostapane"]})],
          ["V = R I.", "In serie le resistenze si sommano.", "In parallelo la resistenza totale diminuisce.", "P = V I.", "L’amperometro si collega in serie.", "Il voltmetro si collega in parallelo.",
           "Un filo più lungo ha resistenza maggiore."],
          [("In parallelo la resistenza aumenta.", "Diminuisce."), ("L’amperometro si collega in parallelo.", "In serie."), ("Un filo più spesso ha resistenza maggiore.", "Ha resistenza minore."),
           ("P = V : I.", "P = V I."), ("La corrente si consuma nei resistori.", "In serie è uguale ovunque.")],
          "la corrente elettrica", "energy", calc=f_cor),

        H("CH", "stechiometria-e-soluzioni", "Stechiometria e soluzioni", "Stechiometria e soluzioni",
          "Lo studente bilancia le reazioni, esegue calcoli stechiometrici con il reagente limitante e la resa e usa le concentrazioni delle soluzioni (molarità, % m/m, diluizioni).",
          "equazione chimica, bilanciamento, coefficienti stechiometrici, calcoli stechiometrici, reagente limitante, resa percentuale, soluzioni, molarità, molalità, frazione molare, diluizione, proprietà colligative",
          "Si ragiona in moli, non in grammi", "Il reagente limitante finisce per primo e decide quanto prodotto si forma.",
          ["Un’equazione bilanciata ha lo stesso numero di atomi di ogni elemento nei due membri.", "I coefficienti indicano il rapporto tra le moli: si passa da grammi a moli, si usa il rapporto e si torna ai grammi.",
           "La molarità è M = n : V (mol/l). Diluendo vale c₁ V₁ = c₂ V₂."],
          [("Quante moli di acqua da 3 mol di H₂ (2 H₂ + O₂ → 2 H₂O)?", ["Il rapporto H₂ : H₂O è 2 : 2.", "3 mol di H₂ → 3 mol di H₂O."], "3 mol.")],
          [("I coefficienti indicano il rapporto tra i grammi.", "Indicano il rapporto tra le moli."), ("Diluendo cambia il numero di moli di soluto.", "Le moli restano uguali; cambia il volume.")],
          [("Perché d’inverno si sparge sale sulle strade?", "Il sale abbassa la temperatura di congelamento dell’acqua (proprietà colligativa)."), ("Che cos’è la resa?", "Il rapporto tra il prodotto ottenuto e quello teorico.")],
          [("Bilanciamento", {"le equazioni bilanciate correttamente": ["2 H₂ + O₂ → 2 H₂O", "N₂ + 3 H₂ → 2 NH₃", "CH₄ + 2 O₂ → CO₂ + 2 H₂O", "2 Na + Cl₂ → 2 NaCl", "4 Fe + 3 O₂ → 2 Fe₂O₃",
                                                          "C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O", "2 Mg + O₂ → 2 MgO"],
                               "le equazioni non bilanciate": ["H₂ + O₂ → H₂O", "N₂ + H₂ → 2 NH₃", "CH₄ + O₂ → CO₂ + 2 H₂O", "Na + Cl₂ → NaCl", "2 Fe + 3 O₂ → Fe₂O₃",
                                                               "C₃H₈ + 3 O₂ → 3 CO₂ + 4 H₂O", "Mg + O₂ → 2 MgO"]}),
           ("Concetti", [("molarità", "moli di soluto per litro di soluzione"), ("molalità", "moli di soluto per kg di solvente"), ("frazione molare", "moli di un componente sulle moli totali"),
                         ("reagente limitante", "il reagente che finisce per primo"), ("reagente in eccesso", "il reagente che avanza"), ("resa percentuale", "prodotto ottenuto su prodotto teorico × 100"),
                         ("innalzamento ebullioscopico", "il soluto alza la temperatura di ebollizione"), ("pressione osmotica", "pressione che ferma l’osmosi")],
            "Che cos’è: {k}?", D),
           ("Proprietà colligative", {"le proprietà colligative": ["abbassamento crioscopico", "innalzamento ebullioscopico", "pressione osmotica", "abbassamento della tensione di vapore"],
                                      "le applicazioni delle proprietà colligative": ["sale sulle strade ghiacciate", "antigelo nel radiatore", "conservazione sotto sale", "flebo isotoniche"],
                                      "le unità di concentrazione": ["mol/l", "mol/kg", "% m/m", "g/l", "ppm"]})],
          ["I coefficienti indicano il rapporto tra le moli.", "Il reagente limitante finisce per primo.", "M = n : V.", "Diluendo le moli di soluto non cambiano.", "c₁ V₁ = c₂ V₂.",
           "Il sale abbassa la temperatura di congelamento.", "In un’equazione bilanciata gli atomi si conservano."],
          [("I coefficienti sono rapporti in grammi.", "Sono rapporti in moli."), ("Diluendo aumentano le moli.", "Restano uguali."), ("Il reagente in eccesso decide il prodotto.", "Lo decide il limitante."),
           ("Il sale alza la temperatura di congelamento.", "La abbassa."), ("La molarità è in grammi per litro.", "È in moli per litro.")],
          "la stechiometria", "matter", calc=f_stech),

        H("CH", "equilibrio-chimico", "Velocità di reazione ed equilibrio chimico", "Equilibrio chimico",
          "Lo studente descrive i fattori che influenzano la velocità di reazione, l’energia di attivazione e i catalizzatori, l’equilibrio dinamico, la costante di equilibrio e il principio di Le Châtelier.",
          "velocità di reazione, teoria degli urti, energia di attivazione, catalizzatori, concentrazione, temperatura, superficie, equilibrio dinamico, costante di equilibrio, quoziente di reazione, principio di Le Châtelier",
          "All’equilibrio le due velocità sono uguali", "Le Châtelier: il sistema si oppone alla perturbazione.",
          ["La velocità cresce con concentrazione, temperatura, superficie di contatto e catalizzatori; il catalizzatore abbassa l’energia di attivazione.",
           "All’equilibrio la reazione diretta e quella inversa hanno la stessa velocità: le concentrazioni restano costanti.",
           "Per aA + bB ⇌ cC + dD: Kc = [C]ᶜ [D]ᵈ : ([A]ᵃ [B]ᵇ). Se si perturba l’equilibrio, il sistema si sposta per ridurre la perturbazione."],
          [("In N₂ + 3 H₂ ⇌ 2 NH₃ si aumenta la pressione. Dove si sposta l’equilibrio?", ["A destra ci sono meno moli di gas.", "Il sistema riduce la pressione."], "Verso destra.")],
          [("All’equilibrio la reazione si ferma.", "Continua nei due sensi alla stessa velocità."), ("Il catalizzatore sposta l’equilibrio.", "Fa solo raggiungere prima l’equilibrio.")],
          [("Perché il cibo in frigorifero si conserva di più?", "A temperatura bassa le reazioni sono più lente."), ("Che cosa indica una Kc molto grande?", "All’equilibrio prevalgono i prodotti.")],
          [("Le Châtelier", [("si aggiunge un reagente", "verso i prodotti"), ("si toglie un prodotto", "verso i prodotti"), ("si aggiunge un prodotto", "verso i reagenti"), ("si toglie un reagente", "verso i reagenti"),
                             ("si aumenta la pressione in N₂ + 3 H₂ ⇌ 2 NH₃", "verso i prodotti"), ("si diminuisce la pressione in N₂ + 3 H₂ ⇌ 2 NH₃", "verso i reagenti"), ("si aggiunge un catalizzatore", "non si sposta")],
            "Dove si sposta l’equilibrio se {k}?", None, ("si ferma",)),
           ("Concetti", [("energia di attivazione", "energia minima per far avvenire la reazione"), ("catalizzatore", "abbassa l’energia di attivazione senza consumarsi"), ("equilibrio dinamico", "velocità diretta uguale a quella inversa"),
                         ("costante di equilibrio", "rapporto tra prodotti e reagenti all’equilibrio"), ("complesso attivato", "struttura instabile al massimo di energia"), ("quoziente di reazione", "rapporto calcolato fuori equilibrio"),
                         ("enzima", "catalizzatore biologico")],
            "Che cos’è: {k}?", D),
           ("Velocità", {"i fattori che aumentano la velocità di reazione": ["temperatura più alta", "concentrazione maggiore", "polvere invece di blocchi", "catalizzatore", "agitazione"],
                         "i catalizzatori": ["marmitta catalitica", "enzimi", "platino", "ferro nel processo Haber", "ossido di manganese per l’acqua ossigenata"],
                         "le reazioni lente": ["arrugginimento del ferro", "formazione delle stalattiti", "maturazione del vino", "decomposizione della plastica"]})],
          ["All’equilibrio le velocità diretta e inversa sono uguali.", "Il catalizzatore abbassa l’energia di attivazione.", "Il catalizzatore non sposta l’equilibrio.", "Aggiungendo un reagente l’equilibrio va verso i prodotti.",
           "La temperatura aumenta la velocità di reazione.", "Una Kc grande indica molti prodotti.", "Gli enzimi sono catalizzatori."],
          [("All’equilibrio la reazione si ferma.", "Continua nei due sensi."), ("Il catalizzatore sposta l’equilibrio.", "Non lo sposta."), ("Il catalizzatore si consuma.", "Resta invariato."),
           ("A bassa temperatura le reazioni sono più veloci.", "Sono più lente."), ("Togliendo un prodotto l’equilibrio va verso i reagenti.", "Va verso i prodotti.")],
          "l’equilibrio chimico", "matter", calc=f_eq),

        H("CH", "acidi-basi-e-ph", "Acidi, basi e pH", "Acidi e basi",
          "Lo studente applica le teorie di Arrhenius, Brønsted-Lowry e Lewis, calcola il pH di acidi e basi forti, descrive acidi deboli, idrolisi, soluzioni tampone e titolazioni.",
          "teoria di Arrhenius, Brønsted-Lowry, Lewis, coppie coniugate, prodotto ionico dell’acqua, pH, pOH, acidi e basi forti e deboli, Ka, idrolisi salina, soluzioni tampone, indicatori, titolazione",
          "pH = −log [H⁺]", "A 25 °C pH + pOH = 14.",
          ["Arrhenius: gli acidi liberano H⁺, le basi OH⁻. Brønsted-Lowry: l’acido cede un protone, la base lo accetta.", "Kw = [H⁺] [OH⁻] = 1,0 × 10⁻¹⁴; pH = −log [H⁺] e pH + pOH = 14.",
           "Gli acidi forti sono completamente dissociati; quelli deboli in parte (Ka). Una soluzione tampone resiste alle variazioni di pH."],
          [("Qual è il pH di HCl 0,001 M?", ["È un acido forte: [H⁺] = 10⁻³.", "pH = 3."], "3.")],
          [("Un acido concentrato è sempre forte.", "Forte significa completamente dissociato, non concentrato."), ("Passando da pH 4 a pH 3 l’acidità aumenta di poco.", "[H⁺] diventa 10 volte maggiore.")],
          [("A che cosa serve una titolazione?", "A trovare la concentrazione di un acido o di una base con una soluzione a concentrazione nota."), ("Perché il sangue ha pH quasi costante?", "Contiene sistemi tampone, come quello del bicarbonato.")],
          [("Forti o deboli", [("HCl", "acido forte"), ("HNO₃", "acido forte"), ("H₂SO₄", "acido forte"), ("CH₃COOH", "acido debole"), ("HF", "acido debole"), ("H₂CO₃", "acido debole"),
                               ("NaOH", "base forte"), ("KOH", "base forte"), ("NH₃", "base debole")],
            "Come si classifica: {k}?", None),
           ("Coppie coniugate", [("HCl", "Cl⁻"), ("H₂O come acido", "OH⁻"), ("NH₄⁺", "NH₃"), ("CH₃COOH", "CH₃COO⁻"), ("H₃O⁺", "H₂O"), ("H₂CO₃", "HCO₃⁻"), ("HF", "F⁻")],
            "Qual è la base coniugata di {k}?", "Di quale acido è la base coniugata {v}?"),
           ("Teorie e strumenti", {"gli indicatori acido-base": ["fenolftaleina", "tornasole", "metilarancio", "blu di bromotimolo", "indicatore universale"],
                                   "le coppie che formano soluzioni tampone": ["CH₃COOH e CH₃COONa", "H₂CO₃ e NaHCO₃", "NH₃ e NH₄Cl", "H₂PO₄⁻ e HPO₄²⁻"],
                                   "le basi di Lewis": ["NH₃", "H₂O", "OH⁻", "Cl⁻", "CN⁻"]})],
          ["pH = −log [H⁺].", "pH + pOH = 14 a 25 °C.", "HCl è un acido forte.", "L’acido acetico è debole.", "Per Brønsted l’acido cede un protone.", "Una soluzione tampone resiste alle variazioni di pH.",
           "Da pH 4 a pH 3 [H⁺] diventa 10 volte maggiore."],
          [("pH 3 è basico.", "È acido."), ("L’acido acetico è forte.", "È debole."), ("Per Brønsted la base cede un protone.", "La base accetta un protone."), ("pH + pOH = 7.", "pH + pOH = 14."),
           ("Concentrato vuol dire forte.", "Forte vuol dire completamente dissociato.")],
          "acidi e basi", "matter", calc=f_eq),

        H("CH", "ossidoriduzioni-ed-elettrochimica", "Ossidoriduzioni ed elettrochimica", "Redox ed elettrochimica",
          "Lo studente assegna i numeri di ossidazione, riconosce ossidazione e riduzione, bilancia le redox, descrive la pila Daniell, i potenziali standard e l’elettrolisi.",
          "numero di ossidazione, ossidazione, riduzione, ossidante, riducente, bilanciamento redox, pila Daniell, anodo, catodo, ponte salino, potenziale standard di riduzione, forza elettromotrice, elettrolisi, corrosione",
          "Ossidazione = perdita di elettroni", "Nella pila l’ossidazione avviene all’anodo, la riduzione al catodo.",
          ["Il numero di ossidazione indica la carica formale di un atomo. Chi si ossida perde elettroni; chi si riduce li acquista.", "Il riducente si ossida; l’ossidante si riduce.",
           "In una pila la reazione redox spontanea produce corrente: fem = E°catodo − E°anodo. Nell’elettrolisi la corrente forza una reazione non spontanea."],
          [("Nella reazione Zn + Cu²⁺ → Zn²⁺ + Cu chi si ossida?", ["Lo zinco passa da 0 a +2.", "Perde due elettroni."], "Lo zinco.")],
          [("Nella pila il catodo è sempre negativo.", "Nella pila il catodo è positivo; nell’elettrolisi è negativo."), ("L’ossidante si ossida.", "L’ossidante si riduce e ossida l’altro.")],
          [("Che cosa fa il ponte salino?", "Chiude il circuito e mantiene neutre le soluzioni."), ("Perché il ferro arrugginisce?", "Il ferro si ossida a contatto con ossigeno e acqua.")],
          [("Numeri di ossidazione", [("O in H₂O", "−2"), ("H in H₂O", "+1"), ("Na in NaCl", "+1"), ("Cl in NaCl", "−1"), ("O in O₂", "0"), ("C in CO₂", "+4"), ("S in H₂SO₄", "+6"),
                                      ("Mn in KMnO₄", "+7"), ("Fe in Fe₂O₃", "+3"), ("N in NH₃", "−3")],
            "Qual è il numero di ossidazione di {k}?", None),
           ("Concetti", [("ossidazione", "perdita di elettroni"), ("riduzione", "acquisto di elettroni"), ("ossidante", "specie che si riduce"), ("riducente", "specie che si ossida"),
                         ("anodo di una pila", "elettrodo dove avviene l’ossidazione"), ("catodo di una pila", "elettrodo dove avviene la riduzione"), ("ponte salino", "chiude il circuito tra le semicelle"),
                         ("elettrolisi", "reazione redox forzata dalla corrente")],
            "Che cos’è: {k}?", D),
           ("Applicazioni", {"le applicazioni dell’elettrolisi": ["produzione di alluminio", "galvanostetica", "cromatura", "produzione di cloro", "raffinazione del rame"],
                             "i dispositivi elettrochimici": ["pila Daniell", "batteria al litio", "accumulatore al piombo", "pila a combustibile", "pila alcalina"],
                             "i modi di proteggere dalla corrosione": ["verniciatura", "zincatura", "anodo sacrificale", "acciaio inossidabile", "protezione catodica"]})],
          ["L’ossidazione è una perdita di elettroni.", "Nella pila l’anodo è il polo dove avviene l’ossidazione.", "Il riducente si ossida.", "Il numero di ossidazione di O₂ è 0.", "L’elettrolisi è una redox non spontanea.",
           "Lo zinco protegge il ferro dalla corrosione.", "La fem di una pila è E°catodo − E°anodo."],
          [("L’ossidazione è un acquisto di elettroni.", "È una perdita."), ("L’ossidante si ossida.", "Si riduce."), ("Nella pila l’ossidazione avviene al catodo.", "Avviene all’anodo."),
           ("Il numero di ossidazione di O in H₂O è +2.", "È −2."), ("L’elettrolisi è spontanea.", "È forzata dalla corrente.")],
          "le ossidoriduzioni", "matter"),

        H("BI", "anatomia-e-fisiologia-umana", "Anatomia e fisiologia del corpo umano", "Il corpo umano",
          "Lo studente descrive l’organizzazione del corpo umano e la fisiologia degli apparati digerente, respiratorio, cardiovascolare, escretore, nervoso, endocrino e immunitario e l’omeostasi.",
          "tessuti, organi, apparati, omeostasi, digestione, enzimi digestivi, respirazione, emoglobina, cuore, circolazione, rene, nefrone, neurone, potenziale d’azione, sinapsi, ormoni, feedback, sistema immunitario, anticorpi",
          "Gli apparati collaborano per l’omeostasi", "Il feedback negativo riporta i valori alla normalità.",
          ["Il corpo è organizzato in tessuti (epiteliale, connettivo, muscolare, nervoso), organi e apparati.",
           "Digestione, respirazione, circolazione ed escrezione portano nutrienti e ossigeno alle cellule ed eliminano gli scarti.",
           "Sistema nervoso ed endocrino regolano l’omeostasi con meccanismi a feedback negativo; il sistema immunitario difende con risposte innata e adattativa."],
          [("Che cosa succede se la glicemia sale dopo un pasto?", ["Il pancreas libera insulina.", "Le cellule assorbono glucosio."], "La glicemia torna normale.")],
          [("I globuli bianchi trasportano ossigeno.", "Lo trasportano i globuli rossi con l’emoglobina."), ("Gli anticorpi uccidono direttamente i virus dentro le cellule.", "Li neutralizzano fuori dalle cellule; le cellule infette sono distrutte dai linfociti T.")],
          [("Che cos’è il nefrone?", "L’unità funzionale del rene, che filtra il sangue e forma l’urina."), ("Come funziona un vaccino?", "Stimola la memoria immunitaria senza causare la malattia.")],
          [("Enzimi e ormoni", [("amilasi salivare", "digerisce l’amido"), ("pepsina", "digerisce le proteine nello stomaco"), ("lipasi", "digerisce i grassi"), ("insulina", "abbassa la glicemia"),
                                ("glucagone", "alza la glicemia"), ("ADH", "riduce l’acqua persa con l’urina"), ("adrenalina", "prepara il corpo all’emergenza"), ("tiroxina", "regola il metabolismo")],
            "Che cosa fa: {k}?", D),
           ("Strutture", [("alveolo", "scambio di gas nei polmoni"), ("villo intestinale", "assorbimento dei nutrienti"), ("nefrone", "filtrazione del sangue"), ("sinapsi", "trasmissione tra neuroni"),
                          ("valvola mitrale", "separa atrio e ventricolo sinistri"), ("linfocita B", "produce anticorpi"), ("linfocita T killer", "distrugge le cellule infette"), ("glomerulo", "gomitolo di capillari che filtra il sangue")],
            "Che funzione ha: {k}?", D),
           ("Tessuti e difese", {"i tessuti connettivi": ["sangue", "osso", "cartilagine", "tessuto adiposo", "tendini"], "le difese innate": ["pelle", "muco", "febbre", "infiammazione", "fagociti"],
                                 "le difese adattative": ["anticorpi", "linfociti B", "linfociti T", "cellule della memoria", "immunità dopo il vaccino"]})],
          ["L’insulina abbassa la glicemia.", "Il nefrone filtra il sangue.", "Gli alveoli scambiano i gas.", "I linfociti B producono anticorpi.", "Il feedback negativo mantiene l’omeostasi.",
           "La pepsina digerisce le proteine.", "Il vaccino crea memoria immunitaria."],
          [("L’insulina alza la glicemia.", "La abbassa."), ("I globuli bianchi trasportano ossigeno.", "Lo fanno i globuli rossi."), ("La lipasi digerisce l’amido.", "Digerisce i grassi."),
           ("Il nefrone fa parte del polmone.", "Fa parte del rene."), ("I vaccini causano la malattia.", "Stimolano la memoria immunitaria.")],
          "il corpo umano", "living-things-and-ecosystems"),
    ]
