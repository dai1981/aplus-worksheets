# -*- coding: utf-8 -*-
"""Sverige gymnasiet: Matematik nivå 5（Gy25）"""
import math
from fractions import Fraction as F
from se_g import nz, xp, pol, U, ri, ch, sh, fq, d, par, sg, M, MN, rd, sup, num, MIN, coin, expr, lista, MQ
from se_g3 import P_, fl, ps, frac_html, ekx

PP = P_ + P_


def kk(k):
    return "" if k == 1 else (MIN if k == -1 else sg(k))


# ============================================================ differentialekvationer av första ordningen
def de1():
    def yky():
        k = nz(-6, 6)
        C = nz(-9, 9)
        if coin():
            return M("Vilken är den allmänna lösningen till y%s = %sy?" % (P_, kk(k)), "y = Ce<sup>%sx</sup>" % kk(k), ["y = Ce<sup>x</sup>" if k != 1 else "y = Ce<sup>2x</sup>", "y = %sx + C" % kk(k), "y = Ce<sup>%sx</sup>" % kk(-k)], "y%s = ky har lösningen y = Ce<sup>kx</sup>: <b>y = Ce<sup>%sx</sup></b>." % (P_, kk(k)))
        return M("Lös y%s = %sy med y(0) = %s." % (P_, kk(k), sg(C)), "y = %se<sup>%sx</sup>" % (kk(C), kk(k)), ["y = %se<sup>%sx</sup>" % (kk(k), kk(C)), "y = e<sup>%sx</sup> %s %d" % (kk(k), "+" if C > 0 else "−", abs(C)), "y = %se<sup>%sx</sup>" % (kk(C), kk(-k))], "y = Ce<sup>kx</sup> och y(0) = C = %s: <b>y = %se<sup>%sx</sup></b>." % (sg(C), kk(C), kk(k)))

    def inh():
        a = nz(-6, 6)
        b = nz(-12, 12)
        if (b % a):
            return None
        yp = F(b, a)
        res = "y = Ce<sup>%sx</sup> %s %s" % (kk(-a), "+" if yp > 0 else "−", d(abs(yp)))
        return M("Lös differentialekvationen y%s %s %sy = %s." % (P_, "+" if a > 0 else "−", "" if abs(a) == 1 else abs(a), sg(b)), res, ["y = Ce<sup>%sx</sup> %s %s" % (kk(a), "+" if yp > 0 else "−", d(abs(yp))), "y = Ce<sup>%sx</sup> %s %s" % (kk(-a), "+" if b > 0 else "−", d(abs(b))) if abs(b) != abs(yp) else "y = Ce<sup>%sx</sup>" % kk(-a), "y = Ce<sup>%sx</sup> %s %s" % (kk(-a), "−" if yp > 0 else "+", d(abs(yp)))],
                 "Homogen lösning Ce<sup>%sx</sup>, partikulärlösning y = %s: <b>%s</b>." % (kk(-a), sg(yp), res))

    def verify():
        k = nz(-4, 4)
        P = [("y = e<sup>%sx</sup>" % kk(k), "y%s = %sy" % (P_, kk(k)), ["y%s = %sy" % (P_, kk(-k)), "y%s = y + %s" % (P_, abs(k) + 1), "y%s = %sx" % (P_, kk(k))]),
             ("y = %s" % pol({2: k}), "y%s = %s" % (P_, frac_html("2y", "x")), ["y%s = 2y" % P_, "y%s = %s" % (P_, frac_html("y", "x")), "y%s = %sy²" % (P_, kk(k))]),
             ("y = %se<sup>x</sup> + x" % kk(k), "y%s = y − x + 1" % P_, ["y%s = y + x" % P_, "y%s = y" % P_, "y%s = y − x" % P_]),
             ("y = sin %sx" % ("" if abs(k) == 1 else abs(k)), "y%s + %sy = 0" % (PP, "" if k * k == 1 else k * k), ["y%s − %sy = 0" % (PP, "" if k * k == 1 else k * k), "y%s + y = 0" % P_ if k * k != 1 else "y%s + 2y = 0" % PP, "y%s = %sy" % (P_, "" if abs(k) == 1 else abs(k))])]
        f, r, w = ch(P)
        return M("Vilken differentialekvation har lösningen %s?" % f, r, w, "Derivera och sätt in: <b>%s</b>." % r)

    def villkor():
        a = nz(-4, 4)
        b = nz(-8, 8) * abs(a)
        y0 = ri(-9, 9)
        yp = F(b, a)
        C = y0 - yp
        if C == 0:
            return None
        res = "y = %se<sup>%sx</sup> %s %s" % (kk(C), kk(-a), "+" if yp > 0 else "−", d(abs(yp)))
        return M("Lös y%s %s %sy = %s med y(0) = %s." % (P_, "+" if a > 0 else "−", "" if abs(a) == 1 else abs(a), sg(b), sg(y0)), res, ["y = %se<sup>%sx</sup> %s %s" % (kk(y0), kk(-a), "+" if yp > 0 else "−", d(abs(yp))), "y = %se<sup>%sx</sup> %s %s" % (kk(C), kk(a), "+" if yp > 0 else "−", d(abs(yp))), "y = %se<sup>%sx</sup> %s %s" % (kk(y0 + yp) if y0 + yp else "2", kk(-a), "+" if yp > 0 else "−", d(abs(yp)))],
                 "Allmän lösning y = Ce<sup>%sx</sup> %s %s. y(0) = C %s %s = %s ger C = %s: <b>%s</b>." % (kk(-a), "+" if yp > 0 else "−", d(abs(yp)), "+" if yp > 0 else "−", d(abs(yp)), sg(y0), sg(C), res))

    def ordning():
        P = [("y%s + 3y = x" % P_, "Första ordningen"), ("y%s − 4y = 0" % PP, "Andra ordningen"), ("y%s + 2y%s + y = 0" % (PP, P_), "Andra ordningen"), ("y%s = 5y" % P_, "Första ordningen"), ("y%s%s = y" % (PP, P_), "Tredje ordningen"), ("2y%s = y + 1" % P_, "Första ordningen"), ("y%s + y = sin x" % PP, "Andra ordningen")]
        q, r = ch(P)
        k = ri(2, 9)
        return M("Vilken ordning har differentialekvationen %s? (Uppgift %d)" % (q, k), r, [x for x in ("Första ordningen", "Andra ordningen", "Tredje ordningen", "Nollte ordningen") if x != r], "Ordningen är den högsta derivatan: <b>%s</b>." % r.lower())

    sets = [("y′ = ky", [(yky, 20)]), ("y′ + ay = b", [(inh, 20)]), ("Kontrollera lösningar", [(verify, 12), (ordning, 8)]), ("Begynnelsevillkor", [(villkor, 20)]), ("Blandat", [(yky, 7), (inh, 6), (villkor, 7)])]
    return U("differentialekvationer-av-forsta-ordningen", "DE", "Differentialekvationer av första ordningen", "Differentialekvationer, ordning 1",
             "Differentialekvationer av första ordningen: y′ = ky och y′ + ay = b, begynnelsevillkor och kontroll av lösningar.",
             "Uppgifter om differentialekvationer av första ordningen för Matematik 5: y′ = ky, y′ + ay = b, kontroll av lösningar, ordning och begynnelsevillkor. 100 uppgifter med facit.",
             "y′ = ky ger y = Ce^(kx)", "Ett villkor bestämmer konstanten C.", sets,
             ["En differentialekvation innehåller en okänd funktion och dess derivator. Lösningen är en funktion, inte ett tal.",
              "y′ = ky har lösningen y = Ce<sup>kx</sup>. y′ + ay = b har lösningen y = Ce<sup>−ax</sup> + b/a.",
              "Ett begynnelsevillkor som y(0) = 5 bestämmer konstanten C. Kontrollera en lösning genom att derivera och sätta in."],
             [("y′ + 2y = 6, y(0) = 1", ["y = Ce<sup>−2x</sup> + 3", "1 = C + 3"], "y = −2e<sup>−2x</sup> + 3")],
             [["Svarar med ett tal", "Lösningen är en funktion"], ["y′ + ay = b ger Ce<sup>ax</sup>", "Exponenten är −a"], ["Glömmer partikulärlösningen", "Lägg till b/a"]],
             [("Vad är en partikulärlösning?", "En lösning som uppfyller ekvationen, ofta en konstant."), ("Varför finns ett C?", "Det finns oändligt många lösningar. Ett villkor väljer en av dem."), ("Var används differentialekvationer?", "I modeller för tillväxt, avsvalning och rörelse.")])


# ============================================================ andra ordningen
def de2():
    def reella():
        r1, r2 = nz(-6, 6), nz(-6, 6)
        if r1 == r2:
            return None
        r1, r2 = sorted([r1, r2])
        a, b = -(r1 + r2), r1 * r2
        res = "y = Ae<sup>%sx</sup> + Be<sup>%sx</sup>" % (kk(r1), kk(r2))
        return M("Lös y%s%s%s = 0." % (PP, ("" if a == 0 else " %s %sy%s" % ("+" if a > 0 else "−", "" if abs(a) == 1 else abs(a), P_)), " %s %sy" % ("+" if b > 0 else "−", "" if abs(b) == 1 else abs(b))), res, ["y = Ae<sup>%sx</sup> + Be<sup>%sx</sup>" % (kk(-r1), kk(-r2)), "y = (A + Bx)e<sup>%sx</sup>" % kk(r1), "y = A cos %sx + B sin %sx" % (abs(r1), abs(r1))],
                 "Karakteristisk ekvation r² %s = 0 ger r = %s och r = %s: <b>%s</b>." % (ps({1: a, 0: b}, "r") if a else sg(b), sg(r1), sg(r2), res))

    def dubbel():
        r = nz(-6, 6)
        a, b = -2 * r, r * r
        res = "y = (A + Bx)e<sup>%sx</sup>" % kk(r)
        m = ri(1, 3)
        return M("Lös %sy%s %s %sy%s + %sy = 0." % ("" if m == 1 else m, PP, "+" if a > 0 else "−", abs(a * m), P_, "" if b * m == 1 else b * m), res, ["y = Ae<sup>%sx</sup> + Be<sup>%sx</sup>" % (kk(r), kk(-r)), "y = (A + Bx)e<sup>%sx</sup>" % kk(-r), "y = Ae<sup>%sx</sup>" % kk(r)], "Dubbelrot r = %s: <b>%s</b>." % (sg(r), res))

    def komplex():
        a = ri(0, 3)
        w = ri(1, 6)
        if a == 0:
            res = "y = A cos %sx + B sin %sx" % ("" if w == 1 else w, "" if w == 1 else w)
            return M("Lös y%s + %sy = 0." % (PP, "" if w * w == 1 else w * w), res, ["y = Ae<sup>%dx</sup> + Be<sup>%sx</sup>" % (w, kk(-w)), "y = A cos %sx + B sin %sx" % (w * w, w * w), "y = (A + Bx)e<sup>%dx</sup>" % w], "r² + %d = 0 ger r = ±%s%s: <b>%s</b>." % (w * w, "" if w == 1 else w, "<i>i</i>", res))
        s = ch([1, -1]) * a
        p = -2 * s
        q = s * s + w * w
        ww = "" if w == 1 else w
        res = "y = e<sup>%sx</sup>(A cos %sx + B sin %sx)" % (kk(s), ww, ww)
        return M("Lös y%s %s %sy%s + %sy = 0." % (PP, "+" if p > 0 else "−", abs(p), P_, q), res, ["y = e<sup>%sx</sup>(A cos %sx + B sin %sx)" % (kk(-s), ww, ww), "y = e<sup>%sx</sup>(A cos %sx + B sin %sx)" % (kk(w), abs(s), abs(s)), "y = Ae<sup>%sx</sup> + Be<sup>%sx</sup>" % (kk(s), kk(w))],
                 "r = %s ± %s<i>i</i>: <b>%s</b>." % (sg(s), ww, res))

    def kar():
        a, b = ri(-9, 9), nz(-20, 20)
        r = "r² %s = 0" % ps({1: a, 0: b}, "r") if a else "r² %s %d = 0" % ("+" if b > 0 else "−", abs(b))
        r = r.replace("r² r", "r² + r").replace("r² −", "r² −")
        txt = "r²" + ("" if a == 0 else " %s %sr" % ("+" if a > 0 else "−", "" if abs(a) == 1 else abs(a))) + " %s %d = 0" % ("+" if b > 0 else "−", abs(b))
        q = "y%s%s %s %sy = 0" % (PP, "" if a == 0 else " %s %sy%s" % ("+" if a > 0 else "−", "" if abs(a) == 1 else abs(a), P_), "+" if b > 0 else "−", "" if abs(b) == 1 else abs(b))
        w1 = "r²" + ("" if a == 0 else " %s %sr" % ("−" if a > 0 else "+", "" if abs(a) == 1 else abs(a))) + " %s %d = 0" % ("+" if b > 0 else "−", abs(b))
        w2 = "r" + ("" if a == 0 else " %s %d" % ("+" if a > 0 else "−", abs(a))) + " %s %d = 0" % ("+" if b > 0 else "−", abs(b))
        w3 = "r²" + ("" if a == 0 else " %s %sr" % ("+" if a > 0 else "−", "" if abs(a) == 1 else abs(a))) + " %s %d = 0" % ("−" if b > 0 else "+", abs(b))
        return M("Vilken är den karakteristiska ekvationen till %s?" % q, txt, [w1 if a else "r² = 0", w2, w3], "Byt y%s mot r², y%s mot r och y mot 1: <b>%s</b>." % (PP, P_, txt))

    def villk():
        r1, r2 = 0, nz(-5, 5)
        A, B = ri(-6, 6), nz(-6, 6)
        # y = A + B e^{r2 x}; y(0) = A + B, y'(0) = B r2
        y0, y1 = A + B, B * r2
        res = "y = %s%se<sup>%sx</sup>" % ("" if A == 0 else sg(A) + (" + " if B > 0 else " − "), ("" if abs(B) == 1 else abs(B)) if A != 0 else kk(B), kk(r2))
        return M("Lös y%s %s %sy%s = 0 med y(0) = %s och y%s(0) = %s." % (PP, "−" if r2 > 0 else "+", "" if abs(r2) == 1 else abs(r2), P_, sg(y0), P_, sg(y1)), res,
                 ["y = %s%se<sup>%sx</sup>" % ("" if B == 0 else sg(B) + (" + " if A > 0 else " − "), ("" if abs(A) == 1 else abs(A)) if B != 0 else kk(A), kk(r2)) if A else "y = %s + %se<sup>%sx</sup>" % (sg(B), "", kk(r2)), "y = %s%se<sup>%sx</sup>" % ("" if A == 0 else sg(A) + (" + " if B > 0 else " − "), ("" if abs(B) == 1 else abs(B)) if A != 0 else kk(B), kk(-r2)), "y = %se<sup>%sx</sup>" % (kk(y0), kk(r2))],
                 "r = 0 och r = %s ger y = A + Be<sup>%sx</sup>. Villkoren ger A = %s och B = %s: <b>%s</b>." % (sg(r2), kk(r2), sg(A), sg(B), res))

    sets = [("Karakteristisk ekvation", [(kar, 20)]), ("Två reella rötter", [(reella, 20)]), ("Dubbelrot", [(dubbel, 20)]), ("Komplexa rötter", [(komplex, 20)]), ("Begynnelsevillkor", [(villk, 20)])]
    return U("differentialekvationer-av-andra-ordningen", "DE", "Differentialekvationer av andra ordningen: karakteristisk ekvation", "Differentialekvationer, ordning 2",
             "Homogena linjära differentialekvationer av andra ordningen med konstanta koefficienter och den karakteristiska ekvationen.",
             "Uppgifter om differentialekvationer av andra ordningen för Matematik 5: karakteristisk ekvation, reella rötter, dubbelrot, komplexa rötter och begynnelsevillkor. 100 uppgifter med facit.",
             "y″ + ay′ + by = 0 → r² + ar + b = 0", "Rötternas typ ger lösningens form.", sets,
             ["Sätt y = e<sup>rx</sup>. Då blir y″ + ay′ + by = 0 den karakteristiska ekvationen r² + ar + b = 0.",
              "Två reella rötter: y = Ae<sup>r₁x</sup> + Be<sup>r₂x</sup>. Dubbelrot: y = (A + Bx)e<sup>rx</sup>.",
              "Komplexa rötter r = p ± qi: y = e<sup>px</sup>(A cos qx + B sin qx). Två villkor bestämmer A och B."],
             [("y″ − y′ − 6y = 0", ["r² − r − 6 = 0", "r = 3, r = −2"], "y = Ae<sup>3x</sup> + Be<sup>−2x</sup>"), ("y″ + 9y = 0", ["r = ±3i"], "y = A cos 3x + B sin 3x")],
             [["Glömmer Bx vid dubbelrot", "Dubbelrot ger (A + Bx)e<sup>rx</sup>"], ["Fel tecken i exponenten", "Roten r står i exponenten"], ["Bara ett villkor", "Andra ordningen behöver två villkor"]],
             [("Varför två konstanter?", "Ekvationen har andra ordningen, så två integrationer behövs."), ("Var finns sådana ekvationer?", "Svängningar, till exempel en fjäder eller en pendel."), ("Vad betyder dämpning?", "Faktorn e<sup>px</sup> med p &lt; 0 gör svängningen mindre.")])


# ============================================================ tillämpningar
def de_till():
    def kyla():
        T0 = ri(60, 95)
        Tr = ri(15, 25)
        k = F(ri(2, 10), 100)
        t = ri(5, 30)
        T = Tr + (T0 - Tr) * math.exp(-float(k) * t)
        w = [int(round(T0 * math.exp(-float(k) * t))), int(round(Tr + (T0 - Tr) * math.exp(-float(k) * t / 2))), int(round((T0 + Tr) / 2.0)), int(round(Tr + (T0 - Tr) * math.exp(-float(k) * t * 2)))]
        return M("Kaffe som är %d °C svalnar i ett rum som är %d °C enligt T%s = −%s(T − %d). Vilken temperatur har kaffet efter %d minuter? Avrunda till heltal." % (T0, Tr, P_, d(k), Tr, t), "%d °C" % int(round(T)),
                 ["%d °C" % x for x in w if x != int(round(T))],
                 "T = %d + %de<sup>−%st</sup>. T(%d) ≈ <b>%d °C</b>." % (Tr, T0 - Tr, d(k), t, int(round(T))))

    def tillv():
        N0 = ri(1, 9) * 100
        k = F(ri(1, 20), 100)
        t = ri(2, 20)
        N = N0 * math.exp(float(k) * t)
        return M("En population växer enligt N%s = %sN med N(0) = %d. Hur stor är den efter %d år? Avrunda till heltal." % (P_, d(k), N0, t), num(int(round(N))), [num(int(round(N0 * (1 + float(k)) ** t))) if int(round(N0 * (1 + float(k)) ** t)) != int(round(N)) else num(int(round(N)) + 1), num(int(round(N0 + float(k) * t * N0))), num(int(round(N0 * math.exp(float(k)) * t)))],
                 "N = %de<sup>%st</sup>. N(%d) ≈ <b>%s</b>." % (N0, d(k), t, num(int(round(N)))))

    def halv():
        T = ri(2, 40)
        k = math.log(2) / T
        return M("Ett radioaktivt ämne sönderfaller enligt N%s = −kN och har halveringstiden %d år. Bestäm k. Avrunda till fyra decimaler." % (P_, T), fl(k, 4), [fl(1.0 / T, 4), fl(0.5 / T, 4), fl(math.log10(2) / T, 4)], "e<sup>−kT</sup> = 1/2 ger k = ln 2 / %d ≈ <b>%s</b>." % (T, fl(k, 4)))

    def jamvikt():
        a = ri(1, 9)
        b = ri(1, 20) * a
        k = ri(0, 1)
        if k == 0:
            return MN("En tank fylls så att volymen V uppfyller V%s = %d − %s V. Vilket värde närmar sig V med tiden?" % (P_, b, d(F(a, 10))), F(b * 10, a), [b, F(b, a), F(a, 10)], "Jämvikt när V%s = 0: V = %d / %s = <b>%s</b>." % (P_, b, d(F(a, 10)), d(F(b * 10, a))))
        L = ri(2, 20) * 100
        return MN("Logistisk tillväxt: y%s = ky(1 − y/%s). Vilket värde närmar sig y?" % (P_, num(L)), L, [L // 2, 0, 2 * L], "Bärförmågan är <b>%s</b>." % num(L))

    def modell():
        P = [("Hastigheten med vilken ett rykte sprids är proportionell mot antalet som har hört det.", "y%s = ky" % P_, ["y%s = k" % P_, "y%s = ky²" % P_, "y%s = −ky" % P_]),
             ("Ett ämne sönderfaller med en hastighet proportionell mot mängden.", "y%s = −ky" % P_, ["y%s = ky" % P_, "y%s = −k" % P_, "y%s = −ky" % PP]),
             ("En kropp svalnar med en hastighet proportionell mot skillnaden till omgivningens temperatur T₀.", "T%s = −k(T − T₀)" % P_, ["T%s = −kT" % P_, "T%s = k(T + T₀)" % P_, "T%s = −k" % P_]),
             ("En fjäder svänger så att accelerationen är proportionell mot och motriktad utslaget.", "y%s = −ky" % PP, ["y%s = −ky" % P_, "y%s = ky" % PP, "y%s = −k" % PP]),
             ("En sjukdom sprids så att ökningen är proportionell mot antalet sjuka och antalet friska i en grupp på M personer.", "y%s = ky(M − y)" % P_, ["y%s = ky" % P_, "y%s = k(M − y)" % P_, "y%s = kM" % P_])]
        q, r, w = ch(P)
        n = ri(1, 9)
        return M("%s Vilken differentialekvation beskriver förloppet? (k &gt; 0, modell %d)" % (q, n), r, w, "<b>%s</b>." % r)

    sets = [("Newtons avsvalningslag", [(kyla, 20)]), ("Exponentiell tillväxt", [(tillv, 20)]), ("Halveringstid", [(halv, 20)]), ("Jämvikt och logistisk tillväxt", [(jamvikt, 20)]), ("Ställ upp modellen", [(modell, 10), (kyla, 5), (halv, 5)])]
    return U("tillampningar-av-differentialekvationer", "DE", "Differentialekvationer som modeller: tillväxt och avsvalning", "Tillämpningar av differentialekvationer",
             "Användning av differentialekvationer som modeller för förlopp inom olika områden och tolkning av lösningarna.",
             "Uppgifter om tillämpningar av differentialekvationer för Matematik 5: avsvalning, tillväxt, halveringstid, jämvikt och logistisk tillväxt samt att ställa upp modeller. 100 uppgifter med facit.",
             "Förändring proportionell mot y: y′ = ky", "Jämvikt där y′ = 0.", sets,
             ["Om förändringshastigheten är proportionell mot mängden gäller y′ = ky (tillväxt) eller y′ = −ky (sönderfall).",
              "Newtons avsvalningslag T′ = −k(T − T₀) har lösningen T = T₀ + Ce<sup>−kt</sup>.",
              "Vid jämvikt är derivatan 0. För logistisk tillväxt y′ = ky(1 − y/L) närmar sig y bärförmågan L."],
             [("Halveringstid 10 år", ["e<sup>−10k</sup> = 1/2", "k = ln 2 / 10"], "k ≈ 0,0693")],
             [["Använder procentuell ökning i stället för e", "Lösningen är Ce<sup>kt</sup>"], ["Glömmer omgivningens temperatur", "T = T₀ + Ce<sup>−kt</sup>"], ["Fel tecken för sönderfall", "Sönderfall ger −k"]],
             [("Vad är bärförmåga?", "Det största antal som miljön kan försörja."), ("Kan man lösa differentialekvationer numeriskt?", "Ja, med till exempel Eulers metod och digitala verktyg."), ("Vad betyder k?", "Hur snabbt förändringen sker.")])


# ============================================================ mängdlära
def mangd():
    def union():
        a, b = ri(10, 60), ri(10, 60)
        c = ri(1, min(a, b) - 1)
        tot = a + b - c + ri(0, 20)
        k = ri(0, 2)
        if k == 0:
            return MN("I en klass spelar %d elever fotboll, %d spelar handboll och %d spelar båda. Hur många spelar minst en av sporterna?" % (a, b, c), a + b - c, [a + b, a + b - 2 * c, a + b + c], "|A ∪ B| = |A| + |B| − |A ∩ B| = %d + %d − %d = <b>%d</b>." % (a, b, c, a + b - c))
        if k == 1:
            u = a + b - c
            return MN("%d personer tillfrågades. %d gillar te, %d gillar kaffe och %d gillar minst ett av dem. Hur många gillar båda?" % (tot, a, b, u), c, [a + b - u + 1 if a + b - u + 1 != c else c + 2, tot - u, a + b], "|A ∩ B| = |A| + |B| − |A ∪ B| = %d + %d − %d = <b>%d</b>." % (a, b, u, c))
        return MN("Av %d elever läser %d spanska, %d tyska och %d båda. Hur många läser inget av språken?" % (tot, a, b, c), tot - (a + b - c), [tot - a - b if tot - a - b >= 0 else tot - a, tot - c, a + b - c], "%d − (%d + %d − %d) = <b>%d</b>." % (tot, a, b, c, tot - a - b + c))

    def op():
        U_ = list(range(1, ri(9, 12)))
        A = sorted(sh(U_)[:ri(3, 5)])
        B = sorted(sh(U_)[:ri(3, 5)])
        k = ri(0, 3)
        fmt = lambda s: "{" + ", ".join(map(str, sorted(s))) + "}" if s else "∅"
        ops = [("A ∩ B", set(A) & set(B)), ("A ∪ B", set(A) | set(B)), ("A \\ B".replace("\\", "∖"), set(A) - set(B)), ("B ∖ A", set(B) - set(A))]
        name, res = ops[k]
        w = [fmt(r) for n_, r in ops if n_ != name and r != res]
        return M("A = %s och B = %s. Bestäm %s." % (fmt(A), fmt(B), name), fmt(res), w + [fmt(set(A) ^ set(B))], "<b>%s = %s</b>." % (name, fmt(res)))

    def komplement():
        n = ri(8, 12)
        U_ = list(range(1, n + 1))
        A = sorted(sh(U_)[:ri(3, 6)])
        fmt = lambda s: "{" + ", ".join(map(str, sorted(s))) + "}" if s else "∅"
        res = set(U_) - set(A)
        return M("Grundmängden är U = {1, 2, …, %d} och A = %s. Bestäm komplementet A%s." % (n, fmt(A), "<sup>c</sup>"), fmt(res), [fmt(A), fmt(set(list(res)[:-1])) if len(res) > 1 else "∅", fmt(set(U_))], "Alla element i U som inte finns i A: <b>%s</b>." % fmt(res))

    def symb():
        P = [("Vad betyder 3 ∈ A?", "3 är ett element i A", ["A är en delmängd av 3", "3 finns inte i A", "A har 3 element"]),
             ("Vad betyder A ⊆ B?", "Alla element i A finns i B", ["A och B har inga gemensamma element", "B ⊆ A", "A och B är lika stora"]),
             ("Vad betyder A ∩ B = ∅?", "A och B är disjunkta", ["A = B", "A ⊆ B", "A ∪ B = ∅"]),
             ("Vilken mängd betecknar ℤ?", "Heltalen", ["De naturliga talen", "De rationella talen", "De reella talen"]),
             ("Vilken mängd betecknar ℚ?", "De rationella talen", ["Heltalen", "De reella talen", "De komplexa talen"]),
             ("Hur många delmängder har en mängd med 4 element?", "16", ["4", "8", "24"]),
             ("Hur många delmängder har en mängd med 3 element?", "8", ["3", "6", "9"]),
             ("Hur många delmängder har en mängd med 5 element?", "32", ["5", "10", "25"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    def tre():
        a, b, c = ri(20, 40), ri(20, 40), ri(20, 40)
        ab, ac, bc = ri(5, 10), ri(5, 10), ri(5, 10)
        abc = ri(1, 4)
        u = a + b + c - ab - ac - bc + abc
        return MN("%d läser matte, %d fysik och %d kemi. %d läser matte och fysik, %d matte och kemi, %d fysik och kemi, och %d läser alla tre. Hur många läser minst ett ämne?" % (a, b, c, ab, ac, bc, abc), u, [a + b + c, a + b + c - ab - ac - bc, u - 2 * abc], "%d + %d + %d − %d − %d − %d + %d = <b>%d</b>." % (a, b, c, ab, ac, bc, abc, u))

    sets = [("Mängdoperationer", [(op, 20)]), ("Komplement", [(komplement, 20)]), ("Två mängder", [(union, 20)]), ("Tre mängder", [(tre, 20)]), ("Symboler och begrepp", [(symb, 8), (op, 12)])]
    return U("mangdlara", "DM", "Mängdlära: union, snitt, komplement och Venndiagram", "Mängdlära",
             "Grundläggande mängdlära: element, delmängd, union, snitt, differens och komplement, och lösning av problem med Venndiagram.",
             "Uppgifter om mängdlära för Matematik 5: mängdoperationer, komplement, två och tre mängder samt symboler och begrepp. 100 uppgifter med facit.",
             "|A ∪ B| = |A| + |B| − |A ∩ B|", "Snittet räknas annars två gånger.", sets,
             ["En mängd är en samling element. A ∪ B (union) innehåller element i A eller B. A ∩ B (snitt) innehåller element i båda.",
              "A ∖ B innehåller elementen i A som inte finns i B. Komplementet Aᶜ är allt i grundmängden som inte finns i A.",
              "Principen om inklusion och exklusion: |A ∪ B| = |A| + |B| − |A ∩ B|. För tre mängder lägger man tillbaka det trefaldiga snittet."],
             [("A = {1, 2, 3, 4}, B = {3, 4, 5}", ["A ∩ B = {3, 4}", "A ∪ B = {1, 2, 3, 4, 5}"], "")],
             [["Räknar snittet två gånger", "Dra bort |A ∩ B|"], ["Blandar ihop ∪ och ∩", "∪ = eller, ∩ = och"], ["Glömmer element som inte finns i någon mängd", "De ligger utanför cirklarna"]],
             [("Vad är den tomma mängden?", "Mängden utan element, ∅."), ("Vad är ett Venndiagram?", "En bild med cirklar som visar hur mängder överlappar."), ("Hur många delmängder har en mängd med n element?", "2ⁿ.")])


# ============================================================ kombinatorik
def kombinatorik():
    def perm():
        n = ri(3, 9)
        return MN(ch(["På hur många sätt kan %d personer ställa sig i en kö?", "På hur många sätt kan %d olika böcker ställas i en bokhylla?", "På hur många sätt kan %d lag placera sig i en tabell (utan delade placeringar)?"]) % n, math.factorial(n), [n * n, n * (n - 1), math.factorial(n - 1)], "%d! = <b>%s</b>." % (n, num(math.factorial(n))))

    def P_nk():
        n = ri(5, 12)
        k = ri(2, 4)
        v = math.perm(n, k)
        return MN("%d löpare tävlar. På hur många sätt kan guld, silver och brons fördelas?" % n if k == 3 else "Hur många ord med %d olika bokstäver kan bildas av %d olika bokstäver?" % (k, n), v, [math.comb(n, k), n ** k, math.factorial(k)], "%d · %d · … (%d faktorer) = <b>%s</b>." % (n, n - 1, k, num(v)))

    def C_nk():
        n = ri(5, 20)
        k = ri(2, 5)
        if k >= n:
            return None
        v = math.comb(n, k)
        return MN("På hur många sätt kan man välja %d personer av %d till en kommitté?" % (k, n), v, [math.perm(n, k), n * k, math.comb(n, k - 1)], "C(%d, %d) = %d!/(%d! · %d!) = <b>%s</b>." % (n, k, n, k, n - k, num(v)))

    def mult():
        a, b, c = ri(2, 8), ri(2, 8), ri(2, 6)
        return MN("En meny har %d förrätter, %d huvudrätter och %d efterrätter. Hur många olika middagar med en av varje kan man välja?" % (a, b, c), a * b * c, [a + b + c, a * b + c, math.comb(a + b + c, 3)], "Multiplikationsprincipen: %d · %d · %d = <b>%d</b>." % (a, b, c, a * b * c))

    def binom():
        n = ri(3, 8)
        k = ri(1, n - 1)
        a = ri(1, 3)
        coef = math.comb(n, k) * a ** (n - k)
        return MN("Bestäm koefficienten för x%s i (%sx + 1)%s." % (sup(k) if k > 1 else "", "" if a == 1 else a, sup(n)), math.comb(n, k) * a ** k, [math.comb(n, k), coef if coef != math.comb(n, k) * a ** k else coef + 1, a ** k], "Binomialsatsen: C(%d, %d) · %d%s = <b>%s</b>." % (n, k, a, sup(k), num(math.comb(n, k) * a ** k)))

    def prob():
        n = ri(8, 15)
        r = ri(3, n - 3)
        k = 2
        p = F(math.comb(r, k), math.comb(n, k))
        return MN("En påse har %d kulor, varav %d är röda. Två kulor dras utan återläggning. Vad är sannolikheten att båda är röda?" % (n, r), p, [F(r, n) ** 2, F(r, n) * F(r, n - 1), F(r * (r - 1), n * n)] if F(r, n) * F(r, n - 1) != p else [F(r, n) ** 2, F(r, n), F(2 * r, n * (n - 1))], "C(%d, 2)/C(%d, 2) = <b>%s</b>." % (r, n, fq(p)))

    sets = [("Permutationer", [(perm, 7), (P_nk, 13)]), ("Kombinationer", [(C_nk, 20)]), ("Multiplikationsprincipen", [(mult, 20)]), ("Binomialsatsen", [(binom, 20)]), ("Sannolikhet med kombinatorik", [(prob, 20)])]
    return U("kombinatorik", "DM", "Kombinatorik: permutationer, kombinationer och binomialsatsen", "Kombinatorik",
             "Metoder för kombinatorik: multiplikationsprincipen, permutationer, kombinationer och binomialsatsen.",
             "Uppgifter om kombinatorik för Matematik 5: permutationer, kombinationer, multiplikationsprincipen, binomialsatsen och sannolikhet. 100 uppgifter med facit.",
             "Ordning spelar roll: permutation", "Ordning spelar ingen roll: kombination.", sets,
             ["Multiplikationsprincipen: med a val och sedan b val finns a · b möjligheter.",
              "n föremål kan ordnas på n! sätt. Att välja och ordna k av n ger P(n, k) = n!/(n − k)!.",
              "Att välja k av n utan ordning ger C(n, k) = n!/(k!(n − k)!). Binomialsatsen: (a + b)ⁿ = Σ C(n, k) aⁿ⁻ᵏ bᵏ."],
             [("Välj 3 av 10", ["10!/(3! · 7!)"], "120"), ("3 av 10 på pallen", ["10 · 9 · 8"], "720")],
             [["Använder kombination när ordningen spelar roll", "Fråga: spelar ordningen roll?"], ["Adderar i stället för att multiplicera", "Oberoende val multipliceras"], ["0! = 0", "0! = 1"]],
             [("Vad betyder n!?", "n · (n − 1) · … · 2 · 1."), ("Varför är C(n, k) = C(n, n − k)?", "Att välja k är samma som att välja bort n − k."), ("Var används kombinatorik?", "I sannolikhet, kodning och schemaläggning.")])


# ============================================================ talteori och kongruensräkning
def kongruens():
    def mod_():
        a = ri(20, 999)
        n = ri(3, 13)
        return MN("Vilken rest får %d vid division med %d? (Bestäm %d mod %d.)" % (a, n, a, n), a % n, [a // n, (a + 1) % n, n - a % n if n - a % n != a % n else (a % n + 2) % n], "%d = %d · %d + %d: <b>%d</b>." % (a, n, a // n, a % n, a % n))

    def rakna():
        n = ri(5, 13)
        a, b = ri(20, 200), ri(20, 200)
        k = ri(0, 1)
        if k == 0:
            r = (a * b) % n
            return MN("Beräkna %d · %d (mod %d)." % (a, b, n), r, [(a + b) % n, (a % n) * (b % n), (r + 1) % n], "%d ≡ %d och %d ≡ %d, så produkten ≡ %d · %d ≡ <b>%d</b>." % (a, a % n, b, b % n, a % n, b % n, r))
        e = ri(10, 99)
        r = pow(a, e, n)
        return MN("Beräkna %d%s (mod %d)." % (a % 10 + 2, sup(e), n), pow(a % 10 + 2, e, n), [(a % 10 + 2) * e % n, pow(a % 10 + 2, e - 1, n) if pow(a % 10 + 2, e - 1, n) != pow(a % 10 + 2, e, n) else (pow(a % 10 + 2, e, n) + 1) % n, e % n], "Leta efter ett mönster i potenserna mod %d: <b>%d</b>." % (n, pow(a % 10 + 2, e, n)))

    def sista():
        b = ri(2, 9)
        e = ri(10, 200)
        r = pow(b, e, 10)
        return MN("Vilken är sista siffran i %d%s?" % (b, sup(e)), r, [(b * e) % 10, b, pow(b, e + 1, 10) if pow(b, e + 1, 10) != r else (r + 2) % 10], "Sista siffran är %d%s mod 10. Siffrorna upprepas med en period: <b>%d</b>." % (b, sup(e), r))

    def sgd():
        a, b = ri(2, 30), ri(2, 30)
        g = ri(2, 15)
        A, B = a * g, b * g
        gg = math.gcd(A, B)
        return MN("Bestäm SGD(%d, %d) med Euklides algoritm." % (A, B), gg, [A * B // gg, min(A, B), gg * 2 if gg * 2 != min(A, B) else gg + 1], "Euklides algoritm ger <b>%d</b>." % gg)

    def kongr():
        n = ri(3, 12)
        a = ri(10, 99)
        opts = [a + n * ri(1, 5), a + ri(1, n - 1), a + n * ri(1, 5) + 1, a + 2 * n + ri(1, n - 1)]
        r = opts[0]
        return MQ("Vilket tal är kongruent med %d modulo %d:" % (a, n), str(r), [str(x) for x in opts[1:]], "Skillnaden %d − %d = %d är delbar med %d: <b>%d</b>." % (r, a, r - a, n, r))

    def dioph():
        a, b = ri(2, 9), ri(2, 9)
        if math.gcd(a, b) != 1:
            return None
        x, y = ri(1, 6), ri(1, 6)
        c = a * x + b * y
        # alla positiva lösningar
        sols = [(xx, (c - a * xx) // b) for xx in range(1, c // a + 1) if (c - a * xx) % b == 0 and (c - a * xx) // b > 0]
        if len(sols) != 1:
            return None
        return M("Bestäm den lösning i positiva heltal till %dx + %dy = %d." % (a, b, c), "x = %d, y = %d" % sols[0], ["x = %d, y = %d" % (sols[0][1], sols[0][0]) if sols[0][1] != sols[0][0] else "x = %d, y = %d" % (sols[0][0] + 1, sols[0][1]), "x = %d, y = %d" % (sols[0][0] + b, sols[0][1]), "x = %d, y = %d" % (sols[0][0], sols[0][1] + a)],
                 "%d · %d + %d · %d = %d: <b>x = %d, y = %d</b>." % (a, sols[0][0], b, sols[0][1], c, sols[0][0], sols[0][1]))

    sets = [("Rest och mod", [(mod_, 20)]), ("Räkna modulo n", [(rakna, 20)]), ("Sista siffran", [(sista, 20)]), ("Kongruenta tal och SGD", [(kongr, 10), (sgd, 10)]), ("Diofantiska ekvationer", [(dioph, 20)])]
    return U("talteori-och-kongruensrakning", "DM", "Talteori och kongruensräkning", "Kongruensräkning",
             "Delbarhet, Euklides algoritm och kongruensräkning samt enkla diofantiska ekvationer.",
             "Uppgifter om talteori och kongruensräkning för Matematik 5: rest och mod, räkna modulo n, sista siffran, kongruenta tal, SGD och diofantiska ekvationer. 100 uppgifter med facit.",
             "a ≡ b (mod n): n delar a − b", "Byt tal mot resten innan du räknar.", sets,
             ["a ≡ b (mod n) betyder att a och b ger samma rest vid division med n, alltså att n delar a − b.",
              "I kongruensräkning kan du byta varje tal mot dess rest innan du adderar, multiplicerar eller upphöjer.",
              "Euklides algoritm ger största gemensamma delaren SGD(a, b) genom upprepad division med rest."],
             [("7¹⁰⁰ mod 10", ["7, 9, 3, 1, 7, …", "Period 4", "100 = 4 · 25"], "1")],
             [["Blandar ihop kvot och rest", "Resten är det som blir över"], ["Räknar ut hela potensen", "Byt mot rester tidigt"], ["Negativ rest", "Resten ligger mellan 0 och n − 1"]],
             [("Var används kongruensräkning?", "I kryptering, kontrollsiffror och kalendrar."), ("Vad är en diofantisk ekvation?", "En ekvation där man söker heltalslösningar."), ("Vad betyder SGD?", "Största gemensamma delare.")])


# ============================================================ talbaser
def talbaser():
    def tillbin():
        n = ri(5, 255)
        r = bin(n)[2:]
        return M("Skriv %d i det binära talsystemet (bas 2)." % n, r, [bin(n + 1)[2:], bin(n - 1)[2:], r[::-1] if r[::-1] != r else bin(n + 2)[2:]], "Dela upprepat med 2 och läs resterna bakifrån: <b>%s<sub>2</sub></b>." % r)

    def frbin():
        n = ri(5, 255)
        r = bin(n)[2:]
        return MN("Skriv %s<sub>2</sub> i det decimala talsystemet." % r, n, [int(r[::-1], 2) if int(r[::-1], 2) != n else n + 1, r.count("1"), n + 2], "Summera tvåpotenserna: <b>%d</b>." % n)

    def hexa():
        n = ri(16, 4095)
        h = "%X" % n
        if coin():
            return M("Skriv %d i det hexadecimala talsystemet (bas 16)." % n, h, ["%X" % (n + 1), "%X" % (n + 16), h[::-1] if h[::-1] != h else "%X" % (n + 2)], "Dela med 16. Resterna 10–15 skrivs A–F: <b>%s<sub>16</sub></b>." % h)
        return MN("Skriv %s<sub>16</sub> i det decimala talsystemet." % h, n, [int(h[::-1], 16) if int(h[::-1], 16) != n else n + 1, n + 16, n - 1], "<b>%s</b>." % num(n))

    def annan():
        b = ri(3, 8)
        n = ri(b, b ** 3 - 1)
        digs = []
        m = n
        while m:
            digs.append(str(m % b))
            m //= b
        s = "".join(reversed(digs))
        if coin():
            return M("Skriv %d i bas %d." % (n, b), s, [s[::-1] if s[::-1] != s else s + "0", "".join(reversed(digs[:-1])) + str(int(digs[-1]) + 1), str(int(s) + 1)], "Dela upprepat med %d: <b>%s<sub>%d</sub></b>." % (b, s, b))
        return MN("Skriv %s<sub>%d</sub> i det decimala talsystemet." % (s, b), n, [n - 1, int(s[::-1], b) if int(s[::-1], b) != n else n + 1, n + b], "<b>%d</b>." % n)

    def rakna():
        a, b = ri(3, 60), ri(3, 60)
        r = bin(a + b)[2:]
        return M("Beräkna %s<sub>2</sub> + %s<sub>2</sub>. Svara i bas 2." % (bin(a)[2:], bin(b)[2:]), r, [bin(a + b + 1)[2:], bin(a ^ b)[2:] if (a ^ b) != a + b else bin(a + b - 1)[2:], bin(a + b + 2)[2:]], "%d + %d = %d = <b>%s<sub>2</sub></b>." % (a, b, a + b, r))

    sets = [("Till binär form", [(tillbin, 20)]), ("Från binär form", [(frbin, 20)]), ("Hexadecimala tal", [(hexa, 20)]), ("Andra baser", [(annan, 20)]), ("Räkna i bas 2", [(rakna, 20)])]
    return U("talbaser", "DM", "Talbaser: binära, hexadecimala och andra talsystem", "Talbaser",
             "Positionssystem med olika baser, särskilt binära och hexadecimala tal, och omvandling mellan baser.",
             "Uppgifter om talbaser för Matematik 5: till och från binär form, hexadecimala tal, andra baser och addition i bas 2. 100 uppgifter med facit.",
             "1011₂ = 8 + 2 + 1 = 11", "Varje position är en potens av basen.", sets,
             ["I ett positionssystem med bas b är positionernas värden 1, b, b², b³, …",
              "Binära tal har basen 2 och siffrorna 0 och 1. Hexadecimala tal har basen 16 och siffrorna 0–9 och A–F.",
              "Omvandla till bas b genom att dividera upprepat med b och läsa resterna bakifrån."],
             [("13 i bas 2", ["13 = 8 + 4 + 1"], "1101₂"), ("2F₁₆", ["2 · 16 + 15"], "47")],
             [["Läser resterna framifrån", "Läs dem nedifrån och upp"], ["F = 16", "F = 15"], ["Adderar binärt som decimalt", "1 + 1 = 10 i bas 2"]],
             [("Varför använder datorer bas 2?", "Elektroniska kretsar har två lägen, av och på."), ("Var används hexadecimala tal?", "För färgkoder och minnesadresser."), ("Hur många siffror finns i bas 8?", "Åtta: 0–7.")])


# ============================================================ rekursiva talföljder
def rekursion():
    def term():
        a0 = ri(-5, 9)
        p, q = ch([1, 2, 3, -1]), ri(-5, 5)
        n = ri(3, 5)
        a = a0
        for _ in range(n):
            a = p * a + q
        return MN("En talföljd ges av a<sub>0</sub> = %s och a<sub>n+1</sub> = %s. Bestäm a<sub>%d</sub>." % (sg(a0), expr([(p, "a<sub>n</sub>"), (q, "")]), n), a, [a - q, p * a + q, a0 + n * q], "Räkna term för term: <b>%s</b>." % sg(a))

    def aritm():
        a1 = ri(-10, 20)
        dd = nz(-6, 9)
        n = ri(10, 60)
        k = ri(0, 1)
        if k == 0:
            an = a1 + (n - 1) * dd
            return MN("En aritmetisk talföljd har a<sub>1</sub> = %s och differensen %s. Bestäm a<sub>%d</sub>." % (sg(a1), sg(dd), n), an, [a1 + n * dd, n * dd, a1 + (n - 2) * dd], "a<sub>n</sub> = a<sub>1</sub> + (n − 1)d = <b>%s</b>." % sg(an))
        S = n * (2 * a1 + (n - 1) * dd) // 2
        return MN("Beräkna summan av de %d första termerna i den aritmetiska talföljden %s, %s, %s, …" % (n, sg(a1), sg(a1 + dd), sg(a1 + 2 * dd)), S, [n * (a1 + (n - 1) * dd), S + a1, n * a1], "S = n(a<sub>1</sub> + a<sub>n</sub>)/2 = %d(%s + %s)/2 = <b>%s</b>." % (n, sg(a1), par(a1 + (n - 1) * dd), num(S) if S >= 0 else MIN + num(-S)))

    def geom():
        a1 = ri(1, 9)
        k = ch([2, 3, -2])
        n = ri(5, 10)
        S = a1 * (k ** n - 1) // (k - 1)
        if coin():
            return MN("En geometrisk talföljd har a<sub>1</sub> = %d och kvoten %s. Bestäm a<sub>%d</sub>." % (a1, sg(k), n), a1 * k ** (n - 1), [a1 * k ** n, a1 * k * (n - 1), k ** (n - 1)], "a<sub>n</sub> = a<sub>1</sub> · k<sup>n − 1</sup> = <b>%s</b>." % sg(a1 * k ** (n - 1)))
        return MN("Beräkna summan av de %d första termerna i den geometriska talföljden %d, %s, %s, …" % (n, a1, sg(a1 * k), sg(a1 * k * k)), S, [a1 * k ** n, a1 * (k ** (n + 1) - 1) // (k - 1), S - a1], "S = a<sub>1</sub>(kⁿ − 1)/(k − 1) = <b>%s</b>." % sg(S))

    def sluten():
        a0 = ri(0, 9)
        dd = nz(-5, 8)
        k = coin()
        if k:
            r = "a<sub>n</sub> = %s" % expr([(dd, "n"), (a0, "")])
            return M("Talföljden ges av a<sub>0</sub> = %d och a<sub>n+1</sub> = a<sub>n</sub> %s %d. Vilken är den slutna formeln?" % (a0, "+" if dd > 0 else "−", abs(dd)), r, ["a<sub>n</sub> = %s" % expr([(a0, "n"), (dd, "")]), "a<sub>n</sub> = %s" % expr([(dd, "n"), (a0 - dd, "")]) if a0 - dd != a0 else "a<sub>n</sub> = %dn" % dd, "a<sub>n</sub> = %s · %d<sup>n</sup>" % (a0 if a0 else 1, abs(dd))], "Varje steg lägger till %s: <b>%s</b>." % (sg(dd), r))
        q = ch([2, 3, 5])
        a0 = ri(1, 9)
        r = "a<sub>n</sub> = %s%d<sup>n</sup>" % ("" if a0 == 1 else "%d · " % a0, q)
        return M("Talföljden ges av a<sub>0</sub> = %d och a<sub>n+1</sub> = %da<sub>n</sub>. Vilken är den slutna formeln?" % (a0, q), r, ["a<sub>n</sub> = %s" % expr([(a0 * q, "n")]), "a<sub>n</sub> = %s%d<sup>n</sup>" % ("" if q == 1 else "%d · " % q, a0) if a0 > 1 else "a<sub>n</sub> = %d<sup>n + 1</sup>" % q, "a<sub>n</sub> = %s" % expr([(q, "n"), (a0, "")])], "Varje steg multiplicerar med %d: <b>%s</b>." % (q, r))

    def fib():
        a, b = ri(1, 5), ri(1, 5)
        n = ri(5, 8)
        x, y = a, b
        for _ in range(n - 2):
            x, y = y, x + y
        return MN("En talföljd har a<sub>1</sub> = %d, a<sub>2</sub> = %d och a<sub>n</sub> = a<sub>n−1</sub> + a<sub>n−2</sub>. Bestäm a<sub>%d</sub>." % (a, b, n), y, [x, x + y, y + 1], "Räkna term för term: <b>%d</b>." % y)

    sets = [("Rekursiva formler", [(term, 20)]), ("Aritmetiska talföljder", [(aritm, 20)]), ("Geometriska talföljder", [(geom, 20)]), ("Sluten formel", [(sluten, 20)]), ("Blandat", [(fib, 8), (term, 6), (aritm, 6)])]
    return U("rekursiva-talfoljder", "DM", "Talföljder: rekursiva och slutna formler samt summor", "Talföljder",
             "Talföljder definierade rekursivt och med slutna formler. Aritmetiska och geometriska talföljder och summor.",
             "Uppgifter om talföljder för Matematik 5: rekursiva formler, aritmetiska och geometriska talföljder och summor, slutna formler och Fibonaccitypen. 100 uppgifter med facit.",
             "Rekursiv: nästa term ur föregående", "Sluten: termen direkt ur n.", sets,
             ["En rekursiv formel ger nästa term ur den eller de föregående, till exempel a<sub>n+1</sub> = 2a<sub>n</sub> + 1.",
              "Aritmetisk talföljd: a<sub>n</sub> = a<sub>1</sub> + (n − 1)d och summan S = n(a<sub>1</sub> + a<sub>n</sub>)/2.",
              "Geometrisk talföljd: a<sub>n</sub> = a<sub>1</sub>k<sup>n−1</sup> och summan S = a<sub>1</sub>(kⁿ − 1)/(k − 1)."],
             [("a₁ = 3, d = 4, a₂₀", ["3 + 19 · 4"], "79")],
             [["a<sub>n</sub> = a<sub>1</sub> + nd", "Det är (n − 1)d"], ["Fel startindex", "Kontrollera om följden börjar med a₀ eller a₁"], ["Blandar ihop kvot och differens", "Geometrisk: multiplicera"]],
             [("Vad är skillnaden mellan rekursiv och sluten formel?", "Den rekursiva behöver föregående termer, den slutna ger termen direkt."), ("Var används talföljder?", "I ränteberäkningar, populationer och algoritmer."), ("Vad är Fibonaccis talföljd?", "1, 1, 2, 3, 5, 8, … där varje term är summan av de två föregående.")])


# ============================================================ bevis och induktion
def bevis():
    def metod():
        P = [("Man antar att √2 är rationellt och visar att det leder till en motsägelse.", "Motsägelsebevis"), ("Man visar att påståendet gäller för n = 1 och att det gäller för n + 1 om det gäller för n.", "Induktionsbevis"),
             ("Man visar att om n² är jämnt så är n jämnt genom att visa att om n är udda så är n² udda.", "Kontrapositivt bevis"), ("Man visar att summan av två jämna tal 2a och 2b är 2(a + b).", "Direkt bevis"),
             ("Man visar att det finns oändligt många primtal genom att anta att det finns ändligt många.", "Motsägelsebevis"), ("Man visar att 1 + 2 + … + n = n(n + 1)/2 för alla positiva heltal n.", "Induktionsbevis"),
             ("Man visar att påståendet är falskt genom ett enda exempel där det inte gäller.", "Motexempel")]
        q, r = ch(P)
        n = ri(1, 9)
        return M("Vilken bevismetod beskrivs? %s (Fall %d)" % (q, n), r, [x for x in ("Motsägelsebevis", "Induktionsbevis", "Kontrapositivt bevis", "Direkt bevis", "Motexempel") if x != r][:3] if r != "Motexempel" else ["Motsägelsebevis", "Induktionsbevis", "Direkt bevis"], "<b>%s</b>." % r)

    def bas():
        P = [("1 + 2 + … + n = n(n + 1)/2", lambda n: n * (n + 1) // 2), ("1 + 3 + 5 + … + (2n − 1) = n²", lambda n: n * n), ("1² + 2² + … + n² = n(n + 1)(2n + 1)/6", lambda n: n * (n + 1) * (2 * n + 1) // 6),
             ("2 + 4 + … + 2n = n(n + 1)", lambda n: n * (n + 1)), ("1 + 2 + 4 + … + 2ⁿ⁻¹ = 2ⁿ − 1", lambda n: 2 ** n - 1)]
        q, f = ch(P)
        n = ri(3, 10)
        v = f(n)
        return MN("Formeln %s ska bevisas med induktion. Vilket värde ger högerledet för n = %d?" % (q, n), v, [f(n - 1), f(n + 1), v + n], "Sätt in n = %d: <b>%s</b>." % (n, num(v)))

    def steg():
        P = [("1 + 2 + … + n = n(n + 1)/2", "n(n + 1)/2 + (n + 1)", ["n(n + 1)/2 + n", "(n + 1)(n + 2)/2 + n", "n(n + 1)/2 · (n + 1)"]),
             ("1 + 3 + … + (2n − 1) = n²", "n² + (2n + 1)", ["n² + (2n − 1)", "n² + 2n", "(n + 1)² + (2n + 1)"]),
             ("2 + 4 + … + 2n = n(n + 1)", "n(n + 1) + 2(n + 1)", ["n(n + 1) + 2n", "n(n + 1) + (n + 1)", "(n + 1)(n + 2) + 2"]),
             ("1 + 2 + 4 + … + 2ⁿ⁻¹ = 2ⁿ − 1", "2ⁿ − 1 + 2ⁿ", ["2ⁿ − 1 + 2ⁿ⁺¹", "2ⁿ⁺¹ − 1 + 2ⁿ", "2ⁿ + 2ⁿ⁻¹"])]
        q, r, w = ch(P)
        n = ri(1, 9)
        return M("Induktionssteget för %s: antag att formeln gäller för n = p. Vad blir vänsterledet för n = p + 1 uttryckt med antagandet? (Skrivet med n i stället för p, uppgift %d.)" % (q, n), r, w, "Lägg till nästa term till antagandet: <b>%s</b>." % r)

    def delbar():
        P = [("n³ − n", 6), ("n² + n", 2), ("n(n + 1)(n + 2)", 6), ("4ⁿ − 1", 3), ("7ⁿ − 1", 6), ("n⁵ − n", 5), ("5ⁿ − 1", 4), ("3²ⁿ − 1", 8)]
        q, k = ch(P)
        n = ri(2, 9)
        return MN("För alla positiva heltal n är %s delbart med ett visst tal. Vilket är det största tal som alltid delar uttrycket? (Pröva t.ex. n = %d.)" % (q, n), k, [k * 2, k - 1 if k > 2 else k + 1, k + 2], "Pröva några n och bevisa med induktion: <b>%d</b>." % k)

    def irr():
        P = [("√2", "Irrationellt"), ("√9", "Rationellt"), ("0,333…", "Rationellt"), ("π", "Irrationellt"), ("√3", "Irrationellt"), ("22/7", "Rationellt"), ("√16 + 1", "Rationellt"), ("√5", "Irrationellt"), ("1,25", "Rationellt"), ("√2 + 1", "Irrationellt"), ("e", "Irrationellt"), ("√49", "Rationellt")]
        q, r = ch(P)
        return M("Är talet %s rationellt eller irrationellt?" % q, r, ["Irrationellt" if r == "Rationellt" else "Rationellt", "Varken eller", "Det går inte att avgöra"], "<b>%s</b>." % r)

    sets = [("Bevismetoder", [(metod, 20)]), ("Induktionsbas", [(bas, 20)]), ("Induktionssteget", [(steg, 20)]), ("Delbarhet", [(delbar, 8), (bas, 12)]), ("Rationella och irrationella tal", [(irr, 12), (metod, 8)])]
    return U("bevismetoder-och-induktion", "DM", "Bevismetoder: direkt bevis, motsägelse och induktion", "Bevismetoder och induktion",
             "Olika bevismetoder: direkt bevis, kontrapositivt bevis, motsägelsebevis och induktionsbevis.",
             "Uppgifter om bevismetoder för Matematik 5: känna igen bevismetoder, induktionsbas och induktionssteg, delbarhet och rationella och irrationella tal. 100 uppgifter med facit.",
             "Induktion: bas + steg", "Visa för n = 1 och från n till n + 1.", sets,
             ["Direkt bevis: utgå från förutsättningarna och dra slutsatser steg för steg. Kontrapositivt bevis: visa att icke q medför icke p.",
              "Motsägelsebevis: anta motsatsen och visa att det leder till något omöjligt, till exempel att √2 är rationellt.",
              "Induktionsbevis: visa att påståendet gäller för n = 1 (basen) och att det gäller för n = p + 1 om det gäller för n = p (steget)."],
             [("1 + 2 + … + n = n(n + 1)/2", ["Bas: 1 = 1 · 2/2", "Steg: p(p + 1)/2 + (p + 1) = (p + 1)(p + 2)/2"], "")],
             [["Glömmer basfallet", "Både bas och steg behövs"], ["Antar det som ska bevisas", "Antagandet gäller bara n = p"], ["Tror att exempel bevisar", "Ett exempel kan bara motbevisa"]],
             [("Varför fungerar induktion?", "Som dominobrickor: den första faller, och varje bricka fäller nästa."), ("Vad är kontraposition?", "p ⇒ q är ekvivalent med icke q ⇒ icke p."), ("Vad är ett motsägelsebevis?", "Man visar att motsatsen är omöjlig.")])


# ============================================================ grafer och nätverk
def grafer():
    def grad():
        n = ri(4, 8)
        m = ri(n, n * (n - 1) // 2)
        return MN("En graf har %d hörn och %d kanter. Vad är summan av alla hörns gradtal?" % (n, m), 2 * m, [m, n, m + n], "Varje kant ger två gradtal: 2 · %d = <b>%d</b>." % (m, 2 * m))

    def komplett():
        n = ri(3, 25)
        return MN(ch(["Hur många kanter har den kompletta grafen med %d hörn?", "%d lag möts en gång var i en serie. Hur många matcher spelas? (Tänk på en komplett graf.)"]) % n, n * (n - 1) // 2, [n * (n - 1), n * n, n - 1], "Varje par av hörn förbinds: %d · %d / 2 = <b>%d</b>." % (n, n - 1, n * (n - 1) // 2))

    def euler():
        n = ri(4, 7)
        degs = [ri(1, 5) for _ in range(n)]
        if sum(degs) % 2:
            degs[-1] += 1
        odd = sum(1 for x in degs if x % 2)
        r = "Eulerkrets" if odd == 0 else "Eulerväg men ingen Eulerkrets" if odd == 2 else "Varken Eulerväg eller Eulerkrets"
        return M("En sammanhängande graf har hörn med gradtalen %s. Vad gäller?" % lista(map(str, degs)), r, [x for x in ("Eulerkrets", "Eulerväg men ingen Eulerkrets", "Varken Eulerväg eller Eulerkrets", "Både Eulerkrets och udda hörn") if x != r], "Antalet hörn med udda gradtal är %d: <b>%s</b>." % (odd, r.lower()))

    def kortast():
        a, b, c, e = ri(2, 9), ri(2, 9), ri(2, 9), ri(2, 9)
        f = ri(5, 20)
        # A-B a, B-D b, A-C c, C-D e, A-D f
        r = min(a + b, c + e, f)
        return MN("Avstånd: A–B %d km, B–D %d km, A–C %d km, C–D %d km och A–D %d km. Vilken är den kortaste vägen från A till D?" % (a, b, c, e, f), r, [max(a + b, c + e), f if f != r else a + b + c + e, a + b + c + e], "Jämför %d, %d och %d: <b>%d km</b>." % (a + b, c + e, f, r), "km")

    def trad():
        n = ri(3, 30)
        return MN("Ett träd har %d hörn. Hur många kanter har det?" % n, n - 1, [n, n + 1, n * (n - 1) // 2], "Ett träd med n hörn har n − 1 kanter: <b>%d</b>." % (n - 1))

    sets = [("Gradtal", [(grad, 20)]), ("Kompletta grafer och träd", [(komplett, 10), (trad, 10)]), ("Eulervägar", [(euler, 20)]), ("Kortaste vägen", [(kortast, 20)]), ("Blandat", [(grad, 5), (komplett, 5), (trad, 5), (euler, 5)])]
    return U("grafer-och-natverk", "DM", "Grafteori: gradtal, träd, Eulervägar och kortaste vägen", "Grafer och nätverk",
             "Grafteori med begreppen hörn, kant och gradtal samt problemlösning med grafer, till exempel Eulervägar och kortaste vägen.",
             "Uppgifter om grafer och nätverk för Matematik 5: gradtal, kompletta grafer, träd, Eulervägar och kortaste vägen. 100 uppgifter med facit.",
             "Summan av gradtalen = 2 · antalet kanter", "Eulerkrets: alla gradtal jämna.", sets,
             ["En graf består av hörn och kanter. Ett hörns gradtal är antalet kanter som möts där.",
              "Summan av alla gradtal är två gånger antalet kanter. Den kompletta grafen med n hörn har n(n − 1)/2 kanter, och ett träd har n − 1 kanter.",
              "En sammanhängande graf har en Eulerkrets om alla gradtal är jämna och en Eulerväg om exakt två är udda."],
             [("Gradtal 2, 2, 3, 3", ["Två udda hörn"], "Eulerväg men ingen Eulerkrets")],
             [["Summan av gradtal = antal kanter", "Den är dubbelt så stor"], ["Glömmer att grafen måste vara sammanhängande", "Kontrollera det först"], ["Väljer den väg med färst kanter", "Summera avstånden"]],
             [("Vad är en Eulerväg?", "En väg som använder varje kant exakt en gång."), ("Var används grafteori?", "I nätverk, kartor, scheman och sociala medier."), ("Vad är ett träd?", "En sammanhängande graf utan cykler.")])


UNITS = {"differentialekvationer-av-forsta-ordningen": de1, "differentialekvationer-av-andra-ordningen": de2, "tillampningar-av-differentialekvationer": de_till, "mangdlara": mangd,
         "kombinatorik": kombinatorik, "talteori-och-kongruensrakning": kongruens, "talbaser": talbaser, "rekursiva-talfoljder": rekursion, "bevismetoder-och-induktion": bevis, "grafer-och-natverk": grafer}
