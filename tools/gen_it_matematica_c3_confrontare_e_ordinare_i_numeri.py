# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Confrontare e ordinare i numeri (Numeri)
  python3 tools/gen_it_matematica_c3_confrontare_e_ordinare_i_numeri.py
Simboli &lt; &gt; =, ordine crescente e decrescente, maggiore e minore, numeri tra due numeri, retta numerica,
arrotondare alla decina e al centinaio, problemi.
Errori: guardare solo le unità (409 &gt; 491), confondere &lt; e &gt;, ordine crescente scambiato con decrescente.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, retta, Kids, pl

R = random.Random(70302)
K = Kids(R)
LT, GT = "&lt;", "&gt;"


def pair_close():
    a = R.randint(101, 989)
    k = R.choice(["u", "d", "h", "swap"])
    if k == "u":
        b = a // 10 * 10 + R.randint(0, 9)
    elif k == "d":
        b = a // 100 * 100 + R.randint(0, 9) * 10 + a % 10
    elif k == "h":
        b = R.randint(1, 9) * 100 + a % 100
    else:
        s = str(a)
        b = int(s[0] + s[2] + s[1]) if s[1] != s[2] else int(s[1] + s[0] + s[2]) if s[1] != "0" else a + 1
    return a, b


def s1_simbolo():
    a, b = pair_close()
    if a == b and R.random() < 0.7:
        return None
    s = LT if a < b else GT if a > b else "="
    why = "le centinaia" if a // 100 != b // 100 else "le decine" if a // 10 != b // 10 else "le unità"
    e = "Confronta prima le centinaia, poi le decine, poi le unità. Qui decidono %s: %s <b>%s</b> %s." % (why, num(a), s, num(b)) if a != b else "I due numeri sono uguali: %s <b>=</b> %s." % (num(a), num(b))
    f = lambda x, o, y: "%s %s %s" % (num(x), o, num(y))
    if a == b:
        return None
    return mcq("Confronta %s e %s. Quale scrittura è vera?" % (num(a), num(b)), f(a, s, b), [f(a, o, b) for o in (LT, GT, "=") if o != s] + [f(b, s, a)], e)


def s1_vero():
    a, b = pair_close()
    if a == b:
        return None
    s = R.choice([LT, GT])
    ok = (a < b) == (s == LT)
    stmt = "%s %s %s" % (num(a), s, num(b))
    return mcq("La scrittura <b>%s</b> è vera o falsa?" % stmt, "vera" if ok else "falsa", ["falsa" if ok else "vera", "non si può dire", "è vera solo per le unità"],
               "%s è %s di %s, quindi la scrittura è <b>%s</b>." % (num(a), "minore" if a < b else "maggiore", num(b), "vera" if ok else "falsa"))


def s2_maggiore():
    base = R.randint(1, 8) * 100
    ns = set()
    while len(ns) < 4:
        x = base + R.choice([R.randint(0, 99), R.randint(100, 199)]) if R.random() < 0.7 else R.randint(101, 999)
        x = int(x)
        if 100 < x < 1000:
            ns.add(x)
    ns = sorted(ns)
    R.shuffle(ns)
    big = R.random() < 0.5
    t = max(ns) if big else min(ns)
    # errore: guardare solo le unità
    by_u = max(ns, key=lambda x: (x % 10, x)) if big else min(ns, key=lambda x: (x % 10, x))
    others = [x for x in ns if x != t]
    cands = ([by_u] if by_u != t else []) + others
    return mcq("Quale numero è il %s? %s" % ("maggiore" if big else "minore", ", ".join(num(x) for x in ns)), num(t), [num(x) for x in cands],
               "Confronta prima le centinaia, poi le decine. Il %s è <b>%s</b>." % ("maggiore" if big else "minore", num(t)))


def s2_ordine():
    ns = set()
    h = R.randint(1, 8)
    while len(ns) < 4:
        ns.add(R.choice([h, h + 1]) * 100 + R.randint(0, 99))
    ns = sorted(ns)
    cres = R.random() < 0.5
    ok = ns if cres else ns[::-1]
    w1 = ok[::-1]
    w2 = sorted(ns, key=lambda x: (x % 10, x))
    w3 = ok[:]
    w3[1], w3[2] = w3[2], w3[1]
    w4 = sorted(ns, key=lambda x: (x % 100, x))
    f = lambda L: ", ".join(num(x) for x in L)
    sh = ns[:]
    R.shuffle(sh)
    return mcq("Metti in ordine %s: %s" % ("crescente (dal più piccolo al più grande)" if cres else "decrescente (dal più grande al più piccolo)", f(sh)), f(ok),
               [f(x) for x in (w1, w2, w3, w4) if x != ok],
               "In ordine %s: <b>%s</b>." % ("crescente" if cres else "decrescente", f(ok)))


def s3_tra():
    a = R.randint(100, 900)
    b = a + R.choice([10, 20, 50, 100])
    if b > 999:
        return None
    ins = R.randint(a + 1, b - 1)
    outs = [a - R.randint(1, 9), b + R.randint(1, 9), a, b, b + 10 * R.randint(1, 5)]
    return mcq("Quale numero è compreso tra %s e %s?" % (num(a), num(b)), num(ins), [num(x) for x in outs if 0 < x < 1000],
               "%s &lt; <b>%s</b> &lt; %s." % (num(a), num(ins), num(b)))


def s3_retta():
    lo = R.randint(0, 9) * 100
    step = R.choice([10, 10, 5])
    hi = lo + (100 if step == 10 else 50)
    if hi > 1000:
        return None
    v = lo + step * R.randint(1, (hi - lo) // step - 1)
    i = (v - lo) // step
    return mcq(retta(lo, hi, step, [(v, "A")], [lo, hi]) + "Quale numero indica la freccia A?", num(v),
               [num(lo + i), num(v + step), num(v - step), num(lo + i * 10) if step == 5 else num(hi - i * step)],
               "Ogni tacca vale %d. Da %s conti %s: <b>%s</b>." % (step, num(lo), pl(i, "tacca", "tacche"), num(v)))


def s4_arrotonda():
    n = R.randint(101, 989)
    if R.random() < 0.5:
        if n % 10 == 0:
            return None
        if R.random() < 0.3:
            n = n // 10 * 10 + 5
        r = (n + 5) // 10 * 10
        return mcq("Arrotonda %s alla decina." % num(n), num(r), [num(n // 10 * 10) if r != n // 10 * 10 else num(r + 10), num((n + 50) // 100 * 100), num(r - 10 if r != n // 10 * 10 else r + 20), num(r + 10), num(r - 10), num(n)],
                   "La cifra delle unità è %d: %s. <b>%s</b>." % (n % 10, "arrotondi per eccesso (5 o più)" if n % 10 >= 5 else "arrotondi per difetto (meno di 5)", num(r)))
    if n % 100 == 0:
        return None
    if R.random() < 0.3:
        n = n // 100 * 100 + 50 + R.randint(0, 9)
    r = (n + 50) // 100 * 100
    return mcq("Arrotonda %s al centinaio." % num(n), num(r), [num(n // 100 * 100) if r != n // 100 * 100 else num(r + 100), num((n + 5) // 10 * 10), num(r + 100 if r == n // 100 * 100 else r - 200 if r >= 300 else r + 200), num(r + 100), num(r - 100) if r > 100 else None, num(n)],
               "La cifra delle decine è %d: %s. <b>%s</b>." % (n // 10 % 10, "arrotondi per eccesso (5 o più)" if n // 10 % 10 >= 5 else "arrotondi per difetto (meno di 5)", num(r)))


def s4_cifre():
    ds = R.sample(range(1, 10), 3)
    big = R.random() < 0.5
    t = sorted(ds, reverse=big)
    v = int("".join(map(str, t)))
    w = [int("".join(map(str, sorted(ds, reverse=not big)))), int("".join(map(str, ds))), int("%d%d%d" % (t[0], t[2], t[1])), int("%d%d%d" % (t[1], t[0], t[2]))]
    return mcq("Con le cifre %s (usandole una volta sola) qual è il numero %s che puoi formare?" % (", ".join(map(str, ds)), "più grande" if big else "più piccolo"), num(v),
               [num(x) for x in w if x != v],
               "Metti %s nelle centinaia: <b>%s</b>." % ("la cifra più grande" if big else "la cifra più piccola", num(v)))


def s5_problema():
    (p1, _), (p2, _) = K.two()
    k = R.choice(["figurine", "punti", "km", "libri", "altezza"])
    a, b = pair_close()
    if a == b:
        return None
    big = max(a, b)
    if k == "figurine":
        q = "%s ha %s figurine, %s ne ha %s. Chi ha più figurine?" % (p1, num(a), p2, num(b))
        ans = p1 if a > b else p2
        return mcq(q, ans, [p2 if ans == p1 else p1, "hanno lo stesso numero di figurine", "non si può sapere"],
                   "%s &gt; %s, quindi ne ha di più <b>%s</b>." % (num(big), num(min(a, b)), ans))
    if k == "punti":
        q = "In un gioco %s fa %s punti e %s fa %s punti. Vince chi fa più punti. Chi vince?" % (p1, num(a), p2, num(b))
        ans = p1 if a > b else p2
        return mcq(q, ans, [p2 if ans == p1 else p1, "pareggiano", "vince chi ha meno punti"],
                   "%s &gt; %s: vince <b>%s</b>." % (num(big), num(min(a, b)), ans))
    if k == "km":
        cs = R.sample(["Firenze", "Bologna", "Verona", "Genova", "Bari", "Torino", "Napoli"], 3)
        ds = R.sample(range(150, 990), 3)
        near = min(ds)
        return mcq("Da Roma, %s è a %s km, %s a %s km e %s a %s km. Quale città è più vicina?" % (cs[0], num(ds[0]), cs[1], num(ds[1]), cs[2], num(ds[2])),
                   cs[ds.index(near)], [c for c in cs if c != cs[ds.index(near)]] + ["sono tutte alla stessa distanza"],
                   "La distanza più piccola è %s km: la città più vicina è <b>%s</b>." % (num(near), cs[ds.index(near)]))
    if k == "libri":
        n = R.randint(3, 9) * 100 + R.randint(1, 99)
        r = (n + 50) // 100 * 100
        return mcq("La biblioteca della scuola ha %s libri. Circa quanti libri sono, arrotondando al centinaio?" % num(n), num(r),
                   [num(n // 100 * 100 + 100) if r == n // 100 * 100 else num(n // 100 * 100), num((n + 5) // 10 * 10), num(r + 100), num(r - 100) if r > 100 else None, num(n)],
                   "Le decine sono %d, quindi %s si arrotonda a <b>%s</b>." % (n // 10 % 10, num(n), num(r)))
    hs = R.sample(range(118, 142), 3)
    nm = [p1, p2, K.next()[0]]
    if len(set(nm)) < 3:
        return None
    hi = max(hs)
    return mcq("Le altezze di tre bambini sono: %s %d cm, %s %d cm, %s %d cm. Chi è il più alto?" % (nm[0], hs[0], nm[1], hs[1], nm[2], hs[2]),
               nm[hs.index(hi)], [x for x in nm if x != nm[hs.index(hi)]] + ["sono alti uguali"],
               "%d cm è il numero più grande: il più alto è <b>%s</b>." % (hi, nm[hs.index(hi)]))


def main():
    seen = set()
    sets = [
        ("Maggiore, minore, uguale", mix(R, seen, [(s1_simbolo, 14), (s1_vero, 6)])),
        ("Il più grande, il più piccolo e l’ordine", mix(R, seen, [(s2_maggiore, 10), (s2_ordine, 10)])),
        ("Sulla retta numerica", mix(R, seen, [(s3_tra, 8), (s3_retta, 12)])),
        ("Arrotondare e formare numeri", mix(R, seen, [(s4_arrotonda, 14), (s4_cifre, 6)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Per confrontare due numeri guarda prima le <b>centinaia</b>. Se sono uguali, guarda le decine, poi le unità.",
         "Il simbolo &lt; vuol dire «è minore di», il simbolo &gt; vuol dire «è maggiore di». La punta indica sempre il numero più piccolo.",
         "Ordine <b>crescente</b>: dal più piccolo al più grande. Ordine <b>decrescente</b>: dal più grande al più piccolo.",
         "Per arrotondare alla decina guarda le unità: da 5 in su arrotondi per eccesso, sotto 5 per difetto."],
        [("Confronta 409 e 491.", ["centinaia: 4 = 4", "decine: 0 &lt; 9"], "409 &lt; 491"),
         ("Arrotonda 368 al centinaio.", ["la cifra delle decine è 6, cioè 5 o più"], "400")],
        [["Guardare solo le unità: 409 &gt; 491", "Parti sempre dalle centinaia, cioè da sinistra."],
         ["Confondere &lt; e &gt;", "La punta del simbolo è rivolta verso il numero più piccolo."],
         ["Arrotondare 368 al centinaio come 370", "Al centinaio la risposta finisce con due zeri: 400."]])
    faq = [("Come ricordo il verso di < e >?", "La parte aperta del simbolo guarda il numero più grande, la punta guarda il più piccolo: 3 < 8."),
           ("A che cosa serve arrotondare?", "Serve a fare calcoli veloci e a controllare se un risultato è ragionevole.")]
    make_unit(R, "confrontare-e-ordinare-i-numeri", "N",
              "Confrontare e ordinare i numeri naturali, anche rappresentandoli sulla retta; usare i simboli <, > e =; arrotondare e stimare",
              "Confrontare e ordinare i numeri fino a 1000", "Confrontare e ordinare i numeri",
              "Schede di matematica per la classe terza su confronto e ordine dei numeri fino a 1000: simboli maggiore e minore, ordine crescente e decrescente, retta numerica, arrotondamenti e problemi. 100 esercizi con soluzioni.",
              "Per confrontare due numeri si parte dalle centinaia.", "La punta di < e > indica il numero più piccolo.",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
