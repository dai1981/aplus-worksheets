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

function topic_defs($country = null) {
    if ($country === 'tw') return topic_defs_tw();
    return array(
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
            'in' => '/(^|-)ratios?(-|$)|(^|-)rates?(-|$)|proportion|scaling|speed/', 'out' => '/trigonometric/',
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
            'in' => '/add|subtract|number-bonds|make-10|ways-to-make|decompose-numbers|decomposing-numbers|ten-more|change-in-quantity|word-problems|part-part-whole|taking-away/',
            'out' => '/fraction|decimal|integer|polynomial|mixed-num|multiplicative|ratio|segment-addition|quadratic|multiplication-and-division-word|measurement-word/',
            'blurb' => 'Number bonds and facts to 20, mental strategies, adding and subtracting with regrouping, and multi-step word problems.',
            'blurb_gb' => 'Number bonds and facts to 20, mental strategies, column addition and subtraction, and multi-step word problems.'),
        'place-value' => array('name' => 'Place Value and Numbers',
            'in' => '/place-value|numbers-to|(^|-)count|tens-and-ones|compare-t|comparing-numbers|writing-numbers|roman|large-numbers|billions|ordinal|odd-and-even|skip-counting|powers-and-large|subitising|comparing-quantities|ordering-numbers/',
            'out' => '/money|fraction|sort-and-count|decompose|decomposing/',
            'blurb' => 'Counting, tens and ones, place value to millions and beyond, comparing and ordering numbers, and odd and even numbers.'),
        'rounding-and-estimation' => array('name' => 'Rounding and Estimation',
            'in' => '/round|estimat|benchmark/', 'out' => '/^$/',
            'blurb' => 'Rounding to the nearest 10, 100 and 1000, rounding decimals, and estimating to check answers.'),
        'order-of-operations' => array('name' => 'Order of Operations',
            'in' => '/order-of-operations|numerical-expressions/', 'out' => '/^$/',
            'blurb' => 'Which operation comes first, working with brackets and exponents, and writing number problems as one expression.'),
        'factors-and-multiples' => array('name' => 'Factors, Multiples and Primes',
            'in' => '/factor|prime|gcf|multiples|divisib/', 'out' => '/multiples-of-10|(?<!prime-)factoris|factoring|missing-factors/',
            'blurb' => 'Factors and multiples, prime and composite numbers, common factors and common multiples.'),
        'exponents-and-roots' => array('name' => 'Exponents and Square Roots', 'name_gb' => 'Powers, Roots and Indices',
            'in' => '/exponent|irrational|square-root|squares-cubes|perfect-square|cube-root|scientific|powers|square-numbers|indices|index-|standard-form|radical|logarithm/', 'out' => '/powers-of-10/',
            'blurb' => 'Powers and exponents, perfect squares, square roots and cube roots, and scientific notation.',
            'blurb_gb' => 'Powers and index laws, square and cube numbers, square roots and cube roots, and standard form.'),
        'integers' => array('name' => 'Integers and Negative Numbers',
            'in' => '/integer|negative|absolute|rational-number|real-numbers/', 'out' => '/irrational|absolute-value-equations|absolute-deviation/',
            'blurb' => 'Negative numbers on the number line, comparing integers, absolute value, and adding, subtracting, multiplying and dividing integers.'),
        'algebra' => array('name' => 'Algebra, Equations and Patterns',
            'in' => '/pattern|algebra|independent-and-dependent-quantities|expression|equation|inequalit|slope|function|equal-sign|equality|equal-and-not|number-sentences|relation|polynomial|missing-numbers|sequence|substitution|expanding|expansion|subject-of|simultaneous|quadratic|straight-line|linear-graphs|exponential-graphs|domain-and-range|logarithm|complex-numbers|binomial-theorem|input-output|multi-step-problems/',
            'out' => '/order-of-operations-and|angle-relationships|correlation|equations-of-circles|trigonometric/',
            'blurb' => 'Number and shape patterns, the equal sign, missing numbers, expressions, one- and two-step equations, inequalities and linear relations.'),
        'quadratics' => array('name' => 'Quadratic Equations and Functions',
            'in' => '/quadratic|factoring-polynomials/', 'out' => '/^$/',
            'blurb' => 'Factoring quadratics, solving by factoring, square roots, completing the square and the quadratic formula, and graphing parabolas.',
            'blurb_gb' => 'Expanding and factorising quadratics, solving quadratic equations, completing the square and quadratic graphs.'),
        'money' => array('name' => 'Money and Financial Literacy',
            'in' => '/money|coins|financial|budget|best-buys|interest|exchange|discount-gst|credit-and-loans|saving-and-investing|paying-for-college/', 'out' => '/^$/',
            'blurb' => 'Counting coins and bills, making change, budgets, discounts and tax, saving and interest.',
            'blurb_gb' => 'Counting coins and notes, giving change, budgets, discounts, saving and interest.'),
        'time' => array('name' => 'Time',
            'in' => '/time|clock|calendar|days-weeks|timetables|duration|elapsed/', 'out' => '/times-table|speed-distance|over-time/',
            'blurb' => 'Telling time on analog and digital clocks, a.m. and p.m., the 24-hour clock, elapsed time and calendars.',
            'blurb_gb' => 'Telling the time on analogue and digital clocks, the 12- and 24-hour clock, how long things take, and calendars.'),
        'measurement' => array('name' => 'Measurement',
            'in' => '/measur|length|mass|capacity|metric|convert|scales|conversion|units-and|liquid-volume|weight/', 'out' => '/angle|converting-fractions|geometric|arc-length|trigonometric/',
            'blurb' => 'Measuring length, mass and capacity, reading scales, and converting between units.'),
        'area-and-perimeter' => array('name' => 'Area and Perimeter',
            'in' => '/area|perimeter/', 'out' => '/surface-area-nets|surface-area-of|surface-area-and/',
            'blurb' => 'Perimeter by counting and by adding sides, area of rectangles, triangles and other polygons, and area of circles.'),
        'volume' => array('name' => 'Volume and Surface Area',
            'in' => '/volume|surface-area/', 'out' => '/liquid-volume/',
            'blurb' => 'Volume by counting cubes, volume of cubes, cuboids, prisms and cylinders, capacity, and surface area from nets.'),
        'angles' => array('name' => 'Angles',
            'in' => '/(^|-)angles?(-|$)|turns|transversal/', 'out' => '/^$/',
            'blurb' => 'Right, acute and obtuse angles, measuring with a protractor, angles on a line and at a point, and angles in shapes.'),
        'shapes' => array('name' => '2D and 3D Shapes',
            'in' => '/shape|polygon|quadrilateral|triangle|circles|circumference|prism|3d|2d|nets|objects|parallelogram|rectangles-and-squares|lines-angles|perpendicular|congruence|classify-two|classifying-two|pythagor|trigonometr|arcs-and|elevations|law-of-sines|points-lines|cross-section/',
            'out' => '/circle-graph|number-shape|composite-area|similar-shapes|area-of|trigonometric/',
            'blurb' => 'Naming and sorting 2D shapes and 3D objects, sides and vertices, triangles and quadrilaterals, circles, nets and solids.'),
        'circles' => array('name' => 'Circles',
            'in' => '/circle|circum|arc-length|arcs-and|sector/', 'out' => '/circle-graph/',
            'blurb' => 'Parts of a circle, circumference and area, arc length and sectors, central and inscribed angles, tangents and equations of circles.',
            'blurb_gb' => 'Parts of a circle, circumference and area, arcs and sectors, angles in circles and tangents.'),
        'congruence-and-similarity' => array('name' => 'Congruence and Similarity',
            'in' => '/congruen|similar/', 'out' => '/^$/',
            'blurb' => 'Congruent figures, the SSS, SAS, ASA, AAS and HL shortcuts, similar figures, scale factors and similar triangles.'),
        'symmetry-and-transformations' => array('name' => 'Symmetry and Transformations',
            'in' => '/symmetr|transform|reflection|translation|tessellation|scale-|similar|dilation/', 'out' => '/properties-of-circles/',
            'blurb' => 'Lines of symmetry, slides, flips and turns, combining transformations, tessellations and scale drawings.'),
        'coordinates-and-position' => array('name' => 'Coordinates and Position',
            'in' => '/coordinat|cartesian|position|direction|maps|location|grid-ref|bearing|loci|distance-and-midpoint|equations-of-circles|conic-sections/', 'out' => '/composition/',
            'blurb' => 'Position and direction words, maps and grid references, plotting points and the coordinate plane.'),
        'data-and-graphs' => array('name' => 'Data and Graphs',
            'in' => '/graph|chart|data|plot|stem-and-leaf|tally|pictogra|mean|median|average|statistic|central-tendency|sorting|sort-and-count|two-way|organize|sampling|random-samples|distribution|correlation|statistical-studies|standard-deviation/',
            'out' => '/straight-line-graphs|linear-graphs|quadratic-graphs|graphing-|graphs-of-sine|exponential-graphs/',
            'blurb' => 'Tally charts, picture graphs and bar graphs, line plots and line graphs, pie charts, the mean, median and mode, and random samples.',
            'blurb_gb' => 'Tally charts, pictograms and bar charts, line graphs and pie charts, and the mean.'),
        'vectors-and-matrices' => array('name' => 'Vectors and Matrices',
            'in' => '/vector|matri/', 'out' => '/^$/',
            'blurb' => 'Vectors in component form, magnitude and direction, vector operations and the dot product, matrix operations, determinants and inverse matrices.'),
        'trigonometry' => array('name' => 'Trigonometry',
            'in' => '/trigonometr|(^|-)sines?(-|$)|cosine|unit-circle|sum-and-difference-formulas|angles-of-elevation|three-dimensions/', 'out' => '/^$/',
            'blurb' => 'Sine, cosine and tangent in right triangles, the laws of sines and cosines, radians and the unit circle, and graphs of sine and cosine.'),
        'probability' => array('name' => 'Probability',  'name_au' => 'Chance and Probability',
            'in' => '/probab|chance|sample-spaces|likelihood|permutations-and-combinations|expected-value/', 'out' => '/^$/',
            'blurb' => 'Likelihood words, spinners and number cubes, probability as a fraction, experiments and tree diagrams.'),
    );
}

/* British spelling for these countries */
function topic_gb($country) { return in_array($country, array('uk', 'au', 'sg'), true); }

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
    return $units[0]['country'] === 'tw' ? $first . '到' . $last : $first . ' to ' . $last;
}

/* lower case for use inside a sentence, keeping "2D", "3D" */
function topic_lc($name) {
    return preg_replace_callback('/\b[A-Za-z]+\b/', function ($m) { return strtolower($m[0]); }, $name);
}
