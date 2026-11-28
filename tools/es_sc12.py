# -*- coding: utf-8 -*-
"""España / 2.º de Bachillerato: Biología, Química, Física, Geología y Ciencias Ambientales"""
import math
from es_sci import H, nq, num, it

D = "¿Qué corresponde a esta descripción: {v}?"
GG = 6.67e-11
MT, RT = 5.97e24, 6.37e6
KC = 9e9
H_ = 6.63e-34
C_ = 3e8
E_ = 1.6e-19


def f_grav(R):
    k = R.choice(["F", "g", "gh", "vorb", "vesc", "T"])
    if k == "F":
        m1, m2, d = R.choice([(100, 50, 2), (1000, 1000, 10), (5.97e24, 1000, 6.37e6), (7.35e22, 70, 1.74e6), (60, 70, 1)])
        F = GG * m1 * m2 / d ** 2
        return nq("¿Con qué fuerza se atraen dos masas de %s kg y %s kg separadas %s m? (G = 6,67 · 10⁻¹¹ N·m²/kg²)" % (num(m1), num(m2), num(d)), F, [GG * m1 * m2 / d, F * 1e3, GG * (m1 + m2) / d ** 2], "N",
                  "F = G · m₁ · m₂ : d² = %s N." % num(F))
    if k == "g":
        M, Rr, nm = R.choice([(7.35e22, 1.74e6, "la Luna"), (6.42e23, 3.39e6, "Marte"), (5.97e24, 6.37e6, "la Tierra"), (1.9e27, 7.15e7, "Júpiter")])
        g = GG * M / Rr ** 2
        return nq("Calcula la gravedad en la superficie de %s (M = %s kg, R = %s m)." % (nm, num(M), num(Rr)), g, [GG * M / Rr, g * 2, GG * M / Rr ** 3], "m/s²",
                  "g = G · M : R² = %s m/s²." % num(g))
    if k == "gh":
        h = R.choice([6.37e6, 3.6e7, 4e5, 1.27e7, 2e6])
        g = GG * MT / (RT + h) ** 2
        return nq("¿Cuánto vale g a %s m sobre la superficie terrestre? (M = 5,97 · 10²⁴ kg, R = 6,37 · 10⁶ m)" % num(h), g, [GG * MT / h ** 2, 9.8 * RT / (RT + h), 9.8 - h / 1e6], "m/s²",
                  "g = G · M : (R + h)² = %s m/s²." % num(g))
    if k == "vorb":
        h = R.choice([4e5, 3.59e7, 2e6, 6.37e6, 1e6])
        v = math.sqrt(GG * MT / (RT + h))
        return nq("¿Qué velocidad orbital tiene un satélite a %s m de altura? (M = 5,97 · 10²⁴ kg, R = 6,37 · 10⁶ m)" % num(h), v, [math.sqrt(GG * MT / h), math.sqrt(2 * GG * MT / (RT + h)), GG * MT / (RT + h)], "m/s",
                  "v = √(G · M : (R + h)) = %s m/s." % num(v))
    if k == "vesc":
        M, Rr, nm = R.choice([(5.97e24, 6.37e6, "la Tierra"), (7.35e22, 1.74e6, "la Luna"), (6.42e23, 3.39e6, "Marte")])
        v = math.sqrt(2 * GG * M / Rr)
        return nq("Calcula la velocidad de escape de %s (M = %s kg, R = %s m)." % (nm, num(M), num(Rr)), v, [math.sqrt(GG * M / Rr), 2 * GG * M / Rr, v * 2], "m/s",
                  "v = √(2 · G · M : R) = %s m/s." % num(v))
    T1, a1, a2 = R.choice([(1, 1, 1.52), (1, 1, 5.2), (1, 1, 9.54), (1, 1, 0.72), (1, 1, 30)])
    T2 = T1 * (a2 / a1) ** 1.5
    return nq("Un planeta está a %s UA del Sol. Por la tercera ley de Kepler, ¿cuántos años dura su órbita?" % num(a2), T2, [a2, a2 ** 2, a2 ** 3], "años",
              "T² ∝ a³: T = %s^(3/2) = %s años." % (num(a2), num(T2)))


def f_elec(R):
    k = R.choice(["F", "E", "V", "W", "Eq"])
    if k == "F":
        q1, q2, d = R.choice([(2e-6, 3e-6, 0.1), (1e-6, 1e-6, 0.01), (5e-6, 2e-6, 0.3), (4e-9, 6e-9, 0.02), (1e-6, 8e-6, 0.2)])
        F = KC * q1 * q2 / d ** 2
        return nq("¿Qué fuerza hay entre %s C y %s C separadas %s m? (K = 9 · 10⁹ N·m²/C²)" % (num(q1), num(q2), num(d)), F, [KC * q1 * q2 / d, F / 100, KC * (q1 + q2) / d ** 2], "N",
                  "F = K · q₁ · q₂ : d² = %s N." % num(F))
    if k == "E":
        q, d = R.choice([(2e-6, 0.1), (1e-9, 0.01), (5e-6, 0.5), (3e-6, 0.3), (8e-9, 0.04)])
        E = KC * q / d ** 2
        return nq("¿Qué campo eléctrico crea una carga de %s C a %s m? (K = 9 · 10⁹ N·m²/C²)" % (num(q), num(d)), E, [KC * q / d, E * d, KC * q * d], "N/C", "E = K · q : d² = %s N/C." % num(E))
    if k == "V":
        q, d = R.choice([(2e-6, 0.1), (1e-9, 0.01), (5e-6, 0.5), (3e-6, 0.3), (4e-9, 0.02)])
        V = KC * q / d
        return nq("¿Qué potencial eléctrico crea una carga de %s C a %s m? (K = 9 · 10⁹ N·m²/C²)" % (num(q), num(d)), V, [KC * q / d ** 2, V * d, KC * q * d], "V", "V = K · q : d = %s V." % num(V))
    if k == "W":
        q, dV = R.choice([(2e-6, 100), (1.6e-19, 1000), (5e-6, 300), (1e-3, 12), (3e-6, 5000)])
        return nq("¿Qué trabajo hace el campo al mover %s C entre dos puntos con una diferencia de potencial de %s V?" % (num(q), num(dV)), q * dV, [q / dV, dV / q, q * dV * 1000], "J",
                  "W = q · ΔV = %s J." % num(q * dV))
    E, d = R.choice([(1000, 0.02), (5000, 0.01), (200, 0.5), (3e4, 0.002)])
    return nq("Entre dos placas paralelas hay un campo uniforme de %s N/C y están separadas %s m. ¿Qué diferencia de potencial hay?" % (num(E), num(d)), E * d, [E / d, d / E, E * d * 100], "V",
              "ΔV = E · d = %s V." % num(E * d))


def f_mag(R):
    k = R.choice(["Fq", "r", "B", "Fi", "fem", "trafo"])
    if k == "Fq":
        q, v, B = R.choice([(1.6e-19, 1e6, 0.5), (1.6e-19, 3e5, 2), (2e-6, 1000, 0.1), (3.2e-19, 2e6, 0.25)])
        return nq("Una carga de %s C entra a %s m/s perpendicular a un campo de %s T. ¿Fuerza magnética?" % (num(q), num(v), num(B)), q * v * B, [q * v / B, q * B, v * B], "N", "F = q · v · B = %s N." % num(q * v * B))
    if k == "r":
        m, v, q, B = R.choice([(9.11e-31, 1e6, 1.6e-19, 0.01), (1.67e-27, 1e6, 1.6e-19, 0.5), (1.67e-27, 3e5, 1.6e-19, 0.1)])
        r = m * v / (q * B)
        return nq("Una partícula de %s kg y %s C entra a %s m/s perpendicular a %s T. ¿Radio de su órbita?" % (num(m), num(q), num(v), num(B)), r, [q * B / (m * v), m * v * q * B, r * 1000], "m",
                  "r = m · v : (q · B) = %s m." % num(r))
    if k == "B":
        I, d = R.choice([(10, 0.05), (5, 0.02), (20, 0.1), (2, 0.01), (15, 0.03)])
        B = 2e-7 * I / d
        return nq("¿Qué campo magnético crea un hilo recto con %s A a %s m? (μ₀ = 4π · 10⁻⁷ T·m/A)" % (I, num(d)), B, [2e-7 * I / d ** 2, 4e-7 * math.pi * I, 2e-7 * I * d], "T",
                  "B = μ₀ · I : (2π · d) = %s T." % num(B))
    if k == "Fi":
        I, L, B = R.choice([(5, 0.2, 0.5), (10, 1, 0.1), (2, 0.5, 0.3), (8, 0.25, 0.4)])
        return nq("Un conductor de %s m con %s A está perpendicular a un campo de %s T. ¿Qué fuerza recibe?" % (num(L), I, num(B)), I * L * B, [I * B / L, L * B, I * L / B], "N", "F = I · L · B = %s N." % num(I * L * B))
    if k == "fem":
        N, dphi, dt = R.choice([(100, 0.02, 0.1), (200, 0.005, 0.01), (50, 0.1, 0.5), (500, 0.002, 0.02), (10, 0.3, 0.2)])
        e = N * dphi / dt
        return nq("Una bobina de %s espiras sufre un cambio de flujo de %s Wb en %s s. ¿Qué fem media se induce?" % (N, num(dphi), num(dt)), e, [dphi / dt, N * dphi * dt, N * dt / dphi], "V",
                  "ε = N · ΔΦ : Δt = %s · %s : %s = %s V (ley de Faraday)." % (N, num(dphi), num(dt), num(e)))
    N1, N2, V1 = R.choice([(1000, 50, 230), (200, 2000, 12), (500, 100, 230), (100, 1000, 220), (2000, 100, 6000)])
    return nq("Un transformador tiene %s espiras en el primario y %s en el secundario. Si entran %s V, ¿cuántos salen?" % (N1, N2, num(V1)), V1 * N2 / N1, [V1 * N1 / N2, V1, V1 * N2], "V",
              "V₂ = V₁ · N₂ : N₁ = %s V." % num(V1 * N2 / N1))


def f_ondas(R):
    k = R.choice(["v", "snell", "lente", "aum", "I", "doppler"])
    if k == "v":
        f, lam = R.choice([(500, 0.68), (1e8, 3), (440, 0.773), (2, 1.5), (1e14, 3e-6)])
        return nq("Una onda tiene %s Hz y %s m de longitud de onda. ¿Velocidad de propagación?" % (num(f), num(lam)), f * lam, [f / lam, lam / f, f * lam * 2], "m/s", "v = λ · f = %s m/s." % num(f * lam))
    if k == "snell":
        n2, ang = R.choice([(1.33, 30), (1.5, 45), (1.33, 60), (1.5, 30), (2.42, 45)])
        r = math.degrees(math.asin(math.sin(math.radians(ang)) / n2))
        return nq("Un rayo pasa del aire (n = 1) a un medio de n = %s con un ángulo de incidencia de %s°. ¿Ángulo de refracción?" % (num(n2), ang), r, [ang / n2, ang * n2, 90 - r], "°",
                  "sen r = sen %s° : %s → r = %s°." % (ang, num(n2), num(r)))
    if k == "lente":
        f_, s = R.choice([(0.1, -0.3), (0.2, -0.5), (0.05, -0.1), (0.15, -0.6), (0.25, -1)])
        si = 1 / (1 / f_ + 1 / s)
        return nq("Una lente convergente de %s m de distancia focal tiene un objeto a %s m delante (s = %s m). ¿Dónde se forma la imagen (s′)?" % (num(f_), num(-s), num(s)), si, [1 / (1 / f_ - 1 / s), f_ + s, -si], "m",
                  "1/s′ − 1/s = 1/f → s′ = %s m (imagen real)." % num(si), neg=True)
    if k == "aum":
        P = R.choice([2, 5, 10, 4, -2, -4])
        return nq("¿Qué distancia focal tiene una lente de %s dioptrías?" % num(P), 1 / P, [P, 1 / P * 100, -1 / P], "m", "f = 1 : P = 1 : %s = %s m." % (num(P), num(1 / P)), neg=True)
    if k == "I":
        I0 = R.choice([1e-6, 1e-4, 1e-8, 1e-2, 1e-5])
        b = 10 * math.log10(I0 / 1e-12)
        return nq("¿Qué nivel de intensidad sonora corresponde a %s W/m²? (I₀ = 10⁻¹² W/m²)" % num(I0), b, [math.log10(I0 / 1e-12), b * 10, b / 2], "dB",
                  "β = 10 · log(I : I₀) = %s dB." % num(b))
    f0, v = R.choice([(500, 20), (1000, 30), (400, 34), (800, 10)])
    f = f0 * 340 / (340 - v)
    return nq("Una ambulancia que emite %s Hz se acerca a %s m/s a un observador quieto. ¿Qué frecuencia oye? (sonido: 340 m/s)" % (f0, v), f, [f0 * (340 - v) / 340, f0, f0 * (340 + v) / 340], "Hz",
              "f′ = f · v : (v − vₑ) = %s · 340 : %s = %s Hz (efecto Doppler)." % (f0, 340 - v, num(f)))


def f_mod(R):
    k = R.choice(["Efot", "fe", "broglie", "desint", "Emc", "dil"])
    if k == "Efot":
        lam = R.choice([500e-9, 400e-9, 700e-9, 300e-9, 600e-9])
        E = H_ * C_ / lam
        return nq("¿Qué energía tiene un fotón de %s m de longitud de onda? (h = 6,63 · 10⁻³⁴ J·s, c = 3 · 10⁸ m/s)" % num(lam), E, [H_ * lam / C_, H_ / lam, E * 1e3], "J", "E = h · c : λ = %s J." % num(E))
    if k == "fe":
        f, W = R.choice([(1e15, 4e-19), (1.5e15, 6e-19), (8e14, 3e-19), (2e15, 7e-19)])
        Ec = H_ * f - W
        if Ec <= 0:
            return None
        return nq("Una luz de %s Hz incide sobre un metal de trabajo de extracción %s J. ¿Energía cinética máxima de los electrones? (h = 6,63 · 10⁻³⁴ J·s)" % (num(f), num(W)), Ec,
                  [H_ * f, H_ * f + W, W], "J", "Ec = h · f − W = %s J (efecto fotoeléctrico)." % num(Ec))
    if k == "broglie":
        m, v = R.choice([(9.11e-31, 1e6), (9.11e-31, 3e6), (1.67e-27, 1e5), (0.145, 40), (9.11e-31, 5e5)])
        lam = H_ / (m * v)
        return nq("¿Qué longitud de onda de De Broglie tiene una partícula de %s kg a %s m/s? (h = 6,63 · 10⁻³⁴ J·s)" % (num(m), num(v)), lam, [m * v / H_, H_ * m * v, H_ / m], "m", "λ = h : (m · v) = %s m." % num(lam))
    if k == "desint":
        T, t = R.choice([(5730, 11460), (8, 24), (30, 90), (1600, 4800), (12, 36), (5730, 17190)])
        frac = 0.5 ** (t / T) * 100
        return nq("Un isótopo tiene un periodo de semidesintegración de %s años. ¿Qué porcentaje queda tras %s años?" % (num(T), num(t)), frac, [100 * T / t, 100 - frac, frac * 2], "%",
                  "Han pasado %s semividas: queda (1/2)^%s · 100 = %s %%." % (num(t / T), num(t / T), num(frac)))
    if k == "Emc":
        m = R.choice([0.001, 1e-6, 2e-3, 1e-9, 0.5e-3])
        return nq("¿Qué energía equivale a una masa de %s kg? (c = 3 · 10⁸ m/s)" % num(m), m * C_ ** 2, [m * C_, m * C_ ** 2 / 2, m * 9e8], "J", "E = m · c² = %s J." % num(m * C_ ** 2))
    v = R.choice([0.6, 0.8, 0.5, 0.9, 0.99])
    g = 1 / math.sqrt(1 - v * v)
    return nq("Una nave viaja a %s c. Para un observador en la Tierra, ¿cuánto dura 1 h del reloj de la nave?" % num(v), g, [1 / g, v, 1 + v], "h", "γ = 1 : √(1 − %s²) = %s; Δt = γ · 1 h = %s h." % (num(v), num(g), num(g)))


def f_cin(R):
    k = R.choice(["v", "orden", "arr", "t12"])
    if k == "v":
        kk, c, n = R.choice([(0.02, 0.5, 1), (0.1, 0.2, 2), (5, 0.1, 2), (0.003, 2, 1), (0.5, 0.4, 2), (0.04, 0.3, 1), (2, 0.05, 2), (0.15, 0.6, 1), (1.2, 0.25, 2)])
        v = kk * c ** n
        return nq("Una reacción de orden %s respecto a A tiene k = %s. ¿Qué velocidad tiene con [A] = %s mol/L?" % (n, num(kk), num(c)), v, [kk * c, kk / c, kk * c * n if n > 1 else kk * c * c], "mol/(L·s)",
                  "v = k · [A]^%s = %s mol/(L·s)." % (n, num(v)))
    if k == "orden":
        f = R.choice([2, 3, 4, 5])
        o = R.choice([1, 2])
        return nq("Al multiplicar por %s la concentración de A, la velocidad se multiplica por %s. ¿Cuál es el orden respecto a A?" % (f, f ** o), o, [f, f ** o, o + 1], "",
                  "%s^n = %s → n = %s." % (f, f ** o, o))
    if k == "arr":
        T1, T2 = R.choice([(300, 310), (290, 300), (280, 300), (300, 320)])
        return it("Una regla práctica dice que la velocidad se duplica cada 10 °C. Si pasas de %s K a %s K, ¿por cuánto se multiplica aproximadamente?" % (T1, T2),
                  "por %s" % num(2 ** ((T2 - T1) / 10)), ["por %s" % num(x) for x in sorted({(T2 - T1) / 10 + 1, 2 * (T2 - T1) / 10 + 3, 1.5}) if num(x) != num(2 ** ((T2 - T1) / 10))][:3],
                  "%s °C de aumento: 2^%s = %s." % (T2 - T1, num((T2 - T1) / 10), num(2 ** ((T2 - T1) / 10))))
    kk = R.choice([0.0693, 0.01, 0.231, 0.00693, 0.0347, 0.0231, 0.1155, 0.005])
    return nq("Una reacción de primer orden tiene k = %s s⁻¹. ¿Cuál es su periodo de semirreacción?" % num(kk), math.log(2) / kk, [1 / kk, kk * math.log(2), 2 / kk], "s",
              "t½ = ln 2 : k = 0,693 : %s = %s s." % (num(kk), num(math.log(2) / kk)))


def f_eq(R):
    k = R.choice(["Kc", "Kc", "Q", "Kp"])
    if k == "Kc":
        a, b, c = R.choice([(0.5, 0.5, 1), (0.2, 0.4, 0.8), (0.1, 0.1, 0.4), (1, 0.5, 2), (0.3, 0.2, 0.6), (0.4, 0.4, 0.6), (0.25, 0.5, 0.9), (0.6, 0.3, 1.2)])
        K = c ** 2 / (a * b)
        return nq("Para H₂ + I₂ ⇌ 2 HI, en el equilibrio [H₂] = %s, [I₂] = %s y [HI] = %s mol/L. ¿Cuánto vale Kc?" % (num(a), num(b), num(c)), K, [c / (a * b), a * b / c ** 2, 2 * c / (a + b)], "",
                  "Kc = [HI]² : ([H₂] · [I₂]) = %s." % num(K))
    if k == "Q":
        Kc, Q = R.choice([(4, 2), (4, 8), (50, 10), (10, 30), (0.5, 0.1), (100, 20), (2, 6), (8, 1), (0.2, 0.9)])
        ans = "hacia los productos" if Q < Kc else "hacia los reactivos"
        return it("Una reacción tiene Kc = %s y en un momento Q = %s. ¿Hacia dónde evoluciona?" % (num(Kc), num(Q)), ans, ["hacia los reactivos" if Q < Kc else "hacia los productos", "no evoluciona", "se detiene para siempre"],
                  "Si Q %s Kc, el sistema avanza %s." % ("&lt;" if Q < Kc else "&gt;", ans))
    Kc, dn, T = R.choice([(4, 0, 500), (0.5, -2, 500), (2, 1, 400), (10, -1, 300), (25, -1, 400), (0.2, 1, 300), (6, 2, 350)])
    Kp = Kc * (0.082 * T) ** dn
    return nq("Un equilibrio tiene Kc = %s a %s K y Δn(gas) = %s. ¿Cuánto vale Kp? (R = 0,082)" % (num(Kc), T, dn), Kp, [Kc, Kc * 0.082 * T, Kc / (0.082 * T) if dn != -1 else Kc * 0.082], "",
              "Kp = Kc · (R · T)^Δn = %s." % num(Kp))


def f_ph(R):
    k = R.choice(["fuerte", "fuerte", "base", "poh", "debil", "neutr"])
    if k == "fuerte":
        c = R.choice([0.1, 0.01, 0.001, 0.05, 0.02, 0.005, 0.2, 0.0001])
        return nq("¿Qué pH tiene una disolución de HCl %s M?" % num(c), -math.log10(c), [math.log10(c) + 14, -math.log10(c) * 2, 14 + math.log10(c)], "", "pH = −log %s = %s." % (num(c), num(-math.log10(c))))
    if k == "base":
        c = R.choice([0.1, 0.01, 0.001, 0.05])
        return nq("¿Qué pH tiene una disolución de NaOH %s M?" % num(c), 14 + math.log10(c), [-math.log10(c), 7 + math.log10(c), 14 - math.log10(c) / 2], "",
                  "pOH = −log %s = %s; pH = 14 − pOH = %s." % (num(c), num(-math.log10(c)), num(14 + math.log10(c))))
    if k == "poh":
        p = R.choice([3, 4.5, 9, 11, 2, 12.5, 5.2, 8.6])
        return nq("Una disolución tiene pH %s. ¿Cuál es su pOH?" % num(p), 14 - p, [p, 7 - p if p < 7 else p - 7, 14 + p], "", "pOH = 14 − pH = %s." % num(14 - p), neg=True)
    if k == "debil":
        c, Ka = R.choice([(0.1, 1.8e-5), (0.01, 1.8e-5), (0.1, 6.3e-5), (0.5, 1.8e-5)])
        x = math.sqrt(Ka * c)
        return nq("¿Qué pH tiene un ácido débil %s M con Ka = %s? (aproxima [H₃O⁺] = √(Ka · c))" % (num(c), num(Ka)), -math.log10(x), [-math.log10(c), -math.log10(Ka), -math.log10(Ka * c)], "",
                  "[H₃O⁺] = √(%s · %s) = %s M; pH = %s." % (num(Ka), num(c), num(x), num(-math.log10(x))))
    ca, Va, cb = R.choice([(0.1, 0.025, 0.1), (0.2, 0.02, 0.1), (0.1, 0.05, 0.25), (0.5, 0.01, 0.2)])
    return nq("¿Qué volumen de NaOH %s M neutraliza %s L de HCl %s M?" % (num(cb), num(Va), num(ca)), ca * Va / cb, [cb * Va / ca, ca * Va, Va], "L", "ca · Va = cb · Vb → Vb = %s L." % num(ca * Va / cb))


def f_redox(R):
    k = R.choice(["pila", "pila", "far", "far", "faradt"])
    if k == "pila":
        c, a, Ec, Ea = R.choice([("Cu²⁺/Cu", "Zn²⁺/Zn", 0.34, -0.76), ("Ag⁺/Ag", "Cu²⁺/Cu", 0.80, 0.34), ("Cu²⁺/Cu", "Fe²⁺/Fe", 0.34, -0.44), ("Ag⁺/Ag", "Zn²⁺/Zn", 0.80, -0.76), ("Cu²⁺/Cu", "Mg²⁺/Mg", 0.34, -2.37), ("Ag⁺/Ag", "Fe²⁺/Fe", 0.80, -0.44), ("Ag⁺/Ag", "Mg²⁺/Mg", 0.80, -2.37), ("Cu²⁺/Cu", "Al³⁺/Al", 0.34, -1.66), ("Ag⁺/Ag", "Pb²⁺/Pb", 0.80, -0.13)])
        return nq("Calcula la fem de una pila con cátodo %s (E° = %s V) y ánodo %s (E° = %s V)." % (c, num(Ec, 2), a, num(Ea, 2)), Ec - Ea, [Ec + Ea, Ea - Ec, abs(Ec) + abs(Ea) + 0.5], "V",
                  "E° = E°(cátodo) − E°(ánodo) = %s − (%s) = %s V." % (num(Ec, 2), num(Ea, 2), num(Ec - Ea)), neg=True)
    if k == "far":
        I, t, M, z, nm = R.choice([(2, 3600, 63.5, 2, "cobre"), (5, 1930, 107.9, 1, "plata"), (1, 9650, 27, 3, "aluminio"), (3, 3000, 65.4, 2, "cinc"), (10, 965, 63.5, 2, "cobre"), (4, 2412.5, 107.9, 1, "plata"), (6, 1800, 27, 3, "aluminio"), (2.5, 7720, 58.7, 2, "níquel")])
        m = I * t * M / (z * 96500)
        return nq("Se electroliza una sal de %s (M = %s g/mol, carga %s+) con %s A durante %s s. ¿Qué masa se deposita? (F = 96 500 C/mol)" % (nm, num(M), z, I, num(t)), m, [I * t * M / 96500, I * t / 96500, m * z * z], "g",
                  "m = I · t · M : (z · F) = %s g." % num(m))
    I, m, M, z = R.choice([(2, 1.27, 63.5, 2), (5, 5.4, 108, 1), (1, 0.9, 27, 3), (3, 2.54, 63.5, 2), (4, 10.8, 108, 1), (2, 0.54, 27, 3)])
    t = m * z * 96500 / (I * M)
    return nq("¿Cuánto tiempo hay que electrolizar con %s A para depositar %s g de un metal (M = %s g/mol, carga %s+)? (F = 96 500 C/mol)" % (I, num(m), num(M), z), t, [m * 96500 / (I * M), t / 60, t * z], "s",
              "t = m · z · F : (I · M) = %s s." % num(t))


def UNITS(grade):
    return [
        H("BI", "las-biomoleculas", "Biomoléculas: del agua a los ácidos nucleicos", "Biomoléculas",
          "Los alumnos describen la estructura y función de los bioelementos, el agua, las sales minerales, los glúcidos, los lípidos, las proteínas, las enzimas y los ácidos nucleicos.",
          "bioelementos, agua, sales minerales, monosacáridos, polisacáridos, enlace O-glucosídico, ácidos grasos, triglicéridos, fosfolípidos, aminoácidos, enlace peptídico, estructura de proteínas, enzimas, nucleótidos, ADN, ARN",
          "Glúcidos, lípidos, proteínas y ácidos nucleicos", "Las enzimas son proteínas que catalizan reacciones con gran especificidad.",
          ["El agua es el disolvente de la vida gracias a su polaridad y sus puentes de hidrógeno. Las sales minerales regulan el pH y la presión osmótica.",
           "Los glúcidos se unen por enlaces O-glucosídicos (almidón, glucógeno, celulosa). Los lípidos incluyen triglicéridos (reserva), fosfolípidos (membranas) y esteroides.",
           "Las proteínas son cadenas de aminoácidos unidos por enlaces peptídicos, con estructuras primaria a cuaternaria. Los ácidos nucleicos son polímeros de nucleótidos."],
          [("¿Qué polisacárido almacena glucosa en el hígado?", ["En las plantas es el almidón.", "En los animales es otro, muy ramificado."], "El glucógeno.")],
          [("La celulosa es una proteína.", "Es un polisacárido estructural de las plantas."), ("Las enzimas se gastan al actuar.", "Se recuperan intactas al final de la reacción.")],
          [("¿Qué es la desnaturalización?", "La pérdida de la estructura de una proteína por calor o pH, que le hace perder su función."), ("¿Por qué el aceite no se mezcla con el agua?", "Los lípidos son apolares e hidrófobos.")],
          [("Biomoléculas", [("glucosa", "monosacárido"), ("fructosa", "monosacárido"), ("sacarosa", "disacárido"), ("lactosa", "disacárido"), ("almidón", "polisacárido"), ("celulosa", "polisacárido"),
                             ("triglicérido", "lípido"), ("colesterol", "lípido"), ("hemoglobina", "proteína"), ("colágeno", "proteína"), ("ADN", "ácido nucleico"), ("ARN mensajero", "ácido nucleico")],
            "¿Qué tipo de biomolécula es: {k}?", None),
           ("Enlaces", [("glúcidos", "enlace O-glucosídico"), ("proteínas", "enlace peptídico"), ("ácidos nucleicos", "enlace fosfodiéster"), ("triglicéridos", "enlace éster"),
                        ("doble hélice del ADN", "puentes de hidrógeno entre bases"), ("estructura terciaria de proteínas", "puentes disulfuro y otras interacciones")],
            "¿Qué enlace une: {k}?", "¿En qué moléculas o estructuras actúa: {v}?", ["enlace metálico"]),
           ("Funciones", [("glucógeno", "reserva de energía en animales"), ("almidón", "reserva de energía en plantas"), ("celulosa", "pared de las células vegetales"), ("fosfolípidos", "forman las membranas"),
                          ("hemoglobina", "transporta oxígeno"), ("anticuerpos", "defensa del organismo"), ("enzimas", "catalizan reacciones"), ("ATP", "moneda energética de la célula")],
            "¿Qué función tiene: {k}?", D)],
          ["La glucosa es un monosacárido.", "Las proteínas se unen por enlaces peptídicos.", "El glucógeno es reserva animal.", "Los fosfolípidos forman membranas.", "Las enzimas no se gastan.",
           "La celulosa es un polisacárido.", "El ADN se une por enlaces fosfodiéster."],
          [("La celulosa es una proteína.", "Es un polisacárido."), ("Las enzimas se consumen.", "Se recuperan."), ("El almidón es reserva animal.", "Es vegetal."), ("Los aminoácidos se unen por enlace glucosídico.", "Por enlace peptídico."),
           ("Los lípidos son muy solubles en agua.", "Son hidrófobos.")],
          "las biomoléculas", "living-things-and-ecosystems"),

        H("BI", "la-celula-eucariota", "La célula eucariota: estructura y orgánulos", "Célula eucariota",
          "Los alumnos describen la membrana plasmática y los mecanismos de transporte, los orgánulos (retículo, Golgi, lisosomas, mitocondrias, cloroplastos), el citoesqueleto, el núcleo y el ciclo celular.",
          "membrana plasmática, modelo de mosaico fluido, transporte pasivo y activo, endocitosis, retículo endoplasmático, aparato de Golgi, lisosomas, mitocondrias, cloroplastos, citoesqueleto, núcleo, ciclo celular",
          "La membrana es un mosaico fluido", "Mitocondrias y cloroplastos tienen ADN propio: teoría endosimbiótica.",
          ["La membrana plasmática es una bicapa de fosfolípidos con proteínas (modelo de mosaico fluido). El transporte puede ser pasivo (sin energía) o activo (con ATP).",
           "El retículo rugoso sintetiza proteínas; el liso, lípidos; el aparato de Golgi las modifica y empaqueta; los lisosomas digieren.",
           "Mitocondrias y cloroplastos tienen ADN y ribosomas propios: según la teoría endosimbiótica descienden de bacterias."],
          [("La bomba de sodio-potasio gasta ATP. ¿Qué tipo de transporte es?", ["Va contra gradiente.", "Necesita energía."], "Transporte activo.")],
          [("La difusión necesita ATP.", "Es transporte pasivo, a favor de gradiente."), ("Las células vegetales no tienen mitocondrias.", "Tienen mitocondrias y cloroplastos.")],
          [("¿Qué es la ósmosis?", "El paso de agua a través de una membrana semipermeable hacia la zona más concentrada."), ("¿Quién propuso la teoría endosimbiótica?", "Lynn Margulis.")],
          [("Orgánulos", [("retículo endoplasmático rugoso", "síntesis de proteínas"), ("retículo endoplasmático liso", "síntesis de lípidos y detoxificación"), ("aparato de Golgi", "modifica y empaqueta sustancias"),
                          ("lisosomas", "digestión intracelular"), ("mitocondrias", "respiración celular"), ("cloroplastos", "fotosíntesis"), ("peroxisomas", "eliminación de peróxido de hidrógeno"), ("ribosomas", "traducción del ARN")],
            "¿Qué función tienen: {k}?", D),
           ("Transporte", [("difusión simple", "pasivo sin proteínas"), ("difusión facilitada", "pasivo con proteínas transportadoras"), ("ósmosis", "pasivo de agua"), ("bomba de sodio-potasio", "activo con ATP"),
                           ("fagocitosis", "endocitosis de partículas grandes"), ("pinocitosis", "endocitosis de líquidos"), ("exocitosis", "salida de sustancias en vesículas")],
            "¿Qué tipo de transporte es: {k}?", None),
           ("Endosimbiosis", {"las pruebas de la teoría endosimbiótica": ["ADN circular propio", "ribosomas como los bacterianos", "doble membrana", "se dividen por bipartición", "tamaño parecido a una bacteria"],
                              "las funciones del núcleo": ["contener el ADN", "dirigir la síntesis de proteínas", "formar los ribosomas en el nucléolo", "controlar la división celular", "guardar la información hereditaria"]})],
          ["La membrana sigue el modelo de mosaico fluido.", "La bomba de sodio-potasio es transporte activo.", "El Golgi empaqueta sustancias.", "Las mitocondrias tienen ADN propio.", "Los lisosomas digieren.",
           "La ósmosis es paso de agua.", "Lynn Margulis propuso la endosimbiosis."],
          [("La difusión gasta ATP.", "Es pasiva."), ("Los lisosomas hacen la fotosíntesis.", "Digieren."), ("Las mitocondrias no tienen ADN.", "Tienen ADN propio."), ("El retículo liso sintetiza proteínas.", "Sintetiza lípidos."),
           ("Las plantas no tienen mitocondrias.", "Sí tienen.")],
          "la célula eucariota", "living-things-and-ecosystems"),

        H("BI", "el-metabolismo-celular", "El metabolismo: catabolismo y anabolismo", "Metabolismo",
          "Los alumnos describen las rutas metabólicas, el papel del ATP y las enzimas, la glucólisis, el ciclo de Krebs, la cadena respiratoria, las fermentaciones, la fotosíntesis y la quimiosíntesis.",
          "metabolismo, catabolismo, anabolismo, ATP, coenzimas, glucólisis, ciclo de Krebs, cadena respiratoria, fosforilación oxidativa, fermentación láctica y alcohólica, fotosíntesis, ciclo de Calvin, quimiosíntesis",
          "El catabolismo libera energía; el anabolismo la consume", "La respiración aerobia produce mucho más ATP que la fermentación.",
          ["El catabolismo degrada moléculas y libera energía, que se guarda en ATP. El anabolismo usa esa energía para construir moléculas.",
           "La glucólisis (citoplasma) rompe la glucosa en piruvato. En las mitocondrias, el ciclo de Krebs y la cadena respiratoria producen la mayor parte del ATP.",
           "Sin oxígeno, el piruvato fermenta: en el músculo da ácido láctico; en las levaduras, etanol y CO₂."],
          [("¿Dónde ocurre el ciclo de Krebs?", ["Es parte de la respiración aerobia.", "Ocurre en un orgánulo con doble membrana."], "En la matriz mitocondrial.")],
          [("La fermentación produce mucho ATP.", "Solo 2 ATP por glucosa, frente a unos 30 de la respiración aerobia."), ("Las plantas no hacen catabolismo.", "Respiran como todas las células eucariotas.")],
          [("¿Por qué nos duelen los músculos tras un esfuerzo intenso?", "Influye la acumulación de ácido láctico por falta de oxígeno."), ("¿Qué es la quimiosíntesis?", "Obtener energía oxidando sustancias inorgánicas, como hacen algunas bacterias.")],
          [("Rutas", [("glucólisis", "citoplasma"), ("fermentación láctica", "citoplasma"), ("fermentación alcohólica", "citoplasma"), ("ciclo de Krebs", "matriz mitocondrial"), ("beta-oxidación de ácidos grasos", "matriz mitocondrial"),
                      ("cadena respiratoria", "membrana mitocondrial interna"), ("fase luminosa de la fotosíntesis", "tilacoides del cloroplasto"), ("ciclo de Calvin", "estroma del cloroplasto")],
            "¿Dónde ocurre: {k}?", None),
           ("Productos", [("glucólisis", "piruvato, ATP y NADH"), ("fermentación láctica", "ácido láctico"), ("fermentación alcohólica", "etanol y dióxido de carbono"), ("ciclo de Krebs", "dióxido de carbono, NADH y FADH₂"),
                          ("cadena respiratoria", "ATP y agua"), ("fase luminosa", "oxígeno, ATP y NADPH"), ("ciclo de Calvin", "glucosa y otros azúcares")],
            "¿Qué produce: {k}?", "¿Qué ruta produce {v}?"),
           ("Catabolismo o anabolismo", {"los procesos catabólicos": ["glucólisis", "ciclo de Krebs", "fermentación", "beta-oxidación", "digestión de proteínas"],
                                         "los procesos anabólicos": ["fotosíntesis", "ciclo de Calvin", "síntesis de proteínas", "replicación del ADN", "síntesis de glucógeno"]})],
          ["El catabolismo libera energía.", "La glucólisis ocurre en el citoplasma.", "El ciclo de Krebs ocurre en la matriz mitocondrial.", "La fermentación alcohólica produce etanol.", "El ATP es la moneda energética.",
           "La fotosíntesis es anabólica.", "La respiración aerobia produce más ATP que la fermentación."],
          [("La fermentación produce más ATP.", "Produce mucho menos."), ("La glucólisis ocurre en la mitocondria.", "En el citoplasma."), ("El anabolismo libera energía.", "La consume."),
           ("El ciclo de Calvin ocurre en los tilacoides.", "En el estroma."), ("La fermentación láctica produce etanol.", "Produce ácido láctico.")],
          "el metabolismo", "living-things-and-ecosystems"),

        H("BI", "genetica-molecular", "Genética molecular: replicación, expresión y mutaciones", "Genética molecular",
          "Los alumnos describen la replicación semiconservativa, la transcripción, la traducción y el código genético, la regulación génica, las mutaciones y su relación con la evolución y el cáncer.",
          "ADN, replicación semiconservativa, ADN polimerasa, fragmentos de Okazaki, transcripción, ARN polimerasa, maduración, intrones y exones, código genético, codón, anticodón, traducción, mutaciones",
          "Replicación, transcripción y traducción", "El código genético es universal y degenerado.",
          ["La replicación del ADN es semiconservativa: cada molécula hija tiene una cadena antigua y una nueva. La ADN polimerasa sintetiza en sentido 5′→3′.",
           "En la transcripción la ARN polimerasa copia un gen en ARN; en eucariotas se eliminan los intrones. En la traducción, los ribosomas leen codones de tres bases.",
           "El código genético es universal (casi igual en todos los seres vivos) y degenerado (varios codones para un aminoácido). Las mutaciones pueden ser génicas, cromosómicas o genómicas."],
          [("¿Cuántos nucleótidos codifican una proteína de 100 aminoácidos (sin el codón de parada)?", ["Cada codón tiene 3 bases.", "100 · 3 = 300."], "300 nucleótidos.")],
          [("Cada aminoácido tiene un único codón.", "El código es degenerado: la mayoría tienen varios."), ("Las mutaciones siempre se heredan.", "Solo se heredan si ocurren en los gametos.")],
          [("¿Qué es el codón AUG?", "El codón de inicio, que codifica metionina."), ("¿Qué es el síndrome de Down?", "Una mutación genómica: trisomía del cromosoma 21.")],
          [("Procesos", [("replicación", "copia del ADN antes de la división"), ("transcripción", "síntesis de ARN a partir de ADN"), ("maduración del ARN", "eliminación de intrones"), ("traducción", "síntesis de proteínas en los ribosomas"),
                         ("transcripción inversa", "síntesis de ADN a partir de ARN en retrovirus"), ("splicing alternativo", "un gen da varias proteínas según los exones que se unen")],
            "¿Qué es: {k}?", D),
           ("Moléculas", [("ADN polimerasa", "sintetiza ADN nuevo"), ("ARN polimerasa", "sintetiza ARN"), ("helicasa", "abre la doble hélice"), ("ligasa", "une fragmentos de ADN"), ("ARN de transferencia", "lleva aminoácidos al ribosoma"),
                          ("ARN mensajero", "lleva la información del gen al ribosoma"), ("ARN ribosómico", "forma parte de los ribosomas"), ("primasa", "sintetiza el cebador de ARN")],
            "¿Qué hace: {k}?", D),
           ("Mutaciones", [("cambio de una base por otra", "mutación génica puntual"), ("pérdida de un fragmento de cromosoma", "mutación cromosómica por deleción"), ("trisomía del cromosoma 21", "mutación genómica"),
                           ("inversión de un fragmento cromosómico", "mutación cromosómica"), ("inserción de una base que cambia la lectura", "mutación génica de desplazamiento de lectura"), ("célula con 3n cromosomas", "mutación genómica por poliploidía")],
            "¿Qué tipo de mutación es: {k}?", None)],
          ["La replicación es semiconservativa.", "El código genético es universal.", "Un codón tiene tres bases.", "AUG es el codón de inicio.", "Los intrones se eliminan en la maduración.", "El síndrome de Down es una trisomía.",
           "La ADN polimerasa sintetiza en sentido 5′→3′."],
          [("La replicación es conservativa.", "Es semiconservativa."), ("Un codón tiene dos bases.", "Tiene tres."), ("Cada aminoácido tiene un solo codón.", "El código es degenerado."), ("Todas las mutaciones se heredan.", "Solo las de los gametos."),
           ("Los exones se eliminan.", "Se eliminan los intrones.")],
          "la genética molecular", "living-things-and-ecosystems"),

        H("BI", "microbiologia-y-biotecnologia", "Microbiología y biotecnología", "Biotecnología",
          "Los alumnos describen los microorganismos y su papel en los ciclos, la industria y la salud, y las técnicas de ingeniería genética (ADN recombinante, PCR, CRISPR) con sus aplicaciones e implicaciones éticas.",
          "bacterias, virus, hongos, protozoos, fermentaciones industriales, biorremediación, ADN recombinante, enzimas de restricción, plásmidos, vectores, PCR, secuenciación, CRISPR-Cas9, transgénicos, clonación, bioética",
          "Las enzimas de restricción cortan el ADN", "La PCR copia millones de veces un fragmento de ADN.",
          ["La biotecnología usa seres vivos para obtener productos: pan, queso, antibióticos, vacunas o biocombustibles.",
           "En la ingeniería genética, las enzimas de restricción cortan el ADN y la ligasa lo une; los plásmidos sirven de vector para introducir genes en bacterias.",
           "La PCR amplifica ADN con ciclos de temperatura y una polimerasa resistente al calor. CRISPR-Cas9 permite editar genes con precisión."],
          [("¿Cómo se fabrica la insulina humana?", ["Se corta el gen humano y un plásmido con la misma enzima.", "Se introduce en bacterias, que la producen."], "Con bacterias transgénicas con ADN recombinante.")],
          [("La PCR fabrica proteínas.", "Copia fragmentos de ADN."), ("Los transgénicos y la mejora tradicional son lo mismo.", "Los transgénicos reciben genes de otra especie en el laboratorio.")],
          [("¿Qué aportó Francis Mojica?", "Este investigador de Alicante describió las secuencias CRISPR en arqueas."), ("¿Qué es una célula madre?", "Una célula capaz de dividirse y diferenciarse en otros tipos.")],
          [("Herramientas", [("enzimas de restricción", "cortan el ADN en secuencias concretas"), ("ADN ligasa", "une fragmentos de ADN"), ("plásmido", "ADN circular usado como vector"), ("PCR", "amplificación de ADN"),
                             ("electroforesis", "separación de fragmentos de ADN por tamaño"), ("CRISPR-Cas9", "edición precisa de genes"), ("Taq polimerasa", "polimerasa resistente al calor de la PCR")],
            "¿Qué es o para qué sirve: {k}?", D),
           ("Aplicaciones", [("insulina recombinante", "medicina"), ("vacuna de la hepatitis B", "medicina"), ("terapia génica", "medicina"), ("maíz Bt resistente a insectos", "agricultura"),
                             ("arroz dorado", "agricultura"), ("pruebas de ADN en un juicio", "ciencia forense"), ("bacterias que limpian vertidos", "medio ambiente"), ("biogás de residuos", "energía")],
            "¿En qué campo se aplica: {k}?", None, ["astrofísica"]),
           ("Microorganismos útiles", [("Saccharomyces cerevisiae", "pan, vino y cerveza"), ("Lactobacillus", "yogur y quesos"), ("Penicillium", "antibióticos"), ("Aspergillus niger", "ácido cítrico"),
                                       ("Escherichia coli", "proteínas recombinantes"), ("Rhizobium", "fijación de nitrógeno"), ("Bacillus thuringiensis", "insecticida biológico")],
            "¿Para qué se usa: {k}?", "¿Qué microorganismo se usa para obtener {v}?")],
          ["La PCR amplifica ADN.", "Las enzimas de restricción cortan el ADN.", "Los plásmidos son vectores.", "CRISPR edita genes.", "La insulina se fabrica con bacterias transgénicas.", "La electroforesis separa fragmentos de ADN.",
           "Francis Mojica describió las secuencias CRISPR."],
          [("La PCR fabrica proteínas.", "Amplifica ADN."), ("La ligasa corta el ADN.", "Lo une."), ("Los plásmidos son proteínas.", "Son ADN circular."), ("CRISPR es un antibiótico.", "Es una herramienta de edición."),
           ("La insulina se obtiene solo de cerdos.", "Hoy se fabrica con bacterias.")],
          "la biotecnología", "living-things-and-ecosystems"),

        H("BI", "inmunologia", "El sistema inmunitario", "Inmunología",
          "Los alumnos describen las defensas innatas y adaptativas, los linfocitos B y T, los anticuerpos, la respuesta primaria y secundaria, las vacunas y sueros, y las alteraciones del sistema inmunitario.",
          "inmunidad innata y adquirida, barreras, fagocitos, inflamación, antígeno, anticuerpo, linfocitos B y T, células de memoria, respuesta primaria y secundaria, vacunas, sueros, alergias, autoinmunidad, VIH, trasplantes",
          "Inmunidad innata y adaptativa", "La memoria inmunitaria hace que la segunda respuesta sea más rápida e intensa.",
          ["La inmunidad innata actúa siempre igual: barreras, fagocitos, inflamación y fiebre. La adaptativa es específica y tiene memoria.",
           "Los linfocitos B producen anticuerpos (inmunidad humoral); los T citotóxicos destruyen células infectadas y los T colaboradores coordinan la respuesta.",
           "Una vacuna genera inmunidad activa artificial con memoria; un suero da inmunidad pasiva inmediata pero temporal. El VIH destruye los linfocitos T colaboradores."],
          [("¿Por qué no solemos pasar el sarampión dos veces?", ["Tras la primera infección quedan células de memoria.", "La segunda respuesta es rápida e intensa."], "Por la memoria inmunitaria.")],
          [("Los anticuerpos destruyen directamente los virus dentro de las células.", "Se unen a los antígenos fuera de las células; las infectadas las destruyen los linfocitos T."), ("Las alergias son infecciones.", "Son respuestas exageradas frente a sustancias inofensivas.")],
          [("¿Qué es una enfermedad autoinmune?", "El sistema inmunitario ataca al propio cuerpo, como en la diabetes tipo 1."), ("¿Por qué hay rechazo en los trasplantes?", "El receptor reconoce como extrañas las moléculas del donante.")],
          [("Células y moléculas", [("linfocitos B", "producen anticuerpos"), ("linfocitos T citotóxicos", "destruyen células infectadas"), ("linfocitos T colaboradores", "coordinan la respuesta inmunitaria"),
                                    ("macrófagos", "fagocitan y presentan antígenos"), ("células plasmáticas", "linfocitos B que secretan anticuerpos"), ("células de memoria", "permiten una respuesta rápida ante el mismo antígeno"),
                                    ("anticuerpos", "proteínas que se unen específicamente a un antígeno"), ("antígeno", "molécula que desencadena la respuesta inmunitaria")],
            "¿Qué hacen o qué son: {k}?", D),
           ("Tipos de inmunidad", [("pasar la varicela", "activa natural"), ("vacunarse", "activa artificial"), ("anticuerpos de la leche materna", "pasiva natural"), ("anticuerpos que pasan por la placenta", "pasiva natural"),
                                   ("suero antiofídico", "pasiva artificial"), ("inyección de gammaglobulina", "pasiva artificial")],
            "¿Qué tipo de inmunidad se adquiere con: {k}?", None, ["innata"]),
           ("Alteraciones", {"las inmunodeficiencias": ["sida", "inmunodeficiencia combinada grave", "déficit de anticuerpos"], "las enfermedades autoinmunes": ["diabetes tipo 1", "lupus", "esclerosis múltiple", "artritis reumatoide"],
                             "las hipersensibilidades": ["alergia al polen", "asma alérgica", "alergia a los ácaros", "shock anafiláctico"]})],
          ["Los linfocitos B producen anticuerpos.", "La vacuna da inmunidad activa.", "El suero da inmunidad pasiva.", "El VIH ataca a los linfocitos T colaboradores.", "La segunda respuesta es más rápida.",
           "La diabetes tipo 1 es autoinmune.", "Los macrófagos fagocitan."],
          [("Los linfocitos T producen anticuerpos.", "Los producen los B."), ("El suero da memoria duradera.", "Es temporal."), ("La vacuna da inmunidad pasiva.", "Es activa."), ("Las alergias son infecciones.", "Son respuestas exageradas."),
           ("El VIH ataca a los glóbulos rojos.", "Ataca a los linfocitos T colaboradores.")],
          "el sistema inmunitario", "living-things-and-ecosystems"),

        H("Q", "modelo-cuantico-y-propiedades-periodicas", "Estructura atómica: modelo cuántico y propiedades periódicas", "Modelo cuántico",
          "Los alumnos aplican los números cuánticos, el principio de exclusión de Pauli y la regla de Hund a las configuraciones electrónicas, y justifican la variación de las propiedades periódicas.",
          "espectros atómicos, modelo de Bohr, hipótesis de De Broglie, principio de incertidumbre, números cuánticos, orbitales, principio de Pauli, regla de Hund, configuración electrónica, radio, energía de ionización, afinidad, electronegatividad",
          "Cuatro números cuánticos: n, l, m y s", "En un átomo no puede haber dos electrones con los cuatro números cuánticos iguales.",
          ["Los números cuánticos son n (nivel), l (tipo de orbital: s = 0, p = 1, d = 2, f = 3), m (orientación) y s (espín, ±½).",
           "Principio de Pauli: un orbital tiene como máximo dos electrones con espines opuestos. Regla de Hund: los electrones ocupan orbitales iguales por separado antes de aparearse.",
           "La energía de ionización y la electronegatividad aumentan hacia arriba y a la derecha; el radio atómico, hacia abajo y a la izquierda."],
          [("¿Cuántos electrones caben en el nivel n = 3?", ["Máximo 2n².", "2 · 3² = 18."], "18 electrones.")],
          [("Un orbital es una órbita fija.", "Es una zona de alta probabilidad de encontrar el electrón."), ("Los iones positivos son más grandes que el átomo neutro.", "Los cationes son más pequeños.")],
          [("¿Qué dice el principio de incertidumbre de Heisenberg?", "Que no se puede conocer a la vez con precisión la posición y la velocidad de un electrón."), ("¿Por qué los espectros atómicos son de líneas?", "Porque los electrones solo pasan entre niveles de energía definidos.")],
          [("Números cuánticos", [("n", "nivel de energía y tamaño del orbital"), ("l", "forma del orbital"), ("m", "orientación del orbital"), ("s", "espín del electrón")],
            "¿Qué indica el número cuántico {k}?", "¿Qué número cuántico indica {v}?", ["la carga del núcleo", "la masa del átomo"]),
           ("Capacidad", [("orbital s", "2 electrones"), ("subnivel p", "6 electrones"), ("subnivel d", "10 electrones"), ("subnivel f", "14 electrones"), ("nivel n = 2", "8 electrones"), ("nivel n = 3", "18 electrones"),
                          ("nivel n = 4", "32 electrones")],
            "¿Cuántos electrones caben como máximo en el {k}?", None),
           ("Principios", [("principio de exclusión de Pauli", "no hay dos electrones con los cuatro números cuánticos iguales"), ("regla de Hund", "los electrones ocupan orbitales degenerados por separado"),
                           ("principio de Aufbau", "los orbitales se llenan en orden de energía creciente"), ("principio de incertidumbre", "no se conocen a la vez posición y momento con precisión"),
                           ("hipótesis de De Broglie", "toda partícula tiene asociada una onda"), ("modelo de Bohr", "el electrón gira en órbitas de energía cuantizada")],
            "¿Qué establece: {k}?", D)],
          ["Un orbital admite dos electrones como máximo.", "El nivel n = 3 admite 18 electrones.", "El subnivel d admite 10 electrones.", "Los cationes son más pequeños que su átomo.", "La electronegatividad aumenta hacia la derecha.",
           "l indica la forma del orbital.", "Los espectros atómicos son de líneas."],
          [("Un orbital es una órbita fija.", "Es una zona de probabilidad."), ("Un orbital admite cuatro electrones.", "Admite dos."), ("Los cationes son más grandes.", "Son más pequeños."), ("El subnivel p admite 10 electrones.", "Admite 6."),
           ("s indica el nivel.", "Indica el espín.")],
          "la estructura atómica", "matter"),

        H("Q", "enlace-quimico-y-geometria-molecular", "Enlace químico, geometría y fuerzas intermoleculares", "Enlace y geometría",
          "Los alumnos describen el enlace iónico (energía de red), el covalente (Lewis, TRPECV, hibridación, polaridad), el metálico y las fuerzas intermoleculares, y relacionan estructura y propiedades.",
          "energía de red, ciclo de Born-Haber, estructura de Lewis, TRPECV, geometría molecular, hibridación sp, sp², sp³, polaridad, enlace metálico, fuerzas de Van der Waals, enlace de hidrógeno",
          "Los pares de electrones se alejan lo máximo posible", "Una molécula con enlaces polares puede ser apolar si es simétrica, como el CO₂.",
          ["La TRPECV predice la geometría: los pares de electrones del átomo central se repelen. CH₄ es tetraédrica, NH₃ piramidal, H₂O angular, CO₂ lineal y BF₃ trigonal plana.",
           "La hibridación explica los enlaces: sp³ en el metano, sp² en el eteno, sp en el etino.",
           "Las fuerzas intermoleculares (dispersión, dipolo-dipolo, enlace de hidrógeno) determinan los puntos de fusión y ebullición de las sustancias moleculares."],
          [("¿Por qué el CO₂ es apolar aunque sus enlaces C=O son polares?", ["La molécula es lineal.", "Los dipolos se anulan."], "Porque es simétrica.")],
          [("El agua es lineal.", "Es angular por sus dos pares no enlazantes."), ("Los enlaces de hidrógeno son más fuertes que los covalentes.", "Son mucho más débiles; solo son fuertes entre fuerzas intermoleculares.")],
          [("¿Por qué el hielo flota?", "Los enlaces de hidrógeno forman una red abierta menos densa que el agua líquida."), ("¿Qué es la energía de red?", "La energía que se libera al formar un cristal iónico a partir de sus iones gaseosos.")],
          [("Geometrías", [("CH₄", "tetraédrica"), ("NH₃", "piramidal trigonal"), ("H₂O", "angular"), ("CO₂", "lineal"), ("BF₃", "trigonal plana"), ("BeCl₂", "lineal"), ("CCl₄", "tetraédrica"), ("SO₂", "angular")],
            "¿Qué geometría tiene {k}?", None, ["octaédrica"]),
           ("Hibridación", [("carbono del metano", "sp³"), ("carbono del eteno", "sp²"), ("carbono del etino", "sp"), ("carbono del CO₂", "sp"), ("carbono del benceno", "sp²"), ("carbono del diamante", "sp³"),
                            ("carbono del grafito", "sp²")],
            "¿Qué hibridación tiene el {k}?", None, ["sp³d²"]),
           ("Polaridad", {"las moléculas polares": ["H₂O", "NH₃", "HCl", "SO₂", "CH₃Cl"], "las moléculas apolares": ["CO₂", "CH₄", "BF₃", "N₂", "CCl₄"]})],
          ["El metano es tetraédrico.", "El agua es angular.", "El CO₂ es apolar.", "El carbono del eteno es sp².", "El enlace de hidrógeno es una fuerza intermolecular.", "El amoniaco es polar.", "El hielo es menos denso que el agua."],
          [("El agua es lineal.", "Es angular."), ("El CO₂ es polar.", "Es apolar."), ("El carbono del etino es sp³.", "Es sp."), ("Los enlaces de hidrógeno son más fuertes que los covalentes.", "Son más débiles."),
           ("El metano es plano.", "Es tetraédrico.")],
          "el enlace químico", "matter"),

        H("Q", "cinetica-quimica", "Cinética química: velocidad de reacción", "Cinética química",
          "Los alumnos expresan la velocidad de reacción y la ecuación de velocidad, determinan órdenes de reacción, aplican la teoría de colisiones y del estado de transición, y explican los factores y los catalizadores.",
          "velocidad de reacción, ecuación de velocidad, constante de velocidad, orden de reacción, teoría de colisiones, estado de transición, energía de activación, ecuación de Arrhenius, catalizadores, enzimas",
          "v = k · [A]^m · [B]^n", "Un catalizador reduce la energía de activación sin cambiar ΔH.",
          ["La velocidad de reacción es la variación de concentración por unidad de tiempo. La ecuación de velocidad es v = k · [A]^m · [B]^n; los órdenes se determinan experimentalmente.",
           "Según la teoría de colisiones, reaccionan los choques con energía suficiente (energía de activación) y orientación adecuada.",
           "La velocidad aumenta con la temperatura (ecuación de Arrhenius), la concentración, la superficie de contacto y los catalizadores."],
          [("Si duplicar [A] cuadruplica la velocidad, ¿orden respecto a A?", ["2ⁿ = 4.", "n = 2."], "Orden 2.")],
          [("Los órdenes coinciden siempre con los coeficientes.", "Se determinan experimentalmente."), ("El catalizador cambia el equilibrio.", "Solo hace que se alcance antes.")],
          [("¿Por qué los alimentos duran más en el congelador?", "La baja temperatura reduce mucho la velocidad de las reacciones."), ("¿Qué son los catalizadores de los coches?", "Dispositivos con platino y rodio que transforman CO y NOx en gases menos dañinos.")],
          [("Factores", [("aumentar la temperatura", "más choques eficaces"), ("aumentar la concentración", "más choques por segundo"), ("triturar un sólido", "más superficie de contacto"), ("añadir un catalizador", "menor energía de activación"),
                         ("añadir un inhibidor", "mayor energía de activación o bloqueo"), ("enfriar", "menos choques eficaces")],
            "¿Qué efecto tiene: {k}?", D),
           ("Conceptos", [("energía de activación", "energía mínima para que un choque sea eficaz"), ("complejo activado", "especie inestable del estado de transición"), ("orden total", "suma de los órdenes parciales"),
                          ("constante de velocidad", "depende de la temperatura según Arrhenius"), ("molecularidad", "número de partículas que chocan en una etapa elemental"), ("etapa limitante", "etapa más lenta de un mecanismo")],
            "¿Qué es: {k}?", D),
           ("Catálisis", {"los ejemplos de catálisis homogénea": ["catalizador disuelto en la misma fase", "descomposición de H₂O₂ con yoduro", "ácido sulfúrico en la esterificación"],
                          "los ejemplos de catálisis heterogénea": ["catalizador de platino del coche", "hierro en el proceso Haber", "níquel en la hidrogenación de aceites"],
                          "los ejemplos de catálisis enzimática": ["amilasa de la saliva", "catalasa del hígado", "lactasa del intestino", "pepsina del estómago"]})],
          ["El catalizador reduce la energía de activación.", "Los órdenes se determinan experimentalmente.", "La temperatura aumenta la velocidad.", "Triturar aumenta la superficie de contacto.", "La etapa más lenta limita la velocidad.",
           "Las enzimas son catalizadores biológicos.", "El catalizador no cambia ΔH."],
          [("El catalizador cambia ΔH.", "No la cambia."), ("Los órdenes son siempre los coeficientes.", "Se miden experimentalmente."), ("Enfriar acelera la reacción.", "La frena."), ("El catalizador se consume.", "Se recupera."),
           ("El inhibidor reduce la energía de activación.", "La aumenta o bloquea.")],
          "la cinética química", "matter", calc=f_cin),

        H("Q", "equilibrio-quimico", "El equilibrio químico", "Equilibrio químico",
          "Los alumnos describen el equilibrio dinámico, calculan Kc y Kp, usan el cociente de reacción, aplican el principio de Le Châtelier y estudian los equilibrios de solubilidad.",
          "equilibrio dinámico, ley de acción de masas, constante Kc y Kp, cociente de reacción Q, grado de disociación, principio de Le Châtelier, equilibrios heterogéneos, solubilidad, producto de solubilidad",
          "Kc = [productos]^coef : [reactivos]^coef", "Si se altera un equilibrio, el sistema evoluciona para contrarrestar el cambio.",
          ["En el equilibrio las velocidades directa e inversa son iguales y las concentraciones no cambian. Kc relaciona esas concentraciones.",
           "Si Q < K la reacción avanza hacia los productos; si Q > K, hacia los reactivos. Kp = Kc · (R · T)^Δn.",
           "Principio de Le Châtelier: al añadir un reactivo, subir la presión o cambiar la temperatura, el equilibrio se desplaza para contrarrestarlo."],
          [("En N₂ + 3 H₂ ⇌ 2 NH₃ (exotérmica), ¿qué pasa si se aumenta la presión?", ["Hay 4 moles de gas a la izquierda y 2 a la derecha.", "El sistema reduce la presión yendo a menos moles."], "Se desplaza hacia el NH₃.")],
          [("En el equilibrio la reacción se detiene.", "Las dos reacciones siguen ocurriendo a la misma velocidad."), ("Un catalizador desplaza el equilibrio.", "Solo acelera que se alcance.")],
          [("¿Qué cambia el valor de K?", "Solo la temperatura."), ("¿Qué es el producto de solubilidad?", "La constante de equilibrio de un sólido poco soluble con sus iones en disolución.")],
          [("Le Châtelier", [("añadir reactivo", "se desplaza hacia los productos"), ("retirar producto", "se desplaza hacia los productos"), ("añadir producto", "se desplaza hacia los reactivos"),
                             ("aumentar la presión", "se desplaza hacia menos moles de gas"), ("disminuir la presión", "se desplaza hacia más moles de gas"), ("calentar una reacción exotérmica", "se desplaza hacia los reactivos"),
                             ("calentar una reacción endotérmica", "se desplaza hacia los productos"), ("añadir un catalizador", "no se desplaza")],
            "¿Qué ocurre con el equilibrio al {k}?", None),
           ("Conceptos", [("equilibrio dinámico", "las velocidades directa e inversa son iguales"), ("cociente de reacción", "expresión de K con concentraciones no de equilibrio"), ("grado de disociación", "fracción de moles que se disocian"),
                          ("equilibrio heterogéneo", "equilibrio con sustancias en distintas fases"), ("producto de solubilidad", "constante de equilibrio de una sal poco soluble"), ("efecto ion común", "disminución de la solubilidad al añadir un ion presente")],
            "¿Qué es: {k}?", D),
           ("Expresiones", [("H₂ + I₂ ⇌ 2 HI", "Kc = [HI]² : ([H₂] · [I₂])"), ("N₂ + 3 H₂ ⇌ 2 NH₃", "Kc = [NH₃]² : ([N₂] · [H₂]³)"), ("2 SO₂ + O₂ ⇌ 2 SO₃", "Kc = [SO₃]² : ([SO₂]² · [O₂])"),
                            ("N₂O₄ ⇌ 2 NO₂", "Kc = [NO₂]² : [N₂O₄]"), ("CaCO₃(s) ⇌ CaO(s) + CO₂(g)", "Kc = [CO₂]"), ("AgCl(s) ⇌ Ag⁺ + Cl⁻", "Ks = [Ag⁺] · [Cl⁻]")],
            "¿Cuál es la constante de equilibrio de {k}?", "¿A qué equilibrio corresponde {v}?")],
          ["En el equilibrio las velocidades son iguales.", "Solo la temperatura cambia K.", "Si Q < K avanza hacia productos.", "Un catalizador no desplaza el equilibrio.", "Los sólidos no aparecen en Kc.",
           "Aumentar la presión desplaza hacia menos moles de gas.", "El efecto ion común reduce la solubilidad."],
          [("En el equilibrio la reacción se detiene.", "Sigue en ambos sentidos."), ("El catalizador desplaza el equilibrio.", "No lo desplaza."), ("La presión cambia K.", "Solo la temperatura."),
           ("Si Q > K avanza hacia productos.", "Hacia reactivos."), ("Los sólidos aparecen en Kc.", "No aparecen.")],
          "el equilibrio químico", "matter", calc=f_eq),

        H("Q", "acidos-y-bases", "Reacciones ácido-base y pH", "Ácidos y bases",
          "Los alumnos aplican las teorías de Arrhenius y Brønsted-Lowry, distinguen ácidos y bases fuertes y débiles, calculan el pH, estudian la hidrólisis de sales, las disoluciones reguladoras y las valoraciones.",
          "Arrhenius, Brønsted-Lowry, pares conjugados, Kw, pH, pOH, ácidos y bases fuertes y débiles, Ka, Kb, hidrólisis, disolución reguladora, indicadores, valoración, punto de equivalencia, lluvia ácida",
          "pH = −log [H₃O⁺]", "A 25 °C, pH + pOH = 14.",
          ["Según Brønsted-Lowry, un ácido cede protones y una base los acepta. Cada ácido tiene su base conjugada.",
           "El pH es −log [H₃O⁺]. Un ácido fuerte se disocia totalmente; uno débil, poco (Ka pequeña).",
           "Una disolución reguladora (ácido débil y su sal) resiste cambios de pH. En una valoración se usa un indicador para detectar el punto de equivalencia."],
          [("¿Qué pH tiene HCl 0,01 M?", ["Ácido fuerte: [H₃O⁺] = 0,01.", "−log 0,01 = 2."], "pH = 2.")],
          [("Un ácido débil es un ácido diluido.", "Débil significa que se disocia poco; diluido, que hay poca concentración."), ("La sal de una neutralización siempre es neutra.", "Puede ser ácida o básica por hidrólisis.")],
          [("¿Qué pH tiene la sangre?", "Alrededor de 7,4, regulado por el sistema bicarbonato."), ("¿Por qué el acetato de sodio es básico?", "El ion acetato se hidroliza y forma OH⁻.")],
          [("Pares conjugados", [("HCl", "Cl⁻"), ("H₂O como ácido", "OH⁻"), ("NH₄⁺", "NH₃"), ("CH₃COOH", "CH₃COO⁻"), ("H₂CO₃", "HCO₃⁻"), ("H₃O⁺", "H₂O"), ("HNO₃", "NO₃⁻")],
            "¿Cuál es la base conjugada de {k}?", "¿Cuál es el ácido conjugado de {v}?"),
           ("Fuertes y débiles", [("HCl", "ácido fuerte"), ("HNO₃", "ácido fuerte"), ("H₂SO₄", "ácido fuerte"), ("CH₃COOH", "ácido débil"), ("HF", "ácido débil"), ("H₂CO₃", "ácido débil"),
                                  ("NaOH", "base fuerte"), ("KOH", "base fuerte"), ("NH₃", "base débil")],
            "¿Cómo se clasifica {k}?", None),
           ("Hidrólisis", {"las sales de disolución neutra": ["NaCl", "KNO₃", "KCl", "NaNO₃"], "las sales de disolución ácida": ["NH₄Cl", "NH₄NO₃", "(NH₄)₂SO₄"],
                           "las sales de disolución básica": ["CH₃COONa", "Na₂CO₃", "NaHCO₃", "KCN"]})],
          ["pH + pOH = 14 a 25 °C.", "Un ácido de Brønsted cede protones.", "El HCl es un ácido fuerte.", "El NH₄Cl da disolución ácida.", "Una disolución reguladora resiste cambios de pH.", "El pH de la sangre es de unos 7,4.",
           "El amoniaco es una base débil."],
          [("Débil significa diluido.", "Significa poco disociado."), ("Toda sal es neutra.", "Puede hidrolizarse."), ("El HCl es débil.", "Es fuerte."), ("pH + pOH = 7.", "Suman 14."), ("Un ácido acepta protones.", "Los cede.")],
          "los ácidos y las bases", "matter", calc=f_ph),

        H("Q", "reacciones-redox-y-electroquimica", "Reacciones redox y electroquímica", "Redox y electroquímica",
          "Los alumnos identifican oxidantes y reductores, ajustan reacciones redox por el método del ion-electrón, calculan la fem de pilas con potenciales estándar y aplican las leyes de Faraday a la electrólisis.",
          "oxidación, reducción, número de oxidación, oxidante, reductor, método del ion-electrón, pila galvánica, ánodo, cátodo, puente salino, potencial estándar, fem, electrólisis, leyes de Faraday, corrosión",
          "Oxidación: pérdida de electrones. Reducción: ganancia", "En una pila el cátodo es donde ocurre la reducción.",
          ["Oxidarse es perder electrones (aumenta el número de oxidación); reducirse es ganarlos. El oxidante se reduce y el reductor se oxida.",
           "En una pila galvánica, la oxidación ocurre en el ánodo y la reducción en el cátodo. La fem es E° = E°(cátodo) − E°(ánodo).",
           "En la electrólisis la corriente provoca una reacción no espontánea. Leyes de Faraday: m = I · t · M : (z · F), con F = 96 500 C/mol."],
          [("En la pila Daniell (Zn | Zn²⁺ ‖ Cu²⁺ | Cu), ¿qué electrodo es el ánodo?", ["El Zn tiene un potencial más negativo.", "Se oxida."], "El cinc.")],
          [("El oxidante se oxida.", "El oxidante se reduce y oxida a otro."), ("En la electrólisis el ánodo es negativo.", "En la electrólisis el ánodo es positivo; en la pila, negativo.")],
          [("¿Cómo se protege el hierro de la corrosión?", "Pintándolo, galvanizándolo con cinc o con un ánodo de sacrificio."), ("¿Qué es la galvanoplastia?", "Recubrir un objeto con un metal por electrólisis.")],
          [("Números de oxidación", [("O en el H₂O", "−2"), ("H en el H₂O", "+1"), ("S en el H₂SO₄", "+6"), ("Mn en el KMnO₄", "+7"), ("Cr en el K₂Cr₂O₇", "+6"), ("Fe en el Fe₂O₃", "+3"),
                                     ("N en el NH₃", "−3"), ("N en el HNO₃", "+5"), ("Cl en el Cl₂", "0")],
            "¿Qué número de oxidación tiene el {k}?", None, ["+4", "−1"]),
           ("Conceptos", [("oxidación", "pérdida de electrones"), ("reducción", "ganancia de electrones"), ("oxidante", "especie que se reduce"), ("reductor", "especie que se oxida"), ("ánodo", "electrodo donde ocurre la oxidación"),
                          ("cátodo", "electrodo donde ocurre la reducción"), ("puente salino", "cierra el circuito y mantiene la neutralidad"), ("faraday", "carga de un mol de electrones")],
            "¿Qué es: {k}?", D),
           ("Aplicaciones", {"las aplicaciones de las pilas": ["batería de litio del móvil", "pila alcalina", "pila de combustible de hidrógeno", "batería del coche eléctrico"],
                             "las aplicaciones de la electrólisis": ["obtención de aluminio", "cromado de piezas", "obtención de cloro y sosa", "refinado del cobre"],
                             "la protección frente a la corrosión": ["galvanizado con cinc", "ánodo de sacrificio de magnesio", "pintura del hierro", "acero inoxidable"]})],
          ["Oxidarse es perder electrones.", "El oxidante se reduce.", "En la pila la oxidación ocurre en el ánodo.", "F vale 96 500 C/mol.", "El galvanizado protege el hierro.", "El Mn del KMnO₄ tiene +7.",
           "La electrólisis provoca reacciones no espontáneas."],
          [("Oxidarse es ganar electrones.", "Es perderlos."), ("El oxidante se oxida.", "Se reduce."), ("La reducción ocurre en el ánodo.", "Ocurre en el cátodo."), ("La electrólisis es espontánea.", "No lo es."),
           ("El oxígeno del agua tiene +2.", "Tiene −2.")],
          "las reacciones redox", "matter", calc=f_redox),

        H("FI", "campo-gravitatorio", "El campo gravitatorio", "Campo gravitatorio",
          "Los alumnos aplican la ley de gravitación universal, calculan el campo y el potencial gravitatorio, la energía potencial, las velocidades orbitales y de escape, y las leyes de Kepler.",
          "ley de gravitación universal, constante G, intensidad del campo gravitatorio, potencial gravitatorio, energía potencial, campo conservativo, leyes de Kepler, velocidad orbital, velocidad de escape, satélites geoestacionarios",
          "F = G · m₁ · m₂ : r²", "g disminuye con el cuadrado de la distancia al centro del planeta.",
          ["La ley de gravitación universal: F = G · m₁ · m₂ : r², con G = 6,67 · 10⁻¹¹ N·m²/kg².",
           "El campo gravitatorio es g = G · M : r² y el potencial, V = −G · M : r. La energía potencial es Ep = −G · M · m : r.",
           "Un satélite orbita con v = √(G · M : r). La velocidad de escape es √(2 · G · M : R). Kepler: T² es proporcional a r³."],
          [("¿Cómo cambia g si te alejas al doble de distancia del centro de la Tierra?", ["g ∝ 1 : r².", "1 : 2² = 1/4."], "Se reduce a la cuarta parte.")],
          [("En la estación espacial no hay gravedad.", "g allí es casi el 90 % del de la superficie; los astronautas están en caída libre."), ("La velocidad de escape depende de la masa del objeto.", "Solo depende del planeta.")],
          [("¿Qué es un satélite geoestacionario?", "Uno que tarda 24 h en dar la vuelta y parece quieto sobre un punto del ecuador."), ("¿Por qué la energía potencial gravitatoria es negativa?", "Porque se toma cero en el infinito y la fuerza es atractiva.")],
          [("Kepler y las órbitas", [("primera ley de Kepler", "las órbitas son elipses con el Sol en un foco"), ("segunda ley de Kepler", "el radio vector barre áreas iguales en tiempos iguales"),
                                     ("tercera ley de Kepler", "T² es proporcional al cubo del semieje mayor"), ("perihelio", "punto de la órbita más cercano al Sol"), ("afelio", "punto de la órbita más alejado del Sol"),
                                     ("velocidad en el perihelio", "la máxima de toda la órbita"), ("velocidad en el afelio", "la mínima de toda la órbita")],
            "¿Qué corresponde a: {k}?", D),
           ("Magnitudes", [("intensidad del campo", "g = G · M : r²"), ("potencial gravitatorio", "V = −G · M : r"), ("energía potencial gravitatoria", "Ep = −G · M · m : r"), ("velocidad orbital", "v = √(G · M : r)"),
                           ("velocidad de escape", "v = √(2 · G · M : R)"), ("fuerza gravitatoria", "F = G · M · m : r²")],
            "¿Qué expresión corresponde a: {k}?", "¿Qué magnitud se calcula con {v}?"),
           ("Conceptos", [("campo conservativo", "el trabajo no depende del camino"), ("línea de campo", "indica la dirección de la fuerza sobre una masa"), ("superficie equipotencial", "puntos con el mismo potencial"),
                          ("ingravidez aparente", "sensación de caída libre en órbita"), ("satélite geoestacionario", "periodo de 24 h sobre el ecuador"), ("órbita de transferencia", "órbita elíptica para pasar de una órbita a otra")],
            "¿Qué es: {k}?", D)],
          ["g disminuye con el cuadrado de la distancia.", "El campo gravitatorio es conservativo.", "Los satélites están en caída libre.", "La velocidad de escape no depende de la masa del objeto.", "Las órbitas son elipses.",
           "Un geoestacionario tarda 24 h en dar la vuelta.", "La energía potencial gravitatoria es negativa."],
          [("En la estación espacial no hay gravedad.", "Hay casi el 90 % de g."), ("La velocidad de escape depende de la masa del cohete.", "No depende."), ("g disminuye linealmente con la distancia.", "Con el cuadrado."),
           ("Las órbitas son círculos perfectos.", "Son elipses."), ("El campo gravitatorio no es conservativo.", "Sí lo es.")],
          "el campo gravitatorio", "forces-and-motion", calc=f_grav),

        H("FI", "campo-electrico", "El campo eléctrico", "Campo eléctrico",
          "Los alumnos aplican la ley de Coulomb, calculan el campo y el potencial eléctrico de cargas puntuales, el trabajo y la energía potencial, el campo entre placas y el teorema de Gauss.",
          "carga eléctrica, ley de Coulomb, constante K, campo eléctrico, líneas de campo, potencial eléctrico, diferencia de potencial, energía potencial eléctrica, superficies equipotenciales, teorema de Gauss, condensador",
          "F = K · q₁ · q₂ : r²", "El campo eléctrico apunta hacia donde se movería una carga positiva.",
          ["Ley de Coulomb: F = K · q₁ · q₂ : r², con K = 9 · 10⁹ N·m²/C². Cargas del mismo signo se repelen.",
           "El campo de una carga puntual es E = K · q : r² y el potencial, V = K · q : r. El trabajo del campo es W = −q · ΔV.",
           "Entre dos placas paralelas cargadas el campo es uniforme: ΔV = E · d. Dentro de un conductor en equilibrio el campo es nulo (jaula de Faraday)."],
          [("¿Cómo cambia la fuerza si se duplica la distancia entre dos cargas?", ["F ∝ 1 : r².", "1 : 4."], "Se reduce a la cuarta parte.")],
          [("El potencial y el campo son lo mismo.", "El campo es vectorial y el potencial escalar."), ("Dentro de un coche te puede alcanzar un rayo.", "La carrocería actúa como jaula de Faraday.")],
          [("¿Qué es un electronvoltio?", "La energía que gana un electrón al atravesar 1 V: 1,6 · 10⁻¹⁹ J."), ("¿Qué dice el teorema de Gauss?", "El flujo eléctrico a través de una superficie cerrada es proporcional a la carga encerrada.")],
          [("Conceptos", [("campo eléctrico", "fuerza por unidad de carga positiva"), ("potencial eléctrico", "energía potencial por unidad de carga"), ("línea de campo", "sale de las cargas positivas y entra en las negativas"),
                          ("superficie equipotencial", "puntos con el mismo potencial"), ("jaula de Faraday", "conductor hueco donde el campo interior es nulo"), ("electronvoltio", "unidad de energía de 1,6 · 10⁻¹⁹ J"),
                          ("condensador", "dos conductores que almacenan carga")],
            "¿Qué es: {k}?", D),
           ("Expresiones", [("fuerza entre cargas", "F = K · q₁ · q₂ : r²"), ("campo de una carga puntual", "E = K · q : r²"), ("potencial de una carga puntual", "V = K · q : r"), ("energía potencial eléctrica", "Ep = K · q₁ · q₂ : r"),
                            ("trabajo entre dos puntos", "W = −q · ΔV"), ("campo entre placas", "E = ΔV : d")],
            "¿Qué expresión corresponde a: {k}?", "¿Qué magnitud se calcula con {v}?"),
           ("Comparación", {"las características del campo gravitatorio": ["siempre atractivo", "depende de la masa", "constante G muy pequeña", "no se puede apantallar"],
                            "las características del campo eléctrico": ["atractivo o repulsivo", "depende de la carga", "constante K muy grande", "se puede apantallar con una jaula de Faraday"],
                            "las características comunes a ambos": ["son conservativos", "disminuyen con el cuadrado de la distancia", "son campos centrales", "tienen asociado un potencial"]})],
          ["Cargas iguales se repelen.", "El campo es vectorial y el potencial escalar.", "Dentro de un conductor en equilibrio el campo es nulo.", "Las líneas salen de las cargas positivas.", "El campo eléctrico es conservativo.",
           "1 eV son 1,6 · 10⁻¹⁹ J.", "La fuerza eléctrica disminuye con el cuadrado de la distancia."],
          [("Cargas iguales se atraen.", "Se repelen."), ("El potencial es un vector.", "Es un escalar."), ("El campo gravitatorio puede ser repulsivo.", "Siempre es atractivo."), ("Las líneas salen de las cargas negativas.", "Entran en ellas."),
           ("Dentro de un conductor hay campo intenso.", "Es nulo.")],
          "el campo eléctrico", "forces-and-motion", calc=f_elec),

        H("FI", "campo-magnetico-e-induccion", "Campo magnético e inducción electromagnética", "Magnetismo e inducción",
          "Los alumnos calculan la fuerza de Lorentz sobre cargas y corrientes, el campo creado por corrientes, aplican las leyes de Faraday y Lenz a la inducción y explican el generador y el transformador.",
          "campo magnético, tesla, fuerza de Lorentz, movimiento de cargas en un campo, fuerza sobre una corriente, ley de Biot-Savart, solenoide, flujo magnético, ley de Faraday, ley de Lenz, alternador, transformador",
          "F = q · v · B · sen α", "Una variación de flujo magnético induce una corriente que se opone a esa variación.",
          ["Una carga que se mueve en un campo magnético recibe la fuerza de Lorentz, F = q · v · B · sen α, perpendicular a v y a B: describe una circunferencia.",
           "Una corriente rectilínea crea un campo B = μ₀ · I : (2π · r). Dos corrientes paralelas del mismo sentido se atraen.",
           "Ley de Faraday: ε = −N · ΔΦ : Δt. Ley de Lenz: la corriente inducida se opone al cambio que la produce. Así funcionan los alternadores y transformadores."],
          [("Un transformador reduce 230 V a 11,5 V. Si el primario tiene 1000 espiras, ¿cuántas tiene el secundario?", ["V₂ : V₁ = N₂ : N₁.", "N₂ = 1000 · 11,5 : 230 = 50."], "50 espiras.")],
          [("Un campo magnético quieto induce corriente.", "Solo induce si el flujo varía."), ("La fuerza magnética cambia la rapidez de la carga.", "Solo cambia la dirección: no hace trabajo.")],
          [("¿Por qué se usa corriente alterna en la red?", "Porque los transformadores permiten elevar la tensión y transportarla con menos pérdidas."), ("¿Qué es el tesla?", "La unidad del campo magnético en el SI.")],
          [("Leyes", [("fuerza de Lorentz", "F = q · v · B · sen α"), ("fuerza sobre un conductor", "F = I · L · B · sen α"), ("campo de un hilo recto", "B = μ₀ · I : (2π · r)"), ("campo en un solenoide", "B = μ₀ · N · I : L"),
                      ("ley de Faraday", "ε = −N · ΔΦ : Δt"), ("flujo magnético", "Φ = B · S · cos α"), ("transformador", "V₁ : V₂ = N₁ : N₂")],
            "¿Qué expresión corresponde a: {k}?", "¿Qué ley o magnitud expresa {v}?"),
           ("Aplicaciones", [("alternador", "inducción electromagnética"), ("transformador", "inducción mutua"), ("motor eléctrico", "fuerza sobre una corriente en un campo"), ("espectrómetro de masas", "fuerza de Lorentz sobre iones"),
                             ("ciclotrón", "fuerza de Lorentz sobre partículas cargadas"), ("cocina de inducción", "corrientes inducidas en el recipiente"), ("frenos magnéticos de un tren", "corrientes de Foucault")],
            "¿Qué fenómeno aprovecha: {k}?", None),
           ("Conceptos", [("ley de Lenz", "la corriente inducida se opone a la variación de flujo"), ("tesla", "unidad de campo magnético"), ("weber", "unidad de flujo magnético"), ("permeabilidad", "capacidad de un medio para el campo magnético"),
                          ("corrientes de Foucault", "corrientes inducidas en masas metálicas"), ("autoinducción", "una bobina induce corriente en sí misma")],
            "¿Qué es: {k}?", D)],
          ["La fuerza magnética no cambia la rapidez de la carga.", "Un flujo variable induce corriente.", "La corriente inducida se opone al cambio de flujo.", "Dos corrientes paralelas del mismo sentido se atraen.", "El transformador funciona por inducción.",
           "El campo magnético se mide en teslas.", "Una carga en un campo uniforme perpendicular describe una circunferencia."],
          [("Un campo quieto induce corriente.", "Debe variar el flujo."), ("La fuerza magnética acelera la carga en rapidez.", "Solo cambia la dirección."), ("Corrientes paralelas del mismo sentido se repelen.", "Se atraen."),
           ("El transformador funciona con corriente continua.", "Necesita alterna."), ("El flujo se mide en teslas.", "Se mide en webers.")],
          "el campo magnético", "energy", calc=f_mag),

        H("FI", "ondas-y-optica", "Ondas, sonido y óptica", "Ondas y óptica",
          "Los alumnos describen el movimiento armónico simple, las ondas armónicas y sus fenómenos (reflexión, refracción, difracción, interferencias, efecto Doppler), el sonido y la óptica geométrica con espejos y lentes.",
          "MAS, ondas mecánicas y electromagnéticas, ecuación de onda, longitud de onda, frecuencia, intensidad, decibelios, reflexión, refracción, ley de Snell, reflexión total, difracción, interferencias, Doppler, lentes, dioptrías, ojo",
          "v = λ · f y n₁ · sen i = n₂ · sen r", "Una lente de P dioptrías tiene f = 1/P metros.",
          ["Una onda armónica cumple v = λ · f. El sonido es una onda mecánica longitudinal; la luz, una onda electromagnética transversal.",
           "Ley de Snell: n₁ · sen i = n₂ · sen r. Si la luz pasa a un medio menos denso con un ángulo mayor que el límite, hay reflexión total (fibra óptica).",
           "En las lentes delgadas, 1/s′ − 1/s = 1/f (normas DIN). La potencia es P = 1/f en dioptrías. La miopía se corrige con lentes divergentes."],
          [("Una lente tiene −2 dioptrías. ¿Qué tipo es y qué focal tiene?", ["P negativa: divergente.", "f = 1 : (−2) = −0,5 m."], "Divergente, f = −0,5 m.")],
          [("La luz se propaga más rápido en el agua que en el aire.", "Va más despacio: n = c : v > 1."), ("La difracción solo ocurre con la luz.", "Ocurre con cualquier onda; con el sonido es muy notable.")],
          [("¿Por qué el cielo es azul?", "La luz azul se dispersa más en la atmósfera."), ("¿Qué es la hipermetropía?", "Un defecto en el que la imagen se forma detrás de la retina; se corrige con lentes convergentes.")],
          [("Fenómenos", [("fibra óptica", "reflexión total"), ("espejismo en la carretera", "refracción en capas de aire"), ("oír a alguien tras una esquina", "difracción"), ("colores de una pompa de jabón", "interferencias"),
                          ("cambio de tono de una sirena que pasa", "efecto Doppler"), ("eco", "reflexión"), ("arco iris", "dispersión"), ("ondas estacionarias de una guitarra", "interferencias")],
            "¿Qué fenómeno ondulatorio explica: {k}?", None),
           ("Lentes, espejos y visión", [("lente convergente", "potencia y focal positivas"), ("lente divergente", "potencia y focal negativas"), ("espejo plano", "imagen virtual del mismo tamaño"),
                                          ("espejo cóncavo", "puede formar imágenes reales"), ("espejo convexo", "imagen virtual y menor, como en los retrovisores"), ("lupa", "lente convergente con el objeto dentro de la focal"),
                                          ("miopía", "se corrige con una lente divergente"), ("hipermetropía", "se corrige con una lente convergente"), ("astigmatismo", "se corrige con una lente cilíndrica")],
            "¿Qué corresponde a: {k}?", D),
           ("Conceptos", [("longitud de onda", "distancia entre dos puntos en fase"), ("frecuencia", "oscilaciones por segundo"), ("índice de refracción", "cociente entre la velocidad de la luz en el vacío y en el medio"),
                          ("ángulo límite", "ángulo de incidencia a partir del cual hay reflexión total"), ("dioptría", "inversa de la distancia focal en metros"), ("intensidad", "energía por unidad de superficie y tiempo"),
                          ("onda estacionaria", "superposición de ondas iguales en sentidos opuestos")],
            "¿Qué es: {k}?", D)],
          ["v = λ · f.", "La luz va más despacio en el agua.", "La fibra óptica usa reflexión total.", "La miopía se corrige con lentes divergentes.", "El sonido es una onda longitudinal.", "La difracción ocurre con cualquier onda.",
           "El efecto Doppler cambia la frecuencia percibida."],
          [("La luz va más rápido en el agua.", "Va más despacio."), ("La miopía se corrige con lentes convergentes.", "Con divergentes."), ("El sonido es transversal.", "Es longitudinal."), ("La difracción solo ocurre con la luz.", "Ocurre con cualquier onda."),
           ("La fibra óptica usa refracción simple.", "Usa reflexión total.")],
          "las ondas y la óptica", "waves-and-light", calc=f_ondas),

        H("FI", "fisica-moderna", "Física del siglo XX: relatividad, cuántica y física nuclear", "Física moderna",
          "Los alumnos describen la relatividad especial, la hipótesis de Planck, el efecto fotoeléctrico, la dualidad onda-corpúsculo, el principio de incertidumbre, la radiactividad, la fisión y la fusión nuclear.",
          "relatividad especial, dilatación del tiempo, contracción de la longitud, E = m · c², cuerpo negro, Planck, efecto fotoeléctrico, fotón, De Broglie, Heisenberg, radiactividad alfa, beta y gamma, semivida, fisión, fusión",
          "E = h · f y E = m · c²", "La luz se comporta como onda y como partícula.",
          ["Relatividad especial: la velocidad de la luz es igual para todos los observadores; el tiempo se dilata y la longitud se contrae a velocidades cercanas a c. E = m · c².",
           "Planck: la energía se emite en cuantos E = h · f. Einstein explicó el efecto fotoeléctrico con fotones: Ec = h · f − W.",
           "Los núcleos inestables emiten radiación alfa, beta o gamma. Tras un periodo de semidesintegración queda la mitad de los núcleos. La fisión divide núcleos pesados y la fusión une ligeros."],
          [("Una luz roja intensa no arranca electrones de un metal, pero una ultravioleta débil sí. ¿Por qué?", ["La energía de cada fotón depende de f.", "Los fotones UV superan el trabajo de extracción."], "Por la cuantización: E = h · f.")],
          [("Más intensidad de luz da electrones más rápidos.", "Da más electrones; su energía depende de la frecuencia."), ("La radiactividad la inventó el ser humano.", "Existe en la naturaleza; Becquerel la descubrió en 1896.")],
          [("¿Cómo produce energía el Sol?", "Por fusión de núcleos de hidrógeno en helio."), ("¿Qué es la vida media de un isótopo?", "El tiempo medio que tarda un núcleo en desintegrarse; distinta de la semivida.")],
          [("Radiaciones", [("radiación alfa", "núcleos de helio, poco penetrantes"), ("radiación beta", "electrones emitidos por el núcleo"), ("radiación gamma", "ondas electromagnéticas muy penetrantes"),
                            ("positrón", "antipartícula del electrón"), ("neutrón", "partícula sin carga que provoca la fisión del uranio")],
            "¿Qué es: {k}?", D, ["un protón libre del aire"]),
           ("Científicos", [("Planck", "cuantización de la energía"), ("Einstein", "efecto fotoeléctrico y relatividad"), ("De Broglie", "ondas asociadas a las partículas"), ("Heisenberg", "principio de incertidumbre"),
                            ("Bohr", "modelo atómico con niveles cuantizados"), ("Marie Curie", "estudio de la radiactividad, polonio y radio"), ("Rutherford", "descubrimiento del núcleo atómico")],
            "¿Qué aportó {k}?", "¿Quién propuso o estudió: {v}?"),
           ("Fisión y fusión", {"las características de la fisión": ["divide núcleos pesados", "uranio-235", "reacción en cadena", "centrales nucleares actuales", "residuos radiactivos de larga vida"],
                                "las características de la fusión": ["une núcleos ligeros", "hidrógeno en helio", "energía del Sol", "proyecto ITER", "necesita millones de grados"]})],
          ["La velocidad de la luz es igual para todos los observadores.", "E = h · f.", "La luz tiene comportamiento dual.", "Tras una semivida queda la mitad de los núcleos.", "El Sol funciona por fusión.",
           "La radiación gamma es muy penetrante.", "Marie Curie estudió la radiactividad."],
          [("Más intensidad da electrones más rápidos.", "Da más electrones."), ("El Sol funciona por fisión.", "Por fusión."), ("La radiación alfa es la más penetrante.", "Es la gamma."), ("La masa no se puede convertir en energía.", "E = m · c²."),
           ("El tiempo es igual para todos los observadores.", "Se dilata a gran velocidad.")],
          "la física moderna", "energy", calc=f_mod),

        H("GC", "riesgos-geologicos", "Los riesgos geológicos y su prevención", "Riesgos geológicos",
          "Los alumnos analizan los riesgos sísmico, volcánico, de inundación, de movimientos de ladera y costeros, sus factores (peligrosidad, exposición, vulnerabilidad), la predicción y prevención, con ejemplos de España.",
          "riesgo, peligrosidad, exposición, vulnerabilidad, terremotos, magnitud, intensidad, volcanes, tsunamis, inundaciones, DANA, movimientos de ladera, mapas de riesgo, prevención, ordenación del territorio",
          "Riesgo = peligrosidad · exposición · vulnerabilidad", "La prevención y la ordenación del territorio reducen los daños.",
          ["El riesgo combina la peligrosidad del fenómeno, la exposición (personas y bienes en la zona) y la vulnerabilidad (lo fácil que es que sufran daños).",
           "La magnitud mide la energía de un terremoto; la intensidad, sus efectos en un lugar. En España las zonas de mayor riesgo sísmico están en el sureste.",
           "Las inundaciones son el riesgo natural que más daños causa en España, sobre todo con episodios de DANA en el Mediterráneo. La erupción de La Palma de 2021 mostró el riesgo volcánico en Canarias."],
          [("¿Por qué un terremoto igual causa más víctimas en un país pobre?", ["La peligrosidad es la misma.", "Las construcciones son más vulnerables."], "Por su mayor vulnerabilidad.")],
          [("Magnitud e intensidad son lo mismo.", "La magnitud es la energía liberada; la intensidad, los efectos observados."), ("Los terremotos se predicen con exactitud.", "Hoy no se pueden predecir; sí se elaboran mapas de peligrosidad.")],
          [("¿Qué es una DANA?", "Una depresión aislada en niveles altos que puede provocar lluvias torrenciales."), ("¿Qué norma regula la construcción sismorresistente?", "La Norma de Construcción Sismorresistente española.")],
          [("Factores del riesgo", [("peligrosidad", "probabilidad de que ocurra un fenómeno de cierta intensidad"), ("exposición", "personas y bienes situados en la zona"), ("vulnerabilidad", "facilidad con que sufren daños"),
                                    ("mapa de riesgo", "representa las zonas según su nivel de riesgo"), ("predicción", "anunciar cuándo y dónde ocurrirá un fenómeno"), ("prevención", "medidas para reducir los daños")],
            "¿Qué es: {k}?", D),
           ("Medidas", [("construir edificios sismorresistentes", "riesgo sísmico"), ("no edificar en cauces y ramblas", "inundaciones"), ("encauzar ríos y construir embalses", "inundaciones"), ("vigilar la deformación del suelo y los gases", "riesgo volcánico"),
                        ("drenar y reforestar laderas", "movimientos de ladera"), ("regenerar playas y proteger dunas", "riesgo costero"), ("sistemas de alerta de tsunamis", "riesgo costero")],
            "¿Frente a qué riesgo se aplica: {k}?", None),
           ("Ejemplos de España", [("Lorca, 2011", "terremoto"), ("La Palma, 2021", "erupción volcánica"), ("Valencia, 2024", "inundación por DANA"), ("Biescas, 1996", "avenida en un cono de deyección"),
                                   ("Lisboa y Huelva, 1755", "terremoto y tsunami"), ("Granada, 1884", "terremoto de Andalucía")],
            "¿Qué fenómeno ocurrió en {k}?", None)],
          ["El riesgo depende de la peligrosidad, la exposición y la vulnerabilidad.", "La magnitud mide la energía del terremoto.", "Las inundaciones causan muchos daños en España.", "Los terremotos no se pueden predecir con exactitud.",
           "No se debe edificar en ramblas.", "En 2021 hubo una erupción en La Palma.", "El sureste peninsular tiene más riesgo sísmico."],
          [("Magnitud e intensidad son lo mismo.", "Son distintas."), ("Los terremotos se predicen con exactitud.", "No se pueden predecir."), ("En España no hay riesgo volcánico.", "Lo hay en Canarias."),
           ("Construir en ramblas reduce el riesgo.", "Lo aumenta."), ("La vulnerabilidad es la energía del fenómeno.", "Es la facilidad de sufrir daños.")],
          "los riesgos geológicos", "earths-systems"),

        H("GC", "recursos-naturales-y-sostenibilidad", "Recursos geológicos, energía y sostenibilidad", "Recursos naturales",
          "Los alumnos clasifican los recursos (minerales, energéticos, hídricos, suelo), analizan su explotación e impactos, el cambio climático, la gestión de residuos y los indicadores de sostenibilidad.",
          "recursos renovables y no renovables, reservas, yacimientos, minería, combustibles fósiles, energías renovables, agua subterránea, suelo, desertificación, cambio climático, residuos, economía circular, indicadores",
          "Un recurso no renovable se agota a escala humana", "La economía circular reduce, reutiliza y recicla para gastar menos recursos.",
          ["Los recursos pueden ser renovables (agua, suelo bien gestionado, energía solar) o no renovables (minerales, combustibles fósiles). Las reservas son la parte explotable con la tecnología actual.",
           "La minería y los combustibles fósiles generan impactos: residuos, contaminación de aguas, emisiones de CO₂ y cambio climático.",
           "En España la desertificación y la sobreexplotación de acuíferos son problemas importantes. La economía circular y las renovables ayudan a la sostenibilidad."],
          [("¿El suelo es un recurso renovable?", ["Se forma muy despacio, durante siglos.", "Se pierde rápido por erosión."], "En la práctica, no renovable a escala humana.")],
          [("Recurso y reserva son lo mismo.", "La reserva es la parte del recurso que se puede explotar hoy con beneficio."), ("La energía renovable no tiene ningún impacto.", "Tiene impactos menores, como en el paisaje o la fauna.")],
          [("¿Qué es la desertificación?", "La degradación del suelo en zonas secas por el clima y la actividad humana."), ("¿Qué son las tierras raras?", "Un grupo de elementos clave para imanes, baterías y electrónica.")],
          [("Tipos de recursos", [("petróleo", "energético no renovable"), ("carbón", "energético no renovable"), ("uranio", "energético no renovable"), ("viento", "energético renovable"), ("radiación solar", "energético renovable"),
                                  ("cobre", "mineral metálico"), ("litio", "mineral metálico"), ("yeso", "mineral no metálico"), ("arcilla", "roca industrial"), ("agua de un acuífero", "hídrico")],
            "¿Qué tipo de recurso es: {k}?", None),
           ("Impactos", [("minería a cielo abierto", "destrucción del paisaje y del suelo"), ("drenaje ácido de minas", "contaminación de ríos"), ("quema de combustibles fósiles", "emisiones de CO₂ y cambio climático"),
                         ("sobreexplotación de acuíferos", "descenso del nivel freático e intrusión salina"), ("vertederos sin control", "contaminación de suelos y aguas"), ("tala de bosques", "erosión y desertificación")],
            "¿Qué impacto produce: {k}?", "¿Qué actividad causa {v}?"),
           ("Economía circular", {"las acciones de reducir": ["comprar sin envases", "ahorrar energía", "usar transporte público", "evitar productos de un solo uso"],
                                  "las acciones de reutilizar": ["rellenar botellas", "reparar aparatos", "comprar de segunda mano", "donar ropa"],
                                  "las acciones de reciclar": ["separar el vidrio", "compostar restos orgánicos", "llevar pilas al punto limpio", "recuperar metales de los móviles"]})],
          ["El petróleo es un recurso no renovable.", "Las reservas son la parte explotable de un recurso.", "La sobreexplotación de acuíferos causa intrusión salina.", "El suelo se forma muy despacio.", "El litio es un recurso mineral.",
           "La economía circular reduce el consumo de recursos.", "La quema de combustibles fósiles contribuye al cambio climático."],
          [("Recurso y reserva son lo mismo.", "Son distintos."), ("El suelo se regenera en pocos años.", "Tarda siglos."), ("Las renovables no tienen impacto.", "Tienen impactos menores."), ("El uranio es renovable.", "No es renovable."),
           ("Reciclar es lo primero de la economía circular.", "Primero reducir y reutilizar.")],
          "los recursos naturales", "earths-systems"),
    ]
