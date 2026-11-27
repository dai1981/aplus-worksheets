<?php
/* Fields for comparing countries in the Quiz Together ranking (/worksheets/ranking/?sub=math&fd=fractions).
   Every country has its own topic slugs (inc/topics.php). MQ_TOPIC_FIELD puts each of them into one or more
   fields that are the same in every country, so "Fractions, decimals and percentages" in Germany, Japan or India
   can be compared, even though the questions are not the same.
   tools/build_mq_fields.php writes inc/mq-fields.json (field -> unit pages) from content/; api/mq.php gives it to
   the shared eigo-duke.com /common/php/mq.php ($MQ_FIELD_FILE). */

const MQ_FIELD_LANGS = array('en', 'zh-TW', 'zh-CN', 'ko', 'id', 'tr', 'sv', 'de', 'fr', 'it', 'es', 'pt-BR');

/* field => [subject group, names in MQ_FIELD_LANGS order] */
function mq_fields() {
    return array(
        'numbers' => array('math', array('Numbers and place value', '數與位值', '数与数位', '수와 자릿값', 'Bilangan dan nilai tempat', 'Sayılar ve basamak değeri', 'Tal och positionssystem', 'Zahlen und Stellenwerte', 'Nombres et numération', 'Numeri e valore posizionale', 'Números y valor posicional', 'Números e valor posicional')),
        'add-sub' => array('math', array('Addition and subtraction', '加法與減法', '加法和减法', '덧셈과 뺄셈', 'Penjumlahan dan pengurangan', 'Toplama ve çıkarma', 'Addition och subtraktion', 'Addition und Subtraktion', 'Addition et soustraction', 'Addizione e sottrazione', 'Suma y resta', 'Adição e subtração')),
        'mul-div' => array('math', array('Multiplication and division', '乘法與除法', '乘法和除法', '곱셈과 나눗셈', 'Perkalian dan pembagian', 'Çarpma ve bölme', 'Multiplikation och division', 'Multiplikation und Division', 'Multiplication et division', 'Moltiplicazione e divisione', 'Multiplicación y división', 'Multiplicação e divisão')),
        'fractions' => array('math', array('Fractions, decimals and percentages', '分數、小數與百分率', '分数、小数和百分数', '분수·소수·백분율', 'Pecahan, desimal, dan persen', 'Kesirler, ondalıklar ve yüzdeler', 'Bråk, decimaltal och procent', 'Brüche, Dezimalzahlen und Prozente', 'Fractions, décimaux et pourcentages', 'Frazioni, decimali e percentuali', 'Fracciones, decimales y porcentajes', 'Frações, decimais e porcentagem')),
        'ratios' => array('math', array('Ratio, proportion and rates', '比與比例', '比和比例', '비와 비율', 'Rasio dan proporsi', 'Oran ve orantı', 'Proportionalitet och förhållanden', 'Verhältnisse und Proportionalität', 'Proportionnalité et ratios', 'Rapporti e proporzionalità', 'Razón y proporcionalidad', 'Razão e proporcionalidade')),
        'integers' => array('math', array('Negative numbers, powers and roots', '正負數、次方與根號', '正负数、乘方和根号', '음수·거듭제곱·제곱근', 'Bilangan bulat, pangkat, dan akar', 'Tam sayılar, üsler ve kökler', 'Negativa tal, potenser och rötter', 'Negative Zahlen, Potenzen und Wurzeln', 'Nombres relatifs, puissances et racines', 'Numeri relativi, potenze e radici', 'Números enteros, potencias y raíces', 'Números inteiros, potências e raízes')),
        'algebra' => array('math', array('Expressions and equations', '式與方程式', '式与方程', '식과 방정식', 'Aljabar dan persamaan', 'Cebirsel ifadeler ve denklemler', 'Uttryck och ekvationer', 'Terme und Gleichungen', 'Calcul littéral et équations', 'Calcolo letterale ed equazioni', 'Expresiones y ecuaciones', 'Expressões e equações')),
        'functions' => array('math', array('Functions and graphs', '函數與圖形', '函数与图像', '함수와 그래프', 'Fungsi dan grafik', 'Fonksiyonlar ve grafikler', 'Funktioner och grafer', 'Funktionen und Graphen', 'Fonctions et graphiques', 'Funzioni e grafici', 'Funciones y gráficas', 'Funções e gráficos')),
        'patterns' => array('math', array('Patterns and sequences', '規律與數列', '规律与数列', '규칙과 수열', 'Pola dan barisan', 'Örüntüler ve diziler', 'Mönster och talföljder', 'Muster und Folgen', 'Suites et régularités', 'Successioni e regolarità', 'Patrones y sucesiones', 'Padrões e sequências')),
        'geometry' => array('math', array('Shapes, angles and geometry', '圖形、角與幾何', '图形、角与几何', '도형·각·기하', 'Bangun, sudut, dan geometri', 'Şekiller, açılar ve geometri', 'Figurer, vinklar och geometri', 'Formen, Winkel und Geometrie', 'Figures, angles et géométrie', 'Figure, angoli e geometria', 'Figuras, ángulos y geometría', 'Figuras, ângulos e geometria')),
        'measurement' => array('math', array('Measurement: length, area, volume, time and money', '量與測量（長度、面積、體積、時間、金錢）', '量与计量（长度、面积、体积、时间、钱币）', '측정(길이·넓이·부피·시간·돈)', 'Pengukuran: panjang, luas, volume, waktu, dan uang', 'Ölçme: uzunluk, alan, hacim, zaman ve para', 'Mätning: längd, area, volym, tid och pengar', 'Größen: Längen, Flächen, Volumen, Zeit und Geld', 'Grandeurs et mesures : longueurs, aires, volumes, durées, monnaie', 'Misure: lunghezze, aree, volumi, tempo e denaro', 'Medida: longitud, área, volumen, tiempo y dinero', 'Medidas: comprimento, área, volume, tempo e dinheiro')),
        'data' => array('math', array('Data, statistics and probability', '資料、統計與機率', '数据、统计与概率', '자료·통계·확률', 'Data, statistika, dan peluang', 'Veri, istatistik ve olasılık', 'Statistik och sannolikhet', 'Daten, Statistik und Wahrscheinlichkeit', 'Données, statistiques et probabilités', 'Dati, statistica e probabilità', 'Estadística y probabilidad', 'Estatística e probabilidade')),
        'trigonometry' => array('math', array('Trigonometry', '三角函數', '三角函数', '삼각함수', 'Trigonometri', 'Trigonometri', 'Trigonometri', 'Trigonometrie', 'Trigonométrie', 'Trigonometria', 'Trigonometría', 'Trigonometria')),
        'calculus' => array('math', array('Calculus', '微積分', '微积分', '미적분', 'Kalkulus', 'Limit, türev ve integral', 'Derivata och integraler', 'Differenzial- und Integralrechnung', 'Analyse : dérivées et intégrales', 'Analisi: derivate e integrali', 'Análisis: derivadas e integrales', 'Cálculo: derivadas e integrais')),
        'word-problems' => array('math', array('Word problems', '應用題', '应用题', '문장제', 'Soal cerita', 'Problemler', 'Problemlösning', 'Sachaufgaben', 'Problèmes', 'Problemi', 'Problemas', 'Problemas')),
        'matter' => array('science', array('Matter and chemistry', '物質與化學', '物质与化学', '물질과 화학', 'Materi dan kimia', 'Madde ve kimya', 'Materia och kemi', 'Stoffe und Chemie', 'Matière et chimie', 'Materia e chimica', 'Materia y química', 'Matéria e química')),
        'forces-and-motion' => array('science', array('Forces and motion', '力與運動', '力与运动', '힘과 운동', 'Gaya dan gerak', 'Kuvvet ve hareket', 'Krafter och rörelse', 'Kräfte und Bewegung', 'Forces et mouvement', 'Forze e moto', 'Fuerzas y movimiento', 'Forças e movimento')),
        'energy' => array('science', array('Energy and electricity', '能量與電', '能量与电', '에너지와 전기', 'Energi dan listrik', 'Enerji ve elektrik', 'Energi och elektricitet', 'Energie und Elektrizität', 'Énergie et électricité', 'Energia ed elettricità', 'Energía y electricidad', 'Energia e eletricidade')),
        'waves-and-light' => array('science', array('Waves, light and sound', '波、光與聲音', '波、光与声', '파동·빛·소리', 'Gelombang, cahaya, dan bunyi', 'Dalgalar, ışık ve ses', 'Vågor, ljus och ljud', 'Wellen, Licht und Schall', 'Ondes, lumière et son', 'Onde, luce e suono', 'Ondas, luz y sonido', 'Ondas, luz e som')),
        'living-things' => array('science', array('Living things and the human body', '生物與人體', '生物与人体', '생물과 인체', 'Makhluk hidup dan tubuh manusia', 'Canlılar ve insan vücudu', 'Levande organismer och människokroppen', 'Lebewesen und der menschliche Körper', 'Le vivant et le corps humain', 'Esseri viventi e corpo umano', 'Seres vivos y cuerpo humano', 'Seres vivos e corpo humano')),
        'earth-and-space' => array('science', array('Earth and space', '地球與太空', '地球与宇宙', '지구와 우주', 'Bumi dan antariksa', 'Dünya ve uzay', 'Jorden och rymden', 'Erde und Weltall', 'La Terre et l’espace', 'La Terra e lo spazio', 'La Tierra y el espacio', 'Terra e espaço')),
    );
}

/* country topic slug (inc/topics.php) => fields. The same slug means the same thing in every country. */
const MQ_TOPIC_FIELD = array(
    // numbers
    'place-value' => 'numbers', 'rounding-and-estimation' => 'numbers', 'whole-numbers' => 'numbers', 'estimation' => 'numbers', 'numbers' => 'numbers',
    'number-bases' => 'numbers', 'zahlen-und-stellenwerte' => 'numbers', 'nombres' => 'numbers', 'numeri' => 'numbers', 'numeros' => 'numbers',
    'bilangan-cacah' => 'numbers', 'sayilar' => 'numbers', 'tal' => 'numbers',
    // addition and subtraction
    'addition-and-subtraction' => 'add-sub', 'plus-und-minus' => 'add-sub', 'addition-et-soustraction' => 'add-sub', 'addizione-e-sottrazione' => 'add-sub',
    'adicao-e-subtracao' => 'add-sub', 'suma-y-resta' => 'add-sub', 'penjumlahan-dan-pengurangan' => 'add-sub', 'toplama-ve-cikarma' => 'add-sub',
    'addition-och-subtraktion' => 'add-sub',
    // multiplication and division
    'multiplication' => 'mul-div', 'division' => 'mul-div', 'order-of-operations' => 'mul-div', 'factors-and-multiples' => 'mul-div',
    'multiplication-and-division' => 'mul-div', 'mal-und-geteilt' => 'mul-div', 'multiplication-et-division' => 'mul-div',
    'moltiplicazione-e-divisione' => 'mul-div', 'multiplicacao-e-divisao' => 'mul-div', 'multiplicacion-y-division' => 'mul-div',
    'perkalian-dan-pembagian' => 'mul-div', 'carpma-ve-bolme' => 'mul-div', 'carpanlar-ve-bolunebilme' => 'mul-div', 'multiplikation-och-division' => 'mul-div',
    // fractions, decimals and percentages
    'fractions' => 'fractions', 'decimals' => 'fractions', 'percents' => 'fractions', 'fractions-and-decimals' => 'fractions',
    'ratios-and-percentages' => 'fractions ratios', 'brueche-und-dezimalzahlen' => 'fractions', 'nombres-decimaux' => 'fractions',
    'frazioni-e-decimali' => 'fractions', 'fracoes-e-decimais' => 'fractions', 'fracciones-y-decimales' => 'fractions',
    'pecahan-desimal-dan-persen' => 'fractions', 'kesirler' => 'fractions', 'brak-decimaltal-och-procent' => 'fractions',
    // ratio and proportion
    'ratios-and-rates' => 'ratios', 'ratios-and-proportions' => 'ratios', 'oran-ve-oranti' => 'ratios', 'matematica-financeira' => 'ratios',
    'algebre-et-proportionnalite' => 'ratios algebra', 'proporzioni-e-funzioni' => 'ratios functions', 'algebra-y-proporcionalidad' => 'ratios algebra',
    'samband-och-forandring' => 'ratios functions',
    // negative numbers, powers and roots
    'integers' => 'integers', 'exponents-and-roots' => 'integers', 'number-systems' => 'integers', 'rational-and-real-numbers' => 'integers',
    'nombres-relatifs' => 'integers', 'puissances-et-racines' => 'integers', 'bilangan-bulat-dan-rasional' => 'integers', 'pangkat-dan-akar' => 'integers',
    'rasyonel-sayilar' => 'integers', 'uslu-ve-karekoklu-ifadeler' => 'integers', 'potenser-och-reella-tal' => 'integers',
    // expressions and equations
    'algebra' => 'algebra', 'quadratics' => 'algebra functions', 'equations' => 'algebra', 'equations-and-inequalities' => 'algebra',
    'calcul-litteral-et-equations' => 'algebra', 'second-degre' => 'algebra functions', 'calcolo-letterale-ed-equazioni' => 'algebra',
    'algebra-e-funcoes' => 'algebra functions', 'aljabar-dan-pola' => 'algebra patterns', 'denklemler-ve-esitsizlikler' => 'algebra', 'sets-and-logic' => 'algebra',
    'lineare-funktionen-und-gleichungssysteme' => 'algebra functions', 'quadratische-funktionen-und-gleichungen' => 'algebra functions',
    'persamaan-dan-fungsi' => 'algebra functions', 'diskret-matematik' => 'algebra',
    // functions and graphs
    'functions-and-graphs' => 'functions', 'functions' => 'functions', 'fonctions' => 'functions', 'funciones' => 'functions',
    'dogrusal-fonksiyonlar' => 'functions', 'fonksiyonlar' => 'functions', 'exponential-potenz-und-winkelfunktionen' => 'functions trigonometry',
    'esponenziali-e-logaritmi' => 'functions', 'exponents-and-logarithms' => 'functions', 'ustel-ve-logaritmik-fonksiyonlar' => 'functions',
    'geometria-analitica' => 'functions', 'analytic-geometry' => 'functions', 'coordinate-geometry' => 'functions',
    // patterns and sequences
    'patterns-and-sequences' => 'patterns', 'patterns' => 'patterns', 'muster-und-strukturen' => 'patterns', 'suites' => 'patterns',
    'sequences' => 'patterns', 'oruntuler-ve-esitlik' => 'patterns', 'sequences-and-derivatives' => 'patterns calculus', 'diziler-ve-polinomlar' => 'patterns',
    // shapes, angles and geometry
    'angles' => 'geometry', 'shapes' => 'geometry', 'circles' => 'geometry', 'congruence-and-similarity' => 'geometry',
    'symmetry-and-transformations' => 'geometry', 'coordinates-and-position' => 'geometry', 'solids' => 'geometry', 'geometry' => 'geometry',
    'transformations' => 'geometry', 'position-and-movement' => 'geometry', 'geometrie' => 'geometry', 'geometria' => 'geometry', 'geometri' => 'geometry',
    'vektorgeometrie' => 'geometry', 'vectors-and-matrices' => 'geometry', 'vectors-and-complex-numbers' => 'geometry',
    // measurement
    'money' => 'measurement', 'time' => 'measurement', 'measurement' => 'measurement', 'area-and-perimeter' => 'measurement', 'volume' => 'measurement',
    'groessen' => 'measurement', 'grandeurs-et-mesures' => 'measurement', 'misure' => 'measurement', 'grandezas-e-medidas' => 'measurement',
    'magnitudes-y-medida' => 'measurement', 'pengukuran' => 'measurement', 'olcme' => 'measurement', 'matning' => 'measurement',
    // data, statistics and probability
    'data-and-graphs' => 'data', 'probability' => 'data', 'statistics' => 'data', 'data' => 'data', 'counting' => 'data',
    'probability-and-statistics' => 'data', 'counting-and-probability' => 'data', 'daten-und-zufall' => 'data', 'donnees' => 'data',
    'dati-e-probabilita' => 'data', 'probabilidade-e-estatistica' => 'data', 'estadistica-y-probabilidad' => 'data', 'data-dan-peluang' => 'data',
    'veri' => 'data', 'olasilik' => 'data', 'statistik-och-sannolikhet' => 'data',
    // trigonometry
    'trigonometry' => 'trigonometry', 'goniometria-e-trigonometria' => 'trigonometry', 'trigonometria' => 'trigonometry', 'trigonometri' => 'trigonometry',
    // calculus
    'calculus' => 'calculus', 'derivation' => 'calculus', 'analisi' => 'calculus', 'analisis' => 'calculus', 'kalkulus' => 'calculus',
    'limit-ve-turev' => 'calculus', 'derivata-och-integraler' => 'calculus', 'differenzial-und-integralrechnung' => 'calculus',
    // word problems
    'word-problems' => 'word-problems', 'sachaufgaben' => 'word-problems', 'problemes' => 'word-problems', 'problemi' => 'word-problems',
    'problemas' => 'word-problems', 'soal-cerita' => 'word-problems', 'problemlosning' => 'word-problems',
);
/* science topic slugs (topic_defs_science) are the same in every country */
const MQ_SCI_FIELD = array('matter' => 'matter', 'forces-and-motion' => 'forces-and-motion', 'energy' => 'energy', 'waves-and-light' => 'waves-and-light',
                           'living-things-and-ecosystems' => 'living-things', 'earth-and-space' => 'earth-and-space', 'earths-systems' => 'earth-and-space');

/* fields of one unit (needs inc/topics.php). The first one is the main field. */
function unit_fields($country, $subject, $slug) {
    $out = array();
    $map = $subject === 'science' ? MQ_SCI_FIELD : MQ_TOPIC_FIELD;
    foreach (unit_topic_slugs($slug, $country, $subject) as $t) {
        if (!isset($map[$t])) continue;
        foreach (explode(' ', $map[$t]) as $f) if (!in_array($f, $out, true)) $out[] = $f;
    }
    if (!$out && $subject !== 'science') {      /* units that are in no topic */
        foreach (array('/multiples-of-10|properties-of-operations/' => 'mul-div', '/money/' => 'measurement',
                       '/patterns/' => 'patterns', '/segment|analitik|uzaklik/' => 'geometry',
                       '/matri/' => 'algebra', '/kompleks/' => 'algebra') as $re => $f)
            if (preg_match($re, $slug)) { $out[] = $f; break; }
    }
    return $out;
}

/* field names for the ranking page: [group => [[key, name], …]] */
function field_menu($lang) {
    $i = array_search($lang === 'es-MX' ? 'es' : $lang, MQ_FIELD_LANGS, true);
    if ($i === false) $i = 0;
    $m = array();
    foreach (mq_fields() as $k => $v) $m[$v[0]][] = array($k, $v[1][$i]);
    return $m;
}

/* words for the field menu on the ranking page: [label, all fields, note] in MQ_FIELD_LANGS order */
function field_ui($lang) {
    $u = array(
        array('Field', 'All fields', 'Each country has its own units, so the questions are not the same. This compares the accuracy of all units in the same field.'),
        array('領域', '全部領域', '每個國家的單元不同，題目也不一樣。這裡比較的是同一個領域所有單元的答對率。'),
        array('领域', '全部领域', '每个国家的单元不同，题目也不一样。这里比较的是同一个领域所有单元的答对率。'),
        array('영역', '모든 영역', '나라마다 단원이 달라서 문제도 같지 않아요. 같은 영역에 있는 모든 단원의 정답률을 비교해요.'),
        array('Bidang', 'Semua bidang', 'Setiap negara punya bab sendiri, jadi soalnya tidak sama. Di sini dibandingkan persentase benar semua bab dalam bidang yang sama.'),
        array('Alan', 'Tüm alanlar', 'Her ülkenin üniteleri farklıdır, bu yüzden sorular aynı değildir. Burada aynı alandaki tüm ünitelerin başarı oranı karşılaştırılır.'),
        array('Område', 'Alla områden', 'Varje land har egna avsnitt, så frågorna är inte desamma. Här jämförs andelen rätt i alla avsnitt inom samma område.'),
        array('Bereich', 'Alle Bereiche', 'Jedes Land hat eigene Themen, die Aufgaben sind also nicht gleich. Verglichen wird die Trefferquote aller Themen im selben Bereich.'),
        array('Domaine', 'Tous les domaines', 'Chaque pays a ses propres chapitres : les questions ne sont donc pas les mêmes. On compare le taux de réussite de tous les chapitres du même domaine.'),
        array('Ambito', 'Tutti gli ambiti', 'Ogni paese ha i suoi argomenti, quindi le domande non sono le stesse. Qui si confronta la percentuale di risposte giuste di tutti gli argomenti dello stesso ambito.'),
        array('Área', 'Todas las áreas', 'Cada país tiene sus propios temas, así que las preguntas no son iguales. Aquí se compara el porcentaje de aciertos de todos los temas de la misma área.'),
        array('Área', 'Todas as áreas', 'Cada país tem seus próprios conteúdos, então as perguntas não são iguais. Aqui se compara a porcentagem de acertos de todos os conteúdos da mesma área.'),
    );
    $i = array_search($lang === 'es-MX' ? 'es' : $lang, MQ_FIELD_LANGS, true);
    return $u[$i === false ? 0 : $i];
}
