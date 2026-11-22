<?php
/* Topic hubs: /worksheets/{country}/{subject}/topics/{topic}/
   One page per topic that collects every skill on that topic, from the lowest grade to the highest.
   Units join a topic when their slug matches 'in' and does not match 'out'.
   Nothing here is stored in the database: the list is built from ws_unit on each request. */

/* Taiwan (zh-TW): its own topic set, because its slugs and grade span (國小一年級 to 國中九年級) differ */
function topic_defs_tw() {
    return array(
        'whole-numbers' => array('name' => '大數與位值', 'in' => '/numbers-to|place-value|^number-line$|comparing-and-number/', 'out' => '/^$/',
            'blurb' => '從 100 以內的數到億，認識位值、數的順序和大小比較，並在數線上找出數的位置。'),
        'addition-and-subtraction' => array('name' => '加法與減法', 'in' => '/add|subtract|column-/', 'out' => '/fraction|decimal|integer|polynom/',
            'blurb' => '從加法和減法的意義、基本加減，到直式進位、退位和一萬以內的加減。'),
        'multiplication' => array('name' => '乘法', 'in' => '/multipl/', 'out' => '/fraction|decimal|integer|polynom|formulas|factors/',
            'blurb' => '從幾個幾、九九乘法表，到一位數乘法和多位數的直式乘法。'),
        'division' => array('name' => '除法', 'in' => '/divi|sharing/', 'out' => '/fraction|decimal|integer|polynom/',
            'blurb' => '從分裝與平分，到除法的意義、有餘數的除法和多位數的直式除法。'),
        'word-problems' => array('name' => '應用問題', 'in' => '/word-problems|two-step|three-step|multi-step|classic|quantity-relationships/', 'out' => '/^$/',
            'blurb' => '加減乘除的應用問題、兩步驟與多步驟問題，以及植樹、年齡、雞兔同籠等經典題型。'),
        'fractions' => array('name' => '分數', 'in' => '/fraction/', 'out' => '/^$/',
            'blurb' => '從單位分數、等值分數、約分與擴分，到分數的加減乘除和應用問題。'),
        'decimals' => array('name' => '小數', 'in' => '/decimal/', 'out' => '/^$/',
            'blurb' => '一位小數、二位小數、小數的大小比較，以及小數的加減乘除和取概數。'),
        'ratios-and-percentages' => array('name' => '比、百分率與速率', 'in' => '/(^|-)ratios?(-|$)|proportion(-|$)|percent|base-and-compared|speed/', 'out' => '/^$/',
            'blurb' => '比與比值、百分率、基準量與比較量、速率，以及正比、反比和連比。'),
        'estimation' => array('name' => '概數與估算', 'in' => '/round|estimat|approximat/', 'out' => '/^$/',
            'blurb' => '四捨五入、無條件進入與無條件捨去，用估算檢查答案，以及平方根的近似值。'),
        'order-of-operations' => array('name' => '四則運算與計算規律', 'in' => '/order-of-operations|calculation-rules|mixed-operations|laws-of-operations|distributive/', 'out' => '/^$/',
            'blurb' => '先乘除後加減、括號，以及交換律、結合律、分配律，讓計算更簡便。'),
        'factors-and-multiples' => array('name' => '因數與倍數', 'in' => '/factors-and|prime|gcf|standard-factorization/', 'out' => '/^$/',
            'blurb' => '因數、倍數、質數，最大公因數與最小公倍數，以及質因數分解。'),
        'integers' => array('name' => '正數與負數', 'in' => '/integer|positive-and-negative|absolute/', 'out' => '/^$/',
            'blurb' => '負數的意義、數線與絕對值，以及正負數的加減乘除。'),
        'exponents-and-roots' => array('name' => '指數與平方根', 'in' => '/exponent|square-root|scientific|radical/', 'out' => '/^$/',
            'blurb' => '指數與指數律、科學記號、平方根，以及根式的化簡與運算。'),
        'algebra' => array('name' => '代數式與多項式', 'in' => '/algebraic|polynomial|multiplication-formulas|factoring|cross-method|formulas/', 'out' => '/^$/',
            'blurb' => '用符號代表數、代數式的化簡、乘法公式、多項式的運算和因式分解。'),
        'equations' => array('name' => '方程式與不等式', 'in' => '/equation|inequalit|solving|systems|number-sentences|quadratic-formula/', 'out' => '/^$/',
            'blurb' => '算式填空、一元一次方程式、二元一次聯立方程式、一元二次方程式和一元一次不等式。'),
        'functions-and-graphs' => array('name' => '坐標與函數', 'in' => '/coordinate|function|graphs-of|maximum-and-minimum|distance-formula/', 'out' => '/^$/',
            'blurb' => '坐標平面、兩點距離、一次函數和二次函數的圖形，以及最大值與最小值。'),
        'patterns-and-sequences' => array('name' => '規律與數列', 'in' => '/pattern|sequence|series/', 'out' => '/^$/',
            'blurb' => '找出圖形和數的規律、等差數列、等差級數和等比數列。'),
        'time' => array('name' => '時間', 'in' => '/(^|-)time(-|$)|dates|years-months/', 'out' => '/^$/',
            'blurb' => '認識時鐘、幾時幾分、年月日、時間的換算和計算。'),
        'measurement' => array('name' => '長度、重量與容量', 'in' => '/comparing-length|meters$|millimeters|kilometers|kilograms|liters|metric-tons|capacity/', 'out' => '/area-square|arc-length/',
            'blurb' => '比長短、公分與公尺、毫米與公里、公斤與公克、公升與毫升，以及單位換算。'),
        'area-and-perimeter' => array('name' => '面積與周長', 'in' => '/area|perimeter|circumference/', 'out' => '/surface|sector|volume|capacity/',
            'blurb' => '周長、面積單位，長方形、三角形、平行四邊形和梯形的面積，以及圓周長和圓面積。'),
        'volume' => array('name' => '體積與表面積', 'in' => '/volume|surface-area/', 'out' => '/^$/',
            'blurb' => '體積單位、長方體與正方體的體積、柱體的體積，以及表面積。'),
        'angles' => array('name' => '角度', 'in' => '/(^|-)angles?(-|$)/', 'out' => '/triangle/',
            'blurb' => '認識角、用量角器量角、旋轉角、多邊形的內角和，以及圓周角。'),
        'shapes' => array('name' => '平面圖形', 'in' => '/shapes$|^triangles$|quadrilateral|parallelogram|squares-and-rectangles|^circles$|congruent-figures|perpendicular|line-symmetry/', 'out' => '/area|faces/',
            'blurb' => '三角形、四邊形和圓的性質，垂直與平行、全等圖形和線對稱。'),
        'solids' => array('name' => '立體圖形', 'in' => '/solids|nets|three-views|faces|lines-and-planes/', 'out' => '/^$/',
            'blurb' => '正方體、長方體、角柱與圓柱，展開圖、三視圖，以及空間中的線與面。'),
        'circles' => array('name' => '圓', 'in' => '/circle|circum|sector|arc-length|inscribed|incenter|centroid/', 'out' => '/^$/',
            'blurb' => '圓的構成、圓周長與圓面積、扇形與弧長，以及圓周角和三角形的三心。'),
        'geometry' => array('name' => '三角形與幾何證明', 'in' => '/triangle|pythagorean|parallel-lines|proportional-segments|similar|proofs|polygon-angle/', 'out' => '/area|quadrilateral-properties|^triangles$/',
            'blurb' => '三角形的性質、全等與相似、畢氏定理、平行線與截角，以及幾何證明。'),
        'transformations' => array('name' => '旋轉、對稱與縮放', 'in' => '/rotation|enlargement|map-scales|similar-figures|line-symmetry/', 'out' => '/^$/',
            'blurb' => '旋轉、線對稱、放大與縮小、比例尺和相似形。'),
        'statistics' => array('name' => '統計圖表', 'in' => '/graph|chart|^tables$|sorting|statistical|mean-median|box-plots|cumulative|averages/', 'out' => '/graphs-of/',
            'blurb' => '分類整理、統計表、長條圖、折線圖、圓形圖、平均數、中位數、眾數和盒狀圖。'),
        'probability' => array('name' => '機率與可能性', 'in' => '/probab|likelihood|^counting$/', 'out' => '/^$/',
            'blurb' => '可能性的大小、樹狀圖與數數，以及機率的計算。'),
    );
}

/* Germany (de): German topic names and German unit slugs */
function topic_defs_de() {
    return array(
        'zahlen-und-stellenwerte' => array('name' => 'Zahlen und Stellenwerte',
            'in' => '/^zahlen-(bis|vergleichen)|stellenwert|runden|zahlenraum|zahlen-ordnen|negative|potenz|rational|wurzel|logarithm/', 'out' => '/potenzfunktion/',
            'blurb' => 'Zahlen lesen und schreiben, Hunderter, Zehner und Einer, Zahlen vergleichen und ordnen, der Zahlenstrahl und das Runden. Dazu negative und rationale Zahlen, Potenzen und Potenzgesetze, Zehnerpotenzen, Quadratwurzeln, Wurzelgesetze, reelle Zahlen und Logarithmen.'),
        'plus-und-minus' => array('name' => 'Addition und Subtraktion',
            'in' => '/plus|minus|addition|subtraktion|addieren|subtrahieren|ergaenzen|verdoppeln/', 'out' => '/^$/',
            'blurb' => 'Kopfrechnen, halbschriftliches Rechnen und die schriftlichen Verfahren mit Übertrag und Entbündeln.'),
        'mal-und-geteilt' => array('name' => 'Multiplikation und Division',
            'in' => '/einmaleins|multipli|dividier|division|mal-und|geteilt|teiler|primzahl/', 'out' => '/ausmultipl/',
            'blurb' => 'Das kleine Einmaleins, Geteiltaufgaben, Rechnen mit Zehnerzahlen, halbschriftliches und schriftliches Multiplizieren und Dividieren, das Teilen mit Rest sowie Teiler, Vielfache und Primzahlen.'),
        'brueche-und-dezimalzahlen' => array('name' => 'Brüche, Dezimalzahlen und Prozente',
            'in' => '/brueche|dezimal|prozent|gemischte-zahlen|zins/', 'out' => '/^$/',
            'blurb' => 'Brüche als Anteile, erweitern und kürzen, vergleichen und mit Brüchen rechnen, Dezimalzahlen und periodische Dezimalzahlen, das Rechnen mit dem Komma, Prozentrechnung, prozentuale Veränderung und Zinsrechnung.'),
        'groessen' => array('name' => 'Größen und Messen',
            'in' => '/geld|laengen|gewicht|uhrzeit|zeitspannen|zeit-und|kalender|hohlmasse|liter|rauminhalt|massstab|volumen/', 'out' => '/^$/',
            'blurb' => 'Mit Euro und Cent, Millimetern bis Kilometern, Gramm bis Tonnen, Litern und Millilitern sowie Uhrzeiten, Zeitspannen und dem Kalender rechnen, umwandeln und schätzen. Dazu Kommaschreibweise und Maßstab.'),
        'sachaufgaben' => array('name' => 'Sachaufgaben',
            'in' => '/sachaufgaben|sachrechnen/', 'out' => '/^$/',
            'blurb' => 'Sachaufgaben mit einem und mehreren Rechenschritten: Frage, Rechnung, Antwort.'),
        'geometrie' => array('name' => 'Geometrie',
            'in' => '/koerper|figuren|symmetrie|flaeche|umfang|geometrie|wuerfel|parallel|senkrecht|vierecke|lage-und|strecken|koordinaten|winkel|kreis|dreieck|prism|kongruenz|thales|zylinder|pythagoras|aehnlich|strahlen|trigonometr|pyramide|kegel|kugel|bogenmass|einheitskreis|sinussatz/', 'out' => '/^$/',
            'blurb' => 'Formen und Körper, Lage und Richtung, Würfelnetze, Ansichten und Baupläne, Strecken und Geraden, parallel und senkrecht, Vierecke, Winkel, das Koordinatensystem, Achsen- und Punktsymmetrie, Dreiecke konstruieren, Kongruenzsätze, Satz des Thales, Umfang, Flächeninhalt, Kreis, Prismen, Zylinder und Volumen. Dazu der Satz des Pythagoras, Ähnlichkeit und Strahlensätze, Trigonometrie im rechtwinkligen Dreieck und am Einheitskreis, Sinus- und Kosinussatz, Bogenmaß und Kreisausschnitt sowie Pyramide, Kegel und Kugel.'),
        'muster-und-strukturen' => array('name' => 'Muster und Strukturen',
            'in' => '/muster|zahlenfolgen|zahlenmauer|rechengesetze|zuordnung|gleichung|terme|ausmultipl|binomisch/', 'out' => '/^$/',
            'blurb' => 'Zahlenfolgen und Regeln, Zahlenmauern und wachsende Muster erkennen, beschreiben und fortsetzen, Rechengesetze und Klammern nutzen, Terme umformen, Ausmultiplizieren, binomische Formeln, Bruchterme, lineare Gleichungen, proportionale und antiproportionale Zuordnungen und Dreisatz.'),
        'lineare-funktionen-und-gleichungssysteme' => array('name' => 'Lineare Funktionen und Gleichungssysteme',
            'in' => '/funktion|geradengleichung|gleichungssystem/', 'out' => '/quadratisch|exponential|potenzfunktion|polynom|sinus/',
            'blurb' => 'Lineare Funktionen mit Steigung und y-Achsenabschnitt, Geradengleichungen aufstellen und lineare Gleichungssysteme grafisch, rechnerisch und in Sachaufgaben lösen.'),
        'quadratische-funktionen-und-gleichungen' => array('name' => 'Quadratische Funktionen und Gleichungen',
            'in' => '/quadratisch|scheitelpunkt/', 'out' => '/^$/',
            'blurb' => 'Parabeln, Scheitelpunktform und Normalform, quadratische Ergänzung, quadratische Gleichungen mit p-q- und abc-Formel und Sachaufgaben mit Parabeln.'),
        'exponential-potenz-und-winkelfunktionen' => array('name' => 'Exponential-, Potenz- und Winkelfunktionen',
            'in' => '/exponential|exponentiell|potenzfunktion|polynomfunktion|sinus-und-kosinusfunktion/', 'out' => '/^$/',
            'blurb' => 'Exponentialfunktionen, exponentielles Wachstum und Zerfall mit Zinseszins und Halbwertszeit, Potenzfunktionen und Hyperbeln, Polynomfunktionen mit Nullstellen und Symmetrie sowie die Sinus- und Kosinusfunktion mit Amplitude und Periode.'),
        'daten-und-zufall' => array('name' => 'Daten und Zufall',
            'in' => '/diagramm|tabellen|daten|wahrscheinlich|zufall|kombinatorik|boxplot|vierfelder|erwartungswert/', 'out' => '/^$/',
            'blurb' => 'Strichlisten, Tabellen, Säulen- und Liniendiagramme lesen und auswerten, Kennwerte und Boxplots, Kombinationen zählen, Wahrscheinlichkeiten, mehrstufige Baumdiagramme, Pfad- und Summenregel, Vierfeldertafeln, bedingte Wahrscheinlichkeit und der Erwartungswert.'),
    );
}

/* France: French unit slugs, French names */
function topic_defs_fr() {
    return array(
        'nombres' => array('name' => 'Nombres et numération',
            'in' => '/nombres|numeration|ranger|comparer-les|compter|valeur-absolue/', 'out' => '/fraction|decima/',
            'blurb' => 'Lire, écrire et décomposer les nombres, les unités de numération, comparer et ranger, placer des nombres sur une droite graduée.'),
        'addition-et-soustraction' => array('name' => 'Addition et soustraction',
            'in' => '/addition|soustraction|calcul-mental|complements|doubles-et-moities/', 'out' => '/fraction/',
            'blurb' => 'Calcul mental, compléments, addition et soustraction posées avec retenues, et problèmes additifs.'),
        'multiplication-et-division' => array('name' => 'Multiplication et division',
            'in' => '/multiplication|division|tables|partage|multiples|arithmetique/', 'out' => '/fraction|tables-d-addition|relatif|suite/',
            'blurb' => 'Tables de multiplication, multiples et diviseurs, multiplication posée, partages et groupements, division euclidienne et décimale.'),
        'fractions' => array('name' => 'Fractions',
            'in' => '/fraction/', 'out' => '/^$/',
            'blurb' => 'Lire et écrire des fractions, les placer, les comparer, trouver des fractions égales, additionner et soustraire des fractions, fraction d’une quantité.'),
        'nombres-decimaux' => array('name' => 'Nombres décimaux',
            'in' => '/decima|arrondir/', 'out' => '/division/',
            'blurb' => 'Dixièmes, centièmes et millièmes, fractions décimales et écriture à virgule, comparer, ranger et arrondir des nombres décimaux.'),
        'algebre-et-proportionnalite' => array('name' => 'Algèbre et proportionnalité',
            'in' => '/egalites|programme|proportionnalit|pourcentage|echelle|agrandissement|(^|-)ratios?(-|$)/', 'out' => '/^$/',
            'blurb' => 'Égalités à trous, programmes de calcul, suites de nombres et de motifs, tableaux de proportionnalité et recettes.'),
        'nombres-relatifs' => array('name' => 'Nombres relatifs',
            'in' => '/relatif/', 'out' => '/^$/',
            'blurb' => 'Nombres positifs et négatifs, droite graduée et repère, comparer, additionner, soustraire, multiplier et diviser des nombres relatifs.'),
        'puissances-et-racines' => array('name' => 'Puissances et racines carrées',
            'in' => '/puissance|racine|carres-et-cubes|notation-scientifique/', 'out' => '/^$/',
            'blurb' => 'Carrés et cubes, puissances de 10, notation scientifique, racines carrées et équation x² = a.'),
        'calcul-litteral-et-equations' => array('name' => 'Calcul littéral et équations',
            'in' => '/priorites|schemas-en-barres|expression|litteral|equation|developper|factoris|identites|programmes-de-calcul|enchainement|systeme|signes/', 'out' => '/^$/',
            'blurb' => 'Priorités opératoires, schémas en barres, expressions littérales, développer et factoriser, identités remarquables, équations et inéquations.'),
        'fonctions' => array('name' => 'Fonctions',
            'in' => '/fonction|variations-et-extremums|deriv|exponentiel/', 'out' => '/^$/',
            'blurb' => 'Tableaux de valeurs et graphiques, image et antécédent, fonctions linéaires et affines, fonction carré.'),
        'suites' => array('name' => 'Suites numériques',
            'in' => '/(^|-)suites-|-de-suites$/', 'out' => '/^$/',
            'blurb' => 'Suites définies de façon explicite ou par récurrence, suites arithmétiques et géométriques, sens de variation, sommes de termes, limites et seuils.'),
        'second-degre' => array('name' => 'Second degré',
            'in' => '/second-degre|forme-canonique/', 'out' => '/^$/',
            'blurb' => 'Forme canonique et sommet de la parabole, discriminant, équations du second degré, signe d’un trinôme, factorisation et inéquations.'),
        'derivation' => array('name' => 'Dérivation',
            'in' => '/deriv/', 'out' => '/^$/',
            'blurb' => 'Taux de variation, nombre dérivé et tangente, formules de dérivation, signe de la dérivée, variations, extremums et optimisation.'),
        'problemes' => array('name' => 'Résolution de problèmes',
            'in' => '/probleme/', 'out' => '/^$/',
            'blurb' => 'Problèmes additifs et multiplicatifs en une ou plusieurs étapes, comparaisons « de plus » et « fois plus ».'),
        'grandeurs-et-mesures' => array('name' => 'Grandeurs et mesures',
            'in' => '/longueur|masse|contenance|perimetre|monnaie|heure|duree|mesure|(^|-)aires|volume/', 'out' => '/^$/',
            'blurb' => 'Longueurs et périmètres, masses, contenances, aires, lire l’heure et calculer des durées, la monnaie et les conversions.'),
        'geometrie' => array('name' => 'Espace et géométrie',
            'in' => '/solide|figure|symetrie|repere|angle|geometrie|deplacer|droite|triangle|quadrilatere|mediatrice|cercle|parallelogramme|translation|pythagore|thales|trigonometr|vecteur|sphere|pyramide|reperage|milieu|cone|colinearite|scalaire|kashi/', 'out' => '/^$/',
            'blurb' => 'Solides, figures planes, angles droits, symétrie axiale, se repérer et se déplacer sur un plan ou un quadrillage.'),
        'donnees' => array('name' => 'Organisation et gestion des données',
            'in' => '/tableau|diagramme|donnees|graphique|probabilit|statistique|echantillon|aleatoire|variance/', 'out' => '/coordonnees|signes/',
            'blurb' => 'Lire et compléter des tableaux, diagrammes en barres, courbes et diagrammes circulaires, et premières probabilités.'),
    );
}

/* Italy: Italian unit slugs, Italian names */
function topic_defs_it() {
    return array(
        'numeri' => array('name' => 'Numeri',
            'in' => '/numeri|ordinare|potenz|pari-e-dispari|espression|multipli/', 'out' => '/decimal|frazion/',
            'blurb' => 'Leggere, scrivere e scomporre i numeri, il valore posizionale delle cifre, confrontare e ordinare i numeri sulla retta.'),
        'addizione-e-sottrazione' => array('name' => 'Addizione e sottrazione',
            'in' => '/addizion|sottrazion|calcolo-mentale/', 'out' => '/^$/',
            'blurb' => 'Calcolo mentale, addizioni e sottrazioni in colonna con il cambio, prova e proprietà delle operazioni.'),
        'moltiplicazione-e-divisione' => array('name' => 'Moltiplicazione e divisione',
            'in' => '/moltiplic|division|tabellin|doppio/', 'out' => '/^$/',
            'blurb' => 'Tabelline, moltiplicazioni in colonna, divisioni con il resto, moltiplicare e dividere per 10, 100 e 1000.'),
        'frazioni-e-decimali' => array('name' => 'Frazioni e numeri decimali',
            'in' => '/frazion|decimal|percentual/', 'out' => '/^$/',
            'blurb' => 'Unità frazionarie, frazione di una quantità, frazioni decimali, numeri decimali con l’euro e le misure, percentuali.'),
        'problemi' => array('name' => 'Problemi',
            'in' => '/problemi|compravendita/', 'out' => '/^$/',
            'blurb' => 'Problemi con una o due operazioni, dati utili e inutili, domande nascoste, problemi con l’euro e le misure.'),
        'misure' => array('name' => 'Misure',
            'in' => '/misure|lunghezz|peso|capacit|euro|orologio|tempo/', 'out' => '/^$/',
            'blurb' => 'Misure di lunghezza, peso e capacità, equivalenze, l’euro, l’orologio e la durata del tempo.'),
        'geometria' => array('name' => 'Geometria',
            'in' => '/linee|angoli|figure|poligon|perimetro|solidi|simmetria|percorsi|cerchio|trasformazion|cartesian|triangol|quadrilater|isometri|(^|-)area(-|$)/', 'out' => '/^$/',
            'blurb' => 'Linee e angoli, poligoni e perimetro, figure solide, simmetria, percorsi e reticoli.'),
        'dati-e-probabilita' => array('name' => 'Dati e probabilità',
            'in' => '/dati|probabilit|grafic|indagin/', 'out' => '/^$/',
            'blurb' => 'Indagini, tabelle, ideogrammi e istogrammi, la moda, eventi certi, possibili e impossibili.'),
    );
}

function topic_defs($country = null) {
    if ($country === 'tw') return topic_defs_tw();
    if ($country === 'de') return topic_defs_de();
    if ($country === 'fr') return topic_defs_fr();
    if ($country === 'it') return topic_defs_it();
    $d = array(
        'fractions' => array('name' => 'Fractions',
            'in' => '/fraction|halves|thirds|fourths|quarters|mixed-num|improper|fair-shares|partition-shapes|operations-with-rational/',
            'out' => '/decimals-tenths|algebraic-fractions|fractional-equations/',
            'blurb' => 'Start with halves and quarters, then move on to equivalent fractions, comparing fractions, mixed numbers, and adding, subtracting, multiplying and dividing fractions.'),
        'decimals' => array('name' => 'Decimals',
            'in' => '/decimal|thousandths/', 'out' => '/^$/',
            'blurb' => 'Tenths and hundredths first, then place value, comparing and rounding decimals, and adding, subtracting, multiplying and dividing with decimals.'),
        'percents' => array('name' => 'Percents', 'name_gb' => 'Percentages',
            'in' => '/percent|discount|compound-interest/', 'out' => '/^$/',
            'blurb' => 'What percent means, converting between fractions, decimals and percents, finding a percent of an amount, discounts and percent change.',
            'blurb_gb' => 'What percentage means, converting between fractions, decimals and percentages, finding a percentage of an amount, discounts and percentage change.'),
        'ratios-and-rates' => array('name' => 'Ratios and Rates',
            'in' => '/(^|-)ratios?(-|$)|(^|-)rates?(-|$)|proportion|scaling|speed/', 'out' => '/trigonometric|rates-of-change|proportionality-and-similarity/',
            'blurb' => 'Writing ratios, equivalent ratios and ratio tables, unit rates, proportional reasoning and ratio word problems.'),
        'multiplication' => array('name' => 'Multiplication',
            'in' => '/multipl|times-table|arrays|equal-groups|twos-doubling/',
            'out' => '/fraction|decimal|integer|polynomial|scientific|multiples/',
            'blurb' => 'Equal groups and arrays, multiplication facts and tables, multiplying by 10 and 100, and multi-digit multiplication with word problems.'),
        'division' => array('name' => 'Division',
            'in' => '/divi|sharing|equal-groups|fair-shares/',
            'out' => '/fraction|decimal|integer|polynomial|divisib/',
            'blurb' => 'Sharing and grouping, division facts, remainders, short division and long division with word problems.'),
        'addition-and-subtraction' => array('name' => 'Addition and Subtraction',
            'in' => '/add|subtract|number-bonds|make-10|making-10|10-more-and-10-less|ways-to-make|decompose-numbers|decomposing-numbers|ten-more|change-in-quantity|word-problems|part-part-whole|taking-away|problem-solving-to|mental-mathematics|story-sums/',
            'out' => '/fraction|decimal|integer|polynomial|mixed-num|multiplicative|ratio|segment-addition|quadratic|multiplication-and-division-word|measurement-word/',
            'blurb' => 'Number bonds and facts to 20, mental strategies, adding and subtracting with regrouping, and multi-step word problems.',
            'blurb_gb' => 'Number bonds and facts to 20, mental strategies, column addition and subtraction, and multi-step word problems.'),
        'place-value' => array('name' => 'Place Value and Numbers',
            'in' => '/place-value|numbers-to|numbers-up-to|(^|-)count|tens-and-ones|compare-t|comparing-numbers|writing-numbers|roman|large-numbers|billions|ordinal|odd-and-even|skip-counting|powers-and-large|subitising|subitizing|one-more-and-one-less|comparing-quantities|ordering-numbers|^number-lines$|^10-more-10-less|^whole-numbers$|comparing-and-ordering-to|number-symbols-and-names/',
            'out' => '/counterexample|money|coins|fraction|sort-and-count|decompose|decomposing|counting-principle/',
            'blurb' => 'Counting, tens and ones, place value to millions and beyond, comparing and ordering numbers, and odd and even numbers.'),
        'rounding-and-estimation' => array('name' => 'Rounding and Estimation',
            'in' => '/round|estimat|benchmark|calculation-techniques/', 'out' => '/^$/',
            'blurb' => 'Rounding to the nearest 10, 100 and 1000, rounding decimals, and estimating to check answers.'),
        'order-of-operations' => array('name' => 'Order of Operations',
            'in' => '/order-of-operations|numerical-expressions|calculating-with-whole-numbers/', 'out' => '/^$/',
            'blurb' => 'Which operation comes first, working with brackets and exponents, and writing number problems as one expression.'),
        'factors-and-multiples' => array('name' => 'Factors, Multiples and Primes',
            'in' => '/factor|prime|gcf|multiples|divisib/', 'out' => '/multiples-of-10|(?<!prime-)factoris|factoring|missing-factors|factor-theorem/',
            'blurb' => 'Factors and multiples, prime and composite numbers, common factors and common multiples.'),
        'exponents-and-roots' => array('name' => 'Exponents and Square Roots', 'name_gb' => 'Powers, Roots and Indices',
            'in' => '/exponent|irrational|square-root|squares-cubes|perfect-square|cube-root|scientific|powers|square-numbers|indices|index-|standard-form|radical|logarithm|surds/', 'out' => '/powers-of-10|hyperbolic-and-exponential/',
            'blurb' => 'Powers and exponents, perfect squares, square roots and cube roots, and scientific notation.',
            'blurb_gb' => 'Powers and index laws, square and cube numbers, square roots and cube roots, and standard form.'),
        'integers' => array('name' => 'Integers and Negative Numbers',
            'in' => '/integer|negative|absolute|rational-number|real-numbers/', 'out' => '/irrational|absolute-value-equations|absolute-value-functions|absolute-deviation/',
            'blurb' => 'Negative numbers on the number line, comparing integers, absolute value, and adding, subtracting, multiplying and dividing integers.'),
        'algebra' => array('name' => 'Algebra, Equations and Patterns',
            'in' => '/pattern|algebra|direct-variation|formulas-and-solving|^factoring$|^(products-and-)?factorisation$|^parallel-and-perpendicular-lines$|independent-and-dependent-quantities|expression|equation|inequalit|slope|function|equal-sign|equality|equal-and-not|number-sentences|relation|polynomial|missing-numbers|sequence|substitution|expanding|expansion|subject-of|simultaneous|quadratic|straight-line|linear-graphs|exponential-graphs|domain-and-range|logarithm|complex-numbers|binomial-theorem|input-output|multi-step-problems|vertex-form|parabolas|discontinuities|end-behavior|nature-of-roots|sigma-notation/',
            'out' => '/geometry-of-straight-lines|triangle-inequality|distance-slope-and-midpoint|order-of-operations-and|angle-relationships|correlation|equations-of-circles|trigonometric|special-angles/',
            'blurb' => 'Number and shape patterns, the equal sign, missing numbers, expressions, one- and two-step equations, inequalities and linear relations.'),
        'quadratics' => array('name' => 'Quadratic Equations and Functions',
            'in' => '/quadratic|nature-of-roots|factoring-polynomials|^factoring$|completing-the-square|vertex-form|parabolas/', 'out' => '/^$/',
            'blurb' => 'Factoring quadratics, solving by factoring, square roots, completing the square and the quadratic formula, and graphing parabolas.',
            'blurb_gb' => 'Expanding and factorising quadratics, solving quadratic equations, completing the square and quadratic graphs.'),
        'money' => array('name' => 'Money and Financial Literacy',
            'in' => '/money|coins|financial|budget|best-buys|interest|exchange|discount-gst|finance|credit-and-loans|saving-and-investing|paying-for-college|annuities/', 'out' => '/^$/',
            'blurb' => 'Counting coins and bills, making change, budgets, discounts and tax, saving and interest.',
            'blurb_gb' => 'Counting coins and notes, giving change, budgets, discounts, saving and interest.'),
        'time' => array('name' => 'Time',
            'in' => '/time|clock|calendar|days-weeks|days-of-the-week|timetables|duration|elapsed/', 'out' => '/times-table|speed-distance|over-time/',
            'blurb' => 'Telling time on analog and digital clocks, a.m. and p.m., the 24-hour clock, elapsed time and calendars.',
            'blurb_gb' => 'Telling the time on analogue and digital clocks, the 12- and 24-hour clock, how long things take, and calendars.'),
        'measurement' => array('name' => 'Measurement',
            'in' => '/measur|^temperature$|length|mass|capacity|metric|convert|scales|conversion|units-and|liquid-volume|weight/', 'out' => '/angle|converting-fractions|geometric|arc-length|trigonometric|parametric/',
            'blurb' => 'Measuring length, mass and capacity, reading scales, and converting between units.'),
        'area-and-perimeter' => array('name' => 'Area and Perimeter',
            'in' => '/area|perimeter|dimensional-change/', 'out' => '/surface-area-nets|surface-area-of|surface-area-and|area-rules/',
            'blurb' => 'Perimeter by counting and by adding sides, area of rectangles, triangles and other polygons, and area of circles.'),
        'volume' => array('name' => 'Volume and Surface Area',
            'in' => '/volume|surface-area|dimensional-change/', 'out' => '/liquid-volume/',
            'blurb' => 'Volume by counting cubes, volume of cubes, cuboids, prisms and cylinders, capacity, and surface area from nets.'),
        'angles' => array('name' => 'Angles',
            'in' => '/(^|-)angles?(-|$)|turns|transversal|geometry-of-straight-lines/', 'out' => '/special-angles|double-angles/',
            'blurb' => 'Right, acute and obtuse angles, measuring with a protractor, angles on a line and at a point, and angles in shapes.'),
        'shapes' => array('name' => '2D and 3D Shapes',
            'in' => '/shape|midsegment|polygon|quadrilateral|triangle|circles|circumference|prism|3d|2d|nets|objects|parallelogram|rectangles-and-squares|lines-angles|perpendicular|congruence|classify-two|classifying-two|pythagor|trigonometr|arcs-and|elevations|law-of-sines|points-lines|cross-section|euclidean-geometry/',
            'out' => '/^parallel-and-perpendicular-lines$|circle-graph|number-shape|composite-area|similar-shapes|area-of|trigonometric|special-angles/',
            'blurb' => 'Naming and sorting 2D shapes and 3D objects, sides and vertices, triangles and quadrilaterals, circles, nets and solids.'),
        'circles' => array('name' => 'Circles',
            'in' => '/circle|circum|arc-length|arcs-and|sector/', 'out' => '/circle-graph|bisector/',
            'blurb' => 'Parts of a circle, circumference and area, arc length and sectors, central and inscribed angles, tangents and equations of circles.',
            'blurb_gb' => 'Parts of a circle, circumference and area, arcs and sectors, angles in circles and tangents.'),
        'congruence-and-similarity' => array('name' => 'Congruence and Similarity',
            'in' => '/congruen|similar/', 'out' => '/similar-fractions|dissimilar/',
            'blurb' => 'Congruent figures, the SSS, SAS, ASA, AAS and HL shortcuts, similar figures, scale factors and similar triangles.'),
        'symmetry-and-transformations' => array('name' => 'Symmetry and Transformations',
            'in' => '/symmetr|transform|reflection|translation|tessellation|scale-|similar|dilation/', 'out' => '/properties-of-circles|transformations-of-(linear|quadratic)-functions|similar-fractions|dissimilar|proportionality-and-similarity/',
            'blurb' => 'Lines of symmetry, slides, flips and turns, combining transformations, tessellations and scale drawings.'),
        'coordinates-and-position' => array('name' => 'Coordinates and Position',
            'in' => '/coordinat|cartesian|position|direction|maps|location|grid-ref|bearing|loci|distance-and-midpoint|distance-slope-and-midpoint|segments-midpoints|equations-of-circles|conic-sections|ellipses-and-hyperbolas|analytical-geometry/', 'out' => '/composition|velocity/',
            'blurb' => 'Position and direction words, maps and grid references, plotting points and the coordinate plane.'),
        'data-and-graphs' => array('name' => 'Data and Graphs',
            'in' => '/graph|chart|data|plot|stem-and-leaf|tally|pictogra|mean|median|average|statistic|central-tendency|sorting|sort-and-count|two-way|organize|sampling|random-samples|distribution|correlation|statistical-studies|standard-deviation/',
            'out' => '/geometric-mean|bisectors-and-medians|straight-line-graphs|linear-graphs|quadratic-graphs|graphing-|graphs-of-sine|graphs-of-trigonometric|polar-coordinates|exponential-graphs/',
            'blurb' => 'Tally charts, picture graphs and bar graphs, line plots and line graphs, pie charts, the mean, median and mode, and random samples.',
            'blurb_gb' => 'Tally charts, pictograms and bar charts, line graphs and pie charts, and the mean.'),
        'vectors-and-matrices' => array('name' => 'Vectors and Matrices',
            'in' => '/vector|matri/', 'out' => '/^$/',
            'blurb' => 'Vectors in component form, magnitude and direction, vector operations and the dot product, matrix operations, determinants and inverse matrices.'),
        'trigonometry' => array('name' => 'Trigonometry',
            'in' => '/trigonometr|(^|-)sines?(-|$)|cosine|unit-circle|sum-and-difference-formulas|angles-of-elevation|three-dimensions|sinusoidal|degrees-radians|angular-velocity|special-angles|reduction-formulae|double-angles/', 'out' => '/^$/',
            'blurb' => 'Sine, cosine and tangent in right triangles, the laws of sines and cosines, radians and the unit circle, and graphs of sine and cosine.'),
        'calculus' => array('name' => 'Differential Calculus',
            'in' => '/limits-and-first|differentiation|equations-of-tangents|cubic-functions|optimisation/', 'out' => '/^$/',
            'blurb' => 'Limits and first principles, the rules of differentiation, equations of tangents, cubic graphs with stationary points, and optimisation and rates of change.'),
        'probability' => array('name' => 'Probability',  'name_au' => 'Chance and Probability',
            'in' => '/probab|chance|sample-spaces|likelihood|permutations-and-combinations|expected-value/', 'out' => '/^$/',
            'blurb' => 'Likelihood words, spinners and number cubes, probability as a fraction, experiments and tree diagrams.'),
    );
    if ($country === 'in') {
        // India (NCERT chapter names): Real Numbers is HCF, LCM and irrational numbers; Arithmetic Progressions are sequences
        $d['factors-and-multiples']['in'] = substr($d['factors-and-multiples']['in'], 0, -1) . '|^real-numbers$/';
        $d['exponents-and-roots']['in'] = substr($d['exponents-and-roots']['in'], 0, -1) . '|^real-numbers$|^number-systems$/';
        $d['integers']['out'] = substr($d['integers']['out'], 0, -1) . '|^real-numbers$/';
        $d['algebra']['in'] = substr($d['algebra']['in'], 0, -1) . '|progression/';
        $d['shapes']['out'] = substr($d['shapes']['out'], 0, -1) . '|trigonometr|areas-related|surface-areas/';
        $d['area-and-perimeter']['out'] = substr($d['area-and-perimeter']['out'], 0, -1) . '|surface-areas/';
        // Class 9: Heron's Formula is the area of a triangle; Euclid's Geometry is points, lines and angles
        $d['area-and-perimeter']['in'] = substr($d['area-and-perimeter']['in'], 0, -1) . '|heron/';
        $d['angles']['in'] = substr($d['angles']['in'], 0, -1) . '|euclid/';
        // Classes 6-8 (Ganita Prakash chapter names)
        $gp = array(
            'factors-and-multiples' => '^prime-time$|common-ground|^number-play$',
            'exponents-and-roots' => 'square-and-a-cube|^power-play$',
            'place-value' => 'story-of-numbers',
            'integers' => 'other-side-of-zero|operations-with-integers',
            'decimals' => 'peek-beyond-the-point',
            'percents' => 'fractions-in-disguise',
            'algebra' => 'finding-the-unknown|we-distribute',
            'data-and-graphs' => 'connecting-the-dots|dots-and-lines',
            'angles' => 'parallel-and-intersecting|three-intersecting|constructions-and-tilings',
            'shapes' => 'three-intersecting|constructions-and-tilings|playing-with-constructions|geometric-themes',
            'circles' => 'playing-with-constructions',
            'congruence-and-similarity' => 'geometric-twins',
        );
        foreach ($gp as $k => $re) $d[$k]['in'] = substr($d[$k]['in'], 0, -1) . '|' . $re . '/';
        $d['time']['out'] = substr($d['time']['out'], 0, -1) . '|^prime-time$/';
        $d['rounding-and-estimation']['out'] = substr($d['rounding-and-estimation']['out'], 0, -1) . '|common-ground/';
        $d['multiplication']['out'] = substr($d['multiplication']['out'], 0, -1) . '|we-distribute/';
        $d['congruence-and-similarity']['in'] = substr($d['congruence-and-similarity']['in'], 0, -1) . '|^triangles$/';
        // Classes 1-5 (Joyful Mathematics and Maths Mela chapter names)
        $jm = array(
            'place-value' => '^thousands-around-us$|^mango-treat$|^making-10$|^fun-with-numbers$|^a-day-at-the-beach$|^double-century$|^house-of-hundreds-1$|^we-the-travellers-1$',
            'addition-and-subtraction' => '^how-many$|^vegetable-farm$|^decoration-for-festival$|^give-and-take$|^vacation-with-my-nani-maa$|^house-of-hundreds-2$|^the-cleanest-village$|^elephants-tigers-and-leopards$|^we-the-travellers-2$',
            'multiplication' => '^how-many-times$|^raksha-bandhan$|^the-transport-museum$|^the-dairy-farm$',
            'division' => '^fun-at-class-party$|^the-transport-museum$|^coconut-farm$',
            'fractions' => '^fair-share$|^sharing-and-measuring$',
            'factors-and-multiples' => '^animal-jumps$',
            'money' => '^how-much-can-we-spend$|^fun-at-the-fair$|^the-surajkund-fair$',
            'time' => '^how-do-i-spend-my-day$|^which-season-is-it$|^racing-seconds$',
            'measurement' => '^linas-family$|^ranis-gift$|^filling-and-lifting$|^weigh-it-pour-it$|^far-and-near$',
            'area-and-perimeter' => '^grandmothers-quilt$',
            'shapes' => '^what-is-long-what-is-round$|^shadow-story$|^playing-with-lines$|^toy-joy$',
            'coordinates-and-position' => '^finding-the-furry-cat$|^hide-and-seek$',
            'data-and-graphs' => '^so-many-toys$|^whats-in-a-name$',
            'algebra' => '^utsav$',
        );
        foreach ($jm as $k => $re) $d[$k]['in'] = substr($d[$k]['in'], 0, -1) . '|' . $re . '/';
        $d['rounding-and-estimation']['out'] = substr($d['rounding-and-estimation']['out'], 0, -1) . '|^(shapes|pattern|thousands)-around-us$|what-is-long-what-is-round/';
        $d['addition-and-subtraction']['out'] = str_replace('|ratio|', '|(?<!deco)ratio|', $d['addition-and-subtraction']['out']);
        $d['time']['out'] = substr($d['time']['out'], 0, -1) . '|^how-many-times$/';
        $d['measurement']['out'] = substr($d['measurement']['out'], 0, -1) . '|^symmetrical-designs$|^sharing-and-measuring$/';
        $d['division']['out'] = substr($d['division']['out'], 0, -1) . '|^sharing-and-measuring$/';
        $d['algebra']['out'] = substr($d['algebra']['out'], 0, -1) . '|^shapes-and-patterns$/';
        // Classes 11-12: calculus covers integrals and differential equations too; lines and 3D geometry are coordinate geometry
        $d['calculus']['name'] = 'Calculus';
        $d['calculus']['blurb'] = 'Limits and derivatives, continuity and differentiability, applications of derivatives, integrals, areas under curves and differential equations.';
        $d['calculus']['in'] = substr($d['calculus']['in'], 0, -1) . '|^limits-and-derivatives$|^continuity-and-differentiability$|^application-of-derivatives$|^integrals$|^application-of-integrals$|^differential-equations$/';
        $d['vectors-and-matrices']['in'] = substr($d['vectors-and-matrices']['in'], 0, -1) . '|^determinants$|^three-dimensional-geometry$/';
        $d['coordinates-and-position']['in'] = substr($d['coordinates-and-position']['in'], 0, -1) . '|^straight-lines$|three-dimensional-geometry$/';
        $d['algebra']['in'] = substr($d['algebra']['in'], 0, -1) . '|^linear-programming$/';
        $d['algebra']['out'] = substr($d['algebra']['out'], 0, -1) . '|^vector-algebra$|^differential-equations$|^straight-lines$/';
    }
    return $d;
}

/* British spelling for these countries */
function topic_gb($country) { return in_array($country, array('uk', 'au', 'sg', 'za', 'in'), true); }

function topic_name($t, $country) {
    if ($country === 'au' && isset($t['name_au'])) return $t['name_au'];
    if (topic_gb($country) && isset($t['name_gb'])) return $t['name_gb'];
    return $t['name'];
}
function topic_blurb($t, $country) {
    return (topic_gb($country) && isset($t['blurb_gb'])) ? $t['blurb_gb'] : $t['blurb'];
}

/* slugs of the topics a unit belongs to (most specific first: definition order) */
function unit_topic_slugs($unit_slug, $country = null) {
    $out = array();
    foreach (topic_defs($country) as $k => $t) {
        if (preg_match($t['in'], $unit_slug) && !preg_match($t['out'], $unit_slug)) $out[] = $k;
    }
    return $out;
}

/* all units of a country+subject with grade name and order (one query per page) */
function subject_units($c, $s) {
    static $cache = array();
    if (!isset($cache[$c . '/' . $s])) {
        $cache[$c . '/' . $s] = qa('SELECT u.country, u.slug, u.title, u.short_title, u.standard_code, u.key_big, u.updated, u.grade,
                       g.name AS grade_name, g.sort AS gsort
                FROM ws_unit u JOIN ws_grade g ON g.country=u.country AND g.subject=u.subject AND g.slug=u.grade
                WHERE u.country=? AND u.subject=? ORDER BY g.sort, u.sort, u.slug', array($c, $s));
    }
    return $cache[$c . '/' . $s];
}

define('TOPIC_MIN_UNITS', 3);   // a topic with fewer skills gets no page (too thin)

/* topic => list of units, only topics with enough units, in definition order */
function topics_for($c, $s) {
    $all = subject_units($c, $s);
    $res = array();
    foreach (topic_defs($c) as $k => $t) {
        $list = array();
        foreach ($all as $u) {
            if (preg_match($t['in'], $u['slug']) && !preg_match($t['out'], $u['slug'])) $list[] = $u;
        }
        if (count($list) >= TOPIC_MIN_UNITS) $res[$k] = $list;
    }
    return $res;
}

/* "Grade 1 to Grade 8" / "Year 3 to Year 6" / "Primary 1 to Primary 6" */
function topic_range($units) {
    $first = $units[0]['grade_name'];
    $last = $units[count($units) - 1]['grade_name'];
    if ($first === $last) return $first;
    if ($units[0]['country'] === 'tw') return $first . '到' . $last;
    if ($units[0]['country'] === 'fr') return 'du ' . $first . ' au ' . $last;
    if ($units[0]['country'] === 'it') return 'dalla ' . strtolower($first) . ' alla ' . strtolower($last);
    return $units[0]['country'] === 'de' ? $first . ' bis ' . $last : $first . ' to ' . $last;
}

/* lower case for use inside a sentence, keeping "2D", "3D" */
function topic_lc($name) {
    return preg_replace_callback('/\b[A-Za-z]+\b/', function ($m) { return strtolower($m[0]); }, $name);
}
