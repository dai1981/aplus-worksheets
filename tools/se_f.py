# -*- coding: utf-8 -*-
"""
Sverige / Matematik / förskoleklass（Lgr22 kapitel 3, 6 år）。
python3 tools/se_f.py [nummer…]   seed は 96000 + nummer。
Problemfunktionerna kommer från se_l（årskurs 1–2）och begränsas med lim() till små tal.
"""
import random
import re
import sys
import se_m as S
import se_common as C
import se_a3a as A
import se_a3b as B
from se_m46 import group
import se_l

STD = "Naturliga tal och deras ordning, att räkna och jämföra antal, enkla mönster, lägesord, former, tid och mätning i vardagen (Lgr22, förskoleklassen)."


def U(slug, src, lv, lim, dom, title, short, meta, kb, ks, sets, think, ex, mist, faq):
    return dict(slug=slug, src=src, lv=lv, lim=lim, dom=dom, title=title, short=short, meta=meta, kb=kb, ks=ks, sets=sets, think=think, ex=ex, mist=mist, faq=faq)


UNITS = [
    U("rakna-till-20", "tal-till-20", 1, 20, "T", "Räkna till 20: antal och siffror", "Räkna till 20",
      "Uppgifter för förskoleklass: räkna föremål, siffror och tal på tallinjen upp till 20. 100 uppgifter med facit.",
      "Räkna en sak i taget", "Det sista talet du säger är antalet.",
      [("Hur många?", [("antal", 20)]), ("Räkna i rutan", [("ruta", 20)]), ("Talet med ord", [("ord_", 15), ("antal", 5)]), ("Tallinjen", [("linje", 15), ("ruta", 5)]), ("Blandat", [("antal", 10), ("ruta", 5), ("ord_", 5)])],
      ["Peka på en sak i taget och säg ett tal för varje sak.", "Det sista talet du säger är hur många det är.", "13 är en tia och tre ettor."],
      [("Fem bollar", ["1, 2, 3, 4, 5"], "5")],
      [["Räknar samma sak två gånger", "Peka och flytta fingret"], ["Hoppar över ett tal", "Säg talen i ordning"], ["Blandar ihop 12 och 21", "Titta på tiotalet först"]],
      [("Hur högt ska barn i förskoleklass räkna?", "Många räknar till 20 eller längre. Det viktiga är att förstå antal."), ("Hur kan jag öva hemma?", "Räkna trappsteg, äpplen eller bilar."), ("Vad är en tallinje?", "En linje där talen står i ordning.")]),
    U("talraden", "talraden-till-100", 1, 20, "T", "Talraden: före, efter och mellan", "Talraden",
      "Uppgifter för förskoleklass om talraden till 20: talet före och efter, tal som saknas och att räkna baklänges. 100 uppgifter med facit.",
      "Talet efter är ett mer", "Talet före är ett mindre.",
      [("Före och efter", [("tal-till-20:granne", 20)]), ("Vilket tal saknas?", [("saknas", 16), ("tal-till-20:granne", 4)]), ("Räkna baklänges", [("bak", 14), ("fortsatt", 5), ("tal-till-20:granne", 1)]), ("Tallinjen", [("tal-till-20:linje", 20)]), ("Blandat", [("tal-till-20:granne", 12), ("tal-till-20:ord_", 8)])],
      ["Talen kommer alltid i samma ordning: 1, 2, 3, 4, …", "Talet efter är ett mer. Talet före är ett mindre.", "Baklänges går talen nedåt: 10, 9, 8, …"],
      [("Vilket tal kommer efter 7?", ["7 och ett till"], "8")],
      [["Blandar ihop före och efter", "Före är mindre"], ["Hoppar över ett tal", "Räkna högt i ordning"], ["Tror att 0 inte är ett tal", "0 kommer före 1"]],
      [("Varför är talraden viktig?", "Den är grunden för att räkna och jämföra."), ("Hur övar man baklänges?", "Räkna ner som vid en raketuppskjutning."), ("Vad är ett grannetal?", "Talet direkt före eller efter.")]),
    U("jamfora-antal", "jamfora-tal", 1, 10, "T", "Jämföra antal: flest, färst och störst", "Jämföra antal",
      "Uppgifter för förskoleklass om att jämföra antal: flest och färst, ordna tal, skillnad och största talet upp till 10. 100 uppgifter med facit.",
      "Flest = det största antalet", "Lika många: varje sak får en kompis.",
      [("Var finns flest?", [("flest", 20)]), ("Vilket tal är störst?", [("storst", 15), ("flest", 5)]), ("Ordna talen", [("ordna", 20)]), ("Hur många fler?", [("skillnad", 15), ("flest", 5)]), ("Blandat", [("flest", 8), ("ordna", 8), ("storst", 4)])],
      ["Räkna båda grupperna och jämför talen.", "Gruppen med det största talet har flest. Gruppen med det minsta talet har färst.", "Du kan också para ihop sakerna: den grupp där det blir saker över har fler."],
      [("4 äpplen och 6 päron", ["6 är mer än 4"], "Päronen är flest")],
      [["Tittar på hur stora sakerna är", "Räkna antalet"], ["Blandar ihop fler och färre", "Fler är mer"], ["Glömmer att räkna båda", "Räkna varje grupp"]],
      [("Hur övar man jämförelse?", "Lägg ut saker i två rader och se vilken som räcker längst."), ("Vad betyder lika många?", "Att båda grupperna har samma antal."), ("Måste barnen kunna tecknen &lt; och &gt;?", "Inte i förskoleklass, men orden fler och färre är viktiga.")]),
    U("talkamrater-till-10", "talkamrater", 1, 10, "T", "Talkamrater till 10: dela upp tal", "Talkamrater till 10",
      "Uppgifter för förskoleklass om talkamrater: tiokamrater, dela upp tal och vilket tal som saknas. 100 uppgifter med facit.",
      "7 och 3 är tiokamrater", "Ett tal kan delas upp på olika sätt.",
      [("Tiokamrater", [("tio", 20)]), ("Dela upp talet", [("bond", 20)]), ("Vilket tal saknas?", [("saknas", 20)]), ("Olika sätt", [("dela", 20)]), ("Blandat", [("tio", 7), ("bond", 7), ("dela", 6)])],
      ["Två tal som tillsammans blir 10 kallas tiokamrater: 1 och 9, 2 och 8, 3 och 7, 4 och 6, 5 och 5.", "Ett tal kan delas upp i två delar: 6 är 4 och 2, eller 5 och 1.", "Använd fingrarna: tio fingrar är två händer."],
      [("6 och ? blir 10", ["Räkna från 6 till 10"], "4")],
      [["Räknar med 6 en gång till", "Börja räkna efter 6"], ["Tror att det bara finns ett sätt", "Det finns många sätt"], ["Blandar ihop delarna", "Delarna ska bli hela talet"]],
      [("Varför tiokamrater?", "De hjälper när man räknar över tiotalet senare."), ("Hur övar man?", "Gömma några av tio föremål och fråga hur många som är gömda."), ("Vad är en del-helhet-bild?", "En bild där helheten delas i två delar.")]),
    U("lagga-till", "addition-till-10", 1, 10, "T", "Lägga till: addition upp till 10", "Lägga till",
      "Uppgifter för förskoleklass om att lägga till: räkna bilder, plus på tallinjen och små berättelser upp till 10. 100 uppgifter med facit.",
      "Plus betyder att det blir fler", "Räkna vidare från det första talet.",
      [("Räkna bilderna", [("bild", 20)]), ("Plus med tal", [("tal", 20)]), ("Tallinjen", [("linje", 20)]), ("Berättelser", [("text_", 20)]), ("Tärningar", [("tarning", 14), ("bild", 6)])],
      ["När man lägger till blir det fler. 3 + 2 betyder 3 och 2 till.", "Börja på det första talet och räkna vidare: 3, sedan 4, 5.", "Ordningen spelar ingen roll: 2 + 3 blir samma som 3 + 2."],
      [("3 bilar och 2 bilar till", ["3, 4, 5"], "5")],
      [["Börjar räkna från 1 varje gång", "Räkna vidare från det första talet"], ["Räknar det första talet två gånger", "Börja på talet efter"], ["Blandar ihop plus och minus", "Plus blir fler"]],
      [("Hur introducerar man plus?", "Med saker som man lägger ihop, till exempel klossar."), ("Vad är en tallinje?", "En linje där man hoppar framåt när man lägger till."), ("Måste barnen skriva tecknet +?", "Det kommer efter hand.")]),
    U("ta-bort", "subtraktion-till-10", 1, 10, "T", "Ta bort: subtraktion upp till 10", "Ta bort",
      "Uppgifter för förskoleklass om att ta bort: överkryssade bilder, minus på tallinjen och små berättelser upp till 10. 100 uppgifter med facit.",
      "Minus betyder att det blir färre", "Räkna det som är kvar.",
      [("Kryssa och räkna", [("bild", 20)]), ("Minus med tal", [("tal", 20)]), ("Tallinjen", [("linje", 20)]), ("Berättelser", [("text_", 20)]), ("Vilket tal saknas?", [("saknas", 20)])],
      ["När man tar bort blir det färre. 7 − 2 betyder 7 och 2 tas bort.", "Räkna det som är kvar, eller räkna bakåt: 7, sedan 6, 5.", "Om man tar bort allt blir det 0 kvar."],
      [("6 fåglar, 2 flyger bort", ["6, 5, 4"], "4")],
      [["Räknar också de bortkryssade", "Räkna bara det som är kvar"], ["Räknar uppåt i stället för nedåt", "Minus går bakåt"], ["Tror att man inte kan få 0", "0 betyder att inget är kvar"]],
      [("Hur introducerar man minus?", "Med saker som man tar bort, till exempel kakor som äts upp."), ("Vad betyder kvar?", "Det som finns efter att något tagits bort."), ("Varför använda tallinjen?", "Den visar att minus är att hoppa bakåt.")]),
    U("dubbelt-och-dela-lika", "dubbelt-och-halften", 1, 10, "T", "Dubbelt, hälften och dela lika", "Dubbelt och dela lika",
      "Uppgifter för förskoleklass om dubbelt och hälften och om att dela lika mellan kompisar, upp till 10. 100 uppgifter med facit.",
      "Dubbelt: lika många till", "Dela lika: alla får lika många.",
      [("Dubbelt", [("dub", 20)]), ("Hälften", [("halv", 20)]), ("Dela lika", [("delning:dela", 20)]), ("Dela bilderna", [("delning:bild", 20)]), ("Blandat", [("dub", 7), ("halv", 7), ("delning:dela", 6)])],
      ["Dubbelt betyder lika många en gång till: dubbelt så många som 3 är 6.", "Hälften betyder att man delar i två lika stora delar: hälften av 8 är 4.", "När man delar lika får alla lika många. Dela ut en i taget."],
      [("8 kakor delas lika av 2 barn", ["En till var tills det är slut"], "4 var")],
      [["Dubbelt av 4 = 5", "Dubbelt av 4 är 4 + 4 = 8"], ["Delar olika mycket", "Alla ska få lika många"], ["Hälften av 6 = 2", "Dela i två lika delar: 3"]],
      [("Varför dubbelt?", "Dubblor är lätta att komma ihåg och hjälper vid huvudräkning."), ("Hur övar man att dela lika?", "Dela ut godis eller kort ett i taget."), ("Vad händer om det inte går jämnt ut?", "Då blir det någon över.")]),
    U("monster", "monster", 1, 20, "A", "Mönster: fortsätt och hitta regeln", "Mönster",
      "Uppgifter för förskoleklass om mönster: fortsätt figurmönster, fyll luckor och hitta regeln i enkla talmönster. 100 uppgifter med facit.",
      "Ett mönster upprepas", "Hitta delen som kommer igen.",
      [("Fortsätt mönstret", [("figur", 20)]), ("Vad saknas?", [("lucka", 20)]), ("Talmönster", [("tal", 15), ("regel", 5)]), ("Hitta regeln", [("regel", 10), ("bak", 10)]), ("Blandat", [("figur", 10), ("lucka", 10)])],
      ["I ett mönster upprepas något hela tiden, till exempel röd, blå, röd, blå.", "Hitta den del som kommer igen. Säg mönstret högt.", "Talmönster kan växa: 2, 4, 6, 8. Varje gång blir det 2 till."],
      [("röd, blå, röd, blå, …", ["röd, blå upprepas"], "röd")],
      [["Tittar bara på den sista figuren", "Titta på hela mönstret"], ["Tror att mönstret byter", "Samma del upprepas"], ["Räknar fel i talmönster", "Kontrollera mellan varje tal"]],
      [("Varför mönster?", "Mönster tränar logiskt tänkande och är en början till algebra."), ("Var finns mönster?", "På tyger, i musik och i naturen."), ("Hur övar man?", "Gör pärlhalsband eller klappa rytmer.")]),
    U("former", "geometriska-figurer", 1, 99, "G", "Former: cirkel, triangel, kvadrat och rektangel", "Former",
      "Uppgifter för förskoleklass om former: namnge cirkel, triangel, kvadrat och rektangel, räkna former och hörn och hitta former i vardagen. 100 uppgifter med facit.",
      "En triangel har tre hörn", "En kvadrat har fyra lika långa sidor.",
      [("Vad heter formen?", [("namn", 20)]), ("Räkna formerna", [("rakna", 20)]), ("Hörn och sidor", [("horn", 8), ("namn", 12)]), ("Former i vardagen", [("saker", 12), ("rakna", 8)]), ("Blandat", [("namn", 10), ("rakna", 10)])],
      ["En cirkel är rund och har inga hörn. En triangel har tre hörn och tre sidor.", "En kvadrat har fyra hörn och fyra lika långa sidor. En rektangel har fyra hörn och två par lika långa sidor.", "Titta efter former omkring dig: en klocka är en cirkel och en dörr är en rektangel."],
      [("Hur många hörn har en triangel?", ["Räkna spetsarna"], "3")],
      [["Kallar en kvadrat för en triangel", "Räkna hörnen"], ["Tror att en vänd kvadrat är en annan form", "Formen är densamma"], ["Glömmer att en kvadrat också är en rektangel", "Alla sidor lika långa: kvadrat"]],
      [("Vilka former ska barnen kunna?", "Cirkel, triangel, kvadrat och rektangel är vanliga i förskoleklass."), ("Vad är ett hörn?", "Där två sidor möts."), ("Hur övar man?", "Leta former i rummet eller bygg med klossar.")]),
    U("lagesord", "lagesord", 1, 99, "G", "Lägesord: på, under, bredvid, framför och bakom", "Lägesord",
      "Uppgifter för förskoleklass om lägesord: på, under och bredvid, framför och bakom, överst och nederst samt vänster och höger. 100 uppgifter med facit.",
      "Lägesord säger var något är", "Höger är handen du ofta skriver med.",
      [("På, under och bredvid", [("bord", 20)]), ("Framför och bakom", [("lada", 20)]), ("Överst och nederst", [("hylla", 20)]), ("Vänster och höger", [("rad", 20)]), ("Blandat", [("bord", 7), ("hylla", 7), ("rad", 6)])],
      ["Lägesord berättar var något finns: på, under, bredvid, framför, bakom, mellan.", "Överst är högst upp och nederst är längst ner.", "Vänster och höger beror på hur man står. Titta på bilden som om du stod framför den."],
      [("Var är katten?", ["Katten ligger under bordet"], "under")],
      [["Blandar ihop vänster och höger", "Gör L med vänster hand"], ["Blandar ihop framför och bakom", "Framför syns först"], ["Glömmer mellan", "Mellan är mitt emellan två saker"]],
      [("Varför lägesord?", "De behövs för att beskriva var saker finns och för att följa instruktioner."), ("Hur övar man?", "Gömma saker och beskriva var de är."), ("Är vänster och höger svårt?", "Ja, det tar tid. Öva med kroppen.")]),
    U("langd-och-vikt", "langd-och-vikt", 1, 99, "G", "Längd och vikt: längst, kortast och tyngst", "Längd och vikt",
      "Uppgifter för förskoleklass om att jämföra längd och vikt: längst och kortast, högst, mäta med klossar och tyngst och lättast. 100 uppgifter med facit.",
      "Jämför från samma startlinje", "Mät med lika stora delar.",
      [("Längst och kortast", [("penna", 20)]), ("Högst och lägst", [("torn", 20)]), ("Mät med klossar", [("matt", 10), ("vag", 10)]), ("Tyngst och lättast", [("vag", 20)]), ("Blandat", [("penna", 6), ("torn", 6), ("ord_", 8)])],
      ["Lägg sakerna bredvid varandra från samma startlinje. Den som räcker längst är längst.", "Man kan mäta med klossar, gem eller fötter. Räkna hur många som får plats.", "På en balansvåg sjunker den tyngsta sidan nedåt."],
      [("En penna är 5 klossar och en annan 7 klossar", ["7 är mer än 5"], "Den andra är längst")],
      [["Jämför utan samma startlinje", "Börja på samma ställe"], ["Mäter med olika stora delar", "Använd lika stora delar"], ["Tror att den största saken alltid är tyngst", "Titta på vågen"]],
      [("Varför mäta med klossar?", "Det visar idén med en måttenhet innan man lär sig centimeter."), ("Vad är en balansvåg?", "En våg där den tyngre sidan sjunker."), ("Hur övar man hemma?", "Jämför längden på leksaker eller väg frukt i händerna.")]),
    U("pengar", "pengar", 1, 20, "T", "Pengar: mynt och att handla för små belopp", "Pengar",
      "Uppgifter för förskoleklass om pengar: känna igen mynt, räkna kronor, köpa saker och räcker pengarna, upp till 20 kronor. 100 uppgifter med facit.",
      "Räkna kronorna", "Ett femkronorsmynt är värt 5 kronor.",
      [("Mynten", [("mynt", 20)]), ("Hur mycket pengar?", [("rakna", 20)]), ("Köpa", [("kopa", 20)]), ("Räcker pengarna?", [("racker", 20)]), ("Blandat", [("rakna", 10), ("kopa", 10)])],
      ["I Sverige finns mynt på 1, 2, 5 och 10 kronor.", "Räkna mynten: ett femkronorsmynt och två enkronorsmynt är 7 kronor.", "Om du har fler kronor än något kostar räcker pengarna."],
      [("Ett 5-kronorsmynt och två 1-kronorsmynt", ["5, 6, 7"], "7 kr")],
      [["Räknar antalet mynt", "Räkna värdet"], ["Tror att ett stort mynt alltid är mest värt", "Titta på siffran"], ["Glömmer att lägga ihop", "Lägg ihop alla mynt"]],
      [("Vilka mynt finns i Sverige?", "1, 2, 5 och 10 kronor."), ("Varför öva med pengar?", "Det tränar att räkna och lägga ihop i vardagen."), ("Hur övar man?", "Leka affär med riktiga eller låtsasmynt.")]),
    U("klockan-och-tid", "klockan", 1, 12, "G", "Klockan och tid: hel timme, halv och dygnet", "Klockan och tid",
      "Uppgifter för förskoleklass om klockan: hela timmar och halvtimmar, visarna, digital tid, senare och tider på dygnet. 100 uppgifter med facit.",
      "Den korta visaren visar timmen", "Halv tre = 2.30.",
      [("Hel timme", [("las", 20)]), ("Visarna", [("visare", 20)]), ("Digital tid", [("digital", 12), ("las", 4), ("dygn", 4)]), ("Senare", [("senare", 20)]), ("Blandat", [("senare", 15), ("visare", 4), ("dygn", 1)])],
      ["Klockan har en kort visare som visar timmen och en lång som visar minuterna.", "När den långa visaren pekar rakt upp är det hel timme. När den pekar rakt ner är det halv.", "Halv tre betyder en halvtimme innan klockan tre, alltså 2.30."],
      [("Kort visare på 4, lång på 12", ["Hel timme"], "Klockan är fyra")],
      [["Blandar ihop visarna", "Den korta visar timmen"], ["Halv tre = 3.30", "Halv tre = 2.30"], ["Glömmer att dygnet har natt", "Ett dygn är dag och natt"]],
      [("När lär sig barn klockan?", "Många börjar med hela och halva timmar i förskoleklass."), ("Vad är ett dygn?", "24 timmar, en dag och en natt."), ("Hur övar man?", "Prata om tider: vi äter klockan tolv.")]),
    U("sortera-och-rakna", "tabeller-och-diagram", 1, 10, "S", "Sortera och räkna: bilddiagram och streck", "Sortera och räkna",
      "Uppgifter för förskoleklass om att sortera och räkna: bilddiagram, stapeldiagram, mest och minst och streckräkning. 100 uppgifter med facit.",
      "Sortera först, räkna sedan", "Den högsta stapeln är flest.",
      [("Bilddiagram", [("bild", 20)]), ("Läs av diagrammet", [("las", 20)]), ("Mest och minst", [("mest", 20)]), ("Hur många fler?", [("skillnad", 20)]), ("Blandat", [("bild", 10), ("mest", 5), ("streck_", 5)])],
      ["Sortera sakerna i grupper, till exempel efter färg eller sort.", "I ett bilddiagram står varje bild för en sak. Räkna bilderna i varje rad.", "Ett streck i taget: fyra streck och ett snett streck är fem."],
      [("3 katter, 5 hundar, 2 fiskar", ["5 är störst"], "Hundar är flest")],
      [["Räknar fel rad", "Följ raden med fingret"], ["Blandar ihop mest och minst", "Mest är flest"], ["Tror att den längsta bilden är flest", "Räkna bilderna"]],
      [("Varför diagram?", "De visar snabbt vilken grupp som är störst."), ("Vad är streckräkning?", "Att göra ett streck för varje sak man räknar."), ("Hur övar man?", "Räkna favoritfrukter i klassen och rita ett diagram.")]),
]


def get(src, lv, name, cache):
    if ":" in name:
        src, name = name.split(":")
        lv = 2 if src == "delning" else lv
    key = (src, lv)
    if key not in cache:
        cache[key] = se_l.UNITS[src](lv)
    for _, parts in cache[key]["sets"]:
        for mk, _n in parts:
            if mk.__name__ == name:
                return mk
    raise KeyError((src, name))


def build(i):
    u = UNITS[i - 1]
    rnd = random.Random(96000 + i)
    S.setup(rnd)
    A.setup(rnd)
    B.setup(rnd)
    cache = {}
    seen = set()
    sets = []
    for t, parts in u["sets"]:
        ps = []
        for name, n in parts:
            if n:
                ps.append((se_l.lim(get(u["src"], u["lv"], name, cache), u["lim"]), n))
        try:
            items = C.mix(rnd, seen, ps)
        except AssertionError as e:
            raise AssertionError("%s / %s: %s" % (u["slug"], t, e))
        for it in items:
            it["q"] = re.sub(r"<div class='qfig'><div class='qfig'>(.*?)</div></div>", r"<div class='qfig'>\1</div>", it["q"], flags=re.S)
            it["q"] = group(it["q"])
            it["e"] = group(it["e"])
            it["c"] = [group(c) for c in it["c"]]
        sets.append((t, items))
    body = C.lesson(u["think"], [C.example(q, s, a) for q, s, a in u["ex"]], u["mist"])
    faq = [{"q": q, "a": a} for q, a in u["faq"]]
    C.make_unit(rnd, u["slug"], u["dom"], STD, u["title"], u["short"], u["meta"], u["kb"], u["ks"], body, faq, sets, i, "forskoleklass")
    return u["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    for i in range(1, len(UNITS) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(i), flush=True)
