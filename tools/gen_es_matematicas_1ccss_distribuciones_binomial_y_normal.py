# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Distribuciones binomial y normal (Sentido estocástico)
Variables aleatorias discretas, distribución binomial (P(X = k), media, «al menos uno»), distribución normal (tabla N(0, 1), tipificación, percentiles), aproximación de la binomial.
Reutiliza los generadores de Matemáticas II con otra semilla.
Errores: olvidar el número combinatorio, P(X ≥ 1) = 1 − P(X = 1), restar al revés al tipificar, buscar valores negativos en la tabla.
"""
import math
import random
from es_ccss import M, mix, unit, L, use_, kurve, BLUE

R = random.Random(53010)
DB = "gen_es_matematicas_2bach_distribuciones"
s_va, s_identificar, s_binomial, s_bin_problema, s_tabla, s_tipificar, s_inversa, s_aprox = use_(DB, 53210, "s_va", "s_identificar", "s_binomial", "s_bin_problema", "s_tabla", "s_tipificar", "s_inversa", "s_aprox")

seen = set()
sets = [("Variables aleatorias y binomial", mix(R, seen, [(s_va, 8), (s_identificar, 12)])), ("Probabilidades binomiales", mix(R, seen, [(s_binomial, 20)])),
        ("Problemas con la binomial", mix(R, seen, [(s_bin_problema, 20)])), ("Distribución normal", mix(R, seen, [(s_tabla, 8), (s_tipificar, 12)])),
        ("Percentiles y aproximación", mix(R, seen, [(s_inversa, 10), (s_aprox, 10)]))]
think = ["Una <b>variable aleatoria discreta</b> toma valores sueltos; sus probabilidades suman 1. Media: μ = Σ x · P(X = x).",
         "<b>Binomial</b> B(n, p): n pruebas independientes con dos resultados; X cuenta los éxitos. P(X = k) = C<sub>n,k</sub> · p<sup>k</sup> · q<sup>n−k</sup>; μ = np; σ = √(npq).",
         "<b>Normal</b> N(μ, σ): campana simétrica. Se <b>tipifica</b> con z = (x − μ)/σ y se usa la tabla de N(0, 1). P(Z ≤ −z) = 1 − P(Z ≤ z).",
         "Si np ≥ 5 y nq ≥ 5, la binomial se aproxima por N(np, √(npq)), con corrección por continuidad (± 0,5)."]
ex = [("El 20 % de los clientes compra; 5 clientes. P(X = 2)", ["C<sub>5,2</sub> · 0,2² · 0,8³"], "0,2048"), ("Notas N(6, 1,5). P(X ≤ 7,5)", ["z = (7,5 − 6)/1,5 = 1"], "0,8413")]
mist = [["Olvidar C<sub>n,k</sub>", "Hay varias formas de colocar los éxitos."], ["P(X ≥ 1) = 1 − P(X = 1)", "Es 1 − P(X = 0)."], ["Buscar z negativos en la tabla", "Usa la simetría: P(Z ≤ −z) = 1 − P(Z ≤ z)."]]
body = L(think, ex, mist, kurve([(lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi) * 5, BLUE, "")], (-3.5, 3.5, 1), (0, 2.5, 1), W=330, H=200, label="campana de Gauss N(0, 1)"))
faq = [("¿Cuándo se usa la binomial y cuándo la normal?", "La binomial cuenta éxitos en un número fijo de pruebas (valores enteros). La normal describe magnitudes continuas como estaturas, notas o tiempos."),
       ("¿Por qué se tipifica?", "Para usar una sola tabla, la de N(0, 1), con cualquier distribución normal.")]
unit(1, R, "distribuciones-binomial-y-normal", "S", "Variables aleatorias; distribución binomial: probabilidades, media y desviación; distribución normal: tipificación, tabla N(0, 1) y aproximación de la binomial",
     "Distribuciones binomial y normal", "Binomial y normal", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: distribución binomial, distribución normal, tipificación y aproximación. 100 ejercicios con soluciones.",
     "Tipifica: z = (x − μ) / σ", "Binomial: n pruebas, dos resultados.", body, faq, sets, 10)
